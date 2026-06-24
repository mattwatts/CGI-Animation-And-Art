"""
SOVEREIGN CODE: logic_garden_337b_fleet_air_defense.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Vectorization
SCENE: Logic Garden 337b (Fleet Air Defense // Radar & VT Fuzes)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING, MILITARY DOCTRINE
HOTFIX: Linear 20.0s Sequence. Daylight Protocol. Absolute Camera & Tuple Lock.
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
OUT_DIR = "frames_337b_fleet_air_defense"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Airspace Matrix Grid
C_STEEL     = '#606065'   # Incoming Aircraft Swarm (IJN)
C_DARK      = '#202025'   # Fleet Node Center (USN)
C_CYAN      = '#00FFFF'   # Air-Search Radar / VT Transceivers
C_MAGENTA   = '#FF0055'   # Lethal Airburst / Spallation fragmentation
C_GOLD      = '#FFB300'   # Fire-Control Lock / Anti-Air Shells
C_MANTIS    = '#00FF00'   # Airspace Secured

# -------- BATTLEFIELD MATRIX --------
# Base Coordinates
N_FLEET = (0, -650)

# Precompute Aircraft Trajectories
N_AIRCRAFT = 5
V_AIRCRAFT_SPEED = 70.0 # units per second downward

# Start positions (staggered V-formation)
A_START_X = np.array([0, -180, 180, -360, 360])
A_START_Y = np.array([1000, 1150, 1150, 1300, 1300])

# Precompute Shell Launch Intercepts
# Calculating exactly when the shell must be fired to hit the aircraft at specific altitudes
INTERCEPT_Y = np.array([200, 150, 150, 100, 100])
SHELL_SPEED = 250.0

shell_launch_times = []
shell_impact_times = []
for i in range(N_AIRCRAFT):
    # Time aircraft reaches intercept Y
    t_aircraft_reach = (A_START_Y[i] - INTERCEPT_Y[i]) / V_AIRCRAFT_SPEED
    # Time shell takes to reach intercept Y from Fleet Y
    t_shell_fly = (INTERCEPT_Y[i] - N_FLEET[1]) / SHELL_SPEED
    # Launch time is when aircraft reaches intercept minus shell flight time
    t_launch = t_aircraft_reach - t_shell_fly
    shell_launch_times.append(t_launch)
    shell_impact_times.append(t_aircraft_reach)

def draw_industrial_grid(ax):
    """Draw the 3D Airspace Coordinate Matrix"""
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
    # 1. THE ALGORITHMIC NODE (USN RADAR SWEEP)
    # ====================================================
    # Fleet Base
    ax.add_patch(patches.RegularPolygon(N_FLEET, numVertices=8, radius=60, facecolor=C_DARK, edgecolor=C_BG, lw=3, zorder=5))
    ax.add_patch(patches.Circle(N_FLEET, 20, facecolor=C_CYAN, zorder=5.1))
    
    # Massive air-search radar emitting pulses outwards
    pulse_freq = 2.0
    for p_time in np.arange(0, t, pulse_freq):
        r_pulse = (t - p_time) * 400.0
        if r_pulse < 2500:
            a_pulse = max(0.0, 1.0 - (r_pulse / 2500.0))
            ax.add_patch(patches.Circle(N_FLEET, r_pulse, fill=False, edgecolor=C_CYAN, lw=2, alpha=a_pulse, zorder=1))

    radar_contact = t > 3.0 # Targets acquired globally after initial sweeps

    # ====================================================
    # 2. INCOMING AERIAL THREAT (IJN KAMIKAZE VECTORS)
    # ====================================================
    threats_active = 0
    
    for i in range(N_AIRCRAFT):
        t_impact = shell_impact_times[i]
        
        if t < t_impact:
            threats_active += 1
            # Current Aircraft Pos
            cur_y = A_START_Y[i] - (V_AIRCRAFT_SPEED * t)
            cur_x = A_START_X[i]
            
            # Draw Vector Line
            ax.plot([cur_x, cur_x], [cur_y, 900], color=C_STEEL, lw=2, linestyle='--', zorder=3)
            # Draw Aircraft Node
            ax.scatter(cur_x, cur_y, s=150, c=C_BG, edgecolors=C_STEEL, lw=3, marker='v', zorder=10)
            
            # Fire-Control Target Lock (CIC)
            if radar_contact:
                # Predictive Lead marker
                lead_y = cur_y - (V_AIRCRAFT_SPEED * 1.5)
                ax.add_patch(patches.Rectangle((cur_x - 30, cur_y - 30), 60, 60, fill=False, edgecolor=C_GOLD, lw=2, zorder=9))
                ax.scatter(cur_x, lead_y, s=30, c=C_GOLD, marker='+', zorder=9)
                ax.plot([cur_x, cur_x], [cur_y, lead_y], color=C_GOLD, lw=1, alpha=0.5, zorder=8)
                
        else:
            # Aircraft is destroyed. Draw wreck drift and smoke
            drift_t = t - t_impact
            if drift_t < 4.0:
                cur_y = INTERCEPT_Y[i] - (V_AIRCRAFT_SPEED * 0.4 * drift_t) # Falling slower
                ax.scatter(A_START_X[i], cur_y, s=150, c=C_STEEL, alpha=1.0-(drift_t/4.0), marker='x', zorder=2)

    # ====================================================
    # 3. KINEMATIC INTERCEPT (VT FUZE ARTILLERY)
    # ====================================================
    for i in range(N_AIRCRAFT):
        t_l = shell_launch_times[i]
        t_imp = shell_impact_times[i]
        
        if t_l <= t <= t_imp + 1.2:
            fly_t = t - t_l
            sh_x = A_START_X[i]
            
            if t < t_imp:
                # Shell ascending
                sh_y = N_FLEET[1] + (SHELL_SPEED * fly_t)
                
                # Draw the actual 5-inch shell trajectory
                ax.plot([sh_x, sh_x], [N_FLEET[1], sh_y], color=C_GOLD, lw=3, alpha=0.7, zorder=11)
                ax.scatter(sh_x, sh_y, s=80, c=C_DARK, edgecolors=C_GOLD, lw=2, zorder=12)
                
                # === VT FUZE ELECTROMAGNETIC TRANSMISSION ===
                # The shell emits miniature high-frequency radar pulses
                vt_r = (t * 400) % 70 # 70 unit lethal radius detection zone
                ax.add_patch(patches.Circle((sh_x, sh_y), vt_r, fill=False, edgecolor=C_CYAN, lw=1.5, alpha=1.0-(vt_r/70.0), zorder=13))
                
                # The structural lethal box (The mathematical trigger volume)
                ax.add_patch(patches.Circle((sh_x, sh_y), 70, fill=False, edgecolor=C_CYAN, lw=0.5, linestyle=':', zorder=13))
                
            else:
                # PROXIMITY TRIGGERED -> AIRBURST SPALLATION
                exp_t = t - t_imp
                if exp_t < 1.2:
                    r_blast = 250 * (exp_t / 0.15) if exp_t < 0.15 else 250 + 50*(exp_t - 0.15)
                    a_blast = 1.0 - (exp_t / 1.2)
                    
                    int_y = INTERCEPT_Y[i]
                    
                    # Outer Shockwave
                    ax.scatter(sh_x, int_y, s=r_blast*40, c=C_BG, edgecolors=C_MAGENTA, lw=8*a_blast, alpha=a_blast, zorder=20)
                    # Inner Thermal Flash
                    ax.scatter(sh_x, int_y, s=r_blast*15, c=C_GOLD, alpha=a_blast, edgecolors='none', zorder=21)
                    
                    # Lethal Spallation Fragmentation Ring (Tearing the target apart)
                    ax.add_patch(patches.Circle((sh_x, int_y), r_blast, fill=False, edgecolor=C_TEXT, lw=4*a_blast, linestyle='--', zorder=22))

    # ====================================================
    # 4. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    # Top Header [Strict Tuples]
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-337b :: FLEET AIR DEFENSE TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] VT FUZE RADAR & KINEMATIC INTERCEPTION", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    # CIC Telemetry HUD
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    if not radar_contact:
        state = "AIRSPACE SCANNING // ZERO METRIC CONTACTS"
        col_main = C_CYAN
    elif threats_active > 0:
        state = f"THREATS ACTIVE: {threats_active} // FIRE-CONTROL ENGAGED"
        col_main = C_GOLD
    else:
        state = "ALL TARGETS NEUTRALIZED // AIRSPACE SECURED"
        col_main = C_MANTIS

    ax.text(-500, -760, "SYS_01 STATE [OPTICAL BASE] :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(30, -760, "INEFFECTIVE / BIOLOGICAL LAG", color=C_STEEL, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 STATE [CIC RADAR]    :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(30, -800, state, color=col_main, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    active_vt = sum((t > shell_launch_times[i] and t < shell_impact_times[i]) for i in range(N_AIRCRAFT))
    ax.text(-500, -840, "VT FUZE TELEMETRY TRACKING  :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    
    if active_vt > 0:
        ax.text(30, -840, f"ACTIVE SHELLS IN BALLISTIC TRANSIT: {active_vt}", color=C_CYAN, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    else:
        ax.text(30, -840, "STANDBY", color=C_STEEL, fontsize=15, fontname='monospace', weight='bold', zorder=82)

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
    print(f"LG-337b: FLEET AIR DEFENSE [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE] [Tuples Sealed]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
