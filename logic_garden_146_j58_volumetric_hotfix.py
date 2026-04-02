"""
SOVEREIGN CODE: logic_garden_145_j58_volumetric_hotfix.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Volumetric Scalar Field Rendering
SCENE: Logic Garden 145 (J58 Afterburner: Photorealistic Reconstruction)
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
DURATION = 36                   
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_145_j58_volumetric"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE J58 PRATT & WHITNEY VOLUMETRIC PALETTE --------
C_VOID = '#020205'
C_TEXT = '#FFFFFF'

C_EDGE    = '#050015'      # Near-black void blend
C_VIOLET  = '#1a0033'      # Deep atmospheric shear boundary
C_INDIGO  = '#3a0ca3'      # Dense plasma body
C_AZURE   = '#4361ee'      # Supersonic core
C_CYAN    = '#4cc9f0'      # Shock diamond outer halo
C_WHITE   = '#ffffff'      # Absolute compression node

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

C_STOPS = np.array([0.0, 0.15, 0.35, 0.6, 0.85, 1.0])
C_RGBA = np.array([
    hex_to_rgba(C_EDGE),
    hex_to_rgba(C_VIOLET),
    hex_to_rgba(C_INDIGO),
    hex_to_rgba(C_AZURE),
    hex_to_rgba(C_CYAN),
    hex_to_rgba(C_WHITE)
])

def multi_lerp(values):
    idx = np.searchsorted(C_STOPS, values) - 1
    idx = np.clip(idx, 0, len(C_STOPS)-2)
    t = (values - C_STOPS[idx]) / (C_STOPS[idx+1] - C_STOPS[idx] + 1e-9)
    t = t[:, np.newaxis]
    return (1.0 - t) * C_RGBA[idx] + t * C_RGBA[idx+1]

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (VOLUMETRIC SPLATTING)
# ------------------------------------------------------------------
def render_frame(data_packet):
    f, t_sec, px, py, sizes, colors, throttle = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # 1. RENDER VOLUMETRIC FLUID
    if len(px) > 0:
        ax.scatter(px, py, s=sizes, c=colors, edgecolors='none', zorder=5)

    # 2. RENDER THE J58 HARDWARE (Afterburner Liner)
    nozzle_lip_y = 1750.0
    ax.add_patch(plt.Rectangle((540-150, nozzle_lip_y), 300, 200, color='#08080a', zorder=20))
    
    for ring_y in range(int(nozzle_lip_y), 1950, 25):
        ax.axhline(ring_y, xmin=0.36, xmax=0.64, color='#FF6600', alpha=0.3 * throttle, lw=2, zorder=21)
        ax.axhline(ring_y+5, xmin=0.36, xmax=0.64, color='#000000', alpha=0.8, lw=4, zorder=21)

    ax.add_patch(plt.Rectangle((540-155, nozzle_lip_y-5), 310, 10, color='#FFDD55', alpha=0.9, zorder=22))
    ax.add_patch(plt.Rectangle((540-155, nozzle_lip_y-5), 310, 10, color='#FFFFFF', alpha=0.6, zorder=23))

    # 3. UI DECOUPLING
    ax.add_patch(plt.Rectangle((0, 0.96), 1, 0.04, transform=ax.transAxes, color=C_VOID, alpha=0.9))
    ax.plot([0, 1], [0.96, 0.96], transform=ax.transAxes, color=C_AZURE, lw=2)
    ax.text(0.04, 0.975, "LOGIC GARDEN 145 :: PRATT & WHITNEY J58 RECONSTRUCTION", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    ax.add_patch(plt.Rectangle((0, 0), 1, 0.10, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 1], [0.10, 0.10], transform=ax.transAxes, color=C_AZURE, lw=2)
    ax.text(0.04, 0.075, "STRUCTURAL SCHEMA : VOLUMETRIC SCALAR FIELD (MACH DISKS)", transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace')
    
    dyn_p = throttle * 125.4
    ax.text(0.04, 0.045, f"AFTERBURNER PRESSURE : [{dyn_p:>06.1f} kPa]", transform=ax.transAxes, color=C_AZURE if throttle < 0.8 else '#FF6600', fontsize=18, fontname='monospace')
    
    ax.text(0.52, 0.045, f"RESOLVED COMPRESSION NODES : 8", transform=ax.transAxes, color=C_CYAN, fontsize=18, fontname='monospace')

    pulse = C_AZURE if (f % 20 < 10) else C_TEXT
    ax.text(0.04, 0.015, f"SYSTEM VECTOR        : SUPERSONIC PHOTOREALISTIC FLOW", transform=ax.transAxes, color=pulse, fontsize=22, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf()
    plt.close(fig)
    plt.close('all')
    gc.collect() 
    return f

# ------------------------------------------------------------------
# THE PHYSICS ENGINE (VOLUMETRIC SCALAR GENERATOR)
# ------------------------------------------------------------------
def generate_physics_stream():
    np.random.seed(42)
    
    N_PARTICLES = 60000         
    LIFESPAN = 140              
    
    pos = np.zeros((N_PARTICLES, 2))
    vel = np.zeros((N_PARTICLES, 2))
    age = np.zeros(N_PARTICLES)
    active = np.zeros(N_PARTICLES, dtype=bool)
    r_norm = np.zeros(N_PARTICLES)  
    
    nozzle_pos = np.array([540.0, 1750.0]) 
    nozzle_radius = 145.0
    cursor = 0
    k = (2.0 * math.pi) / 240.0 

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        throttle = 0.95 + 0.05 * math.sin(t_sec * 8.0)
        E_RATE = int((N_PARTICLES / LIFESPAN) * 1.0) 

        for _ in range(E_RATE):
            u = np.random.uniform(-1, 1)
            rn = np.sign(u) * (np.abs(u)**1.4)
            
            vx_init = np.random.uniform(-2, 2)
            vy_init = np.random.uniform(-20, -28) 
            
            pos[cursor] = nozzle_pos + np.array([rn * nozzle_radius, np.random.uniform(-8, 0)])
            vel[cursor] = np.array([vx_init, vy_init])
            r_norm[cursor] = rn
            age[cursor] = 1
            active[cursor] = True
            
            cursor = (cursor + 1) % N_PARTICLES

        mask = active
        px = pos[mask, 0]
        py = pos[mask, 1]
        
        vel[mask, 1] += 0.05  
        py += vel[mask, 1] 
        age[mask] += 1
        pos[mask, 1] = py
        
        d = nozzle_pos[1] - py 
        rn_live = r_norm[mask]
        
        theta = (k * d) + (0.0003 * d**2)
        W_d = nozzle_radius - 20.0 * (1.0 - np.exp(-0.0015 * d))
        
        target_x = nozzle_pos[0] + (rn_live * W_d)
        vel[mask, 0] = (target_x - px) * 0.6 
        pos[mask, 0] += vel[mask, 0]

        pulse = ((-np.cos(theta) + 1.0) / 2.0)**3.0 
        core_w = 0.15 + (0.45 * pulse)
        
        heat = np.exp(-(np.abs(rn_live) / core_w)**2.5) 
        heat *= np.exp(-0.0008 * d) 
        
        envelope = 0.3 * np.exp(-(np.abs(rn_live) / 0.9)**2) * np.exp(-0.0002 * d)
        total_heat = np.clip((heat + envelope) * throttle, 0, 1)
        colors = multi_lerp(total_heat)
        
        fuel_intensity = np.exp(-d / 200.0) * np.exp(-(np.abs(rn_live) / 0.25)**2.0)
        fuel_intensity = np.clip(fuel_intensity * throttle, 0.0, 1.0)
        
        colors[:, 0] = colors[:, 0] * (1-fuel_intensity) + 1.0 * fuel_intensity
        colors[:, 1] = colors[:, 1] * (1-fuel_intensity) + 0.6 * fuel_intensity
        colors[:, 2] = colors[:, 2] * (1-fuel_intensity) + 0.0 * fuel_intensity
        
        sizes = 120.0 + (100.0 * total_heat) + (d * 0.08)
        
        ages_live = age[mask] / LIFESPAN
        base_alpha = 0.02 + (0.05 * total_heat) 
        colors[:, 3] = np.clip(base_alpha * (1.0 - np.power(ages_live, 4.0)), 0.0, 1.0)

        # -------------------------------------------------------------
        # THE HOTFIX: EXTRACT PAYLOAD BEFORE MEMORY MUTATION
        # -------------------------------------------------------------
        px_pass = pos[mask, 0].copy()
        py_pass = pos[mask, 1].copy()

        # Execute culling AFTER the payload is packaged
        active[age > LIFESPAN] = False
        
        yield (f, t_sec, px_pass, py_pass, sizes.copy(), colors.copy(), throttle)

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER (BATCH EXECUTION)
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 145: J58 VOLUMETRIC [HOTFIX COMPILE] [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=4):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
