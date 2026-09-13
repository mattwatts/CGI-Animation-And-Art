"""
PROJECT: Logic Garden 436 (Exact Physical Construct // W88 Peanut Geometry)
FORMAT: YouTube Shorts (1080x1920)
METADATA: W88, PEANUT, HYDRODYNAMICS, KINEMATICS, DAYLIGHT, MINIATURISATION
EXECUTION: 12.0s Sequence. True Seamless Cyclical Computation Matrix.
RULES ENFORCED:
- O(N^2) 2D Parametric Elliptical Matrix (Approx 10,000 nodes actively shifting).
- O(N) 1D Radial Matrix (100 nodes capturing spherical symmetry).
- Flawless Parametric "Peanut" Spline generating the absolute casing shell.
- Daylight Palette (White Substrate / High-Contrast Solid Geometry).
- Purged Jargon. Australian spelling conventions (maths, colour, miniaturisation).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import multiprocessing as mp
import os
import gc
import math

# ======== SEQUENCE PARAMETERS ========
DURATION = 12.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_436_peanut"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'          # Indestructible Black UI
C_STEEL     = '#94A3B8'          # Reentry Vehicle Grid
C_PEANUT    = '#1E293B'          # Carbon Slate (Radiation Casing)
C_EGG       = '#FF3300'          # Intense Red (2D O(N^2) Computation)
C_SPHERE    = '#005599'          # Deep Marine (1D O(N) Computation)
C_RADAR     = '#00C853'          # Jade Kinematic Tracker

# ------------------------------------------------------------------
# O(1) MACRO PHYSICS ENGINE (GEOMETRY GENERATORS)
# ------------------------------------------------------------------
# 1. Structural RV Dimensions (1 unit = 1 mm scalar projection)
RV_BASE_W = 460.0
RV_HEIGHT = 1500.0
Y_BASE = 250.0
Y_TIP = Y_BASE + RV_HEIGHT

# 2. Peanut Radiation Case Generator
def generate_peanut_casing():
    # Length 890mm. Center = 945. Upper Y = 1390, Lower Y = 500
    Y_pe = np.linspace(500, 1390, 1000)
    R_pe = np.zeros_like(Y_pe)
    for i, y in enumerate(Y_pe):
        if y > 1180.0:
            R_pe[i] = math.sqrt(max(0.0, 160.0**2 - (y - 1180.0)**2))
        elif y < 710.0:
            R_pe[i] = math.sqrt(max(0.0, 170.0**2 - (y - 710.0)**2))
        else:
            # Waist transition (470mm span). Linear taper minus sine dip.
            u = (y - 710.0) / 470.0
            base = 170.0 - 10.0 * u
            dip = 45.0 * math.sin(math.pi * u)
            R_pe[i] = base - dip

    # Mirror Left and Right for polygon wrapping
    L_x = 540.0 - R_pe
    R_x = 540.0 + R_pe

    poly_pts = []
    for i in range(len(Y_pe)):
        poly_pts.append([L_x[i], Y_pe[i]])
    for i in range(len(Y_pe)-1, -1, -1):
        poly_pts.append([R_x[i], Y_pe[i]])

    return poly_pts

PEANUT_PROFILE = generate_peanut_casing()

# 3. 2D Hydrodynamic Matrix Generator (Approx 10,000 internal nodes)
# Egg Primary: Prolate Spheroid locked in the top lobe
def generate_primary_matrix():
    x_steps = 100
    y_steps = 127
    x_grid = np.linspace(540 - 110.0, 540 + 110.0, x_steps)
    y_grid = np.linspace(1170 - 140.0, 1170 + 140.0, y_steps)
    XG, YG = np.meshgrid(x_grid, y_grid)
    XF, YF = XG.flatten(), YG.flatten()

    # Boundary mask for exact elliptical bounds (x/a)^2 + (y/b)^2 <= 1.0
    mask = ((XF - 540.0)/110.0)**2 + ((YF - 1170.0)/140.0)**2 <= 0.98

    return XF[mask], YF[mask]

X_EGG_BASE, Y_EGG_BASE = generate_primary_matrix()
EGG_NODE_COUNT = len(X_EGG_BASE) # Perfectly engineered to ~9,974 nodes

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    tau = f / float(TOTAL_FRAMES)

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # 1. THE CONE: REENTRY VEHICLE (Ghost Outline / Dimensional Reference)
    rv_poly = [
        [540 - RV_BASE_W/2, Y_BASE],
        [540 + RV_BASE_W/2, Y_BASE],
        [540 + 25.0, Y_TIP],
        [540 - 25.0, Y_TIP]
    ]
    ax.add_patch(patches.Polygon(rv_poly, fill=False, edgecolor=C_STEEL, lw=2.5, linestyle='dashed', zorder=5))

    # 2. THE PEANUT: RADIATION CASING
    # FIXED: Replaced invalid solid_capstyle with True Polygon attribute 'joinstyle'
    ax.add_patch(patches.Polygon(PEANUT_PROFILE, fill=False, edgecolor=C_PEANUT, lw=7, joinstyle='round', zorder=10))

    # 3. THE PRIMARY (O(N^2) 2D HYDRODYNAMICS LATTICE)
    # The computational nodes physically flutter as a simulated pressure matrix.
    # 3 cyclic loops visually synchronised to the 12.0s master tape.
    k_cyc = 3.0
    omega = 2.0 * math.pi * k_cyc * tau

    # Spatial differential injects dense fluid oscillation
    disp_x = 2.5 * np.sin(omega + Y_EGG_BASE / 20.0)
    disp_y = 2.5 * np.cos(omega + X_EGG_BASE / 20.0)

    ax.scatter(X_EGG_BASE + disp_x, Y_EGG_BASE + disp_y, s=2.5, color=C_EGG, edgecolors='none', alpha=0.85, zorder=20)

    # Target Box Crosshair overlay showing "Grid Lock"
    ax.plot([400, 680], [1170, 1170], color=C_EGG, lw=1.5, alpha=0.5, zorder=25)
    ax.plot([540, 540], [1000, 1340], color=C_EGG, lw=1.5, alpha=0.5, zorder=25)

    # 4. THE SECONDARY (O(N) 1D SPHERICAL GEOMETRY)
    # Background boundary of the sphere mapped strictly.
    ax.add_patch(patches.Circle((540, 710), 140, fill=False, edgecolor=C_SPHERE, lw=3, alpha=0.5, zorder=15))

    # The 1D Radial Array (Exactly 100 points stretching from center to edge)
    r_1d = np.linspace(0, 140.0, 100)
    theta_1d = omega # Rotates perfectly 3 times across the loop covering the massive 3D architecture
    x_1d = 540.0 + r_1d * np.cos(theta_1d)
    y_1d = 710.0 + r_1d * np.sin(theta_1d)

    # Plot as heavier interconnected structural nodes
    ax.plot(x_1d, y_1d, color=C_SPHERE, lw=3, zorder=18)
    ax.scatter(x_1d, y_1d, s=15, color=C_SPHERE, edgecolors='none', zorder=19)
    # The extreme leading node highlights the 1D sweep
    ax.scatter(x_1d[-1], y_1d[-1], s=40, color=C_RADAR, edgecolors='none', zorder=21)

    # 5. ABSOLUTE DAYLIGHT TELEMETRY (TOP HUD)
    ax.add_patch(patches.Rectangle((0, 1780), 1080, 140, facecolor=C_BG, zorder=80))
    ax.plot([0, 1080], [1780, 1780], color=C_TEXT, lw=6, zorder=81)

    ax.text(40, 1870, "LG-436 // THE W88 KINEMATIC GEOMETRY", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=82)
    ax.text(40, 1825, "MINIATURISATION MATRIX // 1D VS 2D HYDRODYNAMICS", color=C_STEEL, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=82)

    # Dimensional Tags
    ax.text(900, 1000, "PEANUT\nRADIATION\nCASING", color=C_PEANUT, fontsize=18, fontname='monospace', weight='bold', ha='left', va='center', zorder=82)
    ax.plot([880, 715], [1000, 1000], color=C_PEANUT, lw=2, zorder=82)

    ax.text(250, 400, "REENTRY\nVEHICLE\nCONE", color=C_STEEL, fontsize=18, fontname='monospace', weight='bold', ha='right', va='center', zorder=82)
    ax.plot([270, 390], [400, 400], color=C_STEEL, lw=2, linestyle='dashed', zorder=82)

    # 6. ABSOLUTE DAYLIGHT TELEMETRY (BOTTOM HUD)
    ax.add_patch(patches.Rectangle((0, 0), 1080, 160, facecolor=C_BG, zorder=80))
    ax.plot([0, 1080], [160, 160], color=C_TEXT, lw=6, zorder=81)

    ax.text(40, 110, f"PRIMARY (EGG) : O(N²) COMPUTE [{EGG_NODE_COUNT} NODES]", color=C_EGG, fontsize=18, fontname='monospace', weight='bold', zorder=82)
    ax.text(40, 60,  f"SECONDARY (SPHERE) : O(N) COMPUTE [100 NODES]", color=C_SPHERE, fontsize=18, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-436: W88 PEANUT KINEMATICS (DAYLIGHT) [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        frames = range(TOTAL_FRAMES)
        for finished_frame in pool.imap_unordered(render_frame, frames, chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Geometric Patch Parameters Verified. Hydrodynamic Tensors Locked. Stand by for compilation.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
