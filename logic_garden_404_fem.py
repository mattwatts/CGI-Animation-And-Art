"""
PROJECT: Logic Garden 404 (The Finite Element Matrix // High-Contrast Spallation)
FORMAT: YouTube Shorts (1080x1920)
METADATA: FINITE ELEMENT METHOD, STRUCTURAL ENGINEERING, KINEMATICS, YIELD ANALYSIS
EXECUTION: 24.0s Sequence. True 3D Mathematical Construction.
RULES ENFORCED:
- Daylight Palette (White Substrate / High-Contrast Chrome).
- Phase-Locked Metaphor: Explosive Spallation and Catastrophic Severing.
- Exact realisational aspect of O(N) volumetric tensor arrays and Von Mises yield.
- Australian spelling conventions enforced natively (Maths, Colour, Optimise).
- Absolute Baseplate Contrast (Bright Machined Aluminium).
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
OUT_DIR = "frames_404_fem"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG            = '#FFFFFF'
C_TEXT          = '#111115'
C_EDGE          = '#111115'
C_FAIL          = '#111115'  # Indestructible Black
C_FAIL_EDGE     = '#DE008A'  # Deep Magenta Spallation Border
C_FORCE         = '#DE008A'  # Deep Magenta Load Vector
C_ANCHOR        = '#E2E8F0'  # Bright Machined Aluminium (High Contrast Substrate)
C_GUI           = '#64748B'

# Aggressive Heatmap Palette (Colour mapping)
C_COLD          = '#00D2FF'  # High-Contrast Cyan (Zero Stress)
C_SAFE          = '#00C853'  # Jade (Nominal Load)
C_WARN          = '#FFB300'  # Dense Amber (High Stress)
C_CRIT          = '#FF3300'  # Intense Red (Critical Yield)

LIGHT_DIR = np.array([-0.5, 0.7, -0.6])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

# ------------------------------------------------------------------
# O(1) 3D ARCHITECTURAL MESH GENERATOR
# ------------------------------------------------------------------
L_TOTAL = 500.0  
H_TOTAL = 120.0  
W_TOTAL = 60.0   

NX, NY, NZ = 40, 10, 6 
DX, DY, DZ = L_TOTAL/NX, H_TOTAL/NY, W_TOTAL/NZ

# Kinematic Timing Overrides
T_EXTRUDE = 2.0
T_SNAP = 13.0

ELEMENTS = []
np.random.seed(404)

for ix in range(NX):
    for iy in range(NY):
        for iz in range(NZ):
            # I-Beam Topology Filter
            if (iy < 2) or (iy >= NY - 2) or (iz == 2 or iz == 3):
                cx = ix * DX + DX/2
                cy = iy * DY + DY/2 - H_TOTAL/2 
                cz = iz * DZ + DZ/2 - W_TOTAL/2
                
                # Yield mapping
                e_stress = ((L_TOTAL - cx) / L_TOTAL) * ((abs(cy) / (H_TOTAL/2))**0.7)
                
                # Explosive Kinematics for Root Spallation
                vx = np.random.uniform(-400, 600)
                vy = np.random.uniform(-300, 1000)
                vz = np.random.uniform(-500, 500)
                r_spd = np.random.uniform(-5.0, 5.0)

                ELEMENTS.append({'cx': cx, 'cy': cy, 'cz': cz, 'est': e_stress,
                                 'vx': vx, 'vy': vy, 'vz': vz, 'rspd': r_spd})

BASE_CUBE = np.array([
    [[-1,-1, 1], [ 1,-1, 1], [ 1, 1, 1], [-1, 1, 1]], # Front
    [[-1,-1,-1], [-1, 1,-1], [ 1, 1,-1], [ 1,-1,-1]], # Back
    [[-1, 1,-1], [-1, 1, 1], [ 1, 1, 1], [ 1, 1,-1]], # Top
    [[-1,-1,-1], [ 1,-1,-1], [ 1,-1, 1], [-1,-1, 1]], # Bottom
    [[ 1,-1,-1], [ 1, 1,-1], [ 1, 1, 1], [ 1,-1, 1]], # Right
    [[-1,-1,-1], [-1,-1, 1], [-1, 1, 1], [-1, 1,-1]]  # Left
])
SCALE_MAT = np.array([DX*0.48, DY*0.48, DZ*0.48]) # Strict gaps to prove discrete blocks

print(f"PHASE 1: MESH TENSOR PRE-COMPILED [{len(ELEMENTS)} NODES]")

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

def ease_out(t): return np.clip(1.0 - (1.0 - np.clip(t, 0, 1))**3, 0.0, 1.0)
def ease_in_out(t): return np.clip(t*t*(3 - 2*t), 0.0, 1.0)

def get_heat_colour(s_val):
    s = np.clip(s_val, 0.0, 1.0)
    cya = np.array(mcolors.to_rgb(C_COLD))
    jad = np.array(mcolors.to_rgb(C_SAFE))
    amb = np.array(mcolors.to_rgb(C_WARN))
    red = np.array(mcolors.to_rgb(C_CRIT))
    
    if s < 0.33: return cya * (1 - s/0.33) + jad * (s/0.33)
    elif s < 0.66: return jad * (1 - (s-0.33)/0.33) + amb * ((s-0.33)/0.33)
    else: return amb * (1 - (s-0.66)/0.34) + red * ((s-0.66)/0.34)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f_idx):
    t_sec = f_idx / float(FPS)
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.]); ax.set_axis_off(); fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540); ax.set_ylim(-960, 960)

    # 1. KINEMATIC TIMELINE (High Motion)
    extrude_prog = ease_out(t_sec / T_EXTRUDE)
    
    if t_sec < T_EXTRUDE:
        load = 0.0
        shudder = 0.0
    elif t_sec < T_SNAP:
        l_prog = (t_sec - T_EXTRUDE) / (T_SNAP - T_EXTRUDE)
        load = ease_in_out(l_prog)
        # Aggressive mechanical resonance as stress builds
        shudder = np.sin(t_sec * 30.0) * 12.0 * (l_prog ** 3) 
    else:
        load = 1.0
        shudder = 0.0

    # Max tip deflection: massive 220 units to create immense visual arch
    k_bend = load * 220.0 + shudder

    # Calculate absolute failure state parameters at T_SNAP mathematically
    k_fail = 220.0
    def fail_v(x): return k_fail * (3 * L_TOTAL * x**2 - x**3) / (2 * L_TOTAL**3)
    def fail_th(x): return k_fail * (6 * L_TOTAL * x - 3 * x**2) / (2 * L_TOTAL**3)

    M_cam = rx(-18.0) @ ry(-42.0)
    cam_dist = 2400.0
    
    queue = []
    
    for el in ELEMENTS:
        cx, cy, cz = el['cx'], el['cy'], el['cz']
        e_str = el['est']
        
        cxi = cx * extrude_prog 
        
        # Determine geometric state
        if t_sec >= T_SNAP:
            dt = t_sec - T_SNAP
            
            if cx < 120:
                # ROOT SPALLATION: Violent explosion of shattered finite elements
                is_failed = True
                
                # Start from frozen failure position
                fx = cx - cy * np.sin(fail_th(cx))
                fy = cy * np.cos(fail_th(cx)) - fail_v(cx)
                
                nx = fx + el['vx'] * dt
                ny = fy + el['vy'] * dt - 0.5 * 1500 * (dt**2)
                nz = cz + el['vz'] * dt
                
                # Apply tumbling rotation
                R_dyn = rz(el['rspd'] * dt) @ rx(el['rspd'] * dt * 0.5)
                
                base = BASE_CUBE * SCALE_MAT
                spin_pts = np.dot(base, R_dyn.T)
                transformed_faces = spin_pts + np.array([nx, ny, nz])
                
            else:
                # CATASTROPHIC SEVERANCE: The entire tip beam falls as a rigid body
                is_failed = False
                
                # Lock local relative positions to the failure curve
                fx = cx - cy * np.sin(fail_th(cx))
                fy = cy * np.cos(fail_th(cx)) - fail_v(cx)
                
                # Global Rigid Body Drop
                fall_y = - 0.5 * 1800 * (dt**2)
                fall_th_g = - 1.2 * dt 
                fall_x = 100 * dt 
                
                # Rotate entire chunk around severed root roughly at X=120
                pivot_x, pivot_y = 120.0, -fail_v(120.0)
                
                px, py = fx - pivot_x, fy - pivot_y
                c_rot, s_rot = np.cos(fall_th_g), np.sin(fall_th_g)
                rx_p = px * c_rot - py * s_rot
                ry_p = px * s_rot + py * c_rot
                
                nx = pivot_x + rx_p + fall_x
                ny = pivot_y + ry_p + fall_y
                nz = cz
                
                # Poly orientation also follows falling theta + inherent bend
                base = BASE_CUBE * SCALE_MAT
                combined_th = fail_th(cx) + fall_th_g
                R_dyn = rz(-combined_th)
                transformed_faces = np.dot(base, R_dyn.T) + np.array([nx, ny, nz])

        else:
            is_failed = False
            # DYNAMIC LOAD: Polynomial cantilever arching
            v_b = k_bend * (3 * L_TOTAL * cxi**2 - cxi**3) / (2 * L_TOTAL**3)
            th_b = k_bend * (6 * L_TOTAL * cxi - 3 * cxi**2) / (2 * L_TOTAL**3)
            
            nx = cxi - cy * np.sin(th_b)
            ny = cy * np.cos(th_b) - v_b
            nz = cz
            
            base = BASE_CUBE * SCALE_MAT
            transformed_faces = np.dot(base, rz(-th_b).T) + np.array([nx, ny, nz])

        # Shift to center the simulation horizontally
        translated = transformed_faces - np.array([L_TOTAL/2 - 50.0, 0.0, 0.0])
        
        v_cam = np.einsum('ij,knj->kni', M_cam, translated)
        v_cam[:, :, 2] += cam_dist
        
        centroids_z = np.mean(v_cam[:, :, 2], axis=1)
        v1 = v_cam[:, 1, :] - v_cam[:, 0, :]
        v2 = v_cam[:, 2, :] - v_cam[:, 0, :]
        norms = np.cross(v1, v2)
        
        # Depth face culling
        v_mask = norms[:, 2] > 0
        if not np.any(v_mask): continue
        
        v_c = v_cam[v_mask]
        n_c = norms[v_mask]
        z_c = centroids_z[v_mask]
        
        n_len = np.linalg.norm(n_c, axis=1)
        n_c = n_c / np.maximum(n_len, 1e-5)[:, np.newaxis]
        diff = 0.3 + 0.7 * np.maximum(0, np.dot(n_c, LIGHT_DIR))

        if is_failed:
            c_base = np.array(mcolors.to_rgb(C_FAIL))
            lw_cur, ec_cur = 0.8, C_FAIL_EDGE 
        else:
            # Searing Von Mises Heatmap Mapping
            c_heat = get_heat_colour(load * e_str * 1.2) 
            c_base = c_heat
            lw_cur, ec_cur = 0.8, C_EDGE

        fcs = np.zeros((len(v_c), 4))
        fcs[:, :3] = c_base * diff[:, np.newaxis]
        fcs[:, 3] = 1.0

        px = 4000.0 * (v_c[:, :, 0] / v_c[:, :, 2])
        py = 4000.0 * (v_c[:, :, 1] / v_c[:, :, 2]) - 100.0
        
        polys_2d = np.stack((px, py), axis=-1)
        
        for z, p, fc in zip(z_c, polys_2d, fcs):
            queue.append({'sz': z, 'dat': p, 'fc': fc, 'ec': ec_cur, 'lw': lw_cur})

    # ------------------------------------------------------------------
    # BASEPLATE (Highly Contrasting Lighter Solid Aluminium Anchor Wall)
    # ------------------------------------------------------------------
    if True: 
        bp_local = np.array([
            [[-50, -400, -200], [0, -400, -200], [0, 400, -200], [-50, 400, -200]], # Left
            [[-50, -400,  200], [0, -400,  200], [0, 400,  200], [-50, 400,  200]], # Right
            [[0, -400, -200], [0, -400, 200], [0, 400, 200], [0, 400, -200]]        # Front
        ])
        
        bp = bp_local - np.array([L_TOTAL/2 - 50.0, 0.0, 0.0])
        
        v_cam = np.einsum('ij,knj->kni', M_cam, bp)
        v_cam[:, :, 2] += cam_dist
        px = 4000.0 * (v_cam[:, :, 0] / v_cam[:, :, 2])
        py = 4000.0 * (v_cam[:, :, 1] / v_cam[:, :, 2]) - 100.0
        p2d = np.stack((px, py), axis=-1)
        z_c = np.mean(v_cam[:, :, 2], axis=1)
        
        # Calculate strict analytical normals for the baseplate faces
        bc = np.array(mcolors.to_rgb(C_ANCHOR)) 
        for i in range(3):
            v1_bp = bp_local[i, 1] - bp_local[i, 0]
            v2_bp = bp_local[i, 2] - bp_local[i, 0]
            n_bp = np.cross(v1_bp, v2_bp)
            n_len_bp = np.linalg.norm(n_bp)
            n_bp = n_bp / max(n_len_bp, 1e-5)
            
            bp_diff = 0.5 + 0.5 * max(0, np.dot(n_bp, LIGHT_DIR))
            rgba = np.array([bc[0]*bp_diff, bc[1]*bp_diff, bc[2]*bp_diff, 1.0])
            queue.append({'sz': z_c[i] - 100.0, 'dat': p2d[i], 'fc': rgba, 'ec': '#111115', 'lw': 2.0}) # Pushed back artificially to prevent Z-fighting, thick edges
            
    # FORCE VECTOR
    if load > 0.05 and t_sec < T_SNAP:
        tip_x = L_TOTAL * extrude_prog
        v_b = k_bend * (3 * L_TOTAL * tip_x**2 - tip_x**3) / (2 * L_TOTAL**3)
        th_b = k_bend * (6 * L_TOTAL * tip_x - 3 * tip_x**2) / (2 * L_TOTAL**3)
        
        tx = tip_x - 0 * np.sin(th_b) - L_TOTAL/2 + 50.0
        ty = 0 * np.cos(th_b) - v_b + 50
        
        p1 = np.array([tx, ty, 0])
        p2 = np.array([tx, ty + 100 + load*200, 0])
        vc = np.einsum('ij,nj->ni', M_cam, np.stack((p1, p2)))
        vc[:, 2] += cam_dist
        ppx = 4000.0 * (vc[:, 0] / vc[:, 2])
        ppy = 4000.0 * (vc[:, 1] / vc[:, 2]) - 100.0
        
        ax.annotate('', xy=(ppx[0], ppy[0]), xytext=(ppx[1], ppy[1]),
            arrowprops=dict(facecolor=C_FORCE, edgecolor='none', shrink=0, width=6, headwidth=20), zorder=100)

    # 4. DEPTH SORT AND RENDER
    queue.sort(key=lambda x: x['sz'], reverse=True)
    b_p, b_fc, b_ec, b_lw = [], [], [], []
    for item in queue:
        b_p.append(item['dat'])
        b_fc.append(item['fc'])
        b_ec.append(item['ec'])
        b_lw.append(item['lw'])
        
    if b_p:
        ax.add_collection(PolyCollection(b_p, facecolors=b_fc, edgecolors=b_ec, linewidths=b_lw, joinstyle='miter'))

    # 5. HIGH-DENSITY HUD & TELEMETRY
    ax.add_patch(Rectangle((-540, 780), 1080, 180, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [780, 780], color=C_TEXT, lw=3, zorder=81)
    ax.text(-500, 880, "LG-404 :: THE FINITE ELEMENT MATRIX", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 830, "[SFI-1.00] DYNAMIC RESONANCE & CRITICAL SPALLATION", color=C_GUI, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    if t_sec >= T_SNAP:
        state_msg = "PHASE 4: STRUCTURAL YIELD ENGAGED (CATASTROPHIC FAILURE)"
        state_col = C_CRIT
        sys_metric = "ROOT DISCRETISATION BONDS DELETED. BEAM SEVERED."
        prog = 1.0
    elif t_sec >= T_EXTRUDE:
        state_msg = "PHASE 3: DYNAMIC VON MISES LOAD & STRUCTURAL RESONANCE"
        if load > 0.8: state_col = C_CRIT
        elif load > 0.4: state_col = C_WARN
        else: state_col = C_COLD
        sys_metric = f"PEAK YIELD TRACE: {(load * 115):05.1f}%"
        prog = 0.2 + (0.8 * load)
    else:
        state_msg = "PHASE 2: KINEMATIC DISCRETISATION EXTRUSION"
        state_col = C_COLD
        sys_metric = "EXTRUDING 1,500 FINITE ELEMENTS ALONG NEUTRAL AXIS"
        prog = extrude_prog * 0.2

    ax.text(-500, -780, f"CURRENT STATE: {state_msg}", color=state_col, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"STRUCTURAL LOAD VECTOR: {(load * 850):06.1f} KN", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"SYSTEM DIAGNOSTIC     : {sys_metric}", color=C_TEXT, fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(Rectangle((-500, -920), 1000, 8, facecolor=C_GUI, zorder=82))
    ax.add_patch(Rectangle((-500, -920), 1000 * prog, 8, facecolor=state_col, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f_idx:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f_idx

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-404: EXTREME KINEMATICS MATRIX ENGAGED [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            pass
    print("Compilation Complete. Optimised dynamic geometry executed.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
