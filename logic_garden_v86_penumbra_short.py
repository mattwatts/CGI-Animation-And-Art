"""
SOVEREIGN CODE: logic_garden_v86_penumbra_short.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: Stroke Evolution / Time is Brain
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

FPS = 30
DURATION = 15
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_v86_short"
os.makedirs(OUT_DIR, exist_ok=True)

GRID_S = 31

def run():
    print("LOGIC GARDEN 86: THE PENUMBRA")
    fig = plt.figure(figsize=(9, 16), facecolor='#000000')
    ax = fig.add_axes([0, 0, 1, 1], facecolor='#000000')
    
    # 0=Healthy(White), 1=Penumbra(Grey), 2=Dead(Black)
    grid = np.zeros((GRID_S, GRID_S))
    
    # Init: Small core, large Penumbra
    center = GRID_S // 2
    for x in range(GRID_S):
        for y in range(GRID_S):
            dist = np.sqrt((x-center)**2 + (y-center)**2)
            if dist < 3: grid[x,y] = 2 # Core
            elif dist < 12: grid[x,y] = 1 # Penumbra
            
    cmap = matplotlib.colors.ListedColormap(['#FFFFFF', '#888888', '#000000'])
    
    saved = False
    
    for f in range(TOTAL_FRAMES):
        ax.clear()
        ax.axis('off')
        
        # EVOLUTION LOGIC
        # Every bit of time, Penumbra turns Black
        if not saved:
            if f % 5 == 0: # Fast decay
                # Find grey cells
                greys = np.argwhere(grid == 1)
                if len(greys) > 0:
                    # Randomly kill some adjacent to black?
                    # Simple stochastic death
                    idx = np.random.choice(len(greys))
                    target = greys[idx]
                    grid[target[0], target[1]] = 2 # Dies
        
        # INTERVENTION (TPA) at 10s (f=300)
        if f == 300:
            saved = True
            # Convert remaining Grey to White (Saved)
            grid[grid == 1] = 0
            
        ax.imshow(grid, cmap=cmap, vmin=0, vmax=2, interpolation='nearest')
        
        # HUD
        dead_count = np.sum(grid == 2)
        ax.text(GRID_S/2, 2, "TIME IS BRAIN", color='black', ha='center', fontsize=25, weight='bold', fontfamily='monospace')
        
        if not saved:
             ax.text(GRID_S/2, GRID_S-2, f"NEURON DEATH: {dead_count}", color='red', ha='center', fontsize=20, fontfamily='monospace', weight='bold')
        else:
             ax.text(GRID_S/2, GRID_S/2, "REPERFUSION\nSUCCESS", color='#00FF00', ha='center', fontsize=30, weight='bold', fontfamily='monospace', bbox=dict(facecolor='black', alpha=0.8))

        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=100, facecolor='#000000')
        
    plt.close(fig)

if __name__ == "__main__": run()
