"""
SOVEREIGN CODE: logic_garden_139b_transistor_daylight.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Eulerian Phase Tensor
SCENE: LG-139b (Field-Effect Transistor / Solid-State Emulation / Daylight Protocol)
HOTFIX: True Depletion Geometry, Streamline Velocity Integration, Flawless Ouroboros Loop
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
OUT_DIR = "frames_139b_transistor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST ENGINEERING PALETTE --------
C_BG        = '#FFFFFF'
C_IRON      = '#1C2833'        # Hard Machined Engine Limits
C_SILICON   = '#EAEDED'        # N-Type Conductive Matrix Base 
C_PSUB      = '#F8F9F9'        # P-Type Substrate Bulk
C_DEPLETION = '#85929E'        # Insulating Depletion Barrier
C_GATE      = '#D4AC0D'        # Gold Terminal Contacts
C_TEXT      = '#111111'

# Thermodynamics
C_AZURE     = np.array([0.20, 0.60, 0.86]) # Perfect Laminar Flow (Cold)
C_MAGENTA   = np.array([0.90, 0.18, 0.23]) # Bottleneck Friction (Hot)

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY & O(1) STREAMLINE MATRICES
# ------------------------------------------------------------------
N_ELECTRONS = 25000

np.random.seed(139)
# Parametric lifespan tracking (0.0 to 1.0)
offsets = np.random.rand(N_ELECTRONS)
# Streamline mapping (Gaussian distribution for physical current density)
# Spread concentrates flow near center, cleanly bounded to edges
stream_x = np.clip(np.random.normal(0, 0.45, N_ELECTRONS), -0.98, 0.98) 

# Structure Bounds
Y_START = 1800.0
Y_END   = 200.0
Y_LEN   = Y_START - Y_END
CX      = 540.0
R_MAX   = 170.0 # Maximum radius of the conductive channel
R_MIN   = 5.0   # Absolute Pinch-off geometry (near zero to halt flow)

# ------------------------------------------------------------------
# RIGID 4-STATE KINEMATIC INTEGRATION (The Temporal Pulse)
# ------------------------------------------------------------------
# We calculate the continuous, exact mathematical distance the fluid 
# has traveled based on the gate voltage waveform.
T_arr = np.linspace(0, 1, TOTAL_FRAMES, endpoint=False)

# Waveform S(t): Perfectly symmetrical voltage pulse from 0 -> 1 -> 0
S_gate = np.clip(1.5 * np.sin(np.pi * 2 * (T_arr - 0.25)) + 0.5, 0, 1)

# Flow Velocity corresponds squarely to the openness of the gate
V_flow = S_gate ** 2 

# Eulerian Integral for exact spatial alignment
# Ensures Frame 0 equates seamlessly to Frame 600 
cum_flow = np.zeros(TOTAL_FRAMES)
for i in range(1, TOTAL_FRAMES):
    cum_flow[i] = cum_flow[i-1] + V_flow[i-1]

# Force exact macroscopic looping wrapping
total_integral = cum_flow[-1] + V_flow[-1]
LOOPS_PER_CYCLE = 2.0 
cum_flow = cum_flow * (LOOPS_PER_CYCLE / total_integral)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    phase = f / float(TOTAL_FRAMES)
    s_val = S_gate[f]

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    fig.patch.set_facecolor(C_BG)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    # 1. P-SUBSTRATE BASEPLATE & STRUCTURAL WALLS
    ax.add_patch(Rectangle((200, 200), 170, 1600, facecolor=C_PSUB, edgecolor='none', zorder=1))
    ax.add_patch(Rectangle((710, 200), 170, 1600, facecolor=C_PSUB, edgecolor='none', zorder=1))
    ax.plot([200, 200], [200, 1800], color=C_IRON, lw=16, zorder=20)
    ax.plot([880, 880], [200, 1800], color=C_IRON, lw=16, zorder=20)

    # N-Channel Source/Drain Zones
    ax.plot([370, 370], [1800, 1300], color=C_IRON, lw=12, zorder=20)
    ax.plot([710, 710], [1800, 1300], color=C_IRON, lw=12, zorder=20)
    ax.plot([370, 370], [700, 200], color=C_IRON, lw=12, zorder=20)
    ax.plot([710, 710], [700, 200], color=C_IRON, lw=12, zorder=20)

    # 2. EVALUATING THE GATE PINCH & DEPLETION GEOMETRY
    # The physical radius of the channel at the exact gate choke-point
    r_choke = R_MIN + (R_MAX - R_MIN) * s_val

    # Pre-compute the spatial shape of the depletion region down the Y axis
    # Forms a symmetric hourglass contour matching electric field distributions
    curve_y = np.linspace(Y_END, Y_START, 200)
    p_pinch = np.exp(-((curve_y - 1000) / 180.0)**2)  # Gaussian probability density
    r_local_curve = R_MAX - p_pinch * (R_MAX - r_choke)

    # Extract polygon architectures for visual representation
    left_bound = 540 - r_local_curve
    left_pts = [(370, Y_END)] + list(zip(left_bound, curve_y)) + [(370, Y_START)]
    ax.add_patch(Polygon(left_pts, facecolor=C_DEPLETION, hatch='////', edgecolor=C_IRON, lw=4, zorder=18))

    right_bound = 540 + r_local_curve
    right_pts = [(710, Y_END)] + list(zip(right_bound, curve_y)) + [(710, Y_START)]
    ax.add_patch(Polygon(right_pts, facecolor=C_DEPLETION, hatch='\\\\\\\\', edgecolor=C_IRON, lw=4, zorder=18))

    # 3. GOLD GATE TERMINALS (The Imposed Voltage)
    # The gate is visually saturated based on the driving waveform
    alpha_gate = max(0.1, s_val * 0.9)
    ax.add_patch(Rectangle((300, 800), 70, 400, facecolor=C_GATE, alpha=alpha_gate, edgecolor='none', zorder=17))
    ax.add_patch(Rectangle((300, 800), 70, 400, facecolor='none', edgecolor=C_IRON, lw=6, zorder=19))
    
    ax.add_patch(Rectangle((710, 800), 70, 400, facecolor=C_GATE, alpha=alpha_gate, edgecolor='none', zorder=17))
    ax.add_patch(Rectangle((710, 800), 70, 400, facecolor='none', edgecolor=C_IRON, lw=6, zorder=19))

    # 4. PARTICLE PHYSICS: O(1) FLUID TENSOR
    # Particles only advance when fluid is moving. Modulo array assures perfect loop resets.
    y_norm = (offsets + cum_flow[f]) % 1.0
    px = np.zeros(N_ELECTRONS)
    py = Y_START - y_norm * Y_LEN
    
    # Mathematical integration matching the fluid volume exactly to the bottleneck contour
    p_particle = np.exp(-((py - 1000) / 180.0)**2)
    r_particle = R_MAX - p_particle * (R_MAX - r_choke)
    
    # Align particle layout geometrically inside the constraints
    px = CX + stream_x * r_particle

    # Thermal Stress Visualization (Visual Fluid Friction)
    # Fluid squeezed tightest turns violently hot/magenta
    squeeze_metric = (R_MAX - r_particle) / R_MAX
    
    pc = np.zeros((N_ELECTRONS, 3))
    # Scalar broadcast interpolation
    pc[:] = C_AZURE * (1.0 - squeeze_metric[:, None]) + C_MAGENTA * squeeze_metric[:, None]
    
    pa = np.clip(0.6 + squeeze_metric * 0.4, 0, 1) # Hotter = Brighter
    rgba = np.column_stack((pc, pa))
    
    # Velocity expansion (Higher squeeze = visually smaller objects simulating faster traversal)
    ps = np.clip(25.0 - squeeze_metric * 15.0, 5.0, 25.0)

    # Single pass scatter deployment
    ax.scatter(px, py, s=ps, color=rgba, edgecolors='none', zorder=15)

    # 5. INDUSTRIAL UI & READOUT BARS
    ax.add_patch(Rectangle((0, 1840), 1080, 80, facecolor=C_BG, zorder=50))
    ax.text(40, 1880, "LG-139b: O(1) FIELD-EFFECT TRANSISTOR // TRUE SOLID-STATE DAYLIGHT", color=C_IRON, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=51)

    state_str = "CUT-OFF (P-N JUNCTION PINCH)"
    text_color = '#C0392B' # Red Warning
    if s_val > 0.8:
        state_str = "SATURATION (LAMINAR FLUID FLOW)"
        text_color = '#2980B9'
    elif s_val > 0.1:
        state_str = "PHASE TRANSITION (MODULATING)"
        text_color = '#D4AC0D'
        
    ax.add_patch(Rectangle((0, 0), 1080, 140, facecolor=C_BG, zorder=50))
    ax.add_patch(Rectangle((0, 140), 1080, 2, facecolor=C_IRON, zorder=51))
    
    v_volt = s_val * 5.0
    c_cond = s_val * 99.8 # Simulated Siemens conductivity
    
    ax.text(40, 95, f"SYSTEM LOGIC: {state_str}", color=text_color, fontsize=20, fontname='monospace', weight='bold', va='center', zorder=51)
    ax.text(40, 45, f"V_GATE: {v_volt:04.2f} V     CHANNEL COND: {c_cond:04.1f} S/m", color=C_TEXT, fontsize=20, fontname='monospace', weight='bold', va='center', zorder=51)

    # Component Tags
    ax.text(540, 1740, "SOURCE (+)", color=C_BG, fontsize=14, fontname='monospace', weight='bold', ha='center', zorder=50)
    ax.text(540, 260, "DRAIN (-)", color=C_BG, fontsize=14, fontname='monospace', weight='bold', ha='center', zorder=50)
    ax.text(260, 1000, "- Vg -", color=C_BG, rotation=90, fontsize=14, fontname='monospace', weight='bold', ha='center', va='center', zorder=50)
    ax.text(820, 1000, "- Vg -", color=C_BG, rotation=-90, fontsize=14, fontname='monospace', weight='bold', ha='center', va='center', zorder=50)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-139b: TRUE SOLID-STATE TRANSISTOR [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Continuous Fluid Topology // Modulo P-N Depletion Boundaries")

    with mp.Pool(processes=cpu_cores) as pool:
        frames = range(TOTAL_FRAMES)
        for finished_frame in pool.imap_unordered(render_frame, frames, chunksize=8):
            pass
    print("Compilation Complete. Solid-State Limits Locked.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
