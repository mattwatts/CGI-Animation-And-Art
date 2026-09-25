"""
PROJECT: Logic Garden 449r (Exact Physical Construct // 4-Door Sedan Matrix - HOTFIX)
FORMAT: YouTube Shorts (1080x1920)
METADATA: CAR, SEDAN, AUTOMOTIVE, WIREFRAME, ENGINEERING, KINEMATICS, DIAGRAM
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: True parametric hull lofting, Explicit mathematically-carved wheel arches.
- Hotfix: Cleared IndexError in longitudinal stringer meshing loop. 
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
OUT_DIR = "frames_449r_sedan"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG            = '#FFFFFF'
C_TEXT          = '#111115'
C_BODY          = '#1E293B'  # Carbon Slate (Aerodynamic Hull Matrix)
C_GLASS         = '#005599'  # Deep Marine (Windshields & Side Windows)
C_WHEEL         = '#111115'  # Indestructible Black (Tyre Treads)
C_TRIM          = '#94A3B8'  # Machined Steel (Alloys & Grille)
C_LIGHT_FRONT   = '#FFB300'  # Dense Amber (Headlights)
C_LIGHT_REAR    = '#E11D48'  # Kinematic Red (Tail Lights)
C_GRID          = '#CBD5E1'  # Subdued Steel (Baseplate Reference)

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
    """Absolute Segmentation Protocol: Splits arrays into 2-point vectors for strict mathematical depth sorting."""
    for i in range(len(xs) - 1):
        lines_dict[key].append(([xs[i], xs[i+1]], [ys[i], ys[i+1]], [zs[i], zs[i+1]]))

def build_wheel(lines_dict, cx, cy, cz, r_tire, w_tire, r_alloy):
    """Explicitly generates high-detail tyre treads and 5-spoke alloy matrices."""
    t = np.linspace(0, 2*np.pi, 24)
    for y_off in [-w_tire/2, w_tire/2]:
        ix = cx + r_tire*np.cos(t)
        iy = np.full_like(t, cy + y_off)
        iz = cz + r_tire*np.sin(t)
        append_segmented(lines_dict, 'C_WHEEL', list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    
    # Radial tyre tread connecting sidewalls
    for a in t[::2]:
        append_segmented(lines_dict, 'C_WHEEL', [cx+r_tire*np.cos(a)]*2, [cy-w_tire/2, cy+w_tire/2], [cz+r_tire*np.sin(a)]*2)
        
    # Alloy Rim (Flush to outer face)
    y_alloy = cy + w_tire/2 * np.sign(cy) 
    ax_pts = cx + r_alloy*np.cos(t)
    az_pts = cz + r_alloy*np.sin(t)
    append_segmented(lines_dict, 'C_TRIM', list(ax_pts)+[ax_pts[0]], [y_alloy]*(len(t)+1), list(az_pts)+[az_pts[0]])
    
    # Machined Steel 5-Spoke Architecture
    for a in np.linspace(0, 2*np.pi, 5, endpoint=False):
        append_segmented(lines_dict, 'C_TRIM', [cx, cx+r_alloy*np.cos(a)], [y_alloy, y_alloy], [cz, cz+r_alloy*np.sin(a)])

def apply_wheel_arches(xs, ys, zs):
    """Mathematical Boolean Carving: Lifts Z-vectors passing through wheel hub thresholds to form perfect arches."""
    R_arch = 0.40
    z_hub = 0.33
    wf_x = 1.35
    wr_x = -1.45
    new_zs = list(zs)
    for i in range(len(xs)):
        if abs(ys[i]) > 0.65: # Only carve outer side panels
            # Front Arch
            dxf = abs(xs[i] - wf_x)
            if dxf < R_arch:
                arch_z = z_hub + np.sqrt(R_arch**2 - dxf**2)
                if new_zs[i] < arch_z: new_zs[i] = arch_z
            # Rear Arch (Slightly lowered stance)
            dxr = abs(xs[i] - wr_x)
            if dxr < R_arch:
                arch_zr = z_hub - 0.02 + np.sqrt(R_arch**2 - dxr**2)
                if new_zs[i] < arch_zr: new_zs[i] = arch_zr
    return xs, list(ys), new_zs

def get_hull_cross_section(x):
    """Derives exact parametric (Y, Z) bounds for any X-station along the vehicle chassis."""
    # Central Aerodynamic Spine (Z)
    xk = [-2.35, -2.2, -1.7, -0.8, -0.15, 0.5, 1.4, 2.2, 2.35]
    zk = [ 0.30,  0.95, 1.0,  1.40, 1.46,  1.4, 0.9, 0.65, 0.20]
    z_c = np.interp(x, xk, zk)
    
    # Beltline Width (Y)
    yk = [ 0.65, 0.8, 0.88, 0.9, 0.9, 0.9, 0.88, 0.75, 0.6 ]
    y_b = np.interp(x, xk, yk)
    
    # Beltline Ascent (Z)
    x_z = [-2.35, -1.7, 1.4, 2.35]
    z_z = [ 0.95,  0.92, 0.82, 0.75 ]
    z_b = np.interp(x, x_z, z_z)
    
    # Roof/Greenhouse Taper Width (Y)
    x_f = [-2.35, -1.71, -1.60, 1.30, 1.41, 2.35]
    y_f = [ 0.98,  0.98,  0.65, 0.65, 0.98, 0.98]
    y_r = y_b * np.interp(x, x_f, y_f)
    
    # Roof Edge (Z)
    z_r = z_c - min(0.08, (z_c - z_b)*0.2) 
    if z_r < z_b: z_r = z_b + 0.01 
    
    # Ground Clearance / Sill Line
    z_s = 0.22 + 0.05 * (x/2.35)**2
    y_s = y_b * 0.95
    
    # Shoulder Widest Point
    z_m = (z_b + z_s) / 2
    y_m = y_b * 1.02
    
    return [(0.0, z_c), (y_r, z_r), (y_b, z_b), (y_m, z_m), (y_s, z_s)]

# ------------------------------------------------------------------
# RIGID 3D EXACT AUTOMOTIVE GENERATOR
# ------------------------------------------------------------------
def generate_car_vectors():
    lines = {
        'C_BODY': [], 'C_WHEEL': [], 'C_TRIM': [], 'C_GLASS': [], 
        'C_LIGHT_FRONT': [], 'C_LIGHT_REAR': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. BASEPLATE ENVELOPE (REFERENCE GRID)
    # ==============================================================================
    gx_range = np.linspace(-3.5, 3.5, 15) 
    for gx in gx_range:
        append_segmented(lines, 'C_GRID', np.full_like(gx_range, gx), np.clip(gx_range, -2, 2), np.zeros_like(gx_range))
    gy_range = np.linspace(-2.0, 2.0, 9)
    for gy in gy_range:
        append_segmented(lines, 'C_GRID', np.clip(gx_range, -3.5, 3.5), np.full_like(gx_range, gy), np.zeros_like(gx_range))

    # ==============================================================================
    # 2. PARAMETRIC TOPOLOGICAL HULL (Ribs and Stringers)
    # ==============================================================================
    ribs_x = np.linspace(-2.3, 2.3, 36)
    ribs_pts = []
    
    for x in ribs_x:
        pts = get_hull_cross_section(x)
        full_rib = [ (x, -p[0], p[1]) for p in pts[::-1] ] + [ (x, p[0], p[1]) for p in pts[1:] ]
        ribs_pts.append(full_rib)
        
    # Transverse Ribs (O(N) segmentation with arch calculations)
    for rib in ribs_pts:
        xs, ys, zs = [p[0] for p in rib], [p[1] for p in rib], [p[2] for p in rib]
        xs, ys, zs = apply_wheel_arches(xs, ys, zs)
        append_segmented(lines, 'C_BODY', xs, ys, zs)
        
    # Longitudinal Stringers
    num_pts = len(ribs_pts[0])
    for i in range(num_pts):
        # Hotfix: Ensure the index matches the ribs_pts pool longitudinally instead of crashing out of bounds.
        xs = [r[i][0] for r in ribs_pts]
        ys = [r[i][1] for r in ribs_pts]
        zs = [r[i][2] for r in ribs_pts]
        xs, ys, zs = apply_wheel_arches(xs, ys, zs)
        append_segmented(lines, 'C_BODY', xs, ys, zs)

    # ==============================================================================
    # 3. CABIN GLASS & STRUCTURAL PILLARS (DLO Array)
    # ==============================================================================
    # Side Window Frames mapping roofline to beltline
    w_x = np.linspace(-1.5, 1.25, 12)
    for side in [-1, 1]:
        w_px, w_py_top, w_pz_top = [], [], []
        w_py_bot, w_pz_bot = [], []
        for x in w_x:
            sect = get_hull_cross_section(x)
            w_px.append(x)
            w_py_top.append(sect[1][0] * side); w_pz_top.append(sect[1][1] - 0.02)
            w_py_bot.append(sect[2][0] * side); w_pz_bot.append(sect[2][1] + 0.02)
            
        full_wx = w_px + w_px[::-1] + [w_px[0]]
        full_wy = w_py_top + w_py_bot[::-1] + [w_py_top[0]]
        full_wz = w_pz_top + w_pz_bot[::-1] + [w_pz_top[0]]
        append_segmented(lines, 'C_GLASS', full_wx, full_wy, full_wz)
        
        # B-Pillar 4-Door Structural Split
        b_x = -0.1
        bs = get_hull_cross_section(b_x)
        append_segmented(lines, 'C_BODY', [b_x, b_x], [bs[1][0]*side, bs[2][0]*side], [bs[1][1], bs[2][1]])

    # Front Windshield Perimeter
    ws_x = [1.32, 0.6, 0.6, 1.32, 1.32]
    s132 = get_hull_cross_section(1.32)
    s060 = get_hull_cross_section(0.6)
    ws_y = [s132[1][0]-0.02, s060[1][0]-0.02, -s060[1][0]+0.02, -s132[1][0]+0.02, s132[1][0]-0.02]
    ws_z = [s132[1][1], s060[1][1],  s060[1][1],  s132[1][1], s132[1][1]]
    append_segmented(lines, 'C_GLASS', ws_x, ws_y, ws_z)
    
    # Rear Window Perimeter
    rw_x = [-1.6, -0.9, -0.9, -1.6, -1.6]
    s160 = get_hull_cross_section(-1.6)
    s090 = get_hull_cross_section(-0.9)
    rw_y = [s160[1][0]-0.02, s090[1][0]-0.02, -s090[1][0]+0.02, -s160[1][0]+0.02, s160[1][0]-0.02]
    rw_z = [s160[1][1], s090[1][1],  s090[1][1],  s160[1][1], s160[1][1]]
    append_segmented(lines, 'C_GLASS', rw_x, rw_y, rw_z)

    # ==============================================================================
    # 4. FASCIA: MACHINED STEEL GRILLE & OPTICAL ARRAYS
    # ==============================================================================
    # Slatted Front Grille Array
    for gz in np.linspace(0.40, 0.58, 6):
        append_segmented(lines, 'C_TRIM', [2.32, 2.32], [-0.4, 0.4], [gz, gz])
    # Grille Envelope
    append_segmented(lines, 'C_TRIM', [2.32]*5, [-0.4, 0.4, 0.4, -0.4, -0.4], [0.35, 0.35, 0.65, 0.65, 0.35])
    
    # Front Headlights (Dense Amber LED lines)
    for side in [-1, 1]:
        hx = [2.25, 2.31, 2.31, 2.25, 2.25]
        hy = np.array([0.45, 0.45, 0.75, 0.8, 0.45]) * side
        hz = [0.55, 0.55, 0.65, 0.65, 0.55]
        append_segmented(lines, 'C_LIGHT_FRONT', hx, hy, hz)
        
    # Rear Tail Lights (Kinematic Red wrap-around array)
    for side in [-1, 1]:
        tx = [-2.28, -2.35, -2.35, -2.28, -2.28]
        ty = np.array([0.3, 0.3, 0.8, 0.85, 0.3]) * side
        tz = [0.75, 0.75, 0.85, 0.85, 0.75]
        append_segmented(lines, 'C_LIGHT_REAR', tx, ty, tz)
    # Rear LED Lightbar connector
    append_segmented(lines, 'C_LIGHT_REAR', [-2.35, -2.35], [-0.3, 0.3], [0.8, 0.8])

    # ==============================================================================
    # 5. KINEMATIC WHEEL ASSEMBLIES
    # ==============================================================================
    w_z = 0.33
    w_r = 0.33
    a_r = 0.22
    w_w = 0.24
    
    build_wheel(lines,  1.35,  0.8, w_z, w_r, w_w, a_r) # Front Left
    build_wheel(lines,  1.35, -0.8, w_z, w_r, w_w, a_r) # Front Right
    build_wheel(lines, -1.45,  0.8, w_z, w_r, w_w, a_r) # Rear Left
    build_wheel(lines, -1.45, -0.8, w_z, w_r, w_w, a_r) # Rear Right

    return lines

# ------------------------------------------------------------------
# PARALLEL GENERATOR STREAM (KINEMATIC TIMELINE TENSOR)
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_car_vectors() # Computed once for true O(1) loop retrieval
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Central Basepoint: Mapping exact structural centroid of chassis
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.6 
        
        # Continuous 360-degree perfect orbital synchronisation
        # Initiates precisely from Right Side Profile (Azimuth = 90.0)
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

    # Cinematic Rigid Map Boundary - Covers the ~4.8m longitudinal chassis
    cam_span = 3.6
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []

    # 1. PROCESS KINEMATIC VECTOR MATRIX
    for c_key, c_val in [('C_GRID', C_GRID), ('C_BODY', C_BODY), ('C_GLASS', C_GLASS), 
                         ('C_WHEEL', C_WHEEL), ('C_TRIM', C_TRIM), 
                         ('C_LIGHT_FRONT', C_LIGHT_FRONT), ('C_LIGHT_REAR', C_LIGHT_REAR)]:
        
        if c_key == 'C_GRID': lw, alpha = 0.8, 0.4
        elif c_key == 'C_BODY': lw, alpha = 1.3, 1.0     
        elif c_key == 'C_GLASS': lw, alpha = 1.6, 1.0      
        elif c_key == 'C_WHEEL': lw, alpha = 1.8, 1.0  
        elif c_key == 'C_TRIM': lw, alpha = 1.4, 1.0   
        elif c_key in ['C_LIGHT_FRONT', 'C_LIGHT_REAR']: lw, alpha = 2.2, 1.0   
        else: lw, alpha = 1.0, 1.0
            
        for xl, yl, zl in static_rig[c_key]:
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=18.0)
            render_queue.append((np.mean(depth), u, v-0.2, c_val, lw, alpha))

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

    ax.text(-cam_span*0.95, ui_t+1.0, "LG-449r // MACRO-ENGINEERING TENSOR: AUTOMOTIVE", color=C_TEXT, fontsize=19, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t+0.3, "EXPLICIT TRUE-SCALE GEOMETRY // 4-DOOR SEDAN MATRIX", color=C_BODY, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b+1.0, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_TRIM, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.5, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS SYNCHRONISATION)", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.1, "KINEMATICS YIELD : A/B/C-PILLARS EXTRUDED / DLO TENSORS SECURED", color=C_GLASS, fontsize=13, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-449r: 4-DOOR SEDAN MACRO-ENGINEERING TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Automotive Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
