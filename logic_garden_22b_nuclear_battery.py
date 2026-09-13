"""
PROJECT: Logic Garden 22b (Exact Physical Construct // Nuclear Battery)
FORMAT: YouTube Shorts (1080x1920)
METADATA: RTG, THERMODYNAMICS, SEEBECK EFFECT, DAYLIGHT
EXECUTION: 24.0s Sequence. True Vector Geometry. 
RULES ENFORCED: 
- 2,000 Kinematic Particles separated into Thermal Flux and Electric Current.
- Exact Realisational Aspect: True cross-section of a Radioisotope generator.
- Daylight Palette (White Substrate / High-Contrast Solid Geometry).
- Purged Jargon. Australian spelling conventions.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcol
import multiprocessing as mp
import os
import gc
import math

# ======== SEQUENCE PARAMETERS ========
DURATION = 24.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_22b_rtg"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'          # Indestructible Black UI
C_STEEL     = '#94A3B8'          # Vessel Structures
C_CARBON    = '#1E293B'          # Rigid Frame
C_COLD      = '#005599'          # Deep Marine (Space Radiators)
C_HOT       = '#FF3300'          # Intense Red (Plutonium Core)
C_ELEC      = '#FFB300'          # Dense Amber (Electrical Voltage)

# ------------------------------------------------------------------
# CONFIGURATION MATRICES 
# ------------------------------------------------------------------
NUM_FINS = 16
NUM_BRIDGES = 32
RAD_CORE = 140
RAD_BRIDGE_INNER = 160
RAD_BRIDGE_OUTER = 260
RAD_FIN_OUTER = 480
RAD_WIRE = 310

def interpolate_color(c1, c2, frac):
    rgb1 = np.array(mcol.to_rgb(c1))
    rgb2 = np.array(mcol.to_rgb(c2))
    return mcol.to_hex(rgb1 + (rgb2 - rgb1) * frac)

# Thermal Particle Array
N_THERMAL = 800
thermal_offsets = np.linspace(0, 1, N_THERMAL, endpoint=False)
thermal_angles = np.random.uniform(0, 2 * np.pi, N_THERMAL)

# Electrical Particle Array
N_ELEC = 600
elec_offsets = np.linspace(0, 2 * np.pi, N_ELEC, endpoint=False)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(data_packet):
    f, t_phase = data_packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # 9:16 Architectural Viewport scaling (Centered on Core)
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)

    # ====================================================
    # 1. HARDWARE MATRIX (Background Rigid Structure)
    # ====================================================

    # Cold Sink Radiator Fins (Deep Marine)
    for i in range(NUM_FINS):
        ang = (2 * np.pi / NUM_FINS) * i
        # Tapered polygon for heat fins
        w_inner = 25
        w_outer = 8
        pts = [
            [RAD_BRIDGE_OUTER * np.cos(ang) - w_inner * np.sin(ang), RAD_BRIDGE_OUTER * np.sin(ang) + w_inner * np.cos(ang)],
            [RAD_FIN_OUTER * np.cos(ang) - w_outer * np.sin(ang), RAD_FIN_OUTER * np.sin(ang) + w_outer * np.cos(ang)],
            [RAD_FIN_OUTER * np.cos(ang) + w_outer * np.sin(ang), RAD_FIN_OUTER * np.sin(ang) - w_outer * np.cos(ang)],
            [RAD_BRIDGE_OUTER * np.cos(ang) + w_inner * np.sin(ang), RAD_BRIDGE_OUTER * np.sin(ang) - w_inner * np.cos(ang)]
        ]
        ax.add_patch(patches.Polygon(pts, facecolor=C_COLD, edgecolor=C_TEXT, lw=2.5, zorder=5))

    # Outer Cold Containment Ring
    ax.add_patch(patches.Circle((0, 0), RAD_BRIDGE_OUTER, facecolor=C_BG, edgecolor=C_TEXT, lw=4, zorder=6))

    # Inner Hot Containment Ring
    ax.add_patch(patches.Circle((0, 0), RAD_BRIDGE_INNER, facecolor=C_BG, edgecolor=C_TEXT, lw=4, zorder=6))

    # The Thermal Bridges (Bimetallic elements capturing heat flux)
    for i in range(NUM_BRIDGES):
        ang = (2 * np.pi / NUM_BRIDGES) * i + (np.pi / NUM_BRIDGES)
        w_bridge = 12
        pts = [
            [RAD_BRIDGE_INNER * np.cos(ang) - w_bridge * np.sin(ang), RAD_BRIDGE_INNER * np.sin(ang) + w_bridge * np.cos(ang)],
            [RAD_BRIDGE_OUTER * np.cos(ang) - w_bridge * np.sin(ang), RAD_BRIDGE_OUTER * np.sin(ang) + w_bridge * np.cos(ang)],
            [RAD_BRIDGE_OUTER * np.cos(ang) + w_bridge * np.sin(ang), RAD_BRIDGE_OUTER * np.sin(ang) - w_bridge * np.cos(ang)],
            [RAD_BRIDGE_INNER * np.cos(ang) + w_bridge * np.sin(ang), RAD_BRIDGE_INNER * np.sin(ang) - w_bridge * np.cos(ang)]
        ]
        ax.add_patch(patches.Polygon(pts, facecolor=C_STEEL, edgecolor=C_TEXT, lw=2, zorder=7))

    # Center Plutonium Core
    pulse = 1.0 + 0.03 * np.sin(t_phase * 2 * np.pi * 6) # Slow thermodynamic pulse (6 beats per loop)
    ax.add_patch(patches.Circle((0, 0), RAD_CORE * pulse, facecolor=C_HOT, edgecolor=C_TEXT, lw=4, zorder=10))
    ax.add_patch(patches.Circle((0, 0), (RAD_CORE * 0.7) * pulse, facecolor=C_BG, alpha=0.3, zorder=11))

    # Electrical Wire Track (Circuit)
    ax.add_patch(patches.Circle((0, 0), RAD_WIRE, facecolor='none', edgecolor=C_CARBON, lw=18, zorder=3))

    # ====================================================
    # 2. O(N) KINEMATIC PARTICLE SWARMS
    # ====================================================

    # A. Thermal Heat Flux (Radiating outwards through the bridges)
    CYCLES_THERMAL = 6 # Particles do 6 full traversals over 24 seconds
    local_t_thermal = (thermal_offsets + (t_phase * CYCLES_THERMAL)) % 1.0
    
    # Map t to radius (RAD_BRIDGE_INNER to RAD_BRIDGE_OUTER)
    r_thermal = RAD_BRIDGE_INNER + local_t_thermal * (RAD_BRIDGE_OUTER - RAD_BRIDGE_INNER)
    x_thermal = r_thermal * np.cos(thermal_angles)
    y_thermal = r_thermal * np.sin(thermal_angles)
    
    # Heat particles lose energy (Red -> Blue) as they cross to the cold sink
    C_thermal = [interpolate_color(C_HOT, C_COLD, t) for t in local_t_thermal]
    ax.scatter(x_thermal, y_thermal, s=25, c=C_thermal, edgecolors='none', zorder=15)

    # B. Electrical Voltage Current (Orbiting the cold boundary)
    CYCLES_ELEC = 4 # Spins 4 times in 24 seconds
    base_ang_elec = elec_offsets - (t_phase * 2 * np.pi * CYCLES_ELEC)
    
    # Micro-jitter for high-energy electrical flow
    r_elec = RAD_WIRE + np.sin(elec_offsets * 40.0) * 4.0
    x_elec = r_elec * np.cos(base_ang_elec)
    y_elec = r_elec * np.sin(base_ang_elec)
    
    ax.scatter(x_elec, y_elec, s=18, c=C_ELEC, edgecolors='none', zorder=16)

    # ====================================================
    # 3. JARGON-FREE DAYLIGHT TELEMETRY 
    # ====================================================
    ax.add_patch(plt.Rectangle((-540, 780), 1080, 180, facecolor=C_BG, zorder=50))
    ax.plot([-460, 460], [780, 780], color=C_TEXT, lw=4, zorder=51)
    
    ax.text(-460, 880, "LG-22b :: NUCLEAR BATTERY (RTG ARCHITECTURE)", color=C_TEXT, fontsize=22, fontname='monospace', weight='bold', va='center', zorder=52)
    ax.text(-460, 830, "EXACT PHYSICAL CONSTRUCT & THERMAL TENSORS", color=C_STEEL, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=52)

    # Telemetry Left Block
    ax.add_patch(plt.Rectangle((-540, 520), 1080, 240, facecolor=C_BG, alpha=0.85, zorder=40))
    ax.text(-460, 710, "HEAT SOURCE : PLUTONIUM-238 ISOTOPE", color=C_HOT, fontsize=18, fontname='monospace', weight='bold', zorder=52)
    ax.text(-460, 660, "COLD SINK   : DEEP SPACE (0° KELVIN)", color=C_COLD, fontsize=18, fontname='monospace', weight='bold', zorder=52)
    ax.text(-460, 610, "CONVERSION  : THERMAL PRESSURE TO VOLTAGE", color=C_TEXT, fontsize=18, fontname='monospace', weight='bold', zorder=52)
    ax.text(-460, 560, "MOVING PARTS: ZERO (ABSOLUTE SOLID STATE)", color=C_TEXT, fontsize=18, fontname='monospace', zorder=52)

    # Bottom Status Block
    ax.add_patch(plt.Rectangle((-540, -960), 1080, 220, facecolor=C_BG, zorder=50))
    ax.plot([-460, 460], [-740, -740], color=C_TEXT, lw=4, zorder=51)
    
    # Calculate electrical output stability
    elec_kw = 290.0 + math.sin(t_phase * math.pi * 12) * 1.5 
    
    ax.text(-460, -820, "LAW OF PHYSICS : IF YOU ARE HOT AND THE WORLD IS COLD,", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=52)
    ax.text(-460, -870, "                 YOU HAVE INFINITE POWER.", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=52)
    ax.text(80, -845, f"YIELD: {elec_kw:>05.1f} W", color=C_ELEC, fontsize=24, fontname='monospace', weight='bold', zorder=52)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); plt.close('all'); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-22b: NUCLEAR BATTERY (DAYLIGHT) [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    # Generate exact stream parameters for a seamless loop
    stream = [(f, f / float(TOTAL_FRAMES)) for f in range(TOTAL_FRAMES)]

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, stream, chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Solid State Thermal Metrics Locked. Stand by for compilation.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
