"""
SOVEREIGN CODE: logic_garden_326_meanfield_tensor.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 326 (Mean-Field Theory // Topological Annealing Tensor)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Seamless 10.0s Loop. O(N) to O(1) Kinematic Smoothing. Memory Guard Active.
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
DURATION = 10.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_326_meanfield_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Low-Impact Scaffolding
C_STEEL     = '#606065'   # MFT Boundary Ring
C_DARK      = '#202025'   # Heavy Core Node
C_GOLD      = '#FFB300'   # Sovereign Target Core 
C_MAGENTA   = '#FF0055'   # Jagged N-Body Entropy Lines
C_CYAN      = '#00FFFF'   # Rigid MFT Scalar Piston
C_WHITE     = '#FFFFFF'

# -------- O(N) ORBITAL LATTICE CONFIGURATION --------
np.random.seed(326)
NUM_NODES = 150
node_radii = np.linspace(220, 520, NUM_NODES)
# We shuffle so inner/outer tracks are visually chaotic
np.random.shuffle(node_radii) 
node_base_angles = np.random.uniform(0, 2*np.pi, NUM_NODES)
# Absolute integer multiples guarantee exact spatial reset at phase=1.0
node_speeds = np.random.choice([-3, -2, -1, 1, 2, 3], NUM_NODES)
# Phase offsets for independent pseudo-chaotic movement
node_phases = np.random.uniform(0, 2*np.pi, NUM_NODES)

def draw_mft_pistons(ax, mft_val):
    """The idealized O(1) force replacing the chaotic particle field."""
    if mft_val < 0.01: return
    
    # 4 orthogonal heavy vectors pushing from the boundary ring into the central core
    for angle in [0, 90, 180, 270]:
        trans = transforms.Affine2D().rotate_deg(angle) + ax.transData
        # Mechanical bracket
        ax.add_patch(patches.Rectangle((40, -15), 140, 30, facecolor=C_CYAN, alpha=mft_val*0.8, transform=trans, zorder=6))
        # Structural edge
        ax.plot([40, 180], [0, 0], color=C_TEXT, lw=4, alpha=mft_val, transform=trans, zorder=6.1)
        # Interface contact point at core
        ax.plot([40, 40], [-25, 25], color=C_DARK, lw=6, alpha=mft_val, transform=trans, zorder=6.2)

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

    # 1. KINEMATIC INTEGRATION WAVE
    # Continuous smooth wave spanning 0 (Pure Chaos) -> 1 (Pure Mean-Field) -> 0
    mft_val = 0.5 - 0.5 * np.cos(phase_ratio * 2 * np.pi)
    chaos_val = 1.0 - mft_val

    # 2. CORE TARGET ENGINETOPOLOGY
    # High frequency jitter directly proportional to unconstrained entropy
    jitter_amp = 18.0 * (chaos_val ** 2)
    jitter_x = np.sin(phase_ratio * 34 * np.pi) * jitter_amp
    jitter_y = np.cos(phase_ratio * 46 * np.pi) * jitter_amp
    
    core_x, core_y = jitter_x, jitter_y

    # 3. BACKGROUND ORBITAL LATTICE (N-BODY TENSOR)
    target_boundary_r = 180
    
    for i in range(NUM_NODES):
        # Deterministic kinematic positions
        theta = node_base_angles[i] + phase_ratio * 2 * np.pi * node_speeds[i]
        
        # Radial fluctuation (Thermal noise)
        rad_noise = np.sin(phase_ratio * 2 * np.pi * abs(node_speeds[i]) + node_phases[i]) * 20
        r = node_radii[i] + rad_noise
        
        nx = r * np.cos(theta)
        ny = r * np.sin(theta)
        
        # O(N) Chaotic Stress Vectors
        # At chaos_val=1.0, the magenta lines shatter the boundary and hammer the vibrating core.
        # At chaos_val=0.0, the lines clip exactly at R=180, absorbed by the Mean-Field ring.
        t_alpha = 0.5 * chaos_val + 0.1 # Base visibility
        
        if mft_val > 0.05:
            # Clip mathematics for MFT boundary intersection
            intersect_x = target_boundary_r * np.cos(theta)
            intersect_y = target_boundary_r * np.sin(theta)
            
            # Outer segment (Node to Boundary)
            ax.plot([nx, intersect_x], [ny, intersect_y], color=C_STEEL, lw=1.0, alpha=0.3 + 0.3*mft_val, zorder=2)
            # Inner segment (Boundary to Core - fades out)
            ax.plot([intersect_x, core_x], [intersect_y, core_y], color=C_MAGENTA, lw=1.5, alpha=t_alpha*0.8, zorder=2.1)
        else:
            # Total Chaos State
            ax.plot([nx, core_x], [ny, core_y], color=C_MAGENTA, lw=1.5, alpha=t_alpha, zorder=2.1)

        # Draw Node
        ax.add_patch(patches.Circle((nx, ny), radius=6, facecolor=C_TITANIUM, edgecolor=C_STEEL, lw=0.5, alpha=0.8, zorder=4))

    # 4. MEAN-FIELD INTEGRATION RING
    # Materializes mathematically from the chaos fields
    if mft_val > 0.01:
        # Thick outer integration drum
        ax.add_patch(patches.Circle((0, 0), radius=target_boundary_r, fill=False, edgecolor=C_STEEL, lw=15 * mft_val, alpha=mft_val*0.9, zorder=5))
        ax.add_patch(patches.Circle((0, 0), radius=target_boundary_r+7, fill=False, edgecolor=C_TEXT, lw=2 * mft_val, alpha=mft_val, zorder=5.1))
        # Inner clear zone mapping the O(1) sanctuary
        ax.add_patch(patches.Circle((0, 0), radius=target_boundary_r-8, facecolor=C_BG, alpha=mft_val*0.8, zorder=3))
        
        # Deploy Rigid MFT Scalar Force
        draw_mft_pistons(ax, mft_val)

    # 5. SOVEREIGN CORE RENDERING
    # Core locks into absolute rigidity as MFT completes
    ax.add_patch(patches.Rectangle((core_x-35, core_y-35), 70, 70, facecolor=C_GOLD, edgecolor=C_TEXT, lw=3, zorder=7))
    ax.add_patch(patches.Circle((core_x, core_y), radius=20, facecolor=C_DARK, zorder=7.1))

    # 6. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    ax.text(-500, 880, "LG-326 :: MEAN-FIELD APPROXIMATION TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, 840, "[SFI-0.75] THEORETICAL BOUND // O(N) TO O(1) TOPOLOGICAL ANNEALING", color=C_CYAN, fontsize=12, fontname='monospace', zorder=80)
    
    ax.add_patch(patches.Rectangle((-520, -920), 1040, 200, facecolor=C_TITANIUM, alpha=0.9, zorder=79))
    
    # State Engine Text
    state_color = C_CYAN if mft_val > 0.5 else C_MAGENTA
    state_text = "MEAN-FIELD EQUILIBRIUM: O(1) RIGID OVERRIDE" if mft_val > 0.5 else "BARYONIC CHAOS: O(N) INTERACTION ENTROPY"
    ax.text(-500, -760, f"SYSTEM OPERATION: {state_text}", color=state_color, fontsize=16, fontname='monospace', weight='bold', zorder=80)
    
    # Bar 1: Entropy (Decreases as MFT establishes)
    ax.text(-500, -820, f"N-BODY KINETIC EXHAUST (JITTER): {chaos_val * 100:>05.2f} %", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=80)
    ax.add_patch(patches.Rectangle((-500, -840), 1000, 4, facecolor=C_STEEL, zorder=80))
    ax.add_patch(patches.Rectangle((-500, -840), 1000 * chaos_val, 4, facecolor=C_MAGENTA, zorder=81))

    # Bar 2: Mean-Field Scalar
    ax.text(-500, -875, f"SCALAR FIELD APPROXIMATION LOCK: {mft_val * 100:>05.2f} %", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=80)
    ax.add_patch(patches.Rectangle((-500, -895), 1000, 4, facecolor=C_STEEL, zorder=80))
    ax.add_patch(patches.Rectangle((-500, -895), 1000 * mft_val, 4, facecolor=C_CYAN, zorder=81))

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
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-326: MEAN-FIELD TOPOLOGICAL ANNEALING [CORES: {cpu_cores}] [MEMORY LOCK ACTIVE]")
    
    # HOTFIX: maxtasksperchild=1 explicitly eradicates C-backend fragmentation
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
