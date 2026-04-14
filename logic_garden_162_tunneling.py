"""
SOVEREIGN CODE: logic_garden_162_tunneling.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Quantum Wave-Function Emulation (35 seconds)
SCENE: Logic Garden 162 (Quantum Tunneling / The Sublime Breach)
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
OUT_DIR = "frames_162_tunneling"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_GOLD    = '#FFD700'          # The Bounding Box (Energy Barrier)
C_CYAN    = '#00FFFF'          # Incident Wave Function (Potential)
C_RED     = '#FF0033'          # Kinetic Friction (Decoherence)
C_PURPLE  = '#8A2BE2'          # Evanescent Wave (Exponential Decay)
C_MANTIS  = '#00FF00'          # Terminal Green Flow (The Breach)

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# QUANTUM WAVE PACKET GENERATION (COMPILE-TIME LOCK)
# ------------------------------------------------------------------
np.random.seed(162)
NUM_WAVE = 15000

# Gaussian distribution for wave packet
wx_offsets = np.random.normal(0, 150, NUM_WAVE)
wy_offsets = np.random.normal(0, 250, NUM_WAVE)
phase = np.random.uniform(0, 2*np.pi, NUM_WAVE)

# Tunneling Probability Matrix (Only 1% mathematically breach)
tunnel_mask = np.random.rand(NUM_WAVE) > 0.99 

# Static Gold Lattice (The Bounding Box)
wall_x = np.random.uniform(50, 1030, 2000)
wall_y = np.random.uniform(900, 1050, 2000)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (ISOLATED MEMORY NODE)
# ------------------------------------------------------------------
def render_frame(data_packet):
    f, t_sec, state_str, ui_col, p_x, p_y, p_c, p_s, impact_glow = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # 1. RENDER THE BOUNDING BOX (GOLD BARRIER)
    # The hardware matrix of the wall
    ax.add_patch(plt.Rectangle((0, 900), 1080, 150, color=C_GOLD, alpha=0.05, zorder=1))
    ax.scatter(wall_x, wall_y, s=5, c=C_GOLD, alpha=0.3, zorder=2)
    
    # Impact kinetic bloom
    if impact_glow > 0:
        ax.add_patch(plt.Rectangle((0, 900), 1080, 150, color=C_RED, alpha=impact_glow * 0.15, zorder=2))
        ax.plot([0, 1080], [900, 900], color=C_TEXT, lw=4, alpha=impact_glow, zorder=3)

    # 2. RENDER THE WAVE FUNCTION
    ax.scatter(p_x, p_y, s=p_s, c=p_c, marker='h', zorder=5)

    # Add core bloom to tunneled particles (Terminal Green Flow)
    mantis_mask = p_y > 1055
    if np.any(mantis_mask):
        ax.scatter(p_x[mantis_mask], p_y[mantis_mask], s=p_s[mantis_mask]*5, c=C_MANTIS, alpha=0.3, zorder=4)
        ax.scatter(p_x[mantis_mask], p_y[mantis_mask], s=p_s[mantis_mask]*20, c=C_MANTIS, alpha=0.05, zorder=3)

    # 3. TELEMETRY WIDGETS
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.9))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2)
    ax.text(0.04, 0.965, "LOGIC GARDEN 162 :: QUANTUM TUNNELING", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    # Physics Panel
    ax.text(0.04, 0.88, f"BARRIER POTENTIAL (V0): 25.0 eV", transform=ax.transAxes, color=C_GOLD, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.85, f"PARTICLE ENERGY  (E)  : 05.0 eV", transform=ax.transAxes, color=C_CYAN, fontsize=20, fontname='monospace')
    
    # Mathematical Efficacy Check
    logic_col = C_RED if t_sec < 18.0 else C_MANTIS
    logic_str = "DENIED (E < V0)" if t_sec < 18.0 else "OVERRIDE (THE SUBLIME BREACH)"
    ax.text(0.04, 0.81, f"CLASSICAL LOGIC       : {logic_str}", transform=ax.transAxes, color=logic_col, fontsize=20, fontname='monospace', weight='bold')

    # Transmission Coefficient (T)
    if t_sec > 8.0:
        ax.text(0.04, 0.72, "TRANSMISSION COEFFICIENT: T ≈ e^(-2κa)", transform=ax.transAxes, color=C_PURPLE, fontsize=18, fontname='monospace')

    # Bottom Terminal
    ax.add_patch(plt.Rectangle((0, 0), 0.95, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 0.95], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2)
    
    pulse = ui_col if (f % 60 < 30) or ui_col == C_MANTIS else C_TEXT
    ax.text(0.04, 0.08, "WAVE-FUNCTION STATE:", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=28, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf(); plt.close(fig); plt.close('all'); gc.collect() 
    return f

# ------------------------------------------------------------------
# PHYSICS ENGINE (PROBABILITY AMPLITUDE & EXPONENTIAL DECAY)
# ------------------------------------------------------------------
def generate_physics_stream():
    # Base velocity and timing
    V_Y = 130.0
    Y_START = -300.0
    
    # Calculate exact impact time for each node
    impact_times = (900.0 - (Y_START + wy_offsets)) / V_Y
    
    scatters_x = np.random.normal(0, 15, NUM_WAVE)

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        # Initialize cleanly padded arrays
        cur_x = 540 + wx_offsets.copy()
        cur_y = np.zeros(NUM_WAVE)
        cur_c = np.full((NUM_WAVE, 4), hex_to_rgba(C_CYAN, 0.7))
        cur_s = np.full(NUM_WAVE, 15.0)
        
        impact_glow = 0.0
        
        # Dynamic State UI
        if t_sec < 8.0:
            state = "[01] PROBABILITY PROPAGATION"
            ui_col = C_CYAN
        elif t_sec < 18.0:
            state = "[02] KINETIC FRICTION / DECOHERENCE"
            ui_col = C_RED
            # Glow peaks around t=10
            impact_glow = max(0.0, 1.0 - abs(t_sec - 10.0)/2.5)
        elif t_sec < 26.0:
            state = "[03] EVANESCENT PROBABILITY DECAY"
            ui_col = C_PURPLE
        else:
            state = "[04] TATHĀTĀ: SINGULAR COHERENCE"
            ui_col = C_MANTIS

        # ------------------------------------
        # MATRIX 1: The Reflecting Entropy (99%)
        # ------------------------------------
        refl_mask = ~tunnel_mask
        dt_refl = t_sec - impact_times[refl_mask]
        
        # Pre-impact (Cyan Flow) - HOTFIX APPLIED
        mask_pre_refl = refl_mask & (t_sec < impact_times)
        cur_y[mask_pre_refl] = Y_START + (t_sec * V_Y) + wy_offsets[mask_pre_refl]
        cur_x[mask_pre_refl] += np.sin(t_sec * 6 + phase[mask_pre_refl]) * 20
        
        # Post-impact (Red Friction / Scatters downwards)
        post_refl = dt_refl >= 0
        idx_post_refl = np.where(refl_mask)[0][post_refl]
        
        cur_y[idx_post_refl] = 900 - (dt_refl[post_refl] * 80.0) # Slower reflection
        cur_x[idx_post_refl] += scatters_x[idx_post_refl] * dt_refl[post_refl] # chaotic lateral spread
        cur_c[idx_post_refl] = hex_to_rgba(C_RED, 0.4)
        cur_s[idx_post_refl] = 10.0 # Shredds into smaller entropy

        # ------------------------------------
        # MATRIX 2: The Tunneled Coherence (1%)
        # ------------------------------------
        tun_mask = tunnel_mask
        dt_tun = t_sec - impact_times[tun_mask]
        
        TUNNEL_DUR = 12.0 # They spend 12 seconds creeping through the barrier
        
        # Pre-impact (Cyan Flow) - HOTFIX APPLIED (15000, Broadcast Fix)
        mask_pre_tun = tun_mask & (t_sec < impact_times)
        cur_y[mask_pre_tun] = Y_START + (t_sec * V_Y) + wy_offsets[mask_pre_tun]
        cur_x[mask_pre_tun] += np.sin(t_sec * 6 + phase[mask_pre_tun]) * 20
        
        # Inside the Bounding Box (Purple Evanescent Decay)
        in_wall = (dt_tun >= 0) & (dt_tun < TUNNEL_DUR)
        idx_in = np.where(tun_mask)[0][in_wall]
        
        prog = dt_tun[in_wall] / TUNNEL_DUR
        cur_y[idx_in] = 900 + (prog * 150) # Creeps through 150 pixel wall
        # Color changes to purple, alpha decays exponentially
        cur_c[idx_in] = hex_to_rgba(C_PURPLE, 0.8)
        cur_c[idx_in, 3] = np.clip(0.8 * np.exp(-prog * 4.0), 0.1, 0.8) 
        
        # Emergence / The Sublime Breach (Mantis Green Terminal Flow)
        out_wall = dt_tun >= TUNNEL_DUR
        idx_out = np.where(tun_mask)[0][out_wall]
        
        dt_out = dt_tun[out_wall] - TUNNEL_DUR
        # Accelerates rapidly away from the wall
        cur_y[idx_out] = 1050 + (dt_out * 80.0) + (0.5 * 150.0 * dt_out**2)
        
        # The wave instantly collapses into a perfect geometric point (X snaps to 540)
        snap = np.clip(dt_out * 3.0, 0.0, 1.0)
        cur_x[idx_out] += (540 - cur_x[idx_out]) * snap
        
        cur_c[idx_out] = hex_to_rgba(C_MANTIS, 1.0)
        cur_s[idx_out] = 40.0 # Massive geometric authority

        yield (f, t_sec, state, ui_col, cur_x, cur_y, cur_c, cur_s, impact_glow)

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 162: QUANTUM TUNNELING [CORES: {cpu_cores}]")
    print(f"Tracking Probability Matrix: {NUM_WAVE} Nodes")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
