"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v29_tranquility_fixed.py
MODE:   Nursery (Lunar Palette)
TARGET: Apollo Descent (Alpha Clamp Fix)
STYLE:  "Tranquility Base" (FIXED) | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
import os

# --- 1. THE LUNAR PALETTE ---
BG_COLOR = "#000000"
MOON_COLOR = "#282828"      # Deep Dark Grey
GOLD_FOIL = "#FFD700"       # Iconic Gold
CABIN_GREY = "#C0C0C0"
FLAME_CORE = "#FFFFFF"
FLAME_OUTER = "#87CEFA"
DUST_COLOR = "#E0E0E0"

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 25
TOTAL_FRAMES = FPS * DURATION

class LanderSim:
    def __init__(self):
        # Physics State
        self.x = -40.0       
        self.y = 110.0       
        self.vx = 0.4        
        self.vy = -0.3
        
        # Constants
        self.gravity = 0.008 
        self.max_thrust = 0.024 
        
        # Actuators
        self.thrust_angle = 90.0
        self.throttle = 0.0
        
        # Terrain
        np.random.seed(600) 
        self.terrain_x = np.linspace(-200, 200, 600)
        self.terrain_y = np.zeros_like(self.terrain_x)
        
        # Generate Terrain
        for i in range(15):
            cx = np.random.uniform(-150, 150)
            if cx > -20 and cx < 40: continue # Landing zone
            cw = np.random.uniform(5, 20)
            cd = np.random.uniform(1, 4)
            mask = np.abs(self.terrain_x - cx) < cw
            self.terrain_y[mask] -= cd * np.cos((self.terrain_x[mask] - cx) / cw * (np.pi/2))
            
        self.dust_particles = [] 
        self.touchdown = False
        self.settling_phase = 0
        self.prev_error_vy = 0.0

    def update(self, frame_idx):
        # --- 0. ENVIRONMENT SENSORS (Always Run) ---
        idx = int(np.interp(self.x, self.terrain_x, np.arange(len(self.terrain_x))))
        idx = max(0, min(len(self.terrain_y)-1, idx))
        ground_y = self.terrain_y[idx]
        radar_alt = self.y - ground_y - 3.8

        # --- 1. PARTICLE PHYSICS (Always Run) ---
        # "The Dust must fall even if the Engine stops"
        for p in self.dust_particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] -= self.gravity * 2.5 # Dust falls fast in vacuum
            p['life'] -= 0.02
        self.dust_particles = [p for p in self.dust_particles if p['life'] > 0]

        # --- 2. FLIGHT PHYSICS ---
        if self.touchdown:
            # Settling Suspension Logic
            if self.settling_phase < 30:
                self.settling_phase += 1
                self.vx *= 0.8 # Friction
                self.x += self.vx
                # Righting moment
                self.thrust_angle += (90.0 - self.thrust_angle) * 0.15
                # Suspension settle (Damped Spring)
                rest_y = ground_y + 3.6
                self.y += (rest_y - self.y) * 0.1
                self.throttle = 0.0
            return

        # --- 3. GUIDANCE COMPUTER ---
        
        # A. Horizontal Control
        if radar_alt < 15: 
            h_gain = 35.0 
        else:
            h_gain = 15.0
            
        target_tilt = 90.0 + (self.vx * h_gain)
        target_tilt = max(65, min(115, target_tilt))
        
        # B. Vertical Control
        target_vy = -0.15 - (radar_alt * 0.015)
        error = target_vy - self.vy
        
        # Feedforward
        rad = np.radians(self.thrust_angle)
        sin_a = max(0.5, np.sin(rad))
        ff_throttle = self.gravity / (self.max_thrust * sin_a)
        
        kp = 3.5
        kd = 35.0
        
        deriv = error - self.prev_error_vy
        pid_out = (kp * error) + (kd * deriv)
        
        cmd_throttle = ff_throttle + pid_out
        self.prev_error_vy = error
        
        # Probes contact
        if radar_alt < 0.2:
             cmd_throttle = 0.0
        else:
             cmd_throttle = max(0.1, min(1.0, cmd_throttle))

        # --- 4. ACTUATORS ---
        self.throttle += (cmd_throttle - self.throttle) * 0.15
        self.thrust_angle += (target_tilt - self.thrust_angle) * 0.08
        
        # --- 5. INTEGRATION ---
        rad = np.radians(self.thrust_angle)
        fx = np.cos(rad) * self.max_thrust * self.throttle
        fy = np.sin(rad) * self.max_thrust * self.throttle
        
        self.vx += fx
        self.vy += (fy - self.gravity)
        self.x += self.vx
        self.y += self.vy
        
        # Touchdown Check
        if radar_alt <= 0:
            self.y = ground_y + 3.8
            self.touchdown = True
            self.throttle = 0.0
            print("CONTACT LIGHT. ENGINE STOP.")

        # --- 6. DUST GENERATION (Only if Engine Active) ---
        if radar_alt < 30 and self.throttle > 0.1:
            # Generate new dust
            count = int(self.throttle * 5)
            for _ in range(count):
                dx = self.x + np.random.normal(0, 1.2)
                dy = ground_y + 0.2
                direction = np.sign(dx - self.x)
                if direction == 0: direction = 1
                
                blast = self.throttle * 2.5
                dvx = direction * (0.5 + np.random.rand()*blast)
                dvy = np.random.rand() * blast * 0.4
                
                # Life initialized > 1.0 to persist longer
                self.dust_particles.append({'x':dx, 'y':dy, 'vx':dvx, 'vy':dvy, 'life':1.0 + np.random.rand()})


    def render(self, frame_idx, ax):
        # Camera
        cam_x = self.x
        cam_y = max(30, self.y)
        ax.set_xlim(cam_x - 40, cam_x + 30)
        ax.set_ylim(cam_y - 40, cam_y + 30)
        
        # Terrain
        ax.fill_between(self.terrain_x, self.terrain_y, -100, facecolor=MOON_COLOR)
        ax.plot(self.terrain_x, self.terrain_y, color="#666666", linewidth=1.5)
        
        # Dust (FIXED: Clamp Alpha)
        for p in self.dust_particles:
            safe_alpha = max(0.0, min(1.0, p['life'])) # Clamp 0-1
            safe_size = max(0.1, 0.2 * p['life']) # Prevent negative size
            ax.add_patch(Circle((p['x'], p['y']), safe_size, color=DUST_COLOR, alpha=safe_alpha))

        # --- TRANSFORM ---
        rot_deg = self.thrust_angle - 90
        rad = np.radians(rot_deg)
        c, s = np.cos(rad), np.sin(rad)
        
        def t(pts):
            res = []
            for px, py in pts:
                rx = px*c - py*s
                ry = px*s + py*c
                res.append([rx + self.x, ry + self.y])
            return res
            
        w, h = 4.0, 3.0
        
        # Assets
        legs = []
        pads = []
        span = 5.0
        for ang in [40, 140, 220, 320]:
            lr = np.radians(ang)
            lx = np.cos(lr) * span
            ly = np.sin(lr) * span * 0.5 - 1.5
            legs.append([ [0, -1], [lx, ly] ])
            pads.append([lx, ly])
            
        # Draw Back Legs
        for i in [0, 1]:
            l = t(legs[i])
            ax.plot([l[0][0], l[1][0]], [l[0][1], l[1][1]], color="#C5A000", linewidth=2)
            
        # Flame Logic (Clipped)
        if self.throttle > 0.01 and not self.touchdown:
            flame_len = 8.0 * self.throttle + np.random.normal(0,0.5)
            tip_local = [0, -h/2 - flame_len]
            tip_world = t([tip_local])[0]
            
            # Ground Check
            idx_f = int(np.interp(tip_world[0], self.terrain_x, np.arange(len(self.terrain_x))))
            gy_f = self.terrain_y[max(0, min(len(self.terrain_y)-1, idx_f))]
            
            if tip_world[1] < gy_f: tip_world[1] = gy_f
            
            # Reconstruct
            base_l = t([ [-1.2, -h/2] ])[0]
            base_r = t([ [1.2, -h/2] ])[0]
            ax.add_patch(Polygon([base_l, base_r, tip_world], facecolor=FLAME_CORE, alpha=0.9, zorder=4))
            
            # Outer
            glow_tip = [tip_world[0], tip_world[1] + 1.0]
            base_l_g = t([ [-1.8, -h/2] ])[0]
            base_r_g = t([ [1.8, -h/2] ])[0]
            ax.add_patch(Polygon([base_l_g, base_r_g, glow_tip], facecolor=FLAME_OUTER, alpha=0.3, zorder=3))

        # Body
        body_geom = t([ [-w/2,-h/2], [w/2,-h/2], [w/2,h/2], [-w/2,h/2] ])
        ax.add_patch(Polygon(body_geom, facecolor=GOLD_FOIL, edgecolor="black", zorder=5))
        
        # Front Legs
        for i in [2, 3]:
            l = t(legs[i])
            ax.plot([l[0][0], l[1][0]], [l[0][1], l[1][1]], color="#FFD700", linewidth=3)
        for p in pads:
            pp = t([p])[0]
            ax.add_patch(Circle((pp[0], pp[1]), 0.5, color="#101010", zorder=6))

        # Ascent
        asc = t([ [-2.2, h/2], [2.2, h/2], [1.8, h/2+2.2], [-1.8, h/2+2.2] ])
        ax.add_patch(Polygon(asc, facecolor=CABIN_GREY, edgecolor="black", zorder=7))
        
        # HUD
        idx_g = int(np.interp(self.x, self.terrain_x, np.arange(len(self.terrain_x))))
        gy = self.terrain_y[max(0, min(len(self.terrain_y)-1, idx_g))]
        alt = max(0, self.y - gy - 3.8)
        
        info = f"ALT : {alt:5.2f} M\nVY  : {self.vy:5.2f} M/S\nVX  : {self.vx:5.2f} M/S\nFUEL: {int(self.throttle*100):3d} %"
        if self.touchdown: 
            info = "CONTACT LIGHT\nENGINE STOP"
            
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        
        ax.text(xlim[0] + 5, ylim[1] - 15, info, color="#00FF00", fontfamily='monospace', fontsize=14,
                bbox=dict(facecolor='black', alpha=0.6, edgecolor='green'))

        ax.set_aspect('equal')
        ax.set_axis_off()
        
        out_dir = "logic_garden_apollo_final_fixed_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"tranquility_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Tranquility Base (Fixed Alpha). Running...")
    
    sim = LanderSim()
    
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
