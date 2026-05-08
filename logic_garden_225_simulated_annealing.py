"""
SOVEREIGN CODE: logic_garden_225_simulated_annealing.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Phase Space Traversal (17.5 seconds)
SCENE: Logic Garden 225 (Simulated Annealing / The River of Inference)
HOTFIX: Rasterized Topology Clamping, Absolute Value Thermal Locks
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
OUT_DIR = "frames_225_annealing_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'
C_CYAN      = '#00FFFF'        # Alpha-Decay / The River of Inference
C_MAGENTA   = '#FF0055'        # High Temperature / Exothermic Burst
C_GOLD      = '#FFD700'        # Thermal Spallation
C_MANTIS    = '#00FF00'        # Deep Freeze / Phase Coherence

MAX_PARTICLES = 22000

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
# BASE GEOMETRY ARRAYS: THE SEARCH TOPOLOGY
# ------------------------------------------------------------------
np.random.seed(888)

# Initial random distribution across the search space
px_base = np.random.uniform(-130, 130, MAX_PARTICLES)
py_base = np.random.uniform(-130, 130, MAX_PARTICLES)

def objective_topology(x, y):
    # A modified Rastrigin topology (Complex objective function with local minima)
    # The global optimum is at (0,0)
    basin = 0.005 * (x**2 + y**2)
    local_minima = 20.0 * np.cos(0.15 * x) + 20.0 * np.cos(0.15 * y)
    return basin + local_minima - 50.0

pz_target = objective_topology(px_base, py_base)
pz_burst = pz_target + np.random.uniform(50, 200, MAX_PARTICLES) # High thermal height

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, proj_x, proj_y, z_depth, colors, sizes, temp_metric, glucose_drain, is_flash, is_tathata = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_TEXT if is_flash else C_VOID
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    ax.set_xlim(-160, 160)
    ax.set_ylim(-280, 280)

    if not is_flash:
        # Topology Floor Wireframe (Dim context)
        grid_x, grid_y = np.meshgrid(np.linspace(-130, 130, 40), np.linspace(-130, 130, 40))
        grid_z = objective_topology(grid_x, grid_y)
        gf_pts = rotate_3d(np.column_stack([grid_x.flatten(), grid_y.flatten(), grid_z.flatten()]), np.pi/5, t_sec*0.15, 0)
        ax.scatter(gf_pts[:,0], gf_pts[:,1], s=0.5, color=c_dim, zorder=1)

        # O(N) Depth Sorting for Particles
        sort_idx = np.argsort(z_depth)
        s_px = proj_x[sort_idx]
        s_py = proj_y[sort_idx]
        s_c = colors[sort_idx]
        s_s = sizes[sort_idx]

        ax.scatter(s_px, s_py, s=s_s, color=s_c, edgecolors='none', alpha=0.85, zorder=10)

        if is_tathata:
            ax.add_patch(plt.Rectangle((-65, -80), 130, 160, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -100, "TATHĀTĀ: BIOLOGICAL OVERRIDE / RENDER ABORT", color=C_GOLD, fontsize=10, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 85, "[GLOBAL OPTIMUM TRAPPED. GLUCOSE LOCKED.]", color=C_MANTIS, fontsize=10, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    ui_col = C_MAGENTA if t_sec < 5.0 else (C_CYAN if t_sec < 11.0 else C_MANTIS)
    if is_tathata: ui_col = C_GOLD
    
    txt_col = C_TEXT if not is_flash else C_VOID

    ax.text(-145, 250, "LG-225 :: THE ANNEALING TENSOR", color=ui_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-145, 240, "SYSTEM: RIVER OF INFERENCE / OPTIMAL TRAVERSAL", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    
    phase_logic = "HIGH-T: ESCAPING LOCAL MINIMA"
    c_logic = C_MAGENTA
    if 5.0 <= t_sec < 11.0: 
        phase_logic = "ALPHA-DECAY: GRADIENT DESCENT VECTOR"
        c_logic = C_CYAN
    elif 11.0 <= t_sec < 14.8: 
        phase_logic = "DEEP FREEZE: PHASE COHERENCE LOCK"
        c_logic = C_MANTIS
    elif t_sec >= 14.8: 
        phase_logic = "THERMODYNAMIC TRAP: ACCEPTABLE THRESHOLD"
        c_logic = C_GOLD

    ax.text(-145, -200, f"KINEMATIC STATE : {phase_logic}", color=c_logic, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # 1. Thermal Machine Metric Vector
    ax.text(-145, -220, "SYSTEM TEMPERATURE [MACHINE VARIANCE]", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-145, -225), 290, 3, facecolor=C_DIM, zorder=80))
    bar_w = 290 * np.clip(temp_metric, 0, 1)
    ax.add_patch(plt.Rectangle((-145, -225), bar_w, 3, facecolor=ui_col if t_sec < 14.8 else C_MANTIS, zorder=81))

    # 2. Biological Core Metric (Friction-Inject)
    ax.text(-145, -240, "AUDIT TAX [BIOLOGICAL GLUCOSE BURN]", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-145, -245), 290, 3, facecolor=C_DIM, zorder=80))
    g_bar_w = 290 * np.clip(glucose_drain, 0, 1)
    ax.add_patch(plt.Rectangle((-145, -245), g_bar_w, 3, facecolor=C_GOLD if glucose_drain > 0.8 else C_MAGENTA, zorder=81))

    # Phase Text Box
    ax.add_patch(plt.Rectangle((-145, 225), 290, 2, facecolor=ui_col, zorder=80))
    ax.text(145, 215, f"[{state_str}]", color=ui_col if (f%15<10 or is_tathata) else C_VOID, fontsize=14, fontname='monospace', weight='bold', ha='right', zorder=80)

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
        
        cam_rx = np.pi/5
        cam_ry = t_sec * 0.15
        cam_rz = 0.0
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 4.0
        
        curr_x = np.copy(px_base)
        curr_y = np.copy(py_base)
        curr_z = np.copy(pz_target)
        
        temp_metric = 1.0
        glucose_drain = 0.1

        # -------------------------------------------------------------
        # PHASE LOGIC
        # -------------------------------------------------------------
        if t_sec < 5.0:
            state = "EXOTHERMIC BURST :: HIGH VARIANCE"
            
            # Massive thermal energy. Particles bounce chaotically high above the topology.
            # HOTFIX: Absolute Value Thermal Constraint
            thermal_energy = max(0.001, 80.0 * np.abs(np.cos(t_sec * 2)))
            
            curr_z = pz_burst + np.random.normal(0, thermal_energy, MAX_PARTICLES)
            curr_x += np.random.normal(0, thermal_energy * 0.5, MAX_PARTICLES)
            curr_y += np.random.normal(0, thermal_energy * 0.5, MAX_PARTICLES)
            
            colors[:, :] = c_mage
            sizes[:] = np.random.uniform(2, 6, MAX_PARTICLES)
            
            temp_metric = 1.0
            glucose_drain = 0.1 + (t_sec / 15.0) # Glucose burn begins

        elif t_sec < 11.0:
            state = "ALPHA DECAY :: THE RIVER OF INFERENCE"
            prog = (t_sec - 5.0) / 6.0
            if t_sec < 5.1: is_flash = True
            
            # Simulated Cooling: T decays logarithmically
            T = max(0.0001, np.exp(-3.0 * prog))
            
            # Gradient descent. They collapse into a flowing cyan river routing toward the center basin
            pull_force = prog * 0.8
            curr_x = px_base * (1.0 - pull_force) + np.random.normal(0, 15.0 * T, MAX_PARTICLES)
            curr_y = py_base * (1.0 - pull_force) + np.random.normal(0, 15.0 * T, MAX_PARTICLES)
            
            # Recalculate physical height onto the descending topology
            z_surf = objective_topology(curr_x, curr_y)
            # Fluid dropping dynamics
            curr_z = pz_burst * (1.0 - prog) + z_surf * prog + np.random.normal(0, 50.0 * T, MAX_PARTICLES)
            
            colors[:, :] = c_mage * (1.0 - prog) + c_cyan * prog
            sizes[:] = 4.0 + (prog * 2.0)
            
            temp_metric = T
            glucose_drain = 0.3 + (prog * 0.6) # The Audit Tax scales heavily as the system requires pruning

        elif t_sec < 14.8:
            state = "DEEP FREEZE :: BARE-METAL LOCK"
            prog = (t_sec - 11.0) / 3.8
            if t_sec < 11.1: is_flash = True
            
            T = 0.0 # Absolute Zero Friction
            
            # Fluid crystallizes geometrically into the absolute center basin (Global Optimum)
            target_x = curr_x * 0.05 
            target_y = curr_y * 0.05
            target_z = objective_topology(target_x, target_y)
            
            curr_x = curr_x * (1.0 - prog) + target_x * prog
            curr_y = curr_y * (1.0 - prog) + target_y * prog
            curr_z = curr_z * (1.0 - prog) + target_z * prog
            
            # Colors snap to MANTIS
            colors[:, :] = c_cyan * (1.0 - prog) + c_mantis * prog
            sizes[:] = 6.0 + (prog * 4.0)
            
            temp_metric = 0.0
            glucose_drain = 0.9 + (prog * 0.1) # Biological capacity is almost completely redlined

        else:
            state = "TATHĀTĀ :: ACCEPTABLE THRESHOLD ABORT"
            is_tathata = True
            
            # The system achieves an "Acceptable Threshold" and physically terminates the pursuit of perfection
            # The structure is locked exactly as it was. Zero further movement or recalculation.
            target_x = curr_x * 0.05 
            target_y = curr_y * 0.05
            curr_z = objective_topology(target_x, target_y)
            curr_x = target_x
            curr_y = target_y
            
            colors[:, :] = c_mantis
            sizes[:] = 10.0
            
            temp_metric = 0.0 
            glucose_drain = 1.0 # Biological battery terminal state. Operation successfully aborted to save the node.
            
            if t_sec < 14.95:
                is_flash = True

        # Apply Global Tensor Matrix
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1]
        z_depth = rot_pts[:, 2] 

        # O(N) Geometry Culling against Absolute Edges
        cull_mask = (proj_y > -280) & (proj_y < 280) & (proj_x > -160) & (proj_x < 160)

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], colors[cull_mask], sizes[cull_mask], temp_metric, glucose_drain, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 225: THE ANNEALING TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Mathematical Rasterization & Standard Deviation Clamp")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Zero-Temperature Auditing Achieved. Matrix Terminated.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
