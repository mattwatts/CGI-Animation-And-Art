"""
LOGIC GARDEN 203: THE BARIUM TENSOR (Carter's Anomaly)
Target: YouTube Shorts (1080x1920)
FPS: 60 
Duration: 20 seconds (1200 frames)
Engine: Decoupled Operations Research (PNG Array -> FFmpeg)
Topic: Barium Cloud Resonance Scattering (Eglin WSW to Leary, GA - 152km Altitude)
"""

import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba

# =============================================================================
# COMPILE-TIME SAFETY & INDUSTRIAL PALETTE
# =============================================================================
np.random.seed(1969)  # Deterministic seed based on the event year

C_VOID = '#000000'
C_CYAN = '#00FFFF'     # Neutral Barium (455.4 nm)
C_MANTIS = '#39FF14'   # Visual Pop / Terminal Green Truth
C_MAGENTA = '#FF00FF'  # Ionized Barium Drift (Ba+)
C_RED = '#FF0000'      # Deep Ionized Edge
C_TEXT = '#FFFFFF'     # UI Overlay
C_GOLD = '#FFD700'     # Target Lock / Crosshairs

FPS = 60
TOTAL_FRAMES = 1200
N_NODES = 35000  # High-density fluid swarm

rgba_void = np.array(to_rgba(C_VOID))
rgba_cyan = np.array(to_rgba(C_CYAN))
rgba_magenta = np.array(to_rgba(C_MAGENTA))
rgba_red = np.array(to_rgba(C_RED))
rgba_mantis = np.array(to_rgba(C_MANTIS))

# =============================================================================
# TOPOLOGICAL ARCHITECTURE (THE BARIUM CLOUD)
# =============================================================================
# All particles start packed in exactly the payload vector
# Viewport: Ground level at Leary GA, looking WSW, 33 degree elevation. 
# We treat the screen as the 2D projected observation boundary.

X = np.zeros(N_NODES, dtype=np.float32)
Y = np.zeros(N_NODES, dtype=np.float32)

# Kinematics Arrays
# Theta determines radial expansion, speed is Gaussian
theta = np.random.uniform(0, 2 * np.pi, N_NODES)
speed = np.random.normal(0.05, 0.02, N_NODES)

VX = np.cos(theta) * speed
VY = np.sin(theta) * speed * 0.8  # Slight vertical compression in projection

# State Matrix: 0 = Payload, 1 = Neutral (Cyan), 2 = Ionized (Magenta drift)
state = np.zeros(N_NODES, dtype=np.int8)

# Color Matrix initialized to VOID (Invisible before 152km detonation)
colors = np.tile(rgba_void, (N_NODES, 1))

# Starfield (Static Background Context)
N_STARS = 150
star_x = np.random.uniform(-10, 10, N_STARS)
star_y = np.random.uniform(-15, 15, N_STARS)

# =============================================================================
# RENDER ENVIRONMENT (DECOUPLED 2000x2000 PIPELINE)
# =============================================================================
fig, ax = plt.subplots(figsize=(20, 20), dpi=100, facecolor=C_VOID)
ax.set_facecolor(C_VOID)
ax.axis('off')
ax.set_xlim([-10, 10])
ax.set_ylim([-15, 15])  # Enforce vertical aspect ratio framing

# Render Starfield (O(1) Static Layer)
ax.scatter(star_x, star_y, s=2.0, color='#555577', alpha=0.5, edgecolors='none')

# Render Barium Payload Tensor
init_sizes = np.full(N_NODES, 1.0)
scatter = ax.scatter(X, Y, c=colors, s=init_sizes, alpha=0.4, edgecolors='none')

# The Industrialist Telemetry Widgets (HUD)
# Bounding Box coordinates indicating Ground Sensor truth vs Reality Truth
hud_text = ax.text(-9.5, 13.5, "", color=C_CYAN, fontfamily='monospace', fontsize=24)
hud_zen = ax.text(-9.5, -14.0, "", color=C_MANTIS, fontfamily='monospace', fontsize=28, weight='bold')

# Crosshairs (Analytical Bounding)
cross_h = ax.axhline(y=0, color=C_TEXT, alpha=0.0, lw=1, ls='--')
cross_v = ax.axvline(x=0, color=C_TEXT, alpha=0.0, lw=1, ls='--')

