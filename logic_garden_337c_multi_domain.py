"""
SOVEREIGN CODE: logic_garden_337c_multi_domain.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Vectorization
SCENE: Logic Garden 337c (Submarine and Air Integration // Multi-Domain Sensor Fusion)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING, MILITARY DOCTRINE
HOTFIX: Linear 20.0s Sequence. Daylight Protocol. Absolute Camera Lock. Tuple Integrity.
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
OUT_DIR = "frames_337c_multidomain"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Oceanic Matrix / Base Grid
C_STEEL     = '#606065'   # IJN Convoy Base / Unaware State
C_DARK      = '#202025'   # Airborne & Submarine Nodes
C_CYAN      = '#00FFFF'   # Active Radar Sweeps / Wakes
C_MAGENTA   = '#FF0055'   # Keel Break / Lethal Spallation
C_GOLD      = '#FFB300'   # Encrypted Telemetry Link / Torpedo Nodes
C_MANTIS    = '#00FF00'   # Target Sunk / Combat Resolved

# -------- KINEMATIC BATTLEFIELD PARAMETERS --------
# Vector velocities
V_IJN = 20.0  
V_AIR = -35.0  

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

    # 1. POSITION VECTORS
    pos_ijn = (-300 + (t * V_IJN), 400)
    pos_air = (350 + (t * V_AIR), -600)
    pos_sub = (0, 50)  # Submarine holding central intercept position 

    # 2. AIR-SEARCH RADAR SYSTEM (C_CYAN)
    # The aircraft emits continuous sweeping arcs to detect surface elements
    pulse_interval = 2.0
    for pulse_time in np.arange(0, t, pulse_interval):
        r_pulse = (t - pulse_time) * 450.0
        if r_pulse < 2000:
            a_pulse = max(0.0, 1.0 - (r_pulse / 1500.0))
            ax.add_patch(patches.Circle(pos_air, r_pulse, fill=False, edgecolor=C_CYAN, lw=2, alpha=a_pulse, zorder=1))

    # The exact moment the radar arc geographically strikes the IJN target
    target_lock = t >= 2.5 
    
    # 3. DATALINK / O(1) SENSOR FUSION (C_GOLD)
    if target_lock and t < 16.5:
        # Paint the IJN Node
        ax.add_patch(patches.Rectangle((pos_ijn[0]-40, pos_ijn[1]-20), 80, 40, fill=False, edgecolor=C_GOLD, lw=2, zorder=6))
        
        # Telemetry linkage from Air to Sub
        ax.plot([pos_air[0], pos_sub[0]], [pos_air[1], pos_sub[1]], color=C_GOLD, lw=2, linestyle='--', zorder=4)
        
        # Binary data packets traveling the telemetry line
        packet_prg = (t * 5.0) % 1.0
        dp_x = pos_air[0] + (pos_sub[0] - pos_air[0]) * packet_prg
        dp_y = pos_air[1] + (pos_sub[1] - pos_air[1]) * packet_prg
        ax.scatter(dp_x, dp_y, c=C_BG, edgecolors=C_GOLD, s=60, marker='D', lw=2, zorder=5)

    # 4. KINEMATIC TORPEDO EXECUTION (MAGNETIC INFLUENCE EXPLODER)
    LAUNCH_TIME = 8.5
    IMPACT_TIME = 16.0
    FLY_TIME = IMPACT_TIME - LAUNCH_TIME

    if t > LAUNCH_TIME:
        # Calculate ideal intercept (Target pos at IMPACT_TIME)
        int_x = -300 + (IMPACT_TIME * V_IJN)
        int_y = 400
        
        # Fan of 3 vectors
        angles = [-6, 0, 6] 
        
        for deg in angles:
            # Transit ratio
            prg = min(1.0, (t - LAUNCH_TIME) / FLY_TIME)
            
            # Base intercept trajectory
            bx = pos_sub[0] + (int_x - pos_sub[0]) * prg
            by = pos_sub[1] + (int_y - pos_sub[1]) * prg
            
            # Apply fan spread relative to transit distance
            rad = np.radians(deg)
            dx = bx - pos_sub[0]
            dy = by - pos_sub[1]
            # Rotation matrix for slight scatter
            f_x = pos_sub[0] + (dx * np.cos(rad) - dy * np.sin(rad))
            f_y = pos_sub[1] + (dx * np.sin(rad) + dy * np.cos(rad))
            
            if t < IMPACT_TIME:
                # Drawing Torpedo in transit
                # Wake trail
                px = pos_sub[0] + (dx * np.cos(rad) - dy * np.sin(rad)) * (prg - 0.15) if prg > 0.15 else pos_sub[0]
                py = pos_sub[1] + (dx * np.sin(rad) + dy * np.cos(rad)) * (prg - 0.15) if prg > 0.15 else pos_sub[1]
                ax.plot([px, f_x], [py, f_y], color=C_CYAN, lw=2, alpha=0.6, zorder=3)
                # Warhead Core
                ax.scatter(f_x, f_y, c=C_DARK, edgecolors=C_GOLD, s=40, lw=1.5, zorder=7)
                
                # Active Ping (Magnetic anomaly detector)
                ax.add_patch(patches.Circle((f_x, f_y), 25, fill=False, edgecolor=C_CYAN, lw=1, alpha=1.0-(prg%0.5)*2, zorder=6))

            elif deg == 0:
                # Center Torpedo achieves Magnetic Hull Intersect (Spallation)
                exp_t = t - IMPACT_TIME
                if exp_t < 1.5:
                    r_blast = 250 * (exp_t / 0.2) if exp_t < 0.2 else 250 + 80*(exp_t - 0.2)
                    a_blast = max(0.0, 1.0 - (exp_t / 1.5))
                    
                    # Core Magnetic Break (Breaking the keel from underneath)
                    ax.scatter(int_x, int_y, s=r_blast*25, c=C_BG, edgecolors=C_MAGENTA, lw=12*a_blast, alpha=a_blast, zorder=20)
                    ax.scatter(int_x, int_y, s=r_blast*10, c=C_GOLD, alpha=a_blast, edgecolors='none', zorder=21)
                    
                    # Structural fault line ripping cleanly through the Matrix
                    ax.plot([int_x-100, int_x+100], [int_y, int_y], color=C_TEXT, lw=4*a_blast, linestyle='--', zorder=22)

    # 5. DRAWING THE NODES
    # USN Aircraft
    ax.add_patch(patches.RegularPolygon(pos_air, numVertices=3, radius=30, facecolor=C_DARK, edgecolor=C_CYAN, lw=2, orientation=np.radians(180), zorder=8))
    # USN Submarine
    ax.add_patch(patches.Rectangle((pos_sub[0]-40, pos_sub[1]-15), 80, 30, facecolor=C_BG, edgecolor=C_DARK, lw=3, zorder=8))
    if target_lock: ax.scatter(pos_sub[0], pos_sub[1], c=C_GOLD, s=20, zorder=8.1)
    
    # IJN Convoy
    if t < IMPACT_TIME + 0.1:
        # Full convoy layout
        ax.add_patch(patches.Rectangle((pos_ijn[0]-60, pos_ijn[1]-20), 120, 40, facecolor=C_STEEL, edgecolor=C_BG, lw=2, zorder=7))
        # Escorts
        ax.scatter(pos_ijn[0]-40, pos_ijn[1]+40, c=C_STEEL, s=60, marker='s', zorder=7)
        ax.scatter(pos_ijn[0]+40, pos_ijn[1]-40, c=C_STEEL, s=60, marker='s', zorder=7)
    else:
        # Broken Keel (Target Sinking)
        drift = (t - IMPACT_TIME) * 5
        ax.plot([pos_ijn[0]-60, pos_ijn[0]-10], [pos_ijn[1]+drift, pos_ijn[1]-drift*2], color=C_STEEL, lw=15, alpha=0.5, zorder=6)
        ax.plot([pos_ijn[0]+10, pos_ijn[0]+60], [pos_ijn[1]-drift*2, pos_ijn[1]+drift], color=C_STEEL, lw=15, alpha=0.5, zorder=6)
        ax.scatter(pos_ijn[0], pos_ijn[1], s=500, c=C_BG, edgecolors=C_TEXT, lw=3, marker='x', alpha=max(0, 1.0-(drift/20)), zorder=7)

    # ====================================================
    # 6. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    # Top Header [Strict Tuples]
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-337c :: MULTI-DOMAIN SENSOR FUSION", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] AIRBORNE RADAR & SUBMARINE KINEMATIC INTEGRATION", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    # CIC Telemetry HUD
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    if not target_lock:
        state_air = "AIRSPACE SCANNING // ZERO METRIC CONTACTS"
        col_air = C_CYAN
        state_sub = "SUBMERGED // BLIND // RADIO SILENCE"
        col_sub = C_STEEL
        data_link = "OFFLINE"
        col_link = C_STEEL
    elif t < LAUNCH_TIME:
        state_air = "TARGET PAINTED // GENERATING FIRE-CONTROL SOLUTION"
        col_air = C_CYAN
        state_sub = "RECEIVING TELEMETRY // ALIGNING TUBES"
        col_sub = C_GOLD
        data_link = "ACTIVE (ENCRYPTED_UHF) -> C_GOLD DOWNSTREAM"
        col_link = C_GOLD
    elif t < IMPACT_TIME:
        state_air = "MONITORING BALLISTIC KINEMATICS"
        col_air = C_STEEL
        state_sub = "TORPEDOES AWAY // VECTORS RUNNING HOT"
        col_sub = C_CYAN
        data_link = f"TTI (TIME TO INTERCEPT) : {(IMPACT_TIME - t):>04.1f}s"
        col_link = C_GOLD
    else:
        state_air = "MAGNETIC ANOMALY DETECTED // KEEL BROKEN"
        col_air = C_MANTIS
        state_sub = "TARGET DESTROYED // RETURNING TO SILENCE"
        col_sub = C_MANTIS
        data_link = "O(1) ARCHITECTURAL OBLITERATION CONFIRMED"
        col_link = C_MAGENTA

    ax.text(-500, -760, "SYS_01 [AIRBORNE RADAR] :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, state_air, color=col_air, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [SUBMARINE NODE] :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, state_sub, color=col_sub, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "TARGETING DATALINK      :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, data_link, color=col_link, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider [Strict Tuples]
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=col_link, zorder=83))

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
    print(f"LG-337c: MULTI-DOMAIN FUSION [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE] [Tuples Sealed]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
