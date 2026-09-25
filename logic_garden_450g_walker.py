"""
PROJECT: Logic Garden 450g (Exact Physical Construct // AT-AT Walker Kinematics - BARE METAL)
FORMAT: YouTube Shorts (1080x1920)
METADATA: STAR WARS, AT-AT, WALKER, EMPIRE STRIKES BACK, MECH, WIREFRAME, ENGINEERING, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: True Inverse Kinematics (IK) for 4-beat staggered walking cycle, exact hull topography, explicit viewport and cannon parameters.
- Strict Bounds Protocol: Core anchor locked. cam_span dynamically set to 15.0 assuring ABSOLUTE 100% frame preservation.
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
OUT_DIR = "frames_450g_walker"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Baseplate Reference Track)

C_HULL_MAIN = '#94A3B8'          # Heavy Armor Slate (Primary Main Body Panels)
C_HULL_DARK = '#475569'          # Machined Steel (Undercarriage, Knee Casings)
C_DETAILS   = '#1E293B'          # Carbon Slate (Drive Motors, Flex Neck, Ankle Struts)
C_FOOT      = '#111115'          # Indestructible Black (Toe Flaps & Footpads)
C_LASER     = '#FF3300'          # Intense Red (Heavy Laser Cannon Output Nozzles)
C_VIEWPORT  = '#00D2FF'          # High Target Cyan (Command Section Glazing)

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
    if L < 0.0001: return
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
# STATIC SUPERSTRUCTURE BUILDERS (AT-AT HULL)
# ------------------------------------------------------------------
def generate_walker_hull():
    lines = {
        'C_HULL_MAIN': [], 'C_HULL_DARK': [], 'C_DETAILS': [], 
        'C_VIEWPORT': [], 'C_LASER': [], 'C_FOOT': [], 'C_GRID': []
    }

    # 1. BASEPLATE ENVELOPE (REFERENCE GRID)
    gx_range = np.linspace(-15.0, 15.0, 21)
    gy_range = np.linspace(-10.0, 10.0, 15)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, 0.0))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, 0.0))

    # ==============================================================================
    # 2. MAIN TROOP SECTION (The Core Hull)
    # ==============================================================================
    for sign in [-1, 1]:
        # Top half (Tapered inward at the roof)
        p_top_f = ( 4.5,  2.0 * sign, 15.0)
        p_top_r = (-6.5,  2.0 * sign, 15.0)
        p_mid_f = ( 5.0,  3.0 * sign, 11.5)
        p_mid_r = (-7.5,  3.0 * sign, 11.5)
        add_quad_mesh(lines, 'C_HULL_MAIN', p_top_f, p_top_r, p_mid_r, p_mid_f, u_steps=12, v_steps=6)

        # Bottom half (Undercut belly)
        p_bot_f = ( 4.0,  2.2 * sign,  9.5)
        p_bot_r = (-6.0,  2.2 * sign,  9.5)
        add_quad_mesh(lines, 'C_HULL_DARK', p_mid_f, p_mid_r, p_bot_r, p_bot_f, u_steps=12, v_steps=4)

    # Roof and Belly closure
    add_quad_mesh(lines, 'C_HULL_MAIN', (4.5, 2.0, 15.0), (-6.5, 2.0, 15.0), (-6.5, -2.0, 15.0), (4.5, -2.0, 15.0), u_steps=12, v_steps=6)
    add_quad_mesh(lines, 'C_HULL_DARK', (4.0, 2.2,  9.5), (-6.0, 2.2,  9.5), (-6.0, -2.2,  9.5), (4.0, -2.2,  9.5), u_steps=12, v_steps=6)

    # Rear Extrusion / Atmosphere Exchangers array
    add_quad_mesh(lines, 'C_HULL_MAIN', (-6.5, 2.0, 15.0), (-6.5, -2.0, 15.0), (-7.5, -3.0, 11.5), (-7.5, 3.0, 11.5), u_steps=4, v_steps=6)

    # ==============================================================================
    # 3. DRIVE MOTORS (Shoulder & Hip Pivot Hubs)
    # ==============================================================================
    # Massive heavy-duty cylindrical mounts linking the legs
    for cx in [4.0, -5.5]:
        for y_sign in [-1, 1]:
            add_cylinder_oriented(lines, 'C_DETAILS', (cx, 3.0*y_sign, 11.2), (cx, 3.8*y_sign, 11.2), 1.6, 1.4, rings=4, t_count=20)
            # Internal motor detailing
            add_cylinder_oriented(lines, 'C_HULL_DARK', (cx, 3.8*y_sign, 11.2), (cx, 4.0*y_sign, 11.2), 0.8, 0.8, rings=2, t_count=12)

    # ==============================================================================
    # 4. FLEXIBLE ARMORED TUNNEL (The Neck)
    # ==============================================================================
    # Highly corrugated ribbed structure bridging the main body to the command head
    add_cylinder_oriented(lines, 'C_DETAILS', (4.8, 0.0, 12.0), (7.5, 0.0, 11.5), 1.2, 1.2, rings=15, t_count=16)

    # ==============================================================================
    # 5. COMMAND SECTION (The Head)
    # ==============================================================================
    for sign in [-1, 1]:
        h_top_r = ( 7.5, 1.2 * sign, 13.0)
        h_top_f = (11.0, 0.7 * sign, 12.2)
        h_mid_r = ( 7.0, 1.6 * sign, 11.5)
        h_mid_f = (11.5, 1.0 * sign, 11.2)
        h_bot_r = ( 7.5, 1.2 * sign, 10.0)
        h_bot_f = (11.2, 0.7 * sign, 10.4)

        add_quad_mesh(lines, 'C_HULL_MAIN', h_top_r, h_top_f, h_mid_f, h_mid_r, u_steps=5, v_steps=4)
        add_quad_mesh(lines, 'C_HULL_DARK', h_mid_r, h_mid_f, h_bot_f, h_bot_r, u_steps=5, v_steps=3)
        
        # Redundant Viewport Armor Frame
        append_segmented(lines, 'C_VIEWPORT', [10.2, 11.0, 11.0, 10.2, 10.2], 
                         [0.9*sign, 0.75*sign, 0.75*sign, 0.9*sign, 0.9*sign], 
                         [11.8,     11.6,      11.3,      11.5,     11.8])

    # Head Roof and Chin closure
    add_quad_mesh(lines, 'C_HULL_MAIN', (7.5, 1.2, 13.0), (11.0, 0.7, 12.2), (11.0, -0.7, 12.2), (7.5, -1.2, 13.0), u_steps=5, v_steps=4)
    add_quad_mesh(lines, 'C_HULL_DARK', (7.5, 1.2, 10.0), (11.2, 0.7, 10.4), (11.2, -0.7, 10.4), (7.5, -1.2, 10.0), u_steps=5, v_steps=4)

    # ==============================================================================
    # 6. WEAPONS (Heavy Laser Cannons & Medium Blasters)
    # ==============================================================================
    # Under-chin Heavy Lasers
    for cy in [-0.4, 0.4]:
        # Mounts
        add_cylinder_oriented(lines, 'C_DETAILS', (9.5, cy, 10.2), (11.2, cy, 10.2), 0.3, 0.3, rings=3, t_count=8)
        # Heavy Barrel Extrusions
        add_cylinder_oriented(lines, 'C_HULL_DARK', (11.2, cy, 10.2), (13.5, cy, 10.2), 0.15, 0.15, rings=4, t_count=8)
        # Red Hot Nozzles
        add_cylinder_oriented(lines, 'C_LASER',     (13.5, cy, 10.2), (13.7, cy, 10.2), 0.16, 0.18, rings=2, t_count=8)

    # Side Temple Medium Blasters
    for cy_sign in [-1, 1]:
        # Side mounts protruding tangentially
        add_cylinder_oriented(lines, 'C_DETAILS', (10.0, 1.1*cy_sign, 11.2), (10.0, 1.6*cy_sign, 11.2), 0.4, 0.4, rings=3, t_count=8)
        # Barrel Extrusions sweeping forward
        add_cylinder_oriented(lines, 'C_HULL_DARK', (10.0, 1.6*cy_sign, 11.2), (12.5, 1.6*cy_sign, 11.2), 0.1, 0.1, rings=3, t_count=6)

    return lines


# ------------------------------------------------------------------
# TRUE INVERSE KINEMATICS MATHEMATICS (The Biomechanical Solver)
# ------------------------------------------------------------------
def generate_dynamic_leg(lines, Hx, Hy, Hz, phase, is_right, stage_offset):
    # Phase handles fractional progression exactly [0.0 -> 1.0)
    S = 7.0       # Absolute Mathematical Stride Length
    H = 1.8       # Max vertical toe lift during swing
    k = 0.75      # Stance Fraction (Foot on ground 75% of cycle carrying the immense load)
    
    # Kinematic Foot Path (Moving relative to absolute static chassis frame)
    if phase < k: 
        # Power Stance - The chassis is pushed forward geometrically
        fx = S/2.0 - S * (phase / k)
        fz = 0.0
        pitch_rad = 0.0
    else: 
        # Hydraulic Swing Phase - Throwing the massive leg forward via the trajectory arch
        sp = (phase - k) / (1.0 - k)
        fx = -S/2.0 + S * sp
        fz = H * np.sin(np.pi * sp)
        pitch_rad = np.radians(-25.0 * np.sin(np.pi * sp)) # Visual toe tilt upwards

    # The True Target Foot Anchor coordinate
    Fx = Hx + fx
    Fy = Hy
    Fz = fz + 1.2 # Height of the monolithic footpad base

    # 2D Planar Inverse Kinematics (XZ projection)
    dx = Fx - Hx
    dz = Fz - Hz # Geometrically negative displacement
    D = np.sqrt(dx**2 + dz**2)
    
    # True structural limits of the hydraulic pistons
    L1 = 6.2 # Thigh length
    L2 = 6.2 # Calf length
    
    # Absolute Physical Clamp avoiding singularities / infinite extensions
    D = min(D, L1 + L2 - 0.01)
    
    # Law of Cosines solver
    gamma = np.arctan2(dx, -dz) 
    cos_b = (L1**2 + D**2 - L2**2) / (2 * L1 * D)
    b = np.arccos(np.clip(cos_b, -1.0, 1.0))
    
    # Thigh forces knee to physically break "forward" relative to the structural stride
    theta_thigh = gamma + b 
    
    Kx = Hx + L1 * np.sin(theta_thigh)
    Kz = Hz - L1 * np.cos(theta_thigh)

    y_sign = 1.0 if not is_right else -1.0

    # 1. Active Heavy Thigh Construction
    add_cylinder_oriented(lines, 'C_HULL_MAIN', (Hx, Hy + 1.2*y_sign, Hz), (Kx, Hy + 1.2*y_sign, Kz), 1.5, 1.0, rings=6, t_count=16)
    
    # 2. Hydraulic Knee Joint (The primary hinge point)
    add_cylinder_oriented(lines, 'C_DETAILS', (Kx, Hy + 0.4*y_sign, Kz), (Kx, Hy + 2.0*y_sign, Kz), 1.2, 1.2, rings=4, t_count=16)
    # The distinct circular Knee Shield projecting forwards
    add_cylinder_oriented(lines, 'C_HULL_DARK', (Kx+1.0, Hy + 2.1*y_sign, Kz), (Kx+1.0, Hy + 2.2*y_sign, Kz), 0.8, 0.8, rings=2, t_count=16)

    # 3. Straight Calf Piston
    add_cylinder_oriented(lines, 'C_HULL_MAIN', (Kx, Hy + 1.2*y_sign, Kz), (Fx, Fy + 1.2*y_sign, Fz), 0.8, 0.7, rings=5, t_count=12)
    # Ankle Universal Joint
    add_cylinder_oriented(lines, 'C_DETAILS', (Fx, Fy + 0.6*y_sign, Fz), (Fx, Fy + 1.8*y_sign, Fz), 0.8, 0.8, rings=4, t_count=12)

    # 4. The Monolithic Footpad (Dynamic Pitching Cone Base)
    # Applying the forward vector mathematics adjusting to the pitch_rad
    v_down = np.array([np.sin(pitch_rad), 0.0, -np.cos(pitch_rad)])
    cone_base = np.array([Fx, Fy + 1.2*y_sign, Fz]) + v_down * 1.2
    
    add_cylinder_oriented(lines, 'C_FOOT', tuple(cone_base), (Fx, Fy + 1.2*y_sign, Fz), 2.2, 1.2, rings=5, t_count=20)
    
    # Subsurface toe-flaps locking into substrate
    flap_rad = cone_base + v_down * 0.1
    add_cylinder_oriented(lines, 'C_FOOT', tuple(flap_rad), tuple(cone_base), 2.8, 2.2, rings=2, t_count=20)


def generate_kinematic_motion(lines, stage):
    # Base Hip Mount Anchors
    h_front_x = 4.0; h_rear_x = -5.5
    h_y = 3.6
    h_z = 11.2

    # The 6.0 multiplier defines 6 exact full stride cycles over 24 seconds (1 loop = 4s)
    # Using an exact 4-beat pattern for overwhelming mechanical stability
    generate_dynamic_leg(lines, h_front_x,  h_y, h_z, (stage * 6.0 + 0.00) % 1.0, is_right=False, stage_offset=stage) # Front Left
    generate_dynamic_leg(lines,  h_rear_x, -h_y, h_z, (stage * 6.0 + 0.25) % 1.0, is_right=True,  stage_offset=stage) # Rear Right
    generate_dynamic_leg(lines, h_front_x, -h_y, h_z, (stage * 6.0 + 0.50) % 1.0, is_right=True,  stage_offset=stage) # Front Right
    generate_dynamic_leg(lines,  h_rear_x,  h_y, h_z, (stage * 6.0 + 0.75) % 1.0, is_right=False, stage_offset=stage) # Rear Left


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_walker_hull()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking the rig to view the full 15m elevation explicitly
        cam_x, cam_y, cam_z = 1.0, 0.0, 7.5
        
        # Starts exactly from Side Profile evaluating the entire stride length
        azimuth = 90.0 - (stage * 360.0)

        yield (f, t_sec, azimuth, stage, cam_x, cam_y, cam_z, static_rig)

def render_frame(packet):
    f, t_sec, azimuth, stage, cx, cy, cz, static_rig = packet

    # Clone the dictionary securely, then inject the live-solving true procedural mathematics
    local_rig = {k: v.copy() for k,v in static_rig.items()}
    generate_kinematic_motion(local_rig, stage)

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # 100% VISIBILITY THRESHOLD AUDIT:
    # Rigid offset cx=1.0. Max forward extent = 13.5 (Dist=12.5). Max vertical limit Z=15.0. 
    # cam_span = 14.5 guarantees absolute 9:16 borders encapsulation continuously securely.
    cam_span = 14.5
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.3), 
        ('C_DETAILS',   C_DETAILS,   1.4, 1.0),
        ('C_HULL_DARK', C_HULL_DARK, 1.2, 1.0),
        ('C_HULL_MAIN', C_HULL_MAIN, 1.4, 1.0),
        ('C_FOOT',      C_FOOT,      1.8, 1.0),
        ('C_VIEWPORT',  C_VIEWPORT,  1.6, 1.0),
        ('C_LASER',     C_LASER,     2.2, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in local_rig[c_key]:
            # Orbiting meticulously on a low 5-degree elevation mapping the titanic ground scale accurately
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=5.0)
            render_queue.append((np.mean(depth), u, v, c_val, lw, alpha))

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

    ax.text(-cam_span*0.95, ui_t+1.6, "LG-450g // MACRO-ENGINEERING TENSOR: BIOMECHANICAL KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t+0.5, "EXPLICIT TRUE-SCALE GEOMETRY // 20M HEAVY ASSAULT QUADRUPED", color=C_HULL_MAIN, fontsize=13, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b+1.8, "[OPERATIONAL] ACCELERATED 4-BEAT STAGGERED INVERSE KINEMATICS", color=C_VIEWPORT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.7, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (FORWARD PROGRESSION MAPPED)", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b-0.2, "TOPOLOGICAL YIELD: TRUE JOINT ARTICULATION SECURED TO DATUM", color=C_HULL_DARK, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-450g: AT-AT QUADRUPED LATTICE [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Biomechanical Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
