"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v69_lens_fixed.py
MODE:   Study (Relativistic)
TARGET: Gravitational Lensing (Einstein Ring)
STYLE:  "The Lens" | 20s | 600 Frames | 4K Ready
STATUS: PATCHED (Fixed Channel Slicing)

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# --- 1. THE VOID PALETTE ---
BG_DEEP = [0.0, 0.02, 0.06] # Deep Indigo RGB
IKB_BLUE = [0.0, 0.18, 0.65] # International Klein Blue
CYAN_SRC = [0.0, 1.0, 1.0]   # Electric Cyan
EVENT_HORIZON = [0.0, 0.0, 0.0]
RING_GLOW = [0.0, 0.5, 1.0]

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
RES = 1000                 # Resolution (Square)
LIMIT = 8.0                # Spatial Extent (-8 to 8)

def generate_lens_frames():
    # 1. SETUP THE GRID (Vectorized Spacetime)
    # This represents the Image Plane (Theta) - what the observer sees
    x = np.linspace(-LIMIT, LIMIT, RES)
    y = np.linspace(-LIMIT, LIMIT, RES)
    X, Y = np.meshgrid(x, y)
    
    # Polar Coordinates (for radial symmetry of the lens)
    Theta_r = np.sqrt(X**2 + Y**2)
    
    # Safety: Avoid division by zero at the singularity
    Theta_r_safe = np.where(Theta_r < 0.05, 0.05, Theta_r)
    
    # 2. LENS PARAMETERS
    Theta_E = 2.5 # Einstein Radius
    
    # 3. LENS EQUATION (The Deflection)
    # We map 'Image Plane' pixels BACK to 'Source Plane' coordinates.
    # Beta = Theta - (Theta_E^2 / Theta)
    factor = 1.0 - (Theta_E**2 / (Theta_r_safe**2))
    
    Beta_x = X * factor
    Beta_y = Y * factor
    
    # 4. MASKS
    # Event Horizon (The Black Hole itself)
    horizon_mask = Theta_r < (Theta_E * 0.3)
    
    # Einstein Ring Marker (Faint guide)
    ring_guide = np.abs(Theta_r - Theta_E) < 0.02

    # 5. RENDER LOOP
    out_dir = "logic_garden_lens_frames"
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"[RELATIVITY] Warping Spacetime ({TOTAL_FRAMES} frames)...")
    
    # Pre-allocate image buffer
    img_buffer = np.zeros((RES, RES, 3))
    
    # Source Motion Path
    # Pass directly behind center to create the ring
    # Start: (-6, -1.5) -> End: (6, 1.5)
    src_start = np.array([-6.0, -1.5])
    src_end = np.array([6.0, 1.5])
    
    for i in range(TOTAL_FRAMES):
        t = i / TOTAL_FRAMES
        
        # Current Source Position (Beta)
        # Add a slight Sine wave to make it 'orbit' visually
        src_pos = src_start * (1-t) + src_end * t
        src_pos[1] += np.sin(t * np.pi) * 0.5 
        
        # 6. CALCULATE INTENSITY
        # Distance determines if a ray hits the source in the Source Plane
        dist_sq = (Beta_x - src_pos[0])**2 + (Beta_y - src_pos[1])**2
        
        # Source Profile (Gaussian)
        radius_sq = 0.5**2
        # Use simple exponential falloff
        intensity = np.exp(-dist_sq / radius_sq)
        
        # 7. COMPOSITE IMAGE
        # Reset background
        img_buffer[:, :, 0] = BG_DEEP[0]
        img_buffer[:, :, 1] = BG_DEEP[1]
        img_buffer[:, :, 2] = BG_DEEP[2]
        
        # Add Source Light (Cyan)
        # We process 'intensity' which is (1000, 1000)
        
        # Additive Blending: Add intensity to G and B channels (Cyan)
        img_buffer[:, :, 1] += intensity * CYAN_SRC[1]
        img_buffer[:, :, 2] += intensity * CYAN_SRC[2]
        
        # White hot core (add to Red to make it white where very bright)
        # Correctly sliced: [All Rows, All Cols, Channel 0]
        core = np.maximum(0, intensity - 0.7) * 3.0
        img_buffer[:, :, 0] += core 
        img_buffer[:, :, 1] += core
        img_buffer[:, :, 2] += core
        
        # Add Ring Guide (Blue Glow)
        img_buffer[ring_guide] += np.array(RING_GLOW) * 0.3
        
        # Apply Horizon (Black Hole) - Mask sets all channels to 0
        img_buffer[horizon_mask] = EVENT_HORIZON
        
        # Clip to valid range
        img_final = np.clip(img_buffer, 0.0, 1.0)
        
        # 8. PLOT
        fig = plt.figure(figsize=(10, 10), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        fig.add_axes(ax)
        ax.set_axis_off()
        
        ax.imshow(img_final, origin='lower')
        
        # HUD
        ax.text(RES/2, RES*0.05, "LOGIC GARDEN 69: THE LENS", color="#0088FF", ha='center', 
                fontfamily='monospace', fontweight='bold', fontsize=18)
        
        # Alignment indicator
        miss_dist = np.sqrt(src_pos[0]**2 + src_pos[1]**2)
        if miss_dist < 0.5:
             # Just drawing it on top of image
             ax.text(RES/2, RES/2, "EINSTEIN RING", color="white", ha='center', va='center',
                     fontfamily='monospace', fontsize=14, alpha=0.8, fontweight='bold')

        filename = os.path.join(out_dir, f"lens_{i:04d}.png")
        plt.savefig(filename, facecolor='black')
        plt.close()
        
        if i % 60 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES} | Beta: {miss_dist:.2f}")

if __name__ == "__main__":
    generate_lens_frames()
