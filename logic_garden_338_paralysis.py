"""
SOVEREIGN CODE: logic_garden_338_paralysis.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Vectorization
SCENE: Logic Garden 338 (Analysis Paralysis // Cognitive Bottleneck Tensor)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING, COGNITIVE LOGIC
HOTFIX: Linear 20.0s Sequence. Daylight Protocol. Absolute Camera Lock. Tuples Sealed.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
DURATION = 20.0  # 20.0 Second Execution
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_338_paralysis"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Empty Spatial Grid
C_STEEL     = '#606065'   # Jagged Reality Obstacles
C_DARK      = '#202025'   # The Cognitive Payload Node
C_CYAN      = '#00FFFF'   # Smooth Theoretical Vectors (Hallucination)
C_MAGENTA   = '#FF0055'   # Thermal Exhaust / Friction / Spallation
C_GOLD      = '#FFB300'   # Sovereign Fix / Executed Ragged Path
C_MANTIS    = '#00FF00'   # Terminal Green Flow Confirmation

def draw_industrial_grid(ax):
    """Draw the Structural Matrix"""
    for i in range(-5, 6):
        ax.plot([i*100, i*100], [-960, 960], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)
    for j in range(-9, 10):
        ax.plot([-540, 540], [j*100, j*100], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)

# ------------------------------------------------------------------
# ENVIRONMENTAL GEOMETRY (THE AXIOM OF BROKEN GLASS)
# ------------------------------------------------------------------
np.random.seed(338)
N_OBSTACLES = 18
obstacles = []
for i in range(N_OBSTACLES):
    ox = np.random.uniform(-400, 400)
    oy = np.random.uniform(-250, 250)
    # Generate jagged, non-uniform polygon metrics
    angles = np.sort(np.random.uniform(0, 2*np.pi, 5))
    radii = np.random.uniform(20, 90, 5)
    pts = np.column_stack((ox + radii * np.cos(angles), oy + radii * np.sin(angles)))
    obstacles.append(pts)

# The Ragged Diagnosis Path (The actual physical execution route)
P_EXEC = [
    (0, 400),
    (-120, 260),
    (140, 90),
    (-80, -110),
    (100, -250),
    (0, -400)
]
exec_x = [p[0] for p in P_EXEC]
exec_y = [p[1] for p in P_EXEC]

# Calculate total path length for constant velocity interpolation
seg_lens = [np.hypot(exec_x[i]-exec_x[i-1], exec_y[i]-exec_y[i-1]) for i in range(1, len(P_EXEC))]
total_len = sum(seg_lens)
seg_ratios = [l / total_len for l in seg_lens]

def get_kinematic_pos(prg):
    """Rigid O(1) linear interpolation along the ragged execution path."""
    if prg <= 0: return P_EXEC[0]
    if prg >= 1: return P_EXEC[-1]
    
    accum = 0.0
    for i, r in enumerate(seg_ratios):
        if accum + r >= prg:
            local_prg = (prg - accum) / r
            ox, oy = exec_x[i], exec_y[i]
            nx, ny = exec_x[i+1], exec_y[i+1]
            return (ox + (nx - ox) * local_prg, oy + (ny - oy) * local_prg)
        accum += r
    return P_EXEC[-1]

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

    # 1. RENDER BROKEN GLASS OBSTACLES
    for obs in obstacles:
        poly = patches.Polygon(obs, facecolor=C_TITANIUM, edgecolor=C_STEEL, lw=2, alpha=0.7, zorder=2)
        ax.add_patch(poly)

    # Base Nodes
    N_START = (0, 400)
    N_TARGET = (0, -400)
    ax.add_patch(patches.Rectangle((-40, 360), 80, 80, fill=False, edgecolor=C_STEEL, lw=2, linestyle='--', zorder=4))
    ax.add_patch(patches.RegularPolygon(N_TARGET, numVertices=6, radius=40, facecolor=C_BG, edgecolor=C_TEXT, lw=4, zorder=5))
    ax.text(0, -460, "TERMINAL GOAL", color=C_TEXT, fontsize=12, weight='bold', ha='center', fontname='monospace', zorder=5.1)

    # 2. STATE LOGIC ENGINE
    if t < 7.0:
        # STATE 1: THERMODYNAMIC TRAP (Searching for Smooth Hallucinations)
        state_code = "[01] INFINITE RECURSION // THERMODYNAMIC TRAP"
        s_col = C_CYAN
        v_prog = 0.0
        
        # Emitting curved, frictionless paths that fail
        n_paths = min(15, int(t * 3) + 1)
        for i in range(n_paths):
            px = np.sin(t * 2 + i) * 300 * (i/15)
            py = np.cos(t * 1.5 + i) * 200 + 100
            
            p_xs = np.linspace(N_START[0], px, 20)
            p_ys = np.linspace(N_START[1], py, 20)
            # Add "smooth" hallucinatory curves
            p_xs += np.sin(np.linspace(0, np.pi, 20)) * 50 * np.sin(t*5+i)
            ax.plot(p_xs, p_ys, color=C_CYAN, alpha=0.4, lw=1.5, zorder=3)
            
        # Thermal exhaust ring mapping anxiety
        heat_r = 50 + 20 * np.sin(t * 10)
        ax.add_patch(patches.Circle(N_START, heat_r, fill=False, edgecolor=C_MAGENTA, lw=2, alpha=0.8, zorder=3.5))

    elif t < 12.0:
        # STATE 2: RUNAWAY N-SPACE (Paralysis)
        state_code = "[02] O(N\u00b2) RUNAWAY // ANALYSIS PARALYSIS"
        s_col = C_MAGENTA
        v_prog = 0.0
        
        # Fracture / Overload paths
        for i in range(40):
            ex = np.random.uniform(-400, 400)
            ey = np.random.uniform(-100, 300)
            ax.plot([N_START[0], ex], [N_START[1], ey], color=C_MAGENTA if i%3==0 else C_STEEL, lw=0.5, alpha=0.5, zorder=3)
            
        # Violent Thermal Exhaust
        heat_r = 70 + 40 * np.random.random()
        ax.add_patch(patches.Circle(N_START, heat_r, fill=False, edgecolor=C_MAGENTA, lw=4, alpha=0.9, zorder=3.5))
        ax.add_patch(patches.Circle(N_START, heat_r*1.2, fill=False, edgecolor=C_TEXT, lw=1, linestyle='--', zorder=3.4))

    else:
        # STATE 3: SOVEREIGN FIX & KINEMATIC EXECUTION
        v_prog = min(1.0, (t - 12.0) / 6.0) # Moves from 12s to 18s
        state_code = "[03] SOVEREIGN FIX // VECTOR COMMITTED" if v_prog < 1.0 else "[04] TATH\u0100T\u0100 // TERMINAL GREEN FLOW"
        s_col = C_GOLD if v_prog < 1.0 else C_MANTIS
        
        # Draw the absolute rigid, ragged path
        ax.plot(exec_x, exec_y, color=C_GOLD, lw=4, alpha=0.3, linestyle='--', zorder=3)
        
        # Draw path completed so far
        if v_prog > 0:
            cx, cy = get_kinematic_pos(v_prog)
            
            # Find the segment we are on to draw the hard trailing line
            for i in range(len(P_EXEC)-1):
                if exec_y[i] > cy: # Moving down
                    ax.plot([exec_x[i], exec_x[i+1]], [exec_y[i], exec_y[i+1]], color=s_col, lw=5, zorder=3.1)
                else: break

            # Kinematic Spallation at vertices (Friction accepted)
            if v_prog > 0 and v_prog < 1.0:
                ax.scatter(cx, cy, s=np.random.uniform(50, 200), c=C_BG, edgecolors=C_MAGENTA, lw=3, zorder=10)
                ax.scatter(cx+np.random.uniform(-15,15), cy+np.random.uniform(-15,15), s=30, c=C_GOLD, zorder=10.1)

    # 3. RENDER THE COGNITIVE NODE (PAYLOAD)
    cur_pos = get_kinematic_pos(v_prog)
    node_scale = 1.0 if t >= 12.0 else 1.0 + 0.3 * np.sin(t*15) # Shaking during anxiety
    
    trans = matplotlib.transforms.Affine2D().rotate_deg_around(cur_pos[0], cur_pos[1], t*180 if t<12 else (v_prog*360)) + ax.transData
    
    n_col = C_DARK if t >= 12.0 else C_MAGENTA
    ax.add_patch(patches.RegularPolygon(cur_pos, numVertices=4, radius=30*node_scale, facecolor=C_BG, edgecolor=n_col, lw=5, transform=trans, zorder=15))
    ax.add_patch(patches.Circle(cur_pos, 10, facecolor=s_col, zorder=15.1))

    # ====================================================
    # 4. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    # Top Header [Strict Tuples]
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-338 :: ANALYSIS PARALYSIS TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-0.50] COGNITIVE BOTTLENECK // ALGORITHMIC FAILURE STATE", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    # Bottom Telemetry HUD
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    if t < 12.0:
        k_torq = "0.00 kN [ZERO MOVEMENT]"
        t_flow = "BLOCKED // AXES UNLOCKED // RUNAWAY SCOUTING"
    elif t < 18.0:
        k_torq = "84.50 kN [TORQUE TRANSFER ACTIVE]"
        t_flow = "SERIALIZE RAZOR DEPLOYED // FRICTION ACCEPTED"
    else:
        k_torq = "SYSTEM IDLE"
        t_flow = "COMPLETED // METRIC OBLIGATION FULFILLED"

    ax.text(-500, -760, "SYS_STATE [LOGIC MATRIX] :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(10, -760, state_code, color=s_col, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "KINETIC TORQUE OUTPUT    :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(10, -800, k_torq, color=C_GOLD if v_prog > 0 and v_prog < 1 else C_STEEL, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "ARCHITECT INTERVENTION   :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(10, -840, t_flow, color=C_MANTIS if v_prog >= 1.0 else C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider [Strict Tuples]
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=s_col, zorder=83))

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
    print(f"LG-338: ANALYSIS PARALYSIS TENSOR [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE] [Tuples Sealed]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
