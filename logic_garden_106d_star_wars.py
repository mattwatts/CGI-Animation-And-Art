"""
PROJECT: Logic Garden 106d (Exact Physical Construct // Phased Engagement)
FORMAT: YouTube Shorts (1080x1920)
METADATA: SDI, TARGET ACQUISITION, BALLISTICS, DAYLIGHT
EXECUTION: 24.0s Sequence. True 2D High-Density Construct.
RULES ENFORCED: 
- Bipartite Operational Matrix (Surveillance Phase -> Kill Phase).
- Persistent Target Locking logic (O(1) dictionary mapping).
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
OUT_DIR = "frames_106d_star_wars"
os.makedirs(OUT_DIR, exist_ok=True)
WEAPONS_FREE_SEC = 8.0

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'          # Indestructible Black UI
C_STEEL     = '#94A3B8'          # Decoys / Baseline Grid
C_EARTH     = '#F8FAFC'          # Atmosphere Bedrock
C_CRANE     = '#1E293B'          # Heavy Boosters (Carbon Slate)
C_MIRV      = '#DE008A'          # True Warheads (Deep Magenta)
C_LASER     = '#FFB300'          # Directed Energy (Dense Amber)
C_BURN      = '#FF3300'          # Intense Red Plume/Damage
C_SDI       = '#005599'          # Space Platforms (Deep Marine)
C_TRACK     = '#00C853'          # Sensor Arrays (Jade)

# ------------------------------------------------------------------
# O(1) FLIGHT KINEMATICS ENGINE
# ------------------------------------------------------------------
class Missile:
    def __init__(self, uid, x_pos, t_launch):
        self.id = uid
        self.pos = np.array([x_pos, -900.0])
        self.vel = np.array([np.random.uniform(-3.0, 3.0), np.random.uniform(14.0, 18.0)])
        self.state = "BOOST"
        self.t_launch = t_launch
        self.warheads = []
        self.decoys = []
        self.health = 1.0

    def deploy_bus(self):
        self.state = "BUS_DEPLOY"
        # Deploy 3 True MIRVs
        for i in range(3):
            drift = np.array([np.random.uniform(-4, 4), np.random.uniform(-1, 2)])
            self.warheads.append({'pos': self.pos.copy(), 'vel': self.vel + drift, 'health': 1.0, 'id': i})
        # Deploy 6 Radar Decoys
        for i in range(6):
            drift = np.array([np.random.uniform(-6, 6), np.random.uniform(-2, 3)])
            # Decoys are fragile
            self.decoys.append({'pos': self.pos.copy(), 'vel': self.vel + drift, 'health': 0.1, 'id': i})

class SDISatellite:
    def __init__(self, uid, x_pos, y_pos):
        self.id = uid
        self.pos = np.array([x_pos, y_pos])
        self.base_x = x_pos
        self.target_uid = None  
        self.fire_timer = 0     
        self.cooldown = 0
        self.track_pos = None
        self.hit_pos = None

# ------------------------------------------------------------------
# PARALLEL GENERATOR (LOGIC TENSORS)
# ------------------------------------------------------------------
def generate_stream():
    np.random.seed(1064)
    
    missiles = []
    # Heavily saturate the launch window
    launch_schedule = [
        (0.5, -400), (1.0, 200),  (1.8, -150), 
        (2.5,  350), (3.0, -50),  (3.8,  450), 
        (4.5, -250), (5.5,  100)
    ]
    
    satellites = [
        SDISatellite(0, -420, 750), SDISatellite(1, -140, 820),
        SDISatellite(2,  140, 820), SDISatellite(3,  420, 750)
    ]

    # Spallation Engine Array
    N_DEBRIS = 5000
    d_x, d_y = np.zeros(N_DEBRIS), np.zeros(N_DEBRIS)
    d_vx, d_vy = np.zeros(N_DEBRIS), np.zeros(N_DEBRIS)
    d_life = np.zeros(N_DEBRIS)
    
    def spawn_debris(pos, base_vel, count, is_fragile=False):
        dead = np.where(d_life <= 0)[0]
        n_spawn = min(count, len(dead))
        if n_spawn > 0:
            idx = dead[:n_spawn]
            d_x[idx] = pos[0] + np.random.uniform(-10, 10, n_spawn)
            d_y[idx] = pos[1] + np.random.uniform(-10, 10, n_spawn)
            angs = np.random.uniform(0, 2*np.pi, n_spawn)
            
            # Massive kinetic blast if actual warhead
            spd_multi = 1.0 if is_fragile else 3.0
            spds = np.random.uniform(2.0, 6.0, n_spawn) * spd_multi
            
            d_vx[idx] = base_vel[0] + np.cos(angs) * spds
            d_vy[idx] = base_vel[1] + np.sin(angs) * spds
            d_life[idx] = 1.0

    for f in range(TOTAL_FRAMES):
        t = f / FPS
        weapons_free = (t >= WEAPONS_FREE_SEC)
        
        # 1. Spawn Threat Ascent
        for tt, tx in launch_schedule:
            if abs(t - tt) < 0.01:
                missiles.append(Missile(len(missiles), tx, t))
                
        # 2. Physics & Central Architecture Tracking
        threats_dict = {}
        
        for m in missiles:
            if m.state == "BOOST":
                m.pos += m.vel
                m.vel[1] -= 0.015 # Gravity
                if m.pos[1] > -100: 
                    m.deploy_bus()
                else:
                    threats_dict[f"M_{m.id}"] = {'obj': m, 'pos': m.pos, 'type': 'BOOST', 'vel': m.vel}
                    
            elif m.state == "BUS_DEPLOY":
                # Advance Payload Tensors
                for w in m.warheads:
                    if w['health'] > 0:
                        w['pos'] += w['vel']
                        w['vel'][1] -= 0.015
                        threats_dict[f"MIRV_{m.id}_{w['id']}"] = {'obj': w, 'pos': w['pos'], 'type': 'MIRV', 'vel': w['vel']}
                for d in m.decoys:
                    if d['health'] > 0:
                        d['pos'] += d['vel']
                        d['vel'][1] -= 0.015
                        threats_dict[f"DCY_{m.id}_{d['id']}"] = {'obj': d, 'pos': d['pos'], 'type': 'DECOY', 'vel': d['vel']}

        # 3. SDI Engagement Matrix
        active_lasers = []
        active_tracks = []
        
        for s in satellites:
            s.pos[0] = s.base_x + np.sin(t * 0.4 + s.id) * 40.0 # Slow patrol
            s.pos[1] += np.cos(t * 0.2) * 0.1
            
            s.track_pos = None
            s.hit_pos = None
            
            # Check target validity
            if s.target_uid not in threats_dict:
                s.target_uid = None
            
            # Target Acquisition
            if s.target_uid is None and s.cooldown <= 0 and len(threats_dict) > 0:
                prio_map = {'MIRV': 1, 'BOOST': 2, 'DECOY': 3}
                valid = []
                for uid, th in threats_dict.items():
                    if th['pos'][1] < s.pos[1]: # Must be below platform
                        valid.append((uid, th))
                        
                if valid:
                    # Sort completely by Threat Priority -> Geographic Proximity
                    valid.sort(key=lambda x: (prio_map[x[1]['type']], np.linalg.norm(x[1]['pos'] - s.pos)))
                    s.target_uid = valid[0][0]
                    s.fire_timer = 20 if valid[0][1]['type'] != 'DECOY' else 4
            
            # Execution
            if s.target_uid is not None:
                th_data = threats_dict[s.target_uid]
                th_obj = th_data['obj']
                th_pos = th_data['pos']
                
                if not weapons_free:
                    # SURVEILLANCE PHASE (Paint Targets)
                    s.track_pos = th_pos.copy()
                    active_tracks.append((s.pos.copy(), s.track_pos.copy()))
                    
                    # Force a simulated tracking cooldown to scan multiple targets? 
                    # No, rigid lock on high priority target until weapons free
                else:
                    # WEAPONS FREE PHASE (Burn Through)
                    s.track_pos = th_pos.copy() 
                    s.hit_pos = th_pos.copy()
                    active_lasers.append((s.pos.copy(), s.hit_pos.copy()))
                    
                    s.fire_timer -= 1
                    th_obj['health'] -= 0.05
                    
                    if th_obj['health'] <= 0 or s.fire_timer <= 0:
                        th_obj['health'] = 0
                        s.cooldown = 12
                        s.target_uid = None
                        spawn_debris(th_pos, th_data['vel'], 
                                     100 if th_data['type'] != 'DECOY' else 25, 
                                     th_data['type'] == 'DECOY')
                        
            if s.cooldown > 0:
                s.cooldown -= 1

        # 4. Spallation Tensor Processing
        d_life -= 0.02
        d_x += d_vx
        d_y += d_vy
        d_vy -= 0.01 
        
        act_d = np.where(d_life > 0)[0]

        # Serialise output logic arrays
        r_boost   = [m for m in missiles if m.state == "BOOST"]
        r_mirv    = [w for m in missiles for w in m.warheads if w['health'] > 0]
        r_decoy   = [d for m in missiles for d in m.decoys if d['health'] > 0]
        r_lasers  = active_lasers
        r_tracks  = active_tracks
        r_sats    = [s.pos.copy() for s in satellites]
        
        yield (f, t, weapons_free, r_boost, r_mirv, r_decoy, r_lasers, r_tracks, r_sats, 
               np.copy(d_x[act_d]), np.copy(d_y[act_d]), np.copy(d_life[act_d]))

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t, weapons_free, r_boost, r_mirv, r_decoy, r_lasers, r_tracks, r_sats, dx, dy, dl = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)

    # 1. BEDROCK AND EXO-LIMIT GRID
    ax.add_patch(patches.Rectangle((-600, -1000), 1200, 200, facecolor=C_EARTH, zorder=1))
    ax.plot([-600, 600], [-800, -800], color=C_TEXT, lw=4, zorder=2)
    
    ax.plot([-540, 540], [-100, -100], color=C_STEEL, lw=2, linestyle='dashed', zorder=2)
    ax.text(-520, -80, "EXOATMOSPHERIC INTERFACE (VACUUM Y>-100)", color=C_STEEL, fontsize=14, fontname='monospace', weight='bold', zorder=50)

    # 2. SDI PLATFORMS (Deep Marine Geometry)
    for p in r_sats:
        px, py = p[0], p[1]
        ax.add_patch(patches.Rectangle((px-18, py-12), 36, 24, facecolor=C_SDI, edgecolor=C_TEXT, lw=2, zorder=10))
        ax.add_patch(patches.Rectangle((px-65, py-6), 46, 12, facecolor=C_STEEL, edgecolor=C_TEXT, lw=1.5, zorder=9))
        ax.add_patch(patches.Rectangle((px+19, py-6), 46, 12, facecolor=C_STEEL, edgecolor=C_TEXT, lw=1.5, zorder=9))
        # Optic Lens
        optic_color = C_LASER if weapons_free else C_TRACK
        ax.add_patch(patches.Circle((px, py-12), 8, facecolor=optic_color, zorder=11))

    # 3. DIRECTED ENERGY & TRACKING SENSORS
    # A. Tracking Vectors (Phase 1)
    for T_start, T_end in r_tracks:
        ax.plot([T_start[0], T_end[0]], [T_start[1], T_end[1]], color=C_TRACK, lw=2, linestyle='dotted', zorder=4)
        # Draw Target Reticle at destination
        tx, ty = T_end[0], T_end[1]
        s = 20
        ax.plot([tx-s, tx-s/2], [ty-s, ty-s], color=C_TRACK, lw=2)
        ax.plot([tx+s/2, tx+s], [ty-s, ty-s], color=C_TRACK, lw=2)
        ax.plot([tx-s, tx-s/2], [ty+s, ty+s], color=C_TRACK, lw=2)
        ax.plot([tx+s/2, tx+s], [ty+s, ty+s], color=C_TRACK, lw=2)

    # B. Directed Energy Burn-Through (Phase 2)
    for L_start, L_end in r_lasers:
        ax.plot([L_start[0], L_end[0]], [L_start[1], L_end[1]], color=C_LASER, lw=8, zorder=4, solid_capstyle='round')
        ax.plot([L_start[0], L_end[0]], [L_start[1], L_end[1]], color=C_BG, lw=3, zorder=5, solid_capstyle='round')
        ax.add_patch(patches.Circle((L_end[0], L_end[1]), 30, facecolor=C_LASER, alpha=0.6, zorder=15))
        ax.add_patch(patches.Circle((L_end[0], L_end[1]), 12, facecolor=C_BG, zorder=16))

    # 4. THREAT MATRICES
    for d in r_decoy:
        ax.add_patch(patches.Rectangle((d['pos'][0]-5, d['pos'][1]-5), 10, 10, facecolor=C_STEEL, edgecolor=C_TEXT, lw=1.5, zorder=12))

    for w in r_mirv:
        px, py = w['pos'][0], w['pos'][1]
        vx, vy = w['vel'][0], w['vel'][1]
        ang = np.arctan2(vy, vx) - np.pi/2
        poly = np.array([[0, 18], [-9, -12], [9, -12]])
        rot = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
        poly_rot = np.dot(poly, rot.T) + [px, py]
        ax.add_patch(patches.Polygon(poly_rot, facecolor=C_MIRV, edgecolor=C_TEXT, lw=2, zorder=13))

    for b in r_boost:
        px, py = b.pos[0], b.pos[1]
        vx, vy = b.vel[0], b.vel[1]
        ang = np.arctan2(vy, vx) - np.pi/2
        poly = np.array([[-14, 45], [14, 45], [14, -45], [-14, -45]])
        rot = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
        poly_rot = np.dot(poly, rot.T) + [px, py]
        ax.add_patch(patches.Polygon(poly_rot, facecolor=C_CRANE, edgecolor=C_TEXT, lw=3, zorder=14))
        
        p_x, p_y = px - np.sin(ang)*45, py - np.cos(ang)*45
        ax.scatter([p_x], [p_y], s=300, color=C_BURN, zorder=13)
        ax.plot([p_x, p_x - vx*4], [p_y, p_y - vy*4], color=C_BURN, lw=10, solid_capstyle='round', zorder=12)

    # 5. SPALLATION DEBRIS
    if len(dx) > 0:
        c_deb = np.zeros((len(dx), 4))
        c_deb[:, :3] = np.array(mcol.to_rgb(C_TEXT))
        hot_mask = dl > 0.65
        c_deb[hot_mask, :3] = np.array(mcol.to_rgb(C_BURN))
        c_deb[:, 3] = dl 
        ax.scatter(dx, dy, s=dl*35, c=c_deb, edgecolors='none', zorder=18)

    # 6. ABSOLUTE DAYLIGHT TELEMETRY 
    ax.add_patch(plt.Rectangle((0, 0.90), 1, 0.10, transform=ax.transAxes, facecolor=C_BG, zorder=80))
    ax.plot([0, 1], [0.90, 0.90], transform=ax.transAxes, color=C_TEXT, lw=6, zorder=81)
    
    ax.text(0.04, 0.965, "STRATEGIC DEFENCE INITIATIVE (SDI)", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=82)
    
    # Phase specific header
    if weapons_free:
        hdr_txt = "PHASE 2 // DIRECTED ENERGY ENGAGEMENT"
        hdr_col = C_LASER
    else:
        hdr_txt = "PHASE 1 // TARGET ACQUISITION & SURVEILLANCE"
        hdr_col = C_TRACK
        
    ax.text(0.04, 0.930, hdr_txt, transform=ax.transAxes, color=hdr_col, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=82)

    # Bottom Display
    ax.add_patch(plt.Rectangle((0, 0), 1, 0.12, transform=ax.transAxes, facecolor=C_BG, zorder=80))
    ax.plot([0, 1], [0.12, 0.12], transform=ax.transAxes, color=C_TEXT, lw=6, zorder=81)
    
    n_b = len(r_boost)
    n_w = len(r_mirv)
    n_d = len(r_decoy)
    
    if not weapons_free:
        if n_b > 0 and n_w == 0: ui_msg = "[STATE: LAUNCH ALARM DETECTED]"
        else: ui_msg = "[STATE: THREAT CLOUD SATURATION]"
        ui_color = C_TRACK
    else:
        if len(r_lasers) > 0: ui_msg = "[STATE: INTERCEPT IN PROGRESS]"
        elif n_b == 0 and n_w == 0 and t > 10.0: ui_msg = "[STATE: SKY CLEAR // NEUTRALIZED]"
        else: ui_msg = "[STATE: WEAPONS FREE // RE-ACQUIRING]"
        ui_color = C_LASER if len(r_lasers) > 0 else (C_LOCK if "CLEAR" in ui_msg else C_TEXT)

    ax.text(0.04, 0.085, f"HEAVY BOOSTERS : {n_b:02.0f}", transform=ax.transAxes, color=C_CRANE, fontsize=18, fontname='monospace', weight='bold', zorder=82)
    ax.text(0.04, 0.055, f"EXO-WARHEADS   : {n_w:02.0f}", transform=ax.transAxes, color=C_MIRV, fontsize=18, fontname='monospace', weight='bold', zorder=82)
    ax.text(0.04, 0.025, f"DECOY CHAFF    : {n_d:02.0f}", transform=ax.transAxes, color=C_STEEL, fontsize=18, fontname='monospace', weight='bold', zorder=82)

    pulse = ui_color if (f % 30 < 20) else C_BG
    ax.text(0.96, 0.055, ui_msg, transform=ax.transAxes, color=pulse, fontsize=20, fontname='monospace', weight='bold', ha='right', va='center', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-106d: SDI PHASED ENGAGEMENT (DAYLIGHT) [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Orbital Intercept Mechanics Locked. Stand by for compilation.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
