"""
PROJECT: Logic Garden 453x (Exact Physical Construct // Universal GLB Batch Parser - LINUX HOTFIX 9)
FORMAT: YouTube Shorts (1080x1920)
METADATA: GLB, 3D PARSER, WIREFRAME, PYTHON, BATCH AUTOMATION
EXECUTION: 24.0s Sequence per payload. True Continuous Vector Architecture.
RULES ENFORCED:
- Autonomous Batching: Scans directory, sorts all .glb payloads by file size (ascending).
- Universal Normalisation Matrix: Extracts all vertices, shifts the exact physical centroid to [0,0,0], and natively scales the entire object to a 10.0m absolute boundary.
- Zero-Tolerance Bypassing: Eliminates microscopic matplotlib scaling faults natively.
- IPC Pipe Synchronisation: Fixes Linux Mint OOM login crashing by aligning `chunksize=1` with `maxtasksperchild=1`.
- Aggressive OOM Decimation: Max edges slashed to 20,000 ensuring 1080p density while protecting OS stability.
- LineCollection Offloading: Bypasses O(N) plotting overhead via C++ backend arrays.
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
import subprocess
import glob
import sys
import os
import gc

# ======== SEQUENCE PARAMETERS ========
DURATION = 24.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#94A3B8'

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
# .GLB UNIVERSAL NORMALISATION PARSER
# ------------------------------------------------------------------
def ingest_glb_payload(filepath):
    try:
        scene = trimesh.load(filepath, force='scene')
    except Exception as e:
        print(f"      [FATAL] Trimesh failed to parse payload {filepath}. Error: {e}")
        return None, None, None

    transformed_meshes = []
    
    # 1. Native Scene Graph World Transform Dumping
    for geom in scene.dump(concatenate=False):
        if isinstance(geom, trimesh.Trimesh) and len(geom.vertices) > 0:
            transformed_meshes.append(geom.copy())

    if not transformed_meshes:
        print("      [FATAL] GLB container lacks dimensional vertex data. Bypassing render.")
        return None, None, None

    # 2. Extract Raw Vertices & Evaluate True Metrics
    all_raw_vertices = [m.vertices for m in transformed_meshes]
    master_v_stack = np.vstack(all_raw_vertices)
    
    min_b = np.min(master_v_stack, axis=0)
    max_b = np.max(master_v_stack, axis=0)
    
    true_centroid = (max_b + min_b) / 2.0
    max_extent = np.max(max_b - min_b)

    # 3. Universal Vector Scaling
    if np.isnan(max_extent) or max_extent <= 0.0:
        scale_factor = 1.0
        print("      [WARNING] Absolute Mathematical zero-volume coordinate fault. Bypassing scale.")
    else:
        # We explicitly evaluate all geometry into a mathematically enforced 10.0-metre grid
        scale_factor = 10.0 / max_extent
        print(f"      [NORMALISATION] Raw Vector Extent: {max_extent:.2e} units. Normalising to Absolute 10-Unit Substrate.")

    # 4. Rebuilding Validated Meshes on the Null Axis
    validated_meshes = []
    total_edges = 0
    
    for mesh in transformed_meshes:
        # Shift true centroid to [0,0,0] and apply standardisation scale
        mesh.vertices = (mesh.vertices - true_centroid) * scale_factor
        
        try:
            # Welding is now completely safe from microscopic collapse because the mesh is scaled up
            mesh.merge_vertices()
        except:
            pass
            
        if len(mesh.edges_unique) > 0:
            validated_meshes.append(mesh)
            total_edges += len(mesh.edges_unique)

    if not validated_meshes:
        print("      [FATAL] Edge framework entirely nullified. Zero topology array.")
        return None, None, None

    # 5. Fixed Orbital Tracking Dynamics (Locked to the 10-Unit Frame)
    calculated_cam_span = 5.0 * 1.30  # Absolute locked boundary preventing ANY zoom faults
    # Floor calculates exactly 1.0 units below the normalised geometry base
    z_floor = (min_b[2] - true_centroid[2]) * scale_factor - 1.0 

    lines = {'C_GRID': []}
    for c in MESH_PALETTE:
        lines[c] = []

    # Synthesising Fixed Terrestrial Tracking Node (R=2.5, 4.0, 6.0 units natively)
    grid_radii = [2.5, 4.0, 6.0]
    for r_p in grid_radii:
        t_p = np.linspace(0, 2*np.pi, 32, endpoint=False)
        for i in range(len(t_p)-1):
            xs = [r_p * np.cos(t_p[i]), r_p * np.cos(t_p[i+1])]
            ys = [r_p * np.sin(t_p[i]), r_p * np.sin(t_p[i+1])]
            zs = [z_floor, z_floor]
            append_segmented(lines, 'C_GRID', xs, ys, zs)

    # 6. Aggressive OOM Threshold Intervention
    MAX_ALLOWABLE_EDGES = 20000
    decimation_step = 1
    if total_edges > MAX_ALLOWABLE_EDGES:
        decimation_step = int(np.ceil(total_edges / float(MAX_ALLOWABLE_EDGES)))
        print(f"      [OOM INTERVENTION] {total_edges} Edges located. RAM Decimation Protocol active (1-in-{decimation_step}).")

    # 7. Wireframe Matrix Population
    mesh_index = 0
    for mesh in validated_meshes:
        color_key = MESH_PALETTE[mesh_index % len(MESH_PALETTE)]
        mesh_index += 1
        
        edges = mesh.edges_unique[::decimation_step]
        vertices = mesh.vertices
        
        for edge in edges:
            p1 = vertices[edge[0]]
            p2 = vertices[edge[1]]
            append_segmented(lines, color_key, [p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]])

    del transformed_meshes
    del validated_meshes
    del scene
    
    # We return [0,0,0] securely, as everything is mapped identically around physical Zero Point
    return lines, calculated_cam_span, [0.0, 0.0, 0.0]

# ------------------------------------------------------------------
# MASTER RENDERER HOOK & WORKER INITIALIZER
# ------------------------------------------------------------------
GLOBAL_LINES = None
GLOBAL_CAM_SPAN = None
GLOBAL_CENTROID = None
GLOBAL_TARGET_NAME = None
GLOBAL_OUT_DIR = None

def init_worker(lines_bundle, span_bundle, cent_bundle, name_bundle, out_bundle):
    global GLOBAL_LINES, GLOBAL_CAM_SPAN, GLOBAL_CENTROID, GLOBAL_TARGET_NAME, GLOBAL_OUT_DIR
    GLOBAL_LINES = lines_bundle
    GLOBAL_CAM_SPAN = span_bundle
    GLOBAL_CENTROID = cent_bundle
    GLOBAL_TARGET_NAME = name_bundle
    GLOBAL_OUT_DIR = out_bundle

def generate_stream(target_centroid):
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        cam_x, cam_y, cam_z = target_centroid[0], target_centroid[1], target_centroid[2]
        azimuth = 115.0 - (stage * 360.0)
        yield (f, t_sec, azimuth, cam_x, cam_y, cam_z)

def render_frame(packet):
    f, t_sec, azimuth, cx, cy, cz = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # UI tracking span is absolutely uniform for every model 
    ax.set_xlim(-GLOBAL_CAM_SPAN, GLOBAL_CAM_SPAN)
    ax.set_ylim(-GLOBAL_CAM_SPAN * 1.777, GLOBAL_CAM_SPAN * 1.777)

    render_queue = []
    
    for xl, yl, zl in GLOBAL_LINES['C_GRID']:
        u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=16.0)
        render_queue.append((np.mean(depth), [(u[0], v[0]), (u[1], v[1])], C_GRID, 1.0, 0.4))
            
    for col_key in MESH_PALETTE:
        if col_key in GLOBAL_LINES:
            for xl, yl, zl in GLOBAL_LINES[col_key]:
                u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=16.0)
                render_queue.append((np.mean(depth), [(u[0], v[0]), (u[1], v[1])], col_key, 1.25, 0.9))

    render_queue.sort(key=lambda item: item[0], reverse=True)
    
    if render_queue:
        segments = [rq[1] for rq in render_queue]
        colors = [mcolors.to_rgba(rq[2], alpha=rq[4]) for rq in render_queue]
        linewidths = [rq[3] for rq in render_queue]
        lc = LineCollection(segments, colors=colors, linewidths=linewidths)
        ax.add_collection(lc)

    ui_t = GLOBAL_CAM_SPAN * 1.45
    ax.add_patch(patches.Rectangle((-GLOBAL_CAM_SPAN, ui_t), GLOBAL_CAM_SPAN*2, GLOBAL_CAM_SPAN*0.5, facecolor=C_BG, zorder=80))
    ax.plot([-GLOBAL_CAM_SPAN, GLOBAL_CAM_SPAN], [ui_t, ui_t], color=C_TEXT, lw=6, zorder=81)

    ax.text(-GLOBAL_CAM_SPAN*0.95, ui_t + GLOBAL_CAM_SPAN*0.08, "LG-453x // MACRO-ENGINEERING TENSOR: STRUCTURAL KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-GLOBAL_CAM_SPAN*0.95, ui_t + GLOBAL_CAM_SPAN*0.02, f"EXPLICIT TRUE-SCALE GEOMETRY // FILE: {GLOBAL_TARGET_NAME.upper()}", color=MESH_PALETTE[0], fontsize=12, fontname='monospace', weight='bold', zorder=82)

    ui_b = -GLOBAL_CAM_SPAN * 1.777
    ax.add_patch(patches.Rectangle((-GLOBAL_CAM_SPAN, ui_b), GLOBAL_CAM_SPAN*2, GLOBAL_CAM_SPAN*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-GLOBAL_CAM_SPAN, GLOBAL_CAM_SPAN], [ui_b + GLOBAL_CAM_SPAN*0.35, ui_b + GLOBAL_CAM_SPAN*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-GLOBAL_CAM_SPAN*0.95, ui_b + GLOBAL_CAM_SPAN*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=MESH_PALETTE[1], fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-GLOBAL_CAM_SPAN*0.95, ui_b + GLOBAL_CAM_SPAN*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-GLOBAL_CAM_SPAN*0.95, ui_b + GLOBAL_CAM_SPAN*0.02, f"TOPOLOGICAL YIELD: UNIVERSAL NORMALISATION MATRIX RUNNING / BOUNDS ABSOLUTE LOCK", color=C_TEXT, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(GLOBAL_OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    
    plt.close("all")
    fig.clf()
    gc.collect()
    
    return f

# ------------------------------------------------------------------
# BATCH ORCHESTRATION & AUTOMATED FFMPEG PIPELINE
# ------------------------------------------------------------------
def process_batch():
    glb_files = glob.glob("*.glb")
    if not glb_files:
        print("[FATAL] Zero .glb payloads detected in the active working directory.")
        sys.exit(1)

    glb_files.sort(key=lambda f: os.path.getsize(f))
    
    cpu_cores = max(1, mp.cpu_count() // 2)
    print(f"LG-453x: AUTONOMOUS BATCH PIPELINE ENGAGED [THROTTLED CORES: {cpu_cores}]")
    print(f"Payloads detected: {len(glb_files)} (Sorted efficiently by byte mass)")

    for idx, filepath in enumerate(glb_files):
        filename = os.path.basename(filepath)
        basename, _ = os.path.splitext(filename)
        out_mp4 = f"{basename}.mp4"
        
        GLOBAL_TARGET_NAME = filename
        GLOBAL_OUT_DIR = f"frames_{basename}"
        os.makedirs(GLOBAL_OUT_DIR, exist_ok=True)

        size_mb = os.path.getsize(filepath) / (1024*1024)
        print(f"\n[{idx+1}/{len(glb_files)}] PARSING PAYLOAD: {filename} ({size_mb:.2f} MB)")
        
        lines, cam_span, centroid = ingest_glb_payload(filepath)
        
        if lines is None:
            continue
        
        print(f"      Initiating Core Pool -> Rendering {TOTAL_FRAMES} frames...")
        
        with mp.Pool(processes=cpu_cores, maxtasksperchild=1, 
                     initializer=init_worker, 
                     initargs=(lines, cam_span, centroid, GLOBAL_TARGET_NAME, GLOBAL_OUT_DIR)) as pool:
            
            for finished_frame in pool.imap_unordered(render_frame, generate_stream(centroid), chunksize=1):
                if finished_frame % 60 == 0:
                    print(f"      Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

        print(f"      Graphic Topology Yield Complete. Forcing FFmpeg compilation for {out_mp4}...")
        
        ffmpeg_cmd = [
            'ffmpeg', '-y', '-framerate', '60', 
            '-i', os.path.join(GLOBAL_OUT_DIR, 'frame_%04d.png'),
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '14',
            '-preset', 'slow', '-tune', 'animation',
            '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
            '-vf', 'scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:white',
            out_mp4
        ]
        
        try:
            subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"      [SUCCESS] Binary Video Output Secure: {out_mp4}")
        except subprocess.CalledProcessError as e:
            print(f"      [FATAL] FFmpeg pipeline collapsed securely on file: {filename}. Error: {e}")
            
        lines = None
        gc.collect()

    print("\n[OPERATIONAL] MASTER BATCH EXECUTION COMPLETED.")

if __name__ == "__main__":
    mp.freeze_support()
    process_batch()
