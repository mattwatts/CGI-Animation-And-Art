"""
SOVEREIGN CODE: logic_garden_27b_ramjet_daylight.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Eulerian Streamline Tensor
SCENE: LG-27b (J58 Turboramjet / Daylight Protocol)
HOTFIX: Seamless 10s Mach Cycle, Translating Shock Cone, Mach Diamonds
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Wedge, Circle
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 10.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_27b_ramjet_daylight"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST ENGINEERING PALETTE --------
C_BG        = '#FFFFFF'        
C_TITANIUM  = '#1C2833'        # Dark Aero Skin / Spike / Cowls
C_STEEL     = '#7F8C8D'        # Machined Engine Core / Compressor
C_ALUM      = '#EAEDED'        # Cast Housing Enclosures
C_GOLD      = '#B4931C'        # High-Temp Bypass Ducts
C_GRID      = '#BDC3C7'        # Telemetry Bounds
C_TEXT      = '#111111'        

C_AIR_COLD  = np.array([0.0, 0.8, 1.0])    # M=1.0 Intake
C_AIR_COMP  = np.array([0.9, 0.4, 0.0])    # Compressed Ram Air (Orange)
C_BURN      = np.array([1.0, 1.0, 0.9])    # White-hot Core Burn
C_PLUME     = np.array([0.9, 0.1, 0.15])   # Kerosene Supersonic Exhaust
C_SHOCK     = '#ff1a1a'                    # Oblique/Normal Shock Visualizer

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE KINEMATIC CAMERA & O(1) WRAP MATRIX
# ------------------------------------------------------------------
CX = 540
CY_TIP_MAX = 1700
CY_COWL = 1400
CY_COMP = 1100
CY_BURN = 700
CY_NOZ = 400
CY_PLUME_END = -400

N_GAS = 28000
WRAP_LEN = 2400.0  # Particle wrap domain: roughly Y=1800 down to -600

# ------------------------------------------------------------------
# PRE-CALCULATED EXACT INTEGRATION FOR FLAWLESS LOOP
# ------------------------------------------------------------------
# Mach goes from 1.0 -> 3.2 -> 1.0 over 10 seconds.
# We map Phase via: M(t) = 2.1 - 1.1 * cos(2*pi*phase)
mach_array = 2.1 - 1.1 * np.cos(2 * np.pi * np.linspace(0, 1, TOTAL_FRAMES, endpoint=False))
v_base = 60.0 * mach_array  # Velocity scales with M

# To achieve a seamless loop, the sum of velocity over all frames MUST be 
# exactly an integer multiple of the WRAP_LEN.
raw_sum = np.sum(v_base)
target_sum = round(raw_sum / WRAP_LEN) * WRAP_LEN
v_corr = v_base * (target_sum / raw_sum)

# Ouroboros Distance Lookup Table
cum_dist = np.insert(np.cumsum(v_corr), 0, 0.0)

np.random.seed(27)
base_y = np.random.uniform(-400, 2000, N_GAS)
# Local streamline index: -1.0 (left) to 1.0 (right)
stream_x = np.random.uniform(-1, 1, N_GAS)
# Noise arrays for turbulence
turb_x = np.random.normal(0, 1, N_GAS)
turb_size = np.random.uniform(0.5, 1.5, N_GAS)

# ------------------------------------------------------------------
# EULERIAN KINEMATICS & ROUTING
# ------------------------------------------------------------------
def calculate_streamlines(y_arr, local_x, M, spike_y):
    """Maps a 1D streamline identity into exact absolute X,Y layout based on physics."""
    x_out = np.zeros_like(y_arr)
    c_out = np.zeros((len(y_arr), 3))
    s_out = np.ones_like(y_arr) * 12.0
    a_out = np.ones_like(y_arr) * 0.8
    
    # Physics scalars
    ram_prog = np.clip((M - 1.5) / 1.7, 0, 1) # 0 at M=1.5, 1 at M=3.2
    
    # 1. FREE STREAM (Above Cowl)
    m1 = y_arr > CY_COWL
    if np.any(m1):
        x_out[m1] = CX + local_x[m1] * 220
        # Flow narrows slightly near spike tip
        prog = np.clip((y_arr[m1] - CY_COWL) / (spike_y - CY_COWL), 0, 1)
        x_out[m1] = CX + local_x[m1] * (160 + prog * 60)
        c_out[m1] = C_AIR_COLD
        
    # 2. INLET THROAT (Spike Body pushing air outward)
    m2 = (y_arr <= CY_COWL) & (y_arr > CY_COMP)
    if np.any(m2):
        prog = (y_arr[m2] - CY_COMP) / (CY_COWL - CY_COMP)  # 1 at cowl, 0 at comp
        # Throat width narrows 
        outer_r = 160 - (1-prog)*20
        # Spike radius dictates inner boundary
        inner_r = np.clip(100 * ((y_arr[m2] - (spike_y - 300)) / 300.0), 0, 100) 
        
        # Route logic via streamline index
        sign = np.sign(local_x[m2])
        x_out[m2] = CX + sign * (inner_r + (outer_r - inner_r) * np.abs(local_x[m2]))
        # Heating dynamically due to compression
        c_out[m2] = C_AIR_COLD * (1-ram_prog) + C_AIR_COMP * ram_prog

    # 3. ENGINE CORE & BYPASS ROUTING
    m3 = (y_arr <= CY_COMP) & (y_arr > CY_BURN)
    if np.any(m3):
        # By M=2.5, 80% of outer air diverts into ramjet bypass tubes.
        valve_open = ram_prog 
        is_bypass = np.abs(local_x[m3]) > 0.4
        
        sign = np.sign(local_x[m3])
        # Core Path (Inner 40%)
        x_core = CX + sign * 60 * (np.abs(local_x[m3])/0.4)
        # Bypass Path (Outer 60%)
        x_byp = CX + sign * (140 + 40 * ((np.abs(local_x[m3])-0.4)/0.6))
        
        # Dynamic blending based on Mach Valve state
        route_bypass = is_bypass & (np.random.rand(np.sum(m3)) < valve_open)
        m3_byp = np.zeros_like(m3); m3_byp[m3] = route_bypass
        m3_core = np.zeros_like(m3); m3_core[m3] = ~route_bypass
        
        x_out[m3_core] = x_core[~route_bypass]
        c_out[m3_core] = C_BURN # Turbojet Core is always hot
        s_out[m3] = 8.0 # Narrower density
        
        x_out[m3_byp] = x_byp[route_bypass]
        c_out[m3_byp] = C_AIR_COMP # Bypass air is strictly ram compressed heat
        
    # 4. AFTERBURNER & NOZZLE (Rejoin)
    m4 = (y_arr <= CY_BURN) & (y_arr > CY_NOZ)
    if np.any(m4):
        prog = (y_arr[m4] - CY_NOZ) / (CY_BURN - CY_NOZ) # 1 at burn, 0 at nozzle
        outer_r = 180 * prog + 90 * (1-prog) # Constricts at nozzle throat
        x_out[m4] = CX + local_x[m4] * outer_r
        c_out[m4] = C_BURN * prog[:, None] + C_PLUME * (1-prog[:, None])
        s_out[m4] = 16.0
        
    # 5. SUPERSONIC EXHAUST PLUME
    m5 = y_arr <= CY_NOZ
    if np.any(m5):
        dist_out = CY_NOZ - y_arr[m5]
        # Expanding cone
        base_exp = 90 + dist_out * 0.4
        x_out[m5] = CX + local_x[m5] * base_exp + turb_x[m5] * (dist_out * 0.05)
        c_out[m5] = C_PLUME
        s_out[m5] = 20.0 * turb_size[m5]
        a_out[m5] = np.clip(1.0 - (dist_out / 800.0), 0, 1)

    return x_out, c_out, s_out, a_out

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    phase = f / float(TOTAL_FRAMES)
    M = mach_array[f]
    
    # 1. Kinematic Machinery Constraints
    ram_prog = np.clip((M - 1.5) / 1.7, 0, 1)
    
    # The Spike: Translates 26 scale inches backward (from 1700 to 1480 natively)
    spike_base = CY_COMP + 200
    spike_y = 1700 - ram_prog * 220 
    
    # 2. Setup Figure Matrix
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG); ax.set_facecolor(C_BG)

    # UI Alignment Hotfix: Y runs strictly from -500 to 1800 to avoid label clipping.
    ax.set_xlim(0, 1080); ax.set_ylim(-500, 1850)

    # -------------------------------------------------------------
    # 3. DRAW HARDWARE ARCHITECTURE
    # -------------------------------------------------------------
    # Structural Bypass Tubes & Ramjet Hardware
    tube_color = C_STEEL if ram_prog < 0.1 else C_GOLD
    ax.plot([CX-180, CX-120], [CY_COWL-80, CY_COMP-20], color=tube_color, lw=20, zorder=12, solid_capstyle='round')
    ax.plot([CX+180, CX+120], [CY_COWL-80, CY_COMP-20], color=tube_color, lw=20, zorder=12, solid_capstyle='round')
    ax.add_patch(Rectangle((CX-195, CY_COMP), 60, CY_COWL-CY_COMP-150, facecolor=C_ALUM, edgecolor=C_TITANIUM, lw=4, zorder=10))
    ax.add_patch(Rectangle((CX+135, CY_COMP), 60, CY_COWL-CY_COMP-150, facecolor=C_ALUM, edgecolor=C_TITANIUM, lw=4, zorder=10))

    # Outer Nacelle Skin (Titanium)
    nac_l = Polygon([[CX-160, CY_COWL], [CX-220, CY_COWL-200], [CX-220, CY_BURN+100], [CX-160, CY_NOZ]], facecolor=C_TITANIUM, edgecolor=C_STEEL, lw=4, zorder=20)
    nac_r = Polygon([[CX+160, CY_COWL], [CX+220, CY_COWL-200], [CX+220, CY_BURN+100], [CX+160, CY_NOZ]], facecolor=C_TITANIUM, edgecolor=C_STEEL, lw=4, zorder=20)
    ax.add_patch(nac_l); ax.add_patch(nac_r)
    
    # Engine Core Turbojet Base
    ax.add_patch(Rectangle((CX-80, CY_BURN), 160, CY_COMP-CY_BURN, facecolor=C_STEEL, zorder=21))
    for ring_y in np.linspace(CY_BURN+20, CY_COMP-20, 12):
        ax.plot([CX-80, CX+80], [ring_y, ring_y], color=C_TITANIUM, lw=6, zorder=22) # Compressor stages

    # The Translating Isentropic Spike
    ax.add_patch(Polygon([[CX, spike_y], [CX-90, spike_base], [CX+90, spike_base]], facecolor=C_TITANIUM, edgecolor=C_STEEL, lw=4, zorder=18))
    # Spike Specular Highlight
    ax.plot([CX, CX+40], [spike_y-10, spike_base+20], color='#FFFFFF', lw=6, alpha=0.3, zorder=19)

    # 4. VOLUMETRIC NOZZLE ACTUATORS
    noz_w = 90 + ram_prog * 40 # Nozzle physically expands at high mach
    ax.add_patch(Polygon([[CX-160, CY_NOZ], [CX-noz_w, CY_NOZ-100], [CX+noz_w, CY_NOZ-100], [CX+160, CY_NOZ]], facecolor=C_STEEL, edgecolor=C_TITANIUM, lw=5, zorder=25))
    ax.plot([CX-noz_w-10, CX+noz_w+10], [CY_NOZ-100, CY_NOZ-100], color=C_TITANIUM, lw=8, solid_capstyle='round', zorder=26)

    # -------------------------------------------------------------
    # 5. OBLICQUE SHOCKWAVE VISUALIZER (The "Trap")
    # -------------------------------------------------------------
    if M >= 1.05:
        mu = np.arcsin(1.0 / M)
        # Angles originate symmetrically from spike tip
        sx = 450 * np.sin(mu)
        sy = 450 * np.cos(mu)
        ax.plot([CX, CX-sx], [spike_y, spike_y-sy], color=C_SHOCK, lw=4, alpha=0.8, linestyle='--', zorder=30)
        ax.plot([CX, CX+sx], [spike_y, spike_y-sy], color=C_SHOCK, lw=4, alpha=0.8, linestyle='--', zorder=30)

        # Normal Shock seated in throat during Ramjet mode
        if M > 2.0:
            ax.plot([CX-160, CX-90], [CY_COWL-80, CY_COWL-120], color=C_SHOCK, lw=6, alpha=0.6, zorder=30)
            ax.plot([CX+160, CX+90], [CY_COWL-80, CY_COWL-120], color=C_SHOCK, lw=6, alpha=0.6, zorder=30)

    # -------------------------------------------------------------
    # 6. EXACT O(1) Eulerian Streamline Evaluation
    # -------------------------------------------------------------
    curr_y = (base_y - cum_dist[f]) % WRAP_LEN - 500.0
    px, pc, ps, pa = calculate_streamlines(curr_y, stream_x, M, spike_y)
    
    rgba = np.column_stack((pc, pa))
    ax.scatter(px, curr_y, s=ps, color=rgba, edgecolors='none', zorder=15)

    # -------------------------------------------------------------
    # 7. SUPERSONIC MACH DIAMONDS
    # -------------------------------------------------------------
    if M > 1.2:
        dist = 80 * np.sqrt(M**2 - 1)
        for i in range(1, int(400 // dist) + 2):
            d_y = (CY_NOZ-100) - i * dist
            if d_y > -450:
                ax.add_patch(Circle((CX, d_y), 45 - i*8, facecolor='#FFFFFF', alpha=0.5, zorder=28))
                ax.add_patch(Polygon([[CX, d_y+20], [CX-35, d_y], [CX, d_y-20], [CX+35, d_y]], facecolor='#FFD700', alpha=0.4, zorder=29))

    # -------------------------------------------------------------
    # 8. DIAGNOSTIC TELEMETRY WIDGETS
    # -------------------------------------------------------------
    ax.add_patch(Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, facecolor=C_BG, edgecolor=C_TITANIUM, lw=2, clip_on=False, zorder=80))
    ax.text(0.5, 0.965, "LG-27b :: ISENTROPIC VARIABLE INLET TENSOR", transform=ax.transAxes, color=C_TITANIUM, fontsize=15, fontname='monospace', weight='bold', ha='center', va='center', zorder=81)

    state_str = "TURBOJET CORE INTAKE"
    text_color = '#3498DB'
    if M > 2.0:
        state_str = "RAMJET TRANSITION: BYPASS DOORS OPEN"
        text_color = '#E67E22'

    ax.add_patch(Rectangle((0, 0), 1080, 100, facecolor=C_BG, zorder=80))
    ax.text(50, 50, f"MACH {M:.2f} | {state_str}", color=text_color, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-27b: RAMJET TENSOR [DAYLIGHT PROTOCOL] [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Isentropic Cone Translation // Eulerian Fluid Pipe")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            pass
    print("Compilation Complete. Absolute Ouroboros Array inserted.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
