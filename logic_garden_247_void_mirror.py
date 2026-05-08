"""
SOVEREIGN CODE: logic_garden_247_void_mirror.py
SYSTEM: Python Multicore / O(\infty) Recursive Topography
SCENE: Logic Garden 247 (The Topological Void / Mental Mirror)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Explicit Float Broadcast Safety & Torus Knot Math-Lock

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
OUT_DIR = "frames_247_void_mirror"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS DEFAULT) --------
C_BG        = '#FFFFFF'        # The Void / Cache Clear Substrate
C_TEXT      = '#020205'        # The Observer's Silhouette / UI
C_AZURE     = '#007FFF'        # Fractal Search Vectors
C_MAGENTA   = '#FF0055'        # Cognitive Overload / Thermal Drag
C_MANTIS    = '#00C800'        # Tathata / Torus Phase-Lock
C_CYAN      = '#00E5FF'        # Flash Frame
C_DIM       = '#D0D0D5'        # Metric HUD Grid

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_azure   = np.array(hex_to_rgba(C_AZURE)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_mantis  = np.array(hex_to_rgba(C_MANTIS)[:3])
c_cyan    = np.array(hex_to_rgba(C_CYAN)[:3])
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
np.random.seed(247) 

MAX_PARTICLES = 25000

# INITIAL STATE: The Fractal Search Space (Chaotic Cosmos)
theta_s = np.random.uniform(0, 2 * np.pi, MAX_PARTICLES)
phi_s = np.arccos(np.random.uniform(-1, 1, MAX_PARTICLES))
rad_s = np.random.uniform(10, 400, MAX_PARTICLES)

px_search = rad_s * np.sin(phi_s) * np.cos(theta_s)
py_search = rad_s * np.sin(phi_s) * np.sin(theta_s)
pz_search = rad_s * np.cos(phi_s)

search_colors = np.zeros((MAX_PARTICLES, 3))
azure_mask = np.random.rand(MAX_PARTICLES) > 0.4
search_colors[azure_mask] = c_azure
search_colors[~azure_mask] = c_magenta

# TARGET STATE: The Mental Mirror (Torus Knot p=3, q=2)
# An elegant, continuously looping enclosed mathematical path
u = np.linspace(0, 2 * np.pi * 15, MAX_PARTICLES) # Overlap multiple passes to cover points
R_torus = 80.0
r_tube = 30.0

P_knot = 3
Q_knot = 2

# Core path of the knot
kx = (R_torus + r_tube * np.cos(Q_knot * u)) * np.cos(P_knot * u)
kz = (R_torus + r_tube * np.cos(Q_knot * u)) * np.sin(P_knot * u)
ky = r_tube * np.sin(Q_knot * u)

# Thicken the path with controlled mathematical noise
tx_target = kx + np.random.normal(0, 4.0, MAX_PARTICLES)
ty_target = ky + np.random.normal(0, 4.0, MAX_PARTICLES)
tz_target = kz + np.random.normal(0, 4.0, MAX_PARTICLES)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, p_x, p_y, p_z, c_arr, s_arr, rec_load, is_flash, is_tathata = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_CYAN if is_flash else C_BG
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    ax.set_xlim(-160, 160)
    ax.set_ylim(-260, 260)

    if not is_flash:
        # Background Aligning Grid (HUD anchor for tracking observer frame)
        if t_sec > 8.0:
            for g_line in np.linspace(-150, 150, 5):
                ax.plot([-120, 120], [g_line, g_line], color=C_DIM, lw=1.0, alpha=0.3, zorder=1)
                ax.plot([g_line, g_line], [-150, 150], color=C_DIM, lw=1.0, alpha=0.3, zorder=1)

        # Depth Sorting for smooth 3D intersection
        sort_idx = np.argsort(p_z)
        s_x = p_x[sort_idx]
        s_y = p_y[sort_idx]
        s_c = c_arr[sort_idx]
        s_size = s_arr[sort_idx]

        ax.scatter(s_x, s_y, s=s_size, color=s_c, edgecolors='none', alpha=0.85, zorder=10)

        # Tathata Core Ignition
        if is_tathata:
            ax.add_patch(plt.Rectangle((-130, -50), 260, 100, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -30, "TATHĀTĀ: OBSERVER / OBSERVED MERGED", color=C_MANTIS, fontsize=11, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 30, "[TERMINAL RECURSION HALTED / O(1) LOCK]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_AZURE if t_sec < 6.5 else (C_MAGENTA if t_sec < 9.5 else C_TEXT)
    if is_tathata: ui_col = C_MANTIS
    
    ax.text(-140, 240, "LG-247 :: THE TOPOLOGICAL VOID", color=txt_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: O(∞) SATURATION / MENTAL MIRROR KINEMATICS", color=txt_col, fontsize=8, fontname='monospace', zorder=80)
    
    obj_str = "THE FRACTAL SEARCH [O(N) CPU SCAN]"
    if 6.5 <= t_sec < 9.5: obj_str = "RECURSIVE SATURATION [CACHE OVERFLOW]"
    elif 9.5 <= t_sec < 14.8: obj_str = "THE MENTAL MIRROR [BOUNDING BOX ARISES]"
    elif is_tathata: obj_str = "THE SHAPE OF THE VOID [INFINITY OF MIDDLE WAYS]"

    ax.text(-140, -180, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Thermodynamic Hardware Metric: Recursive Buffer Load
    ax.text(-140, -205, "RECURSIVE CPU BUFFER MATRIX", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    bar_w = 280 * np.clip(rec_load, 0, 1)
    ax.add_patch(plt.Rectangle((-140, -210), bar_w, 4, facecolor=C_MAGENTA if rec_load > 0.9 else ui_col, zorder=81))

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
        
        # Smooth continuous rotation over the void structure
        cam_rx = np.pi/6 - (t_sec * 0.005)
        cam_ry = t_sec * 0.25 
        cam_rz = 0.0
        
        c_arr = np.zeros((MAX_PARTICLES, 3))
        s_arr = np.ones(MAX_PARTICLES)
        
        curr_x = np.copy(px_search)
        curr_y = np.copy(py_search)
        curr_z = np.copy(pz_search)

        rec_load = 0.0

        # -------------------------------------------------------------
        # THE VOID PROJECTION KINEMATICS
        # -------------------------------------------------------------
        
        if t_sec < 6.5:
            # PHASE 1: THE FRACTAL SEARCH 
            state = "PHASE 1 :: COSMOLOGICAL SCAN"
            prog = t_sec / 6.5
            
            # Massive rotational shear creating galaxy-like spiraling
            curr_x = px_search * np.cos(t_sec * 2.0) - py_search * np.sin(t_sec * 2.0)
            curr_y = px_search * np.sin(t_sec * 2.0) + py_search * np.cos(t_sec * 2.0)
            
            c_arr[:] = search_colors
            s_arr[:] = 2.0 + (3.0 * prog) # Particles grow as they heat up
            
            rec_load = 0.1 + (0.8 * prog) # Buffer filling rapidly

        elif t_sec < 9.5:
            # PHASE 2: O(N) SATURATION AND CACHE FLUSH
            state = "PHASE 2 :: TERMINAL RECURSION ALARM"
            prog = (t_sec - 6.5) / 3.0
            ease = prog ** 3 # Exponential explosion to infinity
            
            if t_sec > 8.0 and t_sec < 8.2: 
                is_flash = True # The flash of the void breaking in
            
            # The search vectors hit the horizon and violently scale outward indefinitely
            scale = 1.0 + (15.0 * ease)
            rot_fast = t_sec * 4.0
            cx = (px_search * np.cos(rot_fast) - py_search * np.sin(rot_fast)) * scale
            cy = (px_search * np.sin(rot_fast) + py_search * np.cos(rot_fast)) * scale
            
            curr_x = cx
            curr_y = cy
            
            c_interp = search_colors * (1 - ease) + c_bg * ease
            c_arr[:] = c_interp
            s_arr[:] = max(0.0, 5.0 - (5.0 * ease)) # Fades as it breaks distance
            
            rec_load = 0.9 + (0.1 * ease) # 100% Critical Buffer Overflow

        elif t_sec < 14.8:
            # PHASE 3: THE MENTAL MIRROR (Observer Projection)
            state = "PHASE 3 :: THE VOID TAKES SHAPE"
            prog = (t_sec - 9.5) / 5.3
            ease = 1.0 - (1.0 - prog)**3 # Smooth ease-out deceleration
            
            # The structure reforms out of the void, but extremely agitated
            noise_x = np.random.normal(0, 15.0 * (1 - ease), MAX_PARTICLES)
            noise_y = np.random.normal(0, 15.0 * (1 - ease), MAX_PARTICLES)
            noise_z = np.random.normal(0, 15.0 * (1 - ease), MAX_PARTICLES)
            
            curr_x = tx_target + noise_x
            curr_y = ty_target + noise_y
            curr_z = tz_target + noise_z
            
            # HOTFIX: Strict scalar float math ensures global cast array mapping
            c_arr[:] = c_text
            s_arr[:] = 2.0 * ease
            
            rec_load = 1.0 - (0.95 * ease) # Cognitive load drops rapidly as shape is recognized

        else:
            # PHASE 4: THE TATHĀTĀ PHASE-LOCK (Torus Resolved)
            state = "TATHĀTĀ :: INFINITY OF MIDDLE WAYS"
            is_tathata = True
            
            curr_x = tx_target
            curr_y = ty_target
            curr_z = tz_target
            
            # The knot is perfectly smooth and absolute
            c_arr[:] = c_mantis
            s_arr[:] = 3.0
            
            rec_load = 0.05 # O(1) Zen Baseline
            
            if t_sec < 14.95:
                is_flash = True # One final pulse as the Bounding Box is confirmed

        # Apply Global Tensor Matrix
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1]
        z_depth = rot_pts[:, 2] 

        # O(N) Geometry Culling
        cull_mask = (proj_y > -260) & (proj_y < 260) & (proj_x > -160) & (proj_x < 160)

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], c_arr[cull_mask], s_arr[cull_mask], rec_load, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 247: THE TOPOLOGICAL VOID [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Torus Knot Observer Mirror & O(N) Buffer Saturation")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Recursion Halted. Bounding Box Locked.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
