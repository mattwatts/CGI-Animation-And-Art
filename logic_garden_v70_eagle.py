"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v70_eagle_1202_fixed.py
MODE:   Retro (VIC-II Emulation)
TARGET: Apollo Descent Trajectory (P64/P66)
STYLE:  "The Eagle" | 25s | 1202 Alarm Handling
STATUS: PATCHED (PID Gain Reduced + Climb Veto)

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import random

# --- 1. THE VIC-II PALETTE ---
C64 = np.array([
    [0.00, 0.00, 0.00], # 0: Black
    [1.00, 1.00, 1.00], # 1: White
    [0.53, 0.00, 0.00], # 2: Red
    [0.45, 0.75, 0.79], # 3: Cyan
    [0.55, 0.17, 0.55], # 4: Purple (Alarm)
    [0.37, 0.65, 0.29], # 5: Green
    [0.21, 0.16, 0.47], # 6: Blue
    [0.93, 0.94, 0.46], # 7: Yellow (Gold shadow)
    [0.55, 0.31, 0.08], # 8: Orange
    [0.28, 0.20, 0.00], # 9: Brown
    [0.75, 0.42, 0.43], # 10: Light Red
    [0.33, 0.33, 0.33], # 11: Dark Grey
    [0.47, 0.47, 0.47], # 12: Grey (Regolith)
    [0.63, 0.95, 0.61], # 13: Light Green
    [0.42, 0.37, 0.71], # 14: Light Blue
    [0.70, 0.70, 0.70]  # 15: Light Grey
])

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 25
TOTAL_FRAMES = FPS * DURATION
W, H = 320, 200

# --- 3. PHYSICS & UTILS ---
def rotate_point(x, y, angle_rad):
    rx = x * np.cos(angle_rad) - y * np.sin(angle_rad)
    ry = x * np.sin(angle_rad) + y * np.cos(angle_rad)
    return rx, ry

def generate_terrain(width):
    y = np.zeros(width)
    y[:] = 30 # Base height slightly higher to keep in frame
    for i in range(width):
        y[i] += random.uniform(-1, 1)
    
    # Landing Site (Flat) - Target X 240
    site_x = 240
    y[site_x-40:site_x+40] = 30
    
    # Crater (Dip)
    center = 100
    radius = 50
    for i in range(width):
        if abs(i - center) < radius:
            depth = np.sqrt(radius**2 - (i-center)**2) * 0.4
            y[i] -= depth
    
    y = np.clip(y, 5, 100)
    return y.astype(int)

