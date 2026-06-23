"""
PROJECT: Logic Garden 361 (The Relativistic Whip // Sagittarius A* & S2)
FORMAT: YouTube Shorts (1080x1920)
METADATA: ORBITAL MECHANICS, RELATIVITY, SAGITTARIUS A*, KINEMATICS
EXECUTION: Continuous 24.0s Sequence. True 3D Z-Depth Engine. Daylight Palette.
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
OUT_DIR = "frames_361_sgr_a_orbit"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- VISUAL PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#D1D5DB'   # The Spacetime Topology Mesh
C_WARP      = '#9CA3AF'   # Deep Gravity Well
C_SINGULAR  = '#000000'   # The Absolute Coordinate Origin
C_PHOTON    = '#FFB300'   # Photon Ring (Gold)
C_STAR      = '#00D2FF'   # S2 Star (Brilliant Cyan)
C_TRAIL     = '#DE008A'   # Kinetic Spallation / Heat Wake (Magenta)

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

def get_projection(pt_3d, focal_length=1500.0, cam_dist=2000.0):
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
# KINEMATIC MATH: KEPLER'S EQUATION (Numerical Solver)
# ------------------------------------------------------------------
def solve_kepler(M, e, tol=1e-6, max_iter=10):
    """Solves Kepler's equation M = E - e*sin(E) for Eccentric Anomaly (E)"""
    E = M
    for _ in range(max_iter):
        delta_E = (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
        E -= delta_E
        if abs(delta_E) < tol: break
    return E

# Orbit Parameters (Scaled for the matrix)
O_ECCENTRICITY = 0.88    # Highly elliptical, just like S2
O_SEMIMAJOR = 650.0      # Scale
O_PERIOD = 24.0          # Synced to video length
T_PERIAPSIS = 14.5       # The exact second of maximum kinetic velocity

def get_star_position(t):
    # Mean Anomaly
    M = (2.0 * np.pi / O_PERIOD) * (t - T_PERIAPSIS)
    E = solve_kepler(M, O_ECCENTRICITY)
    
    # 2D Orbital Plane Coordinates (Focus is at 0,0)
    x_orbit = O_SEMIMAJOR * (np.cos(E) - O_ECCENTRICITY)
    y_orbit = O_SEMIMAJOR * np.sqrt(1.0 - O_ECCENTRICITY**2) * np.sin(E)
    
    # Rotate the orbital plane to make it visually dynamic (Inclination & Argument of Periapsis)
    p_3d = np.array([x_orbit, 0, y_orbit])
    p_3d = np.dot(p_3d, rotate_x(np.radians(25)).T)
    p_3d = np.dot(p_3d, rotate_z(np.radians(35)).T)
    return p_3d

# Pre-calculate the entire orbit path for the baseline rendering
orbit_path = []
for t_sim in np.linspace(0, 24, 200):
    orbit_path.append(get_star_position(t_sim))
orbit_path = np.array(orbit_path)

# ------------------------------------------------------------------
# SPACETIME GRAVITY WELL GENERATION
# ------------------------------------------------------------------
g_size = 40
g_bound = 1200
x_grid = np.linspace(-g_bound, g_bound, g_size)
z_grid = np.linspace(-g_bound, g_bound, g_size)

grid_pts = []
for x in x_grid:
    for z in z_grid:
        r = np.sqrt(x**2 + z**2)
        # Deep hyperbolic warp pushing down at the singularity
        y = -100000.0 / (r + 150.0) + 150.0 
        y = np.clip(y, -1200, 0)
        grid_pts.append(np.array([x, y, z]))
grid_lines_x = []
grid_lines_z = []

# Construct lines along X
for i in range(g_size):
    line = []
    for j in range(g_size):
        line.append(grid_pts[i*g_size + j])
    grid_lines_x.append(line)
# Construct lines along Z
for j in range(g_size):
    line = []
    for i in range(g_size):
        line.append(grid_pts[i*g_size + j])
    grid_lines_z.append(line)


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

    # 1. KINEMATIC CAMERA TIMELINE
    # ----------------------------
    # Slowly orbit the scene
    pitch = np.radians(-25 + 5 * np.sin(t * 0.2))
    yaw = np.radians(t * 4.0)
    sys_rotation = rotate_x(pitch) @ rotate_y(yaw)
    y_shift = -50
    
    render_queue = []

    # 2. RENDER THE SPACETIME TOPOLOGY (Gravity Well)
    # -----------------------------------------------
    def push_grid_lines(lines_array):
        for line in lines_array:
            line_arr = np.array(line)
            proj = np.dot(line_arr, sys_rotation.T)
            sz = []
            cams = []
            for p in proj:
                res = get_projection(p)
                if res:
                    sz.append([res[0], res[1] + y_shift])
                    cams.append(res[2])
            
            # Draw line segments to apply color gradient based on Depth (Y)
            if len(sz) > 1:
                for idx in range(len(sz)-1):
                    deep_ratio = np.clip(-line_arr[idx][1] / 800.0, 0, 1)
                    c_line = lerp_color(C_GRID, C_WARP, deep_ratio)
                    alpha = 1.0 if deep_ratio < 0.95 else 0.0 # Cut off exactly at the singularity
                    if alpha > 0:
                        render_queue.append({
                            'type': 'line', 'd': (cams[idx] + cams[idx+1])/2, 'pts': [sz[idx], sz[idx+1]], 
                            'c': c_line, 'lw': 1.0
                        })

    push_grid_lines(grid_lines_x)
    push_grid_lines(grid_lines_z)

    # 3. RENDER THE SINGULARITY (Sagittarius A*)
    # ------------------------------------------
    sg_pos = np.array([0, -850, 0])
    proj_sg = np.dot(sg_pos, sys_rotation.T)
    res_sg = get_projection(proj_sg)
    if res_sg:
        sc = 1500.0 / res_sg[2]
        # The Event Horizon Void
        render_queue.append({
            'type': 'pt', 'd': res_sg[2], 'x': res_sg[0], 'y': res_sg[1] + y_shift,
            'c': C_SINGULAR, 's': 60 * sc, 'm': 'o', 'alpha': 1.0
        })
        # The Photon Ring
        render_queue.append({
            'type': 'pt', 'd': res_sg[2] + 1, 'x': res_sg[0], 'y': res_sg[1] + y_shift,
            'c': C_PHOTON, 's': 100 * sc, 'm': 'o', 'alpha': 0.3
        })
        render_queue.append({
            'type': 'pt', 'd': res_sg[2] + 2, 'x': res_sg[0], 'y': res_sg[1] + y_shift,
            'c': C_PHOTON, 's': 80 * sc, 'm': 'o', 'alpha': 0.8
        })

    # 4. RENDER THE ORBITAL PATH
    # --------------------------
    proj_path = np.dot(orbit_path, sys_rotation.T)
    s_path = []
    c_path = []
    for p in proj_path:
        res = get_projection(p)
        if res:
            s_path.append([res[0], res[1] + y_shift])
            c_path.append(res[2])
    
    if len(s_path) > 1:
        for idx in range(len(s_path)-1):
            render_queue.append({
                'type': 'line', 'd': c_path[idx], 'pts': [s_path[idx], s_path[idx+1]], 
                'c': mcolors.to_rgba(C_GRID, 0.4), 'lw': 1.0
            })

    # 5. RENDER THE S2 STAR & KINEMATIC SPALLATION
    # --------------------------------------------
    # Calculate exact velocity vector
    dt = 0.1
    p_now = get_star_position(t)
    p_prev = get_star_position(t - dt)
    velocity_vec = (p_now - p_prev) / dt
    speed = np.linalg.norm(velocity_vec)
    
    # Scale speed for telemetry display (Maxes out around 8000 for realistic metric)
    display_speed = (speed / 50.0) * 8000.0

    # Number of trail particles directly scales with kinetic speed mapping the "relativistic whip"
    num_trails = int(np.clip(speed / 8.0, 0, 30))
    
    for i in range(num_trails):
        # We sample points slightly backward in time to form the heat wake
        hist_t = t - (i * 0.05)
        if hist_t < 0: hist_t += 24.0
        hist_p = get_star_position(hist_t)
        
        proj_h = np.dot(hist_p, sys_rotation.T)
        res_h = get_projection(proj_h)
        if res_h:
            sc = 1500.0 / res_h[2]
            alpha_trail = 1.0 - (i / max(1, num_trails))
            render_queue.append({
                'type': 'pt', 'd': res_h[2], 'x': res_h[0], 'y': res_h[1] + y_shift,
                'c': C_TRAIL, 's': 12 * sc * alpha_trail, 'm': 'o', 'alpha': alpha_trail * 0.8
            })

    # Render True Center of S2
    proj_now = np.dot(p_now, sys_rotation.T)
    res_now = get_projection(proj_now)
    if res_now:
        sc = 1500.0 / res_now[2]
        # Core
        render_queue.append({
            'type': 'pt', 'd': res_now[2]-1, 'x': res_now[0], 'y': res_now[1] + y_shift,
            'c': C_BG, 's': 20 * sc, 'm': 'o', 'alpha': 1.0
        })
        # Corona
        render_queue.append({
            'type': 'pt', 'd': res_now[2], 'x': res_now[0], 'y': res_now[1] + y_shift,
            'c': C_STAR, 's': 35 * sc, 'm': 'o', 'alpha': 0.9
        })


    # 6. ORTHOGRAPHIC Z-DEPTH DISPATCH
    # --------------------------------
    render_queue.sort(key=lambda item: item['d'], reverse=True)

    for item in render_queue:
        if item['type'] == 'line':
            pts = item['pts']
            ax.plot([pts[0][0], pts[1][0]], [pts[0][1], pts[1][1]], color=item['c'], lw=item['lw'], zorder=50)
        elif item['type'] == 'pt':
            ax.scatter(item['x'], item['y'], color=item['c'], s=item['s'], alpha=item.get('alpha', 1.0), edgecolors='none', zorder=50)

    # ====================================================
    # 7. TELEMETRY AND HUD WIDGETS
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_BG, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=2, zorder=81)

    ax.text(-500, 890, "LG-361 :: THE RELATIVISTIC WHIP", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "SAGITTARIUS A* // S2 ORBITAL KINEMATICS", color='#555555', fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_BG, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=2, zorder=81)

    # Narrative Telemetry Mapping
    if t < 8.0:
        s1, c1 = "APOCENTER DRIFT", C_STAR
        s2, c2 = "NOMINAL SPACETIME TOPOLOGY", C_GRID
        t_state = "S-STAR NAVIGATING OUTER ORBIT AT MINIMUM VELOCITY"
    elif t < 13.0:
        s1, c1 = "GRAVITATIONAL PLUNGE DETECTED", C_TEXT
        s2, c2 = "ENTERING SEVERE TOPOLOGICAL WARP", C_WARP
        t_state = "ACCELERATION SPIKING DUE TO EXTREME MASS GRADIENT"
    elif t < 16.0:
        s1, c1 = "PERIAPSIS // CLOSEST APPROACH", C_TRAIL
        s2, c2 = "MAXIMUM KINETIC SPALLATION", C_PHOTON
        t_state = "EXTREME MATHEMATICAL WHIP AROUND THE SINGULARITY"
    else:
        s1, c1 = "KINETIC EGRESS", C_STAR
        s2, c2 = "ESCAPING THE GRAVITY WELL", C_TEXT
        t_state = "S-STAR SURVIVED ENCOUNTER. DECELERATING TO OUTER ORBIT."

    ax.text(-500, -760, "SYS_01 [ORBITAL PHASE]   :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(60, -760, s1, color=c1, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [ENVIRONMENT]     :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(60, -800, s2, color=c2, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    # Dynamic Velocity Widget
    ax.text(-500, -840, "KINETIC VELOCITY TENSOR  :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    v_color = C_TRAIL if display_speed > 4000 else C_TEXT
    ax.text(60, -840, f"{display_speed:,.0f} KM/S", color=v_color, fontsize=16, fontname='monospace', weight='bold', zorder=82)

    # Seamless Transition Progress Bar
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 4, facecolor='#E5E7EB', zorder=82))
    
    prog_c = C_STAR
    if display_speed > 3000: prog_c = C_TRAIL
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 4, facecolor=prog_c, zorder=83))

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
    print(f"LG-361: THE RELATIVISTIC WHIP [CORES: {cpu_cores}] [RENDERING KEPLERIAN ORBIT]")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
