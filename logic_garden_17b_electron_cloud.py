"""
PROJECT: Logic Garden 17b (Exact Physical Construct // The Quantum Cloud)
FORMAT: YouTube Shorts (1080x1920)
METADATA: QUANTUM MECHANICS, HYDROGEN 1S, PROBABILITY DENSITY, DAYLIGHT
EXECUTION: 24.0s Sequence. True High-Density Vector Accumulation.
RULES ENFORCED: 
- True Vectorised Rejection Sampling for Probability Density P(r).
- Daylight Palette (White Substrate / High-Contrast Accumulation).
- 'Axiom of Broken Glass': Building solid form out of chaotic instances.
- Purged Jargon. Australian spelling conventions (maths, colour).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import multiprocessing as mp
import os
import gc
import math

# ======== SEQUENCE PARAMETERS ========
DURATION = 24.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
PTS_PER_FRAME = 120    # Density multiplier
TOTAL_POINTS = TOTAL_FRAMES * PTS_PER_FRAME
OUT_DIR = "frames_17b_electron_cloud"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'          # Indestructible Black UI
C_GRID      = '#E2E8F0'          # Bohr Radius Metric Grids
C_PROTON    = '#E11D48'          # Crimson (The Lonely Anchor)
C_ELECTRON  = '#005599'          # Deep Marine (Probability Accumulation)
C_FLASH     = '#FFB300'          # Dense Amber (Instantaneous Wave Collapse)

# ------------------------------------------------------------------
# O(1) VECTORISED REJECTION SAMPLING ENGINE
# ------------------------------------------------------------------
def precompute_quantum_matrix(total_needed):
    """
    Generates exact (X, Y) coordinates matching the 2D projection 
    probability density function of a 1s orbital.
    P(r) ~ exp(-1.5 * r) visually tuned for the Cartesian viewport.
    """
    np.random.seed(17)
    x_vals, y_vals = [], []
    
    print(f"Pre-compiling {total_needed} Quantum Rejection Samples...")
    while len(x_vals) < total_needed:
        batch = 100000
        # Bounding box [-6.0, 6.0]
        rx = (np.random.rand(batch) - 0.5) * 12.0
        ry = (np.random.rand(batch) - 0.5) * 12.0
        r = np.sqrt(rx**2 + ry**2)
        
        # Exponential decay probability
        prob = np.exp(-1.5 * r)
        accept = np.random.rand(batch) < prob
        
        x_vals.extend(rx[accept])
        y_vals.extend(ry[accept])
        
    return np.array(x_vals[:total_needed]), np.array(y_vals[:total_needed])

X_DOMAIN, Y_DOMAIN = precompute_quantum_matrix(TOTAL_POINTS)

# ------------------------------------------------------------------
# PARALLEL GENERATOR (LOGIC TENSORS)
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, )

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f = packet[0]
    
    current_total = (f + 1) * PTS_PER_FRAME
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # 9:16 Aspect Ratio strictly enforced
    ax.set_xlim(-5.4, 5.4)
    ax.set_ylim(-9.6, 9.6)

    # 1. BOHR RADIUS METRIC GRIDS
    ax.plot([-5.4, 5.4], [0, 0], color=C_GRID, lw=1.5, zorder=1)
    ax.plot([0, 0], [-9.6, 9.6], color=C_GRID, lw=1.5, zorder=1)
    
    for r in [1.0, 2.0, 3.0, 4.0]:
        ax.add_patch(patches.Circle((0,0), r, fill=False, edgecolor=C_GRID, lw=1.5, linestyle='dashed', zorder=2))
        ax.text(r + 0.05, 0.05, f"{r} a₀", color=C_TEXT, fontsize=10, fontname='monospace', alpha=0.5, zorder=3)

    # 2. THE PROBABILITY ACCUMULATION (Deep Marine)
    # The ghosts that have already collapsed and faded into the structural cloud
    if current_total > PTS_PER_FRAME:
        ax.scatter(X_DOMAIN[:current_total - PTS_PER_FRAME], 
                   Y_DOMAIN[:current_total - PTS_PER_FRAME], 
                   s=6, color=C_ELECTRON, alpha=0.08, edgecolors='none', zorder=4)

    # 3. THE INSTANTANEOUS WAVEFUNCTION COLLAPSE (Dense Amber)
    # The active observations for the current frame
    active_x = X_DOMAIN[current_total - PTS_PER_FRAME : current_total]
    active_y = Y_DOMAIN[current_total - PTS_PER_FRAME : current_total]
    ax.scatter(active_x, active_y, s=35, color=C_FLASH, alpha=1.0, edgecolors='none', zorder=5)

    # 4. THE PROTON (Absolute Anchor)
    ax.add_patch(patches.Circle((0,0), 0.12, facecolor=C_PROTON, edgecolor=C_BG, lw=1.5, zorder=10))

    # 5. ABSOLUTE DAYLIGHT TELEMETRY (TOP)
    ax.add_patch(patches.Rectangle((-5.4, 8.2), 10.8, 1.4, facecolor=C_BG, zorder=80))
    ax.plot([-5.4, 5.4], [8.2, 8.2], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-5.0, 8.9, "THE HYDROGEN 1s ORBITAL (WAVEFUNCTION)", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=82)
    ax.text(-5.0, 8.5, "LG-17b // KINEMATIC PROBABILITY TENSOR", color=C_ELECTRON, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=82)

    # 6. ABSOLUTE DAYLIGHT TELEMETRY (BOTTOM)
    ax.add_patch(patches.Rectangle((-5.4, -9.6), 10.8, 1.5, facecolor=C_BG, zorder=80))
    ax.plot([-5.4, 5.4], [-8.1, -8.1], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-5.0, -8.6, f"ACCUMULATED OBSERVATIONS : {current_total:06d}", color=C_TEXT, fontsize=20, fontname='monospace', weight='bold', zorder=82)
    ax.text(-5.0, -9.1, f"INSTANTANEOUS COLLAPSES  : {PTS_PER_FRAME:03d} UNITS/FRAME", color=C_FLASH, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    
    # Progress Bar
    prog = current_total / TOTAL_POINTS
    ax.add_patch(patches.Rectangle((-5.4, -9.6), 10.8 * prog, 0.1, facecolor=C_ELECTRON, zorder=85))

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-17b: THE QUANTUM CLOUD (DAYLIGHT) [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Wavefunction Rendered. Stand by for compilation.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
