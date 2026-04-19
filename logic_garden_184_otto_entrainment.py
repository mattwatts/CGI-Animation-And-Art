"""
SOVEREIGN CODE: logic_garden_184_otto_entrainment.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(N) Numpy Fluid Sim (17.5 seconds)
SCENE: Logic Garden 184 (The Otto Cycle / Thermodynamic Bounding Box)
HOTFIX: ARRAY ROUTING MISALIGNMENT (Mask Mutability Corrected)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, Wedge
import multiprocessing as mp
import os
import gc
import math

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_184_otto"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_DIM     = '#1A1A24'          # Iron Block Bounding Box
C_CYAN    = '#00FFFF'          # Intake Matrix / Oxygen Potential
C_MAGENTA = '#FF00FF'          # Compression / Friction Accumulation
C_GOLD    = '#FFD700'          # Ignition Origin
C_RED     = '#FF0033'          # Thermal Waste / Exhaust Entropy
C_MANTIS  = '#00FF00'          # Terminal Telemetry Flow

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# THE GEOMETRIC BOUNDING BOX & KINEMATICS
# ------------------------------------------------------------------
CYCLES = 4 # Complete 4x720 degree cycles perfectly in 17.5 sec
DEG_PER_FRAME = (CYCLES * 720.0) / TOTAL_FRAMES

CX, CY = 540, 400      # Crankshaft Origin
CRANK_R = 180.0
ROD_L = 480.0
BORE = 360.0
PISTON_H = 150.0
CYL_TOP = CY + CRANK_R + ROD_L + PISTON_H + 100 # Top Dead Center clearance
HEAD_Y = CYL_TOP + 120.0

MAX_PARTICLES = 15000

def get_piston_kine(theta_rad):
    # exact kinematic position of wrist pin relative to crank center
    t = theta_rad
    term1 = CRANK_R * np.cos(t)
    term2 = np.sqrt(ROD_L**2 - (CRANK_R * np.sin(t))**2)
    y = CY + term1 + term2
    
    # Instantaneous velocity (derivative)
    dy = -CRANK_R * np.sin(t) - (CRANK_R**2 * np.sin(t) * np.cos(t)) / term2
    vy = dy * np.radians(DEG_PER_FRAME) # scaled per frame
    return y, vy

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, ca, p_y, p_vy, ax_pts, ay_pts, a_cols, valve_in, valve_ex, is_flash, p_level = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg = C_TEXT if is_flash else C_VOID
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    theta_rad = np.radians(ca)

    # 1. RENDER BOUNDING BOX (ENGINE BLOCK)
    wall_left = CX - BORE/2
    wall_right = CX + BORE/2
    
    # Render cylinder walls
    ax.plot([wall_left, wall_left], [CY+200, HEAD_Y], color=C_CYAN if not is_flash else C_VOID, lw=6, zorder=10)
    ax.plot([wall_right, wall_right], [CY+200, HEAD_Y], color=C_CYAN if not is_flash else C_VOID, lw=6, zorder=10)
    
    # Engine Head & Valves
    ax.plot([wall_left, wall_left+100], [HEAD_Y, HEAD_Y], color=C_DIM, lw=12, zorder=10)
    ax.plot([wall_right-100, wall_right], [HEAD_Y, HEAD_Y], color=C_DIM, lw=12, zorder=10)
    ax.plot([CX-40, CX+40], [HEAD_Y, HEAD_Y], color=C_DIM, lw=12, zorder=10) # Spark plug block

    # Valves (Left = Intake, Right = Exhaust)
    in_v_y = HEAD_Y - (valve_in * 60)
    ex_v_y = HEAD_Y - (valve_ex * 60)
    ax.plot([CX-90, CX-90], [HEAD_Y+150, in_v_y], color=C_TEXT, lw=10, zorder=8) # Stem
    ax.add_patch(Polygon([[CX-130, in_v_y], [CX-50, in_v_y], [CX-90, in_v_y+20]], color=C_TEXT, zorder=8)) # Head
    
    ax.plot([CX+90, CX+90], [HEAD_Y+150, ex_v_y], color=C_TEXT, lw=10, zorder=8) 
    ax.add_patch(Polygon([[CX+50, ex_v_y], [CX+130, ex_v_y], [CX+90, ex_v_y+20]], color=C_TEXT, zorder=8))

    # Spark Plug
    ax.plot([CX, CX], [HEAD_Y+100, HEAD_Y-20], color=C_TEXT, lw=8, zorder=11)
    if is_flash:
        ax.scatter([CX], [HEAD_Y-20], s=30000, facecolors='none', edgecolors=C_CYAN, lw=15, zorder=15)
        ax.scatter([CX], [HEAD_Y-20], s=8000, c=C_TEXT, zorder=16)

    # 2. RENDER FLUID MATRICES (O(N) THERMODYNAMICS)
    if len(ax_pts) > 0:
        ax.scatter(ax_pts, ay_pts, s=25 if not is_flash else 70, c=a_cols, edgecolors='none', alpha=0.8, zorder=5)

    # 3. KINEMATIC COMPONENTS (PISTON / ROD / CRANK)
    pin_y = p_y
    pist_top = p_y + PISTON_H
    
    # Connecting Rod
    crank_x = CX + CRANK_R * np.sin(theta_rad)
    crank_y = CY + CRANK_R * np.cos(theta_rad)
    
    ax.plot([crank_x, CX], [crank_y, pin_y], color=C_MAGENTA if not is_flash else C_VOID, lw=20, zorder=12)
    ax.plot([crank_x, CX], [crank_y, pin_y], color=C_TEXT if not is_flash else C_DIM, lw=4, zorder=13) # Core line
    
    # Crankshaft Web
    ax.add_patch(Circle((CX, CY), CRANK_R + 30, color=C_DIM, zorder=10))
    ax.add_patch(Wedge((CX, CY), CRANK_R+40, np.degrees(theta_rad)+90, np.degrees(theta_rad)+270, color=C_VOID, zorder=11))
    ax.add_patch(Circle((CX, CY), 25, color=C_TEXT, zorder=14)) # Center bearing
    ax.add_patch(Circle((crank_x, crank_y), 30, color=C_TEXT, zorder=14)) # Rod bearing

    # Piston Head
    piston_poly = [
        [wall_left+5, pin_y - 20],
        [wall_right-5, pin_y - 20],
        [wall_right-5, pist_top],
        [wall_left+5, pist_top]
    ]
    ax.add_patch(Polygon(piston_poly, facecolor=C_DIM, edgecolor=C_TEXT, lw=4, zorder=15))
    ax.add_patch(Circle((CX, pin_y), 20, color=C_TEXT, zorder=16)) # Wrist pin
    
    # Piston Rings
    ax.plot([wall_left+5, wall_right-5], [pist_top-20, pist_top-20], color=C_TEXT, lw=3, zorder=16)
    ax.plot([wall_left+5, wall_right-5], [pist_top-40, pist_top-40], color=C_TEXT, lw=3, zorder=16)

    # 4. TELEMETRY WIDGETS (NEURAL ENTRAINMENT UI)
    ui_col = C_CYAN if not is_flash else C_VOID
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID if not is_flash else C_TEXT, alpha=0.9, zorder=20))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2, zorder=20)
    ax.text(0.04, 0.965, "LG-184 :: THE THERMODYNAMIC BOUNDING BOX", transform=ax.transAxes, color=C_TEXT if not is_flash else C_VOID, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=21)

    ax.add_patch(plt.Rectangle((0, 0), 1, 0.12, transform=ax.transAxes, color=C_VOID if not is_flash else C_TEXT, alpha=0.95, zorder=20))
    ax.plot([0, 1], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2, zorder=20)
    ax.text(0.04, 0.08, "OPERATIONAL PHASE TENSOR:", transform=ax.transAxes, color=C_TEXT if not is_flash else C_VOID, fontsize=20, fontname='monospace', zorder=21)
    
    # Pressure Bar
    ax.add_patch(plt.Rectangle((0.75, 0.03), 0.20, 0.02, transform=ax.transAxes, color=C_DIM, zorder=21))
    ax.add_patch(plt.Rectangle((0.75, 0.03), 0.20 * p_level, 0.02, transform=ax.transAxes, color=C_MAGENTA, zorder=22))
    ax.text(0.75, 0.06, f"KINETIC PRESSURE: {int(p_level*100)}%", transform=ax.transAxes, color=C_TEXT if not is_flash else C_VOID, fontsize=14, fontname='monospace', zorder=21)

    pulse = C_MANTIS if (f % 10 < 5) and not is_flash else (C_TEXT if not is_flash else C_VOID)
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=24, fontname='monospace', weight='bold', zorder=21)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) FLUID DYNAMICS STREAM 
# ------------------------------------------------------------------
def generate_stream():
    # Numpy Swarm Pre-Allocation
    px = np.zeros(MAX_PARTICLES)
    py = np.zeros(MAX_PARTICLES)
    vx = np.zeros(MAX_PARTICLES)
    vy = np.zeros(MAX_PARTICLES)
    p_act = np.zeros(MAX_PARTICLES, dtype=bool)
    
    c_cy_rgb = np.array(hex_to_rgba(C_CYAN)[:3])
    c_mg_rgb = np.array(hex_to_rgba(C_MAGENTA)[:3])
    c_re_rgb = np.array(hex_to_rgba(C_RED)[:3])
    
    spawn_idx = 0

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        ca_total = f * DEG_PER_FRAME
        ca = ca_total % 720.0
        
        pin_y, vy_pin = get_piston_kine(np.radians(ca))
        pist_top_y = pin_y + PISTON_H
        
        # Valve Lifts
        v_in = max(0, np.sin(np.radians(ca))) if ca < 180 else 0
        v_ex = max(0, np.sin(np.radians(ca - 540))) if ca >= 540 else 0
        
        is_flash = False
        p_level = 0.0

        # ---- PHASE 1: INTAKE (0 - 180) ----
        if ca < 180:
            state = "[01] INTAKE :: O(N) FLUID INJECTION"
            p_level = 0.1
            # Spawn
            spawns = 200
            if spawn_idx + spawns < MAX_PARTICLES and v_in > 0.1:
                px[spawn_idx:spawn_idx+spawns] = CX - 90 + np.random.uniform(-30, 30, spawns) # Intake port
                py[spawn_idx:spawn_idx+spawns] = HEAD_Y - 20
                vx[spawn_idx:spawn_idx+spawns] = np.random.uniform(-5, 5, spawns)
                vy[spawn_idx:spawn_idx+spawns] = np.random.uniform(-40, -10, spawns) # Sucked down
                p_act[spawn_idx:spawn_idx+spawns] = True
                spawn_idx += spawns

        # ---- PHASE 2: COMPRESSION (180 - 360) ----
        elif ca < 360:
            state = "[02] COMPRESSION :: KINETIC VOLUME CONSTRAINED"
            prog = (ca - 180) / 180.0 
            p_level = 0.1 + (prog**3) * 0.9 

        # ---- PHASE 3: POWER (360 - 540) ----
        elif ca < 540:
            prog = (ca - 360) / 180.0
            if ca < 365:
                is_flash = True
                state = "TATHĀTĀ: THERMODYNAMIC REALIZATION. O(1) IGNITION."
                p_level = 1.0
                if np.any(p_act):
                    vy[p_act] -= np.random.uniform(40, 100, np.sum(p_act))
                    vx[p_act] += np.random.uniform(-30, 30, np.sum(p_act))
            else:
                state = "[03] POWER :: EXPANDING SHOCKWAVE / MAXIMAL MATRIX"
                p_level = max(0.1, 1.0 - prog*1.2)

        # ---- PHASE 4: EXHAUST (540 - 720) ----
        else:
            state = "[04] EXHAUST :: ENTROPY PURGE SEQUENCE"
            p_level = 0.15
            
            if v_ex > 0.1 and np.any(p_act):
                # Pull vectors towards exhaust port
                dx = (CX + 90) - px[p_act]
                dy = HEAD_Y - py[p_act]
                dist = np.sqrt(dx**2 + dy**2) + 1.0
                vx[p_act] += (dx / dist) * 8.0
                vy[p_act] += (dy / dist) * 8.0 + 10.0 # Upward draft

        # -----------------------------------------------
        # O(1) GLOBAL PHYSICS SOLVER (HOTFIX DEPLOYED)
        # -----------------------------------------------
        if np.any(p_act):
            # 1. Update Core Kinematics
            px[p_act] += vx[p_act]
            py[p_act] += vy[p_act]
            
            vx[p_act] *= 0.98
            vy[p_act] -= 0.5 
            
            # 2. Extract Exact Index Routing (Zero Mask-Shrink Error)
            act_idx = np.where(p_act)[0]
            
            # Bounding Box 1: Piston Head
            hit_piston = py[act_idx] < pist_top_y
            hp_idx = act_idx[hit_piston]
            if len(hp_idx) > 0:
                py[hp_idx] = pist_top_y + np.random.uniform(1, 5, len(hp_idx))
                vy[hp_idx] = vy_pin + np.abs(vy[hp_idx]) * 0.8
            
            # Bounding Box 2: Cylinder Walls
            left_w = CX - BORE/2 + 10
            right_w = CX + BORE/2 - 10
            
            # Detect Out of Bounds BEFORE Clip to invert velocity
            hit_walls = (px[act_idx] <= left_w) | (px[act_idx] >= right_w)
            hw_idx = act_idx[hit_walls]
            if len(hw_idx) > 0:
                vx[hw_idx] = -vx[hw_idx] * 0.5
                
            # Restrict bounds mathematically
            px[act_idx] = np.clip(px[act_idx], left_w, right_w)
            
            # Bounding Box 3: Cylinder Head & Ports
            hit_head = py[act_idx] >= HEAD_Y - 5
            kill_mask = hit_head & (px[act_idx] > CX) & (ca >= 540)
            bounce_mask = hit_head & ~kill_mask & (py[act_idx] < HEAD_Y + 100)
            
            # Apply Bounces
            bh_idx = act_idx[bounce_mask]
            if len(bh_idx) > 0:
                py[bh_idx] = HEAD_Y - 5
                vy[bh_idx] = -np.abs(vy[bh_idx]) * 0.5
                
            # Apply Erasure (Kill Particles)
            k_idx = act_idx[kill_mask]
            if len(k_idx) > 0:
                p_act[k_idx] = False

        # -----------------------------------------------
        # O(N) COLOR TENSOR MATRIX
        # -----------------------------------------------
        active_cnt = np.sum(p_act)
        c_tensor = np.zeros((active_cnt, 3))
        
        if ca < 180:   c_tensor[:] = c_cy_rgb
        elif ca < 360: c_tensor[:] = c_cy_rgb + (c_mg_rgb - c_cy_rgb) * ((ca-180)/180.0)
        elif ca < 540: c_tensor[:] = c_mg_rgb + (c_re_rgb - c_mg_rgb) * ((ca-360)/180.0)
        else:          c_tensor[:] = c_re_rgb * 0.6 # Dim waste
        
        if ca > 700.0: spawn_idx = 0 

        yield (f, t_sec, state, ca, pin_y, vy_pin, np.copy(px[p_act]), np.copy(py[p_act]), c_tensor, v_in, v_ex, is_flash, p_level)


# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 184: THE OTTO TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: ARRAY ROUTING MISALIGNMENT (Mask Mutability)")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Nodes: {MAX_PARTICLES}")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
