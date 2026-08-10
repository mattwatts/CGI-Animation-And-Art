"""
PROJECT: Logic Garden 403 (The Da Vinci Matrix // Mathematical Drafting)
FORMAT: YouTube Shorts (1080x1920)
METADATA: MECHANICAL ENGINEERING, EXPLODED VIEW, DRAFTING, LEONARDO DA VINCI, GEOMETRY
EXECUTION: 24.0s Sequence. True 3D Mathematical Construction.
RULES ENFORCED:
- Daylight Palette (White Substrate / High Contrast).
- Phase-Locked Metaphor: The Anatomy of a Machine (Explosion and Ink Transition).
- Exact realisational aspect of O(N) interlocking spur gears.
- True Lambertian Shading dynamically transitioning to Ink-Drafted Wireframes.
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
OUT_DIR = "frames_403_davinci"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG            = '#FFFFFF'
C_TEXT          = '#111115'
C_INK           = '#111115'  # Heavy Graphite / Ink Line
C_AXIS          = '#DE008A'  # Deep Magenta Drafting Vector
C_BRASS         = '#D97706'  # Dense Spur Gear
C_IRON          = '#334155'  # Cast Iron Pulley
C_STEEL         = '#94A3B8'  # Machined Shaft
C_GUI           = '#64748B'

LIGHT_DIR = np.array([-0.5, 0.7, -0.6])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

# ------------------------------------------------------------------
# O(1) 3D ARCHITECTURAL HARDWARE GENERATOR
# ------------------------------------------------------------------
def rx(deg):
    rad = np.radians(deg); c, s = np.cos(rad), np.sin(rad)
    return np.array([[1,0,0],[0,c,-s],[0,s,c]])

def ry(rad):
    c, s = np.cos(rad), np.sin(rad)
    return np.array([[c,0,s],[0,1,0],[-s,0,c]])

def make_sector_block(th_start, th_end, r_in, r_out, y_start, y_end, draw_sides=True):
    # Generates O(N) completely convex polygons for mathematically perfect Z-sorting
    p = []
    def pt(r, th, y): return [r*np.cos(th), y, r*np.sin(th)]
    
    p1 = pt(r_in, th_start, y_start); p2 = pt(r_out, th_start, y_start)
    p3 = pt(r_out, th_end, y_start); p4 = pt(r_in, th_end, y_start)
    p5 = pt(r_in, th_start, y_end); p6 = pt(r_out, th_start, y_end)
    p7 = pt(r_out, th_end, y_end); p8 = pt(r_in, th_end, y_end)
    
    p.append([p5, p6, p7, p8]) # Front Face
    p.append([p4, p3, p2, p1]) # Back Face
    p.append([p2, p6, p7, p3]) # Outer Rim
    if r_in > 0:
        p.append([p4, p8, p5, p1]) # Inner Bore
    if draw_sides:
        p.append([p1, p5, p6, p2]) # Wall A
        p.append([p3, p7, p8, p4]) # Wall B
    return p

def generate_axle(length=300, r_hex=20):
    # Precision 6-spline mechanical transmission shaft
    polys = []
    y1, y2 = -length/2, length/2
    for i in range(6):
        th_base = i * 2*np.pi/6
        dt = 2*np.pi/6
        polys.extend(make_sector_block(th_base, th_base+dt, 0, r_hex, y1, y2, draw_sides=False))
    return np.array(polys)

def generate_pulley(r_hub=20.5, r_root=60, r_rim=70, depth=30):
    polys = []
    y1, y2 = -depth/2, depth/2
    segs = 24
    for i in range(segs):
        th_base = i * 2*np.pi/segs
        dt = 2*np.pi/segs
        # Central Web (Tapped to slide over splines perfectly)
        polys.extend(make_sector_block(th_base, th_base+dt, r_hub, r_root, y1, y2, draw_sides=False))
        # Raised Edge Rim 
        polys.extend(make_sector_block(th_base, th_base+dt, r_root-1, r_rim, y1-6, y2+6, draw_sides=False)) 
    return np.array(polys)

def generate_gear(teeth=12, r_hub=20.5, r_root=45, r_tip=56, depth=20):
    polys = []
    y1, y2 = -depth/2, depth/2
    for i in range(teeth):
        th_base = i * 2*np.pi/teeth
        dt = 2*np.pi/teeth
        # Structural Ring
        polys.extend(make_sector_block(th_base, th_base+dt, r_hub, r_root, y1, y2, draw_sides=False))
        # Extruded Geared Tooth Profile
        polys.extend(make_sector_block(th_base+dt*0.25, th_base+dt*0.75, r_root, r_tip, y1, y2, draw_sides=True))
    return np.array(polys)

def generate_collar(r_in=20.5, r_out=35, depth=24):
    polys = []
    y1, y2 = -depth/2, depth/2
    for i in range(6): # Brutalist Hexagonal Locking Cap
        th_base = i * 2*np.pi/6
        dt = 2*np.pi/6
        polys.extend(make_sector_block(th_base, th_base+dt, r_in, r_out, y1, y2, draw_sides=False))
    return np.array(polys)

print("PHASE 1: PRE-COMPUTING ARCHITECTURAL MESH TENSORS...")
# Base Origin Geometries
P_AXLE = generate_axle(length=300, r_hex=20)
P_PULL = generate_pulley(depth=26)
P_GEAR = generate_gear(depth=20)
P_CAP  = generate_collar(depth=24)

# Native Assembled Axial Topology
Y0_AXLE = 0.0
Y0_PULL = -50.0  
Y0_GEAR = 35.0
Y0_CAP = 85.0

# ------------------------------------------------------------------
# O(1) TIMELINE EASE FUNCTIONS
# ------------------------------------------------------------------
def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f_idx):
    t_sec = f_idx / float(FPS)
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.]); ax.set_axis_off(); fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540); ax.set_ylim(-960, 960)

    # 1. MATHEMATICAL PHASE TENSORS
    # E_val: Separation Magnitude (0 to 1) 
    E_val = smoothstep((t_sec - 4.0)/3.0) - smoothstep((t_sec - 16.0)/3.0)
    # I_val: Ink Transition Magnitude (0 to 1)
    I_val = smoothstep((t_sec - 8.0)/3.0) - smoothstep((t_sec - 19.0)/3.0)
    
    # Absolute Kinematic Spin
    # The assembly spins continuously, proving the spline lock.
    sys_rot = ry(t_sec * 1.5)
    
    cam_pitch = -25.0
    M_cam = rx(cam_pitch)
    cam_dist = 1400.0

    queue = []
    
    # 2. EVALUATE PROJECTIVE MATRIX STATE
    def project_geometry(polys, y_off, color_hex):
        if len(polys) == 0: return []
        
        # O(1) Axial Slide Math
        offset_tensor = np.array([0.0, y_off, 0.0])
        translated = polys + offset_tensor
        
        # True System Rotation
        rotated = np.dot(translated, sys_rot.T)
        
        v_cam = np.einsum('ij,knj->kni', M_cam, rotated)
        v_cam[:, :, 2] += cam_dist
        
        centroids_z = np.mean(v_cam[:, :, 2], axis=1)
        v1 = v_cam[:, 1, :] - v_cam[:, 0, :]
        v2 = v_cam[:, 2, :] - v_cam[:, 0, :]
        norms = np.cross(v1, v2)
        n_len = np.linalg.norm(norms, axis=1, keepdims=True)
        norms /= np.maximum(n_len, 1e-5)
        
        # If deeply inked, we render all faces for structural wireframe overlap. 
        # If solid, we strict cull.
        if I_val > 0.5:
            v_mask = centroids_z > 1.0 
        else:
            v_mask = norms[:, 2] > 0
            
        v_cull = v_cam[v_mask]
        norms_cull = norms[v_mask]
        z_cull = centroids_z[v_mask]
        
        # Base Lambertian Shader
        diff = 0.2 + 0.8 * np.abs(np.dot(norms_cull, LIGHT_DIR))
        c_metal = np.array(mcolors.to_rgb(color_hex))
        c_paper = np.array(mcolors.to_rgb(C_BG))
        
        fcs = np.zeros((len(v_cull), 4))
        for i in range(len(v_cull)):
            f_rgb = (c_metal * diff[i]) * (1.0 - I_val) + c_paper * I_val
            f_alpha = 1.0 * (1.0 - I_val) + 0.85 * I_val # Ink transition becomes translucent paper
            fcs[i, :3] = f_rgb
            fcs[i, 3] = f_alpha
            
        # Parametric Edge Generation (Blueprint enforcement)
        e_rgb = c_metal * 0.4 * (1.0 - I_val) + np.array(mcolors.to_rgb(C_INK)) * I_val
        ecs = np.zeros((len(v_cull), 4))
        for i in range(len(v_cull)):
            ecs[i, :3] = e_rgb
            ecs[i, 3] = 1.0
            
        lw = (0.2 * (1.0 - I_val)) + (1.2 * I_val)

        px = 3000.0 * (v_cull[:, :, 0] / v_cull[:, :, 2])
        py = 3000.0 * (v_cull[:, :, 1] / v_cull[:, :, 2]) - 20

        polys_2d = np.stack((px, py), axis=-1)
        return [{'sz': z, 'dat': p, 'fc': c, 'ec': e, 'lw': lw, 't': 'P'} for z, p, c, e in zip(z_cull, polys_2d, fcs, ecs)]

    # Dynamic Explosion Translations
    # Axial displacement pushing components safely apart for pure visibility
    e_y_axle = Y0_AXLE
    e_y_pull = Y0_PULL - (180.0 * E_val) 
    e_y_gear = Y0_GEAR + (160.0 * E_val)
    e_y_cap  = Y0_CAP  + (270.0 * E_val)

    queue.extend(project_geometry(P_AXLE, e_y_axle, C_STEEL))
    queue.extend(project_geometry(P_PULL, e_y_pull, C_IRON))
    queue.extend(project_geometry(P_GEAR, e_y_gear, C_BRASS))
    queue.extend(project_geometry(P_CAP, e_y_cap,  C_STEEL))

    # Optional: Leonardos Drafting Axis Vector
    if E_val > 0.05:
        p1_w = np.array([0.0, -350.0, 0.0])
        p2_w = np.array([0.0, 420.0, 0.0])
        p1_c = M_cam @ p1_w; p1_c[2] += cam_dist
        p2_c = M_cam @ p2_w; p2_c[2] += cam_dist
        
        px1 = 3000.0 * (p1_c[0] / p1_c[2])
        py1 = 3000.0 * (p1_c[1] / p1_c[2]) - 20
        px2 = 3000.0 * (p2_c[0] / p2_c[2])
        py2 = 3000.0 * (p2_c[1] / p2_c[2]) - 20
        
        c_ax = np.array(mcolors.to_rgb(C_AXIS))
        rgba_ax = np.array([c_ax[0], c_ax[1], c_ax[2], E_val])
        # Force axis below closest blocks but above deep ones roughly
        queue.append({'sz': cam_dist, 'dat': [[px1, py1], [px2, py2]], 'fc': rgba_ax, 'lw': 3.0, 't': 'L'})

    # 3. ABSOLUTE DEPTH SORT (O(N log N))
    queue.sort(key=lambda x: x['sz'], reverse=True)
    
    b_poly, b_fc, b_ec, b_lw = [], [], [], []
    for item in queue:
        if item['t'] == 'P':
            b_poly.append(item['dat'])
            b_fc.append(item['fc'])
            b_ec.append(item['ec'])
            b_lw.append(item['lw'])
        else:
            if b_poly:
                ax.add_collection(PolyCollection(b_poly, facecolors=b_fc, edgecolors=b_ec, linewidths=b_lw, joinstyle='miter'))
                b_poly, b_fc, b_ec, b_lw = [], [], [], []
            ax.add_collection(LineCollection([item['dat']], colors=[item['fc']], linewidths=[item['lw']], linestyles='--'))

    if b_poly:
        ax.add_collection(PolyCollection(b_poly, facecolors=b_fc, edgecolors=b_ec, linewidths=b_lw, joinstyle='miter'))

    # 4. HIGH-DENSITY PROTOCOL HUD
    ax.add_patch(Rectangle((-540, 780), 1080, 180, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [780, 780], color=C_TEXT, lw=3, zorder=81)
    ax.text(-500, 880, "LG-403 :: THE DA VINCI MATRIX", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 830, "[SFI-1.00] MATHEMATICAL DRAFTING // THE EXPLODED VIEW", color=C_GUI, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    if I_val > 0.4:
        state_msg = "PHASE 3: STRUCTURAL WIREFRAME (DA VINCI MAPPING ACTIVE)"
        state_col = C_INK
        t_prog = I_val
    elif E_val > 0.05:
        state_msg = "PHASE 2: AXIAL TENSOR SEPARATION (EXPLODED VIEW)"
        state_col = C_AXIS
        t_prog = E_val
    else:
        state_msg = "PHASE 1: SOLID KINEMATIC LOCK"
        state_col = C_BRASS
        t_prog = 1.0

    ax.text(-500, -780, f"CURRENT STATE: {state_msg}", color=state_col, fontsize=16, fontname='monospace', weight='bold', zorder=82)

    str_disp = f"Y-AXIAL TRANSLATION MAGNITUDE: {(E_val * 270):06.2f} MM"
    ax.text(-500, -830, str_disp, color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"AXIOMATIC TRUTH: TO KNOW THE WHOLE, SEVER IT INTO ITS EXACT PARTS.", color=C_TEXT, fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(Rectangle((-500, -920), 1000, 8, facecolor=C_GUI, zorder=82))
    ax.add_patch(Rectangle((-500, -920), 1000 * t_prog, 8, facecolor=state_col, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f_idx:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f_idx

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-403: DA VINCI MATRIX ENGAGED [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")
    print("Compilation Complete. Technical Drawing Variables isolated.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
