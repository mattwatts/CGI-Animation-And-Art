"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v73_kinetic_calm_fixed.py
MODE:   Industrial Visualization
TARGET: Paramedicine / The Hero
STYLE:  "The Kinetic Operator" | Aura of Calm | FIXED
STATUS: PATCHED (Iterator Variable)

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import os
import random

# --- 1. THE PALETTE [TACTICAL] ---
PALETTE = {
    'night':    '#080808', # Pitch black night
    'ai':       '#00FFFF', # Cyan (The Logic)
    'friction': '#FF4500', # OrangeRed (The Trauma Start)
    'calm':     '#32CD32', # LimeGreen (The Stabilized State)
    'operator': '#FFD700', # Gold (The Kinetic Operator)
    'rain':     '#505050', # Grey rain
    'hud':      '#00FF00'  # Green Matrix text
}

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
W, H = 1920, 1080

def interpolate_color(c1, c2, t):
    """ Blends two hex colors based on t (0.0 to 1.0) """
    rgb1 = np.array(mcolors.to_rgb(c1))
    rgb2 = np.array(mcolors.to_rgb(c2))
    result = rgb1 * (1 - t) + rgb2 * t
    return result

def generate_kinetic_calm():
    out_dir = "logic_garden_kinetic_calm_frames_fixed"
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"[LOGIC GARDEN] KINETIC DAMPENING FIELD ACTIVATED (PATCHED)...")
    
    # SETUP PLOT
    fig = plt.figure(figsize=(16, 9), facecolor=PALETTE['night'])
    ax = fig.add_axes([0, 0, 1, 1], facecolor=PALETTE['night'])
    
    # --- SCENE GEOMETRY ---
    
    # The Wreck (Jagged Polygon)
    wreck_base_x = np.array([60, 65, 75, 80, 75, 65])
    wreck_base_y = np.array([20, 35, 30, 20, 15, 10])
    
    # Rain System
    rain_drops = [{'x': random.uniform(0, 100), 'y': random.uniform(0, 50), 'len': random.uniform(2, 5)} for _ in range(100)]
    
    # Paramedic (The Operator)
    op_pos = {'x': 10, 'y': 25}
    chaos_level = 1.0 # 1.0 = Max Chaos, 0.0 = Calm
    target_x = 72
    
    ai_path_len = 0
    
    for f in range(TOTAL_FRAMES):
        # 1. CLEAR & RESET
        ax.clear()
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 50)
        ax.axis('off')
        ax.set_facecolor(PALETTE['night'])
        
        # --- A. ENVIRONMENT ---
        # Draw Rain
        for r in rain_drops:
            r['y'] -= 2.5
            if r['y'] < 0:
                r['y'] = 50 + random.uniform(0, 10)
                r['x'] = random.uniform(0, 100)
            
            # Rain fades as chaos drops
            rain_alpha = 0.5 * (0.3 + 0.7 * chaos_level)
            ax.plot([r['x'], r['x']-0.5], [r['y'], r['y']-r['len']], color=PALETTE['rain'], linewidth=1, alpha=rain_alpha)

        # Ground
        ax.plot([0, 100], [5, 5], color='#333333', linewidth=2)
        
        # --- B. THE OPERATOR LOGIC ---
        # Move Paramedic
        
        op_state = "APPROACH"
        
        if op_pos['x'] < 55:
            # AI Zone: Fast
             op_pos['x'] += 0.8 
        elif op_pos['x'] < target_x:
             # Friction Zone: Slow, purposeful
             op_state = "BREACH"
             op_pos['x'] += 0.25 
             # ENTROPY DECAY: As he gets deeper, chaos drops
             # Calculate progress through the zone (55 to 72)
             dist_in = (op_pos['x'] - 55) / (target_x - 55)
             chaos_level = max(0.0, 1.0 - dist_in)
        else:
             op_state = "STABILIZED"
             chaos_level = max(0.0, chaos_level - 0.05) # Final cooldown
        
        # --- C. THE WRECK (CHAOS & COLOR) ---
        
        # Vibration Magnitude
        vibration = 1.5 * chaos_level
        
        # Color Transition (Red to Green)
        stabilization_factor = 1.0 - chaos_level
        current_wreck_color = interpolate_color(PALETTE['friction'], PALETTE['calm'], stabilization_factor)
        
        # Apply Noise
        noise_x = np.random.uniform(-vibration, vibration, len(wreck_base_x))
        noise_y = np.random.uniform(-vibration, vibration, len(wreck_base_y))
        
        # Draw Wreck Aura (The Glow)
        if stabilization_factor > 0.1:
            aura = patches.Circle((70, 25), 15 * stabilization_factor, color=PALETTE['calm'], alpha=0.1 * stabilization_factor)
            ax.add_patch(aura)
            
        # Draw Wreck Body
        poly = patches.Polygon(np.column_stack((wreck_base_x + noise_x, wreck_base_y + noise_y)), 
                               closed=True, color=current_wreck_color, alpha=0.6)
        ax.add_patch(poly)
        
        # Wireframe
        ax.plot(wreck_base_x + noise_x, wreck_base_y + noise_y, color='white', linewidth=1, linestyle='--')
        
        # Labeling Wreck
        if stabilization_factor < 0.5:
            ax.text(70, 40, "HIGH FRICTION / NO-TAKE ZONE", color=PALETTE['friction'], ha='center', fontfamily='monospace', fontweight='bold')
        else:
            ax.text(70, 40, "STABILIZED / KINETIC CONTROL", color=PALETTE['calm'], ha='center', fontfamily='monospace', fontweight='bold')


        # --- D. THE AI (BLUE) ---
        if ai_path_len < 55:
            ai_path_len += 1
        
        ax.plot([0, ai_path_len], [25, 25], color=PALETTE['ai'], linewidth=2, alpha=0.8)
        
        if ai_path_len >= 55:
            # The Wall
            ax.plot([55, 55], [0, 50], color=PALETTE['ai'], linestyle=":", linewidth=1)
            # Glitch
            for _ in range(5):
                gx = 55 + random.uniform(0, 5)
                gy = 25 + random.uniform(-10, 10)
                ax.plot([55, gx], [25, gy], color=PALETTE['ai'], alpha=0.5, linewidth=0.5)
            
            # Show AI Text only until Paramedic fixes it
            if stabilization_factor < 0.8:
                ax.text(50, 45, "AI LIMIT REACHED", color=PALETTE['ai'], ha='right', fontfamily='monospace', fontweight='bold')

        # --- E. THE OPERATOR (GOLD) ---
        
        # Draw Paramedic
        bodhi = plt.Circle((op_pos['x'], op_pos['y']), 2, color=PALETTE['operator'], zorder=10)
        ax.add_patch(bodhi)
        
        # Paramedic's Personal Aura (Field Generator)
        if op_state != "APPROACH":
            field_radius = 4 + (stabilization_factor * 8)
            field = patches.Circle((op_pos['x'], op_pos['y']), field_radius, color=PALETTE['calm'], alpha=0.15, zorder=5)
            ax.add_patch(field)

        ax.text(op_pos['x'], 20, "OPERATOR", color=PALETTE['operator'], ha='center', fontfamily='monospace', fontsize=10, fontweight='bold')

        # --- F. HUD METRICS ---
        
        # "ENTROPY" Bar (Drops)
        rect_bg = patches.Rectangle((5, 5), 5, 20, color='#333333')
        rect_fill = patches.Rectangle((5, 5), 5, 20 * chaos_level, color=PALETTE['friction']) # Drops with chaos
        ax.add_patch(rect_bg)
        ax.add_patch(rect_fill)
        ax.text(7.5, 4, "ENTROPY", color='white', ha='center', fontfamily='monospace', fontsize=8)
        
        # "AGENCY" Bar (Rises)
        rect_bg2 = patches.Rectangle((12, 5), 5, 20, color='#333333')
        rect_fill2 = patches.Rectangle((12, 5), 5, 20 * stabilization_factor, color=PALETTE['calm']) # Rises with calm
        ax.add_patch(rect_bg2)
        ax.add_patch(rect_fill2)
        ax.text(14.5, 4, "AGENCY", color='white', ha='center', fontfamily='monospace', fontsize=8)

        # Footer
        ax.text(50, 2, "PROTOCOL: YOU ARE THE GROUND WIRE.", color='#aaaaaa', ha='center', fontfamily='monospace', fontsize=10)

        # SAVE (Fixed filename iterator)
        filename = os.path.join(out_dir, f"kinetic_calm_{f:04d}.png")
        fig.savefig(filename, dpi=100, facecolor=PALETTE['night'])
        
        if f % 30 == 0:
            print(f"Frame {f}/{TOTAL_FRAMES} | Chaos: {chaos_level:.2f}")

    plt.close(fig)

if __name__ == "__main__":
    generate_kinetic_calm()
