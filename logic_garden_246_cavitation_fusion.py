"""
SOVEREIGN CODE: logic_garden_246_cavitation_fusion.py
SYSTEM: Python Multicore / O(1) Kinetic Topology & Adiabatic Compression
SCENE: Logic Garden 246 (Cavitation Fusion / The Hammers)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Float Broadcast Mitigation & O(N) Shockwave Convergence

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
OUT_DIR = "frames_246_cavitation"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS DEFAULT) --------
C_BG        = '#FFFFFF'        # Absolute Void / The Inner Bubble
C_TEXT      = '#020205'        # UI / High Contrast Structural Housing
C_AZURE     = '#007FFF'        # The Liquid Metal Vortex (Lead/Lithium Matrix)
C_GOLD      = '#FFB300'        # The Hammers / Acoustic Shockwaves
C_MAGENTA   = '#FF0055'        # Thermal Spallation / Adiabatic Compression
C_MANTIS    = '#00C800'        # Tathata / The Pop (Q > 1 Ignition)
C_DIM       = '#D0D0D5'        # Heat-Sink Geometry

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_azure   = np.array(hex_to_rgba(C_AZURE)[:3])
c_gold    = np.array(hex_to_rgba(C_GOLD)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
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
# BASE GEOMETRY ARRAYS: STATIC PRE-ALLOCATION
# ------------------------------------------------------------------
np.random.seed(246) 

MAX_PARTICLES = 28000

# 1. The Liquid Metal Vortex (A hollow spinning cylinder)
theta_v = np.random.uniform(0, 2 * np.pi, MAX_PARTICLES)
r_v = np.sqrt(np.random.uniform(0, 1.0, MAX_PARTICLES)) * 90.0 + 35.0  # Void from 0 to 35
y_v = np.random.uniform(-140, 140, MAX_PARTICLES)

px_base = r_v * np.cos(theta_v)
py_base = y_v
pz_base = r_v * np.sin(theta_v)

# Store local 2D radius for accurate shockwave calculations
radial_dist_base = np.sqrt(px_base**2 + pz_base**2)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, p_x, p_y, p_z, c_arr, s_arr, compress_metric, is_flash, is_tathata = packet
    
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
        # Piston Hammer Geometry (Rendered behind the fluid matrix)
        if 4.5 <= t_sec < 14.8:
            hammer_pulse = np.abs(np.sin(t_sec * 30.0))
            for ang in np.linspace(0, 2*np.pi, 12, endpoint=False):
                hx_start = 150 * np.cos(ang)
                hz_start = 150 * np.sin(ang)
                # Hammers physically jab inward
                hx_end = (130 - (15 * hammer_pulse)) * np.cos(ang)
                hz_end = (130 - (15 * hammer_pulse)) * np.sin(ang)
                
                # Isometric flattening for visual 3D
                hx_s_rot, hy_s_rot, _ = rotate_3d(np.array([[hx_start, 0, hz_start]]), np.pi/8, t_sec*0.4, 0)[0]
                hx_e_rot, hy_e_rot, _ = rotate_3d(np.array([[hx_end, 0, hz_end]]), np.pi/8, t_sec*0.4, 0)[0]
                
                ax.plot([hx_s_rot, hx_e_rot], [hy_s_rot, hy_e_rot], color=C_GOLD, lw=4, alpha=0.8, zorder=5)

        # Depth Sorting for perfectly overlapping 3D points
        sort_idx = np.argsort(p_z)
        s_x = p_x[sort_idx]
        s_y = p_y[sort_idx]
        s_c = c_arr[sort_idx]
        s_size = s_arr[sort_idx]

        ax.scatter(s_x, s_y, s=s_size, color=s_c, edgecolors='none', alpha=0.9, zorder=10)

        # Tathata Core Ignition
        if is_tathata:
            ax.add_patch(plt.Circle((0, 0), 40, color=C_MANTIS, alpha=0.3, zorder=30))
            ax.add_patch(plt.Circle((0, 0), 20, color=C_MANTIS, alpha=0.8, zorder=31))
            ax.scatter([0], [0], s=300, color=C_BG, zorder=32) # The absolute center is clean white
            
            ax.add_patch(plt.Rectangle((-130, -100), 260, 200, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -70, "TATHĀTĀ: Q > 1 / FUSION IGNITION", color=C_MANTIS, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 80, "[LAWS OF CHEMISTRY OVERWRITTEN]", color=C_TEXT, fontsize=10, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_AZURE if t_sec < 4.5 else (C_GOLD if t_sec < 11.0 else C_MAGENTA)
    if is_tathata: ui_col = C_MANTIS
    
    ax.text(-140, 240, "LG-246 :: CAVITATION FUSION", color=txt_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: ACOUSTIC INERTIAL CONFINEMENT / PINCH KINEMATICS", color=txt_col, fontsize=8, fontname='monospace', zorder=80)
    
    obj_str = "THE VORTEX SUBSTRATE [LIQUID METAL MASS]"
    if 4.5 <= t_sec < 11.0: obj_str = "HAMMER INJECTIONS [ACOUSTIC SHOCKWAVES]"
    elif 11.0 <= t_sec < 14.8: obj_str = "ADIABATIC PEAK [THERMAL SPALLATION]"
    elif is_tathata: obj_str = "THE POP [ABSOLUTE PHASE COHERENCE]"

    ax.text(-140, -180, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Thermodynamic Hardware Metric: Core Pressure Debt
    ax.text(-140, -205, "ADIABATIC CORE PRESSURE MATRIX", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    bar_w = 280 * np.clip(compress_metric, 0, 1)
    ax.add_patch(plt.Rectangle((-140, -210), bar_w, 4, facecolor=C_MANTIS if is_tathata else ui_col, zorder=81))

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
        
        # Isometric look-down vector
        cam_rx = np.pi/8 
        cam_ry = t_sec * 0.4 # Entire rig slowly rotates
        cam_rz = 0.0
        
        c_arr = np.zeros((MAX_PARTICLES, 3))
        s_arr = np.ones(MAX_PARTICLES)
        
        curr_x = np.copy(px_base)
        curr_y = np.copy(py_base)
        curr_z = np.copy(pz_base)

        compress_metric = 0.0

        # -------------------------------------------------------------
        # THE FUSION KINEMATICS
        # -------------------------------------------------------------
        
        # Base rotation of the fluid vortex
        vortex_spin = t_sec * 3.0
        c_x = radial_dist_base * np.cos(theta_v + vortex_spin)
        c_z = radial_dist_base * np.sin(theta_v + vortex_spin)
        
        if t_sec < 4.5:
            # PHASE 1: THE VORTEX SUBSTRATE
            state = "PHASE 1 :: THE FLUID ANVIL"
            
            curr_x = c_x
            curr_z = c_z
            
            c_arr[:] = c_azure
            # Micro noise to make the lead look heavy and rippling
            s_arr[:] = 2.0 + np.sin(curr_y * 0.2 + t_sec * 5.0) 
            
            compress_metric = 0.05

        elif t_sec < 11.0:
            # PHASE 2: THE HAMMER INJECTIONS
            state = "PHASE 2 :: ACOUSTIC SHOCKWAVES"
            prog = (t_sec - 4.5) / 6.5
            
            # Shockwave expands from perimeter (125) inward to core (35)
            # The hammers strike repeatedly, creating multiple concentric overlapping waves
            wave_speed = 30.0
            wave_dist = (t_sec * wave_speed) % 40.0
            
            # Map shock front based on current radial distance from absolute center
            shock_front = np.abs((radial_dist_base % 40.0) - wave_dist) < 5.0
            
            curr_x = c_x
            curr_z = c_z
            
            c_arr[:] = c_azure
            c_arr[shock_front] = c_gold
            s_arr[:] = 2.0
            s_arr[shock_front] = 4.0
            
            compress_metric = 0.05 + (0.35 * prog)

        elif t_sec < 14.8:
            # PHASE 3: ADIABATIC PEAK (Thermal Compression)
            state = "PHASE 3 :: THE PINCH"
            prog = (t_sec - 11.0) / 3.8
            if t_sec < 11.1: is_flash = True
            
            ease = prog ** 3 # Exponential violent collapse
            
            # The liquid metal is forced into the void
            # The inner boundary shrinks from 35 down to 1
            crush_factor = 1.0 - (0.8 * ease)
            c_x_crush = (radial_dist_base * crush_factor) * np.cos(theta_v + vortex_spin)
            c_z_crush = (radial_dist_base * crush_factor) * np.sin(theta_v + vortex_spin)
            
            curr_x = c_x_crush
            curr_z = c_z_crush
            
            # High friction thermal bleed mapping
            crushed_radius = radial_dist_base * crush_factor
            thermal_mask = crushed_radius < (80.0 * (1.0 - ease))
            core_mask = crushed_radius < (40.0 - (38.0 * ease))
            
            c_arr[:] = c_azure
            c_arr[thermal_mask] = c_gold
            c_arr[core_mask] = c_magenta
            
            s_arr[:] = 2.0
            s_arr[thermal_mask] = 4.0
            s_arr[core_mask] = 6.0 + (np.random.rand(np.sum(core_mask)) * 5.0 * ease) # Boiling friction
            
            compress_metric = 0.40 + (0.60 * prog)

        else:
            # PHASE 4: THE POP (Tathātā)
            state = "TATHĀTĀ :: LAWS OF CHEMISTRY DELETED"
            is_tathata = True
            
            # The void stabilizes instantly in its compressed structure
            crush_factor = 0.2
            curr_x = (radial_dist_base * crush_factor) * np.cos(theta_v + vortex_spin)
            curr_z = (radial_dist_base * crush_factor) * np.sin(theta_v + vortex_spin)
            
            # Absolute phase coherence
            c_arr[:] = c_azure
            
            # The immediate ring next to the new core turns Mantis Green to denote successful ignition containment
            contained_mask = radial_dist_base * crush_factor < 25.0
            c_arr[contained_mask] = c_mantis
            
            s_arr[:] = 2.0
            s_arr[contained_mask] = 4.0
            
            compress_metric = 1.0 # 100% Core Ignition
            
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

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], c_arr[cull_mask], s_arr[cull_mask], compress_metric, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 246: THE CAVITATION TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: O(N) Shockwave Mechanics & Adiabatic Fluid Clamping")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Medium Crushed. Nucleation Achieved.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
