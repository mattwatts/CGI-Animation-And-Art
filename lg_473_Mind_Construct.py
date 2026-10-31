"""
LG-473: The Mind Construct (Lifecycle of a Cognitive Bubble)
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
DURATION = 20.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "LG-473_Frames"
VIDEO_NAME = "LG-473_Mind_Construct.mp4"

# High-Coherence Serene Palette
C_BG      = '#FFFFFF'     # Pure White Background
C_TEXT    = '#111111'     # High Contrast Charcoal
C_DIM     = '#C0C0C0'     # Deflated / Inert State
C_ACTIVE  = '#0055AA'     # Serene Ocean Blue (Kinetic Impulses)

# ------------------------------------------------------------------
# O(1) TENSOR ALGEBRA: THE PHYSICS WAREHOUSE
# ------------------------------------------------------------------
def rotate_3d(x, y, z, rx, ry, rz):
    # Vectorized continuous 3D rotation tensor
    cx, sx = np.cos(rx), np.sin(rx)
    cy, sy = np.cos(ry), np.sin(ry)
    cz, sz = np.cos(rz), np.sin(rz)
    
    y1 = y*cx - z*sx
    z1 = y*sx + z*cx
    
    x2 = x*cy + z1*sy
    z2 = -x*sy + z1*cy
    
    x3 = x2*cz - y1*sz
    y3 = x2*sz + y1*cz
    
    return x3, y3, z2

def smoothstep(edge0, edge1, x):
    t = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)

# ------------------------------------------------------------------
# BASE GEOMETRY PRE-CALCULATION
# ------------------------------------------------------------------
# 1. The Neural Boundary (Fibonacci Sphere)
N_NODES = 250
indices = np.arange(0, N_NODES, dtype=float) + 0.5
phi = np.arccos(1 - 2*indices/N_NODES)
theta = np.pi * (1 + 5**0.5) * indices

bx = np.cos(theta) * np.sin(phi)
by = np.sin(theta) * np.sin(phi)
bz = np.cos(phi)

# Pre-calculate surface connections (The Fabric of the balloon)
connections = []
for i in range(N_NODES):
    for j in range(i + 1, N_NODES):
        dist = (bx[i]-bx[j])**2 + (by[i]-by[j])**2 + (bz[i]-bz[j])**2
        if dist < 0.18:  # Nearest neighbors threshold
            connections.append((i, j))
connections = np.array(connections)

# 2. Inside Gas Molecules (The Impulses)
N_IMPULSES = 120
np.random.seed(473)
freq_x = np.random.uniform(0.5, 1.8, N_IMPULSES)
freq_y = np.random.uniform(0.5, 1.8, N_IMPULSES)
freq_z = np.random.uniform(0.5, 1.8, N_IMPULSES)
phase_x = np.random.uniform(0, 2*np.pi, N_IMPULSES)
phase_y = np.random.uniform(0, 2*np.pi, N_IMPULSES)
phase_z = np.random.uniform(0, 2*np.pi, N_IMPULSES)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(args):
    f, total_frames, out_dir = args
    t_sec = f / FPS
    
    # KINEMATIC TIMELINE (The Lifecycle)
    # Phase 1: Inert (0-3s)
    # Phase 2: Inflation (3-8s)
    # Phase 3: Hold / Existence (8-14s)
    # Phase 4: Deflation (14-19s)
    
    inflation = smoothstep(2.0, 7.0, t_sec) - smoothstep(14.0, 18.0, t_sec)
    
    radius = 180.0 + (320.0 * inflation)
    kinetic_velocity = 1.0 + (1.5 * inflation)
    
    if inflation < 0.05:
        state_str = "[00] INERT : DEFLATED BASELINE"
        c_fabric = C_DIM
    elif inflation < 0.95 and t_sec < 10.0:
        state_str = "[01] KINETIC INFLATION : PRESSURE RISING"
        c_fabric = C_TEXT
    elif t_sec >= 14.0 and inflation < 0.95:
        state_str = "[03] VENTING : STRUCTURAL COLLAPSE"
        c_fabric = C_TEXT
    else:
        state_str = "[02] EQUILIBRIUM : THE MIND CONSTRUCT EXISTS"
        c_fabric = C_ACTIVE

    # Apply global majestic rotation
    rot_t = t_sec * 0.15
    g_x, g_y, g_z = rotate_3d(bx, by, bz, rot_t, rot_t * 0.7, 0)
    
    proj_bx = 540 + (g_x * radius)
    proj_by = 960 + (g_y * radius)
    proj_bz = g_z * radius

    # Generate Impulse Positions (Bounded Harmonic Chaos)
    # The impulses speed up as the pressure builds
    ix = np.sin(freq_x * t_sec * kinetic_velocity + phase_x)
    iy = np.cos(freq_y * t_sec * kinetic_velocity + phase_y)
    iz = np.sin(freq_z * t_sec * kinetic_velocity + phase_z)
    
    # Normalize to keep strictly inside the sphere bubble
    mag = np.sqrt(ix**2 + iy**2 + iz**2)
    ix = (ix / mag) * np.abs(np.sin(freq_x * t_sec))
    iy = (iy / mag) * np.abs(np.cos(freq_y * t_sec))
    iz = (iz / mag) * np.abs(np.sin(freq_z * t_sec))
    
    i_rot_x, i_rot_y, i_rot_z = rotate_3d(ix, iy, iz, rot_t, rot_t * 0.7, 0)
    
    inner_radius = radius * 0.85 # Keep gas slightly off the very edge
    proj_ix = 540 + (i_rot_x * inner_radius)
    proj_iy = 960 + (i_rot_y * inner_radius)
    proj_iz = i_rot_z * inner_radius

    # ---------------------------------------------------------
    # MEMORY SAFE RENDER PIPELINE
    # ---------------------------------------------------------
    fig = Figure(figsize=(10.8, 19.2), dpi=100, facecolor=C_BG)
    canvas = FigureCanvasAgg(fig)
    
    ax = fig.add_axes([0, 0, 1, 1], facecolor=C_BG)
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)
    ax.set_axis_off()

    # Draw the expanding Neural Web (The Balloon)
    # Render back-face fabric deeply transparent, front-face mostly opaque
    for idx_pair in connections:
        p1, p2 = idx_pair
        z_avg = (proj_bz[p1] + proj_bz[p2]) * 0.5
        
        # Depth shading
        if z_avg < 0:
            alpha = 0.1 
            lw = 0.5
        else:
            alpha = np.clip(0.15 + (inflation * 0.35), 0.2, 0.5)
            lw = 1.0 + (inflation * 0.5)
            
        ax.plot([proj_bx[p1], proj_bx[p2]], [proj_by[p1], proj_by[p2]], color=c_fabric, lw=lw, alpha=alpha)

    # Draw Boundary Nodes
    front_nodes = proj_bz > 0
    ax.scatter(proj_bx[front_nodes], proj_by[front_nodes], color=c_fabric, s=4 + (inflation * 8), alpha=0.8, zorder=4)

    # Draw Kinetic Impulses (Gas Molecules)
    front_impulses = proj_iz > -50
    tail_length = 3
    if inflation > 0.05:
        # Draw motion tails natively
        for t_step in range(1, tail_length + 1):
            past_t = max(0, t_sec - (t_step * 0.015))
            pix = np.sin(freq_x * past_t * kinetic_velocity + phase_x)
            piy = np.cos(freq_y * past_t * kinetic_velocity + phase_y)
            piz = np.sin(freq_z * past_t * kinetic_velocity + phase_z)
            pmag = np.sqrt(pix**2 + piy**2 + piz**2)
            pix, piy, piz = (pix/pmag)*np.abs(np.sin(freq_x*past_t)), (piy/pmag)*np.abs(np.cos(freq_y*past_t)), (piz/pmag)*np.abs(np.sin(freq_z*past_t))
            prx, pry, prz = rotate_3d(pix, piy, piz, rot_t, rot_t * 0.7, 0)
            
            p_ix = 540 + (prx * inner_radius)
            p_iy = 960 + (pry * inner_radius)
            
            ax.scatter(p_ix[front_impulses], p_iy[front_impulses], color=C_ACTIVE, s=15/t_step, alpha=0.5/t_step, zorder=5)

        # Primary heads
        ax.scatter(proj_ix[front_impulses], proj_iy[front_impulses], color=C_ACTIVE, s=18 + (inflation * 12), alpha=0.9, zorder=6)
        # Inner glow
        ax.scatter(proj_ix[front_impulses], proj_iy[front_impulses], color=C_BG, s=6 + (inflation * 4), alpha=0.9, zorder=7)

    # ---------------------------------------------------------
    # UI WIDGET COMPONENTS
    # ---------------------------------------------------------
    ax.text(60, 1820, "LG-473 :: THE MIND CONSTRUCT", color=C_TEXT, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(60, 1790, "SYSTEM: KINETIC PRESSURE VESSEL", color=C_DIM, fontsize=12, fontname='monospace', weight='bold', zorder=80)

    # Conceptual Explanation overlapping reality
    ax.text(60, 1640, "The impulses travel around the cluster of", color=C_TEXT, fontsize=14, fontname='monospace')
    ax.text(60, 1610, "neurons like gas molecules in a balloon.", color=C_TEXT, fontsize=14, fontname='monospace')
    ax.text(60, 1580, "Existence relies on structural pressure.", color=C_TEXT, fontsize=14, fontname='monospace')

    # Data Telemetry Box
    p_volume = (radius / 500.0) ** 3
    ax.text(60, 1480, f"INTERNAL PRESSURE  : {inflation * 100:>05.1f} kPa", color=C_TEXT, fontsize=14, fontname='monospace')
    ax.text(60, 1440, f"KINETIC AMPLITUDE  : {(kinetic_velocity-1)*100:>05.1f} Hz", color=C_TEXT, fontsize=14, fontname='monospace')
    ax.text(60, 1400, f"STRUCTURAL VOLUME  : {p_volume * 100:>05.1f} %", color=C_TEXT, fontsize=14, fontname='monospace')

    # Progress Tracking Baseplate
    ax.add_patch(Rectangle((60, 100), 960, 4, facecolor=C_DIM, zorder=80))
    bar_w = 960 * np.clip(t_sec / DURATION, 0, 1)
    ax.add_patch(Rectangle((60, 100), bar_w, 4, facecolor=C_ACTIVE, zorder=81))

    ax.text(60, 120, f"THERMODYNAMIC PHASE: {state_str}", color=C_TEXT, fontsize=12, fontname='monospace', weight='bold', zorder=80)
    ax.text(1020, 120, f"TIME [ {t_sec:>05.2f}s ]", color=C_TEXT, fontsize=12, fontname='monospace', ha='right', zorder=80)

    out_path = os.path.join(out_dir, f"frame_{f:04d}.png")
    fig.savefig(out_path, facecolor=C_BG, edgecolor='none')
    
    fig.clf()
    del ax, canvas, fig
    gc.collect() 
    if f % FPS == 0:
        print(f"Constructed Frame: {f} / {total_frames}")

if __name__ == "__main__":
    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)
    
    cores = max(1, mp.cpu_count() - 1)
    print(f"Executing The Mind Construct on {cores} cores...")
    
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
