"""
PROJECT: Logic Garden 450v (Exact Physical Construct // Venator-class Star Destroyer Matrix) - REVISION
FORMAT: YouTube Shorts (1080x1920)
METADATA: VENATOR, STAR DESTROYER, STAR WARS, AEROSPACE, WIREFRAME, ENGINEERING, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: True vertical twin command bridges with sensor domes, 8-thruster flush aft array.
- Ventral Hangar mapping perfectly reshaped into a shallow Z-axis dome; eliminates "underslung engine" illusion.
- Strict Bounds Protocol: Core locked at origin. cam_span scaled to 800.0 for flawless, unclipped 100% full-body framing.
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
OUT_DIR = "frames_450v_venator"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Baseplate Reference)

C_HULL_MAIN = '#94A3B8'          # Heavy Slate (Primary Armored Skin)
C_HULL_DARK = '#475569'          # Machined Slate (Trench walls, Recessed decks)
C_DETAILS   = '#1E293B'          # Carbon Slate (Sensor Arrays, Turret Mounts, Scaffolding)
C_ENGINE    = '#00D2FF'          # High Engine Cyan (Ion Drive Exhaust Plume Mapping)
C_ACCENT    = '#E11D48'          # Kinematic Red (Dorsal Flight Deck Striping / Diplomatic Markings)

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
        if axis == 'x':   ix, iy, iz = np.full_like(t, cx+s), cy + radius*np.cos(t), cz + radius*np.sin(t)
        elif axis == 'y': ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy+s), cz + radius*np.sin(t)
        else:             ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), np.full_like(t, cz+s)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        if axis == 'x':   sx, sy, sz = cx + steps, np.full_like(steps, cy + radius*np.cos(a)), np.full_like(steps, cz + radius*np.sin(a))
        elif axis == 'y': sx, sy, sz = np.full_like(steps, cx + radius*np.cos(a)), cy + steps, np.full_like(steps, cz + radius*np.sin(a))
        else:             sx, sy, sz = np.full_like(steps, cx + radius*np.cos(a)), np.full_like(steps, cy + radius*np.sin(a)), cz + steps
        append_segmented(lines_dict, col, sx, sy, sz)

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
        ix = cx + r_s*np.cos(t)
        iy = cy + r_s*np.sin(t)
        iz = np.full_like(t, cz + h_s)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        rr = radius * np.cos(p_step)
        hh = radius * np.sin(p_step) * dir
        sx = cx + rr*np.cos(a)
        sy = cy + rr*np.sin(a)
        sz = cz + hh
        append_segmented(lines_dict, col, list(sx), list(sy), list(sz))

def add_sym_dome(lines_dict, col, cx, cy, cz, radius, axis='z', dir=1, rings=4, t_count=16):
    add_dome(lines_dict, col, cx, cy, cz, radius, axis, dir, rings, t_count)
    if abs(cy) > 0.001:
        add_dome(lines_dict, col, cx, -cy, cz, radius, axis, dir, rings, t_count)


# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (VENATOR STAR DESTROYER)
# ------------------------------------------------------------------
def generate_venator_static():
    lines = {
        'C_HULL_MAIN': [], 'C_HULL_DARK': [], 'C_DETAILS': [], 
        'C_ENGINE': [], 'C_ACCENT': [], 'C_GRID': []
    }

    # 1. BASEPLATE ENVELOPE (REFERENCE ORBITAL GRID)
    Z_FLOOR = -300.0
    gx_range = np.linspace(-700.0, 700.0, 29)
    gy_range = np.linspace(-500.0, 500.0, 21)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # Real-world dimensions: 1137m L x 548m W x 268m H.
    X_NOSE = 568.5; X_TAIL = -568.5
    Y_WINGTIP = 274.0; X_WINGTIP = -400.0
    X_AFT_CORNER = -520.0; Y_AFT_CORNER = 180.0

    # ==============================================================================
    # 2. UPPER & LOWER DAGGER HULL PLATING
    # ==============================================================================
    # Equatorial Trench depth boundaries
    Z_TRENCH_UP = 8.0; Z_TRENCH_DN = -8.0
    # Dorsal Ridge elevation points
    Z_RIDGE_FWD = 25.0; Z_RIDGE_AFT = 75.0
    Z_VENTRAL_KEEL = -40.0; Z_VENTRAL_AFT = -85.0

    # Forward Primary Upper Plates
    add_sym_quad(lines, 'C_HULL_MAIN', (X_NOSE, 0, Z_TRENCH_UP), (0, 60, Z_RIDGE_FWD), (X_WINGTIP, Y_WINGTIP, Z_TRENCH_UP), (0, 0, Z_RIDGE_FWD), u_steps=6, v_steps=6)
    # Aft Upper Plates
    add_sym_quad(lines, 'C_HULL_MAIN', (0, 0, Z_RIDGE_FWD), (X_WINGTIP, Y_WINGTIP, Z_TRENCH_UP), (X_AFT_CORNER, Y_AFT_CORNER, Z_TRENCH_UP), (X_TAIL, 0, Z_RIDGE_AFT), u_steps=5, v_steps=6)
    
    # Forward Primary Lower Plates
    add_sym_quad(lines, 'C_HULL_MAIN', (X_NOSE, 0, Z_TRENCH_DN), (0, 0, Z_VENTRAL_KEEL), (X_WINGTIP, Y_WINGTIP, Z_TRENCH_DN), (0, 60, Z_VENTRAL_KEEL), u_steps=6, v_steps=6)
    # Aft Lower Plates
    add_sym_quad(lines, 'C_HULL_MAIN', (0, 0, Z_VENTRAL_KEEL), (X_TAIL, 0, Z_VENTRAL_AFT), (X_AFT_CORNER, Y_AFT_CORNER, Z_TRENCH_DN), (X_WINGTIP, Y_WINGTIP, Z_TRENCH_DN), u_steps=5, v_steps=6)

    # Equatorial Trench Cut-Out (Exposed lateral mechanics)
    add_sym_quad(lines, 'C_HULL_DARK', (X_NOSE, 0, Z_TRENCH_UP), (X_WINGTIP, Y_WINGTIP, Z_TRENCH_UP), (X_WINGTIP, Y_WINGTIP, Z_TRENCH_DN), (X_NOSE, 0, Z_TRENCH_DN), u_steps=8, v_steps=2)
    add_sym_quad(lines, 'C_HULL_DARK', (X_WINGTIP, Y_WINGTIP, Z_TRENCH_UP), (X_AFT_CORNER, Y_AFT_CORNER, Z_TRENCH_UP), (X_AFT_CORNER, Y_AFT_CORNER, Z_TRENCH_DN), (X_WINGTIP, Y_WINGTIP, Z_TRENCH_DN), u_steps=3, v_steps=2)

    # ==============================================================================
    # 3. DORSAL FLIGHT DECK TRENCH (Kinematic Red Stripe)
    # ==============================================================================
    # The massive ½ kilometre long segmented runway bay that splits the central spine
    X_TRENCH_START = 350.0; X_TRENCH_END = -150.0
    Y_TR_W = 20.0; Y_TR_AFT_W = 45.0
    
    # Recessed base floor
    add_sym_quad(lines, 'C_HULL_DARK', (X_TRENCH_START, 0, 15.0), (X_TRENCH_END, 0, 45.0), (X_TRENCH_END, Y_TR_AFT_W-5, 45.0), (X_TRENCH_START, Y_TR_W-2, 15.0), u_steps=6, v_steps=3)
    
    # Iconic Kuat Markings outlining the massive runway blast doors
    add_sym_quad(lines, 'C_ACCENT', (X_TRENCH_START, Y_TR_W, Z_RIDGE_FWD + 5.0), (X_TRENCH_END, Y_TR_AFT_W, Z_RIDGE_FWD + 25.0), 
                                    (X_TRENCH_END, Y_TR_AFT_W+8, Z_RIDGE_FWD + 25.0), (X_TRENCH_START, Y_TR_W+4, Z_RIDGE_FWD + 5.0), u_steps=6, v_steps=1)

    # ==============================================================================
    # 4. VENTRAL HANGAR & REACTOR BULGE
    # ==============================================================================
    # Generates a shallow, securely integrated downward spherical plate array, 
    # categorically eliminating the "underslung engine" illusion.
    add_dome(lines, 'C_HULL_DARK', cx=0.0, cy=0.0, cz=Z_VENTRAL_KEEL+5, radius=45.0, axis='z', dir=-1, rings=5, t_count=20)
    add_quad_mesh(lines, 'C_DETAILS', (30.0, 0.0, Z_VENTRAL_KEEL), (-40.0, 0.0, Z_VENTRAL_AFT), (-40.0, 0.0, Z_VENTRAL_AFT-15), (30.0, 0.0, Z_VENTRAL_KEEL-15), u_steps=4, v_steps=2)

    # ==============================================================================
    # 5. TWIN COMMAND BRIDGES & AFT SUPERSTRUCTURE
    # ==============================================================================
    X_SS_START = -150.0; X_SS_END = -450.0
    add_sym_quad(lines, 'C_HULL_MAIN', (X_SS_START, 0, 80.0), (X_SS_END, 0, 110.0), (X_SS_END, 120.0, 110.0), (X_SS_START, 45.0, 80.0), u_steps=5, v_steps=5)
    add_sym_quad(lines, 'C_DETAILS', (X_SS_START-50, 0, 110.0), (X_SS_END-20, 0, 130.0), (X_SS_END-20, 90.0, 130.0), (X_SS_START-50, 30.0, 110.0), u_steps=4, v_steps=4)

    # Iconic Vertical Port and Starboard Command Towers
    TOW_X = -380.0; TOW_Y = 60.0 # Starboard coordinates; add_sym handles port mirroring automatically.
    T_Z0 = 110.0; T_Z1 = 200.0 
    
    # Rising Ascendant Stalks
    add_sym_quad(lines, 'C_HULL_MAIN', (TOW_X+25, TOW_Y-12, T_Z0), (TOW_X+25, TOW_Y+12, T_Z0), (TOW_X+15, TOW_Y+8, T_Z1), (TOW_X+15, TOW_Y-8, T_Z1), u_steps=3, v_steps=4)
    add_sym_quad(lines, 'C_HULL_MAIN', (TOW_X-25, TOW_Y+12, T_Z0), (TOW_X-25, TOW_Y-12, T_Z0), (TOW_X-15, TOW_Y-8, T_Z1), (TOW_X-15, TOW_Y+8, T_Z1), u_steps=3, v_steps=4)
    add_sym_quad(lines, 'C_HULL_DARK', (TOW_X+25, TOW_Y+12, T_Z0), (TOW_X-25, TOW_Y+12, T_Z0), (TOW_X-15, TOW_Y+8, T_Z1), (TOW_X+15, TOW_Y+8, T_Z1), u_steps=2, v_steps=4)
    add_sym_quad(lines, 'C_HULL_DARK', (TOW_X-25, TOW_Y-12, T_Z0), (TOW_X+25, TOW_Y-12, T_Z0), (TOW_X+15, TOW_Y-8, T_Z1), (TOW_X-15, TOW_Y-8, T_Z1), u_steps=2, v_steps=4)

    # Wide Bridge Command Modules (Hex-Top)
    add_sym_quad(lines, 'C_HULL_MAIN', (TOW_X+18, TOW_Y-25, T_Z1), (TOW_X+18, TOW_Y+25, T_Z1), (TOW_X-12, TOW_Y+25, T_Z1), (TOW_X-12, TOW_Y-25, T_Z1), u_steps=3, v_steps=3)
    add_sym_quad(lines, 'C_HULL_MAIN', (TOW_X+18, TOW_Y-25, T_Z1+12), (TOW_X+18, TOW_Y+25, T_Z1+12), (TOW_X-12, TOW_Y+25, T_Z1+12), (TOW_X-12, TOW_Y-25, T_Z1+12), u_steps=3, v_steps=3)
    add_sym_quad(lines, 'C_ACCENT', (TOW_X+18, TOW_Y-25, T_Z1), (TOW_X+18, TOW_Y+25, T_Z1), (TOW_X+18, TOW_Y+25, T_Z1+12), (TOW_X+18, TOW_Y-25, T_Z1+12), u_steps=2, v_steps=4) # Viewports

    # Sphere Deflector Shield Generators mounted on the bridge roofs
    add_sym_dome(lines, 'C_DETAILS', cx=TOW_X+5, cy=TOW_Y+15, cz=T_Z1+12, radius=4.5, axis='z', dir=1, rings=4, t_count=12)
    add_sym_dome(lines, 'C_DETAILS', cx=TOW_X+5, cy=TOW_Y-15, cz=T_Z1+12, radius=4.5, axis='z', dir=1, rings=4, t_count=12)

    # ==============================================================================
    # 6. HEAVY THRUSTER MATRIX (8x Aft Engine Array Mounted Flush to Bulkhead)
    # ==============================================================================
    TRENCH_Z = Z_TRENCH_UP + 60
    # Flat bulkhead closing off the aft perimeter
    add_sym_quad(lines, 'C_HULL_DARK', (X_TAIL, 0, TRENCH_Z), (X_TAIL, 0, Z_TRENCH_DN-60), (X_TAIL, Y_AFT_CORNER-20, Z_TRENCH_DN), (X_TAIL, Y_AFT_CORNER-20, TRENCH_Z), u_steps=4, v_steps=4)

    # 4 Massive Core Thrusters (Properly scaled and seated at Z=-10 against the back wall)
    add_sym_cylinder(lines, 'C_HULL_DARK', cx=X_TAIL, cy=28.0, cz=-10.0, length=45.0, radius=22.0, axis='x', rings=4, t_count=16)
    add_sym_cylinder(lines, 'C_ENGINE', cx=X_TAIL-40.0, cy=28.0, cz=-10.0, length=8.0, radius=18.0, axis='x', rings=2, t_count=16)
    
    add_sym_cylinder(lines, 'C_HULL_DARK', cx=X_TAIL+10, cy=75.0, cz=-10.0, length=32.0, radius=16.0, axis='x', rings=4, t_count=16)
    add_sym_cylinder(lines, 'C_ENGINE', cx=X_TAIL-20.0, cy=75.0, cz=-10.0, length=7.0, radius=14.0, axis='x', rings=2, t_count=16)

    # 2 Upper Secondary Thrusters
    add_sym_cylinder(lines, 'C_HULL_DARK', cx=X_TAIL, cy=28.0, cz=38.0, length=30.0, radius=12.0, axis='x', rings=4, t_count=12)
    add_sym_cylinder(lines, 'C_ENGINE', cx=X_TAIL-25.0, cy=28.0, cz=38.0, length=6.0, radius=9.0, axis='x', rings=2, t_count=12)

    # 2 Outermost Tertiary Thrusters
    add_sym_cylinder(lines, 'C_HULL_DARK', cx=X_TAIL+20, cy=120.0, cz=5.0, length=20.0, radius=8.0, axis='x', rings=3, t_count=10)
    add_sym_cylinder(lines, 'C_ENGINE', cx=X_TAIL-0.0, cy=120.0, cz=5.0, length=4.0, radius=6.0, axis='x', rings=2, t_count=10)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_venator_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking the geometric True Center of the staggering 1.13km construct
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.0
        
        # Starts explicitly from 115-degrees (Dramatic front-quarter aesthetic tracking the expansive dagger lines)
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
    # Anchor = 0.0. Total vessel length is 1,137m. Transverse span 548m.
    # Setting extreme cam_span strictly to 800.0 to yield 1.6km (1600m) horizontal footprint isolating all extremities.
    cam_span = 800.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.6, 0.3), 
        ('C_HULL_MAIN', C_HULL_MAIN, 1.2, 1.0),
        ('C_HULL_DARK', C_HULL_DARK, 1.3, 1.0),
        ('C_DETAILS',   C_DETAILS,   1.1, 1.0),
        ('C_ENGINE',    C_ENGINE,    1.5, 1.0),
        ('C_ACCENT',    C_ACCENT,    1.6, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +18 degrees to deeply frame the intricate dual command towers and the massive dorsal flight bay
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=18.0)
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-450v // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // VENATOR-CLASS STAR DESTROYER MATRIX", color=C_ACCENT, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_HULL_DARK, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: TRUE VERTICAL COMMAND TOWERS / 8-BANK AFT THRUSTER ARRAY", color=C_DETAILS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-450v_REV: VENATOR-CLASS KINEMATICS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
