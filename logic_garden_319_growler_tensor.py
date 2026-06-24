"""
SOVEREIGN CODE: logic_garden_319_growler_tensor.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 319 (EA-18G Growler // SEAD Electromagnetic Tensor)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Monolithic rendering. Solid F/A-18F topology. Rigid RF emission arcs.
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
OUT_DIR = "frames_319_growler_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#A0A0A5'
C_STEEL     = '#404045'
C_DARK      = '#1A1A20'   # Two-seat Canopy / Intakes
C_AZURE     = '#007FFF'   # ALQ-99 Low-Band Jamming Waveforms
C_MAGENTA   = '#FF0055'   # ALQ-218 Receiver Data-Link / Targeting
C_GOLD      = '#FFB300'   # AGM-88 HARM Seeker Head
C_CYAN      = '#00FFFF'   # Twin F414 Engine Core
C_WHITE     = '#FFFFFF'

# ------------------------------------------------------------------
# O(1) TENSOR KINEMATICS (SLIPSTREAM)
# ------------------------------------------------------------------
np.random.seed(319)

# Atmospheric Shear (Supersonic SEAD transit)
N_STREAKS = 1200
streak_x = np.random.uniform(-540, 540, N_STREAKS)
streak_y_offset = np.random.uniform(0, 1920, N_STREAKS)
streak_length = np.random.uniform(100, 400, N_STREAKS)
streak_width = np.random.uniform(1.0, 3.0, N_STREAKS)

# ------------------------------------------------------------------
# RIGID POLYGON AERODYNAMICS (EA-18G BUILDER)
# ------------------------------------------------------------------
def draw_symmetric_poly(ax, points, facecolor, edgecolor='none', lw=1, zorder=5):
    # Left side
    poly_l = patches.Polygon([[-p[0], p[1]] for p in points], facecolor=facecolor, edgecolor=edgecolor, lw=lw, zorder=zorder)
    # Right side
    poly_r = patches.Polygon(points, facecolor=facecolor, edgecolor=edgecolor, lw=lw, zorder=zorder)
    ax.add_patch(poly_l)
    ax.add_patch(poly_r)

def build_growler(ax, y_offset=0):
    # 1. Main Fuselage
    fuse_pts = [[0, 300], [25, 230], [35, 100], [40, -150], [25, -280], [0, -280]]
    draw_symmetric_poly(ax, fuse_pts, C_TITANIUM, zorder=5)
    
    # Centerline Ridge / Avionics Spine
    spine_pts = [[0, 260], [10, 180], [12, 50], [0, -200]]
    draw_symmetric_poly(ax, spine_pts, C_STEEL, zorder=5.1)

    # 2. Leading Edge Root Extensions (LERX)
    lerx_pts = [[25, 200], [50, 100], [60, 50], [35, 50]]
    draw_symmetric_poly(ax, lerx_pts, C_TITANIUM, zorder=4.9)

    # 3. Two-Seat Tandem Canopy (Pilot & Electronic Warfare Officer)
    canopy_pts = [[0, 240], [15, 190], [18, 110], [0, 80]]
    draw_symmetric_poly(ax, canopy_pts, C_DARK, zorder=6)

    # 4. Main Swept Wings
    wing_pts = [[45, 50], [220, -50], [220, -100], [60, -150], [40, -130]]
    draw_symmetric_poly(ax, wing_pts, C_TITANIUM, edgecolor=C_STEEL, lw=1, zorder=4.8)

    # 5. Twin Canted Vertical Stabilizers (Top-down mapped)
    v_stab_pts = [[30, -180], [60, -260], [50, -300], [20, -250]]
    draw_symmetric_poly(ax, v_stab_pts, C_STEEL, zorder=6.1)

    # 6. Horizontal Stabilators
    h_stab_pts = [[35, -220], [120, -270], [120, -320], [25, -300]]
    draw_symmetric_poly(ax, h_stab_pts, C_TITANIUM, zorder=4.7)

    # 7. Rectangular Intakes (Top-down leading edge under LERX)
    draw_symmetric_poly(ax, [[35, 70], [55, 60], [55, 40], [35, 50]], C_DARK, zorder=5.2)

    # ------------------------------------------------------------------
    # SEAD PAYLOAD ARRAY
    # ------------------------------------------------------------------
    # Wingtip ALQ-218 Receivers (replaces Sidewinders)
    tip_pts = [[220, -40], [230, -40], [230, -110], [220, -110]]
    draw_symmetric_poly(ax, tip_pts, C_TEXT, zorder=4.9)

    # Underwing Pylons & AGM-88 HARM targeting missiles
    harm_pts = [[140, 0], [148, -10], [148, -100], [140, -100]]
    draw_symmetric_poly(ax, harm_pts, C_STEEL, zorder=4.95)
    # HARM Seeker head
    draw_symmetric_poly(ax, [[140, 5], [144, 12], [148, 5]], C_GOLD, zorder=4.96)

    # ALQ-99 Tactical Jamming Pods (Mid-wing pylons & Centerline)
    alq_pts = [[100, 20], [115, 10], [115, -120], [100, -120]]
    draw_symmetric_poly(ax, alq_pts, C_TEXT, zorder=4.95)
    
    # Centerline ALQ-99
    ax.add_patch(patches.Rectangle((-15, -50), 30, -140, facecolor=C_TEXT, zorder=4.5))

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

    # 1. CONTINUOUS SLIPSTREAM (Supersonic Transit)
    slip_velocity = 6000.0 
    current_streak_y = ((streak_y_offset - phase_ratio * slip_velocity) % 1920) - 960
    
    for i in range(N_STREAKS):
        y_top = current_streak_y[i]
        y_bottom = current_streak_y[i] - streak_length[i]
        if y_top > -960 and y_bottom < 960:
            ax.plot([streak_x[i], streak_x[i]], [y_bottom, y_top], 
                    color=C_TITANIUM, lw=streak_width[i], alpha=0.3, zorder=1)

    # 2. ELECTROMAGNETIC WARFARE KINEMATICS (SEAD JAMMING WAVES Z=3)
    # Mathematical representations of RF jamming frequencies radiating from ALQ-99 and ALQ-218
    num_waves = 5
    for w in range(num_waves):
        # Local wave expansion loop
        wave_phase = (phase_ratio + w * (1.0/num_waves)) % 1.0
        wave_radius = 50 + (wave_phase * 1200) # Expands massively
        wave_alpha = 1.0 - wave_phase # Fades to 0
        
        # Centerline ALQ-99 Emission (Low Band Arc)
        arc_c = patches.Arc((0, -120), wave_radius*2, wave_radius*2, angle=0, theta1=210, theta2=330, color=C_AZURE, lw=8, alpha=wave_alpha*0.6, zorder=3)
        ax.add_patch(arc_c)

        # Wingtip ALQ-218 Data-link / Targeting arrays (Magenta pings forward)
        tip_r = 20 + (wave_phase * 400)
        arc_l = patches.Arc((-225, -40), tip_r*2, tip_r*2, angle=0, theta1=30, theta2=150, color=C_MAGENTA, lw=4, alpha=wave_alpha*0.8, zorder=3)
        arc_r = patches.Arc((225, -40), tip_r*2, tip_r*2, angle=0, theta1=30, theta2=150, color=C_MAGENTA, lw=4, alpha=wave_alpha*0.8, zorder=3)
        ax.add_patch(arc_l)
        ax.add_patch(arc_r)

    # 3. EA-18G RIGID AERODYNAMIC PLANFORM (Z=4 to 6)
    build_growler(ax)

    # 4. F414 ENGINE EXHAUST (Eulerian Thrust Vectoring)
    # Engine bells are at Y = -280, X = +/- 15
    thrust_length = 250 + np.sin(phase_ratio * 40 * np.pi) * 20 # Slight micro-flicker
    for ex_x in [-15, 15]:
        poly_flame = patches.Polygon([[ex_x - 12, -280], [ex_x + 12, -280], [ex_x, -280 - thrust_length]], facecolor=C_CYAN, alpha=0.8, zorder=4.5)
        poly_core = patches.Polygon([[ex_x - 5, -280], [ex_x + 5, -280], [ex_x, -280 - thrust_length*0.6]], facecolor=C_WHITE, alpha=0.9, zorder=4.6)
        ax.add_patch(poly_flame)
        ax.add_patch(poly_core)

    # 5. ZERO-TEMPERATURE WIDGETS
    ax.text(-500, 880, "LG-319 :: EA-18G GROWLER", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, 840, "[SFI-1.00] SEAD PROTOCOL // EW SPECTRUM DOMINANCE", color=C_TEXT, fontsize=12, fontname='monospace', zorder=80)
    
    # Jamming Telemetry Dynamics
    ax.text(-500, -840, "ALQ-99/218 EMISSION TENSOR // HARM LOCK", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=80)
    ax.add_patch(patches.Rectangle((-500, -860), 1000, 4, facecolor=C_TITANIUM, zorder=80))
    ax.add_patch(patches.Rectangle((-500, -860), 1000 * phase_ratio, 4, facecolor=C_AZURE, zorder=81))

    # Electronic Warfare Readout
    ax.text(-500, -780, "TARGETING: ENEMY AIR DEFENSE (SUPPRESSED)", color=C_TEXT, fontsize=12, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, -805, f"RF BROADCAST BOUNDARY: ACTIVE Δ{phase_ratio:.3f} Hz", color=C_AZURE, fontsize=10, fontname='monospace', zorder=80)

    # Structural / Payload Callouts
    ax.text(260, -40, "ALQ-218\nWIDERBAND\nRECEIVER", color=C_MAGENTA, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    ax.plot([230, 255], [-40, -40], color=C_MAGENTA, lw=1.5, zorder=80) 
    
    ax.text(170, 0, "AGM-88\nHARM", color=C_GOLD, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    ax.plot([145, 160], [5, 5], color=C_GOLD, lw=1.5, zorder=80)

    ax.text(-400, -20, "ALQ-99\nTACTICAL\nJAMMING POD", color=C_TEXT, fontsize=10, fontname='monospace', weight='bold', ha='right', zorder=80)
    ax.plot([-115, -315], [-20, -20], color=C_TEXT, lw=1.5, zorder=80)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0)
    fig.clf(); plt.close(fig); gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-319: GROWLER SEAD TENSOR [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
