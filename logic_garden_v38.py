"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v38.py
MODE:   Nursery (Victorian Industrial Palette)
TARGET: Steam Locomotive (Linkage & Valve Gear Logic)
STYLE:  "The Iron Horse" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon, Wedge
import os

# --- 1. THE VICTORIAN PALETTE ---
BG_COLOR = "#050505"        # Soot Dark
IRON_BLACK = "#202020"      # Boiler Plate
STEEL_BRIGHT = "#D0D0D0"    # Rods
BRASS = "#B5A642"           # Domes/Trim
FIRE_RED = "#FF4500"        # Firebox Glow
STEAM_WHITE = "#FFFFFF"     # Exhaust
SMOKE_GREY = "#505050"      # Coal Smoke

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 15
TOTAL_FRAMES = FPS * DURATION

class SteamLocoSim:
    def __init__(self):
        self.angle = 0.0      # Wheel rotation
        self.speed = 0.0      # Angular velocity
        
        # Dimensions
        self.wheel_r = 2.5
        self.crank_r = 1.0    # Offset of the pin
        self.rod_l = 7.0      # Main rod length
        
        self.w1_center = [0, 0]      # Rear Driver
        self.w2_center = [5.5, 0]    # Front Driver
        self.cyl_center = [11.0, 1.0] # Cylinder x, Cylinder y (offset relative to visual center)
        
        self.smoke_particles = []
        self.chuff_timer = 0
        
    def update(self, frame_idx):
        # 1. Accelerate
        target_speed = 15.0 # Degrees per frame
        if frame_idx < 60:
            self.speed += 0.2
        else:
            self.speed = target_speed
            
        self.angle += self.speed
        self.angle %= 360.0
        
        # 2. Kinematics (Slider-Crank)
        # We need to find Piston Position based on W2 (Front Driver) angle.
        # W2 Center is at (5.5, 0)
        # Crank Pin is at (5.5 + r*cos(t), r*sin(t))
        
        rad = np.radians(self.angle)
        
        # Pin Position (Front Wheel)
        self.pin_x = self.w2_center[0] + self.crank_r * np.cos(rad)
        self.pin_y = self.w2_center[1] + self.crank_r * np.sin(rad)
        
        # Piston Pin (Crosshead)
        # It moves horizontally at y = self.pin_y (Assuming flat cylinder alignment for simplicity?)
        # Actually usually cylinder is center-aligned with wheel center. Let's assume y=0.
        
        # Solving for Crosshead X (ch_x) where y=0
        # Distance between Pin and Crosshead must be rod_l
        # (ch_x - pin_x)^2 + (0 - pin_y)^2 = rod_l^2
        # (ch_x - pin_x)^2 = rod_l^2 - pin_y^2
        # ch_x - pin_x = sqrt(...)
        # ch_x = pin_x + sqrt(...)
        
        term = self.rod_l**2 - self.pin_y**2
        if term < 0: term = 0 # Safety
        self.crosshead_x = self.pin_x + np.sqrt(term)
        
        # 3. Smoke Logic (The Chuff)
        # Chuff occurs at ends of stroke (0 and 180 degrees)
        # Detecting crossing of 0 or 180
        # Simple proximity check
        
        is_chuff = False
        if (self.angle < 15) or (abs(self.angle - 180) < 15):
             if self.chuff_timer == 0:
                 is_chuff = True
                 self.chuff_timer = 10 # Debounce
        
        if self.chuff_timer > 0: self.chuff_timer -= 1
        
        if is_chuff:
            # Spawn Smoke at Stack
            # Stack is at approx x=10, y=5
            for _ in range(5):
                self.smoke_particles.append({
                    'x': 9.5, 'y': 6.0,
                    'vx': -1.5 - np.random.rand(), # Moves left (train moves right effectively)
                    'vy': 0.5 + np.random.rand(),
                    'size': 0.5,
                    'life': 1.0,
                    'color': STEAM_WHITE
                })
                
        # Move Smoke
        for p in self.smoke_particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['size'] *= 1.05 # Expand
            p['life'] -= 0.02
            # Gravity/Wind
            p['vy'] += 0.01
            
        self.smoke_particles = [p for p in self.smoke_particles if p['life'] > 0]

    def draw_wheel(self, ax, center, angle_deg, is_driver=True):
        cx, cy = center
        r = self.wheel_r
        
        # Rim
        ax.add_patch(Circle((cx, cy), r, color=STEEL_BRIGHT, zorder=2))
        ax.add_patch(Circle((cx, cy), r*0.9, color="#101010", zorder=2)) # Inner
        
        # Spokes
        spoke_count = 12
        rad_offset = np.radians(angle_deg)
        for i in range(spoke_count):
            theta = rad_offset + i * (2*np.pi/spoke_count)
            sx = cx + r * np.cos(theta)
            sy = cy + r * np.sin(theta)
            ax.plot([cx, sx], [cy, sy], color="#101010", linewidth=2, zorder=2)
            
        # Balance Weight (Opposite directly to the pin)
        # Pin is at angle_deg
        # Weight is continuous wedge opposite
        wedge = Wedge((cx, cy), r*0.85, angle_deg+160, angle_deg+200, width=r*0.3, color="#101010", zorder=3)
        ax.add_patch(wedge)
        
        # Crank Pin
        px = cx + self.crank_r * np.cos(rad_offset)
        py = cy + self.crank_r * np.sin(rad_offset)
        
        return px, py # Return pin location

    def render(self, frame_idx, ax):
        ax.set_xlim(-4, 16)
        ax.set_ylim(-4, 10)
        
        # 0. Track
        ax.plot([-10, 20], [-2.6, -2.6], color="#505050", linewidth=5)
        # Dynamic ties (moving left)
        tie_offset = (frame_idx * 15) % 10
        for x in range(-5, 25, 2):
            tx = x - (tie_offset * 0.2)
            if tx < 16 and tx > -4:
                ax.add_patch(Rectangle((tx, -3.0), 0.5, 0.4, color="#302010"))

        # 1. Wheels (Rear, Front)
        pin1 = self.draw_wheel(ax, self.w1_center, self.angle)
        pin2 = self.draw_wheel(ax, self.w2_center, self.angle)
        
        # 2. Coupling Rod (Connecting the pins)
        ax.plot([pin1[0], pin2[0]], [pin1[1], pin2[1]], color=STEEL_BRIGHT, linewidth=8, zorder=10)
        # Pins
        ax.add_patch(Circle(pin1, 0.4, color=BRASS, zorder=11))
        ax.add_patch(Circle(pin2, 0.4, color=BRASS, zorder=11))
        
        # 3. Main Rod (Front Pin to Crosshead)
        # Crosshead calculation done in update
        ch_x = self.crosshead_x
        ch_y = 0 # Centerline
        
        ax.plot([pin2[0], ch_x], [pin2[1], ch_y], color=STEEL_BRIGHT, linewidth=6, zorder=12)
        ax.add_patch(Circle((ch_x, ch_y), 0.5, color="#505050", zorder=13)) # Wrist pin
        
        # 4. Piston Rod & Crosshead Guide
        # Rod extends from crosshead into cylinder (Right to Left in this setup? No, Cylinder is usually front)
        # Setup: Rear Wheel (0), Front Wheel (5.5). Cylinder usually at Front, approx x=10.
        # So Piston rod goes from Crosshead (which is behind cylinder) INTO cylinder (forward).
        # Crosshead x is approx 5.5 + 7 = 12.5.
        # Wait, schematic layout:
        # [Cab] [Wheel] [Wheel] [Cylinder] [Pilot]
        # x=      0       5        10
        # My crosshead calc put it at pin moves -1 to 1. crosshead is pin + rod.
        # If pin x is near 5.5. Rod is 7. Crosshead is near 12.5.
        # Cylinder should be around x=10? No, cylinder is forward of the wheels usually.
        # Let's visualize the block at x=10 to 14.
        
        # Cylinder Block
        ax.add_patch(Rectangle((10, -1), 4, 2, color=IRON_BLACK, zorder=5)) # Cylinder
        ax.add_patch(Rectangle((10.5, -0.8), 3, 1.6, color=BRASS, alpha=0.1, zorder=6)) # Gloss
        
        # Piston Rod
        # From Crosshead (approx 12, fluctuating) into cylinder?
        # Typically Main rod goes to Crosshead. Piston rod goes from Crosshead INTO cylinder.
        # If cylinder is at 13, and crosshead is at 9...
        # My geometry: Wheel at 5.5. Rod 7. Crosshead at ~12.5.
        # Does this overlap? Yes.
        # Let's draw the Cylinder FURTHER forward, or assume cylinder is "around" the piston.
        
        # Guide Bar (Slide)
        ax.plot([8, 14], [0.6, 0.6], color="#404040", linewidth=3, zorder=4)
        ax.plot([8, 14], [-0.6, -0.6], color="#404040", linewidth=3, zorder=4)
        
        # 5. Boiler & Cab
        # Boiler
        ax.add_patch(Rectangle((-2, 2.6), 14, 3.5, color=IRON_BLACK, zorder=4))
        # Brass Bands
        ax.add_patch(Rectangle((2, 2.6), 0.2, 3.5, color=BRASS, zorder=5))
        ax.add_patch(Rectangle((6, 2.6), 0.2, 3.5, color=BRASS, zorder=5))
        
        # Smokebox (Front)
        ax.add_patch(Rectangle((10, 2.6), 2.5, 3.5, color="#101010", zorder=5))
        
        # Funnel
        ax.add_patch(Rectangle((10.5, 6.1), 1.0, 1.5, color="#101010", zorder=4))
        # Funnel Flare
        ax.add_patch(Polygon([[10.3, 7.6], [11.7, 7.6], [11.5, 6.1], [10.5, 6.1]], color=BRASS, zorder=5))
        
        # Cab (Rear)
        ax.add_patch(Polygon([[-5, -1], [-2, -1], [-2, 8], [-5, 8], [-5.5, 5]], color=IRON_BLACK, zorder=3))
        # Cab Window
        ax.add_patch(Rectangle((-4.5, 5), 1.5, 1.5, color="#505050", zorder=4))

        # 6. Smoke Particles
        for p in self.smoke_particles:
            alpha = max(0, min(1.0, p['life']))
            ax.add_patch(Circle((p['x'], p['y']), p['size'], color=p['color'], alpha=alpha, zorder=1))

        # 7. HUD
        info = f"SPEED: {int(self.speed * 3)} MPH"
        ax.text(0, 8, info, color=BRASS, ha='center', fontfamily='monospace', fontsize=15,
                bbox=dict(facecolor='black', edgecolor=BRASS))

        ax.set_aspect('equal')
        ax.set_axis_off()
        
        out_dir = "logic_garden_steam_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"steam_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Building Steam Pressure...")
    
    sim = SteamLocoSim()
    
    for i in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(16, 9), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        sim.update(i)
        sim.render(i, ax)
        plt.close()
        
        if i % 30 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
