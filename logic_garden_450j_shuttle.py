"""
PROJECT: Logic Garden 450j (Exact Physical Construct // Space Shuttle Orbiter Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: NASA, SPACE SHUTTLE, ORBITER, AEROSPACE, WIREFRAME, ENGINEERING, KINEMATICS
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: True parametric Double-Delta wings, flattened HRSI thermal belly, integrated OMS/SSME pods.
- Strict Bounds Protocol: Core anchor locked to Origin. cam_span dynamically set to 21.0 assuring ABSOLUTE 100% frame preservation.
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
OUT_DIR = "frames_450j_shuttle"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#CBD5E1'          # Subdued Steel (Baseplate Reference)

C_HULL_MAIN = '#94A3B8'          # Heavy Slate (Primary White Ceramic Hull/Doors)
C_HULL_DARK = '#1E293B'          # Carbon Slate (HRSI Black Thermal Tiles / Leading Edges)
C_DETAILS   = '#475569'          # Machined Steel (Internal mechanical struts)
C_COCKPIT   = '#111115'          # Indestructible Black (Flight Deck Forward Windows)
C_ENGINE    = '#111115'          # Indestructible Black (RS-25 Thrust Bells & OMS Nozzles)

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
    xs, ys, zs = list(xs), list(ys), list(zs)
    for i in range(len(xs) - 1):
        x1 = xs[i] * scale_x + dx
        x2 = xs[i+1] * scale_x + dx
        lines_dict[key].append(([x1, x2], [ys[i]+dy, ys[i+1]+dy], [zs[i]+dz, zs[i+1]+dz]))

# ------------------------------------------------------------------
# GEOMETRIC SUPERSTRUCTURE BUILDERS (SPACE SHUTTLE ORBITER)
# ------------------------------------------------------------------
def generate_shuttle_static():
    lines = {
        'C_HULL_MAIN': [], 'C_HULL_DARK': [], 'C_DETAILS': [], 
        'C_COCKPIT': [], 'C_ENGINE': [], 'C_GRID': []
    }

    # 1. BASEPLATE ENVELOPE (REFERENCE GRID)
    # Scaled to the 37m x 24m absolute operational envelope
    gx_range = np.linspace(-20.0, 20.0, 21)
    gy_range = np.linspace(-15.0, 15.0, 16)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, -5.0))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, -5.0))

    # ==============================================================================
    # 2. CORE FUSELAGE & THERMAL BELLY TRUNCATION
    # ==============================================================================
    # The Payload Bay (Mid-fuselage) + Tapering Aft (-8 to 14)
    x_body = np.linspace(-8, 14, 16)
    for i in range(len(x_body)):
        x = x_body[i]
        # Standard Payload Array, tapers slightly toward the rear engines
        r = 2.4 - max(0, (x - 8.0) * 0.1) 
        z_c = 0.2 + max(0, (x - 8.0) * 0.05)
        
        t = np.linspace(0, 2*np.pi, 30, endpoint=False)
        y_ring = r * np.cos(t)
        z_ring = z_c + r * np.sin(t)
        
        # Thermal Substrate Array (Flattening the belly at Z=-1.5)
        for k in range(30):
            if z_ring[k] < -1.5: z_ring[k] = -1.5
            
        c_ring = ['C_HULL_DARK' if z < -1.2 else 'C_HULL_MAIN' for z in z_ring]
        
        # Radial slices
        for k in range(30):
            nx = (k+1)%30
            append_segmented(lines, c_ring[k], [x, x], [y_ring[k], y_ring[nx]], [z_ring[k], z_ring[nx]])
            
        # Longitudinal splines
        if i > 0:
            for k in range(30):
                append_segmented(lines, c_ring[k], [x_prev, x], [y_ring_prev[k], y_ring[k]], [z_ring_prev[k], z_ring[k]])
                
        x_prev, y_ring_prev, z_ring_prev = x, y_ring.copy(), z_ring.copy()

    # The Forward Ogive Nose (-18.0 to -8.0)
    x_nose = np.linspace(-18, -8, 14)
    for i in range(len(x_nose)):
        x = x_nose[i]
        ratio = (x + 8.0) / -10.0 # 0 at bridge, 1 at nose
        r = 2.4 * (1.0 - ratio**1.6)**0.6 + 0.15
        z_c = 0.2 - 1.2 * ratio**2
        
        t = np.linspace(0, 2*np.pi, 24, endpoint=False)
        y_ring = r * np.cos(t)
        z_ring = z_c + r * np.sin(t)
        
        for k in range(24):
            if z_ring[k] < -1.5 + (ratio * 1.0): z_ring[k] = -1.5 + (ratio * 1.0) # Bottom slope up to nose tip
            
        c_ring = ['C_HULL_DARK' if z < (-1.0 + ratio) else 'C_HULL_MAIN' for z in z_ring]
        for k in range(24):
            nx = (k+1)%24
            append_segmented(lines, c_ring[k], [x, x], [y_ring[k], y_ring[nx]], [z_ring[k], z_ring[nx]])
            
        if i > 0:
            for k in range(24):
                append_segmented(lines, c_ring[k], [x_prev_n, x], [y_ring_prev_n[k], y_ring[k]], [z_ring_prev_n[k], z_ring[k]])
        x_prev_n, y_ring_prev_n, z_ring_prev_n = x, y_ring.copy(), z_ring.copy()

    # Cockpit Window Polygon Trace (Flight Deck High-Contrast Glazing)
    append_segmented(lines, 'C_COCKPIT', [-14.5, -13.6, -13.0, -13.0, -13.6, -14.5, -14.5], 
                                         [-1.2, -1.0, -0.4, 0.4, 1.0, 1.2, -1.2], 
                                         [1.0, 1.6, 2.0, 2.0, 1.6, 1.0, 1.0])

    # ==============================================================================
    # 3. KINEMATIC DOUBLE-DELTA WING ARCHITECTURE
    # ==============================================================================
    # Swept Leading Edges parameterised explicitly using discrete span cross-sections
    y_vals = np.linspace(2.0, 11.5, 14)
    for sign in [-1, 1]:
        for i in range(len(y_vals)):
            y = y_vals[i] * sign
            
            # The Double Delta Mathematics
            if y_vals[i] <= 5.0:
                x_le = -4.0 + (y_vals[i] - 2.0) * (8.0 / 3.0)  # Forward swept chine
            else:
                x_le = 4.0 + (y_vals[i] - 5.0) * (9.5 / 6.5)   # Main high-sweep primary delta
            
            # Trailing edge elevons sweep slightly forward to the root
            x_te = 14.0 - (y_vals[i] - 2.0) * (1.0 / 9.5)      
            
            z_w = -1.2
            
            # Draw individual mechanical chord ribs
            append_segmented(lines, 'C_HULL_MAIN', [x_le, x_te], [y, y], [z_w, z_w])
            append_segmented(lines, 'C_HULL_DARK', [x_le, x_te], [y, y], [z_w-0.2, z_w-0.2]) # Thick lower thermal surface
            
            # Bind ribs to create skin layer
            if i > 0:
                y_prev = y_vals[i-1] * sign
                append_segmented(lines, 'C_HULL_DARK', [x_le_prev, x_le], [y_prev, y], [z_w-0.1, z_w-0.1]) # True Leading Edge
                append_segmented(lines, 'C_HULL_MAIN', [x_te_prev, x_te], [y_prev, y], [z_w, z_w])         # True Trailing Edge
            
            x_le_prev, x_te_prev = x_le, x_te

    # ==============================================================================
    # 4. VERTICAL STABILISER & RUDDER LATTICE
    # ==============================================================================
    z_stab = np.linspace(2.2, 8.5, 10)
    for i in range(len(z_stab)):
        z = z_stab[i]
        ratio = (z - 2.2) / 6.3
        # Heavy backward sweeping leading edge
        x_le = 9.0 + ratio * 4.5
        x_te = 14.5 + ratio * 1.5
        
        append_segmented(lines, 'C_HULL_MAIN', [x_le, x_te], [0, 0], [z, z])
        if i > 0:
            append_segmented(lines, 'C_HULL_DARK', [x_sle_prev, x_le], [0, 0], [z_sprev, z]) # Leading Edge Carbon Trace
            append_segmented(lines, 'C_HULL_MAIN', [x_ste_prev, x_te], [0, 0], [z_sprev, z])
        x_sle_prev, x_ste_prev, z_sprev = x_le, x_te, z

    # ==============================================================================
    # 5. ORBITAL MANEUVERING SYSTEM (OMS) PODS
    # ==============================================================================
    for sign in [-1, 1]:
        x_oms = np.linspace(10, 14.5, 8)
        for i in range(len(x_oms)):
            x = x_oms[i]
            r = 1.0 - abs((x - 12.2) * 0.3)
            y_c = 2.0 * sign + (x-10)*0.1*sign
            z_c = 2.5
            
            t = np.linspace(0, 2*np.pi, 12, endpoint=False)
            y_ring = y_c + r * np.cos(t)
            z_ring = z_c + r * np.sin(t)
            
            append_segmented(lines, 'C_HULL_MAIN', [x]*13, list(y_ring)+[y_ring[0]], list(z_ring)+[z_ring[0]])
            if i > 0:
                for k in range(12):
                    append_segmented(lines, 'C_HULL_MAIN', [xo_prev, x], [yo_ring_prev[k], y_ring[k]], [zo_ring_prev[k], z_ring[k]])
            xo_prev, yo_ring_prev, zo_ring_prev = x, y_ring.copy(), z_ring.copy()
            
        # Small OMS Thrust Nozzles
        c_omsx = 14.5; c_omsy = y_c; c_omsz = z_c
        steps = 4 
        h_oms = 0.8
        for k in range(steps):
            ratio = k / float(steps-1)
            x_b = c_omsx + ratio * h_oms
            r_b = 0.2 + (0.5 - 0.2) * (ratio**1.5)
            t = np.linspace(0, 2*np.pi, 12, endpoint=False)
            append_segmented(lines, 'C_ENGINE', [x_b]*13, list(c_omsy + r_b*np.cos(t))+[c_omsy + r_b*np.cos(0)], list(c_omsz + r_b*np.sin(t))+[c_omsz + r_b*np.sin(0)])

    # ==============================================================================
    # 6. RS-25 MAIN ENGINE ARRAY (SSME BELLS)
    # ==============================================================================
    def draw_thrust_bell_x(cx, cy, cz, h, r_top, r_bot):
        steps = 6
        for k in range(steps):
            ratio = k / float(steps-1)
            x_b = cx + ratio * h
            r_b = r_top + (r_bot - r_top) * (ratio**1.5) # Bell curve
            t = np.linspace(0, 2*np.pi, 16, endpoint=False)
            yb = cy + r_b*np.cos(t)
            zb = cz + r_b*np.sin(t)
            append_segmented(lines, 'C_ENGINE', [x_b]*17, list(yb)+[yb[0]], list(zb)+[zb[0]])
            if k > 0:
                for m in range(16):
                    append_segmented(lines, 'C_ENGINE', [xb_prev, x_b], [yb_prev[m], yb[m]], [zb_prev[m], zb[m]])
            xb_prev, yb_prev, zb_prev = x_b, yb.copy(), zb.copy()

    # Thrust vector slightly pitched (+X momentum mapping)
    draw_thrust_bell_x(14.0,  0.0,  1.5, h=2.5, r_top=0.4, r_bot=1.1)    # Center Top
    draw_thrust_bell_x(14.0,  1.4, -0.4, h=2.5, r_top=0.4, r_bot=1.1)    # Bottom Left
    draw_thrust_bell_x(14.0, -1.4, -0.4, h=2.5, r_top=0.4, r_bot=1.1)    # Bottom Right

    # Rear Body Flap (Shields the main engines during re-entry)
    append_segmented(lines, 'C_HULL_DARK', [14.0, 16.5, 16.5, 14.0, 14.0], [-3.0, -3.0, 3.0, 3.0, -3.0], [-1.5, -1.5, -1.5, -1.5, -1.5])

    return lines


# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_shuttle_static()
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Absolute Origin Tracking: Locking the rig rigidly across Cartesian Zero (-18 to 16.5 limits)
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.0
        
        # Starts explicitly from 115-degrees (Front/Side dynamic sweeping perspective yielding absolute kinetic energy)
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
    # Anchor = 0.0. Max X extent = 18.5m. Total rotating radial footprint safely inside 20m.
    # Setting cam_span strictly to 21.0 to guarantee flawless 9:16 border insulation dynamically.
    cam_span = 21.0
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    layer_map = [
        ('C_GRID',      C_GRID,      0.8, 0.3), 
        ('C_DETAILS',   C_DETAILS,   1.2, 1.0),
        ('C_HULL_MAIN', C_HULL_MAIN, 1.4, 1.0),
        ('C_HULL_DARK', C_HULL_DARK, 1.6, 1.0), # Heavy structural priority on the Carbon belly tiles
        ('C_COCKPIT',   C_COCKPIT,   1.6, 1.0),
        ('C_ENGINE',    C_ENGINE,    1.5, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            # Elevated +18 degrees to magnificently expose the payload bay doors and overarching Double-Delta wing integration
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=18.0)
            render_queue.append((np.mean(depth), u, v, c_val, lw, alpha))

    # ABSOLUTE Z-SORT (Strict Painter's Algorithm Depth Culling)
    render_queue.sort(key=lambda item: item[0], reverse=True)
    for depth, u, v, c, lw, a in render_queue:
        ax.plot(u, v, color=c, lw=lw, alpha=a)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (TOP HUD)
    # ------------------------------------------------------------------
    ui_t = cam_span * 1.45
    ax.add_patch(patches.Rectangle((-cam_span, ui_t), cam_span*2, 12.0, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_t, ui_t], color=C_TEXT, lw=6, zorder=81)

    ax.text(-cam_span*0.95, ui_t+1.8, "LG-450j // MACRO-ENGINEERING TENSOR: AEROSPACE KINEMATICS", color=C_TEXT, fontsize=17, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t+0.5, "EXPLICIT TRUE-SCALE GEOMETRY // SPACE SHUTTLE ORBITER MATRIX", color=C_HULL_DARK, fontsize=13, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b+2.8, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_HULL_MAIN, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+1.4, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.3, "TOPOLOGICAL YIELD: DOUBLE-DELTA SWEEP / HRSI THERMAL BELLY TRUNCATED", color=C_DETAILS, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-450j: SPACE SHUTTLE KINEMATICS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Aerospace Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
