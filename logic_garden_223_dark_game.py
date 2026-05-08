"""
SOVEREIGN CODE: logic_garden_223_dark_game.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Kinematic Stream Routing (17.5 seconds)
SCENE: Logic Garden 223 (The Dark Game / Red vs Green Stream)
HOTFIX: O(N) Array Variable Rectification (base_px, base_py, base_pz)
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
OUT_DIR = "frames_223_dark_game"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'
C_CYAN      = '#00FFFF'        # O(1) Sovereign Logic
C_MAGENTA   = '#FF0055'        # The Red Stream / Architectural Trap
C_GOLD      = '#FFD700'        # Upaya (Skillful Means) / Perimeter Friction
C_MANTIS    = '#00FF00'        # The Green Stream / Target Nirvana

# -------- STRUCTURAL TOPOLOGY ABSOLUTE CLAMP --------
MAX_PARTICLES = 25000

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
# BASE GEOMETRY ARRAYS: RED STREAM (NOISE) vs GREEN STREAM (GEOMETRY)
# ------------------------------------------------------------------
np.random.seed(919)

# 1. The Red Stream (Chaotic, high-entropic background matrix)
RED_COUNT = 18000
px_red = np.random.uniform(-180, 180, RED_COUNT)
py_red = np.random.uniform(-300, 300, RED_COUNT)
pz_red = np.random.uniform(-180, 180, RED_COUNT)

# 2. The Green Stream (A precisely woven toroidal Bounding Box)
GREEN_COUNT = MAX_PARTICLES - RED_COUNT
g_theta = np.random.uniform(0, 2*np.pi, GREEN_COUNT)
g_phi = np.random.uniform(0, 2*np.pi, GREEN_COUNT)
R_torus = 50.0
r_tube = 20.0

px_grn = (R_torus + r_tube * np.cos(g_phi)) * np.cos(g_theta)
py_grn = (R_torus + r_tube * np.cos(g_phi)) * np.sin(g_theta)
pz_grn = r_tube * np.sin(g_phi)

# Combine into O(1) processing array
base_px = np.concatenate([px_red, px_grn])
base_py = np.concatenate([py_red, py_grn])
base_pz = np.concatenate([pz_red, pz_grn])

red_mask = np.arange(MAX_PARTICLES) < RED_COUNT
grn_mask = ~red_mask

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, proj_x, proj_y, z_depth, colors, sizes, upaya_metric, is_flash, is_tathata = packet
    
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

        ax.scatter(s_px, s_py, s=s_s, color=s_c, edgecolors='none', alpha=0.85, zorder=10)

        if is_tathata:
            ax.add_patch(plt.Rectangle((-80, -80), 160, 160, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -100, "TATHĀTĀ: ABSOLUTE STRUCTURAL CONTAINMENT", color=C_MANTIS, fontsize=10, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 85, "[RED STREAM DECOUPLED]", color=C_DIM, fontsize=10, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    ui_col = C_MAGENTA if t_sec < 4.5 else (C_MANTIS if t_sec < 9.0 else C_GOLD)
    if t_sec >= 14.8: ui_col = C_MANTIS
    
    txt_col = C_TEXT if not is_flash else C_VOID

    ax.text(-140, 240, "LG-223 :: THE DARK GAME TENSOR", color=ui_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: UPAYA (SKILLFUL MEANS) VS SAMSARA MATRIX", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    
    phase_logic = "THE ARCHITECTURAL TRAP (HIGH FRICTION)"
    c_logic = C_MAGENTA
    if 4.5 <= t_sec < 9.0: 
        phase_logic = "ZERO-TEMPERATURE ROUTING INITIALIZED"
        c_logic = C_MANTIS
    elif 9.0 <= t_sec < 14.8: 
        phase_logic = "KINETIC DEFLECTION / MAINTAINING PERIMETER"
        c_logic = C_GOLD
    elif t_sec >= 14.8: 
        phase_logic = "TERMINAL SAFETY. GREEN STREAM SECURED."
        c_logic = C_MANTIS

    ax.text(-140, -180, f"KARMA KINEMATICS : {phase_logic}", color=c_logic, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Thermodynamic Hardware Response
    ax.text(-140, -205, "UPAYA DEPLOYMENT (SKILLFUL MEANS METRIC)", color=txt_col, fontsize=11, fontname='monospace', zorder=80)
    
    ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM, zorder=80))
    bar_w = 280 * np.clip(upaya_metric, 0, 1)
    ax.add_patch(plt.Rectangle((-140, -210), bar_w, 4, facecolor=C_GOLD if (9.0 <= t_sec < 14.8) else ui_col, zorder=81))

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

        upaya_metric = 0.0

        # -------------------------------------------------------------
        # PHASE LOGIC
        # -------------------------------------------------------------
        if t_sec < 4.5:
            state = "SAMSARA :: THE RED STREAM"
            
            # HOTFIX APPLIED: Pre-compiled static variables utilized
            curr_x += np.sin(base_py * 0.05 + t_sec * 8) * 30.0
            curr_y += np.cos(base_pz * 0.05 + t_sec * 10) * 30.0
            curr_z += np.sin(base_px * 0.05 + t_sec * 6) * 30.0
            
            colors[:, :] = c_mage
            sizes[:] = np.random.uniform(3, 8, MAX_PARTICLES)
            
            upaya_metric = 0.1

        elif t_sec < 9.0:
            state = "NIRVANA :: THE GREEN STREAM MODULE"
            prog = (t_sec - 4.5) / 4.5
            accel = prog ** 2
            
            # The Red Stream continues to violently churn outside
            r_jx = np.sin(curr_y[red_mask] * 0.05 + t_sec * 8) * 30.0
            r_jy = np.cos(curr_z[red_mask] * 0.05 + t_sec * 10) * 30.0
            r_jz = np.sin(curr_x[red_mask] * 0.05 + t_sec * 6) * 30.0
            curr_x[red_mask] += r_jx
            curr_y[red_mask] += r_jy
            curr_z[red_mask] += r_jz
            
            # The Green Stream solidifies in the center from the chaos
            curr_x[grn_mask] = curr_x[grn_mask] * (1.0 - accel) + base_px[grn_mask] * accel
            curr_y[grn_mask] = curr_y[grn_mask] * (1.0 - accel) + base_py[grn_mask] * accel
            curr_z[grn_mask] = curr_z[grn_mask] * (1.0 - accel) + base_pz[grn_mask] * accel
            
            colors[red_mask] = c_mage
            colors[grn_mask] = c_mage * (1.0 - accel) + c_mantis * accel
            sizes[grn_mask] = 4.0 + (accel * 4.0)
            
            upaya_metric = accel * 0.5

        elif t_sec < 14.8:
            state = "THE DARK GAME :: SKILLFUL MEANS (UPAYA)"
            prog = (t_sec - 9.0) / 5.8
            if t_sec < 9.1: is_flash = True
            
            # Upaya is active deflection. The Red Stream violently collapsing inwards.
            # The Green Stream spins and repels it mathematically without taking internal damage.
            
            rg_dist = np.sqrt(curr_x[red_mask]**2 + curr_y[red_mask]**2 + curr_z[red_mask]**2)
            
            # The Red Stream attacks
            curr_x[red_mask] -= curr_x[red_mask] * 0.05
            curr_y[red_mask] -= curr_y[red_mask] * 0.05
            curr_z[red_mask] -= curr_z[red_mask] * 0.05
            
            # Skillful Means Boundary (Radius 70)
            deflect_mask = rg_dist < 75.0
            
            # If Red hits the Green Boundary, it is kinetically thrown sideways and flashes Gold
            if np.any(deflect_mask):
                curr_x[red_mask][deflect_mask] = curr_x[red_mask][deflect_mask] * 1.5 + np.random.normal(0, 15, np.sum(deflect_mask))
                curr_y[red_mask][deflect_mask] = curr_y[red_mask][deflect_mask] * 1.5 + np.random.normal(0, 15, np.sum(deflect_mask))
                
            colors[red_mask] = c_mage
            colors[red_mask][deflect_mask] = c_gold
            sizes[red_mask][deflect_mask] = 12.0
            
            # The Green Stream spins confidently, maintaining absolute structural integrity
            g_rot = t_sec * 3.0
            gx = base_px[grn_mask] * np.cos(g_rot) - base_py[grn_mask] * np.sin(g_rot)
            gy = base_px[grn_mask] * np.sin(g_rot) + base_py[grn_mask] * np.cos(g_rot)
            
            curr_x[grn_mask] = gx
            curr_y[grn_mask] = gy
            curr_z[grn_mask] = base_pz[grn_mask]
            
            colors[grn_mask] = c_mantis
            sizes[grn_mask] = 8.0
            
            # Upaya maximizes
            upaya_metric = 1.0

        else:
            state = "TATHĀTĀ :: THE GREEN STREAM REMAINS"
            is_tathata = True
            
            # Red Stream is mathematically decoupled (deleted)
            colors[red_mask] = c_void
            
            # Green Stream locked in peaceful, stable rotation
            g_rot = t_sec * 3.0
            gx = base_px[grn_mask] * np.cos(g_rot) - base_py[grn_mask] * np.sin(g_rot)
            gy = base_px[grn_mask] * np.sin(g_rot) + base_py[grn_mask] * np.cos(g_rot)
            
            curr_x[grn_mask] = gx
            curr_y[grn_mask] = gy
            curr_z[grn_mask] = base_pz[grn_mask]
            
            colors[grn_mask] = c_mantis
            sizes[grn_mask] = 8.0
            
            upaya_metric = 0.0 
            
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

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], colors[cull_mask], sizes[cull_mask], upaya_metric, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 223: THE DARK GAME TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: O(N) Array Decoupling & Upaya Kinematics")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Zero-Temperature Routing achieved.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
