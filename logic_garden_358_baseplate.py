"""
PROJECT: Logic Garden 358 (What is Real? // Thermodynamic Friction)
FORMAT: YouTube Shorts (1080x1920)
METADATA: KINEMATICS, THERMODYNAMICS, SYSTEM CONSTRAINTS, PHILOSOPHY OF SCIENCE
EXECUTION: 24.0s Narrative Sequence. True 3D Particle Physics Engine. Daylight Palette.
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
OUT_DIR = "frames_358_baseplate"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- VISUAL PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_ILLUSION  = '#00D2FF'   # The Frictionless Perfection
C_BASEPLATE = '#E5E7EB'   # The Unyielding Coordinate Plane
C_GRID      = '#9CA3AF'
C_FRICTION  = '#DE008A'   # Kinetic Heat (Magenta)
C_SPARKS    = '#FFB300'   # Thermal Energy Ejection (Gold)
C_COLD_IRON = '#5A6270'   # Dead, cooled reality

# ------------------------------------------------------------------
# 3D ENGINE & KINEMATICS
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
    return 4 * t**3 if t < 0.5 else 1 - (-2 * t + 2)**3 / 2

def get_projection(pt_3d, focal_length=1200.0, cam_dist=1200.0):
    z_cam = pt_3d[2] + cam_dist
    if z_cam < 10: return None
    sx = (pt_3d[0] * focal_length) / z_cam
    sy = (pt_3d[1] * focal_length) / z_cam
    return (sx, sy, z_cam)

# ------------------------------------------------------------------
# SCENE GEOMETRY: THE KNOT & THE BASEPLATE
# ------------------------------------------------------------------
N_POINTS = 1000
t_ang = np.linspace(0, 2*np.pi, N_POINTS)
p, q = 3, 5
r = 180 + 60 * np.cos(q * t_ang)
x_base = r * np.cos(p * t_ang)
z_base = r * np.sin(p * t_ang)
y_base = 70 * np.sin(q * t_ang)
base_knot = np.column_stack((x_base, y_base, z_base))

# The Baseplate Grid
grid_lines = []
for idx in np.arange(-800, 900, 100):
    grid_lines.append((np.array([[idx, 0, -800], [idx, 0, 800]])))
    grid_lines.append((np.array([[-800, 0, idx], [800, 0, idx]])))

# ------------------------------------------------------------------
# DETERMINISTIC PHYSICS ENGINE (PRE-CALCULATED SHATTER STATE)
# ------------------------------------------------------------------
np.random.seed(358)
T_SHATTER = 15.0

# Calculate exact position of knot at shatter point
shatter_rot = rotate_y(T_SHATTER * 4.0)
shatter_pos = np.dot(base_knot, shatter_rot.T)
shatter_pos[:, 1] += 50.0  # Final Y descent position

shatter_vel = np.zeros((N_POINTS, 3))
for i in range(N_POINTS):
    pos = shatter_pos[i]
    # Rotational velocity (Cross product of angular velocity and radius)
    omega = np.array([0, 4.0, 0])
    v_rot = np.cross(omega, pos - np.array([0, 50, 0]))
    
    # Explosive outward force (Thermodynamic rupture)
    burst_dir = pos - np.array([0, -20, 0])
    burst_dir /= np.linalg.norm(burst_dir)
    
    shatter_vel[i] = v_rot + burst_dir * np.random.uniform(300, 1000)

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

    # 1. NARRATIVE TIMELINE
    # ---------------------
    T_DESCEND_START = 4.0
    T_IMPACT = 10.0
    T_END = 24.0

    # Camera slowly orbits
    sys_rotation = rotate_x(np.radians(-20)) @ rotate_y(t * 0.2)
    y_shift = -150

    render_queue = []

    # 2. RENDER THE BASEPLATE
    # -----------------------
    alpha_baseplate = np.clip((t - 4.0) / 4.0, 0.0, 1.0)
    if alpha_baseplate > 0.01:
        # Baseplate geometry plane
        plane_pts = np.array([[-800, 0, -800], [800, 0, -800], [800, 0, 800], [-800, 0, 800]])
        proj_plane = np.dot(plane_pts, sys_rotation.T)
        screen_plane = []
        for pt in proj_plane:
            res = get_projection(pt)
            if res: screen_plane.append([res[0], res[1] + y_shift])
        if len(screen_plane) == 4:
            render_queue.append({
                'type': 'poly', 'd': np.mean(proj_plane[:,2] + 1200), 'pts': np.array(screen_plane),
                'c': mcolors.to_rgba(C_BASEPLATE, alpha_baseplate * 0.6)
            })

        # Baseplate Grid Lines
        for line in grid_lines:
            proj_line = np.dot(line, sys_rotation.T)
            sz = []
            cams = []
            for p in proj_line:
                res = get_projection(p)
                if res:
                    sz.append([res[0], res[1] + y_shift])
                    cams.append(res[2])
            if len(sz) == 2:
                render_queue.append({
                    'type': 'line', 'd': np.mean(cams), 'pts': np.array(sz), 
                    'c': mcolors.to_rgba(C_GRID, alpha_baseplate * 0.4), 'lw': 1.5
                })

    # 3. KINEMATICS & COLLISION LOGIC
    # -------------------------------
    y_offset = 350.0
    if t > T_DESCEND_START:
        prg = np.clip((t - T_DESCEND_START) / (T_IMPACT - T_DESCEND_START), 0.0, 1.0)
        y_offset = 350.0 - (300.0 * ease_in_out(prg))

    if t < T_SHATTER:
        # PURE KINEMATICS (The Illusion)
        cur_rot = rotate_y(t * 4.0)
        current_pts = np.dot(base_knot, cur_rot.T)
        current_pts[:, 1] += y_offset
        
        for i, pt in enumerate(current_pts):
            c_node = C_ILLUSION
            alpha_node = 1.0
            
            # THERMODYNAMIC FRICTION: The Axiom of Broken Glass
            # When the perfect mathematical ring clips the absolute floor constraint, 
            # it is brutally clamped to Y=0, generating massive thermal energy.
            is_grinding = False
            if pt[1] < 0:
                is_grinding = True
                pt[1] = 0 # Clamp to the Baseplate
                c_node = C_FRICTION
                
                # Spark Spallation Ejection
                if np.random.rand() > 0.85:
                    spark = pt + np.random.uniform(-40, 40, 3)
                    spark[1] = np.random.uniform(5, 50)
                    s_proj = get_projection(np.dot(spark, sys_rotation.T))
                    if s_proj:
                        render_queue.append({
                            'type': 'pt', 'd': s_proj[2], 'x': s_proj[0], 'y': s_proj[1] + y_shift,
                            'c': C_SPARKS, 's': np.random.uniform(2, 8), 'm': 'o'
                        })
            
            # Rendering standard particle
            proj = np.dot(pt, sys_rotation.T)
            res = get_projection(proj)
            if res:
                size = 18.0 if is_grinding else 8.0
                render_queue.append({
                    'type': 'pt', 'd': res[2], 'x': res[0], 'y': res[1] + y_shift,
                    'c': c_node, 's': size * (1200.0/res[2]), 'm': 'o'
                })

    else:
        # RAW NEWTONIAN PHYSICS (The Shattered Baseplate Reality)
        dt = 1.0 / FPS
        frames_to_sim = int((t - T_SHATTER) / dt)
        
        # Load the deterministic exact burst state
        p_current = shatter_pos.copy()
        v_current = shatter_vel.copy()
        
        # Fast-forward physics simulation to current frame
        gravity = -1800.0
        for _ in range(frames_to_sim):
            v_current[:, 1] += gravity * dt
            p_current += v_current * dt
            
            # Bouncing on the Baseplate constraint
            hits = p_current[:, 1] < 0
            p_current[hits, 1] = 0
            v_current[hits, 1] *= -0.4  # Velocity restitution (lose energy)
            v_current[hits, 0] *= 0.90  # Kinetic friction mapping
            v_current[hits, 2] *= 0.90
            
        # Cooling thermodynamics mapping
        cool_prg = np.clip((t - T_SHATTER) / (T_END - T_SHATTER), 0.0, 1.0)
        
        r1, g1, b1 = mcolors.to_rgb(C_FRICTION)
        r2, g2, b2 = mcolors.to_rgb(C_COLD_IRON)
        c_r = r1 * (1 - cool_prg) + r2 * cool_prg
        c_g = g1 * (1 - cool_prg) + g2 * cool_prg
        c_b = b1 * (1 - cool_prg) + b2 * cool_prg
        c_cooled = mcolors.to_hex((c_r, c_g, c_b))
        
        for pt in p_current:
            proj = np.dot(pt, sys_rotation.T)
            res = get_projection(proj)
            if res:
                render_queue.append({
                    'type': 'pt', 'd': res[2], 'x': res[0], 'y': res[1] + y_shift,
                    'c': c_cooled, 's': 6.0 * (1200.0/res[2]), 'm': 'o'
                })

    # 4. DEPTH SORT AND RENDER
    # ------------------------
    render_queue.sort(key=lambda item: item['d'], reverse=True)

    for item in render_queue:
        if item['type'] == 'poly':
            ax.add_patch(patches.Polygon(item['pts'], facecolor=item['c'], edgecolor='none', zorder=50))
        elif item['type'] == 'line':
            pts = item['pts']
            ax.plot([pts[0][0], pts[1][0]], [pts[0][1], pts[1][1]], color=item['c'], lw=item['lw'], zorder=50)
        elif item['type'] == 'pt':
            ax.scatter(item['x'], item['y'], color=item['c'], s=item['s'], marker=item['m'], edgecolors='none', zorder=50)

    # ====================================================
    # 5. VISUAL TELEMETRY AND INFORMATION OVERLAYS
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_BG, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=2, zorder=81)

    ax.text(-500, 890, "LG-358 :: THE BASEPLATE REVEAL", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "THE AXIOM OF BROKEN GLASS // REALITY IS RESISTANCE", color='#555555', fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_BG, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=2, zorder=81)

    # Dynamic Descriptive Text
    if t < T_DESCEND_START:
        s1, c1 = "THEORETICAL MODEL: FLAWLESS GEOMETRY", C_ILLUSION
        s2, c2 = "PERPETUAL MOTION / ZERO RESISTANCE", C_TEXT
        t_state = "OBSERVATION: A BEAUTIFUL, FRICTIONLESS UNIVERSE"
    elif t < T_IMPACT:
        s1, c1 = "GEOMETRIC DESCENT DETECTED", C_TEXT
        s2, c2 = "ABSOLUTE RULESET (THE BASEPLATE) MANIFESTING", C_COLD_IRON
        t_state = "SYSTEM APPROACHING THE BOUNDARIES OF PHYSICS"
    elif t < T_SHATTER:
        s1, c1 = "THERMODYNAMIC FRICTION DETECTED", C_FRICTION
        s2, c2 = "GEOMETRIC ILLUSION BRUTALLY CLAMPED", C_SPARKS
        t_state = "PARADOX REJECTED: REALITY RESISTS IMPOSSIBLE LOOPS"
    else:
        s1, c1 = "STRUCTURAL SHATTER // ILLUSION ANNIHILATED", C_TEXT
        s2, c2 = "NEWTONIAN PHYSICS EXERTING ABSOLUTE CONTROL", C_COLD_IRON
        t_state = "CONCLUSION: WHAT IS REAL? THE BOUNDARY THAT BREAKS YOU."

    ax.text(-500, -760, "SYS_01 [PERCEPTUAL STATE] :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(40, -760, s1, color=c1, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [KINETIC LOAD]     :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(40, -800, s2, color=c2, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "SCIENTIFIC AUDIT          :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(40, -840, t_state, color=C_TEXT, fontsize=14, fontname='monospace', zorder=82)

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
    print(f"LG-358: WHAT IS REAL? [CORES: {cpu_cores}] [RENDERING THERMODYNAMIC SHATTER]")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
