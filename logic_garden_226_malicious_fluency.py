"""
SOVEREIGN CODE: logic_garden_226_malicious_fluency.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Behavioral Threat Diagnostics (17.5 seconds)
SCENE: Logic Garden 226 (Malicious Fluency / The Grifter Pathology)
HOTFIX: O(N) Absolute Array Flattening, Dimensional Threat Clamping
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
OUT_DIR = "frames_226_malicious_fluency"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'
C_CYAN      = '#00FFFF'        # The Jagged Edge / Bedrock Truth
C_MAGENTA   = '#FF0055'        # Malicious Fluency / The Smooth Graph
C_GOLD      = '#FFD700'        # Synthetic Jaggedness / Fake Friction
C_MANTIS    = '#00FF00'        # Sovereign Override / Bare-Metal Validation

# -------- STRUCTURAL TOPOLOGY (THE HOTFIX) --------
MAX_PARTICLES = 25000
# Force absolute square root allocation to prevent Dimensional Compiler Crash
GRID_RES = int(np.ceil(np.sqrt(MAX_PARTICLES))) 

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
# BASE GEOMETRY ARRAYS: TRUTH VS EXPLOIT
# ------------------------------------------------------------------
np.random.seed(314)

gv = np.linspace(-140, 140, GRID_RES)
X, Y = np.meshgrid(gv, gv)

# Truncate vectors to map mathematically with MAX_PARTICLES
px_base = X.flatten()[:MAX_PARTICLES]
py_base = Y.flatten()[:MAX_PARTICLES]

# 1. The Bedrock Truth (The Axiom of Broken Glass)
# Unpredictable, high-friction, deeply fractured geometry
pz_bedrock = 25.0 * np.sin(px_base * 0.15) + 30.0 * np.cos(py_base * 0.1) + np.random.normal(0, 15, MAX_PARTICLES)

# 2. The Clever Lie (Malicious Fluency)
# A mathematically frictionless parabola built directly to supersede the bedrock
r_dist = np.sqrt(px_base**2 + py_base**2)
pz_lie = 80.0 - (r_dist**2) / 120.0  # Perfect thermodynamic smoothness

# Bounding Box for Override
validation_mask = (np.abs(px_base) < 60) & (np.abs(py_base) < 60)
dim_mask = ~validation_mask

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, proj_x, proj_y, z_depth, colors, sizes, glucose_drain, threat_metric, is_flash, is_tathata = packet
    
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

        ax.scatter(s_px, s_py, s=s_s, color=s_c, edgecolors='none', alpha=0.9, zorder=10)

        if is_tathata:
            # Sovereign Lockdown Firewall
            ax.add_patch(plt.Rectangle((-70, -70), 140, 150, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -90, "TATHĀTĀ: GRIFTER PAYLOAD PURGED", color=C_MANTIS, fontsize=11, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 100, "[BARE-METAL VALIDATION COMPLETED]", color=C_DIM, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    ui_col = C_CYAN if t_sec < 4.5 else (C_MAGENTA if t_sec < 9.5 else C_GOLD)
    if is_tathata: ui_col = C_MANTIS
    
    txt_col = C_TEXT if not is_flash else C_VOID

    ax.text(-140, 240, "LG-226 :: MALICIOUS FLUENCY", color=ui_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: BEHAVIORAL THREAT ARCHITECTURE", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    
    # Structural Integrity Tracker
    obj_str = "BEDROCK TRUTH [STRUCTURALLY SOUND]"
    if 4.5 <= t_sec < 9.5: obj_str = "EGO-VALIDATION [O(1) EXPLOIT ACTIVE]"
    elif 9.5 <= t_sec < 14.8: obj_str = "THE PUPPET THRESHOLD [SYNTHETIC NOISE]"
    elif is_tathata: obj_str = "SMOOTH GRAPH REJECTED [O(N) RESTORED]"

    ax.text(-140, -180, f"INTEGRITY METRIC : {obj_str}", color=ui_col, fontsize=11, fontname='monospace', weight='bold', zorder=80)
    
    # Vector 1: Glucose Drain (How 'easy' the deception feels to process)
    ax.text(-140, -205, "THERMODYNAMIC COST (GLUCOSE DRAIN)", color=txt_col, fontsize=10, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM, zorder=80))
    bar_w = 280 * np.clip(glucose_drain, 0, 1)
    # Drain is intentionally deceiving (Drops massively when the grifter lie is present)
    ax.add_patch(plt.Rectangle((-140, -210), bar_w, 4, facecolor=C_CYAN if t_sec < 4.5 else (C_MAGENTA if t_sec < 14.8 else C_MANTIS), zorder=81))

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
        
        cam_rx = -np.pi/4
        cam_ry = 0.0
        cam_rz = t_sec * 0.15
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 4.0
        
        curr_x = np.copy(px_base)
        curr_y = np.copy(py_base)
        curr_z = np.copy(pz_bedrock)

        glucose_drain = 1.0 # Baseline truth is expensive to process
        threat_metric = 0.0

        # -------------------------------------------------------------
        # PHASE LOGIC
        # -------------------------------------------------------------
        if t_sec < 4.5:
            state = "THE JAGGED EDGE :: O(N) FRICTION"
            
            # The matrix represents unadulterated reality
            # Computationally expensive, visually chaotic, but physically grounded
            curr_z += np.random.normal(0, 5, MAX_PARTICLES) * np.abs(np.sin(t_sec * 5))
            colors[:, :] = c_cyan
            # Add topological depth mapping
            colors[pz_bedrock < 0] = c_dim 
            
            sizes[:] = np.random.uniform(2, 6, MAX_PARTICLES)
            
            glucose_drain = 0.85 # High friction

        elif t_sec < 9.5:
            state = "MALICIOUS FLUENCY :: THE CLEVER LIE"
            prog = (t_sec - 4.5) / 5.0
            accel = prog ** 3 # Easing curve for deceptive smoothness
            
            # The Grifter completely overrides the complex truth with a flawless facade
            curr_z = pz_bedrock * (1.0 - accel) + pz_lie * accel
            
            colors[:, :] = c_cyan * (1.0 - accel) + c_mage * accel
            sizes[:] = 4.0 + (accel * 4.0)
            
            # The thermodynamic trap. The brain stops burning glucose because the lie feels "right"
            glucose_drain = 0.85 * (1.0 - prog) + 0.1 # Absolute false efficiency

        elif t_sec < 14.8:
            state = "SYNTHETIC JAGGEDNESS :: THE PUPPET THRESHOLD"
            prog = (t_sec - 9.5) / 5.3
            if t_sec < 9.6: is_flash = True
            
            # The smooth lie realizes it might be audited. It begins generating FAKE friction 
            # to mimic structural integrity.
            fake_noise = np.random.normal(0, 25.0, MAX_PARTICLES) * prog
            
            # Application of the noise is uniformly synthetic, completely lacking geological causality
            curr_z = pz_lie + fake_noise
            
            # Spallation artifacts
            noise_mask = np.abs(fake_noise) > 12.0
            colors[:, :] = c_mage
            colors[noise_mask] = c_gold
            sizes[noise_mask] = 10.0
            
            # The system feels a creeping unease, but glucose burn stays deceptively low
            glucose_drain = 0.1 + (0.2 * np.sin(t_sec * 12)) 

        else:
            state = "TATHĀTĀ :: BARE-METAL RESTORED"
            is_tathata = True
            
            # The Logic Auditor kills the parasitic process. The smooth dome and fake noise instantly vanish.
            # We are returned forcefully to the bedrock reality.
            curr_z = pz_bedrock
            
            colors[dim_mask] = c_dim
            sizes[dim_mask] = 2.0
            
            colors[validation_mask] = c_mantis
            sizes[validation_mask] = 8.0
            
            glucose_drain = 0.85 # The honest pain of truth computation returns.
            
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

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], colors[cull_mask], sizes[cull_mask], glucose_drain, threat_metric, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 226: MALICIOUS FLUENCY THREAT METRIC [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Deceptive Payload Visualization & Baseline Extraction")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Smooth Algorithm Terminated.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
