"""
SOVEREIGN CODE: logic_garden_183_hypercube_entrainment.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / N-Dimensional Numpy Projections (17.5 seconds)
SCENE: Logic Garden 183 (The Enneract Entrainment / Dimensions 1 to 9)
HOTFIX: Dependency Injection (import math) & Logic Reordering
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import multiprocessing as mp
import os
import gc
import math  # HOTFIX: Dependency Transistor Re-Linked

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_183_hyperdimensional"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_DIM     = '#1A1A24'
C_CYAN    = '#00FFFF'          # Dimensions 1, 2, 3
C_MAGENTA = '#FF00FF'          # Dimensions 4, 5, 6
C_GOLD    = '#FFD700'          # Dimensions 7, 8, 9
C_RED     = '#FF0033'          # Photic Overload
C_MANTIS  = '#00FF00'          # Terminal Coherence (Tathātā)

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# MATHEMATICAL CONSTANTS & DIMENSIONAL ARCHITECTURE
# ------------------------------------------------------------------
def gen_hypercube(dim):
    vertices = []
    for i in range(2**dim):
        binary = bin(i)[2:].zfill(dim)
        vertices.append(np.array([float(bit)*2-1 for bit in binary]))
    vertices = np.array(vertices)
    
    edges = []
    num_v = len(vertices)
    for i in range(num_v):
        for j in range(i+1, num_v):
            if np.sum(vertices[i] != vertices[j]) == 1:
                edges.append((i, j))
    return vertices, edges

# Matrix Projections for N -> 3D
PROJ_MATRICES = {
    1: np.array([[1.0, 0, 0]]),
    2: np.array([[1.0, 0, 0], [0, 1.0, 0]]),
    3: np.array([[1.0, 0, 0], [0, 1.0, 0], [0, 0, 1.0]]),
    4: np.array([[1,0,0], [0,1,0], [0,0,1], [0.5, 0.5, 0.5]]),
    5: np.array([[1,0,0], [0,1,0], [0,0,1], [0.5, 0.5, 0], [0, 0.5, 0.5]]),
    6: np.array([[1,0,0], [0,1,0], [0,0,1], [0.5, 0.5, 0], [0, 0.5, 0.5], [0.5, 0, 0.5]]),
    7: np.array([[1,0,0], [0,1,0], [0,0,1], [0.5, 0.5, 0], [0, 0.5, 0.5], [0.5, 0, 0.5], [0.3, 0.3, 0.3]]),
    8: np.array([[1,0,0], [0,1,0], [0,0,1], [0.5, 0.5, 0], [0, 0.5, 0.5], [0.5, 0, 0.5], [0.3, 0.3, 0.3], [0.2, 0.2, 0]]),
    9: np.array([[1,0,0], [0,1,0], [0,0,1], [0.5, 0.5, 0], [0, 0.5, 0.5], [0.5, 0, 0.5], [0.3, 0.3, 0.3], [0.2, 0.2, 0], [0, 0.2, 0.2]])
}

def iso_project(vertices_3d):
    cos_30 = np.cos(np.radians(30))
    sin_30 = np.sin(np.radians(30))
    x = (vertices_3d[:, 0] - vertices_3d[:, 1]) * cos_30
    y = (vertices_3d[:, 0] + vertices_3d[:, 1]) * sin_30 - vertices_3d[:, 2]
    return np.column_stack((x, y))

def project_low_d_to_3d(v, dim):
    if dim == 1: return np.column_stack([v, np.zeros((v.shape[0], 2))])
    if dim == 2: return np.column_stack([v, np.zeros(v.shape[0])])
    return v

# Precompute structural data to avoid redundant processing
HC_DATA = {}
for dim in range(1, 10):
    v, e = gen_hypercube(dim)
    # Define rotation planes (up to dim-1 interconnected pairs to create complex tumbling)
    planes = [(i, (i + 1) % dim) for i in range(dim)] if dim > 1 else [(0, 0)]
    speeds = [i + 1.5 for i in range(len(planes))] if dim > 1 else [0]
    HC_DATA[dim] = {
        'v': v, 'e': e, 'planes': planes, 'speeds': speeds, 'nodes': len(v), 'edges': len(e)
    }

# Grid Offsets for the 9-Cubes
GRID_COORDS = {
    1: (180, 1350), 2: (540, 1350), 3: (900, 1350),
    4: (180, 950),  5: (540, 950),  6: (900, 950),
    7: (180, 550),  8: (540, 550),  9: (900, 550)
}
LABELS = ["1D: LINE", "2D: SQUARE", "3D: CUBE", "4D: TESSERACT", "5D: PENTERACT", "6D: HEXERACT", "7D: HEPTERACT", "8D: OCTERACT", "9D: ENNERACT"]

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, global_col, multiplier, do_snap, bg_flash = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_actual = C_TEXT if bg_flash else C_VOID
    fig.patch.set_facecolor(bg_actual)
    ax.set_facecolor(bg_actual)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    theta_base = (t_sec / 17.5) * 4 * np.pi * multiplier

    # Render each dimension in O(1) memory routing
    for dim in range(1, 10):
        cx, cy = GRID_COORDS[dim]
        c_data = HC_DATA[dim]
        
        v_current = np.copy(c_data['v'])
        
        # Apply N-Dimensional Rotation matrix
        if dim > 1 and not do_snap:
            for i, (d1, d2) in enumerate(c_data['planes']):
                theta = theta_base * c_data['speeds'][i]
                cos_t, sin_t = np.cos(theta), np.sin(theta)
                R = np.eye(dim)
                R[d1, d1] = cos_t; R[d1, d2] = -sin_t
                R[d2, d1] = sin_t; R[d2, d2] = cos_t
                v_current = np.dot(v_current, R)
                
        # 3D Projection -> Isometric -> Scaling
        v_3d = np.dot(v_current, PROJ_MATRICES[dim]) if dim > 3 else project_low_d_to_3d(v_current, dim)
        v_2d = iso_project(v_3d)
        
        # Dynamic Scaling (higher dimensions need slightly smaller base scales to fit)
        scale = 140 / (math.log(dim + 1) + 0.5)
        px = cx + v_2d[:, 0] * scale
        py = cy + v_2d[:, 1] * scale

        # Color Routing
        if global_col:
            dim_col = global_col 
            alpha = 1.0 if do_snap else max(0.1, 1.0 / (dim ** 0.6))
        else:
            dim_col = C_CYAN if dim <=3 else (C_MAGENTA if dim <=6 else C_GOLD)
            alpha = max(0.1, 1.0 / (dim ** 0.6))
            
        edge_w = 4.0 / dim

        # Draw Edges (Vectorized extraction is possible but direct plot is safe for matplotlib)
        edge_lines_x = []
        edge_lines_y = []
        for (i, j) in c_data['e']:
            edge_lines_x.extend([px[i], px[j], None])
            edge_lines_y.extend([py[i], py[j], None])
            
        ax.plot(edge_lines_x, edge_lines_y, color=dim_col, alpha=alpha, lw=edge_w, zorder=2)
        
        # Draw Nodes
        node_size = max(5, 50 / dim)
        ax.scatter(px, py, s=node_size, color=C_TEXT if do_snap else dim_col, zorder=3)
        
        # Draw Labels
        str_c = C_VOID if bg_flash else C_TEXT
        ax.text(cx, cy - 160, LABELS[dim-1], color=str_c, fontsize=14, fontname='monospace', alpha=0.6, ha='center', zorder=5)

    # ---------------------------------------------------
    # TELEMETRY WIDGETS
    # ---------------------------------------------------
    rect_c = C_VOID if not bg_flash else C_TEXT
    txt_c = C_TEXT if not bg_flash else C_VOID
    
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=rect_c, alpha=0.9, zorder=10))
    bar_col = global_col if global_col else C_CYAN
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=bar_col, lw=2, zorder=11)
    ax.text(0.04, 0.965, "LG-183 :: O(N) DIMENSION TENSOR COMPOSITE", transform=ax.transAxes, color=txt_c, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=11)

    ax.add_patch(plt.Rectangle((0, 0), 1, 0.12, transform=ax.transAxes, color=rect_c, alpha=0.95, zorder=10))
    ax.plot([0, 1], [0.12, 0.12], transform=ax.transAxes, color=bar_col, lw=2, zorder=11)
    
    # Mathematical Node Density Output
    density = sum(d['nodes'] for d in HC_DATA.values())
    links = sum(d['edges'] for d in HC_DATA.values())
    ax.text(0.04, 0.08, f"TOTAL NODES: {density} | EDGE KINEMATICS: {links}", transform=ax.transAxes, color=txt_c, fontsize=18, fontname='monospace', zorder=11)
    
    pulse = bar_col if (f % 10 < 5) or do_snap else txt_c
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=24, fontname='monospace', weight='bold', zorder=11)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f


# ------------------------------------------------------------------
# THERMODYNAMIC PHYSICS STREAM (TIMING ALIGNMENT)
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        # ---------------------------------------------------
        # PHASE 1: ALGORITHMIC ACCELERATION
        # ---------------------------------------------------
        if t_sec < 10.0:
            global_col = None
            multiplier = 1.0 + (t_sec / 5.0)
            do_snap = False
            bg_flash = False
            state = "[01] ALGORITHMIC TENSOR EXPANDING ACROSS DIMENSIONAL LATTICE"

        # ---------------------------------------------------
        # PHASE 2: DIMENSIONAL OVERLOAD (THE MIND-MELT)
        # ---------------------------------------------------
        elif t_sec < 14.8:
            multiplier = 3.0 + ((t_sec - 10.0)**2) * 0.5 # Exponential velocity
            do_snap = False
            bg_flash = False
            
            # Photic strobe logic
            if f % 8 < 4:
                global_col = C_MAGENTA
                state = "WARNING: O(N) OVERLOAD. OPTIC NERVE SATURATION ERROR."
            else:
                global_col = C_RED
                state = "CRITICAL: THERMODYNAMIC FRICTION EXCEEDING TOLERANCES."

        # ---------------------------------------------------
        # PHASE 3: THE ZEN COLLAPSE (TATHĀTĀ)
        # ---------------------------------------------------
        else:
            global_col = C_MANTIS
            multiplier = 0.0
            do_snap = True
            bg_flash = True if (t_sec >= 14.8 and t_sec < 14.95) else False 
            state = "TATHĀTĀ: DIMENSIONAL COMPILER ENGAGED. PERFECT ALIGNMENT."

        yield (f, t_sec, state, global_col, multiplier, do_snap, bg_flash)

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 183: THE ENNERACT ENTRAINMENT [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Render Mode: 3x3 O(1) Unified Matrix")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
