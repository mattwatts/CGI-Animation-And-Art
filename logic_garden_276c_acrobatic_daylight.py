"""
SOVEREIGN CODE: logic_garden_276c_acrobatic_daylight.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) True Perspective Pipeline
SCENE: LG-276c (Acrobatic Roll Loop / Daylight Protocol)
HOTFIX: Unbroken Substrate Tracking, Solid Rigid Scatters, Absolute Fusion
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
OUT_DIR = "frames_276c_acrobatic_daylight"
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

np.random.seed(276) # Lock structural nodes
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
# INFINITE SCROLLING BASEPLATE (World-Space Floor Matrix)
# ------------------------------------------------------------------
grid_x_local = np.random.uniform(-500, 500, 8000)
grid_z_local = np.random.uniform(0, 1000, 8000)

# ------------------------------------------------------------------
# DYNAMIC INVERSE KINEMATICS & ACROBATIC TIMELINE
# ------------------------------------------------------------------
# Predefined waypoint spline mapping exact physical limits of a forward roll
# T, Pitch(deg), HipX, HipY, LFX, LFY, RFX, RFY, HndX, HndY
waypoints = np.array([
    [0.00,   0,   0,  43,    0,  3,    0,  3,    0, 23],  # Start Stand
    [0.15,  45,  12,  32,   25,  3,    0,  3,   25, 15],  # Step and Lunge Drop
    [0.28, 135,  25,  35,   25,  3,  -10, 15,   40, 2.5], # Hands plant solidly (Radius 2.5 clamp)
    [0.42, 180,  40,  40,   20, 25,   15, 35,   40, 2.5], # Vertical Handstand Apex
    [0.55, 240,  55,  22,   30, 20,   65,  3,   45, 15],  # Spine Roll (Right Foot plants)
    [0.70, 315,  70,  30,   80,  3,   65,  3,   80, 20],  # Stand up pull (Left Foot hits at 80)
    [0.85, 360,  80,  43,   80,  3,   80,  3,   80, 23],  # Smooth completion
    [1.00, 360,  80,  43,   80,  3,   80,  3,   80, 23]   # Idle boundary snap
])

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

def get_kinematic_frame(t_total):
    # Setup O(1) multi-loop pacing
    T_CYCLE = 5.0
    cyl_idx = int(t_total / T_CYCLE)
    t = (t_total % T_CYCLE) / T_CYCLE
    base_x = cyl_idx * 80.0 # Origin drifts forward identically per cycle

    idx = np.searchsorted(waypoints[:, 0], t)
    if idx == 0: idx = 1
    if idx == len(waypoints): idx = len(waypoints)-1
    
    t0, t1 = waypoints[idx-1, 0], waypoints[idx, 0]
    local_t = (t - t0) / (t1 - t0)
    st = 0.5 - 0.5 * np.cos(np.pi * local_t) # Cosine physics drag 
    
    row = waypoints[idx-1, 1:] + (waypoints[idx, 1:] - waypoints[idx-1, 1:]) * st
    Pitch, H_x, H_y, LF_x, LF_y, RF_x, RF_y, Hnd_x, Hnd_y = row

    # Project local waypoints directly into absolute world-translation
    HipX = base_x + H_x
    HipY = H_y
    LF   = np.array([base_x + LF_x,  LF_y])
    RF   = np.array([base_x + RF_x,  RF_y])
    Hnd  = np.array([base_x + Hnd_x, Hnd_y])

    # Dynamic Spine calculation based on Angular Pitch Vector
    SpineL = 20.0
    p_rad = np.radians(Pitch)
    ShldX = HipX + SpineL * np.sin(p_rad)
    ShldY = HipY + SpineL * np.cos(p_rad)
    
    HeadX = ShldX + 5.0 * np.sin(p_rad)
    HeadY = ShldY + 5.0 * np.cos(p_rad)

    Hip  = np.array([HipX, HipY])
    Shld = np.array([ShldX, ShldY])
    Head = np.array([HeadX, HeadY])

    return Hip, Shld, Head, LF, RF, Hnd

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
    t_total = f / float(FPS)
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    
    # UI Cleared Frame Space
    ax.set_xlim(-400, 400); ax.set_ylim(-150, 450) 
    ax.axhline(0, color='#ECF0F1', lw=3, zorder=-1)

    # 1. EXTRACT SPATIAL KINEMATICS
    hip, shld, head, lf, rf, hand = get_kinematic_frame(t_total)
    
    # Resolve IK constraints dynamically (Length limits: Thigh=20, Calf=20, Bicep=16, Forearm=16)
    l_knee, lf = solve_ik_2d(hip, lf, 20.0, 20.0, bend_dir=1.0)
    r_knee, rf = solve_ik_2d(hip, rf, 20.0, 20.0, bend_dir=1.0)
    l_elb, l_hand = solve_ik_2d(shld, hand, 16.0, 16.0, bend_dir=-1.0)
    r_elb, r_hand = solve_ik_2d(shld, hand, 16.0, 16.0, bend_dir=-1.0)

    # Convert to 3D matrix
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

    # 2. BUILD VOLUMETRIC SCATTER ARRAYS
    pts, cols = [], []
    def add_cyl(pA, pB, rad, mesh, color):
        pts.append(transform_mesh(mesh, pA, pB, rad))
        cols.append(np.full((mesh.shape[1], 3), color))
        
    def add_sph(pA, rad, mesh, color):
        pts.append(transform_sphere(mesh, pA, rad))
        cols.append(np.full((mesh.shape[1], 3), color))

    add_cyl(v_P['spine_base'], v_P['spine_top'], 3.5, UNIT_CYL_1500, C_STEEL)
    add_sph(v_P['head'], 5.0, UNIT_SPH_500, C_CARBON)
    add_sph(v_P['spine_top'], 4.5, UNIT_SPH_500, C_CRIMSON)

    # Assembly (Feet Radius = 3.0, Hands Radius = 2.5)
    for side, sign in [('_l', -1), ('_r', 1)]:
        # Legs
        add_sph(v_P['hip'+side], 4.0, UNIT_SPH_500, C_CARBON)
        add_cyl(v_P['hip'+side], v_P['kn'+side], 3.0, UNIT_CYL_1000, C_CARBON)
        add_sph(v_P['kn'+side], 3.5, UNIT_SPH_500, C_CRIMSON)
        add_cyl(v_P['kn'+side], v_P['ft'+side], 2.5, UNIT_CYL_1000, C_STEEL)
        add_sph(v_P['ft'+side], 3.0, UNIT_SPH_500, C_CARBON)
        
        # Arms
        add_sph(v_P['sh'+side], 3.5, UNIT_SPH_500, C_CARBON)
        add_cyl(v_P['sh'+side], v_P['el'+side], 2.5, UNIT_CYL_1000, C_CARBON)
        add_sph(v_P['el'+side], 3.0, UNIT_SPH_500, C_CRIMSON)
        add_cyl(v_P['el'+side], v_P['hd'+side], 2.0, UNIT_CYL_1000, C_STEEL)
        add_sph(v_P['hd'+side], 2.5, UNIT_SPH_500, C_CARBON)

    M_pts = np.hstack(pts)
    M_cols = np.vstack(cols)

    # 3. ABSOLUTE SHADOW PROJECTION & ZERO-GAP BASEPLATE FUSION
    shad_x = M_pts[0] + M_pts[1] * -1.8
    shad_y = np.zeros(M_pts.shape[1]) + 0.001 
    shad_z = M_pts[2] + M_pts[1] * -0.5

    # HARD CLAMP: Prevent geometry from falling below Euclidean Floor
    M_pts[1] = np.maximum(M_pts[1], 0.001)

    all_x = np.concatenate([M_pts[0], shad_x])
    all_y = np.concatenate([M_pts[1], shad_y])
    all_z = np.concatenate([M_pts[2], shad_z])
    all_c = np.vstack([M_cols, np.full_like(M_cols, C_SHADOW)])
    all_a = np.concatenate([np.ones(M_pts.shape[1]), np.full(M_pts.shape[1], 0.35)])

    # 4. INFINITE GRID MATRIX GENERATION
    # The camera perfectly tracks the Hip. 
    # Drawing dots spatially guarantees visual flow without tearing.
    c_x = hip[0] # Exact Camera Parallax Tracking
    c_y = 20.0 + np.sin((t_total/10.0) * 2 * np.pi) * 8.0 
    c_z = -230.0 

    g_x = c_x + grid_x_local
    g_y = np.full(8000, 0.001)
    g_z = grid_z_local
    
    all_x = np.concatenate([all_x, g_x])
    all_y = np.concatenate([all_y, g_y])
    all_z = np.concatenate([all_z, g_z])
    
    g_c = np.full((8000, 3), C_GRID)
    all_c = np.vstack([all_c, g_c])
    
    g_a = np.clip(1.0 - (grid_z_local / 800.0), 0.0, 0.7)
    all_a = np.concatenate([all_a, g_a])

    # 5. RENDER TENSOR PROJECTION
    p_x, p_y, p_s = project_perspective(all_x, all_y, all_z, c_x, c_y, c_z)

    # Modulate dot size for grid (smallest) vs geometry
    p_s[-8000:] *= 0.25 

    sort_idx = np.argsort(all_z)[::-1]
    rgba = np.zeros((len(all_x), 4))
    rgba[:, :3] = all_c[sort_idx]
    rgba[:, 3] = all_a[sort_idx]

    valid = (all_z[sort_idx] > c_z + 10.0)
    ax.scatter(p_x[sort_idx][valid], p_y[sort_idx][valid], s=p_s[sort_idx][valid], color=rgba[valid], edgecolors='none', zorder=10)

    # 6. DIAGNOSTIC TELEMETRY (Anchored out of Camera Frame)
    ax.add_patch(Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, facecolor=C_BG, edgecolor=C_CARBON, lw=2, zorder=80, clip_on=False))
    ax.text(0.5, 0.965, "LG-276c :: DYNAMIC ACROBATIC O(1) TENSOR [DAYLIGHT]", transform=ax.transAxes, color=C_CARBON, fontsize=14, fontname='monospace', weight='bold', ha='center', va='center', zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 276c: ACROBATIC CYCLE [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Kinematic Forward Roll // Absolute Floor Contact")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            pass
    print("Compilation Complete. Zero-Gap Fusion Locked. Camera Path Solved.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
