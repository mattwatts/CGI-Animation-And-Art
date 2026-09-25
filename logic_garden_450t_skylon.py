"""
PROJECT: Logic Garden 450t (Exact Physical Construct // Skylon Spaceplane Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: SKYLON, SPACEPLANE, SABRE, AEROSPACE, WIREFRAME, ENGINEERING, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: 83-metre slender hull, wingtip SABRE nacelles with shock-cones, quad-cluster engine bells.
- Strict Bounds Protocol: Core locked at origin. cam_span scaled to 45.0 for flawless, unclipped 100% full-body framing of the 83.1m object.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from absolute 115-degree dramatic front-quarter angle.
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
OUT_DIR = "frames_450t_skylon"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Baseplate Reference)

C_HULL_MAIN = '#94A3B8'          # Heavy Slate (Primary Aerospace Skin)
C_HULL_DARK = '#475569'          # Machined Slate (Canards, Wings, Tail)
C_DETAILS   = '#1E293B'          # Carbon Slate (Landing Gear Struts, Shock Cones)
C_COCKPIT   = '#111115'          # Indestructible Black (Cockpit Glazing / Instrumentation)
C_ENGINE    = '#E11D48'          # Kinematic Red (SABRE Quad-Nozzle Clusters)

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
        append_segmented(lines_dict, col, [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts])
    for i in range(u_steps + 1):
        u = i / u_steps
        start = p1 * (1-u) + p2 * u
        end   = p4 * (1-u) + p3 * u
        pts = [start * (1-v) + end * v for v in np.linspace(0, 1, v_steps+1)]
        append_segmented(lines_dict, col, [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts])

def add_sym_quad(lines_dict, col, p1, p2, p3, p4, u_steps=4, v_steps=4):
    add_quad_mesh(lines_dict, col, p1, p2, p3, p4, u_steps, v_steps)
    if any(abs(p[1]) > 0.001 for p in [p1, p2, p3, p4]):
        add_quad_mesh(lines_dict, col, (p1[0], -p1[1], p1[2]), (p2[0], -p2[1], p2[2]), 
                                       (p3[0], -p3[1], p3[2]), (p4[0], -p4[1], p4[2]), u_steps, v_steps)

def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='x', rings=4, t_count=16):
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

def add_cone(lines_dict, col, base_x, cy, cz, tip_x, base_r, t_count=16):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    y_b = cy + base_r * np.cos(t)
    z_b = cz + base_r * np.sin(t)
    append_segmented(lines_dict, col, [base_x]*17, list(y_b)+[y_b[0]], list(z_b)+[z_b[0]])
    for i in range(t_count):
        append_segmented(lines_dict, col, [base_x, tip_x], [y_b[i], cy], [z_b[i], cz])

def add_x_thrust_bell(lines_dict, col, cx, cy, cz, length, r_fwd, r_aft):
    steps = 4
    x_steps = np.linspace(cx, cx-length, steps)
    ratio = (cx - x_steps) / length
    r_steps = r_fwd + (r_aft - r_fwd) * (ratio**1.2)
    for i in range(steps):
        r, x = r_steps[i], x_steps[i]
        t = np.linspace(0, 2*np.pi, 16, endpoint=False)
        append_segmented(lines_dict, col, [x]*17, list(cy + r*np.cos(t))+[cy + r*np.cos(0)], list(cz + r*np.sin(t))+[cz + r*np.sin(0)])
    for a in np.linspace(0, 2*np.pi, 16, endpoint=False):
        append_segmented(lines_dict, col, list(x_steps), list(cy + r_steps*np.cos(a)), list(cz + r_steps*np.sin(a)))

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (SKYLON SPACEPLANE)
# ------------------------------------------------------------------
def generate_skylon_static():
    lines = {
        'C_HULL_MAIN': [], 'C_HULL_DARK': [], 'C_DETAILS': [], 
        'C_COCKPIT': [], 'C_ENGINE': [], 'C_GRID': []
    }

    # 1. BASEPLATE ENVELOPE (REFERENCE GRID)
    Z_FLOOR = -4.5
    gx_range = np.linspace(-45.0, 45.0, 19)
    gy_range = np.linspace(-30.0, 30.0, 13)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. CONTINUOUS FUSELAGE LOFTING (83-Metre Slender Body)
    # ==============================================================================
    x_st = np.linspace(-41.5, 41.5, 30)
    for i in range(len(x_st)-1):
        x1, x2 = x_st[i], x_st[i+1]
        
        ratio1 = (x1 + 41.5) / 83.0
        ratio2 = (x2 + 41.5) / 83.0
        # Power-law sinusoidal mapping yielding pure aerodynamic profile
        r1 = 3.3 * np.clip(np.sin(ratio1 * np.pi)**0.65, 0.01, 1.0)
        r2 = 3.3 * np.clip(np.sin(ratio2 * np.pi)**0.65, 0.01, 1.0)
        
        t = np.linspace(0, 2*np.pi, 24, endpoint=False)
        y1_ring, z1_ring = r1 * np.cos(t), r1 * np.sin(t)
        y2_ring, z2_ring = r2 * np.cos(t), r2 * np.sin(t)
        
        col = 'C_HULL_MAIN'
        if i % 5 == 0: col = 'C_HULL_DARK' # Structural Payload Banding
        
        append_segmented(lines, col, [x1]*25, list(y1_ring)+[y1_ring[0]], list(z1_ring)+[z1_ring[0]])
        for k in range(24):
            append_segmented(lines, 'C_HULL_MAIN', [x1, x2], [y1_ring[k], y2_ring[k]], [z1_ring[k], z2_ring[k]])

    # Cockpit Visor Slice (Approx X=32.0, Z=top)
    cx_w = [34.0, 31.0, 31.0, 34.0, 34.0]
    cy_w = [-0.6, -0.9, 0.9, 0.6, -0.6]
    cz_w = [1.5, 2.0, 2.0, 1.5, 1.5]
    append_segmented(lines, 'C_COCKPIT', cx_w, cy_w, cz_w)

    # ==============================================================================
    # 3. KINEMATIC WINGS & CANARDS
    # ==============================================================================
    # Primary Mid-Swept Wings supporting the SABRE Nacelles
    add_sym_quad(lines, 'C_HULL_DARK', (8.0, 3.3, 0.0), (-10.0, 3.3, 0.0), (-10.0, 12.0, 0.0), (2.0, 12.0, 0.0), u_steps=8, v_steps=6)

    # Forward Canards
    add_sym_quad(lines, 'C_DETAILS', (36.0, 1.5, 0.0), (32.0, 2.0, 0.0), (31.0, 4.0, 0.0), (34.0, 4.0, 0.0), u_steps=3, v_steps=3)

    # Single Vertical Tail Fin
    add_quad_mesh(lines, 'C_DETAILS', (-32.0, 0.0, 2.0), (-40.0, 0.0, 1.0), (-41.0, 0.0, 7.5), (-35.0, 0.0, 7.5), u_steps=4, v_steps=5)

    # ==============================================================================
    # 4. SABRE ENGINE NACELLES & QUAD-NOZZLES
    # ==============================================================================
    # Twin 20m nacelles mounted at Wingtips (Y = +/- 12.5)
    for y_sign in [-1, 1]:
        cy = 13.0 * y_sign
        
        # Primary Nacelle Tube (X: 4.0 to -16.0)
        add_cylinder(lines, 'C_HULL_MAIN', cx=-16.0, cy=cy, cz=0.0, length=20.0, radius=2.5, axis='x', rings=8, t_count=20)
        
        # Extruding the extreme Forward Shock Cone (Spike) required for Mach 5+ inlet shockwave control
        add_cone(lines, 'C_DETAILS', base_x=4.0, cy=cy, cz=0.0, tip_x=9.0, base_r=1.5, t_count=16)

        # Aft Ring & 4 Thrust Bells Per Engine 
        for ez_off in [-0.8, 0.8]:
            for ey_off in [-0.8, 0.8]:
                # Deep clustered exhaust matrix terminating the nacelle
                add_x_thrust_bell(lines, 'C_ENGINE', cx=-16.0, cy=cy + ey_off, cz=ez_off, length=2.0, r_fwd=0.4, r_aft=0.7)

    # ==============================================================================
    # 5. TRICYCLE LANDING GEAR
    # ==============================================================================
    # Extracted from Blueprint positioning
    # Nose Gear Assembly (Offset far back from nose)
    append_segmented(lines, 'C_DETAILS', [22.0, 22.0], [0.0, 0.0], [-1.5, Z_FLOOR])
    # Twin Nose Wheels
    for y_n in [-0.4, 0.4]:
        add_cylinder(lines, 'C_DETAILS', cx=22.0, cy=y_n - 0.2*np.sign(y_n), cz=Z_FLOOR+0.3, length=0.4*np.sign(y_n), radius=0.3, axis='y', rings=2)

    # Main Gear Assembly (Under Mid-Fuselage Core)
    append_sym(lines, 'C_DETAILS', [-2.0, -2.0], [2.2, 2.2], [-3.0, Z_FLOOR])
    for y_m in [-2.5, 2.5]:
        # Twin wheel bogie per strut
        add_cylinder(lines, 'C_DETAILS', cx=-1.5, cy=y_m, cz=Z_FLOOR+0.4, length=0.6*np.sign(y_m), radius=0.4, axis='y', rings=2)
        add_cylinder(lines, 'C_DETAILS', cx=-2.5, cy=y_m, cz=Z_FLOOR+0.4, length=0.6*np.sign(y_m), radius=0.4, axis='y', rings=2)

    return lines

# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_skylon_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking the geometric True Center of the 83.1m massive airframe
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.0
        
        # Starts explicitly from 115-degrees (Dramatic front-quarter aesthetic)
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
    # Anchor = 0.0. Total vessel length is 83.1m.
    # Setting cam_span safely wide to 45.0 to yield 90.0m massive horizontal footprint isolating all extremities.
    # Vertical bounds output 45.0 * 1.777 = 79.9m (x2 = 159.9m height).
    # Perfectly frames the huge, slender static stance unconditionally escaping the visual bounding text lines.
    cam_span = 45.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.6, 0.3), 
        ('C_HULL_MAIN', C_HULL_MAIN, 1.2, 1.0),
        ('C_HULL_DARK', C_HULL_DARK, 1.4, 1.0),
        ('C_DETAILS',   C_DETAILS,   1.2, 1.0),
        ('C_COCKPIT',   C_COCKPIT,   1.5, 1.0),
        ('C_ENGINE',    C_ENGINE,    1.4, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +12 degrees to cleanly isolate the massive SABRE nacelles against the wings
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=12.0)
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-450t // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // SKYLON SPACEPLANE MATRIX", color=C_HULL_DARK, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_ENGINE, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: SABRE NACELLE ARRAYS / SSTO FUSELAGE", color=C_DETAILS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-450t: SKYLON KINEMATICS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
