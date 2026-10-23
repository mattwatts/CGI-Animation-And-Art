"""
PROJECT: Logic Garden 452n (Exact Physical Construct // AIM Satellite Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: AIM, SATELLITE, NASA, MESOSPHERE, GLB, WIREFRAME, ENGINEERING, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional 4.3m aerospace scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Octagonal bus, SOFIE optics, CIPS camera cluster, Photovoltaic Arrays.
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
OUT_DIR = "frames_452n_aim"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Orbital Tracking Grid)

C_BUS       = '#CA8A04'          # Kapton Gold (Octagonal Satellite Bus MLI)
C_PANELS    = '#005599'          # Deep Marine (Radial Photovoltaic Arrays)
C_SOFIE     = '#334155'          # Heavy Slate (SOFIE Optical Instrument)
C_CIPS      = '#475569'          # Machined Slate (CIPS Camera Cluster)
C_HARDWARE  = '#0F172A'          # Abyssal Slate (Telemetry Booms & S-Band Nodes)

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

def add_cone_frustum(lines_dict, col, cx, cy, cz, dz, r1, r2, axis='z', rings=4, t_count=16):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, dz, rings)
    r_step = np.linspace(r1, r2, rings)
    
    for i, s in enumerate(steps):
        r = r_step[i]
        if axis == 'x':  ix, iy, iz = np.full_like(t, cx + s), cy + r*np.cos(t), cz + r*np.sin(t)
        elif axis == 'y':ix, iy, iz = cx + r*np.cos(t), np.full_like(t, cy + s), cz + r*np.sin(t)
        else:            ix, iy, iz = cx + r*np.cos(t), cy + r*np.sin(t), np.full_like(t, cz + s)
        append_sym(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        sx, sy, sz = [], [], []
        for i, s in enumerate(steps):
            r = r_step[i]
            if axis == 'x':  sx.append(cx + s); sy.append(cy + r*np.cos(a)); sz.append(cz + r*np.sin(a))
            elif axis == 'y':sx.append(cx + r*np.cos(a)); sy.append(cy + s); sz.append(cz + r*np.sin(a))
            else:            sx.append(cx + r*np.cos(a)); sy.append(cy + r*np.sin(a)); sz.append(cz + s)
        append_sym(lines_dict, col, sx, sy, sz)

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (Aeronomy of Ice in the Mesosphere - AIM)
# ------------------------------------------------------------------
def generate_aim_static():
    lines = {
        'C_BUS': [], 'C_PANELS': [], 'C_SOFIE': [],
        'C_CIPS': [], 'C_HARDWARE': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. ORBITAL TRACKING BASEPLATE (1 Unit = 1 Metre)
    # ==============================================================================
    Z_FLOOR = -1.8
    for r_p in [1.5, 3.0, 4.5]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-4.5, 4.5, 13)
    gy_range = np.linspace(-4.5, 4.5, 13)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. SMEX SPACECRAFT PRIMARY BUS
    # ==============================================================================
    # ~1.2m tall octagonal core enveloped in Kapton MLI
    R_BUS = 0.55
    Z_AFT = -0.6
    Z_FWD = 0.6
    
    # Octagonal Chassis (Forced via t_count=8)
    add_cylinder(lines, 'C_BUS', cx=0.0, cy=0.0, cz=Z_AFT, length=(Z_FWD - Z_AFT), radius=R_BUS, axis='z', rings=5, t_count=8)

    # ==============================================================================
    # 3. FORWARD DECK SCIENCE INSTRUMENTS
    # ==============================================================================
    
    # [SOFIE] Solar Occultation For Ice Experiment
    # Massive tubular thermal housing protruding from +Z deck
    add_cylinder(lines, 'C_SOFIE', cx=0.25, cy=0.0, cz=Z_FWD, length=0.6, radius=0.18, axis='z', rings=4, t_count=12)
    # SOFIE Baffle
    add_cone_frustum(lines, 'C_SOFIE', cx=0.25, cy=0.0, cz=Z_FWD+0.6, dz=0.15, r1=0.18, r2=0.20, axis='z', rings=2, t_count=12)

    # [CIPS] Cloud Imaging and Particle Size
    # Quad-Camera Panoramic Cluster configured around the nadir block
    CIPS_OFFSETS = [
        (-0.25,  0.22),
        (-0.25, -0.22),
        ( 0.05,  0.35),
        ( 0.05, -0.35)
    ]
    # Mount Plate
    add_cylinder(lines, 'C_CIPS', cx=-0.1, cy=0.0, cz=Z_FWD, length=0.1, radius=0.4, axis='z', rings=2, t_count=8)
    
    for ox, oy in CIPS_OFFSETS:
        add_cone_frustum(lines, 'C_CIPS', cx=ox, cy=oy, cz=Z_FWD+0.1, dz=0.18, r1=0.08, r2=0.12, axis='z', rings=3, t_count=8)

    # [CDE] Cosmic Dust Experiment (Flat Interceptor Array)
    add_quad_mesh(lines, 'C_HARDWARE', 
                  (R_BUS+0.05, 0.2, Z_FWD), (R_BUS+0.05, -0.2, Z_FWD),
                  (R_BUS+0.05, -0.2, Z_FWD-0.4), (R_BUS+0.05, 0.2, Z_FWD-0.4),
                  u_steps=2, v_steps=2)

    # ==============================================================================
    # 4. TRANSVERSE PHOTOVOLTAIC SOLAR ARRAYS
    # ==============================================================================
    # Deployable solar wings along the Y-axis. ~4.3m total wingspan
    P_RAD_START = 0.65
    P_RAD_END = 2.15
    P_WIDTH_X = 0.5 
    
    # Y-axis Solar Flanks
    for sign in [-1, 1]:
        # Actuator / Drive Motor Housing
        add_cylinder(lines, 'C_HARDWARE', cx=0.0, cy=R_BUS*sign, cz=0.0, length=0.1*sign, radius=0.12, axis='y', rings=2, t_count=8)
        
        # Photovoltaic Array Base
        add_quad_mesh(lines, 'C_PANELS', 
                      (-P_WIDTH_X, P_RAD_START * sign, 0.0), (P_WIDTH_X, P_RAD_START * sign, 0.0),
                      (P_WIDTH_X, P_RAD_END * sign, 0.0), (-P_WIDTH_X, P_RAD_END * sign, 0.0), 
                      u_steps=4, v_steps=12)

    # ==============================================================================
    # 5. AFT TELEMETRY ANTENNAS (S-BAND)
    # ==============================================================================
    # Communications spikes protruding from the -Z (Aft) deck
    add_cylinder(lines, 'C_HARDWARE', cx=-0.2, cy=0.3, cz=Z_AFT, length=-0.4, radius=0.02, axis='z', rings=2, t_count=6)
    add_cylinder(lines, 'C_HARDWARE', cx=-0.2, cy=-0.3, cz=Z_AFT, length=-0.4, radius=0.02, axis='z', rings=2, t_count=6)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_aim_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry flawlessly at payload centroid
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.0
        
        # Starts explicitly from 115-degrees (Dramatic aesthetic exposing the CIPS and SOFIE payloads)
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
    # Anchor Centroid = Dead zero. Solar array extreme Y-bounds span exactly +/- 2.15m.
    # Setting cam_span strictly to 3.0 locks horizontal width symmetrically across a 6.0m view.
    # Vertical bounds output 3.0 * 1.777 = 5.331m total height window vertically.
    # Completely traps the space vehicle safely inside the transparent viewport, immune to UI overlay clipping.
    cam_span = 3.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_BUS',       C_BUS,       1.4, 1.0),
        ('C_PANELS',    C_PANELS,    1.2, 1.0),
        ('C_SOFIE',     C_SOFIE,     1.6, 1.0),
        ('C_CIPS',      C_CIPS,      1.5, 1.0),
        ('C_HARDWARE',  C_HARDWARE,  1.2, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to clearly parse the forward optical pipelines and lateral wings
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-452n // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // AERONOMY OF ICE IN THE MESOSPHERE (AIM)", color=C_BUS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_PANELS, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: OCTAGONAL SMEX BUS / SOFIE / CIPS MULTI-CAMERA ARRAY", color=C_CIPS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-452n: AIM TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
