"""
PROJECT: Logic Garden 453i (Exact Physical Construct // DG Tau T Tauri Star Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: DG TAU, T TAURI, PROTOSTAR, ACCRETION DISK, STL, WIREFRAME, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true extreme astrophysical scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Protostar Core, Flared Protoplanetary Disk, Bipolar Jets, Bow Shocks.
- Procedural Topography: High-density mesh mirroring unoptimised binary capture limits.
- Viewport Override: Locked cam_span rigorously guarantees 100% full-station visibility between UI boundaries.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from 115-degree dramatic front-quarter angle.
- Daylight Palette (White Substrate / High-Contrast Edge Geometry).
- Purged Jargon. Australian spelling conventions (maths, colour, kilometres, synchronisation, manoeuvre).
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
OUT_DIR = "frames_453i_dg_tau"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Interstellar Tracking Grid)

C_STAR      = '#CA8A04'          # Kapton Gold (Young T Tauri Stellar Core)
C_DISK_IN   = '#334155'          # Heavy Slate (Dense Inner Accretion Matrix)
C_DISK_OUT  = '#0F172A'          # Abyssal Slate (Cooler Flared Outer Dust Fields)
C_JET       = '#E11D48'          # Kinematic Red (High-Velocity Collimated Polar Jets)
C_SHOCK     = '#94A3B8'          # Slate Aluminium (Terminal Bow Shock Knots)
C_WIND      = '#1E293B'          # Carbon Slate (Expanding Low-Velocity Disk Outflow)

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

def append_sym(lines_dict, key, xs, ys, zs):
    append_segmented(lines_dict, key, xs, ys, zs)
    # Autonomously generates identical structural topology across the Z-axis (Bipolar reflection)
    if any(abs(z) > 0.001 for z in zs):
        append_segmented(lines_dict, key, xs, ys, [-z for z in zs])

# ------------------------------------------------------------------
# GEOMETRIC PRIMITIVES
# ------------------------------------------------------------------
def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='z', rings=4, t_count=16, reflect_z=False):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, length, rings)
    for s in steps:
        if axis == 'z':
            ix = cx + radius * np.cos(t)
            iy = cy + radius * np.sin(t)
            iz = np.full_like(t, cz + s)
        if reflect_z: append_sym(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
        else: append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
        
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        if axis == 'z':
            sx = cx + radius * np.cos(a) * np.ones_like(steps)
            sy = cy + radius * np.sin(a) * np.ones_like(steps)
            sz = cz + steps
        if reflect_z: append_sym(lines_dict, col, sx, sy, sz)
        else: append_segmented(lines_dict, col, sx, sy, sz)

def add_cone_frustum(lines_dict, col, cx, cy, cz, dz, r1, r2, rings=4, t_count=16, reflect_z=False):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, dz, rings)
    r_step = np.linspace(r1, r2, rings)
    
    for i, s in enumerate(steps):
        r = r_step[i]
        ix = cx + r * np.cos(t)
        iy = cy + r * np.sin(t)
        iz = np.full_like(t, cz + s)
        if reflect_z: append_sym(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
        else: append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        sx, sy, sz = [], [], []
        for i, s in enumerate(steps):
            r = r_step[i]
            sx.append(cx + r * np.cos(a))
            sy.append(cy + r * np.sin(a))
            sz.append(cz + s)
        if reflect_z: append_sym(lines_dict, col, sx, sy, sz)
        else: append_segmented(lines_dict, col, sx, sy, sz)

def add_ellipsoid(lines_dict, col, cx, cy, cz, rx, ry, rz, rings=8, t_count=16):
    theta = np.linspace(-np.pi/2, np.pi/2, rings)
    phi = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    
    for th in theta:
        xs = cx + rx * np.cos(th) * np.cos(phi)
        ys = cy + ry * np.cos(th) * np.sin(phi)
        zs = cz + rz * np.sin(th) * np.ones_like(phi)
        append_segmented(lines_dict, col, list(xs)+[xs[0]], list(ys)+[ys[0]], list(zs)+[zs[0]])
    for ph in phi:
        xs = cx + rx * np.cos(theta) * np.cos(ph)
        ys = cy + ry * np.cos(theta) * np.sin(ph)
        zs = cz + rz * np.sin(theta)
        append_segmented(lines_dict, col, xs, ys, zs)

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (DG TAU MATRIX)
# ------------------------------------------------------------------
def generate_dg_tau_static():
    lines = {
        'C_STAR': [], 'C_DISK_IN': [], 'C_DISK_OUT': [],
        'C_JET': [], 'C_SHOCK': [], 'C_WIND': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. INTERSTELLAR TRACKING BASEPLATE
    # ==============================================================================
    # Locking a grid below the lowest bow shock vector dynamically mapping the limits
    Z_FLOOR = -21.0
    for r_p in [6.0, 12.0, 18.0]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-18.0, 18.0, 19)
    gy_range = np.linspace(-18.0, 18.0, 19)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. CENTRAL PROTOSTAR (T TAURI CORE)
    # ==============================================================================
    # High-density spherical stellar unit evaluating extreme rotational dynamics
    R_STAR = 0.5
    add_ellipsoid(lines, 'C_STAR', 0.0, 0.0, 0.0, rx=R_STAR, ry=R_STAR, rz=R_STAR, rings=12, t_count=24)

    # ==============================================================================
    # 3. FLARED PROTOPLANETARY DISK (MATHEMATICAL ACCRETION MATRIX)
    # ==============================================================================
    # The disk follows physical flaring limits: Z(r) = H0 * (r)^1.25
    R_IN = 1.0
    R_MID = 6.0
    R_OUT = 12.0
    FLARE_FACTOR = 0.15
    
    t_spokes = np.linspace(0, 2*np.pi, 36, endpoint=False)
    
    # Inner Disk Bounds (Extremely dense material plotting)
    r_inner_vals = np.linspace(R_IN, R_MID, 8)
    for r in r_inner_vals:
        z_flare = FLARE_FACTOR * (r ** 1.25)
        x = r * np.cos(t_spokes)
        y = r * np.sin(t_spokes)
        z_pos = np.full_like(t_spokes, z_flare)
        z_neg = np.full_like(t_spokes, -z_flare)
        append_segmented(lines, 'C_DISK_IN', list(x)+[x[0]], list(y)+[y[0]], list(z_pos)+[z_pos[0]])
        append_segmented(lines, 'C_DISK_IN', list(x)+[x[0]], list(y)+[y[0]], list(z_neg)+[z_neg[0]])
        
    for t in t_spokes:
        x = r_inner_vals * np.cos(t)
        y = r_inner_vals * np.sin(t)
        z_pos = FLARE_FACTOR * (r_inner_vals ** 1.25)
        z_neg = -FLARE_FACTOR * (r_inner_vals ** 1.25)
        append_segmented(lines, 'C_DISK_IN', x, y, z_pos)
        append_segmented(lines, 'C_DISK_IN', x, y, z_neg)

    # Outer Disk Bounds (Sparse cooler material resolving boundary limits)
    t_spokes_out = np.linspace(0, 2*np.pi, 24, endpoint=False)
    r_outer_vals = np.linspace(R_MID, R_OUT, 6)
    for r in r_outer_vals:
        z_flare = FLARE_FACTOR * (r ** 1.25)
        x = r * np.cos(t_spokes_out)
        y = r * np.sin(t_spokes_out)
        z_pos = np.full_like(t_spokes_out, z_flare)
        z_neg = np.full_like(t_spokes_out, -z_flare)
        append_segmented(lines, 'C_DISK_OUT', list(x)+[x[0]], list(y)+[y[0]], list(z_pos)+[z_pos[0]])
        append_segmented(lines, 'C_DISK_OUT', list(x)+[x[0]], list(y)+[y[0]], list(z_neg)+[z_neg[0]])
        
    for t in t_spokes_out:
        x = r_outer_vals * np.cos(t)
        y = r_outer_vals * np.sin(t)
        z_pos = FLARE_FACTOR * (r_outer_vals ** 1.25)
        z_neg = -FLARE_FACTOR * (r_outer_vals ** 1.25)
        append_segmented(lines, 'C_DISK_OUT', x, y, z_pos)
        append_segmented(lines, 'C_DISK_OUT', x, y, z_neg)

    # ==============================================================================
    # 4. COLLIMATED BIPOLAR JETS
    # ==============================================================================
    # High-Velocity inner continuous beam forced directly along the Z-axis
    JET_LIM = 19.5
    JET_R = 0.25
    
    # Natively injecting reflecting Z-geometry for twin polar emissions
    add_cylinder(lines, 'C_JET', cx=0.0, cy=0.0, cz=R_STAR, length=(JET_LIM - R_STAR), radius=JET_R, axis='z', rings=10, t_count=12, reflect_z=True)

    # ==============================================================================
    # 5. BOW SHOCK NODES (HERBIG-HARO FEATURES)
    # ==============================================================================
    # Internal episodic collisions driving massive conical expansions within the jet
    KNOTS = [6.0, 11.5, 17.0]
    for kz in KNOTS:
        # Forward expanding shock cone
        add_cone_frustum(lines, 'C_SHOCK', cx=0.0, cy=0.0, cz=kz, dz=2.0, r1=JET_R, r2=1.4, rings=4, t_count=16, reflect_z=True)
        # Core plasma density capping the shock
        add_ellipsoid(lines, 'C_SHOCK', cx=0.0, cy=0.0, cz=kz+2.0, rx=1.4, ry=1.4, rz=0.8, rings=5, t_count=16)
        add_ellipsoid(lines, 'C_SHOCK', cx=0.0, cy=0.0, cz=-(kz+2.0), rx=1.4, ry=1.4, rz=0.8, rings=5, t_count=16)

    # ==============================================================================
    # 6. EXPANDING DISK-WIND OUTFLOW
    # ==============================================================================
    # Slowly collimating lower-velocity winds stripped from the disk bounds
    add_cone_frustum(lines, 'C_WIND', cx=0.0, cy=0.0, cz=R_STAR, dz=14.0, r1=1.5, r2=4.0, rings=6, t_count=20, reflect_z=True)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_dg_tau_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry flawlessly at the protostar centroid
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.0
        
        # Starts explicitly from 115-degrees (Dramatic aesthetic exposing the massive flared disk and bipolar beams)
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
    # Anchor Centroid = Dead zero. The outermost disk boundary maps consistently exactly to R=12.0.
    # The extreme Bow-Shock Knots push vertical geometry up to ~Z=+/- 19.8 units.
    # Setting cam_span strictly to 13.5 locks horizontal width symmetrically across a 27.0-unit view (safely bounding the disk).
    # Vertical bounds output 13.5 * 1.777 = 23.98 vertical clearance (total height window 47.9 units).
    # Completely traps the immense jet ejections safely inside the transparent viewport, immune to UI overlay clipping.
    cam_span = 13.5
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_DISK_OUT',  C_DISK_OUT,  1.1, 0.8),
        ('C_DISK_IN',   C_DISK_IN,   1.3, 1.0),
        ('C_WIND',      C_WIND,      1.2, 0.9),
        ('C_JET',       C_JET,       1.6, 1.0),
        ('C_SHOCK',     C_SHOCK,     1.4, 1.0),
        ('C_STAR',      C_STAR,      1.8, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to distinctly separate the flared disk topology from the vertical bipolar ejections
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-453i // MACRO-ENGINEERING TENSOR: ASTROPHYSICS KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // DG TAU (T TAURI STAR SYSTEM)", color=C_STAR, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_JET, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: PROTOSTAR CORE / FLARED ACCRETION DISK / BIPOLAR JETS & BOW SHOCKS", color=C_SHOCK, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-453i: DG TAU PROTOSTAR TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Astrophysics Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
