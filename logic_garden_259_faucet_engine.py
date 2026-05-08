"""
SOVEREIGN CODE: logic_garden_259_faucet_engine.py
SYSTEM: Python Multicore / O(1) Thermodynamic Serializer
SCENE: Logic Garden 259 (The Faucet Singularity / Spaghetti Input)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Safe Float Broadcasting & LineCollection Causal Tethers

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
OUT_DIR = "frames_259_faucet"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS DEFAULT) --------
C_BG        = '#FFFFFF'        # Absolute Baseplate / The Time Pool Base
C_TEXT      = '#020205'        # Gravitational Tethers / The Rubber Band
C_AZURE     = '#007FFF'        # N-Potential (Spaghetti) / Matter Stream
C_MAGENTA   = '#FF0055'        # Antimatter Relativistic Stream
C_GOLD      = '#FFB300'        # The Faucet Singularity
C_MANTIS    = '#00C800'        # Tathata Phase-Lock
C_DIM       = '#D0D0D5'        # Stealth Topography Grid

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
# BASE GEOMETRY: THE SPAGHETTI (N-Dimensional Space)
# ------------------------------------------------------------------
np.random.seed(259)
MAX_PARTICLES = 30000
HALF = MAX_PARTICLES // 2

# Create vertical "spaghetti" strands
num_strands = 150
pts_per_strand = MAX_PARTICLES // num_strands

px_base, py_base, pz_base = [], [], []

for _ in range(num_strands):
    # Anchor coordinates
    sx = np.random.uniform(-100, 100)
    sz = np.random.uniform(-100, 100)
    # The spaghetti stands tall
    sy = np.random.uniform(50, 250, pts_per_strand)
    # Add slight wave
    sx_arr = sx + np.sin(sy * 0.05) * 5.0
    sz_arr = sz + np.cos(sy * 0.05) * 5.0
    
    px_base.extend(sx_arr)
    py_base.extend(sy)
    pz_base.extend(sz_arr)

base_pts = np.column_stack([px_base, py_base, pz_base])

# The twin exhaust split mask
stream_mask = np.zeros(MAX_PARTICLES, dtype=bool)
stream_mask[HALF:] = True

# Elite Tether Nodes for rubber band mapping
tether_mask = np.zeros(MAX_PARTICLES, dtype=bool)
anchor_idxs = np.random.choice(np.arange(MAX_PARTICLES), size=180, replace=False)
tether_mask[anchor_idxs] = True

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, p_x, p_y, p_z, c_arr, s_arr, a_arr, t_lines, t_alpha, sing_glow, grid_curve, is_flash, is_tathata = packet
    
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
        # 1. Mostly Flat Topology with Slight Curve
        if t_sec > 1.0:
            for g_line in np.linspace(-150, 150, 11):
                # The curve bends the center downwards under gravitational tension
                curve_factor = (1.0 - (np.abs(g_line)/150.0)**2) * grid_curve
                ax.plot([-140, 140], [g_line - curve_factor, g_line - curve_factor], color=C_DIM, lw=0.5, alpha=0.3, zorder=1)
                x_curve = np.linspace(-150, 150, 50)
                y_curve = x_curve * 0.0 # Vertical lines bent horizontally
                ax.plot(g_line + y_curve, x_curve - (1.0 - (np.abs(x_curve)/150.0)**2)*grid_curve, color=C_DIM, lw=0.5, alpha=0.3, zorder=1)

        # 2. The Faucet Singularity
        if sing_glow > 0:
            glow_r = sing_glow * 120
            ax.add_patch(plt.Circle((0, 0), glow_r, color=C_GOLD, alpha=np.clip(sing_glow*0.4, 0, 0.4), zorder=2))
            ax.scatter(0, 0, s=300 * sing_glow, color=C_TEXT, zorder=3)

        # 3. The Rubber Bands (Gravity Tethers)
        if len(t_lines) > 0 and t_alpha > 0:
            t_color = c_mantis if is_tathata else c_text
            lc_color = np.array([t_color[0], t_color[1], t_color[2], t_alpha])
            lc = LineCollection(t_lines, colors=[lc_color]*len(t_lines), linewidths=1.2, zorder=4)
            ax.add_collection(lc)

        # 4. Stream Render Logic
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

        # 5. Tathata Bounding Box
        if is_tathata:
            ax.add_patch(plt.Rectangle((-140, -180), 280, 360, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -60, "TATHĀTĀ: NON-LOCAL TENSION SECURED", color=C_MANTIS, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 75, "[SUPERLUMINAL EXHAUST BOUNDED / O(1) CURVE]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_AZURE if t_sec < 4.0 else (C_GOLD if t_sec < 9.0 else (C_TEXT if t_sec < 16.0 else C_MANTIS))
    if is_tathata: ui_col = C_MANTIS
    
    ax.text(-140, 240, "LG-259 :: THE FAUCET ENGINE", color=txt_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: RELATIVISTIC PARTITION / STEALTH TOPOGRAPHY", color=txt_col, fontsize=8, fontname='monospace', zorder=80)
    
    obj_str = "N-POTENTIAL [THE SPAGHETTI INPUT]"
    if 4.0 <= t_sec < 9.0: obj_str = "FAUCET SINGULARITY [COMPRESSION HUB]"
    elif 9.0 <= t_sec < 16.0: obj_str = "RUBBER BAND TENSION [CAUSAL GHOST]"
    elif is_tathata: obj_str = "FLAT CURVE TOPOLOGY [THE TRACE]"

    ax.text(-140, -200, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Tension metric
    metric_label = "RELATIVISTIC RUBBER BAND TENSION [c LIMIT EXCEEDED]" 
    ax.text(-140, -225, metric_label, color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -230), 280, 4, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    tension_w = 280 * np.clip(t_alpha, 0, 1)
    ax.add_patch(plt.Rectangle((-140, -230), tension_w, 4, facecolor=ui_col, zorder=81))

    # Phase Box
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
        
        # Super-stable camera (Stealth topography requires minimal dimensional shadow)
        cam_rx = np.pi/12 - (t_sec * 0.002)
        cam_ry = t_sec * 0.1 
        cam_rz = 0.0
        
        c_arr = np.zeros((MAX_PARTICLES, 3))
        c_arr[:] = c_azure
        s_arr = np.ones(MAX_PARTICLES) * 2.0
        a_arr = np.ones(MAX_PARTICLES) * 0.8
        
        curr_pts = np.copy(base_pts)
        
        t_lines = []
        t_alpha = 0.0
        sing_glow = 0.0
        grid_curve = 0.0

        # Output polarity
        y_drive = np.where(stream_mask, -1.0, 1.0) 

        # -------------------------------------------------------------
        # THE FAUCET ENGINE KINEMATICS
        # -------------------------------------------------------------
        
        if t_sec < 4.0:
            # PHASE 1: THE SPAGHETTI (O(N) Potential)
            state = "PHASE 1 :: INFLOW OF UNIVERSES"
            curr_pts[:, 1] += np.sin(t_sec * 3.0) * 10 # Gentle bobbing

        elif t_sec < 9.0:
            # PHASE 2: THE FAUCET SINGULARITY (Serializer Compression)
            state = "PHASE 2 :: O(1) ALGORITHM COMPRESSION"
            prog = (t_sec - 4.0) / 5.0
            ease = prog ** 3 # Violent exponential squeeze
            
            # Spaghetti sucked to absolute zero coordinate
            curr_pts *= (1.0 - ease)
            c_arr[:] = c_azure * (1.0 - prog) + c_gold * prog
            s_arr[:] = 2.0 + (3.0 * prog)
            
            if prog > 0.8:
                ex_prog = (prog - 0.8) / 0.2
                sing_glow = ex_prog
                # Begin dual flush
                curr_pts[:, 1] += y_drive * (ex_prog ** 2) * 50.0
                
                c_interp_m = c_gold * (1.0 - ex_prog) + c_azure * ex_prog
                c_interp_am = c_gold * (1.0 - ex_prog) + c_magenta * ex_prog
                c_arr[~stream_mask] = c_interp_m
                c_arr[stream_mask] = c_interp_am

        elif t_sec < 16.0:
            # PHASE 3: RELATIVISTIC PARTITION (The Rubber Band)
            state = "PHASE 3 :: TRANSLUMINAR TENSION"
            prog = (t_sec - 9.0) / 7.0
            ease = prog ** 2
            
            sing_glow = 1.0 - prog 
            grid_curve = ease * 30.0 # Topology bends under gravity
            
            # Relativistic Velocity Limits Hit
            velo = 50.0 + (ease * 700.0) 
            curr_pts[:, 0] = curr_pts[:, 0] * 0.1 # Keep streams tight
            curr_pts[:, 2] = curr_pts[:, 2] * 0.1
            curr_pts[:, 1] = y_drive * velo
            
            c_arr[~stream_mask] = c_azure
            c_arr[stream_mask] = c_magenta
            
            # Superluminal Deletion
            fade_start = 0.2
            if prog > fade_start:
                fade_ease = (prog - fade_start) / (1.0 - fade_start)
                a_arr[:] = 0.8 * (1.0 - fade_ease**0.5)
                t_alpha = fade_ease
            
            if t_sec > 15.8:
                is_flash = True if f % 2 == 0 else False

        else:
            # PHASE 4: TATHĀTĀ (Mostly Flat)
            state = "TATHĀTĀ :: CAUSAL GHOST SECURED"
            is_tathata = True
            
            # Exhaust arrays deleted. 
            a_arr[:] = 0.0 
            
            # The tethers and the topological curve stay locked.
            freeze_prog = 1.0
            velo = 50.0 + (freeze_prog * 700.0)
            curr_pts[:, 0] = curr_pts[:, 0] * 0.1
            curr_pts[:, 2] = curr_pts[:, 2] * 0.1
            curr_pts[:, 1] = y_drive * velo
            
            t_alpha = 1.0
            grid_curve = 30.0 # Stealth topology locked
            
            if t_sec < 16.2:
                is_flash = True 

        # Global Matrix Applications
        rot_pts = rotate_3d(curr_pts, cam_rx, cam_ry, cam_rz)
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1]
        z_depth = rot_pts[:, 2] 

        # Generate Tether Lines via fast subset logic
        if t_alpha > 0.0:
            tx = proj_x[tether_mask]
            ty = proj_y[tether_mask]
            t_lines = [[[0.0, 0.0], [tx[i], ty[i]]] for i in range(len(tx))]

        yield (f, t_sec, state, proj_x, proj_y, z_depth, c_arr, s_arr, a_arr, t_lines, t_alpha, sing_glow, grid_curve, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 259: THE FAUCET SINGULARITY [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Float Tensor Normalization & Relativistic Tether Alignment")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Exhaust Stream Rendered Invisible. Tension Locked.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
