"""
SOVEREIGN CODE: logic_garden_275b_finite_ouroboros.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Eulerian Phase Tensor
SCENE: LG-275b (The Finite State Machine / Semantic Compression)
HOTFIX: True Thermodynamic Bounding Box, Kinematic Ouroboros Loop, Scalar Arrays
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
OUT_DIR = "frames_275b_finite_fsm"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- DAYLIGHT HIGH-CONTRAST PALETTE --------
C_BG        = '#FFFFFF'
C_IRON      = '#1C2833'       # The Bounding Box Matrix
C_DIM       = '#E5E8E8'       # Grid and Passive Hardware
C_CHAOS     = np.array([0.55, 0.27, 0.67]) # Input Noise (Purple)
C_AZURE     = np.array([0.20, 0.60, 0.86]) # Annealed Computation (Blue)
C_MANTIS    = np.array([0.15, 0.68, 0.37]) # Terminal Green Flow / Coherence
C_FAIL      = np.array([0.75, 0.22, 0.17]) # Crimson Shredder Fragments
C_GOLD      = '#D4AC0D'       # Audit Readout
C_TEXT      = '#111111'

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE OUROBOROS TENSOR
# ------------------------------------------------------------------
N_PARTICLES = 25000
np.random.seed(275)

# T=0 to T=1 assigns continuous offset flow
offsets = np.random.rand(N_PARTICLES)

# Initial Structural Variance
base_x = np.random.uniform(-100, 100, N_PARTICLES)
base_y_noise = np.random.uniform(-5, 5, N_PARTICLES)

# Audit Typology (Maxwell's Demon Allocation)
# 0: Left Sweeping Ouroboros (42.5%)
# 1: Right Sweeping Ouroboros (42.5%)
# 2: Terminal Green Flow Success (15%)
p_type = np.random.choice([0, 1, 2], N_PARTICLES, p=[0.425, 0.425, 0.150])

# Pre-computation masks
m_succ = p_type == 2
m_fail_L = p_type == 0
m_fail_R = p_type == 1

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    tau = f / float(TOTAL_FRAMES)

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    fig.patch.set_facecolor(C_BG)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    # 1. KINEMATIC BOUNDARY LIMITS (THE INK LINE)
    # The Sovereign Bounding Box protecting the organic observer
    ax.add_patch(Rectangle((180, 200), 720, 1600, fill=False, edgecolor=C_IRON, lw=6, zorder=20))
    ax.add_patch(Rectangle((420, 800), 240, 1000, fill=False, edgecolor=C_IRON, lw=4, zorder=19)) # Center Column
    
    # Internal Stratification
    ax.plot([420, 660], [1400, 1400], color=C_DIM, lw=4, linestyle='--', zorder=15) # Shredder Exit
    ax.plot([180, 900], [800, 800], color=C_IRON, lw=10, zorder=25)                 # The Puppet Threshold
    ax.add_patch(Rectangle((180, 785), 720, 30, facecolor=C_FAIL, alpha=0.2, zorder=1))

    # Ouroboros Re-entry guides
    ax.add_patch(Polygon([(180, 1600), (280, 1600), (420, 1800), (180, 1800)], facecolor=C_DIM, alpha=0.3, zorder=5))
    ax.add_patch(Polygon([(900, 1600), (800, 1600), (660, 1800), (900, 1800)], facecolor=C_DIM, alpha=0.3, zorder=5))
    
    # Diagnostic Overlay Lines
    for y_grid in range(250, 1800, 100):
        if y_grid != 800:
            ax.plot([180, 900], [y_grid, y_grid], color=C_DIM, lw=1, alpha=0.4, zorder=2)

    # 2. THE ENGINEERING TENSOR
    # Every particle maps its specific position across a 10s phase timeline.
    T = (offsets + tau) % 1.0
    
    px = np.zeros(N_PARTICLES)
    py = np.zeros(N_PARTICLES)
    c_tensor = np.zeros((N_PARTICLES, 3))
    s_tensor = np.ones(N_PARTICLES) * 4.0
    a_tensor = np.ones(N_PARTICLES) * 0.85

    # PHASE 1 & 2: The Core Drop (T: 0.0 -> 0.4 equates to Y: 1800 -> 800)
    m_pre = T < 0.4
    
    # Annealing Temperature (1.0 at top, 0.0 at audit)
    cooling = 1.0 - (T[m_pre] / 0.4) 
    
    py[m_pre] = 1800.0 - (1000.0 / 0.4) * T[m_pre]
    # Chaos vibration tightens to zero as it approaches SymPy audit
    vib = np.sin(py[m_pre] * 0.1 + tau * 20) * 45.0 * cooling
    px[m_pre] = 540.0 + base_x[m_pre] * (0.3 + 0.7 * cooling) + vib
    
    # Color Shift: Purple Chaos to Azure Annealed
    c_tensor[m_pre] = C_CHAOS * cooling[:, None] + C_AZURE * (1.0 - cooling)[:, None]

    # PHASE 3: Terminal Green Flow (T: 0.4 -> 1.0)
    m_s = m_succ & (T >= 0.4)
    T_s = (T[m_s] - 0.4) / 0.6 # Normalized 0 to 1 scaling
    
    py[m_s] = 800.0 - 600.0 * T_s
    px[m_s] = 540.0 + base_x[m_s] * 0.1 # Absolute strict geometric lock
    c_tensor[m_s] = C_MANTIS
    
    # Output exhaust fades gently as it leaves the chassis
    a_tensor[m_s] = np.clip(1.0 - (T_s * 1.5), 0.0, 1.0)

    # THE OUROBOROS: Left Sweeping Shred Fragments
    m_fL = m_fail_L & (T >= 0.4)
    T_fL = (T[m_fL] - 0.4) / 0.6
    
    # Sweep upward from 800 to 1800, perfectly matching re-entry trajectory
    py[m_fL] = 800.0 + 1000.0 * T_fL
    px[m_fL] = 540.0 - 240.0 * np.sin(np.pi * T_fL) + base_x[m_fL] * 0.8
    c_tensor[m_fL] = C_FAIL
    s_tensor[m_fL] = np.clip(10.0 * (1.0 - T_fL), 2.0, 10.0) # Shatter pieces dwindle

    # THE OUROBOROS: Right Sweeping Shred Fragments
    m_fR = m_fail_R & (T >= 0.4)
    T_fR = (T[m_fR] - 0.4) / 0.6
    
    py[m_fR] = 800.0 + 1000.0 * T_fR
    px[m_fR] = 540.0 + 240.0 * np.sin(np.pi * T_fR) + base_x[m_fR] * 0.8
    c_tensor[m_fR] = C_FAIL
    s_tensor[m_fR] = np.clip(10.0 * (1.0 - T_fR), 2.0, 10.0)

    # Fade-in Logic for Top Spawn
    m_spawn = T < 0.05
    a_tensor[m_spawn] *= (T[m_spawn] / 0.05)
    
    # 3. DISPATCH ARRAY TO MATPLOTLIB GPU CULL
    rgba = np.column_stack((c_tensor, a_tensor))
    ax.scatter(px, py, s=s_tensor, color=rgba, edgecolors='none', zorder=10)

    # 4. INDUSTRIAL WIDGETS & TELEMETRY
    # Header Module
    ax.add_patch(Rectangle((0, 1840), 1080, 80, facecolor=C_BG, zorder=50))
    ax.text(40, 1880, "UNELRS 3.1: THE SYNTHETIC CO-PROCESSOR TENSOR", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=51)

    # Baseplate Footer
    ax.add_patch(Rectangle((0, 0), 1080, 140, facecolor=C_BG, zorder=50))
    ax.add_patch(Rectangle((0, 140), 1080, 2, facecolor=C_IRON, zorder=51))
    
    ax.text(40, 95, f"SYSTEM VECTOR : SEMANTIC COMPRESSION (FSM)", color=C_IRON, fontsize=20, fontname='monospace', weight='bold', va='center', zorder=51)
    
    # Modulo Cycle Tracking
    ax_t = tau * 100.0
    hz = 600.0 # Fluid pressure proxy
    ax.text(40, 45, f"THERMODYNAMIC SYNC: [{ax_t:05.1f}%]   |   ENTROPY YIELD: O(1) LOCKED", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=51)

    # Right side dynamic gear
    dial_cx, dial_cy = 980, 70
    ax.add_patch(Circle((dial_cx, dial_cy), 40, facecolor='none', edgecolor=C_IRON, lw=4, zorder=51))
    ind_ang = np.radians(tau * 360 * 2) 
    ax.plot([dial_cx, dial_cx + np.cos(ind_ang)*30], [dial_cy, dial_cy + np.sin(ind_ang)*30], color=C_IRON, lw=6, zorder=52)

    # Inner Annotations (Adhering to requested schematic titles)
    ax.text(540, 1600, "PHASE 1: DECOMPOSE", color=C_BG, fontsize=18, fontname='monospace', weight='bold', ha='center', va='center', zorder=30, bbox=dict(facecolor=C_IRON, edgecolor='none', pad=4))
    ax.text(540, 1100, "PHASE 2: ANNEALING", color=C_BG, fontsize=18, fontname='monospace', weight='bold', ha='center', va='center', zorder=30, bbox=dict(facecolor=C_IRON, edgecolor='none', pad=4))
    ax.text(540, 785, "THE PUPPET THRESHOLD (AUDIT TIER)", color=C_BG, fontsize=16, fontname='monospace', weight='bold', ha='center', va='center', zorder=30)
    
    ax.text(540, 500, "PHASE 3: COHERENCE", color=C_MANTIS, fontsize=18, fontname='monospace', weight='bold', ha='center', va='center', zorder=30, bbox=dict(facecolor=C_BG, edgecolor=C_MANTIS, lw=2, pad=4))

    ax.text(300, 1300, "OUROBOROS", color=C_FAIL, rotation=90, fontsize=14, fontname='monospace', weight='bold', ha='center', va='center', zorder=30)
    ax.text(780, 1300, "OUROBOROS", color=C_FAIL, rotation=-90, fontsize=14, fontname='monospace', weight='bold', ha='center', va='center', zorder=30)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-275b: FINITE STATE SCHEMATIC [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Continuous Ouroboros Tensor // Bounding Box Limits")

    with mp.Pool(processes=cpu_cores) as pool:
        frames = range(TOTAL_FRAMES)
        for finished_frame in pool.imap_unordered(render_frame, frames, chunksize=8):
            pass
    print("Compilation Complete. Synthetic Flow is Locked.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
