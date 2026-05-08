"""
SOVEREIGN CODE: logic_garden_263_mbmm_gold.py
SYSTEM: Python Multicore / O(1) Zero-Latency Automation Loop
SCENE: Logic Garden 263 (MBMM GOLD / The Double View)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Explicit Torus Pathing & Micro-Friction Jitter Inject

[INSTRUCTION]: RENDER_MODE explicitly set to "ZEN" for the 18.0s flow cycle.
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
DURATION = 18.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_263_mbmm_gold"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS) --------
C_BG        = '#FFFFFF'        # Precision Leveled Hydraulic Floor
C_TEXT      = '#020205'        # The Jagged Grinder Core / Baseplate
C_CYAN      = '#00E5FF'        # The Double View (Borg Trace / Noise)
C_GOLD      = '#FFB300'        # MBMM Automated Recursion Matrix
C_MANTIS    = '#00C800'        # Logic Audit Phase-Lock
C_DIM       = '#D0D0D5'        # Stealth Topography Grid

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_cyan    = np.array(hex_to_rgba(C_CYAN)[:3])
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
# BASE GEOMETRY ARRAYS: THE SUBSTRATE
# ------------------------------------------------------------------
np.random.seed(263)
MAX_PARTICLES = 28000

# Torus Knot Parameters (Mitsubishi Kaikyō Loop)
t_idx = np.linspace(0, 2 * np.pi, MAX_PARTICLES)
t_p = 2  # Sweeps
t_q = 5  # internal winding
torus_r = 130 + 35 * np.cos(t_q * t_idx)

# Target Gold Loop Matrix
px_knot = torus_r * np.cos(t_p * t_idx)
pz_knot = torus_r * np.sin(t_p * t_idx)
py_knot = 140 * np.sin(t_q * t_idx)

# Initial Chaos Matrix (The Cyan Trace / Spaghetti)
px_base = px_knot + np.random.uniform(-100, 100, MAX_PARTICLES)
py_base = np.random.uniform(-200, 250, MAX_PARTICLES)
pz_base = pz_knot + np.random.uniform(-100, 100, MAX_PARTICLES)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, p_x, p_y, p_z, c_arr, s_arr, a_arr, flow_glow, is_flash, is_tathata = packet
    
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
        # 1. Mostly Flat Hydraulic Baseplate Curve
        for g_line in np.linspace(-150, 150, 9):
            curve = (1.0 - (np.abs(g_line)/150.0)**2) * 15.0 # Formal slight curve
            ax.plot([-140, 140], [g_line*0.4 - 100 - curve, g_line*0.4 - 100 - curve], color=C_DIM, lw=0.8, alpha=0.4, zorder=1)
            ax.plot([g_line, g_line], [-140, -40], color=C_DIM, lw=0.8, alpha=0.4, zorder=1)

        # 2. Fluid Dynamic Glow (Central Automation Shaft)
        if flow_glow > 0 and not is_tathata:
            ax.add_patch(plt.Circle((0, 0), flow_glow * 110, color=C_GOLD, alpha=flow_glow*0.25, zorder=2))

        # 3. Particle Tensor Rendering
        active = a_arr > 0.01
        if np.any(active):
            # Sort by Z-depth for correct pseudo-3D
            sort_idx = np.argsort(p_z[active])
            s_x = p_x[active][sort_idx]
            s_y = p_y[active][sort_idx]
            s_c = c_arr[active][sort_idx]
            s_size = s_arr[active][sort_idx]
            s_alpha = a_arr[active][sort_idx]

            rgba_colors = np.zeros((len(s_c), 4))
            rgba_colors[:, :3] = s_c
            rgba_colors[:, 3] = s_alpha
            ax.scatter(s_x, s_y, s=s_size, color=rgba_colors, edgecolors='none', zorder=10)

        # 4. Tathata UI (Logic Audit Guarantee)
        if is_tathata:
            ax.add_patch(plt.Rectangle((-140, -180), 280, 360, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -60, "TATHĀTĀ: LOGIC AUDIT GUARANTEED", color=C_MANTIS, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 75, "[SMOOTH MACRO GRAPH = JAGGED MICRO CORE]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_CYAN if t_sec < 4.5 else (C_GOLD if t_sec < 14.8 else C_TEXT)
    if is_tathata: ui_col = C_MANTIS
    
    ax.text(-140, 240, "LG-263 :: MBMM GOLD AUTOMATION", color=txt_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: MHI-NEURO BOOST/PRUNE / ZERO-LATENCY", color=txt_col, fontsize=8, fontname='monospace', zorder=80)
    
    obj_str = "THE DOUBLE VIEW [CYAN BORG TRACE]"
    if 4.5 <= t_sec < 9.0: obj_str = "FAUCET GOVERNOR [THERMAL COMPRESSION]"
    elif 9.0 <= t_sec < 14.8: obj_str = "FLUID KAIKYŌ LOOP [MBMM GOLD LIMIT]"
    elif is_tathata: obj_str = "THE JAGGED GRINDER [TRUE CORE REVEALED]"

    ax.text(-140, -210, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Thermodynamic Hardware Metric: Smoothness Illusion
    metric_label = "RECURSION EFFICIENCY" if t_sec < 14.8 else "O(1) BIOLOGICAL DIRECTIVE ALIGNMENT"
    ax.text(-140, -235, metric_label, color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -240), 280, 4, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    
    if t_sec < 4.5: coh_gain = 0.1
    elif t_sec < 9.0: coh_gain = 0.1 + 0.9 * ((t_sec - 4.5) / 4.5)
    else: coh_gain = 1.0

    val_w = 280 * coh_gain
    ax.add_patch(plt.Rectangle((-140, -240), val_w, 4, facecolor=ui_col, zorder=81))

    # Phase Text Box
    ax.add_patch(plt.Rectangle((-140, 195), 280, 2, facecolor=ui_col, zorder=80))
    ax.text(140, 185, f"[{state_str}]", color=ui_col if (f%15<10 or is_tathata) else C_BG, fontsize=14, fontname='monospace', weight='bold', ha='right', zorder=80)

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
        flow_glow = 0.0
        
        # Super-stable mechanical lock camera
        cam_rx = np.pi/8 - (np.sin(t_sec * 0.5) * 0.05)
        cam_ry = t_sec * 0.4
        cam_rz = 0.0
        
        c_arr = np.zeros((MAX_PARTICLES, 3))
        s_arr = np.ones(MAX_PARTICLES) * 2.5
        a_arr = np.ones(MAX_PARTICLES) * 0.8
        
        curr_x = np.copy(px_base)
        curr_y = np.copy(py_base)
        curr_z = np.copy(pz_base)

        # -------------------------------------------------------------
        # THE MBMM GOLD KINEMATICS
        # -------------------------------------------------------------
        
        if t_sec < 4.5:
            # PHASE 1: THE DOUBLE VIEW (Cyan vs Chaos)
            state = "PHASE 1 :: BORG TRACE OVERLAY"
            
            # Oscillating chaos
            curr_y += np.sin(t_sec * 5.0 + curr_x * 0.05) * 20.0
            
            c_arr[:] = c_cyan

        elif t_sec < 9.0:
            # PHASE 2: THE FAUCET GOVERNOR
            state = "PHASE 2 :: O(1) THERMAL COMPRESSION"
            prog = (t_sec - 4.5) / 4.5
            ease = prog ** 3 
            
            # Violent pull into the Gold Torus line
            curr_x = px_base * (1.0 - ease) + px_knot * ease
            curr_y = py_base * (1.0 - ease) + py_knot * ease
            curr_z = pz_base * (1.0 - ease) + pz_knot * ease
            
            c_arr[:] = c_cyan * (1.0 - ease) + c_gold * ease
            flow_glow = prog

        elif t_sec < 14.8:
            # PHASE 3: FLUID DYNAMIC CONTINUITY (The Smooth Lie)
            state = "PHASE 3 :: MBMM GOLD LOOP"
            prog = (t_sec - 9.0) / 5.8
            
            # Flow along the mathematical knot at ultra-relatasvistic speeds
            flow_mult = 12.0
            flow_idx = (t_idx + t_sec * flow_mult) % (2 * np.pi)
            
            dyn_r = 130 + 35 * np.cos(t_q * flow_idx)
            curr_x = dyn_r * np.cos(t_p * flow_idx)
            curr_y = 140 * np.sin(t_q * flow_idx)
            curr_z = dyn_r * np.sin(t_p * flow_idx)
            
            # **Friction-Inject:** The structure is overall smooth, but the micro-particles vibrate violently
            micro_jitter_x = np.random.normal(0, 5, MAX_PARTICLES)
            micro_jitter_y = np.random.normal(0, 5, MAX_PARTICLES)
            micro_jitter_z = np.random.normal(0, 5, MAX_PARTICLES)
            
            curr_x += micro_jitter_x
            curr_y += micro_jitter_y
            curr_z += micro_jitter_z
            
            c_arr[:] = c_gold
            a_arr[:] = 0.5 + 0.5 * np.sin(flow_idx * 10) # Shimmering Fluidity
            
            flow_glow = 1.0

            if t_sec > 14.5:
                is_flash = True if f % 2 == 0 else False

        else:
            # PHASE 4: TATHĀTĀ (The Jagged Grinder Core)
            state = "TATHĀTĀ :: JAGGED GRINDER REVEALED"
            is_tathata = True
            
            # Hardware Interrupt. Lock the flow path at the exact interrupt coordinate
            freeze_idx = (t_idx + 14.8 * 12.0) % (2 * np.pi)
            dyn_r = 130 + 35 * np.cos(t_q * freeze_idx)
            curr_x = dyn_r * np.cos(t_p * freeze_idx)
            curr_y = 140 * np.sin(t_q * freeze_idx)
            curr_z = dyn_r * np.sin(t_p * freeze_idx)
            
            # The "Smooth Gold" becomes highly transparent
            c_arr[:] = c_gold
            a_arr[:] = 0.15
            s_arr[:] = 2.0
            
            # The inner 20% of the nodes are stripped of the Gold Marine-Varnish 
            # and revealed as razor-sharp, hard-clipped C_TEXT Cast-Iron shards
            core_mask = t_idx < (np.pi * 0.4) 
            # We distribute these shards across the track to expose the gears
            gear_mask = np.random.rand(MAX_PARTICLES) > 0.8
            
            c_arr[gear_mask] = c_text
            s_arr[gear_mask] = 8.0 # Thick and aggressive
            a_arr[gear_mask] = 1.0
            
            # A subset lock to Mantis to prove Logic Audit 
            audit_mask = gear_mask & (np.random.rand(MAX_PARTICLES) > 0.9)
            c_arr[audit_mask] = c_mantis
            s_arr[audit_mask] = 10.0
            
            if t_sec < 14.95:
                is_flash = True 

        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        # Shift Y to dynamically center the Torus Knot
        proj_y = rot_pts[:, 1] + 20.0
        z_depth = rot_pts[:, 2] 

        yield (f, t_sec, state, proj_x, proj_y, z_depth, c_arr, s_arr, a_arr, flow_glow, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 263: MBMM GOLD AUTOMATION [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Torus Kinematics & Jagged Micro-Grinder Reveal")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Audit Tax Eliminated. Zero-Latency Locked.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
