"""
SOVEREIGN CODE: logic_garden_158_three_body.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / N-Body Vector Physics (40 seconds)
SCENE: Logic Garden 158 (The Three-Body Problem / Deterministic Chaos)
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
DURATION = 40                   
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_158_threebody"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_RED     = '#FF0033'          # Systemic Entropy / Fracture
C_GOLD    = '#FFD700'          # The Interloper (N+1)
C_CYAN    = '#00FFFF'          # Object A
C_PURPLE  = '#8A2BE2'          # Object B
C_MANTIS  = '#00FF00'          # Terminal Green Harmony (Binary State)

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (ISOLATED MEMORY NODE)
# ------------------------------------------------------------------
def render_frame(data_packet):
    f, t_sec, state_str, ui_col, p_data, hist_x, hist_y, lyapunov = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # Dyn-Cam: Find barycenter to keep the chaotic swarm centered
    bary_x = np.mean(p_data[:, 0])
    bary_y = np.mean(p_data[:, 1])
    offset_x = 540 - bary_x
    offset_y = 960 - bary_y

    base_colors = [C_CYAN, C_PURPLE, C_GOLD] if t_sec > 9.0 else [C_MANTIS, C_MANTIS, C_VOID]

    # 1. RENDER KINETIC TAILS (HISTORY ARRAYS)
    tail_length = 300 # 5 seconds of trail
    for i in range(3):
        if len(hist_x[i]) > 1:
            tx = np.array(hist_x[i][-tail_length:]) + offset_x
            ty = np.array(hist_y[i][-tail_length:]) + offset_y
            
            # Fade alphas out linearly
            alphas = np.linspace(0.0, 0.8, len(tx))
            # Color transition during breach
            t_col = base_colors[i]
            if t_sec < 9.0 and i == 2:
                t_col = C_VOID # Hide interloper tail until breach
                
            ax.scatter(tx, ty, c=t_col, s=8, alpha=alphas, zorder=2)
            
            # Connecting line for exact path rendering (Compile-Time structural rigidity)
            ax.plot(tx, ty, c=t_col, lw=1.5, alpha=0.3, zorder=1)

    # 2. RENDER THE PRIMARY NEURAL NODES (3-BODIES)
    for i in range(3):
        px = p_data[i, 0] + offset_x
        py = p_data[i, 1] + offset_y
        
        n_col = base_colors[i]
        n_alpha = 1.0 if (i < 2 or t_sec > 6.0) else 0.0 # Ghost interloper in phase 1
        
        if n_alpha > 0:
            # Core
            ax.scatter(px, py, c=C_TEXT, s=150, zorder=6)
            # Inner Bloom
            ax.scatter(px, py, c=n_col, s=600, alpha=0.6, zorder=5)
            # Outer Neon Pop
            ax.scatter(px, py, c=n_col, s=2500, alpha=0.15, zorder=4)

    # 3. TELEMETRY & CRITICAL DAMPING OVERLAY (NEON POP)
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.9))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2)
    ax.text(0.04, 0.965, "LOGIC GARDEN 158 :: THE THREE-BODY PROBLEM", transform=ax.transAxes, color=C_TEXT, fontsize=22, fontname='monospace', weight='bold', va='center')

    # Data Panel
    system_entropy = "0.000 (ABSOLUTE)" if t_sec < 9.0 else "MAXIMUM (UNBOUND)"
    ent_col = C_MANTIS if t_sec < 9.0 else C_RED
    
    ax.text(0.04, 0.88, f"SYSTEM ENTROPY (ΔS): {system_entropy}", transform=ax.transAxes, color=ent_col, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.85, f"LYAPUNOV EXPONENT  : +{lyapunov:>05.3f} λ", transform=ax.transAxes, color=C_GOLD, fontsize=20, fontname='monospace')
    
    var_state = "N = 2 (BINARY)" if t_sec < 9.0 else "N = 3 (TRINARY)"
    ax.text(0.04, 0.82, f"SYSTEM VARIABLES   : {var_state}", transform=ax.transAxes, color=C_CYAN, fontsize=20, fontname='monospace')

    ax.add_patch(plt.Rectangle((0, 0), 0.95, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 0.95], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2)
    
    pulse = ui_col if (f % 30 < 15) or ui_col == C_MANTIS else C_TEXT
    ax.text(0.04, 0.08, "BOUNDING BOX STATUS:", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=26, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf(); plt.close(fig); plt.close('all'); gc.collect() 
    return f

# ------------------------------------------------------------------
# PHYSICS ENGINE (N-BODY GRAV-MATRIX & DIFFERENTIAL INTEGRATION)
# ------------------------------------------------------------------
def generate_physics_stream():
    # Physics parameters
    G = 15000.0   
    dt = (1.0 / FPS) / 20  # 20 fine sub-steps per frame for absolute precision
    
    m = np.array([100.0, 100.0, 60.0]) # Mass of 3 bodies
    
    # Perfectly calculated binary orbit for 1 and 2
    # F = G * m1 * m2 / r^2. v = sqrt(F * radius / m)
    p = np.array([
        [-150.0, 0.0],
        [150.0, 0.0],
        [30.0, -2800.0]  # Interloper starts deep in the void
    ])
    v = np.array([
        [0.0, 50.0],
        [0.0, -50.0],
        [-4.5, 300.0]    # Interloper velocity vector (slight angle for asymmetrical chaos)
    ])
    
    hist_x = [[], [], []]
    hist_y = [[], [], []]
    
    lyapunov = 0.0
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        # Euler Integration sub-steps
        for _ in range(20):
            acc = np.zeros((3, 2))
            for i in range(3):
                # Before 9s, the interloper's gravity is strictly suppressed to maintain perfect binary simulation
                if t_sec < 9.0 and i == 2:
                    continue
                    
                for j in range(3):
                    if i == j: continue
                    if t_sec < 9.0 and j == 2: continue # Ignore interloper mass early on
                    
                    dp = p[j] - p[i]
                    dist2 = np.sum(dp**2)
                    dist = np.sqrt(dist2)
                    
                    # Gravity scalar (with slight softening to prevent infinite singularity explosions)
                    f_mag = (G * m[j]) / (dist2 + 200.0) 
                    acc[i] += f_mag * (dp / dist)
                    
            v += acc * dt
            p += v * dt
            
            # Central anchor to prevent system flying infinitely off-screen during extreme chaos
            if t_sec >= 9.0:
                p -= p * 0.0003

        # Record history for trailing renders
        for i in range(3):
            hist_x[i].append(p[i, 0])
            hist_y[i].append(p[i, 1])

        # Logical State Management
        if t_sec < 7.0:
            state = "[01] TERMINAL GREEN HARMONY (PREDICTABLE)"
            ui_col = C_MANTIS
            lyapunov = 0.0
        elif t_sec < 9.0:
            state = "[02] INTERLOPER INJECTION (BREACH DETECTED)"
            ui_col = C_GOLD
            lyapunov = (t_sec - 7.0) * 0.5 # Begins rising
        elif t_sec < 20.0:
            state = "[03] DETERMINISTIC CHAOS (BOUNDING BOX FAILED)"
            ui_col = C_RED
            lyapunov = 1.0 + (t_sec - 9.0) * 1.5 
        else:
            state = "[04] MAXIMUM ENTROPY / SYSTEM DECOHERENCE"
            ui_col = C_RED
            lyapunov = 17.5 + np.sin(t_sec * 5) * 2.0

        # Yield copy of arrays so multiprocessing doesn't encounter reference mutation errors
        yield (f, t_sec, state, ui_col, p.copy(), [list(hx) for hx in hist_x], [list(hy) for hy in hist_y], lyapunov)

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 158: THE THREE-BODY PROBLEM [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
