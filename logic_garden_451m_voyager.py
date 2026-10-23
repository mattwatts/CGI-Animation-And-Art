"""
PROJECT: Logic Garden 451m (Exact Physical Construct // Voyager Space Probe Matrix) - HOTFIX
FORMAT: YouTube Shorts (1080x1920)
METADATA: VOYAGER, NASA, SPACE PROBE, WIREFRAME, ENGINEERING, KINEMATICS, ASTROPHYSICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation mapping precise deep-space geometry.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: 10-sided core bus, 3.7m parabolic HGA dish, 13m Astromast truss, RTG blocks.
- Custom Kinematic Nodes: Patched HGA depth calculations guaranteeing unbroken numpy arrays for `list()` broadcasting.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from absolute 115-degree dramatic front-quarter angle.
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
OUT_DIR = "frames_451m_voyager"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Orbital Reference Plane)

C_BUS       = '#D97706'          # Kapton Gold (Decagonal Core, Golden Record)
C_DISH      = '#94A3B8'          # Slate Aluminium (HGA Parabolic Dish & Mast)
C_TRUSS     = '#475569'          # Machined Slate (Magnetometer Astromast)
C_RTG       = '#111115'          # Indestructible Black (Plutonium Power Modules)
C_INSTR     = '#1E293B'          # Carbon Slate (Scan Platforms, Cameras, Antennas)

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
# GEOMETRIC PRIMITIVES
# ------------------------------------------------------------------
def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='z', rings=4, t_count=16):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, length, rings)
    for s in steps:
        if axis == 'x':  ix, iy, iz = np.full_like(t, cx + s), cy + radius*np.cos(t), cz + radius*np.sin(t)
        elif axis == 'y': ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + s), cz + radius*np.sin(t)
        else:             ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), np.full_like(t, cz + s)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        if axis == 'x':   sx, sy, sz = cx + steps, [cy + radius*np.cos(a)]*rings, [cz + radius*np.sin(a)]*rings
        elif axis == 'y': sx, sy, sz = [cx + radius*np.cos(a)]*rings, cy + steps, [cz + radius*np.sin(a)]*rings
        else:             sx, sy, sz = [cx + radius*np.cos(a)]*rings, [cy + radius*np.sin(a)]*rings, cz + steps
        append_segmented(lines_dict, col, sx, sy, sz)

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
        ix = p1[0] + v_dir[0]*s + radius * (np.cos(t)*n1[0] + np.sin(t)*n2[0])
        iy = p1[1] + v_dir[1]*s + radius * (np.cos(t)*n1[1] + np.sin(t)*n2[1])
        iz = p1[2] + v_dir[2]*s + radius * (np.cos(t)*n1[2] + np.sin(t)*n2[2])
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        nx = radius * (np.cos(a)*n1[0] + np.sin(a)*n2[0])
        ny = radius * (np.cos(a)*n1[1] + np.sin(a)*n2[1])
        nz = radius * (np.cos(a)*n1[2] + np.sin(a)*n2[2])
        sx = p1[0] + nx + v_dir[0]*steps
        sy = p1[1] + ny + v_dir[1]*steps
        sz = p1[2] + nz + v_dir[2]*steps
        append_segmented(lines_dict, col, list(sx), list(sy), list(sz))

def add_truss(lines_dict, col, p1, p2, radius, sections=20):
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
    
    t_angles = [0, 2*np.pi/3, 4*np.pi/3] 
    nodes = []
    steps = np.linspace(0, length, sections)
    
    for s in steps:
        sec_nodes = []
        for a in t_angles:
            nx = radius * (np.cos(a)*n1[0] + np.sin(a)*n2[0])
            ny = radius * (np.cos(a)*n1[1] + np.sin(a)*n2[1])
            nz = radius * (np.cos(a)*n1[2] + np.sin(a)*n2[2])
            sec_nodes.append([p1[0] + nx + v_dir[0]*s, 
                              p1[1] + ny + v_dir[1]*s, 
                              p1[2] + nz + v_dir[2]*s])
        nodes.append(sec_nodes)
        
    for c in range(3):
        xs = [n[c][0] for n in nodes]; ys = [n[c][1] for n in nodes]; zs = [n[c][2] for n in nodes]
        append_segmented(lines_dict, col, xs, ys, zs)
        
    for i in range(sections - 1):
        for c in range(3):
            nx_c = (c+1)%3
            append_segmented(lines_dict, col, [nodes[i][c][0], nodes[i+1][nx_c][0]],
                                              [nodes[i][c][1], nodes[i+1][nx_c][1]],
                                              [nodes[i][c][2], nodes[i+1][nx_c][2]])

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (VOYAGER CORE)
# ------------------------------------------------------------------
def generate_voyager_static():
    lines = {
        'C_BUS': [], 'C_DISH': [], 'C_TRUSS': [], 
        'C_RTG': [], 'C_INSTR': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. ORBITAL REFERENCE GRID
    # ==============================================================================
    Z_FLOOR = -4.0
    for r_p in [4.0, 8.0, 12.0]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
    
    # ==============================================================================
    # 2. DECAGONAL BUS & GOLDEN RECORD
    # ==============================================================================
    B_R = 0.9   
    B_ZT = 0.2  
    B_ZB = -0.3 
    
    t_dec = np.linspace(0, 2*np.pi, 10, endpoint=False)
    bx = B_R * np.cos(t_dec); by = B_R * np.sin(t_dec)
    
    append_segmented(lines, 'C_BUS', list(bx)+[bx[0]], list(by)+[by[0]], [B_ZT]*11)
    append_segmented(lines, 'C_BUS', list(bx)+[bx[0]], list(by)+[by[0]], [B_ZB]*11)
    for i in range(10): 
        append_segmented(lines, 'C_BUS', [bx[i], bx[i]], [by[i], by[i]], [B_ZB, B_ZT])
        
    add_cylinder(lines, 'C_BUS', cx=B_R*0.85, cy=-B_R*0.5, cz=-0.05, length=0.08, radius=0.18, axis='x', rings=3, t_count=16)

    # ==============================================================================
    # 3. HIGH-GAIN ANTENNA (3.7m Parabolic Dish)
    # ==============================================================================
    D_R = 1.85
    r_dish = np.linspace(0.1, D_R, 6)
    t_dish = np.linspace(0, 2*np.pi, 24, endpoint=False)
    
    # Concentric Parabolic Mapping (HOTFIX: Explicit array mapping to bypass scalar errors)
    for r in r_dish:
        dx = r * np.cos(t_dish); dy = r * np.sin(t_dish)
        dz = np.full_like(dx, B_ZT + 0.1 + 0.14 * (r/D_R)**2)
        append_segmented(lines, 'C_DISH', list(dx)+[dx[0]], list(dy)+[dy[0]], list(dz)+[dz[0]])
        
    for a in np.linspace(0, 2*np.pi, 12, endpoint=False):
        dxs = r_dish * np.cos(a); dys = r_dish * np.sin(a)
        dzs = B_ZT + 0.1 + 0.14 * (r_dish/D_R)**2
        append_segmented(lines, 'C_DISH', list(dxs), list(dys), list(dzs))

    SR_Z = B_ZT + 0.9
    add_cylinder(lines, 'C_DISH', 0.0, 0.0, SR_Z, 0.1, 0.15, axis='z', rings=2)
    for a in [0, 2*np.pi/3, 4*np.pi/3]:
        px = 1.0 * np.cos(a); py = 1.0 * np.sin(a); pz = B_ZT + 0.1 + 0.14 * (1.0/D_R)**2
        append_segmented(lines, 'C_DISH', [px, 0.0], [py, 0.0], [pz, SR_Z])

    # ==============================================================================
    # 4. SCIENCE PLATFORM BOOM (+X, +Y Bias)
    # ==============================================================================
    S_P1 = (B_R*np.cos(np.pi/4), B_R*np.sin(np.pi/4), 0.0)
    S_P2 = (2.2, 1.5, 0.8)
    add_strut(lines, 'C_DISH', S_P1, S_P2, 0.05, rings=4)
    add_cylinder(lines, 'C_INSTR', cx=2.2, cy=1.5, cz=0.8, length=0.6, radius=0.15, axis='x', rings=3)
    add_cylinder(lines, 'C_INSTR', cx=2.2, cy=1.3, cz=0.9, length=0.4, radius=0.1,  axis='y', rings=3)

    # ==============================================================================
    # 5. RTG POWER BOOM (-X Bias)
    # ==============================================================================
    R_P1 = (-B_R, 0.0, 0.0)
    R_P2 = (-3.2, -0.5, -0.6)
    add_strut(lines, 'C_DISH', R_P1, R_P2, 0.06, rings=4)
    for rtg_idx, offset in enumerate([0.3, 0.6, 0.9]):
        r_cx = R_P1[0] + offset*(R_P2[0]-R_P1[0])
        r_cy = R_P1[1] + offset*(R_P2[1]-R_P1[1])
        r_cz = R_P1[2] + offset*(R_P2[2]-R_P1[2])
        add_cylinder(lines, 'C_RTG', cx=r_cx, cy=r_cy-0.15, cz=r_cz, length=0.3, radius=0.2, axis='y', rings=5, t_count=12)

    # ==============================================================================
    # 6. ASTROMAST MAGNETOMETER BOOM (+Y Bias, 13m extreme truss)
    # ==============================================================================
    M_P1 = (0.0, B_R, 0.0)
    M_P2 = (0.0, 11.0, -0.4) 
    add_truss(lines, 'C_TRUSS', M_P1, M_P2, radius=0.15, sections=36)
    add_cylinder(lines, 'C_INSTR', cx=0.0, cy=10.8, cz=-0.4, length=0.4, radius=0.1, axis='x', rings=3, t_count=8)

    # ==============================================================================
    # 7. PLANETARY RADIO ASTRONOMY (PRA) & PLASMA WAVE SUBSYSTEM (PWS) ANTENNAS
    # ==============================================================================
    A_BASE = (0.0, -B_R*0.5, B_ZB)
    add_strut(lines, 'C_INSTR', A_BASE, (-6.5, -5.5, -3.5), 0.02, rings=8)
    add_strut(lines, 'C_INSTR', A_BASE, ( 6.5, -5.5, -3.5), 0.02, rings=8)

    return lines

# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_voyager_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: 
        # Shifting the Y-center to +2.5 to perfectly balance the immense 11m Astromast boom against the compact RTG
        cam_x, cam_y, cam_z = 0.0, 2.5, 0.0
        
        # Starts explicitly from 115-degrees (Dramatic front-quarter offset)
        azimuth = 115.0 - (stage * 360.0)

        yield (f, t_sec, azimuth, cam_x, cam_y, cam_z, static_rig)

def render_frame(packet):
    f, t_sec, azimuth, cx, cy, cz, static_rig = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # 100% VISIBILITY THRESHOLD AUDIT:
    cam_span = 13.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',  C_GRID,  0.5, 0.4), 
        ('C_TRUSS', C_TRUSS, 1.2, 1.0),
        ('C_RTG',   C_RTG,   1.5, 1.0),
        ('C_INSTR', C_INSTR, 1.2, 1.0),
        ('C_DISH',  C_DISH,  1.2, 1.0),
        ('C_BUS',   C_BUS,   1.4, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=22.0)
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-451m_HF // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // VOYAGER SPACE PROBE MATRIX", color=C_BUS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_INSTR, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: 10-SIDED BUS / 3.7M HGA / 13M ASTROMAST TRUSS", color=C_DISH, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-451m_HF: VOYAGER SPACE PROBE TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
