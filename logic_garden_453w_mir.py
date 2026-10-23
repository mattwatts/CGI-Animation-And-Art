"""
PROJECT: Logic Garden 453w (Exact Physical Construct // Mir Space Station Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: MIR, SPACE STATION, ROSCOSMOS, SOVIET, GLB, WIREFRAME, PYTHON
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional 34m macro-orbital scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: DOS-7 Core, Transfer Node, Kvant-1, Kvant-2, Kristall, Spektr, Priroda.
- Procedural Topography: High-density mesh mirroring asymmetrical hardware constraints and solar arrays.
- Hotfix Integration: Strict np.full_like() propagation inside geometric primitives preventing Scalar Faults.
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
OUT_DIR = "frames_453w_mir"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Orbital Tracking Grid)

C_CORE      = '#334155'          # Heavy Slate (DOS-7 Core Block & Kvant-1)
C_MODULE    = '#94A3B8'          # Slate Aluminium (Kvant-2, Kristall, Spektr, Priroda)
C_SOYUZ     = '#CA8A04'          # Kapton Gold (Soyuz/Progress Orbital Ferry Vehicles)
C_SOLAR     = '#005599'          # Deep Marine (Photovoltaic Tracking Solar Wings)
C_TRUSS     = '#1E293B'          # Carbon Slate (Transfer Hub Nodes & Sofora Mast)

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
# GEOMETRIC PRIMITIVES (HOTFIXED SCALAR ITERATION FAULTS)
# ------------------------------------------------------------------
def add_quad_mesh(lines_dict, col, p1, p2, p3, p4, u_steps=4, v_steps=4, reflect_y=False):
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
        if axis == 'x':  sx, sy, sz = cx + steps, np.full_like(steps, cy + radius*np.cos(a)), np.full_like(steps, cz + radius*np.sin(a))
        elif axis == 'y':sx, sy, sz = np.full_like(steps, cx + radius*np.cos(a)), cy + steps, np.full_like(steps, cz + radius*np.sin(a))
        else:            sx, sy, sz = np.full_like(steps, cx + radius*np.cos(a)), np.full_like(steps, cy + radius*np.sin(a)), cz + steps
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
# SUPERSTRUCTURE BUILDERS (MIR SPACE STATION)
# ------------------------------------------------------------------
def generate_mir_static():
    lines = {
        'C_CORE': [], 'C_MODULE': [], 'C_SOYUZ': [],
        'C_SOLAR': [], 'C_TRUSS': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. ORBITAL TRACKING BASEPLATE (Simulation Space)
    # ==============================================================================
    Z_FLOOR = -18.0
    for r_p in [10.0, 20.0, 30.0]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', -9.0 + r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-35.0, 15.0, 25)
    gy_range = np.linspace(-25.0, 25.0, 25)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. THE FORWARD TRANSFER NODE
    # ==============================================================================
    # The iconic spherical junction natively built via dense mutually penetrating cylinders at 0,0,0
    R_NODE = 1.3
    # Interlocking matrix generates perfect orbital docking hull topology
    add_cylinder(lines, 'C_TRUSS', cx=-R_NODE, cy=0.0, cz=0.0, length=R_NODE*2, radius=R_NODE, axis='x', rings=5, t_count=24)
    add_cylinder(lines, 'C_TRUSS', cx=0.0, cy=-R_NODE, cz=0.0, length=R_NODE*2, radius=R_NODE, axis='y', rings=5, t_count=24)
    add_cylinder(lines, 'C_TRUSS', cx=0.0, cy=0.0, cz=-R_NODE, length=R_NODE*2, radius=R_NODE, axis='z', rings=5, t_count=24)

    # ==============================================================================
    # 3. DOS-7 CORE BLOCK & KVANT-1
    # ==============================================================================
    # Narrow forward access tunnel
    add_cylinder(lines, 'C_CORE', cx=-3.0, cy=0.0, cz=0.0, length=1.7, radius=1.1, axis='x', rings=3, t_count=20)
    # Tapering frustum transition
    add_cone_frustum(lines, 'C_CORE', cx=-3.0, cy=0.0, cz=0.0, dz=-1.5, r1=1.1, r2=2.1, axis='x', rings=3, t_count=20)
    # Massive 4.2-metre diameter primary operational compartment
    add_cylinder(lines, 'C_CORE', cx=-11.0, cy=0.0, cz=0.0, length=6.5, radius=2.1, axis='x', rings=8, t_count=24)
    # Aft propulsion compartment taper
    add_cone_frustum(lines, 'C_CORE', cx=-11.0, cy=0.0, cz=0.0, dz=-2.0, r1=2.1, r2=1.5, axis='x', rings=3, t_count=20)
    
    # Kvant-1 Astrophysics Module (Bolted directly to the aft Core port)
    add_cylinder(lines, 'C_CORE', cx=-18.0, cy=0.0, cz=0.0, length=5.0, radius=2.05, axis='x', rings=6, t_count=24)
    
    # Sofora Thruster Mast (Erected drastically outwards from Kvant-1 towards +Z)
    add_cylinder(lines, 'C_TRUSS', cx=-15.0, cy=0.0, cz=2.05, length=14.0, radius=0.2, axis='z', rings=4, t_count=8)

    # ==============================================================================
    # 4. RADIAL LABORATORY MODULES 
    # ==============================================================================
    # Expanding sequentially outwards from the primary docking node hub to 12m length
    R_MOD = 2.1
    # Kvant-2 (+Y axis)
    add_cylinder(lines, 'C_MODULE', cx=0.0, cy=1.3, cz=0.0, length=10.0, radius=R_MOD, axis='y', rings=8, t_count=20)
    # Kristall (-Y axis)
    add_cylinder(lines, 'C_MODULE', cx=0.0, cy=-11.3, cz=0.0, length=10.0, radius=R_MOD, axis='y', rings=8, t_count=20)
    # Spektr (+Z axis)
    add_cylinder(lines, 'C_MODULE', cx=0.0, cy=0.0, cz=1.3, length=10.0, radius=R_MOD, axis='z', rings=8, t_count=20)
    # Priroda (-Z axis)
    add_cylinder(lines, 'C_MODULE', cx=0.0, cy=0.0, cz=-11.3, length=10.0, radius=R_MOD, axis='z', rings=8, t_count=20)

    # ==============================================================================
    # 5. SOYUZ / PROGRESS ORBITAL FERRY VEHICLES 
    # ==============================================================================
    def add_soyuz(cx_root, axis_dir):
        # Maps the 3-stage Soyuz dynamically depending on the docking port vector (+X forward, -X aft)
        mult = 1.0 if axis_dir == 'pos' else -1.0
        # Orbital Module (Spherical/ovoid)
        add_cylinder(lines, 'C_SOYUZ', cx=cx_root, cy=0.0, cz=0.0, length=2.2*mult, radius=1.0, axis='x', rings=4, t_count=16)
        # Descent Module (Bell shaped taper)
        add_cone_frustum(lines, 'C_SOYUZ', cx=cx_root + 2.2*mult, cy=0.0, cz=0.0, dz=1.8*mult, r1=1.0, r2=1.3, axis='x', rings=3, t_count=16)
        # Service/Propulsion Module (Cylindrical with arrays)
        add_cylinder(lines, 'C_SOYUZ', cx=cx_root + 4.0*mult, cy=0.0, cz=0.0, length=2.5*mult, radius=1.3, axis='x', rings=4, t_count=16)
        # Soyuz lateral tracking arrays
        add_quad_mesh(lines, 'C_SOLAR', 
                      (cx_root + 4.5*mult, 1.3, -0.2), (cx_root + 6.0*mult, 1.3, -0.2), 
                      (cx_root + 6.0*mult, 5.0, -0.2), (cx_root + 4.5*mult, 5.0, -0.2), 
                      u_steps=2, v_steps=6, reflect_y=True)

    # Forward Transport (Docked to the node)
    add_soyuz(1.3, 'pos')
    # Aft Transport (Docked to Kvant-1)
    add_soyuz(-18.0, 'neg')

    # ==============================================================================
    # 6. PHOTOVOLTAIC TRACKING WINGS (SOLAR ARRAYS)
    # ==============================================================================
    # Core Module Primary Arrays (Extending directly outward along +/- Z)
    add_quad_mesh(lines, 'C_SOLAR', (-9.5, -0.2, 2.5), (-6.5, -0.2, 2.5), (-6.5, -0.2, 13.0), (-9.5, -0.2, 13.0), u_steps=3, v_steps=12, reflect_y=False)
    add_quad_mesh(lines, 'C_SOLAR', (-9.5, -0.2, -13.0), (-6.5, -0.2, -13.0), (-6.5, -0.2, -2.5), (-9.5, -0.2, -2.5), u_steps=3, v_steps=12, reflect_y=False)

    # Kvant-1 Power Arrays (Massive arrays spanning the Y-axis)
    add_quad_mesh(lines, 'C_SOLAR', (-16.0, 2.5, -0.2), (-14.0, 2.5, -0.2), (-14.0, 16.0, -0.2), (-16.0, 16.0, -0.2), u_steps=3, v_steps=12, reflect_y=True)

    # Kvant-2 Arrays (Tracking outwards along Z)
    add_quad_mesh(lines, 'C_SOLAR', (-1.5, 7.0, 2.5), (1.5, 7.0, 2.5), (1.5, 7.0, 12.0), (-1.5, 7.0, 12.0), u_steps=3, v_steps=10, reflect_y=False)
    add_quad_mesh(lines, 'C_SOLAR', (-1.5, 7.0, -12.0), (1.5, 7.0, -12.0), (1.5, 7.0, -2.5), (-1.5, 7.0, -2.5), u_steps=3, v_steps=10, reflect_y=False)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_mir_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry precisely midway down the DOS-7 Base Block
        cam_x, cam_y, cam_z = -9.0, 0.0, 0.0
        
        # Starts explicitly from 115-degrees (Dramatic aesthetic exposing the massive multi-module expanse natively)
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
    # Anchor Centroid = X=-9.0m. Extents track outwards dynamically. Max radius includes Soyuz at +8.0m and -25.0m (Distance 17m).
    # Lateral modules (Kvant-2, Kristall) extend to +/- 12m. Sofora Mast extends Z=+16m. Kvant-1 Solar Wings extend Y=+/-16.0m.
    # Setting cam_span strictly to 26.0 locks horizontal width symmetrically across a massive 52.0m geometrical span.
    # Vertical bounds output 26.0 * 1.777 = 46.2m half-height (total transparent window 92.4m).
    # Bounds reliably clear the extreme radial solar arrays and 14m thrust masts effortlessly.
    cam_span = 26.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_CORE',      C_CORE,      1.4, 1.0),
        ('C_MODULE',    C_MODULE,    1.3, 1.0),
        ('C_TRUSS',     C_TRUSS,     1.2, 1.0),
        ('C_SOYUZ',     C_SOYUZ,     1.3, 1.0),
        ('C_SOLAR',     C_SOLAR,     1.5, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to distinctly parse the difference between flat planar solar arrays and cylindrical hull volumes
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-453w // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // MIR SPACE STATION MATRIX", color=C_CORE, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_MODULE, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: DOS-7 CORE / MULTI-AXIS NODE / KVANT & RADIAL LABS / ORBITAL FERRIES", color=C_SOYUZ, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-453w: MIR SPACE STATION TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
