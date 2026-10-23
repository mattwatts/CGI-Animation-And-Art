"""
PROJECT: Logic Garden 453f (Exact Physical Construct // General Dynamics F-111 Aardvark Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: F-111, AARDVARK, GENERAL DYNAMICS, AEROPLANE, GLB, WIREFRAME, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional 22.4m aerospace scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Side-by-Side Canopy, Extended Swing-Wings, TF30 Nozzles, D-Inlets.
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
OUT_DIR = "frames_453f_f111"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Tarmac Tracking Grid)

C_HULL      = '#334155'          # Heavy Slate (Primary Fuselage & Radome)
C_WINGS     = '#005599'          # Deep Marine (Extended Variable-Sweep Wings & Stabilators)
C_COCKPIT   = '#CA8A04'          # Kapton Gold (Side-by-Side Canopy / Escape Module)
C_ENGINES   = '#E11D48'          # Kinematic Red (TF30 Afterburning Exhaust Nozzles)
C_HARDWARE  = '#0F172A'          # Abyssal Slate (D-Inlets, Landing Gear, Ventral Fins)

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

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (F-111 AARDVARK)
# ------------------------------------------------------------------
def generate_f111_static():
    lines = {
        'C_HULL': [], 'C_WINGS': [], 'C_COCKPIT': [],
        'C_ENGINES': [], 'C_HARDWARE': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. TARMAC TRACKING BASEPLATE (1 Unit = 1 Metre)
    # ==============================================================================
    # F-111 length: ~22.4m, Span ~19.2m
    Z_FLOOR = -1.8
    for r_p in [6.0, 12.0, 18.0]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-18.0, 18.0, 19)
    gy_range = np.linspace(-18.0, 18.0, 19)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. PRIMARY FUSELAGE LOFTING
    # ==============================================================================
    # Nose Radome (Sharp penetrator profile)
    add_cone_frustum(lines, 'C_HULL', cx=11.2, cy=0.0, cz=0.0, dz=-2.7, r1=0.0, r2=0.8, axis='x', rings=5, t_count=16, reflect_y=False)
    
    # Forward Fuselage (Widening severely for the side-by-side crew module)
    # X spans from 8.5 down to 5.0
    # Custom lofting block to transition from circular radome to wide flat lifting body
    X_FWD = np.linspace(8.5, 4.0, 6)
    W_FWD = np.linspace(0.8, 1.6, 6)
    H_FWD = np.linspace(0.8, 1.2, 6)
    
    for i in range(len(X_FWD)-1):
        x1, x2 = X_FWD[i], X_FWD[i+1]
        w1, w2 = W_FWD[i], W_FWD[i+1]
        h1, h2 = H_FWD[i], H_FWD[i+1]
        add_quad_mesh(lines, 'C_HULL', (x1, w1, 0), (x2, w2, 0), (x2, 0, h2), (x1, 0, h1), u_steps=2, v_steps=2, reflect_y=True)
        add_quad_mesh(lines, 'C_HULL', (x1, w1, 0), (x2, w2, 0), (x2, 0, -h2), (x1, 0, -h1), u_steps=2, v_steps=2, reflect_y=True)

    # Main Centerbody (Constant wide lifting body geometry)
    add_quad_mesh(lines, 'C_HULL', (4.0, 1.6, 0), (-6.0, 1.6, 0), (-6.0, 0.0, 1.2), (4.0, 0.0, 1.2), u_steps=5, v_steps=5, reflect_y=True)
    add_quad_mesh(lines, 'C_HULL', (4.0, 1.6, 0), (-6.0, 1.6, 0), (-6.0, 0.0, -1.0), (4.0, 0.0, -1.0), u_steps=5, v_steps=5, reflect_y=True)

    # Aft Fuselage (Tapering to the twin engine nozzles between the stabilators)
    add_quad_mesh(lines, 'C_HULL', (-6.0, 1.6, 0), (-10.5, 1.2, 0), (-10.5, 0.0, 0.8), (-6.0, 0.0, 1.2), u_steps=4, v_steps=3, reflect_y=True)
    add_quad_mesh(lines, 'C_HULL', (-6.0, 1.6, 0), (-10.5, 1.2, 0), (-10.5, 0.0, -0.6), (-6.0, 0.0, -1.0), u_steps=4, v_steps=3, reflect_y=True)

    # ==============================================================================
    # 3. SIDE-BY-SIDE COCKPIT / CREW ESCAPE CAPSULE
    # ==============================================================================
    # The F-111 uses a unique side-by-side seating arrangement inside an ejectable module
    # Kapton Gold canopy tracking from X=7.5 down to X=4.5
    X_CANOPY = [7.2, 6.0, 4.5]
    Z_CANOPY = [0.8, 1.7, 1.3]
    W_CANOPY = [0.6, 1.1, 1.0]

    for i in range(2):
        x1, x2 = X_CANOPY[i], X_CANOPY[i+1]
        z1, z2 = Z_CANOPY[i], Z_CANOPY[i+1]
        w1, w2 = W_CANOPY[i], W_CANOPY[i+1]
        add_quad_mesh(lines, 'C_COCKPIT', (x1, w1, 0.8), (x2, w2, 1.0), (x2, 0.0, z2), (x1, 0.0, z1), u_steps=2, v_steps=3, reflect_y=True)

    # ==============================================================================
    # 4. VARIABLE-SWEEP WING MATRIX (FULLY EXTENDED 16-DEGREE)
    # ==============================================================================
    # The mechanical swing-wing pivot box sits heavily at X=1.0, Y=1.5
    PIVOT_X = 1.0
    PIVOT_Y = 1.5
    
    # Extended configuration drives lateral wingspan to 9.6m per side
    WING_TIP_X = -1.5
    WING_TIP_Y = 9.6
    WING_AFT_X = -4.5
    WING_ROOT_AFT_X = -3.0
    
    # Primary Main Wing Box
    add_quad_mesh(lines, 'C_WINGS', 
                  (PIVOT_X, PIVOT_Y, 0.2), (WING_TIP_X, WING_TIP_Y, 0.2), 
                  (WING_AFT_X, WING_TIP_Y, 0.2), (WING_ROOT_AFT_X, PIVOT_Y, 0.2), 
                  u_steps=5, v_steps=8, reflect_y=True)
    # Aerodynamic thickness
    add_quad_mesh(lines, 'C_WINGS', 
                  (PIVOT_X, PIVOT_Y, 0.0), (WING_TIP_X, WING_TIP_Y, 0.0), 
                  (WING_AFT_X, WING_TIP_Y, 0.0), (WING_ROOT_AFT_X, PIVOT_Y, 0.0), 
                  u_steps=5, v_steps=8, reflect_y=True)

    # ==============================================================================
    # 5. D-INLETS & TF30 PROPULSION SYSTEM
    # ==============================================================================
    # Forward quarter-circle D-inlets tucked hard under the armpits of the wing root
    add_quad_mesh(lines, 'C_HARDWARE', (3.5, 0.6, 0.0), (3.5, 1.6, 0.0), (3.5, 1.6, -0.8), (3.5, 0.6, -0.8), u_steps=2, v_steps=3, reflect_y=True)
    # Inlet Cowling flow mapping
    add_quad_mesh(lines, 'C_HARDWARE', (3.5, 1.6, 0.0), (1.0, 1.7, 0.0), (1.0, 1.7, -0.9), (3.5, 1.6, -0.8), u_steps=3, v_steps=4, reflect_y=True)

    # Aft Afterburning Exhaust Nozzles (Kinematic Red)
    add_cylinder(lines, 'C_ENGINES', cx=-10.5, cy=0.7, cz=0.0, length=-1.2, radius=0.6, axis='x', rings=4, t_count=16, reflect_y=True)
    add_cone_frustum(lines, 'C_ENGINES', cx=-11.7, cy=0.7, cz=0.0, dz=-0.5, r1=0.6, r2=0.55, axis='x', rings=2, t_count=16, reflect_y=True)

    # ==============================================================================
    # 6. EMPENNAGE (Tail Vectors)
    # ==============================================================================
    # Massive swept vertical stabiliser
    VS_ROOT_X = -5.0
    VS_AFT_X = -11.0
    VS_TIP_X = -10.5
    VS_TIP_Z = 4.2
    
    add_quad_mesh(lines, 'C_HULL', (VS_ROOT_X, 0.0, 1.2), (VS_ROOT_X-2.0, 0.0, VS_TIP_Z), (VS_TIP_X, 0.0, VS_TIP_Z), (VS_AFT_X, 0.0, 1.2), u_steps=4, v_steps=6, reflect_y=False)
    
    # Twin All-Moving Horizontal Stabilators (Tailplanes)
    # Swept aggressively overlapping the engine vectors
    HS_ROOT_X = -6.0
    HS_TIP_X = -10.0
    HS_TIP_Y = 4.5
    HS_AFT_X = -11.5
    
    add_quad_mesh(lines, 'C_WINGS', (HS_ROOT_X, 1.0, 0.0), (HS_TIP_X, HS_TIP_Y, 0.0), (HS_AFT_X, HS_TIP_Y, 0.0), (-10.5, 1.0, 0.0), u_steps=4, v_steps=5, reflect_y=True)

    # Twin Ventral Fins (Under the rear fuselage)
    add_quad_mesh(lines, 'C_HARDWARE', (-6.0, 0.6, -1.0), (-8.0, 0.6, -1.8), (-10.0, 0.6, -1.8), (-9.0, 0.6, -1.0), u_steps=2, v_steps=3, reflect_y=True)

    # ==============================================================================
    # 7. TACTICAL LOCOMOTION (Deployed Landing Gear)
    # ==============================================================================
    # Nose Gear Assembly
    add_cylinder(lines, 'C_HARDWARE', cx=6.5, cy=0.0, cz=-0.5, length=-1.0, radius=0.05, axis='z', rings=2, t_count=6, reflect_y=False)
    add_cylinder(lines, 'C_HARDWARE', cx=6.5, cy=0.0, cz=-1.65, length=0.3, radius=0.25, axis='y', rings=2, t_count=12, reflect_y=False) # Twin nose wheels
    
    # Main Gear Assembly
    add_cylinder(lines, 'C_HARDWARE', cx=-1.0, cy=1.5, cz=-1.0, length=-0.5, radius=0.1, axis='z', rings=2, t_count=6, reflect_y=True)
    add_cylinder(lines, 'C_HARDWARE', cx=-1.0, cy=1.5, cz=-1.65, length=0.3, radius=0.4, axis='y', rings=2, t_count=12, reflect_y=True) # Massive main wheels

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_f111_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry flawlessly at payload centroid
        cam_x, cam_y, cam_z = 0.0, 0.0, 1.0
        
        # Starts explicitly from 115-degrees (Dramatic aesthetic exposing the massive extended wing and forward radome)
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
    # Anchor Centroid = Z=1.0m. Extents rigidly track ~ +/- 11.2m longitudinally and +/- 9.6m transversely.
    # Setting cam_span strictly to 15.5 locks horizontal width symmetrically across a massive 31.0m view.
    # Vertical bounds compute to 15.5 * 1.777 = 27.54m half-height (total transparent window 55.0m).
    # Entire 22.4-metre aeroplane footprint including the extended sweep matrix is perfectly trapped inside the unoccluded viewing volume.
    cam_span = 15.5
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_HARDWARE',  C_HARDWARE,  1.2, 1.0),
        ('C_ENGINES',   C_ENGINES,   1.5, 1.0),
        ('C_HULL',      C_HULL,      1.3, 1.0),
        ('C_WINGS',     C_WINGS,     1.4, 1.0),
        ('C_COCKPIT',   C_COCKPIT,   1.6, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to parse the sprawling extended swing-wings and wide flat lifting body
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-453f // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // GENERAL DYNAMICS F-111 AARDVARK", color=C_HULL, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_WINGS, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: 22.4M FUSELAGE / EXTENDED VARIABLE-SWEEP MATRIX / TWIN TF30 NOZZLES", color=C_ENGINES, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-453f: F-111 AARDVARK TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
