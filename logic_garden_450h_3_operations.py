"""
PROJECT: Logic Garden 450h (Exact Physical Construct // Starship Flight Operations Matrix - REVISION 3)
FORMAT: YouTube Shorts (1080x1920)
METADATA: SPACEX, STARSHIP, SUPER HEAVY, FLIGHT OPERATIONS, WIREFRAME, ENGINEERING, KINEMATICS
EXECUTION: 36.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: True parametric 50m Ship, 71m Super Heavy Booster, 39 total engines.
- True Kinematics: Hot-staging, independent booster RTLS X-translation, ship belly-flop, distinct vertical landing. 
- Strict Bounds Protocol: NO FORCED LOOPING. Dynamic camera strictly tracks the full-stack mid-point, then irreversibly locks to the Ship post-separation for intimate framing.
- Timeline: Realistic, asymmetrical 36.0s operational trajectory.
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
DURATION = 36.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_450h_operations"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Baseplate Reference & Landing Zones)
C_ENGINE    = '#111115'          # Indestructible Black (Raptor Thrust Bells)

C_HULL      = '#1E293B'          # Carbon Slate (Primary Stainless Steel Skin)
C_AERO      = '#475569'          # Machined Slate (Flaps, Grid Fins & Control Surfaces)
C_TANK      = '#005599'          # Deep Marine (Internal Pressure Domes)
C_FIRE      = '#D95F22'          # Industrial Amber (Booster Plume / Hot-Staging Rings)
C_THRUSTER  = '#00D2FF'          # High Blue (Vacuum / Ship Thrust Vectors)
C_PLASMA    = '#DE008A'          # Intense Magenta (Atmospheric Re-entry Spallation)

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

# ------------------------------------------------------------------
# GEOMETRIC PRIMITIVES
# ------------------------------------------------------------------
def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, rings=8, t_count=24):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, length, rings)
    for s in steps:
        ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + s), cz + radius*np.sin(t)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iz)+[iz[0]], list(iy)+[iy[0]])
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        sx, sy, sz = cx + radius*np.cos(a), cy + steps, cz + radius*np.sin(a)
        append_segmented(lines_dict, col, [sx]*rings, [sz]*rings, list(sy))

def add_ogive(lines_dict, col, cx, cy, z_start, z_end, r_base, rings=12, t_count=24):
    z_steps = np.linspace(z_start, z_end, rings)
    ratio = (z_steps - z_start) / (z_end - z_start)
    r_steps = r_base * np.sqrt(np.clip(1.0 - (ratio)**2.2, 0.001, 1.0)) 
    for i in range(len(z_steps)):
        r, z = r_steps[i], z_steps[i]
        t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
        append_segmented(lines_dict, col, list(cx + r*np.cos(t))+[cx + r*np.cos(0)], list(cy + r*np.sin(t))+[cy + r*np.sin(0)], [z]*(t_count+1))
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        append_segmented(lines_dict, col, list(cx + r_steps*np.cos(a)), list(cy + r_steps*np.sin(a)), list(z_steps))

def add_thrust_bell(lines_dict, col, cx, cy, cz, h, r_top, r_bot):
    steps = 4
    z_steps = np.linspace(cz, cz-h, steps)
    ratio = (cz - z_steps) / h
    r_steps = r_top + (r_bot - r_top) * (ratio**1.5)
    for i in range(steps):
        r, z = r_steps[i], z_steps[i]
        t = np.linspace(0, 2*np.pi, 8, endpoint=False)
        append_segmented(lines_dict, col, list(cx + r*np.cos(t))+[cx + r*np.cos(0)], list(cy + r*np.sin(t))+[cy + r*np.sin(0)], [z]*9)
    for a in np.linspace(0, 2*np.pi, 8, endpoint=False):
        append_segmented(lines_dict, col, list(cx + r_steps*np.cos(a)), list(cy + r_steps*np.sin(a)), list(z_steps))

# ------------------------------------------------------------------
# STATIC RIG GENERATORS (SHIP & BOOSTER DOCKED AT Z=0 LOCALLY)
# ------------------------------------------------------------------
def generate_ship_static():
    lines = {'C_HULL': [], 'C_AERO': [], 'C_TANK': [], 'C_ENGINE': [], 'C_FIRE': []}
    R_HULL = 4.5; H_HULL = 36.28; H_TOTAL = 50.0

    add_cylinder(lines, 'C_HULL', 0, 0, 0, H_HULL, R_HULL, rings=20, t_count=30)
    add_ogive(lines, 'C_HULL', 0, 0, H_HULL, H_TOTAL, R_HULL, rings=14, t_count=30)

    for sign in [-1, 1]:
        z_af_bot = 1.0; z_af_top = 16.14; y_af_out = (R_HULL + 4.2) * sign
        append_segmented(lines, 'C_AERO', [-0.5]*4, [y_af_out, R_HULL*sign, R_HULL*sign, y_af_out, y_af_out], [z_af_bot+1.0, z_af_bot, z_af_top, z_af_top-4.0, z_af_bot+1.0])
        z_ff_bot = 37.0; z_ff_top = 45.0
        r_bot = R_HULL * np.sqrt(max(0.001, 1 - ((z_ff_bot - 36.28)/13.72)**2.2))
        r_top = R_HULL * np.sqrt(max(0.001, 1 - ((z_ff_top - 36.28)/13.72)**2.2))
        y_ff_out = (R_HULL + 3.0) * sign
        append_segmented(lines, 'C_AERO', [-0.3]*4, [y_ff_out, r_bot*sign, r_top*sign, y_ff_out, y_ff_out], [z_ff_bot+1.0, z_ff_bot, z_ff_top, z_ff_top-2.0, z_ff_bot+1.0])

    for a in [0, 120, 240]:
        rad = np.radians(a); add_thrust_bell(lines, 'C_ENGINE', 1.0*np.cos(rad), 1.0*np.sin(rad), 0.0, 1.5, 0.3, 0.65)
    for a in [60, 180, 300]:
        rad = np.radians(a); add_thrust_bell(lines, 'C_ENGINE', 2.8*np.cos(rad), 2.8*np.sin(rad), -0.5, 2.5, 0.5, 1.1)

    return lines

def generate_booster_static():
    lines = {'C_HULL': [], 'C_AERO': [], 'C_ENGINE': [], 'C_FIRE': []}
    R_HULL = 4.5; H_BOOST = 71.0

    add_cylinder(lines, 'C_HULL', 0, 0, 0, H_BOOST, R_HULL, rings=30, t_count=30)
    for z_hs in np.linspace(69.0, 71.0, 4):
        t = np.linspace(0, 2*np.pi, 30)
        append_segmented(lines, 'C_FIRE', R_HULL*np.cos(t), R_HULL*np.sin(t), [z_hs]*len(t))

    add_thrust_bell(lines, 'C_ENGINE', 0, 0, 0.0, 1.5, 0.3, 0.6)
    for a in np.linspace(0, 360, 10, endpoint=False): 
        add_thrust_bell(lines, 'C_ENGINE', 1.8*np.cos(np.radians(a)), 1.8*np.sin(np.radians(a)), 0.0, 1.5, 0.3, 0.6)
    for a in np.linspace(0, 360, 23, endpoint=False): 
        add_thrust_bell(lines, 'C_ENGINE', 3.8*np.cos(np.radians(a)), 3.8*np.sin(np.radians(a)), 0.0, 1.5, 0.3, 0.6)

    for a in [45, 135, 225, 315]:
        rad = np.radians(a)
        cx, cy = (R_HULL+1.5)*np.cos(rad), (R_HULL+1.5)*np.sin(rad)
        v_u = np.array([-np.sin(rad), np.cos(rad)]) * 1.5
        append_segmented(lines, 'C_AERO', [cx-v_u[0], cx+v_u[0], cx+v_u[0], cx-v_u[0], cx-v_u[0]], 
                                          [cy-v_u[1], cy+v_u[1], cy+v_u[1], cy-v_u[1], cy-v_u[1]], 
                                          [67.0, 67.0, 69.5, 69.5, 67.0])
    return lines

# ------------------------------------------------------------------
# KINEMATIC TRANSFORMS & INTERPOLATION
# ------------------------------------------------------------------
def key_interp(t, keyframes):
    if t <= keyframes[0][0]: return keyframes[0][1]
    if t >= keyframes[-1][0]: return keyframes[-1][1]
    for i in range(len(keyframes)-1):
        t1, v1 = keyframes[i]
        t2, v2 = keyframes[i+1]
        if t1 <= t <= t2:
            ratio = (t - t1) / (t2 - t1)
            st = ratio * ratio * (3.0 - 2.0 * ratio) # Smoothstep ballistic blending
            return v1 + (v2 - v1) * st
    return 0.0

def transform_and_merge(master_list, rig_dict, dx, dy, dz, pitch_deg, z_pivot):
    p_rad = np.radians(pitch_deg)
    cos_p, sin_p = np.cos(p_rad), np.sin(p_rad)
    for col, lines_list in rig_dict.items():
        if col not in master_list: master_list[col] = []
        for xs, ys, zs in lines_list:
            xs, ys, zs = np.array(xs), np.array(ys), np.array(zs)
            z_rel = zs - z_pivot
            y_new = ys * cos_p - z_rel * sin_p
            z_new = ys * sin_p + z_rel * cos_p + z_pivot
            master_list[col].append((list(xs + dx), list(y_new + dy), list(z_new + dz)))

# ------------------------------------------------------------------
# PROCEDURAL KINEMATIC VECTORS (Engines & Re-entry Plasma)
# ------------------------------------------------------------------
def generate_dynamics(out_dict, sh_plume, bo_plume, plasma):
    if sh_plume > 0:
        lines = []
        for _ in range(int(sh_plume*8)):
            x, y = np.random.uniform(-2.5, 2.5, 2)
            if (x*x + y*y) < 6.25: lines.append(([x, x], [y, y], [0, -np.random.uniform(0, sh_plume)]))
        out_dict['sh_plume'] = lines
    
    if bo_plume > 0:
        lines = []
        for _ in range(int(bo_plume*12)):
            x, y = np.random.uniform(-4.5, 4.5, 2)
            if (x*x + y*y) < 20.25: lines.append(([x, x], [y, y], [0, -np.random.uniform(0, bo_plume)]))
        out_dict['bo_plume'] = lines

    if plasma > 0:
        lines = []
        for _ in range(int(plasma*40)):
            cz = np.random.uniform(5, 45)
            rad = 4.5 if cz <= 36.28 else 4.5 * np.sqrt(max(0.001, 1.0 - ((cz-36.28)/13.72)**2.2))
            cx = np.random.uniform(-rad, rad)
            y0 = -np.sqrt(max(0.001, rad*rad - cx*cx)) # Exact bottom surface intercept (-Y Belly)
            dy = np.random.uniform(1.0, 4.0) * plasma
            lines.append(([cx, cx], [y0, y0 - dy], [cz, cz]))
        out_dict['ship_plasma'] = lines

# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    ship_rig = generate_ship_static()
    boos_rig = generate_booster_static()

    # Cinematic Timeline Arrays [Time(s), Value]
    # Ship perfectly coupled T=0_6s, then accelerates to orbit, re-enters and lands vertically.
    sh_z_keys     = [(0, 71), (6, 400), (16, 2000), (22, 1800), (32, 200), (36, 0)]
    sh_p_keys     = [(0, 0), (16, 0), (18, -90), (30, -90), (33, 0), (36, 0)]
    sh_pl_keys    = [(0, 0), (5.8, 0), (6.2, 20), (15, 20), (16, 0), (32, 0), (32.5, 25), (35.8, 25), (36, 0)]
    sh_plas_keys  = [(0, 0), (20, 0), (22, 1.0), (28, 1.0), (30, 0), (36, 0)]

    # Booster perfectly coupled T=0_6s, boostback, drops aggressively away on the X axis, lands far out of frame.
    bo_z_keys     = [(0, 0), (6, 329), (9, 400), (18, 0), (36, 0)]
    bo_p_keys     = [(0, 0), (7, 0), (9, -110), (12, -110), (15, 0), (36, 0)]
    bo_x_keys     = [(0, 0), (8, 0), (18, -400), (36, -400)] # RTLS Vector explicitly pulling it off-site
    bo_pl_keys    = [(0, 25), (6, 25), (6.1, 0), (9, 0), (9.5, 20), (12.5, 20), (13, 0), (16, 0), (16.5, 20), (17.8, 20), (18, 0), (36, 0)]

    for f in range(TOTAL_FRAMES):
        t = f / float(FPS)
        # Slow sweeping orbit tracking the physical progression
        azimuth = 90.0 - (t / DURATION * 360.0)
        
        s_z = key_interp(t, sh_z_keys)
        s_p = key_interp(t, sh_p_keys)
        s_pl = key_interp(t, sh_pl_keys)
        s_plas = key_interp(t, sh_plas_keys)
        
        b_z = key_interp(t, bo_z_keys)
        b_p = key_interp(t, bo_p_keys)
        b_x = key_interp(t, bo_x_keys)
        b_pl = key_interp(t, bo_pl_keys)
        
        # CAMERA TARGETING LOGIC
        # 1. Start by viewing the entire 121m Full Stack perfectly.
        # 2. At separation (T=6), gracefully interpolate camera focus securely onto ONLY the 50m Ship.
        cz_ship = s_z + 25.0                               # Center of the Ship
        cz_stack = (s_z + 50.0 + b_z) / 2.0                # Center of the entire vertical stack
        
        if t <= 6.0:
            cz_cam = cz_stack
            cspan = 45.0
        elif t <= 9.0:
            ratio = (t - 6.0) / 3.0
            st = ratio * ratio * (3.0 - 2.0 * ratio)
            cz_cam = cz_stack * (1.0 - st) + cz_ship * st
            cspan = 45.0 * (1.0 - st) + 26.0 * st          # Squeezing the boundaries beautifully around the 50m ship
        else:
            cz_cam = cz_ship
            cspan = 26.0

        label = "VERTICAL LANDING & ENGINE CUTOFF"
        if t < 6.0: label = "FULL STACK LIFT ENGINE BURN"
        elif t < 10.0: label = "HOT-STAGED SEPARATION SEQUENCE"
        elif t < 16.0: label = "SHIP ORBITAL INSERTION (BOOSTER RTLS)"
        elif t < 30.0: label = "AERODYNAMIC BELLY FLOP RE-ENTRY"
        elif t < 33.5: label = "TERMINAL FLIP MANOEUVRE"

        yield (f, t, azimuth, s_z, s_p, s_pl, s_plas, b_z, b_p, b_x, b_pl, cz_cam, cspan, label, ship_rig, boos_rig)

def render_frame(packet):
    f, t, azimuth, s_z, s_p, s_pl, s_plas, b_z, b_p, b_x, b_pl, cz_cam, cspan, label, ship_rig, boos_rig = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    ax.set_xlim(-cspan, cspan)
    ax.set_ylim(-cspan * 1.777, cspan * 1.777)

    master_scene = {'C_GRID': []}
    gx = np.linspace(-15, 15, 12)
    for x in gx: append_segmented(master_scene, 'C_GRID', np.full_like(gx, x), gx, np.zeros_like(gx))
    for y in gx: append_segmented(master_scene, 'C_GRID', gx, np.full_like(gx, y), np.zeros_like(gx))
    
    # Render Booster Landing Zone safely out of frame computationally
    if t > 6.0:
        bx_g = np.linspace(-415, -385, 12)
        for x in bx_g: append_segmented(master_scene, 'C_GRID', np.full_like(bx_g, x), bx_g + 400.0, np.zeros_like(bx_g))
        for y in bx_g: append_segmented(master_scene, 'C_GRID', bx_g, np.full_like(bx_g, y) + 400.0, np.zeros_like(bx_g))

    dyn_lines = {}
    generate_dynamics(dyn_lines, s_pl, b_pl, s_plas)
    
    local_s = {k: v.copy() for k,v in ship_rig.items()}
    local_b = {k: v.copy() for k,v in boos_rig.items()}
    if 'sh_plume' in dyn_lines: local_s['C_THRUSTER'] = dyn_lines['sh_plume']
    if 'ship_plasma' in dyn_lines: local_s['C_PLASMA'] = dyn_lines['ship_plasma']
    if 'bo_plume' in dyn_lines: local_b['C_FIRE'] = dyn_lines['bo_plume']

    # Z-Pivots map the exact geometric Centre of Mass for physical rotations. Booster inherently translates away via dx=b_x
    transform_and_merge(master_scene, local_b, dx=b_x, dy=0.0, dz=b_z, pitch_deg=b_p, z_pivot=35.0)
    transform_and_merge(master_scene, local_s, dx=0.0, dy=0.0, dz=s_z, pitch_deg=s_p, z_pivot=25.0)

    render_queue = []
    layer_config = {
        'C_GRID': (C_GRID, 0.8, 0.4), 'C_TANK': (C_TANK, 1.2, 0.7),
        'C_ENGINE': (C_ENGINE, 1.8, 1.0), 'C_HULL': (C_HULL, 1.3, 1.0),
        'C_AERO': (C_AERO, 1.5, 1.0), 'C_FIRE': (C_FIRE, 1.5, 0.8),
        'C_THRUSTER': (C_THRUSTER, 1.5, 0.8), 'C_PLASMA': (C_PLASMA, 1.8, 0.9)
    }

    for c_key, pl_data in master_scene.items():
        if not pl_data or c_key not in layer_config: continue
        c_val, lw, alpha = layer_config[c_key]
        for xl, yl, zl in pl_data:
            # Orbital camera strictly focused on central action without bounds failures
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), 0.0, 0.0, cz_cam, azimuth, el_deg=7.0)
            render_queue.append((np.mean(depth), u, v, c_val, lw, alpha))

    # ABSOLUTE Z-SORT
    render_queue.sort(key=lambda item: item[0], reverse=True)
    for depth, u, v, c, lw, a in render_queue:
        ax.plot(u, v, color=c, lw=lw, alpha=a)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS
    # ------------------------------------------------------------------
    ui_t = cspan * 1.45
    ax.add_patch(patches.Rectangle((-cspan, ui_t), cspan*2, cspan*0.5, facecolor=C_BG, zorder=80))
    ax.plot([-cspan, cspan], [ui_t, ui_t], color=C_TEXT, lw=6, zorder=81)

    ax.text(-cspan*0.95, ui_t + cspan*0.06, "LG-450h // AEROSPACE KINEMATICS: STARSHIP FLIGHT OPERATIONS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cspan*0.95, ui_t + cspan*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // BALLISTIC KINEMATICS MATRIX", color=C_HULL, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    ui_b = -cspan * 1.777
    ax.add_patch(patches.Rectangle((-cspan, ui_b), cspan*2, cspan*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cspan, cspan], [ui_b + cspan*0.35, ui_b + cspan*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cspan*0.95, ui_b + cspan*0.14, f"[OPERATIONAL] {label}", color=C_AERO, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cspan*0.95, ui_b + cspan*0.08, f"TIMEFRAME VECTOR : T+{t:>05.2f}s (CONTINUOUS SHIP TRACKING)", color=C_TEXT, fontsize=13, fontname='monospace', weight='bold', zorder=82)
    
    booster_loc = "OFF_SITE" if t > 18.0 else f"{b_z:>05.1f}m"
    ax.text(-cspan*0.95, ui_b + cspan*0.03, f"KINEMATIC DELTAS : SHIP_ALT {s_z:>05.1f}m | BOOSTER_ALT {booster_loc}", color=C_THRUSTER, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-450h: FLIGHT OPERATIONS MATRIX [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Sequence Compiled. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
