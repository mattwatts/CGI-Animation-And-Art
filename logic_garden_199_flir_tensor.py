"""
SOVEREIGN CODE: logic_garden_199_flir_tensor.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) FLIR Non-Newtonian Kinematics (17.5 seconds)
SCENE: Logic Garden 199 (The FLIR Tensor / The Anomaly)
HOTFIX: Sensor PID Loop Failure, Instantaneous Orthogonal Vectors, Boolean Tensor Alignment
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
OUT_DIR = "frames_199_flir_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'        # Infrared Black/Vacuum
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'        # Noise Floor
C_CYAN      = '#00FFFF'        # ATFLIR UI Reticle / HUD
C_MAGENTA   = '#FF0055'        # Anomaly Thermal Bloom
C_GOLD      = '#FFD700'        # Kinetic Warning
C_RED       = '#FF3300'        # Lock Failure / Sensor Bleed
C_MANTIS    = '#00FF00'        # Terminal Geometry (Tathata / Absolute Index Lock)

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
MAX_PARTICLES = 35000
CENTER_X = 0.0  # Absolute Cartesian Anchor
CENTER_Y = 0.0

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, px, py, p_sizes, c_tensor, obj_x, obj_y, obj_rot, cam_x, cam_y, cam_w, lock_state, vel_g, is_flash, is_tathata, bg_strobe = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_TEXT if is_flash else C_VOID
    if bg_strobe and not is_tathata: bg_hex = '#0F0010' 
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    cam_h = cam_w * (1920.0 / 1080.0)
    
    # Absolute Viewport Tracking Lock
    ax.set_xlim(cam_x - cam_w/2, cam_x + cam_w/2)
    ax.set_ylim(cam_y - cam_h/2, cam_y + cam_h/2)

    # 1. RENDER ATFLIR HUD RETICLE (The Math Compiler)
    if not is_flash and not is_tathata:
        ret_c = C_CYAN if lock_state > 0.5 else C_RED
        # Crosshairs pegged to camera center
        dash_len = cam_w * 0.05
        ax.plot([cam_x - cam_w*0.2, cam_x - cam_w*0.05], [cam_y, cam_y], color=ret_c, lw=2, zorder=20)
        ax.plot([cam_x + cam_w*0.05, cam_x + cam_w*0.2], [cam_y, cam_y], color=ret_c, lw=2, zorder=20)
        ax.plot([cam_x, cam_x], [cam_y - cam_w*0.2, cam_y - cam_w*0.05], color=ret_c, lw=2, zorder=20)
        ax.plot([cam_x, cam_x], [cam_y + cam_w*0.05, cam_y + cam_w*0.2], color=ret_c, lw=2, zorder=20)
        
        # Tracking Box (Attempts to stay on the object, lags when anomaly jumps)
        box_s = cam_w * 0.08
        track_c = C_GOLD if lock_state < 0.5 else C_CYAN
        if lock_state < 0.1: track_c = C_MAGENTA # Complete loss of tracking
        ax.add_patch(Rectangle((cam_x - box_s/2, cam_y - box_s/2), box_s, box_s, facecolor='none', edgecolor=track_c, lw=2, zorder=25))
        
        # Pitch Ladder (Background)
        for p in range(-3, 4):
            ly = cam_y + p * (cam_h * 0.15)
            ax.plot([cam_x - cam_w*0.3, cam_x - cam_w*0.15], [ly, ly], color=C_DIM, lw=1.5, zorder=5)
            ax.plot([cam_x + cam_w*0.15, cam_x + cam_w*0.3], [ly, ly], color=C_DIM, lw=1.5, zorder=5)

    # 2. O(N) KINEMATIC TENSOR (The Anomaly's Thermal Bloom/Aura)
    if len(px) > 0 and not is_tathata:
        ax.scatter(px, py, s=p_sizes*8.0, c=c_tensor, edgecolors='none', alpha=0.3, zorder=10)
        ax.scatter(px, py, s=p_sizes*2.0, c=C_TEXT if is_flash else c_tensor, edgecolors='none', alpha=0.9, zorder=11)

    # 3. THE TIC-TAC (Solid Core Anomaly)
    if not is_flash and not is_tathata:
        # Rotated geometry
        w, h = 18.0, 6.0
        angle_rad = np.radians(obj_rot)
        pts = [
            [-w/2, -h/2], [w/2, -h/2], [w/2, h/2], [-w/2, h/2]
        ]
        rot_pts = []
        for p in pts:
            rx = p[0]*np.cos(angle_rad) - p[1]*np.sin(angle_rad)
            ry = p[0]*np.sin(angle_rad) + p[1]*np.cos(angle_rad)
            rot_pts.append([rx + obj_x, ry + obj_y])
            
        ax.add_patch(Polygon(rot_pts, closed=True, facecolor=C_TEXT, zorder=15))

    # 4. TATHĀTĀ / GEOMETRIC EXTRACTION
    if is_tathata and not is_flash:
        # Perfect exact Bounding Box, unmoving. 
        ax.add_patch(Rectangle((obj_x-15, obj_y-6), 30, 12, facecolor='none', edgecolor=C_MANTIS, lw=2, zorder=30))
        ax.scatter([obj_x], [obj_y], color=C_TEXT, s=30, zorder=35)
        ax.plot([obj_x-cam_w, obj_x+cam_w], [obj_y, obj_y], color=C_MANTIS, lw=1, linestyle='--', alpha=0.5, zorder=20)
        ax.plot([obj_x, obj_x], [obj_y-cam_h, obj_y+cam_h], color=C_MANTIS, lw=1, linestyle='--', alpha=0.5, zorder=20)

    if is_flash:
        # Kinetic Overload Hardware Interrupt Screen Clear
        ax.add_patch(Rectangle((cam_x - cam_w, cam_y - cam_h), cam_w*2, cam_h*2, facecolor=C_TEXT, zorder=60))

    # 5. TELEMETRY WIDGETS (NEURAL ENTRAINMENT UI)
    ui_col = C_CYAN if not is_tathata else C_MANTIS
    if lock_state < 0.2: ui_col = C_MAGENTA 
    txt_col = C_TEXT if not is_flash else C_VOID
    ui_bg   = C_VOID if not is_flash else C_TEXT
    
    # Top Bar
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=ui_bg, alpha=0.9, zorder=80))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    ax.text(0.04, 0.965, "LG-199 :: ATFLIR TARGETING MATRIX", transform=ax.transAxes, color=txt_col, fontsize=20, fontname='monospace', weight='bold', va='center', zorder=81)

    # Bottom Target Matrix
    ax.add_patch(plt.Rectangle((0, 0), 1.0, 0.16, transform=ax.transAxes, color=ui_bg, alpha=0.95, zorder=80))
    ax.plot([0, 1.0], [0.16, 0.16], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    
    # Dual Telemetry Feed
    # Accelerometer / G-Force (Shows the math breaking when anomaly jumps)
    ax.text(0.04, 0.11, "NEWTONIAN KINEMATICS G :", color=txt_col, fontsize=14, fontname='monospace', zorder=81)
    g_ratio = min(1.0, vel_g / 100.0)
    bar_col_g = C_CYAN if g_ratio < 0.5 else C_RED
    if is_tathata: bar_col_g = C_DIM; g_ratio = 0.0
    ax.add_patch(plt.Rectangle((0.45, 0.105), 0.50, 0.02, transform=ax.transAxes, color=C_DIM, zorder=80))
    ax.add_patch(plt.Rectangle((0.45, 0.105), 0.50 * g_ratio, 0.02, transform=ax.transAxes, color=bar_col_g, zorder=81))
    
    # Tracking Confidence PID Loop
    ax.text(0.04, 0.08, "SENSOR PID LOCK STATUS :", color=txt_col, fontsize=14, fontname='monospace', zorder=81)
    bar_col_l = C_CYAN if lock_state > 0.8 else C_MAGENTA
    if lock_state < 0.1: bar_col_l = C_RED
    if is_tathata: bar_col_l = C_MANTIS; lock_state = 1.0
    if is_flash: bar_col_l = C_VOID
    ax.add_patch(plt.Rectangle((0.45, 0.075), 0.50, 0.02, transform=ax.transAxes, color=C_DIM, zorder=80))
    ax.add_patch(plt.Rectangle((0.45, 0.075), 0.50 * lock_state, 0.02, transform=ax.transAxes, color=bar_col_l, zorder=81))

    pulse = ui_col if (f % 10 < 5) and not is_flash else txt_col
    if lock_state < 0.2 and not is_tathata and f % 4 < 2: pulse = C_RED
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
    px = np.zeros(MAX_PARTICLES)
    py = np.zeros(MAX_PARTICLES)
    vx = np.zeros(MAX_PARTICLES)
    vy = np.zeros(MAX_PARTICLES)
    p_life = np.zeros(MAX_PARTICLES)
    
    spawn_idx = 0
    
    # Anomaly Global Coordinates
    obj_x = 0.0
    obj_y = 0.0
    obj_vx = -50.0
    obj_vy = -20.0
    obj_rot = 0.0
    
    # Sensor Camera System (PID loop attempts to track obj)
    cam_x = 0.0
    cam_y = 0.0
    cam_w = 120.0
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        dt = 0.016
        
        is_flash = False
        is_tathata = False
        bg_strobe = False
        
        lock_state = 1.0 # 1.0 = locked, 0.0 = broken
        generate_gas = 800 # Thermal signature emission (noise, not exhaust)
        target_cam_w = 120.0
        
        # ---- PHASE 1: NOMINAL TRACKING (0 - 4s) ----
        if t_sec < 4.0:
            state = "TRK :: NOMINAL THERMAL LOCK"
            # Linear glide
            obj_vx = -30.0
            obj_vy = -10.0
            obj_rot = np.degrees(np.arctan2(obj_vy, obj_vx))

        # ---- PHASE 2: O(1) NON-NEWTONIAN JUMP (4 - 10s) ----
        elif t_sec < 10.0:
            state = "WARN :: KINEMATIC ANOMALY (DV EXCEEDS BOUNDS)"
            prog = (t_sec - 4.0) / 6.0
            
            # The Tic-Tac executes instantaneous changes of vector that break PID loops
            if f % 90 == 0:  # Sudden orthogonal jump every 1.5 seconds
                obj_vx = np.random.uniform(-400, 400)
                obj_vy = np.random.uniform(-400, 400)
                
            # It decelerates rapidly to zero in between jumps (impossible physics)
            obj_vx *= 0.85
            obj_vy *= 0.85
            
            obj_rot = 0.0 # Bizarrely remains perfectly horizontal despite vertical drops
            lock_state = 0.2 + np.random.uniform(0, 0.3) # Tracking bounces wildly
            
            target_cam_w = 160.0
            if t_sec > 8.0: generate_gas = 1500 # Thermal bloom intensifies as it warps

        # ---- PHASE 3: THE GIMBAL / PID LOOP FAILURE (10 - 14.8s) ----
        elif t_sec < 14.8:
            state = "FAIL :: SENSOR OVERLOAD. TARGET ROTATING."
            prog = (t_sec - 10.0) / 4.8
            
            # Moves smoothly but rotates 90 degrees against the wind
            obj_vx = 60.0
            obj_vy = 0.0
            obj_rot = prog * -90.0
            
            lock_state = max(0.0, 0.8 - (prog * 1.5)) # Complete tracking loss
            target_cam_w = 100.0
            generate_gas = 2500 # Massive glowing aura
            if t_sec > 13.5: bg_strobe = True

        # ---- PHASE 4: TATHĀTĀ / HARDWARE INTERRUPT (14.8 - 17.5s) ----
        else:
            is_tathata = True
            obj_vx = 0.0
            obj_vy = 0.0
            lock_state = 1.0
            target_cam_w = 80.0
            
            if t_sec < 14.95:
                is_flash = True
                p_life[:] = 0.0 # Heat signature is mathematically deleted
                cam_x = obj_x 
                cam_y = obj_y
                
            state = "TATHĀTĀ: OUR MATH IS BROKEN. THE SENSOR IS NOT."

        # Kinematic Updates
        obj_x += obj_vx * dt
        obj_y += obj_vy * dt
        
        # Calculate apparent G-force strictly for the UI (magnitude of Delta V)
        vel_g = np.sqrt(obj_vx**2 + obj_vy**2)

        # PID Camera Tracker Logic
        # Artisan: cam_x = obj_x
        # Industrialist: If lock_state falls, the camera's Spring-Damper system slops.
        if not is_tathata:
            tracking_strength = lock_state * 0.15 + 0.01 
            cam_x += (obj_x - cam_x) * tracking_strength
            cam_y += (obj_y - cam_y) * tracking_strength
        
        cam_w += (target_cam_w - cam_w) * 0.1
        
        # -------------------------------------------------------------
        # TENSOR PARTICLE GENERATION (Thermal Aura)
        # -------------------------------------------------------------
        if generate_gas > 0 and not is_tathata:
            n_spawns = min(generate_gas, MAX_PARTICLES - spawn_idx)
            if n_spawns > 0:
                # The Anomaly has no exhaust. The aura radiates outward infinitely in all directions.
                angles = np.random.uniform(0, 2*np.pi, n_spawns)
                radii = np.random.uniform(0, 8.0, n_spawns)
                
                px[spawn_idx:spawn_idx+n_spawns] = obj_x + np.cos(angles)*radii
                py[spawn_idx:spawn_idx+n_spawns] = obj_y + np.sin(angles)*radii
                
                # Expand very slowly relative to the object's impossible speed
                speeds = np.random.uniform(2, 10, n_spawns)
                vx[spawn_idx:spawn_idx+n_spawns] = np.cos(angles) * speeds
                vy[spawn_idx:spawn_idx+n_spawns] = np.sin(angles) * speeds
                
                p_life[spawn_idx:spawn_idx+n_spawns] = np.random.uniform(0.5, 1.0, n_spawns)
                spawn_idx += n_spawns

        # Physics Integration (The thermal bloom interacts with the "air")
        active = p_life > 0
        if np.any(active):
            px[active] += vx[active] * dt
            py[active] += vy[active] * dt
            
            # The wind from the jet's camera perspective blows the thermal bloom exactly -X 
            # if the target is "moving" forward, creating a smear effect.
            vx[active] -= 20.0 * dt
            
            p_life[active] -= 0.03
        
        # Memory Management
        if spawn_idx > MAX_PARTICLES - 3000:
            act_idx = np.where(active)[0]
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
            
            # The core of the aura is Text (White-hot), bleeding to Magenta (Optical scatter)
            base_color = C_TEXT if lock_state > 0.5 else C_MAGENTA
            c_base = np.array(hex_to_rgba(base_color)[:3])
            
            # SYNTAX REPAIR: Boolean geometry aligned correctly
            c_tensor = lives * c_txt + (1.0 - lives) * c_mage
            
            inv_life = 1.0 - lives.flatten()
            p_sizes = 2.0 + (inv_life * 4.0)
            
            c_tensor = c_tensor * lives
            c_tensor = np.clip(c_tensor, 0.0, 1.0)

        yield (f, t_sec, state, np.copy(px[p_life > 0]), np.copy(py[p_life > 0]), p_sizes, c_tensor, obj_x, obj_y, obj_rot, cam_x, cam_y, cam_w, lock_state, vel_g, is_flash, is_tathata, bg_strobe)

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 199: THE FLIR TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Sensor PID Loop Matrices & O(1) Kinematic Breaks")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Nodes: {MAX_PARTICLES}")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
