import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# ==========================================
#     THE POWER ANIMAL
# FORMAT: YOUTUBE SHORTS (1080x1920)
# ==========================================

# 1. Directory Janitorial Work
OUTPUT_DIR = "frames"
os.makedirs(OUTPUT_DIR, exist_ok=True)
print(f"[*] Provisioning output directory: ./{OUTPUT_DIR}/")

# 2. Canvas Topology (1080x1920 @ 100 DPI)
fig, ax = plt.subplots(figsize=(10.8, 19.2), dpi=100)
fig.patch.set_facecolor('#040408') # Absolute Black / Void
ax.set_facecolor('#040408')

X_LIMIT = 5.4
Y_LIMIT = 9.6
ax.set_xlim(-X_LIMIT, X_LIMIT)
ax.set_ylim(-Y_LIMIT, Y_LIMIT)
ax.axis('off')

# 3. Dynamic Environment: THE SUBCONSCIOUS CAVE (Z-Axis Wireframes)
NUM_PLANES = 15
z_array = np.linspace(0.1, 15, NUM_PLANES)
cave_planes = []
for i in range(NUM_PLANES):
    # C-RAM Cyan line to represent ice structure
    line, = ax.plot([], [], color='#00FFFF', lw=1.5, zorder=1)
    cave_planes.append(line)

# 4. Entity Construction: THE PENGUIN (Pure Matrix Geometry)
# Base shapes generated mathematically
t = np.linspace(0, 2*np.pi, 20)
geo_shapes = {
    'body': np.column_stack((1.2 * np.cos(t), 1.8 * np.sin(t))),
    'belly': np.column_stack((0.8 * np.cos(t), 1.2 * np.sin(t) - 0.4)),
    'head': np.column_stack((0.8 * np.cos(t), 0.8 * np.sin(t) + 2.0)),
    'eye': np.column_stack((0.2 * np.cos(t) + 0.3, 0.2 * np.sin(t) + 2.2)),
    'beak': np.array([[0.6, 2.0], [0.6, 2.4], [1.8, 2.2]]),
    'flipper': np.column_stack((0.4 * np.cos(t) - 0.2, 1.0 * np.sin(t) - 0.2))
}

colors = {
    'body': '#111111', 'belly': '#EEEEEE', 'head': '#111111',
    'eye': '#FFFFFF', 'beak': '#FFD700', 'flipper': '#333333'
}

patches = {}
for name, base_v in geo_shapes.items():
    poly = Polygon(base_v, closed=True, facecolor=colors[name], edgecolor='none', zorder=10, alpha=0.0)
    ax.add_patch(poly)
    patches[name] = poly

# Sliding Friction (Ice Trail)
trail_line, = ax.plot([], [], color='#FFFFFF', lw=3, zorder=9, alpha=0.8)

# 5. Fixed UI / Flight Recorder
hud_title = ax.text(0, 8.5, "[PROTOCOL: CAVE DESCENT]", color='#00FFFF', 
                    ha='center', va='center', fontsize=22, fontfamily='monospace', weight='bold')
hud_quote = ax.text(0, 7.5, "...", color='#FFFFFF', 
                    ha='center', va='center', fontsize=16, fontfamily='monospace', alpha=0.9)

# Engine Variables
TOTAL_FRAMES = 450
speed_z = 0.08
pivot = np.array([0, -1.8]) # Center of rotation (feet)

print(f"[*] Rendering {TOTAL_FRAMES} frames. Initiating burn...")

# 6. Main Render Loop
for frame in range(TOTAL_FRAMES):
    
    # -- A. Update Cave (Z-Axis Translation) --
    z_array -= speed_z
    z_array[z_array < 0.1] += 15.0
    
    for i in range(NUM_PLANES):
        z = z_array[i]
        scale = 1.0 / z
        # Geometric tunnel walls
        cx = [-4*scale, 4*scale, 4*scale, -4*scale, -4*scale]
        cy = [-6*scale, -6*scale, 6*scale, 6*scale, -6*scale]
        cave_planes[i].set_data(cx, cy)
        # Alpha fading relative to depth
        cave_planes[i].set_alpha(max(0, 1 - (z / 15)))

    # -- B. Narrative State Machine --
    alpha_entity = 0.0
    theta = 0.0
    x_offset = 0.0
    y_offset = -2.0 # Base floor position

    if frame < 100:
        hud_quote.set_text('"Step forward into your cave..."')
    elif frame < 200:
        hud_title.set_text("[SUBROUTINE: POWER ANIMAL]")
        hud_quote.set_text('"You\'re going to find your power animal."')
        alpha_entity = min(1.0, (frame - 100) / 50.0) # Materialize
    elif frame < 230:
        hud_title.set_text("[ACTION REQUIRED]")
        hud_quote.set_text('"SLIDE."')
        alpha_entity = 1.0
        # Physics transition: Fall forward to belly (-90 degrees)
        progress = (frame - 200) / 30.0
        theta = - (np.pi / 2) * progress
    else:
        hud_title.set_text("[FRICTION = 0]")
        hud_quote.set_text('>>> FLOW STATE ENGAGED >>>')
        alpha_entity = 1.0
        theta = - np.pi / 2
        # Translate X (Slide)
        x_offset = (frame - 230) * 0.1
        y_offset = -2.5 # Adjusted down for belly drag
        
        # Draw "Ice Trail"
        trail_line.set_data([-X_LIMIT, x_offset], [y_offset - 0.5, y_offset - 0.5])

    # -- C. Apply Matrix Transformations --
    # Rotational Matrix R
    R = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)]
    ])
    
    for name, base_v in geo_shapes.items():
        # Vertex Transformation: Center -> Rotate -> Translate
        v_transformed = np.dot(base_v - pivot, R.T) + pivot + np.array([x_offset, y_offset])
        patches[name].set_xy(v_transformed)
        patches[name].set_alpha(alpha_entity)

    # -- D. Write Frame --
    frame_path = os.path.join(OUTPUT_DIR, f"frame_{frame:04d}.png")
    plt.savefig(frame_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0)
    
    if (frame + 1) % 30 == 0:
        sys.stdout.write(f"\r[*] Render Progress: {frame + 1}/{TOTAL_FRAMES} frames complete.")
        sys.stdout.flush()

print("\n[*] Render Sequence Complete. Gold Lattice achieved.")
