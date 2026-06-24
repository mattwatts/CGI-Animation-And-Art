"""
SOVEREIGN CODE: logic_garden_332_feynman_tensor.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Vectorization
SCENE: Logic Garden 332 (Feynman Spacetime Tensor // QED Scattering)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Seamless Loop. Absolute Camera Lock. O(1) Memory Eradication. CPT Parity.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.transforms as transforms
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
DURATION = 10.0  # 10.0 Second Spacetime Sweep
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_332_feynman_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # The Spacetime Blueprint (Past/Future)
C_STEEL     = '#606065'   # Heavy Muon Mass
C_DARK      = '#202025'   # Electron Mass Base
C_CYAN      = '#00FFFF'   # The "NOW" Scanning Plane / Normal Matter Spin
C_MAGENTA   = '#FF0055'   # Antimatter Parity Spin
C_GOLD      = '#FFB300'   # The Virtual Gauge Boson (Photon)
C_WHITE     = '#FFFFFF'

# -------- KINEMATIC VERTICES --------
V1_Y = -250  # Annihilation Vertex (Time 1)
V2_Y = 250   # Creation Vertex (Time 2)
START_Y = -800
END_Y = 800
TARGET_X = 300

def draw_feynman_arrow(ax, x, y, dx, dy, color):
    """Rigid O(1) mathematical arrow block. Immune to rendering engine drift."""
    angle = np.arctan2(dy, dx)
    trans = transforms.Affine2D().rotate(angle).translate(x, y) + ax.transData
    
    # Draw a sharp geometric chevron
    pts = np.array([[-12, -10], [12, 0], [-12, 10], [-6, 0]])
    poly = patches.Polygon(pts, facecolor=color, edgecolor='none', transform=trans, zorder=1)
    ax.add_patch(poly)

def render_frame(packet):
    f, phase_ratio = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    
    # ----------------------------------------------------
    # BARE-METAL CAMERA LOCK: ALL AUTO-SCALING ANNIHILATED
    # ----------------------------------------------------
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)
    ax.autoscale(False)

    # ----------------------------------------------------
    # 1. THE THEORETICAL SPACETIME BLUEPRINT
    # ----------------------------------------------------
    ax.plot([-TARGET_X, 0], [START_Y, V1_Y], color=C_TITANIUM, lw=4, zorder=0) # e- path
    ax.plot([TARGET_X, 0], [START_Y, V1_Y], color=C_TITANIUM, lw=4, zorder=0)  # e+ path
    ax.plot([0, -TARGET_X], [V2_Y, END_Y], color=C_TITANIUM, lw=4, zorder=0)   # mu- path
    ax.plot([0, TARGET_X], [V2_Y, END_Y], color=C_TITANIUM, lw=4, zorder=0)    # mu+ path
    
    # Virtual Photon Wavy Line (Blueprint)
    wave_y = np.linspace(V1_Y, V2_Y, 200)
    wave_x = 30 * np.sin((wave_y - V1_Y) * np.pi / 20)
    ax.plot(wave_x, wave_y, color=C_TITANIUM, lw=4, zorder=0)

    # Feynman Topological Arrows (Mathematically placed at midpoints)
    # The absolute law: Antimatter arrows point BACKWARDS in time.
    draw_feynman_arrow(ax, -TARGET_X/2, (START_Y + V1_Y)/2, TARGET_X, V1_Y - START_Y, C_TITANIUM) # e- (Forwards)
    draw_feynman_arrow(ax, TARGET_X/2, (START_Y + V1_Y)/2, TARGET_X, START_Y - V1_Y, C_TITANIUM)  # e+ (Backwards)
    
    draw_feynman_arrow(ax, -TARGET_X/2, (V2_Y + END_Y)/2, -TARGET_X, END_Y - V2_Y, C_TITANIUM)    # mu- (Forwards)
    draw_feynman_arrow(ax, TARGET_X/2, (V2_Y + END_Y)/2, -TARGET_X, V2_Y - END_Y, C_TITANIUM)     # mu+ (Backwards)

    # ----------------------------------------------------
    # 2. THE PHYSICAL "NOW" PLANE (TIME INTEGRATOR)
    # ----------------------------------------------------
    # Scan from -850 to +850 over 10 seconds
    Y_NOW = -850 + (phase_ratio * 1700)
    
    # Draw the mathematical threshold of the Present
    ax.plot([-540, 540], [Y_NOW, Y_NOW], color=C_CYAN, lw=2, linestyle='--', zorder=10)
    ax.add_patch(patches.Rectangle((-540, Y_NOW-40), 1080, 80, facecolor=C_CYAN, alpha=0.05, zorder=0.5))

    # ----------------------------------------------------
    # 3. KINEMATIC PARTICLE EXISTENCE (O(1) INTERSECTIONS)
    # ----------------------------------------------------
    # Particles only physically draw if the NOW plane intersects their history segment
    
    # A) Pre-Annihilation (Y in [START_Y, V1_Y])
    if START_Y <= Y_NOW <= V1_Y:
        ratio = (Y_NOW - START_Y) / (V1_Y - START_Y)
        
        # Electron (e-)
        ex = -TARGET_X + ratio * TARGET_X
        ey = Y_NOW
        ax.scatter(ex, ey, c=C_DARK, s=250, marker='o', edgecolors=C_CYAN, lw=3, zorder=15)
        ax.text(ex - 40, ey, r"$e^-$", color=C_TEXT, fontsize=18, fontweight='bold', fontstyle='italic', zorder=16)

        # Positron (e+)
        px = TARGET_X - ratio * TARGET_X
        py = Y_NOW
        ax.scatter(px, py, c=C_DARK, s=250, marker='o', edgecolors=C_MAGENTA, lw=3, zorder=15)
        ax.text(px + 40, py, r"$e^+$", color=C_TEXT, fontsize=18, fontweight='bold', fontstyle='italic', zorder=16)
        
        # High-energy compression lines as they approach
        if Y_NOW > V1_Y - 150:
            ax.plot([ex, px], [ey, py], color=C_MAGENTA, lw=2, alpha=ratio, zorder=14)

    # B) Gauge Mediation (Y in [V1_Y, V2_Y])
    if V1_Y < Y_NOW < V2_Y:
        # The physical photon location
        gx = 30 * np.sin((Y_NOW - V1_Y) * np.pi / 20)
        gy = Y_NOW
        
        # Massive energy packet
        ax.scatter(gx, gy, c=C_GOLD, s=400, edgecolors=C_BG, lw=4, zorder=15)
        ax.add_patch(patches.Circle((gx, gy), 45, facecolor='none', edgecolor=C_GOLD, lw=2, alpha=0.8, zorder=14))
        ax.text(60, gy, r"$\gamma$", color=C_GOLD, fontsize=24, fontweight='bold', zorder=16)

    # C) Pair Production (Y in [V2_Y, END_Y])
    if V2_Y <= Y_NOW <= END_Y:
        ratio = (Y_NOW - V2_Y) / (END_Y - V2_Y)
        
        # Muon (mu-) - Note: Muon is ~200x heavier than electron, we draw it larger and heavier.
        mx = -ratio * TARGET_X
        my = Y_NOW
        ax.scatter(mx, my, c=C_STEEL, s=380, marker='s', edgecolors=C_CYAN, lw=3, zorder=15)
        ax.text(mx - 50, my, r"$\mu^-$", color=C_TEXT, fontsize=18, fontweight='bold', fontstyle='italic', zorder=16)

        # Anti-Muon (mu+)
        amx = ratio * TARGET_X
        amy = Y_NOW
        ax.scatter(amx, amy, c=C_STEEL, s=380, marker='s', edgecolors=C_MAGENTA, lw=3, zorder=15)
        ax.text(amx + 50, amy, r"$\mu^+$", color=C_TEXT, fontsize=18, fontweight='bold', fontstyle='italic', zorder=16)

    # D) Vertex Action Explosions
    if abs(Y_NOW - V1_Y) < 30:
        pulse = 1.0 - (abs(Y_NOW - V1_Y)/30.0)
        ax.scatter(0, V1_Y, c=C_BG, s=1500 + 1000*pulse, edgecolors=C_MAGENTA, lw=5*pulse, alpha=pulse, zorder=16)
        
    if abs(Y_NOW - V2_Y) < 30:
        pulse = 1.0 - (abs(Y_NOW - V2_Y)/30.0)
        ax.scatter(0, V2_Y, c=C_BG, s=1500 + 1000*pulse, edgecolors=C_GOLD, lw=5*pulse, alpha=pulse, zorder=16)

    # ----------------------------------------------------
    # 4. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ----------------------------------------------------
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-332 :: FEYNMAN SPACETIME TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] QUANTUM ELECTRODYNAMICS (QED) // T-CHAN MATRIX", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)
    
    # Bottom Math HUD [Strict Tuple Enforcement]
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, -760, "DIRAC S-MATRIX AMPLITUDE EQUATION:", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    
    # QED Explicit Mathematics Rendering
    math_eq = r"$\mathcal{M} = \left[\bar{v}(p_2)(ie\gamma^\mu)u(p_1)\right] \left(\frac{-ig_{\mu\nu}}{q^2}\right) \left[\bar{u}(p_3)(ie\gamma^\nu)v(p_4)\right]$"
    ax.text(-500, -825, math_eq, color=C_DARK, fontsize=22, zorder=82)
    
    # Active State Tracking 
    if Y_NOW < V1_Y:
        sub_text = "STATE 1: e- / e+ APPROACH"
        HUD_COL = C_DARK
    elif Y_NOW < V2_Y:
        sub_text = "STATE 2: VIRTUAL PHOTON MEDIATION"
        HUD_COL = C_GOLD
    else:
        sub_text = "STATE 3: MUON PAIR CREATION"
        HUD_COL = C_STEEL

    ax.text(-500, -880, sub_text, color=HUD_COL, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.add_patch(patches.Rectangle((-500, -910), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -910), 1000 * phase_ratio, 6, facecolor=C_CYAN, zorder=83))

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
    print(f"LG-332: FEYNMAN SPACETIME TENSOR [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
