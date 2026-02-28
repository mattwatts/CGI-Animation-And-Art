import numpy as np
from PIL import Image
import multiprocessing
import os
import time

# --- CONSTANTS & CONFIGURATION ---
WIDTH, HEIGHT = 2000, 2000
MAX_ITER = 256
FRAMES = 4800
ZOOM_FACTOR = 0.9975  # Zoom
OUTPUT_DIR = "fractal_frames"
# Target: Seahorse Valley specific point
CENTER_X = -0.7436438870371587
CENTER_Y = 0.1318259042053119
INITIAL_RANGE = 3.0

# --- COLOR PALETTE (The Industrialist) ---
# Mapping 0-255 iterations to specific colors
# Midnight Black (0,0,0) -> IKB (0, 47, 167) -> Cyan -> White
def create_palette():
    # Initialize with Midnight Black
    palette = np.zeros((256, 3), dtype=np.uint8)
    
    for i in range(256):
        t = i / 255.0
        if i == MAX_ITER:
            r, g, b = 0, 0, 0 # Stable points are black
        else:
            # Smooth gradient function
            # R: Low
            r = int(9 * (1-t) * t**3 * 255)
            # G: Increases late (Cyan tail)
            g = int(15 * (1-t)**2 * t**2 * 255)
            # B: International Klein Blue dominant
            b = int(8.5 * (1-t)**3 * t * 255) + 40
            
            # Boost brightness for visibility against black
            r = min(255, r * 2)
            g = min(255, g * 3)
            b = min(255, b + i)
            
        palette[i] = (r, g, b)
    return palette

PALETTE = create_palette()

def render_frame(args):
    """
    Worker node function. 
    Isolated memory context for rendering a single frame.
    """
    frame_num, x_center, y_center, zoom_range = args
    
    # Define the complex plane for this frame
    x_min, x_max = x_center - zoom_range / 2, x_center + zoom_range / 2
    y_min, y_max = y_center - zoom_range * (HEIGHT / WIDTH) / 2, y_center + zoom_range * (HEIGHT / WIDTH) / 2

    # Vectorized Grid Generation (The Scout logic)
    x = np.linspace(x_min, x_max, WIDTH).astype(np.float64)
    y = np.linspace(y_min, y_max, HEIGHT).astype(np.float64)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    
    # Initialize Z and Iteration counts
    Z = np.zeros_like(C)
    div_time = np.zeros(Z.shape, dtype=int)
    m = np.full(C.shape, True, dtype=bool)

    # The Skeptic: Maxwell's Demon Iteration Loop
    for i in range(MAX_ITER):
        Z[m] = Z[m]**2 + C[m]
        diverged = np.greater(np.abs(Z[m]), 2)
        div_time_now = div_time[m]
        div_time_now[diverged] = i
        div_time[m] = div_time_now
        m[m] = np.invert(diverged)
        if not np.any(m):
            break

    # Map iterations to Palette
    img_array = PALETTE[div_time]
    
    # The Synthesiser: Construct Artifact
    img = Image.fromarray(img_array, 'RGB')
    filename = os.path.join(OUTPUT_DIR, f"frame_{frame_num:04d}.png")
    img.save(filename)
    return f"Frame {frame_num} complete."

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print(f"| INDUSTRIAL ENGINE START | Cores: {multiprocessing.cpu_count()} | Target: {FRAMES} Frames |")
    
    # Pre-calculate zoom trajectory to avoid race conditions
    tasks = []
    current_range = INITIAL_RANGE
    
    # Generate tasks for Minimum Set Cover of the timeline
    for i in range(FRAMES):
        tasks.append((i, CENTER_X, CENTER_Y, current_range))
        current_range *= ZOOM_FACTOR

    # Parallel Execution (Batch Mode)
    # Using 'spawn' context if on Windows/generic to avoid Copy-on-Write issues, 
    # but standard Pool is fine here for pure maths.
    with multiprocessing.Pool(processes=max(1, multiprocessing.cpu_count() - 1)) as pool:
        # Map tasks to workers
        for result in pool.imap_unordered(render_frame, tasks):
            # Lightweight logging to reduce console I/O entropy
            if int(result.split()[1]) % 10 == 0:
                print(f"[{time.strftime('%H:%M:%S')}] {result}")

    print("| INDUSTRIAL ENGINE STOP | Sequence Generated. |")

if __name__ == "__main__":
    main()
