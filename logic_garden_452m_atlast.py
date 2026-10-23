"""
PROJECT: Logic Garden 452m (Exact Physical Construct // ATLAST Space Telescope Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: ATLAST, LUVOIR, SATELLITE, GLB, WIREFRAME, ENGINEERING, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional 36.0m aerospace scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: 16m Parabolic Mirror, Multi-Layer Sunshield, Octagonal Bus, Solar Arrays.
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
OUT_DIR = "frames_452m_atlast"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Orbital Tracking Grid)

C_MIRROR    = '#CA8A04'          # Kapton Gold (16m Primary & Secondary Optics)
C_TRUSS     = '#1E293B'          # Carbon Slate (Tripod Mounts / Rigidity Struts)
C_SHIELD    = '#334155'          # Heavy Slate (Multi-Layer Deployable Sunshield)
C_BUS       = '#0F172A'          # Abyssal Slate (Octagonal Equipment Bus)
C_PANELS    = '#005599'          # Deep Marine (Transverse Photovoltaic Arrays)

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

def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='z', rings=4, t_count=16):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, length, rings)
    for s in steps:
        if axis == 'x':  ix, iy, iz = np.full_like(t, cx + s), cy + radius*np.cos(t), cz + radius*np.sin(t)
        elif axis == 'y':ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + s), cz + radius*np.sin(t)
        else:            ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), np.full_like(t, cz + s)
        append_sym(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        if axis == 'x':  sx, sy, sz = cx + steps, [cy + radius*np.cos(a)]*rings, [cz + radius*np.sin(a)]*rings
        elif axis == 'y':sx, sy, sz = [cx + radius*np.cos(a)]*rings, cy + steps, [cz + radius*np.sin(a)]*rings
        else:            sx, sy, sz = [cx + radius*np.cos(a)]*rings, [cy + radius*np.sin(a)]*rings, cz + steps
        append_sym(lines_dict, col, sx, sy, sz)

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (ATLAST SATELLITE)
# ------------------------------------------------------------------
def generate_atlast_static():
    lines = {
        'C_MIRROR': [], 'C_TRUSS': [], 'C_SHIELD': [],
        'C_BUS': [], 'C_PANELS': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. ORBITAL TRACKING BASEPLATE (1 Unit = 1 Metre)
    # ==============================================================================
    Z_FLOOR = -10.0
    for r_p in [10.0, 20.0, 30.0]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-30.0, 30.0, 13)
    gy_range = np.linspace(-30.0, 30.0, 13)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. 16-METRE SEGMENTED PRIMARY MIRROR & OPTICS
    # ==============================================================================
    R_M = 8.0     # 16m diameter
    FOCAL = 12.0  # Parabolic curvature depth coefficient
    
    # Generate high-density parabolic primary mesh natively
    # Using Z = (r^2) / (4*F)
    t = np.linspace(0, 2*np.pi, 36, endpoint=False)
    r_steps = np.linspace(0.5, R_M, 12)
    
    # Latitudinal rings
    for r in r_steps:
        xs = r * np.cos(t)
        ys = r * np.sin(t)
        zs = np.full_like(t, (r**2) / (4 * FOCAL))
        append_sym(lines, 'C_MIRROR', list(xs)+[xs[0]], list(ys)+[ys[0]], list(zs)+[zs[0]])
        
    # Longitudinal radials
    for a in np.linspace(0, 2*np.pi, 24, endpoint=False):
        xs = r_steps * np.cos(a)
        ys = r_steps * np.sin(a)
        zs = (r_steps**2) / (4 * FOCAL)
        append_sym(lines, 'C_MIRROR', xs, ys, zs)

    # Central Instrument Baffle Tube penetrating the primary mirror
    add_cylinder(lines, 'C_TRUSS', cx=0.0, cy=0.0, cz=-1.5, length=3.0, radius=0.5, axis='z', rings=4, t_count=12)

    # Secondary Mirror Cluster (Z = 12.0m forward of primary)
    Z_SEC = 12.0
    R_SEC = 1.2
    add_cylinder(lines, 'C_MIRROR', cx=0.0, cy=0.0, cz=Z_SEC, length=-0.3, radius=R_SEC, axis='z', rings=3, t_count=16)

    # Heavy Tripod Support Truss locking secondary mirror to main perimeter
    for ang in [np.pi/2, np.pi/2 + 2*np.pi/3, np.pi/2 - 2*np.pi/3]:
        x0 = R_M * np.cos(ang)
        y0 = R_M * np.sin(ang)
        z0 = (R_M**2) / (4 * FOCAL)
        
        x1 = R_SEC * np.cos(ang)
        y1 = R_SEC * np.sin(ang)
        z1 = Z_SEC
        
        append_segmented(lines, 'C_TRUSS', [x0, x1], [y0, y1], [z0, z1])

    # ==============================================================================
    # 3. 3-LAYER PLANAR DEPLOYABLE SUNSHIELD
    # ==============================================================================
    # JWST-style diamond topology. Spanning +/- 12m in X and +/- 18m in Y.
    # Defines absolute extreme boundaries of the craft.
    SHIELD_X = 14.0
    SHIELD_Y = 20.0
    
    for layer_z in [-1.5, -2.5, -3.5]:
        add_quad_mesh(lines, 'C_SHIELD', 
                      (0, SHIELD_Y, layer_z), (SHIELD_X, 0, layer_z),
                      (0, -SHIELD_Y, layer_z), (-SHIELD_X, 0, layer_z),
                      u_steps=8, v_steps=8)

    # ==============================================================================
    # 4. AFT HEXAGONAL / OCTAGONAL BUS (EQUIPMENT MODULE)
    # ==============================================================================
    # Heavy octagonal bus extending structurally downward from the sunshield base
    Z_BUS_FWD = -3.5
    Z_BUS_AFT = -8.5
    R_BUS = 3.5
    
    add_cylinder(lines, 'C_BUS', cx=0.0, cy=0.0, cz=Z_BUS_AFT, length=(Z_BUS_FWD - Z_BUS_AFT), radius=R_BUS, axis='z', rings=6, t_count=8)

    # ==============================================================================
    # 5. TRANSVERSE PHOTOVOLTAIC SOLAR ARRAYS
    # ==============================================================================
    # Massive wings extending laterally from the equipment bus
    PANEL_X = 16.0
    PANEL_WIDTH = 2.0
    Z_PANEL = -6.5
    
    for sign in [-1, 1]:
        add_quad_mesh(lines, 'C_PANELS', 
                      (R_BUS*sign, -PANEL_WIDTH, Z_PANEL), (PANEL_X*sign, -PANEL_WIDTH, Z_PANEL),
                      (PANEL_X*sign, PANEL_WIDTH, Z_PANEL), (R_BUS*sign, PANEL_WIDTH, Z_PANEL), 
                      u_steps=12, v_steps=4)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_atlast_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry flawlessly at payload centroid
        cam_x, cam_y, cam_z = 0.0, 0.0, 2.0
        
        # Starts explicitly from 115-degrees (Dramatic aesthetic exposing the massive layered sunshield and primary optics)
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
    # Anchor Centroid = Z=2.0. Sunshield extends Y +/- 20m, optics reach Z=12.0m, bus reaches Z=-8.5m.
    # Setting cam_span strictly to 24.0 locks horizontal width symmetrically across a colossal 48.0m.
    # Vertical bounds output 24.0 * 1.777 = 42.648m total height window vertically.
    # Completely traps the 40-metre extreme boundaries of the observatory securely within the viewpoint,
    # ensuring absolute zero graphical UI clipping during continuous orbital rotation.
    cam_span = 24.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_SHIELD',    C_SHIELD,    0.9, 1.0),
        ('C_BUS',       C_BUS,       1.4, 1.0),
        ('C_PANELS',    C_PANELS,    1.2, 1.0),
        ('C_TRUSS',     C_TRUSS,     1.3, 1.0),
        ('C_MIRROR',    C_MIRROR,    1.6, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to clearly parse the vast deployed sunshield layers beneath the parabolic primary matrix
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-452m // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // ADVANCED TECHNOLOGY LARGE-APERTURE SPACE TELESCOPE", color=C_SHIELD, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_PANELS, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: 16M PARABOLIC MIRROR / MULTI-LAYER SUNSHIELD / OCTAGONAL AFT BUS", color=C_MIRROR, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-452m: ATLAST TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
