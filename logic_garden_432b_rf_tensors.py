"""
PROJECT: Logic Garden 432b (Exact Physical Construct // RF Spectrum Tensors)
FORMAT: YouTube Shorts (1080x1920)
METADATA: AM, FM, SSB, VHF, UHF, DIGITAL TV, DAYLIGHT
EXECUTION: 12.0s Seamless Endless Loop. True High-Density Vector Construct.
RULES ENFORCED:
- O(1) Trigonometric Integration for 6 distinct Modulation Standard Kinematics.
- Central Kinematic Read-Head yielding live sub-millisecond telemetry.
- Orthogonal Sub-Carrier Matrix (OFDM) generation for Digital Television.
- Daylight Palette (White Substrate / High-Contrast Mathematical Geometry).
- Purged Jargon. Australian spelling conventions (maths, colour, synchronisation).
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
OUT_DIR = "frames_432b_rf_spectrum"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG          = '#FFFFFF'
C_TEXT        = '#111115'          # Indestructible Black Headers
C_STEEL       = '#94A3B8'          # Carrier Wave / Framework Grid
C_AM          = '#005599'          # Deep Marine
C_SSB         = '#CC6600'          # Dense Amber
C_FM          = '#DE008A'          # Deep Magenta
C_VHF_TV      = '#00C853'          # Jade (Classic Phosphor)
C_UHF_CB      = '#1E293B'          # Carbon Slate
C_UHF_DIGITAL = '#FF3300'          # Intense Red (Broadband Payload)
C_READ        = '#FF0033'          # Vivid Kinematic Read-Head
C_GRID        = '#E2E8F0'          # Soft Base Substrate

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    # Perfect mathematical cyclic scalar (0.0 to 1.0)
    tau = f / float(TOTAL_FRAMES)

    # Structural Substrate Generation
    # 8000 precise computational nodes for flawless anti-aliasing without Bezier cheats
    X = np.linspace(40, 1040, 8000)
    xn = (X - 40) / 1000.0  # Normalised 0.0 to 1.0

    # --------------------------------------------------------------
    # THE MATHS: O(1) MODULATION EQUATIONS
    # --------------------------------------------------------------
    # Global Information Baseplate (Audio/Data parameter to be transmitted)
    # Guaranteed seamless modulo wrapping via absolute integers (3 and 6)
    v_info = 0.7 * np.sin(2 * np.pi * (3 * xn - 3 * tau)) + 0.3 * np.cos(2 * np.pi * (6 * xn - 6 * tau))

    # 1. AM RADIO (Medium Wave - Amplitude Modulation)
    fc_am = 60.0
    env_am = (1.0 + 0.8 * v_info)
    v_am = env_am * np.sin(2 * np.pi * (fc_am * xn - fc_am * tau))

    # 2. SSB RADIO (Shortwave - Suppressed Carrier AM Proxy)
    fc_ssb = 80.0
    v_ssb = v_info * np.sin(2 * np.pi * (fc_ssb * xn - fc_ssb * tau))
    env_ssb = np.abs(v_info)

    # 3. FM RADIO (VHF Band II - Wideband)
    fc_fm = 100.0
    beta_wide = 8.0 # Aggressive frequency expansion
    v_fm = np.sin(2 * np.pi * (fc_fm * xn - fc_fm * tau) + beta_wide * v_info)

    # 4. VHF ANALOG TV (Band III - Negative AM with Synchronisation Base)
    fc_tv = 250.0
    p = (6 * xn - 6 * tau) % 1.0 # 6 rigid scanlines
    env_tv = np.ones_like(p)
    # Synthesize Synchronisation Pulses (Max Carrier Power)
    env_tv[p < 0.08] = 1.0
    # Blanking Porch / Black Level
    env_tv[(p >= 0.08) & (p < 0.15)] = 0.75
    # Active Video Phase (Negative AM: White = Low power, Black = High power)
    active_mask = p >= 0.15
    norm_info = (v_info + 1.0) / 2.0 # Scale input to 0-1
    env_tv[active_mask] = 0.75 - 0.65 * norm_info[active_mask]
    v_tv = env_tv * np.sin(2 * np.pi * (fc_tv * xn - fc_tv * tau))

    # 5. UHF CB RADIO (477 MHz - Narrowband FM)
    fc_cb = 300.0
    beta_narrow = 1.5 # Extreme subtlety inside a high density matrix
    v_cb = np.sin(2 * np.pi * (fc_cb * xn - fc_cb * tau) + beta_narrow * v_info)

    # 6. UHF DIGITAL TV (DVB-T / OFDM)
    # Requires strict RNG seeding per-frame to ensure the multi-path noise shape dynamically 
    # slides across the domain perfectly rather than behaving like staticky snow.
    np.random.seed(432)
    v_ofdm = np.zeros_like(xn)
    for k in range(30):
        phase = np.random.uniform(0, 2*np.pi)
        f_sub = 360.0 + k * 4.0 # Tight clusters of integers for flawless loop wrapping
        v_ofdm += np.sin(2 * np.pi * (f_sub * xn - f_sub * tau) + phase)
    # Normalise thermodynamic yield
    v_ofdm /= (np.max(np.abs(v_ofdm)) + 0.1)

    # TELEMETRY EXTRACTION TENSOR (Center Read-Head)
    idx_center = np.argmin(np.abs(X - 540.0))
    val_am   = v_am[idx_center]
    val_ssb  = v_ssb[idx_center]
    val_fm   = v_fm[idx_center]
    val_tv   = v_tv[idx_center]
    val_cb   = v_cb[idx_center]
    val_ofdm = v_ofdm[idx_center]

    # --- MATPLOTLIB FIGURE INSTANTIATION ---
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # Global Background Cartesian Grid
    for i in range(100, 1920, 100):
        ax.plot([0, 1080], [i, i], color=C_GRID, lw=1.0, zorder=0)

    AMP_GLOBAL = 110 # Uniform vertical yield standard

    # --------------------------------------------------------------
    # 1. AM RADIO
    # --------------------------------------------------------------
    Y1 = 1680
    ax.plot([40, 1040], [Y1, Y1], color=C_STEEL, lw=2, zorder=1)
    ax.plot(X, Y1 + env_am * AMP_GLOBAL, color=C_AM, lw=2, linestyle='dashed', zorder=4, alpha=0.5)
    ax.plot(X, Y1 - env_am * AMP_GLOBAL, color=C_AM, lw=2, linestyle='dashed', zorder=4, alpha=0.5)
    ax.plot(X, Y1 + v_am * AMP_GLOBAL, color=C_AM, lw=2.5, zorder=5)

    ax.text(40, Y1 + 130, "1. AM RADIO // BASELINE AMPLITUDE MODULATION", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold')
    ax.text(40, Y1 + 110, "Base wave linearly overrides the raw vertical envelope payload.", color=C_AM, fontsize=12, fontname='monospace', weight='bold')

    # --------------------------------------------------------------
    # 2. SSB RADIO (Suppressed Carrier)
    # --------------------------------------------------------------
    Y2 = 1380
    ax.plot([40, 1040], [Y2, Y2], color=C_STEEL, lw=2, zorder=1)
    ax.plot(X, Y2 + env_ssb * AMP_GLOBAL, color=C_SSB, lw=2, linestyle='dashed', zorder=4, alpha=0.5)
    ax.plot(X, Y2 - env_ssb * AMP_GLOBAL, color=C_SSB, lw=2, linestyle='dashed', zorder=4, alpha=0.5)
    ax.plot(X, Y2 + v_ssb * AMP_GLOBAL, color=C_SSB, lw=2.5, zorder=5)

    ax.text(40, Y2 + 130, "2. SSB RADIO // SUPPRESSED CARRIER (HF)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold')
    ax.text(40, Y2 + 110, "Thermodynamic efficiency. Carrier collapses to absolute 0 during silence.", color=C_SSB, fontsize=12, fontname='monospace', weight='bold')

    # --------------------------------------------------------------
    # 3. FM RADIO (Wideband VHF)
    # --------------------------------------------------------------
    Y3 = 1080
    ax.plot([40, 1040], [Y3, Y3], color=C_STEEL, lw=2, zorder=1)
    skip = 20
    ax.vlines(X[::skip], Y3, Y3 + v_fm[::skip] * AMP_GLOBAL, colors=C_FM, lw=1.0, alpha=0.3, zorder=4)
    ax.plot(X, Y3 + v_fm * AMP_GLOBAL, color=C_FM, lw=2.5, zorder=5)

    ax.text(40, Y3 + 130, "3. FM RADIO // WIDEBAND FREQUENCY SHIFT", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold')
    ax.text(40, Y3 + 110, "Yield bounds preserved. Data violently alters spatial kinematic density.", color=C_FM, fontsize=12, fontname='monospace', weight='bold')

    # --------------------------------------------------------------
    # 4. VHF ANALOG TV (Negative AM)
    # --------------------------------------------------------------
    Y4 = 780
    ax.plot([40, 1040], [Y4, Y4], color=C_STEEL, lw=2, zorder=1)
    ax.plot(X, Y4 + env_tv * AMP_GLOBAL, color=C_VHF_TV, lw=2, linestyle='dashed', zorder=4, alpha=0.5)
    ax.plot(X, Y4 - env_tv * AMP_GLOBAL, color=C_VHF_TV, lw=2, linestyle='dashed', zorder=4, alpha=0.5)
    ax.plot(X, Y4 + v_tv * AMP_GLOBAL, color=C_VHF_TV, lw=1.5, zorder=5) # Thinner line for extremely high freq

    ax.text(40, Y4 + 130, "4. VHF TV // ANALOG VIDEO SCANLINES", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold')
    ax.text(40, Y4 + 110, "Negative AM logic. Outer spike bounds = True synchronisation pulses.", color=C_VHF_TV, fontsize=12, fontname='monospace', weight='bold')

    # --------------------------------------------------------------
    # 5. UHF CB RADIO (Narrowband FM)
    # --------------------------------------------------------------
    Y5 = 480
    ax.plot([40, 1040], [Y5, Y5], color=C_STEEL, lw=2, zorder=1)
    ax.plot(X, Y5 + v_cb * AMP_GLOBAL, color=C_UHF_CB, lw=1.5, zorder=5)

    ax.text(40, Y5 + 130, "5. UHF CB RADIO // NARROWBAND FM (477 MHz)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold')
    ax.text(40, Y5 + 110, "Massive carrier-frequency multiplier limits baseband shift deviation.", color=C_UHF_CB, fontsize=12, fontname='monospace', weight='bold')

    # --------------------------------------------------------------
    # 6. UHF DIGITAL TV (OFDM / DVB-T)
    # --------------------------------------------------------------
    Y6 = 180
    ax.plot([40, 1040], [Y6, Y6], color=C_STEEL, lw=2, zorder=1)
    ax.plot(X, Y6 + v_ofdm * AMP_GLOBAL, color=C_UHF_DIGITAL, lw=1.0, alpha=0.8, zorder=5)
    ax.fill_between(X, Y6, Y6 + v_ofdm * AMP_GLOBAL, color=C_UHF_DIGITAL, alpha=0.2, zorder=4)

    ax.text(40, Y6 + 130, "6. DIGITAL TELEVISION // OFDM MULTIPLEXING", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold')
    ax.text(40, Y6 + 110, "A dense block of 30 locked orthogonal subcarriers behaving as pure noise.", color=C_UHF_DIGITAL, fontsize=12, fontname='monospace', weight='bold')


    # --------------------------------------------------------------
    # KINEMATIC READ-HEAD TELEMETRY
    # --------------------------------------------------------------
    ax.plot([540, 540], [20, 1850], color=C_READ, lw=2.5, alpha=0.9, zorder=10)
    ax.add_patch(patches.Rectangle((500, 1850), 80, 30, facecolor=C_READ, zorder=11))
    ax.text(540, 1865, "READ", color=C_BG, fontsize=12, fontname='monospace', weight='bold', ha='center', va='center', zorder=12)

    def draw_telemetry(y_center, val, col, prefix):
        ry = y_center + val * AMP_GLOBAL
        # Nodal Strike Base
        ax.add_patch(patches.Circle((540, ry), 8, facecolor=C_BG, edgecolor=col, lw=3, zorder=20))
        # Leader connector
        ax.plot([540, 570], [ry, ry], color=col, lw=2, zorder=19)
        # Background box to guarantee optical supremacy over raw waveforms
        ax.text(580, ry, f"{prefix}[{val:+.3f}]", color=col, fontsize=14, fontname='monospace', weight='bold', va='center', zorder=21, bbox=dict(facecolor=C_BG, alpha=0.8, edgecolor='none', pad=1))

    draw_telemetry(Y1, val_am,   C_AM, "AM:")
    draw_telemetry(Y2, val_ssb,  C_SSB, "SSB:")
    draw_telemetry(Y3, val_fm,   C_FM, "FM :")
    draw_telemetry(Y4, val_tv,   C_VHF_TV, "VHF:")
    draw_telemetry(Y5, val_cb,   C_UHF_CB, "NCB:")
    draw_telemetry(Y6, val_ofdm, C_UHF_DIGITAL, "DIG:")

    # Perimeter UI Block
    ax.add_patch(patches.Rectangle((40, 20), 1000, 40, facecolor=C_TEXT, zorder=80))
    ax.text(60, 40, f"LG-432b // RF COMMUNICATIONS SPECTRUM", color=C_BG, fontsize=14, fontname='monospace', weight='bold', va='center', zorder=81)
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
    print(f"LG-432b: RF SPECTRUM MACRO MATRIX (DAYLIGHT) [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        frames = range(TOTAL_FRAMES)
        for finished_frame in pool.imap_unordered(render_frame, frames, chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Trans-Computational Modulation Block Secured. Stand by for compilation.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
