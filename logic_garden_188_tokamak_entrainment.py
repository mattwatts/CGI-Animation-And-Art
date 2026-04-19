"""
SOVEREIGN CODE: logic_garden_188_tokamak_entrainment.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Lorentz Tensor (17.5 seconds)
SCENE: Logic Garden 188 (The Magnetic Bottle / Tokamak Fusion)
HOTFIX: O(N) Plasma Swarm, Stochastic Fusion Scaling, Neon Pop Kinematics
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon
import multiprocessing as mp
import os
import gc
import math

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_188_tokamak"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#000000'        # Absolute Zero Friction Vacuum
C_TEXT      = '#FFFFFF'
C_DIM       = '#16161D'        # Supercooled Iron/Tungsten Walls
C_CYAN      = '#00FFFF'        # Deuterium Plasma
C_MAGENTA   = '#FF00FF'        # Tritium Plasma
C_GOLD      = '#FFD700'        # Toroidal Magnetic Field Lines
C_RED       = '#FF0033'        # Thermal Instability (Overload)
C_MANTIS    = '#00FF00'        # Sustained Ignition (Terminal Flow)

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE MAGNETIC BOUNDARY
# ------------------------------------------------------------------
N_PARTICLES = 25000
CX, CY = 540, 960

# Tokamak Geometry (Top-Down)
R_INNER = 180.0
R_OUTER = 480.0
R_PLASMA = (R_INNER + R_OUTER) / 2.0
A_MINOR = (R_OUTER - R_INNER) / 2.0  # Minor radius constraint

D_COL = np.array(hex_to_rgba(C_CYAN)[:3])
T_COL = np.array(hex_to_rgba(C_MAGENTA)[:3])
I_COL = np.array(hex_to_rgba(C_MANTIS)[:3])

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, px, py, p_cols, p_sizes, field_amp, flare_pts, is_flash, temp_k, is_tathata = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg = C_TEXT if is_flash else C_VOID
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    # 1. RENDER STRUCTURES (THE MACHINE)
    
    # Outer Containment Wall
    ax.add_patch(Circle((CX, CY), R_OUTER + 80, facecolor=C_VOID, edgecolor=C_DIM if not is_flash else C_VOID, lw=10, zorder=1))
    ax.add_patch(Circle((CX, CY), R_OUTER + 20, facecolor=C_VOID, edgecolor='#22222A' if not is_flash else C_VOID, lw=4, zorder=2))
    
    # Inner Solenoid Core
    ax.add_patch(Circle((CX, CY), R_INNER - 20, facecolor=C_DIM if not is_flash else C_TEXT, edgecolor='#33333D', lw=6, zorder=30))
    ax.add_patch(Circle((CX, CY), R_INNER - 60, facecolor=C_VOID if not is_flash else C_MANTIS, zorder=31))
    
    # Mathematical Bounding Box (Magnetic Field Lines)
    # They tighten and glow Gold under pressure
    f_col = C_GOLD if temp_k > 0.5 else C_CYAN
    f_alpha = 0.2 + (field_amp * 0.8)
    if not is_flash:
        for r_line in np.linspace(R_INNER, R_OUTER, 6):
            if f % 20 < 10 and temp_k > 0.8: # Strobing field under max load
                continue
            ax.add_patch(Circle((CX, CY), r_line, facecolor='none', edgecolor=f_col, lw=2, alpha=f_alpha, linestyle='--', zorder=5))

        # Radial Solenoid Coils
        for ang in np.linspace(0, 2*np.pi, 18, endpoint=False):
            x1, y1 = CX + (R_INNER-20)*np.cos(ang), CY + (R_INNER-20)*np.sin(ang)
            x2, y2 = CX + (R_OUTER+80)*np.cos(ang), CY + (R_OUTER+80)*np.sin(ang)
            ax.plot([x1, x2], [y1, y2], color=C_DIM, lw=8, zorder=3)
            ax.plot([x1, x2], [y1, y2], color=C_TEXT, lw=1, alpha=0.3, zorder=4)

    # 2. O(N) PLASMA SWARM (OVERDRAW BLOOM)
    if len(px) > 0:
        # Layer 1: Aura
        ax.scatter(px, py, s=p_sizes, c=p_cols, edgecolors='none', alpha=0.15, zorder=10)
        # Layer 2: Nuclei Core
        ax.scatter(px, py, s=p_sizes*0.2, c=C_TEXT if is_tathata else p_cols, edgecolors='none', alpha=0.7, zorder=11)

    # 3. $O(1)$ STOCHASTIC FUSION FLARES
    if len(flare_pts) > 0 and not is_flash:
        fx, fy, f_sizes = flare_pts[:,0], flare_pts[:,1], flare_pts[:,2]
        ax.scatter(fx, fy, s=f_sizes*15, facecolors='none', edgecolors=C_TEXT, lw=4, alpha=0.8, zorder=20)
        ax.scatter(fx, fy, s=f_sizes*40, facecolors='none', edgecolors=C_MANTIS, lw=2, alpha=0.5, zorder=19)
        ax.scatter(fx, fy, s=f_sizes*2, c=C_TEXT, zorder=21)

    # Hardware Flash Geometry
    if is_flash:
        ax.add_patch(Circle((CX, CY), R_PLASMA, facecolor='none', edgecolor=C_MANTIS, lw=80, alpha=0.8, zorder=60))
        ax.add_patch(Circle((CX, CY), R_PLASMA, facecolor='none', edgecolor=C_TEXT, lw=20, zorder=61))

    # 4. TELEMETRY WIDGETS (NEURAL ENTRAINMENT UI)
    ui_col = C_CYAN if not is_tathata else C_MANTIS
    if is_flash: ui_col = C_VOID
    txt_col = C_TEXT if not is_flash else C_VOID
    bg_col  = C_VOID if not is_flash else C_TEXT
    
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=bg_col, alpha=0.9, zorder=80))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    ax.text(0.04, 0.965, "LG-188 :: MAGNETIC CONFINEMENT TENSOR", transform=ax.transAxes, color=txt_col, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=81)

    ax.add_patch(plt.Rectangle((0, 0), 1.0, 0.12, transform=ax.transAxes, color=bg_col, alpha=0.95, zorder=80))
    ax.plot([0, 1.0], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    ax.text(0.04, 0.08, f"CORE TEMPERATURE: {int(temp_k * 150):>3d},000,000 °C", transform=ax.transAxes, color=txt_col, fontsize=20, fontname='monospace', zorder=81)
    
    # Lorentz Force Integrity Bar
    ax.add_patch(plt.Rectangle((0.72, 0.03), 0.25, 0.02, transform=ax.transAxes, color=C_DIM, zorder=80))
    
    bar_color = C_GOLD if temp_k > 0.8 else ui_col
    if is_flash: bar_color = C_VOID
    bar_fill = 1.0 if is_tathata else max(0.1, field_amp)
    
    ax.add_patch(plt.Rectangle((0.72, 0.03), 0.25 * bar_fill, 0.02, transform=ax.transAxes, color=bar_color, zorder=81))
    ax.text(0.72, 0.06, f"LORENTZ SHIELD: {bar_fill*100:.1f}%", transform=ax.transAxes, color=txt_col, fontsize=14, fontname='monospace', zorder=81)

    pulse = ui_col if (f % 10 < 5) and not is_flash else txt_col
    if temp_k > 0.8 and not is_tathata and (f % 6 < 3): pulse = C_RED # Overload strobe
    if is_flash: pulse = C_VOID
    if is_tathata and not is_flash: pulse = C_MANTIS

    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=24, fontname='monospace', weight='bold', zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) PLASMA DYNAMICS STREAM (LORENTZ FUNNEL)
# ------------------------------------------------------------------
def generate_stream():
    # Numpy Pre-Allocation
    # Assign 50% Deuterium (Cyan), 50% Tritium (Magenta)
    p_type  = np.random.randint(0, 2, N_PARTICLES)
    p_theta = np.random.uniform(0, 2*np.pi, N_PARTICLES)
    
    # Internal ring distribution (Gaussian mapped to minor radius)
    p_r_base = np.clip(np.random.normal(R_PLASMA, A_MINOR*0.3, N_PARTICLES), R_INNER+10, R_OUTER-10)
    
    # Thermal kinetics
    p_wobble = np.random.uniform(0, 2*np.pi, N_PARTICLES)
    p_speed  = np.random.uniform(0.01, 0.03, N_PARTICLES)
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        is_flash = False
        is_tathata = False
        temp_k = 0.0
        field_amp = 1.0
        flare_chance = 0.0
        
        # ---- PHASE 1: PLASMA INJECTION (0 - 4s) ----
        if t_sec < 4.0:
            state = "[01] INJECTION :: O(N) D-T ISOTOPES STABLE"
            temp_k = 0.1 + (t_sec * 0.05)
            wobb_amp = 5.0
            
        # ---- PHASE 2: MAGNETIC HEATING (4 - 10s) ----
        elif t_sec < 10.0:
            state = "[02] HEATING :: THERMAL INSTABILITY RISING"
            prog = (t_sec - 4.0) / 6.0
            temp_k = 0.3 + (prog * 0.5)
            wobb_amp = 5.0 + (prog * 45.0) # Plasma starts violently escaping
            field_amp = 1.0 - (prog * 0.4) # Magnetic field struggles
            flare_chance = prog * 0.05

        # ---- PHASE 3: IGNITION BOUNDARY / OVERLOAD (10 - 14.8s) ----
        elif t_sec < 14.8:
            state = "WARNING: LORENTZ TENSOR LOAD CRITICAL. CONTAINMENT AT RISK."
            prog = (t_sec - 10.0) / 4.8
            temp_k = 0.8 + (prog * 0.2)
            wobb_amp = 50.0 + (prog * 60.0) # Absolute chaos
            field_amp = 0.6 - (prog * 0.5)
            flare_chance = 0.1 + (prog * 0.6) # Massive fusion events

        # ---- PHASE 4: TATHĀTĀ / IGNITION SECURED (14.8 - 17.5s) ----
        else:
            temp_k = 1.0
            field_amp = 1.0
            is_tathata = True
            if t_sec < 14.95:
                is_flash = True
            state = "TATHĀTĀ: GEOMETRY TRIUMPHS OVER ENTROPY. IGNITION SUSTAINED."
            wobb_amp = 0.0  # Perfect quantum lock

        # -----------------------------------------------
        # O(1) KINEMATIC SOLVER
        # -----------------------------------------------
        # Orbital Velocity (Increases with heat)
        p_theta = (p_theta + p_speed * (1.0 + temp_k*10.0)) % (2*np.pi)
        
        # Thermal Jitter (Gyromotion)
        p_wobble += 0.4 * (1.0 + temp_k*5.0)
        
        # Current Radius = Base + Thermal Wobble
        # If Tathata, everything locks to the absolute center of the torus
        if is_tathata:
            current_r = R_PLASMA + np.random.normal(0, 10, N_PARTICLES)
        else:
            current_r = p_r_base + np.sin(p_wobble) * wobb_amp
        
            # Magnetic Containment Constraint (The Force)
            # If they hit the invisible walls, they are shoved back violently.
            current_r = np.clip(current_r, R_INNER+15, R_OUTER-15)

        # Convert Polar to Cartesian
        px = CX + current_r * np.cos(p_theta)
        py = CY + current_r * np.sin(p_theta)

        # -----------------------------------------------
        # O(1) STOCHASTIC FUSION EVENTS
        # -----------------------------------------------
        # We don't check N^2 manually. We spawn N flares mapped internally to plasma coords.
        flare_list = []
        if flare_chance > 0 and not is_tathata:
            num_flares = int(np.random.normal(flare_chance * 250, 10))
            if num_flares > 0:
                f_idx = np.random.randint(0, N_PARTICLES, num_flares)
                f_x, f_y = px[f_idx], py[f_idx]
                f_s = np.random.uniform(20, 80, num_flares) * temp_k
                flare_list = np.column_stack((f_x, f_y, f_s))
        
        flare_pts = np.array(flare_list) if len(flare_list) > 0 else np.array([])

        # -----------------------------------------------
        # O(N) COLOR CHROMATICS MATRIX 
        # -----------------------------------------------
        # Start Cyan/Magenta, under extreme heat they white-out, finally locking to Mantis
        c_tensor = np.zeros((N_PARTICLES, 3)) 
        
        if is_tathata:
            c_tensor[:] = I_COL
            p_sizes = np.random.uniform(5, 40, N_PARTICLES)
        else:
            # Base types
            c_tensor[p_type == 0] = D_COL
            c_tensor[p_type == 1] = T_COL
            
            # Blend towards White based on heat
            if temp_k > 0.3:
                blend = min(1.0, (temp_k - 0.3) * 1.2)
                c_tensor = (1.0 - blend) * c_tensor + blend * np.array([1.0, 1.0, 1.0])

            p_sizes = np.random.uniform(10, 50, N_PARTICLES) + (temp_k * 40.0)

        yield (f, t_sec, state, px, py, c_tensor, p_sizes, field_amp, flare_pts, is_flash, temp_k, is_tathata)

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 188: THE TOKAMAK ENTRAINMENT [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: O(N) Lorentz Constraints & Stochastic Fusion")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Nodes: {N_PARTICLES}")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
