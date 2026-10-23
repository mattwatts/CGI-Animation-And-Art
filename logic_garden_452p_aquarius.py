"""
PROJECT: Logic Garden 452p (Exact Physical Construct // Aquarius SAC-D Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: AQUARIUS, SAC-D, SATELLITE, NASA, CONAE, GLB, WIREFRAME, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional aerospace scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: SAC-D Box Bus, Offset 2.5m Parabolic Reflector, Tri-Feed Horns, Solar Arrays.
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
OUT_DIR = "frames_452p_aquarius"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Orbital Tracking Grid)

C_BUS       = '#CA8A04'          # Kapton Gold (SAC-D High-Density Chassis Mesh)
C_PANELS    = '#005599'          # Deep Marine (Deployable Photovoltaic Arrays)
C_DISH      = '#334155'          # Heavy Slate (2.5m Offset Parabolic Reflector)
C_FEED      = '#1E293B'          # Carbon Slate (Radiometer Feed Horns & Boom)
C_HARDWARE  = '#0F172A'          # Abyssal Slate (Nadir Instrumentation Deck)

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

def add_rot_frustum(lines_dict, col, ox, oy, oz, dz, r1, r2, pitch_deg, rings=4, count=12):
    # Generates a conical frustum natively rotated across the Y-axis (Elevational Pitch)
    p = np.radians(pitch_deg)
    t = np.linspace(0, 2*np.pi, count, endpoint=False)
    for i in range(rings):
        z_curr = i * (dz / max(1, rings-1))
        r_curr = r1 + (r2 - r1) * (i / max(1, rings-1))
        
        x_b = r_curr * np.cos(t)
        y_b = r_curr * np.sin(t)
        z_b = np.full_like(t, z_curr)
        
        xr = x_b * np.cos(p) + z_b * np.sin(p)
        zr = -x_b * np.sin(p) + z_b * np.cos(p)
        
        append_sym(lines_dict, col, list(xr+ox)+[xr[0]+ox], list(y_b+oy)+[y_b[0]+oy], list(zr+oz)+[zr[0]+oz])
        
    for a in np.linspace(0, 2*np.pi, count//2, endpoint=False):
        sx, sy, sz = [], [], []
        for i in range(rings):
            z_curr = i * (dz / max(1, rings-1))
            r_curr = r1 + (r2 - r1) * (i / max(1, rings-1))
            x_b = r_curr * np.cos(a)
            y_b = r_curr * np.sin(a)
            xr = x_b * np.cos(p) + z_curr * np.sin(p)
            zr = -x_b * np.sin(p) + z_curr * np.cos(p)
            sx.append(xr+ox); sy.append(y_b+oy); sz.append(zr+oz)
        append_sym(lines_dict, col, sx, sy, sz)

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
# SUPERSTRUCTURE BUILDERS (AQUARIUS / SAC-D)
# ------------------------------------------------------------------
def generate_aquarius_static():
    lines = {
        'C_BUS': [], 'C_PANELS': [], 'C_DISH': [],
        'C_FEED': [], 'C_HARDWARE': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. ORBITAL TRACKING BASEPLATE (1 Unit = 1 Metre)
    # ==============================================================================
    Z_FLOOR = -3.5
    for r_p in [3.0, 6.0, 9.0]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-9.0, 9.0, 19)
    gy_range = np.linspace(-9.0, 9.0, 19)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. SAC-D OBSERVATORY BUS (Rectangular Form Factor)
    # ==============================================================================
    # Extends from Z=-1.5 to Z=1.5. Spans X +/- 1.2, Y +/- 0.8
    add_box_mesh(lines, 'C_BUS', -1.2, 1.2, -0.8, 0.8, -1.5, 1.5, div=5)

    # Secondary Environmental Instruments on the Nadir (Aft/-Z) Deck
    add_box_mesh(lines, 'C_HARDWARE', -0.5, 0.5, -0.4, 0.4, -1.9, -1.5, div=2)
    add_cylinder(lines, 'C_HARDWARE', cx=-0.8, cy=0.0, cz=-1.5, length=-0.6, radius=0.15, axis='z', rings=3, t_count=8)

    # ==============================================================================
    # 3. AQUARIUS 2.5-METRE PARABOLIC REFLECTOR
    # ==============================================================================
    # Explicit offset. Mounted at X=1.5, Z=2.2.
    # Dish is mathematically pitched backwards ~40 degrees over the bus.
    CX_DISH = 1.3
    CZ_DISH = 2.2
    R_DISH = 1.25
    FOCAL = 1.0
    TILT_DISH = 40.0
    
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
        
        append_sym(lines, 'C_DISH', list(xr)+[xr[0]], list(y_base)+[y_base[0]], list(zr)+[zr[0]])
        
    # Longitudinal Support Ribs
    for a in np.linspace(0, 2*np.pi, 16, endpoint=False):
        xl = r_steps * np.cos(a)
        yl = r_steps * np.sin(a)
        zl = (r_steps**2) / (4 * FOCAL)
        
        xr = xl * np.cos(p) + zl * np.sin(p) + CX_DISH
        zr = -xl * np.sin(p) + zl * np.cos(p) + CZ_DISH
        
        append_sym(lines, 'C_DISH', xr, yl, zr)

    # Dish mounting struts attaching it to the underlying +X bus wall
    append_segmented(lines, 'C_HARDWARE', [1.2, CX_DISH], [0.0, 0.0], [0.5, CZ_DISH])
    append_segmented(lines, 'C_HARDWARE', [1.2, CX_DISH], [0.4, 0.0], [1.0, CZ_DISH])
    append_segmented(lines, 'C_HARDWARE', [1.2, CX_DISH], [-0.4, 0.0], [1.0, CZ_DISH])

    # ==============================================================================
    # 4. AQUARIUS TRI-BAND RADIOMETER FEED HORNS & BOOM
    # ==============================================================================
    # Offset in the -X / +Z quadrant targeting the focal plane of the offset dish
    CX_FEED = -1.4
    CZ_FEED = 3.6
    TILT_FEED = 135.0 # Pointing back downwards at the dish
    
    # Heavy Structural Support Boom (Carbon Slate)
    add_box_mesh(lines, 'C_FEED', -0.2, 0.2, -0.4, 0.4, 1.5, 2.0, div=2)
    append_segmented(lines, 'C_FEED', [0.0, CX_FEED+0.2], [0.0, 0.0], [2.0, CZ_FEED-0.2])
    
    # The Array of 3 Conical Radiometer Horns, explicitly offset in Y
    HORN_OFFSETS = [-0.4, 0.0, 0.4]
    for oy in HORN_OFFSETS:
        add_rot_frustum(lines, 'C_FEED', ox=CX_FEED, oy=oy, oz=CZ_FEED, dz=0.6, r1=0.08, r2=0.22, pitch_deg=TILT_FEED, rings=4, count=12)
        add_rot_frustum(lines, 'C_FEED', ox=CX_FEED, oy=oy, oz=CZ_FEED, dz=-0.1, r1=0.08, r2=0.05, pitch_deg=TILT_FEED, rings=2, count=12)

    # ==============================================================================
    # 5. TRANSVERSE PHOTOVOLTAIC SOLAR ARRAYS
    # ==============================================================================
    # Massive wings extending laterally across the Y-axis. Spans up to +/- 5.0m
    P_RAD_START = 0.8
    P_RAD_END = 5.0
    P_WIDTH_X = 1.0 # 2.0m wide panels
    
    for sign in [-1, 1]:
        # Torsion Drive actuator housing
        add_cylinder(lines, 'C_HARDWARE', cx=0.0, cy=0.8*sign, cz=0.0, length=0.15*sign, radius=0.2, axis='y', rings=2, t_count=8)
        
        # True Quad-Mesh representing rigid deployable modules
        add_quad_mesh(lines, 'C_PANELS', 
                      (-P_WIDTH_X, P_RAD_START * sign, 0.0), (P_WIDTH_X, P_RAD_START * sign, 0.0),
                      (P_WIDTH_X, P_RAD_END * sign, 0.0), (-P_WIDTH_X, P_RAD_END * sign, 0.0), 
                      u_steps=6, v_steps=18)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_aquarius_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry flawlessly at payload centroid
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.5
        
        # Starts explicitly from 115-degrees (Dramatic aesthetic exposing the offset dish and radiometer boom)
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
    # Anchor Centroid = Dead zero. Solar array extreme Y-bounds reach +/- 5.0m. Z reaches 4.0m.
    # Setting cam_span strictly to 6.5 locks horizontal width symmetrically across a massive 13.0m view.
    # Vertical bounds output 6.5 * 1.777 = 11.55m total height window vertically.
    # Completely traps the space vehicle safely inside the transparent viewport, immune to UI overlay clipping.
    cam_span = 6.5
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_BUS',       C_BUS,       1.4, 1.0),
        ('C_PANELS',    C_PANELS,    1.2, 1.0),
        ('C_HARDWARE',  C_HARDWARE,  1.2, 1.0),
        ('C_FEED',      C_FEED,      1.3, 1.0),
        ('C_DISH',      C_DISH,      1.6, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to clearly parse the offset dish and tri-band horn arrangement
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-452p // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // AQUARIUS (SAC-D) SATELLITE MATRIX", color=C_BUS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_PANELS, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: SAC-D BUS / RADIOMETER FEED HORNS / 2.5M OFFSET PARABOLA", color=C_DISH, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-452p: AQUARIUS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
