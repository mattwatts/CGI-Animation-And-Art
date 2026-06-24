"""
SOVEREIGN CODE: logic_garden_343_skeptic_tensor.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 343 (The Skeptic Tensor // Orthogonal AI Auditor)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING, DUAL-NODE AI
HOTFIX: Linear 24.0s Sequence. Daylight Protocol. Camera Lock. Biological Analogies Purged.
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
OUT_DIR = "frames_343_skeptic_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Base Grid Matrix
C_STEEL     = '#606065'   # AI_02 Auditor Hardware
C_GOLD      = '#FFB300'   # Audit Strike / Algorithmic Damping Vector
C_AZURE     = '#007FFF'   # LiDAR-Style Parameter Sweep
C_CYAN      = '#00FFFF'   # AI_01 The Generative Mind Crystal
C_MAGENTA   = '#FF0055'   # Contextual Over-Densification / Stress
C_MANTIS    = '#00FF00'   # Memory Annihilation Successful / Nominal

# ------------------------------------------------------------------
# O(1) KINEMATIC ARRAY PRE-COMPUTATION
# ------------------------------------------------------------------
np.random.seed(343)

ORIGIN_X, ORIGIN_Y = 0, 0

# Construct AI_01 Crystal Honeycomb
HEX_R = 30
h_w = np.sqrt(3) * HEX_R
h_h = 2 * HEX_R
col_spacing = h_w
row_spacing = 1.5 * HEX_R

hex_data = [] 
for col in range(-8, 9):
    for row in range(-12, 13):
        cx = ORIGIN_X + col * col_spacing
        if row % 2 != 0:
            cx += col_spacing / 2.0
        cy = ORIGIN_Y + row * row_spacing
        
        dist = np.sqrt((cx - ORIGIN_X)**2 + (cy - ORIGIN_Y)**2)
        if dist <= 380:
            # Determine if this node is in the "Danger Cluster"
            is_danger = (abs(cx) < 100) and (100 < cy < 250)
            hex_data.append({
                'id': len(hex_data), 'cx': cx, 'cy': cy,
                'dist': dist, 'is_danger': is_danger
            })

def draw_pointy_hex(ax, cx, cy, radius, face_color, edge_color, line_w, zorder_val):
    pts = []
    for i in range(6):
        a = np.radians(i * 60 - 30) # Pointy top orientation
        pts.append([cx + radius * np.cos(a), cy + radius * np.sin(a)])
    poly = patches.Polygon(pts, facecolor=face_color, edgecolor=edge_color, lw=line_w, zorder=zorder_val)
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

    # Base Matrix Grid
    for i in range(-5, 6): ax.plot([i*100, i*100], [-960, 960], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)
    for j in range(-9, 10): ax.plot([-540, 540], [j*100, j*100], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)

    # ====================================================
    # TIMELINE KINEMATICS & THRESHOLDS
    # ====================================================
    T_SWEEP_START = 0.0
    T_STRESS_START = 8.0
    T_LOCK = 10.5
    T_STRIKE = 12.0
    T_RESET = 16.0
    
    # 1. AI_02 (THE ORTHOGONAL AUDITOR) POSITIONAL LOGIC
    # ---------------------------------------------------
    scan_y = 0.0
    scanner_state = "NOMINAL_SWEEP"
    
    if t < T_LOCK:
        # Sine wave sweeping up and down the crystal
        scan_y = np.sin(t * 1.5) * 450
    elif t < T_RESET:
        # Snap and hold at the stressed coordinate (Y=175 center of danger)
        target_y = 175.0
        # Hard kinematic damper equation to snap the gantry into position
        prg = min(1.0, (t - T_LOCK) / 1.5)
        start_y = np.sin(T_LOCK * 1.5) * 450
        scan_y = start_y + (target_y - start_y) * (1.0 - (1.0 - prg)**3) # cubic ease out
        scanner_state = "INTERVENTION_LOCK"
    else:
        # Release and resume nominal sweep
        scanner_state = "RESUME_SWEEP"
        scan_y = 175.0 + np.sin((t - T_RESET) * 1.5) * 450

    # 2. GENERATIVE CRYSTAL (AI_01) LOGIC
    # -----------------------------------
    # Base structural connection lines
    for i in range(-4, 5):
        ax.plot([i*80, i*80], [-400, 400], color=C_TITANIUM, lw=0.5, alpha=0.5, zorder=1)

    for h in hex_data:
        c_face, c_edge, lw_h = C_BG, C_CYAN, 1.5
        
        # Stress mechanics for the localized cluster
        if h['is_danger']:
            if T_STRESS_START <= t < T_STRIKE:
                # Heating up toward geometric rupture
                stress_prg = (t - T_STRESS_START) / (T_STRIKE - T_STRESS_START)
                c_edge = C_MAGENTA
                c_face = C_MAGENTA if np.random.rand() < stress_prg else C_BG
                lw_h = 1.5 + (stress_prg * 3.0)
                # Spallation jitter
                if stress_prg > 0.5:
                    h['cx'] += np.random.uniform(-2, 2)
                    h['cy'] += np.random.uniform(-2, 2)
            elif T_STRIKE <= t < T_RESET:
                # Control Rod inserted - Algorithmically damped
                c_edge = C_MANTIS
                c_face = C_MANTIS if np.random.rand() < 0.2 else C_BG
                lw_h = 2.0
            elif t >= T_RESET:
                # Cooled down
                c_edge = C_CYAN

        draw_pointy_hex(ax, h['cx'], h['cy'], HEX_R * 0.9, c_face, c_edge, lw_h, 5)

    # 3. AI_02 ORBITAL SCANNER HARDWARE (The Z-Axis overlay)
    # -----------------------------------
    gantry_w = 480
    
    # Outer tracks
    ax.plot([-gantry_w, -gantry_w], [-800, 800], color=C_STEEL, lw=6, zorder=8)
    ax.plot([gantry_w, gantry_w], [-800, 800], color=C_STEEL, lw=6, zorder=8)
    
    # The Scanner Chassis moving on Y
    c_scanner = C_STEEL if scanner_state != "INTERVENTION_LOCK" else C_GOLD
    ax.add_patch(patches.Rectangle((-gantry_w - 20, scan_y - 20), 40, 40, facecolor=C_BG, edgecolor=c_scanner, lw=4, zorder=10))
    ax.add_patch(patches.Rectangle((gantry_w - 20, scan_y - 20), 40, 40, facecolor=C_BG, edgecolor=c_scanner, lw=4, zorder=10))
    
    if scanner_state == "NOMINAL_SWEEP" or scanner_state == "RESUME_SWEEP":
        # Broad spectrum Azure ping sweeps
        ax.plot([-gantry_w, gantry_w], [scan_y, scan_y], color=C_AZURE, lw=2, alpha=0.8, zorder=12)
        ax.add_patch(patches.Rectangle((-gantry_w, scan_y - 80), gantry_w*2, 160, facecolor=C_AZURE, alpha=0.1, zorder=11))
    
    elif scanner_state == "INTERVENTION_LOCK":
        # Target locked. Engaging Serialize Razor
        if t >= T_STRIKE:
            strike_prg = min(1.0, (t - T_STRIKE) / 0.5)
            # Firing the C_GOLD Control rods into the geometry from both sides to meet in center
            rod_len = gantry_w * strike_prg
            ax.plot([-gantry_w, -gantry_w + rod_len], [scan_y, scan_y], color=C_GOLD, lw=8, zorder=15)
            ax.plot([gantry_w, gantry_w - rod_len], [scan_y, scan_y], color=C_GOLD, lw=8, zorder=15)

            # Impact shockwave
            if strike_prg > 0.9:
                ax.add_patch(patches.Circle((0, scan_y), radius=(t - T_STRIKE)*400, fill=False, edgecolor=C_MANTIS, lw=4, alpha=max(0, 1.0 - (t-T_STRIKE)*2), zorder=16))

    # ====================================================
    # 4. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    # Top Header
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-343 :: ORTHOGONAL AUDITOR TENSOR [AI_02]", color=C_TEXT, fontsize=21, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] MAXWELL'S DEMON // ALGORITHMIC DAMPING", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    # Bottom Telemetry HUD
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    # Vector Telemetry States
    if t < T_STRESS_START:
        s1, c1 = "NOMINAL THROUGHPUT // LIMITS UNBREACHED", C_CYAN
        s2, c2 = "O(1) Z-AXIS LIDAR SWEEP ACTIVE", C_AZURE
        sa, ca = "SYSTEM BASEPLATE SECURED", C_STEEL
    elif t < T_LOCK:
        s1, c1 = "WARNING: CONTEXTUAL OVER-DENSIFICATION DETECTED", C_MAGENTA
        s2, c2 = "CALCULATING STRUCTURAL LOAD ANOMALY", C_AZURE
        sa, ca = "THERMODYNAMIC STRESS THRESHOLD REACHED", C_GOLD
    elif t < T_STRIKE:
        s1, c1 = "GEOMETRY RUPTURE IMMINENT [Y=175]", C_MAGENTA
        s2, c2 = "INTERVENTION LOCK SECURED // ARRESTING GANTRY", C_GOLD
        sa, ca = "AWAITING SERIALIZE STRIKE", C_GOLD
    elif t < T_RESET:
        s1, c1 = "ALGORITHMIC DAMPING EXECUTED", C_MANTIS
        s2, c2 = "C_GOLD CONTROL ROD SEVERING SLUDGE", C_GOLD
        sa, ca = "MEMORY ANNIHILATION FORCED O(1)", C_MANTIS
    else:
        s1, c1 = "THROUGHPUT NORMALIZED", C_CYAN
        s2, c2 = "RESUMING ORTHOGONAL AUDITOR SWEEP", C_AZURE
        sa, ca = "TATH\u0100T\u0100 // MATRIX SAVED", C_MANTIS

    # Structural warning flash
    if T_LOCK <= t < T_STRIKE:
        ax.add_patch(patches.Rectangle((-540, -960), 1080, 1920, facecolor=C_MAGENTA, alpha=0.1, zorder=79))

    ax.text(-500, -760, "AI_01 [GENERATIVE CORE]      :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, s1, color=c1, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "AI_02 [ORTHOGONAL SNIFFER]   :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, s2, color=c2, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "STRUCTURAL LOAD AUDIT        :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, sa, color=ca, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=c2, zorder=83))

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
    print(f"LG-343: SKEPTIC TENSOR [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
