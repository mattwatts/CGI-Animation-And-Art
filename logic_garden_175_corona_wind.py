"""
SOVEREIGN CODE: logic_garden_175_corona_wind.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Electrostatic Scalar Fields (35 seconds)
SCENE: Logic Garden 175 (The 3M Forcefield / Electrohydrodynamic Crystallization)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.colors import hsv_to_rgb
import multiprocessing as mp
import os
import gc
import math

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 35                   
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_175_corona_wind"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_DIM     = '#1A1A24'          # Air Matrix (The Void)
C_CYAN    = '#00FFFF'          # High-Speed Polypropylene Film Matrix
C_MAGENTA = '#FF00FF'          # Electrostatic Pressure Gradient
C_GOLD    = '#FFD700'          # 200kV/ft Invisible Bounding Box
C_MANTIS  = '#00FF00'          # Biological Node (Worker) Normal State
C_RED     = '#FF0033'          # Structural Resistance / Friction

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY & MATHEMATICAL SPACE
# ------------------------------------------------------------------
N_GRID = 15000
np.random.seed(175)

# The Void (Air Matrix) Grid representing the corridor
gx = np.linspace(250, 1000, 100)
gy = np.linspace(200, 1700, 150)
xx, yy = np.meshgrid(gx, gy)
base_x = xx.flatten()
base_y = yy.flatten()

# Particulates (Flies, dust, conductive debris)
N_PARTICLES = 300
part_x = np.random.uniform(500, 900, N_PARTICLES)
part_y = np.random.uniform(200, 1700, N_PARTICLES)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (ISOLATED MEMORY NODE)
# ------------------------------------------------------------------
def render_frame(data_packet):
    # STRICT TUPLE PAYLOAD
    f, t_sec, state_str, ui_col, f_x, f_y, f_c, stat_kV, w_x, w_y, w_col, p_x, p_y = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # 1. RENDER POLYPROPYLENE FILM TENSION (THE VELOCITY MATRIX)
    ax.add_patch(Rectangle((100, 0), 100, 1920, fill=True, color=hex_to_rgba(C_CYAN, 0.1), zorder=1))
    
    # Film speed lines (blur effect)
    offset = (t_sec * 3000) % 1920
    for y_line in range(0, 2000, 100):
        y_pos = (y_line - offset) % 1920
        ax.plot([100, 200], [y_pos, y_pos], color=C_CYAN, lw=2, alpha=0.6, zorder=2)
        ax.plot([150, 150], [y_pos, y_pos+50], color=C_TEXT, lw=4, alpha=0.8, zorder=2)

    # 2. THE ELECTROSTATIC SCALAR FIELD (THE INVISIBLE WALL)
    ax.scatter(f_x, f_y, s=12, c=f_c, edgecolors='none', zorder=3)
    ax.scatter(f_x, f_y, s=1, c=C_DIM, alpha=0.5, edgecolors='none', zorder=4)

    # 3. KINETIC PARTICULATES (CONDUCTIVE DEBRIS)
    ax.scatter(p_x, p_y, s=15, c=C_RED, marker='x', alpha=0.8, zorder=5)

    # 4. THE BIOLOGICAL NODE (THE WORKER)
    ax.scatter([w_x], [w_y], s=400, color=w_col, marker='s', zorder=7)
    ax.scatter([w_x], [w_y], s=1200, facecolors='none', edgecolors=w_col, lw=3, alpha=0.5, zorder=6)

    # 5. WALL VISUALIZATION (THE ISO-SURFACE)
    if stat_kV > 50:
        # Draw the critical 200kV bounding box stress line at X ~ 380
        ax.plot([380, 380], [200, 1700], color=C_GOLD, lw=2, linestyle='--', alpha=min((stat_kV-50)/150.0, 0.8), zorder=5)

    # 6. TELEMETRY WIDGETS
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.9))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2)
    ax.text(0.04, 0.965, "LOGIC GARDEN 175 :: E-HYDRODYNAMIC CRYSTALLIZATION", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    # Sensor Panel
    ax.text(0.04, 0.88, f"AMBIENT ELECTROSTATIC CHARGE:", transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace')
    ax.text(0.04, 0.85, f"[{stat_kV:>06.1f} kV/ft]", transform=ax.transAxes, color=C_MAGENTA if stat_kV > 100 else C_CYAN, fontsize=26, fontname='monospace', weight='bold')

    dist_to_film = w_x - 200
    ax.text(0.04, 0.80, f"BIOLOGICAL NODE DISTANCE: {dist_to_film:>04.0f} cm", transform=ax.transAxes, color=w_col, fontsize=20, fontname='monospace')

    # Bottom Terminal
    ax.add_patch(plt.Rectangle((0, 0), 0.95, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 0.95], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2)
    
    pulse = ui_col if (f % 60 < 30) or ui_col == C_RED else C_TEXT
    ax.text(0.04, 0.08, "SPATIAL ARCHITECTURE:", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=24, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf(); plt.close(fig); plt.close('all'); gc.collect() 
    return f

# ------------------------------------------------------------------
# PHYSICS ENGINE (SCALAR FIELD KINEMATICS)
# ------------------------------------------------------------------
def generate_physics_stream():
    curr_w_x, curr_w_y = 900.0, 950.0
    px = part_x.copy()
    py = part_y.copy()

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        # ---------------------------------------------------
        # PHASE 1: INDUSTRIAL ACCUMULATION (0 - 10s)
        # ---------------------------------------------------
        if t_sec < 8.0:
            stat_kV = (t_sec / 8.0) * 200.0
            state = "[01] UNGROUNDED FILM VELOCITY (CHARGE CUMULATION)"
            ui_col = C_CYAN
            w_col = C_MANTIS
            
        # ---------------------------------------------------
        # PHASE 2: PENETRATION ATTEMPT (THE INVISIBLE WALL)
        # ---------------------------------------------------
        elif t_sec < 25.0:
            stat_kV = 200.0 + math.sin(t_sec * 10) * 5.0
            state = "[02] ELECTROHYDRODYNAMIC BOUNDING BOX ACTIVE"
            ui_col = C_GOLD
            
            # Base attempt speed: 40px/sec 
            intent_x = curr_w_x - (40.0 * (1.0/FPS))
            
            # Friction equation (The Wall at ~X=380)
            resistance = max(0, 20000.0 / ((intent_x - 300)**2)) 
            if resistance > 1.0: resistance = 1.0
            
            actual_speed = 40.0 * (1.0 - resistance)
            curr_w_x -= actual_speed * (1.0/FPS)
            
            stress_ratio = np.clip(resistance, 0.0, 1.0)
            if stress_ratio > 0.8: w_col = C_RED
            else: w_col = C_GOLD
            
            if resistance > 0.95:
                state = "[02] ASYMPTOTIC STOPPAGE / TANGIBLE AIR"

        # ---------------------------------------------------
        # PHASE 3: TATHĀTĀ (THE RETREAT)
        # ---------------------------------------------------
        else:
            stat_kV = 200.0 + math.sin(t_sec * 10) * 5.0
            state = "[03] TATHĀTĀ: FRICTION CRYSTALLIZES INTO ARCHITECTURE"
            ui_col = C_MAGENTA
            w_col = C_RED
            curr_w_x += 15.0 * (1.0/FPS)

        # ---------------------------------------------------
        # MATRIX DEFORMATION MATH (THE INVISIBLE WALL)
        # ---------------------------------------------------
        film_x = 200.0
        dx_base = base_x - film_x
        pressure = (stat_kV * 80.0) / (dx_base + 1.0) 
        
        dist_to_worker = np.sqrt((base_x - curr_w_x)**2 + (base_y - curr_w_y)**2)
        worker_push = np.where(dist_to_worker < 200, (200 - dist_to_worker) * 0.5, 0.0)
        
        field_x = base_x + pressure - worker_push
        field_y = base_y
        
        # ---------------------------------------------------
        # HSV COLOR MAPPING FOR PRESSURE DENSITY
        # ---------------------------------------------------
        displacement = np.abs(field_x - base_x)
        norm_disp = np.clip(displacement / 150.0, 0.0, 1.0)
        
        # HOTFIX: Pure continuous vector math. No shape mismatches.
        hue = 0.83 - (norm_disp * 0.7) 
        hue = np.where(hue < 0, hue + 1.0, hue)
        
        sat = np.clip(norm_disp * 2.0, 0.5, 1.0)
        val = np.clip(norm_disp * 3.0, 0.2, 1.0)
        
        hsv_arr = np.stack([hue, sat, val], axis=-1)
        rgb_arr = hsv_to_rgb(hsv_arr)
        f_colors = np.ones((N_GRID, 4))
        f_colors[:, 0:3] = rgb_arr
        f_colors[:, 3] = np.clip(norm_disp + 0.1, 0.1, 1.0) 

        # ---------------------------------------------------
        # KINETIC DEBRIS RIPPED INTO THE FIELD
        # ---------------------------------------------------
        p_speed = stat_kV * 2.0
        px -= p_speed * (1.0/FPS)
        px = np.where(px < 200, np.random.uniform(900, 1050, N_PARTICLES), px)
        py = np.where(px < 200, np.random.uniform(200, 1700, N_PARTICLES), py)

        yield (f, t_sec, state, ui_col, field_x, field_y, f_colors, stat_kV, curr_w_x, curr_w_y, w_col, px.copy(), py.copy())

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 175: THE 3M ANOMALY (E-HD WALL) [CORES: {cpu_cores}]")
    print(f"Tracking 15,000 Air Matrix Nodes & Electrostatic Potentials.")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
