"""
PROJECT: Logic Garden 106e (Exact Physical Construct // Macro-Scale SDI)
FORMAT: YouTube Shorts (1080x1920)
METADATA: SDI, BALLISTICS, KINEMATIC INTERCEPT, RADIAL GRAVITY, DAYLIGHT
EXECUTION: 24.0s Sequence. True Suborbital Flight Paths.
RULES ENFORCED: 
- O(1) True Radial Newtonian Gravity (-GM/R^2).
- Macro-scale Planetary Geometry & Atmospheric Reentry Spallation.
- Bipartite Operational Matrix (Surveillance Phase -> Kill Phase).
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
OUT_DIR = "frames_106e_star_wars"
os.makedirs(OUT_DIR, exist_ok=True)
WEAPONS_FREE_SEC = 8.0

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'          # Indestructible Black UI
C_STEEL     = '#94A3B8'          # Decoys / Baseline Grid
C_EARTH     = '#F1F5F9'          # Planetary Bedrock
C_CRANE     = '#1E293B'          # Heavy Boosters (Carbon Slate)
C_MIRV      = '#DE008A'          # True Warheads (Deep Magenta)
C_LASER     = '#FFB300'          # Directed Energy (Dense Amber)
C_BURN      = '#FF3300'          # Reentry Heat / Plume
C_SDI       = '#005599'          # Space Platforms (Deep Marine)
C_TRACK     = '#00C853'          # Sensor Arrays (Jade)
C_LOCK      = '#00C853'          # Clear/Engaged Telemetry (Jade)

# ------------------------------------------------------------------
# O(1) MACRO PHYSICS ENGINE (RADIAL GRAVITY)
# ------------------------------------------------------------------
EARTH_C = np.array([0.0, -4000.0])
R_EARTH = 3200.0
R_ATMOS = 3380.0
R_ORBIT = 4700.0
GM_CONST = 500000.0 # Absolute gravitational multiplier

def radial_gravity(pos):
    vec = pos - EARTH_C
    dist = np.linalg.norm(vec)
    if dist < 1.0: return np.zeros(2)
    mag = -(GM_CONST / (dist**2))
    return mag * (vec / dist)

class Missile:
    def __init__(self, uid, deg, v_mag, v_deg):
        self.id = uid
        rad_surf = np.radians(deg)
        # Position exactly on massive Earth perimeter
        self.pos = EARTH_C + np.array([R_EARTH * np.cos(rad_surf), R_EARTH * np.sin(rad_surf)])
        
        # Velocity vector relative to Earth Center
        rad_v = np.radians(v_deg) # Absolute flight vector
        self.vel = np.array([v_mag * np.cos(rad_v), v_mag * np.sin(rad_v)])
        
        self.state = "BOOST"
        self.warheads = []
        self.decoys = []
        self.health = 1.0
        
        # Orient booster visually
        self.pitch = v_deg 

    def deploy_bus(self):
        self.state = "BUS_DEPLOY"
        # Deploy 3 True MIRVs
        for i in range(3):
            drift = np.array([np.random.uniform(-1, 1), np.random.uniform(-1, 1)])
            self.warheads.append({'pos': self.pos.copy(), 'vel': self.vel + drift, 'health': 1.0, 'id': i})
        # Deploy 6 Decoys (scattered heavily)
        for i in range(6):
            drift = np.array([np.random.uniform(-2.5, 2.5), np.random.uniform(-2.5, 2.5)])
            self.decoys.append({'pos': self.pos.copy(), 'vel': self.vel + drift, 'health': 0.1, 'id': i})

class SDISatellite:
    def __init__(self, uid, deg):
        self.id = uid
        self.base_deg = deg
        rad_orb = np.radians(deg)
        self.pos = EARTH_C + np.array([R_ORBIT * np.cos(rad_orb), R_ORBIT * np.sin(rad_orb)])
        self.target_uid = None  
        self.fire_timer = 0     
        self.cooldown = 0
        self.track_pos = None
        self.hit_pos = None

# ------------------------------------------------------------------
# PARALLEL GENERATOR (LOGIC TENSORS)
# ------------------------------------------------------------------
def generate_stream():
    np.random.seed(1065)
    
    missiles = []
    # Western Hemisphere suborbital launch coordinates 
    # [time, earth_deg, v_mag, flight_deg]
    launch_schedule = [
        (0.5, 100, 11.5, 75),  (1.2, 98, 11.0, 72),  (1.8, 97, 12.0, 78), 
        (2.5, 102, 10.5, 70),  (3.0, 99, 11.8, 76),  (3.8, 95, 12.5, 80),
        (4.5, 96, 11.2, 74)
    ]
    
    # 5 SDI Platforms spread across the northern orbital arc
    satellites = [
        SDISatellite(0, 115), SDISatellite(1, 102.5),
        SDISatellite(2,  90), SDISatellite(3,  77.5),
        SDISatellite(4,  65)
    ]

    # Spallation Engine
    N_DEBRIS = 6000
    d_x, d_y = np.zeros(N_DEBRIS), np.zeros(N_DEBRIS)
    d_vx, d_vy = np.zeros(N_DEBRIS), np.zeros(N_DEBRIS)
    d_life = np.zeros(N_DEBRIS)
    d_hot = np.zeros(N_DEBRIS, dtype=bool) # Reentry heat tracking
    
    def spawn_debris(pos, base_vel, count, is_fragile=False):
        dead = np.where(d_life <= 0)[0]
        n_spawn = min(count, len(dead))
        if n_spawn > 0:
            idx = dead[:n_spawn]
            d_x[idx] = pos[0] + np.random.uniform(-10, 10, n_spawn)
            d_y[idx] = pos[1] + np.random.uniform(-10, 10, n_spawn)
            angs = np.random.uniform(0, 2*np.pi, n_spawn)
            spd_multi = 1.0 if is_fragile else 2.5
            spds = np.random.uniform(1.0, 4.0, n_spawn) * spd_multi
            d_vx[idx] = base_vel[0] + np.cos(angs) * spds
            d_vy[idx] = base_vel[1] + np.sin(angs) * spds
            d_life[idx] = 1.0
            d_hot[idx] = False

    for f in range(TOTAL_FRAMES):
        t = f / FPS
        weapons_free = (t >= WEAPONS_FREE_SEC)
        
        # 1. Spawn Threat Ascent
        for tt, deg, vmag, vdeg in launch_schedule:
            if abs(t - tt) < 0.01:
                missiles.append(Missile(len(missiles), deg, vmag, vdeg))
                
        # 2. Physics Integration (Newtonian Curves)
        threats_dict = {}
        dead_boosters = [] 
        
        for m in missiles:
            if m.state == "BOOST":
                m.vel += radial_gravity(m.pos)
                m.pos += m.vel
                m.pitch = np.degrees(np.arctan2(m.vel[1], m.vel[0]))
                
                dist_surf = np.linalg.norm(m.pos - EARTH_C)
                if dist_surf > R_ATMOS + 50: # Exits atmosphere completely
                    m.deploy_bus()
                    # Spawn dead booster shell falling away
                    dead_boosters.append({'pos': m.pos.copy(), 'vel': m.vel * 0.95})
                else:
                    threats_dict[f"M_{m.id}"] = {'obj': m, 'pos': m.pos, 'type': 'BOOST', 'vel': m.vel}
                    
            elif m.state == "BUS_DEPLOY":
                # Advance Payload Tensors
                for w in m.warheads:
                    if w['health'] > 0:
                        w['vel'] += radial_gravity(w['pos'])
                        w['pos'] += w['vel']
                        dist_surf = np.linalg.norm(w['pos'] - EARTH_C)
                        if dist_surf < R_EARTH: w['health'] = 0 # Impact
                        else: threats_dict[f"MIRV_{m.id}_{w['id']}"] = {'obj': w, 'pos': w['pos'], 'type': 'MIRV', 'vel': w['vel']}
                
                for d in m.decoys:
                    if d['health'] > 0:
                        d['vel'] += radial_gravity(d['pos'])
                        d['pos'] += d['vel']
                        dist_surf = np.linalg.norm(d['pos'] - EARTH_C)
                        if dist_surf < R_ATMOS: 
                            d['health'] = 0 # Decoys burn up instantly upon hitting atmos
                            spawn_debris(d['pos'], d['vel'], 5, True)
                        else:
                            threats_dict[f"DCY_{m.id}_{d['id']}"] = {'obj': d, 'pos': d['pos'], 'type': 'DECOY', 'vel': d['vel']}

        # 3. SDI Engagement Matrix
        active_lasers = []
        active_tracks = []
        
        for s in satellites:
            # Parametric orbital crawl
            orb_deg = s.base_deg - (t * 0.5) 
            rad_orb = np.radians(orb_deg)
            s.pos = EARTH_C + np.array([R_ORBIT * np.cos(rad_orb), R_ORBIT * np.sin(rad_orb)])
            
            s.track_pos = None
            s.hit_pos = None
            
            if s.target_uid not in threats_dict:
                s.target_uid = None
            
            # Target Acquisition
            if s.target_uid is None and s.cooldown <= 0 and len(threats_dict) > 0:
                prio_map = {'MIRV': 1, 'BOOST': 2, 'DECOY': 3}
                valid = []
                for uid, th in threats_dict.items():
                    # Line of sight check (must be roughly above Earth horizon)
                    th_dist_C = np.linalg.norm(th['pos'] - EARTH_C)
                    if th_dist_C > R_EARTH + 10: 
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
                
                # Handling Class vs Dictionary types seamlessly
                is_dict = isinstance(th_obj, dict)
                hp = th_obj['health'] if is_dict else th_obj.health

                if not weapons_free:
                    s.track_pos = th_pos.copy()
                    active_tracks.append((s.pos.copy(), s.track_pos.copy()))
                else:
                    s.track_pos = th_pos.copy() 
                    s.hit_pos = th_pos.copy()
                    active_lasers.append((s.pos.copy(), s.hit_pos.copy()))
                    
                    s.fire_timer -= 1
                    
                    if is_dict: th_obj['health'] -= 0.05
                    else: th_obj.health -= 0.05
                    hp -= 0.05
                    
                    if hp <= 0 or s.fire_timer <= 0:
                        if is_dict: th_obj['health'] = 0
                        else: th_obj.health = 0
                        
                        target_type = th_data['type']
                        s.target_uid = None
                        s.cooldown = 15 # Rest optics
                        spawn_debris(th_pos, th_data['vel'], 
                                     120 if target_type != 'DECOY' else 25, 
                                     target_type == 'DECOY')

            if s.cooldown > 0:
                s.cooldown -= 1

        # 4. Spallation Tensor Processing (Atmospheric Entry Rules)
        act_d = np.where(d_life > 0)[0]
        
        for idx in act_d:
            # Gravity
            vecC = np.array([d_x[idx], d_y[idx]]) - EARTH_C
            distC = np.linalg.norm(vecC)
            grav = -(GM_CONST / (distC**2)) * (vecC / distC)
            
            d_vx[idx] += grav[0]
            d_vy[idx] += grav[1]
            d_x[idx] += d_vx[idx]
            d_y[idx] += d_vy[idx]
            
            # Reentry friction
            if distC < R_ATMOS:
                d_hot[idx] = True
                d_life[idx] -= 0.04 # Burn up fast
                d_vx[idx] *= 0.95   # Drag
                d_vy[idx] *= 0.95
            else:
                d_hot[idx] = False
                d_life[idx] -= 0.01
                
            if distC < R_EARTH:
                d_life[idx] = 0 # Hit ground

        act_d = np.where(d_life > 0)[0]

        # Freeze extraction arrays for rendering
        r_boost   = [m for m in missiles if m.state == "BOOST"]
        r_mirv    = [w for m in missiles for w in m.warheads if w['health'] > 0]
        r_decoy   = [d for m in missiles for d in m.decoys if d['health'] > 0]
        r_lasers  = active_lasers
        r_tracks  = active_tracks
        r_sats    = [s.pos.copy() for s in satellites]
        
        yield (f, t, weapons_free, r_boost, r_mirv, r_decoy, r_lasers, r_tracks, r_sats, dead_boosters,
               np.copy(d_x[act_d]), np.copy(d_y[act_d]), np.copy(d_life[act_d]), np.copy(d_hot[act_d]))

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t, weapons_free, r_boost, r_mirv, r_decoy, r_lasers, r_tracks, r_sats, r_dead, dx, dy, dl, dhot = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)

    # 1. MACRO PLANETARY ALIGNMENT
    ax.add_patch(patches.Circle((EARTH_C[0], EARTH_C[1]), R_EARTH, facecolor=C_EARTH, edgecolor=C_STEEL, lw=4, zorder=1))
    
    # Atmospheric Envelope (Exoatmospheric line)
    ax.add_patch(patches.Circle((EARTH_C[0], EARTH_C[1]), R_ATMOS, fill=False, edgecolor=C_STEEL, lw=2, linestyle='dashed', zorder=2))
    
    # Dynamic text following the curve loosely
    ax.text(0, R_ATMOS + EARTH_C[1] + 15, "EXOATMOSPHERIC INTERFACE (MACRO BOUNDARY)", 
            color=C_STEEL, fontsize=16, fontname='monospace', weight='bold', ha='center', zorder=50)

    # 2. SDI SURVEILLANCE PLATFORMS
    for p in r_sats:
        px, py = p[0], p[1]
        # Orient satellite tangent to orbital ring
        ang = np.degrees(np.arctan2(py - EARTH_C[1], px - EARTH_C[0])) - 90
        
        t1 = matplotlib.transforms.Affine2D().rotate_deg_around(px, py, ang) + ax.transData
        
        rect_m = patches.Rectangle((px-18, py-12), 36, 24, facecolor=C_SDI, edgecolor=C_TEXT, lw=2, zorder=10, transform=t1)
        rect_sl = patches.Rectangle((px-65, py-6), 46, 12, facecolor=C_STEEL, edgecolor=C_TEXT, lw=1.5, zorder=9, transform=t1)
        rect_sr = patches.Rectangle((px+19, py-6), 46, 12, facecolor=C_STEEL, edgecolor=C_TEXT, lw=1.5, zorder=9, transform=t1)
        
        ax.add_patch(rect_m)
        ax.add_patch(rect_sl)
        ax.add_patch(rect_sr)
        
        optic_color = C_LASER if weapons_free else C_TRACK
        ax.add_patch(patches.Circle((px, py-12), 8, facecolor=optic_color, zorder=11, transform=t1))

    # 3. WEAPONS ENGAGEMENT & TRACKING
    for T_start, T_end in r_tracks:
        ax.plot([T_start[0], T_end[0]], [T_start[1], T_end[1]], color=C_TRACK, lw=2, linestyle='dotted', zorder=4)
        tx, ty = T_end[0], T_end[1]
        s = 20
        ax.plot([tx-s, tx-s/2], [ty-s, ty-s], color=C_TRACK, lw=2)
        ax.plot([tx+s/2, tx+s], [ty-s, ty-s], color=C_TRACK, lw=2)
        ax.plot([tx-s, tx-s/2], [ty+s, ty+s], color=C_TRACK, lw=2)
        ax.plot([tx+s/2, tx+s], [ty+s, ty+s], color=C_TRACK, lw=2)

    for L_start, L_end in r_lasers:
        ax.plot([L_start[0], L_end[0]], [L_start[1], L_end[1]], color=C_LASER, lw=6, zorder=4, solid_capstyle='round')
        ax.plot([L_start[0], L_end[0]], [L_start[1], L_end[1]], color=C_BG, lw=2, zorder=5, solid_capstyle='round')
        ax.add_patch(patches.Circle((L_end[0], L_end[1]), 25, facecolor=C_LASER, alpha=0.6, zorder=15))
        ax.add_patch(patches.Circle((L_end[0], L_end[1]), 10, facecolor=C_BG, zorder=16))

    # 4. THREAT MATRICES (Macro Scale)
    for d in r_decoy:
        ax.add_patch(patches.Rectangle((d['pos'][0]-4, d['pos'][1]-4), 8, 8, facecolor=C_STEEL, edgecolor=C_TEXT, lw=1, zorder=12))

    for w in r_mirv:
        px, py = w['pos'][0], w['pos'][1]
        vx, vy = w['vel'][0], w['vel'][1]
        ang = np.arctan2(vy, vx) - np.pi/2 
        poly = np.array([[0, 12], [-6, -8], [6, -8]])
        rot = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
        poly_rot = np.dot(poly, rot.T) + [px, py]
        ax.add_patch(patches.Polygon(poly_rot, facecolor=C_MIRV, edgecolor=C_TEXT, lw=2, zorder=13))
        
        # Atmospheric Heating Trail explicitly dynamically verified
        dist_c = np.linalg.norm(w['pos'] - EARTH_C)
        if dist_c < R_ATMOS:
            ax.plot([px, px - vx*4], [py, py - vy*4], color=C_BURN, lw=4, solid_capstyle='round', zorder=12)

    # Active ICBM Thrust Vehicles
    for b in r_boost:
        px, py = b.pos[0], b.pos[1]
        ang = np.radians(b.pitch) - np.pi/2
        poly = np.array([[-10, 30], [10, 30], [10, -30], [-10, -30]])
        rot = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
        poly_rot = np.dot(poly, rot.T) + [px, py]
        ax.add_patch(patches.Polygon(poly_rot, facecolor=C_CRANE, edgecolor=C_TEXT, lw=2, zorder=14))
        
        vx, vy = b.vel[0], b.vel[1]
        p_x, p_y = px - np.sin(ang)*35, py - np.cos(ang)*35
        ax.scatter([p_x], [p_y], s=150, color=C_BURN, zorder=13)
        ax.plot([p_x, p_x - vx*3], [p_y, p_y - vy*3], color=C_BURN, lw=6, solid_capstyle='round', zorder=12)
        
    # Dead Boosters tumbling in vacuum
    for db in r_dead:
        px, py = db['pos'][0], db['pos'][1]
        ang = np.arctan2(db['vel'][1], db['vel'][0]) - np.pi/2
        poly = np.array([[-10, 30], [10, 30], [10, -30], [-10, -30]])
        rot = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
        poly_rot = np.dot(poly, rot.T) + [px, py]
        ax.add_patch(patches.Polygon(poly_rot, facecolor=C_STEEL, alpha=0.3, zorder=14))

    # 5. SPALLATION DEBRIS & REENTRY HEATING
    if len(dx) > 0:
        c_deb = np.zeros((len(dx), 4))
        c_deb[:, :3] = np.array(mcol.to_rgb(C_TEXT))
        # Visualise intense red heat for fragments entering atmosphere
        c_deb[dhot, :3] = np.array(mcol.to_rgb(C_BURN))
        c_deb[:, 3] = dl 
        ax.scatter(dx, dy, s=dl*20, c=c_deb, edgecolors='none', zorder=18)

    # 6. ABSOLUTE DAYLIGHT TELEMETRY 
    ax.add_patch(plt.Rectangle((0, 0.90), 1, 0.10, transform=ax.transAxes, facecolor=C_BG, zorder=80))
    ax.plot([0, 1], [0.90, 0.90], transform=ax.transAxes, color=C_TEXT, lw=6, zorder=81)
    
    ax.text(0.04, 0.965, "STRATEGIC DEFENCE INITIATIVE (SDI)", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=82)
    
    if weapons_free:
        hdr_txt = "PHASE 2 // PLANETARY DIRECTED ENERGY MATRIX"
        hdr_col = C_LASER
    else:
        hdr_txt = "PHASE 1 // PLANETARY MACRO-SURVEILLANCE"
        hdr_col = C_TRACK
        
    ax.text(0.04, 0.930, hdr_txt, transform=ax.transAxes, color=hdr_col, fontsize=15, fontname='monospace', weight='bold', va='center', zorder=82)

    # Bottom Display
    ax.add_patch(plt.Rectangle((0, 0), 1, 0.12, transform=ax.transAxes, facecolor=C_BG, zorder=80))
    ax.plot([0, 1], [0.12, 0.12], transform=ax.transAxes, color=C_TEXT, lw=6, zorder=81)
    
    n_b = len(r_boost)
    n_w = len(r_mirv)
    n_d = len(r_decoy)
    n_deb = len(dx)
    
    if not weapons_free:
        if n_b > 0 and n_w == 0: ui_msg = "[STATE: LAUNCH ALARM DETECTED]"
        else: ui_msg = "[STATE: SUBORBITAL TRACKING ACTIVE]"
        ui_color = C_TRACK
    else:
        if len(r_lasers) > 0: ui_msg = "[STATE: INTERCEPT IN PROGRESS]"
        elif n_b == 0 and n_w == 0 and t > 10.0: ui_msg = "[STATE: CONTINENTAL SKY CLEAR]"
        else: ui_msg = "[STATE: WEAPONS FREE // RE-ACQUIRING]"
        ui_color = C_LASER if len(r_lasers) > 0 else (C_LOCK if "CLEAR" in ui_msg else C_TEXT)

    ax.text(0.04, 0.085, f"HEAVY BOOSTERS : {n_b:02.0f}", transform=ax.transAxes, color=C_CRANE, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(0.04, 0.055, f"EXO-WARHEADS   : {n_w:02.0f}", transform=ax.transAxes, color=C_MIRV, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(0.04, 0.025, f"DECOY / DEBRIS : {n_d + n_deb:04.0f}", transform=ax.transAxes, color=C_STEEL, fontsize=16, fontname='monospace', weight='bold', zorder=82)

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
    print(f"LG-106e: SDI MACRO PLANETARY MATRIX (DAYLIGHT) [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Planetary Gravity Tensors Locked. Stand by for compilation.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
