"""
SOVEREIGN CODE: logic_garden_193_gravitational_entrainment.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Relativistic Tensor (17.5 seconds)
SCENE: Logic Garden 193 (The Einstein Tensor / Gravitational Lensing)
HOTFIX: Namespace Resolution 'C_DIM', O(N) Matrix Raytracing, Tathata Alignment
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_193_einstein"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#000000'        # Absolute Vacuum (Event Horizon)
C_DEEP      = '#020205'        # Cosmic Background
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'        # Telemetry Base Structure (HOTFIX)
C_CYAN      = '#00FFFF'        # Structural Geometry (Source Plane)
C_MAGENTA   = '#FF00FF'        # Relativistic Doppler Shift (Friction)
C_MANTIS    = '#00FF00'        # Perfect Einstein Alignment (Tathata)
C_RED       = '#FF0033'        # UI Overload

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_void = np.array(hex_to_rgba(C_VOID)[:3])
c_cy   = np.array(hex_to_rgba(C_CYAN)[:3])
c_mag  = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_man  = np.array(hex_to_rgba(C_MANTIS)[:3])
c_bg   = np.array(hex_to_rgba(C_DEEP)[:3])

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE RELATIVISTIC BOUNDING BOX
# ------------------------------------------------------------------
RES_W, RES_H = 1080, 1920
CX, CY = 540, 960

# Einstein Ring Radius (Mass of the Singularity)
THETA_E = 320.0 

# O(1) Spatial Meshgrid Initialization
y_arr, x_arr = np.mgrid[0:RES_H, 0:RES_W]
dx = x_arr - CX
dy = y_arr - CY

# Distance from lens center (Image Plane)
theta_r = np.sqrt(dx**2 + dy**2)
# Prevent division by zero at the exact singularity
theta_r_safe = np.where(theta_r < 1.0, 1.0, theta_r)

# O(1) Relativistic Deflection Equation
# Beta = Theta * (1 - Theta_E^2 / Theta^2)
deflect_factor = 1.0 - (THETA_E**2 / theta_r_safe**2)
beta_x_global = dx * deflect_factor
beta_y_global = dy * deflect_factor

# Event Horizon Mask (Schwarzschild Radius proxy for visuals)
horizon_mask = theta_r < (THETA_E * 0.15)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, src_x, src_y, is_flash, is_tathata, warp_mult, bg_strobe = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    # Background logic
    bg_hex = C_TEXT if is_flash else C_DEEP
    if bg_strobe and not is_tathata: bg_hex = '#0A0A15'
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)

    # 1. O(N) TENSOR RAYTRACING (Source Plane to Image Plane Mapping)
    if not is_flash:
        # Distance from source light in the Source Plane
        dist_sq = (beta_x_global - src_x)**2 + (beta_y_global - src_y)**2
        
        # Source Profile: A Hyper-bright core wrapped in a rigid geometric grid
        core_radius_sq = 120.0**2
        intensity = np.exp(-dist_sq / core_radius_sq)
        
        # Structural Grid (Visual Friction Matrix)
        grid_freq = 0.05
        grid_matrix = (np.sin(beta_x_global * grid_freq) * np.sin(beta_y_global * grid_freq))**4
        # Mask the grid so it only appears where the source light is illuminating it
        structure = grid_matrix * np.exp(-dist_sq / (600.0**2)) * warp_mult

        # Chromatic Mapping
        img = np.zeros((RES_H, RES_W, 3))
        
        # Base core color
        base_color = c_man if is_tathata else c_cy
        friction_color = c_man if is_tathata else c_mag
        
        # Add Structural Grid (Friction)
        img += structure[:, :, None] * friction_color
        
        # Add Lensed Core
        img += intensity[:, :, None] * base_color
        
        # White hot center clipping
        core_burn = np.maximum(0, intensity - 0.7) * 3.0
        img += core_burn[:, :, None]
        
        # Apply Absolute Event Horizon
        img[horizon_mask] = c_void

        # Clip values to valid RGB float [0, 1]
        img = np.clip(img, 0.0, 1.0)
        
        # Fast render via matplotlib imshow
        ax.imshow(img, origin='lower', extent=[0, RES_W, 0, RES_H], aspect='auto', zorder=10)

        # Photon Sphere glow
        if not is_tathata:
            ax.add_patch(Circle((CX, CY), THETA_E * 0.18, fill=False, edgecolor=C_MAGENTA, lw=2, alpha=0.5, zorder=15))

    # Hardware Flash Geometry
    if is_flash:
        ax.add_patch(Circle((CX, CY), THETA_E, fill=False, edgecolor=C_MANTIS, lw=80, alpha=0.9, zorder=60))
        ax.add_patch(Circle((CX, CY), THETA_E, fill=False, edgecolor=C_TEXT, lw=25, zorder=61))

    # 2. TELEMETRY WIDGETS (NEURAL ENTRAINMENT UI)
    ui_col = C_CYAN if not is_tathata else C_MANTIS
    if is_flash: ui_col = C_VOID
    txt_col = C_TEXT if not is_flash else C_VOID
    ui_bg   = C_VOID if not is_flash else C_TEXT
    
    # Top Data Bar
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=ui_bg, alpha=0.9, zorder=80))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    ax.text(0.04, 0.965, "LG-193 :: RELATIVISTIC LENS (OPTICAL COMPILER)", transform=ax.transAxes, color=txt_col, fontsize=22, fontname='monospace', weight='bold', va='center', zorder=81)

    # Bottom Data Block
    ax.add_patch(plt.Rectangle((0, 0), 1.0, 0.12, transform=ax.transAxes, color=ui_bg, alpha=0.95, zorder=80))
    ax.plot([0, 1.0], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    
    # Alignment Vector
    miss_dist = np.sqrt(src_x**2 + src_y**2)
    alignment_pc = max(0, 100.0 - (miss_dist / 10.0))
    if is_tathata: alignment_pc = 100.0
    
    ax.text(0.04, 0.08, f"SPACETIME ALIGNMENT: {alignment_pc:06.2f}%", transform=ax.transAxes, color=txt_col, fontsize=20, fontname='monospace', zorder=81)
    
    # Load Bar (Fully resolved C_DIM injection)
    ax.add_patch(plt.Rectangle((0.72, 0.03), 0.25, 0.02, transform=ax.transAxes, color=C_DIM, zorder=80))
    bar_fill = min(1.0, alignment_pc / 100.0)
    bar_color = C_MAGENTA if warp_mult > 1.5 else ui_col
    if alignment_pc > 95.0: bar_color = C_RED
    if is_flash: bar_color = C_VOID
    if is_tathata: bar_color = C_MANTIS
    
    ax.add_patch(plt.Rectangle((0.72, 0.03), 0.25 * bar_fill, 0.02, transform=ax.transAxes, color=bar_color, zorder=81))

    pulse = ui_col if (f % 10 < 5) and not is_flash else txt_col
    if warp_mult > 2.0 and not is_tathata and f % 4 < 2: pulse = C_RED # Deformation warning
    if is_flash: pulse = C_VOID
    if is_tathata and not is_flash: pulse = C_MANTIS

    ax.text(0.04, 0.03, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=22, fontname='monospace', weight='bold', zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) RELATIVISTIC KINEMATICS STREAM
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        is_flash = False
        is_tathata = False
        bg_strobe = False
        warp_mult = 1.0
        
        # Source vector approaches singularity from behind
        # Start far bottom-left, end dead center at Tathata
        start_x, start_y = -800.0, -1200.0
        
        # ---- PHASE 1: GEOMETRIC APPROACH (0 - 5s) ----
        if t_sec < 5.0:
            state = "[01] MASS DETECTED :: EUCLIDEAN GEOMETRY STABLE"
            prog = t_sec / 5.0
            cur_x = start_x * (1 - prog*0.4)
            cur_y = start_y * (1 - prog*0.4)
            
        # ---- PHASE 2: OPTICAL SHEARING (5 - 12s) ----
        elif t_sec < 12.0:
            state = "[02] CRITICAL LENSING :: STRUCTURAL DEFORMATION OCCURRING"
            prog = (t_sec - 5.0) / 7.0
            cur_x = (start_x * 0.6) * (1 - prog) + (-200 * prog)
            cur_y = (start_y * 0.6) * (1 - prog) + (-300 * prog)
            warp_mult = 1.0 + prog * 1.5

        # ---- PHASE 3: THE CAUSTIC THRESHOLD / OVERLOAD (12 - 14.8s) ----
        elif t_sec < 14.8:
            state = "WARNING: MAXIMUM GRAVITATIONAL FRICTION. VECTOR TEARING."
            prog = (t_sec - 12.0) / 2.8
            # Snap violently toward the center 0,0 relative
            cur_x = -200 * (1 - prog)
            cur_y = -300 * (1 - prog)
            warp_mult = 2.5 + prog * 3.0
            if t_sec > 13.5: bg_strobe = True

        # ---- PHASE 4: TATHĀTĀ / EINSTEIN RING (14.8 - 17.5s) ----
        else:
            is_tathata = True
            cur_x = 0.0
            cur_y = 0.0
            warp_mult = 0.0
            if t_sec < 14.95:
                is_flash = True
            state = "TATHĀTĀ: ABSOLUTE SYMMETRY ACHIEVED. THE MATRIX IS A LENS."

        yield (f, t_sec, state, cur_x, cur_y, is_flash, is_tathata, warp_mult, bg_strobe)

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 193: THE EINSTEIN TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: O(1) Matrix Raytracing & Deformation Scaling")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Resolution: 1080x1920")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=4):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
