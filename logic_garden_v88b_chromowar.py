"""
SOVEREIGN CODE: logic_garden_v90_chromowar_final.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: Viral Simulation / Color War
FIX: "Void Hunter" mode ensures 100% map fill + 2s Pause.
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
OUT_DIR = "frames_v90_chromowar_final"
os.makedirs(OUT_DIR, exist_ok=True)

# Grid Layout (Low Res for Pixel Style)
GRID_W = 108
GRID_H = 192
grid = np.zeros((GRID_H, GRID_W), dtype=int)

# 0=Black, 1=Red, 2=Blue, 3=Green, 4=Yellow
colors = ['#111111', '#FF0000', '#0088FF', '#00FF00', '#FFFF00']
cmap = matplotlib.colors.ListedColormap(colors)

def run():
    print("LOGIC GARDEN 90: CHROMOWAR (FINAL BLITZ)")
    fig = plt.figure(figsize=(9, 16), facecolor='#111111')
    ax = fig.add_axes([0, 0, 1, 1], facecolor='#111111')
    
    # SEED CORNERS
    grid[0:5, 0:5] = 1 # Top Left: Red
    grid[0:5, GRID_W-5:GRID_W] = 2 # Top Right: Blue
    grid[GRID_H-5:GRID_H, 0:5] = 3 # Bot Left: Green
    grid[GRID_H-5:GRID_H, GRID_W-5:GRID_W] = 4 # Bot Right: Yellow
    
    for f in range(TOTAL_FRAMES):
        ax.clear()
        ax.axis('off')
        
        # TIMING PHASES
        # 1. EARLY WAR (0-10s): Slow expansion
        if f < 300:
            attacks = 2000
            mode = "RANDOM"
        # 2. TOTAL WAR (10-15s): Fast expansion
        elif f < 450:
            attacks = 10000
            mode = "RANDOM"
        # 3. VOID HUNTER (15-18s): Target emptiness
        elif f < 540:
            attacks = 5000 # Checked specifically against zeros
            mode = "HUNT_ZEROS"
        # 4. VICTORY LAP (18-20s): Freeze
        else:
            attacks = 0
            mode = "FREEZE"
            
        # LOGIC
        if mode == "RANDOM":
            # Fast Random Attacks
            # Get list of ALL active pixels? No, too slow.
            # Just pick random coordinates? Most will be empty or internal.
            # Better: Keep list of active? No, Python lists slow.
            # Numpy Mask approach:
            
            # Get indices of ALL colored pixels
            # This is fast enough for 108x192 (~20k pixels)
            active_y, active_x = np.where(grid > 0)
            
            if len(active_y) > 0:
                # Pick random soldiers
                idx = np.random.choice(len(active_y), size=attacks)
                
                # Vectorized attack logic is hard with neighbors
                # Loop the selection
                for i in idx:
                    y, x = active_y[i], active_x[i]
                    c = grid[y, x]
                    
                    # Random neighbor
                    dy = random.choice([-1, 1, 0, 0])
                    dx = random.choice([0, 0, -1, 1])
                    ny, nx = y+dy, x+dx
                    
                    if 0 <= ny < GRID_H and 0 <= nx < GRID_W:
                        target = grid[ny, nx]
                        if target == 0:
                            grid[ny, nx] = c # Claim Void
                        elif target != c:
                            if random.random() < 0.1: # 10% chance to kill enemy
                                grid[ny, nx] = c

        elif mode == "HUNT_ZEROS":
            # Find the remaining zeros and Fill them
            # This guarantees the map closes
            zeros_y, zeros_x = np.where(grid == 0)
            
            if len(zeros_y) > 0:
                # Process chunks of them to animate the closing
                # Don't do all at once, or it looks glitchy. 
                # Do 500 per frame.
                limit = min(len(zeros_y), 500)
                
                # Randomize order so holes close organically
                indices = np.random.choice(len(zeros_y), size=limit, replace=False)
                
                for i in indices:
                    y, x = zeros_y[i], zeros_x[i]
                    
                    # Check neighbors for color
                    # Up, Down, Left, Right
                    neighbors = []
                    if y > 0 and grid[y-1, x] > 0: neighbors.append(grid[y-1, x])
                    if y < GRID_H-1 and grid[y+1, x] > 0: neighbors.append(grid[y+1, x])
                    if x > 0 and grid[y, x-1] > 0: neighbors.append(grid[y, x-1])
                    if x < GRID_W-1 and grid[y, x+1] > 0: neighbors.append(grid[y, x+1])
                    
                    if neighbors:
                        # Adopt a random neighbor's color
                        grid[y, x] = random.choice(neighbors)
                        
            # ALSO continue war at borders so it doesn't look static
            active_y, active_x = np.where(grid > 0)
            idx = np.random.choice(len(active_y), size=2000)
            for i in idx:
                y, x = active_y[i], active_x[i]
                c = grid[y, x]
                dy = random.choice([-1, 1, 0, 0])
                dx = random.choice([0, 0, -1, 1])
                ny, nx = y+dy, x+dx
                if 0 <= ny < GRID_H and 0 <= nx < GRID_W and grid[ny,nx] != 0 and grid[ny,nx] != c:
                     if random.random() < 0.1:
                         grid[ny, nx] = c

        # RENDER
        ax.imshow(grid, cmap=cmap, vmin=0, vmax=4, interpolation='nearest', aspect='auto')
        
        # SCOREBOARD (Optional - user removed text from Sort, kept here for context?)
        # Let's keep it minimal. Just the map.
        # "Who Wins?" Text overlay is good for engagement, but the map is the hero.
        # Let's add the Leader Text only at the end pause.
        
        if mode == "FREEZE":
            counts = [np.sum(grid == i) for i in range(1, 5)]
            leader_idx = np.argmax(counts)
            lead_name = ["RED", "BLUE", "GREEN", "YELLOW"][leader_idx]
            lead_col = colors[leader_idx+1]
            
            # Simple Badge
            ax.text(GRID_W/2, GRID_H/2, f"{lead_name}\nWINS", color=lead_col, ha='center', va='center', 
                   fontsize=40, weight='bold', fontfamily='monospace',
                   bbox=dict(facecolor='black', alpha=0.7, edgecolor=lead_col, linewidth=3))

        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=80, facecolor='#111111')
        
    plt.close(fig)

if __name__ == "__main__": run()