# =============================================================================
# RUNTIME LOGIC / OPTIMAL ALGORITHMIC FLOW
# =============================================================================
def compute_frame_logic(frame):
    global X, Y, VX, VY, state, colors
    
    # PHASE 1: Payload Ascent (0 - 150)
    # The payload is climbing to 152km, invisible in the dark sky until twilight threshold
    if frame < 150:
        hud_text.set_text(f"SENSOR: CIVILIAN OBSERVER (LEARY, GA)\nAZIMUTH: WSW\nELEVATION: 33 DEG\nALTITUDE: {(frame/150)*152:.1f} KM\nSTATUS: ASCENT (DARK)")
        pass

    # PHASE 2: Detonation & Neutral Expansion (Resonance Scattering)
    if frame == 150:
        state[:] = 1
        colors[:] = rgba_cyan
        hud_text.set_text(f"SENSOR: CIVILIAN OBSERVER\nALTITUDE: 152.0 KM\nSTATUS: PAYLOAD DETONATION\nRESONANCE: NEUTRAL Ba (455.4 nm)")
    
    if 150 <= frame < 900:
        # Radial Thermal Expansion
        X += VX
        Y += VY
        
        # Sizing scales up to simulate "glow volume taking size of the moon"
        current_size = min(35.0, 1.0 + ((frame - 150) * 0.05))
        scatter.set_sizes(np.full(N_NODES, current_size))
        
        # PHASE 3: UV Ionization & Magnetic Drift
        if frame > 300:
            hud_text.set_text(f"SENSOR: CIVILIAN OBSERVER\nALTITUDE: 152.0 KM\nSTATUS: SOLAR UV BOMBARDMENT\nRESONANCE: Ba+ IONIZATION DRIFT")
            
            # Probability cascade: Solar UV ionizes particles over time
            # Once ionized, they align with the Earth's magnetic field lines (pulling diagonal Up-Right)
            ion_chance = 0.005 # Operations Research probabilistic mapping
            new_ions = (np.random.random(N_NODES) < ion_chance) & (state == 1)
            state[new_ions] = 2
            
            # The Magnetic Drift Vector (O(1) Override)
            VX[state == 2] += 0.008  # Drift Right
            VY[state == 2] += 0.015  # Spallation Upwards
            
            # Color transition (Cyan -> Magenta -> Red edge)
            colors[state == 2] = rgba_magenta
            
            # Edge of the drift bleeds into red friction
            deep_ions = (state == 2) & (Y > 3.0)
            colors[deep_ions] = rgba_red
            
            # Crosshairs fade in to indicate tracking
            cross_h.set_alpha(min(0.5, (frame - 300)*0.01))
            cross_v.set_alpha(min(0.5, (frame - 300)*0.01))

    # PHASE 4: THE ZEN REALIZATION (TATHĀTĀ) / HARDWARE INTERRUPT (900+)
    if frame >= 900:
        hud_text.set_text(f"ARCHITECTURE LOCKED.\nDIMENSIONAL COMPILER RESET.\nTHE TENSOR IS A MATHEMATICAL FLUID.\nC_MANTIS OVERRIDE.")
        hud_text.set_color(C_MANTIS)
        
        cross_h.set_color(C_MANTIS)
        cross_h.set_alpha(0.8)
        cross_v.set_color(C_MANTIS)
        cross_v.set_alpha(0.8)
        
        hud_zen.set_text("TATHĀTĀ: MAGIC IS SIMPLY PHYSICS WE\nHAVE NOT YET COMPILED.")
        
        # Phase coherence - lock everything into terminal green wireframe proxy
        colors[:] = rgba_mantis
        
        # Stop physics simulation to force the "Compile-Time Safety" freeze
        VX[:] = 0
        VY[:] = 0

    scatter.set_offsets(np.c_[X, Y])
    scatter.set_facecolors(colors)

# =============================================================================
# BATCH EXECUTION & FFMPEG COMPILATION
# =============================================================================
if __name__ == '__main__':
    OUTPUT_DIR = "logic_garden_203_frames"
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print(f"Initiating Array Rendering Engine -> {OUTPUT_DIR}/")
    print("Simulating Target: 1200 Frames (20.0s @ 60FPS) in 2000x2000 PNG")
    
    for frame in range(TOTAL_FRAMES):
        compute_frame_logic(frame)
        filepath = os.path.join(OUTPUT_DIR, f"frame_{frame:04d}.png")
        plt.savefig(filepath, facecolor=C_VOID, edgecolor='none', bbox_inches='tight', pad_inches=0)
        
        if frame % 60 == 0:
            print(f"Rendered: {frame}/{TOTAL_FRAMES} frames ({(frame/TOTAL_FRAMES)*100:.1f}%)")
            
    print(f"\nTerminal Green. Frame extraction complete.")
    print("\n[EXECUTE THIS COMMAND IN YOUR SHELL TO DEPLOY FORCEBOX PROTOCOL:]")
    print("-" * 80)
    print("ffmpeg -y -framerate 60 -i logic_garden_203_frames/frame_%04d.png -vf \"scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1\" -c:v libx264 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 LG_203_THE_BARIUM_TENSOR.mp4")
    print("-" * 80)
