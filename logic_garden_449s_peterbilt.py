"""
PROJECT: Logic Garden 449s (Exact Physical Construct // 1980 Peterbilt 359 Matrix - REVISION)
FORMAT: YouTube Shorts (1080x1920)
METADATA: PETERBILT 359, LONG NOSE TRUCK, TRACTOR, WIREFRAME, ENGINEERING, KINEMATICS, DIAGRAM
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Exact mechanical integration: Conventional Hood, 1 Steer + 2 Drives, Heavy Stacks, Flush Sleeper.
- Corrected Artifacts: Diagonal hood-clipping line permanently eradicated via explicit vector bounding.
- Parametric Peterbilt Front Fenders (True Arcs curving back into flat horizontal cabin steps).
- Native Typography Vector Array ("SIM GARDEN") embedded cleanly into sleeper flanks.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from absolute Side Profile.
- Daylight Palette (White Substrate / High-Contrast Edge Geometry).
- Purged Jargon. Australian spelling conventions (maths, colour, kilometres, aeroplane).
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
OUT_DIR = "frames_449s_peterbilt"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_CAB       = '#005599'          # Deep Marine (Matching classic Pete Blue mapping)
C_CHROME    = '#94A3B8'          # Machined Steel (Grille, Stacks, Tanks, Bumper, Visor)
C_CHASSIS   = '#1E293B'          # Carbon Slate (Frame Rails, 5th Wheel, Axles)
C_WHEEL     = '#111115'          # Indestructible Black (Tyre Treads)
C_LABEL     = '#FFB300'          # Dense Amber (SIM GARDEN Vector Fonts)
C_LIGHTS    = '#E11D48'          # Kinematic Red (Tail Lights, Roof Markers)
C_GRID      = '#CBD5E1'          # Subdued Steel (Baseplate Reference)

# ------------------------------------------------------------------
# O(N) KINEMATIC WIREFRAME ENGINE
# ------------------------------------------------------------------
def project_3d_depth(x, y, z, cx, cy, cz, az_deg, el_deg=0):
    tx, ty, tz = x - cx, y - cy, z - cz
    az, el = np.radians(az_deg), np.radians(el_deg)
    
    # Orbit Matrix
    x1 = tx * np.cos(az) - ty * np.sin(az)
    y1 = tx * np.sin(az) + ty * np.cos(az)
    z1 = tz
    
    # Elevation Matrix
    y2 = y1 * np.cos(el) - z1 * np.sin(el)
    z2 = y1 * np.sin(el) + z1 * np.cos(el)
    
    return x1, z2, y2 

def append_segmented(lines_dict, key, xs, ys, zs):
    """Absolute Segmentation Protocol: Splits arrays into 2-point vectors for strict mathematical depth sorting."""
    for i in range(len(xs) - 1):
        lines_dict[key].append(([xs[i], xs[i+1]], [ys[i], ys[i+1]], [zs[i], zs[i+1]]))

def extrude_profile(lines_dict, col_key, xz_points, y_min, y_max, close_loop=True):
    """Extrudes a 2D X-Z profile strictly across the Y-axis."""
    xs = [p[0] for p in xz_points]
    zs = [p[1] for p in xz_points]
    if close_loop:
        xs.append(xs[0])
        zs.append(zs[0])
        
    append_segmented(lines_dict, col_key, xs, [y_min]*len(xs), zs)
    append_segmented(lines_dict, col_key, xs, [y_max]*len(xs), zs)
    for x, z in xz_points:
        append_segmented(lines_dict, col_key, [x, x], [y_min, y_max], [z, z])

def add_cylinder(lines_dict, col_key, cx, cy, cz, length, radius, axis='y', rings=6, t_count=16):
    """Parametric cylinder generation locked to an explicit Cartesian axis."""
    t = np.linspace(0, 2*np.pi, t_count)
    steps = np.linspace(0, length, rings)
    
    for s in steps:
        if axis == 'y':  ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + s), cz + radius*np.sin(t)
        elif axis == 'x': ix, iy, iz = np.full_like(t, cx + s), cy + radius*np.cos(t), cz + radius*np.sin(t)
        else:             ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), np.full_like(t, cz + s)
        append_segmented(lines_dict, col_key, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
        
    for a in t[::(t_count//8)]: # Stringers
        if axis == 'y':   sx, sy, sz = [cx + radius*np.cos(a)]*rings, cy + steps, [cz + radius*np.sin(a)]*rings
        elif axis == 'x': sx, sy, sz = cx + steps, [cy + radius*np.cos(a)]*rings, [cz + radius*np.sin(a)]*rings
        else:             sx, sy, sz = [cx + radius*np.cos(a)]*rings, [cy + radius*np.sin(a)]*rings, cz + steps
        append_segmented(lines_dict, col_key, sx, sy, sz)

def add_box(lines_dict, col_key, cx, cy, cz, dx, dy, dz):
    """Rigid 3D orthogonal bounding-box construction."""
    hx, hy, hz = dx/2, dy/2, dz/2
    xs = [cx-hx, cx+hx, cx+hx, cx-hx, cx-hx]
    ys1 = [cy-hy, cy-hy, cy+hy, cy+hy, cy-hy]
    ys2 = [cy-hy, cy-hy, cy+hy, cy+hy, cy-hy]
    
    append_segmented(lines_dict, col_key, xs, ys1, [cz-hz]*5)
    append_segmented(lines_dict, col_key, xs, ys2, [cz+hz]*5)
    for i in range(4):
        append_segmented(lines_dict, col_key, [xs[i], xs[i]], [ys1[i], ys1[i]], [cz-hz, cz+hz])

def add_wheel(lines_dict, cx, cy, cz, radius=0.52, width=0.45):
    """Generates accurate heavy-haul tyre treads and wheels."""
    t = np.linspace(0, 2*np.pi, 20)
    for y_off in [-width/2, width/2]:
        ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + y_off), cz + radius*np.sin(t)
        append_segmented(lines_dict, 'C_WHEEL', list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
        # Wheel Rim Array
        ix_rim, iy_rim, iz_rim = cx + (radius*0.5)*np.cos(t), np.full_like(t, cy + y_off*1.05), cz + (radius*0.5)*np.sin(t)
        append_segmented(lines_dict, 'C_CHROME', list(ix_rim)+[ix_rim[0]], list(iy_rim)+[iy_rim[0]], list(iz_rim)+[iz_rim[0]])

    # Spanning Sidewall Treads
    for a in t[::2]:
        append_segmented(lines_dict, 'C_WHEEL', [cx+radius*np.cos(a)]*2, [cy-width/2, cy+width/2], [cz+radius*np.sin(a)]*2)

def draw_vector_text(lines_dict, text, start_x, y_plane, start_z, height, w_char, spacing, col, flip):
    """Explicitly translates typographic strings into rigid architectural vectors."""
    font = {
        'S': [[(1,1),(0,1),(0,0.5),(1,0.5),(1,0),(0,0)]],
        'I': [[(0.5,1),(0.5,0)], [(0,1),(1,1)], [(0,0),(1,0)]],
        'M': [[(0,0),(0,1),(0.5,0.5),(1,1),(1,0)]],
        'G': [[(1,1),(0,1),(0,0),(1,0),(1,0.5),(0.5,0.5)]],
        'A': [[(0,0),(0.5,1),(1,0)], [(0.25,0.5),(0.75,0.5)]],
        'R': [[(0,0),(0,1),(1,1),(1,0.5),(0,0.5)], [(0,0.5),(1,0)]],
        'D': [[(0,0),(0,1),(0.7,1),(1,0.7),(1,0.3),(0.7,0),(0,0)]],
        'E': [[(1,1),(0,1),(0,0),(1,0)], [(0,0.5),(0.8,0.5)]],
        'N': [[(0,0),(0,1),(1,0),(1,1)]],
        ' ': []
    }
    
    current_x = start_x
    for char in text:
        strokes = font.get(char, [])
        for stroke in strokes:
            sx, sy, sz = [], [], []
            for px, pz in stroke:
                if flip:
                    actual_x = current_x + (1.0 - px) * w_char
                else:
                    actual_x = current_x + px * w_char
                actual_z = start_z + pz * height
                sx.append(actual_x); sy.append(y_plane); sz.append(actual_z)
            append_segmented(lines_dict, col, sx, sy, sz)
        
        current_x += (w_char + spacing) if not flip else -(w_char + spacing)

# ------------------------------------------------------------------
# RIGID 3D EXACT KINEMATIC GENERATOR
# ------------------------------------------------------------------
def generate_peterbilt_vectors():
    lines = {
        'C_CAB': [], 'C_CHROME': [], 'C_CHASSIS': [], 
        'C_WHEEL': [], 'C_LABEL': [], 'C_LIGHTS': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. BASEPLATE ENVELOPE (REFERENCE GRID)
    # ==============================================================================
    gx_range = np.linspace(-9, 5, 29) 
    for gx in gx_range:
        append_segmented(lines, 'C_GRID', np.full_like(gx_range, gx), np.clip(gx_range, -2.5, 2.5), np.zeros_like(gx_range))
    gy_range = np.linspace(-2.5, 2.5, 11)
    for gy in gy_range:
        append_segmented(lines, 'C_GRID', np.clip(gx_range, -9, 5), np.full_like(gx_range, gy), np.zeros_like(gx_range))

    # ==============================================================================
    # 2. CHASSIS RAILS AND FIFTH WHEEL
    # ==============================================================================
    ch_x_front = -8.0
    ch_x_rear = 4.5
    cw = 0.45 # Chassis Half-width
    c_zt = 0.9  
    c_zb = 0.5  
    
    for sign in [-1, 1]:
        # Main heavy-duty linear rails
        append_segmented(lines, 'C_CHASSIS', [ch_x_front, ch_x_rear], [cw*sign, cw*sign], [c_zt, c_zt])
        append_segmented(lines, 'C_CHASSIS', [ch_x_front, ch_x_rear], [cw*sign, cw*sign], [c_zb, c_zb])
        
    # Massive Rear Crossmembers & Mudflap Hangers
    append_segmented(lines, 'C_CHASSIS', [ch_x_rear]*2, [-cw, cw], [c_zt, c_zt])
    append_segmented(lines, 'C_CHASSIS', [ch_x_rear]*2, [-cw, cw], [c_zb, c_zb])
    for sign in [-1, 1]:
        # Mudflaps strictly behind tandem wheels
        append_segmented(lines, 'C_WHEEL', [ch_x_rear, ch_x_rear], [0.5*sign, 1.25*sign], [0.9, 0.9])
        append_segmented(lines, 'C_WHEEL', [ch_x_rear, ch_x_rear], [0.5*sign, 1.25*sign], [0.1, 0.1])
        append_segmented(lines, 'C_WHEEL', [ch_x_rear, ch_x_rear], [1.25*sign, 1.25*sign], [0.9, 0.1])

    # True 3D 5th Wheel Plate (Over Tandems, x = 2.7)
    cx_5th, w_5th, z_5th = 2.7, 0.55, c_zt
    add_box(lines, 'C_STEEL' if 'C_STEEL' in lines else 'C_CHROME', cx_5th, 0.0, z_5th+0.1, 1.0, w_5th*2, 0.2)
    append_segmented(lines, 'C_CHROME', [cx_5th+0.5, cx_5th+1.1, cx_5th+1.1, cx_5th+0.5, cx_5th+0.5], 
                     [-w_5th, -w_5th, -0.2, -0.2, -w_5th], [z_5th+0.2, z_5th-0.1, z_5th-0.1, z_5th+0.2, z_5th+0.2])
    append_segmented(lines, 'C_CHROME', [cx_5th+0.5, cx_5th+1.1, cx_5th+1.1, cx_5th+0.5, cx_5th+0.5], 
                     [w_5th, w_5th, 0.2, 0.2, w_5th], [z_5th+0.2, z_5th-0.1, z_5th-0.1, z_5th+0.2, z_5th+0.2])

    # ==============================================================================
    # 3. CABIN & FLAT-TOP SLEEPER COMPARTMENT
    # ==============================================================================
    cab_w = 1.15
    cab_xf = -4.2  # Firewall flush coordinate
    cab_xr = -2.0  # Rear of Cab walls
    slp_xf = -1.8  # Start of sleeper (0.2m gap for exact Peterbilt structure)
    slp_xr =  1.0  # Rear of sleeper bounds
    
    cab_z_b = 1.0  # Cab Floor
    cab_z_m = 1.9  # Belt / Window line
    cab_z_t = 2.8  # Aerodynamic flush roof line
    
    for sign in [-1, 1]:
        y = cab_w * sign
        # Cab Core
        append_segmented(lines, 'C_CAB', [cab_xr, cab_xf, cab_xf, cab_xr, cab_xr], [y]*5, [cab_z_b, cab_z_b, cab_z_m, cab_z_m, cab_z_b])
        # Cab Greenhouse Layer
        append_segmented(lines, 'C_CAB', [cab_xr, cab_xf+0.1, cab_xf+0.1, cab_xr, cab_xr], [y]*5, [cab_z_m, cab_z_m, cab_z_t, cab_z_t, cab_z_m])
        # Front door window frame
        append_segmented(lines, 'C_CAB', [cab_xr+0.1, cab_xf+0.2, cab_xf+0.2, cab_xr+0.1, cab_xr+0.1], [y*1.01]*5, [1.2, 1.2, cab_z_t-0.1, cab_z_t-0.1, 1.2])
        
        # Sleeper Compartment Core (Flush Roof with Cabin)
        append_segmented(lines, 'C_CAB', [slp_xr, slp_xf, slp_xf, slp_xr, slp_xr], [y]*5, [cab_z_b, cab_z_b, cab_z_t, cab_z_t, cab_z_b])
        # Side access storage panel 
        append_segmented(lines, 'C_CHROME', [slp_xr-0.6, slp_xr-0.2, slp_xr-0.2, slp_xr-0.6, slp_xr-0.6], [y*1.02]*5, [1.2, 1.2, 1.9, 1.9, 1.2])

        # Large Cylindrical Air Cleaners (Firewall Mount)
        add_cylinder(lines, 'C_CHROME', cab_xf, 1.1*sign, 1.4, length=0.85, radius=0.25, axis='z', rings=5, t_count=12)
        
    # Transverse roof and floor bounding vectors
    for x, z in [(cab_xf, cab_z_m), (cab_xf+0.1, cab_z_t), (cab_xr, cab_z_t), (slp_xf, cab_z_t), (slp_xr, cab_z_t), (slp_xr, cab_z_b)]:
        append_segmented(lines, 'C_CAB', [x, x], [-cab_w, cab_w], [z, z])

    # Distinct Angled Chrome Sun Visor
    append_segmented(lines, 'C_CHROME', [cab_xf+0.1, cab_xf-0.2, cab_xf-0.2, cab_xf+0.1], [-cab_w, -cab_w, cab_w, cab_w], [cab_z_t, cab_z_t-0.2, cab_z_t-0.2, cab_z_t])
    
    # Roof Bullet Markers
    for mk_y in np.linspace(-0.6, 0.6, 5):
        add_cylinder(lines, 'C_LIGHTS', cab_xf+0.3, mk_y, cab_z_t, 0.15, 0.04, axis='x')

    # ==============================================================================
    # 4. LONG-NOSE HOOD & EXPLICIT CHROME FASCIA
    # ==============================================================================
    hood_xf = -7.6
    hood_w = 0.85
    hood_z_t = 1.7
    
    # EXPLICIT HOOD BOUNDS: Manual segmentation guarantees absolutely zero diagonal clipping lines.
    for sign in [-1, 1]:
        y = hood_w * sign
        append_segmented(lines, 'C_CAB', [cab_xf, hood_xf], [y, y], [hood_z_t, hood_z_t])
        append_segmented(lines, 'C_CAB', [cab_xf, hood_xf], [y, y], [cab_z_b, cab_z_b])
        append_segmented(lines, 'C_CAB', [hood_xf, hood_xf], [y, y], [cab_z_b, hood_z_t])
    append_segmented(lines, 'C_CAB', [hood_xf, hood_xf], [-hood_w, hood_w], [hood_z_t, hood_z_t])
    append_segmented(lines, 'C_CAB', [cab_xf, hood_xf], [0, 0], [hood_z_t, hood_z_t]) # Center line ridge
    
    # Square Chrome Grille Array
    append_segmented(lines, 'C_CHROME', [hood_xf, hood_xf], [-hood_w, hood_w], [hood_z_t-0.05, hood_z_t-0.05])
    append_segmented(lines, 'C_CHROME', [hood_xf, hood_xf], [-hood_w, hood_w], [cab_z_b, cab_z_b])
    for gr_y in np.linspace(-hood_w+0.1, hood_w-0.1, 10):
        append_segmented(lines, 'C_CHROME', [hood_xf, hood_xf], [gr_y, gr_y], [cab_z_b, hood_z_t-0.05])

    # Massive Front Box Bumper
    add_box(lines, 'C_CHROME', hood_xf-0.1, 0.0, 0.6, dx=0.3, dy=2.4, dz=0.4)
    
    # Dual Headlight Buckets
    for hl_y in [-1.15, 1.15]:
        add_cylinder(lines, 'C_CHROME', hood_xf, hl_y, 1.05, 0.25, 0.15, axis='x')
        append_segmented(lines, 'C_CHROME', [hood_xf+0.15, hood_xf+0.15], [hl_y, np.sign(hl_y)*hood_w], [1.05, 1.05])

    # SWEEPING PETERBILT FENDERS (True Arc Logic)
    # Mapping explicitly from the bumper arching over the tyre and running completely flat to the cab base
    xf_pts = np.linspace(-7.6, -4.2, 35)
    zf_pts = []
    for x in xf_pts:
        if x < -6.4: # Front quadrant of arc
            r_z = np.sqrt(max(0.001, 1.0**2 - (x - -6.4)**2))
            zf_pts.append(0.52 + r_z * 0.8)
        elif x < -5.4: # Decent into flat step
            r_z = np.sqrt(max(0.001, 1.0**2 - (x - -6.4)**2))
            z_arch = 0.52 + r_z * 0.8
            blend = (x - -6.4) / 1.0
            zf_pts.append(z_arch * (1-blend) + 0.9 * blend)
        else: # True flat step bound to firewall
            zf_pts.append(0.9)
            
    for sign in [-1, 1]:
        fy_in = np.full_like(xf_pts, hood_w*sign)
        fy_out = np.full_like(xf_pts, 1.25*sign)
        append_segmented(lines, 'C_CAB', list(xf_pts), list(fy_in), list(zf_pts))
        append_segmented(lines, 'C_CAB', list(xf_pts), list(fy_out), list(zf_pts))
        for i in range(len(xf_pts)):
            append_segmented(lines, 'C_CAB', [xf_pts[i], xf_pts[i]], [fy_in[i], fy_out[i]], [zf_pts[i], zf_pts[i]])

    # ==============================================================================
    # 5. HEAVY EXHAUST STACKS & FUEL TANKS
    # ==============================================================================
    # Exhaust stacks securely locked in the absolute X gap between cab and sleeper 
    sx = -1.9
    for sign in [-1, 1]:
        add_cylinder(lines, 'C_CHROME', sx, 1.25*sign, 0.9, 3.5, 0.15, axis='z', rings=10)
        # Smooth turning curved top exhaust 
        to_th = np.linspace(np.pi, 3*np.pi/2, 8)
        tx = sx + 0.3*np.cos(to_th) + 0.3
        tz = 4.4 + 0.3*np.sin(to_th)
        append_segmented(lines, 'C_CHROME', list(tx), [1.15*sign]*len(tx), list(tz))
        append_segmented(lines, 'C_CHROME', list(tx), [1.35*sign]*len(tx), list(tz))

    # Deep Cylindrical Fuel Tanks running below doors
    tank_length = 3.6
    tk_x = -3.7
    for sign in [-1, 1]:
        add_cylinder(lines, 'C_CHROME', tk_x, 1.15*sign, 0.65, tank_length, 0.35, axis='x', rings=12, t_count=20)
        # Retention straps
        add_cylinder(lines, 'C_CHASSIS', tk_x+0.5, 1.15*sign, 0.65, 0.05, 0.36, axis='x', rings=2)
        add_cylinder(lines, 'C_CHASSIS', tk_x+3.1, 1.15*sign, 0.65, 0.05, 0.36, axis='x', rings=2)

    # ==============================================================================
    # 6. TYRE AND AXLE KINEMATICS (1 STEER, 2 DRIVES)
    # ==============================================================================
    y_out = 1.15
    y_in = 0.65
    r_tyre = 0.52
    
    # 1 Forward Steer Axle (Explicit single bounding)
    cx_steer = -6.4
    for sign in [-1, 1]:
        add_wheel(lines, cx_steer, y_out*sign, r_tyre)
        
    # 2 Heavy Tandem Drive Axles (Dual tyre pairing per side)
    for dr_x in [2.0, 3.4]:
        for sign in [-1, 1]:
            add_wheel(lines, dr_x, y_out*sign, r_tyre)
            add_wheel(lines, dr_x, y_in*sign, r_tyre)

    # ==============================================================================
    # 7. EXPLICIT TYPOGRAPHY TENSOR ("SIM GARDEN" ON SLEEPER)
    # ==============================================================================
    # Exact geometric stroke projection centered onto the flat sleeper outer walls
    text1 = "SIM"
    text2 = "GARDEN"
    
    # Parameters: w_char=0.2, spacing=0.06 -> 'SIM' = 0.72 span, 'GARDEN' = 1.5span
    # Left (Port) Side - X draws backward: start at positive X and draw negative (-X)
    draw_vector_text(lines, text1, 0.15, cab_w+0.05, 2.2, 0.3, 0.2, 0.06, 'C_LABEL', flip=True)
    draw_vector_text(lines, text2, 0.60, cab_w+0.05, 1.7, 0.3, 0.2, 0.06, 'C_LABEL', flip=True)

    # Right (Starboard) Side - X draws forward: start at negative X and draw positive (+X)
    draw_vector_text(lines, text1, -0.65, -cab_w-0.05, 2.2, 0.3, 0.2, 0.06, 'C_LABEL', flip=False)
    draw_vector_text(lines, text2, -1.10, -cab_w-0.05, 1.7, 0.3, 0.2, 0.06, 'C_LABEL', flip=False)

    return lines

# ------------------------------------------------------------------
# PARALLEL GENERATOR STREAM (KINEMATIC TIMELINE TENSOR)
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_peterbilt_vectors()

    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Central Basepoint rigidly mapped to the true physical center of the long-nose chassis
        cam_x, cam_y, cam_z = -1.2, 0.0, 1.5 
        
        # Continuous 360-degree perfect orbital synchronisation
        # Initiates strictly from Right Side Profile (Azimuth = 90.0)
        azimuth = 90.0 - (stage * 360.0)

        yield (f, t_sec, azimuth, cam_x, cam_y, cam_z, static_rig)

# ------------------------------------------------------------------
# THREAD-SAFE PAINTER'S RENDERER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, azimuth, cx, cy, cz, static_rig = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # Cinematic Rigid Map Boundary scales massive 12+ meter footprint
    cam_span = 9.8
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []

    # 1. PROCESS KINEMATIC VECTOR MATRIX
    for c_key, c_val in [('C_GRID', C_GRID), ('C_CAB', C_CAB), ('C_CHASSIS', C_CHASSIS), 
                         ('C_WHEEL', C_WHEEL), ('C_CHROME', C_CHROME), ('C_LABEL', C_LABEL), ('C_LIGHTS', C_LIGHTS)]:
        
        if c_key == 'C_GRID': lw, alpha = 0.8, 0.4
        elif c_key == 'C_WHEEL': lw, alpha = 1.3, 1.0 
        elif c_key == 'C_CAB': lw, alpha = 1.6, 1.0
        elif c_key == 'C_CHROME': lw, alpha = 1.4, 1.0
        elif c_key == 'C_LABEL': lw, alpha = 3.5, 1.0 # Emboldened typography payload
        elif c_key == 'C_LIGHTS': lw, alpha = 2.5, 1.0
        else: lw, alpha = 1.0, 1.0
            
        for xl, yl, zl in static_rig[c_key]:
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=16.0)
            render_queue.append((np.mean(depth), u, v-1.0, c_val, lw, alpha))

    # 2. ABSOLUTE PAINTER'S ALGORITHM
    render_queue.sort(key=lambda item: item[0], reverse=True)

    for depth, u, v, c, lw, a in render_queue:
        ax.plot(u, v, color=c, lw=lw, alpha=a)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (TOP HUD)
    # ------------------------------------------------------------------
    ui_t = cam_span * 1.45
    ax.add_patch(patches.Rectangle((-cam_span, ui_t), cam_span*2, 6.0, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_t, ui_t], color=C_TEXT, lw=6, zorder=81)

    ax.text(-cam_span*0.95, ui_t+1.3, "LG-449s // MACRO-ENGINEERING TENSOR: HEAVY HAUL", color=C_TEXT, fontsize=22, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t+0.3, "EXPLICIT TRUE-SCALE GEOMETRY // 1980 PETERBILT 359 MATRIX", color=C_CAB, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b+2.2, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_CHROME, fontsize=17, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+1.1, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=17, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.2, "GEOMETRY YIELD   : LONG-NOSE HOOD / SWEEPING FENDERS BOUND", color=C_LABEL, fontsize=16, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-449s: LONG-NOSE PETERBILT ENGINEERING TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Transport Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
