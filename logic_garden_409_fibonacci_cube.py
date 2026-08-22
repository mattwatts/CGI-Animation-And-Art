"""
PROJECT: Logic Garden 409 (The Fibonacci Cube // Hierarchical Graph Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: FIBONACCI CUBE, GRAPH THEORY, HYPERCUBE, KINEMATICS, DISCRETE MATHS
EXECUTION: 24.0s Sequence. True 3D Mathematical Construction & Topological Spallation.
RULES ENFORCED:
- Daylight Palette (White Substrate / High-Contrast Chrome).
- Phase-Locked Metaphor: Graph filtering via catastrophic physical yielding.
- Exact realisational aspect of topological struts and node alignment.
- Australian spelling conventions enforced natively (Maths, Colour, Optimise).
- Absolute O(N) volumetric arrays mapping 6D -> 3D coordinates.
- HOTFIX: Absolute Cinematic Lock (Radial velocity crushed to 1.0 deg/sec).
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
OUT_DIR = "frames_409_fibonacci"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG            = '#FFFFFF'
C_TEXT          = '#111115'
C_EDGE          = '#111115'
C_SCENE         = '#111115'  # Indestructible Black (Raw Hypercube Node)
C_VALID         = '#1E293B'  # Carbon Slate (Audited Valid)
C_FAIL          = '#FF3300'  # Intense Red (Audit Failure / Spallation)
C_FIBO          = '#00D2FF'  # High-Contrast Cyan (Golden Yield)
C_STEEL         = '#94A3B8'  # Topological Struts
C_GUI           = '#64748B'

LIGHT_DIR = np.array([-0.5, 0.8, -0.4])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

# ------------------------------------------------------------------
# O(1) 6D HYPERCUBE MAP TO 3D CARTESIAN ARCHITECTURE
# ------------------------------------------------------------------
# Generating an explicit asymmetric 6D -> 3D basis to prevent spatial overlapping
BASIS_6D = np.array([
    [ 1.0,  0.4,  0.2],
    [ 0.3,  1.0,  0.5],
    [-0.7,  0.8, -0.3],
    [-0.5, -0.3,  1.0],
    [-0.2, -0.9, -0.6],
    [ 0.8, -0.6,  0.7]
]) * 180.0

def get_hamming_weight(binary_str):
    return binary_str.count('1')

def get_hypercube_pos(binary_str):
    pos = np.zeros(3)
    for i, bit in enumerate(binary_str):
        if bit == '1':
            pos += BASIS_6D[i] * 0.5
        else:
            pos -= BASIS_6D[i] * 0.5
    return pos

NODES = []
EDGES = []
np.random.seed(409)

# 1. Compile 64 Nodes (Q_6)
for i in range(64):
    b_str = f"{i:06b}"
    is_fibo = not ('11' in b_str)
    pos_orig = get_hypercube_pos(b_str)
    
    node = {
        'id': i,
        'b_str': b_str,
        'is_fibo': is_fibo,
        'pos_orig': pos_orig,
        'vel': (pos_orig / (np.linalg.norm(pos_orig) + 1e-4) + np.random.uniform(-0.1, 0.1, 3)) * 600.0,
        'hamming': get_hamming_weight(b_str)
    }
    NODES.append(node)

# 2. Compile Exact Mathematical Edges (Hamming Distance == 1)
for i in range(64):
    for j in range(i + 1, 64):
        diff = i ^ j
        if diff != 0 and (diff & (diff - 1)) == 0:  # O(1) bitwise check for exactly one bit diff
            EDGES.append((i, j))

# 3. Compile Hierarchical Fibonacci Crystal Layout (Calculated per Hamming Layer)
fibo_groups = {0: [], 1: [], 2: [], 3: []}
for n in NODES:
    if n['is_fibo']:
        fibo_groups[n['hamming']].append(n)

for h, items in fibo_groups.items():
    z_layer = 300.0 - h * 200.0
    n_items = len(items)
    if n_items == 1:
        items[0]['pos_fibo'] = np.array([0.0, 0.0, z_layer])
    else:
        rad = 80.0 + n_items * 13.0
        for idx, it in enumerate(items):
            theta = idx * (2 * np.pi / n_items)
            it['pos_fibo'] = np.array([rad * np.cos(theta), rad * np.sin(theta), z_layer])

print(f"PHASE 1: TOPOLOGICAL TENSOR PRE-COMPILED [64 NODES, 192 STRUTS]")

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

def lerp_colour(c1_hex, c2_hex, t):
    c1 = np.array(mcolors.to_rgb(c1_hex))
    c2 = np.array(mcolors.to_rgb(c2_hex))
    return c1 * (1.0 - t) + c2 * t

# ------------------------------------------------------------------
# O(N) PHYSICAL HARDWARE GEOMETRY FACTORY
# ------------------------------------------------------------------
def generate_cube(center, size):
    r = size / 2.0
    v = np.array([
        [-r, -r, -r], [ r, -r, -r], [ r,  r, -r], [-r,  r, -r],
        [-r, -r,  r], [ r, -r,  r], [ r,  r,  r], [-r,  r,  r]
    ])
    f_idx = [[0,1,2,3], [4,5,6,7], [0,1,5,4], [1,2,6,5], [2,3,7,6], [3,0,4,7]]
    return [v[f] + center for f in f_idx]

def generate_strut(p1, p2, thickness):
    v = p2 - p1
    L = np.linalg.norm(v)
    if L < 1e-4: return []
    v = v / L
    up = np.array([0.0, 1.0, 0.0])
    if np.abs(v[1]) > 0.99: up = np.array([1.0, 0.0, 0.0])
    
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
    for face in f_idx:
        rotated = np.dot(vv[face], R.T) + mid
        faces.append(rotated)
    return faces

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
    # ABSOLUTE STUDY MODE: Angular velocity heavily throttled to 1.0 deg/sec
    cam_angle = t_sec * 1.0 - 45.0
    M_cam = rx(-22.0) @ ry(cam_angle)
    cam_dist = 1100.0 
    
    # Timeline Logic
    T_SCAN_STARTS = 4.0
    T_SCAN_ENDS   = 11.0
    T_EXPLODE     = 12.0
    T_SNAP_STARTS = 15.0
    T_SNAP_ENDS   = 18.0

    # Calculate boolean scan plane height
    scan_y = 600.0
    if T_SCAN_STARTS <= t_sec <= T_SCAN_ENDS:
        prog = (t_sec - T_SCAN_STARTS) / (T_SCAN_ENDS - T_SCAN_STARTS)
        scan_y = 400.0 - (prog * 800.0)
    elif t_sec > T_SCAN_ENDS:
        scan_y = -600.0

    faces_collected = []
    face_colors = []
    centroids_z = []
    
    # Node State Evaluation
    node_positions = {}
    node_colors = {}
    node_alive = {}
    
    for n in NODES:
        pos = n['pos_orig'].copy()
        alive = True
        
        # Color mapping based on Audit
        n_col = mcolors.to_rgb(C_SCENE)
        if pos[1] > scan_y:
            if n['is_fibo']:
                n_col = mcolors.to_rgb(C_VALID)
            else:
                n_col = mcolors.to_rgb(C_FAIL)
                
        # Kinematics Execution
        if not n['is_fibo'] and t_sec >= T_EXPLODE:
            dt_exp = t_sec - T_EXPLODE
            pos += n['vel'] * dt_exp + 0.5 * np.array([0.0, -1200.0, 0.0]) * (dt_exp ** 2)
            if pos[1] < -2000.0:
                alive = False
                
        if n['is_fibo'] and t_sec >= T_SNAP_STARTS:
            dt_snap = (t_sec - T_SNAP_STARTS) / (T_SNAP_ENDS - T_SNAP_STARTS)
            lerp_t = ease_in_out(dt_snap)
            pos = pos * (1.0 - lerp_t) + n['pos_fibo'] * lerp_t
            
            if t_sec > T_SNAP_ENDS:
                # Golden Yield Glow after snap finishes
                n_col = mcolors.to_rgb(C_FIBO)

        node_positions[n['id']] = pos
        node_colors[n['id']] = np.array(n_col)
        node_alive[n['id']] = alive

    # 2. O(N) GEOMETRY COMPILER
    # Generate Physical Struts
    for (i, j) in EDGES:
        if not node_alive[i] or not node_alive[j]:
            continue
            
        p1 = node_positions[i]
        p2 = node_positions[j]
        
        # Strut color defaults to steel, unless connected node failed audit.
        s_col = np.array(mcolors.to_rgb(C_STEEL))
        if np.array_equal(node_colors[i], mcolors.to_rgb(C_FAIL)) or np.array_equal(node_colors[j], mcolors.to_rgb(C_FAIL)):
            s_col = np.array(mcolors.to_rgb(C_FAIL))
        
        # Determine strut thickness (thickens on Golden Yield)
        t_strut = 2.5
        if t_sec > T_SNAP_ENDS and NODES[i]['is_fibo'] and NODES[j]['is_fibo']:
            t_strut = 3.5
            s_col = np.array(mcolors.to_rgb(C_TEXT)) # Shifts to black for clean contrast
            
        strut_faces = generate_strut(p1, p2, t_strut)
        for face in strut_faces:
            # Lambertian normal
            v1 = face[1] - face[0]
            v2 = face[2] - face[0]
            norm = np.cross(v1, v2)
            n_len = np.linalg.norm(norm)
            if n_len > 0: norm /= n_len
            
            diff = 0.5 + 0.5 * np.clip(np.dot(norm, LIGHT_DIR), 0, 1)
            fc = np.append(s_col * diff, 1.0)
            
            v_cam = np.einsum('ij,nj->ni', M_cam, face)
            v_cam[:, 2] += cam_dist
            if np.any(v_cam[:, 2] < 10.0): continue
            
            px = 1800.0 * (v_cam[:, 0] / v_cam[:, 2]); py = 1800.0 * (v_cam[:, 1] / v_cam[:, 2])
            faces_collected.append(np.stack((px, py), axis=-1))
            face_colors.append(fc)
            centroids_z.append(np.mean(v_cam[:, 2]))

    # Generate Physical Nodes
    for n in NODES:
        if not node_alive[n['id']]: continue
        
        n_col = node_colors[n['id']]
        cube_faces = generate_cube(node_positions[n['id']], 18.0)
        
        for face in cube_faces:
            v1 = face[1] - face[0]
            v2 = face[2] - face[0]
            norm = np.cross(v1, v2)
            n_len = np.linalg.norm(norm)
            if n_len > 0: norm /= n_len
            
            diff = 0.4 + 0.6 * np.clip(np.dot(norm, LIGHT_DIR), 0, 1)
            fc = np.append(n_col * diff, 1.0)
            
            v_cam = np.einsum('ij,nj->ni', M_cam, face)
            v_cam[:, 2] += cam_dist
            if np.any(v_cam[:, 2] < 10.0): continue
            
            px = 1800.0 * (v_cam[:, 0] / v_cam[:, 2]); py = 1800.0 * (v_cam[:, 1] / v_cam[:, 2])
            faces_collected.append(np.stack((px, py), axis=-1))
            face_colors.append(fc)
            centroids_z.append(np.mean(v_cam[:, 2]) - 5.0) # Bias nodes slightly forward to cap struts cleanly

    # 3. Z-SORT & RENDER O(N) COLLECTION
    sort_idx = np.argsort(centroids_z)[::-1] 
    sorted_faces = [faces_collected[i] for i in sort_idx]
    sorted_fcs = [face_colors[i] for i in sort_idx]
    
    if sorted_faces:
        ax.add_collection(PolyCollection(sorted_faces, facecolors=sorted_fcs, edgecolors='#111115', linewidths=0.4, joinstyle='miter'))

    # 4. HIGH-DENSITY HUD & TELEMETRY
    ax.add_patch(Rectangle((-540, 780), 1080, 180, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [780, 780], color=C_TEXT, lw=3, zorder=81)
    ax.text(-500, 880, "LG-409 :: FIBONACCI CUBE MATRIX", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 830, "[SFI-1.00] TOPOLOGICAL SPALLATION & KINEMATIC ALIGNMENT", color=C_FIBO, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    prog = 0.0
    if t_sec < T_SCAN_STARTS:
        state_msg = "PHASE 1: 6-DIMENSIONAL HYPERCUBE SCAFFOLD (Q6)"
        state_col = C_TEXT
        active_op = "GEOMETRIC SUPRA-MATRIX CONSTRUCTED. 64 NODES."
    elif t_sec < T_EXPLODE:
        state_msg = "PHASE 2: THE SERIALISATION RAZOR"
        state_col = C_FAIL
        active_op = "AUDITING BINARY STRINGS. FLAGGING CONSECUTIVE ONES ('11')."
        prog = (t_sec - T_SCAN_STARTS) / (T_SCAN_ENDS - T_SCAN_STARTS)
    elif t_sec < T_SNAP_STARTS:
        state_msg = "PHASE 3: KINEMATIC SPALLATION & STRUT FAILURE"
        state_col = C_FAIL
        active_op = "ILLEGAL NODES VIOLENTLY EJECTED. TOPOLOGY SHEARING."
        prog = 1.0
    elif t_sec < T_SNAP_ENDS:
        state_msg = "PHASE 4: STRUCTURAL REALIGNMENT"
        state_col = C_VALID
        active_op = "KINEMATIC LERP. ORGANISING BY HAMMING WEIGHT."
        prog = 1.0
    else:
        state_msg = "PHASE 5: THE GOLDEN YIELD"
        state_col = C_FIBO
        active_op = "ABSOLUTE RESOLUTION: FIBONACCI CUBE (21 NODES)."
        prog = 1.0

    ax.text(-500, -780, f"PROTOCOL STATE : {state_msg}", color=state_col, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"DIAGNOSTIC     : {active_op}", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"AXIOMATIC TRUTH: TO EXTRACT THE MATHEMATICS, THE FLAWS MUST BE DESTROYED.", color=C_TEXT, fontsize=11, fontname='monospace', zorder=82)

    ax.add_patch(Rectangle((-500, -920), 1000, 8, facecolor=C_GUI, zorder=82))
    ax.add_patch(Rectangle((-500, -920), 1000 * prog, 8, facecolor=state_col, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f_idx:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f_idx

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-409 (STUDY MODE): FIBONACCI TENSOR ENGAGED [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            pass
    print("Compilation Complete. Matrix resolved to Fibonacci yield.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
