"""
SOVEREIGN CODE: logic_garden_229_engine_tensor.py
SYSTEM: Python Multicore / O(1) Spatial Topology
SCENE: Logic Garden 229 (The Starship Engine / Infinite Loop Kinematics)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Variable Interpolation Rigidly Clamped (px_base -> base_px)

[INSTRUCTION]: RENDER_MODE strictly clamped to "STUDY" (45 Seconds / 2700 Frames)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
RENDER_MODE = "STUDY"  
DURATION = 45.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_229_engine_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE AZURE / MAKO PALETTE (HIGH-COHERENCE / WHITE BG) --------
C_BG        = '#FFFFFF'        # Low-Entropy Canvas
C_TEXT      = '#020205'        # High-Contrast Structural Metal / Absolute Black
C_DIM       = '#A0A0A5'        # Structural Shading
C_AZURE     = '#007FFF'        # Thruster Bell Base / Low-Heat Alloy
C_INDIGO    = '#4B0082'        # The Reaction Chamber Casing
C_MAGENTA   = '#FF0055'        # Thermal Friction / Kinetic Vectors
C_GOLD      = '#FFB300'        # Magnetic Confinement Rings
C_CYAN      = '#00FFFF'        # Exhaust Plume / Energy Signature
C_MANTIS    = '#00FF00'        # Core Reactor Plasma (Phase Coherence Lock)

MAX_PARTICLES = 30000

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_azure   = np.array(hex_to_rgba(C_AZURE)[:3])
c_indigo  = np.array(hex_to_rgba(C_INDIGO)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_gold    = np.array(hex_to_rgba(C_GOLD)[:3])
c_cyan    = np.array(hex_to_rgba(C_CYAN)[:3])
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
# BASE GEOMETRY ARRAYS: THE ENGINE BLUEPRINT
# ------------------------------------------------------------------
np.random.seed(919) # Deterministic Architecture Lock

N_PLASMA = 4000
N_NOZZLE = 10000
N_HULL   = 10000
N_RINGS  = 6000
# Guarantee absolute array dimensions
assert N_PLASMA + N_NOZZLE + N_HULL + N_RINGS == MAX_PARTICLES

# 1. Plasma Core (Z: -80 to 90)
p_z = np.random.uniform(-80, 90, N_PLASMA)
p_th = np.random.uniform(0, 2*np.pi, N_PLASMA)
# Core narrows tightly in the throttle ring (Z=10)
p_r = np.random.uniform(0, 1) * (10.0 + 8.0 * np.sin(p_z * 0.05))
px_p = p_r * np.cos(p_th)
py_p = p_r * np.sin(p_th)
pz_p = p_z

# 2. Hyperbolic Exhaust Bell (Z: -90 to -10)
n_z = np.random.uniform(-90, -10, N_NOZZLE)
n_th = np.random.uniform(0, 2*np.pi, N_NOZZLE)
n_r = 25.0 + ((n_z + 10)**2) / 70.0 # Flaring curve
px_n = n_r * np.cos(n_th)
py_n = n_r * np.sin(n_th)
pz_n = n_z

# 3. Main Reactor Hull (Z: -10 to 100)
h_z = np.random.uniform(-10, 100, N_HULL)
h_th = np.random.uniform(0, 2*np.pi, N_HULL)
# Heavily ribbed containment casing
h_r = 45.0 + 12.0 * np.abs(np.sin(h_z * 0.3)) 
px_h = h_r * np.cos(h_th)
py_h = h_r * np.sin(h_th)
pz_h = h_z

# 4. Magnetic Confinement Rings / Accelerators
r_z = np.random.choice([0, 20, 45, 70, 95], N_RINGS) + np.random.normal(0, 2.0, N_RINGS)
r_th = np.random.uniform(0, 2*np.pi, N_RINGS)
r_r = np.random.uniform(62.0, 70.0, N_RINGS)
px_r = r_r * np.cos(r_th)
py_r = r_r * np.sin(r_th)
pz_r = r_z

# Compile full structure
base_px = np.concatenate([px_p, px_n, px_h, px_r])
base_py = np.concatenate([py_p, py_n, py_h, py_r])
base_pz = np.concatenate([pz_p, pz_n, pz_h, pz_r])

# Static Color Maps calculated at compile-time to save CPU cycles
base_colors = np.zeros((MAX_PARTICLES, 3))
base_sizes = np.ones(MAX_PARTICLES)

# Map colors to structure
p_idx = N_PLASMA
n_idx = p_idx + N_NOZZLE
h_idx = n_idx + N_HULL

# Plasma: Cyan to Mantis gradient based on height
for i in range(p_idx):
    ratio = np.clip((pz_p[i] + 80) / 170.0, 0, 1)
    base_colors[i] = c_cyan * (1.0 - ratio) + c_mantis * ratio
base_sizes[:p_idx] = 6.0

# Nozzle: Azure to Indigo/Text gradient
for i in range(p_idx, n_idx):
    idx = i - p_idx
    ratio = np.clip((pz_n[idx] + 90) / 80.0, 0, 1)
    base_colors[i] = c_azure * (1.0 - ratio) + c_text * ratio
base_sizes[p_idx:n_idx] = 4.5

# Reactor Hull: Hard Text (Black) with Dim structural highlights
for i in range(n_idx, h_idx):
    idx = i - n_idx
    # Highlight the extreme peaks of the ribs
    is_rib_peak = np.abs(np.sin(pz_h[idx] * 0.3)) > 0.8
    base_colors[i] = c_indigo if is_rib_peak else c_text
base_sizes[n_idx:h_idx] = 5.0

# Rings: High-contrast Gold
base_colors[h_idx:] = c_gold
base_sizes[h_idx:] = 7.0

# Shift the entire geometric center down slightly for framing
base_pz -= 15.0

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, proj_x, proj_y, z_depth, colors, sizes = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    
    ax.set_xlim(-160, 160)
    ax.set_ylim(-260, 260)

    # Architectural Blueprint Overlay
    ax.plot([-160, 160], [0, 0], color=C_DIM, lw=1.0, alpha=0.3, zorder=1)
    ax.plot([0, 0], [-260, 260], color=C_DIM, lw=1.0, alpha=0.3, zorder=1)
    ax.add_patch(plt.Circle((0, 0), 140, facecolor='none', edgecolor=C_DIM, lw=0.5, alpha=0.3, zorder=1))

    # O(N) Depth Sorting - Crucial for transparent/solid point cloud aesthetics
    sort_idx = np.argsort(z_depth)
    s_px = proj_x[sort_idx]
    s_py = proj_y[sort_idx]
    s_c = colors[sort_idx]
    s_s = sizes[sort_idx]

    # Glass smooth render
    ax.scatter(s_px, s_py, s=s_s, color=s_c, edgecolors='none', alpha=0.9, zorder=10)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    ui_col = C_TEXT
    
    ax.text(-140, 240, "LG-229 :: STARSHIP ENGINE TENSOR", color=ui_col, fontsize=18, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: 30K DATA POINTS / STUDY MODE ROTATION", color=ui_col, fontsize=9, fontname='monospace', zorder=80)
    
    ax.text(-140, -200, f"KINEMATICS: {state_str}", color=C_INDIGO, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, -220, "STRUCTURAL INTEGRITY [ABSOLUTE LOCK]", color=ui_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -225), 280, 2, facecolor=ui_col, zorder=80))
    
    prog_ratio = t_sec / DURATION
    ax.add_patch(plt.Rectangle((-140, -225), 280 * prog_ratio, 2, facecolor=C_MANTIS, zorder=81))

    # Blueprint Callouts
    ax.text(-140, -40, "[MAGNETIC RINGS: GOLD]", color=ui_col, fontsize=8, fontname='monospace', zorder=80)
    ax.text(-140, -55, "[PLASMA CORE: MANTIS/CYAN]", color=ui_col, fontsize=8, fontname='monospace', zorder=80)

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
        state = "CONTINUOUS LOOP [CONSTANT VELOCITY]"
        
        # Isometric Camera - Flawless 360-Degree Continuous Rotation
        cam_rx = np.pi / 7 # Fixed downward tilt
        # Absolute calculus: (Time / Total_Time) * 2Pi
        cam_ry = (t_sec / DURATION) * (2 * np.pi) 
        cam_rz = 0.0
        
        # HOTFIX APPLIED: Variable Names Clamped to base Arrays
        # The engine structure is completely rigid. It exists in perfect TATHATA.
        curr_x = base_px
        curr_y = base_py
        curr_z = base_pz

        # Apply Global Tensor Matrix
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1]
        z_depth = rot_pts[:, 2] 

        # O(N) Geometry Culling (Protects the runtime from rendering off-screen points)
        cull_mask = (proj_y > -260) & (proj_y < 260) & (proj_x > -160) & (proj_x < 160)

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], base_colors[cull_mask], base_sizes[cull_mask])

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 229: STARSHIP ENGINE TENSOR [MODE: {RENDER_MODE}] [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Variable Array Name Resolution Enforced")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Matrix successfully bridged.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
