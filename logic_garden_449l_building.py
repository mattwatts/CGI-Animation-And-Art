"""
PROJECT: Logic Garden 449l (Exact Physical Construct // Architectural Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: ARCHITECTURE, DRAFTING, WIREFRAME, ENGINEERING, KINEMATICS, ISOMETRIC, PROJECTION
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: L-Footprint, Intersecting Gables, Chimney Node, Flush Front Wall.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from absolute Left Profile.
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
OUT_DIR = "frames_449l_building"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_WALL      = '#1E293B'          # Carbon Slate (Vertical & Base Structures)
C_ROOF      = '#475569'          # Slate Grey (Gables, Ridges & Valleys)
C_CHIMNEY   = '#111115'          # Indestructible Black (Extruded Chimney Node)
C_GLASS     = '#005599'          # Deep Marine (Door / Window Outlines)
C_GRID      = '#CBD5E1'          # Subdued Steel (Baseplate Reference Grid)

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
    """Absolute Segmentation Protocol: Splits arrays into 2-point vectors for absolute Painter depth sorting."""
    for i in range(len(xs) - 1):
        lines_dict[key].append(([xs[i], xs[i+1]], [ys[i], ys[i+1]], [zs[i], zs[i+1]]))

# ------------------------------------------------------------------
# RIGID 3D EXACT ARCHITECTURAL GENERATOR
# ------------------------------------------------------------------
def generate_building_vectors():
    lines = {
        'C_WALL': [], 'C_ROOF': [], 'C_CHIMNEY': [], 
        'C_GLASS': [], 'C_GRID': []
    }

    # ==============================================================================
    # 1. BASEPLATE ENVELOPE (REFERENCE GRID)
    # ==============================================================================
    gx_range = np.linspace(-4, 4, 17) # 0.5 unit intervals
    for gx in gx_range:
        append_segmented(lines, 'C_GRID', np.full_like(gx_range, gx), gx_range, np.zeros_like(gx_range))
        append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gx), np.zeros_like(gx_range))

    # ==============================================================================
    # 2. L-SHAPED FOOTPRINT & VERTICAL WALL STRUCTURE
    # ==============================================================================
    # Outer Footprint Vertices traversing Anti-Clockwise
    # Front is Flush at y = -2. Main block width = 2 (x: 0->2). Extension width = 2 (x: -2->0)
    fx = [-2.0, 0.0, 2.0,  2.0,  0.0,  0.0, -2.0, -2.0]
    fy = [-2.0, -2.0, -2.0, 2.0,  2.0,  0.0,  0.0, -2.0]
    fz_base = [0.0]*8
    fz_wall = [2.0]*8

    # Base Perimeter
    append_segmented(lines, 'C_WALL', fx, fy, fz_base)
    # Wall Tops (Eaves)
    append_segmented(lines, 'C_WALL', fx, fy, fz_wall)
    # Vertical Corners
    for x, y in zip(fx[:-1], fy[:-1]):
        append_segmented(lines, 'C_WALL', [x, x], [y, y], [0.0, 2.0])

    # ==============================================================================
    # 3. INTERSECTING GABLES (ROOF TOPOLOGY)
    # ==============================================================================
    # Main Roof (Over Right Flank: x from 0 to 2)
    # Ridge strictly at x = 1.0, z = 3.5
    append_segmented(lines, 'C_ROOF', [ 0.0,  1.0,  2.0], [-2.0, -2.0, -2.0], [2.0, 3.5, 2.0]) # Front Main Gable
    append_segmented(lines, 'C_ROOF', [ 0.0,  1.0,  2.0], [ 2.0,  2.0,  2.0], [2.0, 3.5, 2.0]) # Back Main Gable
    append_segmented(lines, 'C_ROOF', [ 1.0,  1.0],       [-2.0,  2.0],       [3.5, 3.5])      # Main Ridge

    # Extension Roof (Over Left Flank: x from -2 to intersection)
    # Ridge explicitly at y = -1.0, z = 2.8
    # Absolute mathematically derived valley intersection node at x = 0.5333
    R_INT_X, R_INT_Y, R_INT_Z = 0.5333, -1.0, 2.8
    
    append_segmented(lines, 'C_ROOF', [-2.0, -2.0, -2.0], [0.0, -1.0, -2.0], [2.0, 2.8, 2.0]) # Left Extension Gable
    append_segmented(lines, 'C_ROOF', [-2.0, R_INT_X],    [-1.0, R_INT_Y],   [2.8, R_INT_Z])  # Extension Ridge
    append_segmented(lines, 'C_ROOF', [ 0.0, R_INT_X],    [-2.0, R_INT_Y],   [2.0, R_INT_Z])  # Front Valley Trace
    append_segmented(lines, 'C_ROOF', [ 0.0, R_INT_X],    [ 0.0, R_INT_Y],   [2.0, R_INT_Z])  # Rear Valley Trace

    # ==============================================================================
    # 4. CHIMNEY NODE EXTRUSION
    # ==============================================================================
    # Projecting from the rear-left slope of the main roof.
    # Base intersects roof slope equations explicitly.
    c_b1, c_b2, c_b3, c_b4 = (0.3, 0.8, 2.45), (0.7, 0.8, 3.05), (0.7, 1.2, 3.05), (0.3, 1.2, 2.45)
    c_base_x = [c_b1[0], c_b2[0], c_b3[0], c_b4[0], c_b1[0]]
    c_base_y = [c_b1[1], c_b2[1], c_b3[1], c_b4[1], c_b1[1]]
    c_base_z = [c_b1[2], c_b2[2], c_b3[2], c_b4[2], c_b1[2]]
    
    c_top_x = c_base_x[:]
    c_top_y = c_base_y[:]
    c_top_z = [4.5] * 5

    append_segmented(lines, 'C_CHIMNEY', c_base_x, c_base_y, c_base_z) # Base weld contour
    append_segmented(lines, 'C_CHIMNEY', c_top_x, c_top_y, c_top_z)    # Top crown
    
    for bx, by, bz in zip(c_base_x[:-1], c_base_y[:-1], c_base_z[:-1]):
        append_segmented(lines, 'C_CHIMNEY', [bx, bx], [by, by], [bz, 4.5]) # Vertical risers

    # ==============================================================================
    # 5. APERTURE VECTORS (DOOR & WINDOW)
    # ==============================================================================
    # Main Entrance Door
    d_x = [0.7, 0.7, 1.3, 1.3, 0.7]
    d_y = [-2.0] * 5
    d_z = [0.0, 1.2, 1.2, 0.0, 0.0]
    append_segmented(lines, 'C_GLASS', d_x, d_y, d_z)
    
    # Extension Side Window
    w1_x = [-1.4, -1.4, -0.6, -0.6, -1.4]
    w1_y = [-2.0] * 5
    w1_z = [0.8, 1.5, 1.5, 0.8, 0.8]
    append_segmented(lines, 'C_GLASS', w1_x, w1_y, w1_z)
    
    # Right Flank Main Window
    w2_x = [2.0] * 5
    w2_y = [-0.5, -0.5, 0.5, 0.5, -0.5]
    w2_z = [0.8, 1.5, 1.5, 0.8, 0.8]
    append_segmented(lines, 'C_GLASS', w2_x, w2_y, w2_z)

    return lines

# ------------------------------------------------------------------
# PARALLEL GENERATOR STREAM (KINEMATIC TIMELINE TENSOR)
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_building_vectors() # Computed once for true O(1) retrieval
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Central Basepoint: Mapping architectural boundaries
        cam_x, cam_y, cam_z = 0.0, 0.0, 2.0 
        
        # Continuous 360-degree perfect orbital synchronisation
        # MUST start precisely from LEFT side view per parameter mapping (Azimuth = -90.0)
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

    # Cinematic Rigid Map Boundary - Covers the 4m architectural footprint
    cam_span = 4.2
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []

    # 1. PROCESS ARCHITECTURAL VECTOR MATRIX
    for c_key, c_val in [('C_GRID', C_GRID), ('C_WALL', C_WALL), ('C_ROOF', C_ROOF), 
                         ('C_CHIMNEY', C_CHIMNEY), ('C_GLASS', C_GLASS)]:
        
        if c_key == 'C_GRID': lw, alpha = 0.8, 0.4
        elif c_key == 'C_WALL': lw, alpha = 2.0, 1.0     
        elif c_key == 'C_ROOF': lw, alpha = 1.5, 1.0      
        elif c_key == 'C_CHIMNEY': lw, alpha = 2.4, 1.0  
        elif c_key == 'C_GLASS': lw, alpha = 1.6, 1.0   
        else: lw, alpha = 1.0, 1.0
            
        for xl, yl, zl in static_rig[c_key]:
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=25.0)
            # Center on focal plane dynamically
            render_queue.append((np.mean(depth), u, v-0.5, c_val, lw, alpha))

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

    ax.text(-cam_span*0.95, ui_t+1.5, "LG-449l // MACRO-ENGINEERING TENSOR: ARCHITECTURE", color=C_TEXT, fontsize=21, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t+0.5, "EXPLICIT TRUE-SCALE GEOMETRY // 9-PROJECTION TOPOLOGY", color=C_WALL, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b+1.0, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_ROOF, fontsize=17, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.5, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS SYNCHRONISATION)", color=C_TEXT, fontsize=17, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.1, "GEOMETRY YIELD   : L-FOOTPRINT / INTERSECTING GABLES SECURED", color=C_CHIMNEY, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-449l: ARCHITECTURAL MACRO-ENGINEERING TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Architecture Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
