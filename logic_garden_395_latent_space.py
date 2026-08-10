"""
PROJECT: Logic Garden 395 (The Latent Space // Emergent Pareidolia)
FORMAT: YouTube Shorts (1080x1920)
METADATA: AI HALLUCINATION, UNCANNY VALLEY, PAREIDOLIA, GENERATIVE TENSOR
EXECUTION: 24.0s Sequence. True 3D Mathematical Construction.
RULES ENFORCED: 
- Daylight Palette (White Substrate / High Contrast).
- Phase-Locked Metaphor: Mapping AI latent upscaling to pure topological kinematics.
- High-frequency peripheral spallation to simulate algorithmic "boiling."
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
OUT_DIR = "frames_395_latent_space"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG            = '#FFFFFF'  # Daylight / Absolute Void
C_TEXT          = '#111115'
C_STEEL         = '#94A3B8'  # Core Anthropomorphic Substrate
C_MARINE        = '#005599'  # Topological depth shading
C_HALLUCINATION = '#DE008A'  # Deep Magenta (The Generative Boil)
C_GUI           = '#64748B'

LIGHT_DIR = np.array([-0.3, 0.4, -0.8])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

# ------------------------------------------------------------------
# PHASE 1: EXACT PHYSICAL GEOMETRY GENERATION (THE PROT0-JAW)
# ------------------------------------------------------------------
np.random.seed(395)
print("PHASE 1: COMPUTING EMERGENT ANTHROPOMORPHIC MATRIX...")

X_RES, Y_RES = 100, 100
ix_grid = np.linspace(-400, 400, X_RES)
iy_grid = np.linspace(-500, 500, Y_RES)
xx, yy = np.meshgrid(ix_grid, iy_grid)

# Mathematical definition of an Uncanny Humanoid Structure (Gaussian Subtractions)
zz_target = -((xx**2) / 300.0 + (yy**2) / 500.0)

# Ocular Voids (The mathematical "eyes")
zz_target -= 300.0 * np.exp(-((xx - 130)**2 + (yy - 100)**2) / 2000.0)
zz_target -= 300.0 * np.exp(-((xx + 130)**2 + (yy - 100)**2) / 2000.0)

# Nasal Ridge
zz_target += 180.0 * np.exp(-(xx**2 / 800.0 + (yy + 60)**2 / 4000.0))

# Mandible / Cheek Hollows
zz_target -= 150.0 * np.exp(-((xx - 160)**2 + (yy + 180)**2) / 4000.0)
zz_target -= 150.0 * np.exp(-((xx + 160)**2 + (yy + 180)**2) / 4000.0)
zz_target += 120.0 * np.exp(-(xx**2 / 2000.0 + (yy + 280)**2 / 3000.0))

# Peripheral Fade Mask (used to restrict the "Dancing details" to the edge of perception)
radial_dist = np.sqrt(xx**2 + (yy + 50)**2)
edge_mask = np.clip((radial_dist - 180.0) / 250.0, 0.0, 1.0)

# Vectorized Triangulation for O(N) rendering speed
idx = np.arange(X_RES * Y_RES).reshape(Y_RES, X_RES)
p1 = idx[:-1, :-1].flatten(); p2 = idx[:-1, 1:].flatten()
p3 = idx[1:, :-1].flatten(); p4 = idx[1:, 1:].flatten()

v_target = np.column_stack((xx.flatten(), yy.flatten(), zz_target.flatten()))

# Initiate the Latent Space as a fully chaotic noise volumetric array
v_chaos = np.column_stack((
    np.random.uniform(-1800, 1800, X_RES * Y_RES),
    np.random.uniform(-1800, 1800, X_RES * Y_RES),
    np.random.uniform(-6000, 500, X_RES * Y_RES)
))

# ------------------------------------------------------------------
# TRUE MATRICES & KINEMATIC PROJECTION
# ------------------------------------------------------------------
def rx(deg):
    r = np.radians(deg); c, s = np.cos(r), np.sin(r)
    return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def ry(deg):
    r = np.radians(deg); c, s = np.cos(r), np.sin(r)
    return np.array([[c,0,s],[0,1,0],[-s,0,c]])

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
    return 4 * t**3 if t < 0.5 else 1 - (-2 * t + 2)**3 / 2

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    t = f / float(FPS)

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.]); ax.set_axis_off(); fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540); ax.set_ylim(-960, 960)

    # 1. EVALUATE EMERGENT TIMELINE
    # Phase 1: Fractal Dive (0-4s)
    # Phase 2: Algorithmic Resolution / Convergence (4-10s)
    # Phase 3: The Edge of Perception / The Dancing Detail (10-18s)
    # Phase 4: Resolution Lock (18-24s)
    
    prog_converge = np.clip((t - 4.0) / 6.0, 0.0, 1.0)
    prog_converge = ease_in_out(prog_converge)
    
    prog_hallucination = np.clip((t - 10.0) / 3.0, 0.0, 1.0) - np.clip((t - 18.0) / 3.0, 0.0, 1.0)
    
    # 2. GENERATE LATENT MATHEMATICS
    current_verts = v_chaos * (1.0 - prog_converge) + v_target * prog_converge
    
    # Apply "The Dancing Detail" (Fractal Sinusoidal Jitter driven by algorithmic instability)
    # Only applies radially around the "edge of perception" mask.
    if prog_hallucination > 0.001:
        mask_mult = edge_mask.flatten() * prog_hallucination
        
        # High-frequency boiling noise
        noise_x = np.sin(current_verts[:, 1] * 0.15 + t * 24.0) * 120.0
        noise_y = np.cos(current_verts[:, 0] * 0.15 - t * 20.0) * 120.0
        noise_z = np.sin((current_verts[:, 0] + current_verts[:, 1]) * 0.1 + t * 30.0) * 200.0
        
        current_verts[:, 0] += noise_x * mask_mult
        current_verts[:, 1] += noise_y * mask_mult
        current_verts[:, 2] += noise_z * mask_mult

    # Build the strict 3D Array
    tri1 = np.stack((current_verts[p1], current_verts[p2], current_verts[p3]), axis=1)
    tri2 = np.stack((current_verts[p4], current_verts[p3], current_verts[p2]), axis=1)
    M_ALL = np.concatenate((tri1, tri2), axis=0)

    # Calculate parametric face-mask colors based on the edge topology
    # Center forms solid Steel/Marine. Edges boil into Deep Magenta when hallucinating.
    mask_tri1 = edge_mask.flatten()[p1]
    mask_tri2 = edge_mask.flatten()[p4]
    edge_scale = np.concatenate((mask_tri1, mask_tri2), axis=0)
    
    c_core_rgb = np.array(mcolors.to_rgb(C_STEEL))
    c_void_rgb = np.array(mcolors.to_rgb(C_MARINE))
    c_halluc_rgb = np.array(mcolors.to_rgb(C_HALLUCINATION))
    
    # 3. KINEMATIC CAMERA (The Fractal Zoom Trace)
    # During the chaotic phase, camera dives sharply down the Z axis.
    cam_z_start = 5000.0
    cam_z_end = 2200.0
    cam_z = cam_z_start - (cam_z_start - cam_z_end) * ease_in_out(np.clip(t / 8.0, 0.0, 1.0))
    
    # Slight uncanny bobbing to simulate the instability of biological fixation
    cam_x = np.sin(t * 0.6) * 150.0
    cam_y = np.cos(t * 0.8) * 100.0 

    cam_pos = np.array([cam_x, cam_y, cam_z])
    target_pos = np.array([0, -100, -800]) 
    
    M_view = get_view_matrix(cam_pos, target_pos)
    view_polys = np.einsum('ij,knj->kni', M_view, M_ALL - cam_pos)

    # 4. SOLID LAMBERTIAN SHADING & DEPTH SORT
    centroids_z = np.mean(view_polys[:, :, 2], axis=1)

    v_mask = centroids_z > 50.0
    view_polys = view_polys[v_mask]
    edge_scale_culled = edge_scale[v_mask]
    centroids_z = centroids_z[v_mask]

    if len(view_polys) > 0:
        w_polys = M_ALL[v_mask]
        v1 = w_polys[:, 1, :] - w_polys[:, 0, :]
        v2 = w_polys[:, 2, :] - w_polys[:, 0, :]
        norms = np.cross(v1, v2)
        n_len = np.linalg.norm(norms, axis=1, keepdims=True)
        norms /= np.maximum(n_len, 1e-5)
        
        # Absolute directional shading highlights structural cheekbones and orbital cavities
        diff = 0.2 + 0.8 * np.abs(np.dot(norms, LIGHT_DIR))
        
        final_rgba = np.zeros((len(view_polys), 4))
        
        for i in range(len(view_polys)):
            # interpolate color from core (steel) to edge (marine)
            base_col = c_core_rgb * (1.0 - edge_scale_culled[i]) + c_void_rgb * edge_scale_culled[i]
            
            # Inject Magenta hallucination strictly into the noisy edges based on timeline
            if prog_hallucination > 0.0:
                h_shift = edge_scale_culled[i] * prog_hallucination
                base_col = base_col * (1.0 - h_shift) + c_halluc_rgb * h_shift
                
            final_rgba[i, :3] = base_col * diff[i]
            
        final_rgba[:, 3] = 1.0

        z_safe = np.maximum(view_polys[:, :, 2], 1.0)
        proj_x = 2200.0 * (view_polys[:, :, 0] / z_safe)
        proj_y = 2200.0 * (view_polys[:, :, 1] / z_safe) + 150
        proj_polys = np.stack((proj_x, proj_y), axis=-1)

        sort_idx = np.argsort(centroids_z)[::-1]
        
        # Brutalist rendering rules. Heavy dark edges map the shifting matrix explicitly.
        col = PolyCollection(proj_polys[sort_idx], facecolors=final_rgba[sort_idx], edgecolors=C_TEXT, linewidths=0.3, zorder=10)
        ax.add_collection(col)

    # 5. HIGH-DENSITY HUD & TELEMETRY
    ax.add_patch(Rectangle((-540, 750), 1080, 210, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [750, 750], color=C_TEXT, lw=3, zorder=81)

    ax.text(-500, 890, "LG-395 :: THE LATENT SPACE PROTOCOL", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 840, "[SFI-0.50] ALGORITHMIC PAREIDOLIA / EMERGENT ANTHROPOMORPHISM", color=C_GUI, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    if t < 4.0:
        c_stat = C_MARINE; s_text = "FRACTAL DIVE: SCANNING CHAOTIC NOISE SET"
    elif t < 10.0:
        c_stat = C_STEEL; s_text = "GRADIENT DESCENT: FORCING ANTHROPOMORPHIC FIT"
    elif t < 18.0:
        c_stat = C_HALLUCINATION; s_text = "ERROR: HIGH-FREQUENCY LATENT HALLUCINATION"
    else:
        c_stat = C_TEXT; s_text = "RESOLUTION: ABSOLUTE UNCANNY TOPOLOGY SECURED"

    h_intensity = prog_hallucination * 100.0

    ax.text(-500, -780, f"NETWORK STATE          : {s_text}", color=c_stat, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"EDGE INSTABILITY INDEX : {h_intensity:05.1f}% STRUCTURAL VARIANCE", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"TOPOLOGICAL ARRAY      : {len(view_polys):06d} ACTIVE POLYGONS MAPPED", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    
    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-395: THE LATENT SPACE TENSOR [CORES: {cpu_cores}]")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=4):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")
    print("Compilation Complete. Substrate Pareidolia Extracted.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
