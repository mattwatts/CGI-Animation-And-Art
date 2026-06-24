"""
SOVEREIGN CODE: logic_garden_1c_deterministic_pendulum.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Vectorization
SCENE: Logic Garden 1c (The Deterministic Pendulum / LG-01 x LG-339f)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, CHAOS THEORY, KINEMATIC ENGINEERING
HOTFIX: Linear 24.0s Sequence. Alpha Tensor bounded to [0.0, 1.0].
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
from matplotlib.collections import LineCollection
from scipy.integrate import odeint
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
DURATION = 24.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_1c_deterministic"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Environment Matrix
C_STEEL     = '#606065'   # The Phantom Species / Mechanical Base
C_DARK      = '#202025'   # Joints
C_CYAN      = '#00FFFF'   # Node A / Sovereign Audit Phase
C_GOLD      = '#FFB300'   # Node B / Nursery 
C_AZURE     = '#007FFF'   # Nursery Structure
C_MAGENTA   = '#DE008A'   # The False Causation Tensor
C_MANTIS    = '#00FF00'   # Truth Verified / Terminal Green

# ------------------------------------------------------------------
# DOUBLE PENDULUM PHYSICS ENGINE (O(1) CACHED)
# ------------------------------------------------------------------
def get_derivs(state, t):
    theta1, z1, theta2, z2 = state
    c, s = np.cos(theta1-theta2), np.sin(theta1-theta2)
    
    num1 = M2 * L1 * z1**2 * s * c + M2 * G * np.sin(theta2) * c + \
           M2 * L2 * z2**2 * s - (M1 + M2) * G * np.sin(theta1)
    den1 = L1 * (M1 + M2 * s**2)
    
    num2 = -M2 * L2 * z2**2 * s * c + (M1 + M2) * (G * np.sin(theta1) * c - \
           L1 * z1**2 * s - G * np.sin(theta2))
    den2 = L2 * (M1 + M2 * s**2)
    
    return [z1, num1/den1, z2, num2/den2]

L1, L2 = 1.0, 1.0
M1, M2 = 1.0, 1.0
G = 9.8

time_arr = np.linspace(0, DURATION, TOTAL_FRAMES)
# High energy start exactly as LG-01
initial_state = [np.pi/2, 0, np.pi/2, 0] 
states = odeint(get_derivs, initial_state, time_arr)

# Scale physics vectors to the 1080x1920 matrix
SCALE = 220.0
OFFSET_Y = 150.0

NODE_1_X = SCALE * L1 * np.sin(states[:, 0])
NODE_1_Y = OFFSET_Y - SCALE * L1 * np.cos(states[:, 0])
NODE_2_X = NODE_1_X + SCALE * L2 * np.sin(states[:, 2])
NODE_2_Y = NODE_1_Y - SCALE * L2 * np.cos(states[:, 2])

def draw_industrial_grid(ax):
    """Draw the Structural Matrix"""
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

    # Coordinates for this exact frame
    x1, y1 = NODE_1_X[f], NODE_1_Y[f]
    x2, y2 = NODE_2_X[f], NODE_2_Y[f]

    # 1. STATE PROGRESSIONS
    # ---------------------
    T_AUDIT_START = 8.0
    T_AUDIT_END = 10.0
    T_PHANTOM_REVEAL = 12.0

    # The Logic Sweep Plane (Moves from Y=960 to Y=-960)
    sweep_y = -9999
    if T_AUDIT_START <= t <= T_AUDIT_END:
        prg = (t - T_AUDIT_START) / (T_AUDIT_END - T_AUDIT_START)
        sweep_y = 960 - (1920 * prg)
    elif t < T_AUDIT_START:
        sweep_y = 961
    
    alpha_phantom = np.clip((t - T_PHANTOM_REVEAL) / 3.0, 0.0, 1.0)
    alpha_lie = np.clip(1.0 - (t - T_PHANTOM_REVEAL) / 1.0, 0.0, 1.0)

    # Draw Sweep Effect
    if T_AUDIT_START <= t <= T_AUDIT_END:
        ax.plot([-540, 540], [sweep_y, sweep_y], color=C_CYAN, lw=8, zorder=30)
        ax.fill_between([-540, 540], sweep_y, sweep_y+200, color=C_CYAN, alpha=0.15, zorder=29)

    # 2. RENDER THE Z-AXIS PHANTOM SPECIES (THE TRUTH)
    # ------------------------------------------------
    if alpha_phantom > 0:
        VP_X1, VP_Y1 = -200, 800
        VP_X2, VP_Y2 = 200, 800

        ax.add_patch(patches.Rectangle((-300, 700), 200, 260, facecolor=C_TITANIUM, edgecolor=C_STEEL, lw=3, alpha=alpha_phantom*0.8, zorder=2))
        ax.add_patch(patches.Rectangle((100, 700), 200, 260, facecolor=C_TITANIUM, edgecolor=C_STEEL, lw=3, alpha=alpha_phantom*0.8, zorder=2))

        ax.plot([VP_X1, x1], [VP_Y1, y1], color=C_STEEL, lw=16, solid_capstyle='round', alpha=alpha_phantom, zorder=4)
        ax.plot([VP_X2, x2], [VP_Y2, y2], color=C_STEEL, lw=12, solid_capstyle='round', alpha=alpha_phantom, zorder=4)
        
        ax.plot([x1, x1 - (x1 - VP_X1)*0.2], [y1, y1 - (y1 - VP_Y1)*0.2], color=C_BG, lw=6, alpha=alpha_phantom, zorder=4.1)
        ax.plot([x2, x2 - (x2 - VP_X2)*0.2], [y2, y2 - (y2 - VP_Y2)*0.2], color=C_BG, lw=4, alpha=alpha_phantom, zorder=4.1)

    # 3. RENDER THE PENDULUM (DUAL STATES: NURSERY VS INDUSTRIAL)
    # -----------------------------------------------------------
    c_anchor = C_AZURE if 0 > sweep_y else C_DARK
    ax.add_patch(patches.Circle((0, OFFSET_Y), 20, facecolor=c_anchor, zorder=11))

    if y1 > sweep_y:
        ax.plot([0, x1], [OFFSET_Y, y1], color=C_AZURE, lw=20, solid_capstyle='round', zorder=9)
    else:
        ax.plot([0, x1], [OFFSET_Y, y1], color=C_STEEL, lw=8, zorder=9)

    if y2 > sweep_y:
        ax.plot([x1, x2], [y1, y2], color=C_AZURE, lw=20, solid_capstyle='round', zorder=9)
    else:
        if alpha_lie > 0:
            ax.plot([x1, x2], [y1, y2], color=mcolors.to_rgba(C_MAGENTA, alpha_lie), lw=6, linestyle='dashed', zorder=9)

    if y1 > sweep_y:
        ax.add_patch(patches.Circle((x1, y1), 35, color=C_GOLD, zorder=10))
    else:
        ax.add_patch(patches.Rectangle((x1-25, y1-25), 50, 50, facecolor=C_BG, edgecolor=C_CYAN, lw=5, zorder=20))
        ax.add_patch(patches.Circle((x1, y1), 10, color=C_DARK, zorder=21))

    if y2 > sweep_y:
        ax.add_patch(patches.Circle((x2, y2), 35, color=C_CYAN, zorder=10))
    else:
        ax.add_patch(patches.Rectangle((x2-25, y2-25), 50, 50, facecolor=C_BG, edgecolor=C_GOLD, lw=5, zorder=20))
        ax.add_patch(patches.Circle((x2, y2), 10, color=C_DARK, zorder=21))

    # Memory Trace (SOVEREIGN FIX: np.clip applied to alpha boundary)
    if t < T_AUDIT_END:
        trace_len = min(60, f)
        if trace_len > 1:
            t_x = NODE_2_X[f-trace_len:f]
            t_y = NODE_2_Y[f-trace_len:f]
            pts = np.array([t_x, t_y]).T.reshape(-1, 1, 2)
            segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
            
            # Absolute dimensional bounding box [0.0, 1.0]
            max_alpha = np.clip((T_AUDIT_END - t) / 2.0, 0.0, 1.0)
            alphas = np.linspace(0.0, max_alpha, trace_len-1)
            
            lc = LineCollection(segs, colors=C_AZURE, linewidths=8, alpha=alphas, joinstyle='round', capstyle='round', zorder=8)
            ax.add_collection(lc)

    # ====================================================
    # 4. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)

    ax.text(-500, 890, "LG-1c :: THE DETERMINISTIC PENDULUM", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] Z-AXIS PHANTOM SPECIES // CHAOS THEORY ANNULLED", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    if t < T_AUDIT_START:
        state_code = "NURSERY MODE // 2D CHAOS OBSERVATION ACTIVE"
        c_state = C_AZURE
        aud_code = "ILLUSION: NODE A GOVERNS NODE B TRAJECTORY"
        ca = C_MAGENTA
    elif t < T_PHANTOM_REVEAL:
        state_code = "SOVEREIGN AUDIT // STRIPPING NURSERY MAPPING"
        c_state = C_CYAN
        aud_code = "EXPOSING FALSE CAUSATION TENSOR"
        ca = C_MAGENTA
    else:
        state_code = "Z-AXIS KINEMATICS COMPLETELY REVEALED"
        c_state = C_MANTIS
        aud_code = "TATH\u0100T\u0100 // INDEPENDENT DETERMINISTIC HARDWARE"
        ca = C_MANTIS

    ax.text(-500, -760, "SYS_01 [TOPOLOGICAL STATE]   :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, state_code, color=c_state, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [NODE INTERSECTION]   :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, aud_code, color=ca, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "STRUCTURAL LOAD AUDIT        :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    sys_health = "SYSTEM NOMINAL" if t < T_AUDIT_START else "BARE-METAL PARAMETERS LOCKED"
    ax.text(20, -840, sys_health, color=C_STEEL, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=c_state, zorder=83))

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
    print(f"LG-1c: DETERMINISTIC PENDULUM [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
