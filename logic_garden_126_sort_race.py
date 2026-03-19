"""
SOVEREIGN CODE: logic_garden_126_the_great_search.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python High-Fidelity Simulator
SCENE: Logic Garden 126 (The Algorithm Race)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# CONFIG
FPS = 24
OUT_DIR = "frames_126_sort"
os.makedirs(OUT_DIR, exist_ok=True)
N = 30 # Small enough to see the flow clearly

# THE INDUSTRIAL PALETTE
C_VOID = '#050510'       # Deep Institutional Void
C_DEFAULT = '#AAFFEE'    # Cyan (Unsorted)
C_ACTIVE = '#FF003C'     # Red (Comparing/Reading)
C_SWAP = '#FFD700'       # Gold (Writing/Swapping)
C_SORTED = '#39FF14'     # Terminal Green (Perfect Lattice)
C_TEXT = '#FFFFFF'       # White UI

# --- 1. THE ALGORITHM GENERATORS ---
# Each yields: (current_array_state, [read_indices], [write/swap_indices])

def bubble_sort(arr):
    a = arr.copy()
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            yield a.copy(), [j, j+1], []
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                swapped = True
                yield a.copy(), [], [j, j+1]
        if not swapped: break
    yield a.copy(), [], []

def cocktail_shaker_sort(arr):
    a = arr.copy()
    n = len(a)
    swapped = True
    start, end = 0, n - 1
    while swapped:
        swapped = False
        for i in range(start, end):
            yield a.copy(), [i, i+1], []
            if a[i] > a[i+1]:
                a[i], a[i+1] = a[i+1], a[i]
                swapped = True
                yield a.copy(), [], [i, i+1]
        if not swapped: break
        swapped = False
        end -= 1
        for i in range(end-1, start-1, -1):
            yield a.copy(), [i, i+1], []
            if a[i] > a[i+1]:
                a[i], a[i+1] = a[i+1], a[i]
                swapped = True
                yield a.copy(), [], [i, i+1]
        start += 1
    yield a.copy(), [], []

def selection_sort(arr):
    a = arr.copy()
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            yield a.copy(), [min_idx, j], []
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
        yield a.copy(), [], [i, min_idx]
    yield a.copy(), [], []

def insertion_sort(arr):
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i-1
        while j >= 0 and key < a[j]:
            yield a.copy(), [j, j+1], []
            a[j + 1] = a[j]
            yield a.copy(), [], [j+1]
            j -= 1
        a[j + 1] = key
        yield a.copy(), [], [j+1]
    yield a.copy(), [], []

def shell_sort(arr):
    a = arr.copy()
    n = len(a)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = a[i]
            j = i
            while j >= gap and a[j - gap] > temp:
                yield a.copy(), [j, j-gap], []
                a[j] = a[j - gap]
                yield a.copy(), [], [j]
                j -= gap
            a[j] = temp
            yield a.copy(), [], [j]
        gap //= 2
    yield a.copy(), [], []

def merge_sort_gen(arr):
    a = arr.copy()
    yield from _merge_sort(a, 0, len(a)-1)
    yield a.copy(), [], []

def _merge_sort(a, l, r):
    if l < r:
        m = l + (r - l) // 2
        yield from _merge_sort(a, l, m)
        yield from _merge_sort(a, m + 1, r)
        yield from _merge(a, l, m, r)

def _merge(a, l, m, r):
    left = a[l:m+1].copy()
    right = a[m+1:r+1].copy()
    i = 0; j = 0; k = l
    while i < len(left) and j < len(right):
        yield a.copy(), [k, l+i, m+1+j], []
        if left[i] <= right[j]:
            a[k] = left[i]
            i += 1
        else:
            a[k] = right[j]
            j += 1
        yield a.copy(), [], [k]
        k += 1
    while i < len(left):
        a[k] = left[i]
        yield a.copy(), [], [k]
        i += 1; k += 1
    while j < len(right):
        a[k] = right[j]
        yield a.copy(), [], [k]
        j += 1; k += 1

def heap_sort(arr):
    a = arr.copy()
    n = len(a)
    def heapify(n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < n: yield a.copy(), [largest, l], []
        if l < n and a[l] > a[largest]: largest = l
        if r < n: yield a.copy(), [largest, r], []
        if r < n and a[r] > a[largest]: largest = r
        if largest != i:
            a[i], a[largest] = a[largest], a[i]
            yield a.copy(), [], [i, largest]
            yield from heapify(n, largest)

    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(n, i)
    for i in range(n - 1, 0, -1):
        yield a.copy(), [i, 0], []
        a[i], a[0] = a[0], a[i]
        yield a.copy(), [], [i, 0]
        yield from heapify(i, 0)
    yield a.copy(), [], []

def quick_sort_gen(arr):
    a = arr.copy()
    yield from _quick_sort(a, 0, len(a)-1)
    yield a.copy(), [], []

def _quick_sort(a, low, high):
    if low < high:
        pi_val = [0]
        yield from _partition(a, low, high, pi_val)
        pi = pi_val[0]
        yield from _quick_sort(a, low, pi - 1)
        yield from _quick_sort(a, pi + 1, high)

def _partition(a, low, high, pi_val):
    pivot = a[high]
    i = low - 1
    for j in range(low, high):
        yield a.copy(), [j, high], []
        if a[j] <= pivot:
            i = i + 1
            a[i], a[j] = a[j], a[i]
            yield a.copy(), [], [i, j]
    a[i+1], a[high] = a[high], a[i+1]
    yield a.copy(), [], [i+1, high]
    pi_val[0] = i + 1
    return

# --- 2. ENGINE MAP ---
ALGORITHMS = [
    ("QUICKSORT: O(N log N)", quick_sort_gen),
    ("HEAPSORT: O(N log N)", heap_sort),
    ("MERGE SORT: O(N log N)", merge_sort_gen),
    ("SHELL SORT: O(N (log N)^2)", shell_sort),
    ("INSERTION SORT: O(N^2)", insertion_sort),
    ("SELECTION SORT: O(N^2)", selection_sort),
    ("BUBBLE SORT: O(N^2)", bubble_sort),
    ("COCKTAIL SORT: O(N^2)", cocktail_shaker_sort)
]

def run():
    print("INITIALIZING LOGIC GARDEN 126: THE GREAT SEARCH")
    
    # 1. Create Initial Entropy (Identical for all)
    np.random.seed(42)  # Compile-time lock
    initial_arr = np.arange(1, N + 1)
    np.random.shuffle(initial_arr)
    
    # 2. Setup Generators
    generators = [func(initial_arr) for name, func in ALGORITHMS]
    states = [None] * len(ALGORITHMS)
    finished = [False] * len(ALGORITHMS)
    
    # 3. Setup the UI Matrix
    fig, axes = plt.subplots(8, 1, figsize=(10.8, 19.2), dpi=100, facecolor=C_VOID)
    fig.subplots_adjust(top=0.92, bottom=0.03, left=0.05, right=0.95, hspace=0.4)
    
    fig.suptitle("Logic Garden 126: Sort Race", color=C_DEFAULT, 
                 fontsize=30, fontname='monospace', weight='bold')

    bars_list = []
    text_list = []
    
    for idx, ax in enumerate(axes):
        ax.set_facecolor(C_VOID)
        ax.axis('off')
        
        # Draw initial bars
        bars = ax.bar(range(N), initial_arr, color=C_DEFAULT, edgecolor=C_VOID, linewidth=1)
        bars_list.append(bars)
        
        # Add Title Widget
        t = ax.text(0, N*1.1, ALGORITHMS[idx][0], color=C_TEXT, fontname='monospace', 
                    fontsize=20, weight='bold', verticalalignment='bottom')
        text_list.append(t)
        
        # Lock scales
        ax.set_ylim(0, N * 1.5)
        ax.set_xlim(-1, N)

    frame = 0
    all_done = False
    
    while not all_done:
        all_done = True
        
        for i, gen in enumerate(generators):
            if not finished[i]:
                try:
                    states[i] = next(gen)
                    all_done = False
                except StopIteration:
                    finished[i] = True
                    # Set title to GREEN when finished
                    text_list[i].set_color(C_SORTED)
                    
            if states[i] is not None:
                arr_state, active, swap = states[i]
                
                # Update Bars (Extremely optimized rendering)
                for j, bar in enumerate(bars_list[i]):
                    bar.set_height(arr_state[j])
                    if finished[i]:
                        bar.set_color(C_SORTED)
                    elif j in swap:
                        bar.set_color(C_SWAP)
                    elif j in active:
                        bar.set_color(C_ACTIVE)
                    else:
                        bar.set_color(C_DEFAULT)

        plt.savefig(os.path.join(OUT_DIR, f"frame_{frame:04d}.png"))
        frame += 1
        if frame % 50 == 0:
            print(f"Generated {frame} frames...")

    # Hold Phase
    print("Sorting Complete. Rendering Hold Frames...")
    for h in range(FPS * 3): # 3 Second lock on perfect logic
        plt.savefig(os.path.join(OUT_DIR, f"frame_{frame:04d}.png"))
        frame += 1

    plt.close(fig)
    print(f"Total Frames: {frame}. Phase Transition Complete.")

if __name__ == "__main__": run()
