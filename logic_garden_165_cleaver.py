"""
SOVEREIGN CODE: logic_garden_165_cleaver.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Algorithmic Pathfinding (35 seconds)
SCENE: Logic Garden 165 (O(log N) Cleaver / Binary vs. Linear Search)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing as mp
import os
import gc
import math

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 35                   
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_165_cleaver"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_CYAN    = '#00FFFF'          # Linear Search (Artisan Friction)
C_MANTIS  = '#00FF00'          # Binary Search (Terminal Green Cleaver)
C_GOLD    = '#FFD700'          # The Target / Sovereign Truth
C_RED     = '#FF0033'          # Entropy Erased into the Void
C_DIM     = '#1A1A24'          # Unsearched Hardware

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# HARDWARE LATTICE GENERATION (COMPILE-TIME LOCK)
# ------------------------------------------------------------------
N = 2048
TARGET_IDX = 1913 # Specifically placed in an upper quartile to punish Linear Search

# Create a beautiful sweeping parabolic curve for both arrays
indices = np.arange(N)
norm_i = indices / float(N - 1)
base_y = 250 + (1300 * (norm_i ** 1.3)) # Exaggerated geometry

# Left Array (Linear Search) Harp string bowing outward
left_x = 280 + (np.sin(norm_i * np.pi) * -120)

# Right Array (Binary Search) Harp string bowing outward
right_x = 800 + (np.sin(norm_i * np.pi) * 120)

# Pre-compute Binary Search algorithmic steps to ensure perfect mathematical locking
b_steps = []
low = 0
high = N - 1
while low <= high:
    mid = (low + high) // 2
    b_steps.append({'low': low, 'mid': mid, 'high': high})
    if mid == TARGET_IDX:
        break
    elif mid < TARGET_IDX:
        low = mid + 1
    else:
        high = mid - 1

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (ISOLATED MEMORY NODE)
# ------------------------------------------------------------------
def render_frame(data_packet):
    f, t_sec, state_str, ui_col, lin_idx, b_step_idx, b_state, erase_times = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # -----------------------------------------------------------
    # 1. RENDER LINEAR SEARCH O(N) [LEFT]
    # -----------------------------------------------------------
    # Unsearched
    unsearched_mask = indices > lin_idx
    ax.scatter(left_x[unsearched_mask], base_y[unsearched_mask], s=2, c=C_DIM, zorder=1)
    
    # Searched (Cyan Trail)
    searched_mask = indices <= lin_idx
    if np.any(searched_mask):
        ax.scatter(left_x[searched_mask], base_y[searched_mask], s=4, c=C_CYAN, alpha=0.4, zorder=2)
    
    # Target
    ax.scatter([left_x[TARGET_IDX]], [base_y[TARGET_IDX]], s=250, c=C_GOLD, marker='D', zorder=5)
    
    # Linear Scan Head (Artisan Friction)
    head_y = base_y[min(lin_idx, N-1)]
    ax.plot([0, left_x[min(lin_idx, N-1)]], [head_y, head_y], c=C_CYAN, lw=2, alpha=0.8, zorder=6)
    ax.scatter([left_x[min(lin_idx, N-1)]], [head_y], s=120, c=C_TEXT, zorder=7)

    # -----------------------------------------------------------
    # 2. RENDER BINARY SEARCH O(log N) [RIGHT]
    # -----------------------------------------------------------
    b_x = np.copy(right_x)
    b_y = np.copy(base_y)
    b_c = np.full((N, 4), hex_to_rgba(C_DIM, 1.0))
    b_s = np.full(N, 2.0)
    
    cur_low = b_state['low']
    cur_high = b_state['high']
    cur_mid = b_state['mid']

    # Erased Physics Protocol (Falling into Void)
    dt_erased = t_sec - erase_times
    erased_mask = dt_erased > 0
    valid_mask = ~erased_mask
    
    if np.any(erased_mask):
        # Ballistic trajectory for culled entropy
        b_y[erased_mask] -= 0.5 * 1500.0 * (dt_erased[erased_mask] ** 2)
        b_x[erased_mask] += np.sin(indices[erased_mask]) * 50.0 * dt_erased[erased_mask]
        alphas = np.clip(1.0 - dt_erased[erased_mask]*1.5, 0.0, 1.0)
        c_reds = np.zeros((np.sum(erased_mask), 4))
        c_reds[:, 0:3] = hex_to_rgba(C_RED)[0:3]
        c_reds[:, 3] = alphas
        
        ax.scatter(b_x[erased_mask], b_y[erased_mask], s=b_s[erased_mask]*2, c=c_reds, marker='x', zorder=1)

    # Surviving Hardware 
    if np.any(valid_mask):
        b_c[valid_mask] = hex_to_rgba(C_TEXT, 0.5)
        ax.scatter(b_x[valid_mask], b_y[valid_mask], s=b_s[valid_mask]*2, c=b_c[valid_mask], zorder=3)

    # Active Bounding Box Highlight
    if not (b_step_idx == len(b_steps)-1 and t_sec > 3.0 + len(b_steps)):
        active_mask = valid_mask & (indices >= cur_low) & (indices <= cur_high)
        if np.any(active_mask):
            b_c[active_mask] = hex_to_rgba(C_MANTIS, 0.9)
            ax.scatter(b_x[active_mask], b_y[active_mask], s=b_s[active_mask]*4, c=b_c[active_mask], zorder=4)

    # Target
    ax.scatter([right_x[TARGET_IDX]], [base_y[TARGET_IDX]], s=250, c=C_GOLD, marker='D', zorder=5)

    # Binary Cleaver UI Arrays
    if cur_low <= cur_high:
        # Mid-point Cleaver Array
        mid_y = base_y[cur_mid]
        mid_x = right_x[cur_mid]
        if valid_mask[cur_mid]:
            ax.plot([540, 1080], [mid_y, mid_y], c=C_MANTIS, lw=3, zorder=8)
            ax.text(550, mid_y + 15, "TEST", color=C_MANTIS, fontsize=12, fontname='monospace')
            ax.scatter([mid_x], [mid_y], s=200, c=C_TEXT, marker='s', zorder=9)

    # -----------------------------------------------------------
    # 3. TELEMETRY WIDGETS
    # -----------------------------------------------------------
    # Central Divider
    ax.plot([540, 540], [0, 1920], color=C_DIM, lw=2, zorder=0)

    # Top Terminal
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2)
    ax.text(0.04, 0.965, "LOGIC GARDEN 165 :: THE O(log N) CLEAVER", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    # Status Panel
    ax.text(0.04, 0.88, f"LINEAR SCAN [O(N)]", transform=ax.transAxes, color=C_CYAN, fontsize=22, fontname='monospace', weight='bold')
    ax.text(0.04, 0.85, f"OPERATIONS : {lin_idx:>04d}", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    
    ax.text(0.55, 0.88, f"BINARY SEARCH [O(log N)]", transform=ax.transAxes, color=C_MANTIS, fontsize=22, fontname='monospace', weight='bold')
    ax.text(0.55, 0.85, f"OPERATIONS : {b_step_idx+1:>04d}", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    
    # Mathematical Efficacy Check
    lin_found = "YES" if lin_idx >= TARGET_IDX else "SEARCHING..."
    bin_found = "YES (TERMINAL FLOW)" if cur_mid == TARGET_IDX else "BOUNDING..."
    
    ax.text(0.04, 0.80, f"TARGET {TARGET_IDX:>04d}: {lin_found}", transform=ax.transAxes, color=C_RED if lin_idx < TARGET_IDX else C_MANTIS, fontsize=16, fontname='monospace')
    ax.text(0.55, 0.80, f"TARGET {TARGET_IDX:>04d}: {bin_found}", transform=ax.transAxes, color=C_RED if cur_mid != TARGET_IDX else C_GOLD, fontsize=16, fontname='monospace')

    # Bottom Terminal
    ax.add_patch(plt.Rectangle((0, 0), 0.95, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 0.95], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2)
    
    pulse = ui_col if (f % 60 < 30) or ui_col == C_GOLD else C_TEXT
    ax.text(0.04, 0.08, "SYSTEM EFFICIENCY:", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=26, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf(); plt.close(fig); plt.close('all'); gc.collect() 
    return f

# ------------------------------------------------------------------
# PHYSICS ENGINE (TIME SYNCHRONIZATION MATRIX)
# ------------------------------------------------------------------
def generate_physics_stream():
    # Timing Blocks
    START_RACE = 3.0
    LIN_SPEED = 60.0 # Reads per second. Takes ~34s to reach end.
    BIN_STEP_DUR = 1.2 # 1.2s per log cut
    
    erase_times = np.full(N, 999.0) # t_sec when node is geometrically deleted

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        # 1. Linear Index Calculation
        if t_sec < START_RACE:
            lin_idx = 0
            state = "[01] TARGET ALLOCATED (PRE-RACE)"
            ui_col = C_VOID
        else:
            time_active = t_sec - START_RACE
            lin_idx = int(time_active * LIN_SPEED)
            lin_idx = min(lin_idx, N-1)
            
            if lin_idx >= TARGET_IDX:
                lin_idx = TARGET_IDX
                
        # 2. Binary Protocol Calculation
        if t_sec < START_RACE:
            b_step_idx = 0
        else:
            time_active = t_sec - START_RACE
            b_step_idx = int(time_active / BIN_STEP_DUR)
        
        b_step_idx = min(b_step_idx, len(b_steps) - 1)
        b_state = b_steps[b_step_idx]
        
        # Erase nodes falling outside the Bounding Box
        mask_to_erase = (erase_times == 999.0) & ((indices < b_state['low']) | (indices > b_state['high']))
        if np.any(mask_to_erase):
            erase_times[mask_to_erase] = t_sec # Instantly marks them to fall

        # Dynamic State Management
        if t_sec > START_RACE:
            if b_step_idx < len(b_steps) - 1:
                state = "[02] O(log N) DEPLOYING BOUNDING BOXES"
                ui_col = C_MANTIS
            else:
                state = "[03] TATHĀTĀ: O(N) FAILS / O(log N) RESOLVES"
                ui_col = C_GOLD

        # Yield Data Frame Copies
        yield (f, t_sec, state, ui_col, lin_idx, b_step_idx, b_state, erase_times.copy())

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 165: THE O(log N) CLEAVER [CORES: {cpu_cores}]")
    print(f"Tracking Arithmetic Matrix: {N} Nodes. Target = {TARGET_IDX}")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
