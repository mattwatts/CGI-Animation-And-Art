"""
SOVEREIGN CODE: logic_garden_168_quicksort.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Recursive Frameworks (35 seconds)
SCENE: Logic Garden 168 (The Recursive Pivot / QuickSort vs BubbleSort)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import multiprocessing as mp
import os
import gc
import sys

# Increase recursion depth for QuickSort
sys.setrecursionlimit(5000)

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 35                   
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_168_quicksort"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_CYAN    = '#00FFFF'          # Bubble Sort (Artisan Friction)
C_RED     = '#FF0033'          # Hardware Overheating
C_GOLD    = '#FFD700'          # QuickSort Pivot (Bounding Box)
C_MANTIS  = '#00FF00'          # Terminal Flow (Sorted Lattice)
C_DIM     = '#1A1A24'          # Hardware Mesh

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# SYSTEM PRE-COMPILATION (OPERATIONS RESEARCH LOCK)
# ------------------------------------------------------------------
N = 2048
np.random.seed(168)
original_arr = np.random.rand(N)

# 1. QuickSort Pre-Compilation (Tracking O(N * log N) Mechanics)
qs_history = []
qs_ops = 0
qs_arr = original_arr.copy()

def partition(arr, low, high):
    global qs_ops
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        qs_ops += 1
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    qs_ops += 1
    qs_history.append((qs_ops, arr.copy(), (low, high, i + 1)))
    return i + 1

def quicksort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quicksort(arr, low, pi - 1)
        quicksort(arr, pi + 1, high)

quicksort(qs_arr, 0, N - 1)
QS_TOTAL_OPS = qs_ops
qs_history.append((qs_ops + 10, qs_arr.copy(), (0, N-1, -1))) # Final terminal state

# 2. Bubble Sort Pre-Compilation (Tracking O(N²) Mechanics)
# We strictly lock the instruction rate so Bubble Sort receives the exact
# same number of CPU cycles per second as QuickSort.
bs_history = []
bs_ops = 0
bs_arr = original_arr.copy()

# The simulation ends at 35 seconds. QS finishes around 20 seconds.
# Calculate maximum operations allocated for the entire video timeline.
MAX_SIM_OPS = int((QS_TOTAL_OPS / 20.0) * DURATION) 
SAVE_INTERVAL = max(1, QS_TOTAL_OPS // 500) # Ensure high-fidelity state tracking

for i in range(N):
    for j in range(0, N - i - 1):
        bs_ops += 1
        if bs_arr[j] > bs_arr[j + 1]:
            bs_arr[j], bs_arr[j + 1] = bs_arr[j + 1], bs_arr[j]
        
        if bs_ops % SAVE_INTERVAL == 0:
            bs_history.append((bs_ops, bs_arr.copy(), j))
            
        if bs_ops > MAX_SIM_OPS:
            break
    if bs_ops > MAX_SIM_OPS:
        break


# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (ISOLATED MEMORY NODE)
# ------------------------------------------------------------------
def render_frame(data_packet):
    f, t_sec, state_str, ui_col, current_ops = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # Offset metrics for 9:16 terminal
    TOP_Y_MIN = 1050
    TOP_Y_MAX = 1750
    BOT_Y_MIN = 150
    BOT_Y_MAX = 850
    
    x_coords = np.linspace(50, 1030, N)

    # Resolve active histories via Binary Search logic
    import bisect
    
    # QuickSort State
    qs_idx = bisect.bisect_right([s[0] for s in qs_history], current_ops) - 1
    qs_idx = max(0, min(qs_idx, len(qs_history)-1))
    qs_curr_ops, qs_cur_arr, (q_low, q_high, q_pi) = qs_history[qs_idx]
    
    # BubbleSort State
    bs_idx = bisect.bisect_right([s[0] for s in bs_history], current_ops) - 1
    bs_idx = max(0, min(bs_idx, len(bs_history)-1))
    bs_curr_ops, bs_cur_arr, b_scan_j = bs_history[bs_idx]

    # -----------------------------------------------------------
    # 1. TOP PANEL: O(N log N) QUICKSORT
    # -----------------------------------------------------------
    y_qs = TOP_Y_MIN + (qs_cur_arr * (TOP_Y_MAX - TOP_Y_MIN))
    qs_color = C_TEXT
    
    is_qs_done = (current_ops >= QS_TOTAL_OPS)
    if is_qs_done:
        ax.scatter(x_coords, y_qs, s=7, c=C_MANTIS, zorder=3)
        ax.plot(x_coords, y_qs, c=C_MANTIS, lw=3, alpha=0.3, zorder=2) # Glow
    else:
        ax.scatter(x_coords, y_qs, s=4, c=C_TEXT, zorder=3)
        # Structural Framework (Pivots)
        if q_pi != -1:
            px_low = x_coords[q_low]
            px_high = x_coords[q_high]
            px_pi = x_coords[q_pi]
            
            # Draw the fractured sector bounding box
            ax.add_patch(Rectangle((px_low, TOP_Y_MIN), px_high - px_low, TOP_Y_MAX - TOP_Y_MIN, 
                                   fill=True, color=C_GOLD, alpha=0.1, zorder=1))
            # Draw the rigid Authority Pivot line
            ax.plot([px_pi, px_pi], [TOP_Y_MIN, TOP_Y_MAX], c=C_GOLD, lw=2, zorder=4)

    # -----------------------------------------------------------
    # 2. BOTTOM PANEL: O(N²) BUBBLESORT
    # -----------------------------------------------------------
    y_bs = BOT_Y_MIN + (bs_cur_arr * (BOT_Y_MAX - BOT_Y_MIN))
    ax.scatter(x_coords, y_bs, s=4, c=C_TEXT, zorder=3)
    
    # Draw Scan-Line Physics Mask (The dragging friction)
    scan_x = x_coords[b_scan_j]
    ax.plot([scan_x, scan_x], [BOT_Y_MIN, BOT_Y_MAX], c=C_CYAN, lw=4, alpha=0.9, zorder=4)
    # The wake of the scan trailing leftwards
    ax.add_patch(Rectangle((max(50, scan_x - 150), BOT_Y_MIN), 150, BOT_Y_MAX - BOT_Y_MIN, 
                           fill=True, color=C_CYAN, alpha=0.15, zorder=1))

    # Right edge settling indicator (the only part getting sorted)
    sorted_bound_x = x_coords[N - 1 - (b_scan_j % N)] if current_ops > 1000 else 1030
    ax.plot([sorted_bound_x, 1030], [BOT_Y_MIN, BOT_Y_MAX], c=C_CYAN, lw=2, alpha=0.3, zorder=2)

    # -----------------------------------------------------------
    # 3. OVERLAYS & HARDWARE GRIDS
    # -----------------------------------------------------------
    ax.add_patch(Rectangle((40, TOP_Y_MIN-20), 1000, 740, fill=False, edgecolor=C_DIM, lw=2, zorder=0))
    ax.add_patch(Rectangle((40, BOT_Y_MIN-20), 1000, 740, fill=False, edgecolor=C_DIM, lw=2, zorder=0))

    # Top Terminal Data
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2)
    ax.text(0.04, 0.965, "LOGIC GARDEN 168 :: RECURSIVE PIVOTS", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    # QuickSort Telemetry (Top)
    ax.text(0.04, 0.90, f"QUICKSORT [O(N log N)]", transform=ax.transAxes, color=C_GOLD if not is_qs_done else C_MANTIS, fontsize=22, fontname='monospace', weight='bold')
    ax.text(0.04, 0.88, f"LOGIC: RECURSIVE FRACTURE (PIVOTS)", transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace')
    
    # Bubble Sort Telemetry (Bottom)
    ax.text(0.04, 0.46, f"BUBBLE SORT [O(N²)]", transform=ax.transAxes, color=C_CYAN, fontsize=22, fontname='monospace', weight='bold')
    ax.text(0.04, 0.44, f"LOGIC: GLOBAL LINEAR FRICTION", transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace')

    # The Central Hardware Execution Lock
    ax.text(0.50, 0.49, f"LOCKED INSTRUCTION RATE: {current_ops:>07d} OPS", transform=ax.transAxes, color=C_RED if current_ops < QS_TOTAL_OPS else C_CYAN, fontsize=20, fontname='monospace', ha='center')

    # Bottom Terminal
    ax.add_patch(plt.Rectangle((0, 0), 0.95, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 0.95], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2)
    
    pulse = ui_col if (f % 60 < 30) or ui_col == C_MANTIS else C_TEXT
    ax.text(0.04, 0.08, "ARRAY STATE:", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=26, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf(); plt.close(fig); plt.close('all'); gc.collect() 
    return f

# ------------------------------------------------------------------
# PHYSICS ENGINE (THERMODYNAMIC TIME MAPPING)
# ------------------------------------------------------------------
def generate_physics_stream():
    # Execute identical ops/sec for both to prove geometrical failure
    # Target QS finish at T = 20.0s
    OPS_PER_SEC = QS_TOTAL_OPS / 20.0 

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        current_ops = int(t_sec * OPS_PER_SEC)
        
        # State cycling for visual pacing
        if t_sec < 20.0:
            state = "[01] ORCHESTRATING SIMULTANEOUS COLLAPSE"
            ui_col = C_GOLD
        elif t_sec < 30.0:
            state = "[02] QUICKSORT TERMINAL (BUBBLE SORT DROWNING)"
            ui_col = C_MANTIS
        else:
            state = "[03] TATHĀTĀ: ORGANIZE THE FRACTURE"
            ui_col = C_MANTIS

        yield (f, t_sec, state, ui_col, current_ops)

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 168: RECURSIVE PIVOTS [CORES: {cpu_cores}]")
    print(f"Hardware Logic Lock Activated. Tracking {N} Nodes.")
    print(f"QS Target Operations: {QS_TOTAL_OPS}")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
