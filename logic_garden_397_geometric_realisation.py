"""
PROJECT: Logic Garden 397 (The Geometric Realisation // Quotient Space)
FORMAT: YouTube Shorts (1080x1920)
METADATA: TOPOLOGY, QUOTIENT SPACE, GEOMETRIC REALISATION, MANIFOLD FOLDING
EXECUTION: 24.0s Sequence. True 3D Mathematical Construction.
RULES ENFORCED: 
- Daylight Palette (White Substrate / High Contrast).
- Phase-Locked Metaphor: The literal mathematical folding of R^2/Z^2 into a Torus.
- True Line-of-Sight occlusion processing against brutalist topological blocks.
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
OUT_DIR = "frames_397_geometric_realisation"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG            = '#FFFFFF'  # Daylight / Absolute Void
C_TEXT          = '#111115'
C_EDGE          = '#111115'  # Indestructible Black for polygon bounds
C_C1            = '#005599'  # Deep Marine (Start of U/V grid)
C_C2            = '#FFB300'  # Dense Amber (End of U/V grid)
C_GUI           = '#64748B'

LIGHT_DIR = np.array([-0.6, 0.8, -0.4])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

# ------------------------------------------------------------------
# PHASE 1: PRE-COMPUTE THE ABSTRACT COMBINATORICS
# ------------------------------------------------------------------
np.random.seed(397)
print("PHASE 1: COMPUTING FRACTAL TOPOLOGY...")

U_RES, V_RES = 64, 32
u_arr = np.linspace(0, 2*np.pi, U_RES)
v_arr = np.linspace(0, 2*np.pi, V_RES)
uu, vv = np.meshgrid(u_arr, v_arr)

# Generate a structural color gradient tracking the exact coordinate space
# This ensures that when the edges weld together, the color continuity proves the exact topological parity.
c1_rgb = np.array(mcolors.to_rgb(C_C1))
c2_rgb = np.array(mcolors.to_rgb(C_C2))

uu_norm = uu / (2*np.pi)
vv_norm = vv / (2*np.pi)

# Rigid mapped grid colors (Base colour calculation)
r_grid = c1_rgb[0] * (1 - uu_norm) + c2_rgb[0] * uu_norm
g_grid = c1_rgb[1] * (1 - vv_norm) + c2_rgb[1] * vv_norm
b_grid = c1_rgb[2] * np.ones_like(uu_norm) # Deep anchor

color_matrix = np.stack((r_grid, g_grid, b_grid), axis=-1)

# Generate quad index matrices for O(1) rendering
idx = np.arange(U_RES * V_RES).reshape(V_RES, U_RES)
p1 = idx[:-1, :-1].flatten()
p2 = idx[:-1, 1:].flatten()
p3 = idx[1:, 1:].flatten()
p4 = idx[1:, :-1].flatten()

base_colors = color_matrix[:-1, :-1].reshape(-1, 3)

# ------------------------------------------------------------------
# KINEMATIC GEOMETRY PIPELINE
# ------------------------------------------------------------------
def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return 3 * x**2 - 2 * x**3

def evaluate_manifold(t):
    """
    Translates abstract topological rules into rigid Euclidean coordinates.
    Phase 1: Flat Cartesian Space.
    Phase 2: Mathematical Cylinder (Winding U).
    Phase 3: Perfect Torus (Winding V).
    """
    fold_1_prog = smoothstep(np.clip((t - 4.0) / 6.0, 0.0, 1.0))
    fold_2_prog = smoothstep(np.clip((t - 14.0) / 6.0, 0.0, 1.0))
    
    R_major = 500.0
    r_minor = 200.0
    flat_scale_u = 500.0
    flat_scale_v = 300.0
    
    u = uu.flatten()
    v = vv.flatten()
    
    # State 0: The Flat Abstract Polygon
    x0 = (u - np.pi) * flat_scale_u
    y0 = np.zeros_like(u)
    z0 = (v - np.pi) * flat_scale_v
    
    # State 1: The Cylinder (U wraps around to form a tube, V remains straight)
    x1 = flat_scale_u * 1.5 * np.cos(u)
    y1 = flat_scale_u * 1.5 * np.sin(u)
    z1 = z0
    
    # State 2: Geometric Realisation (Torus - V wraps to close the cylinder)
    x2 = (R_major + r_minor * np.cos(v)) * np.cos(u)
    y2 = r_minor * np.sin(v)
    z2 = (R_major + r_minor * np.cos(v)) * np.sin(u)
    
    # Interpolate Kinematics
    x = x0 * (1 - fold_1_prog) + x1 * fold_1_prog
    y = y0 * (1 - fold_1_prog) + y1 * fold_1_prog
    z = z0 * (1 - fold_1_prog) + z1 * fold_1_prog
    
    x_final = x * (1 - fold_2_prog) + x2 * fold_2_prog
    y_final = y * (1 - fold_2_prog) + y2 * fold_2_prog
    z_final = z * (1 - fold_2_prog) + z2 * fold_2_prog
    
    verts = np.column_stack((x_final, y_final, z_final))
    return verts

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
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540); ax.set_ylim(-960, 960)

    # 1. EVALUATE GEOMETRIC MANIFOLD
    verts = evaluate_manifold(t)
    
    # Assemble Quads
    M_RAW = np.stack((verts[p1], verts[p2], verts[p3], verts[p4]), axis=1)

    # 2. CINEMATIC OVERWATCH CAMERA
    # Continuous isometric orbital trace pulling backwards slightly as the mass expands
    cam_t = t * 0.2
    orbit_rad = 3200.0 + (t * 20.0) 
    cam_x = np.sin(cam_t) * orbit_rad
    cam_z = np.cos(cam_t) * orbit_rad
    cam_y = 2500.0 

    cam_pos = np.array([cam_x, cam_y, cam_z])
    target_pos = np.array([0, 0, 0]) 
    
    M_view = get_view_matrix(cam_pos, target_pos)
    view_polys = np.einsum('ij,knj->kni', M_view, M_RAW - cam_pos)

    # 3. SOLID LAMBERTIAN SHADING & DEPTH SORT
    centroids_z = np.mean(view_polys[:, :, 2], axis=1)
    
    v_mask = centroids_z > 50.0
    view_polys = view_polys[v_mask]
    poly_rgb = base_colors[v_mask]
    centroids_z = centroids_z[v_mask]

    if len(view_polys) > 0:
        # Generate World Space Normals to match exact light vectors
        w_polys = M_RAW[v_mask]
        v1_edge = w_polys[:, 1, :] - w_polys[:, 0, :]
        v2_edge = w_polys[:, 2, :] - w_polys[:, 0, :]
        norms = np.cross(v1_edge, v2_edge)
        n_len = np.linalg.norm(norms, axis=1, keepdims=True)
        norms /= np.maximum(n_len, 1e-5)
        
        diff = 0.2 + 0.8 * np.abs(np.dot(norms, LIGHT_DIR))
        
        final_rgba = np.zeros((len(view_polys), 4))
        for i in range(len(view_polys)):
            final_rgba[i, :3] = poly_rgb[i] * diff[i]
        final_rgba[:, 3] = 1.0

        z_safe = np.maximum(view_polys[:, :, 2], 1.0)
        proj_x = 2400.0 * (view_polys[:, :, 0] / z_safe)
        proj_y = 2400.0 * (view_polys[:, :, 1] / z_safe) + 100
        proj_polys = np.stack((proj_x, proj_y), axis=-1)

        sort_idx = np.argsort(centroids_z)[::-1]

        # Explicit Edge-Lined Brutalist Geometry matching Matt's specifications
        col = PolyCollection(proj_polys[sort_idx], facecolors=final_rgba[sort_idx], edgecolors=C_EDGE, linewidths=0.5, joinstyle='miter', zorder=10)
        ax.add_collection(col)

    # 4. HIGH-DENSITY HUD & TELEMETRY
    ax.add_patch(Rectangle((-540, 750), 1080, 210, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [750, 750], color=C_TEXT, lw=3, zorder=81)

    ax.text(-500, 890, "LG-397 :: GEOMETRIC REALISATION", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 840, "[SFI-1.00] TOPOLOGICAL QUOTIENT SPACE // R^2 TO T^2", color=C_GUI, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    # Phase Evaluator
    if t < 4.0:
        c_stat = C_C1
        s_text = "MATRIX STATUS: ABSTRACT FUNDAMENTAL POLYGON"
    elif t < 14.0:
        c_stat = C_C2
        s_text = "KINEMATIC FOLD 1: ISOMORPHISM TO BOUND CYLINDER"
    elif t < 22.0:
        c_stat = '#DF0000' # Intense Red during violent fold
        s_text = "KINEMATIC FOLD 2: TOPOLOGICAL EXTRUSION TO MANIFOLD"
    else:
        c_stat = '#00C853' # Jade Success
        s_text = "GEOMETRIC REALISATION: EXACT TOROID SECURED"

    ax.text(-500, -780, f"PROTOCOL YIELD   : {s_text}", color=c_stat, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"GEOMETRY VECTORS : {len(view_polys):06d} RIGID POLYGONS RENDERED", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"AXIOMATIC STATE  : MATHEMATICAL ABSTRACTION TRANSLATED TO PHYSICAL MATTER", color=C_TEXT, fontsize=12, fontname='monospace', zorder=82)
    
    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-397: TOPOLOGICAL REALISATION MATRIX [CORES: {cpu_cores}]")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=4):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")
    print("Compilation Complete. True Spatial Realisation Mapped.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
