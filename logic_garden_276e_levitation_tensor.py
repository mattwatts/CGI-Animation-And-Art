"""
SOVEREIGN CODE: logic_garden_276e_levitation_tensor.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) True Perspective Pipeline
SCENE: LG-276e (Laminar Levitation Array / Daylight Protocol)
HOTFIX: Seamless 10s Loop, Thermodynamic Ground Effect, Macro Focal Proximity
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Ellipse
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 10.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_276e_levitation"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_CARBON    = np.array([0.06, 0.06, 0.08])
C_STEEL     = np.array([0.45, 0.50, 0.50])
C_CRIMSON   = np.array([0.80, 0.15, 0.15])
C_SHADOW    = np.array([0.85, 0.86, 0.88])
C_GRID      = np.array([0.70, 0.70, 0.75])
C_CYAN      = np.array([0.00, 1.00, 1.00])
C_MAGENTA   = np.array([0.90, 0.30, 0.35])

# ------------------------------------------------------------------
# RIGID 3D PRIMITIVE GENERATORS
# ------------------------------------------------------------------
def make_unit_cylinder(dens):
    t = np.random.uniform(0, 1, dens)
    r = np.sqrt(np.random.uniform(0, 1, dens))
    theta = np.random.uniform(0, 2*np.pi, dens)
    return np.vstack((r * np.cos(theta), r * np.sin(theta), t))

def make_unit_sphere(dens):
    u = np.random.uniform(0, 2*np.pi, dens)
    v = np.arccos(np.random.uniform(-1, 1, dens))
    r = np.cbrt(np.random.uniform(0, 1, dens))
    return np.vstack((r*np.sin(v)*np.cos(u), r*np.cos(v), r*np.sin(v)*np.sin(u)))

np.random.seed(2765)
UNIT_CYL_1500 = make_unit_cylinder(1500)
UNIT_CYL_1000 = make_unit_cylinder(1000)
UNIT_SPH_500  = make_unit_sphere(500)

def transform_mesh(unit_mesh, p1, p2, radius):
    v = p2 - p1
    d = np.linalg.norm(v)
    if d < 1e-4: v = np.array([0, 1, 0]); d = 1e-4
    S = np.diag([radius, radius, d])
    v_dir = v / d
    up = np.array([0., 1., 0.]) if np.abs(v_dir[1]) < 0.99 else np.array([1., 0., 0.])
    x_axis = np.cross(up, v_dir)
    x_axis /= np.linalg.norm(x_axis)
    y_axis = np.cross(v_dir, x_axis)
    R = np.column_stack((x_axis, y_axis, v_dir))
    return (R @ S @ unit_mesh) + p1[:, np.newaxis]

def transform_sphere(unit_sphere, p1, radius):
    return (unit_sphere * radius) + p1[:, np.newaxis]

def project_perspective(p_x, p_y, p_z, cam_x, cam_y, cam_z):
    focal_length = 800.0
    dx, dy, dz = p_x - cam_x, p_y - cam_y, p_z - cam_z
    z_safe = np.maximum(dz, 1.0)
    proj_x = focal_length * (dx / z_safe)
    proj_y = focal_length * (dy / z_safe)
    proj_s = 20.0 * (focal_length / z_safe)
    return proj_x, proj_y, proj_s

def solve_ik_2d(p_root, p_target, l1, l2, bend_dir):
    v = p_target - p_root
    d = np.linalg.norm(v)
    if d >= l1 + l2:
        v = (v / d) * ((l1 + l2) * 0.999)
        p_target = p_root + v
        d = np.linalg.norm(v)
    elif d <= abs(l1 - l2):
        d = abs(l1 - l2) + 0.001
    cos_angle = np.clip((l1**2 + d**2 - l2**2) / (2 * l1 * d), -1.0, 1.0)
    beta = np.arccos(cos_angle)
    alpha = np.arctan2(v[1], v[0])
    theta = alpha + bend_dir * beta
    return p_root + np.array([l1 * np.cos(theta), l1 * np.sin(theta)]), p_target

# ------------------------------------------------------------------
# THERMODYNAMIC ION EXHAUST MATRIX
# ------------------------------------------------------------------
MAX_SPARKS = 2500
p_life = np.random.uniform(0.0, 1.0, MAX_SPARKS)
p_ang = np.random.uniform(0, 2*np.pi, MAX_SPARKS)
p_vel = np.random.uniform(100.0, 500.0, MAX_SPARKS)
p_type = np.random.choice([0, 1], MAX_SPARKS) # 0=Cyan, 1=Magenta
grid_x_local = np.random.uniform(-400, 400, 6000)
grid_z_local = np.random.uniform(0, 700, 6000)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    t_sec = f / float(FPS)
    tau = t_sec / 10.0
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    
    # Extreme Scale Confinement (Robot fills 85% of screen)
    ax.set_xlim(-160, 160)
    ax.set_ylim(-100, 420)
    ax.axhline(0, color='#EBF0F1', lw=4, zorder=-1)

    # 1. LEVITATION KINEMATICS
    # -------------------------------------------------
    # Center entity on screen, hovering above Y=0
    global_x = 0.0
    # Resonant Hover Harmonics (2 bobs per loop)
    hover_y = 55.0 + np.sin(tau * 4.0 * np.pi) * 8.0
    
    # Aerodynamic Pitch (Leaning forward into the velocity)
    pitch_rad = np.radians(15.0)
    
    hip = np.array([global_x, hover_y + 40.0])
    shld = hip + np.array([25.0 * np.sin(pitch_rad), 25.0 * np.cos(pitch_rad)])
    head = shld + np.array([8.0 * np.sin(pitch_rad), 8.0 * np.cos(pitch_rad)])
    
    # Surf/Skate Aerodynamic Stance
    # Left foot forward, right foot trailing
    lf = np.array([global_x + 18.0, hover_y - 8.0])
    rf = np.array([global_x - 18.0, hover_y])
    
    # Arms swept backward and out for stabilization
    # Left Arm (Foreground)
    hl = shld + np.array([12.0, -18.0])
    # Right Arm (Background)
    hr = shld + np.array([-18.0, -10.0])

    l_knee, lf = solve_ik_2d(hip, lf, 22.0, 22.0, bend_dir=1.0)
    r_knee, rf = solve_ik_2d(hip, rf, 22.0, 22.0, bend_dir=1.0)
    l_elb, hl = solve_ik_2d(shld, hl, 18.0, 18.0, bend_dir=-1.0)
    r_elb, hr = solve_ik_2d(shld, hr, 18.0, 18.0, bend_dir=-1.0)

    Z_HIP = 10.0; Z_SHLD = 16.0
    v_P = {
        'hip_l': np.array([hip[0], hip[1], -Z_HIP]), 'hip_r': np.array([hip[0], hip[1], Z_HIP]),
        'kn_l':  np.array([l_knee[0], l_knee[1], -Z_HIP]), 'kn_r':  np.array([r_knee[0], r_knee[1], Z_HIP]),
        'ft_l':  np.array([lf[0], lf[1], -Z_HIP*1.2]), 'ft_r':  np.array([rf[0], rf[1], Z_HIP*1.2]),
        'sh_l':  np.array([shld[0], shld[1], -Z_SHLD]), 'sh_r':  np.array([shld[0], shld[1], Z_SHLD]),
        'el_l':  np.array([l_elb[0], l_elb[1], -Z_SHLD]), 'el_r':  np.array([r_elb[0], r_elb[1], Z_SHLD]),
        'hd_l':  np.array([hl[0], hl[1], -Z_SHLD]), 'hd_r':  np.array([hr[0], hr[1], Z_SHLD]),
        'spine_base': np.array([hip[0], hip[1], 0]), 'spine_top': np.array([shld[0], shld[1], 0]),
        'head': np.array([head[0], head[1], 0])
    }

    pts, cols = [], []
    def add_cyl(pA, pB, rad, mesh, color):
        pts.append(transform_mesh(mesh, pA, pB, rad))
        cols.append(np.full((mesh.shape[1], 3), color))
    def add_sph(pA, rad, mesh, color):
        pts.append(transform_sphere(mesh, pA, rad))
        cols.append(np.full((mesh.shape[1], 3), color))

    add_cyl(v_P['spine_base'], v_P['spine_top'], 3.8, UNIT_CYL_1500, C_STEEL)
    add_sph(v_P['head'], 5.2, UNIT_SPH_500, C_CARBON)
    add_sph(v_P['spine_top'], 4.8, UNIT_SPH_500, C_CRIMSON)

    # Limbs
    for side, sign in [('_l', -1), ('_r', 1)]:
        add_sph(v_P['hip'+side], 4.5, UNIT_SPH_500, C_CARBON)
        add_cyl(v_P['hip'+side], v_P['kn'+side], 3.2, UNIT_CYL_1000, C_CARBON)
        add_sph(v_P['kn'+side], 3.8, UNIT_SPH_500, C_CRIMSON)
        add_cyl(v_P['kn'+side], v_P['ft'+side], 2.8, UNIT_CYL_1000, C_STEEL)
        add_sph(v_P['ft'+side], 3.4, UNIT_SPH_500, C_CARBON)

        add_sph(v_P['sh'+side], 4.0, UNIT_SPH_500, C_CARBON)
        add_cyl(v_P['sh'+side], v_P['el'+side], 2.8, UNIT_CYL_1000, C_CARBON)
        add_sph(v_P['el'+side], 3.2, UNIT_SPH_500, C_CRIMSON)
        add_cyl(v_P['el'+side], v_P['hd'+side], 2.2, UNIT_CYL_1000, C_STEEL)
        add_sph(v_P['hd'+side], 2.6, UNIT_SPH_500, C_CARBON)

    M_pts = np.hstack(pts)
    M_cols = np.vstack(cols)

    # 3. ABSOLUTE SHADOW (Hover Softening)
    # -------------------------------------------------
    # Because entity is suspended highly, shadow should be softer (alpha scaled)
    shad_x = M_pts[0] + M_pts[1] * -1.0
    shad_y = np.zeros(M_pts.shape[1]) + 0.001
    shad_z = M_pts[2] + M_pts[1] * -0.4

    M_pts[1] = np.maximum(M_pts[1], 0.001)

    all_x = np.concatenate([M_pts[0], shad_x])
    all_y = np.concatenate([M_pts[1], shad_y])
    all_z = np.concatenate([M_pts[2], shad_z])
    all_c = np.vstack([M_cols, np.full_like(M_cols, C_SHADOW)])
    all_a = np.concatenate([np.ones(M_pts.shape[1]), np.full(M_pts.shape[1], 0.15)]) # Soft shadow

    # 4. THERMODYNAMIC GROUND EFFECT (Repulsor Jets)
    # -------------------------------------------------
    # Eject down from boots, hit ground, spread out radially
    for idx_f, ft_pos in enumerate([v_P['ft_l'], v_P['ft_r']]):
        for i in range(MAX_SPARKS // 2):
            g_idx = i + (idx_f * (MAX_SPARKS//2))
            age = (tau - p_life[g_idx]) % 1.0
            
            # Fire down at high speed
            v_drop = 800.0 * age
            curr_py = ft_pos[1] - v_drop
            
            # If hits ground, redirect radially outward
            curr_px = ft_pos[0]
            curr_pz = ft_pos[2]
            
            if curr_py <= 0.001:
                curr_py = 0.001
                time_on_ground = age - (ft_pos[1] / 800.0)
                if time_on_ground > 0:
                    curr_px += np.cos(p_ang[g_idx]) * p_vel[g_idx] * time_on_ground
                    curr_pz += np.sin(p_ang[g_idx]) * p_vel[g_idx] * time_on_ground

            alpha = np.clip(1.0 - (age / 0.15), 0, 1)
            if alpha > 0.05:
                all_x = np.append(all_x, curr_px)
                all_y = np.append(all_y, curr_py)
                all_z = np.append(all_z, curr_pz)
                pcol = C_CYAN if p_type[g_idx] == 0 else C_MAGENTA
                all_c = np.vstack([all_c, pcol])
                all_a = np.append(all_a, alpha*0.8)

    # 5. CAMERA PARALLAX & EXTREME SPEED SUBSTRATE
    # -------------------------------------------------
    # Camera locked very close (Z=-110)
    c_x = 0.0
    c_y = 60.0 + np.sin(tau * 2 * np.pi) * 5.0
    c_z = -110.0 # Extreme macro logic 

    # Baseplate rockets backward to simulate massive forward velocity
    V_g = 2500.0 
    grid_offset = -(tau * 10 * V_g) % 200.0
    
    g_x = grid_x_local + grid_offset
    g_y = np.full(6000, 0.001)
    g_z = grid_z_local

    all_x = np.concatenate([all_x, g_x])
    all_y = np.concatenate([all_y, g_y])
    all_z = np.concatenate([all_z, g_z])
    all_c = np.vstack([all_c, np.full((6000, 3), C_GRID)])
    g_a = np.clip(1.0 - (grid_z_local / 700.0), 0.0, 0.6)
    all_a = np.concatenate([all_a, g_a])

    p_x, p_y, p_s = project_perspective(all_x, all_y, all_z, c_x, c_y, c_z)

    sort_idx = np.argsort(all_z)[::-1]
    rgba = np.zeros((len(all_x), 4))
    rgba[:, :3] = all_c[sort_idx]
    rgba[:, 3] = all_a[sort_idx]

    valid = (all_z[sort_idx] > c_z + 5.0)
    ax.scatter(p_x[sort_idx][valid], p_y[sort_idx][valid], s=p_s[sort_idx][valid], color=rgba[valid], edgecolors='none', zorder=10)

    # 6. UI ROUTING (Extreme Edge Clamping)
    # -------------------------------------------------
    ax.add_patch(Rectangle((0, 0.96), 1, 0.04, transform=ax.transAxes, facecolor=C_BG, edgecolor=C_CARBON, lw=1, zorder=80, clip_on=False))
    ax.text(0.5, 0.98, "LG-276e :: KINEMATIC GLIDE TENSOR // SUB-ATMOSPHERIC", transform=ax.transAxes, color=C_CARBON, fontsize=12, fontname='monospace', weight='bold', ha='center', va='center', zorder=81)
    
    ax.add_patch(Rectangle((0, 0), 1, 0.04, transform=ax.transAxes, facecolor=C_BG, edgecolor=C_CARBON, lw=1, zorder=80, clip_on=False))
    ax.text(0.5, 0.02, f"REPULSOR NODE: ACTIVE // V_g: {V_g} U/S // O(1) BASEPLATE", transform=ax.transAxes, color=C_CARBON, fontsize=12, fontname='monospace', weight='bold', ha='center', va='center', zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 276e: KINEMATIC GLIDE TENSOR [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Laminar Flight Mechanics // Absolute Frame Denial.")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            pass
    print("Compilation Complete. 600 Frames Secured.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
