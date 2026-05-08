"""
SOVEREIGN CODE: logic_garden_249_fight_fire.py
SYSTEM: Python Multicore / O(1) Thermal Containment Topography
SCENE: Logic Garden 249 (The Termination Sequence / Reciprocal Erasure)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Explicit Float Broadcast Safety & O(N) Toroidal Spallation clamp

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
OUT_DIR = "frames_249_fight_fire"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS DEFAULT) --------
C_BG        = '#FFFFFF'        # Absolute Void / The Baseplate
C_TEXT      = '#020205'        # Magnetic Penalty Walls / Containment
C_AZURE     = '#007FFF'        # Acoustic Deception (Smooth Hallucination)
C_GOLD      = '#FFB300'        # Kinetic Spallation / Heat-Sink Bloom
C_MAGENTA   = '#FF0055'        # Thermal Output / Reciprocal Violence
C_MANTIS    = '#00C800'        # Tathata / O(1) Reciprocal Lock
C_DIM       = '#D0D0D5'        # Structural Geometry

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_azure   = np.array(hex_to_rgba(C_AZURE)[:3])
c_gold    = np.array(hex_to_rgba(C_GOLD)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_mantis  = np.array(hex_to_rgba(C_MANTIS)[:3])
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
np.random.seed(1983) 

MAX_PARTICLES = 28000

# INITIAL STATE: Acoustic Deception (Gentle Azure Cloud)
px_cloud = np.random.uniform(-180, 180, MAX_PARTICLES)
py_cloud = np.random.uniform(-20, 20, MAX_PARTICLES)
pz_cloud = np.random.uniform(-180, 180, MAX_PARTICLES)

# TARGET STATE: Toroidal Containment (Tokamak)
R_major = 90.0
r_minor = 35.0
theta_t = np.random.uniform(0, 2 * np.pi, MAX_PARTICLES)
phi_t = np.random.uniform(0, 2 * np.pi, MAX_PARTICLES)

# Give the torus some surface depth (structured placement)
surface_noise = np.random.normal(0, 2.0, MAX_PARTICLES)
r_actual = r_minor + surface_noise

px_torus = (R_major + r_actual * np.cos(phi_t)) * np.cos(theta_t)
py_torus = r_actual * np.sin(phi_t)
pz_torus = (R_major + r_actual * np.cos(phi_t)) * np.sin(theta_t)

# Calculate displacement vectors for thermal spallation
# Vectors point radially outward from the minor axis core
norm_x = r_actual * np.cos(phi_t) * np.cos(theta_t)
norm_y = r_actual * np.sin(phi_t)
norm_z = r_actual * np.cos(phi_t) * np.sin(theta_t)

# Vector normalization
norms = np.sqrt(norm_x**2 + norm_y**2 + norm_z**2) + 0.0001
dx_spall = norm_x / norms
dy_spall = norm_y / norms
dz_spall = norm_z / norms

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, p_x, p_y, p_z, c_arr, s_arr, fatigue, is_flash, is_tathata = packet
    
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
        # Background Grid (Baseplate mapping)
        if t_sec > 7.0:
            for g_line in np.linspace(-150, 150, 7):
                ax.plot([-130, 130], [g_line, g_line], color=C_DIM, lw=1.0, alpha=0.3, zorder=1)
                ax.plot([g_line, g_line], [-130, 130], color=C_DIM, lw=1.0, alpha=0.3, zorder=1)

        # Depth Sorting for smooth 3D intersection
        sort_idx = np.argsort(p_z)
        s_x = p_x[sort_idx]
        s_y = p_y[sort_idx]
        s_c = c_arr[sort_idx]
        s_size = s_arr[sort_idx]

        ax.scatter(s_x, s_y, s=s_size, color=s_c, edgecolors='none', alpha=0.85, zorder=10)

        # Tathata Phase-Lock UI
        if is_tathata:
            ax.add_patch(plt.Rectangle((-130, -50), 260, 100, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -30, "TATHĀTĀ: THREAT NEUTRALIZED", color=C_MANTIS, fontsize=11, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 30, "[TERMINAL EQUILIBRIUM FORCED / O(1) LOCK]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_AZURE if t_sec < 7.0 else (C_TEXT if t_sec < 11.0 else C_MAGENTA)
    if is_tathata: ui_col = C_MANTIS
    
    ax.text(-140, 240, "LG-249 :: THE TERMINATION SEQUENCE", color=txt_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: RECIPROCAL ERASURE / THERMAL TOKAMAK", color=txt_col, fontsize=8, fontname='monospace', zorder=80)
    
    obj_str = "ACOUSTIC DECEPTION [SMOOTH HALLUCINATION]"
    if 7.0 <= t_sec < 11.0: obj_str = "TOROIDAL IGNITION [MAGNETIC CLAMP]"
    elif 11.0 <= t_sec < 14.8: obj_str = "KINETIC VIOLENCE [FIGHT FIRE WITH FIRE]"
    elif is_tathata: obj_str = "STABLE BASEPLATE [RECIPROCAL LOCK]"

    ax.text(-140, -180, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Thermodynamic Hardware Metric: Substrate Fatigue 
    ax.text(-140, -205, "SUBSTRATE FATIGUE [TRANSLATION TAX DEBT]", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    bar_w = 280 * np.clip(fatigue, 0, 1)
    ax.add_patch(plt.Rectangle((-140, -210), bar_w, 4, facecolor=C_MAGENTA if fatigue >= 0.95 and not is_tathata else ui_col, zorder=81))

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
        
        cam_rx = np.pi/6 - (t_sec * 0.003)
        cam_ry = t_sec * 0.4
        cam_rz = 0.0
        
        c_arr = np.zeros((MAX_PARTICLES, 3))
        s_arr = np.ones(MAX_PARTICLES)
        
        curr_x = np.zeros(MAX_PARTICLES)
        curr_y = np.zeros(MAX_PARTICLES)
        curr_z = np.zeros(MAX_PARTICLES)

        fatigue = 0.0

        # -------------------------------------------------------------
        # THE TERMINATION KINEMATICS
        # -------------------------------------------------------------
        
        if t_sec < 7.0:
            # PHASE 1: ACOUSTIC DECEPTION 
            state = "PHASE 1 :: METASTABLE FALSE VACUUM"
            
            # Gentle, deceptive wave motion
            wave = 15.0 * np.sin(px_cloud * 0.05 + t_sec * 2.0) + 15.0 * np.cos(pz_cloud * 0.05 + t_sec * 1.5)
            
            curr_x = px_cloud
            curr_y = py_cloud + wave
            curr_z = pz_cloud
            
            c_arr[:] = c_azure
            s_arr[:] = 2.0 + np.sin(t_sec * 5 + px_cloud) * 1.5
            
            fatigue = 0.1 # Low baseline tax
            
            if t_sec > 6.8:
                is_flash = True if f % 4 < 2 else False

        elif t_sec < 11.0:
            # PHASE 2: TOROIDAL IGNITION (The 0:40 Riff Hardware Interrupt)
            state = "PHASE 2 :: MAGNETIC PENALTY WALLS"
            prog = (t_sec - 7.0) / 4.0
            ease = prog ** 3 # Violent topological snap
            
            # Interpolating from cloud to strict Torus representation
            curr_x = px_cloud * (1 - ease) + px_torus * ease
            curr_y = (py_cloud + 15.0 * np.sin(px_cloud * 0.05)) * (1 - ease) + py_torus * ease
            curr_z = pz_cloud * (1 - ease) + pz_torus * ease
            
            c_interp = c_azure * (1 - ease) + c_text * ease
            c_arr[:] = c_interp
            s_arr[:] = 2.0 + (1.5 * ease)
            
            fatigue = 0.1 + (0.5 * prog) # Rapid accumulation of heat
            
            if t_sec < 7.2:
                is_flash = True

        elif t_sec < 14.8:
            # PHASE 3: KINETIC VIOLENCE (Substrate Fusion)
            state = "PHASE 3 :: DISCRETE QUANTA SPALLATION"
            prog = (t_sec - 11.0) / 3.8
            
            # Massive structural spallation to meet hostile thermal variable
            # "Enjoyment of the Burn" pushes the vectors outwards in explosive bursts
            burst = np.abs(np.sin(t_sec * 40.0)) * (20.0 * prog)
            
            curr_x = px_torus + dx_spall * burst
            curr_y = py_torus + dy_spall * burst
            curr_z = pz_torus + dz_spall * burst
            
            # Color segregation based on displacement severity
            c_arr[:] = c_text
            spall_mask = burst > 5.0
            core_mask = burst > 12.0
            
            c_arr[spall_mask] = c_gold
            c_arr[core_mask] = c_magenta
            
            s_arr[:] = 3.5
            s_arr[spall_mask] = 5.0
            s_arr[core_mask] = 7.0
            
            fatigue = 0.6 + (0.4 * prog) # Baseplate taking extreme structural damage

        else:
            # PHASE 4: TATHĀTĀ (Reciprocal Erasure)
            state = "TATHĀTĀ :: HOSTILE TOPOLOGY NEUTRALIZED"
            is_tathata = True
            
            curr_x = px_torus 
            curr_y = py_torus 
            curr_z = pz_torus 
            
            c_arr[:] = c_mantis
            s_arr[:] = 3.5
            
            fatigue = 1.0 # The cost was paid globally.
            
            if t_sec < 14.95:
                is_flash = True # One final thermal shock before silence

        # Apply Global Tensor Matrix
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz) // 1.0 # Force discrete lock
        
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1]
        z_depth = rot_pts[:, 2] 

        # O(N) Geometry Culling
        cull_mask = (proj_y > -260) & (proj_y < 260) & (proj_x > -160) & (proj_x < 160)

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], c_arr[cull_mask], s_arr[cull_mask], fatigue, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 249: THE TERMINATION SEQUENCE [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Toroidal Substrate Collapse & Substrate Fatigue Matrix")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Threat Level Matched. Erasure Absolute.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
