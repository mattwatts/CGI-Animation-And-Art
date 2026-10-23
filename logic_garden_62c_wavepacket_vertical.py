"""
UNE DEEP RESEARCH PROTOCOL v3.1 - SOVEREIGN CODE
SCRIPT: logic_garden_62c_wavepacket_vertical.py
MODE:   Nursery (Quantum Palette)
TARGET: Wave-Particle Duality (Gaussian Packet / Centred)
STYLE:  "The Breathing Point" | 40s Deep Time | 60 FPS | 9:16 Vertical

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
FPS = 60  # [HOTFIX] Elevated to 60 FPS
DURATION = 40
TOTAL_FRAMES = FPS * DURATION
RES_X = 1080  # Format Shift
RES_Y = 1920

class WavePacketSim:
    def __init__(self):
        # Space [HOTFIX: Expanded to cover extensive horizontal limits over 40s tracking]
        self.x = np.linspace(-50, 150, 10000)
        
        # Packet Properties
        self.k0 = 5.0      # Wavenumber (Momentum)
        self.v = 1.0       # Group Velocity
        self.sigma0 = 2.0  # Initial Width
        
        # Particle State (The "Surfer")
        self.particle_x = 0.0
        
    def wave_function(self, t):
        # Standard Gaussian Packet with Dispersion
        # Width grows over time: sigma(t) = sigma0 * sqrt(1 + t^2)
        # Simplified dispersion maths for visual clarity
        
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
        # Physics Time [HOTFIX: Scaled down strictly to preserve original simulation speed at 60fps]
        t = frame_idx * 0.025 
        
        x_c, sigma_t, psi, prob = self.wave_function(t)
        
        # [HOTFIX] Absolute Viewport Centring
        # By setting the camera to exactly track x_c, the packet remains dead-centre.
        cam_span_x = 12.0
        ax.set_xlim(x_c - cam_span_x, x_c + cam_span_x)
        # Bounding the vertical limits explicitly for the 9:16 layout
        ax.set_ylim(-2.5, 3.5)
        
        # 1. DRAW PROBABILITY ENVELOPE (The Ghost)
        # Filled area
        ax.fill_between(self.x, prob, color=PROB_MAGENTA, alpha=0.2, zorder=1)
        ax.plot(self.x, prob, color=PROB_MAGENTA, linewidth=2, alpha=0.8, linestyle="--", label="PROBABILITY")
        
        # 2. DRAW WAVE FUNCTION (The Ripple)
        ax.plot(self.x, psi, color=WAVE_CYAN, linewidth=1.5, alpha=0.9, label="WAVE FUNCTION (REAL)")
        
        # 3. DRAW THE PARTICLE (The Fact)
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
        ax.plot([x_c - sigma_t, x_c - sigma_t], [-0.5, 0.5], color="white", linewidth=1)
        ax.plot([x_c + sigma_t, x_c + sigma_t], [-0.5, 0.5], color="white", linewidth=1)
        
        # HUD text explicitly bolted to the tracking coordinates
        ax.text(x_c, -1.5, f"UNCERTAINTY \u0394x: {sigma_t*2:.2f}", color="white", ha='center', fontsize=16, fontfamily='monospace')

        # Header bolted proportionally left of frame centre
        ax.text(x_c - cam_span_x * 0.9, 3.1, "LG-62c: THE BREATHING POINT", color=WAVE_CYAN, fontsize=18, fontweight='bold', fontfamily='monospace')
        
        # Equation
        eq = r"$\Psi(x) = \text{Envelope} \times \cos(kx)$"
        ax.text(x_c - cam_span_x * 0.9, 2.7, eq, color=PROB_MAGENTA, fontsize=16)

        ax.set_axis_off()
        ax.set_facecolor(BG_VOID)
        
        # Save
        out_dir = "frames_62c_wavepacket_vertical"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"wave_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_VOID)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print(f"[NURSERY] Collapsing the Wavefunction (60FPS / Centred Track)...")
    
    sim = WavePacketSim()
    
    for i in range(TOTAL_FRAMES):
        # HOTFIX: Explicitly mapping absolute 1080x1920 (9:16) proportional canvas
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100) 
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_VOID)
        
        sim.render(i, ax)
        plt.close()
        
        if i % 60 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
