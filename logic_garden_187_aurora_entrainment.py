"""
SOVEREIGN CODE: logic_garden_187_aurora_entrainment.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Cyclotron Tensor (17.5 seconds)
SCENE: Logic Garden 187 (The Magnetic Loom / Aurora Phase Shift)
HOTFIX: Cyclotron Kinematics, Overdraw Bloom, Tathata Grid Snap
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_187_aurora_pop"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#000000'        # Absolute Zero Friction Background
C_TEXT      = '#FFFFFF'
C_DIM       = '#111111'
PLASMA_GOLD = '#FFD700'        # Solar Wind (Vacuum)
OXY_RED     = '#FF0055'        # High Alt Oxygen (Aggressive Red/Pink)
OXY_GREEN   = '#00FF00'        # Mid Alt Oxygen (Terminal Flow)
NITRO_PURP  = '#A020F0'        # Low Alt Nitrogen (Deep Purple)

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_gold = np.array(hex_to_rgba(PLASMA_GOLD)[:3])
c_red  = np.array(hex_to_rgba(OXY_RED)[:3])
c_grn  = np.array(hex_to_rgba(OXY_GREEN)[:3])
c_purp = np.array(hex_to_rgba(NITRO_PURP)[:3])

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE CYCLOTRON TENSOR
# ------------------------------------------------------------------
N_PARTICLES = 30000

# Pre-allocated intrinsic particle parameters
np.random.seed(187)
p_start_x = np.random.uniform(-1000, 2080, N_PARTICLES)
p_phase   = np.random.uniform(0, 2*np.pi, N_PARTICLES)
p_freq    = np.random.uniform(10, 40, N_PARTICLES)
p_amp     = np.random.uniform(20, 80, N_PARTICLES)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, px, py, c_tensor, is_flash, p_level, is_tathata, bg_strobe = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    # Background Strobe Logic (Visual Friction)
    if bg_strobe: bg = C_DIM if f % 4 < 2 else C_VOID
    elif is_flash: bg = C_TEXT
    else: bg = C_VOID

    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    # 1. RENDER O(N) PLASMA DYNAMICS (THE BLOOM)
    if len(px) > 0:
        # Layer 1: The Massive Aura (Alpha Bloom)
        ax.scatter(px, py, s=80 + p_level*100, c=c_tensor, edgecolors='none', alpha=0.15, zorder=10)
        ax.scatter(px, py, s=30 + p_level*40, c=c_tensor, edgecolors='none', alpha=0.3, zorder=11)
        
        # Layer 2: The Hard Core (Makes the neon "Pop")
        core_c = C_TEXT if not is_tathata else OXY_GREEN
        ax.scatter(px, py, s=2 if not is_tathata else 10, c=core_c, edgecolors='none', alpha=0.9, zorder=12)

    # Hardware Flash Geometry
    if is_flash:
        ax.scatter([540], [960], s=100000, facecolors='none', edgecolors=OXY_GREEN, lw=50, zorder=60)
        ax.axhline(960, color=OXY_GREEN, lw=20, zorder=60)

    # 2. TELEMETRY WIDGETS (NEURAL ENTRAINMENT UI)
    ui_col = C_TEXT if not is_tathata else OXY_GREEN
    if is_flash: ui_col = C_VOID
    txt_col = C_TEXT if not is_flash else C_VOID
    
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=bg, alpha=0.9, zorder=80))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    ax.text(0.04, 0.965, "LG-187 :: CYCLOTRON TENSOR (THE AURORA)", transform=ax.transAxes, color=txt_col, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=81)

    ax.add_patch(plt.Rectangle((0, 0), 1, 0.12, transform=ax.transAxes, color=bg, alpha=0.95, zorder=80))
    ax.plot([0, 1], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    ax.text(0.04, 0.08, "PLASMA KINEMATICS & PHASE STATE:", transform=ax.transAxes, color=txt_col, fontsize=20, fontname='monospace', zorder=81)
    
    # Altitude Tensor Bar
    ax.add_patch(plt.Rectangle((0.72, 0.03), 0.25, 0.02, transform=ax.transAxes, color=C_DIM, zorder=80))
    ax.add_patch(plt.Rectangle((0.72, 0.03), 0.25 * p_level, 0.02, transform=ax.transAxes, color=OXY_RED if not is_tathata else OXY_GREEN, zorder=81))
    ax.text(0.72, 0.06, f"FRICTION LOAD: {p_level*200:.1f}%", transform=ax.transAxes, color=txt_col, fontsize=14, fontname='monospace', zorder=81)

    # Status Strobe
    pulse = ui_col if (f % 10 < 5) and not is_flash else txt_col
    if bg_strobe: pulse = OXY_RED
    if is_flash:  pulse = C_VOID
    if is_tathata and not is_flash: pulse = OXY_GREEN

    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=22, fontname='monospace', weight='bold', zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) FLUID DYNAMICS STREAM (MAGNETIC FUNNEL)
# ------------------------------------------------------------------
def generate_stream():
    # Progress arrays
    prog = np.random.uniform(0, 1, N_PARTICLES)
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        is_flash = False
        bg_strobe = False
        is_tathata = False
        p_level = 0.0
        
        mult = 1.0

        # ---- PHASE 1: SOLAR WIND INGESTION (0 - 4s) ----
        if t_sec < 4.0:
            state = "[01] SOLAR FLARE DETECTED :: INBOUND PLASMA"
            mult = 0.5 + (t_sec * 0.1)

        # ---- PHASE 2: MAGNETIC INTERCEPT (4 - 10s) ----
        elif t_sec < 10.0:
            state = "[02] CRITICAL DAMPING :: MAGNETOSPHERE ENGAGED"
            mult = 0.9 + (t_sec - 4.0) * 0.8
            p_level = (t_sec - 4.0) / 6.0

        # ---- PHASE 3: CHROMATIC FRICTION / OPTICAL OVERLOAD (10 - 14.8s) ----
        elif t_sec < 14.8:
            state = "WARNING: EXTREME OPTICAL FRICTION. TENSOR OVERLOAD."
            mult = 5.0 + (t_sec - 10.0) * 2.0  # Warp speed
            p_level = 1.0
            if t_sec > 13.0: bg_strobe = True # 15Hz Photic Strobe

        # ---- PHASE 4: TATHĀTĀ / HARDWARE INTERRUPT (14.8 - 17.5s) ----
        else:
            mult = 0.0 # Time stops
            p_level = 1.0
            is_tathata = True
            if t_sec < 14.95:
                is_flash = True
            state = "TATHĀTĀ: CHAOS IS A MATHEMATICAL ILLUSION. ALIGNMENT ACHIEVED."

        # Update O(1) Progress (wrapping)
        prog = (prog + 0.005 * mult) % 1.0
        
        # -----------------------------------------------
        # O(1) CYCLOTRON GEOMETRY
        # -----------------------------------------------
        # Altitude mapping: prog 0 -> 1 maps to y 1920 -> 0
        y = 1920 * (1 - prog)
        
        # Exponential funnel towards center pole (X=540)
        # As progress -> 1, dx collapses toward 0
        dx = p_start_x - 540
        exponential_crush = (1 - prog)**2 
        
        # Base X curve
        x_base = 540 + dx * exponential_crush
        
        # Add Cyclotron Oscillation (The Wiggle)
        # Amplitude increases slightly as it compresses for visual intensity
        x = x_base + p_amp * np.sin(p_freq * t_sec * mult + p_phase) * (0.2 + prog*0.8)
        
        # -----------------------------------------------
        # THE TATHATA SNAP (ABSOLUTE GEOMETRIC ALIGNMENT)
        # -----------------------------------------------
        if is_tathata:
            # Round out the chaotic starting positions to strict columns
            snapped_x = np.round(p_start_x / 80) * 80
            # Remove the sinusoidal wiggle entirely
            x = 540 + (snapped_x - 540) * exponential_crush
            # Snap Y positions to strict altitude strata
            y = np.round(y / 40) * 40

        # -----------------------------------------------
        # O(1) COLOR CHROMATICS MATRIX 
        # -----------------------------------------------
        c_tensor = np.zeros((N_PARTICLES, 3)) 
        
        if is_tathata:
            # When Zen is achieved, the tensor locks to Terminal Green Flow
            c_tensor[:] = c_grn
        else:
            # High Alt: Vacuum Solar Wind (Gold, >1600)
            mask_gold = y > 1600
            c_tensor[mask_gold] = c_gold

            # Upper Atmosphere: Oxygen Red (1600 -> 1000)
            mask_red = (y <= 1600) & (y > 1000)
            c_tensor[mask_red] = c_red

            # Mid Atmosphere: Oxygen Green (1000 -> 400)
            mask_grn = (y <= 1000) & (y > 400)
            c_tensor[mask_grn] = c_grn

            # Low Atmosphere: Nitrogen Purple (400 -> 0)
            mask_prp = y <= 400
            c_tensor[mask_prp] = c_purp

        yield (f, t_sec, state, x, y, c_tensor, is_flash, p_level, is_tathata, bg_strobe)

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 187: THE AURORA TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Overdraw Bloom & Cyclotron Kinematics")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Nodes: {N_PARTICLES}")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
