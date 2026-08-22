"""
PROJECT: Logic Garden 412 (The Minimax Tensor // Zero-Sum Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: NOUGHTS AND CROSSES, GAME THEORY, COMBINATORICS, KINEMATICS, DISCRETE MATHS
EXECUTION: 24.0s Sequence. True 3D Mathematical Construction & Topological Fork.
RULES ENFORCED:
- Daylight Palette (White Substrate / High-Contrast Chrome).
- Phase-Locked Metaphor: Stripping "play" into deterministic forced physics.
- Exact realisational aspect of a topological combinatorial trap.
- Australian spelling conventions enforced natively (Maths, Colour, Optimise).
- Absolute O(N) volumetric arrays with Lambertian shading.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
from matplotlib.collections import PolyCollection
import multiprocessing as mp
import os
import gc

# ======== SEQUENCE PARAMETERS ========
FPS = 60
DURATION = 24.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_412_tictactoe"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG            = '#FFFFFF'
C_TEXT          = '#111115'
C_EDGE          = '#111115'
C_GRID          = '#1E293B'  # Carbon Slate
C_CROSS         = '#DE008A'  # Deep Magenta (X)
C_NOUGHT        = '#00D2FF'  # High-Contrast Cyan (O)
C_WIN           = '#FFB300'  # Dense Amber (The Sovereign Vector)
C_GUI           = '#64748B'

LIGHT_DIR = np.array([-0.5, 0.8, -0.4])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

# ------------------------------------------------------------------
# DETERMINISTIC GAME STATE (THE COMBINATORIAL FORK)
# ------------------------------------------------------------------
# Board spatial bounds: spanning -60 to 60. Cell centers: -40, 0, 40.
def get_coords(row, col):
    y_map = {0: 40, 1: 0, 2: -40}  # Row 0 is Top
    x_map = {0: -40, 1: 0, 2: 40}  # Col 0 is Left
    return np.array([x_map[col], y_map[row], 0.0])

MOVES = [
    {'type': 'X', 'r': 0, 'c': 0, 't': 2.0},   # Move 1
    {'type': 'O', 'r': 1, 'c': 1, 't': 4.0},   # Move 2 (Center response)
    {'type': 'X', 'r': 2, 'c': 2, 't': 6.0},   # Move 3
    {'type': 'O', 'r': 0, 'c': 1, 't': 8.0},   # Move 4
    {'type': 'X', 'r': 2, 'c': 0, 't': 10.0},  # Move 5 (FORK LOCKED: Threatens 1,0 and 2,1)
    {'type': 'O', 'r': 1, 'c': 0, 't': 12.0},  # Move 6 (Forced Error)
    {'type': 'X', 'r': 2, 'c': 1, 't': 14.0},  # Move 7 (WIN MATRIX SECURED)
]

T_WIN = 15.0

print(f"PHASE 1: GAME MATRIX COMPILED [7 MOVES -> TERMINAL STATE REACHED]")

# ------------------------------------------------------------------
# MATRIX OPERATIONS
# ------------------------------------------------------------------
def rx(deg):
    rad = np.radians(deg); c, s = np.cos(rad), np.sin(rad)
    return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def ry(rad):
    c, s = np.cos(rad), np.sin(rad)
    return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def rz(rad):
    c, s = np.cos(rad), np.sin(rad)
    return np.array([[c,-s,0],[s,c,0],[0,0,1]])

def ease_in_out(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)

# ------------------------------------------------------------------
# O(N) PHYSICAL HARDWARE GEOMETRY FACTORY
# ------------------------------------------------------------------
def generate_strut(p1, p2, thickness, z_offset=0.0):
    v = p2 - p1
    L = np.linalg.norm(v)
    if L < 1e-4: return []
    v = v / L
    up = np.array([0.0, 0.0, 1.0])
    if np.abs(v[2]) > 0.99: up = np.array([1.0, 0.0, 0.0])
    
    right = np.cross(up, v)
    right = right / np.linalg.norm(right)
    real_up = np.cross(v, right)

    R = np.column_stack((right, real_up, v))
    t = thickness / 2.0
    l = L / 2.0
    
    vv = np.array([
        [-t, -t, -l], [ t, -t, -l], [ t,  t, -l], [-t,  t, -l],
        [-t, -t,  l], [ t, -t,  l], [ t,  t,  l], [-t,  t,  l]
    ])
    f_idx = [[0,1,2,3], [4,5,6,7], [0,1,5,4], [1,2,6,5], [2,3,7,6], [3,0,4,7]]
    
    faces = []
    mid = (p1 + p2) / 2.0
    mid[2] += z_offset
    for face in f_idx:
        rotated = np.dot(vv[face], R.T) + mid
        faces.append(rotated)
    return faces

def generate_X(center, z_base):
    # Two intersecting diagonal vectors
    d = 16.0
    faces = []
    faces += generate_strut(np.array([-d, -d, z_base]), np.array([ d,  d, z_base]), 8.0)
    faces += generate_strut(np.array([-d,  d, z_base]), np.array([ d, -d, z_base]), 8.0)
    for f in faces: f += center
    return faces

def generate_O(center, z_base):
    # 16-Segment Faceted Topological Ring
    segments = 16
    radius = 15.0
    thickness = 6.0
    faces = []
    for i in range(segments):
        a1 = i * (2 * np.pi / segments)
        a2 = (i + 1) * (2 * np.pi / segments)
        p1 = np.array([np.cos(a1)*radius, np.sin(a1)*radius, z_base])
        p2 = np.array([np.cos(a2)*radius, np.sin(a2)*radius, z_base])
        faces += generate_strut(p1, p2, thickness)
        
    for f in faces: f += center
    return faces

# Board geometry
BOARD_FACES = []
b_lw = 6.0
BOARD_FACES += generate_strut(np.array([-20., -60., 0.]), np.array([-20.,  60., 0.]), b_lw, -3.0)
BOARD_FACES += generate_strut(np.array([ 20., -60., 0.]), np.array([ 20.,  60., 0.]), b_lw, -3.0)
BOARD_FACES += generate_strut(np.array([-60., -20., 0.]), np.array([ 60., -20., 0.]), b_lw, -3.0)
BOARD_FACES += generate_strut(np.array([-60.,  20., 0.]), np.array([ 60.,  20., 0.]), b_lw, -3.0)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f_idx):
    t_sec = f_idx / float(FPS)
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.]); ax.set_axis_off(); fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540); ax.set_ylim(-960, 960)

    # 1. KINEMATIC CAMERA TENSOR
    # Smooth isometric orbit 1.0 deg/sec
    cam_angle = t_sec * 1.0 - 45.0
    M_cam = rx(-35.0) @ rz(np.radians(cam_angle))
    cam_dist = 400.0 
    
    faces_collected = []
    face_colors = []
    centroids_z = []
    
    def process_faces(geom_faces, hex_color):
        c_rgb = np.array(mcolors.to_rgb(hex_color))
        for face in geom_faces:
            v1 = face[1] - face[0]; v2 = face[2] - face[0]
            norm = np.cross(v1, v2)
            n_len = np.linalg.norm(norm)
            if n_len > 0: norm /= n_len
            
            diff = 0.5 + 0.5 * np.clip(np.dot(norm, LIGHT_DIR), 0, 1)
            fc = np.append(c_rgb * diff, 1.0)
            
            v_cam = np.einsum('ij,nj->ni', M_cam, face)
            v_cam[:, 2] += cam_dist
            if np.any(v_cam[:, 2] < 10.0): continue
            
            px = 1800.0 * (v_cam[:, 0] / v_cam[:, 2])
            py = 1800.0 * (v_cam[:, 1] / v_cam[:, 2])
            
            faces_collected.append(np.stack((px, py), axis=-1))
            face_colors.append(fc)
            centroids_z.append(np.mean(v_cam[:, 2]))

    # BUILD GRID
    process_faces(BOARD_FACES, C_GRID)
    
    # BUILD PIECES KINEMATICALLY
    for m in MOVES:
        if t_sec >= m['t']:
            # Z-Drop animation
            dt = t_sec - m['t']
            drop_prog = ease_in_out(np.clip(dt / 0.5, 0.0, 1.0))
            z_flight = 200.0 * (1.0 - drop_prog)
            
            center = get_coords(m['r'], m['c'])
            center[2] = z_flight
            
            if m['type'] == 'X':
                process_faces(generate_X(center, 4.0), C_CROSS)
            else:
                process_faces(generate_O(center, 4.0), C_NOUGHT)

    # BUILD WINNING TARGET VECTOR
    if t_sec >= T_WIN:
        dt = t_sec - T_WIN
        prog = ease_in_out(np.clip(dt / 0.5, 0.0, 1.0))
        # Winning line spans Row 2: (-40,-40) to (40,-40)
        p_start = np.array([-50.0, -40.0, 8.0])
        p_end_full = np.array([50.0, -40.0, 8.0])
        p_curr = p_start + (p_end_full - p_start) * prog
        
        process_faces(generate_strut(p_start, p_curr, 6.0), C_WIN)

    # 5. Z-SORT & RENDER O(N) COLLECTION
    sort_idx = np.argsort(centroids_z)[::-1] 
    sorted_faces = [faces_collected[i] for i in sort_idx]
    sorted_fcs = [face_colors[i] for i in sort_idx]
    
    if sorted_faces:
        ax.add_collection(PolyCollection(sorted_faces, facecolors=sorted_fcs, edgecolors='#111115', linewidths=0.8, joinstyle='miter'))

    # 6. HIGH-DENSITY HUD & TELEMETRY
    ax.add_patch(Rectangle((-540, 780), 1080, 180, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [780, 780], color=C_TEXT, lw=3, zorder=81)
    ax.text(-500, 880, "LG-412 :: MINIMAX TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 830, "[SFI-1.00] COMBINATORIAL FORK GEOMETRY", color=C_CROSS, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    prog = 0.0
    if t_sec < MOVES[0]['t']:
        state_msg = "PHASE 1: MATRIX INITIALISATION"
        state_col = C_GRID
        active_op = "3X3 LATTICE CONSTRUCTED. EVALUATING GAME TREE."
    elif t_sec < MOVES[4]['t']:
        state_msg = "PHASE 2: PERFECT INFORMATION SEQUENCE"
        state_col = C_NOUGHT
        active_op = "DETERMINISTIC Z-AXIS KINEMATIC DROPS EXECUTING."
        prog = (t_sec - MOVES[0]['t']) / (MOVES[4]['t'] - MOVES[0]['t'])
    elif t_sec < T_WIN:
        state_msg = "PHASE 3: O(N!) COMBINATORIAL FORK"
        state_col = C_CROSS
        active_op = "DUAL THREAT VECTORS DETECTED. DEFENCE IS MATHEMATICALLY IMPOSSIBLE."
        prog = 1.0
    else:
        state_msg = "PHASE 4: SOVEREIGN VECTOR (RESOLUTION)"
        state_col = C_WIN
        active_op = "TERMINAL STATE REACHED. KINEMATIC LOCK ESTABLISHED."
        prog = 1.0

    ax.text(-500, -780, f"PROTOCOL STATE : {state_msg}", color=state_col, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"DIAGNOSTIC     : {active_op}", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"AXIOMATIC TRUTH: NOUGHTS AND CROSSES IS NOT A GAME. IT IS A PURE ALGORITHMIC RESOLUTION.", color=C_TEXT, fontsize=11, fontname='monospace', zorder=82)

    ax.add_patch(Rectangle((-500, -920), 1000, 8, facecolor=C_GUI, zorder=82))
    ax.add_patch(Rectangle((-500, -920), 1000 * prog, 8, facecolor=state_col, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f_idx:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f_idx

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-412: MINIMAX TENSOR ENGAGED [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            pass
    print("Compilation Complete. Combinatorial matrix resolved.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
