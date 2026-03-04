"""
SOVEREIGN CODE: logic_garden_v82_pump_short.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: Frank-Starling Law (Heart Failure)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

FPS = 30
DURATION = 15
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_v82_short"
os.makedirs(OUT_DIR, exist_ok=True)

def run():
    print("LOGIC GARDEN 82: THE PUMP")
    fig = plt.figure(figsize=(9, 16), facecolor='#000000')
    ax = fig.add_axes([0, 0, 1, 1], facecolor='#000000')
    
    # State
    preload = 0.0 # How much we stretch
    failure = False
    
    for f in range(TOTAL_FRAMES):
        ax.clear()
        ax.set_xlim(-9, 9)
        ax.set_ylim(-16, 16)
        ax.axis('off')
        
        # TIMING LOGIC
        cycle = f % 60 # 2 beats per second-ish
        phase = cycle / 60.0
        
        # Increase Preload over time
        if f < 200:
            mode = "NORMAL LOAD"
            stretch_factor = 1.0
            col = '#FF0000'
        elif f < 350:
            mode = "HIGH PRELOAD (OPTIMAL)"
            stretch_factor = 1.6
            col = '#00FF00'
        else:
            mode = "OVER-STRETCH (FAILURE)"
            stretch_factor = 2.2 # Too big
            col = '#800080' # Purple (Hypoxic)
            failure = True
            
        # PUMP MECHANIC
        # Contraction/Expansion curve
        if not failure:
            # Healthy Snap
            r_base = 3.0 + (stretch_factor * 1.5)
            if phase < 0.5: # Filling
                r = 3.0 + (phase * 2 * (stretch_factor * 1.5))
            else: # Ejection (Snap)
                r = 3.0 + ((1.0-phase) * 2 * (stretch_factor * 1.5))
        else:
            # Failed Snap (Baggy Heart)
            r_base = 3.0 + (stretch_factor * 1.5)
            # It barely moves
            r = r_base + np.sin(f * 0.1) * 0.2
            
        # RENDER
        # The Chamber
        circle = plt.Circle((0, -2), r, color=col, alpha=0.9, zorder=10)
        ax.add_patch(circle)
        
        # The Stroke Volume (Arrow out)
        if not failure and phase > 0.5:
            # Ejection Visual
            arrow_len = stretch_factor * 4
            ax.arrow(0, r-2, 0, arrow_len, color='white', width=0.5, head_width=1.5)
            ax.text(0, r + arrow_len, "OUTPUT", color='white', ha='center', fontsize=20)
            
        if failure:
             ax.text(0, 0, "NO OUTPUT", color='white', ha='center', fontsize=30, weight='bold')

        # HUD
        ax.text(0, 14, "FRANK-STARLING LAW", color='white', ha='center', fontsize=25, weight='bold', fontfamily='monospace')
        ax.text(0, -14, mode, color=col, ha='center', fontsize=20, weight='bold', fontfamily='monospace')
        
        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=100, facecolor='#000000')
        
    plt.close(fig)

if __name__ == "__main__": run()
