"""
SOVEREIGN CODE: logic_garden_272d_radiance_sovereign_walk.py
SYSTEM: Python Multicore / O(1) Continuous Serialisation Loop
SCENE: Logic Garden 272d (Radiance: Sovereign Walk)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: True Perspective Projection Matrix / Euclidean Light Vectors / Parallax Ocean

[INSTRUCTION]: Continuous 18.0s seamless loop. Reference Image is Sacrosanct.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
RENDER_MODE = "RADIANCE_PHOTOREAL_TRUE_PERSPECTIVE"  
DURATION = 18.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_272d_radiance"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- EXTRACTED TARGET MATRIX PALETTE --------
C_SKY_TOP   = '#ECA888'        
C_SKY_BOT   = '#FFB75E'        
C_SUN       = '#FFFFFF'        
C_SUN_GLOW  = '#FFE066'        
C_OCEAN     = '#344A53'        # Dark Marine Parallax 
C_FOAM      = '#D0D8D9'        # Aerated Shore Break
C_SAND      = '#C58249'        # Wet Base Sand 
C_SAND_HI   = '#F2B670'        # Golden Specular Core
C_NODE      = '#201B1A'        
C_SHADOW    = '#5A331A'        # Grounded Euclidean Cast
C_FP        = '#381D0B'        # Carbon Footprint Void

def hex_to_rgba(hc, alpha=1.0):
    hc = hc.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_sand    = np.array(hex_to_rgba(C_SAND)[:3])
c_sand_hi = np.array(hex_to_rgba(C_SAND_HI)[:3])
c_ocean   = np.array(hex_to_rgba(C_OCEAN)[:3])
c_foam    = np.array(hex_to_rgba(C_FOAM)[:3])
c_node    = np.array(hex_to_rgba(C_NODE)[:3])
c_shadow  = np.array(hex_to_rgba(C_SHADOW)[:3])
c_fp      = np.array(hex_to_rgba(C_FP)[:3])

# ------------------------------------------------------------------
# TRUE 3D PERSPECTIVE PIPELINE
# ------------------------------------------------------------------
def project_perspective(p_x, p_y, p_z, base_size):
    # Camera anchored in foreground, elevated to frame Actuator
    cx, cy, cz = 0.0, 16.0, -50.0  
    focal_length = 600.0  

    dx = p_x - cx
    dy = p_y - cy
    dz = p_z - cz

    # Zero-division safety clamp
    z_safe = np.maximum(dz, 1.0)
    
    # Absolute Perspective Division
    proj_x = focal_length * (dx / z_safe)
    proj_y = focal_length * (dy / z_safe)
    
    # Scale physical particles by their focal depth
    proj_s = base_size * (focal_length / z_safe)
    
    return proj_x, proj_y, proj_s

# ------------------------------------------------------------------
# RIGID 3D MEMORY BUFFER (Eliminating Recursive Overflows)
# ------------------------------------------------------------------
np.random.seed(272)

BEACH_N = 60000
OCEAN_N = 30000
FP_N    = 4000  
NODE_N  = 8000
SHAD_N  = 8000
MAX_PARTICLES = BEACH_N + OCEAN_N + FP_N + NODE_N + SHAD_N

p_width = 800  # Expanded for perspective field-of-view

# Beach Substrate (-Z tracking) 0 to 150
bg_x = np.random.uniform(-p_width/2, p_width/2, BEACH_N)
bg_z = np.random.uniform(0, 150, BEACH_N)

# Ocean Substrate (+Z tracking) 150 to Deep Infinity (1000)
oc_x = np.random.uniform(-p_width/2, p_width/2, OCEAN_N)
oc_z = np.random.uniform(150, 1000, OCEAN_N)
shore_z = 150.0

# ------------------------------------------------------------------
# KINEMATICS & SERIALISATION LOGIC
# ------------------------------------------------------------------
walk_freq = 0.5 * np.pi  
stride_len = 16.0
sf_scale = 13.0
velocity = stride_len * walk_freq * 2.0 
wave_cycles = 5.0 

total_cycles = DURATION * walk_freq / np.pi 
num_footprints = 40 
fp_x_base = np.zeros(num_footprints)
fp_z_pos = np.zeros(num_footprints)
fp_spawn_times = np.zeros(num_footprints)

time_per_step = DURATION / (total_cycles * 2)
for i in range(num_footprints):
    is_left = (i % 2 != 0) 
    fp_z_pos[i] = 100 - (sf_scale * 0.25 if is_left else -sf_scale * 0.25)
    fp_spawn_times[i] = i * time_per_step 
    # Footprints anchor at X=0 at their spawn time, then ride the -X belt
    fp_x_base[i] = (fp_spawn_times[i] * velocity)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, p_x, p_y, p_z, c_arr, s_arr, a_arr = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    # Sky gradient starts exactly at mathematical Horizon (Y=0)
    gradient = np.linspace(0, 1, 256).reshape(-1, 1)
    gradient = np.hstack([gradient, gradient])
    ax.imshow(gradient, aspect='auto', cmap=matplotlib.colors.LinearSegmentedColormap.from_list('dawn', [C_SKY_BOT, C_SKY_TOP]), extent=[-350, 350, 0, 300], zorder=-10)
    
    # Faucet Singularity absolute lock at Y=0 (Perspective Vanishing Point)
    ax.add_patch(plt.Circle((0, 30), 120, color=C_SUN_GLOW, alpha=0.3, zorder=-7))
    ax.add_patch(plt.Circle((0, 12), 45, color=C_SUN_GLOW, alpha=0.6, zorder=-6))
    ax.add_patch(plt.Circle((0, 0), 22, color=C_SUN, alpha=1.0, zorder=-5))

    # Canvas constraints shifted to push the horizon (Y=0) above frame centre 
    ax.set_xlim(-350, 350)
    ax.set_ylim(-350, 200)

    # Z-Buffer Array sorting
    sort_idx = np.argsort(p_z)[::-1] # Reverse sort: Draw deepest Z first (Painters Algorithm)
    s_x = p_x[sort_idx]
    s_y = p_y[sort_idx]
    s_c = c_arr[sort_idx]
    s_size = s_arr[sort_idx]
    s_alpha = a_arr[sort_idx]

    rgba = np.zeros((len(s_c), 4))
    rgba[:, :3] = s_c
    rgba[:, 3] = s_alpha

    # Cull floating math anomalies
    valid = (s_y < 15) | (s_size > 0.1)
    ax.scatter(s_x[valid], s_y[valid], s=s_size[valid], color=rgba[valid], edgecolors='none', zorder=10)

    # Telemetry
    ax.add_patch(plt.Rectangle((-260, 160), 520, 32, facecolor='#000000', alpha=0.8, zorder=80))
    ax.text(0, 176, "LG-272d  ::  Radiance: Sovereign Walk", color='#FFFFFF', fontsize=14, fontname='monospace', weight='bold', ha='center', va='center', zorder=81)
    
    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# O(1) STRUCTURAL TARGET MATRIX 
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS

        c_arr = np.zeros((MAX_PARTICLES, 3))
        b_arr = np.zeros(MAX_PARTICLES) # base sizes before perspective scaling
        a_arr = np.ones(MAX_PARTICLES)

        curr_x = np.zeros(MAX_PARTICLES)
        curr_y = np.zeros(MAX_PARTICLES)
        curr_z = np.zeros(MAX_PARTICLES)

        ptr = 0

        # -------------------------------------------------------------
        # 1. FOREGROUND BEACH (Right to Left Lateral Belt -X)
        # -------------------------------------------------------------
        shift_bx = (bg_x - (t_sec * velocity)) % p_width - (p_width/2)
        curr_x[ptr:ptr+BEACH_N] = shift_bx
        curr_y[ptr:ptr+BEACH_N] = 0.0 # Absolute baseplate level
        curr_z[ptr:ptr+BEACH_N] = bg_z
        
        specular_b = np.clip(1.0 - (np.abs(shift_bx) / 80.0), 0.0, 1.0)
        
        for i in range(BEACH_N):
            c_arr[ptr+i] = c_sand * (1.0 - specular_b[i]*0.8) + c_sand_hi * specular_b[i]*0.8
            b_arr[ptr+i] = 12.0 + (specular_b[i] * 6.0) 
            a_arr[ptr+i] = 1.0
            
        ptr += BEACH_N

        # -------------------------------------------------------------
        # 2. PARALLAX OCEAN (Static X, Z-Vector Waves)
        # -------------------------------------------------------------
        # The ocean is anchored on X. It does NOT translate relative to ground. 
        curr_x[ptr:ptr+OCEAN_N] = oc_x
        curr_z[ptr:ptr+OCEAN_N] = oc_z
        
        # Wave propagation from Deep Z (+1000) traveling toward Shore Z (+150)
        wave_time = (t_sec / DURATION) * 2 * np.pi * wave_cycles
        wave_vector = (oc_z - shore_z) * 0.12 + wave_time 
        wave_height = np.sin(wave_vector) * 4.5
        
        # Suppress wave height linearly as it approaches the horizon vanish point
        depth_attenuation = np.clip(1.0 - ((oc_z - 150) / 600), 0.0, 1.0)
        curr_y[ptr:ptr+OCEAN_N] = wave_height * depth_attenuation
        
        specular_o = np.clip(1.0 - (np.abs(oc_x) / 80.0), 0.0, 1.0)

        for i in range(OCEAN_N):
            # Break criteria tied to depth limit directly behind Actuator
            is_breaking = (curr_y[ptr+i] > 2.0) and (oc_z[i] < shore_z + 40)
            if is_breaking:
                c_arr[ptr+i] = c_foam * (1.0 - specular_o[i]*0.1) + np.array(hex_to_rgba('#FFE066')[:3]) * specular_o[i]*0.1
                b_arr[ptr+i] = 16.0 
            else:
                c_arr[ptr+i] = c_ocean * (1.0 - specular_o[i]*0.3) + np.array(hex_to_rgba('#FFE066')[:3]) * specular_o[i]*0.3
                b_arr[ptr+i] = 14.0 

        ptr += OCEAN_N

        # -------------------------------------------------------------
        # 3. CARBON TRACE FOOTPRINTS (Tethered to -X tracking)
        # -------------------------------------------------------------
        for i in range(num_footprints):
            fp_curr_x = fp_x_base[i] - (t_sec * velocity)
            n_fp = 100
            
            curr_x[ptr:ptr+n_fp] = fp_curr_x + np.random.uniform(-1.5, 1.5, n_fp)
            curr_z[ptr:ptr+n_fp] = fp_z_pos[i] + np.random.uniform(-1.5, 1.5, n_fp)
            curr_y[ptr:ptr+n_fp] = 0.2  
            
            c_arr[ptr:ptr+n_fp] = c_fp 
            b_arr[ptr:ptr+n_fp] = 12.0 
            
            if t_sec >= fp_spawn_times[i]:
                fp_alpha = np.clip(1.0 - (np.abs(fp_curr_x) / 250.0), 0.0, 1.0) if fp_curr_x < 0 else 1.0
                a_arr[ptr:ptr+n_fp] = 0.0 if (fp_curr_x > 10.0) else (fp_alpha * 0.95)
            else:
                a_arr[ptr:ptr+n_fp] = 0.0
            
            ptr += n_fp

        # -------------------------------------------------------------
        # 4. EUCLIDEAN ACTUATOR (Photorealistic Hinge Mechanics)
        # -------------------------------------------------------------
        cycle = t_sec * walk_freq * 2.0
        n_x = 0.0 
        n_z = 100.0 # Physical depth placement on the Z-matrix

        hip_y = (sf_scale * 2.0) - np.abs(np.sin(cycle))*sf_scale*0.12 
        spine_y = hip_y + sf_scale
        head_y = spine_y + sf_scale*0.45

        l_foot_x = n_x + np.cos(cycle)*stride_len
        r_foot_x = n_x + np.cos(cycle + np.pi)*stride_len
        l_foot_y = max(0.0, -np.sin(cycle)*stride_len*0.4)
        r_foot_y = max(0.0, -np.sin(cycle + np.pi)*stride_len*0.4)

        # Precise anatomical knee calculation
        l_knee_x, r_knee_x = (n_x + l_foot_x) / 2.0, (n_x + r_foot_x) / 2.0
        l_knee_y = (hip_y + l_foot_y) / 2.0 + (l_foot_y)*0.4 
        r_knee_y = (hip_y + r_foot_y) / 2.0 + (r_foot_y)*0.4

        l_arm_x = n_x - np.cos(cycle)*stride_len*0.6
        r_arm_x = n_x - np.cos(cycle + np.pi)*stride_len*0.6

        bone_t = np.linspace(0, 1, 800)
        
        sf_x = np.zeros(NODE_N)
        sf_y = np.zeros(NODE_N)
        sf_z = np.zeros(NODE_N)
        b = 0
        
        u = np.random.uniform(0, 2*np.pi, 1600)
        v = np.arccos(np.random.uniform(-1, 1, 1600))
        sf_x[b:b+1600] = n_x + np.sin(v)*np.cos(u)*sf_scale*0.45
        sf_y[b:b+1600] = head_y + np.cos(v)*sf_scale*0.45
        sf_z[b:b+1600] = n_z + np.sin(v)*np.sin(u)*sf_scale*0.45
        b += 1600

        sf_x[b:b+800], sf_y[b:b+800], sf_z[b:b+800] = n_x, hip_y + (spine_y - hip_y)*bone_t, n_z
        b += 800
        
        sf_x[b:b+800] = n_x + (l_knee_x - n_x)*bone_t; sf_y[b:b+800] = hip_y + (l_knee_y - hip_y)*bone_t; sf_z[b:b+800] = n_z - sf_scale*0.25; b += 800
        sf_x[b:b+800] = l_knee_x + (l_foot_x - l_knee_x)*bone_t; sf_y[b:b+800] = l_knee_y + (l_foot_y - l_knee_y)*bone_t; sf_z[b:b+800] = n_z - sf_scale*0.25; b += 800

        sf_x[b:b+800] = n_x + (r_knee_x - n_x)*bone_t; sf_y[b:b+800] = hip_y + (r_knee_y - hip_y)*bone_t; sf_z[b:b+800] = n_z + sf_scale*0.25; b += 800
        sf_x[b:b+800] = r_knee_x + (r_foot_x - r_knee_x)*bone_t; sf_y[b:b+800] = r_knee_y + (r_foot_y - r_knee_y)*bone_t; sf_z[b:b+800] = n_z + sf_scale*0.25; b += 800

        sf_x[b:b+800] = l_arm_x + (n_x - l_arm_x)*bone_t; sf_y[b:b+800] = hip_y + (spine_y - hip_y)*bone_t; sf_z[b:b+800] = n_z - sf_scale*0.65; b += 800
        sf_x[b:b+800] = r_arm_x + (n_x - r_arm_x)*bone_t; sf_y[b:b+800] = hip_y + (spine_y - hip_y)*bone_t; sf_z[b:b+800] = n_z + sf_scale*0.65; b += 800

        curr_x[ptr:ptr+NODE_N], curr_y[ptr:ptr+NODE_N], curr_z[ptr:ptr+NODE_N] = sf_x, sf_y, sf_z
        c_arr[ptr:ptr+NODE_N] = c_node
        b_arr[ptr:ptr+NODE_N] = 10.0 
        ptr += NODE_N

        # -------------------------------------------------------------
        # 5. SACROSANCT RAY TRACING (The Target Shadow Vector)
        # -------------------------------------------------------------
        # Faucet Singularity is at +Z Infinity. Light travels in -Z direction.
        # Shadow projects perfectly away from light, towards negative Z (camera) and horizontally tracking the actuator geometry.
        # Strict diagonal Left (-X) pull mathematically replicates the provided optical image.
        shadow_z_stretch = 3.5 
        shadow_x_skew    = 1.5 
        
        curr_x[ptr:ptr+SHAD_N] = sf_x - ((sf_y) * shadow_x_skew) 
        curr_y[ptr:ptr+SHAD_N] = 0.3 
        curr_z[ptr:ptr+SHAD_N] = sf_z - ((sf_y) * shadow_z_stretch)
        
        c_arr[ptr:ptr+SHAD_N] = c_shadow
        b_arr[ptr:ptr+SHAD_N] = 12.0
        a_arr[ptr:ptr+SHAD_N] = 0.85 

        # -------------------------------------------------------------
        # FINAL EXECUTION: PERSPECTIVE TENSOR PROJECTION
        # -------------------------------------------------------------
        proj_x, proj_y, proj_s = project_perspective(curr_x, curr_y, curr_z, b_arr)

        yield (f, t_sec, proj_x, proj_y, curr_z, c_arr, proj_s, a_arr)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 272d: TRUE PERSPECTIVE SOVEREIGN [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Photorealistic Depth scaling / Optical Parallax / Correct Horizon")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Raw Euclidean Truth Secured.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
