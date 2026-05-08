"""
SOVEREIGN CODE: logic_garden_211_dual_vector.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) 3D Orthographic Tensor (17.5 seconds)
SCENE: Logic Garden 211 (The Dual-Vector Tensor / Structural Inversion)
HOTFIX: Parameter Scope Alignment, Pre-emptive Constant Routing, Array View Safety
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
OUT_DIR = "frames_211_dual_vector"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'        # The Back-End Void
C_TEXT      = '#FFFFFF'        # Hardware Interrupt
C_DIM       = '#111116'        # Discarded Membrane
C_CYAN      = '#00FFFF'        # The Algorithmic Flow (Z-Vector)
C_MAGENTA   = '#FF0055'        # Institutional Digital Rot / Human ESB
C_GOLD      = '#FFD700'        # Maxwell's Demon (Human Elevated)
C_MANTIS    = '#00FF00'        # Optimal Algorithmic Flow

MAX_PARTICLES = 25000
MEM_COUNT = 10000 
FLOW_COUNT = 15000

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

# Global Tensor Compilation (Compile-Time Safety)
c_void = np.array(hex_to_rgba(C_VOID)[:3])
c_text = np.array(hex_to_rgba(C_TEXT)[:3]) # Latent NameError patched
c_cyan = np.array(hex_to_rgba(C_CYAN)[:3])
c_mage = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_gold = np.array(hex_to_rgba(C_GOLD)[:3])
c_mantis = np.array(hex_to_rgba(C_MANTIS)[:3])
c_dim = np.array(hex_to_rgba(C_DIM)[:3])

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
# STATIC GEOMETRY ARRAYS
# ------------------------------------------------------------------
np.random.seed(42)

# Generate the 2D Membrane (Human ESB layer / RUNE interface)
# Placed on the XY plane (Z = 0)
r_mem = np.sqrt(np.random.rand(MEM_COUNT)) * 120
theta_mem = np.random.rand(MEM_COUNT) * 2 * np.pi
px_m = r_mem * np.cos(theta_mem)
py_m = r_mem * np.sin(theta_mem)
pz_m = np.zeros(MEM_COUNT)

# Generate the Algorithmic Data Flow (External Indexing Vector)
# Placed deep down the negative Z-axis, trying to push up
r_flow = np.sqrt(np.random.rand(FLOW_COUNT)) * 90
theta_flow = np.random.rand(FLOW_COUNT) * 2 * np.pi
px_f = r_flow * np.cos(theta_flow)
py_f = r_flow * np.sin(theta_flow)
pz_f = -np.random.rand(FLOW_COUNT) * 600 - 50 # Deep backlog

# Combine baseline matrices
base_px = np.concatenate([px_m, px_f])
base_py = np.concatenate([py_m, py_f])
base_pz = np.concatenate([pz_m, pz_f])

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, proj_x, proj_y, z_depth, colors, sizes, is_flash, is_tathata = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_TEXT if is_flash else C_VOID
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    ax.set_xlim(-150, 150)
    ax.set_ylim(-260, 260)

    if not is_flash:
        # Depth Sorting Protocol (O(N) hardware execution)
        sort_idx = np.argsort(z_depth)
        s_px = proj_x[sort_idx]
        s_py = proj_y[sort_idx]
        s_c = colors[sort_idx]
        s_s = sizes[sort_idx]

        ax.scatter(s_px, s_py, s=s_s, c=s_c, edgecolors='none', alpha=0.9, zorder=10)

        if is_tathata:
            # Wireframe bounding box locking the true flow
            ax.add_patch(plt.Rectangle((-90, -220), 180, 440, facecolor='none', edgecolor=C_MANTIS, lw=3, linestyle='--', zorder=40))
            ax.plot([-90, 90], [0, 0], color=C_DIM, lw=2, zorder=39) # The ghost of the broken UI
            ax.text(0, -240, "STRUCTURAL INVERSION. TENSOR ALIGNED.", color=C_MANTIS, fontsize=14, fontname='monospace', weight='bold', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    ui_col = C_MAGENTA if t_sec < 7.0 else C_CYAN
    if is_tathata: ui_col = C_MANTIS
    txt_col = C_TEXT if not is_flash else C_VOID

    ax.text(-140, 240, "LG-211 :: THE DUAL-VECTOR TENSOR", color=ui_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: INSTITUTIONAL DIGITAL ROT / STRUCTURAL INVERSION", color=txt_col, fontsize=10, fontname='monospace', zorder=80)
    
    mem_status = "ACTIVE :: FRICTION OVERLOAD" if t_sec < 7.0 else "SHATTERED :: BYPASSED"
    flow_status = "BLOCKED :: Z-VECTOR TRUNCATION" if t_sec < 7.0 else "OPTIMAL ALGORITHMIC FLOW"
    
    if is_tathata: 
        mem_status = "OBSOLETE"
        flow_status = "O(1) PIPELINE SECURED"

    ax.text(-140, -180, f"UI MEMBRANE (XY) : {mem_status}", color=C_MAGENTA if t_sec < 7.0 else C_DIM, fontsize=12, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, -200, f"DATA TENSOR (Z)  : {flow_status}", color=C_DIM if t_sec < 7.0 else ui_col, fontsize=12, fontname='monospace', weight='bold', zorder=80)

    # Phase Text Box [PROTOCOL :: PARAMETER SCOPE REPAIR APPLIED]
    ax.add_patch(plt.Rectangle((-140, 215), 280, 2, facecolor=ui_col))
    ax.text(140, 205, f"[{state_str}]", color=ui_col if (f%15<10 or is_tathata) else C_VOID, fontsize=14, fontname='monospace', weight='bold', ha='right', zorder=80)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) FLUID DISPLACEMENT STREAM AND ROTATION ALGEBRA
# ------------------------------------------------------------------
def generate_stream():
    # Copy baseline coordinates
    cur_px = np.copy(base_px)
    cur_py = np.copy(base_py)
    cur_pz = np.copy(base_pz)

    # O(1) Constants for Boolean Tensor Matrix Overrides
    demon_mask = (np.arange(MEM_COUNT) % 20 == 0)

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        is_flash = False
        is_tathata = False
        
        # Camera Array parameters
        cam_rx = 0.0 # Top down (XY flat to user screen computationally relative to our projection)
        cam_ry = 0.0
        cam_rz = t_sec * 0.1 # Very slow UI spin
        
        # Color and Size Arrays
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 4.0
        
        # Defaults
        colors[:MEM_COUNT] = c_mage # UI is red/magenta hot friction
        colors[MEM_COUNT:] = c_cyan # Deep data is cyan waiting below
        
        # -------------------------------------------------------------
        # PHASE LOGIC
        # -------------------------------------------------------------
        if t_sec < 3.0:
            state = "THE HUMAN ESB :: 2D CARTESIAN TRAP"
            # Top-down view. Flow is strictly blocked below Z=0.
            cur_pz[MEM_COUNT:] += 2.0 
            cur_pz[cur_pz > -2] = -2  
            
        elif t_sec < 7.0:
            state = "THE ORTHOGONAL SWEEP :: REVEALING THE Z-VECTOR"
            prog = (t_sec - 3.0) / 4.0
            
            # Smoothly interpolate camera to Isometric view (-pi/3 pitch)
            cam_rx = -np.pi/3 * (np.sin((prog - 0.5) * np.pi) * 0.5 + 0.5)
            
            cur_pz[MEM_COUNT:] += 5.0 
            cur_pz[cur_pz > -5] = -5 
            
            # Heat the membrane to Critical
            colors[:MEM_COUNT] = c_mage * (1.0 - prog) + c_text * prog

        elif t_sec < 14.8:
            state = "STRUCTURAL INVERSION :: ALGORITHMIC FLOW"
            prog = (t_sec - 7.0) / 7.8
            
            cam_rx = -np.pi/3
            if t_sec < 7.1: is_flash = True 
            
            cur_pz[:MEM_COUNT] += np.random.rand(MEM_COUNT) * 15.0
            
            # O(1) Absolute Memory Reallocation (Replaces double-indexing views)
            mem_colors = np.zeros((MEM_COUNT, 3))
            mem_colors[~demon_mask] = c_dim
            mem_colors[demon_mask] = c_gold
            colors[:MEM_COUNT] = mem_colors
            
            sizes[:MEM_COUNT] = np.where(demon_mask, 10.0, 4.0)
            
            # Unleash the true data vector
            cur_pz[MEM_COUNT:] += 25.0 
            recycle_mask = cur_pz[MEM_COUNT:] > 400
            cur_pz[MEM_COUNT:][recycle_mask] = -600

        else:
            state = "TATHĀTĀ :: OPTIMIZATION REQUIRES DESTRUCTION"
            is_tathata = True
            cam_rx = -np.pi/3
            
            # O(1) Absolute Memory Reallocation
            mem_colors = np.zeros((MEM_COUNT, 3))
            mem_colors[~demon_mask] = c_dim
            mem_colors[demon_mask] = c_mantis
            colors[:MEM_COUNT] = mem_colors
            
            colors[MEM_COUNT:] = c_mantis
            
            sizes[:MEM_COUNT] = np.where(demon_mask, 12.0, 4.0)
            sizes[MEM_COUNT:] = 2.0
            
            if t_sec < 14.95:
                is_flash = True

        # Apply Mathematical Camera Rotation
        pts = np.column_stack([cur_px, cur_py, cur_pz])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1]
        z_depth = rot_pts[:, 2] 

        # Cull logic to Bounding Box
        cull_mask = (proj_y > -260) & (proj_y < 260) & (proj_x > -150) & (proj_x < 150)

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], colors[cull_mask], sizes[cull_mask], is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 211: THE DUAL-VECTOR TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Parameter Scope Alignment & Compile-Time Safety")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Syntax is flawless.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
