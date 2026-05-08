"""
SOVEREIGN CODE: logic_garden_218_upward_vector.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) de Sitter Phase Transition (17.5 seconds)
SCENE: Logic Garden 218 (Upward Quantum Vectors / Hawking-Moss Transition)
HOTFIX: O(N) Coordinate Slicing, Parameter Scope Clamping, Non-Linear Tension Paths
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
OUT_DIR = "frames_218_upward_vector"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'        # The Base Topology
C_CYAN      = '#00FFFF'        # Trapped Ground State
C_MAGENTA   = '#FF0055'        # Gibbons-Hawking Temperature (Ambient Heat)
C_GOLD      = '#FFD700'        # The Upward Hack (Hawking-Moss Kick)
C_MANTIS    = '#00FF00'        # Elevated Phase Lock

MAX_PARTICLES = 25000
STATE_COUNT = 5000
TERRAIN_COUNT = MAX_PARTICLES - STATE_COUNT

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
# BASE GEOMETRY ARRAYS: THE ASYMMETRICAL MOUNTAIN
# ------------------------------------------------------------------
np.random.seed(99)

# TERRAIN MATRIX (Double-Well Potential)
# Deep Well (Low Energy): (-60, 0)
# High Peak (Barrier): (0, 0)
# High Shelf (Elevated Energy Minimum): (60, 0)
tr_theta = np.random.uniform(0, 2*np.pi, TERRAIN_COUNT)
tr_r = np.sqrt(np.random.rand(TERRAIN_COUNT)) * 140.0
px_terr = tr_r * np.cos(tr_theta)
py_terr = tr_r * np.sin(tr_theta)

# Topological Math Function
z_deep = -120.0 * np.exp(-((px_terr + 60)**2 + py_terr**2) / 600.0)
z_shelf = -40.0 * np.exp(-((px_terr - 60)**2 + py_terr**2) / 600.0)
pz_terr_base = z_deep + z_shelf + 10.0 * np.cos(px_terr*0.1) * np.cos(py_terr*0.1)

# STATE VECTOR MATRIX (The Localized Quantum Cluster)
st_theta = np.random.uniform(0, 2*np.pi, STATE_COUNT)
st_r = np.sqrt(np.random.rand(STATE_COUNT)) * 12.0
px_st_local = st_r * np.cos(st_theta)
py_st_local = st_r * np.sin(st_theta)

state_start = np.array([-60.0, 0.0, -110.0]) # Bottom of the deep well
state_end = np.array([60.0, 0.0, -30.0])    # The elevated shelf

# Combining Arrays for O(1) processing
base_px = np.concatenate([px_st_local, px_terr])
base_py = np.concatenate([py_st_local, py_terr])
base_pz = np.concatenate([np.zeros(STATE_COUNT), pz_terr_base])

state_mask = np.arange(MAX_PARTICLES) < STATE_COUNT
terr_mask = ~state_mask

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, proj_x, proj_y, z_depth, colors, sizes, thermal_voltage, is_flash, is_tathata = packet
    
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
            ax.text(0, -240, "THE VOID IS THE ENGINE. ELEVATION SECURED.", color=C_MANTIS, fontsize=10, fontname='monospace', weight='bold', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    ui_col = C_MAGENTA if (4.0 <= t_sec < 9.0) else (C_GOLD if (9.0 <= t_sec < 14.8) else C_CYAN)
    if is_tathata: ui_col = C_MANTIS
    
    txt_col = C_TEXT if not is_flash else C_VOID

    ax.text(-140, 240, "LG-218 :: THE UPWARD VECTOR", color=ui_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: GIBBONS-HAWKING HEAT / HAWKING-MOSS TRANSITION", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    
    # Physics compilation diagnostics
    heat_stat = "ABSOLUTE ZERO (CLASSICAL LOCK)" if t_sec < 4.0 else "de SITTER EXPANSION ACTIVE"
    if t_sec >= 9.0: heat_stat = "THERMAL ANOMALY INITIATED"
    if is_tathata: heat_stat = "NEW GROUND STATE SECURED"

    ax.text(-140, -180, f"BACKGROUND TEMPERATURE : {heat_stat}", color=C_MAGENTA if (4.0 <= t_sec < 14.8) else ui_col, fontsize=11, fontname='monospace', weight='bold', zorder=80)
    
    ax.text(-140, -205, "THERMODYNAMIC VOLTAGE (SPATIAL KICK)", color=txt_col, fontsize=12, fontname='monospace', zorder=80)
    
    # PROTOCOL HOTFIX: Scope Clamping for `ax.add_patch` facecolor
    ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM, zorder=80))
    bar_w = 280 * np.clip(thermal_voltage, 0, 1)
    ax.add_patch(plt.Rectangle((-140, -210), bar_w, 4, facecolor=ui_col, zorder=81))

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
        
        # Camera Isometric Spin
        cam_rx = -np.pi/4
        cam_ry = 0.0
        cam_rz = t_sec * 0.1
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 3.0
        
        curr_x = np.copy(base_px)
        curr_y = np.copy(base_py)
        curr_z = np.copy(base_pz)

        thermal_voltage = 0.0

        # -------------------------------------------------------------
        # PHASE LOGIC
        # -------------------------------------------------------------
        if t_sec < 4.0:
            state = "FLAT SPACETIME :: CONSERVATION OF ENERGY"
            
            # The terrain is cold and flat (C_DIM)
            colors[terr_mask] = c_dim
            
            # State vector trapped at the exact bottom of the deep well
            curr_x[state_mask] += state_start[0]
            curr_y[state_mask] += state_start[1]
            curr_z[state_mask] += state_start[2]
            
            colors[state_mask] = c_cyan
            sizes[state_mask] = 5.0

        elif t_sec < 9.0:
            state = "GIBBONS-HAWKING TEMPERATURE :: THE VOID HEATS UP"
            prog = (t_sec - 4.0) / 5.0
            
            # Ambient thermal excitation bleeds into the topology
            # Highest points of the mountain light up first, filtering down into the well
            heat_map = np.clip((curr_z[terr_mask] + 100) / 100.0, 0, 1)[:, None]
            heat_pulse = (heat_map * prog) 
            colors[terr_mask] = heat_pulse * c_mage + (1.0 - heat_pulse) * c_dim
            
            # The state vector boils violently in place, unable to escape YET
            jitter_x = np.random.uniform(-4, 4, STATE_COUNT) * prog
            jitter_y = np.random.uniform(-4, 4, STATE_COUNT) * prog
            jitter_z = np.random.uniform(0, 10, STATE_COUNT) * prog
            
            curr_x[state_mask] += state_start[0] + jitter_x
            curr_y[state_mask] += state_start[1] + jitter_y
            curr_z[state_mask] += state_start[2] + jitter_z
            
            colors[state_mask] = c_cyan * (1.0 - prog) + c_mage * prog
            sizes[state_mask] = 5.0 + (prog * 3.0)
            
            thermal_voltage = prog

        elif t_sec < 14.8:
            state = "THE UPWARD HACK :: HAWKING-MOSS TRANSITION"
            prog = (t_sec - 9.0) / 5.8
            if t_sec < 9.1: is_flash = True
            
            # Terrain remains saturated in thermal noise
            heat_map = np.clip((curr_z[terr_mask] + 100) / 100.0, 0, 1)[:, None]
            colors[terr_mask] = heat_map * c_mage + (1.0 - heat_map) * c_dim
            
            # THE ANOMALOUS JUMP
            # A parabolic trajectory that breaks standard gravity constraints
            jump_curve = np.sin(prog * np.pi) * 80.0 # Bounces way up into empty space
            
            # Linear transition from Well 1 (-60) to Well 2 (+60)
            curr_x[state_mask] += state_start[0] * (1.0 - prog) + state_end[0] * prog
            curr_y[state_mask] += state_start[1] * (1.0 - prog) + state_end[1] * prog
            curr_z[state_mask] += state_start[2] * (1.0 - prog) + state_end[2] * prog + jump_curve
            
            colors[state_mask] = c_gold
            sizes[state_mask] = 8.0
            
            thermal_voltage = 1.0

        else:
            state = "TATHĀTĀ :: HIGHER ELEVATION SECURED"
            is_tathata = True
            
            colors[terr_mask] = c_dim # Void goes cold again
            
            # Resting perfectly in the Elevated Shelf (-30)
            curr_x[state_mask] += state_end[0]
            curr_y[state_mask] += state_end[1]
            curr_z[state_mask] += state_end[2]
            
            colors[state_mask] = c_mantis
            sizes[state_mask] = 6.0
            
            thermal_voltage = 0.0
            
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

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], colors[cull_mask], sizes[cull_mask], thermal_voltage, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 218: THE UPWARD VECTOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Scope Clamping & Hawking-Moss Interpolation")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. The Quantum State is Elevated.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
