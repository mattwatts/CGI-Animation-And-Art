"""
SOVEREIGN CODE: logic_garden_321d_dr_tensor.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 321d (Dielectronic Recombination // 2-Step Autoionization Resonance)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Seamless 10.0s Quantum Kinematic Loop. O(1) Doubly-Excited State Bounding Boxes.
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
OUT_DIR = "frames_321d_dr_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Upper Orbital Scaffolding
C_STEEL     = '#606065'   # Track Architecture
C_DARK      = '#202025'   # Ground State Core
C_CYAN      = '#00FFFF'   # Free Electron Payload
C_BLUE      = '#0088FF'   # Bound Electron Payload (Distinguishable purely for tracking)
C_TRANSFER  = '#FF0055'   # Inter-Electron Energy Transfer Beam (Magenta)
C_DEFECT    = '#FF6600'   # Doubly-Excited Resonance Flack (Amber)
C_PHOTON    = '#FFB300'   # Stabilizing Radiation
C_WHITE     = '#FFFFFF'

# ------------------------------------------------------------------
# O(1) KINEMATIC GEOMETRY
# ------------------------------------------------------------------
def draw_carrier(ax, x, y, base_color, alpha=1.0):
    # Industrial Carrier Bracket
    for r, c, a in [(22, C_TEXT, alpha), (18, base_color, alpha), (6, C_WHITE, alpha*0.9)]:
        pts = np.array([[0, -r], [r, 0], [0, r], [-r, 0]])
        ax.add_patch(patches.Polygon(pts + [x, y], facecolor=c, zorder=10))
        
def draw_resonance_cage(ax, x, y_top, y_bottom, intensity, alpha):
    """Generates the unstable bounding box for the doubly-excited phase"""
    w = 60 + (intensity * 20)
    rect = patches.Rectangle((x - w/2, y_bottom - 40), w, (y_top - y_bottom) + 80, 
                             facecolor=C_DEFECT, alpha=alpha * intensity * 0.4, zorder=8)
    ax.add_patch(rect)
    
    # Rigid containment barriers cracking under thermal stress
    out_rect = patches.Rectangle((x - w/2 - 10, y_bottom - 50), w + 20, (y_top - y_bottom) + 100, 
                                 facecolor='none', edgecolor=C_TRANSFER, lw=3 + intensity*4, alpha=alpha * intensity, zorder=8.1)
    ax.add_patch(out_rect)

def render_frame(packet):
    f, phase_ratio = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    cx, cy = 0, 0
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)

    # 1. THE IONIC ORBITAL TRACKS
    # Three discrete structural ion columns
    TRK_COORDS = [-330, 0, 330]
    
    # Horizontal States Lineage
    Y_CONT = 800
    Y_UPPER = 250
    Y_LOWER = 50
    Y_GROUND = -350
    
    # Base structural rails
    for tk in TRK_COORDS:
        ax.plot([tk, tk], [-800, 900], color=C_STEEL, lw=1.5, alpha=0.3, zorder=1)
        ax.axhline(Y_UPPER, color=C_TITANIUM, lw=1, alpha=0.5, zorder=0.5)
        ax.axhline(Y_LOWER, color=C_TITANIUM, lw=1, alpha=0.5, zorder=0.5)
        ax.axhline(Y_GROUND, color=C_DARK, lw=2, linestyle='--', alpha=0.7, zorder=0.5)

    # 2. DIELECTRONIC KINEMATICS ENGINE
    for i, tk in enumerate(TRK_COORDS):
        t = (phase_ratio + i / 3.0) % 1.0
        
        # Absolute Fade Wrapping (0.0=Invis, 0.05=Solid, 0.9=Solid, 1.0=Invis)
        a_m = 1.0
        if t < 0.05: a_m = t / 0.05
        if t > 0.9:  a_m = (1.0 - t) / 0.1
        
        y_free = Y_CONT
        y_bound = Y_GROUND
        res_intensity = 0.0
        
        # PHASE A: KINEMATIC DELIVERY (0.0 to 0.20)
        if t < 0.20:
            drop_p = t / 0.20
            y_free = Y_CONT - (drop_p ** 1.5) * (Y_CONT - Y_UPPER) # Exponential slam
            draw_carrier(ax, tk, y_free, C_CYAN, a_m)
            draw_carrier(ax, tk, y_bound, C_BLUE, a_m)
            
        # PHASE B: CAPTURE & RECOIL (0.20 to 0.25)
        elif 0.20 <= t < 0.25:
            recoil_p = (t - 0.20) / 0.05
            y_free = Y_UPPER
            y_bound = Y_GROUND + (recoil_p ** 0.5) * (Y_LOWER - Y_GROUND)
            
            # The Mechanical Energy Transfer Piston (Magenta Bolt)
            ax.plot([tk, tk], [y_free, y_bound], color=C_TRANSFER, lw=10 * (1.0-recoil_p), alpha=a_m, zorder=9)
            ax.plot([tk, tk], [y_free, y_bound], color=C_WHITE, lw=4 * (1.0-recoil_p), alpha=a_m, zorder=9.1)
            
            draw_carrier(ax, tk, y_free, C_CYAN, a_m)
            draw_carrier(ax, tk, y_bound, C_BLUE, a_m)

        # PHASE C: DOUBLY-EXCITED RESONANCE [UNSTABLE] (0.25 to 0.45)
        elif 0.25 <= t < 0.45:
            y_free = Y_UPPER
            y_bound = Y_LOWER
            
            # High frequency stutter applied to both particles
            vibration = np.sin((t * 200) * np.pi) * 8
            
            # Pulsing resonance bracket
            res_intensity = abs(np.sin((t * 20) * np.pi))
            draw_resonance_cage(ax, tk, Y_UPPER, Y_LOWER, res_intensity, a_m)
            
            draw_carrier(ax, tk + vibration, y_free, C_CYAN, a_m)
            draw_carrier(ax, tk - vibration, y_bound, C_BLUE, a_m)

        # PHASE D: RADIATIVE STABILIZATION DROP (0.45 to 0.60)
        elif 0.45 <= t < 0.60:
            fall_p = (t - 0.45) / 0.15
            y_free = Y_UPPER
            y_bound = Y_LOWER - (fall_p ** 2) * (Y_LOWER - Y_GROUND)
            
            draw_carrier(ax, tk, y_free, C_CYAN, a_m)
            draw_carrier(ax, tk, y_bound, C_BLUE, a_m)

        # PHASE E: PHOTON EMISSION & ION STATE RESET (0.60 to 1.0)
        elif t >= 0.60:
            y_free = Y_UPPER
            y_bound = Y_GROUND
            
            # Stabilized Ion tracking
            draw_carrier(ax, tk, y_free, C_CYAN, a_m)
            draw_carrier(ax, tk, y_bound, C_BLUE, a_m)
            
            # 100% Rigid Transverse Photon Execution 
            p_age = (t - 0.60) / 0.40 # 0.0 to 1.0
            x_front = p_age * 600
            x_rear = max(0, x_front - 200) 
            
            if x_front > x_rear:
                xw = np.linspace(x_rear, x_front, 100)
                env = np.sin((xw - x_rear) / (x_front - x_rear) * np.pi) # Hanning Window
                yw_E = np.sin(xw * 0.15 - phase_ratio * 30 * np.pi) * 80 * env
                yw_B = np.sin(xw * 0.15 - phase_ratio * 30 * np.pi + np.pi/2) * 40 * env
                
                a_wave = max(0.0, 1.0 - (p_age * 1.2)) * a_m
                
                wave_y = Y_LOWER - 100 # Emits from the approximate center of the stabilization drop
                
                # Right Propagation
                ax.plot(tk + xw, wave_y + yw_E, color=C_PHOTON, lw=5, alpha=a_wave, zorder=20)
                ax.plot(tk + xw, wave_y + yw_B, color=C_TRANSFER, lw=2.5, alpha=a_wave*0.8, zorder=20)
                # Left Propagation
                ax.plot(tk - xw, wave_y + yw_E, color=C_PHOTON, lw=5, alpha=a_wave, zorder=20)
                ax.plot(tk - xw, wave_y + yw_B, color=C_TRANSFER, lw=2.5, alpha=a_wave*0.8, zorder=20)

    # 3. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    ax.text(-500, 880, "LG-321d :: DIELECTRONIC RECOMBINATION", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, 840, "[SFI-1.00] DOUBLY-EXCITED KINEMATICS // AUTOIONIZING RESONANCE", color=C_STEEL, fontsize=12, fontname='monospace', zorder=80)
    
    ax.add_patch(patches.Rectangle((-520, -920), 1040, 140, facecolor=C_TITANIUM, alpha=0.9, zorder=79))
    ax.text(-500, -825, "KINETIC ENERGY OVERRIDE: RADIATION DELAYED", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=80)
    
    pulse = abs(np.sin(phase_ratio * 3 * np.pi))
    ax.text(-500, -855, f"ION RESONANCE INSTABILITY: {pulse * 100:>05.2f} % Δ [DOUBLY-EXCITED]", color=C_DEFECT if pulse > 0.3 else C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=80)
    
    ax.add_patch(patches.Rectangle((-500, -880), 1000, 4, facecolor=C_STEEL, zorder=80))
    ax.add_patch(patches.Rectangle((-500, -880), 1000 * pulse, 4, facecolor=C_DEFECT, zorder=81))

    # Architectural Strata Callouts
    ax.text(-500, 260, "EXCITED ORBITAL A (n_u) // CAPTURE TRENCH", color=C_TITANIUM, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, 60, "EXCITED ORBITAL B (n_l) // RECOIL TRENCH", color=C_TITANIUM, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, -380, "GROUND ORBITAL (n_g) // ION CORE", color=C_DARK, fontsize=10, fontname='monospace', weight='bold', zorder=80)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0)
    fig.clf(); plt.close(fig); gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-321d: DIELECTRONIC RECOMBINATION [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
