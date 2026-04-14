"""
SOVEREIGN CODE: logic_garden_171_phase_decomposition.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Fluid Tensor Fields (35 seconds)
SCENE: Logic Garden 171 (Phase Decomposition / The Vibrating Matrix)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.colors import hsv_to_rgb
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 35                   
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_171_phase_decomposition"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE & STRUCTURE --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_DIM     = '#1A1A24'

# Hardware Matrix
N_NODES = 20000
np.random.seed(171)

# Generate a rigid, mathematical matrix starting grid
grid_side_x = 100
grid_side_y = 200
gx = np.linspace(80, 1000, grid_side_x)
gy = np.linspace(250, 1650, grid_side_y)
xg, yg = np.meshgrid(gx, gy)

b_x = xg.flatten()[:N_NODES]
b_y = yg.flatten()[:N_NODES]

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (ISOLATED MEMORY NODE)
# ------------------------------------------------------------------
def render_frame(data_packet):
    # HOTFIX: Memory Payload tightly aligned with Physics Generator output
    f, t_sec, state_str, ui_col, px, py, colors, cohesion_val, vibr_freq = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # 1. RENDER THE FLUID TENSOR FIELD
    # Core illumination (Text)
    ax.scatter(px, py, s=1.5, c=C_TEXT, alpha=0.9, zorder=3, edgecolors='none')
    # Optical realistic spectral bloom via HSV phase mapping
    ax.scatter(px, py, s=18, c=colors, alpha=0.4, zorder=2, edgecolors='none')
    ax.scatter(px, py, s=60, c=colors, alpha=0.08, zorder=1, edgecolors='none')

    # 2. HARDWARE BOUNDING BOXES 
    ax.add_patch(Rectangle((40, 200), 1000, 1500, fill=False, edgecolor=C_DIM, lw=2, zorder=0))

    # 3. TELEMETRY WIDGETS
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2)
    ax.text(0.04, 0.965, "LOGIC GARDEN 171 :: PHASE DECOMPOSITION", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    # Status Panel
    ax.text(0.04, 0.90, f"COGNITIVE BOUNDARY COHESION:", transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace')
    ax.text(0.04, 0.88, f"[{cohesion_val:>03.0f}%] STRUCTURAL INTEGRITY", transform=ax.transAxes, color=ui_col, fontsize=22, fontname='monospace', weight='bold')
    
    ax.text(0.60, 0.90, f"TENSOR RESONANCE:", transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace')
    ax.text(0.60, 0.88, f"{vibr_freq:>05.1f} Hz", transform=ax.transAxes, color='#FF00FF' if vibr_freq > 30 else ui_col, fontsize=22, fontname='monospace', weight='bold')

    # Bottom Terminal
    ax.add_patch(plt.Rectangle((0, 0), 0.95, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 0.95], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2)
    
    pulse = ui_col if (f % 60 < 30) or ui_col == ui_col else C_TEXT
    ax.text(0.04, 0.08, "DIMENSIONAL COMPILER STATUS:", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=26, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf(); plt.close(fig); plt.close('all'); gc.collect() 
    return f

# ------------------------------------------------------------------
# PHYSICS ENGINE (FLUID VECTOR KINEMATICS)
# ------------------------------------------------------------------
def generate_physics_stream():
    # Real-time state arrays
    px = np.copy(b_x)
    py = np.copy(b_y)
    
    dt = 1.0 / FPS

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        # ---------------------------------------------------
        # THE FLUID MATHEMATICS (PROTOCOL: PSYCHEDELIA)
        # ---------------------------------------------------
        melt_factor = np.clip((t_sec - 6.0) / 8.0, 0.0, 1.0)
        cohesion = (1.0 - melt_factor) * 100.0
        
        if t_sec < 6.0:
            state = "[01] STRUCTURAL RIGIDITY DECAYING"
            ui_col = '#00FFFF' # System is trying to maintain Cyan boxes
            vibr_amp = np.clip(t_sec * 1.5, 0, 5)
            vibr_freq = 15.0 + (t_sec * 5.0)
            
        elif t_sec < 25.0:
            state = "[02] MELTING MATRICES (FLUID PHASE)"
            ui_col = '#FF00FF' # Transition to Magenta fluidity
            vibr_amp = 5.0 - (melt_factor * 3.0) 
            vibr_freq = 45.0 - (melt_factor * 20.0)
            
        else:
            state = "[03] TATHĀTĀ: EVERYTHING IS UNIFIED FRICTION"
            ui_col = '#00FF00' # Terminal Flow
            vibr_amp = 2.0
            vibr_freq = 25.0

        # Vector Field Deformation Math
        k_scale = 0.004
        
        vx = np.sin(py * k_scale + t_sec * 1.2) * 50.0 * melt_factor + np.sin(px * 0.01) * 10.0
        vy = np.cos(px * k_scale * 1.1 + t_sec * 0.9) * 50.0 * melt_factor + np.cos(py * 0.01) * 10.0
        
        # Apply fluid velocities
        px += vx * dt
        py += vy * dt
        
        # Jitter injection
        jitter_x = np.sin(np.arange(N_NODES) + t_sec * vibr_freq) * vibr_amp
        jitter_y = np.cos(np.arange(N_NODES) + t_sec * vibr_freq * 1.1) * vibr_amp
        
        # Calculate visual positions (Physics base + Jitter injection)
        final_x = px + jitter_x
        final_y = py + jitter_y
        
        # HOTFIX: Wrapping Bounds corrected to perfectly restrict native arrays
        px = np.where(px > 1030, 50, px)
        px = np.where(px < 50, 1030, px)
        py = np.where(py > 1690, 210, py)
        py = np.where(py < 210, 1690, py) # Restored py routing

        # ---------------------------------------------------
        # HSV COLOR MAPPING (THE INCREDIBLE REALISM)
        # ---------------------------------------------------
        hue = (final_x * 0.002 + final_y * 0.003 + t_sec * 0.2) % 1.0
        sat = np.full(N_NODES, 0.9)   # Max saturation for Neon Pop
        val = np.full(N_NODES, 1.0)   # Max value
        
        hsv_arr = np.stack([hue, sat, val], axis=-1)
        rgb_arr = hsv_to_rgb(hsv_arr)
        color_rgba = np.ones((N_NODES, 4))
        color_rgba[:, 0:3] = rgb_arr

        # ALIGNMENT CORE: Ensure 9-item tuple matches render_frame payload expectation strictly
        yield (f, t_sec, state, ui_col, final_x.copy(), final_y.copy(), color_rgba, cohesion, vibr_freq)

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 171: PHASE DECOMPOSITION [CORES: {cpu_cores}]")
    print(f"Tracking Cognitive Topologies: {N_NODES} Structural Nodes.")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
