"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v58.py
MODE:   Nursery (Manhattan Palette)
TARGET: Hydrodynamic Shockwave Lensing
STYLE:  "The Implosion Lens" | 40s Deep Time | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Polygon
import os

# --- 1. THE MANHATTAN PALETTE ---
BG_VOID = "#101010"         # The Lab
EX_FAST = "#FF8C00"         # Composition B
EX_SLOW = "#F0E68C"         # Baratol
SHOCK_CYAN = "#00FFFF"      # The Wavefront
TAMPER_COL = "#2F4F4F"      # Natural Uranium
PUSHER_COL = "#A9A9A9"      # Aluminum
CORE_GREY = "#778899"       # Pu-239
CRITICAL_WHITE = "#FFFFFF"

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 40
TOTAL_FRAMES = FPS * DURATION

class ShockPoint:
    def __init__(self, angle):
        self.angle = angle
        self.r = 9.0 # Start outer radius
        self.speed = 0.0 # m/s (simulated units)
        self.active = False
        
    def update(self, r_fast_inner, r_slow_inner):
        # Hydrodynamic Logic
        # 1. Fast Explosive Zone (Radius 9 -> 7)
        if self.r > 7.0:
            self.speed = 0.08 # Fast
        # 2. Slow Explosive Zone (Radius 7 -> 4)
        elif self.r > 4.0:
            # HERE IS THE LENSING
            # The geometry of the Baratol lens is thicker in the middle (at the detonator angle)
            # and thinner at the edges.
            # We simulate refraction by varying speed based on angle relative to lens center
            self.speed = 0.05 # Slow base
        # 3. Free Air / Tamper (Radius 4 -> 0)
        else:
            self.speed = 0.1 # Very Fast (Metal shock)
            
        self.r -= self.speed

