"""
SOVEREIGN CODE: logic_garden_100_pareto_v2.py
FORMAT: YouTube Shorts (1080x1920)
SCENE: The Pareto Frontier (Syntax Patched)
SYSTEM: Pure Python
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.patheffects as pe
import os
import random
import math

# CONFIG
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_100_pareto_v2"
os.makedirs(OUT_DIR, exist_ok=True)

# RESOLUTION
RES_W = 1080
RES_H = 1920
ASPECT = RES_H / RES_W

# PALETTE (Industrialist High-Contrast)
C_BG      = '#050510'     # Void
C_GRID    = '#111122'     # Logic Matrix
C_POINT_A = '#333344'     # Sub-optimal (Ghost)
C_POINT_B = '#FFD700'     # Optimal (Gold)
C_LINE    = '#00FFFF'     # The Frontier (Cyan Line)
C_CYAN    = '#00FFFF'     # The Fill Color (Missing var fixed)
C_SCAN    = '#FF0055'     # The Constraint

class Solution:
    def __init__(self, uid):
        self.id = uid
        # Start clustered in "Bad" quadrant
        self.pos = np.array([random.uniform(0, 20), random.uniform(0, 20)])
        self.vel = np.array([random.uniform(0.5, 2.0), random.uniform(0.5, 2.0)])
        self.is_optimal = False
        self.stuck = False
        
    def update(self, dt):
        if self.stuck: return
        self.pos += self.vel * dt

def get_pareto_frontier(points):
    """
    Returns indices of points that are on the Pareto Frontier.
    """
    # Create list of (x, y, index)
    param_list = [(p.pos[0], p.pos[1], i) for i, p in enumerate(points)]
    # Sort by X descending (Right to Left sweep)
    # If a point has higher X, it *might* be optimal.
    # As we sweep left, keep track of the highest Y seen so far.
    # If current Y > max_y, it's a frontier point.
    param_list.sort(key=lambda x: x[0], reverse=True)
    
    pareto_indices = []
    current_max_y = -1.0
    
    for x, y, idx in param_list:
        if y > current_max_y:
            pareto_indices.append(idx)
            current_max_y = y
            
    return pareto_indices

def run():
    print(f"LOGIC GARDEN 100: PARETO FRONTIER V2 ({TOTAL_FRAMES} frames)")
    
    # 1. SETUP
    solutions = [Solution(i) for i in range(80)]
    RADIUS = 90.0
    
    for f in range(TOTAL_FRAMES):
        
        # --- PHYSICS ---
        for s in solutions:
            s.update(0.3)
            
            # Constraint Wall
            dist = np.linalg.norm(s.pos)
            # Add noise to wall for "Ragged" look (Anti-Smoothing)
            local_r = RADIUS + (math.sin(s.id * 132.0) * 5.0) 
            
            if dist >= local_r:
                s.pos = (s.pos / dist) * local_r
                s.stuck = True
        
        # --- LOGIC ---
        for s in solutions: s.is_optimal = False
        
        p_indices = get_pareto_frontier(solutions)
        for idx in p_indices:
            solutions[idx].is_optimal = True
            
        # --- RENDER ---
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        ax.set_xlim(0, 110)
        ax.set_ylim(0, 120)
        ax.set_facecolor(C_BG)
        
        # 1. GRID
        for i in range(0, 120, 10):
            w = 2 if i % 50 == 0 else 1
            ax.axvline(i, color=C_GRID, linewidth=w)
            ax.axhline(i, color=C_GRID, linewidth=w)
            
        # 2. FRONTIER LINE
        optimal_pts = [s for s in solutions if s.is_optimal]
        # Sort by X ascending for plotting line left-to-right
        optimal_pts.sort(key=lambda s: s.pos[0])
        
        if len(optimal_pts) > 1:
            px = [p.pos[0] for p in optimal_pts]
            py = [p.pos[1] for p in optimal_pts]
            
            # Step Plot: The definition of discrete dominance
            # 'post' means the vertical line comes after the point
            ax.step(px, py, where='post', color=C_LINE, linewidth=5, alpha=0.9, zorder=5)
            
            # GLOW FILL
            # Fill between requires x and y to be same length mostly, using step logic internal
            ax.fill_between(px, py, step='post', color=C_CYAN, alpha=0.15, zorder=2)

        # 3. PARTICLES
        for s in solutions:
            if s.is_optimal:
                # OPTIMAL (Gold)
                ax.scatter(s.pos[0], s.pos[1], s=200, c=C_POINT_B, zorder=10, 
                           edgecolors='white', linewidths=2)
            else:
                # DOMINATED (Grey)
                ax.scatter(s.pos[0], s.pos[1], s=50, c=C_POINT_A, zorder=1, alpha=0.5)

        # 4. UI
        stroke = [pe.withStroke(linewidth=4, foreground="black")]
        
        # Labels
        if f > 20:
            ax.text(5, 115, "METRIC: PRECISION (Y)", color='white', fontsize=20, fontname='monospace', weight='bold', path_effects=stroke)
            ax.text(60, 5, "METRIC: VELOCITY (X) ->", color='white', fontsize=20, fontname='monospace', weight='bold', path_effects=stroke)
        
        # Text Reveal
        if f > 80:
             # Diagonal Text aligned with pressure
             ax.text(55, 60, "OPTIMIZATION\nPRESSURE", color='white', alpha=0.15, 
                    ha='center', va='center', fontsize=50, fontname='monospace', rotation=45, weight='bold')

        if f > 140:
            ax.text(55, 100, "THE PARETO FRONTIER", color=C_POINT_B, ha='center', 
                    fontsize=40, fontname='monospace', weight='bold', path_effects=stroke)
            
        if f > 180:
            ax.text(55, 94, "YOU CANNOT HAVE IT ALL", color=C_CYAN, ha='center', 
                    fontsize=25, fontname='monospace', weight='bold', path_effects=stroke)

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
