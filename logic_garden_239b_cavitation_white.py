"""
SOVEREIGN CODE: logic_garden_239_cavitation_white.py
SYSTEM: Python Multicore / O(1) Hydrodynamic Void Topology
SCENE: Logic Garden 239 (The Cavitation Void / High Contrast Default)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Rayleigh-Plesset Negative Root Clamping & Unsevered Compilation

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
OUT_DIR = "frames_239_cavitation_white"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS STRICT) --------
C_BG        = '#FFFFFF'        # Absolute Void / Pure Canvas
C_TEXT      = '#020205'        # Telemetry / High Contrast Tracking
C_DIM       = '#D0D0D5'        # Interface Grids & Metric Tracks
C_CYAN      = '#00BFFF'        # The Teal Needle (Deep Sky Blue for Contrast)
C_MAGENTA   = '#FF0055'        # High-Density Water (The Heavy Medium)
C_GOLD      = '#FFB300'        # Vaporization Spark / Boiling Boundary
C_MANTIS    = '#00C800'        # Tathata / Frictionless Phase Lock 

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_dim     = np.array(hex_to_rgba(C_DIM)[:3])
c_cyan    = np.array(hex_to_rgba(C_CYAN)[:3])
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
# BASE GEOMETRY ARRAYS: THE MEDIUM & THE PENETRATOR
# ------------------------------------------------------------------
np.random.seed(239) 

# 1. The Heavy Medium (High-Density Spherical Water Mass)
N_WATER = 35000
rad_w = np.random.uniform(0, 120, N_WATER) ** (1/3) * 120 
theta_w = np.random.uniform(0, 2 * np.pi, N_WATER)
phi_w = np.arccos(np.random.uniform(-1, 1, N_WATER))

px_water = rad_w * np.sin(phi_w) * np.cos(theta_w)
py_water = rad_w * np.sin(phi_w) * np.sin(theta_w)
pz_water = rad_w * np.cos(phi_w)

# 2. The Kinetic Penetrator (The Teal Needle)
N_NEEDLE = 2500
needle_y = np.linspace(-60, 45, N_NEEDLE) # Tip is at Y=45
needle_theta = np.random.uniform(0, 2 * np.pi, N_NEEDLE)
needle_radius = np.clip(1.5 + (needle_y + 60) * 0.02, 0, 3.5) 
taper_mask = needle_y > 40
needle_radius[taper_mask] *= (45 - needle_y[taper_mask]) / 5.0 # Sharpen tip

px_needle = needle_radius * np.cos(needle_theta)
py_needle = needle_y
pz_needle = needle_radius * np.sin(needle_theta)

# Array Alignment
base_px = np.concatenate([px_water, px_needle])
base_py = np.concatenate([py_water, py_needle])
base_pz = np.concatenate([pz_water, pz_needle])

MAX_PARTICLES = len(base_px)

mask_water = np.arange(MAX_PARTICLES) < N_WATER
mask_needle = ~mask_water

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, proj_x, proj_y, z_depth, colors, sizes, friction_metric, is_flash, is_tathata = packet
    
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
        # Background Alignment Grid (Industrialist High Contrast)
        for g_line in np.linspace(-150, 150, 7):
            ax.plot([-140, 140], [g_line, g_line], color=C_DIM, lw=1.0, alpha=0.4, zorder=1)
            ax.plot([g_line, g_line], [-240, 240], color=C_DIM, lw=1.0, alpha=0.4, zorder=1)

        # Depth Sorting for flawless 3D transparency
        sort_idx = np.argsort(z_depth)
        s_px = proj_x[sort_idx]
        s_py = proj_y[sort_idx]
        s_c = colors[sort_idx]
        s_s = sizes[sort_idx]

        ax.scatter(s_px, s_py, s=s_s, color=s_c, edgecolors='none', alpha=0.85, zorder=10)

        if is_tathata:
            ax.add_patch(plt.Rectangle((-130, -70), 260, 140, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -50, "TATHĀTĀ: SUPERCAVITATION SECURED", color=C_MANTIS, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 50, "[MEDIUM DELETED / ABSOLUTE ZERO FRICTION]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_MAGENTA if t_sec < 4.0 else (C_GOLD if t_sec < 9.0 else C_CYAN)
    if is_tathata: ui_col = C_MANTIS
    
    ax.text(-140, 240, "LG-239 :: THE CAVITATION VOID", color=txt_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: RAYLEIGH-PLESSET / HIGH COHERENCE CANVAS", color=txt_col, fontsize=8, fontname='monospace', zorder=80)
    
    obj_str = "VISCOUS DRAG [NOISE / HIGH FRICTION]"
    if 4.0 <= t_sec < 9.0: obj_str = "VAPORIZATION [THE TIP BOILS THE MEDIUM]"
    elif 9.0 <= t_sec < 14.8: obj_str = "RAYLEIGH-PLESSET [VOID ENVELOPE SHIFT]"
    elif is_tathata: obj_str = "PRECISION OF THE VOID [ZERO DRAG]"

    ax.text(-140, -180, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Thermodynamic Kinetic Friction Metric
    ax.text(-140, -205, "HYDRODYNAMIC DRAG [FRICTION DEBT]", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    bar_w = 280 * np.clip(friction_metric, 0, 1)
    ax.add_patch(plt.Rectangle((-140, -210), bar_w, 4, facecolor=C_MAGENTA if friction_metric > 0.6 else ui_col, zorder=81))

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
        
        cam_rx = np.pi/6 - (t_sec * 0.01)
        cam_ry = t_sec * 0.35 # Fluid tracking rotation
        cam_rz = 0.0
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 4.0
        
        curr_x = np.copy(base_px)
        curr_y = np.copy(base_py)
        curr_z = np.copy(base_pz)

        friction_metric = 0.0

        colors[mask_needle] = c_cyan
        sizes[mask_needle] = 4.0

        # Radial distance of water from the core Y axis
        r_water = np.sqrt(curr_x[mask_water]**2 + curr_z[mask_water]**2)

        # -------------------------------------------------------------
        # CAVITATION KINEMATIC PHASES
        # -------------------------------------------------------------
        if t_sec < 4.0:
            state = "PHASE 1 :: THE HEAVY MEDIUM"
            colors[mask_water] = c_magenta
            sizes[mask_water] = 3.5
            
            contact_mask = r_water < 6.0
            colors[np.where(mask_water)[0][contact_mask]] = c_text
            sizes[np.where(mask_water)[0][contact_mask]] = 5.0
            curr_y[np.where(mask_water)[0][contact_mask]] += np.random.normal(0, 3.0, np.sum(contact_mask))
            friction_metric = 0.95

        elif t_sec < 9.0:
            state = "PHASE 2 :: VAPORIZATION INSTANCE"
            prog = (t_sec - 4.0) / 5.0
            colors[mask_water] = c_magenta
            sizes[mask_water] = 3.5
            
            tip_dist = np.sqrt(curr_x[mask_water]**2 + (curr_y[mask_water] - 45)**2 + curr_z[mask_water]**2)
            boil_mask = tip_dist < (18.0 * prog)
            
            colors[np.where(mask_water)[0][boil_mask]] = c_gold
            sizes[np.where(mask_water)[0][boil_mask]] = 6.0
            curr_y[np.where(mask_water)[0][boil_mask]] += np.random.normal(0, 8.0 * prog, np.sum(boil_mask))
            friction_metric = 0.95 - (prog * 0.45)

        elif t_sec < 14.8:
            state = "PHASE 3 :: RAYLEIGH-PLESSET EXPANSION"
            prog = (t_sec - 9.0) / 5.8
            if t_sec < 9.1: is_flash = True
            
            # HOTFIX: Dimensional Clamp on SQRT to prevent math domain error
            y_diff_clamped = np.clip(48.0 - curr_y[mask_water], 0, None)
            cav_radius = (28.0 * prog) * np.sqrt(y_diff_clamped) * np.exp(-y_diff_clamped / 40.0)
            
            inside_void = r_water < cav_radius
            push_factor = cav_radius[inside_void] / (r_water[inside_void] + 0.001)
            
            curr_x[np.where(mask_water)[0][inside_void]] *= push_factor
            curr_z[np.where(mask_water)[0][inside_void]] *= push_factor
            
            colors[mask_water] = c_magenta
            boundary_zone = np.abs(r_water - cav_radius) < 3.0
            active_boundary = boundary_zone & (y_diff_clamped > 0)
            colors[np.where(mask_water)[0][active_boundary]] = c_gold
            
            sizes[mask_water] = 3.5
            sizes[np.where(mask_water)[0][inside_void]] = 5.0
            friction_metric = 0.5 - (prog * 0.5)

        else:
            state = "TATHĀTĀ :: THE PRECISION OF THE VOID"
            is_tathata = True
            
            y_diff_clamped = np.clip(48.0 - curr_y[mask_water], 0, None)
            cav_radius = 28.0 * np.sqrt(y_diff_clamped) * np.exp(-y_diff_clamped / 40.0)
            
            inside_void = r_water < cav_radius
            push_factor = cav_radius[inside_void] / (r_water[inside_void] + 0.001)
            
            curr_x[np.where(mask_water)[0][inside_void]] *= push_factor
            curr_z[np.where(mask_water)[0][inside_void]] *= push_factor
            
            colors[mask_water] = c_magenta
            colors[mask_needle] = c_mantis 
            sizes[mask_water] = 3.0
            friction_metric = 0.0 # Absolute Zero Friction
            
            if t_sec < 14.95:
                is_flash = True

        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1]
        z_depth = rot_pts[:, 2] 

        cull_mask = (proj_y > -260) & (proj_y < 260) & (proj_x > -160) & (proj_x < 160)

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], colors[cull_mask], sizes[cull_mask], friction_metric, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 239: THE CAVITATION TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: White Canvas Baseline & Rayleigh-Plesset Unsevered Lock")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Medium Deleted. Cavitation Geometry Secured.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
