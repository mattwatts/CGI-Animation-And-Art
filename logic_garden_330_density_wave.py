"""
SOVEREIGN CODE: logic_garden_330_density_wave.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Vectorization
SCENE: Logic Garden 330 (Density Wave Theory // Lin-Shu Kinematics)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Seamless 10.0s Loop. Absolute Camera Lock. O(N) to O(1) Parity. Tuple Rupture Sealed.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.transforms as transforms
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
DURATION = 10.0  # 10.0 Second Seamless Loop
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_330_density_wave"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Low-Impact Orbital Tracks
C_STEEL     = '#606065'   # Mild Compression
C_DARK      = '#202025'   # Unperturbed Vacuum Stars
C_GOLD      = '#FFB300'   # High Compression (Entering the Jam)
C_CYAN      = '#00FFFF'   # The Invisible Density Wave Potential
C_MAGENTA   = '#FF0055'   # Peak Friction / Maximum Traffic Jam
C_WHITE     = '#FFFFFF'

# -------- KINEMATIC CONSTANTS --------
R_MIN = 60
R_MAX = 460
R_STEP = 10
BETA = 1.35  # Logarithmic spiral tightness (1/tan(alpha))
AMPLITUDE = 0.45  # The strength of the "Traffic Jam" perturbation

# Pre-compute static structural nodes to ensure O(1) generation
# We create arrays of R, theta_0, and orbital speed k
node_r = []
node_theta0 = []
node_k = []

for r in range(R_MIN, R_MAX + R_STEP, R_STEP):
    # Inner stars move faster (higher K integer). Outer stars move slower.
    # We must rigorously lock K to integers [1, 2, 3, 4] to guarantee the 10.0s loop parity.
    if r < 140:
        k = 4
    elif r < 240:
        k = 3
    elif r < 360:
        k = 2
    else:
        k = 1
        
    num_stars = int(r * 0.8)  # Track circumference determines array size
    theta_arr = np.linspace(0, 2*np.pi, num_stars, endpoint=False)
    
    node_r.extend([r] * num_stars)
    node_k.extend([k] * num_stars)
    node_theta0.extend(theta_arr)

node_r = np.array(node_r)
node_k = np.array(node_k)
node_theta0 = np.array(node_theta0)
total_nodes = len(node_r)

def render_frame(packet):
    f, phase_ratio = packet
    
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

    # 1. DRAW O(1) BASE TRACKS
    for r in range(R_MIN, R_MAX + R_STEP, R_STEP * 4):
        ax.add_patch(patches.Circle((0, 0), radius=r, fill=False, edgecolor=C_TITANIUM, linestyle=":", lw=1, alpha=0.5, zorder=1))

    # 2. CALCULATE THE GRAVITATIONAL WAVE (The Blueprint)
    # The pattern speed Omega_P rotates exactly 1 full revolution per loop
    theta_p = phase_ratio * 2 * np.pi
    
    # Draw the theoretical C_CYAN boundary defining the two spiral potentials
    scan_r = np.linspace(R_MIN/2, R_MAX + 50, 200)
    phi_r = BETA * np.log(scan_r / (R_MIN/2))
    
    arm1_theta = theta_p + phi_r
    arm2_theta = theta_p + phi_r + np.pi
    
    ax.plot(scan_r * np.cos(arm1_theta), scan_r * np.sin(arm1_theta), color=C_CYAN, lw=4, alpha=0.3, zorder=2)
    ax.plot(scan_r * np.cos(arm2_theta), scan_r * np.sin(arm2_theta), color=C_CYAN, lw=4, alpha=0.3, zorder=2)

    # 3. KINEMATIC INTEGRATION (The Traffic Jam Math)
    base_theta = node_theta0 + node_k * (phase_ratio * 2 * np.pi)
    phi_res = BETA * np.log(node_r / (R_MIN/2))
    delta_theta = base_theta - theta_p - phi_res
    
    theta_actual = base_theta - AMPLITUDE * np.sin(2 * delta_theta)
    
    xs = node_r * np.cos(theta_actual)
    ys = node_r * np.sin(theta_actual)

    # 4. THERMODYNAMIC FRICTION ASSIGNMENT (Heat Map)
    cos_val = np.cos(2 * delta_theta)
    
    idx_magenta = cos_val > 0.85
    idx_gold = (cos_val > 0.4) & (cos_val <= 0.85)
    idx_steel = (cos_val > -0.2) & (cos_val <= 0.4)
    idx_dark = cos_val <= -0.2

    ax.scatter(xs[idx_dark], ys[idx_dark], c=C_DARK, s=15, marker='s', edgecolors='none', zorder=4)
    ax.scatter(xs[idx_steel], ys[idx_steel], c=C_STEEL, s=18, marker='s', edgecolors='none', zorder=4.1)
    ax.scatter(xs[idx_gold], ys[idx_gold], c=C_GOLD, s=25, marker='s', edgecolors='none', zorder=4.2)
    ax.scatter(xs[idx_magenta], ys[idx_magenta], c=C_MAGENTA, s=35, marker='s', edgecolors=C_BG, lw=0.5, zorder=4.3)
    
    # Central Core Anchor
    ax.add_patch(patches.Circle((0, 0), radius=35, facecolor=C_DARK, edgecolor=C_TEXT, lw=3, zorder=8))
    ax.add_patch(patches.Circle((0, 0), radius=20, facecolor=C_GOLD, edgecolor=C_BG, lw=1.5, zorder=8.1))

    # 5. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    ax.text(-500, 880, "LG-330 :: DENSITY WAVE TENSOR (LIN-SHU)", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, 840, "[SFI-1.00] MACRO-STRUCTURAL KINEMATICS // O(1) COMPRESSION", color=C_STEEL, fontsize=12, fontname='monospace', zorder=80)
    
    # Telemetry Data Background
    ax.add_patch(patches.Rectangle((-520, -920), 1040, 240, facecolor=C_TITANIUM, alpha=0.9, zorder=79))
    
    # Active Physics Readout
    ax.text(-500, -740, "GRAVITATIONAL WAVE PATTERN (Ωp): +1.0 LCK", color=C_CYAN, fontsize=15, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, -780, "BARYONIC ORBITAL FLUX (Ω*): K-VAR INTEGER ARRAY", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, -820, "PHYSICAL STATE: COLLISIONAL TRAFFIC IMPEDANCE", color=C_GOLD, fontsize=14, fontname='monospace', weight='bold', zorder=80)
    
    pulse = (np.sin(phase_ratio * 4 * np.pi) ** 2)
    ax.text(-500, -860, f"LOCAL NODE COMPRESSION STRESS: {pulse * 100:>05.2f} % Δ [PEAK LIMIT]", color=C_MAGENTA if pulse > 0.8 else C_STEEL, fontsize=14, fontname='monospace', weight='bold', zorder=80)
    
    # Twin structural tracking bars
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 4, facecolor=C_STEEL, zorder=80))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 4, facecolor=C_CYAN, zorder=81))
    
    ax.add_patch(patches.Rectangle((-500, -910), 1000, 4, facecolor=C_STEEL, zorder=80))
    
    # [HOTFIX]: Oscillating stress tensor bar, XY-Tuple securely locked
    ax.add_patch(patches.Rectangle((-500 + 490*(1-pulse), -910), 20 + 980*pulse, 4, facecolor=C_MAGENTA, zorder=81))

    # Sovereign Execution Output: Crop eradication mathematically locked
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
    # Enforce Executioner Protocol
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-330: DENSITY WAVE TENSOR [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE] [NODES: {total_nodes}]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
