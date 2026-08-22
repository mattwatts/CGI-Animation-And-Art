"""
PROJECT: Logic Garden 407 (The Lithic Extraction Vector // Egyptian Hieroglyphs)
FORMAT: YouTube Shorts (1080x1920)
METADATA: EGYPTIAN HIEROGLYPHS, LITHIC MATRIX, KINEMATICS, DATA STORAGE
EXECUTION: 24.0s Sequence. True 3D Volumetric Subtraction.
RULES ENFORCED:
- Daylight Palette (White Substrate / High-Contrast Chrome).
- Phase-Locked Metaphor: The brute-force writing of data into stone.
- Exact realisational aspect of O(N) volumetric spallation masking.
- Australian spelling conventions enforced natively (Maths, Colour, Optimise).
- Absolute Mathematical Baseplate with True Lambertian Depth Shadows.
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
OUT_DIR = "frames_407_egyptian"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG            = '#FFFFFF'
C_TEXT          = '#111115'
C_EDGE          = '#111115'
C_GUI           = '#64748B'

# Lithic Substrate Palette (Limestone to Deep Basalt Shadow)
C_LITHIC_TOP    = '#F8FAFC'  # Raw uncut surface
C_LITHIC_FRONT  = '#CBD5E1'  # Bevel lighting
C_LITHIC_RIGHT  = '#94A3B8'  # Bevel shadow
C_CARVED_FLOOR  = '#0F172A'  # Deep void ink (Absolute shadow)

# Kinematic Chisel Palette
C_CHISEL        = '#334155'  # Heavy Steel Vector
C_CHISEL_TIP    = '#FF3300'  # Intense Red (Thermodynamic heat)
C_SPARK         = '#FFB300'  # Dense Amber Spallation

LIGHT_DIR = np.array([-0.5, 0.8, -0.4])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

# ------------------------------------------------------------------
# O(1) 3D ARCHITECTURAL GRID GENERATOR
# ------------------------------------------------------------------
DX, DY = 3.5, 3.5
NX, NY = 54, 80
W_TOTAL, H_TOTAL = NX * DX, NY * DY

# Define the absolute mathematical filter for the Ankh
def is_ankh_mask(x, y):
    # Top Loop Matrix
    loop_val = (x**2 / 16.0**2) + ((y - 40.0)**2 / 20.0**2)
    if 0.5 < loop_val < 1.35 and y >= 25.0:
        return 1
    # Crossbar Matrix
    if -36.0 < x < 36.0 and 15.0 < y < 27.0:
        return 2
    # Stem Matrix
    if -10.0 < x < 10.0 and -60.0 < y <= 20.0:
        return 3
    return 0

CELLS = []
carve_list_loop = []
carve_list_bar = []
carve_list_stem = []

for ix in range(NX):
    for iy in range(NY):
        cx = (ix * DX) - W_TOTAL/2.0 + DX/2.0
        cy = (iy * DY) - H_TOTAL/2.0 + DY/2.0
        
        mask_id = is_ankh_mask(cx, cy)
        cell = {'cx': cx, 'cy': cy, 'mask_id': mask_id, 't_strike': 999.0}
        CELLS.append(cell)
        
        if mask_id == 1: carve_list_loop.append(cell)
        elif mask_id == 2: carve_list_bar.append(cell)
        elif mask_id == 3: carve_list_stem.append(cell)

# Mathematical sorting to simulate the Sovereign Strike path
# Loop: Sort circumferentially (atan2)
carve_list_loop.sort(key=lambda c: np.arctan2(c['cx'], c['cy'] - 40.0))
# Bar: Sort left to right
carve_list_bar.sort(key=lambda c: c['cx'])
# Stem: Sort top to bottom
carve_list_stem.sort(key=lambda c: -c['cy'])

ordered_carve_targets = carve_list_loop + carve_list_bar + carve_list_stem

# Assign absolute temporal execution logic
T_START_CARVE = 2.0
T_END_CARVE = 18.0
N_TARGETS = len(ordered_carve_targets)
if N_TARGETS > 0:
    dt = (T_END_CARVE - T_START_CARVE) / N_TARGETS
    for i, tgt in enumerate(ordered_carve_targets):
        tgt['t_strike'] = T_START_CARVE + i * dt

print(f"PHASE 1: LITHIC TENSOR PRE-COMPILED [{NX*NY} PILLARS, {N_TARGETS} EXTRACTION TARGETS]")

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

def lerp_colour(c1_hex, c2_hex, t):
    c1 = np.array(mcolors.to_rgb(c1_hex))
    c2 = np.array(mcolors.to_rgb(c2_hex))
    return c1 * (1 - t) + c2 * t

def ease_out(t): 
    t = np.clip(t, 0.0, 1.0)
    return 1.0 - (1.0 - t)**3

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
    M_cam = rx(-30.0) @ ry(25.0)
    cam_dist = 650.0  # Deep macro zoom establishing intricate detail
    
    queue = []
    
    # 2. CHISEL POSITION EVALUATION
    chisel_active = False
    chisel_pos = np.array([0.0, 0.0, 0.0])
    
    # Find the current striking vector
    if T_START_CARVE <= t_sec <= T_END_CARVE + 0.5:
        idx = int(((t_sec - T_START_CARVE) / (T_END_CARVE - T_START_CARVE)) * N_TARGETS)
        idx = np.clip(idx, 0, N_TARGETS - 1)
        cur_target = ordered_carve_targets[idx]
        
        # Smooth interpolation to target
        chisel_x = cur_target['cx']
        chisel_y = cur_target['cy']
        chisel_z = -10.0 + 10.0 * np.sin(t_sec * 150.0) # Violent high-frequency jackhammer motion
        
        chisel_pos = np.array([chisel_x, chisel_y, chisel_z])
        chisel_active = True

    # 3. LITHIC MATRIX COMPILATION (O(N) Painter's Algorithm on Pillars)
    # To optimise rendering, we draw each pillar strictly as 3 visible faces (Top, Front(-Y), Right(+X))
    DEPTH_MAX = -40.0
    
    c_top_raw = np.array(mcolors.to_rgb(C_LITHIC_TOP))
    c_top_carve = np.array(mcolors.to_rgb(C_CARVED_FLOOR))
    
    faces_collected = []
    fcs_collected = []
    z_collected = []
    edges_collected = []
    lw_collected = []
    
    for cell in CELLS:
        cx, cy = cell['cx'], cell['cy']
        
        # Determine parametric absolute depth
        if t_sec < cell['t_strike']:
            cz = 0.0
        else:
            dt = t_sec - cell['t_strike']
            cz = DEPTH_MAX * ease_out(dt * 8.0) # Rapid drop
            
        t_col = c_top_raw if cz == 0.0 else lerp_colour(C_LITHIC_TOP, C_CARVED_FLOOR, abs(cz)/abs(DEPTH_MAX))
        
        # Top Face Matrix
        dx2 = DX/2.0 * 0.9 # Strict minor gaps for pure physical separation
        dy2 = DY/2.0 * 0.9
        
        v_top = np.array([
            [cx-dx2, cy-dy2, cz], [cx+dx2, cy-dy2, cz],
            [cx+dx2, cy+dy2, cz], [cx-dx2, cy+dy2, cz]
        ])
        
        v_front = np.array([
            [cx-dx2, cy-dy2, DEPTH_MAX], [cx+dx2, cy-dy2, DEPTH_MAX],
            [cx+dx2, cy-dy2, cz], [cx-dx2, cy-dy2, cz]
        ])
        
        v_right = np.array([
            [cx+dx2, cy-dy2, DEPTH_MAX], [cx+dx2, cy+dy2, DEPTH_MAX],
            [cx+dx2, cy+dy2, cz], [cx+dx2, cy-dy2, cz]
        ])
        
        for face_pts, face_col, is_top in [(v_top, t_col, True), (v_front, C_LITHIC_FRONT, False), (v_right, C_LITHIC_RIGHT, False)]:
            v_cam = np.einsum('ij,nj->ni', M_cam, face_pts)
            v_cam[:, 2] += cam_dist
            
            centroid_z = np.mean(v_cam[:, 2])
            
            # Pure Lambertian depth culling (only Top really matters but included for strict architecture)
            px = 1800.0 * (v_cam[:, 0] / v_cam[:, 2])
            py = 1800.0 * (v_cam[:, 1] / v_cam[:, 2])
            
            poly_2d = np.stack((px, py), axis=-1)
            
            faces_collected.append(poly_2d)
            if is_top:
                fcs_collected.append(np.append(face_col, 1.0))
                edges_collected.append(C_EDGE)
                lw_collected.append(0.5)
            else:
                col_rgb = np.array(mcolors.to_rgb(face_col))
                fcs_collected.append(np.append(col_rgb, 1.0))
                edges_collected.append(face_col)
                lw_collected.append(0.1)
                
            z_collected.append(centroid_z)

    # 4. CHISEL GEOMETRY & SPALLATION
    if chisel_active:
        # A brutal triangular pyramid angled slightly
        chisel_mesh = np.array([
            [[0,0,0], [-6, 30, -6], [ 6, 30, -6]],
            [[0,0,0], [ 6, 30, -6], [ 0, 30,  8]],
            [[0,0,0], [ 0, 30,  8], [-6, 30, -6]]
        ])
        
        R_chis = rx(-15.0) @ rz(-20.0)
        chisel_mesh = np.dot(chisel_mesh, R_chis.T) + chisel_pos
        
        for i, face in enumerate(chisel_mesh):
            v_cam = np.einsum('ij,nj->ni', M_cam, face)
            v_cam[:, 2] += cam_dist
            px = 1800.0 * (v_cam[:, 0] / v_cam[:, 2])
            py = 1800.0 * (v_cam[:, 1] / v_cam[:, 2])
            
            c_fill = C_CHISEL_TIP if i == 0 else C_CHISEL
            cc = np.array(mcolors.to_rgb(c_fill))
            faces_collected.append(np.stack((px, py), axis=-1))
            fcs_collected.append(np.array([cc[0], cc[1], cc[2], 1.0]))
            edges_collected.append(C_EDGE)
            lw_collected.append(1.0)
            z_collected.append(np.mean(v_cam[:, 2]))
            
        # Kinematic Spallation Generation
        np.random.seed(int(t_sec * 100)) # Deterministic spark chaos frame-by-frame
        for _ in range(8):
            vx, vy, vz = np.random.uniform(-40, 40), np.random.uniform(-40, 40), np.random.uniform(50, 150)
            spark_pos = chisel_pos + np.array([vx*0.1, vy*0.1, vz*0.1])
            sp = np.array([
                [spark_pos[0]-1, spark_pos[1]-1, spark_pos[2]],
                [spark_pos[0]+1, spark_pos[1]-1, spark_pos[2]],
                [spark_pos[0]+1, spark_pos[1]+1, spark_pos[2]],
                [spark_pos[0]-1, spark_pos[1]+1, spark_pos[2]]
            ])
            vc = np.einsum('ij,nj->ni', M_cam, sp)
            vc[:, 2] += cam_dist
            px = 1800.0 * (vc[:, 0] / vc[:, 2])
            py = 1800.0 * (vc[:, 1] / vc[:, 2])
            fc = np.append(np.array(mcolors.to_rgb(C_SPARK)), 1.0)
            faces_collected.append(np.stack((px, py), axis=-1))
            fcs_collected.append(fc)
            edges_collected.append('none')
            lw_collected.append(0.0)
            z_collected.append(np.mean(vc[:, 2]))

    # 5. SORT AND RENDER TENSORS
    sort_idx = np.argsort(z_collected)[::-1] # Ascending reverse for Painter's algorithm
    sorted_faces = [faces_collected[i] for i in sort_idx]
    sorted_fcs = [fcs_collected[i] for i in sort_idx]
    sorted_ecs = [edges_collected[i] for i in sort_idx]
    sorted_lws = [lw_collected[i] for i in sort_idx]

    if sorted_faces:
        ax.add_collection(PolyCollection(sorted_faces, facecolors=sorted_fcs, edgecolors=sorted_ecs, linewidths=sorted_lws, joinstyle='miter'))

    # 6. HIGH-DENSITY HUD & TELEMETRY
    ax.add_patch(Rectangle((-540, 780), 1080, 180, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [780, 780], color=C_TEXT, lw=3, zorder=81)
    ax.text(-500, 880, "LG-407 :: LITHIC DATA MATRIX", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 830, "[SFI-0.50] MATHEMATICAL COMPRESSION & KINEMATIC WRITING", color=C_GUI, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    # Dynamic metrics formulation
    pct_complete = 0.0
    if T_START_CARVE <= t_sec <= T_END_CARVE:
        pct_complete = (t_sec - T_START_CARVE) / (T_END_CARVE - T_START_CARVE)
    elif t_sec > T_END_CARVE:
        pct_complete = 1.0

    if t_sec < T_START_CARVE:
        state_msg = "PHASE 1: RAW LITHIC SUBSTRATE"
        state_col = C_TEXT
        sys_metric = "AWAITING SOVEREIGN STRIKE VECTOR"
        prog = 0.0
    elif t_sec < T_END_CARVE:
        state_msg = "PHASE 2: KINEMATIC BOLEAN EXTRACTION"
        state_col = C_CHISEL_TIP
        sys_metric = f"CARVING PHONETIC SYMBOL: ANKH // SPALLATION AT {(pct_complete*100):05.1f}%"
        prog = pct_complete
    else:
        state_msg = "PHASE 3: ABSOLUTE INFORMATION YIELD"
        state_col = C_GUI
        sys_metric = "WRITE LATENCY: MASSIVE. RETENTION DELTA: 5,000 YEARS."
        prog = 1.0

    ax.text(-500, -780, f"PROTOCOL STATE: {state_msg}", color=state_col, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"DATA DIAGNOSTIC: {sys_metric}", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"AXIOMATIC TRUTH: TO SECURE DATA AGAINST TIME, CARVE THE MATTER FIELD.", color=C_TEXT, fontsize=11, fontname='monospace', zorder=82)

    ax.add_patch(Rectangle((-500, -920), 1000, 8, facecolor=C_GUI, zorder=82))
    ax.add_patch(Rectangle((-500, -920), 1000 * prog, 8, facecolor=state_col, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f_idx:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f_idx

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-407: LITHIC TENSOR ENGAGED [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")
    print("Compilation Complete. Subterranean data mapped.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
