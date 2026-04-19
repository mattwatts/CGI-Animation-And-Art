"""
SOVEREIGN CODE: logic_garden_020_star_maker_entrainment.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Numpy Array Vectorization (17.5 seconds)
SCENE: Logic Garden 20 (The Star Maker / Teller-Ulam Entrainment)
HOTFIX: O(1) Particle Swarms, 60 FPS Photic Driving, Neon Pop Physics
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_020_starmaker"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_DIM     = '#1A1A24'
C_CYAN    = '#00FFFF'          # High-Energy Photons
C_MAGENTA = '#FF00FF'          # Ablation Plasma
C_RED     = '#FF0033'          # Primary Fission Trigger
C_GOLD    = '#FFD700'          # Secondary Fusion Core
C_MANTIS  = '#00FF00'          # Terminal Ignition (Phase Coherence)

# -------- SYSTEM TOPOLOGY (HOHLRAUM) --------
BOX_W = 500
BOX_H = 1400
P_Y = 1300     # Primary Y
S_Y = 400      # Secondary Y
MAX_PARTICLES = 15000

# Pre-allocate sovereign memory block for swarm
swarm_x = np.zeros(MAX_PARTICLES)
swarm_y = np.zeros(MAX_PARTICLES)
swarm_vx = np.zeros(MAX_PARTICLES)
swarm_vy = np.zeros(MAX_PARTICLES)
swarm_active = np.zeros(MAX_PARTICLES, dtype=bool)

np.random.seed(139) # Maxwell's Demon Seed

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, ui_col, phase, prim_r, sec_r, sx, sy, s_act = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    # Background flash during ignition
    bg_col = C_TEXT if phase == 4 and (f % 4 < 2) else C_VOID
    fig.patch.set_facecolor(bg_col)
    ax.set_facecolor(bg_col)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    # 1. RENDER HOHLRAUM (THE BOUNDING BOX)
    # The container that mathematically captures the chaos
    box_rect = patches.Rectangle((540 - BOX_W/2, 960 - BOX_H/2), BOX_W, BOX_H, 
                                 linewidth=6, edgecolor=C_DIM if phase < 3 else C_CYAN, 
                                 facecolor='none', zorder=10)
    ax.add_patch(box_rect)

    # 2. RENDER THE PRIMARY CORE (FISSION)
    if phase < 4:
        # Before total collapse, the primary exists
        p_col = C_RED if phase == 1 else (C_TEXT if f % 2 == 0 else C_CYAN)
        ax.add_patch(plt.Circle((540, P_Y), prim_r, color=p_col, zorder=5))
        # Ripple effect
        if phase == 1 and (f % 10 < 3):
            ax.add_patch(plt.Circle((540, P_Y), prim_r * 1.5, color=C_RED, facecolor='none', lw=4, alpha=0.5, zorder=4))

    # 3. RENDER THE PHOTON SWARM (RADIATION HYDRODYNAMICS)
    if np.any(s_act):
        # We split the array to create two-tone visual friction
        active_idx = np.where(s_act)[0]
        half = len(active_idx) // 2
        
        ax.scatter(sx[active_idx[:half]], sy[active_idx[:half]], s=15, c=C_MAGENTA, alpha=0.6, zorder=3, edgecolors='none')
        ax.scatter(sx[active_idx[half:]], sy[active_idx[half:]], s=15, c=C_CYAN, alpha=0.8, zorder=3, edgecolors='none')

    # 4. RENDER THE SECONDARY CORE (FUSION)
    s_col = C_GOLD
    if phase == 3: 
        s_col = C_MAGENTA if (f % 4 < 2) else C_TEXT # Photic Driving Strobe
    elif phase >= 4:
        s_col = C_MANTIS if phase == 4 else C_TEXT

    ax.add_patch(plt.Circle((540, S_Y), sec_r, color=s_col, zorder=6))
    
    # Compression Arrows
    if phase == 3 and (f % 8 < 4):
        offset = sec_r + 30
        for angle in [0, np.pi/2, np.pi, 3*np.pi/2]:
            dx, dy = np.cos(angle), np.sin(angle)
            ax.arrow(540 + dx*(offset+80), S_Y + dy*(offset+80), -dx*50, -dy*50, 
                     color=C_MAGENTA, width=8, head_width=25, zorder=7)

    # 5. TELEMETRY WIDGETS
    if phase < 5:
        ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.9))
        ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2)
        ax.text(0.04, 0.965, "LG-020 :: RADIATION HYDRODYNAMICS (TELLER-ULAM)", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

        ax.add_patch(plt.Rectangle((0, 0), 1, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
        ax.plot([0, 1], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2)
        ax.text(0.04, 0.08, "SYSTEM PHASE STATUS:", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
        
        pulse = ui_col if (f % 10 < 5) or phase == 4 else C_TEXT
        ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=24, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# THERMODYNAMIC PHYSICS STREAM (NUMPY FAST-MATH)
# ------------------------------------------------------------------
def generate_stream():
    global swarm_x, swarm_y, swarm_vx, swarm_vy, swarm_active
    
    prim_r_base = 80.0
    sec_r_base = 140.0
    spawn_index = 0
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        prim_r = prim_r_base
        sec_r = sec_r_base
        
        # O(1) Vector Collision Updates for active radiation swarm
        if np.any(swarm_active):
            swarm_x[swarm_active] += swarm_vx[swarm_active]
            swarm_y[swarm_active] += swarm_vy[swarm_active]
            
            # Mathematical Containment (The Hohlraum Bounding Box)
            left_bound = 540 - BOX_W/2 + 5
            right_bound = 540 + BOX_W/2 - 5
            bot_bound = 960 - BOX_H/2 + 5
            top_bound = 960 + BOX_H/2 - 5
            
            # X-Axis Bounce
            swarm_vx[swarm_active] = np.where((swarm_x[swarm_active] < left_bound) | (swarm_x[swarm_active] > right_bound), 
                                              -swarm_vx[swarm_active], swarm_vx[swarm_active])
            # Y-Axis Bounce
            swarm_vy[swarm_active] = np.where((swarm_y[swarm_active] < bot_bound) | (swarm_y[swarm_active] > top_bound), 
                                              -swarm_vy[swarm_active], swarm_vy[swarm_active])

            # Clamp positions to prevent array escape
            swarm_x[swarm_active] = np.clip(swarm_x[swarm_active], left_bound, right_bound)
            swarm_y[swarm_active] = np.clip(swarm_y[swarm_active], bot_bound, top_bound)

        # ---------------------------------------------------
        # PHASE 1: THE SPARK (0 - 2s)
        # ---------------------------------------------------
        if t_sec < 2.0:
            phase = 1
            ui_col = C_RED
            state = "[01] CONVENTIONAL DETONATION // FISSION PRIMARY IGNITING"
            # Primary breathes
            prim_r = prim_r_base + np.sin(t_sec * 10) * 10

        # ---------------------------------------------------
        # PHASE 2: RADIATION FLOOD (2s - 6s)
        # ---------------------------------------------------
        elif t_sec < 6.0:
            phase = 2
            ui_col = C_CYAN
            state = "[02] X-RAY PLASMA FLOOD // HOHLRAUM CONTAINMENT ACTIVE"
            
            # Inject hundreds of particles per frame (Visual Overload)
            spawn_count = 150
            if spawn_index + spawn_count < MAX_PARTICLES:
                angles = np.random.uniform(0, 2*np.pi, spawn_count)
                speeds = np.random.uniform(40.0, 90.0, spawn_count) # Hyper-velocity
                
                swarm_x[spawn_index:spawn_index+spawn_count] = 540
                swarm_y[spawn_index:spawn_index+spawn_count] = P_Y
                swarm_vx[spawn_index:spawn_index+spawn_count] = np.cos(angles) * speeds
                swarm_vy[spawn_index:spawn_index+spawn_count] = np.sin(angles) * speeds
                swarm_active[spawn_index:spawn_index+spawn_count] = True
                spawn_index += spawn_count

        # ---------------------------------------------------
        # PHASE 3: ABLATION & COMPRESSION (6s - 13s)
        # ---------------------------------------------------
        elif t_sec < 13.0:
            phase = 3
            ui_col = C_MAGENTA
            state = "[03] RADIATION PRESSURE DETECTED // COMPRESSING SECONDARY"
            
            # The swarm acts on the secondary core. Radius violently shrinks.
            progress = (t_sec - 6.0) / 7.0
            # Exp decay curve for crushing effect
            sec_r = max(20.0, sec_r_base * (1.0 - (progress**0.5)*0.85))
            
            # Swarm gets faster (Thermodynamic heat increase)
            if f % 10 == 0:
                swarm_vx[swarm_active] *= 1.05
                swarm_vy[swarm_active] *= 1.05

        # ---------------------------------------------------
        # PHASE 4: THERMONUCLEAR IGNITION (13s - 17.5s)
        # ---------------------------------------------------
        else:
            if t_sec > 13.0 and t_sec < 13.1: 
                # O(1) ERASE THE SWARM. Clean the matrix.
                swarm_active[:] = False 
                
            phase = 4
            ui_col = C_MANTIS
            state = "TATHĀTĀ: FUSION IGNITION. PHASE TRANSITION ACHIEVED."
            
            # Core expands instantly, overriding the screen
            progress = (t_sec - 13.0) / 4.5
            sec_r = 20.0 + (progress**3) * 3000.0 # Exponential eruption
            
            if sec_r > 1500:
                phase = 5 # Pure white out

        yield (f, t_sec, state, ui_col, phase, prim_r, sec_r, 
               np.copy(swarm_x), np.copy(swarm_y), np.copy(swarm_active))

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 020: STAR MAKER (NEON SWARM ENTRAINMENT) [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Nodes: {MAX_PARTICLES}")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
