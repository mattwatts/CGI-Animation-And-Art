"""
PROJECT: Logic Garden 413b (The Magneto-Hydrodynamic Kinematic Tensor)
FORMAT: YouTube Shorts (1080x1920)
METADATA: PLANETARY DYNAMO, JUPITER, MAGNETIC FIELD, ASTROPHYSICS, KINEMATICS
EXECUTION: 24.0s Seamless Loop Sequence. True 3D Mathematical Construction.
RULES ENFORCED:
- Daylight Palette (White Substrate / High-Contrast Chrome).
- Phase-Locked Metaphor: Exact realisational aspect of a dynamic fluid core.
- TATHĀTĀ LOOP: Rotations locked to K-Multiplier relative to true day lengths (K=10).
- Photorealistic Jovian atmospheric surface banding tumbling on the exterior.
- Static 90-degree cutaway mathematically mapped to permanently face the viewer.
- Explicit Physical Rotational Axis Vector protruding into space.
- Bounded, high-contrast structural taxonomy labels.
- Australian spelling conventions enforced natively (Maths, Colour, Optimise).
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
OUT_DIR = "frames_413b_dynamo"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG            = '#FFFFFF'
C_TEXT          = '#111115'
C_AXIS          = '#111115'  
C_CORE          = '#111115'  # Indestructible Black (Heavy Core)
C_BASE          = '#78350F'  # Substrate holding the Jovian bands
C_DYNAMO        = '#C20078'  # Deep Magenta (Metallic Hydrogen)
C_MAG_FIELD     = '#00D2FF'  # High-Contrast Cyan (Magnetic Tensor)
C_PLASMA        = '#FFB300'  # Dense Amber (Fluid & Caught Plasma)
C_GUI           = '#64748B'

LIGHT_DIR = np.array([-0.6, 0.7, -0.4])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

# ------------------------------------------------------------------
# RIGID 3D ARCHITECTURAL LAYER METRICS 
# ------------------------------------------------------------------
RAD_CORE = 100.0
RAD_DYN  = 340.0
RAD_GAS  = 440.0

AXIAL_TILT = 3.1
MAG_TILT   = 9.6
K_MULT     = 10   # Seamless 10-rotation loop

print(f"PHASE 1: SINGLE-PLANET MEGA-SUBSTRATE MATRIX DEFINED.")

# ------------------------------------------------------------------
# KINEMATIC TOPOLOGY SEEDING (ATMOSPHERIC BANDING)
# ------------------------------------------------------------------
np.random.seed(413)

def seed_surface_nodes(n_pts, r_val):
    rad = np.full(n_pts, r_val + 2.5)
    phi = np.arccos(np.random.uniform(-0.95, 0.95, n_pts))
    theta = np.random.uniform(0, 2 * np.pi, n_pts)
    return rad, phi, theta

N_CRUST = 1200
CRUST_DR, CRUST_DPHI, CRUST_DTHETA = seed_surface_nodes(N_CRUST, RAD_GAS)

def get_band_color(phi_rad):
    lat = np.degrees(np.abs(np.pi/2.0 - phi_rad))
    if lat < 12: return '#FFFFFF'   # Equatorial zone (Bright White)
    elif lat < 24: return '#EA580C' # SEB/NEB (Rust/Orange)
    elif lat < 38: return '#FDE047' # Temperate Zones (Pale Yellow)
    elif lat < 55: return '#9A3412' # Belts (Sienna)
    else: return '#78350F'          # Polar Regions (Umber)

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

def generate_wedge_shell(r, t_min, t_max, res_phi=24, res_theta=36):
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

def generate_cut_wall(theta, r_min, r_max, res_phi=24, res_r=4):
    phi = np.linspace(0, np.pi, res_phi)
    r_arr = np.linspace(max(r_min, 0.1), r_max, res_r)
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

def generate_magnetic_arc(L_shell, longitude, thickness=3.5, res=60):
    faces = []
    phi = np.linspace(0.06, np.pi - 0.06, res)
    pts = []
    for p in phi:
        r = L_shell * (np.sin(p)**2)
        X = r * np.sin(p) * np.cos(longitude)
        Y = r * np.cos(p)
        Z = r * np.sin(p) * np.sin(longitude)
        pts.append(np.array([X, Y, Z]))

    for i in range(len(pts) - 1):
        p1 = pts[i]; p2 = pts[i+1]
        v = p2 - p1
        length = np.linalg.norm(v)
        if length < 1e-4: continue
        v = v / length
        up = np.array([0., 1., 0.]) if np.abs(v[1]) < 0.99 else np.array([1., 0., 0.])
        right = np.cross(up, v)
        right = right / np.linalg.norm(right)
        real_up = np.cross(v, right)
        R_mat = np.column_stack((right, real_up, v))
        t = thickness / 2.0; l = length / 2.0
        vv = np.array([[-t, -t, -l], [ t, -t, -l], [ t,  t, -l], [-t,  t, -l], [-t, -t,  l], [ t, -t,  l], [ t,  t,  l], [-t,  t,  l]])
        f_idx = [[0,1,2,3], [4,5,6,7], [0,1,5,4], [1,2,6,5], [2,3,7,6], [3,0,4,7]]
        mid = (p1 + p2) / 2.0
        for face in f_idx: faces.append(np.dot(vv[face], R_mat.T) + mid)
    return faces

def generate_particle(size):
    r = size / 2.0
    v = np.array([[0, r, 0], [0, -r, 0], [r, 0, 0], [-r, 0, 0], [0, 0, r], [0, 0, -r]])
    f_idx = [[0, 2, 4], [0, 4, 3], [0, 3, 5], [0, 5, 2], [1, 4, 2], [1, 3, 4], [1, 5, 3], [1, 2, 5]]
    return [v[f] for f in f_idx]

# ------------------------------------------------------------------
# O(N) KINEMATIC FLUID & PLASMA COMPILERS
# ------------------------------------------------------------------
def seed_fluid(n_pts, r_in, r_out):
    rad = np.random.uniform(r_in + 5, r_out - 5, n_pts)
    phi = np.arccos(np.random.uniform(-1, 1, n_pts))
    theta = np.random.uniform(0, 2 * np.pi, n_pts)
    vel = 3.0 + 5.0 * ((r_out - rad) / (r_out - r_in))
    return rad, phi, theta, vel

N_DYNAMO_PTS = 800
D_DR, D_DPHI, D_DTHETA, D_DVEL = seed_fluid(N_DYNAMO_PTS, RAD_CORE, RAD_DYN)

N_PLASMA = 350
L_SHELLS = [550.0, 750.0, 950.0]
P_L = np.random.choice(L_SHELLS, N_PLASMA)
P_LONG = np.random.uniform(0, 2 * np.pi, N_PLASMA)
P_PHI_V = np.random.uniform(-0.6, 0.6, N_PLASMA)
P_PHI = np.random.uniform(0.1, np.pi - 0.1, N_PLASMA)

print(f"PHASE 2: HYDRODYNAMIC AND MAGNETIC PLASMA FIELDS SEEDED.")

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
    cam_pitch = -22.0
    cam_angle = 45.0  # Perfect lock. Exposes the 270->360 void straight to camera.
    M_cam = rx(cam_pitch) @ ry(cam_angle)
    cam_dist = 2200.0

    T_MIN = 0.0
    T_MAX = 1.5 * np.pi # 270-degree solid, 90-degree void facing viewer.

    faces_collected = []
    face_colors = []
    centroids_z = []
    ax_lines_2d = []

    def process_faces(geom_faces, hex_color, M_tilt=None):
        c_rgb = np.array(mcolors.to_rgb(hex_color))
        for face in geom_faces:
            f_local = np.copy(face)
            if M_tilt is not None:
                f_local = np.einsum('ij,nj->ni', M_tilt, f_local)

            v1 = f_local[1] - f_local[0]; v2 = f_local[2] - f_local[0]
            norm = np.cross(v1, v2)
            n_len = np.linalg.norm(norm)
            if n_len > 0: norm /= n_len

            diff = 0.4 + 0.6 * np.clip(np.dot(norm, LIGHT_DIR), 0, 1)
            fc = np.append(c_rgb * diff, 1.0)

            v_cam = np.einsum('ij,nj->ni', M_cam, f_local)
            v_cam[:, 2] += cam_dist
            if np.any(v_cam[:, 2] < 10.0): continue

            px = 1800.0 * (v_cam[:, 0] / v_cam[:, 2])
            py = 1800.0 * (v_cam[:, 1] / v_cam[:, 2])

            faces_collected.append(np.stack((px, py), axis=-1))
            face_colors.append(fc)
            centroids_z.append(np.mean(v_cam[:, 2]))

    def process_kinematic_nodes(dr, dphi, dtheta, v_spin, M_tilt, get_col_func, rad_lim, is_fluid=False):
        for i in range(len(dr)):
            cur_t = (dtheta[i] + np.radians(v_spin)) % (2 * np.pi)
            
            # Surface nodes visible on hull. Dynamo nodes visible inside void cutaway.
            if (not is_fluid and cur_t <= T_MAX) or (is_fluid and cur_t > T_MAX):
                x = dr[i] * np.sin(dphi[i]) * np.cos(cur_t)
                y = dr[i] * np.cos(dphi[i])
                z = dr[i] * np.sin(dphi[i]) * np.sin(cur_t)

                p_f_raw = generate_particle(6.5 if rad_lim > 400 else 8.5) # Dynamic scaling
                p_f = [face + np.array([x, y, z]) for face in p_f_raw]
                
                h_col = get_col_func(dphi[i]) if get_col_func else C_PLASMA
                process_faces(p_f, h_col, M_tilt=M_tilt)

    MT_AXIS_GLOBAL = rz(AXIAL_TILT)
    spin_global = t_sec * (K_MULT * 15.0)

    # 1. MOLECULAR HYDROGEN SHELL (Inner dark substrate to hold the exterior cloud nodes)
    f_gas = generate_wedge_shell(RAD_GAS, T_MIN, T_MAX)
    f_gas += generate_cut_wall(T_MIN, RAD_DYN, RAD_GAS)
    f_gas += generate_cut_wall(T_MAX, RAD_DYN, RAD_GAS)
    process_faces(f_gas, C_BASE, M_tilt=MT_AXIS_GLOBAL)

    # 2. METALLIC HYDROGEN DYNAMO
    f_dyn = generate_wedge_shell(RAD_DYN, T_MIN, T_MAX)
    f_dyn += generate_wedge_shell(RAD_CORE, T_MIN, T_MAX)
    f_dyn += generate_cut_wall(T_MIN, RAD_CORE, RAD_DYN)
    f_dyn += generate_cut_wall(T_MAX, RAD_CORE, RAD_DYN)
    process_faces(f_dyn, C_DYNAMO, M_tilt=MT_AXIS_GLOBAL)

    # 3. HEAVY CORE 
    f_core = generate_wedge_shell(RAD_CORE, T_MIN, T_MAX)
    f_core += generate_cut_wall(T_MIN, 0.0, RAD_CORE)
    f_core += generate_cut_wall(T_MAX, 0.0, RAD_CORE)
    process_faces(f_core, C_CORE, M_tilt=MT_AXIS_GLOBAL)

    # 4. KINEMATICS: SURFACE ATMOSPHERE & INTERNAL HYDRODYNAMIC SPIN
    process_kinematic_nodes(CRUST_DR, CRUST_DPHI, CRUST_DTHETA, spin_global, MT_AXIS_GLOBAL, get_band_color, RAD_GAS, is_fluid=False)
    
    # Internal dynamo uses a secondary independent spin factor mixed with global
    for i in range(N_DYNAMO_PTS):
        cur_t_mod = (D_DTHETA[i] + t_sec * D_DVEL[i] + np.radians(spin_global)) % (2 * np.pi)
        if cur_t_mod > T_MAX:
            r = D_DR[i]
            x = r * np.sin(D_DPHI[i]) * np.cos(cur_t_mod)
            y = r * np.cos(D_DPHI[i])
            z = r * np.sin(D_DPHI[i]) * np.sin(cur_t_mod)
            p_f = generate_particle(8.0)
            p_geom = [face + np.array([x, y, z]) for face in p_f]
            process_faces(p_geom, C_PLASMA, M_tilt=MT_AXIS_GLOBAL)

    # 5. AXI-SYMMETRIC MAGNETIC YIELD (Tilted via Dynamo)
    j_mag_rot = spin_global
    m_long_arr = np.linspace(0, 2*np.pi, 8, endpoint=False)
    for ml in m_long_arr:
        l_mod = (ml - np.radians(j_mag_rot)) % (2*np.pi)
        if l_mod > T_MAX: # Restrict lines inside the visible cutaway void for maximum visibility without clipping
            for L in L_SHELLS:
                arc_faces = generate_magnetic_arc(L, 0, thickness=4.5)
                M_mag_chain = MT_AXIS_GLOBAL @ rz(MAG_TILT) @ ry(ml - np.radians(j_mag_rot))
                process_faces(arc_faces, C_MAG_FIELD, M_tilt=M_mag_chain)

    # 6. EXTERNAL MAGNETIC PLASMA KINEMATICS (Bouncing in L-Shells)
    for i in range(N_PLASMA):
        cur_long = P_LONG[i] + np.radians(spin_global)
        cur_phi = P_PHI[i] + t_sec * P_PHI_V[i]

        if cur_phi < 0.1: cur_phi = 0.2 - cur_phi; P_PHI_V[i] *= -1
        if cur_phi > np.pi - 0.1: cur_phi = 2*(np.pi - 0.1) - cur_phi; P_PHI_V[i] *= -1
        P_PHI[i] = cur_phi

        base_l = (cur_long) % (2 * np.pi)
        if base_l > T_MAX:
            r = P_L[i] * (np.sin(cur_phi)**2)
            # Use raw calculation mapped to mag chain
            x = r * np.sin(cur_phi) * np.cos(0)
            y = r * np.cos(cur_phi)
            z = r * np.sin(cur_phi) * np.sin(0)

            p_f = generate_particle(9.0)
            p_geom = [face + np.array([x, y, z]) for face in p_f]
            M_mag_chain = MT_AXIS_GLOBAL @ rz(MAG_TILT) @ ry(cur_long)
            process_faces(p_geom, C_PLASMA, M_tilt=M_mag_chain)

    # 7. EXPLICIT PHYSICAL AXIS
    ax_top = MT_AXIS_GLOBAL @ np.array([0, RAD_GAS + 200.0, 0])
    ax_bot = MT_AXIS_GLOBAL @ np.array([0, -(RAD_GAS + 200.0), 0])
    l_pts = np.array([ax_top, ax_bot])
    v_cam_s = np.einsum('ij,nj->ni', M_cam, l_pts); v_cam_s[:, 2] += cam_dist
    px_s = 1800.0 * (v_cam_s[:, 0] / v_cam_s[:, 2]); py_s = 1800.0 * (v_cam_s[:, 1] / v_cam_s[:, 2])
    ax_lines_2d.append([(px_s[0], py_s[0]), (px_s[1], py_s[1])])

    # ================= 8. ABSOLUTE DEPENDENCY SORT & RENDER =================
    for line in ax_lines_2d:
        ax.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], color=C_AXIS, lw=3.5, zorder=50)

    sort_idx = np.argsort(centroids_z)[::-1]
    if faces_collected:
        sorted_faces = [faces_collected[i] for i in sort_idx]
        sorted_fcs = [face_colors[i] for i in sort_idx]
        ax.add_collection(PolyCollection(sorted_faces, facecolors=sorted_fcs, edgecolors='#111115', linewidths=0.25, joinstyle='miter', zorder=60))

    # ================= 9. HIGH-DENSITY HUD & TELEMETRY =================
    ax.add_patch(Rectangle((-540, 780), 1080, 180, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [780, 780], color=C_TEXT, lw=3, zorder=81)
    ax.text(-500, 880, "LG-413b :: PLANETARY DYNAMO TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 830, "[SFI-1.00] EXACT REALISATIONAL ASPECT", color='#DE008A', fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    # In-World Target Labels (High Contrast Text against pure White Bounding Box)
    bbox_props = dict(boxstyle="square,pad=0.4", fc="#FFFFFF", ec="#111115", lw=2.5)
    ax.text(-480, 480, f"JUPITER\nP: 9.9h [K:{K_MULT}]", color=C_TEXT, fontsize=20, fontname='monospace', weight='bold', zorder=85, bbox=bbox_props)

    prog = t_sec / DURATION
    if t_sec < 12.0:
        state_msg = "PHASE 1: THE TATHATA K-MULTIPLIER"
        state_col = '#EA580C'
        active_op = "SEAMLESS KINEMATICS ROTATING TRUE LATITUDINAL BANDING."
    else:
        state_msg = "PHASE 2: INTERNAL THERMO-DIAGNOSTICS"
        state_col = C_MAG_FIELD
        active_op = "FLUID METALLIC OCEANS DRIVING TILTED MAGNETIC SHEAR."

    ax.text(-500, -780, f"PROTOCOL STATE : {state_msg}", color=state_col, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"DIAGNOSTIC     : {active_op}", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"AXIOMATIC TRUTH: A MAGNETIC FIELD IS NOT A GHOST. IT IS THE PHYSICAL YIELD OF ROTATING LIQUID METAL.", color=C_TEXT, fontsize=11, fontname='monospace', zorder=82)

    ax.add_patch(Rectangle((-500, -920), 1000, 8, facecolor=C_GUI, zorder=82))
    ax.add_patch(Rectangle((-500, -920), 1000 * prog, 8, facecolor=state_col, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f_idx:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f_idx

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-413b: MAGNETO-HYDRODYNAMIC TENSOR ENGAGED [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            pass
    print("Compilation Complete. Matrix resolved to exact topological magnetic yield.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
