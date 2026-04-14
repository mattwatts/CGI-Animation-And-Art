"""
SOVEREIGN CODE: logic_garden_170_enfilade.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / 3D Kinematic Erasure (35 seconds)
SCENE: Logic Garden 170 (The Orthogonal Sweep / Raking Fire)
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
OUT_DIR = "frames_170_enfilade"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_DIM     = '#1A1A24'          # Hardware Mesh (The Bounding Box)
C_CYAN    = '#00FFFF'          # Broadside Control Vector (High Friction)
C_GOLD    = '#FFD700'          # The Enfilade Vector (Sovereign Override)
C_MAGENTA = '#FF00FF'          # Cascading Node Erasure
C_RED     = '#FF0033'          # Entropy Bloom (Friction limits)
C_MANTIS  = '#00FF00'          # Terminal Green Flow

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# 3D SYSTEM ARCHITECTURE (THE SHIP-OF-THE-LINE MATRIX)
# ------------------------------------------------------------------
np.random.seed(170)

# Generate a massive rectangular prism (9 x 9 x 60 = 4,860 Nodes)
X_DIM, Y_DIM, Z_DIM = 9, 9, 60
xi = np.linspace(-60, 60, X_DIM)
yi = np.linspace(-60, 60, Y_DIM)
zi = np.linspace(-500, 500, Z_DIM)

xx, yy, zz = np.meshgrid(xi, yi, zi)
base_nodes = np.vstack([xx.flatten(), yy.flatten(), zz.flatten()]).T
N_NODES = len(base_nodes)

def project_3d(points, pitch, yaw):
    cp, sp = math.cos(pitch), math.sin(pitch)
    cy, sy = math.cos(yaw), math.sin(yaw)
    
    # Static Roll, dynamic Yaw/Pitch
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rx = np.array([[1, 0, 0], [0, cp, -sp], [0, sp, cp]])
    
    rot = points @ Ry.T @ Rx.T
    
    # 9:16 Isometric Map Scaling
    # Rotate diagonally across the screen to maximize Z-axis depth perception
    xs = 540 + rot[:, 0] * 1.5 - rot[:, 2] * 0.6
    ys = 960 + rot[:, 1] * 1.5 + rot[:, 2] * 0.8
    zs = rot[:, 2] # Depth sorting buffer
    return xs, ys, zs

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (ISOLATED MEMORY NODE)
# ------------------------------------------------------------------
def render_frame(data_packet):
    f, t_sec, state_str, ui_col, rot_p, rot_y, p_alive, cyan_beams, gold_beam, mag_blooms, eff_stat = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # 1. 3D PROJECTION & DEPTH SORTING
    xs, ys, depth = project_3d(base_nodes, rot_p, rot_y)
    
    # Render alive nodes (Inner structure vs Outer Hull)
    alive_idx = np.where(p_alive)[0]
    if len(alive_idx) > 0:
        a_xs = xs[alive_idx]
        a_ys = ys[alive_idx]
        a_depth = depth[alive_idx]
        
        # Sort by depth back-to-front
        sort_order = np.argsort(a_depth)
        s_xs = a_xs[sort_order]
        s_ys = a_ys[sort_order]
        
        # Core is dim, edges are lightly highlighted (Text)
        ax.scatter(s_xs, s_ys, s=8, c=C_DIM, zorder=2)
        ax.scatter(s_xs, s_ys, s=1, c=C_TEXT, alpha=0.3, zorder=3)

    # 2. BROADSIDE TRANSIENTS (THE CYAN FRICTION)
    for (start_pos, end_pos) in cyan_beams:
        # Project beam end points
        b_pts = np.array([start_pos, end_pos])
        bx, by, _ = project_3d(b_pts, rot_p, rot_y)
        
        # The vector line
        ax.plot(bx, by, color=C_CYAN, lw=3, zorder=5)
        # The friction bloom (stopped by armor)
        ax.scatter([bx[1]], [by[1]], s=300, color=C_RED, alpha=0.4, zorder=6)
        ax.scatter([bx[1]], [by[1]], s=50, color=C_TEXT, marker='x', zorder=7)

    # 3. THE ENFILADE STRIKE (THE GOLD SOVEREIGN OVERRIDE)
    if gold_beam is not None:
        (g_start, g_end) = gold_beam
        g_pts = np.array([g_start, g_end])
        gx, gy, _ = project_3d(g_pts, rot_p, rot_y)
        
        ax.plot(gx, gy, color=C_GOLD, lw=6, zorder=8)
        ax.plot(gx, gy, color=C_TEXT, lw=2, zorder=9)
        # Penetration core
        ax.scatter([gx[1]], [gy[1]], s=800, color=C_GOLD, alpha=0.3, zorder=8)

    # 4. KINETIC CASCADE (MAGENTA DELETION BLOOMS)
    if len(mag_blooms) > 0:
        mb = np.array(mag_blooms)
        mx, my, _ = project_3d(mb[:, 0:3], rot_p, rot_y)
        
        # HOTFIX: Strict clipping to eliminate float drift (-1e-16 or 1.0001)
        alphas = np.clip(mb[:, 3], 0.0, 1.0)
        sizes = (1.0 - alphas) * 200 + 20
        
        # Magenta Bloom Assignment
        c_mag = np.zeros((len(alphas), 4))
        c_mag[:, 0:3] = hex_to_rgba(C_MAGENTA)[0:3]
        c_mag[:, 3] = alphas
        ax.scatter(mx, my, s=sizes, c=c_mag, zorder=10)
        
        # Stray Red Entropy Alignment (Replaces buggy scalar alpha mapping)
        c_reds = np.zeros((len(alphas), 4))
        c_reds[:, 0:3] = hex_to_rgba(C_RED)[0:3]
        c_reds[:, 3] = np.clip(alphas * 0.3, 0.0, 1.0)
        ax.scatter(mx, my, s=sizes*1.5, c=c_reds, zorder=9)

    # 5. TELEMETRY WIDGETS
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.9))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2)
    ax.text(0.04, 0.965, "LOGIC GARDEN 170 :: THE ORTHOGONAL SWEEP", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    # Physics Panel
    active_count = np.sum(p_alive)
    erased = N_NODES - active_count
    integ = (active_count / float(N_NODES)) * 100.0

    ax.text(0.04, 0.88, f"BOUNDING BOX INTEGRITY: {integ:>05.1f}%", transform=ax.transAxes, color=C_MANTIS if integ > 95 else C_RED, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.85, f"LOCAL NODES ERASED    : {erased:>04d}", transform=ax.transAxes, color=C_MAGENTA if erased > 20 else C_TEXT, fontsize=20, fontname='monospace')
    
    ax.text(0.04, 0.81, f"VECTOR EFFICACY MULTIPLIER:", transform=ax.transAxes, color=C_GOLD, fontsize=18, fontname='monospace')
    ax.text(0.04, 0.78, f"{eff_stat}", transform=ax.transAxes, color=C_TEXT, fontsize=22, fontname='monospace', weight='bold')

    # Bottom Terminal
    ax.add_patch(plt.Rectangle((0, 0), 0.95, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 0.95], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2)
    
    pulse = ui_col if (f % 60 < 30) or ui_col == C_MANTIS else C_TEXT
    ax.text(0.04, 0.08, "KINEMATIC PROTOCOL:", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=24, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf(); plt.close(fig); plt.close('all'); gc.collect() 
    return f

# ------------------------------------------------------------------
# PHYSICS ENGINE (TOPOLOGICAL KINEMATICS)
# ------------------------------------------------------------------
def generate_physics_stream():
    p_alive = np.ones(N_NODES, dtype=bool)
    mag_blooms = [] # [x, y, z, alpha]
    
    # Beam Event Triggers
    c1_fire, c2_fire, c3_fire = 3.0, 6.0, 9.0
    g_fire = 15.0
    
    base_yaw = 0.6
    base_pitch = 0.3

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        # Slow industrial rotation to present the geometry
        rot_y = base_yaw + (math.sin(t_sec * 0.2) * 0.15)
        rot_p = base_pitch + (math.cos(t_sec * 0.1) * 0.05)
        
        cyan_beams = []
        gold_beam = None
        eff_stat = "[WAITING]"
        
        # Decay blooms
        next_blooms = []
        for mb in mag_blooms:
            mb[3] -= 0.03 # Fade out
            if mb[3] > 0:
                next_blooms.append(mb)
        mag_blooms = next_blooms

        # ---------------------------------------------------
        # PHASE 1: BROADSIDE (ARTISAN FRICTION)
        # ---------------------------------------------------
        if t_sec < 13.0:
            state = "[01] BROADSIDE VECTOR (STRUCTURAL FRICTION)"
            ui_col = C_CYAN
            
            def process_cyan(start_t, head_z):
                dt = t_sec - start_t
                if 0 <= dt < 1.0:
                    v_speed = 300.0
                    cur_x = 200.0 - (dt * v_speed)
                    # Broadside hits side at X=60
                    cur_x = max(cur_x, 40) 
                    cyan_beams.append(([200, 0, head_z], [cur_x, 0, head_z]))
                    eff_stat = "LOW [TRANSVERSE STOPPAGE]"
                    
                    if cur_x == 40:
                        # Erase 3-4 nodes on edge
                        hit_mask = p_alive & (base_nodes[:,0] > 40) & (np.abs(base_nodes[:,1]) < 15) & (np.abs(base_nodes[:,2] - head_z) < 20)
                        if np.any(hit_mask):
                            p_alive[hit_mask] = False
                            for hn in base_nodes[hit_mask]:
                                mag_blooms.append([hn[0], hn[1], hn[2], 1.0])
            
            process_cyan(c1_fire, 200)
            process_cyan(c2_fire, 0)
            process_cyan(c3_fire, -200)

        # ---------------------------------------------------
        # PHASE 2: ENFILADE OVERRIDE (THE LONGITUDINAL SWEEP)
        # ---------------------------------------------------
        elif t_sec < 28.0:
            state = "[02] ENFILADE STRIKE (RECURSIVE LIABILITY)"
            ui_col = C_GOLD
            eff_stat = "MAXIMUM [O(N) ALIGNMENT]"
            
            dt = t_sec - g_fire
            if dt > 0:
                v_speed = 220.0
                cur_z = 600 - (dt * v_speed)
                cur_z = max(cur_z, -600.0)
                
                gold_beam = ([0, 0, 600], [0, 0, cur_z])
                
                if cur_z > -600:
                    # Instantly hollow out the core radius
                    hit_mask = p_alive & (base_nodes[:,2] > cur_z) & (base_nodes[:,2] < cur_z + 40) & ((base_nodes[:,0]**2 + base_nodes[:,1]**2) < 40**2)
                    if np.any(hit_mask):
                        p_alive[hit_mask] = False
                        for hn in base_nodes[hit_mask]:
                            # Random chance to spawn a major visual bloom to save render time, mostly pure erasure
                            if np.random.rand() < 0.3:
                                mag_blooms.append([hn[0] + np.random.uniform(-10,10), 
                                                   hn[1] + np.random.uniform(-10,10), 
                                                   hn[2], 1.0])

        # ---------------------------------------------------
        # PHASE 3: TATHĀTĀ
        # ---------------------------------------------------
        else:
            state = "[03] TATHĀTĀ: DEPTH MATHEMATICALLY HOLLOWED"
            ui_col = C_MANTIS
            eff_stat = "COMPLETE [TERMINAL FLOW]"

        yield (f, t_sec, state, ui_col, rot_p, rot_y, p_alive.copy(), cyan_beams, gold_beam, mag_blooms.copy(), eff_stat)

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 170: THE ORTHOGONAL SWEEP [CORES: {cpu_cores}]")
    print(f"Tracking 3D Topologies: {N_NODES} Structural Nodes.")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
