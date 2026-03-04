"""
SOVEREIGN CODE: logic_garden_v77_orbit_short_fixed.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: Orbital Decay
STATUS: PATCHED (Zero Division Guard)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

FPS, DURATION = 30, 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_v77_short_fixed"
os.makedirs(OUT_DIR, exist_ok=True)

def run():
    print("LOGIC GARDEN 77: ORBIT (SHORT FORMAT / FIXED)")
    fig = plt.figure(figsize=(9, 16), facecolor='#000011')
    ax = fig.add_axes([0, 0, 1, 1], facecolor='#000011')

    trail_x, trail_y = [], []
    
    # Physics State
    r = 7.5 
    theta = 0.0
    decay_rate = 0.005
    impact = False
    
    for f in range(TOTAL_FRAMES):
        ax.clear()
        ax.set_xlim(-9, 9)
        ax.set_ylim(-16, 16)
        ax.axis('off')
        
        # PHYSICS ENGINE (GUARDED)
        if r > 1.2: # Buffer above 0
            theta += 0.05 + (1.0 / r)*0.1
            r -= decay_rate * (10.0 / r)
            
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            
            trail_x.append(x)
            trail_y.append(y)
            if len(trail_x) > 300: 
                trail_x.pop(0)
                trail_y.pop(0)
        else:
            impact = True
            r = 0 # Clamp to core

        # Draw Planet
        planet = plt.Circle((0, 0), 2.0, color='#0000AA')
        atmos = plt.Circle((0, 0), 2.5, color='#FFFFFF', alpha=0.1)
        ax.add_patch(planet)
        ax.add_patch(atmos)
        
        # Draw Trail
        if len(trail_x) > 0:
            ax.plot(trail_x, trail_y, color='#FFD700', linewidth=2, alpha=0.8)
        
        # Draw Sat or Explosion
        if not impact:
            sat = plt.Circle((x, y), 0.4, color='#FFD700', zorder=10)
            ax.add_patch(sat)
        else:
             # Impact Visual
             ax.text(0, 0, "IMPACT", color='white', ha='center', weight='bold', fontsize=30)
             # Flash effect
             if f % 10 < 5:
                 ax.add_patch(plt.Circle((0,0), 3.0, color='#FF4500', alpha=0.5))

             
        # HUD Information
        ax.text(0, 14, "ORBIT DECAY", color='#FFD700', ha='center', fontsize=25, weight='bold', fontfamily='monospace')
        
        if not impact:
            ax.text(0, -14, f"ALTITUDE: {r:.2f} km", color='white', ha='center', fontsize=20, fontfamily='monospace')
        else:
            ax.text(0, -14, "STATUS: TERMINATED", color='#FF0000', ha='center', fontsize=20, fontfamily='monospace')
        
        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=100, facecolor='#000011')
        
    plt.close(fig)

if __name__ == "__main__": run()
