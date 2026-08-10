"""
PROJECT: Logic Garden 406 (Stereoscopy // Binocular Parallax Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: STEREOSCOPY, BINOCULAR VISION, ANAGLYPH, PARALLAX, GEOMETRY
EXECUTION: 24.0s Sequence. True 3D Dual-Origin Projection.
RULES ENFORCED:
- Daylight Palette (White Substrate / High-Contrast Chrome).
- Phase-Locked Metaphor: The Cyclops Fallacy into Binocular Fracture.
- Exact realisational aspect of stereoscopic disparity mapping (1/Z scaling).
- Pure O(N) mathematical drafting in strictly split Red/Cyan spectrums.
- Australian spelling conventions enforced natively (Maths, Colour, Optimise).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
from matplotlib.collections import LineCollection
import multiprocessing as mp
import os
import gc

# ======== SEQUENCE PARAMETERS ========
FPS = 60
DURATION = 24.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_406_stereoscopy"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG            = '#FFFFFF'
C_TEXT          = '#111115'
C_MONO_EDGE     = '#111115'  # Indestructible Black (Cyclops Fallacy Phase)
C_LEFT_EYE      = '#FF3300'  # Intense Red (Left Optical Sensor)
C_RIGHT_EYE     = '#00D2FF'  # High-Contrast Cyan (Right Optical Sensor)
C_GUI           = '#64748B'

# ------------------------------------------------------------------
# O(1) 3D ARCHITECTURAL GENERATOR (THE FLOATING TUNNEL)
# ------------------------------------------------------------------
FOCAL_LENGTH = 1800.0  
NUM_ARCHES = 120
Z_SPACING = 400.0

MAX_IPD = 180.0 # Exaggerated Interpupillary Distance for striking mobile display

# Generate a brutalist wireframe tunnel of rigid nested squares
LINES_3D = []
for i in range(NUM_ARCHES):
    z = i * Z_SPACING
    
    # Outer Frame Boundary
    o_x, o_y = 350.0, 350.0
    p1 = [-o_x, -o_y, z]; p2 = [ o_x, -o_y, z]
    p3 = [ o_x,  o_y, z]; p4 = [-o_x,  o_y, z]
    
    # Inner Frame Boundary
    i_x, i_y = 250.0, 250.0
    p5 = [-i_x, -i_y, z]; p6 = [ i_x, -i_y, z]
    p7 = [ i_x,  i_y, z]; p8 = [-i_x,  i_y, z]
    
    # Assembly
    arch_lines = [
        [p1, p2], [p2, p3], [p3, p4], [p4, p1], # Outer Loop
        [p5, p6], [p6, p7], [p7, p8], [p8, p5], # Inner Loop
        [p1, p5], [p2, p6], [p3, p7], [p4, p8]  # Connecting Struts
    ]
    LINES_3D.extend(arch_lines)

LINES_3D = np.array(LINES_3D) # Shape: (N_lines, 2_pts, 3_coords)
print(f"PHASE 1: PRE-COMPUTED STRUCTURAL MATRIX [{len(LINES_3D)} VECTORS]")

# ------------------------------------------------------------------
# MATRIX OPERATIONS
# ------------------------------------------------------------------
def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)

def project_lines(lines_3d, cam_z, ipd_offset):
    # World matrix to local Camera matrix
    c_space = lines_3d - np.array([0.0, 0.0, cam_z])
    
    # Absolute Z-Clipping Tensor (Delete lines breaching the lens to prevent mathematical tear)
    z_min1 = c_space[:, 0, 2]
    z_min2 = c_space[:, 1, 2]
    valid_mask = (z_min1 > 50.0) & (z_min2 > 50.0)
    
    valid_lines = c_space[valid_mask]
    if len(valid_lines) == 0:
        return []
        
    # Stereoscopic projection matrix
    # X_disp = X_target - X_cam_offset
    dx = valid_lines[:, :, 0] - ipd_offset
    dy = valid_lines[:, :, 1]
    dz = valid_lines[:, :, 2]
    
    px = FOCAL_LENGTH * (dx / dz)
    py = FOCAL_LENGTH * (dy / dz)
    
    # Format into (N, 2, 2) array for matplotlib LineCollection
    return np.stack((px, py), axis=-1)

def lerp_colour(c1_hex, c2_hex, t):
    c1 = np.array(mcolors.to_rgb(c1_hex))
    c2 = np.array(mcolors.to_rgb(c2_hex))
    return c1 * (1 - t) + c2 * t

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f_idx):
    t_sec = f_idx / float(FPS)
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.]); ax.set_axis_off(); fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540); ax.set_ylim(-960, 960)

    # 1. KINEMATIC TIMELINE TENSORS
    # Phase 1 -> 2: IPD Fracture (3.0s to 6.0s)
    fracture_prog = smoothstep((t_sec - 3.0) / 3.0)
    current_ipd = MAX_IPD * fracture_prog
    
    # Phase 2 -> 3: Z-Transit Acceleration (4.0s to 24.0s)
    z_transit_prog = (t_sec - 4.0) / 20.0
    if z_transit_prog > 0:
        # Exponential curve for massive speed rushing past the camera
        cam_z = 25000.0 * (z_transit_prog ** 1.3)
    else:
        cam_z = 0.0

    # 2. CHROMATIC ISOLATION (The Anaglyph Filter)
    # The edges dynamically burn from Indestructible Black into Red/Cyan as IPD widens
    c_left = mcolors.to_rgba(lerp_colour(C_MONO_EDGE, C_LEFT_EYE, fracture_prog), 1.0)
    c_right = mcolors.to_rgba(lerp_colour(C_MONO_EDGE, C_RIGHT_EYE, fracture_prog), 1.0)

    queue = []
    
    # 3. STEREOSCOPIC DOUBLE PROJECTION
    # Right Eye tracks from POSITIVE offset, so optical data shifts negatively
    proj_R = project_lines(LINES_3D, cam_z, ipd_offset= current_ipd/2.0)
    # Left Eye tracks from NEGATIVE offset, so optical data shifts positively
    proj_L = project_lines(LINES_3D, cam_z, ipd_offset=-current_ipd/2.0)

    if len(proj_L) > 0:
        # Paint the Left Array (Red)
        ax.add_collection(LineCollection(proj_L, colors=[c_left], linewidths=2.5, capstyle='round'))
    
    if len(proj_R) > 0:
        # Paint the Right Array (Cyan)
        ax.add_collection(LineCollection(proj_R, colors=[c_right], linewidths=2.5, capstyle='round'))

    # 4. HIGH-DENSITY HUD & TELEMETRY
    ax.add_patch(Rectangle((-540, 780), 1080, 180, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [780, 780], color=C_TEXT, lw=3, zorder=81)
    ax.text(-500, 880, "LG-406 :: STEREOSCOPY", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 830, "[SFI-1.00] BINOCULAR PARALLAX & DISPARITY TENSORS", color=C_GUI, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    if t_sec < 3.0:
        state_msg = "PHASE 1: THE CYCLOPS FALLACY (MONOCULAR)"
        state_col = C_MONO_EDGE
        metric_txt = "MATHEMATICAL HORIZON IS FLAT AND SINGULAR"
        prog = 0.0
    elif t_sec < 8.0:
        state_msg = "PHASE 2: BINOCULAR FRACTURE (IPD INJECTION)"
        state_col = C_LEFT_EYE
        metric_txt = f"INTERPUPILLARY DISTANCE (IPD): {current_ipd:05.1f} MM"
        prog = np.clip((t_sec - 3.0) / 5.0, 0.0, 1.0)
    else:
        state_msg = "PHASE 3: Z-TRANSIT PARALLAX SHIFT (ANAGLYPH)"
        state_col = C_RIGHT_EYE
        # Find nearest un-clipped valid arch for telemetry readout
        z_near = ((cam_z // Z_SPACING) + 1) * Z_SPACING 
        dist_z = max(z_near - cam_z, 50.0)
        disparity_val = (FOCAL_LENGTH * current_ipd) / dist_z
        metric_txt = f"GEOMETRIC DISPARITY (f*IPD/Z) = {disparity_val:06.1f}px"
        prog = np.clip((t_sec - 8.0) / 16.0, 0.0, 1.0)

    ax.text(-500, -780, f"CURRENT STATE: {state_msg}", color=state_col, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"SYSTEM DIAGNOSTIC: {metric_txt}", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"AXIOMATIC TRUTH  : DEPTH IS MATHEMATICALLY INVERSE TO X-AXIS DISPLACEMENT.", color=C_TEXT, fontsize=11, fontname='monospace', zorder=82)

    ax.add_patch(Rectangle((-500, -920), 1000, 8, facecolor=C_GUI, zorder=82))
    ax.add_patch(Rectangle((-500, -920), 1000 * prog, 8, facecolor=state_col, zorder=83))

    # Real-time Lens Status
    ax.text(-500, 740, f"L-OPTIC [RED]: X = {-current_ipd/2:05.1f}", color=C_LEFT_EYE, fontsize=12, fontname='monospace', weight='bold', zorder=82)
    ax.text(200, 740, f"R-OPTIC [CYAN]: X = {+current_ipd/2:05.1f}", color=C_RIGHT_EYE, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f_idx:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f_idx

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-406: STEREOSCOPIC TENSORS ENGAGED [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")
    print("Compilation Complete. Parallax math mapped.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
