"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v72_supernode_fixed.py
MODE:   Industrial Visualization
TARGET: Medical Education / Future Workflow
STYLE:  "The Exocortex" | FIXED RENDERER
STATUS: PATCHED (Figure Persistence)

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import random

# --- 1. THE PALETTE [INDUSTRIAL] ---
PALETTE = {
    'void':   '#050505', # Almost Black
    'data':   '#00FFFF', # Cyan (The Exocortex)
    'chaos':  '#FF3333', # Red (The Patient)
    'node':   '#FFD700', # Gold (The Super-Node)
    'link':   '#FFFFFF', # White
    'grid':   '#1A1A1A'  # Dark Grey
}

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
W, H = 1920, 1080

def generate_supernode():
    out_dir = "logic_garden_supernode_frames_fixed"
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"[LOGIC GARDEN] INITIALIZING EXOCORTEX LINK (PATCHED)...")
    
    # SETUP PLOT (Create ONCE)
    fig = plt.figure(figsize=(16, 9), facecolor=PALETTE['void'])
    ax = fig.add_axes([0, 0, 1, 1], facecolor=PALETTE['void'])
    
    # --- DYNAMIC STATE ---
    
    # Matrix Rain Drops
    drops = [{'x': random.uniform(2, 30), 'y': random.uniform(0, 50), 'speed': random.uniform(0.5, 2.0)} for _ in range(50)]
    
    # Patient Signal
    t_vals = np.linspace(0, 10, 200)
    wave_buffer = np.zeros(200)
    
    # Doctor
    node_pos = {'x': 50, 'y': 25}
    beam_state = "IDLE" 
    beam_timer = 0
    target_y = 25
    
    for f in range(TOTAL_FRAMES):
        # 1. CLEAR CANVAS
        ax.clear()
        
        # 2. RESET VIEWPORT (Required after clear)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 50)
        ax.axis('off')
        ax.set_facecolor(PALETTE['void']) # Enforce void
        
        # --- A. DRAW THE EXOCORTEX (LEFT) ---
        for d in drops:
            d['y'] -= d['speed']
            if d['y'] < 0: 
                d['y'] = 50 + random.uniform(0, 10)
                d['x'] = random.uniform(2, 33)
            
            # Draw trail
            alpha = 1.0
            for k in range(5):
                y_pos = d['y'] + k
                if 0 < y_pos < 50:
                    a_val = max(0.0, alpha * 0.3)
                    rect = plt.Rectangle((d['x'], y_pos), 0.6, 0.8, color=PALETTE['data'], alpha=a_val)
                    ax.add_patch(rect)
                alpha -= 0.2
        
        ax.text(17.5, 45, "THE EXOCORTEX\n(LOW ENTROPY STORAGE)", color=PALETTE['data'], ha='center', fontfamily='monospace', fontsize=12, fontweight='bold', alpha=0.8)
        ax.text(17.5, 3, "CAPACITY: INFINITE\nLATENCY: ZERO", color=PALETTE['data'], ha='center', fontfamily='monospace', fontsize=10, alpha=0.6)

        # Separator
        ax.plot([35, 35], [5, 45], color=PALETTE['grid'], linestyle='--', linewidth=1)
        
        # --- B. DRAW THE PATIENT (RIGHT) ---
        noise = np.random.normal(0, 1.5, 200) * (np.sin(f*0.1) + 1.2)
        
        smoothing_factor = 0.0
        if beam_state == "SYNTHESIZE":
            smoothing_factor = 0.8
        
        base_sig = np.sin(t_vals * 2 + f*0.2) * 5
        current_wave = base_sig + (noise * (1.0 - smoothing_factor))
        wave_buffer = np.roll(wave_buffer, -1)
        wave_buffer[-1] = current_wave[-1]
        
        wave_x = np.linspace(67, 98, 200)
        wave_y = 25 + current_wave
        
        col_wave = PALETTE['chaos']
        if beam_state == "SYNTHESIZE":
            col_wave = "#33FF33"
            
        ax.plot(wave_x, wave_y, color=col_wave, linewidth=1.5)
        
        if beam_state == "SYNTHESIZE":
             ax.plot(wave_x, 25 + base_sig + noise, color=PALETTE['chaos'], linewidth=0.5, alpha=0.3, linestyle=":")

        ax.text(82.5, 45, "THE PATIENT\n(HIGH ENTROPY REALITY)", color=PALETTE['chaos'], ha='center', fontfamily='monospace', fontsize=12, fontweight='bold', alpha=0.8)
        
        # --- C. THE SUPER-NODE (CENTER) ---
        if beam_timer <= 0:
            r = random.random()
            if r < 0.3:
                beam_state = "IDLE"
                beam_timer = 20
                target_y = 25
            elif r < 0.6:
                beam_state = "QUERY"
                beam_timer = 15
                target_y = random.uniform(10, 40)
            else:
                beam_state = "SYNTHESIZE"
                beam_timer = 30
                
        beam_timer -= 1
        
        # Draw Node
        node_circle = plt.Circle((node_pos['x'], node_pos['y']), 1.5, color=PALETTE['node'], zorder=10)
        ax.add_patch(node_circle)
        glow = plt.Circle((node_pos['x'], node_pos['y']), 2.5 + np.sin(f*0.5)*0.5, color=PALETTE['node'], alpha=0.2, zorder=5)
        ax.add_patch(glow)
        
        ax.text(50, 20, "SUPER-NODE\n(SYNTHESIS)", color=PALETTE['node'], ha='center', fontfamily='monospace', fontsize=10, fontweight='bold')

        # --- D. BEAMS ---
        if beam_state == "QUERY":
            ax.plot([node_pos['x'], 35], [node_pos['y'], target_y], color=PALETTE['data'], linewidth=2)
            ax.plot([35], [target_y], 'o', color='white', markersize=5)
            ax.text(42, (node_pos['y']+target_y)/2, "LOOKUP", color=PALETTE['data'], fontsize=8, fontfamily='monospace')
            
        elif beam_state == "SYNTHESIZE":
            poly = plt.Polygon([[50, 25], [67, 15], [67, 35]], color=PALETTE['node'], alpha=0.2)
            ax.add_patch(poly)
            ax.plot([50, 82], [25, 25], color=PALETTE['node'], linestyle="--", linewidth=1)
            ax.text(58, 28, "HARMONIZE", color=PALETTE['node'], fontsize=8, fontfamily='monospace')

        # --- E. SAVE ---
        ax.text(50, 5, "PROTOCOL: MIGRATE THE SIGNAL, REJECT THE NOISE.", color='#aaaaaa', ha='center', fontfamily='monospace', fontsize=10)

        filename = os.path.join(out_dir, f"supernode_{f:04d}.png")
        # USE FIG.SAVEFIG, NOT PLT.SAVEFIG
        fig.savefig(filename, dpi=100, facecolor=PALETTE['void'])
        
        if f % 30 == 0:
            print(f"Frame {f}/{TOTAL_FRAMES} | State: {beam_state}")

    # CLOSE AFTER LOOP
    plt.close(fig)

if __name__ == "__main__":
    generate_supernode()
