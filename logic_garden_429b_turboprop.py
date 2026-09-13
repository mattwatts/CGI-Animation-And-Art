"""
PROJECT: Logic Garden 429b (True 3D Offset Construct // Turboprop Engine)
FORMAT: YouTube Shorts (1080x1920)
METADATA: TURBOPROP, AERODYNAMICS, TWIN-SPOOL, GEOMETRY, 3D DAYLIGHT
EXECUTION: 12.0s Seamless Infite Loop. Dynamic 3D Z-Sorted Matrix.
RULES ENFORCED: 
- O(N * log N) Depth-Sorted Painter's Algorithm for all 3D Polygons.
- True Isometric Affine Projection (Pitch +22deg, Roll -10deg).
- Dynamic Lambertian Normal Shading for photorealistic depth.
- Daylight Palette (White Substrate / High-Contrast Edge Geometry).
- Purged Jargon. Australian spelling conventions.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcol
from matplotlib.colors import LinearSegmentedColormap
import multiprocessing as mp
import os
import gc

# ======== SEQUENCE PARAMETERS ========
DURATION = 12.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_429b_turboprop"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'          # Indestructible Black UI
C_CASE      = '#1E293B'          # Carbon Casing Wires
C_STATOR    = '#94A3B8'          # Steel Stators
C_LP_SPOOL  = '#005599'          # Power Spool (Deep Marine)
C_HP_SPOOL  = '#DE008A'          # Gas Generator Spool (Deep Magenta)
C_GEAR      = '#FFB300'          # Dense Amber (Reduction Box)
C_PROP      = '#0F172A'          # Black Composite Propeller

# Thermodynamic Fluid Gradient Array
fluid_nodes = [0.0, 0.22, 0.50, 0.66, 1.0] # Mapped 0.0 (Exhaust) to 1.0 (Intake)
fluid_colors = ['#71717A', '#DE008A', '#FF3300', '#00C853', '#005599']
cmap_fluid = LinearSegmentedColormap.from_list('thermo', list(zip(fluid_nodes, fluid_colors)))

# ------------------------------------------------------------------
# 3D PROJECTION & SHADING TENSORS
# ------------------------------------------------------------------
# Pitch forward to look INTO the intake, Roll slightly to fit screen diagonally
theta_x = np.radians(22)
cx, sx = np.cos(theta_x), np.sin(theta_x)
RX = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])

theta_z = np.radians(-10)
cz, sz = np.cos(theta_z), np.sin(theta_z)
RZ = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])

ROT_MAT = RZ @ RX
LIGHT_DIR = np.array([0.5, 0.4, 0.7])
LIGHT_DIR = LIGHT_DIR / np.linalg.norm(LIGHT_DIR)

def project_3d(points):
    """ O(1) Matrix Multiplication for true 3D to 2D screen coordinates """
    return points @ ROT_MAT.T

def shade_color(hex_col, normal_vec):
    n = normal_vec / (np.linalg.norm(normal_vec) + 1e-6)
    dot = abs(np.dot(n, LIGHT_DIR))
    rgb = np.array(mcol.to_rgb(hex_col))
    final = np.clip(rgb * (0.35 + 0.65 * dot), 0, 1)
    return final

# ------------------------------------------------------------------
# RIGID 1D PHYSICS DATASTREAMS (Casing Boundary)
# ------------------------------------------------------------------
Y_PTS = np.array([-450, -300, -150, 0, 150, 350, 450])
RO_PTS = np.array([140, 220, 180, 200, 160, 220, 220])
RI_PTS = np.array([ 20,  70,  80,  90, 110,  70,  60])

def get_radii(y):
    return np.interp(y, Y_PTS, RO_PTS), np.interp(y, Y_PTS, RI_PTS)

# ------------------------------------------------------------------
# O(N) 3D GEOMETRY COMPILER
# ------------------------------------------------------------------
def gen_cylinder(y_start, y_end, r, ox, oz, hex_col, num_seg=16):
    items = []
    for i in range(num_seg):
        t1, t2 = i * 2 * np.pi / num_seg, (i+1) * 2 * np.pi / num_seg
        p3d = np.array([
            [r*np.cos(t1)+ox, y_start, r*np.sin(t1)+oz],
            [r*np.cos(t2)+ox, y_start, r*np.sin(t2)+oz],
            [r*np.cos(t2)+ox, y_end,   r*np.sin(t2)+oz],
            [r*np.cos(t1)+ox, y_end,   r*np.sin(t1)+oz]
        ])
        p3_t = project_3d(p3d)
        zc = np.mean(p3_t[:, 2])
        
        # Normal shading
        n_orig = np.array([(np.cos(t1)+np.cos(t2))/2, 0, (np.sin(t1)+np.sin(t2))/2])
        n_t = project_3d(np.array([n_orig]))[0]
        f_col = shade_color(hex_col, n_t)
        
        items.append((zc, 'poly', p3_t[:, :2], tuple(f_col), C_TEXT, 0.5, 1.0))
    return items

def gen_blades(y_val, num_b, th_off, ro, ri, hex_col, twist=0.0):
    items = []
    w = 8.0 
    for i in range(num_b):
        th = i * 2 * np.pi / num_b + th_off
        c1, s1 = np.cos(th - 0.04), np.sin(th - 0.04)
        c2, s2 = np.cos(th + 0.04), np.sin(th + 0.04)
        c3, s3 = np.cos(th + twist - 0.04), np.sin(th + twist - 0.04)
        c4, s4 = np.cos(th + twist + 0.04), np.sin(th + twist + 0.04)
        
        p3d = np.array([
            [ri*c1, y_val - w, ri*s1], [ro*c3, y_val - w, ro*s3],
            [ro*c4, y_val + w, ro*s4], [ri*c2, y_val + w, ri*s2]
        ])
        p3_t = project_3d(p3d)
        zc = np.mean(p3_t[:, 2])
        
        v1, v2 = p3_t[1]-p3_t[0], p3_t[3]-p3_t[0]
        f_col = shade_color(hex_col, np.cross(v1, v2))
        items.append((zc, 'poly', p3_t[:, :2], tuple(f_col), C_TEXT, 0.5, 1.0))
    return items

def gen_propeller(y_val, th_off, ro, hex_col):
    items = []
    for i in range(4):
        th = i * np.pi / 2.0 + th_off
        r1, r2 = 50.0, ro
        w_b, w_t = 25.0, 45.0
        
        segs = 6
        for seg in range(segs):
            radA = r1 + (r2-r1)*(seg/segs)
            radB = r1 + (r2-r1)*((seg+1)/segs)
            pitchA = np.radians(60) * (1.0 - seg/segs)
            pitchB = np.radians(60) * (1.0 - (seg+1)/segs)
            chordA = w_b + (w_t-w_b)*(seg/segs)
            chordB = w_b + (w_t-w_b)*((seg+1)/segs)
            
            def pt(rad, ptc, chord, dir_sign):
                yo = dir_sign * (chord/2) * np.sin(ptc)
                to = dir_sign * (chord/2) * np.cos(ptc)
                return [rad*np.cos(th) - to*np.sin(th), y_val + yo, rad*np.sin(th) + to*np.cos(th)]
                
            p3d = np.array([pt(radA, pitchA, chordA, -1), pt(radB, pitchB, chordB, -1),
                            pt(radB, pitchB, chordB, 1), pt(radA, pitchA, chordA, 1)])
            
            p3_t = project_3d(p3d)
            v1, v2 = p3_t[1]-p3_t[0], p3_t[3]-p3_t[0]
            
            use_col = C_GEAR if seg == segs-1 else hex_col
            f_col = shade_color(use_col, np.cross(v1, v2))
            items.append((np.mean(p3_t[:, 2]), 'poly', p3_t[:, :2], tuple(f_col), C_TEXT, 1.0, 1.0))
    return items

def gen_casing_rings():
    items = []
    for y_v in range(-450, 451, 50):
        ro, ri = get_radii(y_v)
        for r in [ro, ri]:
            # Generate points directly
            pts = 32
            p3d = np.array([[r*np.cos(i*2*np.pi/pts), y_v, r*np.sin(i*2*np.pi/pts)] for i in range(pts+1)])
            p3_t = project_3d(p3d)
            for i in range(pts):
                zc = (p3_t[i, 2] + p3_t[i+1, 2]) / 2.0
                items.append((zc, 'line', [p3_t[i, :2], p3_t[i+1, :2]], C_CASE, 2.0, 0.18))
    return items

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_norm = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # 9:16 Viewport Bounds
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)

    # 1. KINEMATIC ROTATION SYNC 
    th_lp, th_hp, th_pr = t_norm * 12.0 * 2 * np.pi, t_norm * -18.0 * 2 * np.pi, t_norm * 3.0 * 2 * np.pi

    master_list = []

    # 2. GENERATE HARDWARE (O(N) Assembly)
    master_list.extend(gen_cylinder(-320, 560, 12, 0, 0, C_LP_SPOOL))
    master_list.extend(gen_cylinder(-150, 350, 22, 0, 0, C_HP_SPOOL))
    
    # Compressors & Turbines
    for y_rot in [325, 295, 265, 235, 205, 175]: master_list.extend(gen_blades(y_rot, 20, th_hp, get_radii(y_rot)[0], 22, C_HP_SPOOL, 0.2))
    for y_rot in [-40, -90]: master_list.extend(gen_blades(y_rot, 24, th_hp, get_radii(y_rot)[0], 22, C_HP_SPOOL, -0.2))
    for y_rot in [-160, -210, -260]: master_list.extend(gen_blades(y_rot, 28, th_lp, get_radii(y_rot)[0], 12, C_LP_SPOOL, -0.3))
    for y_stat in [340, 310, 280, 250, 220, 190, 160, -20, -70, -140, -190, -240]:
        ro, ri = get_radii(y_stat)
        master_list.extend(gen_blades(y_stat, 24, 0.0, ro, ri, C_STATOR, 0.1))

    # Planetary Reduction Gearbox
    master_list.extend(gen_cylinder(540, 580, 25, 0, 0, C_LP_SPOOL)) # Sun
    for p_id in range(3): # Planets
        al = p_id * (2 * np.pi / 3.0) + th_pr
        master_list.extend(gen_cylinder(540, 580, 18, 55*np.cos(al), 55*np.sin(al), C_GEAR, num_seg=8))

    # Propellor
    master_list.extend(gen_propeller(710, th_pr, 480, C_PROP))
    master_list.extend(gen_cylinder(580, 770, 30, 0, 0, C_CASE, num_seg=8)) # Spinner hub
    master_list.extend(gen_casing_rings())

    # 3. KINEMATIC FLUID SWARM
    np.random.seed(429)
    N_FLUID = 2500
    p_off, p_trk, p_dir = np.random.rand(N_FLUID), np.random.uniform(0.1, 0.9, N_FLUID), np.random.choice([-1, 1], N_FLUID)
    p_glob = (p_off + t_norm) % 1.0
    
    Y_f = 450.0 - 950.0 * (p_glob ** 1.3)
    Ro_f, Ri_f = np.interp(Y_f, Y_PTS, RO_PTS), np.interp(Y_f, Y_PTS, RI_PTS)
    ang_f = p_glob * 35.0 + p_off * 100.0
    r_f = Ri_f + p_trk * (Ro_f - Ri_f)
    
    p3d_f = np.column_stack((r_f * np.cos(ang_f), Y_f, r_f * np.sin(ang_f)))
    p3_tc = project_3d(p3d_f)
    c_arr = cmap_fluid(np.clip((Y_f - (-450)) / 900.0, 0.0, 1.0))
    
    sz = 7
    for i in range(N_FLUID):
        cx, cy, cz = p3_tc[i, 0], p3_tc[i, 1], p3_tc[i, 2]
        d_poly = [[cx, cy-sz], [cx+sz, cy], [cx, cy+sz], [cx-sz, cy]]
        master_list.append((cz, 'poly', d_poly, tuple(c_arr[i]), 'none', 0.0, 0.65))

    # 4. VOLUMETRIC PAINTER'S SORT (O(N log N))
    master_list.sort(key=lambda x: x[0]) 

    # 5. RENDER BATCH 
    for it in master_list:
        if it[1] == 'poly':
            ax.add_patch(patches.Polygon(it[2], facecolor=it[3], edgecolor=it[4], lw=it[5], alpha=it[6]))
        elif it[1] == 'line':
            ax.plot([it[2][0][0], it[2][1][0]], [it[2][0][1], it[2][1][1]], color=it[3], lw=it[4], alpha=it[5])

    # 6. ABSOLUTE DAYLIGHT TELEMETRY
    ax.add_patch(plt.Rectangle((-540, 800), 1080, 160, facecolor=C_BG, zorder=80))
    ax.plot([-460, 460], [800, 800], color=C_TEXT, lw=6, zorder=81)
    ax.text(-460, 890, "LG-429b :: TURBOPROP (TWIN-SPOOL MATRIX)", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-460, 840, "TRUE 3D DEPTH SORT // EXACT KINEMATIC ROTORS", color=C_STATOR, fontsize=16, fontname='monospace', weight='bold', zorder=82)

    # Dynamic 3D Tag Tracking
    tags = [(450, "COLD INTAKE"), (250, "AXIAL COMPRESSOR"), (50, "COMBUSTION CORE"), (-150, "TWIN TURBINES"), (-400, "EXHAUST YIELD")]
    for ty, txt in tags:
        p_c = project_3d(np.array([[0, ty, 0]]))[0]
        ax.plot([-150, -400], [p_c[1], p_c[1]], color=C_TEXT, lw=2, alpha=0.5, zorder=81)
        ax.text(-420, p_c[1], f"[{txt}]", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', ha='left', va='center', zorder=82)

    ax.add_patch(plt.Rectangle((-540, -960), 1080, 260, facecolor=C_BG, zorder=80))
    ax.plot([-460, 460], [-700, -700], color=C_TEXT, lw=6, zorder=81)
    ax.text(-460, -750, "GAS GENERATOR (HP SPOOL) : 38,000 RPM", color=C_HP_SPOOL, fontsize=20, fontname='monospace', weight='bold', zorder=82)
    ax.text(-460, -800, "POWER TURBINE (LP SPOOL) : 25,330 RPM", color=C_LP_SPOOL, fontsize=20, fontname='monospace', weight='bold', zorder=82)
    ax.text(-460, -850, "EPICYCLIC REDUCTION GEAR : 4:1 RATIO", color=C_TEXT, fontsize=18, fontname='monospace', zorder=82)
    ax.text(-460, -900, "COMPOSITE PROPELLOR YIELD: 6,330 RPM", color=C_PROP, fontsize=22, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-429b: 3D OFFSET TURBOPROP MATRIX [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    stream = [(f, f / float(TOTAL_FRAMES)) for f in range(TOTAL_FRAMES)]

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, stream, chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")
    print("3D Painters Algorithm Locked. Stand by for compilation.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
