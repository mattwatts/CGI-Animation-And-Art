"""
SOVEREIGN CODE: logic_garden_36b_wormhole.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Pre-Compiled Cartesian Matrix
SCENE: LG-36b (The Einstein-Rosen Bridge / Seamless Loop Tensor)
HOTFIX: Perfect 10s Orbit, Pre-calculated Facecolors, Double Geodesic Drop
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 10.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_36b_wormhole"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DEEP SPACE PALETTE --------
C_BG        = '#020205'       # Absolute Void Substrate
C_UPPER     = '#00FFFF'       # Cyan (Positive Space)
C_LOWER     = '#FF00FF'       # Magenta (Negative Space)
C_THROAT    = '#FFFFFF'       # Singularity Event Horizon
C_TRAVELER  = '#FFD700'       # Gold Kinematic Mass
C_GRID      = '#404040'       # Geometric Topology Lines

def hex_to_rgba(h, a=1.0):
    h = h.lstrip('#')
    return [int(h[0:2],16)/255.0, int(h[2:4],16)/255.0, int(h[4:6],16)/255.0, a]

color_upper = hex_to_rgba(C_UPPER, 0.4)
color_lower = hex_to_rgba(C_LOWER, 0.4)
color_throat = hex_to_rgba(C_THROAT, 0.8)

# ------------------------------------------------------------------
# O(1) METRIC PRE-COMPILATION (THE EINSTEIN-ROSEN MANIFOLD)
# ------------------------------------------------------------------
print("LG-36b: PRE-COMPILING EXACT SPACETIME METRICS...")
THROAT_RADIUS = 0.8  # Stable, permanently open bridge
U_MAX = 3.0

u_arr = np.linspace(-U_MAX, U_MAX, 45) # Z-axis height
v_arr = np.linspace(0, 2*np.pi, 65)    # Radial angle
U, V = np.meshgrid(u_arr, v_arr)

# The intrinsic metric: r depends on z-axis (u)
R_matrix = np.sqrt(U**2 + THROAT_RADIUS**2)

X_matrix = R_matrix * np.cos(V)
Y_matrix = R_matrix * np.sin(V)
Z_matrix = U

# Pre-compile the color topography to prevent O(N) ram bloat per frame
colors_matrix = np.zeros(Z_matrix.shape + (4,))
for i in range(Z_matrix.shape[0]):
    for j in range(Z_matrix.shape[1]):
        z_val = Z_matrix[i, j]
        if z_val > 0.2:
            colors_matrix[i, j] = color_upper
        elif z_val < -0.2:
            colors_matrix[i, j] = color_lower
        else:
            colors_matrix[i, j] = color_throat

# Pre-compile the Throat Ring mathematical highlight
theta_ring = np.linspace(0, 2*np.pi, 120)
rx_ring = THROAT_RADIUS * np.cos(theta_ring)
ry_ring = THROAT_RADIUS * np.sin(theta_ring)
rz_ring = np.zeros_like(theta_ring)

# ------------------------------------------------------------------
# MULTICORE RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    tau = float(f) / float(TOTAL_FRAMES)

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    fig.patch.set_facecolor(C_BG)
    
    # 3D Axes setup
    ax = fig.add_axes([0, 0, 1, 1], projection='3d')
    ax.set_facecolor(C_BG)
    ax.set_axis_off()

    ax.set_xlim(-U_MAX, U_MAX)
    ax.set_ylim(-U_MAX, U_MAX)
    ax.set_zlim(-U_MAX, U_MAX)

    # Clean axes panels
    try:
        ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    except: pass
    ax.grid(False)

    # 1. ORBITAL KINEMATICS
    # Exact 360 degree azimuthal sweep for seamless Ouroboros loop
    cam_azim = tau * 360.0
    cam_elev = 22.0 + np.sin(tau * 2 * np.pi) * 4.0 # Subtle breathable pitch
    ax.view_init(elev=cam_elev, azim=cam_azim)

    # 2. RENDER STABLE MANIFOLD
    # shade=False forces raw logic colours. Edgecolors applied rigidly post-process.
    surf = ax.plot_surface(X_matrix, Y_matrix, Z_matrix, facecolors=colors_matrix, 
                           rstride=1, cstride=1, linewidth=0.6, shade=False, zorder=1)
    surf.set_edgecolor(C_GRID)

    # The Singularity Ring
    ax.plot(rx_ring, ry_ring, rz_ring, color=C_THROAT, linewidth=3.5, zorder=2)

    # 3. THE GEODESIC TRAVELLER
    # 2 drops per 10-second loop
    drop_phase = (tau * 2.0) % 1.0
    
    # Plunges from +3.0 to -3.0
    t_z = U_MAX - (drop_phase * (U_MAX * 2.0))
    t_r = np.sqrt(t_z**2 + THROAT_RADIUS**2)
    # Locked to the zero-angle track of the geometric grid
    t_theta = 0.0 

    px = t_r * np.cos(t_theta)
    py = t_r * np.sin(t_theta)
    pz = t_z

    ax.scatter([px], [py], [pz], c=C_TRAVELER, s=250, edgecolors=C_BG, linewidth=2, zorder=10)

    # Plasma Wake / Velocity Trace
    num_trail = 15
    trail_z = np.linspace(t_z + 1.2, t_z, num_trail) # Trailing behind
    # Suppress trailing array out of bounds
    trail_z = np.clip(trail_z, -U_MAX, U_MAX)
    trail_r = np.sqrt(trail_z**2 + THROAT_RADIUS**2)
    tx = trail_r * np.cos(t_theta)
    ty = trail_r * np.sin(t_theta)
    ax.plot(tx, ty, trail_z, color=C_TRAVELER, linewidth=3, alpha=0.8, zorder=9)

    # 4. EXPLICIT 2D HUD OVERLAYS
    # Translate math telemetry to flat screen coordinates via text2D
    hud_bg = dict(facecolor=C_BG, edgecolor=C_GRID, lw=2, alpha=0.8)
    ax.text2D(0.05, 0.95, f"LG-36b: EINSTEIN-ROSEN BRIDGE TENSOR", transform=ax.transAxes, color=C_UPPER, fontfamily='monospace', weight='bold', fontsize=18, bbox=hud_bg)
    ax.text2D(0.05, 0.91, f"METRIC: SCHWARZSCHILD // [SFI-1.00]", transform=ax.transAxes, color=C_LOWER, fontfamily='monospace', weight='bold', fontsize=14, bbox=hud_bg)
    
    status_str = "STATUS: TRANSIT ACTIVE"
    ax.text2D(0.05, 0.05, f"THROAT R: {THROAT_RADIUS:.2f}\nZ-VECTOR: {t_z:+.2f}\n{status_str}", transform=ax.transAxes, color=C_UPPER, fontfamily='monospace', weight='bold', fontsize=16, bbox=hud_bg)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"EXECUTING 3D VECTORISED RENDERING [CORES: {cpu_cores}]")
    print("Pre-calculated Topological Array limits Python RAM usage.")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=5) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES)):
            if (finished_frame + 1) % 30 == 0:
                print(f"Matrix Resolved: Frame {finished_frame + 1} / {TOTAL_FRAMES}")

    print("\nCompilation Complete. Singularity Geometry Locked.")

if __name__ == '__main__':
    mp.freeze_support()
    run_batch()
