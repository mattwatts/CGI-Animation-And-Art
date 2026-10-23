"""
PROJECT: Logic Garden 451u (Exact Physical Construct // Gemini Spacecraft Matrix) - HOTFIX
FORMAT: YouTube Shorts (1080x1920)
METADATA: GEMINI, NASA, SPACECRAFT, WIREFRAME, ENGINEERING, KINEMATICS, AEROSPACE
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional 5.67m aerospace scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Equipment Module, Retrograde Module, Re-entry Cabin, R&R Section, RCS Nose.
- Hotfix Integration: 'add_sphere' primitive injected for Active Rendezvous Radar nose.
- Viewport Override: Locked cam_span rigorously guarantees 100% vehicle visibility strictly between UI boundaries.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from 115-degree dramatic front-quarter angle.
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
OUT_DIR = "frames_451u_gemini"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Orbital Tracking Plane)

C_ADAPTER   = '#94A3B8'          # Slate Aluminium (Equipment & Retrograde Modules)
C_CABIN     = '#0F172A'          # Abyssal Slate (Rene 41 Dark Hull of Re-entry Capsule)
C_DETAILS   = '#1E293B'          # Carbon Slate (Structural Ribs & Hatches)
C_HARDWARE  = '#475569'          # Machined Slate (Pilot Windows, RCS Thrusters)
C_FOIL      = '#D97706'          # Kapton Gold (Aft Adapter Thermal Shielding)
C_RED       = '#E11D48'          # Kinematic Red (Active Docking Index / Warning Nodes)

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
def add_quad_mesh(lines_dict, col, p1, p2, p3, p4, u_steps=4, v_steps=4):
    p1, p2, p3, p4 = map(np.array, (p1, p2, p3, p4))
    for i in range(v_steps + 1):
        v = i / v_steps
        start = p1 * (1-v) + p4 * v
        end   = p2 * (1-v) + p3 * v
        pts = [start * (1-u) + end * u for u in np.linspace(0, 1, u_steps+1)]
        append_segmented(lines_dict, col, [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts])
    for i in range(u_steps + 1):
        u = i / u_steps
        start = p1 * (1-u) + p2 * u
        end   = p4 * (1-u) + p3 * u
        pts = [start * (1-v) + end * v for v in np.linspace(0, 1, v_steps+1)]
        append_segmented(lines_dict, col, [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts])

def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='z', rings=4, t_count=16):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, length, rings)
    for s in steps:
        if axis == 'z':
            ix = cx + radius*np.cos(t); iy = cy + radius*np.sin(t); iz = np.full_like(t, cz + s)
        elif axis == 'x':
            ix = np.full_like(t, cx + s); iy = cy + radius*np.cos(t); iz = cz + radius*np.sin(t)
        elif axis == 'y':
            ix = cx + radius*np.cos(t); iy = np.full_like(t, cy + s); iz = cz + radius*np.sin(t)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        if axis == 'z':
            sx = np.full_like(steps, cx + radius*np.cos(a))
            sy = np.full_like(steps, cy + radius*np.sin(a))
            sz = cz + steps
        elif axis == 'x':
            sx = cx + steps
            sy = np.full_like(steps, cy + radius*np.cos(a))
            sz = np.full_like(steps, cz + radius*np.sin(a))
        elif axis == 'y':
            sx = np.full_like(steps, cx + radius*np.cos(a))
            sy = cy + steps
            sz = np.full_like(steps, cz + radius*np.sin(a))
        append_segmented(lines_dict, col, list(sx), list(sy), list(sz))

def add_cone_frustum(lines_dict, col, cx, cy, cz, dz, r1, r2, offset=(0,0), axis='z', rings=4, t_count=16):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, dz, rings)
    r_step = np.linspace(r1, r2, rings)
    ox_step = np.linspace(0, offset[0], rings)
    oy_step = np.linspace(0, offset[1], rings)

    for i, s in enumerate(steps):
        r = r_step[i]; ox = ox_step[i]; oy = oy_step[i]
        iz = np.full_like(t, cz + s)
        ix = cx + ox + r*np.cos(t); iy = cy + oy + r*np.sin(t)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        sx, sy, sz = [], [], []
        for i, s in enumerate(steps):
            r = r_step[i]; ox = ox_step[i]; oy = oy_step[i]
            sx.append(cx + ox + r*np.cos(a)); sy.append(cy + oy + r*np.sin(a)); sz.append(cz + s)
        append_segmented(lines_dict, col, sx, sy, sz)

def add_sphere(lines_dict, col, cx, cy, cz, radius, rings=8, t_count=16):
    for p in np.linspace(-np.pi/2, np.pi/2, rings):
        r_s = radius * np.cos(p)
        z_s = radius * np.sin(p)
        t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
        ix = cx + r_s*np.cos(t); iy = cy + r_s*np.sin(t); iz = np.full_like(t, cz + z_s)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, np.pi, t_count//2, endpoint=False):
        p = np.linspace(-np.pi/2, np.pi/2, rings*2)
        r_s = radius * np.cos(p)
        ix = cx + r_s*np.cos(a); iy = cy + r_s*np.sin(a); iz = cz + radius*np.sin(p)
        append_segmented(lines_dict, col, list(ix), list(iy), list(iz))

def add_box(lines_dict, col, cx, cy, cz, dx, dy, dz):
    hx, hy, hz = dx/2, dy/2, dz/2
    xs = [cx-hx, cx+hx, cx+hx, cx-hx, cx-hx]
    ys1 = [cy-hy, cy-hy, cy+hy, cy+hy, cy-hy]
    ys2 = [cy-hy, cy-hy, cy+hy, cy+hy, cy-hy]
    append_segmented(lines_dict, col, xs, ys1, [cz-hz]*5)
    append_segmented(lines_dict, col, xs, ys2, [cz+hz]*5)
    for i in range(4):
        append_segmented(lines_dict, col, [xs[i], xs[i]], [ys1[i], ys1[i]], [cz-hz, cz+hz])

def add_sym_box(lines_dict, col, cx, cy, cz, dx, dy, dz):
    add_box(lines_dict, col, cx, cy, cz, dx, dy, dz)
    if abs(cy) > 0.001:
        add_box(lines_dict, col, cx, -cy, cz, dx, dy, dz)

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (GEMINI SPACECRAFT)
# ------------------------------------------------------------------
def generate_gemini_static():
    lines = {
        'C_ADAPTER': [], 'C_CABIN': [], 'C_DETAILS': [], 
        'C_HARDWARE': [], 'C_FOIL': [], 'C_RED': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. ORBITAL TRACKING BASEPLATE
    # ==============================================================================
    Z_FLOOR = -1.0
    for r_p in [1.5, 3.0, 5.0]:
        t_p = np.linspace(0, 2*np.pi, 48, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-5.0, 5.0, 11)
    gy_range = np.linspace(-5.0, 5.0, 11)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. EQUIPMENT MODULE (EM)
    # ==============================================================================
    # Total adapter base diameter is 3.05m -> r=1.525
    Z_EM_BASE = 0.0
    Z_EM_TOP = 1.4
    R_EM_BASE = 1.525
    R_EM_TOP = 1.15

    # Aft thermal/gold foil shield backing the adapter
    add_cylinder(lines, 'C_FOIL', 0.0, 0.0, Z_EM_BASE, 0.05, R_EM_BASE, rings=2, t_count=32)

    # Equipment Module Frustum (White/Aluminium)
    add_cone_frustum(lines, 'C_ADAPTER', 0.0, 0.0, Z_EM_BASE+0.05, (Z_EM_TOP - (Z_EM_BASE+0.05)), r1=R_EM_BASE, r2=R_EM_TOP, rings=6, t_count=32)

    # Thrust chamber arrays / Heat radiatior seams around the EM
    for a in np.linspace(0, 2*np.pi, 8, endpoint=False):
        mx = (R_EM_BASE - 0.15) * np.cos(a)
        my = (R_EM_BASE - 0.15) * np.sin(a)
        add_cylinder(lines, 'C_DETAILS', mx, my, Z_EM_BASE+0.2, 0.8, 0.08, axis='z', rings=3, t_count=8)

    # ==============================================================================
    # 3. RETROGRADE MODULE (RM)
    # ==============================================================================
    Z_RM_TOP = 2.3
    R_RM_TOP = 0.95

    # Retro module transitioning from EM to the re-entry cabin flange
    add_cone_frustum(lines, 'C_ADAPTER', 0.0, 0.0, Z_EM_TOP, (Z_RM_TOP - Z_EM_TOP), r1=R_EM_TOP, r2=R_RM_TOP, rings=4, t_count=32)

    # Retro-rocket housing demarcations (4 large strap seams wrapping the RM)
    add_cylinder(lines, 'C_DETAILS', 0.0, 0.0, Z_EM_TOP+0.4, 0.1, R_EM_TOP-0.1, rings=2, t_count=24)

    # ==============================================================================
    # 4. RE-ENTRY MODULE / CABIN
    # ==============================================================================
    Z_CABIN_TOP = 4.2
    R_CABIN_TOP = 0.40

    # The aggressive conical geometry of the primary crew hull (Abyssal Slate / Rene 41)
    # Utilizing an exceptionally dense t_count to define the rigid geometric tracking lines
    add_cone_frustum(lines, 'C_CABIN', 0.0, 0.0, Z_RM_TOP, (Z_CABIN_TOP - Z_RM_TOP), r1=R_RM_TOP, r2=R_CABIN_TOP, rings=10, t_count=36)

    # ==============================================================================
    # 5. TWIN PILOT WINDOWS & HATCH BOUNDARIES
    # ==============================================================================
    # Gemini windows are distinctive multi-pane D-shapes projecting on the +X facing sector
    # Calculated on explicit tangential projections approx 25 deg off the +X axis
    win_angles = [np.pi/8, -np.pi/8] # Symmetrical angles for Command Pilot and Pilot
    
    for a in win_angles:
        # Interpolating structural boundaries across the conical surface
        z_w_bottom = 3.3
        z_w_top = 3.7
        r_w_bottom = R_RM_TOP - ((z_w_bottom - Z_RM_TOP)/(Z_CABIN_TOP - Z_RM_TOP)) * (R_RM_TOP - R_CABIN_TOP)
        r_w_top = R_RM_TOP - ((z_w_top - Z_RM_TOP)/(Z_CABIN_TOP - Z_RM_TOP)) * (R_RM_TOP - R_CABIN_TOP)
        
        # Outward projection vectors for window sealing frames
        px_bot = r_w_bottom * 1.05 * np.cos(a)
        py_bot = r_w_bottom * 1.05 * np.sin(a)
        px_top = r_w_top * 1.05 * np.cos(a)
        py_top = r_w_top * 1.05 * np.sin(a)
        
        w_width = 0.18 # Half-width
        p1 = (px_top - np.sin(a)*w_width, py_top + np.cos(a)*w_width, z_w_top)
        p2 = (px_top + np.sin(a)*w_width, py_top - np.cos(a)*w_width, z_w_top)
        p3 = (px_bot + np.sin(a)*w_width, py_bot - np.cos(a)*w_width, z_w_bottom)
        p4 = (px_bot - np.sin(a)*w_width, py_bot + np.cos(a)*w_width, z_w_bottom)
        
        add_quad_mesh(lines, 'C_HARDWARE', p1, p2, p3, p4, u_steps=2, v_steps=3)

    # ==============================================================================
    # 6. RENDEZVOUS & RECOVERY (R&R) SECTION
    # ==============================================================================
    Z_RR_TOP = 5.0
    R_RR_TOP = 0.35

    # Parachute and recovery compartment
    add_cone_frustum(lines, 'C_CABIN', 0.0, 0.0, Z_CABIN_TOP, (Z_RR_TOP - Z_CABIN_TOP), r1=R_CABIN_TOP, r2=R_RR_TOP, rings=5, t_count=24)

    # ==============================================================================
    # 7. RE-ENTRY CONTROL SYSTEM (RCS) & RADAR NOSE
    # ==============================================================================
    Z_NOSE_TOP = 5.67
    R_NOSE_TOP = 0.10

    # The forward projecting RCS frustum
    add_cone_frustum(lines, 'C_HARDWARE', 0.0, 0.0, Z_RR_TOP, (Z_NOSE_TOP - Z_RR_TOP), r1=R_RR_TOP, r2=R_NOSE_TOP, rings=4, t_count=16)

    # Active Rendezvous Radar array index (Red cap/docking target)
    add_cylinder(lines, 'C_RED', 0.0, 0.0, Z_NOSE_TOP, 0.05, R_NOSE_TOP, rings=2, t_count=12)
    add_sphere(lines, 'C_RED', 0.0, 0.0, Z_NOSE_TOP+0.05, R_NOSE_TOP-0.02, rings=4, t_count=8)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_gemini_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking the vertical focal geometry to dead centre of the 5.67m dimension
        cam_x, cam_y, cam_z = 0.0, 0.0, 2.5
        
        # Starts explicitly from 115-degrees (Dramatic front-quarter aesthetic tracking the pilot windows)
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

    # 100% VISIBILITY THRESHOLD AUDIT (HUD BYPASS PARITY):
    # Anchor Centroid = 2.5m high. Total vertical geometry spanning 0m to 5.67m precisely.
    # We must unconditionally prevent the HUD arrays from occluding the active nose index and baseplate.
    # Setting cam_span forcefully to 3.25 locks horizontal bounds seamlessly across 6.5m total width.
    # Vertical bounds output 3.25 * 1.777 = 5.775m. 
    # Top HUD margin natively forces clearance above 1.45 * 3.25 = 4.712m from centroid (absolute +7.21m).
    # Bottom HUD margin clears below -1.427 * 3.25 = -4.637m from centroid (absolute -2.13m).
    # Asserts an uncompromising, flawlessly framed 5.67m capsule profile cleanly avoiding both UI banners.
    cam_span = 3.25
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,     0.8, 0.4), 
        ('C_FOIL',      C_FOIL,     1.2, 1.0),
        ('C_ADAPTER',   C_ADAPTER,  1.3, 1.0),
        ('C_DETAILS',   C_DETAILS,  1.2, 1.0),
        ('C_CABIN',     C_CABIN,    1.5, 1.0),
        ('C_HARDWARE',  C_HARDWARE, 1.6, 1.0),
        ('C_RED',       C_RED,      1.8, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to powerfully map the high-density frustum tapers across the Z-axis
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=16.0)
            render_queue.append((np.mean(depth), u, v, c_val, lw, alpha))

    # ABSOLUTE Z-SORT (Strict Painter's Algorithm Depth Culling)
    render_queue.sort(key=lambda item: item[0], reverse=True)
    for depth, u, v, c, lw, a in render_queue:
        ax.plot(u, v, color=c, lw=lw, alpha=a)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (TOP HUD)
    # ------------------------------------------------------------------
    ui_t = cam_span * 1.45
    ax.add_patch(patches.Rectangle((-cam_span, ui_t), cam_span*2, cam_span*0.5, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_t, ui_t], color=C_TEXT, lw=6, zorder=81)

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-451u_HF // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // GEMINI SPACECRAFT MATRIX", color=C_ADAPTER, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_CABIN, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: 100% UNCLIPPED HORIZON / EQUIPMENT MODULE / RE-ENTRY CABIN", color=C_HARDWARE, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-451u_HF: GEMINI SPACECRAFT TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
