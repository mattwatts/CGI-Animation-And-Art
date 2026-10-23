"""
PROJECT: Logic Garden 453o (Exact Physical Construct // Habitat Demonstration Unit Part 2)
FORMAT: YouTube Shorts (1080x1920)
METADATA: HDU, HABITAT, NASA, SOLAR DEPLOYMENT, SPACECRAFT, GLB, WIREFRAME, PYTHON
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional massive-scale extended architecture.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Rigid Core, Inflatable Loft, Extended SAWs, Docked Payload, HGA Mast.
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
OUT_DIR = "frames_453o_hdu2"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Extraterrestrial Tracking Grid)

C_CORE      = '#334155'          # Heavy Slate (Primary Rigid 5m Cylindrical Hull & Hubs)
C_LOFT      = '#94A3B8'          # Slate Aluminium (Expandable X-Hab Loft Module)
C_TRUSS     = '#1E293B'          # Carbon Slate (HGA Mast & Solar Array Booms)
C_DOCKED    = '#CA8A04'          # Kapton Gold (Docked Logistics / Rover Payload Module)
C_SOLAR     = '#005599'          # Deep Marine (Deployed 12m Transverse Photovoltaic Wings)

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
# SUPERSTRUCTURE BUILDERS (HABITAT DEMONSTRATION UNIT - PART 2)
# ------------------------------------------------------------------
def generate_hdu2_static():
    lines = {
        'C_CORE': [], 'C_LOFT': [], 'C_TRUSS': [],
        'C_DOCKED': [], 'C_SOLAR': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. PLANETARY TRACKING BASEPLATE (Simulation Surface)
    # ==============================================================================
    # Extends substantially to support visual acquisition of the immense solar wings
    Z_FLOOR = -1.0
    for r_p in [6.0, 12.0, 18.0]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-18.0, 18.0, 19)
    gy_range = np.linspace(-18.0, 18.0, 19)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. RIGID CORE HULL & X-HAB LOFT (The Anchor module)
    # ==============================================================================
    CORE_R = 2.5
    CORE_H = 3.0
    # Primary Substrate Hull
    add_cylinder(lines, 'C_CORE', cx=0.0, cy=0.0, cz=0.0, length=CORE_H, radius=CORE_R, axis='z', rings=8, t_count=32, reflect_y=False)
    
    # Internal strengthening ribs
    for z_rib in np.linspace(0.5, 2.5, 3):
        add_cylinder(lines, 'C_CORE', cx=0.0, cy=0.0, cz=z_rib, length=0.05, radius=CORE_R+0.05, axis='z', rings=2, t_count=32, reflect_y=False)

    # Inflatable Loft expansion (Ascends from deck Z=3.0 to Z=5.7m)
    add_cone_frustum(lines, 'C_LOFT', cx=0.0, cy=0.0, cz=3.0, dz=1.0, r1=CORE_R, r2=2.6, axis='z', rings=4, t_count=32, reflect_y=False)
    add_cone_frustum(lines, 'C_LOFT', cx=0.0, cy=0.0, cz=4.0, dz=1.5, r1=2.6, r2=1.5, axis='z', rings=6, t_count=32, reflect_y=False)
    add_cylinder(lines, 'C_LOFT', cx=0.0, cy=0.0, cz=5.5, length=0.2, radius=1.5, axis='z', rings=2, t_count=16, reflect_y=False)

    # ==============================================================================
    # 3. TERRESTRIAL LANDING KINEMATICS
    # ==============================================================================
    # Integrated structural legs distributing module weight to the regolith
    for ang in [45, 135, 225, 315]:
        rad_a = np.radians(ang)
        r_inner, r_outer = CORE_R, 4.0
        z_root, z_base = 0.5, Z_FLOOR
        sx_1, sy_1 = r_inner * np.cos(rad_a), r_inner * np.sin(rad_a)
        sx_2, sy_2 = r_outer * np.cos(rad_a), r_outer * np.sin(rad_a)
        
        append_segmented(lines, 'C_DOCKED', [sx_1, sx_2], [sy_1, sy_2], [z_root, z_base])
        append_segmented(lines, 'C_DOCKED', [sx_1, sx_2], [sy_1, sy_2], [z_root+0.2, z_base+0.2])
        add_cylinder(lines, 'C_DOCKED', cx=sx_2, cy=sy_2, cz=z_base, length=0.15, radius=0.5, axis='z', rings=2, t_count=16, reflect_y=False)

    # ==============================================================================
    # 4. TRANVERSE SOLAR ARRAY WINGS (DEEP SPACE / MULTI-MONTH UPGRADE)
    # ==============================================================================
    # Booms extend deeply into the lateral tracking geometry
    SAW_Z = 3.5
    SAW_LENGTH = 11.5   # Extends out to Y=12.0 from central root
    SAW_WIDTH = 2.0     # 4.0m span (+X/-X)
    
    # Port / Starboard Carbon Trusses
    add_cylinder(lines, 'C_TRUSS', cx=0.0, cy=CORE_R, cz=SAW_Z, length=(SAW_LENGTH - CORE_R), radius=0.15, axis='y', rings=4, t_count=8, reflect_y=True)
    
    # Dense Photovoltaic Solar Quadrants
    # Forced symmetry replicates the massive panels flawlessly
    add_quad_mesh(lines, 'C_SOLAR', 
                  (-SAW_WIDTH, 4.0, SAW_Z), (-SAW_WIDTH, SAW_LENGTH, SAW_Z), 
                  (SAW_WIDTH, SAW_LENGTH, SAW_Z), (SAW_WIDTH, 4.0, SAW_Z), 
                  u_steps=6, v_steps=15, reflect_y=True)
    add_quad_mesh(lines, 'C_SOLAR', 
                  (-SAW_WIDTH, 4.0, SAW_Z+0.05), (-SAW_WIDTH, SAW_LENGTH, SAW_Z+0.05), 
                  (SAW_WIDTH, SAW_LENGTH, SAW_Z+0.05), (SAW_WIDTH, 4.0, SAW_Z+0.05), 
                  u_steps=6, v_steps=15, reflect_y=True)

    # ==============================================================================
    # 5. DOCKED LOGISTICS PAYLOAD (THE MULTI-MISSION ORBITAL INTERFACE)
    # ==============================================================================
    # Hard-docked to the forward airlock, calculating the volumetric extension to +X
    AIRLOCK_X_START = CORE_R
    AIRLOCK_X_END = 4.0
    
    # Root Airlock Tube
    add_cylinder(lines, 'C_CORE', cx=AIRLOCK_X_START, cy=0.0, cz=1.0, length=(AIRLOCK_X_END - AIRLOCK_X_START), radius=1.2, axis='x', rings=3, t_count=20, reflect_y=False)
    
    # Docked Logistics Module Architecture
    DOCK_X_END = 8.5
    add_cylinder(lines, 'C_DOCKED', cx=AIRLOCK_X_END, cy=0.0, cz=1.0, length=(DOCK_X_END - AIRLOCK_X_END), radius=1.5, axis='x', rings=8, t_count=24, reflect_y=False)
    add_cone_frustum(lines, 'C_DOCKED', cx=DOCK_X_END, cy=0.0, cz=1.0, dz=0.4, r1=1.5, r2=0.8, axis='x', rings=3, t_count=20, reflect_y=False)

    # Twin Rear-Entry EVA Suit Ports (Aft Bulkhead Array)
    for y_offset in [-0.8, 0.8]:
        add_cylinder(lines, 'C_CORE', cx=-CORE_R, cy=y_offset, cz=1.2, length=-0.6, radius=0.45, axis='x', rings=3, t_count=16, reflect_y=False)

    # ==============================================================================
    # 6. HIGH-GAIN ANTENNA (HGA) DEEP SPACE COMMUNICATIONS MAST
    # ==============================================================================
    # Mounted clear of the inflatable boundary at Z = 5.7m, extending up to Z=7.5m
    add_cylinder(lines, 'C_TRUSS', cx=-1.2, cy=0.0, cz=5.0, length=2.5, radius=0.1, axis='z', rings=2, t_count=8, reflect_y=False)
    
    # 1.5m Parabolic Tracking Frustum (Pitched forward dynamically)
    add_cone_frustum(lines, 'C_TRUSS', cx=-1.2, cy=0.0, cz=7.5, dz=0.4, r1=0.2, r2=0.8, axis='y', rings=3, t_count=16, reflect_y=False)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_hdu2_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Centroid mathematically balanced above the hub
        cam_x, cam_y, cam_z = 0.0, 0.0, 2.0
        
        # Starts explicitly from 115-degrees (Dramatic aesthetic exposing the massive arrays and docked module)
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
    # Anchor Centroid = Z=2.0m. Extents track outwards dynamically. Max radius is the solar span (Y=+/-12.0m) and the docked payload (X=8.9m).
    # Setting cam_span rigorously to 15.5 locks horizontal width symmetrically across a 31.0m geometrical span.
    # Vertical bounds output 15.5 * 1.777 = 27.54m half-height (total transparent window 55.0m).
    # Bounds reliably clear the massive extended 12m wings and the 7.5m HGA mast effortlessly.
    # Entire complex is physically trapped inside the unoccluded viewing volume.
    cam_span = 15.5
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_TRUSS',     C_TRUSS,     1.3, 1.0),
        ('C_CORE',      C_CORE,      1.2, 1.0),
        ('C_LOFT',      C_LOFT,      1.1, 0.9),
        ('C_DOCKED',    C_DOCKED,    1.4, 1.0),
        ('C_SOLAR',     C_SOLAR,     1.6, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to distinctly parse the expanded photovoltaic footprint and docked logistics intersection
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-453o // MACRO-ENGINEERING TENSOR: PLANETARY KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // HABITAT DEMONSTRATION UNIT (EXTENDED ARRAYS)", color=C_CORE, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_SOLAR, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: 24.0m DEPLOYED SAWS / DOCKED LOGISTICS PAYLOAD / HGA TELEMETRY MAST", color=C_DOCKED, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-453o: HDU EXTENDED DEPLOYMENT TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Space Architecture Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
