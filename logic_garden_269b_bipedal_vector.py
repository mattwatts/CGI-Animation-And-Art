"""
SOVEREIGN CODE: logic_garden_269b_bipedal_vector.py
SYSTEM: Python Multicore / O(1) Boundary Kinematics
SCENE: Logic Garden 269b (The Bipedal Vector / Minimal Spanning Actuator)
FORMAT: YouTube Shorts (1080x1920) // 60 FPS
HOTFIX: Continuous Locomotion Extension (Static Lock Purged)

[INSTRUCTION]: True Continuous Vector Architecture (No Dots).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.collections import LineCollection
import multiprocessing as mp
import os
import gc
import subprocess

# ======== ARCHITECT CONDITIONAL LOGIC ========
DURATION = 18.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_269b_bipedal"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS DEFAULT) --------
C_BG        = '#FFFFFF'        # Absolute Flat Substrate
C_TEXT      = '#020205'        # UI Widgets / Burned Footprints
C_AZURE     = '#007FFF'        # Fluid State (Ocean)
C_MAGENTA   = '#FF0055'        # Node Core / Bipedal Mechanism
C_GOLD      = '#FFB300'        # Friction Transfer / Walk Exhaust
C_DIM       = '#A0A0A5'        # Static Lattice (Sand)

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_azure   = np.array(hex_to_rgba(C_AZURE)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_gold    = np.array(hex_to_rgba(C_GOLD)[:3])
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
# BASE GEOMETRY ARRAYS: THE SUBSTRATE
# ------------------------------------------------------------------
np.random.seed(269)
MAX_PARTICLES = 30000

# Substrate: 20000 nodes
# Node actuator: 10000 nodes reserved dynamically
px_base = np.random.uniform(-160, 160, 20000)
pz_base = np.random.uniform(-160, 160, 20000)
py_base = np.zeros(20000)

type_mask = np.zeros(MAX_PARTICLES, dtype=int) 
# 0 = Sand (X < 0)
# 1 = Ocean (X > 0)
# 2 = Focus Node Frame

env_mask = px_base > 0
type_mask[:20000][~env_mask] = 0
type_mask[:20000][env_mask] = 1
type_mask[20000:] = 2 # Stick figure nodes

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, p_x, p_y, p_z, c_arr, s_arr, a_arr, act_metric = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    bg_hex = C_BG
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)

    ax.set_xlim(-160, 160)
    ax.set_ylim(-260, 260)

    # Interface Threshold line (The exact boundary)
    ax.plot([0, 0], [-130, -50], color=C_DIM, lw=1.5, alpha=0.8, zorder=1)

    # Depth Sorting & Tracking Execution
    active = a_arr > 0.01
    if np.any(active):
        sort_idx = np.argsort(p_z[active])
        s_x = p_x[active][sort_idx]
        s_y = p_y[active][sort_idx]
        s_c = c_arr[active][sort_idx]
        s_size = s_arr[active][sort_idx]
        s_alpha = a_arr[active][sort_idx]

        rgba_colors = np.zeros((len(s_c), 4))
        rgba_colors[:, :3] = s_c
        rgba_colors[:, 3] = s_alpha

        # NO DOTS PROTOCOL: Convert raw scalar points into direct kinetic true vectors
        u1, v1 = s_x, s_y
        u2, v2 = s_x, s_y - (s_size * 0.1) # Extrude downwards slightly as a short vector
        segments = np.stack((np.column_stack((u1, v1)), np.column_stack((u2, v2))), axis=1)
        lc = LineCollection(segments, colors=rgba_colors, linewidths=s_size*0.5, zorder=10)
        ax.add_collection(lc)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_TEXT
    ui_col = C_DIM if t_sec < 4.5 else (C_MAGENTA if t_sec < 9.0 else C_GOLD)

    ax.text(-140, 250, "LG-269b // MACRO-ENGINEERING TENSOR: BIPEDAL VECTOR", color=txt_col, fontsize=11, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 238, "SYSTEM: PHASE INTERFACE / KINEMATIC WALK CYCLE", color=txt_col, fontsize=9, fontname='monospace', zorder=80)

    obj_str = "PHASE 1: SOLID VS FLUID INTERFACE"
    if 4.5 <= t_sec < 9.0: obj_str = "PHASE 2: KINEMATIC ACTUATOR FORGED"
    elif t_sec >= 9.0: obj_str = "PHASE 3: CONTINUOUS LOCOMOTION CYCLE"

    ax.text(-140, -180, f"OPERATIONAL PHASE: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)

    # Actuator Deflection Tracking
    ax.text(-140, -205, "ACTUATOR TENSION [PERPETUAL FALLING]", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 3, facecolor=C_DIM, zorder=80))
    tension_w = 280 * act_metric
    ax.add_patch(plt.Rectangle((-140, -210), tension_w, 3, facecolor=ui_col, zorder=81))

    # Phase Text Box
    ax.add_patch(plt.Rectangle((-140, 220), 280, 2, facecolor=ui_col, zorder=80))
    ax.text(140, 210, f"[{state_str}]", color=ui_col if (f%15<10) else C_BG, fontsize=14, fontname='monospace', weight='bold', ha='right', zorder=80)

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

        # Stable tracking camera moving parallel to the boundary
        cam_rx = np.pi/6 - 0.05
        cam_ry = np.pi/4 + (t_sec * 0.05) 
        cam_rz = 0.0

        c_arr = np.zeros((MAX_PARTICLES, 3))
        s_arr = np.ones(MAX_PARTICLES) * 4.0
        a_arr = np.ones(MAX_PARTICLES)

        curr_x = np.zeros(MAX_PARTICLES)
        curr_y = np.zeros(MAX_PARTICLES)
        curr_z = np.zeros(MAX_PARTICLES)

        # Map environment base
        curr_x[:20000] = px_base
        curr_z[:20000] = pz_base

        act_metric = 0.0

        # Stick figure construction arrays (10,000 points)
        node_pts = 10000
        bone_t = np.linspace(0, 1, 1400) 
        sf_x = np.zeros(node_pts)
        sf_y = np.zeros(node_pts)
        sf_z = np.zeros(node_pts)
        
        # Base scale properties for the Actuator
        sf_scale = 18.0
        n_z = 0.0 # Will track forward

        # -------------------------------------------------------------
        # PHASE LOGIC
        # -------------------------------------------------------------
        if t_sec < 4.5:
            state = "PHASE 1 :: BOUNDARY CONFLICT"

            # Sand is statically flat. Ocean rolls.
            wave_math = np.sin(t_sec * 4.0 + curr_x[:20000] * 0.1) * 8.0 * (type_mask[:20000] == 1)
            curr_y[:20000] = wave_math

            c_arr[:20000][type_mask[:20000] == 0] = c_dim
            c_arr[:20000][type_mask[:20000] == 1] = c_azure
            
            s_arr[:20000] = 3.0
            a_arr[20000:] = 0.0 

        elif t_sec < 9.0:
            state = "PHASE 2 :: THE MINIMAL ACTUATOR"
            prog = (t_sec - 4.5) / 4.5
            accel = prog ** 3 
            
            # Substrate continues
            wave_math = np.sin(t_sec * 4.0 + curr_x[:20000] * 0.1) * 8.0 * (type_mask[:20000] == 1)
            curr_y[:20000] = wave_math
            c_arr[:20000][type_mask[:20000] == 0] = c_dim
            c_arr[:20000][type_mask[:20000] == 1] = c_azure

            n_y = sf_scale * 3.0 * accel 
            head_y = n_y + sf_scale*1.2
            spine_y = n_y
            hip_y = n_y - sf_scale
            knee_y = hip_y - sf_scale*0.8
            foot_y = 0.0

            idx = 0
            # Head (Sphere approximation)
            u = np.random.uniform(0, 2*np.pi, 1600)
            v = np.arccos(np.random.uniform(-1, 1, 1600))
            sf_x[idx:idx+1600] = 0 + np.sin(v)*np.cos(u)*sf_scale*0.4
            sf_y[idx:idx+1600] = head_y + np.cos(v)*sf_scale*0.4
            sf_z[idx:idx+1600] = n_z + np.sin(v)*np.sin(u)*sf_scale*0.4
            idx += 1600

            # Spine
            sf_y[idx:idx+1400] = hip_y + (spine_y - hip_y)*bone_t
            idx += 1400
            
            # Legs
            sf_x[idx:idx+1400] = -sf_scale*0.2
            sf_y[idx:idx+1400] = foot_y + (hip_y - foot_y)*bone_t
            idx += 1400
            sf_x[idx:idx+1400] = sf_scale*0.2
            sf_y[idx:idx+1400] = foot_y + (hip_y - foot_y)*bone_t
            idx += 1400

            # Arms
            sf_x[idx:idx+1400] = -sf_scale*0.6
            sf_y[idx:idx+1400] = hip_y + (spine_y - hip_y)*bone_t
            idx += 1400
            sf_x[idx:idx+1400] = sf_scale*0.6
            sf_y[idx:idx+1400] = hip_y + (spine_y - hip_y)*bone_t
            idx += 1400

            curr_x[20000:] = sf_x
            curr_y[20000:] = sf_y
            curr_z[20000:] = sf_z

            c_arr[20000:] = c_magenta
            s_arr[20000:] = 5.0
            a_arr[20000:] = accel

            act_metric = prog * 0.5

        else:
            # PHASE 3: CONTINUOUS KINEMATIC WALK CYCLE
            state = "PHASE 3 :: KINEMATIC LOCOMOTION CYCLE"
            # Now calculating across the remainder of the 18.0s duration (9.0 seconds span)
            prog = (t_sec - 9.0) / 9.0
            
            # Substrate continues
            wave_math = np.sin(t_sec * 4.0 + curr_x[:20000] * 0.1) * 8.0 * (type_mask[:20000] == 1)
            curr_y[:20000] = wave_math
            c_arr[:20000][type_mask[:20000] == 0] = c_dim
            c_arr[:20000][type_mask[:20000] == 1] = c_azure

            # Z tracking progression (Maintains equivalent walking velocity)
            n_z = -60 + (prog * 186.2)

            # Mathematical Walk Cycle Engine
            cycle = t_sec * 10.0 
            stride = sf_scale * 0.7
            
            hip_y = (sf_scale * 2.0) - np.abs(np.sin(cycle))*sf_scale*0.2
            spine_y = hip_y + sf_scale
            head_y = spine_y + sf_scale*0.4

            l_foot_z = n_z + np.cos(cycle)*stride
            r_foot_z = n_z + np.cos(cycle + np.pi)*stride
            
            l_foot_y = max(0.0, -np.sin(cycle)*stride*0.5)
            r_foot_y = max(0.0, -np.sin(cycle + np.pi)*stride*0.5)

            l_arm_z = n_z - np.cos(cycle)*stride*0.8
            r_arm_z = n_z - np.cos(cycle + np.pi)*stride*0.8

            idx = 0
            u = np.random.uniform(0, 2*np.pi, 1600)
            v = np.arccos(np.random.uniform(-1, 1, 1600))
            sf_x[idx:idx+1600] = 0 + np.sin(v)*np.cos(u)*sf_scale*0.4
            sf_y[idx:idx+1600] = head_y + np.cos(v)*sf_scale*0.4
            sf_z[idx:idx+1600] = n_z + np.sin(v)*np.sin(u)*sf_scale*0.4
            idx += 1600

            sf_x[idx:idx+1400] = 0
            sf_y[idx:idx+1400] = hip_y + (spine_y - hip_y)*bone_t
            sf_z[idx:idx+1400] = n_z
            idx += 1400
            
            sf_x[idx:idx+1400] = -sf_scale*0.2 
            sf_y[idx:idx+1400] = l_foot_y + (hip_y - l_foot_y)*bone_t
            sf_z[idx:idx+1400] = l_foot_z + (n_z - l_foot_z)*bone_t
            idx += 1400

            sf_x[idx:idx+1400] = sf_scale*0.2 
            sf_y[idx:idx+1400] = r_foot_y + (hip_y - r_foot_y)*bone_t
            sf_z[idx:idx+1400] = r_foot_z + (n_z - r_foot_z)*bone_t
            idx += 1400

            sf_x[idx:idx+1400] = -sf_scale*0.5
            sf_y[idx:idx+1400] = hip_y + (spine_y - hip_y)*bone_t
            sf_z[idx:idx+1400] = l_arm_z + (n_z - l_arm_z)*bone_t
            idx += 1400

            sf_x[idx:idx+1400] = sf_scale*0.5
            sf_y[idx:idx+1400] = hip_y + (spine_y - hip_y)*bone_t
            sf_z[idx:idx+1400] = r_arm_z + (n_z - r_arm_z)*bone_t
            idx += 1400

            curr_x[20000:] = sf_x
            curr_y[20000:] = sf_y
            curr_z[20000:] = sf_z

            c_arr[20000:] = c_magenta
            s_arr[20000:] = 6.0
            a_arr[20000:] = 1.0

            # Footprint Logic (Trails perfectly alongside the actuator)
            footprint_mask = (type_mask[:20000] == 0) & (pz_base > -70) & (pz_base < n_z) & (np.abs(px_base) < 15.0)
            c_arr[:20000][footprint_mask] = c_gold
            s_arr[:20000][footprint_mask] = 5.0

            act_metric = 0.5 + np.abs(np.sin(cycle))*0.5 

        # Apply Global Tensor Matrix
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)

        # Dynamic Track: Camera follows the entity identically
        proj_x = rot_pts[:, 0]
        track_y = 30 - ((n_z + 60) * 0.2) if t_sec > 4.5 else 30
        proj_y = rot_pts[:, 1] + track_y
        z_depth = rot_pts[:, 2]

        yield (f, t_sec, state, proj_x, proj_y, z_depth, c_arr, s_arr, a_arr, act_metric)

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-269b: BIPEDAL VECTOR MATRIX [CORES: {cpu_cores}]")
    print(f"Executing: True Continuous Vector Architecture (No Dots)")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Macro-Engineering Yield Calculated. Engaging FFmpeg automation...")
    
    # Automated FFmpeg Compilation Execution
    ffmpeg_cmd = (
        'ffmpeg -y -framerate 60 -i frames_269b_bipedal/frame_%04d.png '
        '-c:v libx264 -preset fast -crf 14 -pix_fmt yuv420p -threads 2 '
        'logic_garden_269b_bipedal_vector.mp4'
    )
    subprocess.run(ffmpeg_cmd, shell=True)
    print("FFmpeg encoding complete. The MP4 array is secured on disk.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
