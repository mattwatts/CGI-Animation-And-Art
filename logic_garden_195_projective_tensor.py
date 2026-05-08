"""
SOVEREIGN CODE: logic_garden_195_projective_tensor.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Real Projective Plane Tensor (17.5 seconds)
SCENE: Logic Garden 195 (The Projective Tensor / Point at Infinity)
HOTFIX: Viewport Bounding Box Guarantee, Dual Parametric Projection, Absolute Coordinate Clamping
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_195_projective_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'        # Euclidean Vacuum
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'        # Base Cartesian Infrastructure
C_CYAN      = '#00FFFF'        # Euclidean Parallel Rails
C_MAGENTA   = '#FF0055'        # Projective Warp / Spatial Friction
C_GOLD      = '#FFD700'        # The Horizon / Point at Infinity
C_RED       = '#FF3300'        # Metric Overload Boundary
C_MANTIS    = '#00FF00'        # Terminal Geometry (Tathata / Incidence Wireframe)

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_void = np.array(hex_to_rgba(C_VOID)[:3])
c_cyan = np.array(hex_to_rgba(C_CYAN)[:3])
c_mage = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_gold = np.array(hex_to_rgba(C_GOLD)[:3])
c_mant = np.array(hex_to_rgba(C_MANTIS)[:3])
c_txt  = np.array(hex_to_rgba(C_TEXT)[:3])

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE KINEMATIC ARCHITECTURE
# ------------------------------------------------------------------
MAX_PARTICLES = 25000

# Absolute Screen Viewport constraints
CAM_W = 200.0
CAM_H = CAM_W * (1920.0 / 1080.0) # 355.55
CENTER_X = 0.0
CENTER_Y = CAM_H / 2.0

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, px, py, p_sizes, c_tensor, horizon_y, w_proj, is_flash, is_tathata, bg_strobe = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_TEXT if is_flash else C_VOID
    if bg_strobe and not is_tathata: bg_hex = '#0A0010' 
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    # Absolute Viewport Lock (No Bounding Box Drifting allowed)
    ax.set_xlim(-CAM_W/2, CAM_W/2)
    ax.set_ylim(0, CAM_H)

    # 1. RENDER THE HORIZON (Line at Infinity)
    if not is_flash and not is_tathata and w_proj > 0.01:
        # Drawing the Euclidean breaking point
        ax.axhline(horizon_y, color=C_GOLD, lw=3, zorder=5)
        ax.add_patch(Rectangle((-CAM_W/2, horizon_y), CAM_W, CAM_H, facecolor=C_VOID, alpha=0.95, zorder=12)) # Mask everything above horizon
        ax.add_patch(Rectangle((-CAM_W/2, horizon_y - 1.0), CAM_W, 2.0, facecolor=C_GOLD, alpha=0.4, zorder=7))

    # 2. O(N) KINEMATIC PROJECTIVE TENSOR
    if len(px) > 0 and not is_tathata:
        ax.scatter(px, py, s=p_sizes*5.0, c=c_tensor, edgecolors='none', alpha=0.4, zorder=10)
        ax.scatter(px, py, s=p_sizes*1.5, c=C_TEXT if is_flash else c_tensor, edgecolors='none', alpha=0.9, zorder=11)

    # 3. TATHĀTĀ / GEOMETRIC INCIDENCE (RP^2 Map)
    if is_tathata and not is_flash:
        # Cross-cap / Antipodal identification disc
        r_disc = CAM_W * 0.35
        # Draw Fundamental Polygon of RP^2
        ax.add_patch(Circle((CENTER_X, CENTER_Y), r_disc, facecolor=C_VOID, edgecolor=C_MANTIS, lw=4, zorder=20))
        
        # Connect antipodal points (The true definition of the Projective Plane)
        angles = np.linspace(0, np.pi, 18, endpoint=False)
        for a in angles:
            x1, y1 = np.cos(a) * r_disc, np.sin(a) * r_disc
            ax.plot([CENTER_X + x1, CENTER_X - x1], [CENTER_Y + y1, CENTER_Y - y1], color=C_MANTIS, lw=1.5, alpha=0.6, zorder=19)
        
        # Central singularity (The Origin)
        ax.scatter([CENTER_X], [CENTER_Y], s=250, color=C_TEXT, edgecolor=C_MANTIS, lw=3, zorder=25)
        
        # Absolute geometric bounding box constraint representation
        ax.add_patch(Rectangle((CENTER_X - r_disc*1.2, CENTER_Y - r_disc*1.2), r_disc*2.4, r_disc*2.4, facecolor='none', edgecolor=C_MANTIS, lw=2, linestyle='--', zorder=18))

    if is_flash:
        # Kinetic Overload Hardware Interrupt Screen Clear
        ax.add_patch(Rectangle((-CAM_W/2, 0), CAM_W, CAM_H, facecolor=C_TEXT, zorder=60))

    # 4. TELEMETRY WIDGETS (NEURAL ENTRAINMENT UI)
    ui_col = C_CYAN if not is_tathata else C_MANTIS
    if w_proj > 0.8: ui_col = C_MAGENTA 
    txt_col = C_TEXT if not is_flash else C_VOID
    ui_bg   = C_VOID if not is_flash else C_TEXT
    
    # Top Bar 
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=ui_bg, alpha=0.9, zorder=80))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    ax.text(0.04, 0.965, "LG-195 :: REAL PROJECTIVE PLANE (RP^2)", transform=ax.transAxes, color=txt_col, fontsize=20, fontname='monospace', weight='bold', va='center', zorder=81)

    # Bottom Target Matrix
    ax.add_patch(plt.Rectangle((0, 0), 1.0, 0.14, transform=ax.transAxes, color=ui_bg, alpha=0.95, zorder=80))
    ax.plot([0, 1.0], [0.14, 0.14], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    
    dim_str = "EUCLIDEAN PARALLELS" if w_proj < 0.05 else "OBLIQUE PROJECTIVE"
    if w_proj > 0.95: dim_str = "INFINITY COMPRESSION"
    if is_tathata: dim_str = "TATHATA [ABSOLUTE INCIDENCE]"
    
    ax.text(0.04, 0.10, f"METRIC MATRIX: {dim_str}", transform=ax.transAxes, color=txt_col, fontsize=18, fontname='monospace', zorder=81)
    
    # Perspective Collapse Bar
    fill_ratio = min(1.0, max(0.0, w_proj))
    bar_col = C_CYAN
    if fill_ratio > 0.6: bar_col = C_MAGENTA
    if fill_ratio > 0.9: bar_col = C_GOLD
    if is_tathata: bar_col = C_MANTIS
    if is_flash: bar_col = C_VOID
    
    ax.add_patch(plt.Rectangle((0.68, 0.03), 0.28, 0.03, transform=ax.transAxes, color=C_DIM, zorder=80))
    ax.add_patch(plt.Rectangle((0.68, 0.03), 0.28 * fill_ratio, 0.03, transform=ax.transAxes, color=bar_col, zorder=81))
    ax.text(0.68, 0.07, f"INFINITY MAPPING: {fill_ratio*100:03.0f}%", transform=ax.transAxes, color=bar_col, fontsize=14, fontname='monospace', zorder=82)

    pulse = ui_col if (f % 10 < 5) and not is_flash else txt_col
    if fill_ratio > 0.9 and not is_tathata and f % 4 < 2: pulse = C_RED
    if is_flash: pulse = C_VOID

    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=20, fontname='monospace', weight='bold', zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)

# ------------------------------------------------------------------
# O(1) BALLISTIC KINEMATICS STREAM
# ------------------------------------------------------------------
def generate_stream():
    # 1. Euclidean Base Structure (The Rails)
    num_lanes = 40
    lanes = np.linspace(-300, 300, num_lanes)
    p_x = np.random.choice(lanes, MAX_PARTICLES)
    # Add minor vibration to hide pixel aliasing on vertical arrays
    p_x += np.random.normal(0, 0.5, MAX_PARTICLES)
    
    # The world depth buffer [0, 2000]
    p_y_relative = np.random.uniform(0, 2000, MAX_PARTICLES)
    
    cam_speed_base = 250.0

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        dt = 0.016
        
        is_flash = False
        is_tathata = False
        bg_strobe = False
        
        # State variables
        w_proj = 0.0
        cam_z = 20.0
        pitch = 0.12
        cam_speed = cam_speed_base
        
        # ---- PHASE 1: THE EUCLIDEAN ILLUSION (0 - 4s) ----
        if t_sec < 4.0:
            state = "[01] CONTINUOUS METRIC :: EUCLIDEAN R^2 PARALLEL RAYS"
            w_proj = 0.0
            
        # ---- PHASE 2: OBLIQUE PROJECTION REGISTRATION (4 - 10s) ----
        elif t_sec < 10.0:
            state = "[02] INJECTING PROJECTION TENSOR :: INCIDENCE MAPPING"
            prog = smoothstep((t_sec - 4.0) / 6.0)
            w_proj = prog
            cam_speed = cam_speed_base * (1.0 + prog * 1.5)

        # ---- PHASE 3: COMPRESSION / POINT AT INFINITY (10 - 14.8s) ----
        elif t_sec < 14.8:
            state = "WARNING: INFINITY METRIC ACQUIRED. HORIZON COLLAPSE."
            prog = (t_sec - 10.0) / 4.8
            w_proj = 1.0
            # Camera begins dropping aggressively toward the surface, amplifying optical friction
            cam_z = 20.0 - (prog * 17.0) 
            pitch = 0.12 + (prog * 0.03) 
            cam_speed = cam_speed_base * 2.5 * (1.0 + (prog**3) * 8.0)
            
            if t_sec > 13.5: bg_strobe = True

        # ---- PHASE 4: TATHĀTĀ / ABSOLUTE PROJECTIVE GEOMETRY (14.8 - 17.5s) ----
        else:
            is_tathata = True
            w_proj = 1.0
            cam_speed = 0.0
            
            if t_sec < 14.95:
                is_flash = True
            state = "TATHĀTĀ: DISTANCE IS A LIE. ONLY INCIDENCE IS TRUTH."

        # -------------------------------------------------------------
        # THE CALCULUS OF PROJECTION
        # -------------------------------------------------------------
        # Update kinematic distance over the endless 2000-unit loop
        p_y_relative = (p_y_relative - cam_speed * dt) % 2000.0
        dy = p_y_relative # Physical distance ahead of the camera lens
        
        # 1. AFFINE OUTPUT (Euclidean Top-Down)
        # Scale X dynamically so the outer rails are near -100 to +100
        px_affine = p_x * 0.3
        # Scale Y so 0-2000 fits perfectly into 0-CAM_H (355.5)
        py_affine = dy * (CAM_H / 2000.0)
        
        # 2. PERSPECTIVE OUTPUT (Projective Metric)
        dz = cam_z
        y_rot = dy * np.cos(pitch) - dz * np.sin(pitch)
        z_rot = dy * np.sin(pitch) + dz * np.cos(pitch)
        
        # Div by zero guard
        z_safe = np.clip(z_rot, 0.1, 9999.0)
        
        # Calculate projection. Focal length tuned to match horizontal affine width
        focal = 35.0
        px_proj = (p_x * focal) / z_safe
        py_proj = ((y_rot * focal) / z_safe) + 15.0 # Elevate the ground visually
        
        # Horizon mathematical true limit (where dy -> infinity)
        # py_inf = (cos(pitch)*focal)/sin(pitch) = focal/tan(pitch) + 15
        horizon_y = (focal / np.tan(pitch)) + 15.0
        
        # 3. INTERPOLATION (Blending the Geometries)
        px_final = px_affine * (1.0 - w_proj) + px_proj * w_proj
        py_final = py_affine * (1.0 - w_proj) + py_proj * w_proj
        
        # Mask out particles that technically render "below" the camera or way off screen
        active_mask = (py_final > -10) & (py_final < CAM_H + 50) & (px_final > -120) & (px_final < 120)

        # -------------------------------------------------------------
        # THERMODYNAMIC CHROMATIC MAPPING
        # -------------------------------------------------------------
        p_sizes = np.ones(MAX_PARTICLES)
        c_tensor = np.zeros((MAX_PARTICLES, 3))
        
        if np.any(active_mask):
            c_tensor[active_mask] = c_cyan
            
            # Heat increases as they approach the horizon (dy -> 2000)
            heat = dy[active_mask] / 2000.0
            
            # Apply color mapping
            # < 0.5 is Cyan. 0.5 to 0.8 is Magenta. > 0.8 is Gold.
            c_tensor[active_mask] = np.where(heat[:, None] > 0.5, 
                                             c_mage * (heat[:, None] - 0.5)*2.0 + c_cyan * (1.0 - (heat[:, None] - 0.5)*2.0), 
                                             c_cyan)
                                             
            gold_mask = heat > 0.85
            if np.any(gold_mask):
                c_tensor[active_mask][gold_mask] = c_gold
                
            # Depth perception sizing (bigger near the camera, small at horizon)
            p_sizes[active_mask] = 1.0 + (1.0 - heat) * 3.0 * w_proj + (1.0 - heat) * 1.5 * (1-w_proj)

        if is_tathata:
            c_tensor[:] = c_mant
            p_sizes[:] = 1.0
            
        c_tensor = np.clip(c_tensor, 0.0, 1.0)

        yield (f, t_sec, state, np.copy(px_final[active_mask]), np.copy(py_final[active_mask]), p_sizes[active_mask], c_tensor[active_mask], horizon_y, w_proj, is_flash, is_tathata, bg_strobe)

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 195: THE PROJECTIVE TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Absolute Bounding Box Alignment & Parametric Scaling")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Nodes: {MAX_PARTICLES}")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
