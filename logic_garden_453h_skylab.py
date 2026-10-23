"""
PROJECT: Logic Garden 453h (Exact Physical Construct // Skylab Orbital Workshop Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: SKYLAB, SPACE STATION, NASA, APOLLO, GLB, WIREFRAME, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional 25m aerospace scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: S-IVB OWS, Asymmetrical Solar Wing, Kapton Gold Parasol, ATM Cross Arrays.
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
OUT_DIR = "frames_453h_skylab"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Deep Space Tracking Plane)

C_OWS       = '#334155'          # Heavy Slate (Primary Orbital Workshop / S-IVB Hull)
C_MDA       = '#94A3B8'          # Slate Aluminium (Multiple Docking Adapter & Airlock)
C_SUNSHIELD = '#CA8A04'          # Kapton Gold (Deployed Parasol Thermal Blanket)
C_ATM       = '#1E293B'          # Carbon Slate (Apollo Telescope Mount & Struts)
C_SOLAR     = '#005599'          # Deep Marine (Single Surviving Wing & 4x ATM Arrays)

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
        if axis == 'x':  sx, sy, sz = cx + steps, [cy + radius*np.cos(a)]*rings, [cz + radius*np.sin(a)]*rings
        elif axis == 'y':sx, sy, sz = [cx + radius*np.cos(a)]*rings, cy + steps, [cz + radius*np.sin(a)]*rings
        else:            sx, sy, sz = [cx + radius*np.cos(a)]*rings, [cy + radius*np.sin(a)]*rings, cz + steps
        if reflect_y: append_sym(lines_dict, col, sx, sy, sz)
        else: append_segmented(lines_dict, col, sx, sy, sz)

def add_cone_frustum(lines_dict, col, cx, cy, cz, dz, r1, r2, axis='x', rings=4, t_count=16, reflect_y=False):
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
# SUPERSTRUCTURE BUILDERS (SKYLAB ORBITAL WORKSHOP)
# ------------------------------------------------------------------
def generate_skylab_static():
    lines = {
        'C_OWS': [], 'C_MDA': [], 'C_SUNSHIELD': [],
        'C_ATM': [], 'C_SOLAR': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. DEEP SPACE TRACKING PLANE (1 Unit = 1 Metre)
    # ==============================================================================
    Z_FLOOR = -7.0
    for r_p in [6.0, 12.0, 18.0]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-18.0, 18.0, 19)
    gy_range = np.linspace(-18.0, 18.0, 19)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. ORBITAL WORKSHOP (OWS)
    # ==============================================================================
    # Extends from X = 0.0 aft to X = -12.0. Massive 3.3m radius S-IVB adapted stage.
    add_cylinder(lines, 'C_OWS', cx=-12.0, cy=0.0, cz=0.0, length=12.0, radius=3.3, axis='x', rings=10, t_count=24, reflect_y=False)

    # ==============================================================================
    # 3. TWIN-POLE DEPLOYED SUNSHIELD (KAPTON GOLD PARASOL)
    # ==============================================================================
    # Directly wrapped geometrically around the damaged +Z upper quadrant of the OWS
    theta_angles = np.linspace(np.pi/6, 5*np.pi/6, 12)
    x_steps = np.linspace(-11.0, -1.0, 14)
    R_PARASOL = 3.45  # Elevated structural clearance
    
    # Longitudinal drape strings
    for th in theta_angles:
        xl = x_steps
        yl = np.full_like(xl, R_PARASOL * np.cos(th))
        zl = np.full_like(xl, R_PARASOL * np.sin(th))
        append_segmented(lines, 'C_SUNSHIELD', xl, yl, zl)
        
    # Latitudinal support arches
    for x_val in x_steps:
        xl = np.full_like(theta_angles, x_val)
        yl = R_PARASOL * np.cos(theta_angles)
        zl = R_PARASOL * np.sin(theta_angles)
        append_segmented(lines, 'C_SUNSHIELD', xl, yl, zl)

    # ==============================================================================
    # 4. AIRLOCK MODULE (AM) & MULTIPLE DOCKING ADAPTER (MDA)
    # ==============================================================================
    # AM bridges the gap between OWS and MDA.
    add_cylinder(lines, 'C_MDA', cx=0.0, cy=0.0, cz=0.0, length=2.0, radius=1.6, axis='x', rings=3, t_count=16, reflect_y=False)
    
    # Forward MDA docking cylinder
    add_cylinder(lines, 'C_MDA', cx=2.0, cy=0.0, cz=0.0, length=5.0, radius=1.5, axis='x', rings=5, t_count=16, reflect_y=False)
    
    # Forward Axial Docking Port Collar (Target node for Apollo CSM)
    add_cylinder(lines, 'C_MDA', cx=7.0, cy=0.0, cz=0.0, length=0.3, radius=0.8, axis='x', rings=2, t_count=12, reflect_y=False)

    # ==============================================================================
    # 5. APOLLO TELESCOPE MOUNT (ATM) & MOUNTING TRUSS
    # ==============================================================================
    # ATM elevated structurally atop the assembly out of the general shadow
    ATM_CX = 2.0
    ATM_Z_BOT = 4.0
    ATM_Z_TOP = 7.0
    
    # Heavy diagonal framework truss
    append_sym(lines, 'C_ATM', [1.0, ATM_CX-0.5], [1.0, 1.0], [1.5, ATM_Z_BOT])
    append_sym(lines, 'C_ATM', [3.0, ATM_CX+0.5], [1.0, 1.0], [1.5, ATM_Z_BOT])

    # Central ATM Hex/Cylindrical Body
    add_cylinder(lines, 'C_ATM', cx=ATM_CX, cy=0.0, cz=ATM_Z_BOT, length=(ATM_Z_TOP - ATM_Z_BOT), radius=1.5, axis='z', rings=5, t_count=16, reflect_y=False)
    # Telescopic Aperture Shield
    add_cylinder(lines, 'C_ATM', cx=ATM_CX, cy=0.0, cz=ATM_Z_TOP, length=0.4, radius=0.6, axis='z', rings=2, t_count=12, reflect_y=False)

    # ==============================================================================
    # 6. EXPLICIT ASYMMETRICAL SOLAR ARRAYS
    # ==============================================================================
    # A. The 4-Wing ATM Windmill Generation (Fully symmetrical arrays around Z=5.5)
    Z_WINDMILL = 5.5
    W_ATM = 1.5
    
    # Wing +X
    add_quad_mesh(lines, 'C_SOLAR', (ATM_CX+1.5, W_ATM, Z_WINDMILL), (ATM_CX+9.0, W_ATM, Z_WINDMILL),
                                    (ATM_CX+9.0, -W_ATM, Z_WINDMILL), (ATM_CX+1.5, -W_ATM, Z_WINDMILL), u_steps=8, v_steps=3, reflect_y=False)
    # Wing -X
    add_quad_mesh(lines, 'C_SOLAR', (ATM_CX-1.5, W_ATM, Z_WINDMILL), (ATM_CX-9.0, W_ATM, Z_WINDMILL),
                                    (ATM_CX-9.0, -W_ATM, Z_WINDMILL), (ATM_CX-1.5, -W_ATM, Z_WINDMILL), u_steps=8, v_steps=3, reflect_y=False)
    # Wing +Y
    add_quad_mesh(lines, 'C_SOLAR', (ATM_CX+W_ATM, 1.5, Z_WINDMILL), (ATM_CX+W_ATM, 9.0, Z_WINDMILL),
                                    (ATM_CX-W_ATM, 9.0, Z_WINDMILL), (ATM_CX-W_ATM, 1.5, Z_WINDMILL), u_steps=3, v_steps=8, reflect_y=False)
    # Wing -Y
    add_quad_mesh(lines, 'C_SOLAR', (ATM_CX+W_ATM, -1.5, Z_WINDMILL), (ATM_CX+W_ATM, -9.0, Z_WINDMILL),
                                    (ATM_CX-W_ATM, -9.0, Z_WINDMILL), (ATM_CX-W_ATM, -1.5, Z_WINDMILL), u_steps=3, v_steps=8, reflect_y=False)

    # B. The Single Surviving OWS Panel (Extensively Asymmetrical)
    # Deployed solely from the Starboard (+Y) Vector
    OWS_PANEL_X1 = -2.0
    OWS_PANEL_X2 = -10.0
    OWS_PANEL_Y1 = 3.3
    OWS_PANEL_Y2 = 12.0
    
    # Bypassing symmetry logic strictly using explicit quad generation bounds
    add_quad_mesh(lines, 'C_SOLAR', (OWS_PANEL_X1, OWS_PANEL_Y1, 0.0), (OWS_PANEL_X1, OWS_PANEL_Y2, 0.0),
                                    (OWS_PANEL_X2, OWS_PANEL_Y2, 0.0), (OWS_PANEL_X2, OWS_PANEL_Y1, 0.0), u_steps=4, v_steps=12, reflect_y=False)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_skylab_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry biased towards the forward modules
        # Centralizing the X spread roughly to X=-2.0, Z=2.0 to balance the massive offset arrays
        cam_x, cam_y, cam_z = -2.0, 0.0, 2.0
        
        # Starts explicitly from 115-degrees (Dramatic aesthetic showcasing the parasol and the single asymmetrical array)
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
    # Anchor Centroid = X=-2.0, Y=0.0, Z=2.0m. Extents rigidly track ~ +/- 12m longitudinally.
    # The extreme deployed array (+Y) extends to 12.0m. Off-centroid this demands a wide clearance margin.
    # Setting cam_span strictly to 17.5 locks horizontal width symmetrically across a massive 35.0m view.
    # Vertical bounds output 17.5 * 1.777 = 31.1m half-height (total transparent window 62.2m).
    # Completely traps the entire widely dispersed asymmetrical space vehicle safely inside the transparent viewport, immune to UI overlay clipping.
    cam_span = 17.5
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_OWS',       C_OWS,       1.4, 1.0),
        ('C_MDA',       C_MDA,       1.3, 1.0),
        ('C_ATM',       C_ATM,       1.5, 1.0),
        ('C_SOLAR',     C_SOLAR,     1.2, 1.0),
        ('C_SUNSHIELD', C_SUNSHIELD, 1.5, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to parse the exact layout of the complex multi-module integration and dorsal ATM mechanism
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-453h // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // SKYLAB ORBITAL WORKSHOP", color=C_OWS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_SOLAR, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: S-IVB HULL / APOLLO TELESCOPE MOUNT / ASYMMETRICAL SOLAR ARRAY", color=C_ATM, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-453h: SKYLAB ORBITAL WORKSHOP TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
