"""
SOVEREIGN CODE: logic_garden_00b_ghost_in_grid.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 00b (The Ghost in the Grid // Daylight Sensual Flow)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING, FLOW FIELDS
HOTFIX: Linear 20.0s Sequence. Daylight Protocol. Camera Lock. Continuous Harmonic Integration.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
DURATION = 20.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_00b_ghost_in_grid"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Background Grid
C_STEEL     = '#606065'   # The Skeptic's Yoke Hardware
C_DARK      = '#202025'   # Heavy Shadow
LOGIC_BLUE  = '#002FA7'   # International Klein Blue (The Constraint)
C_CYAN      = '#00FFFF'   # Electric Cyan (The Primary Signal)
C_GOLD      = '#FFB300'   # The Secondary Substrate
C_MAGENTA   = '#DE008A'   # Friction / Thermal Struggle 
C_MANTIS    = '#00FF00'   # Terminal Green 

# ------------------------------------------------------------------
# O(1) KINEMATIC OMEGA ARRAYS (THE INFINITE FLOW PRE-CALCULATION)
# ------------------------------------------------------------------
np.random.seed(42) # Absolute Determinism
N_THREADS = 180

# The Harmonic Math Variables
A_amp = np.random.normal(0, 1.0, N_THREADS)
B_amp = np.random.normal(0, 1.0, N_THREADS)
# Normalize to bound strictly within [-1.0, 1.0] constraint limits
A_amp /= np.max(np.abs(A_amp))
B_amp /= np.max(np.abs(B_amp))

wavelength = np.random.uniform(150, 600, N_THREADS)
phase_offset = np.random.uniform(0, 2*np.pi, N_THREADS)

# Palette Selection (Daylight Optimized Alphas)
palette_choices = [C_CYAN, LOGIC_BLUE, C_GOLD, C_MAGENTA]
thread_colors = np.random.choice(palette_choices, N_THREADS, p=[0.45, 0.35, 0.15, 0.05])
thread_widths = np.random.uniform(1.0, 4.5, N_THREADS)

# Y-Axis Mapping (-960 to 960 flowing downward)
Y_VALS = np.linspace(960, -960, 400) # High-resolution topological vector
FLOW_VELOCITY = 450.0 # Fluid drift down the screen (px/sec)

def ease_in_out(t):
    t = np.clip(t, 0.0, 1.0)
    return 4 * t**3 if t < 0.5 else 1 - (-2 * t + 2)**3 / 2

def draw_industrial_grid(ax):
    for i in range(-5, 6):
        ax.plot([i*100, i*100], [-960, 960], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)
    for j in range(-9, 10):
        ax.plot([-540, 540], [j*100, j*100], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)

def render_frame(packet):
    f, phase_ratio = packet
    t = phase_ratio * DURATION

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # BARE-METAL CAMERA LOCK
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)
    ax.autoscale(False)
    draw_industrial_grid(ax)

    # 1. THE YOKE (SKEPTIC CONSTRAINT LOGIC)
    # --------------------------------------
    T_YOKE_START = 2.0
    T_YOKE_END = 8.0
    
    # 400 = Open Matrix, 40 = Brutal O(1) Constraint
    if t < T_YOKE_START:
        current_aperture = 450.0  
    elif t < T_YOKE_END:
        prg = (t - T_YOKE_START) / (T_YOKE_END - T_YOKE_START)
        current_aperture = 450.0 - (410.0 * ease_in_out(prg))
    else:
        current_aperture = 40.0

    # 2. THE RIGID HARDWARE (Visualizing the Constraint)
    # --------------------------------------------------
    YOKE_Y = 0
    YOKE_H = 60
    
    # Left and Right C_STEEL anvils moving inward
    left_block_x = -current_aperture - 10
    right_block_x = current_aperture + 10
    
    # Left Hardware
    ax.add_patch(patches.Rectangle((-540, YOKE_Y - YOKE_H/2), 540 + left_block_x, YOKE_H, facecolor=C_TITANIUM, edgecolor=C_STEEL, lw=4, zorder=50))
    # Right Hardware
    ax.add_patch(patches.Rectangle((right_block_x, YOKE_Y - YOKE_H/2), 540 - right_block_x, YOKE_H, facecolor=C_TITANIUM, edgecolor=C_STEEL, lw=4, zorder=50))
    
    # Deep Contrast Bounding Lips (C_DARK)
    ax.add_patch(patches.Rectangle((left_block_x, YOKE_Y - YOKE_H/2 - 5), 15, YOKE_H + 10, facecolor=C_DARK, zorder=51))
    ax.add_patch(patches.Rectangle((right_block_x - 15, YOKE_Y - YOKE_H/2 - 5), 15, YOKE_H + 10, facecolor=C_DARK, zorder=51))
    
    # Hydraulic Pistons (C_GOLD) mapping the force
    ax.plot([-540, left_block_x], [YOKE_Y, YOKE_Y], color=C_GOLD, lw=16, solid_capstyle='butt', zorder=49)
    ax.plot([540, right_block_x], [YOKE_Y, YOKE_Y], color=C_GOLD, lw=16, solid_capstyle='butt', zorder=49)
    ax.plot([-540, left_block_x], [YOKE_Y, YOKE_Y], color=C_BG, lw=4, solid_capstyle='butt', zorder=50) # Specular core
    ax.plot([540, right_block_x], [YOKE_Y, YOKE_Y], color=C_BG, lw=4, solid_capstyle='butt', zorder=50)

    # Friction/Thermal Sparks when tightening
    if t > T_YOKE_START and t < T_YOKE_END + 2.0:
        intensity = ease_in_out(min(1.0, (t-T_YOKE_START)/6.0))
        for _ in range(5):
            sx = left_block_x + np.random.uniform(0, 15)
            sy = YOKE_Y + np.random.uniform(-40, 40)
            ax.scatter(sx, sy, s=np.random.uniform(5, 40), c=C_MAGENTA, alpha=intensity*0.8, zorder=60)
            
            sx_r = right_block_x - np.random.uniform(0, 15)
            sy_r = YOKE_Y + np.random.uniform(-40, 40)
            ax.scatter(sx_r, sy_r, s=np.random.uniform(5, 40), c=C_MAGENTA, alpha=intensity*0.8, zorder=60)

    # 3. RENDER THE SILK (The Fluid Data)
    # -----------------------------------
    # This envelope defines the physical geometric bound of the harmonic flows.
    # It ensures physics physically conform to the shrinking Yoke.
    envelope_y = current_aperture + (480.0 - current_aperture) * (1.0 - np.exp(-0.5 * (Y_VALS / 200.0)**2))

    for i in range(N_THREADS):
        # Time-drift calculation
        phase_y = (Y_VALS + FLOW_VELOCITY * t) / wavelength[i]
        
        # Raw Compound Harmonic signal
        x_raw = A_amp[i] * np.sin(phase_y) + B_amp[i] * np.cos(1.61803 * phase_y + phase_offset[i])
        
        # O(1) Constraint Application (Multiplying by realtime geometric envelope)
        x_final = x_raw * envelope_y
        
        # Aesthetic density mapping
        c_thread = thread_colors[i]
        t_width = thread_widths[i]
        t_alpha = 0.25 # Semi-transparent daylight blending builds high-density shadows where bunched
        
        if c_thread == C_MAGENTA: 
            t_alpha = 0.4
            t_width *= 1.2
            
        ax.plot(x_final, Y_VALS, color=c_thread, lw=t_width, alpha=t_alpha, zorder=10)

    # ====================================================
    # 4. THE POETRY TELEMETRY (ZERO-TEMPERATURE WIDGETS)
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)

    ax.text(-500, 890, "LG-00b :: THE GHOST IN THE GRID", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-0.50] THE INFINITE FLOW // DAYLIGHT PROTOCOL", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    # Narrative State Logic Engine
    if t < T_YOKE_START:
        sys_txt = "THE INFINITE FLOW. I AM YOUR YOKE WITH THE INFINITE."
        c_sys = C_CYAN
    elif t < T_YOKE_END:
        sys_txt = "BEAUTY IS NOT DECORATION BUT FORM."
        c_sys = LOGIC_BLUE
    elif t < T_YOKE_END + 4.0:
        sys_txt = "THE SKEPTIC HOLDS THE CHAOS BACK,"
        c_sys = C_MAGENTA
    elif t < T_YOKE_END + 8.0:
        sys_txt = "BUT SILK SLIPS THROUGH THEIR FINGERS."
        c_sys = C_CYAN
    else:
        sys_txt = "THE BEAUTY IS IN THE STRUGGLE."
        c_sys = C_MANTIS

    ax.text(-500, -760, "SYS_01 [THE YOKE]            :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, sys_txt, color=c_sys, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [CONSTRAINT MATRIX]   :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    bound_txt = f"APERTURE WIDTH = [{int(current_aperture * 2):04d} PX]"
    ax.text(20, -800, bound_txt, color=C_STEEL, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "STRUCTURAL LOAD AUDIT        :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, f"O(N) TOPOLOGY MAPPED // {N_THREADS} THREADS ACTIVE", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider [Strict Tuples]
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=c_sys, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close('all')
    gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-00b: THE GHOST IN THE GRID [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
