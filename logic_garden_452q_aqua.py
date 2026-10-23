"""
PROJECT: Logic Garden 452q (Exact Physical Construct // Aqua PM-1 Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: AQUA, SATELLITE, NASA, EOS, GLB, WIREFRAME, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional aerospace scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: EOS Box Bus, Asymmetrical Solar Wing, AMSR-E Parabola, MODIS/AIRS Payloads.
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
OUT_DIR = "frames_452q_aqua"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Orbital Tracking Grid)

C_BUS       = '#CA8A04'          # Kapton Gold (EOS Main Bus MLI)
C_PANELS    = '#005599'          # Deep Marine (Single Asymmetrical Photovoltaic Wing)
C_AMSRE     = '#94A3B8'          # Slate Aluminium (2.0m AMSR-E Parabolic Reflector)
C_INSTR     = '#334155'          # Heavy Slate (MODIS / AIRS Instruments)
C_HARDWARE  = '#0F172A'          # Abyssal Slate (Telemetry Booms & X-Band)

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

def add_box_mesh(lines_dict, col, x1, x2, y1, y2, z1, z2, div=4):
    # 6-Face Mathematical Integration of an absolute rectangular prism
    add_quad_mesh(lines_dict, col, (x1, y1, z1), (x2, y1, z1), (x2, y2, z1), (x1, y2, z1), div, div) # Bottom
    add_quad_mesh(lines_dict, col, (x1, y1, z2), (x2, y1, z2), (x2, y2, z2), (x1, y2, z2), div, div) # Top
    add_quad_mesh(lines_dict, col, (x1, y1, z1), (x2, y1, z1), (x2, y1, z2), (x1, y1, z2), div, div) # Front
    add_quad_mesh(lines_dict, col, (x1, y2, z1), (x2, y2, z1), (x2, y2, z2), (x1, y2, z2), div, div) # Back
    add_quad_mesh(lines_dict, col, (x1, y1, z1), (x1, y2, z1), (x1, y2, z2), (x1, y1, z2), div, div) # Left
    add_quad_mesh(lines_dict, col, (x2, y1, z1), (x2, y2, z1), (x2, y2, z2), (x2, y1, z2), div, div) # Right

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
# SUPERSTRUCTURE BUILDERS (AQUA / EOS PM-1)
# ------------------------------------------------------------------
def generate_aqua_static():
    lines = {
        'C_BUS': [], 'C_PANELS': [], 'C_AMSRE': [],
        'C_INSTR': [], 'C_HARDWARE': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. ORBITAL TRACKING BASEPLATE (1 Unit = 1 Metre)
    # ==============================================================================
    Z_FLOOR = -4.0
    for r_p in [4.0, 8.0, 12.0]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-12.0, 12.0, 19)
    gy_range = np.linspace(-12.0, 12.0, 19)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. EOS COMMON SPACECRAFT BUS (Rectangular Form Factor)
    # ==============================================================================
    # Extends 4.8m long (X), 2.8m wide (Y), 2.8m high (Z)
    add_box_mesh(lines, 'C_BUS', -2.4, 2.4, -1.4, 1.4, -1.4, 1.4, div=5)

    # ==============================================================================
    # 3. NADIR INSTRUMENT DECK (MODIS & AIRS Earth-facing Payloads)
    # ==============================================================================
    # MODIS (Moderate Resolution Imaging Spectroradiometer)
    add_box_mesh(lines, 'C_INSTR', -0.5, 0.8, -1.0, 1.0, -2.4, -1.4, div=3)
    add_cylinder(lines, 'C_HARDWARE', cx=-0.2, cy=0.0, cz=-1.9, length=0.0, radius=0.3, axis='x', rings=1, t_count=8) # Optical Aperture
    
    # AIRS (Atmospheric Infrared Sounder)
    add_box_mesh(lines, 'C_INSTR', -1.8, -0.6, -1.0, 0.5, -2.1, -1.4, div=2)
    add_cylinder(lines, 'C_HARDWARE', cx=-1.2, cy=-0.2, cz=-2.1, length=-0.2, radius=0.2, axis='z', rings=2, t_count=8)

    # CERES Modules (Mounted Aft)
    add_cylinder(lines, 'C_HARDWARE', cx=-2.4, cy=0.8, cz=0.0, length=-0.4, radius=0.2, axis='x', rings=3, t_count=8)
    add_cylinder(lines, 'C_HARDWARE', cx=-2.4, cy=-0.8, cz=0.0, length=-0.4, radius=0.2, axis='x', rings=3, t_count=8)

    # ==============================================================================
    # 4. AMSR-E INSTRUMENT (Forward Pitch-Mounted Parabola)
    # ==============================================================================
    # Explicit forward offset. Mounted at X=2.4. Pitch set to 45 degrees.
    CX_DISH = 3.2
    CY_DISH = 0.0
    CZ_DISH = 1.6
    R_DISH = 1.0      # 2.0-metre diameter
    FOCAL = 0.8
    TILT_DISH = 45.0
    
    p = np.radians(TILT_DISH)
    t = np.linspace(0, 2*np.pi, 32, endpoint=False)
    r_steps = np.linspace(0.2, R_DISH, 6)
    
    # Generate true parabola (Z = R^2 / 4f) natively rotated across elevation axis
    for r in r_steps:
        x_base = r * np.cos(t)
        y_base = r * np.sin(t)
        z_base = (r**2) / (4 * FOCAL)
        
        xr = x_base * np.cos(p) + z_base * np.sin(p) + CX_DISH
        zr = -x_base * np.sin(p) + z_base * np.cos(p) + CZ_DISH
        
        append_sym(lines, 'C_AMSRE', list(xr)+[xr[0]], list(y_base+CY_DISH)+[y_base[0]+CY_DISH], list(zr)+[zr[0]])
        
    # Radial Support Ribs
    for a in np.linspace(0, 2*np.pi, 16, endpoint=False):
        xl = r_steps * np.cos(a)
        yl = r_steps * np.sin(a)
        zl = (r_steps**2) / (4 * FOCAL)
        
        xr = xl * np.cos(p) + zl * np.sin(p) + CX_DISH
        zr = -xl * np.sin(p) + zl * np.cos(p) + CZ_DISH
        
        append_sym(lines, 'C_AMSRE', xr, yl+CY_DISH, zr)

    # Spin-mount housing locking dish to forward deck
    add_cylinder(lines, 'C_HARDWARE', cx=2.4, cy=0.0, cz=1.0, length=0.8, radius=0.4, axis='x', rings=3, t_count=12)
    append_segmented(lines, 'C_HARDWARE', [CX_DISH, 2.8], [0.0, 0.0], [CZ_DISH, 1.0])

    # ==============================================================================
    # 5. ASYMMETRICAL SOLAR ARRAY WING (-Y Axis Only)
    # ==============================================================================
    # Aqua strictly deploys one massive array to avoid radiant blocking of cooling units
    P_RAD_START = -1.4
    P_RAD_END = -10.0
    P_WIDTH_X = 1.3 # 2.6m wide panel footprint
    
    # Actuator / Yoke housing
    add_cylinder(lines, 'C_HARDWARE', cx=0.0, cy=P_RAD_START, cz=0.0, length=-0.4, radius=0.25, axis='y', rings=2, t_count=8)
    
    # True Quad-Mesh representing rigid deployable multi-panel wing
    add_quad_mesh(lines, 'C_PANELS', 
                  (-P_WIDTH_X, P_RAD_START, 0.0), (P_WIDTH_X, P_RAD_START, 0.0),
                  (P_WIDTH_X, P_RAD_END, 0.0), (-P_WIDTH_X, P_RAD_END, 0.0), 
                  u_steps=5, v_steps=20)
                  
    # X-Band Telemetry Boom extension (Opposite side +Y)
    add_cylinder(lines, 'C_HARDWARE', cx=0.0, cy=1.4, cz=0.0, length=2.5, radius=0.05, axis='y', rings=2, t_count=4)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_aqua_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry flawlessly at payload centroid
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.0
        
        # Starts explicitly from 115-degrees (Dramatic aesthetic exposing the massive one-sided solar array)
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
    # Anchor Centroid = Dead zero. Solar array extreme reaches out to Y=-10.0m. X bounds ~+/- 4.0m.
    # Setting cam_span strictly to 11.5 locks horizontal width symmetrically across a massive 23.0m view.
    # Vertical bounds output 11.5 * 1.777 = 20.43m total height window vertically.
    # Completely traps the space vehicle safely inside the transparent viewport, immune to UI overlay clipping.
    cam_span = 11.5
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_BUS',       C_BUS,       1.4, 1.0),
        ('C_PANELS',    C_PANELS,    1.2, 1.0),
        ('C_HARDWARE',  C_HARDWARE,  1.2, 1.0),
        ('C_INSTR',     C_INSTR,     1.3, 1.0),
        ('C_AMSRE',     C_AMSRE,     1.5, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to parse the dense nadir instrument suite below the MLI bus
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-452q // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // AQUA (EOS PM-1) SATELLITE MATRIX", color=C_BUS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_PANELS, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: EOS MAIN BUS / ASYMMETRICAL SOLAR WING / AMSR-E TRACKING DISH", color=C_AMSRE, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-452q: AQUA TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
