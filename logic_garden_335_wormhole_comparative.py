"""
SOVEREIGN CODE: logic_garden_335_wormhole_comparative.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Vectorization
SCENE: Logic Garden 335 (Topological Metric Geometry // ER vs Ellis)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Seamless 10.0s Loop. Absolute Camera Lock. Tuple Rupture Sealed.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import multiprocessing as mp
import matplotlib.colors as mcolors
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
DURATION = 10.0  # 10.0 Second Seamless Loop
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_335_wormhole"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Distant Spacetime Manifold
C_STEEL     = '#606065'   # Upper Envelope Metric
C_DARK      = '#202025'   # Transiting Baryonic Mass
C_CYAN      = '#00FFFF'   # Negative Exotic Energy (Ellis Stabilizer)
C_AZURE     = '#007FFF'   # Stable Geodesic
C_MAGENTA   = '#FF0055'   # Metric Collapse / Singularity Crush
C_GOLD      = '#FFB300'   # Spallation Flash
C_WHITE     = '#FFFFFF'

# -------- O(1) GEOMETRY SETTINGS --------
NX = 50   # Longitudinal segments
NTh = 24  # Radial segments
X_RANGE = 450
Z_TILT = 0.35 # Perspective tilt multiplier

def project_wormhole(ax, center_y, R_throat, is_ellis, phase):
    """Rigid generation of the 3D Topological Funnel mapped to 2D."""
    
    xs = np.linspace(-X_RANGE, X_RANGE, NX)
    thetas = np.linspace(0, 2*np.pi, NTh, endpoint=False)
    
    # Pre-allocate 2D buffers
    x2d = np.zeros((NX, NTh))
    y2d = np.zeros((NX, NTh))
    z3d = np.zeros((NX, NTh))
    
    # The Shape Equation (Flamm's paraboloid cross-section pseudo-analog)
    # The mouth flares extremely wide at the edges, pinches to R_throat in center
    a_term = (450 - R_throat) / (X_RANGE**1.8)
    
    for i, x in enumerate(xs):
        r_current = R_throat + a_term * (abs(x)**1.8)
        for j, th in enumerate(thetas):
            # 3D coordinates (Tilted cylinder lying on X-axis)
            z_raw = r_current * np.cos(th)
            y_raw = r_current * np.sin(th)
            
            # Simple isometric projection pseudo-camera
            x2d[i, j] = x - z_raw * 0.15
            y2d[i, j] = center_y + y_raw - z_raw * Z_TILT
            z3d[i, j] = z_raw

    # Render arrays
    
    # Longitudinal lines (Flowing through throat)
    for j in range(NTh):
        depth_order = np.mean(z3d[:, j])
        alpha = 0.15 if depth_order < -50 else 0.6  # Fade the backface
        lw = 1.0 if depth_order < 0 else 2.0
        
        col = C_STEEL
        if is_ellis:
            col = C_AZURE if depth_order < 0 else C_CYAN
            
        ax.plot(x2d[:, j], y2d[:, j], color=col, alpha=alpha, lw=lw, zorder=2 + (depth_order/1000))

    # Radial Rings (Slices of spacetime)
    for i in range(NX):
        # Tie the ring
        ring_x = np.append(x2d[i, :], x2d[i, 0])
        ring_y = np.append(y2d[i, :], y2d[i, 0])
        ring_z = np.mean(z3d[i, :])
        
        # Color mechanics: Highlight the throat
        dist_from_center = abs(xs[i])
        heat = max(0, 1.0 - (dist_from_center / 200.0))
        
        col = C_TITANIUM
        alpha = 0.4
        lw = 1.0
        
        if is_ellis:
            if heat > 0.1:
                col = C_CYAN
                alpha = 0.5 + heat * 0.5
                lw = 1.0 + heat * 2.0
        else:
            if heat > 0.1 and R_throat < 30:
                col = C_MAGENTA # Glowing red hot as it collapses
                alpha = 0.5 + heat * 0.5
                lw = 1.0 + heat * 2.0

        ax.plot(ring_x, ring_y, color=col, alpha=alpha, lw=lw, zorder=3 + (ring_z/1000))

def render_frame(packet):
    f, phase_ratio = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    
    # ----------------------------------------------------
    # BARE-METAL CAMERA LOCK: ALL AUTO-SCALING ANNIHILATED
    # ----------------------------------------------------
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)
    ax.autoscale(False)

    # ====================================================
    # 1. THE EINSTEIN-ROSEN GATE (UPPER CHAMBER)
    # ====================================================
    ER_Y = 320
    
    # The gravitational collapse function:
    # Mouth starts at R=80, rapidly pinches to 0 exactly at phase=0.5, reopens perfectly for loop
    crush_factor = (np.sin(phase_ratio * np.pi) ** 14)
    ER_R = 80 * (1.0 - crush_factor)
    
    project_wormhole(ax, ER_Y, ER_R, is_ellis=False, phase=phase_ratio)
    
    # Particle Dynamics (ER) - Attempting transit
    er_px = -X_RANGE + (X_RANGE*2) * phase_ratio
    # Annihilated?
    crushed = (phase_ratio > 0.48) and (phase_ratio < 0.54)
    gone = phase_ratio >= 0.54
    
    if not gone and not crushed:
        er_py = ER_Y - er_px * 0.05
        ax.scatter(er_px, er_py, c=C_DARK, s=250, edgecolors=C_BG, lw=3, zorder=10)
        ax.text(er_px, er_py+40, "MASS_01", color=C_DARK, fontsize=12, weight='bold', ha='center', zorder=11)
        ax.plot([er_px-60, er_px], [er_py, er_py], color=C_STEEL, lw=2, zorder=9) # Speed line
        
    if crushed:
        # Singularity Spallation Flash
        burst_a = 1.0 - ((phase_ratio - 0.48) / 0.06)
        r_burst = 300 * (1.0 - burst_a)
        ax.scatter(0, ER_Y, c=C_BG, s=r_burst*10, edgecolors=C_MAGENTA, lw=8*burst_a, alpha=burst_a, zorder=20)
        ax.scatter(0, ER_Y, c=C_GOLD, s=r_burst*5, alpha=burst_a, zorder=21)
        ax.plot([-300, 300], [ER_Y, ER_Y], color=C_MAGENTA, lw=6*burst_a, alpha=burst_a, zorder=20)

    # ====================================================
    # 2. THE ELLIS-BRONNIKOV WORMHOLE (LOWER CHAMBER)
    # ====================================================
    ELLIS_Y = -350
    
    # Engineered stability limit: Throat is rigidly propped open by Exotic Matter
    ELLIS_R = 80
    
    project_wormhole(ax, ELLIS_Y, ELLIS_R, is_ellis=True, phase=phase_ratio)
    
    # Particle Dynamics (Ellis) - Flawless Geodesic Transit
    el_px = -X_RANGE + (X_RANGE*2) * phase_ratio
    # Simulate internal trajectory "dip"
    el_py = ELLIS_Y + 15 * np.sin(phase_ratio * 4 * np.pi) 
    
    ax.scatter(el_px, el_py, c=C_DARK, s=250, edgecolors=C_BG, lw=3, zorder=10)
    ax.text(el_px, el_py+40, "MASS_02", color=C_AZURE, fontsize=12, weight='bold', ha='center', zorder=11)
    ax.plot([el_px-80, el_px], [el_py, el_py], color=C_CYAN, lw=3, zorder=9)

    # ====================================================
    # 3. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    
    # --- TOP MAIN HEADER ---
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-335 :: TOPOLOGICAL METRIC COMPARISON", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-0.75] EINSTEIN-ROSEN GATE VS ELLIS WORMHOLE", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    # --- CENTER HUD: ER STATS ---
    ax.add_patch(patches.Rectangle((-540, -10), 1080, 140, facecolor=C_BG, edgecolor=C_TITANIUM, lw=2, alpha=0.9, zorder=80))
    ax.text(-500, 85, "SYSTEM 01 : EINSTEIN-ROSEN BRIDGE (NATURAL)", color=C_TEXT, fontsize=18, fontname='monospace', weight='bold', zorder=82)
    
    er_status = "STABLE (EMPTY)" if ER_R > 20 else "GRAVITATIONAL CRUSH / ANNIHILATION"
    er_col = C_STEEL if ER_R > 20 else C_MAGENTA
    ax.text(-500, 45, f"EXOTIC MASS : 0.00kg // METRIC STATUS: {er_status}", color=er_col, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    
    # ER dynamic pressure bar [Strict Tuple Geometry Verified]
    ax.add_patch(patches.Rectangle((-500, 20), 1000, 4, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500+(500*crush_factor), 20), 1000*(1.0-crush_factor), 4, facecolor=er_col, zorder=83))

    # --- BOTTOM HUD: ELLIS STATS ---
    ax.add_patch(patches.Rectangle((-540, -880), 1080, 200, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-680, -680], color=C_TEXT, lw=4, zorder=81)

    ax.text(-500, -740, "SYSTEM 02 : ELLIS-BRONNIKOV WORMHOLE (ENGINEERED)", color=C_TEXT, fontsize=18, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -780, "EXOTIC MASS : ACTIVE // NEGATIVE ENERGY TENSOR DEPLOYED", color=C_CYAN, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -810, "METRIC STATUS: GEODESIC TRAVERSABLE", color=C_AZURE, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    pulse = np.sin(phase_ratio * 10 * np.pi) ** 2
    ax.text(280, -810, f"STABILITY FLUX: {pulse*100:>05.2f}%", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Track
    ax.add_patch(patches.Rectangle((-500, -850), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -850), 1000 * phase_ratio, 6, facecolor=C_DARK, zorder=83))

    # Sovereign Execution Output
    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    # Absolute Memory Annihilation
    plt.close('all')
    gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-335: METRIC COMPARISON TENSOR [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE] [Tuples Sealed]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
