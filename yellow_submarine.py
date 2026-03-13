import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Wedge

# ==========================================
# LOGIC GARDEN 126: THE ENCAPSULATED NODE (HOTFIX: YELLOW SUBMARINE)
# FORMAT: YOUTUBE SHORTS (1080x1920)
# ==========================================

# 1. Directory Janitorial Work
OUTPUT_DIR = "frames"
os.makedirs(OUTPUT_DIR, exist_ok=True)
print(f"[*] Provisioning output directory: ./{OUTPUT_DIR}/")

# 2. Canvas Topology
fig, ax = plt.subplots(figsize=(10.8, 19.2), dpi=100)
BG_COLOR = '#81D4FA' # Shifted to Oceanic Cyan/Blue for Yellow Contrast
fig.patch.set_facecolor(BG_COLOR) 
ax.set_facecolor(BG_COLOR)

X_LIMIT = 5.4
Y_LIMIT = 9.6
ax.set_xlim(-X_LIMIT, X_LIMIT)
ax.set_ylim(-Y_LIMIT, Y_LIMIT)
ax.axis('off')

# 3. Environment: PINK SEAWEED (Retro Contrast)
num_fronds = 30
x_bases = np.linspace(-X_LIMIT, X_LIMIT, num_fronds)
seaweed_lines = []
for i in range(num_fronds):
    height = np.random.uniform(3.0, 6.0)
    # Magenta/Pink Seaweed for the Subterfuge vibe
    line, = ax.plot([], [], color='#EC407A', lw=6, solid_capstyle='round', zorder=2)
    seaweed_lines.append({'line': line, 'x_base': x_bases[i], 'height': height, 'phase': np.random.uniform(0, 2*np.pi)})

# 4. Exogenous Vectors: FISH SWARM
num_fish = 15
fish_data = {
    'x': np.random.uniform(-X_LIMIT, X_LIMIT, num_fish),
    'y': np.random.uniform(-2, 8, num_fish),
    'speed': np.random.uniform(0.03, 0.07, num_fish),
    'size': np.random.uniform(0.3, 0.7, num_fish),
    'patches': []
}
for i in range(num_fish):
    # Coral colored fish
    poly = Polygon([[0,0], [0,0], [0,0]], facecolor='#FF7043', edgecolor='#212121', lw=1.5, zorder=3)
    ax.add_patch(poly)
    fish_data['patches'].append(poly)

# 5. Core Construct: THE YELLOW SUBMARINE (Topology Update)
sub_colors = {
    'hull': '#FFCA28',        # Pure Gold/Yellow
    'stripes': '#EF5350',     # Red Accents
    'tower': '#FFCA28',       # Conning Tower
    'dome': '#FFFFFF',        # White/Cyan Dome Array
    'prop': '#9CCC65',        # Green Propeller
    'window': '#4DD0E1'       # Internal Light
}

# Generating the bulbous hull using parametric equations
t = np.linspace(0, 2*np.pi, 50)
geo_shapes = {
    # Main Body: elongated oval
    'hull': np.column_stack((3.2 * np.cos(t), 1.4 * np.sin(t) - 0.5)),
    # Conning Tower (Base + Dome)
    'tower_base': np.array([[-1.0, 0.5], [1.0, 0.5], [0.8, 2.0], [-0.8, 2.0]]),
    'tower_dome': np.column_stack((0.8 * np.cos(t[t>0]), 0.6 * np.sin(t[t>0]) + 2.0)),
    # Red Accents (Midline & Tail)
    'stripe': np.array([[-3.0, -0.6], [3.0, -0.6], [3.0, -0.4], [-3.0, -0.4]]),
    'tail_fin': np.array([[2.8, -0.5], [4.0, -1.5], [3.8, 0.5]]),
    'prop_blade': np.array([[3.8, -0.5], [4.5, -1.0], [4.5, 0.0]])
}

sub_patches = {}
for name, v in geo_shapes.items():
    if 'hull' in name or 'tower_base' in name: color = sub_colors['hull']
    elif 'tower_dome' in name: color = sub_colors['dome']
    elif 'prop' in name: color = sub_colors['prop']
    else: color = sub_colors['stripes']
    
    poly = Polygon(v, facecolor=color, edgecolor='#212121', lw=2.5, zorder=5)
    ax.add_patch(poly)
    sub_patches[name] = poly

