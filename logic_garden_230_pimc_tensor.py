"""
SOVEREIGN CODE: logic_garden_230_pimc_tensor.py
SYSTEM: Python Multicore / O(1) Path-Integral Matrix
SCENE: Logic Garden 230 (PIMC Finite Engine / Simulated Tunneling)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Undefined Palette Vector Restored (C_CYAN hardcoded)
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
OUT_DIR = "frames_230_pimc_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE AZURE / MAKO PALETTE (HIGH-COHERENCE / WHITE BG) --------
C_BG        = '#FFFFFF'        # Low-Entropy Canvas
C_TEXT      = '#020205'        # High-Contrast Data Load
C_DIM       = '#D0D0D5'        # QUBO Landscape / Penalty Barriers
C_AZURE     = '#007FFF'        # Trotter Replicas (Classical Clones)
C_CYAN      = '#00FFFF'        # Virtual Spring Matrix (Intermediate state)
C_INDIGO    = '#4B0082'        # Transverse Field / The Convergence Lock
C_MAGENTA   = '#FF0055'        # Thermal Friction / Massive GPU Burn
C_GOLD      = '#FFB300'        # The Compute Tax (Hardware Spallation)

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_azure   = np.array(hex_to_rgba(C_AZURE)[:3])
c_cyan    = np.array(hex_to_rgba(C_CYAN)[:3])
c_indigo  = np.array(hex_to_rgba(C_INDIGO)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
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
# BASE GEOMETRY ARRAYS: QUBO TOPOLOGY & TROTTER SLICES
# ------------------------------------------------------------------
np.random.seed(444)

# 1. The Classical Landscape (14,400 points)
GV = np.linspace(-130, 130, 120)
X, Y = np.meshgrid(GV, GV)
px_land = X.flatten()
py_land = Y.flatten()
# Deep penalty topology tracking toward global minimum at (0,0)
pz_land = (px_land**2 + py_land**2)*0.006 + 25.0 * np.cos(0.12 * px_land) + 25.0 * np.cos(0.12 * py_land) - 40.0

# 2. Imaginary Time Dimension (P = 60 Trotter Replicas, 10,800 points total)
P_SLICES = 60
N_PER_SLICE = 180
N_TROTTER = P_SLICES * N_PER_SLICE

tr_px = np.zeros(N_TROTTER)
tr_py = np.zeros(N_TROTTER)
tr_pz = np.zeros(N_TROTTER)

slice_angles = np.linspace(0, 2*np.pi, P_SLICES, endpoint=False)
for p in range(P_SLICES):
    ids = p * N_PER_SLICE
    ide = (p+1) * N_PER_SLICE
    # Create the virtual ring format
    tr_px[ids:ide] = 85.0 * np.cos(slice_angles[p]) + np.random.normal(0, 2.5, N_PER_SLICE)
    tr_py[ids:ide] = 85.0 * np.sin(slice_angles[p]) + np.random.normal(0, 2.5, N_PER_SLICE)
    tr_pz[ids:ide] = 100.0 + np.random.normal(0, 2.5, N_PER_SLICE) # Suspended above reality

# Compile master array (25,200 points)
base_px = np.concatenate([px_land, tr_px])
base_py = np.concatenate([py_land, tr_py])
base_pz = np.concatenate([pz_land, tr_pz])
MAX_PARTICLES = len(base_px)

mask_land = np.arange(MAX_PARTICLES) < len(px_land)
mask_trotter = ~mask_land

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, proj_x, proj_y, z_depth, colors, sizes, tax_strain, is_flash, is_tathata = packet
    
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
        # Background Grid structure
        ax.add_patch(plt.Rectangle((-150, -250), 300, 500, facecolor='none', edgecolor=C_DIM, lw=1, alpha=0.3, zorder=1))

        # O(N) Depth Sorting
        sort_idx = np.argsort(z_depth)
        s_px = proj_x[sort_idx]
        s_py = proj_y[sort_idx]
        s_c = colors[sort_idx]
        s_s = sizes[sort_idx]

        ax.scatter(s_px, s_py, s=s_s, color=s_c, edgecolors='none', alpha=0.85, zorder=10)

        if is_tathata:
            ax.add_patch(plt.Rectangle((-40, -40), 80, 80, facecolor='none', edgecolor=C_INDIGO, lw=3, zorder=40))
            ax.text(0, -60, "TATHĀTĀ: REPLICA CONVERGENCE SECURED.", color=C_INDIGO, fontsize=10, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 50, "[GLOBAL MINIMUM ACCESSED]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_AZURE if t_sec < 4.5 else (C_CYAN if t_sec < 9.5 else C_MAGENTA)
    if is_flash: ui_col = C_BG
    if is_tathata: ui_col = C_INDIGO
    
    ax.text(-140, 240, "LG-230 :: THE PIMC TENSOR", color=txt_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: SIMULATED QUANTUM ANNEALING (SQA)", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    
    obj_str = "FLOOR 1: TROTTER SLICES (IMAGINARY TIME)"
    if 4.5 <= t_sec < 9.5: obj_str = "FLOOR 2: VIRTUAL SPRING MATRIX"
    elif 9.5 <= t_sec < 14.8: obj_str = "FLOOR 3: PIMC BRUTE-FORCE DEMON"
    elif is_tathata: obj_str = "FLOOR 4: REPLICA DIMENSION COLLAPSE"

    ax.text(-140, -180, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Thermodynamic Hardware Metric: The Compute Tax
    ax.text(-140, -205, "THERMODYNAMIC COMPUTE TAX (GPU BURN)", color=txt_col, fontsize=10, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    bar_w = 280 * np.clip(tax_strain, 0, 1)
    ax.add_patch(plt.Rectangle((-140, -210), bar_w, 4, facecolor=C_GOLD if t_sec >= 9.5 else ui_col, zorder=81))

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
        
        cam_rx = np.pi/6
        cam_ry = t_sec * 0.3
        cam_rz = 0.0
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 4.0
        
        curr_x = np.copy(base_px)
        curr_y = np.copy(base_py)
        curr_z = np.copy(base_pz)

        tax_strain = 0.05 
        
        # Landscape remains static and Dim
        colors[mask_land] = c_dim
        sizes[mask_land] = 1.0

        # -------------------------------------------------------------
        # SQA PHASE LOGIC
        # -------------------------------------------------------------
        if t_sec < 4.5:
            state = "REPLICA ANCHOR :: THE VIRTUAL DIMENSION"
            
            # Replicas float above the reality plane
            colors[mask_trotter] = c_azure
            sizes[mask_trotter] = 5.0
            
            tax_strain = 0.1 # Base power to generate Trotter slices

        elif t_sec < 9.5:
            state = "TRANSVERSE FIELD :: VIRTUAL SPRING TENSION"
            prog = (t_sec - 4.5) / 5.0
            accel = prog ** 2
            
            # Replicas are dropped onto the QUBO landscape
            t_x = curr_x[mask_trotter]
            t_y = curr_y[mask_trotter]
            land_floor = (t_x**2 + t_y**2)*0.006 + 25.0*np.cos(0.12*t_x) + 25.0*np.cos(0.12*t_y) - 40.0
            
            curr_z[mask_trotter] = base_pz[mask_trotter] * (1.0 - accel) + land_floor * accel
            
            # HOTFIX Enacted: c_cyan parameter valid
            colors[mask_trotter] = c_azure * (1.0 - accel) + c_cyan * accel
            sizes[mask_trotter] = 5.0
            
            tax_strain = 0.1 + (accel * 0.3)

        elif t_sec < 14.8:
            state = "SIMULATED TUNNELING :: MARKOV CHAIN EXECUTION"
            prog = (t_sec - 9.5) / 5.3
            if t_sec < 9.6: is_flash = True
            
            # The Monte Carlo steps. Replicas are violently yanked toward the center (0,0) global minimum.
            # They physically "tunnel" through the mathematical penalty barriers.
            t_x = curr_x[mask_trotter]
            t_y = curr_y[mask_trotter]
            
            # Shrink the ring mathematically (Simulating Virtual Spring tension increasing)
            pull_r = 1.0 - (prog * 0.95)
            curr_x[mask_trotter] = t_x * pull_r
            curr_y[mask_trotter] = t_y * pull_r
            
            # Recalculate height logically
            c_x = curr_x[mask_trotter]
            c_y = curr_y[mask_trotter]
            curr_z[mask_trotter] = (c_x**2 + c_y**2)*0.006 + 25.0*np.cos(0.12*c_x) + 25.0*np.cos(0.12*c_y) - 40.0
            
            # MASSIVE COMPUTE TAX. The classical silicon burns electrical energy to fake the tunneling.
            spall_mag = 12.0 * np.abs(np.sin(t_sec * 15)) * prog
            fuzz_x = np.random.normal(0, spall_mag, N_TROTTER)
            fuzz_y = np.random.normal(0, spall_mag, N_TROTTER)
            fuzz_z = np.random.normal(0, spall_mag, N_TROTTER)
            
            curr_x[mask_trotter] += fuzz_x
            curr_y[mask_trotter] += fuzz_y
            curr_z[mask_trotter] += fuzz_z
            
            colors[mask_trotter] = c_cyan * (1.0 - prog) + c_magenta * prog
            # Gold spallation instances to represent thermal load
            burn_mask = np.random.rand(N_TROTTER) < (prog * 0.4)
            full_mask_idx = np.where(mask_trotter)[0]
            colors[full_mask_idx[burn_mask]] = c_gold
            
            sizes[mask_trotter] = 5.0 + (prog * 5.0)
            
            tax_strain = 0.5 + (0.5 * np.abs(np.sin(t_sec * 15))) # Hardware redlined

        else:
            state = "TATHĀTĀ :: THE CLASSICAL CONVERGENCE"
            is_tathata = True
            
            # The virtual springs tighten to absolute infinity. 
            # The Imaginary Time dimension collapses. 
            # All 60 Trotter replicas snap into the exact same physical coordinates at Global Minimum (0,0, -40 + 50 = 10)
            curr_x[mask_trotter] = 0.0 + np.random.normal(0, 5, N_TROTTER)
            curr_y[mask_trotter] = 0.0 + np.random.normal(0, 5, N_TROTTER)
            curr_z[mask_trotter] = 10.0 + np.random.normal(0, 5, N_TROTTER)
            
            colors[mask_trotter] = c_indigo
            sizes[mask_trotter] = 8.0
            
            tax_strain = 0.0 # Bounding box achieved. The algorithm is concluded.
            
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

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], colors[cull_mask], sizes[cull_mask], tax_strain, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 230: THE PIMC TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Variable Array Name Resolution (C_CYAN defined)")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Syntax Restored. Global Minimum Recovered.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
