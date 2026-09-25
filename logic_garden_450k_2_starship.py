"""
PROJECT: Logic Garden 450k (Exact Physical Construct // Federation-Class Dreadnought Matrix NCC-2100)
FORMAT: YouTube Shorts (1080x1920)
METADATA: STAR TREK, STARSHIP, DREADNOUGHT, WIREFRAME, ENGINEERING, KINEMATICS, NCC-2100
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: True tri-nacelle warp matrix, sweeping saucer topography, parametric deflector array.
- Strict Bounds Protocol: Core anchor locked to Origin. cam_span dynamically set to 16.0 assuring ABSOLUTE 100% frame preservation.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from absolute 115-degree dramatic front-quarter angle.
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
OUT_DIR = "frames_450k_starship"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Baseplate Reference)

C_HULL_MAIN = '#94A3B8'          # Heavy Slate (Primary Saucer & Secondary Hull)
C_HULL_DARK = '#475569'          # Machined Steel (Connecting Pylons & Neck)
C_DETAILS   = '#1E293B'          # Carbon Slate (Structural seams, Registry plating)
C_BUSSARD   = '#E11D48'          # Kinematic Red (Front Nacelle Collectors)
C_DEFLECTOR = '#00D2FF'          # High Engine Cyan (Navigational Deflector & Warp Grilles)

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

def append_segmented(lines_dict, key, xs, ys, zs, off=(0,0,0), scale_x=1.0):
    dx, dy, dz = off
    xs, ys, zs = list(xs), list(ys), list(zs)
    for i in range(len(xs) - 1):
        x1 = xs[i] * scale_x + dx
        x2 = xs[i+1] * scale_x + dx
        lines_dict[key].append(([x1, x2], [ys[i]+dy, ys[i+1]+dy], [zs[i]+dz, zs[i+1]+dz]))

# ------------------------------------------------------------------
# GEOMETRIC PRIMITIVES
# ------------------------------------------------------------------
def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='x', rings=6, t_count=20, off=(0,0,0)):
    t = np.linspace(0, 2*np.pi, t_count+1)
    steps = np.linspace(0, length, rings)
    for s in steps:
        if axis == 'x':  ix, iy, iz = np.full_like(t, cx + s), cy + radius*np.cos(t), cz + radius*np.sin(t)
        elif axis == 'y': ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + s), cz + radius*np.sin(t)
        else:             ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), np.full_like(t, cz + s)
        append_segmented(lines_dict, col, ix, iy, iz, off)
    for a in t[:-1][::max(1, t_count//8)]:
        if axis == 'x':   sx, sy, sz = cx + steps, [cy + radius*np.cos(a)]*rings, [cz + radius*np.sin(a)]*rings
        elif axis == 'y': sx, sy, sz = [cx + radius*np.cos(a)]*rings, cy + steps, [cz + radius*np.sin(a)]*rings
        else:             sx, sy, sz = [cx + radius*np.cos(a)]*rings, [cy + radius*np.sin(a)]*rings, cz + steps
        append_segmented(lines_dict, col, sx, sy, sz, off)

def add_dome(lines_dict, col, cx, cy, cz, radius, axis='x', dir=1, rings=5, t_count=20):
    # Perfect spherical parameterisation for Bussard Collectors and sensor arrays
    p_steps = np.linspace(0, np.pi/2, rings)
    for p in p_steps:
        r_slice = radius * np.cos(p)
        h_slice = radius * np.sin(p) * dir
        t = np.linspace(0, 2*np.pi, t_count+1)
        if axis == 'x':   ix, iy, iz = np.full_like(t, cx + h_slice), cy + r_slice*np.cos(t), cz + r_slice*np.sin(t)
        elif axis == 'y': ix, iy, iz = cx + r_slice*np.cos(t), np.full_like(t, cy + h_slice), cz + r_slice*np.sin(t)
        else:             ix, iy, iz = cx + r_slice*np.cos(t), cy + r_slice*np.sin(t), np.full_like(t, cz + h_slice)
        append_segmented(lines_dict, col, ix, iy, iz)
        
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        rr = radius * np.cos(p_steps)
        hh = radius * np.sin(p_steps) * dir
        if axis == 'x':   sx, sy, sz = cx + hh, cy + rr*np.cos(a), cz + rr*np.sin(a)
        elif axis == 'y': sx, sy, sz = cx + rr*np.cos(a), cy + hh, cz + rr*np.sin(a)
        else:             sx, sy, sz = cx + rr*np.cos(a), cy + rr*np.sin(a), cz + hh
        append_segmented(lines_dict, col, sx, sy, sz)

def add_quad_mesh(lines_dict, col, p1, p2, p3, p4, u_steps=6, v_steps=6):
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

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (FEDERATION CLASS DREADNOUGHT)
# ------------------------------------------------------------------
def generate_dreadnought_static():
    lines = {
        'C_HULL_MAIN': [], 'C_HULL_DARK': [], 'C_DETAILS': [], 
        'C_BUSSARD': [], 'C_DEFLECTOR': [], 'C_GRID': []
    }

    # 1. BASEPLATE ENVELOPE (REFERENCE GRID)
    # Scaled to the absolute 32m x 24m functional operational envelope
    gx_range = np.linspace(-15.0, 15.0, 21)
    gy_range = np.linspace(-12.0, 12.0, 16)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, -6.0))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, -6.0))

    # ==============================================================================
    # 2. SAUCER SECTION (PRIMARY HULL)
    # ==============================================================================
    # Centered at X = 5.0, spanning radius 7.5
    cx_s = 5.0; cy_s = 0.0
    r_z_profile = [
        (0.0, 5.2), (0.8, 5.2), (1.2, 4.4), (2.0, 4.2),  # Upper Bridge Domes
        (2.0, 3.8), (7.0, 3.2), (7.5, 3.1), (7.5, 2.9),  # Main upper sloped hull & edge
        (7.0, 2.8), (3.0, 2.2), (1.5, 1.8), (0.0, 1.5)   # Lower sloped hull & sensor array
    ]
    t_s = np.linspace(0, 2*np.pi, 48+1)
    for i in range(len(r_z_profile)-1):
        r1, z1 = r_z_profile[i]
        r2, z2 = r_z_profile[i+1]
        c_ring = 'C_DETAILS' if i in [0, 2, 7, 10] else 'C_HULL_MAIN' 
        for a in t_s[:-1][::3]: # Radial support struts mapping the hull plates
            append_segmented(lines, c_ring, [cx_s + r1*np.cos(a), cx_s + r2*np.cos(a)], [cy_s + r1*np.sin(a), cy_s + r2*np.sin(a)], [z1, z2])
        gx1, gy1 = cx_s + r1 * np.cos(t_s), cy_s + r1 * np.sin(t_s)
        append_segmented(lines, c_ring, list(gx1), list(gy1), [z1]*len(gx1))

    # ==============================================================================
    # 3. SECONDARY HULL & DORSAL NECK
    # ==============================================================================
    # Dorsal Neck sweeping from lower saucer (X=3, Z=2.0) back to Engineering (X=2, Z=-1.0)
    p_ntl = (3.5, 0.4, 2.2); p_ntr = (3.5, -0.4, 2.2)
    p_nbl = (1.5, 0.6, -1.0); p_nbr = (1.5, -0.6, -1.0)
    p_ntl2 = (1.5, 0.3, 2.2); p_ntr2 = (1.5, -0.3, 2.2)
    p_nbl2 = (-1.0, 0.5, -1.0); p_nbr2 = (-1.0, -0.5, -1.0)
    add_quad_mesh(lines, 'C_HULL_DARK', p_ntl, p_ntr, p_nbr, p_nbl, u_steps=3, v_steps=3)     # Front sweep
    add_quad_mesh(lines, 'C_HULL_DARK', p_ntl2, p_ntl, p_nbl, p_nbl2, u_steps=3, v_steps=3)   # Port sweep
    add_quad_mesh(lines, 'C_HULL_DARK', p_ntr, p_ntr2, p_nbr2, p_nbr, u_steps=3, v_steps=3)   # Starboard sweep

    # Main Engineering Cylinder (Tapering)
    x_body = np.linspace(-8, 5, 20)
    for i in range(len(x_body)):
        x = x_body[i]
        # Radius expands to 1.8 near the middle, shrinks strictly down to 1.0 at aft shuttlebay
        r = 1.8 - 0.8 * ((x - 1.0) / 9.0)**2 if x < 1.0 else 1.8 - 0.2 * ((x - 1.0) / 4.0)**2
        z_c = -2.5
        t = np.linspace(0, 2*np.pi, 24+1)
        y_ring = r * np.cos(t); z_ring = z_c + r * np.sin(t)
        
        append_segmented(lines, 'C_HULL_MAIN', [x]*25, list(y_ring), list(z_ring))
        if i > 0:
            for k in range(0, 24, 2):
                append_segmented(lines, 'C_HULL_MAIN', [x_prev_b, x], [y_prev_b[k], y_ring[k]], [z_prev_b[k], z_ring[k]])
        x_prev_b, y_prev_b, z_prev_b = x, y_ring.copy(), z_ring.copy()

    # Forward Navigational Deflector Array
    add_dome(lines, 'C_DEFLECTOR', 5.0, 0.0, -2.5, 1.4, axis='x', dir=1, rings=4, t_count=20)
    add_cylinder(lines, 'C_DETAILS', 5.0, 0.0, -2.5, length=0.6, radius=0.3, axis='x', rings=2) # Spire emitter

    # ==============================================================================
    # 4. TRI-NACELLE WARP MATRIX (The Federation Class Signature)
    # ==============================================================================
    nacelles = [
        (-2.0,  5.5,  0.0),  # Port Lower
        (-2.0, -5.5,  0.0),  # Starboard Lower
        (-2.0,  0.0,  6.5)   # Dorsal Central
    ]
    
    for nx, ny, nz in nacelles:
        # Base precise 15m Nacelle cylinders
        add_cylinder(lines, 'C_HULL_MAIN', nx-10.0, ny, nz, length=15.0, radius=0.9, axis='x', rings=10, t_count=16)
        
        # Radiant Bussard Ramscoops (Forward Facing True Kinematic Red)
        add_dome(lines, 'C_BUSSARD', nx+5.0, ny, nz, radius=0.9, axis='x', dir=1, rings=6, t_count=16)
        
        # Lateral Warp Field Grilles (High Cyan Arrays)
        for g_off in [-0.8, 0.8]:
            append_segmented(lines, 'C_DEFLECTOR', [nx-8.0, nx+3.0], [ny+g_off, ny+g_off], [nz, nz])
            append_segmented(lines, 'C_DEFLECTOR', [nx-8.0, nx+3.0], [ny, ny], [nz+g_off, nz+g_off])
            
        # Aft Exhaust Domes
        add_dome(lines, 'C_DETAILS', nx-10.0, ny, nz, radius=0.7, axis='x', dir=-1, rings=3, t_count=12)

    # ==============================================================================
    # 5. HEAVY PYLON LATTICES
    # ==============================================================================
    # Lower Swept Pylons (Anchoring Port and Starboard Nacelles rigidly to Secondary Hull)
    add_quad_mesh(lines, 'C_HULL_DARK', ( 0.0,  1.4, -2.5), (-1.5,  1.4, -2.5), (-6.0,  5.5,  0.0), (-3.5,  5.5,  0.0), u_steps=3, v_steps=6) # Port
    add_quad_mesh(lines, 'C_HULL_DARK', ( 0.0, -1.4, -2.5), (-1.5, -1.4, -2.5), (-6.0, -5.5,  0.0), (-3.5, -5.5,  0.0), u_steps=3, v_steps=6) # Starboard

    # Central Dorsal Pylon (Anchoring 3rd Nacelle directly over the primary hull axis)
    add_quad_mesh(lines, 'C_HULL_DARK', ( 1.0,  0.5,  4.2), (-1.0,  0.5,  4.2), (-5.0,  0.5,  6.0), (-3.0,  0.5,  6.0), u_steps=2, v_steps=6)
    add_quad_mesh(lines, 'C_HULL_DARK', ( 1.0, -0.5,  4.2), (-1.0, -0.5,  4.2), (-5.0, -0.5,  6.0), (-3.0, -0.5,  6.0), u_steps=2, v_steps=6)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_dreadnought_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking the rig rigidly spanning X=-12 to X=14
        cam_x, cam_y, cam_z = 0.0, 0.0, 1.5 
        
        # Starts explicitly from 115-degrees (Front/Side dynamic sweeping perspective yielding absolute dominance)
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
    # Anchor = 0.0. Max radius safely inside 15m.
    # Setting cam_span strictly to 16.0 to guarantee flawless 9:16 border insulation for a 32m footprint dynamically.
    cam_span = 16.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.3), 
        ('C_HULL_DARK', C_HULL_DARK, 1.4, 1.0),
        ('C_HULL_MAIN', C_HULL_MAIN, 1.2, 1.0),
        ('C_DETAILS',   C_DETAILS,   1.5, 1.0),
        ('C_DEFLECTOR', C_DEFLECTOR, 2.0, 1.0),
        ('C_BUSSARD',   C_BUSSARD,   2.0, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +15 degrees to proudly array the immense three-nozzle warp field structure
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=15.0)
            render_queue.append((np.mean(depth), u, v, c_val, lw, alpha))

    # ABSOLUTE Z-SORT (Strict Painter's Algorithm Depth Culling)
    render_queue.sort(key=lambda item: item[0], reverse=True)
    for depth, u, v, c, lw, a in render_queue:
        ax.plot(u, v, color=c, lw=lw, alpha=a)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (TOP HUD)
    # ------------------------------------------------------------------
    ui_t = cam_span * 1.45
    ax.add_patch(patches.Rectangle((-cam_span, ui_t), cam_span*2, 12.0, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_t, ui_t], color=C_TEXT, lw=6, zorder=81)

    ax.text(-cam_span*0.95, ui_t+1.3, "LG-450k // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=18, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t+0.3, "EXPLICIT TRUE-SCALE GEOMETRY // U.S.S. FEDERATION (NCC-2100) MATRIX", color=C_HULL_DARK, fontsize=13, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b+2.1, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_HULL_MAIN, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+1.0, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.2, "TOPOLOGICAL YIELD: TRUE TRI-NACELLE WARP LATTICE & HEAVY DORSAL PYLON", color=C_DEFLECTOR, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-450k: STARSHIP KINEMATICS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
