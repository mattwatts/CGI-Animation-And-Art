"""
SOVEREIGN CODE: logic_garden_64v_skynet_v2.py
FORMAT: YouTube Shorts (9:16)
SYSTEM: C64 VIC-II Emulation
SCENE: Skynet (A* vs Brute Force) - OPEN FIELD
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import heapq
import random

COLORS = {
    0: [0, 0, 0],       # Black
    1: [255, 255, 255], # White
    2: [136, 0, 0],     # Red (Panic)
    3: [170, 255, 238], # Cyan (Logic)
    11: [51, 51, 51]    # Grey (Obstacles)
}

W, H = 55, 98
OUT_DIR = "frames_64v_skynet"
os.makedirs(OUT_DIR, exist_ok=True)
GRID = np.zeros((H, W, 3), dtype=np.uint8)

def draw_rect(canvas, x, y, c):
    if 0 <= x < W and 0 <= y < H: canvas[y, x] = COLORS[c]

def run():
    print("LOGIC GARDEN 64v: SKYNET V2")
    
    # 1. OBSTACLE MAP
    MAP = np.zeros((H, W), dtype=int)
    # Random blocks
    for _ in range(80):
        ox, oy = random.randint(5, W-5), random.randint(10, H-10)
        w, h = random.randint(2, 8), random.randint(2, 6)
        MAP[oy:oy+h, ox:ox+w] = 1 # Obstacle
        
    start = (2, 2)
    end = (W-3, H-3)
    
    # 2. RED FLOOD (Brute Force)
    red_q = [start]
    red_visited = {start}
    red_history = []
    
    # 3. CYAN A* (Heuristic)
    cyan_path = []
    pq = [(0, start)]
    came_from = {}
    g_score = {start: 0}
    
    # Pre-calc A*
    while pq:
        _, curr = heapq.heappop(pq)
        if curr == end: break
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0: continue
                nx, ny = curr[0]+dx, curr[1]+dy
                if 0<=nx<W and 0<=ny<H and MAP[ny, nx] == 0:
                    tentative_g = g_score[curr] + 1.4 if dx!=0 and dy!=0 else g_score[curr]+1
                    if tentative_g < g_score.get((nx, ny), float('inf')):
                        came_from[(nx, ny)] = curr
                        g_score[(nx, ny)] = tentative_g
                        f = tentative_g + ((nx-end[0])**2 + (ny-end[1])**2)**0.5 # Euclidean Heuristic
                        heapq.heappush(pq, (f, (nx, ny)))
    
    # Reconstruct
    curr = end
    if end in came_from:
        while curr in came_from:
            cyan_path.append(curr)
            curr = came_from[curr]
        cyan_path.reverse()

    # RENDER LOOP
    for f in range(200):
        # Base Map
        GRID[:, :] = COLORS[0]
        for y in range(H):
            for x in range(W):
                if MAP[y, x] == 1: draw_rect(GRID, x, y, 11)

        # RED EXPANSION (Slow & Dumb)
        if f < 150:
            for _ in range(5):
                if red_q:
                    curr = red_q.pop(0)
                    red_history.append(curr)
                    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]: # Orthogonal only (Dumb)
                        nx, ny = curr[0]+dx, curr[1]+dy
                        if 0<=nx<W and 0<=ny<H and MAP[ny, nx]==0 and (nx, ny) not in red_visited:
                            red_visited.add((nx, ny))
                            red_q.append((nx, ny))
                            
        # Draw Red Flood
        for (rx, ry) in red_history:
            draw_rect(GRID, rx, ry, 2)
            
        # CYAN STRIKE (Instant & Smart)
        if f > 60:
            # Draw Path
            path_show = min(len(cyan_path), (f-60)*3) # Fast
            for i in range(path_show):
                cx, cy = cyan_path[i]
                draw_rect(GRID, cx, cy, 3) # Core
                # Glow
                if i == path_show-1: draw_rect(GRID, cx, cy, 1) # Head
        
        # Victory Pulse
        if f > 120 and cyan_path:
            ex, ey = end
            if f % 10 < 5: draw_rect(GRID, ex, ey, 3)

        fig = plt.figure(figsize=(9, 16), dpi=80) 
        plt.figimage(GRID, resize=True, interpolation='nearest') 
        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor='black')
        plt.close(fig)

if __name__ == "__main__": run()
