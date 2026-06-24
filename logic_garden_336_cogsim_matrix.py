"""
SOVEREIGN CODE: logic_garden_336_cogsim_matrix.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Vectorization
SCENE: Logic Garden 336 (ACS CogSim // Clinical Reasoning Tensor)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING, MEDICAL LOGIC
HOTFIX: Linear 15.0s Sequence. Absolute Camera Lock. Tuple Integrity Confirmed.
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
DURATION = 15.0  # 15.0 Second Forward Execution
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_336_cogsim"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Routine Inactive Pathways
C_STEEL     = '#606065'   # Node Base
C_DARK      = '#202025'   # Cognitive Thread Payload
C_CYAN      = '#00FFFF'   # Diagnostic Ingestion (Safe state)
C_MAGENTA   = '#FF0055'   # Perioperative Complication (Fault state)
C_GOLD      = '#FFB300'   # Clinical Rescue (Stabilization state)
C_WHITE     = '#FFFFFF'

# -------- O(1) DECISION MATRIX COORDINATES --------
N_PRE =   (0, 600)    # Preoperative Baseline
N_INT =   (0, 200)    # Intraoperative Boundary
N_FAULT = (280, -100) # Complication Vector
N_STAB =  (0, -400)   # Recovery / Stabilization
N_POST =  (0, -700)   # Post-Op Clearance
N_FATAL = (400, -500) # Unresolved Error (Dashed phantom path)

# Hard-coded routing array to prevent drift
RAILS = [
    (N_PRE, N_INT),
    (N_INT, N_STAB),   # Expected optimal path (Blocked)
    (N_INT, N_FAULT),  # Anomaly path
    (N_FAULT, N_STAB), # Correct cognitive rescue
    (N_STAB, N_POST),
    (N_FAULT, N_FATAL) # The wrong decision
]

def lerp2d(p1, p2, t_val):
    """Rigid O(1) Linear Interpolation for 2D coordinate Tuples."""
    return (p1[0] + (p2[0] - p1[0]) * t_val, p1[1] + (p2[1] - p1[1]) * t_val)

def draw_industrial_grid(ax):
    """Draw the Cognitive Space scaffolding"""
    for i in range(-5, 6):
        ax.plot([i*100, i*100], [-960, 960], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)
    for j in range(-9, 10):
        ax.plot([-540, 540], [j*100, j*100], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)

def render_frame(packet):
    f, phase_ratio = packet
    t = phase_ratio * DURATION  # Absolute time in seconds
    
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

    draw_industrial_grid(ax)

    # 1. DRAW BASE MATRIX (THE SPATIAL RAILS)
    for start, end in RAILS:
        # Determine strict style for specific routes
        if start == N_INT and end == N_STAB:
            # The blocked "optimal" path
            ax.plot([start[0], end[0]], [start[1], end[1]], color=C_TITANIUM, lw=4, linestyle=':', zorder=1)
            # Strikeout marker
            ax.scatter(0, -100, c=C_MAGENTA, s=400, marker='x', lw=5, zorder=2)
        elif start == N_FAULT and end == N_FATAL:
            # The incorrect clinical decision
            ax.plot([start[0], end[0]], [start[1], end[1]], color=C_MAGENTA, lw=3, linestyle='--', alpha=0.4, zorder=1)
        else:
            # Solid standard rail
            ax.plot([start[0], end[0]], [start[1], end[1]], color=C_TITANIUM, lw=6, zorder=1)
            
    # Draw Static Nodes
    for n_pos in [N_PRE, N_INT, N_STAB, N_POST]:
        ax.add_patch(patches.RegularPolygon(n_pos, numVertices=6, radius=25, facecolor=C_STEEL, edgecolor=C_TEXT, lw=2, zorder=3))

    # The Fault Node is permanently marked as high-risk
    ax.add_patch(patches.RegularPolygon(N_FAULT, numVertices=8, radius=35, facecolor=C_BG, edgecolor=C_MAGENTA, lw=4, zorder=3))

    # 2. THE KINEMATIC STATE ENGINE (PGY-3+ LOGIC ROUTING)
    pos = (0, 0)
    state_desc = ""
    load_val = 0.0
    core_color = C_DARK
    trail_pts = []
    
    if t < 2.5:
        # Phase 1: Preoperative execution (Smooth, Cyan)
        prg = t / 2.5
        pos = lerp2d(N_PRE, N_INT, prg)
        state_desc = "[01] PREOPERATIVE BASELINE // CLEAR"
        load_val = 0.15
        core_color = C_CYAN
        # Trail
        ax.plot([N_PRE[0], pos[0]], [N_PRE[1], pos[1]], color=core_color, lw=4, zorder=2)
        
    elif t < 5.5:
        # Phase 2: Anomaly Divergence (Shifting to Magenta)
        prg = (t - 2.5) / 3.0
        pos = lerp2d(N_INT, N_FAULT, prg)
        state_desc = "[02] PERIOPERATIVE ANOMALY // PATH BLOCKED"
        load_val = 0.15 + (0.75 * prg) # Spiking cognitive load
        core_color = C_MAGENTA if prg > 0.5 else C_CYAN
        
        ax.plot([N_PRE[0], N_INT[0]], [N_PRE[1], N_INT[1]], color=C_CYAN, lw=4, zorder=2)
        ax.plot([N_INT[0], pos[0]], [N_INT[1], pos[1]], color=core_color, lw=4, zorder=2)
        
    elif t < 8.0:
        # Phase 3: Diagnostic Lock (Maximum Friction)
        # The surgeon evaluates CogSim parameters to find the rescue route
        pos = N_FAULT
        state_desc = "[03] COGSIM DIAGNOSTIC // COMPLEX REASONING"
        
        # Heavy jitter representing reasoning loops
        jgt = (t - 5.5) / 2.5
        load_val = 0.90 + 0.1 * np.sin(t * 15 * np.pi) 
        core_color = C_MAGENTA
        
        # Draw prior paths
        ax.plot([N_PRE[0], N_INT[0]], [N_PRE[1], N_INT[1]], color=C_CYAN, lw=4, zorder=2)
        ax.plot([N_INT[0], N_FAULT[0]], [N_INT[1], N_FAULT[1]], color=C_MAGENTA, lw=4, zorder=2)
        
        # Stress spallation rings expanding from the fault
        r_pulse = 35 + 80 * (t % 0.5)*2
        a_pulse = max(0, 1.0 - (t % 0.5)*2)
        ax.add_patch(patches.Circle(N_FAULT, r_pulse, fill=False, edgecolor=C_MAGENTA, lw=4, alpha=a_pulse, zorder=2.5))
        
    elif t < 12.0:
        # Phase 4: Resolution / Corrective Action (Shifting to Gold)
        prg = (t - 8.0) / 4.0
        
        # Use mathematical ease-in/out to simulate calculating the route
        prg_e = prg**2 * (3 - 2*prg) 
        pos = lerp2d(N_FAULT, N_STAB, prg_e)
        
        state_desc = "[04] SURGICAL RESCUE // EXECUTING BYPASS"
        load_val = 0.90 - (0.60 * prg_e)
        core_color = C_GOLD
        
        # Prior paths
        ax.plot([N_PRE[0], N_INT[0]], [N_PRE[1], N_INT[1]], color=C_CYAN, lw=4, zorder=2)
        ax.plot([N_INT[0], N_FAULT[0]], [N_INT[1], N_FAULT[1]], color=C_MAGENTA, lw=4, zorder=2)
        ax.plot([N_FAULT[0], pos[0]], [N_FAULT[1], pos[1]], color=C_GOLD, lw=5, zorder=2)
        
    else:
        # Phase 5: Stabilization and closure
        prg = (t - 12.0) / 3.0
        pos = lerp2d(N_STAB, N_POST, prg)
        state_desc = "[05] TARGET STABILIZED // POST-OP CLEARANCE"
        load_val = 0.30 - (0.20 * prg)
        core_color = C_TITANIUM
        
        ax.plot([N_PRE[0], N_INT[0]], [N_PRE[1], N_INT[1]], color=C_CYAN, lw=4, zorder=2)
        ax.plot([N_INT[0], N_FAULT[0]], [N_INT[1], N_FAULT[1]], color=C_MAGENTA, lw=4, zorder=2)
        ax.plot([N_FAULT[0], N_STAB[0]], [N_FAULT[1], N_STAB[1]], color=C_GOLD, lw=5, zorder=2)
        ax.plot([N_STAB[0], pos[0]], [N_STAB[1], pos[1]], color=C_TITANIUM, lw=4, zorder=2)

    # 3. DRAW THE COGNITIVE SUPERVISOR PAYLOAD
    # A massive rotating geometric node representing active intelligence
    spin = t * 60
    trans_thread = transforms.Affine2D().rotate_deg_around(pos[0], pos[1], spin) + ax.transData
    ax.add_patch(patches.RegularPolygon(pos, numVertices=4, radius=40, facecolor=C_BG, edgecolor=core_color, lw=5, transform=trans_thread, zorder=10))
    ax.add_patch(patches.Circle(pos, 20, facecolor=core_color, zorder=10.1))

    # High-freq processing satellites orbiting the payload
    for ang in [0, 120, 240]:
        rad = np.radians(ang - spin*2)
        sx = pos[0] + 65 * np.cos(rad)
        sy = pos[1] + 65 * np.sin(rad)
        ax.scatter(sx, sy, c=C_TEXT, s=80, marker='D', zorder=10.2)
        ax.plot([pos[0], sx], [pos[1], sy], color=C_TITANIUM, lw=1.5, zorder=9)

    # 4. STATIC WIDGETS
    # Top Header [Tuple Enforced]
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-336 :: ACS COGSIM DECISION TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-0.50] EXECUTING PGY-3+ PHASE-LOCKED METAPHOR", color=C_CYAN, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # Bottom Telemetry HUD [Tuple Enforced]
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 220, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-740, -740], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, -780, "CLINICAL PATHWAY STATE ENGINE:", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -820, state_desc, color=core_color, fontsize=18, fontname='monospace', weight='bold', zorder=82)

    # Dynamic Cognitive Load Bar
    bar_col = C_MAGENTA if load_val > 0.6 else (C_GOLD if load_val > 0.3 else C_CYAN)
    ax.text(-500, -870, f"COGNITIVE PROCESSING LOAD: {load_val*100:>05.1f}%", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    
    # Absolute strict Tuple alignment [Y-Axis Locked]
    ax.add_patch(patches.Rectangle((-500, -900), 1000, 8, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -900), 1000 * load_val, 8, facecolor=bar_col, zorder=83))

    # Sovereign Execution Output: Auto-Scale mathematically locked
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
    print(f"LG-336: COGSIM MATRIX TENSOR [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE] [Tuples Sealed]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
