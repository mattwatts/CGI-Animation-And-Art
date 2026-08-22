"""
PROJECT: Logic Garden 414 (The Dual Iso-Structural Tensor // Jupiter & Saturn)
FORMAT: YouTube Shorts (1080x1920)
METADATA: JUPITER, SATURN, PLANETARY DYNAMO, KINEMATICS, ASTROPHYSICS
EXECUTION: 24.0s Sequence. Iso-scaled true 3D Mathematical Comparative Cutaways.
RULES ENFORCED:
- Daylight Palette (White Substrate / High-Contrast Chrome).
- Phase-Locked Metaphor: The mass-compression limit and internal planetary scale.
- Exact realisational aspect of stationary cutaways with spinning internal fluids.
- Australian spelling conventions enforced natively (Maths, Colour, Optimise).
- Absolute O(N) volumetric arrays with Lambertian shading and Deep-Sort.
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
OUT_DIR = "frames_414_jup_sat"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG            = '#FFFFFF'
C_TEXT          = '#111115'
C_EDGE          = '#111115'
C_CORE          = '#111115'  # Indestructible Black (Heavy Cores)

# JUPITER SPECIFICS
C_JUP_GAS       = '#1E293B'  # Carbon Slate (Outer Envelope)
C_JUP_DYN       = '#C20078'  # Deep Magenta (Crushing Metallic Hydrogen)
C_JUP_MAG       = '#FF3300'  # Intense Red (Violent Magnetic Tensor)
C_JUP_PLASMA    = '#FFB300'  # Dense Amber 

# SATURN SPECIFICS
C_SAT_GAS       = '#64748B'  # Lighter Slate (Under-dense Envelope)
C_SAT_DYN       = '#005599'  # Deep Marine (Sunken Metallic Core)
C_SAT_RING      = '#94A3B8'  # Steel (Equatorial Matrix)
C_SAT_MAG       = '#00D2FF'  # High-Contrast Cyan (Axi-symmetric Tensor)

C_GUI           = '#64748B'

LIGHT_DIR = np.array([-0.6, 0.7, -0.4])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

# ------------------------------------------------------------------
# RIGID 3D ARCHITECTURAL LAYER METRICS (SCALED)
# ------------------------------------------------------------------
# JUPITER (Extreme Mass Compression, massive dynamo)
JUP_Y           = 460.0
J_RAD_CORE      = 50.0
J_RAD_DYN       = 320.0  # 80% of radius
J_RAD_GAS       = 400.0
J_TILT          = 9.6

# SATURN (Under-dense, small sunken dynamo, massive gas shell)
SAT_Y           = -460.0
S_RAD_CORE      = 40.0
S_RAD_DYN       = 150.0  # 45% of radius
S_RAD_GAS       = 330.0
S_RING_IN       = 380.0
S_RING_OUT      = 720.0
S_TILT          = 0.0

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

def ease_in_out(t):
    return t * t * (3.0 - 2.0 * t)

# ------------------------------------------------------------------
# O(N) PHYSICAL HARDWARE GEOMETRY FACTORY
# ------------------------------------------------------------------
def generate_wedge_shell(center_y, r, t_min, t_max, res_phi=20, res_theta=28):
    phi = np.linspace(0, np.pi, res_phi)
    theta = np.linspace(t_min, t_max, res_theta)
    P, T = np.meshgrid(phi, theta)
    
    X = r * np.sin(P) * np.cos(T)
    Y = r * np.cos(P) + center_y
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

def generate_cut_wall(center_y, theta, r_min, r_max, res_phi=20, res_r=2):
    phi = np.linspace(0, np.pi, res_phi)
    r_arr = np.linspace(r_min, r_max, res_r)
    P, R = np.meshgrid(phi, r_arr)
    
    X = R * np.sin(P) * np.cos(theta)
    Y = R * np.cos(P) + center_y
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

def generate_flat_ring_segment(center_y, r_in, r_out, t_min, t_max, res_theta=30):
    theta = np.linspace(t_min, t_max, res_theta)
    faces = []
    for i in range(res_theta - 1):
        t1, t2 = theta[i], theta[i+1]
        p1 = np.array([r_in*np.cos(t1), center_y, r_in*np.sin(t1)])
        p2 = np.array([r_out*np.cos(t1), center_y, r_out*np.sin(t1)])
        p3 = np.array([r_out*np.cos(t2), center_y, r_out*np.sin(t2)])
        p4 = np.array([r_in*np.cos(t2), center_y, r_in*np.sin(t2)])
        faces.append([p1, p2, p3, p4])
    return faces

def generate_magnetic_arc(center_y, L_shell, longitude, tilt_deg=0.0, thickness=2.5, res=45):
    faces = []
    phi = np.linspace(0.08, np.pi - 0.08, res)
    pts = []
    
    R_tilt = rz(np.radians(tilt_deg))
    
    for p in phi:
        r = L_shell * (np.sin(p)**2)
        X = r * np.sin(p) * np.cos(longitude)
        Y = r * np.cos(p)
        Z = r * np.sin(p) * np.sin(longitude)
        
        vec = np.array([X, Y, Z])
        vec = np.dot(R_tilt, vec)
        vec[1] += center_y
        pts.append(vec)
        
    for i in range(len(pts) - 1):
        p1 = pts[i]; p2 = pts[i+1]
        v = p2 - p1
        length = np.linalg.norm(v)
        if length < 1e-4: continue
        v = v / length
        
        up = np.array([0., 1., 0.])
        if np.abs(v[1]) > 0.99: up = np.array([1., 0., 0.])
        
        right = np.cross(up, v)
        right = right / np.linalg.norm(right)
        real_up = np.cross(v, right)
        
        R_mat = np.column_stack((right, real_up, v))
        t = thickness / 2.0
        l = length / 2.0
        
        vv = np.array([
            [-t, -t, -l], [ t, -t, -l], [ t,  t, -l], [-t,  t, -l],
            [-t, -t,  l], [ t, -t,  l], [ t,  t,  l], [-t,  t,  l]
        ])
        f_idx = [[0,1,2,3], [4,5,6,7], [0,1,5,4], [1,2,6,5], [2,3,7,6], [3,0,4,7]]
        
        mid = (p1 + p2) / 2.0
        for face in f_idx:
            rot_face = np.dot(vv[face], R_mat.T) + mid
            faces.append(rot_face)
            
    return faces

def generate_particle(center, size):
    r = size / 2.0
    v = np.array([
        [0, r, 0], [0, -r, 0], [r, 0, 0], 
        [-r, 0, 0], [0, 0, r], [0, 0, -r]
    ])
    f_idx = [[0, 2, 4], [0, 4, 3], [0, 3, 5], [0, 5, 2],
             [1, 4, 2], [1, 3, 4], [1, 5, 3], [1, 2, 5]]
    return [v[f] + center for f in f_idx]

# ------------------------------------------------------------------
# O(N) KINEMATIC FLUID COMPILERS
# ------------------------------------------------------------------
np.random.seed(414)

def seed_fluid(n_pts, r_in, r_out):
    rad = np.random.uniform(r_in + 5, r_out - 5, n_pts)
    phi = np.arccos(np.random.uniform(-1, 1, n_pts))
    theta = np.random.uniform(0, 2 * np.pi, n_pts)
    vel = 3.0 + 5.0 * ((r_out - rad) / (r_out - r_in)) 
    return rad, phi, theta, vel

J_N_PTS = 800
S_N_PTS = 300

J_DR, J_DPHI, J_DTHETA, J_DVEL = seed_fluid(J_N_PTS, J_RAD_CORE, J_RAD_DYN)
S_DR, S_DPHI, S_DTHETA, S_DVEL = seed_fluid(S_N_PTS, S_RAD_CORE, S_RAD_DYN)

print(f"PHASE 2: DUAL HYDRODYNAMIC MATRICES SEEDED.")

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f_idx):
    t_sec = f_idx / float(FPS)
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.]); ax.set_axis_off(); fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540); ax.set_ylim(-960, 960)

    # 1. KINEMATIC CAMERA TENSOR
    # Locked Isometric Camera slightly drifting for 3D depth study
    cam_pitch = -12.0
    cam_angle = 45.0 + np.sin(t_sec * 0.2) * 4.0 
    M_cam = rx(cam_pitch) @ ry(cam_angle)
    # Huge distance to render both gas giants in the same frame
    cam_dist = 2800.0 
    
    # 270 Degree wedge (Solid space). The cutaway void is from Theta = 0 to Theta = Pi/2
    T_MIN = np.pi / 2.0
    T_MAX = 2.0 * np.pi

    faces_collected = []
    face_colors = []
    centroids_z = []
    
    def process_faces(geom_faces, hex_color, apply_rot=0.0):
        c_rgb = np.array(mcolors.to_rgb(hex_color))
        rot_mat = ry(np.radians(apply_rot)) if apply_rot != 0.0 else None
        
        for face in geom_faces:
            if rot_mat is not None:
                face = np.einsum('ij,nj->ni', rot_mat, face)
                
            v1 = face[1] - face[0]; v2 = face[2] - face[0]
            norm = np.cross(v1, v2)
            n_len = np.linalg.norm(norm)
            if n_len > 0: norm /= n_len
            
            diff = 0.4 + 0.6 * np.clip(np.dot(norm, LIGHT_DIR), 0, 1)
            fc = np.append(c_rgb * diff, 1.0)
            
            v_cam = np.einsum('ij,nj->ni', M_cam, face)
            v_cam[:, 2] += cam_dist
            if np.any(v_cam[:, 2] < 10.0): continue
            
            # Iso-scale projection to handle enormous structure perfectly on 9:16
            px = 1800.0 * (v_cam[:, 0] / v_cam[:, 2])
            py = 1800.0 * (v_cam[:, 1] / v_cam[:, 2])
            
            faces_collected.append(np.stack((px, py), axis=-1))
            face_colors.append(fc)
            centroids_z.append(np.mean(v_cam[:, 2]))

    # ================= JUPITER COMPILER (Y = +460) =================
    f_j_gas = generate_wedge_shell(JUP_Y, J_RAD_GAS, T_MIN, T_MAX)
    f_j_gas += generate_cut_wall(JUP_Y, T_MIN, J_RAD_DYN, J_RAD_GAS)
    f_j_gas += generate_cut_wall(JUP_Y, T_MAX, J_RAD_DYN, J_RAD_GAS)
    process_faces(f_j_gas, C_JUP_GAS)
    
    f_j_dyn = generate_wedge_shell(JUP_Y, J_RAD_DYN, T_MIN, T_MAX)
    f_j_dyn += generate_wedge_shell(JUP_Y, J_RAD_CORE, T_MIN, T_MAX)
    f_j_dyn += generate_cut_wall(JUP_Y, T_MIN, J_RAD_CORE, J_RAD_DYN)
    f_j_dyn += generate_cut_wall(JUP_Y, T_MAX, J_RAD_CORE, J_RAD_DYN)
    process_faces(f_j_dyn, C_JUP_DYN)
    
    f_j_core = generate_wedge_shell(JUP_Y, J_RAD_CORE, T_MIN, T_MAX)
    f_j_core += generate_cut_wall(JUP_Y, T_MIN, 0.0, J_RAD_CORE)
    f_j_core += generate_cut_wall(JUP_Y, T_MAX, 0.0, J_RAD_CORE)
    process_faces(f_j_core, C_CORE)
    
    # Jupiter Fluid Spin
    for i in range(J_N_PTS):
        cur_t_mod = (J_DTHETA[i] + t_sec * J_DVEL[i]) % (2 * np.pi)
        if cur_t_mod < T_MIN:
            r = J_DR[i]
            x = r * np.sin(J_DPHI[i]) * np.cos(cur_t_mod)
            y = r * np.cos(J_DPHI[i]) + JUP_Y
            z = r * np.sin(J_DPHI[i]) * np.sin(cur_t_mod)
            process_faces(generate_particle(np.array([x, y, z]), 8.0), C_JUP_PLASMA)

    # Jupiter Magnetic Fields (Tilted)
    m_long_arr = np.linspace(0, 2*np.pi, 6, endpoint=False)
    j_mag_rot = t_sec * 4.0
    for ml in m_long_arr:
        l_mod = (ml - np.radians(j_mag_rot)) % (2*np.pi)
        if l_mod > T_MIN:
            for L in [500.0, 700.0]:
                arc = generate_magnetic_arc(JUP_Y, L, ml, tilt_deg=J_TILT, thickness=3.5)
                # Apply rotation manually to pivot around core center
                c_rgb = np.array(mcolors.to_rgb(C_JUP_MAG))
                R_dyn = ry(np.radians(j_mag_rot))
                for face in arc:
                    # Translate to origin, rotate, translate back
                    shifted = face - np.array([0, JUP_Y, 0])
                    rotated = np.einsum('ij,nj->ni', R_dyn, shifted)
                    final = rotated + np.array([0, JUP_Y, 0])
                    
                    v1 = final[1] - final[0]; v2 = final[2] - final[0]
                    norm = np.cross(v1, v2)
                    n_len = np.linalg.norm(norm)
                    if n_len > 0: norm /= n_len
                    
                    diff = 0.5 + 0.5 * np.clip(np.dot(norm, LIGHT_DIR), 0, 1)
                    fc = np.append(c_rgb * diff, 1.0)
                    
                    v_cam = np.einsum('ij,nj->ni', M_cam, final)
                    v_cam[:, 2] += cam_dist
                    if np.any(v_cam[:, 2] < 10.0): continue
                    
                    px = 1800.0 * (v_cam[:, 0] / v_cam[:, 2])
                    py = 1800.0 * (v_cam[:, 1] / v_cam[:, 2])
                    faces_collected.append(np.stack((px, py), axis=-1))
                    face_colors.append(fc)
                    centroids_z.append(np.mean(v_cam[:, 2]))


    # ================= SATURN COMPILER (Y = -460) =================
    f_s_gas = generate_wedge_shell(SAT_Y, S_RAD_GAS, T_MIN, T_MAX)
    f_s_gas += generate_cut_wall(SAT_Y, T_MIN, S_RAD_DYN, S_RAD_GAS)
    f_s_gas += generate_cut_wall(SAT_Y, T_MAX, S_RAD_DYN, S_RAD_GAS)
    process_faces(f_s_gas, C_SAT_GAS)
    
    f_s_dyn = generate_wedge_shell(SAT_Y, S_RAD_DYN, T_MIN, T_MAX)
    f_s_dyn += generate_wedge_shell(SAT_Y, S_RAD_CORE, T_MIN, T_MAX)
    f_s_dyn += generate_cut_wall(SAT_Y, T_MIN, S_RAD_CORE, S_RAD_DYN)
    f_s_dyn += generate_cut_wall(SAT_Y, T_MAX, S_RAD_CORE, S_RAD_DYN)
    process_faces(f_s_dyn, C_SAT_DYN)
    
    f_s_core = generate_wedge_shell(SAT_Y, S_RAD_CORE, T_MIN, T_MAX)
    f_s_core += generate_cut_wall(SAT_Y, T_MIN, 0.0, S_RAD_CORE)
    f_s_core += generate_cut_wall(SAT_Y, T_MAX, 0.0, S_RAD_CORE)
    process_faces(f_s_core, C_CORE)
    
    # Saturn Rings (Cutaway)
    f_rings = generate_flat_ring_segment(SAT_Y, S_RING_IN, S_RING_OUT, T_MIN, T_MAX)
    f_rings += generate_flat_ring_segment(SAT_Y-1.0, S_RING_IN, S_RING_OUT, T_MIN, T_MAX) # Dual thickness
    process_faces(f_rings, C_SAT_RING)

    # Saturn Fluid Spin
    for i in range(S_N_PTS):
        cur_t_mod = (S_DTHETA[i] + t_sec * S_DVEL[i]) % (2 * np.pi)
        if cur_t_mod < T_MIN:
            r = S_DR[i]
            x = r * np.sin(S_DPHI[i]) * np.cos(cur_t_mod)
            y = r * np.cos(S_DPHI[i]) + SAT_Y
            z = r * np.sin(S_DPHI[i]) * np.sin(cur_t_mod)
            process_faces(generate_particle(np.array([x, y, z]), 6.0), C_SAT_MAG)

    # Saturn Magnetic Fields (Perfectly Aligned, 0 degree tilt)
    s_mag_rot = t_sec * 3.5
    for ml in m_long_arr:
        l_mod = (ml - np.radians(s_mag_rot)) % (2*np.pi)
        if l_mod > T_MIN:
            for L in [450.0, 600.0]:
                arc = generate_magnetic_arc(SAT_Y, L, ml, tilt_deg=S_TILT, thickness=2.5)
                c_rgb = np.array(mcolors.to_rgb(C_SAT_MAG))
                R_dyn = ry(np.radians(s_mag_rot))
                for face in arc:
                    shifted = face - np.array([0, SAT_Y, 0])
                    rotated = np.einsum('ij,nj->ni', R_dyn, shifted)
                    final = rotated + np.array([0, SAT_Y, 0])
                    
                    v1 = final[1] - final[0]; v2 = final[2] - final[0]
                    norm = np.cross(v1, v2)
                    n_len = np.linalg.norm(norm)
                    if n_len > 0: norm /= n_len
                    
                    diff = 0.5 + 0.5 * np.clip(np.dot(norm, LIGHT_DIR), 0, 1)
                    fc = np.append(c_rgb * diff, 1.0)
                    
                    v_cam = np.einsum('ij,nj->ni', M_cam, final)
                    v_cam[:, 2] += cam_dist
                    if np.any(v_cam[:, 2] < 10.0): continue
                    
                    px = 1800.0 * (v_cam[:, 0] / v_cam[:, 2])
                    py = 1800.0 * (v_cam[:, 1] / v_cam[:, 2])
                    faces_collected.append(np.stack((px, py), axis=-1))
                    face_colors.append(fc)
                    centroids_z.append(np.mean(v_cam[:, 2]))


    # 5. ABSOLUTE DEPENDENCY SORT & RENDER
    sort_idx = np.argsort(centroids_z)[::-1] 
    sorted_faces = [faces_collected[i] for i in sort_idx]
    sorted_fcs = [face_colors[i] for i in sort_idx]
    
    if sorted_faces:
        ax.add_collection(PolyCollection(sorted_faces, facecolors=sorted_fcs, edgecolors='#111115', linewidths=0.2, joinstyle='miter'))

    # 6. HIGH-DENSITY HUD & TELEMETRY
    ax.add_patch(Rectangle((-540, 780), 1080, 180, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [780, 780], color=C_TEXT, lw=3, zorder=81)
    ax.text(-500, 880, "LG-414 :: JUPITER & SATURN TENSORS", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 830, "[SFI-1.00] THE MASS-COMPRESSION LIMIT EXPOSED", color=C_JUP_DYN, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    prog = t_sec / DURATION
    if t_sec < 12.0:
        state_msg = "PHASE 1: JUPITER (THE ALMOST STAR)"
        state_col = C_JUP_MAG
        active_op = "MASSIVE METALLIC CORE (80%). VIOLENT TILTED MAGNETIC TENSOR."
    else:
        state_msg = "PHASE 2: SATURN (THE UNDER-DENSE SIBLING)"
        state_col = C_SAT_MAG
        active_op = "SUNKEN CORE (45%). AXI-SYMMETRIC MAGNETIC FIELD (0 DEG TILT)."

    ax.text(-500, -780, f"PROTOCOL STATE : {state_msg}", color=state_col, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"DIAGNOSTIC     : {active_op}", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"AXIOMATIC TRUTH: MORE MASS DOES NOT EQUAL MORE SIZE. IT DRIVES VOLUMETRIC CRUSH.", color=C_TEXT, fontsize=11, fontname='monospace', zorder=82)

    ax.add_patch(Rectangle((-500, -920), 1000, 8, facecolor=C_GUI, zorder=82))
    ax.add_patch(Rectangle((-500, -920), 1000 * prog, 8, facecolor=state_col, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f_idx:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f_idx

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-414: DUAL ISO-STRUCTURAL TENSOR ENGAGED [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            pass
    print("Compilation Complete. Matrix resolved to exact thermodynamic comparison.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
