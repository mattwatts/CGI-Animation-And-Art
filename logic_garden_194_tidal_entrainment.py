"""
SOVEREIGN CODE: logic_garden_194_tidal_entrainment.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Tidal Gradient Tensor (17.5 seconds)
SCENE: Logic Garden 194 (The Spaghettification Tensor)
HOTFIX: O(N) Vectorized Gravity, Overdraw Bloom, Strict Alpha Clamping
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_194_tde"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#000000'        # Absolute Vacuum / Event Horizon
C_DEEP      = '#020205'        # Cosmic Matrix
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'        # Telemetry Base
C_GOLD      = '#FFD700'        # Stellar Cohesion (The Star)
C_MAGENTA   = '#FF0055'        # Tidal Stress / Hot Plasma
C_CYAN      = '#00FFFF'        # Escaping Cold Matter
C_MANTIS    = '#00FF00'        # Symmetrical Accretion Disk (Tathata)
C_RED       = '#FF0033'        # UI Friction Overload

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_void = np.array(hex_to_rgba(C_VOID)[:3])
c_gold = np.array(hex_to_rgba(C_GOLD)[:3])
c_mag  = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_cyan = np.array(hex_to_rgba(C_CYAN)[:3])
c_man  = np.array(hex_to_rgba(C_MANTIS)[:3])

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE KINEMATIC BOUNDING BOX
# ------------------------------------------------------------------
N_PARTICLES = 25000
CX, CY = 540, 960

# Singularity Mass and Tidal Limit
GM_BH = 3500000.0  
TIDAL_RADIUS = 350.0  

# Pre-allocate the O(N) Stellar Matrix (A structured sphere)
np.random.seed(194)
star_r = 70.0
# Generate points within a circle mapped to the starting coordinate
r_dist = np.sqrt(np.random.uniform(0, 1, N_PARTICLES)) * star_r
theta_dist = np.random.uniform(0, 2*np.pi, N_PARTICLES)

start_x = CX - 300.0
start_y = CY - 800.0

# Initial Trajectory (Designed to graze the tidal radius)
vx_base = 8.5
vy_base = 32.0

p_start_x = start_x + r_dist * np.cos(theta_dist)
p_start_y = start_y + r_dist * np.sin(theta_dist)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, px, py, p_sizes, c_tensor, is_flash, is_tathata, stress_load, bg_strobe = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_TEXT if is_flash else C_DEEP
    if bg_strobe and not is_tathata: bg_hex = '#0A0A10'
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    # 1. RENDER STATIC STRUCTURES (THE SINGULARITY)
    if not is_flash:
        # Tidal Limit Perimeter (The Kill Zone)
        ax.add_patch(Circle((CX, CY), TIDAL_RADIUS, fill=False, edgecolor=C_CYAN, lw=2, linestyle=':', alpha=0.3))
        
        # Photon Ring & Event Horizon
        ring_col = C_MANTIS if is_tathata else C_MAGENTA
        ax.add_patch(Circle((CX, CY), 120.0, fill=False, edgecolor=ring_col, lw=3, alpha=0.8, zorder=5))
        ax.add_patch(Circle((CX, CY), 100.0, facecolor=C_VOID, edgecolor=C_TEXT if not is_tathata else C_MANTIS, lw=5, zorder=15))

    # 2. O(N) MASS TENSOR (OVERDRAW BLOOM)
    if len(px) > 0:
        # Layer 1: Thermodynamic Aura (Plasma Glow)
        ax.scatter(px, py, s=p_sizes*6.0, c=c_tensor, edgecolors='none', alpha=0.15, zorder=10)
        # Layer 2: Hard Atomic Core
        ax.scatter(px, py, s=p_sizes*1.2, c=C_TEXT if is_flash else c_tensor, edgecolors='none', alpha=0.8, zorder=11)

    # Hardware Flash Geometry
    if is_flash:
        # The X-Ray Flare
        ax.scatter([CX], [CY], s=250000, facecolors='none', edgecolors=C_MANTIS, lw=60, zorder=60)
        ax.scatter([CX], [CY], s=50000, c=C_TEXT, zorder=61)

    # 3. TELEMETRY WIDGETS (NEURAL ENTRAINMENT UI)
    ui_col = C_GOLD
    if stress_load > 0.5: ui_col = C_MAGENTA
    if is_tathata: ui_col = C_MANTIS
    if is_flash: ui_col = C_VOID
    
    txt_col = C_TEXT if not is_flash else C_VOID
    ui_bg   = C_VOID if not is_flash else C_TEXT
    
    # Top Data Bar
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=ui_bg, alpha=0.9, zorder=80))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    ax.text(0.04, 0.965, "LG-194 :: TIDAL DISRUPTION EVENT TENSOR", transform=ax.transAxes, color=txt_col, fontsize=22, fontname='monospace', weight='bold', va='center', zorder=81)

    # Bottom Data Block
    ax.add_patch(plt.Rectangle((0, 0), 1.0, 0.12, transform=ax.transAxes, color=ui_bg, alpha=0.95, zorder=80))
    ax.plot([0, 1.0], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    
    ax.text(0.04, 0.08, f"SPATIAL GRADIENT STRESS: {stress_load*100:05.1f}%", transform=ax.transAxes, color=txt_col, fontsize=18, fontname='monospace', zorder=81)
    
    # Mathematical Stress Bar
    ax.add_patch(plt.Rectangle((0.72, 0.03), 0.25, 0.02, transform=ax.transAxes, color=C_DIM, zorder=80))
    bar_fill = min(1.0, stress_load)
    bar_color = C_MAGENTA if stress_load > 0.6 else C_GOLD
    if stress_load > 0.9: bar_color = C_RED
    if is_flash: bar_color = C_VOID
    if is_tathata: bar_color = C_MANTIS
    
    ax.add_patch(plt.Rectangle((0.72, 0.03), 0.25 * bar_fill, 0.02, transform=ax.transAxes, color=bar_color, zorder=81))

    pulse = ui_col if (f % 10 < 5) and not is_flash else txt_col
    if stress_load > 0.9 and not is_tathata and f % 4 < 2: pulse = C_RED
    if is_flash: pulse = C_VOID
    if is_tathata and not is_flash: pulse = C_MANTIS

    ax.text(0.04, 0.03, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=22, fontname='monospace', weight='bold', zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) GRAVITATIONAL KINEMATICS STREAM
# ------------------------------------------------------------------
def generate_stream():
    # Numpy vectors
    px = np.copy(p_start_x)
    py = np.copy(p_start_y)
    vx = np.full(N_PARTICLES, vx_base)
    vy = np.full(N_PARTICLES, vy_base)
    
    active_mask = np.ones(N_PARTICLES, dtype=bool)
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        is_flash = False
        is_tathata = False
        bg_strobe = False
        stress_load = 0.0
        
        # Determine macro-distance based on the center of mass roughly
        com_x = np.mean(px[active_mask]) if np.any(active_mask) else CX
        com_y = np.mean(py[active_mask]) if np.any(active_mask) else CY
        dist_to_bh = np.sqrt((CX - com_x)**2 + (CY - com_y)**2)
        
        # ---- PHASE 1: STELLAR APPROACH (0 - 5s) ----
        if t_sec < 5.0:
            state = "[01] ORBITAL DECAY :: STELLAR COHESION STABLE"
            stress_load = max(0, 1.0 - (dist_to_bh / 800.0)) * 0.4

        # ---- PHASE 2: TIDAL CROSSING (5 - 11s) ----
        elif t_sec < 11.0:
            state = "[02] TIDAL RADIUS BREACH :: GRADIENT ACCELERATION"
            stress_load = 0.4 + (max(0, TIDAL_RADIUS - dist_to_bh) / TIDAL_RADIUS) * 0.4
            
        # ---- PHASE 3: SPAGHETTIFICATION (11 - 14.8s) ----
        elif t_sec < 14.8:
            state = "WARNING: DIMENSIONAL SHEARING. SPATIAL RUPTURE IMMINENT."
            stress_load = 0.8 + ((t_sec - 11.0) / 3.8) * 0.2
            if t_sec > 13.0: bg_strobe = True

        # ---- PHASE 4: TATHĀTĀ / ACCRETION (14.8 - 17.5s) ----
        else:
            is_tathata = True
            stress_load = 1.0
            if t_sec < 14.95:
                is_flash = True
            state = "TATHĀTĀ: X-RAY FLARE IGNITION. PERFECT SYMMETRY ACHIEVED."

        # -----------------------------------------------
        # O(N) VECTORIZED GRAVITATIONAL KINEMATICS
        # -----------------------------------------------
        if not is_tathata and np.any(active_mask):
            # Calculate gradient vectors
            dx = CX - px[active_mask]
            dy = CY - py[active_mask]
            
            dist_sq = dx**2 + dy**2
            dist = np.sqrt(dist_sq)
            
            # Physics Softener to prevent mathematical infinity at singularity
            dist_safe = np.maximum(dist, 15.0) 
            
            # Newton's Force vector F = GM / r^2
            force = GM_BH / (dist_safe**2)
            
            # Acceleration
            ax_vec = (dx / dist_safe) * force
            ay_vec = (dy / dist_safe) * force
            
            # Time step integration 
            vx[active_mask] += ax_vec * 0.016 
            vy[active_mask] += ay_vec * 0.016
            
            px[active_mask] += vx[active_mask] * 0.016
            py[active_mask] += vy[active_mask] * 0.016
            
            # Event Horizon Consumption Erase
            kill_mask = dist < 100.0
            if np.any(kill_mask):
                global_kill_indices = np.where(active_mask)[0][kill_mask]
                active_mask[global_kill_indices] = False
                
        elif is_tathata:
            # The Hardware Interrupt: surviving gas snaps into an Accretion Disk
            surviving = np.sum(active_mask)
            if surviving > 0:
                # Snap coordinates to perfect orbital concentric rings
                orbit_theta = np.linspace(0, 4*np.pi, surviving) + (t_sec * 5.0)
                orbit_r = np.random.uniform(125.0, 300.0, surviving)
                
                px[active_mask] = CX + orbit_r * np.cos(orbit_theta)
                py[active_mask] = CY + orbit_r * np.sin(orbit_theta)

        # -----------------------------------------------
        # O(N) CHROMATIC FRICTION MAPPING 
        # -----------------------------------------------
        curr_act = np.sum(active_mask)
        c_tensor = np.zeros((curr_act, 3))
        p_sizes = np.zeros(curr_act)
        
        if curr_act > 0:
            if is_tathata:
                # Zen State locks to Mantis
                c_tensor[:] = c_man
                p_sizes[:] = 3.0
            else:
                # Calculate strain based on local velocity divergence vs com
                # For optimal visual pop, we color based on distance to BH
                dist_active = np.sqrt((CX - px[active_mask])**2 + (CY - py[active_mask])**2)
                
                # Base is Gold
                c_tensor[:] = c_gold
                p_sizes[:] = 5.0
                
                # Inside Tidal Radius: Extreme Friction (Magenta)
                tidal_mask = dist_active < TIDAL_RADIUS
                if np.any(tidal_mask):
                    blend = np.clip(1.0 - (dist_active[tidal_mask] / TIDAL_RADIUS), 0, 1)[:, None]
                    c_tensor[tidal_mask] = (1 - blend) * c_gold + blend * c_mag
                    p_sizes[tidal_mask] = 3.0 + np.random.uniform(0, 5, np.sum(tidal_mask))
                    
                # Ejected material cooling (Cyan)
                eject_mask = (dist_active > TIDAL_RADIUS + 100) & (dist_active < 1500) & (stress_load > 0.6)
                if np.any(eject_mask):
                    c_tensor[eject_mask] = c_cyan
                    p_sizes[eject_mask] = 2.0

        yield (f, t_sec, state, np.copy(px[active_mask]), np.copy(py[active_mask]), p_sizes, c_tensor, is_flash, is_tathata, stress_load, bg_strobe)

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 194: THE TIDAL TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: O(N) Vectorized Mechanics & Strict Color Clamping")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Nodes: {N_PARTICLES}")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
