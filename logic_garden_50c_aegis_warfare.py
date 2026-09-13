"""
PROJECT: Logic Garden 50b (The AEGIS Phased Array Warfare Tensor)
FORMAT: YouTube Shorts (1080x1920)
METADATA: AEGIS, PHASED ARRAY, VLS, NAVAL WARFARE, KINEMATICS, DAYLIGHT PROTOCOL
EXECUTION: 24.0s Sequence. True Physical 3D Substrate.
RULES ENFORCED:
- Daylight Palette (White Substrate / High-Contrast Steel & Magenta).
- Exact Realisational Aspect: True 3D turnover kinematics and multi-target tracking.
- Zero Jargon: Industrial terminology for mathematical threat saturation.
- Australian spelling conventions enforced natively (Maths, Colour, Optimise).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle
from matplotlib.collections import LineCollection
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 24.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_50b_aegis_warfare"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST PHOTOREALISTIC PALETTE --------
C_BG        = '#FFFFFF'       # Daylight Protocol 
C_TEXT      = '#111115'       # Indestructible Black UI
C_STEEL     = '#94A3B8'       # Machined VLS Deck
C_CELL      = '#1E293B'       # Carbon Slate (VLS Hatches)
C_THREAT    = '#DE008A'       # Deep Magenta (Hostile Vectors)
C_BIRD      = '#005599'       # Deep Marine (Interceptors)
C_FIRE      = '#FF3300'       # Intense Red (Launch Exhaust / Spallation)
C_RADAR     = '#FFB300'       # Dense Amber (Phased Array Beam)
C_TUNGSTEN  = '#111115'       # Kinetic Shrapnel

# ------------------------------------------------------------------
# O(1) 3D PERSPECTIVE ENGINE
# ------------------------------------------------------------------
def project_3d_to_camera(x, y, z):
    """
    Absolute Euclidean camera projection. 
    Locked slightly elevated behind the VLS matrix, looking into the sky horizon.
    """
    # Camera fixed geometry
    cx, cy, cz = 0.0, 1500.0, -4000.0
    pitch = np.radians(-15.0) 
    
    # Translate to camera origin
    dx, dy, dz = x - cx, y - cy, z - cz

    # Apply pitch (Rotate around X axis)
    dy_rot = dy * np.cos(pitch) - dz * np.sin(pitch)
    dz_rot = dy * np.sin(pitch) + dz * np.cos(pitch)

    # Perspective division
    focal_length = 2000.0
    z_safe = np.maximum(dz_rot, 1.0)
    
    proj_x = focal_length * (dx / z_safe)
    proj_y = focal_length * (dy_rot / z_safe) + 300.0 # Center offset for 9:16
    proj_scale = focal_length / z_safe
    
    return proj_x, proj_y, proj_scale, z_safe

# ------------------------------------------------------------------
# SYSTEMIC TOPOLOGY SETUP
# ------------------------------------------------------------------
np.random.seed(50)
N_THREATS = 16

# 1. VLS Matrix Geometry (4x4 Grid)
vls_cells = []
cell_spacing = 80.0
sz = 1.5 * cell_spacing
for i in range(4):
    for j in range(4):
        cx = (i - 1.5) * cell_spacing
        cz = (j - 1.5) * cell_spacing
        vls_cells.append([cx, 0.0, cz])

# 2. Hostile Vectors (Spawn miles away at high altitude)
threat_start_z = 25000.0
threat_start_y = 6000.0
t_x = np.random.uniform(-4000, 4000, N_THREATS)
t_y = np.random.uniform(threat_start_y - 1000, threat_start_y + 1000, N_THREATS)
t_z = np.random.uniform(threat_start_z - 3000, threat_start_z + 3000, N_THREATS)

v_t_z = -1200.0 # High supersonic approach
v_t_y = -200.0
v_t_x = -t_x / (t_z / abs(v_t_z)) # Converge strictly on origin

# 3. Interceptor Pre-Allocation
i_x = np.zeros(N_THREATS)
i_y = np.zeros(N_THREATS)
i_z = np.zeros(N_THREATS)
i_vx = np.zeros(N_THREATS)
i_vy = np.zeros(N_THREATS)
i_vz = np.zeros(N_THREATS)
i_phase = np.zeros(N_THREATS, dtype=int)
i_launch_t = 4.0 + (np.arange(N_THREATS) * 0.4) # Ripple fire every 0.4s

for n in range(N_THREATS):
    cell = vls_cells[n]
    i_x[n], i_y[n], i_z[n] = cell[0], cell[1], cell[2]

active_threat = np.ones(N_THREATS, dtype=bool)

# Trail arrays for continuous cinematic tracking
history_i = [[] for _ in range(N_THREATS)]
history_t = [[] for _ in range(N_THREATS)]

# ------------------------------------------------------------------
# MULTICORE RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, th_x, th_y, th_z, th_act, in_x, in_y, in_z, in_v, in_ph, hist_i, hist_t, radar_locks = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    
    # 9:16 Fixed bounds (Projected canvas)
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)

    # ---------------------------------------------------------
    # 1. RENDER VLS GRID (Deck Level)
    # ---------------------------------------------------------
    poly_list = []
    poly_col = []
    
    # Baseplate deck steel
    db_x = [-1000, 1000, 1000, -1000]
    db_z = [-500, -500, 500, 500]
    bx, by, _, _ = project_3d_to_camera(np.array(db_x), np.zeros(4), np.array(db_z))
    ax.add_patch(Polygon(np.column_stack((bx, by)), facecolor=C_BG, edgecolor=C_STEEL, lw=2, zorder=1))

    # Cells
    for n, c in enumerate(vls_cells):
        cw = cell_spacing * 0.4
        cx, cz = c[0], c[2]
        pts_x = np.array([cx-cw, cx+cw, cx+cw, cx-cw])
        pts_z = np.array([cz-cw, cz-cw, cz+cw, cz+cw])
        vx, vy, _, _ = project_3d_to_camera(pts_x, np.zeros(4), pts_z)
        
        # Color flash on launch
        col = C_CELL
        if in_ph[n] == 1: col = C_FIRE # Active launch fire
        elif in_ph[n] > 1: col = C_TEXT # Hollow / Spent cell
        
        ax.add_patch(Polygon(np.column_stack((vx, vy)), facecolor=col, edgecolor=C_STEEL, lw=2, zorder=2))

    # ---------------------------------------------------------
    # 2. PHASED ARRAY RADAR VECTORS
    # ---------------------------------------------------------
    if len(radar_locks) > 0:
        lx = []
        ly = []
        for lock in radar_locks:
            if f % 4 < 2: # Electronic strobe
                px, py, _, _ = project_3d_to_camera(np.array([0, lock[0]]), np.array([0, lock[1]]), np.array([0, lock[2]]))
                ax.plot(px, py, color=C_RADAR, lw=1.5, alpha=0.6, zorder=3)

    # ---------------------------------------------------------
    # 3. KINEMATICS (Hostiles & Interceptors) AND CONTRAILS
    # ---------------------------------------------------------
    # Process history for continuous LineCollection trails
    def draw_trails(hist_dict, color, baselw, fade_tail=True):
        for h in hist_dict:
            if len(h) < 2: continue
            hx, hy, hz = zip(*h)
            hx, hy, hz = np.array(hx), np.array(hy), np.array(hz)
            px, py, ps, pz_safe = project_3d_to_camera(hx, hy, hz)
            
            # Form line segments
            points = np.array([px, py]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            
            # Opacity fades towards the tail
            alphas = np.linspace(0.0, 0.8, len(segments)) if fade_tail else np.full(len(segments), 0.8)
            lws = ps[:-1] * baselw
            
            lc = LineCollection(segments, colors=color, linewidths=lws, alpha=alphas, zorder=4)
            ax.add_collection(lc)

    draw_trails(hist_t, C_THREAT, 0.15)
    draw_trails(hist_i, C_BIRD, 0.20)

    # Current Hostile Nodes
    act_t = th_act > 0
    if np.any(act_t):
        px, py, ps, pz = project_3d_to_camera(th_x[act_t], th_y[act_t], th_z[act_t])
        ax.scatter(px, py, s=ps*30.0, color=C_THREAT, edgecolors=C_TEXT, lw=0.5, zorder=6)
        
    # Current Interceptors Nodes
    act_i = in_ph > 0
    in_flight = act_i & (in_ph < 4)
    if np.any(in_flight):
        px, py, ps, pz = project_3d_to_camera(in_x[in_flight], in_y[in_flight], in_z[in_flight])
        ax.scatter(px, py, s=ps*40.0, color=C_BIRD, edgecolors=C_BG, lw=1.0, zorder=7)

    # Spallation Rings (Detonation)
    for n, phase in enumerate(in_ph):
        if phase == 4:
            # Blast marks where target was hit
            bx, by, bs, _ = project_3d_to_camera(np.array([th_x[n]]), np.array([th_y[n]]), np.array([th_z[n]]))
            ax.scatter(bx, by, s=bs*800.0, color=C_FIRE, edgecolors='none', alpha=0.5, zorder=5)
            ax.scatter(bx, by, s=bs*300.0, color=C_TUNGSTEN, edgecolors='none', alpha=0.8, zorder=5)

    # ---------------------------------------------------------
    # 4. INDUSTRIAL HUD & TELEMETRY
    # ---------------------------------------------------------
    ax.add_patch(Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, facecolor=C_BG, edgecolor=C_TEXT, lw=2, zorder=80))
    ax.text(0.04, 0.965, "LG-50b :: THE AEGIS MULTI-TARGET SATURATION TENSOR", transform=ax.transAxes, color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=81)

    ax.add_patch(Rectangle((0, 0), 1.0, 0.18, transform=ax.transAxes, facecolor=C_BG, edgecolor=C_TEXT, lw=2, zorder=80))
    
    state_col = C_RADAR if t_sec < 4.0 else C_FIRE if t_sec < 14.0 else C_BIRD
    if t_sec > 22.0: state_col = C_TEXT
    
    ax.text(0.04, 0.14, f"SYSTEM STATE: {state_str}", transform=ax.transAxes, color=state_col, fontsize=16, fontname='monospace', weight='bold', zorder=81)
    
    act_threats = np.sum(th_act)
    ax.text(0.04, 0.09, f"HOSTILE VECTORS INBOUND: {act_threats:02d} // RADAR LOCK ABSOLUTE", transform=ax.transAxes, color=C_THREAT if act_threats > 0 else C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=81)

    # Engagement Progress Bar
    ax.plot([0.04, 0.96], [0.04, 0.04], transform=ax.transAxes, color=C_STEEL, lw=6, zorder=81)
    prog = min(1.0, t_sec / 20.0)
    ax.plot([0.04, 0.04 + (0.92 * prog)], [0.04, 0.04], transform=ax.transAxes, color=state_col, lw=6, zorder=82)
    
    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) FLIGHT KINEMATICS STREAM
# ------------------------------------------------------------------
def generate_stream():
    th_x, th_y, th_z = np.copy(t_x), np.copy(t_y), np.copy(t_z)
    th_act = np.copy(active_threat)
    
    in_x, in_y, in_z = np.copy(i_x), np.copy(i_y), np.copy(i_z)
    in_vx, in_vy, in_vz = np.copy(i_vx), np.copy(i_vy), np.copy(i_vz)
    in_ph = np.copy(i_phase)
    
    hist_i = [[] for _ in range(N_THREATS)]
    hist_t = [[] for _ in range(N_THREATS)]
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        dt = 0.016
        radar_locks = []
        
        state = "PHASE 1: SEARCH & TRACK [TARGET ACQUISITION]"
        
        if t_sec >= 4.0 and t_sec < 18.0:
            state = "PHASE 2: RIPPLE FIRE // TURNOVER KINEMATICS"
        elif t_sec >= 18.0 and np.any(th_act):
            state = "PHASE 3: KINEMATIC INTERSECTION // SPALLATION"
        elif not np.any(th_act):
            state = "PHASE 4: RESOLUTION 100% // ALL VECTORS NEUTRALISED"

        # Update Threats
        for n in range(N_THREATS):
            if th_act[n]:
                th_x[n] += v_t_x[n] * dt
                th_y[n] += v_t_y * dt
                th_z[n] += v_t_z * dt
                
                # Illuminate active threats
                if t_sec > 1.0: 
                    radar_locks.append([th_x[n], th_y[n], th_z[n]])
                    
                # Store history
                hist_t[n].append([th_x[n], th_y[n], th_z[n]])
                if len(hist_t[n]) > 40: hist_t[n].pop(0)

        # Update Interceptors
        for n in range(N_THREATS):
            if t_sec > i_launch_t[n] and in_ph[n] == 0:
                in_ph[n] = 1 # Launch
                in_vy[n] = 400.0 # High G vertical shove
                
            if in_ph[n] > 0 and in_ph[n] < 4:
                # Phase 1: Vertical clear
                if in_ph[n] == 1:
                    in_vy[n] += 800.0 * dt # Solid rocket booster acceleration
                    if in_y[n] > 500.0:
                        in_ph[n] = 2 # Initiate Turnover
                
                # Phase 2: Pitch/Turnover to direct intercept
                elif in_ph[n] == 2:
                    dx = th_x[n] - in_x[n]
                    dy = th_y[n] - in_y[n]
                    dz = th_z[n] - in_z[n]
                    dist = np.linalg.norm([dx, dy, dz])
                    
                    # Proportional turn
                    speed = np.linalg.norm([in_vx[n], in_vy[n], in_vz[n]]) + (400.0 * dt)
                    speed = min(speed, 2500.0) # Terminal velocity Mach 3+
                    
                    # Exact geometric thrust vectoring
                    in_vx[n] = (dx / dist) * speed
                    in_vy[n] = (dy / dist) * speed
                    in_vz[n] = (dz / dist) * speed
                    
                    # Proximity Fuse Check
                    if dist < 400.0:
                        in_ph[n] = 4 # Detonate
                        th_act[n] = False # Erase threat
                        
                in_x[n] += in_vx[n] * dt
                in_y[n] += in_vy[n] * dt
                in_z[n] += in_vz[n] * dt
                
                # Store history for beautiful arching contrails
                hist_i[n].append([in_x[n], in_y[n], in_z[n]])
                # Contrail duration
                if len(hist_i[n]) > 100: hist_i[n].pop(0)
                        
        yield (f, t_sec, state, np.copy(th_x), np.copy(th_y), np.copy(th_z), np.copy(th_act), 
               np.copy(in_x), np.copy(in_y), np.copy(in_z), np.copy(in_vx), np.copy(in_ph), 
               [list(h) for h in hist_i], [list(h) for h in hist_t], radar_locks)

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-050b: THE AEGIS MULTI-TARGET SATURATION TENSOR [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Compression Duration: {DURATION}s | Hostiles: {N_THREATS}")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Matrix Resolved: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
