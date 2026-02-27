"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v28.py
MODE:   Nursery (Stealth Palette)
TARGET: F-35B STOVL Cycle (Vector Equilibrium)
STYLE:  "The Iron Dancer" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Wedge, Arrow
import os

# --- 1. THE STEALTH PALETTE ---
BG_COLOR = "#001020"        # High Altitude Navy
BODY_COLOR = "#505050"      # Radar Absorbent Grey
NOZZLE_COLOR = "#303030"    # Heat Shield
FAN_AIR = "#00FFFF"         # Cold Air (Lift Fan)
JET_AIR = "#FF4500"         # Hot Exhaust (Main Engine)
VECTOR_ARROW = "#FFD700"    # Physics Truth

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION

class STOVL_Sim:
    def __init__(self):
        # 0.0 = Cruise (Doors closed, Nozzle Back)
        # 1.0 = Hover (Doors open, Nozzle Down)
        self.mode = 0.0 
        self.fan_spin = 0.0

    def get_geometry(self, progress):
        # Maps progress (0->1) to articulation angles
        
        # 1. Door Angle (Opens quickly 0->0.3)
        door_angle = min(progress * 3.0, 1.0) * 80 # Max 80 degrees
        
        # 2. Nozzle Angle (Starts after doors, 0.2->1.0)
        nozzle_curve = max(0, min((progress - 0.2) * 1.25, 1.0))
        # 3 Segments act together to bend 90 deg
        # Simplified: The tail curls down
        # Segment 1: Fixed
        # Segment 2: Rotates 45 * nozzle_curve
        # Segment 3: Rotates 90 * nozzle_curve total
        
        return door_angle, nozzle_curve

    def render(self, frame_idx, ax):
        # Animation Logic
        # 0-5s: Cruise
        # 5-10s: Transition
        # 10-15s: Hover
        # 15-20s: Return
        
        t = frame_idx / FPS
        if t < 2:
            self.mode = 0.0
        elif t < 8:
            self.mode = (t - 2) / 6.0 # Slow transition
        elif t < 14:
            self.mode = 1.0
        else:
            self.mode = 1.0 - ((t - 14) / 4.0)

        # Clamp
        self.mode = max(0.0, min(1.0, self.mode))
        
        door_ang, nozzle_p = self.get_geometry(self.mode)
        
        # --- DRAW FUSELAGE (Static Reference) ---
        # Nose to Tail approx coords
        fuse_pts = [
            [-6, -0.5], # Nose
            [-2, 1.0],  # Canopy start
            [0, 1.2],   # Spine
            [2, 1.2],   # Lift Fan Hump
            [5, 1.0],   # Engine Housing
            [6, 0.5],   # Top Tail
            [5, -0.5],  # Bottom Tail
            [-2, -0.8], # Intake Bottom
            [-6, -0.5]  # Back to Nose
        ]
        ax.add_patch(Polygon(fuse_pts, facecolor=BODY_COLOR, edgecolor="black"))
        
        # Cockpit Glass
        ax.add_patch(Polygon([[-2, 1.0], [-1, 1.3], [0.5, 1.2], [-2, 1.0]], color="#111111"))

        # --- DRAW LIFT FAN (Front) ---
        # Located at x=2.5 roughly
        fan_x = 2.5
        fan_y = 1.2
        
        # Top Door (Opens Aft)
        # Pivot at back of door (x=3.5)
        door_len = 1.8
        door_pivot = [3.4, 1.2]
        
        # Rotate door
        rad_d = np.radians(door_ang)
        dx = -np.cos(rad_d) * door_len
        dy = np.sin(rad_d) * door_len
        
        # Top Door
        ax.plot([door_pivot[0], door_pivot[0]+dx], [door_pivot[1], door_pivot[1]+dy], 
                color=BODY_COLOR, linewidth=4)
        
        # The Fan Mechanism (Visible if door open)
        if self.mode > 0.05:
            # Spinner
            self.fan_spin += 0.5 * self.mode
            ax.add_patch(Rectangle((1.8, 0.5), 1.5, 0.7, color="#222222")) # Fan Shaft
            
            # Thrust Vector (Cold Air) - Downward
            # Grows with mode
            thrust_len = 4.0 * self.mode
            
            # Alpha based on power
            a = 0.3 + (0.3 * np.random.rand())
            
            # Draw Flow
            flow_poly = [
                [1.8, 0.5], [3.3, 0.5], # Top
                [3.5 + np.random.rand(), 0.5 - thrust_len], # Bottom Right
                [1.6 - np.random.rand(), 0.5 - thrust_len]  # Bottom Left
            ]
            ax.add_patch(Polygon(flow_poly, color=FAN_AIR, alpha=0.5))
            
            # Physical Arrow
            ax.arrow(2.55, 0.0, 0, -2.5*self.mode, head_width=0.5, head_length=0.5, fc=VECTOR_ARROW, ec="black", zorder=10)


        # --- DRAW MAIN ENGINE (The 3BSM) ---
        # The trick: 3 segments that curve. 
        # Pivot point at x=5, y=0.0
        
        # Parameters
        seg_len = 0.8
        bend_total = 95 * nozzle_p # Degrees (slightly more than 90 for STOVL braking)
        
        # Segment 1 (Base) - Fixed to body
        s1_pts = [[5, 0.5], [5.8, 0.5], [5.8, -0.5], [5, -0.5]]
        ax.add_patch(Polygon(s1_pts, facecolor=NOZZLE_COLOR, edgecolor="black"))
        
        # Segment 2 - Rotates some
        ang2 = np.radians( -bend_total * 0.5 ) # Half the bend
        p2_pivot = [5.8, 0] # Center of joint
        
        def rotate_pts(pts, pivot, angle):
            res = []
            c, s = np.cos(angle), np.sin(angle)
            for p in pts:
                px, py = p[0]-pivot[0], p[1]-pivot[1]
                nx = px*c - py*s
                ny = px*s + py*c
                res.append([nx+pivot[0], ny+pivot[1]])
            return res
            
        s2_template = [[5.8, 0.45], [6.6, 0.45], [6.6, -0.45], [5.8, -0.45]]
        s2_pts = rotate_pts(s2_template, p2_pivot, ang2)
        ax.add_patch(Polygon(s2_pts, facecolor=NOZZLE_COLOR, edgecolor="black"))
        
        # Segment 3 (The exit) - Rotates more
        ang3 = np.radians( -bend_total ) # Full bend
        # Pivot is end of S2... tricky calc in loop.
        # Analytic approx for visual: 
        # Just pivot S3 relative to S2's end.
        
        # Find end of S2 (middle of right edge)
        # Template end was (6.6, 0)
        p3_pivot_local = [6.6 - 5.8, 0] # 0.8, 0
        # Rotate this vector by ang2
        v2x = 0.8 * np.cos(ang2)
        v2y = 0.8 * np.sin(ang2)
        p3_pivot = [5.8 + v2x, 0 + v2y]
        
        s3_template = [[p3_pivot[0], p3_pivot[1]+0.4], [p3_pivot[0]+0.8, p3_pivot[1]+0.4], 
                       [p3_pivot[0]+0.8, p3_pivot[1]-0.4], [p3_pivot[0], p3_pivot[1]-0.4]]
        
        # Rotate S3 relative to p3_pivot by (ang3 - ang2) ? 
        # No, simpler. S3 angle is absolute ang3
        s3_pts = rotate_pts(s3_template, p3_pivot, ang3 - ang2) # Relative to S2
        # Wait, the rotation function is absolute relative to pivot... 
        # Let's just rotate template S3 by total angle around p3_pivot? No.
        # Just manually construct the polygon at the end of S2 pointing in direction ang3
        
        exit_vec_x = np.cos(ang3)
        exit_vec_y = np.sin(ang3)
        perp_x = -exit_vec_y
        perp_y = exit_vec_x
        
        w = 0.4
        l = 0.8
        
        s3_final = [
            [p3_pivot[0] + perp_x*w, p3_pivot[1] + perp_y*w], # Top Left
            [p3_pivot[0] + exit_vec_x*l + perp_x*w, p3_pivot[1] + exit_vec_y*l + perp_y*w], # Top Right
            [p3_pivot[0] + exit_vec_x*l - perp_x*w, p3_pivot[1] + exit_vec_y*l - perp_y*w], # Bot Right
            [p3_pivot[0] - perp_x*w, p3_pivot[1] - perp_y*w]  # Bot Left
        ]
        
        ax.add_patch(Polygon(s3_final, facecolor="#202020", edgecolor="white")) # Hot tip
        
        # Exhaust Plume (Hot)
        # Starts at end of S3
        exit_center = [p3_pivot[0] + exit_vec_x*l, p3_pivot[1] + exit_vec_y*l]
        
        curr_power = 0.2 + (0.8 * self.mode)
        plume_len = 5.0 * curr_power
        
        # Main Plume
        plume_poly = [
            [exit_center[0] + perp_x*0.3, exit_center[1] + perp_y*0.3],
            [exit_center[0] + exit_vec_x*plume_len, exit_center[1] + exit_vec_y*plume_len],
            [exit_center[0] - perp_x*0.3, exit_center[1] - perp_y*0.3]
        ]
        ax.add_patch(Polygon(plume_poly, color=JET_AIR, alpha=0.6))
        
        # Vector Arrow (Engine)
        # Originates at S3
        if self.mode > 0.1:
             ax.arrow(exit_center[0], exit_center[1], exit_vec_x*2.5*self.mode, exit_vec_y*2.5*self.mode, 
                      head_width=0.5, head_length=0.5, fc=VECTOR_ARROW, ec="black", zorder=10)


        # Ground
        ax.axhline(-4, color="#333333", linewidth=5)

        # Scale
        ax.set_xlim(-8, 10)
        ax.set_ylim(-6, 4)
        ax.set_aspect('equal')
        ax.set_axis_off()
        
        # Text
        status = "MODE: CRUISE"
        if self.mode > 0.1 and self.mode < 0.9: status = "MODE: TRANSITION"
        if self.mode >= 0.9: status = "MODE: STOVL HOVER"
        
        ax.text(0, -5, status, color="white", ha='center', fontsize=20, fontfamily='monospace')

        # Save
        out_dir = "logic_garden_f35_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"f35_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Breaking the Spine...")
    
    sim = STOVL_Sim()
    
    for i in range(TOTAL_FRAMES):
        # Canvas
        fig = plt.figure(figsize=(16, 9), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        sim.render(i, ax)
        
        plt.close() # Memory hygiene
        
        if i % 30 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
