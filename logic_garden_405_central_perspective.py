"""
PROJECT: Logic Garden 405 (Central Perspective // Algorithmic Compression)
FORMAT: YouTube Shorts (1080x1920)
METADATA: CENTRAL PERSPECTIVE, EUCLIDEAN GEOMETRY, ARCHITECTURE, MATHEMATICAL DRAFTING
EXECUTION: 24.0s Sequence. True 3D Extrusion and Spatial Transit.
RULES ENFORCED:
- Daylight Palette (White Substrate / High Contrast).
- Phase-Locked Metaphor: Scaffolding the Null Locus before matter generation.
- Exact realisational aspect of One-Point Linear Perspective.
- Pure O(1) Lambertian Shaded Cathedral Arcade Extrusion.
- Australian spelling conventions enforced natively (Maths, Visualise).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
from matplotlib.collections import PolyCollection, LineCollection
import multiprocessing as mp
import os
import gc

# ======== SEQUENCE PARAMETERS ========
FPS = 60
DURATION = 24.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_405_central_perspective"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG            = '#FFFFFF'
C_TEXT          = '#111115'
C_EDGE          = '#111115'
C_VANISH        = '#DE008A'  # Deep Magenta (The Null Locus & Orthogonals)
C_STEEL         = '#94A3B8'  # Machined Smooth Steel 
C_GRID          = '#94A3B8'  # Substrate Floor Matrix
C_GUI           = '#64748B'

LIGHT_DIR = np.array([-0.4, 0.8, -0.6])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

# ------------------------------------------------------------------
# O(1) PERSPECTIVE TENSOR MECHANICS
# ------------------------------------------------------------------
FOCAL_LENGTH = 1800.0  # Perfect undistorted architectural 35mm-equivalent FOV
CAM_Y = 150.0          # Absolute Observer Altitude (The Horizon Matrix)

# Base Unity Face Tensor: X in [-0.5, 0.5], Y in [0, 1], Z in [-0.5, 0.5]
# Outward-facing Normals guaranteed by exact Right-Hand counter-clockwise ordering
UNIT_FACES = np.array([
    [[-.5, 0, -.5], [-.5, 1, -.5], [ .5, 1, -.5], [ .5, 0, -.5]], # Front (-Z)
    [[ .5, 0,  .5], [ .5, 1,  .5], [-.5, 1,  .5], [-.5, 0,  .5]], # Back (+Z)
    [[-.5, 1, -.5], [-.5, 1,  .5], [ .5, 1,  .5], [ .5, 1, -.5]], # Top (+Y)
    [[-.5, 0,  .5], [-.5, 0, -.5], [ .5, 0, -.5], [ .5, 0,  .5]], # Bottom (-Y)
    [[-.5, 0,  .5], [-.5, 1,  .5], [-.5, 1, -.5], [-.5, 0, -.5]], # Left (-X)
    [[ .5, 0, -.5], [ .5, 1, -.5], [ .5, 1,  .5], [ .5, 0,  .5]]  # Right (+X)
])

# ------------------------------------------------------------------
# 3D ARCHITECTURAL GENERATOR (THE SOVEREIGN ARCADE)
# ------------------------------------------------------------------
NUM_BAYS = 100
SPACING = 300
W_P = 150; H_P = 600; D_P = 150
W_B = 300; H_B = 100; D_B = 150

ALL_FACES_BASE = []
for i in range(NUM_BAYS):
    z_pos = 500 + i * SPACING
    # Brutalist Left Pillar
    p_left_cx = -300 + W_P/2
    for f in UNIT_FACES:
        face = f * np.array([W_P, H_P, D_P]) + np.array([p_left_cx, 0, z_pos])
        ALL_FACES_BASE.append(face)
        
    # Brutalist Right Pillar
    p_right_cx = 300 - W_P/2
    for f in UNIT_FACES:
        face = f * np.array([W_P, H_P, D_P]) + np.array([p_right_cx, 0, z_pos])
        ALL_FACES_BASE.append(face)
        
    # Connecting Crossbeam (Cathedral Arch)
    b_cx = 0
    for f in UNIT_FACES:
        # Crossbeam is suspended, so its unit base Y goes from Top - H_B to Top
        y_shift = H_P - H_B
        face = f * np.array([W_B, H_B, D_B]) + np.array([b_cx, y_shift, z_pos])
        ALL_FACES_BASE.append(face)

ALL_FACES_BASE = np.array(ALL_FACES_BASE)
print(f"PHASE 1: PRE-COMPUTED CATHEDRAL TENSOR [{ALL_FACES_BASE.shape[0]} FACES]")

# Mathematical Orthogonal Tracking Rails
RAILS = np.array([
    [[-150, 0, 0],   [-150, 0, 30000]],
    [[ 150, 0, 0],   [ 150, 0, 30000]],
    [[-450, 0, 0],   [-450, 0, 30000]],
    [[ 450, 0, 0],   [ 450, 0, 30000]],
    [[-150, 600, 0], [-150, 600, 30000]],
    [[ 150, 600, 0], [ 150, 600, 30000]],
])

def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f_idx):
    t_sec = f_idx / float(FPS)
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.]); ax.set_axis_off(); fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540); ax.set_ylim(-960, 960)

    # 1. MATHEMATICAL PHASE TENSORS
    # Extrusion Scaling (Y-Axis grows to prove mathematical fill)
    h_scale = 0.0 if t_sec < 4.0 else (smoothstep((t_sec - 4.0) / 4.0) if t_sec < 8.0 else 1.0)
    
    # Kinematic Viewer Depth (Z-Transit)
    z_cam = 0.0 if t_sec < 12.0 else 17000.0 * (smoothstep((t_sec - 12.0) / 12.0) ** 1.5)
    
    # Kinematic Orthogonal Vector Distance
    z_rail_limit = 30000.0 * np.clip((t_sec - 1.0) / 2.0, 0.0, 1.0)

    def project_3d_to_2d(pts_3d):
        c_space = pts_3d - np.array([0.0, CAM_Y, z_cam])
        valid = c_space[:, 2] > 10.0
        z_safe = np.maximum(c_space[:, 2], 10.0)
        px = FOCAL_LENGTH * (c_space[:, 0] / z_safe)
        py = FOCAL_LENGTH * (c_space[:, 1] / z_safe)
        return np.column_stack((px, py)), c_space[:, 2], valid

    # 2. DRAW PHASE 1 (HORIZON & NULL LOCUS)
    if t_sec > 0.0:
        horiz_prog = np.clip(t_sec / 1.0, 0.0, 1.0)
        ax.plot([-540 * horiz_prog, 540 * horiz_prog], [0, 0], color=C_VANISH, lw=1.5, zorder=5) # Absolute Horizon (py=0)
    if t_sec > 1.0:
        rad = np.clip((t_sec - 1.0)*30, 0, 15)
        ax.add_patch(plt.Circle((0, 0), rad, color=C_BG, ec=C_VANISH, lw=2.0, zorder=6))
        ax.plot([-rad*1.5, rad*1.5], [0, 0], color=C_VANISH, lw=2.0, zorder=7)
        ax.plot([0, 0], [-rad*1.5, rad*1.5], color=C_VANISH, lw=2.0, zorder=7)

    # 3. DRAW ORTHOGONAL TRACKING RAILS & FLOOR GRID
    line_collection_data = []
    line_colors = []
    
    if t_sec > 1.0:
        c_vanish_rgb = mcolors.to_rgba(C_VANISH, 0.8)
        # Main Bounding Box Rails
        for rail in RAILS:
            p1, p2 = np.copy(rail[0]), np.copy(rail[1])
            p2[2] = min(p2[2], z_rail_limit)
            if p2[2] > z_cam + 10.0:
                p1[2] = max(p1[2], z_cam + 10.0)
                pts_2d, _, _ = project_3d_to_2d(np.array([p1, p2]))
                line_collection_data.append(pts_2d)
                line_colors.append(c_vanish_rgb)

        # Floor Geometry Euclidean Grid (X-Lines)
        c_grid_rgb = mcolors.to_rgba(C_GRID, 0.4)
        for tz in range(0, 30000, 300):
            if z_cam + 10.0 < tz < z_rail_limit:
                p1, p2 = np.array([-1500, 0, tz]), np.array([1500, 0, tz])
                pts_2d, _, _ = project_3d_to_2d(np.array([p1, p2]))
                line_collection_data.append(pts_2d)
                line_colors.append(c_grid_rgb)
                
    if line_collection_data:
        lc = LineCollection(line_collection_data, colors=line_colors, lw=1.5, zorder=10)
        ax.add_collection(lc)

    # 4. EXTRUDE AND PROJECT O(N) ARCADE POLYGONS
    if h_scale > 0.0:
        scaled_faces = ALL_FACES_BASE.copy()
        scaled_faces[:, :, 1] *= h_scale
        
        # World to Camera Space Shift
        # v_cam shape is (N, 4, 3)
        v_cam = scaled_faces - np.array([0.0, CAM_Y, z_cam])
        
        # Strict Z-Clipping Algorithm. Cull faces breaching near-plane to avoid perspective tear.
        valid_mask = np.all(v_cam[:, :, 2] > 15.0, axis=1)
        v_cam = v_cam[valid_mask]
        
        if len(v_cam) > 0:
            centroids = np.mean(v_cam, axis=1)
            v1 = v_cam[:, 1] - v_cam[:, 0]
            v2 = v_cam[:, 2] - v_cam[:, 0]
            norms = np.cross(v1, v2)
            
            n_lens = np.linalg.norm(norms, axis=1, keepdims=True)
            norms = norms / np.maximum(n_lens, 1e-5)
            
            # Line of Sight Culling: The true viewing vector is exactly the centroid relative to origin.
            dots_cull = np.sum(norms * centroids, axis=1)
            visible_mask = dots_cull < 0
            
            v_cam = v_cam[visible_mask]
            norms = norms[visible_mask]
            centroids = centroids[visible_mask]
            
            if len(v_cam) > 0:
                # Lambertian Shading against absolute light vector
                diffuse = 0.3 + 0.7 * np.clip(np.dot(norms, LIGHT_DIR), 0, 1)
                
                fcs = np.zeros((len(v_cam), 4))
                fcs[:, :3] = np.array(mcolors.to_rgb(C_STEEL)) * diffuse[:, np.newaxis]
                fcs[:, 3] = 1.0 
                
                px = FOCAL_LENGTH * (v_cam[:, :, 0] / v_cam[:, :, 2])
                py = FOCAL_LENGTH * (v_cam[:, :, 1] / v_cam[:, :, 2])
                polys_2d = np.stack((px, py), axis=-1)
                
                # Z-Sort (Painter's Algorithm) using absolute depth indices
                z_sort = np.argsort(centroids[:, 2])[::-1]
                
                sorted_polys = polys_2d[z_sort]
                sorted_fcs = fcs[z_sort]
                
                # O(N) Matrix Paint
                poly_col = PolyCollection(sorted_polys, facecolors=sorted_fcs, edgecolors=C_EDGE, linewidths=1.2, joinstyle='miter', zorder=20)
                ax.add_collection(poly_col)

    # 5. HIGH-DENSITY HUD & TELEMETRY
    ax.add_patch(Rectangle((-540, 780), 1080, 180, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [780, 780], color=C_TEXT, lw=3, zorder=81)
    ax.text(-500, 880, "LG-405 :: CENTRAL PERSPECTIVE", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 830, "[SFI-1.00] ALGORITHMIC COMPRESSION OF EUCLIDEAN SPACE", color=C_GUI, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    if t_sec < 4.0:
        state_msg = "PHASE 1: THE NULL LOCUS & ORTHOGONAL RAILS"
        state_col = C_VANISH
        metric = f"HORIZON TENSOR: STATIC [Y = {CAM_Y}]"
        prog = 0.0
    elif t_sec < 10.0:
        state_msg = "PHASE 2: ALGORITHMIC BINARY MESH EXTRUSION"
        state_col = C_STEEL
        metric = f"Z-PLANE DEPTH MATRIX: {z_rail_limit:05.1f} UNITS"
        prog = np.clip((t_sec - 4.0) / 6.0, 0.0, 1.0)
    elif t_sec < 12.0:
        state_msg = "PHASE 3: EUCLIDEAN STASIS ACHIEVED"
        state_col = C_GRID
        metric = f"INVERSE SCALE YIELD (1/Z) PROVING DISTANCE"
        prog = 1.0
    else:
        state_msg = "PHASE 4: KINEMATIC Z-AXIS TRANSIT (FLY-THROUGH)"
        state_col = C_VANISH
        metric = f"OBSERVER MATRIX COORDINATE: Z = {z_cam:06.1f}"
        prog = np.clip((t_sec - 12.0) / 12.0, 0.0, 1.0)

    ax.text(-500, -780, f"CURRENT STATE  : {state_msg}", color=state_col, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"SYSTEM DIAGNOSTIC: {metric}", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"AXIOMATIC TRUTH  : 3D VOLUME GEOMETRICALLY COMPRESSED TO A 2D SINGULARITY.", color=C_TEXT, fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(Rectangle((-500, -920), 1000, 8, facecolor=C_GUI, zorder=82))
    ax.add_patch(Rectangle((-500, -920), 1000 * prog, 8, facecolor=state_col, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f_idx:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f_idx

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-405: PERSPECTIVE TENSOR ENGAGED [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")
    print("Compilation Complete. Space geometrically compressed.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
