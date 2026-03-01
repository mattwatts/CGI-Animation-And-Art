"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v65.py
MODE:   Nursery (Astrophysics Palette)
TARGET: Quasar (Relativistic Jet & Accretion)
STYLE:  "The Friction Engine" | 40s Deep Time | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# --- 1. THE QUASAR PALETTE ---
BG_VOID = "#050505"
JET_CORE = "#E0FFFF"        # White-Blue
JET_OUTER = "#00FFFF"       # Cyan
DISK_HOT = "#FFD700"        # Gold (Approaching)
DISK_COLD = "#8B0000"       # Dark Red (Receding)
EVENT_HORIZON = "#000000"
PHOTON_RING = "#FFFFFF"

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 40
TOTAL_FRAMES = FPS * DURATION

class QuasarSim:
    def __init__(self):
        self.num_disk = 4000
        self.num_jet = 2000
        
        # 1. INITIALIZE DISK PARTICLES
        # Logarithmic spiral distribution for density
        r = np.random.uniform(2.0, 8.0, self.num_disk)
        theta = np.random.uniform(0, 2*np.pi, self.num_disk)
        
        self.disk_r = r
        self.disk_theta = theta
        self.disk_z = np.random.normal(0, 0.05, self.num_disk) # Thin disk
        
        # Keplerian Velocity (v ~ 1/sqrt(r))
        # Angular velocity omega = v/r ~ 1 / r^1.5
        self.disk_omega = 5.0 / np.power(self.disk_r, 1.5)
        
        # 2. INITIALIZE JET PARTICLES
        # Two jets (North/South)
        z_jet = np.random.exponential(scale=3.0, size=self.num_jet)
        z_jet = np.clip(z_jet, 0.5, 12.0)
        
        # Assign half to negative Z
        mask = np.random.rand(self.num_jet) > 0.5
        z_jet[mask] *= -1
        
        self.jet_z = z_jet
        self.jet_r = 0.2 + 0.1 * np.abs(z_jet) # Conical expansion
        self.jet_theta = np.random.uniform(0, 2*np.pi, self.num_jet)
        
        # Jet velocity (Plasma flow)
        self.jet_vz = np.sign(z_jet) * 0.5
        
    def update(self, frame_idx):
        # 1. Rotate Disk
        self.disk_theta += self.disk_omega * 0.05
        
        # 2. Flow Jet
        # Move particles outward along Z
        self.jet_z += self.jet_vz
        # Rotate Jet (Magnetic Helix)
        self.jet_theta += 0.2
        
        # Reset Jet particles if too far
        reset_mask = np.abs(self.jet_z) > 12.0
        self.jet_z[reset_mask] = np.sign(self.jet_z[reset_mask]) * 0.5
        self.jet_theta[reset_mask] = np.random.uniform(0, 2*np.pi, np.sum(reset_mask))

    def get_disk_colors(self, view_vec):
        # Doppler Beaming Logic
        # Calculate velocity vector for each particle
        # Tangential velocity direction is (-sin(theta), cos(theta), 0)
        
        vx = -np.sin(self.disk_theta)
        vy =  np.cos(self.disk_theta)
        
        # Project velocity onto view vector (Dot product)
        # View vector is normalized 2D xy projection roughly
        # Let's say camera is at specific azimuth
        view_x = view_vec[0]
        view_y = view_vec[1]
        
        doppler = vx * view_x + vy * view_y
        
        # Map Doppler (-1 to 1) to Color
        # +1 (Approaching) -> Gold/White
        # -1 (Receding) -> Red/Dim
        
        colors = np.zeros((self.num_disk, 4))
        
        # Base RGBs
        c_hot = matplotlib.colors.to_rgb(DISK_HOT)
        c_cold = matplotlib.colors.to_rgb(DISK_COLD)
        
        # Vectorized color map
        # Normalize doppler to 0..1
        norm = (doppler + 1.0) / 2.0
        
        # Non-linear boost for "Beaming" (Relativistic effect)
        # Brightness increases heavily on approach
        norm = np.power(norm, 0.8) 
        
        for i in range(3):
            colors[:, i] = c_cold[i] * (1-norm) + c_hot[i] * norm
            
        colors[:, 3] = 0.4 + 0.4 * norm # Alpha also pulses
        
        return colors

    def render(self, frame_idx, fig):
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor(BG_VOID)
        
        # Camera Orbit
        angle_deg = frame_idx * 0.5
        angle_rad = np.radians(angle_deg)
        elev = 15.0
        ax.view_init(elev=elev, azim=angle_deg)
        
        limit = 10
        ax.set_xlim(-limit, limit); ax.set_ylim(-limit, limit); ax.set_zlim(-limit, limit)
        ax.set_axis_off()
        
        # View Vector (from camera to origin) in XY plane
        # Azimuth 0 looks from -Y towards +Y? 
        # Matplotlib definition: Azim is rotation around Z. 
        view_x = np.cos(angle_rad - np.pi/2) 
        view_y = np.sin(angle_rad - np.pi/2)
        
        # 1. PREPARE GEOMETRY
        # Disk Coords
        dx = self.disk_r * np.cos(self.disk_theta)
        dy = self.disk_r * np.sin(self.disk_theta)
        dz = self.disk_z
        
        # Jet Coords
        jx = self.jet_r * np.cos(self.jet_theta)
        jy = self.jet_r * np.sin(self.jet_theta)
        jz = self.jet_z
        
        # 2. DEPTH SORTING (Manual Painter's Algorithm)
        # We must sort ALL particles (Disk + Jet) by distance to camera
        # Camera position
        r_cam = 20.0
        cam_z = r_cam * np.sin(np.radians(elev))
        r_xy = r_cam * np.cos(np.radians(elev))
        cam_x = r_xy * np.cos(angle_rad - np.pi/2) # Adjust phase to match view
        cam_y = r_xy * np.sin(angle_rad - np.pi/2)
        
        # Combine all particles
        all_x = np.concatenate([dx, jx])
        all_y = np.concatenate([dy, jy])
        all_z = np.concatenate([dz, jz])
        
        # Calculate distance squared (Sort Key) -> Further = Draw First
        # dist = (x-cx)^2 + ... (Negative for descending sort)
        dists = -((all_x - cam_x)**2 + (all_y - cam_y)**2 + (all_z - cam_z)**2)
        
        sort_indices = np.argsort(dists)
        
        # Colors
        disk_cols = self.get_disk_colors([view_x, view_y])
        jet_cols = np.tile(matplotlib.colors.to_rgba(JET_OUTER, alpha=0.3), (self.num_jet, 1))
        # Make jet core brighter
        core_mask = np.abs(self.jet_z) < 2.0
        jet_cols[core_mask] = matplotlib.colors.to_rgba(JET_CORE, alpha=0.6)
        
        all_cols = np.vstack([disk_cols, jet_cols])
        
        # 3. RENDER SORTED
        sorted_x = all_x[sort_indices]
        sorted_y = all_y[sort_indices]
        sorted_z = all_z[sort_indices]
        sorted_c = all_cols[sort_indices]
        sizes = np.ones_like(sorted_x) * 3.0
        
        ax.scatter(sorted_x, sorted_y, sorted_z, c=sorted_c, s=sizes, depthshade=False)
        
        # 4. BLACK HOLE (The Shadow)
        # We need to draw the black hole *in the middle* of the sorted stack
        # But `ax.scatter` is one call. 
        # Matplotlib `zorder` won't interleave with a single scatter call.
        # Hack: The black hole is at (0,0,0).
        # We just draw a large black sphere. Matplotlib's own depth sorting might handle it 
        # if we add it as a separate object, but scatter point sorting is usually separate.
        # Let's draw it explicitly with a high-ish zorder but rely on the gap in our disk (r > 2.0).
        # Since our disk starts at r=2.0, we just need to fill the hole with Black.
        
        ax.scatter([0], [0], [0], color=EVENT_HORIZON, s=500, alpha=1.0, zorder=10)
        # Photon Ring (Visual effect)
        ax.scatter([0], [0], [0], color=PHOTON_RING, s=550, alpha=0.1, zorder=9)

        # 5. HUD
        fig.text(0.5, 0.92, "LOGIC GARDEN 65: THE FRICTION ENGINE", color="white", ha='center', fontsize=16, fontweight='bold', fontfamily='monospace')
        
        power = "LUMINOSITY: 10^40 WATTS"
        fig.text(0.5, 0.05, power, color=DISK_HOT, ha='center', fontfamily='monospace', fontsize=12,
                 bbox=dict(facecolor='black', edgecolor=DISK_HOT, pad=5, alpha=0.5))

        # Save
        out_dir = "logic_garden_quasar_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"quasar_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_VOID)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print(f"[NURSERY] Igniting the Nucleus...")
    
    sim = QuasarSim()
    
    for i in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10, 10), dpi=100)
        
        sim.update(i)
        sim.render(i, fig)
        
        if i % 60 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
