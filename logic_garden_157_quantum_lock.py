"""
SOVEREIGN CODE: logic_garden_157_quantum_lock.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Vector Physics Emulation (35 seconds)
SCENE: Logic Garden 157 (The Meissner Effect / Quantum Levitation)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing as mp
import os
import gc
import math

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 35                   
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_157_meissner"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_RED     = '#FF0033'          # Thermal Entropy / Room Temperature
C_GOLD    = '#FFD700'          # The Superconductor (Truth/Structure)
C_CYAN    = '#00FFFF'          # Magnetic Field Lattice / Extreme Cold
C_MANTIS  = '#00FF00'          # Terminal Green Flow / Quantum Lock
C_VAPOR   = '#AADDFF'          # Liquid Nitrogen Vapor

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# Compile-Time Safety: Superconductor Disk Nodes
np.random.seed(157)
NUM_DISK_NODES = 2500
# Generate a dense 3D cylinder
r_disk = np.random.uniform(0, 150, NUM_DISK_NODES)
theta_disk = np.random.uniform(0, 2*np.pi, NUM_DISK_NODES)
h_disk = np.random.uniform(-15, 15, NUM_DISK_NODES)

# Vapor Particles
NUM_VAPOR = 400
v_x = np.random.uniform(100, 980, NUM_VAPOR)
v_y = np.random.uniform(0, 1920, NUM_VAPOR)
v_speed = np.random.uniform(5, 15, NUM_VAPOR)

# Magnetic Field Grid lines (Avoid dead center 540 to force outward bend)
field_x_starts = np.array([x for x in np.linspace(150, 930, 15) if abs(x - 540) > 10])

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (ISOLATED MEMORY NODE)
# ------------------------------------------------------------------
def render_frame(data_packet):
    f, t_sec, state_str, ui_color, temp_k, deflect, disk_y, rot_angle, vapor_active = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # 1. VAPOR SUB-ROUTINE (LIQUID NITROGEN DRIFT)
    if vapor_active > 0.05:
        # Move vapor down
        curr_vy = (v_y - (f * v_speed * vapor_active)) % 1920
        # Gentle sine sway
        curr_vx = v_x + np.sin(curr_vy * 0.01 + f * 0.05) * 20
        ax.scatter(curr_vx, curr_vy, s=120, c=C_VAPOR, alpha=vapor_active * 0.15, zorder=1)
        ax.scatter(curr_vx, curr_vy, s=40, c=C_TEXT, alpha=vapor_active * 0.3, zorder=2)

    # 2. MAGNETIC FIELD LATTICE (THE BOUNDING BOX)
    y_lines = np.linspace(0, 1920, 100)
    for x0 in field_x_starts:
        dy = (y_lines - disk_y) * 2.5 # Compress Y influence (isometric view adjustment)
        dx = x0 - 540
        dist = np.sqrt(dx**2 + dy**2)
        
        # Gaussian outward pressure (Flux Expulsion)
        push = np.exp(-(dist**2) / 60000.0) * 180 * deflect
        direction = 1 if dx > 0 else -1
        x_draw = x0 + (direction * push)
        
        line_col = C_MANTIS if deflect > 0.95 else C_CYAN
        
        ax.plot(x_draw, y_lines, color=line_col, lw=8, alpha=0.2, zorder=3)
        ax.plot(x_draw, y_lines, color=C_TEXT, lw=1.5, alpha=0.6, zorder=4)

    # 3. SUPERCONDUCTOR MATRIX (THE PAYLOAD)
    # Rotate disk points
    d_x = r_disk * np.cos(theta_disk + rot_angle)
    d_z = r_disk * np.sin(theta_disk + rot_angle)
    
    # Isometric projection mapping
    proj_x = 540 + d_x
    proj_y = disk_y + (d_z * 0.3) + h_disk
    
    # Determine Phase Color based on Temperature
    if temp_k > 92:
        # Normal State (Red Entropy)
        disk_col = hex_to_rgba(C_RED)
        disk_glow = C_RED
    else:
        # Quantum Lock State (Gold Structure)
        disk_col = hex_to_rgba(C_GOLD)
        disk_glow = C_GOLD

    # Render disk
    # Add a glowing back-plate
    ax.scatter([540], [disk_y], s=80000, color=disk_glow, alpha=0.08 * deflect, zorder=5)
    ax.scatter(proj_x, proj_y, s=10, c=[disk_col]*NUM_DISK_NODES, marker='h', zorder=6)
    
    # Highlight the rim
    rim_mask = r_disk > 140
    ax.scatter(proj_x[rim_mask], proj_y[rim_mask], s=25, c=C_TEXT, alpha=0.5, zorder=7)

    # 4. TELEMETRY WIDGETS
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.9))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_color, lw=2)
    ax.text(0.04, 0.965, "LOGIC GARDEN 157 :: THE MEISSNER EFFECT", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    # Physics Panel
    ax.text(0.04, 0.88, f"CRITICAL TEMP (Tc): 092.0 K", transform=ax.transAxes, color=C_CYAN, fontsize=20, fontname='monospace')
    temp_col = C_RED if temp_k > 92 else C_MANTIS
    ax.text(0.04, 0.85, f"CURRENT CORE TEMP : {temp_k:>05.1f} K", transform=ax.transAxes, color=temp_col, fontsize=20, fontname='monospace')
    
    flux_status = "PENETRATING" if deflect < 0.5 else "EXPELLED (MEISSNER)"
    flux_col = C_RED if deflect < 0.5 else C_MANTIS
    ax.text(0.04, 0.81, f"MAGNETIC FLUX     : {flux_status}", transform=ax.transAxes, color=flux_col, fontsize=20, fontname='monospace')
    
    # Deep Math Equation Widget
    if deflect > 0.95:
        ax.text(0.04, 0.70, "B = μ_0 (H + M) = 0", transform=ax.transAxes, color=C_GOLD, fontsize=22, fontname='monospace')
        ax.text(0.04, 0.67, "PERFECT DIAMAGNETISM ACHIEVED", transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace')

    ax.add_patch(plt.Rectangle((0, 0), 0.95, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 0.95], [0.12, 0.12], transform=ax.transAxes, color=ui_color, lw=2)
    
    pulse = ui_color if (f % 60 < 30) or ui_color == C_MANTIS else C_TEXT
    ax.text(0.04, 0.08, "STRUCTURAL LOCK:", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=28, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf(); plt.close(fig); plt.close('all'); gc.collect() 
    return f

# ------------------------------------------------------------------
# PHYSICS ENGINE (THERMAL ENTROPY TO QUANTUM COHERENCE)
# ------------------------------------------------------------------
def generate_physics_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        # -----------------------------------------------------------
        # PHASE 1: THERMAL ENTROPY (0 - 8s)
        # -----------------------------------------------------------
        if t_sec < 8.0:
            state = "[01] THERMAL ENTROPY (NORMAL STATE)"
            ui_col = C_RED
            temp_k = 293.0 - (t_sec * 10) # 293K down to 213K
            deflect = 0.0
            disk_y = 600.0 # Resting on invisible theoretical plinth
            rot_angle = 0.0
            vapor_active = 0.0

        # -----------------------------------------------------------
        # PHASE 2: CRITICAL COOLING DECOHERENCE (8 - 18s)
        # -----------------------------------------------------------
        elif t_sec < 18.0:
            state = "[02] LIQUID NITROGEN (PHASE DECOHERENCE)"
            ui_col = C_CYAN
            phase_t = t_sec - 8.0
            progress = phase_t / 10.0
            
            # Massive temperature drop
            temp_k = 213.0 - (progress * 136.0) # Drops to 77K (Liquid Nitrogen)
            deflect = 0.0 # Flux still penetrates until Tc is crossed
            disk_y = 600.0 
            rot_angle = 0.0
            vapor_active = min(1.0, progress * 2.0)

        # -----------------------------------------------------------
        # PHASE 3: MEISSNER EXPULSION & LEVITATION (18 - 28s)
        # -----------------------------------------------------------
        elif t_sec < 28.0:
            state = "[03] FLUX EXPULSION (QUANTUM LOCK INITIATED)"
            ui_col = C_GOLD
            phase_t = t_sec - 18.0
            progress = phase_t / 10.0
            
            temp_k = 77.0 # Holds at 77K
            vapor_active = max(0.0, 1.0 - (progress * 1.5)) # Vapor clears
            
            # The exact moment of expulsion. Cubic ease-out.
            ease = 1.0 - math.pow(1.0 - progress, 3)
            deflect = ease 
            
            # Disk rises into the magnetic lattice (Flux Pinning)
            disk_y = 600.0 + (ease * 360.0) 
            
            # Gentle rotation begins as friction hits zero
            rot_angle = ease * phase_t * 0.1

        # -----------------------------------------------------------
        # PHASE 4: TATHĀTĀ / ZERO FRICTION (28 - 35s)
        # -----------------------------------------------------------
        else:
            state = "[04] TATHĀTĀ: ZERO FRICTION / ABSOLUTE FLOW"
            ui_col = C_MANTIS
            phase_t = t_sec - 28.0
            
            temp_k = 77.0
            vapor_active = 0.0
            deflect = 1.0
            disk_y = 960.0 + (math.sin(phase_t * 2.0) * 10.0) # Absolute perfect float
            
            rot_angle = (10.0 * 0.1) + (phase_t * 0.8) # Free spinning with 0 friction

        yield (f, t_sec, state, ui_col, temp_k, deflect, disk_y, rot_angle, vapor_active)

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 157: THE MEISSNER EFFECT [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
