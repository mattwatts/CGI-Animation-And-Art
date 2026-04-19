"""
SOVEREIGN CODE: logic_garden_191_steam_entrainment.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Slider-Crank Tensor (17.5 seconds)
SCENE: Logic Garden 191 (The Iron Tensor / Steam Thermodynamics)
HOTFIX: O(N) High-Pressure Exhaust, Linkage Kinematics, Tathata Vectorization
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon
import multiprocessing as mp
import os
import gc
import math

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_191_steam"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'        # Vacuum Background
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'        # Cast Iron Base
C_CYAN      = '#00FFFF'        # Expanding Exhaust (Cooling)
C_MAGENTA   = '#FF00FF'        # Live Steam (High Pressure)
C_GOLD      = '#FFD700'        # Kinetic Linkage Array
C_RED       = '#FF0033'        # Thermodynamic Overload
C_MANTIS    = '#00FF00'        # Terminal Geometry (Tathata)

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE KINEMATIC BOUNDING BOX
# ------------------------------------------------------------------
MAX_PARTICLES = 20000

# Macro-Geometry Coordinates
WHEEL_X = 250.0
WHEEL_Y = 600.0
WHEEL_R = 300.0
CRANK_R = 140.0
ROD_L   = 550.0

CYL_X = WHEEL_X + CRANK_R + ROD_L + 50.0  # ~990
CYL_Y = WHEEL_Y
CYL_W = 200.0
CYL_H = 140.0

c_mag = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_cy  = np.array(hex_to_rgba(C_CYAN)[:3])

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, px, py, p_sizes, c_tensor, angle_deg, is_flash, is_tathata, rpm_mult, ch_x = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg = C_TEXT if is_flash else C_VOID
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    theta_rad = np.radians(angle_deg)
    
    # Kinematics
    pin_x = WHEEL_X + CRANK_R * np.cos(theta_rad)
    pin_y = WHEEL_Y + CRANK_R * np.sin(theta_rad)

    # 1. RENDER STATIC STRUCTURES
    if not is_tathata and not is_flash:
        # The Drive Wheel (Cast Iron)
        ax.add_patch(Circle((WHEEL_X, WHEEL_Y), WHEEL_R, facecolor=C_VOID, edgecolor=C_DIM, lw=20, zorder=1))
        ax.add_patch(Circle((WHEEL_X, WHEEL_Y), WHEEL_R-40, facecolor=C_DIM, alpha=0.3, zorder=2))
        ax.add_patch(Circle((WHEEL_X, WHEEL_Y), 40, facecolor=C_VOID, edgecolor=C_TEXT, lw=4, zorder=3)) # Axle
        
        # Spokes
        for i in range(16):
            spoke_angle = np.radians(angle_deg + (i * 360/16))
            sx = WHEEL_X + (WHEEL_R-40) * np.cos(spoke_angle)
            sy = WHEEL_Y + (WHEEL_R-40) * np.sin(spoke_angle)
            ax.plot([WHEEL_X, sx], [WHEEL_Y, sy], color=C_DIM, lw=12, zorder=2)
            
        # Counterweight
        ax.add_patch(plt.matplotlib.patches.Wedge((WHEEL_X, WHEEL_Y), WHEEL_R-45, angle_deg+140, angle_deg+220, width=80, color=C_DIM, zorder=3))

    # 2. RENDER THE LINKAGE (The Kinetic Array)
    link_c = C_GOLD if not is_tathata else C_MANTIS
    if is_flash: link_c = C_VOID
    
    # Path of the Crank (Revealed during Tathata)
    if is_tathata and not is_flash:
        ax.add_patch(Circle((WHEEL_X, WHEEL_Y), CRANK_R, facecolor='none', edgecolor=C_MANTIS, lw=4, linestyle='--', zorder=5))
        ax.plot([WHEEL_X-CRANK_R, CYL_X], [WHEEL_Y, WHEEL_Y], color=C_MANTIS, lw=2, alpha=0.5, linestyle='--', zorder=5)

    # Main Rod
    ax.plot([pin_x, ch_x], [pin_y, CYL_Y], color=link_c, lw=25, zorder=10)
    ax.plot([pin_x, ch_x], [pin_y, CYL_Y], color=C_TEXT if not is_flash else C_VOID, lw=5, alpha=0.6, zorder=11)
    
    # Piston Rod
    ax.plot([ch_x, CYL_X + 100], [CYL_Y, CYL_Y], color=link_c, lw=15, zorder=8)
    
    # Crosshead / Wrist Pin
    ax.add_patch(Rectangle((ch_x-30, CYL_Y-40), 60, 80, facecolor=C_VOID if not is_flash else C_TEXT, edgecolor=link_c, lw=6, zorder=12))
    ax.add_patch(Circle((ch_x, CYL_Y), 15, facecolor=C_TEXT if not is_flash else C_VOID, zorder=13))
    
    # Crank Pin
    ax.add_patch(Circle((pin_x, pin_y), 30, facecolor=C_VOID if not is_flash else C_TEXT, edgecolor=link_c, lw=8, zorder=12))
    ax.add_patch(Circle((pin_x, pin_y), 15, facecolor=C_TEXT if not is_flash else C_VOID, zorder=13))

    # Cylinder Block
    if not is_tathata and not is_flash:
        ax.add_patch(Rectangle((CYL_X, CYL_Y - CYL_H/2), CYL_W, CYL_H, facecolor=C_VOID, edgecolor=C_DIM, lw=10, zorder=15))
        ax.add_patch(Rectangle((CYL_X+20, CYL_Y - CYL_H/2 + 20), CYL_W-40, CYL_H-40, facecolor=C_DIM, alpha=0.2, zorder=14))

    # 3. O(N) FLUID DYNAMICS (THE STEAM TENSOR)
    if len(px) > 0 and not is_tathata:
        ax.scatter(px, py, s=p_sizes*3.0, c=c_tensor, edgecolors='none', alpha=0.2, zorder=6)
        ax.scatter(px, py, s=p_sizes*1.0, c=C_TEXT if is_flash else c_tensor, edgecolors='none', alpha=0.9, zorder=7)

    # 4. TELEMETRY WIDGETS (NEURAL ENTRAINMENT UI)
    ui_col = C_CYAN if not is_tathata else C_MANTIS
    txt_col = C_TEXT if not is_flash else C_VOID
    bg_col  = C_VOID if not is_flash else C_TEXT
    
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=bg_col, alpha=0.9, zorder=80))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    ax.text(0.04, 0.965, "LG-191 :: THERMODYNAMIC VECTOR TRANSLATION", transform=ax.transAxes, color=txt_col, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=81)

    ax.add_patch(plt.Rectangle((0, 0), 1.0, 0.12, transform=ax.transAxes, color=bg_col, alpha=0.95, zorder=80))
    ax.plot([0, 1.0], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    
    rpm = int(rpm_mult * 300)
    ax.text(0.04, 0.08, f"CYLINDER PRESSURE MATRIX | RPM: {rpm:04d}", transform=ax.transAxes, color=txt_col, fontsize=20, fontname='monospace', zorder=81)
    
    # Tachometer Bar
    ax.add_patch(plt.Rectangle((0.72, 0.03), 0.25, 0.02, transform=ax.transAxes, color=C_DIM, zorder=80))
    bar_fill = min(1.0, rpm_mult / 5.0)
    bar_color = C_MAGENTA if rpm_mult > 3.0 else ui_col
    if is_flash: bar_color = C_VOID
    if is_tathata: bar_color = C_MANTIS
    
    ax.add_patch(plt.Rectangle((0.72, 0.03), 0.25 * bar_fill, 0.02, transform=ax.transAxes, color=bar_color, zorder=81))

    pulse = ui_col if (f % 10 < 5) and not is_flash else txt_col
    if rpm_mult > 4.0 and not is_tathata and f % 4 < 2: pulse = C_RED
    if is_flash: pulse = C_VOID
    if is_tathata and not is_flash: pulse = C_MANTIS

    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=24, fontname='monospace', weight='bold', zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) TENSOR KINEMATICS STREAM
# ------------------------------------------------------------------
def generate_stream():
    px = np.zeros(MAX_PARTICLES)
    py = np.zeros(MAX_PARTICLES)
    vx = np.zeros(MAX_PARTICLES)
    vy = np.zeros(MAX_PARTICLES)
    p_life = np.zeros(MAX_PARTICLES)
    
    spawn_idx = 0
    angle_deg = 0.0
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        is_flash = False
        is_tathata = False
        rpm_mult = 1.0
        
        # ---- PHASE 1: PRESSURE INJECTION (0 - 4s) ----
        if t_sec < 4.0:
            state = "[01] BOILER IGNITION :: O(N) LINEAR EXPANSION"
            rpm_mult = 0.2 + (t_sec * 0.2)

        # ---- PHASE 2: RECIPROCATING ACCELERATION (4 - 10s) ----
        elif t_sec < 10.0:
            state = "[02] RECIPROCATING MATRIX :: TRANSLATING CHAOS TO PI"
            prog = (t_sec - 4.0) / 6.0
            rpm_mult = 1.0 + (prog * 2.0)

        # ---- PHASE 3: OPTICAL FRICTION OVERLOAD (10 - 14.8s) ----
        elif t_sec < 14.8:
            state = "WARNING: THERMODYNAMIC VELOCITY AT STRUCTURAL LIMITS"
            prog = (t_sec - 10.0) / 4.8
            rpm_mult = 3.0 + (prog**2 * 4.0) # Quadratic acceleration

        # ---- PHASE 4: TATHĀTĀ / GEOMETRIC EXTRACTION (14.8 - 17.5s) ----
        else:
            is_tathata = True
            rpm_mult = 1.5 # Lock to perfect stable rpm
            if t_sec < 14.95:
                is_flash = True
            state = "TATHĀTĀ: TO CONQUER THE HORIZON, PUSH THE EARTH BACKWARDS."

        # Kinematic Update
        angle_deg = (angle_deg + 4.0 * rpm_mult) % 360.0
        theta_rad = np.radians(angle_deg)
        
        pin_x = WHEEL_X + CRANK_R * np.cos(theta_rad)
        pin_y = WHEEL_Y + CRANK_R * np.sin(theta_rad)
        
        # Crosshead calculation
        # (ch_x - pin_x)^2 + (CYL_Y - pin_y)^2 = ROD_L^2
        ch_term = ROD_L**2 - (CYL_Y - pin_y)**2
        ch_x = pin_x + np.sqrt(max(0, ch_term))
        
        # Determine exhaust stroke (chuff)
        # Assuming stroke end is near angle 0 or 180
        is_chuff = False
        if abs(np.sin(theta_rad)) < 0.3 and np.cos(theta_rad) > 0 and not is_tathata: 
            is_chuff = True

        # O(1) Steam Injection
        spawns = 0
        if is_chuff:
            spawns = int(300 * rpm_mult)
        else:
            spawns = int(20 * rpm_mult) # Continuous bleed
            
        spawns = min(spawns, MAX_PARTICLES - spawn_idx)
        
        if spawns > 0 and spawn_idx < MAX_PARTICLES:
            # Spawn at cylinder exhaust port (top of cylinder)
            ex_x = CYL_X + 100
            ex_y = CYL_Y + CYL_H/2
            
            px[spawn_idx:spawn_idx+spawns] = ex_x + np.random.uniform(-20, 20, spawns)
            py[spawn_idx:spawn_idx+spawns] = ex_y + np.random.uniform(0, 10, spawns)
            
            # Massive vertical velocity for exhaust
            v_blow = 15.0 * rpm_mult if is_chuff else 5.0
            vx[spawn_idx:spawn_idx+spawns] = np.random.uniform(-4, -1, spawns) # Blows backwards (train moves forward)
            vy[spawn_idx:spawn_idx+spawns] = np.random.uniform(v_blow*0.5, v_blow, spawns)
            
            p_life[spawn_idx:spawn_idx+spawns] = 1.0
            spawn_idx += spawns

        # O(1) Global Physics
        active = p_life > 0
        if np.any(active):
            px[active] += vx[active]
            py[active] += vy[active]
            
            # Expansion and drag
            vx[active] *= 0.98
            vy[active] *= 0.95
            
            p_life[active] -= 0.01

        # Resetter
        if spawn_idx > MAX_PARTICLES - 1000:
            # Shift arrays to drop dead particles instantly
            active_idx = np.where(active)[0]
            new_cnt = len(active_idx)
            px[:new_cnt] = px[active_idx]
            py[:new_cnt] = py[active_idx]
            vx[:new_cnt] = vx[active_idx]
            vy[:new_cnt] = vy[active_idx]
            p_life[:new_cnt] = p_life[active_idx]
            p_life[new_cnt:] = 0
            spawn_idx = new_cnt

        # O(N) Chromatics
        active_cnt = np.sum(p_life > 0)
        c_tensor = np.zeros((active_cnt, 3))
        
        if active_cnt > 0:
            life_array = p_life[p_life > 0][:, None]
            c_tensor = life_array * c_mag + (1 - life_array) * c_cy
            p_sizes = 2.0 + (1.0 - life_array.flatten()) * 20.0

        yield (f, t_sec, state, np.copy(px[p_life > 0]), np.copy(py[p_life > 0]), p_sizes, c_tensor, angle_deg, is_flash, is_tathata, rpm_mult, ch_x)

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 191: THE THERMODYNAMIC DRIVER [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: O(N) High-Pressure Exhaust Vectorization")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Nodes: {MAX_PARTICLES}")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
