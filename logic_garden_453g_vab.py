"""
PROJECT: Logic Garden 453g (Exact Physical Construct // Vehicle Assembly Building Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: VAB, KENNEDY SPACE CENTER, NASA, ARCHITECTURE, GLB, WIREFRAME, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional massive-scale architecture.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: 160m High Bay, 64m Low Bay, 4x Inverted-T Doors, Crawlerway Tracks.
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
OUT_DIR = "frames_453g_vab"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Terrestrial Tracking Grid & Crawlerways)

C_HIGHBAY   = '#334155'          # Heavy Slate (160m Primary Assembly Tower envelope)
C_LOWBAY    = '#94A3B8'          # Slate Aluminium (64m Secondary Processing Bays)
C_DOORS     = '#1E293B'          # Carbon Slate (139m Inverted-T Assembly Doors)
C_DETAILS   = '#005599'          # Deep Marine (Abstract Insignia & Flag Boundaries)
C_ROOF      = '#0F172A'          # Abyssal Slate (Roof HVAC & Infrastructure Nodes)

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
    # The VAB exhibits absolute mirroring across the longitudinal North-South (Y) axis
    if any(abs(x) > 0.001 for x in xs):
        append_segmented(lines_dict, key, [-x for x in xs], ys, zs)

# ------------------------------------------------------------------
# GEOMETRIC PRIMITIVES
# ------------------------------------------------------------------
def add_quad_mesh(lines_dict, col, p1, p2, p3, p4, u_steps=4, v_steps=4, reflect_x=False):
    p1, p2, p3, p4 = map(np.array, (p1, p2, p3, p4))
    for i in range(v_steps + 1):
        v = i / v_steps
        start = p1 * (1-v) + p4 * v
        end   = p2 * (1-v) + p3 * v
        pts = [start * (1-u) + end * u for u in np.linspace(0, 1, u_steps+1)]
        if reflect_x:
            append_sym(lines_dict, col, [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts])
        else:
            append_segmented(lines_dict, col, [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts])
    for i in range(u_steps + 1):
        u = i / u_steps
        start = p1 * (1-u) + p2 * u
        end   = p4 * (1-u) + p3 * u
        pts = [start * (1-v) + end * v for v in np.linspace(0, 1, v_steps+1)]
        if reflect_x:
            append_sym(lines_dict, col, [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts])
        else:
            append_segmented(lines_dict, col, [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts])

def add_box_mesh(lines_dict, col, x1, x2, y1, y2, z1, z2, div=4, reflect_x=False):
    add_quad_mesh(lines_dict, col, (x1, y1, z1), (x2, y1, z1), (x2, y2, z1), (x1, y2, z1), div, div, reflect_x)
    add_quad_mesh(lines_dict, col, (x1, y1, z2), (x2, y1, z2), (x2, y2, z2), (x1, y2, z2), div, div, reflect_x)
    add_quad_mesh(lines_dict, col, (x1, y1, z1), (x2, y1, z1), (x2, y1, z2), (x1, y1, z2), div, div, reflect_x)
    add_quad_mesh(lines_dict, col, (x1, y2, z1), (x2, y2, z1), (x2, y2, z2), (x1, y2, z2), div, div, reflect_x)
    add_quad_mesh(lines_dict, col, (x1, y1, z1), (x1, y2, z1), (x1, y2, z2), (x1, y1, z2), div, div, reflect_x)
    add_quad_mesh(lines_dict, col, (x2, y1, z1), (x2, y2, z1), (x2, y2, z2), (x2, y1, z2), div, div, reflect_x)

def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='z', rings=4, t_count=16, reflect_x=False):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, length, rings)
    for s in steps:
        if axis == 'x':  
            ix, iy, iz = np.full_like(t, cx + s), cy + radius*np.cos(t), cz + radius*np.sin(t)
        elif axis == 'y':
            ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + s), cz + radius*np.sin(t)
        else:            
            ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), np.full_like(t, cz + s)
            
        if reflect_x: append_sym(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
        else: append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
        
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        if axis == 'x':  sx, sy, sz = cx + steps, [cy + radius*np.cos(a)]*rings, [cz + radius*np.sin(a)]*rings
        elif axis == 'y':sx, sy, sz = [cx + radius*np.cos(a)]*rings, cy + steps, [cz + radius*np.sin(a)]*rings
        else:            sx, sy, sz = [cx + radius*np.cos(a)]*rings, [cy + radius*np.sin(a)]*rings, cz + steps
        if reflect_x: append_sym(lines_dict, col, sx, sy, sz)
        else: append_segmented(lines_dict, col, sx, sy, sz)

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (VEHICLE ASSEMBLY BUILDING)
# ------------------------------------------------------------------
def generate_vab_static():
    lines = {
        'C_HIGHBAY': [], 'C_LOWBAY': [], 'C_DOORS': [],
        'C_DETAILS': [], 'C_ROOF': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. MACRO-ENGINEERING TRACKING BASEPLATE (1 Unit = 1 Metre)
    # ==============================================================================
    # Capturing the expansive terrestrial footprint at Launch Complex 39
    Z_FLOOR = 0.0
    for r_p in [40.0, 80.0, 120.0, 160.0]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-160.0, 160.0, 33)
    gy_range = np.linspace(-160.0, 160.0, 33)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. MAIN TOWER (THE HIGH BAY ARCHITECTURE)
    # ==============================================================================
    # Architectural dimensions: 158m span (X-axis), 124m depth (Y-axis), 160m vertical (Z-axis).
    HB_X = 79.0     # Half-width
    HB_Y_FWD = 124.0
    HB_Y_AFT = 0.0
    HB_Z = 160.0
    
    # Executing the primary multi-segmented box mesh mapping the corrugated steel topography
    add_box_mesh(lines, 'C_HIGHBAY', -HB_X, HB_X, HB_Y_AFT, HB_Y_FWD, Z_FLOOR, HB_Z, div=10, reflect_x=False)

    # ==============================================================================
    # 3. SECONDARY ANNEX (THE LOW BAY ARCHITECTURE)
    # ==============================================================================
    # Attaches cleanly to the South (Aft Y) face. Reaches Y = -94.0.
    LB_X = 42.0     # Half-width
    LB_Y_FWD = 0.0
    LB_Y_AFT = -94.0
    LB_Z = 64.0
    
    add_box_mesh(lines, 'C_LOWBAY', -LB_X, LB_X, LB_Y_AFT, LB_Y_FWD, Z_FLOOR, LB_Z, div=6, reflect_x=False)

    # ==============================================================================
    # 4. EXPLICIT MACRO-FEATURES (HIGH BAY DOOR MATRICES)
    # ==============================================================================
    # NASA operates four massive 139m tall inverted-T doors facing East and West (X-Planes)
    DOOR_HEIGHT = 139.0
    DOOR_BASE_H = 35.0
    DOOR_BASE_W = 23.0  # Half-width of base (46m total)
    DOOR_SLOT_W = 11.0  # Half-width of upper slot (22m total)
    
    # Door positions natively offset on the primary structural sides
    Y_BAY_1_3 = 31.0
    Y_BAY_2_4 = 93.0
    
    for face_x in [-HB_X, HB_X]:     # Both East (+X) and West (-X) Faces
        for center_y in [Y_BAY_1_3, Y_BAY_2_4]: 
            # Inverted T-Base Array (Carbon Slate)
            y_base_p = center_y + DOOR_BASE_W
            y_base_m = center_y - DOOR_BASE_W
            append_segmented(lines, 'C_DOORS', [face_x, face_x], [y_base_m, y_base_p], [0, 0])
            append_segmented(lines, 'C_DOORS', [face_x, face_x], [y_base_m, y_base_m], [0, DOOR_BASE_H])
            append_segmented(lines, 'C_DOORS', [face_x, face_x], [y_base_p, y_base_p], [0, DOOR_BASE_H])
            
            # Inverted T-Slot Lateral Steps
            y_slot_p = center_y + DOOR_SLOT_W
            y_slot_m = center_y - DOOR_SLOT_W
            append_segmented(lines, 'C_DOORS', [face_x, face_x], [y_base_m, y_slot_m], [DOOR_BASE_H, DOOR_BASE_H])
            append_segmented(lines, 'C_DOORS', [face_x, face_x], [y_slot_p, y_base_p], [DOOR_BASE_H, DOOR_BASE_H])
            
            # Upper Slots Ascending to High Bay Limits
            append_segmented(lines, 'C_DOORS', [face_x, face_x], [y_slot_m, y_slot_m], [DOOR_BASE_H, DOOR_HEIGHT])
            append_segmented(lines, 'C_DOORS', [face_x, face_x], [y_slot_p, y_slot_p], [DOOR_BASE_H, DOOR_HEIGHT])
            append_segmented(lines, 'C_DOORS', [face_x, face_x], [y_slot_m, y_slot_p], [DOOR_HEIGHT, DOOR_HEIGHT])

    # ==============================================================================
    # 5. CRAWLERWAY EXTRUSIONS
    # ==============================================================================
    # Twin river-rock terrestrial tracks driving the mobile launch platforms away from the bays
    CRAWL_EXTENT = 160.0
    for cx_direct in [-1, 1]:
        for center_y in [Y_BAY_1_3, Y_BAY_2_4]:
            track_start_x = cx_direct * HB_X
            track_end_x   = cx_direct * CRAWL_EXTENT
            append_segmented(lines, 'C_GRID', [track_start_x, track_end_x], [center_y - 20.0, center_y - 20.0], [0, 0])
            append_segmented(lines, 'C_GRID', [track_start_x, track_end_x], [center_y + 20.0, center_y + 20.0], [0, 0])

    # ==============================================================================
    # 6. ABSTRACT PAINTED SUPER-GRAPHICS (FLAG & MEATBALL)
    # ==============================================================================
    # Bounding boxes representing the colossal artwork on the external cladding
    # East Face (+X)
    add_quad_mesh(lines, 'C_DETAILS', (HB_X, 52.0, 90.0), (HB_X, 72.0, 90.0), (HB_X, 72.0, 130.0), (HB_X, 52.0, 130.0), u_steps=2, v_steps=3, reflect_x=False)
    # South Face (Above Low Bay Y=0)
    add_quad_mesh(lines, 'C_DETAILS', (-15.0, 0.0, 80.0), (15.0, 0.0, 80.0), (15.0, 0.0, 120.0), (-15.0, 0.0, 120.0), u_steps=3, v_steps=3, reflect_x=False)

    # ==============================================================================
    # 7. ROOF HVAC INFRASTRUCTURE
    # ==============================================================================
    # Hard-coded engineering extraction arrays topping the 160m volume
    for rx in [-40.0, 40.0]:
        for ry in [30.0, 90.0]:
            add_box_mesh(lines, 'C_ROOF', rx-8.0, rx+8.0, ry-6.0, ry+6.0, HB_Z, HB_Z+4.0, div=2, reflect_x=False)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_vab_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry midway through the structural block
        cam_x, cam_y, cam_z = 0.0, 20.0, 60.0
        
        # Starts explicitly from 115-degrees (Dramatic aesthetic exposing the massive crawlerways and high bays)
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
    # Anchor Centroid = Z=60.0m. Z reaches maximum +160m absolute height (+100m relative). Let alone length constraints.
    # Setting cam_span strictly to 140.0 locks horizontal width symmetrically across a colossal 280.0m view.
    # Vertical bounds compute to 140.0 * 1.777 = 248.78m half-height (total transparent window 497.56m).
    # Transparent viewport bounds mathematically range from Z = -188.7m through Z = +308.7m.
    # Entire 160-metre tall, 218-metre long VAB structure is unequivocally trapped inside the unoccluded viewing volume.
    cam_span = 140.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_LOWBAY',    C_LOWBAY,    1.2, 1.0),
        ('C_HIGHBAY',   C_HIGHBAY,   1.4, 1.0),
        ('C_DOORS',     C_DOORS,     1.6, 1.0),
        ('C_DETAILS',   C_DETAILS,   1.2, 1.0),
        ('C_ROOF',      C_ROOF,      1.1, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to parse the sprawling rigid roofing limits and extending crawler networks
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-453g // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // VEHICLE ASSEMBLY BUILDING (VAB)", color=C_HIGHBAY, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_DOORS, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: 160M HIGH BAY / 4x INVERTED-T DOORS / EXTENDED CRAWLER TRACTS", color=C_LOWBAY, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-453g: VEHICLE ASSEMBLY BUILDING TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Macro-Infrastructure Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
