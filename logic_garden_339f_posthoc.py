"""
SOVEREIGN CODE: logic_garden_339f_posthoc.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Vectorization
SCENE: Logic Garden 339f (Post Hoc Ergo Propter Hoc // Phantom Species Z-Axis)
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
OUT_DIR = "frames_339f_posthoc"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Environment Matrix
C_STEEL     = '#606065'   # The Phantom Species / Mechanical Base
C_DARK      = '#202025'   # Joints and Couplings
C_CYAN      = '#00FFFF'   # Node A / Sovereign Audit Phase
C_GOLD      = '#FFB300'   # Node B
C_MAGENTA   = '#FF0055'   # The False Causation Tensor / Cognitive Lie
C_MANTIS    = '#00FF00'   # Truth Verified / Terminal Green

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

    # 1. KINEMATIC GEOMETRY LOGIC
    # The Phantom Species: A massive camshaft operating at Z-axis
    CAM_X = 0
    CAM_Y = 300
    CAM_R = 140
    ROD_L = 400
    
    # Track Constraints
    X_A = -200
    X_B = 200
    
    # Angular Kinetics (Rad/Sec)
    OMEGA = 2.5
    THETA_A = -t * OMEGA
    THETA_B = (-t * OMEGA) - (np.pi / 4.0) # B lags A strictly by 45 degrees

    # Crank positions (The hidden drivers)
    Crank_A_X = CAM_X + CAM_R * np.cos(THETA_A)
    Crank_A_Y = CAM_Y + CAM_R * np.sin(THETA_A)
    
    Crank_B_X = CAM_X + CAM_R * np.cos(THETA_B)
    Crank_B_Y = CAM_Y + CAM_R * np.sin(THETA_B)

    # Connecting Rod Physics (O(1) geometric intersection)
    Dx_A = X_A - Crank_A_X
    Dy_A = np.sqrt(ROD_L**2 - Dx_A**2)
    Node_A_Y = Crank_A_Y - Dy_A

    Dx_B = X_B - Crank_B_X
    Dy_B = np.sqrt(ROD_L**2 - Dx_B**2)
    Node_B_Y = Crank_B_Y - Dy_B

    # 2. STATE PROGRESSIONS
    T_AUDIT_START = 8.0
    T_AUDIT_END = 12.0
    
    alpha_phantom = np.clip((t - T_AUDIT_START) / 2.0, 0.0, 1.0)
    alpha_lie = np.clip(1.0 - (t - 8.5) / 1.0, 0.0, 1.0)

    if t < T_AUDIT_START:
        state_code = "[01] 2D CHRONOLOGICAL OBSERVATION ACTIVE"
        c_state = C_MAGENTA
        aud_code = "BLIND TO Z-AXIS // HALLUCINATING TORQUE"
    elif t < T_AUDIT_END:
        state_code = "[02] PHANTOM SPECIES REVEALED"
        c_state = C_CYAN
        aud_code = "SOVEREIGN AUDIT // SCANNING ORTHOGONAL Z-AXIS"
    else:
        state_code = "[03] CAUSALITY COMPLETELY NULLIFIED"
        c_state = C_MANTIS
        aud_code = "TATH\u0100T\u0100 // TRUE KINEMATIC DRIVER VERIFIED"

    # 3. RENDER THE PHANTOM SPECIES (THE Z-AXIS TRUTH)
    if alpha_phantom > 0:
        # Ghost Engine Block
        ax.add_patch(patches.RegularPolygon((CAM_X, CAM_Y), numVertices=12, radius=180, facecolor=C_TITANIUM, edgecolor=C_STEEL, lw=3, alpha=alpha_phantom*0.6, zorder=2))
        ax.add_patch(patches.Circle((CAM_X, CAM_Y), 30, facecolor=C_DARK, alpha=alpha_phantom, zorder=3))
        
        # Piston Connecting Rods
        ax.plot([Crank_A_X, X_A], [Crank_A_Y, Node_A_Y], color=C_STEEL, lw=8, solid_capstyle='round', alpha=alpha_phantom, zorder=4)
        ax.plot([Crank_B_X, X_B], [Crank_B_Y, Node_B_Y], color=C_STEEL, lw=8, solid_capstyle='round', alpha=alpha_phantom, zorder=4)
        
        # Internal Structural Drive Spokes
        ax.plot([CAM_X, Crank_A_X], [CAM_Y, Crank_A_Y], color=C_DARK, lw=6, alpha=alpha_phantom, zorder=5)
        ax.plot([CAM_X, Crank_B_X], [CAM_Y, Crank_B_Y], color=C_DARK, lw=6, alpha=alpha_phantom, zorder=5)
        
        # Cranks
        ax.add_patch(patches.Circle((Crank_A_X, Crank_A_Y), 15, facecolor=C_CYAN, edgecolor=C_DARK, lw=2, alpha=alpha_phantom, zorder=6))
        ax.add_patch(patches.Circle((Crank_B_X, Crank_B_Y), 15, facecolor=C_GOLD, edgecolor=C_DARK, lw=2, alpha=alpha_phantom, zorder=6))

    # 4. RENDER THE FALSE CAUSATION (THE 2D LIE)
    if alpha_lie > 0:
        # A massive, high visual priority arrow falsely linking A to B
        c_arrow = mcolors.to_rgba(C_MAGENTA, alpha_lie)
        # Because A generally leads B, draw from A to B with pulsing energy
        pulse = 4 + 2 * np.sin(t*20)
        ax.plot([X_A+30, X_B-30], [Node_A_Y, Node_B_Y], color=c_arrow, lw=pulse, linestyle='dashed', zorder=15)
        ax.scatter((X_A+X_B)/2, (Node_A_Y+Node_B_Y)/2, s=200, c=C_BG, edgecolors=c_arrow, lw=3, marker='>', zorder=16)

    # 5. RENDER THE OBSERVABLE NODES & TRACKS
    # Rigid X-Tracks
    ax.add_patch(patches.Rectangle((X_A-40, -600), 80, 1000, facecolor=C_TITANIUM, edgecolor=C_STEEL, lw=2, alpha=0.5, zorder=8))
    ax.add_patch(patches.Rectangle((X_B-40, -600), 80, 1000, facecolor=C_TITANIUM, edgecolor=C_STEEL, lw=2, alpha=0.5, zorder=8))
    ax.plot([X_A, X_A], [-600, 400], color=C_DARK, lw=4, zorder=9)
    ax.plot([X_B, X_B], [-600, 400], color=C_DARK, lw=4, zorder=9)

    # The Nodes themselves (Operating cleanly in observable 1D tracks)
    ax.add_patch(patches.Rectangle((X_A-30, Node_A_Y-25), 60, 50, facecolor=C_BG, edgecolor=C_CYAN, lw=5, zorder=20))
    ax.add_patch(patches.Rectangle((X_B-30, Node_B_Y-25), 60, 50, facecolor=C_BG, edgecolor=C_GOLD, lw=5, zorder=20))

    # Sovereign Audit Sweep Visual
    if T_AUDIT_START <= t <= T_AUDIT_END:
        prg = (t - T_AUDIT_START) / 4.0
        scan_y = 800 - prg * 1600
        ax.plot([-540, 540], [scan_y, scan_y], color=C_CYAN, lw=6, zorder=30)
        ax.fill_between([-540, 540], scan_y, scan_y+200, color=C_CYAN, alpha=0.15, zorder=29)

    # ====================================================
    # 6. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    # Top Header [Strict Tuples]
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-339f :: POST HOC ERGO PROPTER HOC TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] CHRONOLOGICAL ILLUSION / HIDDEN Z-AXIS PHANTOM SPECIES", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    # Bottom Telemetry HUD
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    ax.text(-500, -760, "SYS_01 [OBSERVED DELTA]      :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, "NODE A PRECEDES NODE B VERIFIED KINEMATICALLY", color=C_STEEL, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [COGNITIVE ENGINE]    :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, state_code, color=c_state, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "STRUCTURAL AUDIT [Z-AXIS]    :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, aud_code, color=C_MAGENTA if t < T_AUDIT_START else (C_MANTIS if t > T_AUDIT_END else C_CYAN), fontsize=15, fontname='monospace', weight='bold', zorder=82)

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
    print(f"LG-339f: POST HOC TENSOR (PHANTOM SPECIES) [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
