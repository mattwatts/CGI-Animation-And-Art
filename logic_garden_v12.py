"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v12.py
MODE:   Nursery (Bauhaus Palette)
TARGET: Pathfinding (Dijkstra / BFS)
STYLE:  "The Maze Solver" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import collections
import os

# --- 1. THE NURSERY PALETTE ---
BG_COLOR = "#FFFFFF"        # Void (Unexplored)
WALL_COLOR = "#000000"      # Structure
VISITED_COLOR = "#0080FF"   # Azure Blue (Water)
FRONTIER_COLOR = "#FFD700"  # Cyber Yellow (The Spark)
PATH_COLOR = "#FF4500"      # Safety Red (The Solution)

# --- 2. CONFIGURATION ---
COLS, ROWS = 32, 18
FPS = 30
WALL_DENSITY = 0.3
START_POS = (1, 1)
END_POS = (COLS-2, ROWS-2)

class MazeSolver:
    def __init__(self):
        # 1. Generate World
        # 0 = Empty, 1 = Wall
        np.random.seed(101) # Fixed seed for solvable nice maze
        self.grid = np.zeros((COLS, ROWS), dtype=int)
        
        # Random walls
        noise = np.random.rand(COLS, ROWS)
        self.grid[noise < WALL_DENSITY] = 1
        
        # Clear Start and End
        self.grid[START_POS] = 0
        self.grid[END_POS] = 0
        
        # Ensure path exists? 
        # For simplicity in "Toy" mode, we just run. 
        # If blocked, we show it filling up.
        
        # 2. Algorithm State (BFS for unweighted grid = Dijkstra)
        self.queue = collections.deque([START_POS])
        self.came_from = {START_POS: None}
        self.visited = set([START_POS])
        
        self.finished = False
        self.path = []
        self.frontier_set = set([START_POS]) 

    def update(self):
        if self.finished:
            return

        # Expand ONE step (or a few for speed?)
        # 1 step per frame gives "Liquid" look.
        
        if not self.queue:
            self.finished = True # No path found
            return
            
        # Process current frontier
        current = self.queue.popleft()
        self.frontier_set.remove(current)
        
        if current == END_POS:
            self.finished = True
            self.reconstruct_path()
            return
        
        # Neighbors (Up, Down, Left, Right)
        cx, cy = current
        neighbors = [
            (cx+1, cy), (cx-1, cy), 
            (cx, cy+1), (cx, cy-1)
        ]
        
        for n in neighbors:
            nx, ny = n
            # Bounds check
            if 0 <= nx < COLS and 0 <= ny < ROWS:
                # Wall check
                if self.grid[nx, ny] == 0:
                    # Visited check
                    if n not in self.visited:
                        self.queue.append(n)
                        self.visited.add(n)
                        self.came_from[n] = current
                        self.frontier_set.add(n)

    def reconstruct_path(self):
        # Backtrack from End
        current = END_POS
        while current is not None:
            self.path.append(current)
            current = self.came_from.get(current)
        self.path.reverse()

    def render(self, frame_idx, ax):
        # We draw grid cells as rectangles
        
        # 1. Draw Walls (Static)
        for x in range(COLS):
            for y in range(ROWS):
                if self.grid[x, y] == 1:
                    # Remember y is up in plot, matrix is usually indexed down
                    # Let's map y directly.
                    rect = Rectangle((x, y), 1, 1, facecolor=WALL_COLOR, edgecolor=None)
                    ax.add_patch(rect)
        
        # 2. Draw Visited (Water)
        for v in self.visited:
            if v != START_POS and v != END_POS:
                 rect = Rectangle((v[0], v[1]), 1, 1, facecolor=VISITED_COLOR, alpha=0.4, edgecolor=None)
                 ax.add_patch(rect)
                 
        # 3. Draw Frontier (Active Edge)
        for f in self.frontier_set:
             rect = Rectangle((f[0], f[1]), 1, 1, facecolor=FRONTIER_COLOR, edgecolor=None)
             ax.add_patch(rect)
        
        # 4. Draw Path (If finished)
        if self.finished and self.path:
            # Draw path as a connected line or blocks? Blocks fit the grid.
            for p in self.path:
                 rect = Rectangle((p[0], p[1]), 1, 1, facecolor=PATH_COLOR, edgecolor=None)
                 ax.add_patch(rect)

        # 5. Start / End Markers
        # Start
        ax.add_patch(Rectangle(START_POS, 1, 1, facecolor=VISITED_COLOR, edgecolor=PATH_COLOR, linewidth=2))
        # End
        ax.add_patch(Rectangle(END_POS, 1, 1, facecolor=BG_COLOR, edgecolor=PATH_COLOR, linewidth=2))

        # Scale
        ax.set_xlim(0, COLS)
        ax.set_ylim(0, ROWS)
        ax.set_aspect('equal')

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Flooding the Maze...")
    solver = MazeSolver()
    
    # Run loop until finished + cushion
    MAX_FRAMES = 600
    
    for i in range(MAX_FRAMES):
        # 1. Canvas
        fig = plt.figure(figsize=(16, 9), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        # 2. Render
        solver.render(i, ax)
        
        # 3. Update Logic
        # Speed up: do 2 steps per frame to ensure we finish
        solver.update()
        solver.update()
        
        # 4. Save
        out_dir = "logic_garden_maze_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"maze_{i:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()
        
        if solver.finished and len(solver.path) > 0 and i > 100:
            # Add a bit of "Victory Lap" freeze frames then break
            # Logic: We just keep rendering the finished state for 60 frames
            pass 
        
        if i % 50 == 0:
            print(f"Frame {i}/{MAX_FRAMES}")
            
        # Hard Stop optimization
        if solver.finished and i > 500:
            break
