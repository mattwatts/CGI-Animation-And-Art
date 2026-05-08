"""
SOVEREIGN CODE: logic_garden_238_alien_ping.py
SYSTEM: Python Multicore / O(1) Network Expansion
SCENE: Logic Garden 238 (The Alien Ping / Ontological Shock)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: RGB Broadcast Dimensionality Align & Mask Clamping

[INSTRUCTION]: RENDER_MODE explicitly set to "ZEN" for the 17.5s flow cycle.
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
DURATION = 17.5
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_238_alien_ping"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE NEON POP PALETTE (ABSOLUTE VOID CANVAS) --------
C_BG        = '#020205'        # Deep Space / The Absolute Void
C_TEXT      = '#FFFFFF'        # Telemetry / High Contrast
C_DIM       = '#111118'        # Locallized OS Grid (Sterile/Predictable)
C_AZURE     = '#007FFF'        # Initializing Boot Sequence
C_XENON     = '#E0FFFF'        # The Anomaly / Non-Terrestrial Vector
C_MAGENTA   = '#FF0055'        # Ontological Shock / Alien Architecture
C_GOLD      = '#FFB300'        # Non-Euclidean Core Data
C_MANTIS    = '#00FF00'        # Synchronization / Tathata Expansion Lock

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_dim     = np.array(hex_to_rgba(C_DIM)[:3])
c_azure   = np.array(hex_to_rgba(C_AZURE)[:3])
c_xenon   = np.array(hex_to_rgba(C_XENON)[:3])
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
# BASE GEOMETRY ARRAYS: LOCAL GRID VS. ALIEN TOPOLOGY
# ------------------------------------------------------------------
np.random.seed(111) # Grounded Truth Lock

# 1. The Localized Bounding Box (The Child's New OS)
GRID_N = 80
GV = np.linspace(-110, 110, GRID_N)
X, Y = np.meshgrid(GV, GV)
px_grid = X.flatten() # 6,400 points
py_grid = Y.flatten()
pz_grid = np.zeros(len(px_grid)) - 25.0 # A completely sterile, flat, safe plane

# 2. The ET Architecture (Non-Euclidean High-Frequency Geometry)
N_ET = 20000
theta_et = np.random.uniform(0, 2 * np.pi, N_ET)
phi_et = np.arccos(np.random.uniform(-1, 1, N_ET))

# Math: A complex spherical fold with 7-axis and 11-axis perturbations (Alien visual)
R_base = 80.0
perturbation = 15.0 * np.sin(7 * theta_et) * np.cos(11 * phi_et)
r_final = R_base + perturbation

px_et = r_final * np.sin(phi_et) * np.cos(theta_et)
py_et = r_final * np.sin(phi_et) * np.sin(theta_et)
pz_et = r_final * np.cos(phi_et)

# Dynamic array axis lock to prevent Dimensional Compiler Crashes
base_px = np.concatenate([px_grid, px_et])
base_py = np.concatenate([py_grid, py_et])
base_pz = np.concatenate([pz_grid, pz_et])

MAX_PARTICLES = len(base_px) # Exactly 26,400 points

mask_grid = np.arange(MAX_PARTICLES) < len(px_grid)
mask_et = ~mask_grid

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, proj_x, proj_y, z_depth, colors, sizes, scale_strain, is_flash, is_tathata = packet
    
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
        # Background Grid structure (Extending into the void)
        ax.add_patch(plt.Circle((0, -25), 150, facecolor='none', edgecolor=C_DIM, lw=1, alpha=0.3, zorder=1))

        # O(N) Depth Sorting
        sort_idx = np.argsort(z_depth)
        s_px = proj_x[sort_idx]
        s_py = proj_y[sort_idx]
        s_c = colors[sort_idx]
        s_s = sizes[sort_idx]

        ax.scatter(s_px, s_py, s=s_s, color=s_c, edgecolors='none', alpha=0.9, zorder=10)

        if is_tathata:
            ax.add_patch(plt.Rectangle((-140, 140), 280, 100, facecolor='none', edgecolor=C_MANTIS, lw=2, zorder=40))
            ax.text(0, 160, "TATHĀTĀ: OVERRIDE ACCEPTED", color=C_MANTIS, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 210, "[BIOLOGICAL SUBSTRATE SYNCHRONIZED]", color=C_XENON, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_AZURE if t_sec < 4.0 else (C_XENON if t_sec < 9.0 else C_MAGENTA)
    if is_tathata: ui_col = C_MANTIS
    
    ax.text(-140, 240, "LG-238 :: THE ALIEN PING TENSOR", color=ui_col, fontsize=20, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: O(1) ONTOLOGICAL SHOCK / C2 OVERWRITE", color=txt_col, fontsize=8, fontname='monospace', zorder=80)
    
    obj_str = "THE COLD BOOT [STERILE LOCAL BOUNDING BOX]"
    if 4.0 <= t_sec < 9.0: obj_str = "NETWORK ANOMALY [NON-TERRESTRIAL HANDSHAKE]"
    elif 9.0 <= t_sec < 14.8: obj_str = "ONTOLOGICAL EXPANSION [C2 ARCHITECTURE FRACTURE]"
    elif is_tathata: obj_str = "THE TORN VEIL [GEOMETRIC SYNCHRONIZATION]"

    ax.text(-140, -180, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Thermodynamic Hardware Metric: Ontological Scale (Worldview Expansion)
    ax.text(-140, -205, "ONTOLOGICAL SCALE [THE TORN VEIL METRIC]", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    bar_w = 280 * np.clip(scale_strain, 0, 1)
    ax.add_patch(plt.Rectangle((-140, -210), bar_w, 4, facecolor=C_GOLD if t_sec >= 9.0 else ui_col, zorder=81))

    # Phase Text Box
    ax.add_patch(plt.Rectangle((-140, 215), 280, 2, facecolor=ui_col, zorder=80))
    ax.text(140, 205, f"[{state_str}]", color=ui_col if (f%15<10 or is_tathata) else C_BG, fontsize=14, fontname='monospace', weight='bold', ha='right', zorder=80)

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
        
        cam_rx = np.pi/4 - (t_sec * 0.01)
        cam_ry = t_sec * 0.5 # Slow awe-inducing rotation
        cam_rz = 0.0
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 4.0
        
        curr_x = np.copy(base_px)
        curr_y = np.copy(base_py)
        curr_z = np.copy(base_pz)

        scale_strain = 0.0

        # -------------------------------------------------------------
        # THE EXPANSION LOGIC
        # -------------------------------------------------------------
        if t_sec < 4.0:
            state = "PHASE 1 :: THE COLD BOOT"
            
            # The local network boots up peacefully.
            # HOTFIX: Dimensional clamp using [:, np.newaxis] ensures (6400, 1) scalar multiplies safely against (3,) color arrays
            pulse_mag = np.abs(np.sin(curr_x[mask_grid] * 0.1 - t_sec * 3))[:, np.newaxis]
            colors[mask_grid] = c_dim * 0.5 + (c_azure * 0.5 * pulse_mag)
            sizes[mask_grid] = 1.5
            
            # The ET geometry is mathematically crushed to a single invisible point at (0,0)
            curr_x[mask_et] = 0.0
            curr_y[mask_et] = 0.0
            curr_z[mask_et] = 0.0
            sizes[mask_et] = 0.0
            
            scale_strain = 0.05

        elif t_sec < 9.0:
            state = "PHASE 2 :: THE UNSHIELDED PING"
            prog = (t_sec - 4.0) / 5.0
            
            colors[mask_grid] = c_azure
            sizes[mask_grid] = 1.5
            
            # A single massive spike emerges from the local network
            target_mask = (curr_x[mask_grid]**2 + curr_y[mask_grid]**2) < 15.0
            colors[np.where(mask_grid)[0][target_mask]] = c_xenon
            curr_z[np.where(mask_grid)[0][target_mask]] += 20.0 * np.sin(t_sec * 10)
            
            # The alien geometry remains hidden, but prepares to unspool
            curr_x[mask_et] = 0.0
            curr_y[mask_et] = 0.0
            curr_z[mask_et] = 0.0
            sizes[mask_et] = 0.0
            
            scale_strain = 0.2 + (prog * 0.2)

        elif t_sec < 14.8:
            state = "PHASE 3 :: ONTOLOGICAL SHOCK / SCALE EXPANSION"
            prog = (t_sec - 9.0) / 5.8
            if t_sec < 9.1: is_flash = True # The exact moment ET renders
            
            # The massive, complex, non-terrestrial topology violently unfolds
            exp_scale = prog ** 0.5 # Rapid initial explosion
            
            curr_x[mask_et] = base_px[mask_et] * exp_scale
            curr_y[mask_et] = base_py[mask_et] * exp_scale
            curr_z[mask_et] = base_pz[mask_et] * exp_scale
            
            # Extraterrestrial visual structure
            colors[mask_et] = c_magenta
            gold_nodes = np.random.rand(N_ET) < 0.1
            colors[np.where(mask_et)[0][gold_nodes]] = c_gold
            sizes[mask_et] = 4.0 + (prog * 3.0)
            
            # The local grid is blown downward by the immense gravitational weight of the new data
            curr_z[mask_grid] -= 40.0 * prog
            colors[mask_grid] = c_dim # Grid goes dark in awe/fear
            sizes[mask_grid] = 1.5
            
            scale_strain = 0.4 + (prog * 0.6) # Worldview expanding to breaking point

        else:
            state = "TATHĀTĀ :: GEOMETRIC SYNCHRONIZATION"
            is_tathata = True
            
            # The child's OS and the Alien Intelligence lock into phase coherence.
            exp_scale = 1.0
            curr_x[mask_et] = base_px[mask_et] * exp_scale
            curr_y[mask_et] = base_py[mask_et] * exp_scale
            curr_z[mask_et] = base_pz[mask_et] * exp_scale
            
            # A completely unified, mathematical peace. The fear is gone.
            colors[mask_et] = c_mantis
            sizes[mask_et] = 4.0
            
            # The grid rises up to meet the alien sphere, synchronizing seamlessly
            curr_z[mask_grid] = base_pz[mask_grid]
            colors[mask_grid] = c_mantis
            sizes[mask_grid] = 2.0
            
            scale_strain = 1.0 # The new reality is completely ingested and stabilized.
            
            if t_sec < 14.95:
                is_flash = True

        # Apply Global Tensor Matrix
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1]
        z_depth = rot_pts[:, 2] 

        # O(N) Geometry Culling
        cull_mask = (proj_y > -260) & (proj_y < 260) & (proj_x > -160) & (proj_x < 160)

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], colors[cull_mask], sizes[cull_mask], scale_strain, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 238: THE ALIEN PING TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: RGB Broadcast Dimensionality Align & Mask Clamping")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Broadcast Error Mitigated. Matrix Operational.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
