"""
PROJECT: Logic Garden 256b (Exact Physical Construct // Reciprocal Engine Matrix)
FORMAT: YouTube Shorts (1080x1920) // 60 FPS
METADATA: PHYSICS, COSMOLOGY, ANTIMATTER, ENGINEERING, PYTHON, MATHEMATICS
EXECUTION: True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true 3D spatial velocity vectors.
- Automated FFmpeg compilation immediately following frame generation.
- Absolute Segmentation Protocol: Particles rendered as 2-point kinetic line segments.
- Comparative Mathematics: Matter (Azure) vs Antimatter (Magenta) volumetric cancellation.
- Viewport Override: Locked cam_span guarantees 100% total system visibility.
- Daylight Palette (White Substrate / High-Contrast Edge Geometry).
- Australian spelling conventions maintained (maths, synchronisation, visualised).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.collections import LineCollection
import multiprocessing as mp
import os
import gc
import subprocess

# ======== SEQUENCE PARAMETERS ========
DURATION = 24.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_256b_reciprocal"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_AZURE     = '#005599'        # Matter (M)
C_MAGENTA   = '#E11D48'        # Antimatter (M-bar)
C_GOLD      = '#D97706'        # Gamma Annihilation Flash
C_BASE      = '#334155'        # Surviving Hardware Baseplate
C_GRID      = '#CBD5E1'        # Subdued Steel

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_azure   = np.array(hex_to_rgba(C_AZURE)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_base    = np.array(hex_to_rgba(C_BASE)[:3])

# ------------------------------------------------------------------
# O(N) 3D TENSOR MATHS
# ------------------------------------------------------------------
def rotate_3d(x, y, z, rx, ry, rz):
    cx, sx = np.cos(rx), np.sin(rx)
    cy, sy = np.cos(ry), np.sin(ry)
    cz, sz = np.cos(rz), np.sin(rz)
    
    # Rx
    y1 = y * cx - z * sx
    z1 = y * sx + z * cx
    # Ry
    x2 = x * cy + z1 * sy
    z2 = -x * sy + z1 * cy
    # Rz
    x3 = x2 * cz - y1 * sz
    y3 = x2 * sz + y1 * cz
    
    return x3, y3, z2

# ------------------------------------------------------------------
# BASE GEOMETRY ARRAYS: KINEMATIC VECTORS (NOT DOTS)
# ------------------------------------------------------------------
np.random.seed(256)
HALF_VECTORS = 6000
MAX_VECTORS = HALF_VECTORS * 2

# Matter Configuration
theta_m = np.random.uniform(0, 2*np.pi, HALF_VECTORS)
phi_m = np.arccos(np.random.uniform(-1, 1, HALF_VECTORS))
r_m = np.random.uniform(20, 90, HALF_VECTORS)

px_m = r_m * np.sin(phi_m) * np.cos(theta_m) - 120.0 
py_m = r_m * np.cos(phi_m)
pz_m = r_m * np.sin(phi_m) * np.sin(theta_m)

# Antimatter Configuration (Reciprocal Offset)
px_am = r_m * np.sin(phi_m) * np.cos(theta_m) + 120.0 
py_am = r_m * np.cos(phi_m)
pz_am = r_m * np.sin(phi_m) * np.sin(theta_m)

base_px = np.concatenate([px_m, px_am])
base_py = np.concatenate([py_m, py_am])
base_pz = np.concatenate([pz_m, pz_am])

base_colors = np.zeros((MAX_VECTORS, 3))
base_colors[:HALF_VECTORS] = c_azure
base_colors[HALF_VECTORS:] = c_magenta

# Asymmetry Flaw: 1% of Matter survives. 
survival_indices = np.random.choice(np.arange(HALF_VECTORS), size=int(HALF_VECTORS * 0.01), replace=False)
base_survival_mask = np.zeros(MAX_VECTORS, dtype=bool)
base_survival_mask[survival_indices] = True

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, p1_x, p1_y, p1_z, p2_x, p2_y, p2_z, c_arr, a_arr, metric, flash, grid_on = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    bg_hex = C_TEXT if flash > 0.9 else C_BG
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)

    cam_span = 260
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    # Gamma Annihilation Flash
    if flash > 0.0:
        flash_circ = plt.Circle((0, 0), flash * 600, color=C_GOLD, alpha=flash * 0.5, zorder=2)
        ax.add_patch(flash_circ)

    # Active Vector Filtering (Removes deleted vectors instantly to save processing time)
    active = a_arr > 0.01

    if np.any(active):
        u1, v1 = p1_x[active], p1_y[active]
        u2, v2 = p2_x[active], p2_y[active]
        z_avg = (p1_z[active] + p2_z[active]) / 2.0
        
        c_active = c_arr[active]
        a_active = a_arr[active]
        
        # Absolute Painter's Algorithm Depth Sort
        sort_idx = np.argsort(z_avg)[::-1]
        
        segments = np.stack((np.column_stack((u1[sort_idx], v1[sort_idx])), 
                             np.column_stack((u2[sort_idx], v2[sort_idx]))), axis=1)
        
        rgba = np.zeros((len(sort_idx), 4))
        rgba[:, :3] = c_active[sort_idx]
        rgba[:, 3] = a_active[sort_idx]

        # LineCollection replaces dots for continuous O(N) true vectors
        lc = LineCollection(segments, colors=rgba, linewidths=1.5, zorder=10)
        ax.add_collection(lc)

    # Baseplate Grid Structure
    if grid_on and not (flash > 0.9):
        lc_grid = []
        for g_line in np.linspace(-200, 200, 9):
            lc_grid.append([[-200, g_line], [200, g_line]])
            lc_grid.append([[g_line, -200], [g_line, 200]])
        
        # Apply slight camera tilt to the grid natively
        for line in lc_grid:
            pA_x, pA_y, pA_z = rotate_3d(line[0][0], line[0][1], -60.0, 0, 0.4, 0)
            pB_x, pB_y, pB_z = rotate_3d(line[1][0], line[1][1], -60.0, 0, 0.4, 0)
            ax.plot([pA_x, pB_x], [pA_y-150, pB_y-150], color=C_GRID, lw=1.0, alpha=0.4, zorder=1)

    # UI PANELS
    txt_col = C_BG if flash > 0.9 else C_TEXT
    ui_col = C_MAGENTA if t_sec < 8.0 else (C_GOLD if t_sec < 14.0 else C_AZURE)
    if grid_on: ui_col = C_BASE

    ui_t = cam_span * 1.45
    ax.add_patch(patches.Rectangle((-cam_span, ui_t), cam_span*2, cam_span*0.5, facecolor=bg_hex, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_t, ui_t], color=txt_col, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-256b // BARYON ASYMMETRY KINEMATICS", color=txt_col, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "RECIPROCAL ERASURE MATRIX", color=ui_col, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=bg_hex, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=txt_col, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, f"[STAGE] {state_str}", color=ui_col, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    
    metric_label = "MATTER SURVIVAL YIELD"
    ax.text(-cam_span*0.95, ui_b + cam_span*0.08, metric_label, color=txt_col, fontsize=10, fontname='monospace', zorder=82)
    
    bar_width = cam_span * 1.9
    ax.add_patch(plt.Rectangle((-cam_span*0.95, ui_b + cam_span*0.03), bar_width, 10, facecolor=C_GRID if not (flash > 0.9) else txt_col, zorder=80))
    ax.add_patch(plt.Rectangle((-cam_span*0.95, ui_b + cam_span*0.03), bar_width * np.clip(metric, 0, 1), 10, facecolor=ui_col, zorder=81))

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# O(1) STRUCTURAL INVERSION KINEMATICS (DATA STREAM)
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS

        grid_on = False
        flash = 0.0

        # Continuous smooth orbit
        cam_rx = np.pi/8 - (t_sec * 0.01)
        cam_ry = t_sec * 0.8
        cam_rz = 0.0

        c_arr = np.copy(base_colors)
        a_arr = np.ones(MAX_VECTORS) * 0.9

        cx = np.copy(base_px)
        cy = np.copy(base_py)
        cz = np.copy(base_pz)
        
        # Velocity vector tails to ensure we draw lines, not dots.
        vx = np.zeros(MAX_VECTORS)
        vy = np.zeros(MAX_VECTORS)
        vz = np.zeros(MAX_VECTORS)

        metric = 0.0

        if t_sec < 8.0:
            # PHASE 1: ORBITAL KINEMATICS
            state = "PHASE 1: MATTER / ANTIMATTER GENERATION"
            
            # Swirling angular momentum
            cx[:HALF_VECTORS] += np.sin(t_sec * 3.0) * 20.0
            cx[HALF_VECTORS:] -= np.sin(t_sec * 3.0) * 20.0
            
            vy[:HALF_VECTORS] = 10.0 * np.cos(t_sec * 2.0)
            vy[HALF_VECTORS:] = -10.0 * np.cos(t_sec * 2.0)
            metric = 0.0

        elif t_sec < 14.0:
            # PHASE 2: RECIPROCAL ANNIHILATION
            state = "PHASE 2: GAMMA ANNIHILATION (CANCELLATION)"
            prog = (t_sec - 8.0) / 6.0
            ease = prog ** 3

            # Snap to central intersection [0,0,0]
            cx[:HALF_VECTORS] = base_px[:HALF_VECTORS] * (1.0 - ease)
            cx[HALF_VECTORS:] = base_px[HALF_VECTORS:] * (1.0 - ease)
            cy *= (1.0 - ease)
            cz *= (1.0 - ease)

            # Trailing velocity pointing inward
            vx = -cx * 0.2
            vy = -cy * 0.2
            vz = -cz * 0.2

            doom_mask = ~base_survival_mask
            a_arr[doom_mask] = 0.9 * (1.0 - ease**2)

            if prog > 0.8:
                flash = (prog - 0.8) * 5.0 
                if 13.5 < t_sec < 13.8: flash = 1.0

            metric = (0.2 * ease)

        elif t_sec < 18.0:
            # PHASE 3: ASYMMETRY YIELD
            state = "PHASE 3: ASYMMETRY YIELD (MATTER SURVIVAL)"
            prog = (t_sec - 14.0) / 4.0
            ease = 1.0 - (1.0 - prog)**3

            doom_mask = ~base_survival_mask
            a_arr[doom_mask] = 0.0

            # Apply survival transformations using the correctly sized base_px/py/pz
            cx[base_survival_mask] = (base_px[base_survival_mask] + 120.0) * (0.05 + 1.2 * ease)
            cy[base_survival_mask] = base_py[base_survival_mask] * (0.05 + 1.2 * ease)
            cz[base_survival_mask] = base_pz[base_survival_mask] * (0.05 + 1.2 * ease)
            
            # Radiating vectors
            vx[base_survival_mask] = cx[base_survival_mask] * 0.1
            vy[base_survival_mask] = cy[base_survival_mask] * 0.1
            vz[base_survival_mask] = cz[base_survival_mask] * 0.1

            c_arr[base_survival_mask] = c_azure * (1 - ease) + c_base * ease
            a_arr[base_survival_mask] = 1.0

            metric = 0.2 + (0.8 * ease)

        else:
            # PHASE 4: STRUCTURAL BASEPLATE LOCK
            state = "PHASE 4: STRUCTURAL BASEPLATE LOCK"
            grid_on = True

            doom_mask = ~base_survival_mask
            a_arr[doom_mask] = 0.0

            cx[base_survival_mask] = (base_px[base_survival_mask] + 120.0) * 1.25
            cy[base_survival_mask] = base_py[base_survival_mask] * 1.25
            cz[base_survival_mask] = base_pz[base_survival_mask] * 1.25
            
            # Locked state (No velocity tails)
            vx[base_survival_mask] = 0
            vy[base_survival_mask] = 0
            vz[base_survival_mask] = 0

            c_arr[base_survival_mask] = c_base
            a_arr[base_survival_mask] = 1.0

            metric = 1.0

        # Project Vector Start Points (P1)
        p1_x, p1_y, p1_z = rotate_3d(cx, cy, cz, cam_rx, cam_ry, cam_rz)
        # Project Vector End Points (P2)
        p2_x, p2_y, p2_z = rotate_3d(cx+vx, cy+vy, cz+vz, cam_rx, cam_ry, cam_rz)

        yield (f, t_sec, state, p1_x, p1_y, p1_z, p2_x, p2_y, p2_z, c_arr, a_arr, metric, flash, grid_on)

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-256b: RECIPROCAL ENGINE MATRIX [CORES: {cpu_cores}]")
    print(f"Executing: True Continuous Vector Architecture (No Dots)")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Frames Generated. Engaging FFmpeg automation...")
    
    # Automated FFmpeg Compilation Execution
    ffmpeg_cmd = (
        'ffmpeg -y -framerate 60 -i frames_256b_reciprocal/frame_%04d.png '
        '-c:v libx264 -preset fast -crf 14 -pix_fmt yuv420p -threads 2 '
        'logic_garden_256b_reciprocal_engine.mp4'
    )
    subprocess.run(ffmpeg_cmd, shell=True)
    print("FFmpeg encoding complete. The MP4 array is secured on disk.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
