"""
PROJECT: Logic Garden 449m (Exact Physical Construct // 6-Axis Industrial Robot Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: INDUSTRIAL ROBOT, 6-AXIS ARM, WIREFRAME, ENGINEERING, KINEMATICS, AUTOMATION
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Scaled directly from the 256.88 blueprint, True Truss Cutouts.
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
OUT_DIR = "frames_449m_robot_arm"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_BASE      = '#1E293B'          # Carbon Slate (Heavy Cast Iron Base)
C_ROBOT     = '#D95F22'          # Industrial Amber/Orange (Primary Arm Castings)
C_JOINT     = '#94A3B8'          # Machined Steel (Cylinders, Linkages, Pistons)
C_MOTOR     = '#111115'          # Indestructible Black (Servo Housings)
C_TOOL      = '#005599'          # Deep Marine (End Effector Payload)
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
    """Extrudes a complex 2D X-Z engineering profile strictly across the Y-axis."""
    xs = [p[0] for p in xz_points]
    zs = [p[1] for p in xz_points]
    if close_loop:
        xs.append(xs[0])
        zs.append(zs[0])
        
    # Y-min plane
    append_segmented(lines_dict, col_key, xs, [y_min]*len(xs), zs)
    # Y-max plane
    append_segmented(lines_dict, col_key, xs, [y_max]*len(xs), zs)
    # Transverse connecting bridges
    for x, z in xz_points:
        append_segmented(lines_dict, col_key, [x, x], [y_min, y_max], [z, z])

def add_cylinder(lines_dict, col_key, cx, cy, cz, length, radius, axis='y', rings=6):
    """Parametric cylinder generation locked to an explicit Cartesian axis."""
    t = np.linspace(0, 2*np.pi, 12)
    steps = np.linspace(0, length, rings)
    
    for s in steps:
        if axis == 'y':
            ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + s), cz + radius*np.sin(t)
        elif axis == 'x':
            ix, iy, iz = np.full_like(t, cx + s), cy + radius*np.cos(t), cz + radius*np.sin(t)
        else: # z
            ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), np.full_like(t, cz + s)
        append_segmented(lines_dict, col_key, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
        
    for a in t[::3]: # 4 Stringers
        if axis == 'y':
            sx, sy, sz = [cx + radius*np.cos(a)]*rings, cy + steps, [cz + radius*np.sin(a)]*rings
        elif axis == 'x':
            sx, sy, sz = cx + steps, [cy + radius*np.cos(a)]*rings, [cz + radius*np.sin(a)]*rings
        else:
            sx, sy, sz = [cx + radius*np.cos(a)]*rings, [cy + radius*np.sin(a)]*rings, cz + steps
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
def generate_robot_vectors():
    lines = {
        'C_BASE': [], 'C_ROBOT': [], 'C_JOINT': [], 
        'C_MOTOR': [], 'C_TOOL': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. BASEPLATE ENVELOPE (REFERENCE GRID)
    # ==============================================================================
    gx_range = np.linspace(-3, 3, 13) 
    for gx in gx_range:
        append_segmented(lines, 'C_GRID', np.full_like(gx_range, gx), gx_range, np.zeros_like(gx_range))
        append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gx), np.zeros_like(gx_range))

    # ==============================================================================
    # 2. HEAVY CAST BASE & WAIST TURRET (Axis 1)
    # Dimensions scaled strictly from 256.88 blueprint relative units.
    # ==============================================================================
    # 0.55 relative height base
    base_prof = [(-0.8, 0.0), (0.8, 0.0), (0.8, 0.3), (0.6, 0.55), (-0.6, 0.55), (-0.8, 0.3)]
    extrude_profile(lines, 'C_BASE', base_prof, -0.6, 0.6)
    
    # Rotating Waist Hub (Z=0.55 to 0.75)
    add_cylinder(lines, 'C_ROBOT', 0.0, 0.0, 0.55, 0.2, 0.5, axis='z')
    
    # Rising Shoulders (Forks) holding the primary axis
    extrude_profile(lines, 'C_ROBOT', [(-0.35, 0.75), (0.35, 0.75), (0.2, 1.2), (-0.4, 1.2)], 0.3, 0.5)
    extrude_profile(lines, 'C_ROBOT', [(-0.35, 0.75), (0.35, 0.75), (0.2, 1.2), (-0.4, 1.2)], -0.5, -0.3)
    
    # Axis 2 Shoulder Cylinder
    S_Z = 1.05
    add_cylinder(lines, 'C_JOINT', 0.0, -0.6, S_Z, 1.2, 0.22, axis='y')
    add_box(lines, 'C_MOTOR', 0.0, 0.65, S_Z, 0.25, 0.3, 0.25) # Servo Housing Right
    add_box(lines, 'C_MOTOR', 0.0, -0.65, S_Z, 0.25, 0.3, 0.25) # Servo Housing Left

    # ==============================================================================
    # 3. LOWER ARM (Link 1 - Axis 2 to 3)
    # The blueprint shows a massive rear-swept 125.86 unit linkage. 
    # ==============================================================================
    E_X, E_Z = -0.4, 2.3  # Elbow Axis target
    
    # Complex Profile tracing the rearward curve of Link 1
    arm1_prof = [
        (0.2, S_Z), (0.1, 1.5), (-0.1, 2.0), (-0.2, E_Z), 
        (-0.55, E_Z), (-0.55, 1.8), (-0.3, 1.3), (-0.25, S_Z)
    ]
    extrude_profile(lines, 'C_ROBOT', arm1_prof, -0.25, 0.25)
    
    # Internal Lightening Truss (Cutouts explicitly modelled)
    truss1 = [(-0.05, 1.2), (-0.15, 1.6), (-0.2, 1.9), (-0.35, 1.9), (-0.2, 1.6), (-0.15, 1.2)]
    extrude_profile(lines, 'C_ROBOT', truss1, -0.25, 0.25)
    
    # Parallel Drive Linkage (Rear stabilizer rod visible in diagram)
    add_cylinder(lines, 'C_JOINT', 0.0, 0.0, 0.0, 1.45, 0.04, axis='y') # Placeholder to be overridden
    # Manual diagonal cylinder construction for rigid rod:
    rx = [-0.4, -0.6]; rz = [0.85, 2.0]
    append_segmented(lines, 'C_JOINT', rx, [0.0, 0.0], rz)
    append_segmented(lines, 'C_JOINT', rx, [0.05, 0.05], rz)
    append_segmented(lines, 'C_JOINT', rx, [-0.05, -0.05], rz)
    
    # Axis 3 Elbow Cylinder
    add_cylinder(lines, 'C_JOINT', E_X, -0.45, E_Z, 0.9, 0.18, axis='y')
    add_box(lines, 'C_MOTOR', E_X, -0.5, E_Z, 0.25, 0.2, 0.25) # Elbow Servo

    # ==============================================================================
    # 4. UPPER ARM (Link 2 - Axis 3 to Wrist)
    # The diagram shows 131.25 extending aggressively forward.
    # ==============================================================================
    W_X, W_Z = 1.0, 2.3  # Wrist Axis base target
    
    arm2_prof = [
        (E_X, 2.15), (E_X-0.2, 2.45), (0.0, 2.45), (W_X, 2.35), 
        (W_X, 2.25), (0.2, 2.15), (-0.2, 2.15)
    ]
    extrude_profile(lines, 'C_ROBOT', arm2_prof, -0.2, 0.2)
    
    # Upper Arm Truss Cutout
    truss2 = [(E_X+0.3, 2.25), (-0.1, 2.35), (0.3, 2.35), (0.6, 2.3), (0.3, 2.25)]
    extrude_profile(lines, 'C_ROBOT', truss2, -0.2, 0.2)

    # ==============================================================================
    # 5. WRIST SUB-ASSEMBLY & END EFFECTOR (Axes 4, 5, 6)
    # ==============================================================================
    # Axis 4/5 Cross Joint
    add_cylinder(lines, 'C_JOINT', W_X, -0.25, W_Z, 0.5, 0.12, axis='y')
    extrude_profile(lines, 'C_ROBOT', [(W_X, W_Z+0.12), (W_X+0.25, W_Z+0.1), (W_X+0.25, W_Z-0.1), (W_X, W_Z-0.12)], -0.15, 0.15)
    
    # Axis 6 (Tool Flange)
    add_cylinder(lines, 'C_JOINT', W_X+0.25, 0.0, W_Z, 0.1, 0.1, axis='x')
    add_box(lines, 'C_JOINT', W_X+0.35, 0.0, W_Z, 0.05, 0.25, 0.25)
    
    # Heavy Payload / End Effector Box (Deep Marine)
    add_box(lines, 'C_TOOL', W_X+0.5, 0.0, W_Z, 0.25, 0.4, 0.15)
    add_box(lines, 'C_TOOL', W_X+0.5, 0.0, W_Z-0.1, 0.15, 0.15, 0.1)

    return lines

# ------------------------------------------------------------------
# PARALLEL GENERATOR STREAM (KINEMATIC TIMELINE TENSOR)
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_robot_vectors() # Computed once for true O(1) loop retrieval
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Central Basepoint: Mapping the structural centre of the robot base
        cam_x, cam_y, cam_z = 0.0, 0.0, 1.2 
        
        # Continuous 360-degree perfect orbital synchronisation
        # Initiates strictly from Right Profile (Azimuth = 90.0) where X extends forward.
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

    # Cinematic Rigid Map Boundary - Covers the ~2.6m vertical topology
    cam_span = 2.4
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []

    # 1. PROCESS KINEMATIC VECTOR MATRIX
    for c_key, c_val in [('C_GRID', C_GRID), ('C_BASE', C_BASE), ('C_ROBOT', C_ROBOT), 
                         ('C_JOINT', C_JOINT), ('C_MOTOR', C_MOTOR), ('C_TOOL', C_TOOL)]:
        
        if c_key == 'C_GRID': lw, alpha = 0.8, 0.4
        elif c_key == 'C_BASE': lw, alpha = 1.8, 1.0     
        elif c_key == 'C_ROBOT': lw, alpha = 1.8, 1.0      
        elif c_key == 'C_JOINT': lw, alpha = 1.2, 1.0  
        elif c_key == 'C_MOTOR': lw, alpha = 2.0, 1.0   
        elif c_key == 'C_TOOL': lw, alpha = 2.0, 1.0   
        else: lw, alpha = 1.0, 1.0
            
        for xl, yl, zl in static_rig[c_key]:
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=22.0)
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

    ax.text(-cam_span*0.95, ui_t+1.0, "LG-449m // MACRO-ENGINEERING TENSOR: INDUSTRIAL AUTOMATION", color=C_TEXT, fontsize=20, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t+0.3, "EXPLICIT TRUE-SCALE GEOMETRY // 6-AXIS KINEMATIC MATRIX", color=C_ROBOT, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b+1.0, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_JOINT, fontsize=17, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.5, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS SYNCHRONISATION)", color=C_TEXT, fontsize=17, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.1, "GEOMETRY YIELD   : 256.88MM BLUEPRINT RATIOS / STRUCTURAL TRUSSES", color=C_TOOL, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-449m: 6-AXIS ROBOT MACRO-ENGINEERING TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Kinematic Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
