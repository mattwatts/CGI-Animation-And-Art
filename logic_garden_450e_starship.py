"""
PROJECT: Logic Garden 450e (Exact Physical Construct // SpaceX Starship Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: SPACEX, STARSHIP, ROCKET, AEROSPACE, WIREFRAME, ENGINEERING, KINEMATICS, MARS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: True parametric 50m hull, explicit ogive nose curve, internal bulkheads/downcomer, 6x Raptor engine array, and dynamic aerodynamic flaps.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from absolute flap-deployed frontal profile.
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
OUT_DIR = "frames_450e_starship"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Baseplate Reference)
C_ENGINE    = '#111115'          # Indestructible Black (Raptor Thrust Bells)

C_HULL      = '#1E293B'          # Carbon Slate (Primary Stainless Steel Skin)
C_AERO      = '#475569'          # Machined Slate (Flaps & Control Surfaces)
C_TANK      = '#005599'          # Deep Marine (Internal Pressure Domes & Downcomer)
C_FIRE      = '#D95F22'          # Industrial Amber (Engine Manifold Interfaces)

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
    for i in range(len(xs) - 1):
        x1 = xs[i] * scale_x + dx
        x2 = xs[i+1] * scale_x + dx
        lines_dict[key].append(([x1, x2], [ys[i]+dy, ys[i+1]+dy], [zs[i]+dz, zs[i+1]+dz]))

# ------------------------------------------------------------------
# GEOMETRIC PRIMITIVES
# ------------------------------------------------------------------
def extrude_profile(lines_dict, col, xz_points, y_min, y_max, close_loop=True, off=(0,0,0)):
    xs = [p[0] for p in xz_points]; zs = [p[1] for p in xz_points]
    if close_loop:
        xs.append(xs[0]); zs.append(zs[0])
    append_segmented(lines_dict, col, xs, [y_min]*len(xs), zs, off)
    append_segmented(lines_dict, col, xs, [y_max]*len(xs), zs, off)
    for x, z in xz_points:
        append_segmented(lines_dict, col, [x, x], [y_min, y_max], [z, z], off)

def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='z', rings=8, t_count=24, off=(0,0,0)):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, length, rings)
    for s in steps:
        if axis == 'y':   ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + s), cz + radius*np.sin(t)
        elif axis == 'x': ix, iy, iz = np.full_like(t, cx + s), cy + radius*np.cos(t), cz + radius*np.sin(t)
        else:             ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), np.full_like(t, cz + s)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]], off)
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        if axis == 'y':   sx, sy, sz = [cx + radius*np.cos(a)]*rings, cy + steps, [cz + radius*np.sin(a)]*rings
        elif axis == 'x': sx, sy, sz = cx + steps, [cy + radius*np.cos(a)]*rings, [cz + radius*np.sin(a)]*rings
        else:             sx, sy, sz = [cx + radius*np.cos(a)]*rings, [cy + radius*np.sin(a)]*rings, cz + steps
        append_segmented(lines_dict, col, sx, sy, sz, off)

def add_ogive(lines_dict, col, cx, cy, z_start, z_end, r_base, rings=12, t_count=24, off=(0,0,0)):
    z_steps = np.linspace(z_start, z_end, rings)
    # Parametric bullet drop to mathematically seal the nose
    ratio = (z_steps - z_start) / (z_end - z_start)
    r_steps = r_base * np.sqrt(np.clip(1.0 - (ratio)**2.2, 0.001, 1.0)) 
    
    for i in range(len(z_steps)):
        r, z = r_steps[i], z_steps[i]
        t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
        append_segmented(lines_dict, col, list(cx + r*np.cos(t))+[cx + r*np.cos(0)], list(cy + r*np.sin(t))+[cy + r*np.sin(0)], [z]*(t_count+1), off)
        
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        append_segmented(lines_dict, col, list(cx + r_steps*np.cos(a)), list(cy + r_steps*np.sin(a)), list(z_steps), off)

def add_dome(lines_dict, col, cx, cy, z_base, radius, up=True, rings=5, t_count=24, off=(0,0,0)):
    # Mathematical dome for internal pressurized bulkheads
    z_sign = 1.0 if up else -1.0
    dome_height = radius * 0.75 # Elliptical dome compression
    p_step = np.linspace(0, np.pi/2, rings)
    
    for p in p_step:
        r = radius * np.cos(p)
        z = z_base + z_sign * dome_height * np.sin(p)
        t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
        append_segmented(lines_dict, col, list(cx + r*np.cos(t))+[cx + r*np.cos(0)], list(cy + r*np.sin(t))+[cy + r*np.sin(0)], [z]*(t_count+1), off)
        
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        rr = radius * np.cos(p_step)
        zz = z_base + z_sign * dome_height * np.sin(p_step)
        append_segmented(lines_dict, col, list(cx + rr*np.cos(a)), list(cy + rr*np.sin(a)), list(zz), off)

def add_thrust_bell(lines_dict, col, cx, cy, cz, h, r_top, r_bot):
    steps = 5
    z_steps = np.linspace(cz, cz-h, steps)
    ratio = (cz - z_steps) / h
    # Swept bell curve nozzle
    r_steps = r_top + (r_bot - r_top) * (ratio**1.5)
    
    for i in range(steps):
        r, z = r_steps[i], z_steps[i]
        t = np.linspace(0, 2*np.pi, 12, endpoint=False)
        append_segmented(lines_dict, col, list(cx + r*np.cos(t))+[cx + r*np.cos(0)], list(cy + r*np.sin(t))+[cy + r*np.sin(0)], [z]*13)
        
    for a in np.linspace(0, 2*np.pi, 12, endpoint=False):
        append_segmented(lines_dict, col, list(cx + r_steps*np.cos(a)), list(cy + r_steps*np.sin(a)), list(z_steps))

# ------------------------------------------------------------------
# STATIC SUPERSTRUCTURE BUILDERS (STARSHIP ARCHITECTURE)
# ------------------------------------------------------------------
def generate_starship_static():
    lines = {
        'C_HULL': [], 'C_AERO': [], 'C_TANK': [], 'C_ENGINE': [], 
        'C_FIRE': [], 'C_GRID': []
    }

    # 1. BASEPLATE ENVELOPE (REFERENCE GRID)
    # Scaled to the 9m x 50m object bounds
    gx_range = np.linspace(-15.0, 15.0, 15)
    gy_range = np.linspace(-15.0, 15.0, 15)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.zeros_like(gy_range))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.zeros_like(gx_range))

    R_HULL = 4.5
    H_HULL = 36.28
    H_TOTAL = 50.0

    # ==============================================================================
    # 2. PRIMARY EXOSKELETON & NOSE CONE (The Stitched Rings)
    # ==============================================================================
    # Main constant-radius chassis extrusion
    add_cylinder(lines, 'C_HULL', 0, 0, 0, H_HULL, R_HULL, axis='z', rings=25, t_count=36)
    
    # Mathematical Ogive section capping
    add_ogive(lines, 'C_HULL', 0, 0, H_HULL, H_TOTAL, R_HULL, rings=16, t_count=36)

    # ==============================================================================
    # 3. INTERNAL VOLUMETRIC MECHANICS (Propellant Tanking Arrays)
    # ==============================================================================
    # Lower Methane Dome
    add_dome(lines, 'C_TANK', 0, 0, 3.54, R_HULL-0.1, up=True, rings=5, t_count=24)
    # Common Compartment Dome
    add_dome(lines, 'C_TANK', 0, 0, 16.14, R_HULL-0.1, up=True, rings=5, t_count=24)
    # Upper LOX Dome
    add_dome(lines, 'C_TANK', 0, 0, 27.14, R_HULL-0.1, up=True, rings=5, t_count=24)
    
    # Internal Header Spherical Tank
    add_dome(lines, 'C_TANK', 0, 0, 46.0, 1.3, up=True, rings=4)
    add_dome(lines, 'C_TANK', 0, 0, 46.0, 1.3, up=False, rings=4)

    # High-pressure Downcomer Tube (Routing fluid straight down through the core)
    add_cylinder(lines, 'C_TANK', 0.0, 1.5, 3.5, 27.14 - 3.5, 0.4, axis='z', rings=8, t_count=8)
    add_cylinder(lines, 'C_TANK', 0.0, 1.5, 30.0, 45.0 - 30.0, 0.2, axis='z', rings=5, t_count=6) # Upper slender feed

    # ==============================================================================
    # 4. EXPLICIT AERODYNAMIC CONTROL SURFACES (4x Canards/Flaps)
    # ==============================================================================
    thick = 0.2
    # AFT FLAPS (Sweeping outwards into the Y-planes)
    for sign in [-1, 1]:
        z_af_bot = 1.0; z_af_top = 16.14
        y_af_in = R_HULL*sign; y_af_out = (R_HULL + 4.2)*sign
        
        # Profile side coordinates mapping exact diagram dimensions
        flap_prof_x = [-0.5, 0.5, 0.5, -0.5]
        flap_prof_y = [y_af_out, y_af_out, y_af_in, y_af_in]
        flap_prof_z = [3.54, 3.54, z_af_top, z_af_top]
        
        # Upper angled sweep
        append_segmented(lines, 'C_AERO', [-0.5]*4, [y_af_out, y_af_in, y_af_in, y_af_out, y_af_out], [z_af_bot+1.0, z_af_bot, z_af_top, z_af_top-4.0, z_af_bot+1.0])
        append_segmented(lines, 'C_AERO', [ 0.5]*4, [y_af_out, y_af_in, y_af_in, y_af_out, y_af_out], [z_af_bot+1.0, z_af_bot, z_af_top, z_af_top-4.0, z_af_bot+1.0])
        # Connect thick ribs
        for i in range(4):
            ry = [y_af_out, y_af_in, y_af_in, y_af_out][i]
            rz = [z_af_bot+1.0, z_af_bot, z_af_top, z_af_top-4.0][i]
            append_segmented(lines, 'C_AERO', [-0.5, 0.5], [ry, ry], [rz, rz])
            
        # Additional surface detailing mesh
        for m_z in np.linspace(4.0, 11.0, 4):
            my = y_af_out - ((m_z - 4.0)/8.0)*4.2*sign
            append_segmented(lines, 'C_AERO', [-0.5, 0.5], [my]*2, [m_z]*2)

    # FORWARD FLAPS (Attached high on the shrinking nose cone)
    for sign in [-1, 1]:
        z_ff_bot = 37.0; z_ff_top = 45.0
        r_at_bot = R_HULL * np.sqrt(max(0.001, 1 - ((z_ff_bot - 36.28)/13.72)**2.2))
        r_at_top = R_HULL * np.sqrt(max(0.001, 1 - ((z_ff_top - 36.28)/13.72)**2.2))
        y_ff_out = (R_HULL + 3.0)*sign
        
        append_segmented(lines, 'C_AERO', [-0.3]*4, [y_ff_out, r_at_bot*sign, r_at_top*sign, y_ff_out, y_ff_out], [z_ff_bot+1.0, z_ff_bot, z_ff_top, z_ff_top-2.0, z_ff_bot+1.0])
        append_segmented(lines, 'C_AERO', [ 0.3]*4, [y_ff_out, r_at_bot*sign, r_at_top*sign, y_ff_out, y_ff_out], [z_ff_bot+1.0, z_ff_bot, z_ff_top, z_ff_top-2.0, z_ff_bot+1.0])
        for i in range(4):
            ry = [y_ff_out, r_at_bot*sign, r_at_top*sign, y_ff_out][i]
            rz = [z_ff_bot+1.0, z_ff_bot, z_ff_top, z_ff_top-2.0][i]
            append_segmented(lines, 'C_AERO', [-0.3, 0.3], [ry, ry], [rz, rz])

    # ==============================================================================
    # 5. HEX-ARRAY RAPTOR KINEMATICS (The Engine Bay)
    # ==============================================================================
    # 3x Sea Level Raptors (Gimballed cluster internally)
    dist_sl = 1.0
    for a in [0, 120, 240]:
        rad = np.radians(a)
        add_thrust_bell(lines, 'C_ENGINE', dist_sl*np.cos(rad), dist_sl*np.sin(rad), cz=0.0, h=1.5, r_top=0.3, r_bot=0.65)
        # Powerhead manifold plumbing
        append_segmented(lines, 'C_FIRE', [dist_sl*np.cos(rad), 0.0], [dist_sl*np.sin(rad), 0.0], [0.0, 3.5])

    # 3x Vacuum Raptors (Massive fixed bells extruded to exterior skirt radius)
    dist_vac = 2.8
    for a in [60, 180, 300]:
        rad = np.radians(a)
        add_thrust_bell(lines, 'C_ENGINE', dist_vac*np.cos(rad), dist_vac*np.sin(rad), cz=-0.5, h=2.5, r_top=0.5, r_bot=1.1)
        # Powerhead manifold plumbing
        append_segmented(lines, 'C_FIRE', [dist_vac*np.cos(rad), 0.0], [dist_vac*np.sin(rad), 0.0], [-0.5, 3.5])

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_starship_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        # Camera dynamically tracks the central 25m mechanical altitude
        cam_x, cam_y, cam_z = 0.0, 0.0, 23.0
        
        # Starts from absolute 0.0 looking down the X-axis (Displaying full Y-Flap Wingspan mapping)
        azimuth = 0.0 - (stage * 360.0)

        yield (f, t_sec, azimuth, cam_x, cam_y, cam_z, static_rig)

def render_frame(packet):
    f, t_sec, azimuth, cx, cy, cz, static_rig = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # Cinematic Rigid Map Boundary - Operating inside the massive 50m payload environment
    cam_span = 17.5
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',   C_GRID,   0.8, 0.3), 
        ('C_TANK',   C_TANK,   1.2, 0.8), # Translucent structural nodes exposing internals correctly
        ('C_ENGINE', C_ENGINE, 1.8, 1.0),
        ('C_FIRE',   C_FIRE,   1.5, 0.85),
        ('C_HULL',   C_HULL,   1.3, 1.0), 
        ('C_AERO',   C_AERO,   1.5, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Evaluated securely with absolute painter's depth-tracking vectorised matrix
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=8.0)
            render_queue.append((np.mean(depth), u, v, c_val, lw, alpha))

    # ABSOLUTE Z-SORT
    render_queue.sort(key=lambda item: item[0], reverse=True)
    for depth, u, v, c, lw, a in render_queue:
        ax.plot(u, v, color=c, lw=lw, alpha=a)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (TOP HUD)
    # ------------------------------------------------------------------
    ui_t = cam_span * 1.45
    ax.add_patch(patches.Rectangle((-cam_span, ui_t), cam_span*2, 12.0, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_t, ui_t], color=C_TEXT, lw=6, zorder=81)

    ax.text(-cam_span*0.95, ui_t+1.8, "LG-450e // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=19, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t+0.5, "EXPLICIT TRUE-SCALE GEOMETRY // STARSHIP ORBITAL MATRIX", color=C_HULL, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b+2.5, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_AERO, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+1.3, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.2, "TOPOLOGICAL YIELD: 50M HULL LIMIT & INTERNAL TANKING NETWORK", color=C_TANK, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-450e: STARSHIP KINEMATICS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
