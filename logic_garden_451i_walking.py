"""
PROJECT: Logic Garden 451i (Exact Physical Construct // Walking Robotic Mannequin Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: ROBOTICS, BIOMECHANICS, WALK CYCLE, KINEMATICS, WIREFRAME, ENGINEERING, ANIMATION
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry.
- Translating Grid Vector: Matches kinematic foot placement mathematically (V=1.0m/s).
- Harmonic Walking Cycle: True anti-phase sinusoidal logic isolating structural robotic articulation.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from 115-degree front-quarter baseline.
- Daylight Palette (White Substrate / High-Contrast Edge Geometry).
- Purged Jargon. Australian spelling conventions (maths, colour, kilometres, synchronisation).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import multiprocessing as mp
import os
import gc

# ======== SEQUENCE PARAMETERS ========
DURATION = 24.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_451i_walking"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- SYNCHRONISATION KINEMATICS --------
VELOCITY = 1.0        # m/s target kinematic translation
STRIDE_FREQ = 5.0/6.0 # Exactly 20 cycles over 24 seconds for flawless seamless loops

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Translating Ground Plane)

C_HULL_MAIN = '#94A3B8'          # Heavy Slate (Skeletal Struts, Thorax, Core Mass)
C_HULL_DARK = '#475569'          # Machined Slate (Articulating Joint Spheres)
C_DETAILS   = '#1E293B'          # Carbon Slate (Extremities, Frame Mounts)
C_ACCENT    = '#E11D48'          # Kinematic Red (Optical nodes / Internal Mechanics)

# ------------------------------------------------------------------
# O(N) KINEMATIC WIREFRAME ENGINE
# ------------------------------------------------------------------
def project_3d_depth(x, y, z, cx, cy, cz, az_deg, el_deg=0):
    tx, ty, tz = x - cx, y - cy, z - cz
    az, el = np.radians(az_deg), np.radians(el_deg)
    
    x1 = tx * np.cos(az) - ty * np.sin(az)
    y1 = tx * np.sin(az) + ty * np.cos(az)
    z1 = tz
    
    y2 = y1 * np.cos(el) - z1 * np.sin(el)
    z2 = y1 * np.sin(el) + z1 * np.cos(el)
    
    return x1, z2, y2 

def append_segmented(lines_dict, key, xs, ys, zs):
    xs, ys, zs = list(xs), list(ys), list(zs)
    for i in range(len(xs) - 1):
        lines_dict[key].append(([xs[i], xs[i+1]], [ys[i], ys[i+1]], [zs[i], zs[i+1]]))

# ------------------------------------------------------------------
# GEOMETRIC PRIMITIVES (ROBOTIC TARGETING)
# ------------------------------------------------------------------
def add_sphere(lines_dict, col, cx, cy, cz, radius, rings=5, t_count=12):
    for p in np.linspace(-np.pi/2, np.pi/2, rings):
        r_s = radius * np.cos(p)
        z_s = radius * np.sin(p)
        t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
        ix = cx + r_s*np.cos(t); iy = cy + r_s*np.sin(t); iz = np.full_like(t, cz + z_s)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, np.pi, t_count//2, endpoint=False):
        p = np.linspace(-np.pi/2, np.pi/2, rings*2)
        ix = cx + (radius*np.cos(p))*np.cos(a); iy = cy + (radius*np.cos(p))*np.sin(a); iz = cz + radius*np.sin(p)
        append_segmented(lines_dict, col, list(ix), list(iy), list(iz))

def add_ellipsoid(lines_dict, col, cx, cy, cz, rx, ry, rz, rings=6, t_count=16):
    for p in np.linspace(-np.pi/2, np.pi/2, rings):
        r_x = rx * np.cos(p); r_y = ry * np.cos(p); z_s = rz * np.sin(p)
        t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
        ix = cx + r_x*np.cos(t); iy = cy + r_y*np.sin(t); iz = np.full_like(t, cz + z_s)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, np.pi, t_count//2, endpoint=False):
        p = np.linspace(-np.pi/2, np.pi/2, rings*2); c_p = np.cos(p); s_p = np.sin(p)
        ix = cx + rx * c_p * np.cos(a); iy = cy + ry * c_p * np.sin(a); iz = cz + rz * s_p
        append_segmented(lines_dict, col, list(ix), list(iy), list(iz))

def add_strut(lines_dict, col, p1, p2, radius, rings=3, t_count=8):
    p1, p2 = np.array(p1), np.array(p2)
    v = p2 - p1
    length = np.linalg.norm(v)
    if length < 0.001: return
    v_dir = v / length
    not_v = np.array([1.0, 0.0, 0.0])
    if abs(np.dot(v_dir, not_v)) > 0.99: not_v = np.array([0.0, 1.0, 0.0])
    n1 = np.cross(v_dir, not_v)
    n1 /= np.linalg.norm(n1)
    n2 = np.cross(v_dir, n1)
    
    steps = np.linspace(0, length, rings)
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    
    for s in steps:
        center = p1 + v_dir * s
        ix = center[0] + radius * (np.cos(t)*n1[0] + np.sin(t)*n2[0])
        iy = center[1] + radius * (np.cos(t)*n1[1] + np.sin(t)*n2[1])
        iz = center[2] + radius * (np.cos(t)*n1[2] + np.sin(t)*n2[2])
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        nx = radius * (np.cos(a)*n1[0] + np.sin(a)*n2[0])
        ny = radius * (np.cos(a)*n1[1] + np.sin(a)*n2[1])
        nz = radius * (np.cos(a)*n1[2] + np.sin(a)*n2[2])
        sx = p1[0] + nx + v_dir[0] * steps
        sy = p1[1] + ny + v_dir[1] * steps
        sz = p1[2] + nz + v_dir[2] * steps
        append_segmented(lines_dict, col, list(sx), list(sy), list(sz))

def rot_y(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (ROBOTIC LOCOMOTION CYCLE)
# ------------------------------------------------------------------
def generate_walking_mannequin(t_sec):
    lines = {
        'C_HULL_MAIN': [], 'C_HULL_DARK': [], 'C_DETAILS': [], 
        'C_ACCENT': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. TRANSLATING VECTOR FLOOR (Simulating 1.0 m/s traversal)
    # ==============================================================================
    Z_FLOOR = 0.0
    travel_offset = (t_sec * VELOCITY) % 2.0
    
    gx_range = np.linspace(-3.0, 3.0, 13)
    gy_range = np.linspace(-3.0, 3.0, 13)
    for gx in gx_range: 
        append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx - travel_offset), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: 
        append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. DYNAMIC HARMONICS & STRUCTURAL BOB
    # ==============================================================================
    phi = t_sec * STRIDE_FREQ * 2 * np.pi
    
    # Mathematical Z-axis compensation replicating bipedal gait bounds
    bob = 0.03 * np.sin(2 * phi)
    
    # Core Centroids
    Z_PELVIS  = 1.02 + bob
    Z_THORAX  = 1.33 + bob
    Z_CRANIUM = 1.68 + bob

    HIP_R = np.array([0.0, -0.13, 0.92 + bob])
    HIP_L = np.array([0.0,  0.13, 0.92 + bob])
    SH_R  = np.array([0.0, -0.22, 1.45 + bob])
    SH_L  = np.array([0.0,  0.22, 1.45 + bob])

    # Core Masses
    add_ellipsoid(lines, 'C_HULL_MAIN', 0.0, 0.0, Z_CRANIUM, 0.10, 0.08, 0.11, rings=6, t_count=16)
    add_ellipsoid(lines, 'C_HULL_MAIN', 0.0, 0.0, Z_THORAX, 0.12, 0.16, 0.16, rings=6, t_count=16)
    add_ellipsoid(lines, 'C_HULL_MAIN', 0.0, 0.0, Z_PELVIS, 0.11, 0.14, 0.10, rings=6, t_count=16)

    # Core Spines & Clavicles
    add_strut(lines, 'C_DETAILS', (0.0, 0.0, Z_PELVIS+0.1), (0.0, 0.0, Z_THORAX+0.17), radius=0.03)
    add_strut(lines, 'C_DETAILS', SH_R, (0.0, 0.0, Z_THORAX+0.12), radius=0.02)
    add_strut(lines, 'C_DETAILS', SH_L, (0.0, 0.0, Z_THORAX+0.12), radius=0.02)

    # ==============================================================================
    # 3. KINEMATIC LEG ARRAYS
    # ==============================================================================
    # Right Leg (Anti-clockwise/Positive Y-rotation pivots backward. Forward swing is Negative theta.)
    theta_hip_R = -0.5 * np.sin(phi)
    # Knee bends backward explicitly (Positive theta) during forward swing
    theta_knee_R = 0.8 * np.maximum(0, np.cos(phi))

    KNEE_R   = HIP_R  + rot_y(theta_hip_R) @ np.array([0.0, -0.01, -0.46])
    ANKLE_R  = KNEE_R + rot_y(theta_hip_R + theta_knee_R) @ np.array([-0.02, 0.0, -0.36])
    FOOT_R_F = ANKLE_R + rot_y(theta_hip_R + theta_knee_R) @ np.array([0.15, -0.02, -0.08])
    FOOT_R_B = ANKLE_R + rot_y(theta_hip_R + theta_knee_R) @ np.array([-0.05, 0.01, -0.08])

    # Left Leg (180 degree offset)
    theta_hip_L = -0.5 * np.sin(phi + np.pi)
    theta_knee_L = 0.8 * np.maximum(0, np.cos(phi + np.pi))

    KNEE_L   = HIP_L  + rot_y(theta_hip_L) @ np.array([0.0, 0.01, -0.46])
    ANKLE_L  = KNEE_L + rot_y(theta_hip_L + theta_knee_L) @ np.array([-0.02, 0.0, -0.36])
    FOOT_L_F = ANKLE_L + rot_y(theta_hip_L + theta_knee_L) @ np.array([0.15, 0.02, -0.08])
    FOOT_L_B = ANKLE_L + rot_y(theta_hip_L + theta_knee_L) @ np.array([-0.05, -0.01, -0.08])

    add_sphere(lines, 'C_HULL_DARK', *HIP_R, 0.045); add_sphere(lines, 'C_HULL_DARK', *HIP_L, 0.045)
    add_sphere(lines, 'C_HULL_DARK', *KNEE_R, 0.040); add_sphere(lines, 'C_HULL_DARK', *KNEE_L, 0.040)
    add_sphere(lines, 'C_HULL_DARK', *ANKLE_R, 0.030); add_sphere(lines, 'C_HULL_DARK', *ANKLE_L, 0.030)

    add_strut(lines, 'C_HULL_MAIN', HIP_R, KNEE_R, radius=0.055, rings=4)
    add_strut(lines, 'C_HULL_MAIN', KNEE_R, ANKLE_R, radius=0.045, rings=4)
    add_strut(lines, 'C_DETAILS', ANKLE_R, FOOT_R_F, radius=0.03, rings=3)
    add_strut(lines, 'C_DETAILS', ANKLE_R, FOOT_R_B, radius=0.025, rings=2)

    add_strut(lines, 'C_HULL_MAIN', HIP_L, KNEE_L, radius=0.055, rings=4)
    add_strut(lines, 'C_HULL_MAIN', KNEE_L, ANKLE_L, radius=0.045, rings=4)
    add_strut(lines, 'C_DETAILS', ANKLE_L, FOOT_L_F, radius=0.03, rings=3)
    add_strut(lines, 'C_DETAILS', ANKLE_L, FOOT_L_B, radius=0.025, rings=2)

    # ==============================================================================
    # 4. KINEMATIC ARM ARRAYS (Anti-phase to legs)
    # ==============================================================================
    # Right Arm (Counter-swing to Right Leg)
    theta_sh_R = 0.4 * np.sin(phi)
    # Elbows bend forward natively (negative theta relative to humorous)
    theta_el_R = -0.15 - 0.3 * np.maximum(0, -np.sin(phi))

    ELBOW_R = SH_R + rot_y(theta_sh_R) @ np.array([0.0, -0.06, -0.30])
    WRIST_R = ELBOW_R + rot_y(theta_sh_R + theta_el_R) @ np.array([0.05, -0.04, -0.30])
    HAND_R  = WRIST_R + rot_y(theta_sh_R + theta_el_R) @ np.array([0.08, -0.02, -0.20])

    # Left Arm
    theta_sh_L = 0.4 * np.sin(phi + np.pi)
    theta_el_L = -0.15 - 0.3 * np.maximum(0, -np.sin(phi + np.pi))

    ELBOW_L = SH_L + rot_y(theta_sh_L) @ np.array([0.0, 0.06, -0.30])
    WRIST_L = ELBOW_L + rot_y(theta_sh_L + theta_el_L) @ np.array([0.05, 0.04, -0.30])
    HAND_L  = WRIST_L + rot_y(theta_sh_L + theta_el_L) @ np.array([0.08, 0.02, -0.20])

    add_sphere(lines, 'C_HULL_DARK', *SH_R, 0.045); add_sphere(lines, 'C_HULL_DARK', *SH_L, 0.045)
    add_sphere(lines, 'C_HULL_DARK', *ELBOW_R, 0.035); add_sphere(lines, 'C_HULL_DARK', *ELBOW_L, 0.035)
    add_sphere(lines, 'C_HULL_DARK', *WRIST_R, 0.025); add_sphere(lines, 'C_HULL_DARK', *WRIST_L, 0.025)

    add_strut(lines, 'C_HULL_MAIN', SH_R, ELBOW_R, radius=0.04, rings=4)
    add_strut(lines, 'C_HULL_MAIN', ELBOW_R, WRIST_R, radius=0.035, rings=4)
    add_strut(lines, 'C_DETAILS', WRIST_R, HAND_R, radius=0.03, rings=3)

    add_strut(lines, 'C_HULL_MAIN', SH_L, ELBOW_L, radius=0.04, rings=4)
    add_strut(lines, 'C_HULL_MAIN', ELBOW_L, WRIST_L, radius=0.035, rings=4)
    add_strut(lines, 'C_DETAILS', WRIST_L, HAND_L, radius=0.03, rings=3)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        dynamic_rig = generate_walking_mannequin(t_sec)
        
        # Absolute Origin Tracking: Locking focal geometry strictly to the core biological boundary
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.9
        
        # Starts explicitly from 115-degrees
        azimuth = 115.0 - (stage * 360.0)

        yield (f, t_sec, azimuth, cam_x, cam_y, cam_z, dynamic_rig)

def render_frame(packet):
    f, t_sec, azimuth, cx, cy, cz, dynamic_rig = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # 100% VISIBILITY THRESHOLD AUDIT:
    cam_span = 0.75
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.6, 0.4), 
        ('C_ACCENT',    C_ACCENT,    1.5, 0.8),
        ('C_HULL_MAIN', C_HULL_MAIN, 1.2, 1.0),
        ('C_HULL_DARK', C_HULL_DARK, 1.5, 1.0),
        ('C_DETAILS',   C_DETAILS,   1.2, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in dynamic_rig[c_key]:
            # Elevated +14 degrees to powerfully dissect the active walking parameters against the translating mat
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=14.0)
            render_queue.append((np.mean(depth), u, v, c_val, lw, alpha))

    # ABSOLUTE Z-SORT 
    render_queue.sort(key=lambda item: item[0], reverse=True)
    for depth, u, v, c, lw, a in render_queue:
        ax.plot(u, v, color=c, lw=lw, alpha=a)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (TOP HUD)
    # ------------------------------------------------------------------
    ui_t = cam_span * 1.45
    ax.add_patch(patches.Rectangle((-cam_span, ui_t), cam_span*2, cam_span*0.5, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_t, ui_t], color=C_TEXT, lw=6, zorder=81)

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-451i // MACRO-ENGINEERING TENSOR: ROBOTIC KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT VECTOR LOCOMOTION // KINEMATIC WALK CYCLE MATRIX", color=C_HULL_DARK, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT / LIVE WALK CYCLE (V=1.0m/s)", color=C_HULL_MAIN, fontsize=13, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: BIOMECHANICAL HARMONICS / ACTIVE Z-AXIS GRAVITY OFFSET", color=C_DETAILS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-451i: ROBOTIC KINEMATICS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Biomechanical Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
