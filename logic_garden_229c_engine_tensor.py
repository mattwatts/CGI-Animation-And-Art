"""
SOVEREIGN CODE: logic_garden_229c_engine_tensor.py
SYSTEM: Python Multicore / O(1) Spatial Topology
SCENE: Logic Garden 229c (The Starship Engine / High-Torque 10s Loop)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Perfect 10.0s 2-Pi Rotational Calculus, Variable Reference Purge, Photorealistic Alloys
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
RENDER_MODE = "HIGH-TORQUE SECURE"
DURATION = 10.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_229c_engine_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE PHOTOREALISTIC ENGINEERING PALETTE (WHITE BG) --------
C_BG        = '#FFFFFF'        # Daylight Baseplate
C_TUNGSTEN  = '#2B2B2C'        # Deep Core Metals
C_TITANIUM  = '#8A8D8F'        # Outer Hull Ribbing
C_STEEL     = '#5D6D7E'        # Nozzle Flaring
C_HOT_IRON  = '#D35400'        # Thermal Wash on Nozzle Base
C_COPPER    = '#B87333'        # Magnetic Confinement Rings
C_PLASMA    = '#00FFFF'        # Hyper-Luminous Exhaust Core
C_CORE      = '#E0FFFF'        # Blinding Inner Reaction
C_DIM       = '#BDC3C7'        # Blueprint Orthogonals

MAX_PARTICLES = 40000

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg        = np.array(hex_to_rgba(C_BG)[:3])
c_tungsten  = np.array(hex_to_rgba(C_TUNGSTEN)[:3])
c_titanium  = np.array(hex_to_rgba(C_TITANIUM)[:3])
c_steel     = np.array(hex_to_rgba(C_STEEL)[:3])
c_hot_iron  = np.array(hex_to_rgba(C_HOT_IRON)[:3])
c_copper    = np.array(hex_to_rgba(C_COPPER)[:3])
c_plasma    = np.array(hex_to_rgba(C_PLASMA)[:3])
c_core      = np.array(hex_to_rgba(C_CORE)[:3])

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
np.random.seed(229) 

N_PLASMA = 6000
N_NOZZLE = 14000
N_HULL   = 12000
N_RINGS  = 8000
assert N_PLASMA + N_NOZZLE + N_HULL + N_RINGS == MAX_PARTICLES

# 1. Plasma Core / Exhaust Plume (Z: -100 to 90)
p_z = np.random.uniform(-100, 90, N_PLASMA)
p_th = np.random.uniform(0, 2*np.pi, N_PLASMA)
p_r = np.random.uniform(0, 1) * (12.0 + 8.0 * np.sin(p_z * 0.05))
px_p = p_r * np.cos(p_th)
py_p = p_r * np.sin(p_th)
pz_p = p_z

# 2. Hyperbolic Exhaust Bell (Z: -90 to -10)
n_z = np.random.uniform(-90, -10, N_NOZZLE)
n_th = np.random.uniform(0, 2*np.pi, N_NOZZLE)
n_r = 25.0 + ((n_z + 10)**2) / 60.0 
px_n = n_r * np.cos(n_th)
py_n = n_r * np.sin(n_th)
pz_n = n_z

# 3. Main Reactor Hull (Z: -10 to 100)
h_z = np.random.uniform(-10, 100, N_HULL)
h_th = np.random.uniform(0, 2*np.pi, N_HULL)
h_r = 45.0 + 12.0 * np.abs(np.sin(h_z * 0.35))
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

# Compile full absolute structure (Fixed variable nomenclature)
px_base = np.concatenate([px_p, px_n, px_h, px_r])
py_base = np.concatenate([py_p, py_n, py_h, py_r])
pz_base = np.concatenate([pz_p, pz_n, pz_h, pz_r])

# Static Color Maps
base_colors = np.zeros((MAX_PARTICLES, 3))
base_sizes = np.ones(MAX_PARTICLES)

p_idx = N_PLASMA
n_idx = p_idx + N_NOZZLE
h_idx = n_idx + N_HULL

for i in range(p_idx):
    ratio = np.clip((pz_p[i] + 100) / 190.0, 0, 1)
    base_colors[i] = c_core * ratio + c_plasma * (1.0 - ratio)
base_sizes[:p_idx] = 6.0

for i in range(p_idx, n_idx):
    idx = i - p_idx
    ratio = np.clip((pz_n[idx] + 90) / 80.0, 0, 1)
    base_colors[i] = c_steel * (1.0 - ratio) + c_hot_iron * ratio
base_sizes[p_idx:n_idx] = 4.5

for i in range(n_idx, h_idx):
    idx = i - n_idx
    is_rib_peak = np.abs(np.sin(pz_h[idx] * 0.35)) > 0.8
    base_colors[i] = c_titanium if is_rib_peak else c_tungsten
base_sizes[n_idx:h_idx] = 5.0

base_colors[h_idx:] = c_copper
base_sizes[h_idx:] = 7.0

# Center Geometry algebraically
pz_base -= 15.0

print("PHASE 1: 40,000 NODE STARSHIP TENSOR COMPILED.")

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

    # O(N*logN) Depth Sorting (Painters Algorithm for Absolute Density)
    sort_idx = np.argsort(z_depth)
    s_px = proj_x[sort_idx]
    s_py = proj_y[sort_idx]
    s_c = colors[sort_idx]
    s_s = sizes[sort_idx]

    ax.scatter(s_px, s_py, s=s_s, color=s_c, edgecolors='none', alpha=0.9, zorder=10)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    ax.text(-140, 240, "LG-229c :: STARSHIP KINEMATIC TENSOR", color=C_TUNGSTEN, fontsize=18, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: 40K DATA POINTS / TATHATA ROTATION (10S)", color=C_TUNGSTEN, fontsize=9, fontname='monospace', zorder=80)

    ax.text(-140, -200, f"STATE: {state_str}", color=C_HOT_IRON, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, -220, "STRUCTURAL INTEGRITY [ABSOLUTE LOCK] ZERO DISTORTION", color=C_TUNGSTEN, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -225), 280, 2, facecolor=C_TUNGSTEN, zorder=80))

    prog_ratio = t_sec / DURATION
    ax.add_patch(plt.Rectangle((-140, -225), 280 * prog_ratio, 2, facecolor=C_PLASMA, zorder=81))

    # Blueprint Callouts
    ax.text(-140, -40, "[MAGNETIC RINGS: COPPER/TUNGSTEN]", color=C_TUNGSTEN, fontsize=8, fontname='monospace', zorder=80)
    ax.text(-140, -55, "[PLASMA CORE: SUPER-HEATED CYAN]", color=C_TUNGSTEN, fontsize=8, fontname='monospace', zorder=80)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# O(1) STRUCTURAL INVERSION KINEMATICS
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        state = "HIGH-TORQUE CONTINUOUS REVOLUTION [10.0S]"

        # Isometric Camera - Flawless 360-Degree Continuous Rotation over exactly 10s
        cam_rx = np.pi / 7 
        cam_ry = (t_sec / DURATION) * (2 * np.pi)
        cam_rz = 0.0

        curr_x = px_base
        curr_y = py_base
        curr_z = pz_base

        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)

        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1]
        z_depth = rot_pts[:, 2]

        # Geometry Culling 
        cull_mask = (proj_y > -260) & (proj_y < 260) & (proj_x > -160) & (proj_x < 160)

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], base_colors[cull_mask], base_sizes[cull_mask])

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 229c: STARSHIP ENGINE TENSOR [MODE: {RENDER_MODE}] [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Continuous 10-Second Pi-Rotation Vector Lock")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Matrix successfully bridged.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
