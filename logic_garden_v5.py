"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v5.py
MODE:   Nursery (Bauhaus Palette)
TARGET: Pendulum Wave (Harmonic Resonance)
STYLE:  "The Dancing Snake" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from matplotlib.lines import Line2D
import os

# --- 1. THE NURSERY PALETTE ---
BG_COLOR = "#FFFFFF"       # Void
STRING_COLOR = "#333333"   # The Connection
BALL_COLORS = ["#FFD700", "#FF4500", "#0080FF"] # Yellow, Red, Blue cycling

# --- 2. PHYSICS CONFIGURATION ---
NUM_PENDULUMS = 15
DURATION = 60.0    # Seconds for full cycle
FPS = 30
TOTAL_FRAMES = int(DURATION * FPS)

# Tuned Frequencies for the Wave Effect
# f = swings per cycle
# Ball 0 does 50 swings
# Ball 14 does 50 + 14 swings
BASE_CYCLES = 20 # Lower = Slower, more meditative
FREQUENCIES = np.array([BASE_CYCLES + i for i in range(NUM_PENDULUMS)])
ANGULAR_VELOCITIES = 2 * np.pi * FREQUENCIES / DURATION

# Amplitude
MAX_THETA = np.pi / 5  # Swing angle (36 degrees)

def render_wave_frame(frame_idx):
    # Time
    t = frame_idx / FPS
    
    # 1. Canvas
    fig = plt.figure(figsize=(16, 9), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.set_facecolor(BG_COLOR)
    
    # 2. Draw The "Ceiling" (Support Beam)
    # A solid black bar at the top
    ax.add_patch(Rectangle((-8, 3.5), 16, 0.2, color="#000000"))
    
    # 3. Calculate and Draw Pendulums
    # We maintain a 3D illusion by spacing them in X, swinging in Z (projected to X) 
    # OR simpler Side View? 
    # Let's do a "Top Down / Front" Hybrid. 
    # Perspective: 
    # X-axis: The row of pendulums (Left to Right)
    # Y-axis: The swing displacement (Up/Down on screen represents Forward/Back)
    
    # Let's use the standard "Front View" where they are stacked in depth
    # But for a 2D child's toy look, let's create a "3D" displacement
    # x_pos = pendulum_index
    # y_pos = length - cos(theta) ... 
    
    # Better Visual for Kids: 
    # View from TOP. Balls move Up and Down screen. 
    # X axis is their spacing.
    
    spacing = 1.0
    x_offsets = np.linspace(-7, 7, NUM_PENDULUMS)
    
    for i in range(NUM_PENDULUMS):
        # Physics
        omega = ANGULAR_VELOCITIES[i]
        theta = MAX_THETA * np.cos(omega * t)
        
        # Projection (Top View)
        # The ball moves in a horizontal arc.
        # Viewed from top, it's simple harmonic motion on Y axis.
        
        x_base = x_offsets[i]
        amplitude_y = 3.0 # How far they swing visually on screen
        
        # Current Position
        px = x_base
        py = amplitude_y * np.sin(theta)
        
        # Color Cycle
        color = BALL_COLORS[i % 3]
        
        # Draw "Track" or "String"?
        # Since it's top view, let's draw a faint line for the path
        ax.plot([x_base, x_base], [-amplitude_y, amplitude_y], 
                color="#F0F0F0", linewidth=2, zorder=1)
        
        # Draw Center Line (Equilibrium)
        # ax.plot([-8, 8], [0, 0], color=GRID_COLOR, linewidth=1)
        
        # Draw The Ball
        # Add a "Pseudo-3D" effect: 
        # When y is negative (bottom), ball is smaller? No, keep it flat "Bauhaus".
        
        # Connector Line (The String - interpreted as a rod here)
        # In visual representation, let's connect them to the center?
        # No, for "Snake" effect, we just render the balls.
        
        # Let's add a "Shadow" to separate from background
        shadow = Circle((px, py - 0.05), 0.35, color="#EEEEEE", zorder=2)
        ax.add_patch(shadow)
        
        # The Ball
        ball = Circle((px, py), 0.35, color=color, zorder=3)
        ax.add_patch(ball)
        
        # Highlight (Shiny Plastic Look)
        glint = Circle((px - 0.1, py + 0.1), 0.1, color="#FFFFFF", alpha=0.6, zorder=4)
        ax.add_patch(glint)

    # Scale
    ax.set_xlim(-9, 9)
    ax.set_ylim(-5, 5)
    ax.set_aspect('equal')
    
    # Save
    out_dir = "logic_garden_wave_frames"
    os.makedirs(out_dir, exist_ok=True)
    filename = os.path.join(out_dir, f"wave_{frame_idx:04d}.png")
    plt.savefig(filename, facecolor=BG_COLOR)
    plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Tuning the Harmonic Snake...")
    
    # Render full cycle
    for i in range(TOTAL_FRAMES):
        render_wave_frame(i)
        
        if i % 50 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
