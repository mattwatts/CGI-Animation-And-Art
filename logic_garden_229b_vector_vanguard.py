"""
SOVEREIGN CODE: logic_garden_229b_vector_vanguard.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 229b (Relativistic Sustainment Tensor // Colony Vanguard)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Purged point-clouds. Activated Solid Vector Array. Zero-Rotation Lock.
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
RENDER_MODE = "STUDY"
DURATION = 10.0  # 10.0 Second Seamless Loop
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_229b_vector_vanguard"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#A0A0A5'
C_STEEL     = '#303035'
C_CYAN      = '#00E5FF'
C_WHITE     = '#FFFFFF'
C_CORE      = '#00AAFF'
C_WARNING   = '#FF0055'

# ------------------------------------------------------------------
# O(1) METALLIC CYLINDER SHADER (RIGID STRUCTURAL MASS)
# ------------------------------------------------------------------
# To avoid the "coloured dots" hallucination, we build solid structural 
# mass by mathematically shading vector rectangles.
def draw_cylinder(ax, y_bottom, y_top, radius, zorder=5, color_base=C_STEEL, is_horizontal=False, x_center=0):
    steps = 40 # Micro-shading layers
    r_val, g_val, b_val = [int(color_base.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)]
    
    for i in range(steps):
        # Calculate horizontal gradient curve for lighting
        ratio = (i / float(steps - 1))
        # Specular highlight slightly off-center
        light_curve = np.exp(-((ratio - 0.4) ** 2) / 0.05) 
        ambient = 0.2 + 0.8 * light_curve
        
        c = f'#{int(r_val*ambient):02x}{int(g_val*ambient):02x}{int(b_val*ambient):02x}'
        
        w = (radius * 2) / steps
        x_start = x_center - radius + (i * w)
        
        if not is_horizontal:
            rect = patches.Rectangle((x_start, y_bottom), w, y_top - y_bottom, facecolor=c, edgecolor='none', zorder=zorder)
        else:
            # For horizontal cross-struts
            rect = patches.Rectangle((y_bottom, x_start), y_top - y_bottom, w, facecolor=c, edgecolor='none', zorder=zorder)
        ax.add_patch(rect)

def draw_toroid_arc(ax, y_center, radius_x, radius_y, thickness, zorder, color_base, theta1, theta2):
    # Front half of biological ring (covers spine) or Back half (behind spine)
    arc = patches.Arc((0, y_center), radius_x*2, radius_y*2, angle=0, 
                      theta1=theta1, theta2=theta2, color=color_base, 
                      linewidth=thickness, zorder=zorder, capstyle='round')
    ax.add_patch(arc)

# ------------------------------------------------------------------
# SLIPSTREAM & GEOMETRIC SETUP (O(1) CACHED ARRAYS)
# ------------------------------------------------------------------
np.random.seed(229)
N_STREAKS = 1500
streak_x = np.random.uniform(-540, 540, N_STREAKS)
streak_y = np.random.uniform(-1000, 1000, N_STREAKS)
streak_length = np.random.uniform(50, 400, N_STREAKS)
streak_width = np.random.uniform(0.5, 2.5, N_STREAKS)

def render_frame(packet):
    f, phase_ratio = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    
    # 1080x1920 logical constraints
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)

    # 1. CONTINUOUS SLIPSTREAM TENSOR (V_G: -8000.0)
    # The ship is paralyzed on the Y-Axis. The universe moves.
    slip_velocity = 4000.0 
    current_y = (streak_y - (phase_ratio * slip_velocity)) % 1920 - 960
    
    for i in range(N_STREAKS):
        # We explicitly enforce the streak wrap to preserve O(1) object permanence
        y_top = current_y[i]
        y_bottom = current_y[i] - streak_length[i]
        if y_bottom < -960: y_bottom = -960 # Hard clip to frame to save CPU
        if y_top > y_bottom:
            # Low entropy structural dark streaks against daylight bg
            ax.plot([streak_x[i], streak_x[i]], [y_bottom, y_top], 
                    color=C_TITANIUM, lw=streak_width[i], alpha=0.4, zorder=1)

    # 2. THE RIGID SHIP TENSOR (STATIC, DEAD-CENTER, ZERO ROTATION)
    # Nose Cone / Shielding Base
    draw_cylinder(ax, 380, 550, radius=30, color_base=C_STEEL, zorder=6)
    poly_nose = patches.Polygon([[-30, 550], [30, 550], [0, 680]], facecolor=C_STEEL, zorder=6)
    ax.add_patch(poly_nose)

    # Main Structural Spine
    draw_cylinder(ax, -100, 400, radius=45, color_base=C_STEEL, zorder=5)
    
    # Intricate Detail / Structural Ribbing along spine
    for y_rib in range(-80, 400, 15):
        draw_cylinder(ax, y_rib, y_rib+4, radius=48, color_base=C_TEXT, zorder=5.1)

    # Biological Containment Toroids (The Payload)
    # 3 massive rings. We draw the back arc (zorder=4), then the front (zorder=7)
    toroid_y_positions = [250, 100, -50]
    for ty in toroid_y_positions:
        # Back half
        draw_toroid_arc(ax, ty, radius_x=280, radius_y=40, thickness=25, zorder=4, color_base=C_TITANIUM, theta1=0, theta2=180)
        # Front half (crosses over the spine)
        draw_toroid_arc(ax, ty, radius_x=280, radius_y=40, thickness=25, zorder=7, color_base=C_TITANIUM, theta1=180, theta2=360)
        
        # High-Contrast Kinematic Locking Struts
        draw_cylinder(ax, ty-8, ty+8, radius=200, color_base=C_TEXT, is_horizontal=True, x_center=ty)

    # Engine Baffles / Lower Assembly
    draw_cylinder(ax, -250, -100, radius=80, color_base=C_STEEL, zorder=6)
    draw_cylinder(ax, -250, -220, radius=90, color_base=C_TEXT, zorder=6.1)

    # Engine Thrust Bell
    poly_bell = patches.Polygon([[-80, -250], [80, -250], [130, -350], [-130, -350]], facecolor=C_TEXT, zorder=4.9)
    ax.add_patch(poly_bell)

    # 3. DYNAMIC ANTIMATTER PLUME (Eulerian Spallation)
    # The plume throbs dynamically but loops perfectly using sine kinematics
    plume_cycles = 15 # Oscillates 15 times over the 10 seconds
    plume_phase = np.sin((phase_ratio * 2 * np.pi) * plume_cycles)
    
    # Inner Plasma Core (White)
    core_length = -600 - (plume_phase * 40)
    poly_core = patches.Polygon([[-70, -340], [70, -340], [0, core_length]], facecolor=C_WHITE, zorder=4.8, alpha=0.9)
    ax.add_patch(poly_core)

    # Outer Energy Corona (Cyan)
    corona_length = -800 - (plume_phase * 120)
    poly_corona = patches.Polygon([[-140, -340], [140, -340], [0, corona_length]], facecolor=C_CYAN, zorder=4.7, alpha=0.6)
    ax.add_patch(poly_corona)

    # Frictional Plasma Exhaust (Spallation Triangles)
    np.random.seed(int(f)) # Tie to frame for chaotic but deterministic noise
    for _ in range(40):
        px = np.random.uniform(-100, 100)
        py_base = np.random.uniform(corona_length, -350)
        pw = np.random.uniform(5, 15)
        ax.add_patch(patches.Polygon([[px-pw, py_base], [px+pw, py_base], [px, py_base-pw*4]], facecolor=C_CYAN, alpha=0.8, zorder=4.6))

    # 4. ZERO-TEMPERATURE WIDGETS (Visually Accurate Telemetry)
    ax.text(-500, 880, "LG-229b :: RIGID VECTOR VANGUARD", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, 840, "[SFI-1.00] Z-PLANE ARCHITECTURE: SOLID POLYGON MASS", color=C_TEXT, fontsize=12, fontname='monospace', zorder=80)
    
    # Progress Bar UI
    ax.text(-500, -840, "KINEMATIC EXHAUST TENSOR", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=80)
    ax.add_patch(patches.Rectangle((-500, -860), 1000, 4, facecolor=C_TITANIUM, zorder=80))
    ax.add_patch(patches.Rectangle((-500, -860), 1000 * phase_ratio, 4, facecolor=C_CYAN, zorder=81))

    # Biological Payload Readout
    ax.text(250, 260, "[BIO-PAYLOAD: 10,000]", color=C_TEXT, fontsize=12, fontname='monospace', weight='bold', zorder=80)
    ax.plot([140, 240], [250, 265], color=C_TEXT, lw=2, zorder=80) # Tie line to top Toroid

    ax.text(250, -70, "[CENTRIFUGAL LOCK: NOMINAL]", color=C_TEXT, fontsize=12, fontname='monospace', weight='bold', zorder=80)
    ax.plot([140, 240], [-50, -60], color=C_TEXT, lw=2, zorder=80) # Tie line to bottom Toroid

    # Frame output
    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0)
    fig.clf(); plt.close(fig); gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        phase_ratio = f / float(TOTAL_FRAMES)
        yield (f, phase_ratio)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-229b: RIGID VECTOR VANGUARD [CORES: {cpu_cores}]")
    print(f"Bypassing Nanobanana. Executing Python Solid Polygon Arrays.")
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
