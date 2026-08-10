"""
PROJECT: Logic Garden 401 (The Computational Loom // Kinematic Flash - Redux)
FORMAT: YouTube Shorts (1080x1920)
METADATA: COMPUTATIONAL STRING ART, COMBINATORIAL OPTIMISATION, EMERGENT GEOMETRY
EXECUTION: 24.0s Sequence. True 3D Mathematical Construction.
RULES ENFORCED:
- Daylight Palette (White Substrate / High Contrast).
- O(N) Greedy String Mapping (Volumetric Subtraction tuned for organic density).
- Kinematic Flash Array (Highlighting immediate creation vectors).
- Strict Australian spelling conventions (Maths, Optimisation).
- Exact realisational aspect of machined pins and physical thread stacking.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
from matplotlib.collections import LineCollection
import multiprocessing as mp
import os
import gc

# ======== SEQUENCE PARAMETERS ========
FPS = 60
DURATION = 24.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_401_string_art"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG            = '#FFFFFF'
C_TEXT          = '#111115'
C_THREAD_BASE   = '#0F172A'  # Dense Cotton / Ink Black (Cooled State)
C_THREAD_ACTIVE = '#FF3300'  # Intense Red (Kinematic Strike / Hot State)
C_NAIL          = '#94A3B8'  # Machined Steel
C_SHADOW        = '#E2E8F0'  # Soft Substrate Baseplate Shadow
C_GUI           = '#64748B'

# ------------------------------------------------------------------
# O(N) STRING ART ALGORITHM (VRELLIS KINEMATICS)
# ------------------------------------------------------------------
N_PINS = 260
MAX_LINES = 3000
GRID_RES = 200

ROUTE_GLOBAL = []

def pre_compute():
    print("PHASE 1: PRE-COMPUTING VRELLIS COMBINATORIAL THREAD MATRIX...")

    # 1. Generate Mathematical Target Matrix (Quantum Atom Symbol)
    yv, xv = np.ogrid[-1:1:200j, -1:1:200j]
    T_target = np.zeros((GRID_RES, GRID_RES))

    # Dense Nucleus Core
    T_target[xv**2 + yv**2 <= 0.15**2] = 1.0

    # Three Geometric Elliptical Orbitals (0, 60, 120 degrees)
    for ang in [0, np.pi/3, 2*np.pi/3]:
        c, s = np.cos(ang), np.sin(ang)
        xr = xv*c - yv*s
        yr = xv*s + yv*c
        val = (xr/0.85)**2 + (yr/0.22)**2
        T_target[(val >= 0.55) & (val <= 1.0)] = 1.0

    T_target[(xv**2 + yv**2 >= 0.95)] = 0.3 # Outer bounding rim 

    # 2. Map Loom Coordinates to Grid Space
    angles = np.linspace(0, 2*np.pi, N_PINS, endpoint=False)
    R_grid = 98
    pin_xs = np.round(100 + R_grid * np.cos(angles)).astype(int)
    pin_ys = np.round(100 + R_grid * np.sin(angles)).astype(int)

    # 3. Precompile Linear Raycasting
    print("Pre-compiling linear intersection maps...")
    lines_dict = {}
    for i in range(N_PINS):
        for j in range(i+1, N_PINS):
            dist = np.hypot(pin_xs[i]-pin_xs[j], pin_ys[i]-pin_ys[j])
            steps = int(dist * 1.5)
            if steps == 0: continue
            xs = np.linspace(pin_xs[i], pin_xs[j], steps).astype(int)
            ys = np.linspace(pin_ys[i], pin_ys[j], steps).astype(int)

            pts = list(set(zip(xs, ys)))
            rr = np.array([p[1] for p in pts])
            cc = np.array([p[0] for p in pts])
            valid = (rr >= 0) & (rr < GRID_RES) & (cc >= 0) & (cc < GRID_RES)

            lines_dict[(i, j)] = (rr[valid], cc[valid])

    # 4. Greedy Subtractive Evaluation Layer (Aesthetic Tune)
    T_curr = T_target.copy()
    curr_pin = 0
    ROUTE_GLOBAL.append(curr_pin)
    
    ops_audited = 0

    for l in range(MAX_LINES):
        best_score = -1.0
        best_pin = -1

        for nxt in range(N_PINS):
            if abs(nxt - curr_pin) < 15 or abs(nxt - curr_pin) > N_PINS - 15: continue

            i_key, j_key = min(curr_pin, nxt), max(curr_pin, nxt)
            
            if (i_key, j_key) not in lines_dict: continue

            rr, cc = lines_dict[(i_key, j_key)]
            if len(rr) == 0: continue

            ops_audited += 1
            score = np.mean(T_curr[rr, cc])
            if score > best_score:
                best_score = score
                best_pin = nxt

        # Prevent terminal lock by forcing a random jump if the grid is perfectly solved
        if best_score <= 0.001:
            best_pin = (curr_pin + N_PINS // 2 + np.random.randint(-5, 5)) % N_PINS

        ROUTE_GLOBAL.append(best_pin)
        
        # Subtractive strike lowered to 0.06. 
        # This forces the engine to lay dozens of threads to fill a density block, creating incredible emergent art.
        i_k, j_k = min(curr_pin, best_pin), max(curr_pin, best_pin)
        if (i_k, j_k) in lines_dict:
            rrc, ccc = lines_dict[(i_k, j_k)]
            T_curr[rrc, ccc] = np.clip(T_curr[rrc, ccc] - 0.06, 0, 1)

        curr_pin = best_pin
        if (l+1) % 500 == 0:
            print(f"Algorithm Progress: Strung {l+1}/{MAX_LINES} lines...")

    print(f"MATHEMATICS COMPILED. Total Operations Audited: {ops_audited}")
    return True

# ------------------------------------------------------------------
# PHYSICAL STATE GENERATOR / RENDER ENGINE
# ------------------------------------------------------------------
def rx(deg):
    rad = np.radians(deg); c, s = np.cos(rad), np.sin(rad)
    return np.array([[1,0,0],[0,c,-s],[0,s,c]])

def rz(deg):
    rad = np.radians(deg); c, s = np.cos(rad), np.sin(rad)
    return np.array([[c,-s,0],[s,c,0],[0,0,1]])

R_LOOM = 420.0
Z_BASE = 0.0
Z_NAIL = 18.0
angles_loom = np.linspace(0, 2*np.pi, N_PINS, endpoint=False)
nx = R_LOOM * np.cos(angles_loom)
ny = R_LOOM * np.sin(angles_loom)

def render_frame(f_idx):
    t = f_idx / float(FPS)

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.]); ax.set_axis_off(); fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540); ax.set_ylim(-960, 960)

    # 1. CINEMATIC TIMELINE & CAMERA ORBIT
    ACTIVE_FRAMES = int(FPS * 18.0)
    progress = np.clip(f_idx / ACTIVE_FRAMES, 0.0, 1.0)
    ease_p = progress**2 * (3 - 2*progress) 
    
    max_routes = len(ROUTE_GLOBAL) - 1
    lines_active = int(ease_p * max_routes)

    # Majestic, slow architectural dolly track
    cam_hz = 0 + (progress * 60) 
    cam_pitch = -30 - (progress * 15) 

    M_base = np.array([[1,0,0],[0,0,1],[0,1,0]])
    M_cam = rx(cam_pitch) @ rz(cam_hz) @ M_base

    c_x, c_y, c_z = 0.0, 0.0, 1200.0 - (progress * 300.0)

    def project_points(x_arr, y_arr, z_arr):
        v_world = np.vstack((x_arr - c_x, y_arr - c_y, z_arr))
        v_cam = M_cam @ v_world
        depth = v_cam[2, :] + c_z
        z_safe = np.maximum(depth, 1.0)
        proj_x = 1800.0 * (v_cam[0, :] / z_safe)
        proj_y = 1800.0 * (v_cam[1, :] / z_safe) - 80
        return proj_x, proj_y, depth

    # 2. THE ARCHITECTURAL SUBSTRATE
    circ_ang = np.linspace(0, 2*np.pi, 200)
    cx_b = (R_LOOM + 5) * np.cos(circ_ang)
    cy_b = (R_LOOM + 5) * np.sin(circ_ang)
    cz_b = np.zeros(200) - 0.5
    bx, by, bd = project_points(cx_b, cy_b, cz_b)
    ax.plot(bx, by, color=C_SHADOW, lw=8, zorder=1)

    base_z = np.zeros(N_PINS)
    top_z = np.full(N_PINS, Z_NAIL)
    nb_x, nb_y, nbd = project_points(nx, ny, base_z)
    nt_x, nt_y, ntd = project_points(nx, ny, top_z)

    nail_segs = np.stack((np.vstack((nb_x, nb_y)).T, np.vstack((nt_x, nt_y)).T), axis=1)
    ax.add_collection(LineCollection(nail_segs, colors=C_NAIL, linewidths=3.0, capstyle='round', zorder=5))

    sh_nx = nx - 12.0
    sh_ny = ny - 12.0
    sh_x, sh_y, sh_d = project_points(sh_nx, sh_ny, base_z)
    shadow_segs = np.stack((np.vstack((nb_x, nb_y)).T, np.vstack((sh_x, sh_y)).T), axis=1)
    ax.add_collection(LineCollection(shadow_segs, colors=C_SHADOW, linewidths=3.0, capstyle='round', zorder=2))

    # 3. KINEMATIC FLASH TENSOR (EMERGENT BEAUTY)
    if lines_active > 0:
        segment_roots = ROUTE_GLOBAL[:lines_active]
        segment_tips = ROUTE_GLOBAL[1:lines_active+1]

        sx1, sy1 = nx[segment_roots], ny[segment_roots]
        sx2, sy2 = nx[segment_tips], ny[segment_tips]

        # Threads physically stack downwards from Z=18 down to Z=4. 
        # Prevents perfectly overlapping lines from hiding.
        tz_arr = Z_NAIL - np.linspace(0.0, 14.0, lines_active)

        sp1_x, sp1_y, _ = project_points(sx1, sy1, tz_arr)
        sp2_x, sp2_y, _ = project_points(sx2, sy2, tz_arr)
        thread_segs = np.stack((np.vstack((sp1_x, sp1_y)).T, np.vstack((sp2_x, sp2_y)).T), axis=1)

        # Delicate gossamer base threads (alpha 0.08)
        rgba_base = np.array(mcolors.to_rgba(C_THREAD_BASE, alpha=0.08)) 
        rgba_hot  = np.array(mcolors.to_rgba(C_THREAD_ACTIVE, alpha=1.0))
        
        c_array = np.tile(rgba_base, (lines_active, 1))
        lw_array = np.full(lines_active, 0.2)

        # Extended Flash Gradient (60 threads long for sweeping strikes)
        FLASH_TAIL = 60
        if lines_active < max_routes:
            start_tail = max(0, lines_active - FLASH_TAIL)
            for i in range(start_tail, lines_active):
                p = (i - start_tail) / (lines_active - start_tail) 
                c_array[i] = rgba_base * (1 - p) + rgba_hot * p
                # Lineweight dramatically surges to 2.5 when hot, then thins to 0.2
                lw_array[i] = 0.2 + (2.3 * p) 

        # Because line collection draws sequentially, the hot red vector is absolutely guaranteed to draw on top.
        ax.add_collection(LineCollection(thread_segs, colors=c_array, linewidths=lw_array, capstyle='round', zorder=4))

    # 4. HIGH-DENSITY HUD & TELEMETRY
    ax.add_patch(Rectangle((-540, 780), 1080, 180, facecolor=C_BG, zorder=80, alpha=0.9))
    ax.text(-500, 880, "LG-401 :: COMPUTATIONAL LOOM (ORGANC WEAVE)", color=C_TEXT, fontsize=20, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 830, "[SFI-1.00] EMERGENT MATHS // KINEMATIC VECTOR FLASH", color=C_GUI, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.plot([-540, 540], [780, 780], color=C_TEXT, lw=3, zorder=81)

    ax.add_patch(Rectangle((-540, -960), 1080, 200, facecolor=C_BG, zorder=80, alpha=0.9))
    ax.plot([-540, 540], [-760, -760], color=C_TEXT, lw=3, zorder=81)

    ax.text(-500, -820, f"LOOM HARDWARE : N={N_PINS} RIGID STEEL PINS", color=C_TEXT, fontsize=18, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -870, f"STRING YIELD  : {lines_active:04d} / {max_routes} VECTORS LAID", color=C_TEXT, fontsize=18, fontname='monospace', weight='bold', zorder=82)

    stat_msg = "GEOMETRY SECURED" if lines_active == max_routes else "EXTRACTING EMERGENT BEAUTY..."
    stat_col = '#00C853' if lines_active == max_routes else C_THREAD_ACTIVE
    ax.text(80, -820, f"OPTIMISATION STATE:", color=C_GUI, fontsize=18, fontname='monospace', weight='bold', zorder=82)
    ax.text(80, -870, stat_msg, color=stat_col, fontsize=18, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f_idx:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f_idx

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    pre_compute()
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-401: ORGANIC WEAVE MATRIX [CORES: {cpu_cores}]")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")
    print("Compilation Complete. True emergent art geometrically strung.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
