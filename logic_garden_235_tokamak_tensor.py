"""
SOVEREIGN CODE: logic_garden_235_tokamak_tensor.py
SYSTEM: Python Multicore / O(1) Phase-Space Topology
SCENE: Logic Garden 235 (The Tokamak QUBO / Macro-Kinetic Torus)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Instantaneous Phase-Shift Mechanics & Substrate Fatigue Clamping

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
OUT_DIR = "frames_235_tokamak_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP ON ABSOLUTE VOID) --------
C_VOID      = '#020205'        # The Abyss / Heat Sink
C_TEXT      = '#22222A'        # Vibrating Magnetic Constraints (Penalty Walls)
C_DIM       = '#111116'        # Deep Structure
C_AZURE     = '#007FFF'        # Phase 1: Diffuse Peace (The Acoustic Deception)
C_XENON     = '#FFFFFF'        # Phase 2: Toroidal Ignition (Pure White-Hot Logic)
C_MAGENTA   = '#FF0055'        # Phase 3: High-Yield Fusion / Kinetic Violence
C_GOLD      = '#FFB300'        # Phase 3: Energy Spallation
C_MANTIS    = '#00FF00'        # Phase 4: Stabilized Baseline / Tathātā

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_void    = np.array(hex_to_rgba(C_VOID)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_dim     = np.array(hex_to_rgba(C_DIM)[:3])
c_azure   = np.array(hex_to_rgba(C_AZURE)[:3])
c_xenon   = np.array(hex_to_rgba(C_XENON)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
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
# BASE GEOMETRY ARRAYS: THE METASTABLE CLOUD VS TOKAMAK TORUS
# ------------------------------------------------------------------
np.random.seed(848) # Substrate Generation Lock

MAX_PARTICLES = 30000

# STATE A: The False Vacuum (Acoustic Deception)
# A wide, gently undulating, unconstrained spherical cloud
A_rad = np.random.uniform(0, 180, MAX_PARTICLES)
A_theta = np.random.uniform(0, 2*np.pi, MAX_PARTICLES)
A_phi = np.arccos(np.random.uniform(-1, 1, MAX_PARTICLES))

px_diff = A_rad * np.sin(A_phi) * np.cos(A_theta)
py_diff = A_rad * np.sin(A_phi) * np.sin(A_theta)
pz_diff = A_rad * np.cos(A_phi) * 0.4 # Slightly flattened logic board

# STATE B: The Toroidal QUBO Engine (Magnetic Confinement)
B_u = np.random.uniform(0, 2*np.pi, MAX_PARTICLES)
B_v = np.random.uniform(0, 2*np.pi, MAX_PARTICLES)

R_major = 90.0 # Strict Magnetic Boundary
r_minor = 35.0 # The variable confinement zone

px_torus = (R_major + r_minor * np.cos(B_v)) * np.cos(B_u)
py_torus = (R_major + r_minor * np.cos(B_v)) * np.sin(B_u)
pz_torus = r_minor * np.sin(B_v)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, proj_x, proj_y, z_depth, colors, sizes, thermal_yield, confinement_integ, is_flash, is_tathata = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = '#FFFFFF' if is_flash else C_VOID
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    ax.set_xlim(-160, 160)
    ax.set_ylim(-260, 260)

    if not is_flash:
        # Magnetic Containment Grid (Only visible during Pulse)
        if t_sec >= 4.0 and not is_tathata:
            circle_rads = [55, 125]
            for cr in circle_rads:
                # Vibrating magnetic boundary constraints (C_TEXT)
                vibe = np.random.normal(0, 1.5)
                ax.add_patch(plt.Circle((0, 0), cr + vibe, facecolor='none', edgecolor=C_TEXT, lw=2, alpha=0.9, zorder=1))

        # O(N) Depth Sorting
        sort_idx = np.argsort(z_depth)
        s_px = proj_x[sort_idx]
        s_py = proj_y[sort_idx]
        s_c = colors[sort_idx]
        s_s = sizes[sort_idx]

        ax.scatter(s_px, s_py, s=s_s, color=s_c, edgecolors='none', alpha=0.9, zorder=10)

        if is_tathata:
            ax.add_patch(plt.Rectangle((-130, -100), 260, 200, facecolor='none', edgecolor=C_MANTIS, lw=2, zorder=40))
            ax.text(0, -70, "TATHĀTĀ: THE SUBSTRATE FATIGUE LIMIT", color=C_MANTIS, fontsize=11, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 60, "[THERMAL CYCLING HALTED / BASEPLATE PROTECTED]", color=C_XENON, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_VOID if is_flash else C_XENON
    ui_col = C_AZURE if t_sec < 4.0 else (C_XENON if t_sec < 9.0 else C_MAGENTA)
    if is_tathata: ui_col = C_MANTIS
    
    ax.text(-140, 240, "LG-235 :: THE TOKAMAK QUBO TENSOR", color=txt_col, fontsize=18, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: MAGNETIC CONFINEMENT / HIGH-YIELD ALGORITHMICS", color=txt_col, fontsize=8, fontname='monospace', zorder=80)
    
    obj_str = "THE FALSE VACUUM [ACOUSTIC DECEPTION]"
    if 4.0 <= t_sec < 9.0: obj_str = "TOROIDAL IGNITION [THE PULSE ACTUATES]"
    elif 9.0 <= t_sec < 14.8: obj_str = "THERMAL FUSION [FIGHT FIRE WITH FIRE]"
    elif is_tathata: obj_str = "TERMINAL PULSE [SUBSTRATE INTEGRITY SAVED]"

    ax.text(-140, -180, f"OPERATIONAL PHASE: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Thermodynamic Hardware Metric 1: Plasma Yield
    ax.text(-140, -205, "TOKAMAK THERMAL YIELD", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 2, facecolor=C_TEXT, zorder=80))
    # Pulses wildly during ignition
    bar_w = 280 * np.clip(thermal_yield, 0, 1)
    ax.add_patch(plt.Rectangle((-140, -210), bar_w, 2, facecolor=C_MAGENTA if thermal_yield > 0.8 else ui_col, zorder=81))

    # Thermodynamic Hardware Metric 2: Confinement Integrity
    ax.text(-140, -225, "MAGNETIC CONTAINMENT VOID", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -230), 280, 2, facecolor=C_TEXT, zorder=80))
    con_w = 280 * np.clip(confinement_integ, 0, 1)
    ax.add_patch(plt.Rectangle((-140, -230), con_w, 2, facecolor=C_AZURE if confinement_integ > 0.5 else C_GOLD, zorder=81))

    # Phase Text Box
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
        
        # High RPM rotation parameters
        cam_rx = np.pi/6
        cam_ry = t_sec * 0.8  # Spinning at mathematically uncomfortable velocities
        cam_rz = t_sec * 0.1
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 4.0
        
        thermal_yield = 0.0
        confinement_integ = 1.0

        # -------------------------------------------------------------
        # PHASE LOGIC
        # -------------------------------------------------------------
        if t_sec < 4.0:
            state = "THE FALSE VACUUM :: UNCONSTRAINED SEARCH"
            
            # The algorithm acts peacefully. Slow wave motion.
            curr_x = px_diff
            curr_y = py_diff
            curr_z = pz_diff + 15.0 * np.sin(px_diff * 0.02 + t_sec)
            
            colors[:, :] = c_azure
            sizes[:] = 3.0 + np.abs(np.sin(t_sec * 2)) * 2.0
            
            thermal_yield = 0.05 
            confinement_integ = 1.0

        elif t_sec < 9.0:
            state = "IGNITION :: THE TOROIDAL STRIKE"
            if t_sec < 4.1: is_flash = True # The exact millisecond of the Riff
            prog = (t_sec - 4.0) / 5.0
            
            # Violent structural mapping. INSTANTANEOUS teleportation of metrics.
            # Variables are ripped from diffuse peace and slammed into C_XENON constraints.
            curr_x = px_torus
            curr_y = py_torus
            curr_z = pz_torus
            
            # Internal plasma velocity massively accelerates
            B_u_mod = B_u + t_sec * 10.0
            curr_x = (R_major + r_minor * np.cos(B_v)) * np.cos(B_u_mod)
            curr_y = (R_major + r_minor * np.cos(B_v)) * np.sin(B_u_mod)
            
            # Pure White-Hot Logic
            colors[:, :] = c_xenon
            sizes[:] = 5.0 + np.random.rand(MAX_PARTICLES)*3.0
            
            thermal_yield = 0.6 + (0.4 * np.abs(np.sin(t_sec * 25)))
            confinement_integ = 0.9 - (0.1 * np.random.rand())

        elif t_sec < 14.8:
            state = "HIGH-YIELD FUSION :: EXTREME KINETIC PENALTY"
            prog = (t_sec - 9.0) / 5.8
            
            # Fighting Fire With Fire. 
            # The Torus major/minor radius physically crushes inwards to force variable alignment.
            shrink_mod = 1.0 - (0.3 * prog) # Shrinks 30%
            mod_r_minor = r_minor * shrink_mod
            
            B_u_mod = B_u + t_sec * 25.0 # Relentlessly fast
            
            # High-G discrete quanta striking (fracturing the Z-axis internally)
            plasma_scatter = np.random.normal(0, 5.0 * prog, MAX_PARTICLES)
            
            curr_x = (R_major + mod_r_minor * np.cos(B_v)) * np.cos(B_u_mod)
            curr_y = (R_major + mod_r_minor * np.cos(B_v)) * np.sin(B_u_mod)
            curr_z = mod_r_minor * np.sin(B_v) + plasma_scatter
            
            # Heavy Magenta and Gold thermal friction overrides the Xenon
            heat_mask = np.random.rand(MAX_PARTICLES) < (0.3 + 0.5 * prog)
            gold_mask = np.random.rand(MAX_PARTICLES) < (0.1 * prog)
            
            colors[:, :] = c_xenon
            colors[heat_mask] = c_magenta
            colors[gold_mask] = c_gold
            
            sizes[:] = 5.0
            sizes[heat_mask] = 8.0
            
            thermal_yield = 0.95 + 0.05 * np.random.rand() # Redline limit
            # The Ragged Edge: Magnetic Containment Void is severely tested
            confinement_integ = max(0.1, 0.8 - (prog * 0.9) + 0.2 * np.abs(np.sin(t_sec * 30))) 

        else:
            state = "TATHĀTĀ :: THE TERMINAL PULSE"
            is_tathata = True
            
            # The Substrate Fatigue limit is reached. The pulse strictly offloads to protect the operator.
            curr_x = px_torus
            curr_y = py_torus
            curr_z = pz_torus
            
            colors[:, :] = c_mantis
            sizes[:] = 5.0
            
            thermal_yield = 0.0 
            confinement_integ = 1.0 # Containment vessel stabilized.
            
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

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], colors[cull_mask], sizes[cull_mask], thermal_yield, confinement_integ, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 235: TOKAMAK QUBO TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Toroidal Substrate Fatigue & Ignition Mechanics")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Substrate Saved. Thermal Engine Quarantined.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
