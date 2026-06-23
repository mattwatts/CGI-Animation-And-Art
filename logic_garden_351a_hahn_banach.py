"""
SOVEREIGN CODE: logic_garden_351a_hahn_banach.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 351a (Hahn-Banach Theorem // The Hyperplane Razor)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: FUNCTIONAL ANALYSIS, ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Linear 24.0s Sequence. Daylight Protocol. Custom Z-Sorting. Alpha Clipping [0,1].
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
DURATION = 24.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_351a_hahn_banach"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # The Norm Canopy (Geometry Boundaries)
C_STEEL     = '#606065'   # Structural Mesh
C_DARK      = '#202025'   # Deep Nodes
C_CYAN      = '#00FFFF'   # The Linear Functional / Hahn-Banach Extension
C_GOLD      = '#FFB300'   # Lower Convex Threat Vector
C_MAGENTA   = '#DE008A'   # Upper Convex Threat Vector
C_MANTIS    = '#00FF00'   # Terminal Green / Verified Separation Hyperplane

# ------------------------------------------------------------------
# O(1) ORTHOGRAPHIC PROJECTION ENGINE & ROTATION MATRICES
# ------------------------------------------------------------------
def rotate_x(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])

def rotate_z(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

def ease_in_out(t):
    t = np.clip(t, 0.0, 1.0)
    return 4 * t**3 if t < 0.5 else 1 - (-2 * t + 2)**3 / 2

def draw_industrial_grid(ax):
    for i in range(-5, 6):
        ax.plot([i*100, i*100], [-960, 960], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)
    for j in range(-9, 10):
        ax.plot([-540, 540], [j*100, j*100], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)

# Generating O(1) Geometry Caches
def generate_cone(rad_max, segments, rings):
    quads = []
    rs = np.linspace(0, rad_max, rings)
    ths = np.linspace(0, 2*np.pi, segments)
    for i in range(len(rs)-1):
        r1, r2 = rs[i], rs[i+1]
        for j in range(len(ths)-1):
            a1, a2 = ths[j], ths[j+1]
            v1 = [r1*np.cos(a1), r1*np.sin(a1), r1]
            v2 = [r2*np.cos(a1), r2*np.sin(a1), r2]
            v3 = [r2*np.cos(a2), r2*np.sin(a2), r2]
            v4 = [r1*np.cos(a2), r1*np.sin(a2), r1]
            quads.append([v1, v2, v3, v4])
    return np.array(quads)

def generate_plane(rad_max, grid_size):
    quads = []
    ls = np.linspace(-rad_max, rad_max, grid_size)
    for i in range(len(ls)-1):
        for j in range(len(ls)-1):
            x1, x2 = ls[i], ls[i+1]
            y1, y2 = ls[j], ls[j+1]
            # Subspace mathematical extension: f(x,y) = 0.8x + 0.4y.
            # Bounded by sqrt(x^2 + y^2) (The Cone) absolutely.
            v1 = [x1, y1, 0.8*x1 + 0.4*y1]
            v2 = [x2, y1, 0.8*x2 + 0.4*y1]
            v3 = [x2, y2, 0.8*x2 + 0.4*y2]
            v4 = [x1, y2, 0.8*x1 + 0.4*y2]
            quads.append([v1, v2, v3, v4])
    return np.array(quads)

def generate_sphere(cx, cy, cz, radius, segments):
    quads = []
    phi = np.linspace(0, np.pi, segments)
    theta = np.linspace(0, 2*np.pi, segments)
    for i in range(len(phi)-1):
        p1, p2 = phi[i], phi[i+1]
        for j in range(len(theta)-1):
            t1, t2 = theta[j], theta[j+1]
            def p(p_, t_): return [cx + radius*np.sin(p_)*np.cos(t_), cy + radius*np.sin(p_)*np.sin(t_), cz + radius*np.cos(p_)]
            quads.append([p(p1, t1), p(p2, t1), p(p2, t2), p(p1, t2)])
    return np.array(quads)

GEOM_CONE = generate_cone(500, 24, 12)
GEOM_PLANE = generate_plane(500, 16)
# Two threatening convex geometric solids
GEOM_CONVEX_A = generate_sphere(0, -180, 250, 100, 10)  # Magenta, above the plane
GEOM_CONVEX_B = generate_sphere(0, 180, -250, 100, 10)  # Gold, below the plane

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

    # 1. KINEMATIC CAMERA MATRIX
    # --------------------------
    rot_matrix = rotate_x(np.radians(-25)) @ rotate_z(t * 0.4)
    y_shift = -150  
    
    # Render Queue for Absolute Z-Sorting
    render_queue = []

    def push_to_queue(quad_list, fc, ec, lw, alpha, force_z=0):
        # SOVEREIGN FIX: Mathematical Bounding Box for Alpha Tuple
        safe_face_alpha = np.clip(alpha, 0.0, 1.0)
        safe_edge_alpha = np.clip(alpha * 1.5, 0.0, 1.0)
        
        for quad in quad_list:
            proj = np.dot(quad, rot_matrix.T)
            depth = np.mean(proj[:, 1]) + force_z
            screen_quad = np.column_stack((proj[:, 0], proj[:, 2] + y_shift))
            render_queue.append({'d': depth, 'poly': screen_quad, 'fc': mcolors.to_rgba(fc, safe_face_alpha), 'ec': mcolors.to_rgba(ec, safe_edge_alpha), 'lw': lw, 'a': safe_face_alpha})

    def push_line(p1, p2, color, lw, alpha, force_z=0):
        # SOVEREIGN FIX: Mathematical Bounding Box for Alpha Tuple
        safe_line_alpha = np.clip(alpha, 0.0, 1.0)
        proj = np.dot([p1, p2], rot_matrix.T)
        depth = np.mean(proj[:, 1]) + force_z
        screen_line = np.column_stack((proj[:, 0], proj[:, 2] + y_shift))
        render_queue.append({'d': depth, 'line': screen_line, 'color': mcolors.to_rgba(color, safe_line_alpha), 'lw': lw, 'a': safe_line_alpha})

    # 2. TIMELINE & DOMAIN ALLOCATION
    # -------------------------------
    T_PHASE1_END = 8.0
    T_PHASE2_END = 16.0
    
    # 3. PHASE 1: THE BOUNDING CANOPY & 1D FUNCTIONAL
    # -----------------------------------------------
    cone_alpha = min(ease_in_out(t/2.0), 1.0) * 0.15 
    push_to_queue(GEOM_CONE, C_TITANIUM, C_STEEL, 1.0, cone_alpha)

    line_prg = np.clip(t / 4.0, 0.0, 1.0)
    line_ext = 500 * ease_in_out(line_prg)
    if line_ext > 0:
        push_line([-line_ext, 0, -0.8*line_ext], [line_ext, 0, 0.8*line_ext], C_CYAN, 8.0, 1.0, force_z=10)
        if t > 4.0 and t < T_PHASE2_END:
            sp_x = np.random.uniform(-line_ext, line_ext)
            sp_z = 0.8 * sp_x
            sp_pt = np.dot([sp_x, 0, sp_z], rot_matrix.T)
            ax.scatter(sp_pt[0], sp_pt[2] + y_shift, s=np.random.uniform(20, 60), color=C_CYAN, zorder=100)

    # 4. PHASE 2: THE HAHN-BANACH CONTINUOUS EXTENSION
    # ------------------------------------------------
    plane_alpha = 0.0
    if t > T_PHASE1_END:
        prg = np.clip((t - T_PHASE1_END) / 4.0, 0.0, 1.0)
        plane_alpha = ease_in_out(prg) * 0.4
    
    # 5. PHASE 3: THE HYPERPLANE SEPARATION ALGORITHM
    # -----------------------------------------------
    vol_alpha = 0.0
    c_plane_fc = C_CYAN
    c_plane_ec = C_CYAN
    lw_plane = 1.0
    
    if t > T_PHASE2_END:
        prg2 = np.clip((t - T_PHASE2_END) / 3.0, 0.0, 1.0)
        vol_alpha = ease_in_out(prg2) * 0.8
        
        plane_alpha = 0.4 + 0.6 * ease_in_out(prg2)
        c_plane_fc = C_TITANIUM
        c_plane_ec = C_MANTIS
        lw_plane = 2.0
        
        push_to_queue(GEOM_CONVEX_A, C_BG, C_MAGENTA, 1.5, vol_alpha)
        push_to_queue(GEOM_CONVEX_B, C_BG, C_GOLD, 1.5, vol_alpha)

    if plane_alpha > 0:
        push_to_queue(GEOM_PLANE, c_plane_fc, c_plane_ec, lw_plane, plane_alpha, force_z=1) 

    # 6. ABSOLUTE Z-SORT RENDERING DISPATCH
    # -------------------------------------
    render_queue.sort(key=lambda item: item['d'], reverse=True) 
    
    for item in render_queue:
        if 'poly' in item:
            ax.add_patch(patches.Polygon(item['poly'], facecolor=item['fc'], edgecolor=item['ec'], lw=item['lw'], zorder=50))
        elif 'line' in item:
            pts = item['line']
            ax.plot([pts[0][0], pts[1][0]], [pts[0][1], pts[1][1]], color=item['color'], lw=item['lw'], zorder=50)

    # ====================================================
    # 7. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)

    ax.text(-500, 890, "LG-351a :: THE HAHN-BANACH THEOREM", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] FUNCTIONAL EXTENSION // THE SEPARATION HYPERPLANE", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    if t < T_PHASE1_END:
        s1, c1 = "O(1) SUBLINEAR CONSTRAINT CANOPY (NORM)", C_STEEL
        s2, c2 = "EVALUATING 1D LOCAL SUBSPACE BOUNDARY", C_CYAN
        t_state = "PROVING LOCAL GEOMETRIC STABILITY..."
    elif t < T_PHASE2_END:
        s1, c1 = "EXECUTING HAHN-BANACH EXTENSION", C_CYAN
        s2, c2 = "SUBLINEAR BOUNDS (f(x) <= p(x)) MAINTAINED", C_TEXT
        t_state = "EXTRUDING FUNCTIONAL TO GLOBAL TOPOLOGY"
    else:
        s1, c1 = "DISJOINT CONVEX SETS (THREAT VECTORS) INGESTED", C_MAGENTA
        s2, c2 = "RIGID HYPERPLANE DROPPED // C_MANTIS LOCK", C_MANTIS
        t_state = "ABSOLUTE GEOMETRIC SEPARATION VERIFIED"

    ax.text(-500, -760, "SYS_01 [GEOMETRIC STATE]     :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, s1, color=c1, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [DATA INGESTION]      :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, s2, color=c2, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "STRUCTURAL LOAD AUDIT        :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, t_state, color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider [Strict Tuples]
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=c1, zorder=83))

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
    print(f"LG-351a: HAHN-BANACH THEOREM [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
