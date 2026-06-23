"""
SOVEREIGN CODE: logic_garden_351d_uniform_bound.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 351d (Uniform Boundedness // Banach-Steinhaus)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: FUNCTIONAL ANALYSIS, ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Linear 24.0s Sequence. Daylight Protocol. Custom Z-Sorting. Alpha Bounds Welded.
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
OUT_DIR = "frames_351d_uniform_bound"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Blueprint / Domain Floor
C_STEEL     = '#606065'   # The Bound Operator Framework
C_CYAN      = '#00FFFF'   # Operator Vector Data (Low Threat)
C_MAGENTA   = '#DE008A'   # Operator Vector Data (High Threat)
C_MANTIS    = '#00FF00'   # Theorem Lock / Uniform Bound Canopy
C_GOLD      = '#FFB300'   # Probing Anchor Coordinates

# ------------------------------------------------------------------
# O(1) ORTHOGRAPHIC PROJECTION ENGINE & MATRICES
# ------------------------------------------------------------------
def rotate_x(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])

def rotate_y(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])

def rotate_z(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

def ease_in_out(t):
    t = np.clip(t, 0.0, 1.0)
    return 4 * t**3 if t < 0.5 else 1 - (-2 * t + 2)**3 / 2

# Generator for the Uniform Bound Hex-Plate Canopy
def generate_canopy(radius, z_height, segments=16):
    quads = []
    ths = np.linspace(0, 2*np.pi, segments+1)
    for i in range(segments):
        a1, a2 = ths[i], ths[i+1]
        v1 = [0, 0, z_height]
        v2 = [radius*np.cos(a1), radius*np.sin(a1), z_height]
        v3 = [radius*np.cos(a2), radius*np.sin(a2), z_height]
        v4 = [0, 0, z_height]
        quads.append([v1, v2, v3, v4])
    return np.array(quads)

# Precalculate Family of 40 Linear Operators (2x2 Matrices)
np.random.seed(3514)
N_OPS = 40
R_BASE = 250.0  # Visual radius of the unit sphere

operators = []
global_supremum = 0.0

for _ in range(N_OPS):
    # Generate random matrix
    A = np.random.randn(2, 2)
    # Norm of operator T is max singular value
    norm_A = np.linalg.norm(A, 2)
    operators.append(A)
    if norm_A > global_supremum:
        global_supremum = norm_A
        
Z_SCALE = 380.0 / global_supremum  # Scale so max Z is exactly 380 pixels
Z_MAX = global_supremum * Z_SCALE

CANOPY_GEOM = generate_canopy(R_BASE + 20, Z_MAX)

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

    # CAMERA LOCK
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)
    ax.autoscale(False)
    draw_industrial_grid(ax)

    # 1. KINEMATIC CAMERA MATRIX
    # --------------------------
    rot_matrix = rotate_x(np.radians(-25)) @ rotate_z(np.radians(15) + t * 0.1)
    y_shift = -150  
    
    render_queue = []

    def push_to_queue(quad_list, fc, ec, lw, alpha, force_z=0):
        safe_a = np.clip(alpha, 0.0, 1.0)
        safe_e_a = np.clip(alpha * 1.5, 0.0, 1.0)
        
        for quad in quad_list:
            proj = np.dot(quad, rot_matrix.T)
            depth = np.mean(proj[:, 1]) + force_z
            screen_quad = np.column_stack((proj[:, 0], proj[:, 2] + y_shift))
            render_queue.append({
                'type': 'poly', 'd': depth, 'poly': screen_quad,
                'fc': mcolors.to_rgba(fc, safe_a) if fc != 'none' else 'none',
                'ec': mcolors.to_rgba(ec, safe_e_a), 'lw': lw
            })

    def push_line(p1, p2, color, lw, alpha, force_z=0):
        safe_a = np.clip(alpha, 0.0, 1.0)
        proj = np.dot([p1, p2], rot_matrix.T)
        depth = np.mean(proj[:, 1]) + force_z
        screen_line = np.column_stack((proj[:, 0], proj[:, 2] + y_shift))
        render_queue.append({'type': 'line', 'd': depth, 'line': screen_line, 'color': mcolors.to_rgba(color, safe_a), 'lw': lw})

    def push_point(p, color, size, alpha, ec=None, lw=1, force_z=0):
        safe_a = np.clip(alpha, 0.0, 1.0)
        safe_e_a = np.clip(alpha * 1.5, 0.0, 1.0)
        proj = np.dot(p, rot_matrix.T)
        depth = proj[1] + force_z
        screen_pt = [proj[0], proj[2] + y_shift]
        face_c = mcolors.to_rgba(color, safe_a)
        edge_c = mcolors.to_rgba(ec, safe_e_a) if ec else face_c
        render_queue.append({'type': 'point', 'd': depth, 'pt': screen_pt, 's': size, 'fc': face_c, 'ec': edge_c, 'lw': lw})

    # 2. TIMELINE ALLOCATION
    # ----------------------
    T_PH1_END = 8.0
    T_PH2_END = 16.0
    
    # 3. BASEPLATE RENDERING (The Banach Space)
    # -----------------------------------------
    # Draw Unit Circle Floor
    base_circle = []
    for angle in np.linspace(0, 2*np.pi, 60):
        base_circle.append([R_BASE*np.cos(angle), R_BASE*np.sin(angle), 0])
    for i in range(len(base_circle)-1):
        push_line(base_circle[i], base_circle[i+1], C_STEEL, 3, 0.5)

    # 4. KINEMATIC OPERATOR EVALUATION
    # --------------------------------
    # Phase 1: Pointwise Probing
    anchor_angles = [0, np.pi/2, np.pi, 3*np.pi/2]
    
    if t < T_PH1_END:
        prg = np.clip(t / 8.0, 0.0, 1.0)
        height_mult = ease_in_out(prg)
        
        for ang in anchor_angles:
            x_vec = np.array([np.cos(ang), np.sin(ang)])
            bx = R_BASE * x_vec[0]
            by = R_BASE * x_vec[1]
            push_point([bx, by, 0], C_GOLD, 80, 1.0, ec=C_TEXT, lw=2, force_z=5)
            
            for A in operators:
                T_x = A @ x_vec
                norm_Tx = np.linalg.norm(T_x)
                z_height = norm_Tx * Z_SCALE * height_mult
                
                # Dynamic Threat Coloring
                c_vec = C_MAGENTA if norm_Tx > (global_supremum * 0.7) else C_CYAN
                push_line([bx, by, 0], [bx, by, z_height], c_vec, 1.5, 0.7)
                push_point([bx, by, z_height], c_vec, 15, 0.8, ec=c_vec, force_z=2)

    # Phase 2 & 3: Domain Sweep and Canopy Lock
    else:
        # Full Sweep logic
        sweep_prg = np.clip((t - T_PH1_END) / 6.0, 0.0, 1.0)
        sweep_angles = np.linspace(0, 2*np.pi * sweep_prg, int(120 * sweep_prg) + 1)
        
        for ang in sweep_angles:
            x_vec = np.array([np.cos(ang), np.sin(ang)])
            bx = R_BASE * x_vec[0]
            by = R_BASE * x_vec[1]
            
            for A in operators:
                T_x = A @ x_vec
                norm_Tx = np.linalg.norm(T_x)
                z_height = norm_Tx * Z_SCALE
                
                c_vec = C_MAGENTA if norm_Tx > (global_supremum * 0.7) else C_CYAN
                # Lower alpha for density handling
                push_line([bx, by, 0], [bx, by, z_height], c_vec, 1.0, 0.35) 
                
        # Leading edge anchor
        if sweep_prg < 1.0:
            edge_ang = sweep_angles[-1] if len(sweep_angles) > 0 else 0
            ex = R_BASE * np.cos(edge_ang)
            ey = R_BASE * np.sin(edge_ang)
            push_point([ex, ey, 0], C_GOLD, 100, 1.0, ec=C_TEXT, lw=2, force_z=10)

    # 5. PHASE 3: THE UNIFORM OVERRIDE LOGIC
    # --------------------------------------
    if t > T_PH2_END:
        canopy_prg = np.clip((t - T_PH2_END) / 3.0, 0.0, 1.0)
        c_alpha = ease_in_out(canopy_prg) * 0.5
        
        if c_alpha > 0:
            push_to_queue(CANOPY_GEOM, C_MANTIS, C_STEEL, 2.0, c_alpha, force_z=-10)
            
            # The Rigid Structural Z-Axis Limit Poles
            for ang in anchor_angles:
                px = (R_BASE+20) * np.cos(ang)
                py = (R_BASE+20) * np.sin(ang)
                push_line([px, py, 0], [px, py, Z_MAX], C_STEEL, 4, c_alpha*1.5)

    # 6. ABSOLUTE Z-SORT RENDERING DISPATCH
    # -------------------------------------
    render_queue.sort(key=lambda item: item['d'], reverse=True) 
    
    for item in render_queue:
        if item['type'] == 'poly':
            fc = 'none' if item['fc'] == 'none' else item['fc']
            ax.add_patch(patches.Polygon(item['poly'], facecolor=fc, edgecolor=item['ec'], lw=item['lw'], zorder=50))
        elif item['type'] == 'line':
            pts = item['line']
            ax.plot([pts[0][0], pts[1][0]], [pts[0][1], pts[1][1]], color=item['color'], lw=item['lw'], zorder=50)
        elif item['type'] == 'point':
            pt = item['pt']
            ax.scatter(pt[0], pt[1], s=item['s'], facecolor=item['fc'], edgecolor=item['ec'], lw=item['lw'], zorder=50)

    # ====================================================
    # 7. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)

    ax.text(-500, 890, "LG-351d :: UNIFORM BOUNDEDNESS PRINCIPLE", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] BANACH-STEINHAUS THEOREM // ABSOLUTE LIMITS", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    if t < T_PH1_END:
        s1, c1 = "FAMILY OF LINEAR OPERATORS T_n LAUNCHED", C_CYAN
        s2, c2 = "EVALUATING ANCHOR COORDINATES ON BASEPLATE", C_GOLD
        t_state = "PROVING POINTWISE BOUNDEDNESS: SUP ||T_x|| < ∞"
    elif t < T_PH2_END:
        s1, c1 = "FULL TOPOLOGICAL SWEEP INITIATED", C_MAGENTA
        s2, c2 = "O(N) MASSIVE KINETIC VECTOR DENSITY", C_TEXT
        t_state = "EVALUATING ENTIRE UNIT DOMAIN GEOMETRY..."
    else:
        s1, c1 = "BANACH BASEPLATE COMPLETENESS VERIFIED", C_STEEL
        s2, c2 = "UNIFORM OVERRIDE EXECUTED // CANOPY LOCKED", C_MANTIS
        t_state = "THEOREM LOCK: GLOBAL SUPREMUM BOUND M CONFIRMED"

    ax.text(-500, -760, "SYS_01 [GEOMETRIC STATE]     :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, s1, color=c1, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [DATA INGESTION]      :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, s2, color=c2, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "STRUCTURAL LOAD AUDIT        :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, t_state, color=C_MANTIS if t >= T_PH2_END else C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider
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
    print(f"LG-351d: UNIFORM BOUNDEDNESS PRINCIPLE [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
