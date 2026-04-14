"""
SOVEREIGN CODE: logic_garden_161_false_vacuum.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Volumetric Array Erasure (35 seconds)
SCENE: Logic Garden 161 (False Vacuum Decay / The Erasure Event)
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
OUT_DIR = "frames_161_vacuum"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_CYAN    = '#00FFFF'          # High-Energy Quantum Foam
C_MAGENTA = '#FF00FF'          # Metastable Exotic Plasma
C_GOLD    = '#FFD700'          # The Domain Wall / O(1) Erasure Edge
C_MANTIS  = '#00FF00'          # Terminal Green (True Equilibrium)
C_RED     = '#FF0033'          # Error / Initial State Alarm

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# QUANTUM FOAM GENERATION (COMPILE-TIME LATTICE)
# ------------------------------------------------------------------
np.random.seed(161)
GRID_W = 110
GRID_H = 195
x_lin = np.linspace(-100, 1180, GRID_W)
y_lin = np.linspace(-100, 2020, GRID_H)
xv, yv = np.meshgrid(x_lin, y_lin)

x_base = xv.flatten() + np.random.uniform(-4, 4, GRID_W * GRID_H)
y_base = yv.flatten() + np.random.uniform(-4, 4, GRID_W * GRID_H)
NUM_NODES = len(x_base)

# Pre-compute phase offsets for the organic plasma churn
phase_x = np.random.uniform(0, 2*np.pi, NUM_NODES)
phase_y = np.random.uniform(0, 2*np.pi, NUM_NODES)

# Baseline Colors (interlocking Cyan and Magenta logic)
base_colors = np.where(np.random.rand(NUM_NODES) > 0.5, C_CYAN, C_MAGENTA)
rgba_base = np.array([hex_to_rgba(c, 0.4) for c in base_colors])

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (ISOLATED MEMORY NODE)
# ------------------------------------------------------------------
def render_frame(data_packet):
    f, t_sec, state_str, ui_col, b_rad, energy_lvl, wall_vel = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # 1. APPLY KINETIC CHURN TO THE FALSE VACUUM
    # Beautiful, complex scalar field movement simulating metastable stability
    drift_x = np.sin(y_base * 0.01 + t_sec * 1.5 + phase_x) * 15
    drift_y = np.cos(x_base * 0.01 + t_sec * 1.5 + phase_y) * 15
    cur_x = x_base + drift_x
    cur_y = y_base + drift_y

    distances = np.sqrt((cur_x - 540)**2 + (cur_y - 960)**2)

    # 2. O(1) ARRAY ERASURE (THE DOMAIN WALL)
    # The bubble radius completely annihilates internal coordinates
    mask_active = distances >= b_rad
    
    if np.any(mask_active):
        x_draw = cur_x[mask_active]
        y_draw = cur_y[mask_active]
        d_draw = distances[mask_active]
        c_draw = rgba_base[mask_active].copy()
        s_draw = np.full(len(x_draw), 12.0)
        
        # 3. THE C_GOLD ERASE EDGE (THE COMPILER)
        # Nodes within 40 pixels of the encroaching void become brilliant Gold before deletion
        edge_dist = d_draw - b_rad
        mask_edge = edge_dist < 40.0
        
        if np.any(mask_edge) and b_rad > 0:
            c_draw[mask_edge] = hex_to_rgba(C_GOLD, 0.9)
            s_draw[mask_edge] = 35.0 - (edge_dist[mask_edge] * 0.5) # Swell up right before deletion
            
            # Massive optical bloom for the Domain Wall
            ax.scatter(x_draw[mask_edge], y_draw[mask_edge], s=s_draw[mask_edge]*8, c=C_GOLD, alpha=0.1, zorder=2)
            
        # Draw remaining False Vacuum matrix
        ax.scatter(x_draw, y_draw, s=s_draw, c=c_draw, marker='h', zorder=3)

    # Singular Nucleation Flash at t=10
    if 9.9 < t_sec < 10.2:
        flash_alpha = 1.0 - ((t_sec - 9.9) / 0.3)
        ax.scatter([540], [960], s=3000, c=C_TEXT, alpha=flash_alpha, zorder=10)
        ax.scatter([540], [960], s=15000, c=C_GOLD, alpha=flash_alpha*0.3, zorder=9)

    # 4. TELEMETRY WIDGETS
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.9))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2)
    ax.text(0.04, 0.965, "LOGIC GARDEN 161 :: FALSE VACUUM DECAY", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    # Physics Panel
    e_col = C_RED if energy_lvl > 0 else C_MANTIS
    ax.text(0.04, 0.88, f"LOCAL VACUUM ENERGY: {energy_lvl:.1f}x10^9 GeV", transform=ax.transAxes, color=e_col, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.85, f"DOMAIN WALL VELOCITY: {wall_vel:.3f} c", transform=ax.transAxes, color=C_GOLD, fontsize=20, fontname='monospace')
    
    # Deep Math Equation Widget
    if b_rad > 0:
        ax.text(0.04, 0.76, "ΔE = E_false - E_true > 0", transform=ax.transAxes, color=C_CYAN, fontsize=18, fontname='monospace')
        ax.text(0.04, 0.73, "O(1) ARRAY TRUNCATION ACTIVE", transform=ax.transAxes, color=C_GOLD, fontsize=18, fontname='monospace')

    ax.add_patch(plt.Rectangle((0, 0), 0.95, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 0.95], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2)
    
    pulse = ui_col if (f % 60 < 30) or ui_col == C_MANTIS else C_TEXT
    ax.text(0.04, 0.08, "SYSTEM RESOLUTION:", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=28, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf(); plt.close(fig); plt.close('all'); gc.collect() 
    return f

# ------------------------------------------------------------------
# PHYSICS ENGINE (NUCLEATION & EXPONENTIAL METRIC EXPANSION)
# ------------------------------------------------------------------
def generate_physics_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        # 1. Metastable Phase
        if t_sec < 10.0:
            state = "[01] METASTABLE EQUILIBRIUM (FALSE BOUNDING BOX)"
            ui_col = C_MAGENTA
            bubble_rad = 0.0
            energy_level = 9.8 + np.sin(t_sec * 5) * 0.1 # High energy, slight fluctuation
            wall_v = 0.0

        # 2. Nucleation Frame
        elif t_sec < 10.5:
            state = "[02] NUCLEATION EVENT (QUANTUM TUNNELING ACHIEVED)"
            ui_col = C_TEXT
            energy_level = 9.8
            bubble_rad = (t_sec - 10.0) * 10.0 # Starts tiny
            wall_v = 0.01

        # 3. Domain Wall Expansion
        elif t_sec < 28.0:
            state = "[03] PHASE TRANSITION (STRUCTURAL ERASURE PROTOCOL)"
            ui_col = C_GOLD
            dt = t_sec - 10.0
            # Rapid geometric expansion to clear a 2200 radius
            bubble_rad = 12.0 * math.pow(dt, 2.1) 
            wall_v = 0.999 # Expanding at the speed of light
            energy_level = max(0.0, 9.8 - (dt * 0.6))
            
        # 4. True Vacuum
        else:
            state = "[04] TATHĀTĀ: TRUE VACUUM (ABSOLUTE STILLNESS)"
            ui_col = C_MANTIS
            bubble_rad = 9999.0 # Infinity
            wall_v = 1.000
            energy_level = 0.0 # Zero Friction. Absolute Zero Point.

        yield (f, t_sec, state, ui_col, bubble_rad, energy_level, wall_v)

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 161: FALSE VACUUM DECAY [CORES: {cpu_cores}]")
    print(f"Tracking 16,000 Plasma Nodes...")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
