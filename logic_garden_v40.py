"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v40.py
MODE:   Nursery (High Energy Palette)
TARGET: Pulsar (Neutron Star Lighthousing)
STYLE:  "The Cosmic Lighthouse" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Rectangle, Polygon
import os

# --- 1. THE HIGH ENERGY PALETTE ---
BG_COLOR = "#000005"        # Deepest Void
STAR_WHITE = "#FFFFFF"      # Neutron Density
BEAM_CYAN = "#00FFFF"       # Radiation Jet
MAG_PURPLE = "#9D00FF"      # Magnetic Field
SIGNAL_GREEN = "#39FF14"    # Radio Data
GRID_GREY = "#202020"

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION

class PulsarSim:
    def __init__(self):
        self.spin_angle = 0.0
        self.tilt_angle = np.radians(30) # Magnetic axis tilt relative to spin
        self.spin_rate = 0.3 # rad per frame
        
        self.signal_history = [0.0] * 100 # For the graph
        
    def update(self, frame_idx):
        # 1. Spin
        self.spin_angle += self.spin_rate
        
        # 2. Calculating Beam Vector (3D Rotation projected to 2D)
        # Spin Axis is Y (Up).
        # Mag Axis starts tilted in XY plane, then rotates around Y.
        
        # Vector Magnitude
        r = 1.0
        
        # Magnetic North Vector
        # x = r * sin(tilt) * cos(spin)
        # y = r * cos(tilt)
        # z = r * sin(tilt) * sin(spin) (Pointing at/away from camera)
        
        self.mx = r * np.sin(self.tilt_angle) * np.cos(self.spin_angle)
        self.my = r * np.cos(self.tilt_angle)
        self.mz = r * np.sin(self.tilt_angle) * np.sin(self.spin_angle)
        
        # Magnetic South (Opposite)
        self.sx = -self.mx
        self.sy = -self.my
        self.sz = -self.mz
        
        # 3. Detect "Pulse" (Alignment with Camera Z-axis)
        # Camera is at Z = +infinity looking at origin.
        # Dot product with (0,0,1) is just mz.
        
        # Intensity is high when mz is positive and large
        raw_signal = max(0, self.mz) 
        
        # Sharpen the beam (Exponential falloff)
        # Only flash when pointing EXACTLY at us
        focus = 10.0
        signal_strength = raw_signal ** focus
        
        self.signal_history.append(signal_strength)
        if len(self.signal_history) > 100:
            self.signal_history.pop(0)
            
        return signal_strength

    def render(self, frame_idx, signal_strength, ax):
        ax.set_xlim(-8, 8)
        ax.set_ylim(-8, 8)
        
        # 1. Background Grid (Toroidal Reference)
        # Faint lines to show rotation plane
        ax.add_patch(Ellipse((0,0), 10, 2, color=GRID_GREY, fill=False, linewidth=1))
        
        # 2. Magnetic Field Lines (Rotating Loops)
        # These follow the Magnetic Axis.
        # It's hard to draw true 3D rotated dipole lines in 2D plot patches.
        # Approximation: Draw ellipses rotated by visual screen angle.
        
        # Visual angle of the magnetic axis on screen
        screen_angle = np.arctan2(self.my, self.mx)
        screen_deg = np.degrees(screen_angle)
        
        # Z-depth effect: alpha fluctuates with rotation
        z_factor = abs(np.cos(self.spin_angle)) * 0.5 + 0.2
        
        # Draw Dipole Loops
        for scale in [2.0, 4.0, 6.0]:
            # North Loop
            ax.add_patch(Ellipse((0,0), scale*2, scale, angle=screen_deg, 
                                 edgecolor=MAG_PURPLE, fill=False, 
                                 alpha=0.3, linewidth=2))
        
        # 3. The Beams (North and South)
        beam_len = 7.0
        
        # North Beam
        nb_x = self.mx * beam_len
        nb_y = self.my * beam_len
        
        # Beam Width (Visual perspective)
        # If pointing at us (mz > 0), beam looks wider/brighter/shorter?
        # Just use simple lines + flare
        
        # Draw Beam Cone
        start_w = 0.2
        end_w = 1.0
        # Perpendicular vector for thickness
        perp_angle = screen_angle + np.pi/2
        px = np.cos(perp_angle)
        py = np.sin(perp_angle)
        
        # North Poly
        poly_n = [
            [self.mx*0.5 + px*start_w, self.my*0.5 + py*start_w],
            [nb_x + px*end_w, nb_y + py*end_w],
            [nb_x - px*end_w, nb_y - py*end_w],
            [self.mx*0.5 - px*start_w, self.my*0.5 - py*start_w]
        ]
        
        # Alpha depends on Z. If sticking out (z>0), bright. In back, dim.
        alpha_n = 0.8 if self.mz > 0 else 0.2
        ax.add_patch(Polygon(poly_n, color=BEAM_CYAN, alpha=alpha_n))
        
        # South Beam
        sb_x = self.sx * beam_len
        sb_y = self.sy * beam_len
        alpha_s = 0.8 if self.sz > 0 else 0.2
         
        poly_s = [
            [self.sx*0.5 + px*start_w, self.sy*0.5 + py*start_w],
            [sb_x + px*end_w, sb_y + py*end_w],
            [sb_x - px*end_w, sb_y - py*end_w],
            [self.sx*0.5 - px*start_w, self.sy*0.5 - py*start_w]
        ]
        ax.add_patch(Polygon(poly_s, color=BEAM_CYAN, alpha=alpha_s))
        
        # 4. The Star (Neutron Core)
        ax.add_patch(Circle((0,0), 0.5, color=STAR_WHITE, zorder=10))
        
        # 5. The "Flash" (Lens Flare when pointing at camera)
        if signal_strength > 0.1:
            # Huge white halo
            flare_size = signal_strength * 15.0 # Big flash
            ax.add_patch(Circle((0,0), flare_size, color="white", alpha=signal_strength*0.8, zorder=20))
            # Cyan ring
            ax.add_patch(Circle((0,0), flare_size*0.8, color=BEAM_CYAN, fill=False, linewidth=5, alpha=signal_strength, zorder=21))

        # 6. HUD - Radio Signal Graph (Oscilloscope)
        # Bottom area
        graph_y_base = -6.0
        graph_h = 2.0
        bars_count = len(self.signal_history)
        bar_w = 16.0 / bars_count
        
        for i, val in enumerate(self.signal_history):
            bx = -8.0 + i * bar_w
            by = graph_y_base
            bh = val * graph_h
            
            # Color logic: Green traces
            c = SIGNAL_GREEN
            ax.add_patch(Rectangle((bx, by), bar_w*0.8, bh, color=c))
            
        # Label
        freq = self.spin_rate * 30.0 / (2*np.pi) # Hz
        info = f"TYPE: MILLISECOND PULSAR\nFREQ: {freq:.2f} Hz"
        ax.text(-7, 7, info, color=SIGNAL_GREEN, fontfamily='monospace',
                bbox=dict(facecolor='black', edgecolor=SIGNAL_GREEN))

        ax.set_aspect('equal')
        ax.set_axis_off()
        
        out_dir = "logic_garden_pulsar_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"pulsar_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Spinning Up Neutron Star...")
    
    sim = PulsarSim()
    
    for i in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(16, 9), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        sig = sim.update(i)
        sim.render(i, sig, ax)
        plt.close()
        
        if i % 30 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
