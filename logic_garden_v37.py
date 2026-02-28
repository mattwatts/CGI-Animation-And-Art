"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v37.py
MODE:   Nursery (Billet Aluminum Palette)
TARGET: Supercharger (Roots Blower Mechanics)
STYLE:  "The Parasite" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon
import os

# --- 1. THE BILLET PALETTE ---
BG_COLOR = "#101010"        # Engine Bay Dark
ROTOR_ALU = "#C0C0C0"       # Polished Aluminum
ROTOR_EDGE = "#404040"      # Machined Edge
CASE_WALL = "#303030"       # Cast Iron Housing
BELT_RUBBER = "#080808"     # Drive Belt
PULLEY_ANOD = "#D00000"     # Red Anodized
AIR_COLD = "#00FFFF"        # Cyan
AIR_HOT = "#00FF00"         # Green (Compressed)

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 15
TOTAL_FRAMES = FPS * DURATION

class SuperchargerSim:
    def __init__(self):
        self.rpm = 0.0
        self.angle = 0.0 # Rotor position
        
        # Geometry
        self.c1 = [-2.2, 0] # Left Rotor Center
        self.c2 = [2.2, 0]  # Right Rotor Center
        self.rotor_r = 3.8  # Outer Radius
        
        self.particles = []
        
    def update(self, frame_idx):
        # 1. Throttle Logic (Instant Response, unlike Turbo)
        target_rpm = 10.0
        if frame_idx > 30:
            target_rpm = 60.0 # Instant jump
            
        self.rpm += (target_rpm - self.rpm) * 0.2 # Fast response
        self.angle += self.rpm * 0.2
        
        # 2. Particle Logic (Positive Displacement)
        # Spawn at Top (Intake)
        spawn_rate = int(self.rpm * 0.1) + 1
        for _ in range(spawn_rate):
            # Random X across the top width
            px = np.random.uniform(-4.0, 4.0)
            self.particles.append({
                'x': px, 
                'y': 6.0, 
                'vx': 0, 'vy': -0.2, 
                'state': 'intake',
                'color': AIR_COLD
            })
            
        # Move Particles
        for p in self.particles:
            
            # A. Intake (Falling)
            if p['state'] == 'intake':
                # Suck down
                p['vy'] -= 0.05
                p['y'] += p['vy']
                
                # Hit Rotors?
                # Check distance to rotor centers
                d1 = np.sqrt((p['x']-self.c1[0])**2 + (p['y']-self.c1[1])**2)
                d2 = np.sqrt((p['x']-self.c2[0])**2 + (p['y']-self.c2[1])**2)
                
                if d1 < self.rotor_r or d2 < self.rotor_r:
                    # Decide which side to get trapped in
                    # Left rotor spins CW (pushes left and down)
                    # Right rotor spins CCW (pushes right and down)
                    
                    if p['x'] < 0:
                        p['state'] = 'trapped_left'
                        # Calculate angular position relative to C1
                        p['theta_offset'] = np.arctan2(p['y']-self.c1[1], p['x']-self.c1[0])
                        # Store current rotor angle to sync
                        p['capture_angle'] = -self.angle # CW
                        p['r_offset'] = d1
                    else:
                        p['state'] = 'trapped_right'
                        p['theta_offset'] = np.arctan2(p['y']-self.c2[1], p['x']-self.c2[0])
                        p['capture_angle'] = self.angle # CCW
                        p['r_offset'] = d2

            # B. Trapped (Moving with Rotor)
            elif p['state'] == 'trapped_left':
                # Rotor 1 spins CW (Negative angle direction)
                # Angle delta
                current_rot = -np.radians(self.angle)
                # Lock geometric position
                # Is the particle strictly locked? 
                # Ideally yes, "Positive Displacement"
                
                # Update angle: Initial theta + change in rotor angle
                # Delta = current_rot - capture_rot (in rads)
                # It's easier to just track total rotation
                
                # Let's say rotor rotates d_theta per frame.
                d_theta = -np.radians(self.rpm * 0.2)
                p['theta_offset'] += d_theta
                
                # New Position
                p['x'] = self.c1[0] + p['r_offset'] * np.cos(p['theta_offset'])
                p['y'] = self.c1[1] + p['r_offset'] * np.sin(p['theta_offset'])
                
                # Check for Release (Bottom)
                # If angle points down/middle approx -90deg (-pi/2) or less
                # Actually, release happens when it clears the casing at the bottom center
                if p['y'] < -2.0 and p['x'] > -2.0:
                    p['state'] = 'outlet'
                    p['vx'] = 0.5 # Spit towards center
                    p['vy'] = -1.0 # Blast down
                    p['color'] = AIR_HOT

            elif p['state'] == 'trapped_right':
                # Rotor 2 spins CCW
                d_theta = np.radians(self.rpm * 0.2)
                p['theta_offset'] += d_theta
                
                p['x'] = self.c2[0] + p['r_offset'] * np.cos(p['theta_offset'])
                p['y'] = self.c2[1] + p['r_offset'] * np.sin(p['theta_offset'])
                
                if p['y'] < -2.0 and p['x'] < 2.0:
                    p['state'] = 'outlet'
                    p['vx'] = -0.5
                    p['vy'] = -1.0
                    p['color'] = AIR_HOT

            # C. Outlet (Boost)
            elif p['state'] == 'outlet':
                p['y'] += p['vy']
                p['x'] += p['vx']
                p['vy'] -= 0.1 # Accelerate down
                
        # Clean
        self.particles = [p for p in self.particles if p['y'] > -8.0]

    def get_lobe_shape(self, center, rotation_deg, offset_angle=0):
        # 3-Lobe Epicycloid Approximation
        # x = r * cos(t)
        # r varies with 3*t
        
        pts = []
        steps = 100
        base_r = 2.5
        amp_r = 1.3
        
        rad_rot = np.radians(rotation_deg + offset_angle)
        
        for i in range(steps):
            t = (i / steps) * 2 * np.pi
            # Shape function
            # 3 lobes
            # We need them to mesh.
            # R1: cos(3t). R2: cos(3(t + pi/3))?
            
            # Simple visual approximation:
            r = base_r + amp_r * np.cos(3 * t)
            
            # Apply Rotation
            theta = t + rad_rot
            
            px = center[0] + r * np.cos(theta)
            py = center[1] + r * np.sin(theta)
            pts.append([px, py])
            
        return pts

    def render(self, frame_idx, ax):
        ax.set_xlim(-8, 8)
        ax.set_ylim(-8, 8)
        
        # 1. Housing
        # Case walls
        ax.add_patch(Rectangle((-5, -4), 0.5, 10, color=CASE_WALL)) # Left Wall
        ax.add_patch(Rectangle((4.5, -4), 0.5, 10, color=CASE_WALL))  # Right Wall
        
        # 2. Rotors
        # Left (CW)
        poly1 = self.get_lobe_shape(self.c1, -self.angle)
        ax.add_patch(Polygon(poly1, facecolor=ROTOR_ALU, edgecolor=ROTOR_EDGE, linewidth=2, zorder=5))
        ax.add_patch(Circle(self.c1, 0.4, color=ROTOR_EDGE, zorder=6)) # Shaft
        
        # Right (CCW)
        # Offset angle by 60 deg (180/3) to mesh?
        poly2 = self.get_lobe_shape(self.c2, self.angle, offset_angle=60)
        ax.add_patch(Polygon(poly2, facecolor=ROTOR_ALU, edgecolor=ROTOR_EDGE, linewidth=2, zorder=5))
        ax.add_patch(Circle(self.c2, 0.4, color=ROTOR_EDGE, zorder=6))
        
        # 3. Belt Drive (Visualized above)
        # Pulley
        pulley_pos = [0, 6.5] # Front mounted (projected to top 2D)
        # Let's draw the belt connecting the two shafts conceptually
        # Draw a big pulley in front of Left Rotor?
        # Let's draw it as an overlay circle
        ax.add_patch(Circle(self.c1, 1.5, color=PULLEY_ANOD, zorder=10))
        # Belt Segment
        ax.add_patch(Rectangle((-4, 0), 2, 8, color=BELT_RUBBER, alpha=0.0)) # Hidden in 2D cross section
        
        # Draw "Belt Speed" indicator lines on the pulley
        p_angle = np.radians(-self.angle)
        px = self.c1[0] + 1.2 * np.cos(p_angle)
        py = self.c1[1] + 1.2 * np.sin(p_angle)
        ax.plot([self.c1[0], px], [self.c1[1], py], color="black", linewidth=3, zorder=11)
        
        # 4. Particles
        for p in self.particles:
            ax.add_patch(Circle((p['x'], p['y']), 0.15, color=p['color'], alpha=0.8, zorder=4))
            
        # 5. HUD
        # Power Cost vs Gain
        cost_h = (self.rpm / 60.0) * 3.0
        gain_h = cost_h * 2.5 # Net positive
        
        # Parasitic Loss Bar (Red)
        ax.add_patch(Rectangle((-7.5, -6), 1, cost_h, color="#FF0000"))
        ax.text(-7, -7, "COST", color="#FF0000", ha='center', fontsize=10)
        
        # Power Gain Bar (Green)
        ax.add_patch(Rectangle((6.5, -6), 1, gain_h, color="#00FF00"))
        ax.text(7, -7, "GAIN", color="#00FF00", ha='center', fontsize=10)
        
        whine_txt = "WHINE: " + ("I" * int(self.rpm/5))
        ax.text(0, -7, whine_txt, color="white", ha='center', fontfamily='monospace', fontsize=12)

        ax.set_aspect('equal')
        ax.set_axis_off()
        
        out_dir = "logic_garden_supercharger_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"super_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Tensioning Belt...")
    
    sim = SuperchargerSim()
    
    for i in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(12, 12), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        sim.update(i)
        sim.render(i, ax)
        plt.close()
        
        if i % 30 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
