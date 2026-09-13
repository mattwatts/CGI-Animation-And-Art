"""
PROJECT: Logic Garden 413 (The Magneto-Hydrodynamic Tensor // Planetary Dynamo)
FORMAT: YouTube Shorts (1080x1920)
METADATA: PLANETARY DYNAMO, METALLIC HYDROGEN, MAGNETIC FIELD, ASTROPHYSICS, KINEMATICS
EXECUTION: 24.0s Sequence. True 3D Mathematical Construction & Volumetric Cutaway.
RULES ENFORCED:
- Daylight Palette (White Substrate / High-Contrast Chrome).
- Phase-Locked Metaphor: Stripping the cognitive hallucination of solid gas giants.
- Exact realisational aspect of differential rotation driving topological magnetic fields.
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
OUT_DIR = "frames_413_dynamo"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG            = '#FFFFFF'
C_TEXT          = '#111115'
C_EDGE          = '#111115'
C_CORE          = '#111115'  # Indestructible Black (Heavy Element Core)
C_DYNAMO        = '#DE008A'  # Deep Magenta (Metallic Hydrogen Ocean)
C_GAS           = '#1E293B'  # Carbon Slate (Molecular Hydrogen Envelope)
C_MAG_FIELD     = '#00D2FF'  # High-Contrast Cyan (Magnetic Tensor)
C_PLASMA        = '#FFB300'  # Dense Amber (Charged Particles)
C_GUI           = '#64748B'

LIGHT_DIR = np.array([-0.6, 0.7, -0.4])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

# ------------------------------------------------------------------
# RIGID 3D ARCHITECTURAL LAYER METRICS
# ------------------------------------------------------------------
# R1: Core. R2: Dynamo Shell. R3: Outer Shell.
# Mechanical clearance enforced between layers for brutalist clarity.
RAD_CORE = 100.0
RAD_DYN_IN = 115.0
RAD_DYN_OUT = 220.0
RAD_GAS_IN = 235.0
RAD_GAS_OUT = 350.0

print(f"PHASE 1: PLANETARY SUBSTRATE MATRICES DEFINED.")

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
def generate_wedge_shell(r, t_min, t_max, res_phi=24, res_theta=36):
    """Generates the convex outer hull of a cutaway sphere."""
    # Note: Y is the polar axis in this kinematic setup.
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
    """Generates the flat, exposed cross-section walls for the cutaway."""
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

def generate_magnetic_arc(L_shell, longitude, thickness=3.0, res=60):
    """Calculates true L-Shell dipole magnetic field vectors (r = L * sin^2(phi))"""
    faces = []
    # Avoid poles slightly to prevent math singularity collisions
    phi = np.linspace(0.05, np.pi - 0.05, res)
    pts = []
    for p in phi:
        r = L_shell * (np.sin(p)**2)
        X = r * np.sin(p) * np.cos(longitude)
        Y = r * np.cos(p)
        Z = r * np.sin(p) * np.sin(longitude)
        pts.append(np.array([X, Y, Z]))
        
    for i in range(len(pts) - 1):
        p1 = pts[i]
        p2 = pts[i+1]
        
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
# O(N) KINEMATIC FLUID & PLASMA COMPILERS
# ------------------------------------------------------------------
np.random.seed(413)

# DYNAMO CONVECTION FLUID (Metallic Hydrogen)
N_DYNAMO_PTS = 800
D_R = np.random.uniform(RAD_DYN_IN + 5, RAD_DYN_OUT - 5, N_DYNAMO_PTS)
D_PHI = np.arccos(np.random.uniform(-1, 1, N_DYNAMO_PTS))
D_THETA = np.random.uniform(0, 2 * np.pi, N_DYNAMO_PTS)
# Differential rotation: innermost fluid spins fastest
D_VEL = 5.0 + 8.0 * ((RAD_DYN_OUT - D_R) / (RAD_DYN_OUT - RAD_DYN_IN)) 

# MAGNETIC PLASMA NODES
N_PLASMA = 300
L_SHELLS = [450.0, 600.0, 750.0]
P_L = np.random.choice(L_SHELLS, N_PLASMA)
P_LONG = np.random.uniform(0, 2 * np.pi, N_PLASMA)
P_PHI_V = np.random.uniform(-0.5, 0.5, N_PLASMA)
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
    # Observation look directly into the 90-degree cutaway (spanning 0 to Pi/2 mapped below)
    # Slow cinematic parallax tracing the fluid sheer
    cam_pitch = -22.0
    cam_angle = 45.0 + (t_sec * 0.8) # Glacial orbit
    M_cam = rx(cam_pitch) @ ry(cam_angle) # Note rx, ry since our poles are on Y
    cam_dist = 1100.0 
    
    # Global Rotational Tensors
    core_rot = t_sec * 2.0
    gas_rot = t_sec * 1.8
    # 270 Degree wedge (Solid space). The cutaway void is from Theta = 0 to Theta = Pi/2
    T_MIN = np.pi / 2.0
    T_MAX = 2.0 * np.pi

    faces_collected = []
    face_colors = []
    centroids_z = []
    
    def process_faces(geom_faces, hex_color, apply_rot=0.0):
        c_rgb = np.array(mcolors.to_rgb(hex_color))
        rot_mat = ry(np.radians(apply_rot))
        
        for face in geom_faces:
            # Rotate object mathematically before camera translation
            if apply_rot != 0.0:
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
            
            px = 1800.0 * (v_cam[:, 0] / v_cam[:, 2])
            py = 1800.0 * (v_cam[:, 1] / v_cam[:, 2])
            
            faces_collected.append(np.stack((px, py), axis=-1))
            face_colors.append(fc)
            centroids_z.append(np.mean(v_cam[:, 2]))

    # BUILD MOLECULAR HYDROGEN SHELL (OUTER)
    f_gas = generate_wedge_shell(RAD_GAS_OUT, T_MIN, T_MAX)
    f_gas += generate_cut_wall(T_MIN, RAD_GAS_IN, RAD_GAS_OUT)
    f_gas += generate_cut_wall(T_MAX, RAD_GAS_IN, RAD_GAS_OUT)
    process_faces(f_gas, C_GAS, gas_rot)
    
    # BUILD METALLIC HYDROGEN DYNAMO (MID)
    f_dyn = generate_wedge_shell(RAD_DYN_OUT, T_MIN, T_MAX)
    f_dyn += generate_wedge_shell(RAD_DYN_IN, T_MIN, T_MAX) # Inner hull
    f_dyn += generate_cut_wall(T_MIN, RAD_DYN_IN, RAD_DYN_OUT)
    f_dyn += generate_cut_wall(T_MAX, RAD_DYN_IN, RAD_DYN_OUT)
    process_faces(f_dyn, C_DYNAMO, gas_rot) # Base anchor frame
    
    # BUILD SOLID HEAVY CORE (INNER)
    f_core = generate_wedge_shell(RAD_CORE, T_MIN, T_MAX)
    f_core += generate_cut_wall(T_MIN, 0.0, RAD_CORE)
    f_core += generate_cut_wall(T_MAX, 0.0, RAD_CORE)
    process_faces(f_core, C_CORE, core_rot)
    
    # EVALUATE DYNAMO FLUID KINEMATICS
    for i in range(N_DYNAMO_PTS):
        # Differential rotation
        cur_t = D_THETA[i] + t_sec * D_VEL[i]
        cur_t_mod = cur_t % (2 * np.pi)
        
        # Only render particles if they are physically inside the Cutaway void,
        # or randomly if they burst out. For brutalist clarity, show only exposed fluid!
        # The void is from 0 to Pi/2. We'll map the gas_rot base frame.
        base_t = (cur_t_mod - np.radians(gas_rot)) % (2 * np.pi)
        if base_t < T_MIN:
            r = D_R[i]
            x = r * np.sin(D_PHI[i]) * np.cos(cur_t_mod)
            y = r * np.cos(D_PHI[i])
            z = r * np.sin(D_PHI[i]) * np.sin(cur_t_mod)
            p_geom = generate_particle(np.array([x, y, z]), 5.0)
            process_faces(p_geom, C_PLASMA, 0.0) # Geometry already absolute
            
    # GENERATE AXI-SYMMETRIC MAGNETIC FIELD (Saturn Dipole)
    # The magnetic field rotates symmetrically with the planet
    mag_base_rot = gas_rot
    if True: # Force block execution
        m_long_arr = np.linspace(0, 2*np.pi, 8, endpoint=False)
        for ml in m_long_arr:
            # We cut away field lines that clip into the slice to keep optics clean
            l_mod = (ml - np.radians(mag_base_rot)) % (2*np.pi)
            if l_mod > T_MIN:
                for L in L_SHELLS:
                    arc = generate_magnetic_arc(L, ml, thickness=4.0)
                    process_faces(arc, C_MAG_FIELD, mag_base_rot)

    # EVALUATE MAGNETIC PLASMA KINEMATICS
    for i in range(N_PLASMA):
        cur_long = P_LONG[i] + np.radians(mag_base_rot)
        cur_phi = P_PHI[i] + t_sec * P_PHI_V[i]
        
        # Bounce mechanism along dipole line
        if cur_phi < 0.1: cur_phi = 0.2 - cur_phi; P_PHI_V[i] *= -1
        if cur_phi > np.pi - 0.1: cur_phi = 2*(np.pi - 0.1) - cur_phi; P_PHI_V[i] *= -1
        P_PHI[i] = cur_phi
        
        # Visibility filter (only show front/exposed arcs)
        base_l = (P_LONG[i]) % (2 * np.pi)
        if base_l > T_MIN:
            r = P_L[i] * (np.sin(cur_phi)**2)
            x = r * np.sin(cur_phi) * np.cos(cur_long)
            y = r * np.cos(cur_phi)
            z = r * np.sin(cur_phi) * np.sin(cur_long)
            p_geom = generate_particle(np.array([x, y, z]), 8.0)
            process_faces(p_geom, C_PLASMA, 0.0)

    # 5. ABSOLUTE DEPENDENCY SORT & RENDER
    sort_idx = np.argsort(centroids_z)[::-1] 
    sorted_faces = [faces_collected[i] for i in sort_idx]
    sorted_fcs = [face_colors[i] for i in sort_idx]
    
    if sorted_faces:
        ax.add_collection(PolyCollection(sorted_faces, facecolors=sorted_fcs, edgecolors='#111115', linewidths=0.4, joinstyle='miter'))

    # 6. HIGH-DENSITY HUD & TELEMETRY
    ax.add_patch(Rectangle((-540, 780), 1080, 180, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [780, 780], color=C_TEXT, lw=3, zorder=81)
    ax.text(-500, 880, "LG-413 :: PLANETARY DYNAMO TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 830, "[SFI-1.00] METALLIC HYDROGEN & MAGNETIC KINEMATICS", color=C_MAG_FIELD, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    prog = t_sec / DURATION
    if t_sec < 8.0:
        state_msg = "PHASE 1: THE ARCHITECTURAL CUTAWAY"
        state_col = C_GAS
        active_op = "GAS GIANT INTERIOR EXPOSED. 90-DEGREE VOID CLEARED."
    elif t_sec < 16.0:
        state_msg = "PHASE 2: DIFFERENTIAL FLUID ROTATION"
        state_col = C_DYNAMO
        active_op = "METALLIC HYDROGEN LAYER EXHIBITING HIGH-SPEED CORIOLIS SHEAR."
    else:
        state_msg = "PHASE 3: AXI-SYMMETRIC MAGNETIC OUTPUT"
        state_col = C_MAG_FIELD
        active_op = "DYNAMO GENERATES MASSIVE L-SHELL DIPOLE VECTORS."

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
    print(f"LG-413: MAGNETO-HYDRODYNAMIC TENSOR ENGAGED [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            pass
    print("Compilation Complete. Matrix resolved to exact topological magnetic yield.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
