"""
PROJECT: Logic Garden 451w (Exact Physical Construct // Lockheed L-1011 TriStar Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: L-1011, TRISTAR, LOCKHEED, WIREFRAME, ENGINEERING, KINEMATICS, AEROPLANE
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation isolating true dimensional 54.17m aerospace scale.
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Purged modern nose geometries; reconstructed authentic blunt radome, S-Duct logic, and swept wings.
- Viewport Override: Locked cam_span rigorously guarantees 100% vehicle visibility strictly between UI boundaries.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from 105-degree dramatic front-quarter angle.
- Daylight Palette (White Substrate / High-Contrast Edge Geometry).
- Purged Jargon. Australian spelling conventions (maths, colour, kilometres, synchronisation, aeroplane).
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
OUT_DIR = "frames_451w_tristar"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Flight Plane Tracking Grid)

C_HULL      = '#0F172A'          # Abyssal Slate (Primary Aluminum Fuselage)
C_WING      = '#334155'          # Heavy Slate (Aerofoils & Stabilisers)
C_DUCT      = '#475569'          # Machined Slate (Dorsal S-Duct)
C_ENGINE    = '#1E293B'          # Carbon Slate (RB211 Engine Nacelles)
C_JET       = '#D97706'          # Kapton Gold (Intake Fans & Exhaust Nodes)
C_GLASS     = '#005599'          # Deep Marine (Cockpit / Passenger Windows)

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

def extrude_airfoil(lines_dict, key, root_prof, tip_prof):
    r_xs, r_ys, r_zs = [p[0] for p in root_prof], [p[1] for p in root_prof], [p[2] for p in root_prof]
    t_xs, t_ys, t_zs = [p[0] for p in tip_prof], [p[1] for p in tip_prof], [p[2] for p in tip_prof]
    
    append_segmented(lines_dict, key, r_xs+[r_xs[0]], r_ys+[r_ys[0]], r_zs+[r_zs[0]])
    append_segmented(lines_dict, key, t_xs+[t_xs[0]], t_ys+[t_ys[0]], t_zs+[t_zs[0]])
    for i in range(len(r_xs)):
        append_segmented(lines_dict, key, [r_xs[i], t_xs[i]], [r_ys[i], t_ys[i]], [r_zs[i], t_zs[i]])

def add_nacelle(lines_dict, cx, cy, cz, length, rad_in, rad_out, rad_ex):
    t = np.linspace(0, 2*np.pi, 20)
    # Intake Lip
    ix_in = np.full_like(t, cx + length*0.4)
    iy_in = cy + rad_in*np.cos(t)
    iz_in = cz + rad_in*np.sin(t)
    # Max Width Barrel
    ix_mid = np.full_like(t, cx + length*0.1)
    iy_mid = cy + rad_out*np.cos(t)
    iz_mid = cz + rad_out*np.sin(t)
    # Exhaust
    ix_ex = np.full_like(t, cx - length*0.6)
    iy_ex = cy + rad_ex*np.cos(t)
    iz_ex = cz + rad_ex*np.sin(t)
    
    append_segmented(lines_dict, 'C_JET', list(ix_in)+[ix_in[0]], list(iy_in)+[iy_in[0]], list(iz_in)+[iz_in[0]])
    append_segmented(lines_dict, 'C_ENGINE', list(ix_mid)+[ix_mid[0]], list(iy_mid)+[iy_mid[0]], list(iz_mid)+[iz_mid[0]])
    append_segmented(lines_dict, 'C_JET', list(ix_ex)+[ix_ex[0]], list(iy_ex)+[iy_ex[0]], list(iz_ex)+[iz_ex[0]])
    
    for a_idx in range(0, 20, 2):
        xs = [ix_in[a_idx], ix_mid[a_idx], ix_ex[a_idx]]
        ys = [iy_in[a_idx], iy_mid[a_idx], iy_ex[a_idx]]
        zs = [iz_in[a_idx], iz_mid[a_idx], iz_ex[a_idx]]
        append_segmented(lines_dict, 'C_ENGINE', xs, ys, zs)

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (LOCKHEED L-1011 TRISTAR)
# ------------------------------------------------------------------
def generate_tristar_static():
    lines = {
        'C_HULL': [], 'C_WING': [], 'C_DUCT': [], 
        'C_ENGINE': [], 'C_JET': [], 'C_GLASS': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. ORBITAL TRACKING BASEPLATE
    # ==============================================================================
    Z_FLOOR = -5.0
    for r_p in [10.0, 20.0, 30.0]:
        t_p = np.linspace(0, 2*np.pi, 64, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
        
    gx_range = np.linspace(-30.0, 30.0, 13)
    gy_range = np.linspace(-30.0, 30.0, 13)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # ==============================================================================
    # 2. CLASSIC BASE WIDE-BODY FUSELAGE
    # ==============================================================================
    station_x = np.linspace(26.0, -27.5, 60)
    ribs = []
    
    for x in station_x:
        if x > 15.0:  
            # Classic Blunt Elliptical Geometry (Replaces A350 pointy nose)
            ratio = (26.0 - x) / 11.0 
            r_y = 2.985 * np.sqrt(max(0, 1 - (1-ratio)**2))
            r_z = 2.985 * np.sqrt(max(0, 1 - (1-ratio)**2))
            # Traditional cab droop
            z_off = -0.7 * (1 - ratio)**2 
        elif x < -10.0:  
            # Tapering tail section dropping away from the S-Duct
            ratio = (-10.0 - x) / 17.5 
            r_y = 2.985 * (1 - 0.7 * ratio)
            r_z = 2.985 * (1 - 0.6 * ratio)
            z_off = 1.0 * ratio**2
        else: 
            # Continuous Nominal 5.97m Wide-body midsection
            r_y = 2.985
            r_z = 2.985
            z_off = 0.0
            
        t = np.linspace(0, 2*np.pi, 24, endpoint=False)
        rib_x = np.full_like(t, x)
        rib_y = r_y * np.cos(t)
        rib_z = r_z * np.sin(t) + z_off
        ribs.append((rib_x, rib_y, rib_z))
        
    for r in ribs:
        append_segmented(lines, 'C_HULL', list(r[0])+[r[0][0]], list(r[1])+[r[1][0]], list(r[2])+[r[2][0]])
        
    for i in range(24):
        sx = [r[0][i] for r in ribs]
        sy = [r[1][i] for r in ribs]
        sz = [r[2][i] for r in ribs]
        append_segmented(lines, 'C_HULL', sx, sy, sz)

    # ==============================================================================
    # 3. DORSAL S-DUCT (#2 ENGINE KINEMATICS)
    # ==============================================================================
    sduct_x = np.linspace(-10.0, -27.5, 20)
    duct_ribs = []
    
    for i, x in enumerate(sduct_x):
        ratio = (-10.0 - x) / 17.5 
        s_curve = 0.5 - 0.5 * np.cos(ratio * np.pi) 

        # Centers from Z=4.0 (+1.15 rad clears top of fuselage) dropping to Z=1.0 at tail
        z_c = 4.0 - 3.0 * s_curve 
        r_d = 1.15 - 0.15 * ratio
        
        t = np.linspace(0, np.pi, 12, endpoint=True) # Top half explicit mapping
        c_x = np.full_like(t, x)
        c_y = r_d * np.cos(t)
        c_z = z_c + r_d * np.sin(t)
        
        # Close bottom half depending on fuselage intersection
        c_zb = z_c - r_d*0.5
        c_xb = [x, x]
        c_yb = [c_y[-1], c_y[0]]
        c_zb_arr = [c_z[-1], c_z[0]]
        
        col = 'C_JET' if i in [0, len(sduct_x)-1] else 'C_DUCT'
        append_segmented(lines, col, list(c_x)+c_xb, list(c_y)+c_yb, list(c_z)+c_zb_arr)
        duct_ribs.append((c_x, c_y, c_z))

    for i in range(12):
        sx = [r[0][i] for r in duct_ribs]
        sy = [r[1][i] for r in duct_ribs]
        sz = [r[2][i] for r in duct_ribs]
        append_segmented(lines, 'C_DUCT', sx, sy, sz)

    # ==============================================================================
    # 4. TANDEM COCKPIT & WINDOW ARRAYS
    # ==============================================================================
    for z_w in [1.0, 1.5]: 
        cx_w = [23.0, 24.2, 24.8, 24.2, 23.0]
        cy_w = [-1.8, -1.0,  0.0,  1.0,  1.8]
        append_segmented(lines, 'C_GLASS', cx_w, cy_w, [z_w]*5)
    for i in range(5):
        cx_w = [23.0, 24.2, 24.8, 24.2, 23.0]
        cy_w = [-1.8, -1.0,  0.0,  1.0,  1.8]
        append_segmented(lines, 'C_GLASS', [cx_w[i]]*2, [cy_w[i]]*2, [1.0, 1.5])

    wx_pts = np.linspace(-10.0, 16.0, 45)
    for y_sign in [-1, 1]:
        wy_pts = np.full_like(wx_pts, 2.96 * y_sign)
        for i in range(len(wx_pts)):
            sz, ez = 0.2, 0.6
            sx, ex = wx_pts[i]-0.15, wx_pts[i]+0.15
            append_segmented(lines, 'C_GLASS', [sx, ex, ex, sx, sx], [wy_pts[i]]*5, [sz, sz, ez, ez, sz])

    # ==============================================================================
    # 5. AERODYNAMIC LIFT SURFACES
    # ==============================================================================
    def airfoil(x_c, y_c, z_c, chord, thick):
        return [
            (x_c + chord*0.25, y_c, z_c), 
            (x_c, y_c, z_c - thick*0.6), 
            (x_c - chord*0.75, y_c, z_c), 
            (x_c, y_c, z_c + thick)
        ]
        
    for sign in [-1, 1]:
        # Massive Swept Wing Profile (No Winglets)
        root = airfoil( 5.0,  2.8 * sign, -1.2, 11.0, 1.0)
        mid  = airfoil(-3.0, 12.0 * sign, -0.2, 6.0,  0.6)
        tip  = airfoil(-10.0, 23.6 * sign, 1.2, 2.5,  0.2)
        
        extrude_airfoil(lines, 'C_WING', root, mid)
        extrude_airfoil(lines, 'C_WING', mid, tip)

        # Swept Horizontal Stabilisers
        h_root = airfoil(-20.0,  1.5 * sign,  0.5, 6.0, 0.5)
        h_tip  = airfoil(-24.0,  9.0 * sign,  1.5, 2.5, 0.2)
        extrude_airfoil(lines, 'C_WING', h_root, h_tip)

    # Vertical Stabiliser (Bolted explicitly atop the S-Duct Housing)
    v_root = [(-13.0, 0.0, 5.0), (-23.0, 0.0, 3.5)] 
    v_tip  = [(-19.0, 0.0, 10.8), (-25.0, 0.0, 10.8)] 
    append_segmented(lines, 'C_WING', [p[0] for p in v_root], [p[1] for p in v_root], [p[2] for p in v_root])
    append_segmented(lines, 'C_WING', [p[0] for p in v_tip], [p[1] for p in v_tip], [p[2] for p in v_tip])
    append_segmented(lines, 'C_WING', [v_root[0][0], v_tip[0][0]], [0,0], [v_root[0][2], v_tip[0][2]]) 
    append_segmented(lines, 'C_WING', [v_root[1][0], v_tip[1][0]], [0,0], [v_root[1][2], v_tip[1][2]]) 

    # ==============================================================================
    # 6. UNDER-WING HIGH-BYPASS NACELLES (#1 & #3)
    # ==============================================================================
    for sign in [-1, 1]:
        en_x = 0.0; en_y = 8.5 * sign; en_z = -2.5
        add_nacelle(lines, en_x, en_y, en_z, length=4.5, rad_in=1.2, rad_out=1.4, rad_ex=0.9)
        # Structural Mount Pylons
        append_segmented(lines, 'C_ENGINE', [en_x, -2.0, -4.0, en_x-2.0, en_x], 
                                            [en_y, en_y, en_y, en_y, en_y], 
                                            [en_z+1.4, 0.0, 0.0, en_z+1.4, en_z+1.4])

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_tristar_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking the focal geometry flawlessly across the massive 54m chassis
        cam_x, cam_y, cam_z = 0.0, 0.0, 2.0
        
        # Starts explicitly from 105-degrees (Slight majestic banking profile exposing radome)
        azimuth = 105.0 - (stage * 360.0)

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
    # Anchor Centroid = Dead zero. Aircraft length equals 54.17 metres.
    # Setting cam_span forcefully to 34.0 locks horizontal width symmetrically across an immense 68.0m.
    # Vertical bounds trace automatically to a massive 60.4m clearance (1.777 * 34.0).
    # The extreme elements (tail fins, wings, radome) never touch the UI bounding boxes regardless of rotation.
    cam_span = 34.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,     0.8, 0.4), 
        ('C_DUCT',      C_DUCT,     1.3, 1.0),
        ('C_WING',      C_WING,     1.3, 1.0),
        ('C_HULL',      C_HULL,     1.4, 1.0),
        ('C_ENGINE',    C_ENGINE,   1.5, 1.0),
        ('C_GLASS',     C_GLASS,    1.3, 1.0),
        ('C_JET',       C_JET,      1.8, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +15 degrees into an intense downward intercept revealing the sweeping flight surfaces
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-451w // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // LOCKHEED L-1011 TRISTAR MATRIX", color=C_HULL, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=C_DUCT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: 100% UNCLIPPED HORIZON / ACCURATE BLUNT RADOME / DORSAL S-DUCT", color=C_JET, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-451w: LOCKHEED TRISTAR TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
