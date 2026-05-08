"""
SOVEREIGN CODE: logic_garden_256_reciprocal_engine.py
SYSTEM: Python Multicore / O(1) Tensor Cancellation 
SCENE: Logic Garden 256 (The Reciprocal Engine / Baryon Asymmetry)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Strict Array Normalization / Asymmetry Dimension Sync

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
OUT_DIR = "frames_256_reciprocal_engine"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS DEFAULT) --------
C_BG        = '#FFFFFF'        # Absolute Flat Substrate / The Void
C_TEXT      = '#020205'        # The Carbon Smudge / UI
C_AZURE     = '#007FFF'        # Matter (M)
C_MAGENTA   = '#FF0055'        # Antimatter (M-bar)
C_GOLD      = '#FFB300'        # Gamma Spallation / Thermal Erasure
C_MANTIS    = '#00C800'        # Tathata Phase-Lock / The Dirt
C_DIM       = '#D0D0D5'        # Grid HUD

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_azure   = np.array(hex_to_rgba(C_AZURE)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
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
# BASE GEOMETRY ARRAYS: THE COLLIDING KINEMATICS
# ------------------------------------------------------------------
np.random.seed(256)
HALF_PARTICLES = 16000
MAX_PARTICLES = HALF_PARTICLES * 2

# Topography of Matter (Azure)
theta_m = np.random.uniform(0, 2*np.pi, HALF_PARTICLES)
phi_m = np.arccos(np.random.uniform(-1, 1, HALF_PARTICLES))
r_m = np.random.uniform(10, 80, HALF_PARTICLES)

px_m = r_m * np.sin(phi_m) * np.cos(theta_m) - 100.0 # Offset Left
py_m = r_m * np.cos(phi_m)
pz_m = r_m * np.sin(phi_m) * np.sin(theta_m)

# Topography of Antimatter (Magenta) - Mathematically mirrored natively
px_am = r_m * np.sin(phi_m) * np.cos(theta_m) + 100.0 # Offset Right
py_am = r_m * np.cos(phi_m)
pz_am = r_m * np.sin(phi_m) * np.sin(theta_m)

base_px = np.concatenate([px_m, px_am])
base_py = np.concatenate([py_m, py_am])
base_pz = np.concatenate([pz_m, pz_am])

base_colors = np.zeros((MAX_PARTICLES, 3))
base_colors[:HALF_PARTICLES] = c_azure
base_colors[HALF_PARTICLES:] = c_magenta

# BARYON ASYMMETRY MASK (The Defect)
# Exactly 1% of the Matter particles strictly lack an Antimatter pair
survival_indices = np.random.choice(np.arange(HALF_PARTICLES), size=int(HALF_PARTICLES * 0.01), replace=False)
base_survival_mask = np.zeros(MAX_PARTICLES, dtype=bool)
base_survival_mask[survival_indices] = True

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, p_x, p_y, p_z, c_arr, s_arr, a_arr, defect_metric, flash_intensity, is_tathata = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_TEXT if flash_intensity > 0.9 else C_BG
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    ax.set_xlim(-160, 160)
    ax.set_ylim(-260, 260)

    # Baseplate Grid Structure
    if t_sec > 11.0 and not (flash_intensity > 0.9):
        for g_line in np.linspace(-150, 150, 7):
            ax.plot([-140, 140], [g_line, g_line], color=C_DIM, lw=0.5, alpha=0.3, zorder=1)
            ax.plot([g_line, g_line], [-150, 150], color=C_DIM, lw=0.5, alpha=0.3, zorder=1)

    # Render Gamma Erasure Flash manually as an expanding background artifact
    if flash_intensity > 0.0:
        flash_circ = plt.Circle((0, 0), flash_intensity * 300, color=C_GOLD, alpha=flash_intensity * 0.4, zorder=2)
        ax.add_patch(flash_circ)

    # Tensor Geometry Sorting
    active_mask = a_arr > 0.01
    sort_idx = np.argsort(p_z[active_mask])
    
    s_x = p_x[active_mask][sort_idx]
    s_y = p_y[active_mask][sort_idx]
    s_c = c_arr[active_mask][sort_idx]
    s_size = s_arr[active_mask][sort_idx]
    s_alpha = a_arr[active_mask][sort_idx]

    rgba_colors = np.zeros((len(s_c), 4))
    rgba_colors[:, :3] = s_c
    rgba_colors[:, 3] = s_alpha

    ax.scatter(s_x, s_y, s=s_size, color=rgba_colors, edgecolors='none', zorder=10)

    # Tathata Firmware Phase-Lock UI
    if is_tathata:
        ax.add_patch(plt.Rectangle((-140, -180), 280, 360, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
        ax.text(0, -50, "TATHĀTĀ: BARYON ASYMMETRY LOCKED", color=C_MANTIS, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=41)
        ax.text(0, 50, "[THE SHOVEL / THE DIRT SUBSTRATE READY]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if flash_intensity > 0.9 else C_TEXT
    ui_col = C_MAGENTA if t_sec < 6.0 else (C_GOLD if t_sec < 11.0 else C_AZURE)
    if is_tathata: ui_col = C_MANTIS
    
    ax.text(-140, 240, "LG-256 :: THE RECIPROCAL ENGINE", color=txt_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: O(1) MATTER ERASURE / STRUCTURAL DEFECT", color=txt_col, fontsize=8, fontname='monospace', zorder=80)
    
    obj_str = "THE THERMAL ENGINE [PRIMARY IGNITION]"
    if 6.0 <= t_sec < 11.0: obj_str = "RECIPROCAL ERASURE [GAMMA FLUSH]"
    elif 11.0 <= t_sec < 14.8: obj_str = "BARYON ASYMMETRY [THE CARBON SMUDGE]"
    elif is_tathata: obj_str = "ABSOLUTE BEDROCK [THE DIRT]"

    ax.text(-140, -200, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Thermodynamic Defect Metric
    metric_label = "STRUCTURAL DEFECT VECTOR [EXISTENCE PROBABILITY]" 
    ax.text(-140, -225, metric_label, color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -230), 280, 4, facecolor=C_DIM if not (flash_intensity > 0.9) else C_TEXT, zorder=80))
    val_w = 280 * np.clip(defect_metric, 0, 1)
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
        
        is_tathata = False
        flash_intensity = 0.0
        
        # Smooth continuous rotation to view the engine
        cam_rx = np.pi/6 - (t_sec * 0.005)
        cam_ry = t_sec * 0.5
        cam_rz = 0.0
        
        c_arr = np.copy(base_colors)
        s_arr = np.ones(MAX_PARTICLES) * 2.0
        a_arr = np.ones(MAX_PARTICLES) * 0.8
        
        curr_x = np.copy(base_px)
        curr_y = np.copy(base_py)
        curr_z = np.copy(base_pz)

        defect_metric = 0.0 

        # -------------------------------------------------------------
        # THE RECIPROCAL COLLISION KINEMATICS
        # -------------------------------------------------------------
        
        if t_sec < 6.0:
            # PHASE 1: THE THERMAL ENGINE (Ignition Burst)
            state = "PHASE 1 :: M + M-BAR GENERATION"
            
            # The two masses rotate internally before crushing together
            curr_x[:HALF_PARTICLES] += np.sin(t_sec * 4.0) * 10.0
            curr_x[HALF_PARTICLES:] -= np.sin(t_sec * 4.0) * 10.0
            
            defect_metric = 0.1

        elif t_sec < 11.0:
            # PHASE 2: RECIPROCAL ERASURE (Mathematical Cancellation)
            state = "PHASE 2 :: KINETIC CANCELLATION"
            prog = (t_sec - 6.0) / 5.0
            ease = prog ** 3
            
            # The two offsets snap violently to zero coordinate [0,0,0]
            curr_x[:HALF_PARTICLES] = base_px[:HALF_PARTICLES] * (1.0 - ease)
            curr_x[HALF_PARTICLES:] = base_px[HALF_PARTICLES:] * (1.0 - ease)
            
            # They compress fiercely into a singularity
            curr_y *= (1.0 - ease)
            curr_z *= (1.0 - ease)
            
            # Particles that are NOT the designated survivors fade out
            doom_mask = ~base_survival_mask
            a_arr[doom_mask] = 0.8 * (1.0 - ease**2)
            
            # Flash intensity metrics (Gamma Release)
            if prog > 0.8:
                flash_intensity = (prog - 0.8) * 5.0 # Scales 0 to 1 rapidly
                if t_sec > 10.7 and t_sec < 10.9:
                    flash_intensity = 1.0 # True blind out

            defect_metric = 0.1 + (0.4 * ease)

        elif t_sec < 14.8:
            # PHASE 3: THE BARYON ASYMMETRY (The Residual Smudge)
            state = "PHASE 3 :: THE CARBON SMUDGE"
            prog = (t_sec - 11.0) / 3.8
            ease = 1.0 - (1.0 - prog)**3
            
            # Antimatter is GONE. Cancelled matter is GONE.
            doom_mask = ~base_survival_mask
            a_arr[doom_mask] = 0.0
            
            # The surviving Azure (Matter) defect fragments expand forming baseplate
            # HOTFIX: Mapped precisely against the full 32000 element base_px tensor
            curr_x[base_survival_mask] = (base_px[base_survival_mask] + 100.0) * (0.1 + 1.5 * ease)
            curr_y[base_survival_mask] = base_py[base_survival_mask] * 0.1
            curr_z[base_survival_mask] = base_pz[base_survival_mask] * (0.1 + 1.5 * ease)
            
            c_arr[base_survival_mask] = c_azure * (1 - ease) + c_text * ease
            s_arr[base_survival_mask] = 5.0 + (3.0 * ease)
            a_arr[base_survival_mask] = 1.0
            
            defect_metric = 0.5 + (0.5 * ease)

        else:
            # PHASE 4: TATHĀTĀ / THE DIRT (Armor Phase)
            state = "TATHĀTĀ :: BASEPLATE RESOLVED"
            is_tathata = True
            
            doom_mask = ~base_survival_mask
            a_arr[doom_mask] = 0.0
            
            # Geometry locks
            curr_x[base_survival_mask] = (base_px[base_survival_mask] + 100.0) * 1.6
            curr_y[base_survival_mask] = base_py[base_survival_mask] * 0.1
            curr_z[base_survival_mask] = base_pz[base_survival_mask] * 1.6
            
            c_arr[base_survival_mask] = c_mantis
            s_arr[base_survival_mask] = 8.0
            a_arr[base_survival_mask] = 1.0
            
            defect_metric = 1.0 
            
            if t_sec < 14.95:
                flash_intensity = 1.0

        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1]
        z_depth = rot_pts[:, 2] 

        # Optimization Culling happens naturally since A=0
        yield (f, t_sec, state, proj_x, proj_y, z_depth, c_arr, s_arr, a_arr, defect_metric, flash_intensity, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 256: THE RECIPROCAL ENGINE [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Strict Array Normalization / Asymmetry Dimension Sync")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Syntax Friction Solved. The Shovel is ready.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
