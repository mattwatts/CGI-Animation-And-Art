"""
SOVEREIGN CODE: logic_garden_237_lorentz_velocity.py
SYSTEM: Python Multicore / O(1) Lorentz Kinematics
SCENE: Logic Garden 237 (Lorentz Velocity / The Railgun Pop)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Dimensional Axis Align / Dynamic Target Array

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
OUT_DIR = "frames_237_lorentz_velocity"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS) --------
C_BG        = '#FFFFFF'        # Absolute Void (High Contrast)
C_TEXT      = '#020205'        # Data Metrics
C_DIM       = '#33333A'        # Parallel Linear Rails (Steel Substrate)
C_CYAN      = '#00FFFF'        # Magnetic Field Pooling / I x B
C_MAGENTA   = '#FF0055'        # Rail Degradation / Thermal Debt
C_MANTIS    = '#00FF00'        # Hyper-Dense Armature (The Payload)
C_GOLD      = '#FFB300'        # The Plasma Bypass / 50k Sparks (Tathata)

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_dim     = np.array(hex_to_rgba(C_DIM)[:3])
c_cyan    = np.array(hex_to_rgba(C_CYAN)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_mantis  = np.array(hex_to_rgba(C_MANTIS)[:3])
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
# BASE GEOMETRY ARRAYS: THE SUBSTRATE & THE ARMATURE
# ------------------------------------------------------------------
np.random.seed(237) # Trajectory Protocol Lock

# 1. The Rails (C_DIM) - Two thick linear arrays
N_RAIL = 12000
rail_y_dist = np.linspace(-220, 160, N_RAIL // 2)

# Left Rail
px_rail_L = -35.0 + np.random.normal(0, 3.0, N_RAIL // 2)
py_rail_L = rail_y_dist
pz_rail_L = np.random.normal(0, 3.0, N_RAIL // 2)

# Right Rail
px_rail_R = 35.0 + np.random.normal(0, 3.0, N_RAIL // 2)
py_rail_R = rail_y_dist
pz_rail_R = np.random.normal(0, 3.0, N_RAIL // 2)

px_rails = np.concatenate([px_rail_L, px_rail_R])
py_rails = np.concatenate([py_rail_L, py_rail_R])
pz_rails = np.concatenate([pz_rail_L, pz_rail_R])

# 2. The Armature (C_MANTIS) - Hyper-Dense Square Block
N_SPARKS = 40000 
px_arm = np.random.uniform(-30, 30, N_SPARKS)
py_arm = np.random.uniform(-215, -185, N_SPARKS)
pz_arm = np.random.uniform(-5, 5, N_SPARKS)

# Explosion vector cache (Calculated O(1) at init)
exp_vec_x = np.random.normal(0, 45.0, N_SPARKS)
exp_vec_y = np.random.normal(250.0, 60.0, N_SPARKS) # Massive forward carry momentum
exp_vec_z = np.random.normal(0, 45.0, N_SPARKS)

# HOTFIX: Dimensional compilation limits mathematically locked
base_px = np.concatenate([px_rails, px_arm])
base_py = np.concatenate([py_rails, py_arm])
base_pz = np.concatenate([pz_rails, pz_arm])

MAX_PARTICLES = len(base_px)

mask_rails = np.arange(MAX_PARTICLES) < len(px_rails)
mask_arm = ~mask_rails

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, proj_x, proj_y, z_depth, colors, sizes, thermal_spall, is_flash, is_tathata = packet
    
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
        # Depth Sorting
        sort_idx = np.argsort(z_depth)
        s_px = proj_x[sort_idx]
        s_py = proj_y[sort_idx]
        s_c = colors[sort_idx]
        s_s = sizes[sort_idx]

        ax.scatter(s_px, s_py, s=s_s, color=s_c, edgecolors='none', alpha=0.9, zorder=10)

        if is_tathata:
            ax.add_patch(plt.Rectangle((-140, 120), 280, 120, facecolor='none', edgecolor=C_GOLD, lw=2, zorder=40))
            ax.text(0, 100, "TATHĀTĀ: AMMUNITION EVENT HORIZON", color=C_GOLD, fontsize=11, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 250, "[PLASMA BYPASS / RAIL DEGRADATION ABSOLUTE]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_MANTIS if t_sec < 4.5 else (C_CYAN if t_sec < 9.0 else C_MAGENTA)
    if is_tathata: ui_col = C_GOLD
    
    ax.text(-140, 240, "LG-237 :: LORENTZ VELOCITY TENSOR", color=txt_col, fontsize=20, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: I.L x B FIELDS / 2,500 m/s INSTANTANEOUS", color=txt_col, fontsize=8, fontname='monospace', zorder=80)
    
    obj_str = "THE BREECH [FRICTIONLESS STATICS]"
    if 4.5 <= t_sec < 9.0: obj_str = "MAGNETIC INJECTION [LORENTZ FORCE POOLING]"
    elif 9.0 <= t_sec < 14.8: obj_str = "KINETIC ACCELERATION [RAIL DEGRADATION]"
    elif is_tathata: obj_str = "THE RAILGUN POP [PLASMA SHATTER]"

    ax.text(-140, -180, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Thermodynamic Hardware Metric: Substrate Spallation
    ax.text(-140, -205, "SUBSTRATE FATIGUE LIMIT [THERMAL SPALLATION]", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    bar_w = 280 * np.clip(thermal_spall, 0, 1)
    ax.add_patch(plt.Rectangle((-140, -210), bar_w, 4, facecolor=C_MAGENTA if thermal_spall > 0.4 else ui_col, zorder=81))

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
        
        # Tilt angle observes down the rails
        cam_rx = np.pi/2.5 - (t_sec * 0.01)
        cam_ry = 0.0
        cam_rz = 0.0
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 4.0
        
        curr_x = np.copy(base_px)
        curr_y = np.copy(base_py)
        curr_z = np.copy(base_pz)

        thermal_spall = 0.0

        # Phase 1: Landscape and Nodes are constant
        colors[mask_rails] = c_dim
        sizes[mask_rails] = 3.0
        
        colors[mask_arm] = c_mantis
        sizes[mask_arm] = 2.0  # Hyper-dense

        # -------------------------------------------------------------
        # LORENTZ KINEMATIC PHASES
        # -------------------------------------------------------------
        if t_sec < 4.5:
            state = "PHASE 1 :: BREECH STATICS"
            # Idling. No movement.
            thermal_spall = 0.0

        elif t_sec < 9.0:
            state = "PHASE 2 :: I.L x B FIELD INJECTION"
            prog = (t_sec - 4.5) / 4.5
            
            # The rails begin to hum with magnetic charge
            charge_mask = np.random.rand(int(N_RAIL)) < (prog * 0.5)
            colors[np.where(mask_rails)[0][charge_mask]] = c_cyan
            
            curr_x[mask_arm] += np.random.normal(0, 0.5 * prog, N_SPARKS) # Vibrating in restraints
            
            thermal_spall = 0.1 * prog

        elif t_sec < 14.8:
            state = "PHASE 3 :: EXPONENTIAL ACCELERATION"
            prog = (t_sec - 9.0) / 5.8
            if t_sec < 9.1: is_flash = True
            
            # The velocity is non-linear. Immediate acceleration.
            travel_dist = 360.0 * (prog ** 3) 
            
            curr_y[mask_arm] += travel_dist
            
            # Substrate Fatigue: The rails are shredded behind the armature
            spallation_zone = curr_y[mask_rails] < (-200 + travel_dist)
            
            colors[mask_rails] = c_dim
            # Melting the rails
            colors[np.where(mask_rails)[0][spallation_zone]] = c_magenta
            curr_x[np.where(mask_rails)[0][spallation_zone]] += np.random.normal(0, 5.0 * prog, np.sum(spallation_zone))
            curr_z[np.where(mask_rails)[0][spallation_zone]] -= np.random.normal(0, 10.0 * prog, np.sum(spallation_zone))
            
            # Plasma trailing off the armature
            sizes[mask_arm] = 3.0
            sizes[np.where(mask_rails)[0][spallation_zone]] = 5.0
            
            thermal_spall = prog ** 2 # Exponential thermodynamic load

        else:
            state = "TATHĀTĀ :: THE RAILGUN POP"
            is_tathata = True
            
            time_post_pop = t_sec - 14.8
            max_dist = 360.0
            
            # The boundaries of the rails end at Y=160.
            # Upon exit, the hyper-dense structure instantly shatters into 50k sparks
            
            curr_y[mask_arm] = -200 + max_dist + (exp_vec_y * time_post_pop)
            curr_x[mask_arm] += (exp_vec_x * time_post_pop)
            curr_z[mask_arm] += (exp_vec_z * time_post_pop)
            
            colors[mask_arm] = c_gold
            sizes[mask_arm] = 5.0
            
            # Rails remain violently permanently disfigured
            colors[mask_rails] = c_dim
            spallation_zone = base_py[mask_rails] < 160
            colors[np.where(mask_rails)[0][spallation_zone]] = c_magenta
            curr_x[np.where(mask_rails)[0][spallation_zone]] += np.random.normal(0, 8.0, np.sum(spallation_zone))
            curr_z[np.where(mask_rails)[0][spallation_zone]] -= np.abs(np.random.normal(0, 20.0, np.sum(spallation_zone)))
            
            thermal_spall = 1.0 # The substrate is terminally destroyed.
            
            if t_sec < 14.95:
                is_flash = True

        # Apply Global Tensor Matrix
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1]
        z_depth = rot_pts[:, 2] 

        # O(N) Geometry Culling
        cull_mask = (proj_y > -260) & (proj_y < 260) & (proj_x > -160) & (proj_x < 160)

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], colors[cull_mask], sizes[cull_mask], thermal_spall, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 237: LORENTZ VELOCITY TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Plasma Expansion Expansion / Substrate Yield Math")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Lorentz Limit Exceeded. Rails Vaporized.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
