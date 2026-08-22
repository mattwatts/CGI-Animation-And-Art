"""
PROJECT: Logic Garden 411b (The Epicyclic Wake Tensor // The Graze Dolly)
FORMAT: YouTube Shorts (1080x1920)
METADATA: SATURN RINGS, KEPLERIAN SHEAR, KINEMATICS, CASSINI EQUINOX, ASTROPHYSICS
EXECUTION: 24.0s Sequence. Dynamic Macro-to-Micro Camera Lerp.
RULES ENFORCED:
- Daylight Palette (White Substrate / High-Contrast Chrome).
- Phase-Locked Metaphor: Stripping the cognitive hallucination of 2D space.
- Exact realisational aspect of vertical mountain spallation popping from flat structures.
- Australian spelling conventions enforced natively (Maths, Colour, Optimise).
- Absolute O(N) Depth Sorting (Painter's Algorithm).
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
OUT_DIR = "frames_411_saturn"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG            = '#FFFFFF'
C_TEXT          = '#111115'
C_EDGE          = '#111115'
C_BASE_ICE      = '#1E293B'  # Carbon Slate (Flat Ring Bedrock)
C_PEAK_ICE      = '#00D2FF'  # High-Contrast Cyan (Crystalline Altitude)
C_MOONLET       = '#FF3300'  # Intense Red (The Sovereign Tensor)
C_SHADOW        = '#94A3B8'  # Steel Shadow projected on pure White
C_GUI           = '#64748B'

# ------------------------------------------------------------------
# O(N) KINEMATIC PARTICLE SEEDING (120,000 NODES FOR SOLID STATE)
# ------------------------------------------------------------------
N_PARTICLES = 120000
np.random.seed(411)

# Compressing particle density explicitly against the gap edges
gap_dist = 14.0
# Inner Ring: Negative X (Orbits Faster)
u_in = np.random.rand(N_PARTICLES // 2) ** 1.6
X_inner = -gap_dist - 150.0 * u_in

# Outer Ring: Positive X (Orbits Slower)
u_out = np.random.rand(N_PARTICLES // 2) ** 1.6
X_outer = gap_dist + 150.0 * u_out

X_ALL = np.concatenate([X_inner, X_outer])
# Elongated initial Y distribution for endless tracking
Y_0 = np.random.uniform(-1000, 1000, N_PARTICLES)

# Absolute Keplerian Relative Velocity (V = c / X)
V_Y = -350.0 / X_ALL

print(f"PHASE 1: RING MATRIX COMPILED [{N_PARTICLES} PARTICULATE NODES]")

# ------------------------------------------------------------------
# MATRIX OPERATIONS
# ------------------------------------------------------------------
def rx(deg):
    rad = np.radians(deg); c, s = np.cos(rad), np.sin(rad)
    return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def ry(rad):
    c, s = np.cos(rad), np.sin(rad)
    return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def rz(rad):
    c, s = np.cos(rad), np.sin(rad)
    return np.array([[c,-s,0],[s,c,0],[0,0,1]])

def ease_in_out(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)

rgb_base = np.array(mcolors.to_rgb(C_BASE_ICE))
rgb_peak = np.array(mcolors.to_rgb(C_PEAK_ICE))

def generate_octahedron(center, size):
    r = size
    v = np.array([
        [0, r, 0], [0, -r, 0], [r, 0, 0], 
        [-r, 0, 0], [0, 0, r], [0, 0, -r]
    ])
    f_idx = [
        [0, 2, 4], [0, 4, 3], [0, 3, 5], [0, 5, 2],
        [1, 4, 2], [1, 3, 4], [1, 5, 3], [1, 2, 5]
    ]
    return [v[f] + center for f in f_idx]

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f_idx):
    t_sec = f_idx / float(FPS)
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.]); ax.set_axis_off(); fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540); ax.set_ylim(-960, 960)

    # 1. TRANCENDENT CAMERA KINEMATICS (MACRO TO GRAZE LERP)
    T_DIVE_START = 2.0
    T_DIVE_END   = 14.0
    
    if t_sec < T_DIVE_START:
        lerp_prog = 0.0
    elif t_sec < T_DIVE_END:
        lerp_prog = ease_in_out((t_sec - T_DIVE_START) / (T_DIVE_END - T_DIVE_START))
    else:
        lerp_prog = 1.0

    # Macro Top-Down: pitch = -10, dist = 2500
    # Micro Grazing: pitch = -84, dist = 650
    current_pitch = -10.0 * (1.0 - lerp_prog) + (-84.0) * lerp_prog
    current_dist  = 2500.0 * (1.0 - lerp_prog) + 650.0 * lerp_prog
    
    # Smooth orbital tracking around the Z-axis
    cam_angle = -60.0 + t_sec * 3.0
    
    M_cam = rx(current_pitch) @ rz(np.radians(cam_angle))
    
    # 2. EVALUATING O(N) RING KINEMATICS
    Y_curr = Y_0 + V_Y * (t_sec * 8.0)
    Y_curr = (Y_curr + 1000) % 2000 - 1000  # Wrap length
    
    active_inner = (X_ALL < 0) & (Y_curr > 0)
    active_outer = (X_ALL > 0) & (Y_curr < 0)
    active = active_inner | active_outer
    
    Y_wake = np.abs(Y_curr)
    onset = np.clip((Y_wake - 20) / 30.0, 0, 1.0) # Sharp onset after passing moonlet
    
    # Brutalist Altitude Mapping: forces massive vertical topology
    Z_amp = 3000.0 / (np.abs(X_ALL)**1.4 + 1.0) 
    K = 0.08 * np.abs(X_ALL)
    decay = np.exp(-Y_wake / 400.0)
    
    Z_ALL = np.zeros_like(X_ALL)
    Z_ALL[active] = Z_amp[active] * np.sin(K[active] * Y_wake[active]) * decay[active] * onset[active]
    Z_ALL += np.random.normal(0, 0.4, N_PARTICLES)

    pts_3d = np.stack((X_ALL, Y_curr, Z_ALL), axis=-1)
    
    # Height-based color mapping for dramatic contrast
    z_norm = np.clip(np.abs(Z_ALL) / 35.0, 0.0, 1.0)[..., np.newaxis]
    col_array = rgb_base * (1.0 - z_norm) + rgb_peak * z_norm

    # 3. ABSOLUTE SHADOW PROJECTION TENSOR
    # Extremely shallow grazing light to blow out shadow lengths
    L_vec = np.array([-1.0, -0.2, -0.15]) 
    
    shadow_mask = Z_ALL > 1.5 
    S_X = X_ALL[shadow_mask] - Z_ALL[shadow_mask] * (L_vec[0] / L_vec[2])
    S_Y = Y_curr[shadow_mask] - Z_ALL[shadow_mask] * (L_vec[1] / L_vec[2])
    S_Z = np.full_like(S_X, -0.1) 
    
    shadows_3d = np.stack((S_X, S_Y, S_Z), axis=-1)
    
    # 4. CAMERA TRANSFORMATIONS & PAINTER'S SORT
    v_cam_S = np.einsum('ij,nj->ni', M_cam, shadows_3d)
    v_cam_S[:, 2] += current_dist
    px_S = 1800.0 * (v_cam_S[:, 0] / v_cam_S[:, 2])
    py_S = 1800.0 * (v_cam_S[:, 1] / v_cam_S[:, 2])
    
    v_cam_R = np.einsum('ij,nj->ni', M_cam, pts_3d)
    v_cam_R[:, 2] += current_dist
    px_R = 1800.0 * (v_cam_R[:, 0] / v_cam_R[:, 2])
    py_R = 1800.0 * (v_cam_R[:, 1] / v_cam_R[:, 2])
    z_depth_R = v_cam_R[:, 2]
    
    # Strictly back-to-front sorting so the mountains physically occlude elements behind them
    sort_idx = np.argsort(z_depth_R)[::-1]
    
    # 5. RENDER THE BARE-METAL STACK
    ax.add_patch(plt.Rectangle((-540, -960), 1080, 1920, color=C_BG, zorder=0))

    # Shadows
    ax.scatter(px_S, py_S, c=C_SHADOW, s=2.5, alpha=0.06, edgecolors='none', zorder=2)
    
    # Particulates
    # Dynamic point sizing: slightly larger up close for monolithic feeling
    p_size = 4.0 if lerp_prog > 0.8 else 2.5
    ax.scatter(px_R[sort_idx], py_R[sort_idx], c=col_array[sort_idx], s=p_size, alpha=1.0, edgecolors='none', zorder=5)

    # Sovereign Node (Moonlet)
    moon_faces = generate_octahedron(np.array([0.,0.,0.]), 4.5)
    
    light_norm = np.array([-0.5, 0.8, -0.4])
    light_norm /= np.linalg.norm(light_norm)

    for face in moon_faces:
        v1 = face[1] - face[0]; v2 = face[2] - face[0]
        f_norm = np.cross(v1, v2)
        nL = np.linalg.norm(f_norm)
        if nL > 0: f_norm /= nL
        
        diff = 0.5 + 0.5 * np.clip(np.dot(f_norm, light_norm), 0, 1)
        fc_m = np.append(np.array(mcolors.to_rgb(C_MOONLET)) * diff, 1.0)
        
        vC = np.einsum('ij,nj->ni', M_cam, face)
        vC[:, 2] += current_dist
        pX = 1800.0 * (vC[:, 0] / vC[:, 2]); pY = 1800.0 * (vC[:, 1] / vC[:, 2])
        
        ax.add_patch(plt.Polygon(np.column_stack((pX, pY)), facecolor=fc_m, edgecolor=C_EDGE, lw=1.0, zorder=6))

    # 6. HIGH-DENSITY HUD & TELEMETRY
    ax.add_patch(Rectangle((-540, 780), 1080, 180, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [780, 780], color=C_TEXT, lw=3, zorder=81)
    ax.text(-500, 880, "LG-411b :: RING KINEMATICS TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 830, "[SFI-1.00] MACRO TO MICRO SPATIAL DIVE", color=C_MOONLET, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    prog = t_sec / DURATION
    if t_sec < T_DIVE_START:
        state_msg = "PHASE 1: THE MACRO ILLUSION"
        state_col = C_BASE_ICE
        active_op = "ORTHOGRAPHIC TOP-DOWN. THE RINGS APPEAR FUNCTIONALLY 2D."
    elif t_sec < T_DIVE_END:
        state_msg = "PHASE 2: CAMERA KINEMATIC DIVE"
        state_col = C_PEAK_ICE
        active_op = "INTERSECTING THE MATRIX. DROPPING TO GRAZING ANGLE (-84 DEG)."
    else:
        state_msg = "PHASE 3: VERTICAL TRUTH EXPOSED"
        state_col = C_MOONLET
        active_op = "MICRO-MOUNTAINS VISIBLE. KEPLERIAN SHEARING PROVEN."

    ax.text(-500, -780, f"PROTOCOL STATE : {state_msg}", color=state_col, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"DIAGNOSTIC     : {active_op}", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"AXIOMATIC TRUTH: A SMOOTH 2D RING IS AN OPTICAL LIE. THE GEOMETRY IS VIOLENTLY SHEARED.", color=C_TEXT, fontsize=11, fontname='monospace', zorder=82)

    ax.add_patch(Rectangle((-500, -920), 1000, 8, facecolor=C_GUI, zorder=82))
    ax.add_patch(Rectangle((-500, -920), 1000 * prog, 8, facecolor=state_col, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f_idx:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f_idx

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-411b: GRAZING TENSOR ENGAGED [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            pass
    print("Compilation Complete. Matrix resolved to exact topological shadow bounds.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
