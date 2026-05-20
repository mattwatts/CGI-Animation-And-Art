"""
SOVEREIGN CODE: logic_garden_276_sovereign_centered.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) True Perspective Projection
SCENE: LG-276 (Sovereign Walk / Daylight Protocol Centered)
HOTFIX: Indestructible Dynamic Concatenation (Eliminates Shape Broadcast Errors)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 10.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_276_sovereign_centered"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'        # Absolute White Void
C_CARBON    = '#111115'        # High-density chassis core
C_STEEL     = '#7F8C8D'        # Machined limb cylinders
C_CRIMSON   = '#C0392B'        # Articulation joints
C_SHADOW    = '#D5DBDB'        # Crisp Euclidean shadow
C_GRID      = '#BDC3C7'        # Substrate tracking lines

def hex_to_rgba(hc, alpha=1.0):
    hc = hc.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_carbon  = np.array(hex_to_rgba(C_CARBON)[:3])
c_steel   = np.array(hex_to_rgba(C_STEEL)[:3])
c_crimson = np.array(hex_to_rgba(C_CRIMSON)[:3])
c_shadow  = np.array(hex_to_rgba(C_SHADOW)[:3])
c_grid    = np.array(hex_to_rgba(C_GRID)[:3])

# ------------------------------------------------------------------
# TRUE 3D PERSPECTIVE PIPELINE
# ------------------------------------------------------------------
def project_perspective(p_x, p_y, p_z, base_size):
    # Camera centered precisely on the actuator's core height
    cx, cy, cz = 0.0, 40.0, -120.0
    focal_length = 800.0

    dx = p_x - cx
    dy = p_y - cy
    dz = p_z - cz

    z_safe = np.maximum(dz, 1.0)
    proj_x = focal_length * (dx / z_safe)
    proj_y = focal_length * (dy / z_safe)
    proj_s = base_size * (focal_length / z_safe)

    return proj_x, proj_y, proj_s

# ------------------------------------------------------------------
# VOLUMETRIC SCATTER GENERATOR
# ------------------------------------------------------------------
def generate_cylinder_points(x1, y1, z1, x2, y2, z2, radius, num_points):
    """Generates a dense mathematical point cloud forming a 3D cylinder."""
    t = np.random.uniform(0, 1, num_points)
    cx = x1 + (x2 - x1) * t
    cy = y1 + (y2 - y1) * t
    cz = z1 + (z2 - z1) * t

    theta = np.random.uniform(0, 2*np.pi, num_points)
    r = np.sqrt(np.random.uniform(0, 1, num_points)) * radius
    
    px = cx + np.cos(theta) * r
    py = cy + np.sin(theta) * r
    pz = cz + np.cos(theta) * r * 0.5 
    return px, py, pz

# ------------------------------------------------------------------
# MEMORY BUFFER ARRANGEMENT
# ------------------------------------------------------------------
np.random.seed(2760)
GRID_N = 8000
grid_x_base = np.random.uniform(-400, 400, GRID_N)
grid_z_base = np.random.uniform(0, 800, GRID_N)

# ------------------------------------------------------------------
# KINEMATICS & SERIALISATION LOGIC
# ------------------------------------------------------------------
walk_freq = np.pi 
stride_len = 24.0
sf_scale = 18.0
velocity = stride_len * (walk_freq / np.pi) * 2.0 
wrap_dist = velocity * 2.0 

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, p_x, p_y, p_z, c_arr, s_arr, a_arr = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    
    # Exact 9:16 Aspect Ratio Bounds centering the entity securely
    ax.set_xlim(-270, 270)
    ax.set_ylim(-480, 480) 

    # Deep Painters Algorithm (Back-to-Front draw ordering)
    sort_idx = np.argsort(p_z)[::-1] 
    s_x = p_x[sort_idx]
    s_y = p_y[sort_idx]
    s_c = c_arr[sort_idx]
    s_size = s_arr[sort_idx]
    s_alpha = a_arr[sort_idx]

    rgba = np.zeros((len(s_c), 4))
    rgba[:, :3] = s_c
    rgba[:, 3] = s_alpha

    # Cull floating nodes behind the lens
    valid = (p_z[sort_idx] > -70.0)
    ax.scatter(s_x[valid], s_y[valid], s=s_size[valid], color=rgba[valid], edgecolors='none', zorder=10)

    # -------------------------------------------------------------
    # ABSOLUTE UI TELEMETRY (Anchored to Screen Edge via transAxes)
    # -------------------------------------------------------------
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, facecolor=C_BG, edgecolor=C_CARBON, lw=2, zorder=80))
    ax.text(0.5, 0.965, "LG-276 :: VOLUMETRIC KINEMATIC MATRIX", transform=ax.transAxes, color=C_CARBON, fontsize=20, fontname='monospace', weight='bold', ha='center', va='center', zorder=81)

    ax.add_patch(plt.Rectangle((0, 0), 1, 0.06, transform=ax.transAxes, facecolor=C_BG, edgecolor=C_CARBON, lw=2, zorder=80))
    ax.text(0.5, 0.03, f"SUBSTRATE VELOCITY: -X CONTINUOUS MODE // O(1) OUROBOROS SEAMLESS", transform=ax.transAxes, color=C_CARBON, fontsize=14, fontname='monospace', weight='bold', ha='center', va='center', alpha=0.6, zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# O(1) STRUCTURAL TARGET MATRIX (DYNAMIC CONCATENATION)
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS

        x_list, y_list, z_list = [], [], []
        c_list, b_list, a_list = [], [], []

        # -------------------------------------------------------------
        # 1. INFINITE SUBSTRATE GRID
        # -------------------------------------------------------------
        shift_x = (grid_x_base - (t_sec * velocity)) % wrap_dist - (wrap_dist/2)
        grid_x_final = np.copy(grid_x_base)
        grid_x_final[:] = shift_x + (np.floor(grid_x_base / wrap_dist) * wrap_dist)

        x_list.append(grid_x_final)
        y_list.append(np.zeros(GRID_N))
        z_list.append(grid_z_base)
        
        c_list.append(np.tile(c_grid, (GRID_N, 1)))
        b_list.append(np.full(GRID_N, 6.0))
        a_list.append(np.clip(1.0 - (grid_z_base / 600.0), 0.0, 0.5)) 

        # -------------------------------------------------------------
        # 2. VOLUMETRIC ACTUATOR (Centered Biomechanics)
        # -------------------------------------------------------------
        cycle = t_sec * walk_freq
        n_x = 0.0
        n_z = 80.0

        hip_y = (sf_scale * 2.2) - np.abs(np.sin(cycle))*sf_scale*0.15
        spine_y = hip_y + sf_scale*1.1
        head_y = spine_y + sf_scale*0.6

        l_foot_x = n_x + np.cos(cycle)*stride_len
        r_foot_x = n_x + np.cos(cycle + np.pi)*stride_len
        l_foot_y = max(0.0, -np.sin(cycle)*stride_len*0.6)
        r_foot_y = max(0.0, -np.sin(cycle + np.pi)*stride_len*0.6)

        l_knee_x, r_knee_x = (n_x + l_foot_x) / 2.0, (n_x + r_foot_x) / 2.0
        l_knee_y = (hip_y + l_foot_y) / 2.0 + (sf_scale*0.4) + (l_foot_y)*0.3
        r_knee_y = (hip_y + r_foot_y) / 2.0 + (sf_scale*0.4) + (r_foot_y)*0.3

        l_sh_x, r_sh_x = n_x, n_x
        l_sh_z, r_sh_z = n_z - sf_scale*0.45, n_z + sf_scale*0.45
        
        l_hand_x = n_x - np.cos(cycle)*stride_len*1.1
        r_hand_x = n_x - np.cos(cycle + np.pi)*stride_len*1.1
        l_hand_y = hip_y + max(0, -np.sin(cycle)*stride_len*0.2)
        r_hand_y = hip_y + max(0, -np.sin(cycle + np.pi)*stride_len*0.2)

        l_elbow_x, r_elbow_x = (l_sh_x + l_hand_x)/2.0, (r_sh_x + r_hand_x)/2.0
        l_elbow_y = (spine_y + l_hand_y) / 2.0 - (sf_scale*0.2)
        r_elbow_y = (spine_y + r_hand_y) / 2.0 - (sf_scale*0.2)

        vol_x, vol_y, vol_z = [], [], []
        vol_c, vol_b = [], []

        def add_segment(x1,y1,z1, x2,y2,z2, rad, dens, mat_c):
            px, py, pz = generate_cylinder_points(x1,y1,z1, x2,y2,z2, rad, dens)
            vol_x.extend(px); vol_y.extend(py); vol_z.extend(pz)
            vol_c.extend([mat_c]*dens); vol_b.extend([7.0]*dens)

        def add_joint(jx, jy, jz, rad, dens, mat_c=c_crimson):
            u = np.random.uniform(0, 2*np.pi, dens)
            v = np.arccos(np.random.uniform(-1, 1, dens))
            r = np.cbrt(np.random.uniform(0, 1, dens)) * rad
            vol_x.extend(jx + r*np.sin(v)*np.cos(u))
            vol_y.extend(jy + r*np.cos(v))
            vol_z.extend(jz + r*np.sin(v)*np.sin(u))
            vol_c.extend([mat_c]*dens); vol_b.extend([9.0]*dens)

        add_joint(n_x, head_y, n_z, sf_scale*0.4, 1500, c_carbon)
        add_segment(n_x, hip_y, n_z, n_x, spine_y, n_z, sf_scale*0.22, 1800, c_steel)
        add_joint(n_x, hip_y, n_z - sf_scale*0.2, sf_scale*0.25, 600)
        add_joint(n_x, hip_y, n_z + sf_scale*0.2, sf_scale*0.25, 600)

        add_segment(n_x, hip_y, n_z - sf_scale*0.2, l_knee_x, l_knee_y, n_z - sf_scale*0.2, sf_scale*0.18, 1200, c_carbon)
        add_joint(l_knee_x, l_knee_y, n_z - sf_scale*0.2, sf_scale*0.2, 500)
        add_segment(l_knee_x, l_knee_y, n_z - sf_scale*0.2, l_foot_x, l_foot_y, n_z - sf_scale*0.25, sf_scale*0.12, 1000, c_steel)
        add_joint(l_foot_x, l_foot_y, n_z - sf_scale*0.25, sf_scale*0.2, 400, c_carbon)

        add_segment(n_x, hip_y, n_z + sf_scale*0.2, r_knee_x, r_knee_y, n_z + sf_scale*0.2, sf_scale*0.18, 1200, c_carbon)
        add_joint(r_knee_x, r_knee_y, n_z + sf_scale*0.2, sf_scale*0.2, 500)
        add_segment(r_knee_x, r_knee_y, n_z + sf_scale*0.2, r_foot_x, r_foot_y, n_z + sf_scale*0.25, sf_scale*0.12, 1000, c_steel)
        add_joint(r_foot_x, r_foot_y, n_z + sf_scale*0.25, sf_scale*0.2, 400, c_carbon)

        add_joint(l_sh_x, spine_y, l_sh_z, sf_scale*0.25, 500)
        add_segment(l_sh_x, spine_y, l_sh_z, l_elbow_x, l_elbow_y, l_sh_z, sf_scale*0.14, 800, c_carbon)
        add_joint(l_elbow_x, l_elbow_y, l_sh_z, sf_scale*0.15, 300)
        add_segment(l_elbow_x, l_elbow_y, l_sh_z, l_hand_x, l_hand_y, l_sh_z, sf_scale*0.1, 700, c_steel)

        add_joint(r_sh_x, spine_y, r_sh_z, sf_scale*0.25, 500)
        add_segment(r_sh_x, spine_y, r_sh_z, r_elbow_x, r_elbow_y, r_sh_z, sf_scale*0.14, 800, c_carbon)
        add_joint(r_elbow_x, r_elbow_y, r_sh_z, sf_scale*0.15, 300)
        add_segment(r_elbow_x, r_elbow_y, r_sh_z, r_hand_x, r_hand_y, r_sh_z, sf_scale*0.1, 700, c_steel)

        # Convert to arrays and rigorously clamp Y against the physical substrate
        vx = np.array(vol_x)
        vy = np.maximum(np.array(vol_y), 0.001)
        vz = np.array(vol_z)
        vc = np.array(vol_c)
        vb = np.array(vol_b)
        va = np.ones(len(vx))

        x_list.append(vx); y_list.append(vy); z_list.append(vz)
        c_list.append(vc); b_list.append(vb); a_list.append(va)

        # -------------------------------------------------------------
        # 3. ABSOLUTE ZERO-POINT SHADOW FUSION
        # -------------------------------------------------------------
        shadow_x_skew    = -1.2
        shadow_z_stretch = -0.5

        shad_x = vx + (vy * shadow_x_skew)
        shad_y = np.zeros(len(vx)) 
        shad_z = vz + (vy * shadow_z_stretch)

        x_list.append(shad_x); y_list.append(shad_y); z_list.append(shad_z)
        c_list.append(np.tile(c_shadow, (len(vx), 1)))
        b_list.append(np.full(len(vx), 10.0))
        a_list.append(np.full(len(vx), 0.65))

        # -------------------------------------------------------------
        # FINAL EXECUTION: DYNAMIC TENSOR CONCATENATION & PROJECTION
        # -------------------------------------------------------------
        curr_x = np.concatenate(x_list)
        curr_y = np.concatenate(y_list)
        curr_z = np.concatenate(z_list)
        curr_c = np.concatenate(c_list)
        curr_b = np.concatenate(b_list)
        curr_a = np.concatenate(a_list)

        proj_x, proj_y, proj_s = project_perspective(curr_x, curr_y, curr_z, curr_b)

        yield (f, t_sec, proj_x, proj_y, curr_z, curr_c, proj_s, curr_a)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 276: SOVEREIGN WALK [CENTERED FRAME] [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Indestructible Dynamic Concatenation // Shadow Fusion")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Absolute Optical Alignment Secured. Matrix is Indestructible.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
