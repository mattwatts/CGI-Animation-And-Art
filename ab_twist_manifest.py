"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: ab_twist_manifest.py
MODE:   Industrialist (Topological / Majestic)
TARGET: Aharonov-Bohm "Phase Twist" (Scattering & Interference)
STYLE:  "Consequence Without Contact" - IKB Palette | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import sys
import time
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, hsv_to_rgb
import numpy as np

# --- 1. SKEPTIC NODE: HARDWARE CHECK ---
try:
    import cupy as cp
    xp = cp
    try:
        cp.get_default_memory_pool() # Wake up GPU
    except: pass
    USE_GPU = True
    print("[SYSTEM] GPU DETECTED. TOPOLOGY ENGINE ENGAGED.")
except ImportError:
    xp = np
    USE_GPU = False
    print("[SYSTEM] GPU NOT FOUND. RUNNING IN CPU MODE.")

# --- 2. MAJESTIC CONFIGURATION ---
N = 128             # High Fidelity Grid
L = 30.0            # Widescreen Stage
DT = 0.03           # Fluid Time Step
STEPS = 500         # Duration of the flow
FRAMES_SKIP = 2     

# Physics - The Electron
M_EFF = 1.0
HBAR = 1.0

# The "Flux Line" (Obstacle)
# A cylinder centered at (0,0) extending infinitely in Z
CYLINDER_R = 2.0   # Radius of the void
V0 = 50.0          # "Infinite" Potential Wall

# The "Signal"
# Start Left, Aim Right at the Cylinder
POS_0 = [-10.0, 0.5, 0.0]  # Slightly offset y to break perfect symmetry (Chaos)
K_0   = [4.0, 0.0, 0.0]    # Momentum

# --- 3. AESTHETIC ENGINE: PHASE-REACTIVE IKB ---
# We use a custom shader that maps Density to Brightness 
# and Phase to subtle Hue shifts (Cyan <-> Indigo)

def render_phase_twist(rho, phase, V, frame_id):
    """
    Renders the field with 'Phase Twist' coloring.
    """
    # 1. Canvas Setup 16:9
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    # 2. Normalize Density for Opacity
    # Clip high values to prevent blowout
    alpha = rho / (np.max(rho) * 0.6 + 1e-6)
    alpha = np.clip(alpha, 0, 1)
    
    # 3. Phase Mapping (The Twist)
    # Map phase (-pi, pi) to a tight hue range in Blue/Cyan
    # Base Blue Hue = 0.6 (216 deg). Cyan = 0.5 (180 deg).
    # We map phase to 0.55 +/- 0.1
    normalized_phase = (phase + np.pi) / (2 * np.pi) # 0 to 1
    hues = 0.6 - (normalized_phase * 0.15) # Shift between Deep Blue and Cyan
    
    # Saturation and Value fixed for "Industrial" look
    sats = np.ones_like(alpha) * 0.9  # Deep saturation
    vals = alpha                   # Brightness = Density
    
    # Construct HSV Image
    hsv_img = np.dstack((hues.T, sats.T, vals.T))
    rgb_img = hsv_to_rgb(hsv_img)
    
    # 4. Render The Void (The Flux Line)
    # Overlay the cylinder as a "Negative Space" mask
    # We verify where V is high (the cylinder) and set alpha to 0 (or Black)
    void_mask = V.T > 1.0
    rgb_img[void_mask] = [0, 0.02, 0.08] # Very dark Indigo (The Solenoid)

    ax.imshow(rgb_img, origin='lower', extent=[-L/2, L/2, -L/2, L/2], interpolation='bicubic')
    
    # 5. Save Artifact
    out_dir = "ab_twist_frames"
    os.makedirs(out_dir, exist_ok=True)
    
    filename = os.path.join(out_dir, f"twist_{frame_id:04d}.png")
    plt.savefig(filename, facecolor='#000514')
    plt.close()
    
    if USE_GPU and frame_id % 20 == 0:
        cp.get_default_memory_pool().free_all_blocks()

# --- 4. PHYSICS ENGINE ---

def generate_grid(N, L):
    x = xp.linspace(-L/2, L/2, N)
    y = xp.linspace(-L/2, L/2, N)
    z = xp.linspace(-L/2, L/2, N) # Dummy Z for 3D logic
    X, Y, Z = xp.meshgrid(x, y, z, indexing='ij')
    
    k = 2 * xp.pi * xp.fft.fftfreq(N, d=L/N)
    KX, KY, KZ = xp.meshgrid(k, k, k, indexing='ij')
    K2 = KX**2 + KY**2 + KZ**2
    return X, Y, Z, K2

def create_cylinder(X, Y):
    """
    The Solenoid. Infinite potential inside radius R.
    """
    V = xp.zeros_like(X)
    r2 = X**2 + Y**2
    mask = r2 < CYLINDER_R**2
    V[mask] = V0
    return V

def initial_wavepacket(X, Y, Z):
    r2 = (X - POS_0[0])**2 + (Y - POS_0[1])**2 + (Z - POS_0[2])**2
    sigma = 2.0
    norm = (1.0 / (np.pi * sigma**2))**0.75
    psi = norm * xp.exp(-r2 / (2 * sigma**2)) * xp.exp(1j * K_0[0]*X)
    return psi

def precompute_prop(V, K2, dt):
    # Split Step Operators
    U_V = xp.exp(-0.5j * V * dt / HBAR)
    U_T = xp.exp(-0.5j * K2 * dt / M_EFF / HBAR)
    return U_V, U_T

# --- 5. EXECUTION ---
if __name__ == "__main__":
    t0 = time.time()
    print("[INDUSTRIALIST] Initializing Aharonov-Bohm Topology...")
    
    X, Y, Z, K2 = generate_grid(N, L)
    psi = initial_wavepacket(X, Y, Z)
    V = create_cylinder(X, Y)
    U_V, U_T = precompute_prop(V, K2, DT)
    
    frame_count = 0
    print(f"[SYNTHESIS] Scattering Simulation ({STEPS} steps)...")
    
    for i in range(STEPS):
        # Evolution
        psi *= U_V
        psi_k = xp.fft.fftn(psi) # 3D FFT
        psi_k *= U_T
        psi = xp.fft.ifftn(psi_k)
        psi *= U_V
        
        # Flight Recorder
        if i % FRAMES_SKIP == 0:
            # Device -> Host for One Slice (Z=0)
            mid = N // 2
            if USE_GPU:
                psi_slice = cp.asnumpy(psi[:, :, mid])
                V_slice   = cp.asnumpy(V[:, :, mid])
            else:
                psi_slice = psi[:, :, mid]
                V_slice   = V[:, :, mid]
            
            # Extract Components
            rho = np.abs(psi_slice)**2
            phase = np.angle(psi_slice)
            
            render_phase_twist(rho, phase, V_slice, frame_count)
            
            sys.stdout.write(f"\r[RENDER] Frame {frame_count:04d} Complete")
            sys.stdout.flush()
            frame_count += 1
            
    print(f"\n[COMPLETED] Total Time: {time.time()-t0:.2f}s")
