"""
PROJECT: Logic Garden 437 (Exact Physical Construct // Plasma Sheet Dynamics)
FORMAT: YouTube Shorts (1080x1920)
METADATA: MAGNETIC RECONNECTION, SOLAR FLARES, PLASMA SHEET, HYDRODYNAMICS, DAYLIGHT
EXECUTION: 16.0s Sequence. Irreversible Topological Reconnection Discontinuity.
RULES ENFORCED:
- O(1) Macroscopic Magnetic Topology (Sweet-Parker / Petschek Reconnection).
- O(N) Plasma Particle Array (15,000 nodes mapping Lorentz and Thermodynamic drift).
- Exact Topological Snapping and Bounding Geometry (No line crossings permitted until T=6.0).
- Daylight Palette (White Substrate / High-Contrast Solid Geometry).
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
DURATION = 16.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_437_plasma"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG            = '#FFFFFF'
C_TEXT          = '#111115'         # Indestructible Black UI
C_MAGNETIC_LINE = '#1E293B'         # Carbon Slate (Heavy Topology Bounds)
C_MAGNETIC_CORE = '#94A3B8'         # Steel (Inner Spline Vector)
C_PLASMA_COLD   = np.array([1.0, 0.70, 0.0])   # FFBB00 Dense Amber
C_PLASMA_WARM   = np.array([1.0, 0.20, 0.0])   # FF3300 Intense Red
C_PLASMA_HOT    = np.array([0.87, 0.0, 0.54])  # DE008A Deep Magenta
C_STEEL         = '#64748B'         # Ghost Metrics

# ------------------------------------------------------------------
# PARALLEL GENERATOR (LOGIC TENSORS)
# ------------------------------------------------------------------
def generate_stream():
    np.random.seed(437)

    N_NODES = 15000
    p_x = np.random.uniform(0, 1080, N_NODES)
    p_y = np.random.uniform(0, 1920, N_NODES)
    p_vx = np.zeros(N_NODES)
    p_vy = np.zeros(N_NODES)
    p_heat = np.random.uniform(0, 0.2, N_NODES)

    for f in range(TOTAL_FRAMES):
        t = f / float(FPS)
        dt = 1.0 / float(FPS)

        # 1. KINEMATIC TIMELINE CONSTRAINTS
        if t < 6.0:
            v_out_accel = 0.0
            # Tension ramps up to perfectly align with T=6.0 snap
            inflow_crush = 80.0 + (t/6.0)*50.0 
        else:
            v_out_accel = 3800.0 # Extreme Hypersonic Reconnection Jets
            inflow_crush = 130.0

        # 2. O(N) LORENTZ AND MAGNETIC PRESSURE CALCULATION
        dx = p_x - 540.0
        dy = p_y - 960.0

        # The opposing domains aggressively drive plasma inwards
        force_inflow = -np.sign(dx) * inflow_crush
        
        # The Current Sheet Resistance (Ideal MHD physics: lines cannot cross)
        # Pushes back dynamically to form a rigorous, infinitely thin 16-unit vertical blade.
        force_sheet_repel = np.sign(dx) * 160.0 * np.exp(-np.abs(dx)/12.0)
        
        ax = force_inflow + force_sheet_repel

        # The Reconnection Slingshot
        # Only active after topological snap. The reconnected lines violently snap away vertically.
        ay = np.zeros(N_NODES)
        if t >= 6.0:
            # Tension is maximised precisely inside the Central X-Point geometry
            tension_mag = v_out_accel * np.exp(-np.abs(dx)/60.0) * np.exp(-np.abs(dy)/500.0)
            ay = np.sign(dy) * tension_mag
            # Inject extreme thermodynamic heat directly from kinetic acceleration
            p_heat += tension_mag * 0.006 * dt

        p_vx += ax * dt
        p_vy += ay * dt

        # Thermal Brownian Noise mapping fluid pressure
        p_vx += np.random.normal(0, 6.0 + p_heat*12.0, N_NODES) * dt
        p_vy += np.random.normal(0, 6.0 + p_heat*12.0, N_NODES) * dt

        # Physical structural drag 
        p_vx *= 0.91
        p_vy *= 0.96 # Yielded highly to allow unimpeded hypersonic jet streams

        p_x += p_vx * dt
        p_y += p_vy * dt

        # Absolute thermodynamic cooling
        p_heat *= 0.95

        # 3. CONSERVATION OF MASS (Infinite Input Flow)
        out_mask = (p_y < -200) | (p_y > 2120) | (np.abs(p_x - 540) > 600)
        if np.any(out_mask):
            n_out = np.sum(out_mask)
            p_y[out_mask] = np.random.uniform(0, 1920, n_out)
            # Re-enter the simulation from the raw outer boundaries
            p_x[out_mask] = np.where(np.random.rand(n_out) > 0.5, np.random.uniform(-100, 0), np.random.uniform(1080, 1180))
            p_vx[out_mask] = 0
            p_vy[out_mask] = 0
            p_heat[out_mask] = 0.0

        yield (f, t, np.copy(p_x), np.copy(p_y), np.copy(p_heat))

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t, px, py, pheat = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # 1. MATHEMATICAL FLUX CALCULATOR FOR TOPOLOGY LATTICE
    # Guaranteed O(1) determinism without state passing
    if t < 6.0:
        flux_tracker = (100.0 / 6.0) * t
    else:
        flux_tracker = 100.0 + 350.0 * (t - 6.0)

    # 2. O(N) THERMODYNAMIC PLASMA PARTICLES
    c_deb = np.zeros((len(px), 4))
    norm_heat = np.clip(pheat, 0, 2.0)
    
    # Vectorized Bi-linear colour interpolation (Amber -> Red -> Magenta)
    mask1 = norm_heat <= 1.0
    u1 = norm_heat[mask1, None]
    c_deb[mask1, :3] = C_PLASMA_COLD * (1-u1) + C_PLASMA_WARM * u1
    
    mask2 = norm_heat > 1.0
    u2 = (norm_heat[mask2, None] - 1.0)
    c_deb[mask2, :3] = C_PLASMA_WARM * (1-u2) + C_PLASMA_HOT * u2
    
    c_deb[:, 3] = 0.82 # Alpha saturation

    # Particles inherently render BELOW the topological magnetic lines
    ax.scatter(px, py, s=18, c=c_deb, edgecolors='none', zorder=5)

    # 3. O(1) MACRO MAGNETIC FIELD LINES (SWEET-PARKER MODEL)
    unique_psis = np.arange(100, 4000, 180)
    for psi in unique_psis:
        C = psi - flux_tracker
        if C > 0:
            # INFLOW CONTINUITY (Magnetic fields compressing inwards)
            line_y = np.linspace(-100, 2020, 250)
            bend = 0.05 * np.abs(line_y - 960)**1.35
            x_offset = C + bend * (1.0 - np.exp(-C/80.0))
            
            line_x_L = 540 - x_offset
            line_x_R = 540 + x_offset
            
            # Left Array
            ax.plot(line_x_L, line_y, color=C_MAGNETIC_LINE, lw=5, zorder=10)
            ax.plot(line_x_L, line_y, color=C_MAGNETIC_CORE, lw=1.5, zorder=11)
            # Right Array
            ax.plot(line_x_R, line_y, color=C_MAGNETIC_LINE, lw=5, zorder=10)
            ax.plot(line_x_R, line_y, color=C_MAGNETIC_CORE, lw=1.5, zorder=11)
        else:
            # OUTFLOW TOPOLOGY (Post-Reconnection Bi-Directional Slingshot)
            C_out = abs(C) * 6.0 
            line_x = np.linspace(-100, 1180, 250)
            bend = 0.05 * np.abs(line_x - 540)**1.35
            y_offset = C_out + bend * (1.0 - np.exp(-C_out/80.0))
            
            line_y_T = 960 + y_offset
            line_y_B = 960 - y_offset
            
            # Top Loop Array
            ax.plot(line_x, line_y_T, color=C_MAGNETIC_LINE, lw=5, zorder=10)
            ax.plot(line_x, line_y_T, color=C_MAGNETIC_CORE, lw=1.5, zorder=11)
            # Bottom Loop Array
            ax.plot(line_x, line_y_B, color=C_MAGNETIC_LINE, lw=5, zorder=10)
            ax.plot(line_x, line_y_B, color=C_MAGNETIC_CORE, lw=1.5, zorder=11)

    # 4. EXPLICIT VISUAL CAUSALITY (X-POINT ANCHOR)
    rx, ry = 540, 960
    if t < 6.0:
        ax.plot([rx-150, rx-50], [ry, ry], color=C_TEXT, lw=4, zorder=20)
        ax.plot([rx+150, rx+50], [ry, ry], color=C_TEXT, lw=4, zorder=20)
        ax.text(rx-160, ry, "POTENTIAL\nCRUSH", color=C_TEXT, fontsize=12, fontname='monospace', weight='bold', ha='right', va='center', zorder=21)
        ax.text(rx+160, ry, "INFLOW\nCOMPRESSION", color=C_TEXT, fontsize=12, fontname='monospace', weight='bold', ha='left', va='center', zorder=21)
    else:
        # Crosshair highlights the exact topological break parameter
        ax.plot([rx-40, rx+40], [ry, ry], color=C_TEXT, lw=2, zorder=20)
        ax.plot([rx, rx], [ry-40, ry+40], color=C_TEXT, lw=2, zorder=20)
        ax.add_patch(patches.Rectangle((rx-120, ry-20), 240, 40, facecolor=C_BG, edgecolor=C_TEXT, lw=3, zorder=21))
        ax.text(rx, ry, "MAGNETIC X-POINT", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', ha='center', va='center', zorder=22)

    # 5. ABSOLUTE DAYLIGHT TELEMETRY (TOP HUD)
    ax.add_patch(patches.Rectangle((0, 1780), 1080, 140, facecolor=C_BG, zorder=90))
    ax.plot([0, 1080], [1780, 1780], color=C_TEXT, lw=6, zorder=91)

    ax.text(40, 1870, "LG-437 // PLASMA SHEET DYNAMICS", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=92)
    ax.text(40, 1825, "MAGNETIC RECONNECTION // SOLAR FLARE EXHAUST", color=C_STEEL, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=92)

    # 6. ABSOLUTE DAYLIGHT TELEMETRY (BOTTOM HUD)
    ax.add_patch(patches.Rectangle((0, 0), 1080, 160, facecolor=C_BG, zorder=90))
    ax.plot([0, 1080], [160, 160], color=C_TEXT, lw=6, zorder=91)

    if t < 6.0: sys_state = "[PHASE 1 : THE CURRENT SHEET // INDUCED INFLOW CRUSH]"
    elif t < 6.4: sys_state = "[PHASE 2 : TOPOLOGICAL SNAP // MAGNETIC RECONNECTION]"
    elif t < 13.0: sys_state = "[PHASE 3 : LORENTZ ACCELERATION // BI-DIRECTIONAL JETS]"
    else: sys_state = "[PHASE 4 : THERMODYNAMIC EXHAUST RELAXATION]"

    hud_col = C_PLASMA_HOT if "JETS" in sys_state else (C_PLASMA_WARM if "SNAP" in sys_state else C_TEXT)

    ax.text(40, 110, f"KINEMATIC STATE : {sys_state}", color=hud_col, fontsize=16, fontname='monospace', weight='bold', zorder=92)

    v_jet = 0.0 if t < 6.0 else min(3800.0, (t-6.0)*4000.0)
    base_heat = np.mean(pheat)
    
    ax.text(40, 60, f"JET EXHAUST VELOCITY : {v_jet:06.1f} KM/S", color=C_TEXT if t < 6.0 else C_PLASMA_HOT, fontsize=16, fontname='monospace', weight='bold', zorder=92)
    ax.text(600, 60, f"STRUCTURAL HEAT YIELD: {base_heat:05.3f} K", color=C_TEXT if t < 6.0 else C_PLASMA_WARM, fontsize=16, fontname='monospace', weight='bold', zorder=92)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-437: PLASMA SHEET MATRIX (DAYLIGHT) [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        # FIXED: Piping the explicit Generator directly into the map worker list.
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Lorentz Vectors Solved. Magnetic Disconnection Wrapped. Stand by for compilation.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
