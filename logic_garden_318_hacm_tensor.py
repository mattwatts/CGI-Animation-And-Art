"""
SOVEREIGN CODE: logic_garden_318_hacm_tensor.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 318 (HACM // Hypersonic Attack Cruise Missile)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Mach 8 Slipstream Tensor / Scramjet Shock Diamonds. Monolithic deployment.
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
OUT_DIR = "frames_318_hacm_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#A0A0A5'
C_STEEL     = '#303035'
C_DARK      = '#15151A'   # Thermal Shielding / Intake Void
C_CYAN      = '#00FFFF'   # Telemetry UI
C_MAGENTA   = '#FF0055'   # Scramjet Shock Diagnostics (Combustion)
C_GOLD      = '#FFB300'   # Leading Edge Hypersonic Friction
C_WHITE     = '#FFFFFF'

# ------------------------------------------------------------------
# O(1) KINEMATIC ARRAYS (SLIPSTREAM & SHOCKWAVES)
# ------------------------------------------------------------------
np.random.seed(318)

# Atmospheric Shear (Moving violently DOWN to simulate Mach 8)
N_STREAKS = 1500
streak_x = np.random.uniform(-540, 540, N_STREAKS)
streak_y_offset = np.random.uniform(0, 1920, N_STREAKS)
streak_length = np.random.uniform(150, 800, N_STREAKS)
streak_width = np.random.uniform(0.5, 2.5, N_STREAKS)

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

    # 1. CONTINUOUS SLIPSTREAM (Mach 8 Equivalent Y-axis drag)
    # V_G = -12000.0 relative velocity
    slip_velocity = 12000.0 
    current_streak_y = ((streak_y_offset - phase_ratio * slip_velocity) % 1920) - 960
    
    for i in range(N_STREAKS):
        y_top = current_streak_y[i]
        y_bottom = current_streak_y[i] - streak_length[i]
        if y_top > -960 and y_bottom < 960:
            ax.plot([streak_x[i], streak_x[i]], [y_bottom, y_top], 
                    color=C_TITANIUM, lw=streak_width[i], alpha=0.3, zorder=1)

    # 2. HYPERSONIC COMPRESSION WAVES (MACH CONE) (Z=2)
    # Originates at the nose (Y=350) and shears outward globally
    cone_w = 480
    cone_base = -960
    # Left Shock boundary
    ax.plot([0, -cone_w], [350, cone_base], color=C_GOLD, lw=2, alpha=0.4, zorder=2)
    ax.plot([0, -cone_w-50], [350, cone_base], color=C_MAGENTA, lw=1, alpha=0.2, zorder=2)
    # Right Shock boundary
    ax.plot([0, cone_w], [350, cone_base], color=C_GOLD, lw=2, alpha=0.4, zorder=2)
    ax.plot([0, cone_w+50], [350, cone_base], color=C_MAGENTA, lw=1, alpha=0.2, zorder=2)

    # 3. HACM WAVERIDER GEOMETRY (Z=5 to Z=7)
    # Absolute zero-rotation, locked dead center on the X-axis.

    # Thermal Leading Edge Shielding (Underlayer)
    poly_shield = patches.Polygon([[0, 360], [-85, -150], [85, -150]], facecolor=C_DARK, zorder=4.9)
    ax.add_patch(poly_shield)

    # Main Fuselage (Ablative Titanium wedges)
    # Left Wing/Body
    poly_left = patches.Polygon([[0, 350], [-80, -150], [-25, -250], [0, -250]], facecolor=C_STEEL, zorder=5)
    ax.add_patch(poly_left)
    # Right Wing/Body (Lighter to simulate fixed directional light / geometry)
    poly_right = patches.Polygon([[0, 350], [80, -150], [25, -250], [0, -250]], facecolor=C_TITANIUM, zorder=5)
    ax.add_patch(poly_right)

    # Central Scramjet Intake Ridge (C_TEXT core running down the spine)
    poly_intake = patches.Polygon([[0, 100], [-30, -50], [-35, -250], [35, -250], [30, -50]], facecolor=C_TEXT, zorder=6)
    ax.add_patch(poly_intake)

    # Inlet compression gap
    rect_inlet = patches.Rectangle((-20, -180), 40, 100, facecolor=C_DARK, zorder=6.5)
    ax.add_patch(rect_inlet)

    # Control Surfaces / Aft Fins (High thermal load)
    poly_fin_l = patches.Polygon([[-80, -150], [-130, -220], [-130, -250], [-25, -250]], facecolor=C_STEEL, edgecolor=C_GOLD, lw=1.5, zorder=4.5)
    poly_fin_r = patches.Polygon([[80, -150], [130, -220], [130, -250], [25, -250]], facecolor=C_TITANIUM, edgecolor=C_GOLD, lw=1.5, zorder=4.5)
    ax.add_patch(poly_fin_l)
    ax.add_patch(poly_fin_r)

    # 4. SCRAMJET SHOCK DIAMONDS (Dynamic Eulerian Phase-Lock) (Z=3)
    # Exhaust runs cleanly out the back. Wraps within a local constrained Bounding Box.
    # Velocity of exhaust is relative to the ship.
    shock_v = 400.0
    for s_idx in range(6):
        # Local cyclic offset for each diamond
        raw_y = -250 - ((phase_ratio * shock_v + s_idx * 70) % 400)
        
        # Sizing and alpha bounds (fades out as it moves aft)
        dist_ratio = abs(raw_y + 250) / 400.0
        s_width = 30 * (1.0 - dist_ratio * 0.5)
        s_alpha = 1.0 - dist_ratio
        
        if raw_y < -250:
            diamond = patches.Polygon([
                [0, raw_y + 25], [-s_width, raw_y], [0, raw_y - 25], [s_width, raw_y]
            ], facecolor=C_MAGENTA, alpha=s_alpha, zorder=3)
            ax.add_patch(diamond)
            # Internal hyper-core
            core = patches.Polygon([
                [0, raw_y + 10], [-s_width/2, raw_y], [0, raw_y - 10], [s_width/2, raw_y]
            ], facecolor=C_WHITE, alpha=s_alpha, zorder=3.1)
            ax.add_patch(core)

    # 5. ZERO-TEMPERATURE WIDGETS
    ax.text(-500, 880, "LG-318 :: HYPERSONIC ATTACK CRUISE MISSILE", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, 840, "[SFI-1.00] MACH 8 FLIGHT PROFILE // SCRAMJET TENSOR", color=C_TEXT, fontsize=12, fontname='monospace', zorder=80)
    
    # Telemetry Dynamics
    ax.text(-500, -840, "TARGET ACQUISITION LOGIC // HVT AT RISK", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=80)
    ax.add_patch(patches.Rectangle((-500, -860), 1000, 4, facecolor=C_TITANIUM, zorder=80))
    ax.add_patch(patches.Rectangle((-500, -860), 1000 * phase_ratio, 4, facecolor=C_MAGENTA, zorder=81))

    # Real-Time Mach Indicator
    ax.text(-500, -780, "VELOCITY: MACH 8.02 (LOCKED)", color=C_TEXT, fontsize=12, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, -805, f"COMPRESSION BOUNDARY: NOMINAL Δ{phase_ratio:.3f}", color=C_TITANIUM, fontsize=10, fontname='monospace', zorder=80)

    # Scramjet Structural Callouts
    ax.text(180, -180, "SCRAMJET\nCOMBUSTION\nACTIVE", color=C_MAGENTA, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    ax.plot([100, 170], [-200, -180], color=C_MAGENTA, lw=1.5, zorder=80) 
    
    ax.text(180, 200, "ABLATIVE\nWAVERIDER\nGEOMETRY", color=C_TEXT, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    ax.plot([50, 170], [150, 200], color=C_TEXT, lw=1.5, zorder=80) 

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0)
    fig.clf(); plt.close(fig); gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-318: HACM KINEMATIC TENSOR [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
