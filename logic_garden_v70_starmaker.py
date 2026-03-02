"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v70_starmaker_fixed.py
MODE:   Retro (VIC-II Emulation)
TARGET: Thermonuclear Ignition (Teller-Ulam Configuration)
STYLE:  "The Star Maker" | 25s | C64 Palette | No Shield
STATUS: PATCHED (Removed Interstage Baffle)

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
    [0.00, 0.00, 0.00], # 0: Black (Void)
    [1.00, 1.00, 1.00], # 1: White (Fusion/X-Ray Peak)
    [0.53, 0.00, 0.00], # 2: Red (Fission Core)
    [0.45, 0.75, 0.79], # 3: Cyan (Plasma)
    [0.55, 0.17, 0.55], # 4: Purple
    [0.37, 0.65, 0.29], # 5: Green
    [0.21, 0.16, 0.47], # 6: Blue (Fusion Fuel - Cold)
    [0.93, 0.94, 0.46], # 7: Yellow (Radiation Flood)
    [0.55, 0.31, 0.08], # 8: Orange (Fission Burn)
    [0.28, 0.20, 0.00], # 9: Brown
    [0.75, 0.42, 0.43], # 10: Light Red
    [0.33, 0.33, 0.33], # 11: Dark Grey (Case)
    [0.47, 0.47, 0.47], # 12: Grey
    [0.63, 0.95, 0.61], # 13: Light Green
    [0.42, 0.37, 0.71], # 14: Light Blue (Ablating Shell)
    [0.70, 0.70, 0.70]  # 15: Light Grey
])

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 25
TOTAL_FRAMES = FPS * DURATION
W, H = 320, 200

# Geometry
CX = W // 2
TOP_Y = 50   # Primary Position
BOT_Y = 140  # Secondary Position
CASE_W = 100 # Hohlraum width

def draw_circle(buffer, cx, cy, r, color_idx):
    # Simple raster circle
    y_min, y_max = max(0, int(cy - r)), min(H, int(cy + r + 1))
    x_min, x_max = max(0, int(cx - r)), min(W, int(cx + r + 1))
    
    for y in range(y_min, y_max):
        for x in range(x_min, x_max):
            if (x - cx)**2 + (y - cy)**2 <= r**2:
                buffer[y, x] = C64[color_idx]

def draw_noise_fill(buffer, x1, y1, x2, y2, density, color_idx):
    # Fills region with random pixels based on density
    x1, x2 = max(0, int(x1)), min(W, int(x2))
    y1, y2 = max(0, int(y1)), min(H, int(y2))
    
    h_slice = y2 - y1
    w_slice = x2 - x1
    if h_slice <= 0 or w_slice <= 0: return
    
    mask = np.random.random((h_slice, w_slice)) < density
    
    target_color = C64[color_idx]
    current_slice = buffer[y1:y2, x1:x2]
    current_slice[mask] = target_color

