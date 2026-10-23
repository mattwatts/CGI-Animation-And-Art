"""
PROJECT: Logic Garden 453j (Exact Physical Construct // ESAS Crew Module Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: ESAS, CREW MODULE, ORION, CEV, NASA, GLB, WIREFRAME, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional 5.5m aerospace scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Conical Hull, Ablative Heat Shield, RCS Quads, Docking Tunnel, Viewports.
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
OUT_DIR = "frames_453j_esas_crew_module"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG            = '#FFFFFF'      # White Substrate
C_TEXT          = '#111115'      # Indestructible Black (Typography)
C_GRID          = '#94A3B8'      # Subdued Steel (Orbital Tracking Grid)

C_HULL          = '#94A3B8'      # Slate Aluminium (Primary Pressurized Frustum)
C_HEATSHIELD    = '#1E293B'      # Carbon Slate (Aft Ablative Convex Dome)
C_DOCKING       = '#334155'      # Heavy Slate (Forward Parachute Bay & Tunnel)
C_RCS           = '#CA8A04'      # Kapton Gold (RCS Thruster Quads & Umbilical Bases)
C_WINDOWS       = '#005599'      # Deep Marine (Crew Viewports & Star Trackers)

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
    # Autonomously generates identical structural topology across the Y-axis
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

def add_box_mesh(lines_dict, col, cx, cy, cz, dx, dy, dz, div=2, reflect_y=False, rot_deg=0):
    # Generates a box centered at cx, cy, cz with total lengths dx, dy, dz. Can be rotated about Z.
    x_half, y_half, z_half = dx/2, dy/2, dz/2
    pts = [
        (-x_half, -y_half, -z_half), (x_half, -y_half, -z_half), (x_half, y_half, -z_half), (-x_half, y_half, -z_half),
        (-x_half, -y_half, z_half),  (x_half, -y_half, z_half),  (x_half, y_half, z_half),  (-x_half, y_half, z_half)
    ]
    rad = np.radians(rot_deg)
    c, s = np.cos(rad), np.sin(rad)
    tr_pts = []
    for px, py, pz in pts:
        rx = px * c - py * s
        ry = px * s + py * c
        tr_pts.append((cx + rx, cy + ry, cz + pz))
    
    add_quad_mesh(lines_dict, col, tr_pts[0], tr_pts[1], tr_pts[2], tr_pts[3], div, div, reflect_y)
    add_quad_mesh(lines_dict, col, tr_pts[4], tr_pts[5], tr_pts[6], tr_pts[7], div, div, reflect_y)
    add_quad_mesh(lines_dict, col, tr_pts[0], tr_pts[1], tr_pts[5], tr_pts[4], div, div, reflect_y)
    add_quad_mesh(lines_dict, col, tr_pts[3], tr_pts[2], tr_pts[6], tr_pts[7], div, div, reflect_y)
    add_quad_mesh(lines_dict, col, tr_pts[0], tr_pts[3], tr_pts[7], tr_pts[4], div, div, reflect_y)
    add_quad_mesh(lines_dict, col, tr_pts[1], tr_pts[2], tr_pts[6], tr_pts[5], div, div, reflect_y)

def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='z', rings=4, t_count=32, reflect_y=False):
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

def add_cone_frustum(lines_dict, col, cx, cy, cz, dz, r1, r2, axis='z', rings=6, t_count=32, reflect_y=False):
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
    
    for a in np.linspace(0, 2*np.pi, t_count, endpoint=False):
        sx, sy, sz = [], [], []
        for i, s in enumerate(steps):
            r = r_step[i]
            if axis == 'x':  sx.append(cx + s); sy.append(cy + r*np.cos(a)); sz.append(cz + r*np.sin(a))
            elif axis == 'y':sx.append(cx + r*np.cos(a)); sy.append(cy + s); sz.append(cz + r*np.sin(a))
            else:            sx.append(cx + r*np.cos(a)); sy.append(cy + r*np.sin(a)); sz.append(cz + s)
        if reflect_y: append_sym(lines_dict, col, sx, sy, sz)
        else: append_segmented(lines_dict, col, sx, sy, sz)

def add_elliptical_cap(lines_dict, col, cx, cy, cz, radius, depth, rings=5, t_count=32):
    # Shallow convex curve for the ablative heat shield
    z_steps = np.linspace(0, -depth, rings)
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    
    for z in z_steps:
        # Elliptical falloff
        r = radius * np.sqrt(1.0 - (z / -depth)**2)
        ix = cx + r*np.cos(t)
        iy = cy + r*np.sin(t)
        iz = np.full_like(t, cz + z)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
        
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        sx, sy, sz = [], [], []
        for z in z_steps:
            r = radius * np.sqrt(1.0 - (z / -depth)**2)
            sx.append(cx + r*np.cos(a))
            sy.append(cy + r*np.sin(a))
            sz.append(cz + z)
        append_segmented(lines_dict, col, sx, sy, sz)

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (ESAS CREW MODULE)
# ------------------------------------------------------------------
def generate_esas_static():
    lines = {
        'C_HULL': [], 'C_HEATSHIELD': [], 'C_DOCKING': [],
        'C_RCS': [], 'C_WINDOWS': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. ORBITAL TRACKING BASEPLATE (Simulation Floor)
    # ==============================================================================
    # Executing the grid sufficiently below the spacecraft to simulate orbital station-keeping
    Z_FLOOR = -2.0
    for r_p in [4.0, 8.0, 12.0]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-12.0, 12.0, 25)
    gy_range = np.linspace(-12.0, 12.0, 25)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. ABLATIVE HEAT SHIELD (AFT DOME)
    # ==============================================================================
    # 5.5m base diameter (R=2.75). A shallow dome capping the extreme physical descent thermodynamics.
    BASE_R = 2.75
    SHIELD_DEPTH = 0.5
    
    add_elliptical_cap(lines, 'C_HEATSHIELD', cx=0.0, cy=0.0, cz=0.0, radius=BASE_R, depth=SHIELD_DEPTH, rings=6, t_count=32)

    # ==============================================================================
    # 3. PRIMARY CONICAL FUSELAGE
    # ==============================================================================
    # The pressure vessel lofts up 3.0 metres, narrowing to a 1.0m radius docking collar
    TOP_R = 1.0
    CONE_H = 3.0
    
    add_cone_frustum(lines, 'C_HULL', cx=0.0, cy=0.0, cz=0.0, dz=CONE_H, r1=BASE_R, r2=TOP_R, axis='z', rings=10, t_count=32, reflect_y=False)

    # ==============================================================================
    # 4. FORWARD PARACHUTE BAY & DOCKING TUNNEL
    # ==============================================================================
    # Heavy structural module retaining recovery parachutes and rendezvous mechanisms
    Z_BAY_TOP = 3.6
    add_cylinder(lines, 'C_DOCKING', cx=0.0, cy=0.0, cz=CONE_H, length=(Z_BAY_TOP - CONE_H), radius=TOP_R, axis='z', rings=4, t_count=32, reflect_y=False)
    
    # Docking Adapter Tunnel
    TUNNEL_R = 0.65
    TUNNEL_TOP = 4.2
    add_cylinder(lines, 'C_DOCKING', cx=0.0, cy=0.0, cz=Z_BAY_TOP, length=(TUNNEL_TOP - Z_BAY_TOP), radius=TUNNEL_R, axis='z', rings=4, t_count=24, reflect_y=False)
    
    # Upper Axial Docking Ring
    add_cylinder(lines, 'C_DOCKING', cx=0.0, cy=0.0, cz=TUNNEL_TOP, length=0.1, radius=TUNNEL_R+0.1, axis='z', rings=2, t_count=24, reflect_y=False)

    # ==============================================================================
    # 5. REACTION CONTROL SYSTEM (RCS) QUADS
    # ==============================================================================
    # Thruster blocks arrayed at 45-degree offsets around the lower cone
    RCS_Z = 0.4
    R_RCS_BASE = BASE_R - (BASE_R - TOP_R) * (RCS_Z / CONE_H) + 0.15 # Offset slightly outwards

    for ang in [45, 135, 225, 315]:
        rad_ang = np.radians(ang)
        rcs_x = R_RCS_BASE * np.cos(rad_ang)
        rcs_y = R_RCS_BASE * np.sin(rad_ang)
        # Kapton Gold rectangular manifolds
        add_box_mesh(lines, 'C_RCS', rcs_x, rcs_y, RCS_Z, 0.4, 0.4, 0.6, div=2, reflect_y=False, rot_deg=ang)

    # ==============================================================================
    # 6. CREW VIEWPORTS (TRAPEZOIDAL MATRICES)
    # ==============================================================================
    # Star-tracking and crew visibility windows intersected smoothly against the cone
    WIN_Z_MID = 1.8
    WIN_H = 0.6
    WIN_W = 0.8
    
    for ang in [0, 90, 180, 270]:
        rad_ang = np.radians(ang)
        
        # Calculate local radius at window center to place mesh explicitly on the hull
        r_mid = BASE_R - (BASE_R - TOP_R) * (WIN_Z_MID / CONE_H) + 0.05
        
        c = np.cos(rad_ang)
        s = np.sin(rad_ang)
        
        # Pitch derivation to match cone angle
        # Slope = (R_BASE - R_TOP) / CONE_H = 1.75 / 3.0
        pitch = np.arctan2((BASE_R - TOP_R), CONE_H)
        
        # Build local plane then rotate into position
        pts_local = [
            (-WIN_W/2, -WIN_H/2), (WIN_W/2, -WIN_H/2), (WIN_W*0.35, WIN_H/2), (-WIN_W*0.35, WIN_H/2)
        ]
        
        w_pts = []
        for lx, lz in pts_local:
            # Apply pitch to the local Z pushing the bottom out
            proj_z = WIN_Z_MID + lz * np.cos(pitch)
            proj_r = r_mid - lz * np.sin(pitch)
            
            # Map back to world X/Y
            wx = proj_r * c - lx * s
            wy = proj_r * s + lx * c
            w_pts.append((wx, wy, proj_z))
            
        add_quad_mesh(lines, 'C_WINDOWS', w_pts[0], w_pts[1], w_pts[2], w_pts[3], u_steps=3, v_steps=3, reflect_y=False)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_esas_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry midway through the height
        cam_x, cam_y, cam_z = 0.0, 0.0, 1.5
        
        # Starts explicitly from 115-degrees (Dramatic aesthetic showcasing hull windows and RCS quads)
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
    # Anchor Centroid = Z=1.5m. The vehicle bounds radially to 2.75m from the core.
    # Setting cam_span strictly to 4.5 locks horizontal width symmetrically across a 9.0m view.
    # Vertical bounds output 4.5 * 1.777 = 7.99m (total height window 16.0m vertically).
    # Completely traps the entire 5.5m width capsule and 4.2m tall docking assembly safely inside the viewport, immune to UI overlay clipping.
    cam_span = 4.5
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',       C_GRID,       0.8, 0.4), 
        ('C_HEATSHIELD', C_HEATSHIELD, 1.6, 1.0),
        ('C_HULL',       C_HULL,       1.2, 1.0),
        ('C_DOCKING',    C_DOCKING,    1.4, 1.0),
        ('C_RCS',        C_RCS,        1.5, 1.0),
        ('C_WINDOWS',    C_WINDOWS,    1.8, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to distinctly parse the forward parachute docking tunnel against the wide aft heat shield
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-453j // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // ESAS CREW MODULE (ORION BASELINE)", color=C_HULL, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_HEATSHIELD, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: 5.5M FUSELAGE / AFT ABLATIVE DOME / RCS QUADS / DOCKING INTERFACE", color=C_RCS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-453j: ESAS CREW MODULE TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
