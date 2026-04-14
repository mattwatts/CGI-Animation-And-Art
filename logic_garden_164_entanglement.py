"""
SOVEREIGN CODE: logic_garden_164_entanglement.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / 3D Tensor Synchronization (35 seconds)
SCENE: Logic Garden 164 (Quantum Entanglement / The Non-Local Tensor)
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
OUT_DIR = "frames_164_entanglement"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_CYAN    = '#00FFFF'          # Node A Initial State
C_GOLD    = '#FFD700'          # Node B Initial State
C_PURPLE  = '#8A2BE2'          # The Non-Local Tensor Matrix
C_RED     = '#FF0033'          # Entropy Injection (Kinetic Strikes)
C_MANTIS  = '#00FF00'          # Tathata (Spatial Collapse / Singularity)

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# 3D GYROSCOPIC HARDWARE GENERATION (COMPILE-TIME LATTICE)
# ------------------------------------------------------------------
np.random.seed(164)

def create_gyro_rings(num_points=1200):
    pts = []
    # Outer Ring (Pitch)
    t1 = np.linspace(0, 2*np.pi, num_points//3)
    pts.append(np.column_stack((np.cos(t1)*180, np.zeros_like(t1), np.sin(t1)*180)))
    # Middle Ring (Roll)
    t2 = np.linspace(0, 2*np.pi, num_points//3)
    pts.append(np.column_stack((np.zeros_like(t2), np.cos(t2)*140, np.sin(t2)*140)))
    # Inner Ring (Yaw)
    t3 = np.linspace(0, 2*np.pi, num_points//3)
    pts.append(np.column_stack((np.cos(t3)*100, np.sin(t3)*100, np.zeros_like(t3))))
    return np.vstack(pts)

BASE_GYRO = create_gyro_rings(1800)
TENSOR_POINTS = 150 # Points forming the connective thread

def rotate_3d(points, pitch, roll, yaw):
    cp, sp = math.cos(pitch), math.sin(pitch)
    cr, sr = math.cos(roll), math.sin(roll)
    cy, sy = math.cos(yaw), math.sin(yaw)

    Rx = np.array([[1, 0, 0], [0, cp, -sp], [0, sp, cp]])
    Ry = np.array([[cr, 0, sr], [0, 1, 0], [-sr, 0, cr]])
    Rz = np.array([[cy, -sy, 0], [sy, cy, 0], [0, 0, 1]])

    R = Rz @ Ry @ Rx
    return points @ R.T

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (ISOLATED MEMORY NODE)
# ------------------------------------------------------------------
def render_frame(data_packet):
    f, t_sec, state_str, ui_col, A_pts, B_pts, y_A, y_B, c_A, c_B, tensor_alpha, red_glow = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # 1. THE NON-LOCAL TENSOR (PURPLE O(1) THREAD)
    if y_A != y_B:
        tensor_y = np.linspace(y_B, y_A, TENSOR_POINTS)
        tensor_x = np.full(TENSOR_POINTS, 540)
        # Pulse formatting proves immediate linkage
        t_sizes = 4 + np.sin(np.arange(TENSOR_POINTS)*0.5 + f*0.4)**2 * 12
        ax.scatter(tensor_x, tensor_y, s=t_sizes, c=C_PURPLE, alpha=tensor_alpha, zorder=2)
        ax.plot([540, 540], [y_B, y_A], color=C_PURPLE, lw=1, alpha=tensor_alpha*0.5, zorder=1)

        # Phantom Central Telemetry (The Latency Proof)
        if t_sec > 10.0 and t_sec < 28.0:
            ax.text(540, 960, "Δt = 0.000 ms", ha='center', va='center', color=C_PURPLE, fontsize=32, fontname='monospace', weight='bold', alpha=0.8, zorder=10)
            ax.text(540, 930, "LATENCY NULLIFIED", ha='center', va='center', color=C_TEXT, fontsize=14, fontname='monospace', alpha=0.5, zorder=10)

    # 2. RENDER NODE A & B (GYROSCOPES)
    def draw_node(pts, y_pos, color, scale, glow=0):
        px = 540 + pts[:, 0] * scale
        py = y_pos + pts[:, 1] * scale * 0.3 + pts[:, 2] * scale * 0.8 # Isometric projection
        
        # Depth sorting
        z_order = np.argsort(pts[:, 1])
        px_s, py_s = px[z_order], py[z_order]
        alphas = np.clip((pts[z_order, 1] + 180) / 360.0 + 0.2, 0.1, 1.0)
        
        c_rgba = np.zeros((len(px_s), 4))
        c_rgba[:, 0:3] = hex_to_rgba(color)[0:3]
        c_rgba[:, 3] = alphas
        
        ax.scatter(px_s, py_s, c=c_rgba, s=8, zorder=5)
        # Node Core
        ax.scatter([540], [y_pos], s=150, c=C_TEXT, zorder=6)
        
        if glow > 0:
            ax.scatter([540], [y_pos], s=60000 * glow, c=color, alpha=0.1 * glow, zorder=4)
            # Entropy Sparks
            sx = 540 + np.random.uniform(-200, 200, 40)
            sy = y_pos + np.random.uniform(-200, 200, 40)
            ax.scatter(sx, sy, c=C_RED, s=np.random.uniform(5, 25, 40), alpha=glow, marker='x', zorder=7)

    # If Tathata merged, only draw A at massive scale
    if y_A == y_B:
         draw_node(A_pts, y_A, C_MANTIS, scale=1.8, glow=1.0)
    else:
         draw_node(A_pts, y_A, C_RED if red_glow > 0 else c_A, scale=1.0, glow=red_glow)
         draw_node(B_pts, y_B, c_B, scale=1.0, glow=red_glow*0.2) # B glows slightly in sympathy

    # 3. TELEMETRY WIDGETS
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.9))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2)
    ax.text(0.04, 0.965, "LOGIC GARDEN 164 :: THE NON-LOCAL TENSOR", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    # Physics Panel
    ent_state = "PERFECT COHERENCE" if t_sec < 10.0 else ("SYNCHRONIZING ENTROPY" if t_sec < 28 else "TOPOLOGICAL SINGULARITY")
    ax.text(0.04, 0.88, f"TENSOR STATE      : {ent_state}", transform=ax.transAxes, color=ui_col, fontsize=20, fontname='monospace')
    
    if y_A != y_B:
        ax.text(0.04, 0.84, f"LOCAL METRIC SPACE: EXPANSIVE", transform=ax.transAxes, color=C_CYAN, fontsize=18, fontname='monospace')
    else:
        ax.text(0.04, 0.84, f"LOCAL METRIC SPACE: COLLAPSED (D=0)", transform=ax.transAxes, color=C_MANTIS, fontsize=20, fontname='monospace', weight='bold')

    # Bottom Terminal
    ax.add_patch(plt.Rectangle((0, 0), 0.95, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 0.95], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2)
    
    pulse = ui_col if (f % 60 < 30) or ui_col == C_MANTIS else C_TEXT
    ax.text(0.04, 0.08, "GEOMETRIC DISTANCE:", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=28, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf(); plt.close(fig); plt.close('all'); gc.collect() 
    return f

# ------------------------------------------------------------------
# PHYSICS ENGINE (O(1) SYNCHRONIZATION MATRIX)
# ------------------------------------------------------------------
def generate_physics_stream():
    # Independent State Variables
    yA_base, yB_base = 1450.0, 470.0
    
    # Spin vectors (Pitch, Roll, Yaw)
    s_A = np.array([0.0, 0.0, 0.0])
    v_A = np.array([1.0, 1.5, 0.5]) * 0.02 # Base velocity
    
    # Tathata Collapse variables
    merged = False

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        red_glow = 0.0
        tensor_alpha = 0.3

        if t_sec < 10.0:
            state = "[01] 4D SEPARATION (ILLUSION ACTIVE)"
            ui_col = C_CYAN
            col_A, col_B = C_CYAN, C_GOLD
            
        elif t_sec < 28.0:
            state = "[02] KINETIC INJECTION (ZERO LATENCY)"
            ui_col = C_RED
            col_A, col_B = C_CYAN, C_GOLD
            tensor_alpha = 0.9 # Tensor burns bright
            
            # Massive unpredictable entropy strikes
            if f % 90 == 0:
                v_A += np.random.uniform(-0.15, 0.15, 3) 
            
            # Red flash on strikes
            if f % 90 < 15:
                red_glow = 1.0 - ((f % 90) / 15.0)

        else:
            state = "[03] TATHĀTĀ: DISTANCE WAS A PHANTOM"
            ui_col = C_MANTIS
            col_A, col_B = C_MANTIS, C_MANTIS
            tensor_alpha = 0.0
            
            dt = t_sec - 28.0
            # Exponential decay of distance
            dist = 490.0 * math.exp(-dt * 2.5)
            yA_base = 960 + dist
            yB_base = 960 - dist
            
            if dist < 2.0:
                yA_base = 960
                yB_base = 960
                merged = True

        # Apply Kinematics
        s_A += v_A
        
        # O(1) ARRAY SYNCHRONIZATION (The heart of Entanglement)
        # Node B's state is strictly the absolute inverse of Node A at Compile Time.
        s_B = -s_A 

        # Calculate 3D points
        pts_A = rotate_3d(BASE_GYRO, s_A[0], s_A[1], s_A[2])
        pts_B = rotate_3d(BASE_GYRO, s_B[0], s_B[1], s_B[2])

        yield (f, t_sec, state, ui_col, pts_A, pts_B, yA_base, yB_base, col_A, col_B, tensor_alpha, red_glow)

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 164: THE NON-LOCAL TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
