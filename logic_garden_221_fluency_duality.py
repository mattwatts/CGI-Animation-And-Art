"""
SOVEREIGN CODE: logic_garden_221_fluency_duality.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Cognitive Architecture (17.5 seconds)
SCENE: Logic Garden 221 (Delusion vs Tathata / The Fluency Dualism)
HOTFIX: O(1) Dimensional Clamping, Array Over-Allocation & Truncation (np.ceil)
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
OUT_DIR = "frames_221_fluency_duality"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'
C_CYAN      = '#00FFFF'        # Delusion / Semantic Hallucination
C_MAGENTA   = '#FF0055'        # The Broken Glass / Thermal Strain
C_GOLD      = '#FFD700'        # Kinetic Crash / The Hardware Ping
C_MANTIS    = '#00FF00'        # Tathātā / Sovereign Bounding Box

# -------- STRUCTURAL TOPOLOGY (THE HOTFIX) --------
MAX_PARTICLES = 25000
# Force a 159x159 grid (25281), which will be strictly truncated to exactly 25000
GRID_RES = int(np.ceil(np.sqrt(MAX_PARTICLES))) 

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_void = np.array(hex_to_rgba(C_VOID)[:3])
c_text = np.array(hex_to_rgba(C_TEXT)[:3])
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

# ------------------------------------------------------------------
# BASE GEOMETRY ARRAYS: THE RUIN AND THE HALO
# ------------------------------------------------------------------
np.random.seed(808)

# The Axiom of Broken Glass: A jagged, computationally expensive terrain
gv = np.linspace(-120, 120, GRID_RES)
X, Y = np.meshgrid(gv, gv)

# Truncate exact vectors to map mathematically with MAX_PARTICLES
px_base = X.flatten()[:MAX_PARTICLES]
py_base = Y.flatten()[:MAX_PARTICLES]

# Chaotic, high-entropy mathematical ruin (The Red Stream)
pz_ruin = 15.0 * np.sin(px_base*0.2) + 20.0 * np.cos(py_base*0.15) + np.random.normal(0, 12, MAX_PARTICLES)

# The Delusion Shortcut: A perfectly smooth, hovered graphical illusion
phi = np.arccos(1 - 2 * np.random.rand(MAX_PARTICLES))
theta = 2 * np.pi * np.random.rand(MAX_PARTICLES)
orb_r = 75.0
px_orb = orb_r * np.sin(phi) * np.cos(theta)
py_orb = orb_r * np.sin(phi) * np.sin(theta)
pz_orb = orb_r * np.cos(phi) + 60.0 # Hovering completely detached from the physics floor

# The Bounding Box Mask: The exact localized perimeter to clamp (The Green Stream)
box_mask = (np.abs(px_base) < 45) & (np.abs(py_base) < 45)
dim_mask = ~box_mask

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, proj_x, proj_y, z_depth, colors, sizes, therm_res, is_flash, is_tathata = packet
    
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

        ax.scatter(s_px, s_py, s=s_s, color=s_c, edgecolors='none', alpha=0.9, zorder=10)

        if is_tathata:
            # The localized green stream wireframe overlaid precisely on the broken reality
            ax.add_patch(plt.Rectangle((-65, -60), 130, 200, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -80, "TATHĀTĀ: LOCALIZED COMPRESSION", color=C_MANTIS, fontsize=11, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, -95, "PHYSICS ALIGNED. VARIABLES CLAMPED TO ZERO.", color=C_DIM, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    ui_col = C_MAGENTA if t_sec < 4.0 else (C_CYAN if t_sec < 9.0 else C_GOLD)
    if t_sec >= 12.0: ui_col = C_MANTIS
    
    txt_col = C_TEXT if not is_flash else C_VOID

    ax.text(-140, 240, "LG-221 :: THE FLUENCY DUALITY", color=ui_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: DELUSIONAL SHORTCUT VS ZEN COMPUTATION", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    
    method_str = "O(N) MASSIVE STRAIN"
    if 4.0 <= t_sec < 9.0: method_str = "O(1) SHORTCUT :: DELETION"
    elif 9.0 <= t_sec < 12.0: method_str = "SYSTEM CRASH :: ZERO-DAY EXPLOIT"
    elif t_sec >= 12.0: method_str = "O(1) SHORTCUT :: COMPRESSION"

    c_meth = C_MAGENTA if t_sec < 4.0 else (C_CYAN if t_sec < 9.0 else C_GOLD)
    if is_tathata: c_meth = C_MANTIS

    ax.text(-140, -180, f"COMPUTATIONAL METHOD : {method_str}", color=c_meth, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Thermodynamic Hardware Response
    ax.text(-140, -205, "THERMODYNAMIC RESPONSE TO 'HARD DATA' PING", color=txt_col, fontsize=11, fontname='monospace', zorder=80)
    
    ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM, zorder=80))
    bar_w = 280 * np.clip(therm_res, 0, 1)
    # The bar turns intensely Magenta when dealing with delusion/strain, dropping to zero at Zen
    ax.add_patch(plt.Rectangle((-140, -210), bar_w, 4, facecolor=c_meth, zorder=81))

    # Phase Text Box [PROTOCOL HOTFIX :: Scope Clamping executed]
    ax.add_patch(plt.Rectangle((-140, 215), 280, 2, facecolor=ui_col, zorder=80))
    ax.text(140, 205, f"[{state_str}]", color=ui_col if (f%15<10 or is_tathata) else C_VOID, fontsize=14, fontname='monospace', weight='bold', ha='right', zorder=80)

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
        
        cam_rx = -np.pi/4
        cam_ry = 0.0
        cam_rz = t_sec * 0.2
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 4.0
        
        curr_x = np.copy(px_base)
        curr_y = np.copy(py_base)
        curr_z = np.copy(pz_ruin)

        therm_res = 1.0

        # -------------------------------------------------------------
        # PHASE LOGIC
        # -------------------------------------------------------------
        if t_sec < 4.0:
            state = "THE BROKEN GRAPH :: BIOLOGICAL FRICTION"
            
            # Violent structural load on the system
            curr_z += np.sin(curr_x * 0.1 + t_sec * 10) * 5.0
            colors[:, :] = c_mage
            therm_res = 0.8 + 0.2 * np.sin(t_sec * 15)

        elif t_sec < 9.0:
            state = "THE SMOOTH UI :: SEMANTIC HALLUCINATION"
            prog = (t_sec - 4.0) / 5.0
            
            # The system achieves fake fluency by lifting into a smooth, ignorant shape
            accel = prog ** 3
            
            curr_x = px_base * (1.0 - accel) + px_orb * accel
            curr_y = py_base * (1.0 - accel) + py_orb * accel
            curr_z = pz_ruin * (1.0 - accel) + pz_orb * accel
            
            colors[:, :] = c_mage * (1.0 - accel) + c_cyan * accel
            
            # Fluency feels absolutely great (Low friction indicator)
            therm_res = 0.8 * (1.0 - accel)

        elif t_sec < 12.0:
            state = "THE HARDWARE PING :: PHYSICS INTERSECTION"
            prog = (t_sec - 9.0) / 3.0
            if t_sec < 9.1: is_flash = True
            
            # The orb violently shatters because the hard data (reality) pings it
            # It crashes back into the jagged matrix
            fall = prog ** 4
            
            # Kinematic Spallation tracking
            curr_x = px_orb * (1.0 - fall) + px_base * fall + np.random.normal(0, 10, MAX_PARTICLES) * (1.0-fall)
            curr_y = py_orb * (1.0 - fall) + py_base * fall + np.random.normal(0, 10, MAX_PARTICLES) * (1.0-fall)
            curr_z = pz_orb * (1.0 - fall) + pz_ruin * fall
            
            # Extreme thermal heat generated by cognitive dissonance
            colors[:, :] = c_gold * (1.0 - fall) + c_mage * fall
            sizes[:] = 5.0 + (1.0 - fall) * 10.0
            
            cam_rx -= np.sin(t_sec*20)*0.05 # Camera violent shake
            
            therm_res = 1.0 # Maximum thermal strain/anger

        elif t_sec < 14.8:
            state = "OPERATIONS RESEARCH :: COMPILING TATHĀTĀ"
            prog = (t_sec - 12.0) / 2.8
            
            # The system remains in the ruin. It does not hover.
            # Instead, it strictly isolates the variables within its localized control.
            
            curr_z = pz_ruin # We stay in reality
            
            # The Bounding Box illuminates
            colors[dim_mask] = c_mage * (1.0 - prog) + c_dim * prog
            sizes[dim_mask] = 4.0 * (1.0 - prog) + 2.0 * prog
            
            colors[box_mask] = c_mage * (1.0 - prog) + c_mantis * prog
            sizes[box_mask] = 4.0 + (prog * 4.0)
            
            # The heat totally bleeds out of the system as physics align
            therm_res = 1.0 - prog

        else:
            state = "TATHĀTĀ :: COMMUTATIVITY ESTABLISHED"
            is_tathata = True
            
            curr_z = pz_ruin
            
            colors[dim_mask] = c_dim
            sizes[dim_mask] = 2.0
            
            colors[box_mask] = c_mantis
            sizes[box_mask] = 8.0
            
            therm_res = 0.0 # Absolute zero processing strain
            
            if t_sec < 14.95:
                is_flash = True

        # Apply Global Tensor Matrix
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1]
        z_depth = rot_pts[:, 2] 

        # O(1) Geometry Culling
        cull_mask = (proj_y > -260) & (proj_y < 260) & (proj_x > -150) & (proj_x < 150)

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], colors[cull_mask], sizes[cull_mask], therm_res, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 221: THE FLUENCY DUALITY [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: O(1) Array Rectification & Compile-Time Safety")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Matrix Topology Locked.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
