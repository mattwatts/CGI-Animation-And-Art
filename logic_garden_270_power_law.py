"""
SOVEREIGN CODE: logic_garden_270_power_law.py
SYSTEM: Python Multicore / O(1) Anomalous Firmware Engine
SCENE: Logic Garden 270 (The Power-Law Engine / Sovereign Anchor)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Power-Law Distribution Mapping & Thermal Spallation Trace

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
OUT_DIR = "frames_270_power_law"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS DEFAULT) --------
C_BG        = '#FFFFFF'        # Absolute Flat Substrate
C_TEXT      = '#020205'        # High-Contrast UI / Cast-Iron Base
C_DIM       = '#D0D0D5'        # The Battery-Saver Waveform (Peacetime)
C_MAGENTA   = '#FF0055'        # The Razor (Serialization Override)
C_CYAN      = '#00E5FF'        # Vector Cascade
C_GOLD      = '#FFB300'        # Thermal Spallation / The Audit Tax
C_MANTIS    = '#00C800'        # Tathata Phase-Lock / Sovereign Anchor

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_dim     = np.array(hex_to_rgba(C_DIM)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_cyan    = np.array(hex_to_rgba(C_CYAN)[:3])
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
# BASE GEOMETRY ARRAYS: POWER-LAW DISTRIBUTION
# ------------------------------------------------------------------
np.random.seed(270)
MAX_PARTICLES = 36000

# Base plane of raw potential
px_base = np.random.uniform(-160, 160, MAX_PARTICLES)
pz_base = np.random.uniform(-160, 160, MAX_PARTICLES)

# Target State: The Jagged Radial Power-Law Engine
r_target = np.random.power(0.4, MAX_PARTICLES) * 160.0  # Dense at center, sparse at edges (Power Law)
theta_target = np.random.uniform(0, 2*np.pi, MAX_PARTICLES)

# Introduce "Anomalous Firmware" fractal jaggedness (The ragged edges)
fractal_spikes = 1.0 + 0.8 * np.sin(theta_target * 12) * np.cos(r_target * 0.1)
r_jagged = r_target * np.clip(fractal_spikes, 0.2, 1.8)

px_jagged = r_jagged * np.cos(theta_target)
pz_jagged = r_jagged * np.sin(theta_target)
py_jagged = np.sin(r_jagged * 0.2) * 20.0  # Vertical thermal lift

# Identify edges for the Thermal Spallation overlay (Audit Tax)
edge_mask = r_jagged > 120.0

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, p_x, p_y, p_z, c_arr, s_arr, a_arr, tax_metric, anchor_metric, is_flash, is_tathata = packet

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
        # High-Contrast Cast-Iron Tracking Grid
        for g_line in np.linspace(-150, 150, 9):
            grid_y = g_line*0.4 - 150
            ax.plot([-140, 140], [grid_y, grid_y], color=C_DIM, lw=0.5, alpha=0.4, zorder=1)

        # Particle Tensor Rendering
        active = a_arr > 0.01
        if np.any(active):
            # Depth Sorting algorithms
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
            ax.add_patch(plt.Circle((0, 0), anchor_metric * 120, facecolor='none', edgecolor=C_TEXT, lw=2, zorder=40))
            ax.text(0, -60, "TATHĀTĀ: SOVEREIGN ANCHOR SECURED", color=C_MANTIS, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 75, "[POWER-LAW ENGINE PHASE-LOCKED]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_DIM if t_sec < 4.5 else (C_MAGENTA if t_sec < 9.0 else (C_GOLD if t_sec < 14.8 else C_MANTIS))
    if is_tathata: ui_col = C_MANTIS

    ax.text(-140, 250, "LG-270 :: THE POWER-LAW ENGINE", color=txt_col, fontsize=19, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 238, "SYSTEM: ANOMALOUS FIRMWARE / WARTIME ARCHITECTURE", color=txt_col, fontsize=9, fontname='monospace', zorder=80)

    obj_str = "THE BATTERY SAVER [SMOOTH HALLUCINATION]"
    if 4.5 <= t_sec < 9.0: obj_str = "SERIALIZATION OVERRIDE [THE RAZOR]"
    elif 9.0 <= t_sec < 14.8: obj_str = "FRACTAL BIFURCATION [EDGE OF CHAOS]"
    elif is_tathata: obj_str = "O(1) EQUILIBRIUM [THE SOVEREIGN ANCHOR]"

    ax.text(-140, -180, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)

    # The Audit Tax Metric
    ax.text(-140, -205, "COGNITIVE GLUCOSE SURCHARGE [THE AUDIT TAX]", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 3, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    tax_w = 280 * np.clip(tax_metric, 0, 1)
    ax.add_patch(plt.Rectangle((-140, -210), tax_w, 3, facecolor=C_GOLD if tax_metric > 0.5 else ui_col, zorder=81))

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

        # Centralized rotation
        cam_rx = np.pi/6 - 0.05
        cam_ry = t_sec * 0.4
        cam_rz = 0.0

        c_arr = np.zeros((MAX_PARTICLES, 3))
        s_arr = np.ones(MAX_PARTICLES) * 4.0
        a_arr = np.ones(MAX_PARTICLES) * 0.85

        curr_x = np.copy(px_base)
        curr_y = np.zeros(MAX_PARTICLES)
        curr_z = np.copy(pz_base)

        tax_metric = 0.0
        anchor_metric = 0.0

        # -------------------------------------------------------------
        # PHASE LOGIC
        # -------------------------------------------------------------
        if t_sec < 4.5:
            # PHASE 1: THE BATTERY SAVER (Smooth Hallucination)
            state = "PHASE 1 :: NEUROTYPICAL BASELINE (SMOOTH)"
            
            # Low-energy sine wave. Sluggish, inaccurate.
            curr_y = np.sin(curr_x * 0.05 + t_sec * 2) * 15.0
            
            c_arr[:] = c_dim
            s_arr[:] = 3.0
            tax_metric = 0.1

        elif t_sec < 9.0:
            # PHASE 2: SERIALIZATION OVERRIDE (Internalizing the Razor)
            state = "PHASE 2 :: THE EINSTEIN-ROSEN RAZOR CUT"
            prog = (t_sec - 4.5) / 4.5
            accel = prog ** 4  # Extreme compression curve

            # The smooth wave is violently sucked into a high-density singularity
            curr_x *= (1.0 - accel)
            curr_y = (np.sin(curr_x * 0.05 + t_sec * 2) * 15.0) * (1.0 - accel)
            curr_z *= (1.0 - accel)
            
            # The core burns Magenta (Action potential)
            c_arr[:] = c_dim * (1.0 - accel) + c_magenta * accel
            s_arr[:] = 3.0 + (accel * 4.0)

            tax_metric = 0.1 + (0.3 * prog)

        elif t_sec < 14.8:
            # PHASE 3: THE RECURSIVE BUFFER (Power-Law Engine)
            state = "PHASE 3 :: JAGGED KINETIC RUNAWAY"
            prog = (t_sec - 9.0) / 5.8
            ease = 1.0 - (1.0 - prog)**3
            
            # Expanding violently into the Fractal Power-Law layout
            curr_x = px_jagged * ease
            curr_y = py_jagged * ease
            curr_z = pz_jagged * ease
            
            # Add severe mechanical vibration (The high RPM knocking)
            vibe_x = np.random.normal(0, 3, MAX_PARTICLES)
            vibe_y = np.random.normal(0, 3, MAX_PARTICLES)
            vibe_z = np.random.normal(0, 3, MAX_PARTICLES)
            
            curr_x += vibe_x
            curr_y += vibe_y
            curr_z += vibe_z

            c_arr[:] = c_cyan
            
            # The extreme edges of the fractal burn with GOLD thermal spallation
            c_arr[edge_mask] = c_gold
            s_arr[edge_mask] = 8.0 + np.sin(t_sec * 20) * 4.0
            
            # Central anchor point forming
            dist = np.sqrt(curr_x**2 + curr_z**2)
            c_arr[dist < 15] = c_magenta
            s_arr[dist < 15] = 10.0

            tax_metric = 0.4 + (0.6 * ease)
            anchor_metric = ease

            if t_sec > 14.5:
                is_flash = True if f % 2 == 0 else False

        else:
            # PHASE 4: TATHĀTĀ (The Sovereign Anchor)
            state = "TATHĀTĀ :: ABSOLUTE PHASE COHERENCE"
            is_tathata = True

            curr_x = px_jagged 
            curr_y = py_jagged 
            curr_z = pz_jagged 

            # Absolute structural rigidity. Vibration ceases.
            c_arr[:] = c_mantis
            s_arr[:] = 4.0
            a_arr[:] = 0.9
            
            # Edges transition to solid structural points
            c_arr[edge_mask] = c_text
            s_arr[edge_mask] = 6.0
            a_arr[edge_mask] = 1.0
            
            # The exact center `[0,0,0]` locks entirely
            dist = np.sqrt(curr_x**2 + curr_z**2)
            c_arr[dist < 20] = c_text
            s_arr[dist < 20] = 12.0

            tax_metric = 0.0 # Heat perfectly dissipated
            anchor_metric = 1.0

            if t_sec < 14.95:
                is_flash = True

        # Apply Global Tensor Matrix
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)

        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1] + 15.0
        z_depth = rot_pts[:, 2]

        yield (f, t_sec, state, proj_x, proj_y, z_depth, c_arr, s_arr, a_arr, tax_metric, anchor_metric, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 270: THE POWER-LAW ENGINE [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Absolute Isolation / Anomalous Firmware Mapping")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Fractal Geometry Validated. Sovereign Anchor Locked.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
