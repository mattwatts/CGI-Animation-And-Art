"""
SOVEREIGN CODE: logic_garden_v79_viral_short_tuned.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: Exponential Growth
STATUS: TUNED (15s Cycle)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import copy

FPS = 30
DURATION = 15 # 15 Seconds exactly
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_v79_short_tuned"
os.makedirs(OUT_DIR, exist_ok=True)

GRID_W, GRID_H = 25, 50 # Taller Grid for Vertical

def get_neighbors(x, y):
    n = []
    # Order: UP, SIDE, DOWN
    # Bias logic handled in loop
    if x > 0: n.append(((x-1, y), 'UP')) 
    if x < GRID_H-1: n.append(((x+1, y), 'DOWN'))
    if y > 0: n.append(((x, y-1), 'SIDE'))
    if y < GRID_W-1: n.append(((x, y+1), 'SIDE'))
    return n

def run():
    print("LOGIC GARDEN 79: VIRAL (TUNED CYCLE)")
    
    # 0=Blue (Susceptible), 1=Red (Infected), 2=Grey (Recovered/Dead)
    grid = np.zeros((GRID_H, GRID_W))
    
    # Patient Zero (Bottom Center)
    grid[GRID_H-1, GRID_W//2] = 1
    
    fig = plt.figure(figsize=(9, 16), facecolor='#000000')
    ax = fig.add_axes([0, 0, 1, 1])
    
    cmap = matplotlib.colors.ListedColormap(['#000055', '#FF0000', '#333333'])
    
    # TUNING PARAMETERS
    # We need to cross 50 rows in ~250 frames (0.2 rows/frame)
    # R0 needs to be just above 1.0 initially, then crash.
    
    BASE_SPREAD = 0.12 
    BASE_BURNOUT = 0.05
    
    for f in range(TOTAL_FRAMES):
        ax.clear()
        ax.axis('off')
        
        # Stop simulation if empty to save 'Silence'
        total_inf = np.sum(grid == 1)
        
        if total_inf > 0 or f < 50:
            new_grid = copy.deepcopy(grid)
            infected_indices = np.argwhere(grid == 1)
            
            for ix, iy in infected_indices:
                neighbors = get_neighbors(ix, iy)
                for (nx, ny), direction in neighbors:
                    if grid[nx, ny] == 0:
                        # Chimney Effect: Heat rises
                        chance = BASE_SPREAD
                        if direction == 'UP': chance *= 1.5 
                        
                        if np.random.random() < chance: 
                            new_grid[nx, ny] = 1
                
                # Recovery
                if np.random.random() < BASE_BURNOUT: 
                    new_grid[ix, iy] = 2
                    
            grid = new_grid
        
        # Render
        ax.imshow(grid, cmap=cmap, vmin=0, vmax=2, interpolation='nearest', aspect='auto')
        
        # Overlay Stats
        percent_infected = (np.sum(grid > 0) / (GRID_W * GRID_H)) * 100
        
        # Dynamic Text
        if total_inf == 0 and f > 50:
             # The Silence
             ax.text(GRID_W/2, GRID_H/2, "EXTINCTION", color='#888888', ha='center', fontsize=40, weight='bold', fontfamily='monospace')
        else:
             # The Fire
             ax.text(GRID_W/2, 2, "VIRAL LOAD", color='white', ha='center', fontsize=25, weight='bold', fontfamily='monospace')
             ax.text(GRID_W/2, GRID_H-2, f"CASES: {total_inf}", color='#FF0000', ha='center', fontsize=20, fontfamily='monospace', weight='bold')

        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=100, facecolor='#000000')
        
    plt.close(fig)

if __name__ == "__main__": run()
