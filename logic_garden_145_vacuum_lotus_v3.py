"""
SOVEREIGN CODE: logic_garden_144_vacuum_lotus_v3.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Dynamic Camera Matrix
SCENE: Logic Garden 144 (The Vacuum Lotus: Absolute Tracking)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
import os
import multiprocessing as mp
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 36                   # 36-Second High-Fidelity Cycle
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_144_lotus_v3"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-DIMENSIONAL CHROMATIC PALETTE --------
C_VOID = '#020205'
C_TEXT = '#FFFFFF'

# Stage 1: Thermal Friction (Atmosphere)
C_THERM_CORE = '#FFFFFF'
C_THERM_YELLOW = '#FFC107'
C_THERM_RED = '#FF003C'

# Stage 2: Geometric Flow (Vacuum Radiance)
C_VAC_CORE = '#E0FFFF'          # High-Energy Plasma White/Cyan
C_VAC_CYAN = '#00FFFF'          # Absolute Cyan
C_VAC_AZURE = '#0066FF'         # Deep Space Mid-body
C_VAC_MAGENTA = '#FF00AA'       # Cooling Edge
C_VAC_PURPLE = '#330088'        # Terminal Decay
C_VAC_PINK = '#FF66B2'

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# O(1) Vectorized Color Targets
A_THERM_CORE   = np.array(hex_to_rgba(C_THERM_CORE))
A_THERM_YELLOW = np.array(hex_to_rgba(C_THERM_YELLOW))
A_THERM_RED    = np.array(hex_to_rgba(C_THERM_RED))

A_VAC_CORE     = np.array(hex_to_rgba(C_VAC_CORE))
A_VAC_CYAN     = np.array(hex_to_rgba(C_VAC_CYAN))
A_VAC_AZURE    = np.array(hex_to_rgba(C_VAC_AZURE))
A_VAC_MAGENTA  = np.array(hex_to_rgba(C_VAC_MAGENTA))
A_VAC_PURPLE   = np.array(hex_to_rgba(C_VAC_PURPLE))

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (ISOLATED MEMORY NODE)
# ------------------------------------------------------------------
def render_frame(data_packet):
    f, t_sec, px, py, sizes, colors, pressure, sys_state, ui_color, flash_alpha, cam_dims = data_packet
    cam_cx, cam_cy, cam_W, cam_H = cam_dims
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    # -------------------------------------------------------------
    # CAMERA MATRIX APPLICATION (ABSOLUTE 9:16 FRAMING)
    # -------------------------------------------------------------
    ax.set_xlim(cam_cx - cam_W/2, cam_cx + cam_W/2)
    ax.set_ylim(cam_cy - cam_H/2, cam_cy + cam_H/2)

    # 1. Max-Q Staging Flash
    if flash_alpha > 0:
        ax.scatter(540.0, 1500.0, s=80000 * flash_alpha, c=C_VAC_CORE, alpha=flash_alpha * 0.9, edgecolors='none', zorder=10)
        ax.scatter(540.0, 1500.0, s=40000 * flash_alpha, c=C_VAC_MAGENTA, alpha=0.6 * flash_alpha, edgecolors='none', zorder=11)

    # 2. Render Node Dispersal
    if len(px) > 0:
        ax.scatter(px, py, s=sizes, c=colors, edgecolors='none', zorder=5)

    # 3. Rocket Hardware Constraint
    cone = plt.Polygon([[540, 1560], [520, 1500], [560, 1500]], color=C_TEXT, zorder=20)
    ax.add_patch(cone)
    ax.scatter(540.0, 1500.0, s=200, c=C_THERM_CORE, zorder=21)
    
    # -------------------------------------------------------------
    # UI DECOUPLING (ANCHORED TO SCREEN TRANSFORMS, NOT DATA OP)
    # -------------------------------------------------------------
    # Top Header
    ax.add_patch(plt.Rectangle((0, 0.96), 1, 0.04, transform=ax.transAxes, color=C_VOID, alpha=0.85))
    ax.plot([0, 1], [0.96, 0.96], transform=ax.transAxes, color=ui_color, lw=2)
    ax.text(0.04, 0.975, "LOGIC GARDEN 144 :: TWILIGHT PHENOMENON", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    # Bottom Telemetry Block
    ax.add_patch(plt.Rectangle((0, 0), 1, 0.10, transform=ax.transAxes, color=C_VOID, alpha=0.85))
    ax.plot([0, 1], [0.10, 0.10], transform=ax.transAxes, color=ui_color, lw=2)
    
    ax.text(0.04, 0.075, "STRUCTURAL SCHEMA : DYNAMIC DENDRITIC TRACKING", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    
    ax.text(0.04, 0.045, f"AMBIENT FRICTION : {pressure:>05.3f} ATM", transform=ax.transAxes, color=C_THERM_RED if pressure > 0.05 else C_TEXT, fontsize=20, fontname='monospace')
    ax.text(0.50, 0.045, f"RADIAL EXPANSION : {1.0-pressure:>05.3f} V", transform=ax.transAxes, color=C_VAC_CYAN if pressure < 0.05 else C_TEXT, fontsize=20, fontname='monospace')
    
    pulse = ui_color if (f % 20 < 10) else C_TEXT
    ax.text(0.04, 0.015, f"SYSTEM VECTOR    : {sys_state}", transform=ax.transAxes, color=pulse, fontsize=22, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf()
    plt.close(fig)
    plt.close('all')
    gc.collect() 
    return f

# ------------------------------------------------------------------
# THE PHYSICS ENGINE (O(1) GENERATOR BOUNDING LOGIC)
# ------------------------------------------------------------------
def generate_physics_stream():
    np.random.seed(31415)
    
    N_PARTICLES = 10000         
    LIFESPAN = 300              # Extended for massive screen coverage    
    E_RATE = 33                 # Normalized injection
    
    pos = np.zeros((N_PARTICLES, 2))
    vel = np.zeros((N_PARTICLES, 2))
    age = np.zeros(N_PARTICLES)
    active = np.zeros(N_PARTICLES, dtype=bool)
    
    N_BRANCHES = 36 # Denser fractal resolution
    branch_angles = np.linspace(-math.pi/2.05, math.pi/2.05, N_BRANCHES)
    cursor = 0
    nozzle_pos = np.array([540.0, 1500.0])
    
    # Camera Smoothing State
    cam_cx, cam_cy, cam_W, cam_H = 540.0, 960.0, 1080.0, 1920.0

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        pressure_curve = max(0.0, 1.0 - (t_sec / 11.0)**2) 
        
        sys_state = "STATE: ATMOSPHERIC COMPRESSION"
        ui_color = C_THERM_RED
        if 10.0 <= t_sec < 13.0:
            sys_state = "STATE: MAX-Q OVERRIDE (DECOHERENCE)"
            ui_color = C_THERM_YELLOW
        elif t_sec >= 13.0:
            sys_state = "STATE: UNCONSTRAINED DENDRITIC FLOW"
            ui_color = C_VAC_CYAN

        flash_alpha = 0.0
        if 11.5 <= t_sec < 12.5:
            flash_alpha = math.sin((t_sec - 11.5) * (math.pi / 1.0))

        # Vector Injection
        for _ in range(E_RATE):
            b_id = np.random.randint(0, N_BRANCHES)
            base_angle = branch_angles[b_id]
            
            radial_expansion = 0.15 + (0.85 * (1.0 - pressure_curve))
            sway = math.sin(t_sec * 2 + base_angle) * 0.10 * (1.0 - pressure_curve)
            active_angle = base_angle * radial_expansion + sway
            
            V_exit = np.random.uniform(9.0, 15.0) 
            v_x = V_exit * math.sin(active_angle) * radial_expansion
            v_y = -V_exit * math.cos(active_angle)
            
            pos[cursor] = nozzle_pos + np.array([np.random.uniform(-4, 4), np.random.uniform(-4, 0)])
            vel[cursor] = np.array([v_x, v_y])
            age[cursor] = 1
            active[cursor] = True
            cursor = (cursor + 1) % N_PARTICLES

        mask = active
        pos[mask] += vel[mask]
        age[mask] += 1
        
        if pressure_curve > 0.05:
            dist_from_nozzle = nozzle_pos[1] - pos[mask, 1]
            shock = np.sin(dist_from_nozzle / 30.0) * pressure_curve * 0.7
            vel[mask, 0] -= np.sign(vel[mask, 0]) * np.abs(shock)
            vel[mask, 1] *= (1.0 - 0.008 * pressure_curve) 
        else:
            vel[mask, 0] *= 0.993 # Slower drag, longer trails
            vel[mask, 1] -= 0.02

        active[age > LIFESPAN] = False
        mask = active
        
        # -------------------------------------------------------------
        # DYNAMIC CAMERA MATRIX (THE BOUNDING BOX ELIMINATOR)
        # -------------------------------------------------------------
        if np.sum(mask) > 0:
            min_x, max_x = np.min(pos[mask, 0]), np.max(pos[mask, 0])
            min_y, max_y = np.min(pos[mask, 1]), np.max(pos[mask, 1])
            
            # Ensure the nozzle is always within the bounding calculations
            min_x, max_x = min(min_x, 520.0), max(max_x, 560.0)
            min_y, max_y = min(min_y, 1500.0), max(max_y, 1560.0)
            
            cx, cy = (min_x + max_x) / 2.0, (min_y + max_y) / 2.0
            W_data, H_data = max_x - min_x, max_y - min_y
            
            # Apply exactly 5% mathematical padding (No excessive void)
            target_W = W_data * 1.05
            target_H = H_data * 1.05
            
            # Force 9:16 Aspect Ratio (1080 / 1920 = 0.5625)
            aspect = 1080.0 / 1920.0
            if target_W / max(target_H, 1) > aspect:
                target_H = target_W / aspect
            else:
                target_W = target_H * aspect
                
            # Baseline Constraint: Don't zoom in closer than native 1080p
            if t_sec < 11.0:
                target_W = max(1080.0, target_W)
                target_H = target_W / aspect
                target_cx, target_cy = 540.0, 960.0
            else:
                # Flow state tracking
                target_cx, target_cy = cx, cy
                
        # Apply Critical Damping to the Camera movement
        cam_lerp = 0.05
        if f == 0:
            cam_cx, cam_cy, cam_W, cam_H = target_cx, target_cy, target_W, target_H
        else:
            cam_cx += (target_cx - cam_cx) * cam_lerp
            cam_cy += (target_cy - cam_cy) * cam_lerp
            cam_W += (target_W - cam_W) * cam_lerp
            cam_H += (target_H - cam_H) * cam_lerp

        zoom_ratio = 1080.0 / cam_W

        # -------------------------------------------------------------
        # COLOR AND SCALE CALCULATION
        # -------------------------------------------------------------
        ages = age[mask] / LIFESPAN
        s_base = ages.shape[0]

        t_mid = np.clip(ages / 0.4, 0, 1)[:, np.newaxis]
        t_end = np.clip((ages - 0.4) / 0.6, 0, 1)[:, np.newaxis]
        color_therm = (1-t_mid)*A_THERM_CORE + t_mid*((1-t_end)*A_THERM_YELLOW + t_end*A_THERM_RED)

        v_1 = np.clip(ages / 0.2, 0, 1)[:, np.newaxis]
        v_2 = np.clip((ages - 0.2) / 0.4, 0, 1)[:, np.newaxis]
        v_3 = np.clip((ages - 0.6) / 0.4, 0, 1)[:, np.newaxis]
        
        c_vac_part1 = (1-v_1)*A_VAC_CORE + v_1*A_VAC_CYAN
        c_vac_part2 = (1-v_2)*A_VAC_CYAN + v_2*A_VAC_AZURE
        c_vac_part3 = (1-v_3)*A_VAC_MAGENTA + v_3*A_VAC_PURPLE
        
        color_vac = np.where(ages[:, np.newaxis] < 0.2, c_vac_part1, 
                    np.where(ages[:, np.newaxis] < 0.6, c_vac_part2, c_vac_part3))
        
        colors = (pressure_curve * color_therm) + ((1.0 - pressure_curve) * color_vac)
        
        core_mask = ages < 0.05
        colors[core_mask] = A_THERM_CORE
        
        alphas = 1.0 - np.power(ages, 1.2)
        colors[:, 3] = alphas * (0.95 if pressure_curve > 0.5 else 0.75)  # Richer opacity

        # Scale must increase correctly as camera zooms out to maintain visibility
        sizes_base = (30.0 * (1.0 - ages)) + (90.0 * ages * (1.0 - pressure_curve))
        # Prevent scaling into oblivion. Cap limits.
        sizes = sizes_base * (zoom_ratio ** 1.3)
        sizes = np.clip(sizes, 2.0, 120.0)

        yield (f, t_sec, pos[mask, 0].copy(), pos[mask, 1].copy(), sizes.copy(), colors.copy(), pressure_curve, sys_state, ui_color, flash_alpha, (cam_cx, cam_cy, cam_W, cam_H))

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 144: THE VACUUM LOTUS v3 [MULTICORE: {cpu_cores} THREADS]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=4):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
