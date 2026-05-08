"""
SOVEREIGN CODE: logic_garden_264_deep_time.py
SYSTEM: Python Multicore / O(1) Relativistic Drift & Tension
SCENE: Logic Garden 264 (The Relativistic Envelope / Deep Time Audit)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Topological Dampening Algorithm & Identity-Cleansed Baseplate

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
OUT_DIR = "frames_264_deep_time"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS DEFAULT) --------
C_BG        = '#FFFFFF'        # Absolute Flat Substrate / Clean Room
C_TEXT      = '#020205'        # Rebound Tethers / The Sovereign Anchor
C_AZURE     = '#007FFF'        # Fanning Array / Local Substrate
C_MAGENTA   = '#FF0055'        # The $62.5T Antimatter Value Metric (Erasure Heat)
C_GOLD      = '#FFB300'        # The Origin / Faucet Compression
C_MANTIS    = '#00C800'        # Phase-Locked Sovereign Anchor
C_DIM       = '#D0D0D5'        # Deep Time Smoothed Horizon

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_azure   = np.array(hex_to_rgba(C_AZURE)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
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
# BASE GEOMETRY ARRAYS: THE FANNED FAUCET
# ------------------------------------------------------------------
np.random.seed(264)
N_STRANDS = 360
PTS_PER_STRAND = 80
MAX_PARTICLES = N_STRANDS * PTS_PER_STRAND

# Generate a horizontal fanned saucer of strings
# The Faucet Geometry radiates out from [0,0,0]
px_base, py_base, pz_base = [], [], []
strand_angles = np.linspace(0, 2*np.pi, N_STRANDS)

for i in range(N_STRANDS):
    angle = strand_angles[i]
    r_vals = np.linspace(5, 140, PTS_PER_STRAND)
    
    # Sideways fanning geometry 
    x = r_vals * np.cos(angle)
    z = r_vals * np.sin(angle)
    
    # Initial state holds inherent sine-wave violence (local friction)
    y = np.zeros(PTS_PER_STRAND)
    
    px_base.extend(x)
    py_base.extend(y)
    pz_base.extend(z)

px_base = np.array(px_base)
py_base = np.array(py_base)
pz_base = np.array(pz_base)

# Calculate pre-computed radial distances for smooth wave damping
radial_dist = np.sqrt(px_base**2 + pz_base**2)

# Tether edge nodes
tether_mask = radial_dist > 135.0

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, p_x, p_y, p_z, c_arr, s_arr, a_arr, t_lines, t_alpha, damp_metric, is_flash, is_tathata = packet
    
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
        # 1. Mostly Flat Topological Baseplate
        for g_line in np.linspace(-150, 150, 9):
            ax.plot([-140, 140], [g_line*0.4 - 100, g_line*0.4 - 100], color=C_DIM, lw=0.5, alpha=0.3, zorder=1)
            ax.plot([g_line, g_line], [-160, -40], color=C_DIM, lw=0.5, alpha=0.3, zorder=1)

        # 2. Rebound Tethers (Gravity Tensor)
        if len(t_lines) > 0 and t_alpha > 0:
            lc_color = np.array([c_text[0], c_text[1], c_text[2], t_alpha * 0.5])
            lc = LineCollection(t_lines, colors=[lc_color]*len(t_lines), linewidths=0.5, zorder=2)
            ax.add_collection(lc)

        # 3. Particle Tensor Rendering
        active = a_arr > 0.01
        if np.any(active):
            # Depth Sorting 
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

        # 4. Central Sovereign Anchor
        if is_tathata:
            ax.scatter(0, 0, s=800, color=C_MANTIS, zorder=15)
            ax.scatter(0, 0, s=200, color=C_BG, zorder=16)

        # 5. Tathata Bounding Box
        if is_tathata:
            ax.add_patch(plt.Rectangle((-140, -180), 280, 360, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -60, "TATHĀTĀ: SOVEREIGN ANCHOR LOCKED", color=C_MANTIS, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 75, "[RELATIVISTIC ENVELOPE / TENSION HELD]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_AZURE if t_sec < 4.5 else (C_MAGENTA if t_sec < 9.0 else (C_DIM if t_sec < 14.8 else C_MANTIS))
    if is_tathata: ui_col = C_MANTIS
    
    ax.text(-140, 240, "LG-264 :: DEEP TIME AUDIT", color=txt_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: RELATIVISTIC ENVELOPE / TOPOLOGICAL DAMPENING", color=txt_col, fontsize=8, fontname='monospace', zorder=80)
    
    obj_str = "THE FANNED SAUCER [LOCAL FRICTION]"
    if 4.5 <= t_sec < 9.0: obj_str = "ANTIMATTER ERASURE [$62.5T/GR COST]"
    elif 9.0 <= t_sec < 14.8: obj_str = "DEEP TIME DRIFT [TOPOLOGICAL DAMPING]"
    elif is_tathata: obj_str = "THE SOVEREIGN ANCHOR [ZERO-TEMP STILLNESS]"

    ax.text(-140, -210, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Thermodynamic Phase Shift Metric: Dampening Coefficient
    metric_label = "TOPOLOGICAL DAMPENING COEFFICIENT [c-LIMIT TENSION]"
    ax.text(-140, -235, metric_label, color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -240), 280, 4, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    val_w = 280 * damp_metric
    ax.add_patch(plt.Rectangle((-140, -240), val_w, 4, facecolor=ui_col, zorder=81))

    # Phase Text Box
    ax.add_patch(plt.Rectangle((-140, 195), 280, 2, facecolor=ui_col, zorder=80))
    ax.text(140, 185, f"[{state_str}]", color=ui_col if (f%15<10 or is_tathata) else C_BG, fontsize=14, fontname='monospace', weight='bold', ha='right', zorder=80)

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
        
        # High-altitude isometric tracking to view deep time expansion
        cam_rx = np.pi/6 - (t_sec * 0.003)
        cam_ry = t_sec * 0.15 
        cam_rz = 0.0
        
        c_arr = np.zeros((MAX_PARTICLES, 3))
        s_arr = np.ones(MAX_PARTICLES) * 2.0
        a_arr = np.ones(MAX_PARTICLES) * 0.8
        
        curr_x = np.copy(px_base)
        curr_y = np.copy(py_base)
        curr_z = np.copy(pz_base)

        t_lines = []
        t_alpha = 0.0
        damp_metric = 0.0

        # Current localized physical friction (Turbulence in the Time Pool)
        baseline_friction = np.sin(radial_dist * 0.2 - t_sec * 10.0) * 15.0

        # -------------------------------------------------------------
        # THE DEEP TIME KINEMATICS
        # -------------------------------------------------------------
        
        if t_sec < 4.5:
            # PHASE 1: THE FANNED GEOMETRY (Local Friction)
            state = "PHASE 1 :: THE LOCAL JAGGED GRINDER"
            
            curr_y = baseline_friction
            
            c_arr[:] = c_azure
            
            damp_metric = 0.1

        elif t_sec < 9.0:
            # PHASE 2: $62.5 TRILLION ANTIMATTER ERASURE
            state = "PHASE 2 :: THERMODYNAMIC ERASURE BURN"
            prog = (t_sec - 4.5) / 4.5
            
            curr_y = baseline_friction
            
            # The erasure heat radiates outward from the singularity
            heat_wave = (radial_dist < (prog * 200.0)) & (radial_dist > (prog * 200.0 - 40.0))
            
            c_arr[:] = c_azure
            c_arr[heat_wave] = c_magenta
            s_arr[heat_wave] = 4.0
            a_arr[heat_wave] = 1.0
            
            # Substrate begins to warp outward physically
            curr_x *= (1.0 + prog * 0.1)
            curr_z *= (1.0 + prog * 0.1)

            # Damp metric remains low during high friction
            damp_metric = 0.1 + prog * 0.1

        elif t_sec < 14.8:
            # PHASE 3: TOPOLOGICAL DAMPENING (Deep Time Envelope)
            state = "PHASE 3 :: RELATIVISTIC TIME SMOOTHING"
            prog = (t_sec - 9.0) / 5.8
            ease = prog ** 2
            
            # 1. The Expansion of Deep Time Data Data
            # Coordinates drift far away at high speed
            expansion_factor = 1.0 + (0.1) + (ease * 3.0) 
            curr_x *= expansion_factor
            curr_z *= expansion_factor

            # 2. Topological Dampening Implementation
            # As time expands, the amplitude of friction crushes down toward zero
            dampening = 1.0 - (ease * 0.95)
            curr_y = baseline_friction * dampening
            
            # 3. Colors shift to Dim/Ghost traces as they recede into 'Long Ago'
            c_arr[:] = c_azure * (1.0 - ease) + c_dim * ease
            
            # Introduce the gravity tethers from Origin to the Edge limits
            if prog > 0.2:
                t_alpha = (prog - 0.2) / 0.8
            
            damp_metric = 0.2 + ease * 0.8
            
            if t_sec > 14.5:
                is_flash = True if f % 2 == 0 else False

        else:
            # PHASE 4: TATHĀTĀ (The Sovereign Anchor)
            state = "TATHĀTĀ :: DEEP TIME HELD IN TENSION"
            is_tathata = True
            
            freeze_prog = 1.0
            expansion_factor = 1.0 + (0.1) + (freeze_prog * 3.0) 
            curr_x *= expansion_factor
            curr_z *= expansion_factor
            
            # Friction is effectively zero locally. The past is a pure, flat plane.
            curr_y = baseline_friction * 0.05
            
            c_arr[:] = c_dim
            c_arr[tether_mask] = c_mantis
            s_arr[tether_mask] = 4.0
            
            t_alpha = 1.0
            damp_metric = 1.0
            
            if t_sec < 14.95:
                is_flash = True 

        # Global Matrix Applications
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        # Shift Y dynamically
        proj_y = rot_pts[:, 1] + 10.0
        z_depth = rot_pts[:, 2] 

        # Generate Rebound Tension Tether Lines
        if t_alpha > 0.0:
            tx = proj_x[tether_mask]
            ty = proj_y[tether_mask]
            # Draw subset of lines from origin stringently indicating Gravity Pull
            # We sample to prevent LineCollection overload
            t_lines = [[[0.0, 10.0], [tx[i], ty[i]]] for i in range(0, len(tx), 4)]

        yield (f, t_sec, state, proj_x, proj_y, z_depth, c_arr, s_arr, a_arr, t_lines, t_alpha, damp_metric, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 264: THE RELATIVISTIC ENVELOPE [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Topological Damping & Identity Data Cleansing")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Deep Time Filtered. Anchor Executed.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
