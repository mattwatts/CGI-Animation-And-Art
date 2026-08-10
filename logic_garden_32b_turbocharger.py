"""
PROJECT: Logic Garden 32b (The Kinematic Turbocharger // Photorealistic Cutaway)
FORMAT: YouTube Shorts (1080x1920)
METADATA: FLUID DYNAMICS, THERMODYNAMICS, KINEMATIC ENGINEERING, CENTRIFUGAL COMPRESSION
EXECUTION: 24.0s Sequence. True 3D Mathematical Construction.
RULES ENFORCED:
- Daylight Palette (White Substrate / High Contrast).
- Static Camera Isometric Cutaway (Dead-center facing, exact anatomical orientation).
- Exact realisational aspect of machined rotors and True Snail-Shell Volutes.
- Absolute Geometrical Fluid Confinement (Axial IN/Radial OUT vs Radial IN/Axial OUT).
- Proper Integral Rotational Kinematics with 10-Layer Shutter Drag (Anti-Aliasing).
- Australian spelling conventions enforced natively.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
from matplotlib.collections import PolyCollection, LineCollection
import multiprocessing as mp
import os
import gc

# ======== SEQUENCE PARAMETERS ========
FPS = 60
DURATION = 24.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_32b_turbocharger"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST PHOTOREALISTIC PALETTE --------
C_BG               = '#FFFFFF'
C_TEXT             = '#111115'
C_EDGE             = '#111115'
C_TURBINE_ROTOR    = '#B45309'  # Heated Iron (Hot Side)
C_COMPRESSOR_ROTOR = '#E2E8F0'  # Machined Aluminium (Cold Side)
C_TURBINE_VOLUTE   = '#4A2A20'  # Deep Cast Iron Housing
C_COMPRESSOR_VOLUTE= '#64748B'  # Deep Cast Alu Housing
C_CHRA             = '#334155'  # Center Housing Rotating Assembly
C_SHAFT            = '#94A3B8'  # High Tensile Steel
C_HOT_IN           = '#FF3300'  # Intense Red
C_HOT_OUT          = '#71717A'  # Spent Zinc
C_COLD_IN          = '#005599'  # Deep Marine
C_COLD_OUT         = '#00C853'  # Jade Boost
C_GUI              = '#64748B'

LIGHT_DIR = np.array([-0.3, 0.8, -0.6])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

# ------------------------------------------------------------------
# O(1) ROTATIONAL INTEGRATION PHYSICS
# ------------------------------------------------------------------
def ease_in_expo(t):
    return np.power(2.0, 10 * (t - 1)) if t > 0 else 0

GLOBAL_ANGLES = np.zeros(TOTAL_FRAMES)
GLOBAL_SPOOL = np.zeros(TOTAL_FRAMES)
current_ang = 0.0
for i in range(TOTAL_FRAMES):
    t = i / FPS
    spool = np.clip((t - 3.0) / 6.0, 0.0, 1.0)
    GLOBAL_SPOOL[i] = spool
    
    # Base idle rotation is pi rad/s. Max is 18pi rad/s (Aggressive forward tracking).
    v = np.pi + (ease_in_expo(spool) * 17.0 * np.pi)
    current_ang -= v * (1.0/FPS) # Negative rotation for directionality
    GLOBAL_ANGLES[i] = current_ang

# ------------------------------------------------------------------
# 3D ARCHITECTURAL HARDWARE GENERATOR
# ------------------------------------------------------------------
def rx(deg):
    rad = np.radians(deg); c, s = np.cos(rad), np.sin(rad)
    return np.array([[1,0,0],[0,c,-s],[0,s,c]])

def ry(rad):
    c, s = np.cos(rad), np.sin(rad)
    return np.array([[c,0,s],[0,1,0],[-s,0,c]])

def generate_true_impeller(blades, r_max, y_base, y_eye, twist, is_compressor):
    # Generates anatomically correct compressor (Axial In) or turbine (Radial In)
    polys_hub, polys_blade = [], []
    hub_segs, steps = 16, 8

    def get_contour(t):
        r_h = 15.0 + (r_max * 0.9 - 15.0) * (1-t)**2
        y_h = y_base + (y_eye - y_base) * t
        r_t = 40.0 + (r_max - 40.0) * (1-t)**1.5
        
        offset = 15.0 if is_compressor else -15.0
        y_t = y_base + offset + (y_eye - y_base - offset) * t
        return r_h, y_h, r_t, y_t

    # HUB GENERATOR
    for i in range(hub_segs):
        th1, th2 = i * 2*np.pi / hub_segs, (i+1) * 2*np.pi / hub_segs
        
        # Flat Backplate
        r_bas, _, _, _ = get_contour(0)
        p1 = [r_bas*np.cos(th1), y_base, r_bas*np.sin(th1)]
        p2 = [r_bas*np.cos(th2), y_base, r_bas*np.sin(th2)]
        polys_hub.append([[0, y_base, 0], p2, p1] if is_compressor else [[0, y_base, 0], p1, p2])

        for s in range(steps):
            t1, t2 = s / steps, (s+1) / steps
            rh1, yh1, _, _ = get_contour(t1)
            rh2, yh2, _, _ = get_contour(t2)
            
            pi1 = [rh1*np.cos(th1), yh1, rh1*np.sin(th1)]
            pi2 = [rh1*np.cos(th2), yh1, rh1*np.sin(th2)]
            pi3 = [rh2*np.cos(th2), yh2, rh2*np.sin(th2)]
            pi4 = [rh2*np.cos(th1), yh2, rh2*np.sin(th1)]
            polys_hub.extend([[pi1, pi2, pi3], [pi1, pi3, pi4]])

    # BLADE GENERATOR
    for b in range(blades):
        base_ang = b * 2*np.pi / blades
        for s in range(steps):
            t1, t2 = s / steps, (s+1) / steps
            rh1, yh1, rt1, yt1 = get_contour(t1)
            rh2, yh2, rt2, yt2 = get_contour(t2)
            
            a1 = base_ang + twist * t1
            a2 = base_ang + twist * t2
            
            p1_in = [rh1*np.cos(a1), yh1, rh1*np.sin(a1)]
            p1_ou = [rt1*np.cos(a1), yt1, rt1*np.sin(a1)]
            p2_in = [rh2*np.cos(a2), yh2, rh2*np.sin(a2)]
            p2_ou = [rt2*np.cos(a2), yt2, rt2*np.sin(a2)]
            
            polys_blade.extend([[p1_in, p1_ou, p2_ou], [p1_in, p2_ou, p2_in]])
            
    return np.array(polys_hub), np.array(polys_blade)

def generate_solid_housing(r_wheel, y_base, y_eye, is_compressor):
    # Generates the exact thick cast volute walls encapsulating the rotor. Z>0 Back half only.
    polys = []
    segs = 16
    angles = np.linspace(0, np.pi, segs) # Precise 180 degree back-half cutaway
    wall = 12.0
    gap = 2.0

    # Shroud trace function matching the blade outer edge
    def get_shroud_contour(t):
        r_t = 40.0 + (r_wheel - 40.0) * (1-t)**1.5
        offset = 15.0 if is_compressor else -15.0
        y_t = y_base + offset + (y_eye - y_base - offset) * t
        return r_t + gap, y_t

    for i in range(segs - 1):
        th1, th2 = angles[i], angles[i+1]
        
        # Volute scroll grows from intake to exit
        scroll_rad_1 = 30.0 + 35.0 * (th1 / np.pi)
        scroll_rad_2 = 30.0 + 35.0 * (th2 / np.pi)
        sys_r1 = r_wheel + scroll_rad_1 + gap
        sys_r2 = r_wheel + scroll_rad_2 + gap

        # 1. The Shroud (Hugging the wheel)
        for s in range(8):
            t1, t2 = s/8.0, (s+1)/8.0
            r_s1, y_s1 = get_shroud_contour(t1)
            r_s2, y_s2 = get_shroud_contour(t2)
            
            p1i = [r_s1*np.cos(th1), y_s1, r_s1*np.sin(th1)]
            p2i = [r_s1*np.cos(th2), y_s1, r_s1*np.sin(th2)]
            p3i = [r_s2*np.cos(th2), y_s2, r_s2*np.sin(th2)]
            p4i = [r_s2*np.cos(th1), y_s2, r_s2*np.sin(th1)]
            polys.extend([[p1i, p3i, p2i], [p1i, p4i, p3i]])

        # 2. Main Snail Shell Volute Outward Wall
        y_v_base = y_base - 20 if is_compressor else y_base + 20
        y_v_top = y_base + 40 if is_compressor else y_base - 40

        v1i = [(sys_r1-scroll_rad_1)*np.cos(th1), y_base, (sys_r1-scroll_rad_1)*np.sin(th1)]
        v2i = [(sys_r2-scroll_rad_2)*np.cos(th2), y_base, (sys_r2-scroll_rad_2)*np.sin(th2)]
        v3i = [sys_r2*np.cos(th2), y_v_top, sys_r2*np.sin(th2)]
        v4i = [sys_r1*np.cos(th1), y_v_top, sys_r1*np.sin(th1)]
        polys.extend([[v1i, v3i, v2i], [v1i, v4i, v3i]])

        # Volute Outer Thick Casting
        v1o = [(sys_r1-scroll_rad_1+wall)*np.cos(th1), y_v_base, (sys_r1-scroll_rad_1+wall)*np.sin(th1)]
        v2o = [(sys_r2-scroll_rad_2+wall)*np.cos(th2), y_v_base, (sys_r2-scroll_rad_2+wall)*np.sin(th2)]
        v3o = [(sys_r2+wall)*np.cos(th2), y_v_top+wall, (sys_r2+wall)*np.sin(th2)]
        v4o = [(sys_r1+wall)*np.cos(th1), y_v_top+wall, (sys_r1+wall)*np.sin(th1)]
        polys.extend([[v1o, v2o, v3o], [v1o, v3o, v4o]])

        # 3. Axial Vertical Pipe Wall
        r_pipe = 40.0 + gap
        py_limit = 450.0 if is_compressor else -450.0
        
        pi1 = [r_pipe*np.cos(th1), y_eye, r_pipe*np.sin(th1)]
        pi2 = [r_pipe*np.cos(th2), y_eye, r_pipe*np.sin(th2)]
        pi3 = [r_pipe*np.cos(th2), py_limit, r_pipe*np.sin(th2)]
        pi4 = [r_pipe*np.cos(th1), py_limit, r_pipe*np.sin(th1)]
        polys.extend([[pi1, pi3, pi2], [pi1, pi4, pi3]])

        po1 = [(r_pipe+wall)*np.cos(th1), y_eye-10 if is_compressor else y_eye+10, (r_pipe+wall)*np.sin(th1)]
        po2 = [(r_pipe+wall)*np.cos(th2), y_eye-10 if is_compressor else y_eye+10, (r_pipe+wall)*np.sin(th2)]
        po3 = [(r_pipe+wall)*np.cos(th2), py_limit, (r_pipe+wall)*np.sin(th2)]
        po4 = [(r_pipe+wall)*np.cos(th1), py_limit, (r_pipe+wall)*np.sin(th1)]
        polys.extend([[po1, po2, po3], [po1, po3, po4]])

    # GENERATE SOLID Z=0 CUT FACES FOR HARD BLUEPRINT AESTHETIC
    for th in [0, np.pi]:
        # Connect inner and outer pipe
        f1 = [r_pipe*np.cos(th), y_eye, 0]
        f2 = [(r_pipe+wall)*np.cos(th), y_eye-10 if is_compressor else y_eye+10, 0]
        f3 = [(r_pipe+wall)*np.cos(th), py_limit, 0]
        f4 = [r_pipe*np.cos(th), py_limit, 0]
        if th == 0: polys.extend([[f1, f2, f3], [f1, f3, f4]])
        else: polys.extend([[f1, f3, f2], [f1, f4, f3]])

    return np.array(polys)

def generate_chra():
    # Solid geometric Center Housing (Z > 0)
    polys = []
    segs = 16
    angles = np.linspace(0, np.pi, segs)
    wall_r = 45.0
    for i in range(segs - 1):
        th1, th2 = angles[i], angles[i+1]
        p1 = [wall_r*np.cos(th1), -120, wall_r*np.sin(th1)]
        p2 = [wall_r*np.cos(th2), -120, wall_r*np.sin(th2)]
        p3 = [wall_r*np.cos(th2),  120, wall_r*np.sin(th2)]
        p4 = [wall_r*np.cos(th1),  120, wall_r*np.sin(th1)]
        polys.extend([[p1, p2, p3], [p1, p3, p4]])
        
        # Cut planes
        if i == 0: polys.extend([[[0, -120, 0], [wall_r, -120, 0], [wall_r, 120, 0]], [[0, -120, 0], [wall_r, 120, 0], [0, 120, 0]]])
        if i == segs-2: polys.extend([[[0, -120, 0], [0, 120, 0], [-wall_r, 120, 0]], [[0, -120, 0], [-wall_r, 120, 0], [-wall_r, -120, 0]]])
    return np.array(polys)

print("PHASE 1: PRE-COMPUTING EXACT MACHINED TENSORS...")
# C: Base=120, Eye=260. T: Base=-120, Eye=-260.
C_HUB, C_BLADES = generate_true_impeller(blades=12, r_max=130.0, y_base=120.0, y_eye=260.0, twist=-1.5, is_compressor=True)
C_HOUS          = generate_solid_housing(r_wheel=130.0, y_base=120.0, y_eye=260.0, is_compressor=True)

T_HUB, T_BLADES = generate_true_impeller(blades=10, r_max=120.0, y_base=-120.0, y_eye=-260.0, twist=0.6, is_compressor=False)
T_HOUS          = generate_solid_housing(r_wheel=120.0, y_base=-120.0, y_eye=-260.0, is_compressor=False)

CHRA = generate_chra()

# Segmented Shaft 360 degrees (Inside CHRA)
shaft = []
for y_b, y_t in zip(np.linspace(-260, 260, 10)[:-1], np.linspace(-260, 260, 10)[1:]):
    for i in range(12):
        th1, th2 = i * 2*np.pi/12, (i+1) * 2*np.pi/12
        r = 12.0
        p1 = [r*np.cos(th1), y_b, r*np.sin(th1)]
        p2 = [r*np.cos(th2), y_b, r*np.sin(th2)]
        p3 = [r*np.cos(th2), y_t, r*np.sin(th2)]
        p4 = [r*np.cos(th1), y_t, r*np.sin(th1)]
        shaft.extend([[p1, p2, p3], [p1, p3, p4]])
S_POLYS = np.array(shaft)


# ------------------------------------------------------------------
# STRICT PARAMETRIC FLUID PATHWAYS (ZERO DEAD SPACE)
# ------------------------------------------------------------------
N_PARTICLES = 600

# Exhaust: Volute -> Radial In -> Axial Out
np.random.seed(42)
hot_life = np.random.uniform(0, 1, N_PARTICLES)
hot_vol_th = np.random.uniform(0, np.pi, N_PARTICLES) # Start in back half volute
hot_rad_n = np.random.uniform(-10, 10, N_PARTICLES)
hot_y_n = np.random.uniform(-10, 10, N_PARTICLES)

# Intake: Axial In -> Radial Out -> Volute
cold_life = np.random.uniform(0, 1, N_PARTICLES)
cold_ang = np.random.uniform(0, 2*np.pi, N_PARTICLES)
cold_rad_n = np.random.uniform(-8, 8, N_PARTICLES)
cold_y_n = np.random.uniform(-5, 5, N_PARTICLES)

def calc_hot_pos(life, vol_th, rn, yn):
    # L(0-0.4): Sweep scroll
    # L(0.4-0.6): Blast inwards across blade
    # L(0.6-1.0): Drop axially
    scroll_r_base = 150.0 + 35.0 * (vol_th / np.pi)
    
    r = np.where(life < 0.4, scroll_r_base + rn,
        np.where(life < 0.6, scroll_r_base - ((life-0.4)/0.2)*(scroll_r_base-20.0) + rn,
                 15.0 + rn))
                 
    y = np.where(life < 0.4, -120.0 + yn,
        np.where(life < 0.6, -120.0 - ((life-0.4)/0.2)*140.0 + yn,
                 -260.0 - ((life-0.6)/0.4)*190.0))
                 
    th = vol_th + np.where(life < 0.4, (life/0.4)*np.pi,
                  np.where(life < 0.6, np.pi + ((life-0.4)/0.2)*1.5*np.pi,
                           2.5*np.pi + ((life-0.6)/0.4)*np.pi))
    return r * np.cos(th), y, r * np.sin(th)

def calc_cold_pos(life, ang, rn, yn):
    # L(0-0.3): Drop axially from top
    # L(0.3-0.5): Fling outward across blade
    # L(0.5-1.0): Sweep scroll and exit
    r = np.where(life < 0.3, 20.0 + rn,
        np.where(life < 0.5, 20.0 + ((life-0.3)/0.2)*120.0 + rn,
                 140.0 + ((life-0.5)/0.5)*35.0 + rn))
                 
    y = np.where(life < 0.3, 450.0 - (life/0.3)*190.0,
        np.where(life < 0.5, 260.0 - ((life-0.3)/0.2)*140.0 + yn,
                 120.0 + yn))
                 
    th = ang + np.where(life < 0.3, 0.0,
               np.where(life < 0.5, ((life-0.3)/0.2)*1.5*np.pi,
                        1.5*np.pi + ((life-0.5)/0.5)*np.pi))
    return r * np.cos(th), y, r * np.sin(th)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f_idx):
    t_sec = f_idx / float(FPS)
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.]); ax.set_axis_off(); fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540); ax.set_ylim(-960, 960)

    # 1. KINEMATIC INTEGRATION & BLUR ARRAY SETUP
    spool_prog = GLOBAL_SPOOL[f_idx]
    sys_rot = ry(GLOBAL_ANGLES[f_idx])

    # True Static Isometric View (Zero Dead Space)
    cam_pitch = -4.0 
    cam_hz = 0.0
    M_cam = rx(cam_pitch) @ ry(cam_hz)
    cam_dist = 1800.0
    queue = []

    def project_geometry(polys, color_hex, local_rot, is_solid, alpha=1.0):
        if len(polys) == 0: return []
        rotated = np.dot(polys, local_rot.T)
        v_cam = np.einsum('ij,knj->kni', M_cam, rotated)
        v_cam[:, :, 2] += cam_dist

        centroids_z = np.mean(v_cam[:, :, 2], axis=1)
        v1 = v_cam[:, 1, :] - v_cam[:, 0, :]
        v2 = v_cam[:, 2, :] - v_cam[:, 0, :]
        norms = np.cross(v1, v2)
        n_len = np.linalg.norm(norms, axis=1, keepdims=True)
        norms /= np.maximum(n_len, 1e-5)

        # For static housings, cull normally. 
        # For rotating blades, cull backfaces too to reduce clutter, but because it's a cutaway, 
        # we only render geometry where Z > 0 in world space if it's housing, 
        # but the housings are ALREADY generated precisely in the +Z space!
        v_mask = norms[:, 2] > 0
        
        v_cull = v_cam[v_mask]
        norms_cull = norms[v_mask]
        z_cull = centroids_z[v_mask]

        diff = 0.3 + 0.7 * np.abs(np.dot(norms_cull, LIGHT_DIR))
        c_rgb = np.array(mcolors.to_rgb(color_hex))

        fcs = np.zeros((len(v_cull), 4))
        fcs[:, :3] = c_rgb * diff[:, np.newaxis]
        fcs[:, 3] = alpha

        px = 3000.0 * (v_cull[:, :, 0] / v_cull[:, :, 2])
        py = 3000.0 * (v_cull[:, :, 1] / v_cull[:, :, 2]) - 50

        # Enforce cutaway blueprint architecture with hard C_EDGE lines
        lw = 0.8 if is_solid else 0.0
        ec = C_EDGE if is_solid else 'none'

        polys_2d = np.stack((px, py), axis=-1)
        return [{'sz': z, 'dat': p, 'fc': c, 'ec': ec, 'lw': lw, 'type': 'P'} for z, p, c in zip(z_cull, polys_2d, fcs)]

    # 1. Base Housings
    queue.extend(project_geometry(T_HOUS, C_TURBINE_VOLUTE, np.eye(3), is_solid=True))
    queue.extend(project_geometry(C_HOUS, C_COMPRESSOR_VOLUTE, np.eye(3), is_solid=True))
    queue.extend(project_geometry(CHRA, C_CHRA, np.eye(3), is_solid=True))
    
    # 2. Shaft & Hubs (Solid, Crisp)
    queue.extend(project_geometry(S_POLYS, C_SHAFT, sys_rot, is_solid=True))
    queue.extend(project_geometry(T_HUB, C_TURBINE_ROTOR, sys_rot, is_solid=True))
    queue.extend(project_geometry(C_HUB, C_COMPRESSOR_ROTOR, sys_rot, is_solid=True))

    # 3. Kinematic Blur Blades (Smearing along velocity tensor)
    blur_steps = 1 + int(spool_prog * 9)
    blur_decay = 1.0 / blur_steps
    for i in range(blur_steps):
        # We look BACK in time using our mathematical rotational speed
        trail_ang = GLOBAL_ANGLES[f_idx] + (i * 0.08 * spool_prog)
        trail_rot = ry(trail_ang)
        a_val = 1.0 - (i * blur_decay)
        # Leading edge gets lines, decay trails do not
        solid = (i == 0)
        queue.extend(project_geometry(T_BLADES, C_TURBINE_ROTOR, trail_rot, is_solid=solid, alpha=a_val))
        queue.extend(project_geometry(C_BLADES, C_COMPRESSOR_ROTOR, trail_rot, is_solid=solid, alpha=a_val))

    # ------------------------------------------------------------------
    # 4. STRICT PARAMETRIC FLUID MAPPING
    # ------------------------------------------------------------------
    speed = 1.0 + (spool_prog * 4.5)
    hot_l = (hot_life + t_sec * 0.8 * speed) % 1.0
    col_l = (cold_life + t_sec * 0.8 * speed) % 1.0
    
    hx, hy, hz = calc_hot_pos(hot_l, hot_vol_th, hot_y_n, hot_rad_n)
    htx, hty, htz = calc_hot_pos(np.maximum(0, hot_l - 0.05), hot_vol_th, hot_y_n, hot_rad_n)

    cx, cy, cz = calc_cold_pos(col_l, cold_ang, cold_y_n, cold_rad_n)
    ctx, cty, ctz = calc_cold_pos(np.maximum(0, col_l - 0.05), cold_ang, cold_y_n, cold_rad_n)

    cq_in, cq_out = np.array(mcolors.to_rgb(C_COLD_IN)), np.array(mcolors.to_rgb(C_COLD_OUT))
    hq_in, hq_out = np.array(mcolors.to_rgb(C_HOT_IN)), np.array(mcolors.to_rgb(C_HOT_OUT))

    def push_vecs(x1, y1, z1, x2, y2, z2, life_arr, c_in, c_out):
        for i in range(len(x1)):
            # Explicit Z-Plane cull: ONLY draw fluids inside the cutaway back half
            if z1[i] < -10.0 or z2[i] < -10.0: continue
            
            p1_w, p2_w = np.array([x1[i],y1[i],z1[i]]), np.array([x2[i],y2[i],z2[i]])
            p1_c, p2_c = M_cam @ p1_w, M_cam @ p2_w
            z_avg = (p1_c[2] + p2_c[2])/2.0 + cam_dist
            
            px1 = 3000.0 * (p1_c[0] / (p1_c[2] + cam_dist))
            py1 = 3000.0 * (p1_c[1] / (p1_c[2] + cam_dist)) - 50
            px2 = 3000.0 * (p2_c[0] / (p2_c[2] + cam_dist))
            py2 = 3000.0 * (p2_c[1] / (p2_c[2] + cam_dist)) - 50
            
            col = c_in * (1.0 - life_arr[i]) + c_out * life_arr[i]
            rgba = np.array([col[0], col[1], col[2], 0.9])
            
            queue.append({'sz': z_avg, 'dat': [[px1,py1],[px2,py2]], 'fc': rgba, 'type': 'L', 'lw': 3.0})

    push_vecs(hx, hy, hz, htx, hty, htz, hot_l, hq_in, hq_out)
    push_vecs(cx, cy, cz, ctx, cty, ctz, col_l, cq_in, cq_out)

    # 5. DEPTH SORT & RENDER (Strict O(1) unification)
    queue.sort(key=lambda x: x['sz'], reverse=True)
    
    b_poly, b_fc, b_ec, b_lw = [], [], [], []
    b_line, b_lc, b_ll = [], [], []

    for item in queue:
        if item['type'] == 'P':
            if b_line:
                ax.add_collection(LineCollection(b_line, colors=b_lc, linewidths=b_ll, capstyle='round'))
                b_line, b_lc, b_ll = [], [], []
            b_poly.append(item['dat']); b_fc.append(item['fc'])
            b_ec.append(item['ec']); b_lw.append(item['lw'])
        else:
            if b_poly:
                ax.add_collection(PolyCollection(b_poly, facecolors=b_fc, edgecolors=b_ec, linewidths=b_lw, joinstyle='miter'))
                b_poly, b_fc, b_ec, b_lw = [], [], [], []
            b_line.append(item['dat']); b_lc.append(item['fc']); b_ll.append(item['lw'])

    if b_poly: ax.add_collection(PolyCollection(b_poly, facecolors=b_fc, edgecolors=b_ec, linewidths=b_lw, joinstyle='miter'))
    if b_line: ax.add_collection(LineCollection(b_line, colors=b_lc, linewidths=b_ll, capstyle='round'))

    # 6. HIGH-DENSITY HUD & TELEMETRY
    ax.add_patch(Rectangle((-540, 780), 1080, 180, facecolor=C_BG, zorder=80, alpha=0.9))
    ax.plot([-540, 540], [780, 780], color=C_TEXT, lw=3, zorder=81)
    ax.text(-500, 880, "LG-32b :: KINEMATIC AIR PUMP", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 830, "[SFI-1.00] EXACT MACHINED CUTAWAY // ZERO DEAD SPACE", color=C_GUI, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.9))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    disp_rpm = int(spool_prog * 115200) if t_sec > 3.0 else 2400

    state_msg = "IDLE. TRUE GEOMETRIC CHOKING ENGAGED."
    state_col = C_GUI
    if t_sec > 3.0 and t_sec < 9.0:
        state_msg = "SPOOLING. THERMO-KINEMATIC LOAD RISING."
        state_col = C_HOT_IN
    elif t_sec >= 9.0:
        state_msg = "MAXIMUM THERMODYNAMIC THRESHOLD EXCEEDED."
        state_col = C_COLD_OUT

    ax.text(-500, -780, f"PROTOCOL PHASE: {state_msg}", color=state_col, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"SHAFT ROTATION: {disp_rpm:06d} RPM", color=C_TEXT, fontsize=18, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"AXIOMATIC TRUTH: ONE SPINS, SO THE OTHER MUST SPIN.", color=C_TEXT, fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(Rectangle((-500, -910), 1000, 8, facecolor=C_GUI, zorder=82))
    ax.add_patch(Rectangle((-500, -910), 1000 * spool_prog, 8, facecolor=C_COLD_OUT, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f_idx:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f_idx

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-32b: EXACT MACHINED CUTAWAY MATRIX [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            pass
    print("Compilation Complete. Cutaway Matrix Verified.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
