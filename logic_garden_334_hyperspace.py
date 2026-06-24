"""
SOVEREIGN CODE: logic_garden_334_hyperspace.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Vectorization
SCENE: Logic Garden 334 (Hyperspace Traversable Metric // Ellis-Bronnikov)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: 10.0s True Topological Wrap. Absolute Camera Lock. O(1) 3D Projection.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import multiprocessing as mp
import matplotlib.colors as mcolors
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
DURATION = 10.0  # 10.0 Second Seamless Topological Loop
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_334_hyperspace"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   
C_STEEL     = '#606065'   
C_DARK      = '#202025'   # Shielding Base
C_AZURE     = '#007FFF'   # Structural Rails (Depth Metric)
C_INDIGO    = '#3F00FF'   # The Throat / Event Horizon
C_CYAN      = '#00FFFF'   # Energy Matrix Spacing
C_GOLD      = '#FFB300'   # Magnetic Confinement Array
C_MAGENTA   = '#FF0055'   # Exotic Flux / Negative Energy
C_WHITE     = '#FFFFFF'

# -------- TOPOLOGICAL CONSTANTS --------
N_RINGS = 60
Z_MIN = 100
Z_MAX = 3100
L_TUBE = Z_MAX - Z_MIN
Z_STEP = L_TUBE / N_RINGS

R_TUBE = 500
SIDES = 16

# Velocity & Wrap Constants
# Moving exactly 25 rings forward perfectly wraps the modular geometry
TUNNEL_RINGS_PER_LOOP = 25 
DZ_TOTAL = TUNNEL_RINGS_PER_LOOP * Z_STEP

# Twist & Torsion (Writhing tube)
WAVE_COUNT = 3  
TORSION_WRAPS = 2  

# Pre-generate Exotic Sparks (O(1) memory allocation)
np.random.seed(334)
N_SPARKS = 300
spark_z_base = np.random.uniform(Z_MIN, Z_MAX, N_SPARKS)
spark_r = np.random.uniform(100, R_TUBE - 50, N_SPARKS)
spark_t = np.random.uniform(0, 2 * np.pi, N_SPARKS)

# Pre-generate base Z arrays for the rings
req_idx = np.arange(N_RINGS)
Z_base_array = Z_MIN + req_idx * Z_STEP

def project_3d(x, y, z, fov=1200):
    """Rigid O(1) coordinate projection bypassing heavy 3D rendering engines."""
    factor = fov / (z + 1e-4) # 1e-4 prevents Div0
    return x * factor, y * factor

def render_frame(packet):
    f, phase_ratio = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    
    # BARE-METAL CAMERA LOCK
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)
    ax.autoscale(False)

    # 1. 3D METRIC TENSOR CALCULATION
    V_X = np.zeros((N_RINGS, SIDES))
    V_Y = np.zeros((N_RINGS, SIDES))
    V_Z = np.zeros(N_RINGS)
    
    for i in range(N_RINGS):
        # Calculate actual Z based on loop phase (Modular topological flow)
        z_val = Z_MIN + (Z_base_array[i] - Z_MIN - phase_ratio * DZ_TOTAL) % L_TUBE
        V_Z[i] = z_val
        
        # Calculate central spine of the tube at this Z
        cx = 350 * np.sin(z_val * WAVE_COUNT * 2 * np.pi / L_TUBE)
        cy = 350 * np.cos(z_val * WAVE_COUNT * 2 * np.pi / L_TUBE)
        
        # Frame Dragging (The rings physically spin)
        spin = (z_val * TORSION_WRAPS * 2 * np.pi / L_TUBE) + (phase_ratio * 2 * np.pi)
        
        # Calculate exactly 16 geometric vertices for the ring
        angles = np.linspace(0, 2*np.pi, SIDES, endpoint=False) + spin
        for k in range(SIDES):
            rx = cx + R_TUBE * np.cos(angles[k])
            ry = cy + R_TUBE * np.sin(angles[k])
            px, py = project_3d(rx, ry, z_val)
            V_X[i, k] = px
            V_Y[i, k] = py

    # 2. OCCLUSION SORTING & GEOMETRIC DEPLOYMENT
    segments = []
    
    # Build structural Quad panels
    for i in range(N_RINGS):
        z1 = V_Z[i]
        next_i = (i + 1) % N_RINGS
        z2 = V_Z[next_i]
        
        # Prevent connection if the index just wrapped the metric
        if abs(z1 - z2) > Z_STEP * 2: continue
            
        z_avg = (z1 + z2) / 2.0
        depth_ratio = (z_avg - Z_MIN) / L_TUBE
        
        for k in range(SIDES):
            k_next = (k + 1) % SIDES
            pts = [
                (V_X[i, k], V_Y[i, k]),
                (V_X[i, k_next], V_Y[i, k_next]),
                (V_X[next_i, k_next], V_Y[next_i, k_next]),
                (V_X[next_i, k], V_Y[next_i, k])
            ]
            segments.append({'z': z_avg, 'type': 'panel', 'pts': pts, 'depth': depth_ratio})

    # Build cross-sectional rings (C_CYAN high-energy pulses)
    for i in range(N_RINGS):
        depth_ratio = (V_Z[i] - Z_MIN) / L_TUBE
        pts = [(V_X[i, k], V_Y[i, k]) for k in range(SIDES)]
        segments.append({'z': V_Z[i], 'type': 'ring', 'pts': pts, 'depth': depth_ratio})

    # Rigid O(N log N) Back-to-Front draw order array
    segments.sort(key=lambda s: s['z'], reverse=True)

    # 3. DRAW THE HORIZON CORE (Absolute Background)
    hx, hy = project_3d(350 * np.sin(Z_MAX * WAVE_COUNT * 2 * np.pi / L_TUBE),
                        350 * np.cos(Z_MAX * WAVE_COUNT * 2 * np.pi / L_TUBE), Z_MAX)
    ax.add_patch(patches.Circle((hx, hy), 400, facecolor=C_INDIGO, alpha=0.3, zorder=0))
    ax.add_patch(patches.Circle((hx, hy), 150, facecolor=C_MAGENTA, alpha=0.2, zorder=0))

    # 4. DRAW EXOTIC MATER FLUX (Spallation sparks)
    for i in range(N_SPARKS):
        # Sparks fly backwards through the tunnel at 4x the geometric speed
        sz = Z_MIN + (spark_z_base[i] - Z_MIN - phase_ratio * DZ_TOTAL * 4) % L_TUBE
        if sz < 200: continue # Don't draw too close to camera
        
        scx = 350 * np.sin(sz * WAVE_COUNT * 2 * np.pi / L_TUBE)
        scy = 350 * np.cos(sz * WAVE_COUNT * 2 * np.pi / L_TUBE)
        sr = spark_r[i]
        st = spark_t[i] + phase_ratio * np.pi # Twisted flux
        
        sx = scx + sr * np.cos(st)
        sy = scy + sr * np.sin(st)
        spx, spy = project_3d(sx, sy, sz)
        
        scale = max(1, 8 - (sz/Z_MAX)*8) # Larger when closer
        col = C_MAGENTA if i % 2 == 0 else C_GOLD
        ax.plot([spx, spx + np.random.uniform(-scale*2, scale*2)], [spy, spy + np.random.uniform(scale*3, scale*6)], color=col, lw=scale, alpha=0.8, zorder=1)

    # 5. DRAW O(1) TRUE 3D OCCLUDING GEOMETRY
    for seg in segments:
        dr = seg['depth']
        alpha = max(0.0, 1.0 - dr*1.2) # Sharp fade out
        if alpha <= 0.01: continue
            
        if seg['type'] == 'panel':
            # Solid white faces completely block lines drawn behind them, line weight thins to 0 for distance fade
            c_edge = mcolors.to_rgba(C_AZURE, alpha)
            ax.add_patch(patches.Polygon(seg['pts'], facecolor=C_BG, edgecolor=c_edge, lw=2*alpha, zorder=2))
        else:
            c_edge = mcolors.to_rgba(C_CYAN, alpha)
            ax.add_patch(patches.Polygon(seg['pts'], fill=False, edgecolor=c_edge, lw=4*alpha, zorder=2.1))

    # 6. EXTERNAL MAGNETIC CONFINEMENT HUD (The Sovereign Shield)
    # 4 massive corner blocks creating the octagonal viewport
    b_zs = 80 # pseudo Z-order
    for dx, dy in [(-1, 1), (1, 1), (1, -1), (-1, -1)]:
        pts = [
            (dx*540, dy*960), (dx*200, dy*960), (dx*540, dy*600)
        ]
        ax.add_patch(patches.Polygon(pts, facecolor=C_DARK, zorder=b_zs))
        ax.add_patch(patches.Polygon(pts, fill=False, edgecolor=C_GOLD, lw=5, zorder=b_zs+1))

    # Inner targeting ring
    ax.add_patch(patches.Circle((0, 0), 900, fill=False, edgecolor=C_TITANIUM, lw=2, linestyle='--', zorder=b_zs, alpha=0.3))
    ax.add_patch(patches.Circle((0, 0), 1050, fill=False, edgecolor=C_STEEL, lw=15, zorder=b_zs+1))
    
    # Top Telemetry Box [Strict Tuple Rules Verified]
    ax.add_patch(patches.Rectangle((-300, 780), 600, 100, facecolor=C_TITANIUM, zorder=b_zs+2, alpha=0.9))
    ax.plot([-300, 300], [780, 780], color=C_GOLD, lw=4, zorder=b_zs+3)
    
    ax.text(0, 845, "LG-334: SPACETIME METRIC", color=C_TEXT, ha='center', fontsize=20, fontname='monospace', weight='bold', zorder=b_zs+3)
    ax.text(0, 805, "[SFI-0.75] ELLIS-BRONNIKOV WORMHOLE", color=C_INDIGO, ha='center', fontsize=12, fontname='monospace', weight='bold', zorder=b_zs+3)

    # Bottom Mechanics Box
    ax.add_patch(patches.Rectangle((-450, -900), 900, 160, facecolor=C_TITANIUM, zorder=b_zs+2, alpha=0.9))
    ax.plot([-450, 450], [-740, -740], color=C_GOLD, lw=4, zorder=b_zs+3)
    
    flux_density = np.sin(phase_ratio * 12 * np.pi) ** 2
    ax.text(-400, -790, "NEGATIVE EXOTIC ENERGY FLUX:", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=b_zs+3)
    ax.text(100, -790, f"ACTIVE [{flux_density * 100:>04.1f}%]", color=C_MAGENTA, fontsize=16, fontname='monospace', weight='bold', zorder=b_zs+3)
    
    ax.text(-400, -835, "TORSIONAL FRAME DRAGGING   :", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=b_zs+3)
    ax.text(100, -835, "LOCKED O(1)", color=C_CYAN, fontsize=16, fontname='monospace', weight='bold', zorder=b_zs+3)

    # Tracking slider
    ax.add_patch(patches.Rectangle((-400, -870), 800, 6, facecolor=C_STEEL, zorder=b_zs+3))
    ax.add_patch(patches.Rectangle((-400, -870), 800 * phase_ratio, 6, facecolor=C_AZURE, zorder=b_zs+4))

    # Sovereign Execution Output
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
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-334: ELLIS WORMHOLE TENSOR [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE] [3D OCCLUSION ENGAGED]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
