"""
SOVEREIGN CODE: logic_garden_154_orbital_spar.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Vector Physics Emulation
SCENE: Logic Garden 154 (Atmospheric Spar - Orbital Buoyancy Optimization)
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
OUT_DIR = "frames_154_spar"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_RED     = '#FF0033'          # Gas Giant Entropy
C_GOLD    = '#FFD700'          # Gravity / Ballasting
C_CYAN    = '#00FFFF'          # The Spar Structure / Cold Void
C_MANTIS  = '#00FF00'          # Terminal Flow / Extraction
C_GAS     = '#FF4400'          # Deep Atmospheric Density

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (ISOLATED MEMORY NODE)
# ------------------------------------------------------------------
def render_frame(data_packet):
    f, t_sec, spar_y, tether_len, ballast_delta, state_str, ui_color, extract_stream = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # 1. THE GAS GIANT (ATMOSPHERIC BOUNDING BOX)
    # The deeper the Y, the denser the gas. We draw volumetric bands.
    band_y = np.linspace(0, 1200, 40)
    for y in band_y:
        density_alpha = min(0.9, (1200 - y) / 1500.0)
        ax.axhline(y, color=C_GAS, lw=15, alpha=density_alpha * 0.3, zorder=1)
        ax.axhline(y, color=C_RED, lw=2, alpha=density_alpha * 0.5, zorder=2)

    # 2. THE MEGA-STRUCTURE (ORBITAL SPAR)
    spar_x = 540
    spar_width = 180
    platform_top = spar_y + 200
    
    # Spar Main Hull (Cylinder)
    ax.plot([spar_x, spar_x], [spar_y, platform_top], color=C_CYAN, lw=spar_width, alpha=0.15, solid_capstyle='butt', zorder=5)
    ax.plot([spar_x - spar_width/2, spar_x - spar_width/2], [spar_y, platform_top], color=C_CYAN, lw=4, zorder=6)
    ax.plot([spar_x + spar_width/2, spar_x + spar_width/2], [spar_y, platform_top], color=C_CYAN, lw=4, zorder=6)

    # Habitat / Control Ring
    ax.plot([spar_x - 140, spar_x + 140], [platform_top, platform_top], color=C_TEXT, lw=12, zorder=7)
    ax.plot([spar_x - 140, spar_x + 140], [platform_top - 30, platform_top - 30], color=C_GOLD, lw=6, zorder=7)

    # 3. THE TETHER & EXTRACTION DYNAMICS
    tether_bottom = platform_top - tether_len
    # Main Drill / Tether Line
    ax.plot([spar_x, spar_x], [platform_top, tether_bottom], color=ui_color, lw=8, zorder=8)
    
    # Extraction Particles (Flowing UP the tether)
    if ui_color == C_MANTIS and len(extract_stream) > 0:
        ex_nodes_y = extract_stream
        ex_nodes_x = np.full_like(ex_nodes_y, spar_x)
        ax.scatter(ex_nodes_x, ex_nodes_y, s=120, c=C_MANTIS, marker='^', alpha=0.9, zorder=12)
        ax.scatter(ex_nodes_x, ex_nodes_y, s=300, c=C_MANTIS, alpha=0.2, zorder=11)

    # Energy Rings pulsing down the hull
    ring_y = spar_y + ( (f * 4) % 200 )
    ax.axhline(ring_y, xmin=0.4, xmax=0.6, color=ui_color, lw=6, alpha=0.8, zorder=9)

    # 4. TELEMETRY & CRITICAL DAMPING OVERLAY (NEON POP)
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.9))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_color, lw=2)
    ax.text(0.04, 0.965, "LOGIC GARDEN 154 :: ORBITAL SPAR MEGA-STRUCTURE", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    # Data Panel
    ax.text(0.04, 0.88, f"ORBITAL ALTITUDE : {spar_y:>06.1f} KM", transform=ax.transAxes, color=C_CYAN, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.85, f"TETHER EXTENSION : {tether_len:>06.1f} KM", transform=ax.transAxes, color=C_GOLD, fontsize=20, fontname='monospace')
    
    # Physics readouts
    density = max(0.1, (1500 - spar_y) / 100.0)
    ax.text(0.04, 0.81, f"LOCAL GAS DENSITY: {density:>06.2f} ρ", transform=ax.transAxes, color=C_RED, fontsize=20, fontname='monospace')
    
    # Ballast Math
    ax.text(0.04, 0.77, f"BALLAST DELTA (F): {ballast_delta:>06.2f} Δ", transform=ax.transAxes, color=ui_color, fontsize=20, fontname='monospace')

    # Formula Widget
    ax.text(0.04, 0.65, "[EQUILIBRIUM PROTOCOL]", transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace')
    ax.text(0.04, 0.63, "F_buoyancy = ρ * V * g", transform=ax.transAxes, color=C_GOLD, fontsize=18, fontname='monospace')

    ax.add_patch(plt.Rectangle((0, 0), 0.95, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 0.95], [0.12, 0.12], transform=ax.transAxes, color=ui_color, lw=2)
    
    pulse = ui_color if (f % 30 < 15) or ui_color == C_MANTIS else C_TEXT
    ax.text(0.04, 0.08, "SYSTEM STATUS:", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=28, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf()
    plt.close(fig)
    plt.close('all')
    gc.collect() 
    return f

# ------------------------------------------------------------------
# THE PHYSICS ENGINE (ORBITAL BUOYANCY & CRITICAL DAMPING)
# ------------------------------------------------------------------
def generate_physics_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        extract_stream = []
        
        # Phase 1: Orbital Ingress (0 - 10s)
        if t_sec < 10.0:
            state = "[01] ORBITAL INGRESS (UNCONSTRAINED)"
            ui_col = C_RED
            
            # Smooth descent from high orbit into the atmosphere
            progress = t_sec / 10.0
            # Ease-out cubic calculation
            eased = 1 - math.pow(1 - progress, 3)
            spar_y = 1800 - (eased * 1000)
            
            tether_len = 0.0
            ballast_delta = 500.0 - (progress * 400.0)

        # Phase 2: Anchoring & Penetration (10 - 20s)
        elif t_sec < 20.0:
            state = "[02] DEEP SEA ANCHORING (TETHER DEPLOYMENT)"
            ui_col = C_GOLD
            phase_t = (t_sec - 10.0) / 10.0
            
            # Platform sinks slightly from kinetic shock
            spar_y = 800 - (math.sin(phase_t * math.pi) * 100)
            
            # Tether shoots down into the core
            eased_tether = phase_t * phase_t
            tether_len = eased_tether * 1200.0
            
            ballast_delta = 100.0 + (math.sin(phase_t * math.pi * 4) * 80)

        # Phase 3: Ballast Adjustment / Critical Damping (20 - 27s)
        elif t_sec < 27.0:
            state = "[03] CRITICAL DAMPING (BUOYANCY CALIBRATION)"
            ui_col = C_CYAN
            phase_t = t_sec - 20.0
            
            # Damped Harmonic Oscillation (Surfing the gas giant)
            damp = math.exp(-phase_t * 0.6)
            spar_y = 800 + (math.sin(phase_t * 5.0) * 150 * damp)
            
            tether_len = 1200.0
            ballast_delta = math.cos(phase_t * 5.0) * 100 * damp

        # Phase 4: Terminal Green Flow / Harvesting (27 - 35s)
        else:
            state = "[04] TERMINAL GREEN FLOW (EXTRACTION ACTIVE)"
            ui_col = C_MANTIS
            phase_t = t_sec - 27.0
            
            # Absolute equilibrium achieved. Friction = 0.
            spar_y = 800.0
            tether_len = 1200.0
            ballast_delta = 0.0
            
            # Logic for extraction nodes flowing UP the tether
            tether_bottom = (spar_y + 200) - tether_len
            platform_top = spar_y + 200
            num_particles = int(phase_t * 5) # Particles increase over time
            num_particles = min(num_particles, 20)
            
            for p in range(num_particles):
                # Modular mathematics to loop the particles seamlessly
                particle_y = tether_bottom + (((f * 15) + (p * 80)) % tether_len)
                extract_stream.append(particle_y)
                
        yield (f, t_sec, spar_y, tether_len, ballast_delta, state, ui_col, np.array(extract_stream))

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER (BATCH EXECUTION)
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 154: ORBITAL SPAR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=4):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
