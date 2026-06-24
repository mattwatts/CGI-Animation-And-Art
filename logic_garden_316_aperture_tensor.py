"""
SOVEREIGN CODE: logic_garden_316_aperture_tensor.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 316 (The Aperture Tensor // Hyperspace Gateway)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, MEGASCAE ARCHITECTURE
HOTFIX: Exhaust variance deleted. Static Megastructure locked.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
DURATION = 10.0  # 10.0 Second Seamless Loop
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_316_aperture_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#A0A0A5'
C_STEEL     = '#303035'
C_CYAN      = '#00E5FF'
C_DIM       = '#D0D0D5'

# ------------------------------------------------------------------
# O(1) METALLIC SHADER (RIGID STRUCTURAL MASS)
# ------------------------------------------------------------------
def draw_cylinder(ax, y_bottom, y_top, radius, zorder=5, color_base=C_STEEL, is_horizontal=False, x_center=0):
    steps = 40 
    r_val, g_val, b_val = [int(color_base.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)]
    
    for i in range(steps):
        ratio = (i / float(steps - 1))
        light_curve = np.exp(-((ratio - 0.4) ** 2) / 0.05) 
        ambient = 0.2 + 0.8 * light_curve
        c = f'#{int(r_val*ambient):02x}{int(g_val*ambient):02x}{int(b_val*ambient):02x}'
        
        w = (radius * 2) / steps
        x_start = x_center - radius + (i * w)
        
        if not is_horizontal:
            rect = patches.Rectangle((x_start, y_bottom), w, y_top - y_bottom, facecolor=c, edgecolor='none', zorder=zorder)
        else:
            rect = patches.Rectangle((y_bottom, x_start), y_top - y_bottom, w, facecolor=c, edgecolor='none', zorder=zorder)
        ax.add_patch(rect)

def draw_toroid_arc(ax, y_center, radius_x, radius_y, thickness, zorder, color_base, theta1, theta2):
    arc = patches.Arc((0, y_center), radius_x*2, radius_y*2, angle=0, 
                      theta1=theta1, theta2=theta2, color=color_base, 
                      linewidth=thickness, zorder=zorder, capstyle='butt')
    ax.add_patch(arc)

# ------------------------------------------------------------------
# SLIPSTREAM & GEOMETRIC SETUP
# ------------------------------------------------------------------
np.random.seed(316)
N_STREAKS = 1200
streak_x = np.random.uniform(-180, 180, N_STREAKS) # Constrained to flow THROUGH the gate
streak_y = np.random.uniform(-1000, 1000, N_STREAKS)
streak_length = np.random.uniform(100, 600, N_STREAKS)
streak_width = np.random.uniform(0.5, 3.0, N_STREAKS)

# Payload arrays (Rigid geometric blocks passing through)
N_SHIPS = 12
ship_x = np.random.uniform(-80, 80, N_SHIPS)
ship_y_start = np.random.uniform(-1000, 1000, N_SHIPS)
ship_w = np.random.uniform(10, 25, N_SHIPS)
ship_h = np.random.uniform(40, 120, N_SHIPS)

def render_frame(packet):
    f, phase_ratio = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)

    # 1. CONTINUOUS SLIPSTREAM (Through the core)
    slip_velocity = 6000.0 
    current_y = (streak_y - (phase_ratio * slip_velocity)) % 1920 - 960
    
    for i in range(N_STREAKS):
        y_top = current_y[i]
        y_bottom = current_y[i] - streak_length[i]
        if y_bottom < -960: y_bottom = -960
        # Check Z-order: Are they Behind the gate, or inside the aperture?
        # We put them at Z=2 so they are behind the front of the gate, but in front of the back.
        if y_top > y_bottom:
            ax.plot([streak_x[i], streak_x[i]], [y_bottom, y_top], 
                    color=C_TITANIUM, lw=streak_width[i], alpha=0.5, zorder=2)

    # 2. RIGID PAYLOAD (Geometric blocks representing traffic)
    current_ship_y = (ship_y_start - (phase_ratio * slip_velocity)) % 1920 - 960
    for i in range(N_SHIPS):
        rect = patches.Rectangle((ship_x[i] - ship_w[i]/2, current_ship_y[i]), 
                                 ship_w[i], ship_h[i], facecolor=C_TEXT, zorder=2.5)
        ax.add_patch(rect)

    # 3. MEGASTRUCTURE TENSOR (THE GATEWAY)
    y_gate = 0 # Center of frame
    
    # Back arc of the massive outer confinement ring (Z=1)
    draw_toroid_arc(ax, y_gate, radius_x=450, radius_y=120, thickness=90, zorder=1, color_base=C_STEEL, theta1=0, theta2=180)
    # Inner focusing ring (Back) (Z=1.5)
    draw_toroid_arc(ax, y_gate, radius_x=300, radius_y=70, thickness=20, zorder=1.5, color_base=C_TEXT, theta1=0, theta2=180)
    
    # Front arc of the massive outer confinement ring (Z=10)
    draw_toroid_arc(ax, y_gate, radius_x=450, radius_y=120, thickness=90, zorder=10, color_base=C_TITANIUM, theta1=180, theta2=360)
    # Inner focusing ring (Front) (Z=10.5)
    draw_toroid_arc(ax, y_gate, radius_x=300, radius_y=70, thickness=20, zorder=10.5, color_base=C_TEXT, theta1=180, theta2=360)

    # Lateral Structural Anchors (Horizontal pylons crossing the side boundaries)
    draw_cylinder(ax, -600, -450, radius=40, color_base=C_STEEL, is_horizontal=True, x_center=0, zorder=9)
    draw_cylinder(ax, 450, 600, radius=40, color_base=C_STEEL, is_horizontal=True, x_center=0, zorder=9)
    
    # Vertical stabilizing masts on the sides
    draw_cylinder(ax, -300, 300, radius=25, color_base=C_TEXT, x_center=-450, zorder=11)
    draw_cylinder(ax, -300, 300, radius=25, color_base=C_TEXT, x_center=450, zorder=11)

    # 4. ZERO-TEMPERATURE WIDGETS
    ax.text(-500, 880, "LG-316 :: THE APERTURE TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, 840, "[SFI-1.00] MEGASCAE ARCHITECTURE // STATIC DEPLOYMENT", color=C_TEXT, fontsize=12, fontname='monospace', zorder=80)
    
    # Telemetry
    ax.text(-500, -840, "SLIPSTREAM MASS THROUGHPUT", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=80)
    ax.add_patch(patches.Rectangle((-500, -860), 1000, 4, facecolor=C_DIM, zorder=80))
    ax.add_patch(patches.Rectangle((-500, -860), 1000 * phase_ratio, 4, facecolor=C_CYAN, zorder=81))

    # Structural Callouts
    ax.text(280, 150, "C_TITANIUM\nCONFINEMENT\nBOUNDARY", color=C_TEXT, fontsize=10, fontname='monospace', zorder=80)
    ax.plot([300, 400], [130, 0], color=C_TEXT, lw=1.5, zorder=80) 

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0)
    fig.clf(); plt.close(fig); gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = mp.cpu_count()
    with mp.Pool(processes=cpu_cores) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
