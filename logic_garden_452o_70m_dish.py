"""
PROJECT: Logic Garden 452o (Exact Physical Construct // 70-Metre Dish Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: 70M DISH, DEEP SPACE NETWORK, NASA DSN, GLB, WIREFRAME, ENGINEERING, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional 70.0m aerospace scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: 70m Parabolic Dish, Dual-Layer Backing Truss, Alidade Base, Quadripod, Subreflector.
- Procedural Topography: High-density mesh mirroring unoptimised binary capture limits (Dish pitched seamlessly at 45-deg).
- Viewport Override: Locked cam_span rigorously guarantees 100% full-station visibility between UI boundaries.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from 115-degree dramatic front-quarter angle.
- Daylight Palette (White Substrate / High-Contrast Edge Geometry).
- Purged Jargon. Australian spelling conventions (maths, colour, kilometres, synchronisation, manoeuvre).
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
OUT_DIR = "frames_452o_70m_dish"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Terrestrial Tracking Grid)

C_DISH      = '#334155'          # Heavy Slate (70m Primary Parabolic Reflector)
C_TRUSS     = '#0F172A'          # Abyssal Slate (Backing Structural Mesh & Quadripod)
C_BASE      = '#1E293B'          # Carbon Slate (Concrete Pedestal & Alidade)
C_SUBREF    = '#CA8A04'          # Kapton Gold (Cassegrain Subreflector & Feed Horns)

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
def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='z', rings=4, t_count=16):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, length, rings)
    for s in steps:
        if axis == 'x':  ix, iy, iz = np.full_like(t, cx + s), cy + radius*np.cos(t), cz + radius*np.sin(t)
        elif axis == 'y':ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + s), cz + radius*np.sin(t)
        else:            ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), np.full_like(t, cz + s)
        append_sym(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        if axis == 'x':  sx, sy, sz = cx + steps, [cy + radius*np.cos(a)]*rings, [cz + radius*np.sin(a)]*rings
        elif axis == 'y':sx, sy, sz = [cx + radius*np.cos(a)]*rings, cy + steps, [cz + radius*np.sin(a)]*rings
        else:            sx, sy, sz = [cx + radius*np.cos(a)]*rings, [cy + radius*np.sin(a)]*rings, cz + steps
        append_sym(lines_dict, col, sx, sy, sz)

def add_cone_frustum(lines_dict, col, cx, cy, cz, dz, r1, r2, axis='z', rings=4, t_count=16):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, dz, rings)
    r_step = np.linspace(r1, r2, rings)
    
    for i, s in enumerate(steps):
        r = r_step[i]
        if axis == 'x':  ix, iy, iz = np.full_like(t, cx + s), cy + r*np.cos(t), cz + r*np.sin(t)
        elif axis == 'y':ix, iy, iz = cx + r*np.cos(t), np.full_like(t, cy + s), cz + r*np.sin(t)
        else:            ix, iy, iz = cx + r*np.cos(t), cy + r*np.sin(t), np.full_like(t, cz + s)
        append_sym(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        sx, sy, sz = [], [], []
        for i, s in enumerate(steps):
            r = r_step[i]
            if axis == 'x':  sx.append(cx + s); sy.append(cy + r*np.cos(a)); sz.append(cz + r*np.sin(a))
            elif axis == 'y':sx.append(cx + r*np.cos(a)); sy.append(cy + s); sz.append(cz + r*np.sin(a))
            else:            sx.append(cx + r*np.cos(a)); sy.append(cy + r*np.sin(a)); sz.append(cz + s)
        append_sym(lines_dict, col, sx, sy, sz)

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (70-Metre Deep Space Network Dish)
# ------------------------------------------------------------------
def rotate_pitch(xs, ys, zs, theta):
    """ Rotates local coordinates around the Y-axis (Elevation Pitch) """
    xs, ys, zs = np.array(xs), np.array(ys), np.array(zs)
    xr = xs * np.cos(theta) + zs * np.sin(theta)
    zr = -xs * np.sin(theta) + zs * np.cos(theta)
    return xr, ys, zr

def generate_70m_dish_static():
    lines = {
        'C_DISH': [], 'C_TRUSS': [], 'C_BASE': [],
        'C_SUBREF': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. TERRESTRIAL TRACKING BASEPLATE (1 Unit = 1 Metre)
    # ==============================================================================
    Z_FLOOR = -30.0
    for r_p in [20.0, 40.0, 60.0]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-60.0, 60.0, 13)
    gy_range = np.linspace(-60.0, 60.0, 13)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. FIXED PEDESTAL & ALIDADE (Azimuth / Elevation Mounts)
    # ==============================================================================
    # Concrete Pedestal Shaft
    add_cylinder(lines, 'C_BASE', cx=0.0, cy=0.0, cz=Z_FLOOR, length=12.0, radius=16.0, axis='z', rings=5, t_count=24)
    # Rotating Hydrostatic Bearing Base (Octagon)
    add_cylinder(lines, 'C_TRUSS', cx=0.0, cy=0.0, cz=-18.0, length=4.0, radius=18.0, axis='z', rings=3, t_count=8)
    
    # Giant Alidade Towers (Rising from Z=-14 to Z=0 elevation bearings)
    # Tower anchors at roughly +/- 15m Y, reaching up to the elevation pins.
    for y_sign in [-1, 1]:
        # Tower uprights
        append_segmented(lines, 'C_BASE', [10.0, 0.0], [15.0*y_sign, 15.0*y_sign], [-14.0, 0.0])
        append_segmented(lines, 'C_BASE', [-10.0, 0.0], [15.0*y_sign, 15.0*y_sign], [-14.0, 0.0])
        add_cylinder(lines, 'C_TRUSS', cx=0.0, cy=15.0*y_sign, cz=0.0, length=2.0*(-y_sign), radius=1.5, axis='y', rings=2, t_count=8)

    # ==============================================================================
    # 3. LOCALLY CONSTRUCTED 70-METRE PRIMARY DISH & TRUSS (Tilted -45 deg)
    # ==============================================================================
    TILT = np.radians(-45.0)  # Elevation Pitch Angle
    R_DISH = 35.0             # 70-metre diameter
    FOCAL = 25.0              # Deep parabola parameter
    Z_OFFSET = 3.0            # Offset above the elevation bearings
    
    # 3.1 Primary Parabolic Reflector Surface (Z = R^2 / 4f)
    r_steps = np.linspace(2.0, R_DISH, 12)
    t = np.linspace(0, 2*np.pi, 48, endpoint=False)
    
    # Latitudinal rings
    for r in r_steps:
        xl_c = r * np.cos(t)
        yl_c = r * np.sin(t)
        zl_c = np.full_like(t, Z_OFFSET + (r**2) / (4 * FOCAL))
        xr, yr, zr = rotate_pitch(list(xl_c)+[xl_c[0]], list(yl_c)+[yl_c[0]], list(zl_c)+[zl_c[0]], TILT)
        append_sym(lines, 'C_DISH', xr, yr, zr)
        
    # Longitudinal radials
    for a in np.linspace(0, 2*np.pi, 24, endpoint=False):
        xl_c = r_steps * np.cos(a)
        yl_c = r_steps * np.sin(a)
        zl_c = Z_OFFSET + (r_steps**2) / (4 * FOCAL)
        xr, yr, zr = rotate_pitch(xl_c, yl_c, zl_c, TILT)
        append_sym(lines, 'C_DISH', xr, yr, zr)

    # 3.2 Backing Truss (Dense interlocking structural webbing behind the dish)
    r_truss = np.linspace(5.0, 32.0, 6)
    for r in r_truss:
        xl_t = r * np.cos(t)
        yl_t = r * np.sin(t)
        # Drops physically beneath the main reflector surface to form a thick rigid skeleton
        zl_t = np.full_like(t, Z_OFFSET - 3.0 + (r**2) / (4 * 28.0))
        xr, yr, zr = rotate_pitch(list(xl_t)+[xl_t[0]], list(yl_t)+[yl_t[0]], list(zl_t)+[zl_t[0]], TILT)
        append_sym(lines, 'C_TRUSS', xr, yr, zr)
        
        # Connect primary reflector roots to backing truss (Z-axis webbing)
        for val in range(0, 48, 2):
            x0, y0, z0 = r * np.cos(t[val]), r * np.sin(t[val]), Z_OFFSET + (r**2) / (4 * FOCAL)
            x1, y1, z1 = r * np.cos(t[val]), r * np.sin(t[val]), Z_OFFSET - 3.0 + (r**2) / (4 * 28.0)
            xr, yr, zr = rotate_pitch([x0, x1], [y0, y1], [z0, z1], TILT)
            append_segmented(lines, 'C_TRUSS', xr, yr, zr)

    # 3.3 Elevation Wheel (Massive Semi-Circular 'Bull Gear')
    # Required to drive the massive 70m payload across the Z-axis
    bull_angles = np.linspace(-np.pi, 0, 32)
    xl_bull = 16.0 * np.cos(bull_angles)
    yl_bull = np.zeros_like(bull_angles)
    zl_bull = 16.0 * np.sin(bull_angles)
    xr_bull, yr_bull, zr_bull = rotate_pitch(xl_bull, yl_bull, zl_bull, TILT)
    append_sym(lines, 'C_TRUSS', xr_bull, yr_bull, zr_bull)

    # 3.4 Focal Feed Cone (Central Instrument Plume)
    # The Cassegrain central feed housing protruding from the vertex
    r_feed_base, r_feed_tip = 3.5, 1.5
    z_feed_base, z_feed_tip = Z_OFFSET + 0.5, Z_OFFSET + 6.0
    for ang in np.linspace(0, 2*np.pi, 8, endpoint=False):
        xl_f = [r_feed_base * np.cos(ang), r_feed_tip * np.cos(ang)]
        yl_f = [r_feed_base * np.sin(ang), r_feed_tip * np.sin(ang)]
        zl_f = [z_feed_base, z_feed_tip]
        xr, yr, zr = rotate_pitch(xl_f, yl_f, zl_f, TILT)
        append_segmented(lines, 'C_SUBREF', xr, yr, zr)

    # 3.5 Asymmetric Quadripod Struts & Cassegrain Subreflector
    Z_SUBREF = Z_OFFSET + FOCAL
    R_SUBREF = 4.0
    
    # Subreflector Dish
    for r in np.linspace(0.5, R_SUBREF, 4):
        xl_s = r * np.cos(t)
        yl_s = r * np.sin(t)
        # Hyperboloidal outward flex
        zl_s = np.full_like(t, Z_SUBREF + (r**2)/10.0)
        xr, yr, zr = rotate_pitch(list(xl_s)+[xl_s[0]], list(yl_s)+[yl_s[0]], list(zl_s)+[zl_s[0]], TILT)
        append_sym(lines, 'C_SUBREF', xr, yr, zr)

    # Four massive struts tying the prime 35m rim radially inwards to the subreflector
    quad_angles = [np.pi/4, 3*np.pi/4, 5*np.pi/4, 7*np.pi/4]
    for ang in quad_angles:
        x0 = R_DISH * np.cos(ang)
        y0 = R_DISH * np.sin(ang)
        z0 = Z_OFFSET + (R_DISH**2)/(4*FOCAL)
        
        x1 = R_SUBREF * np.cos(ang)
        y1 = R_SUBREF * np.sin(ang)
        z1 = Z_SUBREF
        
        xr, yr, zr = rotate_pitch([x0, x1], [y0, y1], [z0, z1], TILT)
        append_segmented(lines, 'C_TRUSS', xr, yr, zr)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_70m_dish_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry flawlessly at celestial baseplate origin
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.0
        
        # Starts explicitly from 115-degrees (Dramatic aesthetic exposing the pitched 70m dish and concrete pedestal)
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
    # Anchor Centroid = Dead zero. 70-metre dish dynamically pitched at 45-degrees.
    # Total swept volume reaches roughly +/- 45m along operational axes.
    # Setting cam_span strictly to 60.0 locks horizontal width symmetrically across an immense 120.0m.
    # Vertical bounds output 60.0 * 1.777 = 106.62m total height window vertically.
    # Completely traps the colossal tracking station absolutely safely inside the transparent viewport, immune to UI clipping.
    cam_span = 60.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_BASE',      C_BASE,      1.2, 1.0),
        ('C_TRUSS',     C_TRUSS,     0.9, 1.0),
        ('C_DISH',      C_DISH,      1.5, 1.0),
        ('C_SUBREF',    C_SUBREF,    1.3, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to clearly parse the colossal internal parabolas and underlying alidade mechanics
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=16.0)
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-452o // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // 70-METRE DEEP SPACE NETWORK ANTENNA", color=C_DISH, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_TRUSS, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: 70M PARABOLIC DISH / QUADRIPOD / ALIDADE / CONCRETE BASE", color=C_SUBREF, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-452o: 70M DISH TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
