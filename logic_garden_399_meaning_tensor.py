"""
PROJECT: Logic Garden 399 (The Meaning Tensor // Sovereign Alignment)
FORMAT: YouTube Shorts (1080x1920)
METADATA: PHASE TRANSITION, ENTROPY, TOPOLOGY OF MEANING, KINEMATICS
EXECUTION: 24.0s Sequence. True 3D Mathematical Construction.
RULES ENFORCED: 
- Daylight Palette (White Substrate / High Contrast).
- Phase-Locked Metaphor: The literal algorithmic mapping of chaos to meaning via orientation.
- True Line-of-Sight Painter's Algorithm.
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
OUT_DIR = "frames_399_meaning_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG            = '#FFFFFF'  # Daylight Void
C_TEXT          = '#111115'
C_EDGE          = '#111115'  # Indestructible Black bounds
C_NOISE         = '#1E293B'  # Carbon Slate (Chaos / Entropy)
C_ANCHOR        = '#DE008A'  # Deep Magenta (The Sovereign Monolith)
C_MEANING       = '#FFB300'  # Dense Amber (Aligned / Oriented Data)
C_GUI           = '#64748B'

LIGHT_DIR = np.array([-0.6, 0.8, -0.4])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

# ------------------------------------------------------------------
# PHASE 1: PRE-COMPUTE THE CHAOTIC SUBSTRATE
# ------------------------------------------------------------------
np.random.seed(399)
print("PHASE 1: SYNTHESIZING MAXIMUM ENTROPY...")

N_POINTERS = 2000
FIELD_RADIUS = 1200.0

# Generate random spatial positions in a cylindrical volume
r_pos = np.random.uniform(150.0, FIELD_RADIUS, N_POINTERS)
theta_pos = np.random.uniform(0, 2 * np.pi, N_POINTERS)
y_pos = np.random.uniform(-400.0, 400.0, N_POINTERS)

px = r_pos * np.cos(theta_pos)
pz = r_pos * np.sin(theta_pos)
pos_matrix = np.column_stack((px, y_pos, pz))

# Generate chaotic intrinsic rotation vectors
rot_axis = np.random.normal(size=(N_POINTERS, 3))
rot_axis /= np.linalg.norm(rot_axis, axis=1, keepdims=True)
rot_speed = np.random.uniform(1.0, 5.0, N_POINTERS)
initial_phase = np.random.uniform(0, 2*np.pi, N_POINTERS)

# Define a single Pointer Tetrahedron (Arrow pointing along +Z)
PTR_W = 20.0
PTR_L = 50.0
BASE_PTR = np.array([
    [-PTR_W, -PTR_W, -PTR_L],
    [ PTR_W, -PTR_W, -PTR_L],
    [   0.0,  PTR_W, -PTR_L],
    [   0.0,    0.0,  PTR_L]   # The tip
])

# 4 Faces of the Tetrahedron (Strictly Triangulated, N=3)
PTR_FACES = np.array([
    [BASE_PTR[0], BASE_PTR[1], BASE_PTR[2]], # Back plate
    [BASE_PTR[0], BASE_PTR[1], BASE_PTR[3]], # Bottom plate
    [BASE_PTR[1], BASE_PTR[2], BASE_PTR[3]], # Right plate
    [BASE_PTR[2], BASE_PTR[0], BASE_PTR[3]]  # Left plate
])

# Generate The Sovereign Monolith (12-sided indestructible cylinder)
M_RAD = 80.0
M_HEIGHT_HALF = 1800.0
monolith_verts = []
SIDES = 12
for i in range(SIDES):
    a1 = i * 2 * np.pi / SIDES
    a2 = (i+1) * 2 * np.pi / SIDES
    x1, z1 = np.cos(a1)*M_RAD, np.sin(a1)*M_RAD
    x2, z2 = np.cos(a2)*M_RAD, np.sin(a2)*M_RAD
    
    # Strict O(1) Triangulation: Slicing the 4-vertex quad into two 3-vertex polygons
    p1 = [x1, -M_HEIGHT_HALF, z1]
    p2 = [x2, -M_HEIGHT_HALF, z2]
    p3 = [x2, M_HEIGHT_HALF, z2]
    p4 = [x1, M_HEIGHT_HALF, z1]
    
    monolith_verts.append([p1, p2, p4])
    monolith_verts.append([p2, p3, p4])
    
M_MONOLITH_FACES = np.array(monolith_verts)

# ------------------------------------------------------------------
# KINEMATIC MATH ENGINES
# ------------------------------------------------------------------
def axis_angle_matrix(axes, angles):
    """Vectorized Axis-Angle to Rotation Matrix."""
    c = np.cos(angles)
    s = np.sin(angles)
    C = 1 - c
    x, y, z = axes[:,0], axes[:,1], axes[:,2]
    
    R = np.zeros((len(axes), 3, 3))
    R[:,0,0] = x*x*C + c;     R[:,0,1] = x*y*C - z*s;   R[:,0,2] = x*z*C + y*s
    R[:,1,0] = y*x*C + z*s;   R[:,1,1] = y*y*C + c;     R[:,1,2] = y*z*C - x*s
    R[:,2,0] = z*x*C - y*s;   R[:,2,1] = z*y*C + x*s;   R[:,2,2] = z*z*C + c
    return R

def get_target_rotations(positions):
    """
    Computes the exact orientation required for meaning.
    The pointer must aim perfectly at the Anchor (0, y, 0), acknowledging the Sovereign.
    """
    target_vec = -positions.copy()
    target_vec[:, 1] *= 0.5 # Point slightly inward but maintain spatial level
    target_len = np.linalg.norm(target_vec, axis=1, keepdims=True)
    target_vec /= np.maximum(target_len, 1e-5)
    
    initial_vec = np.array([0, 0, 1.0])
    
    cross = np.cross(initial_vec, target_vec)
    cross_len = np.linalg.norm(cross, axis=1)
    
    axes = cross / np.maximum(cross_len, 1e-5)[:, np.newaxis]
    angles = np.arcsin(np.clip(cross_len, -1.0, 1.0))
    
    # Handle dot product < 0
    dot = np.dot(target_vec, initial_vec)
    angles[dot < 0] = np.pi - angles[dot < 0]
    
    # Fallback for perfectly aligned/anti-aligned
    axes[cross_len < 1e-5] = np.array([1.0, 0.0, 0.0])
    
    return axis_angle_matrix(axes, angles)

TARGET_MATRICES = get_target_rotations(pos_matrix)

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

def ease_out(t):
    return 1 - (1 - t)**3

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    t = f / float(FPS)
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.]); ax.set_axis_off(); fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540); ax.set_ylim(-960, 960)

    # 1. TIMELINE & KINEMATIC WAVE OVERRIDE
    T_STRIKE = 4.0
    T_RESO = 14.0 # Time the wave finishes propagating
    wave_speed = 1800.0 / (T_RESO - T_STRIKE)
    
    wave_radius = max(0.0, (t - T_STRIKE) * wave_speed)

    # 2. EVALUATE MATRIX STATE
    # Brownian rotations
    current_angles = initial_phase + (t * rot_speed)
    CHAOS_MATRICES = axis_angle_matrix(rot_axis, current_angles)

    active_polys = []
    active_colors = []

    # Calculate transition status for all pointers radially
    dist_to_core = np.linalg.norm(pos_matrix[:, [0,2]], axis=1)
    
    # 0.0 = Absolute Chaos. 1.0 = Absolute Aligned Meaning.
    # The wave takes 1.5 seconds to fully lock a node after it hits
    time_since_hit = np.maximum(0.0, (t - T_STRIKE) - (dist_to_core / wave_speed))
    lock_prog = np.clip(time_since_hit / 1.5, 0.0, 1.0)
    lock_smooth = ease_out(lock_prog)

    # Blend Matrices (Slerp approximation via vector lerp for computational rigidity)
    # Applying the rotation to the base tetrahedron
    for i in range(N_POINTERS):
        R_chaos = CHAOS_MATRICES[i]
        R_target = TARGET_MATRICES[i]
        
        # O(1) Matrix interpolation
        R_blend = R_chaos * (1.0 - lock_smooth[i]) + R_target * lock_smooth[i]
        
        # Orthogonalize the blended matrix to prevent distortion
        u, _, vh = np.linalg.svd(R_blend)
        R_final = u @ vh
        
        # Translate
        v_transformed = np.dot(PTR_FACES, R_final.T) + pos_matrix[i]
        active_polys.extend(v_transformed)
        
        # Color Interpolation
        c_c = np.array(mcolors.to_rgb(C_NOISE))
        c_m = np.array(mcolors.to_rgb(C_MEANING))
        c_final = c_c * (1.0 - lock_smooth[i]) + c_m * lock_smooth[i]
        active_colors.extend([c_final]*4)

    # Add the Sovereign Monolith
    # Plunges from the sky at T=1.0, slams at T=4.0
    mono_y_offset = max(0.0, 5000.0 * (1.0 - np.clip((t - 1.0) / 3.0, 0.0, 1.0)**3))
    monolith_live = M_MONOLITH_FACES + np.array([0, mono_y_offset, 0])
    
    M_ALL = np.concatenate((np.array(active_polys), monolith_live), axis=0)
    
    c_anchor = np.array(mcolors.to_rgb(C_ANCHOR))
    # Provide colour array matching exactly the SIDES * 2 triangulation
    C_ALL = np.concatenate((np.array(active_colors), np.array([c_anchor] * (SIDES * 2))), axis=0)

    # 3. CINEMATIC OVERWATCH CAMERA
    # Isometric tracking, pushing in slightly as coherence builds
    cam_dist = 2800.0 - np.clip((t - T_STRIKE) / 14.0, 0.0, 1.0) * 800.0
    cam_t = t * 0.15
    cam_x = np.sin(cam_t) * cam_dist
    cam_z = np.cos(cam_t) * cam_dist
    cam_y = 1600.0 

    cam_pos = np.array([cam_x, cam_y, cam_z])
    target_pos = np.array([0, 0, 0]) 
    
    M_view = get_view_matrix(cam_pos, target_pos)
    view_polys = np.einsum('ij,knj->kni', M_view, M_ALL - cam_pos)

    # 4. SOLID LAMBERTIAN SHADING & DEPTH SORT
    centroids_z = np.mean(view_polys[:, :, 2], axis=1)
    
    v_mask = centroids_z > 50.0
    view_polys = view_polys[v_mask]
    C_ALL = C_ALL[v_mask]
    centroids_z = centroids_z[v_mask]

    if len(view_polys) > 0:
        w_polys = M_ALL[v_mask]
        v1_edge = w_polys[:, 1, :] - w_polys[:, 0, :]
        v2_edge = w_polys[:, 2, :] - w_polys[:, 0, :]
        norms = np.cross(v1_edge, v2_edge)
        n_len = np.linalg.norm(norms, axis=1, keepdims=True)
        norms /= np.maximum(n_len, 1e-5)
        
        diff = 0.2 + 0.8 * np.abs(np.dot(norms, LIGHT_DIR))
        
        final_rgba = np.zeros((len(view_polys), 4))
        final_rgba[:, :3] = C_ALL * diff[:, np.newaxis]
        final_rgba[:, 3] = 1.0

        z_safe = np.maximum(view_polys[:, :, 2], 1.0)
        proj_x = 2400.0 * (view_polys[:, :, 0] / z_safe)
        proj_y = 2400.0 * (view_polys[:, :, 1] / z_safe) + 100
        proj_polys = np.stack((proj_x, proj_y), axis=-1)

        sort_idx = np.argsort(centroids_z)[::-1]

        col = PolyCollection(proj_polys[sort_idx], facecolors=final_rgba[sort_idx], edgecolors=C_EDGE, linewidths=0.25, joinstyle='miter', zorder=10)
        ax.add_collection(col)

    # 5. HIGH-DENSITY HUD & TELEMETRY
    ax.add_patch(Rectangle((-540, 750), 1080, 210, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [750, 750], color=C_TEXT, lw=3, zorder=81)

    ax.text(-500, 890, "LG-399 :: THE MEANING TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 840, "[SFI-0.50] REDUCTION OF ENTROPY VIA SOVEREIGN ALIGNMENT", color=C_GUI, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    aligned_pct = (np.sum(lock_smooth) / N_POINTERS) * 100.0

    if t < T_STRIKE:
        c_stat = C_NOISE
        s_text = "STATE 0: ABSOLUTE NOISE. MEANING OMITTED."
    elif aligned_pct < 99.0:
        c_stat = C_MEANING
        s_text = "STATE 1: THE SOVEREIGN STRIKE. COLLAPSING ENTROPY."
    else:
        c_stat = '#00C853' # Jade Success
        s_text = "STATE 2: O(1) CRYSTALLIZATION EXECUTED. MEANING ATTAINED."

    ax.text(-500, -780, f"KINEMATIC PHASE  : {s_text}", color=c_stat, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"STRUCTURAL YIELD : {aligned_pct:05.1f}% FRUSTUM COHERENCE", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"AXIOMATIC TRUTH  : NOISE BECOMES DATA ONLY UPON ORIENTATION", color=C_TEXT, fontsize=12, fontname='monospace', zorder=82)
    
    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-399: ALIGNMENT OF MEANING [CORES: {cpu_cores}]")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=4):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")
    print("Compilation Complete. Entropy successfully eradicated.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
