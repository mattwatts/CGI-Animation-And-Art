"""
SOVEREIGN CODE: logic_garden_v73_doppler_short.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: Wave Mechanics
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

FPS = 30
DURATION = 15
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_v73_short"
os.makedirs(OUT_DIR, exist_ok=True)

def run():
    print("LOGIC GARDEN 73: DOPPLER (SHORT FORMAT)")
    fig = plt.figure(figsize=(9, 16), facecolor='#050505')
    ax = fig.add_axes([0, 0, 1, 1], facecolor='#050505')

    # Source Params (Vertical Motion)
    source_y = -8
    velocity = 0.25 # Vertical speed
    
    waves = [] # {y_origin, time_emitted}
    
    for f in range(TOTAL_FRAMES):
        ax.clear()
        ax.set_xlim(-9, 9)
        ax.set_ylim(-16, 16)
        ax.axis('off')
        
        # Move Source Up
        if source_y < 12:
            source_y += velocity
        
        # Emit
        if f % 10 == 0:
            waves.append({'y': source_y, 't': f})
            
        # Draw Waves
        for w in waves:
            age = f - w['t']
            radius = age * 0.15 
            
            circle = plt.Circle((0, w['y']), radius, color='#444444', fill=False, linewidth=2)
            ax.add_patch(circle)
            
        # Draw Source
        source = plt.Circle((0, source_y), 0.5, color='#FFFFFF', zorder=10)
        ax.add_patch(source)
        
        # Observers
        # Top (Blue)
        ax.text(0, 14, "OBSERVER B\n(HIGH FREQ)", color='#00FFFF', ha='center', fontsize=20, fontfamily='monospace', weight='bold')
        # Bottom (Red)
        ax.text(0, -14, "OBSERVER A\n(LOW FREQ)", color='#FF0000', ha='center', fontsize=20, fontfamily='monospace', weight='bold')
        
        # HUD
        ax.text(0, source_y - 2, "VELOCITY UP ->", color='white', ha='center', fontfamily='monospace')

        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=100, facecolor='#050505')
        
    plt.close(fig)

if __name__ == "__main__": run()
