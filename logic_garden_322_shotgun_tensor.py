"""
SOVEREIGN CODE: logic_garden_322_shotgun_tensor.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 322 (Kinematic Shot Separation Tensor)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Syntactic Leak Purged. C_STEEL permanently welded to global matrix.
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
OUT_DIR = "frames_322_shotgun_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_BARREL    = '#303035'   # Heavy Ordnance Steel
C_STEEL     = '#606065'   # Telemetry & Structural Shadow
C_WAD       = '#EAEAEA'   # High-Density Plastic Sabot
C_SHOT      = '#222226'   # Lead Payload
C_GAS_CORE  = '#FF4400'   # Thermodynamic Ignition
C_GAS_OUTER = '#0066FF'   # High-Pressure Vortex (Azure)
C_CYAN      = '#00FFFF'   # Telemetry UI
C_WHITE     = '#FFFFFF'

# ------------------------------------------------------------------
# O(1) DETERMINISTIC SHOT PAYLOAD
# ------------------------------------------------------------------
# Absolute seed guarantees identical polygon arrays across all distributed cores
np.random.seed(322)
NUM_PELLETS = 150

# Generate packed cylinder coordinates
shot_x0 = np.random.uniform(-35, 35, NUM_PELLETS)
shot_y0 = np.random.uniform(-40, 40, NUM_PELLETS)

# Pre-compute rigid exit vectors for radial spread
shot_vx = shot_x0 * np.random.uniform(0.5, 2.0, NUM_PELLETS)
shot_vy = shot_y0 * np.random.uniform(0.5, 3.5, NUM_PELLETS)
shot_sizes = np.random.uniform(4.0, 7.0, NUM_PELLETS)

def draw_wadding(ax, x, y, petal_angle, alpha_m):
    """Rigid Sabot Petal Mechanics"""
    # Main Base Cup
    ax.add_patch(patches.Rectangle((x - 80, y - 45), 60, 90, facecolor=C_WAD, edgecolor=C_TEXT, lw=2, alpha=alpha_m, zorder=5))
    
    # Internal Structural Webbing
    for wy in range(y - 30, y + 40, 15):
        ax.plot([x - 70, x - 25], [wy, wy], color=C_TEXT, lw=1, alpha=alpha_m*0.5, zorder=5.1)

    # Upper Petal (Rotates UP)
    trans_up = transforms.Affine2D().rotate_deg_around(x - 20, y + 45, petal_angle) + ax.transData
    ax.add_patch(patches.Rectangle((x - 20, y + 40), 60, 5, facecolor=C_WAD, edgecolor=C_TEXT, lw=1.5, alpha=alpha_m, transform=trans_up, zorder=5.2))
    
    # Lower Petal (Rotates DOWN)
    trans_dn = transforms.Affine2D().rotate_deg_around(x - 20, y - 45, -petal_angle) + ax.transData
    ax.add_patch(patches.Rectangle((x - 20, y - 45), 60, 5, facecolor=C_WAD, edgecolor=C_TEXT, lw=1.5, alpha=alpha_m, transform=trans_dn, zorder=5.2))

def render_frame(packet):
    f, phase_ratio = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)

    # 1. KINEMATIC TIME SPLITS
    # The action sequences perfectly over 8.0s (0.0 to 0.8 phase). Reset occurs from 8.0s to 10.0s.
    t_act = min(1.0, phase_ratio / 0.8)
    t_rst = max(0.0, (phase_ratio - 0.8) / 0.2)
    
    # Global Loop Master Alpha (Purges the screen smoothly for the wrap)
    alpha_master = 1.0 - (t_rst ** 3)
    if phase_ratio < 0.05:
        alpha_master = phase_ratio / 0.05

    # 2. THE EXPULSION MECHANICS
    # The shot is tracked at X=0. The universe moves left around it.
    
    # Barrel trajectory: recoils back, mathematically snaps back during reset
    barrel_x = -300 - (t_act ** 0.3) * 1200 + (t_rst ** 2) * 1200
    
    # Wadding trajectory: drag forces it to fall behind
    wad_x = -15 - (t_act ** 1.8) * 600 - (t_rst ** 2) * 1500
    wad_angle = min(85, t_act * 350) # Petals peel open aggressively then lock at 85 deg
    
    # Gas Exhaust Toroidal Vortex
    gas_x = barrel_x + 150 + (t_act ** 0.6) * 500
    gas_radius = 80 + (t_act ** 0.8) * 600
    gas_alpha = max(0, 1.0 - (t_act ** 1.5)) * alpha_master
    
    # Gas Rendering
    if gas_alpha > 0:
        # Core Blast Flame
        ax.add_patch(patches.Circle((gas_x - 100, 0), radius=gas_radius*0.4, color=C_GAS_CORE, alpha=gas_alpha*0.8, zorder=2))
        # Upper Blue Vortex
        ax.add_patch(patches.Circle((gas_x, 150 + t_act*200), radius=gas_radius*0.6, color=C_GAS_OUTER, alpha=gas_alpha*0.6, zorder=3))
        # Lower Blue Vortex
        ax.add_patch(patches.Circle((gas_x, -150 - t_act*200), radius=gas_radius*0.6, color=C_GAS_OUTER, alpha=gas_alpha*0.6, zorder=3))

    # Barrel Rendering
    ax.add_patch(patches.Rectangle((barrel_x - 1200, -70), 1200, 140, facecolor=C_BARREL, edgecolor=C_TEXT, lw=4, alpha=alpha_master, zorder=4))
    
    # Wadding Rendering
    draw_wadding(ax, wad_x, 0, wad_angle, alpha_master)

    # 3. SHOT PAYLOAD MATRIX (O(1) Hexagons)
    # The shot spreads violently at the very end to clear the CoM for the loop wrap.
    current_shot_x = shot_x0 + (shot_vx * t_act * 8) + (shot_vx * (t_rst ** 3) * 150)
    current_shot_y = shot_y0 + (shot_vy * t_act * 8) + (shot_vy * (t_rst ** 3) * 150)
    
    for i in range(NUM_PELLETS):
        ax.add_patch(patches.RegularPolygon(
            (current_shot_x[i], current_shot_y[i]), 
            numVertices=6, 
            radius=shot_sizes[i], 
            facecolor=C_SHOT, 
            edgecolor=C_BG, 
            lw=0.5, 
            alpha=alpha_master, 
            zorder=6
        ))

    # 4. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    ax.text(-500, 880, "LG-322 :: KINEMATIC SHOT SEPARATION TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, 840, "[SFI-1.00] 1/1,000,000s EXPOSURE // AERODYNAMIC SHEDDING", color=C_STEEL, fontsize=12, fontname='monospace', zorder=80)
    
    # Telemetry Data Background
    ax.add_patch(patches.Rectangle((-520, -920), 1040, 160, facecolor=C_WAD, alpha=0.9, zorder=79))
    
    # Microsecond Tracker (Mapping 10.0 macro-seconds to 10.0 microseconds)
    math_time = np.sin(phase_ratio * np.pi) * 10.0
    ax.text(-500, -820, f"PAYLOAD KINEMATICS TIME: {math_time:>05.2f} µs", color=C_TEXT, fontsize=18, fontname='monospace', weight='bold', zorder=80)
    
    pulse = abs(np.sin(phase_ratio * 4 * np.pi))
    ax.text(-500, -855, f"WIDGET DRAG DIFFERENTIAL: ΔCd {wad_angle*0.015:>04.2f} // P-SPREAD {t_act*40:>04.2f}mm", color=C_GAS_OUTER if pulse > 0.5 else C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=80)
    
    ax.add_patch(patches.Rectangle((-500, -880), 1000, 4, facecolor=C_STEEL, zorder=80))
    ax.add_patch(patches.Rectangle((-500, -880), 1000 * t_act, 4, facecolor=C_BARREL, zorder=81))

    # Coordinate Origin Geometry (Confirms camera is locked to CoM)
    ax.plot([-40, 40], [0, 0], color=C_CYAN, lw=1, alpha=0.5, zorder=80)
    ax.plot([0, 0], [-40, 40], color=C_CYAN, lw=1, alpha=0.5, zorder=80)
    ax.add_patch(patches.Circle((0, 0), radius=5, facecolor='none', edgecolor=C_CYAN, lw=1, alpha=0.8, zorder=80))

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0)
    
    # Absolute Memory Annihilation execution
    plt.close('all')
    gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    # Retain 1 core to prevent OS suffocation during intensive O(1) tracking computations
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-322: KINEMATIC SHOT SEPARATION [CORES: {cpu_cores}] [MEMORY LOCK ACTIVE]")
    
    # HOTFIX: maxtasksperchild=1 explicitly eradicates C-backend fragmentation
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
