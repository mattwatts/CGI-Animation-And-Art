"""
SOVEREIGN CODE: logic_garden_176_xaver1000.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / 3D UWB Radar Simulation (35 seconds)
SCENE: Logic Garden 176 (The Camero Xaver / Algorithmic Penetration)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import LineCollection
import multiprocessing as mp
import os
import gc
import math

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 35                   
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_176_xaver1000"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_DIM     = '#1A1A24'          # Physical Concrete Wall
C_CYAN    = '#00FFFF'          # UWB Propagation Waves
C_MAGENTA = '#FF00FF'          # Raw Dielectric Point Cloud Echo
C_GOLD    = '#FFD700'          # AI-Resolved Skeletal Wireframe
C_MANTIS  = '#00FF00'          # Terminal Posture Lock
C_RED     = '#FF0033'          # Electromagnetic Friction

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE WALL, THE RADAR, THE TARGET
# ------------------------------------------------------------------
np.random.seed(176)

# 1. The Concrete Wall (Bounding Box)
wall_x = np.random.uniform(-400, 400, 3000)
wall_y = np.random.uniform(-100, -50, 3000)  # Wall Depth
wall_z = np.random.uniform(0, 400, 3000)

# 2. The Radar Source (Xaver 1000 Node)
radar_pos = np.array([0.0, -350.0, 150.0])

# 3. The Biological Target (Humanoid Point Cloud)
N_BIO = 2500
t_x, t_y, t_z = [], [], []

def add_cluster(cx, cy, cz, rx, ry, rz, count):
    t_x.extend(np.random.normal(cx, rx, count))
    t_y.extend(np.random.normal(cy, ry, count))
    t_z.extend(np.random.normal(cz, rz, count))

# Generating Posture: Crouching/Tactical Stance behind wall (y = 200)
add_cluster(0, 200, 180, 15, 15, 18, 400)    # Head
add_cluster(0, 210, 110, 35, 20, 45, 900)    # Torso
add_cluster(-35, 230, 90, 10, 15, 25, 300)   # Left Arm (Raised)
add_cluster(35, 200, 70, 10, 15, 35, 300)    # Right Arm (Lowered)
add_cluster(-20, 210, 35, 18, 20, 35, 300)   # Left Leg (Crouched)
add_cluster(25, 240, 25, 18, 25, 25, 300)    # Right Leg (Kneeling)

bio_pts = np.column_stack((t_x, t_y, t_z))
# Pre-calculate distance to radar for O(1) wave intersections
bio_dist = np.sqrt(np.sum((bio_pts - radar_pos)**2, axis=1))

# HOTFIX: Skeletal Map explicit segment pairing (12 points total) ensures safety
skel_joints = [
    [0, 200, 180], [0, 210, 140],   # Head to Neck
    [0, 210, 140], [0, 210, 80],    # Neck to Pelvis
    [0, 210, 140], [-35, 230, 90],  # Neck to L Arm
    [0, 210, 140], [35, 200, 70],   # Neck to R Arm
    [0, 210, 80], [-20, 210, 35],   # Pelvis to L Leg
    [0, 210, 80], [25, 240, 25]     # Pelvis to R Leg
]

def project_3d(points, pitch, yaw):
    points = np.atleast_2d(points)
    cp, sp = math.cos(pitch), math.sin(pitch)
    cy, sy = math.cos(yaw), math.sin(yaw)
    
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rx = np.array([[1, 0, 0], [0, cp, -sp], [0, sp, cp]])
    
    rot = points @ Ry.T @ Rx.T
    
    xs = 540 + rot[:, 0] * 1.8 - rot[:, 2] * 0.5
    ys = 900 + rot[:, 1] * 1.4 + rot[:, 2] * 1.5
    return xs, ys, rot[:, 2]

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(data_packet):
    # STRICT TUPLE UNPACKING
    f, t_sec, state_str, ui_col, rot_p, rot_y, wave_radii, echo_alphas, ai_confidence, skel_alpha = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # 1. RENDER THE CONCRETE BOUNDARY
    wx, wy, wz = project_3d(np.column_stack((wall_x, wall_y, wall_z)), rot_p, rot_y)
    
    # Wall turns mathematically "transparent" when radar is active
    wall_alpha = 0.8 if t_sec < 6.0 else max(0.1, 0.8 - ((t_sec - 6.0) * 0.4))
    
    c_wall = np.zeros((len(wx), 4))
    c_wall[:, 0:3] = hex_to_rgba(C_DIM)[0:3]
    c_wall[:, 3] = wall_alpha
    ax.scatter(wx, wy, s=8, c=c_wall, edgecolors='none', zorder=4)

    # 2. RENDER THE RADAR NODE
    rx, ry, _ = project_3d(radar_pos, rot_p, rot_y)
    ax.scatter(rx, ry, s=200, c=C_CYAN if ui_col != C_VOID else C_DIM, marker='D', zorder=6)
    
    # 3. UWB EMISSION WAVES (THE DIELECTRIC PENETRATION)
    if len(wave_radii) > 0:
        for rad in wave_radii:
            if rad > 0 and rad < 1200:
                angles = np.linspace(-np.pi/3, np.pi/3, 50)
                arc_x = radar_pos[0] + rad * np.sin(angles)
                arc_y = radar_pos[1] + rad * np.cos(angles)
                arc_z = np.full_like(arc_x, radar_pos[2])
                
                awx, awy, _ = project_3d(np.column_stack((arc_x, arc_y, arc_z)), rot_p, rot_y)
                ax.plot(awx, awy, color=C_CYAN, lw=2, alpha=0.4, zorder=5)

    # 4. RENDER THE BIOLOGICAL TARGET (ECHOES)
    b_xs, b_ys, b_zs = project_3d(bio_pts, rot_p, rot_y)
    
    if np.any(echo_alphas > 0.05):
        active_idx = np.where(echo_alphas > 0.05)[0]
        
        c_bio = np.zeros((len(active_idx), 4))
        # Color shifts from Magenta (Raw Scan) to Mantis (Locked)
        lock_ratio = np.clip(ai_confidence, 0.0, 1.0)
        
        c_mag = np.array(hex_to_rgba(C_MAGENTA)[0:3])
        c_man = np.array(hex_to_rgba(C_MANTIS)[0:3])
        inter_color = c_mag * (1.0 - lock_ratio) + c_man * lock_ratio
        
        c_bio[:, 0:3] = inter_color
        c_bio[:, 3] = np.clip(echo_alphas[active_idx], 0.0, 1.0)
        
        ax.scatter(b_xs[active_idx], b_ys[active_idx], s=12, c=c_bio, edgecolors='none', zorder=5)

    # 5. RENDER THE AI WIREFRAME (TATHĀTĀ)
    if skel_alpha > 0.05:
        skel_pts = np.array(skel_joints)
        sx, sy, _ = project_3d(skel_pts, rot_p, rot_y)
        
        # HOTFIX ALIGNMENT: 12 nodes processes flawlessly in steps of 2.
        lines = [[(sx[i], sy[i]), (sx[i+1], sy[i+1])] for i in range(0, len(sx), 2)]
        lc = LineCollection(lines, color=hex_to_rgba(C_GOLD, skel_alpha), lw=4, zorder=7)
        ax.add_collection(lc)
        
        ax.scatter(sx, sy, s=150, c=C_GOLD, alpha=skel_alpha, edgecolors='none', zorder=8)
        ax.scatter(sx, sy, s=40, c=C_TEXT, alpha=skel_alpha, edgecolors='none', zorder=9)

    # 6. TELEMETRY WIDGETS
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.9))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2)
    ax.text(0.04, 0.965, "LOGIC GARDEN 176 :: UWB DIELECTRIC PENETRATION", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    # AI Processing Panel
    ax.text(0.04, 0.88, f"UWB TENSOR RESOLUTION:", transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace')
    
    conf_pct = ai_confidence * 100.0
    ax.text(0.04, 0.85, f"[{conf_pct:>05.1f}%] POINT-CLOUD SYNTHESIS", transform=ax.transAxes, color=ui_col, fontsize=22, fontname='monospace', weight='bold')
    
    if skel_alpha > 0.5:
        ax.text(0.04, 0.80, f"TARGET LOCKED: 1.7M | POSTURE: CROUCHING", transform=ax.transAxes, color=C_GOLD, fontsize=18, fontname='monospace', weight='bold')

    # Bottom Terminal
    ax.add_patch(plt.Rectangle((0, 0), 0.95, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 0.95], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2)
    
    pulse = ui_col if (f % 60 < 30) or ui_col == C_GOLD else C_TEXT
    ax.text(0.04, 0.08, "AI COMPILER STATUS:", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=24, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf(); plt.close(fig); plt.close('all'); gc.collect() 
    return f

# ------------------------------------------------------------------
# PHYSICS ENGINE (UWB PROPAGATION & AI SYNTHESIS)
# ------------------------------------------------------------------
def generate_physics_stream():
    echo_alphas = np.zeros(N_BIO)
    wave_radii = []
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        rot_y = -0.3 + (math.sin(t_sec * 0.2) * 0.5)
        rot_p = 0.5 + (math.cos(t_sec * 0.15) * 0.1)
        
        ai_confidence = 0.0
        skel_alpha = 0.0
        
        echo_alphas = np.clip(echo_alphas - (0.5 / FPS), 0.0, 1.0)
        
        speed = 800.0
        wave_radii = [r + (speed / FPS) for r in wave_radii]
        wave_radii = [r for r in wave_radii if r < 1200]

        if t_sec < 6.0:
            state = "[01] VISUAL SPECTRUM BLOCKED (STRUCTURAL OPACITY)"
            ui_col = C_VOID
            
        elif t_sec < 23.0:
            state = "[02] UWB EXCITATION: PENETRATING DIELECTRIC MESH"
            ui_col = C_CYAN
            
            if f % 12 == 0:
                wave_radii.append(0.0)
            
            for r in wave_radii:
                hits = np.abs(bio_dist - r) < 20.0
                echo_alphas[hits] = 1.0
                
            ai_confidence = np.clip((t_sec - 10.0) / 10.0, 0.0, 1.0)

        else:
            state = "[03] TATHĀTĀ: THE BOUNDARY COMPUTES TO ZERO"
            ui_col = C_GOLD
            ai_confidence = 1.0
            skel_alpha = np.clip((t_sec - 23.0) / 2.0, 0.0, 1.0)
            
            if f % 30 == 0:
                wave_radii.append(0.0)
            
            for r in wave_radii:
                hits = np.abs(bio_dist - r) < 20.0
                echo_alphas[hits] = 1.0

        yield (f, t_sec, state, ui_col, rot_p, rot_y, wave_radii, echo_alphas.copy(), ai_confidence, skel_alpha)

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 176: UWB DIELECTRIC PENETRATION [CORES: {cpu_cores}]")
    print(f"Tracking 2,500 Biological Nodes & UWB Propagation Fields.")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
