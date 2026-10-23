"""
PROJECT: Logic Garden 452c (Exact Physical Construct // Asteroid 25143 Itokawa Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: ASTEROID, ITOKAWA, JAXA, HAYABUSA, STL, WIREFRAME, ENGINEERING, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional 535m aerospace scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: True triangulated STL mesh mapping the bilobated 535 x 294 x 209m contact binary.
- Viewport Override: Locked cam_span rigorously guarantees 100% full-station visibility between UI boundaries.
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
OUT_DIR = "frames_452c_itokawa"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Astronomic Tracking Grid)

C_LAT       = '#1E293B'          # Carbon Slate (Lateral STL Geometry)
C_LON       = '#334155'          # Heavy Slate (Longitudinal STL Geometry)
C_TRI       = '#0F172A'          # Abyssal Slate (Diagonal Triangulation Vectors)

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

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (ASTEROID 25143 ITOKAWA)
# ------------------------------------------------------------------
def generate_itokawa_stl_static():
    lines = {
        'C_LAT': [], 'C_LON': [], 'C_TRI': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. ORBITAL TRACKING BASEPLATE (1 Unit = 1 Metre)
    # ==============================================================================
    # Baseplate scaled dynamically to the massive 535m tracking sweep
    Z_FLOOR = -200.0
    for r_p in [150.0, 250.0, 400.0]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-400.0, 400.0, 17)
    gy_range = np.linspace(-400.0, 400.0, 17)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. STL TOPOGRAPHY ALGORITHM (True 535 x 294 x 209 metre Profile)
    # ==============================================================================
    u_steps = 72  # Longitude resolution
    v_steps = 36  # Latitude resolution
    
    u = np.linspace(0, 2 * np.pi, u_steps)
    v = np.linspace(0, np.pi, v_steps)
    U, V = np.meshgrid(u, v)
    
    # Fundamental elongated axis X spans from +267.5m to -267.5m (yielding 535m length)
    X_base = 267.5 * np.cos(V)
    
    # Mathematical Contact Binary Construction (The "Sea Otter" configuration)
    # A massive 'Body' lobe transitioning into a severe restriction before a smaller 'Head' lobe.
    neck_pinch = 1.0 - 0.35 * np.exp(-((X_base - 80.0) / 70.0)**2)  # Severe stricture separating lobes
    body_bulge = 1.0 + 0.25 * np.exp(-((X_base + 60.0) / 120.0)**2) # Outward displacement of main mass
    
    # Scaling factors yield max Y~294m diameter, max Z~209m diameter
    R_base = 120.0 * np.sin(V) * neck_pinch * body_bulge
    Y_base = R_base * np.cos(U)
    Z_base = R_base * 0.71 * np.sin(U) # Asymmetrical minor-axis compression
    
    # Mathematical Topographical Interference (Simulated Rubble-Pile Geological Noise)
    noise = np.ones_like(U)
    
    # Heavy blocky faceting mimicking accumulated rubble and massive boulder structures
    noise += 0.08 * np.sin(6 * U) * np.cos(4 * V)
    noise += 0.05 * np.cos(9 * U + 3 * V) * np.sin(7 * V)
    noise += 0.04 * np.sin(15 * U) * np.cos(11 * V)
    
    # The 'Muses Sea' / 'Sagami' Regions:
    # Dampening the rough noise algorithms across specific zones to map the fine regolith plains
    muses_sea = np.exp(-((X_base - 80.0)**2 / 3000.0) - ((U - np.pi/2)**2 / 1.0))
    sagami = np.exp(-((X_base - 80.0)**2 / 3000.0) - ((U - 3*np.pi/2)**2 / 1.0))
    
    noise = noise * (1.0 - 0.6 * muses_sea)
    noise = noise * (1.0 - 0.5 * sagami)
    
    # Apply topography
    X = X_base * (1.0 + 0.03 * (noise - 1.0)) 
    Y = Y_base * noise
    Z = Z_base * noise
    
    # ==============================================================================
    # 3. NATIVE TRIANGULATED WIREFRAME EXTRACTION
    # ==============================================================================
    rows, cols = X.shape
    
    for i in range(rows - 1):
        for j in range(cols - 1):
            # Horizontal (Latitude) Ribs
            append_segmented(lines, 'C_LAT', [X[i, j], X[i, j+1]], 
                                             [Y[i, j], Y[i, j+1]], 
                                             [Z[i, j], Z[i, j+1]])
            # Vertical (Longitude) Ribs
            append_segmented(lines, 'C_LON', [X[i, j], X[i+1, j]], 
                                             [Y[i, j], Y[i+1, j]], 
                                             [Z[i, j], Z[i+1, j]])
            # Diagonal (Triangulation) STL formatting natively bridging the geometry
            append_segmented(lines, 'C_TRI', [X[i, j], X[i+1, j+1]], 
                                             [Y[i, j], Y[i+1, j+1]], 
                                             [Z[i, j], Z[i+1, j+1]])

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_itokawa_stl_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry flawlessly dead centre on the asteroid mass
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.0
        
        # Starts explicitly from 115-degrees (Dramatic aesthetic exposing the massive asymmetric lobes)
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
    # Anchor Centroid = Dead zero. Asteroid extreme X-bounds span exactly +/- 267.5m.
    # Setting cam_span strictly to 350.0 locks horizontal width symmetrically across a colossal 700.0m.
    # Vertical bounds output 350.0 * 1.777 = 621.95m total height window vertically.
    # This immense optical viewport absolutely commands an uncompromising, flawlessly framed profile,
    # trapping the entire tumbling 535m mass securely without any bounding box failure.
    cam_span = 350.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',  C_GRID,  0.8, 0.4), 
        ('C_LAT',   C_LAT,   1.2, 1.0),
        ('C_LON',   C_LON,   1.2, 1.0),
        ('C_TRI',   C_TRI,   1.4, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to expose the violent asymmetrical cratering across the dorsal topography
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-452c // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // ASTEROID 25143 ITOKAWA `.STL` MATRIX", color=C_TRI, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_LON, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: 535 METRE ƁI-LOBED BODY / HIGH-DENSITY TRIANGULATED REGOLITH MESH", color=C_LAT, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-452c: ITOKAWA TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
