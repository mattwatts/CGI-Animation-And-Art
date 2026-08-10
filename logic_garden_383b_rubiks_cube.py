"""
PROJECT: Logic Garden 383b (Exact Physical Construct // Alternate Kinematics)
FORMAT: YouTube Shorts (1080x1920)
METADATA: RUBIKS CUBE, EXACT HARDWARE, PHOTOREALISM, PERMUTATION
EXECUTION: 24.0s Sequence. True 3D Beveled Geometry. Dynamic Lighting.
RULES ENFORCED:
- 27 Unified Dual-Layer Cubies (Solid Plastic Base + Offset Stickers).
- Lambertian Dynamic Shading over Photorealistic Hex values.
- Flawless Z-Sorting and Backface Culling.
- Alternate Thermodynamic Starting State (New Solver Sequence).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcol
import multiprocessing as mp
import os
import gc

# ======== SEQUENCE PARAMETERS ========
DURATION = 24.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_383b_rubiks_cube"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- VISUAL PALETTE (EXACT IMAGE REPLICATION) --------
C_BG        = '#FFFFFF'   # Pure White Background
C_TEXT      = '#111115'
C_CORE      = '#161618'   # Dense Black Plastic Base
C_HUD_LINE  = '#E5E7EB'   # Clean separator for UI

# Exact Photographic Palette Mapping
C_U = '#F4CC2A' # Mustard Yellow (Top)
C_F = '#D83232' # Oxide Red (Front-Left)
C_R = '#1A7B39' # Forest Green (Front-Right)
C_D = '#FFFFFF' # White (Hidden Bottom)
C_B = '#D95F22' # Orange (Hidden Back-Right)
C_L = '#1A5B9C' # Blue (Hidden Back-Left)

# ------------------------------------------------------------------
# 3D ROTATION & LIGHTING ENGINE
# ------------------------------------------------------------------
def get_R(axis, angle):
    c, s = np.cos(angle), np.sin(angle)
    if axis == 0: return np.array([[1,0,0],[0,c,-s],[0,s,c]])
    if axis == 1: return np.array([[c,0,s],[0,1,0],[-s,0,c]])
    if axis == 2: return np.array([[c,-s,0],[s,c,0],[0,0,1]])

def rotate_pt(pt, R):
    return np.dot(R, pt)

def ease_in_out(t):
    t = np.clip(t, 0.0, 1.0)
    return 4 * t**3 if t < 0.5 else 1 - (-2 * t + 2)**3 / 2

def shade_color(hex_color, n_cam):
    # Studio lighting simulation (Light source in camera space)
    light_vec = np.array([0.22, -0.76, -0.61])
    intensity = 0.45 + 0.55 * np.clip(np.dot(n_cam, light_vec), 0.0, 1.0)

    # Plastic base gets a slight gloss multiplier
    if hex_color == C_CORE:
        intensity = 0.35 + 0.65 * np.clip(np.dot(n_cam, light_vec), 0.0, 1.0)

    r, g, b = mcol.to_rgb(hex_color)
    return mcol.to_hex((np.clip(r*intensity,0,1), np.clip(g*intensity,0,1), np.clip(b*intensity,0,1)))

# ------------------------------------------------------------------
# TRUE 3D DUAL-LAYER GEOMETRY (THE FIX)
# ------------------------------------------------------------------
SPACING = 100.0

def build_face(nx, ny, nz, dist, size):
    # Builds absolute 3D corner vertices for a specific face orientation
    sz = size / 2.0
    if nx != 0: return [[nx*dist, -sz, -sz], [nx*dist, -sz, sz], [nx*dist, sz, sz], [nx*dist, sz, -sz]]
    if ny != 0: return [[-sz, ny*dist, -sz], [sz, ny*dist, -sz], [sz, ny*dist, sz], [-sz, ny*dist, sz]]
    if nz != 0: return [[-sz, -sz, nz*dist], [sz, -sz, nz*dist], [sz, sz, nz*dist], [-sz, sz, nz*dist]]

face_dirs = [
    (0,1,0, C_U), (0,-1,0, C_D),
    (0,0,1, C_F), (0,0,-1, C_B),
    (1,0,0, C_R), (-1,0,0, C_L)
]

blocks = []
for cy in [-100, 0, 100]:
    for cx in [-100, 0, 100]:
        for cz in [-100, 0, 100]:
            b = {'logical_pos': np.array([cx, cy, cz]), 'polys': []}
            center = np.array([cx, cy, cz])

            for nx, ny, nz, color in face_dirs:
                # 1. THE BLACK PLASTIC BASE BOX
                # Drawn 48.0 from center, size 96.0 -> 4.0 unit mechanical clearance
                p_verts = np.array(build_face(nx, ny, nz, 48.0, 96.0)) + center
                b['polys'].append({
                    'v': p_verts.tolist(),
                    'n': np.array([nx, ny, nz]),
                    'c': C_CORE
                })

                # 2. THE COLORED VINYL STICKER
                is_outer = (nx*cx > 0 and abs(cx)==100) or (ny*cy > 0 and abs(cy)==100) or (nz*cz > 0 and abs(cz)==100)
                if is_outer:
                    s_verts = np.array(build_face(nx, ny, nz, 49.0, 84.0)) + center
                    b['polys'].append({
                        'v': s_verts.tolist(),
                        'n': np.array([nx, ny, nz]),
                        'c': color
                    })
            blocks.append(b)

# ------------------------------------------------------------------
# SCRAMBLE & SOLVE KINEMATICS (ALTERNATE SEED)
# ------------------------------------------------------------------
# Sequence mapping: Axis (0=X, 1=Y, 2=Z), Slice Index, Direction
SOLVER_SEQUENCE = [
    (1,  100,  1),  # U
    (0,  100, -1),  # R'
    (2,  100,  1),  # F
    (1,  100, -1),  # U'
    (2, -100, -1),  # B'
    (0, -100,  1),  # L
    (2, -100,  1),  # B
    (0, -100, -1),  # L'
    (1, -100,  1),  # D
    (2,  100, -1),  # F'
    (1, -100, -1),  # D'
    (0,  100,  1)   # R
]

# Apply the mathematical inverse to scramble the cube flawlessly at T=0
for move in reversed(SOLVER_SEQUENCE):
    ax_i, sl_i, dir_i = move
    R_inv = get_R(ax_i, -dir_i * (np.pi / 2.0))
    for b in blocks:
        if abs(b['logical_pos'][ax_i] - sl_i) < 1:
            for poly in b['polys']:
                poly['v'] = [rotate_pt(pt, R_inv).tolist() for pt in poly['v']]
                poly['n'] = rotate_pt(poly['n'], R_inv)
            b['logical_pos'] = np.round(rotate_pt(b['logical_pos'], R_inv)).astype(int)

# ------------------------------------------------------------------
# RENDER ENGINE
# ------------------------------------------------------------------
def render_frame(packet):
    f, phase_ratio = packet
    t = phase_ratio * DURATION

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)

    # 1. CAMERA OPTICS (Mimicking exact isometric photo setup)
    pitch = np.radians(-28)
    yaw = np.radians(-42) + (t * 0.12)
    sys_rot = get_R(0, pitch) @ get_R(1, yaw)

    cam_dist = 2200.0
    focal = 3500.0

    # 2. SOLVING TRACKER
    T_START = 3.0
    MOVE_DR = 1.2

    m_idx = -1
    m_prog = 0.0
    if t > T_START:
        t_act = t - T_START
        m_idx = int(t_act // MOVE_DR)
        m_prog = ease_in_out((t_act % MOVE_DR) / MOVE_DR)

    if m_idx >= len(SOLVER_SEQUENCE):
        m_idx = len(SOLVER_SEQUENCE)
        m_prog = 0.0

    render_queue = []

    # 3. KINEMATIC DISPATCH
    for b in blocks:
        l_pos = b['logical_pos'].copy()
        R_total = np.eye(3)

        # Apply snapped moves
        for i in range(min(m_idx, len(SOLVER_SEQUENCE))):
            ax_i, sl_i, dir_i = SOLVER_SEQUENCE[i]
            if abs(l_pos[ax_i] - sl_i) < 1:
                R_step = get_R(ax_i, dir_i * (np.pi / 2.0))
                R_total = np.dot(R_step, R_total)
                l_pos = np.round(rotate_pt(l_pos, R_step)).astype(int)

        # Apply active rotational arc
        if 0 <= m_idx < len(SOLVER_SEQUENCE):
            ax_i, sl_i, dir_i = SOLVER_SEQUENCE[m_idx]
            if abs(l_pos[ax_i] - sl_i) < 1:
                R_arc = get_R(ax_i, dir_i * (np.pi / 2.0) * m_prog)
                R_total = np.dot(R_arc, R_total)

        for poly in b['polys']:
            # Exact 3D Spatial Calculation
            n_world = rotate_pt(poly['n'], R_total)
            n_cam = rotate_pt(n_world, sys_rot)

            # ABSOLUTE BACKFACE CULLING
            if n_cam[2] < 0.01:
                pts_2d = []
                zs = []
                for pt in poly['v']:
                    p_w = rotate_pt(pt, R_total)
                    p_c = rotate_pt(p_w, sys_rot)
                    z = p_c[2] + cam_dist
                    if z > 10:
                        pts_2d.append([p_c[0] * focal / z, p_c[1] * focal / z + 60])
                        zs.append(z)

                if len(pts_2d) == 4:
                    render_queue.append({
                        'z': np.mean(zs),
                        'poly': pts_2d,
                        'n_cam': n_cam,
                        'c': poly['c']
                    })

    # O(1) Mathematically Faultless Depth Sort
    render_queue.sort(key=lambda x: x['z'], reverse=True)

    # 4. TACTILE DRAW
    for obj in render_queue:
        exact_color = shade_color(obj['c'], obj['n_cam'])
        pl = patches.Polygon(obj['poly'], facecolor=exact_color, edgecolor=exact_color, lw=1.0, joinstyle='round')
        ax.add_patch(pl)

    # ====================================================
    # 5. JARGON-FREE REALISTIC UI
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 780), 1080, 180, facecolor=C_BG, zorder=80))
    ax.plot([-460, 460], [780, 780], color=C_HUD_LINE, lw=2, zorder=81)
    ax.text(-460, 860, "LG-383b :: RUBIK'S CUBE RESOLUTION (SEQ II)", color=C_TEXT, fontsize=22, fontname='monospace', weight='bold', zorder=82)
    ax.text(-460, 820, "EXACT PHYSICAL REPLICATION", color='#555555', fontsize=14, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 260, facecolor=C_BG, zorder=80))
    ax.plot([-460, 460], [-700, -700], color=C_HUD_LINE, lw=2, zorder=81)

    solved_moves = min(m_idx, len(SOLVER_SEQUENCE)) if m_idx >= 0 else 0
    total_moves = len(SOLVER_SEQUENCE)

    if phase_ratio < (T_START / DURATION):
        s1, c1 = "SCRAMBLED", C_F
        s2 = "0 / 12"
        s3 = "AWAITING ALIGNMENT"
    elif m_idx < len(SOLVER_SEQUENCE):
        s1, c1 = "SOLVING...", C_R
        s2 = f"{solved_moves+1} / 12"
        s3 = "ALIGNING LAYERS"
    else:
        s1, c1 = "SOLVED", C_U
        s2 = "12 / 12"
        s3 = "PERFECT ALIGNMENT ACHIEVED"

    ax.text(-460, -760, "SYSTEM STATE   :", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, s1, color=c1, fontsize=16, fontname='monospace', weight='bold', zorder=82)

    ax.text(-460, -810, "MOVES COMPLETE :", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -810, s2, color=C_TEXT, fontsize=16, fontname='monospace', zorder=82)

    ax.text(-460, -860, "INTEGRITY      :", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -860, s3, color='#555555', fontsize=16, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-460, -910), 920, 6, facecolor=C_HUD_LINE, zorder=82))
    total_prog = (solved_moves + (m_prog if m_idx>=0 and m_idx<total_moves else 0.0)) / total_moves
    prog_c = C_F if total_prog < 0.1 else (C_U if total_prog >= 0.99 else C_R)
    ax.add_patch(patches.Rectangle((-460, -910), 920 * total_prog, 6, facecolor=prog_c, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close('all')
    gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES): yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-383b: EXACT RUBIK'S METRICS // SEQ II [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1): pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
