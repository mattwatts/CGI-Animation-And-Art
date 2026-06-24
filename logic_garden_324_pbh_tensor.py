"""
SOVEREIGN CODE: logic_garden_324_pbh_tensor.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 324 (PBH Genesis & Dark Matter Tensor)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Seamless 10.0s Loop. Absolute Vector Spacetime Warping. Continuous Memory Annihilation.
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
OUT_DIR = "frames_324_pbh_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Upper Lattice
C_STEEL     = '#606065'   # Spacetime Grid
C_DARK      = '#202025'   # Deep Shadow Array
C_CYAN      = '#00FFFF'   # Quantum Fluctuation State
C_MAGENTA   = '#FF0055'   # Event Horizon / Radiation
C_GOLD      = '#FFB300'   # Critical Telemetry Warning
C_WHITE     = '#FFFFFF'

# ------------------------------------------------------------------
# O(1) DETERMINISTIC SPACETIME KINEMATICS
# ------------------------------------------------------------------    
def draw_pbh_core(ax, x, y, alpha_m):
    """Rigid Primordial Black Hole Kinematic Core"""
    # Photon Sphere
    ax.add_patch(patches.Circle((x, y), radius=28, fill=False, edgecolor=C_MAGENTA, lw=2.5, alpha=alpha_m*0.8, zorder=8))
    # Event Horizon
    ax.add_patch(patches.Circle((x, y), radius=18, facecolor=C_TEXT, edgecolor=C_CYAN, lw=1, alpha=alpha_m, zorder=8.1))
    # Singularity targeting brackets
    ax.plot([x-40, x-25], [y, y], color=C_TEXT, lw=2, alpha=alpha_m, zorder=8.2)
    ax.plot([x+25, x+40], [y, y], color=C_TEXT, lw=2, alpha=alpha_m, zorder=8.2)

def generate_carrier_states(phase_ratio):
    """Calculates exactly synchronized, perfectly looping PBH matrices"""
    pbh_data = []
    TRACKS = [-300, 0, 300]
    STAGGER = [0.0, 0.333, 0.666]
    EVENTS_PER_TRACK = 3

    for trk_idx, x_p in enumerate(TRACKS):
        for i in range(EVENTS_PER_TRACK):
            t = (phase_ratio + i/float(EVENTS_PER_TRACK) + STAGGER[trk_idx]) % 1.0
            y_p = 900 - t * 2000
            
            # Phase Math for Theoretical States
            depth = 0.0
            width = 120.0
            alpha = 1.0
            state = "QUANTUM" # 0=Quantum, 1=Collapse, 2=PBH, 3=Fade
            
            # PHASE A: 0.0 -> 0.15 (Quantum Fluctuations / Positive Spikes)
            if t < 0.15:
                prog = t / 0.15
                # Exactly 8 high-frequency chaotic bounds, returning perfectly to 0 at t=0.15
                depth = np.sin(prog * np.pi * 8) * (200 * prog)
                width = 150.0
                alpha = prog # Fade in seamlessly at top
                state = "QUANTUM"
                
            # PHASE B: 0.15 -> 0.20 (Stillness before Critical Override)
            elif 0.15 <= t < 0.20:
                depth = 0.0
                state = "CRITICAL"
                
            # PHASE C: 0.20 -> 0.25 (Gravitational Collapse inward)
            elif 0.20 <= t < 0.25:
                prog = (t - 0.20) / 0.05
                depth = -500 * (prog ** 2)
                width = 150.0 - (70 * prog) # Compresses to tight gravity well
                state = "COLLAPSE"
                
            # PHASE D: 0.25 -> 0.85 (Dark Matter PBH Translation)
            elif 0.25 <= t < 0.85:
                depth = -500
                width = 80.0
                state = "PBH"
                
            # PHASE E: 0.85 -> 1.00 (Loop Purge / Fade Out)
            else:
                prog = (t - 0.85) / 0.15
                depth = -500 * ((1.0 - prog)**2)
                width = 80.0
                alpha = max(0.0, 1.0 - prog)
                state = "FADE"
                
            pbh_data.append((x_p, y_p, depth, width, alpha, state))
            
    return pbh_data

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

    # 1. GENERATE PBH EVENT MATRICES
    pbh_matrix = generate_carrier_states(phase_ratio)

    # 2. CONTINUOUS SPACETIME LATTICE (Warp Matrix)
    # The grid translates downwards exactly 1 spacing unit over the full phase to loop seamlessly
    SPACING = 30
    g_offset = phase_ratio * SPACING
    
    # 80 Horizontal Geodesics covering screen to screen
    y_lines_base = np.linspace(1200, -1200, 80) - g_offset
    
    # High fidelity X sampling for aggressive mathematical warping
    x_geo = np.linspace(-600, 600, 250)
    
    for y_base in y_lines_base:
        if y_base > 1000 or y_base < -1000:
            continue
            
        y_geo = np.full_like(x_geo, y_base)
        
        # O(1) Matrix Deformation
        for (px, py, p_depth, p_width, p_alpha, state) in pbh_matrix:
            if abs(y_base - py) < 400 and p_alpha > 0 and p_depth != 0:
                dist_sq = (x_geo - px)**2 + (y_geo - py)**2
                # Lorentzian topographic well mapping
                warp = p_depth * (p_width**2 / (dist_sq + p_width**2))
                y_geo += warp * p_alpha
                
        # Fade Alpha near absolute screen bounds to prevent hard polygon clipping
        bound_alpha = 1.0
        if y_base > 800: bound_alpha = (1000 - y_base) / 200.0
        if y_base < -800: bound_alpha = (y_base + 1000) / 200.0
        
        ax.plot(x_geo, y_geo, color=C_STEEL, lw=1.2, alpha=bound_alpha*0.4, zorder=1)

    # 3. DRAW PBH CORES
    critical_count = 0
    for (px, py, p_depth, p_width, p_alpha, state) in pbh_matrix:
        if state in ["PBH", "COLLAPSE", "FADE"] and p_alpha > 0:
            # We enforce core drawing only if depth is severe enough to represent collapse
            if p_depth < -100:
                draw_pbh_core(ax, px, py + p_depth*p_alpha*0.8, p_alpha) # Core sits dynamically *inside* its well
        
        if state == "CRITICAL":
            critical_count += 1
            # Render pre-collapse structural warning (δ_c)
            ax.add_patch(patches.Rectangle((px-15, py-15), 30, 30, facecolor='none', edgecolor=C_MAGENTA, lw=2, zorder=7))
            ax.add_patch(patches.Rectangle((px-5, py-5), 10, 10, facecolor=C_CYAN, zorder=7))

    # 4. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    ax.text(-500, 880, "LG-324 :: PRIMORDIAL BLACK HOLE GENESIS", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, 840, "[SFI-0.75] INFLATIONARY OVERDENSITY // DARK MATTER HALO TRACE", color=C_CYAN, fontsize=12, fontname='monospace', zorder=80)
    
    # Telemetry Box
    ax.add_patch(patches.Rectangle((-520, -920), 1040, 150, facecolor=C_TITANIUM, alpha=0.9, zorder=79))
    
    ax.text(-500, -825, "CRITICAL DENSITY THRESHOLD: δ ≥ δ_c [COLLAPSE ASSERTED]", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=80)
    
    pulse = abs(np.sin(phase_ratio * 6 * np.pi))
    ax.text(-500, -860, f"LOCAL QUANTUM FLUCTUATIONS (Δp): {pulse * 100:>05.2f} % Δ [INFLATON FIELD]", color=C_MAGENTA if pulse > 0.5 else C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=80)
    
    ax.add_patch(patches.Rectangle((-500, -885), 1000, 4, facecolor=C_STEEL, zorder=80))
    ax.add_patch(patches.Rectangle((-500 + 490*(1-pulse), -885), 20 + 980*pulse, 4, facecolor=C_CYAN, zorder=81))

    # Topological structural lines defining Y-Axis Epochs
    ax.text(-500, 620, "EPOCH 1: HIGH-ENERGY QUANTUM FLUCTUATION (INFLATION)", color=C_CYAN, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    ax.plot([-520, 520], [600, 600], color=C_CYAN, lw=2, linestyle=':', alpha=0.6, zorder=80)

    ax.text(-500, 120, "EPOCH 2: GRAVITATIONAL COLLAPSE BEYOND δ_c", color=C_MAGENTA, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    ax.plot([-520, 520], [100, 100], color=C_MAGENTA, lw=2, linestyle=':', alpha=0.6, zorder=80)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0)
    
    # Absolute Memory Annihilation execution
    plt.close('all')
    gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    # Retain 1 core to prevent OS suffocation during intensive O(1) topological computations
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-324: SCALAR INFLATION PBH TENSOR [CORES: {cpu_cores}] [MEMORY LOCK ACTIVE]")
    
    # HOTFIX: maxtasksperchild=1 explicitly eradicates C-backend fragmentation
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
