"""
SOVEREIGN CODE: logic_garden_339a_strawman.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Vectorization
SCENE: Logic Garden 339a (The Straw Man // Proxy Vector Hallucination)
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
DURATION = 20.0  # 20.0 Second Execution
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_339a_strawman"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Empty Spatial Grid
C_STEEL     = '#606065'   # The Actual Argument (True Geometry)
C_DARK      = '#202025'   # The Attacking Node
C_CYAN      = '#00FFFF'   # The Sovereign Audit Scanner
C_MAGENTA   = '#FF0055'   # The Low-Res Proxy Point-Cloud (Straw Man)
C_GOLD      = '#FFB300'   # The Kinetic Strike Output
C_MANTIS    = '#00FF00'   # Fraudulent Success Telemetry

def draw_industrial_grid(ax):
    """Draw the Structural Matrix"""
    for i in range(-5, 6):
        ax.plot([i*100, i*100], [-960, 960], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)
    for j in range(-9, 10):
        ax.plot([-540, 540], [j*100, j*100], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)

# ------------------------------------------------------------------
# PRECOMPUTED GEOMETRIES
# ------------------------------------------------------------------
# 1. The Low-Res Proxy (The Straw Man) / C_MAGENTA point cloud
np.random.seed(339)
N_PROXY = 150
P_PROXY_X = np.random.normal(250, 45, N_PROXY)
P_PROXY_Y = np.random.normal(-50, 45, N_PROXY)

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

    # 1. RENDER THE TRUE ARGUMENT (C_STEEL MONOLITH)
    # A massively fortified, structured, unbreakable geometry
    N_TRUE = (0, 300)
    ax.add_patch(patches.Rectangle((-180, 120), 360, 360, facecolor=C_TITANIUM, edgecolor=C_STEEL, lw=4, zorder=2))
    ax.add_patch(patches.RegularPolygon(N_TRUE, numVertices=8, radius=120, facecolor=C_STEEL, edgecolor=C_BG, lw=3, zorder=3))
    ax.add_patch(patches.Circle(N_TRUE, 40, facecolor=C_DARK, zorder=4))
    
    # Bounding Box indicator
    ax.plot([-220, -220, 220, 220, -220], [80, 520, 520, 80, 80], color=C_STEEL, lw=2, linestyle='--', zorder=1)

    # 2. RENDER THE ATTACKING NODE
    N_ATTACK = (0, -600)
    ax.add_patch(patches.RegularPolygon(N_ATTACK, numVertices=3, radius=80, facecolor=C_DARK, edgecolor=C_CYAN, lw=2, orientation=np.radians(180), zorder=5))
    ax.scatter(N_ATTACK[0], N_ATTACK[1], s=200, c=C_BG, zorder=6)

    # 3. STATE LOGIC ENGINE (THE FRAUDULENT TENSOR)
    L_TIME = 9.0
    FLY_T = 1.5
    I_TIME = L_TIME + FLY_T

    if t < 3.0:
        # State 01: Initial Scan (Ignoring the truth)
        state_code = "COGNITIVE NODE ONLINE // SCANNING MATRIX"
        ax.plot([N_ATTACK[0], N_TRUE[0]], [N_ATTACK[1], N_TRUE[1]-220], color=C_STEEL, lw=1, alpha=0.5, linestyle=':', zorder=4)

    elif t < L_TIME:
        # State 02: Spawning the Proxy (The Geometry Rupture)
        state_code = "PROXY GEOMETRY GENERATED [FALSE MAPPING]"
        spawn_prog = min(1.0, (t - 3.0) / 3.0)
        
        # Point cloud jitters slightly to show it lacks structural integrity
        j_x = P_PROXY_X + np.sin(t*10 + P_PROXY_Y)*5
        j_y = P_PROXY_Y + np.cos(t*12 + P_PROXY_X)*5
        
        ax.scatter(j_x, j_y, s=30*spawn_prog, c=mcolors.to_rgba(C_MAGENTA, spawn_prog), edgecolors='none', zorder=5)
        # Bounding box of the lie
        ax.add_patch(patches.Rectangle((180, -120), 140, 140, fill=False, edgecolor=C_MAGENTA, lw=2, linestyle=':', alpha=spawn_prog, zorder=4))
        
        # Fire-Control shifts to the easy target
        ax.plot([N_ATTACK[0], 250], [N_ATTACK[1], -50], color=C_MAGENTA, lw=2, linestyle='--', alpha=spawn_prog, zorder=4)

    elif t < I_TIME + 2.0:
        # State 03 & 04: The Strike & Sub-Routine Destruction
        state_code = "KINETIC STRIKE EXECUTED AGAINST PROXY"
        prg = (t - L_TIME) / FLY_T
        
        if prg <= 1.0:
            # Shell in transit
            sh_x = N_ATTACK[0] + (250 - N_ATTACK[0]) * prg
            sh_y = N_ATTACK[1] + (-50 - N_ATTACK[1]) * prg
            ax.plot([N_ATTACK[0], sh_x], [N_ATTACK[1], sh_y], color=C_GOLD, lw=5, zorder=10)
            ax.scatter(sh_x, sh_y, s=200, c=C_BG, edgecolors=C_GOLD, lw=4, zorder=11)
            
            # Static proxy waiting for impact
            j_x = P_PROXY_X + np.sin(t*10 + P_PROXY_Y)*5
            j_y = P_PROXY_Y + np.cos(t*12 + P_PROXY_X)*5
            ax.scatter(j_x, j_y, s=30, c=C_MAGENTA, edgecolors='none', zorder=5)
            ax.add_patch(patches.Rectangle((180, -120), 140, 140, fill=False, edgecolor=C_MAGENTA, lw=2, linestyle=':', zorder=4))
        
        else:
            # Impact (Spallation of the Straw Man)
            state_code = "TARGET COMPROMISED // SUCCESS LOGGED"
            exp_t = t - I_TIME
            if exp_t < 2.0:
                blast_r = 300 * (exp_t / 1.0)
                blast_a = max(0, 1.0 - (exp_t / 1.5))
                ax.scatter(250, -50, s=blast_r*15, c=C_BG, edgecolors=C_MAGENTA, lw=8*blast_a, alpha=blast_a, zorder=12)
                ax.scatter(250, -50, s=blast_r*5, c=C_GOLD, alpha=blast_a, edgecolors='none', zorder=13)
                
                # Proxy points flying away in frictionless void
                v_x = P_PROXY_X + (P_PROXY_X - 250) * exp_t * 5
                v_y = P_PROXY_Y + (P_PROXY_Y - (-50)) * exp_t * 5
                ax.scatter(v_x, v_y, s=30, c=C_MAGENTA, alpha=blast_a, edgecolors='none', zorder=5)

    else:
        # State 05: The Reality Audit
        state_code = "SOVEREIGN AUDIT // HALLUCINATION EXPOSED"
        
        # The true structure is audited
        scan_prg = min(1.0, (t - 15.0) / 4.0) # Downward sweep
        if scan_prg > 0:
            scan_y = 550 - (scan_prg * 500)
            ax.plot([-300, 300], [scan_y, scan_y], color=C_CYAN, lw=3, zorder=20)
            ax.fill_between([-300, 300], scan_y, scan_y+50, color=C_CYAN, alpha=0.1, zorder=19)
            
            # Post-scan reality check text physically stamped on the True Argument
            if scan_y < 300:
                ax.text(0, 150, "UNCOMPROMISED\n100% PARITY", color=C_MANTIS, fontsize=16, weight='bold', ha='center', fontname='monospace', zorder=25)

    # ====================================================
    # 4. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    # Top Header [Strict Tuples]
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-339a :: THE STRAW MAN TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] PROXY VECTOR HALLUCINATION / FALSE TELEMETRY", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    # Bottom Telemetry HUD
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    if t < 3.0:
        c_status = C_TEXT; c_strike = C_STEEL; data_return = "STANDBY"
    elif t < L_TIME:
        c_status = C_MAGENTA; c_strike = C_STEEL; data_return = "PROXY DEPLOYED :: REDUCED FRICTION LOGIC"
    elif t < I_TIME:
        c_status = C_MAGENTA; c_strike = C_GOLD; data_return = "KINETIC INTERCEPT IN TRANSIT"
    elif t < 15.0:
        # THE LIE
        c_status = C_MANTIS; c_strike = C_MANTIS; data_return = "SUCCESS :: O(1) STRATEGY VERIFIED [FRAUDULENT]"
    else:
        # THE AUDIT
        c_status = C_CYAN; c_strike = C_MAGENTA; data_return = "ERROR: ACTUAL TARGET MATRIX INTACT // 0.00kN TRANSFERRED"

    ax.text(-500, -760, "SYS_01 [ACTUAL ARGUMENT STR] :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, "C_STEEL MONOLITH [IGNORED]", color=C_STEEL, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [COGNITIVE OPERATION]:", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, state_code, color=c_status, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "KINETIC TELEMETRY RETURN     :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, data_return, color=c_strike, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider [Strict Tuples]
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=c_status, zorder=83))

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
    print(f"LG-339a: THE STRAW MAN TENSOR [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE] [Tuples Sealed]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
