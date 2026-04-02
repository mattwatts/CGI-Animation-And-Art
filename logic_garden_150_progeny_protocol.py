"""
SOVEREIGN CODE: logic_garden_150_progeny_protocol.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Dual-Body Spacetime Lattice
SCENE: Logic Garden 150 (Artemis II: The Progeny Protocol / Free Return)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
import os
import multiprocessing as mp
import gc
from scipy.interpolate import interp1d

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 36                   
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_150_progeny"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-DIMENSIONAL CHROMATIC PALETTE --------
C_VOID     = '#020205'
C_TEXT     = '#FFFFFF'
C_GRID_BG  = '#10002b'          # Deep Space Void
C_GRID_E   = '#00FFFF'          # Deep Azure Earth Gravity
C_GRID_M   = '#FF00FF'          # Magenta Lunar Gravity

C_EARTH    = '#0033aa'          # Earth Mass Core
C_MOON     = '#11111a'          # Lunar Mass Core

C_ORION    = '#00FFCC'          # The Spacecraft (Payload)
C_BURN     = '#FFD700'          # Gold (Trans-Lunar Injection Thrust)
C_MANTIS   = '#00FF00'          # Terminal Green (Free-Return Flow)

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (ISOLATED MEMORY NODE)
# ------------------------------------------------------------------
def render_frame(data_packet):
    f, t_sec, ox_trail, oy_trail, v_current, state_str, burn_factor, cxE, cyE, cxM, cyM, grid_x, grid_y, grid_c, grid_s = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # 1. THE DUAL-BODY SPACETIME LATTICE
    ax.scatter(grid_x, grid_y, s=grid_s, c=grid_c, edgecolors='none', zorder=1)

    # 2. THE GRAVITY ANCHORS
    ax.add_patch(plt.Circle((cxE, cyE), 160.0, color=C_EARTH, zorder=10))
    ax.add_patch(plt.Circle((cxE, cyE), 160.0, color=C_GRID_E, fill=False, lw=3, alpha=0.5, zorder=11))
    ax.text(cxE, cyE, "THE ORIGIN", color=C_GRID_E, ha='center', va='center', fontsize=20, fontname='monospace', weight='bold', alpha=0.8)

    ax.add_patch(plt.Circle((cxM, cyM), 120.0, color=C_MOON, zorder=10))
    ax.add_patch(plt.Circle((cxM, cyM), 120.0, color=C_GRID_M, fill=False, lw=2, alpha=0.5, zorder=11))
    ax.text(cxM, cyM, "THE LUNAR\nANCHOR", color=C_GRID_M, ha='center', va='center', fontsize=14, fontname='monospace', alpha=0.8)

    # 3. THE PROGENY SHIP & TRAIL
    if len(ox_trail) > 0:
        current_x = ox_trail[-1]
        current_y = oy_trail[-1]
        trail_len = len(ox_trail)
        
        if trail_len > 1:
            alphas = np.linspace(0.0, 1.0, trail_len)**2.0
            sizes = np.linspace(1.0, 14.0, trail_len)
            
            if "FLOW" in state_str:
                tc = hex_to_rgba(C_MANTIS, 1.0)
                ship_color = C_MANTIS
            elif burn_factor > 0.0:
                tc = hex_to_rgba(C_BURN, 1.0)
                ship_color = C_ORION
            else:
                tc = hex_to_rgba(C_ORION, 1.0)
                ship_color = C_ORION
                
            trail_colors = np.zeros((trail_len, 4))
            trail_colors[:, 0:3] = tc[0:3]
            trail_colors[:, 3] = alphas * 0.8  
            
            ax.scatter(ox_trail, oy_trail, s=sizes, c=trail_colors, edgecolors='none', zorder=20)
        else:
            ship_color = C_ORION

        # TLI Engine Flare
        if burn_factor > 0.0:
            ax.scatter(current_x, current_y, s=8000 * burn_factor, c=C_BURN, alpha=0.15 * burn_factor, zorder=19)
            ax.scatter(current_x, current_y, s=3000 * burn_factor, c=C_BURN, alpha=0.4 * burn_factor, zorder=20)
            
        ax.scatter(current_x, current_y, s=150, c=C_TEXT, zorder=25)
        ax.scatter(current_x, current_y, s=500, c=ship_color, alpha=0.9, zorder=24)

    # 4. HEADS UP DISPLAY / UI DECOUPLING
    ui_color = C_BURN if burn_factor > 0 else (C_MANTIS if "FLOW" in state_str else C_ORION)
    
    ax.add_patch(plt.Rectangle((0, 0.96), 1, 0.04, transform=ax.transAxes, color=C_VOID, alpha=0.9))
    ax.plot([0, 1], [0.96, 0.96], transform=ax.transAxes, color=ui_color, lw=2)
    ax.text(0.04, 0.975, "LOGIC GARDEN 150 :: THE PROGENY PROTOCOL (ARTEMIS II)", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    ax.add_patch(plt.Rectangle((0, 0), 0.95, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 0.95], [0.12, 0.12], transform=ax.transAxes, color=ui_color, lw=2)
    ax.text(0.04, 0.09, "STRUCTURAL SCHEMA : HYBRID FREE-RETURN TRAJECTORY", transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace')
    
    ax.text(0.04, 0.06, f"RELATIVE VELOCITY : {v_current:>05.2f} km/s", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    
    if burn_factor > 0:
        ax.text(0.55, 0.06, f"TLI BURN : [OVERRIDE ACTIVE]", transform=ax.transAxes, color=C_BURN, fontsize=20, fontname='monospace', weight='bold')
    else:
        ax.text(0.55, 0.06, f"TLI BURN : [0.00 kN]", transform=ax.transAxes, color=ui_color, fontsize=20, fontname='monospace')

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
# THE PHYSICS ENGINE (ORBITAL FIGURE-8 SPLINE)
# ------------------------------------------------------------------
def generate_physics_stream():
    cx_E, cy_E = 540.0, 480.0
    cx_M, cy_M = 540.0, 1440.0
    
    time_nodes = np.array([0.0, 0.15, 0.35, 0.50, 0.70, 0.85, 1.0])
    
    x_nodes = np.array([
        cx_E,                  
        cx_E + 220,            
        cx_E + 250,            
        cx_M + 200,            
        cx_M - 200,            
        cx_E - 250,            
        cx_E                   
    ])
    
    y_nodes = np.array([
        cy_E - 220,            
        cy_E,                  
        cy_E + 350,            
        cy_M,                  
        cy_M,                  
        cy_E + 350,            
        cy_E + 160             
    ])
    
    t_points = np.linspace(0.0, 1.0, len(time_nodes))
    spline_x = interp1d(t_points, x_nodes, kind='cubic')
    spline_y = interp1d(t_points, y_nodes, kind='cubic')
    
    Ox = np.zeros(TOTAL_FRAMES)
    Oy = np.zeros(TOTAL_FRAMES)
    V  = np.zeros(TOTAL_FRAMES)
    States = []
    Burns = np.zeros(TOTAL_FRAMES)
    
    for f in range(TOTAL_FRAMES):
        tn = f / TOTAL_FRAMES
        
        Ox[f] = spline_x(tn)
        Oy[f] = spline_y(tn)
        
        if f > 0:
            dx = Ox[f] - Ox[f-1]
            dy = Oy[f] - Oy[f-1]
            V[f] = np.sqrt(dx**2 + dy**2) * 1.5 
        else:
            V[f] = 8.0
            
        if tn < 0.15:
            States.append("COMPILE-TIME SETUP (HIGH EARTH ORBIT)")
            Burns[f] = 0.0
        elif tn < 0.25:
            States.append("THE PROGENY INJECTION (TLI BURN)")
            burn_mag = math.sin(((tn - 0.15) / 0.10) * math.pi)
            Burns[f] = burn_mag
        elif tn < 0.60:
            States.append("BALLISTIC COAST (GRAVITY ASCENSION)")
            Burns[f] = 0.0
        else:
            States.append("TERMINAL GREEN FLOW (FREE RETURN SLING)")
            Burns[f] = 0.0

    V = [np.mean(V[max(0, i-5):min(TOTAL_FRAMES, i+5)]) for i in range(TOTAL_FRAMES)]

    gx = np.linspace(-100, 1180, 50)
    gy = np.linspace(-100, 2020, 60)
    GX, GY = np.meshgrid(gx, gy)
    base_grid = np.vstack([GX.ravel(), GY.ravel()]).T

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        trail_len = min(f + 1, 150)
        ox_trail = Ox[max(0, f - trail_len + 1) : f + 1][:].copy()
        oy_trail = Oy[max(0, f - trail_len + 1) : f + 1][:].copy()
        
        d_E = np.linalg.norm(base_grid - np.array([cx_E, cy_E]), axis=1)
        d_E_clamped = np.clip(d_E, 140.0, 5000.0) 
        pull_E = 30000.0 / (d_E_clamped**1.3)
        
        d_M = np.linalg.norm(base_grid - np.array([cx_M, cy_M]), axis=1)
        d_M_clamped = np.clip(d_M, 110.0, 5000.0) 
        pull_M = 15000.0 / (d_M_clamped**1.3)
        
        dx_E = (cx_E - base_grid[:,0])
        dy_E = (cy_E - base_grid[:,1])
        len_E = np.sqrt(dx_E**2 + dy_E**2) + 1e-6
        
        dx_M = (cx_M - base_grid[:,0])
        dy_M = (cy_M - base_grid[:,1])
        len_M = np.sqrt(dx_M**2 + dy_M**2) + 1e-6
        
        warped_x = base_grid[:,0] + (dx_E / len_E) * pull_E + (dx_M / len_M) * pull_M
        warped_y = base_grid[:,1] + (dy_E / len_E) * pull_E + (dy_M / len_M) * pull_M
        
        # -------------------------------------------------------------
        # HOTFIX: THE TENSOR CLIPPING PROTOCOL
        # -------------------------------------------------------------
        strain_E = np.clip(pull_E / 30.0, 0.0, 1.0)
        strain_M = np.clip(pull_M / 30.0, 0.0, 1.0)
        strain_sum = strain_E + strain_M 
        strain_Total = np.clip(strain_sum, 0.0, 1.0)
        
        c_bg = np.array(hex_to_rgba(C_GRID_BG))
        c_high_E = np.array(hex_to_rgba(C_GRID_E))
        c_high_M = np.array(hex_to_rgba(C_GRID_M))
        
        # We divide by true sum (strain_sum) instead of the clamped Total to prevent RGB stacking > 1.0
        mix_color = (strain_E[:, np.newaxis] * c_high_E + strain_M[:, np.newaxis] * c_high_M) / (strain_sum[:, np.newaxis] + 1e-6)
        
        grid_colors = (1.0 - strain_Total[:, np.newaxis]) * c_bg + strain_Total[:, np.newaxis] * mix_color
        grid_colors[:, 3] = 0.3 + (0.6 * strain_Total) 
        
        # Absolute Bounding Box for the compiler lock
        grid_colors = np.clip(grid_colors, 0.0, 1.0)
        
        grid_sizes = 2.0 + (12.0 * strain_Total)
        
        yield (f, t_sec, ox_trail, oy_trail, V[f], States[f], Burns[f], cx_E, cy_E, cx_M, cy_M, warped_x.copy(), warped_y.copy(), grid_colors, grid_sizes)

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER (BATCH EXECUTION)
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 150: THE PROGENY PROTOCOL [HOTFIXED] [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=4):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
