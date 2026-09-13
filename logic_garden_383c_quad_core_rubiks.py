"""
PROJECT: Logic Garden 383c (Quad-Core Physical Construct // Rubik's Tensor)
FORMAT: YouTube Shorts (1080x1920)
METADATA: RUBIKS CUBE, MULTI-THREADING, EXACT HARDWARE, PHOTOREALISM
EXECUTION: 24.0s Sequence. True 3D Beveled Geometry. 4x Concurrency.
RULES ENFORCED: 
- 108 Unified Dual-Layer Cubies (Solid Plastic Base + Offset Stickers).
- 4 Isolated Rendering Queues to prevent Z-buffer bleeding across quadrants.
- Lambertian Dynamic Shading over Photorealistic Hex values.
- Flawless Z-Sorting and Backface Culling.
- Australian spelling conventions (Synchronisation).
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
OUT_DIR = "frames_383c_quad_core"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- VISUAL PALETTE (EXACT IMAGE REPLICATION) --------
C_BG        = '#FFFFFF'   # Pure White Daylight Background 
C_TEXT      = '#111115'   # Indestructible Black
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
    # Studio lighting simulation (Light source perfectly locked in camera space)
    light_vec = np.array([0.22, -0.76, -0.61]) 
    intensity = 0.45 + 0.55 * np.clip(np.dot(n_cam, light_vec), 0.0, 1.0)
    
    # Plastic base gets a slight gloss multiplier for material separation
    if hex_color == C_CORE:
        intensity = 0.35 + 0.65 * np.clip(np.dot(n_cam, light_vec), 0.0, 1.0)
        
    r, g, b = mcol.to_rgb(hex_color)
    return mcol.to_hex((np.clip(r*intensity,0,1), np.clip(g*intensity,0,1), np.clip(b*intensity,0,1)))

# ------------------------------------------------------------------
# TRUE 3D DUAL-LAYER GEOMETRY (THE PLASTIC & VINYL MESH)
# ------------------------------------------------------------------
def build_face(nx, ny, nz, dist, size):
    sz = size / 2.0
    if nx != 0: return [[nx*dist, -sz, -sz], [nx*dist, -sz, sz], [nx*dist, sz, sz], [nx*dist, sz, -sz]]
    if ny != 0: return [[-sz, ny*dist, -sz], [sz, ny*dist, -sz], [sz, ny*dist, sz], [-sz, ny*dist, sz]]
    if nz != 0: return [[-sz, -sz, nz*dist], [sz, -sz, nz*dist], [sz, sz, nz*dist], [-sz, sz, nz*dist]]

face_dirs = [
    (0,1,0, C_U), (0,-1,0, C_D), 
    (0,0,1, C_F), (0,0,-1, C_B), 
    (1,0,0, C_R), (-1,0,0, C_L)
]

def create_cube_data(solver_seq):
    """Instantiates a sovereign set of 27 blocks, scrambles it backward via the provided sequence."""
    blocks = []
    for cy in [-100, 0, 100]:
        for cx in [-100, 0, 100]:
            for cz in [-100, 0, 100]:
                b = {'logical_pos': np.array([cx, cy, cz]), 'polys': []}
                center = np.array([cx, cy, cz])
                
                for nx, ny, nz, color in face_dirs:
                    # THE BLACK PLASTIC BASE BOX
                    p_verts = np.array(build_face(nx, ny, nz, 48.0, 96.0)) + center
                    b['polys'].append({'v': p_verts.tolist(), 'n': np.array([nx, ny, nz]), 'c': C_CORE})
                    
                    # THE COLORED VINYL STICKER 
                    is_outer = (nx*cx > 0 and abs(cx)==100) or (ny*cy > 0 and abs(cy)==100) or (nz*cz > 0 and abs(cz)==100)
                    if is_outer:
                        s_verts = np.array(build_face(nx, ny, nz, 49.0, 84.0)) + center
                        b['polys'].append({'v': s_verts.tolist(), 'n': np.array([nx, ny, nz]), 'c': color})
                blocks.append(b)

    # Scramble the cube algebraically by applying the exact mathematical inverse of its intended solution
    for move in reversed(solver_seq):
        ax_i, sl_i, dir_i = move
        R_inv = get_R(ax_i, -dir_i * (np.pi / 2.0))
        for b in blocks:
            if abs(b['logical_pos'][ax_i] - sl_i) < 1:
                for poly in b['polys']:
                    poly['v'] = [rotate_pt(pt, R_inv).tolist() for pt in poly['v']]
                    poly['n'] = rotate_pt(poly['n'], R_inv)
                b['logical_pos'] = np.round(rotate_pt(b['logical_pos'], R_inv)).astype(int)
    
    return blocks

# ------------------------------------------------------------------
# 4 ASYMMETRIC SCRAMBLE / SOLVER MATRICES
# ------------------------------------------------------------------
SEQ_1 = [(0, 100, 1), (1, -100, -1), (2, 100, 1), (0, -100, 1), (1, 100, -1), (2, -100, -1), (0, 0, 1), (1, 0, -1), (2, 0, 1), (0, 100, -1), (1, -100, 1), (2, 100, -1)]
SEQ_2 = [(1, 100, 1), (2, 100, -1), (0, -100, -1), (1, -100, 1), (2, 0, 1), (0, 100, 1), (1, 0, -1), (2, -100, -1), (0, 0, 1), (1, 100, -1), (2, 100, 1), (0, -100, 1)]
SEQ_3 = [(2, -100, 1), (0, 100, 1), (1, -100, -1), (2, 100, -1), (0, 0, -1), (1, 100, 1), (2, 0, 1), (0, -100, 1), (1, 0, -1), (2, -100, -1), (0, 100, -1), (1, -100, 1)]
SEQ_4 = [(0, -100, -1), (1, 0, 1), (2, -100, 1), (0, 100, -1), (1, 100, 1), (2, 100, -1), (0, 0, 1), (1, -100, -1), (2, 0, -1), (0, -100, 1), (1, 100, -1), (2, -100, 1)]

# Instantiate the Master Thread Allocation
CUBES = []
def init_data():
    global CUBES
    # Allocating the 4 Alternate-Universe quadrant projections
    CUBES.append({'blocks': create_cube_data(SEQ_1), 'seq': SEQ_1, 'ox': -260, 'oy': 350})
    CUBES.append({'blocks': create_cube_data(SEQ_2), 'seq': SEQ_2, 'ox':  260, 'oy': 350})
    CUBES.append({'blocks': create_cube_data(SEQ_3), 'seq': SEQ_3, 'ox': -260, 'oy': -210})
    CUBES.append({'blocks': create_cube_data(SEQ_4), 'seq': SEQ_4, 'ox':  260, 'oy': -210})

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

    # 1. OPTICS & RIGID CAMERA (Uniform orbit for all 4 realities)
    pitch = np.radians(-28) 
    yaw = np.radians(-42) + (t * 0.12)
    sys_rot = get_R(0, pitch) @ get_R(1, yaw)
    
    # Pulled back aggressively to encompass the entire 2x2 grid without overlap
    cam_dist = 7500.0  
    focal = 4500.0 

    # 2. CHRONOLOGICAL TENSOR
    T_START = 3.0
    MOVE_DR = 1.2
    
    m_idx = -1
    m_prog = 0.0
    if t > T_START:
        t_act = t - T_START
        m_idx = int(t_act // MOVE_DR)
        m_prog = ease_in_out((t_act % MOVE_DR) / MOVE_DR)
        
    if m_idx >= 12:
        m_idx = 12
        m_prog = 0.0

    # 3. KINEMATIC DISPATCH OVER 4 INDEPENDENT MATRICES
    for cube in CUBES:
        render_queue = []
        seq = cube['seq']
        
        for b in cube['blocks']:
            l_pos = b['logical_pos'].copy()
            R_total = np.eye(3)
            
            # Snap previous layer positions for this specific cube
            for i in range(min(m_idx, 12)):
                ax_i, sl_i, dir_i = seq[i]
                if abs(l_pos[ax_i] - sl_i) < 1:
                    R_step = get_R(ax_i, dir_i * (np.pi / 2.0))
                    R_total = np.dot(R_step, R_total)
                    l_pos = np.round(rotate_pt(l_pos, R_step)).astype(int)
                    
            # Active continuous rotation
            if 0 <= m_idx < 12:
                ax_i, sl_i, dir_i = seq[m_idx]
                if abs(l_pos[ax_i] - sl_i) < 1:
                    R_arc = get_R(ax_i, dir_i * (np.pi / 2.0) * m_prog)
                    R_total = np.dot(R_arc, R_total)

            for poly in b['polys']:
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
                            # 2D QUADRANT OFFSET APPLIED AT TERMINAL STAGE
                            pts_2d.append([p_c[0] * focal / z + cube['ox'], p_c[1] * focal / z + cube['oy']])
                            zs.append(z)
                    
                    if len(pts_2d) == 4:
                        render_queue.append({
                            'z': np.mean(zs),
                            'poly': pts_2d,
                            'n_cam': n_cam,
                            'c': poly['c']
                        })

        # O(1) Mathematically Faultless Depth Sort (Isolated per quadrant!)
        render_queue.sort(key=lambda x: x['z'], reverse=True)

        # Draw the local quadrant matrix
        for obj in render_queue:
            exact_color = shade_color(obj['c'], obj['n_cam'])
            pl = patches.Polygon(obj['poly'], facecolor=exact_color, edgecolor=exact_color, lw=1.0, joinstyle='round')
            ax.add_patch(pl)

    # ====================================================
    # 5. JARGON-FREE REALISTIC UI
    # ====================================================
    # Top Header
    ax.add_patch(patches.Rectangle((-540, 780), 1080, 180, facecolor=C_BG, zorder=80))
    ax.plot([-460, 460], [780, 780], color=C_HUD_LINE, lw=2, zorder=81)
    ax.text(-460, 860, "LG-383c :: QUAD-CORE RUBIK'S TENSOR", color=C_TEXT, fontsize=22, fontname='monospace', weight='bold', zorder=82)
    ax.text(-460, 820, "ASYMMETRIC MULTI-THREADED KINEMATICS", color='#555555', fontsize=14, fontname='monospace', zorder=82)

    # Bottom Footer
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 260, facecolor=C_BG, zorder=80))
    ax.plot([-460, 460], [-700, -700], color=C_HUD_LINE, lw=2, zorder=81)

    solved_moves = min(m_idx, 12) if m_idx >= 0 else 0
    total_moves = 12
    
    if phase_ratio < (T_START / DURATION):
        s1, c1 = "4X SCRAMBLED // ASYMMETRIC", C_F
        s2 = "0 / 12 PER CORE"
        s3 = "AWAITING SYNCHRONISATION"
    elif m_idx < total_moves:
        s1, c1 = "CONCURRENT RESOLUTION...", C_R
        s2 = f"{solved_moves+1} / 12 PER CORE"
        s3 = "ALIGNING MULTI-DOMAIN LAYERS"
    else:
        s1, c1 = "ABSOLUTE RESOLUTION ACHIEVED", C_U
        s2 = "12 / 12 PER CORE"
        s3 = "O(1) HARDWARE PARITY SECURED"

    ax.text(-460, -760, "QUAD-CORE SYSTEM :", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, s1, color=c1, fontsize=16, fontname='monospace', weight='bold', zorder=82)

    ax.text(-460, -810, "TENSOR OPERATIONS:", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -810, s2, color=C_TEXT, fontsize=16, fontname='monospace', zorder=82)

    ax.text(-460, -860, "INTEGRITY        :", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -860, s3, color='#555555', fontsize=16, fontname='monospace', zorder=82)

    # Sleek Progress Bar
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
    print(f"LG-383c: QUAD-CORE RUBIK'S METRICS [CORES: {cpu_cores}]")
    init_data() # Instantiate data prior to multiprocessing fork for state access
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1): pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
