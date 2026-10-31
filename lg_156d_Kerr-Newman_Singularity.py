"""
LG-156d: Kerr-Newman Ring Singularity
Format: YouTube Shorts (1080x1920) | 60fps
Execution: Automated Multiprocessing & FFmpeg Assembly (Memory Safe)
"""

import numpy as np
import os
import multiprocessing as mp
import subprocess
import gc
from pathlib import Path

# Absolute OOM-Resistance bypass of pyplot
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Rectangle

# Mathematical Constants
DURATION = 120.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "LG-156d_Frames"
VIDEO_NAME = "LG-156d.mp4"

# High-Coherence Serene Palette
C_BG      = '#FFFFFF'     # Pure White Background
C_TEXT    = '#111111'     # High Contrast Charcoal
C_DIM     = '#D0D0D0'     # Dim Reference Grid
C_ACTIVE  = '#0055AA'     # Serene Ocean Blue (Active Horizon)

# ------------------------------------------------------------------
# O(1) TENSOR ALGEBRA: THE PHYSICS WAREHOUSE
# ------------------------------------------------------------------
def rotate_3d(x, y, z, rx, ry, rz):
    # Vectorized continuous 3D rotation tensor
    cx, sx = np.cos(rx), np.sin(rx)
    cy, sy = np.cos(ry), np.sin(ry)
    cz, sz = np.cos(rz), np.sin(rz)
    
    # Rx
    y1 = y*cx - z*sx
    z1 = y*sx + z*cx
    # Ry
    x2 = x*cy + z1*sy
    z2 = -x*sy + z1*cy
    # Rz
    x3 = x2*cz - y1*sz
    y3 = x2*sz + y1*cz
    
    return x3, y3, z2

def smoothstep(edge0, edge1, x):
    # Hermite interpolation for majestic, serene transitions (zero jerking)
    t = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)

# Base Geometrical Substrate (Polar Mesh)
angles = np.linspace(0, 2 * np.pi, 91)
radii = np.linspace(40, 900, 50)
Theta_init, R_init = np.meshgrid(angles, radii, indexing='ij')

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(args):
    f, total_frames, out_dir = args
    t_sec = f / FPS
    
    Theta = np.copy(Theta_init)
    R = np.copy(R_init)

    # 1. KINEMATIC INTEGRATION
    # Continuous rotation mapping
    rot = t_sec * 0.5 + 12.0 * smoothstep(20, 60, t_sec) + 6.0 * smoothstep(60, 100, t_sec)
    # Lense-Thirring effect (Frame dragging twist)
    twist_mag = smoothstep(10, 50, t_sec) * 12.0 - smoothstep(70, 110, t_sec) * 12.0
    theta_offset = twist_mag * 400.0 / (R + 100.0)
    
    Theta += (rot + theta_offset)

    # Radial collapse (Formation of the 1D ring)
    r_collapse = smoothstep(80, 115, t_sec)
    R_final = R * (1.0 - r_collapse) + 250.0 * r_collapse

    # Z-Axis Gravity Funnel
    z_depth = smoothstep(20, 60, t_sec) * 900.0 * (1.0 - smoothstep(80, 110, t_sec))
    Z = -z_depth * np.exp(-(R_init**2) / (2 * 300.0**2)) 

    # Polar to Cartesian mapping
    X = R_final * np.cos(Theta)
    Y = R_final * np.sin(Theta)

    # Apply global isometric tilt matrix (Pitch downward to reveal Z depth)
    x3, y3, z3 = rotate_3d(X, Y, Z, rx=-1.0, ry=0.0, rz=0.0)
    
    x_proj = 540 + x3
    y_proj = 960 + y3

    # Physics Readouts
    spin_a = smoothstep(0, 60, t_sec) * 0.999
    frame_vel = 0.5 + smoothstep(10, 50, t_sec) * 2.5 - smoothstep(80, 115, t_sec) * 3.0
    g_shear = (z_depth / 900.0)
    
    if t_sec < 30:
        state_str = "FRAME DRAGGING INGRESS"
    elif t_sec < 60:
        state_str = "EVENT HORIZON GRAVITY SHEAR"
    elif t_sec < 90:
        state_str = "CAUCHY HORIZON CRITICAL DAMPING"
    else:
        state_str = "1D RING SINGULARITY RESOLUTION"

    # ---------------------------------------------------------
    # MEMORY SAFE RENDER PIPELINE
    # ---------------------------------------------------------
    fig = Figure(figsize=(10.8, 19.2), dpi=100, facecolor=C_BG)
    canvas = FigureCanvasAgg(fig)
    
    ax = fig.add_axes([0, 0, 1, 1], facecolor=C_BG)
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)
    ax.set_axis_off()

    # Draw the Wireframe Vectors
    # Radial Spokes
    for j in range(len(angles)):
        ax.plot(x_proj[j, :], y_proj[j, :], color=C_TEXT, lw=0.6, alpha=0.15)
        
    # Concentric Rings
    for i in range(len(radii)):
        c = C_ACTIVE if radii[i] < 350 else C_TEXT
        lw = 1.8 if radii[i] < 350 else 0.8
        alpha = 0.8 if radii[i] < 350 else 0.3
        ax.plot(x_proj[:, i], y_proj[:, i], color=c, lw=lw, alpha=alpha)

    # Draw Physical Constrain Overlays
    if t_sec > 110:
        fade_in = smoothstep(110, 115, t_sec)
        ax.text(60, 1420, "1D RING LOCUS ACHIEVED", color=C_ACTIVE, fontsize=16, fontname='monospace', weight='bold', alpha=fade_in)
        ax.text(60, 1380, "x² + y² = a² | z = 0", color=C_TEXT, fontsize=16, fontname='monospace', alpha=fade_in)

    # ---------------------------------------------------------
    # UI WIDGET COMPONENTS
    # ---------------------------------------------------------
    ax.text(60, 1820, "LG-156d :: KERR-NEWMAN SINGULARITY", color=C_TEXT, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(60, 1790, "SYSTEM: VECTOR WIREFRAME KINEMATICS", color=C_DIM, fontsize=12, fontname='monospace', weight='bold', zorder=80)

    # Data Telemetry Box
    ax.text(60, 1600, f"SPIN PARAMETER (a)   : {spin_a:.4f} c/G", color=C_TEXT, fontsize=14, fontname='monospace')
    ax.text(60, 1560, f"FRAME DRAG VELOCITY  : {frame_vel:.4f} ω", color=C_TEXT, fontsize=14, fontname='monospace')
    ax.text(60, 1520, f"GRAVITATIONAL SHEAR  : {g_shear:.4f} Δg", color=C_TEXT, fontsize=14, fontname='monospace')

    # Progress Tracking Baseplate
    ax.add_patch(Rectangle((60, 100), 960, 4, facecolor=C_DIM, zorder=80))
    bar_w = 960 * np.clip(t_sec / DURATION, 0, 1)
    ax.add_patch(Rectangle((60, 100), bar_w, 4, facecolor=C_ACTIVE, zorder=81))

    ax.text(60, 120, f"KINEMATIC LOGIC: {state_str}", color=C_TEXT, fontsize=12, fontname='monospace', weight='bold', zorder=80)
    ax.text(1020, 120, f"TIME RECORDED [ {t_sec:.2f}s ]", color=C_TEXT, fontsize=12, fontname='monospace', ha='right', zorder=80)

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
        
    print("Vector frames constructed. Engaging FFmpeg compiler...")
    
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
        print(f"Assembly completed successfully. Output sealed at: {VIDEO_NAME}")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg execution fault: {e}")
