import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# GURRGIYN: SHORT FORMAT RENDER ENGINE (1080x1920)
# ==========================================

# 1. Directory Janitorial Work
OUTPUT_DIR = "frames"
os.makedirs(OUTPUT_DIR, exist_ok=True)
print(f"[*] Provisioning output directory: ./{OUTPUT_DIR}/")

# 2. Canvas Topology (1080x1920 @ 100 DPI)
# 10.8 * 100 = 1080px Width | 19.2 * 100 = 1920px Height
fig, ax = plt.subplots(figsize=(10.8, 19.2), dpi=100)
fig.patch.set_facecolor('#040408') # Absolute Black / Void
ax.set_facecolor('#040408')

# Constrain coordinate system to 1 unit = 100 pixels
X_LIMIT = 5.4
Y_LIMIT = 9.6
ax.set_xlim(-X_LIMIT, X_LIMIT)
ax.set_ylim(-Y_LIMIT, Y_LIMIT)
ax.axis('off')

# 3. Static Assets: THE SENTINEL (Gurrgiyn)
# The Mantis is drawn once. It does not iterate.
mantis_color = '#39FF14' # C64 High-Voltage Green equivalent

# Thorax & Abdomen
ax.plot([0, 1.5, 3], [3, -1, -4], color=mantis_color, lw=6, solid_capstyle='round', zorder=10)

# Head (Geometric)
head_triangle = plt.Polygon([[-0.8, 3.8], [0.8, 3.8], [0, 2]], 
                            facecolor='#040408', edgecolor=mantis_color, lw=3, zorder=10)
ax.add_patch(head_triangle)

# Forelegs (The "Praying" Posture - kinetic potential)
ax.plot([0, -2.5, -0.5], [3, 1, -1.5], color=mantis_color, lw=4, solid_capstyle='round', zorder=10) # Left 
ax.plot([0, -1.5, 0], [2.8, 0.5, -2], color=mantis_color, lw=4, solid_capstyle='round', zorder=10)  # Right 

# Standing Base
ax.plot([1.5, 4], [-1, -5.5], color=mantis_color, lw=3, zorder=9)
ax.plot([1.5, 0.5], [-1, -5.5], color=mantis_color, lw=3, zorder=9)
ax.plot([0.5, -3], [0.5, -4.5], color=mantis_color, lw=3, zorder=9)

# The Nila Bindu (The Blue Pearl) - International Klein Blue
ax.scatter([0], [5.0], color='#002FA7', edgecolors='#0000FF', s=300, zorder=11)

# Title UI (Decoupled & Anchored)
ax.text(0, 8.5, "[Gurrgiyn - Silent Sentinel]", color='#39FF14', 
        ha='center', va='center', fontsize=20, fontfamily='monospace', weight='bold')

# 4. Dynamic Assets: THE METADATA FLOW
x_river = np.linspace(-X_LIMIT, X_LIMIT, 300)
river_lines = []
for i in range(7):
    # Alternating C-RAM green & deep green
    color = '#00FF41' if i % 2 == 0 else '#008F11'
    line, = ax.plot([], [], color=color, lw=2.5, alpha=0.5 - (i * 0.06), zorder=5)
    river_lines.append(line)

num_particles = 60
px = np.random.uniform(-X_LIMIT, X_LIMIT, num_particles)
py = np.random.uniform(-Y_LIMIT, Y_LIMIT, num_particles)
phases = np.random.uniform(0, 2*np.pi, num_particles)

# Violet Hexagons (Metadata/Ancestral Logic)
scatter = ax.scatter(px, py, c='#4B0082', edgecolors='#8A2BE2', 
                     marker='h', s=80, alpha=0.8, zorder=2)

# 5. Render Loop (Batch Execution)
TOTAL_FRAMES = 450 # 15 seconds at 30 FPS
print(f"[*] Rendering {TOTAL_FRAMES} frames. Initiating burn...")

for frame in range(TOTAL_FRAMES):
    # Update River (Sine Wave)
    for i, line in enumerate(river_lines):
        # Y-offset anchors it to the bottom third
        y = np.sin(x_river - (frame * 0.08) + (i * 0.6)) * (0.6 + i*0.15) - 6.5
        line.set_data(x_river, y)
        
    # Update Nodes (Vertical Drift)
    py += 0.05 
    py[py > Y_LIMIT] = -Y_LIMIT # "Loop Closure"
    
    # Pulse calculation
    sizes = 80 + 60 * np.sin(phases + frame * 0.1)
    scatter.set_offsets(np.column_stack((px, py)))
    scatter.set_sizes(sizes)
    
    # Commit to Disk
    frame_path = os.path.join(OUTPUT_DIR, f"frame_{frame:04d}.png")
    plt.savefig(frame_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0)
    
    if (frame + 1) % 30 == 0:
        sys.stdout.write(f"\r[*] Render Progress: {frame + 1}/{TOTAL_FRAMES} frames complete.")
        sys.stdout.flush()

print("\n[*] Render Sequence Complete. Gold Lattice achieved.")
