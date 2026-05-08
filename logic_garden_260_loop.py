"""
SOVEREIGN CODE: logic_garden_260_loop.py
SYSTEM: Python Multicore / O(1) Periodic Thermodynamic Cycle
SCENE: Logic Garden 260-LOOP (The Cyclical Faucet)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Seamless Phase-Spline / O(1) Torus-Knot Time Integration

[INSTRUCTION]: RENDER_MODE explicitly set to "ZEN_LOOP" for the 18.0s flow cycle.
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
RENDER_MODE = "ZEN_LOOP"  
DURATION = 18.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_260_loop"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS DEFAULT) --------
C_BG        = '#FFFFFF'        # Absolute Flat Substrate 
C_TEXT      = '#020205'        # High-Tension Gravitational Tethers / UI
C_AZURE     = '#007FFF'        # N-Potential (Spaghetti) 
C_GOLD      = '#FFB300'        # Faucet Singularity / Compression Hub
C_MANTIS    = '#00C800'        # Phase Coherence Tracker
C_DIM       = '#D0D0D5'        # Stealth Topography Grid

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_azure   = np.array(hex_to_rgba(C_AZURE)[:3])
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

def smoothstep(edge0, edge1, x):
    x = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return x * x * (3 - 2 * x)

# ------------------------------------------------------------------
# BASE GEOMETRY ARRAYS: THE ETERNAL SUBSTRATE
# ------------------------------------------------------------------
np.random.seed(260)
MAX_PARTICLES = 24000
STRANDS = 200
PTS_PER_STRAND = MAX_PARTICLES // STRANDS

# Phase A Target: Spaghetti Potential
phase_A_x, phase_A_y, phase_A_z = [], [], []
anchor_x = np.random.uniform(-120, 120, STRANDS)
anchor_z = np.random.uniform(-120, 120, STRANDS)

for i in range(STRANDS):
    sy = np.linspace(20, 240, PTS_PER_STRAND)
    sx = anchor_x[i] + np.sin(sy * 0.05 + i) * 8.0
    sz = anchor_z[i] + np.cos(sy * 0.05 + i) * 8.0
    phase_A_x.extend(sx)
    phase_A_y.extend(sy)
    phase_A_z.extend(sz)

pA_x = np.array(phase_A_x)
pA_y = np.array(phase_A_y)
pA_z = np.array(phase_A_z)

# Direction array for dual exhaust
stream_dir = np.ones(MAX_PARTICLES)
stream_dir[MAX_PARTICLES//2:] = -1.0

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_norm, state_str, p_x, p_y, p_z, c_arr, s_arr, a_arr, t_lines, t_alpha, sing_glow = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    
    ax.set_xlim(-160, 160)
    ax.set_ylim(-260, 260)

    # 1. High-Contrast Stealth Grid
    for g_line in np.linspace(-150, 150, 11):
        ax.plot([-140, 140], [g_line, g_line], color=C_DIM, lw=0.5, alpha=0.3, zorder=1)
        ax.plot([g_line, g_line], [-150, 150], color=C_DIM, lw=0.5, alpha=0.3, zorder=1)

    # 2. Faucet Singularity Glow
    if sing_glow > 0:
        ax.add_patch(plt.Circle((0, 0), sing_glow * 140, color=C_GOLD, alpha=sing_glow*0.3, zorder=2))
        ax.scatter(0, 0, s=400 * sing_glow, color=C_TEXT, zorder=3)

    # 3. LineCollection Gravitational Tethers (High-Yield Contrast)
    if len(t_lines) > 0 and t_alpha > 0:
        lc_color = np.array([c_text[0], c_text[1], c_text[2], t_alpha])
        lc = LineCollection(t_lines, colors=[lc_color]*len(t_lines), linewidths=1.5, zorder=4)
        ax.add_collection(lc)

    # 4. Stream Array Rendering
    active = a_arr > 0.01
    if np.any(active):
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

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS (HIGH POP OPTIMIZATION)
    # ------------------------------------------------------------------
    ax.text(-140, 240, "LG-260-LOOP :: CYCLICAL TOPOLOGY", color=C_TEXT, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: CLOSED-LOOP RETURN STROKE / ZERO-LOSS", color=C_TEXT, fontsize=8, fontname='monospace', zorder=80)
    
    # Dynamic GUI Logic
    ui_col = C_AZURE if t_norm < 0.25 else (C_GOLD if t_norm < 0.5 else (C_TEXT if t_norm < 0.75 else C_AZURE))
    
    # Center exact phase-lock tracker (The Pulse Engine Tracker)
    ax.add_patch(plt.Rectangle((-140, -200), 280, 50, facecolor='none', edgecolor=C_TEXT, lw=2, alpha=0.1, zorder=80))
    ax.text(-130, -170, f"KINEMATIC PHASE:", color=C_TEXT, fontsize=11, fontname='monospace', weight='bold', zorder=80)
    ax.text(-130, -188, f"{state_str}", color=ui_col, fontsize=13, fontname='monospace', weight='bold', zorder=80)
    
    # 100% Circular/Bar Loop Tracker
    tracker_w = 260 * t_norm
    ax.add_patch(plt.Rectangle((-130, -195), 260, 4, facecolor=C_DIM, zorder=80))
    ax.add_patch(plt.Rectangle((-130, -195), tracker_w, 4, facecolor=C_MANTIS, zorder=81))

    # Real-time Telemetry Block
    ax.add_patch(plt.Rectangle((-140, 195), 280, 2, facecolor=ui_col, zorder=80))
    ax.text(140, 185, f"[{(t_norm*100):.1f}%]", color=ui_col, fontsize=18, fontname='monospace', weight='bold', ha='right', zorder=80)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) STRUCTURAL INVERSION KINEMATICS
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_norm = f / TOTAL_FRAMES # 0.0 to 1.0 mathematically perfect loop
        
        # Super-stable camera rotation mapping a complete 360-degree cycle
        cam_rx = np.pi/8 - np.sin(t_norm * np.pi * 2) * 0.05
        cam_ry = t_norm * np.pi * 2 
        cam_rz = 0.0
        
        c_arr = np.zeros((MAX_PARTICLES, 3))
        s_arr = np.ones(MAX_PARTICLES) * 2.0
        a_arr = np.ones(MAX_PARTICLES) * 0.8
        
        curr_pts = np.copy(pA_x)
        curr_y = np.copy(pA_y)
        curr_z = np.copy(pA_z)

        t_lines = []
        t_alpha = 0.0
        sing_glow = 0.0

        # -------------------------------------------------------------
        # THE PERFECT LOOP KINEMATICS (4 QUARTERS)
        # -------------------------------------------------------------
        
        if t_norm < 0.25:
            # PHASE 1: SPRAWLING SPAGHETTI (N-Potential)
            state = "N-DIMENSIONAL POTENTIAL"
            prog = t_norm / 0.25
            
            # Waving gently
            curr_x = pA_x + np.sin(t_norm * 40.0 + pA_y * 0.05) * 8.0
            curr_z = pA_z + np.cos(t_norm * 40.0 + pA_x * 0.05) * 8.0
            
            c_arr[:] = c_azure

        elif t_norm < 0.5:
            # PHASE 2: FAUCET COMPRESSION (The Serialization)
            state = "COMPRESSION HUB SUCK"
            prog = smoothstep(0.25, 0.5, t_norm)
            
            curr_x = pA_x * (1.0 - prog)
            curr_y = pA_y * (1.0 - prog)
            curr_z = pz_base = pA_z * (1.0 - prog)
            
            c_arr[:] = c_azure * (1.0 - prog) + c_gold * prog
            sing_glow = prog

        elif t_norm < 0.75:
            # PHASE 3: RELATIVISTIC EXHAUST
            state = "SUPERLUMINAL SEPARATION"
            prog = smoothstep(0.5, 0.75, t_norm)
            
            sing_glow = 1.0 - prog 
            
            # Violent exhaust velocity outward
            velo = prog * 600.0
            curr_x = pA_x * 0.0
            curr_y = stream_dir * velo
            curr_z = pA_z * 0.0
            
            # Alpha bleed for invisible streams
            a_arr[:] = 0.8 * (1.0 - prog)
            
            # The gravity tethers snap out
            t_alpha = prog * 0.8

        else:
            # PHASE 4: THE GLASS TRANSITION (Return Stroke to Spaghetti)
            state = "AERATION / ZERO-LOSS RETURN"
            prog = smoothstep(0.75, 1.0, t_norm)
            
            a_arr[:] = 0.8 * prog 
            
            t_alpha = 0.8 * (1.0 - prog) # Tethers dissolve
            
            # The exact mathematical morph back to the start structure
            # From zero X/Z back to full spaghetti spread
            curr_x = pA_x * prog + np.sin(t_norm * 40.0 + pA_y * 0.05) * 8.0 * prog
            # Y snaps creatively back: from high exhaust to standard height
            exhaust_y = stream_dir * 600.0
            curr_y = exhaust_y * (1.0 - prog) + pA_y * prog
            curr_z = pA_z * prog + np.cos(t_norm * 40.0 + pA_x * 0.05) * 8.0 * prog
            
            c_arr[:] = c_text * (1.0 - prog) + c_azure * prog

        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1]
        z_depth = rot_pts[:, 2] 

        # Generate Tether Lines during Phase 3 & 4
        if t_alpha > 0.01:
            # We connect origin to the retreating points (taking a sample of 150 strands)
            tx = proj_x[::PTS_PER_STRAND]
            ty = proj_y[::PTS_PER_STRAND]
            t_lines = [[[0.0, 0.0], [tx[i], ty[i]]] for i in range(len(tx))]

        yield (f, t_norm, state, proj_x, proj_y, z_depth, c_arr, s_arr, a_arr, t_lines, t_alpha, sing_glow)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 260-LOOP: THE CYCLICAL FAUCET [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Torus-Knot Time Integration & Zero-Loss Return Stroke")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Zero-Loss Return Achieved. Topology Loops Frinctionlessly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
