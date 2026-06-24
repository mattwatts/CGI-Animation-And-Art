"""
SOVEREIGN CODE: logic_garden_331_decay_tensor.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Vectorization
SCENE: Logic Garden 331 (Radioactive Decay // Stochastic Half-Life Tensor)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Absolute Camera Lock. O(1) Memory Eradication. Tuple Ruptures Sealed.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
DURATION = 15.0  # 15.0 Second Exhaustion Cycle
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_331_decay_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Stable Daughter Isotope (Quiet Lattice)
C_STEEL     = '#606065'   # HUD Elements
C_DARK      = '#202025'   # Unstable Parent Isotope (Fever Jitter)
C_GOLD      = '#FFB300'   # Beta Radiation (e- Ejection)
C_CYAN      = '#00FFFF'   # Telemetry Sweeper
C_MAGENTA   = '#FF0055'   # Alpha Radiation (He2+ Ejection)
C_WHITE     = '#FFFFFF'

# -------- KINEMATIC CONSTANTS --------
HALF_LIFE = 2.2 # Seconds
LAMBDA_DECAY = np.log(2) / HALF_LIFE

# ------------------------------------------------------------------
# O(1) DETERMINISTIC MATRIX CACHE (BARYONIC HEX GRID)
# ------------------------------------------------------------------
R_CORE = 360
SPACING = 32

node_x = []
node_y = []

# Generate a dense hexagonal lattice mask
for q in range(-20, 20):
    for r in range(-20, 20):
        x = SPACING * np.sqrt(3) * (q + r/2.0)
        y = SPACING * 1.5 * r
        if x*x + (y-100)*(y-100) < R_CORE*R_CORE: # Offset Y slightly up
            node_x.append(x)
            node_y.append(y + 100)

N_NODES = len(node_x)
node_x = np.array(node_x)
node_y = np.array(node_y)

# STOCHASTIC PHYSICS INGESTION
np.random.seed(331)
# Calculate exact decay time for every node using Inverse Transform Sampling
U = np.random.uniform(0.0001, 1.0, N_NODES)
decay_times = -np.log(U) / LAMBDA_DECAY

# Assign Decay Mode (0: Alpha, 1: Beta)
decay_modes = np.random.choice([0, 1], N_NODES, p=[0.6, 0.4])

# Assign Ejection Vectors (Random angle)
ejection_angles = np.random.uniform(0, 2*np.pi, N_NODES)
V_ALPHA = 15.0
V_BETA = 45.0

# Pre-calculate ideal exponential curve for the HUD
hud_times = np.linspace(0, DURATION, 300)
hud_ideal_N = N_NODES * np.exp(-LAMBDA_DECAY * hud_times)

def render_frame(packet):
    f, t = packet
    
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

    # 1. EVALUATE MATRIX STATE
    is_decayed = t >= decay_times
    is_unstable = ~is_decayed
    
    num_unstable = np.sum(is_unstable)
    num_stable = N_NODES - num_unstable
    
    # Mathematical Kinematic Fever (Unstable nodes vibrate violently)
    # They do NOT know when they will decay, so vibration is constant until the exact cutoff.
    jx = np.where(is_unstable, np.random.uniform(-3, 3, N_NODES), 0)
    jy = np.where(is_unstable, np.random.uniform(-3, 3, N_NODES), 0)
    
    curr_x = node_x + jx
    curr_y = node_y + jy

    # Plot Stable Daughter Isotopes (Cold, dead lattice)
    ax.scatter(curr_x[is_decayed], curr_y[is_decayed], c=C_TITANIUM, s=160, marker='H', edgecolors=C_BG, lw=1, zorder=3)
    
    # Plot Unstable Parent Isotopes (Fever state)
    ax.scatter(curr_x[is_unstable], curr_y[is_unstable], c=C_DARK, s=160, marker='H', edgecolors=C_TEXT, lw=1.5, zorder=4)

    # 2. RADIATION EJECTION KINEMATICS
    # Calculate flight vectors for nodes that decayed recently (within 0.8 seconds)
    time_since_decay = t - decay_times
    in_flight = (time_since_decay > 0) & (time_since_decay < 0.8)
    
    for idx in np.where(in_flight)[0]:
        dt = time_since_decay[idx]
        mode = decay_modes[idx]
        angle = ejection_angles[idx]
        
        # Fade out radiation over its flight time
        alpha_rad = max(0, 1.0 - (dt / 0.8))
        
        if mode == 0:
            # ALPHA DECAY: Heavy, slow, high-damage (Magenta)
            dist = V_ALPHA * dt * 60 # Scale by framerate approximation
            rx = curr_x[idx] + np.cos(angle) * dist
            ry = curr_y[idx] + np.sin(angle) * dist
            
            # Ejection trail
            ax.plot([curr_x[idx], rx], [curr_y[idx], ry], color=C_MAGENTA, lw=3, alpha=alpha_rad*0.5, zorder=5)
            # Alpha Particle
            ax.scatter(rx, ry, c=C_MAGENTA, s=80, edgecolors=C_BG, lw=1, alpha=alpha_rad, zorder=6)
            
        else:
            # BETA DECAY: Lightweight, hyper-fast electron (Gold)
            dist = V_BETA * dt * 60
            rx = curr_x[idx] + np.cos(angle) * dist
            ry = curr_y[idx] + np.sin(angle) * dist
            
            # Fast trail
            ax.plot([curr_x[idx], rx], [curr_y[idx], ry], color=C_GOLD, lw=1.5, alpha=alpha_rad*0.8, zorder=5)
            # Electron point
            ax.scatter(rx, ry, c=C_BG, s=30, edgecolors=C_GOLD, lw=2, alpha=alpha_rad, zorder=6)

    # 3. STATIC WIDGETS
    ax.text(-500, 880, "LG-331 :: RADIOACTIVE DECAY TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, 840, f"[SFI-1.00] STOCHASTIC QUANTUM TUNNELING // T(1/2) = {HALF_LIFE}s", color=C_STEEL, fontsize=12, fontname='monospace', zorder=80)
    
    # 4. ACTIVE EXPONENTIAL DECAY HUD
    hud_y = -900
    hud_h = 180
    
    # Background enclosure [Strict Tuple Enforcement]
    ax.add_patch(patches.Rectangle((-520, -940), 1040, 260, facecolor=C_TITANIUM, alpha=0.9, zorder=79))
    
    # Live Digital Readout
    ax.text(-480, -730, f"UNSTABLE PARENT ISOTOPES : {num_unstable:>04d}", color=C_DARK, fontsize=16, fontname='monospace', weight='bold', zorder=80)
    ax.text(-480, -770, f"STABLE DAUGHTER NUCLEI   : {num_stable:>04d}", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=80)
    
    # Calculate instantaneous activity (radiation rate) over last 0.2 seconds
    recent_decays = np.sum((t - decay_times > 0) & (t - decay_times < 0.2))
    ax.text(-480, -810, f"RADIATION ACTIVITY FLUX  : {recent_decays:>04d} EVT/s", color=C_MAGENTA, fontsize=16, fontname='monospace', weight='bold', zorder=80)
    
    # Mathematical Graph Line Overlay
    # Scale X from 0 to DURATION across the 900px wide box
    graph_x = -450 + (hud_times / DURATION) * 900
    graph_y = hud_y + (hud_ideal_N / N_NODES) * 80
    ax.plot(graph_x, graph_y, color=C_STEEL, lw=3, zorder=80)
    ax.plot([-450, 450], [hud_y, hud_y], color=C_TEXT, lw=2, zorder=80) # Baseline
    
    # Live Sweeper
    current_x = -450 + (t / DURATION) * 900
    current_y = hud_y + (num_unstable / N_NODES) * 80
    ax.plot([current_x, current_x], [-920, -710], color=C_CYAN, lw=2, linestyle='--', zorder=81)
    ax.scatter(current_x, current_y, c=C_MAGENTA, s=100, zorder=82)

    # Sovereign Execution Output: Crop eradication mathematically locked
    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    # Absolute Memory Annihilation
    plt.close('all')
    gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(FPS))

def run_batch():
    # Enforce Executioner Protocol
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-331: RADIOACTIVE DECAY TENSOR [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE] [NODES: {N_NODES}]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
