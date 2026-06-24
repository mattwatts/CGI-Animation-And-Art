"""
SOVEREIGN CODE: logic_garden_323_williams_tensor.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 323 (Evan James Williams FRS // Virtual Quanta Exchange Tensor)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Seamless 10.0s Loop. Absolute Memory Annihilation Active.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.transforms as transforms
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
DURATION = 10.0  # 10.0 Second Seamless Loop
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_323_williams_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Heavy Core Scaffolding
C_STEEL     = '#606065'   # Structural Geometry
C_DARK      = '#202025'   # Deep Shadow Array
C_GOLD      = '#FFB300'   # Nucleon Mass
C_MAGENTA   = '#FF0055'   # Magnetic Field Quanta
C_CYAN      = '#00FFFF'   # Electric Field Path
C_WHITE     = '#FFFFFF'

# -------- COULOMB SCATTERING CONSTANTS --------
R0 = 55.0  # Distance of closest approach parameter
K = 2.0    # Hyperbolic deflection rigor

# ------------------------------------------------------------------
# O(1) DETERMINISTIC GEOMETRY
# ------------------------------------------------------------------
def draw_nucleus(ax, x, y, excitation, alpha_m):
    """Rigid Atomic Matrix (Hexagonal cluster reacting to mechanical stress)"""
    # Excitatory expansion radius
    rad = 18 + (excitation * 15)
    
    # Outer containment perimeter
    ax.add_patch(patches.Circle((x, y), radius=rad*1.4, facecolor='none', edgecolor=C_STEEL, lw=2.5, alpha=alpha_m*0.6, zorder=8))
    
    # Orbiting Nucleons (Subject to Coulomb spreading)
    for angle in np.linspace(0, 360, 6, endpoint=False):
        nx = x + np.cos(np.radians(angle)) * rad
        ny = y + np.sin(np.radians(angle)) * rad
        
        # Sub-polygon
        pts = np.array([[0, -8], [7, -4], [7, 4], [0, 8], [-7, 4], [-7, -4]])
        ax.add_patch(patches.Polygon(pts + [nx, ny], facecolor=C_TITANIUM, edgecolor=C_TEXT, lw=1.5, alpha=alpha_m, zorder=8.1))
        
    # The Dense Core
    core_pts = np.array([[0, -12], [10, -6], [10, 6], [0, 12], [-10, 6], [-10, -6]])
    ax.add_patch(patches.Polygon(core_pts + [x, y], facecolor=C_GOLD, edgecolor=C_TEXT, lw=2, alpha=alpha_m, zorder=8.2))
    
def draw_spallation(ax, x, y, size, alpha_m):
    """Kinematic chevron vectors ejected post-collision"""
    w = 12 * size
    h = 16 * size
    pts = np.array([[0, -h], [w, 0], [0, -h/2], [-w, 0]])
    ax.add_patch(patches.Polygon(pts + [x, y], facecolor=C_MAGENTA, alpha=alpha_m, zorder=7))

def draw_virtual_quanta(ax, x1, y1, x2, y2, stress, phase, alpha_m):
    """E.J. Williams' Method of Virtual Quanta - Transverse Electromagnetic Exchange"""
    dist = np.sqrt((x2-x1)**2 + (y2-y1)**2)
    angle = np.arctan2(y2-y1, x2-x1)
    
    # Render line coordinates rotated into position
    num_pts = 80
    lx = np.linspace(0, dist, num_pts)
    
    # Electric Field (Rigid cyan straight links acting as tensile cables)
    for offset in [-15, 0, 15]:
        el_y = np.full(num_pts, offset * stress)
        # Apply strict transform
        trans = transforms.Affine2D().rotate(angle).translate(x1, y1) + ax.transData
        ax.plot(lx, el_y, color=C_CYAN, lw=1.5 + stress*2, alpha=alpha_m * stress * 0.8, transform=trans, zorder=6)

    # Magnetic Field (Transverse sine wave representing virtual photon propagation)
    env = np.sin((lx / dist) * np.pi) # Hanning window to pin edges to the particles
    mag_y = np.sin((lx / dist) * 8 * np.pi - phase * 50 * np.pi) * 45 * stress * env
    mag_y2 = np.sin((lx / dist) * 8 * np.pi - phase * 50 * np.pi + np.pi) * 45 * stress * env
    
    trans_mag = transforms.Affine2D().rotate(angle).translate(x1, y1) + ax.transData
    ax.plot(lx, mag_y, color=C_MAGENTA, lw=4 * stress, alpha=alpha_m * stress, transform=trans_mag, zorder=6.5)
    ax.plot(lx, mag_y2, color=C_MAGENTA, lw=4 * stress, alpha=alpha_m * stress, transform=trans_mag, zorder=6.5)

