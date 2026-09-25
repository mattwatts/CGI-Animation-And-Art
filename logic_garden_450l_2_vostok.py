"""
PROJECT: Logic Garden 450l (Exact Physical Construct // Vostok R-7 Spacecraft Matrix - REVISION 2)
FORMAT: YouTube Shorts (1080x1920)
METADATA: VOSTOK, R-7, ROCKET, YURI GAGARIN, AEROSPACE, WIREFRAME, ENGINEERING, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: True parametric slanted boosters, interstage trussing, accurate 32-bell engine cluster.
- Strict Bounds Protocol: Core locked at origin. True Geometric Center verified at Z=19.0. cam_span scaled to 15.5 for flawless, unclipped 100% full-body framing.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from absolute 115-degree dramatic elevation angle.
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
OUT_DIR = "frames_450l_vostok"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Baseplate Reference)

C_HULL_MAIN = '#94A3B8'          # Heavy Slate (Primary Booster and Core skin)
C_HULL_DARK = '#475569'          # Machined Slate (Structural banding, reinforcement ribs)
C_DETAILS   = '#1E293B'          # Carbon Slate (Interstage Trusses, Technical Mounts)
C_ACCENT    = '#E11D48'          # Kinematic Red (Vernier Accents & Top Fairing Topography)
C_ENGINE    = '#111115'          # Indestructible Black (RD-107 / RD-108 Engine Bells)

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

def append_segmented(lines_dict, key, xs, ys, zs, off=(0,0,0)):
    dx, dy, dz = off
    xs, ys, zs = list(xs), list(ys), list(zs)
    for i in range(len(xs) - 1):
        lines_dict[key].append(([xs[i]+dx, xs[i+1]+dx], [ys[i]+dy, ys[i+1]+dy], [zs[i]+dz, zs[i+1]+dz]))

# ------------------------------------------------------------------
# GEOMETRIC PRIMITIVES
# ------------------------------------------------------------------
def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='z', rings=6, t_count=20):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, length, rings)
    for s in steps:
        if axis == 'z':
            ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), np.full_like(t, cz + s)
            append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
            
def add_thrust_bell(lines_dict, col, cx, cy, cz, h, r_top, r_bot):
    steps = 5
    for k in range(steps):
        ratio = k / float(steps-1)
        z_b = cz - ratio * h
        r_b = r_top + (r_bot - r_top) * (ratio**1.5) 
        t = np.linspace(0, 2*np.pi, 12, endpoint=False)
        xb = cx + r_b*np.cos(t)
        yb = cy + r_b*np.sin(t)
        append_segmented(lines_dict, col, list(xb)+[xb[0]], list(yb)+[yb[0]], [z_b]*13)
        if k > 0:
            for m in range(12):
                append_segmented(lines_dict, col, [xb_prev[m], xb[m]], [yb_prev[m], yb[m]], [zb_prev, z_b])
        xb_prev, yb_prev, zb_prev = xb, yb, z_b

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (VOSTOK R-7 MATRIX)
# ------------------------------------------------------------------
def generate_vostok_static():
    lines = {
        'C_HULL_MAIN': [], 'C_HULL_DARK': [], 'C_DETAILS': [], 
        'C_ACCENT': [], 'C_ENGINE': [], 'C_GRID': []
    }

    # 1. BASEPLATE ENVELOPE (REFERENCE GRID)
    gx_range = np.linspace(-12.0, 12.0, 13)
    gy_range = np.linspace(-12.0, 12.0, 13)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, 0.0))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, 0.0))

    # ==============================================================================
    # 2. CORE STAGE (BLOCK A)
    # ==============================================================================
    z_core = np.linspace(0, 28.0, 24)
    t_core = np.linspace(0, 2*np.pi, 24, endpoint=False)
    for i, z in enumerate(z_core):
        r = 1.475 if z < 8.0 else 1.475 - (1.475 - 1.1) * ((z-8.0)/20.0)
        col = 'C_HULL_DARK' if i % 4 == 0 else 'C_HULL_MAIN'
        cx_vals, cy_vals = r * np.cos(t_core), r * np.sin(t_core)
        append_segmented(lines, col, list(cx_vals)+[cx_vals[0]], list(cy_vals)+[cy_vals[0]], [z]*25)
        
        if i > 0:
            for k in range(24):
                append_segmented(lines, 'C_HULL_MAIN', [cx_prev[k], cx_vals[k]], [cy_prev[k], cy_vals[k]], [z_prev, z])
        cx_prev, cy_prev, z_prev = cx_vals, cy_vals, z

    # RD-108 Core Engines (4 Main, 4 Verniers)
    for ang in [45, 135, 225, 315]: # 4 Main Bells
        r_a = np.radians(ang)
        add_thrust_bell(lines, 'C_ENGINE', 0.6*np.cos(r_a), 0.6*np.sin(r_a), 0.0, 1.5, 0.1, 0.45)
    for ang in [0, 90, 180, 270]: # 4 Steering Verniers
        r_a = np.radians(ang)
        add_thrust_bell(lines, 'C_ACCENT', 1.3*np.cos(r_a), 1.3*np.sin(r_a), 0.2, 0.8, 0.05, 0.2)

    # ==============================================================================
    # 3. STRAP-ON BOOSTERS (BLOCKS B, V, G, D)
    # ==============================================================================
    def build_booster(angle_deg):
        rad = np.radians(angle_deg)
        cos_a, sin_a = np.cos(rad), np.sin(rad)
        
        z_boost = np.concatenate([np.linspace(0, 4.0, 5), np.linspace(4.8, 19.8, 14)])
        t_b = np.linspace(0, 2*np.pi, 16, endpoint=False)
        for i, z in enumerate(z_boost):
            r = 1.34 if z <= 4.0 else 1.34 - (1.34 - 0.1) * ((z-4.0)/15.8)
            shift = 0.0 if z <= 4.0 else (2.815 - 1.55) * ((z-4.0)/15.8)
            ccx = (2.815 - shift) * cos_a
            ccy = (2.815 - shift) * sin_a
            
            bx_vals, by_vals = ccx + r * np.cos(t_b), ccy + r * np.sin(t_b)
            col = 'C_HULL_DARK' if i % 3 == 0 else 'C_HULL_MAIN'
            append_segmented(lines, col, list(bx_vals)+[bx_vals[0]], list(by_vals)+[by_vals[0]], [z]*17)
            
            if i > 0:
                for k in range(16):
                    append_segmented(lines, 'C_HULL_MAIN', [bx_prev[k], bx_vals[k]], [by_prev[k], by_vals[k]], [zb_prev, z])
            bx_prev, by_prev, zb_prev = bx_vals, by_vals, z

        for e_ang in [45, 135, 225, 315]:
            e_rad = rad + np.radians(e_ang)
            add_thrust_bell(lines, 'C_ENGINE', 2.815*cos_a + 0.55*np.cos(e_rad), 2.815*sin_a + 0.55*np.sin(e_rad), 0.0, 1.4, 0.1, 0.45)
            
        v_rad = rad + np.pi/2 # Perpendicular outriggers
        for v_s in [-1, 1]:
            add_thrust_bell(lines, 'C_ACCENT', 2.815*cos_a + 1.45*np.cos(v_rad)*v_s, 2.815*sin_a + 1.45*np.sin(v_rad)*v_s, 0.2, 0.8, 0.05, 0.2)
            
    for angle in [0, 90, 180, 270]: build_booster(angle)

    # ==============================================================================
    # 4. INTERSTAGE TRUSS & UPPER STAGES (BLOCK E + SPACECRAFT)
    # ==============================================================================
    z_tb, z_tt = 28.0, 29.5
    r_tb, r_tt = 1.1, 1.29
    t_truss = np.linspace(0, 2*np.pi, 24, endpoint=False)
    for i in range(24):
        nx1, nx2 = (i+1)%24, (i-1)%24
        x1, y1 = r_tb * np.cos(t_truss[i]), r_tb * np.sin(t_truss[i])
        x2, y2 = r_tt * np.cos(t_truss[nx1]), r_tt * np.sin(t_truss[nx1])
        x3, y3 = r_tt * np.cos(t_truss[nx2]), r_tt * np.sin(t_truss[nx2])
        append_segmented(lines, 'C_DETAILS', [x1, x2], [y1, y2], [z_tb, z_tt])
        append_segmented(lines, 'C_DETAILS', [x1, x3], [y1, y3], [z_tb, z_tt])
        append_segmented(lines, 'C_HULL_DARK', [x2, x3], [y2, y3], [z_tt, z_tt])

    add_cylinder(lines, 'C_HULL_MAIN', 0, 0, 29.5, 2.5, 1.29, rings=4, t_count=24)

    z_f = np.linspace(32.0, 38.36, 10)
    for i, z in enumerate(z_f):
        r = 1.65 if z <= 34.0 else 1.65 - (1.65 - 0.1) * ((z-34.0)/4.36)
        x_f, y_f = r * np.cos(t_truss), r * np.sin(t_truss)
        col = 'C_ACCENT' if z > 37.0 else 'C_HULL_MAIN'
        append_segmented(lines, col, list(x_f)+[x_f[0]], list(y_f)+[y_f[0]], [z]*25)
        if i > 0:
            for k in range(24):
                append_segmented(lines, col, [xf_prev[k], x_f[k]], [yf_prev[k], y_f[k]], [zf_prev, z])
        xf_prev, yf_prev, zf_prev = x_f, y_f, z

    append_segmented(lines, 'C_ACCENT', [0, 0], [0, 0], [38.36, 39.5])

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_vostok_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking the geometric True Center (-1.5 to 39.5).
        cam_x, cam_y, cam_z = 0.0, 0.0, 19.0
        
        # Starts explicitly from 115-degrees (Front-quarter dynamic sweeping perspective yielding absolute dominance)
        azimuth = 115.0 + (stage * 360.0)

        yield (f, t_sec, azimuth, cam_x, cam_y, cam_z, static_rig)

def render_frame(packet):
    f, t_sec, azimuth, cx, cy, cz, static_rig = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # 100% VISIBILITY THRESHOLD AUDIT (REVISION 2):
    # Anchor = 19.0. Total length 41.0m. Extents relative to anchor = +/- 20.5m.
    # Setting cam_span strictly to 15.5 generates a vertical viewport height of 55.08m.
    # Visible aperture safely clears HUD overlays. The entire structure remains completely in unoccluded view.
    cam_span = 15.5
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.3), 
        ('C_DETAILS',   C_DETAILS,   1.2, 1.0),
        ('C_HULL_MAIN', C_HULL_MAIN, 1.2, 1.0),
        ('C_HULL_DARK', C_HULL_DARK, 1.4, 1.0),
        ('C_ACCENT',    C_ACCENT,    1.6, 1.0),
        ('C_ENGINE',    C_ENGINE,    1.5, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +10 degrees to peer down the magnificent staggered fairings and engine clusters 
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=10.0)
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-450l // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=17, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // 39-METRE VOSTOK R-7 MATRIX", color=C_HULL_DARK, fontsize=13, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_ACCENT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: DYNAMIC SLANTED C.O.M. STRAP-ONS / 32-BELL CLUSTER", color=C_DETAILS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-450l: VOSTOK KINEMATICS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
