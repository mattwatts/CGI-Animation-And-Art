"""
LG-471c: Opposites (The moral and physical requirements of our existence)
Version: Serene Threshold Matrix 2.0 (Flicker-Free, Half-RPM)
Format: YouTube Shorts (1080x1920) | 60fps
Execution: Automated Multiprocessing & FFmpeg Assembly
"""

import numpy as np
import os
import multiprocessing
import subprocess
import gc
from pathlib import Path

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from mpl_toolkits.mplot3d.art3d import Line3DCollection

# Mathematical Constants
FRAMES = 3600  # 60 seconds at 60fps. Exactly halves the rotational RPM.
FPS = 60
NODES = 1000  
OUTPUT_DIR = "LG-471c_Frames"
VIDEO_NAME = "LG-471c.mp4"

def fibonacci_sphere(samples=NODES):
    """Generates an exact, even distribution of points on a sphere."""
    phi = np.pi * (3.0 - np.sqrt(5.0))
    indices = np.arange(samples)
    y = 1 - (indices / float(samples - 1)) * 2 
    radius = np.sqrt(1 - y * y)
    theta = phi * indices
    x = np.cos(theta) * radius
    z = np.sin(theta) * radius
    return np.column_stack((x, y, z))

def apply_rotation(points, angle):
    """Rotates the structure around the Y execution axis."""
    c, s = np.cos(angle), np.sin(angle)
    matrix = np.array([
        [c, 0, s],
        [0, 1, 0],
        [-s, 0, c]
    ])
    return np.dot(points, matrix)

def generate_frame(args):
    frame_idx, total_frames, out_dir = args
    
    # Progress ratio [0, 1] mapped to a full seamless rotation
    t = frame_idx / total_frames
    rotation_angle = t * 2 * np.pi
    
    # Base structure
    base_points = fibonacci_sphere(NODES)
    rotated = apply_rotation(base_points, rotation_angle)
    
    # Extract coordinates
    x, y, z = rotated[:, 0], rotated[:, 1], rotated[:, 2]
    
    # THE CONTINGENT MULTI-FACTOR TENSOR
    scale = 3.14
    factor_1 = np.sin(x * scale) 
    factor_2 = np.cos(y * scale * 1.5)
    factor_3 = np.sin(z * scale * 0.8)
    
    # Composite state equation
    composite_stress = (factor_1 + factor_2 + factor_3) / 3.0
    
    # Physical threshold
    THRESHOLD = 0.12 
    is_purge = composite_stress > THRESHOLD
    is_stable = ~is_purge
    
    # Execute Serene Phase Decomposition (Flicker-Free)
    volatility = (composite_stress[is_purge] - THRESHOLD) * 0.15
    
    # We replace independent frame white noise with a coherent time-wave constraint.
    # The 't * 2 * np.pi * 8' ensures the wave completes exactly 8 smooth cycles 
    # over the 60-second loop to maintain seamlessness, offset by coordinate positions 
    # to make the floating fluid and organic, rather than random.
    wave_x = np.sin(t * 2 * np.pi * 8 + y[is_purge] * 12)
    wave_y = np.cos(t * 2 * np.pi * 8 + z[is_purge] * 12)
    wave_z = np.sin(t * 2 * np.pi * 8 + x[is_purge] * 12)
    
    # Apply the smooth fluid displacement
    x[is_purge] += volatility * wave_x
    y[is_purge] += volatility * wave_y
    z[is_purge] += volatility * wave_z
    
    # ---------------------------------------------------------
    # MEMORY SAFE RENDER BLOCK
    # ---------------------------------------------------------
    fig = Figure(figsize=(10.8, 19.2), dpi=100, facecolor='white')
    canvas = FigureCanvasAgg(fig) 
    
    ax = fig.add_axes([0, 0, 1, 1], projection='3d', facecolor='white')
    ax.view_init(elev=15, azim=0)
    
    # Render Phase Dissolution (Soothing Purples/Lavenders)
    ax.scatter(x[is_purge], z[is_purge], y[is_purge], 
               c=composite_stress[is_purge], cmap='Purples', s=60, alpha=0.8, 
               edgecolors='lightgrey', linewidth=0.5)

    # Render Accumulation Structure (Calming Greens/Blues)
    ax.scatter(x[is_stable], z[is_stable], y[is_stable], 
               c=y[is_stable], cmap='GnBu', s=45, alpha=0.9, 
               edgecolors='white', linewidth=0.3)
    
    # Connective crystal geometry
    pts_stable = np.column_stack((x[is_stable], z[is_stable], y[is_stable]))
    lines = []
    
    limit = min(len(pts_stable), 300) 
    for i in range(limit):
        for j in range(i+1, limit):
            dist = np.linalg.norm(pts_stable[i] - pts_stable[j])
            if dist < 0.22:
                lines.append([pts_stable[i], pts_stable[j]])
                
    if lines:
        # Softened structural lines using Light Sky Blue
        lc = Line3DCollection(lines, colors='lightskyblue', linewidths=0.9, alpha=0.5)
        ax.add_collection3d(lc)

    # Lock containment scaling
    ax.set_xlim([-1.3, 1.3])
    ax.set_ylim([-1.3, 1.3])
    ax.set_zlim([-1.3, 1.3])
    ax.axis('off')
    
    # Save output and execute absolute memory purge
    filename = os.path.join(out_dir, f"frame_{frame_idx:04d}.png")
    fig.savefig(filename, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf()
    del ax, canvas, fig, pts_stable, lines
    gc.collect() 
    
    print(f"Rendered: {filename}")

if __name__ == '__main__':
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    cores = max(1, multiprocessing.cpu_count() - 1)
    print(f"Executing Serene Generation Matrix on {cores} cores...")
    
    tasks = [(i, FRAMES, OUTPUT_DIR) for i in range(FRAMES)]
    
    with multiprocessing.Pool(cores) as pool:
        pool.map(generate_frame, tasks)
        
    print("Frame generation completed. Engaging FFmpeg compiler...")
    
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-framerate", str(FPS),
        "-i", os.path.join(OUTPUT_DIR, "frame_%04d.png"),
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
