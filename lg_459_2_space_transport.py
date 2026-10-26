import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import multiprocessing as mp
import subprocess
import os
import shutil
import math

# =============================================================================
# ENVIRONMENT VARIABLES & DAYLIGHT PALETTE
# =============================================================================
PROJECT_ID = "LG-459"
FPS = 60
DURATION = 24.0
FRAMES = int(FPS * DURATION)
OUTPUT_DIR = "LG_459_FRAMES"

C_BG = '#FFFFFF'               # Daylight Palette Background
C_SAFE = '#334155'             # Heavy Slate (Failsafe Structure)
C_FRAGILE = '#E11D48'          # Kinematic Red (Failure Nodes)
C_TEXT = '#111115'             # Indestructible Black (UI text)
C_GRID = '#CBD5E1'             # Subdued Steel (UI lines)

# =============================================================================
# KINEMATIC GENERATORS (TRUE O(N) WIREFRAME)
# =============================================================================
def generate_failsafe_transport():
    """
    Upper Frame: Rigid, conical, heavily strutted capsule. 
    O(1) logic. Maximum structural integrity.
    """
    lines = []
    base_z = 20.0
    top_z = 40.0
    base_r = 14.0
    top_r = 6.0
    segments = 32
    
    # Base and Top Rings
    for i in range(segments):
        a1 = (i / segments) * 2 * math.pi
        a2 = ((i + 1) / segments) * 2 * math.pi
        
        # Base ring
        x1, y1 = math.cos(a1) * base_r, math.sin(a1) * base_r
        x2, y2 = math.cos(a2) * base_r, math.sin(a2) * base_r
        lines.append(((x1, y1, base_z), (x2, y2, base_z), C_SAFE, 1.5))
        
        # Top ring
        tx1, ty1 = math.cos(a1) * top_r, math.sin(a1) * top_r
        tx2, ty2 = math.cos(a2) * top_r, math.sin(a2) * top_r
        lines.append(((tx1, ty1, top_z), (tx2, ty2, top_z), C_SAFE, 1.5))
        
        # Vertical / Diagonal Struts
        if i % 2 == 0:
            lines.append(((x1, y1, base_z), (tx1, ty1, top_z), C_SAFE, 1.0))
            # Heavy cross-bracing (Failsafe signature)
            lines.append(((x1, y1, base_z), (tx2, ty2, top_z), C_SAFE, 0.8))
            
    return lines

def generate_volatile_transport():
    """
    Lower Frame: Filigreed commercial booster. 
    High geometric complexity, fragile extensions, software-arbitrated.
    """
    lines = []
    base_z = -45.0
    top_z = -15.0
    body_r = 4.5
    segments = 32
    
    # Cylindrical Hull
    for i in range(segments):
        a1 = (i / segments) * 2 * math.pi
        a2 = ((i + 1) / segments) * 2 * math.pi
        
        x1, y1 = math.cos(a1) * body_r, math.sin(a1) * body_r
        x2, y2 = math.cos(a2) * body_r, math.sin(a2) * body_r
        
        lines.append(((x1, y1, base_z), (x2, y2, base_z), C_SAFE, 1.0))
        lines.append(((x1, y1, top_z), (x2, y2, top_z), C_SAFE, 1.0))
        
        if i % 4 == 0:
            lines.append(((x1, y1, base_z), (x1, y1, top_z), C_SAFE, 0.5))

    # Complex Grid Fins (Top) - High Failure Probability Nodes
    fin_extensions = [0, math.pi/2, math.pi, 3*math.pi/2]
    for angle in fin_extensions:
        fx = math.cos(angle) * body_r
        fy = math.sin(angle) * body_r
        ftx = math.cos(angle) * (body_r + 6.0)
        fty = math.sin(angle) * (body_r + 6.0)
        
        lines.append(((fx, fy, top_z - 2), (ftx, fty, top_z - 2), C_FRAGILE, 1.2))
        lines.append(((fx, fy, top_z - 6), (ftx, fty, top_z - 6), C_FRAGILE, 1.2))
        lines.append(((ftx, fty, top_z - 2), (ftx, fty, top_z - 6), C_FRAGILE, 1.2))
        
        # Grid web
        for g in range(1, 4):
            # Arbitrary interpolated software geometry
            gx = fx + (ftx - fx) * (g/4)
            gy = fy + (fty - fy) * (g/4)
            lines.append(((gx, gy, top_z - 2), (gx, gy, top_z - 6), C_FRAGILE, 0.5))

    # Fragile Landing Legs (Bottom)
    for angle in fin_extensions:
        cx, cy = math.cos(angle) * body_r, math.sin(angle) * body_r
        ex, ey = math.cos(angle) * (body_r + 8.0), math.sin(angle) * (body_r + 8.0)
        lines.append(((cx, cy, base_z + 8), (ex, ey, base_z - 4), C_SAFE, 1.0))
        lines.append(((cx, cy, base_z), (ex, ey, base_z - 4), C_FRAGILE, 0.8)) # Arbitrary actuator
        
    return lines

