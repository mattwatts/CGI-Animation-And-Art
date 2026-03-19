"""
SOVEREIGN CODE: logic_garden_128_quantum_ocean.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python High-Fidelity Simulator
SCENE: Logic Garden 128 (The Quantum Ocean / Pair Production)
VERSION: 1.1 (Syntax Repaired)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import math

# CONFIG
FPS = 30
DURATION = 15
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_128_quantum_ocean"
os.makedirs(OUT_DIR, exist_ok=True)

# THE INDUSTRIAL PALETTE
C_VOID = '#020205'         # Absolute Vacuum
C_NILA_BINDU = '#002FA7'   # International Klein Blue (Probability Field)
C_MATTER = '#00FFCC'       # Cyan (Existence / Particle)
C_ANTIMATTER = '#FF003C'   # Red (Shadow / Anti-particle)
C_ENERGY = '#FFD700'       # Gold (Annihilation Flash)
C_TEXT = '#FFFFFF'         # White UI

def draw_bloom_node(ax, x, y, radius, color):
    """Protocol: NEON POP. Renders an intense, multi-layered energy packet."""
    ax.scatter([x], [y], s=radius*10, c=color, alpha=1.0, zorder=10, edgecolors='none')
    ax.scatter([x], [y], s=radius*30, c=color, alpha=0.5, zorder=9, edgecolors='none')
    ax.scatter([x], [y], s=radius*150, c=color, alpha=0.15, zorder=8, edgecolors='none')

def run():
    print(f"LOGIC GARDEN 128: THE QUANTUM OCEAN ({TOTAL_FRAMES} frames)")
    
    # 1. ESTABLISH THE FIELD MATRIX
    # A dense 2D grid representing the underlying quantum ether
    X_C, Y_C = 540, 960
    x_range = np.linspace(50, 1030, 45)
    y_range = np.linspace(100, 1820, 75)
    X, Y = np.meshgrid(x_range, y_range)
    X_flat, Y_flat = X.flatten(), Y.flatten()
    
    # Timings
    F_BREATHE = 60          # Pure vacuum fluctuations
    F_EMERGE = 140          # Pair production (Tethering)
    F_ORBIT = 320           # Stable orbit / Existence
    F_COLLAPSE = 360        # Annihilation / Flash
    
    for f in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(C_VOID)
        
        t = f / FPS
        
        # --- PARTICLE KINETICS ---
        p_dist = 0
        p_angle = t * 4  # Orbital frequency
        flash_intensity = 0
        
        # Phase Logic
        if f > F_BREATHE and f <= F_EMERGE:
            # Emergence: Spreading apart
            progress = (f - F_BREATHE) / (F_EMERGE - F_BREATHE)
            p_dist = (1 - (1 - progress)**2) * 200 # Ease out
        elif f > F_EMERGE and f <= F_ORBIT:
            # Stable Existence
            p_dist = 200
        elif f > F_ORBIT and f <= F_COLLAPSE:
            # Recombination / Orbital Decay
            progress = (f - F_ORBIT) / (F_COLLAPSE - F_ORBIT)
            p_dist = 200 * (1 - progress**3) # Accelerating decay
            p_angle = t * (4 + (progress * 15)) # Spin speeds up immensely as they approach
        
        if f == F_COLLAPSE:
            flash_intensity = 1.0
        elif f > F_COLLAPSE:
            flash_intensity = max(0, 1.0 - ((f - F_COLLAPSE) / 30.0))
        
        # Particle Coordinates
        p1_x = X_C + math.cos(p_angle) * p_dist
        p1_y = Y_C + math.sin(p_angle) * p_dist
        
        p2_x = X_C + math.cos(p_angle + math.pi) * p_dist
        p2_y = Y_C + math.sin(p_angle + math.pi) * p_dist
        
        # --- THE QUANTUM OCEAN (FIELD CALCULATION) ---
        # Base Zero-Point Fluctuations (Standing Waves)
        Z_base = np.sin(X_flat/80 + t*1.5) * np.cos(Y_flat/120 - t*0.8)
        
        # Interference Ripples from Mass/Energy Presence
        if p_dist > 0:
            d1 = np.sqrt((X_flat - p1_x)**2 + (Y_flat - p1_y)**2)
            d2 = np.sqrt((X_flat - p2_x)**2 + (Y_flat - p2_y)**2)
            # Inverse-square masking for field distortion ripples
            ripple1 = np.sin(d1/20 - t*10) * np.exp(-d1/300) * 3
            ripple2 = np.sin(d2/20 - t*10) * np.exp(-d2/300) * 3
            Z_total = Z_base + ripple1 + ripple2
        else:
            Z_total = Z_base
            
        if flash_intensity > 0:
            # The Annihilation Shockwave
            d_center = np.sqrt((X_flat - X_C)**2 + (Y_flat - Y_C)**2)
            shockwave = np.sin(d_center/15 - (f-F_COLLAPSE)*0.8) * np.exp(-d_center/(100 + flash_intensity*1000))
            Z_total += shockwave * flash_intensity * 10
        
        # Normalize node sizes and opacity
        sizes = 10 + np.abs(Z_total) * 40
        alphas = np.clip(0.1 + np.abs(Z_total) * 0.2, 0, 1)

        # Draw The Ocean
        ocean_color = C_NILA_BINDU if flash_intensity == 0 else C_ENERGY
        ax.scatter(X_flat, Y_flat, s=sizes, c=ocean_color, alpha=alphas, edgecolors='none', zorder=1)
        
        # --- RENDER EXISTENCE (THE PARTICLES) ---
        state_text = "[ STATE: ZERO-POINT FIELD ]"
        val_color = C_NILA_BINDU
        
        if p_dist > 0:
            draw_bloom_node(ax, p1_x, p1_y, 40, C_MATTER)
            draw_bloom_node(ax, p2_x, p2_y, 40, C_ANTIMATTER)
            state_text = "[ STATE: PAIR PRODUCTION (EXISTENCE) ]"
            val_color = C_MATTER
            
            # Draw Quantum Tether (Entanglement)
            ax.plot([p1_x, p2_x], [p1_y, p2_y], color=C_TEXT, lw=2, alpha=0.3, zorder=2)
            
        if flash_intensity > 0:
            # Annihilation Glow
            draw_bloom_node(ax, X_C, Y_C, 200 * flash_intensity, C_ENERGY)
            draw_bloom_node(ax, X_C, Y_C, 50 * flash_intensity, C_TEXT)
            state_text = "[ STATE: ANNIHILATION / RECONCILIATION ]"
            val_color = C_ENERGY
            
        if f > F_COLLAPSE + 30:
            state_text = "[ STATE: TATHĀTĀ (THE VOID RETURNS) ]"
            val_color = C_NILA_BINDU
            
        # UI HUD
        ax.text(540, 1820, "LOGIC GARDEN 128", color=C_TEXT, ha='center', fontsize=35, fontname='monospace', weight='bold')
        ax.text(540, 1780, state_text, color=val_color, ha='center', fontsize=22, fontname='monospace')
        
        # Bounding Constraints
        ax.set_xlim(0, 1080)
        ax.set_ylim(0, 1920)

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close(fig)

if __name__ == "__main__": run()
