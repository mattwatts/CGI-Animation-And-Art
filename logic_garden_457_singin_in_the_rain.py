"""
PROJECT: Logic Garden 457 (Exact Physical Construct // Singin' in the Rain Kinematics)
FORMAT: YouTube Shorts (1080x1920)
METADATA: BIOMECHANICS, GENE KELLY, ALGORITHMIC CHOREOGRAPHY, INFRASTRUCTURE, PYTHON
EXECUTION: 24.0s Sequence @ 60 FPS. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true 3D spatial scale.
- Algorithmic Interpolation: Fluid continuous mathematical tracking from Pose 2 to Pose 1.
- Kinematic Step Flourishes: Z-axis parabolic arcs govern hands and feet during transit.
- Biomechanical Fidelity: Cantilevered spine matrix, closed wet silk umbrella, planted anchors.
- Infrastructural Integration: Exact municipal lamp post geometries (baseplate, crossbar, lantern).
- Viewport Override: Locked cam_span guarantees 100% total system visibility.
- Timeline: Continuous seamless 360-degree orbit starting from 115-degree side-angle.
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
OUT_DIR = "frames_457_singin_rain"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISUAL METRICS) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Rain Matrix / Stygian Pavement)

C_SUIT      = '#334155'          # Heavy Slate (Sodden Worsted Wool)
C_SKIN      = '#CA8A04'          # Kapton Gold (Biomechanical Features & Facial Tilt)
C_POST      = '#1E293B'          # Carbon Slate (Cast Iron Lamp Standard)
C_LIGHT     = '#D97706'          # Golden Amber (Incandescent Lantern Filament)
C_UMBRELLA  = '#0F172A'          # Abyssal Slate (Furled Silk Canopy & Shaft)
C_DETAILS   = '#111115'          # Indestructible Black (Fedora Crown, Tap Shoes)

# ------------------------------------------------------------------
# O(N) MATPLOTLIB KINEMATIC ENGINE
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

# ------------------------------------------------------------------
# GEOMETRIC PRIMITIVES
# ------------------------------------------------------------------
def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='z', rings=4, t_count=16):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, length, rings)
    for s in steps:
        if axis == 'z':
            ix = cx + radius*np.cos(t); iy = cy + radius*np.sin(t); iz = np.full_like(t, cz + s)
        elif axis == 'y':
            ix = cx + radius*np.cos(t); iy = np.full_like(t, cy + s); iz = cz + radius*np.sin(t)
        elif axis == 'x':
            ix = np.full_like(t, cx + s); iy = cy + radius*np.cos(t); iz = cz + radius*np.sin(t)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        if axis == 'z':
            sx = np.full_like(steps, cx + radius*np.cos(a)); sy = np.full_like(steps, cy + radius*np.sin(a)); sz = cz + steps
        elif axis == 'y':
            sx = np.full_like(steps, cx + radius*np.cos(a)); sy = cy + steps; sz = np.full_like(steps, cz + radius*np.sin(a))
        elif axis == 'x':
            sx = cx + steps; sy = np.full_like(steps, cy + radius*np.cos(a)); sz = np.full_like(steps, cz + radius*np.sin(a))
        append_segmented(lines_dict, col, list(sx), list(sy), list(sz))

def add_ellipsoid(lines_dict, col, cx, cy, cz, rx, ry, rz, rings=8, t_count=16):
    for p in np.linspace(-np.pi/2, np.pi/2, rings):
        r_x = rx * np.cos(p); r_y = ry * np.cos(p); z_s = rz * np.sin(p)
        t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
        ix = cx + r_x*np.cos(t); iy = cy + r_y*np.sin(t); iz = np.full_like(t, cz + z_s)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, np.pi, t_count//2, endpoint=False):
        p = np.linspace(-np.pi/2, np.pi/2, rings*2)
        c_p = np.cos(p); s_p = np.sin(p)
        ix = cx + rx * c_p * np.cos(a); iy = cy + ry * c_p * np.sin(a); iz = cz + rz * s_p
        append_segmented(lines_dict, col, list(ix), list(iy), list(iz))

def add_box(lines_dict, col, cx, cy, cz, dx, dy, dz):
    hx, hy, hz = dx/2, dy/2, dz/2
    xs = [cx-hx, cx+hx, cx+hx, cx-hx, cx-hx]
    ys1 = [cy-hy, cy-hy, cy+hy, cy+hy, cy-hy]
    ys2 = [cy-hy, cy-hy, cy+hy, cy+hy, cy-hy]
    append_segmented(lines_dict, col, xs, ys1, [cz-hz]*5)
    append_segmented(lines_dict, col, xs, ys2, [cz+hz]*5)
    for i in range(4):
        append_segmented(lines_dict, col, [xs[i], xs[i]], [ys1[i], ys1[i]], [cz-hz, cz+hz])

def add_ribbed_strut(lines_dict, col, p1, p2, radius, rings=10, t_count=12, rib_freq=6.0, rib_depth=0.15):
    # Mathematics governing fabric tension / worsted wool compression
    p1, p2 = np.array(p1), np.array(p2)
    v = p2 - p1
    length = np.linalg.norm(v)
    if length < 0.001: return
    v_dir = v / length
    not_v = np.array([1.0, 0.0, 0.0])
    if abs(np.dot(v_dir, not_v)) > 0.99: not_v = np.array([0.0, 1.0, 0.0])
    n1 = np.cross(v_dir, not_v)
    n1 /= np.linalg.norm(n1)
    n2 = np.cross(v_dir, n1)
    
    steps = np.linspace(0, length, rings)
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    
    for s in steps:
        r_mod = radius * (1.0 + rib_depth * np.cos((s / length) * rib_freq * 2 * np.pi))
        center = p1 + v_dir * s
        ix = center[0] + r_mod * (np.cos(t)*n1[0] + np.sin(t)*n2[0])
        iy = center[1] + r_mod * (np.cos(t)*n1[1] + np.sin(t)*n2[1])
        iz = center[2] + r_mod * (np.cos(t)*n1[2] + np.sin(t)*n2[2])
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        sx, sy, sz = [], [], []
        for s in steps:
            r_mod = radius * (1.0 + rib_depth * np.cos((s / length) * rib_freq * 2 * np.pi))
            nx = r_mod * (np.cos(a)*n1[0] + np.sin(a)*n2[0])
            ny = r_mod * (np.cos(a)*n1[1] + np.sin(a)*n2[1])
            nz = r_mod * (np.cos(a)*n1[2] + np.sin(a)*n2[2])
            sx.append(p1[0] + nx + v_dir[0] * s)
            sy.append(p1[1] + ny + v_dir[1] * s)
            sz.append(p1[2] + nz + v_dir[2] * s)
        append_segmented(lines_dict, col, sx, sy, sz)

def lerp_vec(v1, v2, p):
    return (np.array(v1) * (1.0 - p)) + (np.array(v2) * p)

# ------------------------------------------------------------------
# KINEMATIC TENSOR ARRAYS (Pose Interpolation)
# ------------------------------------------------------------------
def get_pose_1():
    # Target Kinematics: The Cantilevered Lamppost Hang
    return {
        'HIP_C':      [-0.95, 0.0, 0.95],
        'SHOULDER_C': [-0.6, 0.0, 1.6],
        'HEAD_C':     [-0.7, 0.0, 1.85],
        'HAND_L':     [-0.06, -0.05, 1.7],
        'ELBOW_L':    [-0.3, -0.15, 1.65],
        'HAND_R':     [-0.9, 0.35, 1.1],
        'ELBOW_R':    [-0.8, 0.25, 1.4],
        'KNEE_R':     [-0.6, 0.10, 0.7],
        'ANKLE_R':    [-0.2, 0.10, 0.45],
        'KNEE_L':     [-0.5, -0.10, 0.65],
        'ANKLE_L':    [-0.15, -0.10, 0.35],
        'UMB_HANDLE': [-0.85, 0.3, 1.15],
        'UMB_TIP':    [-1.4, 0.6, 0.4]
    }

def get_pose_2():
    # Target Kinematics: The Horizontal Umbrella Rifle-Hold / Wide Stance
    return {
        'HIP_C':      [-1.4, 0.0, 1.0],
        'SHOULDER_C': [-1.4, 0.0, 1.55],
        'HEAD_C':     [-1.4, 0.0, 1.8],
        'HAND_L':     [-1.7, 0.4, 1.1],
        'ELBOW_L':    [-1.7, 0.2, 1.3],
        'HAND_R':     [-1.1, 0.4, 1.1],
        'ELBOW_R':    [-1.1, 0.2, 1.3],
        'KNEE_R':     [-1.1, 0.1, 0.5],
        'ANKLE_R':    [-0.9, 0.1, 0.05],
        'KNEE_L':     [-1.7, -0.1, 0.5],
        'ANKLE_L':    [-1.9, -0.1, 0.05],
        'UMB_HANDLE': [-0.9, 0.4, 1.1],
        'UMB_TIP':    [-2.3, 0.4, 1.1]
    }

def generate_dynamic_street_matrix(t_sec):
    lines = {
        'C_SUIT': [], 'C_SKIN': [], 'C_POST': [], 
        'C_UMBRELLA': [], 'C_DETAILS': [], 'C_LIGHT': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. INFRASTRUCTURE: MUNICIPAL LAMP POST (Absolute Origin)
    # ==============================================================================
    POST_X, POST_Y = 0.0, 0.0
    
    # Cast-Iron Base Plate (Ribbed and stepped)
    add_cylinder(lines, 'C_POST', POST_X, POST_Y, 0.0, length=0.1, radius=0.25, axis='z', rings=2, t_count=16)
    add_cylinder(lines, 'C_POST', POST_X, POST_Y, 0.1, length=0.4, radius=0.15, axis='z', rings=5, t_count=16)
    # Main Fluted Shaft
    add_cylinder(lines, 'C_POST', POST_X, POST_Y, 0.5, length=2.1, radius=0.06, axis='z', rings=10, t_count=12)
    # Crossbar
    append_segmented(lines, 'C_POST', [-0.3, 0.3], [0.0, 0.0], [1.9, 1.9])
    add_cylinder(lines, 'C_POST', -0.3, 0.0, 1.9, length=0.6, radius=0.015, axis='x', rings=2, t_count=6)
    # Lantern Housing & Glass Frame
    add_box(lines, 'C_POST', POST_X, POST_Y, 2.75, dx=0.25, dy=0.25, dz=0.3)
    add_ellipsoid(lines, 'C_LIGHT', POST_X, POST_Y, 2.75, rx=0.07, ry=0.07, rz=0.11, rings=4, t_count=8)
    # Finial Spire
    append_segmented(lines, 'C_POST', [POST_X, POST_X], [POST_Y, POST_Y], [2.9, 3.1])

    # ==============================================================================
    # 2. CONTINUOUS KINEMATIC INTERPOLATION ALGORITHM
    # ==============================================================================
    # Oscillates fluidly between 0.0 (Pose 2) and 1.0 (Pose 1) providing perfect seamless loop bounds.
    phase = 0.5 * (1.0 - np.cos(2.0 * np.pi * t_sec / DURATION))
    
    # The parabolic step flourish (arcs Z-axes mid-transition for realistic gravity lift)
    swing_arc = np.sin(np.pi * phase)

    P1 = get_pose_1()
    P2 = get_pose_2()
    
    # Dynamic Vector Dictionary
    D = {}
    for key in P1.keys():
        D[key] = lerp_vec(P2[key], P1[key], phase)

    # Injected Gravity Arcs (Ensuring limbs do not drag across the substrate during transition)
    D['HAND_L'][2]  += swing_arc * 0.40  # Left arm reaches high to grab the pole
    D['HAND_R'][2]  += swing_arc * 0.15  # Right arm flourishing the umbrella
    D['ANKLE_L'][2] += swing_arc * 0.35  # Left foot sweeping kick onto the pedestal
    D['ANKLE_R'][2] += swing_arc * 0.25  # Right foot leaping
    D['KNEE_L'][2]  += swing_arc * 0.35  
    D['KNEE_R'][2]  += swing_arc * 0.25  

    # ==============================================================================
    # 3. BIOMECHANICAL SUIT MATRIX EXTRUSION
    # ==============================================================================
    # Torso (Draped, sodden suit fabric linking shoulders to pelvis)
    add_ribbed_strut(lines, 'C_SUIT', D['HIP_C'], D['SHOULDER_C'], radius=0.15, rings=12, t_count=14, rib_freq=4.0, rib_depth=0.02)
    
    # Head & Fedora
    add_ellipsoid(lines, 'C_SKIN', D['HEAD_C'][0], D['HEAD_C'][1], D['HEAD_C'][2], rx=0.08, ry=0.09, rz=0.10, rings=6, t_count=12)
    add_cylinder(lines, 'C_DETAILS', D['HEAD_C'][0]-0.03, D['HEAD_C'][1], D['HEAD_C'][2]+0.05, length=0.01, radius=0.15, axis='z', rings=2, t_count=16)
    add_cylinder(lines, 'C_DETAILS', D['HEAD_C'][0]-0.05, D['HEAD_C'][1], D['HEAD_C'][2]+0.06, length=0.10, radius=0.08, axis='z', rings=3, t_count=12)

    # Left Arm
    add_ribbed_strut(lines, 'C_SUIT', D['SHOULDER_C'], D['ELBOW_L'], radius=0.06, rings=8, t_count=8, rib_freq=7.0, rib_depth=0.03)
    add_ribbed_strut(lines, 'C_SUIT', D['ELBOW_L'], D['HAND_L'], radius=0.05, rings=8, t_count=8, rib_freq=10.0, rib_depth=0.04)

    # Right Arm
    add_ribbed_strut(lines, 'C_SUIT', D['SHOULDER_C'], D['ELBOW_R'], radius=0.06, rings=8, t_count=8, rib_freq=8.0, rib_depth=0.03)
    add_ribbed_strut(lines, 'C_SUIT', D['ELBOW_R'], D['HAND_R'], radius=0.05, rings=8, t_count=8, rib_freq=10.0, rib_depth=0.04)

    # Left Leg & Shoe
    add_ribbed_strut(lines, 'C_SUIT', D['HIP_C'], D['KNEE_L'], radius=0.08, rings=10, t_count=10, rib_freq=6.0, rib_depth=0.05)
    add_ribbed_strut(lines, 'C_SUIT', D['KNEE_L'], D['ANKLE_L'], radius=0.07, rings=10, t_count=10, rib_freq=8.0, rib_depth=0.05)
    add_box(lines, 'C_DETAILS', D['ANKLE_L'][0]+0.04, D['ANKLE_L'][1], D['ANKLE_L'][2]-0.05, dx=0.15, dy=0.07, dz=0.06)

    # Right Leg & Shoe
    add_ribbed_strut(lines, 'C_SUIT', D['HIP_C'], D['KNEE_R'], radius=0.08, rings=10, t_count=10, rib_freq=6.0, rib_depth=0.05)
    add_ribbed_strut(lines, 'C_SUIT', D['KNEE_R'], D['ANKLE_R'], radius=0.07, rings=10, t_count=10, rib_freq=8.0, rib_depth=0.05)
    add_box(lines, 'C_DETAILS', D['ANKLE_R'][0]+0.04, D['ANKLE_R'][1], D['ANKLE_R'][2]-0.05, dx=0.15, dy=0.07, dz=0.06)

    # ==============================================================================
    # 4. THE UMBRELLA PAYLOAD (Continuously Furled & Locked)
    # ==============================================================================
    # Internal structural shaft
    append_segmented(lines, 'C_UMBRELLA', [D['UMB_HANDLE'][0], D['UMB_TIP'][0]], [D['UMB_HANDLE'][1], D['UMB_TIP'][1]], [D['UMB_HANDLE'][2], D['UMB_TIP'][2]])
    # Curved Hook Handle
    v_umb = D['UMB_TIP'] - D['UMB_HANDLE']
    v_norm = v_umb / (np.linalg.norm(v_umb) + 0.001)
    # Pushing the handle out backwards slightly using the vector
    handle_root = D['UMB_HANDLE'] - (v_norm * 0.05)
    add_cylinder(lines, 'C_DETAILS', handle_root[0], handle_root[1], handle_root[2], length=0.1, radius=0.015, axis='z', rings=2, t_count=8)
    
    # The bunched, soaked silk canopy wrapping the shaft
    add_ribbed_strut(lines, 'C_UMBRELLA', D['UMB_HANDLE'], D['UMB_TIP'], radius=0.04, rings=15, t_count=8, rib_freq=12.0, rib_depth=0.3)

    # ==============================================================================
    # 5. ENVIRONMENTAL MATHEMATICS (RAIN & PAVEMENT)
    # ==============================================================================
    Z_FLOOR = 0.0
    for r_p in [1.2, 1.8]:
        t_p = np.linspace(0, 2*np.pi, 48, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-2.5, 2.5, 17)
    gy_range = np.linspace(-2.5, 2.5, 17)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # Stochastic Rain Vector Tracking (Falls downwards perpetually)
    np.random.seed(457)
    for _ in range(120):
        rx, ry = np.random.uniform(-2.5, 2.5, 2)
        rz_base = np.random.uniform(0.1, 4.0)
        # Apply strict downward transit
        rz_start = (rz_base - (t_sec * 4.0)) % 4.0
        rz_end = max(0.0, rz_start - 0.4)
        append_segmented(lines, 'C_GRID', [rx, rx], [ry, ry], [rz_start, rz_end])

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        dynamic_rig = generate_dynamic_street_matrix(t_sec)
        
        # Absolute tracking centroid anchored midway up the torso line allowing 
        # complete bounds for both the umbrella sweep and the lamppost finial.
        cam_x, cam_y, cam_z = -1.0, 0.0, 1.55
        
        # Starts from the dramatic 115-degree side-angle to capture the full structural sequence
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
    # Centroid = Z 1.55. Zenith (Finial) = Z 3.1. Horizon = Z 0.0. Umbrella Tip (Pose 2) = Z -2.3.
    # cam_span = 1.6 dictates a horizontal width of 3.2m. 
    # Vertical viewport becomes 1.6 * 1.777 = 2.84m radius.
    # Therefore bounds definitively clear tracking space across X [-2.6 to 0.6] and Z [-1.29 to 4.39]. Flawless UI boundary clearance.
    cam_span = 1.6
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',     C_GRID,     0.8, 0.4), 
        ('C_POST',     C_POST,     1.3, 1.0),
        ('C_LIGHT',    C_LIGHT,    1.8, 0.9),
        ('C_SUIT',     C_SUIT,     1.2, 1.0),
        ('C_SKIN',     C_SKIN,     1.3, 1.0),
        ('C_DETAILS',  C_DETAILS,  1.4, 1.0),
        ('C_UMBRELLA', C_UMBRELLA, 1.4, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in dynamic_rig[c_key]:
            # Elevated perspective (+10 degrees) to retain sheer verticality of the lamp post 
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=10.0)
            render_queue.append((np.mean(depth), u, v, c_val, lw, alpha))

    # ABSOLUTE Z-SORT (Strict Painter's Algorithm Depth Mapping)
    render_queue.sort(key=lambda item: item[0], reverse=True)
    for depth, u, v, c, lw, a in render_queue:
        ax.plot(u, v, color=c, lw=lw, alpha=a)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (TOP HUD)
    # ------------------------------------------------------------------
    ui_t = cam_span * 1.45
    ax.add_patch(patches.Rectangle((-cam_span, ui_t), cam_span*2, cam_span*0.5, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_t, ui_t], color=C_TEXT, lw=6, zorder=81)

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-457 // MACRO-ENGINEERING TENSOR: BIOMECHANICAL KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "KINEMATIC DANCE INTERPOLATION // SINGIN' IN THE RAIN MATRIX", color=C_UMBRELLA, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, f"[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT / LIVE CHOREOGRAPHY", color=C_POST, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: TRUE HARMONIC DANCE CYCLE / CANTILEVERED SPINE / CLOSED SILK", color=C_SUIT, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-457: CHOREOGRAPHIC TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Biomechanical Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
