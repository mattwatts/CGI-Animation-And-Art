"""
SOVEREIGN CODE: logic_garden_18d_transmutation.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Vectorization
SCENE: Logic Garden 18d (Plutonium-239 Breeder Tensor // Kinematic Carousel)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Seamless 10.0s Loop. Absolute Camera Lock. O(1) Memory Eradication.
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
DURATION = 10.0  # 10.0 Second Seamless Loop
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_18d_transmutation"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Background Factory Rails
C_STEEL     = '#606065'   # Heavy Neutrons (Ballast)
C_DARK      = '#202025'   # Core Protons (Solid Identity)
C_CYAN      = '#00FFFF'   # The Ghost Neutron Flux
C_MAGENTA   = '#FF0055'   # U-239 Instability Fever Tensor
C_GOLD      = '#FFB300'   # Beta Spark Emissions (Electrons)

# -------- O(1) DETERMINISTIC NUCLEON MATRIX (FERMAT PHYLLOTAXIS) --------
N_TOTAL = 239
# Generates a highly realistic, tightly packed mathematical nucleus
phi = np.arange(N_TOTAL) * (np.pi * (3.0 - np.sqrt(5.0)))
r_val = 11.5 * np.sqrt(np.arange(N_TOTAL))
PX = r_val * np.cos(phi)
PY = r_val * np.sin(phi)

# Sort coordinates purely by X-axis to lock boundary geometry mechanics
pt_idx = list(range(N_TOTAL))
pt_idx.sort(key=lambda x: PX[x])

IDX_GHOST = pt_idx[0]       # Leftmost point (Neutron Injection Socket)
IDX_TARGET_2 = pt_idx[1]    # Second Leftmost (Beta 2 Ejection Socket)
IDX_TARGET_1 = pt_idx[-1]   # Rightmost point (Beta 1 Ejection Socket)

# Distribute remaining 92 Protons and 144 Neutrons rigorously
rem = pt_idx[2:-1]
np.random.seed(18)
np.random.shuffle(rem)
IDX_PROTONS = rem[:92]
IDX_NEUTRONS = rem[92:]

N_TYPES = np.zeros(N_TOTAL, dtype=int)
N_TYPES[IDX_GHOST] = 4
N_TYPES[IDX_TARGET_2] = 3
N_TYPES[IDX_TARGET_1] = 2
for i in IDX_PROTONS: N_TYPES[i] = 0
for i in IDX_NEUTRONS: N_TYPES[i] = 1

# Mathematical pseudo-random seed offsets for core jitter
J_SEED = np.arange(N_TOTAL) * 13.7

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

    # 1. INDUSTRIAL FACTORY SCAFFOLDING
    # The Sovereign Core Rail
    ax.plot([0, 0], [-960, 960], color=C_STEEL, lw=12, alpha=0.9, zorder=0)
    ax.plot([-20, 20], [-960, 960], color=C_TEXT, lw=1, alpha=0.3, zorder=0.1)

    # Neutron Injection Manifold (Y=500)
    ax.plot([-540, -180], [500, 500], color=C_CYAN, lw=8, alpha=0.9, zorder=1)
    ax.add_patch(patches.Rectangle((-540, 485), 100, 30, facecolor=C_DARK, zorder=2))
    
    # Beta Ejection Manifold 1 (Y=100)
    ax.plot([180, 540], [100, 100], color=C_GOLD, lw=4, alpha=0.8, zorder=1)
    ax.add_patch(patches.Rectangle((440, 90), 100, 20, facecolor=C_DARK, zorder=2))

    # Beta Ejection Manifold 2 (Y=-300)
    ax.plot([-540, -180], [-300, -300], color=C_GOLD, lw=4, alpha=0.8, zorder=1)
    ax.add_patch(patches.Rectangle((-540, -310), 100, 20, facecolor=C_DARK, zorder=2))

    # 2. THE KINEMATIC CAROUSEL LOGIC
    # Loops exactly over 5 cores running vertically
    nearest_cy = 9999
    
    for i in range(-2, 4):
        # Y traverses strictly down 1000px per cycle
        cy = (i - phase_ratio) * 1000
        
        # Out-of-bounds CPU bypass
        if cy > 1400 or cy < -1400: continue
        
        # HUD Tracking Math
        if abs(cy) < abs(nearest_cy): nearest_cy = cy

        # STATE LOGIC BOOLS
        has_ghost = cy <= 500
        is_fever = 100 < cy <= 500
        is_half_fever = -300 < cy <= 100
        t1_decayed = cy <= 100
        t2_decayed = cy <= -300

        # KINEMATIC HEATING (Jitter)
        mag = 0.0
        if is_fever: mag = 4.5
        elif is_half_fever: mag = 2.0
        
        # Perfect cyclic wave generation
        jx = np.sin((phase_ratio * 40 * np.pi) + J_SEED) * mag
        jy = np.cos((phase_ratio * 40 * np.pi) + J_SEED) * mag

        abs_x = PX + jx
        abs_y = PY + jy + cy

        # -----------------------------------------------
        # DYNAMIC VECTORS (Horizontal factory processing)
        # -----------------------------------------------
        # A) Incoming Neutron (Left tracking)
        if not has_ghost:
            dy = cy - 500
            abs_x[IDX_GHOST] = PX[IDX_GHOST] - dy * 1.5
            abs_y[IDX_GHOST] = 500
            
        # B) Ejected Beta 1 (Right tracking)
        if t1_decayed:
            dy = 100 - cy
            if dy < 300: # Opacity limit
                bx = abs_x[IDX_TARGET_1] + dy * 2.5
                by = 100
                al = max(0.0, 1.0 - dy/300.0)
                ax.scatter(bx, by, c=C_GOLD, s=90, alpha=al, zorder=15)
                ax.plot([abs_x[IDX_TARGET_1], bx], [by, by], color=C_GOLD, lw=3, alpha=al*0.6, zorder=14)

        # C) Ejected Beta 2 (Left tracking)
        if t2_decayed:
            dy = -300 - cy
            if dy < 300:
                bx = abs_x[IDX_TARGET_2] - dy * 2.5
                by = -300
                al = max(0.0, 1.0 - dy/300.0)
                ax.scatter(bx, by, c=C_GOLD, s=90, alpha=al, zorder=15)
                ax.plot([abs_x[IDX_TARGET_2], bx], [by, by], color=C_GOLD, lw=3, alpha=al*0.6, zorder=14)

        # -----------------------------------------------
        # O(1) COLOR MATRIX ASSIGNMENT
        # -----------------------------------------------
        cols = np.empty(N_TOTAL, dtype=object)
        for n in range(N_TOTAL):
            t = N_TYPES[n]
            if t == 0: cols[n] = C_DARK
            elif t == 1: cols[n] = C_STEEL
            elif t == 2: cols[n] = C_DARK if t1_decayed else C_STEEL
            elif t == 3: cols[n] = C_DARK if t2_decayed else C_STEEL
            elif t == 4: cols[n] = C_STEEL if has_ghost else C_CYAN

        # -----------------------------------------------
        # CASING MODIFICATIONS
        # -----------------------------------------------
        halo_c = C_STEEL
        if is_fever: halo_c = C_MAGENTA
        elif is_half_fever: halo_c = C_CYAN
        elif t2_decayed: halo_c = C_GOLD
        
        # Solid Void Blanking Ring
        ax.add_patch(patches.Circle((0, cy), 195, facecolor=C_BG, alpha=0.9, zorder=4))
        ax.add_patch(patches.Circle((0, cy), 195, fill=False, edgecolor=halo_c, lw=5, zorder=5))

        if is_fever:
            pulse = (np.sin(phase_ratio * 40 * np.pi) + 1) * 2
            ax.add_patch(patches.Circle((0, cy), 205, fill=False, edgecolor=C_MAGENTA, lw=4+pulse, alpha=0.7, zorder=4))
        elif is_half_fever:
            ax.add_patch(patches.Circle((0, cy), 205, fill=False, edgecolor=C_CYAN, lw=3, alpha=0.5, zorder=4))

        # Core Particle Scatter (Vastly faster than patch looping)
        ax.scatter(abs_x, abs_y, c=cols, s=110, edgecolors=C_BG, lw=0.4, zorder=10)

    # 3. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-18d :: PLUTONIUM-239 BREEDER TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] O(1) TOPOLOGICAL TRANSMUTATION MACHINE", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)
    
    # Bottom Telemetry HUD
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)
    
    # State tracking mathematically resolved to central core
    if nearest_cy > 500: state_text = "U-238 // STABLE ISOTOPE (WAITING)"
    elif nearest_cy > 100: state_text = "U-239 // NEUTRON ABSORBED (INSTABILITY FEVER)"
    elif nearest_cy > -300: state_text = "Np-239 // POST BETA DECAY 1 (INTERMEDIATE)"
    else: state_text = "Pu-239 // POST BETA DECAY 2 (STABLE CORE)"
    
    bar_color = C_STEEL if nearest_cy > 500 else (C_MAGENTA if nearest_cy > 100 else (C_CYAN if nearest_cy > -300 else C_GOLD))
    
    ax.text(-500, -780, "KINEMATIC TARGET CYCLE IDENTIFIER:", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -820, state_text, color=bar_color, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    
    progress = abs(np.sin(phase_ratio * 10 * np.pi))
    ax.text(-500, -870, f"LOCAL GAUGE FLUX: {progress * 100:>05.2f} % Δ", color=C_TEXT, fontsize=12, fontname='monospace', weight='bold', zorder=82)
    
    # Absolute strict Tuple alignment [Y-Axis Locked]
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 4, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 4, facecolor=bar_color, zorder=83))

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
    print(f"LG-18d: PLUTONIUM BREEDER TENSOR [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
