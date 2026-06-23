"""
PROJECT: Logic Garden 360 (The Gravitational Membrane // Brane Cosmology)
FORMAT: YouTube Shorts (1080x1920)
METADATA: STRING THEORY, M-THEORY, GRAVITY, HIERARCHY PROBLEM, BRANES
EXECUTION: Continuous 24.0s Sequence. True 3D Z-Depth Engine. Daylight Palette.
HOTFIX: Eradicated bbox_inches='tight' for Absolute Camera Lock. Re-aligned HUD text to prevent boundary breach.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import multiprocessing as mp
import os
import gc

# ======== SEQUENCE PARAMETERS ========
DURATION = 24.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_360_brane_cosmology"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- VISUAL PALETTE --------
C_BG          = '#FFFFFF'
C_TEXT        = '#111115'
C_BULK_GRID   = '#E5E7EB'   # The Higher Dimensional Void
C_BRANE       = '#00D2FF'   # Our 3D Universe (Cyan Membrane)
C_BOUND_FORCE = '#DE008A'   # Electromagnetism / Open Strings (Magenta)
C_GRAVITY     = '#FFB300'   # Gravitons / Closed Strings (Gold)

# ------------------------------------------------------------------
# 3D PERSPECTIVE ENGINE 
# ------------------------------------------------------------------
def rotate_x(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])

def rotate_y(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])

def rotate_z(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

def ease_in_out(t):
    t = np.clip(t, 0.0, 1.0)
    return 4 * t**3 if t < 0.5 else 1 - (-2 * t + 2)**3 / 2

def get_projection(pt_3d, focal_length=1600.0, cam_dist=1800.0):
    z_cam = pt_3d[2] + cam_dist
    if z_cam < 10: return None
    sx = (pt_3d[0] * focal_length) / z_cam
    sy = (pt_3d[1] * focal_length) / z_cam
    return (sx, sy, z_cam)

def clip_check(sz):
    """Strict Frustum Culling: Annihilates lines outside the 1080x1920 viewport"""
    xs = [p[0] for p in sz]
    ys = [p[1] for p in sz]
    if min(xs) > 600 or max(xs) < -600: return False   # 540 bound + padding
    if min(ys) > 1050 or max(ys) < -1050: return False # 960 bound + padding
    return True

def get_brane_y(x, z, t):
    """Calculates the undulating fluid motion of the spacetime membrane"""
    wave1 = np.sin(x * 0.0015 + t * 2.0) * np.cos(z * 0.002 + t * 1.5)
    wave2 = np.sin(x * 0.0025 - t * 1.0) * 0.5
    return (wave1 + wave2) * 160.0

# ------------------------------------------------------------------
# BASE GEOMETRY ARRAYS (TITAN-CLASS SCALED TO ERADICATE DEAD SPACE)
# ------------------------------------------------------------------
# 1. The Brane Grid (Our Universe) - Expanded to +/- 6000
grid_size = 75
x_range = np.linspace(-6000, 6000, grid_size)
z_range = np.linspace(-6000, 6000, grid_size)

# 2. Bound Forces (Open Strings scaled for density)
np.random.seed(360)
N_BOUND = 1200
bound_pts = []
for _ in range(N_BOUND):
    x = np.random.uniform(-5000, 5000)
    z = np.random.uniform(-5000, 5000)
    phase = np.random.uniform(0, 2*np.pi)
    bound_pts.append({'x': x, 'z': z, 'p': phase})

# 3. Gravitons (Closed Strings / Loops)
N_GRAV = 700
grav_pts = []
for i in range(N_GRAV):
    x = np.random.uniform(-5000, 5000)
    z = np.random.uniform(-5000, 5000)
    t_spawn = np.random.uniform(-6.0, DURATION)
    grav_pts.append({'x': x, 'z': z, 'ts': t_spawn})

# 4. The Bulk Background Lines (Expanded deep into Y-axis Cartesian limits)
bulk_lines = []
for yy in np.arange(-6000, 201, 600):
    for xx in np.arange(-6000, 6001, 1000):
        bulk_lines.append([[xx, yy, -6000], [xx, yy, 6000]])
    for zz in np.arange(-6000, 6001, 1000):
        bulk_lines.append([[-6000, yy, zz], [6000, yy, zz]])

def render_frame(packet):
    f, phase_ratio = packet
    t = phase_ratio * DURATION

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # Absolute Coordinate Bounding Box lock
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)
    ax.autoscale(False)

    # 1. KINEMATIC CAMERA TIMELINE & LENS OVERRIDE
    # --------------------------------------------
    cam_tilt = ease_in_out(np.clip((t - 4.0)/8.0, 0, 1))
    
    # Pitch clamped to +30deg minimum so the horizon never drops into frame
    pitch = np.radians(65 - 35 * cam_tilt)  
    yaw = t * 0.08  
    sys_rotation = rotate_x(pitch) @ rotate_y(yaw)
    
    dynamic_focal = 1400.0 + (400.0 * cam_tilt)
    dynamic_dist = 2200.0 - (400.0 * cam_tilt)
    y_shift = 0 + (350 * cam_tilt)  # Tracks the membrane upwards physically
    
    render_queue = []

    # 2. RENDER THE BULK (Higher Dimensions)
    # --------------------------------------
    bulk_alpha = cam_tilt * 0.4
    if bulk_alpha > 0.01:
        for line in bulk_lines:
            pts = np.dot(line, sys_rotation.T)
            sz = []
            cams = []
            for p in pts:
                res = get_projection(p, focal_length=dynamic_focal, cam_dist=dynamic_dist)
                if res:
                    sz.append([res[0], res[1] + y_shift])
                    cams.append(res[2])
            if len(sz) == 2 and clip_check(sz):
                render_queue.append({
                    'type': 'line', 'd': np.mean(cams), 'pts': sz, 
                    'c': mcolors.to_rgba(C_BULK_GRID, bulk_alpha), 'lw': 1.0
                })

    # 3. RENDER THE BRANE (Our Universe)
    # ----------------------------------
    surface_map = {}
    for xi, x in enumerate(x_range):
        for zi, z in enumerate(z_range):
            y = get_brane_y(x, z, t)
            surface_map[(xi, zi)] = np.array([x, y, z])

    brane_alpha = 0.6 + 0.3 * (1 - cam_tilt)
    for xi in range(grid_size - 1):
        for zi in range(grid_size - 1):
            p1 = surface_map[(xi, zi)]
            p2 = surface_map[(xi+1, zi)]
            p3 = surface_map[(xi, zi+1)]
            
            for start, end in [(p1, p2), (p1, p3)]:
                proj = np.dot([start, end], sys_rotation.T)
                sz = []
                cams = []
                for p in proj:
                    res = get_projection(p, focal_length=dynamic_focal, cam_dist=dynamic_dist)
                    if res:
                        sz.append([res[0], res[1] + y_shift])
                        cams.append(res[2])
                if len(sz) == 2 and clip_check(sz):
                    render_queue.append({
                        'type': 'line', 'd': np.mean(cams), 'pts': sz, 
                        'c': mcolors.to_rgba(C_BRANE, brane_alpha), 'lw': 1.5
                    })

    # 4. RENDER BOUND FORCES (Open Strings/Light/Matter)
    # --------------------------------------------------
    force_alpha = np.clip((t - 4.0)/3.0, 0.0, 1.0) if t > 4.0 else 0.0
    force_alpha = max(0.5, force_alpha)

    for bp in bound_pts:
        x, z, p = bp['x'], bp['z'], bp['p']
        y_base = get_brane_y(x, z, t)
        vib_height = 120.0 * abs(np.sin(t * 8.0 + p))
        pt_bottom = np.array([x, y_base, z])
        pt_top    = np.array([x, y_base + vib_height, z])
        
        proj = np.dot([pt_bottom, pt_top], sys_rotation.T)
        sz = []
        cams = []
        for p_3d in proj:
            res = get_projection(p_3d, focal_length=dynamic_focal, cam_dist=dynamic_dist)
            if res:
                sz.append([res[0], res[1] + y_shift])
                cams.append(res[2])
        if len(sz) == 2 and clip_check(sz):
            render_queue.append({
                'type': 'line', 'd': np.mean(cams), 'pts': sz, 
                'c': mcolors.to_rgba(C_BOUND_FORCE, force_alpha), 'lw': 3.5
            })

    # 5. RENDER GRAVITY (Closed Strings leaking into the Bulk)
    # --------------------------------------------------------
    grav_alpha_global = np.clip((t - 14.0)/4.0, 0.0, 1.0)
    
    if grav_alpha_global > 0.01:
        for gp in grav_pts:
            x, z, ts = gp['x'], gp['z'], gp['ts']
            if ts > t: continue 
            
            t_local = t - ts
            y_base = get_brane_y(x, z, ts) 
            drop_dist = (t_local ** 2.5) * -35.0
            y_cur = y_base + drop_dist
            
            radius = 20.0 + (t_local * 45.0)
            fade = 1.0 - np.clip(t_local / 7.0, 0.0, 1.0)
            alpha_g = grav_alpha_global * fade
            
            if alpha_g > 0.01:
                ring_pts = []
                for ang in np.linspace(0, 2*np.pi, 20):
                    ring_pts.append([x + radius*np.cos(ang), y_cur, z + radius*np.sin(ang)])
                
                for i in range(len(ring_pts)-1):
                    proj = np.dot([ring_pts[i], ring_pts[i+1]], sys_rotation.T)
                    sz = []
                    cams = []
                    for pp in proj:
                        res = get_projection(pp, focal_length=dynamic_focal, cam_dist=dynamic_dist)
                        if res:
                            sz.append([res[0], res[1] + y_shift])
                            cams.append(res[2])
                    if len(sz) == 2 and clip_check(sz):
                        render_queue.append({
                            'type': 'line', 'd': np.mean(cams), 'pts': sz, 
                            'c': mcolors.to_rgba(C_GRAVITY, alpha_g), 'lw': 2.5
                        })

    # 6. ORTHOGRAPHIC Z-DEPTH DISPATCH (With Frustum Overrides)
    # ---------------------------------------------------------
    render_queue.sort(key=lambda item: item['d'], reverse=True)

    for item in render_queue:
        pts = item['pts']
        ax.plot([pts[0][0], pts[1][0]], [pts[0][1], pts[1][1]], color=item['c'], lw=item['lw'], zorder=50)

    # ====================================================
    # 7. TELEMETRY AND HUD WIDGETS
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_BG, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=2, zorder=81)

    ax.text(-500, 890, "LG-360 :: THE GRAVITATIONAL MEMBRANE", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "M-THEORY // BRANE COSMOLOGY & THE HIERARCHY PROBLEM", color='#555555', fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_BG, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=2, zorder=81)

    if t < 6.0:
        s1, c1 = "THE 3D UNIVERSE", C_BRANE
        s2, c2 = "APPARENT REALITY DETECTED", C_TEXT
        t_state = "OBSERVATION: A CONTINUOUS, FLUCTUATING SPACETIME GRID"
    elif t < 12.0:
        s1, c1 = "OPEN STRINGS // ELECTROMAGNETIC FORCE", C_BOUND_FORCE
        s2, c2 = "ENERGY RIGIDLY CLAMPED TO THE PLANE", C_TEXT
        t_state = "PROPERTIES OF LIGHT AND MATTER ARE TRAPPED ON OUR MEMBRANE"
    elif t < 18.0:
        s1, c1 = "HIGHER-DIMENSIONAL SPACE REVEALED", C_BULK_GRID
        s2, c2 = "THE UNIVERSAL MEMBRANE FLOTATION", C_TEXT
        t_state = "OUR 3D REALITY IS JUST A SLICE OF A MUCH LARGER VOID"
    else:
        s1, c1 = "CLOSED STRINGS // GRAVITONS DETACHING", C_GRAVITY
        s2, c2 = "UNTETHERED LOOPS LEAKING INTO THE VOID", C_TEXT
        t_state = "CONCLUSION: GRAVITY IS WEAK BECAUSE IT LEAKS INTO HIGHER DIMENSIONS"

    ax.text(-500, -760, "SYS_01 [TOPOLOGICAL STATE]   :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(60, -760, s1, color=c1, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [PHYSICAL CONSTANTS]  :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(60, -800, s2, color=c2, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    # Sovereign Fix: Re-aligned text to own line to ensure string stays absolutely within x=540
    ax.text(-500, -840, "SCIENTIFIC AUDIT             :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -865, t_state, color=C_TEXT, fontsize=14, fontname='monospace', zorder=82)

    # Seamless Transition Progress Bar
    ax.add_patch(patches.Rectangle((-500, -895), 1000, 4, facecolor='#E5E7EB', zorder=82)) # Adjusted down slightly
    
    prog_c = C_BRANE
    if t > 6.0: prog_c = C_BOUND_FORCE
    if t > 18.0: prog_c = C_GRAVITY
    ax.add_patch(patches.Rectangle((-500, -895), 1000 * phase_ratio, 4, facecolor=prog_c, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    # Sovereign Fix: Removed bbox_inches='tight' and pad_inches to absolutely enforce the O(1) 1080x1920 Bounding Box
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close('all')
    gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-360: THE GRAVITATIONAL MEMBRANE [CORES: {cpu_cores}] [RENDERING TITAN ARCHITECTURE OVERRIDE]")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
