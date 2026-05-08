"""
SOVEREIGN CODE: logic_garden_212_epistemic_tensor.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Epistemic Tensor (17.5 seconds)
SCENE: Logic Garden 212 (Dual-Vector Reality / Phenomenological Insight)
HOTFIX: Parameter Scope Alignment & Compile-Time GUI Safety
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
OUT_DIR = "frames_212_epistemic"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'
C_CYAN      = '#00FFFF'        # Cognitive Ease / Smooth Hallucination
C_MAGENTA   = '#FF0055'        # High-Entropy Friction / The Broken Graph
C_GOLD      = '#FFD700'        # Maxwell's Demon / Active Solver
C_MANTIS    = '#00FF00'        # Epistemic Certainty / True Terminal Flow

# O(1) Absolute Geometry Lock
MAX_PARTICLES = 25000
GRID_RES = int(np.ceil(np.sqrt(MAX_PARTICLES))) # 159x159

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_void = np.array(hex_to_rgba(C_VOID)[:3])
c_cyan = np.array(hex_to_rgba(C_CYAN)[:3])
c_mage = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_gold = np.array(hex_to_rgba(C_GOLD)[:3])
c_mantis = np.array(hex_to_rgba(C_MANTIS)[:3])
c_dim = np.array(hex_to_rgba(C_DIM)[:3])

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

# Target Terminal Truth (The Chladni Resonance Pattern)
gx = np.linspace(-100, 100, GRID_RES)
gy = np.linspace(-100, 100, GRID_RES)
X, Y = np.meshgrid(gx, gy)
px_base = X.flatten()[:MAX_PARTICLES]
py_base = Y.flatten()[:MAX_PARTICLES]

# Terminal Z-State: A perfect mathematical interference wave
R_base = np.sqrt(px_base**2 + py_base**2)
pz_target = 40.0 * np.sin(R_base * 0.1) * np.cos(px_base * 0.05)

# High-Entropy Initial State (The Broken Graph)
np.random.seed(33)
noise_x = px_base + np.random.uniform(-5, 5, MAX_PARTICLES)
noise_y = py_base + np.random.uniform(-5, 5, MAX_PARTICLES)
noise_z = np.random.uniform(-60, 60, MAX_PARTICLES)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, proj_x, proj_y, z_depth, colors, sizes, is_flash, is_tathata, error_rate = packet
    
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

        ax.scatter(s_px, s_py, s=s_s, c=s_c, edgecolors='none', alpha=0.85, zorder=10)

        if is_tathata:
            ax.add_patch(plt.Rectangle((-130, -220), 260, 440, facecolor='none', edgecolor=C_MANTIS, lw=3, linestyle='--', zorder=40))
            ax.text(0, -240, "TRUTH IS INEVITABLE. FRICTION RESOLVED.", color=C_MANTIS, fontsize=14, fontname='monospace', weight='bold', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    ui_col = C_CYAN
    if t_sec < 4.0: ui_col = C_MAGENTA
    elif t_sec < 8.0: ui_col = C_CYAN
    elif t_sec < 14.8: ui_col = C_GOLD
    if is_tathata: ui_col = C_MANTIS
    
    txt_col = C_TEXT if not is_flash else C_VOID

    ax.text(-140, 240, "LG-212 :: THE EPISTEMIC TENSOR", color=ui_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: DUAL-VECTOR REALITY / HINDSIGHT BIAS", color=txt_col, fontsize=11, fontname='monospace', zorder=80)
    
    # Dual-Vector Telemetry
    vec1_stat = "DOMINANT (RAW ENTROPY)" if t_sec < 8.0 else ("SHATTERED" if t_sec < 14.8 else "DELETED")
    vec2_stat = "OFFLINE" if t_sec < 4.0 else ("HALLUCINATING (COGNITIVE EASE)" if t_sec < 8.0 else ("COMPILING O(1) GEOMETRY" if t_sec < 14.8 else "ABSOLUTE LOCK"))
    col_1 = C_MAGENTA if t_sec < 8.0 else C_DIM
    col_2 = C_CYAN if (4.0 <= t_sec < 8.0) else (C_GOLD if 8.0 <= t_sec < 14.8 else C_MANTIS)
    if t_sec < 4.0: col_2 = C_DIM
    
    ax.text(-140, -180, f"VULNERABILITY VECTOR : {vec1_stat}", color=col_1, fontsize=12, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, -200, f"MASTERY VECTOR       : {vec2_stat}", color=col_2, fontsize=12, fontname='monospace', weight='bold', zorder=80)

    # Mathematical Error / Deviation tracker
    ax.text(-140, -220, "SYSTEM DEVIATION FROM TRUE STATE", color=txt_col, fontsize=12, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -225), 280, 4, facecolor=C_DIM, zorder=80))
    bar_w = 280 * np.clip(error_rate, 0, 1)
    ax.add_patch(plt.Rectangle((-140, -225), bar_w, 4, facecolor=C_MAGENTA if error_rate > 0.05 else C_MANTIS, zorder=81))

    # Phase Text Box [PROTOCOL :: PARAMETER SCOPE REPAIR APPLIED]
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
        
        cam_rx = -np.pi/4
        cam_ry = 0.0
        cam_rz = t_sec * 0.1 
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 4.0
        error_rate = 1.0

        current_x = np.copy(noise_x)
        current_y = np.copy(noise_y)
        current_z = np.copy(noise_z)
        
        # -------------------------------------------------------------
        # PHASE LOGIC
        # -------------------------------------------------------------
        if t_sec < 4.0:
            state = "THE BROKEN GRAPH :: RAW ENTROPY"
            colors[:, :] = c_mage
            error_rate = 1.0 + np.sin(t_sec*10)*0.05
            
            # Subtle vibration of raw noise
            current_z += np.sin(current_x + t_sec*10) * 2.0

        elif t_sec < 8.0:
            state = "COGNITIVE EASE :: SYSTEMIC HALLUCINATION"
            prog = (t_sec - 4.0) / 4.0
            
            # The Artisan Brain hallucinates a rigid, perfectly smooth curve OVER the noise.
            # But the underlying points are merely dragged halfway up, ignoring reality.
            smooth_z = np.sin(noise_x * 0.02) * 20.0
            
            interp_factor = np.clip(prog * 2.0, 0, 1) # Snap to hallucination
            current_z = noise_z * (1.0 - interp_factor) + smooth_z * interp_factor
            
            # Color maps to Cyan, masking the underlying mathematical discrepancy
            colors[:, :] = (1.0 - interp_factor)*c_mage + (interp_factor)*c_cyan
            # High error rate remains, despite the appearance of smoothness
            error_rate = 0.8 

            # Reveal the biological lie: Flash magenta to show it's structurally unstable
            if f % 30 > 25: 
                colors[:, :] = c_mage

        elif t_sec < 14.8:
            state = "INSIGHT PROTOCOL :: STRUCTURAL ALIGNMENT"
            prog = (t_sec - 8.0) / 6.8
            
            if t_sec < 8.1: is_flash = True # Shatter the hallucination
            
            # We solve the physics via nonlinear interpolation toward the Chladni ideal
            accel_curve = prog ** 3 # Slow start, accelerating violently into perfection
            
            current_x = noise_x * (1.0 - accel_curve) + px_base * accel_curve
            current_y = noise_y * (1.0 - accel_curve) + py_base * accel_curve
            
            # Starts from the hallucinated smooth_z and rips apart into the true pz_target
            smooth_z = np.sin(noise_x * 0.02) * 20.0
            current_z = smooth_z * (1.0 - accel_curve) + pz_target * accel_curve
            
            # Complex spatial coloring mapping the alignment
            dist_to_truth = np.abs(current_z - pz_target)
            norm_dist = np.clip(dist_to_truth / 30.0, 0, 1)[:, None]
            
            colors = norm_dist * c_gold + (1.0 - norm_dist) * c_mantis
            sizes = 4.0 + (1.0 - norm_dist.flatten()) * 4.0 # Focus on aligned nodes
            
            error_rate = 0.8 * (1.0 - accel_curve)

        else:
            state = "TATHĀTĀ :: TRUTH IS UNSURPRISING"
            is_tathata = True
            
            current_x = np.copy(px_base)
            current_y = np.copy(py_base)
            current_z = np.copy(pz_target)
            
            colors[:, :] = c_mantis
            sizes[:] = 6.0
            error_rate = 0.0
            
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

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], colors[cull_mask], sizes[cull_mask], is_flash, is_tathata, error_rate)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 212: THE EPISTEMIC TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Parameter Scope Alignment & Compile-Time GUI Safety")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Syntax is flawless.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
