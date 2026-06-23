"""
SOVEREIGN CODE: logic_garden_350_hilbert_isomorphism.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 350 (Hilbert Space // Isomorphism Loop)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: FUNCTIONAL ANALYSIS, ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Exact 16.0s Seamless Loop. Daylight Protocol. C_MANTIS Invariant Subspace.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors  # WELDE TO BASEPLATE
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
DURATION = 16.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_350_hilbert_isomorphism"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Blueprint Ghosting
C_STEEL     = '#606065'   # The Bound Operator (Rigid Mesh)
C_DARK      = '#202025'   # Deep Nodes
C_CYAN      = '#00FFFF'   # l^2 Data Flow
C_MAGENTA   = '#DE008A'   # Kinetic Spallation / Friction
C_MANTIS    = '#00FF00'   # Terminal Green / Invariant Subspace
C_GOLD      = '#FFB300'   # Operator Feedback

# ------------------------------------------------------------------
# O(1) INFINITE DIMENSIONAL PROJECTION ENGINE
# ------------------------------------------------------------------
R_BASE = 540.0
RHO = 0.75               # The Scale Factor per mapped dimension
ROT_STEP = np.pi / 12.0  # The Substrate Twist Array
PHASE_SPEED = 0.5        # Shift 8.0 indices over 16.0 seconds

def get_track_point(s, k):
    """Calculates rigid Cartesian mapping for dimension S along path K"""
    r_cen = R_BASE * (RHO ** s)
    theta = s * ROT_STEP + k * (np.pi / 3.0)
    return r_cen * np.cos(theta), r_cen * np.sin(theta)

def draw_industrial_grid(ax):
    for i in range(-5, 6):
        ax.plot([i*100, i*100], [-960, 960], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)
    for j in range(-9, 10):
        ax.plot([-540, 540], [j*100, j*100], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)

def render_frame(packet):
    f, phase_ratio = packet
    t = phase_ratio * DURATION

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # BARE-METAL CAMERA LOCK
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)
    ax.autoscale(False)
    draw_industrial_grid(ax)

    # 1. KINEMATICS LOGIC MATRIX: THE ISOMORPHISM LOOP
    # ------------------------------------------------
    phase_shift = t * PHASE_SPEED 
    
    # 2. RENDER THE FRACTAL MATRIX (Back to Front / Infinite to Origin)
    # Drawing deeper layers first builds perfect depth sorting 
    for n in range(55, -15, -1):
        s_n = n - phase_shift
        s_np1 = (n + 1) - phase_shift
        
        pts_n = [get_track_point(s_n, k) for k in range(6)]
        pts_np1 = [get_track_point(s_np1, k) for k in range(6)]
        
        r_cen = R_BASE * (RHO ** s_n)
        # Absolute clipping limits to suppress rendering off-screen and pixel-dense singularity
        alpha_dist = np.clip(1.0 - (r_cen / 1200.0)**1.5, 0.0, 1.0)
        alpha_core = np.clip(r_cen / 5.0, 0.0, 1.0)
        alpha = alpha_dist * alpha_core
        
        if alpha <= 0.01:
            continue
            
        # Draw The Diagonal Subspace Connecting Struts
        for k in range(6):
            nxt = (k + 1) % 6
            quad = [pts_np1[k], pts_n[k], pts_n[nxt], pts_np1[nxt]]
            
            # Base Track Logic
            fc = C_TITANIUM
            ec = C_STEEL
            lw = 1.5
            a_f = alpha * 0.05
            
            # *** THE INVARIANT SUBSPACE ***
            # Track 0 and Track 3 form an unbroken mathematical hyper-plane.
            if k == 0 or k == 3: 
                fc = C_MANTIS
                ec = C_MANTIS
                lw = 3.0
                a_f = alpha * 0.20
                
            ax.add_patch(patches.Polygon(quad, facecolor=fc, edgecolor=ec, lw=lw*alpha, alpha=alpha, closed=True, zorder=n))
            
        # Draw The Transverse Ring (Hexagon Subspace Boundary)
        ax.add_patch(patches.Polygon(pts_n, fill=False, edgecolor=C_STEEL, lw=4*alpha, alpha=alpha, zorder=n+0.5))
        
        # Draw The Invariant Subspace Cross-Rung (Connecting K=0 to K=3 directly through origin)
        hr_x = [pts_n[0][0], pts_n[3][0]]
        hr_y = [pts_n[0][1], pts_n[3][1]]
        ax.plot(hr_x, hr_y, color=C_MANTIS, lw=6*alpha, alpha=alpha*0.9, zorder=n+0.6)

    # 3. KINETIC DATA VECTORS FLOWING INTO THE INFINITE
    # -------------------------------------------------
    # Packets race down the C_STEEL tunnels, isolating the C_MANTIS track
    # Packet speed = 1.5. In 16s, travels 24.0 parameter shifts.
    # Base spacing exactly aligns with integer shifts to guarantee the seamless overlay.
    for bs in np.arange(-30, 60, 2.0):
        # S_curr increases, sending them plunging inward.
        S_curr = bs + t * 1.5 
        if S_curr < -15 or S_curr > 50: 
            continue
            
        for k_pkt in [1, 2, 4, 5]:  # Omit the Mantis track
            pk_x, pk_y = get_track_point(S_curr, k_pkt)
            
            r_cen = R_BASE * (RHO ** S_curr)
            alpha_d = np.clip(1.0 - (r_cen / 1200.0)**1.5, 0.0, 1.0)
            alpha_c = np.clip(r_cen / 5.0, 0.0, 1.0)
            alpha = alpha_d * alpha_c
            
            if alpha > 0.02:
                # O(1) Data Tuple
                ax.scatter(pk_x, pk_y, color=C_CYAN, s=50*alpha, zorder=100)
                # Spallation Matrix (Axiom of Broken Glass)
                ax.scatter(pk_x, pk_y, facecolor='none', edgecolor=C_MAGENTA, s=200*alpha, lw=3*alpha, zorder=99)

    # ====================================================
    # 4. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)

    ax.text(-500, 890, "LG-350 :: ISOMORPHIC HILBERT SPACE", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "l^2(ℵ_0) // CONTINUOUS SHIFT OPERATOR KINEMATICS", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    ax.text(-500, -760, "SYS_01 [TOPOLOGY BOUNDS]     :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, "INFINITE-DIMENSIONAL SEPARABLE BASEPLATE", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [DATA INGESTION]      :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, "UNITARY OPERATOR / SEAMLESS TRANSLATION", color=C_CYAN, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "STRUCTURAL LOAD AUDIT        :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, "PROPER INVARIANT SUBSPACE (C_MANTIS) VISUALIZED", color=C_MANTIS, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider [Strict Tuples]
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=C_MANTIS, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close('all')
    gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-350: HILBERT SPACE LOOP [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
