"""
SOVEREIGN CODE: logic_garden_346b_oceanic_tensor.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 346b (SS Great Britain & The Oceanic Tensor)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING, FLUID DYNAMICS
HOTFIX: Linear 24.0s Sequence. Topological Immersion Matrix corrected.
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
DURATION = 24.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_346b_oceanic_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Brunel Iron Hull
C_STEEL     = '#606065'   # Bulkheads / Hardware
C_DARK      = '#202025'   # Deep Structural
C_CYAN      = '#00FFFF'   # Submerged Propeller Matrix
C_GOLD      = '#FFB300'   # Legacy Wooden Hull Constraint
C_MAGENTA   = '#DE008A'   # Thermodynamic Waste / Spallation / Breach
C_MANTIS    = '#00FF00'   # Terminal Thrust / Perfect Buoyancy
C_WATER     = '#007FFF'   # Ocean Fluid Body (Azure)

# ------------------------------------------------------------------
# O(1) KINEMATIC & FLUID FUNCTIONS
# ------------------------------------------------------------------
def ease_in_out(t):
    t = np.clip(t, 0.0, 1.0)
    return 4 * t**3 if t < 0.5 else 1 - (-2 * t + 2)**3 / 2

def rotate_pt(x, y, cx, cy, angle_deg):
    a = np.radians(angle_deg)
    rx = cx + (x - cx) * np.cos(a) - (y - cy) * np.sin(a)
    ry = cy + (x - cx) * np.sin(a) + (y - cy) * np.cos(a)
    return rx, ry

def draw_industrial_grid(ax):
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

    # BARE-METAL CAMERA LOCK
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)
    ax.autoscale(False)
    draw_industrial_grid(ax)

    # 1. TIMELINE & PHASING (Architect's Script)
    # ------------------------------------------
    T_BREACH = 5.0
    T_BRUNEL_FIX_S = 8.0
    T_BRUNEL_FIX_E = 10.0
    T_PADDLE_SHEAR_S = 13.0
    T_PADDLE_SHEAR_E = 14.5
    T_PROP_DEPLOY = 16.0

    # Fluid Dynamics Base (SOVEREIGN FIX: True Topological Intersection)
    OCEAN_BASE_Y = -60

    # True velocity increases when propeller converts 100% torque
    vel_multiplier = 1.0 if t < T_PROP_DEPLOY else 1.0 + 2.0 * ease_in_out(min(1.0, (t-T_PROP_DEPLOY)/2.0))
    fluid_phase = (t * 4.0 * vel_multiplier) % (2 * np.pi * 100)

    # Wave array mapping
    x_wave = np.linspace(-600, 600, 200)
    y_wave = OCEAN_BASE_Y + 30 * np.sin(x_wave*0.015 - fluid_phase) + 10 * np.cos(x_wave*0.03 + fluid_phase*1.5)

    # Ship Architecture Constants
    SHIP_CG_X, SHIP_CG_Y = 0, 0
    HULL_W = 600
    HULL_D = 140

    # Damage and Pitch Mathematics
    flood_level = 0.0
    pitch_deg = 0.0
    
    if t >= T_BREACH and t < T_BRUNEL_FIX_S:
        # Full contiguous interior floods. Catastrophic imbalance.
        flood_level = np.clip((t - T_BREACH) / 2.0, 0.0, 1.0)
        pitch_deg = -12.0 * ease_in_out(flood_level)
    elif t >= T_BRUNEL_FIX_S and t < T_BRUNEL_FIX_E:
        # Bulkheads drop. Flooding is contained. Water drains from rear. Pitch corrects.
        fix_prg = np.clip((t - T_BRUNEL_FIX_S) / (T_BRUNEL_FIX_E - T_BRUNEL_FIX_S), 0.0, 1.0)
        pitch_deg = -12.0 * (1.0 - ease_in_out(fix_prg))
        flood_level = 1.0
    elif t >= T_BRUNEL_FIX_E:
        pitch_deg = 0.0
        flood_level = 1.0 # Only exists in forward compartment now

    # Dynamic Structural Color
    if t < T_BRUNEL_FIX_S:
        hull_color = C_GOLD # Legacy Wood
        edge_color = C_GOLD
        state_phase = "BIOLOGICAL_VULNERABILITY"
    elif t < T_BRUNEL_FIX_E:
        prg = (t - T_BRUNEL_FIX_S) / 2.0
        hull_color = C_TITANIUM # Upgrading to Iron
        edge_color = C_STEEL
        state_phase = "HARDWARE_LOCKING"
    else:
        hull_color = C_TITANIUM
        edge_color = C_STEEL
        if t < T_PADDLE_SHEAR_S:
            state_phase = "COMPARTMENTALIZED_BUOYANCY"
        elif t < T_PROP_DEPLOY:
            state_phase = "PADDLE_ERADICATION"
        else:
            state_phase = "PROPELLER_MATRIX_LOCKED"

    # 2. DRAWING THE BACKGROUND OCEAN (Behind Hull)
    # ---------------------------------------------
    ax.fill_between(x_wave, -960, y_wave, facecolor=C_WATER, alpha=0.3, zorder=5)

    # 3. KINEMATIC HULL ARCHITECTURE
    # ------------------------------
    bow_pts = [(HULL_W/2, 80), (HULL_W/2 + 60, 20), (HULL_W/2 - 20, -HULL_D)]
    stern_pts = [(-HULL_W/2 + 40, -HULL_D), (-HULL_W/2 - 40, 20), (-HULL_W/2, 80)]
    deck_pts = [stern_pts[2], bow_pts[0]]
    keel_pts = [bow_pts[2], stern_pts[0]]
    
    raw_hull = bow_pts + [keel_pts[1]] + stern_pts + [deck_pts[0]]
    rot_hull = [rotate_pt(x, y, SHIP_CG_X, SHIP_CG_Y, pitch_deg) for (x, y) in raw_hull]
    
    # Internal flooding visualization (Accurate to sea level)
    if flood_level > 0:
        flood_x_start = -HULL_W/2 + 40 if t < T_BRUNEL_FIX_S else HULL_W/4
        flood_x_end = bow_pts[2][0]
        
        # Absolute structural coordinate mapping for water inside the hull
        waterline_relative_to_cg = OCEAN_BASE_Y - SHIP_CG_Y
        water_h = -HULL_D + ( (waterline_relative_to_cg - (-HULL_D)) * flood_level )
        
        flood_pts = [
            (flood_x_end, water_h), (flood_x_end, -HULL_D),
            (flood_x_start, -HULL_D), (flood_x_start, water_h)
        ]
        rot_flood = [rotate_pt(x, y, SHIP_CG_X, SHIP_CG_Y, pitch_deg) for (x, y) in flood_pts]
        ax.add_patch(patches.Polygon(rot_flood, facecolor=C_WATER, alpha=0.6, zorder=12))

    # Hull Plating
    ax.add_patch(patches.Polygon(rot_hull, facecolor=C_BG, edgecolor=edge_color, lw=6, zorder=15))
    ax.add_patch(patches.Polygon(rot_hull, facecolor=hull_color, alpha=0.2, zorder=16))

    # Breach Indicator (Strictly underwater now relative to OCEAN_BASE_Y)
    if t >= T_BREACH:
        breach_x, breach_y = rotate_pt(HULL_W/2 - 80, -90, SHIP_CG_X, SHIP_CG_Y, pitch_deg)
        breach_alpha = np.clip(1.0 - (t - T_BRUNEL_FIX_S), 0.0, 1.0) if t > T_BRUNEL_FIX_S else 1.0
        if breach_alpha > 0:
            ax.scatter(breach_x, breach_y, s=800, facecolor='none', edgecolor=C_MAGENTA, lw=6, marker='x', alpha=breach_alpha, zorder=20)
            ax.add_patch(patches.Circle((breach_x, breach_y), 40, fill=False, edgecolor=C_MAGENTA, lw=3, alpha=breach_alpha*0.7, zorder=21))

    # The O(1) Bulkheads
    if t >= T_BRUNEL_FIX_S:
        b_alpha = np.clip((t - T_BRUNEL_FIX_S) / 1.0, 0.0, 1.0)
        c_bulk = mcolors.to_rgba(C_STEEL, b_alpha)
        
        for b_x in [-HULL_W/4, 0, HULL_W/4]:
            top_x, top_y = rotate_pt(b_x, 80, SHIP_CG_X, SHIP_CG_Y, pitch_deg)
            bot_x, bot_y = rotate_pt(b_x, -HULL_D, SHIP_CG_X, SHIP_CG_Y, pitch_deg)
            ax.plot([top_x, bot_x], [top_y, bot_y], color=c_bulk, lw=8, zorder=18)
            for ry in np.linspace(-HULL_D+10, 70, 6):
                riv_x, riv_y = rotate_pt(b_x, ry, SHIP_CG_X, SHIP_CG_Y, pitch_deg)
                ax.add_patch(patches.Circle((riv_x, riv_y), 4, facecolor=C_BG, edgecolor=c_bulk, lw=2, zorder=19))

    # 4. PROPULSION LOGIC (PADDLES VS SCREW)
    # -------------------------------------
    paddle_alpha = 1.0
    if t >= T_PADDLE_SHEAR_S:
        paddle_alpha = np.clip(1.0 - (t - T_PADDLE_SHEAR_S) / 0.5, 0.0, 1.0)

    if paddle_alpha > 0:
        pad_r = 110
        pad_cx, pad_cy = rotate_pt(0, 0, SHIP_CG_X, SHIP_CG_Y, pitch_deg) # Center sits perfectly intersecting the water line
        pad_rot = -t * 10.0
        
        c_pad = mcolors.to_rgba(C_DARK if t < T_BREACH else C_MAGENTA, paddle_alpha)
        
        ax.add_patch(patches.Circle((pad_cx, pad_cy), pad_r, fill=False, edgecolor=c_pad, lw=8, zorder=25))
        ax.add_patch(patches.Circle((pad_cx, pad_cy), 20, facecolor=C_BG, edgecolor=c_pad, lw=4, zorder=26))
        
        for i in range(12):
            ang = pad_rot + (i * 2*np.pi/12)
            px = pad_cx + pad_r * np.cos(ang)
            py = pad_cy + pad_r * np.sin(ang)
            ax.plot([pad_cx, px], [pad_cy, py], color=c_pad, lw=6, zorder=25)
            
            # Spallation (Splashing precisely where paddle blades cross the water layer)
            if py < y_wave[100] and py > y_wave[100] - 60:
                splash_color = mcolors.to_rgba(C_MAGENTA, paddle_alpha * 0.8)
                ax.scatter(px + np.random.uniform(-30,30), py + np.random.uniform(-10,40), s=np.random.uniform(20,70), color=splash_color, zorder=40)

    # The Sovereign Fix: Submerged Screw Propeller
    prop_alpha = 0.0
    if t >= T_PROP_DEPLOY:
        prop_alpha = np.clip((t - T_PROP_DEPLOY) / 1.0, 0.0, 1.0)
    
    if prop_alpha > 0:
        p_cx, p_cy = rotate_pt(-HULL_W/2, -100, SHIP_CG_X, SHIP_CG_Y, pitch_deg) # Utterly submerged.
        p_r = 45
        prop_rot = t * 25.0 
        
        c_prop = mcolors.to_rgba(C_CYAN, prop_alpha)
        
        # Central shaft
        s_x, s_y = rotate_pt(-HULL_W/2 + 60, -100, SHIP_CG_X, SHIP_CG_Y, pitch_deg)
        ax.plot([s_x, p_cx], [s_y, p_cy], color=C_STEEL, lw=10, alpha=prop_alpha, zorder=14)
        
        # Helical Blades
        for i in range(4):
            ang = prop_rot + (i * np.pi/2)
            blade_ext = p_r * np.cos(ang)
            b_x1, b_y1 = p_cx, p_cy - blade_ext
            b_x2, b_y2 = p_cx, p_cy + blade_ext
            ax.plot([b_x1, b_x2], [b_y1, b_y2], color=c_prop, lw=12, solid_capstyle='round', zorder=25)
        
        ax.add_patch(patches.Circle((p_cx, p_cy), 12, facecolor=C_BG, edgecolor=c_prop, lw=4, alpha=prop_alpha, zorder=26))
        
        # Submerged Thrust Vectors (C_MANTIS - Terminal Green)
        if prop_alpha > 0.8:
            for _ in range(5):
                tv_x = p_cx - np.random.uniform(20, 180)
                tv_y = p_cy + np.random.uniform(-40, 40)
                ax.plot([tv_x, tv_x - 60], [tv_y, tv_y], color=C_MANTIS, lw=4, alpha=0.8, zorder=24) # Render under hull, but thick

    # 5. DRAWING THE FOREGROUND OCEAN (True Immersion Matrix)
    # -------------------------------------------------------
    # SOVEREIGN FIX: This solidifies the "sinking" proof. Water overlays the hull and propeller line.
    ax.fill_between(x_wave, -960, y_wave, facecolor=C_WATER, alpha=0.35, zorder=35)
    ax.plot(x_wave, y_wave, color=C_WATER, lw=6, zorder=36)

    # ====================================================
    # 6. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)

    ax.text(-500, 890, "LG-346b :: THE OCEANIC TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-0.75] COMPARTMENTALIZATION & THE KINEMATIC PROPELLER", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    # State Telemetry Logic
    if state_phase == "BIOLOGICAL_VULNERABILITY":
        s1, c1 = "LEGACY WOOD ARCHITECTURE", C_GOLD
        s2, c2 = "THERMODYNAMIC WASTE // PADDLE SPALLATION", C_MAGENTA
        hud_health = "WATER TIGHT COMPROMISE IMMINENT"
    elif state_phase == "HARDWARE_LOCKING":
        s1, c1 = "THE SOVEREIGN FIX // C_TITANIUM ENGAGED", C_CYAN
        s2, c2 = "DROPPING O(1) VERTICAL BULKHEADS", C_STEEL
        hud_health = "MEMORY COMPARTMENTALIZATION ARRESTING FLOOD"
    elif state_phase == "COMPARTMENTALIZED_BUOYANCY":
        s1, c1 = "C_STEEL BULKHEAD MATRIX SECURE", C_MANTIS
        s2, c2 = "BUOYANCY VECTOR MATHEMATICALLY RESTORED", C_CYAN
        hud_health = "BREACH QUARANTINED // PITCH HORIZONTAL"
    elif state_phase == "PADDLE_ERADICATION":
        s1, c1 = "ERADICATING VULNERABLE KINEMATICS", C_MAGENTA
        s2, c2 = "SERIALIZE RAZOR SHEARING EXTERNAL HARDWARE", C_GOLD
        hud_health = "PREPARING SUBSTRATE FOR O(1) PROPELLER"
    else:
        s1, c1 = "THE BRUNEL BASEPLATE VERIFIED", C_MANTIS
        s2, c2 = "100% TORQUE CONVERSION // SUBMERGED MATRIX", C_MANTIS
        hud_health = "TERMINAL GREEN FLOW ACHIEVED"

    ax.text(-500, -760, "SYS_01 [HULL TOPOLOGY]       :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, s1, color=c1, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [PROPULSION MATRIX]   :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, s2, color=c2, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "STRUCTURAL LOAD AUDIT        :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, hud_health, color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider [Strict Tuples]
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=c1, zorder=83))

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
    print(f"LG-346b: THE OCEANIC TENSOR (SS GREAT BRITAIN) [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
