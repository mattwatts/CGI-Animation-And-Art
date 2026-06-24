"""
SOVEREIGN CODE: logic_garden_341c_geometry_rupture.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Vectorization
SCENE: Logic Garden 341c (Geometry Rupture // M2-F2 Lateral Failure)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING, AERODYNAMICS
HOTFIX: Linear 26.0s Sequence. Daylight Protocol. Absolute Camera Lock. Tuples Sealed.
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
DURATION = 26.0  
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_341c_rupture"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Airspace Grid Matrix
C_STEEL     = '#606065'   # Fuselage / Baseline Geometry
C_DARK      = '#202025'   # Shadow / Depth
C_GOLD      = '#FFB300'   # O(1) Target Vectors
C_CYAN      = '#00FFFF'   # Z-Axis Stabilizer (Center Fin) / Fix
C_MAGENTA   = '#FF0055'   # PIO Sine Wave / Tumbling Chaos
C_MANTIS    = '#00FF00'   # Frequency Damned / Terminal Green

# ------------------------------------------------------------------
# O(1) KINEMATIC ARRAY PRE-COMPUTATION (DETERMINISTIC TIMELINE)
# ------------------------------------------------------------------
time_arr = np.linspace(0, DURATION, TOTAL_FRAMES)

roll_arr = np.zeros(TOTAL_FRAMES)
slip_arr = np.zeros(TOTAL_FRAMES)
state_arr = np.zeros(TOTAL_FRAMES, dtype=int)

T_PIO_START = 4.0
T_CRASH = 14.5
T_RESET = 15.0
T_RELAUNCH = 16.0

for i, t in enumerate(time_arr):
    if t < T_PIO_START:
        # Stable descent
        roll_arr[i] = 0.0
        state_arr[i] = 0
    elif t < T_RESET:
        # Phase 1: M2-F2 PIO Exponential Failure
        dt = t - T_PIO_START
        # Amplitude aggressively expands exponentially
        amp = min(180.0, (dt ** 1.8) * 1.5) 
        # Frequency increases as control is lost
        freq = 3.0 + (dt * 0.2)
        r_val = amp * np.sin(dt * freq)
        
        roll_arr[i] = r_val
        if t < T_CRASH:
            state_arr[i] = 1 # PIO Warning
        else:
            state_arr[i] = 2 # Catastrophic Rupture
            
    elif t < T_RELAUNCH:
        # Serialize Razor Wipe
        roll_arr[i] = 0.0
        state_arr[i] = 3
    else:
        # Phase 2: M2-F3 Sovereign Fix (Center Fin stops wave)
        dt = t - T_RELAUNCH
        # Same triggering force as T_PIO_START, but violently damped by fin
        amp = 30.0 * np.exp(-dt * 0.8) # Exponential decay friction
        r_val = amp * np.sin(dt * 3.0)
        
        roll_arr[i] = r_val
        state_arr[i] = 4

# Slip is a mathematical function of roll in a Dutch roll
slip_arr = -roll_arr * 1.5 

def draw_perspective_corridor(ax, t):
    """Draws a deep z-axis tracking tunnel simulating forward flight."""
    horizon_x, horizon_y = 0, 100
    
    # Radiating lines mapped from 3D space to 2D
    for angle in np.linspace(180, 360, 15):
        rad = np.radians(angle)
        ex = horizon_x + 800 * np.cos(rad)
        ey = horizon_y + 800 * np.sin(rad)
        ax.plot([horizon_x, ex], [horizon_y, ey], color=C_TITANIUM, lw=2, alpha=0.3, zorder=0)

    # Approaching grid rings mapped with modulus
    speed = t * 10
    for z in range(1, 10):
        scale = ((z + speed) % 10) / 10.0
        width = 800 * scale
        height = 400 * scale
        if scale > 0.05:
            ax.add_patch(patches.Ellipse((horizon_x, horizon_y), width*2, height*2, fill=False, edgecolor=C_TITANIUM, lw=2, alpha=scale*0.5, zorder=0))

def render_frame(packet):
    f, phase_ratio = packet
    t = phase_ratio * DURATION 
    
    roll = roll_arr[f]
    slip = slip_arr[f]
    state = state_arr[f]
    
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
    
    # The Matrix Corridor
    draw_perspective_corridor(ax, t)
    
    AIRCRAFT_Y = -150

    # ====================================================
    # 1. THE DUTCH ROLL WAKE (PHANTOM SPECIES HISTORY)
    # ====================================================
    # We plot the last 90 frames of trajectory converging to the horizon
    history_len = 90
    if f > 0 and state != 3:
        hist_start = max(0, f - history_len)
        # Verify we don't draw across the boundary reset
        if state == 4:
            boundary_f = int(T_RELAUNCH * FPS)
            hist_start = max(boundary_f, hist_start)
            
        h_slip = slip_arr[hist_start:f]
        h_roll = roll_arr[hist_start:f]
        
        # 3D to 2D perspective mapping
        h_len = len(h_slip)
        z_factors = np.linspace(0.0, 1.0, h_len) # 1.0 is far away (Horizon)
        
        hx_plot = h_slip * (1.0 - z_factors)
        hy_plot = AIRCRAFT_Y + (100 - AIRCRAFT_Y) * z_factors
        
        w_color = C_MAGENTA if state in [1, 2] else C_MANTIS
        ax.plot(hx_plot, hy_plot, color=w_color, lw=4, alpha=0.6, zorder=5)

    # ====================================================
    # 2. THE LIFTING BODY NODE [REAR VIEW GEOMETRY]
    # ====================================================
    if state != 3: # Not in wipe phase
        # Camera shake if catastrophic
        cx, cy = slip, AIRCRAFT_Y
        if state == 2:
            np.random.seed(int(t*100))
            cx += np.random.uniform(-15, 15)
            cy += np.random.uniform(-15, 15)
            
        trans = matplotlib.transforms.Affine2D().rotate_deg_around(cx, cy, roll) + ax.transData
        
        # Color state logic
        body_col = C_STEEL if state in [0, 4] else C_MAGENTA
        hud_warn_alpha = 0.7 if state in [1,2] else 0.0

        # Blunt fuselage (Flat top, rounded bottom in rear profile)
        fuse_pts = [[-120, 20], [120, 20], [80, -60], [-80, -60]]
        ax.add_patch(patches.Polygon(fuse_pts, facecolor=C_BG, edgecolor=body_col, lw=6, transform=trans, zorder=20))
        
        # Mock Engine/Exhaust ports (Closed/Unpowered)
        ax.add_patch(patches.Circle((-50, -20), 15, facecolor=C_DARK, transform=trans, zorder=21))
        ax.add_patch(patches.Circle((50, -20), 15, facecolor=C_DARK, transform=trans, zorder=21))
        
        # Outer Vertical Stabilizers
        fin_l = [[-120, 20], [-150, 100], [-100, 100], [-100, 20]]
        fin_r = [[120, 20], [150, 100], [100, 100], [100, 20]]
        ax.add_patch(patches.Polygon(fin_l, facecolor=C_BG, edgecolor=body_col, lw=5, transform=trans, zorder=19))
        ax.add_patch(patches.Polygon(fin_r, facecolor=C_BG, edgecolor=body_col, lw=5, transform=trans, zorder=19))
        
        # PHASE 2: THE SOVEREIGN FIX (M2-F3 CENTER FIN)
        if state == 4:
            # Welded Z-Axis Fin directly on centerline
            fin_c = [[-15, 20], [0, 140], [15, 20]]
            ax.add_patch(patches.Polygon(fin_c, facecolor=C_CYAN, edgecolor=C_CYAN, alpha=0.9, lw=2, transform=trans, zorder=22))
            
            # Radiating structural enforcement lines proving it kills the PIO
            ax.plot([0, 0], [140, 200], color=C_CYAN, lw=4, linestyle='dashed', transform=trans, zorder=23)

        # CATASTROPHIC SPALLATION
        if state == 2:
            # Heavy friction sparks tearing off the edges
            n_sparks = 40
            for sp in range(n_sparks):
                s_px = cx + np.random.uniform(-150, 150)
                s_py = cy + np.random.uniform(-100, 100)
                ax.scatter(s_px, s_py, s=np.random.uniform(10, 60), c=C_MAGENTA, edgecolors='none', alpha=0.8, zorder=25)
                
            # Giant Lethal Vectors overlay
            ax.add_patch(patches.Circle((cx, cy), 180, fill=False, edgecolor=C_MAGENTA, lw=10, alpha=hud_warn_alpha, zorder=26))
            ax.plot([cx-200, cx+200], [cy-200, cy+200], color=C_MAGENTA, lw=8, zorder=26)
            ax.plot([cx-200, cx+200], [cy+200, cy-200], color=C_MAGENTA, lw=8, zorder=26)

    # ====================================================
    # 3. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-341c :: GEOMETRY RUPTURE [M2-F2 LATERAL FAILURE]", color=C_TEXT, fontsize=20, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] PHANTOM SPECIES YAW-ROLL // Z-AXIS REVISION", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    if state == 0:
        c1, s1 = C_STEEL, "LAMINAR FLOW // NO PERTURBATION"
        c2, s2 = C_STEEL, "O(1) PILOT TRACKING"
        ca, sa = C_STEEL, "MONITORING TOPOLOGY"
    elif state == 1:
        c1, s1 = C_MAGENTA, f"EXPONENTIAL YAW-ROLL: {abs(roll):>05.1f} DEG"
        c2, s2 = C_GOLD, "LATENCY DETECTED // PIO AMPLIFICATION"
        ca, sa = C_MAGENTA, "FATAL Z-AXIS MAPPING ERROR DETECTED"
    elif state == 2:
        c1, s1 = C_MAGENTA, "CATASTROPHIC RUPTURE"
        c2, s2 = C_MAGENTA, "HARDWARE LIMITS EXCEEDED"
        ca, sa = C_MAGENTA, "STRUCTURAL SPALLATION IMMINENT"
    elif state == 3:
        c1, s1 = C_CYAN, "SYSTEM OVERRIDE"
        c2, s2 = C_CYAN, "SERIALIZE RAZOR PURGING CAUSAL CHAIN"
        ca, sa = C_CYAN, "APPLYING HARD GEOMETRIC REVISION"
    elif state == 4:
        c1, s1 = C_MANTIS, f"DAMPED OSCILLATION: {abs(roll):>05.1f} DEG"
        c2, s2 = C_MANTIS, "PILOT LATENCY NULLIFIED BY BAFFLE"
        ca, sa = C_CYAN, "TATH\u0100T\u0100 // C_CYAN CENTER FIN SECURED"

    if state == 3:
        # Full screen wipe effect
        ax.add_patch(patches.Rectangle((-540, -960), 1080, 1920, facecolor=C_CYAN, alpha=0.5, zorder=79))
        ax.text(0, 0, "SERIALIZE RAZOR\nTIMELINE RESET", color=C_TEXT, fontsize=40, fontname='monospace', weight='bold', ha='center', va='center', zorder=80)

    ax.text(-500, -760, "SYS_01 [LATERAL STABILITY]   :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(30, -760, s1, color=c1, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [PIO LATENCY]         :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(30, -800, s2, color=c2, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "STRUCTURAL AUDIT [Z-AXIS]    :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(30, -840, sa, color=ca, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=ca, zorder=83))

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
    print(f"LG-341c: GEOMETRY RUPTURE [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
