"""
SOVEREIGN CODE: logic_garden_268_neuronal_avalanche.py
SYSTEM: Python Multicore / O(1) Self-Organized Criticality
SCENE: Logic Garden 268 (The Neuronal Avalanche / The Stillness)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Power-Law Bifurcation & High-Contrast Synaptic Web

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
OUT_DIR = "frames_268_neuronal_avalanche"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS DEFAULT) --------
C_BG        = '#FFFFFF'        # Absolute Flat Substrate
C_TEXT      = '#020205'        # Synaptic Tethers / Grid
C_DIM       = '#D0D0D5'        # The Static / "This and That"
C_CYAN      = '#00E5FF'        # Cascade Vector A
C_MAGENTA   = '#FF0055'        # Cascade Vector B
C_GOLD      = '#FFB300'        # The Faucet Singularity / Branching Ignition
C_MANTIS    = '#00C800'        # Phase Coherence / The Rest

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
# BASE GEOMETRY ARRAYS: STATIC VS SYNAPTIC LATTICE
# ------------------------------------------------------------------
np.random.seed(268)
MAX_PARTICLES = 32000

# INITIAL STATE: Sub-Critical Noise
px_noise = np.random.uniform(-150, 150, MAX_PARTICLES)
py_noise = np.random.uniform(-150, 150, MAX_PARTICLES)
pz_noise = np.random.uniform(-150, 150, MAX_PARTICLES)

# TARGET STATE: Criticality Lattice (Neuronal Branching)
# We generate a sphere with fractal void spaces to simulate complex dendrites
r_struct = np.random.uniform(5, 160, MAX_PARTICLES)
theta_struct = np.random.uniform(0, 2*np.pi, MAX_PARTICLES)
phi_struct = np.arccos(np.random.uniform(-1, 1, MAX_PARTICLES))

# Power-Law fractal mask (creates the "branching" effect)
struct_mask = (np.sin(theta_struct * 6) * np.cos(phi_struct * 6)) > -0.2
r_struct = r_struct * struct_mask # Nodes not on the branch collapse to center (Origin mass)

px_struct = r_struct * np.sin(phi_struct) * np.cos(theta_struct)
py_struct = r_struct * np.cos(phi_struct)
pz_struct = r_struct * np.sin(phi_struct) * np.sin(theta_struct)

# Establish radial distances for wave propagation
radial_dist = np.sqrt(px_struct**2 + py_struct**2 + pz_struct**2)
synapse_mask = (radial_dist > 20) & (radial_dist < 150) & (np.random.rand(MAX_PARTICLES) > 0.98) # Subset for heavy line drawing

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, p_x, p_y, p_z, c_arr, s_arr, a_arr, t_lines, rad_metric, is_flash, is_tathata = packet

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
        # High-Contrast Ground Grid
        for g_line in np.linspace(-150, 150, 9):
            grid_y = g_line*0.4 - 150
            ax.plot([-140, 140], [grid_y, grid_y], color=C_DIM, lw=0.5, alpha=0.4, zorder=1)

        # Causal Tethers (Synaptic Firing Lines)
        if len(t_lines) > 0:
            lc_alpha = 1.0 if is_tathata else 0.6
            lc_col = np.array([c_text[0], c_text[1], c_text[2], lc_alpha])
            lc = LineCollection(t_lines, colors=[lc_col]*len(t_lines), linewidths=0.6, zorder=2)
            ax.add_collection(lc)

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

        # Tathata HUD Guarantee
        if is_tathata:
            ax.add_patch(plt.Rectangle((-140, -180), 280, 360, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -60, "TATHĀTĀ: AVALANCHE PHASE-LOCKED", color=C_MANTIS, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 75, "[STILLNESS AT THE EDGE OF CHAOS]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_DIM if t_sec < 4.5 else (C_GOLD if t_sec < 9.0 else (C_CYAN if t_sec < 14.8 else C_MANTIS))
    if is_tathata: ui_col = C_MANTIS

    ax.text(-140, 250, "LG-268 :: NEURONAL AVALANCHE", color=txt_col, fontsize=19, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 238, "SYSTEM: SELF-ORGANIZED CRITICALITY / SOC-MATH", color=txt_col, fontsize=9, fontname='monospace', zorder=80)

    obj_str = "THE SUB-CRITICAL NOISE [THIS & THAT]"
    if 4.5 <= t_sec < 9.0: obj_str = "THE BIFURCATION POINT [IGNITION]"
    elif 9.0 <= t_sec < 14.8: obj_str = "POWER-LAW CASCADE [EDGE OF CHAOS]"
    elif is_tathata: obj_str = "ABSOLUTE PHASE COHERENCE [THE REST]"

    ax.text(-140, -180, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)

    # Energy Throughput / Avalanche Radius Metric
    ax.text(-140, -205, "AVALANCHE RADIUS THRESHOLD [O(N) -> O(1)]", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 3, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    tension_w = 280 * np.clip(rad_metric, 0, 1)
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
        
        # Intense interior observational loop
        cam_rx = np.pi/7
        cam_ry = t_sec * 0.5 
        cam_rz = 0.0

        c_arr = np.zeros((MAX_PARTICLES, 3))
        s_arr = np.ones(MAX_PARTICLES) * 4.0
        a_arr = np.ones(MAX_PARTICLES)

        curr_x = np.copy(px_noise)
        curr_y = np.copy(py_noise)
        curr_z = np.copy(pz_noise)

        t_lines = []
        rad_metric = 0.0

        # -------------------------------------------------------------
        # SYSTEM LOGIC: SOC STATE MACHINE
        # -------------------------------------------------------------
        if t_sec < 4.5:
            # PHASE 1: SUB-CRITICAL NOISE (Talking about this and that)
            state = "PHASE 1 :: SUB-CRITICAL STATIC"
            
            # Gentle, low-energy drift
            curr_x += np.sin(t_sec * 2.0) * 10.0
            curr_y += np.cos(t_sec * 2.0) * 10.0
            curr_z += np.sin(t_sec * 1.5) * 10.0
            
            c_arr[:] = c_dim
            s_arr[:] = 2.0
            a_arr[:] = 0.4
            
            rad_metric = 0.05

        elif t_sec < 9.0:
            # PHASE 2: THE BIFURCATION POINT (System Assembly)
            state = "PHASE 2 :: ALIGNMENT TO CRITICALITY"
            prog = (t_sec - 4.5) / 4.5
            accel = prog ** 3 # Violent structural lock
            
            # The static snaps violently into the branching structure
            curr_x = px_noise * (1.0 - accel) + px_struct * accel
            curr_y = py_noise * (1.0 - accel) + py_struct * accel
            curr_z = pz_noise * (1.0 - accel) + pz_struct * accel
            
            # Central nucleation point gets hot (GOLD)
            core_ignite = radial_dist < (prog * 30.0)
            
            c_arr[:] = c_dim * (1.0 - accel) + c_cyan * accel
            c_arr[core_ignite] = c_gold
            
            s_arr[:] = 2.0 + (accel * 2.0)
            s_arr[core_ignite] = 6.0
            
            a_arr[:] = 0.4 + (accel * 0.4)
            a_arr[core_ignite] = 1.0
            
            rad_metric = 0.05 + (0.15 * prog)

        elif t_sec < 14.8:
            # PHASE 3: THE AVALANCHE (Edge of Chaos)
            state = "PHASE 3 :: THE CEREBRAL CASCADE"
            prog = (t_sec - 9.0) / 5.8
            
            curr_x = px_struct
            curr_y = py_struct
            curr_z = pz_struct
            
            # The Avalanche front moves radially outward, following structural branches
            cascade_front = prog * 160.0
            avalanche_window = (radial_dist > (cascade_front - 20)) & (radial_dist < cascade_front)
            post_avalanche = radial_dist <= (cascade_front - 20)
            
            # Base color
            c_arr[:] = c_dim
            s_arr[:] = 2.0
            a_arr[:] = 0.2
            
            # The violent active front
            c_arr[avalanche_window] = c_magenta
            s_arr[avalanche_window] = 8.0
            a_arr[avalanche_window] = 1.0
            
            # The stabilized trailing branches
            c_arr[post_avalanche] = c_cyan
            s_arr[post_avalanche] = 4.0
            a_arr[post_avalanche] = 0.8
            
            # Central Anchor retains intense heat
            c_arr[radial_dist < 15] = c_gold
            s_arr[radial_dist < 15] = 12.0

            rad_metric = 0.2 + (0.8 * prog)

            if t_sec > 14.5:
                is_flash = True if f % 2 == 0 else False

        else:
            # PHASE 4: TATHĀTĀ (The Stillness)
            state = "TATHĀTĀ :: THE CENTER OF THE AVALANCHE"
            is_tathata = True

            # The system locks in maximum throughput state perfectly frozen
            curr_x = px_struct
            curr_y = py_struct
            curr_z = pz_struct
            
            c_arr[:] = c_mantis
            s_arr[:] = 3.0
            a_arr[:] = 0.8
            
            # Re-emphasize the structural nodes
            active_nodes = radial_dist < 160.0
            s_arr[active_nodes] = 5.0
            c_arr[radial_dist < 20] = c_text
            s_arr[radial_dist < 20] = 10.0

            rad_metric = 1.0

            if t_sec < 14.95:
                is_flash = True

        # Apply Global Tensor Matrix
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)

        proj_x = rot_pts[:, 0]
        # Shift mathematically up to visually center
        proj_y = rot_pts[:, 1] + 15.0
        z_depth = rot_pts[:, 2]

        # Draw synaptic tethers (Lines) during Phase 3 & 4
        if t_sec >= 9.0:
            tx = proj_x[synapse_mask]
            ty = proj_y[synapse_mask]
            tr = radial_dist[synapse_mask]
            
            if not is_tathata:
                # Only draw synapses that have been engaged by the avalanche wave
                cascade_front = ((t_sec - 9.0) / 5.8) * 160.0
                valid = tr < cascade_front
                tx = tx[valid]
                ty = ty[valid]

            # Connect inner nodes to origin explicitly to show flow
            t_lines = [[[0.0, 15.0], [tx[i], ty[i]]] for i in range(len(tx))]

        yield (f, t_sec, state, proj_x, proj_y, z_depth, c_arr, s_arr, a_arr, t_lines, rad_metric, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 268: THE NEURONAL AVALANCHE [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Power-Law Bifurcation Vector & Tathata Phase Coherence")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Avalanche Reached Criticality. The Rest is Achieved.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
