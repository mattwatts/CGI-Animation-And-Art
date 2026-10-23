"""
PROJECT: Logic Garden 453t (Exact Physical Construct // LISA 2006 Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: LISA, GRAVITATIONAL WAVES, SPACE OBSERVATORY, ESA, GLB, WIREFRAME, PYTHON
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional 2.7m orbital scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Flat Cylindrical Bus, 60-Degree Y-Tubes, Optical Bench, Solar Shield.
- Procedural Topography: High-density mesh mirroring unoptimised binary capture limits.
- Hotfix Integration: Strict np.full_like() propagation inside geometric primitives preventing Scalar Faults.
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
OUT_DIR = "frames_453t_lisa"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Orbital Tracking Grid)

C_HULL      = '#334155'          # Heavy Slate (Primary Cylindrical Science Bus)
C_OPTICS    = '#005599'          # Deep Marine (60-Degree Y-Tube Interferometer Telescopes)
C_SHIELD    = '#1E293B'          # Carbon Slate (Thermal Solar Array Roof Matrix)
C_THRUST    = '#CA8A04'          # Kapton Gold (Micro-Newton Thrusters & Optical Bench Core)

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
# GEOMETRIC PRIMITIVES (HOTFIXED SCALAR ITERATION FAULTS)
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

def add_box_mesh(lines_dict, col, x1, x2, y1, y2, z1, z2, div=2):
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
        if axis == 'x':  
            ix, iy, iz = np.full_like(t, cx + s), cy + radius*np.cos(t), cz + radius*np.sin(t)
        elif axis == 'y':
            ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + s), cz + radius*np.sin(t)
        else:            
            ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), np.full_like(t, cz + s)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
        
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        if axis == 'x':  sx, sy, sz = cx + steps, np.full_like(steps, cy + radius*np.cos(a)), np.full_like(steps, cz + radius*np.sin(a))
        elif axis == 'y':sx, sy, sz = np.full_like(steps, cx + radius*np.cos(a)), cy + steps, np.full_like(steps, cz + radius*np.sin(a))
        else:            sx, sy, sz = np.full_like(steps, cx + radius*np.cos(a)), np.full_like(steps, cy + radius*np.sin(a)), cz + steps
        append_segmented(lines_dict, col, sx, sy, sz)

def add_rotated_cylinder(lines_dict, col, cx, cy, cz, length, radius, yaw_deg, rings=4, t_count=16):
    # Specialized generator for the 60-degree internally canted telescope tubes
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, length, rings)
    rad = np.radians(yaw_deg)
    c_y, s_y = np.cos(rad), np.sin(rad)
    
    for s in steps:
        # Standard projection along X
        ux = np.full_like(t, s)
        uy = radius * np.cos(t)
        uz = radius * np.sin(t)
        # Apply Yaw (Z-axis rotation)
        rx = ux * c_y - uy * s_y
        ry = ux * s_y + uy * c_y
        append_segmented(lines_dict, col, list(cx+rx)+[cx+rx[0]], list(cy+ry)+[cy+ry[0]], list(cz+uz)+[cz+uz[0]])
        
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        ux = steps
        uy = np.full_like(steps, radius * np.cos(a))
        uz = np.full_like(steps, radius * np.sin(a))
        rx = ux * c_y - uy * s_y
        ry = ux * s_y + uy * c_y
        append_segmented(lines_dict, col, cx+rx, cy+ry, cz+uz)

def add_disk(lines_dict, col, cx, cy, cz, radius, rings=4, t_count=32):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    r_steps = np.linspace(0.1, radius, rings)
    
    for r in r_steps:
        ix = cx + r * np.cos(t)
        iy = cy + r * np.sin(t)
        iz = np.full_like(t, cz)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
        
    for a in np.linspace(0, 2*np.pi, t_count, endpoint=False):
        sx = cx + r_steps * np.cos(a)
        sy = cy + r_steps * np.sin(a)
        sz = np.full_like(r_steps, cz)
        append_segmented(lines_dict, col, sx, sy, sz)

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (LISA 2006 SPACECRAFT)
# ------------------------------------------------------------------
def generate_lisa_static():
    lines = {
        'C_HULL': [], 'C_OPTICS': [], 'C_SHIELD': [],
        'C_THRUST': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. ORBITAL TRACKING BASEPLATE (Simulation Space)
    # ==============================================================================
    Z_FLOOR = -1.2
    for r_p in [1.5, 3.0, 4.5]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-4.5, 4.5, 13)
    gy_range = np.linspace(-4.5, 4.5, 13)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. SPACECRAFT BUS (The Cylindrical Science Module)
    # ==============================================================================
    R_BUS = 1.35   # 2.7m total diameter
    Z_BUS_BOT = -0.4
    Z_BUS_TOP = 0.4
    
    # Natively calculating the primary external bulkhead 
    add_cylinder(lines, 'C_HULL', cx=0.0, cy=0.0, cz=Z_BUS_BOT, length=(Z_BUS_TOP - Z_BUS_BOT), radius=R_BUS, axis='z', rings=4, t_count=36)
    
    # Aft structural closure plate (ventral deck)
    add_disk(lines, 'C_HULL', cx=0.0, cy=0.0, cz=Z_BUS_BOT, radius=R_BUS, rings=4, t_count=36)
    
    # Aft mating / interface ring (separates Science Module from Launch Assembly)
    add_cylinder(lines, 'C_HULL', cx=0.0, cy=0.0, cz=-0.5, length=0.1, radius=0.8, axis='z', rings=2, t_count=24)

    # ==============================================================================
    # 3. Y-TUBE INTERFEROMETER (The Optical Bench Payload)
    # ==============================================================================
    # The gravitational logic: Two 40cm aperture telescopes perfectly tracking inter-satellite distances
    # Fixed at precisely 60 degrees apart from the central proof-mass node
    
    # Kapton Gold Central Optical Bench (Extremely dense zero-thermal-expansion core)
    add_box_mesh(lines, 'C_THRUST', -0.3, 0.3, -0.3, 0.3, -0.2, 0.2, div=3)
    
    # Telescope 1 (+30 Degrees off major axis)
    add_rotated_cylinder(lines, 'C_OPTICS', cx=0.0, cy=0.0, cz=0.0, length=1.2, radius=0.2, yaw_deg=30, rings=6, t_count=20)
    # Telescope 2 (-30 Degrees off major axis, yielding the precise 60-degree intersection)
    add_rotated_cylinder(lines, 'C_OPTICS', cx=0.0, cy=0.0, cz=0.0, length=1.2, radius=0.2, yaw_deg=-30, rings=6, t_count=20)

    # ==============================================================================
    # 4. THERMAL SHIELD & SOLAR ARRAY (Dorsal Architecture)
    # ==============================================================================
    # Sits perfectly atop the bus to physically decouple stellar radiation
    R_SHIELD = 1.4
    Z_SHIELD_BOT = 0.42
    Z_SHIELD_TOP = 0.45
    
    # Underside barrier
    add_disk(lines, 'C_SHIELD', cx=0.0, cy=0.0, cz=Z_SHIELD_BOT, radius=R_SHIELD, rings=5, t_count=36)
    # Upper Photovoltaic Plane
    add_disk(lines, 'C_SHIELD', cx=0.0, cy=0.0, cz=Z_SHIELD_TOP, radius=R_SHIELD, rings=5, t_count=36)
    # Edge banding
    add_cylinder(lines, 'C_SHIELD', cx=0.0, cy=0.0, cz=Z_SHIELD_BOT, length=(Z_SHIELD_TOP - Z_SHIELD_BOT), radius=R_SHIELD, axis='z', rings=2, t_count=36)

    # ==============================================================================
    # 5. MICRO-NEWTON THRUSTER MANIFOLDS
    # ==============================================================================
    # 6-point Kapton Gold manifolds resolving continuous solar pressure torque 
    t6 = np.linspace(0, 2*np.pi, 6, endpoint=False)
    for ang in t6:
        tx = R_BUS * np.cos(ang)
        ty = R_BUS * np.sin(ang)
        yaw_deg = np.degrees(ang)
        # Manifolds projecting radically outwards strictly on the horizontal plane
        add_rotated_cylinder(lines, 'C_THRUST', cx=tx, cy=ty, cz=0.0, length=0.15, radius=0.1, yaw_deg=yaw_deg, rings=2, t_count=8)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_lisa_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry precisely at the Optical Bench center
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.0
        
        # Starts explicitly from 115-degrees (Dramatic aesthetic exposing the top thermal shield and 60-degree Y tubes internally)
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
    # Anchor Centroid = Z=0.0m. Extents track outwards dynamically. Max radius is the thermal shield (1.4m) + thrusters (0.15m) = 1.55m.
    # Setting cam_span strictly to 2.2 locks horizontal width symmetrically across a 4.4m geometrical span.
    # Vertical bounds output 2.2 * 1.777 = 3.9m half-height (total transparent window 7.8m).
    # Bounds reliably clear the massive flat disk observatory parameters effortlessly.
    # Entire complex is physically trapped inside the unoccluded viewing volume.
    cam_span = 2.2
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_HULL',      C_HULL,      1.2, 1.0),
        ('C_OPTICS',    C_OPTICS,    1.5, 1.0),
        ('C_THRUST',    C_THRUST,    1.4, 1.0),
        ('C_SHIELD',    C_SHIELD,    1.6, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to parse the exact dorsal disc layout against the hollow internal optics
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-453t // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // LISA 2006 (GRAVITATIONAL WAVE OBSERVATORY)", color=C_HULL, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_OPTICS, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: FLAT CYLINDRICAL BUS / 60-DEGREE Y-TELESCOPES / THERMAL SHIELD", color=C_SHIELD, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-453t: LISA 2006 SPACECRAFT TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
