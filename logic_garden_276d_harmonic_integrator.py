"""
SOVEREIGN CODE: logic_garden_276d_harmonic_integrator.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) True Perspective Pipeline
SCENE: LG-276d_v2 (Unhurried 30s Loop: Walk -> Handstand -> Walk -> Roll -> Walk)
HOTFIX: Pendulum Arm Harmonics, Aggressive Focal Proximity, Fluid Transition Splines
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
DURATION = 30.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_276d_harmonic_sequence"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_CARBON    = np.array([0.06, 0.06, 0.09])
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

np.random.seed(2764)
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
    proj_s = 25.0 * (focal_length / z_safe)
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
# MASTER PARAMETRIC CONTINUUM (FLUID / UNHURRIED)
# ------------------------------------------------------------------
# Unhurried 30s Timeline:
# 0.0 ->  7.0 : Relaxed Walk (7s)
# 7.0 -> 13.0 : Handstand Phase (Smooth drop, invert, hold, deliberate recovery) (6s)
# 13.0-> 20.0 : Relaxed Walk (7s)
# 20.0-> 25.0 : Acrobatic Roll (Fluid, zero-snap fold, smooth momentum) (5s)
# 25.0-> 30.0 : Relaxed Walk, seamlessly linking to 0.0 (5s)

def smooth_blend(t, t0, t1):
    if t <= t0: return 0.0
    if t >= t1: return 1.0
    u = (t - t0) / (t1 - t0)
    return 0.5 - 0.5 * np.cos(np.pi * u)

def get_integrated_pose(t_sec):
    STRIDE_FREQ = 0.55  # Slow, unhurried, natural walk cycle
    STRIDE_LEN = 35.0
    SPEED_X = STRIDE_LEN * 2.0 * STRIDE_FREQ
    
    # Calculate smooth timeline envelope weights
    w_walk1 = 1.0 - smooth_blend(t_sec, 6.0, 7.5)
    w_hand  = smooth_blend(t_sec, 6.5, 7.5) * (1.0 - smooth_blend(t_sec, 12.5, 13.5))
    w_walk2 = smooth_blend(t_sec, 12.5, 13.5) * (1.0 - smooth_blend(t_sec, 19.5, 20.5))
    w_roll  = smooth_blend(t_sec, 19.5, 20.5) * (1.0 - smooth_blend(t_sec, 24.5, 25.5))
    w_walk3 = smooth_blend(t_sec, 24.5, 25.5)

    base_walk_v = SPEED_X * (w_walk1 + w_walk2 + w_walk3) + (SPEED_X*0.3 * w_hand) + (SPEED_X*1.2 * w_roll)
    global_x = t_sec * (SPEED_X * 0.85) 
    
    # ---------------------------------------------------------
    # STATE A: NATURAL HARMONIC WALK
    # ---------------------------------------------------------
    w_phase = (t_sec * STRIDE_FREQ) % 1.0
    # Hip drops gently at the maximum split, rises slightly when foot passes under
    w_hip_y = 39.0 + np.sin(w_phase * 4 * np.pi) * 2.5
    w_sh_y = w_hip_y + 24.0
    
    def walk_leg(ph):
        if ph < 0.5: # Planted, passing backward under body
            prog = ph / 0.5
            tx = global_x + (STRIDE_LEN * 0.9) - (prog * STRIDE_LEN * 1.8)
            ty = 3.0
        else: # Unhurried swinging arc forward
            prog = (ph - 0.5) / 0.5
            # Smooth cosine forward lift rather than sharp parabola
            st = 0.5 - 0.5 * np.cos(np.pi * prog)
            tx = global_x - (STRIDE_LEN * 0.9) + (st * STRIDE_LEN * 1.8)
            z_arc = np.sin(np.pi * prog)
            ty = 3.0 + z_arc * 16.0
        return np.array([tx, ty])
        
    w_LF = walk_leg(w_phase)
    w_RF = walk_leg((w_phase + 0.5) % 1.0)
    
    # Pendulum Harmonic Arms:
    # Relaxed swing. Hands drop slightly as they swing past the hips.
    arm_swing = 18.0
    sw_L = np.cos(w_phase * 2 * np.pi) * arm_swing
    sw_R = np.cos((w_phase + 0.5) * 2 * np.pi) * arm_swing
    
    # The hand's Y-coordinate gently arcs upward at the apex of the forward/backward swing
    arm_lift_L = np.abs(np.cos(w_phase * 2 * np.pi)) * 6.0
    arm_lift_R = np.abs(np.cos((w_phase + 0.5) * 2 * np.pi)) * 6.0

    w_HL = np.array([global_x - sw_L, w_sh_y - 28.0 + arm_lift_L])
    w_HR = np.array([global_x - sw_R, w_sh_y - 28.0 + arm_lift_R])

    P_WALK = {
        'Pitch': 0.0, 'Hip': np.array([global_x, w_hip_y]), 'Shld': np.array([global_x, w_sh_y]),
        'Head': np.array([global_x + 2.0, w_sh_y + 6.0]), # Slight forward tilt of head
        'LF': w_LF, 'RF': w_RF, 'HL': w_HL, 'HR': w_HR
    }
    
    # ---------------------------------------------------------
    # STATE B: FLUID HANDSTAND
    # ---------------------------------------------------------
    # Runs 7.0 -> 13.0 (6 seconds). 
    h_time = (t_sec - 7.0) / 6.0
    h_wp = np.array([
        [0.00,  0,   0, 39,   10, 3,  -10, 3,   -5, 12,  15, 12],
        [0.15,  55, 15, 23,   15, 3,    0, 3,   22,  5,  22,  5], # Deep, unhurried plant
        [0.35, 180, 22, 48,   18, 30,  30, 40,  22,  3,  22,  3], # Smooth rise
        [0.65, 180, 22, 48,   18, 30,  30, 40,  22,  3,  22,  3], # Extended deliberate hold
        [0.85, 300, 30, 28,   40,  3,  15, 18,  25, 15,  25, 15], # Slow control down
        [1.00, 360, 40, 39,   45,  3,  35,  3,   45, 22,  35, 22]
    ])
    
    idx_h = np.clip(np.searchsorted(h_wp[:, 0], h_time), 1, len(h_wp)-1)
    st_h = smooth_blend(h_time, h_wp[idx_h-1, 0], h_wp[idx_h, 0])
    h_val = h_wp[idx_h-1, 1:] + (h_wp[idx_h, 1:] - h_wp[idx_h-1, 1:]) * st_h
    
    h_pitch = h_val[0]
    h_hip = np.array([global_x, h_val[2]]) 
    h_shld = h_hip + np.array([24.0 * np.sin(np.radians(h_pitch)), 24.0 * np.cos(np.radians(h_pitch))])
    h_head = h_shld + np.array([6.0 * np.sin(np.radians(h_pitch)), 6.0 * np.cos(np.radians(h_pitch))])
    
    P_HAND = {
        'Pitch': h_pitch, 'Hip': h_hip, 'Shld': h_shld, 'Head': h_head,
        'LF': np.array([global_x - 10 + h_val[3], h_val[4]]),
        'RF': np.array([global_x - 10 + h_val[5], h_val[6]]),
        'HL': np.array([global_x - 10 + h_val[7], h_val[8]]),
        'HR': np.array([global_x - 10 + h_val[9], h_val[10]])
    }

    # ---------------------------------------------------------
    # STATE C: FLUID ACROBATIC ROLL
    # ---------------------------------------------------------
    # Runs 20.0 -> 25.0 (5 seconds)
    r_time = (t_sec - 20.0) / 5.0
    r_wp = np.array([
        [0.00,   0,   0, 39,    5,  3,   -5,  3,    5, 15,  -5, 15],
        [0.25, 140,  20, 22,   20,  3,  -10, 10,   30,  3,  30,  3], # Slow controlled tuck
        [0.50, 240,  45, 15,   20, 22,   50,  3,   30, 12,  30, 12], # Smooth back roll
        [0.75, 320,  60, 28,   65,  3,   55,  3,   70, 22,  70, 22],
        [1.00, 360,  70, 39,   75,  3,   60,  3,   75, 27,  60, 27]  
    ])
    
    idx_r = np.clip(np.searchsorted(r_wp[:, 0], r_time), 1, len(r_wp)-1)
    st_r = smooth_blend(r_time, r_wp[idx_r-1, 0], r_wp[idx_r, 0])
    r_val = r_wp[idx_r-1, 1:] + (r_wp[idx_r, 1:] - r_wp[idx_r-1, 1:]) * st_r
    
    r_pitch = r_val[0]
    r_hip = np.array([global_x, r_val[2]])
    r_shld = r_hip + np.array([24.0 * np.sin(np.radians(r_pitch)), 24.0 * np.cos(np.radians(r_pitch))])
    r_head = r_shld + np.array([6.0 * np.sin(np.radians(r_pitch)), 6.0 * np.cos(np.radians(r_pitch))])
    
    P_ROLL = {
        'Pitch': r_pitch, 'Hip': r_hip, 'Shld': r_shld, 'Head': r_head,
        'LF': np.array([global_x - 15 + r_val[3], r_val[4]]),
        'RF': np.array([global_x - 15 + r_val[5], r_val[6]]),
        'HL': np.array([global_x - 15 + r_val[7], r_val[8]]),
        'HR': np.array([global_x - 15 + r_val[9], r_val[10]])
    }

    # ---------------------------------------------------------
    # MASTER BLENDER (Harmonic Ouroboros)
    # ---------------------------------------------------------
    def blend_dict(d1, d2, w2):
        return {k: d1[k]*(1.0-w2) + d2[k]*w2 for k in d1}
    
    FINAL = P_WALK
    if w_hand > 0: FINAL = blend_dict(FINAL, P_HAND, w_hand)
    if w_roll > 0: FINAL = blend_dict(FINAL, P_ROLL, w_roll)

    # Dimensional Rigidity Lock
    L_THIGH, L_CALF = 21.0, 21.0
    L_BICEP, L_FORE = 17.0, 17.0

    l_knee, lf = solve_ik_2d(FINAL['Hip'], FINAL['LF'], L_THIGH, L_CALF, bend_dir=1.0)
    r_knee, rf = solve_ik_2d(FINAL['Hip'], FINAL['RF'], L_THIGH, L_CALF, bend_dir=1.0)
    
    # Bends arms backward typically, unless heavily inverted over the hands
    b_dir = -1.0 if np.cos(np.radians(FINAL['Pitch'])) > -0.4 else 1.0
    l_elb, hl = solve_ik_2d(FINAL['Shld'], FINAL['HL'], L_BICEP, L_FORE, bend_dir=b_dir)
    r_elb, hr = solve_ik_2d(FINAL['Shld'], FINAL['HR'], L_BICEP, L_FORE, bend_dir=b_dir)
    
    FINAL['LF'], FINAL['LKnee'] = lf, l_knee
    FINAL['RF'], FINAL['RKnee'] = rf, r_knee
    FINAL['HL'], FINAL['LElb'] = hl, l_elb
    FINAL['HR'], FINAL['RElb'] = hr, r_elb
    
    return FINAL, global_x

# ------------------------------------------------------------------
# INFINITE SCROLLING BASEPLATE
# ------------------------------------------------------------------
grid_x_local = np.random.uniform(-300, 300, 8000)
grid_z_local = np.random.uniform(0, 800, 8000)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    t_sec = f / float(FPS)
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    ax.set_xlim(-270, 270); ax.set_ylim(-480, 480) # Locked frame proportions
    ax.axhline(0, color='#ECF0F1', lw=3, zorder=-1)

    pose, global_x = get_integrated_pose(t_sec)

    # Construct the true 3D spatial matrix
    Z_HIP = 10.0; Z_SHLD = 15.0
    v_P = {
        'hip_l': np.array([pose['Hip'][0], pose['Hip'][1], -Z_HIP]), 'hip_r': np.array([pose['Hip'][0], pose['Hip'][1], Z_HIP]),
        'kn_l':  np.array([pose['LKnee'][0], pose['LKnee'][1], -Z_HIP]), 'kn_r':  np.array([pose['RKnee'][0], pose['RKnee'][1], Z_HIP]),
        'ft_l':  np.array([pose['LF'][0], pose['LF'][1], -Z_HIP*1.2]), 'ft_r':  np.array([pose['RF'][0], pose['RF'][1], Z_HIP*1.2]),
        'sh_l':  np.array([pose['Shld'][0], pose['Shld'][1], -Z_SHLD]), 'sh_r':  np.array([pose['Shld'][0], pose['Shld'][1], Z_SHLD]),
        'el_l':  np.array([pose['LElb'][0], pose['LElb'][1], -Z_SHLD]), 'el_r':  np.array([pose['RElb'][0], pose['RElb'][1], Z_SHLD]),
        'hd_l':  np.array([pose['HL'][0], pose['HL'][1], -Z_SHLD]), 'hd_r':  np.array([pose['HR'][0], pose['HR'][1], Z_SHLD]),
        'spine_base': np.array([pose['Hip'][0], pose['Hip'][1], 0]), 'spine_top': np.array([pose['Shld'][0], pose['Shld'][1], 0]),
        'head': np.array([pose['Head'][0], pose['Head'][1], 0])
    }

    pts, cols = [], []
    def add_cyl(pA, pB, rad, mesh, color):
        pts.append(transform_mesh(mesh, pA, pB, rad))
        cols.append(np.full((mesh.shape[1], 3), color))
    def add_sph(pA, rad, mesh, color):
        pts.append(transform_sphere(mesh, pA, rad))
        cols.append(np.full((mesh.shape[1], 3), color))

    add_cyl(v_P['spine_base'], v_P['spine_top'], 3.8, UNIT_CYL_1500, C_STEEL)
    add_sph(v_P['head'], 5.5, UNIT_SPH_500, C_CARBON)
    add_sph(v_P['spine_top'], 5.0, UNIT_SPH_500, C_CRIMSON)

    # Biomechanical Node Assembly
    for side, sign in [('_l', -1), ('_r', 1)]:
        add_sph(v_P['hip'+side], 4.5, UNIT_SPH_500, C_CARBON)
        add_cyl(v_P['hip'+side], v_P['kn'+side], 3.2, UNIT_CYL_1000, C_CARBON)
        add_sph(v_P['kn'+side], 4.0, UNIT_SPH_500, C_CRIMSON)
        add_cyl(v_P['kn'+side], v_P['ft'+side], 2.8, UNIT_CYL_1000, C_STEEL)
        add_sph(v_P['ft'+side], 3.5, UNIT_SPH_500, C_CARBON)

        add_sph(v_P['sh'+side], 4.2, UNIT_SPH_500, C_CARBON)
        add_cyl(v_P['sh'+side], v_P['el'+side], 2.8, UNIT_CYL_1000, C_CARBON)
        add_sph(v_P['el'+side], 3.2, UNIT_SPH_500, C_CRIMSON)
        add_cyl(v_P['el'+side], v_P['hd'+side], 2.4, UNIT_CYL_1000, C_STEEL)
        add_sph(v_P['hd'+side], 2.8, UNIT_SPH_500, C_CARBON)

    M_pts = np.hstack(pts)
    M_cols = np.vstack(cols)

    # 3. ABSOLUTE SHADOW FUSION (Rigorous Euclidean clamp)
    shad_x = M_pts[0] + M_pts[1] * -1.2
    shad_y = np.zeros(M_pts.shape[1]) + 0.001
    shad_z = M_pts[2] + M_pts[1] * -0.5

    # Eradicate sub-floor node piercing for true collision physics
    M_pts[1] = np.maximum(M_pts[1], 0.001)

    all_x = np.concatenate([M_pts[0], shad_x])
    all_y = np.concatenate([M_pts[1], shad_y])
    all_z = np.concatenate([M_pts[2], shad_z])
    all_c = np.vstack([M_cols, np.full_like(M_cols, C_SHADOW)])
    all_a = np.concatenate([np.ones(M_pts.shape[1]), np.full(M_pts.shape[1], 0.35)])

    # 4. CAMERA PARALLAX & MAXIMUM PROXIMITY LOCK (Fill the screen)
    c_x = global_x
    c_y = 35.0 + np.sin((t_sec/30.0) * 4 * np.pi) * 6.0
    c_z = -130.0 # Aggressive proximity push. Vastly expands the entity's relative scale on screen.

    mod_x = global_x % 200.0
    g_x = global_x + grid_x_local - mod_x
    g_y = np.full(8000, 0.001)
    g_z = grid_z_local

    all_x = np.concatenate([all_x, g_x])
    all_y = np.concatenate([all_y, g_y])
    all_z = np.concatenate([all_z, g_z])
    all_c = np.vstack([all_c, np.full((8000, 3), C_GRID)])
    
    g_a = np.clip(1.0 - (grid_z_local / 800.0), 0.0, 0.7)
    all_a = np.concatenate([all_a, g_a])

    p_x, p_y, p_s = project_perspective(all_x, all_y, all_z, c_x, c_y, c_z)
    p_s[-8000:] *= 0.25 # Scale down background grid

    # Depth sorting (Painter's algorithm)
    sort_idx = np.argsort(all_z)[::-1]
    rgba = np.zeros((len(all_x), 4))
    rgba[:, :3] = all_c[sort_idx]
    rgba[:, 3] = all_a[sort_idx]

    valid = (all_z[sort_idx] > c_z + 8.0)
    ax.scatter(p_x[sort_idx][valid], p_y[sort_idx][valid], s=p_s[sort_idx][valid], color=rgba[valid], edgecolors='none', zorder=10)

    # 5. UI ROUTING (Extreme Edge Clamping to prevent Obfuscation)
    state_str = "FLUID HARMONIC WALK"
    if 6.0 < t_sec < 13.5: state_str = "NATURAL INVERTED EQUILIBRIUM"
    elif 19.5 < t_sec < 25.5: state_str = "FLUID ROLL ACROBATICS"

    ax.add_patch(Rectangle((0, 0.96), 1, 0.04, transform=ax.transAxes, facecolor=C_BG, edgecolor=C_CARBON, lw=1, zorder=80, clip_on=False))
    ax.text(0.5, 0.98, "LG-276d(v2): MACRO-PROXIMITY FLUID HARMONICS", transform=ax.transAxes, color=C_CARBON, fontsize=12, fontname='monospace', weight='bold', ha='center', va='center', zorder=81)
    
    ax.add_patch(Rectangle((0, 0), 1, 0.04, transform=ax.transAxes, facecolor=C_BG, edgecolor=C_CARBON, lw=1, zorder=80, clip_on=False))
    ax.text(0.5, 0.02, f"\u0394t: {t_sec:05.2f}s // MATRIX: {state_str}", transform=ax.transAxes, color=C_CARBON, fontsize=12, fontname='monospace', weight='bold', ha='center', va='center', zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 276d(v2): FLUID HARMONIC MULTI-CYCLE [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Continuous True Integral Translation // Arm Pendulum Logic.")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            pass
    print("Compilation Complete. 1800 Frames Secured.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
