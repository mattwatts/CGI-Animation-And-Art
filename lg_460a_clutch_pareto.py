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
PROJECT_ID = "LG-460"
FPS = 60
DURATION = 24.0
FRAMES = int(FPS * DURATION)
OUTPUT_DIR = "LG_460_FRAMES"

C_BG = '#FFFFFF'               # Daylight Palette
C_ENV = '#334155'              # Heavy Slate (The Environment Drive Shaft)
C_SELF_IDLE = '#007FFF'        # Azure (Fluid, Unengaged State, Low Load)
C_SELF_LOAD = '#E11D48'        # Kinematic Red (Forced Interaction, High Friction)
C_PARETO = '#94A3B8'           # Subdued Steel (The Optimal Surface)
C_VECTOR = '#FFB300'           # Gold (The Active State Tracer)
C_TEXT = '#111115'             # Indestructible Black
C_GRID = '#CBD5E1'

# =============================================================================
# KINEMATIC GENERATORS (TRUE O(N) WIREFRAME)
# =============================================================================
def generate_pareto_surface(clutch_gap_ratio):
    """
    Upper Frame (Z +20 to +50): Hyperbolic Paraboloid.
    Represents the mathematical tension between Energy (X) and Engagement (Y).
    """
    lines = []
    z_offset = 35.0
    grid_size = 12
    step = 1.5
    
    # Generate the base surface grid
    for x in np.arange(-grid_size, grid_size + step, step):
        for y in np.arange(-grid_size, grid_size + step, step):
            # Saddle math: z = (x^2 - y^2) / scale
            z1 = (x**2 - y**2) / 8.0
            
            # Connect X edges
            if x + step <= grid_size:
                z2 = ((x + step)**2 - y**2) / 8.0
                lines.append(((x, y, z1 + z_offset), (x + step, y, z2 + z_offset), C_PARETO, 0.5))
            
            # Connect Y edges
            if y + step <= grid_size:
                z3 = (x**2 - (y + step)**2) / 8.0
                lines.append(((x, y, z1 + z_offset), (x, y + step, z3 + z_offset), C_PARETO, 0.5))

    # The State Vector: Moves from optimal center (conserving) to the edges (high drain) as clutch engages
    # clutch_gap_ratio: 1.0 = fully separated (conserving), 0.0 = fully engaged (draining)
    vx = (1.0 - clutch_gap_ratio) * grid_size * 0.9  # Pushed outward by engagement
    vy = 0.0 # Stay on interaction axis
    vz = (vx**2 - vy**2) / 8.0
    
    # Plumb line dropping from the optimal Pareto point
    lines.append(((vx, vy, vz + z_offset), (vx, vy, z_offset - 10), C_VECTOR, 2.0))
    # Horizontal cross tracking
    lines.append(((vx - 3, vy, vz + z_offset), (vx + 3, vy, vz + z_offset), C_VECTOR, 1.5))
    lines.append(((vx, vy - 3, vz + z_offset), (vx, vy + 3, vz + z_offset), C_VECTOR, 1.5))

    return lines

def generate_clutch_kinematics(t_progress):
    """
    Lower Frame (Z -50 to -20): The mechanical transition between fluidity and forced interaction.
    """
    lines = []
    base_z = -35.0
    radius = 14.0
    segments = 48
    
    # Kinematic gap logic: 2 full engage/disengage cycles over the 24 sec duration
    # gap goes from 15 (fluid) to 0 (hard interaction)
    wave = math.cos(t_progress * 4 * math.pi)
    gap = 15.0 * ((1.0 - wave) / 2.0)
    gap_ratio = gap / 15.0
    
    # Rotation logic 
    # Environment drives constantly and fast
    env_angle = t_progress * 360.0 * 4.0 
    
    # Self/Biological spin. When fluid (gap wide), it's slow. When engaged (gap 0), it is forced to match env.
    fluid_angle = t_progress * 360.0 * -1.0 # Spinning independently
    forced_angle = env_angle # Forced to match
    self_angle = (fluid_angle * gap_ratio) + (forced_angle * (1.0 - gap_ratio))
    
    # Thermodynamic friction colour map. Transition from Azure (fluid) to Red (engaged/burning glucose).
    def lerp_color(c1, c2, factor):
        c1 = c1.lstrip('#')
        c2 = c2.lstrip('#')
        r = int(int(c1[0:2], 16) * factor + int(c2[0:2], 16) * (1 - factor))
        g = int(int(c1[2:4], 16) * factor + int(c2[2:4], 16) * (1 - factor))
        b = int(int(c1[4:6], 16) * factor + int(c2[4:6], 16) * (1 - factor))
        return f"#{r:02x}{g:02x}{b:02x}"

    dynamic_self_color = lerp_color(C_SELF_IDLE, C_SELF_LOAD, 1.0 - gap_ratio)

    z_env = base_z + gap
    z_self = base_z - gap

    # Build drive plates (True Vector Rings)
    for i in range(segments):
        a1 = (i / segments) * 2 * math.pi
        a2 = ((i + 1) / segments) * 2 * math.pi
        
        # Environment Plate (Top)
        ea1 = a1 + math.radians(env_angle)
        ea2 = a2 + math.radians(env_angle)
        ex1, ey1 = math.cos(ea1) * radius, math.sin(ea1) * radius
        ex2, ey2 = math.cos(ea2) * radius, math.sin(ea2) * radius
        lines.append(((ex1, ey1, z_env), (ex2, ey2, z_env), C_ENV, 2.0))
        # Env Spoke
        if i % 6 == 0:
            lines.append(((0, 0, z_env), (ex1, ey1, z_env), C_ENV, 1.0))
            # Env vertical drive shaft
            lines.append(((0, 0, z_env), (0, 0, z_env + 15), C_ENV, 3.0))

        # Biological/Self Plate (Bottom)
        sa1 = a1 + math.radians(self_angle)
        sa2 = a2 + math.radians(self_angle)
        sx1, sy1 = math.cos(sa1) * radius, math.sin(sa1) * radius
        sx2, sy2 = math.cos(sa2) * radius, math.sin(sa2) * radius
        lines.append(((sx1, sy1, z_self), (sx2, sy2, z_self), dynamic_self_color, 2.0))
        # Self Spoke
        if i % 6 == 0:
            lines.append(((0, 0, z_self), (sx1, sy1, z_self), dynamic_self_color, 1.0))
            # Self vertical baseline shaft
            lines.append(((0, 0, z_self), (0, 0, z_self - 15), dynamic_self_color, 3.0))
            
        # Friction/Interaction Struts (only show when plates are close)
        if gap < 2.0 and i % 3 == 0:
             lines.append(((ex1, ey1, z_env), (sx1, sy1, z_self), C_SELF_LOAD, 2.5 - gap))

    return lines, gap_ratio

