"""
PROJECT: Logic Garden 451h (Exact Physical Construct // Human Figure Proportions Matrix) - HOTFIX
FORMAT: YouTube Shorts (1080x1920)
METADATA: HUMAN PROPORTIONS, ANATOMY, WIREFRAME, KINEMATICS, DRAWING ANGLES, VITRUVIAN
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: 8-Head division grid, accurate biomechanical joints, Vitruvian bounding arrays.
- Custom Kinematic Nodes: Patched add_strut handles explicit 1D scalar expansion over 3D directional vectors.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from absolute 115-degree front-quarter baseline.
- Daylight Palette (White Substrate / High-Contrast Edge Geometry).
- Purged Jargon. Australian spelling conventions (maths, colour, kilometres, synchronisation).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import multiprocessing as mp
import os
import gc

# ======== SEQUENCE PARAMETERS ========
DURATION = 24.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_451h_mannequin"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Reference Planes & Vitruvian bounds)

C_HULL_MAIN = '#94A3B8'          # Heavy Slate (Skeletal Struts, Thorax, Core Mass)
C_HULL_DARK = '#475569'          # Machined Slate (Articulating Joint Spheres)
C_DETAILS   = '#1E293B'          # Carbon Slate (Extremities, Clavicle lines)
C_ACCENT    = '#E11D48'          # Kinematic Red (Center of Gravity, 8-Head Division Nodes)

# ------------------------------------------------------------------
# O(N) KINEMATIC WIREFRAME ENGINE
# ------------------------------------------------------------------
def project_3d_depth(x, y, z, cx, cy, cz, az_deg, el_deg=0):
    tx, ty, tz = x - cx, y - cy, z - cz
    az, el = np.radians(az_deg), np.radians(el_deg)
    
    x1 = tx * np.cos(az) - ty * np.sin(az)
    y1 = tx * np.sin(az) + ty * np.cos(az)
    z1 = tz
    
    y2 = y1 * np.cos(el) - z1 * np.sin(el)
    z2 = y1 * np.sin(el) + z1 * np.cos(el)
    
    return x1, z2, y2 

def append_segmented(lines_dict, key, xs, ys, zs):
    xs, ys, zs = list(xs), list(ys), list(zs)
    for i in range(len(xs) - 1):
        lines_dict[key].append(([xs[i], xs[i+1]], [ys[i], ys[i+1]], [zs[i], zs[i+1]]))

def append_sym(lines_dict, key, xs, ys, zs):
    append_segmented(lines_dict, key, xs, ys, zs)
    if any(abs(y) > 0.001 for y in ys):
        append_segmented(lines_dict, key, xs, [-y for y in ys], zs)

# ------------------------------------------------------------------
# GEOMETRIC PRIMITIVES (BIOMECHANICAL TARGETING)
# ------------------------------------------------------------------
def add_sphere(lines_dict, col, cx, cy, cz, radius, rings=5, t_count=12):
    # Latitudinal topological rings
    for p in np.linspace(-np.pi/2, np.pi/2, rings):
        r_s = radius * np.cos(p)
        z_s = radius * np.sin(p)
        t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
        ix = cx + r_s*np.cos(t); iy = cy + r_s*np.sin(t); iz = np.full_like(t, cz + z_s)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    # Longitudinal topological arcs
    for a in np.linspace(0, np.pi, t_count//2, endpoint=False):
        p = np.linspace(-np.pi/2, np.pi/2, rings*2)
        r_s = radius * np.cos(p)
        ix = cx + r_s*np.cos(a); iy = cy + r_s*np.sin(a); iz = cz + radius*np.sin(p)
        append_segmented(lines_dict, col, list(ix), list(iy), list(iz))

def add_sym_sphere(lines_dict, col, cx, cy, cz, radius, rings=5, t_count=12):
    add_sphere(lines_dict, col, cx, cy, cz, radius, rings, t_count)
    if abs(cy) > 0.001:
        add_sphere(lines_dict, col, cx, -cy, cz, radius, rings, t_count)

def add_ellipsoid(lines_dict, col, cx, cy, cz, rx, ry, rz, rings=6, t_count=16):
    for p in np.linspace(-np.pi/2, np.pi/2, rings):
        r_x = rx * np.cos(p); r_y = ry * np.cos(p); z_s = rz * np.sin(p)
        t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
        ix = cx + r_x*np.cos(t); iy = cy + r_y*np.sin(t); iz = np.full_like(t, cz + z_s)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, np.pi, t_count//2, endpoint=False):
        p = np.linspace(-np.pi/2, np.pi/2, rings*2)
        c_p = np.cos(p); s_p = np.sin(p)
        ix = cx + rx * c_p * np.cos(a); iy = cy + ry * c_p * np.sin(a); iz = cz + rz * s_p
        append_segmented(lines_dict, col, list(ix), list(iy), list(iz))

def add_strut(lines_dict, col, p1, p2, radius, rings=3, t_count=8):
    # Absolute mathematical link plotting an explicitly capped cylinder between two irregular 3D vectors
    p1, p2 = np.array(p1), np.array(p2)
    v = p2 - p1
    length = np.linalg.norm(v)
    if length < 0.001: return
    v_dir = v / length
    not_v = np.array([1.0, 0.0, 0.0])
    if abs(np.dot(v_dir, not_v)) > 0.99: not_v = np.array([0.0, 1.0, 0.0])
    n1 = np.cross(v_dir, not_v)
    n1 /= np.linalg.norm(n1)
    n2 = np.cross(v_dir, n1)
    
    steps = np.linspace(0, length, rings)
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    
    # Circumferential arrays 
    for s in steps:
        center = p1 + v_dir * s
        ix = center[0] + radius * (np.cos(t)*n1[0] + np.sin(t)*n2[0])
        iy = center[1] + radius * (np.cos(t)*n1[1] + np.sin(t)*n2[1])
        iz = center[2] + radius * (np.cos(t)*n1[2] + np.sin(t)*n2[2])
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    
    # Longitudinal linking struts (HOTFIX: Explicitly isolate v_dir channels to broadcast properly)
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        nx = radius * (np.cos(a)*n1[0] + np.sin(a)*n2[0])
        ny = radius * (np.cos(a)*n1[1] + np.sin(a)*n2[1])
        nz = radius * (np.cos(a)*n1[2] + np.sin(a)*n2[2])
        sx = p1[0] + nx + v_dir[0] * steps
        sy = p1[1] + ny + v_dir[1] * steps
        sz = p1[2] + nz + v_dir[2] * steps
        append_segmented(lines_dict, col, list(sx), list(sy), list(sz))

def add_sym_strut(lines_dict, col, p1, p2, radius, rings=3, t_count=8):
    add_strut(lines_dict, col, p1, p2, radius, rings, t_count)
    if abs(p1[1]) > 0.001 or abs(p2[1]) > 0.001:
        sp1 = (p1[0], -p1[1], p1[2])
        sp2 = (p2[0], -p2[1], p2[2])
        add_strut(lines_dict, col, sp1, sp2, radius, rings, t_count)


# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (ARTISTIC & BIOMECHANICAL MANNEQUIN)
# ------------------------------------------------------------------
def generate_mannequin_static():
    lines = {
        'C_HULL_MAIN': [], 'C_HULL_DARK': [], 'C_DETAILS': [], 
        'C_ACCENT': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. VITRUVIAN BOUNDING GEOMETRY & ARCHITECTURAL GRID
    # ==============================================================================
    # Core mathematical threshold: Standard human is 1.8 metres tall (8 head proportions)
    H_DIV = 1.8 / 8.0  # 0.225m
    
    # Primary Floor Pedestal
    for r_p in [0.8, 0.9]:
        t_p = np.linspace(0, 2*np.pi, 32, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, 0.0))

    # Classical Vitruvian Proportions Grid (Squaring the Circle)
    SQ_H = 1.8; SQ_W = 0.9 
    append_segmented(lines, 'C_GRID', [0, 0], [-SQ_W, SQ_W], [0, 0])
    append_segmented(lines, 'C_GRID', [0, 0], [-SQ_W, SQ_W], [SQ_H, SQ_H])
    append_segmented(lines, 'C_GRID', [0, 0], [-SQ_W, -SQ_W], [0, SQ_H])
    append_segmented(lines, 'C_GRID', [0, 0], [SQ_W, SQ_W], [0, SQ_H])
    
    # The Circle centers on exactly the true navel baseline (Z = 1.125m) reaching the floor
    C_CX = 0.0; C_CY = 0.0; C_CZ = 1.125
    C_R = 1.125
    t_c = np.linspace(0, 2*np.pi, 64, endpoint=False)
    append_segmented(lines, 'C_GRID', np.full_like(t_c, 0.0), C_CY + C_R*np.cos(t_c), C_CZ + C_R*np.sin(t_c))

    # 8-Head Proportion Cut-Lines (Architectural Backdrop at X = -0.3)
    for i in range(9):
        z_h = i * H_DIV
        append_segmented(lines, 'C_GRID', [-0.3, -0.3], [-0.5, 0.5], [z_h, z_h])
        append_segmented(lines, 'C_ACCENT', [-0.3, 0.0], [0.5, 0.5], [z_h, z_h])
        append_segmented(lines, 'C_ACCENT', [-0.3, 0.0], [-0.5, -0.5], [z_h, z_h])

    # Absolute Center of Gravity Plumb Line
    append_segmented(lines, 'C_ACCENT', [0, 0], [0, 0], [0, 1.9])

    # ==============================================================================
    # 2. CORE BIOMECHANICAL MASSES (Head, Thorax, Pelvis)
    # ==============================================================================
    # Cranium Array (Fits flawlessly within the top 0.225m zone Z=1.575 to 1.8)
    add_ellipsoid(lines, 'C_HULL_MAIN', cx=0.0, cy=0.0, cz=1.6875, rx=0.10, ry=0.08, rz=0.11, rings=6, t_count=16)
    
    # Thorax / Ribcage (Aggressive trapezoidal egg scaling Z=1.125 to 1.5)
    add_ellipsoid(lines, 'C_HULL_MAIN', cx=0.0, cy=0.0, cz=1.33, rx=0.12, ry=0.16, rz=0.16, rings=6, t_count=16)
    
    # Pelvic Girdle (Anchored strictly Z=0.9 to 1.1)
    add_ellipsoid(lines, 'C_HULL_MAIN', cx=0.0, cy=0.0, cz=1.02, rx=0.11, ry=0.14, rz=0.10, rings=6, t_count=16)

    # Core Spinal and Clavicle Struts connecting the loose masses
    add_strut(lines, 'C_DETAILS', (0.0, 0.0, 1.12), (0.0, 0.0, 1.5), radius=0.03, rings=4) # Spine
    add_sym_strut(lines, 'C_DETAILS', (0.0, 0.0, 1.48), (0.0, 0.22, 1.45), radius=0.02, rings=2) # Clavicle

    # ==============================================================================
    # 3. ARTICULATING JOINTS (Spherical Pivot Nodes)
    # ==============================================================================
    # True biomechanical coordinates enforcing visual aesthetic realism
    J_NECK  = (0.0,  0.0,   1.5)
    J_SH    = (0.0,  0.22,  1.45)
    J_ELBOW = (0.0,  0.28,  1.15)
    J_WRIST = (0.05, 0.32,  0.85)
    J_HIP   = (0.0,  0.13,  0.92)
    J_KNEE  = (0.02, 0.14,  0.46)
    J_ANKLE = (0.0,  0.14,  0.10)
    
    add_sphere(lines, 'C_HULL_DARK', *J_NECK, 0.04)
    add_sym_sphere(lines, 'C_HULL_DARK', *J_SH, 0.045)
    add_sym_sphere(lines, 'C_HULL_DARK', *J_ELBOW, 0.035)
    add_sym_sphere(lines, 'C_HULL_DARK', *J_WRIST, 0.025)
    add_sym_sphere(lines, 'C_HULL_DARK', *J_HIP, 0.045)
    add_sym_sphere(lines, 'C_HULL_DARK', *J_KNEE, 0.040)
    add_sym_sphere(lines, 'C_HULL_DARK', *J_ANKLE, 0.030)

    # ==============================================================================
    # 4. EXTREMITIES & SKELETAL STRUTS
    # ==============================================================================
    # Arm Linkages
    add_sym_strut(lines, 'C_HULL_MAIN', J_SH, J_ELBOW, radius=0.04, rings=4)
    add_sym_strut(lines, 'C_HULL_MAIN', J_ELBOW, J_WRIST, radius=0.035, rings=4)
    add_sym_strut(lines, 'C_DETAILS', J_WRIST, (0.08, 0.34, 0.65), radius=0.03, rings=3) # Hands

    # Leg Linkages
    add_sym_strut(lines, 'C_HULL_MAIN', J_HIP, J_KNEE, radius=0.055, rings=4)
    add_sym_strut(lines, 'C_HULL_MAIN', J_KNEE, J_ANKLE, radius=0.045, rings=4)
    # Foot Platform (Planted aggressively onto the X/Y sub-grid plane)
    add_sym_strut(lines, 'C_DETAILS', J_ANKLE, (0.15, 0.16, 0.02), radius=0.03, rings=3) # Forefoot
    add_sym_strut(lines, 'C_DETAILS', J_ANKLE, (-0.05, 0.13, 0.02), radius=0.025, rings=2) # Heel Anchor

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_mannequin_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry strictly to the core biological centroid
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.9
        
        # Starts explicitly from 115-degrees
        azimuth = 115.0 - (stage * 360.0)

        yield (f, t_sec, azimuth, cam_x, cam_y, cam_z, static_rig)

def render_frame(packet):
    f, t_sec, azimuth, cx, cy, cz, static_rig = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # 100% VISIBILITY THRESHOLD AUDIT:
    cam_span = 0.75
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.6, 0.4), 
        ('C_ACCENT',    C_ACCENT,    1.5, 0.8),
        ('C_HULL_MAIN', C_HULL_MAIN, 1.2, 1.0),
        ('C_HULL_DARK', C_HULL_DARK, 1.3, 1.0),
        ('C_DETAILS',   C_DETAILS,   1.2, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +14 degrees to dynamically slice through the grid-bounded anatomical nodes
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=14.0)
            render_queue.append((np.mean(depth), u, v, c_val, lw, alpha))

    # ABSOLUTE Z-SORT 
    render_queue.sort(key=lambda item: item[0], reverse=True)
    for depth, u, v, c, lw, a in render_queue:
        ax.plot(u, v, color=c, lw=lw, alpha=a)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (TOP HUD)
    # ------------------------------------------------------------------
    ui_t = cam_span * 1.45
    ax.add_patch(patches.Rectangle((-cam_span, ui_t), cam_span*2, cam_span*0.5, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_t, ui_t], color=C_TEXT, lw=6, zorder=81)

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-451h_HF // MACRO-ENGINEERING TENSOR: BIOMECHANICAL KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // HUMAN PROPORTIONS (VITRUVIAN MATRIX)", color=C_ACCENT, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_HULL_DARK, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: 8-HEAD ARTICULATED NODES / CLASSICAL STRUCTURAL BOUNDS", color=C_DETAILS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-451h_HF: BIOMECHANICAL KINEMATICS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Biomechanical Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
