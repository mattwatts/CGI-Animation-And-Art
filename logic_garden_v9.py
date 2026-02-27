"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v9.py
MODE:   Nursery (Bauhaus Palette)
TARGET: Fourier Series (Epicycles)
STYLE:  "The Clockwork Square" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.collections import LineCollection
import os

# --- 1. THE NURSERY PALETTE ---
BG_COLOR = "#FFFFFF"       # Void
GEAR_COLOR = "#E0E0E0"     # Soft Guide Circles
ARM_1_COLOR = "#FFD700"    # Cyber Yellow
ARM_2_COLOR = "#FF4500"    # Safety Red
TRACE_COLOR = "#0080FF"    # Azure Blue

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20  # One full slow rotation
TOTAL_FRAMES = FPS * DURATION

# Fourier Coefficients for a Square Wave (Approximation)
# We treat this as a complex phasor sum: Z(t) = Sum( Amp_n * exp(i * n * t) )
# For a square path in 2D, strictly speaking, it requires a specific set of counter-rotating phasors.
# However, the classic "Square Wave" (1D Y vs Time) wrapped around polar matches the visual well enough for kids?
# No, let's do the proper "Square in Complex Plane" coefficients.
# Actually, the 1D Square Wave components (1, 1/3, 1/5...) applied to Y, and cosine components to X?
# Let's simplify: A classic "Square Wave" signal generator is usually shown as:
# Y = sin(t) + 1/3 sin(3t)...
# To draw an actul SQUARE BOX in 2D, we need both X and Y.
# 4 connected vectors summing to a square path.

# Let's use the standard "Spinning Arms representing harmonic addition"
# Harmonics: 1, -3, 5, -7 ... (Alternating direction creates the corners)
# Frequency: n
# Amplitude: 1/n

HARMONICS = [1, -3, 5, -7, 9, -11] 
SCALES =    [1.5, 1.5/3, 1.5/5, 1.5/7, 1.5/9, 1.5/11] # 1/n decay

def render_fourier_frame(frame_idx):
    # Time (0 to 2pi)
    progress = frame_idx / TOTAL_FRAMES
    t = progress * 2 * np.pi
    
    # 1. Canvas
    fig = plt.figure(figsize=(16, 9), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.set_facecolor(BG_COLOR)
    
    # 2. Calculate Chain
    # Start at center of screen
    cx, cy = 0.0, 0.0
    
    # Store joints for drawing the "Arm"
    joints = [(cx, cy)]
    
    for i, n_freq in enumerate(HARMONICS):
        radius = SCALES[i]
        angle = n_freq * t # (plus phase? square usually starts at pi/4 or 0)
        # Shift phase to make it flat-topped
        # For alternating harmonics generated square, start phase helps orientation
        # Let's just compute:
        
        dx = radius * np.cos(angle)
        dy = radius * np.sin(angle)
        
        # New Center
        nx = cx + dx
        ny = cy + dy
        
        # Draw the "Gear" (The potential path of this arm)
        gear = Circle((cx, cy), radius, fill=False, edgecolor=GEAR_COLOR, linewidth=2)
        ax.add_patch(gear)
        
        # Draw the "Arm" (The vector)
        # Alternate colors for visual separation
        c = ARM_1_COLOR if i % 2 == 0 else ARM_2_COLOR
        # Thicker arms for main, thinner for details
        lw = 8 - i
        ax.plot([cx, nx], [cy, ny], color=c, linewidth=lw, solid_capstyle='round')
        
        # Add a "Joint" dot
        ax.plot([cx], [cy], 'o', color=c, ms=lw*1.5)
        
        # Update cursor
        cx, cy = nx, ny
        joints.append((cx, cy))

    # 3. Draw The TIP (The Pen)
    ax.plot([cx], [cy], 'o', color=TRACE_COLOR, ms=10, zorder=10)
    
    # 4. Draw The TRACE (History)
    # We need to compute the full path analytically to draw the "trail"
    # Otherwise we just keep a buffer. 
    # For perfect "Closed Loop" visuals, let's compute the whole shape 
    # and just unveil it? Or a fading tail?
    # Kids love seeing it "draw". Let's do a long fading tail.
    
    history_len = 200
    points = []
    
    for h in range(history_len):
        # Go backwards in time
        ht = t - (h * 0.05) # step size
        
        # Recompute pos
        hx, hy = 0.0, 0.0
        for i, n_freq in enumerate(HARMONICS):
            hrad = SCALES[i]
            hang = n_freq * ht
            hx += hrad * np.cos(hang)
            hy += hrad * np.sin(hang)
        points.append((hx, hy))
        
    # Plot Trail
    if len(points) > 1:
        pts = np.array(points).reshape(-1, 1, 2)
        segments = np.concatenate([pts[:-1], pts[1:]], axis=1)
        # Alpha fade
        alphas = np.linspace(1.0, 0.0, len(segments))
        lc = LineCollection(segments, colors=TRACE_COLOR, linewidths=6, alpha=alphas, capstyle='round')
        ax.add_collection(lc)

    # Scale
    limit = 2.5
    ax.set_xlim(-limit * (16/9), limit * (16/9))
    ax.set_ylim(-limit, limit)
    ax.set_aspect('equal')
    
    # Save
    out_dir = "logic_garden_fourier_frames"
    os.makedirs(out_dir, exist_ok=True)
    filename = os.path.join(out_dir, f"fourier_{frame_idx:04d}.png")
    plt.savefig(filename, facecolor=BG_COLOR)
    plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Calculating the Epicycles...")
    for i in range(TOTAL_FRAMES):
        render_fourier_frame(i)
        if i % 50 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
