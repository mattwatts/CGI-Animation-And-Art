"""
SOVEREIGN CODE: logic_garden_192_aegis_entrainment.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Phased Array Tensor (17.5 seconds)
SCENE: Logic Garden 192 (The AEGIS Tensor / Saturation Defense)
HOTFIX: Alpha Tensor Overflow Correction / Compile-Time Safety bounds
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_192_aegis"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'        # Deep Ocean / Midnight Sky
C_TEXT      = '#FFFFFF'
C_DIM       = '#0A1520'        # Radar Ambient
C_RED       = '#FF0033'        # The Vampires (Saturation Swarm)
C_MAGENTA   = '#FF00FF'        # High-Speed Hypersonic Threat
C_CYAN      = '#00FFFF'        # SPY-1 Phased Array / Targeting Grid
C_GOLD      = '#FFD700'        # SM-6 Interceptor (Outbound)
C_MANTIS    = '#00FF00'        # Terminal Intercept & Tathata Grid

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE KINEMATIC BOUNDING BOX
# ------------------------------------------------------------------
N_VAMPIRES = 15000
N_BIRDS = 400  # Max concurrent intercepts visualized

SHIP_X, SHIP_Y = 540, 200
ENGAGE_RAD = 750.0  # The Absolute Kill Box Perimeter
WARN_RAD = 1200.0   # SPY-1 Detection Box

# Pre-allocated intrinsic parameters
np.random.seed(192)
# Spawn vampires in a wide arc high above
v_start_theta = np.random.uniform(np.pi*0.1, np.pi*0.9, N_VAMPIRES)
v_start_r = np.random.uniform(WARN_RAD + 200, WARN_RAD + 2000, N_VAMPIRES)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, vx_act, vy_act, v_cols, v_sizes, exp_pts, ex_sizes, beam_theta, radar_alpha, is_flash, is_tathata, def_load = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg = C_TEXT if is_flash else C_VOID
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    # 1. RENDER STATIC STRUCTURES (THE SHIELD PERIMETER)
    if not is_flash:
        # Threat assessment rings
        ax.add_patch(Circle((SHIP_X, SHIP_Y), WARN_RAD, fill=False, edgecolor=C_CYAN, lw=2, linestyle=':', alpha=radar_alpha))
        # HOTFIX IMPLEMENTED: Mathematically bounding the alpha variance
        engage_alpha = min(1.0, radar_alpha + 0.2)
        ax.add_patch(Circle((SHIP_X, SHIP_Y), ENGAGE_RAD, fill=False, edgecolor=C_MANTIS if is_tathata else C_CYAN, lw=4, alpha=engage_alpha))
        ax.add_patch(Circle((SHIP_X, SHIP_Y), ENGAGE_RAD-20, fill=False, edgecolor=C_DIM, lw=20))
        
        # SPY-1 Phased Array Constructive Interference Beams
        # Unlike a mechanical sweep, it rapidly flickers to multiple angles
        if radar_alpha > 0 and not is_tathata:
            for bt in beam_theta:
                bx = SHIP_X + WARN_RAD * 1.5 * np.cos(bt)
                by = SHIP_Y + WARN_RAD * 1.5 * np.sin(bt)
                ax.plot([SHIP_X, bx], [SHIP_Y, by], color=C_CYAN, lw=1, alpha=0.15)
                # Hard targeting beam
                if np.random.rand() > 0.8:
                    ax.plot([SHIP_X, bx], [SHIP_Y, by], color=C_CYAN, lw=4, alpha=0.4)

    # 2. RENDER THE SHIP (VLS SILO)
    if not is_flash:
        ax.add_patch(Circle((SHIP_X, SHIP_Y), 40, facecolor=C_VOID, edgecolor=C_TEXT if not is_tathata else C_MANTIS, lw=6, zorder=50))
        ax.add_patch(Circle((SHIP_X, SHIP_Y), 10, facecolor=C_CYAN if not is_tathata else C_MANTIS, zorder=51))

    # 3. O(N) THREAT SWARM (VAMPIRES)
    if len(vx_act) > 0 and not is_tathata:
        # Massive Overdraw Bloom
        ax.scatter(vx_act, vy_act, s=v_sizes*8.0, c=v_cols, edgecolors='none', alpha=0.15, zorder=10)
        ax.scatter(vx_act, vy_act, s=v_sizes*1.5, c=C_TEXT, edgecolors='none', alpha=0.9, zorder=11)
        
        # Trailing vectors (Visual speed)
        trail_x = vx_act + (vx_act - SHIP_X) * 0.05
        trail_y = vy_act + (vy_act - SHIP_Y) * 0.05
        ax.plot([vx_act, trail_x], [vy_act, trail_y], color=C_RED, lw=0.5, alpha=0.3, zorder=9)

    # 4. O(1) TERMINAL INTERCEPTS (EXPLOSIONS & OUTBOUND BIRDS)
    if len(exp_pts) > 0 and not is_tathata and not is_flash:
        ex_x, ex_y = exp_pts[:,0], exp_pts[:,1]
        
        # Outbound Interceptor Trails (from Ship to Impact)
        for ix, iy in zip(ex_x, ex_y):
            # Draw curved or straight line from ship
            ax.plot([SHIP_X, ix], [SHIP_Y, iy], color=C_GOLD, lw=1, alpha=0.4, zorder=15)
            
        # Impact Bloom (SM-6 Kinetic Kill)
        ax.scatter(ex_x, ex_y, s=ex_sizes*25, facecolors='none', edgecolors=C_MANTIS, lw=4, zorder=20)
        ax.scatter(ex_x, ex_y, s=ex_sizes*5, c=C_TEXT, zorder=21)

    # Hardware Flash Geometry (The Tathata Snap)
    if is_flash:
        ax.add_patch(Circle((SHIP_X, SHIP_Y), ENGAGE_RAD, fill=False, edgecolor=C_MANTIS, lw=60, zorder=60))
        ax.add_patch(Circle((SHIP_X, SHIP_Y), ENGAGE_RAD, fill=False, edgecolor=C_TEXT, lw=20, zorder=61))

    # 5. TELEMETRY WIDGETS (NEURAL ENTRAINMENT UI)
    ui_col = C_CYAN if not is_tathata else C_MANTIS
    if is_flash: ui_col = C_VOID
    txt_col = C_TEXT if not is_flash else C_VOID
    bg_col  = C_VOID if not is_flash else C_TEXT
    
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=bg_col, alpha=0.9, zorder=80))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    ax.text(0.04, 0.965, "LG-192 :: AEGIS COMBAT SYSTEM / SATURATION DEFENSE", transform=ax.transAxes, color=txt_col, fontsize=22, fontname='monospace', weight='bold', va='center', zorder=81)

    ax.add_patch(plt.Rectangle((0, 0), 1.0, 0.12, transform=ax.transAxes, color=bg_col, alpha=0.95, zorder=80))
    ax.plot([0, 1.0], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    ax.text(0.04, 0.08, "AN/SPY-1 RADAR TENSOR :: VLS RIPPLE FIRE", transform=ax.transAxes, color=txt_col, fontsize=18, fontname='monospace', zorder=81)
    
    # AEGIS System Load Bar (VLS Saturation)
    ax.add_patch(plt.Rectangle((0.72, 0.03), 0.25, 0.02, transform=ax.transAxes, color=C_DIM, zorder=80))
    bar_fill = min(1.0, def_load)
    bar_color = C_GOLD if def_load > 0.5 else ui_col
    if def_load > 0.85: bar_color = C_RED
    if is_flash: bar_color = C_VOID
    if is_tathata: bar_color = C_MANTIS
    
    ax.add_patch(plt.Rectangle((0.72, 0.03), 0.25 * bar_fill, 0.02, transform=ax.transAxes, color=bar_color, zorder=81))
    ax.text(0.72, 0.06, f"THREAT LOAD: {bar_fill*100:.1f}%", transform=ax.transAxes, color=txt_col, fontsize=14, fontname='monospace', zorder=81)

    pulse = ui_col if (f % 10 < 5) and not is_flash else txt_col
    if def_load > 0.8 and not is_tathata and f % 4 < 2: pulse = C_RED # Overload warning
    if is_flash: pulse = C_VOID
    if is_tathata and not is_flash: pulse = C_MANTIS

    ax.text(0.04, 0.03, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=22, fontname='monospace', weight='bold', zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) TENSOR KINEMATICS STREAM
# ------------------------------------------------------------------
def generate_stream():
    # Numpy Physics Vectors
    v_r = np.copy(v_start_r)
    v_theta = np.copy(v_start_theta)
    v_active = np.zeros(N_VAMPIRES, dtype=bool)
    
    # Explosions array
    ex_list = []
    
    c_red = np.array(hex_to_rgba(C_RED)[:3])
    c_mag = np.array(hex_to_rgba(C_MAGENTA)[:3])
    
    spawn_idx = 0
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        is_flash = False
        is_tathata = False
        radar_alpha = 0.0
        def_load = 0.0
        beam_theta = []
        
        # ---- PHASE 1: THE SATURATION SWARM (0 - 4s) ----
        if t_sec < 4.0:
            state = "[01] SATURATION ATTACK DETECTED :: MULTIPLE INBOUND VAMPIRES"
            spawns = 250
            if spawn_idx + spawns < N_VAMPIRES:
                v_active[spawn_idx:spawn_idx+spawns] = True
                spawn_idx += spawns

        # ---- PHASE 2: SPY-1 PHASED ARRAY SCAN (4 - 10s) ----
        elif t_sec < 10.0:
            state = "[02] AN/SPY-1 ENGAGED :: CALCULATING INTERCEPT GEOMETRY"
            radar_alpha = min(0.6, (t_sec - 4.0) / 4.0)
            def_load = (t_sec - 4.0) / 12.0
            
            # Massive swarm dump
            spawns = 500
            if spawn_idx + spawns < N_VAMPIRES:
                v_active[spawn_idx:spawn_idx+spawns] = True
                spawn_idx += spawns
                
            # Electronic Beam Steering (Flickering random azimuths instantly)
            num_beams = int(10 + (t_sec - 4.0)*5)
            beam_theta = np.random.uniform(0, np.pi, num_beams)

        # ---- PHASE 3: RIPPLE FIRE / OPTICAL FRICTION (10 - 14.8s) ----
        elif t_sec < 14.8:
            state = "WARNING: VLS EXHAUSTION IMMINENT. MATHEMATICAL OVERLOAD."
            radar_alpha = 0.8
            def_load = 0.5 + ((t_sec - 10.0) / 4.8) * 0.5
            
            num_beams = 40
            beam_theta = np.random.uniform(0, np.pi, num_beams)

        # ---- PHASE 4: TATHĀTĀ / SHIELD WALL (14.8 - 17.5s) ----
        else:
            is_tathata = True
            radar_alpha = 1.0
            def_load = 0.0
            if t_sec < 14.95:
                is_flash = True
            state = "TATHĀTĀ: THE BOUNDARY HOLDS. THE SWARM IS ERGOTICS."

        # -----------------------------------------------
        # O(1) AEGIS KINEMATIC SOLVER
        # -----------------------------------------------
        if np.any(v_active) and not is_tathata:
            act_idx = np.where(v_active)[0]
            
            # Vampires fall screaming towards the ship
            v_r[act_idx] -= 25.0 * (1.0 + (t_sec * 0.1)) # Accelerating threat
            # Add violent jitter (evasive maneuvers)
            v_theta[act_idx] += np.random.normal(0, 0.01, len(act_idx))
            
            # The Mathematical Bounding Box (AEGIS DOCTRINE)
            # If distance crosses ENGAGE_RAD, they hit the absolute wall
            kill_mask = v_r[act_idx] <= ENGAGE_RAD
            
            killed_idx = act_idx[kill_mask]
            
            if len(killed_idx) > 0 and radar_alpha > 0.0:
                # Spawn Explosions
                for kx in killed_idx:
                    k_theta = v_theta[kx]
                    px = SHIP_X + ENGAGE_RAD * np.cos(k_theta)
                    py = SHIP_Y + ENGAGE_RAD * np.sin(k_theta)
                    # Limit explosion render count to maintain 60FPS
                    if len(ex_list) < N_BIRDS:
                        ex_list.append([px, py, 10.0]) # x, y, life
            
                # Delete the threat instantly (O(1) Memory Erase)
                v_active[killed_idx] = False

        # Convert remaining to Cartesian for rendering
        render_active = np.where(v_active)[0]
        vx_act = SHIP_X + v_r[render_active] * np.cos(v_theta[render_active])
        vy_act = SHIP_Y + v_r[render_active] * np.sin(v_theta[render_active])

        # Dynamic array sizes and colors
        v_sizes = np.random.uniform(2, 6, len(render_active))
        v_cols = np.zeros((len(render_active), 3))
        v_cols[:] = c_red
        # High speed threats burn Magenta
        if t_sec > 10.0:
            c_mask = np.random.rand(len(render_active)) > 0.7
            v_cols[c_mask] = c_mag

        # Update Explosions
        new_ex_list = []
        exp_pts = []
        for ex in ex_list:
            ex[2] -= 0.5 # Diminish life
            if ex[2] > 0:
                new_ex_list.append(ex)
                exp_pts.append(ex)
        ex_list = new_ex_list

        yield (f, t_sec, state, vx_act, vy_act, v_cols, v_sizes, np.array(exp_pts), 
               np.array([e[2] for e in exp_pts]) if len(exp_pts)>0 else [], 
               beam_theta, radar_alpha, is_flash, is_tathata, def_load)

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 192: THE AEGIS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Alpha Tensor Bounds enforced.")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Nodes: {N_VAMPIRES}")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
