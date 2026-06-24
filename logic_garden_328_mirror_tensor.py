"""
SOVEREIGN CODE: logic_garden_328_mirror_tensor.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 328 (Mirror Matter // Parity Inversion Tensor)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Seamless 10.0s Loop. Absolute Camera Lock. Rigid Vector Architecture. Syntax Rupture Sealed.
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
OUT_DIR = "frames_328_mirror_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Low-Impact Geodesic Lattice
C_STEEL     = '#606065'   # Heavy Metric Displacement
C_DARK      = '#202025'   # Baryonic Solid Armor
C_GOLD      = '#FFB300'   # Ordinary Matter Core (EM Interactive)
C_CYAN      = '#00FFFF'   # Alice Matter Blueprint (EM Null)
C_MAGENTA   = '#FF0055'   # Kinetic Mixing Rupture
C_WHITE     = '#FFFFFF'

# -------- KINEMATIC CONSTANTS --------
R_ORBIT = 240.0

# ------------------------------------------------------------------
# O(1) DETERMINISTIC PARITY VECTORS
# ------------------------------------------------------------------
def draw_mass_structure(ax, x, y, phase_ratio, is_mirror):
    """Draws the absolute kinematic structures incorporating Parity Inversion (P -> -P)"""
    scale = 35.0
    
    # Internal chiral rotation: Ordinary Matter (Right-handed, CW), Alice Matter (Left-handed, CCW)
    rot_dir = -1 if is_mirror else 1
    base_rot = phase_ratio * 360 * rot_dir
    trans = transforms.Affine2D().rotate_deg_around(x, y, base_rot) + ax.transData

    if not is_mirror:
        # ORDINARY MATTER: Dense, Solid, EM-Interactive
        ax.add_patch(patches.RegularPolygon((x, y), numVertices=6, radius=scale*1.4, facecolor=C_DARK, edgecolor=C_TEXT, lw=2, zorder=8, transform=trans))
        # Asymmetric Right-Handed Structure
        pts = np.array([[-scale, -scale*0.5], [scale, -scale*0.5], [scale*0.5, scale]])
        ax.add_patch(patches.Polygon(pts + [x, y], facecolor=C_GOLD, edgecolor=C_BG, lw=1.5, zorder=8.1, transform=trans))
        ax.add_patch(patches.Circle((x, y), radius=10, facecolor=C_TEXT, zorder=8.2))
    else:
        # MIRROR MATTER (ALICE): Hollow, Wireframe, EM-Null, Left-Handed Inverse Geometry
        ax.add_patch(patches.RegularPolygon((x, y), numVertices=6, radius=scale*1.4, fill=False, edgecolor=C_CYAN, linestyle='-', lw=3, zorder=8, transform=trans))
        # Asymmetric Left-Handed Structure (Strict parity reflection of OM)
        pts_inv = np.array([[scale, -scale*0.5], [-scale, -scale*0.5], [-scale*0.5, scale]])
        ax.add_patch(patches.Polygon(pts_inv + [x, y], fill=False, edgecolor=C_CYAN, lw=2, zorder=8.1, transform=trans))
        
        # Internal hollow core
        ax.plot([x-10, x+10], [y, y], color=C_CYAN, lw=2, zorder=8.2)
        ax.plot([x, x], [y-10, y+10], color=C_CYAN, lw=2, zorder=8.2)

def draw_mixing_stress(ax, x1, y1, x2, y2, phase_ratio):
    """Calculates the theoretical ε kinematic mixing bridge"""
    pulse = (np.sin(phase_ratio * 6 * np.pi) ** 8)  # Sharp, violent, rare pulsing
    if pulse > 0.1:
        # The bridge attempts to form but is mathematically sheared by the parity barrier
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        
        # Draw sheared connection
        ax.plot([x1, mid_x - 20], [y1, mid_y], color=C_MAGENTA, lw=3*pulse, alpha=pulse*0.8, zorder=7)
        ax.plot([mid_x + 20, x2], [mid_y, y2], color=C_CYAN, lw=3*pulse, alpha=pulse*0.8, zorder=7)
        
        # The Rupture point at the exact Barycenter
        ax.add_patch(patches.Circle((mid_x, mid_y), radius=40*pulse, fill=False, edgecolor=C_MAGENTA, lw=2, alpha=pulse*0.6, zorder=7))

def render_frame(packet):
    f, phase_ratio = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    
    # ----------------------------------------------------
    # BARE-METAL CAMERA LOCK & AUTO-SCALE ERADICATION
    # ----------------------------------------------------
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)
    ax.autoscale(False)

    # 1. ORBITAL KINEMATICS
    theta = phase_ratio * 2 * np.pi
    
    # Ordinary Matter Coordinate
    om_x = R_ORBIT * np.cos(theta)
    om_y = R_ORBIT * np.sin(theta)
    
    # Alice Matter Coordinate (Strict 180-degree parity opposite)
    mm_x = R_ORBIT * np.cos(theta + np.pi)
    mm_y = R_ORBIT * np.sin(theta + np.pi)

    # 2. THE GRAVITATIONAL METRIC (SPACETIME LATTICE)
    # We plot the fundamental grid and apply an inverse-square warp to both OM and MM identically.
    lattice_extent = 1200
    grid_lines = np.linspace(-lattice_extent, lattice_extent, 45)
    
    for gy in grid_lines:
        line_x = np.linspace(-lattice_extent, lattice_extent, 200)
        line_y = np.full_like(line_x, gy)
        
        # Apply gravitational displacement
        for mx, my in [(om_x, om_y), (mm_x, mm_y)]:
            dist_sq = (line_x - mx)**2 + (line_y - my)**2 + 8000 # Smoothing factor to prevent divide by zero
            warp_factor = 25000 / dist_sq
            line_y += warp_factor * np.sign(my - gy) * (abs(my - gy)/300) # Pull toward mass
            
        ax.plot(line_x, line_y, color=C_TITANIUM, lw=1.0, alpha=0.5, zorder=1)
        
    for gx in grid_lines:
        line_y = np.linspace(-lattice_extent, lattice_extent, 200)
        line_x = np.full_like(line_y, gx)
        
        for mx, my in [(om_x, om_y), (mm_x, mm_y)]:
            dist_sq = (line_x - mx)**2 + (line_y - my)**2 + 8000
            warp_factor = 25000 / dist_sq
            line_x += warp_factor * np.sign(mx - gx) * (abs(mx - gx)/300)
            
        ax.plot(line_x, line_y, color=C_TITANIUM, lw=1.0, alpha=0.5, zorder=1)

    # Orbital Track
    ax.add_patch(patches.Circle((0, 0), radius=R_ORBIT, fill=False, edgecolor=C_STEEL, linestyle=':', lw=2, alpha=0.4, zorder=2))

    # 3. KINETIC MIXING RUPTURE
    draw_mixing_stress(ax, om_x, om_y, mm_x, mm_y, phase_ratio)

    # 4. MATTER STRUCTURE RENDERING
    # Alice Matter acts entirely indistinguishable topologically from Ordinary Matter
    draw_mass_structure(ax, om_x, om_y, phase_ratio, is_mirror=False)
    draw_mass_structure(ax, mm_x, mm_y, phase_ratio, is_mirror=True)
    
    # Center of Mass absolute tracking
    ax.plot([-30, 30], [0, 0], color=C_STEEL, lw=2, zorder=9)
    ax.plot([0, 0], [-30, 30], color=C_STEEL, lw=2, zorder=9)

    # 5. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    ax.text(-500, 880, "LG-328 :: ALICE MATTER INVERSION TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, 840, "[SFI-0.75] DARK SECTOR CHIRALITY // GRAVITATIONAL COUPLING", color=C_STEEL, fontsize=12, fontname='monospace', zorder=80)
    
    # Telemetry Data Background
    ax.add_patch(patches.Rectangle((-520, -920), 1040, 160, facecolor=C_BG, edgecolor=C_TITANIUM, lw=2, alpha=0.9, zorder=79))
    
    # Active Physics Readout
    ax.text(-500, -805, "GRAVITATIONAL COUPLING (G): 1.00 [LOCKED & SYMMETRIC]", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, -835, "ELECTROMAGNETIC CROSS-SECTION (σ): 0.00 [NULL]", color=C_CYAN, fontsize=14, fontname='monospace', weight='bold', zorder=80)
    
    pulse = (np.sin(phase_ratio * 6 * np.pi) ** 8)
    ax.text(-500, -870, f"PHOTON-MIRROR KINETIC MIXING (ε): {pulse * 1e-9:.2e} [DECAY]", color=C_MAGENTA if pulse > 0.1 else C_STEEL, fontsize=14, fontname='monospace', weight='bold', zorder=80)
    
    ax.add_patch(patches.Rectangle((-500, -895), 1000, 4, facecolor=C_TITANIUM, zorder=80))
    # Chiral Tracking Bar [Y-Axis Vector Locked]
    ax.add_patch(patches.Rectangle((-500 + 490*(1-np.cos(theta)), -896), 20, 6, facecolor=C_DARK, zorder=81))
    
    # Callouts anchored strictly to their masses
    ax.text(om_x + 60, om_y + 40, "ORDINARY SECTOR\n[RIGHT-HANDED]\nEM-ACTIVE", color=C_DARK, fontsize=10, fontname='monospace', weight='bold', zorder=80, alpha=0.8)
    ax.text(mm_x - 60, mm_y - 40, "SHADOW SECTOR\n[LEFT-HANDED]\nEM-NULL", color=C_CYAN, fontsize=10, fontname='monospace', weight='bold', ha='right', zorder=80, alpha=0.8)

    # Sovereign Execution Output
    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    # Absolute Memory Annihilation execution
    plt.close('all')
    gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    # Enforces maxtasksperchild=1 to physically prevent C-level array fragmentation build up
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-328: ALICE MATTER INVERSION TENSOR [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
