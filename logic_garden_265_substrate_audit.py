"""
SOVEREIGN CODE: logic_garden_265_substrate_audit.py
SYSTEM: Python Multicore / O(1) Cosmological Index
SCENE: Logic Garden 265 (The Substrate Bill of Materials)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Inferred Telemetry LineCollection & Dark Sector Tension

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
OUT_DIR = "frames_265_substrate_audit"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS DEFAULT) --------
C_BG        = '#FFFFFF'        # Absolute Flat Substrate / The Canvas
C_TEXT      = '#020205'        # Dark Matter (The Invisible Rubber Band)
C_AZURE     = '#007FFF'        # Baryonic Matter (The Hardware)
C_MAGENTA   = '#FF0055'        # Antimatter (The Erasure Vector)
C_CYAN      = '#00E5FF'        # Dark Energy (The Faucet Expansion)
C_GOLD      = '#FFB300'        # The Photon (The Witness / Telemetry)
C_MANTIS    = '#00C800'        # Tathata Phase-Lock / Equilibrium
C_DIM       = '#D0D0D5'        # Void Stealth Grid

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_azure   = np.array(hex_to_rgba(C_AZURE)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_cyan    = np.array(hex_to_rgba(C_CYAN)[:3])
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
np.random.seed(265)
MAX_PARTICLES = 25000

# Baryonic Cloud (Matter & Antimatter mixed at the origin)
r_base = np.random.uniform(5, 60, MAX_PARTICLES)
theta_base = np.random.uniform(0, 2*np.pi, MAX_PARTICLES)
phi_base = np.arccos(np.random.uniform(-1, 1, MAX_PARTICLES))

px_base = r_base * np.sin(phi_base) * np.cos(theta_base)
py_base = r_base * np.cos(phi_base)
pz_base = r_base * np.sin(phi_base) * np.sin(theta_base)

# Identity arrays for the Bill of Materials
baryon_mask = np.random.choice([True, False], MAX_PARTICLES) # True = Matter, False = Antimatter
photon_mask = np.random.rand(MAX_PARTICLES) > 0.95 # 5% of particles function as Photons

# Tether Anchor Array for Dark Matter tension mapping
tether_mask = np.random.rand(MAX_PARTICLES) > 0.90 

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, p_x, p_y, p_z, c_arr, s_arr, a_arr, t_lines, dm_alpha, de_glow, is_flash, is_tathata = packet

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

        # Dark Energy Repulsion / Expansion Glow
        if de_glow > 0 and not is_tathata:
            ax.add_patch(plt.Circle((0, 0), de_glow * 180, color=C_CYAN, alpha=de_glow*0.15, zorder=2))

        # Dark Matter (The Invisible Rubber Band) LineCollection
        if len(t_lines) > 0 and dm_alpha > 0:
            lc_col = np.array([c_text[0], c_text[1], c_text[2], dm_alpha])
            lc = LineCollection(t_lines, colors=[lc_col]*len(t_lines), linewidths=0.8, zorder=3)
            ax.add_collection(lc)

        # Depth Sorting & Active Masking for Particles (Baryonic + Photons)
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
            ax.text(0, -60, "TATHĀTĀ: EQUILIBRIUM OF THE UNSEEN", color=C_MANTIS, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 75, "[DARK TENSION = EXPANSION PRESSURE]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_MAGENTA if t_sec < 4.5 else (C_CYAN if t_sec < 9.0 else (C_GOLD if t_sec < 14.8 else C_MANTIS))
    if is_tathata: ui_col = C_MANTIS

    ax.text(-140, 250, "LG-265 :: SUBSTRATE BILL OF MATERIALS", color=txt_col, fontsize=19, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 238, "SYSTEM: MHI-SPEC INFERRED TELEMETRY AUDIT", color=txt_col, fontsize=9, fontname='monospace', zorder=80)

    obj_str = "THE HARDWARE CONFLICT [M + M-BAR]"
    if 4.5 <= t_sec < 9.0: obj_str = "THE TOPOLOGICAL WAR [EXPANSION VS TETHER]"
    elif 9.0 <= t_sec < 14.8: obj_str = "INFERRED TELEMETRY [THE PHOTON WITNESS]"
    elif is_tathata: obj_str = "PERFECT EQUILIBRIUM [THE GROUNDED TRACE]"

    ax.text(-140, -180, f"OPERATIONAL PHASE: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)

    # Dark Sector Tension Metric
    ax.text(-140, -205, "DARK SECTOR TENSION [DM PULL vs DE PUSH]", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 3, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    tension_w = 280 * np.clip(dm_alpha, 0, 1)
    ax.add_patch(plt.Rectangle((-140, -210), tension_w, 3, facecolor=C_TEXT if dm_alpha > 0.2 else ui_col, zorder=81))

    # Baryonic Information Visibility (Dips as Photons take over)
    ax.text(-140, -230, "BARYONIC TRACE VISIBILITY [THE 5% HORIZON]", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -235), 280, 3, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    
    vis_val = 1.0
    if 9.0 <= t_sec < 14.8:
        vis_val = 1.0 - np.clip((t_sec - 9.0)/2.0, 0, 0.95)
    elif is_tathata: 
        vis_val = 0.05

    vis_w = 280 * vis_val
    ax.add_patch(plt.Rectangle((-140, -235), vis_w, 3, facecolor=C_AZURE if t_sec < 14.8 else ui_col, zorder=81))

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

        # Stable observer camera. Monitoring the Bounding Box.
        cam_rx = np.pi/7 - (t_sec * 0.002)
        cam_ry = t_sec * 0.3
        cam_rz = 0.0

        c_arr = np.zeros((MAX_PARTICLES, 3))
        s_arr = np.ones(MAX_PARTICLES) * 4.0
        a_arr = np.ones(MAX_PARTICLES)

        curr_x = np.copy(px_base)
        curr_y = np.copy(py_base)
        curr_z = np.copy(pz_base)

        t_lines = []
        dm_alpha = 0.0
        de_glow = 0.0

        # -------------------------------------------------------------
        # PHASE LOGIC
        # -------------------------------------------------------------
        if t_sec < 4.5:
            # PHASE 1: THE HARDWARE CONFLICT (Matter vs Antimatter)
            state = "PHASE 1 :: RECIPROCAL ERASURE COMBAT"

            # Intense high-friction collision at origin
            curr_x += np.random.normal(0, 3, MAX_PARTICLES)
            curr_y += np.random.normal(0, 3, MAX_PARTICLES)
            curr_z += np.random.normal(0, 3, MAX_PARTICLES)

            c_arr[baryon_mask] = c_azure
            c_arr[~baryon_mask] = c_magenta
            
            # Photons are dormant during raw hardware combat
            c_arr[photon_mask] = c_gold
            a_arr[photon_mask] = 0.2

            dm_alpha = 0.0 

        elif t_sec < 9.0:
            # PHASE 2: THE TOPOLOGICAL WAR (Dark Energy Push vs Dark Matter Pull)
            state = "PHASE 2 :: EXPANSION VS CAUSAL TETHERS"
            prog = (t_sec - 4.5) / 4.5
            accel = prog ** 2 

            # Dark Energy physically expands the universe array violently
            exp_factor = 1.0 + (accel * 4.0)
            curr_x *= exp_factor
            curr_y *= (1.0 + accel * 1.5)
            curr_z *= exp_factor

            # Dark Matter Tethers snap onto the grid to hold the array together
            dm_alpha = prog

            # Baryonic components maintain state, but spread out
            c_arr[baryon_mask] = c_azure
            c_arr[~baryon_mask] = c_magenta
            
            c_arr[photon_mask] = c_gold
            a_arr[photon_mask] = 0.5 + (0.5*prog)
            
            de_glow = prog

        elif t_sec < 14.8:
            # PHASE 3: INFERRED TELEMETRY (The Photon Witness)
            state = "PHASE 3 :: THE OBSERVATIONAL HORIZON"
            prog = (t_sec - 9.0) / 5.8
            
            exp_factor = 5.0 + (prog * 2.0)
            curr_x *= exp_factor
            curr_y *= 2.5
            curr_z *= exp_factor

            # Baryonic matter (The 5%) fades out as the gap becomes too vast
            fade_alpha = max(0.05, 1.0 - (prog * 3.0)) # Drops fast 
            a_arr[~photon_mask] = fade_alpha

            c_arr[baryon_mask] = c_azure
            c_arr[~baryon_mask] = c_magenta

            # The Photons (C_GOLD) become the ONLY highly visible signal
            c_arr[photon_mask] = c_gold
            a_arr[photon_mask] = 1.0
            s_arr[photon_mask] = 8.0 # High Yield Sparkle
            
            # Simulated photon travel (zipping along tension lines)
            curr_y[photon_mask] += np.sin(t_sec * 20.0) * 30.0

            dm_alpha = 1.0
            de_glow = 1.0 - prog

            if t_sec > 14.5:
                is_flash = True if f % 2 == 0 else False

        else:
            # PHASE 4: TATHĀTĀ (Perfect Equilibrium)
            state = "TATHĀTĀ :: THE UNSEEN IS BALANCED"
            is_tathata = True

            # The Hardware Interrupt locks the expansion. Push = Pull.
            exp_factor = 7.0 
            curr_x *= exp_factor
            curr_y *= 2.5
            curr_z *= exp_factor

            # Absolute minimal baryonic trace
            a_arr[~photon_mask] = 0.05
            c_arr[baryon_mask] = c_dim
            c_arr[~baryon_mask] = c_dim

            # Photons lock and shift to Mantis 
            c_arr[photon_mask] = c_mantis
            s_arr[photon_mask] = 6.0
            a_arr[photon_mask] = 1.0

            dm_alpha = 1.0
            de_glow = 0.0

            if t_sec < 14.95:
                is_flash = True

        # Apply Global Tensor Matrix
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)

        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1] + 10.0 
        z_depth = rot_pts[:, 2]

        # Process Dark Matter Tethers 
        if dm_alpha > 0.0:
            tx = proj_x[tether_mask]
            ty = proj_y[tether_mask]
            # Dark Matter Tethers link outer nodes back to the Faucet Singularity Origin (0,0)
            t_lines = [[[0.0, 10.0], [tx[i], ty[i]]] for i in range(len(tx))]

        yield (f, t_sec, state, proj_x, proj_y, z_depth, c_arr, s_arr, a_arr, t_lines, dm_alpha, de_glow, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 265: THE SUBSTRATE BILL OF MATERIALS [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Dark Sector Tension Matrices & Inferred Telemetry Overlays")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Baryonic Illusion Stripped. Equilibrium Anchored.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
