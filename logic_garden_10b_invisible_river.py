"""
PROJECT: Logic Garden 10b (The Invisible River // Kinematic Streamlines)
FORMAT: YouTube Shorts (1080x1920)
METADATA: FLUID DYNAMICS, KINEMATICS, VECTOR FIELDS, RK4 INTEGRATION
EXECUTION: 24.0s Sequence. True Mathematical Construction.
RULES ENFORCED:
- Daylight Palette (White Substrate / High Contrast).
- Phase-Locked Metaphor: Fluid flow visualised via trailing vectors.
- Exact realisational aspect of a Runge-Kutta continuous integration field.
- Velocity-based Bauhaus colour mapping.
- Australian spelling conventions enforced natively.
- HOTFIX: O(1) Memory-mapped .npy datastores for strict OS-level multiprocessing stability.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
from matplotlib.collections import LineCollection
import multiprocessing as mp
import os
import gc

# ======== SEQUENCE PARAMETERS ========
FPS = 60
DURATION = 24.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_10b_invisible_river"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL BAUHAUS PALETTE --------
C_BG            = '#FFFFFF'
C_TEXT          = '#111115'
C_EDGE          = '#111115'
C_MARINE        = '#005599'  # Slow Velocity / High Pressure Eddy
C_AMBER         = '#FFB300'  # Nominal Velocity Stream
C_RED           = '#FF3300'  # High Velocity Shear
C_GUI           = '#64748B'

# Architecture Viewport (1080x1920 scaled)
X_MIN, X_MAX = -5.4, 5.4
Y_MIN, Y_MAX = -9.6, 9.6
WIDTH = X_MAX - X_MIN
HEIGHT = Y_MAX - Y_MIN

N_PARTICLES = 10000
TAIL_LEN = 25  # Number of historical vertices forming the streamline
DATA_SHARD = "tensor_10b_fluid_history.npy"

# ------------------------------------------------------------------
# O(1) RK4 CONTINUOUS INTEGRATION ENGINE
# ------------------------------------------------------------------
def vector_field(pos, t):
    # Physical Flow Formula mapping structural chaos and temporal drift
    x, y = pos[:, 0], pos[:, 1]
    k = 0.8
    # Baseline Taylor-Green inspired vortex field with oscillating shear
    u = np.sin(k * y) + 0.5 * np.cos(k * x) * np.sin(t * 0.8)
    v = np.cos(k * x) - 0.5 * np.sin(k * y) * np.cos(t * 0.8)
    
    # Introduce sweeping macroscopic shear over the Y-axis to push the "River"
    v += 0.8 * np.sin(t * 0.3)
    return np.column_stack((u, v))

def pre_compute_fluid_tensor():
    print("PHASE 1: PRE-COMPUTING RUNGE-KUTTA KINEMATICS...")
    np.random.seed(10)
    
    P_HIST = np.zeros((TOTAL_FRAMES, N_PARTICLES, 2), dtype=np.float32)
    
    # Uniform uniform distribution across the topological plane
    P_HIST[0, :, 0] = np.random.uniform(X_MIN, X_MAX, N_PARTICLES)
    P_HIST[0, :, 1] = np.random.uniform(Y_MIN, Y_MAX, N_PARTICLES)
    
    curr_pos = P_HIST[0].copy()
    dt = 1.0 / FPS
    step_mult = 1.5  # Fluid aggression multiplier
    
    for f in range(1, TOTAL_FRAMES):
        t = f * dt
        
        # RK4 Integration steps
        k1 = vector_field(curr_pos, t)
        k2 = vector_field(curr_pos + 0.5 * dt * step_mult * k1, t + 0.5 * dt)
        k3 = vector_field(curr_pos + 0.5 * dt * step_mult * k2, t + 0.5 * dt)
        k4 = vector_field(curr_pos + dt * step_mult * k3, t + dt)
        
        curr_pos += (dt * step_mult / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
        
        # Toroidal Mathematical Wrapping (The Infinite Flow Matrix)
        curr_pos[:, 0] = ((curr_pos[:, 0] - X_MIN) % WIDTH) + X_MIN
        curr_pos[:, 1] = ((curr_pos[:, 1] - Y_MIN) % HEIGHT) + Y_MIN
        
        P_HIST[f] = curr_pos

    np.save(DATA_SHARD, P_HIST)
    print(f"KINEMATIC TENSOR PRE-COMPILED AND SECURED OVER {TOTAL_FRAMES} FRAMES.")

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (O(1) DISK READ)
# ------------------------------------------------------------------
def render_frame(f_idx):
    # Load memory-mapped tensor for absolute OS-level stability
    P_STATE = np.load(DATA_SHARD, mmap_mode='r')
    
    t_sec = f_idx / float(FPS)
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.]); ax.set_axis_off(); fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    
    # Physical scale maps perfectly to the 1080x1920 viewport
    ax.set_xlim(X_MIN, X_MAX)
    ax.set_ylim(Y_MIN, Y_MAX)

    # 1. EVALUATE HISTORICAL TAILING (STREAMLINES)
    start_idx = max(0, f_idx - TAIL_LEN)
    # Shape: (Frames, Particles, 2)
    raw_tail = P_STATE[start_idx : f_idx + 1] 
    
    # Invert Matrix to (Particles, Frames, 2) for Matplotlib segment formatting
    line_tensor = np.transpose(raw_tail, (1, 0, 2))
    
    if line_tensor.shape[1] > 1:
        # Detect mathematical toroidal wraps across the boundary.
        # If the Euclidean distance between historical frame jumps > WIDTH*0.5, we inject a NaN to break the physical line.
        dx = np.diff(line_tensor[:, :, 0], axis=1)
        dy = np.diff(line_tensor[:, :, 1], axis=1)
        dist_sq = dx**2 + dy**2
        wrap_mask = dist_sq > (WIDTH * 0.4)**2
        
        cleaned_tensor = line_tensor.copy()
        # Matplotlib uses NaN vectors to gracefully segment disconnected geometry 
        for p_idx, t_idx in zip(*np.where(wrap_mask)):
            cleaned_tensor[p_idx, t_idx + 1] = np.nan

        # 2. EXACT VELOCITY CHROMATIC MAPPING (Physical Telemetry)
        if f_idx > 0:
            inst_vel = P_STATE[f_idx] - P_STATE[f_idx - 1]
        else:
            inst_vel = P_STATE[1] - P_STATE[0]
            
        vel_mag = np.linalg.norm(inst_vel, axis=1)
        # Normalize baseline to a realistic fluid bracket
        v_norm = np.clip(vel_mag / 0.05, 0.0, 1.0) 

        c_mar_rgb = np.array(mcolors.to_rgb(C_MARINE))
        c_amb_rgb = np.array(mcolors.to_rgb(C_AMBER))
        c_red_rgb = np.array(mcolors.to_rgb(C_RED))
        
        color_matrix = np.zeros((N_PARTICLES, 4))
        # Gradient Application
        for i in range(N_PARTICLES):
            v_val = v_norm[i]
            if v_val < 0.5:
                # Slow -> Mid
                mix = v_val / 0.5
                color_matrix[i, :3] = c_mar_rgb * (1.0 - mix) + c_amb_rgb * mix
            else:
                # Mid -> High
                mix = (v_val - 0.5) / 0.5
                color_matrix[i, :3] = c_amb_rgb * (1.0 - mix) + c_red_rgb * mix
                
            # Kinetic objects are more opaque
            color_matrix[i, 3] = 0.2 + (0.5 * v_val)
            
        # Thicker vector lines for visual "Ink/Dye" simulation
        line_widths = 1.0 + (3.0 * v_norm)

        lc_engine = LineCollection(cleaned_tensor, colors=color_matrix, linewidths=line_widths, capstyle='round')
        ax.add_collection(lc_engine)
        
        # Leading Edge "Comet Head" 
        head_alpha = np.clip(0.5 + (0.5 * v_norm), 0.0, 1.0)
        color_matrix[:, 3] = head_alpha
        ax.scatter(cleaned_tensor[:, -1, 0], cleaned_tensor[:, -1, 1], s=4.0 + (10.0*v_norm), color=color_matrix, edgecolors='none', zorder=5)

    # 3. HIGH-DENSITY HUD & TELEMETRY
    ax.add_patch(Rectangle((X_MIN, Y_MAX - 1.05), WIDTH, 1.05, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([X_MIN, X_MAX], [Y_MAX - 1.05, Y_MAX - 1.05], color=C_TEXT, lw=3, zorder=81)
    
    text_x_base = X_MIN + 0.2
    
    ax.text(text_x_base, Y_MAX - 0.35, "LG-10b :: THE INVISIBLE RIVER", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(text_x_base, Y_MAX - 0.60, "[SFI-1.00] BOUNDED THERMODYNAMIC FLOW KINEMATICS", color=C_GUI, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((X_MIN, Y_MIN), WIDTH, 1.2, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([X_MIN, X_MAX], [Y_MIN + 1.2, Y_MIN + 1.2], color=C_TEXT, lw=3, zorder=81)

    # Evaluate macroscopic energy for HUD readouts
    v_mean = np.mean(v_norm) if f_idx > 0 else 0.0
    v_peak = np.max(v_norm) if f_idx > 0 else 0.0
    
    ax.text(text_x_base, Y_MIN + 0.90, f"PROTOCOL PHASE: RK4 KINEMATIC INTEGRATION VECTORS", color=C_MARINE, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(text_x_base, Y_MIN + 0.65, f"MEAN VECTOR MAGNITUDE: {v_mean:.4f} UNIT/FRAME", color=C_AMBER, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(text_x_base, Y_MIN + 0.40, f"PEAK SHEAR VELOCITY  : {v_peak:.4f} UNIT/FRAME", color=C_RED, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(text_x_base, Y_MIN + 0.15, "BAUHAUS KINEMATIC TRACER MATRIX ACTIVE.", color=C_TEXT, fontsize=12, fontname='monospace', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f_idx:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f_idx

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    # Execute generation phase safely on the Master Thread
    pre_compute_fluid_tensor()
    
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-10b: RUNGE-KUTTA FLUID MATRIX ENGAGED [CORES: {cpu_cores}]")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")
                
    # Clean up the memory-mapped datastore off the system
    if os.path.exists(DATA_SHARD):
        os.remove(DATA_SHARD)
        
    print("Compilation Complete. True Fluid Maths generated.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
