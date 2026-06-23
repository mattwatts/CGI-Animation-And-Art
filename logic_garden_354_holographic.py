"""
PROJECT: Logic Garden 354 (The Holographic Principle)
FORMAT: YouTube Shorts (1080x1920)
METADATA: ASTROPHYSICS, QUANTUM GRAVITY, STRING THEORY, HOLOGRAPHIC BOUNDARY
EXECUTION: Seamless 24.0s Sequence. High Contrast Daylight Palette.
HOTFIX: Syntax variable string closure (T_PHASE1).
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
OUT_DIR = "frames_354_holographic"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- VISUAL PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#E5E7EB'
C_HORIZON   = '#9CA3AF'   # Translucent 2D Boundary Shell
C_BULK_A    = '#00D2FF'   # 3D Matter Array A (Cyan)
C_BULK_B    = '#FFB300'   # 3D Matter Array B (Gold)
C_PROJECT   = '#D1D5DB'   # Spatial Mapping Rays

# ------------------------------------------------------------------
# GEOMETRY ENGINE: ROTATION & PROJECTION
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

# ------------------------------------------------------------------
# GENERATING THE 3D KNOT (THE BULK VOLUME) & 2D HORIZON
# ------------------------------------------------------------------
R_HORIZON = 400.0
N_KNOT_PTS = 800
N_HORIZON_PTS = 1500

# 1. 3D Torus Knot (Inside Volume)
knot_t = np.linspace(0, 2 * np.pi, N_KNOT_PTS)
p, q = 3, 7  # Complexity of the bulk matter
# Scale and parameterize
knot_r = np.cos(q * knot_t) + 2.5
kx = knot_r * np.cos(p * knot_t) * 75
ky = knot_r * np.sin(p * knot_t) * 75
kz = -np.sin(q * knot_t) * 150

bulk_points = np.column_stack((kx, ky, kz))
bulk_colors = [C_BULK_A if (i % 2 == 0) else C_BULK_B for i in range(N_KNOT_PTS)]

# 2. 2D Spherical Horizon Shell (Fibonacci Sphere formulation for even coverage)
phi = np.pi * (3. - np.sqrt(5.))  # Golden angle
horizon_base = []
for i in range(N_HORIZON_PTS):
    y = 1 - (i / float(N_HORIZON_PTS - 1)) * 2
    radius = np.sqrt(1 - y * y)
    theta = phi * i
    x = np.cos(theta) * radius
    z = np.sin(theta) * radius
    horizon_base.append([x * R_HORIZON, y * R_HORIZON, z * R_HORIZON])
horizon_base = np.array(horizon_base)

def render_frame(packet):
    f, phase_ratio = packet
    t = phase_ratio * DURATION

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # Absolute Coordinate Frame
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)
    ax.autoscale(False)

    # Background Environment Grid
    for i in range(-5, 6):
        ax.plot([i*100, i*100], [-960, 960], color=C_GRID, lw=1, alpha=0.5, zorder=0)
    for j in range(-9, 10):
        ax.plot([-540, 540], [j*100, j*100], color=C_GRID, lw=1, alpha=0.5, zorder=0)

    # 1. TIMELINE & FADE MAPPING
    # --------------------------
    T_PHASE1 = 0.0
    T_HORIZON_FORM = 6.0
    T_PROJECT_START = 10.0
    T_DISSOLVE_BULK = 15.0
    T_FINISH = 20.0

    # Alpha controllers
    alpha_horizon = np.clip((t - T_HORIZON_FORM) / 4.0, 0.0, 1.0) * 0.15
    alpha_rays = ease_in_out(np.clip((t - T_PROJECT_START) / 3.0, 0.0, 1.0)) * \
                 (1.0 - ease_in_out(np.clip((t - T_DISSOLVE_BULK - 2.0) / 3.0, 0.0, 1.0))) * 0.4
    alpha_bulk = 1.0 - ease_in_out(np.clip((t - T_DISSOLVE_BULK) / 5.0, 0.0, 1.0))
    alpha_encode = ease_in_out(np.clip((t - T_PROJECT_START) / 4.0, 0.0, 1.0))

    # 2. SYSTEM ROTATION DYNAMICS
    # ---------------------------
    # Global camera slowly drifts to show 3D volume
    sys_rotation = rotate_x(np.radians(-20 + 5 * np.sin(t * 0.5))) @ rotate_y(t * 0.4) 
    
    # Intrinsic rotation of the bulk matter to show dynamic movement
    bulk_rotation = rotate_z(t * 0.8) @ rotate_x(t * 0.2)
    current_bulk = np.dot(bulk_points, bulk_rotation.T)

    y_shift = -70
    render_queue = []

    # Safe alpha wrapper
    def get_rgba(hex_color, a):
        return mcolors.to_rgba(hex_color, np.clip(a, 0.0, 1.0))

    # 3. POPULATE HORIZON SHELL (Background structure)
    # ------------------------------------------------
    if alpha_horizon > 0:
        proj_horiz = np.dot(horizon_base, sys_rotation.T)
        for pt in proj_horiz:
            depth = pt[1]
            render_queue.append({
                'type': 'pt', 'd': depth, 'x': pt[0], 'y': pt[2] + y_shift,
                'c': get_rgba(C_HORIZON, alpha_horizon), 's': 8, 'm': '.'
            })

    # 4. MAP THE HOLOGRAPHIC ENCODING
    # --------------------------------
    # For every point in the bulk, we project it onto the shell (R_HORIZON)
    proj_bulk = np.dot(current_bulk, sys_rotation.T)
    
    for i, pt in enumerate(current_bulk):
        bulk_color = bulk_colors[i]
        
        # Original 3D coordinate transformed by camera
        cam_bulk_pt = proj_bulk[i]
        
        # Calculate where this bulk point projects onto the 2D shell in true 3D space
        dist = np.linalg.norm(pt)
        if dist > 0.001:
            boundary_pt = (pt / dist) * R_HORIZON
            cam_bound_pt = np.dot(boundary_pt, sys_rotation.T)
            
            # --- Rendering Array ---
            
            # A. The Bulk Particles
            if alpha_bulk > 0.01:
                render_queue.append({
                    'type': 'pt', 'd': cam_bulk_pt[1], 'x': cam_bulk_pt[0], 'y': cam_bulk_pt[2] + y_shift,
                    'c': get_rgba(bulk_color, alpha_bulk), 's': 25, 'm': 'o'
                })
            
            # B. The Mapping Rays
            if alpha_rays > 0.01:
                render_queue.append({
                    'type': 'line', 'd': (cam_bulk_pt[1] + cam_bound_pt[1]) / 2.0,
                    'x': [cam_bulk_pt[0], cam_bound_pt[0]], 'y': [cam_bulk_pt[2] + y_shift, cam_bound_pt[2] + y_shift],
                    'c': get_rgba(C_PROJECT, alpha_rays), 'lw': 0.75
                })

            # C. The 2D Encoded Matrix (Surface Pixels)
            if alpha_encode > 0.01:
                render_queue.append({
                    'type': 'pt', 'd': cam_bound_pt[1], 'x': cam_bound_pt[0], 'y': cam_bound_pt[2] + y_shift,
                    'c': get_rgba(bulk_color, alpha_encode * (0.4 + 0.6*(dist/300.0))), 
                    's': 35 * alpha_encode, 'm': 'h'
                })

    # 5. SORT AND RENDER (Orthographic Z-Depth)
    # -----------------------------------------
    # Sort from background to foreground to ensure beautiful visual translucency
    render_queue.sort(key=lambda item: item['d'], reverse=True)

    for item in render_queue:
        if item['type'] == 'pt':
            ax.scatter(item['x'], item['y'], color=item['c'], s=item['s'], marker=item['m'], edgecolors='none', zorder=50)
        elif item['type'] == 'line':
            ax.plot(item['x'], item['y'], color=item['c'], lw=item['lw'], zorder=50)

    # ====================================================
    # 6. VISUAL TELEMETRY AND INFORMATION OVERLAYS
    # ====================================================
    # Top Information Header
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_BG, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=2, zorder=81)

    ax.text(-500, 890, "LG-354 :: THE HOLOGRAPHIC PRINCIPLE", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "QUANTUM GRAVITY // ENCODING 3D VOLUME ON 2D BOUNDARY", color='#555555', fontsize=12, fontname='monospace', zorder=82)

    # Bottom Information Footer
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_BG, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=2, zorder=81)

    # Dynamic Descriptive Text
    if t < T_HORIZON_FORM:
        s1, c1 = "3D BULK VOLUME ACTIVE", C_BULK_A
        s2, c2 = "AWAITING BOUNDARY HORIZON", '#888888'
        t_state = "OBSERVING THREE-DIMENSIONAL SPATIAL METRIC"
    elif t < T_PROJECT_START:
        s1, c1 = "3D BULK VOLUME ACTIVE", C_BULK_A
        s2, c2 = "2D BOUNDARY HORIZON DETECTED", C_TEXT
        t_state = "ESTABLISHING LOWER-DIMENSIONAL ENCLOSURE"
    elif t < T_DISSOLVE_BULK:
        s1, c1 = "VOLUME-TO-SURFACE MAPPING IN PROGRESS", C_BULK_B
        s2, c2 = "2D BOUNDARY ENCODING DATA", C_BULK_A
        t_state = "CALCULATING HOLOGRAPHIC INFORMATION TRANSFER"
    else:
        s1, c1 = "3D BULK VOLUME DISSOLVED // ILLUSION SUPPRESSED", '#888888'
        s2, c2 = "2D BOUNDARY PERFECTLY ENCODES ALL INFORMATION", C_BULK_B
        t_state = "HOLOGRAPHIC PRINCIPLE VERIFIED: REALITY IS 2D"

    ax.text(-500, -760, "SYS_01 [INTERIOR SPACE]  :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, s1, color=c1, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [EXTERIOR SHELL]  :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, s2, color=c2, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "STRUCTURAL STATE AUDIT   :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, t_state, color=C_TEXT, fontsize=14, fontname='monospace', zorder=82)

    # Seamless Transition Progress Bar
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 4, facecolor='#E5E7EB', zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 4, facecolor=C_BULK_A, zorder=83))

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
    print(f"LG-354: HOLOGRAPHIC PRINCIPLE [CORES: {cpu_cores}] [RENDERING SEQUENCE]")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
