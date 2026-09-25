"""
PROJECT: Logic Garden 449n (Exact Physical Construct // Heavy Bulldozer Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: BULLDOZER, HEAVY EQUIPMENT, TRACTOR, ROOT RAKE, WIREFRAME, ENGINEERING, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Enclosed Cab, ROPS cage, Root-Rake blade array, True Grouser Tracks.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from absolute Side Profile.
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
OUT_DIR = "frames_449n_bulldozer"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_TRACTOR   = '#FFB300'          # Dense Amber (Main Hull, Engine, Cab details)
C_BLADE     = '#1E293B'          # Carbon Slate (Heavy-duty Root Rake & Push Arms)
C_TRACKS    = '#111115'          # Indestructible Black (Tracks, Grousers, Sprockets)
C_ROPS      = '#475569'          # Slate Grey (Roll-Over Protection Structure)
C_HYD       = '#94A3B8'          # Machined Steel (Lift/Tilt Cylinders)
C_GLASS     = '#005599'          # Deep Marine (Cabin Window Trim)
C_GRID      = '#CBD5E1'          # Subdued Steel (Baseplate Reference)

# ------------------------------------------------------------------
# O(N) KINEMATIC WIREFRAME ENGINE
# ------------------------------------------------------------------
def project_3d_depth(x, y, z, cx, cy, cz, az_deg, el_deg=0):
    tx, ty, tz = x - cx, y - cy, z - cz
    az, el = np.radians(az_deg), np.radians(el_deg)
    
    # Orbit Matrix
    x1 = tx * np.cos(az) - ty * np.sin(az)
    y1 = tx * np.sin(az) + ty * np.cos(az)
    z1 = tz
    
    # Elevation Matrix
    y2 = y1 * np.cos(el) - z1 * np.sin(el)
    z2 = y1 * np.sin(el) + z1 * np.cos(el)
    
    return x1, z2, y2 

def append_segmented(lines_dict, key, xs, ys, zs):
    """Absolute Segmentation Protocol: Splits arrays into 2-point vectors for absolute Painter depth sorting."""
    for i in range(len(xs) - 1):
        lines_dict[key].append(([xs[i], xs[i+1]], [ys[i], ys[i+1]], [zs[i], zs[i+1]]))

def extrude_profile(lines_dict, col_key, xz_points, y_min, y_max, close_loop=True):
    """Extrudes a 2D X-Z profile strictly across the Y-axis."""
    xs = [p[0] for p in xz_points]
    zs = [p[1] for p in xz_points]
    if close_loop:
        xs.append(xs[0])
        zs.append(zs[0])
        
    append_segmented(lines_dict, col_key, xs, [y_min]*len(xs), zs)
    append_segmented(lines_dict, col_key, xs, [y_max]*len(xs), zs)
    for x, z in xz_points:
        append_segmented(lines_dict, col_key, [x, x], [y_min, y_max], [z, z])

def add_cylinder(lines_dict, col_key, cx, cy, cz, length, radius, axis='y', rings=6):
    """Parametric cylinder generation locked to an explicit Cartesian axis."""
    t = np.linspace(0, 2*np.pi, 12)
    steps = np.linspace(0, length, rings)
    
    for s in steps:
        if axis == 'y':  ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + s), cz + radius*np.sin(t)
        elif axis == 'x': ix, iy, iz = np.full_like(t, cx + s), cy + radius*np.cos(t), cz + radius*np.sin(t)
        else:             ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), np.full_like(t, cz + s)
        append_segmented(lines_dict, col_key, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
        
    for a in t[::3]: 
        if axis == 'y':   sx, sy, sz = [cx + radius*np.cos(a)]*rings, cy + steps, [cz + radius*np.sin(a)]*rings
        elif axis == 'x': sx, sy, sz = cx + steps, [cy + radius*np.cos(a)]*rings, [cz + radius*np.sin(a)]*rings
        else:             sx, sy, sz = [cx + radius*np.cos(a)]*rings, [cy + radius*np.sin(a)]*rings, cz + steps
        append_segmented(lines_dict, col_key, sx, sy, sz)

def add_box(lines_dict, col_key, cx, cy, cz, dx, dy, dz):
    """Rigid 3D orthogonal bounding-box construction."""
    hx, hy, hz = dx/2, dy/2, dz/2
    xs = [cx-hx, cx+hx, cx+hx, cx-hx, cx-hx]
    ys1 = [cy-hy, cy-hy, cy+hy, cy+hy, cy-hy]
    ys2 = [cy-hy, cy-hy, cy+hy, cy+hy, cy-hy]
    
    append_segmented(lines_dict, col_key, xs, ys1, [cz-hz]*5)
    append_segmented(lines_dict, col_key, xs, ys2, [cz+hz]*5)
    for i in range(4):
        append_segmented(lines_dict, col_key, [xs[i], xs[i]], [ys1[i], ys1[i]], [cz-hz, cz+hz])

# ------------------------------------------------------------------
# RIGID 3D EXACT KINEMATIC GENERATOR
# ------------------------------------------------------------------
def generate_dozer_vectors():
    lines = {
        'C_TRACTOR': [], 'C_BLADE': [], 'C_TRACKS': [], 
        'C_ROPS': [], 'C_HYD': [], 'C_GLASS': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. BASEPLATE ENVELOPE (REFERENCE GRID)
    # ==============================================================================
    gx_range = np.linspace(-4, 4, 17) 
    for gx in gx_range:
        append_segmented(lines, 'C_GRID', np.full_like(gx_range, gx), gx_range, np.zeros_like(gx_range))
        append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gx), np.zeros_like(gx_range))

    # ==============================================================================
    # 2. CONTINUOUS CRAWLER TRACKS AND SPROCKETS
    # ==============================================================================
    # Left and Right track centers
    for t_y in [-1.3, 1.3]:
        # Track loop mathematically constructed (Oval)
        # Rear Sprocket
        th1 = np.linspace(np.pi/2, 3*np.pi/2, 10)
        rx = -1.6 + 0.5 * np.cos(th1)
        rz =  0.6 + 0.5 * np.sin(th1)
        # Front Idler
        th2 = np.linspace(-np.pi/2, np.pi/2, 10)
        fx =  2.0 + 0.4 * np.cos(th2)
        fz =  0.5 + 0.4 * np.sin(th2)
        
        # Combine loop
        px = list(rx) + list(fx)[::-1] + [rx[0]]
        pz = list(rz) + list(fz)[::-1] + [rz[0]]
        
        # Extrude inner/outer track perimeter
        tw = 0.3 # Half-width of track
        append_segmented(lines, 'C_TRACKS', px, [t_y - tw]*len(px), pz)
        append_segmented(lines, 'C_TRACKS', px, [t_y + tw]*len(px), pz)
        
        # Drive Sprockets & Hubs
        add_cylinder(lines, 'C_TRACKS', -1.6, t_y-0.2, 0.6, 0.4, 0.45)
        add_cylinder(lines, 'C_TRACKS',  2.0, t_y-0.2, 0.5, 0.4, 0.35)
        
        # Transverse Grouser Plates (Rigid steps on the tracks)
        # Resample the perimeter evenly for 45 grousers
        t_len = 45
        g_x = np.interp(np.linspace(0, len(px)-1, t_len), np.arange(len(px)), px)
        g_z = np.interp(np.linspace(0, len(px)-1, t_len), np.arange(len(px)), pz)
        for gx, gz in zip(g_x, g_z):
            append_segmented(lines, 'C_TRACKS', [gx, gx], [t_y - tw, t_y + tw], [gz, gz])
            # Add grouser tooth (small extrusion normal to path)
            append_segmented(lines, 'C_TRACKS', [gx, gx+0.05], [t_y - tw, t_y - tw], [gz, gz+0.05])

    # ==============================================================================
    # 3. TRACTOR HULL & ENGINE (Amber Substrate)
    # ==============================================================================
    # Main Belly / Core block
    add_box(lines, 'C_TRACTOR', 0.2, 0.0, 0.9, 4.0, 1.8, 0.8)
    
    # Forward Engine Hood (Sloping front)
    hood_prof = [(0.2, 1.3), (2.0, 1.3), (2.4, 1.2), (2.4, 1.8), (0.2, 2.0)]
    extrude_profile(lines, 'C_TRACTOR', hood_prof, -0.7, 0.7)
    
    # Radiator Grille
    for gy in np.linspace(-0.5, 0.5, 6):
        append_segmented(lines, 'C_TRACTOR', [2.4, 2.4], [gy, gy], [1.2, 1.8])

    # Rear Chassis / Equipment box
    add_box(lines, 'C_TRACTOR', -1.2, 0.0, 1.6, 1.6, 1.7, 0.6)

    # ==============================================================================
    # 4. ENCLOSED CABIN & ROPS CAGE
    # ==============================================================================
    # Glass Cabin block
    cab_prof = [(-1.3, 1.9), (0.2, 1.9), (0.2, 2.9), (-1.3, 2.9)]
    extrude_profile(lines, 'C_GLASS', cab_prof, -0.8, 0.8)
    # Cabin door split
    append_segmented(lines, 'C_GLASS', [-0.5, -0.5], [-0.8, -0.8], [1.9, 2.9])
    append_segmented(lines, 'C_GLASS', [-0.5, -0.5], [0.8, 0.8], [1.9, 2.9])

    # Heavy ROPS (Roll-Over Protection Structure) Tubing Layer
    rx1, rx2 = -1.5, 0.4
    ry = 0.9
    rz1, rz2 = 1.9, 3.1
    # Top Box
    add_box(lines, 'C_ROPS', (rx1+rx2)/2, 0.0, rz2, (rx2-rx1), ry*2, 0.1)
    # Main Pillars
    for yp in [-ry, ry]:
        append_segmented(lines, 'C_ROPS', [rx1, rx1], [yp, yp], [rz1, rz2])
        append_segmented(lines, 'C_ROPS', [rx2, rx2], [yp, yp], [rz1, rz2])
        # Diagonal sheer truss to engine block
        append_segmented(lines, 'C_ROPS', [rx2, 1.5], [yp, yp], [rz2, 1.9])

    # ==============================================================================
    # 5. PUSH ARMS & HYDRAULIC CYLINDERS
    # ==============================================================================
    # C-Frame Push Arms mounting to the outside of the track frames
    for sign in [-1, 1]:
        arm_prof = [(-1.0, 0.7), (2.8, 0.5), (3.0, 0.8), (2.8, 1.0), (-1.0, 0.9)]
        extrude_profile(lines, 'C_BLADE', arm_prof, (1.6*sign)-0.1, (1.6*sign)+0.1)
        # Mounting hub at chassis
        add_cylinder(lines, 'C_BLADE', -1.0, 1.2*sign, 0.8, 0.4, 0.2, axis='y')

    # Hydraulic Lift Cylinders (Hood to Blade Base)
    # Fixed base at hood side: (0.8, +/-0.8, 2.0)
    # Rod attaches to blade pivot: (2.8, +/-1.6, 0.7)
    for sign in [-1, 1]:
        rx = [0.8, 2.8]
        ry = [0.8*sign, 1.6*sign]
        rz = [2.0, 0.7]
        # Main heavy cylinder barrel
        append_segmented(lines, 'C_HYD', [0.8, 1.8], [0.8*sign, 1.2*sign], [2.0, 1.35])
        append_segmented(lines, 'C_HYD', [0.8, 1.8], [0.8*sign, 1.2*sign], [2.1, 1.45])
        # Inner polished rod
        append_segmented(lines, 'C_HYD', [1.8, 2.8], [1.2*sign, 1.6*sign], [1.4, 0.7])
        
    # Hydraulic Tilt Cylinders (Push Arm to upper Blade)
    for sign in [-1, 1]:
        append_segmented(lines, 'C_HYD', [1.8, 3.0], [1.6*sign, 1.6*sign], [0.9, 1.5])

    # ==============================================================================
    # 6. ROOT RAKE BLADE (Multi-Shank Array)
    # ==============================================================================
    # Dual Horizontal Support Beams
    add_box(lines, 'C_BLADE', 3.0, 0.0, 1.5, 0.2, 4.0, 0.2)
    add_box(lines, 'C_BLADE', 2.9, 0.0, 0.6, 0.3, 4.0, 0.3)
    
    # Curved Vertical Clearing Tines (11 Shanks)
    shank_ys = np.linspace(-1.9, 1.9, 11)
    shank_prof = [
        (2.9, 1.8), (3.0, 0.9), (3.3, 0.3), (3.6, 0.0), 
        (3.4, 0.3), (3.2, 0.9), (3.1, 1.8)
    ]
    for sy in shank_ys:
        extrude_profile(lines, 'C_BLADE', shank_prof, sy-0.06, sy+0.06)

    return lines

# ------------------------------------------------------------------
# PARALLEL GENERATOR STREAM (KINEMATIC TIMELINE TENSOR)
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_dozer_vectors() # Computed once for true O(1) loop retrieval
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Central Basepoint: Mapping the structural centre of the machine
        cam_x, cam_y, cam_z = 0.5, 0.0, 1.2 
        
        # Continuous 360-degree perfect orbital synchronisation
        # Initiates strictly from Right Profile (Azimuth = 90.0).
        azimuth = 90.0 - (stage * 360.0)

        yield (f, t_sec, azimuth, cam_x, cam_y, cam_z, static_rig)

# ------------------------------------------------------------------
# THREAD-SAFE PAINTER'S RENDERER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, azimuth, cx, cy, cz, static_rig = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # Cinematic Rigid Map Boundary - Covers the ~7.0m longitudinal topology
    cam_span = 4.8
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []

    # 1. PROCESS KINEMATIC VECTOR MATRIX
    for c_key, c_val in [('C_GRID', C_GRID), ('C_TRACTOR', C_TRACTOR), ('C_TRACKS', C_TRACKS), 
                         ('C_BLADE', C_BLADE), ('C_ROPS', C_ROPS), ('C_HYD', C_HYD), ('C_GLASS', C_GLASS)]:
        
        if c_key == 'C_GRID': lw, alpha = 0.8, 0.4
        elif c_key == 'C_TRACTOR': lw, alpha = 1.3, 1.0     
        elif c_key == 'C_TRACKS': lw, alpha = 1.2, 1.0      
        elif c_key == 'C_BLADE': lw, alpha = 1.5, 1.0  
        elif c_key == 'C_ROPS': lw, alpha = 2.2, 1.0   
        elif c_key == 'C_HYD': lw, alpha = 1.6, 1.0   
        elif c_key == 'C_GLASS': lw, alpha = 1.1, 1.0   
        else: lw, alpha = 1.0, 1.0
            
        for xl, yl, zl in static_rig[c_key]:
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=20.0)
            render_queue.append((np.mean(depth), u, v-0.4, c_val, lw, alpha))

    # 2. ABSOLUTE PAINTER'S ALGORITHM
    render_queue.sort(key=lambda item: item[0], reverse=True)

    for depth, u, v, c, lw, a in render_queue:
        ax.plot(u, v, color=c, lw=lw, alpha=a)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (TOP HUD)
    # ------------------------------------------------------------------
    ui_t = cam_span * 1.45
    ax.add_patch(patches.Rectangle((-cam_span, ui_t), cam_span*2, 8.0, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_t, ui_t], color=C_TEXT, lw=6, zorder=81)

    ax.text(-cam_span*0.95, ui_t+1.0, "LG-449n // MACRO-ENGINEERING TENSOR: EARTHMOVING", color=C_TEXT, fontsize=20, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t+0.3, "EXPLICIT TRUE-SCALE GEOMETRY // TRACTOR MATRIX", color=C_TRACTOR, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b+1.0, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_BLADE, fontsize=17, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.5, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS SYNCHRONISATION)", color=C_TEXT, fontsize=17, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.1, "GEOMETRY YIELD   : CONTINUOUS GROUSER TRACKS / ROOT RAKE TENSOR", color=C_ROPS, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-449n: HEAVY DOZER MACRO-ENGINEERING TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Kinematic Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
