"""
SOVEREIGN CODE: logic_garden_320_koch_tensor.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 320 (Koch Snowflake // The Fractal Tensor)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Z-Index Occlusion Purged. Stepped exponential pyramid structure locked.
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
OUT_DIR = "frames_320_koch_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Daylight Plate Faces
C_STEEL     = '#606065'   # Deep Structural Shadow
C_DARK      = '#202025'   # Core Chasm
C_GOLD      = '#FFB300'   # Telemetry & Geometric Binding
C_CYAN      = '#00FFFF'   # High-Energy Tracking UI
C_MAGENTA   = '#FF0055'   # Absolute Zero Point Singularity

# ------------------------------------------------------------------
# O(1) FRACTAL MATRIX GENERATOR (KOCH SNOWFLAKE)
# ------------------------------------------------------------------
def generate_koch_snowflake(radius, depth):
    # Generates the CCW starting equilateral triangle (Point UP)
    angles = np.array([np.pi/2, np.pi/2 + 2*np.pi/3, np.pi/2 + 4*np.pi/3])
    pts = np.column_stack([np.cos(angles), np.sin(angles)]) * radius

    # Iterative bare-metal outward expansion
    for _ in range(depth):
        new_pts = []
        num_pts = len(pts)
        for i in range(num_pts):
            A = pts[i]
            B = pts[(i+1) % num_pts]
            V = B - A
            
            p1 = A + V / 3.0
            p3 = A + 2.0 * V / 3.0
            
            # Rotate exactly -60 degrees for outward spikes on CCW perimeter
            p2x = p1[0] + 0.5 * (V[0]/3.0) + 0.86602540378 * (V[1]/3.0)
            p2y = p1[1] - 0.86602540378 * (V[0]/3.0) + 0.5 * (V[1]/3.0)
            p2 = np.array([p2x, p2y])
            
            new_pts.extend([A, p1, p2, p3])
        pts = np.array(new_pts)
        
    return pts

# Pre-cache the massive geometry vector (3,072 bounds per layer)
BASE_RADIUS = 350.0
KOCH_PTS = generate_koch_snowflake(BASE_RADIUS, depth=5)

def render_frame(packet):
    f, phase_ratio = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    
    # Lock coordinate Bounding Box to precise center
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)

    # 1. INFINITE CONCENTRIC TENSOR (The Logarithmic Zoom)
    # We iterate from massive external structural bounds downwards into the sub-pixel core.
    layers = range(-2, 7) # -2 is extreme macro, 6 is sub-pixel micro
    
    for k in layers:
        # The 3.0 base ensures the fractal boundaries math is locked identically
        scale = 3.0 ** (phase_ratio - k)
        scaled_pts = KOCH_PTS * scale
        
        # Industrial Drop Shadow
        y_offset = -40 * scale
        y_depth  = -70 * scale
        
        # Core Void Shadow (Provides depth to the underlying plates)
        # Z-INDEX HOTFIX: k + 10 ensures smaller layers render ON TOP of massive layers.
        shadow_deep = patches.Polygon(scaled_pts + np.array([0, y_depth]), facecolor=C_DARK, zorder=k + 10 - 0.2, alpha=0.4)
        ax.add_patch(shadow_deep)
        
        # Primary Mechanical Steel Edge
        shadow = patches.Polygon(scaled_pts + np.array([0, y_offset]), facecolor=C_STEEL, zorder=k + 10 - 0.1)
        ax.add_patch(shadow)
        
        # Daylight Face Plate (Solid mass covering everything below it)
        face_plate = patches.Polygon(scaled_pts, facecolor=C_TITANIUM, edgecolor=C_TEXT, lw=1.5 * scale, zorder=k + 10)
        ax.add_patch(face_plate)

        # C_GOLD Geometric Bounding Circumcircle (Tracks the macro-boundary)
        circ = patches.Circle((0,0), radius=BASE_RADIUS * scale, facecolor='none', edgecolor=C_GOLD, lw=0.5 * scale, alpha=0.3, zorder=k + 10 + 0.5)
        ax.add_patch(circ)

    # 2. STATIC KINEMATIC TETHERING (Laser tracking aligning the matrix)
    for angle_deg in range(30, 360, 60):
        rad = np.radians(angle_deg)
        length = 1500
        ax.plot([0, length*np.cos(rad)], [0, length*np.sin(rad)], color=C_CYAN, lw=2, alpha=0.5, zorder=70)

    # 3. ZERO-TEMPERATURE WIDGETS
    ax.text(-500, 880, "LG-320 :: KOCH SNOWFLAKE TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, 840, "[SFI-1.00] INFINITE RECURSION // MEGASCAE ARCHITECTURE", color=C_TEXT, fontsize=12, fontname='monospace', zorder=80)
    
    # Telemetry Dynamics
    ax.text(-500, -840, "LOGARITHMIC KINEMATICS // CONSTANT 3X DRIFT", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=80)
    ax.add_patch(patches.Rectangle((-500, -860), 1000, 4, facecolor=C_TITANIUM, zorder=80))
    ax.add_patch(patches.Rectangle((-500, -860), 1000 * phase_ratio, 4, facecolor=C_GOLD, zorder=81))

    # Algorithmic Readouts
    ax.text(-500, -780, f"STRUCTURAL DELTA: Δ{phase_ratio:.4f}", color=C_TEXT, fontsize=12, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, -805, "INTEGER WRAP: LOCKED ON FRAME 600", color=C_CYAN, fontsize=10, fontname='monospace', zorder=80)

    # Singularities Indicator
    ax.add_patch(patches.Circle((0, 0), radius=4, color=C_MAGENTA, zorder=80))
    ax.text(20, -10, "ABSOLUTE\nZERO POINT\nSINGULARITY", color=C_TEXT, fontsize=8, fontname='monospace', weight='bold', zorder=80)
    ax.plot([10, 40], [0, 0], color=C_TEXT, lw=1, zorder=80)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0)
    fig.clf(); plt.close(fig); gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-320: RECURSIVE FRACTAL TENSOR [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
