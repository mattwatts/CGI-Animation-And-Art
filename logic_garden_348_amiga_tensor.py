"""
SOVEREIGN CODE: logic_garden_348_amiga_tensor.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 348 (The Amiga Kinematic Tensor / Boing Ball)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING, OPERATIONS RESEARCH
HOTFIX: Exact 16.0s Seamless Loop. Daylight Protocol. Backface Culling. Dynamic Normal Shading.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
DURATION = 16.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_348_amiga_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Background Matrix Grid
C_STEEL     = '#606065'   # HUD Elements
C_DARK      = '#202025'   # Shadow / Umbra mapping
C_AMIGA_RED = '#E00020'   # The Primary Semantic Target
C_AMIGA_WHT = '#F5F5FA'   # The Secondary Semantic Target
C_MANTIS    = '#00FF00'   # Terminal Green 
C_SHADOW    = '#000000'   # Floor Shadow Base

# ------------------------------------------------------------------
# O(1) SPHERICAL GEOMETRY ENGINE
# ------------------------------------------------------------------
R = 180
LATS = 16
LONS = 32

def generate_sphere_topology():
    quads = []
    base_color_ids = []
    lat = np.linspace(-np.pi/2, np.pi/2, LATS+1)
    lon = np.linspace(0, 2*np.pi, LONS+1)
    
    for i in range(LATS):
        for j in range(LONS):
            # 3D Cartesian coordinates
            v1 = [R*np.cos(lat[i])*np.sin(lon[j]), R*np.sin(lat[i]), R*np.cos(lat[i])*np.cos(lon[j])]
            v2 = [R*np.cos(lat[i+1])*np.sin(lon[j]), R*np.sin(lat[i+1]), R*np.cos(lat[i+1])*np.cos(lon[j])]
            v3 = [R*np.cos(lat[i+1])*np.sin(lon[j+1]), R*np.sin(lat[i+1]), R*np.cos(lat[i+1])*np.cos(lon[j+1])]
            v4 = [R*np.cos(lat[i])*np.sin(lon[j+1]), R*np.sin(lat[i]), R*np.cos(lat[i])*np.cos(lon[j+1])]
            quads.append(np.array([v1, v2, v3, v4]))
            
            # The Algorithmic Checkerboard Pattern
            if (i + j) % 2 == 0:
                base_color_ids.append(C_AMIGA_RED)
            else:
                base_color_ids.append(C_AMIGA_WHT)
                
    return np.array(quads), base_color_ids

RAW_QUADS, RAW_COLORS = generate_sphere_topology()

# Transformation Matrices
def y_rot(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])

def z_rot(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

# Lighting Vector (Locked directional source)
LIGHT_DIR = np.array([0.4, 0.6, 0.8])
LIGHT_DIR = LIGHT_DIR / np.linalg.norm(LIGHT_DIR)

def get_shaded_color(base_hex, intensity):
    rgb = np.array(mcolors.to_rgb(base_hex))
    ambient = 0.3
    diffuse = 0.7 * intensity
    final_rgb = np.clip(rgb * (ambient + diffuse), 0, 1)
    return final_rgb

def draw_industrial_grid(ax):
    for i in range(-5, 6):
        ax.plot([i*100, i*100], [-960, 960], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)
    for j in range(-9, 10):
        ax.plot([-540, 540], [j*100, j*100], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)

def render_frame(packet):
    f, phase_ratio = packet
    t = phase_ratio * DURATION

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # BARE-METAL CAMERA LOCK
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)
    ax.autoscale(False)
    draw_industrial_grid(ax)

    # 1. NEWTONIAN PHYSICS CALCULATOR (Perfect Bounding)
    # --------------------------------------------------
    # Y-Axis Kinematics
    Y_FLOOR = -600 
    Y_MAX_H = 720
    Y_CONTACT = Y_FLOOR + R  # Center Y when touching floor = -420
    T_BOUNCE = 2.0
    
    t_mod_y = t % T_BOUNCE
    # Mathematical Parabola enforcing exactly standard gravity decay per cycle
    y_prg = 4 * (t_mod_y / T_BOUNCE) * (1.0 - (t_mod_y / T_BOUNCE))
    curr_y = Y_CONTACT + Y_MAX_H * y_prg

    # X-Axis Kinematics (Bouncing against strict lateral boundaries)
    X_BOUND = 300
    T_XR = 8.0 # Full left-to-right-to-left
    
    t_mod_x = (t % T_XR) / T_XR
    if t_mod_x <= 0.5:
        # Moving Right
        curr_x = -X_BOUND + (X_BOUND * 2) * (t_mod_x / 0.5)
    else:
        # Moving Left
        curr_x = X_BOUND - (X_BOUND * 2) * ((t_mod_x - 0.5) / 0.5)

    # 2. RENDER SHADOW MAP
    # --------------------
    # O(1) dropping shadow reflecting altitude and intensity
    shadow_w = 340 * (1.0 - y_prg * 0.4)
    shadow_h = 35 * (1.0 - y_prg * 0.4)
    shadow_alpha = np.clip(0.6 - y_prg * 0.5, 0.0, 1.0)
    
    ax.add_patch(patches.Ellipse((curr_x, Y_FLOOR), shadow_w, shadow_h, facecolor=C_SHADOW, alpha=shadow_alpha, zorder=5))
    ax.plot([-540, 540], [Y_FLOOR, Y_FLOOR], color=C_STEEL, lw=6, zorder=4)

    # 3. KINEMATIC SPHERE ROTATION AND PROJECTION
    # -------------------------------------------
    # Tilted exactly 15 degrees right, spinning along local Y
    spin_rads = t * 3.5 # Spin velocity
    R_MAT = z_rot(np.radians(-15)) @ y_rot(spin_rads)
    
    poly_collection = []
    
    for idx, quad in enumerate(RAW_QUADS):
        # Apply strict O(1) rotational matrix
        rot_quad = quad @ R_MAT.T
        
        # Calculate localized Surface Normal
        v1, v2, v3, v4 = rot_quad
        # Cross product of diagonal edges for true face normal
        face_normal = np.cross(v2 - v1, v4 - v1)
        mag = np.linalg.norm(face_normal)
        if mag == 0: continue
        face_normal = face_normal / mag
        
        # Absolute Face Culling (Camera sees +Z geometry)
        if face_normal[2] < -0.05:
            continue
            
        # Thermodynamic Light Interaction (Lambertian intensity)
        intensity = max(0, np.dot(face_normal, LIGHT_DIR))
        final_color = get_shaded_color(RAW_COLORS[idx], intensity)
        
        # Drop to 2D projection and shift to Newtonian coordinate limits
        proj_quad = [[pt[0] + curr_x, pt[1] + curr_y] for pt in rot_quad]
        
        # Add slight boundary stroke to prevent anti-aliasing bleeds
        poly = patches.Polygon(proj_quad, facecolor=final_color, edgecolor=final_color, lw=0.4, zorder=10)
        ax.add_patch(poly)

    # ====================================================
    # 4. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)

    ax.text(-500, 890, "LG-348 :: THE AMIGA KINEMATIC TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] TOPOLOGICAL SPHERE // O(1) HARDWARE OVERRIDE", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    # State Telemetry Logic
    sys_txt = "O(1) RIGID BODY TRANSLATION MATRICES"
    state_txt = "ABSOLUTE ELASTIC COLLISION // 100% ENERGY PRESERVED"
    
    # Audit display flashes Mantis during floor strike
    at_floor = "YES" if y_prg < 0.02 else "NO"
    c_audit = C_MANTIS if y_prg < 0.02 else C_TEXT

    ax.text(-500, -760, "SYS_01 [HARDWARE KINEMATICS] :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, sys_txt, color=C_AMIGA_RED, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [THERMODYNAMICS]      :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, state_txt, color=C_STEEL, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "STRUCTURAL LOAD AUDIT        :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, f"X:{int(curr_x):04d} | Y:{int(curr_y):04d} | GROUND_IMPACT: {at_floor}", color=c_audit, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider [Strict Tuples]
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=C_AMIGA_RED, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close('all')
    gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-348: THE AMIGA KINEMATIC TENSOR [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
