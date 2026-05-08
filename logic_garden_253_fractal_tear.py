"""
SOVEREIGN CODE: logic_garden_253_fractal_tear.py
SYSTEM: Python Multicore / O(1) Non-Integer Scaling Topology
SCENE: Logic Garden 253 (The Fractal Tear / Deep Crystal)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Scalar Float Broadcast Correction / O(N) Depth Sorting

[INSTRUCTION]: RENDER_MODE explicitly set to "ZEN" for the 18.0s flow cycle.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
RENDER_MODE = "ZEN"  
DURATION = 18.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_253_fractal_tear"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE --------
C_BG        = '#FFFFFF'        # Absolute Flat Substrate
C_TEXT      = '#020205'        # UI / High Contrast Vectors
C_AZURE     = '#007FFF'        # The Outer Lattice / Euclidean Lie
C_MAGENTA   = '#FF0055'        # The Torn Dimension / Inner Shadow
C_GOLD      = '#FFB300'        # Kinetic Friction / Alien Ping
C_XENON     = '#E0FFFF'        # Tathata Phase-Lock
C_DIM       = '#D0D0D5'        # Grid Data

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_azure   = np.array(hex_to_rgba(C_AZURE)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_gold    = np.array(hex_to_rgba(C_GOLD)[:3])
c_dim     = np.array(hex_to_rgba(C_DIM)[:3])
c_xenon   = np.array(hex_to_rgba(C_XENON)[:3])

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
# BASE GEOMETRY ARRAYS: THE PI-SCALED MENGER LATTICE
# ------------------------------------------------------------------
np.random.seed(253)
MAX_PARTICLES = 32000

# INITIAL STATE: A dense, uniform 3D cube (Euclidean space)
base_pts = np.random.uniform(-100, 100, (MAX_PARTICLES, 3))

# NON-INTEGER RUPTURE IDENTIFICATION
# Find points that belong inside the 1/Pi "holes" iteratively
pi_inv = 1.0 / np.pi
limit_1 = 100 * pi_inv

mask_z = (np.abs(base_pts[:,0]) < limit_1) & (np.abs(base_pts[:,1]) < limit_1)
mask_y = (np.abs(base_pts[:,0]) < limit_1) & (np.abs(base_pts[:,2]) < limit_1)
mask_x = (np.abs(base_pts[:,1]) < limit_1) & (np.abs(base_pts[:,2]) < limit_1)

tear_mask_1 = mask_z | mask_y | mask_x

# Deep Iteration (The 2nd Fractal Tier)
offset = 100 * (1 - pi_inv)
limit_2 = offset * pi_inv
mask_z2 = (np.abs(np.abs(base_pts[:,0]) - offset) < limit_2) & (np.abs(np.abs(base_pts[:,1]) - offset) < limit_2)
mask_y2 = (np.abs(np.abs(base_pts[:,0]) - offset) < limit_2) & (np.abs(np.abs(base_pts[:,2]) - offset) < limit_2)
mask_x2 = (np.abs(np.abs(base_pts[:,1]) - offset) < limit_2) & (np.abs(np.abs(base_pts[:,2]) - offset) < limit_2)

tear_mask_2 = (mask_z2 | mask_y2 | mask_x2) & ~tear_mask_1

# TARGET VECTORS (The Tear expanding)
# Instead of deleting points, we violently stretch them outward into a dimensional shadow
target_pts = np.copy(base_pts)
target_pts[tear_mask_1] *= np.pi       # Push tier 1 out
target_pts[tear_mask_2] *= (np.pi**2)  # Push tier 2 further out

base_colors = np.zeros((MAX_PARTICLES, 3))
base_colors[:] = c_azure
base_colors[tear_mask_1] = c_magenta
base_colors[tear_mask_2] = c_gold

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, p_x, p_y, p_z, c_arr, s_arr, ping_active, arc_radius, is_tathata = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_XENON if is_tathata else C_BG
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    ax.set_xlim(-160, 160)
    ax.set_ylim(-260, 260)

    # Background Geometry Grid
    if t_sec > 1.0:
        for g_line in np.linspace(-150, 150, 7):
            ax.plot([-130, 130], [g_line, g_line], color=C_DIM, lw=0.5, alpha=0.3, zorder=1)
            ax.plot([g_line, g_line], [-150, 150], color=C_DIM, lw=0.5, alpha=0.3, zorder=1)

    # The Kinetic "Ping" Arcs (Escaping energy)
    if ping_active and arc_radius > 0:
        arc_circ = plt.Circle((0, 0), arc_radius, color=C_GOLD, fill=False, lw=1.5, alpha=max(0, 1.0 - (arc_radius/180.0)), zorder=5)
        ax.add_patch(arc_circ)

    # Tensor Geometry / Depth Sorting
    sort_idx = np.argsort(p_z)
    s_x = p_x[sort_idx]
    s_y = p_y[sort_idx]
    s_c = c_arr[sort_idx]
    s_size = s_arr[sort_idx]

    ax.scatter(s_x, s_y, s=s_size, color=s_c, edgecolors='none', alpha=0.85, zorder=10)

    # Tathata Phase-Lock UI
    if is_tathata:
        ax.add_patch(plt.Rectangle((-140, -180), 280, 360, facecolor='none', edgecolor=C_TEXT, lw=3, zorder=40))
        ax.text(0, -140, "TATHĀTĀ: ABSOLUTE GEOMETRY", color=C_TEXT, fontsize=13, fontname='monospace', weight='bold', ha='center', zorder=41)
        ax.text(0, -165, "[INFINITE WRITE-OPERATION HALTED]", color=C_AZURE, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_TEXT
    ui_col = C_AZURE if t_sec < 5.0 else (C_MAGENTA if t_sec < 12.0 else C_GOLD)
    if is_tathata: ui_col = C_TEXT
    
    ax.text(-140, 240, "LG-253 :: THE FRACTAL TEAR", color=txt_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: NON-INTEGER TOPOLOGY / DIMENSIONAL RUPTURE", color=txt_col, fontsize=8, fontname='monospace', zorder=80)
    
    obj_str = "EUCLIDEAN ILLUSION [SOLID STATE]"
    if 5.0 <= t_sec < 12.0: obj_str = "NON-INTEGER RUPTURE [PI-SCALING]"
    elif 12.0 <= t_sec < 16.0: obj_str = "DEEP CRYSTAL SATURATION [LEAKY GEOMETRY]"
    elif is_tathata: obj_str = "ABSOLUTE PRESENCE [TRUE VACUUM]"

    ax.text(-140, -180, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Mathematical Bounding Metric
    metric_label = "HAUSDORFF DIMENSIONAL TEAR [D = π]" 
    ax.text(-140, -205, metric_label, color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM, zorder=80))
    
    heat = 1.0 if is_tathata else np.clip(t_sec / 16.0, 0, 1)
    val_w = 280 * heat
    ax.add_patch(plt.Rectangle((-140, -210), val_w, 4, facecolor=ui_col, zorder=81))

    # Phase Text Box
    ax.add_patch(plt.Rectangle((-140, 215), 280, 2, facecolor=ui_col, zorder=80))
    ax.text(140, 205, f"[{state_str}]", color=ui_col if f%15<10 else C_BG, fontsize=14, fontname='monospace', weight='bold', ha='right', zorder=80)

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
        
        is_tathata = False
        ping_active = False
        arc_radius = 0.0
        
        # Smooth continuous rotation over the crystal structure
        cam_rx = np.pi/6 - (t_sec * 0.005)
        cam_ry = t_sec * 0.6 
        cam_rz = t_sec * 0.2
        
        c_arr = np.zeros((MAX_PARTICLES, 3))
        s_arr = np.ones(MAX_PARTICLES)
        curr_pts = np.copy(base_pts)

        # -------------------------------------------------------------
        # THE FRACTAL TEAR KINEMATICS
        # -------------------------------------------------------------
        
        if t_sec < 5.0:
            # PHASE 1: THE EUCLIDEAN ILLUSION
            state = "PHASE 1 :: THE INITIAL TRACE"
            c_arr[:] = c_azure
            s_arr[:] = 2.0

        elif t_sec < 12.0:
            # PHASE 2: NON-INTEGER RUPTURE
            state = "PHASE 2 :: DIMENSIONS TORN ASUNDER"
            prog = (t_sec - 5.0) / 7.0
            ease = prog ** 2 
            
            # HOTFIX: Strict scalar float math ensures global array mapping
            curr_pts = base_pts * (1.0 - ease) + target_pts * ease
            
            # Color interpolates into the deep crystal
            c_interp = c_azure * (1.0 - ease) + base_colors * ease
            c_arr[:] = c_interp
            s_arr[:] = 2.0 + (1.5 * ease)

        elif t_sec < 16.0:
            # PHASE 3: DEEP CRYSTAL SATURATION
            state = "PHASE 3 :: THE AXIOM OF BROKEN GLASS"
            prog = (t_sec - 12.0) / 4.0
            
            # The structure is fully torn. 
            curr_pts = np.copy(target_pts)
            c_arr[:] = np.copy(base_colors)
            s_arr[:] = 3.5
            
            # The Kinetic Pings trigger repeatedly
            ping_active = True
            arc_radius = ((t_sec-12.0) * 120.0) % 200.0

        else:
            # PHASE 4: TATHĀTĀ (Geometric Pop)
            state = "TATHĀTĀ :: O(1) CRYSTAL RESOLVED"
            is_tathata = True
            
            # The 3D rotation instantly halts at t=16.0s
            cam_rx = np.pi/6 - (16.0 * 0.005)
            cam_ry = 16.0 * 0.6 
            cam_rz = 16.0 * 0.2
            
            curr_pts = np.copy(target_pts)
            # Colors snap perfectly to deep stark monochrome and Azure
            c_arr[:] = c_text
            c_arr[~tear_mask_1 & ~tear_mask_2] = c_azure
            
            s_arr[:] = 4.0 

        # Apply Global Tensor Matrix
        rot_pts = rotate_3d(curr_pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1]
        z_depth = rot_pts[:, 2] 

        # O(N) Geometry Culling
        cull_mask = (proj_y > -260) & (proj_y < 260) & (proj_x > -160) & (proj_x < 160)

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], c_arr[cull_mask], s_arr[cull_mask], ping_active, arc_radius, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 253: THE FRACTAL TEAR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Float Datatype Preservation for O(1) Matrix Kinematics")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Dimensional Hierarchy Severed. Crystal Locked.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
