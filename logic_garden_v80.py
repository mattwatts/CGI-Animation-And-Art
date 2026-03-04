"""
SOVEREIGN CODE: logic_garden_v50_phasedarray_short.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: Signal Processing / Radar
STATUS: REFACTORED (Vertical Beam Steering)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_v50_short"
os.makedirs(OUT_DIR, exist_ok=True)

# Grid for field calculation
X = np.linspace(-9, 9, 100)
Y = np.linspace(-16, 16, 200)
XX, YY = np.meshgrid(X, Y)

# Emitter Positions (Bottom Array)
N_EMITTERS = 8
wavelength = 2.0
k = 2 * np.pi / wavelength
omega = 1.0
emitter_x = np.linspace(-4, 4, N_EMITTERS)
emitter_y = -12.0 # Bottom of screen

def calculate_field(t, steering_angle):
    # Calculate Phase Shift per element to steer beam
    # d * sin(theta)
    # phase_shift = k * x * sin(theta)
    
    field = np.zeros_like(XX)
    
    for i, ex in enumerate(emitter_x):
        # Distance from emitter to every point
        dist = np.sqrt((XX - ex)**2 + (YY - emitter_y)**2)
        
        # Phasing logic
        # To steer to theta, element i needs phase shift:
        phase_i = -k * ex * np.sin(steering_angle)
        
        # Wave equation: A * sin(kr - wt + phase)
        # Using 1/r dropoff for realism? No, keeping it clean for viz.
        field += np.sin(k * dist - omega * t + phase_i)
        
    return field

def run():
    print("LOGIC GARDEN 50: PHASED ARRAY (VERTICAL)")
    fig = plt.figure(figsize=(9, 16), facecolor='#000000')
    ax = fig.add_axes([0, 0, 1, 1], facecolor='#000000') # Full bleed
    
    for f in range(TOTAL_FRAMES):
        ax.clear()
        ax.set_xlim(-9, 9)
        ax.set_ylim(-16, 16)
        ax.axis('off')
        
        # BEAM LOGIC
        # Sweep from -30 deg to +30 deg
        # Slow sweep
        sweep_speed = 0.05
        steering_angle = np.sin(f * 0.02) * (np.pi / 4) # +/- 45 degrees
        
        # 1. COMPUTE FIELD (Heavy Lift)
        # Low res for speed, mapped to image
        Z = calculate_field(f * 0.5, steering_angle)
        
        # 2. RENDER HEATMAP
        # Vmin/Vmax controls contrast
        # We want strict interference patterns (Mojave/Matrix aesthetic)
        # Green map
        ax.imshow(Z, extent=[-9, 9, -16, 16], origin='lower', 
                  cmap='gist_ncar', vmin=-N_EMITTERS, vmax=N_EMITTERS, alpha=0.9)
        
        # 3. DRAW EMITTERS (Hardware)
        ax.scatter(emitter_x, [emitter_y]*N_EMITTERS, color='white', s=50, zorder=10)
        
        # 4. DRAW TARGET (Red)
        # Show where the beam is pointing
        target_x = 10 * np.sin(steering_angle)
        target_y = emitter_y + 10 * np.cos(steering_angle)
        
        # Beam Line overlay
        ax.plot([0, target_x], [emitter_y, target_y], color='white', linestyle='--', alpha=0.5)
        
        # HUD
        deg = np.degrees(steering_angle)
        ax.text(0, -14, "PHASED ARRAY", color='white', ha='center', fontsize=20, weight='bold', fontfamily='monospace')
        ax.text(0, -15, f"STEERING: {deg:.1f}°", color='#00FF00', ha='center', fontsize=18, fontfamily='monospace', bbox=dict(facecolor='black', alpha=0.5))
        
        # Explain the Pop
        if abs(deg) < 5:
            ax.text(0, 12, "MAXIMUM SIGNAL", color='white', ha='center', fontsize=25, weight='bold', fontfamily='monospace')
        elif abs(deg) > 30:
            ax.text(0, 12, "OFF-BORESIGHT", color='#FFFF00', ha='center', fontsize=20, fontfamily='monospace')

        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=80, facecolor='#000000') # DPI 80 for speed
        
    plt.close(fig)

if __name__ == "__main__": run()
