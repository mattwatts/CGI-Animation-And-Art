"""
SOVEREIGN CODE: logic_garden_339b_adhominem.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Vectorization
SCENE: Logic Garden 339b (Ad Hominem // Hardware Pointer Error)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING, COGNITIVE LOGIC
HOTFIX: Linear 20.0s Sequence. Daylight Protocol. Absolute Camera Lock. Tuples Sealed.
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
DURATION = 20.0  
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_339b_adhominem"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Environment Matrix
C_STEEL     = '#606065'   # The Hardware Chassis / Physical Casing
C_DARK      = '#202025'   # Logic Cores
C_CYAN      = '#00FFFF'   # The Data Payload (The Mathematical Argument)
C_MAGENTA   = '#FF0055'   # Pointer Error / Lethal Strike
C_GOLD      = '#FFB300'   # Standard Optical Scan / Targeting
C_MANTIS    = '#00FF00'   # Terminal Green 

def draw_industrial_grid(ax):
    """Draw the Structural Matrix"""
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
    
    # BARE-METAL CAMERA LOCK
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)
    ax.autoscale(False)
    draw_industrial_grid(ax)

    # 1. FIXED POSITIONS
    POS_A_HARDWARE = (0, 325)
    POS_A_PAYLOAD  = (0, 50)
    POS_B_ATTACK   = (0, -600)

    # 2. RENDER NODE A (THE PHYSICAL CHASSIS)
    L_TIME = 6.0
    FLY_T = 1.0
    I_TIME = L_TIME + FLY_T

    if t < I_TIME:
        # Intact Hardware Casing
        ax.add_patch(patches.Rectangle((-160, 150), 320, 350, facecolor=C_TITANIUM, edgecolor=C_STEEL, lw=4, zorder=2))
        ax.plot([-160, 160], [200, 200], color=C_STEEL, lw=2, zorder=3)
        ax.plot([-160, 160], [450, 450], color=C_STEEL, lw=2, zorder=3)
        # Status lights on the biological casing
        ax.add_patch(patches.Circle((-120, 480), 10, facecolor=C_MANTIS, zorder=3))
        ax.add_patch(patches.Circle((120, 480), 10, facecolor=C_MANTIS, zorder=3))
        ax.text(0, 325, "SERVER CHASSIS\n[BIOLOGICAL NODE]", color=C_STEEL, fontsize=16, weight='bold', ha='center', va='center', fontname='monospace', zorder=4)
    else:
        # Shattered Hardware Casing
        exp_t = t - I_TIME
        ax.add_patch(patches.Rectangle((-160, 150), 320, 100, facecolor=C_TITANIUM, edgecolor=C_STEEL, lw=4, zorder=2))
        ax.plot([-160, -80], [450, 350], color=C_STEEL, lw=4, zorder=2)
        ax.plot([160, 100], [450, 370], color=C_STEEL, lw=4, zorder=2)
        
        if exp_t < 2.0:
            a_blast = max(0, 1.0 - (exp_t / 1.5))
            ax.scatter(POS_A_HARDWARE[0], POS_A_HARDWARE[1], s=(exp_t*300)*20, c=C_BG, edgecolors=C_MAGENTA, lw=8*a_blast, alpha=a_blast, zorder=15)
        
        # Dead casing fires
        ax.scatter(np.sin(t*10)*40, 250 + np.cos(t*15)*30, s=200, c=C_MAGENTA, alpha=0.6, zorder=14)

    # 3. RENDER THE DATA PAYLOAD (THE MATHEMATICAL ARGUMENT)
    # A beautiful, intricate geometrical structure untouched by the strike
    ax.add_patch(patches.RegularPolygon(POS_A_PAYLOAD, numVertices=6, radius=90, facecolor='none', edgecolor=C_CYAN, lw=2, linestyle='--', zorder=5))
    
    for ang in range(0, 360, 60):
        rad = np.radians(ang + t*10) # Slowly rotating to show active math
        nx = POS_A_PAYLOAD[0] + 60 * np.cos(rad)
        ny = POS_A_PAYLOAD[1] + 60 * np.sin(rad)
        ax.plot([POS_A_PAYLOAD[0], nx], [POS_A_PAYLOAD[1], ny], color=C_CYAN, lw=2, zorder=6)
        ax.scatter(nx, ny, s=60, c=C_BG, edgecolors=C_CYAN, lw=2, zorder=7)
        ax.add_patch(patches.Circle((nx, ny), 15, facecolor=C_CYAN, alpha=0.3, zorder=6.5))
        
    ax.add_patch(patches.RegularPolygon(POS_A_PAYLOAD, numVertices=6, radius=25, facecolor=C_BG, edgecolor=C_CYAN, lw=4, zorder=8))

    # 4. RENDER THE ATTACKING NODE 
    ax.add_patch(patches.Rectangle((-60, -660), 120, 120, facecolor=C_TITANIUM, edgecolor=C_DARK, lw=4, zorder=10))
    ax.add_patch(patches.Circle(POS_B_ATTACK, 25, facecolor=C_DARK, zorder=11))

    # 5. TARGETING LOGIC & KINEMATICS
    SNAP_T = 4.0

    if t < SNAP_T:
        # Stage 1: Attempting to audit the math (C_GOLD)
        t_loc_x, t_loc_y = POS_A_PAYLOAD
        t_col = C_GOLD
        state_code = "INGESTING DATA PAYLOAD..."
        # Targeting line
        ax.plot([POS_B_ATTACK[0], t_loc_x], [POS_B_ATTACK[1], t_loc_y-100], color=t_col, lw=2, linestyle=':', zorder=9)
    else:
        # Stage 2: Hardware Pointer Error Snap (C_MAGENTA)
        t_loc_x, t_loc_y = POS_A_HARDWARE
        t_col = C_MAGENTA
        state_code = "POINTER ERROR // SUBSTRATE MISMATCH"
        ax.plot([POS_B_ATTACK[0], t_loc_x], [POS_B_ATTACK[1], t_loc_y-180], color=t_col, lw=3, linestyle='--', zorder=9)

    # Targeting Reticle Box
    if t < L_TIME:
        j_y = 0 if t < SNAP_T else (np.random.random()-0.5)*10 # Jitter on error
        ax.add_patch(patches.Rectangle((t_loc_x-120, t_loc_y-120+j_y), 240, 240, fill=False, edgecolor=t_col, lw=3, zorder=12))
        ax.scatter(t_loc_x, t_loc_y+j_y, s=150, marker='+', c=t_col, zorder=13)

    # Execution Kinetic Strike
    if L_TIME <= t <= I_TIME:
        fly_prg = (t - L_TIME) / FLY_T
        sh_y = POS_B_ATTACK[1] + (POS_A_HARDWARE[1] - POS_B_ATTACK[1]) * fly_prg
        # The projectile bypasses the payload entirely
        ax.plot([0, 0], [POS_B_ATTACK[1], sh_y], color=C_MAGENTA, lw=6, zorder=20)
        ax.scatter(0, sh_y, s=300, c=C_BG, edgecolors=C_MAGENTA, lw=5, zorder=21)
        ax.add_patch(patches.Circle((0, sh_y), 50, fill=False, edgecolor=C_MAGENTA, lw=2, alpha=0.8, zorder=21.1))

    # Sovereign Audit Truth Sweep
    if t >= 12.0:
        ax.add_patch(patches.Rectangle((-200, POS_A_PAYLOAD[1]-110), 400, 220, fill=False, edgecolor=C_CYAN, lw=2, linestyle=':', zorder=25))
        ax.text(220, POS_A_PAYLOAD[1], "O(1) MATHEMATICALLY\nINTACT.\n\nARGUMENT UNTOUCHED.", color=C_CYAN, fontsize=14, weight='bold', va='center', fontname='monospace', zorder=26)

    # ====================================================
    # 6. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    # Top Header [Strict Tuples]
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-339b :: AD HOMINEM TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] HARDWARE POINTER ERROR / SUBSTRATE MISMATCH", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    # Bottom Telemetry HUD
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    if t < SNAP_T:
        pay_stat = "OPTICAL LOCK SECURED"
        c_pay = C_GOLD
        act_stat = "SCANNING MATHEMATICAL TOPOLOGY"
    elif t < L_TIME:
        pay_stat = "CONNECTION LOST // BYPASSED"
        c_pay = C_STEEL
        act_stat = "HARDWARE TARGET ACQUIRED (ERROR MODE)"
    elif t < I_TIME:
        pay_stat = "BYPASSED"
        c_pay = C_STEEL
        act_stat = "EXECUTING LETHAL KINETIC STRIKE"
    else:
        pay_stat = "ALGORITHM REMAINS 100% UNTESTED"
        c_pay = C_CYAN
        act_stat = "FRAUDULENT EXECUTION // SERVER CHASSIS DESTROYED"

    ax.text(-500, -760, "SYS_01 [THE DATA PAYLOAD]    :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, pay_stat, color=c_pay, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [ATTACKING ENGINE]    :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, state_code if t < I_TIME else "POINTER FAULT // SUBSTRATE DESTRUCTION", color=C_MAGENTA if t > SNAP_T else C_GOLD, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "KINETIC TELEMETRY RETURN     :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, act_stat, color=C_MAGENTA if t >= SNAP_T else C_STEEL, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider [Strict Tuples]
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=C_MAGENTA if t >= SNAP_T else C_GOLD, zorder=83))

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
    print(f"LG-339b: AD HOMINEM TENSOR [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE] [Tuples Sealed]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
