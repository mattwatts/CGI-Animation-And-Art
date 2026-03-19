"""
SOVEREIGN CODE: logic_garden_129_the_neural_lattice.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python High-Fidelity Simulator
SCENE: Logic Garden 129 (BCI Neural Sorting / Phase Coherence)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle
import math
import os

# CONFIG
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_129_neural_lattice"
os.makedirs(OUT_DIR, exist_ok=True)
N = 120 # Density of the neural pathways

# THE INDUSTRIAL PALETTE
C_VOID = '#050510'       # Deep Institutional Void
C_GUIDE = '#112233'      # Structural Orbital Rings
C_NOISE = '#00FFCC'      # Cyan (Unsorted Entropy / Raw thought)
C_COMPARE = '#FF003C'    # Red (Friction / CPU compare)
C_SWAP = '#FFD700'       # Gold (Voltage spike / Value swap)
C_ZEN = '#39FF14'        # Terminal Green (Coherence / Flow state)
C_TEXT = '#FFFFFF'       # White HUD

# --- 1. THE BCI NEURAL ENGINES (Algorithms converted to state recorders) ---
def record_quicksort(arr):
    a = arr.copy()
    states = []
    def _partition(low, high):
        pivot = a[high]
        i = low - 1
        for j in range(low, high):
            states.append((a.copy(), [j, high], []))
            if a[j] <= pivot:
                i = i + 1
                a[i], a[j] = a[j], a[i]
                states.append((a.copy(), [], [i, j]))
        a[i+1], a[high] = a[high], a[i+1]
        states.append((a.copy(), [], [i+1, high]))
        return i + 1
    def _qs(low, high):
        if low < high:
            pi = _partition(low, high)
            _qs(low, pi - 1)
            _qs(pi + 1, high)
    _qs(0, len(a)-1)
    states.append((a.copy(), [], []))
    return states

def record_insertionsort(arr):
    a = arr.copy()
    states = []
    for i in range(1, len(a)):
        key = a[i]
        j = i-1
        while j >= 0 and key < a[j]:
            states.append((a.copy(), [j, j+1], []))
            a[j + 1] = a[j]
            states.append((a.copy(), [], [j+1]))
            j -= 1
        a[j + 1] = key
        states.append((a.copy(), [], [j+1]))
    states.append((a.copy(), [], []))
    return states

def record_bubblesort(arr):
    a = arr.copy()
    states = []
    for i in range(len(a)):
        swapped = False
        for j in range(0, len(a)-i-1):
            states.append((a.copy(), [j, j+1], []))
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                swapped = True
                states.append((a.copy(), [], [j, j+1]))
        if not swapped: break
    states.append((a.copy(), [], []))
    return states

def get_state_at_frame(states, f, target_f):
    """Maps deterministic algorithm logic to physical timeline frames."""
    if f >= target_f: return states[-1], True
    idx = int((f / target_f) * len(states))
    return states[min(idx, len(states)-1)], False

def build_ring_geometry(state, is_locked, N, base_r, max_len, rot_offset):
    """Vectorized geometry generation for ultra-fast rendering of hundreds of lines."""
    arr, active, swap = state
    lines = []
    colors = []
    
    # Mathematical constants
    C_X, C_Y = 540, 960  # Center of 1080x1920
    
    for i in range(N):
        # Angle starts at -90 degrees (Top dead center)
        theta = (2 * math.pi * (i / N)) - (math.pi / 2) + rot_offset
        val = arr[i]
        length = (val / N) * max_len
        
        x0 = C_X + base_r * math.cos(theta)
        y0 = C_Y + base_r * math.sin(theta)
        x1 = C_X + (base_r + length) * math.cos(theta)
        y1 = C_Y + (base_r + length) * math.sin(theta)
        
        lines.append([(x0, y0), (x1, y1)])
        
        # Color resolution mapping (Friction vs Flow)
        if is_locked: colors.append(C_ZEN)
        elif i in swap: colors.append(C_SWAP)
        elif i in active: colors.append(C_COMPARE)
        else: colors.append(C_NOISE)
        
    return lines, colors

def run():
    print(f"LOGIC GARDEN 129: THE NEURAL LATTICE ({TOTAL_FRAMES} frames)")
    
    np.random.seed(42) # Compile-Time Safety
    initial_arr = np.random.permutation(np.arange(1, N + 1))
    
    print("Generating BCI Matrices (O(N) Pre-computation)...")
    st_q = record_quicksort(initial_arr)
    st_i = record_insertionsort(initial_arr)
    st_b = record_bubblesort(initial_arr)
    
    # Timing Limits (When does each band achieve Zen?)
    F_Q = 140  # QuickSort (Macro coherence): 4.6 seconds
    F_I = 320  # Insertion (Logic coherence): 10.6 seconds
    F_B = 520  # Bubble (Deep subconscious): 17.3 seconds
    
    for f in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(C_VOID)
        
        # Lock aspect to perfectly symmetrical circles
        ax.set_aspect('equal')
        ax.set_xlim(0, 1080)
        ax.set_ylim(0, 1920)
        
        # --- LOGIC RESOLUTION ---
        state_q, lock_q = get_state_at_frame(st_q, f, F_Q)
        state_i, lock_i = get_state_at_frame(st_i, f, F_I)
        state_b, lock_b = get_state_at_frame(st_b, f, F_B)
        
        # --- KINETIC FLOW (Rotation applied ONLY post-lock) ---
        rot_q = (f - F_Q) * 0.015 if lock_q else 0
        rot_i = (f - F_I) * -0.012 if lock_i else 0
        rot_b = (f - F_B) * 0.008 if lock_b else 0
        
        # --- GEOMETRY CONSTRUCTION ---
        # Ring 3 (Outer): QuickSort. R=260 to 420
        l_q, c_q = build_ring_geometry(state_q, lock_q, N, base_r=260, max_len=160, rot_offset=rot_q)
        # Ring 2 (Mid): InsertionSort. R=140 to 240
        l_i, c_i = build_ring_geometry(state_i, lock_i, N, base_r=140, max_len=100, rot_offset=rot_i)
        # Ring 1 (Inner): BubbleSort. R=50 to 120
        l_b, c_b = build_ring_geometry(state_b, lock_b, N, base_r=50, max_len=70, rot_offset=rot_b)
        
        all_lines = l_q + l_i + l_b
        all_colors = c_q + c_i + c_b
        
        # --- RENDERING (PROTOCOL: NEON POP) ---
        # Guides
        for r in [50, 140, 260]:
            ax.add_patch(Circle((540, 960), r, fill=False, color=C_GUIDE, lw=1, alpha=0.5))
        
        # Core Nucleus
        nuc_color = C_ZEN if (lock_q and lock_i and lock_b) else C_COMPARE
        nuc_alpha = 1.0 if (lock_q and lock_i and lock_b) else min(1.0, 0.3 + (math.sin(f*0.5)*0.2))
        ax.add_patch(Circle((540, 960), 12, color=nuc_color, alpha=nuc_alpha))
        
        # High-Fidelity Lines with Bloom
        lc_main = LineCollection(all_lines, colors=all_colors, linewidths=4, zorder=3)
        lc_bloom = LineCollection(all_lines, colors=all_colors, linewidths=10, alpha=0.15, zorder=2)
        ax.add_collection(lc_main)
        ax.add_collection(lc_bloom)
        
        # --- UI & TELEMETRY ---
        ax.text(540, 1800, "Logic Garden 129: Neural Lattice", color=C_TEXT, ha='center', fontsize=35, fontname='monospace', weight='bold')
        ax.text(540, 1750, "BCI Cognitive Optimisation", color=C_NOISE, ha='center', fontsize=20, fontname='monospace')
        
        def draw_hud(y, label, locked):
            color = C_ZEN if locked else C_COMPARE
            status = "[ PHASE COHERENCE SYNCHRONIZED ]" if locked else "[ RESOLVING FRICTION ENTROPY... ]"
            ax.text(80, y, label, color=C_TEXT, ha='left', fontsize=18, fontname='monospace')
            ax.text(1000, y, status, color=color, ha='right', fontsize=18, fontname='monospace', weight='bold')
            
        draw_hud(250, "MACRO BAND [QUICKSORT] O(N log N)", lock_q)
        draw_hud(200, "LOGIC BAND [INSERTION] O(N^2)", lock_i)
        draw_hud(150, "SENSORY BAND [BUBBLE] O(N^2)", lock_b)
        
        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close(fig)

if __name__ == "__main__": run()
