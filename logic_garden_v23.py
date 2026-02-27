"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v23.py
MODE:   Nursery (Bauhaus Palette)
TARGET: Orbital Mechanics (Hohmann Transfer / Earth to Mars)
STYLE:  "The Long Shot" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Arc
import os

# --- 1. THE NURSERY PALETTE ---
BG_COLOR = "#FFFFFF"        # Void
SUN_COLOR = "#FFD700"       # Cyber Yellow (Gravity Well)
EARTH_COLOR = "#0080FF"     # Azure Blue
MARS_COLOR = "#FF4500"      # Safety Red
ROCKET_COLOR = "#000000"    # Structure
ORBIT_TRACE = "#BBBBBB"     # The Rails
TRANSFER_TRACE = "#000000"  # The Bridge

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION

# Scale (AU)
R_EARTH = 1.0
R_MARS = 1.52

# Angular Velocities (Kepler: w ~ 1/r^1.5)
W_EARTH = 0.02
W_MARS = W_EARTH / (1.52 ** 1.5)

# Transfer Orbit (Semi-Major Axis)
# a_trans = (1.0 + 1.52) / 2 = 1.26
# Period T_trans = a_trans^1.5
# Travel Time = T_trans / 2
A_TRANS = (R_EARTH + R_MARS) / 2.0
T_TRANS_PERIOD = A_TRANS ** 1.5
TRAVEL_TIME_UNITS = T_TRANS_PERIOD / 2.0 # In relative animation units

