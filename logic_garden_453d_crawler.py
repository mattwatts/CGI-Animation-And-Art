"""
PROJECT: Logic Garden 453d (Exact Physical Construct // Crawler-Transporter Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: CRAWLER, NASA, TRANSPORTER, KSC, GLB, WIREFRAME, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional massive-scale vehicle.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: 4x Tracked Bogies, JEL Hydraulic Rings, Main Chassis truss, Control Cabs.
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
OUT_DIR = "frames_453d_crawler"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Crawlerway Tracking Grid)

C_CHASSIS   = '#334155'          # Heavy Slate (Main Structural Frame)
C_TRACKS    = '#0F172A'          # Abyssal Slate (Track Belts & Bogie Framework)
C_JEL       = '#CA8A04'          # Kapton Gold (Jacking, Equalising, Levelling Hydraulics)
C_DECK      = '#94A3B8'          # Slate Aluminium (Top Payload Decking)
C_CABS      = '#1E293B'          # Carbon Slate (Operational Control Cabins)

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
    # Reflect mapping strictly across primary Y-axis. Crawler applies X,Y reflection natively in placement.
    if any(abs(y) > 0.001 for y in ys):
        append_segmented(lines_dict, key, xs, [-y for y in ys], zs)

# ------------------------------------------------------------------
# GEOMETRIC PRIMITIVES
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
        if axis == 'x':  ix, iy, iz = np.full_like(t, cx + s), cy + radius*np.cos(t), np.full_like(t, cz + radius*np.sin(t)) if cz == 0 else cz + radius*np.sin(t)
        elif axis == 'y':ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + s), np.full_like(t, cz + radius*np.sin(t)) if cz == 0 else cz + radius*np.sin(t)
        else:            ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), np.full_like(t, cz + s)
        if reflect_y: append_sym(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
        else: append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
        
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        if axis == 'x':  sx, sy, sz = cx + steps, [cy + radius*np.cos(a)]*rings, [cz + radius*np.sin(a)]*rings
        elif axis == 'y':sx, sy, sz = [cx + radius*np.cos(a)]*rings, cy + steps, [cz + radius*np.sin(a)]*rings
        else:            sx, sy, sz = [cx + radius*np.cos(a)]*rings, [cy + radius*np.sin(a)]*rings, cz + steps
        if reflect_y: append_sym(lines_dict, col, sx, sy, sz)
        else: append_segmented(lines_dict, col, sx, sy, sz)

def add_track_belt(lines_dict, col, cx, cy, cz, length, height, width, divisions=24):
    """ Explicity maps the massive tracked shoes as a continuous 3D loop """
    r = height / 2.0
    half_L = (length - height) / 2.0  # Straight span length
    
    # Track perimeter generation
    t_fwd = np.linspace(-np.pi/2, np.pi/2, divisions // 2 + 1)
    t_aft = np.linspace(np.pi/2, 3*np.pi/2, divisions // 2 + 1)
    
    # Outer belt profile
    belt_x = np.concatenate([cx + half_L + r * np.cos(t_fwd), cx - half_L + r * np.cos(t_aft)])
    belt_z = np.concatenate([cz + r + r * np.sin(t_fwd), cz + r + r * np.sin(t_aft)])
    
    # Draw Left and Right boundaries of the single belt
    belt_y_p = np.full_like(belt_x, cy + width/2)
    belt_y_m = np.full_like(belt_x, cy - width/2)
    
    append_segmented(lines_dict, col, list(belt_x)+[belt_x[0]], list(belt_y_p)+[belt_y_p[0]], list(belt_z)+[belt_z[0]])
    append_segmented(lines_dict, col, list(belt_x)+[belt_x[0]], list(belt_y_m)+[belt_y_m[0]], list(belt_z)+[belt_z[0]])
    
    # Draw transverse heavy steel shoes
    for i in range(len(belt_x)):
        if i % 2 == 0:  # Density control
            append_segmented(lines_dict, col, [belt_x[i], belt_x[i]], [cy - width/2, cy + width/2], [belt_z[i], belt_z[i]])

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (CRAWLER TRANSPORTER)
# ------------------------------------------------------------------
def generate_crawler_static():
    lines = {
        'C_CHASSIS': [], 'C_TRACKS': [], 'C_JEL': [],
        'C_DECK': [], 'C_CABS': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. MACRO-ENGINEERING TRACKING BASEPLATE (1 Unit = 1 Metre)
    # ==============================================================================
    Z_FLOOR = 0.0
    for r_p in [15.0, 30.0, 45.0]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-45.0, 45.0, 31)
    gy_range = np.linspace(-45.0, 45.0, 31)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. THE 4 BOGIE TRUCKS (TRACK ARRAYS)
    # ==============================================================================
    # 4 distinct corners. X = +/- 14.5m, Y = +/- 13.0m
    TRUCK_L = 12.0
    TRUCK_H = 3.0
    BELT_W = 2.0
    TRUCK_CX = 14.5
    TRUCK_CY = 13.0
    
    for sx in [-1, 1]:
        for sy in [-1, 1]:
            # Bogie Core Chassis Frame
            add_box_mesh(lines, 'C_TRACKS', sx*TRUCK_CX - 6.0, sx*TRUCK_CX + 6.0, 
                                            sy*TRUCK_CY - 3.8, sy*TRUCK_CY + 3.8, 
                                            1.5, 3.5, div=3)
            # Twin Track Belts per truck (8 belts total)
            add_track_belt(lines, 'C_TRACKS', sx*TRUCK_CX, sy*TRUCK_CY + 2.5, Z_FLOOR, TRUCK_L, TRUCK_H, BELT_W, divisions=32)
            add_track_belt(lines, 'C_TRACKS', sx*TRUCK_CX, sy*TRUCK_CY - 2.5, Z_FLOOR, TRUCK_L, TRUCK_H, BELT_W, divisions=32)

    # ==============================================================================
    # 3. J.E.L. HYDRAULIC CYLINDERS (Jacking, Equalising, Levelling)
    # ==============================================================================
    # Giant Kapton Gold geometric cylinders transmitting payload to the bogies
    Z_JEL_BOT = 3.5
    Z_JEL_TOP = 6.0
    R_JEL = 1.2
    
    for sx in [-1, 1]:
        for sy in [-1, 1]:
            add_cylinder(lines, 'C_JEL', sx*TRUCK_CX, sy*TRUCK_CY, Z_JEL_BOT, length=(Z_JEL_TOP - Z_JEL_BOT), radius=R_JEL, axis='z', rings=4, t_count=16)
            add_cylinder(lines, 'C_JEL', sx*TRUCK_CX, sy*TRUCK_CY, Z_JEL_BOT, length=-1.0, radius=R_JEL-0.2, axis='z', rings=2, t_count=12) # Lower piston joint

    # ==============================================================================
    # 4. PRIMARY CHASSIS TRUSS NETWORK
    # ==============================================================================
    # Spans roughly 40m long x 35m wide. Elevates from Z=6.0 to Z=8.0
    CHASSIS_X = 20.0
    CHASSIS_Y = 17.5
    Z_CHASSIS_BOT = 6.0
    Z_CHASSIS_TOP = 8.0
    
    add_box_mesh(lines, 'C_CHASSIS', -CHASSIS_X, CHASSIS_X, -CHASSIS_Y, CHASSIS_Y, Z_CHASSIS_BOT, Z_CHASSIS_TOP, div=10)
    
    # Inner load-bearing crossbeams
    for bx in np.linspace(-15, 15, 7):
        append_segmented(lines, 'C_CHASSIS', [bx, bx], [-CHASSIS_Y, CHASSIS_Y], [Z_CHASSIS_BOT, Z_CHASSIS_BOT])
        append_segmented(lines, 'C_CHASSIS', [bx, bx], [-CHASSIS_Y, CHASSIS_Y], [Z_CHASSIS_TOP, Z_CHASSIS_TOP])
    for by in np.linspace(-12, 12, 5):
        append_segmented(lines, 'C_CHASSIS', [-CHASSIS_X, CHASSIS_X], [by, by], [Z_CHASSIS_BOT, Z_CHASSIS_BOT])
        append_segmented(lines, 'C_CHASSIS', [-CHASSIS_X, CHASSIS_X], [by, by], [Z_CHASSIS_TOP, Z_CHASSIS_TOP])

    # ==============================================================================
    # 5. DORSAL PAYLOAD DECK (MLP Interface)
    # ==============================================================================
    # Explicit flat mounting matrix
    add_quad_mesh(lines, 'C_DECK', 
                  (-CHASSIS_X, -CHASSIS_Y, Z_CHASSIS_TOP), (CHASSIS_X, -CHASSIS_Y, Z_CHASSIS_TOP),
                  (CHASSIS_X, CHASSIS_Y, Z_CHASSIS_TOP), (-CHASSIS_X, CHASSIS_Y, Z_CHASSIS_TOP), u_steps=12, v_steps=10)

    # ==============================================================================
    # 6. DIAGONAL OPERATIONAL CABS
    # ==============================================================================
    # Cabs are positioned at opposite diagonal corners for dual-direction driving.
    # Pos 1: +X, -Y. Pos 2: -X, +Y
    CAB_W = 2.5
    CAB_L = 3.5
    CAB_Z = 8.0
    CAB_H = 2.5
    
    # Cab 1 (+X, -Y quadrant)
    add_box_mesh(lines, 'C_CABS', CHASSIS_X - 1.0, CHASSIS_X + CAB_L, -CHASSIS_Y - CAB_W, -CHASSIS_Y + 1.0, CAB_Z, CAB_Z + CAB_H, div=2)
    
    # Cab 2 (-X, +Y quadrant)
    add_box_mesh(lines, 'C_CABS', -CHASSIS_X - CAB_L, -CHASSIS_X + 1.0, CHASSIS_Y - 1.0, CHASSIS_Y + CAB_W, CAB_Z, CAB_Z + CAB_H, div=2)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_crawler_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry specifically midway up the chassis bulk
        cam_x, cam_y, cam_z = 0.0, 0.0, 4.0
        
        # Starts explicitly from 115-degrees (Dramatic aesthetic exposing the massive corner 8-track bogies)
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
    # Anchor Centroid = Z=4.0m. Diagonal footprint of the ~40x35m chassis stretches significantly.
    # Setting cam_span strictly to 32.0 locks horizontal width symmetrically across a massive 64.0m view.
    # Vertical bounds output 32.0 * 1.777 = 56.86m total height window vertically.
    # Completely traps the immense launch pad transporter safely inside the transparent viewport, immune to UI overlay clipping.
    cam_span = 32.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_CHASSIS',   C_CHASSIS,   1.2, 1.0),
        ('C_TRACKS',    C_TRACKS,    1.4, 1.0),
        ('C_JEL',       C_JEL,       1.5, 1.0),
        ('C_DECK',      C_DECK,      1.1, 1.0),
        ('C_CABS',      C_CABS,      1.6, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to parse the sprawling dense truss grid and massive footprint
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-453d // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // NASA CRAWLER-TRANSPORTER (CT)", color=C_CHASSIS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_TRACKS, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: 40M HEAVY CHASSIS / JEL CYLINDERS / 8x MASSIVE TRACK BELTS", color=C_JEL, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-453d: NASA CRAWLER-TRANSPORTER TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Macro-Infrastructure Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
