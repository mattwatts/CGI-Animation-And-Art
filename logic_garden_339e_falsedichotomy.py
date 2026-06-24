"""
SOVEREIGN CODE: logic_garden_339e_falsedichotomy.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Vectorization
SCENE: Logic Garden 339e (False Dichotomy // Dimensional Truncation)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING, COGNITIVE LOGIC
HOTFIX: Linear 24.0s Sequence. Daylight Protocol. Absolute Camera Lock. Tuples Sealed.
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
DURATION = 24.0  
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_339e_falsedichotomy"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Environment Matrix
C_STEEL     = '#606065'   # Hardware Circuit Breakers / Boolean Rails
C_DARK      = '#202025'   # Logic Cores
C_CYAN      = '#00FFFF'   # Analog Topology 1
C_GOLD      = '#FFB300'   # Analog Topology 2
C_MAGENTA   = '#FF0055'   # Dimensional Truncation / Data Loss
C_MANTIS    = '#00FF00'   # Terminal Green Flow (Analog Restored)

def draw_industrial_grid(ax):
    """Draw the Structural Matrix"""
    for i in range(-5, 6):
        ax.plot([i*100, i*100], [-960, 960], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)
    for j in range(-9, 10):
        ax.plot([-540, 540], [j*100, j*100], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)

X_VALS = np.linspace(-540, 540, 600)  # High resolution sequence

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

    # 1. THE BOOLEAN RAILS (Hardware Constraints)
    # 1-Bit Logic Gate Parameters
    ax.add_patch(patches.Rectangle((-540, 230), 1080, 40, facecolor=C_TITANIUM, edgecolor=C_STEEL, lw=2, zorder=2))
    ax.text(0, 250, "BOOLEAN STATE [1]", color=C_STEEL, fontsize=16, weight='bold', ha='center', va='center', fontname='monospace', zorder=3)
    
    ax.add_patch(patches.Rectangle((-540, -270), 1080, 40, facecolor=C_TITANIUM, edgecolor=C_STEEL, lw=2, zorder=2))
    ax.text(0, -250, "BOOLEAN STATE [0]", color=C_STEEL, fontsize=16, weight='bold', ha='center', va='center', fontname='monospace', zorder=3)
    
    ax.plot([-540, 540], [0, 0], color=C_TITANIUM, lw=2, linestyle='--', zorder=1)

    # 2. WAVEFORM KINEMATICS (Analog vs Binary)
    # The True Analog State (High Complexity)
    Y1 = np.sin(X_VALS * 0.012 - t * 2.5) * 120 + np.cos(X_VALS * 0.005 + t) * 60
    Y2 = np.cos(X_VALS * 0.015 + t * 2.0) * 140 + np.sin(X_VALS * 0.008 - t) * 40
    Y3 = np.sin(X_VALS * 0.020 - t * 3.0) * 80  + np.cos(X_VALS * 0.01 - t*1.5) * 90

    # The Truncated Boolean State (Forced 1-bit compression)
    # Resolves the average geometry into a rigid +250 or -250
    Y_AVG = (Y1 + Y2 + Y3) / 3.0
    Y_SQUARE = np.sign(Y_AVG) * 250

    # 3. COMPRESSION PROGRESSION LOGIC
    T_SQUEEZE_START = 5.0
    T_SQUEEZE_END   = 8.0
    T_RESTORE_START = 16.0
    T_RESTORE_END   = 19.0

    if t < T_SQUEEZE_START:
        comp_prog = 0.0
        state_code = "FULL SPECTRUM TOPOLOGY // N-DIMENSIONAL"
        c_state = C_CYAN
        hud_loss = "0.00% [MATHEMATICAL INTEGRITY RETAINED]"
    elif t < T_SQUEEZE_END:
        comp_prog = (t - T_SQUEEZE_START) / (T_SQUEEZE_END - T_SQUEEZE_START)
        state_code = "BOOLEAN COMPRESSION INSTANTIATED"
        c_state = C_MAGENTA
        hud_loss = f"{(comp_prog * 100):>05.1f}% [ERASING INTERMEDIATE VARIABLES]"
    elif t < T_RESTORE_START:
        comp_prog = 1.0
        state_code = "DIMENSIONAL TRUNCATION // 1-BIT [0,1] ONLY"
        c_state = C_MAGENTA
        hud_loss = "100.0% CATASTROPHIC SPATIAL DATA LOSS"
    elif t < T_RESTORE_END:
        comp_prog = 1.0 - ((t - T_RESTORE_START) / (T_RESTORE_END - T_RESTORE_START))
        state_code = "SERIALIZE RAZOR // OVERRIDING DICHOTOMY"
        c_state = C_GOLD
        hud_loss = f"{(comp_prog * 100):>05.1f}% [RESTRICTIVE GATE DISMANTLED]"
    else:
        comp_prog = 0.0
        state_code = "TATH\u0100T\u0100 // ANALOG TOPOLOGY RESTORED"
        c_state = C_MANTIS
        hud_loss = "0.00% [TERMINAL GREEN FLOW SECURED]"

    # Pre-compute current state lines
    def blend_wave(Y_analog, Y_sq, prog):
        return Y_analog * (1.0 - prog) + Y_sq * prog

    Y1_c = blend_wave(Y1, Y_SQUARE, comp_prog)
    Y2_c = blend_wave(Y2, Y_SQUARE, comp_prog)
    Y3_c = blend_wave(Y3, Y_SQUARE, comp_prog)

    # 4. RENDER WAVEFORMS
    alpha_analog = 1.0 if comp_prog < 1.0 else 0.0
    col_1 = C_MANTIS if t > T_RESTORE_END else C_CYAN
    col_2 = C_MANTIS if t > T_RESTORE_END else C_GOLD
    col_3 = C_MANTIS if t > T_RESTORE_END else C_STEEL

    # Draw interpolated waveforms
    ax.plot(X_VALS, Y1_c, color=col_1, lw=3, zorder=10, alpha=alpha_analog)
    ax.plot(X_VALS, Y2_c, color=col_2, lw=3, zorder=9, alpha=alpha_analog)
    ax.plot(X_VALS, Y3_c, color=col_3, lw=3, zorder=8, alpha=alpha_analog)

    # Draw the strict Boolean constraint block when fully truncated
    if comp_prog > 0:
        ax.plot(X_VALS, Y1_c, color=C_MAGENTA if t < T_RESTORE_START else C_GOLD, lw=4 * comp_prog, zorder=12, alpha=comp_prog)

    # 5. DATA LOSS SPALLATION (Drawing the deleted coordinates)
    if comp_prog > 0.05 and comp_prog < 0.95:
        # Calculate divergence
        loss_gap_1 = np.abs(Y1 - Y1_c)
        loss_gap_2 = np.abs(Y2 - Y2_c)
        loss_mask_1 = loss_gap_1 > 10
        loss_mask_2 = loss_gap_2 > 10

        # Draw the "ghost" of the true wave burning away
        ax.scatter(X_VALS[loss_mask_1], Y1[loss_mask_1], s=10, c=C_MAGENTA, marker='x', alpha=0.6, zorder=6)
        ax.scatter(X_VALS[loss_mask_2], Y2[loss_mask_2], s=10, c=C_MAGENTA, marker='x', alpha=0.6, zorder=6)
        
        # Free-falling deleted geometry
        fall_y = t * 150 % 100
        ax.scatter(X_VALS[::15] + np.sin(t*10)*10, Y1[::15] - fall_y, s=20, c=C_MAGENTA, alpha=0.5, edgecolor='none', zorder=5)

    # Fill aesthetic for pure square wave
    if comp_prog == 1.0:
        ax.fill_between(X_VALS, 0, Y1_c, facecolor=C_MAGENTA, alpha=0.15, zorder=4)

    # ====================================================
    # 6. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    # Top Header [Strict Tuples]
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-339e :: FALSE DICHOTOMY TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] DIMENSIONAL TRUNCATION // 1-BIT BOOLEAN RUPTURE", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    # Bottom Telemetry HUD
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    ax.text(-500, -760, "SYS_01 [COGNITIVE MATRIX]    :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(30, -760, state_code, color=c_state, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [RESOLUTION ALGORITHM]:", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(30, -800, "1-BIT LOCK [0, 1] OVERRIDE" if (comp_prog > 0.0 and t < T_RESTORE_START) else "ANALOG [N-SPACE] UNLOCKED", color=C_MAGENTA if (comp_prog > 0.0 and t < T_RESTORE_START) else (C_MANTIS if t > T_RESTORE_END else C_GOLD), fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "STRUCTURAL DATA LOSS         :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(30, -840, hud_loss, color=C_MAGENTA if comp_prog > 0.0 else C_STEEL, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider [Strict Tuples]
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=c_state, zorder=83))

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
    print(f"LG-339e: FALSE DICHOTOMY TENSOR [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE] [Tuples Sealed]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
