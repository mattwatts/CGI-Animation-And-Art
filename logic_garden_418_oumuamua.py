"""
PROJECT: Logic Garden 418 (The 'Oumuamua Tensor // Interstellar Kinematics)
FORMAT: YouTube Shorts (1080x1920)
METADATA: OUMUAMUA, INTERSTELLAR, ASTROPHYSICS, KINEMATICS, NPA ROTATION
EXECUTION: 24.0s Sequence. True 3D Non-Principal Axis Rotation Matrix.
RULES ENFORCED:
- Daylight Palette (White Substrate / Deep Shadows).
- Exact realisational aspect of a highly elongated irradiated rocky body.
- Complex tumbling kinematics (Compound matrix rotation).
- Procedural multi-octave surface deformation for super realistic topography.
- Australian spelling conventions enforced natively (Maths, Colour, Optimise, Metres).
- Absolute O(N) volumetric arrays with Lambertian shading and True Deep-Sort.
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
OUT_DIR = "frames_418_oumuamua"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG            = '#FFFFFF'
C_TEXT          = '#111115'
C_ROCK_BASE     = '#451A03'  # Irradiated Tholin (Deep Reddish-Brown)
C_GUI           = '#64748B'

# Cinematic strong directional lighting for deep brutalist shadows
LIGHT_DIR = np.array([-0.7, 0.6, -0.4])
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
# O(N) PROCEDURAL ASTEROID MESH FACTORY
# ------------------------------------------------------------------
# Triaxial Ellipsoid Ratios (Length ~ 400m, Width ~ 60m)
R_A = 350.0 
R_B = 60.0
R_C = 60.0

print("PHASE 1: O(N) PROCEDURAL ROCK TOPOGRAPHY GENERATION...")
np.random.seed(418)

# Generate a high-density spherical mesh
res_phi = 50
res_theta = 100
phi = np.linspace(0, np.pi, res_phi)
theta = np.linspace(0, 2*np.pi, res_theta)
P, T = np.meshgrid(phi, theta)

# Base Ellipsoid mapping
X_base = np.sin(P) * np.cos(T)
Y_base = np.sin(P) * np.sin(T)
Z_base = np.cos(P)

# 3-Octave Pseudo-Noise function for photorealistic asteroid carving
noise_1 = np.sin(5 * X_base) * np.cos(5 * Y_base) * np.sin(5 * Z_base)
noise_2 = np.sin(12 * X_base + 1.5) * np.cos(12 * Z_base - 0.5)
noise_3 = np.cos(24 * Y_base) * np.sin(24 * X_base)

# Compile topological displacement matrix
noise_matrix = 1.0 + (0.15 * noise_1) + (0.08 * noise_2) + (0.03 * noise_3)

# Apply elongation vectors and structural noise
X_mesh = R_A * X_base * noise_matrix
Y_mesh = R_B * Y_base * noise_matrix
Z_mesh = R_C * Z_base * noise_matrix

ROCK_FACES = []
for i in range(res_theta - 1):
    for j in range(res_phi - 1):
        p1 = np.array([X_mesh[i][j],     Y_mesh[i][j],     Z_mesh[i][j]])
        p2 = np.array([X_mesh[i+1][j],   Y_mesh[i+1][j],   Z_mesh[i+1][j]])
        p3 = np.array([X_mesh[i+1][j+1], Y_mesh[i+1][j+1], Z_mesh[i+1][j+1]])
        p4 = np.array([X_mesh[i][j+1],   Y_mesh[i][j+1],   Z_mesh[i][j+1]])
        ROCK_FACES.append([p1, p2, p3, p4])

print(f"PHASE 2: TOPOLOGY LOCKED. GENERATED {len(ROCK_FACES)} TRUE POLYGONS.")

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f_idx):
    t_sec = f_idx / float(FPS)
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.]); ax.set_axis_off(); fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540); ax.set_ylim(-960, 960)

    # Static Observatory Camera
    cam_dist = 1100.0
    M_cam = rx(-15.0) @ ry(20.0) # Slight static observatory offset

    faces_collected = []
    face_colors = []
    centroids_z = []

    # EXACT TUMBLING KINEMATICS (Non-Principal Axis Rotation)
    # Combining rotations across all 3 axes explicitly maps the chaotic tumble.
    # Speeds visually amplified so dynamic movement is perfectly clear.
    w_x = t_sec * 32.0   
    w_y = t_sec * -12.0  
    w_z = t_sec * 18.0   
    M_ROCK = rx(w_x) @ ry(w_y) @ rz(w_z)

    c_base = np.array(mcolors.to_rgb(C_ROCK_BASE))

    # O(N) Lambertian Render Pipeline
    for face in ROCK_FACES:
        # 1. Apply Tumbling Matrix
        face_xform = np.einsum('ij,nj->ni', M_ROCK, face)
        
        # 2. Extract Normal Vector for physical shading
        v1 = face_xform[1] - face_xform[0]
        v2 = face_xform[2] - face_xform[0]
        norm = np.cross(v1, v2)
        n_len = np.linalg.norm(norm)
        if n_len > 0: norm /= n_len
        
        # 3. High-Contrast Lambertian Shadow Yield (Dark shadows, bright highlights)
        diff = 0.1 + 0.9 * np.clip(np.dot(norm, LIGHT_DIR), 0, 1)
        fc = np.append(c_base * diff, 1.0)
        
        # 4. Transform to Camera Space
        v_cam = np.einsum('ij,nj->ni', M_cam, face_xform)
        v_cam[:, 2] += cam_dist
        if np.any(v_cam[:, 2] < 10.0): continue
        
        # 5. Project to 2D Screen
        px = 1800.0 * (v_cam[:, 0] / v_cam[:, 2])
        # Slight upward offset for HUD clearance
        py = 1800.0 * (v_cam[:, 1] / v_cam[:, 2]) + 150.0 
        
        faces_collected.append(np.stack((px, py), axis=-1))
        face_colors.append(fc)
        centroids_z.append(np.mean(v_cam[:, 2]))

    # O(N) Absolute Painter's Algorithm Depth Sort
    sort_idx = np.argsort(centroids_z)[::-1]
    if faces_collected:
        sorted_faces = [faces_collected[i] for i in sort_idx]
        sorted_fcs = [face_colors[i] for i in sort_idx]
        
        # PolyCollection with thin edges enforcing brutalist geometric clarity
        ax.add_collection(PolyCollection(
            sorted_faces, facecolors=sorted_fcs, edgecolors='#111115', 
            linewidths=0.2, joinstyle='miter'
        ))

    # ================= 6. HIGH-DENSITY HUD & TELEMETRY =================
    ax.add_patch(Rectangle((-540, 800), 1080, 160, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=3, zorder=81)
    ax.text(-500, 900, "LG-418 :: 'OUMUAMUA KINEMATICS", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 850, "[SFI-1.00] EXACT REALISATIONAL ASPECT (NPA ROTATION)", color='#B45309', fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    prog = t_sec / DURATION
    if t_sec < 12.0:
        state_msg = "PHASE 1: MORPHOLOGICAL TOPOLOGY"
        state_col = '#B45309'
        active_op = "HIGHLY ELONGATED TRIAXIAL ELLIPSOID. ~400 METRES."
    else:
        state_msg = "PHASE 2: NON-PRINCIPAL AXIS ROTATION"
        state_col = '#DE008A'
        active_op = "COMPOUND GYROSCOPIC TUMBLING. NO STABLE YIELD."

    ax.text(-500, -780, f"PROTOCOL STATE : {state_msg}", color=state_col, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"DIAGNOSTIC     : {active_op}", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"AXIOMATIC TRUTH: EXTREME SHAPE AND CHAOTIC TUMBLE CONFIRM INTERSTELLAR ORIGIN.", color=C_TEXT, fontsize=11, fontname='monospace', zorder=82)

    ax.add_patch(Rectangle((-500, -920), 1000, 8, facecolor=C_GUI, zorder=82))
    ax.add_patch(Rectangle((-500, -920), 1000 * prog, 8, facecolor=state_col, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f_idx:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f_idx

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-418 ('OUMUAMUA MATRIX) ENGAGED [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            pass
    print("Compilation Complete. True interstellar tumbling kinematics resolved.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
