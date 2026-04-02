"""
SOVEREIGN CODE: logic_garden_146_artemis_in_frame.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Topological Gravity Distortion
SCENE: Logic Garden 146 (Artemis Mission: Strict Bound Trajectory)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
import os
import multiprocessing as mp
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 30                   # 30-Second Phase Transition
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_146_artemis_bound"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-DIMENSIONAL CHROMATIC PALETTE --------
C_VOID     = '#020205'
C_TEXT     = '#FFFFFF'
C_GRID_BG  = '#1A0040'          # Deep Space Purple (Zero Deformation)
C_GRID_HI  = '#4cc9f0'          # Cyan Spacetime Torsion (Gravity Well)

C_ORION    = '#00FFCC'          # The Spacecraft (High Voltage Cyan)
C_BURN     = '#FFD700'          # Gold (Kinetic Friction / Thrust)
C_MANTIS   = '#00FF00'          # Terminal Green (Perfect Orbital Flow)
C_MOON     = '#11111A'          # The Gravity Anchor

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (ISOLATED MEMORY NODE)
# ------------------------------------------------------------------
def render_frame(data_packet):
    f, t_sec, ox_trail, oy_trail, v_current, state_str, burn_factor, cx, cy, grid_x, grid_y, grid_c, grid_s = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    # Absolute strict Bounding Box mapping
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # 1. THE SPACETIME LATTICE
    ax.scatter(grid_x, grid_y, s=grid_s, c=grid_c, edgecolors='none', zorder=1)

    # 2. THE LUNAR ANCHOR (Strict Center Frame)
    moon_radius = 160.0
    moon_circle = plt.Circle((cx, cy), moon_radius, color=C_MOON, zorder=10)
    moon_edge = plt.Circle((cx, cy), moon_radius, color=C_GRID_HI, fill=False, lw=2, alpha=0.5, zorder=11)
    ax.add_patch(moon_circle)
    ax.add_patch(moon_edge)
    ax.text(cx, cy, "LUNAR MASS", color=C_GRID_HI, ha='center', va='center', fontsize=20, fontname='monospace', alpha=0.6)

    # 3. THE ORION SHIP & TRAIL
    if len(ox_trail) > 0:
        current_x = ox_trail[-1]
        current_y = oy_trail[-1]
        trail_len = len(ox_trail)
        
        if trail_len > 1:
            alphas = np.linspace(0.0, 1.0, trail_len)**2.0
            sizes = np.linspace(1.0, 14.0, trail_len) # Thick bold trail
            
            if burn_factor == 0.0 and state_str == "ORBITAL COHERENCE (TERMINAL FLOW)":
                tc = hex_to_rgba(C_MANTIS, 1.0)
                ship_color = C_MANTIS
            else:
                tc = hex_to_rgba(C_BURN, 1.0)
                ship_color = C_ORION
                
            trail_colors = np.zeros((trail_len, 4))
            trail_colors[:, 0:3] = tc[0:3]
            trail_colors[:, 3] = alphas * 0.8  
            
            ax.scatter(ox_trail, oy_trail, s=sizes, c=trail_colors, edgecolors='none', zorder=20)
            
        else:
            ship_color = C_ORION

        # Burn Flare (Neon Pop Layering)
        if burn_factor > 0.0:
            ax.scatter(current_x, current_y, s=6000 * burn_factor, c=C_BURN, alpha=0.15 * burn_factor, zorder=19)
            ax.scatter(current_x, current_y, s=2000 * burn_factor, c=C_BURN, alpha=0.4 * burn_factor, zorder=20)
            
        # Hard Center Ship Target
        ax.scatter(current_x, current_y, s=150, c=C_TEXT, zorder=25)
        ax.scatter(current_x, current_y, s=500, c=ship_color, alpha=0.8, zorder=24)

    # 4. HEADS UP DISPLAY / UI DECOUPLING
    ui_color = C_BURN if burn_factor > 0 or "COAST" in state_str else C_MANTIS
    
    ax.add_patch(plt.Rectangle((0, 0.96), 1, 0.04, transform=ax.transAxes, color=C_VOID, alpha=0.9))
    ax.plot([0, 1], [0.96, 0.96], transform=ax.transAxes, color=ui_color, lw=2)
    ax.text(0.04, 0.975, "LOGIC GARDEN 146 :: THE ARTEMIS TRAJECTORY", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    ax.add_patch(plt.Rectangle((0, 0), 1, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 1], [0.12, 0.12], transform=ax.transAxes, color=ui_color, lw=2)
    ax.text(0.04, 0.09, "STRUCTURAL SCHEMA : WITHIN-BOUND TOPOLOGICAL CAPTURE", transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace')
    
    ax.text(0.04, 0.06, f"RELATIVE VELOCITY : {v_current:>05.2f} km/s", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    
    if burn_factor > 0:
        ax.text(0.55, 0.06, f"RETRO-BURN : [CRITICAL DAMPING]", transform=ax.transAxes, color=C_BURN, fontsize=20, fontname='monospace', weight='bold')
    else:
        status_c = C_MANTIS if "GREEN" in state_str else C_GRID_HI
        ax.text(0.55, 0.06, f"RETRO-BURN : [0.00 kN]", transform=ax.transAxes, color=status_c, fontsize=20, fontname='monospace')

    pulse = ui_color if (f % 30 < 15) else C_TEXT
    ax.text(0.04, 0.025, f"SYSTEM VECTOR     : {state_str}", transform=ax.transAxes, color=pulse, fontsize=22, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf()
    plt.close(fig)
    plt.close('all')
    gc.collect() 
    return f

# ------------------------------------------------------------------
# THE PHYSICS ENGINE (ORBITAL & TOPOLOGICAL CALCULATION)
# ------------------------------------------------------------------
def generate_physics_stream():
    # Moon strictly at frame centroid to guarantee bounding symmetry
    cx, cy = 540.0, 960.0
    r_orbit = 230.0
    
    Ox = np.zeros(TOTAL_FRAMES)
    Oy = np.zeros(TOTAL_FRAMES)
    V  = np.zeros(TOTAL_FRAMES)
    States = []
    Burns = np.zeros(TOTAL_FRAMES)
    
    for f in range(TOTAL_FRAMES):
        tn = f / TOTAL_FRAMES
        
        # Phase 1: Trans-Lunar Coast (Swoops from bounded Top-Right)
        if tn < 0.45:
            e_t = tn / 0.45
            
            # Starts precisely at r=850, allowing x/y vectors to clear 1080 bounds completely
            r = 850.0 - (850.0 - 450.0) * (e_t**1.4)
            # Starts at 72 degrees (Top Right), arcs down perfectly to 0 degrees (Right)
            angle = 0.4 * math.pi - (0.4 * math.pi * (e_t**1.5))
            
            V[f] = 11.2 - (8 * e_t) 
            States.append("TRANS-LUNAR COAST (GRAVITY FALL)")
            Burns[f] = 0.0
            
        # Phase 2: LOI Burn - Critical Damping (Sweeping the bottom of the moon)
        elif tn < 0.70:
            e_t = (tn - 0.45) / 0.25
            
            # Compresses exactly down to the circular orbit ring
            r = 450.0 - ((450.0 - r_orbit) * math.sin(e_t * math.pi/2))
            # Sweeps from 0 degrees (Right) around to the back (144 degrees / -0.8pi)
            angle = 0.0 - (0.8 * math.pi * e_t)
            
            V[f] = 3.2 - (1.6 * e_t)
            States.append("LUNAR ORBIT INSERTION (CRITICAL DAMPING)")
            Burns[f] = math.sin(e_t * math.pi) # Engine pulses 0 -> 1 -> 0
            
        # Phase 3: Tathātā / Absolute Flow / Terminal Green
        else:
            e_t = (tn - 0.70) / 0.30
            r = r_orbit
            # Smoothly completes the revolution
            angle = -0.8 * math.pi - (1.2 * math.pi * e_t) 
            
            V[f] = 1.6 
            States.append("ORBITAL COHERENCE (TERMINAL FLOW)")
            Burns[f] = 0.0
            
        Ox[f] = cx + r * math.cos(angle)
        Oy[f] = cy + r * math.sin(angle)

    # Pre-Generate the Space-Time Geometry Grid (2500 Voxel Nodes)
    gx = np.linspace(-100, 1180, 50)
    gy = np.linspace(-100, 2020, 75)
    GX, GY = np.meshgrid(gx, gy)
    base_grid = np.vstack([GX.ravel(), GY.ravel()]).T

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        trail_len = min(f + 1, 120)
        ox_trail = Ox[max(0, f - trail_len + 1) : f + 1][:].copy()
        oy_trail = Oy[max(0, f - trail_len + 1) : f + 1][:].copy()
        
        # -------------------------------------------------------------
        # SPACETIME TORSION EQUATION (Warping Grid)
        # -------------------------------------------------------------
        d_moon = np.linalg.norm(base_grid - np.array([cx, cy]), axis=1)
        d_moon_clamped = np.clip(d_moon, 165.0, 5000.0) 
        
        pull_str = 35000.0 / (d_moon_clamped**1.3)
        
        dx = (cx - base_grid[:,0])
        dy = (cy - base_grid[:,1])
        len_d = np.sqrt(dx**2 + dy**2) + 1e-6
        
        warped_x = base_grid[:,0] + (dx / len_d) * pull_str
        warped_y = base_grid[:,1] + (dy / len_d) * pull_str
        
        strain = np.clip(pull_str / 40.0, 0.0, 1.0)
        
        c_p = np.array(hex_to_rgba(C_GRID_BG))
        c_h = np.array(hex_to_rgba(C_GRID_HI))
        
        grid_colors = np.zeros((base_grid.shape[0], 4))
        grid_colors = (1.0 - strain[:, np.newaxis]) * c_p + strain[:, np.newaxis] * c_h
        grid_colors[:, 3] = 0.4 + (0.5 * strain) 
        
        grid_sizes = 2.0 + (12.0 * strain)
        
        yield (f, t_sec, ox_trail, oy_trail, V[f], States[f], Burns[f], cx, cy, warped_x.copy(), warped_y.copy(), grid_colors, grid_sizes)

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER (BATCH EXECUTION)
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 146: ARTEMIS STRICT-BOUND TRAJECTORY [MULTICORE {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=4):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
