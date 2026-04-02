"""
SOVEREIGN CODE: logic_garden_148_stochastic_pi.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Stochastic Geometric Convergence
SCENE: Logic Garden 148 (The C64 Steam Train: Revealing Pi)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
import os
import multiprocessing as mp
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 30                   
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_148_pi_steam"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE ZEN / INDUSTRIAL PALETTE --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'

C_C64_BG  = '#352879'           # Authentic C64 Screen Blue
C_C64_BORDER = '#6C5EB5'        # Authentic C64 Border Light Blue

C_CYAN    = '#00FFCC'           # The Truth Payload (Inside Limit)
C_RED     = '#FF003C'           # The Entropy / Friction (Outside Limit)
C_MANTIS  = '#00FF00'           # Terminal Green 
C_GOLD    = '#FFD700'           # The Mathematical Ideal Line

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (ISOLATED MEMORY NODE)
# ------------------------------------------------------------------
def render_frame(data_packet):
    f, t_sec, px, py, sizes, colors, pi_est, error, max_idx, line_cursor = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    fig.patch.set_facecolor(C_C64_BORDER)
    
    # --- TOP COMPONENT: THE C-64 BOOT & BASIC LOGIC (420px height approx) ---
    ax_top = fig.add_axes([0.05, 0.78, 0.90, 0.20])
    ax_top.set_axis_off()
    ax_top.add_patch(plt.Rectangle((0, 0), 1, 1, color=C_C64_BG, zorder=0))
    
    ax_top.text(0.05, 0.85, "COMMODORE 64 BASIC V2", color=C_C64_BORDER, fontsize=28, fontname='monospace', weight='bold')
    ax_top.text(0.05, 0.70, "64K RAM SYSTEM  38911 BASIC BYTES FREE", color=C_C64_BORDER, fontsize=20, fontname='monospace')
    ax_top.text(0.05, 0.55, "READY.", color=C_C64_BORDER, fontsize=24, fontname='monospace')
    
    # The Steam Train Engine Code
    ax_top.text(0.05, 0.35, "10 X=RND(1): Y=RND(1)", color=C_TEXT if line_cursor==1 else C_C64_BORDER, fontsize=20, fontname='monospace', weight='bold' if line_cursor==1 else 'normal')
    ax_top.text(0.05, 0.22, "20 IF (X*X+Y*Y)<=1 THEN C=C+1", color=C_TEXT if line_cursor==2 else C_C64_BORDER, fontsize=20, fontname='monospace', weight='bold' if line_cursor==2 else 'normal')
    ax_top.text(0.05, 0.09, "30 T=T+1: PRINT 4*(C/T)", color=C_TEXT if line_cursor==3 else C_C64_BORDER, fontsize=20, fontname='monospace', weight='bold' if line_cursor==3 else 'normal')
    ax_top.text(0.05, -0.04, "40 GOTO 10", color=C_TEXT if line_cursor==4 else C_C64_BORDER, fontsize=20, fontname='monospace', weight='bold' if line_cursor==4 else 'normal')

    # --- MIDDLE COMPONENT: THE VOID / GEOMETRIC SANDBOX (1080x1080 pure square) ---
    # Centered precisely. Width=1.0, Height=1080/1920 = 0.5625
    ax_graph = fig.add_axes([0.0, 0.21875, 1.0, 0.5625])
    ax_graph.set_facecolor(C_VOID)
    ax_graph.set_xlim(-1.05, 1.05)
    ax_graph.set_ylim(-1.05, 1.05)
    ax_graph.set_xticks([])
    ax_graph.set_yticks([])
    
    # 1. The Ideal Bounding Box (Zen Truth)
    perfect_circle = plt.Circle((0, 0), 1.0, color=C_GOLD, fill=False, lw=1.5, alpha=0.6, zorder=1)
    ax_graph.add_patch(perfect_circle)
    ax_graph.axhline(0, color=C_GOLD, lw=1, alpha=0.3, zorder=1)
    ax_graph.axvline(0, color=C_GOLD, lw=1, alpha=0.3, zorder=1)

    # 2. The Particles (Stochastic Output)
    if len(px) > 0:
        ax_graph.scatter(px, py, s=sizes, c=colors, edgecolors='none', zorder=5)

    # --- BOTTOM COMPONENT: THE TELEMETRY OUTPUT (approx 420px height) ---
    ax_bot = fig.add_axes([0.05, 0.02, 0.90, 0.18])
    ax_bot.set_axis_off()
    ax_bot.add_patch(plt.Rectangle((0, 0), 1, 1, color=C_C64_BG, zorder=0))

    ax_bot.text(0.05, 0.80, "RUN", color=C_C64_BORDER, fontsize=24, fontname='monospace')
    
    # Display the current state of the machine
    ax_bot.text(0.05, 0.55, f"T (ITERATIONS) : {max_idx:07d}", color=C_TEXT, fontsize=24, fontname='monospace')
    
    # Estimate tracking
    calc_color = C_CYAN if max_idx > 10 else C_TEXT
    ax_bot.text(0.05, 0.35, f"PI ESTIMATION  : {pi_est:.6f}", color=calc_color, fontsize=26, fontname='monospace', weight='bold')
    
    # The Error Signal & Critical Damping Visualizer
    err_color = C_RED if error > 0.01 else (C_MANTIS if error < 0.002 else C_GOLD)
    err_text = "TATHATA (SUCHNESS)" if error < 0.002 and max_idx > 50000 else f"DELTA (ERROR)  : {error:.6f}"
    ax_bot.text(0.05, 0.15, err_text, color=err_color, fontsize=24, fontname='monospace', weight='bold')
    
    # Flashing executing cursor
    flash = "█" if f % 6 < 3 else ""
    ax_bot.text(0.85, 0.15, flash, color=C_C64_BORDER, fontsize=24, fontname='monospace')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf()
    plt.close(fig)
    plt.close('all')
    gc.collect() 
    return f

# ------------------------------------------------------------------
# THE PHYSICS ENGINE (STOCHASTIC MONTE CARLO SEED GENERATOR)
# ------------------------------------------------------------------
def generate_physics_stream():
    np.random.seed(314159) # The architecture is conceptually deterministic
    
    N = 85000 # High density sample for absolute visual truth
    
    X_full = np.random.uniform(-1.0, 1.0, N)
    Y_full = np.random.uniform(-1.0, 1.0, N)
    
    R2_full = X_full**2 + Y_full**2
    mask_in_full = R2_full <= 1.0
    
    # Cumulative calculation O(1) vectorized
    cum_hits = np.cumsum(mask_in_full)
    denoms = np.arange(1, N + 1)
    PI_array = 4.0 * cum_hits / denoms
    Error_array = np.abs(math.pi - PI_array)

    c_in = np.array(hex_to_rgba(C_CYAN))
    c_out = np.array(hex_to_rgba(C_RED))
    c_hot = np.array([1.0, 1.0, 1.0, 1.0])

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        # 1. The Steam Train Acceleration Tensor
        # Starts dead slow (1 point occasionally). Quadratically explodes to 1000+ points/frame
        progress = f / TOTAL_FRAMES
        
        # Exponential curve for index. Guarantees we hit N precisely at the end frame.
        max_idx = int((progress**3.2) * N) + int(f * 0.5) 
        max_idx = np.clip(max_idx, 1, N) # Always at least 1 point to avoid DivByZero
        
        pi_est = PI_array[max_idx - 1]
        error = Error_array[max_idx - 1]

        # Slice the actively drawn dataset
        px = X_full[:max_idx].copy()
        py = Y_full[:max_idx].copy()
        m_in = mask_in_full[:max_idx]
        
        # 2. Geometric Layering & Node Sparking
        colors = np.zeros((max_idx, 4))
        colors[m_in] = c_in
        colors[~m_in] = c_out
        
        # Calculate age of each particle in the stream. (0 is brand new, high number is old)
        ages = max_idx - np.arange(max_idx)
        recent_boost = np.exp(-ages / 120.0) # The "Spark" trail
        
        # Inject Absolute White into the newest drops (Compile-Time Neon Pop)
        colors[:, 0:3] = colors[:, 0:3] * (1 - recent_boost[:, np.newaxis]) + c_hot[0:3] * recent_boost[:, np.newaxis]
        colors[:, 3] = 0.4 + (0.6 * recent_boost) # Older particles fade slightly into the matrix
        
        sizes = 1.0 + (35.0 * recent_boost)
        
        # Quick simulated machine-cycle tracker for the UI
        sys_clock = int(f * (1 + progress * 5)) # Speeds up as the machine cranks
        line_cursor = (sys_clock % 4) + 1 
        
        yield (f, t_sec, px, py, sizes, colors, pi_est, error, max_idx, line_cursor)

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER (BATCH EXECUTION)
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 148: C64 STOCHASTIC PI REVELATION [MULTICORE {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
