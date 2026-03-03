"""
SOVEREIGN CODE: logic_garden_v74_bayes.py
CONTEXT: Diagnostic Logic / Intelligence Analysis
LESSON: "Sensitivity != Truth. Watch the Base Rate."
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import random

FPS, DURATION = 30, 15
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_v74_bayes"
os.makedirs(OUT_DIR, exist_ok=True)

# Grid 40x25 = 1000 nodes
GRID_W, GRID_H = 40, 25
TOTAL_NODES = 1000

def run():
    print("LOGIC GARDEN 74: BAYESIAN TRAP")
    fig = plt.figure(figsize=(16, 9), facecolor='#111111')
    ax = fig.add_axes([0, 0, 1, 1], facecolor='#111111')

    # Data
    nodes = [{'x': c % GRID_W, 'y': GRID_H - (c // GRID_W), 'state': 'HEALTHY'} for c in range(TOTAL_NODES)]
    
    # 1 Infected (Base Rate 1/1000)
    infected_idx = 455 # Centerish
    nodes[infected_idx]['state'] = 'INFECTED'

    # False Positives (1% of 999 Healthy = ~10)
    fp_indices = [i for i in range(TOTAL_NODES) if i != infected_idx]
    random.shuffle(fp_indices)
    fp_indices = fp_indices[:10]

    phase = "POPULATION" 

    for f in range(TOTAL_FRAMES):
        ax.clear()
        ax.set_xlim(-1, GRID_W)
        ax.set_ylim(0, GRID_H+1)
        ax.axis('off')

        # Logic Flow
        if f > 60: phase = "SCANNING"
        if f > 180: phase = "RESULT"
        if f > 300: phase = "TRUTH"

        # Draw Nodes
        x_vals, y_vals, c_vals, s_vals = [], [], [], []
        
        for idx, n in enumerate(nodes):
            color = '#333333' # Default Grey
            size = 10
            
            if phase == "POPULATION":
                if n['state'] == 'INFECTED' and f > 30: # Flash the truth briefly
                    color = '#FF0000' if f % 10 < 5 else '#333333'
            
            elif phase == "SCANNING":
                # Sweep effect
                scan_y = GRID_H - (f - 60) * 0.2
                if n['y'] > scan_y:
                    color = '#555555'

            elif phase == "RESULT":
                # Show Test Positives (High Sensitivity)
                if idx == infected_idx:
                    color = '#00FFFF' # Test Positive (Cyan)
                    size = 25
                elif idx in fp_indices:
                    color = '#00FFFF' # False Positive (Cyan)
                    size = 25
                else:
                    color = '#222222'

            elif phase == "TRUTH":
                if idx == infected_idx:
                    color = '#FF0000' # True (Red)
                    size = 50
                elif idx in fp_indices:
                    color = '#00FFFF' # False (Cyan)
                    size = 20
                else:
                    color = '#111111'

            x_vals.append(n['x'])
            y_vals.append(n['y'])
            c_vals.append(color)
            s_vals.append(size)

        ax.scatter(x_vals, y_vals, c=c_vals, s=s_vals)

        # HUD
        if phase == "POPULATION":
            ax.text(GRID_W/2, 2, "POPULATION: 1000 | TARGET: 1 (RARE)", color='white', ha='center', fontfamily='monospace')
        elif phase == "RESULT":
            ax.text(GRID_W/2, 2, "TEST RESULTS (99% ACCURATE)", color='#00FFFF', ha='center', fontfamily='monospace', fontsize=15)
            ax.text(GRID_W/2, 1, "POSITIVES: 11", color='#00FFFF', ha='center', fontfamily='monospace')
        elif phase == "TRUTH":
            ax.text(GRID_W/2, 2, "THE GROUNDED TRUTH", color='#FF0000', ha='center', fontfamily='monospace', fontsize=15)
            ax.text(GRID_W/2, 1, "REAL: 1 | NOISE: 10 | ERROR: 90%", color='white', ha='center', fontfamily='monospace')

        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=80, facecolor='#111111')
    plt.close(fig)

if __name__ == "__main__": run()
