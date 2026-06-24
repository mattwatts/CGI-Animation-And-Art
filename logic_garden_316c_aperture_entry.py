"""
SOVEREIGN CODE: logic_garden_316c_aperture_entry.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 316c (Einstein-Rosen Aperture // Ingress Tensor)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, EINSTEIN-ROSEN TOPOLOGY
HOTFIX: Slipstream vector reversed. Topological consumption locked at Y=0.
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
DURATION = 10.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_316c_aperture_entry"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + VIBRANT INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#A0A0A5'
C_STEEL     = '#303035'
C_GOLD      = '#FFB300'   # Magnetic Confinement Couplings
C_AZURE     = '#007FFF'   # Structural Stators
C_CYAN      = '#00FFFF'   # Cherenkov Emission Stream
C_INDIGO    = '#1A0033'   # Einstein-Rosen Throat (Absolute Void)

# ------------------------------------------------------------------
# O(1) METALLIC SHADER
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
# EINSTEIN-ROSEN INGRESS LOGIC (O(1) CACHED ARRAYS)
# ------------------------------------------------------------------
np.random.seed(316)

# The aperture throat radius
THROAT_RX = 390
THROAT_RY = 95

# Ingress variables (Traffic flows strictly FROM 1000 DOWN to 0)
N_STREAKS = 1200
# Spawning high up in the Y-axis to map the gravitational pull
streak_x = np.random.uniform(-THROAT_RX + 20, THROAT_RX - 20, N_STREAKS)
streak_y_offset = np.random.uniform(0, 1000, N_STREAKS)
streak_length = np.random.uniform(80, 300, N_STREAKS)
streak_width = np.random.uniform(1.0, 3.5, N_STREAKS)

# Rigid Payload (Ships plummeting into the gate)
N_SHIPS = 18
ship_x = np.random.uniform(-250, 250, N_SHIPS)
ship_y_offset = np.random.uniform(0, 1000, N_SHIPS)
ship_w = np.random.uniform(15, 30, N_SHIPS)
ship_h = np.random.uniform(50, 150, N_SHIPS)

def render_frame(packet):
    f, phase_ratio = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    
    # BARE-METAL CAMERA LOCK (Tuple Rupture Mitigated)
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)
    ax.autoscale(False)

    # 1. EINSTEIN-ROSEN THROAT (Z=5)
    # The Absolute Topological Block. Masks the background.
    throat = patches.Ellipse((0, 0), THROAT_RX*2, THROAT_RY*2, facecolor=C_INDIGO, zorder=5)
    ax.add_patch(throat)

    # Internal Cherenkov Ring inside the throat
    throat_glow = patches.Ellipse((0, 0), THROAT_RX*1.8, THROAT_RY*1.7, facecolor='none', edgecolor=C_CYAN, lw=8, zorder=5.1, alpha=0.3)
    ax.add_patch(throat_glow)

    # 2. INGRESS KINEMATICS (Z=6, Falling from Y=1000 down into Y=0 void)
    slip_velocity = 5000.0

    # Traffic falls inward. 
    current_streak_y = 1000.0 - ((streak_y_offset + phase_ratio * slip_velocity) % 1000)
    
    for i in range(N_STREAKS):
        y_top = current_streak_y[i]
        y_bottom = current_streak_y[i] - streak_length[i]

        # Cull conditions: If completely consumed by the Event Horizon (0), skip render
        if y_top < 0:
            continue

        # Color mapping: Streaks flash Cyan due to immense friction just before entering the throat
        dist_ratio = abs(y_bottom) / 1000.0
        c_streak = C_CYAN if dist_ratio < 0.25 else C_STEEL
        alpha_s = 0.8 if dist_ratio < 0.25 else 0.4

        # Slice the streak exactly at Y=0 so it does not pierce the bottom of the hoop
        if y_bottom < 0:
            y_bottom = 0

        ax.plot([streak_x[i], streak_x[i]], [y_bottom, y_top], color=c_streak, lw=streak_width[i], alpha=alpha_s, zorder=6)

    # 3. RIGID PAYLOAD (Ingress Ships) (Z=6.5)
    current_ship_y = 1000.0 - ((ship_y_offset + phase_ratio * slip_velocity) % 1000)
    
    for i in range(N_SHIPS):
        y_bot_ship = current_ship_y[i] - ship_h[i]
        y_top_ship = current_ship_y[i]

        # Occlusion cull: If the top of the ship is past the boundary, it has vanished.
        if y_top_ship < 0:
            continue

        h_render = ship_h[i]
        y_render = y_bot_ship
        
        # If the ship is partially entering the gate, slice the bottom off
        if y_bot_ship < 0:
            h_render = y_top_ship - 0
            if h_render < 0: continue
            y_render = 0

        rect = patches.Rectangle((ship_x[i] - ship_w[i]/2, y_render), ship_w[i], h_render, facecolor=C_TEXT, edgecolor=C_AZURE, lw=1, zorder=6.5)
        ax.add_patch(rect)

    # 4. MEGASTRUCTURE TENSOR (THE GATEWAY)
    y_gate = 0

    # Back arc (Z=4, structurally behind the incoming traffic)
    draw_toroid_arc(ax, y_gate, radius_x=450, radius_y=130, thickness=100, zorder=4, color_base=C_STEEL, theta1=0, theta2=180)

    # Front arc (Z=10, physically occluding the lower throat edge)
    draw_toroid_arc(ax, y_gate, radius_x=450, radius_y=130, thickness=100, zorder=10, color_base=C_TITANIUM, theta1=180, theta2=360)
    draw_toroid_arc(ax, y_gate, radius_x=370, radius_y=100, thickness=30, zorder=10.5, color_base=C_TEXT, theta1=180, theta2=360)

    # Color Injection: High-Contrast C_GOLD Magnetic Couplings
    # Because we inverted flow, these are now actively pulling energy inward
    for angle in [200, 240, 270, 300, 340]:
        rad = np.radians(angle)
        ex = 450 * np.cos(rad)
        draw_cylinder(ax, y_gate - 140, y_gate - 60, radius=25, color_base=C_GOLD, x_center=ex, zorder=11)
        draw_cylinder(ax, y_gate - 110, y_gate - 90, radius=35, color_base=C_AZURE, x_center=ex, zorder=11.1)

    # Lateral Anchors
    draw_cylinder(ax, -650, -420, radius=50, color_base=C_STEEL, is_horizontal=True, x_center=0, zorder=9)
    draw_cylinder(ax, 420, 650, radius=50, color_base=C_STEEL, is_horizontal=True, x_center=0, zorder=9)

    # 5. ZERO-TEMPERATURE WIDGETS
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-316c :: EINSTEIN-ROSEN INGRESS TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] TOPOLOGICAL CONSUMPTION // Y=0 BOUNDARY LOCK", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    # Telemetry
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    ax.text(-500, -760, "SYS_01 [EVENT HORIZON]       :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, "APERTURE MAINTAINING O(1) STRUCTURAL INTEGRITY", color=C_STEEL, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [INGRESS TRAFFIC]     :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, "LOCAL TENSOR ERASED // TOPOLOGY TRANSITION", color=C_CYAN, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "TRANSIT KINEMATICS           :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=80)
    ax.add_patch(patches.Rectangle((-500, -860), 1000, 4, facecolor=C_STEEL, zorder=80))
    ax.add_patch(patches.Rectangle((-500, -860), 1000 * phase_ratio, 4, facecolor=C_CYAN, zorder=81))

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    
    # Absolute Integrity: bbox_inches removed to prevent Memory Cascade. Grid strictly bounded 1080x1920
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close('all')
    gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-316c: EINSTEIN-ROSEN INGRESS [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
