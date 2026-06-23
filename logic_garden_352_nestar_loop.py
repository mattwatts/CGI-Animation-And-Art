"""
SOVEREIGN CODE: logic_garden_352_nestar_loop.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 352 (Gravastar / Nestar // The Seamless Vacuum Loop)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ASTROPHYSICS, ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Seamless 20.0s Exponential Loop. Custom Horizon Z-Clipping. Daylight Protocol.
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

# ======== ARCHITECT CONDITIONAL LOGIC ========
DURATION = 20.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_352_nestar_loop"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Blueprint / Domain Floor
C_STEEL     = '#606065'   # The Rigid Exotic Matter Binding
C_CYAN      = '#00FFFF'   # The Thin-Shell Horizon Array
C_MANTIS    = '#00FF00'   # The de Sitter Vacuum Core (High Density)
C_DARK      = '#202025'   # Internal Void Space
C_VOID_WALL = '#F2F2F5'   # Translucent Horizon Wall 

# ------------------------------------------------------------------
# O(1) KINEMATIC ENGINE: EXPONENTIAL ZOOM & HORIZON CLIPPING
# ------------------------------------------------------------------
R_BASE = 250.0       # The base radius of Gravastar n=0
SCALE_RATIO = 6.0    # The scaling factor connecting the nested stars
Z_CLIP_START = -250  # Z-coordinate where the shell begins to fracture (Aperutre opens)
Z_CLIP_END = -450    # Z-coordinate where shell is mathematically unrendered (Passed)

def rotate_x(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])

def rotate_y(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])

def rotate_z(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

# Generate O(1) Spherical Basis Matrices (Radius 1.0)
def generate_unit_sphere(lats=16, lons=32):
    quads = []
    lat = np.linspace(-np.pi/2, np.pi/2, lats)
    lon = np.linspace(0, 2*np.pi, lons)
    for i in range(lats-1):
        for j in range(lons-1):
            v1 = [np.cos(lat[i])*np.sin(lon[j]), np.sin(lat[i]), np.cos(lat[i])*np.cos(lon[j])]
            v2 = [np.cos(lat[i+1])*np.sin(lon[j]), np.sin(lat[i+1]), np.cos(lat[i+1])*np.cos(lon[j])]
            v3 = [np.cos(lat[i+1])*np.sin(lon[j+1]), np.sin(lat[i+1]), np.cos(lat[i+1])*np.cos(lon[j+1])]
            v4 = [np.cos(lat[i])*np.sin(lon[j+1]), np.sin(lat[i]), np.cos(lat[i])*np.cos(lon[j+1])]
            quads.append(np.array([v1, v2, v3, v4]))
    return np.array(quads)

def generate_unit_accretion_disk(r_in=1.1, r_out=1.4, segments=40):
    quads = []
    ths = np.linspace(0, 2*np.pi, segments)
    for i in range(len(ths)-1):
        a1, a2 = ths[i], ths[i+1]
        v1 = [r_in*np.cos(a1), 0, r_in*np.sin(a1)]
        v2 = [r_out*np.cos(a1), 0, r_out*np.sin(a1)]
        v3 = [r_out*np.cos(a2), 0, r_out*np.sin(a2)]
        v4 = [r_in*np.cos(a2), 0, r_in*np.sin(a2)]
        quads.append(np.array([v1, v2, v3, v4]))
    return np.array(quads)

# Base Unity Structures
UNIT_SHELL = generate_unit_sphere(16, 32)
UNIT_VACUUM = generate_unit_sphere(8, 16) # Denser, smaller inner polys
UNIT_DISK = generate_unit_accretion_disk(1.05, 1.25, 48)

LIGHT_DIR = np.array([0.5, 0.7, 0.3])
LIGHT_DIR = LIGHT_DIR / np.linalg.norm(LIGHT_DIR)

def get_ambient_shade(base_hex, obj_norm, min_amb=0.4):
    rgb = np.array(mcolors.to_rgb(base_hex))
    diffuse = abs(np.dot(obj_norm, LIGHT_DIR)) # Abs ensures inside walls render
    return np.clip(rgb * (min_amb + (1.0 - min_amb)*diffuse), 0, 1)

def render_frame(packet):
    f, phase_ratio = packet
    # The exponential zooming factor guarantees geometric continuity
    zoom_scale = SCALE_RATIO ** phase_ratio  
    t_rot_angle = phase_ratio * 2.0 * np.pi  # Exact 360-degree lock over the loop

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # CAMERA LOCK
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)
    ax.autoscale(False)

    # 1. KINEMATIC CAMERA MATRIX
    # --------------------------
    # Static off-axis pitch gives volume; dynamic continuous yaw ensures topological sweep
    sys_rotation = rotate_x(np.radians(-25)) @ rotate_y(t_rot_angle) @ rotate_z(np.radians(15))
    render_queue = []

    def push_geometry(geom_array, sys_M, scale, fc_hex, ec_hex, lw_base, alpha_base, culling=False):
        for quad in geom_array:
            proj = np.dot(quad * scale, sys_M.T)
            depth = np.mean(proj[:, 2])
            
            # The Horizon Fracture Algorithm (Simulated Z-Aperture Clipping)
            # If coordinates slam past the camera plane, they aggressively phase out
            # revealing the nested metric inside.
            horizon_alpha_mult = np.clip((depth - Z_CLIP_END) / (Z_CLIP_START - Z_CLIP_END), 0.0, 1.0)
            final_a = alpha_base * horizon_alpha_mult
            
            if final_a < 0.02:
                continue

            v1, v2, v3, v4 = proj
            nrm = np.cross(v2 - v1, v4 - v1)
            mag = np.linalg.norm(nrm)
            if mag > 0: nrm = nrm / mag
            else: nrm = np.array([0,1,0])

            # Standard Backface Cull (For the dense solid interior core)
            if culling and nrm[2] < 0:
                continue
                
            fc_safe = mcolors.to_rgba(get_ambient_shade(fc_hex, nrm), np.clip(final_a, 0, 1))
            ec_safe = mcolors.to_rgba(ec_hex, np.clip(final_a * 1.5, 0, 1))
            
            screen_quad = np.column_stack((proj[:, 0], proj[:, 1]))
            render_queue.append({'d': depth, 'poly': screen_quad, 'fc': fc_safe, 'ec': ec_safe, 'l': lw_base})

    # 2. NESTED MATRIX INGESTION
    # --------------------------
    # Loop over topological depths. 
    # n = -1 is the immense bounding box we are inside.
    # n =  0 is the primary targeting shell.
    # n =  1 is the Nestar forming deep in the vacuum.
    for n in range(-1, 3):
        # Calculate current topological scale
        R_n = R_BASE * (SCALE_RATIO ** -n) * zoom_scale
        
        # Purge logic: If the nestar is too small to render, skip to save O(N) overhead
        if R_n < 2.0 or R_n > 5000.0:
            continue
            
        # A. The Thin-Shell Exotic Matter Bound (The Horizon)
        # Opaque enough to hide the nested void until strictly breached
        push_geometry(UNIT_SHELL, sys_rotation, R_n, C_VOID_WALL, C_CYAN, 1.0, 0.8, culling=False)
        
        # B. The de Sitter High-Density Vacuum Core (Terminal Green)
        # Sits tightly at the center of the local metric
        push_geometry(UNIT_VACUUM, sys_rotation, R_n * 0.15, C_MANTIS, C_TEXT, 1.0, 1.0, culling=True)
        
        # C. The Baryonic Accretion Limit
        # Ensures absolute tracking of spatial orientation
        push_geometry(UNIT_DISK, sys_rotation, R_n, C_TITANIUM, C_STEEL, 1.5, 0.6, culling=False)

    # 3. ABSOLUTE Z-SORT RENDERING DISPATCH
    # -------------------------------------
    render_queue.sort(key=lambda item: item['d'], reverse=True) 
    
    for item in render_queue:
        ax.add_patch(patches.Polygon(item['poly'], facecolor=item['fc'], edgecolor=item['ec'], lw=item['l'], zorder=50))
        
    # Friction Spallation Array (Stochastic Dust on the Matrix)
    np.random.seed(int(f/5)) # Rapid shimmering effect
    for _ in range(8):
        sx, sy = np.random.uniform(-400, 400), np.random.uniform(-400, 400)
        ax.scatter(sx, sy, color=C_STEEL, s=np.random.uniform(5, 15), alpha=np.random.uniform(0.1, 0.4), zorder=60)

    # ====================================================
    # 4. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)

    ax.text(-500, 890, "LG-352 :: THE NESTAR // GRAVASTAR METRIC", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-0.75] SEAMLESS DE SITTER VACUUM KINEMATICS", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    s_scale = f"Z-MULTIPLIER: {zoom_scale:05.2f}X"

    ax.text(-500, -760, "SYS_01 [OUTER METRIC]        :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, "B.E.C. EXOTIC MATTER / RIGID TOPOLOGY", color=C_CYAN, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [INNER METRIC]        :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, "DE SITTER SPACE // 10^44 DENSITY", color=C_MANTIS, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "STRUCTURAL LOAD AUDIT        :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, f"PLUNGING HORIZON // {s_scale}", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider (Perfect Tuple)
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=C_CYAN, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close('all')
    gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-352: NESTAR LOOP [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