class OrbitSim:
    def __init__(self):
        # Initial Angles
        # We need Mars to be at "Arrival Point" when Rocket arrives.
        # Rocket travels 180 degrees (Pi radians).
        # Time required: TRAVEL_TIME_UNITS
        # Mars travels: W_MARS * TRAVEL_TIME_UNITS
        # So Mars Start Angle = Pi - (W_MARS * TRAVEL_TIME)
        # But we need to define "Time" in frames.
        
        # Let's calibrate visually for the video loop.
        # Launch at Frame 60 (2 seconds in).
        # Arrive at Frame 540 (18 seconds in).
        self.launch_frame = 60
        self.arrival_frame = 540
        self.travel_frames = self.arrival_frame - self.launch_frame
        
        # Calculate speed scaling
        # Rocket must cover Pi radians in travel_frames
        self.rocket_angle_speed_avg = np.pi / self.travel_frames
        
        # Earth Speed (Visual reference)
        self.w_earth = np.radians(1.0) # 1 degree per frame roughly
        self.w_mars = self.w_earth / (1.52 ** 1.5)
        
        # Back-calculate start positions so arrival happens at Angle = 180 (Left of screen)
        # Arrival Angle = np.pi
        
        # Mars Position at Arrival = np.pi
        # Mars Start Pos = np.pi - (self.w_mars * self.arrival_frame)
        self.mars_angle = np.pi - (self.w_mars * self.arrival_frame)
        
        # Earth Launch Angle needs to be 0 (Right of screen)
        # Earth Start Pos = 0 - (self.w_earth * self.launch_frame)
        self.earth_angle = 0 - (self.w_earth * self.launch_frame)
        
        # Rocket State
        self.rocket_active = False
        self.rocket_r = R_EARTH
        self.rocket_theta = 0.0
        self.success = False

    def get_transfer_pos(self, progress):
        # Progress 0 -> 1
        # Ellipse Equation in Polar Coords relative to Focus (Sun)
        # r = a(1-e^2) / (1 + e cos(theta))
        # But for Hohmann, it's simpler. 
        # Focus is Sun. Perihelion is Earth Radius. Aphelion is Mars Radius.
        # theta goes 0 -> 180 (Pi)
        
        theta = progress * np.pi
        
        # Ellipse geometry
        ra = R_MARS
        rp = R_EARTH
        a = (ra + rp) / 2.0
        e = (ra - rp) / (ra + rp)
        
        # Polar equation (origin at focus)
        r = (a * (1 - e**2)) / (1 + e * np.cos(theta))
        
        # Note: In polar eq, theta=0 is usually Perihelion (closest).
        # So as theta goes 0->Pi, r goes 1.0 -> 1.52. Correct.
        
        return r, theta

    def update(self, frame_idx):
        # Update Planets
        self.earth_angle += self.w_earth
        self.mars_angle += self.w_mars
        
        # Launch Logic
        if frame_idx >= self.launch_frame and frame_idx <= self.arrival_frame:
            self.rocket_active = True
            # Progress 0.0 to 1.0
            p = (frame_idx - self.launch_frame) / self.travel_frames
            
            # Non-linear time? (Kepler's 2nd law: fast at start, slow at end)
            # Approximation: Map 'p' through a curve?
            # Let's keep it linear for "Nursery" clarity, or use simple sine ease?
            # Let's stick to linear theta for visual smoothness, even if physics is slightly off.
            # (True physics: d_theta/dt varies. Here we lock geometry).
            
            r, theta = self.get_transfer_pos(p)
            self.rocket_r = r
            self.rocket_theta = theta + self.earth_angle_at_launch # Offset by launch pos
            
        elif frame_idx < self.launch_frame:
            # Rocket stuck to Earth
            self.rocket_r = R_EARTH
            self.rocket_theta = self.earth_angle
            self.earth_angle_at_launch = self.earth_angle # Keep updating until launch
            
        elif frame_idx > self.arrival_frame:
            # Arrived! Stuck to Mars
            self.rocket_r = R_MARS
            self.rocket_theta = self.mars_angle
            self.success = True

    def render(self, frame_idx, ax):
        # 1. Draw Orbits (Tracks)
        earth_track = Circle((0,0), R_EARTH, color=ORBIT_TRACE, fill=False, linestyle="--", linewidth=1)
        mars_track = Circle((0,0), R_MARS, color=ORBIT_TRACE, fill=False, linestyle="--", linewidth=1)
        ax.add_patch(earth_track)
        ax.add_patch(mars_track)
        
        # 2. Draw Sun
        ax.add_patch(Circle((0,0), 0.3, color=SUN_COLOR, zorder=5))
        
        # 3. Draw Planets
        ex = R_EARTH * np.cos(self.earth_angle)
        ey = R_EARTH * np.sin(self.earth_angle)
        ax.add_patch(Circle((ex, ey), 0.08, color=EARTH_COLOR, zorder=10))
        
        mx = R_MARS * np.cos(self.mars_angle)
        my = R_MARS * np.sin(self.mars_angle)
        
        # If success, Mars turns Gold
        m_col = "Gold" if self.success else MARS_COLOR
        ax.add_patch(Circle((mx, my), 0.06, color=m_col, zorder=10))
        
        # 4. Draw Transfer Trajectory (The Ghost Path)
        if frame_idx >= self.launch_frame:
            # Draw the half-ellipse
            # We need to compute the points relative to the launch angle
            # Rotation of the ellipse is aligned with launch angle
            
            # Simple way: Plot points
            traj_x = []
            traj_y = []
            steps = 50
            for i in range(steps + 1):
                p = i / steps
                tr, tt = self.get_transfer_pos(p)
                abs_theta = tt + self.earth_angle_at_launch
                traj_x.append(tr * np.cos(abs_theta))
                traj_y.append(tr * np.sin(abs_theta))
            
            ax.plot(traj_x, traj_y, color=TRANSFER_TRACE, linestyle=":", linewidth=2, alpha=0.5)

        # 5. Draw Rocket
        rx = self.rocket_r * np.cos(self.rocket_theta)
        ry = self.rocket_r * np.sin(self.rocket_theta)
        
        # Rocket Orientation
        # Pointing along velocity vector
        # Tangent... roughly perpendicular to radius? 
        # Just draw a triangle pointing in direction of motion (counter-clockwise)
        
        rot = self.rocket_theta + (np.pi/2)
        
        # Triangle
        size = 0.08
        r_pts = np.array([[0, size], [-size*0.5, -size], [size*0.5, -size]])
        
        # Rotate
        c, s = np.cos(rot), np.sin(rot)
        R = np.array([[c, -s], [s, c]])
        r_trans = np.dot(r_pts, R.T) + [rx, ry]
        
        ax.add_patch(Polygon(r_trans, facecolor=ROCKET_COLOR, zorder=20))
        
        # Flame if transferring
        if self.rocket_active and not self.success:
            # Burn only at start and end?
            # Or draw engine trail
            pass

        # Scale
        limit = 1.8
        ax.set_xlim(-limit * (16/9), limit * (16/9))
        ax.set_ylim(-limit, limit)
        ax.set_aspect('equal')
        
        # Text
        if frame_idx < self.launch_frame:
            ax.text(0, -1.6, "WAIT FOR WINDOW...", ha='center', color="#AAAAAA", fontfamily='sans-serif')
        elif self.success:
            ax.text(0, -1.6, "ARRIVAL CONFIRMED", ha='center', color=SUN_COLOR, fontweight='bold', fontfamily='sans-serif')

        
        # Save
        out_dir = "logic_garden_mars_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"mars_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Calculating Launch Window...")
    
    sim = OrbitSim()
    
    for i in range(TOTAL_FRAMES):
        sim.update(i)
        
        # 1. Canvas
        fig = plt.figure(figsize=(16, 9), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        sim.render(i, ax)
        
        if i % 30 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
