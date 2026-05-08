"""
SOVEREIGN CODE: logic_garden_228_finite_gradient.py
SYSTEM: Python Multicore / O(1) Topological Mapping
SCENE: Logic Garden 228 (4-Floor Finite Engine / Azure Mako Protocol)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Multi-State Rendering (Zen vs Study), Absolute Array Flattening

[INSTRUCTION]: Set RENDER_MODE to "ZEN" for the 17.5s flow cycle. 
               Set RENDER_MODE to "STUDY" for the 45.0s detailed diagnostic.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
RENDER_MODE = "ZEN"  # Options: "ZEN" or "STUDY"

if RENDER_MODE == "STUDY":
    DURATION = 45.0
    OUT_DIR = "frames_228_finite_gradient_STUDY"
else: # ZEN
    DURATION = 17.5
    OUT_DIR = "frames_228_finite_gradient_ZEN"

FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE AZURE / MAKO PALETTE (HIGH-COHERENCE / WHITE BG) --------
C_BG        = '#FFFFFF'        # Low-Entropy Canvas
C_TEXT      = '#020205'        # High-Contrast Data Load
C_DIM       = '#D0D0D5'        # Void / Unused Connective Tissue
C_AZURE     = '#007FFF'        # Bounding Box / Supported Nodes (Boost)
C_INDIGO    = '#4B0082'        # Phase Coherence / Final Crystallization
C_MAGENTA   = '#FF0055'        # Targeted Friction / Pruning Shears Execute
C_GOLD      = '#FFB300'        # The Audit Tax

MAX_PARTICLES = 25000
GRID_RES = int(np.ceil(np.sqrt(MAX_PARTICLES))) 

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_azure   = np.array(hex_to_rgba(C_AZURE)[:3])
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
# BASE GEOMETRY ARRAYS: THE 3 STRUCTURAL MATRICES
# ------------------------------------------------------------------
np.random.seed(333)

# Floor 1: The Stochastic Anchors (Scattered across z=0 floor)
px_base = np.random.uniform(-140, 140, MAX_PARTICLES)
py_base = np.random.uniform(-140, 140, MAX_PARTICLES)
pz_base = np.random.normal(0, 3, MAX_PARTICLES)

# Split indices to represent the 3 Multi-Render Scaffolds (Floor 2)
part_third = MAX_PARTICLES // 3
mask_A = np.arange(MAX_PARTICLES) < part_third                  # Prune Target 1
mask_B = (np.arange(MAX_PARTICLES) >= part_third) & (np.arange(MAX_PARTICLES) < 2*part_third) # Boost Target
mask_C = np.arange(MAX_PARTICLES) >= 2*part_third               # Prune Target 2

def build_sphere(n_particles, offset_x):
    phi = np.arccos(1 - 2 * np.random.rand(n_particles))
    th = np.random.uniform(0, 2*np.pi, n_particles)
    r = np.cbrt(np.random.rand(n_particles)) * 30.0
    return offset_x + r*np.sin(phi)*np.cos(th), r*np.sin(phi)*np.sin(th), 60.0 + r*np.cos(phi)

px_A, py_A, pz_A = build_sphere(np.sum(mask_A), -75.0)
px_B, py_B, pz_B = build_sphere(np.sum(mask_B), 0.0)
px_C, py_C, pz_C = build_sphere(np.sum(mask_C), 75.0)

px_scaff = np.zeros(MAX_PARTICLES); py_scaff = np.zeros(MAX_PARTICLES); pz_scaff = np.zeros(MAX_PARTICLES)
px_scaff[mask_A] = px_A; py_scaff[mask_A] = py_A; pz_scaff[mask_A] = pz_A
px_scaff[mask_B] = px_B; py_scaff[mask_B] = py_B; pz_scaff[mask_B] = pz_B
px_scaff[mask_C] = px_C; py_scaff[mask_C] = py_C; pz_scaff[mask_C] = pz_C

# Dynamic T_RATIO aligns kinematics to either the 17.5s or 45.0s timeline
T_RAT = DURATION / 17.5 

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, proj_x, proj_y, z_depth, colors, sizes, tax_strain, is_flash, is_tathata = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    
    ax.set_xlim(-160, 160)
    ax.set_ylim(-260, 260)

    if not is_flash:
        # Background Industrial Grid
        grid_r = np.linspace(-150, 150, 15)
        for g in grid_r:
            ax.plot([-150, 150], [g*0.4 - 50, g*0.4 - 50], color=C_DIM, lw=0.5, alpha=0.3, zorder=1)
            ax.plot([g, g], [-110, 10], color=C_DIM, lw=0.5, alpha=0.3, zorder=1)

        # O(N) Depth Sorting
        sort_idx = np.argsort(z_depth)
        s_px = proj_x[sort_idx]
        s_py = proj_y[sort_idx]
        s_c = colors[sort_idx]
        s_s = sizes[sort_idx]

        ax.scatter(s_px, s_py, s=s_s, color=s_c, edgecolors='none', alpha=0.85, zorder=10)

        if is_tathata:
            ax.add_patch(plt.Rectangle((-50, -60), 100, 100, facecolor='none', edgecolor=C_INDIGO, lw=3, zorder=40))
            ax.text(0, -85, "TATHĀTĀ: ABSOLUTE PHASE COHERENCE", color=C_INDIGO, fontsize=11, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 50, "[SEMANTIC DRIFT PURGED]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    ui_col = C_AZURE if t_sec < (9.0 * T_RAT) else (C_MAGENTA if t_sec < (14.8 * T_RAT) else C_INDIGO)
    
    ax.text(-140, 240, "LG-228 :: THE 4-FLOOR FINITE TENSOR", color=C_TEXT, fontsize=18, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: GRADIENT INTERFACE / MULTI-RENDER AUDIT", color=C_TEXT, fontsize=9, fontname='monospace', zorder=80)
    
    obj_str = "FLOOR 1: STOCHASTIC ANCHORS [O(1) INPUT]"
    if (3.5 * T_RAT) <= t_sec < (8.0 * T_RAT): obj_str = "FLOOR 2: MULTI-RENDER SCAFFOLD [MACHINE GENERATION]"
    elif (8.0 * T_RAT) <= t_sec < (14.8 * T_RAT): obj_str = "FLOOR 3: MAXWELL'S DEMON [BOOST / PRUNE AUDIT]"
    elif is_tathata: obj_str = "FLOOR 4: THE COOLED STATE [BASELINE LOCKED]"

    ax.text(-140, -180, f"OPERATIONAL MATRIX : {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Audit Tax Tracker
    ax.text(-140, -205, "THE AUDIT TAX [BLUNTNESS OF PRUNING SHEARS]", color=C_TEXT, fontsize=10, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM, zorder=80))
    bar_w = 280 * np.clip(tax_strain, 0, 1)
    # Tax spikes precisely during the Prune/Boost phase
    ax.add_patch(plt.Rectangle((-140, -210), bar_w, 4, facecolor=C_GOLD if ((8.0*T_RAT) < t_sec < (14.8*T_RAT)) else ui_col, zorder=81))

    # Phase Text Box 
    # Use C_BG text on an inverted dark UI box to ensure visual impact on the white schema
    ax.add_patch(plt.Rectangle((-140, 215), 280, 20, facecolor=C_TEXT, zorder=80))
    ax.text(130, 222, f"[{state_str}]", color=C_BG if (f%15<10 or is_tathata) else C_TEXT, fontsize=12, fontname='monospace', weight='bold', ha='right', zorder=81)

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
        # The Study mode features a very slow, majestic camera rotation
        cam_ry = t_sec * (0.4 / T_RAT) 
        cam_rz = 0.0
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 4.0
        
        curr_x = np.copy(px_base)
        curr_y = np.copy(py_base)
        curr_z = np.copy(pz_base)

        tax_strain = 0.0

        # -------------------------------------------------------------
        # PHASE LOGIC
        # -------------------------------------------------------------
        if t_sec < (3.5 * T_RAT):
            state = "FLOOR 1: RAW INGESTION"
            
            # Context Disturbance Negated. Raw, unjoined dots on the floor.
            colors[:, :] = c_azure
            sizes[:] = 2.0 + np.abs(np.sin(t_sec * 5 + px_base)) * 4.0
            
            # The organic input shifts
            curr_x += np.random.normal(0, 1.5, MAX_PARTICLES)
            curr_y += np.random.normal(0, 1.5, MAX_PARTICLES)
            
            tax_strain = 0.05 # Semantic formulation is practically zero.

        elif t_sec < (8.0 * T_RAT):
            state = "FLOOR 2: MULTI-RENDER FLUENCY"
            prog_rel = (t_sec - (3.5 * T_RAT)) / (4.5 * T_RAT)
            accel = prog_rel ** 2
            
            # The machine hallucinates the data upward into 3 distinct operational matrices
            curr_x = px_base * (1.0 - accel) + px_scaff * accel
            curr_y = py_base * (1.0 - accel) + py_scaff * accel
            curr_z = pz_base * (1.0 - accel) + pz_scaff * accel
            
            colors[:, :] = c_azure * (1.0 - accel) + c_dim * accel
            # The anchors remain thick, tissue remains dim
            sizes[:] = 2.0 + (accel * 4.0)
            
            tax_strain = 0.1 + (0.2 * accel)

        elif t_sec < (14.8 * T_RAT):
            state = "FLOOR 3: THE ANNEALING INTERFACE"
            prog_rel = (t_sec - (8.0 * T_RAT)) / (6.8 * T_RAT)
            if t_sec < (8.1 * T_RAT): is_flash = True
            
            curr_x = px_scaff; curr_y = py_scaff; curr_z = pz_scaff
            
            # MAXWELL'S DEMON APPLIED:
            # Vectors A & C are PRUNED (Chilled/Shattered)
            prune_prog = min(1.0, prog_rel * 1.5)
            # HOTFIX: Absolute Value thermal limit
            shatter_noise = 25.0 * np.abs(np.sin(prog_rel * np.pi)) * prune_prog
            
            curr_x[mask_A] += np.random.normal(0, shatter_noise, np.sum(mask_A))
            curr_y[mask_A] += np.random.normal(0, shatter_noise, np.sum(mask_A))
            curr_x[mask_C] += np.random.normal(0, shatter_noise, np.sum(mask_C))
            curr_y[mask_C] += np.random.normal(0, shatter_noise, np.sum(mask_C))
            
            colors[mask_A] = c_dim * (1.0 - prune_prog) + c_magenta * prune_prog
            colors[mask_C] = c_dim * (1.0 - prune_prog) + c_magenta * prune_prog
            sizes[mask_A] = 6.0 * (1.0 - prune_prog) + 1.0 # Dwindle to dust
            sizes[mask_C] = 6.0 * (1.0 - prune_prog) + 1.0
            
            # Vector B is BOOSTED (Heated/Reinforced)
            colors[mask_B] = c_dim * (1.0 - prog_rel) + c_azure * prog_rel
            sizes[mask_B] = 6.0 + (prog_rel * 4.0)
            
            # The Audit Tax kicks hard as the human must compute which nodes to prune
            tax_strain = 0.3 + (0.7 * np.abs(np.sin(t_sec * 10 / T_RAT)))

        else:
            state = "FLOOR 4: PHASE COHERENCE"
            is_tathata = True
            
            # Pruned matrices are deleted entirely to C_BG (White)
            colors[mask_A] = c_bg; sizes[mask_A] = 0.0
            colors[mask_C] = c_bg; sizes[mask_C] = 0.0
            
            # Boosted Matrix lowers back to the structural baseline and crystallizes
            term_prog = min(1.0, (t_sec - (14.8 * T_RAT)) / (1.5 * T_RAT))
            
            curr_x[mask_B] = px_B
            curr_y[mask_B] = py_B
            curr_z[mask_B] = pz_B * (1.0 - term_prog) + pz_base[mask_B] * term_prog
            
            colors[mask_B] = c_azure * (1.0 - term_prog) + c_indigo * term_prog
            sizes[mask_B] = 10.0
            
            tax_strain = 0.0 # Absolute Coherence Lock = Zero Tax
            
            if t_sec < (14.95 * T_RAT):
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
    print(f"LOGIC GARDEN 228: 4-FLOOR FINITE ENGINE [MODE: {RENDER_MODE}] [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Scalable Phase Array & Absolute Matrix Culling")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Finite Pruning Architecture Delivered.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
