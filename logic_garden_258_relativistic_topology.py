"""
SOVEREIGN CODE: logic_garden_258_relativistic_topology.py
SYSTEM: Python Multicore / O(1) Superluminal Relativistic Kinematics
SCENE: Logic Garden 258 (Relativistic Topology / Cavitation Void)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Gravity Tether LineCollection & Superluminal Alpha Bleed

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
OUT_DIR = "frames_258_relativistic"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS) --------
C_BG        = '#FFFFFF'        # Absolute Baseplate / The Time Pool Base
C_TEXT      = '#020205'        # Gravitational Tethers / Ghost Physics
C_AZURE     = '#007FFF'        # Matter Stream (North Exhaust)
C_MAGENTA   = '#FF0055'        # Antimatter Stream (South Exhaust)
C_CYAN      = '#00E5FF'        # Pre-Ignition Universes (Nucleation Bubbles)
C_GOLD      = '#FFB300'        # The Vortex / Reciprocal Engine Core
C_MANTIS    = '#00C800'        # Tathata Phase-Lock
C_DIM       = '#D0D0D5'        # Structural Grid

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_azure   = np.array(hex_to_rgba(C_AZURE)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_cyan    = np.array(hex_to_rgba(C_CYAN)[:3])
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
# BASE GEOMETRY ARRAYS: N-UNIVERSES (THE TIME POOL)
# ------------------------------------------------------------------
np.random.seed(258)
MAX_PARTICLES = 30000
N_BUBBLES = 12

# Distribute particles across N nucleation bubbles
bubble_origins = np.random.uniform(-140, 140, (N_BUBBLES, 3))
bubble_origins[:, 1] *= 0.5 # Flatten slightly

px_base, py_base, pz_base = [], [], []
stream_id = [] # Track which exhaust port they will take (0=Matter, 1=Antimatter)

pts_per_bubble = MAX_PARTICLES // N_BUBBLES
for i in range(N_BUBBLES):
    origin = bubble_origins[i]
    r = np.random.uniform(0, 30, pts_per_bubble)
    theta = np.random.uniform(0, 2*np.pi, pts_per_bubble)
    phi = np.arccos(np.random.uniform(-1, 1, pts_per_bubble))
    
    px_base.extend(origin[0] + r * np.sin(phi) * np.cos(theta))
    py_base.extend(origin[1] + r * np.cos(phi))
    pz_base.extend(origin[2] + r * np.sin(phi) * np.sin(theta))
    
    # 50/50 assignment to matter/antimatter exhaust
    assignment = 0 if i % 2 == 0 else 1
    stream_id.extend([assignment] * pts_per_bubble)

# Force exact lengths
px_base = np.array(px_base)[:MAX_PARTICLES]
py_base = np.array(py_base)[:MAX_PARTICLES]
pz_base = np.array(pz_base)[:MAX_PARTICLES]
stream_id = np.array(stream_id)[:MAX_PARTICLES]

# Tether Anchor Array (Selecting 150 elite particles to leave gravity ghosts)
tether_mask = np.zeros(MAX_PARTICLES, dtype=bool)
anchor_idxs = np.random.choice(np.arange(MAX_PARTICLES), size=150, replace=False)
tether_mask[anchor_idxs] = True

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, p_x, p_y, p_z, c_arr, s_arr, a_arr, tether_lines, tether_alpha, engine_glow, is_flash, is_tathata = packet
    
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
        # Background Aligning Grid
        if t_sec > 1.0 and not is_tathata:
            for g_line in np.linspace(-150, 150, 7):
                ax.plot([-140, 140], [g_line, g_line], color=C_DIM, lw=0.5, alpha=0.3, zorder=1)
                ax.plot([g_line, g_line], [-150, 150], color=C_DIM, lw=0.5, alpha=0.3, zorder=1)

        # 1. THE RECIPROCAL ENGINE CORE
        if engine_glow > 0:
            core_size = engine_glow * 150
            EngineCirc = plt.Circle((0, 0), core_size, color=C_GOLD, alpha=np.clip(engine_glow*0.5, 0, 0.5), zorder=2)
            ax.add_patch(EngineCirc)
            ax.scatter(0, 0, s=200 * engine_glow, color=C_TEXT, zorder=3) # The Absolute Zero Point Toggle

        # 2. GRAVITY TETHERS (LineCollection for O(1) performance)
        if len(tether_lines) > 0 and tether_alpha > 0:
            t_color = c_mantis if is_tathata else c_text
            # Append alpha manually to base color
            lc_color = np.array([t_color[0], t_color[1], t_color[2], tether_alpha])
            lc = LineCollection(tether_lines, colors=[lc_color]*len(tether_lines), linewidths=1.0, zorder=4)
            ax.add_collection(lc)

        # 3. KINEMATIC STREAM RENDERING
        # Filter dead-alpha early to save GPU load
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

        # 4. TATHATA UI
        if is_tathata:
            ax.add_patch(plt.Rectangle((-140, -180), 280, 360, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -60, "TATHĀTĀ: TOPOLOGY LOCKED", color=C_MANTIS, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 75, "[SUPERLUMINAL VOID RENDERED]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_CYAN if t_sec < 4.0 else (C_GOLD if t_sec < 9.0 else (C_TEXT if t_sec < 16.0 else C_MANTIS))
    if is_tathata: ui_col = C_MANTIS
    
    ax.text(-140, 240, "LG-258 :: RELATIVISTIC TOPOLOGY", color=txt_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: CAVITATION VOID / TWIN EXHAUST PORTS", color=txt_col, fontsize=8, fontname='monospace', zorder=80)
    
    obj_str = "THE TIME POOL [N-UNIVERSES]"
    if 4.0 <= t_sec < 9.0: obj_str = "THE TAP OPENS [RECIPROCAL IGNITION]"
    elif 9.0 <= t_sec < 16.0: obj_str = "SUPERLUMINAL SEPARATION [GRAVITY TUG]"
    elif is_tathata: obj_str = "CAUSAL BEDROCK [THE GHOST TRACE]"

    ax.text(-140, -200, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Thermodynamic Phase Shift Metric
    metric_label = "LATENCY GAP / RELATIVISTIC EXHAUST VELOCITY" 
    ax.text(-140, -225, metric_label, color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -230), 280, 4, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    
    velo_ratio = 0.1 if t_sec < 4.0 else np.clip(0.1 + ((t_sec - 4.0) / 8.0)**2, 0, 1)
    if is_tathata: velo_ratio = 1.0
    val_w = 280 * velo_ratio
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
        a_arr = np.ones(MAX_PARTICLES) * 0.8
        
        curr_x = np.copy(px_base)
        curr_y = np.copy(py_base)
        curr_z = np.copy(pz_base)

        tether_lines = []
        tether_alpha = 0.0
        engine_glow = 0.0

        # Matter drives up (North), Antimatter drives down (South)
        y_drive_dir = np.where(stream_id == 0, 1.0, -1.0)

        # -------------------------------------------------------------
        # THE RELATIVISTIC KINEMATICS
        # -------------------------------------------------------------
        
        if t_sec < 4.0:
            # PHASE 1: THE TIME POOL (Cavitation Bubbles)
            state = "PHASE 1 :: THE NUCLEATION POOL"
            
            # Gentle drift in the fluid
            curr_x += np.sin(t_sec * 2.0 + py_base * 0.05) * 5.0
            curr_z += np.cos(t_sec * 1.5 + px_base * 0.05) * 5.0
            
            c_arr[:] = c_cyan

        elif t_sec < 9.0:
            # PHASE 2: THE TAP OPENS (Inrush & Ignition)
            state = "PHASE 2 :: ALGORITHM SUCK / ENGINES FIRE"
            prog = (t_sec - 4.0) / 5.0
            ease = prog ** 3 # Violent exponential suck
            
            # 1. The inward vortex crush
            curr_x *= (1.0 - ease)
            curr_y *= (1.0 - ease)
            curr_z *= (1.0 - ease)
            
            # 2. Add swirling spin as they crash toward zero
            spin = t_sec * 15.0 * ease
            spin_x = curr_x * np.cos(spin) - curr_z * np.sin(spin)
            spin_z = curr_x * np.sin(spin) + curr_z * np.cos(spin)
            curr_x, curr_z = spin_x, spin_z
            
            # 3. Post-crush, dual exhaust initiation
            if prog > 0.6:
                ex_prog = (prog - 0.6) / 0.4
                # They start firing out of the Y axis
                curr_y += y_drive_dir * (ex_prog ** 2) * 50.0
                
                # Colors map to exhaust profiles
                c_interp_m = c_cyan * (1.0 - ex_prog) + c_azure * ex_prog
                c_interp_am = c_cyan * (1.0 - ex_prog) + c_magenta * ex_prog
                
                matter_idx = (stream_id == 0)
                anti_idx = (stream_id == 1)
                
                c_arr[matter_idx] = c_interp_m
                c_arr[anti_idx] = c_interp_am
                
                engine_glow = ex_prog
            else:
                c_arr[:] = c_cyan * (1.0 - prog) + c_gold * prog

        elif t_sec < 16.0:
            # PHASE 3: SUPERLUMINAL SEPARATION (Gravity Ghosts)
            state = "PHASE 3 :: TRANSLUMINAR EXTINCTION"
            prog = (t_sec - 9.0) / 7.0
            ease = prog ** 2
            
            engine_glow = 1.0 - prog # Engine cools off
            
            # 1. Relativistic Acceleration
            velo = 50.0 + (ease * 600.0) # Velocity exceeds rendering limits
            curr_y = y_drive_dir * velo
            
            # Maintain strict colors
            c_arr[stream_id == 0] = c_azure
            c_arr[stream_id == 1] = c_magenta
            
            # 2. Superluminal Alpha Bleed
            # Once velocity exceeds a threshold, they disappear from the "Light Cone"
            fade_start = 0.3
            if prog > fade_start:
                fade_ease = (prog - fade_start) / (1.0 - fade_start)
                a_arr[:] = 0.8 * (1.0 - fade_ease**0.5)
            else:
                a_arr[:] = 0.8

            # 3. Gravity Tethers Generation
            # Even as particles vanish, the causal ghost line stretches from origin to object
            if prog > fade_start:
                tether_alpha = (prog - fade_start) / (1.0 - fade_start)
            else:
                tether_alpha = 0.0
                
            if t_sec > 15.8:
                is_flash = True if f % 2 == 0 else False

        else:
            # PHASE 4: TATHĀTĀ (The Ghost Trace)
            state = "TATHĀTĀ :: THE GRAVITY TUG"
            is_tathata = True
            
            # Particles are entirely GONE from the 3D plane
            a_arr[:] = 0.0
            
            # The only thing that exists are the Gravity Tethers pulling on the void
            # We lock the geometry of the tethers
            freeze_prog = (16.0 - 9.0) / 7.0
            velo = 50.0 + (freeze_prog**2 * 600.0)
            curr_y = y_drive_dir * velo
            
            tether_alpha = 1.0
            engine_glow = 0.0
            
            if t_sec < 16.2:
                is_flash = True 

        # Apply Global Tensor Matrix
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1]
        z_depth = rot_pts[:, 2] 

        # Construct LineCollection segments for Ghost Tethers based on final rotated positions
        if tether_alpha > 0.0:
            tx = proj_x[tether_mask]
            ty = proj_y[tether_mask]
            # Line goes from central origin (0,0) to the escaping particle coordinate
            tether_lines = [[[0.0, 0.0], [tx[i], ty[i]]] for i in range(len(tx))]

        yield (f, t_sec, state, proj_x, proj_y, z_depth, c_arr, s_arr, a_arr, tether_lines, tether_alpha, engine_glow, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 258: THE RELATIVISTIC TOPOLOGY [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Gravity Tether LineCollection & Causal Horizon Culling")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Superluminal Threshold Exceeded. Tethers Locked.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
