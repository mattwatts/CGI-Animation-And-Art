"""
PROJECT: Logic Garden 415 (The Terrestrial Substrate // Inner Solar System)
FORMAT: YouTube Shorts (1080x1920)
METADATA: TERRESTRIAL PLANETS, EARTH, MARS, VENUS, MERCURY, GEOPHYSICS, KINEMATICS
EXECUTION: 24.0s Sequence. Iso-scaled true 3D Comparative Matrices.
RULES ENFORCED:
- Daylight Palette (White Substrate / High-Contrast Chrome).
- Phase-Locked Metaphor: The thermodynamic heat engines of the inner solar system.
- Exact realisational aspect of stationary cutaways permanently tracking to the viewer.
- Planetary Radius corresponds exactly with the relative astronomical physical radius.
- HOTFIX: Coplanar Camera Anchoring applied to eradicate perspective-swelling algorithms.
- Australian spelling conventions enforced natively (Maths, Colour, Optimise).
- Absolute O(N) volumetric arrays with Lambertian shading and Deep-Sort.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
from matplotlib.collections import PolyCollection
import multiprocessing as mp
import os
import gc

# ======== SEQUENCE PARAMETERS ========
FPS = 60
DURATION = 24.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_415_terrestrial"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG            = '#FFFFFF'
C_TEXT          = '#111115'
C_EDGE          = '#111115'
C_CORE_DEAD     = '#1E293B'  # Carbon Slate (Frozen Iron Core)
C_CORE_ACTIVE   = '#111115'  # Indestructible Black (Hot Iron Core)
C_CORE_INNER    = '#FFFFFF'  # White Hot (Earth Solid Inner Core)

C_MERCURY_CRUST = '#94A3B8'  # Steel
C_MERC_NODE     = '#64748B'

C_VENUS_MANTLE  = '#DE008A'  # Deep Magenta (Trapped Heat)
C_VENUS_CRUST   = '#FFB300'  # Dense Amber (Choked Atmosphere Lid)
C_VENUS_NODE    = '#CC6600'  

C_EARTH_MANTLE  = '#CC6600'  # Deep Mantle Orange
C_EARTH_FLUID   = '#FF3300'  # Intense Red (Convecting Outer Core Dynamo)
C_EARTH_CRUST   = '#005599'  # Deep Marine (Tri-Phase Surface)
C_EARTH_LAND    = '#00C853'  # Jade Tensor (Continents)

C_MARS_MANTLE   = '#B45309'  # Oxide Rust
C_MARS_CRUST    = '#DF0000'  # High-Contrast Red (Irradiated Surface)
C_MARS_NODE     = '#7F1D1D'  # Deep Crimson Scars

C_GUI           = '#64748B'

LIGHT_DIR = np.array([-0.6, 0.7, -0.4])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

# ------------------------------------------------------------------
# MATRIX OPERATIONS
# ------------------------------------------------------------------
def rx(deg):
    rad = np.radians(deg); c, s = np.cos(rad), np.sin(rad)
    return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def ry(rad):
    c, s = np.cos(rad), np.sin(rad)
    return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def rz(rad):
    c, s = np.cos(rad), np.sin(rad)
    return np.array([[c,-s,0],[s,c,0],[0,0,1]])

# ------------------------------------------------------------------
# COPLANAR CAMERA ANCHORING
# ------------------------------------------------------------------
# To prevent Perspective Z-Depth Swelling (making Venus look bigger than Earth),
# we lock the screen coordinates on a 2D plane perpendicular to the camera.
cam_pitch = -26.0  
cam_angle = 45.0   
M_cam = rx(cam_pitch) @ ry(cam_angle)
M_inv = M_cam.T

# Target HUD layout positions (Camera Space: Flat to lens)
S_MERCURY = np.array([-250.0,  320.0, 0.0])
S_VENUS   = np.array([ 250.0,  320.0, 0.0])
S_EARTH   = np.array([-250.0, -320.0, 0.0])
S_MARS    = np.array([ 250.0, -320.0, 0.0])

# O(1) Mathematical translation into World Space coordinates
P_MERCURY = M_inv @ S_MERCURY
P_VENUS   = M_inv @ S_VENUS
P_EARTH   = M_inv @ S_EARTH
P_MARS    = M_inv @ S_MARS

# ------------------------------------------------------------------
# RIGID 3D ARCHITECTURAL LAYER METRICS (EXACT PHYSICAL RADII)
# ------------------------------------------------------------------
# True scale radii mapped against Earth = 175.0 units.
# Mercury: 38.3% || Venus: 95.0% || Mars: 53.2%
R_MERCURY = {'core': 57.0, 'crust': 67.0}
R_VENUS   = {'core': 83.0, 'mantle': 158.0, 'crust': 166.2}
R_EARTH   = {'inner': 35.0, 'outer': 95.0, 'mantle': 167.0, 'crust': 175.0}
R_MARS    = {'core': 42.0, 'mantle': 88.0, 'crust': 93.1}

print(f"PHASE 1: TERRESTRIAL MATRICES GEOMETRICALLY ANCHORED (Z-DEPTH SWAY NEUTRALISED).")

# ------------------------------------------------------------------
# O(N) PHYSICAL HARDWARE GEOMETRY FACTORY
# ------------------------------------------------------------------
def generate_wedge_shell(r, t_min, t_max, res_phi=24, res_theta=28):
    phi = np.linspace(0, np.pi, res_phi)
    theta = np.linspace(t_min, t_max, res_theta)
    P, T = np.meshgrid(phi, theta)
    X = r * np.sin(P) * np.cos(T)
    Y = r * np.cos(P)
    Z = r * np.sin(P) * np.sin(T)
    
    faces = []
    for i in range(res_theta - 1):
        for j in range(res_phi - 1):
            p1 = np.array([X[i][j], Y[i][j], Z[i][j]])
            p2 = np.array([X[i+1][j], Y[i+1][j], Z[i+1][j]])
            p3 = np.array([X[i+1][j+1], Y[i+1][j+1], Z[i+1][j+1]])
            p4 = np.array([X[i][j+1], Y[i][j+1], Z[i][j+1]])
            faces.append([p1, p2, p3, p4])
    return faces

def generate_cut_wall(theta, r_min, r_max, res_phi=20, res_r=2):
    phi = np.linspace(0, np.pi, res_phi)
    r_arr = np.linspace(r_min, r_max, res_r)
    P, R = np.meshgrid(phi, r_arr)
    X = R * np.sin(P) * np.cos(theta)
    Y = R * np.cos(P)
    Z = R * np.sin(P) * np.sin(theta)
    
    faces = []
    for i in range(res_r - 1):
        for j in range(res_phi - 1):
            p1 = np.array([X[i][j], Y[i][j], Z[i][j]])
            p2 = np.array([X[i+1][j], Y[i+1][j], Z[i+1][j]])
            p3 = np.array([X[i+1][j+1], Y[i+1][j+1], Z[i+1][j+1]])
            p4 = np.array([X[i][j+1], Y[i][j+1], Z[i][j+1]])
            faces.append([p1, p2, p3, p4])
    return faces

def generate_particle(center, size):
    r = size / 2.0
    v = np.array([[0, r, 0], [0, -r, 0], [r, 0, 0], [-r, 0, 0], [0, 0, r], [0, 0, -r]])
    f_idx = [[0, 2, 4], [0, 4, 3], [0, 3, 5], [0, 5, 2], [1, 4, 2], [1, 3, 4], [1, 5, 3], [1, 2, 5]]
    return [v[f] + center for f in f_idx]

# ------------------------------------------------------------------
# KINEMATIC GEOLOGY & FLUID COMPILERS (SURFACE MARKERS)
# ------------------------------------------------------------------
np.random.seed(415)
def seed_surface_nodes(n_pts, r_val):
    rad = np.full(n_pts, r_val + 2.0)
    phi = np.arccos(np.random.uniform(-0.95, 0.95, n_pts))
    theta = np.random.uniform(0, 2 * np.pi, n_pts)
    return rad, phi, theta

N_CRUST = 800
M_DR, M_DPHI, M_DTHETA = seed_surface_nodes(N_CRUST, R_MERCURY['crust'])
V_DR, V_DPHI, V_DTHETA = seed_surface_nodes(N_CRUST, R_VENUS['crust'])
E_DR, E_DPHI, E_DTHETA = seed_surface_nodes(N_CRUST, R_EARTH['crust'])
MA_DR, MA_DPHI, MA_DTHETA = seed_surface_nodes(N_CRUST, R_MARS['crust'])

def seed_volumetric_nodes(n_pts, r_min, r_max):
    rad = np.random.uniform(r_min, r_max, n_pts)
    phi = np.arccos(np.random.uniform(-0.9, 0.9, n_pts))
    theta = np.random.uniform(0, 2 * np.pi, n_pts)
    return rad, phi, theta

# Earth's Fluid Geodynamo (Deep internal spin)
N_DYNAMO = 500
DYN_DR, DYN_DPHI, DYN_DTHETA = seed_volumetric_nodes(N_DYNAMO, R_EARTH['inner']+4, R_EARTH['outer']-4)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f_idx):
    t_sec = f_idx / float(FPS)
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.]); ax.set_axis_off(); fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540); ax.set_ylim(-960, 960)

    # 1. KINEMATIC CAMERA TENSOR 
    # M_cam is pre-calculated dynamically above globally.
    cam_dist = 2200.0 
    
    # Static Cutaway Frame ensuring deep internal exposure.
    T_MIN = 0.0
    T_MAX = 3.0 * np.pi / 2.0

    faces_collected = []
    face_colors = []
    centroids_z = []
    
    def process_layer(f_faces, h_color, pos_offset):
        c_rgb = np.array(mcolors.to_rgb(h_color))
        
        for face in f_faces:    
            v1 = face[1] - face[0]; v2 = face[2] - face[0]
            norm = np.cross(v1, v2)
            n_len = np.linalg.norm(norm)
            if n_len > 0: norm /= n_len
            
            diff = 0.4 + 0.6 * np.clip(np.dot(norm, LIGHT_DIR), 0, 1)
            fc = np.append(c_rgb * diff, 1.0)
            
            f_offset = face + pos_offset
            # Because P_OFFSET was inverse-calculated against M_cam, multiplying
            # it back by M_cam here guarantees standard Z-depth = 0 across all 4 planets.
            v_cam = np.einsum('ij,nj->ni', M_cam, f_offset)
            v_cam[:, 2] += cam_dist
            
            if np.any(v_cam[:, 2] < 10.0): continue
            
            px = 1800.0 * (v_cam[:, 0] / v_cam[:, 2])
            py = 1800.0 * (v_cam[:, 1] / v_cam[:, 2])
            
            faces_collected.append(np.stack((px, py), axis=-1))
            face_colors.append(fc)
            centroids_z.append(np.mean(v_cam[:, 2]))

    def compile_planet(pos, rads, colors):
        keys = list(rads.keys())
        for i, k in enumerate(keys):
            r_out = rads[k]
            r_in = rads[keys[i-1]] if i > 0 else 0.0
            
            f_shell = generate_wedge_shell(r_out, T_MIN, T_MAX)
            f_wall_1 = generate_cut_wall(T_MIN, r_in, r_out)
            f_wall_2 = generate_cut_wall(T_MAX, r_in, r_out)
            process_layer(f_shell + f_wall_1 + f_wall_2, colors[i], pos)

    def process_kinematic_nodes(n_pts, dr, dphi, dtheta, v_spin, pos, h_col, size, expose_in_void=False):
        for i in range(n_pts):
            cur_t = (dtheta[i] + np.radians(v_spin)) % (2 * np.pi)
            is_in_void = (cur_t > T_MAX) 
            
            if expose_in_void == is_in_void:
                x = dr[i] * np.sin(dphi[i]) * np.cos(cur_t)
                y = dr[i] * np.cos(dphi[i])
                z = dr[i] * np.sin(dphi[i]) * np.sin(cur_t)
                p_f = generate_particle(np.array([x, y, z]), size)
                process_layer(p_f, h_col, pos)

    # ================= PLANET 1: MERCURY (Top Left) =================
    spin_merc = t_sec * 3.0
    compile_planet(P_MERCURY, R_MERCURY, [C_CORE_ACTIVE, C_MERCURY_CRUST])
    process_kinematic_nodes(N_CRUST, M_DR, M_DPHI, M_DTHETA, spin_merc, P_MERCURY, C_MERC_NODE, 4.0, expose_in_void=False)

    # ================= PLANET 2: VENUS (Top Right) =================
    # Venus rotates extremely slowly, trapped stagnant crust.
    spin_ven = t_sec * -0.5 
    compile_planet(P_VENUS, R_VENUS, [C_CORE_ACTIVE, C_VENUS_MANTLE, C_VENUS_CRUST])
    process_kinematic_nodes(N_CRUST, V_DR, V_DPHI, V_DTHETA, spin_ven, P_VENUS, C_VENUS_NODE, 5.0, expose_in_void=False)

    # ================= PLANET 3: EARTH (Bottom Left) =================
    spin_earth = t_sec * 12.0
    compile_planet(P_EARTH, R_EARTH, [C_CORE_INNER, C_EARTH_FLUID, C_EARTH_MANTLE, C_EARTH_CRUST])
    process_kinematic_nodes(N_CRUST, E_DR, E_DPHI, E_DTHETA, spin_earth, P_EARTH, C_EARTH_LAND, 6.0, expose_in_void=False)
    # Earth Fluid Dynamo Spin (Exposed strictly *inside* the core void)
    process_kinematic_nodes(N_DYNAMO, DYN_DR, DYN_DPHI, DYN_DTHETA, t_sec * 25.0, P_EARTH, '#FFFFFF', 4.0, expose_in_void=True)

    # ================= PLANET 4: MARS (Bottom Right) =================
    spin_mars = t_sec * 11.5
    compile_planet(P_MARS, R_MARS, [C_CORE_DEAD, C_MARS_MANTLE, C_MARS_CRUST])
    process_kinematic_nodes(N_CRUST, MA_DR, MA_DPHI, MA_DTHETA, spin_mars, P_MARS, C_MARS_NODE, 5.0, expose_in_void=False)

    # 5. ABSOLUTE DEPENDENCY SORT & RENDER
    sort_idx = np.argsort(centroids_z)[::-1] 
    if faces_collected:
        sorted_faces = [faces_collected[i] for i in sort_idx]
        sorted_fcs = [face_colors[i] for i in sort_idx]
        ax.add_collection(PolyCollection(sorted_faces, facecolors=sorted_fcs, edgecolors='#111115', linewidths=0.25, joinstyle='miter'))

    # LABELS (Calculated directly from the Coplanar Anchors to maintain exact padding)
    def project_label(pos_cam, r_bound, title, subtitle, sub_col):
        # Direct screen projection because pos_cam is already heavily aligned
        scale_mod = 1800.0 / cam_dist
        px = pos_cam[0] * scale_mod
        py = pos_cam[1] * scale_mod - (r_bound * scale_mod) - 40.0
        ax.text(px, py, title, color=C_TEXT, fontsize=18, fontname='monospace', weight='bold', ha='center', zorder=85)
        ax.text(px, py - 30, subtitle, color=sub_col, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=85)

    project_label(S_MERCURY, R_MERCURY['crust'], "MERCURY", "(STRIPPED CORE)", C_GUI)
    project_label(S_VENUS, R_VENUS['crust'], "VENUS", "(STAGNANT LID)", C_GUI)
    project_label(S_EARTH, R_EARTH['crust'], "EARTH", "(ACTIVE GEODYNAMO)", C_EARTH_CRUST)
    project_label(S_MARS, R_MARS['crust'], "MARS", "(DEAD ENGINE)", C_MARS_CRUST)

    # 6. HIGH-DENSITY HUD & TELEMETRY
    ax.add_patch(Rectangle((-540, 800), 1080, 160, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=3, zorder=81)
    ax.text(-500, 900, "LG-415 :: THE TERRESTRIAL SUBSTRATE", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 850, "[SFI-1.00] EXACT COMPARATIVE RADII & COPLANAR ALIGNMENT", color=C_EARTH_MANTLE, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    prog = t_sec / DURATION
    if t_sec < 12.0:
        state_msg = "PHASE 1: THE THERMODYNAMIC FAILURES"
        state_col = C_VENUS_CRUST
        active_op = "MERCURY: MASSIVE NAKED CORE. VENUS: HEAT CHOKED, NO DYNAMO."
    else:
        state_msg = "PHASE 2: THE CRITICAL MASS THRESHOLD"
        state_col = C_EARTH_CRUST
        active_op = "EARTH: MAGNETIC SHIELD INTACT. MARS: FROZEN CORE, STRIPPED ATMOSPHERE."

    ax.text(-500, -780, f"PROTOCOL STATE : {state_msg}", color=state_col, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"DIAGNOSTIC     : {active_op}", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"AXIOMATIC TRUTH: SOLAR PROXIMITY IS SECONDARY. O(1) MASS DICTATES CORE SURVIVAL.", color=C_TEXT, fontsize=11, fontname='monospace', zorder=82)

    ax.add_patch(Rectangle((-500, -920), 1000, 8, facecolor=C_GUI, zorder=82))
    ax.add_patch(Rectangle((-500, -920), 1000 * prog, 8, facecolor=state_col, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f_idx:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f_idx

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-415 (HOTFIX): COPLANAR ANCHORED TERRESTRIAL SUBSTRATE [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            pass
    print("Compilation Complete. True isometric 1:1 planar scale enforced.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
