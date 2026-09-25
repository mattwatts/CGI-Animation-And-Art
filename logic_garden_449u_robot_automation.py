"""
PROJECT: Logic Garden 449u (Exact Physical Construct // Robot Automation Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: INDUSTRIAL ROBOT, CONVEYOR, PICK AND PLACE, WIREFRAME, ENGINEERING, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Live Inverse Kinematics (IK): Computes true Yaw/Pitch intersections dynamically.
- State Machine Integration: Flawless trajectory tracking of moving belt payloads.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from absolute Side Profile.
- Daylight Palette (White Substrate / High-Contrast Edge Geometry).
- Purged Jargon. Australian spelling conventions (maths, colour, kilometres, aeroplane, synchronisation).
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
OUT_DIR = "frames_449u_robot_automation"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_BASE      = '#1E293B'          # Carbon Slate (Robot Base)
C_ROBOT     = '#D95F22'          # Industrial Amber (Primary Arms)
C_JOINT     = '#94A3B8'          # Machined Steel (Cylinders, Tooling)
C_BELT      = '#475569'          # Slate Grey (Conveyor Rig)
C_BELT_LINE = '#94A3B8'          # Machined Steel (Belt Treads)
C_CHUTE     = '#111115'          # Indestructible Black (Drop Zone)
C_TARGET    = '#005599'          # Deep Marine (Blue Payloads - Picked)
C_REJECT    = '#00C853'          # Industrial Jade (Green Payloads - Ignored)
C_GRID      = '#CBD5E1'          # Subdued Steel (Baseplate Reference)

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
    for i in range(len(xs) - 1):
        lines_dict[key].append(([xs[i], xs[i+1]], [ys[i], ys[i+1]], [zs[i], zs[i+1]]))

def rotate_y_pitch(x, y, z, cx, cz, pitch_deg):
    p = np.radians(pitch_deg)
    x0, z0 = x - cx, z - cz
    x1 = x0 * np.cos(p) - z0 * np.sin(p)
    z1 = x0 * np.sin(p) + z0 * np.cos(p)
    return x1 + cx, y, z1 + cz

def rotate_z_yaw(x, y, z, cx, cy, yaw_deg):
    yw = np.radians(yaw_deg)
    x0, y0 = x - cx, y - cy
    x1 = x0 * np.cos(yw) - y0 * np.sin(yw)
    y1 = x0 * np.sin(yw) + y0 * np.cos(yw)
    return x1 + cx, y1 + cy, z

def extrude_profile(lines_dict, col, xz_points, y_min, y_max):
    xs = [p[0] for p in xz_points]; zs = [p[1] for p in xz_points]
    xs.append(xs[0]); zs.append(zs[0])
    append_segmented(lines_dict, col, xs, [y_min]*len(xs), zs)
    append_segmented(lines_dict, col, xs, [y_max]*len(xs), zs)
    for x, z in xz_points:
        append_segmented(lines_dict, col, [x, x], [y_min, y_max], [z, z])

def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='y', rings=6, t_count=12):
    t = np.linspace(0, 2*np.pi, t_count)
    steps = np.linspace(0, length, rings)
    for s in steps:
        if axis == 'y':  ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + s), cz + radius*np.sin(t)
        elif axis == 'x': ix, iy, iz = np.full_like(t, cx + s), cy + radius*np.cos(t), cz + radius*np.sin(t)
        else:             ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), np.full_like(t, cz + s)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in t[::max(1, t_count//4)]:
        if axis == 'y':   sx, sy, sz = [cx + radius*np.cos(a)]*rings, cy + steps, [cz + radius*np.sin(a)]*rings
        elif axis == 'x': sx, sy, sz = cx + steps, [cy + radius*np.cos(a)]*rings, [cz + radius*np.sin(a)]*rings
        else:             sx, sy, sz = [cx + radius*np.cos(a)]*rings, [cy + radius*np.sin(a)]*rings, cz + steps
        append_segmented(lines_dict, col, sx, sy, sz)

def add_box(lines_dict, col, cx, cy, cz, dx, dy, dz):
    hx, hy, hz = dx/2, dy/2, dz/2
    xs = [cx-hx, cx+hx, cx+hx, cx-hx, cx-hx]; ys1 = [cy-hy]*2 + [cy+hy]*2 + [cy-hy]; ys2 = ys1[:]
    append_segmented(lines_dict, col, xs, ys1, [cz-hz]*5)
    append_segmented(lines_dict, col, xs, ys2, [cz+hz]*5)
    for i in range(4): append_segmented(lines_dict, col, [xs[i], xs[i]], [ys1[i], ys1[i]], [cz-hz, cz+hz])

# ------------------------------------------------------------------
# MASTER GEOMETRY COMPILERS (LOCAL SPACE)
# ------------------------------------------------------------------
def build_local_waist():
    l = {'C_ROBOT':[], 'C_JOINT':[]} 
    add_cylinder(l, 'C_ROBOT', 0,0,0.55, 0.2, 0.5, 'z')
    extrude_profile(l, 'C_ROBOT', [(-0.35, 0.75), (0.35, 0.75), (0.2, 1.2), (-0.4, 1.2)], 0.3, 0.5)
    extrude_profile(l, 'C_ROBOT', [(-0.35, 0.75), (0.35, 0.75), (0.2, 1.2), (-0.4, 1.2)], -0.5, -0.3)
    return l
    
def build_local_arm1():
    l = {'C_ROBOT':[], 'C_JOINT':[]}
    prof = [(0, 0.25), (0.2, 0.3), (1.1, 0.2), (1.312, 0.15), (1.312, -0.15), (1.1, -0.2), (0.2, -0.3), (0, -0.25)]
    extrude_profile(l, 'C_ROBOT', prof, -0.25, 0.25)
    add_cylinder(l, 'C_JOINT', 0, -0.6, 0, 1.2, 0.22, 'y')
    add_cylinder(l, 'C_JOINT', 1.312, -0.45, 0, 0.9, 0.18, 'y')
    return l
    
def build_local_arm2():
    l = {'C_ROBOT':[], 'C_JOINT':[]}
    prof = [(0, 0.15), (0.2, 0.2), (1.2, 0.1), (1.4, 0.08), (1.4, -0.08), (1.2, -0.1), (0.2, -0.2), (0, -0.15)]
    extrude_profile(l, 'C_ROBOT', prof, -0.2, 0.2)
    add_cylinder(l, 'C_JOINT', 1.4, -0.25, 0, 0.5, 0.12, 'y', t_count=12)
    return l
    
def build_local_tool():
    l = {'C_JOINT':[]}
    add_cylinder(l, 'C_JOINT', 0, 0, 0, 0.35, 0.05, 'x', rings=3)
    add_box(l, 'C_JOINT', 0.35, 0, 0, 0.05, 0.3, 0.2)
    return l
    
def build_static_env():
    l = {'C_BASE':[], 'C_BELT':[], 'C_CHUTE':[], 'C_GRID':[]}
    add_box(l, 'C_BELT', 0, 1.5, 0.225, 24.0, 1.0, 0.45)
    add_box(l, 'C_CHUTE', 1.5, -1.2, 0.25, 1.2, 1.2, 0.5)
    base_prof = [(-0.8, 0.0), (0.8, 0.0), (0.8, 0.3), (0.6, 0.55), (-0.6, 0.55), (-0.8, 0.3)]
    extrude_profile(l, 'C_BASE', base_prof, -0.6, 0.6)
    
    gx = np.linspace(-6, 6, 25) 
    for x in gx: append_segmented(l, 'C_GRID', np.full_like(gx, x), np.clip(gx, -4, 4), np.zeros_like(gx))
    gy = np.linspace(-4, 4, 17)
    for y in gy: append_segmented(l, 'C_GRID', np.clip(gx, -6, 6), np.full_like(gx, y), np.zeros_like(gx))
    return l

def build_payload():
    l = {'C_OBJ': []}
    add_box(l, 'C_OBJ', 0, 0, 0, 0.4, 0.4, 0.3)
    append_segmented(l, 'C_OBJ', [-0.2, 0.2], [0, 0], [0.15, 0.15])
    append_segmented(l, 'C_OBJ', [0, 0], [-0.2, 0.2], [0.15, 0.15])
    return l['C_OBJ']

# ------------------------------------------------------------------
# KINEMATIC TARGETING (STATE MACHINE)
# ------------------------------------------------------------------
def smooth_step(edge0, edge1, x):
    t = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)

def get_target(t):
    tau = t % 3.0
    if tau < 0.7:
        s = smooth_step(0.0, 0.7, tau)
        Tx = np.interp(s, [0, 1], [1.5, -1.6])
        Ty = np.interp(s, [0, 1], [-1.2, 1.5])
        Tz = np.interp(s, [0, 1], [0.8, 0.8])
    elif tau < 1.5:
        s = smooth_step(0.7, 1.5, tau)
        Tx = -3.0 + 2.0 * tau
        Ty = 1.5
        Tz = np.interp(s, [0, 1], [0.8, 0.42])
    elif tau < 2.3:
        s = smooth_step(1.5, 2.3, tau)
        Tx = np.interp(s, [0, 1], [0.0, 1.5])
        Ty = np.interp(s, [0, 1], [1.5, -1.2])
        Tz = np.interp(s, [0, 1], [0.42, 0.8]) + np.sin(s * np.pi) * 0.4
    elif tau < 2.7:
        s = smooth_step(2.3, 2.7, tau)
        Tx, Ty = 1.5, -1.2
        Tz = np.interp(s, [0, 1], [0.8, 0.2])
    else:
        s = smooth_step(2.7, 3.0, tau)
        Tx, Ty = 1.5, -1.2
        Tz = np.interp(s, [0, 1], [0.2, 0.8])
    return Tx, Ty, Tz

# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    w_pts = build_local_waist()
    a1_pts = build_local_arm1()
    a2_pts = build_local_arm2()
    tl_pts = build_local_tool()
    env_pts = build_static_env()
    load_pts = build_payload()

    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        Tx, Ty, Tz = get_target(t_sec)
        
        cam_x, cam_y, cam_z = 0.0, 0.0, 1.2 
        azimuth = 90.0 - ((t_sec / DURATION) * 360.0)
        yield (f, t_sec, azimuth, Tx, Ty, Tz, cam_x, cam_y, cam_z, w_pts, a1_pts, a2_pts, tl_pts, env_pts, load_pts)

def render_frame(packet):
    f, t_sec, azimuth, Tx, Ty, Tz, cx, cy, cz, w_pts, a1_pts, a2_pts, tl_pts, env_pts, load_pts = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    cam_span = 3.6
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []

    def queue_proj(xl, yl, zl, col, lw, alpha):
        u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=22.0)
        render_queue.append((np.mean(depth), u, v-0.4, col, lw, alpha))

    # ---- ENVIRONMENT & BELT ----
    for c_key, lists in env_pts.items():
        if c_key == 'C_GRID': col, lw, a = C_GRID, 0.8, 0.4
        elif c_key == 'C_BASE': col, lw, a = C_BASE, 1.8, 1.0
        elif c_key == 'C_BELT': col, lw, a = C_BELT, 1.5, 1.0
        elif c_key == 'C_CHUTE': col, lw, a = C_CHUTE, 2.0, 1.0
        for xl, yl, zl in lists: queue_proj(xl, yl, zl, col, lw, a)

    # Dynamic Belt Treads
    bx_off = (t_sec * 2.0) % 1.0
    for k in range(-12, 13):
        sx_line = k + bx_off
        queue_proj([sx_line, sx_line], [1.0, 2.0], [0.46, 0.46], C_BELT_LINE, 1.0, 1.0)

    # ---- PAYLOADS ----
    def draw_obj(px, py, pz, col):
        for xl, yl, zl in load_pts:
            queue_proj(np.array(xl)+px, np.array(yl)+py, np.array(zl)+pz, col, 2.2, 1.0)
            
    for k in range(-6, 6):
        # Picked Blue Objects (Stops rendering on belt the exact frame it is gripped)
        bx = (2.0 * (t_sec - 1.5) + k * 6.0) % 24 - 12
        if bx <= 0.01: draw_obj(bx, 1.5, 0.6, C_TARGET) 
        # Missed Green Objects (Continuously translates forward)
        gx = (2.0 * (t_sec - 1.5) - 3.0 + k * 6.0) % 24 - 12
        draw_obj(gx, 1.5, 0.6, C_REJECT)

    # Active Gripped Blue Payload
    tau = t_sec % 3.0
    if 1.5 <= tau < 2.7: draw_obj(Tx, Ty, Tz + 0.15, C_TARGET)

    # ---- INVERSE KINEMATICS (IK) SOLVER ----
    L3 = 0.35; L1 = 1.31244; L2 = 1.4
    Wx, Wy, Wz = Tx, Ty, Tz + L3
    yaw_rad = np.arctan2(Wy, Wx)
    R = np.sqrt(Wx**2 + Wy**2)
    Z_off = Wz - 1.05
    D = np.clip(np.sqrt(R**2 + Z_off**2), abs(L1 - L2) + 0.001, L1 + L2 - 0.001)

    alpha = np.arctan2(Z_off, R)
    beta = np.arccos(np.clip((L1**2 + D**2 - L2**2) / (2 * L1 * D), -1, 1))
    th_s_rad = alpha + beta
    
    gamma = np.arccos(np.clip((L1**2 + L2**2 - D**2) / (2 * L1 * L2), -1, 1))
    th_e_world_rad = th_s_rad - (np.pi - gamma)

    yaw = np.degrees(yaw_rad)
    th_s = np.degrees(th_s_rad)
    th_e_w = np.degrees(th_e_world_rad)

    # ---- ROBOT RIG RENDERING ----
    for c_key, lists in w_pts.items():
        col, lw = (C_ROBOT, 1.8) if c_key == 'C_ROBOT' else (C_JOINT, 1.2)
        for xl, yl, zl in lists:
            rx, ry, rz = rotate_z_yaw(np.array(xl), np.array(yl), np.array(zl), 0, 0, yaw)
            queue_proj(rx, ry, rz, col, lw, 1.0)
            
    for c_key, lists in a1_pts.items():
        col, lw = (C_ROBOT, 1.8) if c_key == 'C_ROBOT' else (C_JOINT, 1.2)
        for xl, yl, zl in lists:
            rx, ry, rz = rotate_y_pitch(np.array(xl), np.array(yl), np.array(zl), 0, 0, th_s)
            rx, ry, rz = rotate_z_yaw(rx, ry, rz + 1.05, 0, 0, yaw)
            queue_proj(rx, ry, rz, col, lw, 1.0)
            
    Ex, Ez = L1 * np.cos(th_s_rad), 1.05 + L1 * np.sin(th_s_rad)
    for c_key, lists in a2_pts.items():
        col, lw = (C_ROBOT, 1.8) if c_key == 'C_ROBOT' else (C_JOINT, 1.2)
        for xl, yl, zl in lists:
            rx, ry, rz = rotate_y_pitch(np.array(xl), np.array(yl), np.array(zl), 0, 0, th_e_w)
            rx, ry, rz = rotate_z_yaw(rx + Ex, ry, rz + Ez, 0, 0, yaw)
            queue_proj(rx, ry, rz, col, lw, 1.0)

    Wx_j, Wz_j = Ex + L2 * np.cos(th_e_world_rad), Ez + L2 * np.sin(th_e_world_rad)
    for c_key, lists in tl_pts.items():
        for xl, yl, zl in lists:
            rx, ry, rz = rotate_y_pitch(np.array(xl), np.array(yl), np.array(zl), 0, 0, -90.0)
            rx, ry, rz = rotate_z_yaw(rx + Wx_j, ry, rz + Wz_j, 0, 0, yaw)
            queue_proj(rx, ry, rz, C_JOINT, 2.0, 1.0)

    # 2. ABSOLUTE PAINTER'S ALGORITHM
    render_queue.sort(key=lambda item: item[0], reverse=True)
    for depth, u, v, c, lw, a in render_queue:
        ax.plot(u, v, color=c, lw=lw, alpha=a)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS
    # ------------------------------------------------------------------
    ui_t = cam_span * 1.45
    ax.add_patch(patches.Rectangle((-cam_span, ui_t), cam_span*2, 8.0, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_t, ui_t], color=C_TEXT, lw=6, zorder=81)
    ax.text(-cam_span*0.95, ui_t+1.0, "LG-449u // MACRO-ENGINEERING TENSOR: ROBOT AUTOMATION", color=C_TEXT, fontsize=20, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t+0.3, "EXPLICIT TRUE-SCALE GEOMETRY // ACTIVE INVERSE KINEMATICS", color=C_ROBOT, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b+1.0, "[OPERATIONAL] CONTINUOUS PAYLOAD SELECTIVE ROUTING", color=C_TARGET, fontsize=17, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.5, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=17, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.1, "KINEMATIC YIELD  : 20 CYCLES/MIN / ZERO LATENCY EXTRACTION", color=C_REJECT, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-449u: ROBOT AUTOMATION KINEMATICS [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Automation Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
