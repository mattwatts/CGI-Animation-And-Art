"""
SOVEREIGN CODE: logic_garden_275_cross_dimension.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Continuous Serialisation (15.0s)
SCENE: LG-275 (The Cross-Dimensional Finite Engine)
HOTFIX: Numpy Tensor Dimensionality Crash (np.random.choice 1D compliance)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 15.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_275_cross_dimension"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST REALISM PALETTE --------
C_BG        = '#FFFFFF'        # Pure White Baseline
C_DOM_A     = '#2980B9'        # Fluid Dynamics (Azure/Blue)
C_DOM_B     = '#D35400'        # Operations Research (Copper/Orange)
C_HALLUC    = '#C0392B'        # Smooth Hallucination Failure (Crimson)
C_PHANTOM   = '#00A86B'        # Phantom Species / Isomorphism Locked (Deep Jade/Teal)
C_TEXT      = '#2C3E50'        # Rigid Dark Iron for Grid/Text
C_SCANNER   = '#7F8C8D'        # Structural Audit laser

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE KINEMATIC ARCHITECTURE
# ------------------------------------------------------------------
N_PHANT_A = 4000
N_PHANT_B = 4000
N_HALLUC  = 12000
MAX_PARTICLES = N_PHANT_A + N_PHANT_B + N_HALLUC

SCAN_Y = 800.0  # The exact Y-coordinate of Floor 3 SymPy Audit

np.random.seed(275)
# Phantom Species Baseline (Center Mass)
pa_th = np.random.uniform(0, 2*np.pi, N_PHANT_A)
pa_r  = np.random.normal(120, 60, N_PHANT_A)
pb_th = np.random.uniform(0, 2*np.pi, N_PHANT_B)
pb_r  = np.random.normal(120, 60, N_PHANT_B)

# Pre-calculate the perfectly balanced geometric target lattice (The Isomorphism)
target_r_a = np.random.choice([40, 80, 120, 160], N_PHANT_A)
target_th_a = (np.arange(N_PHANT_A) % 12) * (2 * np.pi / 12) + np.random.uniform(-0.02, 0.02, N_PHANT_A)

target_r_b = np.random.choice([60, 100, 140, 180], N_PHANT_B)
target_th_b = (np.arange(N_PHANT_B) % 12) * (2 * np.pi / 12) + (np.pi / 12) + np.random.uniform(-0.02, 0.02, N_PHANT_B)

# Hallucinations Baseline (Falling Garbage)
h_x_start = np.random.uniform(0, 1080, N_HALLUC)
h_y_start = np.random.uniform(1000, 3000, N_HALLUC)
h_vy = np.random.uniform(-250, -450, N_HALLUC)
h_vx = np.random.normal(0, 20, N_HALLUC)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    t_sec = f / float(FPS)
    phase = t_sec / DURATION
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    fig.patch.set_facecolor(C_BG)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    # 1. RENDER BACKGROUND & SYMPY GRID (Floor 3)
    ax.axhline(SCAN_Y, color=C_TEXT, lw=4, zorder=5)
    ax.axhline(SCAN_Y - 5, color=C_SCANNER, lw=2, alpha=0.5, zorder=5)
    ax.add_patch(Rectangle((0, SCAN_Y), 1080, 1120, facecolor='#F8F9F9', zorder=1)) # Latent Space
    ax.add_patch(Rectangle((0, 0), 1080, SCAN_Y, facecolor=C_BG, zorder=1))         # Production Env
    
    # 2. TELEMETRY & DIAGNOSTICS TEXT
    ax.text(20, SCAN_Y + 20, "FLOOR 2: LATENT SPACE BRIDGE (LLM)", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', alpha=0.6)
    ax.text(20, SCAN_Y - 35, "FLOOR 3: ALGEBRAIC PARSER (SYMPY) :: DIMENSIONAL AUDIT", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold')
    
    # 3. KINEMATICS: THE HALLUCINATIONS (Failing the Audit)
    curr_h_y = h_y_start + (h_vy * t_sec)
    curr_h_x = h_x_start + (h_vx * t_sec)
    
    h_color = np.zeros((N_HALLUC, 4))
    h_sizes = np.zeros(N_HALLUC)
    
    mask_above = curr_h_y >= SCAN_Y
    mask_below = curr_h_y < SCAN_Y
    
    a_above = np.sum(mask_above)
    a_below = np.sum(mask_below)
    
    if a_above > 0:
        # HOTFIX: 1D Index extraction to adhere to Numpy Dimensional boundary
        color_matrix = np.array([hex_to_rgba(C_DOM_A)[:3], hex_to_rgba(C_DOM_B)[:3]])
        binary_idx = np.random.choice(2, a_above)
        
        h_color[mask_above, :3] = color_matrix[binary_idx]
        h_color[mask_above, 3] = 0.4 # Semi-translucent
        h_sizes[mask_above] = 8.0
        
    if a_below > 0:
        # Shatter effect (Axis broken)
        shear_fall = SCAN_Y - curr_h_y[mask_below]
        curr_h_x[mask_below] += np.sin(shear_fall * 0.1) * (shear_fall * 0.5)
        curr_h_y[mask_below] -= shear_fall * 0.5 # Accelerate drop
        
        h_color[mask_below, :3] = hex_to_rgba(C_HALLUC)[:3]
        h_color[mask_below, 3] = np.clip(1.0 - (shear_fall / 200.0), 0.0, 1.0)
        h_sizes[mask_below] = np.clip(15.0 - (shear_fall / 10.0), 1.0, 15.0)

    # 4. KINEMATICS: THE PHANTOM SPECIES (Balancing the Audit)
    cy = 1600 - (t_sec * 85.0)
    cx = 540
    
    if cy >= SCAN_Y:
        k = 0.0
    else:
        k = np.clip((SCAN_Y - cy) / 250.0, 0.0, 1.0)
        
    orbit_speed = 3.0
    
    # DOMAIN A (Fluid)
    curr_pa_th = pa_th + orbit_speed * t_sec
    curr_pa_r  = pa_r * (1 - k) + target_r_a * k
    final_pa_th = curr_pa_th * (1 - k) + (target_th_a + orbit_speed * t_sec) * k
    
    pax = cx + curr_pa_r * np.cos(final_pa_th)
    pay = cy + curr_pa_r * np.sin(final_pa_th)
    
    c_a = np.array(hex_to_rgba(C_DOM_A)[:3])
    c_p = np.array(hex_to_rgba(C_PHANTOM)[:3])
    ca_tensor = c_a * (1 - k) + c_p * k
    ca_rgba = np.column_stack((np.tile(ca_tensor, (N_PHANT_A, 1)), np.full(N_PHANT_A, 0.9)))
    
    # DOMAIN B (Network)
    curr_pb_th = pb_th - orbit_speed * t_sec # Counter orbit
    curr_pb_r  = pb_r * (1 - k) + target_r_b * k
    final_pb_th = curr_pb_th * (1 - k) + (target_th_b - orbit_speed * t_sec) * k
    
    pbx = cx + curr_pb_r * np.cos(final_pb_th)
    pby = cy + curr_pb_r * np.sin(final_pb_th)
    
    cb_tensor = np.array(hex_to_rgba(C_DOM_B)[:3]) * (1 - k) + c_p * k
    cb_rgba = np.column_stack((np.tile(cb_tensor, (N_PHANT_B, 1)), np.full(N_PHANT_B, 0.9)))

    # Global compilation
    all_x = np.concatenate([curr_h_x, pax, pbx])
    all_y = np.concatenate([curr_h_y, pay, pby])
    all_c = np.concatenate([h_color, ca_rgba, cb_rgba])
    all_s = np.concatenate([h_sizes, np.full(N_PHANT_A, 12.0), np.full(N_PHANT_B, 12.0)])
    
    sort_idx = np.argsort(all_s)
    ax.scatter(all_x[sort_idx], all_y[sort_idx], s=all_s[sort_idx], color=all_c[sort_idx], edgecolors='none', zorder=2)
    
    # Structural Core (The mathematical heart of the Isomorphism)
    if k > 0.05:
        ax.add_patch(plt.Circle((cx, cy), 160 * k, fill=False, edgecolor=C_PHANTOM, lw=3*k, alpha=0.5 + 0.5*k, zorder=3))
        ax.add_patch(plt.Circle((cx, cy), 80 * k, fill=False, edgecolor=C_PHANTOM, lw=2*k, alpha=max(0, k), zorder=3))
    
    # 5. UI HUD WIDGETS
    ui_y = 1800
    ax.add_patch(Rectangle((40, ui_y), 400, 80, facecolor=C_BG, edgecolor=C_TEXT, lw=2, zorder=10))
    ax.text(60, ui_y + 40, f"TIME CAUSALITY: {t_sec:05.2f}S", color=C_TEXT, fontsize=18, fontname='monospace', weight='bold', va='center')
    
    stat_color = C_TEXT if k < 0.1 else C_PHANTOM
    stat_msg = "ANALYSING TENSORS..." if k < 0.1 else "ISOMORPHISM LOCKED."
    if k == 0.0 and (int(f/10) % 2 == 0):
        stat_color = C_HALLUC
        stat_msg = "SHREDDING HALLUCINATIONS"
        
    ax.add_patch(Rectangle((40, ui_y - 100), 400, 80, facecolor=C_BG, edgecolor=stat_color, lw=3, zorder=10))
    ax.text(60, ui_y - 60, stat_msg, color=stat_color, fontsize=16, fontname='monospace', weight='bold', va='center')

    # Phantom Status
    if cy < SCAN_Y + 150:
        p_stat_y = cy + 200
        if k < 1.0:
            ax.plot([cx, cx], [cy+120, p_stat_y-20], color=C_TEXT, lw=2, linestyle=':', alpha=0.5)
            ax.text(cx, p_stat_y, "[DIMENSIONS: ANALYSING M/L/T]", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', ha='center')
        else:
            ax.plot([cx, cx], [cy+180, p_stat_y-20], color=C_PHANTOM, lw=2)
            ax.text(cx, p_stat_y, "[DIMENSIONS BALANCED: \nPHANTOM SPECIES HARVESTED]", color=C_PHANTOM, fontsize=16, fontname='monospace', weight='bold', ha='center')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-275: CROSS-DIMENSIONAL FINITE ENGINE [CORES: {cpu_cores}]")
    print("Executing PROTOCOL: Bare-Metal SymPy Audit & Realism (HOTFIX)")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            if finished_frame % 30 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")
    print("Compilation Complete. Phantom Species Extracted.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
