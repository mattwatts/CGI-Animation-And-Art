"""
PROJECT: Logic Garden 450d (Exact Physical Construct // SAR K-class 0-6-4T Steam Locomotive Matrix - HOTFIX)
FORMAT: YouTube Shorts (1080x1920)
METADATA: TRAIN, LOCOMOTIVE, STEAM, K-CLASS, WIREFRAME, ENGINEERING, KINEMATICS, RAILWAY
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: True 3-axis drive wheels, reciprocating coupling rods, side tank geometry, and massive boiler parameterisation.
- Hotfix: Registered 'C_BG' in master layer_map to correctly process spectacle plate rendering.
- Forward Alignment: Rig operates flawlessly travelling into +X. Wheels/Rods rotate and cycle.
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
OUT_DIR = "frames_450d_train"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Baseplate Track Reference)
C_WHEEL     = '#111115'          # Indestructible Black (Cast Iron Wheel Rims & Flanges)

C_FRAME     = '#1E293B'          # Carbon Slate (Heavy Underframe & Coal Bunker)
C_BOILER    = '#475569'          # Machined Cast Iron (Pressure Vessel & Smokebox)
C_CAB       = '#94A3B8'          # Polished Steel (Side Tanks, Cab Shell)
C_BRASS     = '#D95F22'          # Industrial Amber (Steam Dome, Chimney Lip, Whistle)
C_ROD       = '#E11D48'          # Kinematic Red (Reciprocating Drive Rods & Crossheads)

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
    hx, hy, hz = dx/2.0, dy/2.0, dz/2.0
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
# KINEMATIC STEAM WHEELS & RODS
# ------------------------------------------------------------------
def add_train_wheel(lines_dict, cx, cy, cz, radius, rot_angle, is_drive=True, off=(0,0,0)):
    # Simulates continuous forward +X momentum geometrically mapped to Z=0 substrate
    t = np.linspace(0, 2*np.pi, 24) - rot_angle
    
    # Outer Rolling Rim
    ix_rim = cx + radius * np.cos(t)
    iz_rim = cz + radius * np.sin(t)
    append_segmented(lines_dict, 'C_WHEEL', list(ix_rim)+[ix_rim[0]], [cy]*25, list(iz_rim)+[iz_rim[0]], off)
    
    # Deep Flange (Inside lip guiding on rail)
    flange_radius = radius * 1.08
    ix_flange = cx + flange_radius * np.cos(t)
    iz_flange = cz + flange_radius * np.sin(t)
    cy_flange = cy - 0.1 * np.sign(cy) # Moves flange slightly inwards
    append_segmented(lines_dict, 'C_WHEEL', list(ix_flange)+[ix_flange[0]], [cy_flange]*25, list(iz_flange)+[iz_flange[0]], off)

    # Internal Cast Spokes
    spokes = 16 if is_drive else 10
    spoke_angles = np.linspace(0, 2*np.pi, spokes, endpoint=False) - rot_angle
    for sa in spoke_angles:
        px = cx + radius * 0.95 * np.cos(sa)
        pz = cz + radius * 0.95 * np.sin(sa)
        append_segmented(lines_dict, 'C_WHEEL', [cx, px], [cy, cy], [cz, pz], off)

    if is_drive:
        # Counterweight Arc (Massive iron block opposite the crank pin)
        cw_start = np.pi - 0.7 - rot_angle
        cw_end = np.pi + 0.7 - rot_angle
        cw_t = np.linspace(cw_start, cw_end, 8)
        cw_x = cx + radius * 0.85 * np.cos(cw_t)
        cw_z = cz + radius * 0.85 * np.sin(cw_t)
        # Weld counterweight boundary to the hub
        append_segmented(lines_dict, 'C_FRAME', list(cw_x)+[cx, cw_x[0]], [cy]*10, list(cw_z)+[cz, cw_z[0]], off)
        
        # Exact Crank Pin Location Return
        crank_r = radius * 0.45
        cp_x = cx + crank_r * np.cos(-rot_angle)
        cp_z = cz + crank_r * np.sin(-rot_angle)
        
        # Heavy Crank Boss
        append_segmented(lines_dict, 'C_WHEEL', [cx, cp_x], [cy, cy], [cz, cp_z], off)
        return cp_x, cp_z
        
    return None, None

# ------------------------------------------------------------------
# STATIC SUPERSTRUCTURE BUILDERS (LOCOMOTIVE)
# ------------------------------------------------------------------
def generate_locomotive_static():
    lines = {
        'C_FRAME': [], 'C_BOILER': [], 'C_CAB': [], 'C_BRASS': [], 
        'C_ROD': [], 'C_WHEEL': [], 'C_GRID': [], 'C_BG': []
    }

    # 1. BASEPLATE ENVELOPE (REFERENCE GRID / TRACKS)
    gx_range = np.linspace(-6.0, 6.0, 25)
    gy_range = np.linspace(-1.5, 1.5, 9)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gx_range, gx), np.clip(gx_range, -1.5, 1.5), np.zeros_like(gx_range))
    for gy in gy_range: append_segmented(lines, 'C_GRID', np.clip(gx_range, -6.0, 6.0), np.full_like(gx_range, gy), np.zeros_like(gx_range))

    # Parallel Railway Rails
    for ry in [-0.75, 0.75]:
        append_segmented(lines, 'C_GRID', [-6.0, 6.0], [ry, ry], [0.0, 0.0])
        append_segmented(lines, 'C_GRID', [-6.0, 6.0], [ry, ry], [0.05, 0.05])

    # 2. HEAVY CHASSIS BEDPLATE & BUMPERS
    # Spanning exclusively from nose to tail
    add_box(lines, 'C_FRAME', -0.1, 0.0, 1.0, 10.4, 2.4, 0.3)
    # Forward Pilot Beam
    add_box(lines, 'C_FRAME', 5.15, 0.0, 1.0, 0.3, 2.6, 0.4)
    # Rear Buffer Beam
    add_box(lines, 'C_FRAME', -5.4, 0.0, 1.0, 0.2, 2.6, 0.4)

    # 3. HIGH-PRESSURE BOILER & SMOKEBOX
    boiler_z = 1.95
    # Main continuous boiler barrel
    add_cylinder(lines, 'C_BOILER', cx=-1.5, cy=0.0, cz=boiler_z, length=5.5, radius=0.75, axis='x', rings=8)
    
    # Smokebox (Extended outer wrapper plate at front)
    add_cylinder(lines, 'C_BOILER', cx=4.0, cy=0.0, cz=boiler_z, length=0.9, radius=0.78, axis='x', rings=3)
    # Smokebox Door (Forward domed cap geometry)
    t = np.linspace(0, 2*np.pi, 24)
    append_segmented(lines, 'C_BOILER', np.full_like(t, 4.9), 0.7*np.cos(t), boiler_z + 0.7*np.sin(t))
    append_segmented(lines, 'C_BRASS', np.full_like(t, 5.0), 0.2*np.cos(t), boiler_z + 0.2*np.sin(t))
    for a in t[::3]:
        append_segmented(lines, 'C_BOILER', [4.9, 5.0], [0.7*np.cos(a), 0.2*np.cos(a)], [boiler_z+0.7*np.sin(a), boiler_z+0.2*np.sin(a)])

    # 4. CHIMNEY & STEAM DOME
    # Tall chimney stack breaching absolute clearance
    add_cylinder(lines, 'C_BRASS', cx=4.4, cy=0.0, cz=2.7, length=0.8, radius=0.22, axis='z', rings=3)
    add_cylinder(lines, 'C_BRASS', cx=4.4, cy=0.0, cz=3.5, length=0.15, radius=0.32, axis='z', rings=2) # Flared Cap
    
    # Majestic Steam Dome heavily bound over drive axle
    add_cylinder(lines, 'C_BRASS', cx=1.8, cy=0.0, cz=2.7, length=0.6, radius=0.35, axis='z', rings=4)
    add_cylinder(lines, 'C_ROD', cx=0.8, cy=0.0, cz=2.7, length=0.3, radius=0.1, axis='z', rings=2) # Safety Valves
    
    # 5. DUAL SIDE TANKS (Water Supply)
    # Mounted straddling the boiler down to the footplate
    t_len = 3.6
    t_dx = t_len/2.0
    for t_sign in [-1, 1]:
        # X: Centred at 0.5. Y: Bound to outer 1.25 edge
        add_box(lines, 'C_CAB', 0.5, 0.95*t_sign, 1.65, t_len, 0.6, 1.0)
        # Visual riveted plate overlaps
        append_segmented(lines, 'C_CAB', [0.5-t_dx, 0.5+t_dx], [1.26*t_sign]*2, [1.4, 1.4])
        append_segmented(lines, 'C_CAB', [0.5-t_dx, 0.5+t_dx], [1.26*t_sign]*2, [1.9, 1.9])

    # 6. ENCLOSED CAB & REAR COAL BUNKER
    # Massive rectangular extrusion protecting the crew
    add_box(lines, 'C_CAB', cx=-2.4, cy=0.0, cz=2.2, dx=2.2, dy=2.6, dz=2.1)
    
    # Sweeping arched Cab Roof
    r_t = np.linspace(-1.4, 1.4, 12)
    r_z = 3.25 + 0.15 * np.cos(r_t * (np.pi/2.8)) # Parametric roof curve
    r_x_front = np.full_like(r_t, -1.2)
    r_x_rear  = np.full_like(r_t, -3.7)
    append_segmented(lines, 'C_CAB', list(r_x_front), list(r_t), list(r_z))
    append_segmented(lines, 'C_CAB', list(r_x_rear), list(r_t), list(r_z))
    for i in range(12):
        append_segmented(lines, 'C_CAB', [-1.2, -3.7], [r_t[i]]*2, [r_z[i]]*2)

    # Cab Windows (Circular Spectacle Plates mapped to front sheet)
    w_t = np.linspace(0, 2*np.pi, 16)
    for w_y in [-0.7, 0.7]:
        append_segmented(lines, 'C_BG', list(-1.29 + 0.0*w_t), list(w_y + 0.3*np.cos(w_t)), list(2.7 + 0.3*np.sin(w_t)))
        append_segmented(lines, 'C_CAB', list(-1.31 + 0.0*w_t), list(w_y + 0.3*np.cos(w_t)), list(2.7 + 0.3*np.sin(w_t)))

    # Coal Bunker behind the Cab
    add_box(lines, 'C_FRAME', cx=-4.4, cy=0.0, cz=1.65, dx=1.8, dy=2.3, dz=1.0)
    
    # 7. FORWARD STEAM CYLINDERS (The prime movers)
    for cy_sign in [-1, 1]:
        # Piston casings directly intersecting the mechanical rod path
        add_cylinder(lines, 'C_FRAME', cx=4.2, cy=0.9*cy_sign, cz=0.75, length=0.9, radius=0.28, axis='x', rings=3)

    return lines


def generate_kinematic_motion(lines, rot_angle):
    # Operating specifically on Wide Track constraints
    track_y = 0.85
    r_drive = 0.75
    r_trail = 0.45
    
    # Drive Axle Placements
    x_w1 = 3.2
    x_w2 = 1.6
    x_w3 = 0.0

    # The trailing bogies rotate proportionally faster perfectly preventing slip
    trail_rot = rot_angle * (r_drive / r_trail)

    for sign in [-1, 1]:
        cy = track_y * sign
        
        # 0-6-0 Primary Drive Phase
        cp1x, cp1z = add_train_wheel(lines, x_w1, cy, r_drive, r_drive, rot_angle, is_drive=True)
        cp2x, cp2z = add_train_wheel(lines, x_w2, cy, r_drive, r_drive, rot_angle, is_drive=True)
        cp3x, cp3z = add_train_wheel(lines, x_w3, cy, r_drive, r_drive, rot_angle, is_drive=True)
        
        # -4-0 Trailing Bogie Phase
        add_train_wheel(lines, -2.0, cy, r_trail, r_trail, trail_rot, is_drive=False)
        add_train_wheel(lines, -3.8, cy, r_trail, r_trail, trail_rot, is_drive=False)

        # -------------------------------------------------------------
        # EXPLICIT RECIPROCATING ROD KINEMATICS (The Mechanical Matrix)
        # -------------------------------------------------------------
        # 1. Main Coupling Rod (Bridging the three drives uniformly)
        rod_y = cy + 0.15 * sign
        # Solid core link
        append_segmented(lines, 'C_ROD', [cp1x, cp2x, cp3x], [rod_y]*3, [cp1z, cp2z, cp3z])
        # Volumetric vertical thickening
        append_segmented(lines, 'C_ROD', [cp1x, cp2x, cp3x], [rod_y]*3, [cp1z+0.05, cp2z+0.05, cp3z+0.05])
        append_segmented(lines, 'C_ROD', [cp1x, cp2x, cp3x], [rod_y]*3, [cp1z-0.05, cp2z-0.05, cp3z-0.05])
        
        # 2. Main Piston Push Rod
        # Translates purely horizontal motion strictly bound into the steam cylinders
        piston_x = 4.2 + 0.3 * np.cos(-rot_angle) # Crosshead oscillates explicitly against crank phase
        piston_z = 0.75
        
        append_segmented(lines, 'C_ROD', [cp1x, piston_x], [rod_y+0.05*sign]*2, [cp1z, piston_z])
        # The Crosshead slider tracking linearly into the cylinder
        add_box(lines, 'C_ROD', piston_x, cy+0.1*sign, piston_z, 0.4, 0.15, 0.2)
        append_segmented(lines, 'C_BRASS', [piston_x, 4.8], [cy]*2, [piston_z]*2) # Actual rod breaching cylinder head


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_locomotive_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        cam_x, cam_y, cam_z = -0.5, 0.0, 1.8 
        
        # 360-degree perfect orbital synchronisation (Starts Side Profile mapping completely)
        azimuth = 90.0 - (stage * 360.0)

        # Operational Drive Velocity (12 full wheel rotations driving +X seamlessly)
        rot_angle = stage * 12.0 * 2.0 * np.pi

        yield (f, t_sec, azimuth, rot_angle, cam_x, cam_y, cam_z, static_rig)

def render_frame(packet):
    f, t_sec, azimuth, rot_angle, cx, cy, cz, static_rig = packet

    local_rig = {k: v.copy() for k,v in static_rig.items()}
    generate_kinematic_motion(local_rig, rot_angle)

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    cam_span = 6.2
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_BG',     C_BG,     1.2, 1.0), # Added to support Spectacle Plate cutouts
        ('C_GRID',   C_GRID,   0.8, 0.4), 
        ('C_WHEEL',  C_WHEEL,  1.4, 1.0),
        ('C_ROD',    C_ROD,    1.8, 1.0), 
        ('C_FRAME',  C_FRAME,  1.4, 1.0),
        ('C_BOILER', C_BOILER, 1.2, 1.0), 
        ('C_CAB',    C_CAB,    1.2, 1.0), 
        ('C_BRASS',  C_BRASS,  1.5, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in local_rig[c_key]:
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=10.0)
            render_queue.append((np.mean(depth), u, v-0.5, c_val, lw, alpha))

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

    ax.text(-cam_span*0.95, ui_t+1.5, "LG-450d // MACRO-ENGINEERING TENSOR: LOCOMOTIVE KINEMATICS", color=C_TEXT, fontsize=17, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t+0.5, "EXPLICIT TRUE-SCALE GEOMETRY // SAR K-CLASS (0-6-4T) MATRIX", color=C_ROD, fontsize=13, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b+0.85, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_CAB, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.45, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.05, "KINEMATIC YIELD  : RECIPROCATING RODS & DRIVE COUPLING SECURED", color=C_BRASS, fontsize=13, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-450d: LOCOMOTIVE KINEMATICS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Mechanical Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
