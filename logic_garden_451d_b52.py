"""
PROJECT: Logic Garden 451d (Exact Physical Construct // Boeing B-52 Stratofortress Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: B-52, STRATOFORTRESS, BOMBER, AEROSPACE, KINEMATICS, WIREFRAME, ENGINEERING
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Massive anhedral wing droop, 8x underslung engine pods, towering tail fin.
- Strict Bounds Protocol: Core locked at origin. cam_span scaled to 34.0 for flawless, unclipped full-body framing.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from absolute 115-degree dramatic front-quarter angle.
- Daylight Palette (White Substrate / High-Contrast Edge Geometry).
- Purged Jargon. Australian spelling conventions (maths, colour, kilometres, aeroplane, synchronisation).
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
OUT_DIR = "frames_451d_b52"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Translating Aerospace Plane)

C_HULL_MAIN = '#94A3B8'          # Heavy Slate (Primary Fuselage & Wing Plating)
C_HULL_DARK = '#475569'          # Machined Slate (Flaps, Engine Nacelles, Gear Doors)
C_DETAILS   = '#1E293B'          # Carbon Slate (Pylons, Empennage Spines)
C_COCKPIT   = '#111115'          # Indestructible Black (Stepped Windshield Glazing)
C_ENGINE    = '#E11D48'          # Kinematic Red (TF33 Thrust Exhaust Matrix)

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
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        if axis == 'x':   sx, sy, sz = cx + steps, [cy + radius*np.cos(a)]*rings, [cz + radius*np.sin(a)]*rings
        elif axis == 'y': sx, sy, sz = [cx + radius*np.cos(a)]*rings, cy + steps, [cz + radius*np.sin(a)]*rings
        else:             sx, sy, sz = [cx + radius*np.cos(a)]*rings, [cy + radius*np.sin(a)]*rings, cz + steps
        append_segmented(lines_dict, col, sx, sy, sz)

def add_sym_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='x', rings=4, t_count=16):
    add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis, rings, t_count)
    if abs(cy) > 0.001:
        add_cylinder(lines_dict, col, cx, -cy, cz, length, radius, axis, rings, t_count)


# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (BOEING B-52 STRATOFORTRESS)
# ------------------------------------------------------------------
def generate_b52_static():
    lines = {
        'C_HULL_MAIN': [], 'C_HULL_DARK': [], 'C_DETAILS': [], 
        'C_COCKPIT': [], 'C_ENGINE': [], 'C_GRID': []
    }

    # 1. BASEPLATE ENVELOPE (REFERENCE AEROSPACE GRID)
    Z_FLOOR = -6.0
    gx_range = np.linspace(-35.0, 35.0, 15)
    gy_range = np.linspace(-35.0, 35.0, 15)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # Real-world dimensions: 48.5m Length, 56.4m Wingspan
    # Origin strictly at center of lift. Nose = +24m. Tail = -24m. Wingtips = +/- 28.2m.

    # ==============================================================================
    # 2. CONTINUOUS FUSELAGE LOFTING (Slab-sided heavy structure)
    # ==============================================================================
    x_st = [24.0, 22.0, 18.0, 6.0, -10.0, -20.0, -24.5]
    ry =   [ 0.1,  1.1,  1.5, 1.6,   1.4,   0.9,   0.3]
    rz_t = [ 0.0,  1.3,  1.8, 1.8,   1.5,   1.2,   0.4]
    rz_b = [ 0.0, -1.2, -1.6, -1.6,-1.2,  -0.5,   0.0]
    
    for i in range(len(x_st)-1):
        x1, x2 = x_st[i], x_st[i+1]
        
        # Quarter-arc top (Port/Starboard)
        add_sym_quad(lines, 'C_HULL_MAIN', (x1, 0, rz_t[i]), (x2, 0, rz_t[i+1]), (x2, ry[i+1], rz_t[i+1]*0.3), (x1, ry[i], rz_t[i]*0.3), u_steps=3, v_steps=4)
        # Vertical slab sides
        add_sym_quad(lines, 'C_HULL_MAIN', (x1, ry[i], rz_t[i]*0.3), (x2, ry[i+1], rz_t[i+1]*0.3), (x2, ry[i+1], rz_b[i+1]*0.3), (x1, ry[i], rz_b[i]*0.3), u_steps=3, v_steps=2)
        # Quarter-arc bottom
        add_sym_quad(lines, 'C_HULL_DARK', (x1, ry[i], rz_b[i]*0.3), (x2, ry[i+1], rz_b[i+1]*0.3), (x2, 0, rz_b[i+1]), (x1, 0, rz_b[i]), u_steps=3, v_steps=4)

    # Radar Nose Dome & Tail Gunner/ECM cone
    add_quad_mesh(lines, 'C_DETAILS', (24.0, 0, 0), (25.0, 0, 0), (24.5, 0.4, 0), (24.0, 0.4, 0), u_steps=1, v_steps=2)
    add_quad_mesh(lines, 'C_DETAILS', (-24.5, 0, 0.2), (-25.5, 0, 0.2), (-25.0, 0.3, 0.2), (-24.5, 0.3, 0.2), u_steps=1, v_steps=2)

    # ==============================================================================
    # 3. ICONIC STEPPED COCKPIT 
    # ==============================================================================
    # Stepped upper deck starting at X=21.0
    add_sym_quad(lines, 'C_COCKPIT', (20.5, 0.0, 1.4), (20.5, 0.6, 1.4), (19.0, 0.8, 1.8), (19.0, 0.0, 1.8), u_steps=2, v_steps=2)
    add_sym_quad(lines, 'C_HULL_MAIN', (19.0, 0.0, 1.8), (19.0, 0.8, 1.8), (18.0, 1.0, 1.8), (18.0, 0.0, 1.8), u_steps=2, v_steps=1)

    # ==============================================================================
    # 4. MASSIVE ANHEDRAL SWEPT WINGS (56.4m Span)
    # ==============================================================================
    # Exact geometric mapping of the high-aspect ratio droop.
    W_ROOT_FWD = 8.0; W_ROOT_AFT = -2.0
    W_TIP_FWD = -8.0; W_TIP_AFT = -11.0
    W_SPAN = 28.2
    
    W_Z_ROOT = 1.0     # High mounted shoulder wing
    W_Z_TIP = -3.5     # Severe Anhedral Deflection (-4.5m drop)
    
    # Upper Wing Plating
    add_sym_quad(lines, 'C_HULL_MAIN', (W_ROOT_FWD, 1.6, W_Z_ROOT), (W_TIP_FWD, W_SPAN, W_Z_TIP), 
                                       (W_TIP_AFT, W_SPAN, W_Z_TIP), (W_ROOT_AFT, 1.6, W_Z_ROOT), u_steps=8, v_steps=5)
    # Lower Wing Plating
    add_sym_quad(lines, 'C_HULL_DARK', (W_ROOT_FWD, 1.6, W_Z_ROOT-0.5), (W_TIP_FWD, W_SPAN, W_Z_TIP-0.15), 
                                       (W_TIP_AFT, W_SPAN, W_Z_TIP-0.15), (W_ROOT_AFT, 1.6, W_Z_ROOT-0.5), u_steps=8, v_steps=5)
    
    # Aft flap segmentation lines extending down the wing
    add_sym_quad(lines, 'C_DETAILS', (W_ROOT_AFT+1.5, 1.6, W_Z_ROOT+0.05), (W_TIP_AFT+1.0, W_SPAN, W_Z_TIP+0.05), 
                                     (W_TIP_AFT, W_SPAN, W_Z_TIP+0.05), (W_ROOT_AFT, 1.6, W_Z_ROOT+0.05), u_steps=8, v_steps=2)

    # ==============================================================================
    # 5. EIGHT-BANK TWIN ENGINE NACELLES & PYLONS (TF33 Turbofans)
    # ==============================================================================
    # Inner Pylon (Starboard mapped, symmetry clones to Port)
    Y_IN = 9.0; Z_IN_WING = 1.0 + ((W_Z_TIP - 1.0) * (Y_IN / W_SPAN)) # Z height at wing
    X_IN_FWD = W_ROOT_FWD + ((W_TIP_FWD - W_ROOT_FWD) * (Y_IN / W_SPAN))
    Z_IN_ENG = Z_IN_WING - 1.5
    
    # Forward projecting heavy pylon
    add_sym_quad(lines, 'C_DETAILS', (X_IN_FWD, Y_IN, Z_IN_WING), (X_IN_FWD+3.0, Y_IN, Z_IN_ENG+0.6), 
                                     (X_IN_FWD-1.0, Y_IN, Z_IN_ENG+0.6), (X_IN_FWD-4.0, Y_IN, Z_IN_WING), u_steps=3, v_steps=2)
    # Twin Engine Pod 1 & 2
    add_sym_cylinder(lines, 'C_HULL_DARK', cx=X_IN_FWD+3.0, cy=Y_IN-0.7, cz=Z_IN_ENG, length=4.5, radius=0.6, axis='x', rings=4)
    add_sym_cylinder(lines, 'C_HULL_DARK', cx=X_IN_FWD+3.0, cy=Y_IN+0.7, cz=Z_IN_ENG, length=4.5, radius=0.6, axis='x', rings=4)
    # Exhaust Glow
    add_sym_cylinder(lines, 'C_ENGINE', cx=X_IN_FWD-1.5, cy=Y_IN-0.7, cz=Z_IN_ENG, length=0.2, radius=0.4, axis='x', rings=1)
    add_sym_cylinder(lines, 'C_ENGINE', cx=X_IN_FWD-1.5, cy=Y_IN+0.7, cz=Z_IN_ENG, length=0.2, radius=0.4, axis='x', rings=1)

    # Outer Pylon (Starboard mapped)
    Y_OUT = 18.0; Z_OUT_WING = 1.0 + ((W_Z_TIP - 1.0) * (Y_OUT / W_SPAN))
    X_OUT_FWD = W_ROOT_FWD + ((W_TIP_FWD - W_ROOT_FWD) * (Y_OUT / W_SPAN))
    Z_OUT_ENG = Z_OUT_WING - 1.2

    # Forward projecting outer pylon
    add_sym_quad(lines, 'C_DETAILS', (X_OUT_FWD, Y_OUT, Z_OUT_WING), (X_OUT_FWD+2.5, Y_OUT, Z_OUT_ENG+0.6), 
                                     (X_OUT_FWD-1.0, Y_OUT, Z_OUT_ENG+0.6), (X_OUT_FWD-3.0, Y_OUT, Z_OUT_WING), u_steps=3, v_steps=2)
    # Twin Engine Pod 3 & 4
    add_sym_cylinder(lines, 'C_HULL_DARK', cx=X_OUT_FWD+2.5, cy=Y_OUT-0.6, cz=Z_OUT_ENG, length=4.0, radius=0.6, axis='x', rings=4)
    add_sym_cylinder(lines, 'C_HULL_DARK', cx=X_OUT_FWD+2.5, cy=Y_OUT+0.6, cz=Z_OUT_ENG, length=4.0, radius=0.6, axis='x', rings=4)
    # Exhaust Glow
    add_sym_cylinder(lines, 'C_ENGINE', cx=X_OUT_FWD-1.5, cy=Y_OUT-0.6, cz=Z_OUT_ENG, length=0.2, radius=0.4, axis='x', rings=1)
    add_sym_cylinder(lines, 'C_ENGINE', cx=X_OUT_FWD-1.5, cy=Y_OUT+0.6, cz=Z_OUT_ENG, length=0.2, radius=0.4, axis='x', rings=1)

    # External Fuel Tanks (Mounted strictly between outer engines and wingtip)
    Y_TANK = 23.0; Z_TANK_WING = 1.0 + ((W_Z_TIP - 1.0) * (Y_TANK / W_SPAN))
    X_TANK_FWD = W_ROOT_FWD + ((W_TIP_FWD - W_ROOT_FWD) * (Y_TANK / W_SPAN))
    add_sym_cylinder(lines, 'C_HULL_MAIN', cx=X_TANK_FWD+2.0, cy=Y_TANK, cz=Z_TANK_WING-1.0, length=7.0, radius=0.7, axis='x', rings=5)

    # ==============================================================================
    # 6. TOWERING EMPENNAGE (Vertical & Horizontal Stabilisers)
    # ==============================================================================
    # Massive Vertical Tail Fin
    V_ROOT_FWD = -15.0; V_ROOT_AFT = -23.0
    V_TIP_FWD = -19.0; V_TIP_AFT = -24.0
    V_Z_TIP = 10.0
    
    add_quad_mesh(lines, 'C_HULL_MAIN', (V_ROOT_FWD, 0.2, 1.5), (V_TIP_FWD, 0.1, V_Z_TIP), (V_TIP_AFT, 0.1, V_Z_TIP), (V_ROOT_AFT, 0.2, 1.5), u_steps=4, v_steps=4)
    add_quad_mesh(lines, 'C_HULL_MAIN', (V_ROOT_FWD, -0.2, 1.5), (V_TIP_FWD, -0.1, V_Z_TIP), (V_TIP_AFT, -0.1, V_Z_TIP), (V_ROOT_AFT, -0.2, 1.5), u_steps=4, v_steps=4)

    # Swept Horizontal Stabilisers
    H_ROOT_FWD = -17.0; H_ROOT_AFT = -23.0
    H_TIP_FWD = -21.0; H_TIP_AFT = -24.0
    H_SPAN = 8.5
    
    add_sym_quad(lines, 'C_HULL_MAIN', (H_ROOT_FWD, 0.8, 0.6), (H_TIP_FWD, H_SPAN, 0.6), (H_TIP_AFT, H_SPAN, 0.6), (H_ROOT_AFT, 0.8, 0.6), u_steps=4, v_steps=3)
    add_sym_quad(lines, 'C_HULL_DARK', (H_ROOT_FWD, 0.8, 0.3), (H_TIP_FWD, H_SPAN, 0.3), (H_TIP_AFT, H_SPAN, 0.3), (H_ROOT_AFT, 0.8, 0.3), u_steps=4, v_steps=3)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_b52_static()
    velocity = 5.0 # Slow, majestic sub-orbital glide simulation
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking the geometric True Center of the huge bomber
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.0
        
        # Starts explicitly from 115-degrees (Dramatic front-quarter aesthetic detailing the sweeping wing droop)
        azimuth = 115.0 - (stage * 360.0)

        # Generating translating grid locally to simulate movement without affecting vehicle roots
        grid_shift = (t_sec * velocity) % 4.66  # Grid loops
        
        yield (f, t_sec, azimuth, grid_shift, cam_x, cam_y, cam_z, static_rig)

def render_frame(packet):
    f, t_sec, azimuth, grid_shift, cx, cy, cz, static_rig = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # 100% VISIBILITY THRESHOLD AUDIT:
    # Anchor = 0.0. Total wingspan is 56.4m (-28.2m to 28.2m).
    # Setting cam_span safely to 34.0 to yield 68.0m horizontal footprint isolating the wingtips entirely.
    # Vertical bounds output 34.0 * 1.777 = 60.4m (x2 = 120.8m height allowed).
    # Perfectly frames the super-massive aerospace span unconditionally escaping graphical overlap.
    cam_span = 34.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    # Render static translating grid dynamically inside loop for memory safety
    Z_FLOOR = -6.0
    gx_range = np.linspace(-35.0, 35.0, 16)
    gy_range = np.linspace(-35.0, 35.0, 16)
    for gx in gx_range: 
        shift_x = gx - grid_shift
        u, v, depth = project_3d_depth(np.full_like(gy_range, shift_x), gy_range, np.full_like(gy_range, Z_FLOOR), cx, cy, cz, azimuth, el_deg=14.0)
        render_queue.append((np.mean(depth), u, v, C_GRID, 0.6, 0.3))
    for gy in gy_range: 
        u, v, depth = project_3d_depth(gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR), cx, cy, cz, azimuth, el_deg=14.0)
        render_queue.append((np.mean(depth), u, v, C_GRID, 0.6, 0.3))

    layer_map = [
        ('C_HULL_MAIN', C_HULL_MAIN, 1.2, 1.0),
        ('C_HULL_DARK', C_HULL_DARK, 1.2, 1.0),
        ('C_DETAILS',   C_DETAILS,   1.2, 1.0),
        ('C_COCKPIT',   C_COCKPIT,   1.8, 1.0),
        ('C_ENGINE',    C_ENGINE,    1.8, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +14 degrees to powerfully frame the 8 under-wing nacelles and severe wing droop
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=14.0)
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-451d // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // BOEING B-52 STRATOFORTRESS MATRIX", color=C_HULL_DARK, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT / LIVE FLIGHT VECTOR", color=C_HULL_MAIN, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: ANHEDRAL WING SWEEP / 8-BANK TF33 ENGINE ARRAY", color=C_DETAILS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-451d: BOEING B-52 KINEMATICS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
