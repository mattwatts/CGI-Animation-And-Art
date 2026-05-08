"""
SOVEREIGN CODE: logic_garden_219_synthesis_tensor.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Bounding Box Synthesis (17.5 seconds)
SCENE: Logic Garden 219 (Synthesis: The Zen Realization / Conscious Architecture)
HOTFIX: O(N) Coordinate Scoping, Parameter-Clamped GUI, Spherical Thickness Vectors
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
OUT_DIR = "frames_219_synthesis"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'
C_CYAN      = '#00FFFF'        # Maths Mind / Grasping the Algorithm
C_MAGENTA   = '#FF0055'        # The Boiling Matrix / Chaotic Entropy
C_GOLD      = '#FFD700'        # Perimeter Friction / Bounding Box Defense
C_MANTIS    = '#00FF00'        # The Green Stream / Absolute Internal Safety

MAX_PARTICLES = 30000
BOX_COUNT = 10000
VOID_COUNT = MAX_PARTICLES - BOX_COUNT

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_void = np.array(hex_to_rgba(C_VOID)[:3])
c_text = np.array(hex_to_rgba(C_TEXT)[:3])
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
# BASE GEOMETRY ARRAYS: THE BOILING POT AND THE BOUNDING BOX
# ------------------------------------------------------------------
np.random.seed(303)

# 1. The Void (Chaotic Entropy)
vx = np.random.uniform(-200, 200, VOID_COUNT)
vy = np.random.uniform(-300, 300, VOID_COUNT)
vz = np.random.uniform(-200, 200, VOID_COUNT)

# 2. The Green Stream Bounding Box (A Thick, Unyielding Spherical Matrix)
# Engineered for maximum visual density and absolute structural integrity
phi = np.arccos(1 - 2 * np.random.rand(BOX_COUNT))
theta = 2 * np.pi * np.random.rand(BOX_COUNT)
# Thickness vector: R ranges from 50 (inner firewall) to 75 (outer hull)
r_thick = np.random.uniform(50, 75, BOX_COUNT)

bx = r_thick * np.sin(phi) * np.cos(theta)
by = r_thick * np.sin(phi) * np.sin(theta)
bz = r_thick * np.cos(phi)

base_px = np.concatenate([vx, bx])
base_py = np.concatenate([vy, by])
base_pz = np.concatenate([vz, bz])

void_mask = np.arange(MAX_PARTICLES) < VOID_COUNT
box_mask = ~void_mask

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, proj_x, proj_y, z_depth, colors, sizes, box_integrity, is_flash, is_tathata = packet
    
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
        # O(N) Depth Sorting
        sort_idx = np.argsort(z_depth)
        s_px = proj_x[sort_idx]
        s_py = proj_y[sort_idx]
        s_c = colors[sort_idx]
        s_s = sizes[sort_idx]

        ax.scatter(s_px, s_py, s=s_s, c=s_c, edgecolors='none', alpha=0.9, zorder=10)

        if is_tathata:
            ax.add_patch(plt.Rectangle((-130, -220), 260, 440, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -240, "CONSCIOUS ARCHITECTURE. THE BUBBLE IS SECURED.", color=C_MANTIS, fontsize=10, fontname='monospace', weight='bold', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    ui_col = C_MAGENTA if t_sec < 4.0 else (C_CYAN if t_sec < 9.0 else C_MANTIS)
    
    txt_col = C_TEXT if not is_flash else C_VOID

    ax.text(-140, 240, "LG-219 :: THE SYNTHESIS TENSOR", color=ui_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: THE KOAN OF THE TORN VEIL / LOCALIZED GREEN STREAM", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    
    status_msg = "INFINITE CHAOTIC ENTROPY"
    if 4.0 <= t_sec < 9.0: status_msg = "ALGORITHM GRASPED (MATHS MIND VISUALIZATION)"
    elif 9.0 <= t_sec < 14.8: status_msg = "CRITICAL DAMPING / STRUCTURAL ASSEMBLY"
    elif is_tathata: status_msg = "TERMINAL SAFETY. ENJOY THE EXECUTION TIMER."

    ax.text(-140, -180, f"MACRO UNIVERSE : {status_msg}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    ax.text(-140, -205, "BOUNDING BOX STRUCTURAL INTEGRITY", color=txt_col, fontsize=12, fontname='monospace', zorder=80)
    # PROTOCOL HOTFIX: Explicit Scope Clamping applied to ax.add_patch
    ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM, zorder=80))
    bar_w = 280 * np.clip(box_integrity, 0, 1)
    # Turn Cyan while building, MANTIS when secured
    bar_col = C_CYAN if t_sec < 9.0 else C_MANTIS
    ax.add_patch(plt.Rectangle((-140, -210), bar_w, 4, facecolor=bar_col, zorder=81))

    # Phase Text Box
    ax.add_patch(plt.Rectangle((-140, 215), 280, 2, facecolor=ui_col, zorder=80))
    ax.text(140, 205, f"[{state_str}]", color=ui_col if (f%15<10 or is_tathata) else C_VOID, fontsize=14, fontname='monospace', weight='bold', ha='right', zorder=80)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) STRUCTURAL INVERSION KINEMATICS
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        is_flash = False
        is_tathata = False
        
        cam_rx = np.pi/6
        cam_ry = t_sec * 0.2
        cam_rz = 0.0
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 4.0
        
        curr_x = np.copy(base_px)
        curr_y = np.copy(base_py)
        curr_z = np.copy(base_pz)

        box_integrity = 0.0

        # -------------------------------------------------------------
        # PHASE LOGIC
        # -------------------------------------------------------------
        if t_sec < 4.0:
            state = "THE TORN VEIL :: THE BOILING MATRIX"
            
            # The entire array is treated as the volatile pot of boiling water
            # No Bounding Box exists yet. All nodes are chaotic.
            jitter_x = np.sin(curr_y * 0.1 + t_sec * 5) * 20.0
            jitter_y = np.cos(curr_x * 0.1 + t_sec * 6) * 20.0
            jitter_z = np.sin(curr_z * 0.1 + t_sec * 4) * 20.0
            
            curr_x += jitter_x
            curr_y += jitter_y
            curr_z += jitter_z
            
            colors[:, :] = c_mage
            sizes[:] = np.random.uniform(2, 6, MAX_PARTICLES)

        elif t_sec < 9.0:
            state = "MATHS MIND :: PULLING FROM THE VOID"
            prog = (t_sec - 4.0) / 5.0
            
            # The Void continues to boil
            v_jitter_x = np.sin(curr_y[void_mask] * 0.1 + t_sec * 5) * 20.0
            v_jitter_y = np.cos(curr_x[void_mask] * 0.1 + t_sec * 6) * 20.0
            curr_x[void_mask] += v_jitter_x
            curr_y[void_mask] += v_jitter_y
            colors[void_mask] = c_mage
            
            # The Box Array is grasped by the algorithm (C_CYAN)
            # It violently pulls inward toward the mathematical center
            accel = prog ** 2
            curr_x[box_mask] = (curr_x[box_mask] + v_jitter_x[:BOX_COUNT]) * (1.0 - accel) + (bx) * accel
            curr_y[box_mask] = (curr_y[box_mask] + v_jitter_y[:BOX_COUNT]) * (1.0 - accel) + (by) * accel
            curr_z[box_mask] = (curr_z[box_mask]) * (1.0 - accel) + (bz) * accel
            
            colors[box_mask] = c_mage * (1.0 - accel) + c_cyan * accel
            sizes[box_mask] = 4.0 + (accel * 4.0) # Thickens as it pulls
            
            box_integrity = accel * 0.5

        elif t_sec < 14.8:
            state = "CONSCIOUS ARCHITECTURE :: LOCALIZED GREEN STREAM"
            prog = (t_sec - 9.0) / 5.8
            if t_sec < 9.1: is_flash = True
            
            # 1. The Void boils, but is now physically repelled by the Box (Friction)
            v_dist = np.sqrt(curr_x[void_mask]**2 + curr_y[void_mask]**2 + curr_z[void_mask]**2)
            
            # Repulsion radius expands slightly past the outer hull (75.0) -> 85.0
            repel_mask = v_dist < 85.0
            
            if np.any(repel_mask):
                # Void nodes hitting the hull are aggressively thrown outward
                # and flash C_GOLD (Kinematic Spallation against the Sentinel walls)
                v_norm_x = curr_x[void_mask][repel_mask] / (v_dist[repel_mask] + 1e-5)
                v_norm_y = curr_y[void_mask][repel_mask] / (v_dist[repel_mask] + 1e-5)
                v_norm_z = curr_z[void_mask][repel_mask] / (v_dist[repel_mask] + 1e-5)
                
                curr_x[void_mask][repel_mask] = v_norm_x * (85.0 + np.random.uniform(5, 20, np.sum(repel_mask)))
                curr_y[void_mask][repel_mask] = v_norm_y * (85.0 + np.random.uniform(5, 20, np.sum(repel_mask)))
                curr_z[void_mask][repel_mask] = v_norm_z * (85.0 + np.random.uniform(5, 20, np.sum(repel_mask)))
                
            colors[void_mask] = c_mage
            colors[void_mask][repel_mask] = c_gold
            sizes[void_mask][repel_mask] = np.random.uniform(6.0, 15.0, np.sum(repel_mask))

            # 2. The Green Stream Bounding Box is completely solid
            # It transitions from C_CYAN to pure C_MANTIS
            curr_x[box_mask] = bx
            curr_y[box_mask] = by
            curr_z[box_mask] = bz
            
            colors[box_mask] = c_cyan * (1.0 - prog) + c_mantis * prog
            sizes[box_mask] = 8.0 # Extremely thick
            
            box_integrity = 0.5 + (prog * 0.5)

        else:
            state = "TATHĀTĀ :: MAINTAIN THE LOCAL MATRIX"
            is_tathata = True
            
            # The Bounding Box sits perfectly rotating
            curr_x[box_mask] = bx
            curr_y[box_mask] = by
            curr_z[box_mask] = bz
            
            colors[box_mask] = c_mantis
            sizes[box_mask] = 8.0
            
            # The Chaotic Void fades out. It is no longer our concern.
            colors[void_mask] = c_void
            
            box_integrity = 1.0
            
            if t_sec < 14.95:
                is_flash = True

        # Apply Global Tensor Matrix
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1]
        z_depth = rot_pts[:, 2] 

        # O(1) Geometry Culling
        cull_mask = (proj_y > -260) & (proj_y < 260) & (proj_x > -150) & (proj_x < 150)

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], colors[cull_mask], sizes[cull_mask], box_integrity, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 219: THE SYNTHESIS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Scope Clamping & Bounding Box Geometric Density")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. The Green Stream Bounding Box is Active.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