# Multiple Portholes (The iconic visual signature)
portholes = [
    Circle((-1.8, -0.5), radius=0.4, facecolor=sub_colors['window'], edgecolor='#212121', lw=3, zorder=6),
    Circle((0, -0.5), radius=0.4, facecolor=sub_colors['window'], edgecolor='#212121', lw=3, zorder=6),
    Circle((1.8, -0.5), radius=0.4, facecolor=sub_colors['window'], edgecolor='#212121', lw=3, zorder=6)
]
for p in portholes: ax.add_patch(p)

# Periscopes (Dual Output Nodes)
peri_colors = ['#EF5350', '#42A5F5']
periscopes = [
    ax.plot([-0.2, -0.2, -0.5], [2.5, 3.5, 3.5], color=peri_colors[0], lw=4, solid_capstyle='round', zorder=4)[0],
    ax.plot([0.3, 0.3, 0.6], [2.5, 3.2, 3.2], color=peri_colors[1], lw=4, solid_capstyle='round', zorder=4)[0]
]

# 6. UI / Flight Recorder
ax.text(0, 8.5, "Yellow Submarine", color='#FFCA28', 
        ha='center', va='center', fontsize=22, fontfamily='monospace', weight='bold', zorder=10)
ax.text(0, 7.8, "BUOYANCY: OPTIMAL | ENTROPY: 0", color='#FFFFFF', 
        ha='center', va='center', fontsize=16, fontfamily='monospace', zorder=10)

# ==========================================
# RENDER LOOP (Perfect 15-second / 450 Frame Loop)
# ==========================================
TOTAL_FRAMES = 450
print(f"[*] Rendering {TOTAL_FRAMES} frames. Initiating burn...")

for frame in range(TOTAL_FRAMES):
    t_val = frame * (2 * np.pi / TOTAL_FRAMES) 
    
    # A. Calculate Sovereign Bobbing (Base offset)
    sub_y = np.sin(t_val * 2) * 0.5
    
    # Apply Translations to all Yellow Submarine components
    for name, vOrig in geo_shapes.items():
        vOrig2D = vOrig if len(vOrig.shape) == 2 else np.column_stack((vOrig[0], vOrig[1]))
        v_translated = vOrig2D + np.array([0, sub_y])
        
        # Propeller rotation logic mapping
        if 'prop' in name:
            pivot = np.array([3.8, -0.5]) + np.array([0, sub_y])
            theta = frame * 0.5 # Fast spin
            R = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
            v_centered = vOrig2D + np.array([0, sub_y]) - pivot
            v_translated = np.dot(v_centered, R.T) + pivot
            
        sub_patches[name].set_xy(v_translated)
        
    portholes[0].center = (-1.8, -0.5 + sub_y)
    portholes[1].center = (0, -0.5 + sub_y)
    portholes[2].center = (1.8, -0.5 + sub_y)
    
    # Periscope update
    periscopes[0].set_data([-0.4, -0.4, -0.7], [2.5+sub_y, 3.5+sub_y, 3.5+sub_y])
    periscopes[1].set_data([0.4, 0.4, 0.7], [2.5+sub_y, 3.2+sub_y, 3.2+sub_y])

    # B. Update Pink Seaweed
    for sw in seaweed_lines:
        y_pts = np.linspace(-Y_LIMIT, -Y_LIMIT + sw['height'], 20)
        bend = (y_pts - (-Y_LIMIT)) / sw['height'] 
        x_pts = sw['x_base'] + np.sin(t_val * 4 + sw['phase']) * 0.6 * bend
        sw['line'].set_data(x_pts, y_pts)
        
    # C. Update Fish Data Vectors
    fish_data['x'] -= fish_data['speed']
    fish_data['x'][fish_data['x'] < -X_LIMIT - 1.0] += (X_LIMIT * 2 + 2.0)
    
    for i, f_poly in enumerate(fish_data['patches']):
        fx = fish_data['x'][i]
        fy = fish_data['y'][i] + np.sin(t_val*3 + i)*0.3
        fs = fish_data['size'][i]
        fish_geom = np.array([
            [fx + fs, fy + fs/2], [fx + fs, fy - fs/2], [fx + fs*0.5, fy], 
            [fx - fs, fy], [fx + fs*0.5, fy + fs*0.5]
        ])
        f_poly.set_xy(fish_geom)

    # D. Commit to Disk
    frame_path = os.path.join(OUTPUT_DIR, f"frame_{frame:04d}.png")
    plt.savefig(frame_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0)
    
    if (frame + 1) % 30 == 0:
        sys.stdout.write(f"\r[*] Render Progress: {frame + 1}/{TOTAL_FRAMES} frames complete.")
        sys.stdout.flush()

print("\n[*] Render Sequence Complete. Gold Lattice achieved.")
