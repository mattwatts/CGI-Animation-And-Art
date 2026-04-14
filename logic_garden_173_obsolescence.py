"""
SOVEREIGN CODE: logic_garden_173_obsolescence.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Dimensional Override Simulation (35 seconds)
SCENE: Logic Garden 173 (Architectural Obsolescence / Why the 'T' Died)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import multiprocessing as mp
import os
import gc
import math

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 35                   
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_173_obsolescence"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_DIM     = '#1A1A24'          # Foundation Surface Matrix
C_GOLD    = '#FFD700'          # Legacy Supremacy (The 2D Masters)
C_CYAN    = '#00FFFF'          # Exo-Atmospheric Swarm (The 3D Upgrade)
C_MANTIS  = '#00FF00'          # Terminal Dimension Flow
C_MAGENTA = '#FF00FF'          # Structural Obsolescence (Deletion Blooms)
C_RED     = '#FF0033'          # Unused Legacy Traces

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY & MATHEMATICAL SPACE
# ------------------------------------------------------------------
np.random.seed(173)
N_GOLD = 9
N_SWARM = 500

# The Perfect 2D Line (Crossing the T)
gold_bases_x = np.linspace(-350, 350, N_GOLD)
gold_bases_y = np.zeros(N_GOLD)

# Swarm initial vectors (Staged in high Z-space)
swarm_x = np.random.uniform(-400, 400, N_SWARM)
swarm_y = np.random.uniform(-100, 100, N_SWARM)
swarm_z = np.random.uniform(1000, 3000, N_SWARM) # Stacked in the void
swarm_speeds = np.random.uniform(40, 80, N_SWARM)
swarm_targets = np.random.randint(0, N_GOLD, N_SWARM) # Lock onto a legacy node

# Base grid for the ocean/surface plane
gx, gy = np.meshgrid(np.linspace(-500, 500, 15), np.linspace(-400, 400, 12))
grid_pts = np.column_stack([gx.flatten(), gy.flatten(), np.zeros_like(gx.flatten())])

def project_dimensional(x, y, z, tilt_factor):
    # tilt_factor = 0.0 : Perfect Top-Down 2D Matrix (Z is completely invisible)
    # tilt_factor = 1.0 : Isometric 3D Space (Z axis is stretched vertically)
    
    # 2D flat routing
    x_2d = x * 2.0
    y_2d = y * 2.0
    
    # 3D isometric tilt routing
    x_3d = x * 1.5 - y * 0.8
    y_3d = y * 1.0 + x * 0.4 + (z * 1.5)
    
    # Interpolative Dimensional Override
    xs = 540 + ((1.0 - tilt_factor) * x_2d) + (tilt_factor * x_3d)
    ys = 1100 + ((1.0 - tilt_factor) * y_2d) + (tilt_factor * y_3d)
    
    return xs, ys

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (ISOLATED MEMORY NODE)
# ------------------------------------------------------------------
def render_frame(data_packet):
    # HOTFIX ENFORCED: Strict Tuple Unpacking Array
    f, t_sec, state_str, ui_col, dim_text, tilt, g_alive, s_x, s_y, s_z, blooms, xy_pulses = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # 1. RENDER SURFACE TOPOLOGY (THE GRID)
    gx_sc, gy_sc = project_dimensional(grid_pts[:,0], grid_pts[:,1], grid_pts[:,2], tilt)
    ax.scatter(gx_sc, gy_sc, s=4, c=C_DIM, alpha=0.6, zorder=1)

    # 2. THE 2D LEGACY MATHEMATICS (GOLD PULSES)
    if tilt < 0.9:
        for (px, py, radius, alpha) in xy_pulses:
            if alpha > 0:
                p_xs, p_ys = project_dimensional(np.array([px]), np.array([py]), np.array([0]), tilt)
                circ_rad = radius * (1.0 - tilt*0.5) * 15 # Squash pulse in 3D
                c_p_rgba = hex_to_rgba(C_GOLD, np.clip(alpha, 0.0, 1.0))
                ax.scatter(p_xs, p_ys, s=circ_rad, facecolors='none', edgecolors=c_p_rgba, lw=2, zorder=2)

    # 3. RENDER THE LEGACY FLEET (C_GOLD)
    g_act_x = gold_bases_x[g_alive]
    g_act_y = gold_bases_y[g_alive]
    if len(g_act_x) > 0:
        g_sc_x, g_sc_y = project_dimensional(g_act_x, g_act_y, np.zeros_like(g_act_x), tilt)
        ax.scatter(g_sc_x, g_sc_y, s=150, color=C_GOLD, marker='D', zorder=4)
        ax.scatter(g_sc_x, g_sc_y, s=400, facecolors='none', edgecolors=C_GOLD, lw=2, alpha=0.5, zorder=3)

    # 4. THE DIMENSIONAL OVERRIDE (3D CYAN SWARM)
    # Only render when Z is entering visible geometry or tilt makes it apparent
    z_vis_mask = (s_z > 0) & (s_z < 1500)
    if tilt > 0.05 and np.any(z_vis_mask):
        sx_vis = s_x[z_vis_mask]
        sy_vis = s_y[z_vis_mask]
        sz_vis = s_z[z_vis_mask]
        
        sw_sc_x, sw_sc_y = project_dimensional(sx_vis, sy_vis, sz_vis, tilt)
        
        # Draw motion trails (extrapolating back up the Z axis)
        tail_z = sz_vis + 80
        sw_tail_x, sw_tail_y = project_dimensional(sx_vis, sy_vis, tail_z, tilt)
        
        lines = [[(sw_sc_x[i], sw_sc_y[i]), (sw_tail_x[i], sw_tail_y[i])] for i in range(len(sx_vis))]
        from matplotlib.collections import LineCollection
        lc = LineCollection(lines, color=C_CYAN, lw=2.0, alpha=0.7, zorder=6)
        ax.add_collection(lc)
        
        # Kinetic heads
        ax.scatter(sw_sc_x, sw_sc_y, s=15, color=C_TEXT, zorder=7)

    # 5. STRUCTURAL DELETION BLOOMS
    if len(blooms) > 0:
        b_arr = np.array(blooms)
        bx, by = project_dimensional(b_arr[:,0], b_arr[:,1], np.zeros(len(b_arr)), tilt)
        alphas = np.clip(b_arr[:,2], 0.0, 1.0)
        sizes = (1.0 - alphas) * 600 + 50
        
        c_mag = np.zeros((len(alphas), 4))
        c_mag[:, 0:3] = hex_to_rgba(C_MAGENTA)[0:3]
        c_mag[:, 3] = alphas
        ax.scatter(bx, by, s=sizes, c=c_mag, marker='h', zorder=8)
        
        c_red = np.zeros((len(alphas), 4))
        c_red[:, 0:3] = hex_to_rgba(C_RED)[0:3]
        c_red[:, 3] = np.clip(alphas * 0.4, 0.0, 1.0)
        ax.scatter(bx, by, s=sizes*2.0, c=c_red, edgecolors='none', zorder=7)

    # 6. TELEMETRY WIDGETS
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.9))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2)
    ax.text(0.04, 0.965, "LOGIC GARDEN 173 :: ARCHITECTURAL OBSOLESCENCE", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    # Dimension Status Panel
    ax.text(0.04, 0.88, f"ALGORITHMIC TOPOLOGY:", transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace')
    ax.text(0.04, 0.85, f"{dim_text}", transform=ax.transAxes, color=C_CYAN if tilt > 0.5 else C_GOLD, fontsize=24, fontname='monospace', weight='bold')

    survivors = np.sum(g_alive)
    ax.text(0.04, 0.80, f"LEGACY BOUNDING BOX INTEGRITY: {survivors}/{N_GOLD}", transform=ax.transAxes, color=C_MANTIS if survivors > 0 else C_RED, fontsize=20, fontname='monospace')

    # Bottom Terminal
    ax.add_patch(plt.Rectangle((0, 0), 0.95, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 0.95], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2)
    
    pulse = ui_col if (f % 60 < 30) or ui_col == C_MANTIS else C_TEXT
    ax.text(0.04, 0.08, "SYSTEM PERSPECTIVE:", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=24, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf(); plt.close(fig); plt.close('all'); gc.collect() 
    return f

# ------------------------------------------------------------------
# PHYSICS ENGINE (DIMENSIONAL UPGRADE KINEMATICS)
# ------------------------------------------------------------------
def generate_physics_stream():
    g_alive = np.ones(N_GOLD, dtype=bool)
    sz = swarm_z.copy()
    sx = swarm_x.copy()
    sy = swarm_y.copy()
    
    blooms = []        # [x, y, alpha]
    xy_pulses = []     # [x, y, radius, alpha]
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        blooms = [[x,y, a-0.03] for x,y,a in blooms if a > 0.05]
        xy_pulses = [[x,y, r+5.0, a-0.04] for x,y,r,a in xy_pulses if a > 0.05]

        # ---------------------------------------------------
        # PHASE 1: SUPREMACY IN A FLAT 2D WORLD
        # ---------------------------------------------------
        if t_sec < 10.0:
            tilt = 0.0
            state = "[01] CONTINUOUS OPTIMIZATION OF X-Y MATRIX"
            ui_col = C_GOLD
            dim_text = "[ DIMENSION: 2D FLAT SURFACE ]"
            
            # Gold array is "executing perfect math" in 2D
            if f % 15 == 0:
                xy_pulses.append([0, 0, 10.0, 1.0])

        # ---------------------------------------------------
        # PHASE 2: THE OPERATING SYSTEM UPGRADES
        # ---------------------------------------------------
        elif t_sec < 16.0:
            # Smoothly transition from 0.0 to 1.0 using S-curve
            norm_t = (t_sec - 10.0) / 6.0
            tilt = norm_t * norm_t * (3.0 - 2.0 * norm_t)
            state = "[02] DIMENSIONAL COMPILER OVERRIDE"
            ui_col = C_DIM
            dim_text = "[ !! HARDWARE GEOMETRY AUGMENTATION !! ]"

        # ---------------------------------------------------
        # PHASE 3: THE EXO-ATMOSPHERIC SWARM (3D Z-AXIS)
        # ---------------------------------------------------
        elif t_sec < 28.0:
            tilt = 1.0
            state = "[03] TERMINAL Z-AXIS VULNERABILITY EXPOSED"
            ui_col = C_CYAN
            dim_text = "[ DIMENSION: 3D EXO-ATMOSPHERIC ]"
            
            # Swarm falls rapidly. Target acquisition active.
            dt = 1.0 / FPS
            for i in range(N_SWARM):
                if sz[i] > 0:
                    sz[i] -= swarm_speeds[i] * dt * 90.0
                    
                    # Seek X/Y of locked target
                    target_idx = swarm_targets[i]
                    if g_alive[target_idx]:
                        tx, ty = gold_bases_x[target_idx], gold_bases_y[target_idx]
                        dx, dy = tx - sx[i], ty - sy[i]
                        mag = math.sqrt(dx**2 + dy**2) + 0.001
                        # Hypersonic curve inward
                        sx[i] += (dx/mag) * swarm_speeds[i] * dt * 10.0
                        sy[i] += (dy/mag) * swarm_speeds[i] * dt * 10.0
                    
                    if sz[i] <= 0.0 and g_alive[target_idx]:
                        # Kinetic Impact
                        g_alive[target_idx] = False
                        blooms.append([gold_bases_x[target_idx], gold_bases_y[target_idx], 1.0])
                        # Additional redundant swarm vectors just crash harmlessly to add chaos

        # ---------------------------------------------------
        # PHASE 4: TATHĀTĀ
        # ---------------------------------------------------
        else:
            tilt = 1.0
            state = "[04] TATHĀTĀ: LEGACY MATRIX DELETED"
            ui_col = C_MANTIS
            dim_text = "[ SYSTEM PURGED OF OBSOLETE ARCHITECTURE ]"

        yield (f, t_sec, state, ui_col, dim_text, tilt, g_alive.copy(), sx.copy(), sy.copy(), sz.copy(), blooms.copy(), xy_pulses.copy())

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 173: ARCHITECTURAL OBSOLESCENCE [CORES: {cpu_cores}]")
    print(f"Loading {N_SWARM} Exo-Swarm Vectors & {N_GOLD} Legacy Nodes.")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
