"""
LG-472: The Terminal Process (The Anatomy of the Present Moment)
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
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch

# Mathematical Constants
DURATION = 15.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "LG-472_Frames"
VIDEO_NAME = "LG-472_Cartoon.mp4"

# High-Coherence Serene Palette
C_BG      = '#FFFFFF'     # Pure White Background
C_TEXT    = '#111111'     # High Contrast Charcoal
C_DIM     = '#D0D0D0'     # Dim Reference Grid
C_ACTIVE  = '#0055AA'     # Serene Ocean Blue (The Rendered Output)

# ------------------------------------------------------------------
# O(1) TENSOR ALGEBRA: THE BASE GEOMETRY
# ------------------------------------------------------------------
def get_knot(u, rot_y):
    """Generates a perfect, looping 3D Trefoil knot representation."""
    x = 40 * (np.sin(u) + 2 * np.sin(2 * u))
    y = 40 * (np.cos(u) - 2 * np.cos(2 * u))
    z = 40 * (-np.sin(3 * u))
    
    # Rotate around Y axis
    cx, sx = np.cos(rot_y), np.sin(rot_y)
    x_rot = x * cx - z * sx
    z_rot = x * sx + z * cx
    
    # Static visual tilt for depth
    tilt = 0.4
    ct, st = np.cos(tilt), np.sin(tilt)
    y_tilt = y * ct - z_rot * st
    
    return x_rot, y_tilt

# ------------------------------------------------------------------
# THE 9-FRAME CARTOON LAYOUT (A4 / 9:16 GRID)
# ------------------------------------------------------------------
# Calculate exact center points for the 3x3 matrix
cols = [260, 540 + (540-260) - 260, 0] # Re-calculate cleanly
cols = [240, 540, 840] 

rows = [1480, 1040, 600] 
centers = [(c, r) for r in rows for c in cols]

titles = [
    "1. THE PHYSICAL EVENT",
    "2. SENSOR INGESTION",
    "3. NEURAL TRANSMISSION",
    "4. DARK PROCESSING",
    "5. HISTORICAL ALIGNMENT",
    "6. PHASE COMPOSITION",
    "7. THE FINAL RENDER",
    "8. THE HARDWARE DELAY",
    "9. CONSCIOUS AWARENESS"
]

subtitles = [
    "Kinematic reality unfolds in absolute time.",
    "Physical waves translate into sensory data.",
    "Logistical routing across the biological net.",
    "Scrubbing telemetry and zeroing noise.",
    "Data aligns with structural expectations.",
    "The geometry locks into structural integrity.",
    "The finished data package is completely sealed.",
    "The permanent physical lag between reality and mind.",
    "We endure the delayed output, never the live event."
]

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(args):
    f, total_frames, out_dir = args
    
    # p is the seamless mathematical progression [0.0 to 1.0]
    p = f / total_frames
    
    # The Temporal Vectors
    angle_real = p * 2 * np.pi
    angle_delay = (p - 0.15) * 2 * np.pi  # A hard ~2.2 second delay built into the math
    
    u = np.linspace(0, 2*np.pi, 250)
    rx, ry = get_knot(u, angle_real)
    dx, dy = get_knot(u, angle_delay)
    
    # ---------------------------------------------------------
    # MEMORY LEAK PREVENTION: RAW CANVAS INITIALISATION
    # ---------------------------------------------------------
    fig = Figure(figsize=(10.8, 19.2), dpi=100, facecolor=C_BG)
    canvas = FigureCanvasAgg(fig)
    
    ax = fig.add_axes([0, 0, 1, 1], facecolor=C_BG)
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)
    ax.set_axis_off()

    # Document Header
    ax.text(540, 1820, "THE PROCESS OF PRESENT PERCEPTION", color=C_TEXT, fontsize=28, fontname='monospace', weight='bold', ha='center')
    ax.text(540, 1780, "Mapping the exact physical latency of human cognitive awareness.", color=C_DIM, fontsize=14, fontname='monospace', ha='center', weight='bold')

    # Draw the Cartoon Grid Frames
    for i, (cx, cy) in enumerate(centers):
        # Master Cell Box
        rect = Rectangle((cx - 140, cy - 180), 280, 360, fill=False, edgecolor=C_TEXT, lw=2)
        ax.add_patch(rect)
        
        # Text alignment
        ax.text(cx, cy + 145, titles[i], color=C_TEXT, fontsize=11, fontname='monospace', weight='bold', ha='center')
        ax.text(cx, cy - 155, subtitles[i], color=C_TEXT, fontsize=8, fontname='monospace', ha='center', wrap=True)

    # ---------------------------------------------------------
    # PANEL EXACT MATHEMATICS
    # ---------------------------------------------------------
    
    # PANEL 1: Reality
    cx, cy = centers[0]
    ax.plot(rx + cx, ry + cy, color=C_TEXT, lw=2.5)
    
    # PANEL 2: Ingestion
    cx, cy = centers[1]
    ax.plot(rx + cx, ry + cy, color=C_DIM, lw=2.5)
    scan_y = 70 * np.sin(p * 2 * np.pi * 3)
    ax.plot([cx - 100, cx + 100], [cy + scan_y, cy + scan_y], color=C_ACTIVE, lw=3)
    
    # PANEL 3: Transmission
    cx, cy = centers[2]
    sx = ((np.arange(250) * 1.0 + p * 300) % 240) - 120
    sy = np.sin(np.arange(250) * 0.1 + p * 10) * 10
    ax.scatter(sx + cx, sy + cy, color=C_TEXT, s=8)
    
    # PANEL 4: Dark Processing (Coherent wave flattening out natively - NO STROBING)
    cx, cy = centers[3]
    fx = sx
    variance = np.clip(1.0 - (fx + 120) / 240, 0, 1)  # High on left, approaches 0 on right
    fy = np.sin(np.arange(250) * 0.8 + p * 20) * 40 * variance
    ax.scatter(fx + cx, fy + cy, color=C_TEXT, s=8)
    
    # PANEL 5: Assembly Sweep
    cx, cy = centers[4]
    draw_mask = (u < (p * 2 * np.pi * 3) % (2 * np.pi))
    ax.plot(dx[draw_mask] + cx, dy[draw_mask] + cy, color=C_ACTIVE, lw=3.0)
    ax.plot(dx[~draw_mask] + cx, dy[~draw_mask] + cy, color=C_DIM, lw=1.0)
    
    # PANEL 6: Phase Composition
    cx, cy = centers[5]
    scale = 1.0 + 0.05 * np.sin(p * 2 * np.pi * 12) # Gentle breathing
    ax.plot((dx * scale) + cx, (dy * scale) + cy, color=C_ACTIVE, lw=2.5)
    
    # PANEL 7: The Final Render
    cx, cy = centers[6]
    ax.plot(dx + cx, dy + cy, color=C_ACTIVE, lw=3.0)
    
    # PANEL 8: The Hardware Delay
    cx, cy = centers[7]
    ax.plot(rx + cx, ry + cy, color=C_DIM, lw=2.0)
    ax.plot(dx + cx, dy + cy, color=C_ACTIVE, lw=2.0)
    # The Physical Measurement Marker
    ax.plot([rx[0] + cx, dx[0] + cx], [ry[0] + cy, dy[0] + cy], color=C_TEXT, lw=2.0, linestyle='--')
    ax.scatter([rx[0] + cx, dx[0] + cx], [ry[0] + cy, dy[0] + cy], color=C_TEXT, s=30, zorder=6)
    
    # PANEL 9: Conscious Awareness (The Thought Bubble)
    cx, cy = centers[8]
    # Connective circles
    ax.add_patch(Circle((cx - 70, cy - 90), 8, fill=True, color=C_DIM, zorder=2))
    ax.add_patch(Circle((cx - 40, cy - 40), 12, fill=True, color=C_DIM, zorder=2))
    # Main Box
    bubble = FancyBboxPatch((cx - 120, cy - 20), 240, 130, boxstyle="round,pad=10,rounding_size=20",
                            ec=C_TEXT, fc=C_BG, lw=3, zorder=5)
    ax.add_patch(bubble)
    
    # Shape renders inside the mind
    cy_bubble = cy + 45
    ax.plot((dx * 0.7) + cx, (dy * 0.7) + cy_bubble, color=C_ACTIVE, lw=3.0, zorder=6)
    
    # Output awareness text
    ax.text(cx, cy + 15, "THIS IS NOW.", color=C_TEXT, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=6)

    # ---------------------------------------------------------
    # RENDER PIPELINE DISCHARGE
    # ---------------------------------------------------------
    out_path = os.path.join(out_dir, f"frame_{f:04d}.png")
    fig.savefig(out_path, facecolor=C_BG, edgecolor='none')
    
    fig.clf()
    del ax, canvas, fig
    gc.collect() 
    print(f"Rendered: {out_path}")

if __name__ == "__main__":
    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)
    
    cores = max(1, mp.cpu_count() - 1)
    print(f"Executing Sequential 9-Frame Raster on {cores} cores...")
    
    tasks = [(i, TOTAL_FRAMES, OUT_DIR) for i in range(TOTAL_FRAMES)]
    
    with mp.Pool(processes=cores) as pool:
        pool.map(render_frame, tasks)
        
    print("Matrix generation complete. Locking frames into FFmpeg container...")
    
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
        print(f"Assembly completed successfully. O(N) log sealed at: {VIDEO_NAME}")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg execution fault: {e}")
