"""
SOVEREIGN CODE: logic_garden_341b_energy_decay.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Vectorization
SCENE: Logic Garden 341b (The Energy Decay Curve // HL-10 Descent)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING, AERODYNAMICS
HOTFIX: Linear 24.0s Sequence. Daylight Protocol. Absolute Camera Lock. Tuples Sealed.
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
DURATION = 24.0  
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_341b_decay"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Graph Matrix
C_STEEL     = '#606065'   # HL-10 Node
C_DARK      = '#202025'   # B-52 Carrier
C_GOLD      = '#FFB300'   # Flare Lift Vector
C_CYAN      = '#00FFFF'   # Commercial Glide Baseline (15:1)
C_MAGENTA   = '#FF0055'   # 3:1 Plummet Vector / Kinetic Bleed
C_MANTIS    = '#00FF00'   # Terminal Green Touchdown

# ------------------------------------------------------------------
# O(1) KINEMATIC ARRAY PRE-COMPUTATION (DETERMINISTIC TIMELINE)
# ------------------------------------------------------------------
time_arr = np.linspace(0, DURATION, TOTAL_FRAMES)

# Physics limits
FT_Y_MAX = 45000.0
FT_X_MAX = 150000.0 # 150k ft horizontal

HL_x = np.zeros(TOTAL_FRAMES)
HL_y = np.zeros(TOTAL_FRAMES)
HL_pitch = np.zeros(TOTAL_FRAMES)
HL_vy = np.zeros(TOTAL_FRAMES)

AIR_x = np.zeros(TOTAL_FRAMES)
AIR_y = np.zeros(TOTAL_FRAMES)

T_DROP = 2.0
T_FLARE = 18.0
T_LAND = 20.0

V_X_B52 = 660.0 # ft/sec (Approx 450 mph)

for i, t in enumerate(time_arr):
    # COMMERCIAL AIRLINER (15:1 Ratio, drops 1 unit for every 15 horizontal)
    # V_x approx 400 fps. V_y approx -26 fps.
    if t < T_DROP:
        AIR_x[i] = t * V_X_B52
        AIR_y[i] = 45000.0
    else:
        dt = t - T_DROP
        AIR_x[i] = (T_DROP * V_X_B52) + (400.0 * dt)
        AIR_y[i] = max(0.0, 45000.0 - (26.6 * dt))

    # HL-10 LIFTING BODY (3:1 Ratio, drops 1 unit for every 3 horizontal)
    if t < T_DROP:
        HL_x[i] = t * V_X_B52
        HL_y[i] = 45000.0
        HL_pitch[i] = 0.0
        HL_vy[i] = 0.0
    elif t < T_FLARE:
        dt = t - T_DROP
        total_plummet_time = T_FLARE - T_DROP # 16 seconds
        y_drop = 45000.0 - 200.0 # Target 200ft for flare
        
        v_y = -(y_drop / total_plummet_time) # approx -2800 fps in sim scale
        v_x = abs(v_y) * 3.0 # 3:1 ratio
        
        HL_x[i] = (T_DROP * V_X_B52) + (v_x * dt)
        HL_y[i] = 45000.0 + (v_y * dt)
        HL_pitch[i] = -18.0 # Nose down descent
        HL_vy[i] = v_y
    elif t < T_LAND:
        # THE KINEMATIC FLARE
        dt = t - T_FLARE
        flare_dur = T_LAND - T_FLARE # 2 seconds
        prg = dt / flare_dur
        
        # Y goes from 200 to 0 exponentially decaying
        HL_y[i] = 200.0 * (1.0 - prg)**2
        # Velocity rapidly bleeds
        HL_x[i] = HL_x[i-1] + (200.0 * (1.0 - prg)) # Arbitrary forward bleed
        # Pitch snaps violently back to bleed energy
        HL_pitch[i] = -18.0 + (35.0 * np.sin(prg * np.pi/2)) 
        HL_vy[i] = -100 * (1.0 - prg)
    else:
        # ROLLOUT
        HL_y[i] = 0.0
        HL_x[i] = HL_x[i-1] + (50.0 * np.exp(-(t-T_LAND)))
        HL_pitch[i] = 0.0
        HL_vy[i] = 0.0

# Graphing Transformation Functions
def map_x(ft_x): return -400 + (ft_x / FT_X_MAX) * 800
def map_y(ft_y): return -400 + (ft_y / FT_Y_MAX) * 800

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

    # 1. DRAW KINEMATIC GRID BOUNDARY
    ax.add_patch(patches.Rectangle((-400, -400), 800, 800, facecolor='none', edgecolor=C_TITANIUM, lw=4, zorder=1))
    # Grid lines
    for px in np.linspace(-400, 400, 11): ax.plot([px, px], [-400, 400], color=C_TITANIUM, lw=1, alpha=0.5, zorder=0)
    for py in np.linspace(-400, 400, 11): ax.plot([-400, 400], [py, py], color=C_TITANIUM, lw=1, alpha=0.5, zorder=0)

    # Y-Axis Labels (Altitude)
    for alt in [0, 15000, 30000, 45000]:
        ax.text(-420, map_y(alt), f"{alt} FT", color=C_STEEL, fontsize=10, fontname='monospace', ha='right', va='center', zorder=2)
    # X-Axis Labels (Distance)
    for dist in [0, 50000, 100000, 150000]:
        ax.text(map_x(dist), -420, f"{dist//1000}k", color=C_STEEL, fontsize=10, fontname='monospace', ha='center', va='top', zorder=2)
        
    ax.plot([-400, 400], [-400, -400], color=C_TEXT, lw=6, zorder=5) # HARD BASEPLATE Y=0

    # ====================================================
    # 2. COMMERCIAL AIRLINER TRAJECTORY (15:1 Baseline)
    # ====================================================
    if t > T_DROP:
        air_mx = map_x(AIR_x[f])
        air_my = map_y(AIR_y[f])
        
        # Trajectory trail
        past_f = max(0, f-300)
        ax.plot(np.vectorize(map_x)(AIR_x[past_f:f]), np.vectorize(map_y)(AIR_y[past_f:f]), color=C_CYAN, lw=3, linestyle='--', zorder=10)
        
        # Ghost Node
        if air_mx <= 400:
            ax.add_patch(patches.RegularPolygon((air_mx, air_my), numVertices=3, radius=10, facecolor=C_CYAN, edgecolor='none', transform=matplotlib.transforms.Affine2D().rotate_deg_around(air_mx, air_my, -90).translate(0,0) + ax.transData, zorder=11))
            ax.text(air_mx, air_my+20, "15:1 AERO BASELINE", color=C_CYAN, fontsize=9, fontname='monospace', ha='center', zorder=12)

    # ====================================================
    # 3. HL-10 LIFTING BODY (The Plummet & Flare)
    # ====================================================
    hl_mx = map_x(HL_x[f])
    hl_my = map_y(HL_y[f])
    hl_p = HL_pitch[f]
    
    # 3A. B-52 Carrier
    if t <= T_DROP + 1.0:
        b52_x = map_x(HL_x[f] if t <= T_DROP else HL_x[int(T_DROP*FPS)] + V_X_B52*(t-T_DROP))
        b52_y = map_y(45200)
        ax.add_patch(patches.Rectangle((b52_x-40, b52_y-10), 80, 20, facecolor=C_DARK, zorder=15))
        ax.text(b52_x, b52_y+20, "B-52 MOTHERSHIP", color=C_DARK, fontsize=10, fontname='monospace', weight='bold', ha='center', zorder=16)

    # 3B. HL-10 Kinetic Trail
    if t > T_DROP:
        trail_start = int(T_DROP*FPS)
        ax.plot(np.vectorize(map_x)(HL_x[trail_start:f]), np.vectorize(map_y)(HL_y[trail_start:f]), color=C_MAGENTA if t < T_FLARE else C_GOLD, lw=5, zorder=18)

    # 3C. HL-10 Node
    node_c = C_STEEL if t < T_DROP else (C_MAGENTA if t < T_FLARE else (C_GOLD if t < T_LAND else C_MANTIS))
    trans_hl = matplotlib.transforms.Affine2D().rotate_deg_around(hl_mx, hl_my, hl_p) + ax.transData
    
    # Bullet/Brick shape
    ax.add_patch(patches.Rectangle((hl_mx-20, hl_my-10), 40, 20, facecolor=C_BG, edgecolor=node_c, lw=4, transform=trans_hl, zorder=20))
    ax.plot([hl_mx+20, hl_mx+35], [hl_my, hl_my], color=node_c, lw=4, transform=trans_hl, zorder=20) # Nose
    
    # 3D. The Flare Vector (Kinetic -> Lift Conversion)
    if T_FLARE <= t < T_LAND:
        prg = (t - T_FLARE) / (T_LAND - T_FLARE)
        vec_max = 100 * np.sin(prg * np.pi) # Swells and fades
        # Draw massive vertical vector counteracting gravity
        ax.add_patch(patches.Arrow(hl_mx, hl_my, 0, vec_max, width=20, color=C_GOLD, zorder=25))
        
        # Kinetic Spallation off the bottom due to pure aerodynamic braking
        np.random.seed(int(t*100))
        for _ in range(10):
            ax.scatter(hl_mx + np.random.uniform(-30, 0), hl_my - 15 + np.random.uniform(-10, 10), c=C_GOLD, s=np.random.uniform(10, 40), alpha=0.8, edgecolor='none', zorder=19)

    # ====================================================
    # 4. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    # Top Header
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-341b :: THE ENERGY DECAY CURVE [HL-10]", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] O(1) KINEMATIC BLEED // Ep TO Ek CONVERSION", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    # Bottom Telemetry HUD
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    # Metrics
    alt_metric = f"ALTITUDE  : {int(HL_y[f]):>5d} FT"
    v_metric = f"V-VELOCITY: {int(HL_vy[f]):>5d} FPS"
    
    ax.text(-500, -760, "SYS_01 [ALTIMETER]           :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, alt_metric, color=C_CYAN if t < T_DROP else (C_MAGENTA if t < T_LAND else C_MANTIS), fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [THERMAL DESCENT]     :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, v_metric, color=C_TEXT if t < T_DROP else C_MAGENTA, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    # Engine States
    if t < T_DROP:
        state_str = "TETHERED // POTENTIAL ENERGY (Ep) MAXIMIZED"
        state_col = C_STEEL
    elif t < T_FLARE:
        state_str = "THRUST VARIABLES DELETED // 3:1 GLIDE ACTIVE"
        state_col = C_MAGENTA
    elif t < T_LAND:
        state_str = "O(1) FLARE EXECUTED // KINETIC BINDING"
        state_col = C_GOLD
    else:
        state_str = "TATH\u0100T\u0100 // GRAVITY CAPTURE SECURED"
        state_col = C_MANTIS

    ax.text(-500, -840, "STRUCTURAL LOAD MATRIX       :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, state_str, color=state_col, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=state_col, zorder=83))

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
    print(f"LG-341b: ENERGY DECAY CURVE [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
