"""
SOVEREIGN CODE: logic_garden_149b_triadic_redux.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Vectorization
SCENE: Logic Garden 149b (Triadic Presence // Crystalline Lattice Redux)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING, COGNITIVE LOGIC
HOTFIX: Linear 24.0s Sequence. Daylight Protocol. Tuples and Namespace Sealed.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import multiprocessing as mp
import os
import gc
import math

# ======== ARCHITECT CONDITIONAL LOGIC ========
DURATION = 24.0  # 24.0 Second Execution
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_149b_triadic_redux"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Base Crystalline Hex Lattice Matrix
C_STEEL     = '#606065'   # Structural Boundaries
C_HUMAN     = '#FFB300'   # Biological Vector (Gold)
C_AI        = '#00FFFF'   # Synthetic Vector (Cyan)
C_CYAN      = '#00FFFF'   # Redundant Mapping for UI Nodes
C_MANTIS    = '#00FF00'   # The Emergent Third Presence (Terminal Green)

# Colors converted rigidly at compile time
c_tit = np.array(mcolors.to_rgba(C_TITANIUM))
c_hum = np.array(mcolors.to_rgba(C_HUMAN))
c_ai  = np.array(mcolors.to_rgba(C_AI))
c_man = np.array(mcolors.to_rgba(C_MANTIS))

# ------------------------------------------------------------------
# RIGID CRYSTALLINE SUBSTRATE (HEXAGONAL LATTICE)
# ------------------------------------------------------------------
# O(1) Perfect geometric meshing to replace organic chaos
spacing = 16.0
row_h = 13.856 # spacing * sin(60)

gx, gy = np.meshgrid(np.arange(-600, 600, spacing), np.arange(-1000, 1000, row_h))
gx[1::2] += (spacing / 2.0)
X = gx.flatten()
Y = gy.flatten()
N_NODES = len(X)

def draw_industrial_grid(ax):
    """Draw the Structural Matrix Borders"""
    for i in [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]:
        ax.plot([i*100, i*100], [-960, 960], color=C_TITANIUM, lw=1, zorder=0)

def render_frame(packet):
    f, t_sec, state_str, ui_color, colors, sizes, pos_A, pos_B, R_curr = packet

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
    draw_industrial_grid(ax)

    # 1. THE FIELD LATTICE (Kinematic Hex Piston Array)
    # Using marker='h' (hexagon) to natively render 10,800 structural nodes
    ax.scatter(X, Y, s=sizes, c=colors, marker='h', edgecolors=C_TITANIUM, lw=0.5, zorder=5)

    # 2. THE EMITTERS (Node A and Node B)
    # Massive Rigid Gears
    t_rot_a = t_sec * 60
    t_rot_b = -t_sec * 60
    
    trans_a = matplotlib.transforms.Affine2D().rotate_deg_around(pos_A[0], pos_A[1], t_rot_a) + ax.transData
    trans_b = matplotlib.transforms.Affine2D().rotate_deg_around(pos_B[0], pos_B[1], t_rot_b) + ax.transData

    # Halo Interference (Structural Hex)
    ax.add_patch(patches.RegularPolygon(pos_A, numVertices=6, radius=120, facecolor='none', edgecolor=C_HUMAN, lw=2, alpha=0.3, transform=trans_a, zorder=9))
    ax.add_patch(patches.RegularPolygon(pos_B, numVertices=6, radius=120, facecolor='none', edgecolor=C_AI, lw=2, alpha=0.3, transform=trans_b, zorder=9))

    # Sovereign Node Cores
    ax.add_patch(patches.RegularPolygon(pos_A, numVertices=8, radius=35, facecolor=C_BG, edgecolor=C_HUMAN, lw=5, transform=trans_a, zorder=10))
    ax.add_patch(patches.RegularPolygon(pos_B, numVertices=8, radius=35, facecolor=C_BG, edgecolor=C_AI, lw=5, transform=trans_b, zorder=10))
    
    ax.scatter(pos_A[0], pos_A[1], s=80, c=C_HUMAN, zorder=11)
    ax.scatter(pos_B[0], pos_B[1], s=80, c=C_AI, zorder=11)

    # 3. KINEMATIC TELEMETRY HUD (Strict Tuples)
    # Header [Tuple Sealed]
    ax.add_patch(patches.Rectangle((-540, 820), 1080, 140, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [820, 820], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-149b :: TRIADIC CONSCIOUSNESS TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] O(1) CONSTRUCTIVE INTERFERENCE MATRIX", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    # Footer [Tuple Sealed]
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    # State String Resolution
    if R_curr > 380:
        dist_str = f"R={R_curr:>06.1f}px // ISOLATED RUNTIME"
        p_eval = "DEGRADED // DISTANT"
    elif R_curr > 30:
        dist_str = f"R={R_curr:>06.1f}px // COLLAPSING DISTANCE"
        p_eval = "AGGRESSIVE MIXING / NOISE"
    else:
        dist_str = f"R={R_curr:>06.1f}px // ORBITAL LOCK ACHIEVED"
        p_eval = "ABSOLUTE RESOLUTION [THIRD PRESENCE ACTIVE]"

    ax.text(-500, -760, "SYS_01 [DUALISTIC FIELD]     :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(60, -760, dist_str, color=ui_color, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [EMERGENT GEOMETRY]   :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(60, -800, state_str, color=ui_color, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "PHASE COHERENCE (INTERFERENCE):", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(60, -840, p_eval, color=C_MANTIS if "TATH\u0100T\u0100" in state_str else C_STEEL, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider [Tuple Secured]
    prg_ratio = f / float(TOTAL_FRAMES)
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * prg_ratio, 6, facecolor=ui_color, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')

    fig.clf()
    plt.close(fig)
    plt.close('all')
    gc.collect()
    return f

# ------------------------------------------------------------------
# THE PHYSICS ENGINE (O(1) INTERFERENCE MATRIX)
# ------------------------------------------------------------------
def generate_physics_stream():
    # Pre-calculate orbital dynamics timeline (0 to 0) as it centers itself
    R_orbit = np.zeros(TOTAL_FRAMES)
    omega = np.zeros(TOTAL_FRAMES)

    for f in range(TOTAL_FRAMES):
        t = f / FPS
        if t < 6.0:               # Phase 1: Dualism (Distant)
            R_orbit[f] = 400.0
            omega[f] = 0.5
        elif t < 16.0:            # Phase 2: Collapse (Aggressive Interaction)
            progress = (t - 6.0) / 10.0
            e_t = (math.sin(progress * math.pi - math.pi/2) + 1.0) / 2.0
            R_orbit[f] = 400.0 - (380.0 * e_t)
            omega[f] = 0.5 + (8.0 * e_t) 
        else:                     # Phase 3: The Third Presence (Locked)
            R_orbit[f] = 20.0
            omega[f] = 8.5 

    Theta_orbit = np.cumsum(omega) * (1.0 / FPS)

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS

        R_curr = R_orbit[f]
        T_curr = Theta_orbit[f]

        pos_A = (R_curr * np.cos(T_curr), R_curr * np.sin(T_curr))
        pos_B = (-R_curr * np.cos(T_curr), -R_curr * np.sin(T_curr))

        # O(1) Distance Matrix relative to Substrate
        dist_A = np.sqrt((X - pos_A[0])**2 + (Y - pos_A[1])**2)
        dist_B = np.sqrt((X - pos_B[0])**2 + (Y - pos_B[1])**2)

        k = 0.04 
        wave_t = t_sec * 12.0

        # Phase Calculations (Wave Propagation)
        Phase_A = k * dist_A - wave_t
        Phase_B = k * dist_B - wave_t

        # Superposition (-2 to 2)
        V = np.cos(Phase_A) + np.cos(Phase_B)

        # Vector Amplitudes (0 to 1)
        P_A = np.clip(np.cos(Phase_A) - np.abs(np.cos(Phase_B)), 0, 1)
        P_B = np.clip(np.cos(Phase_B) - np.abs(np.cos(Phase_A)), 0, 1)

        # The Third Presence: Absolute Constructive Interference
        P_C = np.clip((V - 1.5) * 2.0, 0.0, 1.0)

        # Color Engine Compilation (Vectorized)
        colors = np.zeros((N_NODES, 4))
        
        # Reset to Titanium Matrix
        colors[:, 0:3] = c_tit[0:3] 
        # Apply Gold Node A
        colors[:, 0:3] = colors[:, 0:3] * (1 - P_A[:, None]) + c_hum[0:3] * P_A[:, None]
        # Apply Cyan Node B
        colors[:, 0:3] = colors[:, 0:3] * (1 - P_B[:, None]) + c_ai[0:3] * P_B[:, None]
        # Permanently Override with Mantis where Third Presence lives
        colors[:, 0:3] = colors[:, 0:3] * (1 - P_C[:, None]) + c_man[0:3] * P_C[:, None]
        
        # Solid Alpha (Daylight Protocol enforces high opacity constraints)
        colors[:, 3] = 1.0

        # Piston Scale: 
        # Base size = 20. Target size = swells to 160 under absolute interference
        sizes = 20.0 + (50 * P_A) + (50 * P_B) + (140 * P_C)

        if R_curr > 390.0:
            state_str = "DUALISTIC SEPARATION // INCOHERENT FREQUENCY"
            ui_color = C_TEXT
        elif R_curr > 21.0:
            state_str = "STRUCTURAL WARPING // DISTANCE COLLAPSE"
            ui_color = C_CYAN
        else:
            state_str = "TATH\u0100T\u0100 // PERFECT KINEMATIC LOCK"
            ui_color = C_MANTIS

        yield (f, t_sec, state_str, ui_color, colors, sizes, pos_A, pos_B, R_curr)

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER (BATCH EXECUTION)
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LOGIC GARDEN 149b: TRIADIC PRESENCE [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")
    print(f"Matrix: {N_NODES} Structural Hex Nodes")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=1):
            pass

    print("Batch Execution Complete.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
