"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: vacuum_hiss_bright.py
MODE:   Industrialist (High Gain / Cherenkov)
TARGET: Quantum Vacuum Fluctuations ("The Electric Hiss")
STYLE:  "Luminous Aether" - IKB to Cyan | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import sys
import time
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

# --- 1. SKEPTIC NODE: INFRASTRUCTURE ---
try:
    import cupy as cp
    xp = cp
    USE_GPU = True
    print("[SYSTEM] GPU DETECTED. HIGH-GAIN SPECTRAL ENGINE ENGAGED.")
except ImportError:
    xp = np
    USE_GPU = False
    print("[SYSTEM] GPU NOT FOUND. RUNNING IN CPU MODE.")

# --- 2. CONFIGURATION ---
N = 512             # Resolution
FRAMES = 360        # Duration
EXPONENT = 1.3      # Slightly "crunchier" noise for more detail
SCALE_FACTOR = 5.0  # Time evolution speed

# --- 3. AESTHETIC: THE CHERENKOV SPECTRUM ---
# We map the scalar field values to color intensity.
# Range: Deep Blue -> Electric Cyan -> White Hot
cdict = {
    'red':   [
        (0.0, 0.0, 0.0),  # Black start
        (0.6, 0.0, 0.0),  # Stay cool blue mid-tones
        (1.0, 0.9, 0.9)   # White hot peaks
    ],
    'green': [
        (0.0, 0.0, 0.0),  # Black start
        (0.5, 0.2, 0.2),  # Mid-cyan
        (1.0, 1.0, 1.0)   # White
    ],
    'blue':  [
        (0.0, 0.05, 0.05), # Deepest Indigo Base (Not pure black)
        (0.4, 0.8, 0.8),   # Strong Electric Blue Mids
        (1.0, 1.0, 1.0)    # White
    ]
}
CMAP_LUMINOUS = LinearSegmentedColormap('Cherenkov_Blue', cdict)

def generate_noise_field(N, exponent, seed=137): # Fine-structure constant seed
    """Generates the frequency domain seed."""
    xp.random.seed(seed)
    k = 2 * xp.pi * xp.fft.fftfreq(N)
    KX, KY = xp.meshgrid(k, k)
    K = xp.sqrt(KX**2 + KY**2)
    K[0,0] = 1.0 
    
    # Amplitude ~ 1/k^alpha
    amplitude = 1.0 / (K ** exponent)
    amplitude[0,0] = 0.0
    
    # Random Phase
    phase = xp.random.uniform(0, 2*xp.pi, (N, N))
    return amplitude, phase

def render_bright_frame(amplitude, phase_0, t, frame_id):
    """
    Renders the field with high exposure.
    """
    # 1. Evolution Logic
    # We rotate phase to simulate "boiling"
    phase_t = phase_0 + t 
    spectrum = amplitude * xp.exp(1j * phase_t)
    
    # 2. Field Reconstruction
    field = xp.fft.ifft2(spectrum).real
    
    # 3. Normalization (Standard Score)
    # This ensures consistent brightness regardless of random seed
    field = (field - xp.mean(field)) / xp.std(field)
    
    # 4. Data Transfer
    if USE_GPU:
        field_h = cp.asnumpy(field)
    else:
        field_h = field

    # 5. Canvas Setup
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    # 6. The "High ISO" Render
    # vmin/vmax are critical here.
    # vmin=-1.0: We show more of the "dip" as darkness, but not crushed.
    # vmax=2.5:  We allow the peaks to hit white earlier.
    ax.imshow(field_h, 
              cmap=CMAP_LUMINOUS, 
              interpolation='bicubic',
              vmin=-1.5, vmax=2.5) 

    # 7. Save
    out_dir = "vacuum_bright_frames"
    os.makedirs(out_dir, exist_ok=True)
    filename = os.path.join(out_dir, f"hiss_{frame_id:04d}.png")
    
    # Background match
    plt.savefig(filename, facecolor='#000514') 
    plt.close()

# --- 4. EXECUTION ---
if __name__ == "__main__":
    t0 = time.time()
    print("[INDUSTRIALIST] Amplifying Vacuum Signal...")
    
    amplitude, phase_0 = generate_noise_field(N, EXPONENT)
    
    print(f"[SYNTHESIS] Rendering {FRAMES} High-Gain Frames...")
    
    for i in range(FRAMES):
        # Time Step
        t = (i / FRAMES) * 2 * np.pi * SCALE_FACTOR
        
        render_bright_frame(amplitude, phase_0, t, i)
        
        sys.stdout.write(f"\r[RENDER] Frame {i:04d} Complete")
        sys.stdout.flush()
        
    print(f"\n[COMPLETED] Total Time: {time.time()-t0:.2f}s")
