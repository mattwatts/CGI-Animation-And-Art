"""
SOVEREIGN CODE: logic_garden_185_thermo_membrane.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(N) Numpy Fluid Sim (17.5 seconds)
SCENE: Logic Garden 185 (The Thermodynamic Membrane / PWR Entrainment)
HOTFIX: Closed-Loop Vector Squircles, Heat-Exchange Kinematics
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_185_thermo"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_DIM     = '#1A1A24'
C_CYAN    = '#00FFFF'          # Cold Water / Radiator Return
C_MAGENTA = '#FF00FF'          # Pressurized Membrane Transfer
C_GOLD    = '#FFD700'          # Superheated Steam
C_RED     = '#FF0033'          # Fission Core / Apocalyptic Heat
C_MANTIS  = '#00FF00'          # Terminal Work / Output UI

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# THE GEOMETRIC BOUNDING BOXES & KINEMATICS
# ------------------------------------------------------------------
N_PARTICLES = 15000 # Per loop (30k total)

# SQUIRCLE ARCHITECTURE (Superellipse n=0.2)
PRI_CX, PRI_CY = 320, 900
SEC_CX, SEC_CY = 760, 900
RAD_X, RAD_Y = 180, 500

MEMBRANE_LEFT = PRI_CX + RAD_X
MEMBRANE_RIGHT = SEC_CX - RAD_X

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, px, py, p_cols, sx, sy, s_cols, turb_angle, mult, is_flash, p_press, s_press = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg = C_TEXT if is_flash else C_VOID
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    # 1. RENDER STRUCTURES (BOUNDING BOXES)
    
    # The Heat Exchanger (The Membrane)
    ex_bottom = PRI_CY - RAD_Y + 100
    ex_top = PRI_CY + RAD_Y - 100
    ax.add_patch(Rectangle((MEMBRANE_LEFT - 40, ex_bottom), 80 + (MEMBRANE_RIGHT - MEMBRANE_LEFT), ex_top - ex_bottom, 
                 facecolor=C_VOID if not is_flash else C_TEXT, edgecolor=C_DIM if not is_flash else C_VOID, lw=6, zorder=1))
    
    # Hash lines representing titanium membrane plates
    for y in np.linspace(ex_bottom + 20, ex_top - 20, 25):
        ax.plot([MEMBRANE_LEFT - 10, MEMBRANE_RIGHT + 10], [y, y], color=C_DIM, lw=2, zorder=1)
    
    # Mathematical Separation Line
    ax.plot([540, 540], [ex_bottom, ex_top], color=C_TEXT if is_flash else C_MANTIS, lw=2, alpha=0.5, linestyle='--', zorder=1)

    # The Reactor Core (Bottom Left)
    core_rad = 140
    core_pulse = 10 * np.sin(t_sec * 15 * mult)
    ax.add_patch(Rectangle((PRI_CX - core_rad, PRI_CY - RAD_Y - core_rad), core_rad*2, core_rad*2, 
                 facecolor=C_VOID if not is_flash else C_TEXT, edgecolor=C_RED, lw=8, zorder=10))
    ax.scatter([PRI_CX], [PRI_CY - RAD_Y], s=25000 + (3000 * core_pulse), facecolors='none', edgecolors=C_RED, lw=4, alpha=0.4, zorder=11)
    if is_flash: ax.scatter([PRI_CX], [PRI_CY - RAD_Y], s=10000, c=C_RED, zorder=12)

    # The Turbine (Top Right)
    turb_y = SEC_CY + RAD_Y
    ax.add_patch(Circle((SEC_CX, turb_y), 130, facecolor=C_VOID if not is_flash else C_TEXT, edgecolor=C_DIM, lw=8, zorder=10))
    ax.scatter([SEC_CX], [turb_y], s=1000, c=C_RED if is_flash else C_DIM, zorder=12)
    
    # Turbine Blades (Rotating)
    for i in range(6):
        theta = np.radians(turb_angle + i*60)
        bx = SEC_CX + 110 * np.cos(theta)
        by = turb_y + 110 * np.sin(theta)
        ax.plot([SEC_CX, bx], [turb_y, by], color=C_TEXT if not is_flash else C_VOID, lw=8, zorder=11)

    # 2. RENDER FLUID MATRICES (O(N) THERMODYNAMICS)
    # Scatter Primary (Pressurized Loop)
    ax.scatter(px, py, s=15 if not is_flash else 40, c=p_cols, edgecolors='none', alpha=0.9, zorder=5)
    # Scatter Secondary (Steam Loop)
    ax.scatter(sx, sy, s=15 if not is_flash else 40, c=s_cols, edgecolors='none', alpha=0.9, zorder=5)

    # 3. TELEMETRY WIDGETS (NEURAL ENTRAINMENT UI)
    ui_col = C_CYAN if not is_flash else C_VOID
    txt_col = C_TEXT if not is_flash else C_VOID
    bg_col = C_VOID if not is_flash else C_TEXT
    
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=bg_col, alpha=0.9, zorder=20))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2, zorder=20)
    ax.text(0.04, 0.965, "LG-185 :: PWR PHASE BARRIER (THE MEMBRANE)", transform=ax.transAxes, color=txt_col, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=21)

    ax.add_patch(plt.Rectangle((0, 0), 1, 0.12, transform=ax.transAxes, color=bg_col, alpha=0.95, zorder=20))
    ax.plot([0, 1], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2, zorder=20)
    
    # Telemetry Data
    ax.text(0.04, 0.08, f"CORE TEMP: {int(p_press*3200)}°C | STEAM PRS: {int(s_press*1200)} PSI", transform=ax.transAxes, color=txt_col, fontsize=18, fontname='monospace', zorder=21)
    
    pulse = C_MANTIS if (f % 10 < 5) and not is_flash else txt_col
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=24, fontname='monospace', weight='bold', zorder=21)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) FLUID DYNAMICS STREAM (CLOSED LOOP TENSOR)
# ------------------------------------------------------------------
def generate_stream():
    # Numpy Pre-Allocation (The orbits)
    # Theta represents position on the squircle
    p_theta = np.random.uniform(0, 2*np.pi, N_PARTICLES)
    s_theta = np.random.uniform(0, 2*np.pi, N_PARTICLES)
    
    # Thickness offsets for the pipes
    p_dr = np.random.normal(0, 25, N_PARTICLES)
    s_dr = np.random.normal(0, 25, N_PARTICLES)
    
    # Heat specific state
    p_heat = np.zeros(N_PARTICLES)
    s_heat = np.zeros(N_PARTICLES)
    
    c_cy = np.array(hex_to_rgba(C_CYAN)[:3])
    c_red = np.array(hex_to_rgba(C_RED)[:3])
    c_mag = np.array(hex_to_rgba(C_MAGENTA)[:3])
    c_gold = np.array(hex_to_rgba(C_GOLD)[:3])
    
    turb_angle = 0.0

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        is_flash = False
        mult = 1.0
        
        # ---- PHASE 1: COLD START (0 - 4s) ----
        if t_sec < 4.0:
            state = "[01] REACTOR STARTUP :: O(N) PUMPS ENGAGED"
            mult = 0.4
            
        # ---- PHASE 2: THERMODYNAMIC IGNITION (4 - 10s) ----
        elif t_sec < 10.0:
            state = "[02] CRITICALITY :: HEAT TRANSFER ACROSS MEMBRANE"
            mult = 1.0 + (t_sec - 4.0) * 0.3

        # ---- PHASE 3: CRITICAL PRESSURE (10 - 14.8s) ----
        elif t_sec < 14.8:
            state = "WARNING: MAXIMUM VOLUME KINEMATICS. OVERLOAD IMMINENT."
            mult = 2.8 + (t_sec - 10.0) * 0.5
            if f % 8 < 4:
                ui_col = C_MAGENTA

        # ---- PHASE 4: TATHĀTĀ (14.8 - 17.5s) ----
        else:
            mult = 4.0
            if t_sec < 14.95:
                is_flash = True
            state = "TATHĀTĀ: THE BOUNDARY HOLDS. ENERGY IS TRANSLATED."

        # Kinematic Velocity
        base_v = 0.015 * mult
        p_theta = (p_theta + base_v) % (2*np.pi)  # CCW
        s_theta = (s_theta - base_v) % (2*np.pi)  # CW
        turb_angle += 12.0 * mult

        # -----------------------------------------------
        # O(1) SQUIRCLE PROJECTOR
        # -----------------------------------------------
        # abs(cos)^0.2 creates the rounded square bounds
        p_x = PRI_CX + (RAD_X + p_dr) * np.sign(np.cos(p_theta)) * (np.abs(np.cos(p_theta))**0.2)
        p_y = PRI_CY + (RAD_Y + p_dr) * np.sign(np.sin(p_theta)) * (np.abs(np.sin(p_theta))**0.2)

        s_x = SEC_CX + (RAD_X + s_dr) * np.sign(np.cos(s_theta)) * (np.abs(np.cos(s_theta))**0.2)
        s_y = SEC_CY + (RAD_Y + s_dr) * np.sign(np.sin(s_theta)) * (np.abs(np.sin(s_theta))**0.2)

        # -----------------------------------------------
        # O(N) THERMODYNAMIC KINEMATICS (HEAT EXCHANGER)
        # -----------------------------------------------
        # Primary Loop gains heat at the Bottom (Core), loses heat at the Right (Exchanger)
        core_heat_rate = 0.04 * mult
        ex_cool_rate = 0.06 * mult
        ex_heat_rate = 0.08 * mult
        turb_cool_rate = 0.10 * mult
        
        p_heat = np.clip(p_heat + np.where(p_y < PRI_CY - RAD_Y + 150, core_heat_rate, 0), 0, 1)
        p_heat = np.clip(p_heat - np.where(p_x > PRI_CX + RAD_X - 50, ex_cool_rate, 0), 0, 1)
        
        # Secondary Loop gains heat at the Left (Exchanger), loses heat at Top (Turbine)
        s_heat = np.clip(s_heat + np.where(s_x < SEC_CX - RAD_X + 50, ex_heat_rate, 0), 0, 1)
        s_heat = np.clip(s_heat - np.where(s_y > SEC_CY + RAD_Y - 150, turb_cool_rate, 0), 0, 1)

        # -----------------------------------------------
        # O(N) COLOR TENSOR MATRIX
        # -----------------------------------------------
        # Primary transfers from Cyan -> Red (but under pressure looks Magenta)
        p_cols = (1 - p_heat[:, None]) * c_cy + p_heat[:, None] * c_red
        # Secondary transfers from Cyan -> Gold (Steam)
        s_cols = (1 - s_heat[:, None]) * c_cy + s_heat[:, None] * c_gold

        yield (f, t_sec, state, p_x, p_y, p_cols, s_x, s_y, s_cols, turb_angle, mult, is_flash, np.mean(p_heat), np.mean(s_heat))

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 185: PWR THERMODYNAMIC MEMBRANE [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Nodes: {N_PARTICLES*2}")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
