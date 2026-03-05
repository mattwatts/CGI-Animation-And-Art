"""
SOVEREIGN CODE: logic_garden_v94_cycles_short.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: Cliodynamics / War & Peace Cycles
VISUAL: The "Breathing" of Empire (Expansion -> Overextension -> Collapse)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_v94_cycles"
os.makedirs(OUT_DIR, exist_ok=True)

# Canvas
W, H = 1080, 1920
CENTER = (W/2, H/2)

def run():
    print("LOGIC GARDEN 94: THE SECULAR CYCLE")
    fig = plt.figure(figsize=(9, 16), facecolor='#050505')
    ax = fig.add_axes([0, 0, 1, 1], facecolor='#050505')
    
    # PARAMETERS
    # The Empire is a set of particles
    num_particles = 2000
    
    # State: 0=Void, 1=Growth(Green), 2=Stagnation(Yellow), 3=War(Red), 4=Ash(Grey)
    # We simulate the radius behaving like a Sine Wave
    
    for f in range(TOTAL_FRAMES):
        ax.clear()
        ax.set_xlim(0, W)
        ax.set_ylim(0, H)
        ax.axis('off')
        
        # TIME DRIVER (0.0 to 1.0)
        t = f / float(TOTAL_FRAMES)
        
        # CYCLE LOGIC:
        # 0.0 - 0.4: RISE (Peace/Expansion)
        # 0.4 - 0.6: PEAK (Stagnation/Overextension)
        # 0.6 - 0.8: FALL (War/Collapse)
        # 0.8 - 1.0: ASH (Reset)
        
        current_radius = 0
        chaos_factor = 0
        color_mode = "GREEN"
        
        if t < 0.4:
            # EXPANSION
            # Logistic Growth
            progress = t / 0.4
            current_radius = 50 + 800 * (1 / (1 + np.exp(-10 * (progress - 0.5))))
            color_mode = "GREEN"
            
        elif t < 0.6:
            # STAGNATION
            current_radius = 800 + 50 * np.sin(f * 0.1) # Wobble
            chaos_factor = (t - 0.4) * 50 # Jitter starts
            color_mode = "YELLOW"
            
        elif t < 0.85:
            # COLLAPSE (War)
            # Implosion
            progress = (t - 0.6) / 0.25
            current_radius = 800 * (1 - progress**2) # Accelerating collapse
            chaos_factor = 100 + progress * 200 # Max Chaos
            color_mode = "RED"
            
        else:
            # ASH / REBIRTH
            current_radius = 50 * (t - 0.85) * 5 # A tiny seed remains
            chaos_factor = 0
            color_mode = "WHITE"
            
        # RENDER DOTS
        # Generate particles in a circle
        # We use consistent random seed per frame to make them "flow" not flicker?
        # No, let's use a fixed set of angles and vary radius
        
        np.random.seed(42) # Base structure
        angles = np.random.uniform(0, 2*np.pi, num_particles)
        
        # Base radii (Gaussian spread around current_radius)
        # Expansion: Tight
        # War: Ragged
        
        spread = 50
        if color_mode == "RED": spread = 200
        
        # Each frame, the noise is different = "Static/Energy"
        # To make it flow, we should've tracked particles. 
        # For "Industrial Arbitrage", static noise per frame looks like "Energy Field".
        # Let's Seed with Frame ID for "Active" noise, or fixed for "Structure"?
        
        np.random.seed(f) # Active boil
        
        radii = np.random.normal(current_radius, spread, num_particles)
        radii = np.clip(radii, 0, 1500)
        
        # Scatter layout
        x = CENTER[0] + radii * np.cos(angles)
        y = CENTER[1] + radii * np.sin(angles) + chaos_factor * np.random.randn(num_particles)
        
        # COLORS
        if color_mode == "GREEN":
            # Azure/Teal gradient
            c = '#00FFCC'
            alpha = 0.6
        elif color_mode == "YELLOW":
            # Gold/Warning
            c = '#FFD700'
            alpha = 0.7
        elif color_mode == "RED":
            # Bloody
            c = '#FF0033'
            alpha = 0.8
        else:
            c = '#444444' # Ash
            alpha = 0.3
            
        # DRAW
        ax.scatter(x, y, s=5, c=c, alpha=alpha, edgecolors='none')
        
        # HUD TEXT
        title = ""
        subtitle = ""
        
        if t < 0.4:
            title = "THE RISE"
            subtitle = "EXPANSION PHASE"
            t_col = "#00FFCC"
        elif t < 0.6:
            title = "THE PEAK"
            subtitle = "OVER-EXTENSION"
            t_col = "#FFD700"
        elif t < 0.85:
            title = "THE FALL"
            subtitle = "SYSTEM COLLAPSE"
            t_col = "#FF0033"
        else:
            title = "THE RESET"
            subtitle = "HISTORY REPEATS"
            t_col = "#888888"
            
        # Dramatic Titles
        ax.text(W/2, H - 300, title, color=t_col, ha='center', fontsize=50, weight='bold', fontfamily='monospace')
        ax.text(W/2, H - 400, subtitle, color='white', ha='center', fontsize=30, fontfamily='monospace')

        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=80, facecolor='#050505')
        
    plt.close(fig)

if __name__ == "__main__": run()
