"""
PROJECT: Logic Garden 359b (The Inflationary Multiverse // Eternal Inflation)
FORMAT: YouTube Shorts (1080x1920)
METADATA: COSMOLOGY, BUBBLE UNIVERSES, STRING THEORY, INFLATION
EXECUTION: Continuous 24.0s Sequence. True 3D Particle & Topology Engine. Daylight Palette.
HOTFIX: Integrated lerp_color into global scope.
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

# ======== SEQUENCE PARAMETERS ========
DURATION = 24.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_359b_multiverse"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- VISUAL PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#E5E7EB'
C_INFLATON  = '#D1D5DB'   # The expanding background meta-vacuum
C_HORIZON   = '#9CA3AF'   # Translucent bubble boundary
C_UNI_A     = '#00D2FF'   # Universe A: Fine-Tuned (Cyan)
C_UNI_A_G   = '#FFB300'   # Universe A: Stars (Gold)
C_UNI_B     = '#DE008A'   # Universe B: High Gravity (Magenta)
C_UNI_C     = '#0044FF'   # Universe C: Heat Death/Expansion (Deep Azure)

# ------------------------------------------------------------------
# 3D PERSPECTIVE ENGINE 
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

def get_projection(pt_3d, focal_length=1500.0, cam_dist=1800.0):
    z_cam = pt_3d[2] + cam_dist
    if z_cam < 10: return None
    sx = (pt_3d[0] * focal_length) / z_cam
    sy = (pt_3d[1] * focal_length) / z_cam
    return (sx, sy, z_cam)

def lerp_color(c1_hex, c2_hex, t):
    c1 = np.array(mcolors.to_rgb(c1_hex))
    c2 = np.array(mcolors.to_rgb(c2_hex))
    c_out = c1 * (1 - t) + c2 * t
    return mcolors.to_hex(np.clip(c_out, 0, 1))

# ------------------------------------------------------------------
# BASE GEOMETRY: BUBBLE SHELLS & INTERNAL PHYSICS
# ------------------------------------------------------------------
# Fibonacci Sphere for translucent bubble walls
N_B_PTS = 500
phi = np.pi * (3. - np.sqrt(5.))
bubble_base = []
for i in range(N_B_PTS):
    y = 1 - (i / float(N_B_PTS - 1)) * 2
    r = np.sqrt(1 - y * y)
    t = phi * i
    bubble_base.append([np.cos(t) * r, y, np.sin(t) * r])
bubble_base = np.array(bubble_base)

# The Inflaton Field (Background expansion matrix)
np.random.seed(359)
N_INF = 1500
inflaton_pts = np.random.uniform(-1, 1, (N_INF, 3))
for i in range(N_INF):
    norm = np.linalg.norm(inflaton_pts[i])
    if norm > 0: inflaton_pts[i] /= norm
inflaton_radii = np.random.uniform(500, 8000, N_INF)

# Universe Particles
N_UNI_PTS = 800
pt_rand = np.random.uniform(-1, 1, (N_UNI_PTS, 3))
for i in range(N_UNI_PTS):
    n = np.linalg.norm(pt_rand[i])
    if n > 0: pt_rand[i] /= n

def render_frame(packet):
    f, phase_ratio = packet
    t = phase_ratio * DURATION

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)
    ax.autoscale(False)

    # 1. KINEMATIC CAMERA & TIMELINE
    # ------------------------------
    T_NUCLEATE = 4.0
    T_PHYSICS  = 10.0
    T_EXPAND   = 18.0

    # Camera slowly sweeps across the multiverse to reveal the spectrum
    cam_pan = ease_in_out(np.clip((t - 6.0)/12.0, 0, 1))
    pitch = np.radians(-10 + 20 * cam_pan)
    yaw = np.radians(-30) + (t * 0.05)
    sys_rotation = rotate_x(pitch) @ rotate_y(yaw)
    y_shift = -80
    
    render_queue = []

    # 2. THE EXPANDING INFLATON FIELD (The Ocean)
    # -------------------------------------------
    # These base coordinates expand exponentially outwards endlessly
    inf_expansion = np.exp(t * 0.15) if t < T_EXPAND else np.exp(T_EXPAND * 0.15 + (t-T_EXPAND)*0.3)
    field_pts = inflaton_pts * (inflaton_radii[:, np.newaxis] * inf_expansion * 0.1)
    
    # We wrap them using modulo to create an 'infinite' zooming field illusion
    field_pts = ((field_pts + 4000) % 8000) - 4000
    
    proj_inf = np.dot(field_pts, sys_rotation.T)
    for p in proj_inf:
        res = get_projection(p)
        if res:
            render_queue.append({
                'type': 'pt', 'd': res[2], 'x': res[0], 'y': res[1]+y_shift, 
                'c': mcolors.to_rgba(C_INFLATON, 0.4), 's': 3.0 * (1500.0/res[2])
            })

    # 3. BUBBLE LOGIC (The Spectrum of Universes)
    # -------------------------------------------
    # We establish 3 "Hero" bubbles representing the categorical spectrum
    # Over time, the space *between* them expands (Eternal Inflation separating bubbles)
    bubble_separation = 1.0 + ease_in_out(np.clip((t - T_EXPAND)/6.0, 0, 1)) * 3.0
    
    hero_centers = [
        np.array([-450 * bubble_separation, 0,  150 * bubble_separation]), # Uni A: Fine Tuned
        np.array([   0, -100 * bubble_separation, -300 * bubble_separation]), # Uni B: Dense Crush
        np.array([ 450 * bubble_separation,  100 * bubble_separation,   50 * bubble_separation])  # Uni C: Void
    ]

    for b_idx, center in enumerate(hero_centers):
        if t < T_NUCLEATE: continue # Not born yet
        
        # Nucleation Expansion (Bubble rapidly grows to a fixed boundary size)
        b_prg = np.clip((t - T_NUCLEATE) / 3.0, 0.0, 1.0)
        bubble_radius = 280.0 * ease_in_out(b_prg)
        
        # A. Render the Holographic Boundary Shell (The Bubble Wall)
        # ----------------------------------------------------------
        boundary_pts = (bubble_base * bubble_radius) + center
        proj_bound = np.dot(boundary_pts, sys_rotation.T)
        
        shell_alpha = 0.15 * b_prg
        if shell_alpha > 0.01:
            for p in proj_bound:
                res = get_projection(p)
                if res and np.linalg.norm([res[0], res[1]]) < 800: # General screen bound check
                    render_queue.append({
                        'type': 'pt', 'd': res[2], 'x': res[0], 'y': res[1]+y_shift, 
                        'c': mcolors.to_rgba(C_HORIZON, shell_alpha), 's': 3.0
                    })

        # B. Render the Internal Physical Laws (The Spectrum)
        # ---------------------------------------------------
        phys_prg = np.clip((t - T_PHYSICS) / 6.0, 0.0, 1.0)
        
        base_internal = pt_rand * (bubble_radius * 0.9)
        
        if b_idx == 0:
            # UNIVERSE A: "The Goldilocks"
            # Perfect spiral galaxy formation. A balance of gravity and expansion.
            rot_internal = np.dot(base_internal, rotate_y(t).T)
            
            for i, p_int in enumerate(rot_internal):
                # Pull points into a galactic disk
                dist = np.linalg.norm([p_int[0], p_int[2]])
                p_int[1] *= (1.0 - ease_in_out(phys_prg) * 0.95) # Flatten
                # Twist
                theta = np.arctan2(p_int[2], p_int[0])
                theta += dist * 0.01 * phys_prg * 2.0
                p_int[0] = dist * np.cos(theta)
                p_int[2] = dist * np.sin(theta)
                
                final_p = p_int + center
                proj = np.dot(final_p, sys_rotation.T)
                res = get_projection(proj)
                if res:
                    u_col = C_UNI_A if i % 2 == 0 else C_UNI_A_G
                    # Stars ignite
                    c_fade = lerp_color(C_TEXT, u_col, phys_prg)
                    render_queue.append({'type': 'pt', 'd': res[2], 'x': res[0], 'y': res[1]+y_shift, 
                                         'c': c_fade, 's': 8.0 * (1500.0/res[2])})
                                         
        elif b_idx == 1:
            # UNIVERSE B: "The High Gravity Crush"
            # Gravitational constants are too strong. The universe instantly collapses.
            shrink_factor = 1.0 - ease_in_out(phys_prg) * 0.9
            for i, p_int in enumerate(base_internal):
                # Swarm and crush
                vib = np.random.uniform(-10, 10, 3) * (1-phys_prg)
                final_p = (p_int * shrink_factor) + vib + center
                proj = np.dot(final_p, sys_rotation.T)
                res = get_projection(proj)
                if res:
                    c_fade = lerp_color(C_TEXT, C_UNI_B, phys_prg)
                    # Point size increases as density spikes
                    s_mult = 1.0 + (phys_prg * 3.0)
                    render_queue.append({'type': 'pt', 'd': res[2], 'x': res[0], 'y': res[1]+y_shift, 
                                         'c': c_fade, 's': 6.0 * s_mult * (1500.0/res[2])})
                                         
        elif b_idx == 2:
            # UNIVERSE C: "The Cold Void"
            # Expansion forces (Dark Energy) dominate perfectly. Matter is ripped apart instantly.
            expand_factor = 1.0 + ease_in_out(phys_prg) * 0.2 # Pushes right to the bubble edges
            for i, p_int in enumerate(base_internal):
                final_p = (p_int * expand_factor) + center
                proj = np.dot(final_p, sys_rotation.T)
                res = get_projection(proj)
                if res:
                    # Points fade out and cool to deep azure
                    alpha_v = 1.0 - (phys_prg * 0.6)
                    c_fade = lerp_color(C_TEXT, C_UNI_C, phys_prg)
                    render_queue.append({'type': 'pt', 'd': res[2], 'x': res[0], 'y': res[1]+y_shift, 
                                         'c': mcolors.to_rgba(c_fade, alpha_v), 's': 4.0 * (1500.0/res[2])})

    # 4. ORTHOGRAPHIC Z-DEPTH DISPATCH
    # --------------------------------
    render_queue.sort(key=lambda item: item['d'], reverse=True)

    # Fast plotting logic
    for item in render_queue:
        if item['type'] == 'pt':
            if 'alpha' in item:
                ax.scatter(item['x'], item['y'], color=item['c'], s=item['s'], alpha=item['alpha'], edgecolors='none', zorder=50)
            else:
                ax.scatter(item['x'], item['y'], color=item['c'], s=item['s'], edgecolors='none', zorder=50)

    # ====================================================
    # 5. VISUAL TELEMETRY AND INFORMATION OVERLAYS
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_BG, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=2, zorder=81)

    ax.text(-500, 890, "LG-359b :: THE MULTIVERSE", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "COSMOLOGICAL INFLATION // BUBBLE UNIVERSES", color='#555555', fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_BG, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=2, zorder=81)

    # Narrative Telemetry Mapping
    if t < T_NUCLEATE:
        s1, c1 = "ETERNAL INFLATION", C_TEXT
        s2, c2 = "HIGH-ENERGY OCEAN EXPANDING", C_INFLATON
        t_state = "THE BACKGROUND META-VACUUM DOMINATES ALL SPACE"
    elif t < T_PHYSICS:
        s1, c1 = "BUBBLE NUCLEATION", C_TEXT
        s2, c2 = "LOCALIZED BIG BANGS IGNITING", C_HORIZON
        t_state = "REGIONS 'FREEZE OUT' AND STOP EXPANDING SO RAPIDLY"
    elif t < T_EXPAND:
        s1, c1 = "THE SPECTRUM OF PHYSICS", C_UNI_A
        s2, c2 = "RANDOM PHYSICAL CONSTANTS CRYSTALLIZE", C_UNI_B
        t_state = "EACH UNIVERSE DEVELOPS TOTALLY DIFFERENT MATHEMATICAL LAWS"
    else:
        s1, c1 = "THE ENDLESS EXPANSE", C_TEXT
        s2, c2 = "SPACE BETWEEN BUBBLES INFLATES FOREVER", C_INFLATON
        t_state = "THE DISTINCT UNIVERSES ARE ISOLATED FOREVER IN THE VOID"

    ax.text(-500, -760, "SYS_01 [GLOBAL STATE]    :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(30, -760, s1, color=c1, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [LOCAL MECHANICS] :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(30, -800, s2, color=c2, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "SCIENTIFIC AUDIT         :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(30, -840, t_state, color=C_TEXT, fontsize=14, fontname='monospace', zorder=82)

    # Seamless Transition Progress Bar
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 4, facecolor='#E5E7EB', zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 4, facecolor=C_TEXT, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0)
    plt.close('all')
    gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-359b: THE INFLATIONARY MULTIVERSE [CORES: {cpu_cores}] [RENDERING BUBBLE NUCLEATION]")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
