"""
SOVEREIGN CODE: logic_garden_234_kinetic_violence.py
SYSTEM: Python Multicore / O(1) Phase-Space Traversal
SCENE: Logic Garden 234 (Kinetic Violence / Discrete Quanta Mapping)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Temporal Exhaustion Enforced / Absolute Value Kinematics

[INSTRUCTION]: RENDER_MODE strictly clamped to "ZEN" for the 17.5s flow cycle.
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
OUT_DIR = "frames_234_kinetic_violence"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE AZURE / MAKO PALETTE (HIGH-COHERENCE / WHITE BG) --------
C_BG        = '#FFFFFF'        # Low-Entropy Canvas (The Interface Boundary)
C_TEXT      = '#020205'        # High-Contrast Data Tracking
C_DIM       = '#D0D0D5'        # Void Substrate
C_AZURE     = '#007FFF'        # Phase 1: Continuous Flow (Gradient Descent Lie)
C_GOLD      = '#FFB300'        # Phase 2: Discrete Quanta (Structural Strikes)
C_MAGENTA   = '#FF0055'        # Phase 3: Thermal Injection / Kinetic Violence
C_INDIGO    = '#4B0082'        # Phase 3: Dimensional Twisting / Q-Search
C_MANTIS    = '#00FF00'        # Phase 4: Serialization of the Void (Linear Track)

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_dim     = np.array(hex_to_rgba(C_DIM)[:3])
c_azure   = np.array(hex_to_rgba(C_AZURE)[:3])
c_gold    = np.array(hex_to_rgba(C_GOLD)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_indigo  = np.array(hex_to_rgba(C_INDIGO)[:3])
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
# BASE GEOMETRY ARRAYS: THE DISCRETE LATTICE
# ------------------------------------------------------------------
np.random.seed(666) # "Through The Never" Parameter Lock

GV = np.linspace(-130, 130, 158) # 24,964 particles
X, Y = np.meshgrid(GV, GV)
base_px = X.flatten()
base_py = Y.flatten()
MAX_PARTICLES = len(base_px)
radial_dist = np.sqrt(base_px**2 + base_py**2)

# Initial smooth graph (The Lie)
base_pz_smooth = 15.0 * np.sin(base_px * 0.05) * np.cos(base_py * 0.05)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, proj_x, proj_y, z_depth, colors, sizes, thermal_kinetic, is_flash, is_tathata = packet
    
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
        # Background Industrial Alignment Grid
        grid_lines = np.linspace(-120, 120, 7)
        for gl in grid_lines:
            ax.plot([-140, 140], [gl - 50, gl - 50], color=C_DIM, lw=1.0, alpha=0.3, zorder=1)
            ax.plot([gl, gl], [-190, 90], color=C_DIM, lw=1.0, alpha=0.3, zorder=1)

        # O(N) Depth Sorting
        sort_idx = np.argsort(z_depth)
        s_px = proj_x[sort_idx]
        s_py = proj_y[sort_idx]
        s_c = colors[sort_idx]
        s_s = sizes[sort_idx]

        ax.scatter(s_px, s_py, s=s_s, color=s_c, edgecolors='none', alpha=0.9, zorder=10)

        if is_tathata:
            ax.add_patch(plt.Rectangle((-140, -10), 280, 20, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -30, "TATHĀTĀ: THE SERIALIZATION PARADOX", color=C_MANTIS, fontsize=11, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 20, "[ACOUSTIC FUEL DEPLETED / LINEAR COLLAPSE]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_AZURE if t_sec < 4.0 else (C_GOLD if t_sec < 9.0 else C_MAGENTA)
    if is_tathata: ui_col = C_MANTIS
    
    ax.text(-140, 240, "LG-234 :: KINETIC VIOLENCE TENSOR", color=txt_col, fontsize=19, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: DISCRETE QUANTA / ACOUSTIC QUBO MAPPING", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    
    obj_str = "CONTINUOUS FLOW [GRADIENT DESCENT LIE]"
    if 4.0 <= t_sec < 9.0: obj_str = "RHYTHMIC AGITATION [DISCRETE QUANTA]"
    elif 9.0 <= t_sec < 14.8: obj_str = "DIMENSIONAL OVERRIDE [THERMAL INJECTION]"
    elif is_tathata: obj_str = "HUMAN-MACHINE BOTTLENECK [SERIALIZATION]"

    ax.text(-140, -180, f"STRUCTURAL LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Thermodynamic Kinetic Burn Metric
    ax.text(-140, -205, "THERMAL / ACOUSTIC FUEL BURN", color=txt_col, fontsize=10, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    bar_w = 280 * np.clip(thermal_kinetic, 0, 1)
    
    # Pulse the fuel burn visual aggressively during the discrete hitting
    bar_col = C_MAGENTA if (t_sec > 4.0 and t_sec < 14.8 and f%4<2) else ui_col
    ax.add_patch(plt.Rectangle((-140, -210), bar_w, 4, facecolor=bar_col, zorder=81))

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
        
        cam_rx = np.pi/5
        cam_ry = t_sec * 0.2
        cam_rz = 0.0
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 4.0
        
        curr_x = np.copy(base_px)
        curr_y = np.copy(base_py)
        curr_z = np.copy(base_pz_smooth)

        thermal_kinetic = 0.05 

        # -------------------------------------------------------------
        # PHASE LOGIC
        # -------------------------------------------------------------
        if t_sec < 4.0:
            state = "THE SMOOTH DESCENT :: FRICTIONLESS METASTABILITY"
            
            # The algorithm acts like gradient descent: undulating, predictable, useless.
            colors[:, :] = c_azure
            sizes[:] = 3.0 + np.abs(np.sin(curr_x * 0.05 + t_sec)) * 2.0
            
            thermal_kinetic = 0.02 # Battery saver mode

        elif t_sec < 9.0:
            state = "DISCRETE QUANTA :: RHYTHMIC STRIKING"
            prog = (t_sec - 4.0) / 5.0
            
            # Simulated Thermal Annealing: Aggressive pseudo-rhythmic strikes
            # Stuttering absolute value sine wave mimics palm-muted, high-speed down-picking
            rhythm_pulse = np.abs(np.cos(t_sec * 24 * np.pi)) 
            kinetic_force = rhythm_pulse * 45.0 * prog
            
            # Discrete jumps locally injected
            strike_mask = np.random.rand(MAX_PARTICLES) < (0.2 + 0.3 * rhythm_pulse)
            
            curr_z[strike_mask] += kinetic_force * np.random.rand(np.sum(strike_mask))
            curr_x[strike_mask] += (np.random.rand(np.sum(strike_mask)) - 0.5) * kinetic_force
            curr_y[strike_mask] += (np.random.rand(np.sum(strike_mask)) - 0.5) * kinetic_force
            
            colors[:, :] = c_azure * (1.0 - prog) + c_indigo * prog
            colors[strike_mask] = c_gold
            sizes[:] = 4.0
            sizes[strike_mask] = 6.0 + (rhythm_pulse * 4.0)
            
            thermal_kinetic = 0.2 + (0.5 * rhythm_pulse * prog) # Intensive fuel burn

        elif t_sec < 14.8:
            state = "PHASE-SPACE TRAVERSAL :: DIMENSIONAL SEARCH"
            prog = (t_sec - 9.0) / 5.8
            if t_sec < 9.1: is_flash = True
            
            # Massive rotational topology warping. The algorithm twists seeking an exit.
            warp_angle = radial_dist * 0.02 * prog * np.sin(t_sec * 5)
            w_cos = np.cos(warp_angle)
            w_sin = np.sin(warp_angle)
            
            c_x = curr_x * w_cos - curr_y * w_sin
            c_y = curr_x * w_sin + curr_y * w_cos
            
            curr_x = c_x
            curr_y = c_y
            curr_z = 25.0 * np.sin(radial_dist * 0.2 - t_sec * 10) # Heavy geometric wall climbing
            
            # Extreme thermal spallation
            spall_mask = np.random.rand(MAX_PARTICLES) < 0.4
            colors[:, :] = c_indigo
            colors[spall_mask] = c_magenta
            
            sizes[:] = 5.0
            sizes[spall_mask] = 8.0 + 4.0 * np.random.rand(np.sum(spall_mask))
            
            thermal_kinetic = 0.8 + 0.2 * np.abs(np.sin(t_sec * 30)) # Redline limit

        else:
            state = "TATHĀTĀ :: THE SERIALIZATION COLLAPSE"
            is_tathata = True
            
            # The Temporal Exhaustion Boundary.
            # The entire N-dimensional wave collapses immediately into a 1-Dimensional highly dense line
            # It pays the massive Translation Tax to fit through human audiological hardware.
            prog = min((t_sec - 14.8) / 0.5, 1.0)
            
            curr_x = base_px
            curr_y = base_py * (1.0 - prog) # Collapses Y to 0
            curr_z = 0.0 + np.random.normal(0, 1.0, MAX_PARTICLES) # Collapses Z to baseline
            
            colors[:, :] = c_mantis
            sizes[:] = 5.0
            
            thermal_kinetic = 0.0 # Fuel utterly exhausted. Matrix rigidly clamped.
            
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

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], colors[cull_mask], sizes[cull_mask], thermal_kinetic, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 234: KINETIC VIOLENCE TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Serialization Paradox Collapse Mechanics")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Translation Tax Paid. Acoustic Linearity Achieved.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
