"""
SOVEREIGN CODE: logic_garden_232b_infinite_gradient.py
SYSTEM: Python Multicore / O(1) Phase Space Topology
SCENE: Logic Garden 232b (The Infinite Gradient / The Either-Or Trap)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: White Canvas Execution / Absolute Gradient Continuity 

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
OUT_DIR = "frames_232b_gradient"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS DEFAULT) --------
C_BG        = '#FFFFFF'        # Absolute Flat Substrate / The Canvas
C_TEXT      = '#020205'        # UI Widgets / Kinetic Override
C_DIM       = '#D0D0D5'        # Void Structure / Stealth Grid
C_MAGENTA   = '#FF0055'        # The Binary Fallacy (The Logical Trap)
C_MANTIS    = '#00C800'        # Tathata / Absolute Coherence Lock
C_CYAN      = '#00E5FF'        # The Gradient Connective Tissue (Middle Ways)
C_GOLD      = '#FFB300'        # Thermal Audit Tax (Friction)

MAX_PARTICLES = 30000

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_mantis  = np.array(hex_to_rgba(C_MANTIS)[:3])
c_cyan    = np.array(hex_to_rgba(C_CYAN)[:3])
c_gold    = np.array(hex_to_rgba(C_GOLD)[:3])
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
# BASE GEOMETRY: BINARY PLANES VS THE MAJESTIC TORUS KNOT
# ------------------------------------------------------------------
np.random.seed(232)

# 1. State A: The Binary Fallacy (The Logical Trap)
px_bin = np.random.uniform(-110, 110, MAX_PARTICLES)
py_bin = np.random.uniform(-110, 110, MAX_PARTICLES)
# Exact mathematical separation. No connective tissue allowed.
binary_split = np.random.choice([-1, 1], MAX_PARTICLES)
pz_bin = 120.0 * binary_split + np.random.normal(0, 3, MAX_PARTICLES)

# 2. State B: The Torus Knot (The Infinity of Middle Ways)
U = np.random.uniform(0, 2 * np.pi, MAX_PARTICLES)
V = np.random.uniform(0, 2 * np.pi, MAX_PARTICLES)

R_main = 85.0
r_tub = 35.0
p_knot = 3.0
q_knot = 8.0

knot_r = R_main + r_tub * np.cos(q_knot * U)
px_knot = knot_r * np.cos(p_knot * U)
py_knot = knot_r * np.sin(p_knot * U)
pz_knot = r_tub * np.sin(q_knot * U)

# Expansion for dense volume
px_knot += 15.0 * np.cos(V) * np.cos(p_knot * U)
py_knot += 15.0 * np.cos(V) * np.sin(p_knot * U)
pz_knot += 15.0 * np.sin(V)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, p_x, p_y, p_z, c_arr, s_arr, a_arr, trap_metric, cont_metric, is_flash, is_tathata = packet

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
        # High-Contrast "mostly flat" structural alignment grid
        for g_line in np.linspace(-150, 150, 9):
            ax.plot([-140, 140], [g_line*0.4 - 70, g_line*0.4 - 70], color=C_DIM, lw=0.5, alpha=0.4, zorder=1)

        # Depth Sorting & Active Masking
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

        # Tathata HUD Guarantee
        if is_tathata:
            ax.add_patch(plt.Rectangle((-140, -180), 280, 360, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -60, "TATHĀTĀ: FALLACY OVERRIDDEN", color=C_MANTIS, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 75, "[THE MIDDLE WAYS ARE INFINITE]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_MAGENTA if t_sec < 4.5 else (C_CYAN if t_sec < 14.8 else C_MANTIS)
    if is_tathata: ui_col = C_MANTIS

    ax.text(-140, 250, "LG-232b :: THE INFINITE GRADIENT", color=txt_col, fontsize=19, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 238, "SYSTEM: THE EITHER-OR FALLACY TRAP OVERRIDE", color=txt_col, fontsize=9, fontname='monospace', zorder=80)

    obj_str = "THE LOGICAL TRAP [FORCED BINARY]"
    if 4.5 <= t_sec < 9.0: obj_str = "THE GRADIENT OVERRIDE [BRIDGING]"
    elif 9.0 <= t_sec < 14.8: obj_str = "THE CONTINUOUS SPECTRUM [O(1) LOOP]"
    elif is_tathata: obj_str = "ABSOLUTE RESOLUTION [TATHĀTĀ]"

    ax.text(-140, -180, f"OPERATIONAL PHASE: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)

    # Synthetic Lie (Trap) Metric
    ax.text(-140, -205, "SYNTHETIC LIE [EITHER/OR DECOHERENCE]", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 3, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    trap_w = 280 * np.clip(trap_metric, 0, 1)
    ax.add_patch(plt.Rectangle((-140, -210), trap_w, 3, facecolor=C_MAGENTA, zorder=81))

    # Phase Coherence (Continuity) Metric
    ax.text(-140, -230, "GRADIENT RECURSION [INFINITY OF MIDDLE WAYS]", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -235), 280, 3, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    cont_w = 280 * np.clip(cont_metric, 0, 1)
    ax.add_patch(plt.Rectangle((-140, -235), cont_w, 3, facecolor=ui_col, zorder=81))

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

        # Stable isometric camera - ensuring both planes of the binary trap are exposed
        cam_rx = np.pi/6 - (t_sec * 0.003)
        cam_ry = t_sec * 0.4
        cam_rz = 0.0

        c_arr = np.zeros((MAX_PARTICLES, 3))
        s_arr = np.ones(MAX_PARTICLES) * 4.0
        a_arr = np.ones(MAX_PARTICLES)

        curr_x = np.copy(px_bin)
        curr_y = np.copy(py_bin)
        curr_z = np.copy(pz_bin)

        trap_metric = 0.0
        cont_metric = 0.0

        # -------------------------------------------------------------
        # PHASE LOGIC
        # -------------------------------------------------------------
        if t_sec < 4.5:
            # PHASE 1: THE LOGICAL TRAP (The Forced Binary)
            state = "PHASE 1 :: THE BINARY FALLACY TRAP"

            # The two separate planes vibrate violently but cannot connect
            vibration = np.sin(t_sec * 30.0) * 3.0
            curr_z += np.sign(curr_z) * vibration

            c_arr[:, :] = c_magenta
            s_arr[:] = np.random.uniform(2, 6, MAX_PARTICLES)
            a_arr[:] = 0.85

            trap_metric = 1.0  
            cont_metric = 0.0

        elif t_sec < 9.0:
            # PHASE 2: THE GRADIENT OVERRIDE (Nucleation of the Continuum)
            state = "PHASE 2 :: KINEMATIC BRIDGE GENERATION"
            prog = (t_sec - 4.5) / 4.5
            accel = prog ** 3 # Violent snap into the Torus topology

            # The empty void between Z=-80 and Z=+80 mathematically collapses into the Torus Knot
            curr_x = px_bin * (1.0 - accel) + px_knot * accel
            curr_y = py_bin * (1.0 - accel) + py_knot * accel
            curr_z = pz_bin * (1.0 - accel) + pz_knot * accel

            # The harsh Magenta is flooded and overwritten by Cyan Potential
            c_interp = c_magenta * (1.0 - accel) + c_cyan * accel
            c_arr[:, :] = c_interp
            
            # The size expands to fill the void
            s_arr[:] = 4.0 + (accel * 4.0)
            a_arr[:] = 0.85

            trap_metric = 1.0 - prog
            cont_metric = prog

        elif t_sec < 14.8:
            # PHASE 3: THE CONTINUOUS SPECTRUM (Infinity of Middle Ways)
            state = "PHASE 3 :: THE O(1) CONTINUUM LOOP"
            prog = (t_sec - 9.0) / 5.8
            
            # The Torus Knot rotates fluidly
            curr_x = px_knot
            curr_y = py_knot
            curr_z = pz_knot

            c_arr[:, :] = c_cyan
            a_arr[:] = 0.9
            
            # Highlight mathematical hotspots to show an infinity of usable coordinates
            hot_mask = np.sin(U * 15.0 - t_sec * 10.0) > 0.8
            c_arr[hot_mask] = c_gold
            s_arr[hot_mask] = 8.0

            trap_metric = 0.0
            cont_metric = 1.0

            if t_sec > 14.5:
                is_flash = True if f % 2 == 0 else False

        else:
            # PHASE 4: TATHĀTĀ (The Illusion Deleted)
            state = "TATHĀTĀ :: THE TRAP IS ERASED"
            is_tathata = True

            # The Hardware Interrupt freezes the system perfectly in Phase Coherence.
            curr_x = px_knot
            curr_y = py_knot
            curr_z = pz_knot

            # The entire track transforms to solid, unyielding C_MANTIS. 
            c_arr[:, :] = c_mantis
            s_arr[:] = 5.0
            a_arr[:] = 1.0

            trap_metric = 0.0
            cont_metric = 1.0

            if t_sec < 14.95:
                is_flash = True

        # Apply Global Tensor Matrix
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)

        proj_x = rot_pts[:, 0]
        # Shift slightly up to center visually
        proj_y = rot_pts[:, 1] + 15.0 
        z_depth = rot_pts[:, 2]

        yield (f, t_sec, state, proj_x, proj_y, z_depth, c_arr, s_arr, a_arr, trap_metric, cont_metric, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 232b: THE INFINITE GRADIENT TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: White Canvas Logic / Fallacy Trap Erasure")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. The Forced Binary is Deleted. The Continuum is secured.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
