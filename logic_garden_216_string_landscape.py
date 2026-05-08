"""
SOVEREIGN CODE: logic_garden_216_string_landscape.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Topographical Topology (17.5 seconds)
SCENE: Logic Garden 216 (The String Landscape / Critical Damping)
HOTFIX: Parameter Scope Clamping, O(N) Depth Sorting, Helix Array Routing
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_216_string_landscape"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'
C_CYAN      = '#00FFFF'        # Fluid Topography (The Multiverse)
C_MAGENTA   = '#FF0055'        # Lethal Minima / Infinite Repulsion
C_GOLD      = '#FFD700'        # Critical Damping Algorithm
C_MANTIS    = '#00FF00'        # The Anthropic Filter / Terminal Biology

GRID_RES = 158  # 158 x 158 = 24964 particles
MAX_PARTICLES = GRID_RES * GRID_RES

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_void = np.array(hex_to_rgba(C_VOID)[:3])
c_text = np.array(hex_to_rgba(C_TEXT)[:3])
c_cyan = np.array(hex_to_rgba(C_CYAN)[:3])
c_mage = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_gold = np.array(hex_to_rgba(C_GOLD)[:3])
c_mantis = np.array(hex_to_rgba(C_MANTIS)[:3])
c_dim  = np.array(hex_to_rgba(C_DIM)[:3])

# ------------------------------------------------------------------
# O(1) 3D TENSOR ALGEBRA 
# ------------------------------------------------------------------
def rotate_3d(points, rx, ry, rz):
    cx, sx = np.cos(rx), np.sin(rx)
    cy, sy = np.cos(ry), np.sin(ry)
    cz, sz = np.cos(rz), np.sin(rz)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cx, 0], [0, 0, 1]])
    R = Rz.dot(Ry).dot(Rx)
    return points.dot(R.T)

# ------------------------------------------------------------------
# BASE GEOMETRY ARRAYS
# ------------------------------------------------------------------
np.random.seed(77)

# The Topographical Grid
gx = np.linspace(-150, 150, GRID_RES)
gy = np.linspace(-150, 150, GRID_RES)
XX, YY = np.meshgrid(gx, gy)
px_base = XX.flatten()
py_base = YY.flatten()

# Pre-calculate the Anthropic Well (The rare Golden Valley)
R_dist = np.sqrt(px_base**2 + py_base**2)
anthropic_well = -120.0 * np.exp(-(R_dist**2) / 600.0)

# Biological Geometry (Double Helix) for inside the well
helix_phase = px_base * 0.15
helix_x = 15.0 * np.cos(helix_phase)
helix_y = 15.0 * np.sin(helix_phase)
# Map Z inside the well to form a perfect column
helix_z = np.linspace(-120, 20, MAX_PARTICLES)
np.random.shuffle(helix_z) # Distribute vertically

# We only biologize the structure inside the critical damping zone
biology_mask = R_dist < 35.0

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, proj_x, proj_y, z_depth, colors, sizes, damping_val, is_flash, is_tathata = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_TEXT if is_flash else C_VOID
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    ax.set_xlim(-160, 160)
    ax.set_ylim(-260, 260)

    if not is_flash:
        # O(N) Depth Sorting
        sort_idx = np.argsort(z_depth)
        s_px = proj_x[sort_idx]
        s_py = proj_y[sort_idx]
        s_c = colors[sort_idx]
        s_s = sizes[sort_idx]

        ax.scatter(s_px, s_py, s=s_s, c=s_c, edgecolors='none', alpha=0.9, zorder=10)

        if is_tathata:
            # The Localized Bounding Box
            ax.add_patch(plt.Rectangle((-50, -180), 100, 260, facecolor='none', edgecolor=C_MANTIS, lw=3, linestyle='-', zorder=40))
            ax.text(0, -200, "EXISTENCE IS A BOUNDING BOX", color=C_MANTIS, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 100, "[ANTHROPIC FILTER LOCKED]", color=C_TEXT, fontsize=10, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    ui_col = C_CYAN
    if 4.5 <= t_sec < 9.0: ui_col = C_MAGENTA
    elif 9.0 <= t_sec < 14.8: ui_col = C_GOLD
    if is_tathata: ui_col = C_MANTIS
    
    txt_col = C_TEXT if not is_flash else C_VOID

    ax.text(-140, 240, "LG-216 :: THE STRING LANDSCAPE", color=ui_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: 10^500 VACUUM MINIMA / PHYSICAL LAW COMPILATION", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    
    # Physics compilation diagnostics
    status_physics = "ROLLING TOPOLOGY"
    c_phys = C_CYAN
    if 4.5 <= t_sec < 9.0:
        status_physics = "ERR: LETHAL GRAVITY / REPULSION" if f % 20 < 10 else "ERR: DIMENSIONAL CRASH"
        c_phys = C_MAGENTA
    elif 9.0 <= t_sec < 14.8:
        status_physics = "CRITICAL DAMPING REACHED"
        c_phys = C_GOLD
    elif is_tathata:
        status_physics = "TERMINAL BIOLOGY COMPILED"
        c_phys = C_MANTIS

    ax.text(-140, -220, "FUNDAMENTAL CONSTANTS", color=txt_col, fontsize=12, fontname='monospace', zorder=80)
    ax.text(-140, -235, f"STATUS: {status_physics}", color=c_phys, fontsize=12, fontname='monospace', weight='bold', zorder=80)
    
    ax.add_patch(plt.Rectangle((-140, -245), 280, 4, facecolor=C_DIM, zorder=80))
    ax.add_patch(plt.Rectangle((-140, -245), 280 * np.clip(damping_val, 0, 1), 4, facecolor=ui_col, zorder=81))

    # Phase Text Box
    ax.add_patch(plt.Rectangle((-140, 215), 280, 2, facecolor=ui_col, zorder=80))
    ax.text(140, 205, f"[{state_str}]", color=ui_col if (f%15<10 or is_tathata) else C_VOID, fontsize=14, fontname='monospace', weight='bold', ha='right', zorder=80)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) KINEMATIC TOPOGRAPHY ALGEBRA
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        is_flash = False
        is_tathata = False
        
        # Camera Array parameters
        cam_rx = -np.pi/3.5
        cam_ry = 0.0
        cam_rz = t_sec * 0.15 
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 4.0
        
        damping_val = 0.0

        current_x = np.copy(px_base)
        current_y = np.copy(py_base)
        
        # -------------------------------------------------------------
        # PHASE LOGIC & TOPOLOGY ALGEBRA
        # -------------------------------------------------------------
        if t_sec < 4.5:
            state = "10^500 VACUA :: THE LANDSCAPE"
            
            # Fluid topography rolling wave
            wave = 20.0 * np.sin(px_base*0.05 + t_sec*2) * np.cos(py_base*0.05 + t_sec*1.5)
            wave += 10.0 * np.sin(px_base*0.1 + t_sec*3)
            current_z = wave
            
            # Dynamic height mapping to Cyan/Dim tones
            norm_z = np.clip((current_z + 30) / 60, 0, 1)[:, None]
            colors = norm_z * c_cyan + (1.0 - norm_z) * c_dim
            sizes = 3.0 + norm_z.flatten() * 3.0
            
            damping_val = 0.1 * np.sin(t_sec*5) + 0.1

        elif t_sec < 9.0:
            state = "PARAMETER OVERWRITE :: LETHAL PHYSICS"
            
            wave = 30.0 * np.sin(px_base*0.08 + t_sec*4) * np.cos(py_base*0.08 + t_sec*2.5)
            wave += 20.0 * np.cos(np.sqrt(px_base**2 + py_base**2)*0.1 - t_sec*10) # Violent ripples
            current_z = wave
            
            norm_z = np.clip((current_z + 50) / 100, 0, 1)[:, None]
            
            # Instability flashes in Magenta
            flash_mag = f % 15 < 7
            base_col = c_mage if flash_mag else c_cyan
            colors = norm_z * base_col + (1.0 - norm_z) * c_dim
            sizes = 2.0 + norm_z.flatten() * (10.0 if flash_mag else 4.0)
            
            cam_rx -= np.sin(t_sec*20)*0.02 # Camera shake from physical law failure
            damping_val = np.random.rand() * 0.3

        elif t_sec < 14.8:
            state = "THE ANTHROPIC FILTER :: CRITICAL DAMPING"
            prog = (t_sec - 9.0) / 5.8
            if t_sec < 9.1: is_flash = True
            
            # The wild waves heavily decay while the Anthropic Well opens
            decay = (1.0 - prog**2)
            wave = 30.0 * np.sin(px_base*0.08 + t_sec*4) * np.cos(py_base*0.08 + t_sec*2.5) * decay
            
            # The geometric drop
            current_z = wave + anthropic_well * prog
            
            # O(1) Geometry Interpolation (DNA structure forms inside the well)
            well_interpolation = prog ** 3 # Accelerates deeply at the end
            if np.any(biology_mask):
                current_x[biology_mask] = px_base[biology_mask] * (1.0 - well_interpolation) + helix_x[biology_mask] * well_interpolation
                current_y[biology_mask] = py_base[biology_mask] * (1.0 - well_interpolation) + helix_y[biology_mask] * well_interpolation
                current_z[biology_mask] = (wave[biology_mask] + anthropic_well[biology_mask]) * (1.0 - well_interpolation) + helix_z[biology_mask] * well_interpolation
            
            colors[:, :] = c_cyan * (1.0 - prog) + c_dim * prog
            if np.any(biology_mask):
                # Inside the well turns Gold
                colors[biology_mask] = c_cyan * (1.0 - prog) + c_gold * prog
                sizes[biology_mask] = 8.0 * prog + 2.0
            
            damping_val = prog

        else:
            state = "TATHĀTĀ :: THE RARITY OF EXISTENCE"
            is_tathata = True
            
            current_z = anthropic_well
            
            if np.any(biology_mask):
                # Biological structure spins within the locked vacuum
                rot_t = (t_sec - 14.8) * 3.0
                hx = 15.0 * np.cos(helix_phase[biology_mask] + rot_t)
                hy = 15.0 * np.sin(helix_phase[biology_mask] + rot_t)
                current_x[biology_mask] = hx
                current_y[biology_mask] = hy
                current_z[biology_mask] = helix_z[biology_mask]

            # Multiverse fades entirely
            colors[:, :] = c_void
            
            if np.any(biology_mask):
                colors[biology_mask] = c_mantis
                sizes[biology_mask] = 8.0

            damping_val = 1.0
            
            if t_sec < 14.95:
                is_flash = True

        # Apply Global Tensor Matrix
        pts = np.column_stack([current_x, current_y, current_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1]
        z_depth = rot_pts[:, 2] 

        # O(1) Geometry Culling
        cull_mask = (proj_y > -260) & (proj_y < 260) & (proj_x > -160) & (proj_x < 160)

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], colors[cull_mask], sizes[cull_mask], damping_val, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 216: THE STRING LANDSCAPE [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Topographical O(N) Depth Routing & Anthropic Filter")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Biological Constants Locked.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
