"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v21_hotfix.py
MODE:   Nursery (Bauhaus Palette)
TARGET: Ballistics (V2 Rocket / Parabola)
STYLE:  "The Great Curve" (Recursion Fixed) | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
import os

# --- 1. THE NURSERY PALETTE ---
BG_COLOR = "#FFFFFF"        # Void
GROUND_COLOR = "#000000"    # Earth
ROCKET_BODY = "#FFFFFF"     # White
ROCKET_FINS = "#000000"     # Black Checkers
FLAME_COLOR = "#FFD700"     # Yellow Flame
PATH_COLOR = "#FF4500"      # Red Path
GHOST_COLOR = "#0080FF"     # Blue Inertia

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 14 
TOTAL_FRAMES = FPS * DURATION

class RocketSim:
    def __init__(self, run_scout=True):
        # Physics Constants 
        self.gravity = 0.025
        self.thrust = 0.08       
        self.fuel_frames = 50    
        self.start_angle = 82    
        
        self.history_x = []
        self.history_y = []
        self.ghost_line = []
        self.crashed = False
        self.scouting = not run_scout # If we aren't running a scout, WE act as one (or simple mode)
        
        # Initialize State
        self.reset()
        
        # AUTO-SCALE CAMERA
        if run_scout:
            print("[SCOUT] Calculating Ballistic Trajectory...")
            self.max_x = 0
            self.max_y = 0
            
            # RECURSION FIX: Set run_scout=False for the temporary sim
            temp_sim = RocketSim(run_scout=False) 
            
            # Dry Run
            for _ in range(2000): 
                temp_sim.update(_)
                if temp_sim.y > self.max_y: self.max_y = temp_sim.y
                if temp_sim.x > self.max_x: self.max_x = temp_sim.x
                if temp_sim.crashed: break
                
            # Set Camera Limits
            self.cam_xlim = (-self.max_x * 0.1, self.max_x * 1.2) 
            self.cam_ylim = (-self.max_y * 0.1, self.max_y * 1.3)
            
            print(f"[SCOUT] Apogee: {self.max_y:.2f} | Range: {self.max_x:.2f}")
            print(f"[SCOUT] Camera Scaled Successfully.")
        else:
            # Default fallback limits (will be ignored by scout, but needed for init)
            self.cam_xlim = (-10, 100)
            self.cam_ylim = (-5, 100)

    def reset(self):
        self.x = 0.0
        self.y = 2.0 
        self.vx = 0.0
        self.vy = 0.0
        self.angle = np.radians(self.start_angle)

    def update(self, t):
        if self.crashed:
            return

        # 1. Physics Engine
        if t < self.fuel_frames:
            if t > 10: self.angle -= np.radians(0.5)
            
            ax = (self.thrust * np.cos(self.angle))
            ay = (self.thrust * np.sin(self.angle)) - self.gravity
            self.vx += ax
            self.vy += ay
            
        else:
            # Brennschluss
            if not self.ghost_line and not self.scouting:
                gx, gy = self.x, self.y
                gvx, gvy = self.vx, self.vy
                for _ in range(15): 
                     gx += gvx * 15 
                     gy += gvy * 15
                     self.ghost_line.append((gx, gy))
            
            self.vy -= self.gravity
            
            if self.vx != 0 or self.vy != 0:
                self.angle = np.arctan2(self.vy, self.vx)

        self.x += self.vx
        self.y += self.vy
        
        if self.y < 0:
            self.y = 0
            self.vx = 0
            self.vy = 0
            self.crashed = True
            if not self.scouting:
                print(f"Impact at Frame {t}")

        if not self.scouting:
            self.history_x.append(self.x)
            self.history_y.append(self.y)

    def render(self, frame_idx, ax):
        # 1. World
        ax.add_patch(Rectangle((-1000, -100), 3000, 100, facecolor=GROUND_COLOR))
        
        # 2. Trails
        if self.ghost_line:
            gx, gy = zip(*self.ghost_line)
            ax.plot(gx, gy, color=GHOST_COLOR, linestyle="--", linewidth=3, zorder=1)

        if len(self.history_x) > 1:
            ax.plot(self.history_x, self.history_y, color=PATH_COLOR, linewidth=5, zorder=2)

        # 3. Rocket
        # Scale rocket size to the camera
        s = (self.cam_ylim[1] - self.cam_ylim[0]) / 35.0 
        
        pts_body = np.array([[s*1.0, 0], [-s*1.0, s*0.25], [-s*1.0, -s*0.25]])
        pts_fin1 = np.array([[-s*1.0, s*0.25], [-s*1.5, s*0.6], [-s*1.0, 0]])
        pts_fin2 = np.array([[-s*1.0, -s*0.25], [-s*1.5, -s*0.6], [-s*1.0, 0]])
        pts_nose = np.array([[s*1.0, 0], [s*0.5, s*0.12], [s*0.5, -s*0.12]])

        c, s_sin = np.cos(self.angle), np.sin(self.angle)
        R = np.array([[c, -s_sin], [s_sin, c]])

        def trans(pts):
            return np.dot(pts, R.T) + [self.x, self.y]

        ax.add_patch(Polygon(trans(pts_body), facecolor=ROCKET_BODY, edgecolor="black", zorder=10))
        ax.add_patch(Polygon(trans(pts_fin1), facecolor=ROCKET_FINS, zorder=10))
        ax.add_patch(Polygon(trans(pts_fin2), facecolor=ROCKET_FINS, zorder=10))
        ax.add_patch(Polygon(trans(pts_nose), facecolor=ROCKET_FINS, zorder=11))

        # 4. Flame
        if frame_idx < self.fuel_frames and not self.crashed:
            f_len = s * (1.5 + np.random.rand())
            pts_flame = np.array([[-s*1.0, s*0.15], [-s*1.0 - f_len, 0], [-s*1.0, -s*0.15]])
            ax.add_patch(Polygon(trans(pts_flame), facecolor=FLAME_COLOR, alpha=0.9, zorder=5))

        ax.set_xlim(self.cam_xlim)
        ax.set_ylim(self.cam_ylim)
        ax.set_aspect('equal')
        
        out_dir = "logic_garden_v2_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"v2_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Launching the V2 (Recursion Fixed)...")
    
    sim = RocketSim(run_scout=True) # Explicitly allow ONE scout run
    
    for i in range(TOTAL_FRAMES):
        sim.update(i)
        
        fig = plt.figure(figsize=(16, 9), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        sim.render(i, ax)
        
        if i % 30 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
