"""
SOVEREIGN CODE: logic_garden_333_fobs_tensor.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Vectorization
SCENE: Logic Garden 333 (Fractional Orbital Bombardment System)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING
HOTFIX: Linear 15.0s Strike Sequence. Absolute Camera Lock. Tuple Integrity Confirmed.
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
DURATION = 15.0  # 15.0 Second Strike Timeline
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_333_fobs_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Earth Grid Matrix
C_STEEL     = '#606065'   # Earth Crust Bounding
C_DARK      = '#202025'   # Baseline ICBM Arc
C_CYAN      = '#00FFFF'   # Northern Radar Matrix (BMEWS)
C_MAGENTA   = '#FF0055'   # The FOBS Warhead / Kinetic Trajectory
C_GOLD      = '#FFB300'   # Retro-Burn / Impact Spallation
C_WHITE     = '#FFFFFF'

# -------- KINEMATIC CONSTANTS --------
EARTH_CX = 0
EARTH_CY = -50
R_EARTH = 280
R_LEO = 350
R_APOGEE = 550

ANGLE_LAUNCH = 60   # Launch trajectory (Northern Hemisphere Right)
ANGLE_TARGET = 120  # Target coordinates (Northern Hemisphere Left)
# FOBS orbital path traverses backwards: 60 -> 0 -> -90 -> -180 -> -240 (which is 120)

# Precompute deterministic O(1) Kinematic Flight Arrays
F_BOOST = 120   # 0 to 2.0s
F_RETRO = 660   # 11.0s
F_DIVE  = 750   # 12.5s
F_IMPACT = 840  # 14.0s

fobs_r = np.zeros(TOTAL_FRAMES)
fobs_t = np.zeros(TOTAL_FRAMES)

for f in range(TOTAL_FRAMES):
    if f < F_BOOST:
        ratio = f / F_BOOST
        ratio_sq = 1 - (1 - ratio)**2 # Ease out
        fobs_r[f] = R_EARTH + (R_LEO - R_EARTH) * ratio_sq
        fobs_t[f] = ANGLE_LAUNCH - ratio_sq * 20 # Arcing backward 60 -> 40
        
    elif f < F_RETRO:
        ratio = (f - F_BOOST) / (F_RETRO - F_BOOST)
        fobs_r[f] = R_LEO
        # Travel through the entire Southern Hemisphere (-220 is delta of 260 deg)
        fobs_t[f] = 40 - ratio * 260 
        
    elif f < F_DIVE:
        ratio = (f - F_RETRO) / (F_DIVE - F_RETRO)
        fobs_r[f] = R_LEO - (R_LEO - (R_EARTH + 20)) * ratio
        fobs_t[f] = -220 - ratio * 10
        
    elif f < F_IMPACT:
        ratio = (f - F_DIVE) / (F_IMPACT - F_DIVE)
        ratio_accel = ratio**2 # Ease in (gravitational pull)
        fobs_r[f] = (R_EARTH + 20) - 20 * ratio_accel
        fobs_t[f] = -230 - ratio * 10
        
    else:
        fobs_r[f] = R_EARTH
        fobs_t[f] = -240

def draw_industrial_earth(ax):
    """Draw the Baryonic Core mapped with rigid O(1) architectural symmetry"""
    ax.add_patch(patches.Circle((EARTH_CX, EARTH_CY), R_EARTH, facecolor=C_BG, edgecolor=C_STEEL, lw=4, zorder=2))
    ax.add_patch(patches.Circle((EARTH_CX, EARTH_CY), R_EARTH-10, facecolor='none', edgecolor=C_TITANIUM, lw=1.5, zorder=2.1))
    ax.add_patch(patches.Circle((EARTH_CX, EARTH_CY), R_EARTH-40, facecolor='none', edgecolor=C_TITANIUM, lw=1, linestyle='--', zorder=2.1))
    
    # Lat/Long Spokes
    for angle in range(0, 360, 30):
        rad = np.radians(angle)
        ex = EARTH_CX + R_EARTH * np.cos(rad)
        ey = EARTH_CY + R_EARTH * np.sin(rad)
        ax.plot([EARTH_CX, ex], [EARTH_CY, ey], color=C_TITANIUM, lw=1, alpha=0.6, zorder=2.2)

def draw_early_warning_matrix(ax):
    """BMEWS Radar Coverage projection (Detects attacks over the North Pole)"""
    # Create the sweeping radar wedge looking UP and slightly left/right
    angles = np.linspace(40, 140, 100)
    rx = [EARTH_CX] + [EARTH_CX + 1000 * np.cos(np.radians(a)) for a in angles] + [EARTH_CX]
    ry = [EARTH_CY] + [EARTH_CY + 1000 * np.sin(np.radians(a)) for a in angles] + [EARTH_CY]
    
    ax.add_patch(patches.Polygon(np.column_stack((rx, ry)), facecolor=C_CYAN, alpha=0.08, zorder=1))
    ax.plot(rx[1:-1], ry[1:-1], color=C_CYAN, lw=2, linestyle='--', alpha=0.4, zorder=1.1)
    
    # Target Site
    tx = EARTH_CX + R_EARTH * np.cos(np.radians(ANGLE_TARGET))
    ty = EARTH_CY + R_EARTH * np.sin(np.radians(ANGLE_TARGET))
    ax.add_patch(patches.Rectangle((tx-15, ty), 30, 10, facecolor=C_TEXT, angle=ANGLE_TARGET-90, zorder=3))

    # Launch Site
    lx = EARTH_CX + R_EARTH * np.cos(np.radians(ANGLE_LAUNCH))
    ly = EARTH_CY + R_EARTH * np.sin(np.radians(ANGLE_LAUNCH))
    ax.add_patch(patches.Rectangle((lx-15, ly), 30, 20, facecolor=C_DARK, angle=ANGLE_LAUNCH-90, zorder=3))

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

    # 1. GENERATE STATIC GEOMETRY
    draw_industrial_earth(ax)
    draw_early_warning_matrix(ax)

    # 2. DRAW TRADITIONAL ICBM PARABOLA (BASELINE COMPARISON)
    icbm_angles = np.linspace(ANGLE_LAUNCH, ANGLE_TARGET, 150)
    icbm_r = R_EARTH + (R_APOGEE - R_EARTH) * np.sin(np.radians((icbm_angles - ANGLE_LAUNCH) / (ANGLE_TARGET - ANGLE_LAUNCH) * 180))
    icbm_x = EARTH_CX + icbm_r * np.cos(np.radians(icbm_angles))
    icbm_y = EARTH_CY + icbm_r * np.sin(np.radians(icbm_angles))
    ax.plot(icbm_x, icbm_y, color=C_DARK, lw=3, linestyle=':', alpha=0.6, zorder=2.5)

    # Intersection Marker (Detection point)
    ax.scatter(icbm_x[30], icbm_y[30], color=C_DARK, s=80, marker='X', zorder=2.6)
    ax.text(icbm_x[30]+20, icbm_y[30]+20, "INTERCEPTED", color=C_STEEL, fontsize=10, weight='bold', zorder=2.6)

    # 3. KINEMATIC FOBS EXECUTION
    # Draw trailing path up to current frame
    traj_x = EARTH_CX + fobs_r[:f+1] * np.cos(np.radians(fobs_t[:f+1]))
    traj_y = EARTH_CY + fobs_r[:f+1] * np.sin(np.radians(fobs_t[:f+1]))
    if len(traj_x) > 1:
        ax.plot(traj_x, traj_y, color=C_MAGENTA, lw=4, zorder=4)
        
    # Current Position
    cx = traj_x[-1]
    cy = traj_y[-1]
    
    # The Payload Vector Wedge
    flight_angle = 0
    if f > 0:
        flight_angle = np.degrees(np.arctan2(cy - traj_y[-2], cx - traj_x[-2]))
    
    trans = transforms.Affine2D().rotate_deg_around(cx, cy, flight_angle) + ax.transData
    wedge = np.array([[-15, -10], [15, 0], [-15, 10]])
    
    if f < F_IMPACT:
        ax.add_patch(patches.Polygon(wedge + [cx, cy], facecolor=C_MAGENTA, edgecolor='none', transform=trans, zorder=5))
    
    # 4. EVENT TRIGGERS (RETRO BURN & IMPACT)
    if F_RETRO <= f < F_DIVE:
        # Retro-burn thrust vector
        burst = (f - F_RETRO) % 3
        burst_scale = 10 + burst * 15
        burst_trans = transforms.Affine2D().rotate_deg_around(cx, cy, flight_angle + 180) + ax.transData
        burst_wedge = np.array([[-5, -10], [burst_scale, 0], [-5, 10]])
        ax.add_patch(patches.Polygon(burst_wedge + [cx, cy], facecolor=C_GOLD, edgecolor='none', transform=burst_trans, alpha=0.9, zorder=4.5))

    if f >= F_IMPACT:
        # Kinematic Destabilization
        expansion = min(1.0, (f - F_IMPACT) / 30.0)
        ax.scatter(cx, cy, c=C_MAGENTA, s=400 * expansion, edgecolors=C_BG, lw=2, zorder=6)
        ax.add_patch(patches.Circle((cx, cy), 80 * expansion, fill=False, edgecolor=C_GOLD, lw=5, alpha=1.0-expansion, zorder=6))
        ax.plot([cx-150*expansion, cx+150*expansion], [cy, cy], color=C_GOLD, lw=3, alpha=1.0-expansion, zorder=6)

    # 5. STATIC WIDGETS
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-333 :: FRACTIONAL ORBITAL BOMBARDMENT", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] SOUTHERN STRATOSPHERIC INJECTION", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    # 6. KINEMATIC TARGETING HUD [Strict Tuple Fix active]
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 260, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-700, -700], color=C_TEXT, lw=4, zorder=81)
    
    # State Engine Calculation
    if f < F_BOOST:
        state = "ASCENT & ORBITAL INJECTION"
        s_col = C_DARK
    elif f < F_RETRO:
        state = "FRACTIONAL ORBIT COAST (RADAR EVASION)"
        s_col = C_MAGENTA
    elif f < F_DIVE:
        state = "RETRO-BURN KINEMATIC DECELERATION"
        s_col = C_GOLD
    elif f < F_IMPACT:
        state = "TERMINAL RE-ENTRY DIVE"
        s_col = C_MAGENTA
    else:
        state = "KINETIC ENERGY TRANSFER / IMPACT"
        s_col = C_TEXT

    ax.text(-500, -740, "FLIGHT STAGE IDENTIFIER:", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(-180, -740, state, color=s_col, fontsize=16, fontname='monospace', weight='bold', zorder=82)

    alt = int(fobs_r[f] - R_EARTH)
    vel = 28000 if f < F_RETRO else max(0, 28000 - ((f-F_RETRO)*400))
    if f >= F_IMPACT: vel = 0

    ax.text(-500, -790, f"ALTITUDE (R-DELTA): {alt:>04d} KM", color=C_TEXT, fontsize=15, fontname='monospace', zorder=82)
    ax.text(-500, -825, f"VELOCITY VEXTOR : {vel:>05d} KM/H", color=C_TEXT, fontsize=15, fontname='monospace', zorder=82)
    
    # Radar Cross-section logic
    rcs_col = C_STEEL if f < F_IMPACT else C_TEXT
    rcs_text = "UNDETECTED (EVASION VECTOR)"
    # A true FOBS is detected only in the terminal dive (After F_RETRO but close to target)
    if F_DIVE < f < F_IMPACT:
        rcs_text = "DETECTED (WARNING: < 3 MINS)"
        rcs_col = C_CYAN

    ax.text(-500, -860, f"BMEWS RADAR INTERCEPT : {rcs_text}", color=rcs_col, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    # Progress Tracking Bar
    ax.add_patch(patches.Rectangle((-500, -900), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -900), 1000 * phase_ratio, 6, facecolor=C_MAGENTA, zorder=83))

    # Sovereign Execution Output: Auto-Scale mathematically locked
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
    print(f"LG-333: FOBS TENSOR [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE] [Tuples Sealed]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
