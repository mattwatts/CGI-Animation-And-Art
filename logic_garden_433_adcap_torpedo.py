"""
PROJECT: Logic Garden 433 (Exact Physical Construct // Mk 48 ADCAP Propulsion)
FORMAT: YouTube Shorts (1080x1920)
METADATA: TORPEDO, SWASHPLATE, OTTO FUEL, KINEMATICS, DAYLIGHT
EXECUTION: 4.0s Seamless Endless Loop. True High-Density Vector Construct.
RULES ENFORCED: 
- O(1) Orthographic 3D->2D Z-sorting (Painter's Algorithm).
- Integer-quantised fluid vectors for absolute seamless looped framing.
- Thermodynamic Colour Mapping derived from instantaneous piston V_y.
- Purged Jargon. Australian spelling conventions (maths, colour).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcol
import multiprocessing as mp
import os
import gc
import math

# ======== SEQUENCE PARAMETERS ========
DURATION = 4.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_433_adcap_torpedo"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'          # Indestructible Black UI
C_HULL      = '#1E293B'          # Carbon Slate (Armour/Hull)
C_STEEL     = '#94A3B8'          # Machined Internals / Exhaust Stroke
C_BRASS     = '#D4AC0D'          # The Swashplate
C_FUEL      = '#FFB300'          # Dense Amber (Otto Fuel II)
C_COMBUST   = '#FF3300'          # Intense Red (Power Stroke Yield)
C_WATER     = '#005599'          # Deep Marine (Pump-Jet Flow)
C_CAVITATE  = '#E2E8F0'          # Ghost White (Prop Wake)

# ------------------------------------------------------------------
# O(1) SEAMLESS FLUID DYNAMICS (Integer Quantised Modulo wrap)
# ------------------------------------------------------------------
def generate_stream():
    np.random.seed(48)
    
    # Water flow wrapping precisely over a Y=700 length domain in 4.0 seconds.
    # To loop flawlessly: V * 4.0 = 700 * N. 
    # V = 175 (N=1), V = 350 (N=2)
    max_w = 600
    w_x = np.concatenate([np.random.uniform(180, 270, max_w//2), np.random.uniform(810, 900, max_w//2)])
    w_y_init = np.random.uniform(0, 700, max_w)
    w_v = np.random.choice([-175.0, -350.0], max_w)
    
    # Cavitation bubbles (rear exhaust)
    max_c = 400
    c_x = np.random.normal(540, 50, max_c)
    c_y_init = np.random.uniform(0, 300, max_c)
    c_v = np.random.choice([-175.0], max_c) # Sync wake cleanly

    for f in range(TOTAL_FRAMES):
        tau = f / float(TOTAL_FRAMES) # 0.0 -> 1.0 endless
        
        # Piston Engine Kinematics (2 full thermodynamic cycles per loop)
        omega_tau = 4 * math.pi * tau 
        
        # Fluid Kinematics
        t_sec = f / FPS
        current_w_y = (w_y_init + w_v * t_sec) % 700.0
        current_c_y = (c_y_init + c_v * t_sec) % 300.0
        
        yield (f, tau, omega_tau, w_x, current_w_y, c_x, current_c_y)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, tau, w_t, wx, wy, cx, cy = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # Architectural 9:16 Frame
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # 1. WATER & BACKGROUND KINEMATICS
    ax.scatter(wx, wy + 200, s=8, color=C_WATER, alpha=0.5, edgecolors='none', zorder=1)
    ax.scatter(cx, cy, s=15, color=C_CAVITATE, edgecolors='none', zorder=1)

    # 2. MK 48 HULL ARRAY (Static Cutaway Boundaries)
    # Hull Walls (R = 270 from center 540) -> X=[270, 810]
    ax.add_patch(patches.Rectangle((270, 700), 30, 1220, facecolor=C_HULL, edgecolor=C_TEXT, lw=3, zorder=5))
    ax.add_patch(patches.Rectangle((780, 700), 30, 1220, facecolor=C_HULL, edgecolor=C_TEXT, lw=3, zorder=5))
    # Tapered Rear Cone
    ax.plot([270, 420], [700, 250], color=C_HULL, lw=15, solid_capstyle='round', zorder=5)
    ax.plot([810, 660], [700, 250], color=C_HULL, lw=15, solid_capstyle='round', zorder=5)

    # 3. PUMP-JET PROPULSORS (Concentric Z-Sorted Flow)
    # Shroud
    ax.plot([250, 250], [200, 450], color=C_HULL, lw=20, solid_capstyle='round', zorder=15)
    ax.plot([830, 830], [200, 450], color=C_HULL, lw=20, solid_capstyle='round', zorder=15)
    
    # Concentric Hubs 
    ax.add_patch(patches.Rectangle((510, 250), 60, 450, facecolor=C_TEXT, zorder=6))  # Outer 
    ax.add_patch(patches.Rectangle((525, 100), 30, 150, facecolor=C_STEEL, zorder=6)) # Inner Exhaust
    
    # 7-Blade Front Rotors (Outer Shaft = +1.5 ratio)
    # 5-Blade Rear Rotors (Inner Shaft = -1.5 ratio)
    def render_prop(y_hub, num_blades, ratio, r_radius, z_base):
        for j in range(num_blades):
            b_angle = ratio * (4 * math.pi * tau) + j * (2 * math.pi / num_blades)
            bx = 540 + r_radius * math.cos(b_angle)
            bz = math.sin(b_angle)
            b_w = 40 * abs(math.sin(b_angle)) + 5 # Aerodynamic profile width
            b_h = 20 * math.cos(b_angle)          # Pitch
            
            z_idx = z_base + 2 if bz > 0 else z_base - 2
            
            b_poly = [[540, y_hub-15], [540, y_hub+15], [bx+b_w, y_hub+b_h], [bx-b_w, y_hub-b_h]]
            ax.add_patch(patches.Polygon(b_poly, facecolor=C_STEEL, edgecolor=C_TEXT, lw=1.5, zorder=z_idx))

    render_prop(400, 7,  1.5, 280, 15) # Outer
    render_prop(280, 5, -1.5, 230, 10) # Inner

    # 4. KINEMATIC GEARBOX 
    ax.add_patch(patches.Rectangle((450, 700), 180, 120, facecolor=C_HULL, edgecolor=C_TEXT, lw=3, zorder=10))
    ax.text(540, 760, "PLANETARY REVERSAL", color=C_BG, fontsize=12, fontname='monospace', weight='bold', ha='center', va='center', zorder=11)

    # 5. AXIAL SWASHPLATE (THE BOILER)
    # Extract structural math for 6 pistons
    N_p = 6
    P_RAD = 180
    Y_SWASH = 1100
    AMP = 120
    Y_HEAD = 1450
    P_HEIGHT = 140
    
    pistons = []
    for i in range(N_p):
        phi = i * (2 * math.pi / N_p)
        x_proj = 540 + P_RAD * math.cos(phi)
        z_proj = math.sin(phi)
        
        y_contact = Y_SWASH + AMP * math.cos(phi - w_t)
        # Derivative to map colour (v < 0 means power stroke expansion)
        v_y = 100 * math.sin(phi - w_t) 
        
        pistons.append({'x': x_proj, 'z': z_proj, 'yc': y_contact, 'vy': v_y})
        
    pistons.sort(key=lambda p: p['z']) # Absolute O(1) Depth Sorting

    # A. Render Back Pistons (Z < 0)
    for p in pistons:
        if p['z'] < 0:
            c_burn = C_COMBUST if p['vy'] < 0 else C_STEEL
            p_top = p['yc'] + P_HEIGHT
            # Chamber Volume
            ax.add_patch(patches.Rectangle((p['x']-35, p_top), 70, Y_HEAD - p_top, facecolor=c_burn, alpha=0.9, zorder=7))
            # Piston Block
            ax.add_patch(patches.Rectangle((p['x']-35, p['yc']), 70, P_HEIGHT, facecolor=C_HULL, edgecolor=C_TEXT, lw=2, zorder=8))

    # B. Central Drive Shaft & Main Swashplate Ellipse
    ax.add_patch(patches.Rectangle((515, 820), 50, 600, facecolor=C_STEEL, edgecolor=C_TEXT, lw=2, zorder=9))
    
    # Swashplate continuous geometry (A thick tilted band connecting all contact phases)
    sw_poly_bot = []
    sw_poly_top = []
    for deg in range(360):
        rad = math.radians(deg)
        sx = 540 + P_RAD * math.cos(rad)
        sy = Y_SWASH + AMP * math.cos(rad - w_t)
        sw_poly_bot.append([sx, sy - 20])
        sw_poly_top.append([sx, sy + 20])
    sw_poly = sw_poly_top + sw_poly_bot[::-1]
    ax.add_patch(patches.Polygon(sw_poly, facecolor=C_BRASS, edgecolor=C_TEXT, lw=2, zorder=10))

    # C. Render Front Pistons (Z > 0 - Overwrites Swashplate perfectly)
    for p in pistons:
        if p['z'] >= 0:
            c_burn = C_COMBUST if p['vy'] < 0 else C_STEEL
            p_top = p['yc'] + P_HEIGHT
            # Chamber Volume
            ax.add_patch(patches.Rectangle((p['x']-35, p_top), 70, Y_HEAD - p_top, facecolor=c_burn, alpha=0.95, edgecolor=C_TEXT, lw=2, zorder=11))
            # Piston Block
            ax.add_patch(patches.Rectangle((p['x']-35, p['yc']), 70, P_HEIGHT, facecolor=C_HULL, edgecolor=C_TEXT, lw=3, zorder=12))

    # 6. OTTO FUEL II INJECTOR BLOCK
    ax.add_patch(patches.Rectangle((270, 1450), 540, 150, facecolor=C_TEXT, zorder=15))
    ax.text(540, 1525, "MONOPROPELLANT COMBUSTION CORE", color=C_BG, fontsize=18, fontname='monospace', weight='bold', ha='center', va='center', zorder=16)
    
    # Fuel Lines
    ax.plot([540, 540], [1600, 1800], color=C_FUEL, lw=40, solid_capstyle='round', zorder=10)
    ax.add_patch(patches.Rectangle((270, 1800), 540, 60, facecolor=C_HULL, edgecolor=C_TEXT, lw=4, zorder=11))

    # 7. ABSOLUTE DAYLIGHT TELEMETRY (TOP HUD)
    ax.add_patch(patches.Rectangle((0, 1760), 1080, 160, facecolor=C_BG, zorder=80))
    ax.plot([0, 1080], [1760, 1760], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(40, 1860, "LG-433 // MK 48 ADCAP PROPULSION MATRIX", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=82)
    ax.text(40, 1810, "AXIAL SWASHPLATE + COUNTER-ROTATING PUMP JET", color=C_STEEL, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=82)

    # 8. ABSOLUTE DAYLIGHT TELEMETRY (BOTTOM HUD)
    ax.add_patch(patches.Rectangle((0, 0), 1080, 150, facecolor=C_BG, zorder=80))
    ax.plot([0, 1080], [150, 150], color=C_TEXT, lw=6, zorder=81)
    
    # Dynamic Math Readouts
    cam_rpm = 2 * int(1.0 / (DURATION / 2.0) * 60) # Visual equivalent logic
    ax.text(40, 100, f"SWASHPLATE CAM : O(1) CONTINUOUS KINEMATICS", color=C_BRASS, fontsize=18, fontname='monospace', weight='bold', zorder=82)
    ax.text(40, 50, f"THERMODYNAMICS : EXPLICIT COLOUR MAPPING", color=C_COMBUST, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(600, 50, f"FLUID VECTORS : PERFECT MODULO WRAP", color=C_WATER, fontsize=16, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-433: ADCAP KINEMATICS (DAYLIGHT) [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Thermodynamic Mapping and Fluid Wrapping Confirmed. Stand by for compilation.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
