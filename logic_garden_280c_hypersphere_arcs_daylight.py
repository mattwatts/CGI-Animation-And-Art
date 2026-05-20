"""
SOVEREIGN CODE: logic_garden_280c_hypersphere_arcs_daylight.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / N-Dimensional Geodesic LineCollection
SCENE: LG-280c (1D-9D Geodesic Arcs / Temporal Dilation / Daylight Protocol)
HOTFIX: 40-Second Phase Expansion (2400 Frames), Exact Z-Depth Clamping
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 40.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_280c_hypersphere_arcs"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST ENGINEERING PALETTE --------
C_BG        = '#FFFFFF'        
C_IRON      = np.array([0.11, 0.16, 0.20]) # Bold Iron Forefront (#1C2833)
C_AZURE     = np.array([0.20, 0.60, 0.86]) # Azure Mid-Layer (#3498DB)
C_STEEL     = np.array([0.80, 0.82, 0.84]) # Receding Ghost Steel
C_TEXT      = '#111111'

# ------------------------------------------------------------------
# O(1) TOPOLOGICAL GEODESIC GENERATION
# ------------------------------------------------------------------
np.random.seed(280)
PTS_PER_ARC = 150

def generate_geodesics(dim):
    """
    Spawns structural great circles (arcs) wrapping the N-Sphere.
    Uses orthogonal bases generated via Gram-Schmidt scaling.
    """
    if dim == 1:
        # S^0 is two endpoints. The 'arc' representation is the structural 1D axis.
        t = np.linspace(-1, 1, PTS_PER_ARC)
        return np.expand_dims(t, axis=(0, 2)) # Shape (1, 150, 1)
        
    # Scale arc count dynamically up to higher complexity D-spaces
    n_arcs = 1 if dim == 2 else 4 * dim 
    arcs = []
    t = np.linspace(0, 2*np.pi, PTS_PER_ARC)
    
    for _ in range(n_arcs):
        u = np.random.randn(dim)
        u /= np.linalg.norm(u)
        v = np.random.randn(dim)
        v -= np.dot(u, v) * u
        v /= np.linalg.norm(v)
        
        # Geodesic loop mapping: r(t) = u*cos(t) + v*sin(t)
        arc = np.outer(np.cos(t), u) + np.outer(np.sin(t), v)
        arcs.append(arc)
        
    return np.array(arcs) # Shape: (n_arcs, PTS_PER_ARC, dim)

# Pre-compile the un-rotated rigid geometry structures
ARC_GEOMETRY = {dim: generate_geodesics(dim) for dim in range(1, 10)}

# Unified projection matrix from N-Space to 3D Base
P_9_3 = np.array([
    [1.0, 0.0, 0.0],  [0.0, 1.0, 0.0],  [0.0, 0.0, 1.0], 
    [0.5, 0.5, 0.0],  [0.0, 0.5, 0.5],  [0.5, 0.0, 0.5], 
    [0.3, 0.3, 0.3],  [0.2, 0.2, 0.0],  [0.0, 0.2, 0.2]
])

def project_nd_to_3d(v, dim):
    """Linear extraction of 3D shadows from N-Vectors"""
    if dim <= 3:
        res = np.zeros((*v.shape[:-1], 3))
        res[..., :dim] = v
        return res
    return np.dot(v, P_9_3[:dim, :])

def project_3d_to_2d_isometric(vertices_3d):
    """Isometric translation and Z-Depth extraction"""
    cos_30, sin_30 = np.cos(np.radians(30)), np.sin(np.radians(30))
    proj_x = (vertices_3d[..., 0] - vertices_3d[..., 1]) * cos_30
    proj_y = (vertices_3d[..., 0] + vertices_3d[..., 1]) * sin_30 - vertices_3d[..., 2]
    z_view = vertices_3d[..., 0] + vertices_3d[..., 1] + vertices_3d[..., 2]
    return np.stack((proj_x, proj_y), axis=-1), z_view

def rotate_nd_manifold(v, dim, phase):
    """Executes flawless integer-based multi-plane rotation loops"""
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
# PARALLEL RENDER WORKER (LineCollection Processing)
# ------------------------------------------------------------------
POS_MAP = {
    1: (220, 1440), 2: (540, 1440), 3: (860, 1440),
    4: (220, 1050), 5: (540, 1050), 6: (860, 1050),
    7: (220,  660), 8: (540,  660), 9: (860,  660)
}
LABELS = {
    1: "1D: BOUNDARY AXIS",  2: "2D: CIRCLE [S^1]",   3: "3D: SPHERE [S^2]",
    4: "4D: GLOME [S^3]",    5: "5D: 4-SPHERE ARCS",  6: "6D: 5-SPHERE ARCS",
    7: "7D: 6-SPHERE ARCS",  8: "8D: 7-SPHERE ARCS",  9: "9D: 8-SPHERE ARCS"
}
R_SCALE = 135.0 

def render_frame(f):
    phase = f / float(TOTAL_FRAMES)

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    fig.patch.set_facecolor(C_BG)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    # Global array storage to batch the entire continuous tensor
    all_segments = []
    all_z = []

    for dim in range(1, 10):
        cx, cy = POS_MAP[dim]
        
        # 1. Transform entire Arc Matrix through N-Space
        arcs_nd = rotate_nd_manifold(ARC_GEOMETRY[dim], dim, phase)
        # 2. Slice to 3D Space
        arcs_3d = project_nd_to_3d(arcs_nd, dim)
        # 3. Flare out to screen geometry and map Z-depth
        arcs_2d, z_view = project_3d_to_2d_isometric(arcs_3d)
        
        arcs_2d = arcs_2d * R_SCALE + np.array([cx, cy])

        # 4. Fracture geometries into infinitesmal rendering segments (p_i to p_i+1)
        # Shape arcs_2d: (n_arcs, 150, 2). Stack offset arrays to pair segments.
        segs = np.stack((arcs_2d[:, :-1, :], arcs_2d[:, 1:, :]), axis=2)
        segs = segs.reshape(-1, 2, 2)
        
        # Midpoint Z-depth evaluating color and thickness
        z_mid = (z_view[:, :-1] + z_view[:, 1:]) / 2.0
        z_mid = z_mid.reshape(-1)

        all_segments.append(segs)
        all_z.append(z_mid)
        
        # HUD Tag
        ax.text(cx, cy - 170, LABELS[dim], color=('#7F8C8D' if dim <=3 else '#1C2833'), 
                fontsize=11, fontname='monospace', weight='bold', ha='center', va='center', zorder=20)

    # 5. O(1) Unified LineCollection Sort & Render
    segs = np.concatenate(all_segments)
    z_mid = np.concatenate(all_z)

    # Scale Global Z
    z_min, z_max = z_mid.min() - 1e-5, z_mid.max() + 1e-5
    z_norm = (z_mid - z_min) / (z_max - z_min) 

    # Execute painter's algorithm by sorting segments back-to-front
    sort_idx = np.argsort(z_mid)
    segs = segs[sort_idx]
    z_norm = z_norm[sort_idx]

    # Pre-allocate rigid arrays
    rgba = np.zeros((len(z_norm), 4))
    lws = np.zeros(len(z_norm))

    m_back = z_norm < 0.5
    m_front = ~m_back

    # Ghostly Steel -> Azure transition for the receding volumes
    prog_back = z_norm[m_back] / 0.5
    rgba[m_back, :3] = C_STEEL * (1 - prog_back[:, None]) + C_AZURE * prog_back[:, None]
    rgba[m_back, 3]  = 0.10 + 0.35 * prog_back
    lws[m_back]      = 0.5 + 2.0 * prog_back

    # Azure -> Dark Iron transition for structures piercing front lens
    prog_front = (z_norm[m_front] - 0.5) / 0.5
    rgba[m_front, :3] = C_AZURE * (1 - prog_front[:, None]) + C_IRON * prog_front[:, None]
    rgba[m_front, 3]  = 0.45 + 0.45 * prog_front
    lws[m_front]      = 2.5 + 3.0 * prog_front

    # Dispatch to GPU via Matplotlib Collection Engine
    lc = LineCollection(segs, colors=rgba, linewidths=lws, capstyle='round', joinstyle='round', zorder=10)
    ax.add_collection(lc)

    # ------------------------------------------------------------------
    # DIAGNOSTIC HUD LAYER
    # ------------------------------------------------------------------
    ax.add_patch(Rectangle((0, 1840), 1080, 80, facecolor=C_BG, zorder=50))
    ax.text(40, 1880, f"LG-280c: O(1) TENSOR ARRAY // CONTINUOUS GEODESIC ARCS", color=C_TEXT, fontsize=18, fontname='monospace', weight='bold', va='center', zorder=51)

    ax.add_patch(Rectangle((0, 0), 1080, 100, facecolor=C_BG, zorder=50))
    ax.add_patch(Rectangle((0, 100), 1080, 2, facecolor=C_IRON, zorder=51))
    
    ax.text(40, 50, f"GEODESIC SEGMENTS [{len(segs):,}]", color='#3498DB', fontsize=22, fontname='monospace', weight='bold', va='center', zorder=51)
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
    print(f"LG-280c: GEODESIC HYPERSPHERES (40S DILATION) [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Continuous Wireframes // Temporal Dilation Topology")

    with mp.Pool(processes=cpu_cores) as pool:
        frames = range(TOTAL_FRAMES)
        for finished_frame in pool.imap_unordered(render_frame, frames, chunksize=16):
            pass
    print("Compilation Complete. 2400-Frame Geodesic Manifold Locked.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