# =============================================================================
# CO-PROCESSOR RENDER MATRIX
# =============================================================================
# =============================================================================
# CO-PROCESSOR RENDER MATRIX (CORRECTED)
# =============================================================================
def build_frame(frame_idx):
    fig, ax = plt.subplots(figsize=(10.8, 19.2), dpi=100)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    
    cam_span = 40.0
    y_span = cam_span * (19.2 / 10.8) 
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-y_span, y_span)
    ax.set_aspect('equal')
    ax.axis('off')

    t_progress = frame_idx / FRAMES
    azi = np.radians(115.0 + (t_progress * 360.0))
    ele = np.radians(16.0)

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

    clutch_lines, gap_ratio = generate_clutch_kinematics(t_progress)
    pareto_lines = generate_pareto_surface(gap_ratio)
    raw_lines = clutch_lines + pareto_lines
    
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

    # Painter's Algorithm
    sorted_indices = np.argsort(depths)
    sorted_segments = [projected_segments[i] for i in sorted_indices]
    sorted_colors = [colors[i] for i in sorted_indices]
    sorted_linewidths = [linewidths[i] for i in sorted_indices]

    lc = LineCollection(sorted_segments, colors=sorted_colors, linewidths=sorted_linewidths, 
                        capstyle='round', joinstyle='round')
    ax.add_collection(lc)

    # Contextual UI Overlays for Video Compression 
    plt.text(0.5, 0.90, 'UPPER: PARETO TARGET SURFACE', transform=fig.transFigure, ha='center', va='center', color=C_PARETO, fontsize=12, fontweight='bold')
    plt.text(0.5, 0.88, 'V1. OPTIMAL ENERGY TARGET (SOVEREIGN USEFULNESS)', transform=fig.transFigure, ha='center', va='center', color=C_GRID, fontsize=9, fontweight='bold')
    
    plt.text(0.5, 0.14, 'LOWER: THE CLUTCH OF INTERACTION', transform=fig.transFigure, ha='center', va='center', color=C_ENV, fontsize=12, fontweight='bold')
    
    state_text = 'STATE: DISENGAGED (FLUIDITY / CONSERVATION)' if gap_ratio > 0.05 else 'STATE: FORCED ENGAGEMENT (GLUCOSE DRAIN)'
    state_color = C_SELF_IDLE if gap_ratio > 0.05 else C_SELF_LOAD
    
    plt.text(0.5, 0.12, state_text, transform=fig.transFigure, ha='center', va='center', color=state_color, fontsize=10, fontweight='bold')
    plt.axhline(55, color=C_GRID, linewidth=0.5, alpha=0.5)
    plt.axhline(-55, color=C_GRID, linewidth=0.5, alpha=0.5)

    out_path = os.path.join(OUTPUT_DIR, f"frame_{frame_idx:04d}.png")
    plt.savefig(out_path, bbox_inches='tight', pad_inches=0, facecolor=C_BG)
    plt.close(fig)

# =============================================================================
# HARDWARE THROTTLE & BIND
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

    print(f"[{PROJECT_ID}] FRAMES RENDERED. CLUTCHING FFMPEG IN TERMINAL.")

    vid_name = f"{PROJECT_ID}_CLUTCH_OF_INTERACTION.mp4"
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
