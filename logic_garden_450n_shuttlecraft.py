"""
PROJECT: Logic Garden 450n (Exact Physical Construct // Type-II Shuttlecraft Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: STAR TREK, SHUTTLECRAFT, ENTERPRISE, AEROSPACE, WIREFRAME, ENGINEERING, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Faceted forward nose, cantilevered warp nacelles, deployed landing struts.
- Strict Bounds Protocol: Core locked at mid-body. cam_span scaled to 5.5 for flawless, unclipped 100% full-body framing.
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
OUT_DIR = "frames_450n_shuttlecraft"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Baseplate Reference)

C_HULL_MAIN = '#94A3B8'          # Heavy Slate (Primary Shuttle Hull Panels)
C_HULL_DARK = '#475569'          # Machined Slate (Underbelly, Thrust Mounts)
C_DETAILS   = '#1E293B'          # Carbon Slate (Wings, Structural Ribs)
C_COCKPIT   = '#111115'          # Indestructible Black (Forward Windows)
C_BUSSARD   = '#E11D48'          # Kinematic Red (Front Nacelle Domes)
C_IMPULSE   = '#00D2FF'          # High Engine Cyan (Aft Impulse Drive Grille)

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

def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='x', rings=6, t_count=16):
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

def add_dome(lines_dict, col, cx, cy, cz, radius, axis='x', dir=1, rings=4, t_count=16):
    p_step = np.linspace(0, np.pi/2, rings)
    for p in p_step:
        r_s = radius * np.cos(p)
        h_s = radius * np.sin(p) * dir
        t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
        if axis == 'x':   ix, iy, iz = np.full_like(t, cx + h_s), cy + r_s*np.cos(t), cz + r_s*np.sin(t)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        rr = radius * np.cos(p_step)
        hh = radius * np.sin(p_step) * dir
        if axis == 'x':   sx, sy, sz = cx + hh, cy + rr*np.cos(a), cz + rr*np.sin(a)
        append_segmented(lines_dict, col, list(sx), list(sy), list(sz))

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (TYPE-II SHUTTLECRAFT)
# ------------------------------------------------------------------
def generate_shuttle_static():
    lines = {
        'C_HULL_MAIN': [], 'C_HULL_DARK': [], 'C_DETAILS': [], 
        'C_COCKPIT': [], 'C_BUSSARD': [], 'C_IMPULSE': [], 'C_GRID': []
    }

    # 1. BASEPLATE ENVELOPE (REFERENCE GRID)
    gx_range = np.linspace(-6.0, 6.0, 13)
    gy_range = np.linspace(-6.0, 6.0, 13)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, -0.8))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, -0.8))

    # ==============================================================================
    # 2. THE FACETED POLYGONAL CABIN
    # ==============================================================================
    X_REAR = -3.5
    X_TOP_FWD = 2.0
    X_NOSE = 3.5
    X_BOT_FWD = 2.5
    Z_TOP = 2.2
    Z_NOSE = 1.0
    Z_BOT = 0.0
    Y_HW = 1.4

    # Roof & Floor Plates
    add_quad_mesh(lines, 'C_HULL_MAIN', (X_REAR, -Y_HW, Z_TOP), (X_TOP_FWD, -Y_HW, Z_TOP), (X_TOP_FWD, Y_HW, Z_TOP), (X_REAR, Y_HW, Z_TOP), u_steps=8, v_steps=4)
    add_quad_mesh(lines, 'C_HULL_DARK', (X_REAR, -Y_HW, Z_BOT), (X_BOT_FWD, -Y_HW, Z_BOT), (X_BOT_FWD, Y_HW, Z_BOT), (X_REAR, Y_HW, Z_BOT), u_steps=8, v_steps=4)

    # Forward Dynamic Window Plane (Slanted)
    add_quad_mesh(lines, 'C_HULL_MAIN', (X_TOP_FWD, -Y_HW, Z_TOP), (X_NOSE, -Y_HW, Z_NOSE), (X_NOSE, Y_HW, Z_NOSE), (X_TOP_FWD, Y_HW, Z_TOP), u_steps=3, v_steps=4)
    
    # Under-Nose Cutback
    add_quad_mesh(lines, 'C_HULL_DARK', (X_NOSE, -Y_HW, Z_NOSE), (X_BOT_FWD, -Y_HW, Z_BOT), (X_BOT_FWD, Y_HW, Z_BOT), (X_NOSE, Y_HW, Z_NOSE), u_steps=2, v_steps=4)

    # Aft Engineering Plane (Rear Wall)
    add_quad_mesh(lines, 'C_HULL_MAIN', (X_REAR, Y_HW, Z_TOP), (X_REAR, -Y_HW, Z_TOP), (X_REAR, -Y_HW, Z_BOT), (X_REAR, Y_HW, Z_BOT), u_steps=4, v_steps=4)

    # Lateral Hull Facets (Port and Starboard Sides)
    for y_sign in [-1, 1]:
        y = Y_HW * y_sign
        # Main Rear/Mid body
        add_quad_mesh(lines, 'C_HULL_MAIN', (X_REAR, y, Z_TOP), (X_TOP_FWD, y, Z_TOP), (X_BOT_FWD, y, Z_BOT), (X_REAR, y, Z_BOT), u_steps=6, v_steps=4)
        # Forward Nose Wedge
        append_segmented(lines, 'C_HULL_MAIN', [X_TOP_FWD, X_NOSE, X_BOT_FWD, X_TOP_FWD], [y]*4, [Z_TOP, Z_NOSE, Z_BOT, Z_TOP])

    # ==============================================================================
    # 3. WINDOW ARRAYS AND SENSORS
    # ==============================================================================
    # The 3-panel forward panoramic cockpit glass
    wy_centers = [-0.65, 0.0, 0.65]
    for wy in wy_centers:
        wx1 = X_TOP_FWD + 0.3
        wx2 = X_NOSE - 0.3
        wz1 = Z_TOP - 0.25
        wz2 = Z_NOSE + 0.25
        append_segmented(lines, 'C_COCKPIT', [wx1, wx2, wx2, wx1, wx1], 
                                             [wy-0.25, wy-0.25, wy+0.25, wy+0.25, wy-0.25], 
                                             [wz1, wz2, wz2, wz1, wz1])

    # Aft Impulse Engine Block
    append_segmented(lines, 'C_HULL_DARK', [X_REAR, X_REAR-0.5, X_REAR-0.5, X_REAR, X_REAR], [0.8, 0.8, -0.8, -0.8, 0.8], [1.8, 1.8, 1.8, 1.8, 1.8])
    append_segmented(lines, 'C_HULL_DARK', [X_REAR, X_REAR-0.5, X_REAR-0.5, X_REAR, X_REAR], [0.8, 0.8, -0.8, -0.8, 0.8], [0.8, 0.8, 0.8, 0.8, 0.8])
    for x_i in [-0.5, -0.3, -0.1]:
        append_segmented(lines, 'C_IMPULSE', [X_REAR+x_i]*2, [0.7, -0.7], [1.6, 1.6])
        append_segmented(lines, 'C_IMPULSE', [X_REAR+x_i]*2, [0.7, -0.7], [1.0, 1.0])

    # ==============================================================================
    # 4. WARP NACELLES & MOUNTING PYLONS
    # ==============================================================================
    NAC_R = 0.35
    NAC_Y = 2.2
    NAC_Z = 0.4
    NAC_FWD = 1.0
    NAC_AFT = -3.8

    for y_sign in [-1, 1]:
        cy = NAC_Y * y_sign
        
        # Rigid Swept Pylons linking the main chassis to the engines
        add_quad_mesh(lines, 'C_DETAILS', (0.0, Y_HW*y_sign, 0.8), (-3.0, Y_HW*y_sign, 0.8), 
                                          (-3.5, cy, NAC_Z), (0.0, cy, NAC_Z), u_steps=4, v_steps=2)
        add_quad_mesh(lines, 'C_DETAILS', (0.0, Y_HW*y_sign, 0.3), (-3.0, Y_HW*y_sign, 0.3), 
                                          (-3.5, cy, NAC_Z-0.1), (0.0, cy, NAC_Z-0.1), u_steps=4, v_steps=2)

        # Primary Cylindrical Warp Housing
        add_cylinder(lines, 'C_HULL_MAIN', cx=NAC_AFT, cy=cy, cz=NAC_Z, length=abs(NAC_FWD - NAC_AFT), radius=NAC_R, axis='x', rings=8, t_count=16)

        # Forward Bussard Collectors (Kinematic Red Domes)
        add_dome(lines, 'C_BUSSARD', cx=NAC_FWD, cy=cy, cz=NAC_Z, radius=NAC_R, axis='x', dir=1, rings=4, t_count=16)
        
        # Aft Exhaust Cones / Thruster Assemblies
        add_dome(lines, 'C_DETAILS', cx=NAC_AFT, cy=cy, cz=NAC_Z, radius=NAC_R*0.8, axis='x', dir=-1, rings=3, t_count=12)

        # Lateral Warp Grilles (Blacked out vents on side)
        for g_z in [NAC_Z + 0.15, NAC_Z, NAC_Z - 0.15]:
            append_segmented(lines, 'C_DETAILS', [NAC_AFT+0.5, NAC_FWD-0.5], [cy+NAC_R*y_sign*1.02]*2, [g_z]*2)

    # ==============================================================================
    # 5. TRI-STRUT DEPLOYED LANDING GEAR
    # ==============================================================================
    PAD_Z = -0.8
    PAD_R = 0.25

    # Aft Pads
    for y_sign in [-1, 1]:
        pad_y = 1.8 * y_sign
        pad_x = -2.8
        # Hydraulic strut from bottom hull
        append_segmented(lines, 'C_DETAILS', [-2.5, pad_x], [1.0*y_sign, pad_y], [0.0, PAD_Z])
        # Force distribution footpad
        add_cylinder(lines, 'C_DETAILS', cx=pad_x, cy=pad_y, cz=PAD_Z, length=0.08, radius=PAD_R, axis='z', rings=2, t_count=16)

    # Forward Center Pad
    f_pad_x = 2.5
    f_pad_y = 0.0
    append_segmented(lines, 'C_DETAILS', [2.0, f_pad_x], [0.0, f_pad_y], [0.0, PAD_Z])
    add_cylinder(lines, 'C_DETAILS', cx=f_pad_x, cy=f_pad_y, cz=PAD_Z, length=0.08, radius=PAD_R, axis='z', rings=2, t_count=16)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_shuttle_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking the geometric True Center of the 7.5m mass
        cam_x, cam_y, cam_z = 0.0, 0.0, 1.1
        
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
    # Anchor = 1.1m (Z-axis). Total vessel length is 7.5m (radius approx 4m).
    # Setting cam_span safely wide to 5.5 to yield 11.0m horizontal footprint.
    # Vertical bounds output 5.5 * 1.777 = 9.77m (x2 = 19.5m height allowed).
    # Escapes all text overlays entirely preventing mechanical clipping.
    cam_span = 5.5
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_HULL_MAIN', C_HULL_MAIN, 1.3, 1.0),
        ('C_HULL_DARK', C_HULL_DARK, 1.5, 1.0),
        ('C_DETAILS',   C_DETAILS,   1.2, 1.0),
        ('C_COCKPIT',   C_COCKPIT,   1.8, 1.0),
        ('C_IMPULSE',   C_IMPULSE,   1.6, 1.0),
        ('C_BUSSARD',   C_BUSSARD,   1.8, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +12 degrees to proudly array the cantilevered nacelles over the landing footprint
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=12.0)
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-450n // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // TYPE-II SHUTTLECRAFT MATRIX", color=C_HULL_DARK, fontsize=13, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_BUSSARD, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: FACETED HULL / CANTILEVERED WARP NACELLES", color=C_DETAILS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-450n: SHUTTLECRAFT KINEMATICS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
