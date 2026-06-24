"""
SOVEREIGN CODE: logic_garden_337d_stagnation.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Vectorization
SCENE: Logic Garden 337d (Technological Stagnation // Optics vs Radar)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING, MILITARY DOCTRINE
HOTFIX: Linear 20.0s Sequence. Daylight Protocol. Absolute Camera Lock. Tuple Integrity.
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
DURATION = 20.0  # 20.0 Second Execution
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_337d_stagnation"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Oceanic Matrix / Interference Squall
C_STEEL     = '#606065'   # IJN Optical Node / Hardware
C_DARK      = '#202025'   # USN Node Center
C_CYAN      = '#00FFFF'   # Radar Operations / Dielectric Sync
C_MAGENTA   = '#FF0055'   # Error States / Kinematic Spallation
C_GOLD      = '#FFB300'   # Fire-Control / Artillery Transport
C_MANTIS    = '#00FF00'   # Target Sunk Confirm

def draw_industrial_grid(ax):
    """Draw the Baseline Matrix"""
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
    
    # ----------------------------------------------------
    # BARE-METAL CAMERA LOCK: ALL AUTO-SCALING ANNIHILATED
    # ----------------------------------------------------
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)
    ax.autoscale(False)

    draw_industrial_grid(ax)

    # NODES
    POS_IJN = (0, 450)
    POS_USN = (0, -450)

    # ====================================================
    # 1. THE FRICTION VARIABLE (ENVIRONMENTAL OPACITYBOX)
    # ====================================================
    # A massive meteorological or smoke squall sliding across the matrix
    sq_w = 1200
    sq_h = 300
    sq_x = -1500 + t * 180  # Sluggish left-to-right drift
    sq_y = -100

    # True if the Y-axis (LOS) is physically occluded by the box
    is_blocked = (sq_x < 0) and (sq_x + sq_w > 0)
    
    # Draw the Squall (Heavy interference block)
    if sq_x < 600 and sq_x + sq_w > -600:
        c_squall = mcolors.to_rgba(C_TITANIUM, 0.95)
        # Rigid Tuple Box mapping
        ax.add_patch(patches.Rectangle((sq_x, sq_y), sq_w, sq_h, facecolor=c_squall, edgecolor='none', zorder=10))
        # Heavy X-hatching to represent industrial smoke/chaff interference
        ax.add_patch(patches.Rectangle((sq_x, sq_y), sq_w, sq_h, fill=False, hatch='XXXX', edgecolor=C_STEEL, lw=1, alpha=0.4, zorder=10.1))
        # Boundary limits
        ax.plot([sq_x, sq_x+sq_w], [sq_y, sq_y], color=C_STEEL, lw=2, zorder=10.2)
        ax.plot([sq_x, sq_x+sq_w], [sq_y+sq_h, sq_y+sq_h], color=C_STEEL, lw=2, zorder=10.2)

    # ====================================================
    # 2. THE BIOLOGICAL NODE (IJN OPTICAL RANGEFINDER)
    # ====================================================
    # Calculate geometric clipping
    clip_y = sq_y + sq_h if is_blocked else POS_USN[1]
    
    if t < 16.0:
        # Drawing the Optical Cone
        beam_w_origin = 25
        beam_w_target = 80 if is_blocked else 30
        
        cone_pts = [
            [POS_IJN[0] - beam_w_origin, POS_IJN[1]], 
            [POS_IJN[0] + beam_w_origin, POS_IJN[1]], 
            [POS_IJN[0] + beam_w_target, clip_y], 
            [POS_IJN[0] - beam_w_target, clip_y]
        ]
        
        c_opt = mcolors.to_rgba(C_STEEL, 0.6 if is_blocked else 0.8)
        if not is_blocked and t < 10.0:
            c_opt = mcolors.to_rgba(C_GOLD, 0.4) # Target tracked
            
        ax.add_patch(patches.Polygon(cone_pts, facecolor=c_opt, edgecolor='none', zorder=5))
        
        if is_blocked:
            # Shatter graphic where optics hit the fog wall (Kinematic scatter)
            ax.plot([POS_IJN[0]-beam_w_target, POS_IJN[0]+beam_w_target], [clip_y, clip_y], color=C_STEEL, lw=4, zorder=11)
            ax.scatter(np.random.uniform(-beam_w_target, beam_w_target, 8), np.full(8, clip_y), s=20, c=C_MAGENTA, marker='x', zorder=11.1)

    # Draw IJN Node (Monolithic Hexagonal Battleship)
    if t < 16.0:
        ax.add_patch(patches.RegularPolygon(POS_IJN, numVertices=6, radius=55, facecolor=C_STEEL, edgecolor=C_BG, lw=3, zorder=6))
        ax.add_patch(patches.Circle(POS_IJN, 20, facecolor=C_DARK if is_blocked else C_GOLD, zorder=6.1))

    # ====================================================
    # 3. THE ALGORITHMIC NODE (USN RADAR INTEGRATION)
    # ====================================================
    pulse_freq = 1.5
    for p_time in np.arange(0, t, pulse_freq):
        r_pulse = (t - p_time) * 500.0
        if r_pulse < 2000:
            a_pulse = max(0.0, 1.0 - (r_pulse / 1500.0))
            # Radar waves drawn AT Z-ORDER 15: THEY PROJECT *OVER/THROUGH* THE SQUALL (DIELECTRIC PENETRATION)
            ax.add_patch(patches.Circle(POS_USN, r_pulse, fill=False, edgecolor=C_CYAN, lw=2.5, alpha=a_pulse, zorder=15))

    # Target lock is continuous because radar ignores the smoke box
    if t > 2.0 and t < 16.0:
        ax.add_patch(patches.Rectangle((POS_IJN[0]-75, POS_IJN[1]-75), 150, 150, fill=False, edgecolor=C_CYAN, lw=3, zorder=16))
        # Thin predictive laser cutting through the smoke
        ax.plot([POS_USN[0], POS_IJN[0]], [POS_USN[1]+30, POS_IJN[1]-30], color=C_CYAN, lw=1, linestyle=':', zorder=16)

    # USN Node (Agile Rectangular Platform)
    ax.add_patch(patches.Rectangle((-35, -485), 70, 70, facecolor=C_DARK, edgecolor=C_CYAN, lw=3, zorder=6))
    ax.add_patch(patches.Circle(POS_USN, 15, facecolor=C_CYAN, zorder=6.1))

    # ====================================================
    # 4. ASYMMETRIC EXECUTION (RADAR-DIRECTED FIRE)
    # ====================================================
    L_TIME = 12.0
    FLY_T = 3.5
    I_TIME = L_TIME + FLY_T
    
    shells = [L_TIME, L_TIME+0.4, L_TIME+0.8]
    
    for sh in shells:
        if sh <= t <= I_TIME + 1.0:
            fly_prg = (t - sh) / FLY_T
            
            if fly_prg <= 1.0:
                sh_y = POS_USN[1] + (POS_IJN[1] - POS_USN[1]) * fly_prg
                # Shell transits *through* the smoke
                ax.scatter(0, sh_y, s=70, c=C_BG, edgecolors=C_GOLD, lw=3, zorder=17)
                
                # VT-Fuze detection rings
                vt_r = (t * 250) % 50
                ax.add_patch(patches.Circle((0, sh_y), vt_r, fill=False, edgecolor=C_CYAN, lw=1.5, alpha=1.0-(vt_r/50.0), zorder=16.9))

            else:
                # Terminal Spallation
                exp_t = t - I_TIME
                if exp_t < 1.0:
                    r_blast = 300 * exp_t
                    a_blast = 1.0 - exp_t
                    ax.scatter(0, POS_IJN[1], s=r_blast*20, c=C_BG, edgecolors=C_MAGENTA, lw=10*a_blast, alpha=a_blast, zorder=20)
                    ax.scatter(0, POS_IJN[1], s=r_blast*5, c=C_GOLD, alpha=a_blast, zorder=21)

    # Architecture Collapse
    if t >= I_TIME + 0.2:
        drift = (t - I_TIME) * 10
        # Wreckage breaking apart structurally
        ax.scatter(0, POS_IJN[1], s=800, c=C_BG, edgecolors=C_STEEL, lw=4, marker='x', alpha=max(0, 1.0-(t-I_TIME)/4.0), zorder=4)

    # ====================================================
    # 5. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    # Top Header [Strict Tuples]
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-337d :: TECHNOLOGICAL STAGNATION TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] BIOLOGICAL OPTICS VS CENTIMETRIC RADAR", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    # Bottom Telemetry HUD
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    # IJN Logic State
    opt_state = "BLOCKED [BIOLOGICAL BLINDNESS / LAG]" if is_blocked else "CLEAR [OPTICAL LOCK ACTIVE]"
    opt_col = C_MAGENTA if is_blocked else C_GOLD
    if t > I_TIME: opt_state = "NODE DESTROYED"; opt_col = C_MAGENTA

    # USN Logic State
    rad_state = "DIELECTRIC PENETRATION // O(1) LOCK MAINTAINED" if is_blocked else "O(1) SPATIAL LOCK ACQUIRED"
    rad_col = C_CYAN
    if t > I_TIME: rad_state = "TARGET NEUTRALIZED // AIRSPACE SECURED"; rad_col = C_MANTIS

    # Fire-Control Output
    if t > I_TIME:
        fc_state = "18.1-INCH VAPORIZED | CIC KINEMATIC CONFIRM"
        fc_col = C_MANTIS
    elif t > L_TIME:
        fc_state = "18.1-INCH OFFLINE | 5-INCH RADAR DIRECTED EN ROUTE"
        fc_col = C_GOLD
    else:
        fc_state = "18.1-INCH OFFLINE | 5-INCH SPOOLING FIRING SOLUTION" if is_blocked else "18.1-INCH STANDBY | 5-INCH RADAR TRACKING"
        fc_col = C_MAGENTA if is_blocked else C_STEEL

    ax.text(-500, -760, "SYS_01 [IJN 15m RANGEFINDER] :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(60, -760, opt_state, color=opt_col, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [USN SG CENTIMETRIC]  :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(60, -800, rad_state, color=rad_col, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "BATTLESPACE FIRE-CONTROL     :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(60, -840, fc_state, color=fc_col, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider [Strict Tuples]
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=rad_col, zorder=83))

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
    print(f"LG-337d: TECH STAGNATION TENSOR [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE] [Tuples Sealed]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
