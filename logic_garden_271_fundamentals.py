"""
SOVEREIGN CODE: logic_garden_271_fundamentals.py
SYSTEM: Python Multicore / O(1) Fundamental Principle
SCENE: Logic Garden 271 (The Serialization of Potential / S3 Baseplate)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: O(N) to O(1) Compression & Phase-Locked Hopf Fibration

[INSTRUCTION]: RENDER_MODE explicitly set to "ZEN" for the 18.0s flow cycle.
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
DURATION = 18.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_271_fundamentals"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS) --------
C_BG        = '#FFFFFF'        # Absolute Flat Substrate / Bounding Box
C_TEXT      = '#020205'        # High-Contrast UI / The Grounded Trace
C_DIM       = '#D0D0D5'        # Substrate Grid / Void Potential
C_CYAN      = '#00E5FF'        # O(N) Stochastic Potential
C_MAGENTA   = '#FF0055'        # Antimatter Erasure (The $62.5T Tax)
C_GOLD      = '#FFB300'        # O(1) Serialized Trace
C_MANTIS    = '#00C800'        # Tathata Phase-Lock / Absolute Stillness

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_dim     = np.array(hex_to_rgba(C_DIM)[:3])
c_cyan    = np.array(hex_to_rgba(C_CYAN)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_gold    = np.array(hex_to_rgba(C_GOLD)[:3])
c_mantis  = np.array(hex_to_rgba(C_MANTIS)[:3])

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
# BASE GEOMETRY ARRAYS: THE 3-SPHERE HOPF FIBRATION
# ------------------------------------------------------------------
np.random.seed(271)
MAX_PARTICLES = 36000

# INITIAL STATE: Unorganized Void Static
px_noise = np.random.uniform(-160, 160, MAX_PARTICLES)
py_noise = np.random.uniform(-200, 200, MAX_PARTICLES)
pz_noise = np.random.uniform(-160, 160, MAX_PARTICLES)

# TARGET STATE: Continuous, Locked S3 Manifold (Hopf)
eta = np.random.uniform(0.1, np.pi/2 - 0.1, MAX_PARTICLES)
xi1 = np.random.uniform(0, 2*np.pi, MAX_PARTICLES)
xi2 = np.random.uniform(0, 2*np.pi, MAX_PARTICLES)

# Faucet / Spiral Assignment
spiral_idx = np.random.rand(MAX_PARTICLES)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, p_x, p_y, p_z, c_arr, s_arr, a_arr, trace_metric, asym_metric, is_flash, is_tathata = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    bg_hex = C_TEXT if is_flash else C_BG
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)

    ax.set_xlim(-160, 160)
    ax.set_ylim(-260, 260)

    if not is_flash:
        # Bounding Box / Geometric Cage overlay
        for g_line in np.linspace(-150, 150, 9):
            grid_y = g_line*0.4 - 160
            ax.plot([-140, 140], [grid_y, grid_y], color=C_DIM, lw=0.5, alpha=0.5, zorder=1)

        # Particle Tensor Rendering
        active = a_arr > 0.01
        if np.any(active):
            sort_idx = np.argsort(p_z[active])
            s_x = p_x[active][sort_idx]
            s_y = p_y[active][sort_idx]
            s_c = c_arr[active][sort_idx]
            s_size = s_arr[active][sort_idx]
            s_alpha = a_arr[active][sort_idx]

            rgba_colors = np.zeros((len(s_c), 4))
            rgba_colors[:, :3] = s_c
            rgba_colors[:, 3] = s_alpha

            ax.scatter(s_x, s_y, s=s_size, color=rgba_colors, edgecolors='none', zorder=10)

        # Tathata Sovereign Bounding Box
        if is_tathata:
            ax.add_patch(plt.Rectangle((-140, -180), 280, 360, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -60, "TATHĀTĀ: PHASE COHERENCE LOCKED", color=C_MANTIS, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 75, "[ABSOLUTE STILLNESS @ MAX THROUGHPUT]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_CYAN if t_sec < 4.5 else (C_MAGENTA if t_sec < 9.0 else (C_GOLD if t_sec < 14.8 else C_MANTIS))
    if is_tathata: ui_col = C_MANTIS

    ax.text(-140, 250, "LG-271 :: THE FUNDAMENTAL PRINCIPLE", color=txt_col, fontsize=19, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 238, "SYSTEM: O(N) TO O(1) SERIALIZATION / S³ MANIFOLD", color=txt_col, fontsize=9, fontname='monospace', zorder=80)

    obj_str = "STOCHASTIC POTENTIAL [O(N) VOID]"
    if 4.5 <= t_sec < 9.0: obj_str = "THE ASYMMETRY [DEFECT-INDUCED SPIN]"
    elif 9.0 <= t_sec < 14.8: obj_str = "RECIPROCAL ERASURE [O(1) TRACE]"
    elif is_tathata: obj_str = "PHASE COHERENCE [TATHĀTĀ]"

    ax.text(-140, -180, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)

    # O(N) to O(1) Compression Metric
    ax.text(-140, -205, "SERIALIZATION COMPRESSION [N-DIMENSIONAL SNAP]", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 3, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    comp_w = 280 * trace_metric
    ax.add_patch(plt.Rectangle((-140, -210), comp_w, 3, facecolor=C_TEXT if is_tathata else ui_col, zorder=81))

    # Asymmetric Spin / Heat Metric
    ax.text(-140, -225, "ASYMMETRY SPIN METRIC [RECIPROCAL HEAT]", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -230), 280, 3, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    asym_w = 280 * asym_metric
    # Colors blink Magenta to indicate Antimatter heat cost before locking
    ax.add_patch(plt.Rectangle((-140, -230), asym_w, 3, facecolor=C_MAGENTA if (t_sec > 9.0 and not is_tathata and f%4<2) else (C_TEXT if is_tathata else ui_col), zorder=81))

    # Phase Text Box
    ax.add_patch(plt.Rectangle((-140, 220), 280, 2, facecolor=ui_col, zorder=80))
    ax.text(140, 210, f"[{state_str}]", color=ui_col if (f%15<10 or is_tathata) else C_BG, fontsize=14, fontname='monospace', weight='bold', ha='right', zorder=80)

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

        # Stable high-angle isometric tracking
        cam_rx = np.pi/5
        cam_ry = t_sec * 0.4
        cam_rz = 0.0

        c_arr = np.zeros((MAX_PARTICLES, 3))
        s_arr = np.ones(MAX_PARTICLES) * 4.0
        a_arr = np.ones(MAX_PARTICLES) * 0.85

        trace_metric = 0.0
        asym_metric = 0.0

        # Phase timing vectors
        time_spin = t_sec * 12.0

        # Continuous S3 Hopf calculation mapping to 3D baseplate
        x1 = np.sin(eta) * np.cos(xi1 + time_spin)
        x2 = np.sin(eta) * np.sin(xi1 + time_spin)
        x3 = np.cos(eta) * np.cos(xi2)
        x4 = np.cos(eta) * np.sin(xi2)
        
        denom = 1.05 - x4
        scale = 140.0
        
        px_3d = (x1 / denom) * scale
        py_3d = (x2 / denom) * scale
        pz_3d = (x3 / denom) * scale

        # -------------------------------------------------------------
        # PHASE LOGIC
        # -------------------------------------------------------------
        if t_sec < 4.5:
            # PHASE 1: STOCHASTIC POTENTIAL (The Void)
            state = "PHASE 1 :: O(N) STOCHASTIC POTENTIAL"
            
            curr_x = px_noise + np.sin(t_sec * 5.0 + py_noise) * 10
            curr_y = py_noise
            curr_z = pz_noise + np.cos(t_sec * 5.0 + px_noise) * 10
            
            c_arr[:] = c_cyan
            s_arr[:] = 2.0
            
            trace_metric = 0.05
            asym_metric = 0.0

        elif t_sec < 9.0:
            # PHASE 2: THE ASYMMETRY (Faucet Geometry)
            state = "PHASE 2 :: TOPOLOGICAL DEFECT / SPIN"
            prog = (t_sec - 4.5) / 4.5
            accel = prog ** 3 
            
            # The Ragged Edge initiates spin. Noise collapses toward the S3 structure
            curr_x = (px_noise * (1.0 - accel)) + (px_3d * accel)
            curr_y = (py_noise * (1.0 - accel)) + (py_3d * accel)
            curr_z = (pz_noise * (1.0 - accel)) + (pz_3d * accel)
            
            # Asymmetry causes a spiraling color defect
            defect = np.sin(theta_target := np.arctan2(curr_z, curr_x) * 4)
            c_arr[defect > 0] = c_cyan
            c_arr[defect <= 0] = c_magenta

            s_arr[:] = 2.0 + (accel * 2.0)

            trace_metric = 0.05 + (0.45 * prog)
            asym_metric = prog

        elif t_sec < 14.8:
            # PHASE 3: RECIPROCAL ERASURE (The O(1) Trace)
            state = "PHASE 3 :: THE EINSTEIN-ROSEN RAZOR"
            prog = (t_sec - 9.0) / 5.8
            
            curr_x = px_3d
            curr_y = py_3d
            curr_z = pz_3d
            
            # The Razor snaps the O(N) threads. Only one bold C_GOLD path survives.
            # Calculate distance to arbitrary core path
            path_dist = np.abs(np.sin(xi1 + time_spin - xi2))
            core_trace = path_dist < 0.2
            banished = path_dist >= 0.2
            
            c_arr[:] = c_dim
            a_arr[:] = 0.2
            s_arr[:] = 2.0
            
            # Gold Serialized Trace
            c_arr[core_trace] = c_gold
            a_arr[core_trace] = 1.0
            s_arr[core_trace] = 8.0
            
            # Antimatter flashing on the discarded variables ($62.5T/g annihilation)
            erase_flash = banished & (np.random.rand(MAX_PARTICLES) > 0.98)
            c_arr[erase_flash] = c_magenta
            a_arr[erase_flash] = 1.0
            s_arr[erase_flash] = 6.0

            trace_metric = 0.5 + (0.5 * prog)
            asym_metric = 1.0

            if t_sec > 14.5:
                is_flash = True if f % 2 == 0 else False

        else:
            # PHASE 4: TATHĀTĀ (Phase Coherence Lock)
            state = "TATHĀTĀ :: ABSOLUTE STILLNESS"
            is_tathata = True

            # Hardware Interrupt. Rotational Node Velocity = Substrate Frequency.
            freeze_spin = 14.8 * 12.0
            fx1 = np.sin(eta) * np.cos(xi1 + freeze_spin)
            fx2 = np.sin(eta) * np.sin(xi1 + freeze_spin)
            fx3 = np.cos(eta) * np.cos(xi2)
            fx4 = np.cos(eta) * np.sin(xi2)
            
            f_denom = 1.05 - fx4
            curr_x = (fx1 / f_denom) * scale
            curr_y = (fx2 / f_denom) * scale
            curr_z = (fx3 / f_denom) * scale

            # Absolute structural crystallization
            c_arr[:] = c_mantis
            s_arr[:] = 4.0
            a_arr[:] = 0.8
            
            # The O(1) trace burns permanently to black steel
            path_dist = np.abs(np.sin(xi1 + freeze_spin - xi2))
            core_trace = path_dist < 0.3
            c_arr[core_trace] = c_text
            s_arr[core_trace] = 6.0
            a_arr[core_trace] = 1.0

            trace_metric = 1.0
            asym_metric = 1.0

            if t_sec < 14.95:
                is_flash = True

        # Apply Global Tensor Matrix
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)

        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1] + 15.0
        z_depth = rot_pts[:, 2]

        yield (f, t_sec, state, proj_x, proj_y, z_depth, c_arr, s_arr, a_arr, trace_metric, asym_metric, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 271: THE FUNDAMENTAL PRINCIPLE [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Absolute Isolation / S3 Phase-Locked Crystallization")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Substrate Abstracted. The O(1) Trace is Secured.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