def render_frame(packet):
    f, phase_ratio = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)

    # Master Loop Alpha (Seamless invisible entry and exit bounds)
    alpha_master = 1.0
    if phase_ratio < 0.05: alpha_master = phase_ratio / 0.05
    if phase_ratio > 0.95: alpha_master = (1.0 - phase_ratio) / 0.05

    # 1. INDUSTRIAL LATTICE 
    for gy in range(-900, 1000, 150):
        ax.axhline(gy, color=C_STEEL, lw=1, alpha=0.15, zorder=0)

    # 2. HYPERBOLIC COULOMB KINEMATICS
    # The exact mathematical mapping of two identical charged bodies scattering
    
    # Particle A: Drops from top left, scatters bottom left
    yA = 960 - (phase_ratio * 1920)
    xA = -np.sqrt(R0**2 + (yA / K)**2)
    
    # Particle B: Ascends from bottom right, scatters top right
    yB = -960 + (phase_ratio * 1920)
    xB = np.sqrt(R0**2 + (yB / K)**2)

    # Render rigid trailing wake paths (The Wake Tensor)
    hist_p = np.linspace(max(0, phase_ratio - 0.3), phase_ratio, 40)
    
    # A-Wake
    h_yA = 960 - (hist_p * 1920)
    h_xA = -np.sqrt(R0**2 + (h_yA / K)**2)
    ax.plot(h_xA, h_yA, color=C_DARK, lw=4, alpha=alpha_master*0.2, zorder=1)
    
    # B-Wake
    h_yB = -960 + (hist_p * 1920)
    h_xB = np.sqrt(R0**2 + (h_yB / K)**2)
    ax.plot(h_xB, h_yB, color=C_DARK, lw=4, alpha=alpha_master*0.2, zorder=1)

    # 3. INTERACTION STRESS (The Williams Threshold)
    # The stress forces dramatically peak linearly at exact phase 0.5 (Distance of closest approach)
    stress = np.exp(-((phase_ratio - 0.5)**2) / (2 * (0.04)**2))

    # Trigger Method of Virtual Quanta Exchange at high stress
    if stress > 0.05:
        draw_virtual_quanta(ax, xA, yA, xB, yB, stress, phase_ratio, alpha_master)

    # 4. KINEMATIC SPALLATION
    # Smashed fragments break away post-collision (Phase > 0.5)
    if phase_ratio >= 0.5:
        spall_time = (phase_ratio - 0.5) / 0.5
        spall_dist = spall_time * 1800
        sp_alpha = max(0.0, 1.0 - (spall_time * 1.5)) * alpha_master
        
        if sp_alpha > 0:
            # 4 symmetrical blast vectors
            angles = [45, 135, 225, 315]
            for a in angles:
                sx = np.cos(np.radians(a)) * spall_dist
                sy = np.sin(np.radians(a)) * spall_dist
                draw_spallation(ax, sx, sy, 1.0, sp_alpha)

    # Render Solid Core Vehicles
    draw_nucleus(ax, xA, yA, stress, alpha_master)
    draw_nucleus(ax, xB, yB, stress, alpha_master)

    # 5. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    ax.text(-500, 880, "LG-323 :: EVAN JAMES WILLIAMS FRS KINEMATIC TENSOR", color=C_TEXT, fontsize=22, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, 840, "[SFI-1.00] THE METHOD OF VIRTUAL QUANTA // COULOMB SCATTERING", color=C_STEEL, fontsize=12, fontname='monospace', zorder=80)
    
    # Telemetry Data Background
    ax.add_patch(patches.Rectangle((-520, -920), 1040, 160, facecolor=C_TITANIUM, alpha=0.9, zorder=79))
    
    ax.text(-500, -805, "IMPACT PARAMETER (b_c): 110.00 fm", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=80)
    
    # Gauge rendering
    ax.text(-500, -840, f"VIRTUAL QUANTA EXCHANGE STRESS: {stress*100:>05.2f} % Δ [MAX. LOAD]", color=C_MAGENTA if stress > 0.5 else C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=80)
    
    ax.add_patch(patches.Rectangle((-500, -865), 1000, 4, facecolor=C_STEEL, zorder=80))
    ax.add_patch(patches.Rectangle((-500, -865), 1000 * stress, 4, facecolor=C_MAGENTA, zorder=81))

    # Core coordinates
    ax.plot([-40, 40], [0, 0], color=C_CYAN, lw=2, alpha=0.3, zorder=1.5)
    ax.plot([0, 0], [-40, 40], color=C_CYAN, lw=2, alpha=0.3, zorder=1.5)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0)
    
    # Absolute Memory Annihilation execution
    plt.close('all')
    gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    # Retain 1 core to prevent OS suffocation during intensive O(1) tracking computations
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-323: EVAN JAMES WILLIAMS FRS KINEMATIC TENSOR [CORES: {cpu_cores}] [MEMORY LOCK ACTIVE]")
    
    # HOTFIX: maxtasksperchild=1 explicitly eradicates C-backend fragmentation
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
