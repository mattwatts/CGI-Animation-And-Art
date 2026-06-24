"""
SOVEREIGN CODE: logic_garden_154b_orbital_spar.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 154b (Orbital Spar // Megascale Buoyancy Tensor)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: C_WHITE syntax leak sealed. Complete monolithic array deployed.
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
OUT_DIR = "frames_154b_orbital_spar"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#A0A0A5'
C_STEEL     = '#303035'
C_GOLD      = '#FFB300'   # Gravity / Ballasting Logic
C_MANTIS    = '#00FF00'   # Terminal Green Flow (Extraction)
C_CYAN      = '#00FFFF'   # Cooling / Superconductors
C_GAS       = '#D0D0D5'   # Atmospheric Shear Streaks
C_WHITE     = '#FFFFFF'   # Payload core energy

# ------------------------------------------------------------------
# O(1) METALLIC SHADER
# ------------------------------------------------------------------
def draw_cylinder(ax, y_bottom, y_top, radius, zorder=5, color_base=C_STEEL, is_horizontal=False, x_center=0):
    steps = 40 
    r_val, g_val, b_val = [int(color_base.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)]
    
    for i in range(steps):
        ratio = (i / float(steps - 1))
        # Mathematical specularity curve
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
# KINEMATIC ARRAYS (O(1) CACHED)
# ------------------------------------------------------------------
np.random.seed(154)

# 1. Atmospheric Shear (Moving UP to simulate deep descent/buoyancy)
N_STREAKS = 1200
streak_x = np.random.uniform(-540, 540, N_STREAKS)
streak_y_offset = np.random.uniform(0, 1920, N_STREAKS)
streak_length = np.random.uniform(100, 500, N_STREAKS)
streak_width = np.random.uniform(1.0, 4.0, N_STREAKS)

# 2. Terminal Green Extraction Payload (Moving UP the tether)
N_PAYLOADS = 18
payload_y_offset = np.linspace(0, 1920, N_PAYLOADS)

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

    # 1. CRITICAL DAMPING OSCILLATION (The entire structure "breathes" via buoyancy)
    y_bob = np.sin(phase_ratio * 2 * np.pi) * 45.0 

    # 2. ATMOSPHERIC SHEAR (The Local Universe rips upward)
    slip_velocity = 4500.0 
    current_streak_y = ((streak_y_offset + phase_ratio * slip_velocity) % 1920) - 960
    
    for i in range(N_STREAKS):
        y_bottom = current_streak_y[i]
        y_top = y_bottom + streak_length[i]
        
        if y_top > -960:
            ax.plot([streak_x[i], streak_x[i]], [y_bottom, y_top], 
                    color=C_GAS, lw=streak_width[i], alpha=0.35, zorder=1)

    # 3. EXTRACTION TETHER (Z=4)
    ax.plot([0, 0], [-960, y_bob + 250], color=C_TEXT, lw=24, solid_capstyle='butt', zorder=4)
    ax.plot([0, 0], [-960, y_bob + 250], color=C_GOLD, lw=8, zorder=4.1)

    # 4. TERMINAL GREEN PAYLOAD ASCENSION (Z=4.5)
    payload_velocity = 1920.0
    current_payload_y = ((payload_y_offset + phase_ratio * payload_velocity) % 1920) - 960
    for py in current_payload_y:
        if py < y_bob + 250:
            rect = patches.Rectangle((-25, py), 50, 80, facecolor=C_MANTIS, edgecolor=C_TEXT, lw=2, zorder=4.5)
            ax.add_patch(rect)
            # Center energy core of the payload (C_WHITE is now globally bound)
            ax.add_patch(patches.Rectangle((-8, py+20), 16, 40, facecolor=C_WHITE, zorder=4.6))

    # 5. MEGASTRUCTURE: THE ORBITAL SPAR (Z=5 to Z=10)
    poly_cone = patches.Polygon([[-80, y_bob + 150], [80, y_bob + 150], [160, y_bob + 280], [-160, y_bob + 280]], facecolor=C_STEEL, zorder=5)
    ax.add_patch(poly_cone)
    
    draw_cylinder(ax, y_bob + 280, y_bob + 850, radius=160, color_base=C_TITANIUM, zorder=6)
    
    for ry in range(320, 800, 80):
        draw_cylinder(ax, y_bob + ry, y_bob + ry + 20, radius=164, color_base=C_TEXT, zorder=6.1)

    for ty in [450, 700]:
        draw_toroid_arc(ax, y_bob + ty, radius_x=280, radius_y=50, thickness=40, zorder=5, color_base=C_STEEL, theta1=0, theta2=180)
        draw_toroid_arc(ax, y_bob + ty, radius_x=280, radius_y=50, thickness=40, zorder=8, color_base=C_TITANIUM, theta1=180, theta2=360)
        draw_toroid_arc(ax, y_bob + ty, radius_x=280, radius_y=50, thickness=10, zorder=8.1, color_base=C_GOLD, theta1=180, theta2=360)

    draw_cylinder(ax, y_bob + 850, y_bob + 920, radius=90, color_base=C_STEEL, zorder=6)
    ax.plot([0, 0], [y_bob + 920, y_bob + 1200], color=C_TEXT, lw=6, zorder=5) 

    # 6. ZERO-TEMPERATURE WIDGETS
    ax.text(-500, 880, "LG-154b :: ORBITAL SPAR TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, 840, "[SFI-1.00] BUOYANCY KINEMATICS // RIGID POLYGON MASS", color=C_TEXT, fontsize=12, fontname='monospace', zorder=80)
    
    ax.text(-500, -840, "TERMINAL GREEN FLOW // CRITICAL DAMPING", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=80)
    ax.add_patch(patches.Rectangle((-500, -860), 1000, 4, facecolor=C_TITANIUM, zorder=80))
    ax.add_patch(patches.Rectangle((-500, -860), 1000 * phase_ratio, 4, facecolor=C_MANTIS, zorder=81))

    ax.text(-500, -780, f"Z-AXIS DEVIATION: {y_bob:>05.1f}Δ", color=C_TEXT if abs(y_bob) < 10 else C_GOLD, fontsize=12, fontname='monospace', weight='bold', zorder=80)

    ax.text(280, y_bob + 320, "C_MANTIS\nEXTRACTION\nACTIVE", color=C_MANTIS, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    ax.plot([200, 270], [y_bob + 250, y_bob + 330], color=C_MANTIS, lw=1.5, zorder=80) 

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0)
    fig.clf(); plt.close(fig); gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-154b: ORBITAL SPAR TENSOR [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
