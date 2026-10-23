"""
PROJECT: Logic Garden 453k (Exact Physical Construct // Hammer Kinematics Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: HAMMER, DROP-FORGED, KINEMATICS, HAND TOOL, GLB, WIREFRAME, PYTHON
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional 350mm macro scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Elliptical Grip, Steel Neck, Striking Face, Bifurcated V-Claw.
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
OUT_DIR = "frames_453k_hammer"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Terrestrial Tracking Grid)

C_GRIP      = '#005599'          # Deep Marine (Shock-Absorbing Rubberized Handle)
C_SHAFT     = '#94A3B8'          # Slate Aluminium (Drop-Forged Steel Neck/Shaft)
C_HEAD      = '#334155'          # Heavy Slate (Central Eye & Cheek Block)
C_FACE      = '#1E293B'          # Carbon Slate (Hardened Striking Poll)
C_CLAW      = '#0F172A'          # Abyssal Slate (Heavy Extraction V-Claw)

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
    # The drop-forged hammer dictates absolute symmetry across the X-axis (Left/Right Faces).
    if any(abs(x) > 0.001 for x in xs):
        append_segmented(lines_dict, key, [-x for x in xs], ys, zs)

# ------------------------------------------------------------------
# GEOMETRIC PRIMITIVES
# ------------------------------------------------------------------
def add_quad_mesh(lines_dict, col, p1, p2, p3, p4, u_steps=4, v_steps=4, reflect_x=False):
    p1, p2, p3, p4 = map(np.array, (p1, p2, p3, p4))
    for i in range(v_steps + 1):
        v = i / v_steps
        start = p1 * (1-v) + p4 * v
        end   = p2 * (1-v) + p3 * v
        pts = [start * (1-u) + end * u for u in np.linspace(0, 1, u_steps+1)]
        if reflect_x:
            append_sym(lines_dict, col, [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts])
        else:
            append_segmented(lines_dict, col, [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts])
    for i in range(u_steps + 1):
        u = i / u_steps
        start = p1 * (1-u) + p2 * u
        end   = p4 * (1-u) + p3 * u
        pts = [start * (1-v) + end * v for v in np.linspace(0, 1, v_steps+1)]
        if reflect_x:
            append_sym(lines_dict, col, [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts])
        else:
            append_segmented(lines_dict, col, [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts])

def add_box_mesh(lines_dict, col, x1, x2, y1, y2, z1, z2, div=4, reflect_x=False):
    add_quad_mesh(lines_dict, col, (x1, y1, z1), (x2, y1, z1), (x2, y2, z1), (x1, y2, z1), div, div, reflect_x)
    add_quad_mesh(lines_dict, col, (x1, y1, z2), (x2, y1, z2), (x2, y2, z2), (x1, y2, z2), div, div, reflect_x)
    add_quad_mesh(lines_dict, col, (x1, y1, z1), (x2, y1, z1), (x2, y1, z2), (x1, y1, z2), div, div, reflect_x)
    add_quad_mesh(lines_dict, col, (x1, y2, z1), (x2, y2, z1), (x2, y2, z2), (x1, y2, z2), div, div, reflect_x)
    add_quad_mesh(lines_dict, col, (x1, y1, z1), (x1, y2, z1), (x1, y2, z2), (x1, y1, z2), div, div, reflect_x)
    add_quad_mesh(lines_dict, col, (x2, y1, z1), (x2, y2, z1), (x2, y2, z2), (x2, y1, z2), div, div, reflect_x)

def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='z', rings=4, t_count=16, reflect_x=False):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, length, rings)
    for s in steps:
        if axis == 'x':  
            ix, iy, iz = cx + s * np.ones_like(t), cy + radius*np.cos(t), cz + radius*np.sin(t)
        elif axis == 'y':
            ix, iy, iz = cx + radius*np.cos(t), cy + s * np.ones_like(t), cz + radius*np.sin(t)
        else:            
            ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), cz + s * np.ones_like(t)
            
        if reflect_x: append_sym(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
        else: append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
        
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        if axis == 'x':  sx, sy, sz = cx + steps, cy + radius*np.cos(a) * np.ones_like(steps), cz + radius*np.sin(a) * np.ones_like(steps)
        elif axis == 'y':sx, sy, sz = cx + radius*np.cos(a) * np.ones_like(steps), cy + steps, cz + radius*np.sin(a) * np.ones_like(steps)
        else:            sx, sy, sz = cx + radius*np.cos(a) * np.ones_like(steps), cy + radius*np.sin(a) * np.ones_like(steps), cz + steps
        
        if reflect_x: append_sym(lines_dict, col, sx, sy, sz)
        else: append_segmented(lines_dict, col, sx, sy, sz)

def add_cone_frustum(lines_dict, col, cx, cy, cz, dz, r1, r2, axis='z', rings=4, t_count=16, reflect_x=False):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, dz, rings)
    r_step = np.linspace(r1, r2, rings)
    
    for i, s in enumerate(steps):
        r = r_step[i]
        if axis == 'x':  
            ix, iy, iz = cx + s * np.ones_like(t), cy + r*np.cos(t), cz + r*np.sin(t)
        elif axis == 'y':
            ix, iy, iz = cx + r*np.cos(t), cy + s * np.ones_like(t), cz + r*np.sin(t)
        else:            
            ix, iy, iz = cx + r*np.cos(t), cy + r*np.sin(t), cz + s * np.ones_like(t)
            
        if reflect_x: append_sym(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
        else: append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    
    for a in np.linspace(0, 2*np.pi, t_count, endpoint=False):
        sx, sy, sz = [], [], []
        for i, s in enumerate(steps):
            r = r_step[i]
            if axis == 'x':  sx.append(cx + s); sy.append(cy + r*np.cos(a)); sz.append(cz + r*np.sin(a))
            elif axis == 'y':sx.append(cx + r*np.cos(a)); sy.append(cy + s); sz.append(cz + r*np.sin(a))
            else:            sx.append(cx + r*np.cos(a)); sy.append(cy + r*np.sin(a)); sz.append(cz + s)
        if reflect_x: append_sym(lines_dict, col, sx, sy, sz)
        else: append_segmented(lines_dict, col, sx, sy, sz)

def add_elliptical_cylinder(lines_dict, col, cx, cy, cz, length, rx, ry, rings=4, t_count=16):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, length, rings)
    for s in steps:
        ix = cx + rx * np.cos(t)
        iy = cy + ry * np.sin(t)
        iz = np.full_like(t, cz + s)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
        
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        sx = cx + rx * np.cos(a) * np.ones_like(steps)
        sy = cy + ry * np.sin(a) * np.ones_like(steps)
        sz = cz + steps
        append_segmented(lines_dict, col, sx, sy, sz)

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (DROP-FORGED HAMMER)
# ------------------------------------------------------------------
def generate_hammer_static():
    lines = {
        'C_GRIP': [], 'C_SHAFT': [], 'C_HEAD': [],
        'C_FACE': [], 'C_CLAW': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. MICRO-ENGINEERING TRACKING BASEPLATE (Simulation Floor)
    # ==============================================================================
    # Executing the grid slightly below the handle base to contextualize the 350mm tool
    Z_FLOOR = -0.05
    for r_p in [0.1, 0.2, 0.3]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-0.3, 0.3, 13)
    gy_range = np.linspace(-0.3, 0.3, 13)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. VIBRATION-DAMPED ERGONOMIC GRIP
    # ==============================================================================
    # Spans from Z=0.0 to Z=0.15m. Slightly ovular to lock the user's hand plane.
    RX_GRIP, RY_GRIP = 0.012, 0.018
    add_elliptical_cylinder(lines, 'C_GRIP', cx=0.0, cy=0.0, cz=0.0, length=0.15, rx=RX_GRIP, ry=RY_GRIP, rings=10, t_count=20)
    
    # Tactile kinetic ridges (anti-slip architecture)
    for z_ridge in np.linspace(0.015, 0.135, 8):
        # Slightly wider than the core
        add_elliptical_cylinder(lines, 'C_GRIP', cx=0.0, cy=0.0, cz=z_ridge, length=0.004, rx=RX_GRIP+0.001, ry=RY_GRIP+0.001, rings=2, t_count=20)

    # ==============================================================================
    # 3. DROP-FORGED STEEL NECK (THE SHAFT)
    # ==============================================================================
    # Projects out of the rubberised base and flares into the hammer head (Z=0.15 to Z=0.31).
    RX_SHAFT, RY_SHAFT = 0.008, 0.014
    add_elliptical_cylinder(lines, 'C_SHAFT', cx=0.0, cy=0.0, cz=0.15, length=0.16, rx=RX_SHAFT, ry=RY_SHAFT, rings=5, t_count=16)

    # ==============================================================================
    # 4. CENTRAL HEAD BLOCK (EYE & CHEEKS)
    # ==============================================================================
    # The absolute nucleus of kinetic transfer. 
    # Center lines: Z anchors around 0.33m.
    Z_HEAD_BOT = 0.31
    Z_HEAD_TOP = 0.355
    X_CHEEK = 0.012   # 24mm absolute width
    Y_EYE_FWD = 0.02
    Y_EYE_AFT = -0.02

    add_box_mesh(lines, 'C_HEAD', -X_CHEEK, X_CHEEK, Y_EYE_AFT, Y_EYE_FWD, Z_HEAD_BOT, Z_HEAD_TOP, div=3, reflect_x=False)

    # ==============================================================================
    # 5. HARDENED STRIKING FACE (THE POLL)
    # ==============================================================================
    # Forged cylinder bridging forward (+Y) to project the driving forces.
    # Base starts at Y=0.02, extending to Y=0.055.
    FACE_R1 = 0.012 # Neck of poll
    FACE_R2 = 0.014 # Crown of striking face
    
    # reflect_x=False guarantees we don't mathematically clone a solid cylinder over itself
    add_cone_frustum(lines, 'C_FACE', cx=0.0, cy=Y_EYE_FWD, cz=0.3325, dz=0.035, r1=FACE_R1, r2=FACE_R2, axis='y', rings=4, t_count=20, reflect_x=False)
    # The Bevel (Striking Rim) to prevent spallation
    add_cylinder(lines, 'C_FACE', cx=0.0, cy=0.055, cz=0.3325, length=0.003, radius=FACE_R2, axis='y', rings=2, t_count=20, reflect_x=False)

    # ==============================================================================
    # 6. EXTRACTING V-CLAW (BIFURCATED SWEEP MATRIX)
    # ==============================================================================
    # Extruding backwards (-Y) and aggressively translating downwards (-Z) to extract mechanical fasteners.
    t_vals = np.linspace(0, 1, 12)
    for i in range(len(t_vals)-1):
        t1, t2 = t_vals[i], t_vals[i+1]
        
        # Longitudinal extension and downward sweep equations
        y1 = Y_EYE_AFT - 0.06 * t1
        y2 = Y_EYE_AFT - 0.06 * t2
        z1 = 0.3325 - 0.04 * (t1**1.5)
        z2 = 0.3325 - 0.04 * (t2**1.5)
        
        # Outer lateral taper (Claw narrows to a chisel limit at the extreme)
        wo1 = X_CHEEK * (1 - 0.5*t1)
        wo2 = X_CHEEK * (1 - 0.5*t2)
        
        # Inner V-notch (Bifurcates cleanly at t=0.2, carving the inner void)
        wi1 = max(0.0, 0.008 * (t1 - 0.2)/0.8) if t1 > 0.2 else 0.0
        wi2 = max(0.0, 0.008 * (t2 - 0.2)/0.8) if t2 > 0.2 else 0.0
        
        # Top-Face Surface Vector
        add_quad_mesh(lines, 'C_CLAW', (wi1, y1, z1+0.01), (wo1, y1, z1+0.01), (wo2, y2, z2+0.005), (wi2, y2, z2+0.005), reflect_x=True)
        # Bottom-Face Surface Vector
        add_quad_mesh(lines, 'C_CLAW', (wi1, y1, z1-0.01), (wo1, y1, z1-0.01), (wo2, y2, z2-0.005), (wi2, y2, z2-0.005), reflect_x=True)
        # Outer Hull (Sidewall boundary)
        add_quad_mesh(lines, 'C_CLAW', (wo1, y1, z1-0.01), (wo1, y1, z1+0.01), (wo2, y2, z2+0.005), (wo2, y2, z2-0.005), reflect_x=True)
        # Inner Hull (The V-Notch Extraction Wall)
        add_quad_mesh(lines, 'C_CLAW', (wi1, y1, z1-0.01), (wi1, y1, z1+0.01), (wi2, y2, z2+0.005), (wi2, y2, z2-0.005), reflect_x=True)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_hammer_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry explicitly at the mid-shaft (Z=0.175m)
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.175
        
        # Starts explicitly from 115-degrees (Dramatic aesthetic showcasing both striking face and bifurcated claw)
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
    # Anchor Centroid = Z=0.175m. Total physical length is 0.35m.
    # The extreme Y boundaries encompass the 0.06m striking face and -0.08m tail claw.
    # Setting cam_span strictly to 0.25 locks horizontal width symmetrically across a 0.50m macro view.
    # Vertical bounds compute to 0.25 * 1.777 = 0.444m half-height (total transparent window 0.88m).
    # Completely traps the entire drop-forged tool safely inside the extreme close-up viewport, immune to UI overlay clipping.
    cam_span = 0.25
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_GRIP',      C_GRIP,      1.2, 1.0),
        ('C_SHAFT',     C_SHAFT,     1.3, 1.0),
        ('C_CLAW',      C_CLAW,      1.4, 1.0),
        ('C_HEAD',      C_HEAD,      1.5, 1.0),
        ('C_FACE',      C_FACE,      1.6, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to parse the dense mechanical intersection of the head block and neck transition
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-453k // MACRO-ENGINEERING TENSOR: INDUSTRIAL KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // DROP-FORGED CLAW HAMMER (350MM)", color=C_HEAD, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_FACE, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: SHOCK-ABSORBING GRIP / DROP-FORGED STRIKING POLL / MACRO-BIFURCATED CLAW", color=C_CLAW, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-453k: DROP-FORGED CLAW HAMMER TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Macro-Industrial Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
