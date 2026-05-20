"""
SOVEREIGN CODE: logic_garden_276b_handstand_daylight.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) True Perspective Projection & Rigid IK
SCENE: LG-276b (Handstand Sequence / Daylight Protocol)
HOTFIX: Absolute Foot/Shadow Fusion & UI Frame Clearance
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
OUT_DIR = "frames_276b_handstand_daylight"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'        
C_CARBON    = np.array([0.05, 0.05, 0.08]) 
C_STEEL     = np.array([0.45, 0.50, 0.50]) 
C_CRIMSON   = np.array([0.75, 0.15, 0.15]) 
C_SHADOW    = np.array([0.80, 0.82, 0.83]) 
C_GRID      = np.array([0.70, 0.70, 0.75]) 

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

np.random.seed(276) # Lock random rigid layouts
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

# ------------------------------------------------------------------
# BIOLOGICAL INVERSE KINEMATICS & SPLINE TIMELINE
# ------------------------------------------------------------------
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

def get_pose(t):
    wp_t = np.array([0.0, 0.15, 0.25, 0.33, 0.45, 0.60, 0.70, 0.80, 0.90, 1.0])
    
    # KINEMATIC HOTFIX: Y-values elevated geometrically by ~3 units 
    # to maintain true sphere radius tangency with Y=0 baseplate.
    w_Lfoot = np.array([[0,3], [0,3], [0,3],    [5, 43],   [25,93], [25,93],  [5, 43],   [-5,3],    [0,3], [0,3]])
    w_Rfoot = np.array([[0,3], [0,3], [-15,13], [25, 78],  [25,93], [25,93],  [25, 78],  [-15,13],  [0,3], [0,3]])
    w_Hip   = np.array([[0,43],[0,43],[-15,23], [10, 43],  [25,55], [25,55],  [10, 43],  [-15,23],  [0,43], [0,43]])
    w_Shld  = np.array([[0,63],[0,63],[15,28],  [23, 33],  [25,33], [25,33],  [23, 33],  [15,28],   [0,63], [0,63]])
    w_Head  = np.array([[0,73],[0,73],[25,38],  [32, 28],  [35,23], [35,23],  [32, 28],  [25,38],   [0,73], [0,73]])
    
    # Hand target locks to 2.5 (Hand sphere radius = 2.5)
    w_Hand  = np.array([[0,33],[0,33],[25,2.5], [25,2.5],  [25,2.5],[25,2.5], [25,2.5],  [25,2.5],  [0,33], [0,33]])

    idx = np.searchsorted(wp_t, t)
    if idx == 0: idx = 1
    if idx == len(wp_t): idx = len(wp_t)-1
    
    t0, t1 = wp_t[idx-1], wp_t[idx]
    local_t = (t - t0) / (t1 - t0)
    st = 0.5 - 0.5 * np.cos(np.pi * local_t) 
    
    def blend(arr): return arr[idx-1] + (arr[idx] - arr[idx-1]) * st
    
    lf, rf, hip, shld, head, hand = blend(w_Lfoot), blend(w_Rfoot), blend(w_Hip), blend(w_Shld), blend(w_Head), blend(w_Hand)
    
    # Organic Ambient Sway
    sway = np.sin(t * np.pi * 4) * 0.8
    if 0.45 <= t <= 0.60: # Handstand stabilization
        lf[0] += np.sin(t * np.pi * 8) * 1.5 
        rf[0] += np.cos(t * np.pi * 8) * 1.5 
        hip[0] += np.sin(t * np.pi * 4) * 0.5
    elif t <= 0.15 or t >= 0.85: # Standing breath
        shld[1] += sway; hand[1] += sway; head[1] += sway
        
    return lf, rf, hip, shld, head, hand

# ------------------------------------------------------------------
# TRUE 3D PERSPECTIVE PIPELINE 
# ------------------------------------------------------------------
def project_perspective(p_x, p_y, p_z, cam_x, cam_y, cam_z):
    focal_length = 800.0
    dx, dy, dz = p_x - cam_x, p_y - cam_y, p_z - cam_z
    z_safe = np.maximum(dz, 1.0)
    
    proj_x = focal_length * (dx / z_safe)
    proj_y = focal_length * (dy / z_safe)
    proj_s = 25.0 * (focal_length / z_safe)
    return proj_x, proj_y, proj_s

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    t = f / float(TOTAL_FRAMES)
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    
    # HOTFIX: Raised Y-Limit mapping so the handstand clears the UI completely
    ax.set_xlim(-400, 400); ax.set_ylim(-150, 450) 

    ax.axhline(0, color='#ECF0F1', lw=3, zorder=-1)

    lf, rf, hip, shld, head, hand = get_pose(t)
    
    l_knee, lf = solve_ik_2d(hip, lf, 20.0, 20.0, bend_dir=1.0)
    r_knee, rf = solve_ik_2d(hip, rf, 20.0, 20.0, bend_dir=1.0)
    l_elb, l_hand = solve_ik_2d(shld, hand, 16.0, 16.0, bend_dir=-1.0)
    r_elb, r_hand = solve_ik_2d(shld, hand, 16.0, 16.0, bend_dir=-1.0)

    Z_HIP = 10.0; Z_SHLD = 14.0
    v_P = {
        'hip_l': np.array([hip[0], hip[1], -Z_HIP]), 'hip_r': np.array([hip[0], hip[1], Z_HIP]),
        'kn_l':  np.array([l_knee[0], l_knee[1], -Z_HIP]), 'kn_r':  np.array([r_knee[0], r_knee[1], Z_HIP]),
        'ft_l':  np.array([lf[0], lf[1], -Z_HIP*1.2]), 'ft_r':  np.array([rf[0], rf[1], Z_HIP*1.2]), 
        'sh_l':  np.array([shld[0], shld[1], -Z_SHLD]), 'sh_r':  np.array([shld[0], shld[1], Z_SHLD]),
        'el_l':  np.array([l_elb[0], l_elb[1], -Z_SHLD]), 'el_r':  np.array([r_elb[0], r_elb[1], Z_SHLD]),
        'hd_l':  np.array([l_hand[0], l_hand[1], -Z_SHLD]), 'hd_r':  np.array([r_hand[0], r_hand[1], Z_SHLD]),
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

    # Core
    add_cyl(v_P['spine_base'], v_P['spine_top'], 3.5, UNIT_CYL_1500, C_STEEL)
    add_sph(v_P['head'], 5.0, UNIT_SPH_500, C_CARBON)
    add_sph(v_P['spine_top'], 4.5, UNIT_SPH_500, C_CRIMSON)

    # Left Leg (Foot Radius 3.0)
    add_sph(v_P['hip_l'], 4.0, UNIT_SPH_500, C_CARBON)
    add_cyl(v_P['hip_l'], v_P['kn_l'], 3.0, UNIT_CYL_1000, C_CARBON)
    add_sph(v_P['kn_l'], 3.5, UNIT_SPH_500, C_CRIMSON)
    add_cyl(v_P['kn_l'], v_P['ft_l'], 2.5, UNIT_CYL_1000, C_STEEL)
    add_sph(v_P['ft_l'], 3.0, UNIT_SPH_500, C_CARBON)

    # Right Leg (Foot Radius 3.0)
    add_sph(v_P['hip_r'], 4.0, UNIT_SPH_500, C_CARBON)
    add_cyl(v_P['hip_r'], v_P['kn_r'], 3.0, UNIT_CYL_1000, C_CARBON)
    add_sph(v_P['kn_r'], 3.5, UNIT_SPH_500, C_CRIMSON)
    add_cyl(v_P['kn_r'], v_P['ft_r'], 2.5, UNIT_CYL_1000, C_STEEL)
    add_sph(v_P['ft_r'], 3.0, UNIT_SPH_500, C_CARBON)

    # Left Arm (Hand Radius 2.5)
    add_sph(v_P['sh_l'], 3.5, UNIT_SPH_500, C_CARBON)
    add_cyl(v_P['sh_l'], v_P['el_l'], 2.5, UNIT_CYL_1000, C_CARBON)
    add_sph(v_P['el_l'], 3.0, UNIT_SPH_500, C_CRIMSON)
    add_cyl(v_P['el_l'], v_P['hd_l'], 2.0, UNIT_CYL_1000, C_STEEL)
    add_sph(v_P['hd_l'], 2.5, UNIT_SPH_500, C_CARBON) # Hand sphere instantiated

    # Right Arm (Hand Radius 2.5)
    add_sph(v_P['sh_r'], 3.5, UNIT_SPH_500, C_CARBON)
    add_cyl(v_P['sh_r'], v_P['el_r'], 2.5, UNIT_CYL_1000, C_CARBON)
    add_sph(v_P['el_r'], 3.0, UNIT_SPH_500, C_CRIMSON)
    add_cyl(v_P['el_r'], v_P['hd_r'], 2.0, UNIT_CYL_1000, C_STEEL)
    add_sph(v_P['hd_r'], 2.5, UNIT_SPH_500, C_CARBON) # Hand sphere instantiated

    M_pts = np.hstack(pts)
    M_cols = np.vstack(cols)

    # 3. COMBINED SHADOW AND GROUND CLAMP
    # Shadow generation explicitly mapped before geometric clamp to prevent stretching
    shad_x = M_pts[0] + M_pts[1] * -1.8
    shad_y = np.zeros(M_pts.shape[1]) + 0.001 
    shad_z = M_pts[2] + M_pts[1] * -0.5

    # CONTACT HOTFIX: Hard mathematical clamp applied to Y limits.
    # Spherical contact points visibly flatten to align directly with the shadow matrix.
    M_pts[1] = np.maximum(M_pts[1], 0.001)

    all_x = np.concatenate([M_pts[0], shad_x])
    all_y = np.concatenate([M_pts[1], shad_y])
    all_z = np.concatenate([M_pts[2], shad_z])
    all_c = np.vstack([M_cols, np.full_like(M_cols, C_SHADOW)])
    all_a = np.concatenate([np.ones(M_pts.shape[1]), np.full(M_pts.shape[1], 0.35)])

    # 4. CAMERA PARALLAX ORBIT 
    cam_hz = t * 2 * np.pi
    c_x = np.sin(cam_hz) * 30.0 
    c_y = 25.0 + np.sin(cam_hz * 2) * 10.0 # Lifted slightly for horizon perspective
    c_z = -180.0 + np.cos(cam_hz) * 30.0

    p_x, p_y, p_s = project_perspective(all_x, all_y, all_z, c_x, c_y, c_z)

    # Z-Buffer Sort
    sort_idx = np.argsort(all_z)[::-1]
    
    rgba = np.zeros((len(all_x), 4))
    rgba[:, :3] = all_c[sort_idx]
    rgba[:, 3] = all_a[sort_idx]

    valid = (all_z[sort_idx] > c_z + 10.0)
    ax.scatter(p_x[sort_idx][valid], p_y[sort_idx][valid], s=p_s[sort_idx][valid], color=rgba[valid], edgecolors='none', zorder=10)

    # 5. DIAGNOSTIC TELEMETRY (Decoupled to transAxes for immunity from camera bounds)
    ax.add_patch(Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, facecolor=C_BG, edgecolor=C_CARBON, lw=2, zorder=80, clip_on=False))
    ax.text(0.5, 0.965, "LG-276b :: RIGID IK HANDSTAND KINEMATICS [DAYLIGHT]", transform=ax.transAxes, color=C_CARBON, fontsize=14, fontname='monospace', weight='bold', ha='center', va='center', zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 276b: INVERTED KINEMATICS HOTFIX [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Absolute Foot/Shadow Fusion // Boundary Cleared")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            pass
    print("Compilation Complete. Zero-Gap Baseline Achieved.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
