"""
PROJECT: Logic Garden 453c (Exact Physical Construct // Chandra X-ray Observatory Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: CHANDRA, X-RAY, OBSERVATORY, NASA, GLB, WIREFRAME, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional deep-space telescope scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: HRMA Sunshade, Octagonal Bus, Optical Bench, SIM Subsystem, 19.5m PV Arrays.
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
OUT_DIR = "frames_453c_chandra"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Interplanetary Tracking Grid)

C_BUS       = '#CA8A04'          # Kapton Gold (Spacecraft Control Module MLI)
C_HRMA      = '#94A3B8'          # Slate Aluminium (Forward Sunshade & Mirror Assembly)
C_BENCH     = '#334155'          # Heavy Slate (10-Metre Composite Optical Bench)
C_SIM       = '#1E293B'          # Carbon Slate (Science Instrument Module & Reaction Wheels)
C_SOLAR     = '#005599'          # Deep Marine (19.5m Transverse Photovoltaic Wings)
C_HARDWARE  = '#0F172A'          # Abyssal Slate (Telemetry Antennas & Aperture Door)

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
    # Reflect mapping strictly for symmetrical arrays (e.g., PV wings along Y)
    if any(abs(y) > 0.001 for y in ys):
        append_segmented(lines_dict, key, xs, [-y for y in ys], zs)

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
        append_sym(lines_dict, col, [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts])
    for i in range(u_steps + 1):
        u = i / u_steps
        start = p1 * (1-u) + p2 * u
        end   = p4 * (1-u) + p3 * u
        pts = [start * (1-v) + end * v for v in np.linspace(0, 1, v_steps+1)]
        append_sym(lines_dict, col, [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts])

def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='z', rings=4, t_count=16):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, length, rings)
    for s in steps:
        if axis == 'x':  ix, iy, iz = np.full_like(t, cx + s), cy + radius*np.cos(t), np.full_like(t, cz + radius*np.sin(t)) if cz == 0 else cz + radius*np.sin(t)
        elif axis == 'y':ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + s), np.full_like(t, cz + radius*np.sin(t)) if cz == 0 else cz + radius*np.sin(t)
        else:            ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), np.full_like(t, cz + s)
        append_sym(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        if axis == 'x':  sx, sy, sz = cx + steps, [cy + radius*np.cos(a)]*rings, [cz + radius*np.sin(a)]*rings
        elif axis == 'y':sx, sy, sz = [cx + radius*np.cos(a)]*rings, cy + steps, [cz + radius*np.sin(a)]*rings
        else:            sx, sy, sz = [cx + radius*np.cos(a)]*rings, [cy + radius*np.sin(a)]*rings, cz + steps
        append_sym(lines_dict, col, sx, sy, sz)

def add_cone_frustum(lines_dict, col, cx, cy, cz, dz, r1, r2, axis='z', rings=4, t_count=16):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, dz, rings)
    r_step = np.linspace(r1, r2, rings)
    
    for i, s in enumerate(steps):
        r = r_step[i]
        if axis == 'x':  
            ix, iy, iz = np.full_like(t, cx + s), cy + r*np.cos(t), np.full_like(t, cz + r*np.sin(t)) if cz == 0 else cz + r*np.sin(t)
        elif axis == 'y':
            ix, iy, iz = cx + r*np.cos(t), np.full_like(t, cy + s), np.full_like(t, cz + r*np.sin(t)) if cz == 0 else cz + r*np.sin(t)
        else:            
            ix, iy, iz = cx + r*np.cos(t), cy + r*np.sin(t), np.full_like(t, cz + s)
        append_sym(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        sx, sy, sz = [], [], []
        for i, s in enumerate(steps):
            r = r_step[i]
            if axis == 'x':  sx.append(cx + s); sy.append(cy + r*np.cos(a)); sz.append(cz + r*np.sin(a))
            elif axis == 'y':sx.append(cx + r*np.cos(a)); sy.append(cy + s); sz.append(cz + r*np.sin(a))
            else:            sx.append(cx + r*np.cos(a)); sy.append(cy + r*np.sin(a)); sz.append(cz + s)
        append_sym(lines_dict, col, sx, sy, sz)

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (CHANDRA X-RAY OBSERVATORY)
# ------------------------------------------------------------------
def generate_chandra_static():
    lines = {
        'C_BUS': [], 'C_HGA': [], 'C_BENCH': [],
        'C_SIM': [], 'C_SOLAR': [], 'C_HRMA': [], 
        'C_HARDWARE': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. INTERPLANETARY TRACKING BASEPLATE (1 Unit = 1 Metre)
    # ==============================================================================
    Z_FLOOR = -5.0
    for r_p in [5.0, 10.0, 15.0]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        # Direct generation bypassing append_sym to prevent grid overlap
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-15.0, 15.0, 19)
    gy_range = np.linspace(-15.0, 15.0, 19)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. SPACECRAFT MODULE (CENTRAL BUS)
    # ==============================================================================
    # Octagonal control block housing avionics, communications, and power manifolds
    Z_BUS_AFT = -0.5
    Z_BUS_FWD = 2.0
    R_BUS = 1.45
    
    add_cylinder(lines, 'C_BUS', cx=0.0, cy=0.0, cz=Z_BUS_AFT, length=(Z_BUS_FWD - Z_BUS_AFT), radius=R_BUS, axis='z', rings=5, t_count=8)

    # ==============================================================================
    # 3. HIGH-RESOLUTION MIRROR ASSEMBLY (HRMA) & SUNSHADE
    # ==============================================================================
    # Forward tubular shield protecting the nested grazing optics
    Z_HRMA_FWD = 5.5
    Z_APERTURE_DOOR = Z_HRMA_FWD + 1.2
    
    # Outer sunshade frustum
    add_cone_frustum(lines, 'C_HRMA', cx=0.0, cy=0.0, cz=Z_BUS_FWD, dz=(Z_HRMA_FWD - Z_BUS_FWD), r1=R_BUS, r2=1.1, axis='z', rings=4, t_count=16)

    # Deployed Angular Aperture Door (Pitched open 45-degrees)
    # Mapped natively using pure XYZ boundaries
    door_p1 = np.array([-1.1,  0.0, Z_HRMA_FWD])       # Hinge base center
    door_p2 = np.array([-1.1,  0.9, Z_HRMA_FWD])       # Hinge base +Y
    door_p3 = np.array([-1.1 + 1.8,  0.9, Z_APERTURE_DOOR])
    door_p4 = np.array([-1.1 + 1.8,  0.0, Z_APERTURE_DOOR])
    
    add_quad_mesh(lines, 'C_HARDWARE', door_p1, door_p2, door_p3, door_p4, u_steps=2, v_steps=2)

    # ==============================================================================
    # 4. CARBON-COMPOSITE OPTICAL BENCH
    # ==============================================================================
    # 10m focal length tube physically transmitting the X-ray trajectory aft
    Z_BENCH_AFT = -5.8
    # Gentle taper along the Z vector
    add_cone_frustum(lines, 'C_BENCH', cx=0.0, cy=0.0, cz=Z_BUS_AFT, dz=(Z_BENCH_AFT - Z_BUS_AFT), r1=1.2, r2=1.0, axis='z', rings=7, t_count=12)

    # ==============================================================================
    # 5. SCIENCE INSTRUMENT MODULE (SIM)
    # ==============================================================================
    # Massive rear block processing the optical feed (ACIS & HRC housing)
    Z_SIM_AFT = -7.8
    
    # Forward interface ring
    add_cylinder(lines, 'C_HARDWARE', cx=0.0, cy=0.0, cz=Z_BENCH_AFT-0.2, length=0.2, radius=1.3, axis='z', rings=2, t_count=12)
    # Primary SIM Payload Housing
    add_cylinder(lines, 'C_SIM', cx=0.0, cy=0.0, cz=Z_SIM_AFT, length=(Z_BENCH_AFT - 0.2 - Z_SIM_AFT), radius=1.25, axis='z', rings=4, t_count=12)

    # ==============================================================================
    # 6. 19.5M PHOTOVOLTAIC SOLAR ARRAYS
    # ==============================================================================
    # Massive articulated solar wings mapping the deep space solar harvest bounds.
    # The native append_sym will force a perfect mathematical reflection to -Y (Starboard).
    Y_WING_ROOT = 1.7
    Y_WING_TIP = 9.75
    X_SPAN = 1.25   # Wing width: 2.5m
    Z_WING = 0.5    # Deployed from Spacecraft Module centerline
    
    # Mounting Strut (+Y)
    add_cylinder(lines, 'C_HARDWARE', cx=0.0, cy=0.0, cz=Z_WING, length=Y_WING_ROOT, radius=0.15, axis='y', rings=3, t_count=8)

    # High-Density Deployed Photovoltaic Quad-Mesh Array (+Y limits, mathematically mirrored identically)
    add_quad_mesh(lines, 'C_SOLAR', 
                  (-X_SPAN, Y_WING_ROOT, Z_WING), (X_SPAN, Y_WING_ROOT, Z_WING), 
                  (X_SPAN, Y_WING_TIP, Z_WING), (-X_SPAN, Y_WING_TIP, Z_WING), 
                  u_steps=3, v_steps=12)
                  
    # Structural Backing Spines (-Z offset mapping solar sail rigidity)
    append_sym(lines, 'C_HARDWARE', [0.0, 0.0], [Y_WING_ROOT, Y_WING_TIP], [Z_WING-0.05, Z_WING-0.05])

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_chandra_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry flawlessly at payload centroid (Z=0.0)
        # Length boundaries run from approximately Z=-7.8 to Z=+6.7
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.0
        
        # Starts explicitly from 115-degrees (Dramatic aesthetic exposing the massive arrays and forward sunshade)
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
    # Anchor Centroid = Dead zero. Solar arrays reach extreme bounds at Y=+/- 9.75m. 
    # Observatory longitudinal length extends to ~13.8m.
    # Setting cam_span strictly to 14.0 locks horizontal width symmetrically across a massive 28.0m view.
    # Vertical bounds output 14.0 * 1.777 = 24.8m total height window vertically.
    # Completely traps the deeply extended observatory architecture safely inside the transparent viewport, immune to UI overlay clipping.
    cam_span = 14.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_BUS',       C_BUS,       1.4, 1.0),
        ('C_BENCH',     C_BENCH,     1.3, 1.0),
        ('C_SIM',       C_SIM,       1.5, 1.0),
        ('C_SOLAR',     C_SOLAR,     1.2, 1.0),
        ('C_HARDWARE',  C_HARDWARE,  1.1, 1.0),
        ('C_HRMA',      C_HRMA,      1.6, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to parse the sprawling horizontal wings against the deep Z-axis optical bench
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-453c // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // CHANDRA X-RAY OBSERVATORY", color=C_BUS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_SOLAR, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: 13.8M OBSERVATORY / HRMA SUNSHADE / OPTICAL BENCH / 19.5M PV WINGS", color=C_HRMA, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-453c: CHANDRA X-RAY OBSERVATORY TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
