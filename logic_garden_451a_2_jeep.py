"""
PROJECT: Logic Garden 451a - Revision 1 (Exact Physical Construct // Willys MB Jeep Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: WILLYS, JEEP, MB, WW2, GROUND KINEMATICS, WIREFRAME, ENGINEERING
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry.
- Exact structural integration: Flushed flush tailgate spare wheel mount, true dynamic wheel rotation.
- Perfect Mechanical Synchronisation: V = 2.0m/s. Grid span = 1.0m. R_wheel = 0.3819m yielding exactly 20.0 rotations at 24s.
- Strict Bounds Protocol: Core locked at origin. cam_span scaled to 3.2 for flawless, unclipped 100% full-body framing.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from absolute 115-degree dramatic front-quarter angle.
- Daylight Palette (White Substrate / High-Contrast Edge Geometry).
- Purged Jargon. Australian spelling conventions (maths, colour, kilometres, synchronisation).
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
OUT_DIR = "frames_451a_jeep_v2"
os.makedirs(OUT_DIR, exist_ok=True)

VELOCITY = 2.0  # m/s backward grid translation
WHEEL_R = 2.0 / (2 * np.pi * (20 / 24.0)) # 0.38197m to align 20 full rotations perfectly over 24 seconds

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Translating Ground Plane)

C_HULL_MAIN = '#3F6212'          # Military Olive (Primary Tub & Hood)
C_HULL_DARK = '#1A2E05'          # Deep Olive (Undercarriage, Inside Tub)
C_DETAILS   = '#1E293B'          # Carbon Slate (Frame Rails, Bumper, Steering, Tools)
C_WHEEL     = '#111115'          # Indestructible Black (Tyres & Hub Mechanics)
C_ACCENT    = '#64748B'          # Slate Canvas (Seats, Gerry Can details)

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
        append_sym(lines_dict, col, sx, sy, sz)

def add_dynamic_wheel(lines_dict, col, cx, cy, cz, radius, width, theta_rot):
    # Dynamic rotating kinematics mapped via angular arrays (Y-axis aligned)
    t = np.linspace(0, 2*np.pi, 20, endpoint=False)
    R_y = np.array([
        [np.cos(theta_rot),  0, np.sin(theta_rot)],
        [0,                  1,                 0],
        [-np.sin(theta_rot), 0, np.cos(theta_rot)]
    ])
    y_faces = [-width/2, width/2]
    
    for yf in y_faces:
        ox = radius * np.cos(t); oz = radius * np.sin(t); oy = np.full_like(t, yf)
        pts = np.dot(R_y, np.vstack((ox, oy, oz)))
        append_segmented(lines_dict, col, list(pts[0]+cx)+[pts[0][0]+cx], list(pts[1]+cy)+[pts[1][0]+cy], list(pts[2]+cz)+[pts[2][0]+cz])
        
        hx = (radius*0.4) * np.cos(t); hz = (radius*0.4) * np.sin(t); hy = np.full_like(t, yf*1.1) 
        hpts = np.dot(R_y, np.vstack((hx, hy, hz)))
        append_segmented(lines_dict, col, list(hpts[0]+cx)+[hpts[0][0]+cx], list(hpts[1]+cy)+[hpts[1][0]+cy], list(hpts[2]+cz)+[hpts[2][0]+cz])
        
        for s in range(0, 20, 4):
            append_segmented(lines_dict, col, [hpts[0][s]+cx, pts[0][s]+cx], [hpts[1][s]+cy, pts[1][s]+cy], [hpts[2][s]+cz, pts[2][s]+cz])
            
    for i in range(20):
        p1 = np.dot(R_y, np.array([radius * np.cos(t[i]), y_faces[0], radius * np.sin(t[i])]))
        p2 = np.dot(R_y, np.array([radius * np.cos(t[i]), y_faces[1], radius * np.sin(t[i])]))
        append_segmented(lines_dict, col, [p1[0]+cx, p2[0]+cx], [p1[1]+cy, p2[1]+cy], [p1[2]+cz, p2[2]+cz])

def add_static_wheel_x(lines_dict, col, cx, cy, cz, radius, width):
    # Static geometry mapping the flat side directly onto the X-axis (Tailgate mounted)
    t = np.linspace(0, 2*np.pi, 20, endpoint=False)
    x_faces = [cx - width/2, cx + width/2]
    
    for xf in x_faces:
        oy = radius * np.cos(t); oz = radius * np.sin(t)
        append_segmented(lines_dict, col, [xf]*21, list(oy + cy)+[oy[0] + cy], list(oz + cz)+[oz[0] + cz])
        
        hy = (radius*0.4) * np.cos(t); hz = (radius*0.4) * np.sin(t)
        h_xf = xf + (width*0.1 if xf == cx - width/2 else -width*0.1)
        append_segmented(lines_dict, col, [h_xf]*21, list(hy + cy)+[hy[0] + cy], list(hz + cz)+[hz[0] + cz])
        
        for s in range(0, 20, 4):
            append_segmented(lines_dict, col, [h_xf, xf], [hy[s] + cy, oy[s] + cy], [hz[s] + cz, oz[s] + cz])
            
    for i in range(20):
        append_segmented(lines_dict, col, x_faces, [radius * np.cos(t[i]) + cy]*2, [radius * np.sin(t[i]) + cz]*2)

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (DYNAMIC WILLYS MB JEEP)
# ------------------------------------------------------------------
def generate_jeep_dynamic(t_sec):
    lines = {
        'C_HULL_MAIN': [], 'C_HULL_DARK': [], 'C_DETAILS': [], 
        'C_WHEEL': [], 'C_ACCENT': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. TRANSLATING BASEPLATE ENVELOPE
    # ==============================================================================
    Z_FLOOR = 0.0
    travel_offset = (t_sec * VELOCITY) % 1.0  # Loops every 1.0 meters seamlessly
    
    gx_range = np.linspace(-6.0, 6.0, 13)
    gy_range = np.linspace(-4.0, 4.0, 9)
    for gx in gx_range: 
        # Shift the X gridlines backward to simulate forward vehicle locomotion
        shift_x = gx - travel_offset
        append_segmented(lines, 'C_GRID', np.full_like(gy_range, shift_x), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: 
        # The longitudinal lines remain static but provide depth
        append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # Real-world dimensions: WB 2.03m. L 3.33m. W 1.57m.
    # Set wheel coordinates
    X_FRONT = 1.01; X_REAR = -1.02
    Y_TRACK = 0.61

    # ==============================================================================
    # 2. DYNAMIC LOCOMOTIVE WHEEL ARRAY
    # ==============================================================================
    # Mechanical angular rotation over time: theta = (V * t) / R
    theta_rot = (VELOCITY * t_sec) / WHEEL_R

    for y_sign in [-1, 1]:
        cy = Y_TRACK * y_sign
        # Front Wheels
        add_dynamic_wheel(lines, 'C_WHEEL', X_FRONT, cy, Z_FLOOR+WHEEL_R, WHEEL_R, 0.16, theta_rot)
        # Rear Wheels
        add_dynamic_wheel(lines, 'C_WHEEL', X_REAR, cy, Z_FLOOR+WHEEL_R, WHEEL_R, 0.16, theta_rot)

    # Spare tyre mounted flat to the rear transverse tailgate (X-axis alignment)
    add_static_wheel_x(lines, 'C_HULL_DARK', -1.75, 0.0, Z_FLOOR+WHEEL_R+0.4, WHEEL_R, 0.16)

    # ==============================================================================
    # 3. LADDER FRAME & BUMPERS
    # ==============================================================================
    add_sym_quad(lines, 'C_DETAILS', (1.6, 0.35, Z_FLOOR+0.45), (-1.6, 0.35, Z_FLOOR+0.45), (-1.6, 0.35, Z_FLOOR+0.55), (1.6, 0.35, Z_FLOOR+0.55), u_steps=3, v_steps=1)
    
    # Front Bumper
    add_quad_mesh(lines, 'C_DETAILS', (1.65, -0.7, Z_FLOOR+0.5), (1.65, 0.7, Z_FLOOR+0.5), (1.65, 0.7, Z_FLOOR+0.6), (1.65, -0.7, Z_FLOOR+0.6), u_steps=4, v_steps=1)
    # Rear Bumperettes
    add_sym_quad(lines, 'C_DETAILS', (-1.6, 0.45, Z_FLOOR+0.5), (-1.65, 0.45, Z_FLOOR+0.5), (-1.65, 0.7, Z_FLOOR+0.6), (-1.6, 0.7, Z_FLOOR+0.6), u_steps=1, v_steps=1)

    # ==============================================================================
    # 4. PRIMARY TUB & FENDERS
    # ==============================================================================
    # Lower Tub
    add_sym_quad(lines, 'C_HULL_DARK', (0.4, 0.7, Z_FLOOR+0.55), (-1.6, 0.7, Z_FLOOR+0.55), (-1.6, 0.0, Z_FLOOR+0.55), (0.4, 0.0, Z_FLOOR+0.55), u_steps=4, v_steps=2) # Floor
    
    # Side Panels (Iconic stepped entry)
    add_sym_quad(lines, 'C_HULL_MAIN', (0.4, 0.7, Z_FLOOR+0.55), (0.4, 0.7, Z_FLOOR+0.9), (0.0, 0.7, Z_FLOOR+0.9), (0.0, 0.7, Z_FLOOR+0.55), u_steps=2, v_steps=2) # Cowl Side
    add_sym_quad(lines, 'C_HULL_MAIN', (0.0, 0.7, Z_FLOOR+0.55), (-0.4, 0.7, Z_FLOOR+0.55), (-0.4, 0.7, Z_FLOOR+0.9), (0.0, 0.7, Z_FLOOR+0.9), u_steps=1, v_steps=2) # Door Step (Cutout)
    add_sym_quad(lines, 'C_HULL_MAIN', (-0.4, 0.7, Z_FLOOR+0.55), (-1.6, 0.7, Z_FLOOR+0.55), (-1.6, 0.7, Z_FLOOR+0.9), (-0.4, 0.7, Z_FLOOR+0.9), u_steps=3, v_steps=2) # Rear Side
    add_sym_quad(lines, 'C_HULL_MAIN', (-1.6, 0.7, Z_FLOOR+0.55), (-1.6, 0.0, Z_FLOOR+0.55), (-1.6, 0.0, Z_FLOOR+0.9), (-1.6, 0.7, Z_FLOOR+0.9), u_steps=3, v_steps=2) # Rear Transom

    # Flat Front Fenders over wheels
    add_sym_quad(lines, 'C_HULL_MAIN', (1.6, 0.7, Z_FLOOR+0.85), (0.4, 0.7, Z_FLOOR+0.85), (0.4, 0.35, Z_FLOOR+0.85), (1.6, 0.35, Z_FLOOR+0.85), u_steps=3, v_steps=2)

    # Sloping Hood
    add_sym_quad(lines, 'C_HULL_MAIN', (0.4, 0.35, Z_FLOOR+0.95), (1.6, 0.35, Z_FLOOR+0.9), (1.6, 0.0, Z_FLOOR+0.9), (0.4, 0.0, Z_FLOOR+0.95), u_steps=3, v_steps=2)

    # ==============================================================================
    # 5. ICONIC 9-SLOT GRILLE & HEADLIGHTS
    # ==============================================================================
    # Main Stamped Vertical Plate
    add_sym_quad(lines, 'C_HULL_MAIN', (1.6, 0.35, Z_FLOOR+0.9), (1.6, 0.35, Z_FLOOR+0.55), (1.6, 0.0, Z_FLOOR+0.55), (1.6, 0.0, Z_FLOOR+0.9), u_steps=1, v_steps=3)
    
    # Grille Slots
    for g_y in np.linspace(-0.25, 0.25, 9):
        append_segmented(lines, 'C_HULL_DARK', [1.6, 1.6], [g_y, g_y], [Z_FLOOR+0.6, Z_FLOOR+0.85])

    # Headlights
    add_cylinder(lines, 'C_DETAILS', cx=1.58, cy=0.45, cz=Z_FLOOR+0.75, length=0.08, radius=0.08, axis='x', rings=2, t_count=8)
    add_cylinder(lines, 'C_DETAILS', cx=1.58, cy=-0.45, cz=Z_FLOOR+0.75, length=0.08, radius=0.08, axis='x', rings=2, t_count=8)

    # ==============================================================================
    # 6. WINDSHIELD, SEATS & APPENDAGES
    # ==============================================================================
    # Folded-up Windshield Frame
    W_A = 0.3; W_ZTOP = Z_FLOOR+1.4
    add_sym_quad(lines, 'C_DETAILS', (0.4, 0.7, Z_FLOOR+0.95), (W_A, 0.7, W_ZTOP), (W_A, 0.0, W_ZTOP), (0.4, 0.0, Z_FLOOR+0.95), u_steps=2, v_steps=3)
    # Glass panes
    add_sym_quad(lines, 'C_HULL_DARK', (0.38, 0.65, Z_FLOOR+1.0), (0.32, 0.65, W_ZTOP-0.05), (0.32, 0.05, W_ZTOP-0.05), (0.38, 0.05, Z_FLOOR+1.0), u_steps=1, v_steps=1)

    # Steering Column & Wheel
    append_segmented(lines, 'C_DETAILS', [0.4, -0.1], [0.35, 0.35], [Z_FLOOR+0.7, Z_FLOOR+1.0])
    add_cylinder(lines, 'C_DETAILS', cx=-0.1, cy=0.35, cz=Z_FLOOR+1.0, length=0.01, radius=0.18, axis='x', rings=1, t_count=12)

    # Seats (Pilot & Passenger)
    add_sym_quad(lines, 'C_ACCENT', (-0.1, 0.45, Z_FLOOR+0.7), (-0.4, 0.45, Z_FLOOR+0.7), (-0.4, 0.1, Z_FLOOR+0.7), (-0.1, 0.1, Z_FLOOR+0.7), u_steps=2, v_steps=2) # Cushions
    add_sym_quad(lines, 'C_ACCENT', (-0.4, 0.45, Z_FLOOR+0.7), (-0.45, 0.45, Z_FLOOR+1.0), (-0.45, 0.1, Z_FLOOR+1.0), (-0.4, 0.1, Z_FLOOR+0.7), u_steps=2, v_steps=2) # Backrests
    # Rear Bench
    add_quad_mesh(lines, 'C_ACCENT', (-1.2, 0.45, Z_FLOOR+0.7), (-1.5, 0.45, Z_FLOOR+0.7), (-1.5, -0.45, Z_FLOOR+0.7), (-1.2, -0.45, Z_FLOOR+0.7), u_steps=2, v_steps=3)
    
    # Jerry Can
    add_quad_mesh(lines, 'C_ACCENT', (-1.65, -0.4, Z_FLOOR+0.9), (-1.65, -0.6, Z_FLOOR+0.9), (-1.65, -0.6, Z_FLOOR+0.5), (-1.65, -0.4, Z_FLOOR+0.5), u_steps=2, v_steps=2)

    # Pioneer Tools (Axe and Shovel securely harnessed to driver's side plate)
    append_segmented(lines, 'C_DETAILS', [-0.5, -1.3], [0.71, 0.71], [Z_FLOOR+0.85, Z_FLOOR+0.85]) # Shovel Handle
    append_segmented(lines, 'C_DETAILS', [-1.3, -1.5], [0.72, 0.72], [Z_FLOOR+0.85, Z_FLOOR+0.9])  # Spade Blade

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Generates the fully articulated frame matrix based on the absolute timestamp
        dynamic_rig = generate_jeep_dynamic(t_sec)
        
        # Absolute Origin Tracking: Locking the geometric True Center of the 3.3m vehicle
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.0
        
        # Starts explicitly from 115-degrees (Dramatic front-quarter aesthetic tracking the driving dynamics)
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
    # Anchor = 0.0. Total vehicle length is approx 3.3m. Height 1.4m.
    # Setting cam_span strictly to 3.2 to yield a 6.4m horizontal footprint.
    # Vertical bounds output 3.2 * 1.777 = 5.68m (x2 = 11.36m height allowed).
    # Perfectly frames the utilitarian static stance allowing room to observe the ground traverse.
    cam_span = 3.2
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.3), 
        ('C_HULL_DARK', C_HULL_DARK, 1.4, 1.0),
        ('C_HULL_MAIN', C_HULL_MAIN, 1.4, 1.0),
        ('C_DETAILS',   C_DETAILS,   1.3, 1.0),
        ('C_ACCENT',    C_ACCENT,    1.3, 1.0),
        ('C_WHEEL',     C_WHEEL,     1.6, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in dynamic_rig[c_key]:
            # Elevated +14 degrees to prominent display the open tub topology and steering elements
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-451a_REV1 // GROUND KINEMATICS: OPERATIONS RESEARCH", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // WILLYS MB JEEP MATRIX", color=C_HULL_DARK, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, f"[LOCOMOTIVE ALIGNMENT] 4-WHEEL SYNCHRONISATION MATRIX (V=2.0 m/s)", color=C_HULL_MAIN, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: TRUE TAILGATE SPARE ALIGNMENT / ACTIVE MECHANICS", color=C_DETAILS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-451a_REV1: WILLYS MB JEEP KINEMATICS [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Locomotive Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
