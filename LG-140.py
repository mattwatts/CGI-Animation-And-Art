"""
LOGIC GARDEN 141: VELVET ENGINE v2 (PURE ENTRAINMENT)
Target: YouTube Shorts (1080x1920)
FPS: 21 (Absolute Orthogonal Binding to 126 BPM)
Duration: 28.5 seconds (600 frames, seamless loop structure)
Compile-Time Setup: numpy, matplotlib, ffmpeg

FFMPEG PROTOCOL (FORCEBOX):
ffmpeg -i output.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1" -color_primaries bt709 -c:a copy LG_141_VELVET.mp4
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

# =============================================================================
# COMPILE-TIME SAFETY & INDUSTRIAL PALETTE
# =============================================================================
np.random.seed(126) # Seed locked to the Green Velvet Grid (BPM)

C_VOID = '#000000'
C_CYAN = '#00FFFF'     # High-Voltage Wireframes (Outer Delta)
C_MANTIS = '#39FF14'   # The Silent Sentinel (Mid Theta)
C_RED = '#FF0033'      # Entropy / The Drop (Inner Core)

FPS = 21
DURATION = 28.57
TOTAL_FRAMES = 600

# =============================================================================
# THE ARCHITECTURE (POLAR MANDALA -> 3D PROJECTION)
# =============================================================================
# 3 concentric infrastructural rings scaled to fill a 9:16 vertical viewport
num_points = 320
theta = np.linspace(0, 2*np.pi, num_points)

# Ring 1: Delta Band (Kick - Outer) -> Pushed to the very edges of the X-axis
r_delta = np.full(num_points, 11.0)
x_delta, y_delta = r_delta * np.cos(theta), r_delta * np.sin(theta)

# Ring 2: Theta Band (Hi-Hat - Mid)
r_theta = np.full(num_points, 7.5)
x_theta, y_theta = r_theta * np.cos(theta), r_theta * np.sin(theta)

# Ring 3: The Core (Inner)
r_core = np.full(num_points, 3.0)
x_core, y_core = r_core * np.cos(theta), r_core * np.sin(theta)

# Flatten for O(1) scatter matrix array operations
X = np.concatenate([x_delta, x_theta, x_core])
Y = np.concatenate([y_delta, y_theta, y_core])
Z = np.zeros_like(X)

# Assign initial sizes and colors
sizes = np.full(len(X), 35.0) # Base size massively scaled for screen fill
base_colors = np.array([C_CYAN] * num_points + [C_MANTIS] * num_points + [C_RED] * num_points)
colors = base_colors.copy()

# =============================================================================
# ENVIRONMENTAL SETUP (1080x1920 SHORTS FORMAT)
# =============================================================================
# Absolute Black / Void initialization
fig = plt.figure(figsize=(10.8, 19.2), dpi=100, facecolor=C_VOID)
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor(C_VOID)

# Erase structural formatting to isolate the geometry
ax.xaxis.pane.fill = False; ax.yaxis.pane.fill = False; ax.zaxis.pane.fill = False
ax.axis('off')

# Viewport tightened aggressively to force the mandala into full screen
ax.view_init(elev=20, azim=45)
ax.set_xlim([-11.5, 11.5])
ax.set_ylim([-11.5, 11.5])
ax.set_zlim([-15, 15]) # Expanded Z-axis allows waves to explode upward in 9:16

# NEON POP PROTOCOL: Dual-layer scatter
scatter_glow = ax.scatter(X, Y, Z, c=colors, s=sizes*8, alpha=0.15, depthshade=False)
scatter_core = ax.scatter(X, Y, Z, c=colors, s=sizes, alpha=0.9, depthshade=True)

# =============================================================================
# RUNTIME EXECUTION (PROTOCOL: CRITICAL DAMPING)
# =============================================================================
def animate(frame):
    global Z, sizes, colors
    
    # 1. SWEEPING ROTATION (Continuous Kinetic Flow)
    rot_t = frame * 0.12 # Slow, heavy mechanical rotation
    ax.view_init(elev=20 + np.sin(frame*0.05)*5, azim=45 + rot_t)
    
    # 2. ORTHOGONAL BINDING: 126 BPM MATHEMATICAL LOCK
    # Frame % 10 == 0 -> The 2.1 Hz Kick Drum
    kick_frame = frame % 10
    kick_amplitude = 8.0 * np.exp(-kick_frame * 0.25) # Critical Damping
    
    # Frame % 5 == 0 -> The 4.2 Hz Hi-Hat
    hat_frame = frame % 5
    hat_amplitude = 4.0 * np.exp(-hat_frame * 0.4)
    
    # 3. Z-AXIS DISPLACEMENT (The Architecture Breathes)
    # Aggressive vertical scaling to utilize the 1920 height
    Z[:num_points] = np.sin(theta * 5 + rot_t) * kick_amplitude * 1.5              # Delta Array
    Z[num_points:num_points*2] = np.cos(theta * 3 - rot_t * 1.5) * hat_amplitude   # Theta Array
    Z[num_points*2:] = np.sin(theta * 2 + rot_t*3) * (kick_amplitude * 0.8 + 2.0)  # Core
    
    # 4. NEON POP SCATTER SCALING (Massive pulses on the drop)
    sizes[:num_points] = 30.0 + (kick_amplitude * 45.0)
    sizes[num_points:num_points*2] = 20.0 + (hat_amplitude * 35.0)
    sizes[num_points*2:] = 40.0 + (np.sin(frame*0.2)*15.0)
    
    # 5. PHASE-TRANSITION (The Algorithmic Drop Sequence)
    # At frame 300, the system hits peak load and reverses color matrices
    if 300 <= frame < 450:
        if kick_frame < 2:
            colors[:num_points] = C_RED # Delta ring flashes Entropy Red on the kick
        else:
            colors[:num_points] = C_CYAN
            
        if hat_frame < 1:
            colors[num_points:num_points*2] = C_CYAN # Theta ring flashes Cyan
        else:
            colors[num_points:num_points*2] = C_MANTIS
    else:
        # Reset to base schema
        colors = base_colors.copy()

    # 6. RENDER COMMIT
    scatter_core._offsets3d = (X, Y, Z)
    scatter_core.set_sizes(sizes)
    scatter_core.set_color(colors)
    
    scatter_glow._offsets3d = (X, Y, Z)
    scatter_glow.set_sizes(sizes * 8)
    scatter_glow.set_color(colors)

    return scatter_core, scatter_glow

# =============================================================================
# BATCH EXECUTION
# =============================================================================
print("Initiating full-screen optical execution... 126 BPM strict alignment.")
ani = FuncAnimation(fig, animate, frames=TOTAL_FRAMES, interval=1000/FPS, blit=False)

writer = FFMpegWriter(fps=FPS, metadata=dict(artist='The Industrialist'), bitrate=24000)
ani.save('LG_141_VELVET_SHORTS.mp4', writer=writer)
print("Terminal Green. Architecture closed. File output: LG_141_VELVET_SHORTS.mp4")
