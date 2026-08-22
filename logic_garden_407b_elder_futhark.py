"""
PROJECT: Logic Garden 407b (The Anisotropic Matrix // Elder Futhark)
FORMAT: YouTube Shorts (1080x1920)
METADATA: ELDER FUTHARK, RUNES, KINEMATICS, ANISOTROPY, DATA STORAGE
EXECUTION: 24.0s Sequence. True 3D Volumetric Subtraction.
RULES ENFORCED:
- Daylight Palette (White Substrate / High-Contrast Chrome).
- Phase-Locked Metaphor: The physics of wood grain dictating alphabetical geometry.
- Exact realisational aspect of O(N) volumetric fiber spallation.
- Australian spelling conventions enforced natively (Maths, Colour, Optimise).
- No horizontal geometry (preventing split-grain data corruption).
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
OUT_DIR = "frames_407b_elder_futhark"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST BARE-METAL PALETTE --------
C_BG            = '#FFFFFF'
C_TEXT          = '#111115'
C_EDGE          = '#111115'
C_GUI           = '#64748B'

# Lithic/Timber Substrate Palette
C_FIBER_TOP     = '#CC6600'  # Dense Amber (Wood Substrate)
C_FIBER_FRONT   = '#92400E'  # Dark Amber (Extrusion depth shade)
C_FIBER_RIGHT   = '#78350F'  # Deep Amber (Shadow)
C_CARVED_FLOOR  = '#111115'  # Indestructible Black (Absolute shadow)

# Kinematic Blade Palette
C_BLADE         = '#334155'  # Heavy Steel Vector
C_BLADE_TIP     = '#FF3300'  # Intense Red (Kinetic Shear)
C_SPARK         = '#FFB300'  # Dense Amber Spallation

LIGHT_DIR = np.array([-0.5, 0.8, -0.4])
LIGHT_DIR /= np.linalg.norm(LIGHT_DIR)

# ------------------------------------------------------------------
# O(1) 3D ARCHITECTURAL FIBER GENERATOR (ANISOTROPIC GRAIN)
# ------------------------------------------------------------------
# Elongated blocks to emphatically prove the vertical grain direction
DX, DY = 2.5, 5.0
NX, NY = 64, 90
W_TOTAL, H_TOTAL = NX * DX, NY * DY

def dist_to_segment(px, py, x1, y1, x2, y2):
    # O(1) Line Segment Distance Formula
    seg = np.array([x2 - x1, y2 - y1])
    pt = np.array([px - x1, py - y1])
    seg_len_sq = np.dot(seg, seg)
    if seg_len_sq == 0.0:
        return np.linalg.norm(pt)
    t = max(0, min(1, np.dot(pt, seg) / seg_len_sq))
    proj = np.array([x1, y1]) + t * seg
    return np.linalg.norm(np.array([px, py]) - proj), t

# Define the Fehu (ᚠ) Rune Kinematic Vectors
# Cut 1: Vertical Stave. Cut 2: Top Twig. Cut 3: Bottom Twig.
CUTS = [
    {'x1': -15.0, 'y1': -70.0, 'x2': -15.0, 'y2': 70.0, 't_start': 2.0, 't_end': 8.0},
    {'x1': -15.0, 'y1':  20.0, 'x2':  35.0, 'y2': 75.0, 't_start': 9.0, 't_end': 14.0},
    {'x1': -15.0, 'y1': -20.0, 'x2':  35.0, 'y2': 35.0, 't_start': 15.0, 't_end': 20.0}
]
CARVE_RADIUS = 3.5

CELLS = []
for ix in range(NX):
    for iy in range(NY):
        cx = (ix * DX) - W_TOTAL/2.0 + DX/2.0
        cy = (iy * DY) - H_TOTAL/2.0 + DY/2.0
        
        t_strike = 999.0
        # Evaluate intersection with chronological cuts
        for cut in CUTS:
            d, t_seg = dist_to_segment(cx, cy, cut['x1'], cut['y1'], cut['x2'], cut['y2'])
            if d <= CARVE_RADIUS:
                # Calculate exact temporal strike time based on vector progression
                t_impact = cut['t_start'] + t_seg * (cut['t_end'] - cut['t_start'])
                if t_impact < t_strike:
                    t_strike = t_impact
                    
        CELLS.append({'cx': cx, 'cy': cy, 't_strike': t_strike})

print(f"PHASE 1: ANISOTROPIC TENSOR PRE-COMPILED [{NX*NY} PILLARS, {len(CUTS)} KINEMATIC VECTORS]")

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
    M_cam = rx(-35.0) @ ry(20.0)
    cam_dist = 600.0  # Macro inspection
    
    queue = []
    
    # 2. BLADE POSITION EVALUATION
    blade_active = False
    blade_pos = np.array([0.0, 0.0, 0.0])
    current_cut_idx = -1
    
    for i, cut in enumerate(CUTS):
        if cut['t_start'] <= t_sec <= cut['t_end'] + 0.3:
            prog = np.clip((t_sec - cut['t_start']) / (cut['t_end'] - cut['t_start']), 0.0, 1.0)
            bx = cut['x1'] + prog * (cut['x2'] - cut['x1'])
            by = cut['y1'] + prog * (cut['y2'] - cut['y1'])
            bz = -10.0 + 5.0 * np.sin(t_sec * 80.0) # Downward kinetic shear vibration
            blade_pos = np.array([bx, by, bz])
            blade_active = True
            current_cut_idx = i
            break

    # 3. LITHIC MATRIX COMPILATION (O(N) Painter's Algorithm on Pillars)
    DEPTH_MAX = -25.0
    
    c_top_raw = np.array(mcolors.to_rgb(C_FIBER_TOP))
    
    faces_collected = []
    fcs_collected = []
    z_collected = []
    edges_collected = []
    lw_collected = []
    
    # Precompute geometric bounds
    dx2, dy2 = DX/2.0 * 0.85, DY/2.0 * 0.95 # Narrower X-gap to emulate vertical contiguous grain
    
    for cell in CELLS:
        cx, cy = cell['cx'], cell['cy']
        
        # Determine parametric absolute depth
        if t_sec < cell['t_strike']: cz = 0.0
        else:
            dt = t_sec - cell['t_strike']
            cz = DEPTH_MAX * ease_out(dt * 12.0) # Explosive shear drop
            
        t_col = c_top_raw if cz == 0.0 else lerp_colour(C_FIBER_TOP, C_CARVED_FLOOR, abs(cz)/abs(DEPTH_MAX))
        
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
        
        for face_pts, face_col, is_top in [(v_top, t_col, True), (v_front, C_FIBER_FRONT, False), (v_right, C_FIBER_RIGHT, False)]:
            v_cam = np.einsum('ij,nj->ni', M_cam, face_pts)
            v_cam[:, 2] += cam_dist
            
            centroid_z = np.mean(v_cam[:, 2])
            
            px = 1800.0 * (v_cam[:, 0] / v_cam[:, 2])
            py = 1800.0 * (v_cam[:, 1] / v_cam[:, 2])
            poly_2d = np.stack((px, py), axis=-1)
            
            faces_collected.append(poly_2d)
            if is_top:
                if cz < -1.0: # Burnt edge if carved
                    fcs_collected.append(np.append(t_col, 1.0))
                    edges_collected.append(C_CARVED_FLOOR)
                    lw_collected.append(0.5)
                else: 
                    fcs_collected.append(np.append(t_col, 1.0))
                    edges_collected.append(C_EDGE)
                    lw_collected.append(0.4)
            else:
                col_rgb = np.array(mcolors.to_rgb(face_col))
                fcs_collected.append(np.append(col_rgb, 1.0))
                edges_collected.append(face_col)
                lw_collected.append(0.1)
                
            z_collected.append(centroid_z)

    # 4. BLADE GEOMETRY & SPALLATION
    if blade_active:
        cut = CUTS[current_cut_idx]
        cut_vec = np.array([cut['x2'] - cut['x1'], cut['y2'] - cut['y1']])
        ang = np.degrees(np.arctan2(cut_vec[1], cut_vec[0]))
        
        # Brutalist carving wedge
        blade_mesh = np.array([
            [[0,0,0], [ -8,  30, 15], [  8,  30, 15]], # Back
            [[0,0,0], [  8,  30, 15], [  0, -10, 25]], # Front Right
            [[0,0,0], [  0, -10, 25], [ -8,  30, 15]]  # Front Left
        ])
        
        R_blade = rz(ang - 90) @ rx(-15.0)
        b_mesh = np.dot(blade_mesh, R_blade.T) + blade_pos
        
        for i, face in enumerate(b_mesh):
            vc = np.einsum('ij,nj->ni', M_cam, face)
            vc[:, 2] += cam_dist
            px = 1800.0 * (vc[:, 0] / vc[:, 2])
            py = 1800.0 * (vc[:, 1] / vc[:, 2])
            
            c_f = C_BLADE_TIP if i > 0 else C_BLADE
            c_rgb = np.array(mcolors.to_rgb(c_f))
            faces_collected.append(np.stack((px, py), axis=-1))
            fcs_collected.append(np.append(c_rgb, 1.0))
            edges_collected.append(C_EDGE)
            lw_collected.append(1.2)
            z_collected.append(np.mean(vc[:, 2]))
            
        # Kinematic Spark Yield
        np.random.seed(int(t_sec * 200))
        for _ in range(12):
            vx, vy, vz = np.random.uniform(-40, 40), np.random.uniform(-40, 40), np.random.uniform(50, 150)
            spos = blade_pos + np.array([vx*0.1, vy*0.1, vz*0.1])
            sp = np.array([[spos[0]-1, spos[1]-1, spos[2]], [spos[0]+1, spos[1]-1, spos[2]],
                           [spos[0]+1, spos[1]+1, spos[2]], [spos[0]-1, spos[1]+1, spos[2]]])
            vc = np.einsum('ij,nj->ni', M_cam, sp)
            vc[:, 2] += cam_dist
            px = 1800.0 * (vc[:, 0] / vc[:, 2]); py = 1800.0 * (vc[:, 1] / vc[:, 2])
            faces_collected.append(np.stack((px, py), axis=-1))
            fcs_collected.append(np.append(np.array(mcolors.to_rgb(C_SPARK)), 1.0))
            edges_collected.append('none')
            lw_collected.append(0.0)
            z_collected.append(np.mean(vc[:, 2]))

    # 5. SORT AND RENDER TENSORS
    sort_idx = np.argsort(z_collected)[::-1] 
    sorted_faces = [faces_collected[i] for i in sort_idx]
    sorted_fcs = [fcs_collected[i] for i in sort_idx]
    sorted_ecs = [edges_collected[i] for i in sort_idx]
    sorted_lws = [lw_collected[i] for i in sort_idx]

    if sorted_faces:
        ax.add_collection(PolyCollection(sorted_faces, facecolors=sorted_fcs, edgecolors=sorted_ecs, linewidths=sorted_lws, joinstyle='miter'))

    # 6. HIGH-DENSITY HUD & TELEMETRY
    ax.add_patch(Rectangle((-540, 780), 1080, 180, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [780, 780], color=C_TEXT, lw=3, zorder=81)
    ax.text(-500, 880, "LG-407b :: ELDER FUTHARK", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 830, "[SFI-1.00] ANISOTROPIC GRAIN & KINEMATIC SHEAR", color=C_GUI, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(Rectangle((-540, -960), 1080, 240, facecolor=C_BG, zorder=80, alpha=0.95))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=3, zorder=81)

    prog = 0.0
    active_op = "NONE"
    if t_sec < 2.0:
        state_msg = "PHASE 1: FIBROUS SUBSTRATE (WOOD)"
        state_col = C_TEXT
    elif t_sec < 8.0:
        state_msg = "PHASE 2: VERTICAL STAVE YIELD"
        state_col = C_BLADE_TIP
        active_op = "STRIKING PARALLEL TO GRAIN"
        prog = (t_sec - 2.0)/6.0
    elif t_sec < 9.0:
        state_msg = "PHASE 2: VERTICAL STAVE YIELD"
        state_col = C_BLADE_TIP
        prog = 1.0
    elif t_sec < 14.0:
        state_msg = "PHASE 3: PRIMARY DIAGONAL TWIG YIELD"
        state_col = C_BLADE_TIP
        active_op = "STRIKING OBLIQUE TO GRAIN"
        prog = (t_sec - 9.0)/5.0
    elif t_sec < 15.0:
        state_msg = "PHASE 3: PRIMARY DIAGONAL TWIG YIELD"
        state_col = C_BLADE_TIP
        prog = 1.0
    elif t_sec < 20.0:
        state_msg = "PHASE 4: SECONDARY DIAGONAL TWIG YIELD"
        state_col = C_BLADE_TIP
        active_op = "STRIKING OBLIQUE TO GRAIN"
        prog = (t_sec - 15.0)/5.0
    else:
        state_msg = "PHASE 5: ABSOLUTE SYMBOLIC YIELD"
        state_col = C_GUI
        active_op = "RUNE SECURED: FEHU (WEALTH/CATTLE)"
        prog = 1.0

    ax.text(-500, -780, f"PROTOCOL STATE : {state_msg}", color=state_col, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -830, f"DIAGNOSTIC     : {active_op}", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, -880, f"STRUCTURAL RULE: HORIZONTAL VECTORS COMMAND MATERIAL SPLIT. FORBIDDEN.", color=C_TEXT, fontsize=11, fontname='monospace', zorder=82)

    ax.add_patch(Rectangle((-500, -920), 1000, 8, facecolor=C_GUI, zorder=82))
    ax.add_patch(Rectangle((-500, -920), 1000 * prog, 8, facecolor=state_col, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f_idx:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f_idx

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-407b: ANISOTROPIC TENSOR ENGAGED [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")
    print("Compilation Complete. Runic geometry secured.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
