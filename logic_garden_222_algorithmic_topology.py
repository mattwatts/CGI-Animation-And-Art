"""
SOVEREIGN CODE: logic_garden_222_algorithmic_topology.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Algorithmic Topology Analysis (17.5 seconds)
SCENE: Logic Garden 222 (YouTube Recommendation Engine / The Filter Bubble)
HOTFIX: O(N) Depth Sorting, Color Kwarg Syntax Enforcement, Bounding Box Clamping
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_222_algorithmic_topology"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'
C_CYAN      = '#00FFFF'        # Jagged Truth / O(N) Complex Data
C_MAGENTA   = '#FF0055'        # Sensationalism / High-Fluency Emotional Data
C_GOLD      = '#FFD700'        # Kinematic Spallation / Feed Severance
C_MANTIS    = '#00FF00'        # Sovereign Code / Compile-Time Quarantine

MAX_PARTICLES = 25000

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_void = np.array(hex_to_rgba(C_VOID)[:3])
c_text = np.array(hex_to_rgba(C_TEXT)[:3])
c_cyan = np.array(hex_to_rgba(C_CYAN)[:3])
c_mage = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_gold = np.array(hex_to_rgba(C_GOLD)[:3])
c_mantis = np.array(hex_to_rgba(C_MANTIS)[:3])
c_dim = np.array(hex_to_rgba(C_DIM)[:3])

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
# BASE GEOMETRY ARRAYS: THE GLOBAL NETWORK
# ------------------------------------------------------------------
np.random.seed(404)

# Initial chaotic network of truth (Cyan) and noise (Magenta)
phi = np.arccos(1 - 2 * np.random.rand(MAX_PARTICLES))
theta = 2 * np.pi * np.random.rand(MAX_PARTICLES)
radii = np.cbrt(np.random.rand(MAX_PARTICLES)) * 140.0 # Dense sphere distribution

px_base = radii * np.sin(phi) * np.cos(theta)
py_base = radii * np.sin(phi) * np.sin(theta)
pz_base = radii * np.cos(phi)

# Assign intrinsic data values (Truth vs Emotion)
is_emotion = np.random.rand(MAX_PARTICLES) > 0.5

# The Filter Bubble Target Geometry (A tight ring around to the center)
bubble_r = np.random.uniform(25.0, 45.0, MAX_PARTICLES)
bubble_theta = np.random.uniform(0, 2*np.pi, MAX_PARTICLES)
bubble_z = np.random.uniform(-10.0, 10.0, MAX_PARTICLES)

px_bub = bubble_r * np.cos(bubble_theta)
py_bub = bubble_r * np.sin(bubble_theta)
pz_bub = bubble_z

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, proj_x, proj_y, z_depth, colors, sizes, algo_strain, is_flash, is_tathata = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_TEXT if is_flash else C_VOID
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    ax.set_xlim(-150, 150)
    ax.set_ylim(-260, 260)

    if not is_flash:
        # O(N) Depth Sorting
        sort_idx = np.argsort(z_depth)
        s_px = proj_x[sort_idx]
        s_py = proj_y[sort_idx]
        s_c = colors[sort_idx]
        s_s = sizes[sort_idx]

        ax.scatter(s_px, s_py, s=s_s, color=s_c, edgecolors='none', alpha=0.9, zorder=10)

        if is_tathata:
            # The Localized Compile-Time Quarantine Firewall
            ax.add_patch(plt.Rectangle((-50, -60), 100, 120, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -90, "TATHĀTĀ: FEED SEVERED.", color=C_MANTIS, fontsize=11, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 70, "[COMPILE-TIME QUARANTINE]", color=C_DIM, fontsize=10, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    ui_col = C_CYAN if t_sec < 4.0 else (C_MAGENTA if t_sec < 14.8 else C_MANTIS)
    txt_col = C_TEXT if not is_flash else C_VOID

    ax.text(-140, 240, "LG-222 :: ALGORITHMIC TOPOLOGY", color=ui_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: RECOMMENDATION ENGINE / FILTER BUBBLE", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    
    # Telemetry Status
    obj_str = "TRUTH / O(N) FRICTION"
    if 4.0 <= t_sec < 9.0: obj_str = "SEVERING UNWANTED VARIABLES"
    elif 9.0 <= t_sec < 14.8: obj_str = "MAXIMIZING WATCH TIME (T)"
    elif is_tathata: obj_str = "THERMODYNAMIC ENGINE REJECTED"

    ax.text(-140, -180, f"OBJECTIVE FUNCTION : {obj_str}", color=ui_col, fontsize=11, fontname='monospace', weight='bold', zorder=80)
    
    # Thermodynamic Hardware Metric: The Amygdala Drive
    ax.text(-140, -205, "CAPITAL FLUX CONVERSION (ATTENTION MINING)", color=txt_col, fontsize=10, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM, zorder=80))
    bar_w = 280 * np.clip(algo_strain, 0, 1)
    ax.add_patch(plt.Rectangle((-140, -210), bar_w, 4, facecolor=C_MAGENTA if (t_sec < 14.8) else C_MANTIS, zorder=81))

    # Phase Text Box
    ax.add_patch(plt.Rectangle((-140, 215), 280, 2, facecolor=ui_col, zorder=80))
    ax.text(140, 205, f"[{state_str}]", color=ui_col if (f%15<10 or is_tathata) else C_VOID, fontsize=14, fontname='monospace', weight='bold', ha='right', zorder=80)

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
        
        # Isometric Camera
        cam_rx = -np.pi/5
        cam_ry = t_sec * 0.15
        cam_rz = 0.0
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 4.0
        
        curr_x = np.copy(px_base)
        curr_y = np.copy(py_base)
        curr_z = np.copy(pz_base)

        algo_strain = 0.0

        # -------------------------------------------------------------
        # PHASE LOGIC
        # -------------------------------------------------------------
        if t_sec < 4.0:
            state = "THE MACRO UNIVERSE :: JAGGED REALITY"
            
            colors[is_emotion] = c_mage
            colors[~is_emotion] = c_cyan
            # Drifting, high-entropy complex matrix
            curr_x += np.sin(py_base*0.05 + t_sec) * 5.0
            curr_y += np.cos(px_base*0.05 + t_sec) * 5.0
            
            algo_strain = 0.2

        elif t_sec < 9.0:
            state = "ALGORITHMIC SEVERANCE :: BUILDING THE DIMPLE"
            prog = (t_sec - 4.0) / 5.0
            accel = prog ** 2
            
            # 1. The algorithm targets C_MAGENTA data and pulls it aggressively into the localized ring
            curr_x[is_emotion] = px_base[is_emotion] * (1.0 - accel) + px_bub[is_emotion] * accel
            curr_y[is_emotion] = py_base[is_emotion] * (1.0 - accel) + py_bub[is_emotion] * accel
            curr_z[is_emotion] = pz_base[is_emotion] * (1.0 - accel) + pz_bub[is_emotion] * accel
            
            # Spin the ring
            ring_rot = accel * np.pi * 2.0
            ox = curr_x[is_emotion] * np.cos(ring_rot) - curr_y[is_emotion] * np.sin(ring_rot)
            oy = curr_x[is_emotion] * np.sin(ring_rot) + curr_y[is_emotion] * np.cos(ring_rot)
            curr_x[is_emotion] = ox
            curr_y[is_emotion] = oy
            
            colors[is_emotion] = c_mage
            sizes[is_emotion] = 5.0 + (accel * 3.0)
            
            # 2. The Truth (C_CYAN) is structurally expelled outward and muted to build the false vacuum
            curr_x[~is_emotion] = px_base[~is_emotion] * (1.0 + accel * 0.5)
            curr_y[~is_emotion] = py_base[~is_emotion] * (1.0 + accel * 0.5)
            curr_z[~is_emotion] = pz_base[~is_emotion] * (1.0 + accel * 0.5)
            
            colors[~is_emotion] = c_cyan * (1.0 - accel) + c_dim * accel
            
            algo_strain = 0.2 + (prog * 0.8)

        elif t_sec < 14.8:
            state = "THE SMOOTH GRAPH :: MODEL COLLAPSE"
            if t_sec < 9.1: is_flash = True
            
            # The filter bubble is entirely sealed. The user is violently spun in an echo chamber.
            # Emotion vectors are locked into the bubble, spinning at high velocity
            rot_speed = t_sec * 8.0 
            ox = px_bub[is_emotion] * np.cos(rot_speed) - py_bub[is_emotion] * np.sin(rot_speed)
            oy = px_bub[is_emotion] * np.sin(rot_speed) + py_bub[is_emotion] * np.cos(rot_speed)
            curr_x[is_emotion] = ox
            curr_y[is_emotion] = oy
            curr_z[is_emotion] = pz_bub[is_emotion]
            
            # Pulsing heat inside the bubble (fake fluency)
            colors[is_emotion] = c_mage
            sizes[is_emotion] = 8.0 + 3.0 * np.sin(t_sec * 15.0)
            
            # The rest of reality is completely dead/dim to the user
            curr_x[~is_emotion] = px_base[~is_emotion] * 1.5
            curr_y[~is_emotion] = py_base[~is_emotion] * 1.5
            curr_z[~is_emotion] = pz_base[~is_emotion] * 1.5
            colors[~is_emotion] = c_dim
            sizes[~is_emotion] = 2.0
            
            algo_strain = 1.0 # Peak engagement mining

        else:
            state = "TATHĀTĀ :: COMPILE-TIME QUARANTINE"
            is_tathata = True
            
            # The algorithms grasp is severed. The parasitic feed collapses into the void.
            # Sovereign Box initializes in the center
            curr_x *= 0.0
            curr_y *= 0.0
            curr_z *= 0.0
            
            # We map a rigid inner cube of protection utilizing the remaining vertices
            c_r = np.random.uniform(5.0, 30.0, MAX_PARTICLES)
            c_th = np.random.uniform(0, np.pi*2, MAX_PARTICLES)
            c_ph = np.random.uniform(0, np.pi, MAX_PARTICLES)
            
            curr_x = c_r * np.sin(c_ph) * np.cos(c_th)
            curr_y = c_r * np.sin(c_ph) * np.sin(c_th)
            curr_z = c_r * np.cos(c_ph)
            
            colors[:, :] = c_mantis
            sizes[:] = 5.0
            
            algo_strain = 0.0 # Absolute thermodynamic zero / Safety
            
            if t_sec < 14.95:
                is_flash = True

        # Apply Global Tensor Matrix
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1]
        z_depth = rot_pts[:, 2] 

        # O(1) Geometry Culling
        cull_mask = (proj_y > -260) & (proj_y < 260) & (proj_x > -150) & (proj_x < 150)

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], colors[cull_mask], sizes[cull_mask], algo_strain, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 222: THE ALGORITHMIC TOPOLOGY [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Scope Clamping & Filter Bubble Kinematics")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Server Link Severed.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