def generate_starmaker():
    out_dir = "logic_garden_starmaker_frames"
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"[PHYSICS] Initializing Radiation Hydrodynamics...")
    
    rad_temp = 0.0 # Temperature of Hohlraum (0.0 to 1.0)
    sec_rad = 30.0 # Radius of Secondary
    prim_rad = 15.0 # Radius of Primary
    
    ignited = False
    
    for f in range(TOTAL_FRAMES):
        t = f
        
        # 1. INIT BUFFER (Black Void)
        buffer = np.zeros((H, W, 3))
        
        # 2. DRAW HOHLRAUM (The Case)
        hw = CASE_W
        border = 10
        # Walls
        buffer[20:180, CX-hw-border:CX-hw] = C64[11]
        buffer[20:180, CX+hw:CX+hw+border] = C64[11]
        buffer[20:30, CX-hw-border:CX+hw+border] = C64[11]
        buffer[170:180, CX-hw-border:CX+hw+border] = C64[11]
        
        # 3. COMPUTE PHYSICS STATE
        
        # PRIMARY DYNAMICS
        prim_col = 2 # Red
        if t > 30:
            if t < 60:
                # Explosion phase
                prim_rad += 0.5
                prim_col = 8 if (f // 2) % 2 == 0 else 2 # Flash Orange/Red
                rad_temp = (t - 30) / 30.0 # Heat up
            else:
                # Post-explosion
                prim_rad += 0.1
                prim_col = 11 # Burnt out
                rad_temp = 1.0 # Max Temp
        
        # RADIATION DYNAMICS
        if rad_temp > 0.1:
            # Fill the Hohlraum with Yellow/White noise
            dens = rad_temp * 0.8
            r_col = 7 if rad_temp < 0.8 else 1 
            draw_noise_fill(buffer, CX-hw, 30, CX+hw, 170, dens, r_col)
        
        # SECONDARY DYNAMICS
        sec_col = 6 # Dark Blue
        
        if t > 60 and not ignited:
            # Implosion Phase
            compression = (t - 60) / 60.0 # 0 to 1
            if compression > 1.0: compression = 1.0
            
            # Radius shrinks
            sec_rad = 30.0 * (1.0 - compression * 0.7) # Shrink to 30%
            
            # Surface heats up (Ablation layer)
            draw_circle(buffer, CX, BOT_Y, sec_rad + 4, 14) # Light Blue/Cyan Plasma
            sec_col = 6
        
        if t > 125:
            # Ignition!
            ignited = True
            
            # Expansion
            burn_time = t - 125
            sec_rad = 9.0 + burn_time * 4.0 # Rapid expansion
            sec_col = 1 # White Hot
        
        # 4. RENDER OBJECTS
        
        # Draw Secondary
        draw_circle(buffer, CX, BOT_Y, sec_rad, sec_col)
        
        # (REMOVED: Grey Shield / Interstage Baffle)
        
        # Draw Primary
        if t < 60 or (t > 60 and t < 100):
             draw_circle(buffer, CX, TOP_Y, prim_rad, prim_col)

        # 5. OVERLAYS
        # Scanlines
        buffer[1::2] *= 0.75
        
        fig = plt.figure(figsize=(10, 10), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        fig.add_axes(ax)
        ax.set_axis_off()
        ax.imshow(buffer, interpolation='nearest', aspect='auto')
        
        # Text Overlay
        
        # Top: Primary Status
        p_status = "CRITICAL" if t > 30 else "STABLE"
        if t > 60: p_status = "SPENT"
        ax.text(20, 20, f"PRIMARY: {p_status}", color="#ff5555", fontfamily='monospace', fontweight='bold', fontsize=12)
        
        # Middle: Physics
        if t > 50 and t < 130:
            ax.text(W/2, H/2 - 10, "P-GAMMA = 1/3 a T^4", color="#ffff55", ha='center', fontfamily='monospace', fontweight='bold', fontsize=15)
            temp_val = int(rad_temp * 300)
            ax.text(W/2, H/2 + 10, f"TEMP: {temp_val} MK", color="#ffffff", ha='center', fontfamily='monospace', fontweight='bold', fontsize=12)

        # Bottom: Secondary Status
        s_status = "FUEL COLD"
        s_col = "#5555ff"
        if t > 60: s_status = "IMPLODING"; s_col = "#55ffff"
        if t > 125: s_status = "IGNITION"; s_col = "#ffffff"
        
        ax.text(20, 180, f"SECONDARY: {s_status}", color=s_col, fontfamily='monospace', fontweight='bold', fontsize=12)
        ax.text(W/2, 10, "LOGIC GARDEN 20: THE STAR MAKER", color="#aaaaaa", ha='center', fontfamily='monospace', fontweight='bold', fontsize=15)

        filename = os.path.join(out_dir, f"starmaker_{f:04d}.png")
        plt.savefig(filename, facecolor='black')
        plt.close()
        
        if f % 60 == 0:
            print(f"Frame {f}/{TOTAL_FRAMES}")

if __name__ == "__main__":
    generate_starmaker()
