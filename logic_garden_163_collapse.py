"""
SOVEREIGN CODE: logic_garden_163_collapse.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Wave-Function Collapse Emulation (35 seconds)
SCENE: Logic Garden 163 (The Dimensional Compiler / Double Slit Collapse)
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
OUT_DIR = "frames_163_collapse"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_WALL    = '#2A1A24'          # The Bounding Box (Barrier)
C_CYAN    = '#00FFFF'          # Superposition (Probability Waves)
C_GOLD    = '#FFD700'          # The Sovereign Node (The Observer)
C_MANTIS  = '#00FF00'          # Decohered Mass (Terminal Green Ballistics)
C_RED     = '#FF0033'          # Unused Entropy

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# QUANTUM PROBABILITY MATRIX (STATIC TOPOLOGY)
# ------------------------------------------------------------------
np.random.seed(163)

# System Architecture
SLIT_1 = 340
SLIT_2 = 740
SLIT_Y = 600
SCREEN_Y = 1500
WAVE_K = 0.15 # Wave Number for Interference Frequency
WAVE_W = 6.0  # Time evolution speed

# Background Probability Tensor Grid
gx_lin = np.linspace(0, 1080, 120)
gy_lin = np.linspace(SLIT_Y, SCREEN_Y, 120)
gx_grid, gy_grid = np.meshgrid(gx_lin, gy_lin)
gx_f = gx_grid.flatten()
gy_f = gy_grid.flatten()

# Distance tensors from both slits to grid points
dist1_f = np.sqrt((gx_f - SLIT_1)**2 + (gy_f - SLIT_Y)**2)
dist2_f = np.sqrt((gx_f - SLIT_2)**2 + (gy_f - SLIT_Y)**2)

# Particle System
MAX_PARTICLES = 1200
p_x = np.zeros(MAX_PARTICLES)
p_y = np.full(MAX_PARTICLES, -100.0) # Dead state
p_vx = np.zeros(MAX_PARTICLES)
p_vy = np.zeros(MAX_PARTICLES)
p_type = np.zeros(MAX_PARTICLES, dtype=int) # 0=Dead, 1=Cyan (Wave), 2=Mantis (Particle)

# Statistical Back-Wall Hardware
bins_w = np.zeros(108) # Cyan interference accumulation
bins_p = np.zeros(108) # Mantis ballistic accumulation

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (ISOLATED MEMORY NODE)
# ------------------------------------------------------------------
def render_frame(data_packet):
    f, t_sec, state_str, ui_col, f_grid_z, f_px, f_py, f_ptype, f_bw, f_bp, obs_rad = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # 1. RENDER HARDWARE BOUNDING BOXES
    # The Slit Barrier
    ax.fill_between([0, SLIT_1-20], [SLIT_Y-10, SLIT_Y-10], [SLIT_Y+10, SLIT_Y+10], color=C_WALL, zorder=5)
    ax.fill_between([SLIT_1+20, SLIT_2-20], [SLIT_Y-10, SLIT_Y-10], [SLIT_Y+10, SLIT_Y+10], color=C_WALL, zorder=5)
    ax.fill_between([SLIT_2+20, 1080], [SLIT_Y-10, SLIT_Y-10], [SLIT_Y+10, SLIT_Y+10], color=C_WALL, zorder=5)
    
    # The Measurement Screen
    ax.plot([0, 1080], [SCREEN_Y, SCREEN_Y], color=C_TEXT, lw=2, alpha=0.5, zorder=2)

    # 2. THE FLUID PROBABILITY TENSOR (PHASE 1)
    if obs_rad < 2000: # Matrix is erased after complete collapse
        # Calculate visibility mask (erased by the expanding Observer Shockwave)
        dist_to_obs = np.sqrt((gx_f - 540)**2 + (gy_f - SLIT_Y)**2)
        valid_mask = dist_to_obs >= obs_rad
        
        if np.any(valid_mask):
            z_valid = f_grid_z[valid_mask]
            x_valid = gx_f[valid_mask]
            y_valid = gy_f[valid_mask]
            
            # Map wave amplitude to Neon Pop Cyan
            alphas = np.clip(z_valid * 0.7, 0, 0.7)
            sizes = z_valid * 25.0
            
            c_array = np.zeros((len(x_valid), 4))
            c_array[:, 0:3] = hex_to_rgba(C_CYAN)[0:3]
            c_array[:, 3] = alphas
            
            ax.scatter(x_valid, y_valid, c=c_array, s=sizes, marker='h', zorder=1)

    # 3. THE DISCRETE PARTICLES
    mask_cyan = f_ptype == 1
    mask_mantis = f_ptype == 2
    
    if np.any(mask_cyan):
        ax.scatter(f_px[mask_cyan], f_py[mask_cyan], s=20, c=C_CYAN, zorder=3)
        # Probabilistic trail
        ax.scatter(f_px[mask_cyan], f_py[mask_cyan]-15, s=10, c=C_CYAN, alpha=0.5, zorder=3)

    if np.any(mask_mantis):
        ax.scatter(f_px[mask_mantis], f_py[mask_mantis], s=40, c=C_MANTIS, zorder=4)
        ax.scatter(f_px[mask_mantis], f_py[mask_mantis], s=150, c=C_MANTIS, alpha=0.2, zorder=3) # Heavy bloom

    # 4. THE SOVEREIGN NODE (THE OBSERVER)
    if obs_rad > 0:
        ax.scatter([540], [SLIT_Y], s=1200, c=C_GOLD, marker='D', zorder=10)
        ax.scatter([540], [SLIT_Y], s=obs_rad * 30, c=C_GOLD, alpha=max(0, 0.15 - (obs_rad/2000)*0.15), facecolors='none', edgecolors=C_GOLD, lw=4, zorder=8)
        
    # 5. BACK-WALL TELEMETRY (DATA DECOHERENCE)
    bin_edges = np.linspace(0, 1080, 108)
    # Background Wave Pattern (Frozen in time after observation)
    for i in range(108):
        h = min(200, f_bw[i] * 1.5)
        if h > 0:
            ax.fill_between([bin_edges[i], bin_edges[i]+8], [SCREEN_Y, SCREEN_Y], [SCREEN_Y+h, SCREEN_Y+h], color=C_CYAN, alpha=0.3, zorder=2)
            
    # New Ballistic Hardware Facts
    for i in range(108):
        h = min(200, f_bp[i] * 3.0)
        if h > 0:
            ax.fill_between([bin_edges[i], bin_edges[i]+10], [SCREEN_Y, SCREEN_Y], [SCREEN_Y+h, SCREEN_Y+h], color=C_MANTIS, alpha=0.9, zorder=3)

    # 6. UI OVERLAYS
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.9))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2)
    ax.text(0.04, 0.965, "LOGIC GARDEN 163 :: THE DIMENSIONAL COMPILER", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    # Physics Panel
    if t_sec < 14.0:
        func_txt = "UNDETERMINED (INTERFERENCE VISIBLE)"
        func_col = C_CYAN
    elif t_sec < 17.0:
        func_txt = "OBSERVATION EVENT (FORCING 4D FACT)"
        func_col = C_GOLD
    else:
        func_txt = "GEOMETRIC DUALITY (FINITE MASS)"
        func_col = C_MANTIS
        
    obs_txt = "OFFLINE" if t_sec < 14.0 else ("ONLINE (MEASURING)" if t_sec < 17 else "ONLINE")
    
    ax.text(0.04, 0.88, f"SOVEREIGN NODE: {obs_txt}", transform=ax.transAxes, color=C_GOLD if t_sec >= 14 else C_TEXT, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.85, f"WAVE FUNCTION : {func_txt}", transform=ax.transAxes, color=func_col, fontsize=20, fontname='monospace')
    
    ax.add_patch(plt.Rectangle((0, 0), 0.95, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 0.95], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2)
    
    pulse = ui_col if (f % 60 < 30) or ui_col == C_MANTIS else C_TEXT
    ax.text(0.04, 0.08, "SYSTEM REALITY:", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=28, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf(); plt.close(fig); plt.close('all'); gc.collect() 
    return f

# ------------------------------------------------------------------
# PHYSICS ENGINE (PROBABILITY REJECTION SAMPLING & ARRAY UPDATES)
# ------------------------------------------------------------------
def generate_physics_stream():
    global p_x, p_y, p_vx, p_vy, p_type, bins_w, bins_p
    
    dt = 1.0 / FPS
    OBS_TIME = 14.0 # Frame when observer opens
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        # Grid Computation (Phase amplitude)
        # Intensity = (sin(k*r1 - wt) + sin(k*r2 - wt))^2
        field = (np.sin(WAVE_K * dist1_f - WAVE_W * t_sec) + np.sin(WAVE_K * dist2_f - WAVE_W * t_sec))**2 / 4.0
        
        obs_rad = 0.0
        
        if t_sec < OBS_TIME:
            state = "[01] PURE POTENTIAL (SUPERPOSITION)"
            ui_col = C_CYAN
            emit_type = 1
        elif t_sec < 17.0:
            state = "[02] THE AUDIT (DIMENSIONAL COMPILATION)"
            ui_col = C_GOLD
            obs_rad = (t_sec - OBS_TIME) * 1200.0 # Rapid shockwave erasure
            emit_type = 2
        else:
            state = "[03] TATHĀTĀ: CONSCIOUSNESS DEFINES MATTER"
            ui_col = C_MANTIS
            obs_rad = 2500.0
            emit_type = 2

        # Particle Kinematics Update
        active = p_type > 0
        p_x[active] += p_vx[active] * dt
        p_y[active] += p_vy[active] * dt

        # Screen Impact Check (Decoherence)
        hit_mask = (p_y >= SCREEN_Y) & (p_type > 0)
        if np.any(hit_mask):
            hit_x = p_x[hit_mask]
            hit_types = p_type[hit_mask]
            
            for hx, ht in zip(hit_x, hit_types):
                bin_idx = int(np.clip(hx / 10, 0, 107))
                if ht == 1:
                    bins_w[bin_idx] += 1
                else:
                    bins_p[bin_idx] += 1
                    
            p_type[hit_mask] = 0 # Kill particle locally
            p_y[hit_mask] = -100

        # Emitter Array (Spawn 20 new operations per frame)
        dead_indices = np.where(p_type == 0)[0]
        spawn_count = min(20, len(dead_indices))
        
        if spawn_count > 0:
            idx = dead_indices[:spawn_count]
            p_type[idx] = emit_type
            p_y[idx] = SLIT_Y
            
            # Start randomly at Slit 1 or 2
            bases = np.where(np.random.rand(spawn_count) > 0.5, SLIT_1, SLIT_2)

            if emit_type == 1:
                # REJECTION SAMPLING: mathematically matching the probability wave grid!
                # Target anywhere on screen
                targets = np.random.uniform(100, 980, spawn_count)
                # Compute path difference to target
                L1 = np.sqrt((targets - SLIT_1)**2 + (SCREEN_Y - SLIT_Y)**2)
                L2 = np.sqrt((targets - SLIT_2)**2 + (SCREEN_Y - SLIT_Y)**2)
                delta_phase = (L1 - L2) * WAVE_K
                
                # Probability of hitting this target based on interference math
                prob = np.cos(delta_phase / 2.0)**2 
                accepted = np.random.rand(spawn_count) < prob
                
                # If rejected, fallback to straight up to prevent infinite loop
                targets = np.where(accepted, targets, bases + np.random.uniform(-5, 5, spawn_count))
                
                # Vector math
                dx = targets - bases
                dy = SCREEN_Y - SLIT_Y
                dist = np.sqrt(dx**2 + dy**2)
                speed = 250.0
                
                p_x[idx] = bases + np.random.uniform(-8, 8, spawn_count) # Add width to slit
                p_vx[idx] = (dx / dist) * speed
                p_vy[idx] = (dy / dist) * speed

            else:
                # Phase 2/3: Ballistic Newtonian Flow (Straight Lines)
                # The compiler has stripped the chaotic potential geometry
                p_x[idx] = bases + np.random.uniform(-10, 10, spawn_count)
                p_vx[idx] = np.random.normal(0, 5) # Tiny noise, structurally rigid
                p_vy[idx] = 400.0 # Moves much faster as rigid mass
                
                # Instantly cull any ancient Cyan particles that were floating
                p_type[(p_type == 1)] = 0 

        # Yield Data Frame Copies
        yield (f, t_sec, state, ui_col, field.copy(), p_x.copy(), p_y.copy(), p_type.copy(), bins_w.copy(), bins_p.copy(), obs_rad)

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 163: THE DIMENSIONAL COMPILER [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
