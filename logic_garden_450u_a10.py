"""
PROJECT: Logic Garden 450u (Exact Physical Construct // A-10 Thunderbolt II Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: A-10, WARTHOG, THUNDERBOLT II, AEROSPACE, WIREFRAME, ENGINEERING, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: H-Tail dual vertical stabilisers, straight dihedral wings, high-mount engine nacelles, offset front gear.
- Strict Bounds Protocol: Core locked at origin. cam_span scaled to 12.0 for flawless, unclipped 100% full-body framing.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from absolute 115-degree dramatic front-quarter angle.
- Daylight Palette (White Substrate / High-Contrast Edge Geometry).
- Purged Jargon. Australian spelling conventions (maths, colour, kilometres, aeroplane, synchronisation).
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
OUT_DIR = "frames_450u_a10"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Baseplate Reference)

C_HULL_MAIN = '#94A3B8'          # Heavy Slate (Primary Armored Skin)
C_HULL_DARK = '#475569'          # Machined Slate (Wing Pods, Struts, Tail Masts)
C_DETAILS   = '#1E293B'          # Carbon Slate (Landing Gear, Structural Pylons)
C_COCKPIT   = '#005599'          # Deep Marine (Bubble Canopy Glazing)
C_ENGINE    = '#111115'          # Indestructible Black (TF34 Nacelles, GAU-8 Barrel Matrix)
C_ACCENT    = '#E11D48'          # Kinematic Red (Intake Fans / Danger Markings)

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
# GEOMETRIC PRIMITIVES
# ------------------------------------------------------------------
def add_quad_mesh(lines_dict, col, p1, p2, p3, p4, u_steps=4, v_steps=4):
    p1, p2, p3, p4 = map(np.array, (p1, p2, p3, p4))
    for i in range(v_steps + 1):
        v = i / v_steps
        start = p1 * (1-v) + p4 * v
        end   = p2 * (1-v) + p3 * v
        pts = [start * (1-u) + end * u for u in np.linspace(0, 1, u_steps+1)]
        append_segmented(lines_dict, col, [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts])
    for i in range(u_steps + 1):
        u = i / u_steps
        start = p1 * (1-u) + p2 * u
        end   = p4 * (1-u) + p3 * u
        pts = [start * (1-v) + end * v for v in np.linspace(0, 1, v_steps+1)]
        append_segmented(lines_dict, col, [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts])

def add_sym_quad(lines_dict, col, p1, p2, p3, p4, u_steps=4, v_steps=4):
    add_quad_mesh(lines_dict, col, p1, p2, p3, p4, u_steps, v_steps)
    if any(abs(p[1]) > 0.001 for p in [p1, p2, p3, p4]):
        add_quad_mesh(lines_dict, col, (p1[0], -p1[1], p1[2]), (p2[0], -p2[1], p2[2]), 
                                       (p3[0], -p3[1], p3[2]), (p4[0], -p4[1], p4[2]), u_steps, v_steps)

def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='x', rings=4, t_count=16):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, length, rings)
    for s in steps:
        if axis == 'x':  ix, iy, iz = np.full_like(t, cx + s), cy + radius*np.cos(t), cz + radius*np.sin(t)
        elif axis == 'y': ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + s), cz + radius*np.sin(t)
        else:             ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), np.full_like(t, cz + s)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        if axis == 'x':   sx, sy, sz = cx + steps, [cy + radius*np.cos(a)]*rings, [cz + radius*np.sin(a)]*rings
        elif axis == 'y': sx, sy, sz = [cx + radius*np.cos(a)]*rings, cy + steps, [cz + radius*np.sin(a)]*rings
        else:             sx, sy, sz = [cx + radius*np.cos(a)]*rings, [cy + radius*np.sin(a)]*rings, cz + steps
        append_segmented(lines_dict, col, sx, sy, sz)


# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (A-10 WARTHOG)
# ------------------------------------------------------------------
def generate_a10_static():
    lines = {
        'C_HULL_MAIN': [], 'C_HULL_DARK': [], 'C_DETAILS': [], 
        'C_COCKPIT': [], 'C_ENGINE': [], 'C_ACCENT': [], 'C_GRID': []
    }

    # 1. BASEPLATE ENVELOPE (REFERENCE GRID)
    Z_FLOOR = -2.5
    gx_range = np.linspace(-12.0, 12.0, 17)
    gy_range = np.linspace(-10.0, 10.0, 13)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. TUBULAR FUSELAGE LOFTING
    # ==============================================================================
    x_st = [8.0, 7.0, 5.5, 3.5, 1.0, -1.0, -3.0, -5.0, -7.0, -8.5]
    ry_st = [0.1, 0.5, 0.8, 0.95, 1.0, 1.0, 0.9, 0.7, 0.4, 0.1]
    rz_st = [0.1, 0.55, 0.9, 1.1, 1.2, 1.2, 1.1, 0.8, 0.5, 0.2]
    z_off = [0.0, -0.1, 0.0, 0.1, 0.1, 0.1, 0.2, 0.3, 0.5, 0.6]

    for i in range(len(x_st)-1):
        x1, x2 = x_st[i], x_st[i+1]
        ry1, ry2 = ry_st[i], ry_st[i+1]
        rz1, rz2 = rz_st[i], rz_st[i+1]
        zo1, zo2 = z_off[i], z_off[i+1]
        
        t = np.linspace(0, 2*np.pi, 20, endpoint=False)
        y1_ring, z1_ring = ry1*np.cos(t), rz1*np.sin(t) + zo1
        y2_ring, z2_ring = ry2*np.cos(t), rz2*np.sin(t) + zo2
        
        col = 'C_HULL_MAIN' if i % 2 == 0 else 'C_HULL_DARK'
        
        append_segmented(lines, col, [x1]*21, list(y1_ring)+[y1_ring[0]], list(z1_ring)+[z1_ring[0]])
        for k in range(20):
            append_segmented(lines, 'C_HULL_MAIN', [x1, x2], [y1_ring[k], y2_ring[k]], [z1_ring[k], z2_ring[k]])

    # ==============================================================================
    # 3. HIGH-VISIBILITY BUBBLE CANOPY
    # ==============================================================================
    p_c_front = (6.0, 0.0, 0.8); p_c_top = (5.0, 0.0, 1.8); p_c_rear = (3.0, 0.0, 1.2)
    p_s_front = (5.5, 0.5, 0.6); p_s_mid = (4.5, 0.7, 1.0); p_s_rear = (3.5, 0.6, 0.9)

    add_sym_quad(lines, 'C_COCKPIT', p_c_front, p_s_front, p_s_mid, p_c_top, u_steps=4, v_steps=4)
    add_sym_quad(lines, 'C_COCKPIT', p_c_top, p_s_mid, p_s_rear, p_c_rear, u_steps=4, v_steps=4)

    # ==============================================================================
    # 4. ROTARY CANNON (GAU-8 AVENGER)
    # ==============================================================================
    # Core cannon cylinder extending explicitly from the nose bounds
    add_cylinder(lines, 'C_ENGINE', cx=7.5, cy=0.0, cz=-0.5, length=1.2, radius=0.15, axis='x', rings=3, t_count=8)

    # ==============================================================================
    # 5. HIGH-MOUNT TF34 ENGINE NACELLES
    # ==============================================================================
    # Mounted strictly atop the rear chassis, spaced laterally
    for y_sign in [-1, 1]:
        ey = 1.35 * y_sign
        ex = -4.5
        ez = 1.2
        er = 0.75
        el = 2.8
        
        # Primary Cowling
        add_cylinder(lines, 'C_HULL_MAIN', cx=ex, cy=ey, cz=ez, length=el, radius=er, axis='x', rings=6, t_count=16)
        # Inner Exhaust
        add_cylinder(lines, 'C_ENGINE', cx=ex-0.2, cy=ey, cz=ez, length=0.4, radius=er*0.8, axis='x', rings=2, t_count=12)
        # Heavy Structural Pylon anchoring nacelle to central fuselage
        add_quad_mesh(lines, 'C_DETAILS', (ex+2.0, 0.5*y_sign, 0.8), (ex, 0.5*y_sign, 0.8), 
                                          (ex, ey, ez), (ex+1.5, ey, ez), u_steps=2, v_steps=2)

    # ==============================================================================
    # 6. STRAIGHT WINGS WITH DIHEDRAL & LANDING GEAR PODS
    # ==============================================================================
    W_ROOT_X_FWD = 2.5; W_ROOT_X_AFT = -0.5
    W_TIP_X_FWD = 1.5; W_TIP_X_AFT = -0.5
    W_SPAN = 8.75
    W_Z_ROOT = -0.2
    W_Z_TIP = 0.5 # Substantial dihedral

    # Starboard Wing
    add_sym_quad(lines, 'C_HULL_MAIN', (W_ROOT_X_FWD, 1.0, W_Z_ROOT), (W_ROOT_X_AFT, 1.0, W_Z_ROOT), 
                                       (W_TIP_X_AFT, W_SPAN, W_Z_TIP), (W_TIP_X_FWD, W_SPAN, W_Z_TIP), u_steps=6, v_steps=6)
    
    # Wing Sponsons (Landing Gear Pods at Y=+/- 2.6)
    for y_sign in [-1, 1]:
        sy = 2.6 * y_sign
        sz = -0.1
        add_cylinder(lines, 'C_HULL_DARK', cx=-0.5, cy=sy, cz=sz, length=3.0, radius=0.4, axis='x', rings=5, t_count=12)

    # ==============================================================================
    # 7. H-TAIL EMPENNAGE
    # ==============================================================================
    # Massive transverse horizontal stabiliser
    add_sym_quad(lines, 'C_HULL_MAIN', (-7.0, 0.0, 0.8), (-8.5, 0.0, 0.8), (-8.5, 3.1, 0.8), (-7.5, 3.1, 0.8), u_steps=2, v_steps=6)
    
    # Twin Vertical Stabilisers mounted to the absolute tips
    add_sym_quad(lines, 'C_DETAILS', (-7.0, 3.1, 0.0), (-8.8, 3.1, 0.0), (-8.8, 3.1, 2.5), (-7.5, 3.1, 2.5), u_steps=3, v_steps=3)
    add_sym_quad(lines, 'C_DETAILS', (-7.0, 3.15, 0.0), (-8.8, 3.15, 0.0), (-8.8, 3.15, 2.5), (-7.5, 3.15, 2.5), u_steps=3, v_steps=3)

    # ==============================================================================
    # 8. DEPLOYED TRICYCLE LANDING GEAR
    # ==============================================================================
    # Nose Gear Assembly (Offset to starboard slightly to clear GAU-8)
    append_segmented(lines, 'C_DETAILS', [6.5, 6.5], [-0.3, -0.3], [-0.5, Z_FLOOR])
    add_cylinder(lines, 'C_DETAILS', cx=6.5, cy=-0.4, cz=Z_FLOOR+0.3, length=0.2, radius=0.3, axis='y', rings=2)

    # Main Gear Assembly (Dropping explicitly from the wing pods)
    append_sym(lines, 'C_DETAILS', [0.5, 0.5], [2.6, 2.6], [-0.5, Z_FLOOR])
    for y_sign in [-1, 1]:
        add_cylinder(lines, 'C_DETAILS', cx=0.5, cy=2.5*y_sign, cz=Z_FLOOR+0.45, length=0.4, radius=0.45, axis='y', rings=3)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_a10_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking the geometric True Center of the 16.2m airframe
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.0
        
        # Starts explicitly from 115-degrees (Dramatic front-quarter aesthetic)
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
    # Anchor = 0.0. Total vessel length is 16.2m. Wingspan 17.5m.
    # Setting cam_span safely wide to 12.0 to yield 24.0m horizontal footprint.
    # Vertical bounds output 12.0 * 1.777 = 21.32m (x2 = 42.6m height allowed).
    # Perfectly frames the wide, predatory stance without intersecting HUD logic.
    cam_span = 12.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_HULL_MAIN', C_HULL_MAIN, 1.2, 1.0),
        ('C_HULL_DARK', C_HULL_DARK, 1.4, 1.0),
        ('C_DETAILS',   C_DETAILS,   1.3, 1.0),
        ('C_COCKPIT',   C_COCKPIT,   1.8, 1.0),
        ('C_ENGINE',    C_ENGINE,    1.6, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +14 degrees to cleanly isolate the wide straight wings and high-mount engines
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-450u // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // A-10 THUNDERBOLT II MATRIX", color=C_HULL_DARK, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_COCKPIT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: H-TAIL EMPENNAGE / HIGH-MOUNT NACELLES", color=C_DETAILS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-450u: A-10 WARTHOG KINEMATICS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
