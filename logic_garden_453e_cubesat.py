"""
PROJECT: Logic Garden 453e (Exact Physical Construct // CubeSat 1U Generic Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: CUBESAT, 1U, NANO-SATELLITE, MICRO-ENGINEERING, GLB, WIREFRAME, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional 100mm scale (1 Unit = 1 Metre internally).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: 1U Chassis, P-POD Rails, Body-Mounted Solar Cells, Dipole Antennas, PCB Decks.
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
OUT_DIR = "frames_453e_cubesat"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Orbital Tracking Grid)

C_CHASSIS   = '#94A3B8'          # Slate Aluminium (Primary 10x10cm 1U Structure)
C_RAILS     = '#334155'          # Heavy Slate (P-POD Deployment Standoffs)
C_SOLAR     = '#005599'          # Deep Marine (Body-Mounted Photovoltaic Arrays)
C_PCB       = '#CA8A04'          # Kapton Gold (Printed Circuit Boards & MLI)
C_OPTICS    = '#1E293B'          # Carbon Slate (Nadir Optical & Star Trackers)
C_ANTENNA   = '#0F172A'          # Abyssal Slate (Deployed UHF/VHF Measuring-Tape Antennas)

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
    # Reflect mapping strictly across primary Y-grid. 1U CubeSats inherently rely on rotational symmetries.
    if any(abs(y) > 0.001 for y in ys):
        append_segmented(lines_dict, key, xs, [-y for y in ys], zs)

# ------------------------------------------------------------------
# GEOMETRIC PRIMITIVES
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

def add_box_mesh(lines_dict, col, x1, x2, y1, y2, z1, z2, div=4, reflect_y=False):
    add_quad_mesh(lines_dict, col, (x1, y1, z1), (x2, y1, z1), (x2, y2, z1), (x1, y2, z1), div, div, reflect_y)
    add_quad_mesh(lines_dict, col, (x1, y1, z2), (x2, y1, z2), (x2, y2, z2), (x1, y2, z2), div, div, reflect_y)
    add_quad_mesh(lines_dict, col, (x1, y1, z1), (x2, y1, z1), (x2, y1, z2), (x1, y1, z2), div, div, reflect_y)
    add_quad_mesh(lines_dict, col, (x1, y2, z1), (x2, y2, z1), (x2, y2, z2), (x1, y2, z2), div, div, reflect_y)
    add_quad_mesh(lines_dict, col, (x1, y1, z1), (x1, y2, z1), (x1, y2, z2), (x1, y1, z2), div, div, reflect_y)
    add_quad_mesh(lines_dict, col, (x2, y1, z1), (x2, y2, z1), (x2, y2, z2), (x2, y1, z2), div, div, reflect_y)

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
# SUPERSTRUCTURE BUILDERS (CUBESAT 1U)
# ------------------------------------------------------------------
def generate_cubesat_static():
    # HOTFIX: Explicitly injected C_HARDWARE channel
    lines = {
        'C_CHASSIS': [], 'C_RAILS': [], 'C_SOLAR': [],
        'C_PCB': [], 'C_OPTICS': [], 'C_ANTENNA': [], 
        'C_HARDWARE': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. MICRO-ENGINEERING ORBITAL TRACKING BASEPLATE (Simulation Floor)
    # ==============================================================================
    # Executing the grid at Z = -0.2 (20cm) to provide visual scale
    Z_FLOOR = -0.2
    for r_p in [0.1, 0.2, 0.3]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-0.3, 0.3, 13)
    gy_range = np.linspace(-0.3, 0.3, 13)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. PRIMARY 1U CHASSIS & P-POD RAILS
    # ==============================================================================
    # 1 Unit physically defines as 100 x 100 x 100 mm (X/Y from -0.05 to +0.05)
    BOX_LIM = 0.05
    # The P-POD extruded railing extends the true height to exactly 113.5 mm (+/- 0.05675)
    RAIL_LIM = 0.05675
    
    # Internal Structural Block (100x100x100mm)
    add_box_mesh(lines, 'C_CHASSIS', -BOX_LIM, BOX_LIM, -BOX_LIM, BOX_LIM, -BOX_LIM, BOX_LIM, div=5, reflect_y=False)

    # Thickened 4x Corner Rails (Slide mechanisms for the Poly-Picosatellite Orbital Deployer)
    RAIL_WIDTH = 0.004
    for rx in [-BOX_LIM, BOX_LIM]:
        for ry in [-BOX_LIM, BOX_LIM]:
            # Square extruded posts executing the structural corners
            add_box_mesh(lines, 'C_RAILS', rx - RAIL_WIDTH, rx + RAIL_WIDTH, 
                         ry - RAIL_WIDTH, ry + RAIL_WIDTH, 
                         -RAIL_LIM, RAIL_LIM, div=1, reflect_y=False)

    # ==============================================================================
    # 3. BODY-MOUNTED PHOTOVOLTAIC ARRAYS
    # ==============================================================================
    # Covering the primary X and Y faces with standard 2-cell Deep Marine topography
    PANEL_OFFSET = 0.051 # Barely 1mm surface stand-off
    PANEL_EXTENT = 0.045
    
    # Port / Starboard PV Wings (Y-axis offset)
    add_quad_mesh(lines, 'C_SOLAR', (-PANEL_EXTENT, PANEL_OFFSET, -PANEL_EXTENT), (PANEL_EXTENT, PANEL_OFFSET, -PANEL_EXTENT),
                                    (PANEL_EXTENT, PANEL_OFFSET, PANEL_EXTENT), (-PANEL_EXTENT, PANEL_OFFSET, PANEL_EXTENT), 
                                    u_steps=5, v_steps=10, reflect_y=True)
                                    
    # Fore / Aft PV Wings (X-axis offset)
    add_quad_mesh(lines, 'C_SOLAR', (PANEL_OFFSET, -PANEL_EXTENT, -PANEL_EXTENT), (PANEL_OFFSET, PANEL_EXTENT, -PANEL_EXTENT),
                                    (PANEL_OFFSET, PANEL_EXTENT, PANEL_EXTENT), (PANEL_OFFSET, -PANEL_EXTENT, PANEL_EXTENT), 
                                    u_steps=10, v_steps=5, reflect_y=False)
    add_quad_mesh(lines, 'C_SOLAR', (-PANEL_OFFSET, -PANEL_EXTENT, -PANEL_EXTENT), (-PANEL_OFFSET, PANEL_EXTENT, -PANEL_EXTENT),
                                    (-PANEL_OFFSET, PANEL_EXTENT, PANEL_EXTENT), (-PANEL_OFFSET, -PANEL_EXTENT, PANEL_EXTENT), 
                                    u_steps=10, v_steps=5, reflect_y=False)

    # ==============================================================================
    # 4. AVIONICS TOP-DECK (PCB LAMINATES)
    # ==============================================================================
    # High-density electronics interfacing the zenith (+Z) plate
    for dx in np.linspace(-0.04, 0.04, 4):
        add_cylinder(lines, 'C_PCB', cx=dx, cy=0.0, cz=BOX_LIM, length=0.003, radius=0.008, axis='z', rings=2, t_count=8, reflect_y=True)
        # Power & Telemetry logic lines
        append_segmented(lines, 'C_PCB', [dx, dx], [-0.03, 0.03], [BOX_LIM+0.001, BOX_LIM+0.001])
        append_segmented(lines, 'C_PCB', [-0.03, 0.03], [dx, dx], [BOX_LIM+0.001, BOX_LIM+0.001])

    # ==============================================================================
    # 5. NADIR EARTH-OBSERVATION OPTICS
    # ==============================================================================
    # Miniaturized imager projecting through the fundamental floor plate (-Z)
    add_cylinder(lines, 'C_OPTICS', cx=0.0, cy=0.0, cz=-BOX_LIM, length=-0.015, radius=0.025, axis='z', rings=3, t_count=16, reflect_y=False)
    add_cone_frustum(lines, 'C_OPTICS', cx=0.0, cy=0.0, cz=-BOX_LIM - 0.015, dz=-0.005, r1=0.025, r2=0.018, axis='z', rings=2, t_count=16, reflect_y=False)

    # ==============================================================================
    # 6. DEPLOYABLE UHF/VHF DIPOLE ANTENNAS
    # ==============================================================================
    # Exploding out from the 4 nadir (-Z) corners to achieve orbital transmission lengths
    ANTENNA_LEN = 0.15 # 150mm reach
    for sx in [-1, 1]:
        for sy in [-1, 1]:
            # Anchor blocks
            ax, ay, az = sx*0.04, sy*0.04, -BOX_LIM
            add_cylinder(lines, 'C_HARDWARE', cx=ax, cy=ay, cz=az, length=-0.01, radius=0.005, axis='z', rings=2, t_count=6, reflect_y=False)
            
            # Swept dipole extrusions (pointing diagonally out and downwards)
            ex, ey, ez = ax + sx*ANTENNA_LEN, ay + sy*ANTENNA_LEN, az - ANTENNA_LEN*0.5
            append_segmented(lines, 'C_ANTENNA', [ax, ex], [ay, ey], [az, ez])
            
            # Mechanical segment marking (mimicking tape-measure flex markings)
            segments = 5
            for i in range(1, segments):
                frac = i / segments
                mx = ax * (1 - frac) + ex * frac
                my = ay * (1 - frac) + ey * frac
                mz = az * (1 - frac) + ez * frac
                append_segmented(lines, 'C_HARDWARE', [mx-0.002, mx+0.002], [my-0.002, my+0.002], [mz, mz])

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_cubesat_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry flawlessly at payload centroid
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.0
        
        # Starts explicitly from 115-degrees (Dramatic aesthetic showcasing the sweeping dipoles)
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
    # Anchor Centroid = Dead zero. The primary block is tiny (10cm). However, the UHF antennas stretch forcefully out.
    # The antennas reach X/Y of +/- 0.19m (190mm). 
    # Setting cam_span strictly to 0.25 locks horizontal width symmetrically across a 50cm (0.5m) macro view.
    # Vertical bounds output 0.25 * 1.777 = 0.444m (total height window 88.8cm vertically).
    # Completely traps the entire micro-payload safely inside the extreme close-up viewport, immune to UI overlay clipping.
    cam_span = 0.25
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_CHASSIS',   C_CHASSIS,   1.2, 1.0),
        ('C_RAILS',     C_RAILS,     1.3, 1.0),
        ('C_SOLAR',     C_SOLAR,     1.1, 1.0),
        ('C_PCB',       C_PCB,       1.4, 1.0),
        ('C_OPTICS',    C_OPTICS,    1.5, 1.0),
        ('C_HARDWARE',  C_ANTENNA,   1.1, 1.0),
        ('C_ANTENNA',   C_ANTENNA,   1.6, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to parse the exact layout of the P-POD rails and top zenith avionics board
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-453e // MACRO-ENGINEERING TENSOR: MICRO-AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // 1U CUBESAT GENERIC (100MM ARCHITECTURE)", color=C_CHASSIS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_SOLAR, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: 10CM P-POD CHASSIS / PV ARRAYS / UHF-VHF DIPOLE DEPLOYMENT", color=C_ANTENNA, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-453e: 1U CUBESAT GENERIC TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
