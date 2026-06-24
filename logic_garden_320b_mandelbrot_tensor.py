"""
SOVEREIGN CODE: logic_garden_320b_mandelbrot_tensor.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 320b (Mandelbrot // Feigenbaum Tensor)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Optical Frame Snap Purged. 100% Seamless Infinity Loop achieved via Alpha-Squared Phase Math.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
DURATION = 10.0  # 10.0 Second Seamless Loop
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_320b_mandelbrot_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Shallow Topography
C_STEEL     = '#606065'   # Deep Structural Shadow
C_DARK      = '#202025'   # The Core Singularity Chasm
C_GOLD      = '#FFB300'   # Geometry Tracking Bounding Box
C_CYAN      = '#00FFFF'   # High-Energy Telemetry
C_MAGENTA   = '#FF0055'   # Absolute Zero Point Singularity
C_WHITE     = '#FFFFFF'

# -------- FEIGENBAUM KINEMATIC CONSTANTS --------
FEIGENBAUM_CX = -1.40115518909205060
FEIGENBAUM_CY = 0.0

# 1st Feigenbaum scaling factor (Alpha) squared (pre-calculated to perfectly lock orientation)
FEIGENBAUM_ALPHA_SQ = 6.26454783

# Deeper Base Viewport Width to ensure high visual self-similarity accuracy
BASE_W = 0.001

# ------------------------------------------------------------------
# O(1) CONTINUOUS POTENTIAL FRACTAL ENGINE
# ------------------------------------------------------------------
def generate_mandelbrot_strata(cx, cy, w, res_x=540, res_y=960, max_iter=256):
    h = w * (1920.0 / 1080.0)
    # Forced float64 mapping for deep sub-pixel accuracy
    x = np.linspace(cx - w/2, cx + w/2, res_x, dtype=np.float64)
    y = np.linspace(cy - h/2, cy + h/2, res_y, dtype=np.float64)
    
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    Z = np.zeros_like(C)
    
    escape_time = np.zeros(Z.shape, dtype=np.float64)
    active = np.ones(Z.shape, dtype=bool)

    # Bare-Metal iteration
    for i in range(max_iter):
        if not np.any(active): break
        
        Z[active] = Z[active]**2 + C[active]
        
        escaped_now = np.zeros(Z.shape, dtype=bool)
        escaped_now[active] = np.abs(Z[active]) > 10.0  
        
        absZ = np.abs(Z[escaped_now])
        mu = i + 1 - np.log2(np.log2(absZ))
        escape_time[escaped_now] = mu
        active[escaped_now] = False
        
    escape_time[active] = max_iter
    return escape_time

# Industrial Colormap mapping topology depth
cmap_industrial = matplotlib.colors.LinearSegmentedColormap.from_list(
    "industrial", [C_TITANIUM, C_STEEL, C_DARK, C_CYAN, C_TITANIUM], N=256
)

def render_frame(packet):
    f, phase_ratio = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)

    # 1. THE FRACTAL COHERENCE ARRAY (Absolute Seamless Interlock)
    # Layer A: The active view, zooming in
    w_A = BASE_W / (FEIGENBAUM_ALPHA_SQ ** phase_ratio)
    alpha_A = 1.0 - phase_ratio
    
    # Layer B: The parent matrix, zooming in to replace Layer A perfectly at Frame 600
    w_B = (BASE_W * FEIGENBAUM_ALPHA_SQ) / (FEIGENBAUM_ALPHA_SQ ** phase_ratio)
    alpha_B = phase_ratio

    strata_A = generate_mandelbrot_strata(FEIGENBAUM_CX, FEIGENBAUM_CY, w_A)
    strata_B = generate_mandelbrot_strata(FEIGENBAUM_CX, FEIGENBAUM_CY, w_B)

    # Topological Banding Pattern
    banded_A = (strata_A % 15.0) / 15.0
    banded_B = (strata_B % 15.0) / 15.0

    # Cross-Fade Physics: Ensures exactly identical overlapping scales at boundary constraints
    ax.imshow(banded_B, cmap=cmap_industrial, extent=[-540, 540, -960, 960], alpha=alpha_B, zorder=1)
    ax.imshow(banded_A, cmap=cmap_industrial, extent=[-540, 540, -960, 960], alpha=alpha_A, zorder=2)

    # 2. CONTINUOUS EXPANDING GEOMETRY (Loop-Safe Targeting Rings)
    # Replaces static snapping boxes with a modulo exponential array over 4 rings
    num_rings = 4
    for r in range(num_rings):
        ring_phase = (phase_ratio + r / float(num_rings)) % 1.0
        # Exponential expansion keeping visual uniformity
        scale = FEIGENBAUM_ALPHA_SQ ** ring_phase
        radius_x = 40 * scale
        radius_y = 40 * 1.777 * scale
        ring_alpha = 1.0 - ring_phase # Fades to 0 smoothly at extreme bounds
        
        rect = patches.Rectangle((-radius_x, -radius_y), radius_x*2, radius_y*2, 
                                 facecolor='none', edgecolor=C_GOLD, lw=2, alpha=ring_alpha*0.8, zorder=20)
        ax.add_patch(rect)

    # Internal Target Bounding Box Crosshairs
    ax.plot([-30, 30], [0, 0], color=C_CYAN, lw=2, alpha=0.5, zorder=21)
    ax.plot([0, 0], [-30, 30], color=C_CYAN, lw=2, alpha=0.5, zorder=21)

    # 3. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # All linear constraints purged. Tracking is phase-locked.
    ax.text(-500, 880, "LG-320b :: FEIGENBAUM ACCUMULATION TENSOR", color=C_WHITE, fontsize=24, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, 840, "[SFI-1.00] MATHEMATICAL SINGULARITY // C-SPACE", color=C_CYAN, fontsize=12, fontname='monospace', zorder=80)
    
    ax.add_patch(patches.Rectangle((-520, 770), 1040, 160, facecolor=C_TEXT, alpha=0.8, zorder=79))
    ax.add_patch(patches.Rectangle((-520, -900), 1040, 160, facecolor=C_TEXT, alpha=0.8, zorder=79))

    ax.text(-500, -780, f"REAL BOUNDARY: {FEIGENBAUM_CX:.12f}", color=C_WHITE, fontsize=16, fontname='monospace', weight='bold', zorder=80)
    
    # Sine-wave pulse logic inherently loops perfectly back to 0.0
    pulse = abs(np.sin(phase_ratio * np.pi))
    ax.text(-500, -810, f"COHERENCE TENSOR: {pulse:.4f} Δ [LOCKED]", color=C_GOLD, fontsize=14, fontname='monospace', zorder=80)
    
    ax.add_patch(patches.Rectangle((-500, -840), 1000, 4, facecolor=C_STEEL, zorder=80))
    # Static geometric track marker replacing linear progress
    ax.add_patch(patches.Rectangle((-500 + 990*pulse, -848), 10, 20, facecolor=C_CYAN, zorder=81))

    # The Absolute Zero Point Tracking
    ax.add_patch(patches.Circle((0, 0), radius=6, facecolor=C_MAGENTA, zorder=80))
    ax.text(25, -15, "ABSOLUTE\nZERO POINT\nSINGULARITY", color=C_WHITE, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    ax.plot([15, 60], [0, 0], color=C_WHITE, lw=1.5, zorder=80)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0)
    fig.clf(); plt.close(fig); gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-320b: FEIGENBAUM KINEMATIC TENSOR [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
