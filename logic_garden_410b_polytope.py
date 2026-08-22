"""
PROJECT: Logic Garden 410d (The Dimensional Polytope Tensor // Compressed Parity Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: POLYTOPE, TESSERACT, 4D GEOMETRY, KINEMATICS, DISCRETE MATHS
EXECUTION: 24.0s Sequence. True 4D Mathematical Rotation mapped to 3D Physical Struts.
RULES ENFORCED:
- Daylight Palette (White Substrate / High-Contrast Chrome).
- Phase-Locked Metaphor: Stripping the cognitive hallucination of 4D space.
- Exact realisational aspect of topological struts folding through the W-Axis.
- Australian spelling conventions enforced natively (Maths, Colour, Optimise).
- Absolute O(N) volumetric arrays with Lambertian shading.
- HOTFIX: 24-Second Timeline Compressed. Rotational speed explicitly maintained via Pi/2 scaling.
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
DURATION = 24.0  # RE-COMPRESSED TIMELINE
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_410_polytope"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG            = '#FFFFFF'
C_TEXT          = '#111115'
C_EDGE          = '#111115'
C_NODE          = '#1E293B'  # Carbon Slate (Base Vertex)
C_STEEL         = '#94A3B8'  # Topological Struts
C_HIGHLIGHT     = '#DE008A'  # Deep Magenta (The Isolated 3-Face)
C_GUI           = '#64748B'

LIGHT_DIR = np.array([-0.5, 0.8, -0.4])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

# ------------------------------------------------------------------
# O(1) 4D TESSERACT MATRIX COMPILATION
# ------------------------------------------------------------------
VERTS_4D = []
for x in [-1, 1]:
    for y in [-1, 1]:
        for z in [-1, 1]:
            for w in [-1, 1]:
                VERTS_4D.append(np.array([x, y, z, w], dtype=float))
VERTS_4D = np.array(VERTS_4D)

EDGES_4D = []
for i in range(16):
    for j in range(i + 1, 16):
        diff = np.abs(VERTS_4D[i] - VERTS_4D[j])
        if np.sum(diff) == 2.0:  
            EDGES_4D.append((i, j))

# SELECT THE ISOLATED 3-FACE
CELL_VERTS = [i for i, v in enumerate(VERTS_4D) if v[3] == 1.0]
CELL_EDGES = [(i, j) for (i, j) in EDGES_4D if (i in CELL_VERTS and j in CELL_VERTS)]

print(f"PHASE 1: 4D TENSOR COMPILED [16 VERTICES, 32 1-FACES]")
print(f"PHASE 2: COMPRESSED PARITY MODE ENGAGED [DURATION: {DURATION}s]")

# ------------------------------------------------------------------
# MATRIX OPERATIONS
# ------------------------------------------------------------------
def rx(deg):
    rad = np.radians(deg); c, s = np.cos(rad), np.sin(rad)
    return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def ry(rad):
    c, s = np.cos(rad), np.sin(rad)
    return np.array([[c,0,s],[0,1,0],[-s,0,c]])

def ease_in_out(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)

def lerp_colour(c1_hex, c2_hex, t):
    t = np.clip(t, 0.0, 1.0)
    c1 = np.array(mcolors.to_rgb(c1_hex))
    c2 = np.array(mcolors.to_rgb(c2_hex))
    return c1 * (1.0 - t) + c2 * t

def rotate_4d(v, theta_xw, theta_yz):
    x, y, z, w = v
    cx, sx = np.cos(theta_xw), np.sin(theta_xw)
    x_new = x * cx - w * sx
    w_new = x * sx + w * cx
    cy, sy = np.cos(theta_yz), np.sin(theta_yz)
    y_new = y * cy - z * sy
    z_new = y * sy + z * cy
    return np.array([x_new, y_new, z_new, w_new])

def project_4d_to_3d(v4):
    d = 3.5  
    w_factor = d / (d - v4[3])
    return np.array([v4[0] * w_factor, v4[1] * w_factor, v4[2] * w_factor]) * 160.0

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
    # MAINTAIN GLACIAL STUDY MODE PARALLAX: 0.5 degrees per second lock.
    cam_angle = t_sec * 0.5 - 45.0
    M_cam = rx(-15.0) @ ry(cam_angle)
    # Monumental framing hold
    cam_dist = 1100.0 
    
    # 2. TIMELINE MATHEMATICS (Kinematic Proportionality Maintained)
    T_HL_START  = 2.0
    T_HL_END    = 4.0
    T_ROT_START = 6.0
    T_ROT_END   = 20.0  # Exactly 14.0 seconds for the structural inversion
    
    theta_xw = 0.0
    theta_yz = 0.0
    hl_prog = 0.0
    
    if t_sec > T_ROT_START:
        rp = np.clip((t_sec - T_ROT_START) / (T_ROT_END - T_ROT_START), 0.0, 1.0)
        # Mathematical Proportionality: Half the time (14s), half the angle (Pi/2) = IDENTICAL SPEED.
        theta_xw = ease_in_out(rp) * (np.pi / 2.0) 
        theta_yz = ease_in_out(rp) * (np.pi / 8.0)
            
    if t_sec > T_HL_START:
        hl_prog = ease_in_out((t_sec - T_HL_START) / (T_HL_END - T_HL_START))

    # Evaluate 3D positions of all 16 vertices
    nodes_3d = []
    for i in range(16):
        v4_rot = rotate_4d(VERTS_4D[i], theta_xw, theta_yz)
        nodes_3d.append(project_4d_to_3d(v4_rot))

    faces_collected = []
    face_colors = []
    centroids_z = []
    
    # 3. O(N) GEOMETRY COMPILER (Edges)
    for (i, j) in EDGES_4D:
        p1 = nodes_3d[i]
        p2 = nodes_3d[j]
        
        is_highlight_strut = (i in CELL_VERTS and j in CELL_VERTS)
        
        t_strut = 3.5
        s_col = np.array(mcolors.to_rgb(C_STEEL))
        
        if is_highlight_strut:
            t_strut = 3.5 + (4.0 * hl_prog)
            s_col = lerp_colour(C_STEEL, C_HIGHLIGHT, hl_prog)
            
        strut_faces = generate_strut(p1, p2, t_strut)
        for face in strut_faces:
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

    # 4. O(N) GEOMETRY COMPILER (Vertices)
    for i in range(16):
        p_c = nodes_3d[i]
        is_highlight_vert = (i in CELL_VERTS)
        
        v_size = 14.0
        n_col = np.array(mcolors.to_rgb(C_NODE))
        
        if is_highlight_vert:
            v_size = 14.0 + (8.0 * hl_prog)
            n_col = lerp_colour(C_NODE, C_HIGHLIGHT, hl_prog)
            
        cube_faces = generate_cube(p_c, v_size)
        
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
            centroids_z.append(np.mean(v_cam[:, 2]) - 5.0) # Bias nodes slightly forward

    # 5. Z-SORT & RENDER O(N) COLLECTION
    sort_idx = np.argsort(centroids_z)[::-1] 
    sorted_faces = [faces_collected[i] for i in sort_idx]
    sorted_fcs = [face_colors[i] for i in sort_idx]
    
    if sorted_faces:
        ax.add_collection(PolyCollection(sorted_faces, facecolors=sorted_fcs, edgecolors='#111115', linewidths=0.4, joinstyle='miter'))

    # 6. HIGH-DENSITY HUD & TELEMETRY
    ax.add_patch(Rectangle((-540, 780), 1080, 180, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [780, 780], color=C_TEXT, lw=3, zorder=81)
    ax.text(-500, 880, "LG-410d :: POLYTOPE TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 830, "[SFI-1.00] GLACIAL 4-DIMENSIONAL KINEMATICS", color=C_HIGHLIGHT, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    prog = 0.0
    if t_sec < T_HL_END:
        state_msg = "PHASE 1: THE V-STATE TESSERACT (Q4)"
        state_col = C_TEXT
        active_op = "3-FACE HIGHLIGHT: ISOLATING A SINGLE BOUNDING CUBE."
        prog = (t_sec) / T_HL_END
    elif t_sec < T_ROT_END:
        state_msg = "PHASE 2: THE 4-DIMENSIONAL TENSOR (90° FOLD)"
        state_col = C_HIGHLIGHT
        active_op = "SWAPPING THE MATRIX: SLOW TOPOLOGICAL DISTORTION TRACE."
        prog = (t_sec - T_ROT_START) / (T_ROT_END - T_ROT_START)
    else:
        state_msg = "PHASE 3: DIMENSIONAL CONTINUITY CONSERVED"
        state_col = C_HIGHLIGHT
        active_op = "ABSOLUTE RESOLUTION: TOPOLOGY HELD WITHOUT FRACTURE."
        prog = 1.0

    ax.text(-500, -780, f"PROTOCOL STATE : {state_msg}", color=state_col, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"DIAGNOSTIC     : {active_op}", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"AXIOMATIC TRUTH: A 4D ROTATION DOES NOT SPIN. IT MATHEMATICALLY FOLDS SPACE INWARD.", color=C_TEXT, fontsize=11, fontname='monospace', zorder=82)

    ax.add_patch(Rectangle((-500, -920), 1000, 8, facecolor=C_GUI, zorder=82))
    ax.add_patch(Rectangle((-500, -920), 1000 * prog, 8, facecolor=state_col, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f_idx:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f_idx

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-410d: COMPRESSED PARITY TENSOR ENGAGED [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            pass
    print("Compilation Complete. Matrix resolved via absolute glacial kinematics.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
