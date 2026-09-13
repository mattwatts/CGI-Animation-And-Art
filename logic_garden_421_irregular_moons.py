"""
PROJECT: Logic Garden 421c (The Irregular Topology Tensor - Bespoke Matrices)
FORMAT: YouTube Shorts (1080x1920)
METADATA: ASTEROIDS, MOONS, VESTA, KINEMATICS, ASTROPHYSICS, SOLAR SYSTEM
EXECUTION: 24.0s Seamless Loop Sequence. Iso-scaled true volumetric rock matrices (3x3 Grid).
RULES ENFORCED:
- 9x Sovereign Parametric Generators mapped explicitly to true structural geography.
- FLAT-PLANE PROJECTION: Objects translated in 2D post-render to ensure 0% perspective distortion.
- Daylight Palette (White Substrate / High-Contrast Chrome).
- Bounded Telemetry clearance: Labels mathematically anchor below the geometric bounds.
- TATHĀTĀ LOOP: Rotations locked to K-Multiplier relative to true rotational speeds.
- Australian spelling conventions enforced natively (Maths, Colour, Optimise, Kilometres).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
import multiprocessing as mp
import os
import gc

# ======== SEQUENCE PARAMETERS ========
FPS = 60
DURATION = 24.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_421_irregular_moons"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG    = '#FFFFFF'
C_TEXT  = '#111115'
C_GUI   = '#64748B'
C_AXIS  = '#111115' 

LIGHT_DIR = np.array([0.7, 0.6, -0.4])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

# ------------------------------------------------------------------
# MATRIX OPERATIONS
# ------------------------------------------------------------------
def rx(deg):
    rad = np.radians(deg); c, s = np.cos(rad), np.sin(rad)
    return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def ry(deg):
    rad = np.radians(deg); c, s = np.cos(rad), np.sin(rad)
    return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def rz(deg):
    rad = np.radians(deg); c, s = np.cos(rad), np.sin(rad)
    return np.array([[c,-s,0],[s,c,0],[0,0,1]])

# ------------------------------------------------------------------
# 9-NODE IRREGULAR PLANETARY ARCHITECTURE (EXACT SCALES & FLAT PLANE)
# ------------------------------------------------------------------
cam_pitch = -26.0
cam_angle = 45.0
M_cam = rx(cam_pitch) @ ry(cam_angle)
cam_dist = 2200.0

# Base factor to map Vesta's 262 km radius to exactly 160 units pre-perspective
SCALE_F = 160.0 / 262.0 

# Structure: 
# 'NAME': [True_Rad_KM, Category, Period(h), Scaled_R, Bespoke_ID, [Scr_X, Scr_Y], C_Core, C_Mantle, C_Crust, Tilt, K_Mult]
DATA_MATRIX = {
    'VESTA':      [262, 'PROTOPLANET',   5.3,  262*SCALE_F, 0, [-350,  540], '#111115', '#334155', '#64748B',  29.0, 12],
    'PALLAS':     [256, 'ASTEROID',      7.8,  256*SCALE_F, 1, [   0,  540], '#020617', '#1E293B', '#334155',  34.0,  8],
    'HYPERION':   [135, 'SATURN YIELD', 21.2,  135*SCALE_F, 2, [ 350,  540], '#111115', '#475569', '#CBD5E1',   0.0,  1],
    'HEKTOR':     [112, 'JUPITER TROJAN',6.9,  112*SCALE_F, 3, [-350,   40], '#1E293B', '#78350F', '#9A3412',  10.0,  9],
    'PHOEBE':     [106, 'SATURN YIELD',  9.3,  106*SCALE_F, 4, [   0,   40], '#020617', '#1E293B', '#475569', 152.0,  7],
    'JANUS':      [ 89, 'SATURN YIELD', 16.7,   89*SCALE_F, 5, [ 350,   40], '#1E293B', '#64748B', '#94A3B8',   0.0,  4],
    'AMALTHEA':   [ 84, 'JUPITER YIELD',11.9,   84*SCALE_F, 6, [-350, -460], '#451A03', '#9A3412', '#EA580C',   0.0,  5],
    'LUTETIA':    [ 50, 'ASTEROID',      8.1,   50*SCALE_F, 7, [   0, -460], '#0F172A', '#475569', '#94A3B8',  96.0,  8],
    'PROMETHEUS': [ 43, 'SATURN YIELD', 14.7,   43*SCALE_F, 8, [ 350, -460], '#1E293B', '#94A3B8', '#F1F5F9',   0.0,  4],
}

print(f"PHASE 1: 3X3 BESPOKE FLAT-PLANE ARCHITECTURE LOCKED.")

# ------------------------------------------------------------------
# O(N) VOLUMETRIC SOLID RUBBLE PILE GENERATOR
# ------------------------------------------------------------------
np.random.seed(421)
N_PTS = 16000

def generate_asteroid_volume(r_base, shape_id):
    """
    9x Sovereign Mathematical Generators. Transforms 16,000 raw points into explicit geological reality.
    """
    u = np.random.uniform(0, 1, N_PTS)
    r_rand = r_base * u**(1/3) # Forces volumetric solid density, not a shell
    phi = np.arccos(np.random.uniform(-1, 1, N_PTS))
    theta = np.random.uniform(0, 2*np.pi, N_PTS)

    x = r_rand * np.sin(phi) * np.cos(theta)
    y = r_rand * np.cos(phi)
    z = r_rand * np.sin(phi) * np.sin(theta)

    if shape_id == 0:
        # VESTA: Triaxial Oblate Spheroid + Rheasilvia Impact Basin
        x *= 1.09; z *= 1.06; y *= 0.85 
        dist_from_pole = np.sqrt(x**2 + z**2)
        crater_mask = (y < 0) & (dist_from_pole < r_base * 0.85)
        # Parabolic cut with central 20km peak
        crater_floor = -0.70 * r_base + (0.4 * dist_from_pole)
        central_peak = 0.25 * r_base * np.exp(-(dist_from_pole**2) / (r_base * 0.25)**2)
        y[crater_mask] = np.maximum(y[crater_mask], crater_floor[crater_mask] + central_peak[crater_mask])

    elif shape_id == 1:
        # PALLAS: Sub-protoplanet. Slightly oblate, flat battered patches, subdued noise.
        x *= 1.11; y *= 0.88; z *= 1.0
        noise = 1.0 + 0.04*np.sin(3*phi)*np.cos(4*theta)
        x *= noise; y *= noise; z *= noise

    elif shape_id == 2:
        # HYPERION: The Sponge. Carves deep, sharp cellular pockets INWARD.
        x *= 1.25; y *= 0.8; z *= 0.95
        noise = 1.0 - 0.28 * np.abs(np.sin(4*phi) * np.sin(5*theta)) # Inward absolute pockets
        x *= noise; y *= noise; z *= noise

    elif shape_id == 3:
        # HEKTOR: Contact Binary. Extreme elongation with pinched neck.
        x *= 1.85; y *= 0.7; z *= 0.7
        pinch = 0.55 + 0.45 * (np.abs(x) / (r_base*1.85))**2 # Quadratic pinch at X=0
        y *= pinch; z *= pinch

    elif shape_id == 4:
        # PHOEBE: Battered sphere. Features massive spherical divots (Jason crater).
        noise = 1.0 + 0.03*np.cos(4*phi)
        x *= noise; y *= noise; z *= noise
        # Carve a massive spherical crater block
        c_dist = np.sqrt((x - r_base*0.5)**2 + (y - r_base*0.5)**2 + z**2)
        carve_mask = c_dist < (r_base * 0.55)
        # Push nodes inward to the crater boundary
        x[carve_mask] -= 0.3 * r_base
        y[carve_mask] -= 0.3 * r_base

    elif shape_id == 5:
        # JANUS: Blocky/Faceted potato.
        x *= 1.15; y *= 0.9
        # Square-wave logic forces flat edges instead of rolling hills
        noise = 1.0 + 0.1 * np.sign(np.cos(3*phi)) * np.abs(np.cos(3*phi))**0.5
        x *= noise; y *= noise; z *= noise

    elif shape_id == 6:
        # AMALTHEA: Spindle/Cigar with heavy leading hemisphere damage.
        x *= 1.7; y *= 0.9; z *= 0.85
        # Leading edge flattening (craters Pan/Gaea)
        leading_mask = x > (r_base * 0.8)
        x[leading_mask] *= 0.85

    elif shape_id == 7:
        # LUTETIA: Fractured, faceted rock with Massilia region depression.
        x *= 1.2; y *= 1.0; z *= 0.75
        noise = 1.0 - 0.12 * np.abs(np.cos(3*theta)) # Creates sharp longitudinal angular grooves
        x *= noise; y *= noise; z *= noise

    elif shape_id == 8:
        # PROMETHEUS: Smooth Shepherd elongation. 
        x *= 1.55; y *= 0.65; z *= 0.65
        noise = 1.0 + 0.02*np.sin(4*phi) # Minimal surface noise
        x *= noise; y *= noise; z *= noise

    # Recalculate physical matrix limits post-deformation
    r_dist = np.sqrt(x**2 + y**2 + z**2)
    r_max_est = np.max(r_dist) 
    return np.vstack([x, y, z]), r_dist, r_max_est

# PRE-CALCULATE BASE VOLUMES
VOLUMES = {}
for name, data in DATA_MATRIX.items():
    s_r, s_type = data[3], data[4]
    pts, r_dist, r_max = generate_asteroid_volume(s_r, s_type)
    
    colors = np.zeros((N_PTS, 3))
    crust_rgb = np.array(mcolors.to_rgb(data[8]))
    mantle_rgb = np.array(mcolors.to_rgb(data[7]))
    core_rgb = np.array(mcolors.to_rgb(data[6]))

    ratio = r_dist / r_max
    mask_crust = ratio > 0.8
    mask_mantle = (ratio > 0.4) & (ratio <= 0.8)
    mask_core = ratio <= 0.4

    colors[mask_crust] = crust_rgb
    colors[mask_mantle] = mantle_rgb
    colors[mask_core] = core_rgb
    
    VOLUMES[name] = (pts, colors, r_dist)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f_idx):
    t_sec = f_idx / float(FPS)
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.]); ax.set_axis_off(); fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540); ax.set_ylim(-960, 960)

    faces_collected_x = []
    faces_collected_y = []
    face_colors = []
    centroids_z = []
    marker_sizes = []
    ax_lines_2d = []

    # ================= LOOP 9-NODE PHYSICAL MATRICES =================
    for name, data in DATA_MATRIX.items():
        (true_km, home_p, p_days, s_r, shape_id, s_pos, 
         c_core, c_mantle, c_crust, tilt_d, k_m) = data
        
        pts_raw, base_colors, r_dist = VOLUMES[name]

        MT = rz(tilt_d) 
        spin_v = t_sec * (k_m * 15.0) 
        MR = ry(spin_v)
        M_total = MT @ MR 
        
        rot_pts = M_total @ pts_raw
        x_rot, y_rot, z_rot = rot_pts

        # 1. EXACT BOOLEAN CUTAWAY KINEMATICS (Right-Front void)
        mask_void = (x_rot > 0) & (z_rot < 0)
        valid_idx = np.where(~mask_void)[0]

        x_k = x_rot[valid_idx]
        y_k = y_rot[valid_idx]
        z_k = z_rot[valid_idx]
        c_k = base_colors[valid_idx]

        # 2. EXACT WALL SNAP & NORMAL YIELD (Solid interior flushing)
        normals = np.zeros((len(x_k), 3))
        r_k = r_dist[valid_idx] + 1e-4

        normals[:, 0] = x_k / r_k
        normals[:, 1] = y_k / r_k
        normals[:, 2] = z_k / r_k

        # Dynamic thickness clamping
        snap_thresh = max(4.0, s_r * 0.15) 

        wall_x = (x_k > -snap_thresh) & (z_k < 0)
        normals[wall_x] = [1, 0, 0]
        x_k[wall_x] = 0.0 

        wall_z = (z_k > -snap_thresh) & (x_k > 0)
        normals[wall_z] = [0, 0, -1]
        z_k[wall_z] = 0.0 

        # 3. LAMBERTIAN SHADING MATRIX
        dot_p = np.clip(np.dot(normals, LIGHT_DIR), 0, 1)
        diffuse = 0.25 + 0.75 * dot_p
        c_k_shaded = c_k * diffuse[:, np.newaxis]
        
        # 4. FLAT-PLANE 2D CAMERA PROJECTION
        local_pts = np.vstack([x_k, y_k, z_k])
        v_cam = M_cam @ local_pts
        v_cam[2, :] += cam_dist
        
        px = 1800.0 * (v_cam[0, :] / v_cam[2, :]) + s_pos[0]
        py = 1800.0 * (v_cam[1, :] / v_cam[2, :]) + s_pos[1]
        
        faces_collected_x.extend(px)
        faces_collected_y.extend(py)
        face_colors.extend(c_k_shaded)
        centroids_z.extend(v_cam[2, :])
        
        point_scale = (s_r / 20.0)**2 + 4.5
        marker_sizes.extend(np.full(len(x_k), point_scale))

        # 5. VISIBLE ROTATIONAL AXIS LINE
        top_start = MT @ np.array([0, s_r * 1.05, 0])
        top_end   = MT @ np.array([0, s_r * 1.6, 0])
        bot_start = MT @ np.array([0, -s_r * 1.05, 0])
        bot_end   = MT @ np.array([0, -s_r * 1.6, 0])
        
        for segment in [(top_start, top_end), (bot_start, bot_end)]:
            v_s = M_cam @ np.vstack(segment).T
            v_s[2, :] += cam_dist
            px_s = 1800.0 * (v_s[0, :] / v_s[2, :]) + s_pos[0]
            py_s = 1800.0 * (v_s[1, :] / v_s[2, :]) + s_pos[1]
            ax_lines_2d.append([(px_s[0], py_s[0]), (px_s[1], py_s[1])])

        # 6. EXACT CLEARANCE BOUNDED TELEMETRY
        bbox_props = dict(boxstyle="square,pad=0.3", fc="#FFFFFF", ec="#111115", lw=2)
        th_p = s_pos[0]
        screen_r = s_r * (1800.0 / cam_dist)
        tv_p = s_pos[1] - screen_r - 35.0
        
        p_str = f"{p_days}d" if name == 'HYPERION' else f"{p_days}h"
        ax.text(th_p, tv_p, f"{name} ({home_p})\nP: {p_str} [K:{k_m}]", color=C_TEXT, fontsize=12, fontname='monospace', weight='bold', ha='center', va='top', zorder=85, bbox=bbox_props)

    # ================= 7. ABSOLUTE DEPENDENCY SORT & RENDER =================
    for line in ax_lines_2d:
        ax.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], color=C_AXIS, lw=2.5, zorder=90)

    idx_sort = np.argsort(centroids_z)[::-1] 
    if len(faces_collected_x) > 0:
        ax.scatter(np.array(faces_collected_x)[idx_sort], 
                   np.array(faces_collected_y)[idx_sort], 
                   s=np.array(marker_sizes)[idx_sort], 
                   c=np.array(face_colors)[idx_sort], 
                   marker='h', edgecolors='none', zorder=60) 

    # ================= 8. HIGH-DENSITY HUD & TELEMETRY =================
    ax.add_patch(Rectangle((-540, 800), 1080, 160, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=3, zorder=81)
    ax.text(-500, 900, "LG-421c :: IRREGULAR TOPOLOGY ARRAY", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 850, "[SFI-1.00] EXACT PARAMETRIC BESPOKE TOPOLOGIES", color='#475569', fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    prog = t_sec / DURATION
    if t_sec < 12.0:
        state_msg = "PHASE 1: GEOMETRIC YIELD (THE RUBBLE PILE)"
        state_col = '#1E293B'
        active_op = "HYDROSTATIC FAILURE. EXACT FORMS (CIGAR, PEANUT) OBSERVED."
    else:
        state_msg = "PHASE 2: TATHATA KINEMATICS"
        state_col = '#9A3412'
        active_op = "VOLUMETRIC CROSS-SECTIONS CUTTING THROUGH TUMBLING MATRIX."

    ax.text(-500, -780, f"PROTOCOL STATE : {state_msg}", color=state_col, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"DIAGNOSTIC     : {active_op}", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"AXIOMATIC TRUTH: GENERIC NOISE FAILS REALITY. EACH OBJECT REQUIRES A SOVEREIGN MATHEMATICAL GENERATOR.", color=C_TEXT, fontsize=9.5, fontname='monospace', zorder=82)

    ax.add_patch(Rectangle((-500, -920), 1000, 8, facecolor=C_GUI, zorder=82))
    ax.add_patch(Rectangle((-500, -920), 1000 * prog, 8, facecolor=state_col, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f_idx:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f_idx

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-421c: BESPOKE TOPOLOGY TENSOR ENGAGED [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            pass
    print("Compilation Complete. 9x Node Flat-Plane Matrix bounded to explicit bespoke yields.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
