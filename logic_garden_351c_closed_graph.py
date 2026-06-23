"""
SOVEREIGN CODE: logic_garden_351c_closed_graph.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 351c (Closed Graph Theorem // The Continuity Razor)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: FUNCTIONAL ANALYSIS, ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Linear 24.0s Sequence. Daylight Protocol. Custom Z-Sorting Queue. Alpha Bounds Welded.
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
OUT_DIR = "frames_351c_closed_graph"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Blueprint / Domain Floor
C_STEEL     = '#606065'   # The Bound Operator Framework
C_CYAN      = '#00FFFF'   # The Graph Plane / Data Path
C_MAGENTA   = '#DE008A'   # Kinetic Friction / Unbounded Threat (Suppressed)
C_MANTIS    = '#00FF00'   # Theorem Lock / Bounded Verification
C_GOLD      = '#FFB300'   # The Trajectory Limit Target

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

# Generate Graph Plane Quads
def generate_plane(rad_max, grid_size, mult_x, mult_y):
    quads = []
    ls = np.linspace(-rad_max, rad_max, grid_size)
    for i in range(len(ls)-1):
        for j in range(len(ls)-1):
            x1, x2 = ls[i], ls[i+1]
            y1, y2 = ls[j], ls[j+1]
            v1 = [x1, y1, mult_x*x1 + mult_y*y1]
            v2 = [x2, y1, mult_x*x2 + mult_y*y1]
            v3 = [x2, y2, mult_x*x2 + mult_y*y2]
            v4 = [x1, y2, mult_x*x1 + mult_y*y2]
            quads.append([v1, v2, v3, v4])
    return np.array(quads)

# Generate Bounding Box Wireframes connecting top and bottom
def generate_bound_box(rad_max, mult_x, mult_y):
    # Determine max Z
    max_z = abs(mult_x * rad_max) + abs(mult_y * rad_max) + 50
    quads = []
    # Base Box
    quads.append([[rad_max, rad_max, -max_z], [rad_max, -rad_max, -max_z], [-rad_max, -rad_max, -max_z], [-rad_max, rad_max, -max_z]])
    quads.append([[rad_max, rad_max, max_z], [rad_max, -rad_max, max_z], [-rad_max, -rad_max, max_z], [-rad_max, rad_max, max_z]])
    
    # 4 Vertical Walls
    quads.append([[rad_max, rad_max, -max_z], [rad_max, -rad_max, -max_z], [rad_max, -rad_max, max_z], [rad_max, rad_max, max_z]])
    quads.append([[-rad_max, -rad_max, -max_z], [-rad_max, rad_max, -max_z], [-rad_max, rad_max, max_z], [-rad_max, -rad_max, max_z]])
    quads.append([[rad_max, -rad_max, -max_z], [-rad_max, -rad_max, -max_z], [-rad_max, -rad_max, max_z], [rad_max, -rad_max, max_z]])
    quads.append([[-rad_max, rad_max, -max_z], [rad_max, rad_max, -max_z], [rad_max, rad_max, max_z], [-rad_max, rad_max, max_z]])
    return np.array(quads)

MX, MY = 0.5, 0.4
GEOM_PLANE = generate_plane(350, 16, MX, MY)
GEOM_BOX = generate_bound_box(350, MX, MY)

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
    rot_matrix = rotate_x(np.radians(-25)) @ rotate_z(np.radians(25) + t * 0.15)
    y_shift = -100  
    
    # Absolute O(1) Z-Sorting render queue
    render_queue = []

    def push_to_queue(quad_list, fc, ec, lw, alpha, force_z=0):
        safe_a = np.clip(alpha, 0.0, 1.0)
        safe_e_a = np.clip(alpha * 1.5, 0.0, 1.0)
        
        for quad in quad_list:
            proj = np.dot(quad, rot_matrix.T)
            depth = np.mean(proj[:, 1]) + force_z
            # Backface check for solid geometries (Optional, using for bounding box walls)
            v1, v2, v3 = proj[0], proj[1], proj[2]
            nrm = np.cross(v2 - v1, v3 - v1)
            if nrm[2] < 0 and fc != 'none':
                continue # Cull backfaces if filled
                
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
    T_PH1_END = 6.0
    T_SEQ_END = 16.0
    
    # 3. PHASE 1: THE GRAPH PLANE
    # ---------------------------
    plane_alpha = np.clip(t / 4.0, 0.0, 1.0) * 0.4
    if plane_alpha > 0:
        push_to_queue(GEOM_PLANE, C_BG, C_CYAN, 1.0, plane_alpha)
        
    # Cartesian Axes Tracking
    ax_a = np.clip(t / 2.0, 0.0, 1.0) * 0.8
    if ax_a > 0:
        push_line([0,0,-400], [0,0,400], C_STEEL, 3, ax_a)
        push_line([-400,0,0], [400,0,0], C_TITANIUM, 4, ax_a)
        push_line([0,-400,0], [0,400,0], C_TITANIUM, 4, ax_a)

    # 4. PHASE 2: LIMIT SEQUENCE (Proving CLOSED)
    # -------------------------------------------
    target_x, target_y = 180, 120
    target_z = MX*target_x + MY*target_y
    target_pt = [target_x, target_y, target_z]

    if t > T_PH1_END:
        prg = np.clip((t - T_PH1_END) / (T_SEQ_END - T_PH1_END), 0.0, 1.0)
        
        # Spiral decay equations mathematically targeting the limit
        r_path = 400 * (1.0 - ease_in_out(prg)) * np.exp(-1.5 * prg)
        theta_path = prg * 4 * np.pi
        
        curr_x = target_x + r_path * np.cos(theta_path)
        curr_y = target_y + r_path * np.sin(theta_path)
        curr_z = MX*curr_x + MY*curr_y
        curr_pt = [curr_x, curr_y, curr_z]
        
        # Draw target ring
        push_point(target_pt, C_GOLD, 150, 0.8, ec=C_TEXT, lw=3, force_z=20)
        
        # Draw Trailing Path (The Sequence (x_n, Tx_n))
        trail_pts = []
        for back_p in np.linspace(0, prg, int(prg*60)+1):
            r_b = 400 * (1.0 - ease_in_out(back_p)) * np.exp(-1.5 * back_p)
            t_b = back_p * 4 * np.pi
            c_x = target_x + r_b * np.cos(t_b)
            c_y = target_y + r_b * np.sin(t_b)
            c_z = MX*c_x + MY*c_y
            trail_pts.append([c_x, c_y, c_z])
            
        for i in range(len(trail_pts)-1):
            fade_a = np.clip(i / len(trail_pts), 0.0, 1.0) * 0.8
            push_line(trail_pts[i], trail_pts[i+1], C_MAGENTA, 6, fade_a, force_z=5)

        # Draw Current Particle and Plumb Lines
        if prg < 1.0:
            push_line([curr_x, curr_y, curr_z], [curr_x, curr_y, -400], C_STEEL, 2, 0.5) # Drop to floor (Domain)
            push_line([curr_x, curr_y, curr_z], [0, 0, curr_z], C_STEEL, 2, 0.5)         # Drop to Z-axis (Range)
            push_point(curr_pt, C_CYAN, 80, 1.0, ec=C_TEXT, lw=2, force_z=25)
        else:
            # Impact Frame
            push_point(target_pt, C_MANTIS, 300, 1.0, ec=C_CYAN, lw=4, force_z=30)
            
    # 5. PHASE 3: THE THEOREM LOCK (Proving BOUNDED)
    # ----------------------------------------------
    if t > T_SEQ_END:
        prg_lock = np.clip((t - T_SEQ_END) / 2.0, 0.0, 1.0)
        lock_a = ease_in_out(prg_lock)
        
        # The Bounding Box drops aggressively over the infinite topology
        # Proving the Z-axis (Range Norm) is dominated by the XY-radius (Domain Norm) M ||x||
        if lock_a > 0.01:
            push_to_queue(GEOM_BOX, 'none', C_MANTIS if lock_a > 0.9 else C_STEEL, 6.0, lock_a*0.6)

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

    ax.text(-500, 890, "LG-351c :: THE CLOSED GRAPH THEOREM", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] TOPOLOGICAL LIMITS // O(1) CONTINUITY BOUNDS", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    if t < T_PH1_END:
        s1, c1 = "PRODUCT MATRIX X × Y [CARTESIAN SPACE]", C_STEEL
        s2, c2 = "GRAPH OF OPERATOR Γ(T) ESTABLISHED", C_CYAN
        t_state = "AWAITING LIMIT SEQUENCE TOPOLOGY"
    elif t < T_SEQ_END:
        s1, c1 = "TOPOLOGICAL PROOF: CLOSED SET", C_MAGENTA
        s2, c2 = "SEQUENCE x_n CONVERGES TO x", C_CYAN
        t_state = "TRACKING TUPLE SEQUENCE (x_n, Tx_n) TO TARGET"
    else:
        s1, c1 = "LIMIT TARGET HIT // Γ(T) IS CLOSED", C_GOLD
        s2, c2 = "O(1) BOUNDING MULTIPLIER VERIFIED", C_STEEL
        t_state = "THEOREM LOCK: OPERATOR IS STRICTLY CONTINUOUS"

    ax.text(-500, -760, "SYS_01 [GEOMETRIC STATE]     :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, s1, color=c1, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [DATA INGESTION]      :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, s2, color=c2, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "STRUCTURAL LOAD AUDIT        :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, t_state, color=C_MANTIS if t >= T_SEQ_END else C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=C_CYAN, zorder=83))

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
    print(f"LG-351c: CLOSED GRAPH THEOREM [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
