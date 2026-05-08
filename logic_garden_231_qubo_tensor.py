"""
SOVEREIGN CODE: logic_garden_231_qubo_tensor.py
SYSTEM: Python Multicore / O(1) Schrödinger Kinematics
SCENE: Logic Garden 231 (Quantum QUBO Finite Engine / Automated Tunneling)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Wave-Function Destructive Interference / Rigid 15mK Thermal Clamping

[INSTRUCTION]: Set RENDER_MODE to "ZEN" for the 17.5s flow cycle. 
               Set RENDER_MODE to "STUDY" for the 45.0s detailed diagnostic.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
RENDER_MODE = "ZEN"  
if RENDER_MODE == "STUDY":
    DURATION = 45.0
    OUT_DIR = "frames_231_qubo_tensor_STUDY"
else:
    DURATION = 17.5
    OUT_DIR = "frames_231_qubo_tensor_ZEN"

FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE AZURE / MAKO PALETTE (HIGH-COHERENCE / WHITE BG) --------
C_BG        = '#FFFFFF'        # 15-milliKelvin Vacuum (Zero Entropy)
C_TEXT      = '#020205'        # High-Contrast Data Load
C_DIM       = '#D0D0D5'        # The QUBO Penalty Landscape
C_CYAN      = '#00FFFF'        # Transverse Anchor (Pure Superposition)
C_INDIGO    = '#4B0082'        # Quantum Tunneling (Probability Fluid)
C_MAGENTA   = '#FF0055'        # Thermal Decoherence / Entropy Threat
C_GOLD      = '#FFB300'        # Stray Photon / Environmental Friction
C_MANTIS    = '#00FF00'        # Eigenstate Collapse (Global Minimum Lock)

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_cyan    = np.array(hex_to_rgba(C_CYAN)[:3])
c_indigo  = np.array(hex_to_rgba(C_INDIGO)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_gold    = np.array(hex_to_rgba(C_GOLD)[:3])
c_mantis  = np.array(hex_to_rgba(C_MANTIS)[:3])
c_dim     = np.array(hex_to_rgba(C_DIM)[:3])

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
# BASE GEOMETRY: QUBO TOPOLOGY & QUANTUM WAVE-FUNCTION
# ------------------------------------------------------------------
np.random.seed(555)
T_RAT = DURATION / 17.5

# 1. The Problem Hamiltonian Landscape (N = 10,000)
GV = np.linspace(-120, 120, 100)
X, Y = np.meshgrid(GV, GV)
px_land = X.flatten()
py_land = Y.flatten()
# Complex topology with deep local minima and one absolute global minimum at (-50, -50)
pz_land = (px_land**2 + py_land**2)*0.003 + 20.0*np.cos(0.15*px_land) + 20.0*np.cos(0.15*py_land) 
target_well = -45.0 * np.exp(-((px_land + 50)**2 + (py_land + 50)**2) / 600.0)
pz_land += target_well

# 2. Transverse Superposition Cloud (N = 15,000 Qubits)
N_QUBITS = 15000
qx_base = np.random.uniform(-110, 110, N_QUBITS)
qy_base = np.random.uniform(-110, 110, N_QUBITS)
qz_base = np.random.uniform(50, 100, N_QUBITS) # Suspended far above the physical limit

base_px = np.concatenate([px_land, qx_base])
base_py = np.concatenate([py_land, qy_base])
base_pz = np.concatenate([pz_land, qz_base])
MAX_PARTICLES = len(base_px)

mask_land = np.arange(MAX_PARTICLES) < len(px_land)
mask_qubits = ~mask_land

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, proj_x, proj_y, z_depth, colors, sizes, thermal_iso, is_flash, is_tathata = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_TEXT if is_flash else C_BG
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    ax.set_xlim(-160, 160)
    ax.set_ylim(-260, 260)

    if not is_flash:
        # Entanglement Toroid Perimeter (Grid overlay)
        ax.add_patch(plt.Circle((0, 0), 160, facecolor='none', edgecolor=C_DIM, lw=1.5, alpha=0.2, zorder=1))

        # O(N) Depth Sorting
        sort_idx = np.argsort(z_depth)
        s_px = proj_x[sort_idx]
        s_py = proj_y[sort_idx]
        s_c = colors[sort_idx]
        s_s = sizes[sort_idx]

        ax.scatter(s_px, s_py, s=s_s, color=s_c, edgecolors='none', alpha=0.9, zorder=10)

        if is_tathata:
            ax.add_patch(plt.Rectangle((-100, -140), 60, 60, facecolor='none', edgecolor=C_MANTIS, lw=2, zorder=40))
            ax.text(0, -90, "TATHĀTĀ: EIGENSTATE COLLAPSE", color=C_MANTIS, fontsize=11, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 70, "[GLOBAL MINIMUM CLASSICALLY LOCKED]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_CYAN if t_sec < (4.0 * T_RAT) else (C_INDIGO if t_sec < (14.8 * T_RAT) else C_MANTIS)
    if is_tathata: ui_col = C_MANTIS
    
    ax.text(-140, 240, "LG-231 :: THE QUBO TENSOR", color=txt_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: QUANTUM ANNEALING & AMPLITUDE TUNNELING", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    
    obj_str = "FLOOR 1: TRANSVERSE ANCHOR [PURE SUPERPOSITION]"
    if (4.0 * T_RAT) <= t_sec < (8.0 * T_RAT): obj_str = "FLOOR 2: PROBLEM HAMILTONIAN [QUBO SCALING]"
    elif (8.0 * T_RAT) <= t_sec < (13.0 * T_RAT): obj_str = "FLOOR 3: QUANTUM TUNNELING [AUDIT TAX = 0.0]"
    elif (13.0 * T_RAT) <= t_sec < (14.8 * T_RAT): obj_str = "15-mK PERIMETER THREAT [DECOHERENCE CONTAINED]"
    elif is_tathata: obj_str = "FLOOR 4: EIGENSTATE TATHĀTĀ [SPIN-Z CLASSICAL]"

    ax.text(-140, -180, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Thermodynamic Isolation Metric
    ax.text(-140, -205, "THERMODYNAMIC ISOLATION [15-mK VACUUM]", color=txt_col, fontsize=10, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    bar_w = 280 * np.clip(thermal_iso, 0, 1)
    # Visual flag for heat leakage
    heat_col = C_MAGENTA if thermal_iso < 0.95 else ui_col
    ax.add_patch(plt.Rectangle((-140, -210), bar_w, 4, facecolor=heat_col, zorder=81))

    # Phase Text Box
    ax.add_patch(plt.Rectangle((-140, 215), 280, 20, facecolor=txt_col, zorder=80))
    ax.text(130, 222, f"[{state_str}]", color=C_BG if not is_flash else C_TEXT, fontsize=12, fontname='monospace', weight='bold', ha='right', zorder=81)

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
        cam_ry = t_sec * (0.2 / T_RAT)
        cam_rz = 0.0
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 4.0
        
        curr_x = np.copy(base_px)
        curr_y = np.copy(base_py)
        curr_z = np.copy(base_pz)

        thermal_iso = 1.0 # 15-mK absolute cold

        # QUBO Landscape is initially dormant
        if t_sec < (4.0 * T_RAT):
            land_alpha = 0.1
        else:
            prog_l = min(1.0, (t_sec - 4.0*T_RAT) / (2.0*T_RAT))
            land_alpha = 0.1 + (0.9 * prog_l)
            
        colors[mask_land] = c_bg * (1.0 - land_alpha) + c_dim * land_alpha
        sizes[mask_land] = 2.0 * land_alpha

        # -------------------------------------------------------------
        # QUANTUM ANNEALING SCHEDULER
        # -------------------------------------------------------------
        if t_sec < (4.0 * T_RAT):
            state = "PURE SUPERPOSITION"
            
            # Boundless infinite cloud
            curr_x[mask_qubits] += np.random.normal(0, 10, N_QUBITS) * np.abs(np.sin(t_sec * 5))
            curr_y[mask_qubits] += np.random.normal(0, 10, N_QUBITS) * np.abs(np.sin(t_sec * 5))
            
            colors[mask_qubits] = c_cyan
            sizes[mask_qubits] = 3.0 + np.random.rand(N_QUBITS)*4.0
            
        elif t_sec < (8.0 * T_RAT):
            state = "THE INTERFERENCE SCAFFOLD"
            prog = (t_sec - 4.0*T_RAT) / (4.0*T_RAT)
            
            # The cloud gently lowers toward the physical topology
            c_x = curr_x[mask_qubits]
            c_y = curr_y[mask_qubits]
            q_land = (c_x**2 + c_y**2)*0.003 + 20.0*np.cos(0.15*c_x) + 20.0*np.cos(0.15*c_y) - 45.0 * np.exp(-((c_x + 50)**2 + (c_y + 50)**2) / 600.0)
            
            target_z = q_land + 20.0 # Hovering just above the peaks
            curr_z[mask_qubits] = qz_base * (1.0 - prog) + target_z * prog
            
            colors[mask_qubits] = c_cyan * (1.0 - prog) + c_indigo * prog
            sizes[mask_qubits] = 5.0
            
        elif t_sec < (13.0 * T_RAT):
            state = "QUANTUM TUNNELING / THE AUTOMATED DEMON"
            prog = (t_sec - 8.0*T_RAT) / (5.0*T_RAT)
            if t_sec < (8.1 * T_RAT): is_flash = True
            
            # The Probability Wave converges toward (-50, -50). 
            # Crucially, it moves Horizontally THROUGH the z-height barriers, not over them.
            t_x = curr_x[mask_qubits]
            t_y = curr_y[mask_qubits]
            curr_x[mask_qubits] = t_x * (1.0 - prog*0.05) - 50.0 * (prog*1.5)
            curr_y[mask_qubits] = t_y * (1.0 - prog*0.05) - 50.0 * (prog*1.5)
            
            # Destructive interference: points not moving correctly are pruned to dust
            dist_to_well = np.sqrt((curr_x[mask_qubits] + 50)**2 + (curr_y[mask_qubits] + 50)**2)
            cull_prob = np.clip(1.0 - (100.0 / (dist_to_well + 1.0)), 0, 1)
            
            for i, p in enumerate(np.where(mask_qubits)[0]):
                if np.random.rand() < cull_prob[i] * prog:
                    colors[p] = c_bg # Erased mathematically
                    sizes[p] = 0.0
                else:
                    colors[p] = c_indigo
                    sizes[p] = 6.0
                    
        elif t_sec < (14.8 * T_RAT):
            state = "15-mK PERIMETER THREAT / DECOHERENCE WARNING"
            prog = (t_sec - 13.0*T_RAT) / (1.8*T_RAT)
            
            # Geometry continues to tunnel toward (-50,-50)
            curr_x[mask_qubits] = -50.0 + np.random.normal(0, 15.0 * (1.0 - prog), N_QUBITS)
            curr_y[mask_qubits] = -50.0 + np.random.normal(0, 15.0 * (1.0 - prog), N_QUBITS)
            
            # Thermal Threat Injection
            thermal_iso = 0.98 - (0.15 * np.abs(np.sin(t_sec * 20)))
            
            threat_p = np.random.rand(N_QUBITS) < (0.05 * np.abs(np.sin(t_sec * 20)))
            idx_threat = np.where(mask_qubits)[0][threat_p]
            colors[mask_qubits] = c_indigo
            colors[idx_threat] = c_magenta
            sizes[mask_qubits] = 8.0 
            sizes[idx_threat] = 15.0
            
        else:
            state = "TATHĀTĀ :: THE ADIABATIC COLLAPSE"
            is_tathata = True
            
            curr_x[mask_qubits] = -50.0 + np.random.normal(0, 4.0, N_QUBITS)
            curr_y[mask_qubits] = -50.0 + np.random.normal(0, 4.0, N_QUBITS)
            
            fin_x = curr_x[mask_qubits]; fin_y = curr_y[mask_qubits]
            curr_z[mask_qubits] = (fin_x**2 + fin_y**2)*0.003 + 20.0*np.cos(0.15*fin_x) + 20.0*np.cos(0.15*fin_y) - 45.0 * np.exp(-((fin_x + 50)**2 + (fin_y + 50)**2) / 600.0)
            
            colors[mask_qubits] = c_mantis
            sizes[mask_qubits] = 10.0
            
            thermal_iso = 1.0 # Bounding Box locked. Classical state achieved. 
            
            if t_sec < (14.95 * T_RAT):
                is_flash = True

        # Apply Global Tensor Matrix
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1]
        z_depth = rot_pts[:, 2] 

        # O(N) Geometry Culling
        cull_mask = (proj_y > -260) & (proj_y < 260) & (proj_x > -160) & (proj_x < 160)

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], colors[cull_mask], sizes[cull_mask], thermal_iso, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 231: THE QUBO TENSOR [MODE: {RENDER_MODE}] [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Schrödinger Kinematics & Eigenstate Collapse Limits")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Audit Tax deleted. Eigenstate Secured.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
