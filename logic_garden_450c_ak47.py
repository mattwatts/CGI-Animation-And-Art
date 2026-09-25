"""
PROJECT: Logic Garden 450c (Exact Physical Construct // AK-47 Kinematic Architecture - HOTFIX)
FORMAT: YouTube Shorts (1080x1920)
METADATA: AK-47, AKM, RIFLE, FIREARM, WIREFRAME, ENGINEERING, KINEMATICS, MECHANICAL
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Natively swept magazine curve, explicit overhead gas-tube assembly, stamped receiver contours, and structural wooden furniture.
- Hotfix: Rectified numpy broadcast shape error by sequestering magazine tensor variables (mx_front, mx_rear), preserving the global scalar x_rear.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from absolute Side Profile.
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
OUT_DIR = "frames_450c_ak47"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Baseplate Reference)
C_BARREL    = '#111115'          # Indestructible Black (Primary Bore/Gas Tube/Sights/Rod)

C_RECEIVER  = '#1E293B'          # Carbon Slate (Stamped Steel Core & Dust Cover)
C_MAG       = '#475569'          # Machined Steel Slate (Swept 30-round magazine)
C_WOOD      = '#D95F22'          # Industrial Amber (Stock, Grip, Handguards)
C_PINS      = '#94A3B8'          # Polished Steel (Trigger, Pins, Rivets)

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

def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='x', rings=6, t_count=16, off=(0,0,0), half=False):
    t_end = np.pi if half else 2*np.pi
    t = np.linspace(0, t_end, t_count)
    steps = np.linspace(0, length, rings)
    for s in steps:
        if axis == 'y':  ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + s), cz + radius*np.sin(t)
        elif axis == 'x': ix, iy, iz = np.full_like(t, cx + s), cy + radius*np.cos(t), cz + radius*np.sin(t)
        else:             ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), np.full_like(t, cz + s)
        append_segmented(lines_dict, col, list(ix)+([ix[0]] if not half else []), 
                                          list(iy)+([iy[0]] if not half else []), 
                                          list(iz)+([iz[0]] if not half else []), off)
    for a in t[::max(1, t_count//8)]:
        if axis == 'y':   sx, sy, sz = [cx + radius*np.cos(a)]*rings, cy + steps, [cz + radius*np.sin(a)]*rings
        elif axis == 'x': sx, sy, sz = cx + steps, [cy + radius*np.cos(a)]*rings, [cz + radius*np.sin(a)]*rings
        else:             sx, sy, sz = [cx + radius*np.cos(a)]*rings, [cy + radius*np.sin(a)]*rings, cz + steps
        append_segmented(lines_dict, col, sx, sy, sz, off)

# ------------------------------------------------------------------
# STATIC SUPERSTRUCTURE BUILDERS (AK-47 / AKM ARCHITECTURE)
# ------------------------------------------------------------------
def generate_rifle_static():
    lines = {
        'C_RECEIVER': [], 'C_BARREL': [], 'C_WOOD': [], 'C_MAG': [], 
        'C_PINS': [], 'C_GRID': []
    }

    # 1. BASEPLATE ENVELOPE (REFERENCE GRID)
    # Absolute scale derived from 35-inch (880mm) global length 
    gx_range = np.linspace(-6.0, 6.0, 25)
    gy_range = np.linspace(-3.0, 3.0, 13)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gx_range, gx), np.clip(gx_range, -3.0, 3.0), np.zeros_like(gx_range))
    for gy in gy_range: append_segmented(lines, 'C_GRID', np.clip(gx_range, -6.0, 6.0), np.full_like(gx_range, gy), np.zeros_like(gx_range))

    # Core Parameters
    w_rec = 0.16   # Receiver half-width
    x_trun = 1.3   # Front trunnion X
    x_rear = -1.5  # Rear trunnion X (Explicit static scalar)

    # ==============================================================================
    # 2. STAMPED RECEIVER & DUST COVER
    # ==============================================================================
    rec_prof = [(x_trun, 0.4), (x_rear, 0.4), (x_rear, -0.2), (-0.4, -0.2), (0.2, -0.45), (x_trun, -0.3)]
    extrude_profile(lines, 'C_RECEIVER', rec_prof, -w_rec, w_rec)

    # Dust Cover (Curved overhead shell closing the gap)
    t = np.linspace(0, np.pi, 18)
    for x in np.linspace(x_rear+0.05, x_trun-0.05, 8):
        dy = w_rec * np.cos(t)
        dz = 0.4 + 0.3 * np.sin(t)
        # Ribbing explicit vectors
        append_segmented(lines, 'C_RECEIVER', np.full_like(t, x), list(dy), list(dz))
    for a in t[::2]:
        sy = w_rec * np.cos(a)
        append_segmented(lines, 'C_RECEIVER', [x_rear+0.05, x_trun-0.05], [sy, sy], [0.4 + 0.3*np.sin(a)]*2)

    # Right-hand Selector Lever Assymetry (+Y side only)
    append_segmented(lines, 'C_RECEIVER', [-0.5, 0.2, 0.2, -0.5], [w_rec+0.04]*4, [0.0, -0.25, -0.15, 0.1])
    add_cylinder(lines, 'C_PINS', -0.5, w_rec, 0.05, 0.08, 0.05, axis='y', rings=2) # Pivot pin

    # Trigger & Guard
    t_th = np.linspace(np.pi, 2*np.pi, 16)
    append_segmented(lines, 'C_RECEIVER', -0.1 + 0.3*np.cos(t_th), [-0.03]*16, -0.4 + 0.4*np.sin(t_th))
    append_segmented(lines, 'C_RECEIVER', -0.1 + 0.3*np.cos(t_th), [ 0.03]*16, -0.4 + 0.4*np.sin(t_th))
    # Trigger Shoe
    extrude_profile(lines, 'C_PINS', [(-0.15, -0.45), (-0.15, -0.65), (-0.05, -0.65), (-0.05, -0.45)], -0.06, 0.06)

    # ==============================================================================
    # 3. KINEMATIC SWEPT MAGAZINE (The "Banana" Math Vector)
    # ==============================================================================
    t_m = np.linspace(0, 1.0, 16)
    mx_front = 1.0 + 0.3*t_m + 0.8*t_m**2 # Geometrically sequestered to prevent scalar shadowing
    mx_rear  = 0.4 + 0.3*t_m + 0.8*t_m**2
    z_mag    = -0.4 - 2.5*t_m
    w_mag    = 0.14
    for y_sign in [-1, 1]:
        my = w_mag * y_sign
        append_segmented(lines, 'C_MAG', list(mx_front), [my]*16, list(z_mag)) # Front lip
        append_segmented(lines, 'C_MAG', list(mx_rear),  [my]*16, list(z_mag)) # Rear lip
        append_segmented(lines, 'C_MAG', [mx_rear[-1], mx_front[-1]], [my, my], [z_mag[-1], z_mag[-1]]) # Baseplate
    for i in range(16):
        append_segmented(lines, 'C_MAG', [mx_front[i]]*2, [-w_mag, w_mag], [z_mag[i]]*2)
        append_segmented(lines, 'C_MAG', [mx_rear[i]]*2, [-w_mag, w_mag], [z_mag[i]]*2)
    
    # Magazine structural ribs (Longitudinal lines tracing the polynomial)
    xr1 = 0.6 + 0.3*t_m + 0.8*t_m**2
    xr2 = 0.8 + 0.3*t_m + 0.8*t_m**2
    append_segmented(lines, 'C_MAG', list(xr1), [-w_mag-0.02]*16, list(z_mag))
    append_segmented(lines, 'C_MAG', list(xr2), [-w_mag-0.02]*16, list(z_mag))
    append_segmented(lines, 'C_MAG', list(xr1), [w_mag+0.02]*16, list(z_mag))
    append_segmented(lines, 'C_MAG', list(xr2), [w_mag+0.02]*16, list(z_mag))

    # ==============================================================================
    # 4. EXPLICIT BARREL & PNEUMATIC GAS TUBE
    # ==============================================================================
    x_muzz = 4.8
    brl_z = 0.1
    add_cylinder(lines, 'C_BARREL', x_trun, 0.0, brl_z, x_muzz - x_trun, 0.07, axis='x', rings=16)
    
    # Gas Tube (Parallel bridging element)
    x_gas = 2.8
    gas_z = 0.35
    add_cylinder(lines, 'C_BARREL', x_trun, 0.0, gas_z, x_gas - x_trun, 0.08, axis='x', rings=6)
    
    # Slanted Gas Block Matrix
    gb_prof = [(x_gas-0.1, brl_z), (x_gas-0.1, gas_z), (x_gas+0.2, gas_z), (x_gas+0.4, brl_z)]
    extrude_profile(lines, 'C_BARREL', gb_prof, -0.09, 0.09)

    # Front Sight Tower
    fs_prof = [(x_muzz-0.5, brl_z), (x_muzz-0.5, brl_z+0.5), (x_muzz-0.3, brl_z+0.5), (x_muzz-0.2, brl_z)]
    extrude_profile(lines, 'C_BARREL', fs_prof, -0.06, 0.06)

    # Over-barrel cleaning rod (Kinematic parallel geometry)
    add_cylinder(lines, 'C_BARREL', x_trun, 0.0, brl_z-0.15, x_muzz-0.2 - x_trun, 0.02, axis='x', rings=3)
    
    # Classic AKM Slant Brake
    append_segmented(lines, 'C_BARREL', [x_muzz, x_muzz+0.2, x_muzz+0.2, x_muzz], [-0.08, -0.08, 0.08, 0.08], [brl_z-0.08, brl_z-0.08, brl_z+0.02, brl_z+0.02])

    # ==============================================================================
    # 5. MACHINED WOODEN FURNITURE EXTRUSIONS (Stock, Grip, Handguards)
    # ==============================================================================
    # Rear Stock (Comb Drop Topology relying perfectly on geometric static scalar)
    w_stock = 0.17
    stock_prof = [
        (x_rear, 0.4), (x_rear-1.2, 0.4), (x_rear-2.6, 0.2), # Top sweep to heel
        (x_rear-2.6, -0.8), (x_rear-0.2, -0.3), (x_rear, -0.2) # Base sweep from toe
    ]
    extrude_profile(lines, 'C_WOOD', stock_prof, -w_stock, w_stock)
    
    # Distinctive side indent on the AK stock
    ind_x = np.linspace(x_rear-0.2, x_rear-2.2, 10)
    ind_z = np.linspace(0.1, -0.1, 10)
    append_segmented(lines, 'C_WOOD', list(ind_x), [-w_stock-0.02]*10, list(ind_z))
    append_segmented(lines, 'C_WOOD', list(ind_x), [ w_stock+0.02]*10, list(ind_z))

    # Pistol Grip (Aggressively angled)
    grip_prof = [(-0.3, -0.4), (-0.8, -0.4), (-1.2, -1.3), (-0.7, -1.4)]
    extrude_profile(lines, 'C_WOOD', grip_prof, -0.15, 0.15)
    
    # Upper Handguard (Wraps gas tube)
    uh_prof = [(1.5, gas_z), (1.5, gas_z+0.12), (2.3, gas_z+0.12), (2.3, gas_z)]
    extrude_profile(lines, 'C_WOOD', uh_prof, -0.15, 0.15)
    # Swell vents
    for vx in [1.7, 1.9, 2.1]:
        append_segmented(lines, 'C_BARREL', [vx]*2, [-0.16, -0.16], [gas_z+0.03, gas_z+0.08])
        append_segmented(lines, 'C_BARREL', [vx]*2, [ 0.16,  0.16], [gas_z+0.03, gas_z+0.08])

    # Lower Handguard (Wraps barrel with heavy side swells)
    lh_prof = [(1.4, brl_z+0.05), (1.4, brl_z-0.2), (2.6, brl_z-0.15), (2.6, brl_z+0.05)]
    extrude_profile(lines, 'C_WOOD', lh_prof, -0.22, 0.22) # Wider than receiver
    
    # Rear Sight Block (Trunnion mechanical logic)
    rs_prof = [(x_trun-0.2, 0.4), (x_trun-0.2, 0.65), (x_trun+0.3, 0.65), (x_trun+0.5, brl_z+0.1)]
    extrude_profile(lines, 'C_BARREL', rs_prof, -w_rec, w_rec)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_rifle_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        cam_x, cam_y, cam_z = 0.0, 0.0, -0.2 
        
        # 360-degree perfect orbital synchronisation 
        # Starts exactly side-on (+Y Right Side profile exposing Selector)
        azimuth = 90.0 - (stage * 360.0)

        yield (f, t_sec, azimuth, cam_x, cam_y, cam_z, static_rig)

def render_frame(packet):
    f, t_sec, azimuth, cx, cy, cz, static_rig = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # Cinematic Rigid Map Boundary - Covers the expansive 880mm structure perfectly
    cam_span = 5.2
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    # Layer density assignment (True Contrast Scaling)
    layer_map = [
        ('C_GRID',     C_GRID,     0.8, 0.4), 
        ('C_BARREL',   C_BARREL,   1.8, 1.0),
        ('C_RECEIVER', C_RECEIVER, 1.4, 1.0), 
        ('C_WOOD',     C_WOOD,     1.6, 1.0),
        ('C_MAG',      C_MAG,      1.4, 1.0),
        ('C_PINS',     C_PINS,     1.8, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Orbiting precisely on a 15-degree elevation to expose internal bounding
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=10.0) 
            render_queue.append((np.mean(depth), u, v, c_val, lw, alpha))

    # ABSOLUTE Z-SORT (Painter's Algorithm execution perfectly overlapping vectors)
    render_queue.sort(key=lambda item: item[0], reverse=True)
    for depth, u, v, c, lw, a in render_queue:
        ax.plot(u, v, color=c, lw=lw, alpha=a)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (TOP HUD)
    # ------------------------------------------------------------------
    ui_t = cam_span * 1.45
    ax.add_patch(patches.Rectangle((-cam_span, ui_t), cam_span*2, 6.0, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_t, ui_t], color=C_TEXT, lw=6, zorder=81)

    ax.text(-cam_span*0.95, ui_t+1.5, "LG-450c // MACRO-ENGINEERING TENSOR: KINEMATIC INTEGRATION", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t+0.5, "EXPLICIT TRUE-SCALE GEOMETRY // AK-47 ASSAULT RIFLE MATRIX", color=C_WOOD, fontsize=13, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b+2.2, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_MAG, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+1.1, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.2, "TOPOLOGICAL YIELD: DUAL BARREL LOGIC / PARAMETRIC MAGAZINE", color=C_RECEIVER, fontsize=13, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-450c: AK-47 KINEMATICS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Mechanical Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
