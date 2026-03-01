"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v59_loop.py
MODE:   Nursery (Topology Palette)
TARGET: The Mobius Strip (Perfect Loop 4pi)
STYLE:  "The Strange Loop" | 40s Deep Time | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# --- 1. THE TOPOLOGY PALETTE ---
BG_VOID = "#151515"
STRIP_FACE = "#008080"      # Teal (dim)
STRIP_EDGE = "#00FFFF"      # Cyan (bright)
PARTICLE_COL = "#FFFFFF"    # The Monk
NORMAL_VEC = "#FF4500"      # The Stick (Red)
PHASE_2_VEC = "#9400D3"     # The Stick Inverted (Purple)

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 40
TOTAL_FRAMES = FPS * DURATION

class MobiusSim:
    def __init__(self):
        self.R = 4.0 # Major Radius
        self.w = 1.5 # Width
        
        # Grid Resolution
        self.u_res = 120
        self.v_res = 12
        
        # Particle State
        self.p_u = 0.0
        # Exact speed to cover 4pi in TOTAL_FRAMES
        self.speed = (4 * np.pi) / TOTAL_FRAMES 
        
    def parametric(self, u, v):
        # Mobius Parametrization
        # Note: u goes 0..4pi to close the surface in 3D for mesh?
        # Actually 2pi closes the GEOMETRY, but normal flips.
        # 4pi closes the TOPOLOGY (Normal vector returns).
        
        twist = np.cos(u/2)
        lift = np.sin(u/2)
        
        x = (self.R + v * twist) * np.cos(u)
        y = (self.R + v * twist) * np.sin(u)
        z = (self.R + v * twist) * 0.0 + v * lift # Correct Mobius Z depends on v only?
        # Standard Mobius:
        # x = (R + v*cos(u/2)) * cos(u)
        # y = (R + v*cos(u/2)) * sin(u)
        # z = v * sin(u/2)
        
        z = v * lift
        return x, y, z

    def get_mesh(self):
        # Generate surface mesh 0..2pi (visual loop)
        # We extend slightly to overlap for seamless visual if needed
        u = np.linspace(0, 2*np.pi, self.u_res) 
        v = np.linspace(-self.w, self.w, self.v_res)
        U, V = np.meshgrid(u, v)
        
        X, Y, Z = self.parametric(U, V)
        return X, Y, Z

    def update(self, frame_idx):
        # Move particle
        self.p_u = frame_idx * self.speed
        
        # Camera Rotation (Synchronized 360 deg)
        self.cam_angle = 360 * (frame_idx / TOTAL_FRAMES)

    def render(self, frame_idx, fig):
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor(BG_VOID)
        
        # Setup 3D limits
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.set_zlim(-3, 3)
        ax.set_axis_off()
        
        # Camera Rotate
        ax.view_init(elev=25, azim=self.cam_angle)
        
        # 1. DRAW SURFACE
        X, Y, Z = self.get_mesh()
        
        # Surface with transparency
        # To make it look "solid" yet "void", we use low alpha
        ax.plot_surface(X, Y, Z, color=STRIP_FACE, alpha=0.2, rstride=5, cstride=1, shade=False, edgecolor='none')
        
        # Grid Lines (The "Logic")
        # Longitudinal Lines (Along the loop)
        for i in range(0, self.v_res, 3): 
            v_val = np.linspace(-self.w, self.w, self.v_res)[i]
            # Draw full 2pi loop
            u_line = np.linspace(0, 2*np.pi, 200)
            lx, ly, lz = self.parametric(u_line, v_val)
            ax.plot(lx, ly, lz, color=STRIP_EDGE, linewidth=0.6, alpha=0.4)
            
        # 2. DRAW THE MONK (Particle)
        monk_v = 0.0 # Center
        px, py, pz = self.parametric(self.p_u, monk_v)
        
        # Particle Glow
        ax.scatter([px], [py], [pz], color=PARTICLE_COL, s=150, alpha=1.0, zorder=10)
        ax.scatter([px], [py], [pz], color=STRIP_EDGE, s=400, alpha=0.3, zorder=9)
        
        # 3. DRAW THE NORMAL (The Stick)
        # Calculate normal at p_u
        nu = self.p_u
        
        # Tangent Vectors
        # dP/du (approximate direction of travel)
        tx = -np.sin(nu)
        ty = np.cos(nu)
        tz = 0.0
        
        # dP/dv (direction of width / twist)
        bx = np.cos(nu/2)*np.cos(nu)
        by = np.cos(nu/2)*np.sin(nu)
        bz = np.sin(nu/2)
        
        # Normal = Cross(T, B) - Simplified
        # We want the normal to ROTATE with u/2
        # Normal at u=0 is Z (0,0,1)
        # Normal at u=pi is X?
        
        # Let's use the explicit normal formula for mobius strip center
        # N(u) = [ cos(u)sin(u/2), sin(u)sin(u/2), -cos(u/2) ]
        # Wait, at u=0 this gives (0,0,-1).
        # Let's derive or use heuristic for visual arrow
        
        # Heuristic: The normal rotates in the plane perpendicular to the path
        # It's basically the 'lift' vector rotated 90 deg?
        
        # Let's use the cross product logic, it's safer.
        nx = ty*bz - tz*by
        ny = tz*bx - tx*bz
        nz = tx*by - ty*bx
        
        # Normalize
        nm = np.sqrt(nx**2 + ny**2 + nz**2)
        nx /= nm; ny /= nm; nz /= nm
        
        # Stick Color depends on orientation (Flip check)
        # Phase 1 (0-2pi) vs Phase 2 (2pi-4pi)
        
        cycle = self.p_u % (4*np.pi)
        stick_col = NORMAL_VEC
        phase_lbl = "PHASE 1: THE SPEAKING (SIDE A)"
        
        if cycle >= 2*np.pi:
             stick_col = PHASE_2_VEC # Purple to show inversion
             phase_lbl = "PHASE 2: THE SILENCE (SIDE B)"
        
        # Draw Arrow
        L = 2.5
        ax.plot([px, px + nx*L], [py, py + ny*L], [pz, pz + nz*L], color=stick_col, linewidth=4)
        
        # 4. HUD
        # Matplotlib 3D doesn't support text2D easily on the Axes object directly in this context sometimes
        # We attach to figure
        fig.text(0.5, 0.92, "LOGIC GARDEN 59: THE STRANGE LOOP", color="white", ha='center', fontsize=16, fontweight='bold', fontfamily='monospace')
        
        fig.text(0.5, 0.08, phase_lbl, color=stick_col, ha='center', fontfamily='monospace', fontsize=14,
                  bbox=dict(facecolor='black', edgecolor=stick_col, pad=5))

        # Save
        out_dir = "logic_garden_mobius_fixed_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"mobius_fixed_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_VOID)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print(f"[NURSERY] Looping the Infinity...")
    
    sim = MobiusSim()
    
    for i in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10, 10), dpi=100)
        
        sim.update(i)
        sim.render(i, fig)
        # plt.close(fig) # Handled in render save
        
        if i % 60 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
