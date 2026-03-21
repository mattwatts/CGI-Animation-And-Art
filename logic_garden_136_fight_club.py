"""
SOVEREIGN CODE: logic_garden_136_fight_club.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python High-Fidelity Simulator (C-64 Demake Protocol)
SCENE: Logic Garden 136 (Project Mayhem Phase Transition)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import math
import os

# -------- COMPILE-TIME METRICS --------
FPS = 30
DURATION = 24                   # 24-Second Execution
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_136_fightclub"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (HIGH-VOLTAGE) --------
C_VOID = '#020205'              # Absolute Black (The Void)
C_BASEMENT = '#1A1A1A'          # The Dirt/Grime background
C_RED = '#FF003C'               # Node A (Fighter) & Blood Entropy
C_GOLD = '#FFD700'              # Lightbulb / UI Core
C_CYAN = '#00FFCC'              # Project Mayhem Terminal Node
C_MANTIS = '#39FF14'            # Terminal Grid Lines
C_TEXT = '#FFFFFF'              # UI Readout
C_MAGENTA = '#FF00FF'           # Node B (Fighter)

# -------- VIC-II SPRITE ARCHITECTURE (THE SPACE MONKEY) --------
SPRITE_NODE = [
    "0011100",
    "0111110",
    "1101011",  # Blank, emotionless eyes
    "1111111",
    "1011101",
    "0111110",
    "0010100"
]
PIXEL_SIZE = 12 

def render_sprite(ax, base_x, base_y, color, scale_mult=1.0, alpha=1.0):
    px, py = [], []
    eff_size = PIXEL_SIZE * scale_mult
    for row_idx, row in enumerate(SPRITE_NODE):
        for col_idx, pixel in enumerate(row):
            if pixel == "1":
                px.append(base_x + (col_idx * eff_size) - (3 * eff_size))
                py.append(base_y - (row_idx * eff_size) + (3 * eff_size))
    if px:
        ax.scatter(px, py, s=eff_size*10, c=color, marker='s', alpha=alpha, edgecolors='none')

def run():
    print(f"LOGIC GARDEN 136: FIGHT CLUB 64")
    print(f"Executing: {FPS} FPS | Total: {TOTAL_FRAMES} frames")
    print("Initializing Project Mayhem Phase Transition...")

    # Physics Constants for Phase 1 (The Basement)
    box_w, box_h = 600, 600
    box_x, box_y = 540 - box_w/2, 960 - box_h/2
    p1 = np.array([540.0, 960.0])
    p2 = np.array([600.0, 900.0])
    v1 = np.array([-18.0, 15.0]) * 1.5
    v2 = np.array([20.0, -12.0]) * 1.5
    
    # Grid coordinates for Phase 3
    col_count, row_count = 7, 13
    grid_spacing_x = 1080 / col_count
    grid_spacing_y = 1920 / row_count

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        fig.patch.set_facecolor(C_VOID)
        ax.set_facecolor(C_VOID)
        ax.set_xlim(0, 1080)
        ax.set_ylim(0, 1920)

        # ------------------------------------------------------------------
        # STAGE 1: THE BASEMENT (High Entropy / Chaos) [0 to 6 seconds]
        # ------------------------------------------------------------------
        if t_sec < 6.0:
            # Draw the Bounding Box
            ax.add_patch(Rectangle((box_x, box_y), box_w, box_h, fill=False, edgecolor=C_BASEMENT, linewidth=10))
            
            # Simulated collision physics inside the box (Friction)
            p1 += v1
            p2 += v2
            if p1[0] < box_x+40 or p1[0] > box_x+box_w-40: v1[0] *= -1
            if p1[1] < box_y+40 or p1[1] > box_y+box_h-40: v1[1] *= -1
            if p2[0] < box_x+40 or p2[0] > box_x+box_w-40: v2[0] *= -1
            if p2[1] < box_y+40 or p2[1] > box_y+box_h-40: v2[1] *= -1
            
            # Render The Artisans
            render_sprite(ax, p1[0], p1[1], C_RED, scale_mult=1.5)
            render_sprite(ax, p2[0], p2[1], C_MAGENTA, scale_mult=1.5)
            
            # The Single Gold Lightbulb
            light_flicker = 0.5 + 0.5 * np.random.rand()
            ax.scatter(540, box_y+box_h-20, s=800 * light_flicker, c=C_GOLD, alpha=0.3, edgecolors='none')

        # ------------------------------------------------------------------
        # STAGE 2: THE SHATTER & REALIGNMENT [6 to 10 seconds]
        # ------------------------------------------------------------------
        elif 6.0 <= t_sec < 10.0:
            progress = (t_sec - 6.0) / 4.0
            
            # The nodes slowly drift to their grid anchors, changing to Terminal Cyan
            p1_target = np.array([540 - grid_spacing_x/2, 960])
            p2_target = np.array([540 + grid_spacing_x/2, 960])
            p1 = p1 + (p1_target - p1) * 0.05
            p2 = p2 + (p2_target - p2) * 0.05
            
            render_sprite(ax, p1[0], p1[1], C_CYAN, scale_mult=1.5)
            render_sprite(ax, p2[0], p2[1], C_CYAN, scale_mult=1.5)
            
            # Flash of realization (Critical Damping)
            if t_sec < 6.5:
                flash = 1.0 - ((t_sec - 6.0) * 2)
                ax.add_patch(Rectangle((0, 0), 1080, 1920, fill=True, color=C_CYAN, alpha=flash * 0.5))

        # ------------------------------------------------------------------
        # STAGE 3: PROJECT MAYHEM (Batch Execution) [10 seconds onwards]
        # ------------------------------------------------------------------
        else:
            spawn_progress = np.clip((t_sec - 10.0) / 4.0, 0, 1) # Exponential growth phase
            max_nodes = int((col_count * row_count) * (spawn_progress**2)) # Fractal recursion curve
            
            nodes_rendered = 0
            for r in range(row_count):
                for c in range(col_count):
                    nodes_rendered += 1
                    if nodes_rendered <= max_nodes or max_nodes >= (col_count * row_count):
                        nx = (c * grid_spacing_x) + (grid_spacing_x / 2)
                        ny = (r * grid_spacing_y) + (grid_spacing_y / 2)
                        
                        # Unison Pulse (The Hive Mind Breathing)
                        pulse = 1.0 + 0.2 * math.sin(t_sec * 6)
                        render_sprite(ax, nx, ny, C_CYAN, scale_mult=1.5 * pulse)
            
            # Terminal UI Scanlines (Matrix Grid)
            if t_sec > 13.0:
                scanline_y = 1920 - ((f * 30) % 1920)
                ax.axhline(scanline_y, color=C_MANTIS, linewidth=4, alpha=0.5)

        # ------------------------------------------------------------------
        # UI DECOUPLING & THE TYLER DURDEN FLIGHT RECORDER
        # ------------------------------------------------------------------
        # Fixed Terminals
        ax.text(80, 1820, "SYS.ADMIN: DURDEN, T.", color=C_GOLD, fontsize=20, fontname='monospace', weight='bold')
        
        # Phase Subtitles
        if t_sec < 6.0:
            ax.text(80, 1780, "PHASE 1: ARTISAN ENTROPY", color=C_RED, fontsize=20, fontname='monospace')
            lyric_1 = "FIGHT CLUB WAS THE BEGINNING."
            c_lyric = C_TEXT
            if (f // 10) % 2 == 0:  c_lyric = C_RED # Blinking cursor effect
            ax.text(540, 300, lyric_1, color=c_lyric, ha='center', fontsize=32, fontname='monospace', weight='bold')
            
        elif 6.0 <= t_sec < 12.0:
            ax.text(80, 1780, "PHASE 2: THE BOUNDING BOX COMPILED", color=C_TEXT, fontsize=20, fontname='monospace')
            ax.text(540, 300, "NOW IT'S MOVED OUT OF THE BASEMENT,", color=C_CYAN, ha='center', fontsize=30, fontname='monospace', weight='bold')
            
        else:
            ax.text(80, 1780, "PHASE 3: INDUSTRIAL BATCH EXECUTION", color=C_CYAN, fontsize=20, fontname='monospace')
            lyric_1 = "FIGHT CLUB WAS THE BEGINNING."
            lyric_2 = "NOW IT'S MOVED OUT OF THE BASEMENT,"
            lyric_3 = "IT'S CALLED PROJECT MAYHEM."
            
            ax.text(540, 380, lyric_1, color=C_TEXT, alpha=0.4, ha='center', fontsize=22, fontname='monospace')
            ax.text(540, 340, lyric_2, color=C_TEXT, alpha=0.4, ha='center', fontsize=22, fontname='monospace')
            
            # Massive Gold glitch pop on the final phase
            pulse_text = C_GOLD if (f // 5) % 3 != 0 else C_TEXT
            ax.text(540, 270, lyric_3, color=pulse_text, ha='center', fontsize=40, fontname='monospace', weight='bold')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close(fig)

if __name__ == "__main__": run()
