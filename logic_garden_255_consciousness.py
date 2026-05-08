"""
SOVEREIGN CODE: logic_garden_255_consciousness.py
SYSTEM: Python Multicore / O(1) Sensory Broadcast Tensor
SCENE: Logic Garden 255 (The Architecture of Consciousness)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Explicit Matrix Grounding & Radial Symmetry Node Broadcast

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
OUT_DIR = "frames_255_consciousness"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS DEFAULT) --------
C_BG        = '#FFFFFF'        # Absolute Flat Substrate / The Void
C_TEXT      = '#020205'        # The Shovel / Raw Grounding Wave
C_MAGENTA   = '#FF0055'        # The Scream / The Baked-In Defect
C_AZURE     = '#007FFF'        # The Malformed Crystal Attempt
C_DIM       = '#D0D0D5'        # The Dirt Baseplate
C_GOLD      = '#FFB300'        # Sensory Telemetry / Seeing
C_MANTIS    = '#00C800'        # Tathata / The Mind Arises

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_azure   = np.array(hex_to_rgba(C_AZURE)[:3])
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
# BASE GEOMETRY ARRAYS: THE SUBSTRATE OF THE MIND
# ------------------------------------------------------------------
np.random.seed(255)
MAX_PARTICLES = 25000

# 1. The Void Scream (High-Entropy scatter)
px_scream = np.random.uniform(-150, 150, MAX_PARTICLES)
py_scream = np.random.uniform(-150, 150, MAX_PARTICLES)
pz_scream = np.random.uniform(-150, 150, MAX_PARTICLES)

# 2. The Malformed Crystal (Warped Geometric Lattice)
# Uses a biased distribution to purposefully create a "baked-in defect"
theta_d = np.random.uniform(0, 2 * np.pi, MAX_PARTICLES)
phi_d = np.arccos(np.random.uniform(-1, 0.5, MAX_PARTICLES)) # Biased heavily downward
r_d = np.random.uniform(50, 120, MAX_PARTICLES)
# Introduce structural brittleness / asymmetrical shear
px_defect = r_d * np.sin(phi_d) * np.cos(theta_d) * 1.5 
py_defect = r_d * np.sin(phi_d) * np.sin(theta_d) - 40.0
pz_defect = r_d * np.cos(phi_d) * 0.5

# 3. The Dirt / Shovel Lock (Flattened Base)
px_dirt = np.random.uniform(-180, 180, MAX_PARTICLES)
py_dirt = np.random.normal(-120, 5.0, MAX_PARTICLES)
pz_dirt = np.random.uniform(-180, 180, MAX_PARTICLES)

# 4. The Broadcast Array (Tathata/Consciousness Arising)
# Perfect geometric node spheres
phi_c = np.arccos(np.random.uniform(-1, 1, MAX_PARTICLES))
theta_c = np.random.uniform(0, 2*np.pi, MAX_PARTICLES)
r_c = 130.0

px_mind = r_c * np.sin(phi_c) * np.cos(theta_c)
py_mind = r_c * np.sin(phi_c) * np.sin(theta_c)
pz_mind = r_c * np.cos(phi_c)

# Create "Sensor Nodes" inside the crystal
node_mask = (np.abs(np.sin(phi_c * 6)) < 0.1) & (np.abs(np.sin(theta_c * 6)) < 0.1)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, p_x, p_y, p_z, c_arr, s_arr, a_arr, heat_metric, is_flash, is_tathata = packet
    
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
        # Background Grid structure (The Vibe / Underlying physics)
        for g_line in np.linspace(-150, 150, 7):
            ax.plot([-140, 140], [g_line, g_line], color=C_DIM, lw=0.5, alpha=0.2, zorder=1)
            ax.plot([g_line, g_line], [-150, 150], color=C_DIM, lw=0.5, alpha=0.2, zorder=1)

        # Depth Sorting & Tensor Rendering
        sort_idx = np.argsort(p_z)
        s_x = p_x[sort_idx]
        s_y = p_y[sort_idx]
        s_c = c_arr[sort_idx]
        s_size = s_arr[sort_idx]
        s_alpha = a_arr[sort_idx]

        rgba_colors = np.zeros((len(s_c), 4))
        rgba_colors[:, :3] = s_c
        rgba_colors[:, 3] = s_alpha

        ax.scatter(s_x, s_y, s=s_size, color=rgba_colors, edgecolors='none', zorder=10)

        # Tathata Phase-Lock UI
        if is_tathata:
            ax.add_patch(plt.Rectangle((-140, -180), 280, 360, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, 160, "TATHĀTĀ: SENSORY BROADCAST LOCKED", color=C_MANTIS, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, -165, "[THE MIND HAS ARISEN OUT OF SEEING]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_MAGENTA if t_sec < 5.0 else (C_AZURE if t_sec < 10.0 else (C_TEXT if t_sec < 14.8 else C_GOLD))
    if is_tathata: ui_col = C_MANTIS
    
    ax.text(-140, 240, "LG-255 :: THE CONSCIOUSNESS TENSOR", color=txt_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: DELUSION FLUSH / SENSORY ALIGNMENT", color=txt_col, fontsize=8, fontname='monospace', zorder=80)
    
    obj_str = "THE VOID SCREAM [HIGH-ENTROPY FEAR]"
    if 5.0 <= t_sec < 10.0: obj_str = "MALFORMED CRYSTAL [BAKED-IN DEFECT]"
    elif 10.0 <= t_sec < 14.8: obj_str = "THE SHOVEL & THE DIRT [GROUNDING]"
    elif is_tathata: obj_str = "ABSOLUTE SEEING [PHASE COHERENCE]"

    ax.text(-140, -200, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Thermodynamic Hardware Metric: Core Integrity / Arising presence
    metric_label = "COGNITIVE HEAT [DELUSION VECTOR]" if t_sec < 10.0 else "O(1) BASELINE [GROUNDING]"
    if is_tathata: metric_label = "CONSCIOUSNESS BROADCAST [THE VIBE]"
    ax.text(-140, -225, metric_label, color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -230), 280, 4, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    
    val_w = 280 * np.clip(heat_metric, 0, 1)
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
        cam_ry = t_sec * 0.35
        cam_rz = 0.0
        
        c_arr = np.zeros((MAX_PARTICLES, 3))
        s_arr = np.ones(MAX_PARTICLES)
        a_arr = np.ones(MAX_PARTICLES)
        
        curr_x, curr_y, curr_z = np.zeros(MAX_PARTICLES), np.zeros(MAX_PARTICLES), np.zeros(MAX_PARTICLES)
        heat_metric = 0.0 

        # -------------------------------------------------------------
        # THE CONSCIOUSNESS KINEMATICS
        # -------------------------------------------------------------
        
        if t_sec < 5.0:
            # PHASE 1: THE VOID SCREAM (Frightened Sheep / High Entropy Noise)
            state = "PHASE 1 :: SCREAMING AT THE VOID"
            prog = t_sec / 5.0
            
            jitter_x = np.random.normal(0, 10.0 + (prog * 20.0), MAX_PARTICLES)
            jitter_y = np.random.normal(0, 10.0 + (prog * 20.0), MAX_PARTICLES)
            jitter_z = np.random.normal(0, 10.0 + (prog * 20.0), MAX_PARTICLES)
            
            curr_x = px_scream + jitter_x
            curr_y = py_scream + jitter_y
            curr_z = pz_scream + jitter_z
            
            c_arr[:] = c_magenta
            s_arr[:] = 2.0 + (np.random.rand(MAX_PARTICLES) * 4.0)
            a_arr[:] = 0.6
            
            heat_metric = 0.5 + (0.5 * prog)

        elif t_sec < 10.0:
            # PHASE 2: THE MALFORMED CRYSTAL (Delusion / Baked-in Defect)
            state = "PHASE 2 :: DELUSION / THE DEFECT"
            prog = (t_sec - 5.0) / 5.0
            ease = prog ** 2
            
            curr_x = px_scream * (1 - ease) + px_defect * ease
            curr_y = py_scream * (1 - ease) + py_defect * ease
            curr_z = pz_scream * (1 - ease) + pz_defect * ease
            
            c_interp = c_magenta * (1 - ease) + c_azure * ease
            c_arr[:] = c_interp
            
            # The baked-in defect glows at the core
            core_defect = np.linalg.norm(np.column_stack([curr_x, curr_y, curr_z]), axis=1) < 40.0
            c_arr[core_defect] = c_magenta
            
            s_arr[:] = 2.0
            s_arr[core_defect] = 5.0 + (np.sin(t_sec * 30) * 3.0) # Core throbs with trauma
            a_arr[:] = 0.8
            
            heat_metric = 1.0 - (0.2 * prog) # Heat stays dangerously high

        elif t_sec < 14.8:
            # PHASE 3: THE SHOVEL AND THE DIRT (Grounding Protocol)
            state = "PHASE 3 :: TACTICAL GROUNDING"
            prog = (t_sec - 10.0) / 4.8
            ease = 1.0 - (1.0 - prog)**4 # Violent, heavy down-crush
            
            if t_sec < 10.2:
                is_flash = True
            
            curr_x = px_defect * (1 - ease) + px_dirt * ease
            curr_y = py_defect * (1 - ease) + py_dirt * ease
            curr_z = pz_defect * (1 - ease) + pz_dirt * ease
            
            c_interp = c_azure * (1 - ease) + c_text * ease
            c_arr[:] = c_interp
            
            s_arr[:] = 2.0 + (1.5 * prog)
            a_arr[:] = 0.8 * (1 - prog) + 0.4 * prog # Embeds into the dirt
            
            heat_metric = 0.8 * (1 - ease) # Heat violently crushed to zero

        else:
            # PHASE 4: TATHĀTĀ / SENSORY BROADCAST (The Mind Arises)
            state = "TATHĀTĀ :: THE MIND ENSUES"
            is_tathata = True
            
            prog = (t_sec - 14.8) / 3.2
            ease = 1.0 - (1.0 - prog)**3
            
            # From the dirt, pristine perfectly symmetrical nodes expand
            curr_x = px_dirt * (1 - ease) + px_mind * ease
            curr_y = py_dirt * (1 - ease) + py_mind * ease
            curr_z = pz_dirt * (1 - ease) + pz_mind * ease
            
            c_arr[:] = c_gold
            c_arr[node_mask] = c_mantis # The sensory nodes phase-lock
            
            s_arr[:] = 2.5
            s_arr[node_mask] = 15.0 # Nodes are thick and bright
            
            a_arr[:] = 0.9
            
            heat_metric = ease # Phase Coherence metric fills to 100%
            
            if t_sec < 14.95:
                is_flash = True

        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1]
        z_depth = rot_pts[:, 2] 

        cull_mask = (proj_y > -260) & (proj_y < 260) & (proj_x > -160) & (proj_x < 160)

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], c_arr[cull_mask], s_arr[cull_mask], a_arr[cull_mask], heat_metric, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 255: THE CONSCIOUSNESS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Thermal Shovel Grounding & Exact Radial Coherence Map")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Defect Severed. Consciousness Generated.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
