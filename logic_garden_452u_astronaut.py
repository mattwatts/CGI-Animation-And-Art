"""
PROJECT: Logic Garden 452u (Exact Physical Construct // Astronaut (EMU) Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: ASTRONAUT, EMU, EVA SUIT, NASA, GLB, WIREFRAME, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional 1.9m bipedal scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Hard Upper Torso (HUT), PLSS Engine, TMG Ribbed Appendages, Visor Matrix.
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
OUT_DIR = "frames_452u_astronaut"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Orbital Tracking Grid)

C_SUIT      = '#0F172A'          # Abyssal Slate (TMG Suit Integrity / Dark-Contrast Baseline)
C_VISOR     = '#CA8A04'          # Kapton Gold (Polycarbonate Outer Sun Visor)
C_PLSS      = '#1E293B'          # Carbon Slate (Primary Life Support System Backpack)
C_HARDWARE  = '#334155'          # Heavy Slate (Neck Ring / Remote Control Unit / Boots)
C_STRIPE    = '#E11D48'          # Kinematic Red (Commander Identifier Banding)

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
    # Biological Mirroring across the Y-axis (Port / Starboard Limbs)
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
        if axis == 'x':  ix, iy, iz = np.full_like(t, cx + s), cy + radius*np.cos(t), cz + radius*np.sin(t)
        elif axis == 'y':ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + s), cz + radius*np.sin(t)
        else:            ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), np.full_like(t, cz + s)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        if axis == 'x':  sx, sy, sz = cx + steps, [cy + radius*np.cos(a)]*rings, [cz + radius*np.sin(a)]*rings
        elif axis == 'y':sx, sy, sz = [cx + radius*np.cos(a)]*rings, cy + steps, [cz + radius*np.sin(a)]*rings
        else:            sx, sy, sz = [cx + radius*np.cos(a)]*rings, [cy + radius*np.sin(a)]*rings, cz + steps
        append_segmented(lines_dict, col, sx, sy, sz)

def add_ellipsoid(lines_dict, col, cx, cy, cz, rx, ry, rz, rings=8, t_count=16):
    theta = np.linspace(-np.pi/2, np.pi/2, rings)
    phi = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    for th in theta:
        xs = cx + rx * np.cos(th) * np.cos(phi)
        ys = cy + ry * np.cos(th) * np.sin(phi)
        zs = cz + rz * np.sin(th) * np.ones_like(phi)
        append_segmented(lines_dict, col, list(xs)+[xs[0]], list(ys)+[ys[0]], list(zs)+[zs[0]])
    for ph in phi:
        xs = cx + rx * np.cos(theta) * np.cos(ph)
        ys = cy + ry * np.cos(theta) * np.sin(ph)
        zs = cz + rz * np.sin(theta)
        append_segmented(lines_dict, col, xs, ys, zs)

def add_sym_ribbed_strut(lines_dict, col, x0, y0, z0, x1, y1, z1, r_main, r_rib, splits, t_count=12):
    """ Custom TMG pressure-bladder pipeline mapping. Forces ribbed modulation along the structural vector. """
    dx, dy, dz = x1-x0, y1-y0, z1-z0
    L = np.sqrt(dx**2 + dy**2 + dz**2)
    if L < 0.001: return
    ux, uy, uz = dx/L, dy/L, dz/L
    
    # Orthogonal projection basis
    if abs(uz) < 0.99:
        nx, ny, nz = -uy, ux, 0
    else:
        nx, ny, nz = 0, -uz, uy
    nL = np.sqrt(nx**2 + ny**2 + nz**2)
    nx, ny, nz = nx/nL, ny/nL, nz/nL
    bx, by, bz = uy*nz - uz*ny, uz*nx - ux*nz, ux*ny - uy*nx
    
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, L, splits)
    
    for i, s in enumerate(steps):
        # Alternate radius mathematically for severe mechanical ribbing
        rad = r_rib if i%2 == 0 else r_main
        cx, cy, cz = x0 + ux*s, y0 + uy*s, z0 + uz*s
        ring_x = cx + rad * (np.cos(t)*nx + np.sin(t)*bx)
        ring_y = cy + rad * (np.cos(t)*ny + np.sin(t)*by)
        ring_z = cz + rad * (np.cos(t)*nz + np.sin(t)*bz)
        append_sym(lines_dict, col, list(ring_x)+[ring_x[0]], list(ring_y)+[ring_y[0]], list(ring_z)+[ring_z[0]])
        
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        qx = x0 + steps*ux + r_main*(np.cos(a)*nx + np.sin(a)*bx)
        qy = y0 + steps*uy + r_main*(np.cos(a)*ny + np.sin(a)*by)
        qz = z0 + steps*uz + r_main*(np.cos(a)*nz + np.sin(a)*bz)
        append_sym(lines_dict, col, qx, qy, qz)

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (ASTRONAUT / EMU)
# ------------------------------------------------------------------
def generate_astronaut_static():
    lines = {
        'C_SUIT': [], 'C_VISOR': [], 'C_PLSS': [],
        'C_HARDWARE': [], 'C_STRIPE': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. CELESTIAL TRACKING BASEPLATE (1 Unit = 1 Metre)
    # ==============================================================================
    Z_FLOOR = 0.0
    for r_p in [0.5, 1.0, 1.5]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-1.5, 1.5, 13)
    gy_range = np.linspace(-1.5, 1.5, 13)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. HELMET & VISOR MATRIX
    # ==============================================================================
    # Main Polycarbonate/Fiberglass shell (shifted rearward)
    add_ellipsoid(lines, 'C_SUIT', cx=-0.05, cy=0.0, cz=1.75, rx=0.15, ry=0.14, rz=0.14, rings=7, t_count=12)
    # Kapton Gold internal sun visor projecting cleanly out of the forward envelope
    add_ellipsoid(lines, 'C_VISOR', cx=0.02, cy=0.0, cz=1.75, rx=0.14, ry=0.13, rz=0.13, rings=7, t_count=12)
    
    # Heavy Neck Locking Ring
    add_cylinder(lines, 'C_HARDWARE', cx=0.0, cy=0.0, cz=1.55, length=0.05, radius=0.15, axis='z', rings=2, t_count=16)

    # ==============================================================================
    # 3. EMU HARD UPPER TORSO (HUT) & PRIMARY LIFE SUPPORT (PLSS)
    # ==============================================================================
    # Fiberglass Chest Block
    add_box_mesh(lines, 'C_SUIT', -0.15, 0.15, -0.22, 0.22, 1.15, 1.55, div=4)
    # Remote Control Unit (RCU) on chest via physical telemetry manifold block
    add_box_mesh(lines, 'C_HARDWARE', 0.15, 0.22, -0.12, 0.12, 1.15, 1.35, div=2)
    
    # Massive Aft-Mounted PLSS Subsystem backpack
    add_box_mesh(lines, 'C_PLSS', -0.4, -0.15, -0.2, 0.2, 1.0, 1.6, div=4)
    
    # Waist Bearing Assembly
    add_cylinder(lines, 'C_HARDWARE', cx=0.0, cy=0.0, cz=1.1, length=0.05, radius=0.18, axis='z', rings=2, t_count=16)
    
    # Lower Torso Subsystem (LTA Base)
    add_ellipsoid(lines, 'C_SUIT', cx=0.0, cy=0.0, cz=1.0, rx=0.15, ry=0.2, rz=0.1, rings=4, t_count=16)

    # ==============================================================================
    # 4. TMG PIPELINE COMPILATION (APPENDAGES)
    # ==============================================================================
    # Providing purely symmetrical single-side generation. The bare-metal add_sym_ribbed_strut
    # handles autonomous mirroring across the precise Y-axis boundary.
    
    # --- ARMS ---
    # Shoulder joint -> Elbow
    add_sym_ribbed_strut(lines, 'C_SUIT', 0.0, 0.25, 1.45,  0.1, 0.35, 1.15, r_main=0.07, r_rib=0.08, splits=12, t_count=10)
    # Commander Red Stripe ID Block (Upper Bicep overlay)
    add_sym_ribbed_strut(lines, 'C_STRIPE', 0.05, 0.30, 1.30, 0.06, 0.31, 1.27, r_main=0.082, r_rib=0.082, splits=2, t_count=12)
    # Forearm
    add_sym_ribbed_strut(lines, 'C_SUIT', 0.1, 0.35, 1.15,  0.2, 0.3, 0.85, r_main=0.06, r_rib=0.07, splits=10, t_count=10)
    # Heavy EMU EVA Glove
    add_sym_ribbed_strut(lines, 'C_HARDWARE', 0.2, 0.3, 0.85, 0.25, 0.3, 0.7, r_main=0.05, r_rib=0.055, splits=3, t_count=8)

    # --- LEGS ---
    # Hip joint -> Knee
    add_sym_ribbed_strut(lines, 'C_SUIT', 0.0, 0.15, 0.9,  0.1, 0.15, 0.45, r_main=0.09, r_rib=0.10, splits=14, t_count=12)
    # Commander Red Stripe ID Block (Thigh overlay)
    add_sym_ribbed_strut(lines, 'C_STRIPE', 0.05, 0.15, 0.67, 0.06, 0.15, 0.63, r_main=0.102, r_rib=0.102, splits=2, t_count=12)
    # Calf -> Ankle
    add_sym_ribbed_strut(lines, 'C_SUIT', 0.1, 0.15, 0.45, 0.0, 0.15, 0.1, r_main=0.08, r_rib=0.09, splits=12, t_count=12)
    # Rigid Magnetic/Terrain Boot
    add_sym_ribbed_strut(lines, 'C_HARDWARE', -0.05, 0.15, 0.08, 0.2, 0.15, 0.02, r_main=0.06, r_rib=0.07, splits=4, t_count=8)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_astronaut_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry flawlessly at waist-level centroid
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.9
        
        # Starts explicitly from 115-degrees (Dramatic aesthetic exposing the PLSS backpack and forward visor)
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
    # Anchor Centroid = Z=0.9m. Total bipedal envelope ranges from Z=0.0 to Z=1.9. Overhangs minimal.
    # Setting cam_span strictly to 1.3 locks horizontal width symmetrically across a 2.6m view.
    # Vertical bounds output 1.3 * 1.777 = 2.31m total height (extends +/- 2.31m from waist, netting Z=-1.41 to Z=3.21).
    # Completely traps the 1.9m Astronaut safely inside the transparent viewport, immune to UI overlay clipping.
    cam_span = 1.3
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_SUIT',      C_SUIT,      1.2, 1.0),
        ('C_HARDWARE',  C_HARDWARE,  1.4, 1.0),
        ('C_PLSS',      C_PLSS,      1.3, 1.0),
        ('C_STRIPE',    C_STRIPE,    1.8, 1.0),
        ('C_VISOR',     C_VISOR,     1.6, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to parse the exact layout of the chest RCU manifold against the visor
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-452u // MACRO-ENGINEERING TENSOR: EXTRAVEHICULAR KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // 1.9M ASTRONAUT EMU (EVA SUIT)", color=C_HARDWARE, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_STRIPE, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: TMG BLADDERS / HUT / PLSS / COMMANDER DESIGNATION", color=C_VISOR, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-452u: ASTRONAUT (EMU) TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace/Biomedical Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
