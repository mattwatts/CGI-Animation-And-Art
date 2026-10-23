"""
PROJECT: Logic Garden 451f (Exact Physical Construct // Buran Spaceplane Matrix) - HOTFIX
FORMAT: YouTube Shorts (1080x1920)
METADATA: BURAN, SPACEPLANE, AEROSPACE, ENERGIA, WIREFRAME, ENGINEERING, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Double-delta wings, explicit payload bay, correct OMS thruster housing (no SSMEs).
- Hotfix Integration: 'C_DETAILS' array and sub-palette constant formally injected for aft telemetry housings.
- Strict Bounds Protocol: Core locked at origin. cam_span scaled to 22.0 for flawless, unclipped 100% full-body framing.
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
OUT_DIR = "frames_451f_buran"
os.makedirs(OUT_DIR, exist_ok=True)

VELOCITY = 30.0  # m/s aerospace grid translation (orbital drift phase)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Translating Sub-orbital Plane)

C_HULL_MAIN = '#94A3B8'          # Heavy Slate (Upper Heat Shield / Payload Doors)
C_HULL_DARK = '#111115'          # Indestructible Black (Ventral Silica Thermal Tiles)
C_WEDGE     = '#475569'          # Machined Slate (Wing Surfaces, Tail Fin)
C_COCKPIT   = '#111115'          # Indestructible Black (Fused Silica Windshield)
C_ENGINE    = '#E11D48'          # Kinematic Red (OMS Thrust Resonance)
C_DETAILS   = '#334155'          # Deep Slate (Parachute Housing & OMS Thrusters)

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

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (BURAN SPACEPLANE)
# ------------------------------------------------------------------
def generate_buran_dynamic(t_sec):
    lines = {
        'C_HULL_MAIN': [], 'C_HULL_DARK': [], 'C_WEDGE': [], 
        'C_COCKPIT': [], 'C_ENGINE': [], 'C_DETAILS': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. TRANSLATING BASEPLATE ENVELOPE (Sub-Orbital Phase Vector)
    # ==============================================================================
    Z_FLOOR = -7.0
    travel_offset = (t_sec * VELOCITY) % 4.0  # 4m seamless tracking grid bounds
    
    gx_range = np.linspace(-30.0, 30.0, 16)
    gy_range = np.linspace(-25.0, 25.0, 13)
    
    for gx in gx_range: 
        shift_x = gx - travel_offset
        append_segmented(lines, 'C_GRID', np.full_like(gy_range, shift_x), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: 
        append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # Blueprint Parameters: L = 36.37m, W = 23.90m, H = ~10.5m. Center ~ 0,0,0
    X_NOSE = 18.2; X_TAIL = -18.17
    Y_RAD = 2.75 # Fuselage Half-width
    Z_BELLY = -2.5

    # ==============================================================================
    # 2. CORE PRESSURE VESSEL & PAYLOAD BAY
    # ==============================================================================
    # 18.55-metre massive payload doors spanning the dorsal plate
    X_PL_FWD = 9.0; X_PL_AFT = -9.55
    Z_PL_ROOF = 3.0
    
    # Payload Bay Roof (Upper cylindrical profile)
    add_sym_quad(lines, 'C_HULL_MAIN', (X_PL_FWD, 0.0, Z_PL_ROOF), (X_PL_AFT, 0.0, Z_PL_ROOF), 
                                       (X_PL_AFT, Y_RAD, Z_PL_ROOF-1.0), (X_PL_FWD, Y_RAD, Z_PL_ROOF-1.0), u_steps=5, v_steps=4)
    # Primary Lateral Fuselage 
    add_sym_quad(lines, 'C_HULL_MAIN', (X_PL_FWD, Y_RAD, Z_PL_ROOF-1.0), (X_PL_AFT, Y_RAD, Z_PL_ROOF-1.0), 
                                       (X_PL_AFT, Y_RAD, 0.0), (X_PL_FWD, Y_RAD, 0.0), u_steps=5, v_steps=3)
    
    # Ventral Fuselage mapped in Black (Silica Thermal Tiles - TPS)
    add_sym_quad(lines, 'C_HULL_DARK', (X_PL_FWD, Y_RAD, 0.0), (X_PL_AFT, Y_RAD, 0.0), 
                                       (X_PL_AFT, 0.0, Z_BELLY), (X_PL_FWD, 0.0, Z_BELLY), u_steps=5, v_steps=4)

    # Aft Fuselage spanning back to transom (X_PL_AFT to X_TAIL)
    # Tapers slightly upward to accommodate thruster mounts
    add_sym_quad(lines, 'C_HULL_MAIN', (X_PL_AFT, 0.0, Z_PL_ROOF), (X_TAIL, 0.0, Z_PL_ROOF-0.5), 
                                       (X_TAIL, Y_RAD-0.5, Z_PL_ROOF-1.5), (X_PL_AFT, Y_RAD, Z_PL_ROOF-1.0), u_steps=3, v_steps=3)
    add_sym_quad(lines, 'C_HULL_MAIN', (X_PL_AFT, Y_RAD, Z_PL_ROOF-1.0), (X_TAIL, Y_RAD-0.5, Z_PL_ROOF-1.5), 
                                       (X_TAIL, Y_RAD-0.5, 0.0), (X_PL_AFT, Y_RAD, 0.0), u_steps=3, v_steps=3)
    add_sym_quad(lines, 'C_HULL_DARK', (X_PL_AFT, Y_RAD, 0.0), (X_TAIL, Y_RAD-0.5, 0.0), 
                                       (X_TAIL, 0.0, Z_BELLY+0.5), (X_PL_AFT, 0.0, Z_BELLY), u_steps=3, v_steps=3)

    # ==============================================================================
    # 3. NOSE ASSEMBLY & COCKPIT 
    # ==============================================================================
    # Nose cone and crew cabin geometry tapering from Payload bay (X=9.0) to Nose (X=18.2)
    # The Buran windshield features six highly swept fused-silica windows
    
    X_CW = 14.5 # Cockpit Window start
    Z_CW = 1.2  # Cockpit Base Height
    add_sym_quad(lines, 'C_HULL_MAIN', (X_PL_FWD, 0.0, Z_PL_ROOF), (X_CW-1.5, 0.0, Z_PL_ROOF-0.2), 
                                       (X_CW-1.0, Y_RAD-0.5, Z_CW+0.5), (X_PL_FWD, Y_RAD, Z_PL_ROOF-1.0), u_steps=3, v_steps=3)
    
    # Trans-paristeel styled black windows (The 3 forward panes per side)
    add_sym_quad(lines, 'C_COCKPIT', (X_CW-1.5, 0.0, Z_PL_ROOF-0.2), (X_CW, 0.0, Z_CW), 
                                     (X_CW+0.5, 1.2, Z_CW), (X_CW-1.0, Y_RAD-0.5, Z_CW+0.5), u_steps=2, v_steps=3)

    # Blunt radome nose
    add_sym_quad(lines, 'C_HULL_MAIN', (X_CW, 0.0, Z_CW), (X_NOSE, 0.0, -0.5), 
                                       (X_NOSE-1.0, 1.0, -0.5), (X_CW+0.5, 1.2, Z_CW), u_steps=3, v_steps=3)
    add_sym_quad(lines, 'C_HULL_DARK', (X_PL_FWD, Y_RAD, 0.0), (X_CW, 2.0, 0.0), 
                                       (X_NOSE-1.0, 1.0, -0.5), (X_PL_FWD, 0.0, Z_BELLY), u_steps=4, v_steps=4)
    # Thermal nose cap closure
    add_sym_quad(lines, 'C_HULL_DARK', (X_NOSE, 0.0, -0.5), (X_NOSE-0.1, 0.0, -1.0), 
                                       (X_NOSE-1.0, 1.0, -1.0), (X_NOSE-1.0, 1.0, -0.5), u_steps=1, v_steps=2)

    # ==============================================================================
    # 4. DOUBLE-DELTA / CRANKED WING MATRIX
    # ==============================================================================
    # Forward Strake (Chine) generating severe sweep
    W_STRAKE_FWD = 8.0; W_STRAKE_AFT = -2.0
    Y_STRAKE_ROOT = Y_RAD - 0.2; Y_STRAKE_TIP = 6.0
    Z_WING = -1.2
    
    # Upper strake
    add_sym_quad(lines, 'C_WEDGE', (W_STRAKE_AFT, Y_STRAKE_ROOT, Z_WING+0.2), (W_STRAKE_FWD, Y_STRAKE_ROOT, Z_WING+0.2), 
                                   (W_STRAKE_AFT, Y_STRAKE_TIP, Z_WING+0.1), (W_STRAKE_AFT, Y_STRAKE_TIP, Z_WING+0.1), u_steps=3, v_steps=2)
    # Leading edge TPS (Black)
    add_sym_quad(lines, 'C_HULL_DARK', (W_STRAKE_AFT, Y_STRAKE_ROOT, Z_WING-0.2), (W_STRAKE_FWD, Y_STRAKE_ROOT, Z_WING-0.2), 
                                   (W_STRAKE_AFT, Y_STRAKE_TIP, Z_WING-0.1), (W_STRAKE_AFT, Y_STRAKE_TIP, Z_WING-0.1), u_steps=3, v_steps=2)

    # Primary Outboard Delta Wing
    W_ROOT_AFT = -14.0
    W_TIP_FWD = -6.0; W_TIP_AFT = -13.0 # Trailing edge sweeps forward slightly on Buran
    Y_TIP = 11.95 # True 23.90m Wingspan
    
    # Upper primary wing
    add_sym_quad(lines, 'C_WEDGE', (W_STRAKE_AFT, Y_STRAKE_ROOT, Z_WING+0.2), (W_STRAKE_AFT, Y_STRAKE_TIP, Z_WING+0.1), 
                                   (W_TIP_FWD, Y_TIP, Z_WING+0.1), (W_ROOT_AFT, Y_STRAKE_ROOT, Z_WING+0.2), u_steps=4, v_steps=5)
    add_sym_quad(lines, 'C_WEDGE', (W_ROOT_AFT, Y_STRAKE_ROOT, Z_WING+0.2), (W_TIP_FWD, Y_TIP, Z_WING+0.1), 
                                   (W_TIP_AFT, Y_TIP, Z_WING+0.05), (W_ROOT_AFT, Y_STRAKE_ROOT, Z_WING+0.05), u_steps=4, v_steps=5)

    # Lower primary wing (TPS Black underneath)
    add_sym_quad(lines, 'C_HULL_DARK', (W_STRAKE_AFT, Y_STRAKE_ROOT, Z_WING-0.2), (W_STRAKE_AFT, Y_STRAKE_TIP, Z_WING-0.1), 
                                   (W_TIP_FWD, Y_TIP, Z_WING-0.1), (W_ROOT_AFT, Y_STRAKE_ROOT, Z_WING-0.2), u_steps=4, v_steps=5)
    add_sym_quad(lines, 'C_HULL_DARK', (W_ROOT_AFT, Y_STRAKE_ROOT, Z_WING-0.2), (W_TIP_FWD, Y_TIP, Z_WING-0.1), 
                                   (W_TIP_AFT, Y_TIP, Z_WING-0.05), (W_ROOT_AFT, Y_STRAKE_ROOT, Z_WING-0.05), u_steps=4, v_steps=5)

    # ==============================================================================
    # 5. VERTICAL STABILISER (Empennage)
    # ==============================================================================
    # Swept massive dorsal fin 
    V_ROOT_FWD = -9.5; V_ROOT_AFT = -18.0
    V_TIP_FWD = -14.0; V_TIP_AFT = -18.0
    Z_TAIL_TOP = 8.0
    
    add_quad_mesh(lines, 'C_WEDGE', (V_ROOT_FWD, 0.3, Z_PL_ROOF-0.5), (V_TIP_FWD, 0.1, Z_TAIL_TOP), 
                                    (V_TIP_AFT, 0.1, Z_TAIL_TOP), (V_ROOT_AFT, 0.3, Z_PL_ROOF-0.5), u_steps=4, v_steps=4)
    add_quad_mesh(lines, 'C_WEDGE', (V_ROOT_FWD, -0.3, Z_PL_ROOF-0.5), (V_TIP_FWD, -0.1, Z_TAIL_TOP), 
                                    (V_TIP_AFT, -0.1, Z_TAIL_TOP), (V_ROOT_AFT, -0.3, Z_PL_ROOF-0.5), u_steps=4, v_steps=4)

    # Parachute / Drag Housing at base of vertical tail (Aft extension)
    add_cylinder(lines, 'C_DETAILS', cx=V_ROOT_AFT, cy=0.0, cz=Z_PL_ROOF-0.2, length=1.0, radius=0.4, axis='x', rings=2, t_count=8)

    # ==============================================================================
    # 6. AFT PROPULSION & MANOEUVRING (No Main SSMEs)
    # ==============================================================================
    # The Buran distinctly lacks the 3 massive main engines of the US Shuttle.
    # It relies on two smaller Orbital Manoeuvring System (OMS) thrust bells.
    OMS_X = X_TAIL; OMS_Y = 1.8; OMS_Z = 1.0
    
    add_sym_cylinder(lines, 'C_HULL_MAIN', cx=OMS_X+1.0, cy=OMS_Y, cz=OMS_Z, length=1.5, radius=0.8, axis='x', rings=3, t_count=12) # Pod housings
    add_sym_cylinder(lines, 'C_DETAILS', cx=OMS_X-0.5, cy=OMS_Y, cz=OMS_Z, length=1.5, radius=0.6, axis='x', rings=3, t_count=12)   # Thrust bells
    add_sym_cylinder(lines, 'C_ENGINE',  cx=OMS_X-1.5, cy=OMS_Y, cz=OMS_Z, length=1.0, radius=0.4, axis='x', rings=2, t_count=8)    # Plumes

    # Lateral RCS (Reaction Control System) blocks
    add_sym_quad(lines, 'C_DETAILS', (OMS_X+2.0, Y_RAD, Z_BELLY+1.0), (OMS_X+1.0, Y_RAD, Z_BELLY+1.0), 
                                     (OMS_X+1.0, Y_RAD, Z_BELLY+2.0), (OMS_X+2.0, Y_RAD, Z_BELLY+2.0), u_steps=2, v_steps=2)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        dynamic_rig = generate_buran_dynamic(t_sec)
        
        # Absolute Origin Tracking: Locking the geometric True Center of the 36.37m spaceplane
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.0
        
        # Starts explicitly from 115-degrees (Dramatic front-quarter aesthetic tracking massive blunt footprint)
        azimuth = 115.0 - (stage * 360.0)

        yield (f, t_sec, azimuth, cam_x, cam_y, cam_z, dynamic_rig)

def render_frame(packet):
    f, t_sec, azimuth, cx, cy, cz, dynamic_rig = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # 100% VISIBILITY THRESHOLD AUDIT:
    # Anchor = 0.0. Total vessel length is 36.37m. Transverse wingspan is 23.90m.
    # Setting cam_span safely to 22.0 to yield 44.0m horizontal footprint isolating the nose to aft tail completely.
    # Vertical bounds output 22.0 * 1.777 = 39.1m (x2 = 78.2m height allowed).
    # Perfectly frames the immense sub-orbital profile unconditionally escaping graphical overlap.
    cam_span = 22.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.6, 0.3), 
        ('C_HULL_MAIN', C_HULL_MAIN, 1.3, 1.0),
        ('C_HULL_DARK', C_HULL_DARK, 1.3, 1.0),
        ('C_WEDGE',     C_WEDGE,     1.3, 1.0),
        ('C_COCKPIT',   C_COCKPIT,   1.5, 1.0),
        ('C_DETAILS',   C_DETAILS,   1.2, 1.0),
        ('C_ENGINE',    C_ENGINE,    1.5, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in dynamic_rig[c_key]:
            # Elevated +14 degrees to cleanly dissect the expansive delta wings and the stark thermal tiling boundary
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-451f_HF // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // BURAN SPACEPLANE MATRIX", color=C_HULL_DARK, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT / LIVE FLIGHT LOOP (V=30.0m/s)", color=C_ENGINE, fontsize=13, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: DOUBLE-DELTA WINGS / HEAVY TPS TILING / OMS THRUSTER ARRAY", color=C_WEDGE, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-451f_HF: BURAN KINEMATICS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
