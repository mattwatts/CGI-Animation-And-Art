"""
SOVEREIGN CODE: logic_garden_v75_triage.py
CONTEXT: Logistics / Crisis Management
LESSON: "Optimize for Throughput, not Perfection."
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import copy

FPS, DURATION = 30, 15
OUT_DIR = "frames_v75_triage"
os.makedirs(OUT_DIR, exist_ok=True)

# Generate Random Data (Severity 0-100)
N = 50
np.random.seed(42)
initial_data = np.random.randint(0, 100, N)

def get_color(val):
    if val > 80: return '#FF0000' # Critical (Red)
    if val > 50: return '#FFFF00' # Urgent (Yellow)
    return '#00FF00' # Stable (Green)

def run():
    print("LOGIC GARDEN 75: TRIAGE SORT")
    fig = plt.figure(figsize=(16, 9), facecolor='#111111')
    
    # Simulating Sorting States
    # BUBBLE SORT (Slow)
    bubble_states = []
    arr = copy.deepcopy(initial_data)
    for i in range(N):
        for j in range(0, N-i-1):
            bubble_states.append(copy.deepcopy(arr))
            if arr[j] < arr[j+1]: # Sort Descending
                arr[j], arr[j+1] = arr[j+1], arr[j]
    bubble_sorted = arr
    
    # QUICKSORT (Fast - Conceptual)
    # We simulate Quicksort visually as rapid partitioning
    quick_states = []
    arr_q = copy.deepcopy(initial_data)
    # Fake "Log N" steps visually
    for _ in range(20): quick_states.append(copy.deepcopy(initial_data)) # Scan phase
    # Partition High
    high = [x for x in arr_q if x > 80]
    mid = [x for x in arr_q if 50 < x <= 80]
    low = [x for x in arr_q if x <= 50]
    # Snap to sorted
    sorted_q = high + mid + low 
    for _ in range(10): quick_states.append(copy.deepcopy(sorted_q)) # Done

    total_f = FPS * DURATION
    
    for f in range(total_f):
        fig.clf()
        ax1 = fig.add_axes([0.05, 0.2, 0.4, 0.6], facecolor='#111111')
        ax2 = fig.add_axes([0.55, 0.2, 0.4, 0.6], facecolor='#111111')
        
        # DRAW BUBBLE (Left)
        # 1 step per frame (very slow)
        b_idx = min(f, len(bubble_states)-1)
        b_data = bubble_states[b_idx]
        colors_b = [get_color(v) for v in b_data]
        ax1.bar(range(N), b_data, color=colors_b)
        ax1.set_title("ARTISAN SORT (O(N^2))", color='white', fontfamily='monospace')
        ax1.set_ylim(0, 100)
        ax1.axis('off')
        
        # DRAW QUICK (Right)
        # 1 step per 5 frames (fast jumps)
        q_idx = min(f // 5, len(quick_states)-1)
        q_data = quick_states[q_idx]
        colors_q = [get_color(v) for v in q_data]
        ax2.bar(range(N), q_data, color=colors_q)
        ax2.set_title("TRIAGE SORT (O(N log N))", color='#FFD700', fontfamily='monospace')
        ax2.set_ylim(0, 100)
        ax2.axis('off')

        # Annotations
        processed_b = b_idx
        processed_q = N * np.log2(N) # Fake metric
        
        if f > 60:
            ax2.text(25, 50, "CRITICALS CLEARED", color='#FFD700', ha='center', weight='bold', fontsize=12, bbox=dict(facecolor='black'))

        ax1.text(25, -10, "STATUS: STILL PROCESSING...", color='#555555', ha='center', fontfamily='monospace')
        
        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=80, facecolor='#111111')
    
    plt.close(fig)

if __name__ == "__main__": run()
