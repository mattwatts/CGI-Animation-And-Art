"""
SOVEREIGN CODE: logic_garden_153_rotator_zen.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Vector Physics Emulation
SCENE: Logic Garden 153 (The Equilibrium of Forces - Rotator Heavy Recovery)
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
DURATION = 30                   
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_153_rotator"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_RED     = '#FF0033'          # Entropy / The Wreck
C_GOLD    = '#FFD700'          # Tension / Active Pull
C_CYAN    = '#00FFFF'          # Big Flipper (Right Anchor)
C_MANTIS  = '#00FF00'          # Hulk 2 (Left Anchor) / Terminal Flow
C_TETHER  = '#333344'          # Slack Cable

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (ISOLATED MEMORY NODE)
# ------------------------------------------------------------------
def render_frame(data_packet):
    f, t_sec, w_x, w_y, ten_L, ten_R, damp_factor, state_str, ui_color, nodes_x, nodes_y = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # 1. THE SOVEREIGN ANCHORS (HULK 2 & BIG FLIPPER)
    # Boom Pivot Points
    pivot_L = (150, 400)   # Hulk 2 Base
    boom_L  = (350, 1500)  # Hulk 2 Sheave
    
    pivot_R = (930, 400)   # Big Flipper Base
    boom_R  = (730, 1400)  # Big Flipper Sheave

    # Draw Boom Arms
    ax.plot([pivot_L[0], boom_L[0]], [pivot_L[1], boom_L[1]], color=C_MANTIS, lw=18, alpha=0.9, solid_capstyle='round', zorder=5)
    ax.plot([pivot_L[0], boom_L[0]], [pivot_L[1], boom_L[1]], color=C_TEXT, lw=4, alpha=0.5, solid_capstyle='round', zorder=6)
    
    ax.plot([pivot_R[0], boom_R[0]], [pivot_R[1], boom_R[1]], color=C_CYAN, lw=18, alpha=0.9, solid_capstyle='round', zorder=5)
    ax.plot([pivot_R[0], boom_R[0]], [pivot_R[1], boom_R[1]], color=C_TEXT, lw=4, alpha=0.5, solid_capstyle='round', zorder=6)

    # Boom Heads
    ax.scatter([boom_L[0]], [boom_L[1]], s=800, c=C_VOID, edgecolors=C_MANTIS, lw=4, zorder=10)
    ax.scatter([boom_R[0]], [boom_R[1]], s=800, c=C_VOID, edgecolors=C_CYAN, lw=4, zorder=10)

    # 2. THE TETHERS (WIRE ROPE VECTORS)
    c_line_L = C_GOLD if ten_L > 10 else C_TETHER
    c_line_R = C_GOLD if ten_R > 10 else C_TETHER
    
    # Glow effect based on tension
    if ten_L > 10: ax.plot([boom_L[0], w_x], [boom_L[1], w_y], color=C_GOLD, lw=ten_L/5, alpha=0.3, zorder=7)
    if ten_R > 10: ax.plot([boom_R[0], w_x], [boom_R[1], w_y], color=C_GOLD, lw=ten_R/5, alpha=0.3, zorder=7)
    
    # Hard lines
    ax.plot([boom_L[0], w_x], [boom_L[1], w_y], color=c_line_L, lw=4, zorder=8)
    ax.plot([boom_R[0], w_x], [boom_R[1], w_y], color=c_line_R, lw=4, zorder=8)

    # 3. THE WRECK (ENTROPY PAYLOAD)
    # Volumetric splatting for the wreck to simulate mass and distortion
    wreck_size = 3000
    
    # Internal chaotic nodes (The structural stress)
    node_colors = np.zeros((len(nodes_x), 4))
    if ui_color == C_RED:
        rgb = hex_to_rgba(C_RED)
    elif ui_color == C_GOLD:
        rgb = hex_to_rgba(C_GOLD)
    else:
        rgb = hex_to_rgba(C_MANTIS)
        
    node_colors[:, 0:3] = rgb[0:3]
    node_colors[:, 3] = np.random.uniform(0.4, 0.9, len(nodes_x)) # Shimmer
    
    # Wreck Glow
    ax.scatter([w_x], [w_y], s=wreck_size * 2, c=ui_color, alpha=0.15, zorder=14)
    ax.scatter([w_x], [w_y], s=wreck_size, c=C_VOID, edgecolors=ui_color, lw=6, zorder=15)
    
    # Internal Nodes
    ax.scatter(nodes_x, nodes_y, s=150, c=node_colors, marker='x', zorder=16)
    ax.scatter(nodes_x, nodes_y, s=40, c=C_TEXT, zorder=17)

    # 4. CRITICAL DAMPING OVERLAY (TELEMETRY)
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.9))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_color, lw=2)
    ax.text(0.04, 0.965, "LOGIC GARDEN 153 :: THE EQUILIBRIUM OF FORCES", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    # Data Panel
    ax.text(0.04, 0.88, f"HULK 2 (LEFT) TENSION   : {ten_L:>05.1f} kN", transform=ax.transAxes, color=C_MANTIS, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.85, f"BIG FLIPPER (R) TENSION : {ten_R:>05.1f} kN", transform=ax.transAxes, color=C_CYAN, fontsize=20, fontname='monospace')
    
    # Dynamic Math Readout
    force_net = abs((ten_L * math.sin(math.pi/4)) - (ten_R * math.sin(math.pi/4)))
    ax.text(0.04, 0.81, f"F(net) VECTOR DELTA     : {max(0, force_net)*damp_factor:>05.1f} kN", transform=ax.transAxes, color=ui_color, fontsize=20, fontname='monospace')

    ax.add_patch(plt.Rectangle((0, 0), 0.95, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 0.95], [0.12, 0.12], transform=ax.transAxes, color=ui_color, lw=2)
    
    pulse = ui_color if (f % 30 < 15) else C_TEXT
    ax.text(0.04, 0.08, "SYSTEM RESOLUTION:", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=28, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf()
    plt.close(fig)
    plt.close('all')
    gc.collect() 
    return f

# ------------------------------------------------------------------
# THE PHYSICS ENGINE (CRITICALLY DAMPED PENDULUM)
# ------------------------------------------------------------------
def generate_physics_stream():
    cx, cy = 540.0, 700.0  # Target equilibrium
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        # Phase 1: Chaos & Slack (0-5s)
        if t_sec < 5.0:
            state = "[01] UNCONSTRAINED ENTROPY (SLACK)"
            ui_col = C_RED
            damp = 1.0
            wx = 680 + (np.random.rand() * 40 - 20)
            wy = 300 + (np.random.rand() * 40 - 20)
            tL, tR = 0.0, 0.0

        # Phase 2: The Lift & Pendulum Shock (5-15s)
        elif t_sec < 15.0:
            state = "[02] KINETIC EXTRACTION (HARMONIC SHOCK)"
            ui_col = C_GOLD
            phase_t = t_sec - 5.0
            
            # Violent pendulum swing transitioning up
            wx = 540 + math.sin(phase_t * 2.5) * 140 * math.exp(-phase_t * 0.05)
            wy = 300 + ( phase_t / 10.0 ) * 400  # Rising
            
            # Tension spikes wildly
            damp = 1.0
            base_t = 250.0 # ~25 tons per side
            tL = base_t + math.sin(phase_t * 2.5) * 150
            tR = base_t - math.sin(phase_t * 2.5) * 150

        # Phase 3: Critical Damping Applied (15-25s)
        elif t_sec < 25.0:
            state = "[03] CRITICAL DAMPING (TENSION EQUALIZATION)"
            ui_col = C_GOLD
            phase_t = t_sec - 15.0
            
            # Massive exponential decay of the swing (The Operators dial it in)
            wx = 540 + math.sin((10.0 * 2.5) + phase_t * 2.0) * 85 * math.exp(-phase_t * 0.4)
            wy = 700.0
            damp = math.exp(-phase_t * 0.4)
            
            base_t = 250.0
            tL = base_t + (math.sin((10.0 * 2.5) + phase_t * 2.0) * 150 * damp)
            tR = base_t - (math.sin((10.0 * 2.5) + phase_t * 2.0) * 150 * damp)

        # Phase 4: Absolute Coherence = 0 Friction (25-30s)
        else:
            state = "[04] TERMINAL GREEN FLOW (TATHĀTĀ)"
            ui_col = C_MANTIS
            wx = 540.0
            wy = 700.0
            damp = 0.0
            tL = 250.0
            tR = 250.0

        # Internal Wreck Nodes (Geometry)
        num_nodes = 12
        angles = np.linspace(0, 2*math.pi, num_nodes, endpoint=False)
        # They shake hard when damp is high, totally still at green
        shake_x = (np.random.rand(num_nodes) - 0.5) * 40 * damp
        shake_y = (np.random.rand(num_nodes) - 0.5) * 40 * damp
        
        n_x = wx + np.cos(angles) * 80 + shake_x
        n_y = wy + np.sin(angles) * 80 + shake_y
        
        yield (f, t_sec, wx, wy, tL, tR, damp, state, ui_col, n_x, n_y)

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER (BATCH EXECUTION)
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 153: THE EQUILIBRIUM OF FORCES [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=4):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
