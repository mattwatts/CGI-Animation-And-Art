"""
PROJECT: Logic Garden 453l (Exact Physical Construct // RQ-4 Global Hawk Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: GLOBAL HAWK, RQ-4, UAV, AEROSPACE, GLB, WIREFRAME, KINEMATICS, PYTHON
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional 40m wingspan scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: SATCOM Radome, 39.9m Wingspan, Dorsal Engine, V-Tail, Ventral Radars.
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
OUT_DIR = "frames_453l_global_hawk"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Tarmac Tracking Grid)

C_HULL      = '#334155'          # Heavy Slate (Primary Fuselage & Prominent SATCOM Radome)
C_WINGS     = '#005599'          # Deep Marine (39.9m High Aspect Ratio Wings & V-Tail)
C_ENGINE    = '#1E293B'          # Carbon Slate (Dorsal AE 3007H Turbofan Nacelle)
C_EXHAUST   = '#E11D48'          # Kinematic Red (Aft Exhaust Nozzle Boundary)
C_SENSORS   = '#CA8A04'          # Kapton Gold (Ventral SAR & EO/IR Target Blisters)

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
# GEOMETRIC PRIMITIVES
# ------------------------------------------------------------------
def add_quad_mesh(lines_dict, col, p1, p2, p3, p4, u_steps=4, v_steps=4, reflect_y=True):
    p1, p2, p3, p4 = map(np.array, (p1, p2, p3, p4))
    for i in range(v_steps + 1):
        v = i / v_steps
        start = p1 * (1-v) + p4 * v
        end   = p2 * (1-v) + p3 * v
        pts = [start * (1-u) + end * u for u in np.linspace(0, 1, u_steps+1)]
        if reflect_y:
            append_sym(lines_dict, col, [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts])
        else:
            append_segmented(lines_dict, col, [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts])
    for i in range(u_steps + 1):
        u = i / u_steps
        start = p1 * (1-u) + p2 * u
        end   = p4 * (1-u) + p3 * u
        pts = [start * (1-v) + end * v for v in np.linspace(0, 1, v_steps+1)]
        if reflect_y:
            append_sym(lines_dict, col, [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts])
        else:
            append_segmented(lines_dict, col, [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts])

def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='z', rings=4, t_count=16, reflect_y=False):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, length, rings)
    for s in steps:
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

def add_cone_frustum(lines_dict, col, cx, cy, cz, dz, r1, r2, axis='x', rings=4, t_count=16, reflect_y=False):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, dz, rings)
    r_step = np.linspace(r1, r2, rings)
    
    for i, s in enumerate(steps):
        r = r_step[i]
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

def add_ellipsoid(lines_dict, col, cx, cy, cz, rx, ry, rz, rings=8, t_count=16, reflect_y=False):
    theta = np.linspace(-np.pi/2, np.pi/2, rings)
    phi = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    
    for th in theta:
        xs = cx + rx * np.cos(th) * np.cos(phi)
        ys = cy + ry * np.cos(th) * np.sin(phi)
        zs = cz + rz * np.sin(th) * np.ones_like(phi)
        if reflect_y: append_sym(lines_dict, col, list(xs)+[xs[0]], list(ys)+[ys[0]], list(zs)+[zs[0]])
        else: append_segmented(lines_dict, col, list(xs)+[xs[0]], list(ys)+[ys[0]], list(zs)+[zs[0]])
        
    for ph in phi:
        xs = cx + rx * np.cos(theta) * np.cos(ph)
        ys = cy + ry * np.cos(theta) * np.sin(ph)
        zs = cz + rz * np.sin(theta)
        if reflect_y: append_sym(lines_dict, col, xs, ys, zs)
        else: append_segmented(lines_dict, col, xs, ys, zs)

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (GLOBAL HAWK)
# ------------------------------------------------------------------
def generate_global_hawk_static():
    lines = {
        'C_HULL': [], 'C_WINGS': [], 'C_ENGINE': [],
        'C_EXHAUST': [], 'C_SENSORS': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. TARMAC TRACKING BASEPLATE (1 Unit = 1 Metre)
    # ==============================================================================
    # Ground tracking grid safely below the belly sensors and landing gear limits
    Z_FLOOR = -2.5
    for r_p in [8.0, 16.0, 24.0]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-24.0, 24.0, 25)
    gy_range = np.linspace(-24.0, 24.0, 25)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. PRIMARY FUSELAGE & SATCOM RADOME
    # ==============================================================================
    # Main continuous tubular body
    add_cylinder(lines, 'C_HULL', cx=-6.0, cy=0.0, cz=0.0, length=12.0, radius=0.6, axis='x', rings=12, t_count=20, reflect_y=False)
    
    # Sharp Tail Taper (-X geometry)
    add_cone_frustum(lines, 'C_HULL', cx=-6.0, cy=0.0, cz=0.0, dz=-1.25, r1=0.6, r2=0.05, axis='x', rings=3, t_count=20, reflect_y=False)
    
    # Sharp Chin Nose Cone (+X geometry under the radome)
    add_cone_frustum(lines, 'C_HULL', cx=6.0, cy=0.0, cz=0.0, dz=1.25, r1=0.6, r2=0.1, axis='x', rings=3, t_count=20, reflect_y=False)

    # Massive Distinctive SATCOM Radome Hump (Dorsal Forehead)
    # Physically houses the 1.2m Ku-Band communications dish
    add_ellipsoid(lines, 'C_HULL', cx=5.0, cy=0.0, cz=0.3, rx=2.2, ry=0.75, rz=1.1, rings=8, t_count=20, reflect_y=False)

    # ==============================================================================
    # 3. HIGH-ASPECT RATIO WINGS & EMPENNAGE
    # ==============================================================================
    # Massive 39.9-metre wingspan (Y = +/- 19.95m). Characteristically extremely narrow chord.
    WING_ROOT_X = 0.5
    WING_ROOT_CHORD = 1.6
    WING_TIP_X = -1.0       # Slight rearward sweep
    WING_TIP_CHORD = 0.4
    WING_SPAN_Y = 19.95
    
    # Port / Starboard Wing Matrices
    add_quad_mesh(lines, 'C_WINGS', 
                  (WING_ROOT_X, 0.6, 0.2), (WING_TIP_X, WING_SPAN_Y, 0.4), 
                  (WING_TIP_X - WING_TIP_CHORD, WING_SPAN_Y, 0.4), (WING_ROOT_X - WING_ROOT_CHORD, 0.6, 0.2), 
                  u_steps=5, v_steps=15, reflect_y=True)
    add_quad_mesh(lines, 'C_WINGS', 
                  (WING_ROOT_X, 0.6, 0.1), (WING_TIP_X, WING_SPAN_Y, 0.35), 
                  (WING_TIP_X - WING_TIP_CHORD, WING_SPAN_Y, 0.35), (WING_ROOT_X - WING_ROOT_CHORD, 0.6, 0.1), 
                  u_steps=5, v_steps=15, reflect_y=True)

    # V-Tail Empennage (Canted outwards heavily to clear engine exhaust)
    # Mounted natively at X = -6.0.
    VTAIL_ROOT_X = -5.8
    VTAIL_ROOT_CHORD = 1.2
    VTAIL_TIP_X = -7.5
    VTAIL_TIP_CHORD = 0.5
    VTAIL_SPAN_Y = 2.4
    VTAIL_SPAN_Z = 2.2
    
    add_quad_mesh(lines, 'C_WINGS', 
                  (VTAIL_ROOT_X, 0.4, 0.4), (VTAIL_TIP_X, VTAIL_SPAN_Y, VTAIL_SPAN_Z),
                  (VTAIL_TIP_X - VTAIL_TIP_CHORD, VTAIL_SPAN_Y, VTAIL_SPAN_Z), (VTAIL_ROOT_X - VTAIL_ROOT_CHORD, 0.4, 0.4), 
                  u_steps=3, v_steps=6, reflect_y=True)
    add_quad_mesh(lines, 'C_WINGS', 
                  (VTAIL_ROOT_X, 0.4, 0.3), (VTAIL_TIP_X, VTAIL_SPAN_Y, VTAIL_SPAN_Z - 0.05),
                  (VTAIL_TIP_X - VTAIL_TIP_CHORD, VTAIL_SPAN_Y, VTAIL_SPAN_Z - 0.05), (VTAIL_ROOT_X - VTAIL_ROOT_CHORD, 0.4, 0.3), 
                  u_steps=3, v_steps=6, reflect_y=True)

    # ==============================================================================
    # 4. DORSAL ENGINE NACELLE (AE 3007H TURBOFAN)
    # ==============================================================================
    # Elevated along the dorsal spine specifically to mask the infrared exhaust plume from ground tracking
    ENG_Z = 1.3
    
    # Central Pylon fairing bridging the fuselage to the nacelle
    add_quad_mesh(lines, 'C_ENGINE', (-2.0, 0.15, 0.5), (-2.0, -0.15, 0.5), (-4.5, -0.15, 0.5), (-4.5, 0.15, 0.5), u_steps=3, v_steps=2, reflect_y=False)
    add_quad_mesh(lines, 'C_ENGINE', (-2.0, 0.15, ENG_Z), (-2.0, -0.15, ENG_Z), (-4.5, -0.15, ENG_Z), (-4.5, 0.15, ENG_Z), u_steps=3, v_steps=2, reflect_y=False)
    add_quad_mesh(lines, 'C_ENGINE', (-2.0, 0.15, 0.5), (-2.0, 0.15, ENG_Z), (-4.5, 0.15, ENG_Z), (-4.5, 0.15, 0.5), u_steps=3, v_steps=2, reflect_y=True)

    # The Turbofan Bypass Cylinders
    add_cylinder(lines, 'C_ENGINE', cx=-4.5, cy=0.0, cz=ENG_Z, length=2.5, radius=0.6, axis='x', rings=5, t_count=20, reflect_y=False)
    # Intake Lip Taper
    add_cone_frustum(lines, 'C_ENGINE', cx=-2.0, cy=0.0, cz=ENG_Z, dz=0.4, r1=0.6, r2=0.5, axis='x', rings=2, t_count=20, reflect_y=False)
    
    # Kinematic Red Aft Exhaust Nozzle
    add_cone_frustum(lines, 'C_EXHAUST', cx=-4.5, cy=0.0, cz=ENG_Z, dz=-0.6, r1=0.6, r2=0.4, axis='x', rings=3, t_count=20, reflect_y=False)

    # ==============================================================================
    # 5. VENTRAL SENSOR PAYLOADS (SAR / EO/IR)
    # ==============================================================================
    # High-fidelity target acquisition blisters mounted dead-centre below the nose
    add_ellipsoid(lines, 'C_SENSORS', cx=4.5, cy=0.0, cz=-0.5, rx=1.2, ry=0.4, rz=0.4, rings=6, t_count=16, reflect_y=False)
    # Forward EO/IR spherical turret lock
    add_ellipsoid(lines, 'C_WINGS', cx=6.2, cy=0.0, cz=-0.4, rx=0.3, ry=0.3, rz=0.3, rings=4, t_count=16, reflect_y=False)

    # ==============================================================================
    # 6. TACTICAL LOCOMOTION (EXTENDED LANDING GEAR)
    # ==============================================================================
    # Nose Gear Standoff
    add_cylinder(lines, 'C_HULL', cx=5.0, cy=0.0, cz=-0.6, length=-1.6, radius=0.05, axis='z', rings=2, t_count=6, reflect_y=False)
    add_cylinder(lines, 'C_HULL', cx=5.0, cy=0.0, cz=-2.2, length=0.3, radius=0.3, axis='y', rings=2, t_count=12, reflect_y=False)
    
    # Massive Wide-Track Main Gear
    add_cylinder(lines, 'C_HULL', cx=-0.5, cy=2.5, cz=0.0, length=-2.2, radius=0.08, axis='z', rings=2, t_count=6, reflect_y=True)
    add_cylinder(lines, 'C_HULL', cx=-0.5, cy=2.5, cz=-2.2, length=0.4, radius=0.4, axis='y', rings=2, t_count=12, reflect_y=True)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_global_hawk_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry directly between the massive aerodynamic wing roots
        cam_x, cam_y, cam_z = 0.0, 0.0, 1.0
        
        # Starts explicitly from 115-degrees (Dramatic aesthetic exposing the massive spanning wings and bulbous nose radome)
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
    # Anchor Centroid = Z=1.0m. Extents rigidly track ~ +/- 7.25m longitudinally, but an immense +/- 19.95m transversely (Wingspan).
    # Setting cam_span strictly to 22.5 locks horizontal width symmetrically across a colossal 45.0m diagonal view limit.
    # Vertical bounds compute to 22.5 * 1.777 = 39.98m half-height (total transparent window ~79.9m).
    # The extreme 39.9-metre glider wingspan is mathematically forbidden from intersecting the tight 9:16 vertical walls during its rotation.
    cam_span = 22.5
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_EXHAUST',   C_EXHAUST,   1.6, 1.0),
        ('C_ENGINE',    C_ENGINE,    1.4, 1.0),
        ('C_HULL',      C_HULL,      1.2, 1.0),
        ('C_SENSORS',   C_SENSORS,   1.5, 1.0),
        ('C_WINGS',     C_WINGS,     1.3, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to distinctly parse the enormous transverse wing stretch versus the tubular dorsal engine configuration
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-453l // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // NORTHROP GRUMMAN RQ-4 GLOBAL HAWK", color=C_HULL, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_WINGS, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: ELONGATED SATCOM RADOME / 39.9M HIGH-ASPECT WINGS / DORSAL NACELLE", color=C_ENGINE, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-453l: RQ-4 GLOBAL HAWK TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