class ImplosionSim:
    def __init__(self):
        # Geometry
        self.num_lenses = 12 # Visual cross section (real is 32)
        self.shockwaves = []
        
        # Core State
        self.core_r = 1.5
        self.core_density_color = 0.0 # 0=Grey, 1=White
        self.is_critical = False
        self.shock_radius_visual = 9.0
        
        # Lens Geometry
        self.lens_angles = np.linspace(0, 2*np.pi, self.num_lenses, endpoint=False)
        
    def update(self, frame_idx):
        # SEQUENCE
        
        # 1. IGNITION (2-5s)
        if frame_idx == 60:
            print("  > DETONATION")
        
        # 2. TRANSIT (5-30s)
        # We simulate the wavefront as a continuous curve
        # r(theta)
        
        # Normalized time for shock travel
        # Starts at t=0 (frame 60)
        # Hits core at t=1 (frame 900)
        
        if frame_idx > 60 and frame_idx < 900:
            prog = (frame_idx - 60) / 840.0
            
            # THE LENS CALCULATION
            # We want to show Convex -> Concave
            
            current_r = 9.0 * (1.0 - prog * 0.8) # Main contracting radius
            
            # Perturbation (The Shape Error)
            # Early on (prog < 0.5), the wave is Convex (bumpy) around detonators
            # Later (prog > 0.5), the lens smooths it out
            
            distortion_mag = 0.5 * (1.0 - prog*1.5) # Distortion fades
            if distortion_mag < 0: distortion_mag = 0
            
            self.shock_radius_visual = current_r
            self.current_distortion = distortion_mag
            
        # 3. COMPRESSION (30s+)
        if frame_idx >= 900:
            # Impact!
            compress_prog = min(1.0, (frame_idx - 900) / 200.0)
            
            # Core shrinks
            self.core_r = 1.5 * (1.0 - compress_prog * 0.5) # Shrink to half size
            
            # Color shifts to white
            self.core_density_color = compress_prog
            
            self.shock_radius_visual = self.core_r # Shock stays on surface crushing it

    def render(self, frame_idx, ax):
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        
        # --- DRAW THE BOMB LAYERS ---
        
        # Layer 1: Outer Casing (Outline)
        ax.add_patch(Circle((0,0), 9.2, fill=False, edgecolor="#404040", linewidth=2))
        
        # Layer 2: Fast Explosive (Comp B) - The "Matrix"
        ax.add_patch(Circle((0,0), 9.0, color=EX_FAST, zorder=1))
        
        # Layer 3: Slow Explosive (Baratol) - The "Lenses"
        # These are scooped out shapes inside the Fast Explosive
        # In this simplified visuals, we draw them as wedges/circles
        # Baratol Lenses are shaped to focus the wave.
        # They sit "inside" the fast explosive.
        
        for angle in self.lens_angles:
            # Calculate position of lens center
            # Lenses are arranged radially
            lx = 6.0 * np.cos(angle)
            ly = 6.0 * np.sin(angle)
            
            # Draw Baratol shapes (Curved)
            gw_width = (2*np.pi / self.num_lenses) * 57.29 # Degrees
            
            w = Wedge((0,0), 7.0, np.degrees(angle)-gw_width/2, np.degrees(angle)+gw_width/2, width=3.0, color=EX_SLOW, zorder=2)
            ax.add_patch(w)
            
            # Detonators (Sparks)
            dx = 9.0 * np.cos(angle)
            dy = 9.0 * np.sin(angle)
            if frame_idx > 60:
                ax.add_patch(Circle((dx, dy), 0.2, color="white", zorder=10))
            
            # Wiring
            ax.plot([dx, dx*1.1], [dy, dy*1.1], color="#505050", linewidth=1)

        # Layer 4: Pusher / Tamper (The Barrier)
        # Inner Circle
        ax.add_patch(Circle((0,0), 3.5, color=PUSHER_COL, zorder=3))
        # Uranium Tamper
        ax.add_patch(Circle((0,0), 2.5, color=TAMPER_COL, zorder=4))
        
        # --- DRAW THE CORE ---
        # Plutonium
        # Color interpolation
        c_val = self.core_density_color
        # Blend Grey to White/Blue
        # Grey: (0.47, 0.53, 0.6)
        # White: (1, 1, 1)
        
        r = 0.47 + (1.0 - 0.47)*c_val
        g = 0.53 + (1.0 - 0.53)*c_val
        b = 0.60 + (1.0 - 0.60)*c_val
        
        if c_val > 0.9: # Blue tint for criticality
             b = 1.0; r = 0.8; g = 0.9
             
        core_col = (r, g, b)
        
        ax.add_patch(Circle((0,0), self.core_r, color=core_col, zorder=5))
        
        # The Urchin (Initiator)
        if frame_idx < 950:
            ax.add_patch(Circle((0,0), 0.2, color="gold", zorder=6))

        # --- DRAW THE SHOCKWAVE ---
        if frame_idx > 60 and frame_idx < 950:
            # Construct the wave curve
            thetas = np.linspace(0, 2*np.pi, 360)
            
            # Visual Radius with distortion
            # Distortion makes it bulge OUT at the detonators initially (Convex)
            # Then smooths out.
            
            # Modulate radius
            # We use cos(N * theta) to create the bumps matching lenses
            modulation = np.cos(self.num_lenses * (thetas - self.lens_angles[0])) # Phase align
            
            r_wave = self.shock_radius_visual + (modulation * self.current_distortion)
            
            wx = r_wave * np.cos(thetas)
            wy = r_wave * np.sin(thetas)
            
            ax.plot(wx, wy, color=SHOCK_CYAN, linewidth=2, zorder=20)
            # Glow
            ax.plot(wx, wy, color=SHOCK_CYAN, linewidth=6, alpha=0.3, zorder=19)

        # FLASH (Whitout at end)
        if frame_idx > 1100:
            alpha = (frame_idx - 1100) / 100.0
            rect = plt.Rectangle((-10,-10), 20, 20, color="white", alpha=alpha, zorder=100)
            ax.add_patch(rect)

        # HUD
        if frame_idx < 60:
            lbl = "STATUS: ARMED (SUB-CRITICAL)"
            col = "#808080"
        elif frame_idx < 900:
            lbl = f"STATUS: SHOCK TRANSIT (LENSING)"
            col = SHOCK_CYAN
        elif frame_idx < 1100:
            lbl = "STATUS: COMPRESSION (SUPER-CRITICAL)"
            col = "white"
        else:
            lbl = "STATUS: CRITICALITY REACHED"
            col = "black"

        ax.text(0, 9.2, lbl, color=col, ha='center', fontfamily='monospace', fontsize=14, fontweight='bold',
                bbox=dict(facecolor='black', edgecolor=col, zorder=90), zorder=91)

        # Labels
        # Right aligned Labels
        if frame_idx < 900:
            ax.text(9.5, 7, "FAST EXP (COMP B)", color=EX_FAST, ha='right', fontsize=8, fontweight='bold')
            ax.text(9.5, 5, "SLOW EXP (BARATOL / LENS)", color=EX_SLOW, ha='right', fontsize=8, fontweight='bold')
            ax.text(9.5, 3, "PUSHER (AL)", color=PUSHER_COL, ha='right', fontsize=8, fontweight='bold')
            
        # Core Density HUD
        dens = 1.0 + self.core_density_color * 1.0 # 1x to 2x
        ax.text(-9.5, -9, f"CORE DENSITY: {dens:.2f}x", color=core_col, ha='left', fontfamily='monospace', fontsize=12)

        ax.set_aspect('equal')
        ax.set_axis_off()
        
        out_dir = "logic_garden_implosion_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"implosion_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_VOID)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print(f"[NURSERY] Arming Implosion Device...")
    
    sim = ImplosionSim()
    
    for i in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10, 10), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_VOID)
        
        sim.update(i)
        sim.render(i, ax)
        plt.close()
        
        if i % 60 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
