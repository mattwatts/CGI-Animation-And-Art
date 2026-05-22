"""
SOVEREIGN CODE: logic_garden_141b_mind_tap_daylight.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Eulerian Phase Tensor
SCENE: LG-141b (The Consciousness Tap / Neural Transistor / Daylight Protocol)
HOTFIX: True Laminar Gating, Quantum Decoherence Vectors, Flawless Ouroboros Loop
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
OUT_DIR = "frames_141b_mind_tap"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST ENGINEERING PALETTE --------
C_BG          = '#FFFFFF'
C_IRON        = '#1C2833'       # Hard Machined Core Limits
C_SUBSTRATE   = '#F4F6F7'       # Cortical Bed
C_DEPLETION   = '#85929E'       # Attentional Dampers
C_GATE        = '#D4AC0D'       # Gold Neural Contacts
C_TEXT        = '#111111'

# Thermodynamics of Attention
C_AZURE       = np.array([0.20, 0.60, 0.86]) # Superposition State A
C_PURPLE      = np.array([0.55, 0.27, 0.67]) # Superposition State B
C_MANTIS      = np.array([0.15, 0.68, 0.37]) # Decoherence / Terminal Green Flow

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY & O(1) STREAMLINE MATRICES
# ------------------------------------------------------------------
N_QUANTA = 30000

np.random.seed(141)
offsets = np.random.rand(N_QUANTA)
# Streamlines initialized using normal distribution
raw_x = np.clip(np.random.normal(0, 0.45, N_QUANTA), -0.98, 0.98) 
wave_phase = np.random.rand(N_QUANTA) * 2 * np.pi

# Structure Bounds
Y_START = 1800.0
Y_END   = 200.0
Y_LEN   = Y_START - Y_END
CX      = 540.0
R_MAX   = 220.0 # Wide Entropy State
R_MIN   = 20.0  # Ultra-focused Laminar State

# ------------------------------------------------------------------
# RIGID KINEMATIC INTEGRATION (The Attentional Pulse)
# ------------------------------------------------------------------
T_arr = np.linspace(0, 1, TOTAL_FRAMES, endpoint=False)

# Waveform S(t): Cosine control curve mapping from 0 (Wandering) -> 1 (Locked) -> 0
S_focus = 0.5 - 0.5 * np.cos(T_arr * 2 * np.pi)

# Flow Velocity expands under extreme focus (Conservation of Flow + Willpower)
V_flow = 1.0 + 3.0 * S_focus 

cum_flow = np.zeros(TOTAL_FRAMES)
for i in range(1, TOTAL_FRAMES):
    cum_flow[i] = cum_flow[i-1] + V_flow[i-1]

total_integral = cum_flow[-1] + V_flow[-1]
LOOPS_PER_CYCLE = 3.0 # Fluid will fully cycle the height 3 times over 10s
cum_flow = cum_flow * (LOOPS_PER_CYCLE / total_integral)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    phase = f / float(TOTAL_FRAMES)
    s_val = S_focus[f]

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    fig.patch.set_facecolor(C_BG)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    # 1. BASEPLATE & RIGID HARNESS
    ax.add_patch(Rectangle((200, 200), 220, 1600, facecolor=C_SUBSTRATE, edgecolor='none', zorder=1))
    ax.add_patch(Rectangle((660, 200), 220, 1600, facecolor=C_SUBSTRATE, edgecolor='none', zorder=1))
    ax.plot([200, 200], [200, 1800], color=C_IRON, lw=16, zorder=20)
    ax.plot([880, 880], [200, 1800], color=C_IRON, lw=16, zorder=20)

    ax.plot([320, 320], [1800, 1300], color=C_IRON, lw=12, zorder=20)
    ax.plot([760, 760], [1800, 1300], color=C_IRON, lw=12, zorder=20)
    ax.plot([320, 320], [700, 200], color=C_IRON, lw=12, zorder=20)
    ax.plot([760, 760], [700, 200], color=C_IRON, lw=12, zorder=20)

    # 2. THE DECOHERENCE LIMITERS (Attentional Pinch)
    # The physical radius of the channel at the focal node
    r_choke = R_MAX - s_val * (R_MAX - R_MIN)

    # Venturi geometry mapping down the central axis
    curve_y = np.linspace(Y_END, Y_START, 200)
    p_pinch = np.exp(-((curve_y - 1000) / 220.0)**2)  
    r_local_curve = R_MAX - p_pinch * (R_MAX - r_choke)

    # Physical Mechanical Blocks rendering the Pinch
    left_bound = 540 - r_local_curve
    left_pts = [(320, Y_END)] + list(zip(left_bound, curve_y)) + [(320, Y_START)]
    ax.add_patch(Polygon(left_pts, facecolor=C_DEPLETION, hatch='////', edgecolor=C_IRON, lw=4, zorder=18))

    right_bound = 540 + r_local_curve
    right_pts = [(760, Y_END)] + list(zip(right_bound, curve_y)) + [(760, Y_START)]
    ax.add_patch(Polygon(right_pts, facecolor=C_DEPLETION, hatch='\\\\\\\\', edgecolor=C_IRON, lw=4, zorder=18))

    # Neural Pads (The Willpower Input Nodes)
    alpha_gate = max(0.1, s_val * 0.9)
    ax.add_patch(Rectangle((250, 800), 70, 400, facecolor=C_GATE, alpha=alpha_gate, edgecolor='none', zorder=17))
    ax.add_patch(Rectangle((250, 800), 70, 400, facecolor='none', edgecolor=C_IRON, lw=6, zorder=19))
    
    ax.add_patch(Rectangle((760, 800), 70, 400, facecolor=C_GATE, alpha=alpha_gate, edgecolor='none', zorder=17))
    ax.add_patch(Rectangle((760, 800), 70, 400, facecolor='none', edgecolor=C_IRON, lw=6, zorder=19))

    # 3. KINEMATICS: QUANTUM TO CLASSICAL FLUID TENSOR
    y_norm = (offsets + cum_flow[f]) % 1.0
    py = Y_START - y_norm * Y_LEN
    
    # Real-time envelope width at particle's current y
    p_particle = np.exp(-((py - 1000) / 220.0)**2)
    r_particle = R_MAX - p_particle * (R_MAX - r_choke)
    
    # The physical mapping of the streamline
    px = CX + raw_x * r_particle

    # Quantum Chaos (Superposition Entanglement)
    # The wider the envelope, the higher the random traversal noise. 
    # Squeezing the geometry mechanically enforces zero noise (decoherence).
    chaos_allowance = (r_particle - R_MIN) / (R_MAX - R_MIN)
    chaos_x = np.sin(py / 15.0 + wave_phase + cum_flow[f] * 50) * 35.0 * chaos_allowance
    px += chaos_x 

    # Thermodynamic Density Mapping (Collapsing into Terminal Green)
    squeeze_metric = (R_MAX - r_particle) / R_MAX
    
    # Base Wave Color interpolates Azure/Purple via phase oscillation
    wave_color_mix = (np.sin(wave_phase + py / 40.0) + 1.0) / 2.0
    base_c = C_AZURE * wave_color_mix[:, None] + C_PURPLE * (1.0 - wave_color_mix[:, None])
    
    pc = np.zeros((N_QUANTA, 3))
    # Funnel interpolation: Chaos Wave -> Focused Green
    pc[:] = base_c * (1.0 - squeeze_metric[:, None]**1.5) + C_MANTIS * (squeeze_metric[:, None]**1.5)
    
    # Opacity increases as data concentrates
    pa = np.clip(0.4 + squeeze_metric * 0.6, 0, 1) 
    rgba = np.column_stack((pc, pa))
    
    # Visual acceleration sizing
    ps = np.clip(16.0 - squeeze_metric * 10.0, 4.0, 16.0)

    # 4. DISPATCH ARRAYS TO MATPLOTLIB
    ax.scatter(px, py, s=ps, color=rgba, edgecolors='none', zorder=15)

    # 5. INDUSTRIAL WIDGETS & TELEMETRY
    ax.add_patch(Rectangle((0, 1840), 1080, 80, facecolor=C_BG, zorder=50))
    ax.text(40, 1880, "LG-141b: CONSCIOUSNESS TAP // O(1) FLUID DECOHERENCE TENSOR", color=C_IRON, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=51)

    state_str = "HIGH ENTROPY (PROBABILITY CLOUD)"
    text_color = '#8E44AD' 
    if s_val > 0.8:
        state_str = "DECOHERENCE (LAMINAR 4D FOCUS)"
        text_color = '#27AE60'
    elif s_val > 0.1:
        state_str = "PHASE TRANSITION (ATTENTIONAL GATING)"
        text_color = '#D4AC0D'
        
    ax.add_patch(Rectangle((0, 0), 1080, 160, facecolor=C_BG, zorder=50))
    ax.add_patch(Rectangle((0, 160), 1080, 2, facecolor=C_IRON, zorder=51))
    
    v_volt = s_val * 100.0 # Cognitive load percentage
    hz_metric = 5.0 + s_val * 35.0 # Alpha (5Hz) scaling to Gamma (40Hz)
    
    ax.text(40, 115, f"SYSTEM VECTOR: {state_str}", color=text_color, fontsize=20, fontname='monospace', weight='bold', va='center', zorder=51)
    ax.text(40, 65,  f"PRE-FRONTAL LOAD: {v_volt:04.1f}%", color=C_IRON, fontsize=20, fontname='monospace', weight='bold', va='center', zorder=51)
    ax.text(40, 25,  f"NEURAL OSCILLATION: {hz_metric:04.1f} Hz", color=C_IRON, fontsize=20, fontname='monospace', weight='bold', va='center', zorder=51)

    # Dial Widget 
    dial_cx, dial_cy = 960, 80
    ax.add_patch(Circle((dial_cx, dial_cy), 50, facecolor='none', edgecolor=C_IRON, lw=4, zorder=51))
    # Dial spins rapidly when Gamma Hz is high
    ind_ang = np.radians(-cum_flow[f] * 360 * 2) 
    ax.plot([dial_cx, dial_cx + np.cos(ind_ang)*40], [dial_cy, dial_cy + np.sin(ind_ang)*40], color=text_color, lw=6, zorder=52)

    # Component Tags
    ax.text(540, 1750, "CORTICAL SOURCE (ENTROPY)", color=C_BG, fontsize=16, fontname='monospace', weight='bold', ha='center', zorder=50)
    ax.text(540, 260, "4D MANIFESTATION (FLOW)", color=C_BG, fontsize=16, fontname='monospace', weight='bold', ha='center', zorder=50)
    ax.text(210, 1000, "- WILL -", color=C_BG, rotation=90, fontsize=16, fontname='monospace', weight='bold', ha='center', va='center', zorder=50)
    ax.text(870, 1000, "- WILL -", color=C_BG, rotation=-90, fontsize=16, fontname='monospace', weight='bold', ha='center', va='center', zorder=50)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-141b: THE CONSCIOUSNESS TAP // LAMINAR FOCUS [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Decoherence Eulerian Tensor // Daylight Modulo")

    with mp.Pool(processes=cpu_cores) as pool:
        frames = range(TOTAL_FRAMES)
        for finished_frame in pool.imap_unordered(render_frame, frames, chunksize=8):
            pass
    print("Compilation Complete. 4D Laminar Trajectory Locked.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
