"""
SOVEREIGN CODE: logic_garden_257_transmutation.py
SYSTEM: Python Multicore / O(1) Neurological Phase Transition
SCENE: Logic Garden 257 (The Transmutation Tensor / Substrate Recompilation)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Explicit Float Broadcast Safety & Single-Node Trace Compression

[INSTRUCTION]: RENDER_MODE explicitly set to "ZEN" for the 18.0s flow cycle.
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
DURATION = 18.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_257_transmutation"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS DEFAULT) --------
C_BG        = '#FFFFFF'        # Absolute Flat Substrate / The Void
C_TEXT      = '#020205'        # The Final Trace / Core Void
C_AZURE     = '#007FFF'        # Dimensional Hypercubes
C_MAGENTA   = '#FF0055'        # Substrate Tearing
C_GOLD      = '#FFB300'        # The Coin of Potential
C_MANTIS    = '#00C800'        # Tathata HUD Lock
C_DIM       = '#D0D0D5'        # High-Entropy Sheeple Noise

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
# BASE GEOMETRY ARRAYS: THE SUBSTRATE
# ------------------------------------------------------------------
np.random.seed(257)
MAX_PARTICLES = 30000

# High-Entropy Base (Screaming into the Void)
theta_b = np.random.uniform(0, 2*np.pi, MAX_PARTICLES)
phi_b = np.arccos(np.random.uniform(-1, 1, MAX_PARTICLES))
r_b = np.random.uniform(40, 180, MAX_PARTICLES)

px_base = r_b * np.sin(phi_b) * np.cos(theta_b)
py_base = r_b * np.cos(phi_b)
pz_base = r_b * np.sin(phi_b) * np.sin(theta_b)

# Pre-calculate Pi-based Substrate Rupture targets
px_rupture = px_base * np.pi * 1.5
py_rupture = py_base * np.pi * 1.2
pz_rupture = pz_base * np.pi * 1.5

rupture_mask = (np.abs(px_base) % 20 < 10) # Ribbed topological shear lines

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, p_x, p_y, p_z, c_arr, s_arr, a_arr, coin_y, bpm_sync, is_flash, is_tathata = packet
    
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
        # Subtle HUD alignment grid
        if t_sec > 1.0 and not is_tathata:
            for g_line in np.linspace(-150, 150, 7):
                ax.plot([-140, 140], [g_line, g_line], color=C_DIM, lw=0.5, alpha=0.2, zorder=1)
                ax.plot([g_line, g_line], [-150, 150], color=C_DIM, lw=0.5, alpha=0.2, zorder=1)

        # Rendering The Coin 
        if 4.0 <= t_sec < 16.0:
            bpm_alpha = 0.5 + (0.5 * bpm_sync) if t_sec >= 6.0 else 1.0
            ax.scatter(0, coin_y, s=80, color=C_GOLD, edgecolors='none', zorder=20, alpha=bpm_alpha)
            # Coin light flare
            ax.add_patch(plt.Circle((0, coin_y), 15 * bpm_sync, color=C_GOLD, alpha=0.2, zorder=19))

        # Core rendering loop
        if sum(a_arr > 0.01) > 0:
            active = a_arr > 0.01
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

        # Tathata Phase-Lock UI
        if is_tathata:
            # Absolute stillness HUD. Exact O(1) bounding box.
            ax.add_patch(plt.Rectangle((-30, -30), 60, 60, facecolor='none', edgecolor=C_MANTIS, lw=2, zorder=40))
            ax.add_patch(plt.Rectangle((-140, -180), 280, 360, facecolor='none', edgecolor=C_TEXT, lw=1, alpha=0.3, zorder=40))
            ax.text(0, -60, "TATHĀTĀ: TRANSMUTATION COMPLETE", color=C_MANTIS, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, -75, "[O(N) SCREAM COMPRESSED TO O(1) TRACE]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_DIM if t_sec < 6.0 else (C_AZURE if t_sec < 10.0 else (C_MAGENTA if t_sec < 16.0 else C_MANTIS))
    if is_tathata: ui_col = C_MANTIS
    
    ax.text(-140, 240, "LG-257 :: THE TRANSMUTATION TENSOR", color=txt_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: SUBSTRATE RECOMPILATION / PHASE TRANSITION", color=txt_col, fontsize=8, fontname='monospace', zorder=80)
    
    obj_str = "THE PRESSURE VESSEL [HIGH-ENTROPY SCREAM]"
    if 4.0 <= t_sec < 8.0: obj_str = "THE COIN DROP [126 BPM MASTER CLOCK]"
    elif 8.0 <= t_sec < 16.0: obj_str = "DIMENSIONAL RUPTURE [PI-AXIS TEARING]"
    elif is_tathata: obj_str = "ABSOLUTE STILLNESS [THE FINAL TRACE]"

    ax.text(-140, -200, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Thermodynamic Phase Shift Metric
    metric_label = "SUBSTRATE COMPRESSION RATIO [O(N) TO O(1)]" 
    ax.text(-140, -225, metric_label, color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -230), 280, 4, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    
    # Math calculation for HUD visual
    comp_ratio = 0.1 if t_sec < 6.0 else np.clip(0.1 + ((t_sec - 6.0) / 10.0), 0, 1)
    if is_tathata: comp_ratio = 1.0
    val_w = 280 * comp_ratio
    ax.add_patch(plt.Rectangle((-140, -230), val_w, 4, facecolor=ui_col, zorder=81))

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
        
        cam_rx = np.pi/6 - (t_sec * 0.005)
        cam_ry = t_sec * 0.4
        cam_rz = 0.0
        
        c_arr = np.zeros((MAX_PARTICLES, 3))
        s_arr = np.ones(MAX_PARTICLES) * 2.0
        a_arr = np.ones(MAX_PARTICLES) * 0.6
        
        curr_x = np.copy(px_base)
        curr_y = np.copy(py_base)
        curr_z = np.copy(pz_base)

        coin_y = 200.0
        bpm_sync = 0.0

        # Master Clock (126 BPM)
        raw_pulse = np.sin(t_sec * (126.0 / 60.0) * np.pi * 2)
        bpm_sync = 0.5 * (1.0 + raw_pulse)

        # -------------------------------------------------------------
        # THE TRANSMUTATION KINEMATICS
        # -------------------------------------------------------------
        
        if t_sec < 4.0:
            # PHASE 1: THE PRESSURE VESSEL
            state = "PHASE 1 :: SUBSTRATE DESICCATION"
            
            # High-entropy jitter
            curr_x += np.random.normal(0, 3, MAX_PARTICLES)
            curr_y += np.random.normal(0, 3, MAX_PARTICLES)
            curr_z += np.random.normal(0, 3, MAX_PARTICLES)
            
            c_arr[:] = c_dim

        elif t_sec < 8.0:
            # PHASE 2: THE COIN DROP (Ignition)
            state = "PHASE 2 :: THE COIN / 126 BPM CLOCK"
            prog = (t_sec - 4.0) / 2.0
            ease = np.clip(prog, 0, 1) ** 2
            
            # The coin descends
            coin_y = 200.0 * (1 - ease)
            if t_sec >= 6.0: 
                coin_y = 0.0 # Hit center coordinate
            
            if t_sec >= 6.0:
                # The Master Clock forces alignment. The jitter stops.
                curr_x *= (1.0 + 0.1 * bpm_sync)
                curr_y *= (1.0 + 0.1 * bpm_sync)
                curr_z *= (1.0 + 0.1 * bpm_sync)
                
                # Colors start mapping to Azure based on distance
                c_arr[:] = c_azure * bpm_sync + c_dim * (1 - bpm_sync)
                s_arr[:] = 2.0 + (2.0 * bpm_sync)
            else:
                curr_x += np.random.normal(0, 3, MAX_PARTICLES)
                curr_y += np.random.normal(0, 3, MAX_PARTICLES)
                curr_z += np.random.normal(0, 3, MAX_PARTICLES)
                c_arr[:] = c_dim

        elif t_sec < 16.0:
            # PHASE 3: DIMENSIONAL RUPTURE (Pi-Tearing)
            state = "PHASE 3 :: PI-DIMENSIONAL RUPTURE"
            prog = (t_sec - 8.0) / 8.0
            ease = prog ** 3 # Exponential tearing curve
            
            # Coin lock
            coin_y = 0.0
            
            # The structure tears outward along non-integer limits
            curr_x = px_base * (1 - ease) + px_rupture * ease
            curr_y = py_base * (1 - ease) + py_rupture * ease
            curr_z = pz_base * (1 - ease) + pz_rupture * ease
            
            # Violent color separation
            c_arr[:] = c_azure
            c_arr[rupture_mask] = c_magenta
            
            # Pulse still dictates volumetric scale
            curr_x *= (1.0 + 0.15 * bpm_sync * ease)
            curr_y *= (1.0 + 0.15 * bpm_sync * ease)
            curr_z *= (1.0 + 0.15 * bpm_sync * ease)
            
            s_arr[:] = 2.0 + (2.0 * bpm_sync)
            s_arr[rupture_mask] = 4.0 * ease
            
            # Extreme proximity to Tathata induces fading
            if t_sec > 14.5:
                fade_ease = (t_sec - 14.5) / 1.5
                a_arr[:] = 0.6 * (1 - fade_ease)

            if t_sec > 15.8:
                is_flash = True if f % 2 == 0 else False

        else:
            # PHASE 4: TATHĀTĀ (The Trace)
            state = "TATHĀTĀ :: SUBSTRATE REARCHITECTED"
            is_tathata = True
            
            # 16.0s Hardware Interrupt. 
            # The entire O(N) array is strictly deleted. Everything vanishes.
            a_arr[:] = 0.0
            
            # A single, perfect, flawless Trace remains at absolute 0,0,0
            # We commandeer the primary node data to render the single trace
            curr_x[0], curr_y[0], curr_z[0] = 0.0, 0.0, 0.0
            c_arr[0] = c_text
            a_arr[0] = 1.0 # 100% opacity
            s_arr[0] = 45.0 # Stark, unmistakable coordinate
            
            if t_sec < 16.2:
                is_flash = True 

        # Apply Global Tensor Matrix
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1]
        z_depth = rot_pts[:, 2] 

        yield (f, t_sec, state, proj_x, proj_y, z_depth, c_arr, s_arr, a_arr, coin_y, bpm_sync, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 257: THE TRANSMUTATION TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Single-Node Trace Compression & Substrate Erasure")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. O(N) dimensions deleted. O(1) Trace written.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