# =============================================================================
# CO-PROCESSOR RENDER MATRIX
# =============================================================================
def build_frame(frame_idx):
    fig, ax = plt.subplots(figsize=(10.8, 19.2), dpi=100)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    
    # 9:16 Aspect Ratio Constraints. Plenty of padding for YouTube UI.
    cam_span = 40.0
    y_span = cam_span * (19.2 / 10.8)  # Approx 71.1
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-y_span, y_span)
    ax.set_aspect('equal')
    ax.axis('off')

    # Continuous 360 Rotation + Fixed Elevation
    progress = frame_idx / FRAMES
    azi = np.radians(115.0 + (progress * 360.0))
    ele = np.radians(16.0)

    # Rotation Matrices
    cos_a, sin_a = np.cos(azi), np.sin(azi)
    cos_e, sin_e = np.cos(ele), np.sin(ele)

    R_z = np.array([
        [cos_a, -sin_a, 0],
        [sin_a,  cos_a, 0],
        [0,      0,     1]
    ])
    
    R_x = np.array([
        [1, 0,      0],
        [0, cos_e, -sin_e],
        [0, sin_e,  cos_e]
    ])
    
    R_total = R_x @ R_z

    raw_lines = generate_failsafe_transport() + generate_volatile_transport()
    
    projected_segments = []
    depths = []
    colors = []
    linewidths = []

    for pt1, pt2, color, lw in raw_lines:
        v1, v2 = np.array(pt1), np.array(pt2)
        
        rv1 = R_total @ v1
        rv2 = R_total @ v2
        
        avg_z = (rv1[2] + rv2[2]) / 2.0
        
        projected_segments.append([(rv1[0], rv1[1]), (rv2[0], rv2[1])])
        depths.append(avg_z)
        colors.append(color)
        linewidths.append(lw)

    # Painter's Algorithm Depth Sort
    sorted_indices = np.argsort(depths)
    sorted_segments = [projected_segments[i] for i in sorted_indices]
    sorted_colors = [colors[i] for i in sorted_indices]
    sorted_linewidths = [linewidths[i] for i in sorted_indices]

    lc = LineCollection(sorted_segments, colors=sorted_colors, linewidths=sorted_linewidths, 
                        capstyle='round', joinstyle='round')
    ax.add_collection(lc)

    # UI Context Parameters
    # UI Context Parameters
    plt.text(0.5, 0.90, 'UPPER SUBSYSTEM: FAILSAFE KINEMATICS', 
             transform=fig.transFigure, ha='center', va='center', 
             color=C_SAFE, fontsize=12, fontweight='bold')
             
    plt.text(0.5, 0.88, 'O(1) MECHANICAL LOGIC | RIGID TOPOLOGY', 
             transform=fig.transFigure, ha='center', va='center', 
             color=C_GRID, fontsize=10, fontweight='bold')

    plt.text(0.5, 0.12, 'LOWER SUBSYSTEM: VOLATILE KINEMATICS', 
             transform=fig.transFigure, ha='center', va='center', 
             color=C_FRAGILE, fontsize=12, fontweight='bold')

    plt.text(0.5, 0.10, 'SOFTWARE ARBITRATED | HIGH FAILURE PROBABILITY', 
             transform=fig.transFigure, ha='center', va='center', 
             color=C_GRID, fontsize=10, fontweight='bold')
    plt.text(0.5, 0.10, 'SOFTWARE ARBITRATED | HIGH FAILURE PROBABILITY', 
             transform=fig.transFigure, ha='center', va='center', 
             color=C_GRID, fontsize=10, fontweight='bold')

    plt.axhline(60, color=C_GRID, linewidth=0.5, alpha=0.5)
    plt.axhline(-60, color=C_GRID, linewidth=0.5, alpha=0.5)

    out_path = os.path.join(OUTPUT_DIR, f"frame_{frame_idx:04d}.png")
    plt.savefig(out_path, bbox_inches='tight', pad_inches=0, facecolor=C_BG)
    plt.close(fig)

# =============================================================================
# THROTTLE INITIATION & FFMPEG HARD BIND
# =============================================================================
if __name__ == '__main__':
    print(f"[{PROJECT_ID}] INITIATING TRUE CONTINUOUS VECTOR ARCHITECTURE.")
    
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    cores = max(1, mp.cpu_count() - 1)
    print(f"[{PROJECT_ID}] MULTIPROCESSING ALLOCATED: {cores} CORES.")
    
    with mp.Pool(processes=cores, maxtasksperchild=1) as pool:
        pool.map(build_frame, range(FRAMES), chunksize=16)

    print(f"[{PROJECT_ID}] FRAMES RENDERED. INITIATING FFMPEG BIND (MEMORY SAFE).")

    vid_name = f"{PROJECT_ID}_SPACE_TRANSPORT_MATRIX.mp4"
    ffmpeg_cmd = [
        'ffmpeg', '-y', '-framerate', str(FPS),
        '-i', os.path.join(OUTPUT_DIR, 'frame_%04d.png'),
        '-threads', '2',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-crf', '14',
        '-preset', 'fast',
        '-color_primaries', 'bt709',
        '-color_trc', 'bt709',
        '-colorspace', 'bt709',
        '-vf', 'scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-iw)/2:white',
        vid_name
    ]

    subprocess.run(ffmpeg_cmd, check=True)
    print(f"[{PROJECT_ID}] COMPILATION SECURED: {vid_name}")
