"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v31.py
MODE:   Nursery (Automotive Palette)
TARGET: 4-Stroke Otto Cycle (Intake, Compression, Power, Exhaust)
STYLE:  "The Iron Heart" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Wedge
import os

# --- 1. THE AUTOMOTIVE PALETTE ---
BG_COLOR = "#101010"        # Oil Sump Black
CYLINDER_COLOR = "#303030"  # Cast Iron
PISTON_COLOR = "#A0A0A0"    # Aluminum
ROD_COLOR = "#707070"       # Forged Steel
CRANK_COLOR = "#505050"     # Iron
INTAKE_GAS = "#00FFFF"      # Cyan (Fuel/Air)
COMPRESSED_GAS = "#FFFF00"  # Yellow (Hot)
EXPLOSION = "#FFFFFF"       # Flash
EXHAUST_SMOKE = "#555555"   # Grey
VALVE_Metal = "#C0C0C0"

# --- 2. CONFIGURATION ---
FPS = 30
RPM = 600                   # Render speed (not real physics speed)
CYCLES = 2                  # How many full 720 deg cycles
FRAMES_PER_REV = 90         # Frames for 360 degrees
TOTAL_FRAMES = FRAMES_PER_REV * 2 * CYCLES

class EngineSim:
    def __init__(self):
        # Geometry
        self.bore = 6.0
        self.stroke = 8.0
        self.crank_r = self.stroke / 2.0
        self.rod_l = 10.0
        
        self.angle = 0.0 # 0-720
        self.particles = [] # Gas particles

    def get_piston_y(self, theta_rad):
        # Piston Position from Crank Center
        # y = r cos(a) + sqrt(l^2 - (r sin(a))^2)
        # However, typically 0 deg is TDC (Top Dead Center).
        # At 0 deg, cos(0)=1. y = r + l. (Max height).
        # At 180 deg, cos(180)=-1. y = -r + l. (Min height).
        
        # NOTE: Standard math usually puts 0 at East.
        # Let's adjust input so 0 = Up (TDC).
        # Standard: x = r cos t, y = r sin t.
        # We want y axis motion. 
        # Using Law of Cosines based geometry:
        # y = r cos(theta) + sqrt(L^2 - r^2 sin^2(theta))
        
        # Let theta=0 be TDC.
        t = theta_rad
        term1 = self.crank_r * np.cos(t)
        term2 = np.sqrt(self.rod_l**2 - (self.crank_r * np.sin(t))**2)
        return term1 + term2

    def update(self, frame_idx):
        # Advance Angle
        deg_per_frame = 360.0 / FRAMES_PER_REV
        self.angle = (frame_idx * deg_per_frame) % 720.0
        
        # Phase Logic
        # 0-180: INTAKE (Valve 1 Open)
        # 180-360: COMPRESSION (Valves Closed)
        # 360-540: POWER (Valves Closed, Spark at 360)
        # 540-720: EXHAUST (Valve 2 Open)
        
        # Particle Simulation
        # INTAKE: Spawn blue particles at top, suck them down
        if 0 <= self.angle < 180:
            if frame_idx % 2 == 0:
                # Spawn in intake runner
                self.particles.append({
                    'x': -1.5 + np.random.uniform(-0.5, 0.5), 
                    'y': 11.0, 
                    'color': INTAKE_GAS, 
                    'state': 'fresh'
                })
                
        # Move Particles
        # Calculate piston Y for boundary
        rad = np.radians(self.angle)
        pist_y = self.get_piston_y(rad)
        chamber_ceil = 10.0
        
        # If EXHAUST: Push particles up and out right
        is_exhaust = (540 <= self.angle < 720)
        is_combustion = (360 <= self.angle < 540)
        is_compression = (180 <= self.angle < 360)
        
        for p in self.particles:
            # Boundary check logic
            
            # Physics scaling based on phase
            if 0 <= self.angle < 180: # Suck
                 p['y'] -= 0.5 # Flow down
                 # Jiggle
                 p['x'] += np.random.uniform(-0.2, 0.2)
                 
            elif is_compression:
                # Compress logic
                # Scale Y position to fit in shrinking volume
                # Normalized pos between piston and roof
                # Simply: If p['y'] < pist_y, push it up
                if p['y'] < pist_y + 0.5:
                    p['y'] = pist_y + 0.5 + np.random.rand()
                
                # Heating Color
                # Progress 180 -> 360
                prog = (self.angle - 180) / 180.0
                if prog > 0.5: p['color'] = COMPRESSED_GAS
                
            elif is_combustion:
                # Expansion
                # Flash
                if 360 <= self.angle < 370:
                    p['color'] = EXPLOSION
                elif 370 <= self.angle < 400:
                    p['color'] = "#FF4500" # Red/Orange
                else:
                    p['color'] = "#888888" # Cooling smoke
                
                # Spread out
                p['y'] *= 1.01 # Expand
                if p['y'] > pist_y: p['y'] = pist_y # Wait, piston moving down
                
            elif is_exhaust:
                # Push Out
                if p['y'] < pist_y + 0.5:
                    p['y'] = pist_y + 0.5
                
                # Flow to exhaust valve (Right side)
                # Valve at x=1.5, y=10
                dx = 1.5 - p['x']
                dy = 12.0 - p['y'] # Target up and out
                
                if p['y'] > 8.0:
                    p['x'] += dx * 0.2
                    p['y'] += dy * 0.2
                else:
                    p['y'] += 0.5 # Just go up until near valve
                    
                p['color'] = EXHAUST_SMOKE

        # Clean dead particles
        self.particles = [p for p in self.particles if p['y'] < 14.0 and p['x'] > -5 and p['x'] < 5]
        # On exhaust phase, if they go out the runner, kill them
        if is_exhaust:
             self.particles = [p for p in self.particles if not (p['x'] > 1.0 and p['y'] > 11.0)]

    def render(self, frame_idx, ax):
        ax.set_xlim(-8, 8)
        ax.set_ylim(-6, 16)
        
        # 1. Crankshaft
        theta = np.radians(self.angle)
        cx = 0
        cy = 0
        
        # Crank Pin
        # Angle 0 = Top. So math angle is 90?
        # Let's use standard trig: x = r sin(t), y = r cos(t) for TDC at 0.
        px = self.crank_r * np.sin(theta)
        py = self.crank_r * np.cos(theta)
        
        # Draw Crank Wheel
        ax.add_patch(Circle((0,0), self.crank_r + 1.0, color="#202020"))
        # Counterweight (Opposite to pin)
        ox = -px * 0.5
        oy = -py * 0.5
        wedge = Wedge((0,0), self.crank_r, np.degrees(theta)+90, np.degrees(theta)+270, width=self.crank_r, color="#404040")
        ax.add_patch(wedge)
        
        # Draw Pin
        ax.add_patch(Circle((px, py), 0.8, color="#505050"))
        
        # 2. Piston & Rod
        pist_y = self.get_piston_y(theta)
        
        # Rod
        # From (px, py) to (0, pist_y)
        ax.plot([px, 0], [py, pist_y], color=ROD_COLOR, linewidth=12, zorder=3)
        ax.plot([px, 0], [py, pist_y], color="#909090", linewidth=4, zorder=4) # Highlight
        
        # Piston Head
        ph_w = 5.5
        ph_h = 4.0
        # Pivot point is usually mid-piston. get_piston_y calculates pin height.
        # Piston extends above and below pin.
        
        piston_poly = [
            [-ph_w/2, pist_y - 1.5],
            [ph_w/2, pist_y - 1.5],
            [ph_w/2, pist_y + 2.5],
            [-ph_w/2, pist_y + 2.5]
        ]
        ax.add_patch(Polygon(piston_poly, facecolor=PISTON_COLOR, edgecolor="black", zorder=5))
        
        # Rings
        ax.plot([-ph_w/2, ph_w/2], [pist_y + 1.8, pist_y + 1.8], color="#404040")
        ax.plot([-ph_w/2, ph_w/2], [pist_y + 1.2, pist_y + 1.2], color="#404040")
        
        # Pin
        ax.add_patch(Circle((0, pist_y), 0.6, color="#404040", zorder=6))

        # 3. Cylinder Block
        cyl_top = 10.0
        cyl_bot = -2.0
        wall_thick = 1.0
        
        # Left Wall
        ax.add_patch(Rectangle((-3.0 - wall_thick, cyl_bot), wall_thick, cyl_top - cyl_bot, color=CYLINDER_COLOR))
        # Right Wall
        ax.add_patch(Rectangle((3.0, cyl_bot), wall_thick, cyl_top - cyl_bot, color=CYLINDER_COLOR))
        
        # Head (Roof)
        head_h = 3.0
        ax.add_patch(Rectangle((-4.0, cyl_top), 8.0, head_h, color=CYLINDER_COLOR))
        
        # 4. Valves
        # Centers: Intake (-1.5), Exhaust (1.5)
        # Cam Logic:
        # Intake open 0-180. Peak at 90.
        # Exhaust open 540-720. Peak at 630.
        
        iv_lift = 0.0
        ev_lift = 0.0
        
        if 0 <= self.angle < 180:
            iv_lift = np.sin(theta) * 1.5 # Simple cam profile
            if iv_lift < 0: iv_lift = 0
            
        if 540 <= self.angle < 720:
             # theta for 540 is 3pi. sin(3pi) = 0.
             # Phase shift: sin(theta - 3pi) ? 
             # 540 = 1.5 cycles.
             # Angle 630 (peak) -> sin(90) = 1.
             # 630 deg = 3.5 pi.
             
             ev_lift = np.sin(np.radians(self.angle - 540)) * 1.5
             if ev_lift < 0: ev_lift = 0
             
        # Draw Valves (T-shape)
        # Intake
        iv_x = -1.5
        iv_stem_top = 12.0
        iv_seat = 10.0
        iv_y = iv_seat - iv_lift
        
        ax.plot([iv_x, iv_x], [iv_stem_top, iv_y], color=VALVE_Metal, linewidth=3)
        ax.add_patch(Polygon([ [iv_x-1, iv_y], [iv_x+1, iv_y], [iv_x, iv_y+0.5] ], color=VALVE_Metal))
        
        # Exhaust
        ev_x = 1.5
        ev_stem_top = 12.0
        ev_y = iv_seat - ev_lift
        
        ax.plot([ev_x, ev_x], [ev_stem_top, ev_y], color=VALVE_Metal, linewidth=3)
        ax.add_patch(Polygon([ [ev_x-1, ev_y], [ev_x+1, ev_y], [ev_x, ev_y+0.5] ], color=VALVE_Metal))

        # 5. Particles
        for p in self.particles:
             ax.add_patch(Circle((p['x'], p['y']), 0.2, color=p['color'], alpha=0.7))
             
        # 6. Spark Plug & Combustion
        ax.plot([0, 0], [13, 10], color="white", linewidth=2)
        if 358 <= self.angle <= 365:
            # SPARK!
            ax.add_patch(Circle((0, 10), 0.8, color="#FFFFFF", zorder=10))
            ax.plot([0, np.random.uniform(-1,1)], [10, 9], color="#FFFF00", linewidth=2)

        # 7. HUD
        phase_txt = "PHASE: "
        bg_col = "black"
        txt_col = "white"
        
        if 0 <= self.angle < 180: 
            phase_txt += "INTAKE (SUCK)"
            txt_col = INTAKE_GAS
        elif 180 <= self.angle < 360: 
            phase_txt += "COMPRESSION (SQUEEZE)"
            txt_col = "#FFFF00"
        elif 360 <= self.angle < 540: 
            phase_txt += "POWER (BANG)"
            txt_col = "#FF4500"
        else: 
            phase_txt += "EXHAUST (BLOW)"
            txt_col = "#AAAAAA"
            
        ax.text(0, -5, phase_txt, color=txt_col, fontsize=15, ha='center',
                bbox=dict(facecolor=bg_col, edgecolor=txt_col))

        ax.set_aspect('equal')
        ax.set_axis_off()
        
        # Save
        out_dir = "logic_garden_engine_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"engine_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

from matplotlib.patches import Rectangle # Missing import fix

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Starting Engine...")
    
    sim = EngineSim()
    
    for i in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10, 10), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        sim.update(i)
        sim.render(i, ax)
        plt.close()
        
        if i % 30 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
