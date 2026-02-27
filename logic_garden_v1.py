"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v1.py
MODE:   Nursery (Early Childhood Education Palette)
TARGET: Double Pendulum (Chaos Theory for Toddlers)
STYLE:  "Bauhaus Toy" | High Contrast | Soft Physics

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
BG_COLOR = "#FFFFFF"        # Pure White Paper
BOB_1_COLOR = "#FFD700"     # Cyber Yellow (Sun)
BOB_2_COLOR = "#FF4500"     # Safety Red (Balloon)
LINK_COLOR = "#0080FF"      # Azure Blue (Structure)
TRACE_COLOR = "#00EEFF"     # Electric Cyan (Memory)

# --- 2. PHYSICS ENGINE (The Chaos) ---
# Standard Hamiltonian Mechanics for Double Pendulum
def get_derivs(state, t):
    theta1, z1, theta2, z2 = state
    c, s = np.cos(theta1-theta2), np.sin(theta1-theta2)
    
    num1 = M2 * L1 * z1**2 * s * c + M2 * G * np.sin(theta2) * c + \
           M2 * L2 * z2**2 * s - (M1 + M2) * G * np.sin(theta1)
    den1 = L1 * (M1 + M2 * s**2)
    
    num2 = -M2 * L2 * z2**2 * s * c + (M1 + M2) * (G * np.sin(theta1) * c - \
           L1 * z1**2 * s - G * np.sin(theta2))
    den2 = L2 * (M1 + M2 * s**2)
    
    return [z1, num1/den1, z2, num2/den2]

# Physics Constants
L1, L2 = 1.0, 1.0  # Lengths
M1, M2 = 1.0, 1.0  # Masses
G = 9.8            # Gravity
DT = 0.05
STEPS = 400

# --- 3. RENDERER ---
def render_toy_frame(state, trace_history, frame_id):
    theta1, z1, theta2, z2 = state
    
    # Calculate Positions
    x1 = L1 * np.sin(theta1)
    y1 = -L1 * np.cos(theta1)
    x2 = x1 + L2 * np.sin(theta2)
    y2 = y1 - L2 * np.cos(theta2)
    
    # Setup Canvas (Square for Instagram/Shorts?) 
    # Let's keep 16:9 for YouTube
    fig = plt.figure(figsize=(16, 9), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    # Set Background
    ax.set_facecolor(BG_COLOR)
    
    # 1. Draw The "Memory" (Trace)
    # A soft, thick crayon line
    trace_x = [t[0] for t in trace_history]
    trace_y = [t[1] for t in trace_history]
    if len(trace_x) > 1:
        points = np.array([trace_x, trace_y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        
        # Fade out the tail
        alphas = np.linspace(0.1, 1.0, len(segments))
        lc = LineCollection(segments, colors=TRACE_COLOR, linewidths=8, alpha=alphas, joinstyle='round', capstyle='round')
        ax.add_collection(lc)

    # 2. Draw The "Arms" (Structure)
    # Thick, friendly lines
    ax.plot([0, x1], [0, y1], color=LINK_COLOR, linewidth=12, solid_capstyle='round')
    ax.plot([x1, x2], [y1, y2], color=LINK_COLOR, linewidth=12, solid_capstyle='round')
    
    # 3. Draw The "Bobs" (Agents)
    # Big, perfectly round circles
    circle1 = Circle((x1, y1), 0.15, color=BOB_1_COLOR, zorder=10)
    circle2 = Circle((x2, y2), 0.15, color=BOB_2_COLOR, zorder=10)
    ax.add_patch(circle1)
    ax.add_patch(circle2)
    
    # 4. Draw the "Pivot" (Anchor)
    pivot = Circle((0, 0), 0.08, color="#333333", zorder=11)
    ax.add_patch(pivot)

    # Scaling
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)
    ax.set_aspect('equal')

    # Save
    out_dir = "logic_garden_frames"
    os.makedirs(out_dir, exist_ok=True)
    filename = os.path.join(out_dir, f"toy_{frame_id:04d}.png")
    plt.savefig(filename, facecolor=BG_COLOR)
    plt.close()

# --- 4. EXECUTION LOOP ---
if __name__ == "__main__":
    from scipy.integrate import odeint
    
    # Initial State (High Energy!)
    state = [np.pi/2, 0, np.pi/2, 0] # Horizontal start
    t = np.linspace(0, 20, STEPS)
    
    # Solve ODE
    print("[NURSERY] Calculating Physics...")
    states = odeint(get_derivs, state, t)
    
    trace_history = []
    
    print("[RENDER] Painting the Logic Garden...")
    for i in range(STEPS):
        curr_state = states[i]
        
        # Update trace for the tip (x2, y2)
        theta1, _, theta2, _ = curr_state
        x1 = L1 * np.sin(theta1)
        y1 = -L1 * np.cos(theta1)
        x2 = x1 + L2 * np.sin(theta2)
        y2 = y1 - L2 * np.cos(theta2)
        
        trace_history.append((x2, y2))
        if len(trace_history) > 50: # Limit memory length
            trace_history.pop(0)
            
        render_toy_frame(curr_state, trace_history, i)
        print(f"Frame {i}/{STEPS}")

