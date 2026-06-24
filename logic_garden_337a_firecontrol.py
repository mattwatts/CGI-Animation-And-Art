"""
SOVEREIGN CODE: logic_garden_337_firecontrol.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Vectorization
SCENE: Logic Garden 337 (Fire-Control & Night Combat // USN vs IJN)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING, MILITARY DOCTRINE
HOTFIX: Linear 20.0s Sequence. Daylight Protocol. Syntax Rupture Sealed.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
DURATION = 20.0  # 20.0 Second Forward Execution
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_337_firecontrol"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Oceanic Matrix / Base Grid
C_STEEL     = '#606065'   # IJN Node / Optical Limits
C_DARK      = '#202025'   # USN Node Center
C_CYAN      = '#00FFFF'   # Radar Matrix / Detection Network
C_MAGENTA   = '#FF0055'   # Lethal Shockwave / Spallation
C_GOLD      = '#FFB300'   # Target Lock / Artillery Shells / CIC Logic
C_MANTIS    = '#00FF00'   # Terminal Confirm

# -------- BATTLEFIELD MATRIX --------
# Coordinate Tuples
N_USN = (0, -400)
N_IJN = (0, 400)
DIST_MAX = abs(N_USN[1] - N_IJN[1]) # 800

def draw_industrial_grid(ax):
    """Draw the Oceanic Coordinate Matrix"""
    for i in range(-5, 6):
        ax.plot([i*100, i*100], [-960, 960], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)
    for j in range(-9, 10):
        ax.plot([-540, 540], [j*100, j*100], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)

def render_frame(packet):
    f, phase_ratio = packet
    t = phase_ratio * DURATION 
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    
    # ----------------------------------------------------
    # BARE-METAL CAMERA LOCK: ALL AUTO-SCALING ANNIHILATED
    # ----------------------------------------------------
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)
    ax.autoscale(False)

    draw_industrial_grid(ax)

    # ====================================================
    # 1. THE BIOLOGICAL NODE (IJN: OPTICAL RANGEFINDER)
    # ====================================================
    # The optical cone is limited to R=300, looking south.
    # It sweeps slowly back and forth over a narrow angle.
    opt_angle = np.sin(t * 1.5) * 45  # -45 to +45 degree sweep
    opt_r = 300
    
    # Draw arc and cone
    cone_pts = [N_IJN]
    for ang in np.linspace(opt_angle - 15, opt_angle + 15, 10):
        rad_ang = np.radians(ang - 90) # Face South
        cx = N_IJN[0] + opt_r * np.cos(rad_ang)
        cy = N_IJN[1] + opt_r * np.sin(rad_ang)
        cone_pts.append((cx, cy))
    
    if t < 16.0:
        poly_opt = patches.Polygon(cone_pts, facecolor=C_TITANIUM, edgecolor='none', alpha=0.4, zorder=1)
        ax.add_patch(poly_opt)
        # Limit arc rim
        ax.plot([p[0] for p in cone_pts[1:]], [p[1] for p in cone_pts[1:]], color=C_STEEL, lw=2, linestyle='--', zorder=2)
    
    # IJN Hull [Hex Node] perfectly synced hardware state
    if t < 16.0:
        ax.add_patch(patches.RegularPolygon(N_IJN, numVertices=6, radius=40, facecolor=C_GOLD if t > 4 else C_STEEL, edgecolor=C_BG, lw=2, zorder=5))
        ax.add_patch(patches.Circle(N_IJN, 15, facecolor=C_BG, zorder=5.1))

    # ====================================================
    # 2. THE ALGORITHMIC NODE (USN: CENTIMETRIC RADAR)
    # ====================================================
    # Omnidirectional 360 sweep. 1 full rotation every 3.0 seconds
    rad_speed = (t % 3.0) / 3.0
    sweep_ang = 90 - (rad_speed * 360) # Start pointing North (90), sweep clockwise
    rad_dist = 1100
    
    # Draw fading radar wedge
    sweep_pts = [N_USN]
    for ang in np.linspace(sweep_ang + 25, sweep_ang, 20):
        r_ang = np.radians(ang)
        cx = N_USN[0] + rad_dist * np.cos(r_ang)
        cy = N_USN[1] + rad_dist * np.sin(r_ang)
        sweep_pts.append((cx, cy))
    
    c_rad = mcolors.to_rgba(C_CYAN, 0.1)
    ax.add_patch(patches.Polygon(sweep_pts, facecolor=c_rad, edgecolor='none', zorder=1))
    
    # Sweep Leading Edge
    lead_x = N_USN[0] + rad_dist * np.cos(np.radians(sweep_ang))
    lead_y = N_USN[1] + rad_dist * np.sin(np.radians(sweep_ang))
    ax.plot([N_USN[0], lead_x], [N_USN[1], lead_y], color=C_CYAN, lw=2, zorder=2)

    # USN Hull [Heavy Square Node]
    ax.add_patch(patches.Rectangle((-45, -445), 90, 90, facecolor=C_DARK, edgecolor=C_BG, lw=2, zorder=5))
    ax.add_patch(patches.Circle(N_USN, 20, facecolor=C_CYAN, zorder=5.1))

    # ====================================================
    # 3. CIC INTEGRATION (THE TARGET LOCK)
    # ====================================================
    # Lock is established when the sweep passes over the IJN target (Angle = 90)
    # In a 3.0 second orbit starting at 90 and sweeping clockwise, it hits at t=0, t=3, t=6, t=9
    # We simulate a "confirmed lock" after the second sweep (t > 4)
    target_locked = t >= 4.0
    
    if target_locked and t < 16.0:
        # Paint the target with a tracking box
        ax.add_patch(patches.Rectangle((-60, 340), 120, 120, fill=False, edgecolor=C_GOLD, lw=4, zorder=6))
        # Draw the invisible data-link line
        ax.plot([N_USN[0], N_IJN[0]], [N_USN[1], N_IJN[1]], color=C_GOLD, lw=1.5, linestyle=':', zorder=4)

    # ====================================================
    # 4. KINEMATIC ARTILLERY (VT PROXIMITY FUZE)
    # ====================================================
    FIRE_TIME = 10.0
    IMPACT_TIME = 15.0
    FLY_TIME = IMPACT_TIME - FIRE_TIME
    
    # Three shells launched in tight succession
    shells = [FIRE_TIME, FIRE_TIME + 0.3, FIRE_TIME + 0.6]
    
    for s_launch in shells:
        if s_launch <= t <= IMPACT_TIME + 1.0:
            prg = (t - s_launch) / FLY_TIME
            if prg < 1.0:
                # Shell in flight
                sh_x = 0
                sh_y = N_USN[1] + (DIST_MAX * prg)
                # Draw Shell
                ax.scatter(sh_x, sh_y, c=C_BG, edgecolors=C_GOLD, s=60, lw=3, zorder=10)
                ax.plot([sh_x, sh_x], [sh_y-60, sh_y], color=C_GOLD, lw=2, alpha=0.5, zorder=9)
                
                # ------ The Proximity Fuze Engine ------
                # Emitting miniaturized radar rings checking for bounding box
                fuze_r = (t * 200) % 40 # Expanding rings
                ax.add_patch(patches.Circle((sh_x, sh_y), fuze_r, fill=False, edgecolor=C_CYAN, lw=1, alpha=1.0-(fuze_r/40), zorder=8))
                
            else:
                # Terminal Spallation / Airburst
                # Proximity fuzes detonate slightly before/above hull contact
                exp_prg = (t - (s_launch + FLY_TIME)) / 1.0
                if exp_prg < 1.0:
                    r_blast = 200 * exp_prg
                    a_blast = 1.0 - exp_prg
                    # Airburst shrapnel cone
                    ax.scatter(0, N_IJN[1]-20, c=C_BG, s=r_blast*20, edgecolors=C_MAGENTA, lw=10*a_blast, alpha=a_blast, zorder=20)
                    ax.scatter(0, N_IJN[1]-20, c=C_GOLD, s=r_blast*10, alpha=a_blast, zorder=21)

    # Destruct State of IJN Node
    if t >= IMPACT_TIME + 0.5:
        # Wreckage matrix
        ax.scatter(N_IJN[0], N_IJN[1], s=400, c=C_BG, edgecolors=C_STEEL, lw=4, marker='X', zorder=4)

    # ====================================================
    # 5. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    # Top Header [Strict Tuples]
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-337 :: ASYMMETRIC COMBAT DOCTRINE", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] ALGORITHMIC DETECTION VS BIOLOGICAL OPTICS", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    # CIC Telemetry HUD
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    if t < 4.0:
        state = "BLIND SWEEP // INFORMATION DEPRIVATION"
        col_main = C_STEEL
        tgt_data = "TARGET POSITION: UNKNOWN | RANGE: NaN"
    elif t < 10.0:
        state = "RADAR CONTACT // CIC FIRE-CONTROL INTEGRATION"
        col_main = C_CYAN
        tgt_data = f"TARGET LOCKED | BRG: 000 | RNG: {DIST_MAX}.00m"
    elif t < 15.0:
        state = "FIRING // RADAR-DIRECTED ARTILLERY EN ROUTE"
        col_main = C_GOLD
        tgt_data = f"VT-FUZE ACTIVE | TTI: {(15.0 - t):>04.1f}s"
    else:
        state = "TERMINAL AIRBURST // TARGET OBLITERATED"
        col_main = C_MAGENTA
        tgt_data = "TARGET POSITION: NEUTRALIZED"

    ax.text(-500, -760, "SYS_01 STATE [OPTICAL IJN] :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, "BLIND", color=C_STEEL if t < 13 else C_MAGENTA, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 STATE [RADAR USN]   :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, state, color=col_main, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "CIC TARGETING TELEMETRY    :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, tgt_data, color=C_GOLD if target_locked else C_STEEL, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider [Strict Tuples]
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=col_main, zorder=83))

    # Sovereign Execution Output
    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    # Absolute Memory Annihilation
    plt.close('all')
    gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-337: FIRE-CONTROL TENSOR [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE] [Tuples Sealed]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
