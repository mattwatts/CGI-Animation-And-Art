"""
SOVEREIGN CODE: logic_garden_105_seed_v2.py
FORMAT: YouTube Shorts (1080x1920)
SCENE: The Seed (Syntax Patched)
SYSTEM: Pure Python
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
import matplotlib.collections as mc
import matplotlib.patheffects as pe
import os
import math
import random

# CONFIG
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_105_seed_v2"
os.makedirs(OUT_DIR, exist_ok=True)

# RESOLUTION
RES_W = 1080
RES_H = 1920

# PALETTE
C_BG    = '#050510'
C_SEED  = '#00FFFF'     # The Generator (Cyan)
C_CHILD = '#0088AA'     # The Output (Darker Cyan)
C_GOLD  = '#FFD700'     # The Legacy
C_CODE  = '#FFFFFF'

def get_triangle_vertices(cx, cy, radius, angle_offset=0):
    """ Return 3 points of an equilateral triangle """
    points = []
    for i in range(3):
        angle = angle_offset + (i * (2 * math.pi / 3)) + (math.pi/2)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append([x, y])
    return np.array(points)

def get_sierpinski_triangles(vertices, depth):
    """ 
    Recursive generator of triangles.
    Returns list of (vertices, depth_level)
    """
    if depth == 0:
        return [(vertices, 0)]
    
    # Vertices
    p0 = vertices[0]
    p1 = vertices[1]
    p2 = vertices[2]
    
    m01 = (p0 + p1) / 2
    m12 = (p1 + p2) / 2
    m20 = (p2 + p0) / 2
    
    # 3 Sub-triangles
    t1 = np.array([p0, m01, m20])
    t2 = np.array([m01, p1, m12])
    t3 = np.array([m20, m12, p2])
    
    # Recurse
    results = []
    results.extend(get_sierpinski_triangles(t1, depth - 1))
    results.extend(get_sierpinski_triangles(t2, depth - 1))
    results.extend(get_sierpinski_triangles(t3, depth - 1))
    
    return results

def run():
    print(f"LOGIC GARDEN 105: THE SEED V2 ({TOTAL_FRAMES} frames)")
    
    # Base Triangle
    base_radius = 800
    base_verts = get_triangle_vertices(0, -100, base_radius)
    
    for f in range(TOTAL_FRAMES):
        
        # --- TIMELINE ---
        current_depth_float = 0.0
        
        if f > 60:
            val = (f - 60) / 300.0 # Slow ramp
            current_depth_float = val * 6.0 
            
        if current_depth_float > 6: current_depth_float = 6.0
        
        display_depth = int(current_depth_float)
        
        # --- GENERATE GEOMETRY ---
        triangles = get_sierpinski_triangles(base_verts, display_depth)
        
        # --- RENDER ---
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        ax.set_xlim(-540, 540)
        ax.set_ylim(-960, 960)
        ax.set_facecolor(C_BG)
        
        # 1. DRAW THE "GHOST" SEED (Outline)
        seed_poly = Polygon(base_verts, closed=True, fill=False, edgecolor=C_SEED, linewidth=4, alpha=0.5, zorder=5)
        ax.add_patch(seed_poly)
        
        # 2. DRAW THE RECURSION (Leaves)
        # Extract vertices list for PolyCollection
        verts_list = [t[0] for t in triangles]
        
        p_col = mc.PolyCollection(verts_list, edgecolors=C_CHILD, facecolors=(0,0,0,0), linewidths=2)
        if display_depth > 3:
            p_col.set_linewidth(1) 
        ax.add_collection(p_col)

        # 3. THE "GENERATOR" TEXT (Center of the Void)
        # Calculate center of the central hole (m01, m12, m20)
        m01 = (base_verts[0] + base_verts[1]) / 2
        m12 = (base_verts[1] + base_verts[2]) / 2
        m20 = (base_verts[2] + base_verts[0]) / 2
        
        # Center of that inner triangle
        void_center = (m01 + m12 + m20) / 3
        
        stroke = [pe.withStroke(linewidth=4, foreground="black")]
        
        ax.text(void_center[0], void_center[1] + 50, "def legacy(self):", 
                color=C_CODE, ha='center', fontsize=30, fontname='monospace', path_effects=stroke)
        
        # Fixed typo: C_CHILD instead of C_CHLID
        cursor_col = C_CHILD if f % 20 < 10 else C_SEED
        ax.text(void_center[0], void_center[1] - 50, "  return self.copy()", 
                color=cursor_col, ha='center', fontsize=25, fontname='monospace', path_effects=stroke)


        # 4. GLOWING NODES
        if f % 2 == 0:
            all_x = []
            all_y = []
            for t in verts_list:
                all_x.extend([v[0] for v in t])
                all_y.extend([v[1] for v in t])
            
            # Subsample
            if len(all_x) > 500:
                idx = random.sample(range(len(all_x)), 500)
                draw_x = [all_x[i] for i in idx]
                draw_y = [all_y[i] for i in idx]
            else:
                draw_x = all_x
                draw_y = all_y
            
            if len(draw_x) > 0:
                ax.scatter(draw_x, draw_y, s=10, c=C_SEED, alpha=0.6, zorder=2)


        # 5. UI
        if f < 90:
            ax.text(0, 800, "THE SEED", color=C_SEED, ha='center', fontsize=40, fontname='monospace', weight='bold', path_effects=stroke)
            ax.text(0, 750, "(Generator Function)", color=C_SEED, ha='center', fontsize=25, fontname='monospace', path_effects=stroke)
            
        elif f > 90 and f < 450:
            n_polys = len(triangles)
            ax.text(0, 800, f"RECURSION DEPTH: {display_depth}", color=C_GOLD, ha='center', fontsize=30, fontname='monospace', weight='bold', path_effects=stroke)
            ax.text(0, 750, f"NODES: {n_polys}", color=C_GOLD, ha='center', fontsize=25, fontname='monospace', path_effects=stroke)

        elif f >= 450:
            ax.text(0, 800, "INFINITE OUTPUT", color=C_GOLD, ha='center', fontsize=40, fontname='monospace', weight='bold', path_effects=stroke)
            ax.text(0, -600, "LEAVE THE CODE", color=C_CODE, ha='center', fontsize=35, fontname='monospace', weight='bold', path_effects=stroke)
            ax.text(0, -660, "NOT THE DATA", color=C_CODE, ha='center', fontsize=25, fontname='monospace', path_effects=stroke)

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
