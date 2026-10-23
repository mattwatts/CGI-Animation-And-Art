"""
PROJECT: Logic Garden 455 (Exact Physical Construct // Universal STL Batch Parser)
FORMAT: YouTube Shorts (1080x1920)
METADATA: STL, 3D PARSER, WIREFRAME, PYTHON, BATCH AUTOMATION
EXECUTION: 24.0s Sequence per payload. True Continuous Vector Architecture.
RULES ENFORCED:
- Autonomous Batching: Scans directory, sorts all STL payloads by byte mass.
- Pure Triangulation: Rejects non-spatial facets, calculates true edges natively.
- High-Density Decimation: Caps rendering density to prevent OS RAM flooding.
- Linux OOM Shield: FFmpeg strictly throttled to 2 threads, preset fast.
"""

import os
os.environ["MALLOC_TRIM_THRESHOLD_"] = "0"

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
import gc

try:
    trimesh.constants.tol.merge = 1e-10
    trimesh.constants.tol.zero = 1e-10
except:
    pass

# ======== SEQUENCE PARAMETERS ========
DURATION = 24.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
MAX_ALLOWABLE_EDGES = 15000

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

# ------------------------------------------------------------------
# .STL BARE-METAL EXTRACTOR 
# ------------------------------------------------------------------
def ingest_stl_payload(filepath):
    print(f"      [INGESTION] Engaging pure STL Triangulation Ripper for: {filepath}")
    
    try:
        # STL files are purely geometric. We bypass scenes completely.
        mesh = trimesh.load(filepath, file_type='stl', force='mesh', process=True)
    except Exception as e:
        print(f"      [FATAL] STL Substrate Corrupt or Unreadable. Mathematics failed: {e}")
        return None, None

    if not hasattr(mesh, 'edges_unique') or len(mesh.edges_unique) == 0:
        print("      [FATAL] STL yields zero edges. Topologies corrupt.")
        return None, None

    edges_indices = mesh.edges_unique
    vertices = mesh.vertices

    # Reconstruct exact vertex pairs
    raw_edges = []
    for pair in edges_indices:
        raw_edges.append([vertices[pair[0]], vertices[pair[1]]])
        
    edges_array = np.array(raw_edges)
    total_raw_edges = len(edges_array)

    if total_raw_edges == 0:
        print("      [FATAL] Pipeline Blockage. STL geometry evaluates natively as computationally dead.")
        return None, None

    decimation_step = int(np.ceil(total_raw_edges / float(MAX_ALLOWABLE_EDGES)))
    
    if decimation_step > 1:
        edges_array = edges_array[::decimation_step]
        print(f"      [OOM SHUTTLE] True physical edges mapped: {total_raw_edges}. Decimated systematically (1-in-{decimation_step}) to prevent RAM overflow.")
    else:
        print(f"      [GEOMETRY] Topology bound within limit. Edges mapped: {total_raw_edges}.")

    flat_verts = edges_array.reshape(-1, 3)
    valid_verts = flat_verts[~np.isnan(flat_verts).any(axis=1)]
    
    min_b = np.min(valid_verts, axis=0)
    max_b = np.max(valid_verts, axis=0)
    true_centroid = (min_b + max_b) / 2.0
    extent_eval = float(np.max(max_b - min_b))

    scale_factor = 10.0 / (extent_eval if extent_eval > 0 else 1.0)
    normalized_edges = (edges_array - true_centroid) * scale_factor
    print(f"      [NORMALISATION] Matrix safely stabilised boundary by factor of {scale_factor:.2e}")

    lines_output = {'C_GRID': []}
    for c in MESH_PALETTE:
        lines_output[c] = []

    # Map directly to palette layers
    for i, edge in enumerate(normalized_edges):
        col_key = MESH_PALETTE[i % len(MESH_PALETTE)]
        lines_output[col_key].append(([edge[0][0], edge[1][0]], [edge[0][1], edge[1][1]], [edge[0][2], edge[1][2]]))

    # Ground Tracking Frame Definition (Translates underneath lowest point)
    z_floor = (min_b[2] - true_centroid[2]) * scale_factor - 1.0 
    grid_radii = [2.5, 4.0, 6.0]
    for r_p in grid_radii:
        t_p = np.linspace(0, 2*np.pi, 32, endpoint=False)
        for i in range(len(t_p)-1):
            xs = [r_p * np.cos(t_p[i]), r_p * np.cos(t_p[i+1])]
            ys = [r_p * np.sin(t_p[i]), r_p * np.sin(t_p[i+1])]
            zs = [z_floor, z_floor]
            lines_output['C_GRID'].append((xs, ys, zs))

    cam_span = 5.0 * 1.30
    
    del raw_edges, edges_array, flat_verts, normalized_edges, mesh
    gc.collect()
    
    return lines_output, cam_span

# ------------------------------------------------------------------
# MASTER RENDERER HOOK & WORKER INITIALIZER
# ------------------------------------------------------------------
GLOBAL_LINES = None
GLOBAL_CAM_SPAN = None
GLOBAL_TARGET_NAME = None
GLOBAL_OUT_DIR = None

