"""
SOVEREIGN CODE: logic_garden_339c_slipperyslope.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Vectorization
SCENE: Logic Garden 339c (Slippery Slope // Runaway N-Space Cascade)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING, COGNITIVE LOGIC
HOTFIX: Linear 24.0s Sequence. Daylight Protocol. Absolute Camera Lock. Tuples Sealed.
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
OUT_DIR = "frames_339c_slipperyslope"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Environment Matrix
C_STEEL     = '#606065'   # Hardware Circuit Breakers / Damping Valves
C_DARK      = '#202025'   # Base Nodes
C_CYAN      = '#00FFFF'   # The Logic Audit Sweep
C_MAGENTA   = '#FF0055'   # Frictionless Cascade / Thermal Exhaust
C_GOLD      = '#FFB300'   # Sovereign Truth Vector (Reality)
C_MANTIS    = '#00FF00'   # Terminal Green / Safe Halt

def draw_industrial_grid(ax):
    """Draw the Structural Matrix"""
    for i in range(-5, 6):
        ax.plot([i*100, i*100], [-960, 960], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)
    for j in range(-9, 10):
        ax.plot([-540, 540], [j*100, j*100], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)

# PRECOMPUTE PYRAMID NODES
NODES = {}
idx = 0
for L in range(8):
    y = 500 - L * 140
    n_nodes = L + 1
    x_start = -100 * (n_nodes - 1) / 2
    for i in range(n_nodes):
        NODES[idx] = (x_start + i * 100, y, L)
        idx += 1

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

    # 1. RENDER BASE NODES
    for i, (nx, ny, nL) in NODES.items():
        if nL == 0:
            ax.add_patch(patches.RegularPolygon((nx, ny), numVertices=6, radius=25, facecolor=C_DARK, edgecolor=C_TEXT, lw=3, zorder=5))
            ax.text(nx+40, ny, "STEP A", color=C_TEXT, fontsize=12, weight='bold', va='center', fontname='monospace', zorder=5.1)
        elif nL == 7:
            ax.add_patch(patches.RegularPolygon((nx, ny), numVertices=6, radius=15, facecolor=C_TITANIUM, edgecolor=C_STEEL, lw=2, zorder=5))
            if nx == 0:
                ax.text(nx, ny-30, "STEP Z", color=C_STEEL, fontsize=12, weight='bold', ha='center', fontname='monospace', zorder=5.1)
        else:
            ax.add_patch(patches.RegularPolygon((nx, ny), numVertices=6, radius=15, facecolor=C_BG, edgecolor=C_DARK, lw=2, zorder=5))

    # 2. STATE LOGIC TIMELINE
    T_HALLUCINATION_START = 2.0
    T_AUDIT = 11.0
    T_REALITY_START = 13.0

    # ====================================================
    # SCENARIO A: THE HALLUCINATION (Frictionless Runaway)
    # ====================================================
    if t > T_HALLUCINATION_START and t < T_AUDIT:
        state_code = "[01] HALLUCINATION // SLIPPERY SLOPE"
        c_state = C_MAGENTA
        t_hal = t - T_HALLUCINATION_START
        velocity = 1.0 + (t_hal ** 2) * 0.5  # Quadratic runaway acceleration
        cascade_L = t_hal * velocity
        
        ax.text(0, 600, "FRICTION PARAMETER: 0.00 // O(N\u00b2) RUPTURE ACTIVE", color=C_MAGENTA, fontsize=14, weight='bold', ha='center', fontname='monospace', zorder=20)
        
        # Exponential branching logic breaking the bounds
        np.random.seed(339)
        max_lines = min(800, int(2 ** t_hal))
        
        for p in range(max_lines):
            # Lines spawn randomly and accelerate downwards wildly
            sx = np.random.normal(0, 50 + t_hal*20)
            sy = 500 - (t_hal * 100 * np.random.random())
            vy = -np.random.uniform(100, 300) * velocity
            vx = np.random.uniform(-1, 1) * 100 * velocity
            
            ex = sx + vx * 0.1
            ey = sy + vy * 0.1
            
            if sy > -900: # Draw while inside matrix
                ax.plot([sx, ex], [sy, ey], color=C_MAGENTA, lw=np.random.uniform(0.5, 2.5), alpha=0.6, zorder=10)
        
        # Original node goes critical
        ax.add_patch(patches.Circle((0, 500), 50 + t_hal*10, fill=False, edgecolor=C_MAGENTA, lw=4, alpha=max(0, 1.0 - t_hal/5.0), zorder=4))
        
        energy_out = f"KINETIC ENERGY: {int(cascade_L * 1000)} kN [UNBOUNDED]"

    # ====================================================
    # THE SOVEREIGN AUDIT (Reset)
    # ====================================================
    elif t >= T_AUDIT and t < T_REALITY_START:
        state_code = "[02] SERIALIZE RAZOR // INJECTING FRICTION"
        c_state = C_CYAN
        prg = (t - T_AUDIT) / 2.0
        
        sweep_y = 960 - (prg * 1920)
        ax.plot([-540, 540], [sweep_y, sweep_y], color=C_CYAN, lw=8, zorder=30)
        ax.fill_between([-540, 540], sweep_y, 960, color=C_CYAN, alpha=0.1, zorder=29)
        
        energy_out = "SYSTEM HALT // THERMODYNAMICS RESTORED"
        ax.text(0, 600, "RECALIBRATING MATRIX PARITY", color=C_CYAN, fontsize=16, weight='bold', ha='center', fontname='monospace', zorder=31)

    # ====================================================
    # SCENARIO B: THE REALITY (Algorithmic Damping)
    # ====================================================
    elif t >= T_REALITY_START:
        t_real = t - T_REALITY_START
        is_terminal = t_real >= 6.0
        state_code = "[03] TRUTHFUL EXECUTION" if not is_terminal else "[04] TATH\u0100T\u0100 // KINETICS RESOLVED"
        c_state = C_GOLD if not is_terminal else C_MANTIS
        
        ax.text(0, 600, "FRICTION PARAMETER: 0.85 // THERMODYNAMICS ACTIVE", color=C_MANTIS, fontsize=14, weight='bold', ha='center', fontname='monospace', zorder=20)
        
        # Add Physical Circuit Breakers (Baffles) to the nodes at Level 1 and 2
        baffle_width = 40
        for i, (nx, ny, nL) in NODES.items():
            if nL in [1, 2]:
                ax.add_patch(patches.Rectangle((nx-baffle_width/2, ny-20), baffle_width, 10, facecolor=C_STEEL, edgecolor=C_TEXT, lw=2, zorder=6))

        # Vector Propagation Flow
        # Sequence: A -> B1 (Level 1, left node) -> C2 (Level 2, middle node) -> Halt
        A = (0, 500)
        B = (-50, 360)
        C = (0, 220)
        
        if t_real < 1.0:
            energy_out = "KINETIC ENERGY: 100.00 kN"
            # Traveling A to B
            prg = t_real
            cur_x = A[0] + (B[0] - A[0]) * prg
            cur_y = A[1] + (B[1] - A[1]) * prg
            ax.plot([A[0], cur_x], [A[1], cur_y], color=C_GOLD, lw=5, zorder=10)
            ax.scatter(cur_x, cur_y, s=150, c=C_BG, edgecolors=C_GOLD, lw=3, zorder=11)
            
        elif t_real < 2.5:
            # Impact Baffle 1 (Spallation and damping)
            energy_out = "KINETIC ENERGY: 40.00 kN [BAFFLE IMPACT/LOS]"
            ax.plot([A[0], B[0]], [A[1], B[1]], color=C_GOLD, lw=5, zorder=10)
            
            exp_t = t_real - 1.0
            if exp_t < 1.0:
                ax.scatter(B[0], B[1]-20, s=exp_t*3000, c=C_BG, edgecolors=C_MAGENTA, lw=3, alpha=1.0-exp_t, zorder=15)
                # Spallation sparks off the baffle
                np.random.seed(int(t*100))
                ax.scatter(B[0] + np.random.uniform(-40, 40, 10), B[1] - 20 + np.random.uniform(0, 30, 10), s=20, c=C_MAGENTA, zorder=16)

        elif t_real < 4.0:
            energy_out = "KINETIC ENERGY: 40.00 kN -> DECAYING"
            # Traveling B to C (Thinner line, energy lost)
            prg = (t_real - 2.5) / 1.5
            cur_x = B[0] + (C[0] - B[0]) * prg
            cur_y = B[1] + (C[1] - B[1]) * prg
            
            ax.plot([A[0], B[0]], [A[1], B[1]], color=C_GOLD, lw=5, zorder=10)
            ax.plot([B[0], cur_x], [B[1], cur_y], color=C_GOLD, lw=2, zorder=10)
            ax.scatter(cur_x, cur_y, s=80, c=C_BG, edgecolors=C_GOLD, lw=2, zorder=11)

        else:
            energy_out = "KINETIC ENERGY: 0.00 kN [CASCADE HALTED SAFELY]"
            # Impact Baffle 2 (Final block)
            ax.plot([A[0], B[0]], [A[1], B[1]], color=C_GOLD, lw=5, zorder=10)
            ax.plot([B[0], C[0]], [B[1], C[1]], color=C_GOLD, lw=2, zorder=10)
            
            exp_t = t_real - 4.0
            if exp_t < 1.0:
                ax.scatter(C[0], C[1]-20, s=exp_t*1000, c=C_BG, edgecolors=C_MAGENTA, lw=2, alpha=1.0-exp_t, zorder=15)
                
            ax.add_patch(patches.Circle(C, 30, fill=False, edgecolor=C_MANTIS, lw=4, alpha=0.8, zorder=16))

    else:
        state_code = "SYSTEM ONLINE // STANDBY"
        c_state = C_TEXT
        energy_out = "WAITING ON INITIATIVE SPARK"

    # ====================================================
    # 4. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    # Top Header [Strict Tuples]
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-339c :: SLIPPERY SLOPE TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] O(N\u00b2) VARIABLE LOSS VS STRUCTURAL DAMPING", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    # Bottom Telemetry HUD
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    ax.text(-500, -760, "SYS_01 [ALGORITHMIC ENGINE]  :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, state_code, color=c_state, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [THERMODYNAMIC STATE] :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, energy_out, color=C_GOLD if (t > T_REALITY_START and t < T_REALITY_START+4.0) else (C_TEXT if t < T_HALLUCINATION_START else c_state), fontsize=15, fontname='monospace', weight='bold', zorder=82)

    # Metric step check
    if t > T_REALITY_START + 4.0: step_z = "UNBREACHED // ISOLATED"
    elif t > T_HALLUCINATION_START and t < T_AUDIT: step_z = "CATASTROPHIC SPATIAL RUPTURE"
    else: step_z = "IDLE // PERFECT INTEGRITY"

    ax.text(-500, -840, "METRIC AUDIT [STEP Z]        :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, step_z, color=C_MAGENTA if (t > T_HALLUCINATION_START and t < T_AUDIT) else C_MANTIS, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider [Strict Tuples]
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=c_state, zorder=83))

    # Sovereign Execution Output
    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    # Absolute Memory Annihilation
    plt.close('all')
    gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-339c: SLIPPERY SLOPE TENSOR [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE] [Tuples Sealed]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
