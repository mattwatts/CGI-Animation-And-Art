"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v63_loop.py
MODE:   Nursery (Quantum Palette)
TARGET: Quantum Superposition (Seamless Rabi Oscillation)
STYLE:  "The Quantum Coin Loop" | 40s Deep Time | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# --- 1. THE QUBIT PALETTE ---
BG_VOID = "#080810"
SPHERE_GRID = "#008080"     # Teal
STATE_VEC = "#FFD700"       # Gold
BASIS_0 = "#FF4500"         # Red (North)
BASIS_1 = "#1E90FF"         # Blue (South)
TRACE_COL = "#FFFFFF"

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 40
TOTAL_FRAMES = FPS * DURATION

class BlochLoopSim:
    def __init__(self):
        # We perform a rotation around the Y-axis
        # Theta goes 0 -> 2pi (Full circle passing through poles)
        self.theta = 0.0
        self.phi = 0.0 # Keeping phi fixed (or 0) for pure Rabi oscillation
        
        # Camera Angle
        self.cam_azim = 0.0
        
        # Trace history
        self.history = []

    def get_coords(self, theta, phi):
        # Bloch Sphere mapping
        # x = sin(theta) cos(phi)
        # y = sin(theta) sin(phi)
        # z = cos(theta)
        x = np.sin(theta) * np.cos(phi)
        y = np.sin(theta) * np.sin(phi)
        z = np.cos(theta)
        return x, y, z

    def update(self, frame_idx):
        prog = frame_idx / float(TOTAL_FRAMES)
        
        # 1. QUANTUM STATE ROTATION (Rabi Cycle)
        # Theta: 0 -> 2*pi
        self.theta = prog * 2 * np.pi
        
        # 2. CAMERA ORBIT
        # Full 360 spin for seamless visual loop
        self.cam_azim = prog * 360.0
        
        # Update Trace
        cx, cy, cz = self.get_coords(self.theta, self.phi)
        self.history.append((cx, cy, cz))
        
        # Limit trace length to show a "Comet Tail"
        trace_len = 100
        if len(self.history) > trace_len:
            self.history.pop(0)

    def render(self, frame_idx, fig):
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor(BG_VOID)
        
        # Camera
        ax.view_init(elev=20, azim=self.cam_azim)
        
        limit = 1.1
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.set_zlim(-limit, limit)
        ax.set_axis_off()
        
        # 1. DRAW WIREFRAME SPHERE
        # Standard sphere grid
        u, v = np.mgrid[0:2*np.pi:30j, 0:np.pi:20j]
        x = np.cos(u)*np.sin(v)
        y = np.sin(u)*np.sin(v)
        z = np.cos(v)
        ax.plot_wireframe(x, y, z, color=SPHERE_GRID, alpha=0.1, linewidth=0.5)
        
        # Equator Ring for reference
        theta_eq = np.linspace(0, 2*np.pi, 100)
        xe = np.cos(theta_eq)
        ye = np.sin(theta_eq)
        ze = np.zeros_like(xe)
        ax.plot(xe, ye, ze, color=SPHERE_GRID, alpha=0.4, linewidth=1, linestyle="--")
        
        # 2. DRAW BASES (Axes)
        ax.plot([0,0],[0,0],[-1.2,1.2], color=SPHERE_GRID, alpha=0.3, linestyle=":") # Z Axis
        
        # |0> Node (North)
        ax.scatter([0],[0],[1], color=BASIS_0, s=80, alpha=0.9)
        ax.text(0, 0, 1.3, r"$|0\rangle$", color=BASIS_0, fontsize=12, fontweight='bold', ha='center')
        
        # |1> Node (South)
        ax.scatter([0],[0],[-1], color=BASIS_1, s=80, alpha=0.9)
        ax.text(0, 0, -1.3, r"$|1\rangle$", color=BASIS_1, fontsize=12, fontweight='bold', ha='center')
        
        # 3. DRAW STATE VECTOR
        vx, vy, vz = self.get_coords(self.theta, self.phi)
        
        # The Arrow
        ax.quiver(0, 0, 0, vx, vy, vz, color=STATE_VEC, linewidth=4, arrow_length_ratio=0.15)
        
        # The Trace (Comet Tail)
        if len(self.history) > 1:
            hx, hy, hz = zip(*self.history)
            # Fade trace alpha? Matplotlib plot gradient is hard
            # Just draw solid line for now
            ax.plot(hx, hy, hz, color=TRACE_COL, linewidth=1.5, alpha=0.6)
            
        # 4. HUD STATISTICS
        # P(0) = cos^2(theta/2)
        p0 = np.cos(self.theta / 2.0)**2
        p1 = 1.0 - p0 # Conservation of probability
        
        # Determine Status Text
        # Identify key positions
        t_mod = self.theta % (2*np.pi)
        
        if t_mod < 0.2 or t_mod > (2*np.pi - 0.2):
            status = "STATE: PURE |0>"
            col = BASIS_0
        elif abs(t_mod - np.pi) < 0.2:
            status = "STATE: PURE |1>"
            col = BASIS_1
        else:
            status = "STATE: SUPERPOSITION"
            col = STATE_VEC
            
        # Overlay Text
        fig.text(0.5, 0.92, "LOGIC GARDEN 63: THE QUANTUM COIN", color="white", ha='center', fontsize=16, fontweight='bold', fontfamily='monospace')
        fig.text(0.5, 0.88, "(SEAMLESS RABI CYCLE)", color=SPHERE_GRID, ha='center', fontsize=10, fontfamily='monospace', alpha=0.7)
        
        # Probabilities
        fig.text(0.1, 0.1, f"P(|0>) = {p0*100:5.1f}%", color=BASIS_0, fontsize=14, fontfamily='monospace', fontweight='bold')
        fig.text(0.7, 0.1, f"P(|1>) = {p1*100:5.1f}%", color=BASIS_1, fontsize=14, fontfamily='monospace', fontweight='bold')
        
        # Center Status Box
        fig.text(0.5, 0.08, status, color=col, ha='center', fontsize=12,
                 bbox=dict(facecolor='black', edgecolor=col, alpha=0.8, pad=6))

        # Save
        out_dir = "logic_garden_loop_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"loop_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_VOID)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print(f"[NURSERY] Cycling the State...")
    
    sim = BlochLoopSim()
    
    for i in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10, 10), dpi=100)
        
        sim.update(i)
        sim.render(i, fig)
        
        if i % 60 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
