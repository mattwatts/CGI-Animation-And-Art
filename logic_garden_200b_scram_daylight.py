"""
SOVEREIGN CODE: logic_garden_200b_scram_daylight.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Cinematic Fluid & Geometry Tensor
SCENE: LG-200b (The SCRAM Tensor / Daylight Realism)
HOTFIX: Exact Seamless Phase Math, Macro-Orthographic Engineering Render
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 10.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_200b_scram_daylight"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST ENGINEERING PALETTE --------
C_BG        = '#FFFFFF'        # Absolute White Daylight Array
C_ZIRC      = '#BDC3C7'        # Zirconium Alloy Cladding
C_URANIUM   = '#7F8C8D'        # Ceramic Fuel Pellets
C_BORON     = '#1C2833'        # Dark Control Rod Material
C_STEEL     = '#95A5A6'        # Structural Guide Tubes
C_ALARM     = '#C0392B'        # Critical Prompt Red

# Coolant Thermodynamics (Cherenkov / Boiling spectrum)
C_FLUID_COLD = np.array([0.10, 0.30, 0.60])   # Deep Sapphire Coolant
C_FLUID_HOT  = np.array([0.00, 1.00, 1.00])   # High-Excitation Cyan
C_FLUID_BOIL = np.array([1.00, 1.00, 1.00])   # Photic Whiteout

N_FLUID = 30000

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE MACRO REACTOR CROSS-SECTION
# ------------------------------------------------------------------
# We calculate horizontal component mapping algorithmically (Left to Right)
start_x = 240
elements = [
    ('FUEL',  70), ('FLUID', 60), ('CTRL',  50), ('FLUID',  60),
    ('FUEL',  70), ('FLUID', 60), ('CTRL',  50), ('FLUID',  60), ('FUEL', 70)
]

# Map exact geometric bounds for rendering
fuel_spans = []
ctrl_spans = []
fluid_spans = []
curr_x = start_x

for etype, ewidth in elements:
    span = (curr_x, curr_x + ewidth)
    if etype == 'FUEL': fuel_spans.append(span)
    elif etype == 'CTRL': ctrl_spans.append(span)
    elif etype == 'FLUID': fluid_spans.append(span)
    curr_x += ewidth

Y_CORE_TOP = 1700
Y_CORE_BOT = 200

# ------------------------------------------------------------------
# O(1) FLUID PRE-ALLOCATION & TENSOR PRE-COMPUTATION
# ------------------------------------------------------------------
np.random.seed(200)

rod_y_array = np.zeros(TOTAL_FRAMES)
heat_array = np.zeros(TOTAL_FRAMES)
vel_array = np.zeros(TOTAL_FRAMES)

# Phase Mathematics (The Seamless 10s Timeline)
for i in range(TOTAL_FRAMES):
    ph = i / float(TOTAL_FRAMES)
    
    # KINEMATIC ROD DROP LOGIC
    # 0.0 - 0.2: Extracting (y = 1000 to y = 2000)
    # 0.2 - 0.6: Suspended/Slow creep (y = 2000 to y = 2100)
    # 0.6 - 0.65: SCRAM (Gravity Drop to y = 300)
    # 0.65 - 0.9: Seated/Quenched (y = 300)
    # 0.9 - 1.0: Retraction prep (y=300 to y=1000)
    if ph < 0.2:
        r = np.interp(ph, [0.0, 0.2], [1000, 2000])
    elif ph < 0.6:
        r = np.interp(ph, [0.2, 0.6], [2000, 2100])
    elif ph < 0.65:
        # Gravity ballistic curve
        p_fall = (ph - 0.6) / 0.05
        r = 2100 - (1800 * (p_fall**2))
    elif ph < 0.9:
        r = 300
    else:
        p_up = (ph - 0.9) / 0.1
        r = 300 + (700 * (p_up**2))
    rod_y_array[i] = r

# THERMODYNAMIC HEAT LOGIC
# Calculate raw target heat based purely on rod position
for i in range(TOTAL_FRAMES):
    h = np.clip((rod_y_array[i] - 1000) / 1000.0, 0.0, 1.0)
    if rod_y_array[i] > 1900:  # Exponential runaway at peak extraction
        h += (rod_y_array[i] - 1900) / 200.0
    heat_array[i] = np.clip(h, 0.0, 1.0)

# Smooth thermodynamic mass (Lag simulation via Convolution)
kernel = np.ones(15) / 15.0
for _ in range(4):
    heat_array = np.convolve(np.tile(heat_array, 3), kernel, mode='same')[TOTAL_FRAMES:2*TOTAL_FRAMES]

# VELOCITY & DISTANCE INTEGRATION (To ensure PERFECT Modulo wrapping)
vel_array = 8.0 + (heat_array * 35.0)
raw_dist = np.cumsum(vel_array)

# To perfectly wrap fluid at frame 600, the last distance MUST equal an exact integer multiple of 1920
WRAP_TARGET = 1920.0
total_sweeps = np.round(raw_dist[-1] / WRAP_TARGET)
scale_factor = (total_sweeps * WRAP_TARGET) / raw_dist[-1]
fluid_dist_array = raw_dist * scale_factor  # This array is now indestructible math

# FLUID BASE COORDS
f_x = np.zeros(N_FLUID)
f_y = np.random.uniform(0, WRAP_TARGET, N_FLUID)
# Distribute particles perfectly inside the 4 fluid cavities
particles_per_channel = N_FLUID // len(fluid_spans)
for idx, (lx, rx) in enumerate(fluid_spans):
    start = idx * particles_per_channel
    end = start + particles_per_channel
    f_x[start:end] = np.random.uniform(lx + 2, rx - 2, particles_per_channel)

# Handle remainder
if len(f_x) < N_FLUID:
    f_x[-(N_FLUID-len(f_x)):] = np.random.uniform(fluid_spans[-1][0]+2, fluid_spans[-1][1]-2, N_FLUID-len(f_x))
f_offset = np.random.uniform(-0.5, 0.5, N_FLUID) # X-wobble seeds

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    fig.patch.set_facecolor(C_BG)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    # Global State Tensors
    curr_heat = heat_array[f]
    curr_rod  = rod_y_array[f]
    curr_dist = fluid_dist_array[f]

    # 1. RENDER FUEL BUNDLE (ZIRCONIUM STRUCTURAL CLADDING)
    for (lx, rx) in fuel_spans:
        width = rx - lx
        ax.add_patch(Rectangle((lx, Y_CORE_BOT-100), width, Y_CORE_TOP, facecolor=C_BG, edgecolor=C_ZIRC, lw=6, zorder=10))
        # Uranium Pellet Stack Emulation (Machined ribs)
        for y_pellet in range(Y_CORE_BOT, Y_CORE_TOP, 15):
            ax.plot([lx+6, rx-6], [y_pellet, y_pellet], color=C_URANIUM, lw=2, alpha=0.6, zorder=11)
            # Specular Cladding Highlight
            ax.plot([lx+15, lx+15], [Y_CORE_BOT, Y_CORE_TOP], color='#FFFFFF', lw=8, alpha=0.8, zorder=12)

    # 2. RENDER CONTROL ROD CHANNELS (EMPTY GUIDE TUBES)
    for (lx, rx) in ctrl_spans:
        width = rx - lx
        cx = (lx + rx) / 2.0
        ax.add_patch(Rectangle((lx, Y_CORE_BOT-100), width, Y_CORE_TOP+200, facecolor=C_BG, edgecolor=C_STEEL, lw=4, zorder=15))
        # Internal hollow shadow indication
        ax.add_patch(Rectangle((lx+4, Y_CORE_BOT-90), width-8, Y_CORE_TOP+180, facecolor='#E5E8E8', zorder=16))

        # RENDER DYNAMIC BORON CONTROL RODS INSIDE GUIDES
        ax.add_patch(Rectangle((lx+6, curr_rod), width-12, 1800, facecolor=C_BORON, edgecolor=C_ZIRC, lw=2, zorder=17))
        # Chamfered Aerodynamic Tip
        ax.add_patch(Polygon([(lx+6, curr_rod), (rx-6, curr_rod), (rx-15, curr_rod-25), (lx+15, curr_rod-25)], facecolor=C_BORON, zorder=17))
        # Machined Rod Highlight
        ax.plot([lx+14, lx+14], [curr_rod, 1920], color='#FFFFFF', lw=4, alpha=0.3, zorder=18)

    # 3. RENDER O(N) THERMODYNAMIC HYDRAULIC MATRIX
    # Fluid shifts exactly based on the seamlessly scaled integral distance array
    calc_y = (f_y + curr_dist) % WRAP_TARGET
    # Heat causes particles to vibrate laterally
    calc_x = f_x + (f_offset * curr_heat * 12.0)

    # Dynamic Cherenkov Vector Mapping
    if curr_heat < 0.5:
        p = curr_heat / 0.5
        c_rgb = C_FLUID_COLD * (1-p) + C_FLUID_HOT * p
    else:
        p = (curr_heat - 0.5) / 0.5
        c_rgb = C_FLUID_HOT * (1-p) + C_FLUID_BOIL * p

    # Array Broadcasting
    rgba = np.zeros((N_FLUID, 4))
    rgba[:, :3] = c_rgb
    rgba[:, 3] = np.clip(0.4 + (curr_heat * 0.4), 0, 1) # Hotter = thicker opacity
    
    # Boil Expansion size mechanics
    p_size = 12.0 + (curr_heat * 25.0)

    # Scatter Matrix (Clipped to visually exist behind the framing if needed, but here it flows continuously)
    valid_fluid = (calc_y > 100) & (calc_y < 1850)
    ax.scatter(calc_x[valid_fluid], calc_y[valid_fluid], s=p_size, color=rgba[valid_fluid], edgecolors='none', zorder=5)

    # 4. HARDWARE ALARMS & DIAGNOSTIC TELEMETRY
    ax.add_patch(Rectangle((0, 1840), 1080, 80, facecolor=C_ZIRC, zorder=50))
    ax.text(40, 1880, "LG-200b: MACRO CROSS-SECTION // CORE SCRAM TENSOR", color=C_BG, fontsize=18, fontname='monospace', weight='bold', va='center', zorder=51)

    # UI Baseplate
    ax.add_patch(Rectangle((0, 0), 1080, 110, facecolor=C_ZIRC, zorder=50))

    if curr_heat > 0.95 and (f % 10 < 5):
        # Local Photic Alarm Flash
        ax.add_patch(Rectangle((20, 20), 1040, 70, facecolor=C_ALARM, zorder=51))
        txt_col, hud_col = C_BG, C_BG
        status = "CRITICAL PROMPT CASCADE DETECTED"
    elif curr_rod < 1800 and curr_heat > 0.8:
        txt_col, hud_col = C_ALARM, C_ALARM
        status = "SCRAM DEPLOYED: MATHEMATICAL OVERRIDE"
    else:
        txt_col, hud_col = C_BORON, C_URANIUM
        status = "THERMAL HYDRODYNAMICS NOMINAL"

    ax.text(40, 55, f"STATUS: {status}", color=txt_col, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=52)
    
    # K-Effective Sub-Bar
    ax.add_patch(Rectangle((700, 30), 340, 20, facecolor=C_BG, zorder=52))
    k_bar_w = 340 * np.clip(curr_heat + 0.1, 0, 1)
    ax.add_patch(Rectangle((700, 30), k_bar_w, 20, facecolor=txt_col, zorder=53))
    ax.text(700, 70, f"THERMODYNAMIC K-EFF: {1.0 + (curr_heat-0.5)*0.8:0.2f}", color=txt_col, fontsize=14, fontname='monospace', zorder=52)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-200b SCRAM DAYLIGHT TENSOR [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Orthographic Engineering Realism // O(1) Fluid Modulo Wrap")

    with mp.Pool(processes=cpu_cores) as pool:
        frames = range(TOTAL_FRAMES)
        for finished_frame in pool.imap_unordered(render_frame, frames, chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")
    print("Compilation Complete. Absolute Geometry Asserted. Runaway Terminated.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
