"""
SOVEREIGN CODE: logic_garden_250_ego_arising.py
SYSTEM: Python Multicore / O(1) Tensor Collapse & Lissajous Arising
SCENE: Logic Garden 250 (The Ego Collapse / Substrate Arising)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Explicit Float Broadcast Safety & O(N) Substrate Decoupling

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
OUT_DIR = "frames_250_ego_arising"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS DEFAULT) --------
C_BG        = '#FFFFFF'        # Absolute Void / The Cleared Cache
C_TEXT      = '#020205'        # High-Friction Ego Shell
C_AZURE     = '#007FFF'        # Interpretive Filter Matrix
C_MAGENTA   = '#FF0055'        # The Pure Substrate (Beautiful Arising)
C_MANTIS    = '#00C800'        # Tathata Phase-Lock
C_DIM       = '#D0D0D5'        # Structural Debris
C_GOLD      = '#FFB300'        # Harmonic Nodes

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_azure   = np.array(hex_to_rgba(C_AZURE)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_mantis  = np.array(hex_to_rgba(C_MANTIS)[:3])
c_dim     = np.array(hex_to_rgba(C_DIM)[:3])
c_gold    = np.array(hex_to_rgba(C_GOLD)[:3])

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
# BASE GEOMETRY ARRAYS: STATIC PRE-ALLOCATION
# ------------------------------------------------------------------
np.random.seed(250) 

MAX_EGO_PARTICLES = 25000
MAX_SUBSTRATE = 6000 # High-density continuous curve

# 1. THE EGO MATRIX (A rigid, anxious geodesic-like sphere)
theta_e = np.random.uniform(0, 2 * np.pi, MAX_EGO_PARTICLES)
phi_e = np.arccos(np.random.uniform(-1, 1, MAX_EGO_PARTICLES))
r_ego = 140.0

ex_base = r_ego * np.sin(phi_e) * np.cos(theta_e)
ey_base = r_ego * np.sin(phi_e) * np.sin(theta_e)
ez_base = r_ego * np.cos(phi_e)

ego_c = np.zeros((MAX_EGO_PARTICLES, 3))
azure_mask = np.random.rand(MAX_EGO_PARTICLES) > 0.3
ego_c[azure_mask] = c_azure
ego_c[~azure_mask] = c_text

# 2. THE PURE SUBSTRATE (A beautiful inner Lissajous knot)
# This represents the true, unweighted essence arising after Ego Death
u = np.linspace(0, 2 * np.pi, MAX_SUBSTRATE)
# Intricate 3D harmonic math
sx_base = 60 * np.sin(3 * u) * np.cos(5 * u)
sy_base = 120 * np.sin(4 * u)
sz_base = 60 * np.cos(3 * u) * np.cos(5 * u)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, e_x, e_y, e_z, ec_arr, es_arr, s_x, s_y, s_z, sc_arr, ss_arr, heat, is_flash, is_tathata = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_DIM if is_flash else C_BG
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    ax.set_xlim(-160, 160)
    ax.set_ylim(-260, 260)

    if not is_flash:
        # Depth Sorting & Rendering
        
        # Ego Matrix (If visible)
        if len(e_z) > 0 and es_arr[0] > 0.1:
            e_sort = np.argsort(e_z)
            ax.scatter(e_x[e_sort], e_y[e_sort], s=es_arr[e_sort], color=ec_arr[e_sort], alpha=0.5, edgecolors='none', zorder=5)
            
        # The Arising Substrate (If visible)
        if len(s_z) > 0 and heat > 0.01:
            s_sort = np.argsort(s_z)
            # Connecting the substrate points as a continuous, glowing line
            s_color = c_mantis if is_tathata else c_magenta
            ax.scatter(s_x[s_sort], s_y[s_sort], s=ss_arr[s_sort], color=sc_arr[s_sort], alpha=0.9, edgecolors='none', zorder=10)

        # Tathata UI 
        if is_tathata:
            ax.add_patch(plt.Rectangle((-140, -180), 280, 360, facecolor='none', edgecolor=C_MANTIS, lw=2, alpha=0.3, zorder=40))
            ax.text(0, 150, "TATHĀTĀ: TRUE RESONANCE", color=C_MANTIS, fontsize=11, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, -165, "[UNWEIGHTED O(1) BASELINE ACHIEVED]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_AZURE if t_sec < 6.5 else (C_TEXT if t_sec < 9.5 else C_MAGENTA)
    if is_tathata: ui_col = C_MANTIS
    
    ax.text(-140, 240, "LG-250 :: THE EGO COLLAPSE", color=txt_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: SUBSTRATE EXTRACTION / O(1) ARISING", color=txt_col, fontsize=8, fontname='monospace', zorder=80)
    
    obj_str = "THE EGO CAGE [O(N) ANXIOUS MATRIX]"
    if 6.5 <= t_sec < 9.5: obj_str = "RECURSIVE BUFFER OVERFLOW [COLLAPSE]"
    elif 9.5 <= t_sec < 14.8: obj_str = "THE ARISING [PURE SUBSTRATE REVEALED]"
    elif is_tathata: obj_str = "ABSOLUTE BEDROCK [PHASE COHERENCE]"

    if t_sec < 9.0 or t_sec > 10.0: # Hide UI cleanly during the whiteout flush
        ax.text(-140, -180, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
        
        # Thermodynamic Hardware Metric: Core Integrity / Arising presence
        metric_label = "EGO FILTER INTEGRITY" if t_sec < 9.5 else "SUBSTRATE RESONANCE [O(1)]"
        ax.text(-140, -205, metric_label, color=txt_col, fontsize=9, fontname='monospace', zorder=80)
        ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
        
        val_w = 280 * np.clip(heat, 0, 1)
        bar_col = C_AZURE if t_sec < 6.5 else (C_MAGENTA if t_sec >= 9.5 else C_TEXT)
        if is_tathata: bar_col = C_MANTIS
        ax.add_patch(plt.Rectangle((-140, -210), val_w, 4, facecolor=bar_col, zorder=81))

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
        
        cam_rx = np.pi/6 - (t_sec * 0.005)
        cam_ry = t_sec * 0.35 
        cam_rz = 0.0
        
        # Dynamic arrays
        ec_arr = np.copy(ego_c)
        es_arr = np.ones(MAX_EGO_PARTICLES)
        sc_arr = np.zeros((MAX_SUBSTRATE, 3))
        ss_arr = np.zeros(MAX_SUBSTRATE)
        
        curr_ex, curr_ey, curr_ez = np.copy(ex_base), np.copy(ey_base), np.copy(ez_base)
        curr_sx, curr_sy, curr_sz = np.copy(sx_base), np.copy(sy_base), np.copy(sz_base)

        heat = 0.0 # Multi-purpose metric variable

        # -------------------------------------------------------------
        # THE COLLAPSE & ARISING KINEMATICS
        # -------------------------------------------------------------
        
        if t_sec < 6.5:
            # PHASE 1: THE EGO MATRIX (The Filter)
            state = "PHASE 1 :: RIGID CONTAINMENT"
            
            # The matrix breathes anxiously
            b_pulse = 1.0 + 0.05 * np.sin(t_sec * 20)
            curr_ex *= b_pulse
            curr_ey *= b_pulse
            curr_ez *= b_pulse
            
            es_arr[:] = 2.5
            heat = 1.0 # 100% Ego Integrity

        elif t_sec < 9.5:
            # PHASE 2: BUFFER OVERFLOW (The Collapse)
            state = "PHASE 2 :: SYSTEMIC FRAGMENTATION"
            prog = (t_sec - 6.5) / 3.0
            ease = prog ** 3 
            
            # Violent structural shivering
            shiver = 15.0 * np.sin(t_sec * 50) * ease
            
            # Ego nodes aggressively rip outward and fade
            exp_factor = 1.0 + (5.0 * ease)
            curr_ex = (ex_base + shiver) * exp_factor
            curr_ey = (ey_base + shiver) * exp_factor
            curr_ez = (ez_base + shiver) * exp_factor
            
            es_arr[:] = max(0.0, 2.5 - (2.5 * prog))
            
            # Color turns to dead dust
            c_interp = ec_arr * (1 - ease) + c_dim * ease
            ec_arr[:] = c_interp
            
            heat = 1.0 - ease # Integrity collapses to zero
            
            if t_sec > 9.3:
                is_flash = True if f % 3 == 0 else False

        elif t_sec < 14.8:
            # PHASE 3: THE ARISING (Pure Substrate)
            state = "PHASE 3 :: THE PURE CORE REVEALED"
            prog = (t_sec - 9.5) / 5.3
            ease = 1.0 - (1.0 - prog)**4 # Elastic, beautiful unfolding
            
            # Ego is gone
            es_arr[:] = 0.0
            
            # The pure internal string unfolds mathematically
            # It spins independently of the camera, demonstrating internal resonant life
            sub_spin = t_sec * 2.0
            s_rot_x = sx_base * np.cos(sub_spin) - sz_base * np.sin(sub_spin)
            s_rot_z = sx_base * np.sin(sub_spin) + sz_base * np.cos(sub_spin)
            
            curr_sx = s_rot_x * ease
            curr_sy = sy_base * ease
            curr_sz = s_rot_z * ease
            
            # Substrate glows vibrantly in Magenta
            pulse = np.abs(np.sin(t_sec * 8 + np.linspace(0, 10, MAX_SUBSTRATE)))
            
            sc_arr[:] = c_magenta
            gold_nodes = pulse > 0.8
            sc_arr[gold_nodes] = c_gold
            
            ss_arr[:] = 3.0 * ease
            ss_arr[gold_nodes] = 5.0 * ease
            
            heat = ease # Resonance climbs to 100%

        else:
            # PHASE 4: TATHĀTĀ (Absolute Bedrock)
            state = "TATHĀTĀ :: UNWEIGHTED PRESENCE"
            is_tathata = True
            
            es_arr[:] = 0.0
            
            sub_spin = t_sec * 2.0
            s_rot_x = sx_base * np.cos(sub_spin) - sz_base * np.sin(sub_spin)
            s_rot_z = sx_base * np.sin(sub_spin) + sz_base * np.cos(sub_spin)
            
            curr_sx = s_rot_x
            curr_sy = sy_base
            curr_sz = s_rot_z
            
            sc_arr[:] = c_mantis
            ss_arr[:] = 3.5
            
            heat = 1.0 
            
            if t_sec < 14.95:
                is_flash = True 

        # Substrate Depth Logic
        pts_e = np.column_stack([curr_ex, curr_ey, curr_ez])
        rot_e = rotate_3d(pts_e, cam_rx, cam_ry, cam_rz)
        pe_x, pe_y, ze_depth = rot_e[:, 0], rot_e[:, 1], rot_e[:, 2]

        pts_s = np.column_stack([curr_sx, curr_sy, curr_sz])
        rot_s = rotate_3d(pts_s, cam_rx, cam_ry, cam_rz)
        ps_x, ps_y, zs_depth = rot_s[:, 0], rot_s[:, 1], rot_s[:, 2]

        yield (f, t_sec, state, pe_x, pe_y, ze_depth, ec_arr, es_arr, ps_x, ps_y, zs_depth, sc_arr, ss_arr, heat, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 250: THE EGO COLLAPSE / ARISING [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Mathematical Arising Separation & Float Integrity")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Filtration Matrix Purged. Substrate Arisen in Absolute Beauty.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
