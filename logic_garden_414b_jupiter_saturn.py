"""
PROJECT: Logic Garden 414b (The Dual Kinematic Tensor // Jupiter & Saturn) - V2 Corrected
FORMAT: YouTube Shorts (1080x1920)
METADATA: JUPITER, SATURN, PLANETARY DYNAMO, KINEMATICS, ASTROPHYSICS
EXECUTION: 24.0s Seamless Loop Sequence. Iso-scaled true 3D Mathematical Comparative Cutaways.
RULES ENFORCED:
- Daylight Palette (White Substrate / High-Contrast Chrome).
- Exact realisational aspect: Cutaways re-engineered to mathematically face the viewer.
- TATHĀTĀ LOOP: Rotations locked to K-Multiplier relative to true rotational speeds.
- Explicit Physical Rotational Axis Vectors exposed and piercing the poles.
- High-Contrast Telemetry: Labels relocated and bounded for absolute readability.
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
OUT_DIR = "frames_414b_jup_sat"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG            = '#FFFFFF'
C_TEXT          = '#111115'  # Indestructible Black for Labels
C_AXIS          = '#111115'  # Indestructible Black for polar rotation axis
C_CORE          = '#111115'  # Heavy Cores

# JUPITER SPECIFICS
C_JUP_BASE      = '#78350F'  # Substrate underpinning bands
C_JUP_DYN       = '#C20078'  # Deep Magenta (Crushing Metallic Hydrogen)
C_JUP_MAG       = '#FF3300'  # Intense Red (Violent Magnetic Tensor)
C_JUP_PLASMA    = '#FFB300'  # Dense Amber

# SATURN SPECIFICS
C_SAT_BASE      = '#B45309'  # Substrate underpinning bands
C_SAT_DYN       = '#005599'  # Deep Marine (Sunken Metallic Core)
C_SAT_RING      = '#94A3B8'  # Steel (Equatorial Matrix)
C_SAT_MAG       = '#00D2FF'  # High-Contrast Cyan (Axi-symmetric Tensor)

C_GUI           = '#64748B'

LIGHT_DIR = np.array([-0.6, 0.7, -0.4])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

# ------------------------------------------------------------------
# RIGID 3D ARCHITECTURAL LAYER METRICS (SCALED)
# ------------------------------------------------------------------
JUP_Y           = 460.0
J_RAD_CORE      = 50.0
J_RAD_DYN       = 320.0  
J_RAD_GAS       = 400.0
J_MAG_TILT      = 9.6
J_AXIAL_TILT    = 3.1
J_K_MULT        = 10     

SAT_Y           = -460.0
S_RAD_CORE      = 40.0
S_RAD_DYN       = 150.0  
S_RAD_GAS       = 330.0
S_RING_IN       = 380.0
S_RING_OUT      = 720.0
S_MAG_TILT      = 0.0
S_AXIAL_TILT    = 26.7
S_K_MULT        = 9      

# ------------------------------------------------------------------
# KINEMATIC TOPOLOGY SEEDING (ATMOSPHERIC BANDING)
# ------------------------------------------------------------------
np.random.seed(414)

def seed_surface_nodes(n_pts, r_val):
    rad = np.full(n_pts, r_val + 2.0)
    phi = np.arccos(np.random.uniform(-0.95, 0.95, n_pts))
    theta = np.random.uniform(0, 2 * np.pi, n_pts)
    return rad, phi, theta

N_CRUST = 800
J_CRUST_DR, J_CRUST_DPHI, J_CRUST_DTHETA = seed_surface_nodes(N_CRUST, J_RAD_GAS)
S_CRUST_DR, S_CRUST_DPHI, S_CRUST_DTHETA = seed_surface_nodes(N_CRUST, S_RAD_GAS)

def get_jup_band_color(phi_rad):
    lat = np.degrees(np.abs(np.pi/2.0 - phi_rad))
    if lat < 12: return '#FFFFFF'   
    elif lat < 24: return '#EA580C' 
    elif lat < 38: return '#FDE047' 
    elif lat < 55: return '#9A3412' 
    else: return '#78350F'          

def get_sat_band_color(phi_rad):
    lat = np.degrees(np.abs(np.pi/2.0 - phi_rad))
    if lat < 15: return '#FEF9C3'   
    elif lat < 35: return '#FCD34D' 
    elif lat < 60: return '#D97706' 
    else: return '#92400E'          

# ------------------------------------------------------------------
# MATRIX OPERATIONS & GEOMETRY GENERATORS (CENTERED 0,0,0)
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

def generate_wedge_shell(r, t_min, t_max, res_phi=20, res_theta=28):
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

def generate_cut_wall(theta, r_min, r_max, res_phi=20, res_r=2):
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

def generate_flat_ring_segment(r_in, r_out, t_min, t_max, res_theta=35):
    theta = np.linspace(t_min, t_max, res_theta)
    faces = []
    for i in range(res_theta - 1):
        t1, t2 = theta[i], theta[i+1]
        p1 = np.array([r_in*np.cos(t1), 0, r_in*np.sin(t1)])
        p2 = np.array([r_out*np.cos(t1), 0, r_out*np.sin(t1)])
        p3 = np.array([r_out*np.cos(t2), 0, r_out*np.sin(t2)])
        p4 = np.array([r_in*np.cos(t2), 0, r_in*np.sin(t2)])
        faces.append([p1, p2, p3, p4])
    return faces

def generate_magnetic_arc(L_shell, longitude, thickness=2.5, res=45):
    faces = []
    phi = np.linspace(0.08, np.pi - 0.08, res)
    pts = []
    for p in phi:
        r = L_shell * (np.sin(p)**2)
        pts.append(np.array([r * np.sin(p) * np.cos(longitude), r * np.cos(p), r * np.sin(p) * np.sin(longitude)]))
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
# KINEMATIC FLUID COMPILERS (Internal dynamos)
# ------------------------------------------------------------------
def seed_fluid(n_pts, r_in, r_out):
    rad = np.random.uniform(r_in + 5, r_out - 5, n_pts)
    phi = np.arccos(np.random.uniform(-1, 1, n_pts))
    theta = np.random.uniform(0, 2 * np.pi, n_pts)
    vel = 3.0 + 5.0 * ((r_out - rad) / (r_out - r_in))
    return rad, phi, theta, vel

J_N_PTS = 600
S_N_PTS = 250
J_DR, J_DPHI, J_DTHETA, J_DVEL = seed_fluid(J_N_PTS, J_RAD_CORE, J_RAD_DYN)
S_DR, S_DPHI, S_DTHETA, S_DVEL = seed_fluid(S_N_PTS, S_RAD_CORE, S_RAD_DYN)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f_idx):
    t_sec = f_idx / float(FPS)

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.]); ax.set_axis_off(); fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540); ax.set_ylim(-960, 960)

    # LOCKED CAMERA TENSOR
    cam_pitch = -20.0
    cam_angle = 45.0  # Mathematically locks with a [1.5*pi to 2.0*pi] geometric void to perfectly face viewer
    M_cam = rx(cam_pitch) @ ry(cam_angle)
    cam_dist = 2800.0

    # THE CAMERA-FACING CUTAWAY: Solid planet mapped 0->270 deg. Missing wedge (facing camera) is 270->360.
    T_MIN = 0.0
    T_MAX = 1.5 * np.pi 

    faces_collected = []
    face_colors = []
    centroids_z = []
    ax_lines_2d = []

    def process_faces(geom_faces, hex_color, M_tilt=None, local_y=0.0):
        c_rgb = np.array(mcolors.to_rgb(hex_color))
        for face in geom_faces:
            f_local = np.copy(face)
            if M_tilt is not None:
                f_local = np.einsum('ij,nj->ni', M_tilt, f_local)
            
            f_global = f_local + np.array([0, local_y, 0])

            v1 = f_global[1] - f_global[0]; v2 = f_global[2] - f_global[0]
            norm = np.cross(v1, v2)
            n_len = np.linalg.norm(norm)
            if n_len > 0: norm /= n_len
            
            diff = 0.4 + 0.6 * np.clip(np.dot(norm, LIGHT_DIR), 0, 1)
            fc = np.append(c_rgb * diff, 1.0)
            
            v_cam = np.einsum('ij,nj->ni', M_cam, f_global)
            v_cam[:, 2] += cam_dist
            if np.any(v_cam[:, 2] < 10.0): continue
            
            px = 1800.0 * (v_cam[:, 0] / v_cam[:, 2])
            py = 1800.0 * (v_cam[:, 1] / v_cam[:, 2])
            
            faces_collected.append(np.stack((px, py), axis=-1))
            face_colors.append(fc)
            centroids_z.append(np.mean(v_cam[:, 2]))

    def process_kinematic_nodes(dr, dphi, dtheta, v_spin, pos_y, M_tilt, get_col_func, rad_lim, is_fluid=False):
        for i in range(len(dr)):
            cur_t = (dtheta[i] + np.radians(v_spin)) % (2 * np.pi)
            
            # Crust tumbles on solid exterior. Fluid tumbles in the missing void.
            if (not is_fluid and cur_t <= T_MAX) or (is_fluid and cur_t > T_MAX):
                x = dr[i] * np.sin(dphi[i]) * np.cos(cur_t)
                y = dr[i] * np.cos(dphi[i])
                z = dr[i] * np.sin(dphi[i]) * np.sin(cur_t)

                p_f_raw = generate_particle(4.5 if rad_lim > 350 else 5.5)
                # Translate mesh directly to local node coordinate
                p_f = [face + np.array([x, y, z]) for face in p_f_raw]
                
                h_col = get_col_func(dphi[i]) if get_col_func else C_JUP_PLASMA
                process_faces(p_f, h_col, M_tilt=M_tilt, local_y=pos_y)

    # ================= JUPITER COMPILER (Y = +460, K=10) =================
    MT_JUP = rz(J_AXIAL_TILT)
    
    # Solid Geometry
    f_j_gas = generate_wedge_shell(J_RAD_GAS, T_MIN, T_MAX)
    f_j_gas += generate_cut_wall(T_MIN, J_RAD_DYN, J_RAD_GAS)
    f_j_gas += generate_cut_wall(T_MAX, J_RAD_DYN, J_RAD_GAS)
    process_faces(f_j_gas, C_JUP_BASE, M_tilt=MT_JUP, local_y=JUP_Y)

    f_j_dyn = generate_wedge_shell(J_RAD_DYN, T_MIN, T_MAX)
    f_j_dyn += generate_wedge_shell(J_RAD_CORE, T_MIN, T_MAX)
    f_j_dyn += generate_cut_wall(T_MIN, J_RAD_CORE, J_RAD_DYN)
    f_j_dyn += generate_cut_wall(T_MAX, J_RAD_CORE, J_RAD_DYN)
    process_faces(f_j_dyn, C_JUP_DYN, M_tilt=MT_JUP, local_y=JUP_Y)

    f_j_core = generate_wedge_shell(J_RAD_CORE, T_MIN, T_MAX)
    f_j_core += generate_cut_wall(T_MIN, 0.0, J_RAD_CORE)
    f_j_core += generate_cut_wall(T_MAX, 0.0, J_RAD_CORE)
    process_faces(f_j_core, C_CORE, M_tilt=MT_JUP, local_y=JUP_Y)

    # Kinematic Nodes
    spin_jup = t_sec * (J_K_MULT * 15.0)
    process_kinematic_nodes(J_CRUST_DR, J_CRUST_DPHI, J_CRUST_DTHETA, spin_jup, JUP_Y, MT_JUP, get_jup_band_color, J_RAD_GAS, is_fluid=False)
    process_kinematic_nodes(J_DR, J_DPHI, J_DTHETA, spin_jup, JUP_Y, MT_JUP, lambda _: C_JUP_PLASMA, J_RAD_DYN, is_fluid=True)

    # Jupiter Magnetic Fields (Tilted internally relative to Dynamo)
    j_mag_rot = t_sec * (J_K_MULT * 15.0)
    for ml in np.linspace(0, 2*np.pi, 6, endpoint=False):
        l_mod = (ml - np.radians(j_mag_rot)) % (2*np.pi)
        if l_mod > T_MAX: # Drawn natively inside the static void window
            for L in [500.0, 700.0]:
                arc_faces = generate_magnetic_arc(L, 0, thickness=4.0)
                # Chain of rotations: Spin Dynamo -> Mag Tilt -> Planet Axis Tilt
                M_mag_chain = MT_JUP @ rz(J_MAG_TILT) @ ry(ml - np.radians(j_mag_rot))
                process_faces(arc_faces, C_JUP_MAG, M_tilt=M_mag_chain, local_y=JUP_Y)

    # Jupiter Axis
    ax_j_top = MT_JUP @ np.array([0, J_RAD_GAS + 150.0, 0]) + np.array([0, JUP_Y, 0])
    ax_j_bot = MT_JUP @ np.array([0, -(J_RAD_GAS + 150.0), 0]) + np.array([0, JUP_Y, 0])
    l_pts_j = np.array([ax_j_top, ax_j_bot]); v_cam_j = np.einsum('ij,nj->ni', M_cam, l_pts_j); v_cam_j[:, 2] += cam_dist
    px_j = 1800.0 * (v_cam_j[:, 0] / v_cam_j[:, 2]); py_j = 1800.0 * (v_cam_j[:, 1] / v_cam_j[:, 2])
    ax_lines_2d.append([(px_j[0], py_j[0]), (px_j[1], py_j[1])])

    # ================= SATURN COMPILER (Y = -460, K=9) =================
    MT_SAT = rz(S_AXIAL_TILT)

    f_s_gas = generate_wedge_shell(S_RAD_GAS, T_MIN, T_MAX)
    f_s_gas += generate_cut_wall(T_MIN, S_RAD_DYN, S_RAD_GAS)
    f_s_gas += generate_cut_wall(T_MAX, S_RAD_DYN, S_RAD_GAS)
    process_faces(f_s_gas, C_SAT_BASE, M_tilt=MT_SAT, local_y=SAT_Y)

    f_s_dyn = generate_wedge_shell(S_RAD_DYN, T_MIN, T_MAX)
    f_s_dyn += generate_wedge_shell(S_RAD_CORE, T_MIN, T_MAX)
    f_s_dyn += generate_cut_wall(T_MIN, S_RAD_CORE, S_RAD_DYN)
    f_s_dyn += generate_cut_wall(T_MAX, S_RAD_CORE, S_RAD_DYN)
    process_faces(f_s_dyn, C_SAT_DYN, M_tilt=MT_SAT, local_y=SAT_Y)

    f_s_core = generate_wedge_shell(S_RAD_CORE, T_MIN, T_MAX)
    f_s_core += generate_cut_wall(T_MIN, 0.0, S_RAD_CORE)
    f_s_core += generate_cut_wall(T_MAX, 0.0, S_RAD_CORE)
    process_faces(f_s_core, C_CORE, M_tilt=MT_SAT, local_y=SAT_Y)

    # Saturn Rings
    f_rings = generate_flat_ring_segment(S_RING_IN, S_RING_OUT, T_MIN, T_MAX)
    f_rings += generate_flat_ring_segment(S_RING_IN, S_RING_OUT, T_MIN, T_MAX) # Thickness reinforcement
    process_faces(f_rings, C_SAT_RING, M_tilt=MT_SAT, local_y=SAT_Y)

    # Kinematic Nodes
    spin_sat = t_sec * (S_K_MULT * 15.0)
    process_kinematic_nodes(S_CRUST_DR, S_CRUST_DPHI, S_CRUST_DTHETA, spin_sat, SAT_Y, MT_SAT, get_sat_band_color, S_RAD_GAS, is_fluid=False)
    process_kinematic_nodes(S_DR, S_DPHI, S_DTHETA, spin_sat, SAT_Y, MT_SAT, lambda _: C_SAT_MAG, S_RAD_DYN, is_fluid=True)

    # Saturn Magnetic Fields (0 degree tilt)
    s_mag_rot = t_sec * (S_K_MULT * 15.0)
    for ml in np.linspace(0, 2*np.pi, 6, endpoint=False):
        l_mod = (ml - np.radians(s_mag_rot)) % (2*np.pi)
        if l_mod > T_MAX:
            for L in [450.0, 600.0]:
                arc_faces = generate_magnetic_arc(L, 0, thickness=2.5)
                M_mag_chain = MT_SAT @ rz(S_MAG_TILT) @ ry(ml - np.radians(s_mag_rot))
                process_faces(arc_faces, C_SAT_MAG, M_tilt=M_mag_chain, local_y=SAT_Y)

    # Saturn Axis
    ax_s_top = MT_SAT @ np.array([0, S_RAD_GAS + 150.0, 0]) + np.array([0, SAT_Y, 0])
    ax_s_bot = MT_SAT @ np.array([0, -(S_RAD_GAS + 150.0), 0]) + np.array([0, SAT_Y, 0])
    l_pts_s = np.array([ax_s_top, ax_s_bot]); v_cam_s = np.einsum('ij,nj->ni', M_cam, l_pts_s); v_cam_s[:, 2] += cam_dist
    px_s = 1800.0 * (v_cam_s[:, 0] / v_cam_s[:, 2]); py_s = 1800.0 * (v_cam_s[:, 1] / v_cam_s[:, 2])
    ax_lines_2d.append([(px_s[0], py_s[0]), (px_s[1], py_s[1])])

    # ================= 5. ABSOLUTE DEPENDENCY SORT & RENDER =================
    for line in ax_lines_2d:
        ax.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], color=C_AXIS, lw=2.5, zorder=50)

    sort_idx = np.argsort(centroids_z)[::-1]
    if faces_collected:
        sorted_faces = [faces_collected[i] for i in sort_idx]
        sorted_fcs = [face_colors[i] for i in sort_idx]
        ax.add_collection(PolyCollection(sorted_faces, facecolors=sorted_fcs, edgecolors='#111115', linewidths=0.2, joinstyle='miter', zorder=60))

    # ================= 6. HIGH-DENSITY HUD & TELEMETRY =================
    ax.add_patch(Rectangle((-540, 780), 1080, 180, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [780, 780], color=C_TEXT, lw=3, zorder=81)
    ax.text(-500, 880, "LG-414b :: JUPITER & SATURN KINEMATICS", color=C_TEXT, fontsize=22, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 830, "[SFI-1.00] EXACT COMPARATIVE TENSORS", color='#DF0000', fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    # In-World Target Labels (High Contrast Text against pure White Bounding Box)
    bbox_props = dict(boxstyle="square,pad=0.3", fc="#FFFFFF", ec="#111115", lw=2)
    ax.text(-480, 680, f"JUPITER\nP: 9.9h [K:{J_K_MULT}]", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=85, bbox=bbox_props)
    
    # Saturn Label placed completely clear of the ring matrix
    ax.text(-480, -200, f"SATURN\nP: 10.6h [K:{S_K_MULT}]", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=85, bbox=bbox_props)

    prog = t_sec / DURATION
    if t_sec < 12.0:
        state_msg = "PHASE 1: THE TATHATA K-MULTIPLIER"
        state_col = '#1E293B'
        active_op = "SEAMLESS ROTATION ENFORCING RELATIVE DAY CYCLES."
    else:
        state_msg = "PHASE 2: INTERNAL THERMO-DIAGNOSTICS"
        state_col = '#B45309'
        active_op = "METALLIC OCEANS AND AXI-SYMMETRIC MAGNETIC SHEAR."

    ax.text(-500, -780, f"PROTOCOL STATE : {state_msg}", color=state_col, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"DIAGNOSTIC     : {active_op}", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"AXIOMATIC TRUTH: MORE MASS GENERATES CRUSHING INTERNAL YIELD, NOT VOLUME.", color=C_TEXT, fontsize=11, fontname='monospace', zorder=82)

    ax.add_patch(Rectangle((-500, -920), 1000, 8, facecolor=C_GUI, zorder=82))
    ax.add_patch(Rectangle((-500, -920), 1000 * prog, 8, facecolor=state_col, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f_idx:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f_idx

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-414b: KINEMATIC DUAL TENSOR ENGAGED [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            pass
    print("Compilation Complete. Matrix resolved to exact thermodynamic comparison.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
