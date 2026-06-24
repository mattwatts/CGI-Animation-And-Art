"""
SOVEREIGN CODE: logic_garden_342_mind_crystal.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 342 (The Mind Crystal // Pareto Frontier Rupture)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, COGNITIVE LOGIC, KINEMATIC ENGINEERING
HOTFIX: Linear 24.0s Sequence. Daylight Protocol. Mathtext fixed. Local scope 'ey' sealed.
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
OUT_DIR = "frames_342_mind_crystal"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Base Grid Matrix
C_STEEL     = '#606065'   # Structural Hardware
C_GOLD      = '#FFB300'   # O(1) Probe Vectors / Context Sludge
C_CYAN      = '#00FFFF'   # The Pareto Frontier (Mind Crystal)
C_MAGENTA   = '#FF0055'   # Semantic Exhaust / System Collapse
C_MANTIS    = '#00FF00'   # Tracked Coordinate / Successfully Locked 

# ------------------------------------------------------------------
# O(1) KINEMATIC ARRAY PRE-COMPUTATION (DETERMINISTIC TIMELINE)
# ------------------------------------------------------------------
np.random.seed(342)

# Origin point for prompts
ORIGIN_X, ORIGIN_Y = 0, -450

# Constructing the Mind Crystal (Hexagonal Pareto Arc)
HEX_R = 25
h_y_offset = HEX_R * np.sqrt(3)

hex_data = [] # Stores cx, cy, layer, angle, and kinematic states
for layer in range(5):
    for i in range(-12, 13):
        angle_deg = i * 6 + 90
        theta = np.radians(angle_deg)
        r = 400 + (layer * h_y_offset)
        
        # Jitter the arc slightly for an organic crystal edge variation
        r += np.sin(i * 1.5) * 5.0
        
        cx = ORIGIN_X + r * np.cos(theta)
        cy = ORIGIN_Y + r * np.sin(theta)
        
        # Rupture physics parameters
        vx = np.cos(theta) * np.random.uniform(200, 500) * (1.0 - layer*0.1)
        vy = np.sin(theta) * np.random.uniform(200, 500) * (1.0 - layer*0.1)
        v_rot = np.random.uniform(-180, 180)
        
        hex_data.append({
            'id': len(hex_data), 'cx': cx, 'cy': cy, 'layer': layer, 
            'theta': theta, 'vx': vx, 'vy': vy, 'v_rot': v_rot,
            'state_locked': False
        })

# Phase 1: MCMC Executioner Probes
probe_targets = [h for h in hex_data if h['layer'] == 0]
np.random.shuffle(probe_targets)
active_probes = []
for sec in range(1, 8):
    if sec < len(probe_targets):
        target = probe_targets[sec]
        active_probes.append({'start_t': sec - 0.2, 'end_t': sec + 0.8, 'target': target})

def draw_hex(ax, h, t):
    """Draws a single rigid hexagonal tile with state shading"""
    T_RUPTURE = 16.0
    
    cx, cy = h['cx'], h['cy']
    rot = 0
    c_line = C_CYAN
    fade_alpha = 0.8 - (h['layer'] * 0.15)
    
    if h['state_locked']:
        c_line = C_MANTIS
        fade_alpha = 1.0

    # Shatter Geometry Logic
    if t >= T_RUPTURE:
        dt = t - T_RUPTURE
        # Center hexes blow out instantly. Edge hexes delay slightly simulating structural tear.
        tear_delay = abs(np.degrees(h['theta']) - 90) * 0.015
        if dt > tear_delay:
            active_dt = dt - tear_delay
            cx += h['vx'] * active_dt
            cy += h['vy'] * active_dt - (0.5 * 800 * active_dt**2) # Gravity capture on fragments
            rot = h['v_rot'] * active_dt
            c_line = C_MAGENTA
            fade_alpha = max(0, fade_alpha - active_dt * 0.5)
            
    if fade_alpha <= 0: return # Cinematic culling
            
    # Calculate Hexagon Points
    pts = []
    for i in range(6):
        a = np.radians(i * 60 + rot + 30)
        pts.append([cx + HEX_R * np.cos(a), cy + HEX_R * np.sin(a)])
    
    poly = patches.Polygon(pts, facecolor=C_BG, edgecolor=c_line, lw=1.5, alpha=fade_alpha, zorder=10 + h['layer'])
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

    # 1. RENDER PHASE 1 PROBES (O(1) Memory Annihilation Vectors)
    for p in active_probes:
        if p['start_t'] <= t <= p['end_t']:
            tgt = p['target']
            prg = (t - p['start_t']) / (p['end_t'] - p['start_t'])
            # Shoot up constraints
            if prg < 0.5:
                # Extending
                ex = ORIGIN_X + (tgt['cx'] - ORIGIN_X) * (prg * 2.0)
                ey = ORIGIN_Y + (tgt['cy'] - ORIGIN_Y) * (prg * 2.0)
                ax.plot([ORIGIN_X, ex], [ORIGIN_Y, ey], color=C_GOLD, lw=4, zorder=5)
            else:
                # Retracting / Erasing memory footprint
                tgt['state_locked'] = True
                eprg = (prg - 0.5) * 2.0
                ex = ORIGIN_X + (tgt['cx'] - ORIGIN_X) * eprg
                # SOVEREIGN FIX: 'ey' explicitly instantiated to prevent local scope rupture
                ey = ORIGIN_Y + (tgt['cy'] - ORIGIN_Y) * eprg  
                ax.plot([ex, tgt['cx']], [ey, tgt['cy']], color=C_MANTIS, lw=2, alpha=1.0-eprg, zorder=5)
                # Success flash
                ax.add_patch(patches.Circle((tgt['cx'], tgt['cy']), 35 * eprg, facecolor='none', edgecolor=C_MANTIS, alpha=1.0-eprg, lw=2, zorder=15))

    # 2. RENDER PHASE 2 & 3: CONTEXT SLUDGE (The Overload)
    T_SLUDGE_START = 8.0
    T_RUPTURE = 16.0
    
    if t > T_SLUDGE_START:
        s_prg = min(1.0, (t - T_SLUDGE_START) / (T_RUPTURE - T_SLUDGE_START))
        block_y = ORIGIN_Y + (s_prg * 380) # Rises perfectly up to hit the R=400 crystal boundary
        
        # Heavy overlapping parameter arrays pushing up
        b_wid = 300
        b_pts = [[-b_wid/2, ORIGIN_Y], [-b_wid/2, block_y], [b_wid/2, block_y], [b_wid/2, ORIGIN_Y]]
        c_block = C_GOLD if t < T_RUPTURE else C_MAGENTA
        
        ax.add_patch(patches.Polygon(b_pts, facecolor=C_TITANIUM, edgecolor=c_block, lw=4, alpha=0.6, zorder=4))
        
        # Internal density (representing unmanaged variables)
        for vx in np.linspace(-b_wid/2+10, b_wid/2-10, 12):
            ax.plot([vx, vx], [ORIGIN_Y, block_y], color=c_block, lw=1, alpha=0.5, linestyle='-.', zorder=4.1)

        if t > T_RUPTURE:
            # The sludge block penetrates completely, blowing out the top
            pen_prg = (t - T_RUPTURE) / (DURATION - T_RUPTURE)
            ax.add_patch(patches.Polygon(b_pts, facecolor=C_BG, edgecolor=C_MAGENTA, lw=6, zorder=8))
            ax.plot([-b_wid/2, b_wid/2], [block_y + pen_prg*800, block_y + pen_prg*800], color=C_MAGENTA, lw=8, zorder=9)
            
            # Semantic Exhaust (Spallation sparks)
            np.random.seed(int(t*100))
            for _ in range(40):
                spx = np.random.uniform(-b_wid/2-50, b_wid/2+50)
                spy = block_y + (pen_prg*800) + np.random.uniform(-50, -200)
                ax.scatter(spx, spy, s=np.random.uniform(10, 40), c=C_MAGENTA, alpha=0.8, edgecolors='none', zorder=16)

    # 3. RENDER THE MIND CRYSTAL PARETO FRONTIER
    for h in hex_data:
        draw_hex(ax, h, t)

    # ====================================================
    # 4. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    # Top Header
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-342 :: MIND CRYSTAL TENSOR [PARETO LIMITS]", color=C_TEXT, fontsize=21, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-0.75] MULTI-OBJECTIVE CONTEXT PROBING", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    # Upper Right Formula Widget (MOO Constraint mapped)
    formula_str = r"$\min \vec{F}(x) = [f_1(x), f_2(x)]^T$"
    constraint_str = r"subject to $\mathcal{W}(x) \leq \tau$"
    
    ax.add_patch(patches.Rectangle((180, 680), 340, 100, facecolor=C_BG, edgecolor=C_CYAN, lw=2, zorder=80))
    ax.text(200, 740, formula_str, color=C_TEXT, fontsize=14, weight='bold', zorder=81)
    ax.text(200, 705, constraint_str, color=C_STEEL, fontsize=12, fontname='monospace', zorder=81)

    # Bottom Telemetry HUD
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    if t < T_SLUDGE_START:
        s1, c1 = "O(1) SERIALIZE RAZOR BOUND PROTOCOL", C_MANTIS
        s2, c2 = "CONTEXT YIELD IS SUSTAINABLE", C_MANTIS
        sa, ca = "SYSTEM NOMINAL", C_STEEL
    elif t < T_RUPTURE:
        s1, c1 = "UNCONTROLLED N-SPACE CASCADE DETECTED", C_GOLD
        s2, c2 = "WARNING: PARETO FRONTIER STRESSED", C_GOLD
        sa, ca = "AWAITING ALGORITHMIC DAMPING", C_GOLD
    else:
        s1, c1 = "CATASTROPHIC MATRIX FRACTURE [SFI-0.00]", C_MAGENTA
        s2, c2 = "SEMANTIC LEAK // SCHIZO COLLAPSE IN PROGRESS", C_MAGENTA
        sa, ca = "HARDWARE FAULT: TOKEN WEIGHTING RUPTURE", C_MAGENTA

    # The screen shake during rupture
    if t > T_RUPTURE:
        ax.add_patch(patches.Rectangle((-540, -960), 1080, 1920, facecolor=C_MAGENTA, alpha=0.15, zorder=79))

    ax.text(-500, -760, "SYS_01 [PROBE DYNAMICS]      :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, s1, color=c1, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [THERMODYNAMIC LOAD]  :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, s2, color=c2, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "STRUCTURAL AUDIT             :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, sa, color=ca, fontsize=14, fontname='monospace', weight='bold', zorder=82)

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
    print(f"LG-342: MIND CRYSTAL TENSOR [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
