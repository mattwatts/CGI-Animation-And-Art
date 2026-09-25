"""
PROJECT: Logic Garden 450a (Exact Physical Construct // Heavy V-Twin Cruiser Matrix - HOTFIX 2)
FORMAT: YouTube Shorts (1080x1920)
METADATA: MOTORCYCLE, MOTORBIKE, CRUISER, V-TWIN, WIREFRAME, ENGINEERING, KINEMATICS, AUTOMOTIVE
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: True parametric 45-degree V-Twin block, staggered asymmetric exhaust, raked front forks, and explicit cast mag wheels.
- Hotfix 2: Reinstated the 'add_box' geometrical primitive function.
- Forward Alignment: Rig operates flawlessly travelling into +X. Wheels rotate forward.
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
OUT_DIR = "frames_450a_motorbike"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Baseplate Reference)
C_WHEEL     = '#111115'          # Indestructible Black (Tyre Treads / Rubber Grips)

C_FRAME     = '#1E293B'          # Carbon Slate (Tubular Cradle Frame & Swingarm)
C_LIVERY    = '#BE123C'          # Deep Crimson (Teardrop Tank & Swept Fenders)
C_ENGINE    = '#475569'          # Machined Cast Iron (Cylinders, Primary Drive)
C_CHROME    = '#94A3B8'          # Polished Steel (Exhaust, Forks, Handlebars, Shocks)
C_SEAT      = '#020617'          # Obsidian Leather (Stepped Saddle)
C_LIGHTS    = '#FFB300'          # Dense Amber (Turn Signals, Headlight Lens)
C_TAIL      = '#E11D48'          # Kinematic Red (Rear Brake Lamp)

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
    for i in range(len(xs) - 1):
        x1 = xs[i] * scale_x + dx
        x2 = xs[i+1] * scale_x + dx
        lines_dict[key].append(([x1, x2], [ys[i]+dy, ys[i+1]+dy], [zs[i]+dz, zs[i+1]+dz]))

def rotate_y_pitch(x, y, z, cx, cz, pitch_deg):
    p = np.radians(pitch_deg)
    x0, z0 = x - cx, z - cz
    x1 = x0 * np.cos(p) - z0 * np.sin(p)
    z1 = x0 * np.sin(p) + z0 * np.cos(p)
    return x1 + cx, y, z1 + cz

# ------------------------------------------------------------------
# GEOMETRIC PRIMITIVES
# ------------------------------------------------------------------
def extrude_profile(lines_dict, col, xz_points, y_min, y_max, close_loop=True, off=(0,0,0)):
    xs = [p[0] for p in xz_points]; zs = [p[1] for p in xz_points]
    if close_loop:
        xs.append(xs[0]); zs.append(zs[0])
    append_segmented(lines_dict, col, xs, [y_min]*len(xs), zs, off)
    append_segmented(lines_dict, col, xs, [y_max]*len(xs), zs, off)
    for x, z in xz_points:
        append_segmented(lines_dict, col, [x, x], [y_min, y_max], [z, z], off)

def add_box(lines_dict, col, cx, cy, cz, dx, dy, dz, off=(0,0,0)):
    hx, hy, hz = dx/2, dy/2, dz/2
    xs = [cx-hx, cx+hx, cx+hx, cx-hx, cx-hx]
    ys1 = [cy-hy, cy-hy, cy+hy, cy+hy, cy-hy]
    ys2 = [cy-hy, cy-hy, cy+hy, cy+hy, cy-hy]
    
    append_segmented(lines_dict, col, xs, ys1, [cz-hz]*5, off)
    append_segmented(lines_dict, col, xs, ys2, [cz+hz]*5, off)
    for i in range(4):
        append_segmented(lines_dict, col, [xs[i], xs[i]], [ys1[i], ys1[i]], [cz-hz, cz+hz], off)

def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='y', rings=6, t_count=16, off=(0,0,0)):
    t = np.linspace(0, 2*np.pi, t_count)
    steps = np.linspace(0, length, rings)
    for s in steps:
        if axis == 'y':  ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + s), cz + radius*np.sin(t)
        elif axis == 'x': ix, iy, iz = np.full_like(t, cx + s), cy + radius*np.cos(t), cz + radius*np.sin(t)
        else:             ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), np.full_like(t, cz + s)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]], off)
    for a in t[::max(1, t_count//8)]:
        if axis == 'y':   sx, sy, sz = [cx + radius*np.cos(a)]*rings, cy + steps, [cz + radius*np.sin(a)]*rings
        elif axis == 'x': sx, sy, sz = cx + steps, [cy + radius*np.cos(a)]*rings, [cz + radius*np.sin(a)]*rings
        else:             sx, sy, sz = [cx + radius*np.cos(a)]*rings, [cy + radius*np.sin(a)]*rings, cz + steps
        append_segmented(lines_dict, col, sx, sy, sz, off)

# ------------------------------------------------------------------
# KINEMATIC DYNAMIC WHEELS
# ------------------------------------------------------------------
def add_rotating_wheel(lines_dict, cx, cy, cz, radius, width, rot_angle, spokes=13, mag_ratio=0.8, off=(0,0,0)):
    # Simulates continuous forward +X momentum by rotating negatively
    t = np.linspace(0, 2*np.pi, 24) - rot_angle
    
    # Outer Tyre Matrix
    for y_off in [-width/2, width/2]:
        ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + y_off), cz + radius*np.sin(t)
        append_segmented(lines_dict, 'C_WHEEL', list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]], off)
        
        # Chrome Mag Wheel Lip
        ix_rim, iy_rim, iz_rim = cx + (radius*mag_ratio)*np.cos(t), np.full_like(t, cy + y_off*1.02), cz + (radius*mag_ratio)*np.sin(t)
        append_segmented(lines_dict, 'C_CHROME', list(ix_rim)+[ix_rim[0]], list(iy_rim)+[iy_rim[0]], list(iz_rim)+[iz_rim[0]], off)
    
    # Cross Tyre Treads
    for a in t[::2]:
        append_segmented(lines_dict, 'C_WHEEL', [cx+radius*np.cos(a)]*2, [cy-width/2, cy+width/2], [cz+radius*np.sin(a)]*2, off)

    # Internal Machined Cast Spokes Array
    spoke_angles = np.linspace(0, 2*np.pi, spokes, endpoint=False) - rot_angle
    for sa in spoke_angles:
        px = cx + (radius*mag_ratio)*np.cos(sa)
        pz = cz + (radius*mag_ratio)*np.sin(sa)
        # Hub to Mag lip tie
        append_segmented(lines_dict, 'C_CHROME', [cx, px], [cy+width/3.5, cy+width/3.5], [cz, pz], off)
        append_segmented(lines_dict, 'C_CHROME', [cx, px], [cy-width/3.5, cy-width/3.5], [cz, pz], off)

# ------------------------------------------------------------------
# STATIC SUPERSTRUCTURE BUILDERS (MOTORBIKE)
# ------------------------------------------------------------------
def generate_motorbike_static():
    lines = {
        'C_FRAME': [], 'C_LIVERY': [], 'C_ENGINE': [], 'C_CHROME': [], 
        'C_SEAT': [], 'C_LIGHTS': [], 'C_TAIL': [], 'C_WHEEL': [], 'C_GRID': []
    }

    # 1. BASEPLATE ENVELOPE (REFERENCE GRID)
    # Absolute scale derived from 1.625m wheelbase context
    gx_range = np.linspace(-2.0, 2.0, 17)
    gy_range = np.linspace(-1.0, 1.0, 9)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gx_range, gx), np.clip(gx_range, -1.0, 1.0), np.zeros_like(gx_range))
    for gy in gy_range: append_segmented(lines, 'C_GRID', np.clip(gx_range, -2.0, 2.0), np.full_like(gx_range, gy), np.zeros_like(gx_range))

    # Kinematic Axis Centres
    x_front = 0.812
    x_rear = -0.812

    # 2. V-TWIN ENGINE BLOCK (The Mechanical Tensor)
    # Crankcase
    add_cylinder(lines, 'C_ENGINE', 0.0, -0.15, 0.35, 0.3, 0.18, axis='y', rings=4)
    # Heavy Primary Drive Case (Asymmetrically heavy to the Left side)
    add_cylinder(lines, 'C_ENGINE', -0.2, -0.25, 0.35, 0.1, 0.15, axis='y', rings=2)
    extrude_profile(lines, 'C_ENGINE', [(0.0, 0.5), (-0.2, 0.5), (-0.25, 0.2), (-0.1, 0.2), (0.1, 0.2)], -0.3, -0.15)
    
    # 45-Degree Fin-Cooled Cylinder Heads
    # Front Jug (Slanted Forward)
    for fl in np.linspace(0.4, 0.72, 10): # High-density cooling fins
        fx1, _, fz1 = rotate_y_pitch(0.05, 0.0, fl, 0.0, 0.35, -25.0)
        fx2, _, fz2 = rotate_y_pitch(0.15, 0.0, fl, 0.0, 0.35, -25.0)
        append_segmented(lines, 'C_ENGINE', [fx1, fx2], [-0.12, -0.12], [fz1, fz2])
        append_segmented(lines, 'C_ENGINE', [fx1, fx2], [0.12, 0.12], [fz1, fz2])
        append_segmented(lines, 'C_ENGINE', [fx1, fx1], [-0.12, 0.12], [fz1, fz1])
        append_segmented(lines, 'C_ENGINE', [fx2, fx2], [-0.12, 0.12], [fz2, fz2])

    # Rear Jug (Slanted Backward)
    for fl in np.linspace(0.4, 0.72, 10):
        fx1, _, fz1 = rotate_y_pitch(-0.05, 0.0, fl, 0.0, 0.35, 20.0)
        fx2, _, fz2 = rotate_y_pitch(-0.15, 0.0, fl, 0.0, 0.35, 20.0)
        append_segmented(lines, 'C_ENGINE', [fx1, fx2], [-0.12, -0.12], [fz1, fz2])
        append_segmented(lines, 'C_ENGINE', [fx1, fx2], [0.12, 0.12], [fz1, fz2])
        append_segmented(lines, 'C_ENGINE', [fx1, fx1], [-0.12, 0.12], [fz1, fz1])
        append_segmented(lines, 'C_ENGINE', [fx2, fx2], [-0.12, 0.12], [fz2, fz2])

    # Rounded Overhanging Air Cleaner (Explicitly on the Right side)
    add_cylinder(lines, 'C_CHROME', 0.02, 0.15, 0.55, 0.1, 0.14, axis='y', rings=4, t_count=16)

    # 3. TUBULAR CHASSIS & SUSPENSION
    # Backbone
    append_segmented(lines, 'C_FRAME', [0.55, -0.3], [0.0, 0.0], [0.85, 0.65])
    # Down-tubes looping under engine
    append_segmented(lines, 'C_FRAME', [0.55, 0.3, 0.1, -0.3], [0.1, 0.1, 0.1, 0.1], [0.85, 0.25, 0.25, 0.3])
    append_segmented(lines, 'C_FRAME', [0.55, 0.3, 0.1, -0.3], [-0.1, -0.1, -0.1, -0.1], [0.85, 0.25, 0.25, 0.3])
    
    # Raked Front Forks (30-degree offset targeting Front Axle)
    fork_t = 0.95; fork_b = 0.31
    for fy in [-0.12, 0.12]:
        append_segmented(lines, 'C_CHROME', [0.50, x_front], [fy, fy], [fork_t, fork_b])
        # Fork thick sliders
        append_segmented(lines, 'C_CHROME', [0.65, x_front], [fy+0.01, fy+0.01], [0.55, fork_b])
    # Triple trees mapping structural binding
    for f_ty in [0.93, 0.82]:
        append_segmented(lines, 'C_CHROME', [0.51, 0.51], [-0.14, 0.14], [f_ty, f_ty])
        
    # Swingarm logic
    append_segmented(lines, 'C_FRAME', [-0.25, x_rear], [0.15, 0.15], [0.35, 0.32])
    append_segmented(lines, 'C_FRAME', [-0.25, x_rear], [-0.15, -0.15], [0.35, 0.32])

    # Dynamic Dual Rear Coil Shocks
    for sy in [-0.14, 0.14]:
        append_segmented(lines, 'C_CHROME', [-0.6, -0.55], [sy, sy], [0.33, 0.66])
        # Visualised Suspension Spring winding radially
        s_th = np.linspace(0, 10*np.pi, 40)
        sx = -0.6 + (0.05 * (s_th/(10*np.pi))) + 0.03*np.cos(s_th)
        sz = 0.33 + (0.33 * (s_th/(10*np.pi)))
        sy_arr = sy + 0.03*np.sin(s_th)
        append_segmented(lines, 'C_CHROME', list(sx), list(sy_arr), list(sz))

    # 4. TEARDROP TANK & STEPPED SADDLE
    tank_prof = [(0.5, 0.85), (0.2, 0.92), (-0.1, 0.78), (-0.2, 0.65), (0.5, 0.65)]
    extrude_profile(lines, 'C_LIVERY', tank_prof, -0.25, 0.25)
    
    seat_prof = [(-0.15, 0.73), (-0.4, 0.62), (-0.7, 0.65), (-0.8, 0.65), (-0.8, 0.55), (-0.15, 0.55)]
    extrude_profile(lines, 'C_SEAT', seat_prof, -0.22, 0.22)

    # 5. ASYMMETRICAL STAGGERED DUAL EXHAUST TENSOR (Right Y-Plane routing purely)
    py = 0.28
    # Front pipe sweeping down and straight back
    f_px = [0.15, 0.25,  0.2, -0.2, -0.6]
    f_pz = [0.65, 0.45, 0.25, 0.25,  0.25]
    append_segmented(lines, 'C_CHROME', f_px, [py]*5, f_pz)
    append_segmented(lines, 'C_CHROME', f_px, [py+0.04]*5, f_pz)
    # Heavy slashed muffler block
    add_cylinder(lines, 'C_CHROME', -0.7, py, 0.25, 0.1, 0.06, axis='x', rings=3)
    
    # Rear pipe sweeping tight and crossing above primary constraint
    r_px = [-0.15, -0.05, -0.1, -0.4, -0.8]
    r_pz = [ 0.65,  0.55, 0.35, 0.35,  0.35]
    append_segmented(lines, 'C_CHROME', r_px, [py]*5, r_pz)
    append_segmented(lines, 'C_CHROME', r_px, [py+0.04]*5, r_pz)
    add_cylinder(lines, 'C_CHROME', -0.9, py, 0.35, 0.1, 0.06, axis='x', rings=3)

    # 6. EXTERNAL LIVERY & APPENDAGES
    # Swept Front Fender 
    f_th = np.linspace(np.pi*0.4, np.pi*0.9, 12)
    fx = x_front + 0.38*np.cos(f_th)
    fz = 0.33 + 0.38*np.sin(f_th)
    append_segmented(lines, 'C_LIVERY', list(fx), [-0.1]*12, list(fz))
    append_segmented(lines, 'C_LIVERY', list(fx), [ 0.1]*12, list(fz))
    for i in range(12): append_segmented(lines, 'C_LIVERY', [fx[i]]*2, [-0.1, 0.1], [fz[i]]*2)
    
    # Deep Rear Fender (chopped profile mapping wheel arc)
    r_th = np.linspace(np.pi*0.2, np.pi, 20)
    rx = x_rear + 0.4*np.cos(r_th)
    rz = 0.33 + 0.4*np.sin(r_th)
    append_segmented(lines, 'C_LIVERY', list(rx), [-0.18]*20, list(rz))
    append_segmented(lines, 'C_LIVERY', list(rx), [ 0.18]*20, list(rz))
    for i in range(20): append_segmented(lines, 'C_LIVERY', [rx[i]]*2, [-0.18, 0.18], [rz[i]]*2)

    # Bullet Headlight Matrix
    add_cylinder(lines, 'C_CHROME', 0.6, -0.08, 0.85, 0.16, 0.08, axis='y', rings=3)
    add_cylinder(lines, 'C_LIGHTS', 0.68, -0.06, 0.85, 0.12, 0.07, axis='y', rings=2)

    # Distinctive Cruiser Handlebars (Buckhorn/Ape sweep)
    # Riser central
    append_segmented(lines, 'C_CHROME', [0.45, 0.48], [0.0, 0.0], [0.95, 1.05])
    # Sweep out and back
    append_segmented(lines, 'C_CHROME', [0.48, 0.45, 0.35], [0.0, 0.25, 0.45], [1.05, 1.15, 1.1])
    append_segmented(lines, 'C_CHROME', [0.48, 0.45, 0.35], [0.0, -0.25, -0.45], [1.05, 1.15, 1.1])
    
    # Hand Grips (Rubber Black mapped securely to existing C_WHEEL vector)
    add_cylinder(lines, 'C_WHEEL', 0.35,  0.45, 1.1, 0.08, 0.02, axis='x')
    add_cylinder(lines, 'C_WHEEL', 0.35, -0.53, 1.1, 0.08, 0.02, axis='x')
    
    # Mirrors bridging upward from controls
    append_segmented(lines, 'C_CHROME', [0.38, 0.42], [0.4, 0.45], [1.13, 1.25])
    append_segmented(lines, 'C_CHROME', [0.38, 0.42], [-0.4, -0.45], [1.13, 1.25])
    add_cylinder(lines, 'C_CHROME', 0.42, 0.42, 1.25, 0.06, 0.05, axis='y', rings=3)
    add_cylinder(lines, 'C_CHROME', 0.42, -0.48, 1.25, 0.06, 0.05, axis='y', rings=3)
    
    # Brake/Tailight box mounted structurally on rear fender lip
    add_box(lines, 'C_TAIL', -1.15, 0.0, 0.5, 0.08, 0.15, 0.1)

    return lines


def generate_dynamic_wheels(lines, rot_angle):
    x_front = 0.812
    x_rear = -0.812
    
    # Front Wheel: Narrow aspect, dense 13-spoke cast mag visually scaling
    add_rotating_wheel(lines, x_front, 0.0, 0.33, 0.33, 0.14, rot_angle, spokes=13, mag_ratio=0.8)
    
    # Rear Wheel: Burly wide-tyre parameter, 13-spoke cast mag
    add_rotating_wheel(lines, x_rear, 0.0, 0.32, 0.32, 0.22, rot_angle, spokes=13, mag_ratio=0.75)

# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_motorbike_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        cam_x, cam_y, cam_z = -0.2, 0.0, 0.6 
        
        # 360-degree perfect orbital synchronisation (Starts exactly from Right Side +Y profile mapping)
        azimuth = 90.0 - (stage * 360.0)

        # Operational Drive Velocity (8 full cyclic rotation driving +X seamlessly)
        rot_angle = stage * 8.0 * 2.0 * np.pi

        yield (f, t_sec, azimuth, rot_angle, cam_x, cam_y, cam_z, static_rig)

def render_frame(packet):
    f, t_sec, azimuth, rot_angle, cx, cy, cz, static_rig = packet

    local_rig = {k: v.copy() for k,v in static_rig.items()}
    generate_dynamic_wheels(local_rig, rot_angle)

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    cam_span = 1.95
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID', C_GRID, 0.8, 0.4), ('C_WHEEL', C_WHEEL, 1.4, 1.0),
        ('C_CHROME', C_CHROME, 1.3, 1.0), ('C_ENGINE', C_ENGINE, 1.2, 1.0),
        ('C_FRAME', C_FRAME, 1.6, 1.0), ('C_LIVERY', C_LIVERY, 1.8, 1.0), 
        ('C_SEAT', C_SEAT, 1.8, 1.0), ('C_LIGHTS', C_LIGHTS, 2.2, 1.0), 
        ('C_TAIL', C_TAIL, 2.2, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in local_rig[c_key]:
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=10.0)
            render_queue.append((np.mean(depth), u, v-0.1, c_val, lw, alpha))

    # ABSOLUTE Z-SORT
    render_queue.sort(key=lambda item: item[0], reverse=True)
    for depth, u, v, c, lw, a in render_queue:
        ax.plot(u, v, color=c, lw=lw, alpha=a)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (TOP HUD)
    # ------------------------------------------------------------------
    ui_t = cam_span * 1.45
    ax.add_patch(patches.Rectangle((-cam_span, ui_t), cam_span*2, 6.0, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_t, ui_t], color=C_TEXT, lw=6, zorder=81)

    ax.text(-cam_span*0.95, ui_t+1.5, "LG-450a // MACRO-ENGINEERING TENSOR: CRUISER KINEMATICS", color=C_TEXT, fontsize=17, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t+0.5, "EXPLICIT TRUE-SCALE GEOMETRY // ASYMMETRICAL V-TWIN MATRIX", color=C_LIVERY, fontsize=13, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b+0.85, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_CHROME, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.45, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.05, "WHEEL VELOCITY   : FORWARD ORBITAL SYNCHRONISATION LOCKED", color=C_ENGINE, fontsize=13, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-450a: MOTORCYCLE KINEMATICS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Automotive Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
