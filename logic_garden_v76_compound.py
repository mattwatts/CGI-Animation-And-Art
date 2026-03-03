"""
SOVEREIGN CODE: logic_garden_v76_compound.py
CONTEXT: Assets / Knowledge / Strategy
LESSON: "Survive the Valley of Disappointment."
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

FPS, DURATION = 30, 15
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_v76_compound"
os.makedirs(OUT_DIR, exist_ok=True)

def run():
    print("LOGIC GARDEN 76: COMPOUND INTEREST")
    fig = plt.figure(figsize=(16, 9), facecolor='#050505') # Void Black
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], facecolor='#050505')

    # Data
    # Time x goes 0 to 100
    x = np.linspace(0, 100, TOTAL_FRAMES)
    
    # Linear (Salary/Labour)
    y_linear = x * 20 
    
    # Exponential (Compound/Assets)
    # Start small, end huge
    y_exp = 5 * (1.08 ** x) 

    for f in range(TOTAL_FRAMES):
        ax.clear()
        ax.set_facecolor('#050505')
        
        # Dynamic Scaling to keep 'current' point in view, 
        # but showing the history
        current_x = x[:f+1]
        current_lin = y_linear[:f+1]
        current_exp = y_exp[:f+1]
        
        # Plot
        ax.plot(current_x, current_lin, color='#00FFFF', linewidth=3, label="LINEAR EFFORT")
        ax.plot(current_x, current_exp, color='#FFD700', linewidth=3, label="COMPOUND GROWTH")
        
        # Limits - Dynamic zoom out
        max_y = max(2000, current_exp[-1] * 1.2, current_lin[-1] * 1.2)
        ax.set_ylim(0, max_y)
        ax.set_xlim(0, 100)
        
        # Grid
        ax.grid(color='#222222', linestyle='--')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        
        # Labels
        ax.legend(loc='upper left', facecolor='black', labelcolor='white')
        
        # The Lesson Text
        if f < TOTAL_FRAMES * 0.6:
            ax.text(50, max_y/2, "THE VALLEY OF DISAPPOINTMENT", color='#555555', ha='center', fontsize=15, fontfamily='monospace')
        else:
            ax.text(50, max_y/2, "THE KNEE OF THE CURVE", color='#FFD700', ha='center', fontsize=20, weight='bold', fontfamily='monospace')
            
        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=80, facecolor='#050505')
        
    plt.close(fig)

if __name__ == "__main__": run()
