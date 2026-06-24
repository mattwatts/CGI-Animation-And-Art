"""
SOVEREIGN CODE: logic_garden_321c_defect_tensor.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 321c (SRH Defect-Assisted Recombination // Trap State Tensor)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Seamless 10.0s Quantum Kinematic Loop. Rigid O(1) Actuating Impurity Cages.
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
OUT_DIR = "frames_321c_defect_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Conduction Band Scaffold
C_STEEL     = '#606065'   # Structural Trap Architecture 
C_DARK      = '#202025'   # Valence Band Scaffold
C_ELECTRON  = '#00FFFF'   # High Energy Payload
C_HOLE      = '#1A1A20'   # Empty State Void
C_DEFECT    = '#FF6600'   # Industrial Amber (Impurity Energy Glow)
C_HEAT      = '#FF0055'   # Dull Thermal Phonon Decay
C_WHITE     = '#FFFFFF'   # Collision Core

# ------------------------------------------------------------------
# O(1) KINEMATIC GEOMETRY
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
    
def draw_trap(ax, x, y, clamp_ratio, glow_ratio):
    # dx handles the mechanical closure of the jaws around the trapped electron
    dx = 8 * clamp_ratio
    
    jaw_l = np.array([[-60+dx, 40], [-35+dx, 40], [-25+dx, 15], [-25+dx, -15], [-35+dx, -40], [-60+dx, -40]])
    jaw_r = jaw_l * np.array([-1, 1])
    
    # Base steel structure
    ax.add_patch(patches.Polygon(jaw_l + [x, y], facecolor=C_TEXT, edgecolor=C_STEEL, lw=2, zorder=8))
    ax.add_patch(patches.Polygon(jaw_r + [x, y], facecolor=C_TEXT, edgecolor=C_STEEL, lw=2, zorder=8))
    
    # Energized glow when carrying a trapped electron
    if glow_ratio > 0:
        ax.add_patch(patches.Polygon(jaw_l + [x, y], facecolor=C_DEFECT, alpha=glow_ratio*0.8, zorder=8.1))
        ax.add_patch(patches.Polygon(jaw_r + [x, y], facecolor=C_DEFECT, alpha=glow_ratio*0.8, zorder=8.1))
        # Containment beam locking the carrier in place
        ax.plot([x - 22 + dx, x + 22 - dx], [y, y], color=C_DEFECT, lw=3, alpha=glow_ratio, zorder=11)

def draw_phonon_spark(ax, x, y, size_ratio, alpha):
    s = 15 * size_ratio
    pts = np.array([[0, s], [s, 0], [0, -s], [-s, 0]])
    ax.add_patch(patches.Polygon(pts + [x, y], facecolor=C_HEAT, alpha=alpha, zorder=12))
    ax.add_patch(patches.Polygon((pts * 0.5) + [x, y], facecolor=C_WHITE, alpha=alpha, zorder=12.1))

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

    # 1. THE THERMODYNAMIC LATTICE
    for gy in range(-900, 1000, 150):
        ax.axhline(gy, color=C_STEEL, lw=1, alpha=0.15, zorder=0)

    # 2. BANDGAP STRUCTURAL SCAFFOLD
    # Conduction Band (E_c)
    ax.add_patch(patches.Rectangle((-540, 400), 1080, 560, facecolor=C_TITANIUM, alpha=0.15, zorder=1))
    ax.axhline(400, color=C_STEEL, lw=2.5, zorder=1.5)
    
    # Valence Band (E_v)
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 760, facecolor=C_DARK, alpha=0.10, zorder=1))
    ax.axhline(-200, color=C_STEEL, lw=2.5, zorder=1.5)
    
    # The Impurity Line (Forbidden Gap Cut)
    ax.axhline(100, color=C_DEFECT, lw=2, linestyle=':', alpha=0.6, zorder=1.2)
    ax.plot([-540, 540], [100, 100], color=C_STEEL, lw=1, zorder=1.1)

    # 3. KINEMATIC SRH TRAPPING EVENTS
    # Three explicit defect states anchored across the X-axis
    TRAP_COORDS = [-320, 0, 320]
    
    for i, trk_x in enumerate(TRAP_COORDS):
        # 33% phase stagger mathematically guarantees constant action looping seamlessly
        t = (phase_ratio + i / 3.0) % 1.0
        
        clamp_val = 0.0
        glow_val = 0.0
        
        # PHASE A: KINEMATIC CARRIER DROP (0.0 to 0.35)
        if 0.0 <= t < 0.35:
            e_phase = t / 0.35
            y_e = 700 - (e_phase * 600)  # Descends from E_c (700) to Trap (100)
            a_e = min(1.0, t / 0.05)     # Fade in absolute seamlessly at Frame 0
            
            # Trap mechanical approach response
            if t >= 0.30:
                clamp_val = (t - 0.30) / 0.05
                glow_val = clamp_val
                
            draw_electron(ax, trk_x, y_e, alpha=a_e)
            
        # PHASE B: TRAPPED CARRIER HOLD ENFORCED (0.35 to 0.50)
        elif 0.35 <= t < 0.50:
            clamp_val = 1.0
            glow_val = 1.0
            draw_electron(ax, trk_x, 100, alpha=1.0)
            
        # PHASE B.2: HOLE ASCENT (0.15 to 0.50)
        if 0.15 <= t < 0.50:
            h_phase = (t - 0.15) / 0.35
            y_h = -500 + (h_phase * 600) # Ascends from E_v (-500) to Trap (100)
            a_h = min(1.0, (t - 0.15) / 0.05)
            draw_hole(ax, trk_x, y_h, alpha=a_h)
            
        # PHASE C: ANNIHILATION & SPALLATION (0.50 to 0.65)
        if 0.50 <= t < 0.65:
            age = (t - 0.50) / 0.15
            clamp_val = 1.0 - (age ** 1.5)
            glow_val = clamp_val
            
            # Mechanical Thermal Shockwave within the trap
            spark_dist = 40 + age * 160
            spark_alpha = max(0.0, 1.0 - (age * 1.5))
            
            if spark_alpha > 0:
                draw_phonon_spark(ax, trk_x + spark_dist, 100 + spark_dist, 1.0, spark_alpha)
                draw_phonon_spark(ax, trk_x - spark_dist, 100 + spark_dist, 1.0, spark_alpha)
                draw_phonon_spark(ax, trk_x + spark_dist, 100 - spark_dist, 1.0, spark_alpha)
                draw_phonon_spark(ax, trk_x - spark_dist, 100 - spark_dist, 1.0, spark_alpha)
                
                # Center blast
                ax.add_patch(patches.Circle((trk_x, 100), radius=50 * (1.0-age), facecolor=C_WHITE, alpha=spark_alpha, zorder=13))

        # Render explicit O(1) trap architecture
        draw_trap(ax, trk_x, 100, clamp_ratio=clamp_val, glow_ratio=glow_val)
        
        # Absolute Reset (0.65 to 1.0): Completely empty, guaranteeing invisible wrap.

    # 4. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    ax.text(-500, 880, "LG-321c :: SRH DEFECT RECOMBINATION TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, 840, "[SFI-1.00] IMPURITY KINEMATICS // CARRIER TRAPPING CAGE", color=C_STEEL, fontsize=12, fontname='monospace', zorder=80)
    
    # Band Callouts (Mathematically aligned)
    ax.add_patch(patches.Rectangle((-540, 400), 280, 28, facecolor=C_TITANIUM, zorder=79))
    ax.text(-520, 408, "CONDUCTION BAND (E_c)", color=C_TEXT, fontsize=12, fontname='monospace', weight='bold', zorder=80)

    ax.add_patch(patches.Rectangle((-540, 72), 340, 28, facecolor=C_DEFECT, zorder=79))
    ax.text(-520, 80, "TRAP STATE (E_t) // IMPURITY", color=C_WHITE, fontsize=12, fontname='monospace', weight='bold', zorder=80)

    ax.add_patch(patches.Rectangle((-540, -228), 260, 28, facecolor=C_DARK, zorder=79))
    ax.text(-520, -220, "VALENCE BAND (E_v)", color=C_WHITE, fontsize=12, fontname='monospace', weight='bold', zorder=80)

    # Loss Telemetry Data Box
    ax.add_patch(patches.Rectangle((-520, -920), 1040, 160, facecolor=C_TITANIUM, alpha=0.9, zorder=79))
    ax.text(-500, -805, "THERMODYNAMIC INTERRUPT: CARRIERS SNARED", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=80)
    
    # Capture Density Pulse 
    pulse = abs(np.sin(phase_ratio * 3 * np.pi))
    ax.text(-500, -840, f"TRAPPED CARRIER DENSITY: {pulse * 100:>05.2f} % Δ [CURRENT LOSS]", color=C_DEFECT if pulse > 0.5 else C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=80)
    
    ax.add_patch(patches.Rectangle((-500, -865), 1000, 4, facecolor=C_STEEL, zorder=80))
    ax.add_patch(patches.Rectangle((-500, -865), 1000 * pulse, 4, facecolor=C_DEFECT, zorder=81))

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0)
    fig.clf(); plt.close(fig); gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-321c: SRH DEFECT KINEMATIC TENSOR [CORES: {cpu_cores}]")
    with mp.Pool(processes=cpu_cores) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
