"""
SOVEREIGN CODE: logic_garden_267_3sphere.py
SYSTEM: Python Multicore / O(1) 4D Topological Manifold
SCENE: Logic Garden 267 (The 3-Sphere Bounding Box / Manifold Audit)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Stereographic Hopf Fibration & Local Identity Purge

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
OUT_DIR = "frames_267_3sphere"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS DEFAULT) --------
C_BG        = '#FFFFFF'        # Absolute Canvas
C_TEXT      = '#020205'        # High-Contrast UI / Tracking Grid
C_CYAN      = '#00E5FF'        # Local Flat Illusion
C_AZURE     = '#007FFF'        # S3 Great Circle Flow A
C_MAGENTA   = '#FF0055'        # S3 Great Circle Flow B
C_GOLD      = '#FFB300'        # Faucet Singularity Data
C_MANTIS    = '#00C800'        # Tathata / Absolute Stillness
C_DIM       = '#D0D0D5'        # Void Structure

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_cyan    = np.array(hex_to_rgba(C_CYAN)[:3])
c_azure   = np.array(hex_to_rgba(C_AZURE)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_gold    = np.array(hex_to_rgba(C_GOLD)[:3])
c_mantis  = np.array(hex_to_rgba(C_MANTIS)[:3])
c_dim     = np.array(hex_to_rgba(C_DIM)[:3])

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
# BASE GEOMETRY ARRAYS: THE 3-SPHERE TENSORS (Hopf Fibrations)
# ------------------------------------------------------------------
np.random.seed(267)
MAX_PARTICLES = 36000

# Parametric Setup for S3 mapping to R3
# Eta [0, pi/2], Xi1 [0, 2pi], Xi2 [0, 2pi]
eta = np.random.uniform(0.1, np.pi/2 - 0.1, MAX_PARTICLES)
xi1 = np.random.uniform(0, 2 * np.pi, MAX_PARTICLES)
xi2 = np.random.uniform(0, 2 * np.pi, MAX_PARTICLES)

# Initial Flat State Projection (The Local Illusion)
px_flat = np.random.uniform(-180, 180, MAX_PARTICLES)
pz_flat = np.random.uniform(-180, 180, MAX_PARTICLES)
py_flat = np.random.normal(0, 4, MAX_PARTICLES) # Mostly Flat

# Establish Color Assignment based on Eta (Fiber selection)
fiber_id = np.random.choice([0, 1], MAX_PARTICLES)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, p_x, p_y, p_z, c_arr, s_arr, a_arr, c_metric, t_metric, is_flash, is_tathata = packet

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
        # High-Contrast Track Grid
        for g_line in np.linspace(-150, 150, 9):
            grid_y = g_line*0.4 - 120
            ax.plot([-140, 140], [grid_y, grid_y], color=C_DIM, lw=0.5, alpha=0.3, zorder=1)

        # 4D Singularity Representation (The Unseen Center)
        if t_sec > 4.5 and not is_tathata:
            sing_alpha = np.clip((t_sec - 4.5) / 4.5, 0, 1) * 0.15
            ax.add_patch(plt.Circle((0, 0), 100, color=C_GOLD, alpha=sing_alpha, zorder=2))

        # Tensor Rendering
        active = a_arr > 0.01
        if np.any(active):
            # Strict O(N) Depth Processing to highlight volume
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
            ax.add_patch(plt.Rectangle((-15, -15), 30, 30, facecolor='none', edgecolor=C_TEXT, lw=2, zorder=40)) 
            ax.text(0, -60, "TATHĀTĀ: MANIFOLD LOCKED", color=C_MANTIS, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 75, "[S³ THERMODYNAMIC CAGE SECURED]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_CYAN if t_sec < 4.5 else (C_AZURE if t_sec < 9.0 else (C_MAGENTA if t_sec < 14.8 else C_MANTIS))
    if is_tathata: ui_col = C_MANTIS

    ax.text(-140, 250, "LG-267 :: THE 3-SPHERE AUDIT", color=txt_col, fontsize=19, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 238, "SYSTEM: FINITE BOUNDING BOX / S³ TOPOLOGY", color=txt_col, fontsize=9, fontname='monospace', zorder=80)

    obj_str = "THE LOCAL ILLUSION [MOSTLY FLAT]"
    if 4.5 <= t_sec < 9.0: obj_str = "TOPOLOGICAL WARPING [4D CURVATURE]"
    elif 9.0 <= t_sec < 14.8: obj_str = "GREAT ROTATION [CLOSED-LOOP MANIFOLD]"
    elif is_tathata: obj_str = "ABSOLUTE MANIFOLD [ZERO-TEMP STILLNESS]"

    ax.text(-140, -180, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)

    # Topological Tension Metrics
    ax.text(-140, -205, "SUBSTRATE CURVATURE INDEX [SPACE METRIC]", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 3, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    ax.add_patch(plt.Rectangle((-140, -210), 280 * c_metric, 3, facecolor=C_TEXT if is_tathata else ui_col, zorder=81))

    ax.text(-140, -225, "BOUNDARY TENSION LIMIT [THERMODYNAMIC CAGE]", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -230), 280, 3, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    ax.add_patch(plt.Rectangle((-140, -230), 280 * t_metric, 3, facecolor=C_TEXT if is_tathata else ui_col, zorder=81))

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

        # Slower, majestic, multi-axis audit rotation to reveal the closed structure
        cam_rx = np.pi/5 + np.sin(t_sec * 0.2) * 0.1
        cam_ry = t_sec * 0.35 
        cam_rz = 0.0

        c_arr = np.zeros((MAX_PARTICLES, 3))
        s_arr = np.ones(MAX_PARTICLES) * 4.0
        a_arr = np.ones(MAX_PARTICLES) * 0.85

        c_metric = 0.0
        t_metric = 0.0

        # Phase timing vectors (Spin calculation)
        time_spin = t_sec * 8.0
        
        # 4D S3 Calculation mapped to Stereographic 3D
        # Using Hopf Fibration parameters for extreme visual beauty inside the cage
        x1 = np.sin(eta) * np.cos(xi1 + time_spin)
        x2 = np.sin(eta) * np.sin(xi1 + time_spin)
        x3 = np.cos(eta) * np.cos(xi2)
        x4 = np.cos(eta) * np.sin(xi2)
        
        # Safe Projection factor (bounding to avoid infinity)
        denom = 1.05 - x4
        scale = 120.0
        
        px_3d = (x1 / denom) * scale
        py_3d = (x2 / denom) * scale
        pz_3d = (x3 / denom) * scale

        # -------------------------------------------------------------
        # THE 3-SPHERE KINEMATICS
        # -------------------------------------------------------------
        if t_sec < 4.5:
            # PHASE 1: THE LOCAL ILLUSION (Mostly Flat Substrate)
            state = "PHASE 1 :: MOSTLY FLAT BASEPLATE"
            
            # High speed lateral movement indicating local false infinity
            flow_offset = t_sec * 150.0
            curr_x = ((px_flat + flow_offset + 180) % 360) - 180
            curr_y = py_flat
            curr_z = pz_flat
            
            c_arr[:] = c_cyan
            s_arr[:] = 4.0

            c_metric = 0.05
            t_metric = 0.1

        elif t_sec < 9.0:
            # PHASE 2: TOPOLOGICAL WARPING (Curvature Audit)
            state = "PHASE 2 :: TOPOLOGICAL AUDIT (CURVING)"
            prog = (t_sec - 4.5) / 4.5
            accel = prog ** 3 
            
            # Substrate physically bends from the linear plane into the S3 Spherical Manifold
            # Linear flow also maps progressively into the time_spin
            curr_x = px_flat * (1.0 - accel) + px_3d * accel
            curr_y = py_flat * (1.0 - accel) + py_3d * accel
            curr_z = pz_flat * (1.0 - accel) + pz_3d * accel
            
            c_arr[fiber_id == 0] = c_cyan * (1.0 - accel) + c_azure * accel
            c_arr[fiber_id == 1] = c_cyan * (1.0 - accel) + c_magenta * accel

            s_arr[:] = 4.0 - (accel * 1.5)

            c_metric = 0.05 + (0.95 * prog)
            t_metric = 0.1 + (0.9 * accel)

        elif t_sec < 14.8:
            # PHASE 3: THE GREAT CIRCLES (Closed-Loop Manifold)
            state = "PHASE 3 :: GREAT CIRCLE MANIFOLD"
            
            curr_x = px_3d
            curr_y = py_3d
            curr_z = pz_3d
            
            c_arr[fiber_id == 0] = c_azure
            c_arr[fiber_id == 1] = c_magenta
            s_arr[:] = 2.5
            
            # Pulse the core density to simulate high thermodynamic pressure internally
            radius_dist = np.sqrt(curr_x**2 + curr_y**2 + curr_z**2)
            core_mask = radius_dist < 40.0
            c_arr[core_mask] = c_gold
            s_arr[core_mask] = 5.0

            c_metric = 1.0
            t_metric = 1.0

            if t_sec > 14.5:
                is_flash = True if f % 2 == 0 else False

        else:
            # PHASE 4: TATHĀTĀ (Absolute Movement in Stillness)
            state = "TATHĀTĀ :: MANIFOLD CAGE SECURED"
            is_tathata = True

            # Hardware Interrupt. Time_spin locks at exact frame coordinates.
            freeze_spin = 14.8 * 8.0
            fx1 = np.sin(eta) * np.cos(xi1 + freeze_spin)
            fx2 = np.sin(eta) * np.sin(xi1 + freeze_spin)
            fx3 = np.cos(eta) * np.cos(xi2)
            fx4 = np.cos(eta) * np.sin(xi2)
            f_denom = 1.05 - fx4
            
            curr_x = (fx1 / f_denom) * scale
            curr_y = (fx2 / f_denom) * scale
            curr_z = (fx3 / f_denom) * scale

            # Convert entirely to green structural verification lines
            c_arr[:] = c_mantis
            s_arr[:] = 3.0
            
            # Emphasize the core bounding anchor
            radius_dist = np.sqrt(curr_x**2 + curr_y**2 + curr_z**2)
            c_arr[radius_dist < 30.0] = c_text
            s_arr[radius_dist < 30.0] = 6.0

            c_metric = 1.0
            t_metric = 1.0

            if t_sec < 14.95:
                is_flash = True

        # Apply Global Tensor Matrix
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)

        proj_x = rot_pts[:, 0]
        # Shift slightly up visually
        proj_y = rot_pts[:, 1] + 20.0
        z_depth = rot_pts[:, 2]

        yield (f, t_sec, state, proj_x, proj_y, z_depth, c_arr, s_arr, a_arr, c_metric, t_metric, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 267: THE 3-SPHERE BOUNDING BOX [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Stereographic O(1) Mapping / Topological Identity Cleansing")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. 4D Audit Confirmed. Bounding Box is secure.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
