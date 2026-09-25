"""
PROJECT: Logic Garden 450x (Exact Physical Construct // HMS Victorious (R38) Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: HMS VICTORIOUS, AIRCRAFT CARRIER, ROYAL NAVY, MARITIME, WIREFRAME, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: True angled flight deck, massive Type 984 radar, hurricane bow lofting.
- Strict Bounds Protocol: Core locked at origin. cam_span scaled to 140.0 for flawless, unclipped 100% full-body framing of the 237m object.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from absolute 115-degree dramatic front-quarter angle.
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
OUT_DIR = "frames_450x_victorious"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Ocean Baseplate Reference)

C_HULL_MAIN = '#94A3B8'          # Heavy Slate (Upper Freeboard / Superstructure)
C_HULL_DARK = '#475569'          # Machined Slate (Lower Draught / Radar Base)
C_DECK      = '#64748B'          # Armoured Steel (Flight Deck Plateau)
C_DETAILS   = '#1E293B'          # Carbon Slate (Masts, Propellers, Sponsons)
C_ACCENT    = '#E11D48'          # Kinematic Red (Runway Markings / Deck Warnings)
C_RADAR     = '#FFB300'          # Dense Gold (Type 984 3D Radar Lens)

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

def add_sym_quad(lines_dict, col, p1, p2, p3, p4, u_steps=4, v_steps=4):
    add_quad_mesh(lines_dict, col, p1, p2, p3, p4, u_steps, v_steps)
    if any(abs(p[1]) > 0.001 for p in [p1, p2, p3, p4]):
        add_quad_mesh(lines_dict, col, (p1[0], -p1[1], p1[2]), (p2[0], -p2[1], p2[2]), 
                                       (p3[0], -p3[1], p3[2]), (p4[0], -p4[1], p4[2]), u_steps, v_steps)

def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='z', rings=4, t_count=16):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, length, rings)
    for s in steps:
        if axis == 'x':  ix, iy, iz = np.full_like(t, cx + s), cy + radius*np.cos(t), cz + radius*np.sin(t)
        elif axis == 'y': ix, iy, iz = cx + radius*np.cos(t), np.full_like(t, cy + s), cz + radius*np.sin(t)
        else:             ix, iy, iz = cx + radius*np.cos(t), cy + radius*np.sin(t), np.full_like(t, cz + s)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        if axis == 'x':   sx, sy, sz = cx + steps, [cy + radius*np.cos(a)]*rings, [cz + radius*np.sin(a)]*rings
        elif axis == 'y': sx, sy, sz = [cx + radius*np.cos(a)]*rings, cy + steps, [cz + radius*np.sin(a)]*rings
        else:             sx, sy, sz = [cx + radius*np.cos(a)]*rings, [cy + radius*np.sin(a)]*rings, cz + steps
        append_segmented(lines_dict, col, sx, sy, sz)

def add_dome(lines_dict, col, cx, cy, cz, radius, axis='z', dir=1, rings=4, t_count=16):
    p_step = np.linspace(0, np.pi/2, rings)
    for p in p_step:
        r_s = radius * np.cos(p)
        h_s = radius * np.sin(p) * dir
        t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
        if axis == 'z':
            ix, iy, iz = cx + r_s*np.cos(t), cy + r_s*np.sin(t), np.full_like(t, cz + h_s)
            append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        rr = radius * np.cos(p_step)
        hh = radius * np.sin(p_step) * dir
        if axis == 'z':
            sx, sy, sz = cx + rr*np.cos(a), cy + rr*np.sin(a), cz + hh
            append_segmented(lines_dict, col, list(sx), list(sy), list(sz))

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (HMS VICTORIOUS R38)
# ------------------------------------------------------------------
def generate_carrier_static():
    lines = {
        'C_HULL_MAIN': [], 'C_HULL_DARK': [], 'C_DECK': [], 
        'C_DETAILS': [], 'C_ACCENT': [], 'C_RADAR': [], 'C_GRID': []
    }

    # 1. BASEPLATE ENVELOPE (REFERENCE GRID - Sea Level)
    Z_FLOOR = 0.0
    gx_range = np.linspace(-150.0, 150.0, 21)
    gy_range = np.linspace(-100.0, 100.0, 15)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # Real-world dimensions: 237m Length. Use X from +118.5 (Bow) to -118.5 (Stern)
    X_BOW = 118.0; X_STERN = -118.0
    Z_DECK = 14.5; Z_KEEL = -9.0
    Y_HULL = 15.5 # 31m beam

    # ==============================================================================
    # 2. CONTINUOUS HULL LOFTING (Hurricane Bow & Carrier Belly)
    # ==============================================================================
    # Upper Freeboard (Sea level to Flight Deck)
    x_st = [118.0, 110.0,  90.0,  50.0,   0.0, -50.0, -90.0, -118.0]
    ry_b = [  0.0,   5.0,  12.0,  15.5,  15.5,  15.5,  12.0,    6.0]
    ry_d = [ 12.0,  14.0,  16.0,  17.0,  17.0,  17.0,  17.0,   16.0] # Starboard deck edge flare
    
    for i in range(len(x_st)-1):
        x1, x2 = x_st[i], x_st[i+1]
        
        # Starboard side freeboard flare
        add_quad_mesh(lines, 'C_HULL_MAIN', (x1, -ry_b[i], Z_FLOOR), (x2, -ry_b[i+1], Z_FLOOR), (x2, -ry_d[i+1], Z_DECK), (x1, -ry_d[i], Z_DECK), u_steps=3, v_steps=4)
        
        # Port side (Main hull flare, before angled deck protrusion)
        add_quad_mesh(lines, 'C_HULL_MAIN', (x1, ry_b[i], Z_FLOOR), (x2, ry_b[i+1], Z_FLOOR), (x2, ry_d[i+1], Z_DECK), (x1, ry_d[i], Z_DECK), u_steps=3, v_steps=4)
        
        # Underwater Hull (-9m Draught to Sea Level)
        ru_k = [0.0, 2.0, 7.0, 11.0, 12.0, 11.0, 7.0, 4.0]
        # Starboard below
        add_quad_mesh(lines, 'C_HULL_DARK', (x1, -ru_k[i], Z_KEEL), (x2, -ru_k[i+1], Z_KEEL), (x2, -ry_b[i+1], Z_FLOOR), (x1, -ry_b[i], Z_FLOOR), u_steps=3, v_steps=3)
        # Port below
        add_quad_mesh(lines, 'C_HULL_DARK', (x1, ru_k[i], Z_KEEL), (x2, ru_k[i+1], Z_KEEL), (x2, ry_b[i+1], Z_FLOOR), (x1, ry_b[i], Z_FLOOR), u_steps=3, v_steps=3)

    # Transom Stern Closing
    add_quad_mesh(lines, 'C_HULL_MAIN', (-118.0, 6.0, Z_FLOOR), (-118.0, 16.0, Z_DECK), (-118.0, -16.0, Z_DECK), (-118.0, -6.0, Z_FLOOR), u_steps=4, v_steps=2)
    add_quad_mesh(lines, 'C_HULL_DARK', (-118.0, 4.0, Z_KEEL), (-118.0, 6.0, Z_FLOOR), (-118.0, -6.0, Z_FLOOR), (-118.0, -4.0, Z_KEEL), u_steps=4, v_steps=2)

    # ==============================================================================
    # 3. ANGLED FLIGHT DECK (The 8.75-Degree Port Extrusion)
    # ==============================================================================
    # Primary Axial Base Plateau
    add_quad_mesh(lines, 'C_DECK', (118.0, -12.0, Z_DECK), (118.0, 12.0, Z_DECK), (-118.0, 16.0, Z_DECK), (-118.0, -16.0, Z_DECK), u_steps=12, v_steps=6)
    
    # Fully Asymmetric Angled Port Runway Sponson
    A_START = 60.0; A_END = -118.0
    A_PORT_MAX = 33.0
    add_quad_mesh(lines, 'C_DECK', (A_START, 17.0, Z_DECK), (A_START-30, A_PORT_MAX, Z_DECK), (A_END, A_PORT_MAX+1, Z_DECK), (A_END, 16.0, Z_DECK), u_steps=8, v_steps=4)

    # Structural struts supporting the massive angled overhang
    for x_s in np.linspace(A_START-20, A_END+10, 8):
        append_segmented(lines, 'C_DETAILS', [x_s, x_s], [15.5, (A_PORT_MAX - 5)], [Z_FLOOR + 4, Z_DECK])
        
    # Runway Extrusions & Markings
    append_segmented(lines, 'C_ACCENT', [110, -112], [0, 0], [Z_DECK+0.1, Z_DECK+0.1])          # Axial centre
    append_segmented(lines, 'C_ACCENT', [50, -115], [10, 30], [Z_DECK+0.1, Z_DECK+0.1])         # Angled centre
    add_quad_mesh(lines, 'C_ACCENT', (-110, 24, Z_DECK+0.1), (-112, 24, Z_DECK+0.1), (-112, 32, Z_DECK+0.1), (-110, 32, Z_DECK+0.1), u_steps=1, v_steps=1) # Arresting gear zone

    # ==============================================================================
    # 4. ISLAND SUPERSTRUCTURE & MASSIVE TYPE 984 RADAR
    # ==============================================================================
    # The island sits tight to the Starboard edge. (Y = -12 to -22)
    ISL_X = -10.0; ISL_Y = -16.0 # Center of island mass
    
    # Bridge Block
    add_quad_mesh(lines, 'C_HULL_MAIN', (ISL_X+25, ISL_Y-5, Z_DECK), (ISL_X+25, ISL_Y+5, Z_DECK), (ISL_X-35, ISL_Y+5, Z_DECK), (ISL_X-35, ISL_Y-5, Z_DECK), u_steps=6, v_steps=2)
    add_quad_mesh(lines, 'C_HULL_MAIN', (ISL_X+20, ISL_Y-4, Z_DECK+10), (ISL_X+20, ISL_Y+4, Z_DECK+10), (ISL_X-30, ISL_Y+4, Z_DECK+10), (ISL_X-30, ISL_Y-4, Z_DECK+10), u_steps=5, v_steps=2)
    
    # Bridge Front Windows (Deep Marine)
    add_quad_mesh(lines, 'C_DETAILS', (ISL_X+20, ISL_Y-4, Z_DECK+10), (ISL_X+20, ISL_Y+4, Z_DECK+10), (ISL_X+25, ISL_Y+5, Z_DECK), (ISL_X+25, ISL_Y-5, Z_DECK), u_steps=2, v_steps=4)

    # Secondary Tower / Mast Base
    add_cylinder(lines, 'C_HULL_DARK', cx=ISL_X-15, cy=ISL_Y, cz=Z_DECK+10, length=12.0, radius=3.0, axis='z', rings=3, t_count=12)
    add_cylinder(lines, 'C_DETAILS', cx=ISL_X-15, cy=ISL_Y, cz=Z_DECK+22, length=15.0, radius=0.5, axis='z', rings=2, t_count=6) # Central Mast
    
    # Type 984 "Dustbin" 3D Radar System (Focal Asset)
    R_CX = ISL_X + 15
    R_CZ = Z_DECK + 15
    # Heavy rotational mount
    add_cylinder(lines, 'C_HULL_DARK', cx=R_CX, cy=ISL_Y, cz=Z_DECK+10, length=5.0, radius=3.5, axis='z', rings=2, t_count=16)
    # The gigantic hemispherical radar lens itself
    add_dome(lines, 'C_RADAR', cx=R_CX, cy=ISL_Y, cz=R_CZ, radius=5.5, axis='z', dir=1, rings=6, t_count=20)
    # The flat radar face (slanted downward slightly for array scanning)
    add_quad_mesh(lines, 'C_RADAR', (R_CX+2, ISL_Y-5.5, R_CZ+5.5), (R_CX+2, ISL_Y+5.5, R_CZ+5.5), (R_CX+4, ISL_Y+5.5, R_CZ-1), (R_CX+4, ISL_Y-5.5, R_CZ-1), u_steps=4, v_steps=6)

    # Funnel (Exhaust Stack)
    add_quad_mesh(lines, 'C_DETAILS', (ISL_X, ISL_Y-3, Z_DECK+10), (ISL_X, ISL_Y+3, Z_DECK+10), (ISL_X-10, ISL_Y+3, Z_DECK+10), (ISL_X-10, ISL_Y-3, Z_DECK+10), u_steps=2, v_steps=2)
    add_quad_mesh(lines, 'C_HULL_DARK', (ISL_X, ISL_Y-2, Z_DECK+18), (ISL_X, ISL_Y+2, Z_DECK+18), (ISL_X-8, ISL_Y+2, Z_DECK+18), (ISL_X-8, ISL_Y-2, Z_DECK+18), u_steps=2, v_steps=2)

    # ==============================================================================
    # 5. PROPULSION & SENSORS (Lower Mechanics)
    # ==============================================================================
    # Twin Propellers and Rudders
    for y_p in [-5.0, 5.0]:
        # Propeller Shafts
        append_segmented(lines, 'C_DETAILS', [-80.0, -95.0], [y_p*0.8, y_p], [-5.0, -7.0])
        add_cylinder(lines, 'C_HULL_DARK', cx=-95.0, cy=y_p, cz=-7.0, length=2.0, radius=0.8, axis='x', rings=2, t_count=8)
        # Blades
        append_segmented(lines, 'C_DETAILS', [-96.0, -96.0], [y_p-2, y_p+2], [-7.0, -7.0])
        append_segmented(lines, 'C_DETAILS', [-96.0, -96.0], [y_p, y_p], [-9.0, -5.0])
        # Twin Rudders
        add_quad_mesh(lines, 'C_DETAILS', (-100, y_p, -2.0), (-100, y_p, -8.0), (-105, y_p, -8.0), (-108, y_p, -2.0), u_steps=2, v_steps=2)

    # Port and Starboard Lateral Sponsons / Crane housing
    add_quad_mesh(lines, 'C_DETAILS', (-20, 17, Z_DECK-2), (-50, 17, Z_DECK-2), (-50, 20, Z_DECK-2), (-20, 20, Z_DECK-2), u_steps=3, v_steps=1)
    add_quad_mesh(lines, 'C_DETAILS', (-20, -17, Z_DECK-2), (-50, -17, Z_DECK-2), (-50, -20, Z_DECK-2), (-20, -20, Z_DECK-2), u_steps=3, v_steps=1)

    return lines

# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_carrier_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking the geometric True Center of the colossal 237m carrier
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.0
        
        # Starts explicitly from 115-degrees (Dramatic front-quarter aesthetic tracking massive hurricane bow)
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
    # Anchor = 0.0. Total vessel length is 237m.
    # Setting cam_span safely to 140.0 to yield 280.0m horizontal footprint isolating bow to stern.
    # Vertical bounds output 140.0 * 1.777 = 248.7m (x2 = 497.5m height allowed).
    # Perfectly frames the super-massive static stance unconditionally escaping visual logic layers.
    cam_span = 140.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.6, 0.3), 
        ('C_HULL_DARK', C_HULL_DARK, 1.3, 1.0),
        ('C_HULL_MAIN', C_HULL_MAIN, 1.2, 1.0),
        ('C_DECK',      C_DECK,      1.1, 1.0),
        ('C_DETAILS',   C_DETAILS,   1.2, 1.0),
        ('C_RADAR',     C_RADAR,     1.5, 1.0),
        ('C_ACCENT',    C_ACCENT,    1.6, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +16 degrees to prominently display the massive angled deck geometry and radar island
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-450x // MARITIME KINEMATICS: OPERATIONS RESEARCH", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // HMS VICTORIOUS (R38) MATRIX", color=C_DECK, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_RADAR, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: 8.75-DEGREE ANGLED FLIGHT DECK / TYPE 984 RADAR", color=C_DETAILS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-450x: HMS VICTORIOUS ENGINERING TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Maritime Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
