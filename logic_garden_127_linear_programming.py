"""
SOVEREIGN CODE: logic_garden_127_linear_programming.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python High-Fidelity Simulator
SCENE: Logic Garden 127 (Linear Programming Graphical Method)
VERSION: 1.1 (Syntax Repaired)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle  # <-- FIXED IMPORT
import math
import os

# CONFIG
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_127_linear_programming"
os.makedirs(OUT_DIR, exist_ok=True)

# THE INDUSTRIAL PALETTE
C_VOID = '#050510'       # Deep Institutional Void
C_GRID = '#112233'       # Subdued Structural Grid
C_AXIS = '#335577'       # Math Coordinate Bounds
C_CONSTRAINT = '#00FFCC' # Cyan (The Bounding Walls)
C_FEASIBLE = '#006644'   # Deep Green/Cyan (The Safe Zone)
C_PRESSURE = '#FF003C'   # Red (Gradient/Direction of Optimization)
C_OBJECTIVE = '#FFD700'  # Gold (The Objective Function / Z-Line)
C_TEXT = '#FFFFFF'       # White (UI & Telemetry)

def draw_glow_line(ax, x_vals, y_vals, color, base_lw=2, zorder=2):
    """Protocol: NEON POP. Renders a line with optical bloom."""
    ax.plot(x_vals, y_vals, color=color, lw=base_lw, zorder=zorder)
    ax.plot(x_vals, y_vals, color=color, lw=base_lw*2, alpha=0.4, zorder=zorder-1)
    ax.plot(x_vals, y_vals, color=color, lw=base_lw*4, alpha=0.1, zorder=zorder-2)

def ease_out_quad(t):
    return t * (2 - t)

def run():
    print(f"LOGIC GARDEN 127: OPTIMIZATION LIMIT ({TOTAL_FRAMES} frames)")
    
    # THE MATH CONSTRUCT
    # Max Z = 30x + 20y
    # ST:
    # C1: 2x + y <= 100
    # C2: x + y <= 80
    # C3: x <= 40
    # x, y >= 0
    
    # Vertices of the Feasible Polygon
    feasible_pts = np.array([
        [0, 0],
        [40, 0],
        [40, 20],   # Intersection of x=40 and 2x+y=100 -> y=20
        [20, 60],   # Intersection of 2x+y=100 and x+y=80 -> x=20, y=60
        [0, 80]     # Intersection of x+y=80 and x=0 -> y=80
    ])
    
    # Objective Function Gradient
    grad_x, grad_y = 30, 20
    grad_mag = math.hypot(grad_x, grad_y)
    u_x, u_y = grad_x / grad_mag, grad_y / grad_mag # Unit vector directions
    
    # Timeline
    F_GRID = 30
    F_C1 = 60
    F_C2 = 90
    F_C3 = 120
    F_REGION = 160
    F_SWEEP_START = 220
    F_SWEEP_END = 480
    
    for f in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        # Using specific axes to ensure square coordinate system (1:1 ratio)
        ax = plt.Axes(fig, [0.05, 0.2, 0.9, 0.6]) # [left, bottom, width, height]
        ax.set_axis_off()
        fig.add_axes(ax)
        
        fig.patch.set_facecolor(C_VOID)
        ax.set_facecolor(C_VOID)
        
        # Lock standard coordinate space for the math [0, 100] scale
        ax.set_xlim(-10, 110)
        ax.set_ylim(-10, 150)
        ax.set_aspect('equal', adjustable='box')
        
        # --- 1. RENDER GRID & AXES ---
        p_grid = min(1.0, f / F_GRID) if f > 0 else 0
        if p_grid > 0:
            for i in range(0, 120, 10):
                ax.axvline(i, color=C_GRID, lw=1, alpha=p_grid*0.5)
                ax.axhline(i, color=C_GRID, lw=1, alpha=p_grid*0.5)
            # Axes
            draw_glow_line(ax, [0, 110], [0, 0], C_AXIS, base_lw=3*p_grid, zorder=1)
            draw_glow_line(ax, [0, 0], [0, 150], C_AXIS, base_lw=3*p_grid, zorder=1)

        # --- 2. RENDER CONSTRAINTS ---
        if f >= F_C1:
            p = min(1.0, (f - F_C1) / 30.0)
            x_line = np.array([0, 50 * p])
            y_line = -2 * x_line + 100
            draw_glow_line(ax, x_line, y_line, C_CONSTRAINT, base_lw=4)
        
        if f >= F_C2:
            p = min(1.0, (f - F_C2) / 30.0)
            x_line = np.array([0, 80 * p])
            y_line = -x_line + 80
            draw_glow_line(ax, x_line, y_line, C_CONSTRAINT, base_lw=4)

        if f >= F_C3:
            p = min(1.0, (f - F_C3) / 30.0)
            y_line = np.array([0, 120 * p])
            x_line = np.array([40, 40])
            draw_glow_line(ax, x_line, y_line, C_CONSTRAINT, base_lw=4)

        # --- 3. RENDER FEASIBLE REGION ---
        if f >= F_REGION:
            p = min(1.0, (f - F_REGION) / 40.0)
            poly = Polygon(feasible_pts, closed=True, color=C_FEASIBLE, alpha=p * 0.4, zorder=0)
            ax.add_patch(poly)
            # Outer boundary glow
            draw_glow_line(ax, np.append(feasible_pts[:,0], feasible_pts[0,0]), 
                           np.append(feasible_pts[:,1], feasible_pts[0,1]), 
                           C_FEASIBLE, base_lw=2*p, zorder=1)

        # --- 4. RENDER OBJECTIVE FUNCTION (OPTIMIZATION PRESSURE) ---
        Z_val = 0
        status = "ESTABLISHING BOUNDING BOX (CONSTRAINTS)"
        
        if f >= F_SWEEP_START:
            status = "APPLYING OPTIMIZATION PRESSURE"
            t = (f - F_SWEEP_START) / (F_SWEEP_END - F_SWEEP_START)
            if t > 1.0: t = 1.0
            
            # Ease the sweep
            eased_t = ease_out_quad(t)
            
            # Max Z is at (20, 60): Z = 30(20) + 20(60) = 600 + 1200 = 1800
            Z_val = eased_t * 1800
            
            x_obj = np.array([-50, 150])
            y_obj = -1.5 * x_obj + (Z_val / 20)
            
            draw_glow_line(ax, x_obj, y_obj, C_OBJECTIVE, base_lw=5, zorder=5)
            
            # The Normal Vector (Gradient)
            mid_x = min(max(Z_val / 60, 0), 100)
            mid_y = -1.5 * mid_x + (Z_val / 20)
            
            arrow_len = 15
            ax.arrow(mid_x, mid_y, u_x * arrow_len, u_y * arrow_len, 
                     head_width=4, head_length=5, fc=C_PRESSURE, ec=C_PRESSURE, lw=3, zorder=6)

            if t >= 1.0:
                status = "HARD LIMIT REACHED [PARETO OPTIMAL]"
                pulse = math.sin((f - F_SWEEP_END) * 0.4) * 3
                ax.add_patch(Circle((20, 60), 4 + max(0, pulse), color=C_TEXT, zorder=7))
                ax.add_patch(Circle((20, 60), 8 + max(0, pulse*2), color=C_OBJECTIVE, alpha=0.5, zorder=6))

        # --- 5. UI AND TELEMETRY (HUD) ---
        fig.text(0.5, 0.92, "LOGIC GARDEN 127", color=C_TEXT, ha='center', 
                 fontsize=35, fontname='monospace', weight='bold')
        fig.text(0.5, 0.89, "THE BOUNDING BOX (LINEAR PROGRAMMING)", color=C_CONSTRAINT, ha='center', 
                 fontsize=20, fontname='monospace')

        hud_y = 0.15
        fig.text(0.1, hud_y, "OBJECTIVE:", color=C_GRID, fontsize=18, fontname='monospace')
        fig.text(0.1, hud_y - 0.02, "Max Z = 30x + 20y", color=C_OBJECTIVE, fontsize=24, fontname='monospace', weight='bold')
        
        fig.text(0.1, hud_y - 0.06, "CONSTRAINTS:", color=C_GRID, fontsize=18, fontname='monospace')
        fig.text(0.1, hud_y - 0.08, "1. 2x + y <= 100 [Capacity]", color=C_CONSTRAINT if f > F_C1 else C_VOID, fontsize=20, fontname='monospace')
        fig.text(0.1, hud_y - 0.10, "2. x + y  <= 80  [Time]", color=C_CONSTRAINT if f > F_C2 else C_VOID, fontsize=20, fontname='monospace')
        fig.text(0.1, hud_y - 0.12, "3. x      <= 40  [Limits]", color=C_CONSTRAINT if f > F_C3 else C_VOID, fontsize=20, fontname='monospace')

        fig.text(0.65, hud_y - 0.02, f"Z = {Z_val:08.2f}", color=C_TEXT, fontsize=28, fontname='monospace', weight='bold')
        
        fig.text(0.5, 0.02, f">> {status} <<", color=C_PRESSURE if "OPTIMAL" in status else C_FEASIBLE, 
                 ha='center', fontsize=22, fontname='monospace', weight='bold')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close(fig)

if __name__ == "__main__": run()
