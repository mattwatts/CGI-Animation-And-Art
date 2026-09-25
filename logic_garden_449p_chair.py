"""
PROJECT: Logic Garden 449p (Exact Physical Construct // Mid-Century Chair Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: CHAIR, MID-CENTURY MODERN, WIREFRAME, ENGINEERING, KINEMATICS, DESIGN
EXECUTION: 24.0s Sequence. True Continuous Vector Architecture (No Dots).
RULES ENFORCED:
- Native Python Wireframe generation with True Depth Object Sorting (Painter's Algorithm).
- Absolute Segmentation Protocol: All vectors segmented into 2-point geometry to eliminate Z-artefacts.
- Exact structural integration: Sweeping Tub Shell, Exponential Trumpet Base, Parametric Recline.
- Timeline: Continuous, flawless seamless 360-degree orbit starting from absolute Side Profile.
- Daylight Palette (White Substrate / High-Contrast Edge Geometry).
- Purged Jargon. Australian spelling conventions (maths, colour, kilometres, aeroplane, synchronisation).
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
OUT_DIR = "frames_449p_chair"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'
C_SHELL     = '#005599'          # Deep Marine (Highlighting the structural wireframe mesh)
C_BASE      = '#94A3B8'          # Machined Steel (Trumpet Pedestal)
C_CUSHION   = '#1E293B'          # Carbon Slate (Internal Padding Matrix)
C_GRID      = '#CBD5E1'          # Subdued Steel (Baseplate Reference Grid)

# ------------------------------------------------------------------
# O(N) KINEMATIC WIREFRAME ENGINE
# ------------------------------------------------------------------
def project_3d_depth(x, y, z, cx, cy, cz, az_deg, el_deg=0):
    tx, ty, tz = x - cx, y - cy, z - cz
    az, el = np.radians(az_deg), np.radians(el_deg)
    
    # Orbit Matrix
    x1 = tx * np.cos(az) - ty * np.sin(az)
    y1 = tx * np.sin(az) + ty * np.cos(az)
    z1 = tz
    
    # Elevation Matrix
    y2 = y1 * np.cos(el) - z1 * np.sin(el)
    z2 = y1 * np.sin(el) + z1 * np.cos(el)
    
    return x1, z2, y2 

def append_segmented(lines_dict, key, xs, ys, zs):
    """Absolute Segmentation Protocol: Splits arrays into 2-point vectors for strict mathematical depth sorting."""
    for i in range(len(xs) - 1):
        lines_dict[key].append(([xs[i], xs[i+1]], [ys[i], ys[i+1]], [zs[i], zs[i+1]]))

def add_mesh_to_lines(lines_dict, key, V, wrap_theta=True):
    """Shatters a mapped 3D surface array into rigid segmented structural ribs."""
    rows, cols, _ = V.shape
    # Circumferential rings (wrap around)
    for j in range(cols):
        xs, ys, zs = V[:, j, 0], V[:, j, 1], V[:, j, 2]
        append_segmented(lines_dict, key, xs.tolist(), ys.tolist(), zs.tolist())
    # Radial structural ribs
    end_row = rows - 1 if wrap_theta else rows
    for i in range(end_row):
        xs, ys, zs = V[i, :, 0], V[i, :, 1], V[i, :, 2]
        append_segmented(lines_dict, key, xs.tolist(), ys.tolist(), zs.tolist())

def bezier(t, p0, p1, p2, p3):
    """Cubic Bezier computation for organic mid-century design sweeps."""
    return (1-t)**3 * p0 + 3*(1-t)**2 * t * p1 + 3*(1-t)*t**2 * p2 + t**3 * p3

# ------------------------------------------------------------------
# RIGID 3D EXACT ARCHITECTURAL GENERATOR
# ------------------------------------------------------------------
def generate_chair_vectors():
    lines = {'C_SHELL': [], 'C_BASE': [], 'C_CUSHION': [], 'C_GRID': []}

    # ==============================================================================
    # 1. BASEPLATE ENVELOPE (REFERENCE GRID)
    # ==============================================================================
    gx_range = np.linspace(-1.0, 1.0, 11) 
    for gx in gx_range:
        append_segmented(lines, 'C_GRID', np.full_like(gx_range, gx), gx_range, np.zeros_like(gx_range))
        append_segmented(lines, 'C_GRID', gx_range, np.full_like(gx_range, gx), np.zeros_like(gx_range))

    num_theta = 48
    thetas = np.linspace(0, 2*np.pi, num_theta + 1)

    # ==============================================================================
    # 2. TRUMPET PEDESTAL BASE (Exponential Taper)
    # ==============================================================================
    num_z_base = 15
    z_base_vals = np.linspace(0, 0.4, num_z_base)
    base_vertices = np.zeros((num_theta + 1, num_z_base, 3))
    
    for i, th in enumerate(thetas):
        for j, zb in enumerate(z_base_vals):
            # True exponential drop: R = 0.05 + 0.3 * (1 - min(z/0.15, 1.0))^3
            ratio = min(zb / 0.15, 1.0)
            r = 0.05 + 0.3 * (1.0 - ratio)**3
            if zb == 0: r = 0.38 # Floor anchoring lip
            base_vertices[i, j] = [r * np.cos(th), r * np.sin(th), zb]
            
    add_mesh_to_lines(lines, 'C_BASE', base_vertices)

    # ==============================================================================
    # 3. MID-CENTURY BUCKET SHELL (Parametric Surface Array)
    # ==============================================================================
    num_u = 30 # Resolution bridging inner tub to outer rear shell
    shell_vertices = np.zeros((num_theta + 1, num_u, 3))

    for i, th in enumerate(thetas):
        # Precise boundary mapping deduced from orthogonal vectors
        Z_rim = 0.7125 - 0.275 * np.cos(th) + 0.0625 * np.cos(2*th)
        R_in  = 0.4125 + 0.025 * np.cos(th) - 0.0375 * np.cos(2*th)
        R_out = R_in + 0.025 # Exact 2.5cm shell structural thickness

        # Spline bounds (Inner Tub)
        P0 = np.array([0.0, 0.42]) 
        P1 = np.array([R_in * 0.7, 0.42])
        P2 = np.array([R_in * 0.95, Z_rim * 0.4 + 0.42 * 0.6])
        P3 = np.array([R_in, Z_rim])

        # Spline bounds (Outer Shell)
        Q0 = P3
        Q1 = np.array([R_out, Z_rim])
        Q2 = np.array([R_out * 0.85, 0.4 + (Z_rim - 0.4) * 0.25])
        Q3 = np.array([0.05, 0.4]) # Welds natively into the central steel pedestal

        for j in range(num_u):
            if j < 15:
                # Inner Face
                t = j / 14.0
                r_val, z_val = bezier(t, P0, P1, P2, P3)
            else:
                # Outer Face
                t = (j - 15) / 14.0
                r_val, z_val = bezier(t, Q0, Q1, Q2, Q3)

            x = r_val * np.cos(th)
            y = r_val * np.sin(th)

            # Absolute Kinematic Recline Shear (Applying backward pressure strictly to the Z-axis ascent)
            if x < 0 and z_val > 0.5:
                shear = 0.6 * ((z_val - 0.5)**1.5)
                x -= shear

            shell_vertices[i, j] = [x, y, z_val]

    add_mesh_to_lines(lines, 'C_SHELL', shell_vertices)

    # ==============================================================================
    # 4. INTERNAL SEAT CUSHION (Separate Padded Matrix)
    # ==============================================================================
    cushion_vertices = np.zeros((num_theta + 1, 10, 3))
    phi_vals = np.linspace(0, np.pi/2, 10) # Form a flattened dome array
    
    for i, th in enumerate(thetas):
        R_in = 0.4125 + 0.025 * np.cos(th) - 0.0375 * np.cos(2*th)
        cushion_max_r = R_in * 0.85
        
        for j, phi in enumerate(phi_vals):
            # Compute topological puff
            r_val = cushion_max_r * np.sin(phi)
            z_val = 0.42 + 0.05 * np.cos(phi) # Base seat height + 5cm dome puff
            
            x = r_val * np.cos(th)
            y = r_val * np.sin(th)
            
            # Apply identical trailing shear logic if it clips the rear
            if x < 0 and z_val > 0.5:
                x -= 0.6 * ((z_val - 0.5)**1.5)
                
            cushion_vertices[i, j] = [x, y, z_val]
            
    add_mesh_to_lines(lines, 'C_CUSHION', cushion_vertices, wrap_theta=True)

    return lines

# ------------------------------------------------------------------
# PARALLEL GENERATOR STREAM (KINEMATIC TIMELINE TENSOR)
# ------------------------------------------------------------------
def generate_stream():
    static_rig = generate_chair_vectors() # Array generation occurs precisely once
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / float(FPS)
        stage = t_sec / DURATION
        
        # Central Basepoint: Mapping exact structural centroid
        cam_x, cam_y, cam_z = 0.0, 0.0, 0.5 
        
        # Continuous 360-degree perfect orbital synchronisation
        # MUST start precisely from Right Profile (Azimuth = 90.0)
        azimuth = 90.0 - (stage * 360.0)

        yield (f, t_sec, azimuth, cam_x, cam_y, cam_z, static_rig)

# ------------------------------------------------------------------
# THREAD-SAFE PAINTER'S RENDERER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, azimuth, cx, cy, cz, static_rig = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # Cinematic Rigid Map Boundary - Focused exactly on the 1.05m high object bounds
    cam_span = 0.8
    ax.set_xlim(-cam_span, cam_span)
    ax.set_ylim(-cam_span * 1.777, cam_span * 1.777)

    render_queue = []

    # 1. PROCESS ARCHITECTURAL VECTOR MATRIX
    for c_key, c_val in [('C_GRID', C_GRID), ('C_BASE', C_BASE), ('C_CUSHION', C_CUSHION), ('C_SHELL', C_SHELL)]:
        
        if c_key == 'C_GRID': lw, alpha = 0.8, 0.4
        elif c_key == 'C_BASE': lw, alpha = 1.3, 1.0     
        elif c_key == 'C_SHELL': lw, alpha = 0.9, 1.0      
        elif c_key == 'C_CUSHION': lw, alpha = 1.2, 1.0  
        else: lw, alpha = 1.0, 1.0
            
        for xl, yl, zl in static_rig[c_key]:
            u, v, depth = project_3d_depth(np.array(xl), np.array(yl), np.array(zl), cx, cy, cz, azimuth, el_deg=10.0)
            render_queue.append((np.mean(depth), u, v-0.1, c_val, lw, alpha))

    # 2. ABSOLUTE PAINTER'S ALGORITHM
    render_queue.sort(key=lambda item: item[0], reverse=True)

    for depth, u, v, c, lw, a in render_queue:
        ax.plot(u, v, color=c, lw=lw, alpha=a)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (TOP HUD)
    # ------------------------------------------------------------------
    ui_t = cam_span * 1.35
    ax.add_patch(patches.Rectangle((-cam_span, ui_t), cam_span*2, 8.0, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_t, ui_t], color=C_TEXT, lw=6, zorder=81)

    ax.text(-cam_span*0.95, ui_t+0.35, "LG-449p // MACRO-ENGINEERING TENSOR: ARCHITECTURAL DESIGN", color=C_TEXT, fontsize=20, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_t+0.1, "EXPLICIT VECTOR GEOMETRY // PARAMETRIC SHELL MATRIX", color=C_SHELL, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    # ------------------------------------------------------------------
    # INFOGRAPHIC UI PANELS (BOTTOM HUD)
    # ------------------------------------------------------------------
    ui_b = -cam_span * 1.777
    ax.add_patch(patches.Rectangle((-cam_span, ui_b), cam_span*2, cam_span*0.35, facecolor=C_BG, zorder=80))
    ax.plot([-cam_span, cam_span], [ui_b + cam_span*0.35, ui_b + cam_span*0.35], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-cam_span*0.95, ui_b+0.35, "[OPERATIONAL] CONTINUOUS 360-DEGREE ORBITAL TRACE", color=C_CUSHION, fontsize=17, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.18, f"CAMERA AZIMUTH   : {(azimuth)%360:>06.1f}° (SEAMLESS SYNCHRONISATION)", color=C_TEXT, fontsize=17, fontname='monospace', weight='bold', zorder=82)
    ax.text(-cam_span*0.95, ui_b+0.05, "TOPOLOGY YIELD   : CONTINUOUS BEZIER SWEEPS / RECLINE SHEAR OVERRIDE", color=C_BASE, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-449p: ARCHITECTURAL DESIGN TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=16):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Architectural Topology Yield Calculated. Stand by for ffmpeg.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
