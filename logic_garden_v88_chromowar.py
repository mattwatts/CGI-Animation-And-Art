"""
SOVEREIGN CODE: logic_garden_v88_chromowar.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: Viral Simulation / Color War
HOOK: "Bet on your color."
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import random

FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_v90_chromowar"
os.makedirs(OUT_DIR, exist_ok=True)

# THE ARENA
GRID_W = 108
GRID_H = 192 # 9:16 Aspect
grid = np.zeros((GRID_H, GRID_W), dtype=int)

# 0=Empty(Black), 1=Red, 2=Blue, 3=Green, 4=Yellow
# Color Map
colors = ['#111111', '#FF0000', '#0088FF', '#00FF00', '#FFFF00']
cmap = matplotlib.colors.ListedColormap(colors)

def run():
    print("LOGIC GARDEN 90: CHROMOWAR")
    fig = plt.figure(figsize=(9, 16), facecolor='#111111')
    ax = fig.add_axes([0, 0, 1, 1], facecolor='#111111')
    
    # SEED CORNERS
    grid[0:10, 0:10] = 1 # Top Left: Red
    grid[0:10, GRID_W-10:GRID_W] = 2 # Top Right: Blue
    grid[GRID_H-10:GRID_H, 0:10] = 3 # Bot Left: Green
    grid[GRID_H-10:GRID_H, GRID_W-10:GRID_W] = 4 # Bot Right: Yellow
    
    # The active front (optimization)
    # Instead of scanning full grid, only scan non-zeros that have 0 neighbors?
    # For simplicity/visual chaos, we iterate full grid stochastically.
    
    for f in range(TOTAL_FRAMES):
        ax.clear()
        ax.axis('off')
        
        # BATTLE LOGIC (Stochastic Expansion)
        # 1. Expand
        # We process 'N' attacks per frame to speed it up
        attacks = 2000 
        
        # Vectorized approach is hard for random growth, simpler loop:
        # Pick random active cells? 
        # Let's find edges
        
        # Get all non-zero/non-empty indices
        sq_indices = np.argwhere(grid > 0)
        
        if len(sq_indices) > 0:
            # Pick random soldiers to attack
            # Choosing random indices from the list is faster than scanning
            soldier_idxs = np.random.choice(len(sq_indices), size=attacks)
            
            for idx in soldier_idxs:
                y, x = sq_indices[idx]
                color = grid[y, x]
                
                # Attack random neighbor (UP, DOWN, LEFT, RIGHT)
                dy = random.choice([-1, 1, 0, 0])
                dx = random.choice([0, 0, -1, 1])
                
                ny, nx = y+dy, x+dx
                
                # Boundary check
                if 0 <= ny < GRID_H and 0 <= nx < GRID_W:
                    target = grid[ny, nx]
                    if target == 0:
                        # Claim empty land (100% chance)
                        grid[ny, nx] = color
                    elif target != color:
                        # Attack enemy! (5% chance to overtake)
                        # This creates the "Battle Line" wobble
                        if random.random() < 0.05:
                            grid[ny, nx] = color

        # RENDER
        ax.imshow(grid, cmap=cmap, vmin=0, vmax=4, interpolation='nearest', aspect='auto')
        
        # SCOREBOARD (The Hook)
        counts = [np.sum(grid == i) for i in range(1, 5)] # R, B, G, Y
        leader = np.argmax(counts)
        lead_col = colors[leader+1]
        lead_name = ["RED", "BLUE", "GREEN", "YELLOW"][leader]
        
        # Dynamic Text
        if f % 10 == 0: # Flash effect?
             pass 
             
        ax.text(GRID_W/2, 20, "WHO WINS?", color='white', ha='center', fontsize=30, weight='bold', fontfamily='monospace',
               bbox=dict(facecolor='black', alpha=0.5))
               
        ax.text(GRID_W/2, GRID_H-20, f"LEADER: {lead_name}", color=lead_col, ha='center', fontsize=40, weight='bold', fontfamily='monospace',
               bbox=dict(facecolor='black', alpha=0.7))

        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=80, facecolor='#111111')
        
    plt.close(fig)

if __name__ == "__main__": run()
