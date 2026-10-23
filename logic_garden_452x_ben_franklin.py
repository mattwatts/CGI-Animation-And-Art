"""
PROJECT: Logic Garden 452x (Exact Physical Construct // Grumman Ben Franklin PX-15 Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: BEN FRANKLIN, PX-15, GRUMMAN, SUBMARINE, GLB, WIREFRAME, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional 14.8m maritime scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Cylindrical Pressure Hull, Hemispherical End-Caps, Dorsal Deck, Pleuger Propulsion Pods.
- Procedural Topography: High-density mesh mirroring unoptimised binary capture limits.
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
OUT_DIR = "frames_452x_ben_franklin"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Oceanographic Tracking Grid)

C_HULL      = '#334155'          # Heavy Slate (14.8m Primary Pressure Vessel & Shell)
C_DECK      = '#CA8A04'          # Kapton Gold (Dorsal Hydrodynamic Superstructure)
C_KEEL      = '#1E293B'          # Carbon Slate (Ventral Ballast & Battery Keel)
C_MOTORS    = '#005599'          # Deep Marine (Pleuger Electric Propulsion Pods)
C_HARDWARE  = '#0F172A'          # Abyssal Slate (Access Trunks & Observation Windows)

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
    # Maritime Mirroring across the Y-axis (Port / Starboard Hull Geometry)
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

def add_box_mesh(lines_dict, col, x1, x2, y1, y2, z1, z2, div=4):
    add_quad_mesh(lines_dict, col, (x1, y1, z1), (x2, y1, z1), (x2, y2, z1), (x1, y2, z1), div, div)
    add_quad_mesh(lines_dict, col, (x1, y1, z2), (x2, y1, z2), (x2, y2, z2), (x1, y2, z2), div, div)
    add_quad_mesh(lines_dict, col, (x1, y1, z1), (x2, y1, z1), (x2, y1, z2), (x1, y1, z2), div, div)
    add_quad_mesh(lines_dict, col, (x1, y2, z1), (x2, y2, z1), (x2, y2, z2), (x1, y2, z2), div, div)
    add_quad_mesh(lines_dict, col, (x1, y1, z1), (x1, y2, z1), (x1, y2, z2), (x1, y1, z2), div, div)
    add_quad_mesh(lines_dict, col, (x2, y1, z1), (x2, y2, z1), (x2, y2, z2), (x2, y1, z2), div, div)

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

def add_ellipsoid(lines_dict, col, cx, cy, cz, rx, ry, rz, rings=8, t_count=16, half=None):
    if half == 'pos_x': theta = np.linspace(-np.pi/2, np.pi/2, rings); phi = np.linspace(-np.pi/2, np.pi/2, rings)
    elif half == 'neg_x': theta = np.linspace(-np.pi/2, np.pi/2, rings); phi = np.linspace(np.pi/2, 3*np.pi/2, rings)
    else: theta = np.linspace(-np.pi/2, np.pi/2, rings); phi = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    
    for th in theta:
        xs = cx + rx * np.cos(th) * np.cos(phi)
        ys = cy + ry * np.cos(th) * np.sin(phi)
        zs = cz + rz * np.sin(th) * np.ones_like(phi)
        append_sym(lines_dict, col, list(xs)+[xs[0]] if half is None else list(xs), list(ys)+[ys[0]] if half is None else list(ys), list(zs)+[zs[0]] if half is None else list(zs))
    for ph in phi:
        xs = cx + rx * np.cos(theta) * np.cos(ph)
        ys = cy + ry * np.cos(theta) * np.sin(ph)
        zs = cz + rz * np.sin(theta)
        append_sym(lines_dict, col, xs, ys, zs)

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (GRUMMAN BEN FRANKLIN PX-15)
# ------------------------------------------------------------------
def generate_ben_franklin_static():
    lines = {
        'C_HULL': [], 'C_DECK': [], 'C_KEEL': [],
        'C_MOTORS': [], 'C_HARDWARE': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. OCEANOGRAPHIC TRACKING BASEPLATE (1 Unit = 1 Metre)
    # ==============================================================================
    Z_FLOOR = -4.0
    for r_p in [4.0, 8.0, 12.0]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-12.0, 12.0, 25)
    gy_range = np.linspace(-12.0, 12.0, 25)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. MAIN PRESSURE HULL (Mesoscaphe Architecture)
    # ==============================================================================
    R_HULL = 1.58
    L_HULL_MID = 11.6 # Central cylindrical section length
    HULL_FRONT_X = L_HULL_MID / 2.0
    HULL_REAR_X = -L_HULL_MID / 2.0
    
    # Primary Main Hull Body (X extends across the tracking origin)
    add_cylinder(lines, 'C_HULL', cx=HULL_REAR_X, cy=0.0, cz=0.0, length=L_HULL_MID, radius=R_HULL, axis='x', rings=16, t_count=24)
    
    # Bow & Stern Hemispherical End-Caps (Engineered for immense structural pressure)
    add_ellipsoid(lines, 'C_HULL', cx=HULL_FRONT_X, cy=0.0, cz=0.0, rx=1.6, ry=R_HULL, rz=R_HULL, rings=8, t_count=24, half='pos_x')
    add_ellipsoid(lines, 'C_HULL', cx=HULL_REAR_X, cy=0.0, cz=0.0, rx=1.6, ry=R_HULL, rz=R_HULL, rings=8, t_count=24, half='neg_x')

    # Observation Viewports (Plexiglas forward array plotting)
    # Central forward bow window
    add_cylinder(lines, 'C_HARDWARE', cx=HULL_FRONT_X+1.5, cy=0.0, cz=0.0, length=0.15, radius=0.3, axis='x', rings=2, t_count=12)

    # ==============================================================================
    # 3. DORSAL HYDRODYNAMIC DECK (Superstructure / Hatches)
    # ==============================================================================
    DECK_W = 0.9  # Half-width
    DECK_Z_TOP = 2.4
    
    # Longitudinal deck casing tracking the length of the cylinder
    add_box_mesh(lines, 'C_DECK', HULL_REAR_X+1.0, HULL_FRONT_X-1.0, -DECK_W, DECK_W, R_HULL-0.1, DECK_Z_TOP, div=5)
    
    # Conical Access Hatches (Fore and Aft Conning Trunks)
    add_cylinder(lines, 'C_HARDWARE', cx=HULL_FRONT_X-2.5, cy=0.0, cz=DECK_Z_TOP, length=0.6, radius=0.45, axis='z', rings=3, t_count=12)
    add_cylinder(lines, 'C_HARDWARE', cx=HULL_REAR_X+2.5, cy=0.0, cz=DECK_Z_TOP, length=0.6, radius=0.45, axis='z', rings=3, t_count=12)

    # ==============================================================================
    # 4. VENTRAL BALLAST & BATTERY KEEL
    # ==============================================================================
    KEEL_W = 0.6
    KEEL_Z_BOT = -2.6
    KEEL_START_X = HULL_REAR_X + 1.5
    KEEL_END_X = HULL_FRONT_X - 1.5
    
    # Main heavy ballast extrusion locking the low centre of gravity
    add_box_mesh(lines, 'C_KEEL', KEEL_START_X, KEEL_END_X, -KEEL_W, KEEL_W, KEEL_Z_BOT, -R_HULL+0.1, div=5)
    
    # Impact skids/landing rails
    append_segmented(lines, 'C_HARDWARE', [KEEL_START_X, KEEL_END_X], [-KEEL_W-0.1, -KEEL_W-0.1], [KEEL_Z_BOT, KEEL_Z_BOT])
    append_segmented(lines, 'C_HARDWARE', [KEEL_START_X, KEEL_END_X], [KEEL_W+0.1, KEEL_W+0.1], [KEEL_Z_BOT, KEEL_Z_BOT])

    # ==============================================================================
    # 5. PLEUGER PROPULSION PODS & THRUSTERS
    # ==============================================================================
    # 4x steerable pods externally mounted on heavy struts, strictly decoupled from the main hull
    POD_OFFSET_X_FWD = HULL_FRONT_X - 2.5
    POD_OFFSET_X_AFT = HULL_REAR_X + 2.5
    POD_OFFSET_Y = 2.4
    POD_Z = 0.0
    POD_R = 0.35
    POD_L = 1.4

    for cx_pod in [POD_OFFSET_X_FWD, POD_OFFSET_X_AFT]:
        # Outboard electric motor housings
        add_cylinder(lines, 'C_MOTORS', cx=cx_pod, cy=POD_OFFSET_Y, cz=POD_Z, length=-POD_L, radius=POD_R, axis='x', rings=4, t_count=12)
        add_cylinder(lines, 'C_MOTORS', cx=cx_pod, cy=-POD_OFFSET_Y, cz=POD_Z, length=-POD_L, radius=POD_R, axis='x', rings=4, t_count=12)
        
        # Heavy mounting struts penetrating the main hull
        # Starboard
        append_segmented(lines, 'C_HARDWARE', [cx_pod-0.5, cx_pod-0.5], [R_HULL, POD_OFFSET_Y], [POD_Z, POD_Z])
        append_segmented(lines, 'C_HARDWARE', [cx_pod-1.0, cx_pod-1.0], [R_HULL, POD_OFFSET_Y], [POD_Z, POD_Z])
        # Port
        append_segmented(lines, 'C_HARDWARE', [cx_pod-0.5, cx_pod-0.5], [-R_HULL, -POD_OFFSET_Y], [POD_Z, POD_Z])
        append_segmented(lines, 'C_HARDWARE', [cx_pod-1.0, cx_pod-1.0], [-R_HULL, -POD_OFFSET_Y], [POD_Z, POD_Z])

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_ben_franklin_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry flawlessly at the absolute geometrical midpoint
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.0
        
        # Starts explicitly from 115-degrees (Dramatic aesthetic showcasing the forward hemispherical viewports & struts)
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
    # Anchor Centroid = Z=0.0m. Extents rigidly track ~ +/- 7.4m longitudinally (14.8m LOA).
    # Setting cam_span strictly to 9.5 locks horizontal width symmetrically across a 19.0m view.
    # Vertical bounds compute to 9.5 * 1.777 = 16.88m half-height (total transparent window 33.7m).
    # Entire 14.8-metre submerged footprint perfectly trapped inside the unoccluded viewing volume during full 90-degree broadside.
    cam_span = 9.5
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_KEEL',      C_KEEL,      1.2, 1.0),
        ('C_HULL',      C_HULL,      1.4, 1.0),
        ('C_DECK',      C_DECK,      1.3, 1.0),
        ('C_HARDWARE',  C_HARDWARE,  1.2, 1.0),
        ('C_MOTORS',    C_MOTORS,    1.5, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to parse the dorsal decking blocks and the external motor arrangements
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-452x // MACRO-ENGINEERING TENSOR: MARITIME KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // GRUMMAN BEN FRANKLIN (PX-15) MESOSCAPHE", color=C_HULL, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_MOTORS, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: 14.8M CYLINDRICAL VESSEL / 4x PLEUGER PODS / BALLAST KEEL", color=C_DECK, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-452x: BEN FRANKLIN (PX-15) TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Maritime Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
