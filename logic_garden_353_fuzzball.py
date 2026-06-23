"""
SOVEREIGN CODE: logic_garden_353_fuzzball.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 353 (The Fuzzball Matrix // Singularity Override)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ASTROPHYSICS, STRING THEORY, KINEMATIC ENGINEERING
HOTFIX: Exact 24.0s Seamless Loop. Custom Z-Sorting Line Segments. Daylight Protocol.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors  # WELDED TO BASEPLATE
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
DURATION = 24.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_353_fuzzball"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Blueprint / Environment Grid
C_STEEL     = '#606065'   # The Schwarzschild Geometric Shell
C_CYAN      = '#00FFFF'   # Cold Strings (Outer Boundary)
C_MANTIS    = '#00FF00'   # Theorem Lock / Terminal Green Frame
C_GOLD      = '#FFB300'   # High-Energy Metric Boundary
C_MAGENTA   = '#DE008A'   # Deep Core Spallation (String Collisions)

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

# ------------------------------------------------------------------
# STRING MATRIX (FUZZBALL TOPOLOGY) GENERATOR
# ------------------------------------------------------------------
R_HORIZON = 380.0
N_STRINGS = 250
PTS_PER_STRING = 45 # O(1) balance for the Executioner Protocol (11,000 vertices total)

np.random.seed(353)

# O(1) Parametric Arrays for String Orbits
# Each string is a closed loop circle in 3D that heavily vibrates orthogonally
string_params = []
for _ in range(N_STRINGS):
    r_base = np.random.uniform(0.15, 0.95) * R_HORIZON
    
    # Random orthogonal plane (u, v) and normal (n)
    n = np.random.randn(3)
    n /= np.linalg.norm(n)
    u = np.cross(n, np.array([0, 1, 0]) if abs(n[1]) < 0.9 else np.array([1, 0, 0]))
    u /= np.linalg.norm(u)
    v = np.cross(n, u)
    
    # Vibration parameters (integer waves to guarantee seamless loop closure)
    wave_k1 = np.random.randint(2, 7)
    wave_k2 = np.random.randint(3, 10)
    phase_1 = np.random.uniform(0, 2*np.pi)
    phase_2 = np.random.uniform(0, 2*np.pi)
    
    # Spin multiplier maps vibration speed to the 24s loop exactly
    freq_mult = np.random.randint(1, 4) * 2.0 * np.pi 
    
    # Amp decays strongly near the horizon so they don't break the Bounding Box
    amp = (1.0 - (r_base / R_HORIZON)**2) * 50.0 
    
    color_hex = C_CYAN
    if r_base < R_HORIZON * 0.4:
        color_hex = C_MAGENTA
    elif r_base < R_HORIZON * 0.7:
        if np.random.rand() > 0.5: color_hex = C_GOLD
        
    string_params.append({
        'r': r_base, 'u': u, 'v': v, 'n': n,
        'k1': wave_k1, 'k2': wave_k2, 'p1': phase_1, 'p2': phase_2,
        'fm': freq_mult, 'amp': amp, 'color': color_hex
    })

# The Horizon Ghost Array
horizon_quads = []
lats = np.linspace(-np.pi/2, np.pi/2, 12)
lons = np.linspace(0, 2*np.pi, 24)
for i in range(len(lats)-1):
    for j in range(len(lons)-1):
        def surf(lat, lon): return [R_HORIZON*np.cos(lat)*np.sin(lon), R_HORIZON*np.sin(lat), R_HORIZON*np.cos(lat)*np.cos(lon)]
        horizon_quads.append([surf(lats[i], lons[j]), surf(lats[i+1], lons[j]), surf(lats[i+1], lons[j+1]), surf(lats[i], lons[j+1])])
horizon_quads = np.array(horizon_quads)

def draw_industrial_grid(ax):
    for i in range(-5, 6):
        ax.plot([i*100, i*100], [-960, 960], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)
    for j in range(-9, 10):
        ax.plot([-540, 540], [j*100, j*100], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)

def render_frame(packet):
    f, phase_ratio = packet
    t_ratio = phase_ratio  # 0.0 to 1.0 exact

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

    # 1. KINEMATIC CAMERA MATRIX
    # --------------------------
    # Slowly plunging, rotating view to reveal 3D density
    pitch = -15 + 10 * np.sin(t_ratio * 2 * np.pi)
    yaw = t_ratio * 2 * np.pi
    
    sys_rotation = rotate_x(np.radians(pitch)) @ rotate_y(yaw) @ rotate_z(np.radians(10))
    y_shift = -50  
    
    render_queue = []

    # 2. HORIZON BOUNDARY RENDERING
    # -----------------------------
    for quad in horizon_quads:
        proj = np.dot(quad, sys_rotation.T)
        depth = np.mean(proj[:, 1])
        # Only draw the back wall of the ghost horizon to cradle the strings
        v1, v2, v3 = proj[0], proj[1], proj[2]
        nrm = np.cross(v2 - v1, v3 - v1)
        if nrm[2] > 0: # Backface relative to camera
            screen_quad = np.column_stack((proj[:, 0], proj[:, 2] + y_shift))
            render_queue.append({
                'type': 'poly', 'd': depth, 'poly': screen_quad,
                'fc': 'none', 'ec': mcolors.to_rgba(C_TITANIUM, 0.3), 'lw': 1.0
            })

    # 3. KINEMATIC STRING VIBRATION EVALUATION
    # ----------------------------------------
    theta_array = np.linspace(0, 2*np.pi, PTS_PER_STRING)
    
    for p in string_params:
        # Evaluate parametric equation over arc (theta) and time (t_ratio)
        # O(1) Matrix operations
        pts = np.outer(np.cos(theta_array), p['u']) * p['r'] + np.outer(np.sin(theta_array), p['v']) * p['r']
        
        # High-dimensional vibration pushing along the normal vector
        vib = p['amp'] * np.sin(p['k1'] * theta_array + p['p1'] + p['fm'] * t_ratio) * np.cos(p['k2'] * theta_array + p['p2'] - p['fm'] * t_ratio)
        pts += np.outer(vib, p['n'])
        
        # Rotate to camera
        proj = np.dot(pts, sys_rotation.T)
        
        # Chop into segments for perfect Z-sorting
        for i in range(PTS_PER_STRING - 1):
            seg_depth = (proj[i, 1] + proj[i+1, 1]) / 2.0
            # Alpha scales slightly by depth to enhance 3D overlap realism
            depth_alpha = np.clip((seg_depth + 400) / 800.0, 0.3, 0.95)
            
            # Hotter strings glow brighter
            final_a = depth_alpha if p['color'] == C_CYAN else depth_alpha * 0.9
            
            line_2d = np.column_stack((proj[i:i+2, 0], proj[i:i+2, 2] + y_shift))
            render_queue.append({
                'type': 'seg', 'd': seg_depth, 'line': line_2d, 
                'c': mcolors.to_rgba(p['color'], np.clip(final_a, 0, 1)), 
                'lw': 2.5 if p['color'] == C_MAGENTA else 1.5
            })

    # 4. ABSOLUTE Z-SORT RENDERING DISPATCH
    # -------------------------------------
    render_queue.sort(key=lambda item: item['d'], reverse=True) 
    
    for item in render_queue:
        if item['type'] == 'poly':
            ax.add_patch(patches.Polygon(item['poly'], facecolor='none', edgecolor=item['ec'], lw=item['lw'], zorder=50))
        elif item['type'] == 'seg':
            pts = item['line']
            ax.plot([pts[0][0], pts[1][0]], [pts[0][1], pts[1][1]], color=item['c'], lw=item['lw'], zorder=50)

    # ====================================================
    # 5. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)

    ax.text(-500, 890, "LG-353 :: THE FUZZBALL MATRICES", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-0.75] SINGULARITY OVERRIDE // QUANTUM STRING TOPOLOGY", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    pulse_sym = "||" if int(t_ratio * 40) % 2 == 0 else ">>"
    
    ax.text(-500, -760, "SYS_01 [TOPOLOGY BOUNDS]     :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, "SCHWARZSCHILD LIMIT SECURED // EXTREME EXTENDED OBJECT", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [THERMODYNAMICS]      :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, f"DIVIDE-BY-ZERO ANNIHILATED {pulse_sym} NO SINGULARITY", color=C_MANTIS, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "STRUCTURAL LOAD AUDIT        :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, "O(1) VIBRATING 1D TENSOR OVERLAP // C_MAGENTA SPALLATION", color=C_MAGENTA, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider
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
    print(f"LG-353: THE FUZZBALL MATRIX [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
