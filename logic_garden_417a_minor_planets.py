"""
PROJECT: Logic Garden 417 (The Minor Planet Tensor // Trans-Neptunian Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: PLUTO, ERIS, MINOR PLANETS, ASTROPHYSICS, KINEMATICS, DWARF PLANETS
EXECUTION: 24.0s Sequence. Iso-scaled true 3D Comparative Matrices (3x3 Grid).
RULES ENFORCED:
- Daylight Palette (White Substrate / High-Contrast Chrome).
- Phase-Locked Metaphor: The hydrostatic equilibrium limit.
- Exact realisational aspect of stationary cutaways perfectly tracking to the viewer.
- Planetary Radius corresponds exactly with the relative astronomical physical radius.
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
OUT_DIR = "frames_417_dwarf_planets"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG    = '#FFFFFF'
C_TEXT  = '#111115'
C_GUI   = '#64748B'

LIGHT_DIR = np.array([-0.6, 0.7, -0.4])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

# ------------------------------------------------------------------
# MATRIX OPERATIONS
# ------------------------------------------------------------------
def rx(deg):
    rad = np.radians(deg); c, s = np.cos(rad), np.sin(rad)
    return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def ry(rad):
    c, s = np.cos(rad), np.sin(rad)
    return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def rz(rad):
    c, s = np.cos(rad), np.sin(rad)
    return np.array([[c,-s,0],[s,c,0],[0,0,1]])

# ------------------------------------------------------------------
# 9-NODE MINOR PLANET ARCHITECTURE (EXACT SCALES & COPLANAR ANCHORS)
# ------------------------------------------------------------------
cam_pitch = -26.0  
cam_angle = 45.0   
M_cam = rx(cam_pitch) @ ry(cam_angle)
M_inv = M_cam.T
cam_dist = 2200.0 

# Structure: [True_Radius_KM, Scaled_Radius, Core_Radius, [Screen_X, Screen_Y], C_Core, C_Crust, C_Node, Spin_Speed]
DATA_MATRIX = {
    'PLUTO':    [1188, 175.0, 115.0, [-340,  560], '#1E293B', '#B45309', '#FFB300', 4.0],
    'ERIS':     [1163, 171.3, 110.0, [   0,  560], '#111115', '#E2E8F0', '#00D2FF', 3.5],
    'MAKEMAKE': [ 715, 105.3,  70.0, [ 340,  560], '#1A202C', '#CC6600', '#FF3300', 6.0],
    'CHARON':   [ 606,  89.2,  50.0, [-340,   50], '#111115', '#94A3B8', '#DE008A', 5.5],
    'QUAOAR':   [ 555,  81.7,  45.0, [   0,   50], '#1E293B', '#64748B', '#00C853', 5.0],
    'SEDNA':    [ 497,  73.1,  40.0, [ 340,   50], '#111115', '#DF0000', '#FFB300', 4.2],
    'CERES':    [ 473,  69.6,  40.0, [-340, -460], '#020617', '#475569', '#E2E8F0', 7.0],
    'ORCUS':    [ 458,  67.4,  38.0, [   0, -460], '#1E293B', '#005599', '#00D2FF', 6.5],
    'SALACIA':  [ 423,  62.2,  35.0, [ 340, -460], '#111115', '#334155', '#94A3B8', 6.0],
}

print(f"PHASE 1: 3X3 HYDROSTATIC EQUILIBRIUM MATRICES COMPILED. Z-DEPTH SWAY NEUTRALISED.")

# ------------------------------------------------------------------
# O(N) PHYSICAL HARDWARE GEOMETRY FACTORY
# ------------------------------------------------------------------
def generate_wedge_shell(r, t_min, t_max, res_phi=20, res_theta=24):
    phi = np.linspace(0, np.pi, res_phi)
    theta = np.linspace(t_min, t_max, res_theta)
    P, T = np.meshgrid(phi, theta)
    X = r * np.sin(P) * np.cos(T)
    Y = r * np.cos(P)
    Z = r * np.sin(P) * np.sin(T)
    
    faces = []
    for i in range(res_theta - 1):
        for j in range(res_phi - 1):
            p1 = np.array([X[i][j], Y[i][j], Z[i][j]])
            p2 = np.array([X[i+1][j], Y[i+1][j], Z[i+1][j]])
            p3 = np.array([X[i+1][j+1], Y[i+1][j+1], Z[i+1][j+1]])
            p4 = np.array([X[i][j+1], Y[i][j+1], Z[i][j+1]])
            faces.append([p1, p2, p3, p4])
    return faces

def generate_cut_wall(theta, r_min, r_max, res_phi=16, res_r=2):
    phi = np.linspace(0, np.pi, res_phi)
    r_arr = np.linspace(r_min, r_max, res_r)
    P, R = np.meshgrid(phi, r_arr)
    X = R * np.sin(P) * np.cos(theta)
    Y = R * np.cos(P)
    Z = R * np.sin(P) * np.sin(theta)
    
    faces = []
    for i in range(res_r - 1):
        for j in range(res_phi - 1):
            p1 = np.array([X[i][j], Y[i][j], Z[i][j]])
            p2 = np.array([X[i+1][j], Y[i+1][j], Z[i+1][j]])
            p3 = np.array([X[i+1][j+1], Y[i+1][j+1], Z[i+1][j+1]])
            p4 = np.array([X[i][j+1], Y[i][j+1], Z[i][j+1]])
            faces.append([p1, p2, p3, p4])
    return faces

def generate_particle(center, size):
    r = size / 2.0
    v = np.array([[0, r, 0], [0, -r, 0], [r, 0, 0], [-r, 0, 0], [0, 0, r], [0, 0, -r]])
    f_idx = [[0, 2, 4], [0, 4, 3], [0, 3, 5], [0, 5, 2], [1, 4, 2], [1, 3, 4], [1, 5, 3], [1, 2, 5]]
    return [v[f] + center for f in f_idx]

# ------------------------------------------------------------------
# KINEMATIC GEOLOGY SEEDING
# ------------------------------------------------------------------
np.random.seed(417)
def seed_surface_nodes(n_pts, r_val):
    rad = np.full(n_pts, r_val + 1.5)
    phi = np.arccos(np.random.uniform(-0.95, 0.95, n_pts))
    theta = np.random.uniform(0, 2 * np.pi, n_pts)
    return rad, phi, theta

N_CRUST = 250  # Balanced for 9 simultaneous spheres
NODE_ARRAYS = {}
for name, data in DATA_MATRIX.items():
    NODE_ARRAYS[name] = seed_surface_nodes(N_CRUST, data[1])

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
    
    def process_layer(f_faces, h_color, pos_offset):
        c_rgb = np.array(mcolors.to_rgb(h_color))
        for face in f_faces:    
            v1 = face[1] - face[0]; v2 = face[2] - face[0]
            norm = np.cross(v1, v2)
            n_len = np.linalg.norm(norm)
            if n_len > 0: norm /= n_len
            
            diff = 0.4 + 0.6 * np.clip(np.dot(norm, LIGHT_DIR), 0, 1)
            fc = np.append(c_rgb * diff, 1.0)
            
            f_offset = face + pos_offset
            # Multiply back by M_cam guarantees standard Z-depth = 0 across 9 bodies
            v_cam = np.einsum('ij,nj->ni', M_cam, f_offset)
            v_cam[:, 2] += cam_dist
            
            if np.any(v_cam[:, 2] < 10.0): continue
            
            px = 1800.0 * (v_cam[:, 0] / v_cam[:, 2])
            py = 1800.0 * (v_cam[:, 1] / v_cam[:, 2])
            
            faces_collected.append(np.stack((px, py), axis=-1))
            face_colors.append(fc)
            centroids_z.append(np.mean(v_cam[:, 2]))

    def process_kinematic_nodes(dr, dphi, dtheta, v_spin, pos, h_col):
        for i in range(N_CRUST):
            cur_t = (dtheta[i] + np.radians(v_spin)) % (2 * np.pi)
            if cur_t <= T_MAX:  # Exclusively render ON the crust (vanish in void)
                x = dr[i] * np.sin(dphi[i]) * np.cos(cur_t)
                y = dr[i] * np.cos(dphi[i])
                z = dr[i] * np.sin(dphi[i]) * np.sin(cur_t)
                p_f = generate_particle(np.array([x, y, z]), 3.5)
                process_layer(p_f, h_col, pos)

    # LOOP 9-NODE PHYSICAL MATRICES
    for name, data in DATA_MATRIX.items():
        # Extrapolate config
        true_km, s_r, c_r, screen_pos, c_core, c_crust, c_node, spin = data
        
        # Coplanar World Position
        world_p = M_inv @ np.array([screen_pos[0], screen_pos[1], 0.0])
        
        # 1. Compile Core
        c_shell = generate_wedge_shell(c_r, T_MIN, T_MAX)
        c_w1 = generate_cut_wall(T_MIN, 0.0, c_r)
        c_w2 = generate_cut_wall(T_MAX, 0.0, c_r)
        process_layer(c_shell + c_w1 + c_w2, c_core, world_p)
        
        # 2. Compile Mantle/Crust
        m_shell = generate_wedge_shell(s_r, T_MIN, T_MAX)
        m_w1 = generate_cut_wall(T_MIN, c_r, s_r)
        m_w2 = generate_cut_wall(T_MAX, c_r, s_r)
        process_layer(m_shell + m_w1 + m_w2, c_crust, world_p)
        
        # 3. Kinematic Nodes
        dr, dphi, dtheta = NODE_ARRAYS[name]
        process_kinematic_nodes(dr, dphi, dtheta, t_sec * spin, world_p, c_node)

        # 4. Draw Scaled HUD Direct to Screen
        scale_mod = 1800.0 / cam_dist
        px = screen_pos[0] * scale_mod
        py = screen_pos[1] * scale_mod - (s_r * scale_mod) - 30.0
        
        ax.text(px, py, name, color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', ha='center', zorder=85)
        ax.text(px, py - 20, f"({true_km} KM)", color=c_crust, fontsize=11, fontname='monospace', weight='bold', ha='center', zorder=85)

    # 5. ABSOLUTE DEPENDENCY SORT & RENDER
    sort_idx = np.argsort(centroids_z)[::-1] 
    if faces_collected:
        sorted_faces = [faces_collected[i] for i in sort_idx]
        sorted_fcs = [face_colors[i] for i in sort_idx]
        ax.add_collection(PolyCollection(sorted_faces, facecolors=sorted_fcs, edgecolors='#111115', linewidths=0.25, joinstyle='miter'))


    # 6. HIGH-DENSITY HUD & TELEMETRY
    ax.add_patch(Rectangle((-540, 800), 1080, 160, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=3, zorder=81)
    ax.text(-500, 900, "LG-417 :: THE MINOR PLANET TENSORS", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 850, "[SFI-1.00] EXACT COMPARATIVE RADII (TRANS-NEPTUNIAN MATRIX)", color=C_GUI, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    prog = t_sec / DURATION
    if t_sec < 12.0:
        state_msg = "PHASE 1: THE HYDROSTATIC EQUILIBRIUM"
        state_col = '#B45309'
        active_op = "VOLUMETRIC CRUSH ENFORCED. ALL BODIES ARE MATHEMATICAL SPHERES."
    else:
        state_msg = "PHASE 2: INTERNAL THERMODYNAMICS"
        state_col = '#00D2FF'
        active_op = "SILICATE CORES WRAPPED IN AMMONIA/WATER/METHANE HYPER-ICES."

    ax.text(-500, -780, f"PROTOCOL STATE : {state_msg}", color=state_col, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"DIAGNOSTIC     : {active_op}", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"AXIOMATIC TRUTH: PLANETARY CLASSIFICATION IS LINGUISTIC. KINEMATIC GRAVITY IS ABSOLUTE.", color=C_TEXT, fontsize=11, fontname='monospace', zorder=82)

    ax.add_patch(Rectangle((-500, -920), 1000, 8, facecolor=C_GUI, zorder=82))
    ax.add_patch(Rectangle((-500, -920), 1000 * prog, 8, facecolor=state_col, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f_idx:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f_idx

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-417: MINOR PLANET TENSORS ENGAGED [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            pass
    print("Compilation Complete. 9x Node Matrix resolved to exact physical volume.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
