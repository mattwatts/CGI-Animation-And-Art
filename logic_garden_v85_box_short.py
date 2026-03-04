"""
SOVEREIGN CODE: logic_garden_v85_box_short.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: Monro-Kellie Doctrine / ICP
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import matplotlib.patches as patches

FPS = 30
DURATION = 15
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_v85_short"
os.makedirs(OUT_DIR, exist_ok=True)

def run():
    print("LOGIC GARDEN 85: THE BOX")
    fig = plt.figure(figsize=(9, 16), facecolor='#000000')
    ax = fig.add_axes([0, 0, 1, 1], facecolor='#000000')
    
    # Initial Volumes (Units arbitrary, total 20)
    v_brain = 16.0
    v_csf = 2.0
    v_blood = 2.0 # Normal blood
    v_bleed = 0.0 # The problem
    
    skull_h = 20.0
    skull_w = 10.0
    
    for f in range(TOTAL_FRAMES):
        ax.clear()
        ax.set_xlim(-9, 9)
        ax.set_ylim(-5, 25)
        ax.axis('off')
        
        # LOGIC
        # Bleed starts at f=60
        if f > 60:
            v_bleed += 0.05
            
        # COMPENSATION (Monro-Kellie)
        # 1. Squeeze CSF out first
        current_csf = max(0.0, v_csf - v_bleed)
        
        # 2. If bleed > csf, Squeeze Blood? No, Venous but simplified.
        # 3. Squeeze Brain (Herniation)
        # Total volume attempting to exist
        total_vol = v_brain + v_blood + current_csf + v_bleed
        
        herniation = 0.0
        if total_vol > 20.0:
            herniation = total_vol - 20.0
            total_vol = 20.0 # Capped by skull
            
        # RENDER STACK
        # Bottom -> Up
        # 1. BRAIN (Grey) - Moves down if herniating? No, stays at bottom, gets squeezed?
        # Let's visualize herniation as "Red pushing Grey out bottom"
        
        y_cursor = 0
        
        # BRAIN
        effective_brain = v_brain 
        rect_brain = patches.Rectangle((-5, y_cursor), 10, effective_brain, color='#666666')
        ax.add_patch(rect_brain)
        ax.text(0, y_cursor + effective_brain/2, "BRAIN", color='white', ha='center', weight='bold')
        y_cursor += effective_brain
        
        # BLOOD (Normal - Red)
        rect_blood = patches.Rectangle((-5, y_cursor), 10, v_blood, color='#880000')
        ax.add_patch(rect_blood)
        y_cursor += v_blood
        
        # CSF (Blue)
        if current_csf > 0.1:
            rect_csf = patches.Rectangle((-5, y_cursor), 10, current_csf, color='#00FFFF')
            ax.add_patch(rect_csf)
            ax.text(0, y_cursor + current_csf/2, "CSF", color='black', ha='center', fontsize=10)
            y_cursor += current_csf
            
        # BLEED (Bright Red)
        if v_bleed > 0.1:
            rect_bleed = patches.Rectangle((-5, y_cursor), 10, v_bleed, color='#FF0000')
            ax.add_patch(rect_bleed)
            ax.text(0, y_cursor + v_bleed/2, "BLEED", color='white', ha='center', weight='bold')

        # SKULL (Fixed Container)
        skull = patches.Rectangle((-5, 0), 10, 20, linewidth=5, edgecolor='white', facecolor='none')
        ax.add_patch(skull)
        
        # HERNIATION VISUAL
        if herniation > 0:
            # Draw "Brain" leaking out bottom
            leak = patches.Rectangle((-3, -herniation), 6, herniation, color='#666666')
            ax.add_patch(leak)
            ax.text(0, -herniation-1, "HERNIATON", color='#FF0000', ha='center', weight='bold', fontsize=20)
            
        # HUD
        ax.text(0, 22, "MONRO-KELLIE", color='white', ha='center', fontsize=25, weight='bold', fontfamily='monospace')
        
        status = "COMPENSATED"
        if current_csf < 0.1 and herniation == 0: status = "UNCOMPENSATED (DANGER)"
        if herniation > 0: status = "TERMINAL"
        
        cols = {'COMPENSATED':'#00FF00', 'UNCOMPENSATED (DANGER)':'#FFFF00', 'TERMINAL':'#FF0000'}
        ax.text(0, -4, status, color=cols.get(status, 'white'), ha='center', fontsize=15, fontfamily='monospace', weight='bold')

        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=100, facecolor='#000000')
        
    plt.close(fig)

if __name__ == "__main__": run()
