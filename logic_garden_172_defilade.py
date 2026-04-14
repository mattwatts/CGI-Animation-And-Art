"""
SOVEREIGN CODE: logic_garden_172_defilade.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / 3D Topological Matrix (35 seconds)
SCENE: Logic Garden 172 (The Topological Override / Defilade to Enfilade)
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
OUT_DIR = "frames_172_defilade"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_DIM     = '#1A1A24'          # Topographic Matrix Mesh
C_CYAN    = '#00FFFF'          # Defeated Vectors (Defilade Frontal Assault)
C_RED     = '#FF0033'          # Entropy Bloom (Kinetic Shadow Intercepts)
C_GOLD    = '#FFD700'          # Sovereign Flank Node
C_MANTIS  = '#00FF00'          # The Enfilade Erasure Beam
C_MAGENTA = '#FF00FF'          # Terminal Node Evaporation

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# 3D TOPOGRAPHICAL ARCHITECTURE (THE SHIELD / THE CAGE)
# ------------------------------------------------------------------
np.random.seed(172)

# Point Cloud Terrain Generation (LiDAR Matrix aesthetic)
X_DIM, Y_DIM = 90, 140
xi = np.linspace(-250, 250, X_DIM)
yi = np.linspace(-300, 300, Y_DIM)
xg, yg = np.meshgrid(xi, yi)

# Mathematical Terrain: A steep ridge at X = -50, a deep trench at X = 50
# Left flank = high elevation, Right flank = flat.
zg = 180.0 * np.exp(-((xg + 50)**2) / 1200.0) # The Shield (Ridge)
zg += 20.0 * np.sin(yg * 0.05) + 15.0 * np.cos(xg * 0.08) # Fractal Noise

terr_x = xg.flatten()
terr_y = yg.flatten()
terr_z = zg.flatten()

# Defender Array located deep in the trench (X=50, Y spaced out)
N_TARGETS = 180
targ_x = np.random.normal(50, 15, N_TARGETS) # Clustered in the trench
targ_y = np.linspace(-200, 200, N_TARGETS)
targ_z = np.zeros(N_TARGETS)
for i in range(N_TARGETS):
    # Map their height to the terrain floor
    dist = (terr_x - targ_x[i])**2 + (terr_y - targ_y[i])**2
    targ_z[i] = terr_z[np.argmin(dist)] + 5.0

def project_3d(points, pitch, yaw):
    cp, sp = math.cos(pitch), math.sin(pitch)
    cy, sy = math.cos(yaw), math.sin(yaw)
    
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rx = np.array([[1, 0, 0], [0, cp, -sp], [0, sp, cp]])
    
    rot = points @ Ry.T @ Rx.T
    
    # 9:16 Screen Calibration
    xs = 540 + rot[:, 0] * 1.6 - rot[:, 2] * 0.5
    ys = 1100 + rot[:, 1] * 1.5 + rot[:, 2] * 1.2
    return xs, ys, rot[:, 2]

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (ISOLATED MEMORY NODE)
# ------------------------------------------------------------------
def render_frame(data_packet):
    # HOTFIX ENFORCED: Strict payload mapping array
    f, t_sec, state_str, ui_col, rot_p, rot_y, cyan_lines, red_blooms, gold_lines, mag_blooms, p_alive, g_pos, eff_ratio = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # 1. RENDER TOPOLOGICAL MATRIX (LiDAR POINT CLOUD)
    t_pts = np.column_stack((terr_x, terr_y, terr_z))
    t_xs, t_ys, t_depth = project_3d(t_pts, rot_p, rot_y)
    
    # Terrain fading algorithm based on depth
    z_norm = np.clip((t_depth - np.min(t_depth)) / (np.max(t_depth) - np.min(t_depth) + 0.01), 0, 1)
    t_colors = np.zeros((len(t_pts), 4))
    t_colors[:, 0:3] = hex_to_rgba(C_DIM)[0:3]
    t_colors[:, 3] = np.clip(1.0 - (z_norm * 0.6), 0.1, 0.5) # Deeper points fade out
    
    # Render ridge caps brighter
    ridge_mask = terr_x < -20
    t_colors[ridge_mask, 0:3] = hex_to_rgba(C_TEXT)[0:3]
    t_colors[ridge_mask, 3] = np.clip(t_colors[ridge_mask, 3] * 1.5, 0.0, 0.4)
    
    ax.scatter(t_xs, t_ys, s=2, c=t_colors, edgecolors='none', zorder=1)

    # 2. RENDER THE TARGET ARRAY (IN THE TRENCH)
    if np.any(p_alive):
        alive_idx = np.where(p_alive)[0]
        alive_pts = np.column_stack((targ_x[alive_idx], targ_y[alive_idx], targ_z[alive_idx]))
        a_xs, a_ys, _ = project_3d(alive_pts, rot_p, rot_y)
        ax.scatter(a_xs, a_ys, s=25, c=C_TEXT, marker='X', alpha=0.9, zorder=4)

    # 3. PHASE 1 KINEMATICS: CYAN DEFILADE STRIKES
    for (start_p, end_p) in cyan_lines:
        line_pts = np.array([start_p, end_p])
        lx, ly, _ = project_3d(line_pts, rot_p, rot_y)
        ax.plot(lx, ly, color=C_CYAN, lw=1.5, alpha=0.6, zorder=5)
        
    for (rx, ry, rz, alpha) in red_blooms:
        b_pt = np.array([[rx, ry, rz]])
        bx, by, _ = project_3d(b_pt, rot_p, rot_y)
        c_red_rgba = hex_to_rgba(C_RED, np.clip(alpha, 0.0, 1.0))
        ax.scatter(bx, by, s=200 * alpha, color=c_red_rgba, edgecolors='none', zorder=6)

    # 4. SOVEREIGN NODE MANEUVER (THE GOLD PIVOT)
    g_pt = np.array([g_pos])
    g_sx, g_sy, _ = project_3d(g_pt, rot_p, rot_y)
    ax.scatter(g_sx, g_sy, s=200, color=C_GOLD, marker='D', zorder=10)
    ax.scatter(g_sx, g_sy, s=600, facecolors='none', edgecolors=C_GOLD, lw=2, alpha=0.6, zorder=9)

    # 5. PHASE 3 KINEMATICS: MANTIS ENFILADE ERASURE
    for (start_p, end_p) in gold_lines:
        line_pts = np.array([start_p, end_p])
        lx, ly, _ = project_3d(line_pts, rot_p, rot_y)
        ax.plot(lx, ly, color=C_MANTIS, lw=5, alpha=0.9, zorder=8)
        ax.plot(lx, ly, color=C_TEXT, lw=2, alpha=1.0, zorder=9)

    for (mx, my, mz, alpha) in mag_blooms:
        b_pt = np.array([[mx, my, mz]])
        bx, by, _ = project_3d(b_pt, rot_p, rot_y)
        c_mag_rgba = hex_to_rgba(C_MAGENTA, np.clip(alpha, 0.0, 1.0))
        ax.scatter(bx, by, s=400 * alpha, color=c_mag_rgba, marker='h', edgecolors='none', zorder=11)
        # Red kinetic flash
        c_rf = hex_to_rgba(C_TEXT, np.clip(alpha*0.5, 0.0, 1.0))
        ax.scatter(bx, by, s=150 * alpha, color=c_rf, edgecolors='none', zorder=12)

    # 6. TELEMETRY WIDGETS
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.9))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2)
    ax.text(0.04, 0.965, "LOGIC GARDEN 172 :: Z-AXIS NULLIFICATION", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    # Physics Panel
    survivors = np.sum(p_alive)
    surv_pct = (survivors / N_TARGETS) * 100.0

    ax.text(0.04, 0.88, f"BOUNDING BOX EFFICIENCY:", transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace')
    ax.text(0.04, 0.85, f"{eff_ratio}", transform=ax.transAxes, color=C_CYAN if ui_col==C_VOID else ui_col, fontsize=22, fontname='monospace', weight='bold')
    
    ax.text(0.04, 0.81, f"TRENCH INTEGRITY: {surv_pct:>05.1f}%", transform=ax.transAxes, color=C_MANTIS if survivors > 10 else C_RED, fontsize=20, fontname='monospace')

    # Bottom Terminal
    ax.add_patch(plt.Rectangle((0, 0), 0.95, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 0.95], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2)
    
    pulse = ui_col if (f % 60 < 30) or ui_col == C_MANTIS else C_TEXT
    ax.text(0.04, 0.08, "GEOMETRIC PERSPECTIVE:", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=24, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf(); plt.close(fig); plt.close('all'); gc.collect() 
    return f

# ------------------------------------------------------------------
# PHYSICS ENGINE (TOPOLOGICAL KINEMATICS)
# ------------------------------------------------------------------
def generate_physics_stream():
    p_alive = np.ones(N_TARGETS, dtype=bool)
    red_blooms = []     # (x, y, z, alpha)
    mag_blooms = []     # (x, y, z, alpha)
    
    # Gold Sovereign starts out of position (flanking)
    g_pos_list = []
    # Interpolate path from Flank to Enfilade firing position
    for t in np.linspace(0, 1, int(FPS * 8.0)):
        # Arc translation
        gx = -200 + (250 * t) 
        gy = 0 - (300 * t)     
        gz = 200 + (50 * t)
        g_pos_list.append([gx, gy, gz])
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        # Smooth camera rotation to map the geometry discovery
        rot_y = 0.5 + (math.sin(t_sec * 0.15) * 0.4)
        rot_p = 0.6 + (math.cos(t_sec * 0.1) * 0.1)
        
        cyan_lines = []
        gold_lines = []
        
        # Alpha Decay for Blooms
        red_blooms = [[x,y,z, a-0.05] for x,y,z,a in red_blooms if a > 0.05]
        mag_blooms = [[x,y,z, a-0.03] for x,y,z,a in mag_blooms if a > 0.03]

        g_pos = g_pos_list[-1] if f >= len(g_pos_list) else g_pos_list[f]

        # ---------------------------------------------------
        # PHASE 1: THE SHIELD (DEFILADE)
        # ---------------------------------------------------
        if t_sec < 14.0:
            state = "[01] DEFILADE SECURE (THE RIDGE AS SHIELD)"
            ui_col = C_VOID
            eff_ratio = "99.9% [KINETIC SHADOW ACTIVE]"
            
            # Fire Cyan vectors from X = -250 towards X = 50
            if f % 2 == 0:
                for _ in range(3):
                    start_y = np.random.uniform(-200, 200)
                    start_z = np.random.uniform(100, 250)
                    end_str = [50, start_y, 0] # Aiming for the valley
                    
                    # Intersect Mathematics: Hits the ridge at X ≈ -50
                    hit_x = np.random.uniform(-70, -30)
                    hit_z = 180.0 * np.exp(-((hit_x + 50)**2) / 1200.0) + np.random.uniform(0,30)
                    
                    cyan_lines.append(([-250, start_y, start_z], [hit_x, start_y, hit_z]))
                    red_blooms.append([hit_x, start_y, hit_z, 1.0])

        # ---------------------------------------------------
        # PHASE 2: THE MANEUVER (THE FLANK)
        # ---------------------------------------------------
        elif t_sec < 22.0:
            state = "[02] ORTHOGONAL FLANK (GEOMETRY COMPROMISED)"
            ui_col = C_GOLD
            eff_ratio = "WARNING: PERSPECTIVE ALIGNMENT SHIFT"

        # ---------------------------------------------------
        # PHASE 3: THE CAGE (ENFILADE)
        # ---------------------------------------------------
        else:
            state = "[03] TATHĀTĀ: THE PIVOT MAKES THE SHIELD A CAGE"
            ui_col = C_MANTIS
            eff_ratio = "0.0% [STRUCTURAL TRAP EXECUTED]"
            
            # Erase Nodes based on Y position (sweeping down the trench)
            sweep_y = -300 + ((t_sec - 22.0) * 120)
            
            if sweep_y > -300 and sweep_y < 300:
                gold_lines.append((g_pos, [50, sweep_y, 0]))
                
                # Sift collision targets
                hit_mask = p_alive & (targ_y < sweep_y)
                if np.any(hit_mask):
                    new_hits = np.where(hit_mask)[0]
                    p_alive[hit_mask] = False
                    for idx in new_hits:
                        mag_blooms.append([targ_x[idx], targ_y[idx], targ_z[idx], 1.0])

        yield (f, t_sec, state, ui_col, rot_p, rot_y, cyan_lines, red_blooms, gold_lines, mag_blooms, p_alive.copy(), g_pos, eff_ratio)

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 172: THE TOPOLOGICAL OVERRIDE [CORES: {cpu_cores}]")
    print(f"Tracking 3D Terrain Matrix Geometry.")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
