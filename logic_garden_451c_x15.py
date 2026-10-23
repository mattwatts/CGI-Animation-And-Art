"""
PROJECT: Logic Garden 451c (Exact Physical Construct // North American X-15 Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: X-15, HYPERSONIC, AEROSPACE, NASA, WIREFRAME, ENGINEERING, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Ball nose Q-ball array, heavy lateral chines, blunt-trailing wedge fins.
- Strict Bounds Protocol: Core locked at origin. cam_span scaled to 10.0 for flawless, unclipped 100% full-body framing.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from absolute 115-degree dramatic front-quarter angle.
- Daylight Palette (White Substrate / High-Contrast Edge Geometry).
- Purged Jargon. Australian spelling conventions (maths, colour, kilometres, aeroplane, re-entry, manoeuvre).
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
OUT_DIR = "frames_451c_x15"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Translating Sub-orbital Plane)

C_HULL_MAIN = '#111115'          # Indestructible Black (Inconel-X Ablative Skin)
C_HULL_DARK = '#475569'          # Machined Slate (Lateral Chines, Panel Splits)
C_WEDGE     = '#1E293B'          # Carbon Slate (Heavy Empennage Geometry)
C_DETAILS   = '#94A3B8'          # Heavy Slate (Leading Edges, Ball Nose, Landing Skids)
C_ENGINE    = '#E11D48'          # Kinematic Red (XLR99 Thrust Bell Resonance)

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

def add_sym_quad(lines_dict, col, p1, p2, p3, p4, u_steps=4, v_steps=4):
    add_quad_mesh(lines_dict, col, p1, p2, p3, p4, u_steps, v_steps)
    if any(abs(p[1]) > 0.001 for p in [p1, p2, p3, p4]):
        add_quad_mesh(lines_dict, col, (p1[0], -p1[1], p1[2]), (p2[0], -p2[1], p2[2]), 
                                       (p3[0], -p3[1], p3[2]), (p4[0], -p4[1], p4[2]), u_steps, v_steps)

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

def add_sym_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='x', rings=4, t_count=16):
    add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis, rings, t_count)
    if abs(cy) > 0.001:
        add_cylinder(lines_dict, col, cx, -cy, cz, length, radius, axis, rings, t_count)

def add_dome(lines_dict, col, cx, cy, cz, radius, axis='z', dir=1, rings=4, t_count=16):
    p_step = np.linspace(0, np.pi/2, rings)
    for p in p_step:
        r_s = radius * np.cos(p)
        h_s = radius * np.sin(p) * dir
        t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
        if axis == 'x':   ix, iy, iz = np.full_like(t, cx + h_s), cy + r_s*np.cos(t), cz + r_s*np.sin(t)
        else:             ix, iy, iz = cx + r_s*np.cos(t), cy + r_s*np.sin(t), np.full_like(t, cz + h_s)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        rr = radius * np.cos(p_step)
        hh = radius * np.sin(p_step) * dir
        if axis == 'x':   sx, sy, sz = cx + hh, cy + rr*np.cos(a), cz + rr*np.sin(a)
        else:             sx, sy, sz = cx + rr*np.cos(a), cy + rr*np.sin(a), cz + hh
        append_segmented(lines_dict, col, list(sx), list(sy), list(sz))

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (NORTH AMERICAN X-15)
# ------------------------------------------------------------------
def generate_x15_static():
    lines = {
        'C_HULL_MAIN': [], 'C_HULL_DARK': [], 'C_DETAILS': [], 
        'C_WEDGE': [], 'C_ENGINE': [], 'C_GRID': []
    }

    # 1. BASEPLATE ENVELOPE (REFERENCE GRID)
    Z_FLOOR = -4.0
    gx_range = np.linspace(-12.0, 12.0, 13)
    gy_range = np.linspace(-8.0, 8.0, 9)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # Real-world dimensions: 15.45m Length. Setup X boundaries from +7.7 (Nose) to -7.7 (Tail)
    X_TAIL = -7.7

    # ==============================================================================
    # 2. CONTINUOUS FUSELAGE LOFTING (Core Pressure Vessel)
    # ==============================================================================
    x_st = [7.6, 6.0,  5.0,  3.0,  0.0, -3.0, -6.0, X_TAIL]
    rad_b = [0.15, 0.40, 0.55, 0.65, 0.70, 0.70, 0.70, 0.65] # Base cylinder radii
    
    for i in range(len(x_st)-1):
        x1, x2 = x_st[i], x_st[i+1]
        r1, r2 = rad_b[i], rad_b[i+1]

        t = np.linspace(0, 2*np.pi, 12, endpoint=False)
        y1_ring, z1_ring = r1*np.cos(t), r1*np.sin(t)
        y2_ring, z2_ring = r2*np.cos(t), r2*np.sin(t)
        
        append_segmented(lines, 'C_HULL_MAIN', [x1]*13, list(y1_ring)+[y1_ring[0]], list(z1_ring)+[z1_ring[0]])
        for k in range(12):
            append_segmented(lines, 'C_HULL_MAIN', [x1, x2], [y1_ring[k], y2_ring[k]], [z1_ring[k], z2_ring[k]])
            
    append_segmented(lines, 'C_HULL_MAIN', [X_TAIL]*13, list(rad_b[-1]*np.cos(t))+[rad_b[-1]*np.cos(t[0])], list(rad_b[-1]*np.sin(t))+[rad_b[-1]*np.sin(t[0])])

    # ==============================================================================
    # 3. LATERAL CHINES (Equipment Fairings)
    # ==============================================================================
    # Sweeping from behind cockpit all the way to the tail edges
    x_c = [4.5,  2.0,  0.0, -3.0, -6.0, X_TAIL]
    y_c = [0.6,  0.9, 0.95, 0.95, 0.95, 0.95]
    
    for i in range(len(x_c)-1):
        # Chine top surface expanding out from pressure vessel
        add_sym_quad(lines, 'C_HULL_DARK', (x_c[i], rad_b[2]*0.8, 0.2), (x_c[i+1], rad_b[3]*0.8, 0.2), 
                                           (x_c[i+1], y_c[i+1], 0.0), (x_c[i], y_c[i], 0.0), u_steps=2, v_steps=2)
        # Chine bottom surface tucking back in
        add_sym_quad(lines, 'C_HULL_DARK', (x_c[i], rad_b[2]*0.8, -0.2), (x_c[i+1], rad_b[3]*0.8, -0.2), 
                                           (x_c[i+1], y_c[i+1], 0.0), (x_c[i], y_c[i], 0.0), u_steps=2, v_steps=2)

    # ==============================================================================
    # 4. EXTREME WEDGE EMPENNAGE (Dorsal & Ventral Structural Fins)
    # ==============================================================================
    # Top Wedge Parameters
    D_FRONT = -3.5; D_AFT = X_TAIL
    D_Z_ROOT = 0.7; D_Z_TIP = 2.4; D_Z_TIP_FWD = 2.4
    X_TIP_FWD = -6.0
    
    # Left and Right plates of the thick dorsal wedge fin
    # The trailing edge expands to Y +/- 0.15 for hypersonic stability
    add_sym_quad(lines, 'C_WEDGE', (D_FRONT, 0.02, D_Z_ROOT), (X_TIP_FWD, 0.06, D_Z_TIP_FWD), 
                                   (D_AFT, 0.15, D_Z_TIP), (D_AFT, 0.15, D_Z_ROOT), u_steps=4, v_steps=4)
    # Top closure plate
    add_sym_quad(lines, 'C_WEDGE', (X_TIP_FWD, 0.0, D_Z_TIP_FWD), (D_AFT, 0.0, D_Z_TIP), 
                                   (D_AFT, 0.15, D_Z_TIP), (X_TIP_FWD, 0.06, D_Z_TIP_FWD), u_steps=1, v_steps=3)
    # Blunt Trailing Edge
    add_sym_quad(lines, 'C_WEDGE', (D_AFT, 0.0, D_Z_TIP), (D_AFT, 0.0, D_Z_ROOT), 
                                   (D_AFT, 0.15, D_Z_ROOT), (D_AFT, 0.15, D_Z_TIP), u_steps=4, v_steps=1)

    # Bottom Ventral Wedge Fin (Symmetrical downward but steeper front sweep)
    # Blueprint distinct lower fin includes a full wedge.
    V_FRONT = -4.0; V_Z_ROOT = -0.7; V_Z_TIP = -2.4; V_Z_TIP_FWD = -2.4
    X_V_TIP_FWD = -6.5
    
    add_sym_quad(lines, 'C_WEDGE', (V_FRONT, 0.02, V_Z_ROOT), (X_V_TIP_FWD, 0.06, V_Z_TIP_FWD), 
                                   (D_AFT, 0.15, V_Z_TIP), (D_AFT, 0.15, V_Z_ROOT), u_steps=4, v_steps=4)
    add_sym_quad(lines, 'C_WEDGE', (X_V_TIP_FWD, 0.0, V_Z_TIP_FWD), (D_AFT, 0.0, V_Z_TIP), 
                                   (D_AFT, 0.15, V_Z_TIP), (X_V_TIP_FWD, 0.06, V_Z_TIP_FWD), u_steps=1, v_steps=3)
    add_sym_quad(lines, 'C_WEDGE', (D_AFT, 0.0, V_Z_TIP), (D_AFT, 0.0, V_Z_ROOT), 
                                   (D_AFT, 0.15, V_Z_ROOT), (D_AFT, 0.15, V_Z_TIP), u_steps=4, v_steps=1)
    
    # Internal Cut Line representing the jettisonable parachute/landing boundary of the bottom ventral wedge
    add_sym_quad(lines, 'C_DETAILS', (-5.8, 0.1, -1.5), (D_AFT, 0.15, -1.5), (D_AFT, 0.15, -1.45), (-5.8, 0.1, -1.45), u_steps=2, v_steps=1)

    # ==============================================================================
    # 5. STRAIGHT SHORT SPAN WINGS & ANHEDRAL TAILPLANES
    # ==============================================================================
    # Main Wings (Very far aft, heavily loaded)
    W_ROOT_FWD = -1.5; W_ROOT_AFT = -4.5
    W_TIP_FWD = -3.0; W_TIP_AFT = -4.5
    W_SPAN = 3.4
    
    # Upper Wing Surface (Anhedral deflection is minimal on main wings)
    add_sym_quad(lines, 'C_HULL_MAIN', (W_ROOT_FWD, 0.9, 0.0), (W_TIP_FWD, W_SPAN, 0.05), (W_TIP_AFT, W_SPAN, 0.05), (W_ROOT_AFT, 0.95, 0.05), u_steps=4, v_steps=4)
    # Lower Wing Surface
    add_sym_quad(lines, 'C_HULL_MAIN', (W_ROOT_FWD, 0.9, 0.0), (W_TIP_FWD, W_SPAN, -0.05), (W_TIP_AFT, W_SPAN, -0.05), (W_ROOT_AFT, 0.95, -0.05), u_steps=4, v_steps=4)
    # Wingtips closing plates
    add_sym_quad(lines, 'C_DETAILS', (W_TIP_FWD, W_SPAN, 0.05), (W_TIP_AFT, W_SPAN, 0.05), (W_TIP_AFT, W_SPAN, -0.05), (W_TIP_FWD, W_SPAN, -0.05), u_steps=2, v_steps=1)

    # Anhedral Horizontal Tailplanes (Deflected sharply downward)
    T_ROOT_FWD = -5.5; T_ROOT_AFT = -7.5
    T_TIP_FWD = -6.5; T_TIP_AFT = -7.7
    T_SPAN = 2.8; T_DROP = -0.5
    
    add_sym_quad(lines, 'C_WEDGE', (T_ROOT_FWD, 0.95, 0.0), (T_TIP_FWD, T_SPAN, T_DROP), (T_TIP_AFT, T_SPAN, T_DROP), (T_ROOT_AFT, 0.95, 0.0), u_steps=4, v_steps=3)
    add_sym_quad(lines, 'C_WEDGE', (T_ROOT_FWD, 0.95, -0.1), (T_TIP_FWD, T_SPAN, T_DROP-0.05), (T_TIP_AFT, T_SPAN, T_DROP-0.05), (T_ROOT_AFT, 0.95, -0.1), u_steps=4, v_steps=3)

    # ==============================================================================
    # 6. BALL NOSE PROBE & INTEGRATED COCKPIT
    # ==============================================================================
    # Cockpit Wedged Canopy (Flush to maintain atmospheric integrity)
    add_sym_quad(lines, 'C_HULL_MAIN', (4.5, 0.2, 0.5), (3.0, 0.3, 0.75), (2.0, 0.3, 0.75), (2.0, 0.2, 0.65), u_steps=3, v_steps=2)
    # The distinct wedge-shaped blast windows (high-temp trans-paristeel geometry)
    add_sym_quad(lines, 'C_WEDGE', (4.0, 0.0, 0.55), (3.2, 0.15, 0.65), (3.0, 0.15, 0.65), (3.0, 0.0, 0.55), u_steps=2, v_steps=2)

    # High Altitude Ball Nose / Q-Ball Sensor Platform
    add_dome(lines, 'C_DETAILS', cx=7.6, cy=0.0, cz=0.0, radius=0.15, axis='x', dir=1, rings=4, t_count=12)
    # Projecting air data probe (Pitot cylinder)
    add_cylinder(lines, 'C_DETAILS', cx=7.75, cy=0.0, cz=0.0, length=0.6, radius=0.02, axis='x', rings=2, t_count=4)

    # ==============================================================================
    # 7. REACTION MOTORS XLR99 ROCKET EXHAUST
    # ==============================================================================
    # Main Thrust Housing Array protruding from aft transom
    add_cylinder(lines, 'C_WEDGE', cx=X_TAIL, cy=0.0, cz=0.0, length=0.4, radius=0.5, axis='x', rings=2, t_count=16)
    
    # Flaring XLR99 Bell Extrusion
    for ex_step in range(4):
        ex_x = X_TAIL - 0.4 - (ex_step * 0.15)
        ex_r = 0.5 + (ex_step * 0.08)
        add_cylinder(lines, 'C_ENGINE', cx=ex_x, cy=0.0, cz=0.0, length=0.15, radius=ex_r, axis='x', rings=1, t_count=16)
    
    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_x15_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking the geometric True Center of the 15.45m airframe
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.0
        
        # Starts explicitly from 115-degrees (Dramatic front-quarter aesthetic tracking the hypersonic needle geometry)
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
    # Anchor = 0.0. Total vessel length is 15.45m.
    # Setting cam_span safely to 10.0 to yield 20.0m horizontal footprint isolating the probe to engine bell.
    # Vertical bounds output 10.0 * 1.777 = 17.77m (x2 = 35.54m height allowed).
    # Perfectly frames the extremely slender aerodynamic profile escaping graphical overlap.
    cam_span = 10.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.6, 0.3), 
        ('C_HULL_MAIN', C_HULL_MAIN, 1.3, 1.0),
        ('C_HULL_DARK', C_HULL_DARK, 1.2, 1.0),
        ('C_WEDGE',     C_WEDGE,     1.3, 1.0),
        ('C_DETAILS',   C_DETAILS,   1.2, 1.0),
        ('C_ENGINE',    C_ENGINE,    1.5, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +12 degrees to cleanly dissect the dorsal and ventral stabilizer symmetry and sweeping chines
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=12.0)
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-451c // MACRO-ENGINEERING TENSOR: HYPERSONIC KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // NORTH AMERICAN X-15 MATRIX", color=C_HULL_DARK, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_ENGINE, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: SEVERE WEDGE EMPENNAGE / BALL NOSE / XLR99 EXHAUST", color=C_DETAILS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-451c: NORTH AMERICAN X-15 KINEMATICS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
