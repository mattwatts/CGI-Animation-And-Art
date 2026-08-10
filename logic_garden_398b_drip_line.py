"""
PROJECT: Logic Garden 398b (The Drip Line // Island of Stability)
FORMAT: YouTube Shorts (1080x1920)
METADATA: CHART OF NUCLIDES, NUCLEAR DRIP LINE, ISLAND OF STABILITY, SPALLATION
EXECUTION: 24.0s Sequence. True 3D Mathematical Construction.
RULES ENFORCED: 
- Daylight Palette (White Substrate / High Contrast).
- Phase-Locked Metaphor: Atomic disintegration rendered as rigid Z-axis spallation.
- O(N) True Polygon Depth Sorting.
- Australian spelling conventions enforced natively.
- Zero arbitrary filler. True cinematic realisational optics.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
from matplotlib.collections import PolyCollection
import multiprocessing as mp
import os
import gc

# ======== SEQUENCE PARAMETERS ========
FPS = 60
DURATION = 24.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_398b_drip_line"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG            = '#FFFFFF'  # Daylight / Absolute Void
C_TEXT          = '#111115'
C_EDGE          = '#111115'  # Indestructible Black (Polygon boundaries)
C_STABLE        = '#1E293B'  # Carbon Slate (The Valley Floor)
C_UNSTABLE      = '#005599'  # Deep Marine (General Instability)
C_DRIP          = '#FF3300'  # Intense Red (The Precipice / Spallation Zone)
C_ISLAND        = '#00C853'  # Jade (Theoretical Stability)
C_GUI           = '#64748B'

LIGHT_DIR = np.array([-0.6, 0.8, -0.4])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

# ------------------------------------------------------------------
# PHASE 1: EXACT PHYSICAL ISOTOPE MAP GENERATION
# ------------------------------------------------------------------
np.random.seed(398)
print("PHASE 1: COMPUTING THE THEORETICAL SEGRe TOPOLOGY...")

BLOCK_SIZE = 12.0
SPACING = 14.0

nuclides = []
colors = []
drip_flags = []  # Boolean array tracking the physical spallation edge

# Synthesize the exact empirical topography of the Valley of Stability
# Including the drip line bounds and the void gap.
for z in range(1, 130):
    target_n = int(z + 0.006 * (z ** 2))
    
    for n in range(max(0, target_n - 35), target_n + 35):
        d = n - (z + 0.006 * (z ** 2))
        
        # Determine Mathematical Bounds
        # 1. The Superheavy Void (Z between 104 and 110 where life is fleeting)
        is_void = (z > 104) and (z < 112)
        
        # 2. Island of Stability (Theoretical peak around Z=114, N=184)
        dist_to_island = np.sqrt((z - 114)**2 + (n - 184)**2)
        is_island = (dist_to_island < 5.5)
        
        c_state = None
        y_alt = 0.0
        is_drip_edge = False
        
        if is_island:
            c_state = C_ISLAND
            y_alt = 2.0
            if dist_to_island > 4.0:
                is_drip_edge = True
                c_state = C_DRIP
        elif not is_void and (z <= 104):
            # Known Matrix bounds
            if abs(d) <= 1.2:
                c_state = C_STABLE
                y_alt = 2.0 
            elif abs(d) < 22:
                c_state = C_UNSTABLE
                y_alt = 6.0 + np.abs(d) * 1.5
            elif abs(d) >= 22 and abs(d) <= 25:
                # The Physical Precipice (Drip line)
                c_state = C_DRIP
                y_alt = 6.0 + np.abs(d) * 1.5
                is_drip_edge = True

        if c_state:
            # X=Neutrons, Z=Protons
            nuclides.append([n * SPACING, y_alt, z * SPACING])
            colors.append(c_state)
            drip_flags.append(is_drip_edge)

N_NUCLIDES = len(nuclides)
nuclides = np.array(nuclides)
colors_base = np.array(colors)
drip_flags = np.array(drip_flags)

# Randomize fall velocities for the spallating nodes
fall_speeds = np.random.uniform(150.0, 450.0, N_NUCLIDES)
fall_delays = np.random.uniform(0.0, 5.0, N_NUCLIDES)

# ------------------------------------------------------------------
# 3D CUBE GEOMETRY GENERATOR (Brutalist Architecture)
# ------------------------------------------------------------------
def get_base_cube():
    v = np.array([
        [-1, -1, -1], [ 1, -1, -1], [ 1,  1, -1], [-1,  1, -1],
        [-1, -1,  1], [ 1, -1,  1], [ 1,  1,  1], [-1,  1,  1]
    ]) * 0.5
    faces = [
        [v[0], v[1], v[2]], [v[0], v[2], v[3]], # Front
        [v[1], v[5], v[6]], [v[1], v[6], v[2]], # Right
        [v[5], v[4], v[7]], [v[5], v[7], v[6]], # Back
        [v[4], v[0], v[3]], [v[4], v[3], v[7]], # Left
        [v[3], v[2], v[6]], [v[3], v[6], v[7]], # Top
        [v[4], v[5], v[1]], [v[4], v[1], v[0]], # Bottom
    ]
    return np.array(faces) 

BASE_CUBE = get_base_cube()

# ------------------------------------------------------------------
# TRUE MATRICES & PROJECTION
# ------------------------------------------------------------------
def get_view_matrix(cam_pos, target_pos, up_vector=np.array([0, 1.0, 0])):
    forward = target_pos - cam_pos
    f_len = np.linalg.norm(forward)
    if f_len < 1e-5: return np.eye(3)
    forward /= f_len
    right = np.cross(up_vector, forward)
    r_len = np.linalg.norm(right)
    if r_len < 1e-5: right = np.array([1.0, 0, 0])
    else: right /= r_len
    up = np.cross(forward, right)
    return np.array([right, up, forward])

def ease_in_out(t):
    t_c = np.clip(t, 0.0, 1.0)
    return 4 * t_c**3 if t_c < 0.5 else 1 - (-2 * t_c + 2)**3 / 2

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    t = f / float(FPS)

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.]); ax.set_axis_off(); fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540); ax.set_ylim(-960, 960)

    # 1. TIMELINE & ANIMATION LOGIC
    # Base extrude phase
    extrude_prog = np.clip(t / 4.0, 0.0, 1.0)
    
    # 2. CALCULATE PHYSICAL STATE MATRICES
    v_active = nuclides.copy()
    v_active[:, 1] = v_active[:, 1] * ease_in_out(extrude_prog) 
    
    scales_w = np.full((N_NUCLIDES, 3), BLOCK_SIZE)
    # Form skyscrapers grounded to Y=0
    scales_w[:, 1] = v_active[:, 1] * 2.0 
    v_active[:, 1] = v_active[:, 1] / 2.0 
    
    # KINEMATIC SPALLATION TENSOR
    # The drip edge continuously shears off into the void
    spall_time = max(0.0, t - 2.0)
    for i in range(N_NUCLIDES):
        if drip_flags[i]:
            time_active = max(0.0, spall_time - fall_delays[i])
            # Drop acceleration
            y_drop = (0.5 * 250.0 * (time_active ** 2))
            
            # Loop the drop logically to simulate endless breakdown at the edge
            if y_drop > 2000.0:
                fall_delays[i] += 4.0
                y_drop = 0.0
                
            v_active[i, 1] -= y_drop 

    # 3. FAST VECTORIZED CUBE GENERATION
    M_POLYS = v_active[:, None, None, :] + (BASE_CUBE[None, :, :, :] * (scales_w[:, None, None, :]/2.0))
    M_POLYS = M_POLYS.reshape(-1, 3, 3)

    c_rgb = np.array([mcolors.to_rgb(c) for c in colors_base])
    poly_rgb = np.repeat(c_rgb, 12, axis=0)

    # 4. CINEMATIC OUTWARD PUSH CAMERA (Over the Abyss)
    # Start looking at the stable peninsula, push directly over the edge to reveal the Island
    p_trace = ease_in_out(np.clip((t - 4.0) / 16.0, 0.0, 1.0))
    
    start_cent_n = 50 * SPACING
    start_cent_z = 40 * SPACING
    
    end_cent_n = 184 * SPACING
    end_cent_z = 114 * SPACING
    
    center_x = start_cent_n + (end_cent_n - start_cent_n) * p_trace
    center_z = start_cent_z + (end_cent_z - start_cent_z) * p_trace
    
    # Camera maintains an exact vector behind the focal point
    r_cam = 1500.0
    cam_x = center_x - r_cam * 0.8
    cam_z = center_z - r_cam * 0.8
    cam_y = 1200.0 - (p_trace * 300.0) # Slowly descend as we cross the void

    cam_pos = np.array([cam_x, cam_y, cam_z])
    target_pos = np.array([center_x, 0, center_z])
    
    M_view = get_view_matrix(cam_pos, target_pos)

    view_polys = np.einsum('ij,knj->kni', M_view, M_POLYS - cam_pos)
    centroids_z = np.mean(view_polys[:, :, 2], axis=1)

    # Exact Frustum Culling
    v_mask = centroids_z > 50.0
    view_polys = view_polys[v_mask]
    poly_rgb = poly_rgb[v_mask]
    centroids_z = centroids_z[v_mask]

    if len(view_polys) > 0:
        # True Lambertian Solid Substrate Shading
        v1 = view_polys[:, 1, :] - view_polys[:, 0, :]
        v2 = view_polys[:, 2, :] - view_polys[:, 0, :]
        norms = np.cross(v1, v2)
        n_len = np.linalg.norm(norms, axis=1, keepdims=True)
        norms /= np.maximum(n_len, 1e-5)
        
        L_DIR_VIEW = np.einsum('ij,j->i', M_view, LIGHT_DIR)
        diff = 0.2 + 0.8 * np.clip(np.dot(norms, L_DIR_VIEW), 0.0, 1.0)
        
        final_rgba = np.zeros((len(view_polys), 4))
        final_rgba[:, :3] = poly_rgb * diff[:, np.newaxis]
        final_rgba[:, 3] = 1.0

        z_safe = np.maximum(view_polys[:, :, 2], 1.0)
        proj_x = 2200.0 * (view_polys[:, :, 0] / z_safe)
        proj_y = 2200.0 * (view_polys[:, :, 1] / z_safe) + 150
        proj_polys = np.stack((proj_x, proj_y), axis=-1)

        sort_idx = np.argsort(centroids_z)[::-1]
        
        # Absolute high-contrast boundary welding
        col = PolyCollection(proj_polys[sort_idx], facecolors=final_rgba[sort_idx], edgecolors=C_EDGE, linewidths=0.25, zorder=10)
        ax.add_collection(col)

    # 5. HIGH-DENSITY HUD & TELEMETRY
    ax.add_patch(Rectangle((-540, 750), 1080, 210, facecolor=C_BG, zorder=80, alpha=0.9))
    ax.plot([-540, 540], [750, 750], color=C_TEXT, lw=4, zorder=81)

    ax.text(-500, 890, "LG-398b :: THE DRIP LINE & THE ISLAND", color=C_TEXT, fontsize=22, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 840, "[SFI-0.75] THEORETICAL BOUND / NUCLEAR SPALLATION TENSOR", color=C_GUI, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.9))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    if t < 6.0:
        p_str = "[+] OBSERVABLE PHYSICS: THE CONTINUOUS PENINSULA"
        c_stat = C_STABLE
    elif t < 16.0:
        p_str = "[-] CRITICAL LIMIT: KINEMATIC DRIP LINE REACHED"
        c_stat = C_DRIP
    else:
        p_str = "[+] THEORETICAL ARTIFACT: ISLAND OF STABILITY SIGHTED"
        c_stat = C_ISLAND

    cur_z = int((center_z / SPACING))
    cur_n = int((center_x / SPACING))

    ax.text(-500, -780, f"TOPOLOGICAL SECTOR : {p_str}", color=c_stat, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"CAMERA KINEMATICS  : TRACKING P={cur_z:03d} | N={cur_n:03d}", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"SPALLATION STATE   : EXTREME NUCLEON REJECTION RENDERED", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-398b: THE DRIP LINE VECTOR [CORES: {cpu_cores}]")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=4):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")
    print("Compilation Complete. Island of Stability Extracted.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
