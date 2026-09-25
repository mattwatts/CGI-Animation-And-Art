"""
PROJECT: Logic Garden 450y (Exact Physical Construct // USS Independence LCS-2 Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: USS INDEPENDENCE, LCS-2, NAVY, MARITIME, TRIMARAN, WIREFRAME, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: True Trimaran hull, massive aft flight deck, faceted stealth superstructure.
- Strict Bounds Protocol: Core locked at origin. cam_span scaled to 75.0 for flawless, unclipped 100% full-body framing of the 127.4m object.
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
OUT_DIR = "frames_450y_independence"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Ocean Baseplate Reference)

C_HULL_MAIN = '#94A3B8'          # Heavy Slate (Upper Freeboard & Superstructure)
C_HULL_DARK = '#475569'          # Machined Slate (Lower Draught, Waterjets)
C_DECK      = '#64748B'          # Armoured Steel (Trimaran Flight Deck)
C_DETAILS   = '#1E293B'          # Carbon Slate (Gun Turret, Masts, Vents)
C_ACCENT    = '#E11D48'          # Kinematic Red (Runway Markings / Hazard Bounds)

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
        append_sym(lines_dict, col, sx, sy, sz)

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (USS INDEPENDENCE LCS-2)
# ------------------------------------------------------------------
def generate_trimaran_static():
    lines = {
        'C_HULL_MAIN': [], 'C_HULL_DARK': [], 'C_DECK': [], 
        'C_DETAILS': [], 'C_ACCENT': [], 'C_GRID': []
    }

    # 1. BASEPLATE ENVELOPE (REFERENCE ORBITAL GRID)
    Z_FLOOR = 0.0
    gx_range = np.linspace(-80.0, 80.0, 21)
    gy_range = np.linspace(-40.0, 40.0, 9)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # Real-world dimensions: 127.4m Length x 31.6m Beam.
    X_BOW = 63.7; X_STERN = -63.7
    Z_DECK = 9.0; Z_KEEL = -4.5
    BEAM = 15.8

    # ==============================================================================
    # 2. TRIMARAN HULL LOFTING (Central Keel & Twin Amas)
    # ==============================================================================
    # Core Slender Hull
    x_core = [X_BOW, 50.0, 30.0, 10.0, -20.0, X_STERN]
    y_core = [0.0, 2.5, 4.0, 4.5, 4.5, 4.5]
    z_keel = [-0.5, -2.5, -4.0, -4.5, -4.5, -4.0]
    
    for i in range(len(x_core)-1):
        x1, x2 = x_core[i], x_core[i+1]
        
        # Central hull upper freeboard (Sea level to Deck)
        add_sym_quad(lines, 'C_HULL_MAIN', (x1, y_core[i], Z_FLOOR), (x1, y_core[i], Z_DECK), (x2, y_core[i+1], Z_DECK), (x2, y_core[i+1], Z_FLOOR), u_steps=2, v_steps=2)
        # Central hull draft (Keel to Sea level)
        add_sym_quad(lines, 'C_HULL_DARK', (x1, 0, z_keel[i]), (x1, y_core[i], Z_FLOOR), (x2, y_core[i+1], Z_FLOOR), (x2, 0, z_keel[i+1]), u_steps=2, v_steps=2)

    # Lateral Outriggers (Amas) forming the Trimaran Span
    x_ama = [20.0, 0.0, -20.0, X_STERN]
    y_ama_in = [4.5, 5.0, 7.0, 8.0]
    y_ama_out = [4.5, 12.0, 15.8, 15.8]
    z_ama_k = [0.0, -1.0, -2.5, -2.5]
    
    for i in range(len(x_ama)-1):
        x1, x2 = x_ama[i], x_ama[i+1]
        
        # Outer Face of Outrigger
        add_sym_quad(lines, 'C_HULL_MAIN', (x1, y_ama_out[i], Z_FLOOR), (x1, y_ama_out[i], Z_DECK), (x2, y_ama_out[i+1], Z_DECK), (x2, y_ama_out[i+1], Z_FLOOR), u_steps=3, v_steps=3)
        # Inner Face of Outrigger
        add_sym_quad(lines, 'C_HULL_DARK', (x1, y_ama_in[i], Z_FLOOR), (x1, y_ama_out[i], Z_FLOOR), (x2, y_ama_out[i+1], Z_FLOOR), (x2, y_ama_in[i+1], Z_FLOOR), u_steps=2, v_steps=2)
        # Underwater Ama Keel
        add_sym_quad(lines, 'C_HULL_DARK', (x1, (y_ama_in[i]+y_ama_out[i])/2, z_ama_k[i]), (x1, y_ama_out[i], Z_FLOOR), (x2, y_ama_out[i+1], Z_FLOOR), (x2, (y_ama_in[i+1]+y_ama_out[i+1])/2, z_ama_k[i+1]), u_steps=2, v_steps=2)
        add_sym_quad(lines, 'C_HULL_DARK', (x1, y_ama_in[i], Z_FLOOR), (x1, (y_ama_in[i]+y_ama_out[i])/2, z_ama_k[i]), (x2, (y_ama_in[i+1]+y_ama_out[i+1])/2, z_ama_k[i+1]), (x2, y_ama_in[i+1], Z_FLOOR), u_steps=2, v_steps=2)
        # Bridging Deck (connecting central hull to outriggers)
        add_sym_quad(lines, 'C_HULL_DARK', (x1, y_core[3] if i==0 else y_core[4], Z_DECK), (x1, y_ama_out[i], Z_DECK), (x2, y_ama_out[i+1], Z_DECK), (x2, y_core[4] if i<=1 else y_core[5], Z_DECK), u_steps=3, v_steps=1)

    # Transom Stern Geometry (Closing off the rear)
    add_sym_quad(lines, 'C_HULL_MAIN', (X_STERN, 0, Z_FLOOR), (X_STERN, 0, Z_DECK), (X_STERN, BEAM, Z_DECK), (X_STERN, BEAM, Z_FLOOR), u_steps=4, v_steps=2)

    # ==============================================================================
    # 3. MASSIVE AVIATION FLIGHT DECK
    # ==============================================================================
    # The enormous flat deck explicitly covers the entire aft boundary
    add_sym_quad(lines, 'C_DECK', (0.0, 0, Z_DECK), (0.0, 12.0, Z_DECK), (X_STERN, BEAM, Z_DECK), (X_STERN, 0, Z_DECK), u_steps=8, v_steps=8)
    
    # Helipad Warning Bounds and Centreline Runway Markings
    append_segmented(lines, 'C_ACCENT', [0.0, X_STERN+2.0], [0.0, 0.0], [Z_DECK+0.1, Z_DECK+0.1])
    add_sym_quad(lines, 'C_ACCENT', (-10.0, 0, Z_DECK+0.1), (-10.0, 8.0, Z_DECK+0.1), (-55.0, 8.0, Z_DECK+0.1), (-55.0, 0, Z_DECK+0.1), u_steps=1, v_steps=1)

    # ==============================================================================
    # 4. FACETED STEALTH SUPERSTRUCTURE
    # ==============================================================================
    # Lower Tier Bridge Block (Sloping strictly inwards perfectly reflecting radar waves)
    SS_F = 35.0; SS_A = -5.0
    SS_Z1 = 16.0
    add_sym_quad(lines, 'C_HULL_MAIN', (SS_F, 0, Z_DECK), (SS_F, 8.0, Z_DECK), (SS_F-5, 6.0, SS_Z1), (SS_F-5, 0, SS_Z1), u_steps=3, v_steps=3) # Forward Facet
    add_sym_quad(lines, 'C_HULL_MAIN', (SS_A, 12.0, Z_DECK), (SS_F, 8.0, Z_DECK), (SS_F-5, 6.0, SS_Z1), (SS_A, 8.0, SS_Z1), u_steps=5, v_steps=3) # Lateral Facets
    add_sym_quad(lines, 'C_HULL_MAIN', (SS_A, 0, Z_DECK), (SS_A, 12.0, Z_DECK), (SS_A, 8.0, SS_Z1), (SS_A, 0, SS_Z1), u_steps=3, v_steps=3) # Aft Wall
    
    # Upper Tier / Integrated Phased Array Mast
    SS_Z2 = 24.0; M_F = 25.0; M_A = 5.0
    add_sym_quad(lines, 'C_HULL_MAIN', (M_F, 0, SS_Z1), (M_F, 6.0, SS_Z1), (M_F-3, 3.0, SS_Z2), (M_F-3, 0, SS_Z2), u_steps=2, v_steps=2)
    add_sym_quad(lines, 'C_HULL_MAIN', (M_A, 8.0, SS_Z1), (M_F, 6.0, SS_Z1), (M_F-3, 3.0, SS_Z2), (M_A+2, 4.0, SS_Z2), u_steps=3, v_steps=2)
    add_sym_quad(lines, 'C_HULL_MAIN', (M_A, 0, SS_Z1), (M_A, 8.0, SS_Z1), (M_A+2, 4.0, SS_Z2), (M_A+2, 0, SS_Z2), u_steps=2, v_steps=2)

    # Mast Tower Spire
    add_cylinder(lines, 'C_DETAILS', cx=15.0, cy=0.0, cz=SS_Z2, length=12.0, radius=0.6, axis='z', rings=3, t_count=8)

    # Bridge Windows (High Contrast Black logic slits)
    add_sym_quad(lines, 'C_DETAILS', (31.0, 0.5, 14.5), (31.0, 5.0, 14.5), (28.5, 5.5, 12.0), (28.5, 0.5, 12.0), u_steps=1, v_steps=2)

    # ==============================================================================
    # 5. FOREDECK ARMAMENT & WATERJET EXHAUSTS
    # ==============================================================================
    # 57mm Bofors Naval Gun
    add_cylinder(lines, 'C_HULL_MAIN', cx=45.0, cy=0.0, cz=Z_DECK, length=1.2, radius=1.5, axis='z', rings=2, t_count=12) # Turret Base
    add_cylinder(lines, 'C_DETAILS', cx=46.5, cy=0.0, cz=Z_DECK+0.8, length=4.0, radius=0.15, axis='x', rings=2, t_count=6) # Barrel

    # Waterjet Propulsion (4 directional jet cylinders at stern instead of props)
    for y_wj in [2.5, 7.5]:
        # Twin steerable jet housings embedded below the water line
        add_cylinder(lines, 'C_HULL_DARK', cx=X_STERN-0.5, cy=y_wj, cz=-1.5, length=3.0, radius=1.1, axis='x', rings=3, t_count=12)
        add_cylinder(lines, 'C_HULL_DARK', cx=X_STERN-0.5, cy=-y_wj, cz=-1.5, length=3.0, radius=1.1, axis='x', rings=3, t_count=12)

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_trimaran_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking the geometric True Center of the 127.4m hull
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.0
        
        # Starts explicitly from 115-degrees (Dramatic front-quarter aesthetic tracking the wave-piercing bow)
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
    # Anchor = 0.0. Total vessel length is 127.4m. Transverse span 31.6m.
    # Setting cam_span safely to 75.0 to yield 150.0m horizontal footprint isolating bow to stern.
    # Vertical bounds output 75.0 * 1.777 = 133.2m (x2 = 266.4m height allowed).
    # Perfectly frames the super-massive static stance unconditionally escaping visual logic layers.
    cam_span = 75.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.6, 0.3), 
        ('C_HULL_DARK', C_HULL_DARK, 1.3, 1.0),
        ('C_HULL_MAIN', C_HULL_MAIN, 1.2, 1.0),
        ('C_DECK',      C_DECK,      1.1, 1.0),
        ('C_DETAILS',   C_DETAILS,   1.3, 1.0),
        ('C_ACCENT',    C_ACCENT,    1.6, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +14 degrees to prominent display the huge trimaran aviation deck and faceted bridge
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-450y // MARITIME KINEMATICS: OPERATIONS RESEARCH", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // USS INDEPENDENCE (LCS-2) MATRIX", color=C_HULL_DARK, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_DECK, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: STEALTH TRIMARAN ARCHITECTURE / WATERJET PROPULSION", color=C_DETAILS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-450y: USS INDEPENDENCE KINEMATICS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Maritime Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
