"""
PROJECT: Logic Garden 450p (Exact Physical Construct // F-22 Raptor Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: F-22, RAPTOR, LOCKHEED MARTIN, AEROSPACE, WIREFRAME, ENGINEERING, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: True stealth faceted topography, cantilevered aerodynamics, deployed tricycle landing gear.
- Strict Bounds Protocol: Core locked at origin. cam_span scaled to 12.0 for flawless, unclipped 100% full-body framing.
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
OUT_DIR = "frames_450p_raptor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Baseplate Reference)

C_HULL_MAIN = '#94A3B8'          # Heavy Slate (Primary Air Superiority Grey)
C_HULL_DARK = '#475569'          # Machined Slate (RAM Edges, Baseplates, Stealth Chines)
C_DETAILS   = '#1E293B'          # Carbon Slate (Vertical Stabs, Gear Struts)
C_COCKPIT   = '#FFB300'          # Dense Gold (ITO Coated Canopy Glazing)
C_ENGINE    = '#111115'          # Indestructible Black (2D Thrust Vectoring Nozzles)

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


# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (LOCKHEED F-22 RAPTOR)
# ------------------------------------------------------------------
def generate_raptor_static():
    lines = {
        'C_HULL_MAIN': [], 'C_HULL_DARK': [], 'C_DETAILS': [], 
        'C_COCKPIT': [], 'C_ENGINE': [], 'C_GRID': []
    }

    # 1. BASEPLATE ENVELOPE (REFERENCE GRID - Tarmac Level)
    Z_FLOOR = -2.5
    gx_range = np.linspace(-12.0, 12.0, 17)
    gy_range = np.linspace(-10.0, 10.0, 13)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. CONTINUOUS STEALTH FUSELAGE (Topological Lofting)
    # ==============================================================================
    x_st = [9.0, 7.5, 6.0, 4.0, 2.0, 0.0, -2.0, -4.0, -6.0, -8.0, -9.0, -9.5]
    ct = [(0,0), (0,0.3), (0,0.5), (0,0.8), (0,0.9), (0,0.9), (0,0.9), (0,0.8), (0,0.7), (0,0.5), (0, 0.2), (0, 0.1)]
    ch = [(0,0), (0.5,-0.1), (0.9,-0.1), (1.5, 0.0), (2.0, 0.1), (2.2, 0.1), (2.2, 0.1), (2.2, 0.1), (2.0, 0.1), (1.6, 0.1), (1.4, 0.1), (1.0, 0.1)]
    be = [(0,0), (0.3,-0.3), (0.7,-0.6), (1.2,-1.0), (1.6,-1.2), (1.6,-1.2), (1.6,-1.2), (1.6,-1.2), (1.6,-1.1), (1.4,-0.8), (1.3,-0.3), (1.0, -0.1)]
    cb = [(0,0), (0,-0.4), (0,-0.8), (0,-1.2),  (0,-1.3),  (0,-1.3),  (0,-1.3),  (0,-1.3),  (0,-1.2),  (0,-0.8), (0,-0.3), (0, -0.1)]

    for i in range(len(x_st)-1):
        x1, x2 = x_st[i], x_st[i+1]
        add_sym_quad(lines, 'C_HULL_MAIN',
            (x1, ct[i][0], ct[i][1]), (x1, ch[i][0], ch[i][1]),
            (x2, ch[i+1][0], ch[i+1][1]), (x2, ct[i+1][0], ct[i+1][1]), u_steps=2, v_steps=2)
        add_sym_quad(lines, 'C_HULL_MAIN',
            (x1, ch[i][0], ch[i][1]), (x1, be[i][0], be[i][1]),
            (x2, be[i+1][0], be[i+1][1]), (x2, ch[i+1][0], ch[i+1][1]), u_steps=2, v_steps=2)
        add_sym_quad(lines, 'C_HULL_DARK',
            (x1, be[i][0], be[i][1]), (x1, cb[i][0], cb[i][1]),
            (x2, cb[i+1][0], cb[i+1][1]), (x2, be[i+1][0], be[i+1][1]), u_steps=2, v_steps=2)

    # ==============================================================================
    # 3. ITO COATED STEALTH CANOPY (Dense Gold Bubble)
    # ==============================================================================
    p_c_front = (6.0, 0, 0.5); p_c_top = (4.5, 0, 1.4); p_c_rear = (2.5, 0, 0.95)
    p_s_front = (5.5, 0.5, 0.4); p_s_mid = (4.5, 0.7, 0.75); p_s_rear = (3.0, 0.6, 0.8)

    add_sym_quad(lines, 'C_COCKPIT', p_c_front, p_s_front, p_s_mid, p_c_top, u_steps=4, v_steps=4)
    add_sym_quad(lines, 'C_COCKPIT', p_c_top, p_s_mid, p_s_rear, p_c_rear, u_steps=4, v_steps=4)

    # ==============================================================================
    # 4. KINEMATIC WINGS & STABILISERS
    # ==============================================================================
    # Main Diamond-Delta Wings
    add_sym_quad(lines, 'C_HULL_MAIN', (3.5, 1.5, 0.0), (-2.0, 6.8, 0.0), (-3.5, 6.8, 0.0), (-5.5, 2.0, 0.0), u_steps=6, v_steps=4)
    add_sym_quad(lines, 'C_HULL_DARK', (3.5, 1.5, -0.05), (-2.0, 6.8, -0.05), (-3.5, 6.8, -0.05), (-5.5, 2.0, -0.05), u_steps=6, v_steps=4)
    
    # Canted Horizontal Stabilisers (Aft)
    add_sym_quad(lines, 'C_HULL_DARK', (-5.5, 1.5, -0.2), (-7.5, 4.5, -0.2), (-9.5, 4.5, -0.2), (-8.0, 1.5, -0.2), u_steps=3, v_steps=3)

    # Canted Vertical Stabilisers (28-degree outward lean)
    add_sym_quad(lines, 'C_DETAILS', (-5.0, 1.5, 0.5), (-6.5, 3.2, 2.5), (-8.5, 3.2, 2.5), (-8.0, 1.5, 0.5), u_steps=3, v_steps=3)
    add_sym_quad(lines, 'C_DETAILS', (-5.0, 1.55, 0.5), (-6.5, 3.25, 2.5), (-8.5, 3.25, 2.5), (-8.0, 1.55, 0.5), u_steps=3, v_steps=3)

    # ==============================================================================
    # 5. LATERAL STEALTH INTAKES
    # ==============================================================================
    # Sharply swept-back side air induction geometry
    add_sym_quad(lines, 'C_HULL_DARK', (4.0, 1.5, 0.4), (2.0, 2.0, 0.4), (2.0, 2.0, -0.5), (3.5, 1.5, -0.5), u_steps=4, v_steps=2)

    # ==============================================================================
    # 6. 2D THRUST VECTORING NOZZLES
    # ==============================================================================
    p_up_l = (-9.5, 0.2, 0.1); p_up_r = (-9.5, 1.0, 0.1)
    p_dn_r = (-9.5, 1.0, -0.1); p_dn_l = (-9.5, 0.2, -0.1)
    # The actual rectangular nozzle aperture
    add_sym_quad(lines, 'C_ENGINE', p_up_l, p_up_r, p_dn_r, p_dn_l, u_steps=2, v_steps=1)
    # Vectoring flaps terminating the main fuselage
    add_sym_quad(lines, 'C_ENGINE', (-9.0, 0.2, 0.2), (-9.0, 1.0, 0.2), p_up_r, p_up_l, u_steps=2, v_steps=1) 
    add_sym_quad(lines, 'C_ENGINE', (-9.0, 0.2, -0.2), (-9.0, 1.0, -0.2), p_dn_r, p_dn_l, u_steps=2, v_steps=1) 

    # ==============================================================================
    # 7. TRICYCLE LANDING GEAR
    # ==============================================================================
    # Nose Gear Assembly
    append_segmented(lines, 'C_DETAILS', [6.0, 6.0], [0.0, 0.0], [-1.0, Z_FLOOR])
    add_cylinder(lines, 'C_DETAILS', cx=6.0, cy=-0.1, cz=Z_FLOOR, length=0.2, radius=0.3, axis='y', rings=2)

    # Main Gear Assembly
    append_sym(lines, 'C_DETAILS', [-1.0, -1.0], [1.5, 1.5], [-1.0, Z_FLOOR])
    add_cylinder(lines, 'C_DETAILS', cx=-1.0, cy=1.4, cz=Z_FLOOR, length=0.4, radius=0.45, axis='y', rings=3)
    add_cylinder(lines, 'C_DETAILS', cx=-1.0, cy=-1.8, cz=Z_FLOOR, length=0.4, radius=0.45, axis='y', rings=3)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_raptor_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking the geometric True Center of the 19.5m airframe
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
    # Anchor = 0.0. Total vessel length is 19.5m.
    # Setting cam_span safely wide to 12.0 to yield 24.0m horizontal footprint.
    # Vertical bounds output 12.0 * 1.777 = 21.32m (x2 = 42.6m height allowed).
    # Perfectly frames the wide, predatory stance without intersecting HUD logic.
    cam_span = 12.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_HULL_MAIN', C_HULL_MAIN, 1.2, 1.0),
        ('C_HULL_DARK', C_HULL_DARK, 1.4, 1.0),
        ('C_DETAILS',   C_DETAILS,   1.4, 1.0),
        ('C_COCKPIT',   C_COCKPIT,   1.8, 1.0),
        ('C_ENGINE',    C_ENGINE,    1.6, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +12 degrees to cleanly isolate the faceted stealth upper body and wide diamond wings
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-450p // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // F-22 RAPTOR MATRIX", color=C_HULL_DARK, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_COCKPIT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: STEALTH FACET TOPOGRAPHY / 2D VECTOR NOZZLES", color=C_DETAILS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-450p: F-22 RAPTOR KINEMATICS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
