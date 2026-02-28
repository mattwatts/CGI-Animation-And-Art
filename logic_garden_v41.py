"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v41_fixed.py
MODE:   Nursery (LIGO Palette)
TARGET: Gravitational Waves (Binary Merger & Chirp Signal)
STYLE:  "The Cosmic Chirp" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse
import os

# --- 1. THE LIGO PALETTE ---
BG_COLOR = "#050510"        # Vacuum Tube
WAVE_COLOR = "#00FFFF"      # Laser Inteferometer light
STRAIN_HOT = "#FF4500"      # High Distortion
HOLE_COLOR = "#000000"      # Event Horizon
ACCRETION = "#FFFFFF"       # Lensing Halo

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
MERGER_FRAME = 450          # The exact moment of contact

class MergerSim:
    def __init__(self):
        self.angle = 0.0
        self.phase = 'inspiral' # inspiral, merger, ringdown
        
        # Strain Data (The Chirp Graph)
        self.strain_history = [0.0] * 400 
        self.max_history = 400
        
        # Wavefronts
        self.waves = []

    def update(self, frame_idx):
        # Time to merger (reversed)
        time_to_merge = MERGER_FRAME - frame_idx
        
        # 1. ORBITAL MECHANICS (Post-Newtonian Approx)
        if time_to_merge > 0:
            # Separation decreases as we get closer to T=0
            # Scale time so separation starts at ~6.0 and hits 0.6 at merger
            # r ~ t^0.25 (approximate inspiral scaling)
            t_norm = max(1.0, time_to_merge) / MERGER_FRAME
            self.separation = 6.0 * (t_norm ** 0.4) 
            
            # Velocity (Keplerian + GR)
            # v ~ 1/sqrt(r)
            self.velocity = 0.8 / np.sqrt(max(0.1, self.separation))
            
            self.angle += self.velocity
            self.phase = 'inspiral'
            
            # Amplitude increases
            amp = 2.0 / (self.separation + 0.5)
            # Freq increases (velocity)
            strain = amp * np.sin(self.angle * 2) # Quadrupole

        else:
            # RINGDOWN PHASE
            self.phase = 'ringdown'
            self.separation = 0.0
            
            # Damped Harmonic Oscillator
            t_ring = frame_idx - MERGER_FRAME
            decay = np.exp(-t_ring * 0.05)
            freq = 1.5 # Fixed high ringdown freq
            strain = 8.0 * np.sin(self.angle + t_ring * freq) * decay
            
            # Stop strain if too small
            if decay < 0.01: strain = 0.0

        # 2. WAVE GENERATION
        # Emit a wave crest at peaks only? Or continuous spiral?
        # Let's emit a particle on the "arms"
        if frame_idx % 2 == 0:
            # Arm 1
            self.waves.append({
                'r': 0.0 if self.phase == 'ringdown' else self.separation/2.0, 
                'theta': self.angle,
                'amp': 1.0 if self.phase == 'ringdown' else 0.5 / (self.separation + 0.1)
            })
            # Arm 2
            self.waves.append({
                'r': 0.0 if self.phase == 'ringdown' else self.separation/2.0, 
                'theta': self.angle + np.pi,
                'amp': 1.0 if self.phase == 'ringdown' else 0.5 / (self.separation + 0.1)
            })
            
        # Expand Waves (Speed of Light)
        c = 0.35
        for w in self.waves:
            w['r'] += c
            # Rotation drag (Spiral effect visual hack)
            w['theta'] -= 0.02
            w['amp'] *= 0.98 # Distance attenuation
            
        self.waves = [w for w in self.waves if w['amp'] > 0.05]

        # 3. RECORD DATA
        self.strain_history.append(strain * 0.1)
        if len(self.strain_history) > self.max_history:
            self.strain_history.pop(0)

    def render(self, frame_idx, ax):
        ax.set_xlim(-10, 10)
        ax.set_ylim(-12, 8) # Extra space at bottom for graph
        
        # 1. GRAVITATIONAL WAVES (The Fabric)
        # Plot as scatter points forming the spiral
        wx = []
        wy = []
        ws = []
        
        for w in self.waves:
            x = w['r'] * np.cos(w['theta'])
            y = w['r'] * np.sin(w['theta'])
            wx.append(x)
            wy.append(y)
            ws.append(w['amp'] * 50)
            
        ax.scatter(wx, wy, s=ws, color=WAVE_COLOR, alpha=0.4, marker='o')

        # 2. THE BLACK HOLES
        if self.phase == 'inspiral':
            # Two holes
            r1 = self.separation / 2.0
            
            # Hole 1
            h1x = r1 * np.cos(self.angle)
            h1y = r1 * np.sin(self.angle)
            ax.add_patch(Circle((h1x, h1y), 0.8, color=HOLE_COLOR, zorder=10))
            # Accretion Glow
            ax.add_patch(Circle((h1x, h1y), 1.0, color=ACCRETION, fill=False, linewidth=1, zorder=9, alpha=0.5))

            # Hole 2
            h2x = r1 * np.cos(self.angle + np.pi)
            h2y = r1 * np.sin(self.angle + np.pi)
            ax.add_patch(Circle((h2x, h2y), 0.8, color=HOLE_COLOR, zorder=10))
            ax.add_patch(Circle((h2x, h2y), 1.0, color=ACCRETION, fill=False, linewidth=1, zorder=9, alpha=0.5))
            
        else: # Merger / Ringdown
            # Single Hole
            # Wobble geometry (Quasinormal Modes)
            t_ring = frame_idx - MERGER_FRAME
            damp = np.exp(-t_ring * 0.05)
            
            # Distortion amounts
            dx = np.sin(t_ring * 0.8) * 0.3 * damp
            dy = np.cos(t_ring * 0.8) * 0.3 * damp
            
            # Draw as Ellipse to show distortion
            # Base radius 1.5 (Mass conservation: Area increase)
            radius_base = 1.5
            ax.add_patch(Ellipse((0,0), radius_base*2 + dx, radius_base*2 + dy, 
                                 angle=self.angle*10, color=HOLE_COLOR, zorder=10))
            
            # Hot Horizon (The "Event")
            if t_ring < 30:
                # Flash
                alpha_flash = 1.0 - (t_ring/30.0)
                ax.add_patch(Circle((0,0), 5.0 * alpha_flash, color="white", alpha=alpha_flash*0.5, zorder=5))
                ax.text(0, 0, "MERGER", color="black", ha='center', va='center', fontweight='bold', alpha=alpha_flash)

        # 3. THE CHIRP GRAPH (Bottom)
        # Background box
        bg_rect = plt.Rectangle((-10, -12), 20, 4, color="#000000", alpha=0.8, zorder=15)
        ax.add_patch(bg_rect)
        
        # Plot Line
        # Map history to x coordinates -9 to 9
        data_len = len(self.strain_history)
        gx = np.linspace(-9, 9, data_len)
        gy = np.array(self.strain_history) * 10.0 - 10.0 # Center at y=-10
        
        # Color the line based on "heat" (amplitude)
        # Using simple plot for speed, but coloring last segment red
        ax.plot(gx, gy, color=WAVE_COLOR, linewidth=1.5, zorder=16)
        
        # Highlight cursor (Current time)
        ax.scatter([9], [gy[-1]], color=STRAIN_HOT, s=50, zorder=17)

        # Labels
        status = "PHASE 1: INSPIRAL"
        if self.phase == 'ringdown': status = "PHASE 3: RINGDOWN"
        # Plunge detection
        if self.phase == 'inspiral' and self.separation < 1.0: status = "PHASE 2: PLUNGE"
        
        ax.text(-9, -7.5, status, color=STRAIN_HOT, fontfamily='monospace', fontsize=12, fontweight='bold', zorder=20)
        ax.text(9, -7.5, "LIGO STRAIN DATA (h)", color=WAVE_COLOR, ha='right', fontfamily='monospace', fontsize=8, zorder=20)

        ax.set_aspect('equal')
        ax.set_axis_off()
        
        out_dir = "logic_garden_gravity_frames_fixed"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"gravity_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Compressing Space-Time...")
    
    sim = MergerSim()
    
    for i in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10, 12), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        sim.update(i)
        sim.render(i, ax)
        plt.close()
        
        if i % 30 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
