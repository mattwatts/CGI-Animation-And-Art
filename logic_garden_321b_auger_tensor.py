"""
SOVEREIGN CODE: logic_garden_321b_auger_tensor.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 321b (Auger Recombination // Non-Radiative Loss)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Seamless 10.0s Quantum Kinematic Loop. Rigid O(1) Thermodynamic Spallation.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
DURATION = 10.0  # 10.0 Second Seamless Loop
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_321b_auger_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Conduction Band Scaffold
C_STEEL     = '#606065'   # Structural Shadow
C_DARK      = '#202025'   # Valence Band Scaffold
C_ELECTRON  = '#00FFFF'   # High Energy Payload
C_HOLE      = '#1A1A20'   # Empty State Void
C_TRANSFER  = '#FF0055'   # Non-Radiative Energy Surge (Magenta)
C_HEAT      = '#FF2200'   # Phonon Spallation / Heat Exhaust
C_WHITE     = '#FFFFFF'   # Collision Core

# ------------------------------------------------------------------
# O(1) CARRIER GEOMETRY
# ------------------------------------------------------------------
def draw_electron(ax, x, y, alpha=1.0):
    for r, c, a in [(24, C_TEXT, alpha), (20, C_ELECTRON, alpha), (8, C_WHITE, alpha*0.9)]:
        pts = np.array([[0, -r], [r, 0], [0, r], [-r, 0]])
        ax.add_patch(patches.Polygon(pts + [x, y], facecolor=c, zorder=10))

def draw_hole(ax, x, y, alpha=1.0):
    pts_out = np.array([[0, -28], [28, 0], [0, 28], [-28, 0]])
    ax.add_patch(patches.Polygon(pts_out + [x, y], facecolor=C_TEXT, alpha=alpha, zorder=9))
    pts_in = np.array([[0, -18], [18, 0], [0, 18], [-18, 0]])
    ax.add_patch(patches.Polygon(pts_in + [x, y], facecolor=C_HOLE, alpha=alpha, zorder=9.1))
    ax.plot([-35+x, -20+x], [y, y], color=C_TRANSFER, lw=2, zorder=9.2, alpha=alpha)
    ax.plot([20+x, 35+x], [y, y], color=C_TRANSFER, lw=2, zorder=9.2, alpha=alpha)

def draw_phonon_shear(ax, x, y, size_ratio, alpha):
    # Rigid geometric spallation propagating bilaterally to signify structural vibration
    w = 50 * size_ratio
    h = 25 * size_ratio
    
    # Left Shear
    pts_l = np.array([[-15-w, y-h/2], [-15-w-15, y], [-15-w, y+h/2], [-15-w/2, y]])
    # Right Shear
    pts_r = np.array([[15+w, y-h/2], [15+w+15, y], [15+w, y+h/2], [15+w/2, y]])
    
    ax.add_patch(patches.Polygon(pts_l, facecolor=C_HEAT, alpha=alpha, zorder=8))
    ax.add_patch(patches.Polygon(pts_r, facecolor=C_HEAT, alpha=alpha, zorder=8))
    # Core linkage
    ax.plot([-15-w, 15+w], [y, y], color=C_HEAT, lw=1.5, alpha=alpha, zorder=8)

def render_frame(packet):
    f, phase_ratio = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)

    # 1. THE THERMODYNAMIC CRYSTAL LATTICE
    for gy in range(-900, 1000, 150):
        ax.axhline(gy, color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)

    # 2. BANDGAP STRUCTURAL SCAFFOLD
    # Central bandgap void
    ax.add_patch(patches.Rectangle((-540, -100), 1080, 200, facecolor='#F4F4F8', edgecolor='none', zorder=0.5))
    ax.axhline(100, color=C_STEEL, lw=1.5, linestyle='--', alpha=0.6, zorder=0.6) # E_c edge
    ax.axhline(-100, color=C_STEEL, lw=1.5, linestyle='--', alpha=0.6, zorder=0.6) # E_v edge
    
    # Conduction Band (Top)
    ax.add_patch(patches.Rectangle((-540, 100), 1080, 860, facecolor=C_TITANIUM, alpha=0.2, zorder=1))
    # Valence Band (Bottom)
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 860, facecolor=C_DARK, alpha=0.05, zorder=1))

    # Dual Tracks (The Auger Physics Rails)
    TRK_L = -180
    TRK_R = 180
    for tk in [TRK_L, TRK_R]:
        ax.plot([tk, tk], [-960, 960], color=C_STEEL, lw=2, alpha=0.4, zorder=1.1)

    # 3. KINEMATICS OF AUGER RECOMBINATION
    N_EVENTS = 3
    for i in range(N_EVENTS):
        t = (phase_ratio + i / float(N_EVENTS)) % 1.0
        
        # Smooth master alpha constraints to enforce seamless 0/1 wrap
        alpha_master = 1.0
        if t < 0.05: alpha_master = t / 0.05
        if t > 0.95: alpha_master = (1.0 - t) / 0.05

        # PHASE A: KINEMATIC APPROACH (0.0 to 0.25)
        if t < 0.25:
            e1_phase = t / 0.25
            y_e1 = 500 - (e1_phase * 400)
            y_h1 = -500 + (e1_phase * 400)
            
            draw_electron(ax, TRK_L, y_e1, alpha=alpha_master)
            draw_hole(ax, TRK_L, y_h1, alpha=alpha_master)
            draw_electron(ax, TRK_R, 100, alpha=alpha_master) # 3rd target holds at edge

        # PHASE B: ANNIHILATION & TRANSFER SHOCK (0.245 to 0.265)
        if 0.245 < t < 0.265:
            transfer_scale = 1.0 - abs(t - 0.255) / 0.010
            # Collision flash on Track L
            ax.add_patch(patches.Circle((TRK_L, 100), radius=90 * transfer_scale, color=C_TRANSFER, alpha=transfer_scale*0.8, zorder=7))
            
            # Rigid energy transmission matrix bridging Track L to Track R
            ax.plot([TRK_L, TRK_L + (360 * transfer_scale)], [100, 100], color=C_TRANSFER, lw=8 * transfer_scale, zorder=6)
            ax.plot([TRK_L, TRK_L + (360 * transfer_scale)], [100, 100], color=C_WHITE, lw=3 * transfer_scale, zorder=6.1)

        # PHASE C: AUGER EXCITATION (0.25 to 0.40)
        if 0.25 <= t < 0.4:
            launch_p = (t - 0.25) / 0.15
            # Electron 2 is violently catapulted deep into conduction band
            y_e2 = 100 + np.sin(launch_p * np.pi/2) * 650 
            draw_electron(ax, TRK_R, y_e2, alpha=alpha_master)

        # PHASE D: THERMALIZATION & PHONON SPALLATION (0.4 to 0.9)
        if 0.4 <= t < 0.9:
            fall_p = (t - 0.4) / 0.5
            # Rigid O(1) polynomial fall back to band edge
            y_e2 = 750 - (fall_p ** 1.5) * 650 
            draw_electron(ax, TRK_R, y_e2, alpha=alpha_master)
            
            # Generate Rigid Thermodynamic Phonons as Heat Waste
            phonon_levels = [600, 450, 300, 150]
            for pl in phonon_levels:
                # Calculate what phase 't' corresponds to this phonon's drop Y
                trigger_p = ((750 - pl) / 650.0) ** (1/1.5) 
                
                # If Electron 2 has fallen past this coordinate, spawn and expand heat shear
                if fall_p > trigger_p:
                    age = (fall_p - trigger_p) / (1.0 - trigger_p)
                    # Expand sideways and shrink/fade
                    p_scale = age * 3.0
                    p_alpha = max(0, 1.0 - (age * 1.5)) * alpha_master
                    if p_alpha > 0:
                        draw_phonon_shear(ax, TRK_R, pl, p_scale, p_alpha)

        # PHASE E: RESET (0.9 to 1.0)
        if t >= 0.9:
            draw_electron(ax, TRK_R, 100, alpha=alpha_master)

    # 4. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    ax.text(-500, 880, "LG-321b :: AUGER RECOMBINATION TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, 840, "[SFI-1.00] NON-RADIATIVE THERMODYNAMICS // EFFICIENCY LOSS", color=C_HEAT, fontsize=12, fontname='monospace', zorder=80)
    
    # Mathematical Physics Readouts
    ax.add_patch(patches.Rectangle((-520, -920), 1040, 170, facecolor=C_TITANIUM, alpha=0.9, zorder=79))

    ax.text(-500, -805, "ENERGY PARITY OVERRIDE: E_g → KE_carrier", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=80)
    
    # Loss Telemetry Pulse 
    pulse = abs(np.sin(phase_ratio * np.pi * N_EVENTS))
    # Invert pulse color logic: High intensity = Critical Thermal Loss
    ax.text(-500, -840, f"STRUCTURAL PHONON SPALLATION: {pulse * 100:>05.2f} % Δ [HEAT LOSS]", color=C_HEAT if pulse > 0.5 else C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=80)
    
    ax.add_patch(patches.Rectangle((-500, -865), 1000, 4, facecolor=C_STEEL, zorder=80))
    ax.add_patch(patches.Rectangle((-500, -865), 1000 * pulse, 4, facecolor=C_HEAT, zorder=81))

    # Structural Vector Callouts
    ax.text(-500, 300, "RECOMBINATION\nENGINE\n(TRACK 1)", color=C_TEXT, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    ax.plot([-360, -200], [280, 280], color=C_STEEL, lw=1.5, zorder=80)
    
    ax.text(360, 300, "AUGER\nTARGET\n(TRACK 2)", color=C_TEXT, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    ax.plot([200, 340], [280, 280], color=C_STEEL, lw=1.5, zorder=80)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0)
    fig.clf(); plt.close(fig); gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-321b: AUGER KINEMATIC TENSOR [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
