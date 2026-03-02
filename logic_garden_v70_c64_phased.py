"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v70_c64_phased.py
MODE:   Retro (VIC-II Emulation)
TARGET: Phased Array Beamforming (8-Bit Visualization)
STYLE:  "The Scan" | 20s | C64 Palette | 4K Upscale

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# --- 1. THE VIC-II PALETTE ---
C64 = np.array([
    [0.00, 0.00, 0.00], # 0: Black (Void)
    [1.00, 1.00, 1.00], # 1: White (Peak Energy)
    [0.53, 0.00, 0.00], # 2: Red
    [0.45, 0.75, 0.79], # 3: Cyan (High Energy)
    [0.55, 0.17, 0.55], # 4: Purple
    [0.37, 0.65, 0.29], # 5: Green
    [0.21, 0.16, 0.47], # 6: Blue (Low Energy)
    [0.93, 0.94, 0.46], # 7: Yellow
    [0.55, 0.31, 0.08], # 8: Orange
    [0.28, 0.20, 0.00], # 9: Brown
    [0.75, 0.42, 0.43], # 10: Light Red
    [0.33, 0.33, 0.33], # 11: Dark Grey
    [0.47, 0.47, 0.47], # 12: Grey
    [0.63, 0.95, 0.61], # 13: Light Green
    [0.42, 0.37, 0.71], # 14: Light Blue (Mid Energy)
    [0.70, 0.70, 0.70]  # 15: Light Grey
])

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION

# C64 Resolution
W, H = 320, 200 
# Calculation Resolution (Optimization for Python loop speed)
CALC_W, CALC_H = 160, 100 

def generate_phased_array():
    out_dir = "logic_garden_phased_frames"
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"[C64] Initializing Interferometry Matrix...")
    
    # 1. SETUP EMITTERS
    # 8 Emitters along the bottom
    num_emitters = 8
    # Spread them across the x-axis
    emitter_x = np.linspace(CALC_W * 0.2, CALC_W * 0.8, num_emitters)
    emitter_y = np.ones(num_emitters) * (CALC_H - 5) # Bottom of screen
    
    # 2. PRE-CALCULATE DISTANCE MATRICES (Vectorization Strategy)
    # create grid
    x = np.linspace(0, CALC_W, CALC_W)
    y = np.linspace(0, CALC_H, CALC_H)
    X, Y = np.meshgrid(x, y)
    
    # Tensor: [Emitter, Y, X]
    distances = np.zeros((num_emitters, CALC_H, CALC_W))
    
    for i in range(num_emitters):
        distances[i] = np.sqrt((X - emitter_x[i])**2 + (Y - emitter_y[i])**2)
    
    # Wavelength
    k = 0.5 # Wavenumber
    
    for f in range(TOTAL_FRAMES):
        t = f * 0.2
        
        # 3. BEAM STEERING LOGIC
        # We modulate the phase shift (d_phi) between adjacent emitters
        # Sweep sinusoidal -PI to PI
        scan_angle = np.sin(f * 0.05) * 1.5 
        
        # Calculate Phase for each emitter: phi_i = i * scan_angle
        total_field = np.zeros((CALC_H, CALC_W))
        
        for i in range(num_emitters):
            phase = i * scan_angle
            # Wave Function: sin(k*r - w*t + phi)
            # We treat w*t as propagation
            
            # Simple Interference
            wave = np.sin(distances[i] * k - t + phase)
            
            # Distance Attenuation (1/r) - makes it look like real radar
            # Add minimal epsilon to avoid div/0
            attenuation = 1.0 / (distances[i] * 0.05 + 1.0)
            
            total_field += wave * attenuation

        # 4. COLOR QUANTIZATION (The 8-Bit Look)
        # Map float field to C64 color indices
        # Scale field implies typical range -4 to 4 roughly
        
        # Index Map:
        # < -0.5  : Black (0)
        # -0.5 to 0.0 : Blue (6)
        # 0.0 to 0.5 : Light Blue (14)
        # 0.5 to 1.5 : Cyan (3)
        # > 1.5   : White (1)
        
        color_indices = np.zeros((CALC_H, CALC_W), dtype=int)
        
        color_indices[total_field < -0.2] = 0  # Void
        color_indices[(total_field >= -0.2) & (total_field < 0.1)] = 6  # Deep Blue
        color_indices[(total_field >= 0.1) & (total_field < 0.5)] = 14 # Light Blue
        color_indices[(total_field >= 0.5) & (total_field < 1.0)] = 3  # Cyan
        color_indices[total_field >= 1.0] = 1  # White Hot
        
        # 5. EXPAND TO FULL RES (Nearest Neighbor)
        # Repeat elements to scale up 2x
        buffer_idx = color_indices.repeat(2, axis=0).repeat(2, axis=1)
        
        # Look up colors
        buffer_rgb = C64[buffer_idx]
        
        # 6. OVERLAY SCANLINES (CRT Effect)
        # Darken every second row
        buffer_rgb[1::2, :] *= 0.75
        
        # 7. DRAW EMITTERS
        # Draw physical dots at bottom
        for i in range(num_emitters):
            ex, ey = int(emitter_x[i]*2), int(emitter_y[i]*2)
            # Draw a little box
            buffer_rgb[ey-4:ey, ex-3:ex+3] = C64[7] # Yellow boxes
            if (f // 10) % 2 == 0:
                 buffer_rgb[ey-2:ey, ex-1:ex+1] = C64[2] # Red Blink
        
        # 8. RENDER HUD
        fig = plt.figure(figsize=(10, 10), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        fig.add_axes(ax)
        ax.set_axis_off()
        
        ax.imshow(buffer_rgb, interpolation='nearest', aspect='auto')
        
        # HUD Text
        ax.text(W/2, 20, "LOGIC GARDEN 70: PHASED ARRAY", color=C64[14]/255.0, ha='center',
                fontfamily='monospace', fontweight='bold', fontsize=20)
        
        beam_deg = int(np.degrees(scan_angle))
        ax.text(W/2, 180, f"PHASE SHIFT: {beam_deg:+03d}^", color="white", ha='center',
                fontfamily='monospace', fontweight='bold', fontsize=15)
        
        # Save
        filename = os.path.join(out_dir, f"phased_{f:04d}.png")
        plt.savefig(filename, facecolor='black')
        plt.close()
        
        if f % 60 == 0:
            print(f"Frame {f}/{TOTAL_FRAMES} | Steering Angle: {beam_deg}")

if __name__ == "__main__":
    generate_phased_array()
