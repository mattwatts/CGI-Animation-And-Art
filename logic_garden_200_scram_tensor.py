"""
SOVEREIGN CODE: logic_garden_200_scram_tensor.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Thermodynamic Dampening Tensor (17.5 seconds)
SCENE: Logic Garden 200 (The SCRAM Tensor / Hardware Dampener)
HOTFIX: Boolean Array Geometry Alignment, Absolute Bounding Cartesian Locks, O(N) Swarm Muting
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_200_scram_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'        # Core Vacuum
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'        # Dark Architecture
C_CYAN      = '#00FFFF'        # Thermal Coolant / Low Energy Neutrons
C_MAGENTA   = '#FF0055'        # High Energy Fission Spallation
C_GOLD      = '#FFD700'        # Core Containment Membrane
C_RED       = '#FF3300'        # Critical Prompt Alarm
C_IRON      = '#1A1A24'        # Control Rod Shell
C_MANTIS    = '#00FF00'        # Terminal Geometry (Tathata / Bounding Box)

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_void = np.array(hex_to_rgba(C_VOID)[:3])
c_cyan = np.array(hex_to_rgba(C_CYAN)[:3])
c_mage = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_gold = np.array(hex_to_rgba(C_GOLD)[:3])
c_mant = np.array(hex_to_rgba(C_MANTIS)[:3])
c_txt  = np.array(hex_to_rgba(C_TEXT)[:3])

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE KINEMATIC ARCHITECTURE
# ------------------------------------------------------------------
MAX_PARTICLES = 40000
CENTER_X = 0.0  # Absolute Cartesian Anchor
CENTER_Y = 0.0

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, px, py, p_sizes, c_tensor, cam_w, k_eff, rod_y, core_temp, is_flash, is_tathata, bg_strobe = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_TEXT if is_flash else C_VOID
    if bg_strobe and not is_tathata: bg_hex = '#0F0005' 
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    cam_h = cam_w * (1920.0 / 1080.0)
    
    # Absolute Viewport Tracking Lock
    ax.set_xlim(CENTER_X - cam_w/2, CENTER_X + cam_w/2)
    ax.set_ylim(CENTER_Y - cam_h/2, CENTER_Y + cam_h/2)

    # Core Boundaries
    core_w = 80.0
    core_h = 100.0

    # 1. RENDER CORE INFRASTRUCTURE
    if not is_flash:
        core_c = C_GOLD if core_temp < 0.8 else C_RED
        if is_tathata: core_c = C_MANTIS
        
        # Containment Vessel Bounding Box
        ax.add_patch(Rectangle((CENTER_X - core_w/2, CENTER_Y - core_h/2), core_w, core_h, facecolor='none', edgecolor=core_c, lw=3, zorder=20))
        
        # Draw Control Rods
        rod_x_positions = [-24, -8, 8, 24]
        rod_width = 8.0
        
        for rx in rod_x_positions:
            # The rod itself drops from the top of the core
            r_c = C_TEXT if not is_tathata else 'none'
            e_c = 'none' if not is_tathata else C_MANTIS
            ls = '-' if not is_tathata else '--'
            
            ax.add_patch(Rectangle((rx - rod_width/2, rod_y), rod_width, core_h/2 + 50 - rod_y, facecolor=r_c, edgecolor=e_c, lw=2, linestyle=ls, zorder=25))
            
            # Guide tubes
            if not is_tathata:
                ax.plot([rx - rod_width/2, rx - rod_width/2], [CENTER_Y - core_h/2, CENTER_Y + core_h/2], color=C_DIM, lw=1, zorder=5)
                ax.plot([rx + rod_width/2, rx + rod_width/2], [CENTER_Y - core_h/2, CENTER_Y + core_h/2], color=C_DIM, lw=1, zorder=5)

    # 2. O(N) KINEMATIC TENSOR (Neutron Swarm)
    if len(px) > 0 and not is_tathata:
        ax.scatter(px, py, s=p_sizes*6.0, c=c_tensor, edgecolors='none', alpha=0.4, zorder=10)
        ax.scatter(px, py, s=p_sizes*1.5, c=C_TEXT if is_flash else c_tensor, edgecolors='none', alpha=0.9, zorder=11)

    # 3. TATHĀTĀ / GEOMETRIC EXTRACTION
    if is_tathata and not is_flash:
        ax.text(CENTER_X, CENTER_Y, "RECURSION MUTED", color=C_DIM, fontsize=18, fontname='monospace', ha='center', weight='bold', zorder=30)
        # Bounding lock
        ax.add_patch(Rectangle((CENTER_X - core_w*0.6, CENTER_Y - core_h*0.6), core_w*1.2, core_h*1.2, facecolor='none', edgecolor=C_MANTIS, lw=1, linestyle='--', zorder=30))

    if is_flash:
        # Kinetic Overload Hardware Interrupt Screen Clear
        ax.add_patch(Rectangle((CENTER_X - cam_w, CENTER_Y - cam_h), cam_w*2, cam_h*2, facecolor=C_TEXT, zorder=60))

    # 4. TELEMETRY WIDGETS (NEURAL ENTRAINMENT UI)
    ui_col = C_CYAN if not is_tathata else C_MANTIS
    if core_temp > 0.8: ui_col = C_MAGENTA 
    if core_temp > 0.95 and f%8<4: ui_col = C_RED
    txt_col = C_TEXT if not is_flash else C_VOID
    ui_bg   = C_VOID if not is_flash else C_TEXT
    
    # Top Bar
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=ui_bg, alpha=0.9, zorder=80))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    ax.text(0.04, 0.965, "LG-200 :: REACTOR SCRAM DAMPENING TENSOR", transform=ax.transAxes, color=txt_col, fontsize=20, fontname='monospace', weight='bold', va='center', zorder=81)

    # Bottom Target Matrix
    ax.add_patch(plt.Rectangle((0, 0), 1.0, 0.16, transform=ax.transAxes, color=ui_bg, alpha=0.95, zorder=80))
    ax.plot([0, 1.0], [0.16, 0.16], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    
    # K-Effective Metric
    ax.text(0.04, 0.11, f"K-EFFECTIVE (k) : {k_eff:04.2f}", color=txt_col, fontsize=14, fontname='monospace', zorder=81)
    bar_k = C_CYAN if k_eff <= 1.0 else C_MAGENTA
    if k_eff > 1.2: bar_k = C_RED
    if is_tathata: bar_k = C_MANTIS
    k_ratio = np.clip(k_eff / 2.0, 0.0, 1.0)
    ax.add_patch(plt.Rectangle((0.45, 0.105), 0.50, 0.02, transform=ax.transAxes, color=C_DIM, zorder=80))
    ax.add_patch(plt.Rectangle((0.45, 0.105), 0.50 * k_ratio, 0.02, transform=ax.transAxes, color=bar_k, zorder=81))
    
    # Core Temp / Rod UI
    rod_ratio = np.clip((50.0 - rod_y) / 100.0, 0.0, 1.0)
    ax.text(0.04, 0.08, f"ROD INSERTION   : {rod_ratio*100:03.0f}%", color=txt_col, fontsize=14, fontname='monospace', zorder=81)
    bar_rod = C_CYAN if core_temp < 0.8 else C_RED
    if rod_ratio > 0.0: bar_rod = C_GOLD
    if is_tathata: bar_rod = C_MANTIS
    ax.add_patch(plt.Rectangle((0.45, 0.075), 0.50, 0.02, transform=ax.transAxes, color=C_DIM, zorder=80))
    ax.add_patch(plt.Rectangle((0.45, 0.075), 0.50 * rod_ratio, 0.02, transform=ax.transAxes, color=bar_rod, zorder=81))

    pulse = ui_col if (f % 10 < 5) and not is_flash else txt_col
    if is_flash: pulse = C_VOID

    ax.text(0.04, 0.03, f"[{state_str}]", transform=ax.transAxes, color=pulse, fontsize=20, fontname='monospace', weight='bold', zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) BALLISTIC KINEMATICS STREAM
# ------------------------------------------------------------------
def generate_stream():
    px = np.random.uniform(-38, 38, MAX_PARTICLES)
    py = np.random.uniform(-48, 48, MAX_PARTICLES)
    vx = np.zeros(MAX_PARTICLES)
    vy = np.zeros(MAX_PARTICLES)
    p_life = np.zeros(MAX_PARTICLES) 
    
    # Initialize nominal core
    spawn_idx = 0
    init_spawns = 2000
    p_life[:init_spawns] = 1.0
    vx[:init_spawns] = np.random.uniform(-20, 20, init_spawns)
    vy[:init_spawns] = np.random.uniform(-20, 20, init_spawns)
    spawn_idx = init_spawns
    
    cam_w = 120.0
    rod_x_positions = [-24, -8, 8, 24]
    rod_width = 8.0
    
    core_w = 80.0
    core_h = 100.0

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        dt = 0.016
        
        is_flash = False
        is_tathata = False
        bg_strobe = False
        
        target_cam_w = 120.0
        
        # State Arrays
        k_eff = 1.0
        rod_y = 60.0 # Fully withdrawn above core (Core max Y is 50)
        core_temp = 0.2
        
        # ---- PHASE 1: NOMINAL CRITICALITY (0 - 4s) ----
        if t_sec < 4.0:
            state = "NOMINAL :: CRITICALITY K=1.0"
            k_eff = 1.0 + np.random.uniform(-0.02, 0.02)
            core_temp = 0.2

        # ---- PHASE 2: PROMPT CRITICAL CASCADE (4 - 9s) ----
        elif t_sec < 9.0:
            state = "ALARM :: THERMODYNAMIC CASCADE DETECTED"
            prog = (t_sec - 4.0) / 5.0
            k_eff = 1.0 + (prog**2 * 0.8) # Rises to 1.8 (massively supercritical)
            core_temp = 0.2 + (prog * 0.8)
            target_cam_w = 140.0
            if core_temp > 0.8 and f % 6 < 3: bg_strobe = True

        # ---- PHASE 3: THE SCRAM (9 - 14.8s) ----
        elif t_sec < 14.8:
            state = "SCRAM INITIATED :: GRAVITY ROD DEPLOYMENT"
            prog = (t_sec - 9.0) / 5.8
            # Rod falls from +60 down to -50
            rod_y = max(-50.0, 60.0 - (prog * 300.0)) # Rapid drop
            
            # K-eff instantly collapses as rods insert
            k_eff = max(0.0, 1.8 - (prog * 4.0)) 
            core_temp = max(0.1, 1.0 - prog)
            
            target_cam_w = 160.0

        # ---- PHASE 4: TATHĀTĀ / HARDWARE INTERRUPT (14.8 - 17.5s) ----
        else:
            is_tathata = True
            k_eff = 0.0
            rod_y = -50.0
            core_temp = 0.0
            target_cam_w = 100.0
            
            if t_sec < 14.95:
                is_flash = True
                p_life[:] = 0.0 # Mathematically delete ALL entropy
                
            state = "TATHĀTĀ: GEOMETRY DICTATES ENERGY. SILENCE IS STRUCTURAL."

        cam_w += (target_cam_w - cam_w) * 0.1
        
        # -------------------------------------------------------------
        # TENSOR PARTICLE GENERATION (Neutron Multiplication)
        # -------------------------------------------------------------
        active_count = np.sum(p_life > 0)
        # Spawn new particles based on K-eff replication
        spawns_needed = int((active_count * k_eff * 0.05) + 10) # Base flux
        if is_tathata: spawns_needed = 0
            
        if spawns_needed > 0:
            n_spawns = min(spawns_needed, MAX_PARTICLES - spawn_idx)
            if n_spawns > 0:
                px[spawn_idx:spawn_idx+n_spawns] = np.random.uniform(-core_w/2 + 2, core_w/2 - 2, n_spawns)
                py[spawn_idx:spawn_idx+n_spawns] = np.random.uniform(-core_h/2 + 2, core_h/2 - 2, n_spawns)
                
                # Higher K-eff produces hotter, faster neutrons
                speed_base = 30.0 + (core_temp * 150.0)
                angles = np.random.uniform(0, 2*np.pi, n_spawns)
                speeds = np.random.uniform(speed_base*0.5, speed_base*1.5, n_spawns)
                
                vx[spawn_idx:spawn_idx+n_spawns] = np.cos(angles) * speeds
                vy[spawn_idx:spawn_idx+n_spawns] = np.sin(angles) * speeds
                
                p_life[spawn_idx:spawn_idx+n_spawns] = 1.0
                spawn_idx += n_spawns

        # Physics Integration (Bouncing inside the core Bounding Box)
        active = p_life > 0
        if np.any(active):
            px[active] += vx[active] * dt
            py[active] += vy[active] * dt
            
            # Wall Collisions
            mask_left = px < -core_w/2
            mask_right = px > core_w/2
            vx[mask_left] *= -1; px[mask_left] = -core_w/2
            vx[mask_right] *= -1; px[mask_right] = core_w/2
            
            mask_bottom = py < -core_h/2
            mask_top = py > core_h/2
            vy[mask_bottom] *= -1; py[mask_bottom] = -core_h/2
            vy[mask_top] *= -1; py[mask_top] = core_h/2
            
            # SCRAM ROD ANNIHILATION TENSOR
            # Find any particles intersecting the dropped control rods
            for rx in rod_x_positions:
                mask_rod_x = (px > rx - rod_width/2) & (px < rx + rod_width/2)
                mask_rod_y = (py < core_h/2) & (py > rod_y) # Rod falls from top down to rod_y
                intersect = mask_rod_x & mask_rod_y & active
                p_life[intersect] = 0.0 # Absolute neutron deletion

            # Natural thermal decay over time
            p_life[active] -= 0.02
        
        # Memory Management Defragmentation
        if spawn_idx > MAX_PARTICLES - 5000:
            act_idx = np.where(p_life > 0)[0]
            cnt = len(act_idx)
            px[:cnt] = px[act_idx]
            py[:cnt] = py[act_idx]
            vx[:cnt] = vx[act_idx]
            vy[:cnt] = vy[act_idx]
            p_life[:cnt] = p_life[act_idx]
            p_life[cnt:] = 0
            spawn_idx = cnt

        # Chromatic Mapping
        active_cnt = np.sum(p_life > 0)
        c_tensor = np.zeros((active_cnt, 3))
        p_sizes = np.zeros(active_cnt)
        
        if active_cnt > 0:
            lives = np.clip(p_life[p_life > 0][:, None], 0.0, 1.0)
            
            # Color maps based on absolute velocity
            v_mag = np.sqrt(vx[p_life > 0]**2 + vy[p_life > 0]**2)
            # Velocity normalization (30 is cold cyan, 150+ is hot magenta)
            heat_norm = np.clip((v_mag - 30.0) / 120.0, 0.0, 1.0)
            
            # SYNTAX REPAIR: Rigid Boolean Blend aligned precisely
            c_tensor = heat_norm[:, None] * c_mage + (1.0 - heat_norm[:, None]) * c_cyan
            
            p_sizes = 1.0 + (heat_norm * 3.0) 
            
            c_tensor = c_tensor * lives
            c_tensor = np.clip(c_tensor, 0.0, 1.0)

        yield (f, t_sec, state, np.copy(px[p_life > 0]), np.copy(py[p_life > 0]), p_sizes, c_tensor, cam_w, k_eff, rod_y, core_temp, is_flash, is_tathata, bg_strobe)

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 200: THE SCRAM TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Boolean Tensor Logic & Particle Annihilation Bounds")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Nodes: {MAX_PARTICLES}")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
