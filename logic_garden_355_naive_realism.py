"""
CODE: logic_garden_355_naive_realism.py
SYSTEM: Python Multicore / Rigid Polygon Topology
SCENE: Logic Garden 355 (Naive Realism // The Macroscopic Illusion)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: QUANTUM PHYSICS, PHILOSOPHY OF SCIENCE, PARTICLE DYNAMICS
HOTFIX: Restored C_TITANIUM to global color palette.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
DURATION = 24.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_355_naive_realism"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- VISUAL PALETTE (HIGH VISIBILITY / DAYLIGHT) --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_TITANIUM  = '#A0A0A5'   # The missing structural gray
C_GRID      = '#E5E7EB'
C_MACRO     = '#9398A1'   # The Smooth Solid Illusion (Polished Titanium)
C_STEEL     = '#5A6270'   # Molecular Bonds
C_NUCLEUS   = '#FFB300'   # Atomic Centers
C_ELECTRON1 = '#00E5FF'   # Point Charge A
C_ELECTRON2 = '#DE008A'   # Point Charge B

# ------------------------------------------------------------------
# GEOMETRY ENGINE: TRUE 3D PERSPECTIVE PROJECTION
# ------------------------------------------------------------------
def rotate_rx(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])

def rotate_ry(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])

def rotate_rz(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

def ease_in_out(t):
    t = np.clip(t, 0.0, 1.0)
    return 4 * t**3 if t < 0.5 else 1 - (-2 * t + 2)**3 / 2

# ------------------------------------------------------------------
# MATRIX GENERATION: MACRO BLOCK TO MICRO CLOUDS
# ------------------------------------------------------------------
# 1. The Macro Faces (A 400x400x400 perfectly smooth cube)
BOX_R = 200.0
MACRO_FACES = np.array([
    [[-BOX_R, -BOX_R,  BOX_R], [ BOX_R, -BOX_R,  BOX_R], [ BOX_R,  BOX_R,  BOX_R], [-BOX_R,  BOX_R,  BOX_R]], # Top
    [[-BOX_R, -BOX_R, -BOX_R], [-BOX_R,  BOX_R, -BOX_R], [ BOX_R,  BOX_R, -BOX_R], [ BOX_R, -BOX_R, -BOX_R]], # Bottom
    [[-BOX_R,  BOX_R, -BOX_R], [-BOX_R,  BOX_R,  BOX_R], [ BOX_R,  BOX_R,  BOX_R], [ BOX_R,  BOX_R, -BOX_R]], # Front
    [[-BOX_R, -BOX_R, -BOX_R], [ BOX_R, -BOX_R, -BOX_R], [ BOX_R, -BOX_R,  BOX_R], [-BOX_R, -BOX_R,  BOX_R]], # Back
    [[-BOX_R, -BOX_R, -BOX_R], [-BOX_R, -BOX_R,  BOX_R], [-BOX_R,  BOX_R,  BOX_R], [-BOX_R,  BOX_R, -BOX_R]], # Left
    [[ BOX_R, -BOX_R, -BOX_R], [ BOX_R,  BOX_R, -BOX_R], [ BOX_R,  BOX_R,  BOX_R], [ BOX_R, -BOX_R,  BOX_R]], # Right
])

# 2. Molecular Lattice (5x5x5 Array)
lattice_nodes = []
pts = [-200, -100, 0, 100, 200]
for x in pts:
    for y in pts:
        for z in pts:
            lattice_nodes.append([x, y, z])
lattice_nodes = np.array(lattice_nodes)
N_NODES = len(lattice_nodes)

# 3. Vibration Profiles & Electrons
np.random.seed(355)
vib_offsets = np.random.uniform(0, 2*np.pi, (N_NODES, 3))
edges = []
for i in range(N_NODES):
    for j in range(i+1, N_NODES):
        if np.linalg.norm(lattice_nodes[i] - lattice_nodes[j]) <= 101.0:
            edges.append((i, j))

N_ELECTRONS_PER_NODE = 25
electrons = []
for i in range(N_NODES):
    for _ in range(N_ELECTRONS_PER_NODE):
        r = np.random.uniform(15, 60)
        theta = np.random.uniform(0, 2*np.pi)
        phi = np.random.uniform(0, np.pi)
        speed = np.random.uniform(2.0, 8.0) * np.random.choice([-1, 1])
        c = C_ELECTRON1 if np.random.rand() > 0.3 else C_ELECTRON2
        electrons.append({'node': i, 'r': r, 'theta': theta, 'phi': phi, 'v': speed, 'c': c})

# Light Source relative shading
LIGHT_DIR = np.array([0.4, 0.8, -0.4])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

def get_shaded_color(hex_color, normal, alpha):
    rgb = np.array(mcolors.to_rgb(hex_color))
    amb = 0.4
    diff = 0.6 * max(0, -np.dot(normal, LIGHT_DIR)) # Neg dot b/c looking at front faces
    final_rgb = np.clip(rgb * (amb + diff), 0, 1)
    return mcolors.to_rgba(final_rgb, alpha)

def render_frame(packet):
    f, phase_ratio = packet
    t = phase_ratio * DURATION

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)
    ax.autoscale(False)

    # 1. TIMELINE & FADE MAPPING
    # --------------------------
    alpha_macro   = 1.0 - ease_in_out(np.clip((t - 5.0) / 4.0, 0.0, 1.0))
    alpha_lattice = ease_in_out(np.clip((t - 4.0) / 4.0, 0.0, 1.0))
    alpha_bonds   = alpha_lattice * (1.0 - ease_in_out(np.clip((t - 11.0) / 3.0, 0.0, 1.0)))
    alpha_quantum = ease_in_out(np.clip((t - 12.0) / 4.0, 0.0, 1.0))
    
    vib_amplitude = ease_in_out(np.clip((t - 10.0) / 8.0, 0.0, 1.0)) * 60.0 # Atoms scatter out of grid
    plunge_prg    = ease_in_out(np.clip((t - 6.0) / 14.0, 0.0, 1.0))
    
    # 2. CAMERA AND PROJECTION LOGIC
    # ------------------------------
    cam_dist = 1100.0 * (1.0 - plunge_prg) + -20.0 * plunge_prg  # Fly deep into the matrix
    focal_length = 1000.0
    sys_rotation = rotate_rx(np.radians(-20) + t * 0.1) @ rotate_ry(t * 0.3)
    
    render_queue = []

    def get_projection(pt_3d):
        """Translates a 3D point relative to the plunging camera"""
        z_cam = pt_3d[2] + cam_dist
        if z_cam < 10: return None # Clipped by camera plane (we flew past it)
        sx = (pt_3d[0] * focal_length) / z_cam
        sy = (pt_3d[1] * focal_length) / z_cam
        return (sx, sy, z_cam)

    # 3. THE MACROSCOPIC BLOCK (Rendering)
    # ------------------------------------
    if alpha_macro > 0.01:
        for face in MACRO_FACES:
            proj = np.dot(face, sys_rotation.T)
            z_cams = proj[:, 2] + cam_dist
            if np.any(z_cams < 10): continue # Skip if punching through
                
            v1, v2, v3 = proj[0], proj[1], proj[2]
            nrm = np.cross(v2 - v1, v3 - v1)
            mag = np.linalg.norm(nrm)
            if mag > 0: nrm /= mag
            
            # Backface cull geometric solid
            if nrm[2] > 0: continue 

            screen_pts = []
            valid = True
            for pt in proj:
                res = get_projection(pt)
                if not res:
                    valid = False
                    break
                screen_pts.append([res[0], res[1]])
                
            if valid:
                z_depth = np.mean(z_cams)
                c_shade = get_shaded_color(C_MACRO, nrm, alpha_macro)
                render_queue.append({'type': 'poly', 'd': z_depth, 'pts': np.array(screen_pts), 'c': c_shade})

    # 4. KINEMATIC VIBRATION & LATTICE
    # --------------------------------
    # Apply thermal vibration offsets driven by timeline
    current_nodes = []
    screen_nodes = []
    
    for i in range(N_NODES):
        # Sine-wave thermal jitter
        jitter = vib_amplitude * np.sin(t * 12.0 + vib_offsets[i])
        dynamic_pos = lattice_nodes[i] + jitter
        rot_pos = np.dot(dynamic_pos, sys_rotation.T)
        
        current_nodes.append(rot_pos)
        res = get_projection(rot_pos)
        screen_nodes.append(res)
        
        # Append Node (Nucleus)
        if res and alpha_lattice > 0.01:
            size = (1800.0 / res[2]) * alpha_lattice # Perspective scaling for particle dot
            render_queue.append({
                'type': 'pt', 'd': res[2], 'x': res[0], 'y': res[1], 
                'c': mcolors.to_rgba(C_NUCLEUS, np.clip(alpha_lattice, 0, 1)), 's': size
            })

    # Structural Bonds (Edges)
    if alpha_bonds > 0.01:
        for (i, j) in edges:
            ni, nj = screen_nodes[i], screen_nodes[j]
            if ni and nj:
                d_line = (ni[2] + nj[2]) / 2.0
                render_queue.append({
                    'type': 'line', 'd': d_line, 'x': [ni[0], nj[0]], 'y': [ni[1], nj[1]], 
                    'c': mcolors.to_rgba(C_STEEL, np.clip(alpha_bonds, 0, 1)), 'lw': max(0.5, 800.0 / d_line)
                })

    # 5. THE QUANTUM ELECTRON CLOUD
    # -----------------------------
    if alpha_quantum > 0.01:
        a_q_safe = np.clip(alpha_quantum, 0, 1)
        for e in electrons:
            node_idx = e['node']
            n_pos = current_nodes[node_idx]
            
            # Electron position relative to its vibrating nucleus
            e_x = e['r'] * np.cos(e['theta'] + t * e['v']) * np.sin(e['phi'])
            e_y = e['r'] * np.sin(e['theta'] + t * e['v']) * np.sin(e['phi'])
            e_z = e['r'] * np.cos(e['phi'])
            
            # The electron orbital vector must ALSO be rotated to match the scene coordinate frame
            e_pos_rotated = np.dot([e_x, e_y, e_z], sys_rotation.T)
            
            final_pos = n_pos + e_pos_rotated
            res = get_projection(final_pos)
            if res:
                # Closer to camera = much larger soft dot
                e_size = (1200.0 / res[2]) * alpha_quantum 
                render_queue.append({
                    'type': 'pt', 'd': res[2], 'x': res[0], 'y': res[1], 
                    'c': mcolors.to_rgba(e['c'], a_q_safe), 's': e_size
                })

    # 6. ABSOLUTE Z-SORT RENDERING DISPATCH
    # -------------------------------------
    render_queue.sort(key=lambda item: item['d'], reverse=True) 

    for item in render_queue:
        if item['type'] == 'poly':
            ax.add_patch(patches.Polygon(item['pts'], facecolor=item['c'], edgecolor='none', zorder=50))
        elif item['type'] == 'line':
            ax.plot(item['x'], item['y'], color=item['c'], lw=item['lw'], zorder=50)
        elif item['type'] == 'pt':
            ax.scatter(item['x'], item['y'], color=item['c'], s=item['s'], edgecolors='none', zorder=50)

    # ====================================================
    # 7. VISUAL TELEMETRY AND INFORMATION OVERLAYS
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_BG, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=2, zorder=81)

    ax.text(-500, 890, "LG-355 :: SENSORY ABSTRACTION", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "NAIVE REALISM // THE BIOLOGICAL ILLUSION", color='#555555', fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_BG, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=2, zorder=81)

    # Dynamic Descriptive Text
    if t < 6.0:
        s1, c1 = "MACROSCOPIC // 1:1 RESOLUTION", C_TEXT
        s2, c2 = "BIOLOGICAL SMOOTHING ACTIVE", C_TITANIUM
        t_state = "PERCEPTION: 100% SOLID STATE MATTER"
    elif t < 12.0:
        s1, c1 = "MOLECULAR // 1:1,000,000 RESOLUTION", C_STEEL
        s2, c2 = "SENSORY ABSTRACTION BYPASSED", C_TEXT
        t_state = "REVEALING UNDERLYING CRYSTALLINE LATTICE"
    elif t < 18.0:
        s1, c1 = "SUB-ATOMIC // DEEP PENETRATION", C_NUCLEUS
        s2, c2 = "THERMAL VIBRATIONS DESTABILIZING GRID", C_TEXT
        t_state = "RIGID STRUCTURE RUPTURED BY KINETIC SEPARATION"
    else:
        s1, c1 = "QUANTUM // 1:1,000,000,000 RESOLUTION", C_ELECTRON1
        s2, c2 = "MACROSCOPIC ILLUSION SHATTERED", C_TEXT
        t_state = "REALITY: 99.999% VACUUM STATE / VIBRATING ENERGY"

    ax.text(-500, -760, "SYS_01 [PERCEPTUAL SCALE] :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(30, -760, s1, color=c1, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [COGNITIVE LOAD]   :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(30, -800, s2, color=c2, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "STRUCTURAL AUDIT          :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(30, -840, t_state, color=C_TEXT, fontsize=14, fontname='monospace', zorder=82)

    # Seamless Transition Progress Bar
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 4, facecolor='#E5E7EB', zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 4, facecolor=C_TEXT, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0)
    plt.close('all')
    gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-355: NAIVE REALISM [CORES: {cpu_cores}] [RENDERING EXPONENTIAL PLUNGE]")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
