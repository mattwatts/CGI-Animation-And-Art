"""
PROJECT: Logic Garden 356 (Entropic & Emergent Gravity)
FORMAT: YouTube Shorts (1080x1920)
METADATA: ASTROPHYSICS, EMERGENT GRAVITY, THERMODYNAMICS, INFORMATION THEORY
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
OUT_DIR = "frames_356_entropic_gravity"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- VISUAL PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#E5E7EB'
C_MASS      = '#8B93A0'   # Physical Macroscopic Mass
C_ENTROPY_H = '#00D2FF'   # High Entropy / High Density Information (Cyan)
C_ENTROPY_L = '#E5E7EB'   # Low Entropy / Depleted Information (Grey)
C_HIGHLIGHT = '#FFB300'   # Thermodynamic Pressure Vectors (Gold)

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

# ------------------------------------------------------------------
# SCENE GEOMETRY GENERATION
# ------------------------------------------------------------------
# 1. Macroscopic Spheres
def generate_sphere_quads(radius=150, lats=16, lons=32):
    quads = []
    lat = np.linspace(-np.pi/2, np.pi/2, lats)
    lon = np.linspace(0, 2*np.pi, lons)
    for i in range(lats-1):
        for j in range(lons-1):
            v1 = [radius*np.cos(lat[i])*np.sin(lon[j]), radius*np.sin(lat[i]), radius*np.cos(lat[i])*np.cos(lon[j])]
            v2 = [radius*np.cos(lat[i+1])*np.sin(lon[j]), radius*np.sin(lat[i+1]), radius*np.cos(lat[i+1])*np.cos(lon[j])]
            v3 = [radius*np.cos(lat[i+1])*np.sin(lon[j+1]), radius*np.sin(lat[i+1]), radius*np.cos(lat[i+1])*np.cos(lon[j+1])]
            v4 = [radius*np.cos(lat[i])*np.sin(lon[j+1]), radius*np.sin(lat[i]), radius*np.cos(lat[i])*np.cos(lon[j+1])]
            quads.append(np.array([v1, v2, v3, v4]))
    return np.array(quads)

BASE_SPHERE = generate_sphere_quads()

# 2. Quantum Information Matrix (A volume of microstate nodes)
np.random.seed(356)
N_NODES = 2500
nodes_base = []
for _ in range(N_NODES):
    x = np.random.uniform(-700, 700)
    y = np.random.uniform(-700, 700)
    z = np.random.uniform(-700, 700)
    # Give each node a unique frequency and phase for vibration
    freq = np.random.uniform(2.0, 10.0)
    phase = np.random.uniform(0, 2 * np.pi)
    nodes_base.append({'pos': np.array([x, y, z]), 'f': freq, 'p': phase})

# Lighting array
LIGHT_DIR = np.array([0.5, 0.7, -0.4])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

def get_shaded_color(hex_color, normal, alpha):
    rgb = np.array(mcolors.to_rgb(hex_color))
    amb = 0.3
    diff = 0.7 * max(0, -np.dot(normal, LIGHT_DIR)) # Looking at front
    final_rgb = np.clip(rgb * (amb + diff), 0, 1)
    return mcolors.to_rgba(final_rgb, np.clip(alpha, 0, 1))

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
    T_MATRIX_IN  = 4.0
    T_MATRIX_ON  = 8.0
    T_PUSH_START = 11.0
    T_PUSH_END   = 19.0
    T_MATRIX_OUT = 21.0

    # Visibility Opacity
    if t < T_MATRIX_IN:
        alpha_matrix = 0.0
    elif t < T_MATRIX_ON:
        alpha_matrix = (t - T_MATRIX_IN) / (T_MATRIX_ON - T_MATRIX_IN)
    elif t < T_PUSH_END:
        alpha_matrix = 1.0
    elif t < T_MATRIX_OUT:
        alpha_matrix = 1.0 - (t - T_PUSH_END) / (T_MATRIX_OUT - T_PUSH_END)
    else:
        alpha_matrix = 0.0

    alpha_matrix = ease_in_out(alpha_matrix)

    # Kinematics: The spheres drifting together smoothly
    push_progress = np.clip((t - T_PUSH_START) / (T_PUSH_END - T_PUSH_START), 0.0, 1.0)
    push_ease = ease_in_out(push_progress)
    
    # Starting offset is +/- 300. Ending offset is +/- 150 (touching)
    mass_offset_x = 300.0 - (150.0 * push_ease)

    # Global rotation to visualize depth
    sys_rotation = rotate_x(np.radians(-15 + 5 * np.cos(t * 0.5))) @ rotate_y(t * 0.3)
    y_shift = -50
    
    render_queue = []

    # 2. RENDER MACROSCOPIC MASSES (The Spheres)
    # ------------------------------------------
    centers = [np.array([-mass_offset_x, 0, 0]), np.array([mass_offset_x, 0, 0])]
    
    for center in centers:
        # Move base sphere to center, then rotate for camera
        offset_quads = [quad + center for quad in BASE_SPHERE]
        for quad in offset_quads:
            proj = np.dot(quad, sys_rotation.T)
            z_cams = proj[:, 2] + 1200.0
            if np.any(z_cams < 10): continue
                
            v1, v2, v3 = proj[0], proj[1], proj[2]
            nrm = np.cross(v2 - v1, v3 - v1)
            mag = np.linalg.norm(nrm)
            if mag > 0: nrm /= mag
            
            if nrm[2] > 0: continue # Backface cull

            screen_pts = []
            for pt in proj:
                res = get_projection(pt)
                if res: screen_pts.append([res[0], res[1] + y_shift])
                
            if len(screen_pts) == 4:
                z_depth = np.mean(z_cams)
                c_shade = get_shaded_color(C_MASS, nrm, 1.0)
                render_queue.append({'type': 'poly', 'd': z_depth, 'pts': np.array(screen_pts), 'c': c_shade})

    # 3. RENDER THE INFORMATION MATRIX (Entropic Pressure)
    # ----------------------------------------------------
    if alpha_matrix > 0.01:
        for node in nodes_base:
            base_p = node['pos']
            
            # Check proximity to the two masses
            d1 = np.linalg.norm(base_p - centers[0])
            d2 = np.linalg.norm(base_p - centers[1])
            
            # Cull nodes physically inside the macroscopic spheres
            if d1 < 145 or d2 < 145: continue
            
            # Entropy gradient calculation:
            # Nodes outside the masses vibrate highly (pressure). 
            # Nodes in the direct gap between them are depleted of states.
            is_between = (base_p[0] > -mass_offset_x and base_p[0] < mass_offset_x) and \
                         (abs(base_p[1]) < 180) and (abs(base_p[2]) < 180)
            
            if is_between:
                # The Gap (Low Entropy)
                amp = 2.0
                c_node = C_ENTROPY_L
                node_alpha = alpha_matrix * 0.3
            else:
                # The Outer Pressure (High Entropy)
                # Pressure increases dynamically as we enter the pushing phase
                amp = 10.0 + (30.0 * push_ease)
                c_node = C_ENTROPY_H
                node_alpha = alpha_matrix * 0.8
                
                # Near the back ends of the spheres, highlight the mathematical 'push'
                if (base_p[0] < -(mass_offset_x + 100) or base_p[0] > (mass_offset_x + 100)) and \
                   d1 < 300 or d2 < 300:
                    c_node = C_HIGHLIGHT
                    amp *= 1.5
                    node_alpha = alpha_matrix * 0.9

            # Apply kinetic thermal vibration
            vib = amp * np.sin(t * node['f'] + node['p'])
            # Vibration happens largely orthogonally to the spheres, or randomly
            active_p = base_p + np.array([vib, vib*0.5, vib*0.5])
            
            proj = np.dot(active_p, sys_rotation.T)
            res = get_projection(proj)
            if res:
                # Size inversely proportional to depth
                size = max(2.0, (1500.0 / res[2])) * 0.8
                render_queue.append({'type': 'pt', 'd': res[2], 'x': res[0], 'y': res[1] + y_shift, 
                                     'c': mcolors.to_rgba(c_node, np.clip(node_alpha, 0, 1)), 's': size})

    # 4. DEPTH SORT AND RENDER
    # ------------------------
    render_queue.sort(key=lambda item: item['d'], reverse=True)

    for item in render_queue:
        if item['type'] == 'poly':
            ax.add_patch(patches.Polygon(item['pts'], facecolor=item['c'], edgecolor='none', zorder=50))
        elif item['type'] == 'pt':
            ax.scatter(item['x'], item['y'], color=item['c'], s=item['s'], edgecolors='none', zorder=50)

    # ====================================================
    # 5. VISUAL TELEMETRY AND INFORMATION OVERLAYS
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_BG, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=2, zorder=81)

    ax.text(-500, 890, "LG-356 :: ENTROPIC GRAVITY", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "EMERGENT FORCES // THERMODYNAMIC STATISTICAL PRESSURE", color='#555555', fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_BG, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=2, zorder=81)

    # Dynamic Descriptive Text
    if t < T_MATRIX_IN:
        s1, c1 = "MACROSCOPIC VIEW: SOLID SPHERES", C_TEXT
        s2, c2 = "APPARENT ATTRACTION IN PROGRESS", C_MASS
        t_state = "PERCEPTION: INVISIBLE FUNDAMENTAL FORCE \"PULLING\""
    elif t < T_PUSH_START:
        s1, c1 = "REVEALING UNDERLYING INFORMATION MATRIX", C_ENTROPY_H
        s2, c2 = "CALCULATING MICROSTATE DENSITY", C_TEXT
        t_state = "OBSERVATION: HIGH EXTERNAL ENTROPY, LOW INTERNAL ENTROPY"
    elif t < T_PUSH_END:
        s1, c1 = "THERMODYNAMIC PRESSURE DIFFERENTIAL", C_HIGHLIGHT
        s2, c2 = "UNIVERSE MAXIMIZING GLOBAL ENTROPY", C_ENTROPY_H
        t_state = "MASSES ARE ROUTED INWARD BY EXTERNAL STATISTICAL PUSH"
    else:
        s1, c1 = "GRAVITY WELL CONDENSED", C_MASS
        s2, c2 = "MACROSCOPIC REALITY RESTORED", C_TEXT
        t_state = "CONCLUSION: GRAVITY IS AN EMERGENT THERMODYNAMIC ILLUSION"

    ax.text(-500, -760, "SYS_01 [OPTICAL RESOLUTION] :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(30, -760, s1, color=c1, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [SYSTEM METRICS]     :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(30, -800, s2, color=c2, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "SCIENTIFIC AUDIT            :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(30, -840, t_state, color=C_TEXT, fontsize=14, fontname='monospace', zorder=82)

    # Seamless Transition Progress Bar
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 4, facecolor='#E5E7EB', zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 4, facecolor=C_TEXT, zorder=83))

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
    print(f"LG-356: ENTROPIC GRAVITY [CORES: {cpu_cores}] [RENDERING THERMODYNAMICS]")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
