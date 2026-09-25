"""
PROJECT: Logic Garden 450o (Exact Physical Construct // Type-11 Workbee Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: STAR TREK, WORKBEE, ENTERPRISE, AEROSPACE, WIREFRAME, ENGINEERING, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Industrial faceted canopy, massive forward viewport, forward manipulator boom, spherical landing pads.
- Strict Bounds Protocol: Core locked at mid-body. cam_span scaled to 3.2 for flawless, unclipped 100% full-body framing.
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
OUT_DIR = "frames_450o_workbee"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Baseplate Reference)

C_HULL_MAIN = '#94A3B8'          # Heavy Slate (Primary Shuttle Hull Panels)
C_HULL_DARK = '#475569'          # Machined Slate (Underbelly, Thrust Pods)
C_DETAILS   = '#1E293B'          # Carbon Slate (Manipulator Arms, Structural Ribs)
C_COCKPIT   = '#111115'          # Indestructible Black (Massive Forward Windshield)
C_ACCENT    = '#FFB300'          # Dense Gold (Roof Beacon / Warning Optics)

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

def add_dome(lines_dict, col, cx, cy, cz, radius, axis='z', dir=1, rings=4, t_count=16):
    p_step = np.linspace(0, np.pi/2, rings)
    for p in p_step:
        r_s = radius * np.cos(p)
        h_s = radius * np.sin(p) * dir
        t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
        if axis == 'z':
            ix, iy, iz = cx + r_s*np.cos(t), cy + r_s*np.sin(t), np.full_like(t, cz + h_s)
            append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        rr = radius * np.cos(p_step)
        hh = radius * np.sin(p_step) * dir
        if axis == 'z':
            sx, sy, sz = cx + rr*np.cos(a), cy + rr*np.sin(a), cz + hh
            append_segmented(lines_dict, col, list(sx), list(sy), list(sz))

def add_sphere(lines_dict, col, cx, cy, cz, radius, t_count=16):
    add_dome(lines_dict, col, cx, cy, cz, radius, axis='z', dir=1, rings=5, t_count=t_count)
    add_dome(lines_dict, col, cx, cy, cz, radius, axis='z', dir=-1, rings=5, t_count=t_count)

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (TYPE-11 WORKBEE)
# ------------------------------------------------------------------
def generate_workbee_static():
    lines = {
        'C_HULL_MAIN': [], 'C_HULL_DARK': [], 'C_DETAILS': [], 
        'C_COCKPIT': [], 'C_ACCENT': [], 'C_GRID': []
    }

    # 1. BASEPLATE ENVELOPE (REFERENCE GRID)
    gx_range = np.linspace(-4.0, 4.0, 13)
    gy_range = np.linspace(-3.0, 3.0, 9)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, -0.4))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, -0.4))

    # ==============================================================================
    # 2. THE FACETED POLYGONAL CABIN
    # ==============================================================================
    X_REAR = -1.2; X_ROOF_FWD = 0.2
    X_NOSE = 1.6; X_BASE_FWD = 0.8
    Z_TOP = 1.2; Z_NOSE = 0.3; Z_BOT = 0.0
    Y_HW = 0.65  # Half width of main chassis

    # Roof Plane
    add_quad_mesh(lines, 'C_HULL_MAIN', (X_REAR, -Y_HW, Z_TOP), (X_ROOF_FWD, -Y_HW, Z_TOP), (X_ROOF_FWD, Y_HW, Z_TOP), (X_REAR, Y_HW, Z_TOP), u_steps=4, v_steps=4)
    # Floor Base Plane
    add_quad_mesh(lines, 'C_HULL_DARK', (X_REAR, -Y_HW, Z_BOT), (X_BASE_FWD, -Y_HW, Z_BOT), (X_BASE_FWD, Y_HW, Z_BOT), (X_REAR, Y_HW, Z_BOT), u_steps=4, v_steps=4)
    # Aft Engineering Plane (Back Wall)
    add_quad_mesh(lines, 'C_HULL_MAIN', (X_REAR, Y_HW, Z_TOP), (X_REAR, -Y_HW, Z_TOP), (X_REAR, -Y_HW, Z_BOT), (X_REAR, Y_HW, Z_BOT), u_steps=4, v_steps=3)
    # Forward Cockpit Viewport Base (Slanted)
    add_quad_mesh(lines, 'C_HULL_MAIN', (X_ROOF_FWD, -Y_HW, Z_TOP), (X_NOSE, -Y_HW, Z_NOSE), (X_NOSE, Y_HW, Z_NOSE), (X_ROOF_FWD, Y_HW, Z_TOP), u_steps=3, v_steps=4)
    # Nose-to-Base Cutback
    add_quad_mesh(lines, 'C_HULL_DARK', (X_NOSE, -Y_HW, Z_NOSE), (X_BASE_FWD, -Y_HW, Z_BOT), (X_BASE_FWD, Y_HW, Z_BOT), (X_NOSE, Y_HW, Z_NOSE), u_steps=1, v_steps=4)

    # Lateral Hull Facets
    for y_sign in [-1, 1]:
        y = Y_HW * y_sign
        # Main Rear/Mid body
        add_quad_mesh(lines, 'C_HULL_MAIN', (X_REAR, y, Z_TOP), (X_ROOF_FWD, y, Z_TOP), (X_ROOF_FWD, y, Z_BOT), (X_REAR, y, Z_BOT), u_steps=4, v_steps=3)
        # Forward Nose Wedge
        append_segmented(lines, 'C_HULL_MAIN', [X_ROOF_FWD, X_NOSE, X_BASE_FWD, X_ROOF_FWD], [y]*4, [Z_TOP, Z_NOSE, Z_BOT, Z_TOP])

    # ==============================================================================
    # 3. MASSIVE BLACKOUT WINDSHIELD
    # ==============================================================================
    # An extreme offset black plane perfectly tracing the forward slope geometry
    wx1 = X_ROOF_FWD + 0.15; wz1 = Z_TOP - 0.1
    wx2 = X_NOSE - 0.15; wz2 = Z_NOSE + 0.1
    wy = Y_HW - 0.1
    
    append_segmented(lines, 'C_COCKPIT', [wx1, wx2, wx2, wx1, wx1], 
                                         [-wy, -wy, wy, wy, -wy], 
                                         [wz1, wz2, wz2, wz1, wz1])
    # Massive internal window meshing
    add_quad_mesh(lines, 'C_COCKPIT', (wx1, -wy, wz1), (wx2, -wy, wz2), (wx2, wy, wz2), (wx1, wy, wz1), u_steps=8, v_steps=8)

    # ==============================================================================
    # 4. LATERAL DRIVE PODS
    # ==============================================================================
    for y_sign in [-1, 1]:
        py_in = (Y_HW + 0.05) * y_sign
        py_out = (Y_HW + 0.45) * y_sign
        px_rear = -1.1
        px_fwd_top = 0.0
        px_fwd_bot = 0.4
        pz_top = 0.45
        pz_bot = 0.1
        
        # Upper pod casing
        add_quad_mesh(lines, 'C_HULL_DARK', (px_rear, py_in, pz_top), (px_fwd_top, py_in, pz_top), (px_fwd_top, py_out, pz_top), (px_rear, py_out, pz_top), u_steps=3, v_steps=2)
        # Lower pod casing
        add_quad_mesh(lines, 'C_HULL_DARK', (px_rear, py_in, pz_bot), (px_fwd_bot, py_in, pz_bot), (px_fwd_bot, py_out, pz_bot), (px_rear, py_out, pz_bot), u_steps=3, v_steps=2)
        # Outer casing
        add_quad_mesh(lines, 'C_HULL_DARK', (px_rear, py_out, pz_top), (px_fwd_top, py_out, pz_top), (px_fwd_bot, py_out, pz_bot), (px_rear, py_out, pz_bot), u_steps=3, v_steps=2)
        # Slanted forward intake
        add_quad_mesh(lines, 'C_DETAILS', (px_fwd_top, py_in, pz_top), (px_fwd_top, py_out, pz_top), (px_fwd_bot, py_out, pz_bot), (px_fwd_bot, py_in, pz_bot), u_steps=2, v_steps=3)
        # Rear vent
        add_quad_mesh(lines, 'C_DETAILS', (px_rear, py_in, pz_top), (px_rear, py_in, pz_bot), (px_rear, py_out, pz_bot), (px_rear, py_out, pz_top), u_steps=2, v_steps=3)

    # ==============================================================================
    # 5. SPHERICAL LANDING APPARATUS
    # ==============================================================================
    PAD_R = 0.18
    PAD_Z = -0.15 # Centers of the spheres, reaching near Z=-0.35 at base

    for y_sign in [-1, 1]:
        pad_y = 1.35 * y_sign # Wider than pods
        for pad_x, strut_x in [(-0.9, -0.6), (0.2, 0.0)]: # Aft and Fwd locations
            # Landing Strut dropping from pod
            append_segmented(lines, 'C_DETAILS', [strut_x, pad_x], [Y_HW * y_sign + 0.25*y_sign, pad_y], [0.1, PAD_Z])
            # Perfect Spherical Floor Dampers
            add_sphere(lines, 'C_DETAILS', pad_x, pad_y, PAD_Z, PAD_R, t_count=12)

    # ==============================================================================
    # 6. FORWARD MANIPULATOR BOOM (The "Work" in Workbee)
    # ==============================================================================
    # Base housing block
    add_cylinder(lines, 'C_DETAILS', cx=1.2, cy=0.0, cz=0.25, length=0.4, radius=0.15, axis='x', rings=3)
    # Telescoping Arm
    add_cylinder(lines, 'C_DETAILS', cx=1.6, cy=0.0, cz=0.25, length=1.2, radius=0.08, axis='x', rings=4)
    # Gripping Claw (4 Prongs)
    for a in [45, 135, 225, 315]:
        rad = np.radians(a)
        cx, cy, cz = 2.8, np.cos(rad)*0.1, 0.25 + np.sin(rad)*0.1
        append_segmented(lines, 'C_DETAILS', [2.8, 3.0, 3.1], [cy, cy*1.5, cy*0.5], [cz, 0.25+np.sin(rad)*0.15, 0.25+np.sin(rad)*0.05])
    # Core nozzle
    add_cylinder(lines, 'C_DETAILS', cx=2.8, cy=0.0, cz=0.25, length=0.1, radius=0.06, axis='x', rings=2)

    # Roof Sensor Beacon
    add_sphere(lines, 'C_ACCENT', cx=-0.2, cy=0.0, cz=1.25, radius=0.08, t_count=8)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_workbee_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking the geometric True Center of the 4.2m vehicle mass.
        cam_x, cam_y, cam_z = 0.4, 0.0, 0.4
        
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
    # Anchor = 0.4m (Z-axis). Total vessel length is 4.3m, width 3.0m.
    # Setting cam_span safely wide to 3.2 to yield 6.4m horizontal footprint.
    # Vertical bounds output 3.2 * 1.777 = 5.68m (x2 = 11.36m height allowed).
    # Beautifully frames the small, compact industrial pod escaping all HUD limits.
    cam_span = 3.2
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_HULL_MAIN', C_HULL_MAIN, 1.4, 1.0),
        ('C_HULL_DARK', C_HULL_DARK, 1.6, 1.0),
        ('C_DETAILS',   C_DETAILS,   1.4, 1.0),
        ('C_COCKPIT',   C_COCKPIT,   1.8, 1.0),
        ('C_ACCENT',    C_ACCENT,    2.0, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +15 degrees to peer perfectly over the massive frontal windshield mapping
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=15.0)
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-450o // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // TYPE-11 WORKBEE MATRIX", color=C_HULL_DARK, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_ACCENT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: INDUSTRIAL CABIN / DEPLOYED GRAPPLE BOOM", color=C_DETAILS, fontsize=11, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-450o: WORKBEE KINEMATICS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
