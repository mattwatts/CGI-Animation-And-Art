"""
SOVEREIGN CODE: logic_garden_233_false_vacuum.py
SYSTEM: Python Multicore / O(1) Quantum Landscape
SCENE: Logic Garden 233 (The False Vacuum / Bubble Nucleation)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Terminal Phase Shift Kinematics / Absolute Variable Mapping

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
OUT_DIR = "frames_233_false_vacuum"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP / C_VOID CORE) --------
C_VOID      = '#020205'        # Deep Space / Absolute Null
C_TEXT      = '#FFFFFF'        # Data Load / High Coherence
C_DIM       = '#111116'        # The Underlying Abyss
C_CYAN      = '#00FFFF'        # Phase 1: The False Vacuum (Metastable Trap)
C_GOLD      = '#FFD700'        # Phase 2: Quantum Tunneling Origin Point
C_MAGENTA   = '#FF0055'        # Phase 3: The Expanding Annihilation Radius
C_MANTIS    = '#00FF00'        # Phase 4: The True Vacuum (Absolute Floor)

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_void    = np.array(hex_to_rgba(C_VOID)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_dim     = np.array(hex_to_rgba(C_DIM)[:3])
c_cyan    = np.array(hex_to_rgba(C_CYAN)[:3])
c_gold    = np.array(hex_to_rgba(C_GOLD)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
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
# BASE GEOMETRY ARRAYS: THE METASTABLE & TRUE LANDSCAPES
# ------------------------------------------------------------------
np.random.seed(888)

# Calculate exactly 25,000 points across a uniform matrix
GV = np.linspace(-140, 140, 158) # 158^2 = 24,964
X, Y = np.meshgrid(GV, GV)
base_px = X.flatten()
base_py = Y.flatten()
MAX_PARTICLES = len(base_px)
base_r_dist = np.sqrt(base_px**2 + base_py**2)

# State 1: The False Vacuum
# A complex, visually beautiful trap hovering high on the Z-axis
base_pz_false = 45.0 + (base_px**2 + base_py**2)*0.0015 + 10.0 * np.cos(base_px * 0.08) * np.cos(base_py * 0.08)

# State 2: The True Vacuum
# The absolute thermodynamic sink. Utterly rigid array, devoid of structural variation.
base_pz_true = -65.0 + (base_px**2 + base_py**2)*0.0002 

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, proj_x, proj_y, z_depth, colors, sizes, vacuum_stability, is_flash, is_tathata = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_TEXT if is_flash else C_VOID
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    ax.set_xlim(-160, 160)
    ax.set_ylim(-260, 260)

    if not is_flash:
        # Background Grid structure
        ax.plot([-150, 150], [0, 0], color=C_DIM, lw=1.0, alpha=0.3, zorder=1)
        ax.plot([0, 0], [-250, 250], color=C_DIM, lw=1.0, alpha=0.3, zorder=1)

        # O(N) Depth Sorting
        sort_idx = np.argsort(z_depth)
        s_px = proj_x[sort_idx]
        s_py = proj_y[sort_idx]
        s_c = colors[sort_idx]
        s_s = sizes[sort_idx]

        ax.scatter(s_px, s_py, s=s_s, color=s_c, edgecolors='none', alpha=0.9, zorder=10)

        if is_tathata:
            ax.add_patch(plt.Rectangle((-100, -120), 200, 240, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -90, "TATHĀTĀ: TRUE VACUUM ACHIEVED", color=C_MANTIS, fontsize=11, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 70, "[FALSE UNIVERSE DISINTEGRATED]", color=C_DIM, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_VOID if is_flash else C_TEXT
    ui_col = C_CYAN if t_sec < 4.5 else (C_GOLD if t_sec < 9.0 else C_MAGENTA)
    if is_tathata: ui_col = C_MANTIS
    
    ax.text(-140, 240, "LG-233 :: THE FALSE VACUUM", color=ui_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: QUANTUM FIELD TUNNELING / BUBBLE NUCLEATION", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    
    obj_str = "THE METASTABLE TRAP [LOCALLY OPTIMAL]"
    if 4.5 <= t_sec < 9.0: obj_str = "QUANTUM TUNNELING [O(0) FRICTION SHIFT]"
    elif 9.0 <= t_sec < 14.8: obj_str = "BUBBLE NUCLEATION [ANNIHILATION RADIUS]"
    elif is_tathata: obj_str = "TERMINAL PHASE SHIFT [TRUE VACUUM]"

    ax.text(-140, -180, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Thermodynamic Hardware Metric: Stability
    ax.text(-140, -205, "VACUUM STABILITY QUOTIENT", color=txt_col, fontsize=10, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    bar_w = 280 * np.clip(vacuum_stability, 0, 1)
    ax.add_patch(plt.Rectangle((-140, -210), bar_w, 4, facecolor=C_CYAN if t_sec < 9.0 else C_MAGENTA, zorder=81))

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
        
        # Slow tilt to reveal the vast gap between False and True Vacuum
        cam_rx = np.pi/4 - (t_sec * 0.015)
        cam_ry = t_sec * 0.25
        cam_rz = 0.0
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 4.0
        
        curr_x = np.copy(base_px)
        curr_y = np.copy(base_py)
        curr_z = np.copy(base_pz_false)

        vacuum_stability = 1.0 

        # -------------------------------------------------------------
        # THE ANNIHILATION SCHEDULER
        # -------------------------------------------------------------
        if t_sec < 4.5:
            state = "PHASE 1: THE METASTABLE STATE"
            
            # The system sits comfortably in the False Vacuum
            colors[:, :] = c_cyan
            # Add a slight energetic pulse 
            sizes[:] = 2.0 + np.abs(np.sin(t_sec * 5 + base_px * 0.1)) * 3.0
            
            vacuum_stability = 1.0

        elif t_sec < 9.0:
            state = "PHASE 2: DIMENSIONAL QUANTUM TUNNELING"
            prog = (t_sec - 4.5) / 4.5
            
            colors[:, :] = c_cyan
            sizes[:] = 3.0
            
            # The singularity forms at the origin (0,0) as the system tunnels
            # We see a deep visual well forming directly above the True Vacuum
            tunnel_mask = base_r_dist < (20.0 * prog)
            colors[tunnel_mask] = c_gold
            curr_z[tunnel_mask] -= 15.0 * np.sin(prog * np.pi) 
            
            vacuum_stability = 1.0 - (prog * 0.2)

        elif t_sec < 14.8:
            state = "PHASE 3: BUBBLE NUCLEATION / SHOCKWAVE"
            prog = (t_sec - 9.0) / 5.8
            if t_sec < 9.1: is_flash = True
            
            # The Annihilation Radius explodes outward from (0,0)
            # The False Vacuum is mathematically erased inside this radius
            blast_radius = prog * 250.0 
            
            survived_mask = base_r_dist > blast_radius
            annihilated_mask = ~survived_mask
            
            # Shockwave Ridge: A violent, destructive wall moving outward
            shock_mask = (base_r_dist < blast_radius + 8.0) & (base_r_dist > blast_radius - 8.0)
            
            # Apply False Vacuum physics to those who survived
            colors[survived_mask] = c_cyan
            curr_z[survived_mask] = base_pz_false[survived_mask]
            
            # Apply True Vacuum physics to those inside the bubble
            curr_z[annihilated_mask] = base_pz_true[annihilated_mask] + np.random.normal(0, 1.0, np.sum(annihilated_mask))
            colors[annihilated_mask] = c_mantis
            sizes[annihilated_mask] = 6.0
            
            # The Shockwave eats the geometry
            colors[shock_mask] = c_magenta
            curr_z[shock_mask] += np.random.normal(0, 25.0, np.sum(shock_mask)) # Violent Spallation
            sizes[shock_mask] = 12.0
            
            vacuum_stability = max(0.0, 0.8 - (prog * 1.5))

        else:
            state = "TATHĀTĀ :: THE TERMINAL PHASE SHIFT"
            is_tathata = True
            
            # The entire landscape has been collapsed into the True Vacuum
            curr_x = base_px
            curr_y = base_py
            curr_z = base_pz_true
            
            colors[:, :] = c_mantis
            sizes[:] = 7.0
            
            vacuum_stability = 0.0 # Bounding box locked. The old universe is gone.
            
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

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], colors[cull_mask], sizes[cull_mask], vacuum_stability, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 233: THE FALSE VACUUM TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: True Vacuum Annihilation Mechanics")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. False Universe Destroyed. True Vacuum Achieved.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
