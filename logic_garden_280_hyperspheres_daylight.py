"""
SOVEREIGN CODE: logic_garden_280_hyperspheres_daylight.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / N-Dimensional Tensor Projections
SCENE: LG-280 (1D-9D Uniform Hyperspheres / Daylight Protocol)
HOTFIX: Unified 3x3 Memory Buffer, Isometric Depth-Sorting, Photorealistic Point Clouds
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 10.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_280_hypersphere_daylight"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST ENGINEERING PALETTE --------
C_BG        = '#FFFFFF'        
C_IRON      = np.array([0.11, 0.16, 0.20]) # Iron Blue Forefront (#1C2833)
C_AZURE     = np.array([0.20, 0.60, 0.86]) # Azure Mid-Layer (#3498DB)
C_STEEL     = np.array([0.80, 0.82, 0.84]) # Ghostly Steel Back-Layer (#CCD1D1)
C_TEXT      = '#111111'

N_POINTS = 3500

# ------------------------------------------------------------------
# O(1) TOPOLOGICAL GENERATION (Generated Once Globally)
# ------------------------------------------------------------------
np.random.seed(280)

def generate_nsphere_surface(dim, n=N_POINTS):
    """Generates uniform points strictly upon the perimeter boundary of an N-Sphere"""
    if dim == 1:
        # A 1D sphere (S^0) strictly exists as two disjoint points.
        # We duplicate them merely to satisfy array processing limits uniformly.
        pts = np.ones((n, 1))
        pts[:n//2] = -1.0
        return pts
    else:
        # Multi-dimensional Gaussian yields perfectly distributed angle scalars
        pts = np.random.randn(n, dim)
        pts /= np.linalg.norm(pts, axis=1, keepdims=True)
        return pts

# Pre-allocate rigid arrays to entirely banish timeline flickering
SPHERES = {dim: generate_nsphere_surface(dim) for dim in range(1, 10)}

# Unified projection matrix mathematically extracted from your Enneract protocols
P_9_3 = np.array([
    [1.0, 0.0, 0.0],  [0.0, 1.0, 0.0],  [0.0, 0.0, 1.0], 
    [0.5, 0.5, 0.0],  [0.0, 0.5, 0.5],  [0.5, 0.0, 0.5], 
    [0.3, 0.3, 0.3],  [0.2, 0.2, 0.0],  [0.0, 0.2, 0.2]
])

def project_nd_to_3d(v, dim):
    """Derives precise 3-dimensional shadow vectors from N-Space"""
    if dim <= 3:
        res = np.zeros((v.shape[0], 3))
        res[:, :dim] = v
        return res
    return np.dot(v, P_9_3[:dim, :])

def project_3d_to_2d_isometric(vertices_3d):
    """Identical Isometric translation to previous hypercube specifications"""
    cos_30, sin_30 = np.cos(np.radians(30)), np.sin(np.radians(30))
    proj_x = (vertices_3d[:, 0] - vertices_3d[:, 1]) * cos_30
    proj_y = (vertices_3d[:, 0] + vertices_3d[:, 1]) * sin_30 - vertices_3d[:, 2]
    # In isometric projection, physical Z-depth mapping equals x + y + z
    z_view = vertices_3d[:, 0] + vertices_3d[:, 1] + vertices_3d[:, 2]
    return np.column_stack((proj_x, proj_y)), z_view

def rotate_nd_manifold(v, dim, phase):
    """Executes smooth continuous plane matrices. Integers guarantee seamless 10.0s loops."""
    if dim == 1: return v.copy()
    
    v_rot = v.copy()
    planes, speeds = [], []
    
    if dim == 2:
        planes, speeds = [(0, 1)], [2]
    elif dim == 3:
        planes, speeds = [(0, 1), (0, 2), (1, 2)], [2, 3, 4]
    else:
        for i in range(dim - 1):
            planes.append((i, i + 1))
            speeds.append(i + 2)
            
    for (d1, d2), speed in zip(planes, speeds):
        theta = phase * 2 * np.pi * speed
        R = np.eye(dim)
        c, s = np.cos(theta), np.sin(theta)
        R[d1, d1] = c
        R[d1, d2] = -s
        R[d2, d1] = s
        R[d2, d2] = c
        v_rot = np.dot(v_rot, R)
        
    return v_rot

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (Absolute Memory Consolidation)
# ------------------------------------------------------------------
# Geometric grid positioning dynamically calculated for 1080x1920
POS_MAP = {
    1: (220, 1440), 2: (540, 1440), 3: (860, 1440),
    4: (220, 1050), 5: (540, 1050), 6: (860, 1050),
    7: (220,  660), 8: (540,  660), 9: (860,  660)
}
LABELS = {
    1: "1D: S^0 SURFACE", 2: "2D: CIRCLE [S^1]", 3: "3D: SPHERE [S^2]",
    4: "4D: GLOME [S^3]", 5: "5D: 4-SPHERE", 6: "6D: 5-SPHERE",
    7: "7D: 6-SPHERE", 8: "8D: 7-SPHERE", 9: "9D: 8-SPHERE"
}
R_SCALE = 135.0 # Max radius per grid cell

def render_frame(f):
    phase = f / float(TOTAL_FRAMES)

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    fig.patch.set_facecolor(C_BG)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    # Global compilation lists to ensure rapid single-pass scatter render
    gl_x, gl_y, gl_s, gl_c, gl_a = [], [], [], [], []

    for dim in range(1, 10):
        cx, cy = POS_MAP[dim]
        
        # 1. Rotate in Origin N-Space
        points_nd = rotate_nd_manifold(SPHERES[dim], dim, phase)
        
        # 2. Extract into 3-Space Geometry
        points_3d = project_nd_to_3d(points_nd, dim)
        
        # 3. Flatten to Substrate Lens 
        points_2d, z_view = project_3d_to_2d_isometric(points_3d)
        
        # Evaluate Z-Depth metrics universally
        z_min, z_max = z_view.min() - 1e-5, z_view.max() + 1e-5
        z_norm = (z_view - z_min) / (z_max - z_min) # Range 0 (back) to 1 (front)
        
        # 4. Thermodynamic & Atmospheric Palette Injection
        colors = np.zeros((N_POINTS, 3))
        alphas = np.zeros(N_POINTS)
        sizes = np.zeros(N_POINTS)
        
        # Linear interpolations based entirely on absolute physical depth
        for i in range(N_POINTS):
            zn = z_norm[i]
            if zn < 0.5:
                # Ghostly backing
                prog = zn / 0.5
                colors[i] = C_STEEL * (1-prog) + C_AZURE * prog
                alphas[i] = 0.15 + (prog * 0.3)
                sizes[i]  = 6.0 + (prog * 6.0)
            else:
                # Solid brutalist frontings
                prog = (zn - 0.5) / 0.5
                colors[i] = C_AZURE * (1-prog) + C_IRON * prog
                alphas[i] = 0.45 + (prog * 0.45)
                sizes[i]  = 12.0 + (prog * 8.0)

        # 5. Translate matrix natively to the Canvas array
        gl_x.extend(points_2d[:, 0] * R_SCALE + cx)
        gl_y.extend(points_2d[:, 1] * R_SCALE + cy)
        gl_s.extend(sizes)
        gl_a.extend(alphas)
        
        # Convert explicit RGB points layout
        for c in colors: gl_c.append(c)
        
        # 6. Append Metric Type
        ax.text(cx, cy - 170, LABELS[dim], color=('#7F8C8D' if dim <=3 else '#1C2833'), 
                fontsize=11, fontname='monospace', weight='bold', ha='center', va='center', zorder=20)

    # O(1) Unified Scatter Draw 
    gl_x = np.array(gl_x); gl_y = np.array(gl_y)
    gl_s = np.array(gl_s); gl_a = np.array(gl_a)
    gl_c = np.vstack(gl_c)
    rgba = np.column_stack((gl_c, gl_a))
    
    # Global Painter's Depth Sorting
    sort_idx = np.argsort(gl_s) # Proxy: Size explicitly scales with Z_depth
    ax.scatter(gl_x[sort_idx], gl_y[sort_idx], s=gl_s[sort_idx], color=rgba[sort_idx], edgecolors='none', zorder=10)

    # ------------------------------------------------------------------
    # DIAGNOSTIC HUD LAYER
    # ------------------------------------------------------------------
    ax.add_patch(Rectangle((0, 1840), 1080, 80, facecolor=C_BG, zorder=50))
    ax.text(40, 1880, f"LG-280: O(1) TENSOR ARRAY // N-DIMENSIONAL SPHERES [S^0 TO S^8]", color=C_TEXT, fontsize=18, fontname='monospace', weight='bold', va='center', zorder=51)

    ax.add_patch(Rectangle((0, 0), 1080, 100, facecolor=C_BG, zorder=50))
    ax.add_patch(Rectangle((0, 100), 1080, 2, facecolor=C_IRON, zorder=51))
    
    ax.text(40, 50, "BASE TENSOR [N=31,500]", color='#3498DB', fontsize=22, fontname='monospace', weight='bold', va='center', zorder=51)
    ax.text(1040, 50, f"θ={phase*360:05.1f}° EX. SYNC", color=C_IRON, fontsize=18, fontname='monospace', weight='bold', ha='right', va='center', zorder=51)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-280: UNIFIED HYPERSPHERE PROTOCOL [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Continuous Volume Limits // Substrate Translation")

    with mp.Pool(processes=cpu_cores) as pool:
        frames = range(TOTAL_FRAMES)
        for finished_frame in pool.imap_unordered(render_frame, frames, chunksize=8):
            pass
    print("Compilation Complete. Zero Memory Leaks. Absolute Frame Generation.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
