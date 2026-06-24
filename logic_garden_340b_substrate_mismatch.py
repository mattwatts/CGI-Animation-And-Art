"""
SOVEREIGN CODE: logic_garden_340b_substrate_mismatch.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Vectorization
SCENE: Logic Garden 340b (Framework Overlay // Substrate Mismatch)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING, COGNITIVE LOGIC
HOTFIX: Linear 24.0s Sequence. Daylight Protocol. Absolute Camera Lock. Tuples Sealed.
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
DURATION = 24.0  
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_340b_substrate"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Environment Matrix
C_STEEL     = '#606065'   # Base infrastructure
C_DARK      = '#202025'   # Corporate Press Body
C_CYAN      = '#00FFFF'   # The Academic Baseplate (Jagged/Specialized)
C_GOLD      = '#FFB300'   # Corporate Schema (MBA Standardized Overlay)
C_MAGENTA   = '#FF0055'   # Systemic Friction / Mismatch Error
C_MANTIS    = '#00FF00'   # Terminal Green 

def draw_industrial_grid(ax):
    """Draw the Structural Matrix"""
    for i in range(-5, 6):
        ax.plot([i*100, i*100], [-960, 960], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)
    for j in range(-9, 10):
        ax.plot([-540, 540], [j*100, j*100], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)

# PRECOMPUTE ACADEMIC BASEPLATE (JAGGED, ASYMMETRICAL TOPOLOGY)
# Complex X, Y coordinates representing diverse, uneven academic specializations
ACAD_X = [-540, -420, -310, -200, -80, 50, 210, 310, 420, 540]
ACAD_Y = [-300, 180, -20, -100, 250, 40, -150, 190, 80, -300]

def render_frame(packet):
    f, phase_ratio = packet
    t = phase_ratio * DURATION 
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    
    # BARE-METAL CAMERA LOCK
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)
    ax.autoscale(False)
    draw_industrial_grid(ax)

    # 1. RENDER ACADEMIC BASEPLATE (The Ground Truth)
    pts = [[-540, -720]]
    for x, y in zip(ACAD_X, ACAD_Y):
        pts.append([x, y])
    pts.append([540, -720])
    
    # Solid geometric foundation
    ax.add_patch(patches.Polygon(pts, facecolor=C_TITANIUM, edgecolor=C_CYAN, lw=5, zorder=5))
    
    # Internal structural bracing for academic density
    for i in range(1, len(ACAD_X)-1):
        ax.plot([ACAD_X[i], ACAD_X[i]], [ACAD_Y[i], -720], color=C_CYAN, lw=2, linestyle='--', alpha=0.6, zorder=4)
        ax.scatter(ACAD_X[i], ACAD_Y[i], s=100, c=C_BG, edgecolors=C_CYAN, lw=3, zorder=6)

    # 2. THE CORPORATE SCHEMA (Descending Industrial Press)
    # Uniform, zero-friction expectation, 100px wide standardized slots
    T_COLLIDE = 7.5
    PRESS_START_Y = 800
    PRESS_END_Y = 320 # Hand-calculated collision point with highest peak (Y=250)
    
    if t < T_COLLIDE:
        prg = t / T_COLLIDE
        y_curr = PRESS_START_Y - (PRESS_START_Y - PRESS_END_Y) * prg
        press_c = C_GOLD
        press_jitter_x, press_jitter_y = 0, 0
    else:
        # Pinned under friction. Jitter applied to simulate extreme thermodynamic stress.
        y_curr = PRESS_END_Y
        press_c = C_MAGENTA if (t*10)%2 < 1 else C_GOLD # Flashing error state
        np.random.seed(int(t*60))
        press_jitter_y = np.random.uniform(-4, 4)
        press_jitter_x = np.random.uniform(-3, 3)

    y_base = y_curr + press_jitter_y
    x_offset = press_jitter_x

    # Constructing the standardized uniform schema
    c_pts = [[-540, y_base+400], [-540, y_base]]
    
    # Uniform standardized "Throughput Slots"
    for cx in range(-500, 500, 120):
        c_pts.append([cx + x_offset, y_base])
        c_pts.append([cx + x_offset, y_base - 70])
        c_pts.append([cx + 80 + x_offset, y_base - 70])
        c_pts.append([cx + 80 + x_offset, y_base])
        
    c_pts.append([540, y_base])
    c_pts.append([540, y_base+400])

    ax.add_patch(patches.Polygon(c_pts, facecolor=C_DARK, edgecolor=press_c, lw=6, zorder=10))

    # Add logical tracking nodes inside the schema block
    for cx in [-400, -160, 80, 320]:
        ax.add_patch(patches.Circle((cx + x_offset, y_base + 100), 20, facecolor=press_c, zorder=11))
        ax.plot([cx + x_offset, cx + x_offset], [y_base + 100, y_base + 300], color=press_c, lw=3, linestyle='-', zorder=11)

    # 3. KINEMATIC COLLISION & SPALLATION
    # Detect exact strike points:
    # Highest academic peak is at X=-80, Y=250
    # Next highest is at X=310, Y=190, X=-420, Y=180
    
    if t >= T_COLLIDE:
        # Thermodynamic Spallation logic
        n_sparks = 40
        np.random.seed(int(t*100))
        
        # Site 1: Absolute highest peak
        s1_x = -80 + np.random.normal(0, 15, n_sparks)
        s1_y = 250 + np.random.normal(0, 5, n_sparks)
        sx_vel = np.random.uniform(-1, 1, n_sparks) * 200
        sy_vel = -np.abs(np.random.uniform(0, 1, n_sparks)) * 150 # Blow downward off the press
        ax.scatter(s1_x + sx_vel*0.1, s1_y + sy_vel*0.1, s=np.random.uniform(10, 50, n_sparks), c=C_MAGENTA, edgecolors='none', alpha=0.8, zorder=15)
        
        # Site 2: Secondary impacts
        s2_x = 310 + np.random.normal(0, 10, n_sparks//2)
        s2_y = 190 + np.random.normal(0, 5, n_sparks//2)
        sx2_vel = np.random.uniform(-1, 1, n_sparks//2) * 150
        sy2_vel = -np.abs(np.random.uniform(0, 1, n_sparks//2)) * 100
        ax.scatter(s2_x + sx2_vel*0.1, s2_y + sy2_vel*0.1, s=np.random.uniform(10, 40, n_sparks//2), c=C_MAGENTA, edgecolors='none', alpha=0.7, zorder=15)

        # Draw intense structural strain vectors traversing the corporate block
        strain_alpha = 0.4 + 0.4 * np.sin(t*20)
        ax.plot([-80+press_jitter_x, -200], [250+press_jitter_y, 450], color=C_MAGENTA, lw=4, alpha=strain_alpha, linestyle='-.', zorder=12)
        ax.plot([-80+press_jitter_x, 100], [250+press_jitter_y, 400], color=C_MAGENTA, lw=4, alpha=strain_alpha, linestyle='-.', zorder=12)

    # 4. HUD DESCRIPTORS
    if t < T_COLLIDE:
        stat_schema = "EXECUTING UNIFORM ALIGNMENT"
        stat_parity = "WAITING ON INTERSECTION"
        stat_c = C_GOLD
        stat_p = C_STEEL
        hud_output = "THROUGHPUT: O(1) EXPECTED"
    else:
        stat_schema = "CATASTROPHIC STALL // RUPTURE"
        stat_parity = f"{0.00:>04.2f}% [SUBSTRATE INCOMPATIBLE]"
        stat_c = C_MAGENTA
        stat_p = C_MAGENTA
        hud_output = "THROUGHPUT: 0.00kN [SYSTEM LOCKED]"

    # ====================================================
    # 5. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    # Top Header [Strict Tuples]
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-340b :: OVERLAY TENSOR / SUBSTRATE MISMATCH", color=C_TEXT, fontsize=22, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] CORPORATE SCHEMA VS ACADEMIC BASEPLATE", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    # Bottom Telemetry HUD
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    ax.text(-500, -760, "SYS_01 [ACADEMIC MATRIX]     :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, "JAGGED TOPOLOGY // HIGHLY SPECIALIZED", color=C_CYAN, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [CORPORATE OVERLAY]   :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, stat_schema, color=stat_c, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "PARITY / THROUGHPUT          :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, hud_output, color=stat_p, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider [Strict Tuples]
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=stat_c, zorder=83))

    # Sovereign Execution Output
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
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-340b: SUBSTRATE MISMATCH TENSOR [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
