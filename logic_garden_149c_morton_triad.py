"""
SOVEREIGN CODE: logic_garden_149c_morton_triad_v2.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Vectorization
SCENE: Logic Garden 149c v2 (Bruce Morton's Triad // Accelerated Engine)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, NEUROBIOLOGY, KINEMATIC ENGINEERING
HOTFIX: Linear 20.0s Sequence. Dead-Space Eradicated. Tuples Sealed.
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
DURATION = 20.0  # Compressed from 24s. Vacuum eradicated.
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_149c_morton_v2"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Environment Matrix
C_STEEL     = '#606065'   # T1: Biological Hardware
C_DARK      = '#202025'   # Base Accents
C_GOLD      = '#FFB300'   # T2: Metabolic Energy
C_CYAN      = '#00FFFF'   # T3: Temporal Chronology 
C_MAGENTA   = '#FF0055'   # Uncoupled Spallation 
C_MANTIS    = '#00FF00'   # Consciousness (Survival Output)

def draw_industrial_grid(ax):
    """Draw the Structural Matrix"""
    for i in range(-5, 6):
        ax.plot([i*100, i*100], [-960, 960], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)
    for j in range(-9, 10):
        ax.plot([-540, 540], [j*100, j*100], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)

def draw_gear(ax, x, y, radius, teeth, face_color, edge_color, lw, rot_deg, zorder, alpha=1.0):
    """Draw standard industrial kinematic gear"""
    pts = []
    dr = radius * 0.15
    for i in range(teeth * 2):
        angle = np.radians(i * (360 / (teeth * 2)) + rot_deg)
        r = radius if i % 2 == 0 else radius - dr
        pts.append([x + r * np.cos(angle), y + r * np.sin(angle)])
    poly = patches.Polygon(pts, facecolor=face_color, edgecolor=edge_color, lw=lw, alpha=alpha, zorder=zorder)
    ax.add_patch(poly)

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

    # 1. ACCELERATED TIMING STATES
    T_ATP_ENGAGE = 1.5   # ATP floods reactor at 1.5s
    T_SYNC_ENGAGE = 8.0  # Sweep locks at 8.0s
    T_LOCK = 14.0        # Terminal Green at 14.0s

    # 2. THE HARDWARE BASE (BRUCE MORTON T1)
    CORE_X, CORE_Y = 0, 100
    
    # Structural Bed
    ax.add_patch(patches.RegularPolygon((CORE_X, CORE_Y), numVertices=8, radius=280, facecolor=C_TITANIUM, edgecolor=C_STEEL, lw=6, zorder=2))
    
    # Base Rotational Kinematics
    if t < T_ATP_ENGAGE:
        base_rot = t * 10 # Slow, biological baseline crawl
        state_code = "HARDWARE BASELINE ACTIVATED"
        c_state = C_STEEL
        c_core = C_DARK
    elif t < T_SYNC_ENGAGE:
        base_rot = (T_ATP_ENGAGE * 10) + (t - T_ATP_ENGAGE) * 70  # Chaotic overdrive
        state_code = "METABOLIC INGESTION (ATP) // ERRATIC"
        c_state = C_GOLD
        c_core = C_MAGENTA 
    else:
        # Synced rotation sequence
        rot_offset = (T_ATP_ENGAGE * 10) + ((T_SYNC_ENGAGE - T_ATP_ENGAGE) * 70)
        base_rot = rot_offset + (t - T_SYNC_ENGAGE) * 20
        state_code = "TEMPORAL COUPLING // CONSCIOUSNESS EMERGING"
        c_state = C_CYAN
        c_core = C_MANTIS if t > T_LOCK else C_CYAN

    # Main Biological Hardware Gear
    draw_gear(ax, CORE_X, CORE_Y, 240, 16, C_BG, C_STEEL, 4, base_rot, 3)
    ax.add_patch(patches.Circle((CORE_X, CORE_Y), 100, fill=False, edgecolor=C_STEEL, lw=4, zorder=4))

    # 3. METABOLIC ENERGY PIPELINE (BRUCE MORTON T2)
    FEED_X, FEED_Y = 300, 600
    ax.plot([FEED_X, CORE_X], [FEED_Y, CORE_Y], color=C_TITANIUM, lw=40, solid_capstyle='round', zorder=1)
    ax.add_patch(patches.Rectangle((FEED_X-50, FEED_Y-50), 100, 100, facecolor=C_BG, edgecolor=C_GOLD if t > T_ATP_ENGAGE else C_STEEL, lw=4, zorder=5))
    ax.text(FEED_X, FEED_Y+70, "ATP INTAKE", color=C_GOLD if t > T_ATP_ENGAGE else C_STEEL, fontsize=14, weight='bold', ha='center', fontname='monospace', zorder=6)

    ATP_SPEED = 400
    if t > T_ATP_ENGAGE: # Energy actively flowing
        for i in range(15):
            atp_offset = ((t - T_ATP_ENGAGE) * ATP_SPEED + i * 80) % 650
            if atp_offset < np.hypot(FEED_X - CORE_X, FEED_Y - CORE_Y):
                prg = atp_offset / np.hypot(FEED_X - CORE_X, FEED_Y - CORE_Y)
                px = FEED_X + (CORE_X - FEED_X) * prg
                py = FEED_Y + (CORE_Y - FEED_Y) * prg
                ax.add_patch(patches.RegularPolygon((px, py), numVertices=6, radius=12, facecolor=C_GOLD, edgecolor=C_BG, lw=1.5, zorder=7))

        # Thermal exhaust if poorly coupled
        if t < T_SYNC_ENGAGE:
            np.random.seed(int(t*10))
            ax.scatter(CORE_X + np.random.uniform(-150, 150, 20), CORE_Y + np.random.uniform(-150, 150, 20), s=np.random.uniform(10, 50, 20), c=C_MAGENTA, alpha=0.6, zorder=10)

    # 4. TEMPORAL CHRONOLOGY ENGINE (BRUCE MORTON T3)
    if t > T_SYNC_ENGAGE:
        sync_prg = t - T_SYNC_ENGAGE
        theta_sweep = np.radians(-sync_prg * 120)  # Clockwise rotation
        sw_x = CORE_X + 250 * np.sin(theta_sweep)
        sw_y = CORE_Y + 250 * np.cos(theta_sweep)
        
        ax.plot([CORE_X, sw_x], [CORE_Y, sw_y], color=C_CYAN, lw=8, zorder=15)
        ax.add_patch(patches.Wedge((CORE_X, CORE_Y), 250, np.degrees(theta_sweep), 90, facecolor=C_CYAN, alpha=0.15, zorder=14))
        
        # Chrono Locking Ring
        ax.add_patch(patches.Circle((CORE_X, CORE_Y), 250, fill=False, edgecolor=C_CYAN, lw=3, linestyle='--', zorder=15))
        ax.text(-350, 400, "TEMPORAL / CHRONOLOGICAL \nCOUPLING ENGAGED", color=C_CYAN, fontsize=12, weight='bold', fontname='monospace', zorder=16)

    # 5. THE TRIADIC OUTPUT 
    if t > T_LOCK:
        lock_prg = min(1.0, (t - T_LOCK) / 1.5)
        state_code = "TATH\u0100T\u0100 // CONSCIOUSNESS [SURVIVAL OP]"
        c_state = C_MANTIS
        c_core = C_MANTIS
        
        # When all three align, geometry hardens perfectly into the third state
        ax.add_patch(patches.RegularPolygon((CORE_X, CORE_Y), numVertices=3, radius=150 * lock_prg, facecolor='none', edgecolor=C_MANTIS, lw=8, transform=matplotlib.transforms.Affine2D().rotate_deg_around(CORE_X, CORE_Y, t*30) + ax.transData, zorder=20))
        ax.add_patch(patches.RegularPolygon((CORE_X, CORE_Y), numVertices=3, radius=150 * lock_prg, facecolor='none', edgecolor=C_MANTIS, lw=8, transform=matplotlib.transforms.Affine2D().rotate_deg_around(CORE_X, CORE_Y, -t*30) + ax.transData, zorder=20))
        
        ax.add_patch(patches.Circle((CORE_X, CORE_Y), 50 * lock_prg, facecolor=C_MANTIS, zorder=21))
    else:
        # Dormant / Erratic Core
        ax.add_patch(patches.Circle((CORE_X, CORE_Y), 30, facecolor=c_core, zorder=21))
        if t > T_ATP_ENGAGE and t < T_SYNC_ENGAGE:
            rad = 30 + 15 * np.sin(t*20)
            ax.add_patch(patches.Circle((CORE_X, CORE_Y), rad, fill=False, edgecolor=C_MAGENTA, lw=4, zorder=20))

    # ====================================================
    # 6. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    # Top Header [Strict Tuples]
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-149c :: MORTON TRIAD (CONSCIOUSNESS) TENSOR", color=C_TEXT, fontsize=21, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-0.75] O(1) THERMODYNAMIC SUBSTRATE INTEGRATION", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    # Bottom Telemetry HUD
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    t1_status = "INTACT"
    t2_status = "ACTIVE // DELIVERING FUEL" if t > T_ATP_ENGAGE else "SPOOLING"
    t3_status = "SYNCHRONIZED" if t > T_SYNC_ENGAGE else "UNBOUND"

    ax.text(-500, -760, "T1 [BIOLOGICAL HARDWARE]:", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(40, -760, t1_status, color=C_STEEL, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "T2 [METABOLIC FUEL/ATP] :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(40, -800, t2_status, color=C_GOLD if t > T_ATP_ENGAGE else C_STEEL, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "T3 [TEMPORAL COUPLING]  :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(40, -840, t3_status, color=C_CYAN if t > T_SYNC_ENGAGE else C_STEEL, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -680, "SYS OUTPUT :", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -680, state_code, color=c_state, fontsize=18, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider [Strict Tuples]
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=c_state, zorder=83))

    # Sovereign Execution Output
    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    plt.close('all')
    gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-149c v2: MORTON TRIADIC ENGINE [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
