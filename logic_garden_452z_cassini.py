"""
PROJECT: Logic Garden 452z (Exact Physical Construct // Cassini-Huygens Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: CASSINI, HUYGENS, SATURN, NASA, ESA, GLB, WIREFRAME, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional deep-space scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Upper/Lower Bus, 4.0m HGA Parabola, Huygens Probe, 11m Magnetometer Boom.
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
OUT_DIR = "frames_452z_cassini"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Interplanetary Tracking Grid)

C_BUS       = '#CA8A04'          # Kapton Gold (Upper/Lower Equipment Module MLI)
C_HGA       = '#94A3B8'          # Slate Aluminium (4.0m High-Gain Antenna)
C_PROBE     = '#334155'          # Heavy Slate (Huygens Titan Atmospheric Entry Probe)
C_BOOM      = '#005599'          # Deep Marine (11.0m Magnetometer Truss)
C_RTG       = '#1E293B'          # Carbon Slate (Radioisotope Thermoelectric Generators)
C_ENGINE    = '#E11D48'          # Kinematic Red (Twin R-4D Main Bipropellant Engines)
C_HARDWARE  = '#0F172A'          # Abyssal Slate (Science Pallets & Structural Rings)

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
    # Reflect mapping strictly for symmetrical arrays (e.g. parabolas, straight structural limbs)
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
        if axis == 'x':  ix, iy, iz = np.full_like(t, cx + s), cy + radius*np.cos(t), np.full_like(t, cz + radius*np.sin(t)) if cz == 0 else cz + radius*np.sin(t)
        elif axis == 'y':ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + s), np.full_like(t, cz + radius*np.sin(t)) if cz == 0 else cz + radius*np.sin(t)
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
        if axis == 'x':  
            ix, iy, iz = np.full_like(t, cx + s), cy + r*np.cos(t), np.full_like(t, cz + r*np.sin(t)) if cz == 0 else cz + r*np.sin(t)
        elif axis == 'y':
            ix, iy, iz = cx + r*np.cos(t), np.full_like(t, cy + s), np.full_like(t, cz + r*np.sin(t)) if cz == 0 else cz + r*np.sin(t)
        else:            
            ix, iy, iz = cx + r*np.cos(t), cy + r*np.sin(t), np.full_like(t, cz + s)
        append_sym(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        sx, sy, sz = [], [], []
        for i, s in enumerate(steps):
            r = r_step[i]
            if axis == 'x':  sx.append(cx + s); sy.append(cy + r*np.cos(a)); sz.append(cz + r*np.sin(a))
            elif axis == 'y':sx.append(cx + r*np.cos(a)); sy.append(cy + s); sz.append(cz + r*np.sin(a))
            else:            sx.append(cx + r*np.cos(a)); sy.append(cy + r*np.sin(a)); sz.append(cz + s)
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
# SUPERSTRUCTURE BUILDERS (CASSINI-HUYGENS)
# ------------------------------------------------------------------
def generate_cassini_static():
    lines = {
        'C_BUS': [], 'C_HGA': [], 'C_PROBE': [],
        'C_BOOM': [], 'C_RTG': [], 'C_ENGINE': [], 
        'C_HARDWARE': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. INTERPLANETARY TRACKING BASEPLATE (1 Unit = 1 Metre)
    # ==============================================================================
    Z_FLOOR = -4.0
    for r_p in [4.5, 9.0, 13.5]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-13.5, 13.5, 19)
    gy_range = np.linspace(-13.5, 13.5, 19)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. CASSINI HIGH-GAIN ANTENNA (HGA)
    # ==============================================================================
    Z_HGA_BASE = 2.4
    R_DISH = 2.0  # 4.0m diameter
    FOCAL = 1.3
    
    t = np.linspace(0, 2*np.pi, 36, endpoint=False)
    r_steps = np.linspace(0.2, R_DISH, 6)
    
    # Generate true parabola (Z = R^2 / 4f)
    for r in r_steps:
        x_base = r * np.cos(t)
        y_base = r * np.sin(t)
        # HOTFIX: Force numpy array execution explicitly
        z_base = np.full_like(t, (r**2) / (4 * FOCAL) + Z_HGA_BASE)
        append_sym(lines, 'C_HGA', list(x_base)+[x_base[0]], list(y_base)+[y_base[0]], list(z_base)+[z_base[0]])
        
    for a in np.linspace(0, 2*np.pi, 16, endpoint=False):
        xl = r_steps * np.cos(a)
        yl = r_steps * np.sin(a)
        zl = np.full_like(xl, (r_steps**2) / (4 * FOCAL) + Z_HGA_BASE) if isinstance(r_steps, float) else (r_steps**2) / (4 * FOCAL) + Z_HGA_BASE
        append_sym(lines, 'C_HGA', xl, yl, zl)

    # Subreflector Quadripod Mount
    Z_SUBREF = Z_HGA_BASE + FOCAL
    add_cylinder(lines, 'C_HARDWARE', cx=0.0, cy=0.0, cz=Z_SUBREF-0.1, length=0.1, radius=0.25, axis='z', rings=2, t_count=12)
    for a in [np.pi/4, 3*np.pi/4, 5*np.pi/4, 7*np.pi/4]:
        append_segmented(lines, 'C_HGA', [R_DISH*np.cos(a), 0.25*np.cos(a)], [R_DISH*np.sin(a), 0.25*np.sin(a)], [Z_HGA_BASE+(R_DISH**2)/(4*FOCAL), Z_SUBREF])

    # ==============================================================================
    # 3. OBSERVATORY BUS (Upper & Lower Equipment Modules)
    # ==============================================================================
    Z_UPPER_TOP = 2.4
    Z_UPPER_BOT = 0.5
    R_UPPER = 1.5
    
    Z_LOWER_BOT = -2.2
    R_LOWER = 1.25
    
    # Upper Equipment Module (12-sided polygonal prism wrapping)
    add_cylinder(lines, 'C_BUS', cx=0.0, cy=0.0, cz=Z_UPPER_BOT, length=(Z_UPPER_TOP - Z_UPPER_BOT), radius=R_UPPER, axis='z', rings=5, t_count=12)
    
    # Lower Propulsion Module (Slightly narrower chassis)
    add_cylinder(lines, 'C_BUS', cx=0.0, cy=0.0, cz=Z_LOWER_BOT, length=(Z_UPPER_BOT - Z_LOWER_BOT), radius=R_LOWER, axis='z', rings=6, t_count=12)
    
    # Heavy Structural Interstage Rings
    add_cylinder(lines, 'C_HARDWARE', cx=0.0, cy=0.0, cz=Z_UPPER_BOT-0.1, length=0.2, radius=R_UPPER+0.05, axis='z', rings=2, t_count=16)

    # ==============================================================================
    # 4. HUYGENS TITAN PROBE (Side Mount)
    # ==============================================================================
    # Massive 2.7m diameter saucer bolted to the -X face of the upper module
    PROBE_X_MOUNT = -1.5
    PROBE_DZ = -1.1   # Extends outwards mapping the aeroshell (-X vector)
    PROBE_RADIUS = 1.35
    
    # Aft Cover Frustum (Mounts to bus)
    add_cone_frustum(lines, 'C_PROBE', cx=PROBE_X_MOUNT, cy=0.0, cz=0.3, dz=PROBE_DZ, r1=0.7, r2=PROBE_RADIUS, axis='x', rings=5, t_count=16)
    
    # Forward Aerodynamic Heat Shield (Ellipsoid cap pointing fully deep space)
    add_ellipsoid(lines, 'C_PROBE', cx=PROBE_X_MOUNT+PROBE_DZ, cy=0.0, cz=0.3, rx=0.25, ry=PROBE_RADIUS, rz=PROBE_RADIUS, rings=8, t_count=16, half='neg_x')

    # ==============================================================================
    # 5. RADIOISOTOPE THERMOELECTRIC GENERATORS (RTGs)
    # ==============================================================================
    # 3 massive power units bolted horizontally to the lower propulsion module
    for angle in [0, 2*np.pi/3, 4*np.pi/3]:
        # Outrigger angle offset to miss the Huygens -X shadow
        rtg_ang = angle + np.pi/6
        rx_dir, ry_dir = np.cos(rtg_ang), np.sin(rtg_ang)
        
        rtg_start_x, rtg_start_y = R_LOWER * rx_dir, R_LOWER * ry_dir
        
        # Calculate cylindrical vectors spanning radially
        # Generating manually to capture radial translation easily
        steps = np.linspace(0, 1.4, 4) # 1.4m length
        for s in steps:
            cx, cy, cz = rtg_start_x + rx_dir*s, rtg_start_y + ry_dir*s, -1.0
            t = np.linspace(0, 2*np.pi, 8, endpoint=False)
            # Normal perpendicular vectors to cap the cylinder bounds
            nx, ny = -ry_dir, rx_dir
            r_rtg = 0.25
            ring_x = cx + r_rtg * np.cos(t) * nx
            ring_y = cy + r_rtg * np.cos(t) * ny
            # HOTFIX: Force array propagation
            ring_z = np.full_like(t, cz + r_rtg * np.sin(t)) if cz == -1.0 else cz + r_rtg * np.sin(t)
            append_sym(lines, 'C_RTG', list(ring_x)+[ring_x[0]], list(ring_y)+[ring_y[0]], list(ring_z)+[ring_z[0]])
            
        for a in np.linspace(0, 2*np.pi, 8, endpoint=False):
            nx, ny = -ry_dir, rx_dir
            lx = rtg_start_x + steps*rx_dir + 0.25*np.cos(a)*nx
            ly = rtg_start_y + steps*ry_dir + 0.25*np.cos(a)*ny
            # HOTFIX: Force array propagation
            lz = np.full_like(steps, -1.0 + 0.25*np.sin(a))
            append_sym(lines, 'C_RTG', lx, ly, lz)

    # ==============================================================================
    # 6. ASYMMETRICAL 11M MAGNETOMETER BOOM
    # ==============================================================================
    # Collapsed during launch, physically extruded here reaching Y=12.2
    BOOM_START_Y = 1.3
    BOOM_EXT = 11.0
    BOOM_Z = 1.0
    
    # Heavy science truss tracking flawlessly out the extreme +Y vector
    add_cylinder(lines, 'C_BOOM', cx=0.0, cy=BOOM_START_Y, cz=BOOM_Z, length=BOOM_EXT, radius=0.15, axis='y', rings=8, t_count=8)

    # Distal Magnetometer Sensor Nodes
    add_cylinder(lines, 'C_HARDWARE', cx=0.0, cy=BOOM_START_Y + BOOM_EXT - 3.5, cz=BOOM_Z-0.1, length=0.2, radius=0.25, axis='z', rings=3, t_count=8)
    add_cylinder(lines, 'C_HARDWARE', cx=0.0, cy=BOOM_START_Y + BOOM_EXT, cz=BOOM_Z-0.1, length=0.2, radius=0.25, axis='z', rings=3, t_count=8)

    # ==============================================================================
    # 7. AFT MAIN BIPROPELLANT ENGINES
    # ==============================================================================
    # Twin R-4D nozzles tucked inside a micrometeoroid thermal skirt
    add_cylinder(lines, 'C_HARDWARE', cx=0.0, cy=0.0, cz=Z_LOWER_BOT, length=-0.4, radius=0.7, axis='z', rings=2, t_count=16)
    
    # Port / Starboard nozzles exactly spanning the aft boundary
    add_cone_frustum(lines, 'C_ENGINE', cx=-0.35, cy=0.0, cz=Z_LOWER_BOT-0.1, dz=-0.6, r1=0.1, r2=0.3, axis='z', rings=3, t_count=12)
    add_cone_frustum(lines, 'C_ENGINE', cx=0.35, cy=0.0, cz=Z_LOWER_BOT-0.1, dz=-0.6, r1=0.1, r2=0.3, axis='z', rings=3, t_count=12)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_cassini_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry flawlessly at payload centroid
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.0
        
        # Starts explicitly from 115-degrees (Dramatic aesthetic exposing the massive asymmetrical boom and Huygens)
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
    # Anchor Centroid = Dead zero. The extreme Science Boom reaches out to Y=+12.3m. 
    # Setting cam_span strictly to 13.0 locks horizontal width symmetrically across a massive 26.0m view.
    # Vertical bounds output 13.0 * 1.777 = 23.1m total height window vertically.
    # Completely traps the deeply asymmetrical space vehicle safely inside the transparent viewport, immune to UI overlay clipping.
    cam_span = 13.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_BUS',       C_BUS,       1.4, 1.0),
        ('C_RTG',       C_RTG,       1.3, 1.0),
        ('C_PROBE',     C_PROBE,     1.5, 1.0),
        ('C_BOOM',      C_BOOM,      1.3, 1.0),
        ('C_HARDWARE',  C_HARDWARE,  1.2, 1.0),
        ('C_HGA',       C_HGA,       1.6, 1.0),
        ('C_ENGINE',    C_ENGINE,    1.5, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to parse the dense lower propulsion block and the Cassegrain subreflector up top
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-452z // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // CASSINI-HUYGENS MULTI-MODULE MATRIX", color=C_BUS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_BOOM, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: 4M HGA / HUYGENS PROBE / 11M MAG BOOM / 3x RTG ARRAYS", color=C_PROBE, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-452z: CASSINI-HUYGENS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
