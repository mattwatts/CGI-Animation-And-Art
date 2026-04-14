"""
SOVEREIGN CODE: logic_garden_166_tsp.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Combinatorial Optimization (35 seconds)
SCENE: Logic Garden 166 (The TSP Annealer / Simulated Annealing vs Brute Force)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing as mp
import os
import gc
import math

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 35                   
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_166_tsp"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_CYAN    = '#00FFFF'          # Brute Force Base
C_RED     = '#FF0033'          # Pure Entropy / Brute Force Friction
C_GOLD    = '#FFD700'          # Thermodynamic Heat (Simulated Annealing)
C_MANTIS  = '#00FF00'          # Terminal Green Ring (The Global Minimum)
C_DIM     = '#1A1A24'          # Hardware Mesh

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# TOPOLOGICAL OFFSETS & DISTANCE MATRICES
# ------------------------------------------------------------------
NUM_NODES = 50
np.random.seed(166)

# Generate a perfect spatial circle (The Global Minimum Truth)
# We randomize the starting index to tangle it initially
angles = np.linspace(0, 2 * np.pi, NUM_NODES, endpoint=False)
base_x = np.cos(angles) * 320
base_y = np.sin(angles) * 320

dist_matrix = np.zeros((NUM_NODES, NUM_NODES))
for i in range(NUM_NODES):
    for j in range(NUM_NODES):
        dist_matrix[i, j] = np.sqrt((base_x[i]-base_x[j])**2 + (base_y[i]-base_y[j])**2)

def calc_dist(path):
    return sum(dist_matrix[path[i-1], path[i]] for i in range(NUM_NODES))

# ------------------------------------------------------------------
# PRE-COMPILE SIMULATED ANNEALING VECTOR PATH
# ------------------------------------------------------------------
# We compile the exact thermodynamic descent prior to rendering
# to ensure flawless O(1) multi-core distribution.
initial_path = np.random.permutation(NUM_NODES)
sa_states = [initial_path.copy()]
sa_costs = [calc_dist(initial_path)]
sa_accepted_chaos = [0] # Tracking when it accepts a worse move

current_path = initial_path.copy()
chaos_counter = 0

# Phase 1: High Heat (Accepting friction to escape local minimums)
for step in range(2500):
    temp = 1.0 - (step / 2500.0)
    i, j = sorted(np.random.choice(NUM_NODES, 2, replace=False))
    new_path = current_path.copy()
    new_path[i:j] = new_path[i:j][::-1] # 2-opt swap
    
    old_c = calc_dist(current_path)
    new_c = calc_dist(new_path)
    
    if new_c < old_c or (np.random.rand() < (temp * 0.4)):
        if new_c > old_c:
            chaos_counter += 1
        current_path = new_path
        sa_states.append(current_path.copy())
        sa_costs.append(calc_dist(current_path))
        sa_accepted_chaos.append(chaos_counter)

# Phase 2: Absolute Frost (Greedy 2-opt to guarantee Terminal Green Flow)
while True:
    improved = False
    for i in range(NUM_NODES-1):
        for j in range(i+2, NUM_NODES):
            if j-i == NUM_NODES-1: continue
            new_path = current_path.copy()
            new_path[i:j] = new_path[i:j][::-1]
            if calc_dist(new_path) < calc_dist(current_path):
                current_path = new_path
                chaos_counter += 0
                sa_states.append(current_path.copy())
                sa_costs.append(calc_dist(current_path))
                sa_accepted_chaos.append(chaos_counter)
                improved = True
    if not improved:
        break

TOTAL_SA_STEPS = len(sa_states)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (ISOLATED MEMORY NODE)
# ------------------------------------------------------------------
def render_frame(data_packet):
    f, t_sec, state_str, ui_col, sa_idx = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # Topological Centers
    TOP_Y = 1420
    BOT_Y = 520
    
    # -----------------------------------------------------------
    # 1. TOP PANEL: O(N!) BRUTE FORCE
    # -----------------------------------------------------------
    # Generate random path for visual noise (never converges)
    bf_path = np.random.permutation(NUM_NODES) if f % 2 == 0 else np.random.permutation(NUM_NODES)
    bf_x = base_x[bf_path] + 540
    bf_y = base_y[bf_path] + TOP_Y
    
    # Draw hardware nodes
    ax.scatter(base_x + 540, base_y + TOP_Y, s=20, c=C_TEXT, zorder=5)
    
    # Draw jagged, unpredictable red/cyan noise
    ax.plot(np.append(bf_x, bf_x[0]), np.append(bf_y, bf_y[0]), c=C_RED, lw=1.0, alpha=0.6, zorder=2)
    ax.plot(np.append(bf_x, bf_x[0]), np.append(bf_y, bf_y[0]), c=C_CYAN, lw=3.0, alpha=0.2, zorder=1)

    # -----------------------------------------------------------
    # 2. BOTTOM PANEL: SIMULATED ANNEALING
    # -----------------------------------------------------------
    cur_sa_path = sa_states[sa_idx]
    cur_sa_cost = sa_costs[sa_idx]
    cur_chaos = sa_accepted_chaos[sa_idx]
    
    sa_px = base_x[cur_sa_path] + 540
    sa_py = base_y[cur_sa_path] + BOT_Y
    
    ax.scatter(base_x + 540, base_y + BOT_Y, s=20, c=C_TEXT, zorder=5)
    
    # Mathematical Efficacy Color Logic
    is_terminal = (sa_idx == TOTAL_SA_STEPS - 1)
    if is_terminal:
        sa_line_col = C_MANTIS
        line_w = 4.0
        ax.plot(np.append(sa_px, sa_px[0]), np.append(sa_py, sa_py[0]), c=C_MANTIS, lw=12, alpha=0.3, zorder=2) # Glow
    else:
        # Interpolate between Red (Hot/Tangled) and Gold (Cooling)
        heat_ratio = 1.0 - (sa_idx / TOTAL_SA_STEPS)
        if heat_ratio > 0.5:
            sa_line_col = C_RED
        else:
            sa_line_col = C_GOLD
        line_w = 1.5 + (1.0 - heat_ratio) * 1.5
        
    ax.plot(np.append(sa_px, sa_px[0]), np.append(sa_py, sa_py[0]), c=sa_line_col, lw=line_w, alpha=0.9, zorder=3)

    # -----------------------------------------------------------
    # 3. TELEMETRY WIDGETS & BOUNDING BOXES
    # -----------------------------------------------------------
    # Bounding Boxes
    ax.add_patch(plt.Rectangle((40, TOP_Y - 350), 1000, 700, fill=False, edgecolor=C_DIM, lw=2, zorder=0))
    ax.add_patch(plt.Rectangle((40, BOT_Y - 350), 1000, 700, fill=False, edgecolor=C_DIM, lw=2, zorder=0))
    
    # Top Terminal Data
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2)
    ax.text(0.04, 0.965, "LOGIC GARDEN 166 :: THE O(N!) BOTTLENECK", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    # Brute Force Telemetry (Top)
    ax.text(0.06, 0.90, f"BRUTE FORCE ALGORITHM [O(N!)]", transform=ax.transAxes, color=C_CYAN, fontsize=22, fontname='monospace', weight='bold')
    ax.text(0.06, 0.88, f"POSSIBLE ROUTES: 3.04 x 10^64", transform=ax.transAxes, color=C_RED, fontsize=18, fontname='monospace')
    ax.text(0.06, 0.86, f"ETA TO COMPLETE: AGE OF UNIVERSE", transform=ax.transAxes, color=C_TEXT, fontsize=16, fontname='monospace')
    
    # Simulated Annealing Telemetry (Middle)
    ax.text(0.06, 0.44, f"SIMULATED ANNEALING [HEURISTIC]", transform=ax.transAxes, color=C_GOLD if not is_terminal else C_MANTIS, fontsize=22, fontname='monospace', weight='bold')
    ax.text(0.06, 0.42, f"SYSTEM ENERGY (DIST): {cur_sa_cost:>07.1f} μ", transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace')
    
    # The Zen realization widget
    chaos_col = C_GOLD if (f % 20 < 10 and not is_terminal and cur_chaos > 0) else C_TEXT
    ax.text(0.06, 0.40, f"ACCEPTED CHAOS MOVES: {cur_chaos:>04d}", transform=ax.transAxes, color=chaos_col, fontsize=18, fontname='monospace')

    # Bottom Terminal
    ax.add_patch(plt.Rectangle((0, 0), 0.95, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 0.95], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2)
    
    pulse = ui_col if (f % 60 < 30) or is_terminal else C_TEXT
    ax.text(0.04, 0.08, "STRUCTURAL STATUS:", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=26, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf(); plt.close(fig); plt.close('all'); gc.collect() 
    return f

# ------------------------------------------------------------------
# PHYSICS ENGINE (THERMODYNAMIC TIME MAPPING)
# ------------------------------------------------------------------
def generate_physics_stream():
    # We map the physical seconds strictly into the SA state array
    SOLVE_TIME = 26.0

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        if t_sec < SOLVE_TIME:
            # S-Curve Ease In/Out mapping for a beautiful resolution
            progress = t_sec / SOLVE_TIME
            eased_prog = progress**1.5 # Decelerates as it cools
            sa_idx = int(eased_prog * (TOTAL_SA_STEPS - 1))
            
            if progress < 0.5:
                state = "[01] HIGH HEAT (ACCEPTING ENTROPY)"
                ui_col = C_RED
            else:
                state = "[02] THERMAL DECAY (UNTANGLING MATRICES)"
                ui_col = C_GOLD
        else:
            sa_idx = TOTAL_SA_STEPS - 1
            state = "[03] TATHĀTĀ: HARMONY THROUGH CHAOS"
            ui_col = C_MANTIS

        # Safety clamp
        sa_idx = np.clip(sa_idx, 0, TOTAL_SA_STEPS - 1)

        yield (f, t_sec, state, ui_col, sa_idx)

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 166: THE TSP ANNEALER [CORES: {cpu_cores}]")
    print(f"SA Computed {TOTAL_SA_STEPS} Thermodynamic States.")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