def generate_eagle():
    out_dir = "logic_garden_eagle_frames"
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"[AGC] 1202 ALARM CLEARED. PRIORITY: LANDING...")
    
    terrain = generate_terrain(W)
    stars = [(random.randint(0, W-1), random.randint(40, H-1)) for _ in range(80)]
    
    # FLIGHT STATE
    pos_x = 10.0
    pos_y = 160.0 # High Gate
    
    vel_x = 2.2 
    vel_y = -0.4 
    
    pitch = 110.0 
    
    fuel = 100.0
    target_x = 240.0
    
    # PHYSICS CONSTANTS
    GRAVITY = 0.05
    THRUST_POWER = 0.11
    # Hover Throttle needed = GRAVITY / THRUST_POWER = 0.4545...
    HOVER_THROTTLE = GRAVITY / THRUST_POWER
    
    for f in range(TOTAL_FRAMES):
        # 1. FLIGHT COMPUTER
        
        throttle = 0.0
        desired_pitch = 90.0
        dist_to_go = target_x - pos_x
        
        # P64 APPROACH (Frames 0-200)
        if f < 200:
            # Horizontal Logic: Slow down as we get closer
            target_vx = dist_to_go * 0.012
            err_vx = target_vx - vel_x
            
            # Use Pitch to control Horizontal Velocity
            # Lean back (>90) to slow down
            desired_pitch = 90.0 - (err_vx * 25.0)
            desired_pitch = np.clip(desired_pitch, 80, 120)
            
            # Vertical Logic: Maintain constant descent
            target_vy = -0.5
            err_vy = target_vy - vel_y
            # PD Loop
            throttle = HOVER_THROTTLE + (err_vy * 0.8) # Moderate gain
            
        # P66 TERMINAL / HOVER (Frames 200+)
        else:
            # Stick the landing
            # X Logic: Fine adjustments
            if dist_to_go > 5.0: desired_pitch = 85.0
            elif dist_to_go < -5.0: desired_pitch = 95.0
            else: 
                desired_pitch = 90.0
                vel_x *= 0.96 # Kill lateral drift
                
            # Y Logic: Soft Descent
            ground_h = terrain[int(np.clip(pos_x, 0, W-1))]
            alt = pos_y - ground_h
            
            target_vy = -0.3 # Descent
            if alt < 50: target_vy = -0.2
            if alt < 20: target_vy = -0.1
            
            err_vy = target_vy - vel_y
            # PID: Base Hover + Correction
            throttle = HOVER_THROTTLE + (err_vy * 0.5) # Gentle gain
            
        # 2. SAFETY INTERLOCKS (The Patch)
        # Verify Throttle
        throttle = np.clip(throttle, 0.0, 1.0)
        
        # CLIMB VETO: If we are climbing (vel_y > 0), cut throttle to force descent
        # This prevents the "float away" bug
        if vel_y > 0.0:
            throttle *= 0.1
            
        # 3. PHYSICS INTEGRATION
        pitch += (desired_pitch - pitch) * 0.1
        pitch_rad = np.radians(pitch)
        
        fx = np.cos(pitch_rad) * throttle * THRUST_POWER
        fy = np.sin(pitch_rad) * throttle * THRUST_POWER
        
        if pos_y > 30 and fuel > 0:
            vel_x += fx
            vel_y += fy
            fuel -= throttle * 0.1
            
        vel_y -= GRAVITY
        
        pos_x += vel_x
        pos_y += vel_y
        
        # Collision
        clamped_x = int(np.clip(pos_x, 0, W-1))
        gh = terrain[clamped_x]
        
        if pos_y < gh + 14: # Landing Legs
            pos_y = gh + 14
            vel_y = 0; vel_x = 0
            pitch = 90.0
            pass    

        # 4. RENDER BUFFER
        buffer = np.zeros((H, W, 3))
        
        # Stars
        for sx, sy in stars:
            if sy > terrain[sx]: buffer[sy, sx] = C64[11]
            
        # Terrain
        for x in range(W):
            th = int(terrain[x])
            if th > 0:
                buffer[0:th, x] = C64[12]
                buffer[th, x] = C64[15]
        
        # Lander
        cx, cy = int(pos_x), int(pos_y)
        rotation = np.radians(pitch - 90) 
        
        def plot_rot(lx, ly, c):
            bx = lx * np.cos(rotation) - ly * np.sin(rotation)
            by = lx * np.sin(rotation) + ly * np.cos(rotation)
            px, py = int(cx + bx), int(cy + by)
            if 0 <= px < W and 0 <= py < H: buffer[py, px] = c

        # Flame
        if throttle > 0.1 and pos_y > gh + 16:
            flame_len = int(throttle * 22 + random.randint(0, 4))
            for i in range(6, 6+flame_len):
                spread = (i-6) * 0.25
                for w in np.linspace(-spread, spread, 3):
                    plot_rot(w, -i, C64[1] if i < 12 else C64[3])

        # Legs
        leg_span = 12
        foot_y = -12
        for s in [-1, 1]:
            lx = s * leg_span
            plot_rot(lx, foot_y, C64[7]) 
            for k in range(10):
                t = k/10.0
                cur_x = (s*6)*(1-t) + lx*t
                cur_y = (-6)*(1-t) + foot_y*t
                plot_rot(cur_x, cur_y, C64[7])
        
        # Body
        for by in range(-6, 7):
            for bx in range(-6, 7):
                if max(abs(bx), abs(by)) < 6: # Box look
                    plot_rot(bx, by, C64[7])
        
        # Window (Black)
        plot_rot(3, 2, C64[0]); plot_rot(4, 2, C64[0]); plot_rot(3, 3, C64[0])

        # 5. OVERLAY
        fig = plt.figure(figsize=(10, 10), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        fig.add_axes(ax)
        ax.set_axis_off()
        ax.imshow(buffer, interpolation='nearest', aspect='auto', origin='lower')
        
        mode = "P64 APPROACH"
        if f > 200: mode = "P66 TERMINAL"
        if pos_y <= gh+15: mode = "TOUCHDOWN"
        
        ax.text(10, H-15, f"{mode}", color="#55ff55", fontfamily='monospace', fontweight='bold', fontsize=12)
        
        alt_ft = max(0, (pos_y - (gh+14)) * 5)
        ax.text(10, H-30, f"ALT: {int(alt_ft):03d} FT", color="white", fontfamily='monospace', fontweight='bold', fontsize=12)
        
        # 1202 ALARM (Frames 120-160)
        # Visual only, logic fixed
        if f > 120 and f < 160:
            if (f // 5) % 2 == 0: # Blink
                ax.text(W/2, H-50, "1202 ALARM", color="purple", ha='center', fontfamily='monospace', fontweight='bold', fontsize=20)
                ax.text(W/2, H-70, "EXECUTIVE OVERFLOW", color="purple", ha='center', fontfamily='monospace', fontweight='bold', fontsize=10)

        filename = os.path.join(out_dir, f"eagle_{f:04d}.png")
        plt.savefig(filename, facecolor='black')
        plt.close()
        
        if f % 60 == 0:
            print(f"Frame {f}/{TOTAL_FRAMES} | Alt: {alt_ft:.0f}")

if __name__ == "__main__":
    generate_eagle()
