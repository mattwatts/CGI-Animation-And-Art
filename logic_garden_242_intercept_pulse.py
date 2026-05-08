"""
SOVEREIGN CODE: logic_garden_242_intercept_pulse.py
SYSTEM: Python Multicore / O(1) Kinetic Topography
SCENE: Logic Garden 242 (The Intercept Pulse / C-RAM Logic)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Dimensional Array Pre-allocation / Euclidean Delta Calculation

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
OUT_DIR = "frames_242_intercept_pulse"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS DEFAULT) --------
C_BG        = '#FFFFFF'        # Absolute Void / Pure Canvas
C_TEXT      = '#020205'        # Telemetry / High Contrast Tracking
C_DIM       = '#D0D0D5'        # Radar Tracking Grid
C_THREAT    = '#FF0055'        # The Threat Vector (Hostile Arc)
C_SHIELD    = '#00BFFF'        # The Kinetic Kill Vehicle (Cyan Interceptor)
C_GOLD      = '#FFB300'        # Kinetic Spallation / Intercept Pop
C_MANTIS    = '#00C800'        # Tathata Base / Threat Erased

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_dim     = np.array(hex_to_rgba(C_DIM)[:3])
c_threat  = np.array(hex_to_rgba(C_THREAT)[:3])
c_shield  = np.array(hex_to_rgba(C_SHIELD)[:3])
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
# BASE GEOMETRY ARRAYS: STATIC PRE-ALLOCATION
# ------------------------------------------------------------------
np.random.seed(242)

# 1. The Tracking Grid (Floor / Radar Geometry)
N_GRID = 5000
gx = np.random.uniform(-150, 150, N_GRID) # X wide
gy = np.zeros(N_GRID) - 100.0             # Floor at Y = -100
gz = np.random.uniform(-150, 150, N_GRID) # Z depth

# 2. The Intercept Sparks (The Kinetic Pop)
N_SPARKS = 22000
sx = np.zeros(N_SPARKS)
sy = np.zeros(N_SPARKS)
sz = np.zeros(N_SPARKS)
# Spherical explosive expansion vectors
theta_s = np.random.uniform(0, 2*np.pi, N_SPARKS)
phi_s = np.arccos(np.random.uniform(-1, 1, N_SPARKS))
vel_s = np.random.uniform(20.0, 150.0, N_SPARKS)
svx = vel_s * np.sin(phi_s) * np.cos(theta_s)
svy = vel_s * np.sin(phi_s) * np.sin(theta_s)
svz = vel_s * np.cos(phi_s)

# 3. Dynamic Vector Trails 
N_TRAIL = 1500
tx_trail = np.zeros(N_TRAIL)
ty_trail = np.zeros(N_TRAIL)
tz_trail = np.zeros(N_TRAIL)

sx_trail = np.zeros(N_TRAIL)
sy_trail = np.zeros(N_TRAIL)
sz_trail = np.zeros(N_TRAIL)

# Merge Arrays for absolute dimension locking
base_px = np.concatenate([gx, sx, tx_trail, sx_trail])
base_py = np.concatenate([gy, sy, ty_trail, sy_trail])
base_pz = np.concatenate([gz, sz, tz_trail, sz_trail])

MAX_PARTICLES = len(base_px) # 30,000 exact lock

idx_grid_end = N_GRID
idx_spark_end = idx_grid_end + N_SPARKS
idx_tt_end = idx_spark_end + N_TRAIL

mask_grid = np.arange(MAX_PARTICLES) < idx_grid_end
mask_spark = (np.arange(MAX_PARTICLES) >= idx_grid_end) & (np.arange(MAX_PARTICLES) < idx_spark_end)
mask_ttrail = (np.arange(MAX_PARTICLES) >= idx_spark_end) & (np.arange(MAX_PARTICLES) < idx_tt_end)
mask_strail = np.arange(MAX_PARTICLES) >= idx_tt_end

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, proj_x, proj_y, z_depth, colors, sizes, closing_delta, is_flash, is_tathata = packet
    
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
        # Radar Baseplane
        ax.plot([-140, 140], [-100, -100], color=C_DIM, lw=1.5, alpha=0.5, zorder=1)

        # Depth Sorting for flawless 3D transparency
        sort_idx = np.argsort(z_depth)
        s_px = proj_x[sort_idx]
        s_py = proj_y[sort_idx]
        s_c = colors[sort_idx]
        s_s = sizes[sort_idx]

        ax.scatter(s_px, s_py, s=s_s, color=s_c, edgecolors='none', alpha=0.85, zorder=10)

        if is_tathata:
            ax.add_patch(plt.Rectangle((-140, -50), 280, 120, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -20, "TATHĀTĀ: THE INTERCEPT IS THE ONLY TRUTH", color=C_MANTIS, fontsize=10, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 40, "[TRAJECTORY ERASED / MUTUAL ANNIHILATION]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_THREAT if t_sec < 4.5 else (C_SHIELD if t_sec < 11.5 else C_GOLD)
    if is_tathata: ui_col = C_MANTIS
    
    ax.text(-140, 240, "LG-242 :: THE INTERCEPT PULSE", color=txt_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: O(1) KINEMATIC KILL / C-RAM TOPOLOGY", color=txt_col, fontsize=8, fontname='monospace', zorder=80)
    
    obj_str = "THREAT ACQUISITION [BALLISTIC ARC]"
    if 4.5 <= t_sec < 11.5: obj_str = "PROPORTIONAL NAVIGATION [INTERCEPT VECTOR]"
    elif 11.5 <= t_sec < 14.8: obj_str = "TOTAL ENERGY SPALLATION [ZERO DISTANCE]"
    elif is_tathata: obj_str = "ABSOLUTE RESOLUTION [TATHĀTĀ]"

    ax.text(-140, -180, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Delta (Distance to Intercept)
    ax.text(-140, -205, f"Δ (DELTA TO INTERCEPT): {max(0.0, closing_delta):.2f}m", color=txt_col, fontsize=10, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    bar_w = 280 * np.clip(closing_delta / 250.0, 0, 1) # Normalizing delta scale
    ax.add_patch(plt.Rectangle((-140, -210), bar_w, 4, facecolor=ui_col, zorder=81))

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
    # Kinematic Setup
    t_intercept = 11.5
    
    # Target Intercept Coordinate (Zero-Dimensional Point)
    Int_X, Int_Y, Int_Z = 0.0, 0.0, 0.0
    
    # Threat Starts at t=0
    Th_X0, Th_Y0, Th_Z0 = 120.0, 180.0, -80.0
    # Parabolic calculation to hit [0,0,0] at t=11.5. Uses gravity.
    T_Vx = (Int_X - Th_X0) / t_intercept
    T_Vz = (Int_Z - Th_Z0) / t_intercept
    g = 9.81
    T_Vy = ((Int_Y - Th_Y0) / t_intercept) + (0.5 * g * t_intercept)

    # Shield Starts at t=3.0
    Sh_t_start = 3.0
    Sh_X0, Sh_Y0, Sh_Z0 = -90.0, -90.0, 60.0
    flight_time = t_intercept - Sh_t_start
    S_Vx = (Int_X - Sh_X0) / flight_time
    S_Vy = (Int_Y - Sh_Y0) / flight_time
    S_Vz = (Int_Z - Sh_Z0) / flight_time

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        is_flash = False
        is_tathata = False
        
        # Subtle, high-tension camera pan
        cam_rx = np.pi/8 - (t_sec * 0.005)
        cam_ry = t_sec * 0.08 
        cam_rz = 0.0
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.zeros(MAX_PARTICLES)
        
        curr_x = np.copy(base_px)
        curr_y = np.copy(base_py)
        curr_z = np.copy(base_pz)

        closing_delta = 250.0

        # Radar Grid is always faintly active
        colors[mask_grid] = c_dim
        # Radar sweeping pulse effect
        pulse = np.sin(curr_x[mask_grid] * 0.1 - t_sec * 5.0)
        sizes[mask_grid] = 1.0 + (pulse * 1.5)

        # -------------------------------------------------------------
        # KINEMATIC VECTOR PHASES
        # -------------------------------------------------------------
        
        # Calculate Current Threat Pos
        cur_Tx = Th_X0 + T_Vx * t_sec
        cur_Ty = Th_Y0 + T_Vy * t_sec - 0.5 * g * (t_sec**2)
        cur_Tz = Th_Z0 + T_Vz * t_sec

        # Calculate Current Shield Pos
        if t_sec > Sh_t_start:
            s_t = t_sec - Sh_t_start
            cur_Sx = Sh_X0 + S_Vx * s_t
            cur_Sy = Sh_Y0 + S_Vy * s_t
            cur_Sz = Sh_Z0 + S_Vz * s_t
        else:
            cur_Sx, cur_Sy, cur_Sz = Sh_X0, Sh_Y0, Sh_Z0

        if t_sec < t_intercept:
            # Active Flight Phase
            closing_delta = np.sqrt((cur_Tx - cur_Sx)**2 + (cur_Ty - cur_Sy)**2 + (cur_Tz - cur_Sz)**2)
            if t_sec < Sh_t_start:
                closing_delta = 250.0 # Maintain full bar before launch
                
            # Render Threat Trail (Last N_TRAIL frames logic via modulo/random)
            # Create a localized swarm around the head to act as the thick trail
            curr_x[mask_ttrail] = cur_Tx - (T_Vx * np.random.uniform(0, 1.5, N_TRAIL)) + np.random.normal(0, 1.5, N_TRAIL)
            curr_y[mask_ttrail] = cur_Ty - (T_Vy * np.random.uniform(0, 1.5, N_TRAIL)) + np.random.normal(0, 1.5, N_TRAIL)
            curr_z[mask_ttrail] = cur_Tz - (T_Vz * np.random.uniform(0, 1.5, N_TRAIL)) + np.random.normal(0, 1.5, N_TRAIL)
            colors[mask_ttrail] = c_threat
            sizes[mask_ttrail] = 4.0
            
            # Render Shield Trail if launched
            if t_sec > Sh_t_start:
                curr_x[mask_strail] = cur_Sx - (S_Vx * np.random.uniform(0, 0.8, N_TRAIL)) + np.random.normal(0, 0.5, N_TRAIL)
                curr_y[mask_strail] = cur_Sy - (S_Vy * np.random.uniform(0, 0.8, N_TRAIL)) + np.random.normal(0, 0.5, N_TRAIL)
                curr_z[mask_strail] = cur_Sz - (S_Vz * np.random.uniform(0, 0.8, N_TRAIL)) + np.random.normal(0, 0.5, N_TRAIL)
                colors[mask_strail] = c_shield
                sizes[mask_strail] = 5.0

        elif t_sec < 14.8:
            # THE EXACT INTERCEPT (t_intercept = 11.5)
            pop_time = t_sec - t_intercept
            closing_delta = 0.00
            
            if pop_time < 0.1:
                is_flash = True

            # Vectors are erased instantly. Sparks ignite outward from the zero-point (Int_X, Y, Z = 0)
            curr_x[mask_spark] = Int_X + (svx * pop_time)
            curr_y[mask_spark] = Int_Y + (svy * pop_time) - (0.5 * g * (pop_time**2) * 5.0) # Ash falling
            curr_z[mask_spark] = Int_Z + (svz * pop_time)
            
            colors[mask_spark] = c_gold
            sizes[mask_spark] = max(0.0, 5.0 - (pop_time * 1.5)) # Burn out into vapor

        else:
            # TATHĀTĀ
            is_tathata = True
            closing_delta = 0.00
            
            # The explosion fades into nothing. Sky is entirely empty.
            sizes[mask_spark] = 0.0
            sizes[mask_ttrail] = 0.0
            sizes[mask_strail] = 0.0
            
            if t_sec < 14.95:
                is_flash = True

        # Phase strings for Telemetry
        if t_sec < 4.5: state = "PHASE 1 :: THREAT ACQUIRED"
        elif t_sec < 11.5: state = "PHASE 2 :: C-RAM INTERCEPT VECTOR"
        elif t_sec < 14.8: state = "PHASE 3 :: THE POP (MUTUAL ERASURE)"
        else: state = "TATHĀTĀ :: ZERO-DISTANCE TRUTH"

        # Apply Global Tensor Matrix
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1]
        z_depth = rot_pts[:, 2] 

        # O(N) Geometry Culling
        cull_mask = (proj_y > -260) & (proj_y < 260) & (proj_x > -160) & (proj_x < 160)

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], colors[cull_mask], sizes[cull_mask], closing_delta, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 242: THE INTERCEPT PULSE [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Euclidean Trajectories & Absolute Dimensional Override")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Threat Trajectory Mapped and Erased. Sky Clear.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
