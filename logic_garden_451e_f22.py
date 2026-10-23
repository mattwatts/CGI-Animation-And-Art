"""
PROJECT: Logic Garden 451e (Exact Physical Construct // F-22 Raptor Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: F-22, RAPTOR, STEALTH, AEROSPACE, WIREFRAME, ENGINEERING, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Canted vertical stabilisers, diamond-delta wings, 2D thrust vectoring nozzles.
- Strict Bounds Protocol: Core locked at origin. cam_span scaled to 12.0 for flawless, unclipped 100% full-body framing.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from absolute 115-degree dramatic front-quarter angle.
- Daylight Palette (White Substrate / High-Contrast Edge Geometry).
- Purged Jargon. Australian spelling conventions (maths, colour, kilometres, aeroplane, manoeuvre, synchronisation).
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
OUT_DIR = "frames_451e_f22"
os.makedirs(OUT_DIR, exist_ok=True)

VELOCITY = 30.0  # m/s aerospace grid translation

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Translating Sub-orbital Plane)

C_HULL_MAIN = '#94A3B8'          # Heavy Slate (Primary Stealth Facets & Wings)
C_HULL_DARK = '#475569'          # Machined Slate (Intake ramps, Weapon Bay edges)
C_WEDGE     = '#1E293B'          # Carbon Slate (Heavy Empennage Geometry)
C_COCKPIT   = '#111115'          # Indestructible Black (Frameless Canopy & Radar Arrays)
C_ENGINE    = '#E11D48'          # Kinematic Red (2D Thrust Vectoring Exhausts)

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

# ------------------------------------------------------------------
# SUPERSTRUCTURE BUILDERS (LOCKHEED MARTIN F-22 RAPTOR)
# ------------------------------------------------------------------
def generate_f22_dynamic(t_sec):
    lines = {
        'C_HULL_MAIN': [], 'C_HULL_DARK': [], 'C_WEDGE': [], 
        'C_COCKPIT': [], 'C_ENGINE': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. TRANSLATING BASEPLATE ENVELOPE (Kinetic Flight Simulation)
    # ==============================================================================
    Z_FLOOR = -5.0
    travel_offset = (t_sec * VELOCITY) % 2.0  # Seamless looping threshold
    
    gx_range = np.linspace(-20.0, 20.0, 21)
    gy_range = np.linspace(-15.0, 15.0, 16)
    
    for gx in gx_range: 
        shift_x = gx - travel_offset
        append_segmented(lines, 'C_GRID', np.full_like(gy_range, shift_x), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: 
        append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # Real-world F-22 dimensions: Length 18.92m, Wingspan 13.56m
    # Kinematic Center: X=0
    X_NOSE = 9.45
    X_TAIL = -9.45

    # ==============================================================================
    # 2. FACETED STEALTH FUSELAGE & CHINES
    # ==============================================================================
    # The extreme continuous blended chine edges from nose to wing root
    x_chines = [X_NOSE, 7.0, 5.0, 3.5, 0.0, -5.0, -7.5, X_TAIL]
    y_chines = [0.0,    0.6, 1.3, 1.9,  2.2, 2.2, 1.8,  1.5]
    z_chines = [0.0,    0.0, 0.0, 0.0,  0.0, 0.0, 0.0,  0.0]

    # Upper Fuselage Spine (Dorsal)
    z_spine = [0.0, 0.4, 0.7, 0.8, 0.8, 0.6, 0.4, 0.3]
    y_spine = [0.0, 0.0, 0.5, 0.8, 1.0, 1.0, 0.8, 0.8]

    # Lower Fuselage Belly (Ventral - Weapon Bays)
    z_belly = [0.0, -0.4, -0.6, -0.8, -0.8, -0.7, -0.5, -0.4]
    y_belly = [0.0,  0.0,  0.4,  0.6,  0.8,  0.8,  0.7,  0.7]

    for i in range(len(x_chines)-1):
        x1, x2 = x_chines[i], x_chines[i+1]
        
        # Upper Forward / Central Dorsal Facets
        add_sym_quad(lines, 'C_HULL_MAIN', 
            (x1, y_spine[i], z_spine[i]), (x2, y_spine[i+1], z_spine[i+1]), 
            (x2, y_chines[i+1], z_chines[i+1]), (x1, y_chines[i], z_chines[i]), u_steps=3, v_steps=2)
            
        # Lower Forward / Central Ventral Facets (Belly)
        add_sym_quad(lines, 'C_HULL_DARK', 
            (x1, y_belly[i], z_belly[i]), (x2, y_belly[i+1], z_belly[i+1]), 
            (x2, y_chines[i+1], z_chines[i+1]), (x1, y_chines[i], z_chines[i]), u_steps=3, v_steps=2)

    # Centreline Dorsal Ridge closing the gap
    for i in range(len(x_chines)-1):
        if y_spine[i] > 0.01 or y_spine[i+1] > 0.01:
            add_sym_quad(lines, 'C_HULL_MAIN', 
                (x_chines[i], 0.0, z_spine[i]), (x_chines[i+1], 0.0, z_spine[i+1]), 
                (x_chines[i+1], y_spine[i+1], z_spine[i+1]), (x_chines[i], y_spine[i], z_spine[i]), u_steps=2, v_steps=2)
            add_sym_quad(lines, 'C_HULL_DARK', 
                (x_chines[i], 0.0, z_belly[i]), (x_chines[i+1], 0.0, z_belly[i+1]), 
                (x_chines[i+1], y_belly[i+1], z_belly[i+1]), (x_chines[i], y_belly[i], z_belly[i]), u_steps=2, v_steps=2)

    # ==============================================================================
    # 3. ADVANCED TACTICAL FIGHTER INTAKES
    # ==============================================================================
    # Iconic rhomboidal/swept side air intakes
    IX_FWD = 3.5; IX_AFT = 1.0
    IY_IN = 1.0; IY_OUT = 1.9
    IZ_TOP = 0.2; IZ_BOT = -0.8
    
    # Slanted outward intake aperture edge geometry
    add_sym_quad(lines, 'C_HULL_DARK', (IX_FWD, IY_IN, IZ_TOP), (IX_FWD-1.0, IY_OUT, IZ_TOP), (IX_FWD-1.0, IY_OUT, IZ_BOT), (IX_FWD, IY_IN, IZ_BOT), u_steps=2, v_steps=2)
    # Ducting swept back into fuselage body
    add_sym_quad(lines, 'C_HULL_DARK', (IX_FWD-1.0, IY_OUT, IZ_TOP), (IX_AFT, 2.2, 0.0), (IX_AFT, 2.2, -0.6), (IX_FWD-1.0, IY_OUT, IZ_BOT), u_steps=3, v_steps=2)

    # ==============================================================================
    # 4. FRAMELESS BUBBLE CANOPY
    # ==============================================================================
    # Stepless gold-tinted (rendered black) radar reflective canopy
    add_sym_quad(lines, 'C_COCKPIT', (6.5, 0.0, 0.4), (4.5, 0.0, 1.3), (4.5, 0.45, 0.9), (6.0, 0.3, 0.5), u_steps=3, v_steps=3)
    add_sym_quad(lines, 'C_COCKPIT', (4.5, 0.0, 1.3), (2.0, 0.0, 1.2), (2.5, 0.55, 0.8), (4.5, 0.45, 0.9), u_steps=4, v_steps=3)
    add_sym_quad(lines, 'C_COCKPIT', (2.0, 0.0, 1.2), (1.0, 0.0, 0.8), (1.5, 0.4, 0.7), (2.5, 0.55, 0.8), u_steps=3, v_steps=3)

    # ==============================================================================
    # 5. CONTINUOUS DIAMOND-DELTA WING MATRIX
    # ==============================================================================
    W_ROOT_FWD = 2.0; W_ROOT_AFT = -6.5
    W_TIP_FWD = -3.5; W_TIP_AFT = -5.0
    W_SPAN = 6.78
    
    # Upper Wing Surface (Highly swept leading edge, forward swept trailing edge)
    add_sym_quad(lines, 'C_HULL_MAIN', (W_ROOT_FWD, 2.2, 0.05), (W_TIP_FWD, W_SPAN, 0.02), 
                                       (W_TIP_AFT, W_SPAN, 0.02), (W_ROOT_AFT, 2.2, 0.05), u_steps=6, v_steps=4)
    # Lower Wing Surface
    add_sym_quad(lines, 'C_HULL_MAIN', (W_ROOT_FWD, 2.2, -0.05), (W_TIP_FWD, W_SPAN, -0.02), 
                                       (W_TIP_AFT, W_SPAN, -0.02), (W_ROOT_AFT, 2.2, -0.05), u_steps=6, v_steps=4)

    # Flaperons and Aileron panel delineation on the trailing edges
    add_sym_quad(lines, 'C_HULL_DARK', (W_ROOT_AFT, 2.2, 0.055), (-4.5, 4.5, 0.025), 
                                       (-4.0, 4.5, 0.025), (W_ROOT_AFT+0.5, 2.2, 0.055), u_steps=4, v_steps=2)

    # ==============================================================================
    # 6. EMPENNAGE (Canted Vertical & Diamond Horizontal Stabilators)
    # ==============================================================================
    # Twin Outward-Canted Vertical Stabilisers (28 degree outward tilt)
    V_ROOT_FWD = -5.0; V_ROOT_AFT = -8.5
    V_TIP_FWD = -7.5;  V_TIP_AFT = -9.2
    
    V_Y_ROOT = 1.3; V_Y_TIP = 2.6
    V_Z_ROOT = 0.5; V_Z_TIP = 3.2
    
    # Outer Face
    add_sym_quad(lines, 'C_WEDGE', (V_ROOT_FWD, V_Y_ROOT, V_Z_ROOT), (V_TIP_FWD, V_Y_TIP, V_Z_TIP), 
                                   (V_TIP_AFT, V_Y_TIP, V_Z_TIP), (V_ROOT_AFT, V_Y_ROOT, V_Z_ROOT), u_steps=4, v_steps=4)
    # Inner Face
    add_sym_quad(lines, 'C_WEDGE', (V_ROOT_FWD, V_Y_ROOT-0.1, V_Z_ROOT), (V_TIP_FWD, V_Y_TIP-0.05, V_Z_TIP), 
                                   (V_TIP_AFT, V_Y_TIP-0.05, V_Z_TIP), (V_ROOT_AFT, V_Y_ROOT-0.1, V_Z_ROOT), u_steps=4, v_steps=4)

    # Sovereign Horizontal Stabilators (Diamond Planform)
    H_ROOT_FWD = -6.0; H_ROOT_AFT = -9.45
    H_TIP_FWD = -8.5;  H_TIP_AFT = -9.45
    H_SPAN = 4.8
    H_Z = -0.1
    
    # Upper Stabilator 
    add_sym_quad(lines, 'C_WEDGE', (H_ROOT_FWD, 1.8, H_Z+0.05), (H_TIP_FWD, H_SPAN, H_Z+0.02), 
                                   (H_TIP_AFT, H_SPAN, H_Z+0.02), (H_ROOT_AFT, 1.5, H_Z+0.05), u_steps=4, v_steps=4)
    # Lower Stabilator
    add_sym_quad(lines, 'C_WEDGE', (H_ROOT_FWD, 1.8, H_Z-0.05), (H_TIP_FWD, H_SPAN, H_Z-0.02), 
                                   (H_TIP_AFT, H_SPAN, H_Z-0.02), (H_ROOT_AFT, 1.5, H_Z-0.05), u_steps=4, v_steps=4)

    # ==============================================================================
    # 7. 2D THRUST VECTORING EXHAUST NOZZLES
    # ==============================================================================
    # Explicit rectangular exhaust geometry terminating the F119 engines
    N_FWD = -8.5; N_AFT = X_TAIL
    N_Y_IN = 0.3; N_Y_OUT = 1.3
    N_Z = 0.0
    N_H = 0.3 # Half-height of the nozzle aperture
    
    # Upper vectoring flap
    add_sym_quad(lines, 'C_HULL_DARK', (N_FWD, N_Y_IN, N_Z+N_H), (N_AFT, N_Y_IN, N_Z+N_H*0.6), 
                                       (N_AFT, N_Y_OUT, N_Z+N_H*0.6), (N_FWD, N_Y_OUT, N_Z+N_H), u_steps=2, v_steps=2)
    # Lower vectoring flap
    add_sym_quad(lines, 'C_HULL_DARK', (N_FWD, N_Y_IN, N_Z-N_H), (N_AFT, N_Y_IN, N_Z-N_H*0.6), 
                                       (N_AFT, N_Y_OUT, N_Z-N_H*0.6), (N_FWD, N_Y_OUT, N_Z-N_H), u_steps=2, v_steps=2)
    # Side sealing plates
    add_sym_quad(lines, 'C_HULL_DARK', (N_FWD, N_Y_IN, N_Z+N_H), (N_AFT, N_Y_IN, N_Z+N_H*0.6), 
                                       (N_AFT, N_Y_IN, N_Z-N_H*0.6), (N_FWD, N_Y_IN, N_Z-N_H), u_steps=2, v_steps=1)
    add_sym_quad(lines, 'C_HULL_DARK', (N_FWD, N_Y_OUT, N_Z+N_H), (N_AFT, N_Y_OUT, N_Z+N_H*0.6), 
                                       (N_AFT, N_Y_OUT, N_Z-N_H*0.6), (N_FWD, N_Y_OUT, N_Z-N_H), u_steps=2, v_steps=1)

    # Active Kinematic Red Exhaust Plume Deep Inside Nozzles
    add_sym_quad(lines, 'C_ENGINE', (N_AFT-0.1, N_Y_IN+0.1, N_Z+0.1), (N_AFT-0.1, N_Y_IN+0.1, N_Z-0.1), 
                                    (N_AFT-0.1, N_Y_OUT-0.1, N_Z-0.1), (N_AFT-0.1, N_Y_OUT-0.1, N_Z+0.1), u_steps=2, v_steps=2)

    return lines

# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        dynamic_rig = generate_f22_dynamic(t_sec)
        
        # Absolute Origin Tracking: Locking the geometric True Center of the 18.9m airframe
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.0
        
        # Starts explicitly from 115-degrees (Dramatic front-quarter aesthetic tracking the stealth faceting)
        azimuth = 115.0 - (stage * 360.0)

        yield (f, t_sec, azimuth, cam_x, cam_y, cam_z, dynamic_rig)

def render_frame(packet):
    f, t_sec, azimuth, cx, cy, cz, dynamic_rig = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # 100% VISIBILITY THRESHOLD AUDIT:
    # Anchor = 0.0. Total vessel length is 18.9m. Span is 13.56m.
    # Setting cam_span safely to 12.0 to yield 24.0m horizontal footprint bounding nose, tail, and wingtips fully.
    # Vertical bounds output 12.0 * 1.777 = 21.3m (x2 = 42.6m height allowed).
    # Perfectly frames the super-manoeuvrable stealth profile unconditionally escaping graphical overlap.
    cam_span = 12.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.6, 0.3), 
        ('C_HULL_MAIN', C_HULL_MAIN, 1.3, 1.0),
        ('C_HULL_DARK', C_HULL_DARK, 1.3, 1.0),
        ('C_WEDGE',     C_WEDGE,     1.3, 1.0),
        ('C_COCKPIT',   C_COCKPIT,   1.5, 1.0),
        ('C_ENGINE',    C_ENGINE,    1.8, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in dynamic_rig[c_key]:
            # Elevated +14 degrees to powerfully dissect the sprawling diamond wings and canted vertical tails
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

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-451e // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "EXPLICIT TRUE-SCALE GEOMETRY // F-22 RAPTOR STEALTH MATRIX", color=C_HULL_DARK, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT / LIVE FLIGHT LOOP (V=30.0m/s)", color=C_ENGINE, fontsize=13, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: CONTINUOUS DIAMOND-DELTA WINGS / 2D VECTORING EXHAUSTS", color=C_WEDGE, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-451e: F-22 RAPTOR KINEMATICS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
