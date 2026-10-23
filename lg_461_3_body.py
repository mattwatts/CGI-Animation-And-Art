import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import multiprocessing as mp
import subprocess
import os
import shutil

# =============================================================================
# ENVIRONMENT VARIABLES & HIGH-CONTRAST PALETTE
# =============================================================================
PROJECT_ID = "LG-461"
FPS = 60
DURATION = 20.0  # 20 seconds allows the chaotic maths to naturally unfold
FRAMES = int(FPS * DURATION)
OUTPUT_DIR = "LG_461_FRAMES"

C_BG = '#FFFFFF'               # White background
C_COMP_EDGE = '#334155'        # Machined Grey (The higher-dimensional network)
C_COMP_NODE = '#94A3B8'        # Light Grey for 4D vertices
C_BODY_1 = '#D91A1A'           # Deep Red
C_BODY_2 = '#002FA7'           # International Klein Blue
C_BODY_3 = '#FFB300'           # Gold
C_TRACK = '#1A1E24'            # Dark grey for targeting paths

# =============================================================================
# EXACT PHYSICS: THE 3-BODY GRAVITY SOLVER (RK4 MATHS)
# =============================================================================
# We pre-calculate the chaotic physics to guarantee mathematical accuracy.
# Masses
m1, m2, m3 = 1.0, 1.0, 1.0
G = 1.0

# Initial Conditions (A known 3D chaotic bound state)
# Positions (x, y, z)
p1 = np.array([1.0, -0.5, 0.2])
p2 = np.array([-1.0, 0.5, -0.2])
p3 = np.array([0.0, 0.0, 0.0])

# Velocities (x, y, z) - carefully balanced so they don't fly apart instantly
v3 = np.array([-0.9, -0.8, 0.3])
v1 = -v3 / 2.0 + np.array([0.1, 0.0, 0.1])
v2 = -v3 / 2.0 - np.array([0.1, 0.0, 0.1])

state = np.concatenate([p1, p2, p3, v1, v2, v3])

def compute_gravity(t, y):
    r1, r2, r3 = y[0:3], y[3:6], y[6:9]
    v1_curr, v2_curr, v3_curr = y[9:12], y[12:15], y[15:18]
    
    def force(ra, rb, ma, mb):
        diff = rb - ra
        dist = np.linalg.norm(diff) + 1e-5  # Softening to prevent singularity crash
        return G * mb * diff / (dist**3)
    
    a1 = force(r1, r2, m1, m2) + force(r1, r3, m1, m3)
    a2 = force(r2, r1, m2, m1) + force(r2, r3, m2, m3)
    a3 = force(r3, r1, m3, m1) + force(r3, r2, m3, m2)
    
    return np.concatenate([v1_curr, v2_curr, v3_curr, a1, a2, a3])

def rk4_step(y, dt):
    k1 = compute_gravity(0, y)
    k2 = compute_gravity(0, y + 0.5 * dt * k1)
    k3 = compute_gravity(0, y + 0.5 * dt * k2)
    k4 = compute_gravity(0, y + dt * k3)
    return y + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

# Precompute the paths over the timeline
sim_steps_per_frame = 8
dt_sim = 0.005
history = np.zeros((FRAMES, 18))

print(f"[{PROJECT_ID}] Calculating exact physical trajectories...")
current_state = state
for f in range(FRAMES):
    for _ in range(sim_steps_per_frame):
        current_state = rk4_step(current_state, dt_sim)
    history[f] = current_state

# Centers the camera on the center of mass
com_history = (history[:, 0:3]*m1 + history[:, 3:6]*m2 + history[:, 6:9]*m3) / (m1+m2+m3)

# =============================================================================
# HIGHER-DIMENSIONAL COMPUTER (4D TESSERACT GENERATOR)
# =============================================================================
def generate_tesseract(t_progress):
    """
    Creates a 4D hypercube, rotates it in the 4th dimension (X-W plane), 
    and mathematically projects it down to 3D space.
    """
    # 16 vertices of a hypercube
    vertices_4d = []
    for x in [-1, 1]:
        for y in [-1, 1]:
            for z in [-1, 1]:
                for w in [-1, 1]:
                    vertices_4d.append(np.array([x, y, z, w]))
                    
    # Edges connect vertices that differ by exactly one coordinate
    edges = []
    for i in range(16):
        for j in range(i+1, 16):
            diff = np.abs(vertices_4d[i] - vertices_4d[j])
            if np.sum(diff) == 2:
                edges.append((i, j))

    # Angle for 4D rotation (continuous over the video)
    theta = t_progress * 2 * np.pi 
    cos_t, sin_t = np.cos(theta), np.sin(theta)
    
    projected_3d = []
    scale_factor = 2.5
    
    for v in vertices_4d:
        # Rotate in the X-W plane
        x_rot = v[0] * cos_t - v[3] * sin_t
        w_rot = v[0] * sin_t + v[3] * cos_t
        
        # Stereographic projection from 4D to 3D
        distance = 3.0
        w_proj = 1.0 / (distance - w_rot)
        
        x_3d = x_rot * w_proj * scale_factor
        y_3d = v[1] * w_proj * scale_factor
        z_3d = v[2] * w_proj * scale_factor
        
        projected_3d.append(np.array([x_3d, y_3d, z_3d]))
        
    lines_3d = []
    for edge in edges:
        p1 = projected_3d[edge[0]]
        p2 = projected_3d[edge[1]]
        lines_3d.append((p1, p2, C_COMP_EDGE, 1.2))
        
    return lines_3d, projected_3d

