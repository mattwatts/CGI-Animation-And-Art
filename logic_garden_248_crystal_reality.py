"""
SOVEREIGN CODE: logic_garden_248_crystal_reality.py
SYSTEM: Python Multicore / O(1) Complex Polyhedron Generation
SCENE: Logic Garden 248 (The Crystal Void / Tathata Arising)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: LineCollection Optimization & Strict Matrix Memory Cleansing

[INSTRUCTION]: RENDER_MODE explicitly set to "ZEN" for the 17.5s flow cycle.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
RENDER_MODE = "ZEN"  
DURATION = 17.5
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_248_crystal_reality"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS DEFAULT) --------
C_BG        = '#FFFFFF'        # Absolute Void / Cleared Buffer
C_TEXT      = '#020205'        # Stark Reality / Unyielding Geometry
C_CYAN      = '#00BFFF'        # Interpretive Noise / Brain Fog
C_MANTIS    = '#00C800'        # Tathata Phase-Lock
C_DIM       = '#D0D0D5'        # The Entropy Substrate / Cognitive Sweep
C_MAGENTA   = '#FF0055'        # Buffer Saturation Alarm

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_cyan    = np.array(hex_to_rgba(C_CYAN)[:3])
c_mantis  = np.array(hex_to_rgba(C_MANTIS)[:3])
c_dim     = np.array(hex_to_rgba(C_DIM)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])

# ------------------------------------------------------------------
# O(1) 3D TENSOR ALGEBRA 
# ------------------------------------------------------------------
def rotate_3d(points, rx, ry, rz):
    cx, sx = np.cos(rx), np.sin(rx)
    cy, sy = np.cos(ry), np.sin(ry)
    cz, sz = np.cos(rz), np.sin(rz)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cx, 0], [0, 0, 1]])
    R = Rz.dot(Ry).dot(Rx)
    return points.dot(R.T)

# ------------------------------------------------------------------
# BASE GEOMETRY ARRAYS: STATIC PRE-ALLOCATION
# ------------------------------------------------------------------
np.random.seed(248) 

MAX_PARTICLES = 25000

# 1. The Interpretive Noise (High Entropy Swarm)
theta_n = np.random.uniform(0, 2 * np.pi, MAX_PARTICLES)
phi_n = np.arccos(np.random.uniform(-1, 1, MAX_PARTICLES))
rad_n = np.random.uniform(10, 250, MAX_PARTICLES)

px_noise = rad_n * np.sin(phi_n) * np.cos(theta_n)
py_noise = rad_n * np.sin(phi_n) * np.sin(theta_n)
pz_noise = rad_n * np.cos(phi_n)

# 2. The Stark Reality Crystal (High-Fidelity Fibonacci Lattice)
N_VERTICES = 1200
indices = np.arange(0, N_VERTICES, dtype=float) + 0.5
phi_ang = np.arccos(1 - 2*indices/N_VERTICES)
theta_ang = np.pi * (1 + np.sqrt(5)) * indices
R_CYRSTAL = 90.0

cx_base = R_CYRSTAL * np.cos(theta_ang) * np.sin(phi_ang)
cy_base = R_CYRSTAL * np.sin(theta_ang) * np.sin(phi_ang)
cz_base = R_CYRSTAL * np.cos(phi_ang)

# Mathematical Rigidity: Edge connection mapping
print("Pre-computing Crystal Edge Tensors...")
edges = []
for i in range(N_VERTICES):
    for j in range(i+1, N_VERTICES):
        dist = np.sqrt((cx_base[i]-cx_base[j])**2 + (cy_base[i]-cy_base[j])**2 + (cz_base[i]-cz_base[j])**2)
        if dist < 16.0:  # Distance optimized for highly intricate mesh
            edges.append((i, j))
edges = np.array(edges)
print(f"Secured {len(edges)} rigid geometrical connections.")

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, noise_x, noise_y, noise_z, c_noise, s_noise, c_x, c_y, c_z, crystal_prog, heat, is_flash, is_tathata = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_MAGENTA if is_flash and t_sec < 6.0 else C_BG
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    ax.set_xlim(-160, 160)
    ax.set_ylim(-260, 260)

    if not is_flash:
        # 1. Render Noise (If active)
        if len(noise_x) > 0:
            sort_idx = np.argsort(noise_z)
            n_x = noise_x[sort_idx]
            n_y = noise_y[sort_idx]
            n_c = c_noise[sort_idx]
            n_s = s_noise[sort_idx]
            ax.scatter(n_x, n_y, s=n_s, color=n_c, edgecolors='none', alpha=0.6, zorder=5)

        # 2. Render Crystal Geometry (If active)
        if crystal_prog > 0:
            # Edges via fast LineCollection
            segments = np.zeros((len(edges), 2, 2))
            segments[:, 0, 0] = c_x[edges[:, 0]]
            segments[:, 0, 1] = c_y[edges[:, 0]]
            segments[:, 1, 0] = c_x[edges[:, 1]]
            segments[:, 1, 1] = c_y[edges[:, 1]]
            
            c_edge = C_MANTIS if is_tathata else C_TEXT
            lc = LineCollection(segments, colors=c_edge, linewidths=0.6 * crystal_prog, alpha=0.8)
            ax.add_collection(lc)

            # Vertices
            v_color = C_BG if is_tathata else C_TEXT
            ax.scatter(c_x, c_y, s=12 * crystal_prog, color=C_TEXT, edgecolors='none', zorder=10)
            ax.scatter(c_x, c_y, s=3 * crystal_prog, color=v_color, edgecolors='none', zorder=11)

        # Tathata Phase-Lock UI
        if is_tathata:
            ax.add_patch(plt.Rectangle((-130, -140), 260, 280, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -110, "STARK.", color=C_TEXT, fontsize=35, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 120, "TATHĀTĀ: ABSOLUTE CLARITY", color=C_MANTIS, fontsize=11, fontname='monospace', weight='bold', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_CYAN if t_sec < 6.0 else (C_TEXT if t_sec < 14.8 else C_MANTIS)
    if is_tathata: ui_col = C_MANTIS
    if t_sec >= 6.0 and t_sec < 8.0: ui_col = C_BG # Fully muted during flush
    
    ax.text(-140, 240, "LG-248 :: THE CRYSTAL VOID", color=txt_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: O(N) BUFFER FLUSH / KINEMATIC REVEAL", color=txt_col, fontsize=8, fontname='monospace', zorder=80)
    
    obj_str = "THE INTERPRETER'S NOISE [COGNITIVE SEARCH]"
    if 6.0 <= t_sec < 8.0: obj_str = "BUFFER FLUSH [O(1) EMPTY VESSEL]"
    elif 8.0 <= t_sec < 14.8: obj_str = "REALITY ARISING [STARK GEOMETRY]"
    elif is_tathata: obj_str = "PRECISION ZERO-DECISION MATRIX"

    if t_sec < 6.0 or t_sec > 8.0:
        ax.text(-140, -180, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
        # Thermodynamic Hardware Metric: Interpretation Filter Load
        ax.text(-140, -205, "O(N) INTERPRETATION FILTER [BUFFER LOAD]", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
        ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
        bar_w = 280 * np.clip(heat, 0, 1)
        ax.add_patch(plt.Rectangle((-140, -210), bar_w, 4, facecolor=C_MAGENTA if heat > 0.9 else ui_col, zorder=81))

    # Phase Text Box
    if t_sec < 6.0 or t_sec > 8.0:
        ax.add_patch(plt.Rectangle((-140, 215), 280, 2, facecolor=ui_col, zorder=80))
        ax.text(140, 205, f"[{state_str}]", color=ui_col if (f%15<10 or is_tathata) else C_BG, fontsize=14, fontname='monospace', weight='bold', ha='right', zorder=80)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) STRUCTURAL INVERSION KINEMATICS
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        is_flash = False
        is_tathata = False
        
        cam_rx = np.pi/6 - (t_sec * 0.005)
        cam_ry = t_sec * 0.3 # Continuous slow observation 
        cam_rz = 0.0
        
        # Arrays to pass
        noise_x, noise_y, noise_z = [], [], []
        c_noise, s_noise = [], []
        c_x, c_y, c_z = [], [], []
        crystal_prog = 0.0
        heat = 0.0
        
        # -------------------------------------------------------------
        # THE VOID PROJECTION KINEMATICS
        # -------------------------------------------------------------
        
        if t_sec < 6.0:
            # PHASE 1: THE INTERPRETER'S NOISE
            state = "PHASE 1 :: THOUGHT CLUTTER"
            prog = t_sec / 6.0
            
            # Violent, massive swirling paths simulating brain-fog trying to calculate infinity
            n_x = px_noise + np.sin(py_noise * 0.05 + t_sec * 8.0) * 40.0
            n_y = py_noise + np.cos(px_noise * 0.05 + t_sec * 7.0) * 40.0
            n_z = pz_noise + np.sin(pz_noise * 0.05 + t_sec * 9.0) * 40.0
            
            pts = np.column_stack([n_x, n_y, n_z])
            rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
            noise_x, noise_y, noise_z = rot_pts[:, 0], rot_pts[:, 1], rot_pts[:, 2]
            
            # Color assignment
            c_noise = np.zeros((MAX_PARTICLES, 3))
            cyan_mask = np.random.rand(MAX_PARTICLES) > 0.4
            c_noise[cyan_mask] = c_cyan
            c_noise[~cyan_mask] = c_dim
            
            s_noise = np.ones(MAX_PARTICLES) * 2.0
            
            heat = 0.2 + (0.8 * prog) # Scaling interpretation buffer
            
            if t_sec > 5.8:
                is_flash = True if f % 4 < 2 else False

        elif t_sec < 8.0:
            # PHASE 2: THE BUFFER FLUSH
            state = "PHASE 2 :: THE VOID CLEARED"
            # Everything is empty. Arrays are dumped.
            # Only the stark White Canvas C_BG remains on screen.
            heat = 0.0

        elif t_sec < 14.8:
            # PHASE 3: REALITY ARISING 
            state = "PHASE 3 :: THE CRYSTAL FORMS"
            prog = (t_sec - 8.0) / 6.8
            # Elastic snap expansion
            ease = 1.0 - (1.0 - prog)**4
            crystal_prog = ease
            
            # Grow crystal mathematically from the center core
            cr_x = cx_base * ease
            cr_y = cy_base * ease
            cr_z = cz_base * ease
            
            pts = np.column_stack([cr_x, cr_y, cr_z])
            rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
            c_x, c_y, c_z = rot_pts[:, 0], rot_pts[:, 1], rot_pts[:, 2]
            
            heat = 0.0 # Zero cognitive load. True reality generates zero heat.

        else:
            # PHASE 4: TATHĀTĀ
            state = "TATHĀTĀ :: STARK REALITY"
            is_tathata = True
            crystal_prog = 1.0
            
            # Lock geometry in place, rotation halts 
            pts = np.column_stack([cx_base, cy_base, cz_base])
            rot_pts = rotate_3d(pts, np.pi/6 - (14.8 * 0.005), 14.8 * 0.3, 0)
            c_x, c_y, c_z = rot_pts[:, 0], rot_pts[:, 1], rot_pts[:, 2]
            
            heat = 0.0 

        # Cull and package
        yield (f, t_sec, state, noise_x, noise_y, noise_z, c_noise, s_noise, c_x, c_y, c_z, crystal_prog, heat, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 248: THE CRYSTAL VOID [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Intricate Topography via LineCollection Pre-Sets")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Filter Purged. Stark Reality Arisen.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
