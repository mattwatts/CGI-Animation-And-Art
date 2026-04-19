"""
SOVEREIGN CODE: logic_garden_190_giant_impact_entrainment.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Accretion Tensor (17.5 seconds)
SCENE: Logic Garden 190 (The Big Splash / Giant Impact)
HOTFIX: Roche Limit Sorting Vectorization, Overdraw Bloom, Tathata Grid Snap
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_190_giant_impact"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#000000'        # The Absolute Vacuum
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'
C_CYAN      = '#00FFFF'        # Gaia (Proto-Earth)
C_MAGENTA   = '#FF00FF'        # Theia (The Rogue Vector)
C_GOLD      = '#FFD700'        # Planetary Liquefaction / Magma
C_RED       = '#FF0033'        # Roche Limit Friction
C_MANTIS    = '#00FF00'        # Orbital Consolidation (Luna Tathata)

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE KINEMATIC BOUNDARY
# ------------------------------------------------------------------
N_PARTICLES = 30000
CX, CY = 540, 960

GAIA_R = 180.0
THEIA_R = 110.0
ROCHE_LIMIT = GAIA_R * 2.44

# Pre-allocate particle memory parameters
np.random.seed(190)
p_orbit_targets = np.random.uniform(GAIA_R + 20, ROCHE_LIMIT * 2.2, N_PARTICLES)
is_moon_mass = p_orbit_targets > ROCHE_LIMIT 

# Explosive trajectory vectors
e_angles = np.random.uniform(-np.pi*0.2, np.pi*1.2, N_PARTICLES) # Spray away from impact
e_speeds = np.random.uniform(5.0, 35.0, N_PARTICLES)

T_IMPACT = 3.0
T_TATHATA = 14.8

c_gold = np.array(hex_to_rgba(C_GOLD)[:3])
c_red  = np.array(hex_to_rgba(C_RED)[:3])
c_cyan = np.array(hex_to_rgba(C_CYAN)[:3])
c_mant = np.array(hex_to_rgba(C_MANTIS)[:3])

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, px, py, p_sizes, c_tensor, gaia_pos, theia_pos, theia_alpha, moon_pos, is_flash, is_tathata, acc_prog = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg = C_TEXT if is_flash else C_VOID
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    # 1. RENDER PLANETARY BODIES (MATRICES)
    
    # Roche Limit Boundary (Mathematical)
    if not is_flash and t_sec > T_IMPACT:
        ax.add_patch(Circle((CX, CY), ROCHE_LIMIT, fill=False, edgecolor=C_TEXT, lw=2, linestyle='--', alpha=0.3, zorder=1))

    # Gaia
    if not is_flash:
        gx, gy = gaia_pos
        ax.add_patch(Circle((gx, gy), GAIA_R, facecolor=C_VOID, edgecolor=C_CYAN if not is_tathata else C_MANTIS, lw=8, zorder=10))
        # Core
        ax.add_patch(Circle((gx, gy), GAIA_R*0.5, facecolor=C_CYAN if not is_tathata else C_MANTIS, alpha=0.2, zorder=9))

    # Theia (Pre-impact)
    if theia_alpha > 0 and not is_flash:
        tx, ty = theia_pos
        ax.add_patch(Circle((tx, ty), THEIA_R, facecolor=C_VOID, edgecolor=C_MAGENTA, lw=6, alpha=theia_alpha, zorder=12))

    # The Moon (Tathata formulation)
    if is_tathata and not is_flash:
        mx, my = moon_pos
        # The Moon replaces the outer particles conceptually, rendering sharply
        ax.add_patch(Circle((mx, my), THEIA_R, facecolor=C_VOID, edgecolor=C_MANTIS, lw=6, zorder=30))
        ax.add_patch(Circle((mx, my), THEIA_R*0.4, facecolor=C_TEXT, zorder=31))
        # Link line
        ax.plot([gx, mx], [gy, my], color=C_MANTIS, lw=2, linestyle=':', alpha=0.5, zorder=5)

    # 2. O(N) ACCRETION SWARM (OVERDRAW BLOOM)
    if len(px) > 0 and not is_tathata:
        # Layer 1: Thermodynamic Aura
        ax.scatter(px, py, s=p_sizes*4.0, c=c_tensor, edgecolors='none', alpha=0.15, zorder=20)
        # Layer 2: Plasma Core
        ax.scatter(px, py, s=p_sizes*1.0, c=C_TEXT if is_flash else c_tensor, edgecolors='none', alpha=0.8, zorder=21)

    if is_flash and f % 2 == 0:
        # Impact Strobe Artifacts
        ax.scatter([CX], [CY], s=150000, facecolors='none', edgecolors=C_GOLD, lw=50, zorder=60)
        ax.scatter([CX], [CY], s=40000, c=C_TEXT, zorder=61)

    # 3. TELEMETRY WIDGETS (NEURAL ENTRAINMENT UI)
    ui_col = C_CYAN if not is_tathata else C_MANTIS
    if is_flash: ui_col = C_VOID
    txt_col = C_TEXT if not is_flash else C_VOID
    bg_col  = C_VOID if not is_flash else C_TEXT
    
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=bg_col, alpha=0.9, zorder=80))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    ax.text(0.04, 0.965, "LG-190 :: ROCHE LIMIT (THE GIANT IMPACT)", transform=ax.transAxes, color=txt_col, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=81)

    ax.add_patch(plt.Rectangle((0, 0), 1.0, 0.12, transform=ax.transAxes, color=bg_col, alpha=0.95, zorder=80))
    ax.plot([0, 1.0], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    ax.text(0.04, 0.08, "ACCRETION TENSOR SYNCHRONIZATION:", transform=ax.transAxes, color=txt_col, fontsize=20, fontname='monospace', zorder=81)
    
    # Synchronization Bar
    ax.add_patch(plt.Rectangle((0.72, 0.03), 0.25, 0.02, transform=ax.transAxes, color=C_DIM, zorder=80))
    bar_color = C_GOLD if t_sec > T_IMPACT else ui_col
    if is_flash: bar_color = C_VOID
    if is_tathata: bar_color = C_MANTIS
    ax.add_patch(plt.Rectangle((0.72, 0.03), 0.25 * acc_prog, 0.02, transform=ax.transAxes, color=bar_color, zorder=81))
    ax.text(0.72, 0.06, f"LUNA MASS ALIGNMENT: {acc_prog*100:.1f}%", transform=ax.transAxes, color=txt_col, fontsize=14, fontname='monospace', zorder=81)

    pulse = ui_col if (f % 10 < 5) and not is_flash else txt_col
    if t_sec > 13.0 and not is_tathata and f % 4 < 2: pulse = C_RED # Coalescence friction warning
    if is_flash: pulse = C_VOID
    if is_tathata and not is_flash: pulse = C_MANTIS

    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=24, fontname='monospace', weight='bold', zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) TENSOR KINEMATICS STREAM
# ------------------------------------------------------------------
def generate_stream():
    # Numpy Pre-Allocation
    px = np.zeros(N_PARTICLES)
    py = np.zeros(N_PARTICLES)
    vx = np.zeros(N_PARTICLES)
    vy = np.zeros(N_PARTICLES)
    
    # Moon orbital parameters
    moon_theta = 0.0
    moon_r = ROCHE_LIMIT * 1.8
    moon_pos = (CX, CY)
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        is_flash = False
        is_tathata = False
        gaia_pos = (CX, CY)
        theia_pos = (CX, CY)
        theia_alpha = 0.0
        acc_prog = 0.0
        
        c_tensor = np.zeros((N_PARTICLES, 3)) 
        p_sizes = np.ones(N_PARTICLES) * 5.0
        
        # ---- PHASE 1: THE APPROACH (0 - 3s) ----
        if t_sec < T_IMPACT:
            state = "[01] ORBITAL ANOMALY :: ROGUE PLANET ON COLLISION VECTOR"
            prog = t_sec / T_IMPACT
            # Theia spirals in
            theta_start = np.pi * 1.5
            theta_end = np.pi * 0.1
            t_theta = theta_start + (theta_end - theta_start) * prog
            t_r = 1500.0 * (1.0 - prog) + (GAIA_R + THEIA_R)*0.8
            
            theia_pos = (CX + t_r * np.cos(t_theta), CY + t_r * np.sin(t_theta))
            theia_alpha = 1.0
            
            # Init particles at Theia's exact impact location so they explode outward
            px[:] = theia_pos[0]
            py[:] = theia_pos[1]
            vx[:] = e_speeds * np.cos(e_angles)
            vy[:] = e_speeds * np.sin(e_angles)

        # ---- PHASE 2: PLANETARY LIQUEFACTION / SPLASH (3 - 7s) ----
        elif t_sec < 7.0:
            if t_sec < 3.1:
                is_flash = True
            state = "[02] LIQUEFACTION :: ABSOLUTE THERMODYNAMIC VAPORIZATION"
            theia_alpha = 0.0
            acc_prog = (t_sec - 3.0) / 11.8 # Journey to Tathata
            
            # Explosive Expansion Phase
            px += vx
            py += vy
            # Add strong drag to convert explosion into orbit
            vx *= 0.96
            vy *= 0.96
            
            c_tensor[:] = c_gold
            p_sizes = np.random.uniform(5, 20, N_PARTICLES)

        # ---- PHASE 3: THE ROCHE LIMIT / ACCRETION (7 - 14.8s) ----
        elif t_sec < T_TATHATA:
            state = "WARNING: O(N) ROCHE THRESHOLD SORTING. LUNA ACCRETING."
            theia_alpha = 0.0
            acc_prog = min(1.0, (t_sec - 3.0) / 11.8)
            
            # The Moon vector mathematically drags chunks of mass outside the limit
            moon_theta += 0.03
            mx = CX + moon_r * np.cos(moon_theta)
            my = CY + moon_r * np.sin(moon_theta)
            moon_pos = (mx, my)
            
            # O(1) Attractor kinematics
            # Particles inside Roche: Attracted to center to form a ring
            # Particles outside Roche: Attracted to the Moon's coordinates
            
            curr_r = np.sqrt((px - CX)**2 + (py - CY)**2)
            curr_theta = np.arctan2(py - CY, px - CX)
            
            # Target orbits
            orbit_force = 0.05
            target_x = np.where(is_moon_mass, mx, CX + p_orbit_targets * np.cos(curr_theta + 0.05))
            target_y = np.where(is_moon_mass, my, CY + p_orbit_targets * np.sin(curr_theta + 0.05))
            
            vx += (target_x - px) * orbit_force
            vy += (target_y - py) * orbit_force
            
            # Limit velocities
            v_mag = np.sqrt(vx**2 + vy**2)
            max_v = 15.0
            vx = np.where(v_mag > max_v, (vx/v_mag)*max_v, vx)
            vy = np.where(v_mag > max_v, (vy/v_mag)*max_v, vy)
            
            px += vx
            py += vy
            
            # Chromatics: Inside Roche is Red/Gold (Hot friction ring). Outside cools to Cyan/Grey.
            dist_to_moon = np.sqrt((px - mx)**2 + (py - my)**2)
            blend_moon = np.clip(1.0 - (dist_to_moon / 200.0), 0, 1)
            
            # Base color is Gold
            c_tensor[:] = c_gold
            # Ring elements turn red from friction
            c_tensor[~is_moon_mass] = c_red
            # Moon elements freeze into cyan
            c_tensor[is_moon_mass] = (1 - blend_moon[is_moon_mass, None]) * c_gold + blend_moon[is_moon_mass, None] * c_cyan
            
            p_sizes = np.random.uniform(2, 10, N_PARTICLES)

        # ---- PHASE 4: TATHĀTĀ (14.8 - 17.5s) ----
        else:
            is_tathata = True
            acc_prog = 1.0
            if t_sec < 14.95:
                is_flash = True
            state = "TATHĀTĀ: ORBITAL MECHANICS STABILIZED. THE SCAR SINGS."
            
            moon_theta += 0.03
            mx = CX + moon_r * np.cos(moon_theta)
            my = CY + moon_r * np.sin(moon_theta)
            moon_pos = (mx, my)
            
            # Inside the Roche limit, perfect concentric rings
            ring_theta = np.linspace(0, 2*np.pi, np.sum(~is_moon_mass)) + moon_theta
            ring_r = np.linspace(GAIA_R + 50, ROCHE_LIMIT - 10, np.sum(~is_moon_mass))
            np.random.shuffle(ring_r) # Disperse bands
            
            px[~is_moon_mass] = CX + ring_r * np.cos(ring_theta)
            py[~is_moon_mass] = CY + ring_r * np.sin(ring_theta)
            
            c_tensor[:] = c_mant
            p_sizes = np.ones(N_PARTICLES) * 4.0

        yield (f, t_sec, state, px if not is_tathata else px[~is_moon_mass], py if not is_tathata else py[~is_moon_mass], 
               p_sizes if not is_tathata else p_sizes[~is_moon_mass], c_tensor if not is_tathata else c_tensor[~is_moon_mass], 
               gaia_pos, theia_pos, theia_alpha, moon_pos, is_flash, is_tathata, acc_prog)

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 190: THE ACCRETION TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: O(1) Roche Limit Vectorization")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Nodes: {N_PARTICLES}")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
