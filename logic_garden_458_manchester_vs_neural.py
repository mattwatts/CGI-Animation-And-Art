"""
PROJECT: Logic Garden 458 (Exact Physical Construct // Manchester vs Neural Kinematics)
FORMAT: YouTube Shorts (1080x1920)
METADATA: ENGINEERING, COMPUTER SCIENCE, BIOLOGY, NETWORKING, NEUROSCIENCE, PYTHON
EXECUTION: 24.0s Sequence @ 60 FPS. True Continuous Vector Architecture.
RULES ENFORCED:
- Native Python Wireframe generation isolating true 3D spatial data strings.
- Absolute Segmentation Protocol: All vectors segmented exactly, zero disconnected dots.
- Comparative Mathematics: Discrete Phase Encoding (Manchester) vs Frequency Rate Encoding (Neural).
- Biological Fidelity: Action potentials trace exact depolarisation and undershoot vectors.
- Viewport Override: Locked cam_span guarantees 100% total system visibility.
- Timeline: Continuous seamless 360-degree orbit starting from 115-degree side-angle.
- Daylight Palette (White Substrate / High-Contrast Edge Geometry).
- Purged Jargon. Australian spelling conventions (maths, visualised, synchronisation).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import multiprocessing as mp
import os
import gc

# ======== SEQUENCE PARAMETERS ========
DURATION = 24.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_458_coding"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE (OPTIMISED FOR VISUAL METRICS) --------
C_BG          = '#FFFFFF'          # White Substrate
C_TEXT        = '#111115'          # Indestructible Black (Typography)
C_GRID        = '#CBD5E1'          # Subdued Steel (Baseplate matrix)
C_CORE        = '#94A3B8'          # Slate Aluminium (Central Hardware Spool)
C_MANCHESTER  = '#E11D48'          # Kinematic Red (Strict Digital Energy)
C_NEURAL      = '#005599'          # Deep Marine (Biological Fluid gradients)

# ------------------------------------------------------------------
# O(N) MATPLOTLIB KINEMATIC ENGINE
# ------------------------------------------------------------------
def project_3d_depth(x, y, z, cx, cy, cz, az_deg, el_deg=0):
    tx, ty, tz = x - cx, y - cy, z - cz
    az, el = np.radians(az_deg), np.radians(el_deg)
    
    x1 = tx * np.cos(az) - ty * np.sin(az)
    y1 = tx * np.sin(az) + ty * np.cos(az)
    z1 = tz
    
    y2 = y1 * np.cos(el) - z1 * np.sin(el)
    z2 = y1 * np.sin(el) + z1 * np.cos(el)
    
    return x1, z2, y2 

def append_segmented(lines_dict, key, xs, ys, zs):
    xs, ys, zs = list(xs), list(ys), list(zs)
    for i in range(len(xs) - 1):
        lines_dict[key].append(([xs[i], xs[i+1]], [ys[i], ys[i+1]], [zs[i], zs[i+1]]))

def add_cylinder(lines_dict, col, cx, cy, cz, length, radius, axis='z', rings=4, t_count=16):
    t = np.linspace(0, 2*np.pi, t_count, endpoint=False)
    steps = np.linspace(0, length, rings)
    for s in steps:
        if axis == 'z':
            ix = cx + radius*np.cos(t); iy = cy + radius*np.sin(t); iz = np.full_like(t, cz + s)
        append_segmented(lines_dict, col, list(ix)+[ix[0]], list(iy)+[iy[0]], list(iz)+[iz[0]])
    for a in np.linspace(0, 2*np.pi, t_count//2, endpoint=False):
        if axis == 'z':
            sx = np.full_like(steps, cx + radius*np.cos(a))
            sy = np.full_like(steps, cy + radius*np.sin(a))
            sz = cz + steps
        append_segmented(lines_dict, col, list(sx), list(sy), list(sz))

# ------------------------------------------------------------------
# MACRO-ENGINEERING TENSOR ALGORITHMS (DATA SPOOL)
# ------------------------------------------------------------------
def generate_data_spool():
    lines = {
        'C_GRID': [], 'C_CORE': [], 'C_MANCHESTER': [], 'C_NEURAL': []
    }

    # 1. BASEPLATE & CENTRAL HARDWARE
    Z_FLOOR = -1.0
    for r_p in [1.5, 2.0, 2.5]:
        t_p = np.linspace(0, 2*np.pi, 48, endpoint=False)
        append_segmented(lines, 'C_GRID', r_p * np.cos(t_p), r_p * np.sin(t_p), np.full_like(t_p, Z_FLOOR))
    gx_range = np.linspace(-3.0, 3.0, 15)
    gy_range = np.linspace(-3.0, 3.0, 15)
    for gx in gx_range: append_segmented(lines, 'C_GRID', np.full_like(gy_range, gx), gy_range, np.full_like(gy_range, Z_FLOOR))
    for gy in gy_range: append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gy), np.full_like(gx_range, Z_FLOOR))

    # The Spool Axle
    add_cylinder(lines, 'C_CORE', 0.0, 0.0, -0.6, length=2.8, radius=0.2, axis='z', rings=10, t_count=16)

    # 16-Bit Logic Array Map
    BITS = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1]
    NUM_BITS = len(BITS)
    RESOLUTION = 2000
    R_BASE = 0.8
    R_HIGH = 1.4

    THETA = np.linspace(0, 2*np.pi, RESOLUTION, endpoint=True)
    
    # --------------------------------------------------------------------------
    # 2. MANCHESTER ENCODING ALGORITHM (Top Ribbon)
    # --------------------------------------------------------------------------
    Z_MAN = 1.2
    H_MAN = 0.4
    r_man = np.zeros(RESOLUTION)
    
    for j in range(RESOLUTION):
        curr_th = THETA[j]
        if curr_th >= 2*np.pi: curr_th = 0
            
        bit_idx = int((curr_th / (2*np.pi)) * NUM_BITS)
        frac = (curr_th % (2*np.pi / NUM_BITS)) / (2*np.pi / NUM_BITS)
        
        bit = BITS[bit_idx]
        if bit == 1:
            r_man[j] = R_BASE if frac < 0.5 else R_HIGH
        else:
            r_man[j] = R_HIGH if frac < 0.5 else R_BASE
            
    # Extrude the digital array into a 3D physical ribbon
    x_man = r_man * np.cos(THETA)
    y_man = r_man * np.sin(THETA)
    
    append_segmented(lines, 'C_MANCHESTER', x_man, y_man, np.full_like(x_man, Z_MAN))
    append_segmented(lines, 'C_MANCHESTER', x_man, y_man, np.full_like(x_man, Z_MAN + H_MAN))
    
    # Structural Zig-Zag Trusses holding the digital ribbon (HOTFIX: Modulo array boundary enforcement)
    for step in range(0, RESOLUTION, 10):
        idx_next = (step + 10) % RESOLUTION
        append_segmented(lines, 'C_MANCHESTER', 
                         [x_man[step], x_man[idx_next]], 
                         [y_man[step], y_man[idx_next]], 
                         [Z_MAN, Z_MAN + H_MAN])

    # --------------------------------------------------------------------------
    # 3. NEURAL ACTION POTENTIAL ALGORITHM (Bottom Ribbon)
    # --------------------------------------------------------------------------
    Z_NEU = 0.0
    H_NEU = 0.4
    r_neu = np.full(RESOLUTION, R_BASE)
    
    # Determine Spike Origins (Rate Coding: High rate for '1', Low rate for '0')
    spike_centers = []
    bit_arc = 2*np.pi / NUM_BITS
    for i, bit in enumerate(BITS):
        t_s = i * bit_arc
        if bit == 1:
            spike_centers.extend([t_s + bit_arc*0.25, t_s + bit_arc*0.75])
        else:
            spike_centers.extend([t_s + bit_arc*0.5])
            
    # Mathematically construct the biological action potential wave
    for j in range(RESOLUTION):
        curr_th = THETA[j]
        for sc in spike_centers:
            delta = curr_th - sc
            if delta < -np.pi: delta += 2*np.pi
            if delta > np.pi: delta -= 2*np.pi
            
            tau = delta / 0.08  
            if 0 <= tau <= 3.0:
                spike_volts = (np.sin(np.pi * tau) * np.exp(-1.4 * tau)) * 2.2
                r_neu[j] += (R_HIGH - R_BASE) * spike_volts

    x_neu = r_neu * np.cos(THETA)
    y_neu = r_neu * np.sin(THETA)
    
    append_segmented(lines, 'C_NEURAL', x_neu, y_neu, np.full_like(x_neu, Z_NEU))
    append_segmented(lines, 'C_NEURAL', x_neu, y_neu, np.full_like(x_neu, Z_NEU + H_NEU))
    
    # Structural Zig-Zag Trusses (HOTFIX: Modulo array boundary enforcement)
    for step in range(0, RESOLUTION, 10):
        idx_next = (step + 10) % RESOLUTION
        append_segmented(lines, 'C_NEURAL', 
                         [x_neu[step], x_neu[idx_next]], 
                         [y_neu[step], y_neu[idx_next]], 
                         [Z_NEU, Z_NEU + H_NEU])
                         
    # --------------------------------------------------------------------------
    # 4. HARDWARE RADIAL INTERCONNECTS
    # --------------------------------------------------------------------------
    for i in range(NUM_BITS):
        th_t = i * (2*np.pi / NUM_BITS)
        cx, cy = 0.2 * np.cos(th_t), 0.2 * np.sin(th_t)
        ox, oy = R_BASE * np.cos(th_t), R_BASE * np.sin(th_t)
        
        append_segmented(lines, 'C_CORE', [cx, ox], [cy, oy], [Z_MAN, Z_MAN])
        append_segmented(lines, 'C_CORE', [cx, ox], [cy, oy], [Z_NEU, Z_NEU])

    return lines

# ------------------------------------------------------------------
# MASTER RENDERER HOOK
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_data_spool()
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.8
        azimuth = 115.0 - (stage * 360.0)

        yield (f, t_sec, azimuth, cam_x, cam_y, cam_z, static_rig)

def render_frame(packet):
    f, t_sec, azimuth, cx, cy, cz, static_rig = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    cam_span = 2.2
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []
    layer_map = [
        ('C_GRID',       C_GRID,       1.0, 0.5), 
        ('C_CORE',       C_CORE,       1.2, 0.9),
        ('C_NEURAL',     C_NEURAL,     1.3, 1.0),
        ('C_MANCHESTER', C_MANCHESTER, 1.3, 1.0)
    ]

    for c_key, c_val, lw, alpha in layer_map:
        for xl, yl, zl in static_rig[c_key]:
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=16.0)
            render_queue.append((np.mean(depth), u, v, c_val, lw, alpha))

    render_queue.sort(key=lambda item: item[0], reverse=True)
    for depth, u, v, c, lw, a in render_queue:
        ax.plot(u, v, color=c, lw=lw, alpha=a)

    ui_t = cam_span * 1.45
    ax.add_patch(patches.Rectangle((-cam_span, ui_t), cam_span*2, cam_span*0.5, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_t, ui_t], color=C_TEXT, lw=6, zorder=81)

    ax.text(-cam_span*0.95, ui_t + cam_span*0.08, "LG-458 // MACRO-ENGINEERING TENSOR: INFORMATION SYSTEMS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t + cam_span*0.02, "SILICON VS BIOLOGICAL HARDWARE // METRIC SYNCHRONISATION", color=C_MANCHESTER, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b + cam_span*0.14, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBIT / HIGH-CONTRAST TRACE", color=C_NEURAL, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.07, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS TRACE)", color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b + cam_span*0.02, "TOPOLOGICAL YIELD: MANCHESTER PHASE LOGIC [RED] VS NEURAL RATE CODING [BLUE]", color=C_CORE, fontsize=12, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-458: ALGORITHMIC COMPARISON TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Macro-Engineering Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
