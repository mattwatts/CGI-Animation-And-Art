"""
SOVEREIGN CODE: logic_garden_v20_starmaker_short_fixed.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: Radiation Hydrodynamics / Teller-Ulam
STATUS: CORRECTED (2-Stage Implosion)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import matplotlib.patches as patches

FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_v20_short_fixed"
os.makedirs(OUT_DIR, exist_ok=True)

def run():
    print("LOGIC GARDEN 20: THE STAR MAKER (TELLER-ULAM)")
    fig = plt.figure(figsize=(9, 16), facecolor='#000000')
    ax = fig.add_axes([0, 0, 1, 1], facecolor='#000000')

    # GEOMETRY
    # Box Limits
    BOX_W = 8
    BOX_H = 28
    # Primary (Top)
    prim_y = 8
    prim_r = 2.5
    # Secondary (Bottom)
    sec_y = -8
    sec_r = 3.5
    
    # PULSE STATE
    # Rays are particles filling the box
    rays = [] 
    
    for f in range(TOTAL_FRAMES):
        ax.clear()
        ax.set_xlim(-9, 9)
        ax.set_ylim(-16, 16)
        ax.axis('off')
        
        # --- DRAW THE BLACK BOX (HOHLRAUM) ---
        # A container for the light
        rect = patches.Rectangle((-4.5, -14), 9, 28, linewidth=5, edgecolor='#444444', facecolor='none')
        ax.add_patch(rect)
        
        # --- PHASE CONTROL ---
        PHASE_TRIGGER = 60   # 2s
        PHASE_FLOOD = 120    # 4s
        PHASE_CRUSH = 300    # 10s
        PHASE_IGNITION = 450 # 15s
        
        # 1. THE PRIMARY (RED SUN)
        if f < PHASE_TRIGGER:
            # Static waiting
            ax.add_patch(plt.Circle((0, prim_y), prim_r, color='#FF0000'))
            ax.text(0, prim_y, "FISSION", color='white', ha='center', weight='bold')
            
        elif f < PHASE_IGNITION:
            # Detonated -> Becomes Source of Radiation
            # Flash yellow/white
            col = '#FFFF00' if f % 4 < 2 else '#FFFFFF'
            ax.add_patch(plt.Circle((0, prim_y), prim_r, color=col))
            
            # EMIT RAYS constantly
            if f < PHASE_CRUSH:
                for _ in range(20): # Heavy flux
                    angle = np.random.uniform(0, 2*np.pi)
                    speed = np.random.uniform(0.5, 1.5)
                    rays.append({'x': 0, 'y': prim_y, 'vx': np.cos(angle)*speed, 'vy': np.sin(angle)*speed, 'life': 60})

        # 2. THE RAYS (YELLOW X-RAYS)
        # They fill the box but reflect off walls
        surviving_rays = []
        for r in rays:
            r['x'] += r['vx']
            r['y'] += r['vy']
            r['life'] -= 1
            
            # Wall bouncing (Containment)
            if r['x'] > 4 or r['x'] < -4: r['vx'] *= -1
            if r['y'] > 13 or r['y'] < -13: r['vy'] *= -1
            
            # Render visual pop: Bright Yellow Dot
            if r['life'] > 0:
                ax.add_patch(plt.Circle((r['x'], r['y']), 0.15, color='#FFFF00'))
                surviving_rays.append(r)
        rays = surviving_rays

        # 3. THE SECONDARY (BLUE MOON)
        # Interaction Logic
        current_sec_r = sec_r
        col_sec = '#0000FF'
        
        if f > PHASE_FLOOD and f < PHASE_IGNITION:
            # COMPRESSION PHASE
            # The more rays, the smaller it gets
            # Maps time 120->450 to radius 3.5->0.5
            progress = (f - PHASE_FLOOD) / (PHASE_IGNITION - PHASE_FLOOD)
            current_sec_r = sec_r * (1.0 - (progress * 0.9)) # Shrink to 10%
            
            # Ablation Glow (Surface heats up)
            ax.add_patch(plt.Circle((0, sec_y), current_sec_r + 0.5, color='#FFFF00', alpha=0.5))
            
        if f >= PHASE_IGNITION:
            # IGNITION PHASE
            # Expansion!
            progress = (f - PHASE_IGNITION) / 60.0
            current_sec_r = 0.5 + (progress * 15.0) # Blow up
            col_sec = '#FFFFFF' # Fusion White
            
            # Wipe screen
            if current_sec_r > 10:
                ax.add_patch(patches.Rectangle((-9, -16), 18, 32, color='#FFFFFF'))
        
        # Draw Secondary
        ax.add_patch(plt.Circle((0, sec_y), current_sec_r, color=col_sec, zorder=10))
        
        # HUD TEXT SEQUENCE
        if f < PHASE_TRIGGER:
            ax.text(0, 15, "STAGE 1: THE SPARK", color='#FF0000', ha='center', fontsize=25, weight='bold', fontfamily='monospace')
        elif f < PHASE_FLOOD:
             ax.text(0, 0, "X-RAY FLOOD", color='#FFFF00', ha='center', fontsize=30, weight='bold', fontfamily='monospace',
                    bbox=dict(facecolor='black', alpha=0.7))
        elif f < PHASE_IGNITION:
             ax.text(0, 5, "RADIATION PRESSURE", color='#FFFF00', ha='center', fontsize=20, weight='bold', fontfamily='monospace')
             ax.text(0, sec_y - 5, "COMPRESSION", color='#00FFFF', ha='center', fontsize=20, weight='bold', fontfamily='monospace')
             
             # Force Arrows on Secondary
             offset = current_sec_r + 1
             ax.arrow(0, sec_y + offset, 0, -0.5, color='#FFFF00', width=0.2, head_width=0.5)
             ax.arrow(0, sec_y - offset, 0, 0.5, color='#FFFF00', width=0.2, head_width=0.5)
             ax.arrow(offset, sec_y, -0.5, 0, color='#FFFF00', width=0.2, head_width=0.5)
             ax.arrow(-offset, sec_y, 0.5, 0, color='#FFFF00', width=0.2, head_width=0.5)
             
        elif f >= PHASE_IGNITION and current_sec_r < 10:
             ax.text(0, 0, "IGNITION", color='#000000', ha='center', fontsize=40, weight='bold', fontfamily='monospace', 
                     bbox=dict(facecolor='white', edgecolor='none'))

        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=100, facecolor='#000000')
        
    plt.close(fig)

if __name__ == "__main__": run()
