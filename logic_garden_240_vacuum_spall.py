"""
SOVEREIGN CODE: logic_garden_240_vacuum_spall.py
SYSTEM: Python Multicore / O(1) Kinetic Topology & Tensor Strain
SCENE: Logic Garden 240 (The Vacuum Spall / Armor Failure)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Boolean Axis Alignment & Dynamic Velocity Vector Clamping

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
OUT_DIR = "frames_240_vacuum_spall"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS STRICT) --------
C_BG        = '#FFFFFF'        # Absolute Void / Pure Canvas
C_TEXT      = '#020205'        # The Penetrator (High-Velocity APFSDS)
C_DIM       = '#33333A'        # The Armor Block / Bounding Box Geometry
C_MAGENTA   = '#FF0055'        # Acoustic Shockwave / Tensile Stress-Strain
C_GOLD      = '#FFB300'        # The Spallation Cone / Substrate Shrapnel
C_CYAN      = '#00FFFF'        # Telemetry Lock
C_MANTIS    = '#00C800'        # Tathata Base

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_dim     = np.array(hex_to_rgba(C_DIM)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_gold    = np.array(hex_to_rgba(C_GOLD)[:3])
c_cyan    = np.array(hex_to_rgba(C_CYAN)[:3])
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
# BASE GEOMETRY ARRAYS: THE ARMOR BLOCK & APFSDS
# ------------------------------------------------------------------
np.random.seed(240) 

# 1. The Armor Block (Thick, dense cubic matrix)
NUM_ARMOR = 25000
# Armor face is at Y = -25, Rear free surface is at Y = 25
b_x = np.random.uniform(-45, 45, NUM_ARMOR)
b_y = np.random.uniform(-25, 25, NUM_ARMOR)
b_z = np.random.uniform(-45, 45, NUM_ARMOR)

# Pre-identify the Spallation Layer (Rear surface: Y > 15)
spall_filter = b_y > 15.0
spall_indices = np.where(spall_filter)[0]
N_SPALL = len(spall_indices)

# Spall Expansion Vectors (Dynamically locked to exact N_SPALL count)
spall_vel_x = np.random.normal(0, 15.0, N_SPALL)
spall_vel_y = np.random.uniform(40.0, 180.0, N_SPALL) # High velocity conical spread
spall_vel_z = np.random.normal(0, 15.0, N_SPALL)

# 2. The APFSDS Penetrator (High-speed kinetic rod)
NUM_PEN = 3000
p_theta = np.random.uniform(0, 2 * np.pi, NUM_PEN)
p_rad = np.sqrt(np.random.uniform(0, 2.5**2, NUM_PEN))
px_pen = p_rad * np.cos(p_theta)
pz_pen = p_rad * np.sin(p_theta)
py_pen = np.random.uniform(-140, -40, NUM_PEN) # Starts far away

# Array Alignment & Global Particle Lock
base_px = np.concatenate([b_x, px_pen])
base_py = np.concatenate([b_y, py_pen])
base_pz = np.concatenate([b_z, pz_pen])

MAX_PARTICLES = len(base_px) # Exactly 28,000

# HOTFIX: Boolean tracking maps precisely mapped to global 28,000 array
mask_armor = np.arange(MAX_PARTICLES) < NUM_ARMOR
mask_penetrator = ~mask_armor

mask_spall = np.zeros(MAX_PARTICLES, dtype=bool)
mask_spall[spall_indices] = True

mask_armor_core = mask_armor.copy()
mask_armor_core[spall_indices] = False # The part of the block that survives

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, proj_x, proj_y, z_depth, colors, sizes, bio_tax, is_flash, is_tathata = packet
    
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
        # Background Grid structure
        for g_line in np.linspace(-150, 150, 5):
            ax.plot([-100, 100], [g_line, g_line], color=C_DIM, lw=1.0, alpha=0.3, zorder=1)

        # Depth Sorting
        sort_idx = np.argsort(z_depth)
        s_px = proj_x[sort_idx]
        s_py = proj_y[sort_idx]
        s_c = colors[sort_idx]
        s_s = sizes[sort_idx]

        ax.scatter(s_px, s_py, s=s_s, color=s_c, edgecolors='none', alpha=0.9, zorder=10)

        if is_tathata:
            ax.add_patch(plt.Rectangle((-140, -100), 280, 200, facecolor='none', edgecolor=C_MAGENTA, lw=3, zorder=40))
            ax.text(0, -70, "TATHĀTĀ: BIOLOGICAL TRANSLATION TAX", color=C_MAGENTA, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 80, "DIAGNOSTIC: FATAL\n[THE SHIELD BECOMES THE SHRAPNEL]", color=C_TEXT, fontsize=10, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_DIM if t_sec < 4.5 else (C_MAGENTA if t_sec < 9.0 else C_GOLD)
    if is_tathata: ui_col = C_MAGENTA
    
    ax.text(-140, 240, "LG-240 :: THE VACUUM SPALL", color=txt_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: HUGONIOT ELASTIC LIMIT / ARMOR FAILURE", color=txt_col, fontsize=8, fontname='monospace', zorder=80)
    
    obj_str = "HUGONIOT BASELINE [IMPROBABLE SHIELD]"
    if 4.5 <= t_sec < 9.0: obj_str = "HYDRODYNAMIC SHEAR [ACOUSTIC SHOCKWAVE]"
    elif 9.0 <= t_sec < 14.8: obj_str = "THE POP [TENSILE YIELD SPALLATION]"
    elif is_tathata: obj_str = "RAGGED EDGE [BIOLOGICAL FAILURE]"

    ax.text(-140, -180, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Thermodynamic Hardware Metric: Tensile Load / Biological Survivability Inverse
    ax.text(-140, -205, "INTERNAL TENSILE LOAD MATRIX", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    bar_w = 280 * np.clip(bio_tax, 0, 1)
    ax.add_patch(plt.Rectangle((-140, -210), bar_w, 4, facecolor=ui_col, zorder=81))

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
        
        # Angled isometric view down the Y-axis (direction of travel)
        cam_rx = np.pi/6 - (t_sec * 0.01)
        cam_ry = t_sec * 0.15 
        cam_rz = 0.0
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 4.0
        
        curr_x = np.copy(base_px)
        curr_y = np.copy(base_py)
        curr_z = np.copy(base_pz)

        bio_tax = 0.0

        # Phase 1 Defaults
        colors[mask_armor_core] = c_dim
        colors[mask_spall] = c_dim
        colors[mask_penetrator] = c_text
        sizes[mask_armor_core] = 3.0
        sizes[mask_spall] = 3.0
        sizes[mask_penetrator] = 5.0

        # -------------------------------------------------------------
        # THE SPALL EXPANSION LOGIC
        # -------------------------------------------------------------
        if t_sec < 4.5:
            state = "PHASE 1 :: THE HUGONIOT BASELINE"
            prog = t_sec / 4.5
            
            # The penetrator accelerates brutally towards the armor face (Y=-25)
            curr_y[mask_penetrator] += (115.0 * (prog ** 3))
            
            bio_tax = 0.05

        elif t_sec < 9.0:
            state = "PHASE 2 :: HYDRODYNAMIC SHEAR TENSOR"
            prog = (t_sec - 4.5) / 4.5
            if t_sec < 4.6: is_flash = True # The actual impact event
            
            # Penetrator halts exactly at the front armor face
            curr_y[mask_penetrator] = base_py[mask_penetrator] + 115.0 
            curr_y[mask_penetrator] = np.clip(curr_y[mask_penetrator], None, -25.0)
            
            # Acoustic shockwave expands linearly inside the block from Y=-25 to Y=25
            shock_front_y = -25.0 + (50.0 * prog)
            
            # Identify armor particles inside the shock band
            shock_band = (curr_y[mask_armor] < shock_front_y) & (curr_y[mask_armor] > shock_front_y - 15.0)
            colors[np.where(mask_armor)[0][shock_band]] = c_magenta
            sizes[np.where(mask_armor)[0][shock_band]] = 6.0
            
            bio_tax = 0.5 * prog # The internal pressure rises exponentially

        elif t_sec < 14.8:
            state = "PHASE 3 :: THE VACUUM SPALL [YIELD]"
            prog = (t_sec - 9.0) / 5.8
            if t_sec < 9.1: is_flash = True # The backface detaches
            
            # Penetrator is arrested.
            curr_y[mask_penetrator] = base_py[mask_penetrator] + 115.0 
            curr_y[mask_penetrator] = np.clip(curr_y[mask_penetrator], None, -25.0)
            
            # The acoustic shockwave hit the back face. It reflects. The steel snaps.
            time_burst = prog * 5.8
            curr_x[mask_spall] += spall_vel_x * time_burst
            curr_y[mask_spall] += spall_vel_y * time_burst
            curr_z[mask_spall] += spall_vel_z * time_burst
            
            colors[mask_spall] = c_gold
            sizes[mask_spall] = 5.0
            
            # The main armor block remains visibly intact, revealing the trap (The shield survived)
            colors[mask_armor_core] = c_dim
            
            bio_tax = 0.5 + (0.5 * (prog**0.5)) # Biological limits categorically exceeded

        else:
            state = "TATHĀTĀ :: EXTREME TRANSLATION TAX"
            is_tathata = True
            
            # Freeze-frame the catastrophic expansion. Biological merge failed.
            time_burst = 5.8
            curr_x[mask_spall] += spall_vel_x * time_burst
            curr_y[mask_spall] += spall_vel_y * time_burst
            curr_z[mask_spall] += spall_vel_z * time_burst
            
            curr_y[mask_penetrator] = base_py[mask_penetrator] + 115.0 
            curr_y[mask_penetrator] = np.clip(curr_y[mask_penetrator], None, -25.0)
            
            colors[mask_spall] = c_gold
            sizes[mask_spall] = 5.0
            sizes[mask_armor_core] = 2.0 # Fade the block out slightly
            
            bio_tax = 1.0 # 100% Lethality Array
            
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

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], colors[cull_mask], sizes[cull_mask], bio_tax, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 240: THE VACUUM SPALL [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Boolean Axis Alignment & Dynamic Velocity Spall Vectors")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Kinetic Trap Sprung. Inhabitants Deleted.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
