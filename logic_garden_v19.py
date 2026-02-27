"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v19.py
MODE:   Nursery (Bauhaus Palette)
TARGET: Thermodynamics (Naval Reactor / PWR)
STYLE:  "The Kettle" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Wedge
import os

# --- 1. THE NURSERY PALETTE ---
BG_COLOR = "#FFFFFF"        # Void
PIPE_COLOR = "#000000"      # Structure
CORE_COLOR = "#FF4500"      # Safety Red (Radioactive Heat)
WATER_COLOR = "#0080FF"     # Azure Blue (Liquid)
STEAM_COLOR = "#FFD700"     # Cyber Yellow (Gas/Energy)

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
NUM_PARTICLES = 40

# Paths defined as (x, y) functions of t (0->1)
# Primary Loop: Left side rounded rect
# Secondary Loop: Right side rounded rect

class ReactorSim:
    def __init__(self):
        self.particles_pri = np.linspace(0, 1, NUM_PARTICLES)
        self.particles_sec = np.linspace(0, 1, NUM_PARTICLES)
        self.turbine_angle = 0.0

    def get_pos_primary(self, t):
        # 0.0 -> 1.0 along the path
        # Simple box: (-4, -2) to (-1, 2)
        # Sequence: Bottom -> Right(Heat Exchanger) -> Top -> Left(Core)
        
        t = t % 1.0
        # Perimeter approx 12 units
        # Let's use simple logic
        if t < 0.25: # Bottom (-1 to -4)
            x = -1 - (t/0.25)*3
            y = -2
        elif t < 0.5: # Left (Up through Core)
            x = -4
            y = -2 + ((t-0.25)/0.25)*4
        elif t < 0.75: # Top (-4 to -1)
            x = -4 + ((t-0.5)/0.25)*3
            y = 2
        else: # Right (Down through Exchanger)
            x = -1
            y = 2 - ((t-0.75)/0.25)*4
        return x, y

    def get_pos_secondary(self, t):
        # Mirror image: (1, -2) to (4, 2)
        # Sequence: Bottom -> Left(Exchanger) -> Top -> Right(Turbine)
        
        t = t % 1.0
        if t < 0.25: # Bottom (4 to 1)
            x = 4 - (t/0.25)*3
            y = -2
        elif t < 0.5: # Left (Up through Exchanger - absorbing heat)
            x = 1
            y = -2 + ((t-0.25)/0.25)*4
        elif t < 0.75: # Top (1 to 4)
            x = 1 + ((t-0.5)/0.25)*3
            y = 2
        else: # Right (Down through Turbine)
            x = 4
            y = 2 - ((t-0.75)/0.25)*4
        return x, y

    def get_color_primary(self, t):
        # Logic: 
        # Left Leg (0.25-0.5) is CORE -> Heating Up
        # Top/Right Leg is HOT (Red)
        # Right Leg (0.75-1.0) is EXCHANGER -> Cooling Down
        # Bottom is COLD (Blue)
        
        # Simple Phase mapping
        if t < 0.25: return WATER_COLOR # Cold return
        if 0.25 <= t < 0.5: return CORE_COLOR # Heating in core
        if 0.5 <= t < 0.75: return CORE_COLOR # Hot loop
        return WATER_COLOR # Cooling in exchanger
        
        # We can interpolate for smooth gradient, but Blocky is Bauhaus.

    def get_color_secondary(self, t):
        # Left Leg (0.25-0.5) is EXCHANGER -> Heating Up (Turns to Steam)
        # Top/Right is STEAM (Yellow)
        # Right Leg is TURBINE -> Losing Energy
        # Bottom is CONDENSED (Blue)
        
        if t < 0.25: return WATER_COLOR
        if 0.25 <= t < 0.5: return STEAM_COLOR # Boiling!
        if 0.5 <= t < 0.75: return STEAM_COLOR # Steam pipe
        return WATER_COLOR # Condenser

    def render(self, frame_idx, ax):
        # 1. Draw Structure (Pipes)
        # Core Box
        core = Rectangle((-4.5, -1), 1, 2, facecolor="#333333", zorder=0) # Graphite/Fuel
        ax.add_patch(core)
        ax.text(-4.0, 0, "CORE", color="white", ha="center", va="center", fontweight="bold", rotation=90)
        
        # Heat Exchanger (The Middle)
        hx = Rectangle((-1.5, -2.5), 3, 5, facecolor="#EEEEEE", edgecolor="black", zorder=0)
        ax.add_patch(hx)
        
        # Turbine (The Right)
        turb_x, turb_y = 4, 0
        
        # 2. Update & Draw Particles (Primary)
        speed = 0.005
        self.particles_pri = (self.particles_pri + speed) % 1.0
        
        for p in self.particles_pri:
            x, y = self.get_pos_primary(p)
            c = self.get_color_primary(p)
            ax.add_patch(Circle((x, y), 0.15, color=c, zorder=5))

        # 3. Update & Draw Particles (Secondary)
        self.particles_sec = (self.particles_sec + speed) % 1.0
        
        for p in self.particles_sec:
            x, y = self.get_pos_secondary(p)
            c = self.get_color_secondary(p)
            ax.add_patch(Circle((x, y), 0.15, color=c, zorder=5))
            
        # 4. Animate Turbine
        self.turbine_angle -= 15 # Spin!
        # Draw Propeller blades
        r = 0.8
        for i in range(3):
            theta = np.radians(self.turbine_angle + i*120)
            dx = r * np.cos(theta)
            dy = r * np.sin(theta)
            ax.plot([turb_x, turb_x+dx], [turb_y, turb_y+dy], color="black", linewidth=5, zorder=10)
        
        ax.add_patch(Circle((turb_x, turb_y), 0.2, color="black", zorder=11))

        # 5. Connectors (Pipe outlines)
        # Just drawn logically by particle flow
        
        # Scale
        ax.set_xlim(-6, 6)
        ax.set_ylim(-3.5, 3.5)
        ax.set_aspect('equal')
        
        # Save
        out_dir = "logic_garden_kettle_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"kettle_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Boiling the Ocean...")
    
    sim = ReactorSim()
    
    for i in range(TOTAL_FRAMES):
        # 1. Canvas
        fig = plt.figure(figsize=(16, 9), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        sim.render(i, ax)
        
        if i % 30 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
