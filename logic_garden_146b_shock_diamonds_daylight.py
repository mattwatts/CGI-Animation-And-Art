"""
SOVEREIGN CODE: logic_garden_146b_shock_diamonds_daylight.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Eulerian Standing-Wave Tensor
SCENE: LG-146b (Shock Diamonds / Daylight Protocol)
HOTFIX: Exact Seamless Ouroboros Loop, Daylight High-Contrast Fluid Matrix
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 10.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_146b_shock_diamonds_daylight"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'        
C_TITANIUM  = '#1C2833'        
C_STEEL     = '#7F8C8D'        
C_GRID      = '#BDC3C7'        
C_TEXT      = '#111111'        

# Thermodynamic Mach Compression Palette
def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

C_STOPS = np.array([0.0, 0.2, 0.45, 0.8, 1.0])
C_RGBA = np.array([
    hex_to_rgba('#1A252F', 0.9),  # Outer Shear (Dark Heavy Gas for Contrast)
    hex_to_rgba('#2980B9', 0.9),  # Expansion Fan (Azure Core)
    hex_to_rgba('#00FFFF', 0.9),  # Supersonic Transition (Cyan)
    hex_to_rgba('#F1C40F', 1.0),  # Mach Disk Edge (Dense Gold)
    hex_to_rgba('#FFFFFF', 1.0)   # Absolute Compression (Pure White)
])

def multi_lerp(values):
    idx = np.searchsorted(C_STOPS, values) - 1
    idx = np.clip(idx, 0, len(C_STOPS)-2)
    t = (values - C_STOPS[idx]) / (C_STOPS[idx+1] - C_STOPS[idx] + 1e-9)
    t = t[:, np.newaxis]
    return (1.0 - t) * C_RGBA[idx] + t * C_RGBA[idx+1]

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY & O(1) FLUID ALLOCATION
# ------------------------------------------------------------------
CX = 540.0
CY_NOZZLE = 1650.0  
MAX_DIST = 1800.0   # Flow tracks down to Y = -150

N_GAS = 45000
np.random.seed(146)
offsets = np.random.uniform(0, 1, N_GAS)

# Cross-sectional distribution (u). Emphasize core density.
u_rand = np.random.normal(0, 0.35, N_GAS)
u_rand = np.clip(u_rand, -1.0, 1.0)

# Rotational Swirl for pseudo-3D turbulence (stable over the loop)
theta_rand = np.random.uniform(0, 2*np.pi, N_GAS)

# ------------------------------------------------------------------
# STANDING WAVE THERMODYNAMICS
# ------------------------------------------------------------------
def calculate_fluid_field(phase):
    """Maps continuous particle lifetimes against a stationary pressure field."""
    # T cycles exactly 0 -> 1 over the duration. Modulo enforces the loop.
    T = (offsets + phase) % 1.0
    
    # Distance from nozzle
    d = T * MAX_DIST
    curr_y = CY_NOZZLE - d

    # Mach Disk Standing Wave Equation
    WAVELENGTH = 240.0
    # Compression: 1.0 = Max compression (Disk), 0.0 = Max expansion (Bulge)
    k = (2.0 * np.pi) / WAVELENGTH
    
    # Mathematical shaping of the disk
    praw = (np.cos(d * k) + 1.0) / 2.0
    compression = np.power(praw, 3.5) # Sharpen the nodes

    # Base plume tapers slightly over distance
    base_radius = 160.0 * (1.0 - (d / MAX_DIST) * 0.3)
    
    # Envelope constricts violently at compression == 1.0
    envelope_r = base_radius * (1.0 - compression * 0.45)
    
    # Apply baseline random distribution to the dynamic envelope
    x_pos = CX + u_rand * envelope_r
    
    # Add high-frequency shear turbulence at the outer edges 
    edge_factor = np.abs(u_rand)
    shear_noise = np.sin(d * 0.08 + theta_rand) * 15.0 * edge_factor
    x_pos += shear_noise

    # Thermal/Pressure Matrix Evaluation
    # Heat is highest at exact center of compression nodes
    core_proximity = 1.0 - np.abs(u_rand)
    heat = compression * core_proximity
    
    # Residual heat in the expansion fans
    ambient_heat = (1.0 - compression) * core_proximity * 0.4
    total_heat = np.clip(heat + ambient_heat, 0, 1.0)
    
    # Attenuate overall energy as distance increases
    decay = np.clip(1.0 - (d / MAX_DIST)**1.5, 0.0, 1.0)
    total_heat *= decay

    # Map colors
    colors = multi_lerp(total_heat)
    
    # Fade alpha elegantly at genesis (nozzle) and death (bottom)
    alpha_mask = np.ones(N_GAS)
    fade_in = np.clip(d / 80.0, 0, 1)
    alpha_mask *= fade_in * decay
    colors[:, 3] *= alpha_mask

    # Volumetric resizing: Disks feature dense, massive tightly packed nodes
    sizes = 40.0 + (compression * core_proximity * 160.0) + (d * 0.05)
    
    return x_pos, curr_y, sizes, colors, decay

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    phase = f / float(TOTAL_FRAMES)
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)

    # Secure rendering pipeline (UI will not overstep)
    ax.set_xlim(0, 1080); ax.set_ylim(-150, 1850)

    # 1. RENDER 45,000-NODE FLUID TENSOR
    px, py, ps, pc, decay = calculate_fluid_field(phase)
    
    # Painter's Algorithm: Draw cooler/outer gas first, intensely hot dense core last
    heat_proxy = pc[:, 0] + pc[:, 1] + pc[:, 2] # Sum of RGB roughly tracks heat intensity in our palette
    sort_idx = np.argsort(heat_proxy)
    
    ax.scatter(px[sort_idx], py[sort_idx], s=ps[sort_idx], color=pc[sort_idx], edgecolors='none', zorder=10)

    # 2. RENDER THE ACTUATOR HARDWARE 
    # High-Contrast Machined Titanium Exhaust Nozzle
    n_width = 170.0
    n_top = 1850.0
    ax.add_patch(Rectangle((CX - n_width, CY_NOZZLE), n_width * 2, n_top - CY_NOZZLE, facecolor=C_TITANIUM, edgecolor=C_TEXT, lw=6, zorder=20))
    ax.add_patch(Polygon([[CX - n_width, CY_NOZZLE], [CX - n_width - 30, CY_NOZZLE - 60], [CX + n_width + 30, CY_NOZZLE - 60], [CX + n_width, CY_NOZZLE]], facecolor=C_STEEL, edgecolor=C_TEXT, lw=6, zorder=21))
    
    # Cooling / Expansion structural rings
    for ry in np.linspace(CY_NOZZLE + 40, n_top - 40, 5):
        ax.plot([CX - n_width, CX + n_width], [ry, ry], color=C_STEEL, lw=12, zorder=22)
        ax.plot([CX - n_width, CX + n_width], [ry, ry], color=C_TEXT, lw=4, zorder=23)

    # Secondary Afterburner Glow (Cast light reflecting off the inner nozzle wall)
    ax.add_patch(Rectangle((CX - n_width + 10, CY_NOZZLE), n_width * 2 - 20, 30, facecolor='#00FFFF', alpha=0.3, zorder=24))

    # 3. DIAGNOSTIC TELEMETRY WIDGETS
    # Anchored safely via transAxes. Zero occlusion of physical simulation.
    ax.add_patch(Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, facecolor=C_BG, edgecolor=C_TITANIUM, lw=4, clip_on=False, zorder=80))
    ax.text(0.5, 0.965, "LG-146b :: O(1) SHOCK DIAMOND TENSOR [DAYLIGHT]", transform=ax.transAxes, color=C_TITANIUM, fontsize=16, fontname='monospace', weight='bold', ha='center', va='center', zorder=81)

    ax.add_patch(Rectangle((0, 0), 1, 0.12, transform=ax.transAxes, facecolor=C_BG, edgecolor=C_TITANIUM, lw=4, zorder=80))
    ax.text(0.04, 0.08, "STATE: OVEREXPANDED SUPERSONIC PLUME", transform=ax.transAxes, color=C_TITANIUM, fontsize=20, fontname='monospace', weight='bold', zorder=81)
    
    pulse = '#F1C40F' if (f % 40 < 20) else '#00FFFF'
    ax.text(0.04, 0.035, "TRACE: NORMAL SHOCK RECOVERY NODES [MACH DISKS]", transform=ax.transAxes, color=pulse, fontsize=18, fontname='monospace', weight='bold', zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 146b: SHOCK DIAMONDS [DAYLIGHT PROTOCOL] [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: O(1) Standing Wave // Rigid Thermodynamic Palette")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            pass
    print("Compilation Complete. Absolute Ouroboros Fluid Tensor locked.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
