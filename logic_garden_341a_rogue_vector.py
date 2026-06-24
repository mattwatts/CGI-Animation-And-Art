"""
SOVEREIGN CODE: logic_garden_341a_rogue_vector.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Vectorization
SCENE: Logic Garden 341a (The Rogue Vector // M2-F1 Pontiac Tow)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING, AERODYNAMICS
HOTFIX: Linear 24.0s Sequence. Daylight Protocol. Camera Lock. Bezier Intersection Sealed.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import matplotlib.path as mpath
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
DURATION = 24.0  
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_341a_rogue"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Lakebed Substrate Matrix
C_STEEL     = '#606065'   # Internal Hardware / Tow Cable
C_DARK      = '#202025'   # Pontiac Chassis
C_GOLD      = '#FFB300'   # Raw ICE Torque
C_CYAN      = '#00FFFF'   # M2-F1 Aerodynamic Geometry
C_MAGENTA   = '#FF0055'   # Surface Friction / Dust Spallation
C_MANTIS    = '#00FF00'   # Lift-Off / Terminal Green

# ------------------------------------------------------------------
# PRE-CALCULATE O(1) KINEMATIC ARRAYS (DETERMINISTIC TIMELINE)
# ------------------------------------------------------------------
time_arr = np.linspace(0, DURATION, TOTAL_FRAMES)
vel_arr = np.zeros(TOTAL_FRAMES)     # Velocity in MPH
dist_arr = np.zeros(TOTAL_FRAMES)    # Integrated distance metric

T_ACCEL_START = 3.0
T_LIFTOFF = 16.0
T_DEKEL = 22.0

for i, t in enumerate(time_arr):
    if t < T_ACCEL_START:
        v = 0.0
    elif t < T_LIFTOFF:
        prg = (t - T_ACCEL_START) / (T_LIFTOFF - T_ACCEL_START)
        v = 125.0 * (prg ** 1.5) # Smooth curve to 125 mph
    elif t < T_DEKEL:
        v = 125.0 # Sustained towing
    else:
        v = 125.0 - 50.0 * (t - T_DEKEL) # Braking phase initiation
    
    vel_arr[i] = v
    if i > 0:
        dist_arr[i] = dist_arr[i-1] + (v * (1.0/FPS)) * 0.5 # Arbitrary visual scaling factor

def draw_industrial_grid(ax, scroll_offset):
    """Draw the Scrolling Substrate Matrix"""
    for i in range(-5, 6):
        ax.plot([i*100, i*100], [-960, 960], color=C_TITANIUM, lw=2, alpha=0.5, zorder=0)
    wrap_mod = int(scroll_offset * 100) % 100
    for j in range(-10, 11):
        y_pos = j*100 - wrap_mod
        ax.plot([-540, 540], [y_pos, y_pos], color=C_TITANIUM, lw=2, alpha=0.5, zorder=0)

def render_frame(packet):
    f, phase_ratio = packet
    t = phase_ratio * DURATION 
    v_mph = vel_arr[f]
    scroll = dist_arr[f]
    
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
    draw_industrial_grid(ax, scroll)

    # ====================================================
    # 1. THE PRIME MOVER: PONTIAC CATALINA
    # ====================================================
    P_Y = 300
    
    ax.add_patch(patches.Rectangle((-70, P_Y-120), 140, 240, facecolor=C_TITANIUM, alpha=0.8, zorder=2))
    ax.add_patch(patches.Rectangle((-60, P_Y-100), 120, 220, facecolor=C_DARK, edgecolor=C_STEEL, lw=4, zorder=10))
    ax.add_patch(patches.Rectangle((-50, P_Y-20), 100, 100, facecolor=C_BG, edgecolor=C_STEEL, lw=3, zorder=11))
    ax.add_patch(patches.Rectangle((-30, P_Y+50), 60, 50, facecolor=C_GOLD, zorder=11))
    
    wheel_w, wheel_h = 20, 40
    ax.add_patch(patches.Rectangle((-75, P_Y-80), wheel_w, wheel_h, facecolor=C_STEEL, zorder=12))
    ax.add_patch(patches.Rectangle((55, P_Y-80), wheel_w, wheel_h, facecolor=C_STEEL, zorder=12))
    
    if v_mph > 0 and t < T_LIFTOFF:
        np.random.seed(int(t*100))
        for wx in [-65, 65]:
            dx = np.random.normal(0, 15, 20)
            dy = np.random.uniform(-100, -20, 20) - (v_mph * 0.5)
            ax.scatter(wx + dx, (P_Y-80) + dy, s=np.random.uniform(10, 40, 20), c=C_MAGENTA, alpha=0.6, edgecolors='none', zorder=5)

    # ====================================================
    # 2. THE TENSION VECTOR (TOW CABLE)
    # ====================================================
    TOW_START = (0, P_Y-100)
    TOW_END = (0, -100)
    
    if v_mph < 2.0 and t < T_ACCEL_START:
        Path = mpath.Path
        pp1 = patches.PathPatch(
            Path([TOW_START, (40, 100), TOW_END], [Path.MOVETO, Path.CURVE3, Path.CURVE3]),
            facecolor='none', edgecolor=C_STEEL, lw=4, linestyle='--', zorder=6
        )
        ax.add_patch(pp1)
        tension_metric = "0.00 N"
        t_col = C_STEEL
    else:
        ax.plot([TOW_START[0], TOW_END[0]], [TOW_START[1], TOW_END[1]], color=C_STEEL, lw=6, zorder=6)
        strain_p = (t * 8) % 1.0
        s_y = TOW_START[1] - strain_p * (TOW_START[1] - TOW_END[1])
        ax.plot([0, 0], [s_y-20, s_y+20], color=C_BG, lw=4, zorder=7)
        
        tension_val = v_mph * 14.5 + (120 if t < T_LIFTOFF else 50)
        tension_metric = f"{tension_val:>6.1f} kN"
        t_col = C_GOLD

    # ====================================================
    # 3. THE PAYLOAD: M2-F1 AERODYNAMIC GEOMETRY 
    # ====================================================
    M_Y = -250
    lift_ratio = np.clip((v_mph / 120.0)**2, 0.0, 1.2)
    is_flying = v_mph >= 120.0
    base_color = C_MANTIS if is_flying else C_CYAN
    
    shadow_offset_y = -10 - (lift_ratio * 40)
    shadow_offset_x = 10 + (lift_ratio * 20)
    m_scale = 1.0 + (lift_ratio * 0.1)
    
    m_pts = [[0, 150], [-70, -100], [70, -100]]
    m_pts = [[x * m_scale, y * m_scale] for x, y in m_pts]
    
    s_pts = [[x + shadow_offset_x, M_Y + y + shadow_offset_y] for x, y in m_pts]
    ax.add_patch(patches.Polygon(s_pts, facecolor=C_TITANIUM, alpha=0.9, zorder=3))

    c_pts = [[x, M_Y + y] for x, y in m_pts]
    ax.add_patch(patches.Polygon(c_pts, facecolor=C_BG, edgecolor=base_color, lw=6, zorder=20))
    
    ax.plot([0, 0], [M_Y+150*m_scale, M_Y-100*m_scale], color=base_color, lw=3, zorder=21)
    ax.plot([-70*m_scale, 70*m_scale], [M_Y-50*m_scale, M_Y-50*m_scale], color=base_color, lw=3, linestyle='--', zorder=21)
    
    if not is_flying and v_mph > 0:
        np.random.seed(int(t*200))
        for gx, gy in [[0, M_Y+100], [-50, M_Y-80], [50, M_Y-80]]:
            dx = np.random.normal(0, 10, 10)
            dy = np.random.uniform(-60, -10, 10)
            ax.scatter(gx + dx, gy + dy, s=np.random.uniform(5, 20, 10), c=C_MAGENTA, alpha=0.8, edgecolors='none', zorder=4)

    # Dynamic airflow paths bending around the lifting body
    if v_mph > 30:
        flow_alpha = min(1.0, v_mph / 100.0)
        flow_color = C_CYAN if not is_flying else C_MANTIS
        Path = mpath.Path
        for f_off in [-100, -80, 80, 100]:
            # Absolute Bezier Math bypassing ConnectionPatch
            ptA = (f_off, M_Y + 300)
            ptB = (f_off * 1.8, M_Y - 200)
            # Control point stretches out to simulate aerodynamic bending
            ctrl = (f_off * 1.5, M_Y + 100) 
            
            p_data = [(Path.MOVETO, ptA), (Path.CURVE3, ctrl), (Path.CURVE3, ptB)]
            codes, verts = zip(*p_data)
            flow_path = Path(verts, codes)
            ax.add_patch(patches.PathPatch(flow_path, facecolor='none', edgecolor=flow_color, lw=2, alpha=flow_alpha*0.5, zorder=18))

    # ====================================================
    # 4. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-341a :: THE ROGUE VECTOR [M2-F1]", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] O(1) RAW COMBUSTION TRANSFER / SUBSTRATE BYPASSED", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    ax.text(-500, -760, "SYS_01 [VELOCITY / Q]        :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, f"V = {v_mph:>05.1f} MPH", color=C_GOLD if v_mph > 0 else C_STEEL, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [TENSION VECTOR]      :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, tension_metric, color=t_col, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    l_status = "AERODYNAMIC LIFT < W [GROUNDED]"
    l_color = C_MAGENTA if (v_mph > 0 and not is_flying) else C_STEEL
    if is_flying:
        l_status = "TATH\u0100T\u0100 // LIFT > W [ORBITAL ROTATION]"
        l_color = C_MANTIS

    ax.text(-500, -840, "STRUCTURAL LOAD MATRIX       :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, l_status, color=l_color, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=l_color, zorder=83))

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
    print(f"LG-341a Revision 3: O(1) BEZIER MATRIX [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
