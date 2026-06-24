"""
SOVEREIGN CODE: logic_garden_321e_threebody_tensor.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 321e (Three-Body Recombination Tensor)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: OOM Cascade Purged via Absolute Worker Annihilation (maxtasksperchild=1).
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
OUT_DIR = "frames_321e_threebody_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Upper Continuum Scaffold
C_STEEL     = '#606065'   # Structural Rails
C_DARK      = '#202025'   # Ion Core Scaffold
C_CYAN      = '#00FFFF'   # Free Electron
C_BOUND     = '#0066FF'   # Captured State Payload
C_TRANSFER  = '#FF0055'   # 3-Body Momentum Bridge (Magenta)
C_KINETIC   = '#FF4400'   # High-Velocity Exit Spallation (Orange)
C_WHITE     = '#FFFFFF'

# ------------------------------------------------------------------
# O(1) KINEMATIC GEOMETRY
# ------------------------------------------------------------------
def draw_carrier(ax, x, y, base_color, alpha=1.0):
    for r, c, a in [(24, C_TEXT, alpha), (20, base_color, alpha), (8, C_WHITE, alpha*0.9)]:
        pts = np.array([[0, -r], [r, 0], [0, r], [-r, 0]])
        ax.add_patch(patches.Polygon(pts + [x, y], facecolor=c, zorder=10))

def draw_velocity_chevron(ax, x, y, scale, alpha):
    w = 30 * scale
    h = 40 * scale
    pts = np.array([[0, -h], [w, 0], [0, -h/2], [-w, 0]])
    ax.add_patch(patches.Polygon(pts + [x, y], facecolor=C_KINETIC, alpha=alpha, zorder=9))

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

    # 1. THE STRUCTURAL LATTICE & ION CORE
    for gy in range(-900, 1000, 150):
        ax.axhline(gy, color=C_STEEL, lw=1, alpha=0.15, zorder=0)

    ax.add_patch(patches.Rectangle((-540, 400), 1080, 560, facecolor=C_TITANIUM, alpha=0.15, zorder=1))
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 660, facecolor=C_DARK, alpha=0.10, zorder=1))
    
    ax.add_patch(patches.Rectangle((-260, 80), 520, 40, facecolor=C_TITANIUM, zorder=2))
    ax.axhline(100, color=C_STEEL, lw=2.5, linestyle='--', zorder=2.1)
    
    TRK_L = -180  
    TRK_R = 180   
    
    ax.plot([TRK_L, TRK_L], [100, 960], color=C_STEEL, lw=2, alpha=0.4, zorder=1.1)
    ax.plot([TRK_R, TRK_R], [100, 960], color=C_STEEL, lw=2, alpha=0.4, zorder=1.1)
    ax.plot([TRK_L, TRK_L], [-960, 100], color=C_STEEL, lw=2, alpha=0.2, zorder=1.1)
    
    core_pts = np.array([[-60, 40], [60, 40], [40, -120], [-40, -120]])
    ax.add_patch(patches.Polygon(core_pts + [TRK_L, -300], facecolor=C_DARK, edgecolor=C_TEXT, lw=3, zorder=4))

    # 2. THREE-BODY KINEMATICS ENGINE
    N_EVENTS = 3
    for i in range(N_EVENTS):
        t = (phase_ratio + i / float(N_EVENTS)) % 1.0
        
        a_m = 1.0
        if t < 0.05: a_m = t / 0.05
        if t > 0.95: a_m = (1.0 - t) / 0.05

        if t < 0.40:
            drop_p = t / 0.40
            y_free = 800 - (drop_p * 700) 
            draw_carrier(ax, TRK_L, y_free, C_CYAN, a_m)
            draw_carrier(ax, TRK_R, y_free, C_CYAN, a_m)

        if 0.395 < t < 0.430:
            bridge_p = 1.0 - abs(t - 0.4125) / 0.0175
            bridge_w = 340 * bridge_p
            ax.add_patch(patches.Rectangle((-(bridge_w/2), 90), bridge_w, 20, facecolor=C_TRANSFER, zorder=5))
            ax.plot([-(bridge_w/2), bridge_w/2], [100, 100], color=C_WHITE, lw=4, zorder=5.1)
            ax.add_patch(patches.Circle((TRK_L, 100), radius=50*bridge_p, color=C_TRANSFER, alpha=bridge_p, zorder=6))
            ax.add_patch(patches.Circle((TRK_R, 100), radius=80*bridge_p, color=C_TRANSFER, alpha=bridge_p, zorder=6))

        if 0.40 <= t < 0.70:
            sep_p = (t - 0.40) / 0.30
            y_e1 = 100 - (sep_p ** 0.8) * 400
            draw_carrier(ax, TRK_L, y_e1, C_BOUND, a_m)
            
            y_e2 = 100 + (sep_p ** 2.0) * 1100
            a_spall = max(0.0, 1.0 - (sep_p * 1.2)) * a_m
            draw_velocity_chevron(ax, TRK_R, y_e2 - 60, 1.0, a_spall)
            draw_velocity_chevron(ax, TRK_R, y_e2 - 120, 0.8, a_spall * 0.8)
            draw_velocity_chevron(ax, TRK_R, y_e2 - 180, 0.5, a_spall * 0.5)
            
            draw_carrier(ax, TRK_R, y_e2, C_KINETIC if sep_p < 0.5 else C_CYAN, a_m)

        if t >= 0.70:
            draw_carrier(ax, TRK_L, -300, C_BOUND, a_m)

    # 3. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    ax.text(-500, 880, "LG-321e :: THREE-BODY RECOMBINATION", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, 840, "[SFI-1.00] ASYMMETRIC MOMENTUM VECTORING // PLASMA DENSITY", color=C_STEEL, fontsize=12, fontname='monospace', zorder=80)
    
    ax.add_patch(patches.Rectangle((-520, -920), 1040, 140, facecolor=C_TITANIUM, alpha=0.9, zorder=79))
    ax.text(-500, -825, "KINETIC CARRIER EXCITATION: E_k2 = E_g + E_k1(init) + E_k2(init)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=80)
    
    pulse = abs(np.sin(phase_ratio * 3 * np.pi))
    ax.text(-500, -855, f"LOCAL PLASMA DENSITY TARGET: {pulse * 10:>05.2f} e-/cm³x10¹⁹ [CRITICAL]", color=C_TRANSFER if pulse > 0.5 else C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=80)
    
    ax.add_patch(patches.Rectangle((-500, -880), 1000, 4, facecolor=C_STEEL, zorder=80))
    ax.add_patch(patches.Rectangle((-500, -880), 1000 * pulse, 4, facecolor=C_TRANSFER, zorder=81))

    ax.text(-470, 200, "EXCESS KINETIC\nVECTOR SHUNT", color=C_KINETIC, fontsize=10, fontname='monospace', weight='bold', ha='right', zorder=80)
    ax.plot([-360, -180], [180, 180], color=C_STEEL, lw=2, linestyle=':', zorder=80)
    ax.text(-180, -380, "ION CORE (n_g)\nSTABILIZED", color=C_BOUND, fontsize=10, fontname='monospace', weight='bold', ha='center', zorder=80)

    # Force hard garbage collection before exiting the function
    plt.close('all'); gc.collect()
    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    # Reserve 1 core for the OS to guarantee terminal responsiveness
    cpu_cores = max(1, mp.cpu_count() - 1) 
    print(f"LG-321e: THREE-BODY RECOMBINATION [CORES: {cpu_cores}] [MEMORY LOCK ACTIVE]")
    
    # HOTFIX: maxtasksperchild=1 mathematically enforces OS-level memory reclaiming per frame.
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
