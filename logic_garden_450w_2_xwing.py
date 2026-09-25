"""
PROJECT: Logic Garden 450w - Revision 1 (Exact Physical Construct // T-65 X-wing Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: X-WING, STAR WARS, INCOM, AEROSPACE, WIREFRAME, ENGINEERING, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry.
- Exact structural integration: Astromech oriented vertical, engines/guns bound flawlessly to S-foil roots/tips.
- Asymmetry Purge: Strict add_sym_cylinder macro eliminates right-side flattened malformations.
- Active Kinematic Flight: Z-floor tracks backward dynamically simulating sustained Mach/aerospace velocity.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from absolute 115-degree front-quarter angle.
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
OUT_DIR = "frames_450w_xwing"
os.makedirs(OUT_DIR, exist_ok=True)

VELOCITY = 30.0  # m/s aerospace grid translation

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Translating Aerospace Plane)

C_HULL_MAIN = '#94A3B8'          # Heavy Slate (Primary Fuselage & S-Foils)
C_HULL_DARK = '#475569'          # Machined Slate (Trench walls, Engine Intakes)
C_DETAILS   = '#1E293B'          # Carbon Slate (Laser Cannons, Astromech, S-foil Actuators)
C_COCKPIT   = '#111115'          # Indestructible Black (Cockpit Glazing / Pilot Seat)
C_ENGINE    = '#E11D48'          # Kinematic Red (Fusial Thrust Plumes)

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
    # Absolute Symmetry Protocol for discrete coordinate points
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

# FIXED: Pure cylinder construction eliminating symmetry conflicts
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

def add_dome(lines_dict, col, cx, cy, cz, radius, axis='z', dir=1, rings=4, t_count=16):
    p_step = np.linspace(0, np.pi/2, rings)
    for p in p_step:
        r_s = radius * np.cos(p)
        h_s = radius * np.sin(p) * dir
        t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
        if axis == 'z':
            ix, iy, iz = cx + r_s*np.cos(t), cy + r_s*np.sin(t), np.full_like(t, cz + h_s)
            append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        rr = radius * np.cos(p_step)
        hh = radius * np.sin(p_step) * dir
        if axis == 'z':
            sx, sy, sz = cx + rr*np.cos(a), cy + rr*np.sin(a), cz + hh
            append_segmented(lines_dict, col, list(sx), list(sy), list(sz))

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (T-65 X-WING FLIGHT OPERATIONS)
# ------------------------------------------------------------------
def generate_xwing_dynamic(t_sec):
    lines = {
        'C_HULL_MAIN': [], 'C_HULL_DARK': [], 'C_DETAILS': [], 
        'C_COCKPIT': [], 'C_ENGINE': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. TRANSLATING AEROSPACE GRID (Kinetic Flight Simulation)
    # ==============================================================================
    Z_FLOOR = -4.0
    travel_offset = (t_sec * VELOCITY) % 2.0  # 2.0m loop grid
    
    gx_range = np.linspace(-15.0, 15.0, 16)
    gy_range = np.linspace(-10.0, 10.0, 11)
    
    for gx in gx_range: 
        shift_x = gx - travel_offset
        append_segmented(lines, 'C_GRID', np.full_like(gy_range, shift_x), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: 
        append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. CONTINUOUS FUSELAGE LOFTING (Precision Hex-Hull)
    # ==============================================================================
    x_st = [6.7, 4.5, 1.5, -1.0, -4.0, -6.5]
    Y_w  = [0.05, 0.35, 0.55, 0.70, 0.70, 0.50]
    Z_t  = [0.05, 0.25, 0.45, 0.75, 0.80, 0.60]
    Z_b  = [-0.05,-0.15,-0.25,-0.40,-0.40,-0.30]
    
    for i in range(len(x_st)-1):
        x1, x2 = x_st[i], x_st[i+1]
        
        # Exact Hexagonal Mapping
        y1_pts = [0, Y_w[i], Y_w[i], 0, -Y_w[i], -Y_w[i]]
        z1_pts = [Z_t[i], Z_t[i]*0.5, Z_b[i]*0.5, Z_b[i], Z_b[i]*0.5, Z_t[i]*0.5]
        
        y2_pts = [0, Y_w[i+1], Y_w[i+1], 0, -Y_w[i+1], -Y_w[i+1]]
        z2_pts = [Z_t[i+1], Z_t[i+1]*0.5, Z_b[i+1]*0.5, Z_b[i+1], Z_b[i+1]*0.5, Z_t[i+1]*0.5]

        append_segmented(lines, 'C_HULL_MAIN', [x1]*7, y1_pts+[y1_pts[0]], z1_pts+[z1_pts[0]])
        for k in range(6):
            append_segmented(lines, 'C_HULL_MAIN', [x1, x2], [y1_pts[k], y2_pts[k]], [z1_pts[k], z2_pts[k]])
        
        if i == len(x_st)-2: # Append massive tail flat-plate closure
            append_segmented(lines, 'C_HULL_MAIN', [x2]*7, y2_pts+[y2_pts[0]], z2_pts+[z2_pts[0]])

    # ==============================================================================
    # 3. HIGH-ELEVATION COCKPIT & R2 ASTROMECH UNIT
    # ==============================================================================
    # Deep Faceted Cockpit Geometry
    p_c_front = (2.0, 0.0, 0.45)
    p_c_top   = (0.5, 0.0, 1.05)
    p_c_rear  = (-0.8, 0.0, 0.8) # Placed correctly before astromech socket
    
    p_s_front = (1.5, 0.35, 0.55)
    p_s_mid   = (0.5, 0.45, 0.8)
    p_s_rear  = (-0.8, 0.5, 0.75)

    add_sym_quad(lines, 'C_COCKPIT', p_c_front, p_s_front, p_s_mid, p_c_top, u_steps=3, v_steps=3)
    add_sym_quad(lines, 'C_COCKPIT', p_c_top, p_s_mid, p_s_rear, p_c_rear, u_steps=3, v_steps=3)
    
    # Internal Pilot Seat details
    add_sym_quad(lines, 'C_DETAILS', (0.8, 0.2, 0.3), (0.0, 0.2, 0.3), (0.0, 0.2, 0.8), (0.8, 0.2, 0.8), u_steps=2, v_steps=2)

    # R2-Series Astromech firmly standing behind canopy
    add_cylinder(lines, 'C_DETAILS', cx=-1.2, cy=0.0, cz=0.75, length=0.3, radius=0.2, axis='z', rings=3, t_count=12)
    add_dome(lines, 'C_DETAILS', cx=-1.2, cy=0.0, cz=1.05, radius=0.2, axis='z', dir=1, rings=3, t_count=12)

    # ==============================================================================
    # 4. DEPLOYED S-FOIL MATRIX (ATTACK POSITION)
    # ==============================================================================
    S_ANGLE = np.radians(15.0)
    W_SPAN = 5.88
    
    # Kinematic Tips
    z_tip_up = 0.2 + (W_SPAN - 0.7) * np.sin(S_ANGLE)
    z_tip_dn = -0.2 - (W_SPAN - 0.7) * np.sin(S_ANGLE)
    
    # Upper S-Foil Quad (Accurate root bounds)
    add_sym_quad(lines, 'C_HULL_MAIN',
        (-0.5, 0.7, 0.2), (-5.0, 0.7, 0.2),               # Root 
        (-2.5, W_SPAN, z_tip_up), (-0.5, W_SPAN, z_tip_up), # Tip 
        u_steps=5, v_steps=6)
    
    # Lower S-Foil Quad
    add_sym_quad(lines, 'C_HULL_MAIN',
        (-0.5, 0.7, -0.2), (-5.0, 0.7, -0.2),
        (-2.5, W_SPAN, z_tip_dn), (-0.5, W_SPAN, z_tip_dn),
        u_steps=5, v_steps=6)

    # ==============================================================================
    # 5. INCOM FUSIAL THRUST ENGINES (Bolted accurately to wings)
    # ==============================================================================
    z_eng_up = 0.2 + (1.6 - 0.7) * np.sin(S_ANGLE)
    z_eng_dn = -0.2 - (1.6 - 0.7) * np.sin(S_ANGLE)

    # Upper Port/Starboard Engines
    add_sym_cylinder(lines, 'C_HULL_MAIN', cx=-2.0, cy=1.6, cz=z_eng_up, length=2.0, radius=0.45, axis='x') # Front Intake
    add_sym_cylinder(lines, 'C_HULL_DARK', cx=-5.0, cy=1.6, cz=z_eng_up, length=3.0, radius=0.40, axis='x') # Rear Exhaust Main
    add_sym_cylinder(lines, 'C_ENGINE',    cx=-8.0, cy=1.6, cz=z_eng_up, length=3.0, radius=0.25, axis='x') # Extended Thrust Plumes

    # Lower Port/Starboard Engines
    add_sym_cylinder(lines, 'C_HULL_MAIN', cx=-2.0, cy=1.6, cz=z_eng_dn, length=2.0, radius=0.45, axis='x') 
    add_sym_cylinder(lines, 'C_HULL_DARK', cx=-5.0, cy=1.6, cz=z_eng_dn, length=3.0, radius=0.40, axis='x') 
    add_sym_cylinder(lines, 'C_ENGINE',    cx=-8.0, cy=1.6, cz=z_eng_dn, length=3.0, radius=0.25, axis='x') 
        
    # ==============================================================================
    # 6. TAIM & BAK KX9 LASER CANNONS (Locked accurately to wingtips)
    # ==============================================================================
    # Upper Cannons
    add_sym_cylinder(lines, 'C_HULL_DARK', cx=-3.5, cy=W_SPAN, cz=z_tip_up, length=2.0, radius=0.15, axis='x') # Power Generator Aft Pod
    add_sym_cylinder(lines, 'C_DETAILS',   cx=-1.5, cy=W_SPAN, cz=z_tip_up, length=7.0, radius=0.06, axis='x') # Very long slim barrel extending physical
    add_sym_cylinder(lines, 'C_DETAILS',   cx=5.5,  cy=W_SPAN, cz=z_tip_up, length=0.5, radius=0.15, axis='x') # Flash Suppressor Bulb
    
    # Lower Cannons
    add_sym_cylinder(lines, 'C_HULL_DARK', cx=-3.5, cy=W_SPAN, cz=z_tip_dn, length=2.0, radius=0.15, axis='x') 
    add_sym_cylinder(lines, 'C_DETAILS',   cx=-1.5, cy=W_SPAN, cz=z_tip_dn, length=7.0, radius=0.06, axis='x') 
    add_sym_cylinder(lines, 'C_DETAILS',   cx=5.5,  cy=W_SPAN, cz=z_tip_dn, length=0.5, radius=0.15, axis='x') 

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        dynamic_rig = generate_xwing_dynamic(t_sec)
        
        # Absolute Origin Tracking: Locking the geometric True Center of the 13.4m airframe
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.0
        
        # Starts explicitly from 115-degrees (Dramatic front-quarter aesthetic tracking flight kinematics)
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
    cam_span = 9.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.6, 0.3), 
        ('C_HULL_MAIN', C_HULL_MAIN, 1.2, 1.0),
        ('C_HULL_DARK', C_HULL_DARK, 1.3, 1.0),
        ('C_DETAILS',   C_DETAILS,   1.2, 1.0),
        ('C_COCKPIT',   C_COCKPIT,   1.8, 1.0),
        ('C_ENGINE',    C_ENGINE,    1.5, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in dynamic_rig[c_key]:
            # Elevated +14 degrees to powerfully frame the flight dynamics and S-Foil arrays
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-450w // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // T-65 X-WING STARFIGHTER MATRIX", color=C_HULL_DARK, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT / LIVE FLIGHT LOOP (V=30.0m/s)", color=C_ENGINE, fontsize=13, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: TRUE S-FOIL STRUCTURAL MOUNTS / VERTICAL ASTROMECH NODE", color=C_DETAILS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-450w: T-65 X-WING DYNAMIC TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
