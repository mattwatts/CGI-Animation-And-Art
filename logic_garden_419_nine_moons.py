"""
PROJECT: Logic Garden 419 (The Nine Moons Tensor)
FORMAT: YouTube Shorts (1080x1920)
METADATA: MOONS, GANYMEDE, TITAN, KINEMATICS, ASTROPHYSICS, SOLAR SYSTEM
EXECUTION: 24.0s Seamless Loop Sequence. Iso-scaled true 3D Comparative Matrices (3x3 Grid).
RULES ENFORCED:
- Daylight Palette (White Substrate / High-Contrast Chrome).
- Phase-Locked Metaphor: Exact internal thermodynamic architectures.
- Exact realisational aspect of stationary cutaways perfectly tracking to the viewer.
- TATHĀTĀ LOOP: Rotations locked to K-Multiplier relative to true tidal locking speeds.
- Explicit Physical Rotational Axis Vectors.
- COPLANAR CAMERA ANCHORING: Strict isometric scale retention across 9 separated nodes.
- Australian spelling conventions enforced natively (Maths, Colour, Optimise, Kilometres).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
from matplotlib.collections import PolyCollection
import multiprocessing as mp
import os
import gc

# ======== SEQUENCE PARAMETERS ========
FPS = 60
DURATION = 24.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_419_nine_moons"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG    = '#FFFFFF'
C_TEXT  = '#111115'
C_GUI   = '#64748B'
C_AXIS  = '#111115' # Indestructible Black for the polar rotation axis

LIGHT_DIR = np.array([-0.6, 0.7, -0.4])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

# ------------------------------------------------------------------
# MATRIX OPERATIONS
# ------------------------------------------------------------------
def rx(deg):
    rad = np.radians(deg); c, s = np.cos(rad), np.sin(rad)
    return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def ry(deg):
    rad = np.radians(deg); c, s = np.cos(rad), np.sin(rad)
    return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def rz(deg):
    rad = np.radians(deg); c, s = np.cos(rad), np.sin(rad)
    return np.array([[c,-s,0],[s,c,0],[0,0,1]])

# ------------------------------------------------------------------
# 9-NODE MINOR PLANET ARCHITECTURE (EXACT SCALES & COPLANAR ANCHORS)
# ------------------------------------------------------------------
cam_pitch = -26.0
cam_angle = 45.0
M_cam = rx(cam_pitch) @ ry(cam_angle)
M_inv = M_cam.T
cam_dist = 2200.0

# Base factor to map 2634 km to 140 visual units
SCALE_F = 140.0 / 2634.0 

# Structure: 
# 'NAME': [True_Rad_KM, Planet, Period(Day), Scaled_R, Core_R, Mantle_R, [Scr_X, Scr_Y], C_Core, C_Mantle, C_Crust, C_Node, Tilt, K_Mult]
DATA_MATRIX = {
    'GANYMEDE': [2634, 'JUPITER', 7.1,  2634*SCALE_F,  800*SCALE_F, 1600*SCALE_F, [-340,  560], '#1E293B', '#111115', '#64748B', '#E2E8F0', 5.0,  2],
    'TITAN':    [2575, 'SATURN',  15.9, 2575*SCALE_F, 1700*SCALE_F, 2300*SCALE_F, [   0,  560], '#334155', '#005599', '#CC6600', '#FFB300', -8.0, 1],
    'CALLISTO': [2410, 'JUPITER', 16.7, 2410*SCALE_F, 1200*SCALE_F, 1200*SCALE_F, [ 340,  560], '#111115', '#111115', '#475569', '#94A3B8', 12.0, 1],
    'IO':       [1821, 'JUPITER', 1.7,  1821*SCALE_F,  900*SCALE_F, 1820*SCALE_F, [-340,   50], '#1E293B', '#B45309', '#EAB308', '#DF0000', 8.0,  7],
    'MOON':     [1737, 'EARTH',   27.3, 1737*SCALE_F,  330*SCALE_F, 1730*SCALE_F, [   0,   50], '#111115', '#475569', '#94A3B8', '#E2E8F0', 1.5,  1],
    'EUROPA':   [1560, 'JUPITER', 3.5,  1560*SCALE_F,  600*SCALE_F, 1400*SCALE_F, [ 340,   50], '#1E293B', '#B45309', '#FFFFFF', '#DE008A', 22.0, 4],
    'TRITON':   [1353, 'NEPTUNE', -5.8, 1353*SCALE_F,  950*SCALE_F,  950*SCALE_F, [-340, -460], '#1E293B', '#1E293B', '#FBCFE8', '#00D2FF', -15.0,-3], # Retrograde
    'TITANIA':  [ 788, 'URANUS',  8.7,   788*SCALE_F,  480*SCALE_F,  480*SCALE_F, [   0, -460], '#111115', '#111115', '#475569', '#94A3B8', -2.0, 2],
    'RHEA':     [ 764, 'SATURN',  4.5,   764*SCALE_F,  380*SCALE_F,  380*SCALE_F, [ 340, -460], '#1E293B', '#1E293B', '#E2E8F0', '#FFFFFF', 4.0,  3],
}

print(f"PHASE 1: 3X3 MOON KINEMATIC MATRICES COMPILED. SCALE CONSTANT: {SCALE_F:.4f}")

# ------------------------------------------------------------------
# O(N) PHYSICAL HARDWARE GEOMETRY FACTORY
# ------------------------------------------------------------------
def generate_wedge_shell(r, t_min, t_max, res_phi=20, res_theta=24):
    if r < 1.0: return []
    phi = np.linspace(0, np.pi, res_phi)
    theta = np.linspace(t_min, t_max, res_theta)
    P, T = np.meshgrid(phi, theta)
    X = r * np.sin(P) * np.cos(T)
    Y = r * np.cos(P)
    Z = r * np.sin(P) * np.sin(T)
    
    faces = []
    for i in range(res_theta - 1):
        for j in range(res_phi - 1):
            p1 = np.array([X[i][j],     Y[i][j],     Z[i][j]])
            p2 = np.array([X[i+1][j],   Y[i+1][j],   Z[i+1][j]])
            p3 = np.array([X[i+1][j+1], Y[i+1][j+1], Z[i+1][j+1]])
            p4 = np.array([X[i][j+1],   Y[i][j+1],   Z[i][j+1]])
            faces.append([p1, p2, p3, p4])
    return faces

def generate_cut_wall(theta, r_min, r_max, res_phi=16, res_r=2):
    if r_max < 1.0: return []
    phi = np.linspace(0, np.pi, res_phi)
    r_arr = np.linspace(max(0.1, r_min), r_max, res_r)
    P, R = np.meshgrid(phi, r_arr)
    X = R * np.sin(P) * np.cos(theta)
    Y = R * np.cos(P)
    Z = R * np.sin(P) * np.sin(theta)
    
    faces = []
    for i in range(res_r - 1):
        for j in range(res_phi - 1):
            p1 = np.array([X[i][j],     Y[i][j],     Z[i][j]])
            p2 = np.array([X[i+1][j],   Y[i+1][j],   Z[i+1][j]])
            p3 = np.array([X[i+1][j+1], Y[i+1][j+1], Z[i+1][j+1]])
            p4 = np.array([X[i][j+1],   Y[i][j+1],   Z[i][j+1]])
            faces.append([p1, p2, p3, p4])
    return faces

def generate_particle(center, size):
    r = size / 2.0
    v = np.array([[0, r, 0], [0, -r, 0], [r, 0, 0], [-r, 0, 0], [0, 0, r], [0, 0, -r]])
    f_idx = [[0, 2, 4], [0, 4, 3], [0, 3, 5], [0, 5, 2], [1, 4, 2], [1, 3, 4], [1, 5, 3], [1, 2, 5]]
    return [v[f] + center for f in f_idx]

# ------------------------------------------------------------------
# KINEMATIC TOPOLOGY SEEDING
# ------------------------------------------------------------------
np.random.seed(419)
def seed_surface_nodes(n_pts, r_val):
    rad = np.full(n_pts, r_val + 1.2)
    phi = np.arccos(np.random.uniform(-0.95, 0.95, n_pts))
    theta = np.random.uniform(0, 2 * np.pi, n_pts)
    return rad, phi, theta

N_CRUST = 300 
NODE_ARRAYS = {}

for name, data in DATA_MATRIX.items():
    NODE_ARRAYS[name] = seed_surface_nodes(N_CRUST, data[3])

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f_idx):
    t_sec = f_idx / float(FPS)
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.]); ax.set_axis_off(); fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540); ax.set_ylim(-960, 960)

    T_MIN = 0.0
    T_MAX = 3.0 * np.pi / 2.0

    faces_collected = []
    face_colors = []
    centroids_z = []
    
    # Render visible axis vectors
    ax_lines_2d = []

    def process_layer(f_faces, h_color, pos_offset, M_tilt=None):
        c_rgb = np.array(mcolors.to_rgb(h_color))
        for face in f_faces:    
            if M_tilt is not None:
                face_xform = np.einsum('ij,nj->ni', M_tilt, face)
            else:
                face_xform = np.copy(face)

            v1 = face_xform[1] - face_xform[0]
            v2 = face_xform[2] - face_xform[0]
            norm = np.cross(v1, v2)
            n_len = np.linalg.norm(norm)
            if n_len > 0: norm /= n_len
            
            diff = 0.35 + 0.65 * np.clip(np.dot(norm, LIGHT_DIR), 0, 1)
            fc = np.append(c_rgb * diff, 1.0)
            
            f_offset = face_xform + pos_offset
            v_cam = np.einsum('ij,nj->ni', M_cam, f_offset)
            v_cam[:, 2] += cam_dist
            
            if np.any(v_cam[:, 2] < 10.0): continue
            
            px = 1800.0 * (v_cam[:, 0] / v_cam[:, 2])
            py = 1800.0 * (v_cam[:, 1] / v_cam[:, 2])
            
            faces_collected.append(np.stack((px, py), axis=-1))
            face_colors.append(fc)
            centroids_z.append(np.mean(v_cam[:, 2]))

    def process_kinematic_nodes(dr, dphi, dtheta, v_spin, pos, h_col, M_tilt):
        for i in range(len(dr)):
            cur_t = (dtheta[i] + np.radians(v_spin)) % (2 * np.pi)
            if cur_t <= T_MAX:  # Vanish inside internal core cutaway void
                x = dr[i] * np.sin(dphi[i]) * np.cos(cur_t)
                y = dr[i] * np.cos(dphi[i])
                z = dr[i] * np.sin(dphi[i]) * np.sin(cur_t)
                p_f = generate_particle(np.array([x, y, z]), 3.0)
                process_layer(p_f, h_col, pos, M_tilt=M_tilt)

    # ================= LOOP 9-NODE PHYSICAL MATRICES =================
    for name, data in DATA_MATRIX.items():
        (true_km, home_p, p_days, s_r, c_r, m_r, s_pos, 
         c_core, c_mantle, c_crust, c_node, tilt_d, k_m) = data
        
        world_p = M_inv @ np.array([s_pos[0], s_pos[1], 0.0])
        MT = rx(tilt_d) # Axial tilt applies specifically to the crust/mantle/axis

        # 1. CORE (Geometrically locked to cutaway, un-tilted so cutaway remains strictly Coplanar)
        if c_r > 1.0:
            c_sh = generate_wedge_shell(c_r, T_MIN, T_MAX)
            c_w1 = generate_cut_wall(T_MIN, 0.0, c_r)
            c_w2 = generate_cut_wall(T_MAX, 0.0, c_r)
            process_layer(c_sh + c_w1 + c_w2, c_core, world_p, M_tilt=None)

        # 2. MANTLE (If differentiated)
        if m_r > c_r:
            m_sh = generate_wedge_shell(m_r, T_MIN, T_MAX)
            m_w1 = generate_cut_wall(T_MIN, c_r, m_r)
            m_w2 = generate_cut_wall(T_MAX, c_r, m_r)
            process_layer(m_sh + m_w1 + m_w2, c_mantle, world_p, M_tilt=None)

        # 3. CRUST 
        r_sh = generate_wedge_shell(s_r, T_MIN, T_MAX)
        r_w1 = generate_cut_wall(T_MIN, m_r, s_r)
        r_w2 = generate_cut_wall(T_MAX, m_r, s_r)
        process_layer(r_sh + r_w1 + r_w2, c_crust, world_p, M_tilt=None)

        # 4. KINEMATIC ROTATION (Nodes spin exactly around tilted axis)
        dr, dphi, dtheta = NODE_ARRAYS[name]
        spin_v = t_sec * (k_m * 15.0) # Seamless loop: 360 degrees inside 24s window * K multiplier
        process_kinematic_nodes(dr, dphi, dtheta, spin_v, world_p, c_node, MT)

        # 5. VISIBLE PHYSICAL AXIS LINE
        # Piercing the poles. Sticking out 30 units past the crust.
        ax_top = MT @ np.array([0, s_r + 35.0, 0]) + world_p
        ax_bot = MT @ np.array([0, -(s_r + 35.0), 0]) + world_p
        
        # Camera transform the explicit line
        l_pts = np.array([ax_top, ax_bot])
        v_cam = np.einsum('ij,nj->ni', M_cam, l_pts)
        v_cam[:, 2] += cam_dist
        px = 1800.0 * (v_cam[:, 0] / v_cam[:, 2])
        py = 1800.0 * (v_cam[:, 1] / v_cam[:, 2])
        ax_lines_2d.append([(px[0], py[0]), (px[1], py[1])])

        # 6. SCALED HUD TARGETING
        scale_mod = 1800.0 / cam_dist
        th_p = s_pos[0] * scale_mod
        tv_p = s_pos[1] * scale_mod - (s_r * scale_mod) - 25.0
        
        ax.text(th_p, tv_p, name, color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', ha='center', zorder=85)
        ax.text(th_p, tv_p - 18, f"{home_p}", color=c_crust, fontsize=11, fontname='monospace', weight='bold', ha='center', zorder=85)
        ax.text(th_p, tv_p - 32, f"P:{p_days}d [K:{k_m}]", color=c_node, fontsize=9, fontname='monospace', weight='bold', ha='center', zorder=85)

    # ================= 7. ABSOLUTE DEPENDENCY SORT & RENDER =================
    # Draw rotation axes (behind the planet shells theoretically, but overdrawn so it pierces visually)
    for line in ax_lines_2d:
        ax.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], color=C_AXIS, lw=2.0, zorder=50)

    # Z-Sort polygons
    sort_idx = np.argsort(centroids_z)[::-1] 
    if faces_collected:
        sorted_faces = [faces_collected[i] for i in sort_idx]
        sorted_fcs = [face_colors[i] for i in sort_idx]
        ax.add_collection(PolyCollection(sorted_faces, facecolors=sorted_fcs, edgecolors='#111115', linewidths=0.2, joinstyle='miter', zorder=60))

    # ================= 8. HIGH-DENSITY HUD & TELEMETRY =================
    ax.add_patch(Rectangle((-540, 800), 1080, 160, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=3, zorder=81)
    ax.text(-500, 900, "LG-419 :: THE NINE MOONS TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 850, "[SFI-1.00] EXACT COMPARATIVE RADII & KINEMATIC LOOP", color=C_GUI, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    prog = t_sec / DURATION
    if t_sec < 12.0:
        state_msg = "PHASE 1: THE TATHATA K-MULTIPLIER"
        state_col = '#1E293B'
        active_op = "SEAMLESS ROTATION ENFORCING RELATIVE TIDAL VELOCITIES."
    else:
        state_msg = "PHASE 2: INTERNAL THERMO-DIAGNOSTICS"
        state_col = '#CC6600'
        active_op = "EXPLICIT CORE/MANTLE ARCHITECTURE MAPPED TO CUTAWAYS."

    ax.text(-500, -780, f"PROTOCOL STATE : {state_msg}", color=state_col, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"DIAGNOSTIC     : {active_op}", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"AXIOMATIC TRUTH: VISUALISE THE MASSIVE SCALE VARIANCE OF SATELLITE MECHANICS.", color=C_TEXT, fontsize=11, fontname='monospace', zorder=82)

    ax.add_patch(Rectangle((-500, -920), 1000, 8, facecolor=C_GUI, zorder=82))
    ax.add_patch(Rectangle((-500, -920), 1000 * prog, 8, facecolor=state_col, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f_idx:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f_idx

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-419: NINE MOONS TENSOR ENGAGED [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            pass
    print("Compilation Complete. 9x Node Matrix resolved to exact physical volume.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
