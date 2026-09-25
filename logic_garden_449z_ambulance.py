"""
PROJECT: Logic Garden 449z (Exact Physical Construct // Ambulance Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: AMBULANCE, EMS, PARAMEDIC, WIREFRAME, ENGINEERING, KINEMATICS, AUTOMOTIVE
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Dual-hull geometry (Cab + Box), rigid fender flares, extruded AC units, and high-visibility lightbars.
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
OUT_DIR = "frames_449z_ambulance"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Baseplate Reference)
C_WHEEL     = '#111115'          # Indestructible Black (Tyre Treads)

C_BODY      = '#1E293B'          # Carbon Slate (Main Extrusion Edges)
C_STRIPE    = '#E11D48'          # Kinematic Red (High-Contrast Livery Vector)
C_CHROME    = '#94A3B8'          # Machined Steel (Bumpers, Rims, Grille)
C_GLASS     = '#005599'          # Deep Marine (Cab & Box Windows)
C_LIGHTS_B  = '#0ea5e9'          # Electric Blue (Primary Lightbars)
C_LIGHTS_R  = '#BE123C'          # Ruby (Secondary Strobes/Tail-lights)

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
    xs = [cx-hx, cx+hx, cx+hx, cx-hx, cx-hx]; ys1 = [cy-hy]*2 + [cy+hy]*2 + [cy-hy]; ys2 = ys1[:]
    append_segmented(lines_dict, col, xs, ys1, [cz-hz]*5, off)
    append_segmented(lines_dict, col, xs, ys2, [cz+hz]*5, off)
    for i in range(4): append_segmented(lines_dict, col, [xs[i], xs[i]], [ys1[i], ys1[i]], [cz-hz, cz+hz], off)

def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='y', rings=6, t_count=16, off=(0,0,0)):
    t = np.linspace(0, 2*np.pi, t_count)
    steps = np.linspace(0, length, rings)
    for s in steps:
        if axis == 'y':  ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + s), cz + radius*np.sin(t)
        elif axis == 'x': ix, iy, iz = np.full_like(t, cx + s), cy + radius*np.cos(t), cz + radius*np.sin(t)
        else:             ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), np.full_like(t, cz + s)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]], off)
    for a in t[::(t_count//8)]:
        if axis == 'y':   sx, sy, sz = [cx + radius*np.cos(a)]*rings, cy + steps, [cz + radius*np.sin(a)]*rings
        elif axis == 'x': sx, sy, sz = cx + steps, [cy + radius*np.cos(a)]*rings, [cz + radius*np.sin(a)]*rings
        else:             sx, sy, sz = [cx + radius*np.cos(a)]*rings, [cy + radius*np.sin(a)]*rings, cz + steps
        append_segmented(lines_dict, col, sx, sy, sz, off)

# ------------------------------------------------------------------
# KINEMATIC DYNAMIC WHEELS
# ------------------------------------------------------------------
def add_rotating_wheel(lines_dict, cx, cy, cz, radius, width, rot_angle, rim_rad=0.5, off=(0,0,0)):
    t = np.linspace(0, 2*np.pi, 20) - rot_angle # Negative links rotation forward relative to right-hand view
    for y_off in [-width/2, width/2]:
        ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + y_off), cz + radius*np.sin(t)
        append_segmented(lines_dict, 'C_WHEEL', list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]], off)
        ix_rim, iy_rim, iz_rim = cx + (radius*rim_rad)*np.cos(t), np.full_like(t, cy + y_off*1.05), cz + (radius*rim_rad)*np.sin(t)
        append_segmented(lines_dict, 'C_CHROME', list(ix_rim)+[ix_rim[0]], list(iy_rim)+[iy_rim[0]], list(iz_rim)+[iz_rim[0]], off)
    
    # Machine 5-Spoke Mag geometry linked to rotational spin
    for a in t[::4]:
        append_segmented(lines_dict, 'C_CHROME', [cx, cx+radius*0.5*np.cos(a)], [cy+width/2.1]*2, [cz, cz+radius*0.5*np.sin(a)], off)
        append_segmented(lines_dict, 'C_CHROME', [cx, cx+radius*0.5*np.cos(a)], [cy-width/2.1]*2, [cz, cz+radius*0.5*np.sin(a)], off)
        append_segmented(lines_dict, 'C_WHEEL', [cx+radius*np.cos(a)]*2, [cy-width/2, cy+width/2], [cz+radius*np.sin(a)]*2, off)

# ------------------------------------------------------------------
# STATIC SUPERSTRUCTURE BUILDERS
# ------------------------------------------------------------------
def generate_ambulance_static():
    lines = {
        'C_BODY': [], 'C_STRIPE': [], 'C_WHEEL': [], 'C_CHROME': [], 
        'C_GLASS': [], 'C_LIGHTS_B': [], 'C_LIGHTS_R': [], 'C_GRID': []
    }

    # 1. BASEPLATE ENVELOPE (REFERENCE GRID)
    gx_range = np.linspace(-6, 6, 25)
    gy_range = np.linspace(-3, 3, 13)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gx_range, gx), np.clip(gx_range, -3, 3), np.zeros_like(gx_range))
    for gy in gy_range: append_segmented(lines, 'C_GRID', np.clip(gx_range, -6, 6), np.full_like(gx_range, gy), np.zeros_like(gx_range))

    # 2. PATIENT CARGO COMPARTMENT (BOX)
    box_w = 1.1
    # Profile traces flat sides but wraps cleanly around the explicit wheel arch cutout
    box_prof = [
        (0.4, 0.7), (-1.4, 0.7), (-1.6, 1.1), (-2.4, 1.1), (-2.6, 0.7),
        (-3.6, 0.7), (-3.6, 2.8), (0.4, 2.8)
    ]
    extrude_profile(lines, 'C_BODY', box_prof, -box_w, box_w)
    
    # Roof details: Extruded AC/vent block
    add_box(lines, 'C_BODY', -1.5, 0.0, 2.95, 2.4, 1.2, 0.3)

    # 3. COMMERCIAL CAB CHASSIS 
    cab_w = 0.95
    cab_prof = [
        (0.4, 0.7), (1.4, 0.7), (1.6, 1.1), (2.4, 1.1), (2.6, 0.7),
        (2.9, 0.7), (2.9, 1.25), (2.2, 1.5), (1.35, 2.25), (0.4, 2.25)
    ]
    extrude_profile(lines, 'C_BODY', cab_prof, -cab_w, cab_w)
    
    # Explicit Grille Matrix
    for gy in np.linspace(-0.8, 0.8, 6):
        append_segmented(lines, 'C_CHROME', [2.9, 2.9], [gy, gy], [0.8, 1.2])

    # 4. KINEMATIC RED STRIPING (HIGH-VIS LOGISTICS)
    for sy in [-box_w, box_w]:
        # Box Section
        append_segmented(lines, 'C_STRIPE', [-3.6, 0.4], [sy, sy], [1.45, 1.45])
        append_segmented(lines, 'C_STRIPE', [-3.6, 0.4], [sy, sy], [1.85, 1.85])
        append_segmented(lines, 'C_STRIPE', [-3.6, -3.6], [sy, sy], [1.45, 1.85])
        append_segmented(lines, 'C_STRIPE', [0.4, 0.4], [sy, sy], [1.45, 1.85])
    # Connect back doors
    append_segmented(lines, 'C_STRIPE', [-3.6]*2, [-box_w, box_w], [1.45, 1.45])
    append_segmented(lines, 'C_STRIPE', [-3.6]*2, [-box_w, box_w], [1.85, 1.85])

    for sy in [-cab_w, cab_w]:
        # Cab Section (Angling dynamically upon intercepting the sloped hood geometry)
        append_segmented(lines, 'C_STRIPE', [0.4, 2.1], [sy, sy], [1.45, 1.45])
        append_segmented(lines, 'C_STRIPE', [0.4, 1.7], [sy, sy], [1.85, 1.85])
        append_segmented(lines, 'C_STRIPE', [2.1, 1.7], [sy, sy], [1.45, 1.85]) # Sloped leading edge flush with hood drop

    # 5. DYNAMIC GLASS (WINDOWS)
    # Angled windshield 
    append_segmented(lines, 'C_GLASS', [2.15, 2.15, 1.4, 1.4, 2.15], [-0.9, 0.9, 0.9, -0.9, -0.9], [1.5, 1.5, 2.2, 2.2, 1.5])
    # Cab door windows
    for y in [-cab_w*1.01, cab_w*1.01]:
        append_segmented(lines, 'C_GLASS', [1.3, 0.6, 0.6, 1.95, 1.3], [y]*5, [2.15, 2.15, 1.5, 1.5, 2.15])
    # Box side sliding windows
    for y in [-box_w*1.01, box_w*1.01]:
        append_segmented(lines, 'C_GLASS', [-2.4, -0.8, -0.8, -2.4, -2.4], [y]*5, [2.1, 2.1, 2.6, 2.6, 2.1])
        append_segmented(lines, 'C_GLASS', [-1.6, -1.6], [y, y], [2.1, 2.6]) # Middle sliding rail
    # Rear compartment doors (Dual panels)
    append_segmented(lines, 'C_GLASS', [-3.61]*5, [-0.95, -0.1, -0.1, -0.95, -0.95], [2.0, 2.0, 2.6, 2.6, 2.0])
    append_segmented(lines, 'C_GLASS', [-3.61]*5, [0.1, 0.95, 0.95, 0.1, 0.1], [2.0, 2.0, 2.6, 2.6, 2.0])

    # 6. EXTERNAL MACHINED FENDER FLARES
    r_flare = [(-1.4, 0.7), (-1.6, 1.1), (-2.4, 1.1), (-2.6, 0.7)]
    extrude_profile(lines, 'C_BODY', r_flare, box_w, box_w+0.15, close_loop=False)     # Right Rear
    extrude_profile(lines, 'C_BODY', r_flare, -box_w-0.15, -box_w, close_loop=False)   # Left Rear

    f_flare = [(1.4, 0.7), (1.6, 1.1), (2.4, 1.1), (2.6, 0.7)]
    extrude_profile(lines, 'C_BODY', f_flare, cab_w, cab_w+0.15, close_loop=False)     # Right Front
    extrude_profile(lines, 'C_BODY', f_flare, -cab_w-0.15, -cab_w, close_loop=False)   # Left Front

    # 7. HIGH-VIS EMERGENCY LIGHTING ARCHITECTURE (STROBES & BEACONS)
    add_box(lines, 'C_LIGHTS_B', 0.25, 0.0, 2.9, 0.3, 1.8, 0.2)  # Box Front Main Blue
    add_box(lines, 'C_LIGHTS_R', -3.45, 0.0, 2.9, 0.3, 1.8, 0.2) # Box Rear Main Red
    add_box(lines, 'C_LIGHTS_B', 0.8, 0.0, 2.35, 0.2, 0.8, 0.2)  # Cab Roof Mini-Strobe
    
    # Forward warning flares
    for y in [-0.8, 0.8]:
        add_box(lines, 'C_LIGHTS_R', 2.85, y, 1.35, 0.15, 0.2, 0.15)
        add_box(lines, 'C_CHROME', 2.91, y, 0.95, 0.1, 0.25, 0.15) # Headlight

    # 8. HARDPOINT BUMPERS & CHASSIS RAILS
    add_box(lines, 'C_CHROME', 3.0, 0.0, 0.6, 0.2, 2.0, 0.2)    # Front Bash Bar
    add_box(lines, 'C_CHROME', -3.75, 0.0, 0.55, 0.3, 2.2, 0.25) # Massive Rear Entry Step
    # Exposed suspension/chassis rail bounding
    append_segmented(lines, 'C_CHROME', [-3.6, 2.8], [-0.5, -0.5], [0.55, 0.55])
    append_segmented(lines, 'C_CHROME', [-3.6, 2.8], [0.5, 0.5], [0.55, 0.55])

    return lines


def generate_dynamic_wheels(lines, rot_angle):
    # Front Axles (Single wide setup)
    for sign in [-1, 1]: 
        add_rotating_wheel(lines, 2.0, 0.9*sign, 0.45, 0.45, 0.3, rot_angle)
    # Rear Axles (Dually dense simulation)
    for sign in [-1, 1]:
        add_rotating_wheel(lines, -2.0, 1.05*sign, 0.45, 0.45, 0.4, rot_angle)

# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_ambulance_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        cam_x, cam_y, cam_z = -0.5, 0.0, 1.5 
        
        # 360-degree perfect orbital synchronisation (Starts exactly from Right Side +Y)
        azimuth = 90.0 - (stage * 360.0)

        # Operational Drive Velocity (12 full rotations driving +X)
        rot_angle = stage * 12.0 * 2.0 * np.pi

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

    cam_span = 5.2
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID', C_GRID, 0.8, 0.4), ('C_WHEEL', C_WHEEL, 1.4, 1.0),
        ('C_CHROME', C_CHROME, 1.4, 1.0), ('C_BODY', C_BODY, 1.6, 1.0),
        ('C_GLASS', C_GLASS, 1.4, 1.0), ('C_STRIPE', C_STRIPE, 2.5, 1.0), 
        ('C_LIGHTS_B', C_LIGHTS_B, 2.2, 1.0), ('C_LIGHTS_R', C_LIGHTS_R, 2.2, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in local_rig[c_key]:
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=16.0)
            render_queue.append((np.mean(depth), u, v-0.6, c_val, lw, alpha))

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

    ax.text(-cam_span*0.95, ui_t+1.5, "LG-449z // MACRO-ENGINEERING TENSOR: EMERGENCY MEDICAL KINEMATICS", color=C_TEXT, fontsize=17, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t+0.5, "EXPLICIT TRUE-SCALE GEOMETRY // TYPE III AMBULANCE MATRIX", color=C_BODY, fontsize=13, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b+2.2, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_STRIPE, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+1.1, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.2, "WHEEL VELOCITY   : FORWARD ORBITAL SYNCHRONISATION LOCKED", color=C_LIGHTS_B, fontsize=13, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-449z: AMBULANCE KINEMATICS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Automotive Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
