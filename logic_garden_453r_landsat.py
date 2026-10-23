"""
PROJECT: Logic Garden 453r (Exact Physical Construct // Landsat 1-3 Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: LANDSAT, ERTS-1, SATELLITE, NASA, GLB, WIREFRAME, KINEMATICS, PYTHON
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional 4m orbital scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: 18-Bay Sensory Ring, V-Strut Truss, Hexagonal ACS, RBV/MSS Payloads, Solar Paddles.
- Procedural Topography: High-density mesh mirroring physical Nimbus-bus constraints.
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
OUT_DIR = "frames_453r_landsat"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Orbital Tracking Grid)

C_HULL      = '#94A3B8'          # Slate Aluminium (Hexagonal ACS Upper Module)
C_RING      = '#334155'          # Heavy Slate (18-Bay Modular Sensory Ring)
C_SOLAR     = '#005599'          # Deep Marine (Transverse Tracking Solar Paddles)
C_TRUSS     = '#1E293B'          # Carbon Slate (Triangulated Load-Bearing Struts)
C_PAYLOAD   = '#CA8A04'          # Kapton Gold (MSS & RBV Nadir Instruments)

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
# GEOMETRIC PRIMITIVES
# ------------------------------------------------------------------
def add_quad_mesh(lines_dict, col, p1, p2, p3, p4, u_steps=4, v_steps=4, reflect_y=True):
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

def add_box_mesh(lines_dict, col, x1, x2, y1, y2, z1, z2, div=3, reflect_y=False):
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
        if axis == 'x':  
            ix, iy, iz = np.full_like(t, cx + s), cy + radius*np.cos(t), cz + radius*np.sin(t)
        elif axis == 'y':
            ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + s), cz + radius*np.sin(t)
        else:            
            ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), np.full_like(t, cz + s)
            
        if reflect_y: append_sym(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
        else: append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
        
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        if axis == 'x':  sx, sy, sz = cx + steps, [cy + radius*np.cos(a)]*rings, [cz + radius*np.sin(a)]*rings
        elif axis == 'y':sx, sy, sz = [cx + radius*np.cos(a)]*rings, cy + steps, [cz + radius*np.sin(a)]*rings
        else:            sx, sy, sz = [cx + radius*np.cos(a)]*rings, [cy + radius*np.sin(a)]*rings, cz + steps
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
# SUPERSTRUCTURE BUILDERS (LANDSAT 1-3)
# ------------------------------------------------------------------
def generate_landsat_static():
    lines = {
        'C_HULL': [], 'C_RING': [], 'C_SOLAR': [],
        'C_TRUSS': [], 'C_PAYLOAD': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. ORBITAL TRACKING BASEPLATE (Simulation Space)
    # ==============================================================================
    # Safely clearing the nadir sensory payload modules
    Z_FLOOR = -2.0
    for r_p in [1.5, 3.0, 4.5]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-4.5, 4.5, 13)
    gy_range = np.linspace(-4.5, 4.5, 13)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. 18-BAY SENSORY RING (The Nimbus Bus Foundation)
    # ==============================================================================
    R_OUTER = 0.75
    R_INNER = 0.55
    Z_RING_BOT = 0.0
    Z_RING_TOP = 0.4
    
    # Executing exactly 18 segments to map the true physical hardware bays natively
    add_cylinder(lines, 'C_RING', cx=0.0, cy=0.0, cz=Z_RING_BOT, length=(Z_RING_TOP - Z_RING_BOT), radius=R_OUTER, axis='z', rings=2, t_count=18, reflect_y=False)
    add_cylinder(lines, 'C_RING', cx=0.0, cy=0.0, cz=Z_RING_BOT, length=(Z_RING_TOP - Z_RING_BOT), radius=R_INNER, axis='z', rings=2, t_count=18, reflect_y=False)
    
    # Cap Plates locking the inner and outer bays
    t18 = np.linspace(0, 2*np.pi, 18, endpoint=False)
    for t in t18:
        cx_o, cy_o = R_OUTER * np.cos(t), R_OUTER * np.sin(t)
        cx_i, cy_i = R_INNER * np.cos(t), R_INNER * np.sin(t)
        append_segmented(lines, 'C_RING', [cx_i, cx_o], [cy_i, cy_o], [Z_RING_BOT, Z_RING_BOT])
        append_segmented(lines, 'C_RING', [cx_i, cx_o], [cy_i, cy_o], [Z_RING_TOP, Z_RING_TOP])

    # ==============================================================================
    # 3. NADIR INSTRUMENT SUITE (MSS & RBV MODULES)
    # ==============================================================================
    # Multispectral Scanner (MSS) Box directly traversing the Earth-facing plane
    add_box_mesh(lines, 'C_PAYLOAD', 0.1, 0.6, -0.25, 0.25, -0.4, 0.0, div=3, reflect_y=False)
    
    # Return Beam Vidicon (RBV) Three-Camera Array
    # Arrays sit grouped adjacently for simultaneous three-band exposure
    for y_cam in [-0.25, 0.0, 0.25]:
        add_cylinder(lines, 'C_PAYLOAD', cx=-0.35, cy=y_cam, cz=-0.4, length=0.4, radius=0.08, axis='z', rings=3, t_count=12, reflect_y=False)

    # ==============================================================================
    # 4. ATTITUDE CONTROL SYSTEM (ACS) & V-STRUT TRUSS
    # ==============================================================================
    Z_ACS_BOT = 1.6
    Z_ACS_TOP = 2.8
    R_ACS = 0.45
    
    # The Triangulated Space Frame Struts connecting the Sensory Ring to the ACS
    t6_base = np.linspace(0, 2*np.pi, 6, endpoint=False) + np.pi/6 # Offset mounting
    t6_top = np.linspace(0, 2*np.pi, 6, endpoint=False) # Hexagonal vertices
    
    for i in range(6):
        pt_top = (R_ACS * np.cos(t6_top[i]), R_ACS * np.sin(t6_top[i]), Z_ACS_BOT)
        pt_b1 = (0.65 * np.cos(t6_base[i]), 0.65 * np.sin(t6_base[i]), Z_RING_TOP)
        pt_b2 = (0.65 * np.cos(t6_base[(i-1)%6]), 0.65 * np.sin(t6_base[(i-1)%6]), Z_RING_TOP)
        
        append_segmented(lines, 'C_TRUSS', [pt_top[0], pt_b1[0]], [pt_top[1], pt_b1[1]], [pt_top[2], pt_b1[2]])
        append_segmented(lines, 'C_TRUSS', [pt_top[0], pt_b2[0]], [pt_top[1], pt_b2[1]], [pt_top[2], pt_b2[2]])

    # Hexagonal ACS Housing Matrix (Native t_count=6 forces absolute hexagonal prism)
    add_cylinder(lines, 'C_HULL', cx=0.0, cy=0.0, cz=Z_ACS_BOT, length=(Z_ACS_TOP - Z_ACS_BOT), radius=R_ACS, axis='z', rings=5, t_count=6, reflect_y=False)
    
    # Capping the ACS Module natively
    for t in t6_top:
        cx_t, cy_t = R_ACS * np.cos(t), R_ACS * np.sin(t)
        append_segmented(lines, 'C_HULL', [0.0, cx_t], [0.0, cy_t], [Z_ACS_BOT, Z_ACS_BOT])
        append_segmented(lines, 'C_HULL', [0.0, cx_t], [0.0, cy_t], [Z_ACS_TOP, Z_ACS_TOP])

    # Command / Telemetry Antenna array crowning the structure
    add_cylinder(lines, 'C_TRUSS', cx=0.0, cy=0.0, cz=Z_ACS_TOP, length=0.4, radius=0.04, axis='z', rings=2, t_count=8, reflect_y=False)
    add_cone_frustum(lines, 'C_HULL', cx=0.0, cy=0.0, cz=Z_ACS_TOP+0.4, dz=0.15, r1=0.04, r2=0.25, axis='z', rings=2, t_count=12, reflect_y=False)
    add_cone_frustum(lines, 'C_HULL', cx=0.0, cy=0.0, cz=Z_ACS_TOP+0.55, dz=0.25, r1=0.25, r2=0.02, axis='z', rings=3, t_count=12, reflect_y=False)

    # ==============================================================================
    # 5. TRANSVERSE SOLAR PADDLES (TRACKING MATRICES)
    # ==============================================================================
    # Rigid deployment angled at 35 degrees to accurately intersect the thermodynamic plane
    SAW_Z_ROOT = 2.2
    SAW_PITCH = np.radians(35)
    cp = np.cos(SAW_PITCH)
    sp = np.sin(SAW_PITCH)
    X_EXT = 0.5
    Y_START = 0.6
    Y_END = 2.0
    
    # Solar Drive Motor Booms
    append_segmented(lines, 'C_TRUSS', [0.0, 0.0], [-Y_START, Y_START], [SAW_Z_ROOT, SAW_Z_ROOT])
    
    # Port / Starboard Deep Marine Arrays (Photovoltaic Field Grid)
    # Applying the pitch transforms natively to the geometrical corners
    p1 = (-X_EXT * cp, Y_START, SAW_Z_ROOT - X_EXT * sp)
    p2 = ( X_EXT * cp, Y_START, SAW_Z_ROOT + X_EXT * sp)
    p3 = ( X_EXT * cp, Y_END,   SAW_Z_ROOT + X_EXT * sp)
    p4 = (-X_EXT * cp, Y_END,   SAW_Z_ROOT - X_EXT * sp)
    add_quad_mesh(lines, 'C_SOLAR', p1, p2, p3, p4, u_steps=4, v_steps=12, reflect_y=True)
    
    # Underside Panel Thickness
    p1_b = (-X_EXT * cp, Y_START, SAW_Z_ROOT - 0.03 - X_EXT * sp)
    p2_b = ( X_EXT * cp, Y_START, SAW_Z_ROOT - 0.03 + X_EXT * sp)
    p3_b = ( X_EXT * cp, Y_END,   SAW_Z_ROOT - 0.03 + X_EXT * sp)
    p4_b = (-X_EXT * cp, Y_END,   SAW_Z_ROOT - 0.03 - X_EXT * sp)
    add_quad_mesh(lines, 'C_SOLAR', p1_b, p2_b, p3_b, p4_b, u_steps=4, v_steps=12, reflect_y=True)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_landsat_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry explicitly amidst the V-Strut structural truss
        cam_x, cam_y, cam_z = 0.0, 0.0, 1.2
        
        # Starts explicitly from 115-degrees (Dramatic aesthetic exposing the pitched solar wings and asymmetric payloads)
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
    # Anchor Centroid = Z=1.2m. Extents rigidly track to Z=-0.4m (Cameras) and Z=+3.6m (Antenna). 
    # Transversally, the solar paddles reach Y=+/- 2.0m.
    # Setting cam_span strictly to 3.2 locks horizontal width symmetrically across a 6.4m geometrical span.
    # Vertical bounds output 3.2 * 1.777 = 5.68m half-height (total transparent window 11.36m).
    # Perfectly traps the extreme high-gain antenna components and wide solar arrays safely inside the viewport.
    cam_span = 3.2
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_TRUSS',     C_TRUSS,     1.2, 1.0),
        ('C_RING',      C_RING,      1.4, 1.0),
        ('C_HULL',      C_HULL,      1.3, 1.0),
        ('C_PAYLOAD',   C_PAYLOAD,   1.5, 1.0),
        ('C_SOLAR',     C_SOLAR,     1.6, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to distinctly parse the difference between the empty truss volume and solid modular bays
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-453r // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // LANDSAT 1, 2 & 3 (ERTS MISSION)", color=C_HULL, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_SOLAR, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: 18-BAY SENSORY RING / HEXAGONAL ACS / RBV & MSS PAYLOAD / PITCHED SAWS", color=C_PAYLOAD, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-453r: LANDSAT 1-3 TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
