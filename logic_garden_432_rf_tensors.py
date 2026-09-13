"""
PROJECT: Logic Garden 432 (Exact Physical Construct // RF Modulation Matrices)
FORMAT: YouTube Shorts (1080x1920)
METADATA: AM, FM, AMPLITUDE, FREQUENCY, MODULATION, DAYLIGHT
EXECUTION: 12.0s Seamless Endless Loop. True High-Density Vector Construct.
RULES ENFORCED: 
- O(1) Trigonometric Integration for Phase-Level FM precision.
- Central Kinematic Read-Head for live V(t) telemetry readout.
- Daylight Palette (White Substrate / High-Contrast Mathematical Geometry).
- Purged Jargon. Australian spelling conventions (maths, colour).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import multiprocessing as mp
import os
import gc
import math

# ======== SEQUENCE PARAMETERS ========
DURATION = 12.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_432_rf_tensors"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'          # Indestructible Black Headers
C_STEEL     = '#94A3B8'          # Carrier Wave / Framework
C_INFO      = '#00C853'          # Jade (The Information Baseplate)
C_AM        = '#005599'          # Deep Marine (Amplitude Mod Yield)
C_FM        = '#DE008A'          # Deep Magenta (Frequency Mod Yield)
C_READ      = '#FF3300'          # Intense Red (Kinematic Read-Head)
C_GRID      = '#E2E8F0'          # Soft Base Substrate

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    # Perfect mathematical cyclic scalar (0.0 to 1.0)
    tau = f / float(TOTAL_FRAMES)
    
    # Structural Substrate Generation
    # 5400 precise computational nodes for flawless anti-aliasing without Bezier cheats
    X = np.linspace(40, 1040, 5400)
    X_norm = (X - 40) / 1000.0  # Normalized 0.0 to 1.0
    
    # --------------------------------------------------------------
    # THE MATHS: O(1) MODULATION EQUATIONS
    # --------------------------------------------------------------
    
    # 1. Information Tensor (Baseplate)
    f_s_m = 3.0    # 3 Spatial cycles across screen
    f_t_m = 6.0    # 6 Temporal cycles per 12 seconds (0.5 Hz) - Guarantees seamless loop
    phase_m = 2 * np.pi * (f_s_m * X_norm - f_t_m * tau)
    V_m = np.sin(phase_m)
    
    # 2. Carrier Tensor (High-Frequency Substrate)
    f_s_c = 60.0   # 60 Spatial cycles
    f_t_c = 120.0  # 120 Temporal cycles - Guarantees seamless loop
    phase_c = 2 * np.pi * (f_s_c * X_norm - f_t_c * tau)
    V_c = np.sin(phase_c)
    
    # 3. AM Tensor (Amplitude Index override)
    m_idx = 0.85
    V_am = (1.0 + m_idx * V_m) * V_c
    
    # 4. FM Tensor (Phase Integral Override -> Instantaneous Frequency Shift)
    # frequency f(t) = f_c + beta * f_m * cos(wt) -> integrated phase = f_c*t + beta * sin(wt)
    beta = 6.0
    V_fm = np.sin(phase_c + beta * V_m)

    # Extraction indexing for the Center Read-Head (X = 540 is literally half 1080)
    idx_center = np.argmin(np.abs(X - 540.0))
    val_m = V_m[idx_center]
    val_c = V_c[idx_center]
    val_am = V_am[idx_center]
    val_fm = V_fm[idx_center]

    # --- MATPLOTLIB FIGURE INSTANTIATION ---
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # Global Background Grid
    for i in range(100, 1920, 100):
        ax.plot([0, 1080], [i, i], color=C_GRID, lw=1, zorder=0)

    # --------------------------------------------------------------
    # TENSOR 1: INFORMATION BASEPLATE
    # --------------------------------------------------------------
    Y_C1 = 1600
    AMP1 = 110
    ax.plot([40, 1040], [Y_C1, Y_C1], color=C_STEEL, lw=2, zorder=1)
    ax.plot(X, Y_C1 + V_m * AMP1, color=C_INFO, lw=4, solid_capstyle='round', zorder=5)
    
    ax.text(40, Y_C1 + 140, "1. THE BASEPLATE // O(1) INFORMATION TENSOR", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold')
    ax.text(40, Y_C1 + 115, "SIGNAL: V_m = A_m * sin(2π * f_m * t)", color=C_INFO, fontsize=12, fontname='monospace', weight='bold')

    # --------------------------------------------------------------
    # TENSOR 2: CARRIER WAVE
    # --------------------------------------------------------------
    Y_C2 = 1200
    AMP2 = 110
    ax.plot([40, 1040], [Y_C2, Y_C2], color=C_STEEL, lw=2, zorder=1)
    ax.plot(X, Y_C2 + V_c * AMP2, color=C_STEEL, lw=2.5, zorder=5)
    
    ax.text(40, Y_C2 + 140, "2. THE TRANSPORT // KINETIC CARRIER WAVE", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold')
    ax.text(40, Y_C2 + 115, "CARRIER: V_c = A_c * sin(2π * f_c * t)", color=C_STEEL, fontsize=12, fontname='monospace', weight='bold')

    # --------------------------------------------------------------
    # TENSOR 3: AMPLITUDE MODULATION (AM)
    # --------------------------------------------------------------
    Y_C3 = 750
    AMP3 = 140
    ax.plot([40, 1040], [Y_C3, Y_C3], color=C_STEEL, lw=2, zorder=1)
    
    # The Defining Envelopes (Proving the maths visually)
    env_top = Y_C3 + (1.0 + m_idx * V_m) * AMP3
    env_bot = Y_C3 - (1.0 + m_idx * V_m) * AMP3
    ax.plot(X, env_top, color=C_AM, lw=2.5, linestyle='dashed', zorder=4, alpha=0.7)
    ax.plot(X, env_bot, color=C_AM, lw=2.5, linestyle='dashed', zorder=4, alpha=0.7)
    
    # Internal AM Waveform
    ax.plot(X, Y_C3 + V_am * AMP3, color=C_AM, lw=3, zorder=5)
    
    ax.text(40, Y_C3 + 190, "3. AMPLITUDE MODULATION (AM) YIELD", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold')
    ax.text(40, Y_C3 + 165, "KINEMATICS: Baseplate wave violently overwrites carrier height gain.", color=C_AM, fontsize=12, fontname='monospace', weight='bold')

    # --------------------------------------------------------------
    # TENSOR 4: FREQUENCY MODULATION (FM)
    # --------------------------------------------------------------
    Y_C4 = 250
    AMP4 = 140
    # Background Information Vector applied at low opacity to prove the correlation
    ax.plot(X, Y_C4 + V_m * AMP4, color=C_INFO, lw=4, alpha=0.15, solid_capstyle='round', zorder=3)
    ax.plot([40, 1040], [Y_C4, Y_C4], color=C_STEEL, lw=2, zorder=1)
    
    # Draw vertical machined 'struts' for industrial detail density
    skip = 15
    ax.vlines(X[::skip], Y_C4, Y_C4 + V_fm[::skip] * AMP4, colors=C_FM, lw=1.0, alpha=0.4, zorder=4)
    # Prime FM Continuous Wave
    ax.plot(X, Y_C4 + V_fm * AMP4, color=C_FM, lw=3, zorder=5)
    
    ax.text(40, Y_C4 + 190, "4. FREQUENCY MODULATION (FM) YIELD", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold')
    ax.text(40, Y_C4 + 165, "KINEMATICS: Spatial density spallation perfectly preserving rigid amplitude.", color=C_FM, fontsize=12, fontname='monospace', weight='bold')

    # --------------------------------------------------------------
    # READ-HEAD KINEMATIC TELEMETRY (CENTER ANCHOR)
    # --------------------------------------------------------------
    # The Absolute Playhead Line
    ax.plot([540, 540], [30, 1780], color=C_READ, lw=2, alpha=0.8, zorder=10)
    ax.add_patch(patches.Rectangle((500, 1780), 80, 30, facecolor=C_READ, zorder=11))
    ax.text(540, 1795, "READ", color=C_BG, fontsize=12, fontname='monospace', weight='bold', ha='center', va='center', zorder=12)

    def draw_telemetry(y_center, amp, val, col, prefix):
        ry = y_center + val * amp
        # Nodal Strike Point
        ax.add_patch(patches.Circle((540, ry), 8, facecolor=C_BG, edgecolor=col, lw=3, zorder=20))
        # Leader line to telemetry box
        ax.plot([540, 580], [ry, ry], color=col, lw=2, zorder=19)
        # Dynamic Text Feed
        ax.text(590, ry, f"{prefix} [{val:+.3f}]", color=col, fontsize=14, fontname='monospace', weight='bold', va='center', zorder=21)

    draw_telemetry(Y_C1, AMP1, val_m, C_INFO, "SIG")
    draw_telemetry(Y_C2, AMP2, val_c, C_STEEL, "CAR")
    draw_telemetry(Y_C3, AMP3, val_am, C_AM, "AM ")
    draw_telemetry(Y_C4, AMP4, val_fm, C_FM, "FM ")

    # Perimeter UI Block
    ax.add_patch(patches.Rectangle((40, 20), 1000, 40, facecolor=C_TEXT, zorder=80))
    ax.text(60, 40, f"LG-432 // RF TENSOR GEOMETRY MATRIX", color=C_BG, fontsize=14, fontname='monospace', weight='bold', va='center', zorder=81)
    ax.text(1020, 40, f"TIME DOMAIN: {tau*DURATION:05.2f}s", color=C_BG, fontsize=14, fontname='monospace', weight='bold', ha='right', va='center', zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-432: RF MODULATION MATRICES (DAYLIGHT) [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        frames = range(TOTAL_FRAMES)
        for finished_frame in pool.imap_unordered(render_frame, frames, chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Trans-Computational Modulation Locked. Stand by for compilation.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
