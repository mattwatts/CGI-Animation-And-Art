import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Wedge

# ==========================================
# LOGIC GARDEN 126: THE ENCAPSULATED NODE
# FORMAT: YOUTUBE SHORTS (1080x1920)
# ==========================================

# 1. Directory Janitorial Work
OUTPUT_DIR = "frames"
os.makedirs(OUTPUT_DIR, exist_ok=True)
print(f"[*] Provisioning output directory: ./{OUTPUT_DIR}/")

# 2. Canvas Topology
fig, ax = plt.subplots(figsize=(10.8, 19.2), dpi=100)
BG_COLOR = '#F9D8DF' # Retro Pale Pink BG
fig.patch.set_facecolor(BG_COLOR) 
ax.set_facecolor(BG_COLOR)

X_LIMIT = 5.4
Y_LIMIT = 9.6
ax.set_xlim(-X_LIMIT, X_LIMIT)
ax.set_ylim(-Y_LIMIT, Y_LIMIT)
ax.axis('off')

# 3. Static & Sine-Anchored Environment: RED SEAWEED
num_fronds = 25
x_bases = np.linspace(-X_LIMIT, X_LIMIT, num_fronds)
seaweed_lines = []
for i in range(num_fronds):
    # Alternating heights and phase offsets
    height = np.random.uniform(2.5, 5.0)
    line, = ax.plot([], [], color='#D81B60', lw=5, solid_capstyle='round', zorder=2)
    seaweed_lines.append({'line': line, 'x_base': x_bases[i], 'height': height, 'phase': np.random.uniform(0, 2*np.pi)})

# 4. Exogenous Data Vectors: YELLOW FISH SWARM
num_fish = 12
fish_data = {
    'x': np.random.uniform(-X_LIMIT, X_LIMIT, num_fish),
    'y': np.random.uniform(-2, 7, num_fish),
    'speed': np.random.uniform(0.04, 0.08, num_fish),
    'size': np.random.uniform(0.4, 0.8, num_fish),
    'patches': []
}
for i in range(num_fish):
    # Simple retro geometric fish (Triangle + Oval)
    poly = Polygon([[0,0], [0,0], [0,0]], facecolor='#FFD54F', edgecolor='#212121', lw=1.5, zorder=3)
    ax.add_patch(poly)
    fish_data['patches'].append(poly)

# 5. Core Construct: THE OPTIMAL HIVE (Submarine Base Vectors)
# We define base zero-centered vertices, and translate them dynamically.
sub_colors = {'hull': '#FFFFFF', 'base': '#29B6F6', 'canopy': '#FFF59D', 'accent': '#1E88E5'}

geo_shapes = {
    'fin_top': np.array([[1.5, 0.5], [2.5, 2.0], [2.5, 0.5]]),
    'hull_main': np.array([[-3.0, -1.0], [3.0, -1.0], [3.2, 0.8], [-2.8, 0.8]]),
    'hull_base': np.array([[-2.8, -1.8], [2.8, -1.8], [3.0, -1.0], [-3.0, -1.0]]),
    'canopy': np.array([[-1.8, 0.8], [0.8, 0.8], [0.5, 2.5], [-1.2, 2.5]]),
    'headlight_housing': np.array([[-3.2, -1.2], [-2.5, -1.2], [-2.3, -0.4], [-3.0, -0.4]]),
}

sub_patches = {}
for name, v in geo_shapes.items():
    color = sub_colors['hull'] if 'hull_main' in name else \
            sub_colors['base'] if 'hull_base' in name or 'headlight' in name else \
            sub_colors['canopy'] if 'canopy' in name else sub_colors['accent']
    poly = Polygon(v, facecolor=color, edgecolor='#212121', lw=2, zorder=5)
    ax.add_patch(poly)
    sub_patches[name] = poly

headlight = Circle((0,0), radius=0.3, facecolor='#FFCA28', edgecolor='#212121', lw=2, zorder=6)
porthole = Circle((0,0), radius=0.4, facecolor='#E1F5FE', edgecolor='#1E88E5', lw=3, zorder=6)
bubble_scatter = ax.scatter([], [], color='#E1F5FE', edgecolors='#81D4FA', s=80, alpha=0.7, zorder=4)
ax.add_patch(headlight)
ax.add_patch(porthole)

