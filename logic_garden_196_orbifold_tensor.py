"""
SOVEREIGN CODE: logic_garden_196_orbifold_tensor.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Orbifold T^3/S_3 Tensor (17.5 seconds)
SCENE: Logic Garden 196 (The Harmonic Matrix / Twisted Prism)
HOTFIX: Voronoi Slice Calculation, Topologic Color Mapping, Bounding Box Supremacy
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
OUT_DIR = "frames_196_orbifold_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'        # Acoustic Vacuum
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'        # Deep Spatial Grid
C_CYAN      = '#00FFFF'        # UI Base
C_MAGENTA   = '#FF0055'        # UI Friction Overload
C_MAJOR     = '#32CD32'        # Lime Green (Major Triad Regions)
C_MINOR     = '#000080'        # Navy Blue (Minor Triad Regions)
C_AUG       = '#FFD700'        # Gold (Augmented Triad Singularity)
C_DEGEN     = '#FFFFFF'        # White (Degenerate Trichord Walls)
C_MANTIS    = '#00FF00'        # Terminal Geometry (Tathata Prism Wireframe)

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_void  = np.array(hex_to_rgba(C_VOID)[:3])
c_major = np.array(hex_to_rgba(C_MAJOR)[:3])
c_minor = np.array(hex_to_rgba(C_MINOR)[:3])
c_aug   = np.array(hex_to_rgba(C_AUG)[:3])
c_degen = np.array(hex_to_rgba(C_DEGEN)[:3])
c_cyan  = np.array(hex_to_rgba(C_CYAN)[:3])
c_mage  = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_mant  = np.array(hex_to_rgba(C_MANTIS)[:3])
c_txt   = np.array(hex_to_rgba(C_TEXT)[:3])

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE KINEMATIC ARCHITECTURE
# ------------------------------------------------------------------
MAX_PARTICLES = 35000

# Absolute Screen Viewport constraints
CAM_W = 100.0
CAM_H = CAM_W * (1920.0 / 1080.0) # 177.77
CENTER_X = 0.0
CENTER_Y = 0.0

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, px, py, p_sizes, c_tensor, z_slice, slice_radius, is_flash, is_tathata, bg_strobe = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_TEXT if is_flash else C_VOID
    if bg_strobe and not is_tathata: bg_hex = '#02000A' # Deep minor shift
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    # Absolute Viewport Lock
    ax.set_xlim(CENTER_X - CAM_W/2, CENTER_X + CAM_W/2)
    ax.set_ylim(CENTER_Y - CAM_H/2, CENTER_Y + CAM_H/2)

    # 1. RENDER BACKGROUND INFRASTRUCTURE
    if not is_flash and not is_tathata:
        # Base limits of the widest slice
        ax.add_patch(Circle((CENTER_X, CENTER_Y), 40.0, facecolor='none', edgecolor=C_DIM, lw=1, zorder=2))

    # 2. O(N) KINEMATIC VORONOI TENSOR
    if len(px) > 0 and not is_tathata:
        ax.scatter(px, py, s=p_sizes*6.0, c=c_tensor, edgecolors='none', alpha=0.9, zorder=10)

    # 3. TATHĀTĀ / GEOMETRIC INCIDENCE (TWISTED TRIANGULAR PRISM)
    if is_tathata and not is_flash:
        # We calculate the isometric projection of the pure Twisted Prism boundaries
        # A prism twisting 60 degrees from bottom to top
        z_vals = [-20.0, 20.0]
        r_prism = 35.0
        
        for z_i in z_vals:
            phase = 0 if z_i < 0 else np.pi/3
            pts = []
            for i in range(3):
                ang = phase + i * (2*np.pi/3)
                p_x = r_prism * np.cos(ang)
                # Pseudo depth for isometric UI
                p_y = (r_prism * np.sin(ang)) * 0.5 + z_i 
                pts.append([p_x, p_y])
                ax.scatter([p_x], [p_y], s=50, color=C_TEXT, zorder=25)
            
            # Bottom/Top Triangles
            ax.add_patch(Polygon(pts, closed=True, fill=False, edgecolor=C_MANTIS, lw=3, zorder=20))
            
            # Vertical twisting pillars connecting the layers
            if z_i < 0:
                for i in range(3):
                    ang_bot = 0 + i * (2*np.pi/3)
                    ang_top = np.pi/3 + i * (2*np.pi/3)
                    bx, by = r_prism*np.cos(ang_bot), (r_prism*np.sin(ang_bot))*0.5 - 20.0
                    tx, ty = r_prism*np.cos(ang_top), (r_prism*np.sin(ang_top))*0.5 + 20.0
                    ax.plot([bx, tx], [by, ty], color=C_MANTIS, lw=2, linestyle='--', zorder=19)

        # Central Singularity (Augmented)
        ax.scatter([0], [0], color=C_AUG, s=200, zorder=25)

    if is_flash:
        # Kinetic Overload Hardware Interrupt Screen Clear
        ax.add_patch(Rectangle((-CAM_W/2, -CAM_H/2), CAM_W, CAM_H, facecolor=C_TEXT, zorder=60))

    # 4. TELEMETRY WIDGETS (NEURAL ENTRAINMENT UI)
    ui_col = C_CYAN if not is_tathata else C_MANTIS
    if bg_strobe: ui_col = C_MAGENTA 
    txt_col = C_TEXT if not is_flash else C_VOID
    ui_bg   = C_VOID if not is_flash else C_TEXT
    
    # Top Bar 
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=ui_bg, alpha=0.9, zorder=80))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    ax.text(0.04, 0.965, "LG-196 :: ORBIFOLD T^3/S_3 TENSOR", transform=ax.transAxes, color=txt_col, fontsize=20, fontname='monospace', weight='bold', va='center', zorder=81)

    # Bottom Target Matrix
    ax.add_patch(plt.Rectangle((0, 0), 1.0, 0.14, transform=ax.transAxes, color=ui_bg, alpha=0.95, zorder=80))
    ax.plot([0, 1.0], [0.14, 0.14], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    
    dim_str = "EUCLIDEAN SLICE [Z]" if not is_tathata else "TATHATA [TWISTED PRISM]"
    ax.text(0.04, 0.10, f"METRIC: {dim_str} | TRANSPOSITION: {z_slice:05.2f}", transform=ax.transAxes, color=txt_col, fontsize=18, fontname='monospace', zorder=81)
    
    # Harmonic Z-Phase Bar
    fill_ratio = (z_slice + 1.0) / 2.0  # Normalize -1 to 1 into 0 to 1
    bar_col = C_CYAN
    if np.abs(z_slice) < 0.2: bar_col = C_AUG
    if is_tathata: bar_col = C_MANTIS
    if is_flash: bar_col = C_VOID
    
    ax.add_patch(plt.Rectangle((0.68, 0.03), 0.28, 0.03, transform=ax.transAxes, color=C_DIM, zorder=80))
    ax.add_patch(plt.Rectangle((0.68, 0.03), 0.28 * np.clip(fill_ratio, 0, 1), 0.03, transform=ax.transAxes, color=bar_col, zorder=81))
    ax.text(0.68, 0.07, f"HARMONIC PHASE: {fill_ratio*100:03.0f}%", transform=ax.transAxes, color=bar_col, fontsize=14, fontname='monospace', zorder=82)

    pulse = ui_col if (f % 10 < 5) and not is_flash else txt_col
    if bg_strobe and not is_tathata and f % 4 < 2: pulse = C_MAGENTA
    if is_flash: pulse = C_VOID

    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=20, fontname='monospace', weight='bold', zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)

# ------------------------------------------------------------------
# O(1) BALLISTIC/HARMONIC KINEMATICS STREAM
# ------------------------------------------------------------------
def generate_stream():
    # 1. Base Density Fluid (Fill the Maximum Hexagon)
    p_radii = np.random.uniform(0.0, 45.0, MAX_PARTICLES)
    p_angles = np.random.uniform(0.0, 2*np.pi, MAX_PARTICLES)
    
    # Thermal jitter for visual flow
    jitter_v = np.random.normal(0, 0.1, MAX_PARTICLES)
    
    max_radius = 40.0

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        dt = 0.016
        
        is_flash = False
        is_tathata = False
        bg_strobe = False
        
        # State variables
        z_slice = -1.0
        phase_spd = 0.0
        
        # ---- PHASE 1: THE EUCLIDEAN SLICE WAKE (0 - 4s) ----
        if t_sec < 4.0:
            state = "[01] CONTINUOUS METRIC :: CHORD INITIATION (Z = -1)"
            z_slice = -1.0 + (t_sec / 4.0) * 0.2
            phase_spd = 1.0
            
        # ---- PHASE 2: PARAMETRIC TRANSPOSITION (4 - 10s) ----
        elif t_sec < 10.0:
            state = "[02] INJECTING TRANSPOSITION TENSOR :: Z-SWEEP"
            prog = smoothstep((t_sec - 4.0) / 6.0)
            z_slice = -0.8 + (prog * 1.6) # Sweep from -0.8 to 0.8
            phase_spd = 1.5 + prog * 4.0

        # ---- PHASE 3: PHOTIC HARMONIC OVERLOAD (10 - 14.8s) ----
        elif t_sec < 14.8:
            state = "WARNING: TONAL MATRIX COMPRESSION. VORONOI OVERLOAD."
            prog = (t_sec - 10.0) / 4.8
            # Hyper-oscillation through the Z-axis bounds
            z_slice = 0.8 * np.sin(prog * 15.0 * np.pi) 
            phase_spd = 8.0 + (prog * 20.0)
            if t_sec > 13.5: bg_strobe = True

        # ---- PHASE 4: TATHĀTĀ / TWISTED PRISM BOUNDARY (14.8 - 17.5s) ----
        else:
            is_tathata = True
            z_slice = 0.0
            phase_spd = 0.0
            
            if t_sec < 14.95:
                is_flash = True
            state = "TATHĀTĀ: MUSIC IS NOT SOUND. IT IS PERFECTLY FOLDED GEOMETRY."

        # Update Vector Positions (Minor angular rotation simulating phase shift)
        if not is_tathata:
            p_angles = (p_angles + jitter_v * phase_spd * dt) % (2*np.pi)
            
        p_x = p_radii * np.cos(p_angles)
        p_y = p_radii * np.sin(p_angles)
        
        # -------------------------------------------------------------
        # THE CALCULUS OF THE ORBIFOLD (Voronoi Triads)
        # -------------------------------------------------------------
        # 1. Determine bounding polygon radius based on Z-slice
        # At z=0, it's a full Hexagon. At z=-1 or 1, it's a triangle.
        current_max_r = max_radius * (1.0 - (np.abs(z_slice) * 0.6))
        
        # Mask out particles outside the current z-bounding geometry bounds
        # Hexagonal bounded approximation filtering:
        mod_angles = p_angles % (np.pi / 3.0)
        hex_bound = current_max_r / np.cos(mod_angles - np.pi/6.0)
        
        # In actual Orbifold slice, the shape morphs. We approximate the geometric clip.
        active_mask = p_radii < hex_bound
        
        # 2. Chromatic Voronoi Topologies
        c_tensor = np.zeros((MAX_PARTICLES, 3))
        p_sizes = np.zeros(MAX_PARTICLES)
        
        if np.any(active_mask):
            act_r = p_radii[active_mask]
            act_ang = p_angles[active_mask]
            
            # Augmented Triads (The absolute Core singularity)
            mask_aug = act_r < (current_max_r * 0.15)
            
            # Major and Minor Regions (Alternating Sextants)
            sector_id = np.floor((act_ang / (2*np.pi)) * 6.0).astype(int)
            mask_maj = (sector_id % 2 == 0) & (~mask_aug)
            mask_min = (sector_id % 2 == 1) & (~mask_aug)
            
            # Degenerate Trichords (The white walls / dividing borders between phases)
            # Find points where angle is very close to breaking boundary
            dist_to_boundary = np.abs(act_ang % (np.pi/3.0) - (np.pi/6.0))
            mask_degen = (dist_to_boundary > 0.45) & (~mask_aug)
            
            # Array application
            tmp_c = np.zeros((np.sum(active_mask), 3))
            tmp_c[mask_maj] = c_major
            tmp_c[mask_min] = c_minor
            tmp_c[mask_degen] = c_degen
            tmp_c[mask_aug]  = c_aug
            
            c_tensor[active_mask] = tmp_c
            p_sizes[active_mask] = 8.0 # Large fluid Voronoi blobs

        if is_tathata:
            c_tensor[:] = c_mant
            p_sizes[:] = 1.0
            
        c_tensor = np.clip(c_tensor, 0.0, 1.0)

        yield (f, t_sec, state, np.copy(p_x[active_mask]), np.copy(p_y[active_mask]), p_sizes[active_mask], c_tensor[active_mask], z_slice, current_max_r, is_flash, is_tathata, bg_strobe)

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 196: THE ORBIFOLD TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Absolute Bounding Box Alignment & Parametric Scaling")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Nodes: {MAX_PARTICLES}")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
