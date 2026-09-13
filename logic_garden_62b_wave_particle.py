"""
PROJECT: Logic Garden 62b (The Deterministic Jitter Matrix // Electron Wave Packet)
FORMAT: YouTube Shorts (1080x1920)
METADATA: QUANTUM MECHANICS, WAVE-PARTICLE DUALITY, GAUSSIAN PACKET, HEISENBERG, KINEMATICS
EXECUTION: 24.0s Sequence. High-Fidelity 2D Cinematic Tracking Tensor.
RULES ENFORCED:
- Daylight Palette (White Substrate / High-Contrast Chrome).
- Phase-Locked Metaphor: The Probability Envelope vs The Real Phase.
- Exact realisational aspect of free-particle quantum dispersion and group velocity.
- Australian spelling conventions enforced natively (Maths, Colour, Optimise).
- Absolute O(N) plotting with cinematic focal locking.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
import multiprocessing as mp
import os
import gc

# ======== SEQUENCE PARAMETERS ========
FPS = 60
DURATION = 24.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_62b_wavepacket"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG            = '#FFFFFF'
C_TEXT          = '#111115'
C_EDGE          = '#111115'
C_GRID          = '#94A3B8'  # Machined Steel Matrix
C_WAVE          = '#00D2FF'  # High-Contrast Cyan (Real Amplitude)
C_PROB          = '#DE008A'  # Deep Magenta (Probability Envelope)
C_PARTICLE      = '#111115'  # Indestructible Black (The Deterministic Jitter)
C_GUI           = '#64748B'

# -------- QUANTUM KINEMATICS --------
V_GROUP = 4.0      # Group velocity (speed of the envelope)
K_0 = 12.0         # Wavenumber (frequency of the phase ripples)
SIGMA_0 = 1.2      # Initial spatial confinement
DISPERSION = 0.22  # Rate of wave-packet spreading

# ------------------------------------------------------------------
# MATRIX OPERATIONS
# ------------------------------------------------------------------
def quantum_wave_state(t, x_array):
    # Free particle dispersion maths: sigma(t) = sigma_0 * sqrt(1 + (dispersion * t)^2)
    t_disp = t * DISPERSION
    sigma_t = SIGMA_0 * np.sqrt(1.0 + t_disp**2)
    
    # Conservation of probability demands peak amplitude scales down by sqrt(sigma_0 / sigma_t)
    amp = np.sqrt(SIGMA_0 / sigma_t)
    
    # Kinematic centering
    x_c = V_GROUP * t
    
    # 1. The Gaussian Probability Density (|Psi|^2)
    # Scaled massively (x 4.0) purely for high-visibility graphic rendering 
    rho = 4.0 * (amp**2) * np.exp(-((x_array - x_c)**2) / (sigma_t**2))
    
    # 2. The Carrier Wave (Real part of Psi)
    # Phase velocity differs from Group velocity; ripples move faster/slower through the envelope.
    omega = (K_0**2) / 2.0  # roughly E = p^2 / 2m
    phase = K_0 * (x_array - x_c) - (omega * t * 0.1) 
    
    psi_real = np.sqrt(rho) * np.cos(phase)
    
    return x_c, sigma_t, psi_real, rho

def deterministic_heisenberg_jitter(t, sigma_t):
    # Generates a bounded high-frequency noise scalar clamped strongly within -1 to 1 
    # to represent precise probability confinement.
    j = np.sin(t * 37.0) * 0.4 + np.sin(t * 89.0) * 0.3 + np.cos(t * 151.0) * 0.3
    # Weight the jitter against the probability bell curve distribution bounds
    return j * sigma_t * 1.2 

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f_idx):
    t_sec = f_idx / float(FPS)
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.]); ax.set_axis_off(); fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540); ax.set_ylim(-960, 960)

    # 1. THE RELATIVE MATHEMATICAL TRACKING MATRIX
    # We dynamically evaluate a 20-unit physics window strictly surrounding the packet
    x_c, sigma_t, _, _ = quantum_wave_state(t_sec, np.array([0]))
    x_min = x_c - 10.0
    x_max = x_c + 10.0
    
    # Generating the high-density local X array
    x_array = np.linspace(x_min, x_max, 2000)
    
    # Re-evaluating exact waveforms over the focused array
    _, _, psi_real, rho = quantum_wave_state(t_sec, x_array)

    # Mapping logic: Map x_array [-10 to +10 relative to x_c] to screen [-500 to +500]
    # Y-axis will scale wave height 1.0 -> 250 pixels
    px_array = 500.0 * ((x_array - x_c) / 10.0)
    py_wave = psi_real * 180.0
    py_prob = rho * 180.0

    # 2. DRAWING THE GRID (Continuous Cinematic Scroll)
    grid_spacing = 2.0
    # Find all absolutely placed grid lines that fall within current camera view
    start_grid = np.floor(x_min / grid_spacing) * grid_spacing
    end_grid = np.ceil(x_max / grid_spacing) * grid_spacing
    
    for g_x in np.arange(start_grid, end_grid + grid_spacing, grid_spacing):
        g_px = 500.0 * ((g_x - x_c) / 10.0)
        ax.plot([g_px, g_px], [-400, 400], color=C_GRID, lw=1.0, alpha=0.4, zorder=1)
        # Spatial absolute coordinate marking
        ax.text(g_px + 5, -390, f"X={g_x:04.1f}", color=C_GRID, fontsize=10, fontname='monospace', alpha=0.8, zorder=1)

    # Baseline
    ax.plot([-540, 540], [0, 0], color=C_EDGE, lw=2.5, zorder=2)

    # 3. DRAWING THE PROBABILITY ENVELOPE
    ax.fill_between(px_array, 0, py_prob, color=C_PROB, alpha=0.15, zorder=3)
    ax.plot(px_array, py_prob, color=C_PROB, lw=3.5, zorder=4)
    # Mirrored envelope for architectural symmetry
    ax.plot(px_array, -py_prob, color=C_PROB, lw=1.5, alpha=0.3, zorder=4)

    # 4. DRAWING THE REAL WAVE PHASE
    ax.plot(px_array, py_wave, color=C_WAVE, lw=4.5, zorder=5)

    # 5. THE DETERMINISTIC PARTICLE (HEISENBERG BOUNDS)
    p_x_offset = deterministic_heisenberg_jitter(t_sec, sigma_t)
    p_x_abs = x_c + p_x_offset
    
    # Calculate exact wave elevation at the particle's X position
    # Instead of searching the array, we do a direct scalar math evaluation for absolute perfection
    _, _, p_psi, _ = quantum_wave_state(t_sec, np.array([p_x_abs]))
    
    p_px = 500.0 * (p_x_offset / 10.0)
    p_py = p_psi[0] * 180.0
    
    # Draw tracking crosshair linking particle to baseline
    ax.plot([p_px, p_px], [0, p_py], color=C_PARTICLE, lw=1.5, linestyle='--', zorder=6)
    
    # Draw the massive particle point
    ax.scatter([p_px], [p_py], color=C_PARTICLE, s=350, zorder=10, edgecolors=C_WAVE, linewidths=2.5)

    # 6. HIGH-DENSITY HUD & TELEMETRY
    ax.add_patch(Rectangle((-540, 780), 1080, 180, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [780, 780], color=C_TEXT, lw=3, zorder=81)
    ax.text(-500, 880, "LG-62b :: ELECTRON WAVE PACKET", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 830, "[SFI-1.00] QUANTUM KINEMATICS & WAVE DISPERSION", color=C_WAVE, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    prog = t_sec / DURATION
    if t_sec < 6.0:
        state_msg = "PHASE 1: HIGHLY LOCALIZED PACKET"
        state_col = C_WAVE
    elif t_sec < 18.0:
        state_msg = "PHASE 2: SCHRÖDINGER DISPERSION MECHANICS"
        state_col = C_PROB
    else:
        state_msg = "PHASE 3: MAXIMUM SPATIAL UNCERTAINTY"
        state_col = C_TEXT

    sys_metric = f"ABS_X: {x_c:05.1f} | SPREAD (σ): {sigma_t:05.2f} | P_OFFSET: {p_x_offset:+05.2f}"

    ax.text(-500, -780, f"PROTOCOL STATE : {state_msg}", color=state_col, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"DIAGNOSTIC     : {sys_metric}", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"AXIOMATIC TRUTH: THE PARTICLE JITTERS DETERMINISTICALLY WITHIN THE ENVELOPE.", color=C_TEXT, fontsize=11, fontname='monospace', zorder=82)

    ax.add_patch(Rectangle((-500, -920), 1000, 8, facecolor=C_GUI, zorder=82))
    ax.add_patch(Rectangle((-500, -920), 1000 * prog, 8, facecolor=state_col, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f_idx:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f_idx

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-62b: QUANTUM WAVE TENSOR ENGAGED [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")
    print("Compilation Complete. Wavefunction mathematically collapsed.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
