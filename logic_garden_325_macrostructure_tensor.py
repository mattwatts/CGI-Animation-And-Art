"""
SOVEREIGN CODE: logic_garden_325_macrostructure_tensor.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 325 (Macro-Structural Web // Perfect Zoom Tensor)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Seamless 10.0s Loop. Topological Parity Enforced. Torsional Matrix Synced.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
DURATION = 10.0  # 10.0 Second Seamless Loop
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_325_macro_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Void Pressure Vectors
C_STEEL     = '#606065'   # Dark Matter Filament Rebar
C_DARK      = '#202025'   # Core Structural Matrix
C_GOLD      = '#FFB300'   # Baryonic Thermal Exhaust
C_CYAN      = '#00FFFF'   # Dense Galactic Nodes
C_MAGENTA   = '#FF0055'   # Tensile Rupture / Dark Energy Overpressure
C_WHITE     = '#FFFFFF'

# -------- KINEMATIC CONSTANTS --------
N_NODES = 12       # Structural geometric pillars per shell
EXP_BASE = 2.0     # The Void Metric expansion multiplier
R_BASE = 50.0      # Base radius coordinate

# ------------------------------------------------------------------
# O(1) DETERMINISTIC GEOMETRY
# ------------------------------------------------------------------
def calculate_shell_topology(layer_idx, phase_ratio):
    """Calculates the absolute position of a Dark Matter concentric shell."""
    # Exponential scaling forces the continuous infinite zoom
    r = R_BASE * (EXP_BASE ** (layer_idx + phase_ratio))
    
    # Continuous Torsional Expansion. 
    # Ensures that when Layer L expands to the size of Layer L+1, it is rotated perfectly into place.
    ang_offset = (layer_idx + phase_ratio) * (np.pi / N_NODES)
    angles = np.linspace(0, 2*np.pi, N_NODES, endpoint=False) + ang_offset
    
    xs = r * np.cos(angles)
    ys = r * np.sin(angles)
    
    # Absolute Loop Fade Constraints (Zero pop at extreme Z-boundaries)
    alpha = 1.0
    if r < 20: 
        alpha = max(0.0, (r - 5) / 15.0) 
    elif r > 800:
        alpha = max(0.0, (1200 - r) / 400.0) 
        
    return xs, ys, r, angles, alpha

def draw_baryonic_node(ax, x, y, r, alpha_m):
    """Galactic thermal exhaust trapped in the Dark Matter gravity well."""
    scale = r * 0.04 # Perspective node scaling
    
    # Gravity Trench (The Bounding Box Base)
    ax.add_patch(patches.Circle((x, y), radius=scale*1.4, facecolor=C_DARK, alpha=alpha_m*0.8, zorder=6))
    # Baryonic Dust
    ax.add_patch(patches.Circle((x, y), radius=scale*0.8, facecolor=C_GOLD, alpha=alpha_m*0.9, zorder=6.1))
    # Core Density
    pts = np.array([[0, -scale*0.5], [scale*0.5, 0], [0, scale*0.5], [-scale*0.5, 0]])
    ax.add_patch(patches.Polygon(pts + [x, y], facecolor=C_CYAN, zorder=6.2, alpha=alpha_m))
    
def draw_dark_energy_piston(ax, r, alpha_m):
    """Visualizes the invisible scalar pressure of the Void Engine."""
    if r > 30 and r < 900:
        ax.add_patch(patches.Circle((0, 0), radius=r*0.95, fill=False, edgecolor=C_TITANIUM, linestyle=':', lw=2, alpha=alpha_m*0.5, zorder=2))

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

    shells = []
    # Layer range guarantees full visibility span from center void to outer camera limit
    for L in range(-4, 6):
        xs, ys, r, ang, alpha = calculate_shell_topology(L, phase_ratio)
        shells.append((xs, ys, r, ang, alpha))

    # 1. DRAW STRUCTURE: DARK MATTER SCAFFOLD & VOID PRESSURES
    for idx in range(len(shells)):
        xs, ys, r, ang, alpha = shells[idx]
        
        if alpha <= 0.0: continue
        
        draw_dark_energy_piston(ax, r, alpha)
        
        # Filament Runaway Overpressure Limit
        is_rupturing = r > 600
        edge_color = C_MAGENTA if is_rupturing else C_STEEL
        line_w = 4.5 if is_rupturing else 2.5
        
        # Concentric Structural Ring
        for i in range(N_NODES):
            x1, y1 = xs[i], ys[i]
            x2, y2 = xs[(i+1)%N_NODES], ys[(i+1)%N_NODES]
            ax.plot([x1, x2], [y1, y2], color=edge_color, lw=line_w, alpha=alpha*0.8, zorder=4)
            draw_baryonic_node(ax, x1, y1, r, alpha)
            
        # Transverse Radial Bridging (Filaments crossing the void)
        if idx < len(shells) - 1:
            nx_xs, nx_ys, nx_r, nx_ang, nx_alpha = shells[idx+1]
            if nx_alpha > 0:
                t_alpha = min(alpha, nx_alpha) * 0.7
                
                # Rigid geometric bridging maintaining symmetric tension
                for i in range(N_NODES):
                    x1, y1 = xs[i], ys[i]
                    
                    # Offsets map to the mathematically closest inner nodes under torsional twist
                    for offset in [0, -1]:
                        target_idx = (i + offset) % N_NODES
                        tx, ty = nx_xs[target_idx], nx_ys[target_idx]
                        
                        mid_r = (r + nx_r) / 2.0
                        rad_rupture = mid_r > 600
                        rad_color = C_MAGENTA if rad_rupture else C_STEEL
                        rad_w = 3.5 if rad_rupture else 1.5
                        
                        ax.plot([x1, tx], [y1, ty], color=rad_color, lw=rad_w, alpha=t_alpha, zorder=3)

    # 2. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    ax.text(-500, 880, "LG-325 :: MACRO-STRUCTURAL KINEMATICS TENSOR", color=C_TEXT, fontsize=22, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, 840, "[SFI-0.50] THE COSMIC WEB // EXPONENTIAL RUNAWAY RUPTURE", color=C_STEEL, fontsize=12, fontname='monospace', zorder=80)
    
    # Telemetry Data Background
    ax.add_patch(patches.Rectangle((-520, -920), 1040, 200, facecolor=C_TITANIUM, alpha=0.9, zorder=79))
    
    # Cosmological Readouts (Configured for strict closed-loop observation)
    expansion_pulse = abs(np.sin(phase_ratio * 4 * np.pi))
    ax.text(-500, -780, f"LOCAL HUBBLE EXPANSION (H0): Δ{expansion_pulse*72:>05.2f} km/s/Mpc", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, -820, "SYSTEM DIAGNOSTIC: EQUILIBRIUM BROKEN. UNCONSTRAINED EXPANSION.", color=C_MAGENTA, fontsize=12, fontname='monospace', weight='bold', zorder=80)
    
    ax.text(-500, -855, f"OVERPRESSURE SHIFT LOGIC (Λ): {expansion_pulse * 100:>05.2f} % Δ [SHEAR IMMINENT]", color=C_MAGENTA if expansion_pulse > 0.5 else C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=80)
    
    ax.add_patch(patches.Rectangle((-500, -880), 1000, 4, facecolor=C_STEEL, zorder=80))
    # Oscillating Loop Sweep to prevent bar snapping
    ax.add_patch(patches.Rectangle((-500 + 490*(1-expansion_pulse), -880), 20 + 980*expansion_pulse, 4, facecolor=C_MAGENTA, zorder=81))

    # Core Reference Callouts
    ax.text(-470, 200, "DARK MATTER\nSCAFFOLD\n(FILAMENT)", color=C_STEEL, fontsize=10, fontname='monospace', weight='bold', ha='right', zorder=80)
    ax.text(470, -200, "BARYONIC\nEXHAUST\n(NODE)", color=C_GOLD, fontsize=10, fontname='monospace', weight='bold', ha='left', zorder=80)

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
    # Retain 1 core to prevent OS suffocation during intensive fractal tracking computations
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-325: MACRO-STRUCTURAL KINEMATICS [CORES: {cpu_cores}] [MEMORY LOCK ACTIVE]")
    
    # HOTFIX: maxtasksperchild=1 explicitly eradicates C-backend fragmentation
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
