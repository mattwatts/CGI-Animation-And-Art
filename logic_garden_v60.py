"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v60.py
MODE:   Nursery (Hyper-Dimensional Palette)
TARGET: Tesseract (4D Projection)
STYLE:  "The Shadow Cast" | 40s Deep Time | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import LineCollection
import os

# --- 1. THE HYPER PALETTE ---
BG_VOID = "#050505"
OUTER_BLUE = "#4169E1"      # Royal Blue
INNER_CYAN = "#00FFFF"      # Electric Cyan
CONN_MAGENTA = "#FF00FF"    # The 4th Dimension connectivity
VERTEX_GLOW = "#FFFFFF"

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 40
TOTAL_FRAMES = FPS * DURATION

class TesseractSim:
    def __init__(self):
        # 1. Define Vertices of a 4D Hypercube
        # 16 Vertices: (+-1, +-1, +-1, +-1)
        self.vertices_4d = []
        for x in [-1, 1]:
            for y in [-1, 1]:
                for z in [-1, 1]:
                    for w in [-1, 1]:
                        self.vertices_4d.append(np.array([x, y, z, w]))
        self.vertices_4d = np.array(self.vertices_4d) # Shape (16, 4)
        
        # 2. Define Edges (Connections)
        # Vertices connected if distance is 2 (change in only 1 dim)
        self.edges = []
        for i in range(16):
            for j in range(i+1, 16):
                dist = np.sum(np.abs(self.vertices_4d[i] - self.vertices_4d[j]))
                if np.isclose(dist, 2.0):
                    self.edges.append((i, j))
        
        # 3. Rotation State
        self.angle_xy = 0.0
        self.angle_zw = 0.0
        
    def rotate(self, pts, theta, plane='zw'):
        # 4D Rotation Logic
        c, s = np.cos(theta), np.sin(theta)
        
        rot_mat = np.eye(4)
        if plane == 'zw': # "Inside-Out" rotation
            rot_mat[2,2] = c; rot_mat[2,3] = -s
            rot_mat[3,2] = s; rot_mat[3,3] = c
        elif plane == 'xw':
            rot_mat[0,0] = c; rot_mat[0,3] = -s
            rot_mat[3,0] = s; rot_mat[3,3] = c
            
        return np.dot(pts, rot_mat.T)

    def project(self, pts_4d):
        # 4D -> 3D Stereographic / Perspective Projection
        # Factor = 1 / (distance - w)
        # This makes things "far away" in W smaller
        
        distance = 3.0 # Camera distance in 4th dimension
        
        pts_3d = []
        w_depths = [] # Store w for z-sorting or coloring
        
        for p in pts_4d:
            w = p[3]
            scale = 1.0 / (distance - w)
            
            x_3d = p[0] * scale
            y_3d = p[1] * scale
            z_3d = p[2] * scale
            
            pts_3d.append([x_3d, y_3d, z_3d])
            w_depths.append(w)
            
        return np.array(pts_3d), np.array(w_depths)

    def update(self, frame_idx):
        # We perform a double rotation to show complexity
        # Slow rotation in ZW (The "Inside Out" morph)
        self.angle_zw = frame_idx * 0.02
        # Slight rotation in XW to show depth
        self.angle_xw = frame_idx * 0.01

    def render(self, frame_idx, fig):
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor(BG_VOID)
        
        # Setup 3D limits
        lim = 1.0
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_zlim(-lim, lim)
        ax.set_axis_off()
        
        # 1. APPLY 4D ROTATIONS
        current_pts = self.vertices_4d.copy()
        current_pts = self.rotate(current_pts, self.angle_zw, 'zw')
        current_pts = self.rotate(current_pts, self.angle_xw, 'xw')
        
        # 2. PROJECT TO 3D
        pts_3d, w_depths = self.project(current_pts)
        
        # 3. DRAW EDGES
        # We color edges based on their 4D depth (w) or type
        for edge in self.edges:
            p1 = pts_3d[edge[0]]
            p2 = pts_3d[edge[1]]
            
            # Check W coords to determine color
            w1 = w_depths[edge[0]]
            w2 = w_depths[edge[1]]
            avg_w = (w1 + w2) / 2.0
            
            # Color Logic
            # "Inner" cube (positive w) -> Cyan
            # "Outer" cube (negative w) -> Blue
            # Connecting struts -> Magenta
            
            # But in perspective projection, W causes scaling.
            # Small things are "Inner" (W > 0, dist-w is small? No, dist-w is small means BIG scale)
            # Wait, 1/(2-1) = 1 (Big), 1/(2-(-1)) = 0.3 (Small).
            # So W=+1 is the BIG one (Close to camera), W=-1 is SMALL (Far).
            # The "Inside-Out" effect is them swapping.
            
            # Let's map color to the 4D coordinate avg_w
            # -1 (Far/Small) -> Blue
            # +1 (Close/Large) -> Cyan
            
            # Normalize w (-1.5 to 1.5 approx after rotation)
            norm_w = (avg_w + 1.0) / 2.0
            norm_w = np.clip(norm_w, 0, 1)
            
            # Interpolate
            if abs(w1 - w2) > 0.5:
                # This is a connection between inner and outer
                col = CONN_MAGENTA
                width = 1.0
            else:
                # This is a face edge
                # Blend Blue -> Cyan
                c_b = matplotlib.colors.to_rgb(OUTER_BLUE)
                c_c = matplotlib.colors.to_rgb(INNER_CYAN)
                col = (
                    c_b[0]*(1-norm_w) + c_c[0]*norm_w,
                    c_b[1]*(1-norm_w) + c_c[1]*norm_w,
                    c_b[2]*(1-norm_w) + c_c[2]*norm_w,
                    0.8 # Alpha
                )
                width = 2.0 if norm_w > 0.5 else 1.0
            
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color=col, linewidth=width)

        # 4. DRAW VERTICES (Light Nodes)
        # Size based on perspective (Z and W)
        # 3D Depth
        # z_vals = pts_3d[:, 2] # Already projected
        sizes = 20 * (w_depths + 2.0) # Scale by W depth
        
        ax.scatter(pts_3d[:,0], pts_3d[:,1], pts_3d[:,2], s=sizes, color=VERTEX_GLOW, alpha=1.0)
        
        # 5. CAMERA ROTATION (3D)
        # We also rotate the 3D camera to see the structure
        ax.view_init(elev=20, azim=frame_idx * 0.2)
        
        # 6. HUD
        fig.text(0.5, 0.92, "LOGIC GARDEN 60: THE SHADOW CAST", color="white", ha='center', fontsize=16, fontweight='bold', fontfamily='monospace')
        
        label = "PROJECTION: 4D -> 3D -> 2D"
        fig.text(0.5, 0.08, label, color=CONN_MAGENTA, ha='center', fontfamily='monospace', fontsize=12,
                  bbox=dict(facecolor='black', edgecolor=CONN_MAGENTA, pad=5, alpha=0.5))

        # Save
        out_dir = "logic_garden_tesseract_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"tesseract_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_VOID)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print(f"[NURSERY] Unfolding Dimensions...")
    
    sim = TesseractSim()
    
    for i in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10, 10), dpi=100)
        
        sim.update(i)
        sim.render(i, fig)
        
        if i % 60 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
