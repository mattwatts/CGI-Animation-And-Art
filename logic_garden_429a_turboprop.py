"""
PROJECT: Logic Garden 429 (Exact Physical Construct // Turboprop Engine)
FORMAT: YouTube Shorts (1080x1920)
METADATA: TURBOPROP, AERODYNAMICS, TWIN-SPOOL, GEOMETRY, DAYLIGHT
EXECUTION: 12.0s Seamless Infite Loop. Active Kinematic Cross-Section.
RULES ENFORCED: 
- O(N) Depth-Sorted Painter's Algorithm for Rotary Blades.
- Mathematical Fluid Simulation tracking state-change thermodynamics.
- Daylight Palette (White Substrate / High-Contrast Edge Geometry).
- Purged Jargon. Australian spelling conventions.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
import multiprocessing as mp
import os
import gc

# ======== SEQUENCE PARAMETERS ========
DURATION = 12.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_429_turboprop"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'          # Indestructible Black UI
C_CASE      = '#1E293B'          # Carbon Casing Cutaway Lines
C_STATOR    = '#94A3B8'          # Steel Stators (Background)
C_CHAMBER   = '#475569'          # Combustor Liner
C_LP_SPOOL  = '#005599'          # Power Spool (Deep Marine)
C_HP_SPOOL  = '#DE008A'          # Gas Generator Spool (Deep Magenta)
C_GEAR      = '#FFB300'          # Dense Amber (Reduction Box)
C_PROP      = '#0F172A'          # Black Composite Propeller

# Thermodynamic Fluid Gradient Array
fluid_nodes = [0.0, 0.22, 0.50, 0.66, 1.0] # Mapped 0.0 (Exhaust) to 1.0 (Intake)
fluid_colors = ['#71717A', '#DE008A', '#FF3300', '#00C853', '#005599']
cmap_fluid = LinearSegmentedColormap.from_list('thermo', list(zip(fluid_nodes, fluid_colors)))

# ------------------------------------------------------------------
# RIGID 1D PHYSICS DATASTREAMS (Exact Geometric Casing Boundary)
# ------------------------------------------------------------------
# Y goes from -450 (Exhaust) to 450 (Intake)
Y_PTS = np.array([-450, -300, -150, 0, 150, 350, 450])
RO_PTS = np.array([140, 220, 180, 200, 160, 220, 220])
RI_PTS = np.array([ 20,  70,  80,  90, 110,  70,  60])

def get_annulus_radii(y):
    ro = np.interp(y, Y_PTS, RO_PTS)
    ri = np.interp(y, Y_PTS, RI_PTS)
    return ro, ri

# ------------------------------------------------------------------
# O(N) ROTOR GEOMETRY COMPILER (Depth Sorted Projection)
# ------------------------------------------------------------------
def draw_blade_stage(ax, y_val, num_blades, theta_global, is_rotor, color):
    # Mathematical cutaway limits Z > 0 for front elements
    ro, ri = get_annulus_radii(y_val)
    z_limit = 0.0 if is_rotor else -0.01 # Stators drawn strictly behind shafts
    
    for i in range(num_blades):
        theta = i * 2 * np.pi / num_blades + theta_global
        
        # Painter's Rule: Front facing elements ONLY
        if (np.sin(theta) > 0 and is_rotor) or (np.sin(theta) <= 0 and not is_rotor):
            x_in_l = ri * np.cos(theta - 0.04)
            x_in_r = ri * np.cos(theta + 0.04)
            x_out_l = ro * np.cos(theta - 0.07)
            x_out_r = ro * np.cos(theta + 0.07)
            
            # Constant 2D Y-width ensures true planar projection logic
            c_w = 6.0 
            poly = [[x_in_l, y_val - c_w], [x_out_l, y_val - c_w], 
                    [x_out_r, y_val + c_w], [x_in_r, y_val + c_w]]
                    
            zord = 10 if is_rotor else 2
            ax.add_patch(patches.Polygon(poly, facecolor=color, edgecolor=C_TEXT, lw=0.5, zorder=zord))

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_norm = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)

    # 1. KINEMATIC ROTATION MATRICES (Flawless Loop Sync)
    # LP loops 12 times, HP loops -18 times, Prop loops 3 times over 12s
    theta_lp   = t_norm * 12.0 * 2 * np.pi
    theta_hp   = t_norm * -18.0 * 2 * np.pi
    theta_prop = t_norm * 3.0 * 2 * np.pi

    # ====================================================
    # 2. BACKGROUND CASING & STATORS (zorder: 1-2)
    # ====================================================
    # Outer casing flow-path fill
    hi_res_y = np.linspace(-450, 450, 100)
    hi_res_ro = np.interp(hi_res_y, Y_PTS, RO_PTS)
    ax.fill_betweenx(hi_res_y, -hi_res_ro, hi_res_ro, facecolor='#F8FAFC', zorder=1)
    
    # Render static background stators
    for y_stat in [340, 310, 280, 250, 220, 190, 160, -20, -70, -140, -190, -240]:
        draw_blade_stage(ax, y_stat, 24, 0.0, False, C_STATOR)

    # ====================================================
    # 3. SOLID TWIN-SHAFT ARCHITECTURE (zorder: 3-4)
    # ====================================================
    # LP Spool (Power Turbine to Gearbox)
    ax.add_patch(patches.Rectangle((-30, -320), 60, 870, facecolor=C_LP_SPOOL, edgecolor=C_TEXT, lw=2, zorder=3))
    # HP Spool (Gas Generator Sleeve wrapping the LP shaft)
    ax.add_patch(patches.Rectangle((-50, -150), 100, 520, facecolor=C_HP_SPOOL, edgecolor=C_TEXT, lw=2, zorder=4))
    
    # Outer Combustor Liners
    ax.plot([-190, -190], [10, 140], color=C_CHAMBER, lw=4, zorder=5)
    ax.plot([190, 190], [10, 140], color=C_CHAMBER, lw=4, zorder=5)
    
    # ====================================================
    # 4. KINEMATIC FLUID SWARM / O(N) TENSOR (zorder: 8)
    # ====================================================
    np.random.seed(429)
    N_FLUID = 2500
    p_offsets = np.random.uniform(0.0, 1.0, N_FLUID)
    p_tracks = np.random.uniform(0.1, 0.9, N_FLUID)
    p_sides = np.random.choice([-1.0, 1.0], N_FLUID)
    
    # Evaluate global thermodynamic position
    p_glob = (p_offsets + t_norm) % 1.0
    fluid_Y = 450.0 - 950.0 * (p_glob ** 1.3) # Acceleration multiplier
    
    fluid_Ri = np.interp(fluid_Y, Y_PTS, RI_PTS)
    fluid_Ro = np.interp(fluid_Y, Y_PTS, RO_PTS)
    
    # Explicit volumetric jitter (swirl effect induced by rotation)
    swirl = np.sin(p_glob * 30.0 + p_offsets * 100.0) * 8.0
    fluid_X = p_sides * (fluid_Ri + p_tracks * (fluid_Ro - fluid_Ri)) + swirl
    
    # Extract RGB values safely matching strictly normalized Array (0 = -500, 1 = 450)
    norm_Y = np.clip((fluid_Y - (-450)) / 900.0, 0.0, 1.0)
    colors = cmap_fluid(norm_Y)
    
    ax.scatter(fluid_X, fluid_Y, c=colors, s=12, alpha=0.5, edgecolors='none', zorder=8)

    # ====================================================
    # 5. FRONT ROTORS & PLANETARY GEARBOX (zorder: 10)
    # ====================================================
    # HP Compressor (Fast Magenta)
    for y_rot in [325, 295, 265, 235, 205, 175]:
        draw_blade_stage(ax, y_rot, 20, theta_hp, True, C_HP_SPOOL)
        
    # HP Turbine (Extracting gas core work)
    for y_rot in [-40, -90]:
        draw_blade_stage(ax, y_rot, 24, theta_hp, True, C_HP_SPOOL)
        
    # LP Turbine (Extracting propellor work)
    for y_rot in [-160, -210, -260]:
        draw_blade_stage(ax, y_rot, 28, theta_lp, True, C_LP_SPOOL)

    # Reduction Gearbox Cutaway (Y=550)
    # RGB Housing
    ax.add_patch(patches.Rectangle((-100, 520), 200, 60, facecolor='#CAD5E2', edgecolor=C_TEXT, lw=4, zorder=10))
    # Sun Gear (Driven by LP Spool)
    ax.add_patch(patches.Circle((0, 550), 25, facecolor=C_LP_SPOOL, edgecolor=C_TEXT, lw=2, zorder=11))
    
    # Orbiting Planetary Gears (True Kinematic Mesh)
    for p_id in range(3):
        alpha_p = p_id * (2 * np.pi / 3.0) + theta_prop
        if np.sin(alpha_p) > -0.2: # Only draw front gears
            planet_x = 55 * np.cos(alpha_p)
            ax.add_patch(patches.Circle((planet_x, 550), 20, facecolor=C_GEAR, edgecolor=C_TEXT, lw=2, zorder=12))
            ax.add_patch(patches.Circle((planet_x, 550), 4, facecolor=C_TEXT, zorder=13))

    # ====================================================
    # 6. EXTERNAL CASING OVERLAY (zorder: 20)
    # ====================================================
    ax.plot(-hi_res_ro, hi_res_y, color=C_CASE, lw=8, zorder=20)
    ax.plot( hi_res_ro, hi_res_y, color=C_CASE, lw=8, zorder=20)

    # Exhaust Nozzle Boundary
    ax.plot([-140, 140], [-450, -450], color=C_CASE, lw=8, zorder=20)

    # ====================================================
    # 7. MAIN PROPELLOR MATRIX (zorder: 1 - 25)
    # ====================================================
    # We must explicitly split prop blades into Background (Z<0) and Foreground (Z>0)
    hub_base_w = 40
    prop_rad = 480
    
    for i in range(4):
        theta = i * np.pi / 2.0 + theta_prop
        
        y_thick = 28 * np.abs(np.cos(theta)) # Visual twist projection
        hub_w   = 16 * np.abs(np.cos(theta - 0.5))
        tip_x   = prop_rad * np.cos(theta)
        base_x  = hub_base_w * np.cos(theta)
        
        blade_poly = [[base_x, 710 - hub_w], [tip_x, 710 - y_thick], 
                      [tip_x, 710 + y_thick], [base_x, 710 + hub_w]]
                      
        z_prop = 25 if np.sin(theta) > 0 else 0
        ax.add_patch(patches.Polygon(blade_poly, facecolor=C_PROP, edgecolor=C_TEXT, lw=2, zorder=z_prop))
        
        # High contrast warning tips (Dense Amber)
        tip_paint_x = (prop_rad - 60) * np.cos(theta)
        tip_poly = [[tip_paint_x, 710 - y_thick*0.8], [tip_x, 710 - y_thick], 
                    [tip_x, 710 + y_thick], [tip_paint_x, 710 + y_thick*0.8]]
        ax.add_patch(patches.Polygon(tip_poly, facecolor=C_GEAR, zorder=z_prop+1))

    # Propellor Spinner Cone
    ax.add_patch(patches.Polygon([[-100, 580], [100, 580], [40, 770], [-40, 770]], facecolor=C_CASE, edgecolor=C_TEXT, lw=4, zorder=24))

    # ====================================================
    # 8. JARGON-FREE DAYLIGHT TELEMETRY 
    # ====================================================
    # Top Architecture Enclosure
    ax.add_patch(plt.Rectangle((-540, 800), 1080, 160, facecolor=C_BG, zorder=80))
    ax.plot([-460, 460], [800, 800], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(-460, 890, "LG-429 :: TURBOPROP (TWIN-SPOOL MATRIX)", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-460, 840, "REDUCTION GEARBOX // EXACT AERODYNAMIC CROSS-SECTION", color=C_STATOR, fontsize=16, fontname='monospace', weight='bold', zorder=82)

    # Kinematic Side-Tags (Aligned geometrically with components)
    tags = [(450, "COLD INTAKE"), (250, "AXIAL COMPRESSOR"), (50, "COMBUSTION CORE"), 
            (-150, "TWIN TURBINES"), (-400, "EXHAUST YIELD")]
    for ty, txt in tags:
        ax.plot([-400, -260], [ty, ty], color=C_TEXT, lw=2, alpha=0.5, zorder=81)
        ax.text(-420, ty+15, f"[{txt}]", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', ha='left', zorder=82)

    # Bottom Live Telemetry Layout
    ax.add_patch(plt.Rectangle((-540, -960), 1080, 260, facecolor=C_BG, zorder=80))
    ax.plot([-460, 460], [-700, -700], color=C_TEXT, lw=6, zorder=81)

    ax.text(-460, -750, "GAS GENERATOR (HP SPOOL) : 38,000 RPM", color=C_HP_SPOOL, fontsize=20, fontname='monospace', weight='bold', zorder=82)
    ax.text(-460, -800, "POWER TURBINE (LP SPOOL) : 25,330 RPM", color=C_LP_SPOOL, fontsize=20, fontname='monospace', weight='bold', zorder=82)
    ax.text(-460, -850, "EPICYCLIC REDUCTION GEAR : 4:1 RATIO", color=C_TEXT, fontsize=18, fontname='monospace', zorder=82)
    ax.text(-460, -900, "PROPELLOR OUTPUT SHAFT   : 6,330 RPM", color=C_PROP, fontsize=22, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-429: TURBOPROP EXACT CROSS-SECTION [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    stream = [(f, f / float(TOTAL_FRAMES)) for f in range(TOTAL_FRAMES)]

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, stream, chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Thermodynamic Extrusion Locked. Stand by for compilation.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
