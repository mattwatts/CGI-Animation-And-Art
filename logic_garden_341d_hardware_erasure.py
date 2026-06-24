"""
SOVEREIGN CODE: logic_garden_341d_hardware_erasure.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Vectorization
SCENE: Logic Garden 341d (Hardware Erasure // Space Shuttle Inheritance)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING, AEROSPACE ARCHITECTURE
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
OUT_DIR = "frames_341d_erasure"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Blueprint Grid Matrix
C_STEEL     = '#606065'   # Base Airframe Geometry
C_DARK      = '#202025'   # Hull Shading
C_GOLD      = '#FFB300'   # O(1) Orbital Payload Capacity
C_CYAN      = '#00FFFF'   # Edwards Telemetry / Sovereign Audit
C_MAGENTA   = '#FF0055'   # Parasitic Jet Engines / Dead Weight
C_MANTIS    = '#00FF00'   # Terminal Green / Optimization Locked

def draw_blueprint_grid(ax):
    """Draw the Structural Blueprint Matrix"""
    for i in range(-5, 6):
        ax.plot([i*100, i*100], [-960, 960], color=C_TITANIUM, lw=1, alpha=0.6, zorder=0)
    for j in range(-9, 10):
        ax.plot([-540, 540], [j*100, j*100], color=C_TITANIUM, lw=1, alpha=0.6, zorder=0)
    
    # Measurement reticles
    ax.add_patch(patches.Circle((0, 0), 400, fill=False, edgecolor=C_TITANIUM, lw=2, linestyle='--', alpha=0.5, zorder=1))
    ax.add_patch(patches.Circle((0, 0), 200, fill=False, edgecolor=C_TITANIUM, lw=2, linestyle='--', alpha=0.5, zorder=1))

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
    draw_blueprint_grid(ax)

    # ====================================================
    # 1. KINEMATIC TIMELINE THRESHOLDS
    # ====================================================
    T_SCAN_START = 6.0
    T_SCAN_END = 11.0
    T_ERASE_START = 12.0
    T_ERASE_END = 16.0
    
    # 2. BASE ORBITER GEOMETRY (Top-Down Blueprint)
    # ---------------------------------------------
    orbiter_pts = [
        [0, 550],               # Nose
        [60, 420], [120, 250],  # Forward Fuselage
        [320, -150],            # Wing Tip R
        [320, -350], [90, -350],# Trailing Edge R
        [60, -420], [-60, -420],# Aft Engine Bells
        [-90, -350], [-320, -350],# Trailing Edge L
        [-320, -150],           # Wing Tip L
        [-120, 250], [-60, 420] # Forward Fuselage L
    ]
    ax.add_patch(patches.Polygon(orbiter_pts, fill=False, edgecolor=C_STEEL, lw=4, zorder=10))
    ax.add_patch(patches.Polygon(orbiter_pts, facecolor=C_BG, alpha=0.8, edgecolor='none', zorder=9)) # Occlude grid
    
    # Centerline
    ax.plot([0, 0], [-420, 550], color=C_STEEL, lw=2, linestyle='-.', zorder=11)

    # ====================================================
    # 3. PARASITIC HARDWARE (MAGENTA) vs ERASURE
    # ====================================================
    # Jet engines, intake ducts, JP-4 fuel tanks embedded in wings/cargo bay
    parasitic_alpha = 1.0
    if t > T_ERASE_START:
        parasitic_alpha = max(0.0, 1.0 - ((t - T_ERASE_START) / (T_ERASE_END - T_ERASE_START)))

    if parasitic_alpha > 0:
        # Jet Engines (L/R Wings)
        ax.add_patch(patches.Rectangle((-240, -280), 80, 150, facecolor=C_BG, edgecolor=C_MAGENTA, lw=3, alpha=parasitic_alpha, zorder=15))
        ax.add_patch(patches.Rectangle((160, -280), 80, 150, facecolor=C_BG, edgecolor=C_MAGENTA, lw=3, alpha=parasitic_alpha, zorder=15))
        # Internal compressor blades (abstracted slots)
        for y_slice in range(-260, -140, 20):
            ax.plot([-240, -160], [y_slice, y_slice], color=C_MAGENTA, lw=2, alpha=parasitic_alpha, zorder=16)
            ax.plot([160, 240], [y_slice, y_slice], color=C_MAGENTA, lw=2, alpha=parasitic_alpha, zorder=16)

        # Intake Ducting & Fuel Lines snaking to the fuselage
        ax.plot([-200, -80], [-130, -50], color=C_MAGENTA, lw=6, linestyle='solid', alpha=parasitic_alpha, zorder=15)
        ax.plot([200, 80], [-130, -50], color=C_MAGENTA, lw=6, linestyle='solid', alpha=parasitic_alpha, zorder=15)

        # Aviation Fuel Tanks stealing payload length
        ax.add_patch(patches.Rectangle((-70, -100), 140, 150, facecolor=C_BG, edgecolor=C_MAGENTA, lw=4, hatch='///', alpha=parasitic_alpha, zorder=15))
        ax.text(0, -25, "ATMOSPHERIC\nFUEL PENALTY", color=C_MAGENTA, fontsize=10, fontname='monospace', weight='bold', ha='center', va='center', alpha=parasitic_alpha, zorder=16)

        # Spallation / Vaporization effect during erasure
        if t > T_ERASE_START:
            np.random.seed(int(t*80))
            n_parts = int(60 * parasitic_alpha)
            p_x = np.random.uniform(-300, 300, n_parts)
            p_y = np.random.uniform(-350, 100, n_parts)
            ax.scatter(p_x, p_y + (t-T_ERASE_START)*50, s=np.random.uniform(10, 40, n_parts), c=C_MAGENTA, edgecolors='none', alpha=parasitic_alpha, zorder=18)

    # ====================================================
    # 4. THE PAYLOAD EXPANSION (GOLD)
    # ====================================================
    # As the magenta hardware vanishes, the payload bay expands
    payload_y_min = 50
    if t > T_ERASE_START:
        expansion_prg = min(1.0, (t - T_ERASE_START) / (T_ERASE_END - T_ERASE_START))
        payload_y_min = 50 - (200 * expansion_prg) # Expands downward into the freed volume
    
    payload_h = 280 - payload_y_min
    pay_col = C_GOLD if t > T_ERASE_START else C_STEEL
    
    ax.add_patch(patches.Rectangle((-80, payload_y_min), 160, payload_h, facecolor=C_TITANIUM, edgecolor=pay_col, lw=5, zorder=12))
    
    # Payload Ribs
    rib_spacing = max(10, payload_h / 12)
    for ry in np.arange(payload_y_min + rib_spacing/2, 280, rib_spacing):
        ax.plot([-80, 80], [ry, ry], color=pay_col, lw=2, alpha=0.5, zorder=13)
        
    p_text = "ORBITAL PAYLOAD // O(1) CAPACITY SECURED" if t >= T_ERASE_END else "COMPROMISED CAPACITY"
    if t >= T_ERASE_END:
        ax.text(0, 100, "100%", color=C_GOLD, fontsize=32, fontname='monospace', weight='bold', ha='center', va='center', zorder=14)

    # ====================================================
    # 5. EDWARDS C_CYAN TELEMETRY SWEEP (THE AUDIT)
    # ====================================================
    if T_SCAN_START <= t <= T_SCAN_END:
        scan_prg = (t - T_SCAN_START) / (T_SCAN_END - T_SCAN_START)
        scan_y = 600 - (1050 * scan_prg)
        
        ax.plot([-540, 540], [scan_y, scan_y], color=C_CYAN, lw=6, zorder=25)
        ax.add_patch(patches.Rectangle((-540, scan_y), 1080, 150, facecolor=C_CYAN, alpha=0.2, zorder=24))
        
        # Intersection detection: highlighting magenta components as the scanner finds them
        if -300 < scan_y < 0:
            ax.add_patch(patches.Rectangle((-250, scan_y-20), 100, 40, facecolor='none', edgecolor=C_CYAN, lw=3, zorder=26))
            ax.add_patch(patches.Rectangle((150, scan_y-20), 100, 40, facecolor='none', edgecolor=C_CYAN, lw=3, zorder=26))

    # ====================================================
    # 6. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    # Top Header
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-341d :: O(1) HARDWARE ERASURE TENSOR", color=C_TEXT, fontsize=22, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] SPACE SHUTTLE PARASITIC MASS DELETION", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    # Bottom Telemetry HUD
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    # State Logic
    if t < T_SCAN_START:
        s1, c1 = "CORPORATE SCHEMA // THRUST REDUNDANCY ACTIVE", C_MAGENTA
        s2, c2 = "AWAITING EXPERIMENTAL AERODYNAMIC DATA", C_STEEL
    elif t < T_ERASE_START:
        s1, c1 = "EDWARDS KINEMATICS // UNPOWERED DESCENT PROVEN", C_CYAN
        s2, c2 = "JET ENGINES FLAGGED AS DEAD WEIGHT", C_MAGENTA
    elif t < T_ERASE_END:
        s1, c1 = "SERIALIZE RAZOR // DELETING PARASITIC MASS", C_GOLD
        s2, c2 = "EXPANDING ORBITAL PAYLOAD VOLUME", C_GOLD
    else:
        s1, c1 = "TATH\u0100T\u0100 // SPACE-FARING BEHEMOTH SECURED", C_MANTIS
        s2, c2 = "100% THRUST-TO-WEIGHT OPTIMIZATION", C_MANTIS

    ax.text(-500, -760, "SYS_01 [ARCHITECTURE]        :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, s1, color=c1, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [MASS PENALTY]        :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, s2, color=c2, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    p_cap = 65000 if t >= T_ERASE_END else 32000
    ax.text(-500, -840, "STRUCTURAL PAYLOAD CAPACITY  :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, f"{p_cap} LBS TO LEO", color=pay_col, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider [Strict Tuples]
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=c1, zorder=83))

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
    print(f"LG-341d: HARDWARE ERASURE TENSOR [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
