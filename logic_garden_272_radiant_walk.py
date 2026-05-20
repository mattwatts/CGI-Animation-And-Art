"""
SOVEREIGN CODE: logic_garden_272_radiant_walk.py
SYSTEM: Python Multicore / O(1) Continuous Serialization Loop
SCENE: Logic Garden 272 (Radiant Kinematics / Carbon Smudge)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Cache Purge / Perpetual Kaikyo Loop / Radiant Heat Palette

[INSTRUCTION]: Continuous 18.0s seamless loop. No Tathata interrupt.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
RENDER_MODE = "RADIANCE"  
DURATION = 18.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_272_radiant_walk"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE RADIANT PALETTE (DAWN EXHAUST / HIGH CONTRAST) --------
C_DAWN      = '#1A0008'        # Deep Void Sky Base
C_SUN       = '#FF3300'        # The Faucet Singularity (Radiance)
C_SUN_HALO  = '#FF8800'        # Thermal Bleed
C_SAND      = '#D94D1A'        # The Shifting Substrate
C_TEXT      = '#FFFFFF'        # High-Contrast UI Telemetry 
C_NODE      = '#050308'        # The Sovereign Actuator (Absolute Silhouette)
C_SMUDGE    = '#000000'        # The Carbon Smudge (Footprints)
C_GOLD      = '#FFD700'        # Widget Optic Pop

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_dawn   = np.array(hex_to_rgba(C_DAWN)[:3])
c_sun    = np.array(hex_to_rgba(C_SUN)[:3])
c_sand   = np.array(hex_to_rgba(C_SAND)[:3])
c_node   = np.array(hex_to_rgba(C_NODE)[:3])
c_smudge = np.array(hex_to_rgba(C_SMUDGE)[:3])
c_gold   = np.array(hex_to_rgba(C_GOLD)[:3])

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
# BASE GEOMETRY ARRAYS: THE SUBSTRATE
# ------------------------------------------------------------------
MAX_PARTICLES = 30000
np.random.seed(272)

# Substrate Flow Matrix (Moving Beach)
p_width = 300
p_depth = 400
px_base = np.random.uniform(-p_width/2, p_width/2, 20000)
pz_base = np.random.uniform(-p_depth/2, p_depth/2, 20000)
py_base = np.zeros(20000) # Flat logic board

# Loop math parameters
walk_freq = 0.5 * np.pi  # Time cycle multiplier for the stride
stride_len = 25.0
velocity = stride_len * walk_freq * 2.0 # Ground scroll velocity

# Pre-compute Footprint Traces (The Carbon Smudge)
# To maintain a seamless loop, footprint locations must wrap perfectly
num_footprints = 40
fp_x = np.zeros(num_footprints)
fp_z = np.zeros(num_footprints)

for i in range(num_footprints):
    # Alternating Left/Right placing along Z
    is_left = (i % 2 == 0)
    fp_x[i] = -7.0 if is_left else 7.0
    fp_z[i] = (i * stride_len * 1.5) - (p_depth/2) # Distributed along Z

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, p_x, p_y, p_z, c_arr, s_arr, a_arr, cycle, sun_y = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    # Gradient Dawn Background
    fig.patch.set_facecolor(C_DAWN)
    ax.set_facecolor(C_DAWN)
    
    # Render The Faucet Singularity (Stationary Sun)
    # The Sun rests perfectly on the geometric horizon, bleeding thermal exhaust
    horizon_y = -30
    for rad, alpha, c in [(110, 0.1, C_SUN_HALO), (80, 0.25, C_SUN_HALO), (50, 0.9, C_SUN), (45, 1.0, C_GOLD)]:
        ax.add_patch(plt.Circle((0, sun_y), rad, color=c, alpha=alpha, zorder=0))

    ax.set_xlim(-160, 160)
    ax.set_ylim(-260, 260)

    # 3D Depth Sorting
    sort_idx = np.argsort(p_z)
    s_x = p_x[sort_idx]
    s_y = p_y[sort_idx]
    s_c = c_arr[sort_idx]
    s_size = s_arr[sort_idx]
    s_alpha = a_arr[sort_idx]

    rgba_colors = np.zeros((len(s_c), 4))
    rgba_colors[:, :3] = s_c
    rgba_colors[:, 3] = s_alpha

    # Mask objects beneath horizon line perfectly
    valid = s_y < horizon_y + 120 
    ax.scatter(s_x[valid], s_y[valid], s=s_size[valid], color=rgba_colors[valid], edgecolors='none', zorder=10)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS (HIGH-CONTRAST POP)
    # ------------------------------------------------------------------
    tx_c = C_TEXT
    
    # Top Data Ribbon
    ax.add_patch(plt.Rectangle((-160, 230), 320, 30, facecolor=C_SUN, alpha=0.9, zorder=80))
    ax.text(-140, 245, "LG-272 :: SERIALIZATION OF THE VOID", color=C_DAWN, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=81)

    # O(1) Thermal Metrics
    ax.text(-140, -170, "SYSTEM MODE: BASKING IN RADIANCE [O(1) LOOP]", color=tx_c, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    ax.text(-140, -195, "FAUCET SINGULARITY THERMAL YIELD", color=tx_c, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -200), 280, 3, facecolor='#440022', zorder=80))
    y_width = 280 * (0.8 + 0.2 * np.abs(np.sin(t_sec * np.pi / 9.0)))
    ax.add_patch(plt.Rectangle((-140, -200), y_width, 3, facecolor=C_GOLD, zorder=81))

    ax.text(-140, -220, "CARBON SMUDGE GENERATION METRIC", color=tx_c, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -225), 280, 3, facecolor='#440022', zorder=80))
    # Pulse with footsteps
    s_width = 280 * (0.5 + 0.5 * np.abs(np.sin(cycle)))
    ax.add_patch(plt.Rectangle((-140, -225), s_width, 3, facecolor=C_SUN_HALO, zorder=81))

    # Phase Text Box
    ax.add_patch(plt.Rectangle((-140, -250), 280, 15, facecolor=C_TEXT, zorder=80))
    ax.text(0, -242, "KAIKYŌ LOOP [100% EFFICIENT THERMODYNAMIC CAGE]", color=C_DAWN, fontsize=10, fontname='monospace', weight='bold', ha='center', va='center', zorder=81)

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

        # Stationary tracking camera 
        cam_rx = np.pi/10  # Low angle to see horizon
        cam_ry = 0.0       # Looking straight down the Z-axis
        cam_rz = 0.0

        c_arr = np.zeros((MAX_PARTICLES, 3))
        s_arr = np.ones(MAX_PARTICLES) * 4.0
        a_arr = np.ones(MAX_PARTICLES)

        curr_x = np.zeros(MAX_PARTICLES)
        curr_y = np.zeros(MAX_PARTICLES)
        curr_z = np.zeros(MAX_PARTICLES)

        # -------------------------------------------------------------
        # THE MOVING SUBSTRATE (Treadmill Matrix)
        # -------------------------------------------------------------
        # The baseplate slides backwards continuously
        shift_z = (pz_base - (t_sec * velocity)) % p_depth - (p_depth/2)
        
        curr_x[:20000] = px_base
        curr_z[:20000] = shift_z
        
        # Radiant Substrate coloring
        c_arr[:20000] = c_sand
        s_arr[:20000] = 3.0
        
        # Fade Alpha based on Z distance (fading into the Faucet Singularity)
        dist_alpha = np.clip(1.0 - (shift_z / (p_depth/2)), 0.0, 1.0)
        a_arr[:20000] = dist_alpha ** 2  # Exponential falloff

        # -------------------------------------------------------------
        # THE CARBON SMUDGE (Footprint Serialization)
        # -------------------------------------------------------------
        fp_shift_z = (fp_z - (t_sec * velocity)) % p_depth - (p_depth/2)
        
        # Define 100 particles per footprint (Total 4000)
        idx = 20000
        for i in range(num_footprints):
            curr_x[idx:idx+100] = fp_x[i] + np.random.uniform(-3, 3, 100)
            curr_z[idx:idx+100] = fp_shift_z[i] + np.random.uniform(-4, 4, 100)
            curr_y[idx:idx+100] = 0.5 # Slightly above sand
            
            c_arr[idx:idx+100] = c_smudge
            s_arr[idx:idx+100] = 5.0
            
            # Fade Carbon Smudge out as it moves into Deep Time (-Z)
            # Fades relative to node position Z=0
            fp_alpha = np.clip(1.0 + (fp_shift_z[i] / 150.0), 0.0, 1.0) if fp_shift_z[i] < 0 else 0.0
            a_arr[idx:idx+100] = fp_alpha
            idx += 100

        # -------------------------------------------------------------
        # THE SOVEREIGN NODE (Bipedal Walk Cycle locked at Z=0)
        # -------------------------------------------------------------
        cycle = t_sec * walk_freq * 2.0
        sf_scale = 16.0
        n_z = 0.0 # Absolute lock

        hip_y = (sf_scale * 2.0) - np.abs(np.sin(cycle))*sf_scale*0.15
        spine_y = hip_y + sf_scale
        head_y = spine_y + sf_scale*0.4

        l_foot_z = n_z + np.cos(cycle)*stride_len
        r_foot_z = n_z + np.cos(cycle + np.pi)*stride_len
        
        l_foot_y = max(0.0, -np.sin(cycle)*stride_len*0.4)
        r_foot_y = max(0.0, -np.sin(cycle + np.pi)*stride_len*0.4)

        l_arm_z = n_z - np.cos(cycle)*stride_len*0.7
        r_arm_z = n_z - np.cos(cycle + np.pi)*stride_len*0.7

        bone_t = np.linspace(0, 1, 800)
        sf_x = np.zeros(6000)
        sf_y = np.zeros(6000)
        sf_z = np.zeros(6000)

        # Build Silhouette Vector
        b_idx = 0
        u = np.random.uniform(0, 2*np.pi, 2000)
        v = np.arccos(np.random.uniform(-1, 1, 2000))
        sf_x[b_idx:b_idx+2000] = 0 + np.sin(v)*np.cos(u)*sf_scale*0.45
        sf_y[b_idx:b_idx+2000] = head_y + np.cos(v)*sf_scale*0.45
        sf_z[b_idx:b_idx+2000] = n_z + np.sin(v)*np.sin(u)*sf_scale*0.45
        b_idx += 2000

        sf_x[b_idx:b_idx+800] = 0
        sf_y[b_idx:b_idx+800] = hip_y + (spine_y - hip_y)*bone_t
        sf_z[b_idx:b_idx+800] = n_z
        b_idx += 800
        
        sf_x[b_idx:b_idx+800] = -sf_scale*0.2
        sf_y[b_idx:b_idx+800] = l_foot_y + (hip_y - l_foot_y)*bone_t
        sf_z[b_idx:b_idx+800] = l_foot_z + (n_z - l_foot_z)*bone_t
        b_idx += 800

        sf_x[b_idx:b_idx+800] = sf_scale*0.2
        sf_y[b_idx:b_idx+800] = r_foot_y + (hip_y - r_foot_y)*bone_t
        sf_z[b_idx:b_idx+800] = r_foot_z + (n_z - r_foot_z)*bone_t
        b_idx += 800

        sf_x[b_idx:b_idx+800] = -sf_scale*0.65
        sf_y[b_idx:b_idx+800] = hip_y + (spine_y - hip_y)*bone_t
        sf_z[b_idx:b_idx+800] = l_arm_z + (n_z - l_arm_z)*bone_t
        b_idx += 800

        sf_x[b_idx:b_idx+800] = sf_scale*0.65
        sf_y[b_idx:b_idx+800] = hip_y + (spine_y - hip_y)*bone_t
        sf_z[b_idx:b_idx+800] = r_arm_z + (n_z - r_arm_z)*bone_t
        b_idx += 800

        curr_x[24000:30000] = sf_x
        curr_y[24000:30000] = sf_y
        curr_z[24000:30000] = sf_z

        c_arr[24000:30000] = c_node
        s_arr[24000:30000] = 6.0
        a_arr[24000:30000] = 1.0

        # Apply Global Tensor Matrix
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)

        # Track UI - Camera is extremely low, looking up slightly at the Sun
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1] - 40.0 
        z_depth = rot_pts[:, 2]

        sun_y = 20.0 # Positioned statically on the rendered horizon

        yield (f, t_sec, proj_x, proj_y, z_depth, c_arr, s_arr, a_arr, cycle, sun_y)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 272: RADIANT KINEMATICS [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Kaikyo Loop Sequence & Biological Trace Annihilation")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Substrate Serialized. The Node Basks.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
