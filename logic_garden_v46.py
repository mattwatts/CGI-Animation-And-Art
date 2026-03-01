"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v46.py
MODE:   Nursery (Quantum Palette)
TARGET: Double Slit Experiment (Observer Effect)
STYLE:  "The Observer" | Split-Phase Simulation | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Wedge
import os

# --- 1. THE QUANTUM PALETTE ---
BG_COLOR = "#050005"
WAVE_CYAN = "#00FFFF"       # Unobserved Potential
PARTICLE_GOLD = "#FFD700"   # Observed Reality
OBSERVER_RED = "#FF0000"    # Calibration Laser / Eye
SCREEN_GREEN = "#39FF14"    # Detector Results
BARRIER_GREY = "#404040"

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION

class DetectorScreen:
    def __init__(self, width=16.0, bins=200):
        self.width = width
        self.bins = bins
        self.histogram = np.zeros(bins)
        
    def hit(self, x):
        # Map x (-8 to 8) to bin (0 to 200)
        # Clamp
        norm_x = (x + self.width/2) / self.width
        idx = int(norm_x * self.bins)
        if 0 <= idx < self.bins:
            self.histogram[idx] += 1.0

class QuantumSim:
    def __init__(self):
        self.phase = 'wave' # wave (0-300), particle (300-600)
        self.particles = [] # In-flight
        self.screen = DetectorScreen()
        self.eye_openness = 0.0
        
        # Slit positions
        self.slit_y = 0.0
        self.slit_1_x = -2.0
        self.slit_2_x = 2.0
        
    def update(self, frame_idx):
        # SWITCH PHASE at Frame 300
        if frame_idx == 300:
            self.phase = 'particle'
            
        # ANIMATE EYE
        if self.phase == 'particle':
            self.eye_openness = min(1.0, self.eye_openness + 0.05)
        else:
            self.eye_openness = max(0.0, self.eye_openness - 0.05)
            
        # SPAWN PARTICLES
        # Rate: 5 per frame
        for _ in range(5):
            # Select Slit?
            # 1. Start at Source (Bottom)
            start_x = 0
            start_y = -8
            
            # 2. Determine "Destined" Result on screen based on Physics
            if self.phase == 'wave':
                # Interference Pattern Dest (Probability Dist)
                # I(x) ~ cos^2(k*x) * envelope
                # Rejection sampling for target position
                while True:
                    gx = np.random.uniform(-8, 8)
                    # Simple interference function approx
                    prob = (np.cos(gx * 1.5)**2) * np.exp(-0.1 * gx**2)
                    if np.random.random() < prob:
                        target_x = gx
                        break
                col = WAVE_CYAN
                
            else:
                # Particle Pattern Dest (Two Gaussians)
                # Randomly pick slit 1 or 2
                if np.random.random() < 0.5:
                    mu = -3.0 # Projected impact from slit 1
                else:
                    mu = 3.0 # Projected impact from slit 2
                    
                target_x = np.random.normal(mu, 1.0)
                col = PARTICLE_GOLD
                
            # Create particle moving from source to slit to target
            # Ideally we animate them passing slits.
            # Simplified: Spawn AT slit for visualization of the path logic
            
            # Which slit is closer to target trajectory?
            # For Wave, it goes through BOTH. We visualize it as a wavefront or split particle?
            # Let's visualize Wave as a Cyan Dot that travels in a curve
            
            self.particles.append({
                'x': 0, 'y': -8,
                'tx': target_x, 'ty': 8, # Top screen
                'progress': 0.0,
                'color': col,
                'mode': self.phase
            })
            
        # MOVE PARTICLES
        for p in self.particles:
            p['progress'] += 0.02
            
            # Trajectory Logic
            # P0(0,-8) -> P1(Slit) -> P2(Target)
            # Quadratic Bezier or Linear?
            
            # Choosing intermediate slit point
            if p['mode'] == 'wave':
                # "Both" slits? Visually jitter between them or go center?
                # Wave particles "interfere".
                # Let's lerp directly to target but visualize them differently
                
                # Simple Linear for now implies they ignore slits?
                # No, they must pass Y=0.
                
                if p['progress'] < 0.5:
                    # Source to Center-ish
                    t = p['progress'] * 2
                    p['x'] = 0
                    p['y'] = -8 + t * 8
                else:
                    # Center to Target
                    t = (p['progress'] - 0.5) * 2
                    p['x'] = t * p['tx']
                    p['y'] = t * 8 
                    
            else:
                # Particle Mode: Must pick a slit visually
                # Based on target X sign roughly
                slit_x = -2.0 if p['tx'] < 0 else 2.0
                
                if p['progress'] < 0.5:
                     # Source to Slit
                    t = p['progress'] * 2
                    p['x'] = t * slit_x
                    p['y'] = -8 + t * 8
                else:
                    # Slit to Target
                    t = (p['progress'] - 0.5) * 2
                    p['x'] = slit_x + t * (p['tx'] - slit_x)
                    p['y'] = t * 8
            
            # Hit Screen
            if p['progress'] >= 1.0:
                self.screen.hit(p['tx'])
                
        self.particles = [p for p in self.particles if p['progress'] < 1.0]

    def render(self, frame_idx, ax):
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        
        # 1. The Barrier
        ax.plot([-10, -3], [0, 0], color=BARRIER_GREY, linewidth=5)
        ax.plot([-1, 1], [0, 0], color=BARRIER_GREY, linewidth=5)
        ax.plot([3, 10], [0, 0], color=BARRIER_GREY, linewidth=5)
        
        # 2. The Particles
        px = [p['x'] for p in self.particles]
        py = [p['y'] for p in self.particles]
        pc = [p['color'] for p in self.particles]
        
        if px:
            ax.scatter(px, py, c=pc, s=10, alpha=0.8, zorder=10)
            
        # 3. Wavefronts (Visual styling only for Wave Mode)
        if self.phase == 'wave':
            # Draw expanding circles from slits
            # Just animation loop effect
            scale = (frame_idx % 20) / 20.0 * 8.0 # 0 to 8 radius
            
            # Slit 1 ripples
            ax.add_patch(Circle((-2, 0), scale, color=WAVE_CYAN, fill=False, alpha=0.2))
            ax.add_patch(Circle((-2, 0), scale/2, color=WAVE_CYAN, fill=False, alpha=0.1))
            
            # Slit 2 ripples
            ax.add_patch(Circle((2, 0), scale, color=WAVE_CYAN, fill=False, alpha=0.2))
            ax.add_patch(Circle((2, 0), scale/2, color=WAVE_CYAN, fill=False, alpha=0.1))

        # 4. The Observer (Eye)
        if self.eye_openness > 0.01:
            # Eye Base
            eye_h = self.eye_openness * 1.5
            # Sclera
            ax.add_patch(Circle((0, 3), 1.0, color="black", zorder=20)) # Pupil
            # Red Glow
            ax.add_patch(Circle((0, 3), 1.2, color=OBSERVER_RED, alpha=0.3, zorder=19))
            
            # Laser beams to slits
            ax.plot([0, -2], [3, 0], color=OBSERVER_RED, alpha=self.eye_openness*0.5, linestyle='--')
            ax.plot([0, 2], [3, 0], color=OBSERVER_RED, alpha=self.eye_openness*0.5, linestyle='--')
            
            # "OBSERVING" text
            ax.text(0, 4.5, "OBSERVING", color=OBSERVER_RED, ha='center', fontsize=10, fontweight='bold')

        # 5. Screen Results (Histogram)
        # Top of chart y=8
        # We draw bars DOWN from 10 or UP from 8? Let's draw UP from 8.
        
        bin_w = self.screen.width / self.screen.bins
        max_h = 2.0
        
        # Normalize histogram for display
        peak = np.max(self.screen.histogram)
        if peak == 0: peak = 1
        
        for i, val in enumerate(self.screen.histogram):
            if val > 0:
                h = (val / peak) * max_h
                bx = -8 + i * bin_w
                by = 8.0
                c = SCREEN_GREEN
                ax.add_patch(Rectangle((bx, by), bin_w, h, color=c, alpha=0.8))

        # 6. HUD
        status = "PHASE 1: NO OBSERVER (WAVE)"
        col = WAVE_CYAN
        if self.phase == 'particle':
            status = "PHASE 2: OBSERVER ACTIVE (PARTICLE)"
            col = PARTICLE_GOLD
            
        ax.text(0, -9.5, status, color=col, ha='center', fontfamily='monospace', fontsize=14,
               bbox=dict(facecolor='black', edgecolor=col))
               
        # Legend
        ax.text(-9, 9, "DETECTOR SCREEN", color=SCREEN_GREEN, fontsize=8)

        ax.set_axis_off()
        
        out_dir = "logic_garden_observer_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"obs_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Collapsing Wave Functions...")
    
    sim = QuantumSim()
    
    for i in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(12, 12), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        sim.update(i)
        sim.render(i, ax)
        plt.close()
        
        if i % 30 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
