"""
SOVEREIGN CODE: logic_garden_317b_shipyard_cycle.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 317b (Orbital Shipyard // Assembly Cycle)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING, MEGASCAE ARCHITECTURE
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
OUT_DIR = "frames_317b_shipyard_cycle"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#A0A0A5'
C_STEEL     = '#303035'
C_GOLD      = '#FFB300'   # Internal Energy Spine / Exposed Engineering
C_AZURE     = '#007FFF'   # Supply Mag-Rails
C_CYAN      = '#00FFFF'   # Welding Spallation Sparks
C_MAGENTA   = '#FF0055'   # Deceleration Thrust / Friction
C_MANTIS    = '#00FF00'   # Completion / Terminal Green
C_WHITE     = '#FFFFFF'

# ------------------------------------------------------------------
# O(1) METALLIC SHADER AND KINEMATIC ARMS
# ------------------------------------------------------------------
def draw_cylinder(ax, y_bottom, y_top, radius, zorder=5, color_base=C_STEEL, is_horizontal=False, x_center=0):
    if y_bottom >= y_top: return # Zero-height culling
    steps = 40
    r_val, g_val, b_val = [int(color_base.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)]

    for i in range(steps):
        ratio = (i / float(steps - 1))
        # Hard spec highlight simulating raw zero-atmosphere lighting
        light_curve = np.exp(-((ratio - 0.35) ** 2) / 0.04)
        ambient = 0.2 + 0.8 * light_curve
        c = f'#{int(r_val*ambient):02x}{int(g_val*ambient):02x}{int(b_val*ambient):02x}'

        w = (radius * 2) / steps
        x_start = x_center - radius + (i * w)

        if not is_horizontal:
            rect = patches.Rectangle((x_start, y_bottom), w, y_top - y_bottom, facecolor=c, edgecolor='none', zorder=zorder)
        else:
            rect = patches.Rectangle((y_bottom, x_start), y_top - y_bottom, w, facecolor=c, edgecolor='none', zorder=zorder)
        ax.add_patch(rect)

def draw_gantry_arm(ax, y_anchor, clamp_prg, side='left', zorder=8):
    # Brutalist angular scaffolding arms physically extending inward to clamp the hull
    sign = -1 if side == 'left' else 1
    
    extension = clamp_prg * 140 # Modifies X reach

    # Base anchor connecting to the outer rails (STATIC)
    poly_base = patches.Polygon([
        [sign * 480, y_anchor - 40], [sign * 400, y_anchor - 40],
        [sign * 400, y_anchor + 40], [sign * 480, y_anchor + 40]
    ], facecolor=C_TEXT, zorder=zorder)

    # Angled thrust arm extending toward the ship hull (DYNAMIC)
    poly_arm = patches.Polygon([
        [sign * 400, y_anchor - 30], [sign * (320 - extension), y_anchor - 80],
        [sign * (320 - extension), y_anchor - 40], [sign * 400, y_anchor + 30]
    ], facecolor=C_STEEL, zorder=zorder)

    # Locking clamp touching the hull (DYNAMIC)
    poly_clamp = patches.Polygon([
        [sign * (320 - extension), y_anchor - 100], [sign * (280 - extension), y_anchor - 100],
        [sign * (280 - extension), y_anchor - 20], [sign * (320 - extension), y_anchor - 20]
    ], facecolor=C_TITANIUM if clamp_prg < 0.99 else C_MANTIS, zorder=zorder+0.1)

    ax.add_patch(poly_base)
    ax.add_patch(poly_arm)
    ax.add_patch(poly_clamp)

# ------------------------------------------------------------------
# CACHED KINEMATICS (WELDING POINTS & MAG-RAIL DROPS)
# ------------------------------------------------------------------
N_CARGO = 24
c_x = np.random.choice([-450, -420, 420, 450], N_CARGO)
c_y_offset = np.random.uniform(0, 1920, N_CARGO)
c_h = np.random.uniform(60, 140, N_CARGO)
c_w = 20

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

    # 1. TEMPORAL PHYSICS LOGIC
    # --------------------------
    T_ARRIVE = 4.0
    T_CLAMP  = 6.0
    T_WELD   = 18.0
    T_RELEASE= 20.0
    
    # Y-axis translation of the ship
    ship_y = 0.0
    if t < T_ARRIVE:
        # Decelerating into the matrix from below
        prg = t / T_ARRIVE
        ship_y = -1400.0 + (1400.0 * (prg ** 0.5)) # Fast entry, slow clamp
    elif t > T_RELEASE:
        # Accelerating out of the matrix upward
        prg = (t - T_RELEASE) / (DURATION - T_RELEASE)
        ship_y = 0.0 + (1800.0 * (prg ** 2.0)) # Exponential exit
        
    # Gantry Clamp State (0.0 = Open, 1.0 = Clamped)
    clamp_prg = 0.0
    if T_ARRIVE <= t < T_CLAMP:
        clamp_prg = (t - T_ARRIVE) / (T_CLAMP - T_ARRIVE)
    elif T_CLAMP <= t <= T_RELEASE:
        clamp_prg = 1.0
    elif t > T_RELEASE:
        clamp_prg = 1.0 - ((t - T_RELEASE) / 1.5)
    clamp_prg = np.clip(clamp_prg, 0.0, 1.0)
    
    # Assembly State (The hull plates closing over the Gold spine)
    # Gap originally exists from ShipY - 300 to ShipY + 300
    gap_half = 300.0 
    if T_CLAMP < t <= T_WELD:
        build_prg = (t - T_CLAMP) / (T_WELD - T_CLAMP)
        gap_half = 300.0 * (1.0 - build_prg)
    elif t > T_WELD:
        gap_half = 0.0 # Fully locked
        
    # 2. THE SHIP RENDER
    # ------------------
    # The Exposed C_GOLD Spine (Z=3)
    draw_cylinder(ax, ship_y - 800, ship_y + 800, radius=90, color_base=C_GOLD, zorder=3)
    for spine_y in range(-780, 780, 60):
        sy = ship_y + spine_y
        draw_cylinder(ax, sy, sy+15, radius=95, color_base=C_TEXT, zorder=3.1)

    # Outer Hull Plating (C_TITANIUM) (Z=4)
    # Bottom portion building upwards
    if ship_y - 800 < ship_y - gap_half:
        draw_cylinder(ax, ship_y - 800, ship_y - gap_half, radius=180, color_base=C_TITANIUM, zorder=4)
    # Top portion building downwards
    if ship_y + gap_half < ship_y + 800:
        draw_cylinder(ax, ship_y + gap_half, ship_y + 800, radius=180, color_base=C_TITANIUM, zorder=4)

    # 3. THRUST SPALLATION (Ingress / Egress)
    # ---------------------------------------
    if t < T_ARRIVE:
        # Firing massive front retro thrusters (C_MAGENTA)
        np.random.seed(int(t*100))
        for _ in range(40):
            ex = np.random.uniform(-180, 180)
            ey = ship_y + 800 + np.random.uniform(0, 200)
            ax.scatter(ex, ey, s=np.random.uniform(20, 80), c=C_MAGENTA, edgecolors='none', alpha=0.7, zorder=10)
    elif t > T_RELEASE:
        # Firing main engine rear thrust (C_CYAN/MANTIS)
        np.random.seed(int(t*100))
        for _ in range(60):
            ex = np.random.uniform(-150, 150)
            offset = (t - T_RELEASE) * 50
            ey = ship_y - 800 - np.random.uniform(0, 300) - offset
            ax.scatter(ex, ey, s=np.random.uniform(40, 150), c=C_CYAN, edgecolors='none', alpha=0.9, zorder=1)

    # 4. SHIPYARD LATTICE & GANTRY (Z=2 & 8)
    # --------------------------------------
    # Static boundary rails
    draw_cylinder(ax, -960, 960, radius=30, color_base=C_STEEL, x_center=-450, zorder=8)
    draw_cylinder(ax, -960, 960, radius=30, color_base=C_STEEL, x_center=-420, zorder=2) 
    draw_cylinder(ax, -960, 960, radius=30, color_base=C_STEEL, x_center=450, zorder=8)
    draw_cylinder(ax, -960, 960, radius=30, color_base=C_STEEL, x_center=420, zorder=2)

    # Dynamic Gantry Clamp Arms
    for gantry_y in [-600, -300, 0, 300, 600]:
        draw_gantry_arm(ax, gantry_y, clamp_prg, side='left', zorder=8)
        draw_gantry_arm(ax, gantry_y, clamp_prg, side='right', zorder=8)

    # 5. MAG-RAIL KINEMATICS (Logistics)
    # ----------------------------------
    v_cargo = 800.0 if (t < T_CLAMP or t > T_RELEASE) else 2400.0 # Speed up during work phase
    cargo_y_current = ((c_y_offset + t * v_cargo) % 1920) - 960
    for i in range(N_CARGO):
        cy = cargo_y_current[i]
        c_z = 8.5 if abs(c_x[i]) == 450 else 2.5
        rect = patches.Rectangle((c_x[i] - c_w/2, cy), c_w, c_h[i], facecolor=C_TEXT, edgecolor=C_AZURE, lw=2, zorder=c_z)
        ax.add_patch(rect)

    # 6. WELDING TENSORS (O(1) Eulerian Spallation during ASSEMBLY phase)
    # -------------------------------------------------------------------
    if T_CLAMP < t < T_WELD:
        np.random.seed(int(f/2)) 
        for i in range(25): # Heavy welding
            # Calculate dynamic weld points creeping toward the center
            weld_y_top = ship_y + gap_half + np.random.uniform(-10, 10)
            weld_y_bot = ship_y - gap_half + np.random.uniform(-10, 10)
            w_y = np.random.choice([weld_y_top, weld_y_bot])
            w_x = np.random.uniform(-180, 180)
            
            # Flash core
            ax.add_patch(patches.Circle((w_x, w_y), radius=np.random.uniform(4, 12), color=C_WHITE, zorder=9))
            # Magenta thermal splash
            for _ in range(3):
                sx = w_x + np.random.uniform(-40, 40)
                sy = w_y + np.random.uniform(-60, 60)
                ax.plot([w_x, sx], [w_y, sy], color=C_CYAN, lw=2, zorder=8.5)

    # ====================================================
    # 7. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-317b :: SHIPYARD THERMODYNAMIC CYCLE", color=C_TEXT, fontsize=22, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] O(1) INGRESS, ASSEMBLY, AND EGRESS SEQUENCE", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    # State Telemetry Logic
    if t < T_ARRIVE:
        s_cmd = "PHASE 1: INGRESS KINEMATICS"
        s_col = C_MAGENTA
        s_det = "DECELERATING // VECTORS ACTIVE"
    elif t < T_CLAMP:
        s_cmd = "PHASE 2: PHYSICAL CONSTRAINT"
        s_col = C_GOLD
        s_det = "GANTRY ARMS DEPLOYING TO Y=0"
    elif t < T_WELD:
        s_cmd = "PHASE 3: BARE-METAL ASSEMBLY"
        s_col = C_CYAN
        s_det = "SEALING HULL PLATINGS // MAG-RAILS MAX"
    elif t < T_RELEASE:
        s_cmd = "PHASE 4: GANTRY PURGE"
        s_col = C_GOLD
        s_det = "HULL INTEGRITY 100% // RETRACTING"
    else:
        s_cmd = "PHASE 5: EGRESS KINEMATICS"
        s_col = C_MANTIS
        s_det = "TATH\u0100T\u0100 // VECTOR THRUST SECURED"

    ax.text(-500, -760, "SYS_01 [ENGINEERING CYCLE]   :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, s_cmd, color=s_col, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [GANTRY LOGIC]        :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, s_det, color=s_col, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "STRUCTURAL THROUGHPUT RANK   :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, f"{(100 * phase_ratio):>04.1f}% [O(1) TIMELINE]", color=C_STEEL, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider [Strict Tuples]
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=s_col, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0)
    
    # Absolute Memory Annihilation
    plt.close('all')
    gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-317b: SHIPYARD THERMODYNAMIC CYCLE [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
