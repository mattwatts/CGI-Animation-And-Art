"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v62.py
MODE:   Nursery (Quantum Palette)
TARGET: Wave-Particle Duality (Gaussian Packet)
STYLE:  "The Breathing Point" | 40s Deep Time | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# --- 1. THE QUANTUM PALETTE ---
BG_VOID = "#050510"
WAVE_CYAN = "#00FFFF"       # The Oscillation
PROB_MAGENTA = "#FF00FF"    # The Envelope
REALITY_WHITE = "#FFFFFF"   # The Dot
AXIS_GREY = "#303030"

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 40
TOTAL_FRAMES = FPS * DURATION
RES_X = 1920
RES_Y = 1080

class WavePacketSim:
    def __init__(self):
        # Space
        self.x = np.linspace(-10, 50, 2000)
        
        # Packet Properties
        self.k0 = 5.0      # Wavenumber (Momentum)
        self.v = 1.0       # Group Velocity
        self.sigma0 = 2.0  # Initial Width
        
        # Particle State (The "Surfer")
        self.particle_x = 0.0
        
    def wave_function(self, t):
        # Standard Gaussian Packet with Dispersion
        # Width grows over time: sigma(t) = sigma0 * sqrt(1 + t^2)
        # Simplified dispersion math for visual clarity
        
        dispersion_rate = 0.05
        sigma_t = self.sigma0 * (1.0 + dispersion_rate * t)
        
        # Center moves
        x_c = self.v * t
        
        # 1. The Gaussian Envelope (Amplitude)
        # Normalized roughly for visuals
        envelope = np.exp(-0.5 * ((self.x - x_c)**2) / (sigma_t**2))
        
        # 2. The Carrier Wave (Oscillation)
        # Phase velocity is different from group velocity in dispersive media
        # but here we keep it simple: cos(k(x-vt))
        carrier = np.cos(self.k0 * (self.x - x_c) - 2.0 * t) 
        # Note: Added extra time term to make carrier flow through envelope
        
        # The Wave
        psi_real = envelope * carrier
        
        # The Probability Density (Envelope Squared)
        prob_density = envelope**2
        
        return x_c, sigma_t, psi_real, prob_density

    def render(self, frame_idx, ax):
        ax.set_xlim(0, 40)
        ax.set_ylim(-1.5, 2.0)
        
        # Physics Time
        t = frame_idx * 0.05
        
        x_c, sigma_t, psi, prob = self.wave_function(t)
        
        # 1. DRAW PROBABILITY ENVELOPE (The Ghost)
        # Filled area
        ax.fill_between(self.x, prob, color=PROB_MAGENTA, alpha=0.2, zorder=1)
        ax.plot(self.x, prob, color=PROB_MAGENTA, linewidth=2, alpha=0.8, linestyle="--", label="PROBABILITY")
        
        # 2. DRAW WAVE FUNCTION (The Ripple)
        ax.plot(self.x, psi, color=WAVE_CYAN, linewidth=1.5, alpha=0.9, label="WAVE FUNCTION (REAL)")
        
        # 3. DRAW THE PARTICLE (The Fact)
        # The particle jitters inside the probability cloud based on Heisenberg
        # Simulation: Pick a random X weighted by Prob?
        # For smooth animation, we use a Perlin-like walk inside the envelope
        
        # Deterministic Jitter
        jitter = np.sin(t * 13.0) * np.cos(t * 7.0) * sigma_t * 0.8
        p_x = x_c + jitter
        p_y = psi[np.abs(self.x - p_x).argmin()] # Ride the wave height
        
        # Pulse size
        pulse = 100 + 50 * np.sin(t * 10)
        
        ax.scatter([p_x], [p_y], color=REALITY_WHITE, s=pulse, zorder=10, edgecolors=WAVE_CYAN)
        ax.scatter([p_x], [p_y], color=REALITY_WHITE, s=pulse*3, alpha=0.1, zorder=9)
        
        # 4. HUD elements
        ax.axhline(0, color=AXIS_GREY, linewidth=1)
        
        # Vertical markers for spread (Uncertainty)
        ax.plot([x_c - sigma_t, x_c - sigma_t], [-0.2, 0.2], color="white", linewidth=1)
        ax.plot([x_c + sigma_t, x_c + sigma_t], [-0.2, 0.2], color="white", linewidth=1)
        ax.text(x_c, -0.4, f"UNCERTAINTY $\Delta x$: {sigma_t*2:.2f}", color="white", ha='center', fontsize=10, fontfamily='monospace')

        # Header
        ax.text(2, 1.8, "LOGIC GARDEN 62: THE BREATHING POINT", color=WAVE_CYAN, fontsize=14, fontweight='bold', fontfamily='monospace')
        
        # Equation
        eq = r"$\Psi(x) = \text{Envelope} \times \cos(kx)$"
        ax.text(2, 1.6, eq, color=PROB_MAGENTA, fontsize=12)

        ax.set_axis_off()
        ax.set_facecolor(BG_VOID)
        
        # Save
        out_dir = "logic_garden_wavepacket_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"wave_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_VOID)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print(f"[NURSERY] Collapsing the Wavefunction...")
    
    sim = WavePacketSim()
    
    for i in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(12, 6), dpi=100) # Wide aspect
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_VOID)
        
        sim.render(i, ax)
        plt.close()
        
        if i % 60 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
