"""
SOVEREIGN CODE: logic_garden_179_superposition.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Many-Worlds Tensor (17.5 seconds)
SCENE: Logic Garden 179 (Quantum Superposition / Reality is a Calculation)
HOTFIX: ARRAY ROUTING MISALIGNMENT (25,200 Nodes)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_179_superposition"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_DIM     = '#1A1A24'          # Hardware Matrix / Slit Architecture
C_CYAN    = '#00FFFF'          # High-Probability Amplitude
C_MAGENTA = '#FF00FF'          # Destructive Interference (Phase Shift)
C_RED     = '#FF0033'          # The Observer (Detector / Hardware Interrupt)
C_MANTIS  = '#00FF00'          # The Compiled Reality (Post-Collapse Node)

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE QUANTUM GRID
# ------------------------------------------------------------------
# HOTFIX: Explicit mathematical parity. 140 * 180 = 25,200 nodes.
N_GRID = 25200
np.random.seed(179)

gx = np.linspace(100, 980, 140)
gy = np.linspace(720, 1850, 180)
xx, yy = np.meshgrid(gx, gy)

base_x = xx.flatten()
base_y = yy.flatten()

# Add systemic noise to break the "smooth graph" into a ragged truth
jitter_x = np.random.normal(0, 3, len(base_x))
jitter_y = np.random.normal(0, 3, len(base_y))

px_grid = base_x + jitter_x
py_grid = base_y + jitter_y

# Slit Coordinates (The Bounding Box Breach)
SLIT_1 = (440, 700)
SLIT_2 = (640, 700)

r1 = np.sqrt((px_grid - SLIT_1[0])**2 + (py_grid - SLIT_1[1])**2)
r2 = np.sqrt((px_grid - SLIT_2[0])**2 + (py_grid - SLIT_2[1])**2)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    # STRICT TUPLE PAYLOAD UNPACK
    f, t_sec, state_str, ui_col, p_y, wave_alpha, colors, detector_x, collapse_pt = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    # 1. THE DOUBLE-SLIT ARCHITECTURE (HARDWARE MEMBRANE)
    ax.plot([0, 420], [700, 700], color=C_DIM, lw=8, zorder=2)
    ax.plot([460, 620], [700, 700], color=C_DIM, lw=8, zorder=2)
    ax.plot([660, 1080], [700, 700], color=C_DIM, lw=8, zorder=2)

    # 2. PHASE 1: THE UN-CAST CALCULATION (SINGLE DOT)
    if t_sec < 4.5:
        # Pre-slit single pixel
        ax.scatter([540], [p_y], s=250, c=C_TEXT, marker='X', zorder=5)
        # Trajectory blur
        ax.plot([540, 540], [p_y-80, p_y], color=C_TEXT, lw=2, alpha=0.5, zorder=4)

    # 3. PHASE 2: THE MANY-WORLDS TENSOR (WAVE MECHANICS)
    if wave_alpha > 0.05 and collapse_pt is None:
        c_tensor = np.zeros((N_GRID, 4))
        c_tensor[:, 0:3] = colors
        # Modulate alpha based on wave propagation frame and distance
        dist_mask = np.clip(1.0 - (np.abs(py_grid - p_y) / 200.0), 0.0, 1.0)
        c_tensor[:, 3] = dist_mask * wave_alpha

        # The Visual Friction: 25,200 points rendering a ragged interference pattern
        ax.scatter(px_grid, py_grid, s=15, c=c_tensor, edgecolors='none', zorder=3)

    # 4. PHASE 3: THE OBSERVER AND COLLAPSE (TATHĀTĀ)
    if detector_x > 0:
        # The Red Sweeping Laser (Hardware Interrupt)
        ax.plot([0, detector_x], [1600, 1600], color=C_RED, lw=4, zorder=6)
        ax.plot([detector_x, detector_x], [1550, 1650], color=C_TEXT, lw=4, zorder=6)
        ax.scatter([detector_x], [1600], s=800, c=C_RED, edgecolors='none', alpha=0.4, zorder=5)

    if collapse_pt is not None:
        # The O(1) Erased Reality - Single Point Defined
        ax.scatter([collapse_pt[0]], [collapse_pt[1]], s=5000, facecolors='none', edgecolors=C_MANTIS, lw=8, alpha=0.8, zorder=7)
        ax.scatter([collapse_pt[0]], [collapse_pt[1]], s=400, c=C_MANTIS, marker='X', zorder=8)
        ax.plot([collapse_pt[0], collapse_pt[0]], [700, collapse_pt[1]], color=C_MANTIS, lw=2, linestyle=':', alpha=0.5, zorder=1)

    # 5. TELEMETRY WIDGETS
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.9))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2)
    ax.text(0.04, 0.965, "LG-179 :: QUANTUM SUPERPOSITION / MANY WORLDS", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    ax.add_patch(plt.Rectangle((0, 0), 1, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 1], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2)
    ax.text(0.04, 0.08, "DIMENSIONAL COMPILER STATUS:", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    
    pulse = ui_col if (f % 10 < 5) or ui_col == C_MANTIS else C_TEXT
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=24, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# QUANTUM PROPAGATION STREAM
# ------------------------------------------------------------------
def generate_stream():
    k = 0.06      # Wavenumber
    omega = 12.0  # Angular frequency
    
    c_cy_rgb = np.array(hex_to_rgba(C_CYAN)[0:3])
    c_mg_rgb = np.array(hex_to_rgba(C_MAGENTA)[0:3])
    c_void_rgb = np.array(hex_to_rgba(C_VOID)[0:3])

    colors = np.zeros((N_GRID, 3))

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        wave_alpha = 0.0
        detector_x = -100
        collapse_pt = None
        p_y = 100.0

        # Phase 1: Pure Mathematical Journey
        if t_sec < 4.0:
            p_y = 100 + (t_sec / 4.0) * 600
            ui_col = C_TEXT
            state = "[01] REALITY IS A CALCULATION (PRE-SLIT VECTOR)"
            
        # Phase 2: Superposition & Interference
        elif t_sec < 14.5:
            ui_col = C_CYAN
            state = "[02] MANY-WORLDS TENSOR: PROBABILITY BRANCHING"
            wave_alpha = min(1.0, (t_sec - 4.0) * 2.0) # Fade in
            
            # The calculation wavefront moves upwards
            p_y = 700 + ((t_sec - 4.0) / 10.5) * 1100 
            
            # Constructive/Destructive Interference Math
            amp = np.sin(k * r1 - omega * t_sec) + np.sin(k * r2 - omega * t_sec)
            intensity = (amp / 2.0) # Range [-1, 1]
            
            # Map [-1, 0, 1] to [Magenta, Void, Cyan]
            colors = np.where(intensity[:, None] > 0,
                              c_void_rgb + (c_cy_rgb - c_void_rgb) * intensity[:, None],
                              c_void_rgb + (c_mg_rgb - c_void_rgb) * np.abs(intensity[:, None]))

        # Phase 3: The Dimensional Compiler (Collapse)
        else:
            ui_col = C_RED
            state = "[03] OBSERVER DETECTED // HARDWARE INTERRUPT ACTIVE"
            
            # Laser scans horizontally across the screen rapidly
            scan_t = (t_sec - 14.5) / 1.0 
            detector_x = min(1080.0, scan_t * 1500)
            
            wave_alpha = max(0.0, 1.0 - scan_t*5.0) 
            p_y = 1800 
            
            if t_sec >= 15.2:
                ui_col = C_MANTIS
                detector_x = 1080.0
                state = "TATHĀTĀ: WAVE-FUNCTION COMPILED TO O(1) NODE"
                collapse_pt = (555, 1600) 

        yield (f, t_sec, state, ui_col, p_y, wave_alpha, colors, detector_x, collapse_pt)

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 179: QUANTUM SUPERPOSITION [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: 25,200 Nodes Aligned")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
