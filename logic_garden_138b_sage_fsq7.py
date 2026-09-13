"""
PROJECT: Logic Garden 138b (Exact Physical Construct // SAGE AN/FSQ-7 Daylight Vector)
FORMAT: YouTube Shorts (1080x1920)
METADATA: SAGE, AIR DEFENCE, KINEMATIC INTERCEPT, DAYLIGHT
EXECUTION: 24.0s Sequence. True 2D High-Density Construct.
RULES ENFORCED: 
- O(1) Proportional Navigation Intercept Math.
- Daylight Palette (White Substrate / High-Contrast Solid Geometry).
- Purged Phosphor Bloom (Replaced with Geometric Spallation).
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
OUT_DIR = "frames_138b_sage_fsq7"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'          # Indestructible Black UI
C_STEEL     = '#94A3B8'          # Passive Commercial Traffic
C_COAST     = '#E2E8F0'          # Ghost Coastline Grid
C_CRANE     = '#1E293B'          # Carbon Slate (Heavy Borders)
C_HOSTILE   = '#FF3300'          # Intense Red Threat Vector
C_INTERCEPT = '#005599'          # Deep Marine BOMARC Missile
C_TARGET    = '#FFB300'          # Dense Amber Selection/Light Gun
C_OK        = '#00C853'          # Jade Confirmations

# ------------------------------------------------------------------
# O(1) VECTOR GEOGRAPHY
# ------------------------------------------------------------------
def generate_vector_map():
    coastline = [
        (100, 1900), (350, 1600), (300, 1400), (450, 1200), (400, 1000),
        (650, 850), (450, 600), (500, 400), (600, 200), (550, -100)
    ]
    borders = [
        [(100, 1900), (0, 1900)], [(300, 1400), (0, 1400)],
        [(400, 1000), (0, 950)], [(500, 400), (200, 400)]
    ]
    return coastline, borders

# ------------------------------------------------------------------
# PARALLEL GENERATOR (LOGIC TENSORS)
# ------------------------------------------------------------------
def generate_stream():
    np.random.seed(1958)
    
    base_pos = np.array([540.0, 300.0])
    interceptor_speed = 15.0
    
    # Background Traffic Array
    friendlies = []
    for i in range(15):
        pos = np.array([np.random.uniform(50, 1000), np.random.uniform(200, 1800)])
        ang = np.random.uniform(0, 2*math.pi)
        vel = np.array([math.cos(ang), math.sin(ang)]) * np.random.uniform(1.5, 3.5)
        friendlies.append({
            'id': f"FLT-{np.random.randint(100,999)}", 'pos': pos, 'vel': vel, 'history': []
        })

    # Hostile Flight Plans (3 waves over 24 seconds)
    hostiles = [
        {'id': "TRK-01", 'pos': np.array([200.0, 1950.0]), 'aim': np.array([540.0, 300.0]), 'spawn': 0.5, 'select': 1.5, 'launch': 2.5, 'v_mag': 8.0, 'state': 'PENDING'},
        {'id': "TRK-02", 'pos': np.array([900.0, 1900.0]), 'aim': np.array([600.0, 300.0]), 'spawn': 8.0, 'select': 9.0, 'launch': 10.0, 'v_mag': 9.0, 'state': 'PENDING'},
        {'id': "TRK-03", 'pos': np.array([50.0, 1600.0]), 'aim': np.array([500.0, 300.0]), 'spawn': 15.5, 'select': 16.5, 'launch': 17.5, 'v_mag': 9.5, 'state': 'PENDING'}
    ]
    
    for h in hostiles:
        direction = h['aim'] - h['pos']
        h['vel'] = (direction / np.linalg.norm(direction)) * h['v_mag']
        h['history'] = []
        h['int_pos'] = np.copy(base_pos)
        h['int_history'] = []

    # Spallation Debris Matrix
    N_DEB = 1000
    d_x, d_y, d_vx, d_vy, d_life = np.zeros(N_DEB), np.zeros(N_DEB), np.zeros(N_DEB), np.zeros(N_DEB), np.zeros(N_DEB)

    def spawn_debris(pos, vel):
        dead = np.where(d_life <= 0)[0]
        n_spawn = min(60, len(dead))
        if n_spawn > 0:
            idx = dead[:n_spawn]
            d_x[idx] = pos[0]
            d_y[idx] = pos[1]
            angs = np.random.uniform(0, 2*np.pi, n_spawn)
            spds = np.random.uniform(2.0, 8.0, n_spawn)
            d_vx[idx] = vel[0] * 0.5 + np.cos(angs) * spds
            d_vy[idx] = vel[1] * 0.5 + np.sin(angs) * spds
            d_life[idx] = 1.0

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        radar_angle = -(t_sec * 3.0) % (2 * math.pi)

        # 1. Update Friendlies
        for flt in friendlies:
            flt['pos'] += flt['vel']
            if flt['pos'][0] < -50: flt['pos'][0] = 1130
            elif flt['pos'][0] > 1130: flt['pos'][0] = -50
            if flt['pos'][1] < -50: flt['pos'][1] = 1970
            elif flt['pos'][1] > 1970: flt['pos'][1] = -50
                
            flt['history'].append(flt['pos'].copy())
            if len(flt['history']) > 15: flt['history'].pop(0)

        # 2. Update Hostiles & Interceptor Logic
        active_track_uid = "NOMINAL"
        active_ghost = None
        current_status = "SCANNING RADAR SECTORS..."
        
        for h in hostiles:
            if h['state'] == 'DESTROYED': continue
            
            if t_sec >= h['spawn'] and h['state'] == 'PENDING':
                h['state'] = 'TRACKING'
            if t_sec >= h['select'] and h['state'] == 'TRACKING':
                h['state'] = 'SELECTED'
            if t_sec >= h['launch'] and h['state'] == 'SELECTED':
                h['state'] = 'ENGAGED'

            if h['state'] in ['TRACKING', 'SELECTED', 'ENGAGED']:
                h['pos'] += h['vel']
                h['history'].append(h['pos'].copy())
                if len(h['history']) > 20: h['history'].pop(0)

                active_track_uid = h['id']
                if h['state'] == 'TRACKING': current_status = f"UNKNOWN KINEMATIC VECTOR DETECTED"
                if h['state'] == 'SELECTED': current_status = f"LIGHT GUN ENGAGED. CALCULATING T.T.I."
                if h['state'] == 'ENGAGED':  current_status = f"INTERCEPTOR IN FLIGHT. O(1) DATALINK."

                # Mathematics of the 'Ghost Intercept' Lead Calculation
                dist = np.linalg.norm(h['pos'] - base_pos)
                tti = dist / interceptor_speed
                ghost_x = h['pos'][0] + (h['vel'][0] * tti)
                ghost_y = h['pos'][1] + (h['vel'][1] * tti)
                active_ghost = np.array([ghost_x, ghost_y])

                if h['state'] == 'ENGAGED':
                    # Missile steers toward the absolute mathematical ghost
                    dist_m = np.linalg.norm(h['int_pos'] - active_ghost)
                    dir_vec = active_ghost - h['int_pos']
                    
                    if np.linalg.norm(dir_vec) > 0.1:
                        h['int_pos'] += (dir_vec / np.linalg.norm(dir_vec)) * interceptor_speed
                        
                    h['int_history'].append(h['int_pos'].copy())
                    if len(h['int_history']) > 20: h['int_history'].pop(0)

                    # Collision Matrix
                    if np.linalg.norm(h['int_pos'] - h['pos']) < interceptor_speed * 1.5:
                        h['state'] = 'DESTROYED'
                        active_track_uid = f"{h['id']} - NEUTRALISED"
                        current_status = "KINETIC IMPACT. TRACK PURGED."
                        spawn_debris(h['pos'], h['vel'])

        # 3. Spallation Updates
        d_life -= 0.05
        d_x += d_vx
        d_y += d_vy
        
        act_d = np.where(d_life > 0)[0]

        # Extract rendering tensors
        r_flts = [{'pos': fl['pos'].copy(), 'hist': list(fl['history']), 'id': fl['id']} for fl in friendlies]
        r_hsts = [{'state': h['state'], 'pos': h['pos'].copy(), 'hist': list(h['history']), 
                   'id': h['id'], 'int_pos': h['int_pos'].copy(), 'int_hist': list(h['int_history'])} for h in hostiles if h['state'] != 'PENDING']

        yield (f, base_pos, radar_angle, active_track_uid, current_status, active_ghost, 
               r_flts, r_hsts, np.copy(d_x[act_d]), np.copy(d_y[act_d]), np.copy(d_life[act_d]))

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    (f, base_pos, radar_angle, a_uid, a_stat, a_ghost, r_flts, r_hsts, dx, dy, dl) = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # 1. VECTOR GEOGRAPHY & GRID
    coastline, borders = generate_vector_map()
    coast_x, coast_y = zip(*coastline)
    
    # Dense Grid Background
    for x_line in range(0, 1100, 100):
        ax.plot([x_line, x_line], [0, 1920], color=C_COAST, lw=1.5, alpha=0.6, zorder=1)
    for y_line in range(0, 2000, 100):
        ax.plot([0, 1080], [y_line, y_line], color=C_COAST, lw=1.5, alpha=0.6, zorder=1)

    ax.plot(coast_x, coast_y, color=C_STEEL, lw=4, zorder=2)
    for bx, by in borders:
        ax.plot([bx[0], by[0]], [bx[1], by[1]], color=C_STEEL, lw=2, linestyle='dashed', zorder=2)
        
    ax.add_patch(plt.Rectangle((base_pos[0]-15, base_pos[1]-15), 30, 30, fill=True, color=C_TEXT, zorder=5))
    ax.text(base_pos[0]+25, base_pos[1]-5, "RADAR BASE 07", color=C_TEXT, fontsize=12, fontname='monospace', weight='bold', zorder=6)

    # Radial Sweep Line
    sweep_len = 1500
    sx = base_pos[0] + sweep_len * math.cos(radar_angle)
    sy = base_pos[1] + sweep_len * math.sin(radar_angle)
    ax.plot([base_pos[0], sx], [base_pos[1], sy], color=C_STEEL, lw=2, alpha=0.4, zorder=7)

    # 2. COMMERCIAL/PASSIVE TRAFFIC
    for flt in r_flts:
        if len(flt['hist']) > 2:
            pts = np.array(flt['hist'])
            ax.plot(pts[:, 0], pts[:, 1], color=C_STEEL, lw=2, alpha=0.5, zorder=8)
            
        ax.add_patch(patches.Circle((flt['pos'][0], flt['pos'][1]), 6, facecolor=C_STEEL, zorder=9))
        
        # Identify flights near the scan line
        ang_to_flt = math.atan2(flt['pos'][1] - base_pos[1], flt['pos'][0] - base_pos[0]) % (2 * math.pi)
        if abs(radar_angle - ang_to_flt) < 0.2:
            ax.text(flt['pos'][0]+15, flt['pos'][1]+10, flt['id'], color=C_TEXT, fontsize=10, fontname='monospace', weight='bold', zorder=10)
            ax.add_patch(patches.Circle((flt['pos'][0], flt['pos'][1]), 8, facecolor=C_TEXT, zorder=9))

    # 3. HOSTILE TENSORS & INTERCEPT KINEMATICS
    for h in r_hsts:
        if h['state'] == 'DESTROYED': continue

        # Hostile Path History
        if len(h['hist']) > 2:
            pts = np.array(h['hist'])
            ax.plot(pts[:, 0], pts[:, 1], color=C_HOSTILE, lw=4, zorder=12, solid_capstyle='round')

        # Hostile Object
        ax.add_patch(plt.Rectangle((h['pos'][0]-10, h['pos'][1]-10), 20, 20, facecolor=C_HOSTILE, zorder=13))

        if h['state'] in ['SELECTED', 'ENGAGED']:
            cx, cy = h['pos']
            s = 35 # Bounding box size
            ax.plot([cx-s, cx-s, cx-s+12], [cy+s, cy+s-12, cy+s-12], color=C_TARGET, lw=4, zorder=14)
            ax.plot([cx-s, cx-s, cx-s+12], [cy-s, cy-s+12, cy-s+12], color=C_TARGET, lw=4, zorder=14)
            ax.plot([cx+s, cx+s, cx+s-12], [cy+s, cy+s-12, cy+s-12], color=C_TARGET, lw=4, zorder=14)
            ax.plot([cx+s, cx+s, cx+s-12], [cy-s, cy-s+12, cy-s+12], color=C_TARGET, lw=4, zorder=14)
            
            # Distance Telemetry
            dist_to_base = np.linalg.norm(h['pos'] - base_pos) * 0.1 # Arbitrary scale for UI km
            ax.text(cx + 45, cy, f"TRK: {h['id']}", color=C_HOSTILE, fontsize=14, fontname='monospace', weight='bold', zorder=15)
            ax.text(cx + 45, cy - 25, f"RNG: {dist_to_base:.1f} KM", color=C_TEXT, fontsize=12, fontname='monospace', weight='bold', zorder=15)

            # Mathematical Ghost Intercept Pointer
            if a_ghost is not None:
                ax.plot([base_pos[0], a_ghost[0]], [base_pos[1], a_ghost[1]], color=C_STEEL, linestyle='dotted', lw=3, zorder=11)
                ax.scatter(a_ghost[0], a_ghost[1], marker='x', color=C_TARGET, s=150, lw=3, zorder=16)
                ax.text(a_ghost[0]+20, a_ghost[1]+20, "PROJ. INTERCEPT", color=C_TARGET, fontsize=12, fontname='monospace', weight='bold', zorder=17)

        # Active BOMARC Missile In Flight
        if h['state'] == 'ENGAGED':
            if len(h['int_hist']) > 2:
                ipts = np.array(h['int_hist'])
                ax.plot(ipts[:, 0], ipts[:, 1], color=C_INTERCEPT, lw=5, zorder=18, solid_capstyle='round')

            # Interceptor Polygon (Diamond)
            ix, iy = h['int_pos']
            ax.add_patch(patches.Polygon([[ix, iy+15], [ix-12, iy], [ix, iy-15], [ix+12, iy]], facecolor=C_INTERCEPT, zorder=19))
            
            if f % 10 < 5:
                ax.plot([base_pos[0], ix], [base_pos[1], iy], color=C_TARGET, lw=2, linestyle='dashed', zorder=11)

    # 4. KINETIC SPALLATION DEBRIS
    if len(dx) > 0:
        c_deb = np.zeros((len(dx), 4))
        c_deb[:, :3] = np.array(mcol.to_rgb(C_TEXT))
        c_deb[:, 3] = dl # Fading life
        ax.scatter(dx, dy, s=dl*45, c=c_deb, marker='s', edgecolors='none', zorder=25)

    # 5. ABSOLUTE DAYLIGHT TELEMETRY (TOP)
    ax.add_patch(plt.Rectangle((0, 1820), 1080, 100, facecolor=C_BG, zorder=80))
    ax.plot([0, 1080], [1820, 1820], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(40, 1870, "USAF AN/FSQ-7 [SAGE CONTINUOUS TENSOR]", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=82)
    ax.text(40, 1835, "DAYLIGHT INVERSE PROTOCOL // TRUE KINEMATICS", color=C_STEEL, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=82)
    
    ax.text(900, 1850, f"CYC:{f:05d}", color=C_TEXT, fontsize=22, fontname='monospace', weight='bold', zorder=82)

    # 6. ABSOLUTE DAYLIGHT TELEMETRY (BOTTOM)
    ax.add_patch(plt.Rectangle((0, 0), 1080, 180, facecolor=C_BG, zorder=80))
    ax.plot([0, 1080], [180, 180], color=C_TEXT, lw=6, zorder=81)
    
    ax.text(40, 130, f"SYSTEM TRAFFIC : 15 PASSIVE VECTORS", color=C_TEXT, fontsize=18, fontname='monospace', weight='bold', zorder=82)
    ax.text(40, 90, f"KINETIC FOCUS  : ", color=C_TEXT, fontsize=18, fontname='monospace', weight='bold', zorder=82)
    
    pulse_col = C_OK if "NEUTRALISED" in a_uid else (C_HOSTILE if a_uid != "NOMINAL" else C_TEXT)
    ax.text(280, 90, a_uid, color=pulse_col, fontsize=20, fontname='monospace', weight='bold', zorder=82)
    
    pulse_stat = C_TARGET if ("ENGAGED" in a_stat or "CALCULATING" in a_stat) else C_STEEL
    ax.text(40, 40, f"> {a_stat}", color=pulse_stat, fontsize=18, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-138b: SAGE AN/FSQ-7 DAYLIGHT PROTOCOL [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Inverse Kinematics Locked. Stand by for compilation.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
