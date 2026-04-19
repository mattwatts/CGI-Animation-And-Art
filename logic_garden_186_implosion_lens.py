"""
SOVEREIGN CODE: logic_garden_186_implosion_lens.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Numpy Hydrodynamics (17.5 seconds)
SCENE: Logic Garden 186 (The Implosion Lens / Hydrodynamic Shockwave)
HOTFIX: O(N) Wavefront Arrays, Photic Phase Alignment, Neon Pop Physics
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
import multiprocessing as mp
import os
import gc
import math

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_186_implosion"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_DIM     = '#1A1A24'          # Aluminum Pusher
C_CYAN    = '#00FFFF'          # Smoothed Wavefront (Terminal Flow)
C_MAGENTA = '#FF00FF'          # Fast Explosive / Chaotic Plasma
C_GOLD    = '#FFD700'          # Natural Uranium Tamper
C_RED     = '#FF0033'          # Core / Overload
C_MANTIS  = '#00FF00'          # Criticality Achievement

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE HYDRODYNAMIC BOUNDING BOX
# ------------------------------------------------------------------
CX, CY  = 540, 960
OUTER_R = 450.0   # Casing
FAST_R  = 350.0   # Lens Outer Interface
LENS_R  = 260.0   # Lens Base Inner Interface
TAMP_R  = 160.0   # Uranium Tamper
CORE_R  = 60.0    # Plutonium Core

N_DETONATORS = 32
N_POINTS = 25000

# Base array representing the shockwave angle
theta_arr = np.linspace(0, 2*np.pi, N_POINTS)

# Generate Detonator Angles
det_angles = np.linspace(0, 2*np.pi, N_DETONATORS, endpoint=False)

# Precompute the Slow Explosive Lens Geometry (Baratol)
# Formula: Lens must be THICKEST at the detonators to slow down the leading edge of the wave.
# At theta=0 (detonator), cos(32*theta) = 1.
# Inner radius = 260 - 45*cos = 215. Thickness = 350 - 215 = 135.
# At theta=pi/32 (gap), cos = -1. Inner = 305. Thickness = 350 - 305 = 45.
lens_inner_r = LENS_R - 45.0 * np.cos(N_DETONATORS * np.linspace(0, 2*np.pi, 2000))

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, r_shock, amp_shock, noise_amp, w_color, core_rad, core_col, is_flash, p_level = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg = C_TEXT if is_flash else C_VOID
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    # 1. RENDER STRUCTURES (STATIC TOPOLOGY)
    
    # Pusher & Tamper
    ax.add_patch(Circle((CX, CY), FAST_R, facecolor=C_VOID, edgecolor=C_DIM, lw=4, zorder=1))
    ax.add_patch(Circle((CX, CY), TAMP_R, facecolor=C_VOID, edgecolor=C_GOLD, lw=4, zorder=2))
    
    # The Slow Explosive Lenses (Baratol Array)
    lens_x = CX + lens_inner_r * np.cos(np.linspace(0, 2*np.pi, 2000))
    lens_y = CY + lens_inner_r * np.sin(np.linspace(0, 2*np.pi, 2000))
    ax.fill(lens_x, lens_y, facecolor=C_VOID, edgecolor=C_DIM, lw=2, zorder=3)
    # Fill between OUTER limit and inner lens edge
    cx_outer = CX + FAST_R * np.cos(np.linspace(0, 2*np.pi, 2000))
    cy_outer = CY + FAST_R * np.sin(np.linspace(0, 2*np.pi, 2000))
    for i in range(2000-1):
        if i % 30 == 0: # Draw struts for aesthetic matrix
            ax.plot([lens_x[i], cx_outer[i]], [lens_y[i], cy_outer[i]], color=C_DIM, lw=1, alpha=0.5, zorder=2)

    # Detonators (Outer Casing)
    for ang in det_angles:
        dx, dy = CX + OUTER_R * np.cos(ang), CY + OUTER_R * np.sin(ang)
        ax.scatter([dx], [dy], s=40, c=C_MAGENTA if r_shock > 440 else C_DIM, zorder=10)
        ax.plot([CX + (OUTER_R)*np.cos(ang), CX + (OUTER_R-20)*np.cos(ang)], 
                [CY + (OUTER_R)*np.sin(ang), CY + (OUTER_R-20)*np.sin(ang)], color=C_DIM, lw=2, zorder=10)

    # 2. RENDER THE PLUTONIUM CORE
    ax.add_patch(Circle((CX, CY), core_rad, facecolor=core_col, edgecolor=C_TEXT if not is_flash else C_VOID, lw=2, zorder=5))
    if core_col != C_VOID:
        ax.scatter([CX], [CY], s=(CORE_R - core_rad)*1000, c=C_CYAN, alpha=0.3, edgecolors='none', zorder=4)

    # 3. O(N) FLUID DYNAMICS (THE HYDRODYNAMIC SHOCKWAVE)
    if r_shock < OUTER_R and not is_flash:
        # Compute exact topological shape using O(1) Numpy vector math
        # Bumps physically reverse as it goes through the lens due to differential speed.
        actual_r = r_shock + amp_shock * np.cos(N_DETONATORS * theta_arr)
        
        # Add explosive thermodynamic friction (random noise)
        plasma_noise = np.random.normal(0, noise_amp, N_POINTS)
        actual_r += plasma_noise
        
        wx = CX + actual_r * np.cos(theta_arr)
        wy = CY + actual_r * np.sin(theta_arr)
        
        ax.scatter(wx, wy, c=w_color, s=2, edgecolors='none', alpha=0.8, zorder=20)
        # Core glowing wave
        ax.plot(CX + (actual_r - np.abs(plasma_noise)*0.5) * np.cos(theta_arr), 
                CY + (actual_r - np.abs(plasma_noise)*0.5) * np.sin(theta_arr), color=C_TEXT, lw=1, alpha=0.5, zorder=21)

    # Flash Geometry Overlay
    if is_flash:
        ax.scatter([CX], [CY], s=50000, facecolors='none', edgecolors=C_MANTIS, lw=20, zorder=30)
        ax.scatter([CX], [CY], s=15000, c=C_TEXT, zorder=31)

    # 4. TELEMETRY WIDGETS (NEURAL ENTRAINMENT UI)
    ui_col = w_color if not is_flash else C_VOID
    txt_col = C_TEXT if not is_flash else C_VOID
    bg_col = C_VOID if not is_flash else C_TEXT
    
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=bg_col, alpha=0.9, zorder=40))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2, zorder=40)
    ax.text(0.04, 0.965, "LG-186 :: HYDRODYNAMIC PHASE LENSING", transform=ax.transAxes, color=txt_col, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=41)

    ax.add_patch(plt.Rectangle((0, 0), 1, 0.12, transform=ax.transAxes, color=bg_col, alpha=0.95, zorder=40))
    ax.plot([0, 1], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2, zorder=40)
    ax.text(0.04, 0.08, "WAVEFRONT ACCELERATION TENSOR:", transform=ax.transAxes, color=txt_col, fontsize=20, fontname='monospace', zorder=41)
    
    # Core Density Bar
    ax.add_patch(plt.Rectangle((0.75, 0.03), 0.20, 0.02, transform=ax.transAxes, color=C_DIM, zorder=41))
    ax.add_patch(plt.Rectangle((0.75, 0.03), 0.20 * p_level, 0.02, transform=ax.transAxes, color=ui_col, zorder=42))
    ax.text(0.75, 0.06, f"CORE DENSITY: {p_level*200:.1f}%", transform=ax.transAxes, color=txt_col, fontsize=14, fontname='monospace', zorder=41)

    pulse = C_MANTIS if (f % 10 < 5) and not is_flash else txt_col
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=24, fontname='monospace', weight='bold', zorder=41)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) KINEMATIC STREAM GENERATOR
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        r_shock = OUTER_R + 50  # Start outside
        amp_shock = 0.0
        noise_amp = 0.0
        w_color = C_DIM
        core_rad = CORE_R
        core_col = C_VOID
        is_flash = False
        p_level = 0.0

        # ---- PHASE 1: ARMING (0 - 2s) ----
        if t_sec < 2.0:
            state = "[01] INITIATING CAPACITORS :: 32-POINT ARRAY ARMED"
            r_shock = OUTER_R

        # ---- PHASE 2: CHAOTIC EXPANSION (2 - 7s) ----
        elif t_sec < 7.0:
            state = "[02] DETONATION :: DIVERGENT O(N) PLASMA WAVEFRONT"
            prog = (t_sec - 2.0) / 5.0
            r_shock = OUTER_R - (OUTER_R - FAST_R) * prog
            
            # Geometric bump grows because explosion originates from discrete points
            amp_shock = prog * 25.0 
            noise_amp = prog * 15.0 # Extreme visual friction / heat
            w_color = C_MAGENTA

        # ---- PHASE 3: THE LENS REFRACTION (7 - 12s) ----
        elif t_sec < 12.0:
            if f % 12 < 6: w_color = C_CYAN
            else: w_color = C_MAGENTA
            
            state = "[03] PHASE LENSING :: APPLYING CRITICAL DAMPING TO CHAOS"
            prog = (t_sec - 7.0) / 5.0
            r_shock = FAST_R - (FAST_R - TAMP_R) * prog
            
            # The geometry mathematically corrects itself
            # Amplitude drops from 25.0 -> 0. Noise drops from 15.0 -> 2.0
            amp_shock = 25.0 * (1.0 - prog)
            noise_amp = 15.0 * ((1.0 - prog)**2) + 2.0
            
        # ---- PHASE 4: TERMINAL COMPRESSION (12 - 14.8s) ----
        elif t_sec < 14.8:
            state = "WARNING: CORE COMPRESSION. SYMMETRY LOCKED AT 100%."
            prog = (t_sec - 12.0) / 2.8
            r_shock = TAMP_R - (TAMP_R - CORE_R * 0.4) * prog
            
            amp_shock = 0.0  # Perfect sphere
            noise_amp = 1.0  # Absolute zero friction limit
            w_color = C_CYAN
            
            if r_shock < core_rad:
                core_rad = r_shock
                p_level = prog
                core_col = C_RED if f % 4 < 2 else C_GOLD

        # ---- PHASE 5: TATHĀTĀ / THE HARDWARE INTERRUPT (14.8 - 17.5s) ----
        else:
            w_color = C_MANTIS
            core_rad = CORE_R * 0.4
            p_level = 1.0
            core_col = C_TEXT
            if t_sec < 14.95:
                is_flash = True
            state = "TATHĀTĀ: PERFECT STILLNESS EXTRACTED FROM ABSOLUTE CHAOS."

        yield (f, t_sec, state, r_shock, amp_shock, noise_amp, w_color, core_rad, core_col, is_flash, p_level)

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 186: THE IMPLOSION TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: O(N) Wavefront Vectorization & Photic Alignment")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Nodes: {N_POINTS}")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
