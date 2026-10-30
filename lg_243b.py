"""
LG-243b: The Serialisation of Time
Format: YouTube Shorts (1080x1920) | 60fps
Execution: Automated Multiprocessing & FFmpeg Assembly (Memory Safe)
"""

import numpy as np
import os
import multiprocessing as mp
import subprocess
import gc
from pathlib import Path

# Bypassing pyplot global state for OOM-Resistance
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Rectangle

# Mathematical Constants
DURATION = 20.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "LG-243b_Frames"
VIDEO_NAME = "LG-243b.mp4"

# High-Coherence Serene Palette
C_BG      = '#FFFFFF'     # Pure White Background
C_TEXT    = '#111111'     # High Contrast Charcoal Trace
C_DIM     = '#E0E0E0'     # Dim Reference Grid
C_ACTIVE  = '#0055AA'     # Serene Ocean Blue (Active Pointer)

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_dim     = np.array(hex_to_rgba(C_DIM)[:3])
c_active  = np.array(hex_to_rgba(C_ACTIVE)[:3])

# ------------------------------------------------------------------
# O(1) 3D TENSOR ALGEBRA
# ------------------------------------------------------------------
def rotate_3d(points, rx, ry, rz):
    cx, sx = np.cos(rx), np.sin(rx)
    cy, sy = np.cos(ry), np.sin(ry)
    cz, sz = np.cos(rz), np.sin(rz)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cx, 0], [0, 0, 1]])
    R = Rz.dot(Ry).dot(Rx)
    return points.dot(R.T)

# ------------------------------------------------------------------
# BASE GEOMETRY ARRAYS: STATIC PRE-ALLOCATION
# ------------------------------------------------------------------
np.random.seed(1983) 

# 1. The Reference Substrate (Grid Geometry)
GV = np.linspace(-150, 150, 80)
Xg, Yg = np.meshgrid(GV, GV)
gx = Xg.flatten()
gy = Yg.flatten()
gz = np.zeros(len(gx)) - 10.0 # Grid lies flat at Z=-10

# 2. The Carbon Trace (Pre-calculated smooth geometric trajectory)
T_INTERRUPT = 17.5 # Point at which the trace completes, leaving 2.5s of rest
N_TRACE = 15000
time_nodes = np.linspace(0, T_INTERRUPT, N_TRACE)

# Serene geometric wave (Low frequency, smooth execution)
trace_x = np.sin(time_nodes * 10.0) * 6.0 + np.sin(time_nodes * 3.0) * 3.0
trace_y = np.linspace(160, -160, N_TRACE)
trace_z = np.zeros(N_TRACE) - 9.8 

# Initialize physical arrays. Carbon hides outside frame until drawn.
cx_arr = np.zeros(N_TRACE) + 9999.0
cy_arr = np.zeros(N_TRACE) + 9999.0
cz_arr = np.zeros(N_TRACE) + 9999.0

# Array Merge and Index Bounds
base_px = np.concatenate([gx, cx_arr])
base_py = np.concatenate([gy, cy_arr])
base_pz = np.concatenate([gz, cz_arr])

MAX_PARTICLES = len(base_px)
idx_grid_end = len(gx) 

