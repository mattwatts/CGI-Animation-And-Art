"""
SOVEREIGN CODE: logic_garden_39c_cosmic_forge_daylight.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Ouroboros Nucleosynthesis Tensor
SCENE: LG-39c (The Cosmic Forge / Daylight Protocol)
HOTFIX: Absolute Scalar Enforcement, Ouroboros Loop, Negative Flash Limits
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 10.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_39c_cosmic_daylight"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- DAYLIGHT HIGH-CONTRAST PALETTE --------
C_BG        = '#FFFFFF'
C_IRON      = '#1C2833'       # Isotopic Poisoning / Hardware Interrupt
C_ORANGE    = '#E67E22'       # Stellar Fusion Boundary
C_GOLD      = '#F1C40F'       # Core Hydrostatic Pressure
C_UV        = '#8E44AD'       # Crushing Thermodynamic Force
C_MAGENTA   = '#E74C3C'       # Shockwave Ejecta
C_CYAN      = '#3498DB'       # Oxygen / Platinum Ejecta
C_TEXT      = '#111111'
C_SILICON   = '#EAEDED'       # UI Substrate Base

def hex_to_rgb(h):
    h = h.lstrip('#')
    return np.array([int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)])/255.0

c_iron = hex_to_rgb(C_IRON)
c_oran = hex_to_rgb(C_ORANGE)
c_gold = hex_to_rgb(C_GOLD)
c_uv   = hex_to_rgb(C_UV)
c_mag  = hex_to_rgb(C_MAGENTA)
c_cyan = hex_to_rgb(C_CYAN)

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE KINEMATIC BOUNDING BOX
# ------------------------------------------------------------------
N_PARTICLES = 30000
np.random.seed(39)

base_r = np.sqrt(np.random.rand(N_PARTICLES)) 
base_theta = np.random.rand(N_PARTICLES) * 2 * np.pi

# Typologies for Spallation (Heavy metals)
# 0: Iron/Shockwave (Magenta), 1: Au/Gold (Yellow), 2: Oxygen/Light (Cyan)
p_type = np.random.choice([0, 1, 2], N_PARTICLES, p=[0.60, 0.20, 0.20])
type_colors = np.array([c_mag, c_gold, c_cyan])
c_spal = type_colors[p_type]

# Explosive velocity differentials
v_scale = np.random.uniform(0.5, 2.5, N_PARTICLES)

def ease_in_out(x):
    """C1 continuous parametric easing."""
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)

# ------------------------------------------------------------------
# O(1) MACRO-TIMELINE PRECOMPILATION
# ------------------------------------------------------------------
times = np.linspace(0, 1, TOTAL_FRAMES, endpoint=False)

# Track Dynamic Spin (Conservation of Angular Momentum)
raw_spin = np.zeros(TOTAL_FRAMES)
raw_cam  = np.zeros(TOTAL_FRAMES)

for f in range(TOTAL_FRAMES):
    t = times[f]
    
    # Parametric Envelope
    if t < 0.25: r_env = 1.0 + 0.03 * np.sin(t * 8 * np.pi)
    elif t < 0.35: r_env = 1.0
    elif t < 0.49: r_env = (1.0 - (t-0.35)/0.14)**6.0
    elif t < 0.50: r_env = 0.001
    elif t < 0.75: r_env = 25.0 * ((t-0.5)/0.25)**0.5
    else: r_env = 25.0 * (1 - ease_in_out((t-0.75)/0.25)) + 1.0 * ease_in_out((t-0.75)/0.25)
    
    # Gravity accelerates spin violently at tightly packed radius
    raw_spin[f] = 1.0 / (r_env**2 + 0.02)
    # Target Camera Width (Outer particle boundary logic)
    raw_cam[f] = max(3.0, r_env * 2.5 * 2.2)

# Normalize spatial rotation to exactly 6.0 revolutions for flawless re-entry
cum_spin = np.cumsum(raw_spin)
cum_spin = (cum_spin / cum_spin[-1]) * (2 * np.pi * 6.0)

# Smooth Autonomous Bounding Box Matrix
smooth_cam = np.copy(raw_cam)
for _ in range(30):
    smooth_cam = np.convolve(np.pad(smooth_cam, (10,10), mode='wrap'), np.ones(21)/21, mode='valid')

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    t = times[f]
    spin_rad = cum_spin[f]
    cam_w = smooth_cam[f]
    cam_h = cam_w * (1920.0 / 1080.0)

    # Instantiate Geometry Constraints
    is_flash = (0.49 <= t < 0.50)
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    bg_current = C_IRON if is_flash else C_BG
    fig.patch.set_facecolor(bg_current)
    ax_cam = plt.Axes(fig, [0., 0., 1., 1.])
    ax_cam.set_axis_off()
    fig.add_axes(ax_cam)
    ax_cam.set_facecolor(bg_current)
    ax_cam.set_xlim(-cam_w/2, cam_w/2)
    ax_cam.set_ylim(-cam_h/2, cam_h/2)

    # 1. KINEMATIC TENSOR LOGIC
    # Base configuration: Hydrostatic equilibrium
    # base_r is shape (N,), so [:, None] correctly maps to (N, 3) matrix
    c_fusion = c_gold * (1 - base_r)[:, None] + c_oran * base_r[:, None]
    
    R_current = np.zeros(N_PARTICLES)
    C_current = np.zeros((N_PARTICLES, 3))

    if t < 0.25:
        state_str = "HYDROSTATIC EQUILIBRIUM: FUSION VS GRAVITY"
        ui_c = C_ORANGE
        mult = 1.0 + 0.03 * np.sin(t * 8 * np.pi) # scalar
        R_current = base_r * mult
        C_current = c_fusion

    elif t < 0.35:
        state_str = "STRUCTURAL CRITICAL FAIL: IRON ISOTOPE POISONING"
        ui_c = C_IRON
        prog = (t - 0.25) / 0.10
        R_current = base_r
        # base_r is array, so [:, None] is correct here
        poison_fade = np.clip((prog * 1.5 - base_r) * 5.0, 0, 1)
        C_current = c_iron * poison_fade[:, None] + c_fusion * (1 - poison_fade)[:, None]

    elif t < 0.49:
        state_str = "THERMODYNAMIC BOUNDARY SHATTER: CRUSH LOGIC"
        ui_c = C_UV
        prog = (t - 0.35) / 0.14
        R_current = base_r * (1.0 - prog)**6.0
        
        # SOVEREIGN FIX: heat_fade is a pure float scalar. 
        heat_fade = float(np.clip(prog * 2.0, 0.0, 1.0))
        # Broadcast scalar mix globally across an N-sized matrix 
        c_mix = c_uv * heat_fade + c_iron * (1.0 - heat_fade)
        C_current = np.ones((N_PARTICLES, 3)) * c_mix

    elif t < 0.50:
        state_str = "HARDWARE INTERRUPT: CORE BOUNCE"
        ui_c = C_BG
        R_current = base_r * 0.001
        C_current = hex_to_rgb(C_BG) * np.ones((N_PARTICLES, 3)) # Brilliant white flash

    elif t < 0.75:
        state_str = "SPALLATION MATRIX: NUCLEOSYNTHESIS PHASE"
        ui_c = C_MAGENTA
        prog = (t - 0.50) / 0.25
        R_current = base_r * (25.0 * v_scale * (prog**0.5))
        C_current = c_spal

    else:
        state_str = "TATHĀTĀ OUROBOROS: NEBULA ACCRETION / RECYCLE"
        ui_c = C_CYAN
        # SOVEREIGN FIX: prog is a pure float scalar.
        prog = float(ease_in_out((t - 0.75) / 0.25))
        R_start = base_r * (25.0 * v_scale)
        R_current = R_start * (1.0 - prog) + base_r * prog
        
        # Scalar natively applies cleanly across arrays c_spal and c_fusion without [:, None]
        C_current = c_spal * (1.0 - prog) + c_fusion * prog

    # Calculate precise cartesian layout with rotation
    theta_current = base_theta + spin_rad
    px = R_current * np.cos(theta_current)
    py = R_current * np.sin(theta_current)

    # Dynamic Volumetric Scaling
    s_val = np.clip(45.0 / (cam_w**0.7), 0.5, 20.0)

    if is_flash: C_current = np.ones((N_PARTICLES, 3))

    ax_cam.scatter(px, py, s=s_val, facecolor=C_current, edgecolor='none', alpha=0.9, zorder=10)

    # 2. DIAGNOSTIC HUD LAYER
    ax_ui = fig.add_axes([0., 0., 1., 1.])
    ax_ui.set_axis_off()
    ax_ui.set_xlim(0, 1080); ax_ui.set_ylim(0, 1920)

    txt_col = C_BG if is_flash else C_TEXT
    box_col = C_IRON if is_flash else C_SILICON

    ax_ui.add_patch(Rectangle((0, 1840), 1080, 80, facecolor=box_col, alpha=0.95, zorder=50))
    ax_ui.text(40, 1880, "LG-39c: SUPERNOVA SPALLATION // TRUE OUROBOROS ACCRETION", color=txt_col, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=51)

    ax_ui.add_patch(Rectangle((0, 0), 1080, 140, facecolor=box_col, alpha=0.95, zorder=50))
    ax_ui.add_patch(Rectangle((0, 140), 1080, 2, facecolor=C_IRON if not is_flash else C_BG, zorder=51))
    
    bind_sys = 100.0 / max(0.001, np.mean(R_current))
    cam_display = cam_w * 400.0 # Virtual km span

    ax_ui.text(40, 95, f"SYS TRACE: {state_str}", color=ui_c, fontsize=20, fontname='monospace', weight='bold', va='center', zorder=51)
    ax_ui.text(40, 45, f"BINDING ENERGY: {bind_sys:06.1f} PJ   |   BOUNDING BOX: {cam_display:08.0f} KM", color=txt_col, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=51)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=bg_current, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-39c: OUROBOROS FORGE MATRIX (SCALAR ENFORCED) [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Parametric Bounding Box // Negative Flash Limits")

    with mp.Pool(processes=cpu_cores) as pool:
        frames = range(TOTAL_FRAMES)
        for finished_frame in pool.imap_unordered(render_frame, frames, chunksize=8):
            pass
    print("Compilation Complete. Nucleosynthesis Baseplate Locked.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
