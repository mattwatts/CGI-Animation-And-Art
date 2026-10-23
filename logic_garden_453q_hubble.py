"""
PROJECT: Logic Garden 453q (Exact Physical Construct // Hubble Space Telescope Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: HUBBLE, HST, TELESCOPE, NASA, GLB, WIREFRAME, KINEMATICS, PYTHON
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional 13.2m observatory scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: OTA Light Shield, Aft SSM Shroud, SA3 Solar Arrays, HGAs, Aperture Door.
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
OUT_DIR = "frames_453q_hubble"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Orbital Tracking Grid)

C_HULL      = '#94A3B8'          # Slate Aluminium (Forward Light Shield / Optical Telescope Assembly)
C_AFT       = '#334155'          # Heavy Slate (Support Systems Module / Aft Shroud Base)
C_SOLAR     = '#005599'          # Deep Marine (Third-Gen Rigid Photovoltaic Wings)
C_FOIL      = '#CA8A04'          # Kapton Gold (Handrails, Star Trackers, HGA Parabolic Dishes)
C_DOOR      = '#1E293B'          # Carbon Slate (Hinged Aperture Flap & Telemetry Booms)

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

def add_cone_frustum(lines_dict, col, cx, cy, cz, dz, r1, r2, axis='z', rings=4, t_count=16, reflect_y=False):
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
# SUPERSTRUCTURE BUILDERS (HUBBLE SPACE TELESCOPE)
# ------------------------------------------------------------------
def generate_hubble_static():
    lines = {
        'C_HULL': [], 'C_AFT': [], 'C_SOLAR': [],
        'C_FOIL': [], 'C_DOOR': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. ORBITAL TRACKING BASEPLATE (Simulation Space)
    # ==============================================================================
    # Executing the grid safely below the extreme structural boundaries
    Z_FLOOR = -6.0
    for r_p in [5.0, 10.0, 15.0]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-15.0, 15.0, 19)
    gy_range = np.linspace(-15.0, 15.0, 19)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. AFT SHROUD & SUPPORT SYSTEMS MODULE (SSM)
    # ==============================================================================
    # The wider base cylinder housing logic computers, momentum wheels, and main focal plane instruments
    R_AFT = 2.1
    Z_AFT_BOTTOM = -4.0
    Z_AFT_TOP = 0.0
    
    add_cylinder(lines, 'C_AFT', cx=0.0, cy=0.0, cz=Z_AFT_BOTTOM, length=(Z_AFT_TOP - Z_AFT_BOTTOM), radius=R_AFT, axis='z', rings=10, t_count=32, reflect_y=False)
    
    # Rounded End-Cap Taper (Aft Bulkhead closure)
    add_cone_frustum(lines, 'C_AFT', cx=0.0, cy=0.0, cz=Z_AFT_BOTTOM, dz=-0.6, r1=R_AFT, r2=1.0, axis='z', rings=4, t_count=32, reflect_y=False)

    # Equipment Array Circumferential Handrails (Kapton Gold geometry rings)
    for zh in [-1.0, -2.5]:
        add_cylinder(lines, 'C_FOIL', cx=0.0, cy=0.0, cz=zh-0.05, length=0.1, radius=R_AFT+0.05, axis='z', rings=2, t_count=32, reflect_y=False)

    # ==============================================================================
    # 3. FORWARD LIGHT SHIELD (OPTICAL TELESCOPE ASSEMBLY - OTA)
    # ==============================================================================
    # Narrows to a 3.0-metre diameter, extending 7.0 metres towards the target celestial object
    R_OTA = 1.5
    Z_OTA_TOP = 7.0
    
    # Sharp transitional lip collar at Z=0
    add_cylinder(lines, 'C_HULL', cx=0.0, cy=0.0, cz=0.0, length=0.2, radius=R_AFT, axis='z', rings=2, t_count=32, reflect_y=False)
    
    # Main Baffle Cylinder
    add_cylinder(lines, 'C_HULL', cx=0.0, cy=0.0, cz=0.2, length=(Z_OTA_TOP - 0.2), radius=R_OTA, axis='z', rings=14, t_count=32, reflect_y=False)

    # ==============================================================================
    # 4. TRANSVERSE SOLAR WING ARRAYS (SA3 RIGID MATRICES)
    # ==============================================================================
    # Symmetrically mounted to the central Equipment Bays spanning outward to Y=7.2m
    SAW_Z = -0.5
    SAW_WIDTH = 1.3 # 2.6m chord
    SAW_START = R_AFT + 0.5
    SAW_END = 7.5
    
    # Solar Array Drive Mechanism (SADM) Mast
    add_cylinder(lines, 'C_AFT', cx=0.0, cy=R_AFT, cz=SAW_Z, length=(SAW_START - R_AFT), radius=0.15, axis='y', rings=3, t_count=12, reflect_y=True)
    
    # Deep Marine Rigid Solar Panels
    add_quad_mesh(lines, 'C_SOLAR', 
                  (-SAW_WIDTH, SAW_START, SAW_Z), (-SAW_WIDTH, SAW_END, SAW_Z), 
                  (SAW_WIDTH, SAW_END, SAW_Z), (SAW_WIDTH, SAW_START, SAW_Z), 
                  u_steps=4, v_steps=12, reflect_y=True)
    # Underside thickness geometry
    add_quad_mesh(lines, 'C_SOLAR', 
                  (-SAW_WIDTH, SAW_START, SAW_Z-0.05), (-SAW_WIDTH, SAW_END, SAW_Z-0.05), 
                  (SAW_WIDTH, SAW_END, SAW_Z-0.05), (SAW_WIDTH, SAW_START, SAW_Z-0.05), 
                  u_steps=4, v_steps=12, reflect_y=True)

    # ==============================================================================
    # 5. HIGH GAIN ANTENNAS (HGA)
    # ==============================================================================
    # Twin telemetry dishes. Masts emerge angled aftwards and outwards from the Z = -2.5m mark
    HGA_ROOT_Z = -2.5
    HGA_TIP_Y = 3.5
    HGA_TIP_Z = -4.0
    
    # Mast Extrusion
    # From [0, R_AFT, HGA_ROOT_Z] to [0, HGA_TIP_Y, HGA_TIP_Z]
    append_segmented(lines, 'C_DOOR', [0.0, 0.0], [R_AFT, HGA_TIP_Y], [HGA_ROOT_Z, HGA_TIP_Z])
    append_segmented(lines, 'C_DOOR', [0.0, 0.0], [-R_AFT, -HGA_TIP_Y], [HGA_ROOT_Z, HGA_TIP_Z])
    
    # Tracking Dish (Parabolic frustum facing outwards down the +/- Y axis perfectly)
    add_cone_frustum(lines, 'C_FOIL', cx=0.0, cy=HGA_TIP_Y, cz=HGA_TIP_Z, dz=0.3, r1=0.1, r2=0.7, axis='y', rings=4, t_count=20, reflect_y=False)
    add_cone_frustum(lines, 'C_FOIL', cx=0.0, cy=-HGA_TIP_Y, cz=HGA_TIP_Z, dz=-0.3, r1=0.1, r2=0.7, axis='y', rings=4, t_count=20, reflect_y=False)

    # ==============================================================================
    # 6. OPERATIONAL APERTURE DOOR
    # ==============================================================================
    # Hinged exclusively on the -X edge at Z=7.0.
    # Angle is 75 degrees pitched open.
    ALPHA = np.radians(75)
    HINGE_X = -R_OTA
    HINGE_Z = Z_OTA_TOP
    
    # New geometric center after applying 75 degree kinematic tilt
    DOOR_CX = HINGE_X + R_OTA * np.cos(ALPHA)
    DOOR_CZ = HINGE_Z + R_OTA * np.sin(ALPHA)
    
    t_door = np.linspace(0, 2*np.pi, 32, endpoint=False)
    
    # Concentric door disc rings mapped perfectly across the angled plane
    for r in [0.5, 1.0, 1.5]:
        lx = r * np.cos(t_door)
        ly = r * np.sin(t_door)
        # Apply strict coordinate tilt locally
        wx = DOOR_CX + lx * np.cos(ALPHA)
        wy = ly
        wz = DOOR_CZ + lx * np.sin(ALPHA)
        # Bypassing symmetry reflecting explicitly because this flap is definitively asymmetrical globally
        append_segmented(lines, 'C_DOOR', list(wx)+[wx[0]], list(wy)+[wy[0]], list(wz)+[wz[0]])
        
    # Door structural spokes enforcing rigidity across the plane
    for th in np.linspace(0, 2*np.pi, 8, endpoint=False):
        lx_end, ly_end = 1.5 * np.cos(th), 1.5 * np.sin(th)
        wx_end = DOOR_CX + lx_end * np.cos(ALPHA)
        wy_end = ly_end
        wz_end = DOOR_CZ + lx_end * np.sin(ALPHA)
        append_segmented(lines, 'C_DOOR', [DOOR_CX, wx_end], [0.0, wy_end], [DOOR_CZ, wz_end])

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_hubble_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry explicitly midway up the primary OTA light shield
        cam_x, cam_y, cam_z = 0.0, 0.0, 1.5
        
        # Starts explicitly from 115-degrees (Dramatic aesthetic showcasing the deployed aperture door & rigid wings)
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
    # Anchor Centroid = Z=1.5m. Extents rigidly track to Z=-4.6m and Z=+8.5m (including door pitch). 
    # The extreme aerodynamic penalty occurs transversally, with wingspans reaching +/- 7.5m outward.
    # Setting cam_span strictly to 9.0 locks horizontal width symmetrically across an 18.0m geometrical span.
    # Vertical bounds output 9.0 * 1.777 = 15.99m half-height (total transparent window 31.9m).
    # Perfectly traps the extreme high-gain antennas (-4.0m Z) and towering aperture door safely inside the viewport.
    cam_span = 9.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_AFT',       C_AFT,       1.4, 1.0),
        ('C_HULL',      C_HULL,      1.2, 1.0),
        ('C_DOOR',      C_DOOR,      1.6, 1.0),
        ('C_FOIL',      C_FOIL,      1.5, 1.0),
        ('C_SOLAR',     C_SOLAR,     1.3, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to distinctly parse the difference between the aft SSM hull and the forward light shield width
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-453q // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // HUBBLE SPACE TELESCOPE (HST)", color=C_AFT, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_SOLAR, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: 4.2M SSM AFT SHROUD / OTA LIGHT SHIELD / KINEMATIC APERTURE DOOR", color=C_FOIL, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-453q: HUBBLE SPACE TELESCOPE TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
