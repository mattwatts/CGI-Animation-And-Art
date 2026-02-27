"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v6.py
MODE:   Nursery (Bauhaus Palette)
TARGET: Lissajous Figures (Parametric Geometry)
STYLE:  "The Invisible Pen" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from matplotlib.collections import LineCollection
import os

# --- 1. THE NURSERY PALETTE ---
BG_COLOR = "#FFFFFF"       # Void
GUIDE_COLOR = "#DDDDDD"    # Soft Mechanical Lines
DRIVER_X_COLOR = "#FFD700" # Cyber Yellow (Horizontal Logic)
DRIVER_Y_COLOR = "#FF4500" # Safety Red (Vertical Logic)
PEN_COLOR = "#0080FF"      # Azure Blue (The Synthesis)

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20 # Seconds
TOTAL_FRAMES = FPS * DURATION
R = 1.5                # Radius of circles

# Layout Coordinates (16:9 Canvas is roughly -8 to 8, -4.5 to 4.5)
# Center of Drawing
DRAW_X, DRAW_Y = 2, -1.5

# Driver Positions relative to drawing
OFFSET = 4.0
DRIVER_X_POS = (DRAW_X, DRAW_Y + OFFSET)     # Top
DRIVER_Y_POS = (DRAW_X - OFFSET, DRAW_Y)     # Left

def render_lissajous_frame(frame_idx):
    # Time
    t_global = frame_idx / FPS
    
    # 1. Canvas
    fig = plt.figure(figsize=(16, 9), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.set_facecolor(BG_COLOR)
    
    # 2. Physics (The Frequencies)
    # Omega X is constant (The Base Rhythm)
    omega_x = 1.0 * (2 * np.pi) # 1 Hz
    
    # Omega Y speeds up slowly (The Melody)
    # Ramps from 1.0 to 3.0
    progress = frame_idx / TOTAL_FRAMES
    freq_ratio = 1.0 + (2.0 * progress) # 1 -> 3
    omega_y = freq_ratio * (2 * np.pi)
    
    # Current Phase for the Dots
    phase_x = omega_x * t_global
    # Note: For Y, we integrate frequency because it changes over time
    # phi = integral(omega dt). Simplification: just use current ratio * t for visual flow
    # This might cause a "jump" if we aren't careful, but linear ramp * t produces chirp.
    # Correct Phase = 2*pi * (1*t + t^2/(2*T)*(increase))
    # Let's keep it simple: t * current_freq (slight slip but ok for kids)
    phase_y = omega_y * t_global 
    
    # 3. Calculate Positions
    # Driver X (Top) - Moves Cosine (Left/Right)
    dx_local = R * np.cos(phase_x)
    dy_local = R * np.sin(phase_x)
    pos_x_driver = (DRIVER_X_POS[0] + dx_local, DRIVER_X_POS[1] + dy_local)
    
    # Driver Y (Left) - Moves Sine (Up/Down)
    # Note: Standard parametric is x=cos, y=sin.
    dx_local_y = R * np.cos(phase_y) # Visual rotation
    dy_local_y = R * np.sin(phase_y) # Visual rotation
    pos_y_driver = (DRIVER_Y_POS[0] + dx_local_y, DRIVER_Y_POS[1] + dy_local_y)
    
    # The Pen (Synthesis)
    # X comes from Driver X's horizontal position
    # Y comes from Driver Y's vertical position
    pen_x = DRAW_X + (pos_x_driver[0] - DRIVER_X_POS[0])
    # For Lissajous, Y driver usually drives Y amplitude.
    pen_y = DRAW_Y + (pos_y_driver[1] - DRIVER_Y_POS[1])
    
    # 4. Draw GUIDES (The Mechanism)
    # Circle X
    circle_x = Circle(DRIVER_X_POS, R, fill=False, edgecolor=GUIDE_COLOR, linewidth=3)
    ax.add_patch(circle_x)
    # Circle Y
    circle_y = Circle(DRIVER_Y_POS, R, fill=False, edgecolor=GUIDE_COLOR, linewidth=3)
    ax.add_patch(circle_y)
    
    # Connector Lines (Dashed)
    # Vertical Line from X Driver to Pen
    ax.plot([pos_x_driver[0], pen_x], [pos_x_driver[1], pen_y], 
            color=DRIVER_X_COLOR, linestyle='--', linewidth=2, alpha=0.5)
    # Horizontal Line from Y Driver to Pen
    ax.plot([pos_y_driver[0], pen_x], [pos_y_driver[1], pen_y], 
            color=DRIVER_Y_COLOR, linestyle='--', linewidth=2, alpha=0.5)

    # 5. Draw The TRACE (The History)
    # calculate the history tail
    tail_len = 120 # frames
    points = []
    
    # Generate history analytically to look smooth
    current_ratio = freq_ratio
    for i in range(tail_len):
        hist_t = t_global - (i * 0.02) # finer steps
        if hist_t < 0: break
        
        # Approximate history with CURRENT ratio to show the standing wave shape
        # (If we use true history, the line morphs/wiggles. 
        # For 'Ghost Trace' usually we want to see the shape *as it is now*.)
        
        h_px = DRAW_X + R * np.cos(omega_x * hist_t)
        # Use current ratio for the "Ideal Shape" visualization
        h_py = DRAW_Y + R * np.sin(current_ratio * omega_x * hist_t) 
        
        points.append((h_px, h_py))
        
    if len(points) > 1:
        pts = np.array(points).reshape(-1, 1, 2)
        segments = np.concatenate([pts[:-1], pts[1:]], axis=1)
        
        # Fade Alpha
        alphas = np.linspace(1.0, 0.0, len(segments))
        lc = LineCollection(segments, colors=PEN_COLOR, linewidths=6, alpha=alphas, capstyle='round')
        ax.add_collection(lc)

    # 6. Draw The DOTS (The Agents)
    # Driver X Dot
    ax.add_patch(Circle(pos_x_driver, 0.25, color=DRIVER_X_COLOR, zorder=10))
    # Driver Y Dot
    ax.add_patch(Circle(pos_y_driver, 0.25, color=DRIVER_Y_COLOR, zorder=10))
    # Pen Dot
    ax.add_patch(Circle((pen_x, pen_y), 0.3, color=PEN_COLOR, zorder=11))
    
    # 7. Labels (Ratio)
    # ax.text(-7, 3.5, f"RATIO: 1 : {freq_ratio:.1f}", fontsize=20, fontfamily='monospace', color='#CCCCCC')

    # Scale
    ax.set_xlim(-8, 8)
    ax.set_ylim(-4.5, 4.5)
    ax.set_aspect('equal')
    
    # Save
    out_dir = "logic_garden_curve_frames"
    os.makedirs(out_dir, exist_ok=True)
    filename = os.path.join(out_dir, f"curve_{frame_idx:04d}.png")
    plt.savefig(filename, facecolor=BG_COLOR)
    plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Connecting the Invisible Pen...")
    for i in range(TOTAL_FRAMES):
        render_lissajous_frame(i)
        if i % 30 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
