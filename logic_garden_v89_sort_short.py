"""
SOVEREIGN CODE: logic_garden_v91_sort_final_v4.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: Satisfaction / Entropy Reduction
TIMING: 0-12s Slow, 12-16s Fast, 16-18s Snap, 18-20s Pause
CHANGE: Removed text overlay. Pure visual.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_v91_sort_v4"
os.makedirs(OUT_DIR, exist_ok=True)

# Grid size (Low res for pixel art look)
W, H = 108, 192

def hsv_to_rgb(h, s, v):
    i = (h * 6).astype(int)
    f = (h * 6) - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    i = i % 6
    rgb = np.zeros((h.shape[0], h.shape[1], 3))
    mask = i == 0; rgb[mask] = np.stack([v[mask], t[mask], p[mask]], axis=-1)
    mask = i == 1; rgb[mask] = np.stack([q[mask], v[mask], p[mask]], axis=-1)
    mask = i == 2; rgb[mask] = np.stack([p[mask], v[mask], t[mask]], axis=-1)
    mask = i == 3; rgb[mask] = np.stack([p[mask], q[mask], v[mask]], axis=-1)
    mask = i == 4; rgb[mask] = np.stack([t[mask], p[mask], v[mask]], axis=-1)
    mask = i == 5; rgb[mask] = np.stack([v[mask], p[mask], q[mask]], axis=-1)
    return rgb

def run():
    print("LOGIC GARDEN 91: THE PERFECT SORT (V4 - CLEAN)")
    fig = plt.figure(figsize=(9, 16), facecolor='black')
    ax = fig.add_axes([0, 0, 1, 1], facecolor='black')
    
    # INIT
    np.random.seed(42)
    hues = np.random.rand(H, W)
    sats = np.ones((H, W))
    vals = np.ones((H, W))
    
    for f in range(TOTAL_FRAMES):
        ax.clear()
        ax.axis('off')
        
        # MATH-VERIFIED THROTTLE
        
        # 0-12s (0-360f): MOLASSES
        if f < 360:
            swap_prob = 0.25 
            passes = 1
            
        # 12-16s (360-480f): ACCELERATION
        elif f < 480:
            swap_prob = 0.8
            passes = 2 
            
        # 16-18s (480-540f): THE SNAP
        elif f < 540:
            swap_prob = 1.0
            passes = 10 
            
        # 18-20s (540-600f): PAUSE
        else:
            swap_prob = 0.0
            passes = 0
            
        # SORTING LOOP
        for _ in range(passes):
            for parity in [0, 1]:  
                row_indices = np.arange(parity, H-1, 2)
                
                # Slicing
                rows_top = hues[row_indices]
                rows_bot = hues[row_indices+1]
                
                # Check Order
                candidates = rows_top > rows_bot
                
                # Stochastic Filter
                if swap_prob < 1.0:
                    random_mask = np.random.rand(*candidates.shape) < swap_prob
                    do_swap = np.logical_and(candidates, random_mask)
                else:
                    do_swap = candidates 
                
                # Apply Swap
                if np.any(do_swap):
                    t_vals = rows_top[do_swap]
                    b_vals = rows_bot[do_swap]
                    
                    rows_top[do_swap] = b_vals
                    rows_bot[do_swap] = t_vals
                    
                    hues[row_indices] = rows_top
                    hues[row_indices+1] = rows_bot

        # RENDER
        rgb = hsv_to_rgb(hues, sats, vals)
        ax.imshow(rgb, aspect='auto', interpolation='nearest') 
        
        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=80, facecolor='black')
        
    plt.close(fig)

if __name__ == "__main__": run()
