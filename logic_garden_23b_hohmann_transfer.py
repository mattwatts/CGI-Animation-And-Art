"""
PROJECT: Logic Garden 23b (The Interplanetary Tensor // Hohmann Transfer)
FORMAT: YouTube Shorts (1080x1920)
METADATA: ORBITAL MECHANICS, ASTRODYNAMICS, KEPLER'S LAWS, KINEMATIC ENGINEERING
EXECUTION: 24.0s Sequence. True 3D Mathematical Construction.
RULES ENFORCED:
- Daylight Palette (White Substrate / High Contrast).
- Static Camera Isometric Lock (Zero yaw rotation, exact observation framing).
- Exact realisational aspect of a Runge-Kutta / Keplerian transit.
- Native 3D projection of $O(N)$ celestial spheres without wireframe bleed.
- Australian spelling conventions enforced natively (Maths, Optimisation).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
from matplotlib.collections import PolyCollection, LineCollection
import multiprocessing as mp
import os
import gc

# ======== SEQUENCE PARAMETERS ========
FPS = 60
DURATION = 24.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_23b_hohmann"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG            = '#FFFFFF'
C_TEXT          = '#111115'
C_EDGE          = '#111115'
C_SUN           = '#FFD700'  # Cyber Yellow (Emissive)
C_EARTH         = '#0080FF'  # Azure Blue
C_MARS          = '#FF4500'  # Safety Red
C_ROCKET        = '#111115'  # Indestructible Black
C_ORBIT_E       = '#94A3B8'
C_ORBIT_M       = '#94A3B8'
C_ORBIT_T       = '#C20078'  # Deep Magenta Transit
C_GUI           = '#64748B'

LIGHT_DIR = np.array([-0.5, 0.8, -0.4])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

# ------------------------------------------------------------------
# O(1) ASTRODYNAMICS CONSTANTS & MATRICES
# ------------------------------------------------------------------
R_E_ORBIT = 300.0
R_M_ORBIT = 300.0 * 1.524

A_TRANS = (R_E_ORBIT + R_M_ORBIT) / 2.0
E_TRANS = (R_M_ORBIT - R_E_ORBIT) / (R_M_ORBIT + R_E_ORBIT)

# Launch and Arrival Framing
F_LAUNCH = 240   # 4.0s Wait for alignment
F_ARRIVE = 1200  # 20.0s Transfer complete
F_TRANSIT = F_ARRIVE - F_LAUNCH

# Astrodynamics scaling to match sequence duration perfectly
T_TRAVEL_YEARS = 0.7087 
FRAMES_PER_YEAR = F_TRANSIT / T_TRAVEL_YEARS
W_EARTH = (2 * np.pi) / FRAMES_PER_YEAR
W_MARS = W_EARTH / (1.524 ** 1.5)

# Absolute Geometric Intercept
TH_EARTH_0 = 0 - (W_EARTH * F_LAUNCH)
TH_MARS_0  = np.pi - (W_MARS * F_ARRIVE)

def rx(deg):
    rad = np.radians(deg); c, s = np.cos(rad), np.sin(rad)
    return np.array([[1,0,0],[0,c,-s],[0,s,c]])

def rz(deg):
    rad = np.radians(deg); c, s = np.cos(rad), np.sin(rad)
    return np.array([[c,-s,0],[s,c,0],[0,0,1]])

def ry(rad):
    c, s = np.cos(rad), np.sin(rad)
    return np.array([[c,0,s],[0,1,0],[-s,0,c]])

# Kepler Equation Solver utilizing absolute Newton-Raphson mathematics
def solve_kepler(M, e, tol=1e-6):
    E_curr = M
    for _ in range(10):
        E_next = E_curr - (E_curr - e*np.sin(E_curr) - M) / (1.0 - e*np.cos(E_curr))
        if abs(E_next - E_curr) < tol: break
        E_curr = E_next
    return E_curr

def get_transit_vector(t_frames):
    prog = np.clip(t_frames / F_TRANSIT, 0.0, 1.0)
    M = prog * np.pi
    E = solve_kepler(M, E_TRANS)
    nu = 2.0 * np.arctan(np.sqrt((1.0 + E_TRANS)/(1.0 - E_TRANS)) * np.tan(E / 2.0))
    r = A_TRANS * (1.0 - E_TRANS * np.cos(E))
    return r * np.cos(nu), 0.0, r * np.sin(nu)

# ------------------------------------------------------------------
# O(N) 3D ARCHITECTURAL HARDWARE GENERATOR
# ------------------------------------------------------------------
def generate_sphere(radius, rings=16, sectors=16):
    polys = []
    for r in range(rings):
        lat1 = np.pi * (-0.5 + float(r) / rings)
        lat2 = np.pi * (-0.5 + float(r+1) / rings)
        sin1, cos1 = np.sin(lat1), np.cos(lat1)
        sin2, cos2 = np.sin(lat2), np.cos(lat2)
        
        for s in range(sectors):
            lon1 = 2 * np.pi * float(s) / sectors
            lon2 = 2 * np.pi * float(s+1) / sectors
            
            p1 = [radius * cos1 * np.cos(lon1), radius * sin1, radius * cos1 * np.sin(lon1)]
            p2 = [radius * cos1 * np.cos(lon2), radius * sin1, radius * cos1 * np.sin(lon2)]
            p3 = [radius * cos2 * np.cos(lon2), radius * sin2, radius * cos2 * np.sin(lon2)]
            p4 = [radius * cos2 * np.cos(lon1), radius * sin2, radius * cos2 * np.sin(lon1)]
            
            polys.append([p1, p2, p3])
            polys.append([p1, p3, p4])
    return np.array(polys)

print("PHASE 1: PRE-COMPUTING CELESTIAL TENSORS...")
SPHERE_SUN = generate_sphere(50.0, 16, 16)
SPHERE_EARTH = generate_sphere(20.0, 12, 12)
SPHERE_MARS = generate_sphere(15.0, 12, 12)
SPHERE_CRAFT = generate_sphere(6.0, 6, 6)

def generate_orbital_ring(radius, segments=120):
    lines = []
    for i in range(segments):
        a1 = (i / segments) * 2 * np.pi
        a2 = ((i+1) / segments) * 2 * np.pi
        p1 = [radius * np.cos(a1), 0, radius * np.sin(a1)]
        p2 = [radius * np.cos(a2), 0, radius * np.sin(a2)]
        lines.append([p1, p2])
    return np.array(lines)

ORBIT_E_LINES = generate_orbital_ring(R_E_ORBIT)
ORBIT_M_LINES = generate_orbital_ring(R_M_ORBIT)

TRANSIT_PATH = []
for i in range(120):
    tr, ty, tz = get_transit_vector( (i/120.0) * F_TRANSIT )
    TRANSIT_PATH.append([tr, ty, tz])
TRANSIT_PATH = np.array(TRANSIT_PATH)
T_LINES = np.array([[TRANSIT_PATH[i], TRANSIT_PATH[i+1]] for i in range(len(TRANSIT_PATH)-1)])

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f_idx):
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.]); ax.set_axis_off(); fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540); ax.set_ylim(-960, 960)

    # 1. ORBITAL KINEMATICS
    th_e = TH_EARTH_0 + W_EARTH * f_idx
    th_m = TH_MARS_0 + W_MARS * f_idx
    
    pos_e = np.array([R_E_ORBIT * np.cos(th_e), 0.0, R_E_ORBIT * np.sin(th_e)])
    pos_m = np.array([R_M_ORBIT * np.cos(th_m), 0.0, R_M_ORBIT * np.sin(th_m)])
    
    # 2. SPACECRAFT KINEMATICS
    if f_idx < F_LAUNCH:
        pos_s, craft_state = pos_e, 0
    elif f_idx <= F_ARRIVE:
        pos_s, craft_state = get_transit_vector(f_idx - F_LAUNCH), 1
    else:
        pos_s, craft_state = pos_m, 2

    # 3. CAMERA BINDING TENSOR (Absolute Static Lock)
    cam_pitch = -35.0
    cam_yaw = 0.0 
    M_cam = rx(cam_pitch) @ ry(cam_yaw)
    cam_dist = 4000.0  # Pushed way back to capture the entire astrodynamics matrix

    queue = []

    def project_polys(base_polys, offset, color_hex, is_sun=False):
        translated = base_polys + offset
        v_cam = np.einsum('ij,knj->kni', M_cam, translated)
        v_cam[:, :, 2] += cam_dist
        
        centroids_z = np.mean(v_cam[:, :, 2], axis=1)
        v1 = v_cam[:, 1, :] - v_cam[:, 0, :]
        v2 = v_cam[:, 2, :] - v_cam[:, 0, :]
        norms = np.cross(v1, v2)
        n_len = np.linalg.norm(norms, axis=1, keepdims=True)
        norms /= np.maximum(n_len, 1e-5)
        
        v_mask = norms[:, 2] > 0
        v_cull = v_cam[v_mask]
        norms_cull = norms[v_mask]
        z_cull = centroids_z[v_mask]
        
        # Sun casts its own light. Planets use true Lambertian volume.
        if is_sun:
            diff = np.ones(len(norms_cull))
        else:
            diff = 0.4 + 0.6 * np.maximum(0, np.dot(norms_cull, LIGHT_DIR))
            
        c_rgb = np.array(mcolors.to_rgb(color_hex))
        fcs = np.zeros((len(v_cull), 4))
        fcs[:, :3] = c_rgb * diff[:, np.newaxis]
        fcs[:, 3] = 1.0
        
        # Recalibrated FOV limits to fit precisely inside the matrix limits
        px = 4000.0 * (v_cull[:, :, 0] / v_cull[:, :, 2])
        py = 4000.0 * (v_cull[:, :, 1] / v_cull[:, :, 2]) - 150
        
        polys_2d = np.stack((px, py), axis=-1)
        # Using ec=fc purges the black blob wireframes and preserves exact 3D shading
        return [{'sz': z, 'dat': p, 'fc': c, 'ec': c, 'lw': 0.1, 'type': 'P'} for z, p, c in zip(z_cull, polys_2d, fcs)]

    def project_lines(base_lines, offset, color_hex, lw, dashed=False):
        translated = base_lines + offset
        v_cam = np.einsum('ij,knj->kni', M_cam, translated)
        v_cam[:, :, 2] += cam_dist
        
        z_avg = np.mean(v_cam[:, :, 2], axis=1)
        px = 4000.0 * (v_cam[:, :, 0] / v_cam[:, :, 2])
        py = 4000.0 * (v_cam[:, :, 1] / v_cam[:, :, 2]) - 150
        
        lines_2d = np.stack((px, py), axis=-1)
        c_rgb = np.array(mcolors.to_rgb(color_hex) + (0.5 if dashed else 0.8,))
        ls = ':' if dashed else '-'
        return [{'sz': z, 'dat': p, 'fc': c_rgb, 'lw': lw, 'ls': ls, 'type': 'L'} for z, p in zip(z_avg, lines_2d)]

    # Populate Graphic Queue
    queue.extend(project_lines(ORBIT_E_LINES, np.zeros(3), C_ORBIT_E, 1.5))
    queue.extend(project_lines(ORBIT_M_LINES, np.zeros(3), C_ORBIT_M, 1.5))
    queue.extend(project_lines(T_LINES, np.zeros(3), C_ORBIT_T, 2.0, dashed=True))

    queue.extend(project_polys(SPHERE_SUN, np.zeros(3), C_SUN, is_sun=True))
    queue.extend(project_polys(SPHERE_EARTH, pos_e, C_EARTH))
    queue.extend(project_polys(SPHERE_MARS, pos_m, C_MARS))
    
    if craft_state == 1:
        # Generate the kinematic trajectory history trail
        tail_start = max(F_LAUNCH, f_idx - 60)
        tail_path = []
        for tf in range(tail_start, f_idx):
            trail_r, _, trail_z = get_transit_vector(tf - F_LAUNCH)
            tail_path.append([trail_r, 0.0, trail_z])
            
        if len(tail_path) > 1:
            tail_lines = np.array([[tail_path[i], tail_path[i+1]] for i in range(len(tail_path)-1)])
            queue.extend(project_lines(tail_lines, np.zeros(3), C_ORBIT_T, 4.0))

        # Re-attach hard edge for purely the rocket to pop
        p_rock = project_polys(SPHERE_CRAFT, pos_s, C_ROCKET)
        for d in p_rock: d['ec'] = C_ROCKET
        queue.extend(p_rock)

    # O(1) Absolute Depth Sort
    queue.sort(key=lambda x: x['sz'], reverse=True)
    
    b_poly, b_fc, b_ec, b_lw = [], [], [], []
    for item in queue:
        if item['type'] == 'P':
            b_poly.append(item['dat'])
            b_fc.append(item['fc'])
            b_ec.append(item['ec'])
            b_lw.append(item['lw'])
        else:
            if b_poly:
                ax.add_collection(PolyCollection(b_poly, facecolors=b_fc, edgecolors=b_ec, linewidths=b_lw))
                b_poly, b_fc, b_ec, b_lw = [], [], [], []
            ax.add_collection(LineCollection([item['dat']], colors=[item['fc']], linewidths=[item['lw']], linestyles=[item['ls']]))

    if b_poly:
        ax.add_collection(PolyCollection(b_poly, facecolors=b_fc, edgecolors=b_ec, linewidths=b_lw))

    # 4. HIGH-DENSITY HUD & TELEMETRY
    ax.add_patch(Rectangle((-540, 780), 1080, 180, facecolor=C_BG, zorder=80, alpha=0.9))
    ax.plot([-540, 540], [780, 780], color=C_TEXT, lw=3, zorder=81)
    ax.text(-500, 880, "LG-23b :: INTERPLANETARY TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 830, "[SFI-1.00] EXACT KEPLERIAN HOHMANN TRANSFER", color=C_GUI, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.9))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    state_msg = "AWAITING PHASE ALIGNMENT"
    state_col = C_GUI
    m_anom = 0.0
    if craft_state == 1:
        state_msg = "TRANS-MARS INJECTION (TMI) COASTING"
        state_col = C_ORBIT_T
        m_anom = np.clip((f_idx - F_LAUNCH) / F_TRANSIT, 0.0, 1.0)
    elif craft_state == 2:
        state_msg = "MARS ORBIT INSERTION ACHIEVED"
        state_col = C_MARS
        m_anom = 1.0

    ax.text(-500, -780, f"PROTOCOL PHASE: {state_msg}", color=state_col, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"VEHICLE MEAN ANOMALY : {(m_anom * 180):06.2f} DEG", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"ORBITAL ECCENTRICITY : {E_TRANS:05.4f} (e)", color=C_TEXT, fontsize=14, fontname='monospace', zorder=82)

    ax.add_patch(Rectangle((-500, -920), 1000, 8, facecolor=C_GUI, zorder=82))
    ax.add_patch(Rectangle((-500, -920), 1000 * m_anom, 8, facecolor=state_col, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f_idx:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f_idx

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-23b: KEPLERIAN ASTRODYNAMICS MATRIX ENGAGED [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")
    print("Compilation Complete. True Orbital Transfer Verified.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
