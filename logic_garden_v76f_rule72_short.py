"""
SOVEREIGN CODE: logic_garden_v76_rule72_short.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: Mental Math / Exponential Growth
SCENARIO: Race to Double (1% vs 7% vs 10%)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

FPS = 30
DURATION = 15
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_v76_rule72"
os.makedirs(OUT_DIR, exist_ok=True)

def run():
    print("LOGIC GARDEN 76: RULE OF 72")
    fig = plt.figure(figsize=(9, 16), facecolor='#050505')
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], facecolor='#050505')
    
    # LOGIC
    # 72 / Rate = Years
    rates = [1, 7, 10]
    years_to_double = [72.0/r for r in rates] # [72, 10.2, 7.2]
    
    # We simulate 30 Years
    MAX_YEARS = 30
    
    for f in range(TOTAL_FRAMES):
        ax.clear()
        
        progress = f / float(TOTAL_FRAMES - 60)
        if progress > 1.0: progress = 1.0
        
        curr_year = progress * MAX_YEARS
        
        # RENDER BARS
        # We draw bars side by side
        # Height = (1 + r)^t
        
        ax.set_ylim(0, 10) # 10x Max
        ax.set_xlim(0, 4)
        ax.axis('off')
        
        positions = [1, 2, 3]
        colors = ['#888888', '#00CCFF', '#FFD700']
        labels = ['SAVINGS\n(1%)', 'INDEX\n(7%)', 'GROWTH\n(10%)']
        
        for i, r in enumerate(rates):
            # Calc multiple
            mult = (1 + r/100.0) ** curr_year
            
            # The Bar
            rect = plt.Rectangle((positions[i]-0.4, 0), 0.8, mult, color=colors[i])
            ax.add_patch(rect)
            
            # The Text
            ax.text(positions[i], mult + 0.2, f"{mult:.1f}x", color='white', ha='center', fontsize=20, weight='bold', fontfamily='monospace')
            ax.text(positions[i], -0.5, labels[i], color=colors[i], ha='center', fontsize=15, fontfamily='monospace', weight='bold')

            # DOUBLING MARKERS
            # Draw a line every 2x, 4x, 8x
            for mark in [2, 4, 8]:
                if mult >= mark:
                     # Just reached?
                     pass
        
        # GRID LINES
        for y in [2, 4, 8]:
            ax.axhline(y, color='#333333', linestyle='--')
            ax.text(0.1, y, f"{y}X", color='#555555')

        # HUD
        ax.text(2, 9, "THE RULE OF 72", color='white', ha='center', fontsize=30, weight='bold', fontfamily='monospace')
        ax.text(2, 8.5, f"YEAR: {curr_year:.1f}", color='white', ha='center', fontsize=25, fontfamily='monospace')
        
        # WINNER
        if curr_year > 25:
             ax.text(3, 7, "DOMINANCE", color='#FFD700', ha='center', fontsize=20, weight='bold', rotation=90)

        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=100, facecolor='#050505')
        
    plt.close(fig)

if __name__ == "__main__": run()
