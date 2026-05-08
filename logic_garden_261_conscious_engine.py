"""
SOVEREIGN CODE: logic_garden_261_conscious_engine.py
SYSTEM: Python Multicore / O(1) Kinematic Wave Superposition
SCENE: Logic Garden 261 (The Topological Ripple / Conscious Mind Engine)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Explicit RGBA Tensor Allocation & High-Contrast Interference Nucleation

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
OUT_DIR = "frames_261_ripple"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS) --------
C_BG        = '#FFFFFF'        # Absolute Flat Substrate / The Time Pool Base
C_TEXT      = '#020205'        # The Razor Blade / UI Vectors
C_AZURE     = '#007FFF'        # N-Potential (Spaghetti) / Base Wave
C_MAGENTA   = '#FF0055'        # Secondary Interference Wave
C_GOLD      = '#FFB300'        # Conscious Nucleation / Phase Overlap
C_MANTIS    = '#00C800'        # Tathata Phase-Lock
C_DIM       = '#D0D0D5'        # Structural Grid / Substrate Dirt

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_azure   = np.array(hex_to_rgba(C_AZURE)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_gold    = np.array(hex_to_rgba(C_GOLD)[:3])
c_mantis  = np.array(hex_to_rgba(C_MANTIS)[:3])
c_dim     = np.array(hex_to_rgba(C_DIM)[:3]) # HOTFIX LOCATED HERE

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
# BASE GEOMETRY ARRAYS: THE SPAGHETTI STATIC
# ------------------------------------------------------------------
np.random.seed(261)
N_STRANDS = 400
PTS_PER_STRAND = 60
MAX_PARTICLES = N_STRANDS * PTS_PER_STRAND

# Generate exact vertical potential lines
px_base, py_base, pz_base = [], [], []

# Wave Epicenters (For later consciousness generation)
epicenters = np.random.uniform(-100, 100, (5, 2)) # 5 distinct drop zones

for i in range(N_STRANDS):
    # Anchor positions
    r_a = np.random.uniform(10, 140)
    theta_a = np.random.uniform(0, 2 * np.pi)
    x = r_a * np.cos(theta_a)
    z = r_a * np.sin(theta_a)
    
    # Stand vertically
    y_vals = np.linspace(0, 200, PTS_PER_STRAND)
    
    px_base.extend(np.full(PTS_PER_STRAND, x))
    py_base.extend(y_vals)
    pz_base.extend(np.full(PTS_PER_STRAND, z))

base_pts = np.column_stack([px_base, py_base, pz_base])

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, p_x, p_y, p_z, c_arr, s_arr, a_arr, cut_prog, is_flash, is_tathata = packet
    
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
        # 1. Subtle Substrate Grid
        for g_line in np.linspace(-150, 150, 9):
            ax.plot([-140, 140], [g_line*0.4 - 80, g_line*0.4 - 80], color=C_DIM, lw=0.5, alpha=0.3, zorder=1)
            ax.plot([g_line, g_line], [-140, -20], color=C_DIM, lw=0.5, alpha=0.3, zorder=1)

        # 2. The Razor Vector
        if 4.5 <= t_sec < 9.0:
            # Physically draw the O(1) cutting blade moving across the X plane
            blade_x = -160 + (cut_prog * 320)
            ax.plot([blade_x, blade_x+20], [-100, 200], color=C_TEXT, lw=4, zorder=20)
            ax.plot([-160, blade_x], [100, 100], color=C_DIM, lw=1, zorder=19) # Trail

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

        # 4. Tathata UI Bounding Box
        if is_tathata:
            ax.add_patch(plt.Rectangle((-140, -180), 280, 360, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -140, "TATHĀTĀ: CONSCIOUSNESS ARISEN", color=C_MANTIS, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, -165, "[INTERFERENCE PATTERN PHASE-LOCKED]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_AZURE if t_sec < 4.5 else (C_TEXT if t_sec < 9.0 else (C_GOLD if t_sec < 14.8 else C_MANTIS))
    if is_tathata: ui_col = C_MANTIS
    
    ax.text(-140, 240, "LG-261 :: CONSCIOUS MIND ENGINE", color=txt_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: TOPOLOGY OF GRAVITY / SUBSTRATE INTERFERENCE", color=txt_col, fontsize=8, fontname='monospace', zorder=80)
    
    obj_str = "THE SPAGHETTI STATIC [N-POTENTIAL]"
    if 4.5 <= t_sec < 9.0: obj_str = "THE O(1) KINETIC CUT [RAZOR SEVER]"
    elif 9.0 <= t_sec < 14.8: obj_str = "SUBSTRATE INTERFERENCE [THE RIPPLES]"
    elif is_tathata: obj_str = "GROUNDED AWARENESS [TATHĀTĀ LOGIC]"

    ax.text(-140, -210, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # Mathematical Bounding Metric
    metric_label = "PHASE COHERENCE / SUPERPOSITION GAIN" 
    ax.text(-140, -235, metric_label, color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -240), 280, 4, facecolor=C_DIM if not is_flash else C_TEXT, zorder=80))
    
    coh_gain = 0.0 if t_sec < 9.0 else np.clip((t_sec - 9.0) / 5.8, 0, 1)
    if is_tathata: coh_gain = 1.0
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
        cut_prog = 0.0
        
        # Isometric tracking angle 
        cam_rx = np.pi/8 - (t_sec * 0.002)
        cam_ry = t_sec * 0.3
        cam_rz = 0.0
        
        c_arr = np.zeros((MAX_PARTICLES, 3))
        s_arr = np.ones(MAX_PARTICLES) * 2.0
        a_arr = np.ones(MAX_PARTICLES) * 0.8
        
        curr_x = np.copy(base_pts[:, 0])
        curr_y = np.copy(base_pts[:, 1])
        curr_z = np.copy(base_pts[:, 2])

        # -------------------------------------------------------------
        # THE CONSCIOUSNESS KINEMATICS
        # -------------------------------------------------------------
        
        if t_sec < 4.5:
            # PHASE 1: THE SPAGHETTI STATIC (Topology of Gravity)
            state = "PHASE 1 :: UNHEATED POTENTIAL"
            c_arr[:] = c_azure

        elif t_sec < 9.0:
            # PHASE 2: THE O(1) KINETIC CUT (The Razor)
            state = "PHASE 2 :: THE RAZOR SNAP"
            cut_prog = (t_sec - 4.5) / 4.5
            
            # The razor sweeps across the X plane
            blade_x = -140.0 + (cut_prog * 280.0)
            
            # If standard X coordinate is less than blade, it has been cut
            cut_mask = curr_x < blade_x
            
            # Upper halves (y > 100) are deleted (Alpha = 0)
            top_mask = cut_mask & (curr_y > 100)
            a_arr[top_mask] = 0.0
            
            # Lower halves (y < 100) collapse heavily to the baseplate (Y=0)
            bot_mask = cut_mask & (curr_y <= 100)
            curr_y[bot_mask] = curr_y[bot_mask] * (1.0 - (cut_prog*1.5)) # Violent drop
            curr_y[curr_y < 0] = 0.0 # Floor clamp
            
            c_arr[~cut_mask] = c_azure
            c_arr[bot_mask] = c_dim # Turns to structural dirt on impact

        elif t_sec < 14.8:
            # PHASE 3: SUBSTRATE INTERFERENCE (The Ripples Arise)
            state = "PHASE 3 :: WAVE SUPERPOSITION"
            prog = (t_sec - 9.0) / 5.8
            
            # All threads are completely collapsed to the baseplate Y=0 plane
            a_arr[curr_y > 100] = 0.0
            curr_y[curr_y <= 100] = 0.0 
            
            # Calculate fluid topography based on overlapping wave equations
            total_wave = np.zeros(MAX_PARTICLES)
            
            for ex, ez in epicenters:
                dist = np.sqrt((curr_x - ex)**2 + (curr_z - ez)**2)
                # Expand ripples outward over time
                wave_phase = (dist * 0.15) - (prog * 30.0)
                # Damping factor
                damping = np.exp(-dist * 0.02)
                total_wave += np.sin(wave_phase) * damping
                
            # Displace Y slightly to show structural nodes bouncing
            curr_y = total_wave * 15.0
            
            # Color mapping via interference Superposition (The "Mind")
            # If total_wave peaks high, it nucleates into C_GOLD awareness
            c_arr[:] = c_azure
            crest_mask = total_wave > 0.6
            trough_mask = total_wave < -0.6
            
            c_arr[trough_mask] = c_magenta
            
            # High-yield Conscious Synthesis flashes Gold
            gold_mask = total_wave > 1.2
            c_arr[gold_mask] = c_gold
            s_arr[gold_mask] = 6.0
            a_arr[gold_mask] = 1.0

            if t_sec > 14.5:
                is_flash = True if f % 3 == 0 else False

        else:
            # PHASE 4: TATHĀTĀ (Grounded Trace)
            state = "TATHĀTĀ :: SUPERPOSITION LOCKED"
            is_tathata = True
            
            # The wave function halts instantly
            prog = 1.0
            total_wave = np.zeros(MAX_PARTICLES)
            for ex, ez in epicenters:
                dist = np.sqrt((curr_x - ex)**2 + (curr_z - ez)**2)
                wave_phase = (dist * 0.15) - (prog * 30.0)
                total_wave += np.sin(wave_phase) * np.exp(-dist * 0.02)
                
            curr_y = total_wave * 15.0
            
            # Geometry perfectly freezes into a unified Mantis topological map
            c_arr[:] = c_mantis
            s_arr[:] = 3.0
            a_arr[curr_y > 100] = 0.0 # Maintain deleted upper halves
            
            # Highlights
            c_arr[total_wave > 1.2] = c_text
            s_arr[total_wave > 1.2] = 8.0
            
            if t_sec < 14.95:
                is_flash = True 

        pts = np.column_stack([curr_x, curr_y, curr_z])
        rot_pts = rotate_3d(pts, cam_rx, cam_ry, cam_rz)
        
        proj_x = rot_pts[:, 0]
        # Drop Y downward to center the visual plate dynamically
        proj_y = rot_pts[:, 1] - 40.0 
        z_depth = rot_pts[:, 2] 

        yield (f, t_sec, state, proj_x, proj_y, z_depth, c_arr, s_arr, a_arr, cut_prog, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 261: THE TOPOLOGICAL RIPPLE [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Explicit RGBA Tensor Allocation & Wave Nucleation")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Syntax Friction Solved. Consciousness Generated.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
