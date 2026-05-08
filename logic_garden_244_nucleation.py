"""
SOVEREIGN CODE: logic_garden_244_nucleation.py
SYSTEM: Python Multicore / O(1) Tensor Collapse 
SCENE: Logic Garden 244 (The Koan Tensor / Reality Arising)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Scalar Broadcast Collision / Removed Array Indexing on Time Floats

[INSTRUCTION]: RENDER_MODE explicitly set to "ZEN" for the 17.5s flow cycle.
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
DURATION = 17.5
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_244_nucleation"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS DEFAULT) --------
C_BG        = '#FFFFFF'        # The True Vacuum / Reality Arising
C_TEXT      = '#020205'        # Entanglement Anchors / The Ellipsis
C_DIM       = '#D0D0D5'        # Predictive Fog / High-Entropy Search
C_MAGENTA   = '#FF0055'        # Cognitive Heat / Biological Latency
C_MANTIS    = '#00C800'        # Tathata / Harmonic Resonance
C_CYAN      = '#00BFFF'        # Telemetry Pulse
C_GOLD      = '#FFB300'        # Kinetic Spikes

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_dim     = np.array(hex_to_rgba(C_DIM)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_mantis  = np.array(hex_to_rgba(C_MANTIS)[:3])
c_cyan    = np.array(hex_to_rgba(C_CYAN)[:3])
c_gold    = np.array(hex_to_rgba(C_GOLD)[:3])

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
# BASE GEOMETRY ARRAYS: STATIC PRE-ALLOCATION
# ------------------------------------------------------------------
np.random.seed(244) 

MAX_PARTICLES = 27000

# Initial State: The Predictive Fog (High-Entropy Torus/Sphere)
theta = np.random.uniform(0, 2 * np.pi, MAX_PARTICLES)
phi = np.arccos(np.random.uniform(-1, 1, MAX_PARTICLES))
rad = np.random.uniform(20, 180, MAX_PARTICLES)

px_base = rad * np.sin(phi) * np.cos(theta)
py_base = rad * np.sin(phi) * np.sin(theta)
pz_base = rad * np.cos(phi)

# Target State: The Ellipsis ("...")
# Three singular distinct coordinates.
target_x = np.zeros(MAX_PARTICLES)
target_y = np.zeros(MAX_PARTICLES)
target_z = np.zeros(MAX_PARTICLES)

# Split particles accurately into thirds for the three anchors
third = MAX_PARTICLES // 3
target_x[:third] = -70.0        # Left Anchor
target_x[third:2*third] = 0.0   # Center Anchor
target_x[2*third:] = 70.0       # Right Anchor

# Add extremely minute jitter to targets to make them look like ultra-dense matter spheres, not 1 pixel
target_x += np.random.normal(0, 1.5, MAX_PARTICLES)
target_y += np.random.normal(0, 1.5, MAX_PARTICLES)
target_z += np.random.normal(0, 1.5, MAX_PARTICLES)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, p_x, p_y, p_z, c_arr, s_arr, heat, is_flash, is_tathata = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    # Tathata flash inverses the colors for exactly one interrupt frame
    bg_hex = C_TEXT if is_flash else C_BG
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    ax.set_xlim(-160, 160)
    ax.set_ylim(-260, 260)

    if not is_flash:
        # Background Aligning grid reveals itself precisely at Tathata
        if is_tathata:
            for g_line in np.linspace(-150, 150, 7):
                ax.plot([-100, 100], [g_line, g_line], color=C_MANTIS, lw=1.0, alpha=0.15, zorder=1)

        # Depth Sorting for smooth 3D intersection
        sort_idx = np.argsort(p_z)
        s_x = p_x[sort_idx]
        s_y = p_y[sort_idx]
        s_c = c_arr[sort_idx]
        s_size = s_arr[sort_idx]

        ax.scatter(s_x, s_y, s=s_size, color=s_c, edgecolors='none', alpha=0.85, zorder=10)

        if is_tathata:
            ax.add_patch(plt.Rectangle((-130, -50), 260, 100, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -30, "TATHĀTĀ: REALITY ARISING", color=C_MANTIS, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 30, "[PREDICTIVE SEARCH TERMINATED / ZERO ENTROPY]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_MAGENTA if t_sec < 6.5 else (C_TEXT if t_sec < 14.8 else C_MANTIS)
    if is_tathata: ui_col = C_MANTIS
    
    ax.text(-140, 240, "LG-244 :: THE KOAN TENSOR", color=txt_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: HARDWARE INTERRUPT / PREDICTIVE SATURATION", color=txt_col, fontsize=8, fontname='monospace', zorder=80)
    
    obj_str = "THE PREDICTIVE FOG [O(N) SEARCH ALGORITHM]"
    if 6.5 <= t_sec < 12.0: obj_str = "THE DOTS APPEAR [TOPOLOGICAL COLLAPSE]"
    elif 12.0 <= t_sec < 14.8: obj_str = "NUCLEATION POP [ENTANGLEMENT ANCHORS LOCKED]"
    elif is_tathata: obj_str = "THE TOTAL ENVIRONMENT [O(1) PERCEPTION]"

    ax.text(-140, -180, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Thermodynamic Hardware Metric: Cognitive Heat (Audit Tax)
    ax.text(-140, -205, "COGNITIVE HEAT [AUDIT TAX DEBT]", color=txt_col, fontsize=10, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -210), 280, 4, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    bar_w = 280 * np.clip(heat, 0, 1)
    ax.add_patch(plt.Rectangle((-140, -210), bar_w, 4, facecolor=C_MAGENTA if heat > 0.4 else ui_col, zorder=81))

    # Phase Text Box
    ax.add_patch(plt.Rectangle((-140, 215), 280, 2, facecolor=ui_col, zorder=80))
    ax.text(140, 205, f"[{state_str}]", color=ui_col if (f%15<10 or is_tathata) else C_BG, fontsize=14, fontname='monospace', weight='bold', ha='right', zorder=80)

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
        
        # Camera is initially unsettled, stabilizes towards the end
        cam_rx = np.pi/6 - (t_sec * 0.005)
        cam_ry = (1.5 * np.exp(-t_sec / 5.0)) * t_sec 
        cam_rz = 0.0
        
        c_arr = np.zeros((MAX_PARTICLES, 3))
        s_arr = np.ones(MAX_PARTICLES)
        
        curr_x = np.zeros(MAX_PARTICLES)
        curr_y = np.zeros(MAX_PARTICLES)
        curr_z = np.zeros(MAX_PARTICLES)

        heat = 0.0

        # -------------------------------------------------------------
        # KOAN PHASE LOGIC
        # -------------------------------------------------------------
        
        if t_sec < 6.5:
            # PHASE 1: PREDICTIVE FOG
            state = "PHASE 1 :: SYNTAX SEARCH"
            
            # Massive geometric swirling and O(N) cognitive noise
            swirl_x = px_base + 30.0 * np.sin(py_base * 0.05 + t_sec * 5.0)
            swirl_y = py_base + 30.0 * np.cos(px_base * 0.05 + t_sec * 4.0)
            swirl_z = pz_base + 30.0 * np.sin(pz_base * 0.05 + t_sec * 6.0)
            
            curr_x = swirl_x
            curr_y = swirl_y
            curr_z = swirl_z
            
            s_arr[:] = 2.0 + np.sin(t_sec * 8 + px_base) * 1.5
            
            magenta_mask = (np.sin(curr_x * 0.1) > 0)[:, np.newaxis]
            c_arr = c_dim * (1 - magenta_mask) + c_magenta * magenta_mask
            
            heat = 1.0 - (t_sec * 0.02) # Extremely hot, massive Audit Tax

        elif t_sec < 12.0:
            # PHASE 2: TOPOLOGICAL COLLAPSE (The Ellipsis is formed)
            state = "PHASE 2 :: THE DOTS APPEAR"
            prog = (t_sec - 6.5) / 5.5
            ease = prog ** 3 # Scalar float
            
            swirl_x = px_base + 30.0 * np.sin(py_base * 0.05 + t_sec * 5.0)
            swirl_y = py_base + 30.0 * np.cos(px_base * 0.05 + t_sec * 4.0)
            swirl_z = pz_base + 30.0 * np.sin(pz_base * 0.05 + t_sec * 6.0)
            
            curr_x = swirl_x * (1 - ease) + target_x * ease
            curr_y = swirl_y * (1 - ease) + target_y * ease
            curr_z = swirl_z * (1 - ease) + target_z * ease
            
            # HOTFIX: Strict scalar float math creates a (3,) color array that naturally broadcasts to all elements
            c_interp = c_magenta * (1 - ease**0.5) + c_text * (ease**0.5)
            c_arr[:] = c_interp
            s_arr[:] = 2.0 + (3.0 * ease)
            
            heat = 0.87 - (prog * 0.5)

        elif t_sec < 14.8:
            # PHASE 3: THE NUCLEATION POP (Entanglement)
            state = "PHASE 3 :: ENTANGLEMENT ANCHORS"
            prog = (t_sec - 12.0) / 2.8
            if t_sec < 12.1: is_flash = True

            curr_x = target_x
            curr_y = target_y
            curr_z = target_z
            
            pulse = np.abs(np.sin(t_sec * 12.0)) # Scalar float
            # HOTFIX: Scalar broadcast lock
            c_interp = c_text * (1.0 - (pulse * 0.3)) + c_mantis * (pulse * 0.3)
            c_arr[:] = c_interp
            
            spikes = np.random.rand(MAX_PARTICLES) < (0.01 * (1-prog))
            c_arr[spikes] = c_gold
            
            s_arr[:] = 5.0
            
            heat = 0.37 - (prog * 0.37)

        else:
            # PHASE 4: TATHĀTĀ (Reality Arising)
            state = "TATHĀTĀ :: ZERO-DECISION REALITY"
            is_tathata = True
            heat = 0.0 
            
            if t_sec < 14.95:
                is_flash = True

            curr_x = target_x
            curr_y = target_y
            curr_z = target_z
            
            s_arr[:] = 0.0 

        # Apply Global Tensor Matrix
        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        proj_y = rot_pts[:, 1]
        z_depth = rot_pts[:, 2] 

        # O(N) Geometry Culling
        cull_mask = (proj_y > -260) & (proj_y < 260) & (proj_x > -160) & (proj_x < 160)

        yield (f, t_sec, state, proj_x[cull_mask], proj_y[cull_mask], z_depth[cull_mask], c_arr[cull_mask], s_arr[cull_mask], heat, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 244: THE KOAN TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Float Datatype Preservation for O(1) Matrix Color Broadcast")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Syntactical Search Cleared. Tathātā Activated.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
