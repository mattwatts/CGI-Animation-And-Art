"""
PROJECT: Logic Garden 449x (Exact Physical Construct // Orbital Launch Vehicle Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: ROCKET, SOYUZ, R-7, SPACE LAUNCH, WIREFRAME, ENGINEERING, KINEMATICS, AEROSPACE
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: True parametric 54-metre lofting, offset conical strap-on boosters, dense corrugated structural stages, and 20-nozzle quad-engine arrays.
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
OUT_DIR = "frames_449x_rocket"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG            = '#FFFFFF'
C_TEXT          = '#111115'
C_HULL_MAIN     = '#1E293B'  # Carbon Slate (Smooth Stage Sections)
C_HULL_RIBS     = '#94A3B8'  # Machined Steel (Dense Corrugated Stages)
C_BOOSTER       = '#005599'  # Deep Marine (4x Outer Strap-on Cones)
C_FINS          = '#111115'  # Indestructible Black (Aerodynamic Stabilisers)
C_FAIRING       = '#111115'  # Indestructible Black (Payload Cone)
C_ENGINE        = '#D95F22'  # Industrial Amber (Thrust Nozzles)
C_GRID          = '#CBD5E1'  # Subdued Steel (Baseplate Reference)

# ------------------------------------------------------------------
# O(N) KINEMATIC WIREFRAME ENGINE
# ------------------------------------------------------------------
def project_3d_depth(x, y, z, cx, cy, cz, az_deg, el_deg=0):
    tx, ty, tz = x - cx, y - cy, z - cz
    az, el = np.radians(az_deg), np.radians(el_deg)
    
    # Orbit Matrix
    x1 = tx * np.cos(az) - ty * np.sin(az)
    y1 = tx * np.sin(az) + ty * np.cos(az)
    z1 = tz
    
    # Elevation Matrix
    y2 = y1 * np.cos(el) - z1 * np.sin(el)
    z2 = y1 * np.sin(el) + z1 * np.cos(el)
    
    return x1, z2, y2 

def append_segmented(lines_dict, key, xs, ys, zs):
    """Absolute Segmentation Protocol: Splits arrays into 2-point vectors for strict mathematical depth sorting."""
    for i in range(len(xs) - 1):
        lines_dict[key].append(([xs[i], xs[i+1]], [ys[i], ys[i+1]], [zs[i], zs[i+1]]))

def rotate_z_yaw_arr(x, y, z, cx, cy, yaw_deg):
    """Executes a pure Z-axis matrix rotation capable of handling scalar or NumPy arrays natively."""
    yw = np.radians(yaw_deg)
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    z_arr = np.asarray(z, dtype=float)
    
    x0 = x_arr - cx
    y0 = y_arr - cy
    x1 = x0 * np.cos(yw) - y0 * np.sin(yw)
    y1 = x0 * np.sin(yw) + y0 * np.cos(yw)
    
    return x1 + cx, y1 + cy, z_arr

def add_loft(lines_dict, key, z_arr, r_arr, cx=0.0, cy=0.0, t_count=24):
    """Parametric topological loft. Dynamically adjusts visual density via t_count for ribbed detailing."""
    z_arr = np.asarray(z_arr)
    r_arr = np.asarray(r_arr)
    
    # Transverse Hoops
    for i in range(len(z_arr)):
        t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
        hx = cx + r_arr[i] * np.cos(t)
        hy = cy + r_arr[i] * np.sin(t)
        hz = np.full_like(t, z_arr[i])
        append_segmented(lines_dict, key, list(hx)+[hx[0]], list(hy)+[hy[0]], list(hz)+[hz[0]])
        
    # Longitudinal Stringers
    for j in range(t_count):
        theta = j * (2*np.pi/t_count)
        sx = cx + r_arr * np.cos(theta)
        sy = cy + r_arr * np.sin(theta)
        sz = z_arr
        append_segmented(lines_dict, key, sx, sy, sz)

def generate_engine_nozzle(lines_dict, cx, cy, cz, col='C_ENGINE'):
    """Generates an explicit mechanical thrust bell matrix."""
    zn = np.array([0.0, 0.5, 1.2]) + cz
    rn = np.array([0.4, 0.15, 0.35])
    for i in range(len(zn)):
        t = np.linspace(0, 2*np.pi, 12, endpoint=False)
        x = cx + rn[i] * np.cos(t)
        y = cy + rn[i] * np.sin(t)
        z = np.full_like(t, zn[i])
        append_segmented(lines_dict, col, list(x)+[x[0]], list(y)+[y[0]], list(z)+[z[0]])
    for j in range(12):
        theta = j * (2*np.pi/12)
        sx = cx + rn * np.cos(theta)
        sy = cy + rn * np.sin(theta)
        append_segmented(lines_dict, col, sx, sy, zn)

# ------------------------------------------------------------------
# RIGID 3D EXACT KINEMATIC GENERATOR
# ------------------------------------------------------------------
def generate_rocket_vectors():
    lines = {
        'C_HULL_MAIN': [], 'C_HULL_RIBS': [], 'C_BOOSTER': [], 
        'C_FINS': [], 'C_FAIRING': [], 'C_ENGINE': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. BASEPLATE ENVELOPE (REFERENCE GRID)
    # ==============================================================================
    gx_range = np.linspace(-15, 15, 13) 
    for gx in gx_range:
        append_segmented(lines, 'C_GRID', np.full_like(gx_range, gx), np.clip(gx_range, -15, 15), np.zeros_like(gx_range))
    gy_range = np.linspace(-15, 15, 13)
    for gy in gy_range:
        append_segmented(lines, 'C_GRID', np.clip(gx_range, -15, 15), np.full_like(gx_range, gy), np.zeros_like(gx_range))

    # ==============================================================================
    # 2. CENTRAL CORE STAGE (R-7 Derived Substrate)
    # ==============================================================================
    # Base Flaring & Lower Stage
    z_core = [ 1.0,  3.0,  5.0,  15.0, 20.0, 23.0]
    r_core = [ 1.8,  1.9,  1.8,  1.8,  1.8,  1.6]
    add_loft(lines, 'C_HULL_MAIN', z_core, r_core, t_count=24)
    
    # Structural Void Transition
    add_loft(lines, 'C_HULL_MAIN', [23.0, 24.5], [1.6, 1.4], t_count=24)

    # First Dense Corrugated Stage (Machined Steel Ribs)
    z_rib1 = np.linspace(24.5, 29.5, 8)
    r_rib1 = np.full_like(z_rib1, 1.4)
    add_loft(lines, 'C_HULL_RIBS', z_rib1, r_rib1, t_count=48) # 48 points achieves high visual density

    # Midstage Inter-stage connection
    z_mid = [29.5, 33.0, 36.5]
    r_mid = [1.4, 1.4, 1.4]
    add_loft(lines, 'C_HULL_MAIN', z_mid, r_mid, t_count=24)

    # Second Dense Corrugated Stage
    z_rib2 = np.linspace(36.5, 41.5, 6)
    r_rib2 = np.full_like(z_rib2, 1.4)
    add_loft(lines, 'C_HULL_RIBS', z_rib2, r_rib2, t_count=48)

    # Payload Fairing (Double-taper explicit payload cone)
    z_fair = [41.5, 42.0, 47.0, 52.0, 54.0]
    r_fair = [1.4,  1.7,  1.7,  0.5,  0.0]
    add_loft(lines, 'C_FAIRING', z_fair, r_fair, t_count=24)

    # Central Core Quad-Engine Thrust Array
    for ang in [45, 135, 225, 315]:
        rad = np.radians(ang)
        generate_engine_nozzle(lines, 0.8 * np.cos(rad), 0.8 * np.sin(rad), -0.2)

    # ==============================================================================
    # 3. KINEMATIC STRAP-ON BOOSTERS (x4)
    # ==============================================================================
    # The blueprint explicitly models off-angle conical bodies nesting against the core.
    # We dynamically interpolate their central axis inward as altitude increases.
    z_b = np.array([ 1.0,  5.0, 10.0, 18.0, 22.0, 25.0])
    r_b = np.array([ 1.3,  1.6,  1.6,  0.9,  0.4,  0.0])
    cx_b = np.interp(z_b, [1.0, 25.0], [3.3, 1.45]) # Center tilts inwards to lay flush with the core (R=1.6)
    
    for angle in [0, 90, 180, 270]:
        # Aerodynamic Core Lofting
        for i in range(len(z_b)):
            t = np.linspace(0, 2*np.pi, 20, endpoint=False)
            hx = cx_b[i] + r_b[i] * np.cos(t)
            hy = r_b[i] * np.sin(t)
            hz = np.full_like(t, z_b[i])
            rx, ry, rz = rotate_z_yaw_arr(hx, hy, hz, 0, 0, angle)
            append_segmented(lines, 'C_BOOSTER', list(rx)+[rx[0]], list(ry)+[ry[0]], list(rz)+[rz[0]])
            
        for j in range(20):
            sx, sy, sz = [], [], []
            for i in range(len(z_b)):
                theta = j * (2*np.pi/20)
                lx = cx_b[i] + r_b[i] * np.cos(theta)
                ly = r_b[i] * np.sin(theta)
                lz = z_b[i]
                sx.append(lx); sy.append(ly); sz.append(lz)
            rx, ry, rz = rotate_z_yaw_arr(np.array(sx), np.array(sy), np.array(sz), 0, 0, angle)
            append_segmented(lines, 'C_BOOSTER', rx, ry, rz)
            
        # Heavy Outer Sub-Engines (Quad clusters per booster)
        base_cx, base_cy, _ = rotate_z_yaw_arr(cx_b[0], 0, 0, 0, 0, angle)
        for e_ang in [45, 135, 225, 315]:
            rad = np.radians(e_ang + angle) 
            generate_engine_nozzle(lines, base_cx + 0.7*np.cos(rad), base_cy + 0.7*np.sin(rad), -0.2)

        # Base Aerodynamic Stabiliser Fins
        # Mapped securely locking onto the extreme outer sweep of the booster matrix
        c_base = np.interp(1.5, z_b, cx_b)
        r_base = np.interp(1.5, z_b, r_b)
        
        fx = [c_base + r_base, c_base + r_base + 1.8, c_base + r_base + 1.8, np.interp(8.0, z_b, cx_b) + np.interp(8.0, z_b, r_b), c_base + r_base]
        fy = [0.0, 0.0, 0.0, 0.0, 0.0]
        fz = [1.0, 1.0, 3.5, 8.0, 1.0] # Closed explicit polygon
        
        rx, ry, rz = rotate_z_yaw_arr(np.array(fx), np.array(fy), np.array(fz), 0, 0, angle)
        append_segmented(lines, 'C_FINS', rx, ry, rz)
        
        # Inner structural rib for the fin
        fx_in = [c_base + r_base, c_base + r_base + 1.8]
        fz_in = [3.5, 3.5]
        rxi, ryi, rzi = rotate_z_yaw_arr(np.array(fx_in), np.array([0.0, 0.0]), np.array(fz_in), 0, 0, angle)
        append_segmented(lines, 'C_FINS', rxi, ryi, rzi)

    return lines

# ------------------------------------------------------------------
# PARALLEL GENERATOR STREAM (KINEMATIC TIMELINE TENSOR)
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_rocket_vectors() # Computed once for true O(1) loop retrieval
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Central Basepoint: Mapping exact structural centroid of the massive 54m chassis
        cam_x, cam_y, cam_z = 0.0, 0.0, 26.0 
        
        # Continuous 360-degree perfect orbital synchronisation
        # Initiates precisely from Right Side Profile (Azimuth = 90.0)
        azimuth = 90.0 - (stage * 360.0)

        yield (f, t_sec, azimuth, cam_x, cam_y, cam_z, static_rig)

# ------------------------------------------------------------------
# THREAD-SAFE PAINTER'S RENDERER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, azimuth, cx, cy, cz, static_rig = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # Cinematic Rigid Map Boundary - Covers the expansive 54m vertical tracking structure perfectly
    cam_span = 18.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []

    # 1. PROCESS KINEMATIC VECTOR MATRIX
    # Mapped with highly specific stroke parameters to amplify visual accuracy
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4),
        ('C_ENGINE',    C_ENGINE,    1.8, 1.0),
        ('C_FINS',      C_FINS,      1.5, 1.0),
        ('C_HULL_MAIN', C_HULL_MAIN, 1.2, 1.0),
        ('C_BOOSTER',   C_BOOSTER,   1.3, 1.0),
        ('C_HULL_RIBS', C_HULL_RIBS, 1.0, 0.9), # Narrower bounds yielding extreme density
        ('C_FAIRING',   C_FAIRING,   1.4, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=12.0)
            render_queue.append((np.mean(depth), u, v, c_val, lw, alpha))

    # 2. ABSOLUTE PAINTER'S ALGORITHM
    render_queue.sort(key=lambda item: item[0], reverse=True)

    for depth, u, v, c, lw, a in render_queue:
        ax.plot(u, v, color=c, lw=lw, alpha=a)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (TOP HUD)
    # ------------------------------------------------------------------
    ui_t = cam_span * 1.45
    ax.add_patch(patches.Rectangle((-cam_span, ui_t), cam_span*2, 10.0, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_t, ui_t], color=C_TEXT, lw=6, zorder=81)

    ax.text(-cam_span*0.95, ui_t+1.8, "LG-449x // MACRO-ENGINEERING TENSOR: AEROSPACE LOGISTICS", color=C_TEXT, fontsize=21, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t+0.5, "EXPLICIT TRUE-SCALE GEOMETRY // MULTI-STAGE ORBITAL LAUNCH VEHICLE", color=C_HULL_MAIN, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b+2.5, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_BOOSTER, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+1.3, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS SYNCHRONISATION)", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.1, "AERODYNAMIC YIELD: 4x STRAP-ON BOOSTERS & EXPLICIT DENSE CORRUGATION", color=C_HULL_RIBS, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-449x: ORBITAL LAUNCH VEHICLE TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
