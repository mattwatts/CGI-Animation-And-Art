"""
SOVEREIGN CODE: logic_garden_351b_open_mapping.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 351b (Open Mapping Theorem & Bounded Inverse)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: FUNCTIONAL ANALYSIS, ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Linear 24.0s Sequence. Daylight Protocol. Custom Z-Sorting. Matrix Interpolation.
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
DURATION = 24.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_351b_open_mapping"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Blueprint / Axes
C_STEEL     = '#606065'   # Structural Mesh
C_CYAN      = '#00FFFF'   # The Open Set in Banach Space X
C_MAGENTA   = '#DE008A'   # The Kinetic Shear Force
C_MANTIS    = '#00FF00'   # The Open Map Proof (Inner Ball in Y)
C_GOLD      = '#FFB300'   # The Bounded Inverse Proof (Mapped back to X)

# ------------------------------------------------------------------
# O(1) ORTHOGRAPHIC PROJECTION ENGINE & MATRICES
# ------------------------------------------------------------------
def rotate_x(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])

def rotate_y(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])

def rotate_z(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

def ease_in_out(t):
    t = np.clip(t, 0.0, 1.0)
    return 4 * t**3 if t < 0.5 else 1 - (-2 * t + 2)**3 / 2

# The Bounded Linear Operator T (Surjective & Bijective)
T_OP = np.array([
    [ 1.8,  0.5,  0.0],
    [-0.3,  1.1,  0.4],
    [ 0.2, -0.4,  0.8]
])
# The Bounded Inverse Operator T^-1
T_INV = np.linalg.inv(T_OP)

# Geometry Generators
def generate_sphere(radius, lats=16, lons=32):
    quads = []
    lat = np.linspace(-np.pi/2, np.pi/2, lats)
    lon = np.linspace(0, 2*np.pi, lons)
    for i in range(lats-1):
        for j in range(lons-1):
            v1 = [radius*np.cos(lat[i])*np.sin(lon[j]), radius*np.sin(lat[i]), radius*np.cos(lat[i])*np.cos(lon[j])]
            v2 = [radius*np.cos(lat[i+1])*np.sin(lon[j]), radius*np.sin(lat[i+1]), radius*np.cos(lat[i+1])*np.cos(lon[j])]
            v3 = [radius*np.cos(lat[i+1])*np.sin(lon[j+1]), radius*np.sin(lat[i+1]), radius*np.cos(lat[i+1])*np.cos(lon[j+1])]
            v4 = [radius*np.cos(lat[i])*np.sin(lon[j+1]), radius*np.sin(lat[i]), radius*np.cos(lat[i])*np.cos(lon[j+1])]
            quads.append(np.array([v1, v2, v3, v4]))
    return np.array(quads)

# Base Geometries
R_OUTER = 300
R_INNER = 100 # Mathematically tailored to fit inside the deformed ellipsoid of T_OP
BASE_SPHERE = generate_sphere(R_OUTER)
INNER_SPHERE = generate_sphere(R_INNER)

LIGHT_DIR = np.array([0.4, 0.7, 0.5])
LIGHT_DIR = LIGHT_DIR / np.linalg.norm(LIGHT_DIR)

def get_shaded_color(base_hex, intensity):
    rgb = np.array(mcolors.to_rgb(base_hex))
    ambient = 0.2
    diffuse = 0.8 * intensity
    return np.clip(rgb * (ambient + diffuse), 0, 1)

def draw_industrial_grid(ax):
    for i in range(-5, 6):
        ax.plot([i*100, i*100], [-960, 960], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)
    for j in range(-9, 10):
        ax.plot([-540, 540], [j*100, j*100], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)

def render_frame(packet):
    f, phase_ratio = packet
    t = phase_ratio * DURATION

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
    draw_industrial_grid(ax)

    # 1. TIMELINE & MATRIX MORPH LOGIC
    # --------------------------------
    T_PHASE1 = 4.0   # End setup
    T_PHASE2 = 10.0  # End T Transform
    T_PHASE3 = 16.0  # End Inner Ball Proof
    T_PHASE4 = 21.0  # End T^-1 Transform

    current_mat = np.eye(3)
    c_outer = C_CYAN
    a_outer = 0.85
    c_inner = C_MANTIS
    scale_inner = 0.0

    # Phase 2: Morph to Operator T
    if t > T_PHASE1 and t <= T_PHASE2:
        prg = ease_in_out((t - T_PHASE1) / (T_PHASE2 - T_PHASE1))
        current_mat = (1.0 - prg) * np.eye(3) + prg * T_OP
        a_outer = 0.85 - (0.5 * prg) # Becomes more translucent to reveal interior
        
    # Phase 3: Hold T, expand inner Mantis ball
    elif t > T_PHASE2 and t <= T_PHASE3:
        current_mat = T_OP
        a_outer = 0.35
        prg2 = ease_in_out((t - T_PHASE2) / (T_PHASE3 - T_PHASE2))
        scale_inner = prg2
        
    # Phase 4: Execute Bounded Inverse (Morph space back to Identity)
    elif t > T_PHASE3:
        prg3 = ease_in_out(min(1.0, (t - T_PHASE3) / (T_PHASE4 - T_PHASE3)))
        # Moving backwards through T^-1 is mathematically equivalent to returning to I
        current_mat = (1.0 - prg3) * T_OP + prg3 * np.eye(3)
        scale_inner = 1.0
        a_outer = 0.35 + (0.5 * prg3)
        # Inner ball geometrically maps from MANTIS to GOLD as it shifts to Space X
        c_r = (1.0 - prg3) * np.array(mcolors.to_rgb(C_MANTIS)) + prg3 * np.array(mcolors.to_rgb(C_GOLD))
        c_inner = mcolors.to_hex(np.clip(c_r, 0, 1))

    # 2. CAMERA AND Z-SORT QUEUE
    # --------------------------
    sys_rotation = rotate_x(np.radians(-20)) @ rotate_y(t * 0.5) @ rotate_z(np.radians(15))
    render_queue = []

    def push_sphere(geom_quads, T_matrix, base_color, alpha_val, scale=1.0):
        safe_a = np.clip(alpha_val, 0.0, 1.0)
        # O(1) Matrix multiplier pipeline
        combined_matrix = T_matrix @ sys_rotation.T
        
        for quad in geom_quads:
            scaled_quad = quad * scale
            # Affine translation
            proj = np.dot(scaled_quad, combined_matrix)
            
            # Surface Normal Calculation for Shading (Post T-Matrix transform!)
            v1, v2, v3, v4 = proj
            face_normal = np.cross(v2 - v1, v4 - v1)
            mag = np.linalg.norm(face_normal)
            if mag == 0: continue
            face_normal = face_normal / mag
            
            # Backface cull
            if face_normal[2] < -0.1:
                continue
                
            intensity = max(0, np.dot(face_normal, LIGHT_DIR))
            final_c = get_shaded_color(base_color, intensity)
            
            depth = np.mean(proj[:, 2])
            screen_quad = np.column_stack((proj[:, 0], proj[:, 1]))
            
            render_queue.append({
                'd': depth, 
                'poly': screen_quad, 
                'fc': mcolors.to_rgba(final_c, safe_a), 
                'ec': mcolors.to_rgba(final_c, np.clip(safe_a*1.2, 0, 1)), 
                'lw': 0.5 if safe_a > 0.5 else 1.5,
                'a': safe_a
            })

    # Render Geometries
    push_sphere(BASE_SPHERE, current_mat, c_outer, a_outer)
    if scale_inner > 0.01:
        push_sphere(INNER_SPHERE, current_mat, c_inner, 0.95, scale=scale_inner)

    # Z-Sort strictly by depth (lowest Z rendered first)
    render_queue.sort(key=lambda item: item['d']) 

    for item in render_queue:
        ax.add_patch(patches.Polygon(item['poly'], facecolor=item['fc'], edgecolor=item['ec'], lw=item['lw'], zorder=50))
        
    # Cartesian Axes Tracking the Shear
    origin = np.dot([0,0,0], current_mat @ sys_rotation.T)
    x_ax = np.dot([400,0,0], current_mat @ sys_rotation.T)
    y_ax = np.dot([0,400,0], current_mat @ sys_rotation.T)
    z_ax = np.dot([0,0,400], current_mat @ sys_rotation.T)
    
    ax.plot([origin[0], x_ax[0]], [origin[1], x_ax[1]], color=C_STEEL, lw=3, zorder=20)
    ax.plot([origin[0], y_ax[0]], [origin[1], y_ax[1]], color=C_STEEL, lw=3, zorder=20)
    ax.plot([origin[0], z_ax[0]], [origin[1], z_ax[1]], color=C_STEEL, lw=3, zorder=20)

    # Friction spallation during transformation
    if (t > T_PHASE1 and t < T_PHASE2) or (t > T_PHASE3 and t < T_PHASE4):
        for _ in range(3):
            sx, sy = np.random.uniform(-400, 400), np.random.uniform(-400, 400)
            ax.scatter(sx, sy, facecolor='none', edgecolor=C_MAGENTA, s=np.random.uniform(20, 80), alpha=0.5, lw=2, zorder=90)

    # ====================================================
    # 3. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)

    ax.text(-500, 890, "LG-351b :: THE BANACH-SCHAUDER THEOREM", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] OPEN MAPPING // THE BOUNDED INVERSE", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    # Telemetry State Logic
    if t < T_PHASE1:
        s1, c1 = "BANACH SPACE X [BASEPLATE SECURED]", C_STEEL
        s2, c2 = "UNIT OPEN BALL INITIALIZED", C_CYAN
        t_state = "AWAITING OPERATOR MATRIX EXECUTION"
    elif t < T_PHASE2:
        s1, c1 = "EXECUTING SURJECTIVE LINEAR OPERATOR T", C_MAGENTA
        s2, c2 = "O(1) AFFINE TOPOLOGICAL SHEAR", C_TEXT
        t_state = "TRANSLATING TO BANACH SPACE Y..."
    elif t < T_PHASE3:
        s1, c1 = "BANACH SPACE Y [TOPOLOGY SHEARED]", C_STEEL
        s2, c2 = "OPEN MAPPING THEOREM PROOF", C_MANTIS
        t_state = "INNER C_MANTIS BALL PROVES Z-AXIS WAS NOT CRUSHED"
    else:
        s1, c1 = "EXECUTING BOUNDED INVERSE T^-1", C_GOLD
        s2, c2 = "THE BOOMERANG TENSOR [MAPPING BACK TO X]", C_CYAN
        t_state = "INVERSE TOPOLOGY SECURE // DID NOT EXPLODE TO INFINITY"

    ax.text(-500, -760, "SYS_01 [GEOMETRIC STATE]     :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, s1, color=c1, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [DATA INGESTION]      :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, s2, color=c2, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "STRUCTURAL LOAD AUDIT        :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, t_state, color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider [Strict Tuples]
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=c1, zorder=83))

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
    print(f"LG-351b: BANACH-SCHAUDER THEOREM [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
