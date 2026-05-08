"""
SOVEREIGN CODE: logic_garden_224_phase_coherence.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Gradient Kinematics (17.5 seconds)
SCENE: Logic Garden 224 (Phase Coherence Restored / The Audit Tax)
HOTFIX: O(N) Absolute Value Clamping (Negative Entropy Excision)
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
OUT_DIR = "frames_224_phase_coherence"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'
C_CYAN      = '#00FFFF'        # Connective Tissue (Machine Fill)
C_MAGENTA   = '#FF0055'        # The Binary Fallacy / Error
C_GOLD      = '#FFD700'        # The Ragged Edge / Audit Tax (Friction)
C_MANTIS    = '#00FF00'        # Sparse-Node Anchors / Phase Coherence

MAX_PARTICLES = 25000

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_void = np.array(hex_to_rgba(C_VOID)[:3])
c_text = np.array(hex_to_rgba(C_TEXT)[:3])
c_cyan = np.array(hex_to_rgba(C_CYAN)[:3])
c_mage = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_gold = np.array(hex_to_rgba(C_GOLD)[:3])
c_mantis = np.array(hex_to_rgba(C_MANTIS)[:3])
c_dim = np.array(hex_to_rgba(C_DIM)[:3])

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
# BASE GEOMETRY ARRAYS: THE BINARY SPHERES VS THE TORUS KNOT
# ------------------------------------------------------------------
np.random.seed(777)

# Geometry 1: The Binary Fallacy (Two detached, dense spheres)
bin_phi = np.arccos(1 - 2 * np.random.rand(MAX_PARTICLES))
bin_th = np.random.uniform(0, 2 * np.pi, MAX_PARTICLES)
bin_r = np.cbrt(np.random.rand(MAX_PARTICLES)) * 35.0
# Split exactly in half
sign = np.where(np.arange(MAX_PARTICLES) < MAX_PARTICLES/2, -1, 1)
px_bin = sign * 60.0 + bin_r * np.sin(bin_phi) * np.cos(bin_th)
py_bin = bin_r * np.sin(bin_phi) * np.sin(bin_th)
pz_bin = bin_r * np.cos(bin_phi)

# Geometry 2: The Gradient Interface (Majestic 3D Torus Knot p=3, q=7)
knot_t = np.linspace(0, 2 * np.pi, MAX_PARTICLES)
px_knot = (70.0 + 25.0 * np.cos(7 * knot_t)) * np.cos(3 * knot_t)
py_knot = (70.0 + 25.0 * np.cos(7 * knot_t)) * np.sin(3 * knot_t)
pz_knot = 25.0 * np.sin(7 * knot_t)

# Define the Sparse-Node Anchors (20 Load-Bearing Variable Clusters)
anchor_mask = np.zeros(MAX_PARTICLES, dtype=bool)
anchor_indices = np.linspace(100, MAX_PARTICLES-100, 20, dtype=int)
for idx in anchor_indices:
    anchor_mask[idx-200:idx+200] = True # Create "thick" visual nodes

tissue_mask = ~anchor_mask

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, proj_x, proj_y, z_depth, colors, sizes, tax_strain, is_flash, is_tathata = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_TEXT if is_flash else C_VOID
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    ax.set_xlim(-150, 150)
    ax.set_ylim(-260, 260)

    if not is_flash:
        # O(N) Depth Sorting
        sort_idx = np.argsort(z_depth)
        s_px = proj_x[sort_idx]
        s_py = proj_y[sort_idx]
        s_c = colors[sort_idx]
        s_s = sizes[sort_idx]

        ax.scatter(s_px, s_py, s=s_s, color=s_c, edgecolors='none', alpha=0.9, zorder=10)

        if is_tathata:
            ax.add_patch(plt.Rectangle((-130, -220), 260, 440, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -240, "TATHĀTĀ: PHASE COHERENCE SECURED.", color=C_MANTIS, fontsize=10, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 225, "[SPARSE-NODE ANCHORING EXECUTED]", color=C_DIM, fontsize=10, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    ui_col = C_MAGENTA if t_sec < 4.0 else (C_CYAN if t_sec < 9.0 else C_GOLD)
    if is_tathata: ui_col = C_MANTIS
    
    txt_col = C_TEXT if not is_flash else C_VOID

    ax.text(-140, 240, "LG-224 :: PHASE COHERENCE", color=ui_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: GRADIENT MAPPING / THE MIDDLE WAYS", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    
    # Telemetry Status
    obj_str = "STRUCTURAL ERROR: INVERSE OF SPECIFICITY"
    if 4.0 <= t_sec < 9.0: obj_str = "SPARSE-NODE ANCHORING (THICK DATA INPUT)"
    elif 9.0 <= t_sec < 14.8: obj_str = "MACHINE SYNTHESIS / DRIFT PRUNING"
    elif is_tathata: obj_str = "DYNAMIC PARAMETER CLAMP / BALANCE ACHIEVED"

    ax.text(-140, -180, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=11, fontname='monospace', weight='bold', zorder=80)
    
    # Thermodynamic Hardware Metric: The Semantic Tax Vector
    metric_label = "PROMPTING TAX (GLUCOSE DRAIN)" if t_sec < 4.0 else "AUDIT TAX (FRICTION-INJECT)"
    ax.text(-140, -205, metric_label, color=txt_col, fontsize=10, fontname='monospace', zorder=80)
    
    ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM, zorder=80))
    bar_w = 280 * np.clip(tax_strain, 0, 1)
    ax.add_patch(plt.Rectangle((-140, -210), bar_w, 4, facecolor=ui_col, zorder=81))

    # Phase Text Box
    ax.add_patch(plt.Rectangle((-140, 215), 280, 2, facecolor=ui_col, zorder=80))
    ax.text(140, 205, f"[{state_str}]", color=ui_col if (f%15<10 or is_tathata) else C_VOID, fontsize=14, fontname='monospace', weight='bold', ha='right', zorder=80)

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
        
        # Isometric Camera - Majestic Slow Rotation
        cam_rx = np.pi/6
        cam_ry = t_sec * 0.4
        cam_rz = np.sin(t_sec * 0.1) * 0.2
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 4.0
        
        curr_x = np.copy(px_bin)
        curr_y = np.copy(py_bin)
        curr_z = np.copy(pz_bin)

        tax_strain = 1.0

        # -------------------------------------------------------------
        # PHASE LOGIC
        # -------------------------------------------------------------
        if t_sec < 4.0:
            state = "THE BINARY FALLACY :: RIGID DISCONNECTION"
            
            colors[:int(MAX_PARTICLES/2)] = c_mage
            colors[int(MAX_PARTICLES/2):] = c_dim
            sizes[:] = 5.0
            
            tax_strain = 1.0 # Max Human Drain for brute-forcing rigid inputs

        elif t_sec < 9.0:
            state = "THE GRADIENT INTERFACE :: THICK DATA NODES"
            prog = (t_sec - 4.0) / 5.0
            accel = prog ** 2
            
            # The Binary Spheres aggressively unravel into the neural lattice
            curr_x = px_bin * (1.0 - accel) + px_knot * accel
            curr_y = py_bin * (1.0 - accel) + py_knot * accel
            curr_z = pz_bin * (1.0 - accel) + pz_knot * accel
            
            # The Nodes lock first
            colors[anchor_mask] = c_mage * (1.0 - accel) + c_mantis * accel
            sizes[anchor_mask] = 5.0 + (accel * 5.0)
            
            # The Connective Tissue remains dim/fuzzy
            colors[tissue_mask] = c_dim * (1.0 - accel) + c_cyan * (accel * 0.3)
            sizes[tissue_mask] = 2.0
            
            tax_strain = 1.0 - (accel * 0.8) # Prompting tax drops as sparse nodes do the lifting

        elif t_sec < 14.8:
            state = "CONNECTIVE TISSUE :: THE RAGGED EDGE (FRICTION)"
            prog = (t_sec - 9.0) / 5.8
            if t_sec < 9.1: is_flash = True
            
            curr_x = px_knot
            curr_y = py_knot
            curr_z = pz_knot
            
            # The Machine calculates the tissue. It generates "Semantic Drift"
            # HOTFIX APPLIED: Entropy Cannot Be Negative. np.abs enforced.
            drift_mag = 15.0 * np.abs(np.sin(t_sec * 8))
            fuzz_x = np.random.normal(0, drift_mag, MAX_PARTICLES)
            fuzz_y = np.random.normal(0, drift_mag, MAX_PARTICLES)
            fuzz_z = np.random.normal(0, drift_mag, MAX_PARTICLES)
            
            curr_x[tissue_mask] += fuzz_x[tissue_mask]
            curr_y[tissue_mask] += fuzz_y[tissue_mask]
            curr_z[tissue_mask] += fuzz_z[tissue_mask]
            
            colors[anchor_mask] = c_mantis
            sizes[anchor_mask] = 10.0
            
            # The further the tissue drifts from the knot, the more it costs in "Audit Tax" (Gold)
            dist_drift = np.sqrt(fuzz_x**2 + fuzz_y**2 + fuzz_z**2)
            gold_ratio = np.clip(dist_drift / 15.0, 0, 1)
            
            for i in np.where(tissue_mask)[0]:
                colors[i] = c_cyan * (1.0 - gold_ratio[i]) + c_gold * gold_ratio[i]
            
            sizes[tissue_mask] = 3.0 + (prog * 2.0)
            
            tax_strain = 0.5 + (0.5 * np.sin(t_sec*10)) # Fluctuating Audit Tax

        else:
            state = "TATHĀTĀ :: BOOST & PRUNE FEEDBACK LOCKED"
            is_tathata = True
            
            # Absolute mathematical alignment. The Semantic Drift is pruned.
            curr_x = px_knot
            curr_y = py_knot
            curr_z = pz_knot
            
            colors[anchor_mask] = c_mantis
            sizes[anchor_mask] = 10.0
            
            colors[tissue_mask] = c_cyan
            sizes[tissue_mask] = 5.0
            
            tax_strain = 0.0 # Bounding box achieved. Zero unnecessary friction.
            
            if t_sec < 14.95:
                is_flash = True

        # Apply Global Tensor Matrix
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1]
        z_depth = rot_pts[:, 2] 

        # O(1) Geometry Culling
        cull_mask = (proj_y > -260) & (proj_y < 260) & (proj_x > -150) & (proj_x < 150)

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], colors[cull_mask], sizes[cull_mask], tax_strain, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 224: PHASE COHERENCE [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Torus-Knot Network Construction & Scale Constraint")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Zero-Temperature Auditing Achieved.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
