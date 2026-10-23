"""
PROJECT: Logic Garden 453s (Exact Physical Construct // Kepler Space Telescope Matrix - HOTFIX)
FORMAT: YouTube Shorts (1080x1920)
METADATA: KEPLER, EXOPLANET, SPACE TELESCOPE, NASA, GLB, WIREFRAME, PYTHON
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional 4.7m orbital scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Hexagonal Bus, Schmidt Tube, Curved Solar Shield, Oblique Hood.
- Procedural Topography: High-density mesh mirroring asymmetrical hardware constraints.
- Hotfix: Resolved Scalar Iteration Fault in geometric primitives via np.full_like() propagation.
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
OUT_DIR = "frames_453s_kepler"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Orbital Tracking Grid)

C_BUS       = '#334155'          # Heavy Slate (Hexagonal Avionics Bus)
C_TUBE      = '#94A3B8'          # Slate Aluminium (Primary Schmidt Photometer Hull)
C_SHIELD    = '#005599'          # Deep Marine (Curved Photovoltaic Solar Array wrap)
C_HOOD      = '#1E293B'          # Carbon Slate (Oblique Sunshade Baffle)
C_ANTENNA   = '#CA8A04'          # Kapton Gold (Fixed HGA Telemetry Dish & Instruments)

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
    # Autonomously generates identical structural topology across the Y-axis (Port/Starboard Mirroring)
    if any(abs(y) > 0.001 for y in ys):
        append_segmented(lines_dict, key, xs, [-y for y in ys], zs)

# ------------------------------------------------------------------
# GEOMETRIC PRIMITIVES (HOTFIXED SCALAR ITERATION FAULTS)
# ------------------------------------------------------------------
def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='z', rings=4, t_count=16, reflect_y=False):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, length, rings)
    for s in steps:
        # HOTFIX: Explicitly mapping np.full_like() to array propagating axes
        if axis == 'x':  
            ix, iy, iz = np.full_like(t, cx + s), cy + radius*np.cos(t), cz + radius*np.sin(t)
        elif axis == 'y':
            ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + s), cz + radius*np.sin(t)
        else:            
            ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), np.full_like(t, cz + s)
            
        if reflect_y: append_sym(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
        else: append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
        
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        if axis == 'x':  sx, sy, sz = cx + steps, [cy + radius*np.cos(a)]*rings, [cz + radius*np.sin(a)]*rings
        elif axis == 'y':sx, sy, sz = [cx + radius*np.cos(a)]*rings, cy + steps, [cz + radius*np.sin(a)]*rings
        else:            sx, sy, sz = [cx + radius*np.cos(a)]*rings, [cy + radius*np.sin(a)]*rings, cz + steps
        if reflect_y: append_sym(lines_dict, col, sx, sy, sz)
        else: append_segmented(lines_dict, col, sx, sy, sz)

def add_partial_cylinder(lines_dict, col, cx, cy, cz, length, radius, theta_start, theta_end, rings=5, t_count=16, reflect_y=False):
    t = np.linspace(theta_start, theta_end, t_count)
    steps = np.linspace(0, length, rings)
    
    for s in steps:
        ix = cx + radius * np.cos(t)
        iy = cy + radius * np.sin(t)
        iz = np.full_like(t, cz + s)
        if reflect_y: append_sym(lines_dict, col, ix, iy, iz)
        else: append_segmented(lines_dict, col, ix, iy, iz)
        
    for a in t:
        sx = cx + radius * np.cos(a) * np.ones_like(steps)
        sy = cy + radius * np.sin(a) * np.ones_like(steps)
        sz = cz + steps
        if reflect_y: append_sym(lines_dict, col, sx, sy, sz)
        else: append_segmented(lines_dict, col, sx, sy, sz)

def add_cone_frustum(lines_dict, col, cx, cy, cz, dz, r1, r2, axis='z', rings=4, t_count=16, reflect_y=False):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, dz, rings)
    r_step = np.linspace(r1, r2, rings)
    
    for i, s in enumerate(steps):
        r = r_step[i]
        # HOTFIX: Explicitly mapping np.full_like() to array propagating axes
        if axis == 'x':  
            ix, iy, iz = np.full_like(t, cx + s), cy + r*np.cos(t), cz + r*np.sin(t)
        elif axis == 'y':
            ix, iy, iz = cx + r*np.cos(t), np.full_like(t, cy + s), cz + r*np.sin(t)
        else:            
            ix, iy, iz = cx + r*np.cos(t), cy + r*np.sin(t), np.full_like(t, cz + s)
        if reflect_y: append_sym(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
        else: append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        sx, sy, sz = [], [], []
        for i, s in enumerate(steps):
            r = r_step[i]
            if axis == 'x':  sx.append(cx + s); sy.append(cy + r*np.cos(a)); sz.append(cz + r*np.sin(a))
            elif axis == 'y':sx.append(cx + r*np.cos(a)); sy.append(cy + s); sz.append(cz + r*np.sin(a))
            else:            sx.append(cx + r*np.cos(a)); sy.append(cy + r*np.sin(a)); sz.append(cz + s)
        if reflect_y: append_sym(lines_dict, col, sx, sy, sz)
        else: append_segmented(lines_dict, col, sx, sy, sz)

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (KEPLER SPACE TELESCOPE)
# ------------------------------------------------------------------
def generate_kepler_static():
    lines = {
        'C_BUS': [], 'C_TUBE': [], 'C_SHIELD': [],
        'C_HOOD': [], 'C_ANTENNA': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. ORBITAL TRACKING BASEPLATE (Simulation Space)
    # ==============================================================================
    Z_FLOOR = -2.0
    for r_p in [2.0, 4.0, 6.0]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-6.0, 6.0, 19)
    gy_range = np.linspace(-6.0, 6.0, 19)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. SPACECRAFT BUS (The Hexagonal Avionics Root)
    # ==============================================================================
    R_BUS = 1.35
    Z_BUS_BOT = 0.0
    Z_BUS_TOP = 1.0
    
    # Natively calculating an explicit hexagonal prism (t_count=6)
    add_cylinder(lines, 'C_BUS', cx=0.0, cy=0.0, cz=Z_BUS_BOT, length=(Z_BUS_TOP - Z_BUS_BOT), radius=R_BUS, axis='z', rings=4, t_count=6, reflect_y=False)
    
    # Base closure ring
    t6 = np.linspace(0, 2*np.pi, 6, endpoint=False)
    for t in t6:
        cx_p, cy_p = R_BUS * np.cos(t), R_BUS * np.sin(t)
        append_segmented(lines, 'C_BUS', [0.0, cx_p], [0.0, cy_p], [Z_BUS_BOT, Z_BUS_BOT])
        append_segmented(lines, 'C_BUS', [0.0, cx_p], [0.0, cy_p], [Z_BUS_TOP, Z_BUS_TOP])

    # ==============================================================================
    # 3. SCHMIDT PHOTOMETER (The Primary Optical Tube)
    # ==============================================================================
    R_TUBE = 1.1
    Z_TUBE_TOP = 4.0
    # Dense cylindrical resolution to differentiate from the angular bus
    add_cylinder(lines, 'C_TUBE', cx=0.0, cy=0.0, cz=Z_BUS_TOP, length=(Z_TUBE_TOP - Z_BUS_TOP), radius=R_TUBE, axis='z', rings=10, t_count=32, reflect_y=False)
    
    # Telescope aperture structural ring at Z=4.0
    add_cylinder(lines, 'C_HOOD', cx=0.0, cy=0.0, cz=Z_TUBE_TOP-0.1, length=0.1, radius=R_TUBE+0.05, axis='z', rings=2, t_count=32, reflect_y=False)

    # ==============================================================================
    # 4. ASYMMETRICAL SOLAR ARRAY AND SUNSHIELD
    # ==============================================================================
    # Transversally wrapping the +X hemisphere facing the sun.
    # Extending beyond the tube radius slightly (R=1.3)
    R_SHIELD = 1.3
    Z_SHIELD_TOP = 4.2
    
    # Generates exclusively across the forward arc (-pi/2 to pi/2)
    add_partial_cylinder(lines, 'C_SHIELD', cx=0.0, cy=0.0, cz=Z_BUS_TOP, length=(Z_SHIELD_TOP - Z_BUS_TOP), 
                         radius=R_SHIELD, theta_start=-np.pi/2, theta_end=np.pi/2, rings=8, t_count=17, reflect_y=False)

    # ==============================================================================
    # 5. OBLIQUE APERTURE HOOD (Asymmetrical Baffle)
    # ==============================================================================
    # Reaching upwards specifically on the +X sun-facing side to Z=4.7m
    # We dynamically calculate a sliced cylinder using explicit trigonometric bounding
    t_hood = np.linspace(-np.pi/2, np.pi/2, 17)
    
    for th in t_hood:
        hx = R_TUBE * np.cos(th)
        hy = R_TUBE * np.sin(th)
        # Oblique cut: Z extends higher on +X, scales down to Z_TUBE_TOP at Y-extents
        # Equation: max_z = Z_TUBE_TOP + 0.7 * cos(th)
        z_peak = Z_TUBE_TOP + 0.7 * np.cos(th)
        
        # Vertical extrusion lines
        append_segmented(lines, 'C_HOOD', [hx, hx], [hy, hy], [Z_TUBE_TOP, z_peak])
        
    # The slanted continuous leading edge of the hood
    hz_array = Z_TUBE_TOP + 0.7 * np.cos(t_hood)
    hx_array = R_TUBE * np.cos(t_hood)
    hy_array = R_TUBE * np.sin(t_hood)
    append_segmented(lines, 'C_HOOD', hx_array, hy_array, hz_array)

    # ==============================================================================
    # 6. FIXED HIGH-GAIN ANTENNA (HGA)
    # ==============================================================================
    # Rigid telemetry mount locked underneath the primary bus
    add_cylinder(lines, 'C_ANTENNA', cx=0.0, cy=-R_BUS, cz=0.5, length=-0.6, radius=0.08, axis='y', rings=2, t_count=8, reflect_y=False)
    
    # 0.8m diameter dish facing towards Earth (approx -Y and slight Z pitch)
    add_cone_frustum(lines, 'C_ANTENNA', cx=0.0, cy=-R_BUS-0.6, cz=0.5, dz=-0.2, r1=0.08, r2=0.4, axis='y', rings=4, t_count=20, reflect_y=False)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_kepler_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry midway up the Schmidt Tube
        cam_x, cam_y, cam_z = 0.0, 0.0, 1.5
        
        # Starts explicitly from 115-degrees (Dramatic aesthetic showcasing the curved shield and angled hood)
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
    # Anchor Centroid = Z=1.5m. The observatory extents stretch from Z=4.7m (Upper Hood) down to Z=0.0m (Bus Base).
    # Transversally, the solar shield runs +/- 1.3m, and the HGA reaches approximately Y = -2.1m.
    # Setting cam_span strictly to 3.5 locks horizontal width symmetrically across a 7.0m geometrical span.
    # Vertical bounds output 3.5 * 1.777 = 6.22m half-height (total transparent window 12.4m).
    # Perfectly traps the extreme asymmetric hood cut and base telemetry antenna safely inside the viewport overhead.
    cam_span = 3.5
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_BUS',       C_BUS,       1.4, 1.0),
        ('C_ANTENNA',   C_ANTENNA,   1.5, 1.0),
        ('C_TUBE',      C_TUBE,      1.2, 1.0),
        ('C_HOOD',      C_HOOD,      1.4, 1.0),
        ('C_SHIELD',    C_SHIELD,    1.6, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to parse the exact hexagonal corners against the perfectly smooth primary tube
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-453s // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // KEPLER SPACE TELESCOPE MATRIX", color=C_BUS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_SHIELD, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: HEXAGONAL AVIONICS / SCHMIDT TUBE / WRAPAROUND SHIELD / OBLIQUE HOOD", color=C_SHIELD, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-453s: KEPLER SPACE TELESCOPE TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
