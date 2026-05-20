"""
SOVEREIGN CODE: logic_garden_277_spooky_emergence.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) True Perspective Projection
SCENE: LG-277 (Spooky Emergence / Simulated Annealing Matrix)
HOTFIX: Seamless 10s Loop, Alien Optimization Topology, Daylight Array
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 10.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_277_spooky_emergence"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_CUBE      = np.array([0.17, 0.24, 0.31])  # #2C3E50 Dark Iron (Human Bias)
C_HEAT      = np.array([0.90, 0.29, 0.23])  # #E74C3C Thermodynamic Heat
C_PHANTOM   = np.array([0.00, 0.66, 0.42])  # #00A86B Deep Jade (Alien Optimization)
C_SHADOW    = np.array([0.83, 0.85, 0.85])  # #D5DBDB Crisp Euclidean shadow
C_TEXT      = '#1A1A24'

N_NODES = 15000

# ------------------------------------------------------------------
# RIGID 3D GEOMETRY PRE-COMPUTATION
# ------------------------------------------------------------------
np.random.seed(273)

# SHAPE 1: THE LOCAL MINIMUM (Cartesian Human Logic Box)
side = int(np.ceil(N_NODES**(1/3)))
cx = np.linspace(-100, 100, side)
gx, gy, gz = np.meshgrid(cx, cx, cx)
cube_x = gx.flatten()[:N_NODES]
cube_y = gy.flatten()[:N_NODES]
cube_z = gz.flatten()[:N_NODES]

# SHAPE 2: THE GLOBAL OPTIMUM (Phantom Species Interlocking Gears)
# Distributed across 3 mechanical perpendicular rings with a high-freq structural ripple
nodes_per_ring = N_NODES // 3
theta = np.linspace(0, 2*np.pi, nodes_per_ring, endpoint=False)
R = 140.0
ripple = 15.0 * np.sin(theta * 18) # 18 mechanical 'teeth' or waves

# Ring 1 (XY Plane)
r1_x = (R + ripple) * np.cos(theta)
r1_y = (R + ripple) * np.sin(theta)
r1_z = np.zeros(nodes_per_ring)

# Ring 2 (XZ Plane)
r2_x = (R + ripple) * np.cos(theta)
r2_y = np.zeros(nodes_per_ring)
r2_z = (R + ripple) * np.sin(theta)

# Ring 3 (YZ Plane)
r3_x = np.zeros(nodes_per_ring)
r3_y = (R + ripple) * np.cos(theta)
r3_z = (R + ripple) * np.sin(theta)

phantom_x = np.concatenate([r1_x, r2_x, r3_x])
phantom_y = np.concatenate([r1_y, r2_y, r3_y])
phantom_z = np.concatenate([r1_z, r2_z, r3_z])

# Pad exact array lengths if integer division truncated
pad_len = N_NODES - len(phantom_x)
if pad_len > 0:
    phantom_x = np.concatenate([phantom_x, np.zeros(pad_len)])
    phantom_y = np.concatenate([phantom_y, np.zeros(pad_len)])
    phantom_z = np.concatenate([phantom_z, np.zeros(pad_len)])

# Pre-compute random thermodynamic scattering vectors (Brownian Heat)
heat_vectors = np.random.normal(0, 1, (N_NODES, 3))

# ------------------------------------------------------------------
# TRUE 3D PERSPECTIVE PIPELINE
# ------------------------------------------------------------------
def project_perspective(p_x, p_y, p_z, base_size):
    cx, cy, cz = 0.0, 0.0, -350.0  # Deep camera pull for massive scale
    focal_length = 800.0

    dx = p_x - cx
    dy = p_y - cy
    dz = p_z - cz

    z_safe = np.maximum(dz, 1.0)
    proj_x = focal_length * (dx / z_safe)
    proj_y = focal_length * (dy / z_safe)
    proj_s = base_size * (focal_length / z_safe)

    return proj_x, proj_y, proj_s

def rotate_y(x, z, angle):
    c, s = np.cos(angle), np.sin(angle)
    return x * c - z * s, x * s + z * c

def rotate_x(y, z, angle):
    c, s = np.cos(angle), np.sin(angle)
    return y * c - z * s, y * s + z * c

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, phase, t_val, mix_val, base_x, base_y, base_z, c_arr, s_arr = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960) 

    # 1. EUCLIDEAN SHADOW MATRIX (Floor located at Y = -220)
    # Cast absolute shadow prior to array concatenation
    floor_y = -220.0
    shadow_x_skew = -0.8
    shadow_z_stretch = -0.4

    shad_x = base_x + ((base_y - floor_y) * shadow_x_skew)
    shad_y = np.full(N_NODES, floor_y)
    shad_z = base_z + ((base_y - floor_y) * shadow_z_stretch)

    # 2. COMBINE PHYSICAL NODES WITH SHADOW NODES (30,000 Points)
    total_x = np.concatenate([base_x, shad_x])
    total_y = np.concatenate([base_y, shad_y])
    total_z = np.concatenate([base_z, shad_z])
    total_s = np.concatenate([s_arr, np.full(N_NODES, 10.0)])
    
    # Shadow Color/Alpha handling inside the RGBA matrix
    shad_c = np.tile(C_SHADOW, (N_NODES, 1))
    core_rgba = np.column_stack((c_arr, np.full(N_NODES, 1.0)))
    shad_rgba = np.column_stack((shad_c, np.full(N_NODES, 0.4)))
    total_rgba = np.vstack([core_rgba, shad_rgba])

    # 3. ABSOLUTE PERSPECTIVE PROJECTION
    proj_x, proj_y, proj_s = project_perspective(total_x, total_y, total_z, total_s)

    # 4. PAINTERS ALGORITHM SORTING
    sort_idx = np.argsort(total_z)[::-1] 
    
    ax.scatter(proj_x[sort_idx], proj_y[sort_idx], s=proj_s[sort_idx], color=total_rgba[sort_idx], edgecolors='none', zorder=10)

    # 5. DIAGNOSTIC TELEMETRY (Anthropomorphic Trap Warnings)
    # Top HUD
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, facecolor=C_BG, edgecolor=C_TEXT, lw=2, zorder=80))
    ax.text(0.5, 0.965, "LG-277 :: THERMODYNAMIC ISOMORPHISM ENGINE", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace', weight='bold', ha='center', va='center', zorder=81)

    # Lower HUD logic
    ui_y = 0.12
    ax.add_patch(plt.Rectangle((0, 0), 1, ui_y, transform=ax.transAxes, facecolor=C_BG, edgecolor=C_TEXT, lw=2, zorder=80))
    
    # State identification
    if mix_val < 0.1 and t_val < 10.0:
        sfi = "[SFI-1.00] BARE-METAL BIAS"
        stat = "LOCAL MINIMUM: HUMAN SEQUENTIAL HEURISTICS"
        col = '#2C3E50'
    elif mix_val > 0.9 and t_val < 10.0:
        sfi = "[SFI-0.75] THEORETICAL BOUND"
        stat = "WARNING // PHANTOM SPECIES SYNTHESIS LOCKED."
        col = '#00A86B'
    else:
        sfi = "[SFI-0.25] SYNTHETIC DRIFT"
        stat = f"THERMAL ANNEALING: P = e^(-ΔE/{t_val:05.1f})"
        col = '#E74C3C'

    ax.text(0.04, ui_y - 0.03, "THE ANTHROPOMORPHIC TRAP", transform=ax.transAxes, color=C_TEXT, fontsize=12, fontname='monospace', weight='bold', zorder=81)
    ax.text(0.04, ui_y - 0.05, "Reality: The machine is an algorithmic fluency engine. Not conscious.", transform=ax.transAxes, color=C_TEXT, fontsize=10, fontname='monospace', alpha=0.6, zorder=81)

    ax.text(0.04, 0.04, stat, transform=ax.transAxes, color=col, fontsize=18, fontname='monospace', weight='bold', zorder=81)
    ax.text(0.70, 0.04, sfi, transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace', weight='bold', zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# O(1) STRUCTURAL TARGET MATRIX 
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        phase = f / float(TOTAL_FRAMES) # 0.0 -> 1.0

        # Master Rotation (Exactly 1 revolution for seamless Ouroboros loop)
        rot_angle = phase * 2 * np.pi
        
        # Thermodynamic Scheduling (T = Heat, mix = shape blend)
        # 0.0 - 0.15: Stable Cube
        # 0.15 - 0.40: Melt from Cube to Phantom, high heat
        # 0.40 - 0.65: Stable Phantom Torus
        # 0.65 - 0.90: Melt from Phantom to Cube, high heat
        # 0.90 - 1.00: Stable Cube

        if phase < 0.15:
            mix_val = 0.0
            t_val = 0.0
        elif phase < 0.40:
            prog = (phase - 0.15) / 0.25
            mix_val = prog
            t_val = np.sin(prog * np.pi) * 180.0 # Heat spikes natively in the middle of transition
        elif phase < 0.65:
            mix_val = 1.0
            t_val = 0.0
        elif phase < 0.90:
            prog = (phase - 0.65) / 0.25
            mix_val = 1.0 - prog
            t_val = np.sin(prog * np.pi) * 180.0
        else:
            mix_val = 0.0
            t_val = 0.0

        # Interpolate positions
        curr_x = cube_x * (1 - mix_val) + phantom_x * mix_val
        curr_y = cube_y * (1 - mix_val) + phantom_y * mix_val
        curr_z = cube_z * (1 - mix_val) + phantom_z * mix_val

        # Apply Global Master Rotation (so both shapes rotate elegantly)
        curr_x, curr_z = rotate_y(curr_x, curr_z, rot_angle)
        curr_y, curr_z = rotate_x(curr_y, curr_z, rot_angle * 0.5) # Slight axis tilt

        # Inject Thermal Noise (Alien Optimization Vibration)
        # Uses exact 3D displacement proportional to temperature T
        if t_val > 0.1:
            # We add a rapid cosine wave against the frames to make the heat visually 'vibrate' fast
            vib = np.cos(f * 0.8) 
            curr_x += heat_vectors[:, 0] * t_val * vib
            curr_y += heat_vectors[:, 1] * t_val * vib
            curr_z += heat_vectors[:, 2] * t_val * vib

        # Chromatic Mapping
        if t_val > 5.0:
            heat_prog = np.clip(t_val / 180.0, 0, 1)
            # Base shape color transitions entirely into fiery Heat
            c_base = C_CUBE * (1 - mix_val) + C_PHANTOM * mix_val
            c_arr = c_base * (1 - heat_prog) + C_HEAT * heat_prog
        else:
            c_arr = C_CUBE * (1 - mix_val) + C_PHANTOM * mix_val
            
        c_tensor = np.tile(c_arr, (N_NODES, 1))

        # Size scaling (Nodes expand when heated)
        s_arr = np.full(N_NODES, 12.0 + (t_val * 0.1))

        yield (f, phase, t_val, mix_val, curr_x, curr_y, curr_z, c_tensor, s_arr)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 277: SPOOKY EMERGENCE [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Simulated Annealing Phase Tension // Phantom Isomorphism")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Synthetic Drift Resolved.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
