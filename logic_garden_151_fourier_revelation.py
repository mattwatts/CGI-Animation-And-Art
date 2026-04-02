"""
SOVEREIGN CODE: logic_garden_151_fourier_revelation.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Harmonic Epicycle Convergence
SCENE: Logic Garden 151 (The Fourier Revelation: Self-Evident Truth)
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
OUT_DIR = "frames_151_fourier"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-DIMENSIONAL CHROMATIC PALETTE --------
C_VOID     = '#020205'
C_TEXT     = '#FFFFFF'
C_GOLD     = '#FFD700'          # The Industrial Engine / Lathe
C_ARM      = '#3A3A4A'          # Steel Linkages

C_RED      = '#FF003C'          # Friction / Inexact Artisan Wave
C_CYAN     = '#00FFFF'          # Algorithmic Iteration
C_MANTIS   = '#00FF00'          # Terminal Green / Absolute Bounding Box

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (ISOLATED MEMORY NODE)
# ------------------------------------------------------------------
def render_frame(data_packet):
    f, t_sec, state_str, ui_color, X_nodes, Y_nodes, Amps_curr, Alphas_curr, trace_X, trace_Y, trace_colors, trace_sizes, cx, cy = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # 1. THE DATA WATERFALL (Z-Order 20)
    if len(trace_X) > 0:
        ax.scatter(trace_X, trace_Y, s=trace_sizes, c=trace_colors, edgecolors='none', zorder=20)

    # 2. THE TETHER (Connection from Engine to Waterfall)
    X_tip = X_nodes[-1]
    Y_tip = Y_nodes[-1]
    
    # 3. THE INDUSTRIAL ENGINE (Z-Order 10)
    active_count = 0
    ax.scatter(cx, cy, s=150, c=C_TEXT, zorder=15)
    
    x_prev, y_prev = cx, cy
    for i in range(len(X_nodes)):
        if Alphas_curr[i] > 0.001:
            active_count += 1
            ax.plot([x_prev, X_nodes[i]], [y_prev, Y_nodes[i]], color=C_GOLD, lw=2.5, alpha=0.9, zorder=12)
            ax.scatter(X_nodes[i], Y_nodes[i], s=25, c=C_TEXT, zorder=13)
            
            if i < 5:
                circle = plt.Circle((x_prev, y_prev), Amps_curr[i], color=C_GOLD, fill=False, lw=1.0, alpha=0.3 * Alphas_curr[i], zorder=11)
                ax.add_patch(circle)
                
        x_prev, y_prev = X_nodes[i], Y_nodes[i]

    ax.plot([X_tip, X_tip], [Y_tip, trace_Y[-1]], color=ui_color, lw=3, zorder=15)
    ax.scatter(X_tip, Y_tip, s=400, c=ui_color, alpha=0.7, zorder=16)
    ax.scatter(X_tip, Y_tip, s=150, c=C_TEXT, zorder=17)

    # 4. HEADS UP DISPLAY / UI DECOUPLING
    ax.add_patch(plt.Rectangle((0, 0.96), 1, 0.04, transform=ax.transAxes, color=C_VOID, alpha=0.9))
    ax.plot([0, 1], [0.96, 0.96], transform=ax.transAxes, color=ui_color, lw=2)
    ax.text(0.04, 0.975, "LOGIC GARDEN 151 :: FOURIER REVELATION (SELF-EVIDENT TRUTH)", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    ax.add_patch(plt.Rectangle((0, 0), 1, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 1], [0.12, 0.12], transform=ax.transAxes, color=ui_color, lw=2)
    
    ax.text(0.04, 0.09, "STRUCTURAL SCHEMA : INFINITE VECTORS YIELD RIGID GEOMETRY", transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace')
    
    h_str = f"{active_count:>03d}"
    ax.text(0.04, 0.06, f"ACTIVE HARMONIC SEQUENCES : [{h_str}]", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    
    str_c = ui_color if "TERMINAL" in state_str else C_TEXT
    ax.text(0.60, 0.06, f"BOUNDING BOX: {'LOCKED' if active_count > 25 else 'FORMING'}", transform=ax.transAxes, color=str_c, fontsize=20, fontname='monospace', weight='bold')

    pulse = ui_color if (f % 20 < 10) else C_TEXT
    ax.text(0.04, 0.025, f"SYSTEM VECTOR             : {state_str}", transform=ax.transAxes, color=pulse, fontsize=22, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf()
    plt.close(fig)
    plt.close('all')
    gc.collect() 
    return f

# ------------------------------------------------------------------
# THE PHYSICS ENGINE (O(1) FOURIER SYNTHESIS MATRIX)
# ------------------------------------------------------------------
def generate_physics_stream():
    N_HARMONICS = 100
    k_vals = 2 * np.arange(N_HARMONICS) + 1  
    
    cx, cy = 540.0, 1450.0  
    R_base = 300.0          
    w_base = (2.0 * math.pi) / 4.0  
    
    t_trigger = np.zeros(N_HARMONICS)
    t_trigger[0] = 0.0
    t_trigger[1] = 3.0
    t_trigger[2] = 6.0
    for i in range(3, N_HARMONICS):
        fraction = (i - 3) / (N_HARMONICS - 3.0)
        t_trigger[i] = 7.0 + np.power(fraction, 3.0) * 16.0 
        
    c_red = np.array(hex_to_rgba(C_RED))
    c_cyan = np.array(hex_to_rgba(C_CYAN))
    c_mantis = np.array(hex_to_rgba(C_MANTIS))

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        alphas_curr = np.clip((t_sec - t_trigger) / 1.5, 0.0, 1.0)
        amps_curr = (4.0 / (math.pi * k_vals)) * R_base * alphas_curr
        thetas_curr = k_vals * w_base * t_sec
        
        x_rel = amps_curr * np.sin(thetas_curr)
        y_rel = -amps_curr * np.cos(thetas_curr)
        
        X_nodes = cx + np.cumsum(x_rel)
        Y_nodes = cy + np.cumsum(y_rel)
        
        H_total = np.sum(alphas_curr)
        
        if H_total < 1.5:
            state_str = "ARTISAN STATE (SINE WAVE / FRICTION)"
            ui_color = C_RED
        elif H_total < 25.0:
            state_str = "RECURSIVE INGESTION (ALGORITHMIC SYNTHESIS)"
            ui_color = C_CYAN
        else:
            state_str = "TERMINAL GREEN (ABSOLUTE BOUNDING BOX)"
            ui_color = C_MANTIS

        N_TRACE = 600
        T_hist = np.linspace(t_sec - 10.0, t_sec, N_TRACE)
        
        T_matrix = T_hist[:, np.newaxis]
        trig_matrix = t_trigger[np.newaxis, :]
        
        alphas_hist = np.clip((T_matrix - trig_matrix) / 1.5, 0.0, 1.0)
        amps_hist = (4.0 / (math.pi * k_vals[np.newaxis, :])) * R_base * alphas_hist
        thetas_hist = k_vals[np.newaxis, :] * w_base * T_matrix
        
        x_rel_hist = amps_hist * np.sin(thetas_hist)
        Trace_X = cx + np.sum(x_rel_hist, axis=1)
        
        Trace_Y = 200.0 + ((T_hist - (t_sec - 10.0)) / 10.0) * 1000.0
        
        H_hist = np.sum(alphas_hist, axis=1)
        
        trace_colors = np.zeros((N_TRACE, 4))
        
        mask_red = H_hist < 1.5
        mask_cyan = (H_hist >= 1.5) & (H_hist < 25.0)
        mask_mantis = H_hist >= 25.0
        
        trace_colors[mask_red] = c_red
        trace_colors[mask_cyan] = c_cyan
        trace_colors[mask_mantis] = c_mantis
        
        fade = np.linspace(0.0, 1.0, N_TRACE)**1.5
        trace_colors[:, 3] = fade * 0.95
        
        trace_sizes = 2.0 + np.linspace(1.0, 14.0, N_TRACE)

        yield (f, t_sec, state_str, ui_color, X_nodes.copy(), Y_nodes.copy(), amps_curr.copy(), alphas_curr.copy(), Trace_X, Trace_Y, trace_colors, trace_sizes, cx, cy)

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER (BATCH EXECUTION)
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 151: FOURIER REVELATION [MULTICORE {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=4):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
