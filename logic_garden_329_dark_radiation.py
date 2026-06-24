"""
SOVEREIGN CODE: logic_garden_329_dark_radiation.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 329 (Dark Radiation // U(1)' Gauge Symmetry Tensor)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Seamless 10.0s Loop. Absolute Camera Lock. O(1) Memory Eradication.
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
OUT_DIR = "frames_329_dark_rad_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Spacetime Metric Wireframe
C_STEEL     = '#606065'   # Invisible Dark Matter Halo (Blueprint)
C_DARK      = '#202025'   # Baryonic Core Shell
C_GOLD      = '#FFB300'   # Baryonic Core Density (Standard Matter)
C_CYAN      = '#00FFFF'   # Dark Electric Field Vector
C_MAGENTA   = '#FF0055'   # Dark Magnetic Field Vector
C_WHITE     = '#FFFFFF'

# -------- KINEMATIC CONSTANTS --------
R_ORBIT = 400.0
WAVE_CYCLES = 12       # Number of physical wave peaks between nodes
WAVE_SPEED  = -10       # Phase velocity of Dark Radiation (Integer for perfect wrap)
N_DARK_NODES = 4       # Quadruple DM tensor arrangement

# ------------------------------------------------------------------
# O(1) DETERMINISTIC WAVE VECTORS
# ------------------------------------------------------------------
def draw_dark_photon_flux(ax, x1, y1, x2, y2, phase_ratio):
    """Generates the Dark Electromagnetism transverse wave tensor propagating between nodes."""
    # Distance and Normal vectors
    dx = x2 - x1
    dy = y2 - y1
    dist = np.hypot(dx, dy)
    
    # Unit vectors
    ux = dx / dist
    uy = dy / dist
    nx = -uy  # Normal for transverse wave
    ny = ux
    
    # 300 discrete calculation points per beam for ultra-high-resolution rendering
    s = np.linspace(0, 1, 300)
    
    # Base linear interpolation coordinate
    bx = x1 + s * dx
    by = y1 + s * dy
    
    # Envelope function (Sinusoidal taper to prevent hard cuts at the nodes)
    envelope = np.sin(s * np.pi) ** 2
    
    # Wave equations matching exactly integer wrapped phase offsets
    wave_phase = s * WAVE_CYCLES * 2 * np.pi + phase_ratio * WAVE_SPEED * 2 * np.pi
    
    # Dark "E-Field" Displacement
    e_amp = 40.0 * envelope
    ex = bx + nx * np.sin(wave_phase) * e_amp
    ey = by + ny * np.sin(wave_phase) * e_amp
    
    # Dark "B-Field" Displacement (Orthogonal projection offset for pseudo-3D chirality)
    b_amp = 40.0 * envelope
    # We shift the orthogonal phase by pi/2 and project it
    bx_b = bx + (ux * 0.5 + nx * 0.5) * np.sin(wave_phase + np.pi/2) * b_amp
    by_b = by + (uy * 0.5 + ny * 0.5) * np.sin(wave_phase + np.pi/2) * b_amp

    # Draw the Dark Radiation Beams
    ax.plot(ex, ey, color=C_CYAN, lw=2.0, alpha=0.85, zorder=5)
    ax.plot(bx_b, by_b, color=C_MAGENTA, lw=1.5, alpha=0.85, zorder=5)
    
    # High-intensity energy spine
    ax.plot(bx, by, color=C_TITANIUM, lw=1.0, alpha=0.6, linestyle='--', zorder=4.9)

def draw_baryonic_core(ax):
    """The static Standard Model Matter, perfectly blind to the Dark Radiation intersecting it."""
    # Central armor plating
    ax.add_patch(patches.RegularPolygon((0, 0), numVertices=8, radius=90, facecolor=C_DARK, zorder=3))
    ax.add_patch(patches.RegularPolygon((0, 0), numVertices=8, radius=80, facecolor=C_GOLD, zorder=3.1))
    
    # Internal Standard Model architecture constraints
    ax.add_patch(patches.Circle((0, 0), radius=50, facecolor=C_BG, zorder=3.2))
    ax.add_patch(patches.Circle((0, 0), radius=35, facecolor=C_DARK, zorder=3.3))
    
    for ang in range(0, 360, 45):
        trans = transforms.Affine2D().rotate_deg(ang) + ax.transData
        ax.plot([50, 90], [0, 0], color=C_TEXT, lw=3, transform=trans, zorder=3.4)

def render_frame(packet):
    f, phase_ratio = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    
    # ----------------------------------------------------
    # BARE-METAL CAMERA LOCK: ALL AUTO-SCALING ANNIHILATED
    # ----------------------------------------------------
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)
    ax.autoscale(False)

    # 1. BARYONIC CENTER MASS
    draw_baryonic_core(ax)

    # 2. DARK MATTER HALO KINEMATICS
    # Orbital rotation over exactly 1 loop
    base_theta = phase_ratio * 2 * np.pi
    dm_x, dm_y = [], []
    
    for i in range(N_DARK_NODES):
        angle = base_theta + i * (2 * np.pi / N_DARK_NODES)
        x = R_ORBIT * np.cos(angle)
        y = R_ORBIT * np.sin(angle)
        dm_x.append(x)
        dm_y.append(y)
        
        # O(1) Dark Matter Nodes (Hollow Blueprints to show EM transparency)
        ax.add_patch(patches.Circle((x, y), radius=60, fill=False, edgecolor=C_STEEL, lw=4, linestyle='-', zorder=6))
        ax.add_patch(patches.Circle((x, y), radius=45, fill=False, edgecolor=C_TITANIUM, lw=2, linestyle='--', zorder=6))
        
        # Rotation crosshairs tracking spin
        cross_trans = transforms.Affine2D().rotate_deg_around(x, y, -phase_ratio * 360 * 2) + ax.transData
        ax.plot([x-70, x+70], [y, y], color=C_STEEL, lw=1.5, alpha=0.5, transform=cross_trans, zorder=6.1)
        ax.plot([x, x], [y-70, y+70], color=C_STEEL, lw=1.5, alpha=0.5, transform=cross_trans, zorder=6.1)

    ax.add_patch(patches.Circle((0, 0), radius=R_ORBIT, fill=False, edgecolor=C_TITANIUM, linestyle=":", lw=2, alpha=0.3, zorder=1))

    # 3. DARK RADIATION EXCHANGE MATRIX
    # Connect every node to every other node with the Dark EM flux
    for i in range(N_DARK_NODES):
        for j in range(i + 1, N_DARK_NODES):
            draw_dark_photon_flux(ax, dm_x[i], dm_y[i], dm_x[j], dm_y[j], phase_ratio)

    # 4. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    ax.text(-500, 880, "LG-329 :: DARK RADIATION TENSOR (U(1)' GAUGE)", color=C_TEXT, fontsize=22, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, 840, "[SFI-0.75] DARK ELECTROMAGNETISM // GAUGE BOSON (A') MEDIATION", color=C_CYAN, fontsize=12, fontname='monospace', zorder=80)
    
    # Telemetry Data Background
    ax.add_patch(patches.Rectangle((-520, -920), 1040, 200, facecolor=C_BG, edgecolor=C_TITANIUM, lw=2, alpha=0.9, zorder=79))
    
    # Theoretical Readouts
    ax.text(-500, -760, "STANDARD MODEL PHOTON CROSS-SECTION (U(1)_EM): 0.00", color=C_GOLD, fontsize=14, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, -800, "DARK SECTOR GAUGE SYMMETRY (U(1)'): ACTIVE VIBRATION", color=C_CYAN, fontsize=14, fontname='monospace', weight='bold', zorder=80)
    
    flux_state = abs(np.sin(phase_ratio * 4 * np.pi))
    ax.text(-500, -840, f"DARK PHOTON (A') FLUX DENSITY: {flux_state * 100:>05.2f} % Δ [PEAK LIMIT]", color=C_MAGENTA, fontsize=14, fontname='monospace', weight='bold', zorder=80)
    
    ax.add_patch(patches.Rectangle((-500, -865), 1000, 4, facecolor=C_STEEL, zorder=80))
    ax.add_patch(patches.Rectangle((-500, -865), 1000 * flux_state, 4, facecolor=C_MAGENTA, zorder=81))

    # Structural Callouts
    ax.text(120, -120, "BARYONIC CORE\nSTANDARD MATTER\nEM-INTERACTIVE", color=C_GOLD, fontsize=10, fontname='monospace', weight='bold', zorder=80, alpha=0.9)
    ax.text(0, 520, "DARK MATTER HALO / A' SOURCE", color=C_STEEL, fontsize=10, fontname='monospace', weight='bold', ha='center', zorder=80, alpha=0.9)

    # Output execution ensuring bounded output
    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    # Absolute Memory Annihilation
    plt.close('all')
    gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    # Enforce Executioner Protocol
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-329: DARK RADIATION TENSOR [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
