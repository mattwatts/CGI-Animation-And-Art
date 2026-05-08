"""
SOVEREIGN CODE: logic_garden_197_tralfamadorian_tensor.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Tralfamadorian Block Universe Tensor (17.5 seconds)
SCENE: Logic Garden 197 (The Tralfamadorian Tensor / Space-Time)
HOTFIX: Z-Axis Chronological Extrusion, Isometric Bounding Box, Frame De-compression
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_197_tralfamadorian_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'        # Spacetime Vacuum
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'        # Base Infrastructure Grid
C_CYAN      = '#00FFFF'        # The Local Present (Slice)
C_MAGENTA   = '#FF0055'        # Solidified Past/Future
C_GOLD      = '#FFD700'        # Zenith Nodes
C_RED       = '#FF3300'        # Kinetic Friction
C_MANTIS    = '#00FF00'        # Terminal Geometry (Tathata / Block Universe)

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_void = np.array(hex_to_rgba(C_VOID)[:3])
c_cyan = np.array(hex_to_rgba(C_CYAN)[:3])
c_mage = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_gold = np.array(hex_to_rgba(C_GOLD)[:3])
c_mant = np.array(hex_to_rgba(C_MANTIS)[:3])
c_txt  = np.array(hex_to_rgba(C_TEXT)[:3])

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE KINEMATIC ARCHITECTURE
# ------------------------------------------------------------------
NUM_TRAILS  = 50
PTS_PER_TRL = 1000
MAX_PARTICLES = NUM_TRAILS * PTS_PER_TRL

CENTER_X = 0.0
CENTER_Y = 0.0

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, px, py, p_sizes, c_tensor, box_edges, cam_w, z_slice_w, is_flash, is_tathata, bg_strobe = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_TEXT if is_flash else C_VOID
    if bg_strobe and not is_tathata: bg_hex = '#0A0010' 
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    # Absolute Viewport Bounding Box
    cam_h = cam_w * (1920.0 / 1080.0)
    ax.set_xlim(CENTER_X - cam_w/2, CENTER_X + cam_w/2)
    ax.set_ylim(CENTER_Y - cam_h/2, CENTER_Y + cam_h/2)

    # 1. RENDER BLOCK UNIVERSE WIREFRAME
    if not is_flash and len(box_edges) > 0:
        c_line = C_MANTIS if is_tathata else C_DIM
        alpha_line = 0.8 if is_tathata else 0.3
        for edge in box_edges:
            ax.plot([edge[0], edge[2]], [edge[1], edge[3]], color=c_line, lw=1.5, alpha=alpha_line, zorder=5)

    # 2. O(N) KINEMATIC TENSOR (The Trajectories)
    if len(px) > 0 and not is_tathata:
        ax.scatter(px, py, s=p_sizes*4.0, c=c_tensor, edgecolors='none', alpha=0.5, zorder=10)
        ax.scatter(px, py, s=p_sizes*1.0, c=C_TEXT if is_flash else c_tensor, edgecolors='none', alpha=0.9, zorder=11)

    # 3. TATHĀTĀ / GEOMETRIC INCIDENCE (So it goes)
    if is_tathata and not is_flash:
        ax.scatter(px, py, s=p_sizes*1.5, c=C_MANTIS, edgecolors='none', alpha=0.7, zorder=10)
        # The Absolute Center 
        ax.scatter([CENTER_X], [CENTER_Y], s=150, color=C_VOID, edgecolor=C_MANTIS, lw=2, zorder=20)
        ax.add_patch(Circle((CENTER_X, CENTER_Y), cam_w*0.4, facecolor='none', edgecolor=C_MANTIS, lw=2, linestyle='--', zorder=19))

    if is_flash:
        # Kinetic Overload Hardware Interrupt Screen Clear
        ax.add_patch(Rectangle((CENTER_X - cam_w, CENTER_Y - cam_h), cam_w*2, cam_h*2, facecolor=C_TEXT, zorder=60))

    # 4. TELEMETRY WIDGETS (NEURAL ENTRAINMENT UI)
    ui_col = C_CYAN if not is_tathata else C_MANTIS
    if z_slice_w > 0.8: ui_col = C_MAGENTA 
    txt_col = C_TEXT if not is_flash else C_VOID
    ui_bg   = C_VOID if not is_flash else C_TEXT
    
    # Top Bar 
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=ui_bg, alpha=0.9, zorder=80))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    ax.text(0.04, 0.965, "LG-197 :: TRALFAMADORIAN BLOCK UNIVERSE", transform=ax.transAxes, color=txt_col, fontsize=20, fontname='monospace', weight='bold', va='center', zorder=81)

    # Bottom Target Matrix
    ax.add_patch(plt.Rectangle((0, 0), 1.0, 0.14, transform=ax.transAxes, color=ui_bg, alpha=0.95, zorder=80))
    ax.plot([0, 1.0], [0.14, 0.14], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    
    dim_str = "LOCAL LINEAR TIME" if z_slice_w < 0.1 else "4D CHRONO-COMPRESSION"
    if is_tathata: dim_str = "TATHATA [ABSOLUTE STATIC METRIC]"
    
    ax.text(0.04, 0.10, f"METRIC: {dim_str}", transform=ax.transAxes, color=txt_col, fontsize=18, fontname='monospace', zorder=81)
    
    # Time Compression Bar
    fill_ratio = min(1.0, max(0.0, z_slice_w))
    bar_col = C_CYAN
    if fill_ratio > 0.6: bar_col = C_MAGENTA
    if fill_ratio > 0.9: bar_col = C_GOLD
    if is_tathata: bar_col = C_MANTIS
    if is_flash: bar_col = C_VOID
    
    ax.add_patch(plt.Rectangle((0.68, 0.03), 0.28, 0.03, transform=ax.transAxes, color=C_DIM, zorder=80))
    ax.add_patch(plt.Rectangle((0.68, 0.03), 0.28 * fill_ratio, 0.03, transform=ax.transAxes, color=bar_col, zorder=81))
    
    status_msg = f"{fill_ratio*100:03.0f}%" if not is_tathata else "SO IT GOES."
    ax.text(0.68, 0.07, f"Z-AXIS REVELATION: {status_msg}", transform=ax.transAxes, color=bar_col, fontsize=14, fontname='monospace', zorder=82)

    pulse = ui_col if (f % 10 < 5) and not is_flash else txt_col
    if fill_ratio > 0.9 and not is_tathata and f % 4 < 2: pulse = C_MAGENTA
    if is_flash: pulse = C_VOID

    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=20, fontname='monospace', weight='bold', zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

def project_3d_to_2d(x, y, z, rot_x, rot_y, scale=1.0):
    # O(1) Isometric Numpy projection.
    
    # Rotate around Y axis
    x_new = x*np.cos(rot_y) - z*np.sin(rot_y)
    z_new = x*np.sin(rot_y) + z*np.cos(rot_y)
    x, z = x_new, z_new
    
    # Rotate around X axis
    y_new = y*np.cos(rot_x) - z*np.sin(rot_x)
    z_new = y*np.sin(rot_x) + z*np.cos(rot_x)
    y, z = y_new, z_new
    
    return x * scale, y * scale

def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)

# ------------------------------------------------------------------
# O(1) BALLISTIC KINEMATICS STREAM
# ------------------------------------------------------------------
def generate_stream():
    # 1. Generate the absolute Block Universe up front
    # 50 entities, tracing continuous fluid paths through time (Z-axis).
    rng = np.random.default_rng(42) # Deterministic universe
    
    # Z acts as time: -100 (Birth) to +100 (Death)
    z_space = np.linspace(-100, 100, PTS_PER_TRL)
    master_z = np.tile(z_space, NUM_TRAILS)
    
    master_x = np.zeros(MAX_PARTICLES)
    master_y = np.zeros(MAX_PARTICLES)
    
    # Build Lissajous/Harmonic trajectories for each entity
    for i in range(NUM_TRAILS):
        idx_start = i * PTS_PER_TRL
        idx_end = idx_start + PTS_PER_TRL
        
        freq_x = rng.uniform(0.01, 0.05)
        freq_y = rng.uniform(0.01, 0.05)
        phase_x = rng.uniform(0, 2*np.pi)
        phase_y = rng.uniform(0, 2*np.pi)
        amp_x = rng.uniform(10, 40)
        amp_y = rng.uniform(10, 40)
        
        master_x[idx_start:idx_end] = np.sin(z_space * freq_x + phase_x) * amp_x
        master_y[idx_start:idx_end] = np.cos(z_space * freq_y + phase_y) * amp_y

    cam_w = 120.0

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        is_flash = False
        is_tathata = False
        bg_strobe = False
        
        # State variables
        z_slice_w = 0.0
        current_time_z = -100.0
        rot_x = 0.0 # Viewing down the Z axis initially (looking at standard xy plane)
        rot_y = 0.0 
        target_cam_w = 120.0
        
        # ---- PHASE 1: THE ILLUSION OF FLOW (0 - 5s) ----
        if t_sec < 5.0:
            state = "[01] CONTINUOUS METRIC :: THE ILLUSION OF FLOW"
            prog = t_sec / 5.0
            current_time_z = -100.0 + (prog * 200.0) # Move linearly through time
            z_slice_w = 0.0 # Restrict vision to the present moment
            
        # ---- PHASE 2: THE TRALFAMADORIAN REVELATION (5 - 11s) ----
        elif t_sec < 11.0:
            state = "[02] INJECTING PROJECTION TENSOR :: Z-AXIS UNBOUND"
            prog = smoothstep((t_sec - 5.0) / 6.0)
            current_time_z = 100.0 # Reached the end
            z_slice_w = prog # Slowly open the aperture to reveal past and future
            
            # Rotate camera isometrically to show the length of the time block
            rot_x = prog * (np.pi/4) # 45 degree tilt
            rot_y = prog * (np.pi/4)
            target_cam_w = 120.0 + (prog * 150.0) # Zoom out to see the whole block

        # ---- PHASE 3: COMPRESSION / BLOCK UNIVERSE ROTATION (11 - 14.8s) ----
        elif t_sec < 14.8:
            state = "WARNING: CHRONOLOGICAL OVERLOAD. SIMULTANEOUS EXISTENCE."
            prog = (t_sec - 11.0) / 3.8
            z_slice_w = 1.0
            
            # Massive continuous rotation of the 4D block
            rot_x = (np.pi/4) + np.sin(prog * np.pi) * 0.2
            rot_y = (np.pi/4) + (prog * 2.0)
            target_cam_w = 270.0

            if t_sec > 13.5: bg_strobe = True

        # ---- PHASE 4: TATHĀTĀ / SO IT GOES (14.8 - 17.5s) ----
        else:
            is_tathata = True
            z_slice_w = 1.0
            rot_x = np.pi/6
            rot_y = np.pi/4 # Static lock
            target_cam_w = 250.0
            
            if t_sec < 14.95:
                is_flash = True
            state = "TATHĀTĀ: TIME IS A STATIC MATRIX. SO IT GOES."

        cam_w += (target_cam_w - cam_w) * 0.1

        # -------------------------------------------------------------
        # THE CALCULUS OF THE BLOCK UNIVERSE
        # -------------------------------------------------------------
        
        # Determine visibility mask based on chronological compression
        if z_slice_w < 0.01:
            # Phase 1: Only the present exists
            # We allow a small trailing tail for visual persistence
            dist = np.clip((current_time_z - master_z) / 10.0, 0, 1)
            active_mask = (master_z <= current_time_z) & (master_z > current_time_z - 10.0)
        else:
            # Phase 2&3: Expanding the slice symmetrically to reveal all time
            visible_radius = 10.0 + (z_slice_w * 250.0)
            active_mask = np.abs(master_z - 0.0) < visible_radius
            current_time_z = np.max(master_z[active_mask]) if np.any(active_mask) else 100.0

        # Project standard coordinates isometrically
        px, py = project_3d_to_2d(master_x, master_y, master_z, rot_x, rot_y, scale=1.0)

        # Base wireframe Bounding Box (The dimensions of the universe)
        box_edges = []
        if z_slice_w > 0.01:
            size_xy = 50.0
            size_z = 100.0
            corners = [
                [-size_xy, -size_xy, -size_z], [size_xy, -size_xy, -size_z], [size_xy, size_xy, -size_z], [-size_xy, size_xy, -size_z],
                [-size_xy, -size_xy,  size_z], [size_xy, -size_xy,  size_z], [size_xy, size_xy,  size_z], [-size_xy, size_xy,  size_z]
            ]
            proj_corn = [project_3d_to_2d(c[0], c[1], c[2], rot_x, rot_y) for c in corners]
            
            # Connect bottom
            for i in range(4): box_edges.append([proj_corn[i][0], proj_corn[i][1], proj_corn[(i+1)%4][0], proj_corn[(i+1)%4][1]])
            # Connect top
            for i in range(4,8): box_edges.append([proj_corn[i][0], proj_corn[i][1], proj_corn[4+(i+1)%4][0], proj_corn[4+(i+1)%4][1]])
            # Connect pillars
            for i in range(4): box_edges.append([proj_corn[i][0], proj_corn[i][1], proj_corn[i+4][0], proj_corn[i+4][1]])

        # -------------------------------------------------------------
        # SYNTAX REPAIR: ABSOLUTE VARIABLE BINDING & COLOR MAPPING
        # -------------------------------------------------------------
        p_sizes = np.ones(MAX_PARTICLES)
        c_tensor = np.zeros((MAX_PARTICLES, 3))
        
        if np.any(active_mask):
            z_act = master_z[active_mask]
            
            if z_slice_w < 0.01:
                # Phase 1: Pure Cyan points, with alpha trailing
                c_tensor[active_mask] = c_cyan
                p_sizes[active_mask] = 4.0
            else:
                # The full structure. Magenta core, transitioning to Cyan at the chronos tips.
                # Distance from origin
                norm_z = np.abs(z_act) / 100.0
                
                # Blend Magenta to Cyan
                blend_c = norm_z[:, None] * c_cyan + (1.0 - norm_z[:, None]) * c_mage
                c_tensor[active_mask] = blend_c
                p_sizes[active_mask] = 1.5 + (1.0 - norm_z) * 2.0

        if is_tathata:
            c_tensor[:] = c_mant
            p_sizes[:] = 1.0
            
        c_tensor = np.clip(c_tensor, 0.0, 1.0)

        yield (f, t_sec, state, np.copy(px[active_mask]), np.copy(py[active_mask]), p_sizes[active_mask], c_tensor[active_mask], box_edges, cam_w, z_slice_w, is_flash, is_tathata, bg_strobe)

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 197: THE TRALFAMADORIAN TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: 4D Chronological Extrusion & Bounding Box Supremacy")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Nodes: {MAX_PARTICLES}")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
