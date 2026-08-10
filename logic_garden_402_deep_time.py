"""
PROJECT: Logic Garden 402 (Deep Time // Bi-Directional Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: DEEP TIME, KINEMATIC DISPERSION, THERMODYNAMICS, ONTOLOGY
EXECUTION: 24.0s Sequence. True 3D Mathematical Construction.
RULES ENFORCED:
- Daylight Palette (White Substrate / High Contrast Core).
- Phase-Locked Metaphor: Time does not end, human conception merely disperses.
- True Line-of-Sight Painter's Algorithm with Alpha Blending.
- Australian spelling conventions enforced natively (Maths, Optimisation).
- Exact realisational aspect of machined blocks spanning an infinite Z-axis.
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
OUT_DIR = "frames_402_deep_time"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG            = '#FFFFFF'  # The Infinite Void
C_TEXT          = '#111115'
C_EDGE          = '#111115'  # Present Moment Hard Lines
C_PRESENT       = '#111115'  # Indestructible Black (Z=0)
C_PAST          = '#005599'  # Deep Marine (-Z)
C_FUTURE        = '#FFB300'  # Dense Amber (+Z)
C_GUI           = '#64748B'

LIGHT_DIR = np.array([-0.6, 0.8, -0.4])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

# ------------------------------------------------------------------
# O(N) BASE GEOMETRY PRE-COMPUTATION
# ------------------------------------------------------------------
np.random.seed(402)
print("PHASE 1: SYNTHESIZING DEEP TIME AXIS...")

BLOCK_SIZE = 40.0
Z_MAX = 7000.0

def get_base_cube():
    sz = BLOCK_SIZE / 2.0
    v = np.array([
        [-sz, -sz, -sz], [ sz, -sz, -sz], [ sz,  sz, -sz], [-sz,  sz, -sz],
        [-sz, -sz,  sz], [ sz, -sz,  sz], [ sz,  sz,  sz], [-sz,  sz,  sz]
    ])
    faces = [
        [v[0], v[1], v[2], v[3]], [v[4], v[5], v[6], v[7]],
        [v[0], v[1], v[5], v[4]], [v[2], v[3], v[7], v[6]],
        [v[1], v[2], v[6], v[5]], [v[3], v[0], v[4], v[7]]
    ]
    # Triangulate for absolute Matrix rigidity
    tris = []
    for f in faces:
        tris.append([f[0], f[1], f[2]]); tris.append([f[0], f[2], f[3]])
    return np.array(tris)

BASE_CUBE = get_base_cube()

# Generate the Infinite Tube
N_Z_RINGS = 350
N_THETA = 12

blocks = []

for z in np.linspace(-Z_MAX, Z_MAX, N_Z_RINGS):
    # Fuzziness Tensor: Conception loses coherence exponentially at range
    fuzz_ratio = min(abs(z) / (Z_MAX - 1000), 1.0)
    fuzz = fuzz_ratio ** 2.5
    
    alpha = np.clip(1.0 - fuzz_ratio**1.5, 0.0, 1.0)
    if alpha < 0.02: continue # Plunges below Observational Horizon
    
    # Colour Determination
    if z < -150:
        c_target = np.array(mcolors.to_rgb(C_PAST))
    elif z > 150:
        c_target = np.array(mcolors.to_rgb(C_FUTURE))
    else:
        c_target = np.array(mcolors.to_rgb(C_PRESENT))
        
    blend = min(1.0, abs(z)/1000.0)
    c_final = c_target * blend + np.array(mcolors.to_rgb(C_PRESENT)) * (1.0 - blend)
    
    for t_idx in range(N_THETA):
        theta = (t_idx / N_THETA) * 2 * np.pi + (z * 0.001) # Architectural twist
        
        # Absolute exact structure at Z=0. Severe structural decoherence at extremes.
        r = 600.0 + np.random.normal(0, 1500 * fuzz)
        cx = r * np.cos(theta) + np.random.normal(0, 2000 * fuzz)
        cy = r * np.sin(theta) + np.random.normal(0, 2000 * fuzz)
        cz = z + np.random.normal(0, 800 * fuzz)
        
        # Random Rotation applied based on fuzzy metric
        rx = np.random.uniform(0, 2*np.pi) * fuzz
        ry = np.random.uniform(0, 2*np.pi) * fuzz
        rz = np.random.uniform(0, 2*np.pi) * fuzz
        
        blocks.append({
            'pos': np.array([cx, cy, cz]),
            'rot': np.array([rx, ry, rz]),
            'color': c_final,
            'alpha': alpha,
            'z_base': z # For tracking
        })

print(f"COMPILED: {len(blocks)} Structural Epochs inside the Bounding Box.")

# ------------------------------------------------------------------
# KINEMATIC MATH ENGINES
# ------------------------------------------------------------------
def get_R(rx, ry, rz):
    cx, sx = np.cos(rx), np.sin(rx)
    cy, sy = np.cos(ry), np.sin(ry)
    cz, sz = np.cos(rz), np.sin(rz)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cx, 0], [0, 0, 1]])
    return Rz @ Ry @ Rx

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
    return 1 - (1 - t)**3

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f_idx):
    t = f_idx / float(FPS)
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.]); ax.set_axis_off(); fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540); ax.set_ylim(-960, 960)

    # 1. CINEMATIC TIMELINE (MACROSCOPIC PULL)
    prog = np.clip(t / DURATION, 0.0, 1.0)
    
    # Global structure slowly revolves
    global_rz = t * 0.15
    R_sys = get_R(0, 0, global_rz)

    if t < 4.0:
        # Looking straight down the barrel at the perfect Present 
        cam_pos = np.array([0.0, 0.0, -1800.0])
        target_pos = np.array([0.0, 0.0, 0.0])
    elif t < 16.0:
        # Magnificent sweeping pull-back sideways to reveal the infinite scale
        sub_p = ease_in_out((t - 4.0) / 12.0)
        c_x = sub_p * 4500.0
        c_y = sub_p * 2500.0
        c_z = -1800.0 + (sub_p * 1800.0)
        cam_pos = np.array([c_x, c_y, c_z])
        target_pos = np.array([0.0, 0.0, 0.0])
    else:
        # Gliding along the X-axis tracking across the deep timeline
        sub_p = ease_in_out((t - 16.0) / 8.0)
        cam_pos = np.array([4500.0 - (sub_p * 1000.0), 2500.0, 0.0])
        # Look from past towards the future
        target_pos = np.array([0.0, 0.0, -1500.0 + (sub_p * 3000.0)])
    
    M_view = get_view_matrix(cam_pos, target_pos)

    # 2. EVALUATE MATRIX STATE
    render_queue = []
    
    for b in blocks:
        # Cull blocks that are totally faded
        if b['alpha'] < 0.05: continue
            
        R_local = get_R(b['rot'][0], b['rot'][1], b['rot'][2])
        v_world = np.dot(BASE_CUBE, R_local.T) + b['pos']
        v_world = np.dot(v_world, R_sys.T)
        
        # Coordinate Space 
        v_cam = np.einsum('ij,knj->kni', M_view, v_world - cam_pos)
        
        # Depth Centroid
        centroids_z = np.mean(v_cam[:, :, 2], axis=1)
        mask = centroids_z > 50.0
        
        if np.any(mask):
            v_cam = v_cam[mask]
            
            # Shading & Normal evaluation
            v1_edge = v_cam[:, 1, :] - v_cam[:, 0, :]
            v2_edge = v_cam[:, 2, :] - v_cam[:, 0, :]
            norms = np.cross(v1_edge, v2_edge)
            n_len = np.linalg.norm(norms, axis=1, keepdims=True)
            norms /= np.maximum(n_len, 1e-5)
            
            diff = 0.3 + 0.7 * np.abs(np.dot(norms, LIGHT_DIR))
            
            c_rgb = np.zeros(4)
            c_rgb[:3] = b['color']
            c_rgb[3] = b['alpha']
            
            for i in range(len(v_cam)):
                poly_pts = v_cam[i]
                z_safe = np.maximum(poly_pts[:, 2], 1.0)
                px = 2500.0 * (poly_pts[:, 0] / z_safe)
                py = 2500.0 * (poly_pts[:, 1] / z_safe) + 50
                
                final_c = c_rgb.copy()
                final_c[:3] *= diff[i]
                
                # Dynamic Edges: Core holds thick black lines, ends dissolve beautifully.
                edge_c = C_PRESENT if (abs(b['z_base']) < 1500) else 'none'
                lw = 1.0 if (abs(b['z_base']) < 1500) else 0.0

                render_queue.append({
                    'sort': centroids_z[mask][i],
                    'poly': np.stack((px, py), axis=-1),
                    'fc': final_c,
                    'ec': edge_c,
                    'lw': lw
                })

    # O(1) Painter's Sort
    render_queue.sort(key=lambda x: x['sort'], reverse=True)
    
    if len(render_queue) > 0:
        polys = [q['poly'] for q in render_queue]
        fcs = [q['fc'] for q in render_queue]
        ecs = [q['ec'] for q in render_queue]
        lws = [q['lw'] for q in render_queue]
        
        col = PolyCollection(polys, facecolors=fcs, edgecolors=ecs, linewidths=lws, joinstyle='round', zorder=10)
        ax.add_collection(col)

    # 3. HIGH-DENSITY HUD & TELEMETRY
    ax.add_patch(Rectangle((-540, 750), 1080, 210, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [750, 750], color=C_TEXT, lw=3, zorder=81)
    ax.text(-500, 890, "LG-402 :: DEEP TIME KINEMATICS", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 840, "[SFI-0.75] THEORETICAL BOUND // THE ILLUSION OF HEAT DEATH", color=C_GUI, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    ax.text(-500, -780, f"OBSERVATION VECTOR: DEEP PAST TO DEEP FUTURE", color=C_PAST, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"STRUCTURAL MATRIX : THE PRESENT MOMENT (Z=0) IS ABSOLUTE", color=C_PRESENT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"AXIOMATIC TRUTH   : TIME POSSESSES NO TERMINAL BOUNDARIES.", color=C_GUI, fontsize=12, fontname='monospace', zorder=82)
    
    out_path = os.path.join(OUT_DIR, f"frame_{f_idx:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f_idx

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-402: DEEP TIME DISPERSION MATRIX [CORES: {cpu_cores}]")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")
    print("Compilation Complete. The continuum extends without constraint.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
