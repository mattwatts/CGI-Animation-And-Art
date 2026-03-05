"""
SOVEREIGN CODE: logic_garden_v95_optimizer_short.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: Operations Research / Penny Post
VISUAL: Network Graph Explosion (Friction Drop)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import networkx as nx

FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_v95_optimizer"
os.makedirs(OUT_DIR, exist_ok=True)

# Canvas
W, H = 9, 16 

def run():
    print("LOGIC GARDEN 95: THE OPTIMIZER")
    fig = plt.figure(figsize=(9, 16), facecolor='#000510') # Deep Blue Void
    ax = fig.add_axes([0, 0, 1, 1], facecolor='#000510')
    
    # PARAMETERS
    num_nodes = 50
    # Fixed Positions (Ring? Random?)
    # Random layout for "Messy Reality"
    np.random.seed(42)
    pos = {i: (np.random.uniform(0.1, 8.9), np.random.uniform(1, 15)) for i in range(num_nodes)}
    
    # We simulate connection probability based on Friction
    # P(connect) = 1 / (Distance * Friction)
    
    for f in range(TOTAL_FRAMES):
        ax.clear()
        ax.set_xlim(0, 9)
        ax.set_ylim(0, 16)
        ax.axis('off')
        
        # 3 PHASES
        # 1. HIGH FRICTION (0-8s): Local connections only.
        # 2. THE REFORM (8-14s): Friction drops rapidly.
        # 3. METCALFE (14-20s): Total Web.
        
        fraction = f / TOTAL_FRAMES
        
        friction = 10.0 # High cost
        title = "HIGH FRICTION"
        mode_color = "#444444" # Grey lines
        
        if fraction > 0.4: # The Reform (Penny Post) starts
            # Decay Friction
            progress = (fraction - 0.4) * 2.0 
            friction = 10.0 * (1 - progress)
            if friction < 0.1: friction = 0.1 # Floor
            
            title = "THE REFORM"
            mode_color = "#0088FF" # Blue lines
            
        if fraction > 0.7:
             title = "INFINITE SCALE"
             mode_color = "#FFD700" # GOLD
        
        # DRAW NODES
        for i in range(num_nodes):
            ax.scatter(pos[i][0], pos[i][1], c='white', s=50, zorder=10)
            
        # DRAW EDGES
        # We calculate edges per frame based on current friction
        # This is expensive ($O(N^2)$) but okay for N=50
        
        edge_count = 0
        
        for i in range(num_nodes):
            for j in range(i+1, num_nodes):
                # Distance
                dist = np.sqrt((pos[i][0]-pos[j][0])**2 + (pos[i][1]-pos[j][1])**2)
                
                # Connection logic
                # If Cost < Value
                # Cost = Dist * Friction
                cost = dist * friction
                
                # Assume constant Value = 2.0
                if cost < 2.0:
                    # Draw Line
                    # Alpha depends on strength?
                    alpha = 0.5
                    width = 1.0
                    
                    if mode_color == "#FFD700": # Gold phase
                         alpha = 0.2
                         width = 0.5
                         
                    ax.plot([pos[i][0], pos[j][0]], [pos[i][1], pos[j][1]], c=mode_color, alpha=alpha, linewidth=width, zorder=1)
                    edge_count += 1
                    
        # HUD
        ax.text(4.5, 15, title, color='white', ha='center', fontsize=40, weight='bold', fontfamily='monospace')
        ax.text(4.5, 1, f"CONNECTIONS: {edge_count}", color='#AAAAAA', ha='center', fontsize=20, fontfamily='monospace')

        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=80, facecolor='#000510')
        
    plt.close(fig)

if __name__ == "__main__": run()
