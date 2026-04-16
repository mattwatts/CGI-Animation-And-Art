"""
SOVEREIGN CODE: logic_garden_178_pathfinding.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Algorithmic Pathfinding Race (17.8 seconds)
SCENE: Logic Garden 178 (Dijkstra vs A* / The Efficiency of Intent)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import multiprocessing as mp
import heapq
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.8                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_178_pathfinding"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_DIM     = '#1A1A24'          # Maze Geometry
C_CYAN    = '#00FFFF'          # Dijkstra (Unbiased Diligence)
C_MAGENTA = '#FF00FF'          # A* (Guided Intent)
C_GOLD    = '#FFD700'          # The Destination Node
C_MANTIS  = '#00FF00'          # Terminal Path Resolution
C_RED     = '#FF0033'          # High Friction Obstacles

# ------------------------------------------------------------------
# MATRIX GENERATION (THE TOPOLOGICAL MAZE)
# ------------------------------------------------------------------
COLS, ROWS = 60, 45 # For each half-screen maze
np.random.seed(178)

def generate_maze():
    grid = np.zeros((ROWS, COLS), dtype=int)
    # Generate structural Bounding Boxes (Obstacles)
    for _ in range(35):
        w, h = np.random.randint(2, 8), np.random.randint(2, 12)
        x, y = np.random.randint(5, COLS-10), np.random.randint(2, ROWS-h-2)
        grid[y:y+h, x:x+w] = 1
    
    # Create the "Heuristic Trap" (A Wall that forces A* into a local minimum)
    grid[10:35, 30:35] = 1 
    grid[10:15, 20:30] = 1
    return grid

maze_grid = generate_maze()
START = (5, 22)
GOAL = (55, 22)

# ------------------------------------------------------------------
# ALGORITHMIC PHYSICS (OFFLINE PRE-COMPUTATION)
# ------------------------------------------------------------------
def get_neighbors(node):
    x, y = node
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    valid = []
    for dx, dy in directions:
        nx, ny = x+dx, y+dy
        if 0 <= nx < COLS and 0 <= ny < ROWS:
            if maze_grid[ny, nx] == 0:
                valid.append((nx, ny))
    return valid

def compute_search(use_heuristic=False):
    frontier = []
    heapq.heappush(frontier, (0, START))
    came_from = dict()
    cost_so_far = dict()
    came_from[START] = None
    cost_so_far[START] = 0
    
    exploration_history = []
    
    while frontier:
        _, current = heapq.heappop(frontier)
        exploration_history.append(current)
        
        if current == GOAL:
            break
            
        for next_node in get_neighbors(current):
            new_cost = cost_so_far[current] + 1
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost
                if use_heuristic:
                    # Manhattan distance heuristic (Intent)
                    priority += abs(GOAL[0] - next_node[0]) + abs(GOAL[1] - next_node[1])
                heapq.heappush(frontier, (priority, next_node))
                came_from[next_node] = current
                
    # Backtrack optimal path
    path = []
    curr = GOAL
    if curr in came_from:
        while curr != START:
            path.append(curr)
            curr = came_from[curr]
        path.append(START)
        path.reverse()
        
    return exploration_history, path

dijkstra_history, dijkstra_path = compute_search(use_heuristic=False)
astar_history, astar_path = compute_search(use_heuristic=True)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, d_idx, a_idx, phase_flash = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    # Global UI lines
    ax.axhline(960, color=C_DIM, lw=4, zorder=1)

    # ---------------------------------------------------
    # RENDER ENGINE: DIJKSTRA (TOP MATRIX)
    # ---------------------------------------------------
    d_offset_y = 1000
    m_scale = 16.0
    
    # Draw Maze
    obs_y, obs_x = np.where(maze_grid == 1)
    ax.scatter(obs_x * m_scale + 50, obs_y * m_scale + d_offset_y, s=150, c=C_RED, alpha=0.3, marker='s', zorder=2)

    # Draw Visited
    if d_idx > 0:
        vis_x = [p[0] * m_scale + 50 for p in dijkstra_history[:d_idx]]
        vis_y = [p[1] * m_scale + d_offset_y for p in dijkstra_history[:d_idx]]
        ax.scatter(vis_x, vis_y, s=80, c=C_CYAN, alpha=0.4, marker='s', zorder=3)
        # Frontier Head
        ax.scatter([vis_x[-1]], [vis_y[-1]], s=250, c=C_TEXT, zorder=5)

    # Final Path Dijkstra
    if d_idx >= len(dijkstra_history):
        px = [p[0] * m_scale + 50 for p in dijkstra_path]
        py = [p[1] * m_scale + d_offset_y for p in dijkstra_path]
        ax.plot(px, py, color=C_MANTIS if phase_flash else C_TEXT, lw=6, zorder=6)

    # Goal Node Top
    ax.scatter([GOAL[0]*m_scale+50], [GOAL[1]*m_scale+d_offset_y], s=500, c=C_GOLD, marker='*', zorder=4)

    # ---------------------------------------------------
    # RENDER ENGINE: A* SEARCH (BOTTOM MATRIX)
    # ---------------------------------------------------
    a_offset_y = 150
    # Draw Maze
    ax.scatter(obs_x * m_scale + 50, obs_y * m_scale + a_offset_y, s=150, c=C_RED, alpha=0.3, marker='s', zorder=2)

    # Draw Visited
    if a_idx > 0:
        vis_x = [p[0] * m_scale + 50 for p in astar_history[:a_idx]]
        vis_y = [p[1] * m_scale + a_offset_y for p in astar_history[:a_idx]]
        ax.scatter(vis_x, vis_y, s=80, c=C_MAGENTA, alpha=0.4, marker='s', zorder=3)
        # Frontier Head
        ax.scatter([vis_x[-1]], [vis_y[-1]], s=250, c=C_TEXT, zorder=5)

    # Final Path A*
    if a_idx >= len(astar_history):
        px = [p[0] * m_scale + 50 for p in astar_path]
        py = [p[1] * m_scale + a_offset_y for p in astar_path]
        pulse = C_MANTIS if (f % 10 < 5) else C_TEXT
        ax.plot(px, py, color=pulse if phase_flash else C_TEXT, lw=6, zorder=6)

    # Goal Node Bottom
    ax.scatter([GOAL[0]*m_scale+50], [GOAL[1]*m_scale+a_offset_y], s=500, c=C_GOLD, marker='*', zorder=4)

    # ---------------------------------------------------
    # TELEMETRY WIDGETS
    # ---------------------------------------------------
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.9))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=C_CYAN, lw=2)
    ax.text(0.04, 0.965, "DIJKSTRA: UNBIASED DILIGENCE", transform=ax.transAxes, color=C_CYAN, fontsize=24, fontname='monospace', weight='bold', va='center')
    ax.text(0.04, 0.91, f"NODES EXPANDED: {min(d_idx, len(dijkstra_history)):04d}", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')

    ax.add_patch(plt.Rectangle((0, 0), 1, 0.10, transform=ax.transAxes, color=C_VOID, alpha=0.9))
    ax.plot([0, 1], [0.10, 0.10], transform=ax.transAxes, color=C_MAGENTA, lw=2)
    ax.text(0.04, 0.065, "A* SEARCH: THE EFFICIENCY OF INTENT", transform=ax.transAxes, color=C_MAGENTA, fontsize=24, fontname='monospace', weight='bold', va='center')
    ax.text(0.04, 0.02, f"NODES EXPANDED: {min(a_idx, len(astar_history)):04d}", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# PHYSICS STREAM (TIMING ALIGNMENT)
# ------------------------------------------------------------------
def generate_stream():
    d_total = len(dijkstra_history)
    a_total = len(astar_history)
    
    # We want A* to finish at t=9 seconds. Dijkstra to finish at t=15 seconds.
    # 17.8 total duration leaves 2.8s for the "Terminal Green Flow" lock-in hook.
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        # Calculate indices based on target completion times
        a_idx = int((t_sec / 9.0) * a_total) if t_sec < 9.0 else a_total
        d_idx = int((t_sec / 15.0) * d_total) if t_sec < 15.0 else d_total
        
        # Phase transition hook logic
        phase_flash = (t_sec > 15.0)
        
        yield (f, t_sec, d_idx, a_idx, phase_flash)

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 178: DIJKSTRA VS A* [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
