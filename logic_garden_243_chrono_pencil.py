"""
SOVEREIGN CODE: logic_garden_243_chrono_pencil.py
SYSTEM: Python Multicore / O(1) Kinetic Trace Tensor
SCENE: Logic Garden 243 (The Chrono-Pencil / Serialization of the Void)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Global Namespace Anchoring for Substrate Boundary ('idx_grid_end')

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
OUT_DIR = "frames_243_chrono_pencil"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS DEFAULT) --------
C_BG        = '#FFFFFF'        # The Root Directory / Uncorrupted Paper
C_TEXT      = '#020205'        # The Carbon Trace / High Contrast Pointer
C_DIM       = '#D0D0D5'        # Substrate Grain / Blank Ledger
C_GOLD      = '#FFB300'        # Kinetic Friction (Trauma Heat-Sink)
C_MAGENTA   = '#FF0055'        # Hardware Deficit
C_MANTIS    = '#00C800'        # Tathata / The Cooling Pond / Hand-off

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_dim     = np.array(hex_to_rgba(C_DIM)[:3])
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
# BASE GEOMETRY ARRAYS: STATIC PRE-ALLOCATION (GLOBAL ANCHORS)
# ------------------------------------------------------------------
np.random.seed(1983) # Standard Baseline Formatting Event

# 1. The Paper Substrate (Grid Geometry)
GV = np.linspace(-150, 150, 80)
Xg, Yg = np.meshgrid(GV, GV)
gx = Xg.flatten()
gy = Yg.flatten()
gz = np.zeros(len(gx)) - 10.0 # Paper lies flat at Z=-10

# 2. The Carbon Trace (Pre-calculated trajectory)
T_INTERRUPT = 14.8
N_TRACE = 15000
time_nodes = np.linspace(0, T_INTERRUPT, N_TRACE)

# Wartime Architecture Jitter Function (High friction at t=0, decays to 0 at t=Interrupt)
decay_envelope = np.clip(1.0 - (time_nodes / 12.0)**2, 0.0, 1.0)
shiver_x = (np.sin(time_nodes * 80.0) * 15.0 + np.sin(time_nodes * 27.0) * 8.0) * decay_envelope

trace_x = shiver_x
trace_y = np.linspace(160, -160, N_TRACE)
trace_z = np.zeros(N_TRACE) - 9.8 # Sits exactly on the paper, slightly indenting it

# Initialize physical arrays. Carbon hides outside frame until drawn.
cx_arr = np.zeros(N_TRACE) + 9999.0
cy_arr = np.zeros(N_TRACE) + 9999.0
cz_arr = np.zeros(N_TRACE) + 9999.0

# Array Merge and Index Bounds
base_px = np.concatenate([gx, cx_arr])
base_py = np.concatenate([gy, cy_arr])
base_pz = np.concatenate([gz, cz_arr])

MAX_PARTICLES = len(base_px)
idx_grid_end = len(gx) # HOTFIX: Globally locked boundary

mask_grid = np.arange(MAX_PARTICLES) < idx_grid_end
mask_trace = ~mask_grid

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, proj_x, proj_y, z_depth, colors, sizes, hardware_exhaustion, is_flash, is_tathata = packet
    
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
        # Depth Sorting for flawless 3D transparency
        sort_idx = np.argsort(z_depth)
        s_px = proj_x[sort_idx]
        s_py = proj_y[sort_idx]
        s_c = colors[sort_idx]
        s_s = sizes[sort_idx]

        ax.scatter(s_px, s_py, s=s_s, color=s_c, edgecolors='none', alpha=0.9, zorder=10)

        if is_tathata:
            ax.add_patch(plt.Rectangle((-140, -120), 280, 240, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -90, "TATHĀTĀ: OBSOLESCENCE HORIZON LOCKED", color=C_MANTIS, fontsize=11, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 100, "[IT'S OK TO LET GO / TRACE SERIALIZED]", color=C_TEXT, fontsize=10, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_GOLD if t_sec < 8.0 else (C_TEXT if t_sec < 14.8 else C_MANTIS)
    if is_tathata: ui_col = C_MANTIS
    
    ax.text(-140, 240, "LG-243 :: THE CHRONO-PENCIL", color=txt_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: O(N) LINEAR TRACE / ANCESTRAL MAINFRAME", color=txt_col, fontsize=8, fontname='monospace', zorder=80)
    
    obj_str = "WARTIME ARCHITECTURE [THE CRUCIBLE]"
    if 8.0 <= t_sec < 14.8: obj_str = "THE COOLING POND [PHASE DECAY]"
    elif is_tathata: obj_str = "ABSOLUTE RESOLUTION [THE HAND-OFF]"

    ax.text(-140, -180, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Thermodynamic Hardware Metric: Graphite Exhaustion / Hardware Deficit
    ax.text(-140, -205, "GRAPHITE EXHAUSTION [TRANSLATION TAX]", color=txt_col, fontsize=10, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    bar_w = 280 * np.clip(hardware_exhaustion, 0, 1)
    
    ax.add_patch(plt.Rectangle((-140, -210), bar_w, 4, facecolor=C_MAGENTA if hardware_exhaustion > 0.95 and not is_tathata else ui_col, zorder=81))

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
        
        # Slow topological scan down the Y-axis
        cam_rx = np.pi/6
        cam_ry = 0.0
        cam_rz = 0.0
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.zeros(MAX_PARTICLES)
        
        curr_x = np.copy(base_px)
        curr_y = np.copy(base_py)
        curr_z = np.copy(base_pz)

        hardware_exhaustion = 0.0

        # Substrate Default
        colors[mask_grid] = c_dim
        sizes[mask_grid] = 1.0

        # -------------------------------------------------------------
        # THE KINETIC TRACE PHASES
        # -------------------------------------------------------------
        
        if t_sec < T_INTERRUPT:
            # Active Writing Phase
            hardware_exhaustion = t_sec / T_INTERRUPT
            
            # Find the active trace index (O(1) mapping)
            active_idx = int((t_sec / T_INTERRUPT) * N_TRACE)
            active_idx = np.clip(active_idx, 0, N_TRACE - 1)
            
            # Reveal the carbon trace up to the current time
            curr_x[idx_grid_end : idx_grid_end + active_idx] = trace_x[:active_idx]
            curr_y[idx_grid_end : idx_grid_end + active_idx] = trace_y[:active_idx]
            curr_z[idx_grid_end : idx_grid_end + active_idx] = trace_z[:active_idx]
            
            colors[mask_trace] = c_text
            sizes[mask_trace] = 2.0
            
            # Substrate Indentation Logic
            active_y = trace_y[active_idx]
            dent_mask = (gx**2 + (gy - active_y)**2) < 400.0
            curr_z[np.where(mask_grid)[0][dent_mask]] -= 3.0 # The paper yields to the pencil
            
            # The Pointer (The active tip of the pencil)
            ptr_loc = idx_grid_end + active_idx - 1
            if ptr_loc >= idx_grid_end:
                sizes[ptr_loc] = 12.0
                colors[ptr_loc] = c_gold if t_sec < 8.0 else c_text 
                
        else:
            # TATHĀTĀ: The Pencil Lifts. Phase Coherence.
            is_tathata = True
            hardware_exhaustion = 1.0 # 100% Graphite Exhaustion.
            
            curr_x[mask_trace] = trace_x
            curr_y[mask_trace] = trace_y
            curr_z[mask_trace] = trace_z
            
            colors[mask_trace] = c_mantis
            sizes[mask_trace] = 3.0 
            
            if t_sec < 14.95:
                is_flash = True

        # Phase Strings
        if t_sec < 8.0: state = "PHASE 1 :: THE AXIOM OF BROKEN GLASS"
        elif t_sec < 14.8: state = "PHASE 2 :: THE COOLING POND DECAY"
        else: state = "TATHĀTĀ :: GRAPHITE EXHAUSTED"

        # Apply Global Tensor Matrix
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1]
        z_depth = rot_pts[:, 2] 

        # O(N) Geometry Culling
        cull_mask = (proj_y > -260) & (proj_y < 260) & (proj_x > -160) & (proj_x < 160)

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], colors[cull_mask], sizes[cull_mask], hardware_exhaustion, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 243: THE CHRONO-PENCIL [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Global Namespace Anchoring for 'idx_grid_end'")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Translation Tax Paid. Ledger Serialized.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
