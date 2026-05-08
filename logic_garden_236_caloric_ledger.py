"""
SOVEREIGN CODE: logic_garden_236_caloric_ledger.py
SYSTEM: Python Multicore / O(1) QUBO Topology
SCENE: Logic Garden 236 (The Caloric Ledger / Optimal Foraging)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Dimensional Axis Align / Dynamic Particle Limit Clamping

[INSTRUCTION]: RENDER_MODE explicitly set to "ZEN" for the 17.5s flow cycle.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
RENDER_MODE = "ZEN"  
DURATION = 17.5
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_236_caloric_ledger"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS) --------
C_BG        = '#FFFFFF'        # Low-Entropy Canvas (The Void)
C_TEXT      = '#020205'        # High-Contrast Data Load / Superposition Vectors
C_DIM       = '#A0A0A5'        # J_ij Penalty Walls / Hostile Topography
C_MAGENTA   = '#FF0055'        # Sub-optimal Route Decay / Caloric Debt
C_GOLD      = '#FFB300'        # Thermal Friction / Kinetic Exhaustion
C_CYAN      = '#00FFFF'        # State Collapse / The Absolute Optimal Path
C_MANTIS    = '#00FF00'        # h_i Caloric Nodes / Resource Patches

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_dim     = np.array(hex_to_rgba(C_DIM)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_gold    = np.array(hex_to_rgba(C_GOLD)[:3])
c_cyan    = np.array(hex_to_rgba(C_CYAN)[:3])
c_mantis  = np.array(hex_to_rgba(C_MANTIS)[:3])

# ------------------------------------------------------------------
# O(1) 3D TENSOR ALGEBRA 
# ------------------------------------------------------------------
def rotate_3d(points, rx, ry, rz):
    cx, sx = np.cos(rx), np.sin(rx)
    cy, sy = np.cos(ry), np.sin(ry)
    cz, sz = np.cos(rz), np.sin(rz)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cx, 0], [0, 0, 1]])
    R = Rz.dot(Ry).dot(Rx)
    return points.dot(R.T)

# ------------------------------------------------------------------
# BASE GEOMETRY ARRAYS: THE QUBO TOPOLOGY
# ------------------------------------------------------------------
np.random.seed(909) # Absolute matrix lock

# 1. The Penalty Landscape (J_ij Hostile Geometry)
GV = np.linspace(-120, 120, 140)
X, Y = np.meshgrid(GV, GV)
px_land = X.flatten() # 19,600 points
py_land = Y.flatten()
# Hostile, jagged transit walls
pz_land = 20.0 * np.sin(px_land * 0.15) * np.cos(py_land * 0.15) + (px_land**2 + py_land**2) * 0.002 - 30.0

# 2. The Caloric Nodes (h_i)
NUM_NODES = 25 # 25 points
px_nodes = np.random.uniform(-100, 100, NUM_NODES)
py_nodes = np.random.uniform(-100, 100, NUM_NODES)
pz_nodes = 20.0 * np.sin(px_nodes * 0.15) * np.cos(py_nodes * 0.15) + (px_nodes**2 + py_nodes**2) * 0.002 - 10.0 # Hovering strictly above terrain

# Optimal Path Calculation (A simple Traveling Salesperson heuristic proxy)
# Generate a greedy path through all nodes as the "Tathata Collapse"
unvisited = list(range(NUM_NODES))
current = 0
path_idx = [current]
unvisited.remove(current)

while unvisited:
    next_node = min(unvisited, key=lambda x: (px_nodes[current] - px_nodes[x])**2 + (py_nodes[current] - py_nodes[x])**2)
    path_idx.append(next_node)
    unvisited.remove(next_node)
    current = next_node

# 3. Superposition Lines (The Multiverse Search)
N_LINES = 5000 # 5000 points
px_lines = np.zeros(N_LINES)
py_lines = np.zeros(N_LINES)
pz_lines = np.zeros(N_LINES)

for i in range(N_LINES):
    # Randomly string together points to simulate quantum path evaluation
    n1 = np.random.randint(0, NUM_NODES)
    n2 = np.random.randint(0, NUM_NODES)
    ratio = np.random.rand()
    px_lines[i] = px_nodes[n1] * ratio + px_nodes[n2] * (1 - ratio)
    py_lines[i] = py_nodes[n1] * ratio + py_nodes[n2] * (1 - ratio)
    # The lines arc over the hostile topography
    arc = 15.0 * np.sin(ratio * np.pi)
    pz_lines[i] = pz_nodes[n1] * ratio + pz_nodes[n2] * (1 - ratio) + arc

# HOTFIX: Dynamic array axis lock
base_px = np.concatenate([px_land, px_nodes, px_lines])
base_py = np.concatenate([py_land, py_nodes, py_lines])
base_pz = np.concatenate([pz_land, pz_nodes, pz_lines])

MAX_PARTICLES = len(base_px) # Perfectly aligns to 24,625 points

idx_land_end = len(px_land)
idx_node_end = idx_land_end + len(px_nodes)

mask_land = np.arange(MAX_PARTICLES) < idx_land_end
mask_nodes = (np.arange(MAX_PARTICLES) >= idx_land_end) & (np.arange(MAX_PARTICLES) < idx_node_end)
mask_lines = np.arange(MAX_PARTICLES) >= idx_node_end

# Pre-calculate the optimal path vectors for rapid injection during Phase 4
optimal_px = []
optimal_py = []
optimal_pz = []
for i in range(len(path_idx) - 1):
    n1 = path_idx[i]
    n2 = path_idx[i+1]
    seg_ratios = np.linspace(0, 1, 200) # 200 points per line segment
    for r in seg_ratios:
        optimal_px.append(px_nodes[n1] * r + px_nodes[n2] * (1 - r))
        optimal_py.append(py_nodes[n1] * r + py_nodes[n2] * (1 - r))
        optimal_pz.append(pz_nodes[n1] * r + pz_nodes[n2] * (1 - r))
        
optimal_px = np.array(optimal_px)
optimal_py = np.array(optimal_py)
optimal_pz = np.array(optimal_pz)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, proj_x, proj_y, z_depth, colors, sizes, tax_strain, is_flash, is_tathata = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_TEXT if is_flash else C_BG
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    ax.set_xlim(-160, 160)
    ax.set_ylim(-260, 260)

    if not is_flash:
        # Background Grid structure
        ax.plot([-150, 150], [0, 0], color=C_DIM, lw=1.0, alpha=0.3, zorder=1)
        ax.plot([0, 0], [-250, 250], color=C_DIM, lw=1.0, alpha=0.3, zorder=1)

        # O(N) Depth Sorting
        sort_idx = np.argsort(z_depth)
        s_px = proj_x[sort_idx]
        s_py = proj_y[sort_idx]
        s_c = colors[sort_idx]
        s_s = sizes[sort_idx]

        ax.scatter(s_px, s_py, s=s_s, color=s_c, edgecolors='none', alpha=0.85, zorder=10)

        if is_tathata:
            ax.add_patch(plt.Rectangle((-130, -110), 260, 220, facecolor='none', edgecolor=C_MANTIS, lw=2, zorder=40))
            ax.text(0, -80, "TATHĀTĀ: MULTIVERSE COLLAPSE", color=C_MANTIS, fontsize=11, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 80, "[GROUND STATE / LOWEST ENERGY PATH SECURED]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_MANTIS if t_sec < 4.5 else (C_TEXT if t_sec < 9.0 else C_MAGENTA)
    if is_tathata: ui_col = C_CYAN
    
    ax.text(-140, 240, "LG-236 :: THE CALORIC LEDGER", color=txt_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: OPTIMAL FORAGING AS QUBO / EFFORT = DEBT", color=txt_col, fontsize=8, fontname='monospace', zorder=80)
    
    obj_str = "THE HOSTILE VOID [LINEAR GAIN h_i]"
    if 4.5 <= t_sec < 9.0: obj_str = "SUPERPOSITION DEPLOYED [O(N) PATH SEARCH]"
    elif 9.0 <= t_sec < 14.8: obj_str = "THE CALORIC LEDGER [QUADRATIC PENALTY J_ij]"
    elif is_tathata: obj_str = "GEOMETRIC COLLAPSE [ZERO-DECISION TATHĀTĀ]"

    ax.text(-140, -180, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Thermodynamic Hardware Metric: The Caloric Debt
    ax.text(-140, -205, "THERMODYNAMIC / CALORIC DEBT", color=txt_col, fontsize=10, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    bar_w = 280 * np.clip(tax_strain, 0, 1)
    ax.add_patch(plt.Rectangle((-140, -210), bar_w, 4, facecolor=C_GOLD if t_sec >= 9.0 else ui_col, zorder=81))

    # Phase Text Box
    ax.add_patch(plt.Rectangle((-140, 215), 280, 2, facecolor=ui_col, zorder=80))
    ax.text(140, 205, f"[{state_str}]", color=ui_col if (f%15<10 or is_tathata) else C_BG, fontsize=14, fontname='monospace', weight='bold', ha='right', zorder=80)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) STRUCTURAL INVERSION KINEMATICS
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        is_flash = False
        is_tathata = False
        
        cam_rx = np.pi/6
        cam_ry = t_sec * 0.25
        cam_rz = 0.0
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 4.0
        
        curr_x = np.copy(base_px)
        curr_y = np.copy(base_py)
        curr_z = np.copy(base_pz)

        tax_strain = 0.0

        # Phase 1: Landscape and Nodes are constant
        colors[mask_land] = c_dim
        sizes[mask_land] = 1.0
        
        colors[mask_nodes] = c_mantis
        sizes[mask_nodes] = 15.0 + 5.0 * np.sin(t_sec * 10) # Heavy thermodynamic value

        # -------------------------------------------------------------
        # SQA PHASE LOGIC
        # -------------------------------------------------------------
        if t_sec < 4.5:
            state = "PHASE 1 :: ESTABLISHING HOSTILE TOPOLOGY"
            # Superposition lines are invisible
            colors[mask_lines] = c_bg
            tax_strain = 0.0

        elif t_sec < 9.0:
            state = "PHASE 2 :: THE SUPERPOSITION OF HUNGER"
            prog = (t_sec - 4.5) / 4.5
            
            # The network of possible paths bursts out simultaneously
            colors[mask_lines] = c_text
            sizes[mask_lines] = 2.0 * prog
            
            # Dynamic buzzing as paths are evaluated
            curr_z[mask_lines] += np.random.normal(0, 1.5, N_LINES)
            
            tax_strain = 0.2 + (prog * 0.3)

        elif t_sec < 14.8:
            state = "PHASE 3 :: THE QUADRATIC PENALTY J_ij"
            prog = (t_sec - 9.0) / 5.8
            if t_sec < 9.1: is_flash = True
            
            # Sub-optimal paths snap and decay into MAGENTA and GOLD sparks
            decay_mask = np.random.rand(N_LINES) < prog
            full_mask = np.where(mask_lines)[0]
            
            colors[mask_lines] = c_text
            sizes[mask_lines] = 2.0
            
            colors[full_mask[decay_mask]] = c_magenta
            curr_z[full_mask[decay_mask]] -= np.random.normal(0, 15.0 * prog, np.sum(decay_mask)) # Crashing into the penalty walls
            
            gold_mask = np.random.rand(N_LINES) < (prog * 0.2)
            colors[full_mask[gold_mask]] = c_gold
            sizes[full_mask[gold_mask]] = 5.0
            
            tax_strain = 0.5 + (0.5 * np.abs(np.sin(t_sec * 15))) # Debt maxed out

        else:
            state = "TATHĀTĀ :: THE ABSOLUTE GROUND STATE"
            is_tathata = True
            
            # The multiverse collapses. The single optimal path is instantiated.
            colors[mask_lines] = c_bg # Erase the noise
            
            # Inject the pre-calculated Optimal Path into the line array coordinates
            opt_len = min(N_LINES, len(optimal_px))
            opt_idx = np.where(mask_lines)[0][:opt_len]
            
            curr_x[opt_idx] = optimal_px[:opt_len]
            curr_y[opt_idx] = optimal_py[:opt_len]
            curr_z[opt_idx] = optimal_pz[:opt_len]
            
            colors[opt_idx] = c_cyan
            sizes[opt_idx] = 8.0
            
            tax_strain = 0.0 # Debt resolved. Optimal state acquired.
            
            if t_sec < 14.95:
                is_flash = True

        # Apply Global Tensor Matrix
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1]
        z_depth = rot_pts[:, 2] 

        # O(N) Geometry Culling
        cull_mask = (proj_y > -260) & (proj_y < 260) & (proj_x > -160) & (proj_x < 160)

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], colors[cull_mask], sizes[cull_mask], tax_strain, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 236: THE CALORIC LEDGER [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Dimensional Axis Align / Dynamic Array Boundary")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Syntax Bridged. Ground State Secured.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
