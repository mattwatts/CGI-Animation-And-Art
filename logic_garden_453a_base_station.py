"""
PROJECT: Logic Garden 453a (Exact Physical Construct // Planetary Base Station Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: BASE STATION, OUTPOST, LUNAR, MARS, GLB, WIREFRAME, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional modular aerospace scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Central Command Hub, Radian Corridors, Habitat Cylinders, PV Arrays, HGA Dish.
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
OUT_DIR = "frames_453a_base_station"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Planetary Regolith Surface Grid)

C_HAB       = '#334155'          # Heavy Slate (Primary Pressure Vessels & Domes)
C_AIRLOCK   = '#1E293B'          # Carbon Slate (Corridors, Airlocks & Decking)
C_SOLAR     = '#005599'          # Deep Marine (Photovoltaic Tracking Wings)
C_DISH      = '#CA8A04'          # Kapton Gold (High-Gain Antenna Parabola)
C_LEGS      = '#0F172A'          # Abyssal Slate (Structural Landing Struts & Footpads)

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
def add_quad_mesh(lines_dict, col, p1, p2, p3, p4, u_steps=4, v_steps=4):
    p1, p2, p3, p4 = map(np.array, (p1, p2, p3, p4))
    for i in range(v_steps + 1):
        v = i / v_steps
        start = p1 * (1-v) + p4 * v
        end   = p2 * (1-v) + p3 * v
        pts = [start * (1-u) + end * u for u in np.linspace(0, 1, u_steps+1)]
        append_segmented(lines_dict, col, [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts])
        if any(abs(p[1]) > 0.001 for p in pts):
            append_segmented(lines_dict, col, [p[0] for p in pts], [-p[1] for p in pts], [p[2] for p in pts])
    for i in range(u_steps + 1):
        u = i / u_steps
        start = p1 * (1-u) + p2 * u
        end   = p4 * (1-u) + p3 * u
        pts = [start * (1-v) + end * v for v in np.linspace(0, 1, v_steps+1)]
        append_segmented(lines_dict, col, [p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts])
        if any(abs(p[1]) > 0.001 for p in pts):
            append_segmented(lines_dict, col, [p[0] for p in pts], [-p[1] for p in pts], [p[2] for p in pts])

def add_box_mesh(lines_dict, col, x1, x2, y1, y2, z1, z2, div=4):
    add_quad_mesh(lines_dict, col, (x1, y1, z1), (x2, y1, z1), (x2, y2, z1), (x1, y2, z1), div, div)
    add_quad_mesh(lines_dict, col, (x1, y1, z2), (x2, y1, z2), (x2, y2, z2), (x1, y2, z2), div, div)
    add_quad_mesh(lines_dict, col, (x1, y1, z1), (x2, y1, z1), (x2, y1, z2), (x1, y1, z2), div, div)
    add_quad_mesh(lines_dict, col, (x1, y2, z1), (x2, y2, z1), (x2, y2, z2), (x1, y2, z2), div, div)
    add_quad_mesh(lines_dict, col, (x1, y1, z1), (x1, y2, z1), (x1, y2, z2), (x1, y1, z2), div, div)
    add_quad_mesh(lines_dict, col, (x2, y1, z1), (x2, y2, z1), (x2, y2, z2), (x2, y1, z2), div, div)

def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='z', rings=4, t_count=16):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, length, rings)
    for s in steps:
        if axis == 'x':  ix, iy, iz = np.full_like(t, cx + s), cy + radius*np.cos(t), np.full_like(t, cz + radius*np.sin(t)) if cz == 0 else cz + radius*np.sin(t)
        elif axis == 'y':ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + s), np.full_like(t, cz + radius*np.sin(t)) if cz == 0 else cz + radius*np.sin(t)
        else:            ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), np.full_like(t, cz + s)
        append_sym(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        if axis == 'x':  sx, sy, sz = cx + steps, [cy + radius*np.cos(a)]*rings, [cz + radius*np.sin(a)]*rings
        elif axis == 'y':sx, sy, sz = [cx + radius*np.cos(a)]*rings, cy + steps, [cz + radius*np.sin(a)]*rings
        else:            sx, sy, sz = [cx + radius*np.cos(a)]*rings, [cy + radius*np.sin(a)]*rings, cz + steps
        append_sym(lines_dict, col, sx, sy, sz)

def add_ellipsoid(lines_dict, col, cx, cy, cz, rx, ry, rz, rings=8, t_count=16, half=None):
    if half == 'pos_x': theta = np.linspace(-np.pi/2, np.pi/2, rings); phi = np.linspace(-np.pi/2, np.pi/2, rings)
    elif half == 'neg_x': theta = np.linspace(-np.pi/2, np.pi/2, rings); phi = np.linspace(np.pi/2, 3*np.pi/2, rings)
    elif half == 'pos_z': theta = np.linspace(0, np.pi/2, rings); phi = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    else: theta = np.linspace(-np.pi/2, np.pi/2, rings); phi = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    
    for th in theta:
        xs = cx + rx * np.cos(th) * np.cos(phi)
        ys = cy + ry * np.cos(th) * np.sin(phi)
        zs = cz + rz * np.sin(th) * np.ones_like(phi)
        append_sym(lines_dict, col, list(xs)+[xs[0]] if half is None or half=='pos_z' else list(xs), list(ys)+[ys[0]] if half is None or half=='pos_z' else list(ys), list(zs)+[zs[0]] if half is None or half=='pos_z' else list(zs))
    for ph in phi:
        xs = cx + rx * np.cos(theta) * np.cos(ph)
        ys = cy + ry * np.cos(theta) * np.sin(ph)
        zs = cz + rz * np.sin(theta)
        append_sym(lines_dict, col, xs, ys, zs)

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (PLANETARY BASE STATION)
# ------------------------------------------------------------------
def generate_base_station_static():
    lines = {
        'C_HAB': [], 'C_AIRLOCK': [], 'C_SOLAR': [],
        'C_DISH': [], 'C_LEGS': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. PLANETARY REGOLITH TRACKING BASEPLATE (1 Unit = 1 Metre)
    # ==============================================================================
    Z_FLOOR = 0.0
    for r_p in [6.0, 12.0, 18.0]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-18.0, 18.0, 25)
    gy_range = np.linspace(-18.0, 18.0, 25)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. CENTRAL COMMAND HUB
    # ==============================================================================
    HUB_R = 3.5
    HUB_Z_BOT = 1.5
    HUB_Z_TOP = 8.0
    
    # Primary cylindrical superstructure
    add_cylinder(lines, 'C_HAB', cx=0.0, cy=0.0, cz=HUB_Z_BOT, length=(HUB_Z_TOP - HUB_Z_BOT), radius=HUB_R, axis='z', rings=8, t_count=24)
    # Ellipsoidal Pressure Dome
    add_ellipsoid(lines, 'C_HAB', cx=0.0, cy=0.0, cz=HUB_Z_TOP, rx=HUB_R, ry=HUB_R, rz=2.0, rings=6, t_count=24, half='pos_z')
    
    # Heavy Structural Interstage Rings
    add_cylinder(lines, 'C_AIRLOCK', cx=0.0, cy=0.0, cz=HUB_Z_BOT, length=1.0, radius=HUB_R+0.1, axis='z', rings=2, t_count=24)

    # ==============================================================================
    # 3. PORT & STARBOARD HABITAT MODULES (Y-Axis Symmetry)
    # ==============================================================================
    HAB_CX = 0.0
    HAB_CY = 8.5
    HAB_CZ = 4.0
    HAB_R = 2.5
    HAB_L = 10.0 # Length spans X=-5.0 to X=5.0
    
    # Connecting Corridors from Hub to Habitat Cylinders
    # Appending exactly at Y=3.5 out to Y=6.0
    add_cylinder(lines, 'C_AIRLOCK', cx=0.0, cy=HUB_R, cz=HAB_CZ, length=(HAB_CY - HAB_R), radius=1.2, axis='y', rings=4, t_count=12)
    
    # Main Horizontal Living Modules (Port/Starboard Native Mirrors)
    add_cylinder(lines, 'C_HAB', cx=-HAB_L/2, cy=HAB_CY, cz=HAB_CZ, length=HAB_L, radius=HAB_R, axis='x', rings=10, t_count=16)
    
    # Hemispherical End-Caps (Forward and Aft bulkheads)
    add_ellipsoid(lines, 'C_HAB', cx=HAB_L/2, cy=HAB_CY, cz=HAB_CZ, rx=1.0, ry=HAB_R, rz=HAB_R, rings=6, t_count=16, half='pos_x')
    add_ellipsoid(lines, 'C_HAB', cx=-HAB_L/2, cy=HAB_CY, cz=HAB_CZ, rx=1.0, ry=HAB_R, rz=HAB_R, rings=6, t_count=16, half='neg_x')

    # ==============================================================================
    # 4. FORWARD AIRLOCK & DECK (+X Axis)
    # ==============================================================================
    # Forward Crew Airlock Box projecting from the Hub
    add_box_mesh(lines, 'C_AIRLOCK', HUB_R, HUB_R+2.5, -1.5, 1.5, HUB_Z_BOT+0.5, HUB_Z_BOT+2.5, div=3)
    
    # Landing / Ramp Extrusion Deck
    add_quad_mesh(lines, 'C_AIRLOCK', (HUB_R+2.5, -1.8, HUB_Z_BOT+0.5), (HUB_R+4.5, -1.8, Z_FLOOR+0.1),
                                      (HUB_R+4.5,  1.8, Z_FLOOR+0.1), (HUB_R+2.5,  1.8, HUB_Z_BOT+0.5), u_steps=3, v_steps=3)

    # ==============================================================================
    # 5. PHOTOVOLTAIC SOLAR ARRAYS (Tracking Wings)
    # ==============================================================================
    # Massive multi-panel wings bolted symmetrically above the Port/Starboard Hab modules
    Z_MAST_TOP = 9.0
    Z_PANEL_TOP = 11.5
    Z_PANEL_BOT = 6.5
    
    # Structural Mounting Masts
    add_cylinder(lines, 'C_LEGS', cx=0.0, cy=HAB_CY, cz=HAB_CZ+HAB_R, length=(Z_MAST_TOP - (HAB_CZ+HAB_R)), radius=0.3, axis='z', rings=3, t_count=8)
    
    # PV Quad Meshes (Array 1: Aft, Array 2: Forward)
    # Note: `add_quad_mesh` with native arrays handles rigorous mirroring automatically.
    add_quad_mesh(lines, 'C_SOLAR', (-6.0, HAB_CY, Z_PANEL_TOP), (-1.0, HAB_CY, Z_PANEL_TOP), (-1.0, HAB_CY, Z_PANEL_BOT), (-6.0, HAB_CY, Z_PANEL_BOT), 4, 8)
    add_quad_mesh(lines, 'C_SOLAR', (1.0, HAB_CY, Z_PANEL_TOP), (6.0, HAB_CY, Z_PANEL_TOP), (6.0, HAB_CY, Z_PANEL_BOT), (1.0, HAB_CY, Z_PANEL_BOT), 4, 8)

    # ==============================================================================
    # 6. HIGH-GAIN COMMAND ANTENNA (HGA)
    # ==============================================================================
    Z_HGA_STRUT = HUB_Z_TOP + 1.8
    CZ_DISH = Z_HGA_STRUT + 0.5
    R_DISH = 2.5
    FOCAL = 1.0
    TILT_DISH = 45.0
    
    # Heavy Telemetry Mast
    add_cylinder(lines, 'C_LEGS', cx=0.0, cy=0.0, cz=HUB_Z_TOP+1.0, length=1.2, radius=0.4, axis='z', rings=2, t_count=8)
    
    p = np.radians(TILT_DISH)
    t = np.linspace(0, 2*np.pi, 24, endpoint=False)
    r_steps = np.linspace(0.2, R_DISH, 6)
    
    # Generate true parabola (Z = R^2 / 4f) natively pitched 45 degrees
    for r in r_steps:
        x_base = r * np.cos(t)
        y_base = r * np.sin(t)
        z_base = np.full_like(t, (r**2) / (4 * FOCAL))
        
        xr = x_base * np.cos(p) + z_base * np.sin(p)
        zr = -x_base * np.sin(p) + z_base * np.cos(p) + CZ_DISH
        append_sym(lines, 'C_DISH', list(xr)+[xr[0]], list(y_base)+[y_base[0]], list(zr)+[zr[0]])
        
    for a in np.linspace(0, 2*np.pi, 12, endpoint=False):
        xl = r_steps * np.cos(a)
        yl = r_steps * np.sin(a)
        zl = np.full_like(xl, (r_steps**2) / (4 * FOCAL)) if isinstance(r_steps, float) else (r_steps**2) / (4 * FOCAL)
        
        xr = xl * np.cos(p) + zl * np.sin(p)
        zr = -xl * np.sin(p) + zl * np.cos(p) + CZ_DISH
        append_sym(lines, 'C_DISH', xr, yl, zr)

    # ==============================================================================
    # 7. STRUCTURAL LANDING STRUTS & PADS
    # ==============================================================================
    # 6 massive diagonal spars anchoring the primary hub into the planetary surface
    STRUT_COUNT = 6
    R_BASE = 3.5
    R_FOOT = 7.0
    
    for i in range(STRUT_COUNT):
        theta = i * (2*np.pi / STRUT_COUNT) + np.pi/6
        x_top, y_top = R_BASE * np.cos(theta), R_BASE * np.sin(theta)
        x_bot, y_bot = R_FOOT * np.cos(theta), R_FOOT * np.sin(theta)
        
        # Heavy Abyssal Slate Spar
        append_segmented(lines, 'C_LEGS', [x_top, x_bot], [y_top, y_bot], [HUB_Z_BOT+0.5, Z_FLOOR+0.2])
        append_segmented(lines, 'C_LEGS', [x_top*0.9, x_bot*0.95], [y_top*0.9, y_bot*0.95], [HUB_Z_BOT+0.5, Z_FLOOR+0.2])
        
        # Flanged Load-Bearing Surface Pads
        add_cylinder(lines, 'C_LEGS', cx=x_bot, cy=y_bot, cz=Z_FLOOR, length=0.3, radius=1.2, axis='z', rings=2, t_count=12)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_base_station_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry flawlessly at payload centroid
        cam_x, cam_y, cam_z = 0.0, 0.0, 6.0
        
        # Starts explicitly from 115-degrees (Dramatic aesthetic exposing the forward airlock and sprawling arrays)
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
    # Anchor Centroid = Z=6.0m. The extensive habitat wings dictate an extreme radius spanning +/- 11.5m (Y-bound).
    # Setting cam_span strictly to 14.0 locks horizontal width symmetrically across a massive 28.0m view.
    # Vertical bounds output 14.0 * 1.777 = 24.8m total height window vertically.
    # With centroid at Z=6.0, window spans perfectly from Z=-18.8 to Z=+30.8.
    # Completely traps the planetary infrastructure safely inside the transparent viewport, immune to UI overlay clipping.
    cam_span = 14.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_LEGS',      C_LEGS,      1.5, 1.0),
        ('C_HAB',       C_HAB,       1.4, 1.0),
        ('C_AIRLOCK',   C_AIRLOCK,   1.3, 1.0),
        ('C_SOLAR',     C_SOLAR,     1.2, 1.0),
        ('C_DISH',      C_DISH,      1.6, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to parse the sprawling horizontal topography and the dominant solar wings
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-453a // MACRO-ENGINEERING TENSOR: EXTRATERRESTRIAL KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // PLANETARY BASE STATION INFRASTRUCTURE", color=C_HAB, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_SOLAR, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: CENTRAL HUB / HABITAT RINGS / PV ARRAYS / HGA PARABOLA", color=C_DISH, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-453a: PLANETARY BASE STATION TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Macro-Infrastructure Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
