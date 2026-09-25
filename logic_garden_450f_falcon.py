"""
PROJECT: Logic Garden 450f (Exact Physical Construct // Millennium Falcon YT-1300 Matrix - BARE METAL)
FORMAT: YouTube Shorts (1080x1920)
METADATA: STAR WARS, MILLENNIUM FALCON, UNDECLARED FREIGHTER, SPACECRAFT, WIREFRAME, ENGINEERING, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Dynamic saucer, exact orthogonal starboard cockpit bounds, and structured high-density mandibles.
- Strict Bounds Protocol: Core anchor locked to X=4.0. cam_span dynamically set to 22.0, assuring ABSOLUTE 100% frame preservation.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from absolute Side Profile.
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
OUT_DIR = "frames_450f_falcon"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Baseplate Reference)

C_HULL_MAIN = '#94A3B8'          # Heavy Falcon Slate (Primary Panels)
C_HULL_DARK = '#475569'          # Machined Steel (Vents, Dark Plates)
C_DETAILS   = '#1E293B'          # Carbon Slate (Trench Pipes, Mechanical Substrate)
C_COCKPIT   = '#111115'          # Indestructible Black (Canopy Glass)
C_THRUSTER  = '#00D2FF'          # High Engine Blue (Sublight Engine Glow Tensor)
C_LASER     = '#FF3300'          # Intense Red (Accent geometry for Quad Cannons)

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

def append_segmented(lines_dict, key, xs, ys, zs, off=(0,0,0), scale_x=1.0):
    dx, dy, dz = off
    xs, ys, zs = list(xs), list(ys), list(zs)
    for i in range(len(xs) - 1):
        x1 = xs[i] * scale_x + dx
        x2 = xs[i+1] * scale_x + dx
        lines_dict[key].append(([x1, x2], [ys[i]+dy, ys[i+1]+dy], [zs[i]+dz, zs[i+1]+dz]))

# ------------------------------------------------------------------
# GEOMETRIC PRIMITIVES
# ------------------------------------------------------------------
def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='z', rings=6, t_count=16, off=(0,0,0)):
    t = np.linspace(0, 2*np.pi, t_count+1)
    steps = np.linspace(0, length, rings)
    for s in steps:
        if axis == 'y':  ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + s), cz + radius*np.sin(t)
        elif axis == 'x': ix, iy, iz = np.full_like(t, cx + s), cy + radius*np.cos(t), cz + radius*np.sin(t)
        else:             ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), np.full_like(t, cz + s)
        append_segmented(lines_dict, col, ix, iy, iz, off)
    for a in t[:-1][::max(1, t_count//8)]:
        if axis == 'y':   sx, sy, sz = [cx + radius*np.cos(a)]*rings, cy + steps, [cz + radius*np.sin(a)]*rings
        elif axis == 'x': sx, sy, sz = cx + steps, [cy + radius*np.cos(a)]*rings, [cz + radius*np.sin(a)]*rings
        else:             sx, sy, sz = [cx + radius*np.cos(a)]*rings, [cy + radius*np.sin(a)]*rings, cz + steps
        append_segmented(lines_dict, col, sx, sy, sz, off)

def add_cylinder_oriented(lines_dict, col, p1, p2, r1, r2, rings=8, t_count=16, off=(0,0,0)):
    p1, p2 = np.array(p1), np.array(p2)
    v = p2 - p1
    L = np.linalg.norm(v)
    if L == 0: return
    v = v / L
    up = np.array([0.0, 0.0, 1.0])
    if abs(v[2]) > 0.99: up = np.array([1.0, 0.0, 0.0])
    
    xu = np.cross(up, v); xu = xu / np.linalg.norm(xu)
    yu = np.cross(v, xu); yu = yu / np.linalg.norm(yu)
    
    t = np.linspace(0, 2*np.pi, t_count+1)
    steps = np.linspace(0, 1, rings)
    
    for s in steps:
        C = p1 + s * v * L
        r = r1 + s * (r2 - r1)
        px = C[0] + r*np.cos(t)*xu[0] + r*np.sin(t)*yu[0]
        py = C[1] + r*np.cos(t)*xu[1] + r*np.sin(t)*yu[1]
        pz = C[2] + r*np.cos(t)*xu[2] + r*np.sin(t)*yu[2]
        append_segmented(lines_dict, col, px, py, pz, off)
        
    for a in t[:-1]:
        sx, sy, sz = [], [], []
        for s in steps:
            C = p1 + s * v * L
            r = r1 + s * (r2 - r1)
            sx.append(C[0] + r*np.cos(a)*xu[0] + r*np.sin(a)*yu[0])
            sy.append(C[1] + r*np.cos(a)*xu[1] + r*np.sin(a)*yu[1])
            sz.append(C[2] + r*np.cos(a)*xu[2] + r*np.sin(a)*yu[2])
        append_segmented(lines_dict, col, sx, sy, sz, off)

def add_quad_mesh(lines_dict, col, p1, p2, p3, p4, u_steps=8, v_steps=8, off=(0,0,0)):
    p1, p2, p3, p4 = map(np.array, (p1, p2, p3, p4))
    for i in range(v_steps + 1):
        v = i / v_steps
        start = p1 * (1-v) + p4 * v
        end   = p2 * (1-v) + p3 * v
        pts = [start * (1-u) + end * u for u in np.linspace(0, 1, u_steps+1)]
        append_segmented(lines_dict, col, [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts], off)
    for i in range(u_steps + 1):
        u = i / u_steps
        start = p1 * (1-u) + p2 * u
        end   = p4 * (1-u) + p3 * u
        pts = [start * (1-v) + end * v for v in np.linspace(0, 1, v_steps+1)]
        append_segmented(lines_dict, col, [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts], off)

# ------------------------------------------------------------------
# STATIC SUPERSTRUCTURE BUILDERS (YT-1300 MATRIX)
# ------------------------------------------------------------------
def generate_falcon_static():
    lines = {
        'C_HULL_MAIN': [], 'C_HULL_DARK': [], 'C_DETAILS': [], 
        'C_COCKPIT': [], 'C_THRUSTER': [], 'C_LASER': [], 'C_GRID': []
    }

    # 1. BASEPLATE ENVELOPE (REFERENCE GRID)
    # Scales dynamically across the immense 35x27-metre Cartesian substrate
    gx_range = np.linspace(-15.0, 25.0, 21)
    gy_range = np.linspace(-20.0, 20.0, 21)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, -4.5))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, -4.5))

    # ==============================================================================
    # 2. THE PRIMARY SAUCER CHASSIS (Scaled 1.2x to equal true dimensions)
    # ==============================================================================
    r_z_profile = [
        (0.0, 2.4), (2.4, 2.4), (12.0, 1.0),
        (12.0, 0.6), (12.6, 0.6), (12.6, -0.6), (12.0, -0.6),
        (12.0, -1.0), (2.4, -2.4), (0.0, -2.4)
    ]
    
    t_s = np.linspace(0, 2*np.pi, 50)
    for i in range(len(r_z_profile)-1):
        r1, z1 = r_z_profile[i]
        r2, z2 = r_z_profile[i+1]
        for a in t_s[:-1][::2]: # Radial braces
            append_segmented(lines, 'C_HULL_MAIN', [r1*np.cos(a), r2*np.cos(a)], [r1*np.sin(a), r2*np.sin(a)], [z1, z2])
        # Latitudinal structural plates
        gx1, gy1 = r1 * np.cos(t_s), r1 * np.sin(t_s)
        append_segmented(lines, 'C_HULL_MAIN', gx1, gy1, np.full_like(gx1, z1))

    # Heavy Armor Plate Arrays (Visual Greeble Lines)
    for r_p in [4.8, 8.4]:
        z_p = np.interp(r_p, [2.4, 12.0], [2.4, 1.0])
        gx, gy = r_p * np.cos(t_s), r_p * np.sin(t_s)
        append_segmented(lines, 'C_HULL_DARK', gx, gy, np.full_like(gx, z_p))
        append_segmented(lines, 'C_HULL_DARK', gx, gy, np.full_like(gx, -z_p))

    # 6x Top Heat Exhaust Rings (Rear Quadrants strictly)
    for a_deg in [135, 153, 171, 189, 207, 225]:
        vent_x, vent_y = 7.5 * np.cos(np.radians(a_deg)), 7.5 * np.sin(np.radians(a_deg))
        add_cylinder(lines, 'C_DETAILS', vent_x, vent_y, 0.6, 0.4, 1.3, axis='z', rings=3)

    # Sublight Thruster Array (Trench emission node explicitly mapping the Cyan Engine glow)
    t_eng = np.linspace(np.radians(135), np.radians(225), 45)
    for z_g in np.linspace(-0.4, 0.4, 7):
        gx, gy = 12.02 * np.cos(t_eng), 12.02 * np.sin(t_eng)
        append_segmented(lines, 'C_THRUSTER', list(gx), list(gy), [z_g]*45)
    for ang in t_eng: # Vertical plasma baffles
        gx, gy = 12.02 * np.cos(ang), 12.02 * np.sin(ang)
        append_segmented(lines, 'C_THRUSTER', [gx, gx], [gy, gy], [-0.4, 0.4])

    # ==============================================================================
    # 3. FORWARD MANDIBLES (Massive Bilinear Solid Extrusion Matrices)
    # ==============================================================================
    # Port (-Y)
    p_t1 = (4.8, -1.8, 1.4);  p_t2 = (22.5, -3.0, 0.5)
    p_t3 = (22.5, -6.6, 0.5);  p_t4 = (4.8, -11.0, 1.4)
    p_b1 = (4.8, -1.8, -1.4); p_b2 = (22.5, -3.0, -0.5)
    p_b3 = (22.5, -6.6, -0.5); p_b4 = (4.8, -11.0, -1.4)
    
    for face in [(p_t1, p_t2, p_t3, p_t4), (p_b1, p_b2, p_b3, p_b4),  
                 (p_t1, p_t2, p_b2, p_b1), (p_t4, p_t3, p_b3, p_b4),  
                 (p_t2, p_t3, p_b3, p_b2)]:                           
        add_quad_mesh(lines, 'C_HULL_MAIN', *face, u_steps=9, v_steps=3)

    # Starboard (+Y)
    s_t1 = (4.8, 1.8, 1.4);   s_t2 = (22.5, 3.0, 0.5)
    s_t3 = (22.5, 6.6, 0.5);   s_t4 = (4.8, 11.0, 1.4)
    s_b1 = (4.8, 1.8, -1.4);  s_b2 = (22.5, 3.0, -0.5)
    s_b3 = (22.5, 6.6, -0.5);  s_b4 = (4.8, 11.0, -1.4)

    for face in [(s_t1, s_t2, s_t3, s_t4), (s_b1, s_b2, s_b3, s_b4),
                 (s_t1, s_t2, s_b2, s_b1), (s_t4, s_t3, s_b3, s_b4),
                 (s_t2, s_t3, s_b3, s_b2)]:
        add_quad_mesh(lines, 'C_HULL_MAIN', *face, u_steps=9, v_steps=3)

    # Access Maintenance Trench cutouts (Running laterally down mandibles)
    append_segmented(lines, 'C_DETAILS', [4.8, 22.5], [-8.8, -4.8], [0.0, 0.0])
    append_segmented(lines, 'C_DETAILS', [4.8, 22.5], [ 8.8,  4.8], [0.0, 0.0])

    # ==============================================================================
    # 4. EXPLICIT COPLANAR STARBOARD COCKPIT
    # ==============================================================================
    # Tunnel extending diagonally to the precise rigid offset
    add_cylinder_oriented(lines, 'C_HULL_DARK', (5.0, 10.0, 0.0), (8.5, 14.5, 0.0), 1.6, 1.6, rings=5, t_count=16)
    # The Pod strictly executing parallel to the X-Axis forwards
    add_cylinder_oriented(lines, 'C_HULL_MAIN', (8.5, 14.5, 0.0), (12.5, 14.5, 0.0), 1.8, 1.4, rings=8, t_count=16)
    # Frontal glass canopy arrays (Blackout frames + Glass boundary)
    add_cylinder_oriented(lines, 'C_COCKPIT', (12.5, 14.5, 0.0), (13.5, 14.5, 0.0), 1.4, 0.4, rings=6, t_count=12)

    # Lateral Port-Side Docking Ring intersecting the -Y trench
    add_cylinder_oriented(lines, 'C_DETAILS', (0.0, -11.5, 0.0), (0.0, -13.0, 0.0), 1.6, 1.6, rings=4, t_count=16)

    # ==============================================================================
    # 5. WEAPONS, SENSORS & TACTICAL APPENDAGES
    # ==============================================================================
    # Quad Laser Cannon Turrets (Dorsal & Ventral Core)
    for z_base, z_gun in [(2.4, 3.4), (-2.4, -3.4)]:
        add_cylinder(lines, 'C_HULL_DARK', cx=0, cy=0, cz=z_base, length=0.6*np.sign(z_base), radius=1.3, axis='z', rings=3)
        add_cylinder(lines, 'C_HULL_MAIN', cx=0, cy=0, cz=z_base+0.6*np.sign(z_base), length=0.4*np.sign(z_base), radius=1.0, axis='z', rings=2)
        # Heavy Quad Gun Barrels projecting strictly forwards (+X)
        for g_off in [(-0.3, -0.3), (-0.3, 0.3), (0.3, -0.3), (0.3, 0.3)]:
            append_segmented(lines, 'C_LASER', [0.0, 2.5], [g_off[1], g_off[1]], [z_gun+g_off[0]*np.sign(z_base), z_gun+g_off[0]*np.sign(z_base)])

    # Rigid Radar Sensor Dish (Upper Port Side -Y) mapped absolutely
    add_cylinder(lines, 'C_HULL_DARK', cx=-2.0, cy=-7.0, cz=1.5, length=1.0, radius=0.6, axis='z', rings=3)
    
    # Parabolic Dish Curve Mathematics
    dish_center = np.array([-2.0, -7.0, 2.5])
    dish_dir = np.array([1.0, -0.2, 1.0])
    dish_dir = dish_dir / np.linalg.norm(dish_dir)
    up = np.array([0., 1., 0.])
    xu = np.cross(up, dish_dir); xu = xu / np.linalg.norm(xu)
    yu = np.cross(dish_dir, xu); yu = yu / np.linalg.norm(yu)
    
    t_d = np.linspace(0, 2*np.pi, 24)
    for r_d in np.linspace(0, 2.0, 6):
        z_d = -0.4 * (r_d / 2.0)**2 # The dish concavity
        dx = dish_center[0] + dish_dir[0]*z_d + r_d * np.cos(t_d)*xu[0] + r_d * np.sin(t_d)*yu[0]
        dy = dish_center[1] + dish_dir[1]*z_d + r_d * np.cos(t_d)*xu[1] + r_d * np.sin(t_d)*yu[1]
        dz = dish_center[2] + dish_dir[2]*z_d + r_d * np.cos(t_d)*xu[2] + r_d * np.sin(t_d)*yu[2]
        append_segmented(lines, 'C_HULL_MAIN', list(dx)+[dx[0]], list(dy)+[dy[0]], list(dz)+[dz[0]])

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_falcon_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking the 35m rig tightly to its mechanical center X=4.0
        cam_x, cam_y, cam_z = 4.0, 0.0, 0.0
        
        # Starts from absolute 90.0 (Right Side Profile revealing starboard alignment completely)
        azimuth = 90.0 - (stage * 360.0)

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
    # Rigid offset cx=4.0. Max forward extent = 22.5 (Dist=18.5). Max Y extent = 16.3 (Dist=16.3).
    # cam_span = 22.0 guarantees the rotating object ABSOLUTELY CANNOT clip the 9:16 borders.
    cam_span = 22.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.3), 
        ('C_DETAILS',   C_DETAILS,   1.2, 1.0),
        ('C_HULL_DARK', C_HULL_DARK, 1.4, 1.0),
        ('C_HULL_MAIN', C_HULL_MAIN, 1.3, 1.0),
        ('C_COCKPIT',   C_COCKPIT,   1.6, 1.0),
        ('C_LASER',     C_LASER,     2.2, 1.0),
        ('C_THRUSTER',  C_THRUSTER,  1.8, 0.95)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Executing a pristine 18-degree viewing elevation bounding the Top and Sides identically
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=18.0)
            render_queue.append((np.mean(depth), u, v+1.0, c_val, lw, alpha))

    # ABSOLUTE Z-SORT (Strict Painter's Algorithm Depth Culling)
    render_queue.sort(key=lambda item: item[0], reverse=True)
    for depth, u, v, c, lw, a in render_queue:
        ax.plot(u, v, color=c, lw=lw, alpha=a)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (TOP HUD)
    # ------------------------------------------------------------------
    ui_t = cam_span * 1.45
    ax.add_patch(patches.Rectangle((-cam_span, ui_t), cam_span*2, 12.0, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_t, ui_t], color=C_TEXT, lw=6, zorder=81)

    ax.text(-cam_span*0.95, ui_t+1.8, "LG-450f // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=17, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t+0.5, "EXPLICIT TRUE-SCALE GEOMETRY // YT-1300 FREIGHTER MATRIX", color=C_HULL_MAIN, fontsize=13, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b+2.8, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_THRUSTER, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+1.4, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.3, "TOPOLOGICAL YIELD: TRUE BILINEAR LATTICE / OFF-AXIS CANOPY VALIDATED", color=C_HULL_DARK, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-450f: YT-1300 KINEMATICS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
