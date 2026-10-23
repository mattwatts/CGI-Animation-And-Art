"""
PROJECT: Logic Garden 451t (Exact Physical Construct // Mercury Spacesuit Matrix) - HOTFIX
FORMAT: YouTube Shorts (1080x1920)
METADATA: MERCURY, SPACESUIT, PROJECT MERCURY, NASA, WIREFRAME, ENGINEERING, KINEMATICS, AEROSPACE
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional 1.85m aerospace scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: B.F. Goodrich Mark IV profile, rigid neck ring, umbilical manifold, ribbed pressure folds.
- Hotfix Integration: Bilateral symmetry hook 'add_sym_sphere' injected for exact mirror rendering.
- High-Contrast Override: Primary geometries darkened aggressively to guarantee absolute optical clarity against daylight substrate.
- Viewport Override: Locked cam_span guarantees 100% total vehicle visibility between UI boundaries.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from 115-degree dramatic front-quarter angle.
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
OUT_DIR = "frames_451t_mercury_suit"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Reference Baseplate)

C_SUIT      = '#334155'          # Heavy Slate (Aluminised Nylon Fabric)
C_HELMET    = '#0F172A'          # Abyssal Slate (Rigid Fiberglass Shell)
C_VISOR     = '#111115'          # Indestructible Black (Plexiglass Viewport)
C_HARDWARE  = '#E11D48'          # Kinematic Red (Umbilical Inlets, Communication Harness)
C_DETAILS   = '#475569'          # Machined Slate (Locking Collar, Boots, Gloves)

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

# ------------------------------------------------------------------
# GEOMETRIC PRIMITIVES
# ------------------------------------------------------------------
def add_box(lines_dict, col, cx, cy, cz, dx, dy, dz):
    hx, hy, hz = dx/2, dy/2, dz/2
    xs = [cx-hx, cx+hx, cx+hx, cx-hx, cx-hx]
    ys1 = [cy-hy, cy-hy, cy+hy, cy+hy, cy-hy]
    ys2 = [cy-hy, cy-hy, cy+hy, cy+hy, cy-hy]
    append_segmented(lines_dict, col, xs, ys1, [cz-hz]*5)
    append_segmented(lines_dict, col, xs, ys2, [cz+hz]*5)
    for i in range(4):
        append_segmented(lines_dict, col, [xs[i], xs[i]], [ys1[i], ys1[i]], [cz-hz, cz+hz])

def add_sym_box(lines_dict, col, cx, cy, cz, dx, dy, dz):
    add_box(lines_dict, col, cx, cy, cz, dx, dy, dz)
    if abs(cy) > 0.001:
        add_box(lines_dict, col, cx, -cy, cz, dx, dy, dz)

def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='z', rings=4, t_count=16):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, length, rings)
    for s in steps:
        if axis == 'z':
            ix = cx + radius*np.cos(t); iy = cy + radius*np.sin(t); iz = np.full_like(t, cz + s)
        elif axis == 'y':
            ix = cx + radius*np.cos(t); iy = np.full_like(t, cy + s); iz = cz + radius*np.sin(t)
        elif axis == 'x':
            ix = np.full_like(t, cx + s); iy = cy + radius*np.cos(t); iz = cz + radius*np.sin(t)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        if axis == 'z':
            sx = np.full_like(steps, cx + radius*np.cos(a))
            sy = np.full_like(steps, cy + radius*np.sin(a))
            sz = cz + steps
        elif axis == 'y':
            sx = np.full_like(steps, cx + radius*np.cos(a))
            sy = cy + steps
            sz = np.full_like(steps, cz + radius*np.sin(a))
        elif axis == 'x':
            sx = cx + steps
            sy = np.full_like(steps, cy + radius*np.cos(a))
            sz = np.full_like(steps, cz + radius*np.sin(a))
        append_segmented(lines_dict, col, list(sx), list(sy), list(sz))

def add_sphere(lines_dict, col, cx, cy, cz, radius, rings=8, t_count=16):
    for p in np.linspace(-np.pi/2, np.pi/2, rings):
        r_s = radius * np.cos(p)
        z_s = radius * np.sin(p)
        t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
        ix = cx + r_s*np.cos(t); iy = cy + r_s*np.sin(t); iz = np.full_like(t, cz + z_s)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, np.pi, t_count//2, endpoint=False):
        p = np.linspace(-np.pi/2, np.pi/2, rings*2)
        r_s = radius * np.cos(p)
        ix = cx + r_s*np.cos(a); iy = cy + r_s*np.sin(a); iz = cz + radius*np.sin(p)
        append_segmented(lines_dict, col, list(ix), list(iy), list(iz))

def add_sym_sphere(lines_dict, col, cx, cy, cz, radius, rings=8, t_count=16):
    add_sphere(lines_dict, col, cx, cy, cz, radius, rings, t_count)
    if abs(cy) > 0.001:
        add_sphere(lines_dict, col, cx, -cy, cz, radius, rings, t_count)

def add_ellipsoid(lines_dict, col, cx, cy, cz, rx, ry, rz, rings=8, t_count=16):
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

def add_sym_ellipsoid(lines_dict, col, cx, cy, cz, rx, ry, rz, rings=8, t_count=16):
    add_ellipsoid(lines_dict, col, cx, cy, cz, rx, ry, rz, rings, t_count)
    if abs(cy) > 0.001:
        add_ellipsoid(lines_dict, col, cx, -cy, cz, rx, ry, rz, rings, t_count)

def add_ribbed_strut(lines_dict, col, p1, p2, radius, rings=10, t_count=12, rib_freq=6.0, rib_depth=0.15):
    # Specialized primitive generating mathematically inflated pressure folds natively inside the tube vector
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
    
    for s in steps:
        r_mod = radius * (1.0 + rib_depth * np.cos((s / length) * rib_freq * 2 * np.pi))
        center = p1 + v_dir * s
        ix = center[0] + r_mod * (np.cos(t)*n1[0] + np.sin(t)*n2[0])
        iy = center[1] + r_mod * (np.cos(t)*n1[1] + np.sin(t)*n2[1])
        iz = center[2] + r_mod * (np.cos(t)*n1[2] + np.sin(t)*n2[2])
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        sx, sy, sz = [], [], []
        for s in steps:
            r_mod = radius * (1.0 + rib_depth * np.cos((s / length) * rib_freq * 2 * np.pi))
            nx = r_mod * (np.cos(a)*n1[0] + np.sin(a)*n2[0])
            ny = r_mod * (np.cos(a)*n1[1] + np.sin(a)*n2[1])
            nz = r_mod * (np.cos(a)*n1[2] + np.sin(a)*n2[2])
            sx.append(p1[0] + nx + v_dir[0] * s)
            sy.append(p1[1] + ny + v_dir[1] * s)
            sz.append(p1[2] + nz + v_dir[2] * s)
        append_segmented(lines_dict, col, sx, sy, sz)

def add_sym_ribbed_strut(lines_dict, col, p1, p2, radius, rings=10, t_count=12, rib_freq=6.0, rib_depth=0.15):
    add_ribbed_strut(lines_dict, col, p1, p2, radius, rings, t_count, rib_freq, rib_depth)
    if abs(p1[1]) > 0.001 or abs(p2[1]) > 0.001:
        sp1 = (p1[0], -p1[1], p1[2])
        sp2 = (p2[0], -p2[1], p2[2])
        add_ribbed_strut(lines_dict, col, sp1, sp2, radius, rings, t_count, rib_freq, rib_depth)


# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (MERCURY SPACESUIT)
# ------------------------------------------------------------------
def generate_mercury_static():
    lines = {
        'C_SUIT': [], 'C_HELMET': [], 'C_HARDWARE': [], 
        'C_VISOR': [], 'C_DETAILS': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. ORBITAL REFERENCE BASEPLATE
    # ==============================================================================
    Z_FLOOR = 0.0
    for r_p in [0.6, 0.9]:
        t_p = np.linspace(0, 2*np.pi, 48, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-1.2, 1.2, 13)
    gy_range = np.linspace(-1.2, 1.2, 13)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. HELMET & VISOR ASSEMBLY
    # ==============================================================================
    H_Z = 1.70
    # Primary Fiberglass Shell
    add_sphere(lines, 'C_HELMET', cx=0.0, cy=0.0, cz=H_Z, radius=0.12, rings=8, t_count=16)
    
    # Plexiglass Visor (Forward intersecting cut)
    add_ellipsoid(lines, 'C_VISOR', cx=0.07, cy=0.0, cz=H_Z+0.01, rx=0.10, ry=0.11, rz=0.09, rings=8, t_count=20)
    
    # Neck Locking Collar (Machined Slate)
    add_cylinder(lines, 'C_DETAILS', cx=0.0, cy=0.0, cz=H_Z-0.14, length=0.04, radius=0.11, axis='z', rings=2, t_count=20)

    # ==============================================================================
    # 3. TAILORED TORSO 
    # ==============================================================================
    # Close-fitting aluminized nylon upper body
    add_ellipsoid(lines, 'C_SUIT', cx=0.0, cy=0.0, cz=1.30, rx=0.11, ry=0.20, rz=0.26, rings=8, t_count=20)
    
    # Lower Torso Subsystem
    add_ellipsoid(lines, 'C_SUIT', cx=0.0, cy=0.0, cz=0.95, rx=0.12, ry=0.18, rz=0.15, rings=6, t_count=16)

    # ==============================================================================
    # 4. CHEST UMBILICAL MANIFOLD
    # ==============================================================================
    # Communication and Life Support inlets
    add_box(lines, 'C_HARDWARE', cx=0.11, cy=0.0, cz=1.20, dx=0.06, dy=0.12, dz=0.10)
    
    # Tethers dropping away from the suit
    add_cylinder(lines, 'C_HARDWARE', cx=0.13, cy=-0.04, cz=1.05, length=0.10, radius=0.02, axis='z', rings=2, t_count=8)
    add_cylinder(lines, 'C_HARDWARE', cx=0.13, cy=0.04, cz=1.05, length=0.10, radius=0.02, axis='z', rings=2, t_count=8)

    # ==============================================================================
    # 5. TAILORED ARMS (Kinematic Pressure Folds)
    # ==============================================================================
    SH_R = (0.0, -0.22, 1.45)
    ELBOW_R = (0.08, -0.24, 1.15)
    WRIST_R = (0.20, -0.22, 0.95)
    
    # Upper Arms (Bicep) - Tighter radius than modern EVA suits
    add_sym_ribbed_strut(lines, 'C_SUIT', SH_R, ELBOW_R, radius=0.06, rings=12, t_count=12, rib_freq=9.0, rib_depth=0.06)
    # Lower Arms (Forearm)
    add_sym_ribbed_strut(lines, 'C_SUIT', ELBOW_R, WRIST_R, radius=0.05, rings=12, t_count=12, rib_freq=11.0, rib_depth=0.06)
    
    # Locking Wrist Rings
    add_sym_sphere(lines, 'C_DETAILS', *WRIST_R, 0.04, rings=4, t_count=10) 
    
    # Lightweight Pressure Gloves
    add_sym_ellipsoid(lines, 'C_DETAILS', cx=0.25, cy=-0.21, cz=0.88, rx=0.05, ry=0.04, rz=0.07, rings=6, t_count=12) 

    # ==============================================================================
    # 6. TAILORED LEGS (Kinematic Pressure Folds)
    # ==============================================================================
    HIP_R = (0.0, -0.12, 0.90)
    KNEE_R = (0.05, -0.14, 0.50)
    ANKLE_R = (0.0, -0.12, 0.12)
    
    # Thighs
    add_sym_ribbed_strut(lines, 'C_SUIT', HIP_R, KNEE_R, radius=0.09, rings=16, t_count=16, rib_freq=12.0, rib_depth=0.05)
    # Calves
    add_sym_ribbed_strut(lines, 'C_SUIT', KNEE_R, ANKLE_R, radius=0.07, rings=16, t_count=16, rib_freq=14.0, rib_depth=0.05)

    # Leather-over-Nylon Boot Profile
    add_sym_box(lines, 'C_DETAILS', cx=0.05, cy=-0.12, cz=0.06, dx=0.18, dy=0.08, dz=0.12)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_mercury_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry precisely midway up the spacesuit bounds (Z=0.9m)
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.9
        
        # Starts explicitly from 115-degrees (Dramatic front-quarter aesthetic pushing depth)
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
    # Anchor Centroid = 0.9m high. Total vertical geometry spanning 0m to 1.85m precisely.
    # Setting cam_span strictly to 1.15 locks horizontal bounds seamlessly across 2.30m total.
    # Vertical bounds output 1.15 * 1.777 = 2.04m. (+/- 2.04m from 0.9m = -1.14m to +2.94m).
    # Asserts an uncompromising, flawlessly framed 1.85m profile cleanly avoiding both UI banners.
    cam_span = 1.15
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',     C_GRID,     1.0, 0.4), 
        ('C_SUIT',     C_SUIT,     1.3, 1.0),
        ('C_HELMET',   C_HELMET,   1.4, 1.0),
        ('C_DETAILS',  C_DETAILS,  1.3, 1.0),
        ('C_HARDWARE', C_HARDWARE, 1.5, 1.0),
        ('C_VISOR',    C_VISOR,    1.6, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +14 degrees to dynamically slice through the continuous suit volumes
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=14.0)
            render_queue.append((np.mean(depth), u, v, c_val, lw, alpha))

    # ABSOLUTE Z-SORT (Strict Painter's Algorithm Depth Culling)
    render_queue.sort(key=lambda item: item[0], reverse=True)
    for depth, u, v, c, lw, a in render_queue:
        ax.plot(u, v, color=c, lw=lw, alpha=a)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (TOP HUD)
    # ------------------------------------------------------------------
    ui_t = cam_span * 1.45
    ax.add_patch(patches.Rectangle((-cam_span, ui_t), cam_span*2, cam_span*0.5, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_t, ui_t], color=C_TEXT, lw=6, zorder=81)

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-451t_HF // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // MERCURY SPACESUIT MATRIX", color=C_SUIT, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_HARDWARE, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: MARK IV PROFILE / RIGID HELMET / CHEST UMBILICAl", color=C_DETAILS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-451t_HF: MERCURY SPACESUIT TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
