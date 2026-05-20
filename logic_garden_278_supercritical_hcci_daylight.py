"""
SOVEREIGN CODE: logic_garden_278_supercritical_hcci_daylight.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Fluid Phase Tensor
SCENE: LG-278 (Supercritical Free-Piston HCCI / Daylight Protocol)
HOTFIX: Magnetic Linear Alternator Physics, Supercritical Phase Transform
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 10.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_278_supercritical_hcci_daylight"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'        
C_TITANIUM  = '#1C2833'        # Magnetic Piston Masses
C_STEEL     = '#7F8C8D'        # Machined Cylinder Liners
C_ALUM      = '#EAEDED'        # Static Engine Housing
C_COPPER    = '#B9770E'        # Faraday Induction Coils
C_FLUX      = '#00FFFF'        # Alternator Current Plasma
C_TEXT      = '#111111'        

# Thermodynamics
C_BIO_RAW   = np.array([0.15, 0.68, 0.38]) # Jagged Waste Biodiesel (Green)
C_SUPERCRIT = np.array([0.20, 0.60, 0.86]) # Homogenized Supercritical Grid
C_HCCI_BURN = np.array([0.29, 0.00, 0.51]) # Indigo Simultaneous Flash
C_FLASH     = np.array([1.00, 1.00, 1.00]) # Pure White Detonation Core
C_EXHAUST   = np.array([0.70, 0.70, 0.75]) # Clean H20 / CO2 trace

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY & O(1) FLUID ALLOCATION
# ------------------------------------------------------------------
CX, CY = 540, 1100      
BORE = 260.0
STROKE = 220.0
MIN_GAP = 40.0 # Absolute inner dead center gap
PISTON_L = 280.0
CYL_EXTENT = 850.0

N_GAS = 26000
np.random.seed(278)
offsets = np.random.rand(N_GAS)
g_rx = np.clip(np.random.normal(0, 0.4, N_GAS), -1, 1) 
g_ry = np.random.uniform(-1, 1, N_GAS)
turb = np.random.uniform(-1, 1, N_GAS)

# ------------------------------------------------------------------
# FREE-PISTON KINEMATICS (Harmonic Magnetic Restraint)
# ------------------------------------------------------------------
def get_kinematics(e_mod):
    """
    e_mod cycles 0 -> 1.
    0.5 is Inner Dead Center (IDC) - Full Compression.
    0.0 / 1.0 is Outer Dead Center (ODC) - Expansion / Scavenge.
    Free pistons have a physically "snappier" turnaround at compression
    and linger slightly at ODC due to the air-spring geometry.
    """
    # Profile shaping to mimic non-crankshaft bouncing
    raw_cycle = np.cos(2 * np.pi * (e_mod - 0.5)) 
    # Compress sharp, expand broad
    pos_factor = (raw_cycle + 1.0) / 2.0 
    pos_factor = np.power(pos_factor, 1.5) # Sharpens the IDC spike
    
    # Derivation for Alternator Voltage (Velocity proportional)
    delta = 1e-4
    raw_next = np.cos(2 * np.pi * (e_mod + delta - 0.5))
    pos_next = np.power((raw_next + 1.0) / 2.0, 1.5)
    velocity = (pos_factor - pos_next) / delta # Proportional to flux
    
    l_px = CX - (MIN_GAP/2) - (STROKE * (1.0 - pos_factor))
    r_px = CX + (MIN_GAP/2) + (STROKE * (1.0 - pos_factor))
    
    return l_px, r_px, pos_factor, velocity

# ------------------------------------------------------------------
# FLUID TENSOR / SUPERCRITICAL SHATTER
# ------------------------------------------------------------------
def get_fluid_state(T, l_px, r_px, pos_factor):
    """O(1) lifetime mapping. 1 Cycle = 1 Particle Journey"""
    px = np.zeros(N_GAS)
    py = np.zeros(N_GAS)
    pc = np.zeros((N_GAS, 3))
    ps = np.full(N_GAS, 16.0)
    pa = np.ones(N_GAS)
    
    # T_0 -> 0.15: Intake Manifold (Waste Injection)
    m_in = T < 0.15
    pr_in = T[m_in] / 0.15
    px[m_in] = (CX - 380) - (g_rx[m_in]*40) - pr_in*100
    py[m_in] = 1750 - pr_in * 650 + (g_ry[m_in]*120)
    
    # SHATTER GATE PHYSICS (T ~ 0.08)
    pre_shatter = pr_in < 0.5
    pc[m_in] = np.where(pre_shatter[:, None], C_BIO_RAW, C_SUPERCRIT)
    ps[m_in] = np.where(pre_shatter, 28.0, 14.0) # Thick drops shatter to fine mist
    pa[m_in] = np.where(pre_shatter, 1.0, 0.7)
    
    # T_0.15 -> 0.45: Uniflow Scavenge & Compression (Left to Right bounded)
    m_cp = (T >= 0.15) & (T < 0.45)
    pr_cp = (T[m_cp] - 0.15) / 0.30
    
    # Dynamic bounding box: Fluid travels from moving L to converging R
    L_bound = l_px + 20
    R_bound = r_px - 20
    
    # Particles sweep from left port to evenly distributed center
    span_x = L_bound + (R_bound - L_bound) * pr_cp
    # Swirl kinetics inside cylinder
    swirl = np.sin(pr_cp * np.pi) * turb[m_cp] * 80
    px[m_cp] = span_x + swirl
    # Height constrains to bore
    py[m_cp] = CY + g_ry[m_cp] * (BORE / 2.0 - 15)
    pc[m_cp] = C_SUPERCRIT
    
    # T_0.45 -> 0.55: HCCI DETONATION (Inner Dead Center)
    m_br = (T >= 0.45) & (T < 0.55)
    pr_br = (T[m_br] - 0.45) / 0.10
    
    # Maintain strict bounding within moving pistons
    px[m_br] = CX + g_rx[m_br] * ((r_px - l_px)/2.0 - 10)
    py[m_br] = CY + g_ry[m_br] * (BORE / 2.0 - 15)
    
    # HCCI Flash Math (Instant volume burn at T=0.5)
    dist_to_flash = 1.0 - (np.abs((T[m_br] - 0.5) / 0.05))
    flash_curve = np.power(dist_to_flash, 2.5) # Extremely sharp spike
    
    pc[m_br] = C_SUPERCRIT * (1-flash_curve[:, None]) + C_FLASH * flash_curve[:, None]
    ps[m_br] = 14.0 + (flash_curve * 40.0) # Expansion pop
    
    # Heavy violet residue immediately post-flash
    post_flash = T[m_br] > 0.5
    pc[m_br] = np.where(post_flash[:, None], C_HCCI_BURN * (flash_curve[:, None]) + C_EXHAUST * (1-flash_curve[:, None]), pc[m_br])
    
    # T_0.55 -> 0.85: Expansion (Power Stroke / ODC Target)
    m_ex = (T >= 0.55) & (T < 0.85)
    pr_ex = (T[m_ex] - 0.55) / 0.30
    px[m_ex] = CX + g_rx[m_ex] * ((r_px - l_px)/2.0 - 10) + pr_ex * 50 # Pushing right
    py[m_ex] = CY + g_ry[m_ex] * (BORE / 2.0 - 15)
    pc[m_ex] = C_EXHAUST
    pa[m_ex] = 0.5 # Clean H20/CO2 is visually thinner
    
    # T_0.85 -> 1.0: Exhaust Manifold
    m_out = T >= 0.85
    pr_out = (T[m_out] - 0.85) / 0.15
    px[m_out] = CX + 400 + (g_rx[m_out]*50) + pr_out*80
    py[m_out] = 1100 - pr_out * 850 + (g_ry[m_out]*100)
    pc[m_out] = C_EXHAUST
    pa[m_out] = (1.0 - pr_out) * 0.5
    ps[m_out] = 30.0 * (1.0 + pr_out) # Dispersion

    rgba = np.column_stack((pc, pa))
    return px, py, ps, rgba, pos_factor

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    global_phase = f / float(TOTAL_FRAMES)
    engine_revs = 10.0 # 10 full strokes in 10s
    e_tot = global_phase * engine_revs
    e_mod = e_tot % 1.0

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)
    ax.set_xlim(0, 1080); ax.set_ylim(-150, 1850)

    # 1. SOLVE KINEMATICS & TENSORS
    l_px, r_px, pos_factor, velocity = get_kinematics(e_mod)
    
    T_array = (offsets + (e_tot)) % 1.0
    px, py, ps, rgba, p_fac = get_fluid_state(T_array, l_px, r_px, pos_factor)

    # 2. RENDER THE HARDWARE BOUNDING BOX
    # Main Cast Housing
    ax.add_patch(Rectangle((CX - CYL_EXTENT/2, CY - BORE/2 - 60), CYL_EXTENT, BORE + 120, facecolor='#F2F4F4', edgecolor='none', zorder=1))
    
    # Internal Machined Steel Sleeve (The Cylinder)
    ax.plot([CX - CYL_EXTENT/2, CX + CYL_EXTENT/2], [CY + BORE/2, CY + BORE/2], color=C_STEEL, lw=16, solid_capstyle='round', zorder=20)
    ax.plot([CX - CYL_EXTENT/2, CX + CYL_EXTENT/2], [CY - BORE/2, CY - BORE/2], color=C_STEEL, lw=16, solid_capstyle='round', zorder=20)

    # Ports
    # Intake Track (Left Top)
    ax.plot([CX - 420, CX - 420], [CY + BORE/2, 1750], color=C_STEEL, lw=14, zorder=18)
    ax.plot([CX - 300, CX - 300], [CY + BORE/2, 1750], color=C_STEEL, lw=14, zorder=18)
    ax.add_patch(Polygon([[CX - 420, CY + BORE/2], [CX - 300, CY + BORE/2], [CX - 300, 1750], [CX - 420, 1750]], facecolor='#F2F4F4', zorder=2))
    
    # The Supercritical Shatter Gate (Heat Exchanger Grid)
    gate_y = 1450
    ax.add_patch(Rectangle((CX - 410, gate_y - 20), 100, 40, facecolor=C_BG, edgecolor=C_STEEL, lw=6, zorder=18))
    for gy in range(gate_y - 15, gate_y + 16, 10):
        ax.plot([CX - 410, CX - 310], [gy, gy], color=C_SUPERCRIT, lw=4, alpha=0.9, zorder=19) # Glowing titanium heater elements

    # Exhaust Track (Right Down)
    ax.plot([CX + 350, CX + 350], [CY - BORE/2, 250], color=C_STEEL, lw=14, zorder=18)
    ax.plot([CX + 470, CX + 470], [CY - BORE/2, 250], color=C_STEEL, lw=14, zorder=18)
    ax.add_patch(Polygon([[CX + 350, CY - BORE/2], [CX + 470, CY - BORE/2], [CX + 470, 250], [CX + 350, 250]], facecolor='#F2F4F4', zorder=2))

    # 3. FARADAY LINEAR ALTERNATOR COILS
    flux_intensity = np.clip(np.abs(velocity) * 1.5, 0, 1.0) # Lights up purely based on kinematic velocity

    coils_l = []
    coils_r = []
    for cx_o in np.linspace(CX - 120, CX - 380, 8):
        coils_l.append(cx_o)
    for cx_o in np.linspace(CX + 120, CX + 380, 8):
        coils_r.append(cx_o)

    for cx_idx in coils_l + coils_r:
        # Top Coils
        col_t = C_COPPER if flux_intensity < 0.1 else '#C39BD3' if np.random.rand() > 0.5 else C_FLUX
        c_a = 1.0 if flux_intensity < 0.1 else 0.8 + flux_intensity * 0.2
        ax.add_patch(Rectangle((cx_idx - 10, CY + BORE/2 + 20), 20, 40, facecolor=col_t, edgecolor=C_TEXT, lw=3, alpha=c_a, zorder=22))
        ax.add_patch(Rectangle((cx_idx - 10, CY - BORE/2 - 60), 20, 40, facecolor=col_t, edgecolor=C_TEXT, lw=3, alpha=c_a, zorder=22))
        
        # Plasma induction arcs
        if flux_intensity > 0.3:
            ax.plot([cx_idx, cx_idx], [CY + BORE/2 + 65, CY + BORE/2 + 65 + flux_intensity*40], color=C_FLUX, lw=3, alpha=flux_intensity, zorder=23)

    # 4. RENDER FLUID TENSOR
    ax.scatter(px, py, s=ps, color=rgba, edgecolors='none', zorder=10)
    
    # HCCI Flash Illuminator
    if 0.48 <= e_mod <= 0.52:
        flash_prog = 1.0 - np.abs((e_mod - 0.5) / 0.02)
        ax.add_patch(Circle((CX, CY), BORE/2 * 1.1, facecolor='#FFFFFF', alpha=float(flash_prog*0.6), zorder=20))
        ax.add_patch(Circle((CX, CY), BORE/2 * 1.8, facecolor=C_HCCI_BURN, alpha=float(flash_prog*0.3), zorder=21))

    # 5. THE ACTUATORS (Free-Floating Magnetic Pistons)
    # Left Piston
    ax.add_patch(Rectangle((l_px - PISTON_L, CY - BORE/2 + 4), PISTON_L, BORE - 8, facecolor=C_TITANIUM, edgecolor=C_TEXT, lw=6, zorder=15))
    # Right Piston
    ax.add_patch(Rectangle((r_px, CY - BORE/2 + 4), PISTON_L, BORE - 8, facecolor=C_TITANIUM, edgecolor=C_TEXT, lw=6, zorder=15))

    # Piston Specular geometry
    for p_edge in [l_px - PISTON_L + 20, r_px + 20]:
        ax.plot([p_edge, p_edge], [CY - BORE/2 + 20, CY + BORE/2 - 20], color='#FFFFFF', lw=8, alpha=0.3, zorder=16)

    # 6. DIAGNOSTIC TELEMETRY GRAPH & WIDGET (The Computational Demon)
    ax.add_patch(Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, facecolor=C_BG, edgecolor=C_TITANIUM, lw=4, clip_on=False, zorder=80))
    ax.text(0.5, 0.965, "LG-278 :: SUPERCRITICAL OP-HCCI TENSOR [DAYLIGHT]", transform=ax.transAxes, color=C_TITANIUM, fontsize=15, fontname='monospace', weight='bold', ha='center', va='center', zorder=81)

    # Real-time Graph Box
    gy_base = 0.05
    ax.add_patch(Rectangle((0, 0), 1, 0.18, transform=ax.transAxes, facecolor=C_BG, edgecolor=C_STEEL, lw=4, zorder=80))
    ax.text(0.05, 0.15, f"THERMODYNAMIC HCCI CYCLE: {int(e_tot):02d}", transform=ax.transAxes, color=C_TITANIUM, fontsize=18, fontname='monospace', weight='bold', zorder=81)
    
    v_col = C_FLUX if flux_intensity > 0.2 else C_STEEL
    ax.text(0.95, 0.15, f"INDUCTION FLUX: {int(flux_intensity * 100):03d}%", transform=ax.transAxes, color=v_col, fontsize=18, fontname='monospace', weight='bold', ha='right', zorder=81)

    # Tracing the Kinetic Velocity Graph
    x_hist = np.linspace(0, 1.0, 120)
    y_hist = np.zeros(120)
    for i, xh in enumerate(x_hist):
        # Reverse trace history mathematically
        hist_e_tot = e_tot - (1.0 - xh)
        h_mod = hist_e_tot % 1.0
        _, _, _, h_vel = get_kinematics(h_mod)
        y_hist[i] = np.abs(h_vel) * 0.08 # Scale to graph height
    
    # Plot graph lines via TransAxes coordinates
    gx_px = 0.05 + x_hist * 0.9
    gy_py = gy_base + y_hist
    ax.plot(gx_px, gy_py, transform=ax.transAxes, color=C_TITANIUM, lw=3, zorder=82)
    ax.fill_between(gx_px, gy_base, gy_py, transform=ax.transAxes, color=C_FLUX, alpha=0.4, zorder=81)
    
    # Leading edge scanline dot
    ax.scatter([gx_px[-1]], [gy_py[-1]], transform=ax.transAxes, color=C_HCCI_BURN, s=150, zorder=83)
    ax.plot([gx_px[-1], gx_px[-1]], [gy_base, gy_py[-1]], transform=ax.transAxes, color=C_HCCI_BURN, lw=2, linestyle='--', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 278: SUPERCRITICAL HCCI FREE-PISTON [DAYLIGHT PROTOCOL] [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: O(1) Linear Alternator // Absolute HCCI Flash")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            pass
    print("Compilation Complete. Absolute Ouroboros Array inserted.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
