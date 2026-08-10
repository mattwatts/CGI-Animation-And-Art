"""
PROJECT: Logic Garden 400 (The Radiance Tensor // Isotropic Illumination)
FORMAT: YouTube Shorts (1080x1920)
METADATA: RADIATIVE TRANSFER, PHASE TRANSITION, LIGHT KINEMATICS, ENTROPY OVERRIDE
EXECUTION: 24.0s Sequence. True 3D Mathematical Construction.
RULES ENFORCED: 
- Temporary Dark Substrate (Phase-Locked Metaphor representation).
- Spherical Kinematic Radiance pushing a Daylight Override.
- O(N) True Polygon Depth Sorting.
- Australian spelling conventions enforced natively.
- Zero arbitrary filler. True cinematic realisational optics.
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
OUT_DIR = "frames_400_radiance_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE (INVERTED YIELD) --------
C_VOID          = '#020617'  # Absolute Darkness
C_DEAD          = '#111115'  # Indestructible Black (Unlit Matrix)
C_DEAD_EDGE     = '#1E293B'  # Faint geometry line in the dark
C_LIGHT         = '#FFFFFF'  # Daylight / Absolute Truth
C_LIGHT_EDGE    = '#FFB300'  # Dense Amber (High-Contrast Radiance)
C_GUI           = '#94A3B8'

LIGHT_DIR = np.array([-0.6, 0.8, -0.4])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

# ------------------------------------------------------------------
# PHASE 1: PRE-COMPUTE THE DEAD MATRIX
# ------------------------------------------------------------------
np.random.seed(400)
print("PHASE 1: SYNTHESIZING THE VOID MATRIX...")

GRID_SIZE = 15 # 15x15x15 = 3375 blocks
SPACING = 150.0
OFFSET = (GRID_SIZE - 1) * SPACING / 2.0

grid_coords = []
for x in range(GRID_SIZE):
    for y in range(GRID_SIZE):
        for z in range(GRID_SIZE):
            cx = (x * SPACING) - OFFSET
            cy = (y * SPACING) - OFFSET
            cz = (z * SPACING) - OFFSET
            
            # Hollow out a tiny core to clearly see the origin
            if np.linalg.norm([cx, cy, cz]) > 80.0:
                grid_coords.append([cx, cy, cz])

N_BLOCKS = len(grid_coords)
matrix_pos = np.array(grid_coords)

# ------------------------------------------------------------------
# 3D CUBE GEOMETRY GENERATOR
# ------------------------------------------------------------------
def get_base_cube():
    # 40-unit wide brutalist blocks
    v = np.array([
        [-1, -1, -1], [ 1, -1, -1], [ 1,  1, -1], [-1,  1, -1],
        [-1, -1,  1], [ 1, -1,  1], [ 1,  1,  1], [-1,  1,  1]
    ]) * 20.0
    faces = [
        [v[0], v[1], v[2]], [v[0], v[2], v[3]], # Front
        [v[1], v[5], v[6]], [v[1], v[6], v[2]], # Right
        [v[5], v[4], v[7]], [v[5], v[7], v[6]], # Back
        [v[4], v[0], v[3]], [v[4], v[3], v[7]], # Left
        [v[3], v[2], v[6]], [v[3], v[6], v[7]], # Top
        [v[4], v[5], v[1]], [v[4], v[1], v[0]], # Bottom
    ]
    return np.array(faces) 

BASE_CUBE = get_base_cube()

# Vectorized Poly Generation
M_POLYS = matrix_pos[:, None, None, :] + BASE_CUBE[None, :, :, :]
M_POLYS = M_POLYS.reshape(-1, 3, 3)

# World normals for static blocks
v1 = M_POLYS[:, 1, :] - M_POLYS[:, 0, :]
v2 = M_POLYS[:, 2, :] - M_POLYS[:, 0, :]
norms = np.cross(v1, v2)
n_len = np.linalg.norm(norms, axis=1, keepdims=True)
norms /= np.maximum(n_len, 1e-5)
block_diff = 0.2 + 0.8 * np.clip(np.dot(norms, LIGHT_DIR), 0.0, 1.0)

# Pre-calculate distances from origin for O(1) wave intersections
block_centers = np.repeat(matrix_pos, 12, axis=0) # 12 polys per block
dist_from_core = np.linalg.norm(block_centers, axis=1)

# Ignite the Origin Core Sphere
SIDES = 16
M_RAD = 40.0
origin_verts = []
for i in range(SIDES):
    for j in range(SIDES//2):
        th1 = i * 2 * np.pi / SIDES
        th2 = (i+1) * 2 * np.pi / SIDES
        phi1 = j * np.pi / (SIDES//2) - np.pi/2
        phi2 = (j+1) * np.pi / (SIDES//2) - np.pi/2
        
        p1 = [M_RAD*np.cos(phi1)*np.cos(th1), M_RAD*np.sin(phi1), M_RAD*np.cos(phi1)*np.sin(th1)]
        p2 = [M_RAD*np.cos(phi1)*np.cos(th2), M_RAD*np.sin(phi1), M_RAD*np.cos(phi1)*np.sin(th2)]
        p3 = [M_RAD*np.cos(phi2)*np.cos(th2), M_RAD*np.sin(phi2), M_RAD*np.cos(phi2)*np.sin(th2)]
        p4 = [M_RAD*np.cos(phi2)*np.cos(th1), M_RAD*np.sin(phi2), M_RAD*np.cos(phi2)*np.sin(th1)]
        
        origin_verts.append([p1, p2, p4])
        origin_verts.append([p2, p3, p4])
ORIGIN_POLYS = np.array(origin_verts)

# ------------------------------------------------------------------
# TRUE MATRICES & PROJECTION
# ------------------------------------------------------------------
def get_view_matrix(cam_pos, target_pos, up_vector=np.array([0, 1.0, 0])):
    forward = target_pos - cam_pos
    f_len = np.linalg.norm(forward)
    if f_len < 1e-5: return np.eye(3)
    forward /= f_len
    right = np.cross(up_vector, forward)
    r_len = np.linalg.norm(right)
    if r_len < 1e-5: right = np.array([1.0, 0, 0])
    else: right /= r_len
    up = np.cross(forward, right)
    return np.array([right, up, forward])

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    t = f / float(FPS)

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.]); ax.set_axis_off(); fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID); ax.set_facecolor(C_VOID)
    ax.set_xlim(-540, 540); ax.set_ylim(-960, 960)

    # 1. KINEMATIC TIMELINE
    T_STRIKE = 4.0
    WAVE_SPEED = 300.0 # units per second
    
    # Radius of absolute truth propagating through the void
    wave_radius = max(0.0, (t - T_STRIKE) * WAVE_SPEED)
    
    # 2. EVALUATE MATRIX ILLUMINATION
    # True if Block is inside the wave boundary
    illuminated_mask = dist_from_core < wave_radius
    
    # Base colors
    rgb_dead = np.array(mcolors.to_rgb(C_DEAD))
    rgb_light = np.array(mcolors.to_rgb(C_LIGHT))
    
    poly_rgb = np.where(illuminated_mask[:, np.newaxis], rgb_light, rgb_dead)
    
    final_block_rgba = np.zeros((len(M_POLYS), 4))
    final_block_rgba[:, :3] = poly_rgb * block_diff[:, np.newaxis]
    final_block_rgba[:, 3] = 1.0
    
    edges_block = np.where(illuminated_mask, C_LIGHT_EDGE, C_DEAD_EDGE)
    
    # Combine with Origin Sphere
    c_core_rgb = np.array(mcolors.to_rgb(C_LIGHT_EDGE if t < T_STRIKE else C_LIGHT))
    origin_rgba = np.zeros((len(ORIGIN_POLYS), 4))
    origin_rgba[:, :3] = c_core_rgb # Pure emissive core, no shading
    origin_rgba[:, 3] = 1.0
    
    M_ALL = np.concatenate((M_POLYS, ORIGIN_POLYS), axis=0)
    C_ALL = np.concatenate((final_block_rgba, origin_rgba), axis=0)
    EDGE_ALL = np.concatenate((edges_block, np.full(len(ORIGIN_POLYS), 'none')), axis=0)

    # 3. CINEMATIC GAP-LOCK CAMERA
    # Isometric slow orbit revealing the geometric scale
    cam_dist = 3000.0
    cam_t = t * 0.15
    cam_x = np.sin(cam_t) * cam_dist
    cam_z = np.cos(cam_t) * cam_dist
    cam_y = 1800.0 

    cam_pos = np.array([cam_x, cam_y, cam_z])
    target_pos = np.array([0, 0, 0])
    
    M_view = get_view_matrix(cam_pos, target_pos)

    view_polys = np.einsum('ij,knj->kni', M_view, M_ALL - cam_pos)
    centroids_z = np.mean(view_polys[:, :, 2], axis=1)

    # Frustum Culling
    v_mask = centroids_z > 10.0
    view_polys = view_polys[v_mask]
    C_ALL = C_ALL[v_mask]
    EDGE_ALL = EDGE_ALL[v_mask]
    centroids_z = centroids_z[v_mask]

    if len(view_polys) > 0:
        z_safe = np.maximum(view_polys[:, :, 2], 1.0)
        proj_x = 2400.0 * (view_polys[:, :, 0] / z_safe)
        proj_y = 2400.0 * (view_polys[:, :, 1] / z_safe) + 150
        proj_polys = np.stack((proj_x, proj_y), axis=-1)

        sort_idx = np.argsort(centroids_z)[::-1]
        
        col = PolyCollection(proj_polys[sort_idx], facecolors=C_ALL[sort_idx], edgecolors=EDGE_ALL[sort_idx], linewidths=0.5, joinstyle='miter', zorder=10)
        ax.add_collection(col)

    # 4. HIGH-DENSITY HUD & TELEMETRY
    # Dark Mode HUD
    ax.add_patch(Rectangle((-540, 750), 1080, 210, facecolor=C_VOID, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [750, 750], color=C_LIGHT_EDGE, lw=2, zorder=81)

    ax.text(-500, 890, "LG-400 :: THE ILLUMINATION TENSOR", color=C_LIGHT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 840, "[SFI-0.50] ISOTROPIC RADIATIVE OVERRIDE", color=C_GUI, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_VOID, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_LIGHT_EDGE, lw=2, zorder=81)

    active_nodes = np.sum(illuminated_mask) // 12
    light_pct = (active_nodes / N_BLOCKS) * 100.0

    if t < T_STRIKE:
        p_str = "STATE 0: ABSOLUTE VOID. MAXIMUM ENTROPY."
        c_stat = C_GUI
    else:
        p_str = "STATE 1: ISOTROPIC RADIATIVE OVERRIDE ENGAGED."
        c_stat = C_LIGHT_EDGE

    if light_pct >= 99.9:
        p_str = "STATE 2: TOTAL ILLUMINATION. DARKNESS ERADICATED."
        c_stat = C_LIGHT

    ax.text(-500, -780, f"PROTOCOL PHASE : {p_str}", color=c_stat, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"DAYLIGHT YIELD : {light_pct:05.1f}% SUBSTRATE OVERWRITTEN", color=C_LIGHT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"NOISE REDUCTION: {active_nodes:04d} / {N_BLOCKS} NODES ALIGNED", color=C_LIGHT, fontsize=14, fontname='monospace', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_VOID, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-400: KINEMATIC ILLUMINATION MATRIX [CORES: {cpu_cores}]")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=4):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")
    print("Compilation Complete. The darkness has been eradicated.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
