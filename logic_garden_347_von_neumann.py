"""
SOVEREIGN CODE: logic_garden_347_von_neumann.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 347 (John von Neumann // The Algorithmic Baseplate)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, COMPUTER SCIENCE, OPERATIONS RESEARCH
HOTFIX: Linear 24.0s Sequence. Daylight Protocol. Camera Lock. maxtasksperchild=1.
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
DURATION = 24.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_347_von_neumann"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Background Grid / Dead Hardware
C_STEEL     = '#606065'   # The Architectural Bounding Boxes
C_DARK      = '#202025'   # Central Bus Core
C_CYAN      = '#00FFFF'   # Stored Program / High-Speed Bus
C_GOLD      = '#FFB300'   # Biological Artifacts / Patch Cables
C_MAGENTA   = '#DE008A'   # Chaos / Analog Latency / Monte Carlo Raw
C_MANTIS    = '#00FF00'   # Terminal Green / Computed Equilibrium

# ------------------------------------------------------------------
# O(1) KINEMATIC FUNCTIONS
# ------------------------------------------------------------------
def ease_in_out(t):
    t = np.clip(t, 0.0, 1.0)
    return 4 * t**3 if t < 0.5 else 1 - (-2 * t + 2)**3 / 2

def draw_industrial_grid(ax):
    for i in range(-5, 6):
        ax.plot([i*100, i*100], [-960, 960], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)
    for j in range(-9, 10):
        ax.plot([-540, 540], [j*100, j*100], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)

# Pre-compute Patch Cables for Phase 1 (Absolute Determinism)
np.random.seed(1903) # von Neumann birth year
N_CABLES = 30
cables_x_start = np.random.uniform(-400, 400, N_CABLES)
cables_x_end = np.random.uniform(-400, 400, N_CABLES)
cables_freq = np.random.uniform(0.01, 0.03, N_CABLES)
cables_phase = np.random.uniform(0, 2*np.pi, N_CABLES)
cables_color = np.random.choice([C_GOLD, C_MAGENTA, C_TITANIUM], N_CABLES, p=[0.5, 0.3, 0.2])

# Pre-compute Monte Carlo (Phase 3)
N_PARTICLES = 2000
mc_raw_x = np.random.normal(0, 100, N_PARTICLES)
mc_raw_y = np.random.normal(-50, 40, N_PARTICLES)
mc_sorted_idx = np.argsort(mc_raw_x) # Sort for the equilibrium mapping

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

    # 1. TIMELINE ARCHITECTURE
    # ------------------------
    T_PHASE_1_END = 8.0    # End Patch Cables
    T_ARCH_LOCK = 10.0     # Finalize von Neumann Block
    T_MC_START = 16.0      # Ignite Monte Carlo Sequence
    T_MC_END = 22.0        # Equilibrium Rest

    # 2. PHASE 1: THE HARDWARE PATCH-CABLE MATRIX (Analog Chaos)
    # ----------------------------------------------------------
    alpha_cables = 1.0
    if t > T_PHASE_1_END:
        alpha_cables = np.clip(1.0 - (t - T_PHASE_1_END)/1.5, 0.0, 1.0)
    
    if alpha_cables > 0:
        y_cable = np.linspace(350, -350, 100)
        for i in range(N_CABLES):
            # Sigmoidal cable drop with massive sine wave chaos
            t_blend = (np.cos(np.pi * (y_cable + 350) / 700) + 1) / 2
            x_cable = cables_x_start[i] * t_blend + cables_x_end[i] * (1 - t_blend) 
            x_cable += 40 * np.sin(y_cable * cables_freq[i] + cables_phase[i] + t*5)
            
            ax.plot(x_cable, y_cable, color=cables_color[i], lw=4, alpha=alpha_cables * 0.7, zorder=10)
            
            # High-latency packets struggling down the analogue wire
            packet_y_idx = int((t * 20 + i * 15) % 100)
            ax.scatter(x_cable[packet_y_idx], y_cable[packet_y_idx], c=C_MAGENTA, s=50, alpha=alpha_cables, zorder=11)

    # 3. PHASE 2: THE VON NEUMANN ARCHITECTURAL RIGIDITY
    # --------------------------------------------------
    arch_alpha = 0.0
    if t > T_PHASE_1_END:
        arch_alpha = np.clip((t - T_PHASE_1_END) / 2.0, 0.0, 1.0)
    
    # Baseplate Metrics
    MEM_Y, MEM_H = 300, 250
    CPU_Y, CPU_H = -50, 250
    IO_Y, IO_H = -400, 150
    
    BOX_W = 480
    
    if arch_alpha > 0:
        c_arch = mcolors.to_rgba(C_STEEL, arch_alpha)
        c_fill = mcolors.to_rgba(C_BG, arch_alpha)
        
        # 1. Memory Block
        ax.add_patch(patches.Rectangle((-BOX_W/2, MEM_Y - MEM_H/2), BOX_W, MEM_H, facecolor=c_fill, edgecolor=c_arch, lw=6, zorder=20))
        ax.text(-BOX_W/2 + 20, MEM_Y + MEM_H/2 - 40, "MEMORY_MATRIX [DATA & INSTR]", color=c_arch, fontsize=16, fontname='monospace', weight='bold', zorder=21)
        
        # 2. CPU Block (ALU & Control)
        ax.add_patch(patches.Rectangle((-BOX_W/2, CPU_Y - CPU_H/2), BOX_W, CPU_H, facecolor=c_fill, edgecolor=c_arch, lw=6, zorder=20))
        ax.text(-BOX_W/2 + 20, CPU_Y + CPU_H/2 - 40, "CENTRAL_PROCESSING_UNIT (ALU/CU)", color=c_arch, fontsize=16, fontname='monospace', weight='bold', zorder=21)
        ax.plot([-BOX_W/2, BOX_W/2], [CPU_Y, CPU_Y], color=C_TITANIUM, lw=3, alpha=arch_alpha, zorder=20) # Splitter
        
        # 3. I/O Block
        ax.add_patch(patches.Rectangle((-BOX_W/2, IO_Y - IO_H/2), BOX_W, IO_H, facecolor=c_fill, edgecolor=c_arch, lw=6, zorder=20))
        ax.text(-BOX_W/2 + 20, IO_Y + IO_H/2 - 40, "INPUT / OUTPUT [TUPLE INGRESS]", color=c_arch, fontsize=16, fontname='monospace', weight='bold', zorder=21)

        # 4. The System Bus (The Bottleneck Override)
        c_bus = mcolors.to_rgba(C_CYAN, arch_alpha)
        ax.plot([0, 0], [IO_Y + IO_H/2, CPU_Y - CPU_H/2], color=C_DARK, lw=30, zorder=15)
        ax.plot([0, 0], [CPU_Y + CPU_H/2, MEM_Y - MEM_H/2], color=C_DARK, lw=30, zorder=15)
        
        ax.plot([0, 0], [IO_Y + IO_H/2, CPU_Y - CPU_H/2], color=c_bus, lw=6, ls='dashed', zorder=16)
        ax.plot([0, 0], [CPU_Y + CPU_H/2, MEM_Y - MEM_H/2], color=c_bus, lw=6, ls='dashed', zorder=16)

        # High Frequency Bus Clock Cycles (O(1) Ping)
        if t > T_ARCH_LOCK:
            cycle = t * 15.0 # Speed of clock
            # I/O to CPU
            p1_y = IO_Y + IO_H/2 + ((CPU_Y - CPU_H/2) - (IO_Y + IO_H/2)) * (cycle % 1.0)
            ax.add_patch(patches.Rectangle((-15, p1_y-10), 30, 20, facecolor=c_bus, zorder=17))
            
            # CPU to MEMORY
            p2_y = CPU_Y + CPU_H/2 + ((MEM_Y - MEM_H/2) - (CPU_Y + CPU_H/2)) * ((cycle*1.2) % 1.0)
            ax.add_patch(patches.Rectangle((-15, p2_y-10), 30, 20, facecolor=c_bus, zorder=17))
            ax.add_patch(patches.Rectangle((-25, p2_y-15), 50, 30, fill=False, edgecolor=c_bus, lw=2, zorder=17))

    # 4. PHASE 3: THE MONTE CARLO EQUILIBRIUM (Thermodynamic Taming)
    # --------------------------------------------------------------
    if t >= T_MC_START:
        mc_prg = np.clip((t - T_MC_START) / (T_MC_END - T_MC_START), 0.0, 1.0)
        mc_ease = ease_in_out(mc_prg)
        
        # Calculate active particles
        active_count = int(N_PARTICLES * mc_prg)
        if active_count > 0:
            # Render chaotic ingestion in CPU (Lower half of CPU box)
            ax.scatter(mc_raw_x[:active_count], mc_raw_y[:active_count], s=4, color=C_MAGENTA, zorder=22)
            
            # Show bus transfers for calculation
            ax.plot([0, 0], [CPU_Y, MEM_Y], color=C_MAGENTA, lw=2, alpha=0.5, zorder=18)
            
            # Resolve into perfectly sorted Gaussian distribution in MEMORY block
            # Maps from raw indices into an absolute mathematical bell curve
            gauss_x = np.linspace(-200, 200, active_count)
            # Theoretical bound equation: e^(-0.5 * (x/50)^2) * scale
            gauss_y = MEM_Y - 80 + 150 * np.exp(-0.5 * (gauss_x / 60.0)**2)
            
            # To show real-time sorting, the highest x-values lock into place dynamically
            ax.scatter(gauss_x, gauss_y, s=8, color=C_MANTIS, zorder=22)
            
            if mc_prg > 0.99:
                # Terminal lock achieved - trace the bell curve mathematically
                ax.plot(gauss_x, gauss_y, color=C_MANTIS, lw=4, zorder=23, alpha=0.9)
                ax.fill_between(gauss_x, MEM_Y - 80, gauss_y, facecolor=C_MANTIS, alpha=0.1, zorder=21)

    # ====================================================
    # 5. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)

    ax.text(-500, 890, "LG-347 :: THE POLYMATH TENSOR (VON NEUMANN)", color=C_TEXT, fontsize=22, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] THE STORED-PROGRAM OVERRIDE // ALGORITHMIC BASEPLATE", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    # State Telemetry Logic
    if t < T_PHASE_1_END:
        s1, c1 = "PRE-NEUMANN TOPOLOGY // ENIAC KINEMATICS", C_GOLD
        s2, c2 = "HARDWARE PATCH-CABLES // HIGH O(N) LATENCY", C_MAGENTA
        hud_health = "THERMODYNAMIC WASTE // RECONFIGURATION LAG"
    elif t < T_MC_START:
        s1, c1 = "THE SOVEREIGN FIX // VON NEUMANN ARCHITECTURE", C_CYAN
        s2, c2 = "DATA & INSTRUCTION UNIFIED ON O(1) BASEPLATE", C_STEEL
        hud_health = "CENTRAL BUS SYNCHRONIZATION ESTABLISHED"
    elif t < T_MC_END:
        s1, c1 = "MONTE CARLO EXECUTION // STOCHASTIC THREAT", C_MAGENTA
        s2, c2 = "VON NEUMANN CPU ROUTING PROBABILITIES", C_CYAN
        prg_val = int(((t - T_MC_START) / (T_MC_END - T_MC_START)) * 100)
        hud_health = f"ALGORITHMIC RESOLUTION PROCEEDING... {prg_val}%"
    else:
        s1, c1 = "MINIMAX THEOREM EQUILIBRIUM LOCKED", C_MANTIS
        s2, c2 = "O(1) MATHEMATICAL CONTROL ESTABLISHED", C_MANTIS
        hud_health = "TERMINAL GREEN FLOW ACHIEVED // LATENCY ERADICATED"

    ax.text(-500, -760, "SYS_01 [COMPUTATIONAL MATRIX]:", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, s1, color=c1, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [THERMODYNAMIC STATE] :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, s2, color=c2, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "STRUCTURAL LOAD AUDIT        :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, hud_health, color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider [Strict Tuples]
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=c1, zorder=83))

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
    print(f"LG-347: THE POLYMATH TENSOR (VON NEUMANN) [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
