"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v35.py
MODE:   Nursery (Cymatic Palette)
TARGET: Chladni Patterns (Wave Function Nodal Lines)
STYLE:  "The Sound of Geometry" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

# --- 1. THE CYMATIC PALETTE ---
BG_COLOR = "#050510"        # Acoustic Chamber
PLATE_COLOR = "#101020"     # Dark Metal
SAND_COLOR = "#FFFFFF"      # High Contrast Silica
TEXT_COLOR = "#00FFFF"      # Digital Readout

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
PARTICLE_COUNT = 15000      # Heavy grain count for definition

class ChladniSim:
    def __init__(self):
        # Particles: Normalized coords -1.0 to 1.0
        self.x = np.random.uniform(-1, 1, PARTICLE_COUNT)
        self.y = np.random.uniform(-1, 1, PARTICLE_COUNT)
        self.vx = np.zeros(PARTICLE_COUNT)
        self.vy = np.zeros(PARTICLE_COUNT)
        
        # Sequence of Modes (n, m)
        self.modes = [
            (1, 2),  # The Cross
            (2, 3),  # The Grid
            (3, 5),  # The Lattice
            (5, 7),  # The Mosaic
            (7, 9)   # The High Freq
        ]
        self.current_mode_idx = 0
        self.transition_timer = 0
        self.amplitude = 1.0 # Master volume
        
    def get_vibration(self, x, y, n, m):
        # Chladni 2D Wave Function (Square)
        # u(x,y) = cos(n*pi*x)*cos(m*pi*y) - cos(m*pi*x)*cos(n*pi*y)
        # We need the absolute magnitude of vibration
        
        # Map -1..1 to 0..1 for pi calcs? 
        # Standard Chladni works on -1 to 1 usually with pi/2 or just pi
        # Let's use simple pi scaling
        
        val = np.cos(n * np.pi * x) * np.cos(m * np.pi * y) - \
              np.cos(m * np.pi * x) * np.cos(n * np.pi * y)
              
        return np.abs(val)

    def update(self, frame_idx):
        # 1. Mode Sequencing
        # Change mode every 120 frames (4 seconds)
        cycle_len = 120
        seq_idx = int(frame_idx / cycle_len)
        
        if seq_idx < len(self.modes):
            target_n, target_m = self.modes[seq_idx]
        else:
            target_n, target_m = self.modes[-1] # Hold last
            
        # Detect change -> Scramble
        phase = frame_idx % cycle_len
        
        current_amp = 1.0
        
        # Transition Effect:
        # First 20 frames of cycle: Chaos (Volume Cranked to max, mix modes?)
        if phase < 20:
            # Scramble Phase
            # High vibration everywhere to reset sand
            current_amp = 2.5
            # Jitter target to mix it up
            target_n += np.sin(frame_idx)*0.1
            
        elif phase < 40:
             # Settling Phase
             current_amp = 1.0
        
        # 2. Physics Update (Stochastic Gradient Descent)
        # Particles move randomly proportional to Vibration Amplitude
        # High Vib -> Big jump (Leave)
        # Low Vib -> Small jump (Stay)
        
        vib = self.get_vibration(self.x, self.y, target_n, target_m)
        
        # Kick force
        # Random direction -1 to 1
        rx = np.random.uniform(-1, 1, PARTICLE_COUNT)
        ry = np.random.uniform(-1, 1, PARTICLE_COUNT)
        
        # Step size depends on Vibration
        # If Vib is high, big step. If Vib is 0 (Node), no step.
        step = vib * 0.08 * current_amp
        
        self.x += rx * step
        self.y += ry * step
        
        # 3. Boundary Clamp
        # If they fall off, wrap or clamp? 
        # Real sim: they fall off. Here: Clamp to visual plate
        self.x = np.clip(self.x, -0.98, 0.98)
        self.y = np.clip(self.y, -0.98, 0.98)
        
        return target_n, target_m

    def render(self, frame_idx, n, m, ax):
        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-1.1, 1.1)
        
        # 1. Plate
        plate = Rectangle((-1, -1), 2, 2, color=PLATE_COLOR, zorder=1)
        ax.add_patch(plate)
        
        # 2. Sand
        # Scatter plot
        # Use very small marker size (0.5)
        ax.scatter(self.x, self.y, s=0.8, color=SAND_COLOR, alpha=0.6, zorder=5, marker='.')
        
        # 3. HUD
        # Frequency visualization
        freq_est = int((n * m) * 100) + int(np.sin(frame_idx*0.5)*10)
        info = f"MODE: N={int(n)} M={int(m)}\nFREQ: {freq_est} Hz"
        
        ax.text(-0.95, -0.95, info, color=TEXT_COLOR, fontfamily='monospace', fontsize=14,
                bbox=dict(facecolor='black', edgecolor=TEXT_COLOR, alpha=0.5))

        ax.set_aspect('equal')
        ax.set_axis_off()
        
        out_dir = "logic_garden_chladni_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"chladni_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Vibrating Plate...")
    
    sim = ChladniSim()
    
    for i in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10, 10), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        n, m = sim.update(i)
        sim.render(i, n, m, ax)
        plt.close()
        
        if i % 30 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
