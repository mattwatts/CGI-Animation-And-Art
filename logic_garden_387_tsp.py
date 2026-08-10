"""
PROJECT: Logic Garden 387 (The Travelling Salesman // O(N!) Brute Force Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: EXACT BIO-KINEMATICS, COMBINATORIAL OPTIMISATION, NP-HARD GEOMETRY
EXECUTION: 24.0s Sequence. True Mathematical Permutation.
RULES ENFORCED:
- Daylight Palette (White Background / High Contrast).
- O(1) Pre-compiled physical state arrays.
- Brutalist geometric vectorisation (No floating scatter/dots/labels).
- Australian spelling conventions enforced natively.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
from matplotlib.collections import LineCollection
import multiprocessing as mp
import itertools
import os
import gc

# ======== SEQUENCE PARAMETERS ========
FPS = 60
DURATION = 24.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_387_tsp"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG            = '#FFFFFF'
C_TEXT          = '#111115'
C_NODE          = '#0F172A'  # Indestructible Black Mass
C_SEARCH        = '#FF3300'  # Intense Red (Combustion of Operations)
C_LOCKED        = '#00C853'  # Jade (Secured Isomorphism)
C_ORIGIN        = '#005599'  # Deep Marine (Node 0)
C_GUI           = '#94A3B8'

# ------------------------------------------------------------------
# O(N!) KINEMATIC GEOMETRY PRE-COMPUTATION
# ------------------------------------------------------------------
np.random.seed(387)
N_CITIES = 10
# (N-1)! permutations = 9! = 362,880 unique geometric routes

# Generate highly structured pseudo-random city coordinates (Brutalist spread)
theta = np.linspace(0, 2*np.pi, N_CITIES, endpoint=False)
radius = np.random.uniform(200, 380, N_CITIES)
cx = 540 + radius * np.cos(theta + np.random.uniform(-0.5, 0.5, N_CITIES))
cy = 960 + radius * np.sin(theta + np.random.uniform(-0.5, 0.5, N_CITIES))
cities = np.column_stack((cx, cy))

# O(1) Distance Matrix Map
dist_matrix = np.zeros((N_CITIES, N_CITIES))
for i in range(N_CITIES):
    for j in range(N_CITIES):
        dist_matrix[i, j] = np.linalg.norm(cities[i] - cities[j])

GLOBAL_HISTORY = []

def pre_compute():
    print("PHASE 1: PRE-COMPUTING O(N!) COMBINATORIAL MATHEMATICS...")
    # Anchor at City 0 to remove rotational duplicates.
    perms = list(itertools.permutations(range(1, N_CITIES)))
    total_perms = len(perms)
    print(f"TOTAL GEOMETRIC VECTORS GENERATED: {total_perms}")

    # 24 seconds = 1440 frames. 362880 / 1440 = 252 operations per frame.
    active_frames = int(FPS * 18.0)
    chunk_size = total_perms // active_frames

    best_dist = float('inf')
    best_path = None
    ops_count = 0

    for f in range(active_frames):
        start = f * chunk_size
        end = min(start + chunk_size, total_perms)

        for i in range(start, end):
            p = (0,) + perms[i] + (0,) # Start and terminate at Origin

            # Explicit physical distance tensor
            d = sum(dist_matrix[p[k], p[k+1]] for k in range(N_CITIES))
            ops_count += 1

            if d < best_dist:
                best_dist = d
                best_path = p

        # Lock in state for current frame render
        curr_view = (0,) + perms[end-1] + (0,)
        curr_dist = sum(dist_matrix[curr_view[k], curr_view[k+1]] for k in range(N_CITIES))
        
        GLOBAL_HISTORY.append({
            'ops': ops_count,
            'curr_path': curr_view,
            'curr_dist': curr_dist,
            'best_path': best_path,
            'best_dist': best_dist,
            'terminated': False
        })

    # Phase Transition: Hold Final Isomorphism for 6.0 seconds
    last_state = GLOBAL_HISTORY[-1].copy()
    last_state['terminated'] = True
    last_state['ops'] = total_perms
    for _ in range(TOTAL_FRAMES - active_frames):
        GLOBAL_HISTORY.append(last_state)

    print(f"MATHEMATICS COMPILED: {len(GLOBAL_HISTORY)} TOTAL FRAMES AWAITING DISPATCH.")

# ------------------------------------------------------------------
# PHYSICAL STATE GENERATOR / RENDER ENGINE
# ------------------------------------------------------------------
def render_frame(f_idx):
    state = GLOBAL_HISTORY[f_idx]

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.]); ax.set_axis_off(); fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    # 1. KINEMATIC GEOMETRY PIPELINE
    best_p = state['best_path']
    curr_p = state['curr_path']

    # Layer A: The Secure Isomorphism (Jade)
    if best_p is not None:
        best_lines = []
        for i in range(N_CITIES):
            p1, p2 = best_p[i], best_p[i+1]
            best_lines.append([cities[p1], cities[p2]])
        lc_best = LineCollection(best_lines, colors=C_LOCKED, linewidths=5.0, capstyle='round', zorder=2)
        ax.add_collection(lc_best)

    # Layer B: The Thermodynamic Search Vector (Crimson spallation)
    if not state['terminated']:
        search_lines = []
        for i in range(N_CITIES):
            p1, p2 = curr_p[i], curr_p[i+1]
            search_lines.append([cities[p1], cities[p2]])
        # Aggressive thin red line rapidly shifting to map operations
        lc_search = LineCollection(search_lines, colors=C_SEARCH, linewidths=1.5, alpha=0.8, zorder=3)
        ax.add_collection(lc_search)

    # Layer C: Primary Architectural Nodes
    ax.scatter(cities[1:, 0], cities[1:, 1], s=400, color=C_BG, edgecolors=C_NODE, linewidths=4, zorder=5)
    ax.scatter(cities[0, 0], cities[0, 1], s=600, color=C_BG, edgecolors=C_ORIGIN, linewidths=6, zorder=6) # Origin
    
    # Isolate Identity tag purely to Origin node
    ax.text(cities[0, 0], cities[0, 1], "ORG", color=C_ORIGIN, fontsize=12, fontname='monospace', weight='bold', ha='center', va='center', zorder=10)

    # 2. HIGH-DENSITY HUD & TELEMETRY
    # Header Module
    ax.add_patch(Rectangle((0, 1720), 1080, 200, facecolor=C_BG, zorder=80))
    ax.text(50, 1840, "LG-387 :: THE TRAVELLING SALESMAN TENSOR", color=C_TEXT, fontsize=28, fontname='monospace', weight='bold', zorder=82)
    ax.text(50, 1780, "[SFI-1.00] O(N!) COMBINATORIAL OPTIMISATION COMPILER", color=C_GUI, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.plot([0, 1080], [1720, 1720], color=C_TEXT, lw=4, zorder=81)

    # Footer Module
    ax.add_patch(Rectangle((0, 0), 1080, 240, facecolor=C_BG, zorder=80))
    ax.plot([0, 1080], [240, 240], color=C_TEXT, lw=4, zorder=81)

    # Left Telemetry
    ax.text(50, 160, f"NODES (CITIES)    : N={N_CITIES}", color=C_TEXT, fontsize=20, fontname='monospace', weight='bold', zorder=82)
    ax.text(50, 110, f"TOTAL PERMUTATIONS: {362880:06d}", color=C_TEXT, fontsize=20, fontname='monospace', weight='bold', zorder=82)

    op_color = C_LOCKED if state['terminated'] else C_SEARCH
    ax.text(50, 60,  f"OPERATIONS AUDITED: {state['ops']:06d}", color=op_color, fontsize=20, fontname='monospace', weight='bold', zorder=82)

    # Right Telemetry
    ax.text(550, 160, f"OPTIMISATION TARGET: ABS(MIN)", color=C_GUI, fontsize=20, fontname='monospace', weight='bold', zorder=82)
    
    if not state['terminated']:
        ax.text(550, 110, "BRUTE FORCE SCANNING...", color=C_SEARCH, fontsize=20, fontname='monospace', weight='bold', zorder=82)
        ax.text(550, 60,  f"CURRENT PATH LENGTH: {state['curr_dist']:06.1f} U", color=C_SEARCH, fontsize=20, fontname='monospace', weight='bold', zorder=82)
    else:
        ax.text(550, 110, "NP-HARD GEOMETRY LOCKED", color=C_LOCKED, fontsize=20, fontname='monospace', weight='bold', zorder=82)
        ax.text(550, 60,  f"SHORTEST PATH SECURED: {state['best_dist']:06.1f} U", color=C_LOCKED, fontsize=20, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f_idx:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f_idx

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    pre_compute()
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-387: THE TRAVELLING SALESMAN TENSOR [CORES: {cpu_cores}]")
    print("Executing PROTOCOL: Multicore Combinatorial Yield")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")
    print("Compilation Complete. True NP-Hard Physical State Rendered.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
