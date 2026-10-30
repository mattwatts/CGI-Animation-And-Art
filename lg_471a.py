"""
LG-471: Opposites (The moral and physical requirements of our existence)
Format: YouTube Shorts (1080x1920) | 60fps
Execution: Automated Multiprocessing & FFmpeg Assembly
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import os
import multiprocessing
import subprocess
from pathlib import Path

# Mathematical Constants
FRAMES = 720  # 12 seconds at 60fps
FPS = 60
NODES = 800
OUTPUT_DIR = "LG-471_Frames"
VIDEO_NAME = "LG-471.mp4"

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
    
    # Progress ratio [0, 1]
    t = frame_idx / total_frames
    rotation_angle = t * 2 * np.pi
    
    # Base structure
    base_points = fibonacci_sphere(NODES)
    rotated = apply_rotation(base_points, rotation_angle)
    
    # Extract coordinates
    x, y, z = rotated[:, 0], rotated[:, 1], rotated[:, 2]
    
    # Substrate classification
    is_upper = y > 0
    is_lower = ~is_upper
    
    # The Fire: Induce thermal spallation (jitter) based on depth
    thermal_variance = np.abs(y[is_lower]) * 0.15
    y[is_lower] += np.random.normal(0, thermal_variance)
    x[is_lower] += np.random.normal(0, thermal_variance)
    z[is_lower] += np.random.normal(0, thermal_variance)
    
    # Setup Figure for 9:16 Shorts (1080x1920)
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100, facecolor='white')
    
    # Force axes to fill the entire 1080x1920 geometry without arbitrary padding
    ax = fig.add_axes([0, 0, 1, 1], projection='3d', facecolor='white')
    ax.view_init(elev=15, azim=0)
    
    # Plotting The Lower Purge (The Devils / Fire phase)
    ax.scatter(x[is_lower], z[is_lower], y[is_lower], 
               c=np.abs(y[is_lower]), cmap='hot', s=60, alpha=0.9, 
               edgecolors='black', linewidth=0.5)

    # Plotting The Upper Accumulation (The Angels / Prosperity phase)
    ax.scatter(x[is_upper], z[is_upper], y[is_upper], 
               c=y[is_upper], cmap='ocean', s=40, alpha=0.9, 
               edgecolors='white', linewidth=0.3)
    
    # Draw strict crystalline geometry only for the upper stable phase
    pts_upper = np.column_stack((x[is_upper], z[is_upper], y[is_upper]))
    lines = []
    
    limit = min(len(pts_upper), 250) 
    for i in range(limit):
        for j in range(i+1, limit):
            dist = np.linalg.norm(pts_upper[i] - pts_upper[j])
            if dist < 0.25:
                lines.append([pts_upper[i], pts_upper[j]])
                
    if lines:
        from mpl_toolkits.mplot3d.art3d import Line3DCollection
        lc = Line3DCollection(lines, colors='teal', linewidths=0.8, alpha=0.6)
        ax.add_collection3d(lc)

    # Enforce physical scaling limits
    ax.set_xlim([-1.2, 1.2])
    ax.set_ylim([-1.2, 1.2])
    ax.set_zlim([-1.2, 1.2])
    ax.axis('off')
    
    # Output file - pad_inches and bbox_inches removed to lock physical dimensions
    filename = os.path.join(out_dir, f"frame_{frame_idx:04d}.png")
    plt.savefig(filename, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)
    print(f"Rendered: {filename}")

if __name__ == '__main__':
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    cores = max(1, multiprocessing.cpu_count() - 1)
    print(f"Executing Generation Matrix on {cores} cores...")
    
    tasks = [(i, FRAMES, OUTPUT_DIR) for i in range(FRAMES)]
    
    with multiprocessing.Pool(cores) as pool:
        pool.map(generate_frame, tasks)
        
    print("Frame generation completed. Engaging FFmpeg compiler...")
    
    # Automated FFmpeg assembly with explicit scaling lock
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
