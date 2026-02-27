"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: anneal_manifest_v1.py
MODE:   Industrialist (Optimization / Aesthetic)
TARGET: Quantum Annealing Energy Landscape (QUBO Visualization)
STYLE:  "The Electric Fog" - IKB Palette | 4K Ready | No Text

AUTHOR: Matt Watts / Assistant Protocol
"""

import sys
import time
import os
import matplotlib
matplotlib.use('Agg') # Headless backend
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

# --- 1. SKEPTIC NODE: INFRASTRUCTURE ---
try:
    import cupy as cp
    xp = cp
    USE_GPU = True
    print("[SYSTEM] GPU DETECTED. ENGAGING HYPER-PLANE ACCELERATION.")
except ImportError:
    xp = np
    USE_GPU = False
    print("[SYSTEM] GPU NOT FOUND. FALLING BACK TO STANDARD MANIFOLD DETECTORS.")

# --- 2. MAJESTIC CONFIGURATION ---
N = 200             # Grid Resolution (200x200 = 40,000 Qubits simulated)
FRAMES = 480        # 20 seconds at 24fps (Slow, meditative anneal)
L = 10.0            # Domain Size

# The Annealing Schedule
# We slowly reduce "Temperature/Tunneling" (T) from High to Zero
T_START = 2.0
T_END = 0.01

# --- 3. PALETTE: THE SOVEREIGN SPECTRUM ---
# 1. The Landscape (Deep IKB -> Indigo)
landscape_cdict = {
    'red':   [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0)],
    'green': [(0.0, 0.02, 0.02), (1.0, 0.1, 0.1)],
    'blue':  [(0.0, 0.08, 0.08), (1.0, 0.4, 0.4)] # Deep Indigo to Muted Blue
}
CMAP_LANDSCAPE = LinearSegmentedColormap('IKB_Deep', landscape_cdict)

# 2. The Quantum Mist (Electric Cyan -> White Singularity)
mist_cdict = {
    'red':   [(0.0, 0.0, 0.0), (0.5, 0.0, 0.0), (1.0, 1.0, 1.0)],
    'green': [(0.0, 0.0, 0.0), (0.5, 0.4, 0.4), (1.0, 1.0, 1.0)],
    'blue':  [(0.0, 0.0, 0.0), (0.5, 1.0, 1.0), (1.0, 1.0, 1.0)],
    'alpha': [(0.0, 0.0, 0.0), (0.2, 0.0, 0.0), (1.0, 0.8, 0.8)] # Transparent at low val
}
CMAP_MIST = LinearSegmentedColormap('Cyan_Energy', mist_cdict)

def generate_qubo_landscape(N):
    """
    Generates a complex 'Cost Surface' with many Local Minima 
    and one Global Minimum (The Optimization Target).
    """
    x = xp.linspace(-3, 3, N)
    y = xp.linspace(-3, 3, N)
    X, Y = xp.meshgrid(x, y)
    
    # 1. The "Basin" (Global Convexity)
    Z = 0.5 * (X**2 + Y**2)
    
    # 2. The "Friction" (High Frequency Noise/Local Traps)
    # Using multiple sine waves to create 'Ruggedness'
    Z += 0.8 * xp.sin(3*X) * xp.cos(3*Y)
    Z += 0.4 * xp.cos(5*X + 1.2)
    
    # 3. The "Deep Void" (Global Minimum Injection)
    # We artificially punch a deep hole at [1.5, -1.5]
    r_target = (X - 1.5)**2 + (Y + 1.5)**2
    Z -= 3.0 * xp.exp(-r_target * 5.0)
    
    return X, Y, Z

def boltzmann_distribution(Z, T):
    """
    Simulates the Quantum Probability Cloud.
    P(x) ~ exp(-Energy / Tunneling_Factor)
    As T -> 0, P concentrates entirely in the Global Minimum.
    """
    # Clip T to avoid division by zero
    T = max(T, 0.001)
    
    # Calculate Probability
    P = xp.exp(-Z / T)
    
    # Normalize (Unit probability)
    P_sum = xp.sum(P)
    P_norm = P / P_sum
    
    # Scale for visualization (make it visible against the mountains)
    return P_norm * 5000.0 # Arbitrary gain for visual height

def render_frame_sovereign(X, Y, Z, P, angle, frame_id):
    """
    Renders the composite 3D artifact efficiently.
    """
    # Device -> Host
    if USE_GPU:
        X_h, Y_h, Z_h, P_h = cp.asnumpy(X), cp.asnumpy(Y), cp.asnumpy(Z), cp.asnumpy(P)
    else:
        X_h, Y_h, Z_h, P_h = X, Y, Z, P

    # Setup Canvas (Cinema 4K Ratio)
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1], projection='3d')
    ax.set_axis_off() # Zero Metadata
    
    # Set "Void" Background
    ax.set_facecolor('#000514') 
    fig.patch.set_facecolor('#000514') 

    # --- LAYER 1: THE LANDSCAPE (The Problem) ---
    # Rendered as a dark, wire-mesh structure texturing
    surf = ax.plot_surface(X_h, Y_h, Z_h, 
                           cmap=CMAP_LANDSCAPE, 
                           linewidth=0, 
                           antialiased=True, 
                           alpha=0.9,
                           rcount=N//2, ccount=N//2) # Optimization for render speed

    # --- LAYER 2: THE MIST (The Solution) ---
    # We offset Z by P to show "Volume"
    # Only plot where Probability is significant to save render cycles
    mask = P_h > 0.05 
    if np.any(mask):
        # We perform a slight Z-shift so the mist floats ABOVE the terrain
        Z_mist = Z_h + P_h * 0.5 
        
        # Visualize the Mist
        ax.plot_surface(X_h, Y_h, Z_mist, 
                        cmap=CMAP_MIST, 
                        linewidth=0,
                        antialiased=True, 
                        alpha=0.6,    # Semitransparent Ghost
                        shade=False,  # Self-luminous
                        rcount=N//2, ccount=N//2)

    # --- CINEMATOGRAPHY ---
    # Orbiting Camera to show depth
    ax.view_init(elev=45, azim=angle)
    ax.dist = 8 # Zoom level

    # Save
    out_dir = "anneal_frames"
    os.makedirs(out_dir, exist_ok=True)
    filename = os.path.join(out_dir, f"anneal_{frame_id:04d}.png")
    
    plt.savefig(filename, facecolor='#000514')
    plt.close()
    
    # VRAM Purge
    if USE_GPU and frame_id % 10 == 0:
        cp.get_default_memory_pool().free_all_blocks()

# --- 4. EXECUTION ---
if __name__ == "__main__":
    t0 = time.time()
    print("[INDUSTRIALIST] Generating QUBO Topology...")
    X, Y, Z = generate_qubo_landscape(N)
    
    # Generate linear annealing schedule
    T_schedule = np.linspace(T_START, T_END, FRAMES)
    
    print(f"[SYNTHESIS] Commencing {FRAMES} frame Annealing Process...")
    
    for i in range(FRAMES):
        # 1. Update Physics (Cooling)
        current_T = T_schedule[i]
        P = boltzmann_distribution(Z, current_T)
        
        # 2. Update Camera (Slow Rotation)
        # Rotate 90 degrees over the full duration
        angle = 30 + (i / FRAMES) * 90 
        
        # 3. Render
        render_frame_sovereign(X, Y, Z, P, angle, i)
        
        # Progress
        sys.stdout.write(f"\r[RENDER] Frame {i:04d} | Temp: {current_T:.2f}")
        sys.stdout.flush()

    print(f"\n[COMPLETED] Total Time: {time.time()-t0:.2f}s")
