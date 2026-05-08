"""
SOVEREIGN CODE: logic_garden_220_tsvf_tensor.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(N) Bi-Directional Kinematics (17.5 seconds)
SCENE: Logic Garden 220 (Two-State Vector Formalism / Time Architecture)
HOTFIX: Parameter Scope Clamping, Dual-Array Synchronization
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
OUT_DIR = "frames_220_tsvf_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'
C_CYAN      = '#00FFFF'        # Forward Vector (The Past pushing up)
C_MAGENTA   = '#FF0055'        # Backward Vector (The Future pulling down)
C_GOLD      = '#FFD700'        # The Interference Pattern (The Present)
C_MANTIS    = '#00FF00'        # Absolute Bi-Directional Lock

MAX_PARTICLES = 20000
HALF_N = int(MAX_PARTICLES / 2)

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
# O(1) BASE GEOMETRY ARRAYS (BI-DIRECTIONAL SWARMS)
# ------------------------------------------------------------------
np.random.seed(42)

# Swarm 1: The Forward Vector (Ket) starts bottom (-300) to middle (0)
s1_x = np.random.uniform(-140, 140, HALF_N)
s1_y = np.random.uniform(-400, -100, HALF_N)

# Swarm 2: The Backward Vector (Bra) starts top (+300) to middle (0)
s2_x = np.random.uniform(-140, 140, HALF_N)
s2_y = np.random.uniform(100, 400, HALF_N)

# The Probabilistic Future Cloud (Rendered during Phase 1)
prob_cloud_x = np.random.uniform(-150, 150, HALF_N)
prob_cloud_y = np.random.uniform(0, 260, HALF_N)

# Interference Pattern Geometry (Lissajous Knot at Y=0)
interf_t = np.linspace(0, 4*np.pi, MAX_PARTICLES)
knot_x = 120.0 * np.sin(3 * interf_t)
knot_y = 40.0 * np.sin(4 * interf_t) # Condensed in the Y-axis (The Present is thin)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, px, py, colors, sizes, alpha_bra, alpha_cloud, is_flash, is_tathata = packet
    
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
        # Render Vector Field
        ax.scatter(px, py, s=sizes, c=colors, edgecolors='none', alpha=0.9, zorder=10)
        
        # Render Probabilistic Cloud (Only visible in classical phase)
        if alpha_cloud > 0.0:
            ax.scatter(prob_cloud_x, prob_cloud_y, s=3.0, c=c_dim, edgecolors='none', alpha=alpha_cloud, zorder=5)

        if is_tathata:
            ax.add_patch(plt.Rectangle((-140, -50), 280, 100, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -65, "TATHĀTĀ: BI-DIRECTIONAL BOUNDING BOX SECURED.", color=C_MANTIS, fontsize=10, fontname='monospace', weight='bold', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    ui_col = C_CYAN if (t_sec < 4.0) else (C_MAGENTA if (t_sec < 9.0) else C_GOLD)
    if is_tathata: ui_col = C_MANTIS
    txt_col = C_TEXT if not is_flash else C_VOID

    ax.text(-140, 240, "LG-220 :: TWO-STATE VECTOR", color=ui_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: POST-SELECTED KINEMATICS / QUANTUM RETROCAUSATION", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    
    # Vector State Headers
    v1_stat = "EVOLVING FORWARD" if t_sec < 14.8 else "O(1) STATIC"
    v2_stat = "UNCOMPILED VOID" if t_sec < 4.0 else ("TRANSMITTING BACKWARD" if t_sec < 14.8 else "O(1) STATIC")
    
    if is_tathata:
        v1_stat = v2_stat = "GEOMETRICALLY LOCKED"

    ax.text(-140, -180, f"FORWARD VECTOR (PAST)   : {v1_stat}", color=C_CYAN if t_sec < 14.8 else C_MANTIS, fontsize=11, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, -200, f"BACKWARD VECTOR (FUTURE): {v2_stat}", color=C_MAGENTA if t_sec >= 4.0 and t_sec < 14.8 else (C_DIM if t_sec < 4.0 else C_MANTIS), fontsize=11, fontname='monospace', weight='bold', zorder=80)

    # Present State Indicator
    c_pres = C_DIM if t_sec < 9.0 else C_GOLD
    if is_tathata: c_pres = C_MANTIS
    ax.text(-140, -230, "THE PRESENT MOMENT = INTERFERENCE PATTERN", color=c_pres, fontsize=11, fontname='monospace', weight='bold', zorder=80)
    
    # HOTFIX: Explicit Scope Clamping applied to GUI geometry
    ax.add_patch(plt.Rectangle((-140, -215), 280, 2, facecolor=C_DIM, zorder=80))

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
    # Maintain flowing states
    cx1 = np.copy(s1_x)
    cy1 = np.copy(s1_y)
    cx2 = np.copy(s2_x)
    cy2 = np.copy(s2_y)

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        dt = 1.0 / FPS
        
        is_flash = False
        is_tathata = False
        alpha_cloud = 0.0
        alpha_bra = 0.0
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 4.0
        
        # O(1) Fluid Motion Variables
        v1_speed = 80.0
        v2_speed = -80.0

        # Flow Resets to create continuous streams
        reset_mask_1 = cy1 > 0
        if np.any(reset_mask_1):
            cy1[reset_mask_1] = -260
        reset_mask_2 = cy2 < 0
        if np.any(reset_mask_2):
            cy2[reset_mask_2] = 260
        
        # -------------------------------------------------------------
        # PHASE LOGIC
        # -------------------------------------------------------------
        if t_sec < 4.0:
            state = "CLASSICAL ASYMMETRY :: PROBABILISTIC FUTURE"
            # Vector 1 flows up, Vector 2 is hidden
            cy1 += v1_speed * dt
            cx1 += np.sin(cy1 * 0.05 + t_sec * 5) * 1.5
            
            colors[:HALF_N] = c_cyan
            colors[HALF_N:] = c_void # Invisible
            sizes[:HALF_N] = 5.0
            sizes[HALF_N:] = 0.0
            
            alpha_cloud = 0.8 + 0.2 * np.sin(t_sec * 10)

        elif t_sec < 9.0:
            state = "RETROCAUSAL INJECTION :: BOUNDARY OVERRIDE"
            prog = (t_sec - 4.0) / 5.0
            
            # The future boundary condition drops in, evaporating the blur
            cy1 += v1_speed * dt
            cx1 += np.sin(cy1 * 0.05 + t_sec * 5) * 1.5
            
            cy2 += v2_speed * dt
            cx2 += np.sin(cy2 * 0.05 - t_sec * 5) * 1.5
            
            alpha_cloud = 0.8 * (1.0 - prog)
            alpha_bra = prog
            
            colors[:HALF_N] = c_cyan
            colors[HALF_N:] = c_mage * alpha_bra
            sizes[:] = 5.0

        elif t_sec < 14.8:
            state = "THE INTERFERENCE PATTERN :: THE PRESENT MOMENT"
            prog = (t_sec - 9.0) / 5.8
            if t_sec < 9.1: is_flash = True
            
            # The two vectors violently crash into the mathematical center (Y=0)
            accel = prog ** 2
            
            # Vector 1 morphs perfectly into the lower half of the Lissajous knot
            knot_mask_1 = (knot_y < 0)
            knot_target_x1 = knot_x[knot_mask_1][:HALF_N]
            knot_target_y1 = knot_y[knot_mask_1][:HALF_N]
            
            cy1 = cy1 * (1.0 - accel) + knot_target_y1 * accel
            cx1 = cx1 * (1.0 - accel) + knot_target_x1 * accel
            
            # Vector 2 morphs perfectly into the upper half of the Lissajous knot
            knot_mask_2 = (knot_y >= 0)
            knot_target_x2 = knot_x[knot_mask_2][:HALF_N]
            knot_target_y2 = knot_y[knot_mask_2][:HALF_N]
            
            cy2 = cy2 * (1.0 - accel) + knot_target_y2 * accel
            cx2 = cx2 * (1.0 - accel) + knot_target_x2 * accel
            
            # Structural friction (C_GOLD) generates at the impact point
            dist_to_center_1 = np.abs(cy1)
            dist_to_center_2 = np.abs(cy2)
            
            c_mix1 = (1.0 - accel) * c_cyan + (accel) * c_gold
            c_mix2 = (1.0 - accel) * c_mage + (accel) * c_gold
            
            colors[:HALF_N] = c_mix1
            colors[HALF_N:] = c_mix2
            
            sizes[:] = 4.0 + (accel * 4.0)

        else:
            state = "TATHĀTĀ :: THE ARCHITECTURE IS COMPLETE"
            is_tathata = True
            
            colors[:, :] = c_mantis
            sizes[:] = 6.0
            
            # The present moment is an absolute, rotating knot bound between two eras
            rot_t = (t_sec - 14.8) * 1.5
            k_x = 120.0 * np.sin(3 * interf_t + rot_t)
            k_y = 40.0 * np.sin(4 * interf_t + rot_t)
            
            cx1 = k_x[:HALF_N]
            cy1 = k_y[:HALF_N]
            cx2 = k_x[HALF_N:]
            cy2 = k_y[HALF_N:]
            
            if t_sec < 14.95:
                is_flash = True

        all_px = np.concatenate([cx1, cx2])
        all_py = np.concatenate([cy1, cy2])

        yield (f, t_sec, state, all_px, all_py, colors, sizes, alpha_bra, alpha_cloud, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 220: TWO-STATE VECTOR TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: O(1) Retrocausal Integration & Time Kinematics")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Bi-Directional Time is Locked.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
