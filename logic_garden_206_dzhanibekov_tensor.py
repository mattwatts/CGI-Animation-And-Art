"""
SOVEREIGN CODE: logic_garden_206_dzhanibekov_tensor.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / 3D Tensor Projection (17.5 seconds)
SCENE: Logic Garden 206 (The Dzhanibekov Effect / Intermediate Axis Flip)
HOTFIX: Euler Polhode Intersection (Hyperbolic Saddle O(N) Matrix Reveal)
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
OUT_DIR = "frames_206_dzhanibekov"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020206'
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'
C_CYAN      = '#00FFFF'        # Illusion of Smooth Spin
C_MAGENTA   = '#FF0055'        # Mathematical Friction / Orthogonal Rupture
C_GOLD      = '#FFD700'        # Kinetic Axis / Saddle Topology
C_MANTIS    = '#00FF00'        # Terminal Truth
C_NODE      = '#222233'

# ------------------------------------------------------------------
# O(1) 3D TENSOR ALGEBRA & TOPOLOGY
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

def project_ortho(points, scale=1.0):
    return points[:, 0] * scale, points[:, 1] * scale

# Define the Asymmetrical T-Handle
shaft_h = 100.0
cross_w = 80.0

# Generate O(N) Euler Saddle Topology (Hyperbolic Paraboloid z = y^2 - x^2)
s_grid = np.linspace(-120, 120, 50) # 2500 node high-density cage
SX, SY = np.meshgrid(s_grid, s_grid)
SZ = (SY**2 / 80.0) - (SX**2 / 80.0)
SADDLE_BASE = np.column_stack([SX.flatten(), SY.flatten(), SZ.flatten()])

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, rx, ry, rz, flip_vel, phase, is_flash, is_tathata = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_TEXT if is_flash else C_VOID
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    ax.set_xlim(-150, 150)
    ax.set_ylim(-260, 260)

    # Base Nodes for wireframe
    shaft_pts = np.array([[0, -shaft_h/2, 0], [0, shaft_h/2, 0]])
    cross_pts = np.array([[-cross_w/2, shaft_h/2 - 10, 0], [cross_w/2, shaft_h/2 - 10, 0]])
    asym_mass_pts = np.array([[0, -shaft_h/2 + 20, 30]]) 

    # Compute Structural Rotations
    rot_shaft = rotate_3d(shaft_pts, rx, ry, rz)
    rot_cross = rotate_3d(cross_pts, rx, ry, rz)
    rot_mass  = rotate_3d(asym_mass_pts, rx, ry, rz)

    px_s, py_s = project_ortho(rot_shaft)
    px_c, py_c = project_ortho(rot_cross)
    px_m, py_m = project_ortho(rot_mass)

    if not is_flash:
        line_clr = C_CYAN if flip_vel < 0.1 else C_MANTIS
        if phase == 2: line_clr = C_MAGENTA
        if is_tathata: line_clr = C_MANTIS

        # --- THE TOPOLOGICAL REVEAL (THE ZEN MOMENT) ---
        # The saddle matrix fades in during high velocity flips, and locks permanently during Tathata
        if flip_vel > 0.05 or is_tathata:
            # Rotate the generic saddle to match the bounding box orientation of the object
            rot_saddle = rotate_3d(SADDLE_BASE, rx, ry, rz)
            px_sad, py_sad = project_ortho(rot_saddle)
            
            # Z-sorting proxy (closest nodes are brighter/larger)
            z_depth = rot_saddle[:, 2] 
            
            visibility = flip_vel if not is_tathata else 1.0
            
            # Color assignment based on Hyperbolic tension
            sad_c = np.zeros((len(px_sad), 4))
            # Gold mapping for peaks, Magenta for troughs
            sz_norm = (SADDLE_BASE[:,2] - SADDLE_BASE[:,2].min()) / (SADDLE_BASE[:,2].max() - SADDLE_BASE[:,2].min())
            
            for i in range(len(sz_norm)):
                color_arr = np.array([1, 0, 0.33]) if sz_norm[i] < 0.5 else np.array([1, 0.84, 0])
                sad_c[i] = [color_arr[0], color_arr[1], color_arr[2], visibility * np.clip((z_depth[i] + 150)/300, 0.1, 0.9)]
            
            sizes = np.clip((z_depth + 150) / 10, 1, 30)
            ax.scatter(px_sad, py_sad, s=sizes, c=sad_c, edgecolors='none', zorder=5)

        # Draw Z-Axis Ghost Line
        ax.plot([0, 0], [-180, 180], color=C_DIM, lw=2, linestyle='--', zorder=1)

        # Draw structural spine
        lw_str = 6 if is_tathata else 14
        glow_lw = 24 if is_tathata else 20
        
        # Inner Core
        ax.plot(px_s, py_s, color=C_TEXT if not is_tathata else C_MANTIS, lw=lw_str-2, solid_capstyle='round', zorder=11)
        ax.plot(px_c, py_c, color=C_TEXT if not is_tathata else C_MANTIS, lw=lw_str-4, solid_capstyle='round', zorder=11)
        
        # Outer Glow Bounding
        ax.plot(px_s, py_s, color=line_clr, lw=glow_lw, solid_capstyle='round', alpha=0.6, zorder=10)
        ax.plot(px_c, py_c, color=line_clr, lw=glow_lw-4, solid_capstyle='round', alpha=0.6, zorder=10)

        # Asymmetrical Mass
        ax.plot([px_s[0], px_m[0]], [py_s[0], py_m[0]], color=line_clr, lw=2, zorder=12)
        ax.scatter(px_m, py_m, s=400, facecolor=C_VOID, edgecolor=line_clr, lw=4, zorder=15)
        ax.scatter(px_m, py_m, s=80, facecolor=C_TEXT if not is_tathata else C_MANTIS, zorder=16)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    ui_col = C_CYAN
    if flip_vel > 0.1: ui_col = C_MAGENTA
    if is_tathata: ui_col = C_MANTIS
    txt_col = C_TEXT if not is_flash else C_VOID

    # Header Matrix
    ax.text(-140, 240, "LG-206 :: THE DZHANIBEKOV TENSOR", color=ui_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: O(N) POLHODE SADDLE INTERSECTION", color=txt_col, fontsize=12, fontname='monospace', zorder=80)
    
    # Mathematical Bounding Frame
    ax.text(-140, -180, f"ω_2 (ROTATION) : {np.cos(ry*2.0):05.2f} RAD/S", color=C_CYAN if (np.cos(ry*2.0)>0.5 and not is_tathata) else txt_col, fontsize=14, fontname='monospace', zorder=80)
    ax.text(-140, -195, f"ω_1 (RUPTURE)  : {flip_vel*10.0:05.2f} RAD/S", color=C_MAGENTA if (flip_vel>0.1 and not is_tathata) else txt_col, fontsize=14, fontname='monospace', zorder=80)

    # Instability Matrix
    ax.text(-140, -220, "GEOMETRIC CAGE: HYPERBOLIC PARABOLOID TENSION", color=txt_col, fontsize=12, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -225), 280, 4, facecolor=C_DIM, zorder=80))
    bar_w = 280 * np.clip(flip_vel * 2.0 + 0.05, 0, 1) if not is_tathata else 280
    ax.add_patch(plt.Rectangle((-140, -225), bar_w, 4, facecolor=ui_col, zorder=81))

    # Phase Text
    status_txt = "ILLUSION: CONSTANT ROTATION"
    if phase == 2: status_txt = "RUPTURE: ORTHOGONAL COLLAPSE"
    if is_tathata: status_txt = "TATHĀTĀ: THE MATH IS A PRISON."

    ax.text(-140, -245, f"[{status_txt}]", color=ui_col if (f%15<10 or is_tathata) else C_VOID, fontsize=18, fontname='monospace', weight='bold', zorder=80)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) EULER KINEMATIC STREAM 
# ------------------------------------------------------------------
def generate_stream():
    ry = 0.0 
    rx = 0.0 
    rz = 0.0
    
    flip_points = [4.5, 9.5]
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        dt = 1.0 / FPS

        is_flash = False
        is_tathata = False
        phase = 1

        ry -= 2.0 * dt

        vel_x = 0.0
        for ft in flip_points:
            time_diff = t_sec - ft
            if abs(time_diff) < 1.0:
                phase = 2
                vel_x += np.exp(-(time_diff * 4.0)**2) * 5.0

        rx += vel_x * dt
        flip_vel = vel_x / 5.0

        if t_sec >= 14.8:
            is_tathata = True
            phase = 4
            ry -= ry * 0.1 # Exponential brake into the saddle
            rx -= rx * 0.1
            if t_sec < 14.95:
                is_flash = True

        yield (f, t_sec, rx, ry, rz, flip_vel, phase, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 206: THE DZHANIBEKOV TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Topological Saddle Reveal & Geometric Cage Insertion")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
