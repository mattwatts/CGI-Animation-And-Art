"""
SOVEREIGN CODE: logic_garden_159_pathfinder.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Algorithmic Pathfinding (30 seconds)
SCENE: Logic Garden 159 (A* vs Dijkstra / Operations Research)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing as mp
import os
import gc
import heapq

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 30                   
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_159_pathfinder"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_WALL    = '#2A1A24'          # Obstacles / Bounding Box
C_CYAN    = '#00FFFF'          # Dijkstra (Blind Radius Expansion)
C_GOLD    = '#FFD700'          # A* (Heuristic Spear)
C_MANTIS  = '#00FF00'          # Terminal Green (The Optimal Path)
C_RED     = '#FF0033'          # Unresolved Endpoint (HOTFIX)

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# TOPOLOGICAL MAZE GENERATION (COMPILE-TIME LOCK)
# ------------------------------------------------------------------
np.random.seed(159)
GRID_W = 60
GRID_H = 100
CELL_SIZE = 15

grid = np.zeros((GRID_H, GRID_W), dtype=int)
for y in range(GRID_H):
    for x in range(GRID_W):
        if np.random.rand() < 0.35:
            grid[y, x] = 1 # Obstacle

start_pos = (5, GRID_W // 2)
end_pos = (GRID_H - 6, GRID_W // 2)

# Ensure Guaranteed Valid Path (Carving the Matrix)
cx, cy = start_pos[1], start_pos[0]
while cy < end_pos[0] + 1:
    grid[cy, cx] = 0
    if np.random.rand() < 0.6:
        cy += 1
    else:
        cx += np.random.choice([-1, 1])
        cx = np.clip(cx, 1, GRID_W - 2)
    grid[cy, cx] = 0
grid[end_pos[0], end_pos[1]] = 0
grid[start_pos[0], start_pos[1]] = 0

def solve_maze(weight=0.0):
    frontier = []
    heapq.heappush(frontier, (0, start_pos))
    came_from = {start_pos: None}
    cost_so_far = {start_pos: 0}
    explored = []
    
    while frontier:
        current = heapq.heappop(frontier)[1]
        explored.append(current)
        if current == end_pos:
            break
            
        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ny, nx = current[0] + dy, current[1] + dx
            if 0 <= nx < GRID_W and 0 <= ny < GRID_H and grid[ny, nx] == 0:
                new_cost = cost_so_far[current] + 1
                nxt = (ny, nx)
                if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                    cost_so_far[nxt] = new_cost
                    # Heuristic function: Manhattan Distance
                    h = abs(nx - end_pos[1]) + abs(ny - end_pos[0])
                    priority = new_cost + weight * h
                    heapq.heappush(frontier, (priority, nxt))
                    came_from[nxt] = current
                    
    path = []
    if end_pos in came_from:
        curr = end_pos
        while curr != start_pos:
            path.append(curr)
            curr = came_from[curr]
        path.append(start_pos)
    return explored, path[::-1]

# Pre-compile the algorithmic runtimes
d_explored, d_path = solve_maze(weight=0.0) # Dijkstra
a_explored, a_path = solve_maze(weight=1.5) # A* (Aggressive Heuristic)

# Build static wall coordinates
wall_y, wall_x = np.where(grid == 1)
wall_px = 540 - (GRID_W * CELL_SIZE / 2) + (wall_x * CELL_SIZE)
wall_py = 210 + (wall_y * CELL_SIZE)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (ISOLATED MEMORY NODE)
# ------------------------------------------------------------------
def render_frame(data_packet):
    f, t_sec, state_str, ui_col, d_idx, a_idx = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # 1. RENDER STATIC MAZE BOUNDARY (FRICTION ALERTS)
    ax.scatter(wall_px, wall_py, s=CELL_SIZE**2, c=C_WALL, marker='s', zorder=1)

    # Convert coordinates for plotting
    def to_px(node_list, idx):
        sub = node_list[:idx]
        px = [540 - (GRID_W * CELL_SIZE / 2) + (n[1] * CELL_SIZE) for n in sub]
        py = [210 + (n[0] * CELL_SIZE) for n in sub]
        return px, py

    # 2. RENDER THE OPERATIONS RESEARCH ALGORITHMS
    d_px, d_py = to_px(d_explored, d_idx)
    a_px, a_py = to_px(a_explored, a_idx)

    # Dijkstra Flood (Cyan)
    if d_idx > 0:
        ax.scatter(d_px, d_py, s=CELL_SIZE**2 * 1.5, c=C_CYAN, alpha=0.3, marker='s', zorder=2)
        # Scan-head (Brightest edge)
        ax.scatter([d_px[-1]], [d_py[-1]], s=300, c=C_TEXT, marker='s', zorder=4)

    # A* Spear (Gold)
    if a_idx > 0:
        ax.scatter(a_px, a_py, s=CELL_SIZE**2 * 0.8, c=C_GOLD, alpha=0.8, marker='s', zorder=3)
        ax.scatter(a_px, a_py, s=CELL_SIZE**2 * 3, c=C_GOLD, alpha=0.2, zorder=2)
        # Scan-head
        ax.scatter([a_px[-1]], [a_py[-1]], s=300, c=C_TEXT, marker='s', zorder=5)

    # 3. TERMINAL GREEN RESOLUTION
    if t_sec > 25.0:
        # Both complete. Draw the Commutative Truth line.
        p_px, p_py = to_px(a_path, len(a_path))
        ax.plot(p_px, p_py, color=C_MANTIS, lw=8, zorder=6)
        ax.plot(p_px, p_py, color=C_TEXT, lw=2, alpha=0.5, zorder=7)
        ax.scatter(p_px, p_py, s=400, color=C_MANTIS, alpha=0.2, zorder=5)

    # Start & End Nodes
    sx_px, sy_py = to_px([start_pos], 1)
    ex_px, ey_py = to_px([end_pos], 1)
    ax.scatter(sx_px, sy_py, s=600, color=C_TEXT, zorder=10)
    # The C_RED Hotfix is executed here
    ax.scatter(ex_px, ey_py, s=600, color=C_MANTIS if t_sec > 25 else C_RED, zorder=10)

    # 4. TELEMETRY WIDGETS
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.9))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2)
    ax.text(0.04, 0.965, "LOGIC GARDEN 159 :: PATHFINDING MATRICES", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    # Status Panel
    ax.text(0.04, 0.88, f"[O(V+E)] DIJKSTRA NODES : {d_idx:>04d}", transform=ax.transAxes, color=C_CYAN, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.85, f"[A* Heu] A-STAR NODES   : {a_idx:>04d}", transform=ax.transAxes, color=C_GOLD, fontsize=20, fontname='monospace')
    
    # Mathematical Efficacy Check
    if t_sec > 25.0:
        reduction = 100 - (len(a_explored) / len(d_explored) * 100)
        ax.text(0.04, 0.80, f"COMPUTATIONAL EFFICIENCY: +{reduction:.1f}%", transform=ax.transAxes, color=C_MANTIS, fontsize=22, fontname='monospace', weight='bold')

    # Bottom Terminal
    ax.add_patch(plt.Rectangle((0, 0), 0.95, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 0.95], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2)
    
    pulse = ui_col if (f % 60 < 30) or ui_col == C_MANTIS else C_TEXT
    ax.text(0.04, 0.08, "SYSTEM STATUS:", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=28, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf(); plt.close(fig); plt.close('all'); gc.collect() 
    return f

# ------------------------------------------------------------------
# PHYSICS ENGINE (TIME SYNCHRONIZATION MATRIX)
# ------------------------------------------------------------------
def generate_physics_stream():
    # Timing Blocks
    A_STAR_FINISH = 10.0 # A* arrives at 10 seconds
    DIJKSTRA_FINISH = 23.0 # Dijkstra arrives at 23 seconds
    
    total_a = len(a_explored)
    total_d = len(d_explored)

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        # Calculate indices based on exact time mapping
        a_idx = min(total_a, int((t_sec / A_STAR_FINISH) * total_a))
        d_idx = min(total_d, int((t_sec / DIJKSTRA_FINISH) * total_d))
        
        # Phase Management
        if t_sec < A_STAR_FINISH:
            state = "[01] ALGORITHMIC RACE (HEURISTIC VS BRUTE-FORCE)"
            ui_col = C_GOLD
        elif t_sec < DIJKSTRA_FINISH:
            state = "[02] A* TARGET LOCK (DIJKSTRA STILL CALCULATING)"
            ui_col = C_CYAN
        elif t_sec < 25.0:
            state = "[03] DIJKSTRA TARGET LOCK (RESOLVING BINDINGS)"
            ui_col = C_VOID
        else:
            state = "[04] TATHĀTĀ: MINIMUM SET COVER SECURED"
            ui_col = C_MANTIS

        yield (f, t_sec, state, ui_col, d_idx, a_idx)

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 159: PATHFINDING MATRICES [CORES: {cpu_cores}]")
    print(f"Dijkstra evaluated: {len(d_explored)} | A* evaluated: {len(a_explored)}")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
