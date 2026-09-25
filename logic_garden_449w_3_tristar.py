"""
PROJECT: Logic Garden 449w_3 (Exact Physical Construct // L-1011 TriStar Matrix - REVISION 3)
FORMAT: YouTube Shorts (1080x1920)
METADATA: LOCKHEED TRISTAR, L-1011, AEROSPACE, WIREFRAME, ENGINEERING, KINEMATICS, AEROPLANE
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: True spherical blunt radome, Corrected S-Duct curve, scaled Vertical Fin, and explicit Horizontal Dihedral reflecting the Lockheed 3-view blueprint perfectly.
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
OUT_DIR = "frames_449w_tristar"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG            = '#FFFFFF'
C_TEXT          = '#111115'
C_FUSELAGE      = '#1E293B'  # Carbon Slate (Heavy Wide-body Hull)
C_WING          = '#475569'  # Slate Grey (Aerofoil Surfaces)
C_JET           = '#D95F22'  # Industrial Amber (Engine Intake/Exhaust Cores)
C_CHROME        = '#94A3B8'  # Machined Steel (Engine Nacelles & Pylons / Inner S-Duct)
C_GLASS         = '#005599'  # Deep Marine (Cockpit & Passenger Windows)
C_GRID          = '#CBD5E1'  # Subdued Steel (Baseplate Reference)

# ------------------------------------------------------------------
# O(N) KINEMATIC WIREFRAME ENGINE
# ------------------------------------------------------------------
def project_3d_depth(x, y, z, cx, cy, cz, az_deg, el_deg=0):
    tx, ty, tz = x - cx, y - cy, z - cz
    az, el = np.radians(az_deg), np.radians(el_deg)
    
    # Orbit Matrix
    x1 = tx * np.cos(az) - ty * np.sin(az)
    y1 = tx * np.sin(az) + ty * np.cos(az)
    z1 = tz
    
    # Elevation Matrix
    y2 = y1 * np.cos(el) - z1 * np.sin(el)
    z2 = y1 * np.sin(el) + z1 * np.cos(el)
    
    return x1, z2, y2 

def append_segmented(lines_dict, key, xs, ys, zs):
    """Absolute Segmentation Protocol: Splits arrays into 2-point vectors for strict mathematical depth sorting."""
    for i in range(len(xs) - 1):
        lines_dict[key].append(([xs[i], xs[i+1]], [ys[i], ys[i+1]], [zs[i], zs[i+1]]))

def extrude_airfoil(lines_dict, key, root_prof, tip_prof):
    """Generates aerodynamic surfaces transitioning from root to tip parameters."""
    r_xs, r_ys, r_zs = [p[0] for p in root_prof], [p[1] for p in root_prof], [p[2] for p in root_prof]
    t_xs, t_ys, t_zs = [p[0] for p in tip_prof], [p[1] for p in tip_prof], [p[2] for p in tip_prof]
    
    # Map root and tip full loops
    append_segmented(lines_dict, key, r_xs+[r_xs[0]], r_ys+[r_ys[0]], r_zs+[r_zs[0]])
    append_segmented(lines_dict, key, t_xs+[t_xs[0]], t_ys+[t_ys[0]], t_zs+[t_zs[0]])
    
    # Connect aerodynamic ribs along span
    for i in range(len(r_xs)):
        append_segmented(lines_dict, key, [r_xs[i], t_xs[i]], [r_ys[i], t_ys[i]], [r_zs[i], t_zs[i]])

def add_engine_nacelle(lines_dict, cx, cy, cz, length, rad_in, rad_out, rad_ex):
    """Constructs high bypass turbofan nacelles (Rolls-Royce RB211 profile)."""
    t = np.linspace(0, 2*np.pi, 24)
    
    # Intake Lip
    ix_in = np.full_like(t, cx + length/2)
    iy_in = cy + rad_in*np.cos(t)
    iz_in = cz + rad_in*np.sin(t)
    
    # Nacelle Max Width
    ix_mid = np.full_like(t, cx + length/4)
    iy_mid = cy + rad_out*np.cos(t)
    iz_mid = cz + rad_out*np.sin(t)
    
    # Exhaust
    ix_ex = np.full_like(t, cx - length/2)
    iy_ex = cy + rad_ex*np.cos(t)
    iz_ex = cz + rad_ex*np.sin(t)
    
    append_segmented(lines_dict, 'C_JET', list(ix_in)+[ix_in[0]], list(iy_in)+[iy_in[0]], list(iz_in)+[iz_in[0]])
    append_segmented(lines_dict, 'C_CHROME', list(ix_mid)+[ix_mid[0]], list(iy_mid)+[iy_mid[0]], list(iz_mid)+[iz_mid[0]])
    append_segmented(lines_dict, 'C_JET', list(ix_ex)+[ix_ex[0]], list(iy_ex)+[iy_ex[0]], list(iz_ex)+[iz_ex[0]])
    
    for a_idx in range(0, 24, 3):
        xs = [ix_in[a_idx], ix_mid[a_idx], ix_ex[a_idx]]
        ys = [iy_in[a_idx], iy_mid[a_idx], iy_ex[a_idx]]
        zs = [iz_in[a_idx], iz_mid[a_idx], iz_ex[a_idx]]
        append_segmented(lines_dict, 'C_CHROME', xs, ys, zs)

# ------------------------------------------------------------------
# RIGID 3D EXACT KINEMATIC GENERATOR
# ------------------------------------------------------------------
def generate_aircraft_vectors():
    lines = {
        'C_FUSELAGE': [], 'C_WING': [], 'C_JET': [], 
        'C_CHROME': [], 'C_GLASS': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. BASEPLATE ENVELOPE (REFERENCE GRID)
    # ==============================================================================
    gx_range = np.linspace(-30, 30, 25) 
    for gx in gx_range:
        append_segmented(lines, 'C_GRID', np.full_like(gx_range, gx), np.clip(gx_range, -25, 25), np.zeros_like(gx_range))
    gy_range = np.linspace(-25, 25, 21)
    for gy in gy_range:
        append_segmented(lines, 'C_GRID', np.clip(gx_range, -30, 30), np.full_like(gx_range, gy), np.zeros_like(gx_range))

    # ==============================================================================
    # 2. PARAMETRIC TOPOLOGICAL FUSELAGE HULL (TriStar Blunt Nose & Taper)
    # ==============================================================================
    # Length mapped explicitly from 27.0 (nose) to -27.0 (tail)
    station_x = np.linspace(27.0, -27.0, 54)
    ribs_pts = []
    
    for x in station_x:
        if x > 21.0:  # Dolphin Nose Array - True spherical/elliptical blunting
            ratio = (27.0 - x) / 6.0 
            arc_falloff = np.sqrt(max(0.001, 1.0 - (1.0 - ratio)**2))
            r_y = 3.0 * arc_falloff
            r_z = 3.0 * arc_falloff
            z_off = -1.2 * (1.0 - arc_falloff) # Aggressive aerodynamic droop tracking the blunt arc
        elif x < -12.0:  # Sweeping Tail Cone -> Tapering perfectly cleanly into the #2 Turbine
            ratio = (x - (-27.0)) / 15.0 # 0 at tail cone apex/exhaust, 1 at wide midbody
            r_y = 1.0 + 2.0 * ratio      # Linear converge exactly to the 1.0m Engine radius
            r_z = 1.0 + 2.0 * ratio
            z_off = 0.8 * (1.0 - ratio)  # Fuselage centerline pulls smoothly UP to the exhaust port Z=0.8
        else: # Constant Midbody Cylinder Array
            r_y = 3.0
            r_z = 3.0
            z_off = 0.0
            
        t = np.linspace(0, 2*np.pi, 24, endpoint=False)
        rib_x = np.full_like(t, x)
        rib_y = r_y * np.cos(t)
        rib_z = r_z * np.sin(t) + z_off
        ribs_pts.append((rib_x, rib_y, rib_z))
        
    # Segmented Transverse Ribs 
    for rx, ry, rz in ribs_pts:
        append_segmented(lines, 'C_FUSELAGE', list(rx)+[rx[0]], list(ry)+[ry[0]], list(rz)+[rz[0]])
        
    # Interlocking Longitudinal Stringers
    for i in range(24):
        sx = [r[0][i] for r in ribs_pts]
        sy = [r[1][i] for r in ribs_pts]
        sz = [r[2][i] for r in ribs_pts]
        append_segmented(lines, 'C_FUSELAGE', sx, sy, sz)

    # ==============================================================================
    # 3. EXPLICIT S-DUCT KINEMATIC CORE (Engine #2 Deep Curve)
    # ==============================================================================
    # Exact 3-view replication: Sweeping deeply inside the tail structure, exiting perfectly straight at Z=0.8.
    sduct_x = np.linspace(-13.5, -27.0, 16)
    for i, x in enumerate(sduct_x):
        u = (x - (-27.0)) / 13.5 # 1 at dorsal intake, 0 at terminal exhaust
        s_factor = u * u * (3.0 - 2.0 * u) # Smoothstep mathematical plunge curve
        z_c = 0.8 + (3.6 - 0.8) * s_factor # Bends elegantly from Intake(3.6) -> Turbine(0.8)
        r_d = 1.0 + (1.2 - 1.0) * u        # Diameter compression from open intake to thrust nozzle
        
        t = np.linspace(0, 2*np.pi, 24)
        c_x = np.full_like(t, x)
        c_y = r_d * np.cos(t)
        c_z = z_c + r_d * np.sin(t)
        
        col = 'C_JET' if i in [0, len(sduct_x)-1] else 'C_CHROME'
        append_segmented(lines, col, list(c_x)+[c_x[0]], list(c_y)+[c_y[0]], list(c_z)+[c_z[0]])
        
        if i < len(sduct_x)-1:
            u_n = (sduct_x[i+1] - (-27.0)) / 13.5
            sfn = u_n * u_n * (3.0 - 2.0*u_n)
            zcn = 0.8 + (3.6 - 0.8) * sfn
            rdn = 1.0 + (1.2 - 1.0) * u_n
            cx_n = np.full_like(t, sduct_x[i+1])
            cy_n = rdn * np.cos(t)
            cz_n = zcn + rdn * np.sin(t)
            for a_idx in range(0, 24, 3):
                append_segmented(lines, 'C_CHROME', [c_x[a_idx], cx_n[a_idx]], [c_y[a_idx], cy_n[a_idx]], [c_z[a_idx], cz_n[a_idx]])

    # ==============================================================================
    # 4. WINDOW DLOs & COCKPIT GLASS ARRAYS (Aligned to blunt nose geometry)
    # ==============================================================================
    for z_w in [0.4, 0.9]: 
        cx_w = [24.0, 24.8, 25.4, 24.8, 24.0]
        cy_w = [-1.4, -0.7,  0.0,  0.7,  1.4]
        append_segmented(lines, 'C_GLASS', cx_w, cy_w, [z_w]*5)
    for i in range(5):
        cx_w = [24.0, 24.8, 25.4, 24.8, 24.0]
        cy_w = [-1.4, -0.7,  0.0,  0.7,  1.4]
        append_segmented(lines, 'C_GLASS', [cx_w[i]]*2, [cy_w[i]]*2, [0.4, 0.9])

    wx_pts = np.linspace(-10.0, 18.0, 45)
    for y_sign in [-1, 1]:
        wy_pts = np.full_like(wx_pts, 2.95 * y_sign)
        wz_pts = np.full_like(wx_pts, 0.4)
        for i in range(len(wx_pts)):
            sz, ez = 0.2, 0.6
            sx, ex = wx_pts[i]-0.15, wx_pts[i]+0.15
            append_segmented(lines, 'C_GLASS', [sx, ex, ex, sx, sx], [wy_pts[i]]*5, [sz, sz, ez, ez, sz])

    # ==============================================================================
    # 5. SWEEPING WINGS (Main Planes & Stabilisers matched to Blueprint Dimensions)
    # ==============================================================================
    def airfoil_pts(x_c, y_c, z_c, chord, thickness):
        return [
            (x_c + chord*0.3, y_c, z_c), 
            (x_c,             y_c, z_c - thickness), 
            (x_c - chord*0.7, y_c, z_c - thickness*0.2), 
            (x_c - chord,     y_c, z_c), 
            (x_c - chord*0.7, y_c, z_c + thickness*0.4), 
            (x_c,             y_c, z_c + thickness)
        ]
        
    for sign in [-1, 1]:
        # Main heavy-lift Swept Wings
        root = airfoil_pts(  2.0,  3.0 * sign, -1.0, chord=9.0, thickness=0.8 )
        mid  = airfoil_pts( -2.0,  8.5 * sign,  0.0, chord=4.5, thickness=0.4 )
        tip  = airfoil_pts(-11.0, 24.0 * sign,  1.8, chord=2.0, thickness=0.15 )
        
        extrude_airfoil(lines, 'C_WING', root, mid)
        extrude_airfoil(lines, 'C_WING', mid, tip)

    # Vertical Stabiliser (Scaled perfectly, seated natively behind/on the pod intake)
    v_root = [(-15.0, 0.0, 4.8), (-24.0, 0.0, 3.8)] # Leading edge anchors tightly with the 3.8m intake, TE swoops back.
    v_tip  = [(-21.0, 0.0, 9.5), (-26.0, 0.0, 9.5)] 
    
    append_segmented(lines, 'C_WING', [p[0] for p in v_root], [p[1] for p in v_root], [p[2] for p in v_root])
    append_segmented(lines, 'C_WING', [p[0] for p in v_tip], [p[1] for p in v_tip], [p[2] for p in v_tip])
    append_segmented(lines, 'C_WING', [v_root[0][0], v_tip[0][0]], [0,0], [v_root[0][2], v_tip[0][2]]) # Leading Edge
    append_segmented(lines, 'C_WING', [v_root[1][0], v_tip[1][0]], [0,0], [v_root[1][2], v_tip[1][2]]) # Trailing Edge

    # Horizontal Stabilisers (High Dihedral exactly matching TriStar specifications)
    for sign in [-1, 1]:
        h_root = airfoil_pts(-22.0,  1.0 * sign,  0.6, chord=5.0, thickness=0.3 )
        h_tip  = airfoil_pts(-24.5,  9.0 * sign,  1.8, chord=2.5, thickness=0.1 )
        extrude_airfoil(lines, 'C_WING', h_root, h_tip)

    # ==============================================================================
    # 6. EXPLICIT ROLLS-ROYCE RB211 ENGINES (Wing Nacelles)
    # ==============================================================================
    for sign in [-1, 1]:
        en_x = 2.0; en_y = 8.5 * sign; en_z = -1.8
        # Deep, massive high bypass turbofan dimensions natively modelled
        add_engine_nacelle(lines, en_x, en_y, en_z, length=5.0, rad_in=1.1, rad_out=1.35, rad_ex=0.9)
        # Heavy Machined Steel Engine Pylons
        append_segmented(lines, 'C_CHROME', [en_x-0.5, en_x-1.0, en_x-3.0, en_x-3.0, en_x-0.5], 
                                            [en_y, en_y, en_y, en_y, en_y], 
                                            [en_z+1.35, 0.0, -0.2, en_z+1.30, en_z+1.35])

    return lines

# ------------------------------------------------------------------
# PARALLEL GENERATOR STREAM (KINEMATIC TIMELINE TENSOR)
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_aircraft_vectors() # Computed once for true O(1) loop retrieval
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        cam_x, cam_y, cam_z = 0.0, 0.0, 1.5 
        azimuth = 90.0 - (stage * 360.0)

        yield (f, t_sec, azimuth, cam_x, cam_y, cam_z, static_rig)

# ------------------------------------------------------------------
# THREAD-SAFE PAINTER'S RENDERER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, azimuth, cx, cy, cz, static_rig = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    cam_span = 32.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []

    # 1. PROCESS KINEMATIC VECTOR MATRIX
    for c_key, c_val in [('C_GRID', C_GRID), ('C_FUSELAGE', C_FUSELAGE), ('C_WING', C_WING), 
                         ('C_CHROME', C_CHROME), ('C_JET', C_JET), ('C_GLASS', C_GLASS)]:
        
        if c_key == 'C_GRID': lw, alpha = 0.8, 0.4
        elif c_key == 'C_FUSELAGE': lw, alpha = 1.3, 1.0     
        elif c_key == 'C_GLASS': lw, alpha = 1.6, 1.0      
        elif c_key == 'C_WING': lw, alpha = 1.2, 1.0  
        elif c_key == 'C_CHROME': lw, alpha = 1.4, 1.0   
        elif c_key == 'C_JET': lw, alpha = 2.0, 1.0   
        else: lw, alpha = 1.0, 1.0
            
        for xl, yl, zl in static_rig[c_key]:
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=20.0)
            render_queue.append((np.mean(depth), u, v-3.0, c_val, lw, alpha))

    # 2. ABSOLUTE PAINTER'S ALGORITHM
    render_queue.sort(key=lambda item: item[0], reverse=True)

    for depth, u, v, c, lw, a in render_queue:
        ax.plot(u, v, color=c, lw=lw, alpha=a)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (TOP HUD)
    # ------------------------------------------------------------------
    ui_t = cam_span * 1.45
    ax.add_patch(patches.Rectangle((-cam_span, ui_t), cam_span*2, 16.0, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_t, ui_t], color=C_TEXT, lw=6, zorder=81)

    ax.text(-cam_span*0.95, ui_t+3.0, "LG-449w // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t+1.0, "EXPLICIT TRUE-SCALE GEOMETRY // LOCKHEED L-1011 TRISTAR MATRIX (REVISION 3)", color=C_FUSELAGE, fontsize=17, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b+4.5, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_CHROME, fontsize=18, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+2.5, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS SYNCHRONISATION)", color=C_TEXT, fontsize=18, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.5, "AERODYNAMIC YIELD: INTEGRAL S-DUCT & TRUE DIHEDRAL SWEEP SECURED", color=C_GLASS, fontsize=16, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-449w: TRISTAR MACRO-ENGINEERING TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
