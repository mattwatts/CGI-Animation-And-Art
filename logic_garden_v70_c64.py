"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v70_c64.py
MODE:   Retro (VIC-II Emulation)
TARGET: 8-Bit Bootstrap (Raster Bars)
STYLE:  "The Bootstrap" | 20s | C64 Palette | 4K Ready (Pixelated)

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# --- 1. THE VIC-II PALETTE (RGB) ---
C64_COLORS = {
    0:  [0.00, 0.00, 0.00], # Black
    1:  [1.00, 1.00, 1.00], # White
    2:  [0.53, 0.00, 0.00], # Red
    3:  [0.45, 0.75, 0.79], # Cyan
    4:  [0.55, 0.17, 0.55], # Purple
    5:  [0.37, 0.65, 0.29], # Green
    6:  [0.21, 0.16, 0.47], # Blue (Border)
    7:  [0.93, 0.94, 0.46], # Yellow
    8:  [0.55, 0.31, 0.08], # Orange
    9:  [0.28, 0.20, 0.00], # Brown
    10: [0.75, 0.42, 0.43], # Light Red
    11: [0.33, 0.33, 0.33], # Dark Grey
    12: [0.47, 0.47, 0.47], # Grey
    13: [0.63, 0.95, 0.61], # Light Green
    14: [0.42, 0.37, 0.71], # Light Blue (Screen)
    15: [0.70, 0.70, 0.70]  # Light Grey
}

# Raster Bar Sequence (Cyclic)
RASTER_SEQ = [0, 9, 2, 8, 7, 1, 7, 8, 2, 9, 0] # Black->Brown->Red->Orange->Yellow->White...

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
W, H = 320, 200 # Native C64 Resolution

def generate_c64_frames():
    out_dir = "logic_garden_c64_frames"
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"[VIC-II] Initializing 64K RAM System...")
    
    # Text Buffer sim
    # We will just overlay text with matplotlib using a monospace font
    
    for i in range(TOTAL_FRAMES):
        t = i / float(FPS)
        
        # 1. INIT SCREEN BUFFER (Light Blue Screen, Blue Border)
        # Create full buffer including border
        # Border is roughly 10% of screen space
        buffer = np.zeros((H, W, 3))
        
        # Fill Main Screen Color (Color 14)
        bg = C64_COLORS[6] # Border Color base
        buffer[:, :] = bg
        
        # Inner Screen Area (where text goes)
        margin_x = 40
        margin_y = 25
        screen_color = C64_COLORS[6] # Default Blue Background for "Intense" feel
        buffer[margin_y:H-margin_y, margin_x:W-margin_x] = screen_color
        
        # 2. RASTER BARS (The Demo Effect)
        # Calculate Y positions with Sine waves
        # Bar 1
        y1 = int(100 + 70 * np.sin(t * 2.5))
        # Bar 2 (Out of phase)
        y2 = int(100 + 70 * np.sin(t * 3.0 + 2.0))
        # Bar 3 (Fast)
        y3 = int(100 + 20 * np.sin(t * 8.0))
        
        draw_raster_bar(buffer, y1, RASTER_SEQ)
        draw_raster_bar(buffer, y2, RASTER_SEQ)
        # Intertwining sine wave
        draw_raster_bar(buffer, y3, [6, 14, 3, 1, 3, 14, 6])

        # 3. SCANLINE FILTER (CRT Emulation)
        # Darken every 2nd line by 20%
        buffer[1::2] *= 0.8
        
        # 4. RENDER
        fig = plt.figure(figsize=(10, 10), dpi=100) # Output is square 1000x1000
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        fig.add_axes(ax)
        ax.set_axis_off()
        
        # Display with NEAREST interpolation to keep it blocky
        ax.imshow(buffer, interpolation='nearest', aspect='auto')
        
        # 5. TEXT LAYER (PETSCII Simulation)
        # C64 Font is Monospace, Uppercase usually
        base_y = 0.2
        col_txt = "white"
        
        # Header
        ax.text(0.5, 0.90, "**** COMMODORE 64 BASIC V2 ****", color=col_txt, ha='center', 
                fontfamily='monospace', fontweight='bold', fontsize=15)
        ax.text(0.5, 0.86, "64K RAM SYSTEM  38911 BASIC BYTES FREE", color=col_txt, ha='center', 
                fontfamily='monospace', fontweight='bold', fontsize=15)
        
        # Interaction Simulation
        if i > 20:
             ax.text(0.12, 0.78, "READY.", color=col_txt, ha='left', fontfamily='monospace', fontweight='bold', fontsize=15)
        if i > 50:
             blink = "_" if (i // 15) % 2 == 0 else " "
             ax.text(0.12, 0.74, "LOAD \"LOGIC GARDEN\",8,1" + blink, color=col_txt, ha='left', fontfamily='monospace', fontweight='bold', fontsize=15)
        
        if i > 120:
             ax.text(0.12, 0.68, "SEARCHING FOR LOGIC GARDEN", color=col_txt, ha='left', fontfamily='monospace', fontweight='bold', fontsize=15)
             
        if i > 150:
             ax.text(0.12, 0.64, "LOADING", color=col_txt, ha='left', fontfamily='monospace', fontweight='bold', fontsize=15)
             
        if i > 180:
             ax.text(0.12, 0.60, "READY.", color=col_txt, ha='left', fontfamily='monospace', fontweight='bold', fontsize=15)
             
        if i > 210:
             ax.text(0.12, 0.56, "RUN", color=col_txt, ha='left', fontfamily='monospace', fontweight='bold', fontsize=15)
        
        # The Output Text (Center)
        if i > 240:
             # Flash text with Sine intensity
             alpha = 0.5 + 0.5 * np.sin(i * 0.2)
             ax.text(0.5, 0.4, "LOGIC GARDEN 70", color=C64_COLORS[7], ha='center', 
                     fontfamily='monospace', fontweight='bold', fontsize=25)
             ax.text(0.5, 0.35, "THE BOOTSTRAP", color=C64_COLORS[3], ha='center', 
                     fontfamily='monospace', fontweight='bold', fontsize=20)
        
        filename = os.path.join(out_dir, f"c64_{i:04d}.png")
        plt.savefig(filename, facecolor='black')
        plt.close()
        
        if i % 60 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES} | Raster Line: {y1}")

def draw_raster_bar(buffer, y_center, palette_indices):
    # Draw horizontal lines around y_center
    h, w, _ = buffer.shape
    num_lines = len(palette_indices)
    start_y = y_center - num_lines // 2
    
    for j, color_idx in enumerate(palette_indices):
        y = start_y + j
        if 0 <= y < h:
            color = C64_COLORS[color_idx]
            buffer[y, :] = color # Write entire row

if __name__ == "__main__":
    generate_c64_frames()
