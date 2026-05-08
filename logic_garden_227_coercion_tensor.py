"""
SOVEREIGN CODE: logic_garden_227_coercion_tensor.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Behavioral Threat Analytics (17.5 seconds)
SCENE: Logic Garden 227 (Coercive Extraction / Unmasking the Beast)
HOTFIX: O(N) Spherical Vector Clamping, Load Inversion Physics applied
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
OUT_DIR = "frames_227_coercion_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'
C_CYAN      = '#00FFFF'        # The Target Node (Sovereign Baseline)
C_MAGENTA   = '#FF0055'        # The Beast (Hostile Red Stream Payload)
C_GOLD      = '#FFD700'        # The Glorious Form (Zero-Friction Illusion)
C_MANTIS    = '#00FF00'        # The Friction Test / Structural Containment

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
# BASE GEOMETRY ARRAYS: TARGET, PREDATOR, AND NETWORK
# ------------------------------------------------------------------
np.random.seed(616)

TAR_N = 5000
PRED_N = 12000
NET_N = 8000

# 1. Target Node (Inner Core)
tar_phi = np.arccos(1 - 2 * np.random.rand(TAR_N))
tar_th = np.random.uniform(0, 2 * np.pi, TAR_N)
tar_r = np.cbrt(np.random.rand(TAR_N)) * 25.0
px_tar = tar_r * np.sin(tar_phi) * np.cos(tar_th)
py_tar = tar_r * np.sin(tar_phi) * np.sin(tar_th)
pz_tar = tar_r * np.cos(tar_phi)

# 2. The Predator Shell (Perfectly wraps the target)
pred_phi = np.arccos(1 - 2 * np.random.rand(PRED_N))
pred_th = np.random.uniform(0, 2 * np.pi, PRED_N)
pred_r = 45.0  # Mathematically smooth shell radius
px_pred = pred_r * np.sin(pred_phi) * np.cos(pred_th)
py_pred = pred_r * np.sin(pred_phi) * np.sin(pred_th)
pz_pred = pred_r * np.cos(pred_phi)

# 3. Macro Network (Trusted friends/family/reality)
net_phi = np.arccos(1 - 2 * np.random.rand(NET_N))
net_th = np.random.uniform(0, 2 * np.pi, NET_N)
net_r = np.random.uniform(70.0, 140.0, NET_N)
px_net = net_r * np.sin(net_phi) * np.cos(net_th)
py_net = net_r * np.sin(net_phi) * np.sin(net_th)
pz_net = net_r * np.cos(net_phi)

base_px = np.concatenate([px_tar, px_pred, px_net])
base_py = np.concatenate([py_tar, py_pred, py_net])
base_pz = np.concatenate([pz_tar, pz_pred, pz_net])

tar_mask = np.arange(MAX_PARTICLES) < TAR_N
pred_mask = (np.arange(MAX_PARTICLES) >= TAR_N) & (np.arange(MAX_PARTICLES) < TAR_N + PRED_N)
net_mask = np.arange(MAX_PARTICLES) >= TAR_N + PRED_N

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, proj_x, proj_y, z_depth, colors, sizes, glucose_burn, is_flash, is_tathata = packet
    
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

        ax.scatter(s_px, s_py, s=s_s, color=s_c, edgecolors='none', alpha=0.9, zorder=10)

        if is_tathata:
            ax.add_patch(plt.Rectangle((-50, -50), 100, 100, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -70, "TATHĀTĀ: C2 AUTHORIZATION RECLAIMED", color=C_MANTIS, fontsize=10, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 70, "[SOVEREIGN PERIMETER ESTABLISHED]", color=C_DIM, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    ui_col = C_GOLD if t_sec < 9.0 else (C_MAGENTA if t_sec < 14.8 else C_MANTIS)
    txt_col = C_TEXT if not is_flash else C_VOID

    ax.text(-140, 240, "LG-227 :: COERCIVE EXTRACTION", color=ui_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: BEHAVIORAL EXPLOIT / LOAD INVERSION", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    
    obj_str = "THE GLORIOUS EXPLOIT [ZERO FRICTION ILLUSION]"
    if 4.0 <= t_sec < 9.0: obj_str = "MACRO-NETWORK SEVERANCE [ISOLATION VECTOR]"
    elif 9.0 <= t_sec < 13.0: obj_str = "THE LOAD INVERSION [PARASITIC TRANSFER]"
    elif 13.0 <= t_sec < 14.8: obj_str = "THE FRICTION TEST INJECTED"
    elif is_tathata: obj_str = "STRUCTURAL THREAT QUARANTINED"

    ax.text(-140, -180, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=11, fontname='monospace', weight='bold', zorder=80)
    
    # Target Node Metabolic Load Metric
    ax.text(-140, -205, "TARGET METABOLIC BURN (GLUCOSE DRAIN)", color=txt_col, fontsize=10, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM, zorder=80))
    bar_w = 280 * np.clip(glucose_burn, 0, 1)
    
    # Drain color reflects reality: Starts artificially low (cyan), then hits maximum (magenta) when inverted
    g_col = C_CYAN if t_sec < 4.0 else (C_GOLD if t_sec < 9.0 else C_MAGENTA)
    if is_tathata: g_col = C_MANTIS
    ax.add_patch(plt.Rectangle((-140, -210), bar_w, 4, facecolor=g_col, zorder=81))

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
        
        cam_rx = -np.pi/6
        cam_ry = t_sec * 0.2
        cam_rz = 0.0
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 4.0
        
        curr_x = np.copy(base_px)
        curr_y = np.copy(base_py)
        curr_z = np.copy(base_pz)

        glucose_burn = 0.05 

        # -------------------------------------------------------------
        # PHASE LOGIC
        # -------------------------------------------------------------
        if t_sec < 4.0:
            state = "FRICTIONLESS INFILTRATION :: THE FLUENCY TRAP"
            
            # Target is internally healthy
            colors[tar_mask] = c_cyan
            sizes[tar_mask] = 4.0 + 2.0 * np.sin(t_sec * 4)
            
            # Predator presents as perfectly smooth, validating shell (Glorious Form)
            curr_x[pred_mask] = px_pred
            curr_y[pred_mask] = py_pred
            curr_z[pred_mask] = pz_pred
            colors[pred_mask] = c_gold
            sizes[pred_mask] = 5.0
            
            # Network exists naturally
            colors[net_mask] = c_cyan
            sizes[net_mask] = 2.0
            
            glucose_burn = 0.05 # Artificial zero. Dangerously low friction.

        elif t_sec < 9.0:
            state = "NETWORK SEVERANCE :: STRUCTURAL ISOLATION"
            prog = (t_sec - 4.0) / 5.0
            accel = prog ** 2
            
            colors[tar_mask] = c_cyan
            sizes[tar_mask] = 4.0
            
            colors[pred_mask] = c_gold
            sizes[pred_mask] = 5.0
            
            # The predator actively distances the target from the network
            curr_x[net_mask] = px_net * (1.0 + accel * 1.5)
            curr_y[net_mask] = py_net * (1.0 + accel * 1.5)
            curr_z[net_mask] = pz_net * (1.0 + accel * 1.5)
            
            # The network dims into the void
            colors[net_mask] = c_cyan * (1.0 - accel) + c_dim * accel
            sizes[net_mask] = 2.0 * (1.0 - accel)
            
            glucose_burn = 0.1 + (accel * 0.2) # A slight rise as isolation occurs

        elif t_sec < 13.0:
            state = "THE LOAD INVERSION :: PARASITIC ATTACHMENT"
            prog = (t_sec - 9.0) / 4.0
            if t_sec < 9.1: is_flash = True
            
            # Network is gone
            curr_x[net_mask] *= 2.5
            curr_y[net_mask] *= 2.5
            curr_z[net_mask] *= 2.5
            colors[net_mask] = c_dim
            sizes[net_mask] = 0.0
            
            # The truth actuates. The "Glorious" shell violently corrupts into massive, jagged spikes
            # It collapses geometrically to crush the Target.
            spall_mag = 15.0 * np.abs(np.sin(t_sec * 12)) + (prog * 30.0)
            p_fuzz_x = np.random.normal(0, spall_mag, PRED_N)
            p_fuzz_y = np.random.normal(0, spall_mag, PRED_N)
            p_fuzz_z = np.random.normal(0, spall_mag, PRED_N)
            
            # Shell radius drastically shrinks, crushing inward
            crush_r = 45.0 * (1.0 - prog * 0.5)
            cpx = crush_r * np.sin(pred_phi) * np.cos(pred_th)
            cpy = crush_r * np.sin(pred_phi) * np.sin(pred_th)
            cpz = crush_r * np.cos(pred_phi)
            
            curr_x[pred_mask] = cpx + p_fuzz_x
            curr_y[pred_mask] = cpy + p_fuzz_y
            curr_z[pred_mask] = cpz + p_fuzz_z
            
            colors[pred_mask] = c_gold * (1.0 - prog) + c_mage * prog
            sizes[pred_mask] = 6.0 + (prog * 4.0)
            
            # Target node agitates, colors desaturate to represent exhaustion
            colors[tar_mask] = c_cyan * (1.0 - prog) + c_text * prog
            
            glucose_burn = 0.3 + (prog * 0.7) # Maximum metabolic burn. Target is supporting the predator.

        elif t_sec < 14.8:
            state = "THE FRICTION TEST :: INJECTING BOUNDARIES"
            prog = (t_sec - 13.0) / 1.8
            
            colors[net_mask] = c_dim
            sizes[net_mask] = 0.0
            
            # Target injects a heavily fortified MANTIS sphere ("No") outward
            deflect_r = 25.0 + (prog * 50.0)
            colors[tar_mask] = c_mantis
            sizes[tar_mask] = 6.0
            
            # Predator matrix cannot tolerate friction. It kinematically shatters outward rapidly.
            shatter = prog ** 3
            curr_x[pred_mask] += px_pred * shatter * 3.0
            curr_y[pred_mask] += py_pred * shatter * 3.0
            curr_z[pred_mask] += pz_pred * shatter * 3.0
            
            colors[pred_mask] = c_mage
            sizes[pred_mask] = 10.0 * (1.0 - prog) + 2.0
            
            glucose_burn = 1.0 - (prog * 0.5)

        else:
            state = "TATHĀTĀ :: SOVEREIGNTY RESTORED"
            is_tathata = True
            
            # The Hostile payload is deleted entirely
            colors[pred_mask] = c_void
            colors[net_mask] = c_void
            
            # Target node is perfectly aligned, clamped in the center
            curr_x[tar_mask] = px_tar
            curr_y[tar_mask] = py_tar
            curr_z[tar_mask] = pz_tar
            
            colors[tar_mask] = c_mantis
            sizes[tar_mask] = 8.0
            
            glucose_burn = 0.0 
            
            if t_sec < 14.95:
                is_flash = True

        # Apply Global Tensor Matrix
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1]
        z_depth = rot_pts[:, 2] 

        # O(N) Geometry Culling
        cull_mask = (proj_y > -260) & (proj_y < 260) & (proj_x > -160) & (proj_x < 160)

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], colors[cull_mask], sizes[cull_mask], glucose_burn, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 227: COERCIVE EXTRACTION TRAP [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Load Inversion Geometrics & Structural Friction")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Threat Model Objectively Quarantined.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
