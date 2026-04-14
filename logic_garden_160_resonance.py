"""
SOVEREIGN CODE: logic_garden_160_resonance.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Aeroelastic Physics Emulation (40 seconds)
SCENE: Logic Garden 160 (Structural Resonance / Tacoma Narrows Decoherence)
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
DURATION = 40                   
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_160_resonance"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_CYAN    = '#00FFFF'          # Stable Structure / Laminar Wind
C_GOLD    = '#FFD700'          # Harmonic Amplification (Stress)
C_RED     = '#FF0033'          # Structural Decoherence (Fracture)
C_MANTIS  = '#00FF00'          # Terminal Green (Control Variable)

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# STRUCTURAL LATTICE GENERATION (COMPILE-TIME LOCK)
# ------------------------------------------------------------------
np.random.seed(160)
NUM_SEGMENTS = 100
BRIDGE_LEN = 800.0
BRIDGE_WID = 120.0

# Base rest positions (1D length mapping)
x_base = np.linspace(-BRIDGE_LEN/2, BRIDGE_LEN/2, NUM_SEGMENTS)

# Wind Particles (Laminar Flow)
NUM_WIND = 300
w_x = np.random.uniform(-500, 1500, NUM_WIND)
w_y = np.random.uniform(-400, 400, NUM_WIND)
w_z = np.random.uniform(-200, 200, NUM_WIND)

# Ballistic Shatter Matrix (Pre-compiled triggers for T >= 28s)
SHATTER_TIME = 28.0
# The exact phase shift at T = 28s
shatter_phase = SHATTER_TIME * 4.0
shatter_envelope = math.exp((SHATTER_TIME - 10.0) * 0.25)
# Base positions at shatter
shatter_z_left  = shatter_envelope * np.sin(np.pi * (x_base + BRIDGE_LEN/2) / BRIDGE_LEN) * np.cos(shatter_phase)
shatter_z_right = -shatter_z_left

# Explosive vectors
v_explode_x = np.random.uniform(-150, 150, (2, NUM_SEGMENTS))
v_explode_y = np.random.uniform(-100, 100, (2, NUM_SEGMENTS))
v_explode_z = np.random.uniform(200, 600, (2, NUM_SEGMENTS)) # Violent upward twist snap

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (ISOLATED MEMORY NODE)
# ------------------------------------------------------------------
def render_frame(data_packet):
    f, t_sec, state_str, ui_col, env_amp, proj_L, proj_R, is_shattered, wind_data = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # 1. RENDER WIND FLUX (LAMINAR TO CHAOTIC)
    wx, wy = wind_data
    wind_alphas = np.where(wx > 1080 - 100, 0.0, np.where(wx < 100, 0.0, 0.3))
    # Wind turns Gold/Red as it injects destructive energy
    wind_color = C_CYAN if env_amp < 10 else (C_GOLD if env_amp < 50 else C_RED)
    ax.scatter(wx, wy, c=wind_color, s=8, alpha=wind_alphas, zorder=1)

    xl, yl = proj_L[0], proj_L[1]
    xr, yr = proj_R[0], proj_R[1]

    # 2. RENDER THE HARDWARE LATTICE
    if not is_shattered:
        # Intact Structural Matrix
        struct_col = C_CYAN if env_amp < 15 else (C_GOLD if env_amp < 60 else C_RED)
        
        # Parallel Deck Lines
        ax.plot(xl, yl, c=struct_col, lw=4, zorder=3)
        ax.plot(xr, yr, c=struct_col, lw=4, zorder=3)
        
        # Struts (Zig-Zag truss geometry)
        for i in range(NUM_SEGMENTS - 1):
            if i % 2 == 0:
                ax.plot([xl[i], xr[i+1]], [yl[i], yr[i+1]], c=struct_col, lw=1.5, alpha=0.6, zorder=2)
            else:
                ax.plot([xr[i], xl[i+1]], [yr[i], yl[i+1]], c=struct_col, lw=1.5, alpha=0.6, zorder=2)
                
        # Nodes
        ax.scatter(xl, yl, s=15, c=C_TEXT, zorder=4)
        ax.scatter(xr, yr, s=15, c=C_TEXT, zorder=4)
        
        # Center constraint line (The Bounding Box anchor attempt)
        cx = (xl + xr) / 2
        cy = (yl + yr) / 2
        ax.plot(cx, cy, c=C_TEXT, lw=1, alpha=0.3, zorder=2)
        
    else:
        # Shattered Entropy (Free Falling Particles)
        ax.scatter(xl, yl, s=25, c=C_RED, marker='x', alpha=0.8, zorder=4)
        ax.scatter(xr, yr, s=25, c=C_RED, marker='x', alpha=0.8, zorder=4)
        
        # Draw broken struts scattering
        for i in range(NUM_SEGMENTS - 1):
            if i % 3 == 0:
                ax.plot([xl[i], xl[i]+(xr[i]-xl[i])*0.2], [yl[i], yl[i]+(yr[i]-yl[i])*0.2], c=C_RED, lw=2, alpha=0.5, zorder=2)

    # 3. TELEMETRY WIDGETS
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.9))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2)
    ax.text(0.04, 0.965, "LOGIC GARDEN 160 :: STRUCTURAL RESONANCE", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    # Physics Panel
    k_friction = "0.000 μ (UNDAMPED)"
    ax.text(0.04, 0.88, f"CRITICAL DAMPING : {k_friction}", transform=ax.transAxes, color=C_RED, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.85, f"WIND VELOCITY    : {42.5 + env_amp*0.1:>05.1f} m/s", transform=ax.transAxes, color=C_CYAN, fontsize=20, fontname='monospace')
    
    # Mathematical Efficacy Check
    amp_str = f"MAX (FRACTURE!)" if is_shattered else f"{env_amp:>06.2f} Δz"
    amp_col = C_RED if env_amp > 60 else (C_GOLD if env_amp > 15 else C_CYAN)
    ax.text(0.04, 0.80, f"TORSIONAL SHEAR  : {amp_str}", transform=ax.transAxes, color=amp_col, fontsize=22, fontname='monospace', weight='bold')

    # Bottom Terminal
    ax.add_patch(plt.Rectangle((0, 0), 0.95, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 0.95], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2)
    
    pulse = ui_col if (f % 60 < 30) or is_shattered else C_TEXT
    ax.text(0.04, 0.08, "SYSTEM STATUS:", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=28, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf(); plt.close(fig); plt.close('all'); gc.collect() 
    return f

# ------------------------------------------------------------------
# PHYSICS ENGINE (AEROELASTIC DIFFERENTIAL CALCULATIONS)
# ------------------------------------------------------------------
def get_isometric_projection(x, y, z):
    # Map 3D coordinates to the 2D plane for 1080x1920
    # X axis runs horizontal, Y axis acts as depth, Z is vertical
    px = 540 + x + (y * 0.5)
    py = 960 + (y * 0.3) + z
    return px, py

def generate_physics_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        # 1. Wind Kinematics (Flowing left to right)
        curr_wx = (w_x + (t_sec * 600)) % 1500 - 200
        # Wind buffets up and down with the torsional frequency
        curr_wy = w_y + np.sin(curr_wx * 0.01) * 30 + np.sin(t_sec * 4.0) * 50
        
        wx_proj, wy_proj = get_isometric_projection(curr_wx, curr_wy, w_z)

        # 2. Structural Torsion & Decay Phases
        if t_sec < 10.0:
            state = "[01] LAMINAR FLOW (TERMINAL GREEN HARDWARE)"
            ui_col = C_CYAN
            env_amp = (t_sec / 10.0) * 5.0 # Gentle flutter
            is_shattered = False
            
            phase = t_sec * 4.0
            z_left  = env_amp * np.sin(np.pi * (x_base + BRIDGE_LEN/2) / BRIDGE_LEN) * np.cos(phase)
            z_right = -z_left
            
            y_left = np.full(NUM_SEGMENTS, -BRIDGE_WID/2)
            y_right = np.full(NUM_SEGMENTS, BRIDGE_WID/2)
            
            pL = get_isometric_projection(x_base, y_left, z_left)
            pR = get_isometric_projection(x_base, y_right, z_right)

        elif t_sec < SHATTER_TIME: # Up to 28s
            state = "[02] AEROELASTIC FLUTTER (UNDAMPED RESONANCE)"
            ui_col = C_GOLD
            # Exponential amplification of energy
            env_amp = 5.0 + math.exp((t_sec - 10.0) * 0.25)
            is_shattered = False
            
            if env_amp > 60.0:
                state = "[03] CRITICAL UNDAMPED HARMONIC (BOUNDING BOX FAILING)"
                ui_col = C_RED
            
            phase = t_sec * 4.0
            # A torsional standing wave
            z_left  = env_amp * np.sin(np.pi * (x_base + BRIDGE_LEN/2) / BRIDGE_LEN) * np.cos(phase)
            # Center of deck holds, edges twist violently
            z_right = -z_left
            
            # The deck natively narrows slightly under extreme torsion
            twist_pull = np.abs(z_left) * 0.1
            y_left = np.full(NUM_SEGMENTS, -BRIDGE_WID/2) + twist_pull
            y_right = np.full(NUM_SEGMENTS, BRIDGE_WID/2) - twist_pull
            
            pL = get_isometric_projection(x_base, y_left, z_left)
            pR = get_isometric_projection(x_base, y_right, z_right)
            
        else:
            state = "[04] STRUCTURAL DECOHERENCE (MAXIMUM ENTROPY)"
            ui_col = C_RED
            is_shattered = True
            env_amp = 999.99
            
            dt = t_sec - SHATTER_TIME
            # Ballistic trajectory based on failure velocity
            GRAVITY = -800.0
            
            # Left Nodes trajectory
            cur_x_L = x_base + (v_explode_x[0] * dt)
            cur_y_L = np.full(NUM_SEGMENTS, -BRIDGE_WID/2) + (v_explode_y[0] * dt)
            cur_z_L = shatter_z_left + (v_explode_z[0] * dt) + (0.5 * GRAVITY * dt**2)
            
            # Right Nodes trajectory
            cur_x_R = x_base + (v_explode_x[1] * dt)
            cur_y_R = np.full(NUM_SEGMENTS, BRIDGE_WID/2) + (v_explode_y[1] * dt)
            cur_z_R = shatter_z_right + (v_explode_z[1] * dt) + (0.5 * GRAVITY * dt**2)

            pL = get_isometric_projection(cur_x_L, cur_y_L, cur_z_L)
            pR = get_isometric_projection(cur_x_R, cur_y_R, cur_z_R)

        yield (f, t_sec, state, ui_col, env_amp, pL, pR, is_shattered, (wx_proj, wy_proj))

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 160: STRUCTURAL RESONANCE [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=12):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
