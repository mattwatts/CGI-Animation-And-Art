"""
PROJECT: Logic Garden 416 (The Ice Giant Tensor // Uranus & Neptune)
FORMAT: YouTube Shorts (1080x1920)
METADATA: URANUS, NEPTUNE, ICE GIANTS, SUPERCRITICAL FLUID, DIAMOND RAIN, KINEMATICS
EXECUTION: 24.0s Sequence. Iso-scaled true 3D Comparative Matrices.
RULES ENFORCED:
- Daylight Palette (White Substrate / High-Contrast Chrome).
- Phase-Locked Metaphor: Thermodynamic death vs Supersonic convection.
- Exact realisational aspect of stationary cutaways permanently tracking to the viewer.
- Planetary Radius corresponds exactly with the relative astronomical physical radius.
- COPLANAR CAMERA ANCHORING: Strict isometric scale retention.
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
OUT_DIR = "frames_416_ice_giants"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG            = '#FFFFFF'
C_TEXT          = '#111115'
C_EDGE          = '#111115'

# URANUS (Dead Engine, Sluggish, Cold)
C_URA_CORE      = '#1E293B'  # Carbon Slate (Frozen Core)
C_URA_MANTLE    = '#005599'  # Deep Marine (Cold Supercritical Ices)
C_URA_CRUST     = '#64748B'  # Dull Haze
C_URA_NODE      = '#94A3B8'  

# NEPTUNE (Active Convection, Supersonic, Hot)
C_NEP_CORE      = '#FFFFFF'  # White Hot Activity
C_NEP_MANTLE    = '#DE008A'  # Deep Magenta (Convecting Hot Ices)
C_NEP_CRUST     = '#0033CC'  # High-Contrast Azure (Supersonic Envelope)
C_NEP_NODE      = '#00D2FF'  
C_DIAMOND       = '#FFB300'  # Dense Amber (Precipitating Carbon)

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
cam_pitch = -26.0  
cam_angle = 45.0   
M_cam = rx(cam_pitch) @ ry(cam_angle)
M_inv = M_cam.T
cam_dist = 2200.0 

# Target HUD layout positions (Camera Space: Flat to lens, stacked vertically along X=0)
S_URANUS  = np.array([0.0,  380.0, 0.0])
S_NEPTUNE = np.array([0.0, -380.0, 0.0])

# O(1) Mathematical translation into World Space coordinates
P_URANUS  = M_inv @ S_URANUS
P_NEPTUNE = M_inv @ S_NEPTUNE

# ------------------------------------------------------------------
# RIGID 3D ARCHITECTURAL LAYER METRICS (EXACT PHYSICAL RADII)
# ------------------------------------------------------------------
# True scale radii mapped against Uranus = 300.0 units.
# Uranus: 25,362 km || Neptune: 24,622 km (97.08% of Uranus)
R_URANUS  = {'core': 60.0, 'mantle': 210.0, 'crust': 300.0}
R_NEPTUNE = {'core': 58.2, 'mantle': 203.0, 'crust': 291.2}

print(f"PHASE 1: ICE GIANT MATRICES GEOMETRICALLY ANCHORED (Z-DEPTH SWAY NEUTRALISED).")

# ------------------------------------------------------------------
# O(N) PHYSICAL HARDWARE GEOMETRY FACTORY
# ------------------------------------------------------------------
def generate_wedge_shell(r, t_min, t_max, res_phi=28, res_theta=32):
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

def generate_cut_wall(theta, r_min, r_max, res_phi=24, res_r=2):
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
np.random.seed(416)
def seed_surface_nodes(n_pts, r_val):
    rad = np.full(n_pts, r_val + 2.0)
    phi = np.arccos(np.random.uniform(-0.95, 0.95, n_pts))
    theta = np.random.uniform(0, 2 * np.pi, n_pts)
    return rad, phi, theta

N_CRUST = 900
U_DR, U_DPHI, U_DTHETA = seed_surface_nodes(N_CRUST, R_URANUS['crust'])
N_DR, N_DPHI, N_DTHETA = seed_surface_nodes(N_CRUST, R_NEPTUNE['crust'])

# Neptune Diamond Rain (Sinking through mantle)
N_DIAMONDS = 600
D_DR = np.random.uniform(R_NEPTUNE['core'] + 10, R_NEPTUNE['mantle'] - 10, N_DIAMONDS)
D_DPHI = np.arccos(np.random.uniform(-0.8, 0.8, N_DIAMONDS))
D_DTHETA = np.random.uniform(0, 2 * np.pi, N_DIAMONDS)
D_SPEED = np.random.uniform(8.0, 15.0, N_DIAMONDS) # Rad/sec drop

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f_idx):
    t_sec = f_idx / float(FPS)
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.]); ax.set_axis_off(); fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540); ax.set_ylim(-960, 960)

    # Static Cutaway Frame ensuring deep internal exposure.
    T_MIN = 0.0
    T_MAX = 3.0 * np.pi / 2.0

    faces_collected = []
    face_colors = []
    centroids_z = []
    
    def process_layer(f_faces, h_color, pos_offset):
        # NATIVE SPIN STRIPPED. Geometric shells are completely locked.
        c_rgb = np.array(mcolors.to_rgb(h_color))
        
        for face in f_faces:    
            v1 = face[1] - face[0]; v2 = face[2] - face[0]
            norm = np.cross(v1, v2)
            n_len = np.linalg.norm(norm)
            if n_len > 0: norm /= n_len
            
            diff = 0.4 + 0.6 * np.clip(np.dot(norm, LIGHT_DIR), 0, 1)
            fc = np.append(c_rgb * diff, 1.0)
            
            f_offset = face + pos_offset
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

    def process_kinematic_nodes(n_pts, dr, dphi, dtheta, v_spin, tilt_deg, pos, h_col, size, expose_in_void=False):
        R_tilt = rx(tilt_deg)
        for i in range(n_pts):
            # 1. Base Spherical Coord
            x0 = dr[i] * np.sin(dphi[i]) * np.cos(dtheta[i])
            y0 = dr[i] * np.cos(dphi[i])
            z0 = dr[i] * np.sin(dphi[i]) * np.sin(dtheta[i])
            p0 = np.array([x0, y0, z0])
            
            # 2. Apply explicit rotation matrix (Spin around Y, then Tilt)
            p1 = ry(np.radians(v_spin)) @ p0
            p_final = R_tilt @ p1
            
            # 3. Mathematically evaluate if the final position is inside the static cutaway void
            # The void is defined in absolute World Space (0 to 3*pi/2)
            world_theta = np.arctan2(p_final[2], p_final[0]) % (2 * np.pi)
            is_in_void = (world_theta > T_MAX)
            
            if expose_in_void == is_in_void:
                p_f = generate_particle(p_final, size)
                process_layer(p_f, h_col, pos)

    # ================= PLANET 1: URANUS (Top Axis) =================
    # Kinematic Spallation Event: Uranus explicitly rolls on a 98 degree tilted axis.
    spin_ura = t_sec * 8.0 
    compile_planet(P_URANUS, R_URANUS, [C_URA_CORE, C_URA_MANTLE, C_URA_CRUST])
    process_kinematic_nodes(N_CRUST, U_DR, U_DPHI, U_DTHETA, spin_ura, 98.0, P_URANUS, C_URA_NODE, 6.0, expose_in_void=False)

    # ================= PLANET 2: NEPTUNE (Bottom Axis) =================
    # Supersonic engine: Neptune actively convects and spins violently.
    spin_nep = t_sec * 22.0 
    compile_planet(P_NEPTUNE, R_NEPTUNE, [C_NEP_CORE, C_NEP_MANTLE, C_NEP_CRUST])
    process_kinematic_nodes(N_CRUST, N_DR, N_DPHI, N_DTHETA, spin_nep, 28.3, P_NEPTUNE, C_NEP_NODE, 6.0, expose_in_void=False)
    
    # KINEMATIC DIAMOND RAIN (Exposed explicitly inside Neptune's Mantel Void)
    # They plunge downward kinematically due to gravity exceeding convective buoyancy in this layer.
    for i in range(N_DIAMONDS):
        # Calculate dynamic dropping radius
        r_current = D_DR[i] - (t_sec * D_SPEED[i])
        # Wrap the precipitating carbon around the mantle if it hits the core
        r_range = R_NEPTUNE['mantle'] - R_NEPTUNE['core']
        r_current = R_NEPTUNE['core'] + ((r_current - R_NEPTUNE['core']) % r_range)
        
        # Convective twist as they fall
        c_theta = (D_DTHETA[i] + t_sec * 4.0) % (2 * np.pi)
        
        x = r_current * np.sin(D_DPHI[i]) * np.cos(c_theta)
        y = r_current * np.cos(D_DPHI[i])
        z = r_current * np.sin(D_DPHI[i]) * np.sin(c_theta)
        p_final = rx(28.3) @ np.array([x, y, z])
        
        world_t = np.arctan2(p_final[2], p_final[0]) % (2 * np.pi)
        if world_t > T_MAX:  # Exclusively render inside the internal cutaway void
            p_f = generate_particle(p_final, 5.0)
            process_layer(p_f, C_DIAMOND, P_NEPTUNE)

    # 5. ABSOLUTE DEPENDENCY SORT & RENDER
    sort_idx = np.argsort(centroids_z)[::-1] 
    if faces_collected:
        sorted_faces = [faces_collected[i] for i in sort_idx]
        sorted_fcs = [face_colors[i] for i in sort_idx]
        ax.add_collection(PolyCollection(sorted_faces, facecolors=sorted_fcs, edgecolors='#111115', linewidths=0.25, joinstyle='miter'))

    # LABELS (Calculated directly from the Coplanar Anchors to maintain exact padding)
    def project_label(pos_cam, r_bound, title, subtitle, sub_col):
        scale_mod = 1800.0 / cam_dist
        px = pos_cam[0] * scale_mod
        py = pos_cam[1] * scale_mod - (r_bound * scale_mod) - 40.0
        ax.text(px, py, title, color=C_TEXT, fontsize=20, fontname='monospace', weight='bold', ha='center', zorder=85)
        ax.text(px, py - 30, subtitle, color=sub_col, fontsize=14, fontname='monospace', weight='bold', ha='center', zorder=85)

    project_label(S_URANUS, R_URANUS['crust'], "URANUS", "(THE DEAD ARTEFACT)", C_GUI)
    project_label(S_NEPTUNE, R_NEPTUNE['crust'], "NEPTUNE", "(THE SUPERSONIC ENGINE)", C_NEP_CRUST)

    # 6. HIGH-DENSITY HUD & TELEMETRY
    ax.add_patch(Rectangle((-540, 800), 1080, 160, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=3, zorder=81)
    ax.text(-500, 900, "LG-416 :: THE ICE GIANT TENSORS", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 850, "[SFI-1.00] EXACT COMPARATIVE RADII & KINEMATIC TILT", color=C_URA_MANTLE, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    prog = t_sec / DURATION
    if t_sec < 12.0:
        state_msg = "PHASE 1: THE THERMODYNAMIC EQUILIBRIUM"
        state_col = C_URA_CRUST
        active_op = "URANUS: 98 DEGREE TILT. CORE IS FROZEN. ENGINE DEAD."
    else:
        state_msg = "PHASE 2: THE CONVECTIVE EXTREME"
        state_col = C_NEP_CRUST
        active_op = "NEPTUNE: SUPERSONIC WINDS. O(N) DIAMOND RAIN FRICTION."

    ax.text(-500, -780, f"PROTOCOL STATE : {state_msg}", color=state_col, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"DIAGNOSTIC     : {active_op}", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"AXIOMATIC TRUTH: KINETIC IMPACTS CAN PERMANENTLY DESTROY A PLANETARY HEAT ENGINE.", color=C_TEXT, fontsize=11, fontname='monospace', zorder=82)

    ax.add_patch(Rectangle((-500, -920), 1000, 8, facecolor=C_GUI, zorder=82))
    ax.add_patch(Rectangle((-500, -920), 1000 * prog, 8, facecolor=state_col, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f_idx:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f_idx

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-416 (ICE GIANTS): TENSOR ENGAGED [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            pass
    print("Compilation Complete. Matrix resolved to exact thermodynamic yield.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
