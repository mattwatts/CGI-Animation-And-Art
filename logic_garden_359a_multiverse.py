"""
PROJECT: Logic Garden 359a (The Multiverse // Many-Worlds Decoherence)
FORMAT: YouTube Shorts (1080x1920)
METADATA: QUANTUM MECHANICS, DECOHERENCE, MANY WORLDS, WAVEFUNCTION
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
OUT_DIR = "frames_359a_multiverse"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- VISUAL PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#E5E7EB'
C_UNIFIED   = '#10B981'   # Coherent Superposition (Green)
C_WORLD_A   = '#00D2FF'   # Decohered Reality A (Cyan)
C_WORLD_B   = '#FFB300'   # Decohered Reality B (Gold)
C_OBSERVER  = '#DE008A'   # The Macroscopic Interaction Plane (Magenta)
C_SHADOW    = '#D1D5DB'

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

def get_projection(pt_3d, focal_length=1200.0, cam_dist=1200.0):
    z_cam = pt_3d[2] + cam_dist
    if z_cam < 10: return None
    sx = (pt_3d[0] * focal_length) / z_cam
    sy = (pt_3d[1] * focal_length) / z_cam
    return (sx, sy, z_cam)

def lerp_color(c1_hex, c2_hex, t):
    c1 = np.array(mcolors.to_rgb(c1_hex))
    c2 = np.array(mcolors.to_rgb(c2_hex))
    c_out = c1 * (1 - t) + c2 * t
    return mcolors.to_hex(np.clip(c_out, 0, 1))

# ------------------------------------------------------------------
# BASE GEOMETRY: THE WAVEFUNCTION (A Complex Torus Knot)
# ------------------------------------------------------------------
N_POINTS = 1600
t_ang = np.linspace(0, 2*np.pi, N_POINTS)
# P and Q dictate the elegant intertwining of the strands
p, q = 3, 8
knot_r = 180 + 70 * np.cos(q * t_ang)
hx = knot_r * np.cos(p * t_ang)
hz = knot_r * np.sin(p * t_ang)
hy = 200 * np.sin(q * t_ang)
base_waveform = np.column_stack((hx, hy, hz))

# Interaction Plane Math
PLANE_START_Y = 800.0
PLANE_END_Y   = -800.0
T_PLANE_START = 4.0
T_PLANE_END   = 10.0
PLANE_VEL     = (PLANE_START_Y - PLANE_END_Y) / (T_PLANE_END - T_PLANE_START)

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

    # 1. KINEMATIC CAMERA ORBIT
    # -------------------------
    # A grand, sweeping orbit to observe the split from multiple angles
    pitch = np.radians(-15 + 10 * np.sin(t * 0.3))
    yaw = t * 0.4
    sys_rotation = rotate_x(pitch) @ rotate_y(yaw)
    y_shift = -50
    
    render_queue = []

    # 2. DECOHERENCE LOGIC (UNZIPPING REALITY)
    # ----------------------------------------
    if T_PLANE_START <= t <= T_PLANE_END:
        current_plane_y = PLANE_START_Y - PLANE_VEL * (t - T_PLANE_START)
    elif t < T_PLANE_START:
        current_plane_y = 9999.0
    else:
        current_plane_y = -9999.0

    # Draw the expanding realities
    for i, pt in enumerate(base_waveform):
        # Calculate exactly when the "Observation Plane" passes this specific coordinate
        time_hit = T_PLANE_START + (PLANE_START_Y - pt[1]) / PLANE_VEL
        time_since_passed = max(0.0, t - time_hit)
        
        # Calculate separation distance (Expands rapidly, then smooths out)
        # World A pushes left and back; World B pushes right and forward
        dist = 200.0 * (1.0 - np.exp(-1.5 * time_since_passed))
        color_fade = np.clip(time_since_passed * 1.5, 0.0, 1.0)
        
        pos_A = pt + np.array([-dist, 0,  dist * 0.5])
        pos_B = pt + np.array([ dist, 0, -dist * 0.5])
        
        # Color transitioning from unified green into pure distinct world colors
        c_A = lerp_color(C_UNIFIED, C_WORLD_A, color_fade)
        c_B = lerp_color(C_UNIFIED, C_WORLD_B, color_fade)
        
        # If the plane hasn't passed, we draw the unified overlay
        if time_since_passed == 0:
            proj = np.dot(pt, sys_rotation.T)
            res = get_projection(proj)
            if res:
                s = 15.0 * (1200.0 / res[2])
                render_queue.append({
                    'type': 'pt', 'd': res[2], 'x': res[0], 'y': res[1]+y_shift, 
                    'c': C_UNIFIED, 's': s, 'alpha': 1.0
                })
        else:
            # Reality has branched. Draw both distinct worlds.
            proj_A = np.dot(pos_A, sys_rotation.T)
            res_A = get_projection(proj_A)
            if res_A:
                s_A = 12.0 * (1200.0 / res_A[2])
                render_queue.append({
                    'type': 'pt', 'd': res_A[2], 'x': res_A[0], 'y': res_A[1]+y_shift, 
                    'c': c_A, 's': s_A, 'alpha': 0.8
                })
                
            proj_B = np.dot(pos_B, sys_rotation.T)
            res_B = get_projection(proj_B)
            if res_B:
                s_B = 12.0 * (1200.0 / res_B[2])
                render_queue.append({
                    'type': 'pt', 'd': res_B[2], 'x': res_B[0], 'y': res_B[1]+y_shift, 
                    'c': c_B, 's': s_B, 'alpha': 0.8
                })

    # 3. RENDER THE INTERACTION PLANE (THE OBSERVER)
    # ----------------------------------------------
    alpha_plane = 0.0
    if T_PLANE_START - 1.0 < t < T_PLANE_END + 1.0:
        if t < T_PLANE_START:
            alpha_plane = (t - (T_PLANE_START - 1.0))
        elif t > T_PLANE_END:
            alpha_plane = 1.0 - (t - T_PLANE_END)
        else:
            alpha_plane = 1.0
            
    if alpha_plane > 0.01:
        plane_rad = 600.0
        plane_pts = np.array([
            [-plane_rad, current_plane_y, -plane_rad],
            [ plane_rad, current_plane_y, -plane_rad],
            [ plane_rad, current_plane_y,  plane_rad],
            [-plane_rad, current_plane_y,  plane_rad]
        ])
        proj_plane = np.dot(plane_pts, sys_rotation.T)
        screen_plane = []
        valid = True
        cams = []
        for p in proj_plane:
            res = get_projection(p)
            if not res: 
                valid = False
                break
            screen_plane.append([res[0], res[1] + y_shift])
            cams.append(res[2])
            
        if valid:
            d_mean = np.mean(cams)
            render_queue.append({
                'type': 'poly', 'd': d_mean, 'pts': np.array(screen_plane),
                'c': mcolors.to_rgba(C_OBSERVER, alpha_plane * 0.15),
                'ec': mcolors.to_rgba(C_OBSERVER, alpha_plane * 0.8)
            })

    # 4. ORTHOGRAPHIC Z-DEPTH DISPATCH
    # --------------------------------
    render_queue.sort(key=lambda item: item['d'], reverse=True)

    for item in render_queue:
        if item['type'] == 'pt':
            ax.scatter(item['x'], item['y'], color=item['c'], s=item['s'], edgecolors='none', alpha=item['alpha'], zorder=50)
        elif item['type'] == 'poly':
            ax.add_patch(patches.Polygon(item['pts'], facecolor=item['c'], edgecolor=item['ec'], lw=2, zorder=50))
            
    # ====================================================
    # 5. VISUAL TELEMETRY AND INFORMATION OVERLAYS
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_BG, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=2, zorder=81)

    ax.text(-500, 890, "LG-359a :: THE MULTIVERSE", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "MANY-WORLDS THEORY // DECOHERENCE AND BIFURCATION", color='#555555', fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_BG, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=2, zorder=81)

    # Narrative Telemetry Mapping
    if t < T_PLANE_START:
        s1, c1 = "COHERENT SUPERPOSITION", C_UNIFIED
        s2, c2 = "ENVIRONMENT IS ISOLATED", C_SHADOW
        t_state = "SYSTEM SPANS ALL POSSIBLE STATES SIMULTaneously"
    elif t < T_PLANE_END:
        s1, c1 = "MACROSCOPIC INTERACTION DETECTED", C_OBSERVER
        s2, c2 = "WAVEFUNCTION UNZIPPING", C_UNIFIED
        t_state = "ENVIRONMENT CAUSES IMMEDIATE QUANTUM DECOHERENCE"
    elif t < 16.0:
        s1, c1 = "TOPOLOGICAL BIFURCATION", C_TEXT
        s2, c2 = "REALITIES PULLING APART", C_WORLD_A
        t_state = "THE UNIVERSE SPLITS INTO DISTINCT PHYSICAL OUTCOMES"
    else:
        s1, c1 = "THE MANY WORLDS", C_TEXT
        s2, c2 = "BRANCHES SECURED AND ISOLATED", C_WORLD_B
        t_state = "IDENTICAL UNIVERSES OPERATING INDEPENDENTLY IN PARALLEL"

    ax.text(-500, -760, "SYS_01 [QUANTUM STATE] :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(30, -760, s1, color=c1, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [THE ENVIRONMENT]:", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(30, -800, s2, color=c2, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "SCIENTIFIC AUDIT       :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(30, -840, t_state, color=C_TEXT, fontsize=14, fontname='monospace', zorder=82)

    # Seamless Transition Progress Bar
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 4, facecolor='#E5E7EB', zorder=82))
    progress_color = C_UNIFIED if t < 10.0 else C_WORLD_A 
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 4, facecolor=progress_color, zorder=83))

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
    print(f"LG-359a: THE MULTIVERSE [CORES: {cpu_cores}] [RENDERING DECOHERENCE CLEAVE]")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
