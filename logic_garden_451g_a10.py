"""
PROJECT: Logic Garden 451g (Exact Physical Construct // A-10 Thunderbolt II Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: A-10, WARTHOG, THUNDERBOLT II, AEROSPACE, KINEMATICS, WIREFRAME, ENGINEERING
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry.
- Exact structural integration: High-density 3D fuselage lofting, true tubular TF34 nacelles.
- True Asymmetric Mechanics: Offset nose gear (starboard), rotating 7-barrel GAU-8 cannon (port).
- Ground Kinematics: Real-time dynamic wheel rotation with translating baseplate (V = 10.0 m/s).
- Timeline: Continuous, flawless seamless 360-degree orbit starting from 115-degree dramatic front-quarter.
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
OUT_DIR = "frames_451g_a10"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- SYNCHRONISATION KINEMATICS --------
VELOCITY = 10.0  # m/s ground taxi translation
R_WHEEL_MAIN = 0.45 
R_WHEEL_NOSE = 0.35

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Translating Tarmac)

C_HULL_MAIN = '#94A3B8'          # Heavy Slate (Primary Rounded Fuselage / Wings)
C_HULL_DARK = '#475569'          # Machined Slate (Wing Pods, Struts, Tail Masts)
C_DETAILS   = '#1E293B'          # Carbon Slate (Heavy Ordnance, Pylons)
C_COCKPIT   = '#005599'          # Deep Marine (Bubble Canopy)
C_ENGINE    = '#111115'          # Indestructible Black (GAU-8 Matrix, Tyres)
C_ACCENT    = '#E11D48'          # Kinematic Red (TF34 Engine Fans)

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

def add_dynamic_wheel(lines_dict, col, cx, cy, cz, radius, width, theta_rot):
    t = np.linspace(0, 2*np.pi, 20, endpoint=False)
    R_y = np.array([[np.cos(theta_rot), 0, np.sin(theta_rot)], [0, 1, 0], [-np.sin(theta_rot), 0, np.cos(theta_rot)]])
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


# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (A-10 WARTHOG / HIGH-DENSITY SMOOTHING)
# ------------------------------------------------------------------
def generate_a10_dynamic(t_sec):
    lines = {
        'C_HULL_MAIN': [], 'C_HULL_DARK': [], 'C_DETAILS': [], 
        'C_COCKPIT': [], 'C_ENGINE': [], 'C_ACCENT': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. TRANSLATING BASEPLATE (Ground Taxi Matrix)
    # ==============================================================================
    Z_FLOOR = -2.5
    travel_offset = (t_sec * VELOCITY) % 4.0
    
    gx_range = np.linspace(-16.0, 16.0, 17)
    gy_range = np.linspace(-12.0, 12.0, 13)
    for gx in gx_range: 
        append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx - travel_offset), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: 
        append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. SEVERE 3D FUSELAGE SMOOTHING (True Array Lofting)
    # ==============================================================================
    x_st  = [ 8.0,  7.0,  5.5,  3.5,  1.0, -1.0, -3.0, -5.0, -7.0, -8.5]
    ry_st = [ 0.1,  0.6,  0.85, 0.95, 1.0,  1.0,  0.9,  0.7,  0.4,  0.1]
    rz_st = [ 0.1,  0.6,  0.9,  1.1,  1.2,  1.2,  1.1,  0.8,  0.5,  0.2]
    z_off = [ 0.0, -0.1,  0.0,  0.1,  0.1,  0.1,  0.2,  0.3,  0.5,  0.6]

    for i in range(len(x_st)-1):
        x1, x2 = x_st[i], x_st[i+1]
        t = np.linspace(0, 2*np.pi, 24, endpoint=False) # High density 24-point smoothing
        
        y1_ring = ry_st[i]*np.cos(t)
        z1_ring = rz_st[i]*np.sin(t) + z_off[i]
        y2_ring = ry_st[i+1]*np.cos(t)
        z2_ring = rz_st[i+1]*np.sin(t) + z_off[i+1]
        
        col = 'C_HULL_MAIN' if i % 2 == 0 else 'C_HULL_DARK'
        append_segmented(lines, col, [x1]*25, list(y1_ring)+[y1_ring[0]], list(z1_ring)+[z1_ring[0]])
        for k in range(24):
            append_segmented(lines, col, [x1, x2], [y1_ring[k], y2_ring[k]], [z1_ring[k], z2_ring[k]])

    # Rounded Nose Dome
    add_cylinder(lines, 'C_HULL_MAIN', cx=8.0, cy=0.0, cz=0.0, length=0.4, radius=0.1, axis='x', rings=3, t_count=24)

    # ==============================================================================
    # 3. HIGH-VISIBILITY BUBBLE CANOPY
    # ==============================================================================
    p_c_front = (6.0, 0.0, 0.8)
    p_c_top   = (5.0, 0.0, 1.8)
    p_c_rear  = (3.0, 0.0, 1.2)
    p_s_front = (5.5, 0.5, 0.6)
    p_s_mid   = (4.5, 0.7, 1.0)
    p_s_rear  = (3.5, 0.6, 0.9)

    add_sym_quad(lines, 'C_COCKPIT', p_c_front, p_s_front, p_s_mid, p_c_top, u_steps=4, v_steps=4)
    add_sym_quad(lines, 'C_COCKPIT', p_c_top, p_s_mid, p_s_rear, p_c_rear, u_steps=4, v_steps=4)

    # ==============================================================================
    # 4. ASYMMETRIC MECHANICS: 7-BARREL GAU-8 AVENGER (Offset Port)
    # ==============================================================================
    G_X = 8.0; G_Y = -0.2; G_Z = -0.3 # Explicit port offset
    theta_gun = t_sec * 6.0 # Rotating dynamically
    
    # 7 Independent Barrels Matrix
    for g_b in range(7):
        ang = theta_gun + (g_b * (2*np.pi / 7))
        b_y = G_Y + 0.1 * np.cos(ang)
        b_z = G_Z + 0.1 * np.sin(ang)
        append_segmented(lines, 'C_ENGINE', [G_X, G_X+1.2], [b_y, b_y], [b_z, b_z]) # Barrels
        
    # Barrel Clamps
    add_cylinder(lines, 'C_DETAILS', cx=G_X+0.3, cy=G_Y, cz=G_Z, length=0.1, radius=0.13, axis='x', rings=2, t_count=14)
    add_cylinder(lines, 'C_DETAILS', cx=G_X+0.9, cy=G_Y, cz=G_Z, length=0.1, radius=0.13, axis='x', rings=2, t_count=14)

    # ==============================================================================
    # 5. HIGH-MOUNT TF34 ENGINE NACELLES (High-Density Cylinders)
    # ==============================================================================
    for y_sign in [-1, 1]:
        ey = 1.6 * y_sign # Pushed outward slightly for rounded clearance
        ex = -4.5
        ez = 1.4
        er = 0.85 # Thickened nacelles to match the diagrams
        
        # Primary Outer Nacelle (24-point cylinder)
        add_cylinder(lines, 'C_HULL_MAIN', cx=ex, cy=ey, cz=ez, length=3.0, radius=er, axis='x', rings=6, t_count=24)
        
        # Internal Intake Lip & Fan Blades
        add_cylinder(lines, 'C_HULL_DARK', cx=ex+2.8, cy=ey, cz=ez, length=0.2, radius=er*0.9, axis='x', rings=2, t_count=24)
        add_cylinder(lines, 'C_ACCENT', cx=ex+2.6, cy=ey, cz=ez, length=0.0, radius=er*0.7, axis='x', rings=4, t_count=16) # Fan Map
        
        # Exhaust Cone
        add_cylinder(lines, 'C_ENGINE', cx=ex-0.4, cy=ey, cz=ez, length=0.8, radius=er*0.6, axis='x', rings=3, t_count=16)
        
        # Heavy Structural Pylon anchoring nacelle to fuselage
        add_quad_mesh(lines, 'C_HULL_DARK', (ex+2.0, 0.6*y_sign, 0.8), (ex, 0.6*y_sign, 0.8), 
                                            (ex, ey, ez), (ex+1.5, ey, ez), u_steps=3, v_steps=3)

    # ==============================================================================
    # 6. STRAIGHT DIHEDRAL WINGS & SPONSONS
    # ==============================================================================
    W_ROOT_X_FWD = 2.5; W_ROOT_X_AFT = -0.8
    W_TIP_X_FWD = 1.0; W_TIP_X_AFT = -0.5
    W_SPAN = 8.76
    W_Z_ROOT = -0.2
    W_Z_TIP = 0.4 

    # Sweeping Dihedral Wings with top and bottom aerofoil thickness
    add_sym_quad(lines, 'C_HULL_MAIN', (W_ROOT_X_FWD, 1.0, W_Z_ROOT+0.1), (W_ROOT_X_AFT, 1.0, W_Z_ROOT+0.1), 
                                       (W_TIP_X_AFT, W_SPAN, W_Z_TIP+0.05), (W_TIP_X_FWD, W_SPAN, W_Z_TIP+0.05), u_steps=8, v_steps=6)
    add_sym_quad(lines, 'C_HULL_DARK', (W_ROOT_X_FWD, 1.0, W_Z_ROOT-0.1), (W_ROOT_X_AFT, 1.0, W_Z_ROOT-0.1), 
                                       (W_TIP_X_AFT, W_SPAN, W_Z_TIP-0.05), (W_TIP_X_FWD, W_SPAN, W_Z_TIP-0.05), u_steps=8, v_steps=6)
    
    # Wing Sponsons (Landing Gear Pods at Y=+/- 2.6)
    for y_sign in [-1, 1]:
        sy = 2.6 * y_sign
        sz = W_Z_ROOT + ((W_Z_TIP - W_Z_ROOT) * (abs(sy) / W_SPAN)) - 0.2
        add_cylinder(lines, 'C_HULL_DARK', cx=-1.0, cy=sy, cz=sz, length=3.5, radius=0.45, axis='x', rings=5, t_count=16)
        
        # Heavy Ordnance Pylons & AGMs
        for p_y in [4.0, 5.5, 7.0]:
            p_z = W_Z_ROOT + ((W_Z_TIP - W_Z_ROOT) * (p_y / W_SPAN)) - 0.1
            py_sign = p_y * y_sign
            # Pylon Mount
            append_segmented(lines, 'C_DETAILS', [0.5, -0.2], [py_sign, py_sign], [p_z, p_z-0.3])
            # AGM/Bomb Cylinder
            add_cylinder(lines, 'C_DETAILS', cx=-0.4, cy=py_sign, cz=p_z-0.4, length=1.2, radius=0.15, axis='x', rings=3, t_count=8)

    # ==============================================================================
    # 7. H-TAIL EMPENNAGE
    # ==============================================================================
    # Massive transverse horizontal stabiliser
    add_sym_quad(lines, 'C_HULL_MAIN', (-7.0, 0.0, 1.0), (-8.5, 0.0, 1.0), (-8.5, 3.1, 1.0), (-7.5, 3.1, 1.0), u_steps=3, v_steps=6)
    
    # Twin Vertical Stabilisers mounted to the absolute tips
    add_sym_quad(lines, 'C_HULL_DARK', (-7.0, 3.1, 0.0), (-8.8, 3.1, 0.0), (-8.8, 3.1, 2.8), (-7.5, 3.1, 2.8), u_steps=4, v_steps=4)

    # ==============================================================================
    # 8. LIVE TRICYCLE LANDING GEAR KINEMATICS
    # ==============================================================================
    theta_main = (VELOCITY * t_sec) / R_WHEEL_MAIN
    theta_nose = (VELOCITY * t_sec) / R_WHEEL_NOSE

    # Asymmetric Nose Gear (Offset to Starboard explicitly)
    N_Y = 0.35
    append_segmented(lines, 'C_DETAILS', [6.5, 6.5], [N_Y, N_Y], [-0.5, Z_FLOOR+R_WHEEL_NOSE])
    add_dynamic_wheel(lines, 'C_ENGINE', cx=6.5, cy=N_Y, cz=Z_FLOOR+R_WHEEL_NOSE, radius=R_WHEEL_NOSE, width=0.2, theta_rot=theta_nose)

    # Main Gear Assembly (Deploying from sponsons)
    for y_sign in [-1, 1]:
        my = 2.7 * y_sign
        mx = 0.2
        append_segmented(lines, 'C_DETAILS', [mx, mx], [my, my], [-0.5, Z_FLOOR+R_WHEEL_MAIN])
        add_dynamic_wheel(lines, 'C_ENGINE', cx=mx, cy=my, cz=Z_FLOOR+R_WHEEL_MAIN, radius=R_WHEEL_MAIN, width=0.3, theta_rot=theta_main)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        dynamic_rig = generate_a10_dynamic(t_sec)
        
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

    # 100% VISIBILITY THRESHOLD AUDIT:
    # Anchor = 0.0. Wingspan 17.5m. Length 16.2m.
    cam_span = 12.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.6, 0.3), 
        ('C_HULL_MAIN', C_HULL_MAIN, 1.2, 1.0),
        ('C_HULL_DARK', C_HULL_DARK, 1.3, 1.0),
        ('C_DETAILS',   C_DETAILS,   1.2, 1.0),
        ('C_COCKPIT',   C_COCKPIT,   1.5, 1.0),
        ('C_ACCENT',    C_ACCENT,    1.5, 1.0),
        ('C_ENGINE',    C_ENGINE,    1.5, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in dynamic_rig[c_key]:
            # Elevated +14 degrees to cleanly survey the thick wings and offset front mechanics
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=14.0)
            render_queue.append((np.mean(depth), u, v, c_val, lw, alpha))

    # ABSOLUTE Z-SORT 
    render_queue.sort(key=lambda item: item[0], reverse=True)
    for depth, u, v, c, lw, a in render_queue:
        ax.plot(u, v, color=c, lw=lw, alpha=a)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (TOP HUD)
    # ------------------------------------------------------------------
    ui_t = cam_span * 1.45
    ax.add_patch(patches.Rectangle((-cam_span, ui_t), cam_span*2, cam_span*0.5, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_t, ui_t], color=C_TEXT, lw=6, zorder=81)

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-451g // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // A-10 THUNDERBOLT II MATRIX", color=C_HULL_DARK, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT / TAXI KINEMATICS (V=10.0m/s)", color=C_COCKPIT, fontsize=13, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: TRUE H-TAIL / ASYMMETRICAL GAU-8 CANNON / HIGH-DENSITY NACELLES", color=C_DETAILS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-451g: A-10 WARTHOG KINEMATICS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