def init_worker(lines_bundle, span_bundle, name_bundle, out_bundle):
    global GLOBAL_LINES, GLOBAL_CAM_SPAN, GLOBAL_TARGET_NAME, GLOBAL_OUT_DIR
    GLOBAL_LINES = lines_bundle
    GLOBAL_CAM_SPAN = span_bundle
    GLOBAL_TARGET_NAME = name_bundle
    GLOBAL_OUT_DIR = out_bundle

def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        yield (f, t_sec, 115.0 - (stage * 360.0), 0.0, 0.0, 0.0)

def render_frame(packet):
    f, t_sec, azimuth, cx, cy, cz = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

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

    ax.text(-GLOBAL_CAM_SPAN*0.95, ui_t + GLOBAL_CAM_SPAN*0.08, "LG-455 // MACRO-ENGINEERING TENSOR: STRUCTURAL KINEMATICS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-GLOBAL_CAM_SPAN*0.95, ui_t + GLOBAL_CAM_SPAN*0.02, f"EXPLICIT STL BASE LOGIC // FILE: {GLOBAL_TARGET_NAME.upper()}", color=MESH_PALETTE[0], fontsize=12, fontname='monospace', weight='bold', zorder=82)

    ui_b = -GLOBAL_CAM_SPAN * 1.777
    ax.add_patch(patches.Rectangle((-GLOBAL_CAM_SPAN, ui_b), GLOBAL_CAM_SPAN*2, GLOBAL_CAM_SPAN*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-GLOBAL_CAM_SPAN, GLOBAL_CAM_SPAN], [ui_b + GLOBAL_CAM_SPAN*0.35, ui_b + GLOBAL_CAM_SPAN*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-GLOBAL_CAM_SPAN*0.95, ui_b + GLOBAL_CAM_SPAN*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT HIGH-CONTRAST TRACE", color=MESH_PALETTE[1], fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-GLOBAL_CAM_SPAN*0.95, ui_b + GLOBAL_CAM_SPAN*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-GLOBAL_CAM_SPAN*0.95, ui_b + GLOBAL_CAM_SPAN*0.02, f"TOPOLOGICAL YIELD: TRUE GEOMETRIC TRIANGULATION BOUNDARY", color=C_TEXT, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(GLOBAL_OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    
    plt.close("all")
    fig.clf()
    del fig
    gc.collect()
    
    return f

# ------------------------------------------------------------------
# BATCH ORCHESTRATION & AUTOMATED FFMPEG PIPELINE
# ------------------------------------------------------------------
def process_batch():
    # DIRECTORY BOUNDARY SCAN FOR STL EXTENSIONS
    stl_files = glob.glob("*.stl") + glob.glob("*.STL")
    if not stl_files:
        print("[FATAL] Zero .stl payloads detected in the active working directory.")
        sys.exit(1)

    stl_files = list(set(stl_files)) # Remove case-insensitive duplicates if present
    stl_files.sort(key=lambda f: os.path.getsize(f))
    
    cpu_cores = max(1, mp.cpu_count() // 2)
    print(f"LG-455: AUTONOMOUS STL BATCH PIPELINE ENGAGED [THROTTLED CORES: {cpu_cores}]")
    print(f"Payloads detected: {len(stl_files)} (Sorted efficiently by byte mass)")

    for idx, filepath in enumerate(stl_files):
        filename = os.path.basename(filepath)
        basename, _ = os.path.splitext(filename)
        out_mp4 = f"{basename}.mp4"
        
        GLOBAL_TARGET_NAME = filename
        GLOBAL_OUT_DIR = f"frames_{basename}"
        os.makedirs(GLOBAL_OUT_DIR, exist_ok=True)

        size_mb = os.path.getsize(filepath) / (1024*1024)
        print(f"\n[{idx+1}/{len(stl_files)}] PARSING PAYLOAD: {filename} ({size_mb:.2f} MB)")
        
        lines, cam_span = ingest_stl_payload(filepath)
        
        if lines is None:
            continue
        
        print(f"      Initiating Core Pool -> Rendering {TOTAL_FRAMES} frames...")
        
        with mp.Pool(processes=cpu_cores, maxtasksperchild=180, 
                     initializer=init_worker, 
                     initargs=(lines, cam_span, GLOBAL_TARGET_NAME, GLOBAL_OUT_DIR)) as pool:
            
            for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
                if finished_frame % 60 == 0:
                    print(f"      Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

        print(f"      Graphic Topology Yield Complete. Forcing FFmpeg compilation for {out_mp4}...")
        
        ffmpeg_cmd = [
            'ffmpeg', '-y', '-framerate', '60', 
            '-i', f'{GLOBAL_OUT_DIR}/frame_%04d.png',
            '-threads', '2', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18',
            '-preset', 'fast', '-tune', 'animation',
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

    print("\n[OPERATIONAL] MASTER STL BATCH EXECUTION COMPLETED.")

if __name__ == "__main__":
    mp.freeze_support()
    process_batch()
