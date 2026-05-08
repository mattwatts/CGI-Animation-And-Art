"""
SOVEREIGN CODE: logic_garden_262_mhi_neuro.py
SYSTEM: Python Multicore / O(1) Industrial Thermodynamic Cycle
SCENE: Logic Garden 262 (MHI-NEURO-V3 / The Cast-Iron Turbine)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Explicit Torus-Knot Topology & Rigid State Synchronization

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
OUT_DIR = "frames_262_mhi_neuro"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS DEFAULT) --------
C_BG        = '#FFFFFF'        # Absolute Flat Substrate / Clean Room
C_TEXT      = '#020205'        # Cast-Iron Baseplate / Tension Tethers
C_AZURE     = '#007FFF'        # Variable Geometry Potential Fibers
C_MITSUBISHI= '#E60012'        # The Three Diamonds Resonance (Magenta/Red Core)
C_GOLD      = '#FFB300'        # Ceramic Aperture Heat / Thermal Exhaust
C_MANTIS    = '#00C800'        # Phase Coherence Governor Lock
C_DIM       = '#D0D0D5'        # Stealth Topography Grid

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_azure   = np.array(hex_to_rgba(C_AZURE)[:3])
c_mitsu   = np.array(hex_to_rgba(C_MITSUBISHI)[:3])
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
# BASE GEOMETRY ARRAYS: THE SUBSTRATE INTAKE
# ------------------------------------------------------------------
np.random.seed(262)
MAX_PARTICLES = 32000

# Generate a dense cylinder of vertical potential "spaghetti" fibers
r_cyl = np.random.uniform(5, 120, MAX_PARTICLES)
theta_cyl = np.random.uniform(0, 2*np.pi, MAX_PARTICLES)
height_cyl = np.random.uniform(-180, 180, MAX_PARTICLES)

px_base = r_cyl * np.cos(theta_cyl)
pz_base = r_cyl * np.sin(theta_cyl)
py_base = height_cyl

# Pre-calculate the Zero-Loss Torus Knot (Kaikyō Loop) mapping
# We map the particle's index to a position on a sweeping multi-dimensional torus
t_idx = np.linspace(0, 2*np.pi, MAX_PARTICLES)
t_p = 3  # Wraps
t_q = 8  # Inner loops
torus_r = 110 + 40 * np.cos(t_q * t_idx)
px_torus = torus_r * np.cos(t_p * t_idx)
pz_torus = torus_r * np.sin(t_p * t_idx)
py_torus = 160 * np.sin(t_q * t_idx)

# The "Three Diamonds" logic core (A secondary internal resonance array)
diamond_mask = r_cyl < 25.0

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, p_x, p_y, p_z, c_arr, s_arr, a_arr, core_spin, is_flash, is_tathata = packet
    
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
        # 1. Heavy Cast-Iron Precision Grid
        for g_line in np.linspace(-150, 150, 9):
            ax.plot([-140, 140], [g_line*0.4 - 100, g_line*0.4 - 100], color=C_DIM, lw=1.0, alpha=0.5, zorder=1)
            ax.plot([g_line, g_line], [-160, -40], color=C_DIM, lw=1.0, alpha=0.5, zorder=1)

        # 2. Structural Singularity Glow
        if core_spin > 0 and not is_tathata:
            ax.add_patch(plt.Circle((0, 0), core_spin * 100, color=C_MITSUBISHI, alpha=core_spin*0.2, zorder=2))
            ax.scatter(0, 0, s=200 * core_spin, color=C_TEXT, zorder=3)

        # 3. Particle Tensor Rendering
        active = a_arr > 0.01
        if np.any(active):
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

        # 4. Tathata UI Bounding Box (Governor Lock)
        if is_tathata:
            ax.add_patch(plt.Rectangle((-140, -180), 280, 360, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.add_patch(plt.Rectangle((-20, -20), 40, 40, facecolor='none', edgecolor=C_TEXT, lw=2, zorder=40))
            ax.text(0, -60, "TATHĀTĀ: UTILITY GOVERNOR LOCKED", color=C_MANTIS, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 75, "[ZERO-LOSS THERMODYNAMIC LOOP SECURED]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_AZURE if t_sec < 4.5 else (C_GOLD if t_sec < 9.0 else (C_MITSUBISHI if t_sec < 14.8 else C_MANTIS))
    if is_tathata: ui_col = C_MANTIS
    
    ax.text(-140, 240, "LG-262 :: MHI-NEURO-V3 ENGINE", color=txt_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: HEAVY-DUTY TURBINE / ZERO-LOSS RETURN", color=txt_col, fontsize=8, fontname='monospace', zorder=80)
    
    obj_str = "CAST-IRON INTAKE [POTENTIAL FIBERS]"
    if 4.5 <= t_sec < 9.0: obj_str = "DUAL-SCROLL SINGULARITY [COMPRESSION]"
    elif 9.0 <= t_sec < 14.8: obj_str = "THE KAIKYŌ LOOP [ZERO-LOSS TORUS]"
    elif is_tathata: obj_str = "MECHANICAL STILLNESS [PHASE COHERENCE]"

    ax.text(-140, -210, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Thermodynamic Hardware Metric: Thermal Spallation -> Coherence
    metric_label = "THERMAL SPALLATION / UTILITY HEAT" if t_sec < 14.8 else "ABSOLUTE GOVERNOR PHASE COHERENCE"
    ax.text(-140, -235, metric_label, color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -240), 280, 4, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    
    # Metric bar logic
    if t_sec < 9.0: coh_gain = np.clip((t_sec - 4.5) / 4.5, 0, 1) # Heat builds
    elif t_sec < 14.8: coh_gain = 1.0 # Max operating temp
    else: coh_gain = 1.0 # Lock

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
        core_spin = 0.0
        
        # Super-stable isometric mechanical angle 
        cam_rx = np.pi/6 - (t_sec * 0.002)
        cam_ry = t_sec * 0.5 # Fast mechanical rotational scan
        cam_rz = 0.0
        
        c_arr = np.zeros((MAX_PARTICLES, 3))
        s_arr = np.ones(MAX_PARTICLES) * 2.0
        a_arr = np.ones(MAX_PARTICLES) * 0.8
        
        curr_x = np.copy(px_base)
        curr_y = np.copy(py_base)
        curr_z = np.copy(pz_base)

        # -------------------------------------------------------------
        # THE MHI-NEURO-V3 KINEMATICS
        # -------------------------------------------------------------
        
        if t_sec < 4.5:
            # PHASE 1: THE CAST-IRON INTAKE
            state = "PHASE 1 :: HYDRAULIC MANIFOLD FEED"
            
            # Gentle mechanical pump sequence on Y
            curr_y += np.sin(t_sec * (126/60) * np.pi) * 8.0 
            
            c_arr[:] = c_azure
            c_arr[diamond_mask] = c_dim # Core lies dormant

        elif t_sec < 9.0:
            # PHASE 2: THE DUAL-SCROLL SINGULARITY
            state = "PHASE 2 :: O(1) CERAMIC APERTURE SUCK"
            prog = (t_sec - 4.5) / 4.5
            ease = prog ** 3 # Violent pneumatic crunch
            
            core_spin = prog
            
            # The razor zeroes the fibers directly into the center
            curr_x *= (1.0 - ease)
            curr_y *= (1.0 - ease)
            curr_z *= (1.0 - ease)
            
            # Flash heating
            c_arr[:] = c_azure * (1.0 - prog) + c_gold * prog
            c_arr[diamond_mask] = c_mitsu # Core ignites to Red

        elif t_sec < 14.8:
            # PHASE 3: THE KAIKYŌ LOOP (Zero-Loss Exhaust Return)
            state = "PHASE 3 :: ZERO-LOSS RELATIVISTIC RETURN"
            prog = (t_sec - 9.0) / 5.8
            ease = 1.0 - (1.0 - prog)**3
            
            core_spin = 1.0
            
            # Instead of firing straight out (vanishing), the stream is forced 
            # to map onto the Torus-Knot (The Carbon-Fiber Gravity Tethers)
            curr_x = px_base * (1.0 - ease) + px_torus * ease
            curr_y = py_base * (1.0 - ease) + py_torus * ease
            curr_z = pz_base * (1.0 - ease) + pz_torus * ease
            
            # The stream circulates along the torus based on frame time
            flow_spin = t_sec * 10.0
            flow_x = curr_x * np.cos(flow_spin) - curr_z * np.sin(flow_spin)
            flow_z = curr_x * np.sin(flow_spin) + curr_z * np.cos(flow_spin)
            curr_x, curr_z = flow_x, flow_z
            
            # Superheated thermal colors
            c_arr[:] = c_gold * (1.0 - prog) + c_mitsu * prog
            c_arr[diamond_mask] = c_bg # Core burns bright white
            s_arr[:] = 2.0 + (3.0 * prog)

            if t_sec > 14.5:
                is_flash = True if f % 2 == 0 else False

        else:
            # PHASE 4: TATHĀTĀ (Governor Lock)
            state = "TATHĀTĀ :: GOVERNOR THRESHOLD REACHED"
            is_tathata = True
            
            # Hardware Interrupt. The loop perfectly freezes into its geometric shape.
            curr_x = px_torus
            curr_y = py_torus
            curr_z = pz_torus
            
            # Lock the flow spin visually
            flow_spin = 14.8 * 10.0
            flow_x = curr_x * np.cos(flow_spin) - curr_z * np.sin(flow_spin)
            flow_z = curr_x * np.sin(flow_spin) + curr_z * np.cos(flow_spin)
            curr_x, curr_z = flow_x, flow_z
            
            # Complete Substrate Cooling (Absolute Phase Coherence)
            c_arr[:] = c_mantis
            s_arr[:] = 3.0
            a_arr[:] = 0.9
            
            # Maintain the deep core nodes
            c_arr[diamond_mask] = c_text
            s_arr[diamond_mask] = 6.0
            
            if t_sec < 14.95:
                is_flash = True 

        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        # Shift up dynamically to center the torus ring structure
        proj_y = rot_pts[:, 1] + 20.0
        z_depth = rot_pts[:, 2] 

        yield (f, t_sec, state, proj_x, proj_y, z_depth, c_arr, s_arr, a_arr, core_spin, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 262: THE MHI-NEURO-V3 [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Torus-Knot Thermodynamic Alignment & Governor Safety Hook")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Zero-Loss Loop Verified. Machine Coherence Locked.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
