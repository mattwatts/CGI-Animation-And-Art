"""
PROJECT: Logic Garden 21b (Exact Physical Construct // V2 Ballistics)
FORMAT: YouTube Shorts (1080x1920)
METADATA: V2 ROCKET, BALLISTICS, INERTIA, DAYLIGHT
EXECUTION: 24.0s Sequence. True 3D Beveled Geometry. 
RULES ENFORCED: 
- Exact V2 (Aggregat 4) geometric scaling and optical tracking checks.
- Dynamic Camera Lock (9:16) rendering speed via background grid sliding.
- Ghost Vector Separation (Inertia vs Gravity shear).
- Daylight Palette (White Substrate / High-Contrast Solid Geometry).
- Purged Jargon. Australian spelling conventions.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import multiprocessing as mp
import os
import gc

# ======== SEQUENCE PARAMETERS ========
DURATION = 24.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_21b_v2_rocket"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'          # Indestructible Black UI
C_STEEL     = '#94A3B8'          # Passive Cartesian Grid
C_WHITE     = '#F8FAFC'          # Rocket White Geometry
C_BLACK     = '#0F172A'          # Rocket Black Geometry
C_INERTIA   = '#005599'          # Deep Marine (Straight Ghost Line)
C_GRAVITY   = '#FF3300'          # Intense Red (The True Parabola)
C_FLAME     = '#FFB300'          # Dense Amber (Thrust Plume)

# ------------------------------------------------------------------
# RIGID FLIGHT PHYSICS PRE-PROCESSOR (O(1) Data Lock)
# ------------------------------------------------------------------
def calculate_flight_path():
    dt = 1.0 / FPS
    T_BURN = 6.0
    gravity = 9.81
    thrust_accel = 22.5 # Tuned so total flight time lands exactly at ~23.5s

    state = {'x': 0.0, 'y': 0.0, 'vx': 0.0, 'vy': 0.0, 'angle': 90.0}
    
    history = []
    ghost_data = {'locked': False, 'origin_x': 0, 'origin_y': 0, 'vx': 0, 'vy': 0, 't_cutoff': 0}

    for f in range(TOTAL_FRAMES):
        t = f * dt
        
        # Phase 1: Powered Ascent & Gravity Turn
        if t <= T_BURN:
            if t > 1.0:
                pitch_deg = 90.0 - ((t - 1.0) / 5.0) * 45.0 # Tilts to 45 degrees
            else:
                pitch_deg = 90.0
                
            state['angle'] = pitch_deg    
            theta = np.radians(pitch_deg)
            ax = thrust_accel * np.cos(theta)
            ay = thrust_accel * np.sin(theta) - gravity
            
            ghost_data['vx'] = state['vx']
            ghost_data['vy'] = state['vy']
            ghost_data['origin_x'] = state['x']
            ghost_data['origin_y'] = state['y']
            ghost_data['t_cutoff'] = t
            
        # Phase 2: Ballistic Flight (Engine Cutoff)
        else:
            ghost_data['locked'] = True
            ax = 0.0
            ay = -gravity
            
            # Aerodynamic Stability (Rocket points into velocity vector)
            if (state['x'] > 0 or state['y'] > 0): # Avoid div 0 at pad
                state['angle'] = np.degrees(np.arctan2(state['vy'], state['vx']))
                
        # Euler Integration
        state['vx'] += ax * dt
        state['vy'] += ay * dt
        state['x']  += state['vx'] * dt
        state['y']  += state['vy'] * dt
        
        # Terminal Impact Lock (Floor = 0)
        if state['y'] <= 0.0 and t > 10.0:
            state['y'] = 0.0
            state['vx'] = 0.0
            state['vy'] = 0.0
            state['angle'] = min(max(state['angle'], -90), 0) # Crash crumple angle
            
        # Append clone to history
        state_copy = state.copy()
        state_copy['t'] = t
        state_copy['phase'] = "POWERED ASCENT" if t <= T_BURN else ("TERMINAL IMPACT" if state['y'] == 0 else "BALLISTIC COAST")
        state_copy['ghost_x'] = ghost_data['origin_x'] + ghost_data['vx'] * (t - ghost_data['t_cutoff']) if ghost_data['locked'] else state['x']
        state_copy['ghost_y'] = ghost_data['origin_y'] + ghost_data['vy'] * (t - ghost_data['t_cutoff']) if ghost_data['locked'] else state['y']
        
        history.append(state_copy)
        
    return history

flight_data = calculate_flight_path()

# ------------------------------------------------------------------
# GEOMETRY ENGINE (Exact Coordinate Transformation)
# ------------------------------------------------------------------
def rotate_and_translate(pts, x, y, angle_deg):
    angle_rad = np.radians(angle_deg - 90.0) # -90 because our base points +Y
    R = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad)],
        [np.sin(angle_rad),  np.cos(angle_rad)]
    ])
    return np.dot(pts, R.T) + [x, y]

# Constructing exact V2 Polygons (Scale: 1 unit = 1 Metre)
# Y=0 is base, Y=14 is nose tip. X=0 is centerline. Max width ~ 1.6m.
geo_bw_l  = [[0, 2], [-0.8, 2], [-0.8, 7], [0, 7]]
geo_bw_r  = [[0, 2], [0.8, 2], [0.8, 7], [0, 7]]
geo_tw_l  = [[0, 7], [-0.8, 7], [-0.8, 10], [0, 10]]
geo_tw_r  = [[0, 7], [0.8, 7], [0.8, 10], [0, 10]]
geo_nw_l  = [[0, 10], [-0.8, 10], [-0.6, 11.5], [-0.3, 13], [0, 14]]
geo_nw_r  = [[0, 10], [0.8, 10], [0.6, 11.5], [0.3, 13], [0, 14]]
geo_fin_l = [[-0.8, 5], [-1.8, 1], [-1.8, -0.5], [-0.8, -0.5]]
geo_fin_r = [[0.8, 5], [1.8, 1], [1.8, -0.5], [0.8, -0.5]]

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    dat = flight_data[f]
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # 1. DYNAMIC CAMERA LOCK 
    # Viewport locked precisely to 9:16 aspect ratio (Width: 72m, Height: 128m)
    c_x = dat['x']
    c_y = max(dat['y'], 40.0) # Prevent panning below bedrock
    
    x_min, x_max = c_x - 36, c_x + 36
    y_min, y_max = c_y - 42, c_y + 86 # Offset to keep rocket lower-mid frame
    
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    # 2. BACKGROUND ARCHITECTURE
    # Bedrock Ground Line (Y < 0 is indestructible black)
    ax.add_patch(patches.Rectangle((x_min - 100, -500), 2000, 500, facecolor=C_TEXT, zorder=1))
    
    # Active Cartesian Coordinate Grid (Anchored to world space, pans through camera)
    grid_bound_x_min = int(np.floor(x_min / 10.0)) * 10
    grid_bound_x_max = int(np.ceil(x_max / 10.0)) * 10
    grid_bound_y_min = int(np.floor(max(0, y_min) / 10.0)) * 10
    grid_bound_y_max = int(np.ceil(y_max / 10.0)) * 10
    
    for gx in range(grid_bound_x_min, grid_bound_x_max + 10, 10):
        ax.plot([gx, gx], [0, y_max + 100], color=C_STEEL, lw=1.0, alpha=0.3, zorder=2)
    for gy in range(grid_bound_y_min, grid_bound_y_max + 10, 10):
        ax.plot([x_min - 100, x_max + 100], [gy, gy], color=C_STEEL, lw=1.0, alpha=0.3, zorder=2)

    # 3. KINEMATIC TRAJECTORY RENDER
    # Solid Gravity Curve & Dotted Inertia Line
    if f > 0:
        hist_xs = [d['x'] for d in flight_data[:f]]
        hist_ys = [d['y'] for d in flight_data[:f]]
        ax.plot(hist_xs, hist_ys, color=C_GRAVITY, lw=5, zorder=8)
        
        if dat['ghost_x'] != dat['x']: # Engine is cutoff, Ghost is active
            ghost_xs = [d['ghost_x'] for d in flight_data[:f+1] if d['ghost_x'] != d['x']]
            ghost_ys = [d['ghost_y'] for d in flight_data[:f+1] if d['ghost_y'] != d['y']]
            ax.plot(ghost_xs, ghost_ys, color=C_INERTIA, lw=4, linestyle='dashed', zorder=7)

    # 4. DRAW V2 HARDWARE MATRICES
    angle = dat['angle']
    x_pos = dat['x']
    y_pos = dat['y']
    
    polys = [
        (geo_bw_l, C_WHITE), (geo_bw_r, C_BLACK),
        (geo_tw_l, C_BLACK), (geo_tw_r, C_WHITE),
        (geo_nw_l, C_WHITE), (geo_nw_r, C_BLACK),
        (geo_fin_l, C_BLACK), (geo_fin_r, C_WHITE)
    ]
    
    for (pts, col) in polys:
        trans_pts = rotate_and_translate(np.array(pts), x_pos, y_pos, angle)
        ax.add_patch(patches.Polygon(trans_pts, facecolor=col, edgecolor=C_TEXT, lw=2.0, zorder=10, joinstyle='miter'))

    # Flame Emission Matrix (Only during Phase 1)
    if dat['phase'] == "POWERED ASCENT":
        # Procedural Mach-Diamonds based on Engine Pressure
        flame_len = 8.0 + np.sin(f * 1.5) * 2.0
        geo_flame = [[-0.6, 0.5], [-0.3, -flame_len*0.6], [0.0, -flame_len], [0.3, -flame_len*0.6], [0.6, 0.5]]
        
        t_flame = rotate_and_translate(np.array(geo_flame), x_pos, y_pos, angle)
        ax.add_patch(patches.Polygon(t_flame, facecolor=C_GRAVITY, edgecolor='none', alpha=0.9, zorder=9))
        
        # Inner Core
        geo_core = [[-0.3, 0.5], [0.0, -flame_len*0.6], [0.3, 0.5]]
        t_core = rotate_and_translate(np.array(geo_core), x_pos, y_pos, angle)
        ax.add_patch(patches.Polygon(t_core, facecolor=C_FLAME, edgecolor='none', alpha=0.9, zorder=10))

    # Impact Crater Flash
    if dat['phase'] == "TERMINAL IMPACT" and dat['t'] < 23.8:
        flash_rad = (23.8 - dat['t']) * 50.0  # Expands and fades rapidly
        ax.add_patch(patches.Circle((x_pos, 0), flash_rad, facecolor=C_GRAVITY, alpha=0.8, zorder=20))
        ax.add_patch(patches.Circle((x_pos, 0), flash_rad*0.5, facecolor=C_FLAME, zorder=21))

    # 5. JARGON-FREE DAYLIGHT TELEMETRY
    # Top Panel
    ax.add_patch(plt.Rectangle((0, 0.88), 1, 0.12, transform=ax.transAxes, color=C_BG, zorder=50))
    ax.plot([0, 1], [0.88, 0.88], transform=ax.transAxes, color=C_TEXT, lw=4, zorder=51)
    
    ax.text(0.04, 0.955, "LG-21b :: V2 ROCKET KINEMATICS", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=52)
    ax.text(0.04, 0.915, "THE GREAT CURVE // GRAVITY VS INERTIA", transform=ax.transAxes, color=C_GRAVITY, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=52)

    # Left Telemetry Block
    ax.add_patch(plt.Rectangle((0, 0.70), 0.75, 0.18, transform=ax.transAxes, color=C_BG, zorder=50))
    
    alt_col = C_TEXT if dat['y'] > 0 else C_GRAVITY
    vel = np.sqrt(dat['vx']**2 + dat['vy']**2)
    
    ax.text(0.04, 0.84, f"FLIGHT PHASE : {dat['phase']}", transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace', weight='bold', zorder=52)
    ax.text(0.04, 0.80, f"VELOCITY     : {vel:05.1f} METRES/SEC", transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace', zorder=52)
    ax.text(0.04, 0.76, f"ALTITUDE (Y) : {dat['y']:06.1f} METRES", transform=ax.transAxes, color=alt_col, fontsize=18, fontname='monospace', weight='bold', zorder=52)
    ax.text(0.04, 0.72, f"DISTANCE (X) : {dat['x']:06.1f} METRES", transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace', zorder=52)

    # Bottom Legend Block
    ax.add_patch(plt.Rectangle((0, 0), 1, 0.10, transform=ax.transAxes, color=C_BG, zorder=50))
    ax.plot([0, 1], [0.10, 0.10], transform=ax.transAxes, color=C_TEXT, lw=4, zorder=51)
    
    ax.text(0.04, 0.07, "--- INERTIA (BLUE LINE)   : WHERE IGNORING GRAVITY GOES", transform=ax.transAxes, color=C_INERTIA, fontsize=15, fontname='monospace', weight='bold', zorder=52)
    ax.text(0.04, 0.03, "--- PARABOLA (RED LINE)   : WHERE PHYSICAL GRAVITY DRAGS IT", transform=ax.transAxes, color=C_GRAVITY, fontsize=15, fontname='monospace', weight='bold', zorder=52)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); plt.close('all'); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-21b: V2 ROCKET BALLISTICS (DAYLIGHT) [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, range(TOTAL_FRAMES), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Kinematics Locked. Stand by for compilation.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
