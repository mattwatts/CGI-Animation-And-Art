"""
PROJECT: Logic Garden 451z (Exact Physical Construct // Apollo-Soyuz Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: APOLLO, SOYUZ, ASTP, NASA, ROSCOSMOS, WIREFRAME, ENGINEERING, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional 23.3m aerospace scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Apollo CSM, Docking Module, Soyuz 7K-TM modules (BO, SA, PAO), Solar Arrays.
- Viewport Override: Locked cam_span rigorously guarantees 100% vehicle visibility strictly between UI boundaries.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from 115-degree dramatic front-quarter angle.
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
OUT_DIR = "frames_451z_apollo_soyuz"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#CBD5E1'          # Subdued Steel (Flight Plane Tracking Grid)

C_APOLLO    = '#94A3B8'          # Slate Aluminium (Apollo Service & Command Module)
C_DM        = '#475569'          # Machined Slate (Universal Docking Module)
C_SOYUZ     = '#1E293B'          # Carbon Slate (Soyuz Hull & Descent Module)
C_SOYUZ_PAO = '#0F172A'          # Abyssal Slate (Soyuz Service Module)
C_PANELS    = '#005599'          # Deep Marine (Soyuz Twin Solar Arrays)
C_ENGINE    = '#E11D48'          # Kinematic Red (SPS thrust bell & Soyuz Main Engine)
C_HARDWARE  = '#111115'          # Indestructible Black (Thruster Quads & Periscopes)

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

def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='x', rings=4, t_count=16):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, length, rings)
    for s in steps:
        if axis == 'x':  ix, iy, iz = np.full_like(t, cx + s), cy + radius*np.cos(t), cz + radius*np.sin(t)
        elif axis == 'y': ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + s), cz + radius*np.sin(t)
        else:             ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), np.full_like(t, cz + s)
        append_sym(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        if axis == 'x':   sx, sy, sz = cx + steps, [cy + radius*np.cos(a)]*rings, [cz + radius*np.sin(a)]*rings
        elif axis == 'y': sx, sy, sz = [cx + radius*np.cos(a)]*rings, cy + steps, [cz + radius*np.sin(a)]*rings
        else:             sx, sy, sz = [cx + radius*np.cos(a)]*rings, [cy + radius*np.sin(a)]*rings, cz + steps
        append_sym(lines_dict, col, sx, sy, sz)

def add_cone_frustum(lines_dict, col, cx, cy, cz, dz, r1, r2, offset=(0,0), axis='x', rings=4, t_count=16):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, dz, rings)
    r_step = np.linspace(r1, r2, rings)
    ox_step = np.linspace(0, offset[0], rings)
    oy_step = np.linspace(0, offset[1], rings)

    for i, s in enumerate(steps):
        r, ox, oy = r_step[i], ox_step[i], oy_step[i]
        if axis == 'x':
            ix, iy, iz = np.full_like(t, cx + s), cy + ox + r*np.cos(t), cz + oy + r*np.sin(t)
        else:
            iz = np.full_like(t, cz + s)
            ix, iy = cx + ox + r*np.cos(t), cy + oy + r*np.sin(t)
        append_sym(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        sx, sy, sz = [], [], []
        for i, s in enumerate(steps):
            r, ox, oy = r_step[i], ox_step[i], oy_step[i]
            if axis == 'x':
                sx.append(cx + s); sy.append(cy + ox + r*np.cos(a)); sz.append(cz + oy + r*np.sin(a))
            else:
                sx.append(cx + ox + r*np.cos(a)); sy.append(cy + oy + r*np.sin(a)); sz.append(cz + s)
        append_sym(lines_dict, col, sx, sy, sz)

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

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (APOLLO-SOYUZ ASTP)
# ------------------------------------------------------------------
def generate_astp_static():
    lines = {
        'C_APOLLO': [], 'C_DM': [], 'C_SOYUZ': [], 
        'C_SOYUZ_PAO': [], 'C_PANELS': [], 'C_ENGINE': [], 
        'C_HARDWARE': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. ORBITAL TRACKING BASEPLATE
    # ==============================================================================
    Z_FLOOR = -4.5
    for r_p in [6.0, 12.0, 18.0]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-15.0, 15.0, 11)
    gy_range = np.linspace(-15.0, 15.0, 11)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. APOLLO COMMAND/SERVICE MODULE (CSM) (Facing Positive X)
    # ==============================================================================
    X_SM_BACK = -9.0; X_SM_FWD = -1.5; CSM_RAD = 1.95
    
    # Service Propulsion System (SPS) Engine Bell
    add_cone_frustum(lines, 'C_ENGINE', cx=-11.0, cy=0.0, cz=0.0, dz=2.0, r1=1.3, r2=0.6, axis='x', rings=5, t_count=20)
    
    # Service Module (SM) Core
    add_cylinder(lines, 'C_APOLLO', cx=X_SM_BACK, cy=0.0, cz=0.0, length=(X_SM_FWD - X_SM_BACK), radius=CSM_RAD, axis='x', rings=8, t_count=24)
    
    # Apollo RCS Thruster Quads (Mounted symmetrically at 90-degree intervals)
    for a in [0, np.pi/2, np.pi, 3*np.pi/2]:
        qx, qy, qz = -2.5, (CSM_RAD+0.1)*np.cos(a), (CSM_RAD+0.1)*np.sin(a)
        add_ellipsoid(lines, 'C_HARDWARE', cx=qx, cy=qy, cz=qz, rx=0.3, ry=0.15, rz=0.15, rings=3, t_count=8)

    # Command Module (CM) Crew Cabin
    X_CM_FWD = 1.7; CM_TIP_RAD = 0.45
    add_cone_frustum(lines, 'C_APOLLO', cx=X_SM_FWD, cy=0.0, cz=0.0, dz=(X_CM_FWD - X_SM_FWD), r1=CSM_RAD, r2=CM_TIP_RAD, axis='x', rings=6, t_count=24)

    # ==============================================================================
    # 3. UNIVERSAL DOCKING MODULE (DM)
    # ==============================================================================
    X_DM_FWD = 4.8; DM_RAD = 0.75
    add_cylinder(lines, 'C_DM', cx=X_CM_FWD, cy=0.0, cz=0.0, length=(X_DM_FWD - X_CM_FWD), radius=DM_RAD, axis='x', rings=6, t_count=20)
    
    # Exterior Nitrogen/Oxygen Pressure Vessels on the DM
    for a in [np.pi/4, 3*np.pi/4, 5*np.pi/4, 7*np.pi/4]:
        tx, ty, tz = 3.25, (DM_RAD+0.2)*np.cos(a), (DM_RAD+0.2)*np.sin(a)
        add_cylinder(lines, 'C_HARDWARE', cx=tx-0.8, cy=ty, cz=tz, length=1.6, radius=0.15, axis='x', rings=3, t_count=8)

    # ==============================================================================
    # 4. SOYUZ 7K-TM (Facing Negative X, Docked to DM at X=4.8)
    # ==============================================================================
    # Orbital Module (BO)
    OM_X_CEN = 6.0; OM_L = 2.4; OM_RAD = 1.1
    add_ellipsoid(lines, 'C_SOYUZ', cx=OM_X_CEN, cy=0.0, cz=0.0, rx=OM_L/2, ry=OM_RAD, rz=OM_RAD, rings=8, t_count=24)

    # Descent Module (SA) - Heavy bell-shape contour
    X_SA_FWD = OM_X_CEN + (OM_L/2); X_SA_AFT = 9.3; SA_RAD_AFT = 1.15
    add_cone_frustum(lines, 'C_SOYUZ', cx=X_SA_FWD, cy=0.0, cz=0.0, dz=(X_SA_AFT - X_SA_FWD), r1=0.7, r2=SA_RAD_AFT, axis='x', rings=6, t_count=24)
    # Periscope Port on Descent Module
    add_cylinder(lines, 'C_HARDWARE', cx=8.5, cy=0.0, cz=1.0, length=0.3, radius=0.1, axis='z', rings=2, t_count=8)

    # Service Module (PAO) - Flared transitioning cylinder
    X_PAO_FWD = X_SA_AFT; X_PAO_MID = 11.3; PAO_RAD_MAX = 1.35
    X_PAO_AFT = 11.8
    # Flare Transition
    add_cone_frustum(lines, 'C_SOYUZ_PAO', cx=X_PAO_FWD, cy=0.0, cz=0.0, dz=0.5, r1=SA_RAD_AFT, r2=PAO_RAD_MAX, axis='x', rings=3, t_count=24)
    # Primary Cylinder
    add_cylinder(lines, 'C_SOYUZ_PAO', cx=X_PAO_FWD+0.5, cy=0.0, cz=0.0, length=(X_PAO_MID - (X_PAO_FWD+0.5)), radius=PAO_RAD_MAX, axis='x', rings=5, t_count=24)
    # Aft Thermal Flare
    add_cone_frustum(lines, 'C_SOYUZ_PAO', cx=X_PAO_MID, cy=0.0, cz=0.0, dz=(X_PAO_AFT - X_PAO_MID), r1=PAO_RAD_MAX, r2=1.1, axis='x', rings=3, t_count=24)

    # Soyuz Main Engine Thruster
    add_cone_frustum(lines, 'C_ENGINE', cx=X_PAO_AFT, cy=0.0, cz=0.0, dz=0.5, r1=0.4, r2=0.7, axis='x', rings=3, t_count=16)

    # ==============================================================================
    # 5. SOYUZ TWIN SOLAR ARRAYS
    # ==============================================================================
    # Extended horizontally across the Y-axis from the PAO module
    PANEL_X1 = 10.0; PANEL_X2 = 11.4
    Y_ROOT = PAO_RAD_MAX; Y_TIP = 4.5
    Z_PANEL = 0.0

    for sign in [-1, 1]:
        # Outboard solar grids defined with structural segmentation
        add_quad_mesh(lines, 'C_PANELS', 
                      (PANEL_X1, Y_ROOT*sign, Z_PANEL), (PANEL_X2, Y_ROOT*sign, Z_PANEL),
                      (PANEL_X2, Y_TIP*sign, Z_PANEL), (PANEL_X1, Y_TIP*sign, Z_PANEL), 
                      u_steps=6, v_steps=12)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_astp_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry precisely midway along the 23-metre structure (X=1.0)
        cam_x, cam_y, cam_z = 1.0, 0.0, 0.0
        
        # Starts explicitly from 115-degrees (Dramatic front-quarter aesthetic pushing depth on both aerospace architectures)
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
    # Anchor Centroid = X=1.0. Total geometry bounds [-11.0 to 12.3].
    # Setting cam_span strictly to 14.0 locks horizontal bounds seamlessly across 28.0m total width.
    # Vertical bounds output 14.0 * 1.777 = 24.8m. 
    # Asserts an uncompromising, flawlessly framed 23.3m combined profile cleanly avoiding both UI banners natively.
    cam_span = 14.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.6, 0.4), 
        ('C_PANELS',    C_PANELS,    1.2, 1.0),
        ('C_APOLLO',    C_APOLLO,    1.3, 1.0),
        ('C_DM',        C_DM,        1.4, 1.0),
        ('C_SOYUZ',     C_SOYUZ,     1.3, 1.0),
        ('C_SOYUZ_PAO', C_SOYUZ_PAO, 1.4, 1.0),
        ('C_ENGINE',    C_ENGINE,    1.6, 1.0),
        ('C_HARDWARE',  C_HARDWARE,  1.5, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +15 degrees to dynamically dissect the continuous orbital volumes and solar arrays
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-451z // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // APOLLO-SOYUZ ASTP MATRIX", color=C_APOLLO, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_PANELS, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: 100% UNCLIPPED HORIZON / APOLLO CSM / DOCKING MODULE / SOYUZ 7K-TM", color=C_ENGINE, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-451z: APOLLO-SOYUZ TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
