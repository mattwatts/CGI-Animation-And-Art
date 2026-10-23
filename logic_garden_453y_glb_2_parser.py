"""
PROJECT: Logic Garden 453y (Exact Physical Construct // Universal GLB Kinematic Parser - OOM HOTFIX)
FORMAT: YouTube Shorts (1080x1920)
METADATA: GLB, 3D PARSER, WIREFRAME, KINEMATICS, PYTHON, DATA VISUALISATION
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe extraction of arbitrary .glb binary payloads.
- OOM Decimation Protocol: Autonomously scales down polygon density on massive payloads to prevent RAM death-spirals.
- LineCollection Offloading: Bypasses O(N) plotting overhead via C++ backend arrays.
- Automated Viewport Synchronisation: Calculates maximum bounds to dynamically output `cam_span`.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from 115-degree front-quarter angle.
- Daylight Palette (White Substrate / High-Contrast Edge Geometry).
- Purged Jargon. Australian spelling conventions (maths, colour, kilometres, synchronisation).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
from matplotlib.collections import LineCollection
import multiprocessing as mp
import trimesh
import sys
import os
import gc

# ======== SEQUENCE PARAMETERS ========
DURATION = 24.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_453y_glb_parser"
os.makedirs(OUT_DIR, exist_ok=True)

# Define the target GLB payload here
TARGET_GLB = "input_model.glb"  # The Architect must designate the local payload path

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISIBILITY) --------
C_BG        = '#FFFFFF'          # White Substrate
C_TEXT      = '#111115'          # Indestructible Black (Typography)
C_GRID      = '#94A3B8'          # Subdued Steel (Orbital Tracking Grid)

# Dynamic allocation palette for sub-meshes
MESH_PALETTE = [
    '#334155', # Heavy Slate
    '#005599', # Deep Marine
    '#1E293B', # Carbon Slate
    '#94A3B8', # Slate Aluminium
    '#CA8A04'  # Kapton Gold
]

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
    lines_dict[key].append(([xs[0], xs[1]], [ys[0], ys[1]], [zs[0], zs[1]]))

# ------------------------------------------------------------------
# .GLB BINARY PARSER & TERRESTRIAL GRID BUILDER
# ------------------------------------------------------------------
def ingest_glb_payload(filepath):
    if not os.path.exists(filepath):
        print(f"[FATAL] Payload missing. The engine requires '{filepath}' to compute topography.")
        sys.exit(1)
        
    scene = trimesh.load(filepath, force='scene')
    
    bounds = scene.bounds
    centroid = scene.centroid
    extents = scene.extents
    
    max_extent = np.max(extents)
    calculated_cam_span = (max_extent / 2.0) * 1.30
    z_floor = bounds[0][2] - (max_extent * 0.1)

    lines = {
        'C_GRID': []
    }
    
    for c in MESH_PALETTE:
        lines[c] = []

    # Injecting Subdued Steel Tracking Grid mathematically scaled manually
    grid_radii = [max_extent * 0.5, max_extent * 0.8, max_extent * 1.2]
    for r_p in grid_radii:
        t_p = np.linspace(0, 2*np.pi, 32, endpoint=False)
        for i in range(len(t_p)-1):
            xs = [centroid[0] + r_p * np.cos(t_p[i]), centroid[0] + r_p * np.cos(t_p[i+1])]
            ys = [centroid[1] + r_p * np.sin(t_p[i]), centroid[1] + r_p * np.sin(t_p[i+1])]
            zs = [z_floor, z_floor]
            append_segmented(lines, 'C_GRID', xs, ys, zs)

    # ---------------------------------------------------------
    # OOM DECIMATION PROTOCOL AUDIT
    # ---------------------------------------------------------
    total_edges = 0
    for geometry in scene.geometry.values():
        if isinstance(geometry, trimesh.Trimesh):
            total_edges += len(geometry.edges_unique)
            
    MAX_ALLOWABLE_EDGES = 40000
    decimation_step = 1
    
    if total_edges > MAX_ALLOWABLE_EDGES:
        decimation_step = int(np.ceil(total_edges / float(MAX_ALLOWABLE_EDGES)))
        print(f"\n[WARNING] EXTREME GEOMETRY DETECTED: {total_edges} Edges.")
        print(f"[WARNING] Activating RAM Decimation Protocol. Sub-sampling every {decimation_step} vectors.\n")

    # Dissecting individual mesh components
    mesh_index = 0
    for geometry_name, geometry in scene.geometry.items():
        if isinstance(geometry, trimesh.Trimesh):
            color_key = MESH_PALETTE[mesh_index % len(MESH_PALETTE)]
            mesh_index += 1
            
            # Apply Decimation Step securely to the edge array
            edges = geometry.edges_unique[::decimation_step]
            vertices = geometry.vertices
            
            for edge in edges:
                p1 = vertices[edge[0]]
                p2 = vertices[edge[1]]
                xs = [p1[0], p2[0]]
                ys = [p1[1], p2[1]]
                zs = [p1[2], p2[2]]
                append_segmented(lines, color_key, xs, ys, zs)

    return lines, calculated_cam_span, centroid

global_lines, global_cam_span, global_centroid = None, None, None

def initialize_payload():
    global global_lines, global_cam_span, global_centroid
    print(f"Ingesting payload bounds for {TARGET_GLB}...")
    global_lines, global_cam_span, global_centroid = ingest_glb_payload(TARGET_GLB)
    print(f"Topography resolved. Dynamic cam_span locked at: {global_cam_span:.2f}m")

# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        cam_x, cam_y, cam_z = global_centroid[0], global_centroid[1], global_centroid[2]
        azimuth = 115.0 - (stage * 360.0)
        yield (f, t_sec, azimuth, cam_x, cam_y, cam_z, global_lines, global_cam_span)

def render_frame(packet):
    f, t_sec, azimuth, cx, cy, cz, static_rig, cam_span = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    
    # Pack rendering tuples: (depth, [(x1,y1), (x2,y2)], color, linewidth, alpha)
    for xl, yl, zl in static_rig['C_GRID']:
        u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=16.0)
        render_queue.append((np.mean(depth), [(u[0], v[0]), (u[1], v[1])], C_GRID, 0.8, 0.4))
            
    for col_key in MESH_PALETTE:
        if col_key in static_rig:
            for xl, yl, zl in static_rig[col_key]:
                u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=16.0)
                render_queue.append((np.mean(depth), [(u[0], v[0]), (u[1], v[1])], col_key, 1.0, 0.9))

    # ABSOLUTE Z-SORT (Painter's Algorithm)
    render_queue.sort(key=lambda item: item[0], reverse=True)
    
    # ---------------------------------------------------------
    # LINÉCOLLECTION OFFLOAD PROTOCOL (RAM SAVER)
    # ---------------------------------------------------------
    # Instead of iterating ax.plot() 40,000 times, we send 1 monolithic array to C++ backend
    if render_queue:
        segments = [rq[1] for rq in render_queue]
        # rgba extraction mapping colour string + alpha value
        colors = [mcolors.to_rgba(rq[2], alpha=rq[4]) for rq in render_queue]
        linewidths = [rq[3] for rq in render_queue]
        
        lc = LineCollection(segments, colors=colors, linewidths=linewidths)
        ax.add_collection(lc)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (TOP HUD)
    # ------------------------------------------------------------------
    ui_t = cam_span * 1.45
    ax.add_patch(patches.Rectangle((-cam_span, ui_t), cam_span*2, cam_span*0.5, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_t, ui_t], color=C_TEXT, lw=6, zorder=81)

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-453y // MACRO-ENGINEERING TENSOR: STRUCTURAL KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, f"EXPLICIT TRUE-SCALE GEOMETRY // BARE-METAL GLB PARSER", color=MESH_PALETTE[0], fontsize=12, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=MESH_PALETTE[1], fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, f"TOPOLOGICAL YIELD: DYNAMIC MULTI-MESH EXTRACTION / O(N) LINE-COLLECTION ARRAY / DYNAMIC BOUNDS", color=C_TEXT, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    initialize_payload()
    
    # CORE THROTTLING: Restricting to half physical cores to salvage OS stability
    cpu_cores = max(1, mp.cpu_count() // 2)
    print(f"LG-453y: OOM RECOVERED UNIVERSAL GLB PARSING TENSOR [CORES THROLTTLED: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    # Lowering chunksize prevents memory backlog pooling inside worker nodes
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=4):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Dynamic Topography Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
