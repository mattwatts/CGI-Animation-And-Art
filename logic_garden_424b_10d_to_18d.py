"""
PROJECT: Logic Garden 424b (The Ascendant Topology Grid // Optical Saturation Tensor)
FORMAT: YouTube Shorts (1080x1920)
METADATA: 18D, HYPERCUBE, MATHEMATICS, O(1) SUB-PIXEL DECIMATION, BITWISE XOR
EXECUTION: 45.0s Sequence.
RULES ENFORCED:
- 3x3 Combinatorial Grid mathematically scaled exactly.
- O(D * 2^D) VECTORISATION: Bypasses the 68.7 billion operation limit.
- OPTICAL SATURATION LIMIT: Capped to 120,000 rendering edges per sector to prevent C++ Agg Backend buffer collapse.
- Daylight Palette (White Substrate / High-Contrast Deep Marine).
- Sovereign Explicit 'Architect's Dials' exposed. 
- Australian spelling conventions enforced natively (Maths, Colour, Optimise).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
# Massive backend optimisations to prevent LineCollection stalling
matplotlib.rcParams['path.simplify'] = True
matplotlib.rcParams['path.simplify_threshold'] = 1.0
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 24
ROTATION_TIME_SECONDS = 45.0 
TOTAL_FRAMES = int(FPS * ROTATION_TIME_SECONDS)
OUT_DIR = "frames_424_10d_to_18d"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG    = '#FFFFFF'
C_TEXT  = '#111115'
C_EDGE  = '#005599'
C_NODE  = '#111115'
C_GUI   = '#64748B'

# ------------------------------------------------------------------
# O(1) BARE-METAL BITWISE MESH GENERATOR (The Breakthrough Algorithm)
# ------------------------------------------------------------------
def generate_hypercube_fast(dim):
    """Evaluates vertices and edges via strict NumPy broadcast logic."""
    num_pts = 2**dim
    
    # O(1) Vertices
    arr = np.arange(num_pts, dtype=np.int32)[:, None]
    shift = np.arange(dim - 1, -1, -1, dtype=np.int32)
    vertices = ((arr >> shift) & 1).astype(np.float32) * 2.0 - 1.0
    
    # O(1) Edges
    i = np.arange(num_pts, dtype=np.int32)[:, None]
    k_shifts = 1 << np.arange(dim, dtype=np.int32)
    j = i ^ k_shifts
    mask = i < j 
    
    edge_i = np.broadcast_to(i, j.shape)[mask]
    edge_j = j[mask]
    edges = np.column_stack((edge_i, edge_j))
    
    return vertices, edges

# ------------------------------------------------------------------
# PROJECTION MATRICES
# ------------------------------------------------------------------
def get_projection_matrix(dim):
    base = np.array([
        [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0],
        [0.5, 0.5, 0.0], [0.0, 0.5, 0.5], [0.5, 0.0, 0.5],
        [0.3, 0.3, 0.3], [0.2, 0.2, 0.0], [0.0, 0.2, 0.2],
        [0.2, 0.0, 0.2], [0.1, 0.1, 0.0], [0.05, 0.05, 0.05],
        [0.05, 0.0, 0.05], [0.02, 0.02, 0.02], [0.01, 0.01, 0.00],
        [0.005, 0.01, 0.01], [0.01, 0.005, 0.01], [0.01, 0.01, 0.005]
    ])
    return base[:dim]

def project_3d_to_2d_isometric(vertices_3d):
    cos_30 = np.cos(np.radians(30))
    sin_30 = np.sin(np.radians(30))
    proj_x = (vertices_3d[:, 0] - vertices_3d[:, 1]) * cos_30
    proj_y = (vertices_3d[:, 0] + vertices_3d[:, 1]) * sin_30 - vertices_3d[:, 2]
    return proj_x, proj_y

# ------------------------------------------------------------------
# GEOMETRIC CONSTANTS AND HYPER-ARRAYS
# ------------------------------------------------------------------
DIMS = list(range(10, 19)) # [10, 11, 12, ... 18]

# 3x3 Coordinate Matrix Layout
LAYOUT_X = [-350.0, 0.0, 350.0]
LAYOUT_Y = [ 600.0, 0.0,-600.0]

def get_density_dials(dim):
    """
    ARCHITECT'S DENSITY TENSOR
    Adjusted based on the post-stride decimation geometry to preserve visual volume.
    """
    scales = {
        10: (0.250, 0.500, 1.5),  # 5k Edges
        11: (0.200, 0.400, 1.0),  # 11k Edges
        12: (0.150, 0.300, 0.5),  # 24k Edges
        13: (0.080, 0.250, 0.2),  # 53k Edges
        14: (0.060, 0.200, 0.0),  # 114k Edges
        15: (0.050, 0.150, 0.0),  # Sub-Pixel Decimation occurs here. Stride caps at ~120K.
        16: (0.040, 0.100, 0.0),
        17: (0.030, 0.080, 0.0),
        18: (0.020, 0.050, 0.0)   
    }
    return scales.get(dim, (0.02, 0.05, 0.0))

# ------------------------------------------------------------------
# THE OPTIMAL SUB-PIXEL SATURATION PRE-PROCESSOR
# ------------------------------------------------------------------
print(f"LG-424b: OPTICAL SATURATION LIMIT TRANSDUCER ENGAGED.")

MASTER_V = {}
MASTER_E = {}
MASTER_P = {}
MASTER_S = {}
MASTER_E_COUNT = {}

MAX_LINES_PER_SECTOR = 120000

for d in DIMS:
    v, e = generate_hypercube_fast(d)
    MASTER_V[d] = v
    MASTER_P[d] = get_projection_matrix(d)
    
    # Calculate base bounds to lock uniform scale exactly
    base_proj_3d = np.dot(v, MASTER_P[d])
    bx, by = project_3d_to_2d_isometric(base_proj_3d)
    max_extent = np.max(np.abs(np.column_stack((bx, by))))
    
    # Lock boundary to perfectly fit 145-radius tile layout
    MASTER_S[d] = 145.0 / max_extent

    true_lines = len(e)
    MASTER_E_COUNT[d] = true_lines
    
    # THE OPTICAL SATURATION DECIMATOR
    if true_lines > MAX_LINES_PER_SECTOR:
        stride = (true_lines // MAX_LINES_PER_SECTOR) + 1
        e_decimated = e[::stride]
        print(f"[{d}D] {true_lines:>9,d} Edges -> Decimated to {len(e_decimated):>7,d} (Stride {stride})")
        MASTER_E[d] = e_decimated
    else:
        MASTER_E[d] = e
        print(f"[{d}D] Solved: {len(v):>7,d} Vertices | {len(e):>9,d} Edges (Native)")

total_active_edges = sum(len(e) for e in MASTER_E.values())
print(f"\nARRAY BOUNDED. Total active vectors per frame: {total_active_edges:,d} (Preventing Agg Backend RAM Crash)")

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(frame_idx):
    theta_base = (frame_idx / TOTAL_FRAMES) * 2 * np.pi

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(C_BG)
    fig.patch.set_facecolor(C_BG)
    
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')

    # Draw Matrix Subsections
    for grid_i, dim in enumerate(DIMS):
        pos_x = LAYOUT_X[grid_i % 3]
        pos_y = LAYOUT_Y[grid_i // 3]

        verts = np.copy(MASTER_V[dim])
        edges = MASTER_E[dim]
        
        # Apply N-Dimensional Cascading Rotations
        rot_planes = [(x, (x+1)%dim) for x in range(dim)]
        rot_speeds = list(range(2, dim + 2))
        
        for p_idx, (d1, d2) in enumerate(rot_planes):
            theta = theta_base * rot_speeds[p_idx]
            cos_t, sin_t = np.cos(theta), np.sin(theta)
            
            R_plane = np.identity(dim)
            R_plane[d1, d1] = cos_t
            R_plane[d1, d2] = -sin_t
            R_plane[d2, d1] = sin_t
            R_plane[d2, d2] = cos_t
            
            verts = np.dot(verts, R_plane)

        # 3D and 2D Projections
        p3d = np.dot(verts, MASTER_P[dim])
        px, py = project_3d_to_2d_isometric(p3d)
        
        # Absolute Grid Scale & Offset Translation
        scl = MASTER_S[dim]
        px = (px * scl) + pos_x
        py = (py * scl) + pos_y

        e_alpha, e_width, n_size = get_density_dials(dim)

        # O(1) VECTORISED LINE COMPILATION
        points_2d = np.column_stack((px, py))
        lines = np.zeros((len(edges), 2, 2), dtype=np.float32)
        lines[:, 0] = points_2d[edges[:, 0]]
        lines[:, 1] = points_2d[edges[:, 1]]
        
        # Adding to strict C-backend Matplotlib stack
        ax.add_collection(LineCollection(lines, colors=C_EDGE, alpha=e_alpha, linewidths=e_width, zorder=2))

        if n_size > 0.0:
            ax.scatter(px, py, s=n_size, color=C_NODE, zorder=3, edgecolors='none')

        # Tile Labeling
        bbox_props = dict(boxstyle="square,pad=0.3", fc=C_BG, ec=C_TEXT, lw=2)
        ax.text(pos_x, pos_y - 180, f"{dim}D HYPER-TENSOR", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', ha='center', va='top', zorder=85, bbox=bbox_props)
        # Note: We display the TRUE mathematical edges, even if sub-pixel logic conceals them on rendering.
        true_edges = MASTER_E_COUNT[dim]
        ax.text(pos_x, pos_y - 215, f"{true_edges:,} EDGES", color=C_GUI, fontsize=12, fontname='monospace', weight='bold', ha='center', va='top', zorder=85)

    # -------------------------------------------------------------
    # ABSOLUTE UI TELEMETRY
    # -------------------------------------------------------------
    ax.add_patch(Rectangle((-540, 800), 1080, 160, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=3, zorder=81)
    ax.text(-500, 900, "LG-424b :: ASCENDANT TOPOLOGY GRID", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 850, f"[SFI-1.00] 10D TO 18D GEOMETRIC HORIZON", color=C_GUI, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)
    
    ax.text(-500, -780, f"PROTOCOL STATE : TATHATA MATHEMATICAL ROTATION", color=C_EDGE, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"DIAGNOSTIC     : SUB-PIXEL SATURATION DECIMATION ENGAGED.", color=C_TEXT, fontsize=13, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"AXIOMATIC TRUTH: A 18D SECTOR OCCUPIES 129,600 PIXELS. DRAWING 2.3 MILLION LINES CAUSES BUFFER\nOVERFLOW. THE ARRAY MATHEMATICALLY STRIDES GEOMETRY TO RENDER TRUE OPTICAL DENSITY.", color=C_TEXT, fontsize=9.5, fontname='monospace', zorder=82)

    frame_filename = os.path.join(OUT_DIR, f"frame_{frame_idx:04d}.png")
    plt.savefig(frame_filename, facecolor=C_BG, edgecolor='none')

    fig.clf()
    plt.close(fig)
    gc.collect()

    return frame_idx

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"EXECUTING VECTORISED RENDERING [CORES: {cpu_cores}]")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=2) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES)):
            if (finished_frame + 1) % 10 == 0:
                print(f"Matrix Resolved: Frame {finished_frame + 1} / {TOTAL_FRAMES}")

    print("\nCompilation Complete. Buffer Overflows Defeated.")

if __name__ == '__main__':
    mp.freeze_support()
    run_batch()
