"""
SOVEREIGN CODE: logic_garden_342b_mind_crystal_optimal.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 342b (Optimal Mind Crystal // Pareto Adjacent Continuous Loop)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, COGNITIVE LOGIC, OPERATIONS RESEARCH
HOTFIX: Seamless 16.0s Loop. Daylight Protocol. Camera Lock. Magenta Purged.
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
DURATION = 16.0  
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_342b_optimal_crystal"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY (OPTIMAL) --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Base Grid Matrix / Inactive Structure
C_STEEL     = '#606065'   # Structural Hardware / Origin
C_GOLD      = '#FFB300'   # O(1) Active Outbound Probes 
C_AZURE     = '#007FFF'   # Stable Internal Connectivity
C_CYAN      = '#00FFFF'   # The Pareto Frontier Limit
C_MANTIS    = '#00FF00'   # Tracked Coordinate / Data Retrieval

# ------------------------------------------------------------------
# O(1) KINEMATIC ARRAY PRE-COMPUTATION (HONEYCOMB PACKING)
# ------------------------------------------------------------------
np.random.seed(342)

ORIGIN_X, ORIGIN_Y = 0, -450

# True Cartesian Honeycomb Math (Pointy-topped)
HEX_R = 25
h_w = np.sqrt(3) * HEX_R
h_h = 2 * HEX_R
col_spacing = h_w
row_spacing = 1.5 * HEX_R

hex_data = [] 
# Scan a broad grid and rigidly filter by distance to simulate organic crystal arc
for col in range(-15, 16):
    for row in range(0, 25):
        cx = ORIGIN_X + col * col_spacing
        if row % 2 != 0:
            cx += col_spacing / 2.0
        cy = ORIGIN_Y + 120 + row * row_spacing
        
        dist = np.sqrt((cx - ORIGIN_X)**2 + (cy - ORIGIN_Y)**2)
        
        # Outer boundary limit = 450 (The Tau Limit). Inner cut-off = 250
        if 250 <= dist <= 450 and cy >= ORIGIN_Y + 50:
            angle = np.arctan2(cy - ORIGIN_Y, cx - ORIGIN_X)
            # Normalizing layer from boundary (0 is the Outer Pareto Edge, higher is interior)
            layer = int((450 - dist) / (row_spacing))
            
            # Lock the array tuple
            hex_data.append({
                'id': len(hex_data), 'cx': cx, 'cy': cy, 
                'dist': dist, 'layer': layer, 'angle': angle
            })

# Sort hexes by angle for orderly wave processing
hex_data.sort(key=lambda x: x['angle'])

def draw_pointy_hex(ax, cx, cy, radius, face_color, edge_color, line_w, alpha_val, zorder_val):
    pts = []
    for i in range(6):
        a = np.radians(i * 60 - 30) # -30 offsets to pointy-top
        pts.append([cx + radius * np.cos(a), cy + radius * np.sin(a)])
    poly = patches.Polygon(pts, facecolor=face_color, edgecolor=edge_color, lw=line_w, alpha=alpha_val, zorder=zorder_val)
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

    # Base Matrix Grid (Mathematical precision background)
    for i in range(-5, 6): ax.plot([i*100, i*100], [-960, 960], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)
    for j in range(-9, 10): ax.plot([-540, 540], [j*100, j*100], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)

    # 1. RENDER CONTINUOUS O(1) EXECUTIONER PROBES & HONEYCOMB LATTICE
    # ----------------------------------------------------------------
    # We drive a continuous complex harmonic wave across the angular coordinate plane
    # 4 massive waves per 16.0s sequence ensures a perfect loop
    waves_per_loop = 4.0
    
    # The Core Node (Processor Origin)
    ax.add_patch(patches.Circle((ORIGIN_X, ORIGIN_Y), 30, facecolor=C_BG, edgecolor=C_STEEL, lw=4, zorder=20))
    ax.add_patch(patches.Circle((ORIGIN_X, ORIGIN_Y), 15, facecolor=C_AZURE, edgecolor='none', zorder=20))

    current_load_metric = 0 # Accumulate load for dynamic telemetry

    for h in hex_data:
        # Calculate dynamic phase engagement for each hex based on its angle
        # This converts physical coordinates into chronological activation triggers
        h_phase = (h['angle'] * 3.0) - (phase_ratio * 2.0 * np.pi * waves_per_loop)
        
        # Activation is mapped to a sharp sine wave pulse, highly tuned for precision
        activation_raw = np.sin(h_phase)
        activation = max(0.0, (activation_raw - 0.75) / 0.25) # Extremely tight, sharp impulses
        
        # Internal wiring: Render baseline connectivity
        ax.plot([ORIGIN_X, h['cx']], [ORIGIN_Y, h['cy']], color=C_TITANIUM, lw=0.5, alpha=0.1, zorder=1)

        c_face = C_BG
        c_edge = C_CYAN if h['layer'] <= 1 else C_AZURE
        alpha_e = 0.4 + (0.6 * activation)
        lw_e = 1.0
        z_layer = 10 - h['layer']

        if activation > 0:
            current_load_metric += activation
            
            # The node actively lights up as it's targeted / processed
            c_edge = C_MANTIS if h['layer'] <= 1 else C_GOLD
            c_face = c_edge
            alpha_f = activation * 0.5
            lw_e = 2.0 + (1.5 * activation)
            
            # Draw the active executioner vector slicing from origin to the node
            # The vector shoots out as activation rises, and pulls data back as it falls
            vec_prg = activation
            vx = ORIGIN_X + (h['cx'] - ORIGIN_X) * vec_prg
            vy = ORIGIN_Y + (h['cy'] - ORIGIN_Y) * vec_prg
            
            ax.plot([ORIGIN_X, vx], [ORIGIN_Y, vy], color=C_GOLD if h['layer']>1 else C_MANTIS, lw=2*activation, alpha=activation, zorder=5)

            # High-fidelity data extraction ripples (Safe Spallation)
            if activation > 0.8 and h['layer'] == 0:
                ax.add_patch(patches.Circle((h['cx'], h['cy']), radius=HEX_R * activation * 1.5, facecolor='none', edgecolor=C_MANTIS, lw=1.5, alpha=(1.0 - activation)*2.0, zorder=12))

            draw_pointy_hex(ax, h['cx'], h['cy'], HEX_R * 0.9, c_face, c_edge, lw_e, alpha_f, z_layer)
        else:
            # Baseline dormant state
            draw_pointy_hex(ax, h['cx'], h['cy'], HEX_R * 0.9, c_face, c_edge, lw_e, alpha_e, z_layer)

    # 2. THE ABSOLUTE BOUNDARY (Tau Limit)
    # ------------------------------------
    # A massive, rigid C_TITANIUM / C_CYAN arc encapsulating the entire structure
    arc_radius = 480
    theta_start, theta_end = 25, 155
    arc_tau = patches.Arc((ORIGIN_X, ORIGIN_Y), arc_radius*2, arc_radius*2, angle=0, theta1=theta_start, theta2=theta_end, color=C_CYAN, linewidth=4, zorder=15)
    ax.add_patch(arc_tau)
    
    # Pulsing energy traveling along the limit line
    flash_prg = (phase_ratio * waves_per_loop) % 1.0
    flash_angle = theta_start + (theta_end - theta_start) * flash_prg
    ax.add_patch(patches.Arc((ORIGIN_X, ORIGIN_Y), arc_radius*2, arc_radius*2, angle=0, theta1=flash_angle-5, theta2=flash_angle+5, color=C_MANTIS, linewidth=8, zorder=16))

    # ====================================================
    # 3. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    # Top Header
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-342b :: OPTIMAL MIND CRYSTAL TENSOR", color=C_TEXT, fontsize=21, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] PARETO ADJACENT // CONTINUOUS O(1) EXECUTION", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    # Upper Right Formula Widget (MOO Constraint mapped with Sovereign Fix \)
    formula_str = r"$\min \vec{F}(x) = [f_1(x), f_2(x)]^T$"
    constraint_str = r"subject to $\mathcal{W}(x) \leq \tau$"
    
    ax.add_patch(patches.Rectangle((180, 680), 340, 100, facecolor=C_BG, edgecolor=C_AZURE, lw=2, zorder=80))
    ax.text(200, 740, formula_str, color=C_TEXT, fontsize=14, weight='bold', zorder=81)
    ax.text(200, 705, constraint_str, color=C_STEEL, fontsize=12, fontname='monospace', zorder=81)

    # Bottom Telemetry HUD
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    # Simulated parameter reading (Safe boundary tracking)
    tau_max = 128000
    current_tokens = int(98000 + (current_load_metric * 1500)) # Fluctuates entirely based on active node logic, never exceeds
    pct_load = (current_tokens / tau_max) * 100

    ax.text(-500, -760, "SYS_01 [PROBE KINEMATICS]    :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, "O(1) SERIALIZE RAZOR PROTOCOL BOUND", color=C_AZURE, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [THERMODYNAMIC LOAD]  :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, f"SYSTEM NOMINAL // {current_tokens:,} < {tau_max:,} (\u03C4)", color=C_GOLD, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "STRUCTURAL AUDIT             :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, "TERMINAL GREEN FLOW ACHIEVED", color=C_MANTIS, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider [Strict Tuples]
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=C_MANTIS, zorder=83))
    
    # Real-time Load Bar
    ax.add_patch(patches.Rectangle((20, -820), 400, 4, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((20, -820), 400 * (pct_load/100.0), 4, facecolor=C_GOLD, zorder=83))

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
    print(f"LG-342b: CONTINUOUS OPTIMAL CRYSTAL TENSOR [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
