"""
SOVEREIGN CODE: logic_garden_266b_singular_trace.py
SYSTEM: Python Multicore / O(1) Singular Worldline Mapping
SCENE: Logic Garden 266b (The Singular Trace / Absolute Isolation)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Triple-Helix Eradication / Substrate Visual Contrast Override

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
OUT_DIR = "frames_266b_singular_trace"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS DEFAULT) --------
C_BG        = '#FFFFFF'        # Absolute Flat Substrate
C_TEXT      = '#020205'        # The Burned Single Trace
C_CYAN      = '#00E5FF'        # High-Contrast Void Static
C_MAGENTA   = '#FF0055'        # High-Contrast Void Static
C_GOLD      = '#FFB300'        # The Singular Kinetic Vector
C_MANTIS    = '#00C800'        # Tathata Phase-Lock
C_DIM       = '#A0A0A5'        # Substrate Grid (Darkened for visibility)

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_cyan    = np.array(hex_to_rgba(C_CYAN)[:3])
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
# BASE GEOMETRY ARRAYS: THE SUBSTRATE
# ------------------------------------------------------------------
np.random.seed(888)
MAX_PARTICLES = 35000

# Generating a dense, highly visible 3D box of particles for immediate impact
px_base = np.random.uniform(-140, 140, MAX_PARTICLES)
py_base = np.random.uniform(-200, 200, MAX_PARTICLES)
pz_base = np.random.uniform(-140, 140, MAX_PARTICLES)

noise_color = np.random.choice([0, 1], MAX_PARTICLES)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, p_x, p_y, p_z, c_arr, s_arr, a_arr, drill_y, is_flash, is_tathata = packet

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
        # High-Contrast tracking grid (Only visible after collapse in Phase 2)
        if t_sec > 4.5:
            grid_a = np.clip((t_sec - 4.5) / 2.0, 0, 0.4)
            for g_line in np.linspace(-150, 150, 9):
                ax.plot([-140, 140], [g_line*0.4 - 100, g_line*0.4 - 100], color=C_DIM, lw=1.0, alpha=grid_a, zorder=1)
                ax.plot([g_line, g_line], [-160, -40], color=C_DIM, lw=1.0, alpha=grid_a, zorder=1)

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
            ax.text(0, -60, "TATHĀTĀ: SINGULAR TRACE SECURED", color=C_MANTIS, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 75, "[ISOLATED WORLDLINE PHASE-LOCKED]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_CYAN if t_sec < 4.5 else (C_DIM if t_sec < 9.0 else (C_GOLD if t_sec < 14.8 else C_MANTIS))
    if is_tathata: ui_col = C_MANTIS

    ax.text(-140, 250, "LG-266b :: SINGULAR WORLDLINE AUDIT", color=txt_col, fontsize=19, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 238, "SYSTEM: ABSOLUTE ISOLATION / KINETIC VECTOR", color=txt_col, fontsize=9, fontname='monospace', zorder=80)

    obj_str = "THE SUBSTRATE STATIC [HIGH ENTROPY]"
    if 4.5 <= t_sec < 9.0: obj_str = "NUCLEATION [THE KINETIC CRUSH]"
    elif 9.0 <= t_sec < 14.8: obj_str = "THE BURNED TRACE [SINGULAR VECTOR]"
    elif is_tathata: obj_str = "O(1) RESOLUTION [BASEPLATE LOCKED]"

    ax.text(-140, -180, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)

    # Singular Trajectory Metric
    trace_metric = 0.0
    if 9.0 <= t_sec < 14.8: trace_metric = (t_sec - 9.0) / 5.8
    elif is_tathata: trace_metric = 1.0

    ax.text(-140, -205, "VECTOR EXHAUSTION [BURN TRACE]", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 3, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    tension_w = 280 * trace_metric
    ax.add_patch(plt.Rectangle((-140, -210), tension_w, 3, facecolor=C_TEXT if is_tathata else ui_col, zorder=81))

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
        drill_y = -300.0

        # Stable isometric camera
        cam_rx = np.pi/6 - (t_sec * 0.002)
        cam_ry = t_sec * 0.4 
        cam_rz = 0.0

        c_arr = np.zeros((MAX_PARTICLES, 3))
        s_arr = np.ones(MAX_PARTICLES) * 4.0
        a_arr = np.ones(MAX_PARTICLES) * 0.8

        curr_x = np.copy(px_base)
        curr_y = np.copy(py_base)
        curr_z = np.copy(pz_base)

        # -------------------------------------------------------------
        # THE WORLDLINE KINEMATICS
        # -------------------------------------------------------------
        if t_sec < 4.5:
            # PHASE 1: THE SUBSTRATE STATIC (Immediate Visual Impact)
            state = "PHASE 1 :: CHAOTIC POTENTIAL"

            # Violent, high-density jitter to ensure screen is not "empty"
            curr_y += np.sin(t_sec * 20.0 + curr_x * 0.1) * 20.0
            
            c_arr[noise_color == 0] = c_cyan
            c_arr[noise_color == 1] = c_magenta
            s_arr[:] = 5.0
            a_arr[:] = 0.7

        elif t_sec < 9.0:
            # PHASE 2: WORLDLINE NUCLEATION (The Kinetic Crush)
            state = "PHASE 2 :: THE BASEPLATE CRUSH"
            prog = (t_sec - 4.5) / 4.5
            accel = prog ** 3 

            # The entire 3D cloud violently flattens into the baseplate
            curr_y *= (1.0 - accel)

            # Colors wash out into the steel-grey substrate
            c_arr[noise_color == 0] = c_cyan * (1.0 - accel) + c_dim * accel
            c_arr[noise_color == 1] = c_magenta * (1.0 - accel) + c_dim * accel

            s_arr[:] = 5.0 - (accel * 3.0)
            a_arr[:] = 0.7 - (accel * 0.3)

        elif t_sec < 14.8:
            # PHASE 3: THE SINGULAR TRACE
            state = "PHASE 3 :: THE KINETIC WORLDLINE"
            prog = (t_sec - 9.0) / 5.8
            
            curr_y *= 0.0 # Grid is completely flat
            
            drill_y = -150.0 + (prog * 300.0) # Moves from bottom to top
            
            # Distance from the center Y-axis path
            dist_to_center = np.sqrt(curr_x**2 + curr_z**2)
            
            # The Relativistic Drill head (The Worldline Coordinate)
            drill_head = (dist_to_center < 15) & (np.abs(curr_y - drill_y) < 15) & (py_base < drill_y) 
            
            # The Burned Trace left behind 
            scorched_track = (dist_to_center < 12) & (py_base < drill_y)
            
            c_arr[:] = c_dim
            
            # Core Particle
            c_arr[drill_head] = c_gold
            s_arr[drill_head] = 10.0
            a_arr[drill_head] = 1.0
            
            # The permanent black burned trace
            c_arr[scorched_track & ~drill_head] = c_text
            a_arr[scorched_track & ~drill_head] = 0.95
            s_arr[scorched_track & ~drill_head] = 6.0

            if t_sec > 14.5:
                is_flash = True if f % 2 == 0 else False

        else:
            # PHASE 4: TATHĀTĀ (The Traced Path)
            state = "TATHĀTĀ :: SINGULAR PATH LOCKED"
            is_tathata = True

            curr_y *= 0.0
            drill_y = 150.0 # Locks at top
            
            dist_to_center = np.sqrt(curr_x**2 + curr_z**2)
            scorched_track = (dist_to_center < 12) & (py_base < drill_y)
            
            c_arr[:] = c_dim
            s_arr[:] = 2.0
            a_arr[:] = 0.4
            
            # The trace permanently hardens into MANTIS geometric proof
            c_arr[scorched_track] = c_mantis
            a_arr[scorched_track] = 1.0
            s_arr[scorched_track] = 6.0

            if t_sec < 14.95:
                is_flash = True

        # Apply Global Tensor Matrix
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)

        # For phase 3 & 4, remap the py_base to standard vertical Y projection so the track carves "Up" screen
        if t_sec >= 9.0:
            proj_x = rot_pts[:, 0]
            proj_y = py_base # Force the original distribution to act as the vertical plane
            z_depth = rot_pts[:, 2]
        else:
            proj_x = rot_pts[:, 0]
            proj_y = rot_pts[:, 1]
            z_depth = rot_pts[:, 2]

        yield (f, t_sec, state, proj_x, proj_y, z_depth, c_arr, s_arr, a_arr, drill_y, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 266b: THE SINGULAR TRACE [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Total Isolation Geometry & Substrate Contrast Boost")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Entwinement Geometry Eradicated. Trace is Singular.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
