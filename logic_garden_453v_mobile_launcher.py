"""
PROJECT: Logic Garden 453v (Exact Physical Construct // Mobile Launcher Assembled)
FORMAT: YouTube Shorts (1080x1920)
METADATA: MOBILE LAUNCHER, SLS, NASA, ARTEMIS, GLB, WIREFRAME, PYTHON
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional 125m orbital scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Base Platform, Umbilical Tower, Swing Arms, TSMUs, Lightning Mast.
- Procedural Topography: High-density mesh mirroring asymmetrical hardware constraints.
- Hotfix Integration: Strict np.full_like() propagation inside geometric primitives preventing Scalar Faults.
- Strict Bounds Protocol: cam_span aggressively escalated to 55.0 avoiding Top UI metadata occlusion.
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
OUT_DIR = "frames_453v_mobile_launcher"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Urban Tracking Grid)

C_BASE      = '#334155'          # Heavy Slate (Primary 2-Story Launch Platform)
C_EXHAUST   = '#1E293B'          # Carbon Slate (Thermal Blast Chamber Cutout)
C_TOWER     = '#94A3B8'          # Slate Aluminium (Launch Umbilical Tower & Mast)
C_ARMS      = '#005599'          # Deep Marine (Crew Access & Cryogenic Swing Arms)
C_TSMU      = '#CA8A04'          # Kapton Gold (Tail Service Masts & Base Interfaces)

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
    # Autonomously generates identical structural topology across the Y-axis (Port/Starboard Mirroring)
    if any(abs(y) > 0.001 for y in ys):
        append_segmented(lines_dict, key, xs, [-y for y in ys], zs)

# ------------------------------------------------------------------
# GEOMETRIC PRIMITIVES (HOTFIXED SCALAR ITERATION FAULTS)
# ------------------------------------------------------------------
def add_quad_mesh(lines_dict, col, p1, p2, p3, p4, u_steps=4, v_steps=4, reflect_y=False):
    p1, p2, p3, p4 = map(np.array, (p1, p2, p3, p4))
    for i in range(v_steps + 1):
        v = i / v_steps
        start = p1 * (1-v) + p4 * v
        end   = p2 * (1-v) + p3 * v
        pts = [start * (1-u) + end * u for u in np.linspace(0, 1, u_steps+1)]
        if reflect_y:
            append_sym(lines_dict, col, [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts])
        else:
            append_segmented(lines_dict, col, [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts])
    for i in range(u_steps + 1):
        u = i / u_steps
        start = p1 * (1-u) + p2 * u
        end   = p4 * (1-u) + p3 * u
        pts = [start * (1-v) + end * v for v in np.linspace(0, 1, v_steps+1)]
        if reflect_y:
            append_sym(lines_dict, col, [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts])
        else:
            append_segmented(lines_dict, col, [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts])

def add_box_mesh(lines_dict, col, x1, x2, y1, y2, z1, z2, div=4, reflect_y=False):
    add_quad_mesh(lines_dict, col, (x1, y1, z1), (x2, y1, z1), (x2, y2, z1), (x1, y2, z1), div, div, reflect_y)
    add_quad_mesh(lines_dict, col, (x1, y1, z2), (x2, y1, z2), (x2, y2, z2), (x1, y2, z2), div, div, reflect_y)
    add_quad_mesh(lines_dict, col, (x1, y1, z1), (x2, y1, z1), (x2, y1, z2), (x1, y1, z2), div, div, reflect_y)
    add_quad_mesh(lines_dict, col, (x1, y2, z1), (x2, y2, z1), (x2, y2, z2), (x1, y2, z2), div, div, reflect_y)
    add_quad_mesh(lines_dict, col, (x1, y1, z1), (x1, y2, z1), (x1, y2, z2), (x1, y1, z2), div, div, reflect_y)
    add_quad_mesh(lines_dict, col, (x2, y1, z1), (x2, y2, z1), (x2, y2, z2), (x2, y1, z2), div, div, reflect_y)

def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='z', rings=4, t_count=16, reflect_y=False):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, length, rings)
    for s in steps:
        # Explicit propagation preventing dimensional collapse
        if axis == 'x':  
            ix, iy, iz = np.full_like(t, cx + s), cy + radius*np.cos(t), cz + radius*np.sin(t)
        elif axis == 'y':
            ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + s), cz + radius*np.sin(t)
        else:            
            ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), np.full_like(t, cz + s)
            
        if reflect_y: append_sym(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
        else: append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
        
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        if axis == 'x':  sx, sy, sz = cx + steps, np.full_like(steps, cy + radius*np.cos(a)), np.full_like(steps, cz + radius*np.sin(a))
        elif axis == 'y':sx, sy, sz = np.full_like(steps, cx + radius*np.cos(a)), cy + steps, np.full_like(steps, cz + radius*np.sin(a))
        else:            sx, sy, sz = np.full_like(steps, cx + radius*np.cos(a)), np.full_like(steps, cy + radius*np.sin(a)), cz + steps
        if reflect_y: append_sym(lines_dict, col, sx, sy, sz)
        else: append_segmented(lines_dict, col, sx, sy, sz)

def add_cone_frustum(lines_dict, col, cx, cy, cz, dz, r1, r2, axis='z', rings=4, t_count=16, reflect_y=False):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, dz, rings)
    r_step = np.linspace(r1, r2, rings)
    
    for i, s in enumerate(steps):
        r = r_step[i]
        if axis == 'x':  
            ix, iy, iz = np.full_like(t, cx + s), cy + r*np.cos(t), cz + r*np.sin(t)
        elif axis == 'y':
            ix, iy, iz = cx + r*np.cos(t), np.full_like(t, cy + s), cz + r*np.sin(t)
        else:            
            ix, iy, iz = cx + r*np.cos(t), cy + r*np.sin(t), np.full_like(t, cz + s)
        if reflect_y: append_sym(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
        else: append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        sx, sy, sz = [], [], []
        for i, s in enumerate(steps):
            r = r_step[i]
            if axis == 'x':  sx.append(cx + s); sy.append(cy + r*np.cos(a)); sz.append(cz + r*np.sin(a))
            elif axis == 'y':sx.append(cx + r*np.cos(a)); sy.append(cy + s); sz.append(cz + r*np.sin(a))
            else:            sx.append(cx + r*np.cos(a)); sy.append(cy + r*np.sin(a)); sz.append(cz + s)
        if reflect_y: append_sym(lines_dict, col, sx, sy, sz)
        else: append_segmented(lines_dict, col, sx, sy, sz)


# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (MOBILE LAUNCHER)
# ------------------------------------------------------------------
def generate_mobile_launcher_static():
    lines = {
        'C_BASE': [], 'C_HULL': [], 'C_EXHAUST': [],
        'C_TOWER': [], 'C_ARMS': [], 'C_TSMU': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. TERRESTRIAL CRAWLERWAY TRACKING BASEPLATE
    # ==============================================================================
    Z_FLOOR = -3.0
    for r_p in [15.0, 30.0, 45.0]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-45.0, 45.0, 25)
    gy_range = np.linspace(-45.0, 45.0, 25)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. HEAVY STRUCTURAL PLATFORM BASE (The Lower Deck)
    # ==============================================================================
    # Massive 45m x 41m two-story block. Offset X=0 to allow absolute centering.
    PLATFORM_X_MIN, PLATFORM_X_MAX = -22.5, 22.5
    PLATFORM_Y_MIN, PLATFORM_Y_MAX = -20.5, 20.5
    PLATFORM_Z = 7.6
    
    add_box_mesh(lines, 'C_BASE', PLATFORM_X_MIN, PLATFORM_X_MAX, PLATFORM_Y_MIN, PLATFORM_Y_MAX, 0.0, PLATFORM_Z, div=5)

    # Core Stage Main Engine Exhaust Cutout
    add_cylinder(lines, 'C_EXHAUST', cx=-4.0, cy=0.0, cz=0.0, length=PLATFORM_Z+0.5, radius=7.0, axis='z', rings=5, t_count=32)
    # Solid Booster Drop Holes
    for y_b in [-8.0, 8.0]:
        add_cylinder(lines, 'C_EXHAUST', cx=-4.0, cy=y_b, cz=0.0, length=PLATFORM_Z+0.2, radius=2.5, axis='z', rings=3, t_count=16)

    # ==============================================================================
    # 3. UMBILICAL TOWER (LUT MATRIX)
    # ==============================================================================
    # Rises from the forward section of the deck (X: 10.0 to 18.0) up to 110.0 metres.
    TOWER_X_MIN, TOWER_X_MAX = 10.0, 18.0
    TOWER_Y_MIN, TOWER_Y_MAX = -6.0, 6.0
    TOWER_Z_TOP = 110.0
    
    # Outer Trusses (Vertical structural bounding box)
    add_box_mesh(lines, 'C_TOWER', TOWER_X_MIN, TOWER_X_MAX, TOWER_Y_MIN, TOWER_Y_MAX, PLATFORM_Z, TOWER_Z_TOP, div=5)
    
    # Horizontal Inter-Stage Flooring
    for z_deck in np.linspace(17.6, 107.6, 10):
        add_box_mesh(lines, 'C_TOWER', TOWER_X_MIN, TOWER_X_MAX, TOWER_Y_MIN, TOWER_Y_MAX, z_deck-0.5, z_deck, div=2)

    # Lightning Mast & Crane Assembly (Reaching completely to 125 metres)
    add_cylinder(lines, 'C_TOWER', cx=14.0, cy=0.0, cz=TOWER_Z_TOP, length=15.0, radius=0.6, axis='z', rings=4, t_count=12)

    # ==============================================================================
    # 4. SWING ARMS & UMBILICAL MANIFOLDS
    # ==============================================================================
    def add_swing_arm(z_level, length, width, depth_z):
        start_x = TOWER_X_MIN
        end_x = TOWER_X_MIN - length
        add_box_mesh(lines, 'C_ARMS', end_x, start_x, -width/2.0, width/2.0, z_level-depth_z, z_level, div=2)
        add_box_mesh(lines, 'C_TSMU', end_x-1.0, end_x, -width/1.5, width/1.5, z_level-depth_z, z_level, div=1)

    # Crew Access Arm (CAA) 
    add_swing_arm(z_level=90.0, length=18.0, width=2.5, depth_z=2.0)
    # Core Stage Forward Skirt Umbilical (CSFSU)
    add_swing_arm(z_level=75.0, length=17.0, width=2.0, depth_z=1.5)
    # Interim Cryogenic Propulsion Stage Umbilical (ICPSU)
    add_swing_arm(z_level=60.0, length=16.0, width=2.0, depth_z=1.5)
    # Core Stage Inter-tank Umbilical (CSITU)
    add_swing_arm(z_level=45.0, length=16.0, width=2.0, depth_z=1.5)
    # Aft Skirt Electrical Umbilicals
    add_swing_arm(z_level=20.0, length=15.0, width=1.5, depth_z=1.0)

    # ==============================================================================
    # 5. TAIL SERVICE MASTS & BASE VSPs
    # ==============================================================================
    for y_offset in [-6.5, 6.5]:
        add_box_mesh(lines, 'C_TSMU', -8.0, -3.0, y_offset-1.5, y_offset+1.5, PLATFORM_Z, PLATFORM_Z+12.0, div=3)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_mobile_launcher_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        cam_x, cam_y, cam_z = 0.0, 0.0, 57.5
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
    # Anchor Centroid = Z=57.5m. The observatory extents stretch from Z=125.0m (Lightning Mast) down to Z=0.0m (Platform).
    # To clear the Top UI panel (which spawns at Y=+79.75m based on `cam_span * 1.45`), we MUST increase the bound.
    # Maximum rendered height of mast above centroid at 16 degrees tilt: ~70.5 metres.
    # By strictly commanding `cam_span = 55.0`, the horizontal span scales completely out to 110.0m.
    # Vertical transparent window outputs 55.0 * 1.777 = 97.73m half-height.
    # Top UI panel boundary guarantees a full 9-metre clearance above the extreme altitude lightning rod preventing HUD clipping perfectly.
    cam_span = 55.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_BASE',      C_BASE,      1.3, 1.0),
        ('C_EXHAUST',   C_EXHAUST,   1.2, 0.9),
        ('C_TOWER',     C_TOWER,     1.0, 0.8),
        ('C_TSMU',      C_TSMU,      1.5, 1.0),
        ('C_ARMS',      C_ARMS,      1.6, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=16.0)
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-453v // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // MOBILE LAUNCHER (ASSEMBLED) MATRIX", color=C_BASE, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_ARMS, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: 45M LAUNCH PLATFORM / 110M UMBILICAL TOWER / 5X CREW-ACCESS ARMS", color=C_TSMU, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-453v: MOBILE LAUNCHER (ASSEMBLED) TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
