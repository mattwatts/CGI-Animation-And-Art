"""
PROJECT: Logic Garden 450z (Exact Physical Construct // M1 Abrams Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: M1 ABRAMS, TANK, ARMOUR, GROUND KINEMATICS, DYNAMIC TREADS, ENGINEERING
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry.
- Exact structural integration: Flawless dynamic track system matching wheel velocities.
- Perfect Mechanical Synchronisation: V = 2.0m/s. Tracks and wheels precisely locked seamlessly.
- Strict Bounds Protocol: Core locked at origin. cam_span scaled to 7.5.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from absolute 115-degree dramatic front-quarter angle.
- Daylight Palette (White Substrate / High-Contrast Edge Geometry).
- Purged Jargon. Australian spelling conventions (maths, colour, kilometres, armour, synchronisation).
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
OUT_DIR = "frames_450z_abrams"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- SYNCHRONISATION KINEMATICS --------
VELOCITY = 2.0  # m/s backward grid translation
# Tuning wheel radii so they perfectly cleanly loop over 24 seconds (48m travel distance)
R_WHEEL = 48.0 / (2 * np.pi * 22)    # approx 0.347m (22 perfect rotations)
R_IDLER = 48.0 / (2 * np.pi * 25)    # approx 0.306m (25 perfect rotations)
R_SPROCK = 48.0 / (2 * np.pi * 22)   # approx 0.347m (22 perfect rotations)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Translating Ground Plane)

C_HULL_MAIN = '#94A3B8'          # Heavy Slate (Primary Armour Panels)
C_HULL_DARK = '#475569'          # Machined Slate (Side Skirts, Engine Deck)
C_DETAILS   = '#1E293B'          # Carbon Slate (Road Wheels, Track Edges, Bustle Rack)
C_WEAPON    = '#111115'          # Indestructible Black (120mm Cannon, M2 .50 Calibre, Track Pads)
C_OPTICS    = '#E11D48'          # Kinematic Red (Thermal Sights, Laser Rangefinders)

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
    # Sovereign Symmetry Protocol explicitly mirroring Y components
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

def add_dynamic_wheel(lines_dict, col, cx, cy, cz, radius, width, theta_rot):
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
        
        for s in range(0, 20, 2): 
            append_segmented(lines_dict, col, [hpts[0][s]+cx, pts[0][s]+cx], [hpts[1][s]+cy, pts[1][s]+cy], [hpts[2][s]+cz, pts[2][s]+cz])
            
    for i in range(20):
        p1 = np.dot(R_y, np.array([radius * np.cos(t[i]), y_faces[0], radius * np.sin(t[i])]))
        p2 = np.dot(R_y, np.array([radius * np.cos(t[i]), y_faces[1], radius * np.sin(t[i])]))
        append_segmented(lines_dict, col, [p1[0]+cx, p2[0]+cx], [p1[1]+cy, p2[1]+cy], [p1[2]+cz, p2[2]+cz])

def add_dynamic_tracks(lines_dict, col_edge, col_pad, t_sec, velocity, y_inner, y_outer):
    # Absolute mathematical perimeter bounding for continuous tracks
    path_x = []
    path_z = []
    
    # 1. Top Edge
    for p in np.linspace(0, 1, 20, endpoint=False):
        path_x.append((1-p)*(-4.0) + p*(3.5))
        path_z.append((1-p)*0.947 + p*(0.806))
        
    # 2. Front Idler Arc (90 deg to -90 deg)
    for a in np.linspace(np.pi/2, -np.pi/2, 12, endpoint=False):
        path_x.append(3.5 + 0.306 * np.cos(a))
        path_z.append(0.5 + 0.306 * np.sin(a))
        
    # 3. Front Diagonal (Idler bottom to Road Wheel Front)
    for p in np.linspace(0, 1, 5, endpoint=False):
        path_x.append((1-p)*3.5 + p*2.5)
        path_z.append((1-p)*0.194 + p*0.0)
        
    # 4. Ground Contact Edge (Flat along Z=0)
    for p in np.linspace(0, 1, 30, endpoint=False):
        path_x.append((1-p)*2.5 + p*(-3.2))
        path_z.append(0.0)
        
    # 5. Rear Diagonal (Road Wheel Rear to Sprocket bottom)
    for p in np.linspace(0, 1, 6, endpoint=False):
        path_x.append((1-p)*(-3.2) + p*(-4.0))
        path_z.append((1-p)*0.0 + p*(0.6 - 0.347))
        
    # 6. Rear Sprocket Arc (-90 deg to -270 deg / +90 deg equiv)
    for a in np.linspace(-np.pi/2, -3*np.pi/2, 16, endpoint=False):
        path_x.append(-4.0 + 0.347 * np.cos(a))
        path_z.append(0.6 + 0.347 * np.sin(a))
        
    path_x = np.array(path_x)
    path_z = np.array(path_z)
    
    # Pre-calculating path physics and distances
    dx = np.diff(np.append(path_x, path_x[0]))
    dz = np.diff(np.append(path_z, path_z[0]))
    dists = np.sqrt(dx**2 + dz**2)
    cum_dists = np.insert(np.cumsum(dists), 0, 0)
    L = cum_dists[-1]
    
    # Draw solid rubber track boundaries covering internal wheels
    append_sym(lines_dict, col_edge, list(path_x)+[path_x[0]], [y_inner]*(len(path_x)+1), list(path_z)+[path_z[0]])
    append_sym(lines_dict, col_edge, list(path_x)+[path_x[0]], [y_outer]*(len(path_x)+1), list(path_z)+[path_z[0]])
    
    # Array computation for dynamically translating grousers locked to tank velocity
    N_pads = 85
    spacing = L / N_pads
    shift = (velocity * t_sec) % L
    
    for i in range(N_pads):
        d = (i * spacing + shift) % L
        
        idx = np.searchsorted(cum_dists, d) - 1
        if idx < 0: idx = 0
        if idx >= len(dists): idx = len(dists) - 1
        
        remainder = d - cum_dists[idx]
        ratio = remainder / dists[idx] if dists[idx] > 0 else 0
        
        x1, z1 = path_x[idx], path_z[idx]
        x2, z2 = path_x[(idx+1)%len(path_x)], path_z[(idx+1)%len(path_z)]
        
        px = x1 + ratio * (x2 - x1)
        pz = z1 + ratio * (z2 - z1)
        
        # Heavy transverse track lines natively mirrored via append_sym
        append_sym(lines_dict, col_pad, [px, px], [y_inner, y_outer], [pz, pz])

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (M1 ABRAMS DYNAMIC TANK)
# ------------------------------------------------------------------
def generate_abrams_dynamic(t_sec):
    lines = {
        'C_HULL_MAIN': [], 'C_HULL_DARK': [], 'C_DETAILS': [], 
        'C_WEAPON': [], 'C_OPTICS': [], 'C_GRID': []
    }

    # 1. BASEPLATE ENVELOPE (TRANSLATING DIRT/TARMAC GRID)
    Z_FLOOR = 0.0
    travel_offset = (t_sec * VELOCITY) % 1.0  
    
    gx_range = np.linspace(-10.0, 10.0, 21)
    gy_range = np.linspace(-6.0, 6.0, 13)
    for gx in gx_range: 
        shift_x = gx - travel_offset
        append_segmented(lines, 'C_GRID', np.full_like(gy_range, shift_x), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: 
        append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))
    
    # ==============================================================================
    # 2. DYNAMIC TRACK MATRIX & SUSPENSION
    # ==============================================================================
    theta_wheel = (VELOCITY * t_sec) / R_WHEEL
    theta_idler = (VELOCITY * t_sec) / R_IDLER
    theta_sprock = (VELOCITY * t_sec) / R_SPROCK

    # Emplacing the dynamic wheels within the chassis flanks
    wheel_x = np.linspace(2.5, -3.2, 7)
    for y_sign in [-1, 1]:
        cy = 1.7 * y_sign
        for wx in wheel_x:
            add_dynamic_wheel(lines, 'C_DETAILS', cx=wx, cy=cy, cz=Z_FLOOR+R_WHEEL, radius=R_WHEEL, width=0.4, theta_rot=theta_wheel)
        add_dynamic_wheel(lines, 'C_DETAILS', cx=3.5, cy=cy, cz=Z_FLOOR+0.5, radius=R_IDLER, width=0.4, theta_rot=theta_idler)
        add_dynamic_wheel(lines, 'C_DETAILS', cx=-4.0, cy=cy, cz=Z_FLOOR+0.6, radius=R_SPROCK, width=0.4, theta_rot=theta_sprock)

    # Natively constructing the live continuous tracks tracking over the suspension
    add_dynamic_tracks(lines, 'C_DETAILS', 'C_WEAPON', t_sec, VELOCITY, 1.5, 1.9)

    # ==============================================================================
    # 3. HULL CHASSIS & HEAVY SIDE SKIRTS
    # ==============================================================================
    add_sym_quad(lines, 'C_HULL_MAIN', (3.8, 1.0, 0.5), (2.8, 1.0, 1.1), (2.8, 1.8, 1.1), (3.8, 1.8, 0.5), u_steps=2, v_steps=2) 
    add_sym_quad(lines, 'C_HULL_MAIN', (3.8, 0.0, 0.5), (2.8, 0.0, 1.1), (2.8, 1.0, 1.1), (3.8, 1.0, 0.5), u_steps=2, v_steps=2) 
    add_sym_quad(lines, 'C_HULL_DARK', (3.8, 0.0, 0.5), (3.3, 0.0, 0.2), (3.3, 1.5, 0.2), (3.8, 1.5, 0.5), u_steps=2, v_steps=1) 

    add_sym_quad(lines, 'C_HULL_MAIN', (2.8, 0.0, 1.1), (-4.4, 0.0, 1.1), (-4.4, 1.5, 1.1), (2.8, 1.5, 1.1), u_steps=6, v_steps=3)
    
    sk = np.linspace(3.4, -4.2, 8)
    for i in range(len(sk)-1):
        add_sym_quad(lines, 'C_HULL_DARK', (sk[i], 1.9, 1.1), (sk[i+1]-0.05, 1.9, 1.1), (sk[i+1]-0.05, 1.95, 0.4), (sk[i], 1.95, 0.4), u_steps=2, v_steps=2)

    add_sym_quad(lines, 'C_HULL_DARK', (-2.0, 0.0, 1.15), (-4.2, 0.0, 1.15), (-4.2, 1.0, 1.15), (-2.0, 1.0, 1.15), u_steps=4, v_steps=3)
    add_sym_quad(lines, 'C_HULL_MAIN', (-4.4, 0.0, 1.1), (-4.4, 0.0, 0.2), (-4.4, 1.5, 0.2), (-4.4, 1.5, 1.1), u_steps=2, v_steps=2)

    # ==============================================================================
    # 4. CHOBHAM COMPOSITE TURRET MATRIX
    # ==============================================================================
    add_sym_quad(lines, 'C_HULL_MAIN', (1.0, 0.3, 1.8), (0.8, 1.4, 1.8), (1.5, 1.2, 1.4), (1.5, 0.4, 1.4), u_steps=3, v_steps=3)
    add_sym_quad(lines, 'C_HULL_MAIN', (1.5, 0.4, 1.4), (1.5, 1.2, 1.4), (1.2, 1.3, 1.15), (1.2, 0.4, 1.15), u_steps=3, v_steps=2) 
    add_sym_quad(lines, 'C_HULL_MAIN', (0.8, 1.4, 1.8), (-2.8, 1.4, 1.8), (-2.8, 1.3, 1.15), (1.2, 1.3, 1.15), u_steps=4, v_steps=2)
    add_sym_quad(lines, 'C_HULL_MAIN', (1.0, 0.0, 1.8), (-2.8, 0.0, 1.8), (-2.8, 1.4, 1.8), (1.0, 1.4, 1.8), u_steps=4, v_steps=3)
    
    add_sym_quad(lines, 'C_DETAILS', (-2.8, 0.0, 1.8), (-3.6, 0.0, 1.8), (-3.6, 1.3, 1.8), (-2.8, 1.4, 1.8), u_steps=3, v_steps=2)
    add_sym_quad(lines, 'C_DETAILS', (-2.8, 0.0, 1.2), (-3.6, 0.0, 1.2), (-3.6, 1.3, 1.2), (-2.8, 1.3, 1.2), u_steps=3, v_steps=2)
    for bx in [-3.0, -3.3, -3.6]: 
        append_sym(lines, 'C_DETAILS', [bx, bx], [0.0, 1.3], [1.2, 1.8])

    # ==============================================================================
    # 5. WEAPONRY (120mm M256 Smoothbore Cannon)
    # ==============================================================================
    add_quad_mesh(lines, 'C_HULL_DARK', (1.0, 0.3, 1.8), (1.0, -0.3, 1.8), (1.4, -0.4, 1.2), (1.4, 0.4, 1.2), u_steps=2, v_steps=2)
    add_cylinder(lines, 'C_WEAPON', cx=1.4, cy=0.0, cz=1.5, length=1.0, radius=0.15, axis='x', rings=3, t_count=8)
    add_cylinder(lines, 'C_WEAPON', cx=2.4, cy=0.0, cz=1.5, length=1.2, radius=0.22, axis='x', rings=4, t_count=12) 
    add_cylinder(lines, 'C_WEAPON', cx=3.6, cy=0.0, cz=1.5, length=2.8, radius=0.12, axis='x', rings=6, t_count=8)
    add_cylinder(lines, 'C_WEAPON', cx=6.3, cy=0.0, cz=1.5, length=0.15, radius=0.14, axis='x', rings=2, t_count=8)

    add_cylinder(lines, 'C_WEAPON', cx=0.5, cy=0.6, cz=2.0, length=1.2, radius=0.03, axis='x', rings=2, t_count=4)
    add_quad_mesh(lines, 'C_WEAPON', (0.5, 0.55, 1.95), (0.5, 0.65, 1.95), (-0.2, 0.65, 1.95), (-0.2, 0.55, 1.95), u_steps=2, v_steps=2)

    # ==============================================================================
    # 6. SENSORS & HATCHES
    # ==============================================================================
    add_cylinder(lines, 'C_OPTICS', cx=0.5, cy=-0.8, cz=1.8, length=0.4, radius=0.15, axis='z', rings=3, t_count=8)
    add_quad_mesh(lines, 'C_HULL_MAIN', (1.0, 0.3, 1.8), (1.0, 0.7, 1.8), (0.7, 0.7, 2.0), (0.7, 0.3, 2.0), u_steps=2, v_steps=2)
    add_quad_mesh(lines, 'C_OPTICS', (1.01, 0.4, 1.85), (1.01, 0.6, 1.85), (1.01, 0.6, 1.95), (1.01, 0.4, 1.95), u_steps=1, v_steps=1)
    add_cylinder(lines, 'C_DETAILS', cx=0.0, cy=0.6, cz=1.8, length=0.1, radius=0.35, axis='z', rings=2, t_count=12)
    add_cylinder(lines, 'C_DETAILS', cx=0.2, cy=-0.4, cz=1.8, length=0.05, radius=0.3, axis='z', rings=2, t_count=12)

    return lines

# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        dynamic_rig = generate_abrams_dynamic(t_sec)

        # Absolute Origin Tracking
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.0
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

    cam_span = 7.5
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.3), 
        ('C_HULL_DARK', C_HULL_DARK, 1.4, 1.0),
        ('C_HULL_MAIN', C_HULL_MAIN, 1.4, 1.0),
        ('C_DETAILS',   C_DETAILS,   1.3, 1.0),
        ('C_WEAPON',    C_WEAPON,    1.5, 1.0),
        ('C_OPTICS',    C_OPTICS,    1.8, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in dynamic_rig[c_key]:
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=16.0)
            render_queue.append((np.mean(depth), u, v, c_val, lw, alpha))

    render_queue.sort(key=lambda item: item[0], reverse=True)
    for depth, u, v, c, lw, a in render_queue:
        ax.plot(u, v, color=c, lw=lw, alpha=a)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (TOP HUD)
    # ------------------------------------------------------------------
    ui_t = cam_span * 1.45
    ax.add_patch(patches.Rectangle((-cam_span, ui_t), cam_span*2, cam_span*0.5, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_t, ui_t], color=C_TEXT, lw=6, zorder=81)

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-450z // GROUND KINEMATICS: HEAVY ARMOUR ARCHITECTURE", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // M1 ABRAMS TANK MATRIX", color=C_HULL_DARK, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT / LIVE DYNAMIC LOCOMOTION (V=2.0m/s)", color=C_WEAPON, fontsize=13, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: 120MM SMOOTHBORE / CHOBHAM COMPOSITE TURRET / ACTIVE TRACKS", color=C_DETAILS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-450z: M1 ABRAMS DYNAMIC TRACK TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Armour Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
