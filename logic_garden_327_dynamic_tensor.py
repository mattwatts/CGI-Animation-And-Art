"""
SOVEREIGN CODE: logic_garden_327_dynamic_tensor.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 327 (Dynamic Programming // Bellman Optimization Tensor)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Seamless 10.0s Loop. Absolute Camera Lock. O(2^N) to O(N) Topological Tabulation.
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
OUT_DIR = "frames_327_dynamic_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # O(2^N) Chaotic Overlap Web
C_STEEL     = '#606065'   # O(N) Optimized Substructure Paths
C_DARK      = '#202025'   # Hardware Node Base
C_GOLD      = '#FFB300'   # Optimal Policy Indicator
C_MAGENTA   = '#FF0055'   # Sovereign Optimal Matrix Vector
C_CYAN      = '#00FFFF'   # Cached Value Extraction
C_WHITE     = '#FFFFFF'

# -------- KINEMATIC CONSTANTS --------
DY = 150       # Vertical row offset
DX = 105       # Horizontal state offset
N_COLS = 9     # Number of parallel states per row
ROW_CYCLE = 10 # 10 Rows exactly cycle per 10.0 seconds

# ------------------------------------------------------------------
# O(1) DETERMINISTIC MATRIX CACHE (THE BELLMAN SOLUTION)
# ------------------------------------------------------------------
DP_OPT = np.zeros((ROW_CYCLE, N_COLS), dtype=int)
for r in range(ROW_CYCLE):
    for c in range(N_COLS):
        val = int(round(c + 1.8 * np.sin(r * 2 * np.pi / ROW_CYCLE + c * 0.4)))
        DP_OPT[r, c] = max(0, min(N_COLS - 1, val))

def get_node_x(j):
    return (j - 4) * DX

def get_row_y(i, phase_ratio):
    return (i - phase_ratio * ROW_CYCLE) * DY - 450

def draw_hardware_node(ax, x, y, state_val, is_optimized, alpha_m):
    height = 20
    width = 44
    border = C_TEXT if is_optimized else C_STEEL
    fill = C_DARK if is_optimized else C_BG
    
    ax.add_patch(patches.Rectangle((x - width/2, y - height/2), width, height, facecolor=fill, edgecolor=border, lw=2, alpha=alpha_m, zorder=6))
    
    if is_optimized:
        ax.text(x, y, f"V:{state_val:02d}", color=C_CYAN, fontsize=8, fontname='monospace', weight='bold', ha='center', va='center', alpha=alpha_m, zorder=6.1)

def render_frame(packet):
    f, phase_ratio = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    
    # BARE-METAL CAMERA LOCK: Forces the viewport to exactly these coordinates.
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)
    
    # THE IRON CAGE: Violently suppresses Matplotlib's auto-zooming AI.
    # Off-screen vectors will now be physically clipped, preventing the "shrink".
    ax.autoscale(False)

    # 1. THE BELLMAN COMPUTATION THRESHOLD
    THRESHOLD_Y = 180
    
    # 2. EVALUATING THE DYNAMIC GRAPH
    for i in range(-5, 25):
        cy = get_row_y(i, phase_ratio)
        ny = get_row_y(i - 1, phase_ratio)
        
        alpha_m = 1.0
        if cy < -800: alpha_m = max(0, (cy + 1000) / 200.0)
        if cy > 1300: continue
        
        is_optimized = cy <= THRESHOLD_Y
        
        for j in range(N_COLS):
            cx = get_node_x(j)
            state_val = ((i%ROW_CYCLE) * 7 + j * 3) % 99
            
            draw_hardware_node(ax, cx, cy, state_val, is_optimized, alpha_m)
            
            if ny > -1000:
                opt_j = DP_OPT[i % ROW_CYCLE, j]
                
                if not is_optimized:
                    for kj in [j-1, j, j+1]:
                        if 0 <= kj < N_COLS:
                            kx = get_node_x(kj)
                            ax.plot([cx, kx], [cy - 10, ny + 10], color=C_TITANIUM, lw=1.5, alpha=0.35, zorder=2)
                else:
                    kx = get_node_x(opt_j)
                    ax.plot([cx, kx], [cy - 10, ny + 10], color=C_STEEL, lw=2.5, alpha=alpha_m*0.8, zorder=3)

    # 3. THE SOVEREIGN MAGENTA PIPELINE (GLOBAL TRACE)
    trace_i = int(np.floor((THRESHOLD_Y + 450) / DY + phase_ratio * ROW_CYCLE))
    trace_j = int(N_COLS / 2)
    
    trace_pts_x = []
    trace_pts_y = []
    
    for _ in range(15):
        cy = get_row_y(trace_i, phase_ratio)
        if cy < -900: break
        
        trace_pts_x.append(get_node_x(trace_j))
        trace_pts_y.append(cy)
        
        trace_j = DP_OPT[trace_i % ROW_CYCLE, trace_j]
        trace_i -= 1

    if len(trace_pts_x) > 1:
        ax.plot(trace_pts_x, trace_pts_y, color=C_MAGENTA, lw=7, solid_joinstyle='bevel', alpha=0.9, zorder=4)

    # 4. STATIC HARDWARE WIDGETS
    ax.add_patch(patches.Rectangle((-540, THRESHOLD_Y - 20), 1080, 40, facecolor=C_TITANIUM, alpha=0.9, zorder=10))
    ax.plot([-540, 540], [THRESHOLD_Y + 20, THRESHOLD_Y + 20], color=C_TEXT, lw=2, zorder=10.1)
    ax.plot([-540, 540], [THRESHOLD_Y - 20, THRESHOLD_Y - 20], color=C_CYAN, lw=2, zorder=10.1)
    ax.text(0, THRESHOLD_Y, "THE BELLMAN THRESHOLD // TABULATION OVERRIDE", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', ha='center', va='center', zorder=11)

    ax.text(-500, 880, "LG-327 :: DYNAMIC PROGRAMMING TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, 840, "[SFI-1.00] OPTIMAL SUBSTRUCTURE CACHE // MEMOIZATION MATRIX", color=C_STEEL, fontsize=12, fontname='monospace', zorder=80)
    
    ax.add_patch(patches.Rectangle((-520, 680), 1040, 140, facecolor=C_BG, edgecolor=C_TITANIUM, lw=2, alpha=0.9, zorder=79))
    ax.text(-500, 785, "RICHARD BELLMAN // O(2^N) TO O(N) TOPOLOGICAL SEVERING", color=C_DARK, fontsize=15, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, 740, "Equation: V(x) = max_a { C(x, a) + γV(T(x, a)) }", color=C_MAGENTA, fontsize=14, fontname='monospace', weight='bold', zorder=80)
    
    ax.add_patch(patches.Rectangle((-520, -940), 1040, 120, facecolor=C_DARK, alpha=0.95, zorder=79))
    
    pipeline_state = abs(np.sin(phase_ratio * ROW_CYCLE * np.pi))
    ax.text(-500, -855, "GLOBAL RECURSION STATE: SEVERED", color=C_STEEL, fontsize=14, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, -895, f"CACHED MEMORY ARRAY ACCESS: {pipeline_state * 100:>05.2f} % Δ [ACTIVE LOAD]", color=C_CYAN if pipeline_state > 0.5 else C_TITANIUM, fontsize=14, fontname='monospace', weight='bold', zorder=80)
    
    ax.add_patch(patches.Rectangle((-500, -915), 1000, 4, facecolor=C_STEEL, zorder=80))
    ax.add_patch(patches.Rectangle((-500, -915), 1000 * pipeline_state, 4, facecolor=C_CYAN, zorder=81))

    # Strict Output Control Enforced
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
    print(f"LG-327: DYNAMIC PROGRAMMING TENSOR [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
