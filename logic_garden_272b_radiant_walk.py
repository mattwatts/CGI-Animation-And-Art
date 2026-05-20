"""
SOVEREIGN CODE: logic_garden_272b_radiance.py
SYSTEM: Python Multicore / O(1) Continuous Serialisation Loop
SCENE: Logic Garden 272b (Radiance / Absolute Specular Phase)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Z-Axis Kinetic Wave Break & Extreme Luminosity Mapping

[INSTRUCTION]: Continuous 18.0s seamless loop. Total substrate radiance.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
RENDER_MODE = "RADIANCE_ABSOLUTE"  
DURATION = 18.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_272b_radiance"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE RADIANT PALETTE (MAXIMUM LUMINOSITY) --------
C_SKY_TOP   = '#FF4E00'        # Upper Atmosphere Ignition
C_SKY_BOT   = '#FFD800'        # Blinding Horizon Radiance
C_SUN       = '#FFFFFF'        # Core Singularity (Absolute White)
C_SUN_GLOW  = '#FFB700'        # Thermal Halo
C_SAND      = '#FFC04C'        # Wet Sunlit Sand (Highly Reflective)
C_OCEAN     = '#E65C00'        # Sun-Struck Water (Deep Orange/Gold)
C_FOAM      = '#FFDB4D'        # Glowing Crash Foam
C_NODE      = '#1A0000'        # Absolute High-Contrast Silhouette
C_FP_GLOW   = '#FFEAA7'        # Thermal Footprint Imprint
C_UI_TEXT   = '#FFFFFF'

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_sand    = np.array(hex_to_rgba(C_SAND)[:3])
c_ocean   = np.array(hex_to_rgba(C_OCEAN)[:3])
c_foam    = np.array(hex_to_rgba(C_FOAM)[:3])
c_node    = np.array(hex_to_rgba(C_NODE)[:3])
c_fp_glow = np.array(hex_to_rgba(C_FP_GLOW)[:3])
c_sun_glow= np.array(hex_to_rgba(C_SUN_GLOW)[:3])

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
# BASE GEOMETRY ARRAYS: THE RADIANT INTERFACE
# ------------------------------------------------------------------
MAX_PARTICLES = 40000
np.random.seed(272)

p_width = 360
p_depth = 280
px_base = np.random.uniform(-p_width/2, p_width/2, 30000)
# Shift the boundary to align with isometric projection
# Z > 0 is Ocean (Background). Z < 0 is Sand (Foreground).
pz_base = np.random.uniform(-100, 180, 30000)

type_mask = (pz_base > 0).astype(int) 

# Loop math parameters (Walking Left to Right)
walk_freq = 0.5 * np.pi  
stride_len = 22.0
velocity = stride_len * walk_freq * 2.0 

wave_cycles = 3.0 # Number of waves that crash perfectly per 18-sec loop

# Pre-compute Glowing Footprint Traces
num_footprints = 40
fp_z_pos = np.zeros(num_footprints)
fp_x_base = np.zeros(num_footprints)

for i in range(num_footprints):
    is_left = (i % 2 == 0)
    fp_z_pos[i] = -6.0 if is_left else 2.0 # Barely touching the breaking foam
    fp_x_base[i] = (i * stride_len * 1.3) % p_width - (p_width/2)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, p_x, p_y, p_z, c_arr, s_arr, a_arr = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    # Blinding Dawn Background Gradient
    gradient = np.linspace(0, 1, 256).reshape(-1, 1)
    gradient = np.hstack([gradient, gradient])
    ax.imshow(gradient, aspect='auto', cmap=matplotlib.colors.LinearSegmentedColormap.from_list('dawn', [C_SKY_BOT, C_SKY_TOP]), extent=[-160, 160, -260, 260], zorder=-10)
    
    # The Faucet Singularity over the Deep Ocean
    # Pinned to the background horizon
    ax.add_patch(plt.Circle((0, 35), 90, color=C_SUN_GLOW, alpha=0.4, zorder=-7))
    ax.add_patch(plt.Circle((0, 35), 60, color=C_SUN_GLOW, alpha=0.8, zorder=-6))
    ax.add_patch(plt.Circle((0, 35), 30, color=C_SUN, alpha=1.0, zorder=-5))

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

    # Ocean and Sand rendering
    ax.scatter(s_x, s_y, s=s_size, color=rgba_colors, edgecolors='none', zorder=10)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    tx_c = C_UI_TEXT
    
    # Exact Directive Title Application
    ax.text(-140, 240, "LG-272b  ::  Radiance", color=tx_c, fontsize=18, fontname='monospace', weight='bold', va='center', zorder=81)
    ax.text(-140, 225, "SYSTEM: O(1) CONTINUOUS SERIALISATION TRACE", color=tx_c, fontsize=9, fontname='monospace', zorder=81)

    # Widget Styling updated for Extreme Luminosity Contrast
    ax.add_patch(plt.Rectangle((-140, -200), 280, 20, facecolor=C_NODE, alpha=0.85, zorder=80))
    ax.text(0, -190, "ABSOLUTE METRIC :: BASKING", color=C_SUN, fontsize=11, fontname='monospace', weight='bold', ha='center', va='center', zorder=81)

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

        # Stationary tracking camera observing laterally but angled
        # Looking out over the ocean toward the sun
        cam_rx = np.pi/12 
        cam_ry = 0.0 # Straight on to center the sun reflection
        cam_rz = 0.0

        c_arr = np.zeros((MAX_PARTICLES, 3))
        s_arr = np.ones(MAX_PARTICLES) * 4.0
        a_arr = np.ones(MAX_PARTICLES)

        curr_x = np.zeros(MAX_PARTICLES)
        curr_y = np.zeros(MAX_PARTICLES)
        curr_z = np.zeros(MAX_PARTICLES)

        # -------------------------------------------------------------
        # THE MOVING SUBSTRATE & KINETIC OCEAN PARAMETERS
        # -------------------------------------------------------------
        # 1. Lateral Base movement (-X axis)
        shift_x = (px_base - (t_sec * velocity)) % p_width - (p_width/2)
        
        curr_x[:30000] = shift_x
        curr_z[:30000] = pz_base
        
        # 2. Z-Axis Crashing Wave Math (Perpendicular to Walk)
        # Wave phase linked perfectly to the 18s duration to ensure seamless loop
        wave_time = (t_sec / DURATION) * 2 * np.pi * wave_cycles
        wave_vector = pz_base * 0.15 - wave_time 
        
        wave_height = np.sin(wave_vector) * 8.0
        
        # Height applies strictly to Ocean (Z > 0)
        curr_y[:30000][type_mask == 1] = wave_height[type_mask == 1]
        
        # 3. Specular Reflection Logic (The "Glow" Path)
        # The sun is at X=0 in the background. Reflection creates a heavy vertical band.
        reflect_dist = np.abs(shift_x) 
        specular_boost = np.clip(1.0 - (reflect_dist / 40.0), 0.0, 1.0)

        for i in range(30000):
            if type_mask[i] == 0: # Sand Phase
                # Base sand reflects the sun path intensely
                base_col = c_sand * (1.0 - specular_boost[i]) + c_sun_glow * specular_boost[i]
                c_arr[i] = base_col
                s_arr[i] = 4.0 + (specular_boost[i] * 3.0)
                a_arr[i] = 0.9 + (specular_boost[i] * 0.1)

            else: # Ocean Phase
                is_breaking = (curr_y[i] > 4.0) and (pz_base[i] < 35) # Waves peak near the shore
                
                if is_breaking:
                    # Crashing crest applies glowing foam
                    base_col = c_foam * (1.0 - specular_boost[i]) + c_sun_glow * specular_boost[i]
                    s_arr[i] = 6.0 + (specular_boost[i] * 4.0)
                else:
                    # Deep ocean reflects sun path
                    base_col = c_ocean * (1.0 - specular_boost[i]*0.8) + c_sun_glow * specular_boost[i]*0.8
                    s_arr[i] = 4.0 + (specular_boost[i] * 2.0)
                
                c_arr[i] = base_col
                a_arr[i] = 0.95

        # -------------------------------------------------------------
        # THE LUMINOUS TRACE (Glowing footprints bleeding off Left)
        # -------------------------------------------------------------
        fp_shift_x = (fp_x_base - (t_sec * velocity)) % p_width - (p_width/2)
        
        idx = 30000
        for i in range(num_footprints):
            curr_x[idx:idx+80] = fp_shift_x[i] + np.random.uniform(-3, 3, 80)
            curr_z[idx:idx+80] = fp_z_pos[i] + np.random.uniform(-3, 3, 80)
            curr_y[idx:idx+80] = 0.8 # Sits atop the wet sand layer
            
            c_arr[idx:idx+80] = c_fp_glow
            s_arr[idx:idx+80] = 6.0
            
            # Continuous fade towards the left border
            fp_alpha = np.clip((fp_shift_x[i] + (p_width/2)) / 120.0, 0.0, 1.0)
            a_arr[idx:idx+80] = fp_alpha
            idx += 80

        # -------------------------------------------------------------
        # THE SOVEREIGN NODE (Centred Walk Cycle along X-axis)
        # -------------------------------------------------------------
        cycle = t_sec * walk_freq * 2.0
        sf_scale = 17.0
        n_x = 0.0 # Perfect Centre Lock
        n_z = 0.0 # Exactly on the phase interface line

        hip_y = (sf_scale * 2.0) - np.abs(np.sin(cycle))*sf_scale*0.12
        spine_y = hip_y + sf_scale
        head_y = spine_y + sf_scale*0.4

        l_foot_x = n_x + np.cos(cycle)*stride_len
        r_foot_x = n_x + np.cos(cycle + np.pi)*stride_len
        
        l_foot_y = max(0.0, -np.sin(cycle)*stride_len*0.35)
        r_foot_y = max(0.0, -np.sin(cycle + np.pi)*stride_len*0.35)

        l_arm_x = n_x - np.cos(cycle)*stride_len*0.6
        r_arm_x = n_x - np.cos(cycle + np.pi)*stride_len*0.6

        bone_t = np.linspace(0, 1, 800)
        sf_x = np.zeros(6800)
        sf_y = np.zeros(6800)
        sf_z = np.zeros(6800)

        # Silhouette Actuator Forge (Total Absorbance C_NODE against the bright radiance)
        b_idx = 0
        u = np.random.uniform(0, 2*np.pi, 2000)
        v = np.arccos(np.random.uniform(-1, 1, 2000))
        sf_x[b_idx:b_idx+2000] = n_x + np.sin(v)*np.cos(u)*sf_scale*0.45
        sf_y[b_idx:b_idx+2000] = head_y + np.cos(v)*sf_scale*0.45
        sf_z[b_idx:b_idx+2000] = n_z + np.sin(v)*np.sin(u)*sf_scale*0.45
        b_idx += 2000

        sf_x[b_idx:b_idx+800] = n_x
        sf_y[b_idx:b_idx+800] = hip_y + (spine_y - hip_y)*bone_t
        sf_z[b_idx:b_idx+800] = n_z
        b_idx += 800
        
        sf_x[b_idx:b_idx+800] = l_foot_x + (n_x - l_foot_x)*bone_t
        sf_y[b_idx:b_idx+800] = l_foot_y + (hip_y - l_foot_y)*bone_t
        sf_z[b_idx:b_idx+800] = n_z - sf_scale*0.2
        b_idx += 800

        sf_x[b_idx:b_idx+800] = r_foot_x + (n_x - r_foot_x)*bone_t
        sf_y[b_idx:b_idx+800] = r_foot_y + (hip_y - r_foot_y)*bone_t
        sf_z[b_idx:b_idx+800] = n_z + sf_scale*0.2
        b_idx += 800

        sf_x[b_idx:b_idx+800] = l_arm_x + (n_x - l_arm_x)*bone_t
        sf_y[b_idx:b_idx+800] = hip_y + (spine_y - hip_y)*bone_t
        sf_z[b_idx:b_idx+800] = n_z - sf_scale*0.6
        b_idx += 800

        sf_x[b_idx:b_idx+800] = r_arm_x + (n_x - r_arm_x)*bone_t
        sf_y[b_idx:b_idx+800] = hip_y + (spine_y - hip_y)*bone_t
        sf_z[b_idx:b_idx+800] = n_z + sf_scale*0.6
        b_idx += 800

        curr_x[33200:40000] = sf_x
        curr_y[33200:40000] = sf_y
        curr_z[33200:40000] = sf_z

        c_arr[33200:40000] = c_node
        s_arr[33200:40000] = 6.0
        a_arr[33200:40000] = 1.0

        # Apply Global Tensor Matrix
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)

        # Base track projection
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1] - 40.0
        z_depth = rot_pts[:, 2]

        yield (f, t_sec, proj_x, proj_y, z_depth, c_arr, s_arr, a_arr)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 272b: RADIANCE [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Absolute Specular Reflection & Perpendicular Wave Break")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Substrate Basking Enabled. Seamless loop secured.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
