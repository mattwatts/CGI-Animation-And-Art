"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v32.py
MODE:   Nursery (Industrial Palette)
TARGET: Turbocharger (Radial Dynamics / Thermodynamics)
STYLE:  "The Air Pump" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Wedge, Rectangle
import os

# --- 1. THE INDUSTRIAL PALETTE ---
BG_COLOR = "#101010"        # Workshop Dark
TURBINE_IRON = "#502010"    # Rusted Cast Iron
TURBINE_HOT = "#FF4500"     # Glowing Red
COMPRESSOR_ALU = "#E0E0E0"  # Clean Aluminum
SHAFT_STEEL = "#707070"
OIL_FILM = "#FFD700"        # Gold Bearing
EXHAUST_GAS = "#FF2200"     # Hot Inlet
EXHAUST_SPENT = "#555555"   # Grey Outlet
AIR_COLD = "#00FFFF"        # Cyan Inlet
AIR_BOOST = "#00FF00"       # Compressed Green Outlet

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 15
TOTAL_FRAMES = FPS * DURATION

class TurboSim:
    def __init__(self):
        self.rpm = 0.0      # Current Speed
        self.angle = 0.0    # Rotation
        self.lag_timer = 0  # Spool up delay
        
        self.particles_hot = []
        self.particles_cold = []
        
        # Geometry
        self.t_center = [-4, 0] # Turbine Location
        self.c_center = [4, 0]  # Compressor Location
        self.radius = 3.5
        
    def update(self, frame_idx):
        # 1. Physics (Lag & Spool)
        # Frames 0-60: Idle
        # Frames 60-200: Spool Up (Exponential)
        # Frames 200+: Full Boost
        
        target_rpm = 5.0 # Low idle
        
        if frame_idx > 60:
            # Throttle applied
            ramp = (frame_idx - 60) / 100.0
            target_rpm = 5.0 + (ramp**2 * 45.0) # Curve up to 50
            
        if target_rpm > 50.0: target_rpm = 50.0 # Rev limiter
        
        # Smooth RPM (Inertia)
        self.rpm += (target_rpm - self.rpm) * 0.05
        self.angle += self.rpm
        
        # 2. Particle Systems
        
        # A. TURBINE (Hot Side)
        # Flow: Radial In -> Axial Out (Center)
        # Spawn at perimeter
        spawn_rate = int(self.rpm / 2) + 1
        for _ in range(spawn_rate):
            # Spawn on ring
            theta = np.random.uniform(0, 2*np.pi)
            r = self.radius * 0.95
            px = self.t_center[0] + r * np.cos(theta)
            py = self.t_center[1] + r * np.sin(theta)
            
            self.particles_hot.append({
                'x': px, 'y': py,
                'vx': 0, 'vy': 0,
                'life': 1.0,
                'stage': 'inlet' # inlet -> wheel -> outlet
            })
            
        # Update Hot Particles
        for p in self.particles_hot:
            # Vector to center
            dx = self.t_center[0] - p['x']
            dy = self.t_center[1] - p['y']
            dist = np.sqrt(dx*dx + dy*dy)
            
            # Spiral In
            # Tangential velocity (Spin with wheel)
            msg_rpm = self.rpm * 0.1
            
            # Cross product logic for tangent
            tx = -dy 
            ty = dx
            
            # Normalize tangent
            if dist > 0.1:
                tx /= dist
                ty /= dist
            
            # Radial velocity (Suction to center)
            # Higher RPM = Faster flow
            suction = 0.05 + (self.rpm * 0.01)
            
            p['x'] += (dx/dist * suction) + (tx * msg_rpm * 0.5)
            p['y'] += (dy/dist * suction) + (ty * msg_rpm * 0.5)
            
            # Color Logic
            # Hot Red at edge -> Cooling Grey at center
            if dist < 1.0:
                p['color'] = EXHAUST_SPENT
                p['stage'] = 'outlet'
                # Eject axially (visualize as fading/shrinking)
                p['life'] -= 0.1
            else:
                p['color'] = EXHAUST_GAS
                
        self.particles_hot = [p for p in self.particles_hot if p['life'] > 0]
        
        # B. COMPRESSOR (Cold Side)
        # Flow: Axial In (Center) -> Radial Out
        for _ in range(spawn_rate):
            # Spawn at center
            px = self.c_center[0] + np.random.uniform(-0.5, 0.5)
            py = self.c_center[1] + np.random.uniform(-0.5, 0.5)
            
            self.particles_cold.append({
                'x': px, 'y': py,
                'life': 1.0, 
                'color': AIR_COLD
            })
            
        for p in self.particles_cold:
            # Vector from center
            dx = p['x'] - self.c_center[0]
            dy = p['y'] - self.c_center[1]
            dist = np.sqrt(dx*dx + dy*dy)
            if dist == 0: dist = 0.001
            
            # Radial Out Force (Centrifugal)
            force = self.rpm * 0.015
            
            # Tangential Spin
            tx = -dy
            ty = dx
            
            # Normalize
            tx /= dist
            ty /= dist
            
            # Move
            norm_x = dx/dist
            norm_y = dy/dist
            
            p['x'] += (norm_x * force) + (tx * self.rpm * 0.1)
            p['y'] += (norm_y * force) + (ty * self.rpm * 0.1)
            
            # Color Logic (Pressure)
            # Cyan -> Green
            if dist > 2.0:
                p['color'] = AIR_BOOST # Compressed
            else:
                p['color'] = AIR_COLD
                
            if dist > self.radius:
                p['life'] -= 0.1
                
        self.particles_cold = [p for p in self.particles_cold if p['life'] > 0]


    def render(self, frame_idx, ax):
        ax.set_xlim(-10, 10)
        ax.set_ylim(-6, 6)
        
        # 1. The Shaft (Connecting the two)
        ax.add_patch(Rectangle((-4, -0.4), 8, 0.8, color=SHAFT_STEEL, zorder=1))
        # Bearing Housing (Center)
        ax.add_patch(Rectangle((-1.5, -1.5), 3, 3, color="#303030", zorder=2))
        # Oil Feed
        ax.add_patch(Circle((0,0), 0.5, color=OIL_FILM, zorder=3))
        
        # 2. Turbine (Left, Hot)
        # Draw Housing Shell
        t_shell = Circle((self.t_center[0], self.t_center[1]), self.radius, color=TURBINE_IRON, alpha=0.3)
        ax.add_patch(t_shell)
        
        # Draw Particles UNDER wheel
        for p in self.particles_hot:
            ax.add_patch(Circle((p['x'], p['y']), 0.15, color=p['color'], alpha=0.8))
            
        # Draw Wheel (Rotated)
        self.draw_impeller(ax, self.t_center, self.radius*0.8, self.angle, 11, TURBINE_HOT)
        
        # 3. Compressor (Right, Cold)
        # Housing Shell
        c_shell = Circle((self.c_center[0], self.c_center[1]), self.radius, color=COMPRESSOR_ALU, alpha=0.3)
        ax.add_patch(c_shell)
        
        # Draw Particles UNDER wheel
        for p in self.particles_cold:
            ax.add_patch(Circle((p['x'], p['y']), 0.15, color=p['color'], alpha=0.8))
            
        # Draw Wheel
        # Note: Compressor blades curve opposite to turbine usually, or same?
        # Let's flip curvature for visual distinction
        self.draw_impeller(ax, self.c_center, self.radius*0.8, self.angle, 9, COMPRESSOR_ALU, flip=True)

        # 4. HUD
        bar_len = (self.rpm / 50.0) * 8.0
        # Boost Gauge
        ax.add_patch(Rectangle((-4, -5.5), 8, 0.5, color="#303030"))
        ax.add_patch(Rectangle((-4, -5.5), bar_len, 0.5, color=AIR_BOOST))
        
        info = f"RPM: {int(self.rpm * 2000)}"
        ax.text(0, -4.5, info, color="white", ha='center', fontfamily='monospace')

        ax.set_aspect('equal')
        ax.set_axis_off()
        
        out_dir = "logic_garden_turbo_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"turbo_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

    def draw_impeller(self, ax, center, radius, angle_deg, blades, color, flip=False):
        # Draw blades as curved lines radiating from center
        cx, cy = center
        
        rad_offset = np.radians(angle_deg)
        
        for i in range(blades):
            blade_ang = rad_offset + (i * (2*np.pi / blades))
            
            # Curve points
            pts = []
            steps = 10
            for j in range(steps):
                r = (j / steps) * radius
                # Curvature function
                # Linear angle change + twist
                twist = (j/steps) * 1.0 # 1 radian twist
                if flip: twist *= -1
                
                a = blade_ang + twist
                
                px = cx + r * np.cos(a)
                py = cy + r * np.sin(a)
                pts.append([px, py])
                
            # Draw line
            pts = np.array(pts)
            ax.plot(pts[:,0], pts[:,1], color=color, linewidth=3)
            
        # Nut
        ax.add_patch(Circle(center, radius*0.15, color=SHAFT_STEEL, zorder=10))


# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Spooling Turbocharger...")
    
    sim = TurboSim()
    
    for i in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(16, 8), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        sim.update(i)
        sim.render(i, ax)
        plt.close()
        
        if i % 30 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
