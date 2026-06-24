"""
SOVEREIGN CODE: logic_garden_321a_recombination_tensor.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 321a (Radiative Recombination // Solid-State Laser)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Seamless 10.0s Quantum Kinematic Loop. Rigid O(1) wave propagation.
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
OUT_DIR = "frames_321a_recombination_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Conduction Band Scaffold
C_STEEL     = '#606065'   # Structural Shadow
C_DARK      = '#202025'   # Valence Band Scaffold
C_ELECTRON  = '#00FFFF'   # High Energy Payload
C_HOLE      = '#1A1A20'   # Empty State Void
C_PHOTON    = '#FFB300'   # Electromagnetic Emission (Gold)
C_MAGENTA   = '#FF0055'   # Magnetic Phase Sine
C_WHITE     = '#FFFFFF'   # Recombination Flash

# ------------------------------------------------------------------
# O(1) CARRIER GEOMETRY
# ------------------------------------------------------------------
def draw_electron(ax, y, alpha=1.0):
    for r, c, a in [(24, C_TEXT, alpha), (20, C_ELECTRON, alpha), (8, C_WHITE, alpha*0.9)]:
        pts = np.array([[0, -r], [r, 0], [0, r], [-r, 0]])
        ax.add_patch(patches.Polygon(pts + [0, y], facecolor=c, zorder=10))

def draw_hole(ax, y, alpha=1.0):
    # The physical receptacle
    pts_out = np.array([[0, -28], [28, 0], [0, 28], [-28, 0]])
    ax.add_patch(patches.Polygon(pts_out + [0, y], facecolor=C_TEXT, alpha=alpha, zorder=9))
    # Inner void
    pts_in = np.array([[0, -18], [18, 0], [0, 18], [-18, 0]])
    ax.add_patch(patches.Polygon(pts_in + [0, y], facecolor=C_HOLE, alpha=alpha, zorder=9.1))
    
    # Locking Brackets
    ax.plot([-35, -20], [y, y], color=C_MAGENTA, lw=2, zorder=9.2, alpha=alpha)
    ax.plot([20, 35], [y, y], color=C_MAGENTA, lw=2, zorder=9.2, alpha=alpha)

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

    # 1. INDUSTRIAL GRID (The Background Crystal Lattice)
    for gy in range(-900, 1000, 150):
        ax.axhline(gy, color=C_STEEL, lw=1, alpha=0.15, zorder=0)

    # 2. BANDGAP STRUCTURAL SCAFFOLD (Conduction and Valence Delivery Tracks)
    # The Optical Cavity (Laser guide)
    ax.add_patch(patches.Rectangle((-540, 20), 1080, 160, facecolor='#F4F4F8', edgecolor='none', zorder=0.5))
    ax.axhline(100, color=C_STEEL, lw=1.5, linestyle='--', alpha=0.4, zorder=0.6) # X-axis baseline for recombination
    
    # Top Track (Conduction Band E_c)
    ax.add_patch(patches.Rectangle((-45, 100), 90, 860, facecolor=C_TITANIUM, edgecolor=C_TEXT, lw=2, zorder=1))
    ax.plot([-18, -18], [100, 960], color=C_STEEL, lw=2, alpha=0.5, zorder=1.1)
    ax.plot([18, 18], [100, 960], color=C_STEEL, lw=2, alpha=0.5, zorder=1.1)

    # Bottom Track (Valence Band E_v)
    ax.add_patch(patches.Rectangle((-45, -960), 90, 1060, facecolor=C_DARK, edgecolor=C_TEXT, lw=2, zorder=1))
    ax.plot([-18, -18], [-960, 100], color=C_STEEL, lw=2, alpha=0.2, zorder=1.1)
    ax.plot([18, 18], [-960, 100], color=C_STEEL, lw=2, alpha=0.2, zorder=1.1)

    # 3. KINEMATICS OF RADIATIVE RECOMBINATION
    # 5 isolated staggered events seamlessly looping over 10.0s
    N_EVENTS = 5
    for i in range(N_EVENTS):
        t = (phase_ratio + i / float(N_EVENTS)) % 1.0
        
        # PHASE A: CARRIER APPROACH & INJECTION (0.0 to 0.4)
        if t < 0.4:
            e_phase = t / 0.4
            # Electron drops from high potential +700 down to annihilation coordinate +100
            y_e = 700 - (e_phase * 600)
            # Hole rises from deep lattice -500 up to +100
            y_h = -500 + (e_phase * 600)
            
            # Smooth fade-in at the bounds
            a_carry = 1.0 if e_phase > 0.1 else (e_phase / 0.1)
            
            draw_electron(ax, y_e, alpha=a_carry)
            draw_hole(ax, y_h, alpha=a_carry)

        # PHASE B: STRUCTURAL ANNEALING & BLAST (0.395 to 0.405)
        if 0.395 < t < 0.415:
            blast_scale = 1.0 - abs(t - 0.405) / 0.010
            ax.add_patch(patches.Circle((0, 100), radius=120 * blast_scale, color=C_ELECTRON, alpha=blast_scale*0.8, zorder=7))
            ax.add_patch(patches.Circle((0, 100), radius=60 * blast_scale, color=C_WHITE, alpha=blast_scale, zorder=7.1))

        # PHASE C: PHOTON ELECTROMAGNETIC EMISSION (0.4 to 1.0)
        if t >= 0.4:
            p_age = (t - 0.4) / 0.6  # Normalized 0.0 to 1.0
            x_front = p_age * 700
            x_rear = max(0, x_front - 280) # Wave packet length
            
            if x_front > x_rear:
                xw = np.linspace(x_rear, x_front, 150)
                # Hanning Window envelope forces wave to 0 amplitude at the front/rear boundaries
                env = np.sin((xw - x_rear) / (x_front - x_rear) * np.pi)
                
                # The wave frequency mathematically aligns so it loops purely
                yw_E = np.sin(xw * 0.12 - phase_ratio * 20 * np.pi) * 90 * env
                yw_B = np.sin(xw * 0.12 - phase_ratio * 20 * np.pi + np.pi/2) * 45 * env
                
                alpha_wave = max(0.0, 1.0 - p_age*1.2) # Wave attenuates flawlessly to 0 before wrap
                
                # Right Propagation
                ax.plot(xw, 100 + yw_E, color=C_PHOTON, lw=5, alpha=alpha_wave, zorder=8)
                ax.plot(xw, 100 + yw_B, color=C_MAGENTA, lw=2.5, alpha=alpha_wave*0.8, zorder=8)
                
                # Left Propagation
                ax.plot(-xw, 100 + yw_E, color=C_PHOTON, lw=5, alpha=alpha_wave, zorder=8)
                ax.plot(-xw, 100 + yw_B, color=C_MAGENTA, lw=2.5, alpha=alpha_wave*0.8, zorder=8)

    # 4. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    ax.text(-500, 880, "LG-321a :: RADIATIVE RECOMBINATION TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, 840, "[SFI-1.00] LED/LASER DIODE KINEMATICS // BANDGAP EXCITATION", color=C_STEEL, fontsize=12, fontname='monospace', zorder=80)
    
    # Mathematical Physics Readouts
    ax.add_patch(patches.Rectangle((-520, -900), 1040, 150, facecolor=C_TITANIUM, alpha=0.9, zorder=79))

    ax.text(-500, -805, "ENERGY MASS CONVERSIONS: E = hc / λ", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=80)
    
    # Telemetry Pulse
    pulse = abs(np.sin(phase_ratio * np.pi * N_EVENTS))
    ax.text(-500, -840, f"PHOTON FLUX DENSITY: {pulse:.4f} Δ [LOCKED]", color=C_PHOTON if pulse > 0.5 else C_TEXT, fontsize=14, fontname='monospace', zorder=80)
    
    ax.add_patch(patches.Rectangle((-500, -865), 1000, 4, facecolor=C_STEEL, zorder=80))
    ax.add_patch(patches.Rectangle((-500 + 490*(1-pulse), -865), 20 + 980*pulse, 4, facecolor=C_PHOTON, zorder=81))

    # Structural Callouts
    ax.text(-250, 400, "CONDUCTION BAND (E_c)\nELECTRON VECTOR", color=C_ELECTRON, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    ax.plot([-95, -45], [410, 410], color=C_ELECTRON, lw=1.5, zorder=80)
    
    ax.text(120, -400, "VALENCE BAND (E_v)\nHOLE VECTOR", color=C_TEXT, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    ax.plot([45, 110], [-390, -390], color=C_TEXT, lw=1.5, zorder=80)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0)
    fig.clf(); plt.close(fig); gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-321a: RECOMBINATION KINEMATIC TENSOR [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
