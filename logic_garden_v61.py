"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v61.py
MODE:   Nursery (Quantum Palette)
TARGET: Quantum Entanglement (Bell States)
STYLE:  "The Non-Local Knot" | 40s Deep Time | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# --- 1. THE QUANTUM PALETTE ---
BG_VOID = "#020205"
WAVE_GOLD = "#FFD700"       # The Link
SPIN_UP = "#FF2020"         # Red
SPIN_DOWN = "#2020FF"       # Blue
UNCERTAIN = "#B000B0"       # Purple
GHOST_GREY = "#404040"

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 40
TOTAL_FRAMES = FPS * DURATION

class EntanglementSim:
    def __init__(self):
        # Positions
        self.dist = 0.0 # Separation
        self.max_dist = 8.0
        
        # Spin State
        # 0 = Superposition, 1 = Collapsed
        self.state = 0 
        self.spin_val_A = 0.0 # Will be +1 or -1
        self.spin_val_B = 0.0 # Will be -1 or +1
        
        # Vibration of the tether
        self.phase = 0.0
        
        # Random fluctuation for superposition
        self.noise_seed = np.random.randn(1000)

    def update(self, frame_idx):
        t = frame_idx / float(FPS)
        
        # 1. DRIFT APART (0-20s)
        if frame_idx < 600:
            self.dist = (frame_idx / 600.0) * self.max_dist
        else:
            self.dist = self.max_dist
            
        # 2. MEASUREMENT (At 20s / Frame 600)
        if frame_idx == 600:
            # COLLAPSE WAVEFUNCTION
            self.state = 1
            # Random choice for A
            choice = np.random.choice([1, -1])
            self.spin_val_A = choice
            self.spin_val_B = -choice # Conservation
            
        # Tether vibration
        self.phase += 0.2

    def render(self, frame_idx, fig):
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor(BG_VOID)
        
        # Limits
        ax.set_xlim(-5, 5)
        ax.set_ylim(-2, 2)
        ax.set_zlim(-2, 2)
        ax.set_axis_off()
        
        # Camera
        # Slow pan
        ax.view_init(elev=10, azim=frame_idx * 0.1)
        
        # POSITIONS
        # Move along X axis
        pos_A = np.array([-self.dist/2.0, 0, 0])
        pos_B = np.array([ self.dist/2.0, 0, 0])
        
        # 1. DRAW THE TETHER (The Wavefunction)
        # A sine wave connecting them, representing shared phase
        # Even when far apart, the wave connects them.
        
        # Generate points between A and B
        num_pts = 100
        xs = np.linspace(pos_A[0], pos_B[0], num_pts)
        ys = np.zeros(num_pts)
        zs = np.zeros(num_pts)
        
        # Add vibration (Standing Wave)
        # Amplitude dies off if collapsed? 
        # No, entanglement breaks upon measurement? 
        # Standard QM: Interaction breaks entanglement.
        # But let's show the "Correction" traveling? No, it's instant.
        # Let's show the tether turning from Gold (Potential) to Grey (Broken)
        
        if self.state == 0:
            # Superposition Mode
            amp = 0.5 * np.sin(self.phase)
            # Standing wave k=3
            zs = amp * np.sin(3 * np.pi * (xs - pos_A[0]) / (self.dist + 0.1))
            tether_col = WAVE_GOLD
            tether_alpha = 0.8
        else:
            # Collapsed Mode
            # Tether snaps/fades
            fade_time = (frame_idx - 600) / 60.0 # 2 seconds to fade
            alpha = max(0, 0.8 - fade_time)
            zs = np.zeros(num_pts) # Straight line
            tether_col = GHOST_GREY
            tether_alpha = alpha
            
        if tether_alpha > 0.01:
            ax.plot(xs, ys, zs, color=tether_col, alpha=tether_alpha, linewidth=1.5)

        # 2. DRAW PARTICLES
        # Particle A (Alice)
        # Particle B (Bob)
        
        # Determine Color/Vector
        if self.state == 0:
            # Fluctuation
            idx = frame_idx % 1000
            val = self.noise_seed[idx]
            # Blend colors rapidly
            # 50% Red, 50% Blue -> Purple
            col_A = UNCERTAIN
            col_B = UNCERTAIN
            
            # Spin Vector (Random Jitter)
            vec_A = np.array([0, np.cos(self.phase), np.sin(self.phase)])
            vec_B = -vec_A # Always opposite even in fluctuation? 
            # In Singlet state, yes, even before measurement they are correlated.
            
        else:
            # Determinate
            col_A = SPIN_UP if self.spin_val_A > 0 else SPIN_DOWN
            col_B = SPIN_UP if self.spin_val_B > 0 else SPIN_DOWN
            
            # Solid Vectors
            vec_A = np.array([0, 0, self.spin_val_A * 1.5])
            vec_B = np.array([0, 0, self.spin_val_B * 1.5])

        # Draw Spheres
        ax.scatter([pos_A[0]], [pos_A[1]], [pos_A[2]], color=col_A, s=300, alpha=1.0)
        ax.scatter([pos_B[0]], [pos_B[1]], [pos_B[2]], color=col_B, s=300, alpha=1.0)
        
        # Draw Glow
        ax.scatter([pos_A[0]], [pos_A[1]], [pos_A[2]], color=col_A, s=800, alpha=0.2)
        ax.scatter([pos_B[0]], [pos_B[1]], [pos_B[2]], color=col_B, s=800, alpha=0.2)
        
        # Draw Spin Arrows
        ax.quiver(pos_A[0], pos_A[1], pos_A[2], vec_A[0], vec_A[1], vec_A[2], color="white", length=1.0, normalize=False)
        ax.quiver(pos_B[0], pos_B[1], pos_B[2], vec_B[0], vec_B[1], vec_B[2], color="white", length=1.0, normalize=False)

        # 3. HUD
        fig.text(0.5, 0.92, "LOGIC GARDEN 61: THE NON-LOCAL KNOT", color="white", ha='center', fontsize=16, fontweight='bold', fontfamily='monospace')
        
        if self.state == 0:
            status = f"STATE: ENTANGLED (SUPERPOSITION) | DIST: {self.dist:.2f} units"
            col = WAVE_GOLD
        else:
            status = "STATE: MEASURED (COLLAPSE) | SPOOKY ACTION CONFIRMED"
            col = SPIN_UP
            
        fig.text(0.5, 0.08, status, color=col, ha='center', fontfamily='monospace', fontsize=12,
                  bbox=dict(facecolor='black', edgecolor=col, pad=5, alpha=0.5))
        
        # Equation
        if frame_idx < 600:
             fig.text(0.5, 0.85, r"$\Psi = \frac{1}{\sqrt{2}} (|\uparrow\downarrow\rangle - |\downarrow\uparrow\rangle)$", color="gray", ha='center', fontsize=14)

        # Save
        out_dir = "logic_garden_entangle_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"entangle_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_VOID)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print(f"[NURSERY] Connecting the Universe...")
    
    sim = EntanglementSim()
    
    for i in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10, 10), dpi=100)
        
        sim.update(i)
        sim.render(i, fig)
        
        if i % 60 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
