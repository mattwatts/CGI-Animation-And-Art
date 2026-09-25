"""
PROJECT: Logic Garden 449q (Exact Physical Construct // Ocean Liner Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: SHIP, OCEAN LINER, NAVAL ARCHITECTURE, WIREFRAME, ENGINEERING, KINEMATICS, DIAGRAM
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Hydrodynamic Hull lofting, Tiered Decks, 3 Raked Funnels, Rigging Tensors.
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
OUT_DIR = "frames_449q_ship"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG          = '#FFFFFF'
C_TEXT        = '#111115'
C_HULL_UPPER  = '#1E293B'  # Carbon Slate (Upper freeboard)
C_HULL_LOWER  = '#991B1B'  # Crimson Oxide (Lower draft / Anti-fouling layer)
C_SUPERSTRUCT = '#94A3B8'  # Machined Steel (Promenade and Decks)
C_FUNNEL      = '#D97706'  # Dense Amber (Classic funnel bases)
C_FUNNEL_TOP  = '#111115'  # Indestructible Black (Funnel exhaust cowlings)
C_GLASS       = '#005599'  # Marine Blue (Bridge and promenade windows)
C_WIRE        = '#64748B'  # Slate (High-tension rigging arrays)
C_GRID        = '#CBD5E1'  # Subdued Steel (Baseplate Reference)

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

def extrude_deck_plane(lines_dict, col_key, x_bounds, y_bounds, z_val):
    """Extrudes a planar deck matrix segment."""
    x1, x2 = x_bounds
    y1, y2 = y_bounds
    xs = np.linspace(x1, x2, int((x2-x1)*4)+2)
    append_segmented(lines_dict, col_key, xs, np.full_like(xs, y1), np.full_like(xs, z_val))
    append_segmented(lines_dict, col_key, xs, np.full_like(xs, y2), np.full_like(xs, z_val))
    ys = np.linspace(y1, y2, int((y2-y1)*4)+2)
    append_segmented(lines_dict, col_key, np.full_like(ys, x1), ys, np.full_like(ys, z_val))
    append_segmented(lines_dict, col_key, np.full_like(ys, x2), ys, np.full_like(ys, z_val))

def build_raked_cylinder(lines_dict, col_key, base_x, base_y, base_z, radius, height, rake_offset):
    """Generates an extruded cylindrical mast or funnel perfectly raked across the X-axis."""
    t = np.linspace(0, 2*np.pi, 16)
    rings = 6
    for i, r_ratio in enumerate(np.linspace(0, 1, rings)):
        z = base_z + height * r_ratio
        x = base_x + rake_offset * r_ratio
        ix, iy, iz = x + radius*np.cos(t), base_y + radius*np.sin(t), np.full_like(t, z)
        append_segmented(lines_dict, col_key, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
        
    for a in t[::2]:
        sx = base_x + rake_offset * np.linspace(0, 1, rings) + radius*np.cos(a)
        sy = np.full_like(sx, base_y + radius*np.sin(a))
        sz = base_z + height * np.linspace(0, 1, rings)
        append_segmented(lines_dict, col_key, list(sx), list(sy), list(sz))

# ------------------------------------------------------------------
# RIGID 3D EXACT NAVAL ARCHITECTURE GENERATOR
# ------------------------------------------------------------------
def generate_ship_vectors():
    lines = {
        'C_HULL_UPPER': [], 'C_HULL_LOWER': [], 'C_SUPERSTRUCT': [],
        'C_FUNNEL': [], 'C_FUNNEL_TOP': [], 'C_GLASS': [], 'C_WIRE': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. BASEPLATE ENVELOPE (REFERENCE GRID)
    # ==============================================================================
    gx_range = np.linspace(-6.0, 6.0, 25) 
    for gx in gx_range:
        append_segmented(lines, 'C_GRID', np.full_like(gx_range, gx), np.clip(gx_range, -3, 3), np.zeros_like(gx_range))
    gy_range = np.linspace(-3.0, 3.0, 13)
    for gy in gy_range:
        append_segmented(lines, 'C_GRID', np.clip(gx_range, -6, 6), np.full_like(gx_range, gy), np.zeros_like(gx_range))

    # ==============================================================================
    # 2. HYDRODYNAMIC HULL LOFTING TENSOR
    # X bounds: Stern ~ -5.0, Bow ~ 5.5
    # Z bounds: Keel = 0.0, Draft Line = 0.4, Upper Deck = 1.3
    # ==============================================================================
    wl_z = 0.4    # Waterline Draft boundary
    deck_z = 1.3  # Main weather deck boundary
    stations = np.linspace(-5.0, 5.5, 36)
    
    ribs = []
    for x in stations:
        # Beam mapping
        if x > 3.0:    # Tapering Bow
            ratio = (5.5 - x) / 2.5
            w_deck = 0.9 * ratio
            w_wl   = 0.8 * ratio
        elif x < -3.5: # Tapering Cruiser Stern
            ratio = np.sqrt((x - (-5.0)) / 1.5)
            w_deck = 0.8 * ratio + 0.1
            w_wl   = 0.7 * ratio
        else:          # Parallel Midbody
            w_deck = 0.9
            w_wl   = 0.85
            
        w_keel = 0.05
        # Compute exact topological Z heights for this rib
        keel_lift = 0.0
        if x < -4.5: keel_lift = 0.2  # Stern propeller arch
        if x > 4.5:  keel_lift = 0.05 # Minor bow rake
        
        z_pts = [keel_lift, wl_z, deck_z - ((5.5-x)*0.015 if x > 2.0 else 0)]
        y_pts = [w_keel, w_wl, w_deck]
        ribs.append((x, z_pts, y_pts))
        
    # Extrude Ribs (Transverse Frames) and Stringers (Longitudinal Hull Plating)
    for side in [1, -1]:
        # Stringers
        for pt_idx, col_layer in [(0, 'C_HULL_LOWER'), (1, 'C_HULL_UPPER'), (2, 'C_HULL_UPPER')]:
            xs = [r[0] for r in ribs]
            zs = [r[1][pt_idx] for r in ribs]
            ys = [r[2][pt_idx] * side for r in ribs]
            append_segmented(lines, col_layer, xs, ys, zs)
            
        # Hull Section Plating
        for r in ribs:
            x, zs, ys = r[0], r[1], r[2]
            # Draft section
            append_segmented(lines, 'C_HULL_LOWER', [x, x], [ys[0]*side, ys[1]*side], [zs[0], zs[1]])
            # Freeboard section
            append_segmented(lines, 'C_HULL_UPPER', [x, x], [ys[1]*side, ys[2]*side], [zs[1], zs[2]])
            
    # Mid-Deck Portholes Array
    for x in np.linspace(-4.0, 3.5, 18):
        for side in [-1, 1]:
            # Exact mapping directly into the freeboard plate
            append_segmented(lines, 'C_HULL_UPPER', [x-0.05, x+0.05, x+0.05, x-0.05, x-0.05], 
                             [0.85*side]*5, [wl_z+0.35, wl_z+0.35, wl_z+0.45, wl_z+0.45, wl_z+0.35])

    # ==============================================================================
    # 3. SUPERSTRUCTURE TIER MATRIX (Tier 1 Promenade, Tier 2 Boat Deck)
    # ==============================================================================
    # Promenade Deck (Closed in with windows)
    t1_x1, t1_x2 = -3.5, 3.5
    t1_w = 0.8
    t1_zb, t1_zt = deck_z, deck_z + 0.4
    append_segmented(lines, 'C_SUPERSTRUCT', [t1_x1, t1_x2, t1_x2, t1_x1, t1_x1], [-t1_w, -t1_w, t1_w, t1_w, -t1_w], [t1_zt]*5)
    for x in [t1_x1, t1_x2]:
        append_segmented(lines, 'C_SUPERSTRUCT', [x, x, x, x], [-t1_w, -t1_w, t1_w, t1_w], [t1_zb, t1_zt, t1_zt, t1_zb])
    for y in [-t1_w, t1_w]:
        append_segmented(lines, 'C_SUPERSTRUCT', [t1_x1, t1_x2], [y, y], [t1_zb, t1_zb])
        # Promenade Windows
        for px in np.linspace(t1_x1+0.2, t1_x2-0.2, 28):
            append_segmented(lines, 'C_GLASS', [px, px], [y, y], [t1_zb+0.1, t1_zt-0.1])

    # Boat Deck (Upper tiered block)
    t2_x1, t2_x2 = -3.0, 3.0
    t2_w = 0.65
    t2_zb, t2_zt = t1_zt, t1_zt + 0.35
    append_segmented(lines, 'C_SUPERSTRUCT', [t2_x1, t2_x2, t2_x2, t2_x1, t2_x1], [-t2_w, -t2_w, t2_w, t2_w, -t2_w], [t2_zt]*5)
    for x in [t2_x1, t2_x2]:
        append_segmented(lines, 'C_SUPERSTRUCT', [x, x, x, x], [-t2_w, -t2_w, t2_w, t2_w], [t2_zb, t2_zt, t2_zt, t2_zb])
    for y in [-t2_w, t2_w]:
        append_segmented(lines, 'C_SUPERSTRUCT', [t2_x1, t2_x2], [y, y], [t2_zb, t2_zb])

    # Bridge House (Forward commanding block)
    b_x1, b_x2 = 2.4, 3.2
    b_w = 0.7
    b_zb, b_zt = t2_zt, t2_zt + 0.35
    append_segmented(lines, 'C_SUPERSTRUCT', [b_x1, b_x2, b_x2, b_x1, b_x1], [-b_w, -b_w, b_w, b_w, -b_w], [b_zt]*5)
    for y in [-b_w, b_w]:
        append_segmented(lines, 'C_SUPERSTRUCT', [b_x1, b_x2], [y, y], [b_zb, b_zb])
        append_segmented(lines, 'C_SUPERSTRUCT', [b_x1, b_x1], [y, y], [b_zb, b_zt])
        append_segmented(lines, 'C_SUPERSTRUCT', [b_x2, b_x2], [y, y], [b_zb, b_zt])
    # Bridge Windows (Forward facing)
    append_segmented(lines, 'C_GLASS', [b_x2]*2, [-b_w+0.1, b_w-0.1], [b_zb+0.15, b_zb+0.15])
    append_segmented(lines, 'C_GLASS', [b_x2]*2, [-b_w+0.1, b_w-0.1], [b_zt-0.05, b_zt-0.05])
    for wx in np.linspace(-b_w+0.1, b_w-0.1, 7):
        append_segmented(lines, 'C_GLASS', [b_x2, b_x2], [wx, wx], [b_zb+0.15, b_zt-0.05])

    # ==============================================================================
    # 4. EXPLICIT 3-FUNNEL MATRIX (Classic Liner Draft)
    # Raked backward across X axis natively
    # ==============================================================================
    funnel_x = [-1.5, 0.2, 1.9]
    f_r = 0.28
    f_h_main = 1.05
    f_h_cap = 0.25
    f_rake = -0.3 # Pushes the top backwards

    for fx in funnel_x:
        # Lower funnel block (Dense Amber)
        build_raked_cylinder(lines, 'C_FUNNEL', fx, 0.0, t2_zt, f_r, f_h_main, f_rake)
        # Upper exhaust cap (Indestructible Black)
        c_base_x = fx + f_rake
        build_raked_cylinder(lines, 'C_FUNNEL_TOP', c_base_x, 0.0, t2_zt + f_h_main, f_r, f_h_cap, f_rake*0.2)

    # ==============================================================================
    # 5. MASTS & HIGH-TENSION WIRE RIGGING
    # ==============================================================================
    fm_x, fm_h = 4.3, 3.8
    am_x, am_h = -4.0, 3.5
    
    # Fore Mast
    append_segmented(lines, 'C_SUPERSTRUCT', [fm_x, fm_x], [0.0, 0.0], [deck_z, fm_h])
    # Aft Mast
    append_segmented(lines, 'C_SUPERSTRUCT', [am_x, am_x], [0.0, 0.0], [t1_zt, am_h])
    
    # Kinetic Rigging traces (Tethers bow to masts to funnels to stern)
    w_pts = [
        (5.4, deck_z), (fm_x, fm_h-0.2), 
        (funnel_x[2]+f_rake*1.2, t2_zt+f_h_main+f_h_cap),
        (funnel_x[1]+f_rake*1.2, t2_zt+f_h_main+f_h_cap),
        (funnel_x[0]+f_rake*1.2, t2_zt+f_h_main+f_h_cap),
        (am_x, am_h-0.2), (-4.8, deck_z)
    ]
    for k in range(len(w_pts)-1):
        append_segmented(lines, 'C_WIRE', [w_pts[k][0], w_pts[k+1][0]], [0.0, 0.0], [w_pts[k][1], w_pts[k+1][1]])

    return lines

# ------------------------------------------------------------------
# PARALLEL GENERATOR STREAM (KINEMATIC TIMELINE TENSOR)
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_ship_vectors() # Computed once for true O(1) loop retrieval
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Central Basepoint: Mapping exact structural centroid of the vessel
        cam_x, cam_y, cam_z = 0.0, 0.0, 1.2 
        
        # Continuous 360-degree perfect orbital synchronisation
        # Initiates precisely from Left Side Profile (Azimuth = -90.0)
        azimuth = -90.0 - (stage * 360.0)

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

    # Cinematic Rigid Map Boundary - Covers the massive ~11m longitudinal hull
    cam_span = 6.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []

    # 1. PROCESS STRUCTURAL VECTOR MATRIX
    for c_key, c_val in [('C_GRID', C_GRID), ('C_HULL_LOWER', C_HULL_LOWER), ('C_HULL_UPPER', C_HULL_UPPER), 
                         ('C_SUPERSTRUCT', C_SUPERSTRUCT), ('C_FUNNEL', C_FUNNEL), ('C_FUNNEL_TOP', C_FUNNEL_TOP), 
                         ('C_GLASS', C_GLASS), ('C_WIRE', C_WIRE)]:
        
        if c_key == 'C_GRID': lw, alpha = 0.8, 0.4
        elif c_key == 'C_HULL_LOWER': lw, alpha = 1.3, 1.0     
        elif c_key == 'C_HULL_UPPER': lw, alpha = 1.4, 1.0      
        elif c_key == 'C_SUPERSTRUCT': lw, alpha = 1.2, 1.0  
        elif c_key == 'C_FUNNEL': lw, alpha = 1.3, 1.0   
        elif c_key == 'C_FUNNEL_TOP': lw, alpha = 1.5, 1.0   
        elif c_key == 'C_GLASS': lw, alpha = 1.0, 1.0   
        elif c_key == 'C_WIRE': lw, alpha = 0.7, 1.0   
        else: lw, alpha = 1.0, 1.0
            
        for xl, yl, zl in static_rig[c_key]:
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=22.0)
            render_queue.append((np.mean(depth), u, v-0.6, c_val, lw, alpha))

    # 2. ABSOLUTE PAINTER'S ALGORITHM
    render_queue.sort(key=lambda item: item[0], reverse=True)

    for depth, u, v, c, lw, a in render_queue:
        ax.plot(u, v, color=c, lw=lw, alpha=a)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (TOP HUD)
    # ------------------------------------------------------------------
    ui_t = cam_span * 1.45
    ax.add_patch(patches.Rectangle((-cam_span, ui_t), cam_span*2, 8.0, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_t, ui_t], color=C_TEXT, lw=6, zorder=81)

    ax.text(-cam_span*0.95, ui_t+1.0, "LG-449q // MACRO-ENGINEERING TENSOR: NAVAL ARCHITECTURE", color=C_TEXT, fontsize=17, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t+0.3, "EXPLICIT TRUE-SCALE GEOMETRY // OCEAN LINER MATRIX", color=C_HULL_UPPER, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b+1.0, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_FUNNEL, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.5, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS SYNCHRONISATION)", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.1, "HULL YIELD       : TRUE DISPLACEMENT / HYDRODYNAMIC TENSOR SECURED", color=C_HULL_LOWER, fontsize=13, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-449q: NAVAL ARCHITECTURE TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Hydrodynamic Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
