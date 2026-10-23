"""
PROJECT: Logic Garden 452l (Exact Physical Construct // Advanced Composition Explorer Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: ACE, SATELLITE, SOLAR WIND, GLB, WIREFRAME, ENGINEERING, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional 12.0m aerospace scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Hexagonal bus, Parabolic HGA, Radial Photovoltaic Arrays, Magnetometer Booms.
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
OUT_DIR = "frames_452l_ace"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Orbital Tracking Grid)

C_BUS       = '#CA8A04'          # Kapton Gold (Hexagonal Satellite Bus MLI)
C_PANELS    = '#005599'          # Deep Marine (Radial Photovoltaic Arrays)
C_HGA       = '#94A3B8'          # Slate Aluminium (Parabolic High-Gain Antenna)
C_INSTR     = '#475569'          # Machined Slate (Forward Deck Science Payloads)
C_BOOMS     = '#1E293B'          # Carbon Slate (Extended Magnetometer Booms)

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
# SUPERSTRUCTURE BUILDERS (Advanced Composition Explorer)
# ------------------------------------------------------------------
def generate_ace_static():
    lines = {
        'C_BUS': [], 'C_PANELS': [], 'C_HGA': [],
        'C_INSTR': [], 'C_BOOMS': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. ORBITAL TRACKING BASEPLATE (1 Unit = 1 Metre)
    # ==============================================================================
    Z_FLOOR = -2.5
    for r_p in [2.5, 5.0, 7.5]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-7.5, 7.5, 13)
    gy_range = np.linspace(-7.5, 7.5, 13)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. ACE PRIMARY HEXAGONAL BUS
    # ==============================================================================
    # 1.6m across (0.8m radius), roughly 1.0m tall (spanning Z = -0.5 to Z = +0.5)
    R_BUS = 0.8
    Z_AFT = -0.5
    Z_FWD = 0.5
    
    # Hexagonal Prism Chassis (Forced via t_count=6) covered in Kapton MLI
    add_cylinder(lines, 'C_BUS', cx=0.0, cy=0.0, cz=Z_AFT, length=(Z_FWD - Z_AFT), radius=R_BUS, axis='z', rings=5, t_count=6)

    # ==============================================================================
    # 3. HIGH-GAIN ANTENNA (HGA) & FORWARD DECK INSTRUMENTS
    # ==============================================================================
    # Central Parabolic Communications Dish mounted on the +Z forward spin axis
    # Represented strictly as a widely flared cone frustum
    add_cone_frustum(lines, 'C_HGA', cx=0.0, cy=0.0, cz=Z_FWD, dz=0.35, r1=0.1, r2=0.75, axis='z', rings=6, t_count=24)
    
    # Solar Wind and Isotope Spectrometers (SWICS/SWIMS/CRIS) - Asymmetric structural nodes
    add_cylinder(lines, 'C_INSTR', cx=0.4, cy=0.4, cz=Z_FWD, length=0.4, radius=0.2, axis='z', rings=3, t_count=8)
    add_cylinder(lines, 'C_INSTR', cx=-0.5, cy=-0.2, cz=Z_FWD, length=0.35, radius=0.15, axis='z', rings=3, t_count=8)
    add_cylinder(lines, 'C_INSTR', cx=0.0, cy=-0.6, cz=Z_FWD, length=0.25, radius=0.1, axis='z', rings=2, t_count=6)

    # ==============================================================================
    # 4. RADIAL PHOTOVOLTAIC SOLAR ARRAYS
    # ==============================================================================
    # Four panels extending radially outwards in crossed configuration
    # Span reaches out to R=4.15m per axis
    P_RAD_START = 0.9
    P_RAD_END = 4.15
    P_WIDTH = 0.4 # Half-width (Total 0.8m wide panels)
    
    # Panels along the X-Axis (+X and -X)
    for sign in [-1, 1]:
        add_quad_mesh(lines, 'C_PANELS', 
                      (P_RAD_START * sign, -P_WIDTH, 0.0), (P_RAD_END * sign, -P_WIDTH, 0.0),
                      (P_RAD_END * sign, P_WIDTH, 0.0), (P_RAD_START * sign, P_WIDTH, 0.0), 
                      u_steps=8, v_steps=3)
                      
    # Panels along the Y-Axis (+Y and -Y)
    for sign in [-1, 1]:
        add_quad_mesh(lines, 'C_PANELS', 
                      (-P_WIDTH, P_RAD_START * sign, 0.0), (P_WIDTH, P_RAD_START * sign, 0.0),
                      (P_WIDTH, P_RAD_END * sign, 0.0), (-P_WIDTH, P_RAD_END * sign, 0.0), 
                      u_steps=3, v_steps=8)

    # ==============================================================================
    # 5. MAGNETOMETER BOOMS
    # ==============================================================================
    # Delicate structural trusses extending from the extreme ends of the Y-axis solar arrays
    # Total radial distance extends out to ~6.0m per side
    BOOM_END = 6.0
    
    for sign in [-1, 1]:
        # Heavy central strut rod
        add_cylinder(lines, 'C_BOOMS', cx=0.0, cy=P_RAD_END * sign, cz=0.0, length=(BOOM_END - P_RAD_END)*sign, radius=0.04, axis='y', rings=4, t_count=6)
        # Terminal MAG sensors
        add_cylinder(lines, 'C_INSTR', cx=0.0, cy=BOOM_END * sign, cz=-0.05, length=0.1, radius=0.1, axis='z', rings=2, t_count=4)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_ace_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry flawlessly at payload centre
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.0
        
        # Starts explicitly from 115-degrees (Dramatic aesthetic exposing the massive solar arrays and offset HGA)
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
    # Anchor Centroid = Dead zero. Solar array and magnetometer boom span extends strictly to +/- 6.0 metres across Y.
    # Setting cam_span strictly to 7.5 locks horizontal width symmetrically across an immense 15.0m.
    # Vertical bounds output 7.5 * 1.777 = 13.3275m total height window vertically.
    # Completely traps the 12-metre space vehicle safely inside the transparent viewport, immune to UI overlay clipping.
    cam_span = 7.5
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_BOOMS',     C_BOOMS,     1.3, 1.0),
        ('C_BUS',       C_BUS,       1.4, 1.0),
        ('C_PANELS',    C_PANELS,    1.2, 1.0),
        ('C_HGA',       C_HGA,       1.5, 1.0),
        ('C_INSTR',     C_INSTR,     1.2, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to clearly parse the faceted hexagonal chassis, massive arrays, and forward deck
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-452l // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // ADVANCED COMPOSITION EXPLORER (ACE)", color=C_BUS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_PANELS, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: 12-METRE SPAN / HEXAGONAL BUS / RADIAL PHOTOVOLTAIC ARRAYS", color=C_HGA, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-452l: ACE TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