# Internal Observer Node (The Passengers)
pilot = Circle((0,0), radius=0.4, facecolor='#EF5350', zorder=4.5) # Subterfuge red hair analog
copilot = Circle((0,0), radius=0.4, facecolor='#FFB74D', zorder=4.5) # Orange suit analog
ax.add_patch(pilot)
ax.add_patch(copilot)

# 6. UI / Flight Recorder
ax.text(0, 8.5, "Subterfuge Stereo Party", color='#D81B60', 
        ha='center', va='center', fontsize=20, fontfamily='monospace', weight='bold', zorder=10)
depth_ui = ax.text(0, 7.8, "DEPTH: 2012m | STATUS: OPTIMAL", color='#212121', 
                   ha='center', va='center', fontsize=16, fontfamily='monospace', zorder=10)

# ==========================================
# RENDER LOOP (Perfect 15-second / 450 Frame Loop)
# ==========================================
TOTAL_FRAMES = 450
print(f"[*] Rendering {TOTAL_FRAMES} frames. Initiating burn...")

# Exhaust Bubbles state
bx = np.random.uniform(2, 3.5, 15)
by = np.random.uniform(-1, Y_LIMIT, 15)

for frame in range(TOTAL_FRAMES):
    t = frame * (2 * np.pi / TOTAL_FRAMES) # t goes from 0 to 2*PI perfectly
    
    # A. Calculate Sovereign Bobbing (Sinusoidal Submarine Y-Translation)
    sub_y = np.sin(t * 2) * 0.4 - 1.0 # 2 cycles per loop
    
    # Apply Translations to all Submarine components
    for name, v in geo_shapes.items():
        v_translated = v + np.array([0, sub_y])
        sub_patches[name].set_xy(v_translated)
        
    headlight.center = (-3.2, -0.8 + sub_y)
    porthole.center = (2.2, -0.1 + sub_y)
    pilot.center = (-1.0, +1.4 + sub_y)
    copilot.center = (-0.0, +1.2 + sub_y)
    
    # B. Update Red Seaweed (Sine wave kinetics anchored to the floor)
    for sw in seaweed_lines:
        y_pts = np.linspace(-Y_LIMIT, -Y_LIMIT + sw['height'], 20)
        # Bending increases as it gets higher from the base
        bend = (y_pts - (-Y_LIMIT)) / sw['height'] 
        x_pts = sw['x_base'] + np.sin(t * 4 + sw['phase']) * 0.4 * bend
        sw['line'].set_data(x_pts, y_pts)
        
    # C. Update Fish Data Vectors (Leftward Traversal)
    fish_data['x'] -= fish_data['speed']
    fish_data['x'][fish_data['x'] < -X_LIMIT - 1.0] += (X_LIMIT * 2 + 2.0)
    
    for i, f_poly in enumerate(fish_data['patches']):
        fx = fish_data['x'][i]
        fy = fish_data['y'][i] + np.sin(t*3 + i)*0.2
        fs = fish_data['size'][i]
        # Draw a fish shape (tail + body)
        fish_geom = np.array([
            [fx + fs, fy + fs/2], # Tail top
            [fx + fs, fy - fs/2], # Tail bot
            [fx + fs*0.5, fy],    # Tail joint
            [fx - fs, fy],        # Nose
            [fx + fs*0.5, fy + fs*0.5] # Top fin area
        ])
        f_poly.set_xy(fish_geom)
        
    # D. Exhaust Bubbles (Vertical ascent)
    by += 0.08
    bx += np.sin(by * 2) * 0.01 # slight wobble
    by[by > Y_LIMIT] = -2.0 + sub_y # Reset to sub exhaust area
    bubble_scatter.set_offsets(np.column_stack((bx, by)))

    # E. Commit to disk
    frame_path = os.path.join(OUTPUT_DIR, f"frame_{frame:04d}.png")
    plt.savefig(frame_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0)
    
    if (frame + 1) % 30 == 0:
        sys.stdout.write(f"\r[*] Render Progress: {frame + 1}/{TOTAL_FRAMES} frames complete.")
        sys.stdout.flush()

print("\n[*] Render Sequence Complete. Gold Lattice achieved.")
