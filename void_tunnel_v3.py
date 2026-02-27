"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: void_tunnel_v3.py
MODE:   Industrialist (Aesthetic / High-Res)
TARGET: 3D Quantum Tunneling (The majestic 'Ghost' Protocol)
STYLE:  International Klein Blue | No Text | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import sys
import time
import os
import matplotlib
matplotlib.use('Agg') # Headless backend
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

# --- 1. SKEPTIC NODE: HARDWARE ABSTRACTION ---
try:
    import cupy as cp
    xp = cp
    try:
        # Pre-allocate memory pool for "High Fidelity"
        mempool = cp.get_default_memory_pool()
        print("[SYSTEM] GPU DETECTED. VRAM POOL INITIALIZED.")
    except:
        pass
    USE_GPU = True
except ImportError:
    xp = np
    USE_GPU = False
    print("[SYSTEM] GPU NOT FOUND. RUNNING IN CPU MODE (Expect Latency).")

# --- 2. MAJESTIC CONFIGURATION ---
# "High Fidelity" Grid
N = 128             # 128^3 = ~2 million points. (Increase to 256 only if VRAM > 12GB)
L = 40.0            # Widescreen Stage
DT = 0.02           # Slow-motion time step (finer resolution)
STEPS = 600         # Long duration for "Majestic" flow
FRAMES_SKIP = 2     # Export every 2nd calculation (Effective 300 frames)

# Physics
M_EFF = 1.0
HBAR = 1.0

# The "No-Take Zone" (Barrier)
V0 = 25.0           # High barrier
BARRIER_X = 5.0
BARRIER_W = 1.5

# The "Signal"
# Start further back (-10) to allow the wave to "breathe" before impact
POS_0 = [-12.0, 0.0, 0.0] 
K_0   = [3.5, 0.0, 0.0]

# --- 3. AESTHETIC ENGINE: IKB PALETTE ---
# Defining the "Sovereign" Colormap manually
# Deep Indigo (#000514) -> IKB (#002FA7) -> Electric Cyan (#0064FF) -> Singularity (#FFFFFF)
cdict = {
    'red':   [(0.0, 0.0, 0.0), (0.2, 0.0, 0.0), (0.6, 0.0, 0.0), (1.0, 1.0, 1.0)],
    'green': [(0.0, 0.03, 0.03), (0.2, 0.02, 0.02), (0.6, 0.18, 0.18), (1.0, 1.0, 1.0)],
    'blue':  [(0.0, 0.1, 0.1), (0.2, 0.18, 0.18), (0.6, 0.65, 0.65), (1.0, 1.0, 1.0)]
}
IKB_CMAP = LinearSegmentedColormap('Sovereign_IKB', cdict)

def generate_grid(N, L):
    x = xp.linspace(-L/2, L/2, N)
    y = xp.linspace(-L/2, L/2, N)
    z = xp.linspace(-L/2, L/2, N)
    X, Y, Z = xp.meshgrid(x, y, z, indexing='ij')
    
    k = 2 * xp.pi * xp.fft.fftfreq(N, d=L/N)
    KX, KY, KZ = xp.meshgrid(k, k, k, indexing='ij')
    K2 = KX**2 + KY**2 + KZ**2
    return X, Y, Z, K2

def initial_state(X, Y, Z):
    r2 = (X - POS_0[0])**2 + (Y - POS_0[1])**2 + (Z - POS_0[2])**2
    sigma = 1.8 # Slightly fatter packet for "Majestic" look
    norm = (1.0 / (np.pi * sigma**2))**0.75
    psi = norm * xp.exp(-r2 / (2 * sigma**2)) * xp.exp(1j * (K_0[0]*X))
    return psi

def create_barrier(X):
    V = xp.zeros_like(X)
    mask = (X > BARRIER_X) & (X < BARRIER_X + BARRIER_W)
    V[mask] = V0
    return V

def precompute_operators(V, K2, dt):
    U_V = xp.exp(-0.5j * V * dt / HBAR)
    U_T = xp.exp(-0.5j * K2 * dt / M_EFF / HBAR)
    return U_V, U_T

def export_frame(psi_dev, V_dev, frame_id):
    """
    Renders a 4K-ready, text-free artifact.
    """
    # 1. Device -> Host
    if USE_GPU:
        psi_host = cp.asnumpy(psi_dev)
    else:
        psi_host = psi_dev

    # 2. Slice Density (Z=0)
    rho = np.abs(psi_host)**2
    mid = N // 2
    rho_slice = rho[:, :, mid]

    # 3. Setup The Canvas (16:9 Aspect Ratio)
    # 19.2 x 10.8 inches @ 100 dpi = 1920x1080 (HD) 
    # Increase dpi to 200 for 4K-ish logic
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100) 
    
    # Remove all margins - "Full Bleed"
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    # 4. Render Field
    # Use 'bicubic' interpolation for "Glass Smooth" aesthetic
    # vmin/vmax tuned to keep the background Deep Indigo, not washed out
    ax.imshow(rho_slice.T, 
              extent=[-L/2, L/2, -L/2, L/2], 
              origin='lower', 
              cmap=IKB_CMAP, 
              interpolation='bicubic',
              vmin=0, 
              vmax=np.max(rho)*0.6) # Saturate the core

    # 5. Render The "Ghost" of the Barrier
    # Using a subtle alpha line to show the "Constraint Entity"
    ax.axvline(x=BARRIER_X, color='#0064FF', linewidth=1, alpha=0.3)
    ax.axvline(x=BARRIER_X+BARRIER_W, color='#0064FF', linewidth=1, alpha=0.3)

    # 6. Save Artifact
    out_dir = "majestic_frames"
    os.makedirs(out_dir, exist_ok=True)
    
    # Strict 0000 Sequence Protocol
    filename = os.path.join(out_dir, f"frame_{frame_id:04d}.png")
    
    # Save with Deep Indigo background explicitly
    plt.savefig(filename, facecolor='#000514') 
    plt.close()
    
    # Garbage Collection for long runs
    if frame_id % 20 == 0:
        if USE_GPU:
            mempool.free_all_blocks()

# --- 4. EXECUTION ---
if __name__ == "__main__":
    t0 = time.time()
    print("[INDUSTRIALIST] Initializing Majestic Render Protocol...")
    
    X, Y, Z, K2 = generate_grid(N, L)
    psi = initial_state(X, Y, Z)
    V = create_barrier(X)
    U_V, U_T = precompute_operators(V, K2, DT)
    
    # Frame Counter (Independent of Physics Steps)
    frame_count = 0 
    
    print(f"[SYNTHESIS] Rendering {STEPS} physics steps (Output: ~{STEPS//FRAMES_SKIP} frames)...")
    
    for i in range(STEPS):
        # Physics Engine
        psi *= U_V
        psi_k = xp.fft.fftn(psi)
        psi_k *= U_T
        psi = xp.fft.ifftn(psi_k)
        psi *= U_V
        
        # Validation & Render
        if i % FRAMES_SKIP == 0:
            export_frame(psi, V, frame_count)
            # Progress Bar "Pulse"
            sys.stdout.write(f"\r[RENDER] Frame {frame_count:04d} Complete")
            sys.stdout.flush()
            frame_count += 1

    print(f"\n[COMPLETED] Total Time: {time.time()-t0:.2f}s")