# =============================================================================
# RENDER ENGINE
# =============================================================================
def build_frame(frame_idx):
    fig, ax = plt.subplots(figsize=(10.8, 19.2), dpi=100)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    
    # 9:16 portrait bounds
    cam_span = 3.2
    y_span = cam_span * (19.2 / 10.8)
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-y_span, y_span)
    ax.set_aspect('equal')
    ax.axis('off')

    t_progress = frame_idx / FRAMES
    
    # Slow 3D camera rotation to view the full volume
    azi = np.radians(45.0 + (t_progress * 180.0))
    ele = np.radians(25.0 + np.sin(t_progress * np.pi) * 15.0)

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

    # Get physics data up to current frame
    com = com_history[frame_idx]
    r1 = history[frame_idx, 0:3] - com
    r2 = history[frame_idx, 3:6] - com
    r3 = history[frame_idx, 6:9] - com

    # Gather geometry
    raw_lines = []
    
    # 1. 4D Computer Network
    tesseract_lines, tess_nodes = generate_tesseract(t_progress)
    raw_lines.extend(tesseract_lines)
    
    # Tracking lines from the computer framework to the objects
    node_a = tess_nodes[0]
    node_b = tess_nodes[-1]
    node_c = tess_nodes[8]
    raw_lines.append((node_a, r1, C_TRACK, 0.5))
    raw_lines.append((node_b, r2, C_TRACK, 0.5))
    raw_lines.append((node_c, r3, C_TRACK, 0.5))

    # 2. 3-Body Trajectories (Trails)
    trail_length = min(frame_idx, 150) # Trail length
    for t_step in range(1, trail_length):
        idx = frame_idx - t_step
        idx_prev = idx - 1
        fade = 1.0 - (t_step / trail_length)
        lw = 2.0 * fade
        
        c = com_history[idx]
        cp = com_history[idx_prev]
        
        raw_lines.append((history[idx_prev, 0:3]-cp, history[idx, 0:3]-c, C_BODY_1, lw))
        raw_lines.append((history[idx_prev, 3:6]-cp, history[idx, 3:6]-c, C_BODY_2, lw))
        raw_lines.append((history[idx_prev, 6:9]-cp, history[idx, 6:9]-c, C_BODY_3, lw))

    # Add the current positions as distinct points (small segments for the renderer)
    def add_sphere(pos, color):
        s = 0.05
        raw_lines.append((pos - np.array([s,0,0]), pos + np.array([s,0,0]), color, 6.0))
        raw_lines.append((pos - np.array([0,s,0]), pos + np.array([0,s,0]), color, 6.0))
        raw_lines.append((pos - np.array([0,0,s]), pos + np.array([0,0,s]), color, 6.0))
        
    add_sphere(r1, C_BODY_1)
    add_sphere(r2, C_BODY_2)
    add_sphere(r3, C_BODY_3)

    # Apply 3D Projection
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

    # Sort geometry by depth (Painter's Algorithm)
    sorted_indices = np.argsort(depths)
    sorted_segments = [projected_segments[i] for i in sorted_indices]
    sorted_colors = [colors[i] for i in sorted_indices]
    sorted_linewidths = [linewidths[i] for i in sorted_indices]

    lc = LineCollection(sorted_segments, colors=sorted_colors, linewidths=sorted_linewidths, 
                        capstyle='round', joinstyle='round')
    ax.add_collection(lc)

    out_path = os.path.join(OUTPUT_DIR, f"frame_{frame_idx:04d}.png")
    plt.savefig(out_path, bbox_inches='tight', pad_inches=0, facecolor=C_BG)
    plt.close(fig)

# =============================================================================
# MULTIPROCESSING & FFMPEG
# =============================================================================
if __name__ == '__main__':
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    cores = max(1, mp.cpu_count() - 1)
    print(f"[{PROJECT_ID}] Allocating {cores} cores for rendering...")
    
    with mp.Pool(processes=cores) as pool:
        pool.map(build_frame, range(FRAMES), chunksize=8)

    vid_name = f"{PROJECT_ID}_3_BODY_DIMENSIONALITY.mp4"
    print(f"[{PROJECT_ID}] Executing ffmpeg output...")
    
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
    print(f"[{PROJECT_ID}] Compilation complete: {vid_name}")
