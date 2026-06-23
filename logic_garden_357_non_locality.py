"""
PROJECT: Logic Garden 357 (Non-Locality & Entanglement)
FORMAT: YouTube Shorts (1080x1920)
METADATA: QUANTUM MECHANICS, NON-LOCALITY, HOLOGRAPHIC PRINCIPLE
EXECUTION: Continuous 24.0s Sequence. True 3D Perspective Projection. Daylight Palette.
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
OUT_DIR = "frames_357_non_locality"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- VISUAL PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#D1D5DB'   # 3D Space Illusion Grid
C_HORIZON   = '#9CA3AF'   # Translucent 2D Boundary Shell
C_STATE_1   = '#00D2FF'   # Particle Spin State A (Cyan)
C_STATE_2   = '#DE008A'   # Particle Spin State B (Magenta)
C_WAVEFRONT = '#FFB300'   # Speed of Light Constraint
C_PROJECT   = '#5A6270'   # Holographic Projection Rays

# ------------------------------------------------------------------
# 3D PERSPECTIVE ENGINE & KINEMATICS
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

def get_projection(pt_3d, focal_length=1200.0, cam_dist=1200.0):
    z_cam = pt_3d[2] + cam_dist
    if z_cam < 10: return None
    sx = (pt_3d[0] * focal_length) / z_cam
    sy = (pt_3d[1] * focal_length) / z_cam
    return (sx, sy, z_cam)

def bezier_curve(p0, p1, p2, num_pts=60):
    pts = []
    for t in np.linspace(0, 1, num_pts):
        pt = ((1-t)**2)*p0 + 2*(1-t)*t*p1 + (t**2)*p2
        pts.append(pt)
    return np.array(pts)

# ------------------------------------------------------------------
# GEOMETRY GENERATION
# ------------------------------------------------------------------
# 1. Background Illusion Grid (Restricted to XZ plane)
grid_lines = []
for idx in np.arange(-500, 600, 100):
    grid_lines.append((np.array([[idx, -200, -500], [idx, -200, 500]])))
    grid_lines.append((np.array([[-500, -200, idx], [500, -200, idx]])))

# 2. 2D Boundary Shell (Fibonacci Sphere representing the holographic horizon)
N_HORIZON_PTS = 2000
R_HORIZON = 600.0
phi = np.pi * (3. - np.sqrt(5.))
horizon_base = []
for i in range(N_HORIZON_PTS):
    y = 1 - (i / float(N_HORIZON_PTS - 1)) * 2
    radius = np.sqrt(1 - y * y)
    theta = phi * i
    x = np.cos(theta) * radius
    z = np.sin(theta) * radius
    horizon_base.append([x * R_HORIZON, y * R_HORIZON, z * R_HORIZON])
horizon_base = np.array(horizon_base)

# Constant Target Holographic Coordinates (Adjacent on the Boundary)
H_A = np.array([-15, R_HORIZON-5, 0])
H_B = np.array([ 15, R_HORIZON-5, 0])

def render_frame(packet):
    f, phase_ratio = packet
    t = phase_ratio * DURATION

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)
    ax.autoscale(False)

    # 1. NARRATIVE TIMELINE
    # ---------------------
    T_SEPARATE = 3.0
    T_FLIP = 5.0
    T_HORIZON_IN = 9.0
    T_RAY_IN = 12.0
    T_TRUE_PROXIMITY = 16.0
    T_GRID_OUT = 18.0

    # Opacities
    alpha_grid   = 1.0 if t < T_GRID_OUT else 1.0 - ease_in_out(np.clip((t - T_GRID_OUT)/3.0, 0, 1))
    alpha_horizon = ease_in_out(np.clip((t - T_HORIZON_IN)/3.0, 0, 1))
    alpha_rays = ease_in_out(np.clip((t - T_RAY_IN)/3.0, 0, 1))
    alpha_true = ease_in_out(np.clip((t - T_TRUE_PROXIMITY)/2.0, 0, 1))

    # Kinematics: 3D Particle Separation
    if t < T_SEPARATE:
        dist = 350.0 * ease_in_out(t / T_SEPARATE)
    else:
        dist = 350.0

    # 3D Coordinates
    P_A = np.array([-dist, -200, 0])
    P_B = np.array([ dist, -200, 0])

    # Particle states (Entanglement action)
    c_part_A = C_STATE_1 if t < T_FLIP else C_STATE_2
    c_part_B = C_STATE_1 if t < T_FLIP else C_STATE_2

    # Global rotation to visualize depth, panning slightly upwards over time
    pitch = np.radians(-15 + 10 * ease_in_out(np.clip((t - T_HORIZON_IN)/8.0, 0, 1)))
    yaw = t * 0.15
    sys_rotation = rotate_x(pitch) @ rotate_y(yaw)
    y_shift = -100
    
    render_queue = []

    def push_point(p_3d, color, size, alpha, marker='o'):
        proj = np.dot(p_3d, sys_rotation.T)
        res = get_projection(proj)
        if res:
            render_queue.append({
                'type': 'pt', 'd': res[2], 'x': res[0], 'y': res[1] + y_shift,
                'c': mcolors.to_rgba(color, np.clip(alpha, 0, 1)), 's': size * (1200.0/res[2]), 'm': marker
            })

    def push_line(pts_3d, color, lw, alpha):
        proj = np.dot(pts_3d, sys_rotation.T)
        sz = []
        cams = []
        for p in proj:
            res = get_projection(p)
            if res:
                sz.append([res[0], res[1] + y_shift])
                cams.append(res[2])
        if len(sz) == len(pts_3d):
            render_queue.append({
                'type': 'line', 'd': np.mean(cams), 'pts': np.array(sz), 
                'c': mcolors.to_rgba(color, np.clip(alpha, 0, 1)), 'lw': lw
            })

    # 2. SCENE ASSEMBLY
    # -----------------
    # Illusion Grid
    if alpha_grid > 0.01:
        for line in grid_lines:
            push_line(line, C_GRID, 1.0, alpha_grid * 0.4)

    # The Entangled Particles (In False 3D Space)
    # They vibrate based on energy
    vib_A = P_A + np.random.uniform(-4, 4, 3)
    vib_B = P_B + np.random.uniform(-4, 4, 3)
    push_point(vib_A, c_part_A, 40, alpha_grid, marker='o')
    push_point(vib_B, c_part_B, 40, alpha_grid, marker='o')

    # The Light-Speed Wavefront (The Paradox visualizer)
    if T_FLIP < t < T_HORIZON_IN:
        # Expanding sphere of light from Particle A showing it's physically impossible 
        # for a signal to have travelled to Particle B in 0 seconds.
        wave_radius = (t - T_FLIP) * 120.0
        wave_pts = []
        for theta in np.linspace(0, 2*np.pi, 60):
            wave_pts.append(P_A + np.array([wave_radius*np.cos(theta), 0, wave_radius*np.sin(theta)]))
        for i in range(len(wave_pts)-1):
            push_line([wave_pts[i], wave_pts[i+1]], C_WAVEFRONT, 2.0, 0.8)

    # The Holographic Horizon Shell
    if alpha_horizon > 0.01:
        proj_horiz = np.dot(horizon_base, sys_rotation.T)
        for pt in proj_horiz:
            # We skip rendering dots near the projection targets to make them stand out
            if np.linalg.norm(pt - np.dot(H_A, sys_rotation.T)) < 50: continue
            if np.linalg.norm(pt - np.dot(H_B, sys_rotation.T)) < 50: continue
            
            res = get_projection(pt)
            if res:
                render_queue.append({
                    'type': 'pt', 'd': res[2], 'x': res[0], 'y': res[1] + y_shift,
                    'c': mcolors.to_rgba(C_HORIZON, alpha_horizon * 0.15), 's': 5, 'm': '.'
                })

    # The Holographic Projection Rays (Mapping 3D coordinates to adjacent 2D topology)
    if alpha_rays > 0.01:
        C_A = np.array([-350, 200, 0])
        C_B = np.array([ 350, 200, 0])
        
        curve_A = bezier_curve(P_A, C_A, H_A)
        curve_B = bezier_curve(P_B, C_B, H_B)
        
        # Animate drawing the rays
        anim_prg = np.clip((t - T_RAY_IN) / 2.0, 0.0, 1.0)
        idx = int(anim_prg * len(curve_A))
        
        if idx > 1:
            for i in range(idx - 1):
                push_line([curve_A[i], curve_A[i+1]], C_PROJECT, 1.5, alpha_rays * 0.6)
                push_line([curve_B[i], curve_B[i+1]], C_PROJECT, 1.5, alpha_rays * 0.6)

    # The True Reality (Tokens adjacent on the boundary)
    if alpha_horizon > 0.01:
        h1 = H_A + np.random.uniform(-1, 1, 3)
        h2 = H_B + np.random.uniform(-1, 1, 3)
        
        # Before projection completes, show them as hollow targets
        if t < T_TRUE_PROXIMITY:
            push_point(h1, C_GRID, 30, alpha_horizon * 0.5, marker='h')
            push_point(h2, C_GRID, 30, alpha_horizon * 0.5, marker='h')
        else:
            # Full illumination: The true origin of the entangled state
            push_point(h1, c_part_A, 50, alpha_true, marker='h')
            push_point(h2, c_part_B, 50, alpha_true, marker='h')
            
            # The exact, immediate zero-distance topological lock
            push_line([h1, h2], C_STATE_2, 4.0, alpha_true)


    # 3. DEPTH SORT AND RENDER
    # ------------------------
    render_queue.sort(key=lambda item: item['d'], reverse=True)

    for item in render_queue:
        if item['type'] == 'line':
            pts = item['pts']
            ax.plot([pts[0][0], pts[1][0]], [pts[0][1], pts[1][1]], color=item['c'], lw=item['lw'], zorder=50)
        elif item['type'] == 'pt':
            ax.scatter(item['x'], item['y'], color=item['c'], s=item['s'], marker=item['m'], edgecolors='none', zorder=50)


    # ====================================================
    # 4. VISUAL TELEMETRY AND INFORMATION OVERLAYS
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_BG, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=2, zorder=81)

    ax.text(-500, 890, "LG-357 :: NON-LOCALITY AND ENTANGLEMENT", color=C_TEXT, fontsize=22, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "HOLOGRAPHIC PROJECTION // 3D DISTANCE IS AN ILLUSION", color='#555555', fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_BG, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=2, zorder=81)

    # Dynamic Descriptive Text
    if t < T_FLIP:
        s1, c1 = "ENTANGLED PARTICLES CREATED", C_STATE_1
        s2, c2 = "RAPID SPATIAL SEPARATION DETECTED", C_TEXT
        t_state = "OBSERVATION: DEEP CARTESIAN DISTANCE MEASURED"
    elif t < T_HORIZON_IN:
        s1, c1 = "INSTANTANEOUS STATE CHANGE", C_STATE_2
        s2, c2 = "IMPOSSIBLE CORRELATION SPEED", C_WAVEFRONT
        t_state = "PARADOX: REACTION EXCEEDS THE SPEED OF LIGHT"
    elif t < T_TRUE_PROXIMITY:
        s1, c1 = "REVEALING TRUE BASEPLATE DATA", C_PROJECT
        s2, c2 = "MAPPING 3D COORDINATES TO 2D SHELL", C_TEXT
        t_state = "ANALYZING HOLOGRAPHIC BOUNDARY TOPOLOGY"
    else:
        s1, c1 = "PARTICLES ARE ADJACENT ON THE HORIZON", C_STATE_2
        s2, c2 = "STATE CHANGE DISTANCE EQUALS ZERO", C_TEXT
        t_state = "CONCLUSION: SPATIAL LOCALITY IS A 3D RENDERING ILLUSION"

    ax.text(-500, -760, "SYS_01 [QUANTUM STATE] :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(30, -760, s1, color=c1, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [SPATIAL GEOMETRY]:", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(30, -800, s2, color=c2, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "SCIENTIFIC AUDIT       :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(30, -840, t_state, color=C_TEXT, fontsize=14, fontname='monospace', zorder=82)

    # Seamless Transition Progress Bar
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 4, facecolor='#E5E7EB', zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 4, facecolor=C_STATE_1, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0)
    plt.close('all')
    gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-357: NON LOCALITY [CORES: {cpu_cores}] [RENDERING TOPOLOGICAL PARADOX]")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
