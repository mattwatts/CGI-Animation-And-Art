"""
PROJECT: Logic Garden 449o (Exact Physical Construct // Aerospace Drone Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: DRONE, QUADCOPTER, UAV, WIREFRAME, ENGINEERING, KINEMATICS, DIAGRAM
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Ducted fan shrouds, aerodynamic hull, camera gimbal, skid arrays.
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
OUT_DIR = "frames_449o_drone"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_FUSE      = '#1E293B'          # Carbon Slate (Central Aerodynamic Hull)
C_BODY      = '#475569'          # Slate Grey (Ducted fan shrouds and arms)
C_PROP      = '#94A3B8'          # Machined Steel (Motors and internal lattice)
C_SKID      = '#111115'          # Indestructible Black (Landing Skids)
C_GLASS     = '#005599'          # Deep Marine (Optical Payload Gimbal)
C_LIGHTS    = '#E11D48'          # Kinematic Red (Nav Beacons)
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

def add_cylinder_surface(lines_dict, col_key, cx, cy, cz, length, r_start, r_end, axis='z', rings=6, num_str=16):
    """Parametric cylinder shell rigorously segmented for depth-sorting."""
    t = np.linspace(0, 2*np.pi, num_str)
    steps = np.linspace(0, length, rings)
    
    # Hoop Rings
    for s in steps:
        ratio = s / length if length != 0 else 0
        r = r_start * (1 - ratio) + r_end * ratio
        if axis == 'z':   ix, iy, iz = cx + r*np.cos(t), cy + r*np.sin(t), np.full_like(t, cz + s)
        elif axis == 'y': ix, iy, iz = cx + r*np.cos(t), np.full_like(t, cy + s), cz + r*np.sin(t)
        elif axis == 'x': ix, iy, iz = np.full_like(t, cx + s), cy + r*np.cos(t), cz + r*np.sin(t)
        append_segmented(lines_dict, col_key, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
        
    # Stringers
    for a in t[::2]: 
        sx, sy, sz = [], [], []
        for s in steps:
            ratio = s / length if length != 0 else 0
            r = r_start * (1 - ratio) + r_end * ratio
            if axis == 'z':   sx.append(cx + r*np.cos(a)); sy.append(cy + r*np.sin(a)); sz.append(cz + s)
            elif axis == 'y': sx.append(cx + r*np.cos(a)); sy.append(cy + s); sz.append(cz + r*np.sin(a))
            elif axis == 'x': sx.append(cx + s); sy.append(cy + r*np.cos(a)); sz.append(cz + r*np.sin(a))
        append_segmented(lines_dict, col_key, sx, sy, sz)

def add_sphere(lines_dict, col_key, cx, cy, cz, r, slices=10, stacks=8):
    """Geometric sphere segmented into explicit vectors."""
    phi = np.linspace(0, np.pi, stacks)
    theta = np.linspace(0, 2*np.pi, slices)
    # Latitude rings
    for p in phi:
        rx = cx + r * np.sin(p) * np.cos(theta)
        ry = cy + r * np.sin(p) * np.sin(theta)
        rz = np.full_like(theta, cz + r * np.cos(p))
        append_segmented(lines_dict, col_key, list(rx), list(ry), list(rz))
    # Longitude arcs
    for t in theta:
        rx = cx + r * np.sin(phi) * np.cos(t)
        ry = cy + r * np.sin(phi) * np.sin(t)
        rz = cz + r * np.cos(phi)
        append_segmented(lines_dict, col_key, list(rx), list(ry), list(rz))

# ------------------------------------------------------------------
# RIGID 3D EXACT KINEMATIC GENERATOR
# ------------------------------------------------------------------
def generate_drone_vectors():
    lines = {
        'C_FUSE': [], 'C_BODY': [], 'C_PROP': [], 
        'C_SKID': [], 'C_GLASS': [], 'C_LIGHTS': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. BASEPLATE ENVELOPE (REFERENCE GRID)
    # ==============================================================================
    gx_range = np.linspace(-3.5, 3.5, 15) 
    for gx in gx_range:
        append_segmented(lines, 'C_GRID', np.full_like(gx_range, gx), gx_range, np.zeros_like(gx_range))
        append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gx), np.zeros_like(gx_range))

    # ==============================================================================
    # 2. CENTRAL FUSELAGE MATRIX (AERODYNAMIC HULL)
    # Length ~ 3.6m (X = -1.8 to 1.8)
    # ==============================================================================
    fuse_x = np.linspace(-1.8, 1.8, 20)
    t = np.linspace(0, 2*np.pi, 20)
    center_z = 0.5
    
    # Parabolic sweeping hull contour
    for x in fuse_x:
        # Elliptical radius tapering at ends
        r = 0.55 * np.sqrt(max(0, 1.0 - (x/1.8)**2))
        fx = np.full_like(t, x)
        fy = r * np.cos(t)
        # Flatten the belly slightly, arch the dorsal spine
        fz = center_z + r * np.sin(t) * (1.2 if np.mean(np.sin(t)) > 0 else 0.8)
        append_segmented(lines, 'C_FUSE', list(fx)+[fx[0]], list(fy)+[fy[0]], list(fz)+[fz[0]])
        
    for a in t[::2]:
        sx, sy, sz = [], [], []
        for x in fuse_x:
            r = 0.55 * np.sqrt(max(0, 1.0 - (x/1.8)**2))
            sx.append(x)
            sy.append(r * np.cos(a))
            sz.append(center_z + r * np.sin(a) * (1.2 if np.sin(a) > 0 else 0.8))
        append_segmented(lines, 'C_FUSE', sx, sy, sz)

    # GPS Antenna Dome (Top Spine)
    add_cylinder_surface(lines, 'C_PROP', -0.5, 0.0, center_z+0.5, 0.3, 0.08, 0.08, 'z', 3, 8)
    add_sphere(lines, 'C_PROP', -0.5, 0.0, center_z+0.8, 0.1)

    # ==============================================================================
    # 3. QUADROTOR DUCTED FAN ARRAYS & SUPPORT ARMS
    # ==============================================================================
    # X configuration offset
    duct_pos = [(1.3, 1.4), (1.3, -1.4), (-1.3, 1.4), (-1.3, -1.4)]
    r_in = 0.8
    r_out = 0.95
    h_duct = 0.35
    z_duct = center_z - 0.1

    for dx, dy in duct_pos:
        # Outer and Inner Ducted Shroud Walls
        add_cylinder_surface(lines, 'C_BODY', dx, dy, z_duct, h_duct, r_out, r_out, 'z', 4)
        add_cylinder_surface(lines, 'C_BODY', dx, dy, z_duct, h_duct, r_in, r_in, 'z', 4)
        
        # Bridging lips (Top and Bottom of Shrouds)
        dt = np.linspace(0, 2*np.pi, 24)
        for hz in [z_duct, z_duct + h_duct]:
            ix_in, iy_in = dx + r_in*np.cos(dt), dy + r_in*np.sin(dt)
            ix_out, iy_out = dx + r_out*np.cos(dt), dy + r_out*np.sin(dt)
            for i in range(len(dt)):
                append_segmented(lines, 'C_BODY', [ix_in[i], ix_out[i]], [iy_in[i], iy_out[i]], [hz, hz])
                
        # Heavy Structural Mounts (Fuselage to Ducts)
        # Vector points tracing from hull to duct perimeter
        arm_w = 0.25
        fx_anchor, fy_anchor = dx*0.5, dy*0.4 # Connection root at fuselage
        # Solid diagonal bracing bounds
        bx = [fx_anchor, dx, dx, fx_anchor, fx_anchor]
        by = [fy_anchor-arm_w, dy-arm_w, dy+arm_w, fy_anchor+arm_w, fy_anchor-arm_w]
        bz_top = [center_z+0.1, z_duct+h_duct, z_duct+h_duct, center_z+0.1, center_z+0.1]
        bz_bot = [center_z-0.1, z_duct, z_duct, center_z-0.1, center_z-0.1]
        
        append_segmented(lines, 'C_BODY', bx, by, bz_top)
        append_segmented(lines, 'C_BODY', bx, by, bz_bot)
        for i in range(4):
            append_segmented(lines, 'C_BODY', [bx[i], bx[i]], [by[i], by[i]], [bz_top[i], bz_bot[i]])

        # Internal Propulsion Hardware (Motors & Struts)
        m_z = z_duct + 0.15
        add_cylinder_surface(lines, 'C_PROP', dx, dy, z_duct, h_duct-0.05, 0.15, 0.15, 'z', 3, 12)
        # Transverse internal motor mounts (X cross)
        cx1 = dx + r_in * np.cos(np.pi/4); cy1 = dy + r_in * np.sin(np.pi/4)
        cx2 = dx - r_in * np.cos(np.pi/4); cy2 = dy - r_in * np.sin(np.pi/4)
        append_segmented(lines, 'C_PROP', [cx1, cx2], [cy1, cy2], [m_z, m_z])
        cx3 = dx + r_in * np.cos(3*np.pi/4); cy3 = dy + r_in * np.sin(3*np.pi/4)
        cx4 = dx - r_in * np.cos(3*np.pi/4); cy4 = dy - r_in * np.sin(3*np.pi/4)
        append_segmented(lines, 'C_PROP', [cx3, cx4], [cy3, cy4], [m_z, m_z])
        
        # Propeller Blades (Static geometric yield)
        pb = np.linspace(0.15, r_in-0.02, 5)
        for ang in [0, np.pi/2, np.pi, 3*np.pi/2]:
            append_segmented(lines, 'C_PROP', dx + pb*np.cos(ang), dy + pb*np.sin(ang), np.full_like(pb, m_z+0.05))

    # ==============================================================================
    # 4. OPTICAL SENSOR GIMBAL (Underslung Payload)
    # ==============================================================================
    gx, gy, gz = 1.3, 0.0, center_z - 0.4
    # Mounting bracket
    append_segmented(lines, 'C_GLASS', [gx-0.1, gx+0.1, gx+0.1, gx-0.1, gx-0.1], 
                     [-0.1, -0.1, 0.1, 0.1, -0.1], [center_z, center_z, center_z, center_z, center_z])
    append_segmented(lines, 'C_GLASS', [gx, gx], [0.0, 0.0], [center_z, gz+0.1])
    # Main Sensor Sphere
    add_sphere(lines, 'C_GLASS', gx, gy, gz, 0.25)
    # Forward Lens Tube
    add_cylinder_surface(lines, 'C_GLASS', gx, gy, gz-0.1, 0.4, 0.15, 0.18, 'x', 4, 12)

    # ==============================================================================
    # 5. LANDING SKIDS (Rigid Footprint)
    # ==============================================================================
    # Attaching dynamically to lower hull
    skid_z = 0.0 # Pavement contact
    sx_bounds = [-1.0, 1.2]
    sy_bounds = [-0.7, 0.7]

    for sign in [-1, 1]:
        # Heavy horizontal ground rails (Tubes running along X axis)
        add_cylinder_surface(lines, 'C_SKID', sx_bounds[0], sy_bounds[1]*sign, skid_z, sx_bounds[1]-sx_bounds[0], 0.06, 0.06, 'x', 4, 8)
        # Angled mounting struts connecting rail to body
        s_y = sy_bounds[1]*sign
        for x_mount in [-0.5, 0.7]:
            # Extrude from body center_z-0.3 outwards and downwards to rail
            b_x = x_mount; b_y = 0.25 * sign; b_z = center_z - 0.2
            append_segmented(lines, 'C_SKID', [b_x, b_x], [b_y, s_y], [b_z, skid_z+0.05])
            append_segmented(lines, 'C_SKID', [b_x-0.05, b_x-0.05], [b_y, s_y], [b_z, skid_z+0.05])
            append_segmented(lines, 'C_SKID', [b_x+0.05, b_x+0.05], [b_y, s_y], [b_z, skid_z+0.05])

    return lines

# ------------------------------------------------------------------
# PARALLEL GENERATOR STREAM (KINEMATIC TIMELINE TENSOR)
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_drone_vectors() # Computed once for true O(1) loop retrieval
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Central Basepoint: Mapping the structural centre of the drone
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.5 
        
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

    # Cinematic Rigid Map Boundary - Covers the ~5.0m bounding box uniformly
    cam_span = 3.6
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []

    # 1. PROCESS KINEMATIC VECTOR MATRIX
    for c_key, c_val in [('C_GRID', C_GRID), ('C_FUSE', C_FUSE), ('C_BODY', C_BODY), 
                         ('C_PROP', C_PROP), ('C_SKID', C_SKID), ('C_GLASS', C_GLASS), ('C_LIGHTS', C_LIGHTS)]:
        
        if c_key == 'C_GRID': lw, alpha = 0.8, 0.4
        elif c_key == 'C_FUSE': lw, alpha = 1.6, 1.0     
        elif c_key == 'C_BODY': lw, alpha = 1.3, 1.0      
        elif c_key == 'C_PROP': lw, alpha = 1.0, 1.0  
        elif c_key == 'C_SKID': lw, alpha = 2.0, 1.0   
        elif c_key == 'C_GLASS': lw, alpha = 1.6, 1.0   
        elif c_key == 'C_LIGHTS': lw, alpha = 2.5, 1.0   
        else: lw, alpha = 1.0, 1.0
            
        for xl, yl, zl in static_rig[c_key]:
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=25.0)
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

    ax.text(-cam_span*0.95, ui_t+1.0, "LG-449o // MACRO-ENGINEERING TENSOR: UNMANNED AEROSPACE", color=C_TEXT, fontsize=19, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t+0.3, "EXPLICIT TRUE-SCALE GEOMETRY // QUADROTOR MATRIX", color=C_GLASS, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b+1.0, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_FUSE, fontsize=17, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.5, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS SYNCHRONISATION)", color=C_TEXT, fontsize=17, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.1, "GEOMETRY YIELD   : DUCTED FAN SHROUDS / O(N) SKID TENSORS SECURED", color=C_BODY, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-449o: AEROSPACE DRONE MACRO-ENGINEERING TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
