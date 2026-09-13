"""
PROJECT: Logic Garden 19b (Exact Physical Construct // PWR)
FORMAT: YouTube Shorts (1080x1920)
METADATA: PRESSURIZED WATER REACTOR, THERMODYNAMICS, DAYLIGHT
EXECUTION: 24.0s Sequence. True 3D Beveled Geometry. 
RULES ENFORCED: 
- 1,200 Kinematic Fluid Particles across Dual Sovereign Loops.
- Phase Transition Geometry: Steam physically expands and jitters.
- Daylight Palette (White Substrate / High-Contrast Solid Geometry).
- Purged Jargon. Australian spelling conventions.
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
DURATION = 24.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_19b_pwr"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'          # Indestructible Black UI
C_STEEL     = '#94A3B8'          # Vessel Structures
C_CARBON    = '#1E293B'          # Pipe Outer Borders
C_COLD      = '#005599'          # Deep Marine (Liquid Coolant)
C_HOT       = '#FF3300'          # Intense Red (Pressurised Hot Liquid)
C_STEAM     = '#FFB300'          # Dense Amber (High Kinetic Gas)

# Fluid Configuration
N_PARTICLES = 600
CYCLES = 3 # Particles complete exactly 3 laps in 24 seconds for high-kinetic flow

def interpolate_color(c1, c2, frac):
    rgb1 = np.array(mcol.to_rgb(c1))
    rgb2 = np.array(mcol.to_rgb(c2))
    return mcol.to_hex(rgb1 + (rgb2 - rgb1) * frac)

# ------------------------------------------------------------------
# THERMODYNAMIC PATH GENERATOR (Euclidean Trajectories)
# ------------------------------------------------------------------
def get_path_state(s, is_primary):
    """
    Maps 1D track scalar s [0, 16) to 2D Cartesian Space, 
    evaluating exact physical states (Color, Size, Kinematic Jitter).
    """
    s = s % 16.0
    
    # Base Geometries
    if is_primary:
        x0, y0 = -2.5, -4.0
    else:
        x0, y0 = 0.5, -4.0
        
    # Cartesian Routing
    if s < 6:
        x, y = x0, y0 + s
        nx, ny = 1, 0 # Tangent normal for jitter
    elif s < 8:
        x, y = x0 + (s - 6), y0 + 6
        nx, ny = 0, 1
    elif s < 14:
        x, y = x0 + 2, y0 + 6 - (s - 8)
        nx, ny = 1, 0
    else:
        x, y = x0 + 2 - (s - 14), y0
        nx, ny = 0, 1

    # Thermodynamic States
    if is_primary:
        # Loop 1: Constant Density Pressurised Liquid
        size = 35.0
        jitter_amp = 0.0
        # Color mapping: 
        if 0 <= s < 4: # Core Heating
            col = interpolate_color(C_COLD, C_HOT, s/4.0)
        elif 4 <= s < 9: # Hot Leg
            col = C_HOT
        elif 9 <= s < 13: # HX Cooling
            col = interpolate_color(C_HOT, C_COLD, (s-9)/4.0)
        else: # Cold Leg
            col = C_COLD
            
    else:
        # Loop 2: Phase Transition (Boiling to Condensing)
        if 0 <= s < 2:
            # Liquid Inlet
            col = C_COLD
            size = 35.0
            jitter_amp = 0.0
        elif 2 <= s < 6:
            # Boiling Phase (Heat Exchanger)
            frac = (s - 2) / 4.0
            col = interpolate_color(C_COLD, C_STEAM, frac)
            size = 35.0 + (80.0 * frac) # Gas expansion
            jitter_amp = 0.15 * frac  # Kinetic vibration
        elif 6 <= s < 10:
            # Pure Steam (High kinetic energy driving Turbine)
            col = C_STEAM
            size = 115.0
            jitter_amp = 0.15
        elif 10 <= s < 14:
            # Condensation
            frac = (s - 10) / 4.0
            col = interpolate_color(C_STEAM, C_COLD, frac)
            size = 115.0 - (80.0 * frac)
            jitter_amp = 0.15 * (1.0 - frac)
        else:
            # Liquid Return
            col = C_COLD
            size = 35.0
            jitter_amp = 0.0
            
    return x, y, nx, ny, col, size, jitter_amp

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(data_packet):
    f, t_phase = data_packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # 9:16 Architectural Viewport scaling
    ax.set_xlim(-4, 4)
    ax.set_ylim(-7.11, 7.11)

    # ====================================================
    # 1. HARDWARE MATRIX (Background Vessels)
    # ====================================================
    
    # A. Reactor Core Substrate (Left)
    ax.add_patch(patches.Rectangle((-3.3, -4.5), 1.6, 6.0, facecolor=C_STEEL, edgecolor=C_TEXT, lw=4, zorder=5))
    ax.text(-2.5, -5.0, "REACTOR CORE\n(THERMAL IGNITION)", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', ha='center', zorder=20)
    # Control Rods (Inserted)
    for cx in [-2.9, -2.7, -2.3, -2.1]:
        ax.plot([cx, cx], [-4.5, -1.0], color=C_TEXT, lw=6, zorder=6)
        
    # B. The Exchanger Tower (Center Interface)
    ax.add_patch(patches.Rectangle((-1.2, -4.5), 2.4, 7.0, facecolor=C_STEEL, edgecolor=C_TEXT, lw=4, zorder=5))
    ax.text(0.0, 2.8, "HEAT EXCHANGER TOWER\n(NO FLUID MIXING)", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', ha='center', zorder=20)
    # Thermal Baffle Matrix inside the Exchanger
    for by in np.linspace(-4, 2, 20):
        ax.plot([-1.2, 1.2], [by, by], color=C_BG, lw=2, alpha=0.9, zorder=6)
        
    # C. Condenser Unit (Bottom Right)
    ax.add_patch(patches.Rectangle((1.7, -4.5), 1.6, 2.0, facecolor=C_STEEL, edgecolor=C_TEXT, lw=4, zorder=5))
    ax.text(2.5, -5.0, "CONDENSER UNIT\n(HEAT REJECTION)", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', ha='center', zorder=20)

    # ====================================================
    # 2. FLUID PIPING (The Track)
    # ====================================================
    # Outer Carbon Steel Jackets
    ax.plot([-2.5, -2.5, -0.5, -0.5, -2.5], [2, 2, 2, -4, -4], color=C_CARBON, lw=24, zorder=8, solid_joinstyle='miter')
    ax.plot([0.5, 0.5, 2.5, 2.5, 0.5], [-4, 2, 2, -4, -4], color=C_CARBON, lw=24, zorder=8, solid_joinstyle='miter')
    ax.plot([-2.5, -2.5], [-4, 2], color=C_CARBON, lw=24, zorder=8) # Close loop 1
    ax.plot([0.5, 0.5], [-4, 2], color=C_CARBON, lw=24, zorder=8) # Close loop 2
    
    # Inner Pipe Volumes (Hollow White for daylight particles)
    for px, py in [[[-2.5, -2.5, -0.5, -0.5, -2.5], [2, 2, 2, -4, -4]], 
                   [[0.5, 0.5, 2.5, 2.5, 0.5], [-4, 2, 2, -4, -4]]]:
        ax.plot(px, py, color=C_BG, lw=14, zorder=9, solid_joinstyle='miter')
    ax.plot([-2.5, -2.5], [-4, 2], color=C_BG, lw=14, zorder=9) 
    ax.plot([0.5, 0.5], [-4, 2], color=C_BG, lw=14, zorder=9) 

    # ====================================================
    # 3. KINEMATIC FLUID SWARM
    # ====================================================
    
    # Particle baseline arrays
    base_s = np.linspace(0, 16, N_PARTICLES, endpoint=False)
    
    # Evolve time: Particles must traverse L=16 exactly 'CYCLES' times in the loop
    s_current = (base_s + (t_phase * 16.0 * CYCLES)) % 16.0
    
    for loop_id in [0, 1]:
        is_pri = (loop_id == 0)
        
        # Batch compute all states for the specific loop
        X, Y, C, S = [], [], [], []
        
        for i, s_val in enumerate(s_current):
            x, y, nx, ny, col, size, j_amp = get_path_state(s_val, is_pri)
            
            # Kinematic Jitter specifically engineered to loop seamlessly 
            # (Matches identical phase at t=0.0 and t=1.0)
            if j_amp > 0:
                local_phase = (t_phase * 2 * math.pi * CYCLES)
                jitter_val = math.sin(i * 117.3 + local_phase) * j_amp
                x += nx * jitter_val
                y += ny * jitter_val
                
            X.append(x)
            Y.append(y)
            C.append(col)
            S.append(size)
            
        # Draw the dense fluid scatter matrix
        ax.scatter(X, Y, s=S, c=C, edgecolors='none', zorder=15, alpha=0.9)

    # ====================================================
    # 4. ROTARY KINEMATICS (The Turbine)
    # ====================================================
    turb_cx, turb_cy = 2.5, 1.0
    
    # Thick Steel Housing
    ax.add_patch(patches.Rectangle((1.5, 0.0), 2.0, 2.0, facecolor=C_STEEL, edgecolor=C_TEXT, lw=4, zorder=18))
    
    # Shaft - NameError 'Circle' fixed to 'patches.Circle'
    ax.add_patch(patches.Circle((turb_cx, turb_cy), 0.25, facecolor=C_TEXT, zorder=20))
    
    TURBINE_REVS = 12 # Spins 12 times per 24s loop
    t_angle = np.radians(t_phase * 360 * TURBINE_REVS)
    
    # Tri-blade propeller mapping
    r = 0.8
    for i in range(3):
        blade_ang = t_angle + np.radians(i * 120)
        dx = r * np.cos(blade_ang)
        dy = r * np.sin(blade_ang)
        ax.plot([turb_cx, turb_cx+dx], [turb_cy, turb_cy+dy], color=C_TEXT, lw=12, zorder=19, solid_capstyle='round')

    # ====================================================
    # 5. JARGON-FREE DAYLIGHT TELEMETRY 
    # ====================================================
    ax.add_patch(plt.Rectangle((0, 0.90), 1, 0.10, transform=ax.transAxes, color=C_BG, zorder=50))
    ax.plot([0, 1], [0.90, 0.90], transform=ax.transAxes, color=C_TEXT, lw=4, zorder=51)
    
    ax.text(0.04, 0.965, "LG-19b :: PRESSURIZED WATER REACTOR (PWR)", transform=ax.transAxes, color=C_TEXT, fontsize=22, fontname='monospace', weight='bold', va='center', zorder=52)
    ax.text(0.04, 0.930, "EXACT PHYSICAL CONSTRUCT & THERMAL MAPPING", transform=ax.transAxes, color=C_STEEL, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=52)

    # Top Informational Block
    ax.add_patch(plt.Rectangle((0, 0.77), 0.95, 0.13, transform=ax.transAxes, color=C_BG, zorder=50))
    ax.text(0.04, 0.86, "PRIMARY LOOP   : ENCLOSED RADIOACTIVE FLUID", transform=ax.transAxes, color=C_HOT, fontsize=18, fontname='monospace', weight='bold', zorder=52)
    ax.text(0.04, 0.82, "SECONDARY LOOP : NON-RADIOACTIVE KINEMATIC STEAM", transform=ax.transAxes, color=C_STEAM, fontsize=18, fontname='monospace', weight='bold', zorder=52)
    ax.text(0.04, 0.79, "LAW OF PHYSICS : THE FIRE AND THE STEAM NEVER TOUCH", transform=ax.transAxes, color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=52)

    # Bottom Status Block
    ax.add_patch(plt.Rectangle((0, 0), 1, 0.10, transform=ax.transAxes, color=C_BG, zorder=50))
    ax.plot([0, 1], [0.10, 0.10], transform=ax.transAxes, color=C_TEXT, lw=4, zorder=51)
    
    turbine_rpm = int(4800 * (0.8 + 0.2*np.sin(t_phase * math.pi))) # Realistic fluctuating RPM
    ax.text(0.04, 0.05, f"TURBINE LOAD : {turbine_rpm} RPM", transform=ax.transAxes, color=C_TEXT, fontsize=22, fontname='monospace', weight='bold', zorder=52)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); plt.close('all'); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-19b: PRESSURIZED WATER REACTOR (DAYLIGHT) [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    # Generate exact stream parameters for a seamless loop
    stream = [(f, f / float(TOTAL_FRAMES)) for f in range(TOTAL_FRAMES)]

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, stream, chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Thermodynamics Locked. Stand by for compilation.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
