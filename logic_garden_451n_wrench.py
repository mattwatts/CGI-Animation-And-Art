"""
PROJECT: Logic Garden 451n (Exact Physical Construct // Combination Wrench Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: WRENCH, SPANNER, TOOLS, ENGINEERING, WIREFRAME, KINEMATICS, CAD
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation bypassing binary imports for absolute topological mapping.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: True 15-degree offset open jaw, 12-point bi-hexagonal ring head, recessed drop-forged shaft.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from 115-degree dramatic offset profile.
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
OUT_DIR = "frames_451n_wrench"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Mechanical Baseplate)

C_CHROME    = '#94A3B8'          # Slate Aluminium (Primary Outer Forging)
C_INSET     = '#475569'          # Machined Slate (Recessed Channels / Tool Marks)
C_EDGE      = '#1E293B'          # Carbon Slate (Heavy Structural Boundaries)
C_ACCENT    = '#E11D48'          # Kinematic Red (Centerline Alignment)

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
def extrude_profile(lines_dict, col, pts, z_min, z_max):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    # Draw solid upper and lower rims
    append_segmented(lines_dict, col, xs+[xs[0]], ys+[ys[0]], [z_max]*(len(xs)+1))
    append_segmented(lines_dict, col, xs+[xs[0]], ys+[ys[0]], [z_min]*(len(xs)+1))
    # Drop vertical intersecting struts
    for i in range(len(xs)):
        append_segmented(lines_dict, col, [xs[i], xs[i]], [ys[i], ys[i]], [z_min, z_max])

def add_flat_loop(lines_dict, col, pts, z):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    append_segmented(lines_dict, col, xs+[xs[0]], ys+[ys[0]], [z]*(len(xs)+1))

def get_open_end_pts(cx, cy, r_out, W, x_c_in_local, angle_deg):
    # Core mathematical boundaries mapping the C-spanner jaw intersection
    x_int = np.sqrt(r_out**2 - (W/2)**2)
    theta_int = np.arcsin((W/2)/r_out)
    
    pts = []
    # 1. Outer curved forging bounding the head
    t_arc = np.linspace(theta_int, 2*np.pi - theta_int, 40)
    for t in t_arc:
        pts.append((r_out * np.cos(t), r_out * np.sin(t)))
        
    # 2. Top precision-machined jaw line
    pts.append((x_int, -W/2))
    pts.append((x_c_in_local, -W/2))
    
    # 3. Inner relief curve securing the hardware
    t_in = np.linspace(-np.pi/2, np.pi/2, 16)
    for t in t_in:
        pts.append((x_c_in_local + (W/2)*np.cos(t), (W/2)*np.sin(t)))
        
    # 4. Bottom precision-machined jaw line
    pts.append((x_c_in_local, W/2))
    pts.append((x_int, W/2))
    
    # Apply operational 15-degree mechanical offset and global translation
    ang = np.radians(angle_deg)
    c, s = np.cos(ang), np.sin(ang)
    out = []
    for x,y in pts:
        rx = x*c - y*s + cx
        ry = x*s + y*c + cy
        out.append((rx, ry))
        
    return out

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (COMBINATION WRENCH MATRIX)
# ------------------------------------------------------------------
def generate_wrench_static():
    lines = {
        'C_CHROME': [], 'C_INSET': [], 'C_EDGE': [], 
        'C_ACCENT': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. REFERENCE BASEPLATE
    # ==============================================================================
    Z_FLOOR = -0.15
    gx_range = np.linspace(-1.5, 1.5, 17)
    gy_range = np.linspace(-1.5, 1.5, 17)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # Wrench scale operates across a massive ~1.9m vector for extreme macro detail projection
    # ==============================================================================
    # 2. BOX END (12-Point Bi-Hexagonal Ring)
    # ==============================================================================
    CX_BOX = -0.75
    Z_HEAD = 0.04 # Thicker bounds locking the nut
    
    t_star = np.linspace(0, 2*np.pi, 24, endpoint=False)
    r_in1 = 0.08
    r_in2 = 0.10
    pts_box_in = []
    for i, t in enumerate(t_star):
         r = r_in1 if i%2 == 0 else r_in2
         pts_box_in.append((CX_BOX + r*np.cos(t), 0.0 + r*np.sin(t)))
         
    t_out = np.linspace(0, 2*np.pi, 40, endpoint=False)
    pts_box_out = [(CX_BOX + 0.18*np.cos(t), 0.18*np.sin(t)) for t in t_out]
    
    # Render heavy structural boundaries
    extrude_profile(lines, 'C_EDGE', pts_box_in, -Z_HEAD, Z_HEAD)
    extrude_profile(lines, 'C_CHROME', pts_box_out, -Z_HEAD, Z_HEAD)
    
    # Render dense concentric tool-marks mapping the forged steel
    for r_tm in [0.16, 0.14, 0.12]:
        p = [(CX_BOX + r_tm*np.cos(t), 0.0 + r_tm*np.sin(t)) for t in t_out]
        for z in [-Z_HEAD, Z_HEAD]: add_flat_loop(lines, 'C_INSET', p, z)

    # ==============================================================================
    # 3. OPEN END (15-Degree Offset C-Spanner)
    # ==============================================================================
    CX_OPEN = 0.75
    
    open_pts = get_open_end_pts(cx=CX_OPEN, cy=0.0, r_out=0.22, W=0.15, x_c_in_local=-0.05, angle_deg=15.0)
    extrude_profile(lines, 'C_EDGE', open_pts, -Z_HEAD, Z_HEAD)
    
    # Internal tapering facets mapping the open jaws
    for s in [0.93, 0.86, 0.79]:
        scaled_pts = [(CX_OPEN + (x-CX_OPEN)*s, 0.0 + (y-0.0)*s) for x,y in open_pts]
        for z in [-Z_HEAD, Z_HEAD]: add_flat_loop(lines, 'C_INSET', scaled_pts, z)

    # ==============================================================================
    # 4. CHROME VANADIUM SHAFT (Recessed Drop-forging logic)
    # ==============================================================================
    x_h = np.linspace(-0.7, 0.7, 40)
    y_h = np.interp(x_h, [-0.7, 0.7], [0.10, 0.12])
    Z_HAND = 0.03 # The handle is exactly 1mm step equivalent thinner than the heads
    
    # Primary Outer Forging Rails sliding into the heads
    for sign in [-1, 1]:
        ys = y_h * sign
        append_segmented(lines, 'C_EDGE', list(x_h), list(ys), [Z_HAND]*40)
        append_segmented(lines, 'C_EDGE', list(x_h), list(ys), [-Z_HAND]*40)
        for i in range(40):
            append_segmented(lines, 'C_CHROME', [x_h[i], x_h[i]], [ys[i], ys[i]], [-Z_HAND, Z_HAND])
            
    # Continuous Transverse Grid mapping the un-recessed smooth necks
    for i in list(range(0, 5)) + list(range(35, 40)):
         append_segmented(lines, 'C_INSET', [x_h[i], x_h[i]], [-y_h[i], y_h[i]], [Z_HAND, Z_HAND])
         append_segmented(lines, 'C_INSET', [x_h[i], x_h[i]], [-y_h[i], y_h[i]], [-Z_HAND, -Z_HAND])
         
    # Deep Recessed Channel Execution (Indices 5 through 34)
    y_rc = y_h * 0.65 # Channel recess targets 65% total shaft width
    Z_RC = 0.015      # Hard plunge depth representing forged out material
    
    for i in range(5, 35):
         # Top Angled Bevels cutting structurally down into the core
         append_segmented(lines, 'C_INSET', [x_h[i], x_h[i]], [y_h[i], y_rc[i]], [Z_HAND, Z_RC])
         append_segmented(lines, 'C_INSET', [x_h[i], x_h[i]], [-y_h[i], -y_rc[i]], [Z_HAND, Z_RC])
         
         # Bottom Angled Bevels cutting structurally up into the core
         append_segmented(lines, 'C_INSET', [x_h[i], x_h[i]], [y_h[i], y_rc[i]], [-Z_HAND, -Z_RC])
         append_segmented(lines, 'C_INSET', [x_h[i], x_h[i]], [-y_h[i], -y_rc[i]], [-Z_HAND, -Z_RC])
         
         # Inner Channel Floor Grids
         append_segmented(lines, 'C_CHROME', [x_h[i], x_h[i]], [-y_rc[i], y_rc[i]], [Z_RC, Z_RC])
         append_segmented(lines, 'C_CHROME', [x_h[i], x_h[i]], [-y_rc[i], y_rc[i]], [-Z_RC, -Z_RC])
         
    # Fastener longitudinal rails defining the plunged recess bounds
    for sign in [-1, 1]:
        ys_rc = y_rc[5:35] * sign
        xs_rc = x_h[5:35]
        append_segmented(lines, 'C_EDGE', list(xs_rc), list(ys_rc), [Z_RC]*30)
        append_segmented(lines, 'C_EDGE', list(xs_rc), list(ys_rc), [-Z_RC]*30)
        
    # Vertical closure bounds linking the un-recessed necks into the channel geometry
    for b_idx in [5, 34]:
        for sign in [-1, 1]:
            append_segmented(lines, 'C_EDGE', [x_h[b_idx]]*2, [0, y_rc[b_idx]*sign], [Z_HAND, Z_RC])
            append_segmented(lines, 'C_EDGE', [x_h[b_idx]]*2, [0, y_rc[b_idx]*sign], [-Z_HAND, -Z_RC])

    # Absolute kinematic centerline tracking the length of the tool
    append_segmented(lines, 'C_ACCENT', [-0.75, 0.75], [0.0, 0.0], [0.0, 0.0])

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_wrench_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.0
        
        # Starts explicitly from 115-degrees (Dramatic side-biased aesthetic tracking the entire shaft logic)
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
    # 2.0m scaled geometry mapping.
    cam_span = 1.15
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',   C_GRID,   0.6, 0.4), 
        ('C_ACCENT', C_ACCENT, 1.2, 0.7),
        ('C_INSET',  C_INSET,  1.0, 1.0),
        ('C_CHROME', C_CHROME, 1.4, 1.0),
        ('C_EDGE',   C_EDGE,   1.8, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +14 degrees to dynamically slice through the intense forged recess
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=14.0)
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-451n // MACRO-ENGINEERING TENSOR: MECHANICAL KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // COMBINATION WRENCH MATRIX", color=C_INSET, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_CHROME, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: TRUE 12-POINT BOX END / TAPERED DROP-FORGED RECESS", color=C_EDGE, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-451n: KINEMATIC WRENCH TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Mechanical Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
