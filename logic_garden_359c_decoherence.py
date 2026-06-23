"""
PROJECT: Logic Garden 359c (Irreversible Decoherence // Environmental Entanglement)
FORMAT: YouTube Shorts (1080x1920)
METADATA: QUANTUM MECHANICS, DECOHERENCE, MANY WORLDS, ENTANGLEMENT
EXECUTION: Continuous 24.0s Sequence. True 3D Particle Engine. Daylight Palette.
HOTFIX: Absolute Bounding Box Locked. Frustum Culling Active.
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
OUT_DIR = "frames_359c_decoherence"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- VISUAL PALETTE (DAYLIGHT PROTOCOL) --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_UNIFIED   = '#10B981'   # Pure Superposition (Green)
C_ENV       = '#DE008A'   # Environmental/Observer Particles (Magenta)
C_WORLD_A   = '#00D2FF'   # Decohered Reality A (Cyan)
C_WORLD_B   = '#FFB300'   # Decohered Reality B (Gold)
C_GRID      = '#E5E7EB'

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
# BASE GEOMETRY: WAVEFUNCTION & ENVIRONMENT
# ------------------------------------------------------------------
# 1. Quantum System in Superposition (Dense Parametric Knot)
N_SYS = 2000
t_ang = np.linspace(0, 2*np.pi, N_SYS)
p, q = 3, 5
r_knot = 220 + 80 * np.cos(q * t_ang)
sys_x = r_knot * np.cos(p * t_ang)
sys_z = r_knot * np.sin(p * t_ang)
sys_y = 120 * np.sin(q * t_ang)
base_system = np.column_stack((sys_x, sys_y, sys_z))

# 2. Environmental Particles (The "Observer")
np.random.seed(363)
N_ENV = 600
env_start = []
env_target_idx = np.random.choice(N_SYS, N_ENV, replace=False)

for _ in range(N_ENV):
    # Spawn in a distant spherical shell
    vec = np.random.uniform(-1, 1, 3)
    vec /= np.linalg.norm(vec)
    dist = np.random.uniform(1500, 2500)
    env_start.append(vec * dist)
env_start = np.array(env_start)

# The illusion grid
grid_lines = []
for idx in np.arange(-500, 600, 250):
    grid_lines.append([[idx, 0, -500], [idx, 0, 500]])
    grid_lines.append([[-500, 0, idx], [500, 0, idx]])

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

    # 1. KINEMATIC TIMELINE OVERRIDES
    # -------------------------------
    T_ENV_START = 4.0
    T_ENTANGLE  = 11.0
    T_DECOHERE  = 13.0
    T_SPLIT_END = 19.0

    pitch = np.radians(-15 + 10 * np.sin(t * 0.2))
    yaw = t * 0.25
    sys_rotation = rotate_x(pitch) @ rotate_y(yaw)
    y_shift = -50
    
    render_queue = []

    # Calculate Geometric Drift for the Split
    drift_prg = np.clip((t - T_DECOHERE) / (T_SPLIT_END - T_DECOHERE), 0.0, 1.0)
    drift_ease = ease_in_out(drift_prg)
    
    # World A moves Left, World B moves Right
    dist_split = 280.0 * drift_ease
    offset_A = np.array([-dist_split, 0, 0])
    offset_B = np.array([ dist_split, 0, 0])
    
    # Color fading mechanics
    c_phase_A = lerp_color(C_UNIFIED, C_WORLD_A, drift_ease)
    c_phase_B = lerp_color(C_UNIFIED, C_WORLD_B, drift_ease)
    c_env_A   = lerp_color(C_ENV, C_WORLD_A, drift_ease)
    c_env_B   = lerp_color(C_ENV, C_WORLD_B, drift_ease)

    # 2. RENDER THE GRID
    # ------------------
    for line in grid_lines:
        proj = np.dot(line, sys_rotation.T)
        cams, sz = [], []
        for p in proj:
            res = get_projection(p)
            if res:
                sz.append([res[0], res[1] + y_shift])
                cams.append(res[2])
        if len(sz) == 2:
            render_queue.append({'type': 'line', 'd': np.mean(cams), 'pts': sz, 'c': C_GRID, 'lw': 1.0})

    # 3. KINEMATICS: QUANTUM SYSTEM & ENVIRONMENT
    # -------------------------------------------
    # Global base rotation of the system
    sys_spin = rotate_y(t * 1.5)
    
    # Calculate environment progress
    env_prg = np.clip((t - T_ENV_START) / (T_ENTANGLE - T_ENV_START), 0.0, 1.0)
    env_ease = ease_in_out(env_prg)

    # --- THE QUANTUM SYSTEM ---
    current_system = np.dot(base_system, sys_spin.T)
    # Violent vibration right before decoherence
    if T_ENTANGLE <= t < T_DECOHERE:
        vib_amp = 8.0 * ((t - T_ENTANGLE) / (T_DECOHERE - T_ENTANGLE))
        current_system += np.random.uniform(-vib_amp, vib_amp, current_system.shape)

    for i, pt in enumerate(current_system):
        if t < T_DECOHERE:
            # Single Unified World
            proj = np.dot(pt, sys_rotation.T)
            res = get_projection(proj)
            if res:
                s = 10.0 * (1500.0 / res[2])
                render_queue.append({'type': 'pt', 'd': res[2], 'x': res[0], 'y': res[1]+y_shift, 'c': C_UNIFIED, 's': s})
        else:
            # Irreversible Split (Duplicate and Displace)
            pA = pt + offset_A
            pB = pt + offset_B
            
            projA = np.dot(pA, sys_rotation.T)
            resA = get_projection(projA)
            if resA:
                s = 8.0 * (1500.0 / resA[2])
                render_queue.append({'type': 'pt', 'd': resA[2], 'x': resA[0], 'y': resA[1]+y_shift, 'c': c_phase_A, 's': s})
                
            projB = np.dot(pB, sys_rotation.T)
            resB = get_projection(projB)
            if resB:
                s = 8.0 * (1500.0 / resB[2])
                render_queue.append({'type': 'pt', 'd': resB[2], 'x': resB[0], 'y': resB[1]+y_shift, 'c': c_phase_B, 's': s})

    # --- THE ENVIRONMENT (OBSERVER) ---
    for i in range(N_ENV):
        start_p = env_start[i]
        target_p = current_system[env_target_idx[i]]
        
        # Position interpolation
        cur_p = start_p * (1 - env_ease) + target_p * env_ease
        
        # Vibration to show kinetic energy
        if t < T_ENTANGLE:
            cur_p += np.random.uniform(-5, 5, 3) * (1 - env_ease)
            
        if t < T_DECOHERE:
            # Single Environment crashing in
            proj = np.dot(cur_p, sys_rotation.T)
            res = get_projection(proj)
            if res:
                s = 14.0 * (1500.0 / res[2])
                alpha = env_prg # Fades in as it approaches
                if alpha > 0.05:
                    render_queue.append({'type': 'pt', 'd': res[2], 'x': res[0], 'y': res[1]+y_shift, 'c': mcolors.to_rgba(C_ENV, alpha), 's': s})
        else:
            # The Observer physically branches and duplicates into both new universes
            pA = cur_p + offset_A
            pB = cur_p + offset_B
            
            projA = np.dot(pA, sys_rotation.T)
            resA = get_projection(projA)
            if resA:
                s = 10.0 * (1500.0 / resA[2])
                render_queue.append({'type': 'pt', 'd': resA[2], 'x': resA[0], 'y': resA[1]+y_shift, 'c': c_env_A, 's': s})
                
            projB = np.dot(pB, sys_rotation.T)
            resB = get_projection(projB)
            if resB:
                s = 10.0 * (1500.0 / resB[2])
                render_queue.append({'type': 'pt', 'd': resB[2], 'x': resB[0], 'y': resB[1]+y_shift, 'c': c_env_B, 's': s})

    # 4. ORTHOGRAPHIC Z-DEPTH DISPATCH 
    # --------------------------------
    render_queue.sort(key=lambda item: item['d'], reverse=True)

    for item in render_queue:
        if item['type'] == 'line':
            pts = item['pts']
            ax.plot([pts[0][0], pts[1][0]], [pts[0][1], pts[1][1]], color=item['c'], lw=item['lw'], zorder=50)
        elif item['type'] == 'pt':
            ax.scatter(item['x'], item['y'], color=item['c'], s=item['s'], edgecolors='none', zorder=50)

    # ====================================================
    # 5. TELEMETRY AND HUD WIDGETS
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_BG, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=2, zorder=81)

    ax.text(-500, 890, "LG-359c :: THE ENVIRONMENTAL SPLIT", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "MANY-WORLDS INTERPRETATION // IRREVERSIBLE DECOHERENCE", color='#555555', fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_BG, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=2, zorder=81)

    if t < T_ENV_START:
        s1, c1 = "PURE ISOLATED WAVEFUNCTION", C_UNIFIED
        s2, c2 = "SUPERPOSITION INTACT", C_TEXT
        t_state = "ALL POSSIBLE STATES CO-EXISTING IN MATHEMATICAL UNITY"
    elif t < T_ENTANGLE:
        s1, c1 = "ENVIRONMENTAL INTRUSION", C_ENV
        s2, c2 = "OBSERVER PARTICLES APPROACHING", C_TEXT
        t_state = "THE SYSTEM IS ABOUT TO BREACH THERMODYNAMIC ISOLATION"
    elif t < T_DECOHERE:
        s1, c1 = "CRITICAL ENTANGLEMENT", C_ENV
        s2, c2 = "UNITY DESTABILIZING", C_UNIFIED
        t_state = "THE ENVIRONMENT PHYSICALLY LOCKS THE WAVEFUNCTION"
    elif t < T_SPLIT_END:
        s1, c1 = "DECOHERENCE // REALITY BIFURCATING", C_TEXT
        s2, c2 = "THE OBSERVER IS BRANCHING WITH THE SYSTEM", C_WORLD_A
        t_state = "OUTCOMES DO NOT COLLAPSE. THEY PHYSICALLY SPLIT."
    else:
        s1, c1 = "THE MANY WORLDS", C_TEXT
        s2, c2 = "IRREVERSIBLE ISOLATION SECURED", C_WORLD_B
        t_state = "THE UNIVERSES—AND THE OBSERVERS—ARE NOW FOREVER SEPARATED"

    ax.text(-500, -760, "SYS_01 [QUANTUM MATRIX]  :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(60, -760, s1, color=c1, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [THE ENVIRONMENT] :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(60, -800, s2, color=c2, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "SCIENTIFIC AUDIT         :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -865, t_state, color=C_TEXT, fontsize=14, fontname='monospace', zorder=82)

    # Seamless Transition Progress Bar
    ax.add_patch(patches.Rectangle((-500, -895), 1000, 4, facecolor='#E5E7EB', zorder=82))
    
    prog_c = C_UNIFIED
    if t > T_ENTANGLE: prog_c = C_ENV
    if t > T_DECOHERE: prog_c = C_WORLD_A
    ax.add_patch(patches.Rectangle((-500, -895), 1000 * phase_ratio, 4, facecolor=prog_c, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    
    # Absolute override: No bounding box expansion
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close('all')
    gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-359c: THE ENVIRONMENTAL SPLIT [CORES: {cpu_cores}] [RENDERING IRREVERSIBLE DECOHERENCE]")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
