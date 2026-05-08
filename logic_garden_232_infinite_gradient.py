"""
SOVEREIGN CODE: logic_garden_232_infinite_gradient.py
SYSTEM: Python Multicore / O(1) Phase Space Topology
SCENE: Logic Garden 232 (The Infinite Gradient / Middle Ways)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Semantic Drift Absolute Standard Deviation Clamp (np.abs)
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
OUT_DIR = "frames_232_infinite_gradient"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'        # Deep Space / Absolute Null
C_TEXT      = '#FFFFFF'        # Data Load / High Coherence
C_DIM       = '#111116'        # Void Structure
C_MAGENTA   = '#FF0055'        # The Binary Fallacy (Disconnected states)
C_MANTIS    = '#00FF00'        # Sparse Node Anchors / Bedrock Logic
C_CYAN      = '#00FFFF'        # Gradient Connective Tissue (Middle Ways)
C_GOLD      = '#FFD700'        # Thermal Friction / The Audit Tax

MAX_PARTICLES = 25000

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_void    = np.array(hex_to_rgba(C_VOID)[:3])
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
# BASE GEOMETRY: BINARY PLANES VS MAJESTIC TORUS KNOT
# ------------------------------------------------------------------
np.random.seed(777)

# 1. State A: The Binary Fallacy (Two disconnected structural planes)
px_bin = np.random.uniform(-100, 100, MAX_PARTICLES)
py_bin = np.random.uniform(-100, 100, MAX_PARTICLES)
# Force split into Z = -80 and Z = +80
binary_split = np.random.choice([-1, 1], MAX_PARTICLES)
pz_bin = 80.0 * binary_split + np.random.normal(0, 5, MAX_PARTICLES)

# 2. State B: The Torus Knot (The Infinity of Middle Ways)
# P = 3, Q = 7 Topology
U = np.random.uniform(0, 2 * np.pi, MAX_PARTICLES)
V = np.random.uniform(0, 2 * np.pi, MAX_PARTICLES)

R = 60.0
r_tub = 25.0
p_knot = 3.0
q_knot = 7.0

# Parametric Torus Knot
knot_r = R + r_tub * np.cos(q_knot * U)
px_knot = knot_r * np.cos(p_knot * U)
py_knot = knot_r * np.sin(p_knot * U)
pz_knot = r_tub * np.sin(q_knot * U)

# Add volume to the knot via V
px_knot += 8.0 * np.cos(V) * np.cos(p_knot * U)
py_knot += 8.0 * np.cos(V) * np.sin(p_knot * U)
pz_knot += 8.0 * np.sin(V)

# Identify mathematical "Sparse Anchors" (Lowest points on the knot structure)
anchor_mask = np.abs(np.sin(p_knot * U)) < 0.15

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, proj_x, proj_y, z_depth, colors, sizes, tax_metric, coher_metric, is_flash, is_tathata = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_TEXT if is_flash else C_VOID
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    ax.set_xlim(-160, 160)
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
            ax.add_patch(plt.Rectangle((-120, -120), 240, 240, facecolor='none', edgecolor=C_MANTIS, lw=2, zorder=40))
            ax.text(0, -140, "TATHĀTĀ: PHASE COHERENCE LOCKED", color=C_MANTIS, fontsize=11, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 130, "[SEMANTIC DRIFT = 0.0]", color=C_CYAN, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    ui_col = C_MAGENTA if t_sec < 4.0 else (C_CYAN if t_sec < 9.0 else C_GOLD)
    if is_tathata: ui_col = C_MANTIS
    txt_col = C_VOID if is_flash else C_TEXT

    ax.text(-140, 250, "LG-232 :: THE INFINITE GRADIENT", color=ui_col, fontsize=19, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 238, "SYSTEM: MIDDLE WAYS / KNOT TOPOLOGY", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    
    obj_str = "THE BINARY FALLACY [TEXT VS DNI]"
    if 4.0 <= t_sec < 9.0: obj_str = "SPARSE-NODE ANCHORING [N-DIMENSIONAL WEAVE]"
    elif 9.0 <= t_sec < 14.8: obj_str = "THE RAGGED EDGE [SEMANTIC DRIFT ACTIVE]"
    elif is_tathata: obj_str = "TATHĀTĀ [ABSOLUTE SYNCHRONIZATION]"

    ax.text(-140, -180, f"OPERATIONAL PHASE: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Audit Tax Metric (Friction Inject)
    ax.text(-140, -205, "AUDIT TAX [GLUCOSE BURN / NOISE RATIO]", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 3, facecolor=C_DIM, zorder=80))
    tax_w = 280 * np.clip(tax_metric, 0, 1)
    ax.add_patch(plt.Rectangle((-140, -210), tax_w, 3, facecolor=C_GOLD if tax_metric > 0.3 else ui_col, zorder=81))

    # Phase Coherence Metric
    ax.text(-140, -230, "PHASE COHERENCE [O(1) FLUENCY]", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -235), 280, 3, facecolor=C_DIM, zorder=80))
    coh_w = 280 * np.clip(coher_metric, 0, 1)
    ax.add_patch(plt.Rectangle((-140, -235), coh_w, 3, facecolor=C_MANTIS if coher_metric > 0.9 else ui_col, zorder=81))

    # Phase Text Box
    ax.add_patch(plt.Rectangle((-140, 220), 280, 2, facecolor=ui_col, zorder=80))
    ax.text(140, 210, f"[{state_str}]", color=ui_col if (f%15<10 or is_tathata) else C_VOID, fontsize=14, fontname='monospace', weight='bold', ha='right', zorder=80)

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
        
        cam_rx = np.pi/5
        cam_ry = t_sec * 0.4
        cam_rz = t_sec * 0.1
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 4.0
        
        curr_x = np.copy(px_bin)
        curr_y = np.copy(py_bin)
        curr_z = np.copy(pz_bin)

        tax_metric = 0.0
        coher_metric = 0.0

        # -------------------------------------------------------------
        # PHASE LOGIC
        # -------------------------------------------------------------
        if t_sec < 4.0:
            state = "THE BINARY FALLACY :: RIGID STATES"
            
            # The two separate planes pulse with inefficiency
            fluct = 5.0 * np.sin(t_sec * 6)
            curr_z += np.sign(curr_z) * fluct
            
            colors[:, :] = c_magenta
            sizes[:] = np.random.uniform(2, 6, MAX_PARTICLES)
            
            tax_metric = 0.9  # High cognitive cost to bridge the gap
            coher_metric = 0.0

        elif t_sec < 9.0:
            state = "SPARSE-NODE ANCHORING :: GRADIENT GENERATION"
            prog = (t_sec - 4.0) / 5.0
            accel = prog ** 2
            
            # Interpolate from Binary planes to the Torus Knot
            curr_x = px_bin * (1.0 - accel) + px_knot * accel
            curr_y = py_bin * (1.0 - accel) + py_knot * accel
            curr_z = pz_bin * (1.0 - accel) + pz_knot * accel
            
            # The connective tissue weaves into Cyan
            colors[:, :] = c_magenta * (1.0 - accel) + c_cyan * accel
            
            # Sparse Nodes permanently map to MANTIS
            colors[anchor_mask] = c_magenta * (1.0 - accel) + c_mantis * accel
            sizes[anchor_mask] = 4.0 + (accel * 6.0)
            
            tax_metric = 0.9 * (1.0 - prog) + 0.1
            coher_metric = prog * 0.7

        elif t_sec < 14.8:
            state = "THE RAGGED EDGE :: AUDIT TAX & SEMANTIC DRIFT"
            prog = (t_sec - 9.0) / 5.8
            if t_sec < 9.1: is_flash = True
            
            # TATHĀTĀ HOTFIX INSTALLED: Absolute Value Standard Deviation Clamp
            # This directly eliminates the ValueError: scale < 0 dimensional crash.
            drift_mag = 15.0 * np.abs(np.sin(t_sec * 8))
            
            # The knot topology holds, but machine hallucination introduces friction
            noise_x = np.random.normal(0, drift_mag, MAX_PARTICLES)
            noise_y = np.random.normal(0, drift_mag, MAX_PARTICLES)
            noise_z = np.random.normal(0, drift_mag, MAX_PARTICLES)
            
            curr_x = px_knot + noise_x
            curr_y = py_knot + noise_y
            curr_z = pz_knot + noise_z
            
            # The Sparse Anchors (MANTIS) are immovable truth vectors. They do NOT drift.
            curr_x[anchor_mask] = px_knot[anchor_mask]
            curr_y[anchor_mask] = py_knot[anchor_mask]
            curr_z[anchor_mask] = pz_knot[anchor_mask]
            
            colors[:, :] = c_cyan
            
            # The drift nodes visually spike as GOLD (Audit Tax)
            drift_thresh = np.random.rand(MAX_PARTICLES) < (np.abs(np.sin(t_sec * 8)) * 0.8)
            drift_idx = np.where(drift_thresh & ~anchor_mask)[0]
            colors[drift_idx] = c_gold
            sizes[drift_idx] = 8.0
            
            colors[anchor_mask] = c_mantis
            sizes[anchor_mask] = 10.0
            
            tax_metric = 0.1 + (0.9 * np.abs(np.sin(t_sec * 8)))
            coher_metric = 0.7 - (0.4 * np.abs(np.sin(t_sec * 8)))

        else:
            state = "TATHĀTĀ :: ABSOLUTE PHASE COHERENCE"
            is_tathata = True
            
            # The human manually terminates the Audit Loop at the acceptable threshold.
            # Semantic drift drops to an absolute, mathematical 0.0.
            curr_x = px_knot
            curr_y = py_knot
            curr_z = pz_knot
            
            colors[:, :] = c_cyan
            colors[anchor_mask] = c_mantis
            
            sizes[:] = 5.0
            sizes[anchor_mask] = 12.0
            
            tax_metric = 0.0 
            coher_metric = 1.0 
            
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

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], colors[cull_mask], sizes[cull_mask], tax_metric, coher_metric, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 232: THE INFINITE GRADIENT TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: drift_mag Absolute Value Clamp (ValueError Terminated)")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Zero-Day Exploit Patched. Torus Knot Secured.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
