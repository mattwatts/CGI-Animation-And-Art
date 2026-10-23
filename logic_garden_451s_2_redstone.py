"""
PROJECT: Logic Garden 451s (Exact Physical Construct // Redstone 3 'Freedom 7' Matrix) - REVISION
FORMAT: YouTube Shorts (1080x1920)
METADATA: REDSTONE, MERCURY, FREEDOM 7, NASA, WIREFRAME, ENGINEERING, KINEMATICS, AEROSPACE
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional 26.0m aerospace scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: A-7 Engine, Redstone Booster, Tapered Adapter, Mercury Capsule, LES Tower.
- Viewport Override: Aggressive cam_span recalculation guarantees 100% total vehicle visibility between UI boundaries.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from 115-degree dramatic front-quarter angle.
- Daylight Palette (White Substrate / High-Contrast Edge Geometry).
- Purged Jargon. Australian spelling conventions (maths, colour, kilometres, synchronisation).
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
OUT_DIR = "frames_451s_redstone"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Launch Pad Reference Baseplate)

C_HULL_MAIN = '#94A3B8'          # Slate Aluminium (Primary Rocket Subsurface)
C_STRIPES   = '#111115'          # Indestructible Black (Roll Pattern Markings explicitly modeled)
C_CAPSULE   = '#1E293B'          # Carbon Slate (Corrugated Mercury Spacecraft vessel)
C_LES       = '#E11D48'          # Kinematic Red (Launch Escape System Tower & Motor)
C_ENGINE    = '#334155'          # Heavy Slate (A-7 Thrust Bell & Retropack)
C_FINS      = '#0F172A'          # Abyssal Slate (Aerodynamic Steering Fins & Rudders)

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

def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='z', rings=4, t_count=16):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, length, rings)
    for s in steps:
        if axis == 'z':
            ix = cx + radius*np.cos(t); iy = cy + radius*np.sin(t); iz = np.full_like(t, cz + s)
        elif axis == 'x':
            ix = np.full_like(t, cx + s); iy = cy + radius*np.cos(t); iz = cz + radius*np.sin(t)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        if axis == 'z':
            sx = np.full_like(steps, cx + radius*np.cos(a))
            sy = np.full_like(steps, cy + radius*np.sin(a))
            sz = cz + steps
        elif axis == 'x':
            sx = cx + steps
            sy = np.full_like(steps, cy + radius*np.cos(a))
            sz = np.full_like(steps, cz + radius*np.sin(a))
        append_segmented(lines_dict, col, list(sx), list(sy), list(sz))

def add_cone_frustum(lines_dict, col, cx, cy, cz, dz, r1, r2, axis='z', rings=4, t_count=16):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, dz, rings)
    r_step = np.linspace(r1, r2, rings)
    for i, s in enumerate(steps):
        r = r_step[i]
        iz = np.full_like(t, cz + s)
        ix = cx + r*np.cos(t); iy = cy + r*np.sin(t)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        sx, sy, sz = [], [], []
        for i, s in enumerate(steps):
            r = r_step[i]
            sx.append(cx + r*np.cos(a)); sy.append(cy + r*np.sin(a)); sz.append(cz + s)
        append_segmented(lines_dict, col, sx, sy, sz)

def add_truss(lines_dict, col, p1, p2, radius, sections=10):
    # Specialized high-density 3-point lattice (Mercury LES Tower format)
    p1, p2 = np.array(p1), np.array(p2)
    v = p2 - p1
    length = np.linalg.norm(v)
    if length < 0.001: return
    v_dir = v / length
    not_v = np.array([1.0, 0.0, 0.0])
    if abs(np.dot(v_dir, not_v)) > 0.99: not_v = np.array([0.0, 1.0, 0.0])
    n1 = np.cross(v_dir, not_v)
    n1 /= np.linalg.norm(n1)
    n2 = np.cross(v_dir, n1)
    
    t_angles = [0, 2*np.pi/3, 4*np.pi/3] # Strict Triangular cross-section
    nodes = []
    steps = np.linspace(0, length, sections)
    
    for s in steps:
        sec_nodes = []
        for a in t_angles:
            nx = radius * (np.cos(a)*n1[0] + np.sin(a)*n2[0])
            ny = radius * (np.cos(a)*n1[1] + np.sin(a)*n2[1])
            nz = radius * (np.cos(a)*n1[2] + np.sin(a)*n2[2])
            sec_nodes.append([p1[0] + nx + v_dir[0]*s, 
                              p1[1] + ny + v_dir[1]*s, 
                              p1[2] + nz + v_dir[2]*s])
        nodes.append(sec_nodes)
        
    for c in range(3):
        xs = [n[c][0] for n in nodes]; ys = [n[c][1] for n in nodes]; zs = [n[c][2] for n in nodes]
        append_segmented(lines_dict, col, xs, ys, zs)
        
    for i in range(sections - 1):
        for c in range(3):
            nx_c = (c+1)%3
            append_segmented(lines_dict, col, [nodes[i][c][0], nodes[i+1][nx_c][0]],
                                              [nodes[i][c][1], nodes[i+1][nx_c][1]],
                                              [nodes[i][c][2], nodes[i+1][nx_c][2]])

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (REDSTONE 3 STACK)
# ------------------------------------------------------------------
def generate_redstone_static():
    lines = {
        'C_HULL_MAIN': [], 'C_STRIPES': [], 'C_CAPSULE': [], 
        'C_LES': [], 'C_ENGINE': [], 'C_FINS': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. LAUNCH PAD / REFERENCE BASEPLATE
    # ==============================================================================
    Z_FLOOR = 0.0
    for r_p in [1.5, 3.0, 5.0]:
        t_p = np.linspace(0, 2*np.pi, 48, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-6.0, 6.0, 13)
    gy_range = np.linspace(-6.0, 6.0, 13)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. A-7 ENGINE & REDSTONE BOOSTER TAIL SECTION
    # ==============================================================================
    R_1 = 0.89  # 1.78m exact diameter
    Z_TAIL_TOP = 2.8
    
    # A-7 Thrust Bell Extruding Below Chassis
    add_cone_frustum(lines, 'C_ENGINE', 0.0, 0.0, Z_FLOOR, 1.2, r1=0.6, r2=0.2, rings=4, t_count=20)
    
    # Base Tail Unit containing steering mechanisms
    add_cylinder(lines, 'C_STRIPES', 0.0, 0.0, 1.2, (Z_TAIL_TOP - 1.2), R_1, rings=4, t_count=24)

    # Four aerodynamic fins with explicit boundary meshes
    fin_angles = [np.pi/4, 3*np.pi/4, 5*np.pi/4, 7*np.pi/4]
    for a in fin_angles:
        fin_root_r = R_1; fin_tip_r = R_1 + 1.25
        f_bx1 = fin_root_r * np.cos(a); f_by1 = fin_root_r * np.sin(a)
        f_bx2 = fin_tip_r * np.cos(a);  f_by2 = fin_tip_r * np.sin(a)
        f_tx1 = fin_root_r * np.cos(a); f_ty1 = fin_root_r * np.sin(a)
        
        # Lower fixed fin
        add_quad_mesh(lines, 'C_FINS', (f_bx1, f_by1, 1.2), (f_bx2, f_by2, 1.2), (f_bx2, f_by2, 2.5), (f_tx1, f_ty1, 3.8), u_steps=2, v_steps=3)
        # Rudder extension (dropped below the fin line for exhaust impingement steering)
        add_quad_mesh(lines, 'C_FINS', (f_bx2, f_by2, 0.5), (fin_tip_r*1.1*np.cos(a), fin_tip_r*1.1*np.sin(a), 0.5), 
                                       (fin_tip_r*1.1*np.cos(a), fin_tip_r*1.1*np.sin(a), 1.2), (f_bx2, f_by2, 1.2), u_steps=1, v_steps=2)

    # ==============================================================================
    # 3. REDSTONE MAIN PROPELLANT TANK (ROLL PATTERNS)
    # ==============================================================================
    Z_TANK_END = 16.5
    # The tank is painted in strict alternating bounds for longitudinal tracking analysis
    bands = [
        (2.8, 5.5, 'C_STRIPES'),
        (5.5, 8.2, 'C_HULL_MAIN'),
        (8.2, 10.9, 'C_STRIPES'),
        (10.9, 13.6, 'C_HULL_MAIN'),
        (13.6, 16.5, 'C_STRIPES')
    ]
    for z_start, z_end, col in bands:
        add_cylinder(lines, col, 0.0, 0.0, z_start, (z_end - z_start), R_1, rings=4, t_count=24)

    # ==============================================================================
    # 4. INSTRUMENT COMPARTMENT & ADAPTER
    # ==============================================================================
    Z_ADAPTER_TOP = 18.0
    R_CAPSULE_BASE = 0.945 # The Mercury capsule requires an extruded tapering ring (74.5 inches)
    
    # Expanding structural frustum adapting the 1.78m booster to the 1.89m payload
    add_cone_frustum(lines, 'C_HULL_MAIN', 0.0, 0.0, Z_TANK_END, (Z_ADAPTER_TOP - Z_TANK_END), r1=R_1, r2=R_CAPSULE_BASE, rings=5, t_count=24)

    # ==============================================================================
    # 5. MERCURY CAPSULE (FREEDOM 7)
    # ==============================================================================
    Z_RETRO_TOP = 18.25
    Z_CABIN_TOP = 20.25
    Z_REC_TOP = 21.0
    Z_ANT_TOP = 21.5
    R_HATCH = 0.35
    R_ANT = 0.25

    # Retropack / Heatshield
    add_cylinder(lines, 'C_ENGINE', 0.0, 0.0, Z_ADAPTER_TOP, (Z_RETRO_TOP - Z_ADAPTER_TOP), R_CAPSULE_BASE-0.05, rings=2, t_count=24)

    # Primary Conical Crew Cabin (Heavy corrugated mapping)
    add_cone_frustum(lines, 'C_CAPSULE', 0.0, 0.0, Z_RETRO_TOP, (Z_CABIN_TOP - Z_RETRO_TOP), r1=R_CAPSULE_BASE, r2=R_HATCH, rings=8, t_count=32)

    # Cylindrical Recovery Compartment (Parachute housing)
    add_cylinder(lines, 'C_CAPSULE', 0.0, 0.0, Z_CABIN_TOP, (Z_REC_TOP - Z_CABIN_TOP), R_HATCH, rings=3, t_count=16)

    # Tapered Antenna Fairing
    add_cone_frustum(lines, 'C_CAPSULE', 0.0, 0.0, Z_REC_TOP, (Z_ANT_TOP - Z_REC_TOP), r1=R_HATCH, r2=R_ANT, rings=3, t_count=16)

    # ==============================================================================
    # 6. LAUNCH ESCAPE SYSTEM (LES) TOWER
    # ==============================================================================
    Z_TOWER_TOP = 24.5
    Z_MOTOR_TOP = 25.4
    Z_SPIKE_TOP = 26.0

    # 3-Strut lattice tower anchoring physically into the capsule apex
    add_truss(lines, 'C_LES', (0.0, 0.0, Z_ANT_TOP), (0.0, 0.0, Z_TOWER_TOP), radius=R_ANT, sections=6)

    # Solid Rocket Escort Motor (Red)
    add_cylinder(lines, 'C_LES', 0.0, 0.0, Z_TOWER_TOP, (Z_MOTOR_TOP - Z_TOWER_TOP), 0.15, rings=4, t_count=12)

    # Aerodynamic Control Spike
    add_cone_frustum(lines, 'C_LES', 0.0, 0.0, Z_MOTOR_TOP, (Z_SPIKE_TOP - Z_MOTOR_TOP), r1=0.15, r2=0.02, rings=3, t_count=8)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_redstone_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking the vertical focal geometry to dead centre of the 26.0m dimension
        cam_x, cam_y, cam_z = 0.0, 0.0, 13.0
        
        # Starts explicitly from 115-degrees (Dramatic front-quarter aesthetic tracking the heavy launch engines)
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

    # 100% VISIBILITY THRESHOLD AUDIT (HUD BYPASS PARITY):
    # Anchor Centroid = 13.0m high. Total vertical geometry spanning 0m to 26.0m precisely.
    # We must unconditionally prevent the HUD arrays from occluding the upper LES tower and lower extreme fins.
    # Setting cam_span forcefully to 10.0 ensures the view bracket spans 14.5m upwards and 14.27m downwards 
    # strictly BETWEEN the top and bottom UI banners respectively. Total unclipped vertical visibility = 28.77m.
    cam_span = 10.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.6, 0.4), 
        ('C_HULL_MAIN', C_HULL_MAIN, 1.2, 1.0),
        ('C_STRIPES',   C_STRIPES,   1.5, 1.0),
        ('C_CAPSULE',   C_CAPSULE,   1.6, 1.0),
        ('C_ENGINE',    C_ENGINE,    1.4, 1.0),
        ('C_FINS',      C_FINS,      1.4, 1.0),
        ('C_LES',       C_LES,       1.5, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +10 degrees to effectively map the tapered geometry across the long Z-axis footprint
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=10.0)
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-451s_REV // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // REDSTONE 3 (FREEDOM 7) MATRIX", color=C_STRIPES, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_CAPSULE, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: 100% UNCLIPPED HORIZON / A-7 ENGINE / CAPSULE / LES", color=C_LES, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-451s_REV: REDSTONE 3 AEROSPACE TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
