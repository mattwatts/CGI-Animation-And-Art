"""
SOVEREIGN CODE: logic_garden_174_distributed_lethality.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Swarm Kinematics (35 seconds)
SCENE: Logic Garden 174 (Distributed Lethality / The Swarm Transition)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import LineCollection
import multiprocessing as mp
import os
import gc
import math

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 35                   
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_174_distributed_lethality"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_DIM     = '#1A1A24'          # Hardware Mesh
C_GOLD    = '#FFD700'          # The Legacy Monolith (Concentrated Target)
C_RED     = '#FF0033'          # Enemy Targeting Algorithms / Friction
C_CYAN    = '#00FFFF'          # Fracture Energy / Swarm Logic
C_MANTIS  = '#00FF00'          # Terminal Green Flow (Distributed Mesh)

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY & FIBONACCI MONOLITH
# ------------------------------------------------------------------
N_NODES = 400
np.random.seed(174)

# Generate a hyper-dense Fibonacci sphere for the original Monolith
indices = np.arange(0, N_NODES, dtype=float)
monolith_radius = 120.0
r = np.sqrt(indices / N_NODES) * monolith_radius
theta = np.pi * (1 + 5**0.5) * indices

offset_x = r * np.cos(theta)
offset_y = r * np.sin(theta)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (ISOLATED MEMORY NODE)
# ------------------------------------------------------------------
def render_frame(data_packet):
    # HOTFIX ENFORCED: Strict Tuple Unpacking Array
    f, t_sec, state_str, ui_col, px, py, colors, mesh_lines, red_beams, eff_ratio = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # 1. HARDWARE GRID (THE OCEAN/MATRIX)
    for x in range(0, 1080, 108):
        ax.plot([x, x], [0, 1920], color=C_DIM, lw=1, alpha=0.3, zorder=0)
    for y in range(0, 1920, 108):
        ax.plot([0, 1080], [y, y], color=C_DIM, lw=1, alpha=0.3, zorder=0)

    # 2. ENEMY TARGETING VECTORS (RED FRICTION)
    # These strike from off-screen
    if len(red_beams) > 0:
        lines = [[(rb[0], rb[1]), (rb[2], rb[3])] for rb in red_beams]
        alphas = [np.clip(rb[4], 0.0, 1.0) for rb in red_beams]
        
        # We draw individually to apply correct alpha decay
        for i, line in enumerate(lines):
            c_red_rgba = hex_to_rgba(C_RED, alphas[i])
            ax.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], color=c_red_rgba, lw=2, zorder=3)
            # Kinetic explosion at terminus
            ax.scatter([line[1][0]], [line[1][1]], s=250 * alphas[i], color=c_red_rgba, edgecolors='none', zorder=4)

    # 3. DISTRIBUTED MESH CONNECTIVITY (THE SWARM GRAPH)
    if len(mesh_lines) > 0:
        lc = LineCollection(mesh_lines, color=hex_to_rgba(C_MANTIS, 0.3), lw=1.0, zorder=5)
        ax.add_collection(lc)

    # 4. THE AUTONOMOUS NODES
    ax.scatter(px, py, s=40, c=colors, zorder=7)
    # Sovereign Core highlight
    ax.scatter(px, py, s=8, c=C_TEXT, alpha=0.8, zorder=8)

    # 5. MONOLITH BOUNDING BOX SHADOW (PHASE 1)
    if t_sec < 10.0:
        # Draw a massive rigid box around the dense cluster
        cx, cy = np.mean(px), np.mean(py)
        ax.add_patch(Rectangle((cx - 140, cy - 140), 280, 280, fill=False, edgecolor=hex_to_rgba(C_GOLD, 0.8), lw=3, zorder=6))
        ax.scatter([cx], [cy], s=120000, facecolors='none', edgecolors=C_RED, lw=1, alpha=0.2, zorder=2) # Target lock

    # 6. TELEMETRY WIDGETS
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.9))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2)
    ax.text(0.04, 0.965, "LOGIC GARDEN 174 :: DISTRIBUTED LETHALITY", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    # Network Status Panel
    ax.text(0.04, 0.88, f"ALGORITHMIC ARCHITECTURE:", transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace')
    
    if t_sec < 10.0:
        ax.text(0.04, 0.85, f"[ MONOLITHIC SUPER-NODE (CSG) ]", transform=ax.transAxes, color=C_GOLD, fontsize=22, fontname='monospace', weight='bold')
    else:
        ax.text(0.04, 0.85, f"[ DISTRIBUTED SWARM MESH ]", transform=ax.transAxes, color=C_MANTIS, fontsize=22, fontname='monospace', weight='bold')

    ax.text(0.04, 0.80, f"TARGETING FRICTION ABSORPTION:", transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace')
    ax.text(0.04, 0.77, f"{eff_ratio}", transform=ax.transAxes, color=ui_col, fontsize=22, fontname='monospace', weight='bold')

    # Bottom Terminal
    ax.add_patch(plt.Rectangle((0, 0), 0.95, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 0.95], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2)
    
    pulse = ui_col if (f % 60 < 30) or ui_col == C_MANTIS else C_TEXT
    ax.text(0.04, 0.08, "SYSTEM SURVIVABILITY:", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=24, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf(); plt.close(fig); plt.close('all'); gc.collect() 
    return f

# ------------------------------------------------------------------
# PHYSICS ENGINE (THE SHATTER MATRIX)
# ------------------------------------------------------------------
def generate_physics_stream():
    # Initial Monolith State
    cx, cy = 540.0, 960.0
    px = cx + offset_x
    py = cy + offset_y
    
    vx = np.zeros(N_NODES)
    vy = np.zeros(N_NODES)
    
    red_beams = [] # [start_x, start_y, end_x, end_y, alpha]
    
    dt = 1.0 / FPS

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        mesh_lines = []
        colors = np.zeros((N_NODES, 4))
        
        # Fade old beams
        red_beams = [[sx, sy, ex, ey, a - 0.04] for sx, sy, ex, ey, a in red_beams if a > 0.04]

        # ---------------------------------------------------
        # PHASE 1: THE MONOLITH (LEGACY CONCENTRATION)
        # ---------------------------------------------------
        if t_sec < 10.0:
            state = "[01] MASSIVE TOPOLOGICAL TARGET (HIGH FRICTION)"
            ui_col = C_GOLD
            eff_ratio = "0.0% (MATHEMATICAL VULNERABILITY)"
            
            # The carrier drifts slowly
            px += np.cos(t_sec * 0.5) * 10.0 * dt
            py += np.sin(t_sec * 0.3) * 10.0 * dt
            
            colors[:, 0:3] = hex_to_rgba(C_GOLD)[0:3]
            colors[:, 3] = 1.0
            
            # Incoming hypersonics lock perfectly onto the center of mass
            if f % 12 == 0:
                edge_x = np.random.choice([0, 1080])
                edge_y = np.random.uniform(0, 1920)
                # Strike hits the monolithic bounding box exactly
                red_beams.append([edge_x, edge_y, np.mean(px) + np.random.uniform(-40, 40), np.mean(py) + np.random.uniform(-40, 40), 1.0])

        # ---------------------------------------------------
        # PHASE 2: THE SHATTER PROTOCOL
        # ---------------------------------------------------
        elif t_sec < 12.0:
            state = "[02] ORCHESTRATED COLLAPSE OF THE BOUNDING BOX"
            ui_col = C_CYAN
            eff_ratio = "FRACTURING ARCHITECTURE..."
            
            # The explosive un-binding
            if f == int(10.0 * FPS):
                # Apply radial velocity outwards from center
                mag = np.sqrt(offset_x**2 + offset_y**2) + 0.001
                vx = (offset_x / mag) * np.random.uniform(300, 800, N_NODES)
                vy = (offset_y / mag) * np.random.uniform(300, 800, N_NODES)
                
                # Immediate massive red strikes try to intercept but hit the void where it used to be
                for _ in range(8):
                    red_beams.append([np.random.choice([0, 1080]), np.random.uniform(0, 1920), 540, 960, 1.0])

            # Apply kinematics with drag
            vx *= 0.96
            vy *= 0.96
            px += vx * dt
            py += vy * dt
            
            # Color transitions from Gold to Cyan Energy
            c_mix = (t_sec - 10.0) / 2.0
            colors[:, 0:3] = hex_to_rgba(C_CYAN)[0:3]
            colors[:, 3] = 1.0

        # ---------------------------------------------------
        # PHASE 3: DISTRIBUTED SWARM MESH (TERMINAL FLOW)
        # ---------------------------------------------------
        else:
            state = "[03] TATHĀTĀ: BECOME THE KINETIC FLUID"
            ui_col = C_MANTIS
            eff_ratio = "99.9% (TARGETING ALGORITHM DEFEATED)"
            
            # Form Swarm Fluidity (Boids / Flow Field)
            # Gentle drift based on Perlin-like noise
            vx += np.sin(py * 0.005 + t_sec) * 15.0 * dt
            vy += np.cos(px * 0.005 + t_sec * 0.8) * 15.0 * dt
            
            # Rigid Bounding Toroid to keep them on screen
            vx = np.where(px > 1030, vx - 5.0, vx)
            vx = np.where(px < 50, vx + 5.0, vx)
            vy = np.where(py > 1870, vy - 5.0, vy)
            vy = np.where(py < 250, vy + 5.0, vy)
            
            # Speed limit
            speed = np.sqrt(vx**2 + vy**2) + 0.001
            vx = np.where(speed > 100, (vx/speed)*100, vx)
            vy = np.where(speed > 100, (vy/speed)*100, vy)
            
            px += vx * dt
            py += vy * dt
            
            # Calculate Local Mesh Connectivity O(N^2) broadcast (Pythonic fast for N=400)
            dx = px[:, np.newaxis] - px[np.newaxis, :]
            dy = py[:, np.newaxis] - py[np.newaxis, :]
            dist_sq = dx**2 + dy**2
            
            # Connect nodes closer than 90 units
            close_pairs = np.argwhere((dist_sq < 90**2) & (dist_sq > 0.1))
            
            # Build line collection list (deduplicated by ensuring i < j)
            for i, j in close_pairs:
                if i < j:
                    mesh_lines.append([(px[i], py[i]), (px[j], py[j])])

            colors[:, 0:3] = hex_to_rgba(C_MANTIS)[0:3]
            colors[:, 3] = np.clip(0.5 + (len(mesh_lines)/4000.0), 0.5, 1.0) # Glow based on network density
            
            # The Enemy Targeting Algorithm fails
            if f % 8 == 0:
                edge_x = np.random.choice([0, 1080])
                edge_y = np.random.choice([250, 1870])
                # It attempts to shoot at random zones where the monolith *would* have been
                # The strike hits empty matrix space. The Swarm survives seamlessly.
                miss_x = np.random.uniform(100, 980)
                miss_y = np.random.uniform(300, 1800)
                red_beams.append([edge_x, edge_y, miss_x, miss_y, 0.8])

        yield (f, t_sec, state, ui_col, px.copy(), py.copy(), colors, mesh_lines, red_beams, eff_ratio)

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 174: DISTRIBUTED LETHALITY [CORES: {cpu_cores}]")
    print(f"Tracking {N_NODES} Sovereign Swarm Nodes.")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
