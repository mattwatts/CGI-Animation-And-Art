"""
PROJECT: Logic Garden 362 (Black Hole Accretion Disk // Gravitational Lensing)
FORMAT: YouTube Shorts (1080x1920)
METADATA: BLACK HOLE, ACCRETION DISK, GRAVITATIONAL LENSING, RELATIVITY
EXECUTION: Continuous 24.0s Sequence. O(1) Kinematic Matrix Override. Daylight Palette.
HOTFIX: bbox_inches eradicated. Absolute 1080x1920 screen coverage locked.
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
OUT_DIR = "frames_362_accretion_disk"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- VISUAL PALETTE (DAYLIGHT PROTOCOL) --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_GRID      = '#E5E7EB'
C_SINGULAR  = '#000000'   # Absolute Void
C_INNER     = '#00D2FF'   # Relativistic Inner Edge (Cyan)
C_MID       = '#FFB300'   # Mid Orbit Energy (Gold)
C_OUTER     = '#DE008A'   # Outer Cooling Gas (Magenta)

# ------------------------------------------------------------------
# KINEMATIC PERSPECTIVE ENGINE 
# ------------------------------------------------------------------
def rotate_x(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])

def ease_in_out(t):
    t = np.clip(t, 0.0, 1.0)
    return 4 * t**3 if t < 0.5 else 1 - (-2 * t + 2)**3 / 2

def lerp_color(c1_hex, c2_hex, t):
    c1 = np.array(mcolors.to_rgb(c1_hex))
    c2 = np.array(mcolors.to_rgb(c2_hex))
    c_out = c1 * (1 - t) + c2 * t
    return mcolors.to_hex(np.clip(c_out, 0, 1))

# ------------------------------------------------------------------
# ACCRETION DISK ARRAYS (O(1) MATHEMATICAL GAS PLUME)
# ------------------------------------------------------------------
R_SCHWARZSCHILD = 155.0
R_IN = 200.0
R_OUT = 750.0

np.random.seed(362)
N_GAS = 8000

# Density bias towards the inner ring where energy is highest
r_gas = R_IN + (R_OUT - R_IN) * (np.random.rand(N_GAS) ** 1.8)
theta_gas = np.random.uniform(0, 2*np.pi, N_GAS)
# Keplerian velocity formulation: inner particles orbit much faster
speed_gas = 3500.0 / (r_gas ** 1.5)

# Pre-calculate thermodynamic color mapping based on orbital depth
color_gas = []
for rad in r_gas:
    norm = (rad - R_IN) / (R_OUT - R_IN)
    if norm < 0.3:
        color_gas.append(lerp_color(C_INNER, C_MID, norm / 0.3))
    else:
        color_gas.append(lerp_color(C_MID, C_OUTER, (norm - 0.3) / 0.7))

# ------------------------------------------------------------------
# RENDER DISPATCH
# ------------------------------------------------------------------
def render_frame(packet):
    f, phase_ratio = packet
    t = phase_ratio * DURATION

    # Absolute Canvas Generation
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # Rigid Frame Lock
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)
    ax.autoscale(False)

    # 1. TIMELINE & CAMERA KINEMATICS
    # -------------------------------
    T_MORPH_START = 8.0
    T_MORPH_END = 16.0
    
    if t < T_MORPH_START:
        cam_tilt = 0.0
    elif t > T_MORPH_END:
        cam_tilt = 1.0
    else:
        cam_tilt = ease_in_out((t - T_MORPH_START) / (T_MORPH_END - T_MORPH_START))
        
    pitch = np.radians(85 * cam_tilt) # From 0 (edge-on) to 85 (top-down)
    sys_rotation = rotate_x(pitch)
    y_shift = -80
    focal_length = 1500.0
    cam_dist = 2200.0
    
    render_queue = []

    # 2. THE LENSING ALGORITHM
    # ------------------------
    # When viewed edge-on, light from the back of the disk bends around the black hole.
    # We mathematically fake this 3D ray-tracing by displacing the apparent Y-coordinate of the gas.
    # As the camera rises (cam_tilt approaches 1), the lensing effect mathematically fades to zero.
    lens_power_up = 450.0 * (1.0 - cam_tilt)**2
    lens_power_dn = 200.0 * (1.0 - cam_tilt)**2

    # Advance the gas positions
    cur_theta = theta_gas + speed_gas * t
    x_pos = r_gas * np.cos(cur_theta)
    y_pos = np.zeros(N_GAS)
    z_pos = r_gas * np.sin(cur_theta)

    # Apply 3D rotation based on camera pitch
    unbent_points = np.column_stack((x_pos, y_pos, z_pos))
    rotated_points = np.dot(unbent_points, sys_rotation.T)

    for i in range(N_GAS):
        x3 = rotated_points[i, 0]
        y3 = rotated_points[i, 1]
        z3 = rotated_points[i, 2] # This is depth post-rotation
        
        # Original Z dictates if it's behind the black hole
        orig_z = z_pos[i] 
        orig_x = x_pos[i]
        orig_r = r_gas[i]
        
        # Base Doppler Beaming (Particles moving towards camera = brighter & bluer)
        # Rotation is counter-clockwise. Approaching side is X > 0.
        v_los = orig_x / orig_r 
        intensity = 1.0 + (v_los * 0.7)  # Ranges ~0.3 to 1.7
        gas_color = color_gas[i]
        
        # Primary Image (Front disk + Light bending OVER the top)
        # Z/R creates a perfect semi-circle arc over the singularity
        y_primary = y3 + lens_power_up * max(0, orig_z) / orig_r
        
        z_cam = z3 + cam_dist
        if z_cam > 10:
            sx = (x3 * focal_length) / z_cam
            sy = (y_primary * focal_length) / z_cam + y_shift
            
            # Particle size scales with distance and Doppler intensity
            p_size = 15.0 * (1500.0 / z_cam) * intensity
            p_alpha = np.clip(0.4 * intensity, 0.1, 0.9)
            
            render_queue.append({
                'type': 'pt', 'd': z_cam, 'x': sx, 'y': sy, 
                'c': mcolors.to_rgba(gas_color, p_alpha), 's': p_size
            })
            
        # Secondary Image (Light bending UNDER the bottom)
        # Only visible if the gas is behind the black hole
        if orig_z > 0 and lens_power_dn > 1.0:
            y_secondary = y3 - lens_power_dn * max(0, orig_z) / orig_r
            
            z_cam_sec = z3 + cam_dist  # Placed at same depth
            if z_cam_sec > 10:
                sx2 = (x3 * focal_length) / z_cam_sec
                sy2 = (y_secondary * focal_length) / z_cam_sec + y_shift
                
                s_size = 10.0 * (1500.0 / z_cam_sec) * intensity
                s_alpha = np.clip(0.25 * intensity, 0.05, 0.6)
                
                render_queue.append({
                    'type': 'pt', 'd': z_cam_sec, 'x': sx2, 'y': sy2, 
                    'c': mcolors.to_rgba(gas_color, s_alpha), 's': s_size
                })

    # 3. THE SINGULARITY (Absolute Void)
    # ----------------------------------
    # Displayed exactly at origin depth. Anything in front covers it, anything behind is blocked
    bh_sx = 0
    bh_sy = y_shift
    bh_radius = R_SCHWARZSCHILD * (focal_length / cam_dist)
    render_queue.append({
        'type': 'bh', 'd': cam_dist, 'x': bh_sx, 'y': bh_sy, 'r': bh_radius
    })

    # 4. ORTHOGRAPHIC Z-DEPTH SORTING & RENDER OVERRIDE
    # -------------------------------------------------
    render_queue.sort(key=lambda item: item['d'], reverse=True)

    for item in render_queue:
        if item['type'] == 'pt':
            ax.scatter(item['x'], item['y'], color=item['c'], s=item['s'], edgecolors='none', zorder=50)
        elif item['type'] == 'bh':
            ax.add_patch(patches.Circle((item['x'], item['y']), radius=item['r'], facecolor=C_SINGULAR, edgecolor='none', zorder=50))

    # ====================================================
    # 5. TELEMETRY AND HUD WIDGETS
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_BG, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=2, zorder=81)

    ax.text(-500, 890, "LG-362 :: ACCRETION GEOMETRY", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "SUPERMASSIVE SINGULARITY // GRAVITATIONAL LENSING", color='#555555', fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_BG, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=2, zorder=81)

    if t < T_MORPH_START:
        s1, c1 = "EDGE-ON ORIENTATION", C_INNER
        s2, c2 = "GRAVITATIONAL LENSING ACTIVE", C_MID
        t_state = "ILLUSION: LIGHT FROM BACK OF DISK BENDS OVER SINGULARITY"
    elif t < T_MORPH_END:
        s1, c1 = "CAMERA ELEVATION ASCENDING", C_TEXT
        s2, c2 = "OPTICAL WARP DECREASING", C_INNER
        t_state = "MATHEMATICAL UNFOLDING OF THE LENS EFFECT IN PROGRESS"
    else:
        s1, c1 = "TOP-DOWN ORIENTATION", C_TEXT
        s2, c2 = "OPTICAL ILLUSION DISPELLED", C_OUTER
        t_state = "REALITY: THE ACCRETION DISK IS A PERFECTLY FLAT GEOMETRIC RING"

    ax.text(-500, -760, "SYS_01 [PERSPECTIVE]     :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(60, -760, s1, color=c1, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [OPTICAL STATE]   :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(60, -800, s2, color=c2, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "SCIENTIFIC AUDIT         :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    # Kept string firmly below boundary
    ax.text(-500, -865, t_state, color=C_TEXT, fontsize=14, fontname='monospace', zorder=82)

    # Seamless Transition Progress Bar
    ax.add_patch(patches.Rectangle((-500, -895), 1000, 4, facecolor='#E5E7EB', zorder=82))
    prog_c = C_INNER if t < 12.0 else C_OUTER
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
    print(f"LG-362: ACCRETION DISK [CORES: {cpu_cores}] [RENDERING GRAVITATIONAL LENSING]")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
