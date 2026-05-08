"""
SOVEREIGN CODE: logic_garden_201_broken_glass_tensor.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Phase Space Fracture Tensor (17.5 seconds)
SCENE: Logic Garden 201 (The Fracture Tensor / Reality is Broken Glass)
HOTFIX: O(1) Matrix Projection, Depth Sorting (Z-Buffer), Combinatorial Shatter Vectors
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
from matplotlib.collections import PolyCollection
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_201_broken_glass"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'        # The Thermodynamic Vacuum
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'        # Dark Architecture
C_CYAN      = '#00FFFF'        # Continuous Manifold Illusion
C_MAGENTA   = '#FF0055'        # Constraint Friction (The Break)
C_GOLD      = '#FFD700'        # Discrete OR Pathfinding Trace
C_RED       = '#FF3300'        # Dimensional Compiler Crash
C_MANTIS    = '#00FF00'        # Terminal Geometry (Tathata / The True Graph)

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_void = np.array(hex_to_rgba(C_VOID)[:3])
c_cyan = np.array(hex_to_rgba(C_CYAN)[:3])
c_mage = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_gold = np.array(hex_to_rgba(C_GOLD)[:3])
c_mant = np.array(hex_to_rgba(C_MANTIS)[:3])
c_txt  = np.array(hex_to_rgba(C_TEXT)[:3])

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE KINEMATIC ARCHITECTURE
# ------------------------------------------------------------------
GRID_SIZE = 35 # 35x35 grid = 1225 squares = 2450 shards (Broken Glass)
CENTER_X = 0.0  
CENTER_Y = 0.0

# Pre-compile the geometry matrices
def compile_shard_matrix():
    # 1. Generate base grid nodes with intentional structural anomalies (jitter)
    base_x = np.linspace(-100, 100, GRID_SIZE)
    base_y = np.linspace(-100, 100, GRID_SIZE)
    X, Y = np.meshgrid(base_x, base_y)
    
    # Introduce the roughness to the topology
    np.random.seed(42)
    noise_x = np.random.normal(0, 1.8, (GRID_SIZE, GRID_SIZE))
    noise_y = np.random.normal(0, 1.8, (GRID_SIZE, GRID_SIZE))
    
    # Clamp edges for clean Bounding Box
    noise_x[:, 0] = noise_x[:, -1] = 0
    noise_y[0, :] = noise_y[-1, :] = 0
    X += noise_x
    Y += noise_y
    Z = np.sin(X/20.0) * np.cos(Y/20.0) * 15.0 # The "Smooth Manifold" curve
    
    # 2. Extract discrete triangles (The Shards)
    shards = []
    centers = []
    vectors = []
    
    for i in range(GRID_SIZE - 1):
        for j in range(GRID_SIZE - 1):
            # Triangle 1
            v1 = [X[i,j], Y[i,j], Z[i,j]]
            v2 = [X[i+1,j], Y[i+1,j], Z[i+1,j]]
            v3 = [X[i,j+1], Y[i,j+1], Z[i,j+1]]
            c1 = np.mean([v1, v2, v3], axis=0)
            shards.append([v1, v2, v3])
            centers.append(c1)
            # Explosion vector (Radial + Z)
            r = np.sqrt(c1[0]**2 + c1[1]**2)
            vectors.append([c1[0]/(r+1)*10, c1[1]/(r+1)*10, np.random.uniform(5, 40)])
            
            # Triangle 2
            v4 = [X[i+1,j+1], Y[i+1,j+1], Z[i+1,j+1]]
            c2 = np.mean([v2, v4, v3], axis=0)
            shards.append([v2, v4, v3])
            centers.append(c2)
            r2 = np.sqrt(c2[0]**2 + c2[1]**2)
            vectors.append([c2[0]/(r2+1)*10, c2[1]/(r2+1)*10, np.random.uniform(5, 40)])
            
    return np.array(shards), np.array(centers), np.array(vectors)

GLOBAL_SHARDS, GLOBAL_CENTERS, GLOBAL_VECTORS = compile_shard_matrix()
NUM_SHARDS = len(GLOBAL_SHARDS)

# Pre-compute an operations research path (jumping across the centers)
# Greedy nearest-neighbor jump sequence from corner to corner
OR_PATH = [0]
curr = 0
visited = set([0])
for _ in range(150):
    dists = np.linalg.norm(GLOBAL_CENTERS - GLOBAL_CENTERS[curr], axis=1)
    dists[list(visited)] = 999999
    # Add a directional bias to move diagonally explicitly
    dists -= (GLOBAL_CENTERS[:,0] + GLOBAL_CENTERS[:,1]) * 0.1 
    nxt = np.argmin(dists)
    OR_PATH.append(nxt)
    visited.add(nxt)

# ------------------------------------------------------------------
# O(1) ISOMETRIC PROJECTION MATRICES
# ------------------------------------------------------------------
def rotate_3d(tensor, rot_x, rot_z):
    # tensor shape: (N, 3, 3) -> N fragments, 3 vertices, 3 dimensions
    # 1. Rotate Z (Yaw)
    cos_z, sin_z = np.cos(rot_z), np.sin(rot_z)
    Rz = np.array([[cos_z, -sin_z, 0], [sin_z, cos_z, 0], [0, 0, 1]])
    
    # 2. Rotate X (Pitch)
    cos_x, sin_x = np.cos(rot_x), np.sin(rot_x)
    Rx = np.array([[1, 0, 0], [0, cos_x, -sin_x], [0, sin_x, cos_x]])
    
    # Apply Rz then Rx
    flat = tensor.reshape(-1, 3)
    rotated = flat @ Rz.T @ Rx.T
    return rotated.reshape(tensor.shape)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, active_tensor, z_depths, c_faces, c_edges, lw_tensor, cam_w, frac_val, jump_idx, is_flash, is_tathata, bg_strobe = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_TEXT if is_flash else C_VOID
    if bg_strobe and not is_tathata: bg_hex = '#0F0005' 
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    cam_h = cam_w * (1920.0 / 1080.0)
    ax.set_xlim(CENTER_X - cam_w/2, CENTER_X + cam_w/2)
    ax.set_ylim(CENTER_Y - cam_h/2, CENTER_Y + cam_h/2)

    # 1. THE FRACTURE MATRIX (Depth-sorted Z-buffer PolyCollection)
    if not is_flash:
        # Sort shards by Z-depth to ensure proper 3D occlusion
        sort_idx = np.argsort(z_depths)[::-1] # Farthest first
        
        # We drop the actual Z coordinate for 2D plotting, using only X and Y
        polys_2d = active_tensor[sort_idx][:, :, :2]
        c_f_sorted = c_faces[sort_idx]
        c_e_sorted = c_edges[sort_idx]
        lw_sorted = lw_tensor[sort_idx]

        collection = PolyCollection(polys_2d, facecolors=c_f_sorted, edgecolors=c_e_sorted, linewidths=lw_sorted, zorder=10)
        ax.add_collection(collection)
        
        # 2. THE CHRONOLOGICAL PATH TENSOR (The Golden OR routing)
        if jump_idx > 0 and not is_tathata:
            path_pts = []
            # Calculate the transformed centers for the active path
            path_shards = active_tensor[OR_PATH[:jump_idx]]
            path_centers_2d = np.mean(path_shards, axis=1)[:, :2]
            
            # Draw the jagged trajectory lines connecting the discrete matrix
            ax.plot(path_centers_2d[:,0], path_centers_2d[:,1], color=C_GOLD, lw=4, zorder=25)
            # Strike nodes
            ax.scatter(path_centers_2d[:,0], path_centers_2d[:,1], s=40, color=C_TEXT, edgecolor=C_GOLD, lw=1.5, zorder=26)

    # 3. TATHĀTĀ / GEOMETRIC EXTRACTION
    if is_tathata and not is_flash:
        # Bounding lock visuals
        ax.text(CENTER_X, CENTER_Y - cam_h*0.4, "NON-CONVEX GRAPH ACKNOWLEDGED", color=C_MANTIS, fontsize=18, fontname='monospace', ha='center', weight='bold', zorder=30)

    if is_flash:
        ax.add_patch(Rectangle((CENTER_X - cam_w, CENTER_Y - cam_h), cam_w*2, cam_h*2, facecolor=C_TEXT, zorder=60))

    # 4. TELEMETRY WIDGETS (NEURAL ENTRAINMENT UI)
    ui_col = C_CYAN if not is_tathata else C_MANTIS
    if frac_val > 0.01: ui_col = C_MAGENTA 
    if jump_idx > 0 and not is_tathata: ui_col = C_GOLD
    txt_col = C_TEXT if not is_flash else C_VOID
    ui_bg   = C_VOID if not is_flash else C_TEXT
    
    # Top Bar
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=ui_bg, alpha=0.9, zorder=80))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    ax.text(0.04, 0.965, "LG-201 :: PHASE SPACE FRACTURE TENSOR", transform=ax.transAxes, color=txt_col, fontsize=20, fontname='monospace', weight='bold', va='center', zorder=81)

    # Bottom Target Matrix
    ax.add_patch(plt.Rectangle((0, 0), 1.0, 0.16, transform=ax.transAxes, color=ui_bg, alpha=0.95, zorder=80))
    ax.plot([0, 1.0], [0.16, 0.16], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    
    # Discrete Separation Metric
    ax.text(0.04, 0.11, "GRAPH FRACTURE DISTANCE :", color=txt_col, fontsize=14, fontname='monospace', zorder=81)
    bar_f = C_CYAN if frac_val < 0.1 else C_MAGENTA
    if is_tathata: bar_f = C_MANTIS
    ax.add_patch(plt.Rectangle((0.45, 0.105), 0.50, 0.02, transform=ax.transAxes, color=C_DIM, zorder=80))
    ax.add_patch(plt.Rectangle((0.45, 0.105), 0.50 * np.clip(frac_val, 0, 1), 0.02, transform=ax.transAxes, color=bar_f, zorder=81))
    
    # O.R. Pathfinding Progress
    ax.text(0.04, 0.08, "O.R. DISCRETE ALGORITHM :", color=txt_col, fontsize=14, fontname='monospace', zorder=81)
    jump_ratio = np.clip(jump_idx / float(len(OR_PATH)), 0.0, 1.0)
    bar_o = C_DIM if jump_idx == 0 else C_GOLD
    if is_tathata: bar_o = C_MANTIS
    if is_flash: bar_o = C_VOID
    ax.add_patch(plt.Rectangle((0.45, 0.075), 0.50, 0.02, transform=ax.transAxes, color=C_DIM, zorder=80))
    ax.add_patch(plt.Rectangle((0.45, 0.075), 0.50 * jump_ratio, 0.02, transform=ax.transAxes, color=bar_o, zorder=81))

    pulse = ui_col if (f % 10 < 5) and not is_flash else txt_col
    if is_flash: pulse = C_VOID
    ax.text(0.04, 0.03, f"[{state_str}]", transform=ax.transAxes, color=pulse, fontsize=20, fontname='monospace', weight='bold', zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)

# ------------------------------------------------------------------
# O(1) BALLISTIC KINEMATICS STREAM
# ------------------------------------------------------------------
def generate_stream():
    cam_w = 180.0
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        is_flash = False
        is_tathata = False
        bg_strobe = False
        
        frac_val = 0.0
        jump_idx = 0
        rot_x = np.pi/4 # 45 degrees pitch
        rot_z = t_sec * 0.2 # Slow rotation of the phase space
        
        target_cam_w = 180.0
        
        # ---- PHASE 1: THE EUCLIDEAN ILLUSION (0 - 4s) ----
        if t_sec < 4.0:
            state = "NOMINAL :: CONTINUOUS MANIFOLD ASSUMED"
            frac_val = 0.0

        # ---- PHASE 2: THE COMBINATORIAL SHATTER (4 - 10s) ----
        elif t_sec < 10.0:
            state = "WARNING :: ILP CONSTRAINTS INTRODUCED. GRAPH SHATTERED."
            prog = (t_sec - 4.0) / 6.0
            # Expansive kinetic shatter
            frac_val = smoothstep(prog) * 1.5 
            if t_sec < 4.5 and f % 6 < 3: bg_strobe = True
            rot_z = (4.0 * 0.2) + (prog * 2.0) # Spin violently as it breaks

        # ---- PHASE 3: OPERATIONS RESEARCH ROUTING (10 - 14.8s) ----
        elif t_sec < 14.8:
            state = "TENSOR JUMP :: CALCULATING DISCRETE NON-CONVEX PATHWAYS"
            prog = (t_sec - 10.0) / 4.8
            frac_val = 1.5 + (prog * 0.5) # Continues drifting slowly
            
            # The algorithm pathfinds sequentially across the shattered nodes
            jump_idx = int(prog * len(OR_PATH))
            target_cam_w = 200.0
            
            # Lock rotation to stabilize the algorithmic view
            rot_z = (4.0 * 0.2) + (1.0 * 2.0) + (prog * 0.2)
            rot_x = (np.pi/4) - (prog * 0.2) # Tilt down slightly to see the gaps

        # ---- PHASE 4: TATHĀTĀ / THE ZEN REALIZATION (14.8 - 17.5s) ----
        else:
            is_tathata = True
            frac_val = 2.0
            jump_idx = len(OR_PATH)
            target_cam_w = 160.0
            rot_z = (4.0 * 0.2) + (1.0 * 2.0) + (4.8 * 0.2)
            rot_x = (np.pi/4) - (1.0 * 0.2)
            
            if t_sec < 14.95:
                is_flash = True
                
            state = "TATHĀTĀ: THE SMOOTH GRAPH WAS A LIE. REALITY IS BROKEN GLASS."

        cam_w += (target_cam_w - cam_w) * 0.1
        
        # -------------------------------------------------------------
        # TENSOR PARTICLE CALCULATION (Kinematic Translation)
        # -------------------------------------------------------------
        # Apply the explosion to the original coordinates
        shift_matrix = GLOBAL_VECTORS * frac_val
        # shift_matrix is (N, 3). We need to broadcast it to (N, 3, 3) to move all vertices of each shard equally
        translated_shards = GLOBAL_SHARDS + shift_matrix[:, np.newaxis, :]
        
        # Project visually
        projected = rotate_3d(translated_shards, rot_x, rot_z)
        
        # Extract Z for depth sorting
        z_depths = np.mean(projected[:,:,2], axis=1)
        
        # -------------------------------------------------------------
        # CHROMATIC THEOREM
        # -------------------------------------------------------------
        c_faces = np.zeros((NUM_SHARDS, 4))
        c_edges = np.zeros((NUM_SHARDS, 4))
        lw_tensor = np.ones(NUM_SHARDS) * 0.5
        
        if is_tathata:
            c_faces[:] = hex_to_rgba(C_VOID, 0.8)
            c_edges[:] = hex_to_rgba(C_MANTIS, 0.9)
            lw_tensor[:] = 1.0
        else:
            # Distance from center determines base color
            dists = np.linalg.norm(GLOBAL_CENTERS[:, :2], axis=1) / 140.0
            dists = np.clip(dists, 0, 1)
            
            # Phase 1: Smooth cyan continuous gradient
            base_faces = dists[:, None] * np.array(hex_to_rgba('#0044FF')) + (1-dists[:, None]) * np.array(hex_to_rgba(C_CYAN))
            
            if frac_val > 0.01:
                # Add Magenta friction edges as it breaks
                f_inf = np.clip(frac_val, 0, 1)
                edge_col = f_inf * np.array(hex_to_rgba(C_MAGENTA)) + (1-f_inf) * np.array(hex_to_rgba(C_CYAN))
                c_edges[:] = edge_col
                # Dim the faces to emphasize the breakage
                base_faces = base_faces * (1.0 - (f_inf * 0.7))
                lw_tensor[:] = 0.5 + (f_inf * 1.5)
            else:
                # Perfect continuity (no edges visible)
                c_edges[:] = base_faces
                
            c_faces[:] = base_faces
            
            # Highlighting the OR Path
            if jump_idx > 0:
                active_path = OR_PATH[:jump_idx]
                c_faces[active_path] = hex_to_rgba(C_GOLD, 0.7)
                c_edges[active_path] = hex_to_rgba(C_TEXT, 1.0)
                lw_tensor[active_path] = 2.0

        yield (f, t_sec, state, projected, z_depths, c_faces, c_edges, lw_tensor, cam_w, frac_val, jump_idx, is_flash, is_tathata, bg_strobe)

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 201: THE FRACTURE TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: O(1) Matrix Projection & Isometric Z-Buffer Reordering")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Nodes: {NUM_SHARDS} Discrete Shards")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