mask_grid = np.arange(MAX_PARTICLES) < idx_grid_end
mask_trace = ~mask_grid

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (OOM-SAFE)
# ------------------------------------------------------------------
def render_frame(args):
    f, total_frames, out_dir = args
    t_sec = f / FPS
    
    colors = np.zeros((MAX_PARTICLES, 3))
    sizes = np.zeros(MAX_PARTICLES)
    
    curr_x = np.copy(base_px)
    curr_y = np.copy(base_py)
    curr_z = np.copy(base_pz)

    # Substrate Default
    colors[mask_grid] = c_dim
    sizes[mask_grid] = 1.0

    # Execute Kinetic Trace
    if t_sec < T_INTERRUPT:
        active_idx = int((t_sec / T_INTERRUPT) * N_TRACE)
        active_idx = np.clip(active_idx, 0, N_TRACE - 1)
        
        curr_x[idx_grid_end : idx_grid_end + active_idx] = trace_x[:active_idx]
        curr_y[idx_grid_end : idx_grid_end + active_idx] = trace_y[:active_idx]
        curr_z[idx_grid_end : idx_grid_end + active_idx] = trace_z[:active_idx]
        
        colors[mask_trace] = c_text
        sizes[mask_trace] = 2.0
        
        # Substrate Indentation Logic
        active_y = trace_y[active_idx]
        dent_mask = (gx**2 + (gy - active_y)**2) < 400.0
        curr_z[np.where(mask_grid)[0][dent_mask]] -= 3.0
        
        # The Active Pointer
        ptr_loc = idx_grid_end + active_idx - 1
        if ptr_loc >= idx_grid_end:
            sizes[ptr_loc] = 12.0
            colors[ptr_loc] = c_active 
            
        state_str = "ACTIVE TRACE"
        completion = t_sec / T_INTERRUPT
    else:
        # Trace Complete. Geometric hold.
        curr_x[mask_trace] = trace_x
        curr_y[mask_trace] = trace_y
        curr_z[mask_trace] = trace_z
        
        colors[mask_trace] = c_text
        sizes[mask_trace] = 2.0 
        
        state_str = "TRACE COMPLETE"
        completion = 1.0

    # Apply Global Tensor Matrix
    pts = np.column_stack([curr_x, curr_y, curr_z])
    rot_pts = rotate_3d(pts, np.pi/6, 0.0, 0.0)
    
    proj_x = rot_pts[:, 0]
    proj_y = rot_pts[:, 1]
    z_depth = rot_pts[:, 2] 

    # O(N) Geometry Culling
    cull_mask = (proj_y > -260) & (proj_y < 260) & (proj_x > -160) & (proj_x < 160)
    
    s_px = proj_x[cull_mask]
    s_py = proj_y[cull_mask]
    s_z = z_depth[cull_mask]
    s_c = colors[cull_mask]
    s_s = sizes[cull_mask]

    # Depth Sorting
    sort_idx = np.argsort(s_z)
    s_px = s_px[sort_idx]
    s_py = s_py[sort_idx]
    s_c = s_c[sort_idx]
    s_s = s_s[sort_idx]

    # Render Block
    fig = Figure(figsize=(10.8, 19.2), dpi=100, facecolor=C_BG)
    canvas = FigureCanvasAgg(fig)
    
    ax = fig.add_axes([0, 0, 1, 1], facecolor=C_BG)
    ax.set_xlim(-160, 160)
    ax.set_ylim(-260, 260)
    ax.set_axis_off()

    # Draw nodes
    ax.scatter(s_px, s_py, s=s_s, color=s_c, edgecolors='none', alpha=0.9, zorder=10)

    # Clean Physical Telemetry Widgets
    ax.text(-140, 240, "LG-243b :: SERIALISATION OF TIME", color=C_TEXT, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: KINETIC TRACE", color=C_TEXT, fontsize=8, fontname='monospace', zorder=80)
    
    ax.text(-140, -180, f"KINEMATIC LOGIC: {state_str}", color=C_ACTIVE if completion < 1.0 else C_TEXT, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    ax.text(-140, -205, f"TIME RECORDED [ {t_sec:.2f}s ]", color=C_TEXT, fontsize=10, fontname='monospace', zorder=80)
    
    # Progress Bar (Replaced plt.Rectangle with direct object instance)
    ax.add_patch(Rectangle((-140, -210), 280, 4, facecolor=C_DIM, zorder=80))
    bar_w = 280 * np.clip(completion, 0, 1)
    ax.add_patch(Rectangle((-140, -210), bar_w, 4, facecolor=C_ACTIVE, zorder=81))

    # Phase Text Box
    ax.add_patch(Rectangle((-140, 215), 280, 2, facecolor=C_ACTIVE, zorder=80))
    ax.text(140, 205, f"[{state_str}]", color=C_ACTIVE if completion < 1.0 else C_TEXT, fontsize=14, fontname='monospace', weight='bold', ha='right', zorder=80)

    out_path = os.path.join(out_dir, f"frame_{f:04d}.png")
    fig.savefig(out_path, facecolor=C_BG, edgecolor='none')
    
    fig.clf()
    del ax, canvas, fig
    gc.collect() 
    print(f"Rendered: {out_path}")

if __name__ == "__main__":
    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)
    
    cores = max(1, mp.cpu_count() - 1)
    print(f"Executing Clean Generation Matrix on {cores} cores...")
    
    tasks = [(i, TOTAL_FRAMES, OUT_DIR) for i in range(TOTAL_FRAMES)]
    
    with mp.Pool(processes=cores) as pool:
        pool.map(render_frame, tasks)
        
    print("Frame generation completed. Engaging FFmpeg compiler...")
    
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-framerate", str(FPS),
        "-i", os.path.join(OUT_DIR, "frame_%04d.png"),
        "-vf", "scale=1080:1920",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "15",
        VIDEO_NAME
    ]
    
    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"Assembly completed successfully. Output fixed at: {VIDEO_NAME}")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg execution fault: {e}")
