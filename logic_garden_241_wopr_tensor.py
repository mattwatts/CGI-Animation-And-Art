"""
SOVEREIGN CODE: logic_garden_241_wopr_white.py
SYSTEM: Python 3.x / Strict Memory Management (Zero-Leakage)
SCENE: LG-241 (WOPR / Terminal Game - High Contrast Edition)
HOTFIX: Explicit gc.collect() / Agg Backend / Fig Disposal
"""

import numpy as np
import matplotlib
matplotlib.use('Agg') # Memory-safe non-interactive backend
import matplotlib.pyplot as plt
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS, DURATION = 60, 17.5
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_241_white"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-CONTRAST PALETTE (WHITE SUBSTRATE) --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205' # Absolute Black
C_AZURE     = '#007FFF' # Forward Arcs
C_INDIGO    = '#4B0082' # Cold Logic
C_MAGENTA   = '#FF0055' # Hostile Arcs
C_MANTIS    = '#00AF00' # Conclusion Lock
C_DIM       = '#D0D0D5' # Raster Grid

def render_frame(f):
    """Encapsulated frame logic for O(1) memory footprint."""
    t_sec = f / FPS
    
    # 1. Initialize Figure
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)
    ax.axis('off')

    # Background Alignment Grid (Industrialist Protocol)
    for x in np.linspace(0, 1080, 10): ax.axvline(x, color=C_DIM, lw=0.5, alpha=0.3)
    for y in np.linspace(0, 1920, 20): ax.axhline(y, color=C_DIM, lw=0.5, alpha=0.3)

    # Deterministic Data Seed
    np.random.seed(1983)
    targets = np.random.uniform(200, 1700, (30, 2))

    # PHASE 1 & 2: ARCS AND PERMUTATIONS
    if t_sec < 14.0:
        prog = min(1.0, t_sec / 14.0)
        for i, target in enumerate(targets):
            # Azure vs Magenta dichotomy
            col = C_AZURE if i % 2 == 0 else C_MAGENTA
            origin = [540, 1920] if i % 2 == 0 else [540, 0]
            
            curr_x = origin[0] * (1-prog) + target[0] * prog
            curr_y = origin[1] * (1-prog) + target[1] * prog
            
            ax.plot([origin[0], curr_x], [origin[1], curr_y], color=col, alpha=0.4, lw=1.5)
            ax.scatter(curr_x, curr_y, s=15, color=col)

        ax.text(540, 1820, f"ANALYZING: {int(t_sec * 1234567)} PERMUTATIONS", 
                color=C_TEXT, fontname='monospace', ha='center', weight='bold', fontsize=18)
        ax.text(80, 1880, "STATUS: DEFCON 1", color=C_MAGENTA, fontname='monospace', fontsize=22, weight='bold')

    # PHASE 3: THE FLASH (Inversion)
    elif 14.0 <= t_sec < 15.0:
        # High Contrast Heat Shock
        ax.set_facecolor(C_INDIGO)
        ax.text(540, 960, "TERMINAL OVERRIDE", color=C_BG, ha='center', fontsize=30, weight='bold')

    # PHASE 4: TATHĀTĀ (The Conclusion)
    else:
        ax.text(540, 960, "> A STRANGE GAME.\n> THE ONLY WINNING MOVE IS\n> NOT TO PLAY.", 
                color=C_MANTIS, fontname='monospace', ha='center', fontsize=22, weight='bold')
        if f % 30 < 15:
            ax.text(540, 750, "_", color=C_TEXT, ha='center', fontsize=30)

    # 2. Strict Memory Cleanup
    plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor=C_BG)
    fig.clf()
    plt.close(fig)
    del fig, ax
    gc.collect()

if __name__ == "__main__":
    print(f"EXECUTING LG-241 [HIGH CONTRAST / ZERO-LEAKAGE]...")
    for f in range(TOTAL_FRAMES):
        render_frame(f)
        if f % 100 == 0: print(f"MEMORY GUARD STATUS: {f}/{TOTAL_FRAMES} FRAMES COMMITTED.")
