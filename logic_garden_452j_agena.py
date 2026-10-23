"""
PROJECT: Logic Garden 452j (Exact Physical Construct // Agena Target Vehicle Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: AGENA, TARGET VEHICLE, GEMINI, GLB, WIREFRAME, ENGINEERING, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional 7.92m aerospace scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Agena-D hull, Target Docking Adapter (TDA), L-Band Booms, and Bell 8247 Engine.
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
OUT_DIR = "frames_452j_agena"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Orbital Tracking Grid)

C_HULL_MAIN = '#94A3B8'          # Heavy Slate (Agena-D Primary Hull)
C_HULL_DARK = '#1E293B'          # Carbon Slate (Docking Adapter / Thermal Shroud)
C_GOLD      = '#CA8A04'          # Kapton Gold (L-Band Booms / Helical Antennas)
C_HARDWARE  = '#0F172A'          # Abyssal Slate (Index Cones / Aft Rack)
C_ENGINE    = '#E11D48'          # Kinematic Red (Bell 8247 Thrust Frame)

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
def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='x', rings=4, t_count=16):
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

def add_cone_frustum(lines_dict, col, cx, cy, cz, dz, r1, r2, axis='x', rings=4, t_count=16):
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
# SUPERSTRUCTURE BUILDERS (AGENA TARGET VEHICLE)
# ------------------------------------------------------------------
def generate_atv_static():
    lines = {
        'C_HULL_MAIN': [], 'C_HULL_DARK': [], 'C_GOLD': [],
        'C_HARDWARE': [], 'C_ENGINE': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. ORBITAL TRACKING BASEPLATE (1 Unit = 1 Metre)
    # ==============================================================================
    Z_FLOOR = -2.5
    for r_p in [4.0, 8.0, 12.0]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-12.0, 12.0, 13)
    gy_range = np.linspace(-12.0, 12.0, 13)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. AGENA-D PRIMARY HULL METRICS (~1.52m Diameter)
    # ==============================================================================
    R_BODY = 0.76
    X_AFT = -5.0
    
    # Main Propellant Tanks / Hull Core
    add_cylinder(lines, 'C_HULL_MAIN', cx=X_AFT, cy=0.0, cz=0.0, length=5.5, radius=R_BODY, axis='x', rings=14, t_count=32)

    # ==============================================================================
    # 3. TARGET DOCKING ADAPTER (TDA)
    # ==============================================================================
    # Forward Shroud transitioning to docking cone
    add_cylinder(lines, 'C_HULL_DARK', cx=0.5, cy=0.0, cz=0.0, length=1.0, radius=R_BODY, axis='x', rings=4, t_count=32)
    
    # Outer rigid docking cone (Tapering violently toward X=2.4)
    add_cone_frustum(lines, 'C_HULL_DARK', cx=1.5, cy=0.0, cz=0.0, dz=0.9, r1=R_BODY, r2=0.4, axis='x', rings=5, t_count=32)
    
    # Inner Indexing Mooring Cone (Reversed slope forcing Gemini alignment)
    add_cone_frustum(lines, 'C_HARDWARE', cx=2.4, cy=0.0, cz=0.0, dz=-0.6, r1=0.4, r2=0.2, axis='x', rings=4, t_count=16)

    # ==============================================================================
    # 4. TELEMETRY ARRAY & ASYMMETRIC BOOMS
    # ==============================================================================
    # Dual spiralled L-Band / S-Band Radar Antennas protruding laterally from the TDA
    add_cylinder(lines, 'C_GOLD', cx=1.2, cy=R_BODY, cz=0.0, length=1.6, radius=0.03, axis='x', rings=3, t_count=6)
    add_cylinder(lines, 'C_GOLD', cx=1.2, cy=-R_BODY, cz=0.0, length=1.6, radius=0.03, axis='x', rings=3, t_count=6)
    
    # High-Gain Helix node
    add_cylinder(lines, 'C_HARDWARE', cx=2.8, cy=R_BODY, cz=0.0, length=0.1, radius=0.08, axis='x', rings=2, t_count=8)
    add_cylinder(lines, 'C_HARDWARE', cx=2.8, cy=-R_BODY, cz=0.0, length=0.1, radius=0.08, axis='x', rings=2, t_count=8)

    # ==============================================================================
    # 5. AFT EQUIPMENT RACK & PROPULSION
    # ==============================================================================
    # Rear Structural Equipment Rack (Mounts SPS and Attitude Control Systems)
    add_cylinder(lines, 'C_HARDWARE', cx=-5.5, cy=0.0, cz=0.0, length=0.5, radius=R_BODY-0.05, axis='x', rings=3, t_count=24)
    
    # SPS Thruster Pods (Lateral Mounts)
    add_cylinder(lines, 'C_HARDWARE', cx=-5.3, cy=R_BODY-0.05, cz=0.0, length=0.5, radius=0.15, axis='y', rings=3, t_count=12)
    add_cylinder(lines, 'C_HARDWARE', cx=-5.3, cy=-R_BODY-0.45, cz=0.0, length=0.5, radius=0.15, axis='y', rings=3, t_count=12)
    
    # Main Engine: Bell Aerosystems Model 8247
    # Executing backward thrust bell using negative spatial integration (Z = -1.2m)
    add_cone_frustum(lines, 'C_ENGINE', cx=-5.5, cy=0.0, cz=0.0, dz=-1.2, r1=0.25, r2=0.55, axis='x', rings=5, t_count=24)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_atv_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking focal geometry flawlessly at payload centre (X = -1.5m)
        cam_x, cam_y, cam_z = -1.5, 0.0, 0.0
        
        # Starts explicitly from 115-degrees (Dramatic aesthetic exposing the massive TDA cone and asymmetric booms)
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
    # Anchor Centroid = X = -1.5m. Total vehicle length is roughly 7.92 metres.
    # Setting cam_span strictly to 7.0 locks horizontal width symmetrically across an immense 14.0m.
    # Vertical bounds output 7.0 * 1.777 = 12.43m total height window vertically.
    # Completely traps the space vehicle safely inside the transparent viewport, immune to UI overlay clipping.
    cam_span = 7.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.4), 
        ('C_HULL_MAIN', C_HULL_MAIN, 1.2, 1.0),
        ('C_HULL_DARK', C_HULL_DARK, 1.4, 1.0),
        ('C_HARDWARE',  C_HARDWARE,  1.3, 1.0),
        ('C_GOLD',      C_GOLD,      1.5, 1.0),
        ('C_ENGINE',    C_ENGINE,    1.6, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +15 degrees to clearly render the interior indexing cone and the Bell 8247 thrust chamber
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
    ax.add_patch(patches.Rectangle((-cam_span, ui_t), cam_span*2, cam_span*0.5, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_t, ui_t], color=C_TEXT, lw=6, zorder=81)

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-452j // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // AGENA TARGET VEHICLE (NASA GEMINI)", color=C_HULL_DARK, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_GOLD, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: AGENA-D HULL / TARGET DOCKING ADAPTER / BELL 8247 ENGINE", color=C_HULL_MAIN, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-452j: AGENA TARGET VEHICLE TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
