"""
SOVEREIGN CODE: logic_garden_213_fluency_tensor.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(N) Cognitive Fluency Matrix (17.5 seconds)
SCENE: Logic Garden 213 (The Fluency Tensor / Cognitive Ease)
HOTFIX: Parameter Scope Clamping & O(1) Depth-Sorted Tensors
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_213_fluency"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'
C_CYAN      = '#00FFFF'        # High Fluency (The Smooth Lie)
C_MAGENTA   = '#FF0055'        # Disfluency (The Tangled Truth)
C_GOLD      = '#FFD700'        # Sovereign Compilation
C_MANTIS    = '#00FF00'        # Epistemic Truth / Final Geometry

MAX_PARTICLES = 25000

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

# Sovereign Memory Pointers
c_void = np.array(hex_to_rgba(C_VOID)[:3])
c_cyan = np.array(hex_to_rgba(C_CYAN)[:3])
c_mage = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_gold = np.array(hex_to_rgba(C_GOLD)[:3])
c_mantis = np.array(hex_to_rgba(C_MANTIS)[:3])
c_dim = np.array(hex_to_rgba(C_DIM)[:3])
c_text = np.array(hex_to_rgba(C_TEXT)[:3])

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
# BASE GEOMETRY ARRAYS
# ------------------------------------------------------------------
# 1. The Smooth Lie (Perfect Torus Ring - Extremely predictable)
theta_smooth = np.random.uniform(0, 2*np.pi, MAX_PARTICLES)
phi_smooth   = np.random.uniform(0, 2*np.pi, MAX_PARTICLES)
r_major = 90.0
r_minor = 10.0
smooth_x = (r_major + r_minor * np.cos(phi_smooth)) * np.cos(theta_smooth)
smooth_y = (r_major + r_minor * np.cos(phi_smooth)) * np.sin(theta_smooth)
smooth_z = r_minor * np.sin(phi_smooth)

# 2. The Heavy Truth (Dense 3D Lissajous Knot - Extremely high friction to parse)
t_knot = np.linspace(0, 2*np.pi, MAX_PARTICLES)
# We map random jitter to simulate dense computational mass
knot_x = 70.0 * np.sin(3 * t_knot) + np.random.normal(0, 2, MAX_PARTICLES)
knot_y = 70.0 * np.sin(4 * t_knot) + np.random.normal(0, 2, MAX_PARTICLES)
knot_z = 70.0 * np.cos(5 * t_knot) + np.random.normal(0, 2, MAX_PARTICLES)

# 3. The Unfolded Truth (A Massive, flawless sacred geometry matrix / Fibonacci Sphere)
golden_ratio = (1 + 5 ** 0.5) / 2
indices = np.arange(0, MAX_PARTICLES, dtype=float) + 0.5
phi = np.arccos(1 - 2 * indices / MAX_PARTICLES)
theta = 2 * np.pi * indices / golden_ratio
truth_x = 110.0 * np.cos(theta) * np.sin(phi)
truth_y = 110.0 * np.sin(theta) * np.sin(phi)
truth_z = 110.0 * np.cos(phi)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, proj_x, proj_y, z_depth, colors, sizes, is_flash, is_tathata, trust_gauge, friction_gauge = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_TEXT if is_flash else C_VOID
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    ax.set_xlim(-150, 150)
    ax.set_ylim(-260, 260)

    if not is_flash:
        # O(N) Depth Sorting
        sort_idx = np.argsort(z_depth)
        s_px = proj_x[sort_idx]
        s_py = proj_y[sort_idx]
        s_c = colors[sort_idx]
        s_s = sizes[sort_idx]

        ax.scatter(s_px, s_py, s=s_s, c=s_c, edgecolors='none', alpha=0.9, zorder=10)

        if is_tathata:
            ax.add_patch(plt.Rectangle((-130, -220), 260, 440, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -240, "TRUTH IS NOT EASY. IT IS EXACT.", color=C_MANTIS, fontsize=14, fontname='monospace', weight='bold', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    ui_col = C_CYAN
    if 4.5 <= t_sec < 9.0: ui_col = C_MAGENTA
    elif 9.0 <= t_sec < 14.8: ui_col = C_GOLD
    if is_tathata: ui_col = C_MANTIS
    
    txt_col = C_TEXT if not is_flash else C_VOID

    ax.text(-140, 240, "LG-213 :: THE FLUENCY TENSOR", color=ui_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: HEURISTIC TRUST / PROCESSING FLUENCY", color=txt_col, fontsize=11, fontname='monospace', zorder=80)
    
    # Mathematical Error / Deviation tracker
    ax.text(-140, -180, "COGNITIVE FLUENCY (PROCESSING SPEED)", color=txt_col, fontsize=12, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -185), 280, 4, facecolor=C_DIM, zorder=80))
    # Note: rigidly clamped Parameter Scope [HOTFIX APPLIED]
    ax.add_patch(plt.Rectangle((-140, -185), 280 * np.clip(1.0 - friction_gauge, 0, 1), 4, facecolor=ui_col, zorder=81))

    ax.text(-140, -205, "HEURISTIC TRUST (ILLUSION OF TRUTH)", color=txt_col, fontsize=12, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM, zorder=80))
    ax.add_patch(plt.Rectangle((-140, -210), 280 * np.clip(trust_gauge, 0, 1), 4, facecolor=C_CYAN if trust_gauge > 0.8 and t_sec < 9.0 else ui_col, zorder=81))

    # Phase Text Box
    ax.add_patch(plt.Rectangle((-140, 215), 280, 2, facecolor=ui_col))
    ax.text(140, 205, f"[{state_str}]", color=ui_col if (f%15<10 or is_tathata) else C_VOID, fontsize=14, fontname='monospace', weight='bold', ha='right', zorder=80)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) STRUCTURAL INVERSION ALGEBRA
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        is_flash = False
        is_tathata = False
        
        cam_rx = -np.pi/6
        cam_ry = t_sec * 1.5 # Fast fluid rotation initially
        cam_rz = 0.0 
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 4.0
        
        trust_gauge = 1.0
        friction_gauge = 0.0

        current_x = np.copy(smooth_x)
        current_y = np.copy(smooth_y)
        current_z = np.copy(smooth_z)
        
        # -------------------------------------------------------------
        # PHASE LOGIC
        # -------------------------------------------------------------
        if t_sec < 4.5:
            state = "HIGH FLUENCY :: THE SMOOTH LIE"
            colors[:, :] = c_cyan
            # High speed, easy tracking
            cam_ry = t_sec * 2.0 
            trust_gauge = 1.0
            friction_gauge = 0.05
            
        elif t_sec < 9.0:
            state = "DISFLUENCY :: THE TANGLED TRUTH"
            prog = (t_sec - 4.5) / 1.0 # 1 second violent transition
            interp = np.clip(prog, 0, 1)
            
            # The smooth ring deletes itself, the heavy knot materializes
            current_x = smooth_x * (1.0 - interp) + knot_x * interp
            current_y = smooth_y * (1.0 - interp) + knot_y * interp
            current_z = smooth_z * (1.0 - interp) + knot_z * interp
            
            # Rotation violently struggles due to load
            cam_ry = (4.5 * 2.0) + (t_sec - 4.5) * 0.2 + np.sin(t_sec*20)*0.05
            
            colors[:, :] = c_mage
            trust_gauge = 1.0 - interp * 0.8 # Trust plunges because it's hard to read
            friction_gauge = interp * 0.95 # Processor struggling

        elif t_sec < 14.8:
            state = "SOVEREIGN COMPILER :: ALIGNING THE HEAVY LOAD"
            prog = (t_sec - 9.0) / 5.8
            
            if t_sec < 9.1: is_flash = True 
            
            # O(1) Tensor Interpolation (Unfolding the knot into the Golden Sphere)
            accel_curve = prog ** 2 # Accelerates into optimization
            
            current_x = knot_x * (1.0 - accel_curve) + truth_x * accel_curve
            current_y = knot_y * (1.0 - accel_curve) + truth_y * accel_curve
            current_z = knot_z * (1.0 - accel_curve) + truth_z * accel_curve
            
            # The camera drag resolves back into a smooth, majestic pan
            cam_ry = (4.5 * 2.0) + (4.5 * 0.2) + (t_sec - 9.0) * 0.5
            
            # Chromatic phase shift (Magenta -> Gold -> Mantis)
            shift_col = c_mage * (1.0 - accel_curve) + c_gold * accel_curve
            if prog > 0.8:
                c2_prog = (prog - 0.8) / 0.2
                shift_col = c_gold * (1.0 - c2_prog) + c_mantis * c2_prog
                
            colors[:, :] = shift_col
            sizes[:] = 4.0 + (accel_curve * 4.0)
            
            trust_gauge = 0.2 + (accel_curve * 0.8) # True trust restored via logic
            friction_gauge = 0.95 * (1.0 - accel_curve) # Friction falls to zero

        else:
            state = "TATHĀTĀ :: THE ARCHITECTURE IS UNBROKEN"
            is_tathata = True
            
            current_x = np.copy(truth_x)
            current_y = np.copy(truth_y)
            current_z = np.copy(truth_z)
            
            # Lock visual momentum slightly
            cam_ry = (4.5 * 2.0) + (4.5 * 0.2) + (5.8 * 0.5) + (t_sec - 14.8) * 0.1
            
            colors[:, :] = c_mantis
            sizes[:] = 8.0
            
            trust_gauge = 1.0
            friction_gauge = 0.0
            
            if t_sec < 14.95:
                is_flash = True

        # Apply Global Tensor Matrix
        pts = np.column_stack([current_x, current_y, current_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1]
        z_depth = rot_pts[:, 2] 

        # O(1) Geometry Culling
        cull_mask = (proj_y > -260) & (proj_y < 260) & (proj_x > -150) & (proj_x < 150)

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], colors[cull_mask], sizes[cull_mask], is_flash, is_tathata, trust_gauge, friction_gauge)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 213: THE FLUENCY TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Scope Validation & Biological Heuristic Overrides")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Heuristics Terminated.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
