"""
PROJECT: Logic Garden 106f (Exact Physical Construct // Macro-Global SDI)
FORMAT: YouTube Shorts (1080x1920)
METADATA: SDI, BALLISTICS, KINEMATIC INTERCEPT, RADIAL GRAVITY, DAYLIGHT
EXECUTION: 24.0s Sequence. True Suborbital Flight Paths & Intercept Modes.
RULES ENFORCED: 
- O(1) True Radial Newtonian Gravity (-GM/R^2).
- Bipartite Modalities: [BOOST-MODE] vs [ORBIT-MODE] Intercept Tracking.
- Macro-scale Planetary Geometry & Atmospheric Reentry Spallation.
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
OUT_DIR = "frames_106f_star_wars"
os.makedirs(OUT_DIR, exist_ok=True)

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
EARTH_C = np.array([0.0, -700.0])
R_EARTH = 600.0
R_ATMOS = 660.0
R_ORBIT = 1200.0
GM_CONST = 18000.0 # Tuned Gravitational Acceleration Factor

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
        self.pos = EARTH_C + np.array([R_EARTH * np.cos(rad_surf), R_EARTH * np.sin(rad_surf)])
        
        rad_v = np.radians(v_deg) 
        self.vel = np.array([v_mag * np.cos(rad_v), v_mag * np.sin(rad_v)])
        
        self.state = "BOOST"
        self.warheads = []
        self.decoys = []
        self.health = 1.0
        self.pitch = v_deg 

    def deploy_bus(self):
        self.state = "BUS_DEPLOY"
        # Deploy 3 True MIRVs
        for i in range(3):
            drift = np.array([np.random.uniform(-0.4, 0.4), np.random.uniform(-0.4, 0.4)])
            self.warheads.append({'pos': self.pos.copy(), 'vel': self.vel + drift, 'health': 1.0, 'id': i})
        # Deploy 6 Decoys
        for i in range(6):
            drift = np.array([np.random.uniform(-1.0, 1.0), np.random.uniform(-1.0, 1.0)])
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
        self.hit_pos = None
        self.hit_type = None

# ------------------------------------------------------------------
# PARALLEL GENERATOR (LOGIC TENSORS)
# ------------------------------------------------------------------
def generate_stream():
    np.random.seed(1066)
    
    missiles = []
    # Western Hemisphere suborbital launch coordinates 
    # [time, earth_deg, v_mag, flight_deg]
    launch_schedule = [
        # Wave 1 (Designed for Boost-Phase Intercept)
        (0.5, 137, 5.8, 62),  (1.2, 134, 5.6, 60), 
        # Wave 2 (Mixed Penetration)
        (3.0, 136, 5.5, 61),  (3.6, 133, 5.9, 64), (4.2, 131, 5.4, 60),
        # Wave 3 (Mass Deployment)
        (6.0, 138, 5.7, 63),  (6.5, 135, 6.0, 66), (7.0, 130, 5.6, 61),
        (7.8, 133, 5.8, 65)
    ]
    
    # 5 SDI Platforms spread across the northern orbital arc
    satellites = [
        SDISatellite(0, 125), SDISatellite(1, 105), # Western group (Optimised for Boost Mode)
        SDISatellite(2,  85), SDISatellite(3,  65), # Eastern group (Optimised for Orbit Mode)
        SDISatellite(4,  45)
    ]

    # Spallation Engine
    N_DEBRIS = 8000
    d_x, d_y = np.zeros(N_DEBRIS), np.zeros(N_DEBRIS)
    d_vx, d_vy = np.zeros(N_DEBRIS), np.zeros(N_DEBRIS)
    d_life = np.zeros(N_DEBRIS)
    d_hot = np.zeros(N_DEBRIS, dtype=bool) 
    
    intercept_markers = []
    stats = {'boost_kills': 0, 'orbit_kills': 0}

    def spawn_debris(pos, base_vel, count, is_fragile=False):
        dead = np.where(d_life <= 0)[0]
        n_spawn = min(count, len(dead))
        if n_spawn > 0:
            idx = dead[:n_spawn]
            d_x[idx] = pos[0] + np.random.uniform(-4, 4, n_spawn)
            d_y[idx] = pos[1] + np.random.uniform(-4, 4, n_spawn)
            angs = np.random.uniform(0, 2*np.pi, n_spawn)
            spd_multi = 0.5 if is_fragile else 1.5
            spds = np.random.uniform(0.5, 2.0, n_spawn) * spd_multi
            d_vx[idx] = base_vel[0] + np.cos(angs) * spds
            d_vy[idx] = base_vel[1] + np.sin(angs) * spds
            d_life[idx] = 1.0
            d_hot[idx] = False

    for f in range(TOTAL_FRAMES):
        t = f / FPS
        
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
                if dist_surf > R_ATMOS: 
                    m.deploy_bus()
                    dead_boosters.append({'pos': m.pos.copy(), 'vel': m.vel * 0.95})
                else:
                    threats_dict[f"M_{m.id}"] = {'obj': m, 'pos': m.pos, 'type': 'BOOST', 'vel': m.vel}
                    
            elif m.state == "BUS_DEPLOY":
                for w in m.warheads:
                    if w['health'] > 0:
                        w['vel'] += radial_gravity(w['pos'])
                        w['pos'] += w['vel']
                        dist_surf = np.linalg.norm(w['pos'] - EARTH_C)
                        if dist_surf < R_EARTH: w['health'] = 0 
                        else: threats_dict[f"MIRV_{m.id}_{w['id']}"] = {'obj': w, 'pos': w['pos'], 'type': 'MIRV', 'vel': w['vel']}
                
                for d in m.decoys:
                    if d['health'] > 0:
                        d['vel'] += radial_gravity(d['pos'])
                        d['pos'] += d['vel']
                        dist_surf = np.linalg.norm(d['pos'] - EARTH_C)
                        if dist_surf < R_ATMOS: 
                            d['health'] = 0 
                            spawn_debris(d['pos'], d['vel'], 5, True)
                        else:
                            threats_dict[f"DCY_{m.id}_{d['id']}"] = {'obj': d, 'pos': d['pos'], 'type': 'DECOY', 'vel': d['vel']}

        # 3. SDI Bipartite Engagement Matrix
        active_lasers = []
        
        for s in satellites:
            # Parametric orbital crawl
            orb_deg = s.base_deg - (t * 0.3) 
            rad_orb = np.radians(orb_deg)
            s.pos = EARTH_C + np.array([R_ORBIT * np.cos(rad_orb), R_ORBIT * np.sin(rad_orb)])
            
            s.hit_pos = None
            s.hit_type = None
            
            if s.target_uid not in threats_dict:
                s.target_uid = None
            
            # Target Acquisition
            if s.target_uid is None and s.cooldown <= 0 and len(threats_dict) > 0:
                valid = []
                for uid, th in threats_dict.items():
                    # Geometry mask: Can we visually see it over the Earth's curve?
                    th_dist_C = np.linalg.norm(th['pos'] - EARTH_C)
                    if th_dist_C > R_EARTH - 5: 
                        valid.append((uid, th))
                        
                if valid:
                    # Target selection logic based on hemispheric location
                    # Satellites >= 100 degrees prioritize Boost. Others prioritize Orbit.
                    if orb_deg >= 100:
                        prio_map = {'BOOST': 1, 'MIRV': 2, 'DECOY': 3}
                    else:
                        prio_map = {'MIRV': 1, 'BOOST': 2, 'DECOY': 3}
                        
                    valid.sort(key=lambda x: (prio_map[x[1]['type']], np.linalg.norm(x[1]['pos'] - s.pos)))
                    s.target_uid = valid[0][0]
                    s.fire_timer = 20 if valid[0][1]['type'] != 'DECOY' else 3
            
            # Execution
            if s.target_uid is not None:
                th_data = threats_dict[s.target_uid]
                th_obj = th_data['obj']
                th_pos = th_data['pos']
                
                is_dict = isinstance(th_obj, dict)
                hp = th_obj['health'] if is_dict else th_obj.health

                s.hit_pos = th_pos.copy()
                s.hit_type = th_data['type']
                active_lasers.append((s.pos.copy(), s.hit_pos.copy(), C_LASER if s.hit_type == 'BOOST' else C_LOCK))
                
                s.fire_timer -= 1
                
                if is_dict: th_obj['health'] -= 0.05
                else: th_obj.health -= 0.05
                hp -= 0.05
                
                if hp <= 0 or s.fire_timer <= 0:
                    if is_dict: th_obj['health'] = 0
                    else: th_obj.health = 0
                    
                    target_type = th_data['type']
                    s.target_uid = None
                    s.cooldown = 20 
                    
                    if target_type == 'BOOST':
                        stats['boost_kills'] += 1
                        intercept_markers.append({'pos': th_pos.copy(), 'type': 'BOOST-KILL', 'life': 2.0})
                    elif target_type == 'MIRV':
                        stats['orbit_kills'] += 1
                        intercept_markers.append({'pos': th_pos.copy(), 'type': 'ORBIT-KILL', 'life': 2.0})

                    spawn_debris(th_pos, th_data['vel'], 
                                 120 if target_type != 'DECOY' else 20, 
                                 target_type == 'DECOY')

            if s.cooldown > 0:
                s.cooldown -= 1

        # Fade markers
        active_markers = []
        for mrk in intercept_markers:
            mrk['life'] -= (1/FPS)
            if mrk['life'] > 0: active_markers.append(mrk)
        intercept_markers = active_markers

        # 4. Spallation Tensor Processing 
        act_d = np.where(d_life > 0)[0]
        
        for idx in act_d:
            vecC = np.array([d_x[idx], d_y[idx]]) - EARTH_C
            distC = np.linalg.norm(vecC)
            grav = -(GM_CONST / (distC**2)) * (vecC / distC)
            
            d_vx[idx] += grav[0]
            d_vy[idx] += grav[1]
            d_x[idx] += d_vx[idx]
            d_y[idx] += d_vy[idx]
            
            if distC < R_ATMOS:
                d_hot[idx] = True
                d_life[idx] -= 0.04 
                d_vx[idx] *= 0.94   
                d_vy[idx] *= 0.94
            else:
                d_hot[idx] = False
                d_life[idx] -= 0.015
                
            if distC < R_EARTH:
                d_life[idx] = 0 

        act_d = np.where(d_life > 0)[0]

        r_boost   = [m for m in missiles if m.state == "BOOST"]
        r_mirv    = [w for m in missiles for w in m.warheads if w['health'] > 0]
        r_decoy   = [d for m in missiles for d in m.decoys if d['health'] > 0]
        r_lasers  = active_lasers
        r_sats    = [s.pos.copy() for s in satellites]
        
        yield (f, t, stats, r_boost, r_mirv, r_decoy, r_lasers, r_sats, dead_boosters, intercept_markers,
               np.copy(d_x[act_d]), np.copy(d_y[act_d]), np.copy(d_life[act_d]), np.copy(d_hot[act_d]))

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t, stats, r_boost, r_mirv, r_decoy, r_lasers, r_sats, r_dead, intercept_markers, dx, dy, dl, dhot = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)

    # 1. MACRO PLANETARY ALIGNMENT
    ax.add_patch(patches.Circle((EARTH_C[0], EARTH_C[1]), R_EARTH, facecolor=C_EARTH, zorder=1))
    ax.add_patch(patches.Circle((EARTH_C[0], EARTH_C[1]), R_EARTH, fill=False, edgecolor=C_TEXT, lw=4, zorder=2))
    
    # Atmospheric Envelope (Exoatmospheric line)
    ax.add_patch(patches.Circle((EARTH_C[0], EARTH_C[1]), R_ATMOS, fill=False, edgecolor=C_STEEL, lw=2, linestyle='dashed', zorder=2))
    ax.text(0, R_ATMOS + EARTH_C[1] + 10, "EXOATMOSPHERIC INTERFACE (MACRO BOUNDARY)", 
            color=C_STEEL, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=50)

    # Launch pad indicators
    ax.plot([-460, -420], [-270, -270], color=C_STEEL, lw=3, zorder=5)
    ax.text(-470, -290, "WESTERN SUBORBITAL COMMAND", color=C_STEEL, fontsize=12, fontname='monospace', weight='bold', ha='left', rotation=30, zorder=50)

    # 2. SDI SURVEILLANCE PLATFORMS
    for p in r_sats:
        px, py = p[0], p[1]
        ang = np.degrees(np.arctan2(py - EARTH_C[1], px - EARTH_C[0])) - 90
        
        t1 = matplotlib.transforms.Affine2D().rotate_deg_around(px, py, ang) + ax.transData
        
        ax.add_patch(patches.Rectangle((px-8, py-5), 16, 10, facecolor=C_SDI, edgecolor=C_TEXT, lw=1.5, zorder=10, transform=t1))
        ax.add_patch(patches.Rectangle((px-25, py-2), 17, 4, facecolor=C_STEEL, edgecolor=C_TEXT, lw=1.0, zorder=9, transform=t1))
        ax.add_patch(patches.Rectangle((px+8, py-2), 17, 4, facecolor=C_STEEL, edgecolor=C_TEXT, lw=1.0, zorder=9, transform=t1))

    # 3. WEAPONS ENGAGEMENT & TRACKING
    for L_start, L_end, L_col in r_lasers:
        ax.plot([L_start[0], L_end[0]], [L_start[1], L_end[1]], color=L_col, lw=4, zorder=4, solid_capstyle='round')
        ax.plot([L_start[0], L_end[0]], [L_start[1], L_end[1]], color=C_BG, lw=1.5, zorder=5, solid_capstyle='round')
        ax.add_patch(patches.Circle((L_end[0], L_end[1]), 15, facecolor=L_col, alpha=0.6, zorder=15))

    # Explicit Tactical Intercept Markers
    for mrk in intercept_markers:
        alpha = np.clip(mrk['life'], 0.0, 1.0)
        col = C_LASER if mrk['type'] == 'BOOST-KILL' else C_LOCK
        tx, ty = mrk['pos'][0], mrk['pos'][1]
        ax.plot([tx-8, tx+8], [ty-8, ty+8], color=col, lw=2, alpha=alpha, zorder=19)
        ax.plot([tx-8, tx+8], [ty+8, ty-8], color=col, lw=2, alpha=alpha, zorder=19)
        ax.text(tx+15, ty, f"[{mrk['type']}]", color=col, fontsize=12, fontname='monospace', weight='bold', alpha=alpha, zorder=20)

    # 4. THREAT MATRICES (Macro Scale Vectors)
    for d in r_decoy:
        ax.add_patch(patches.Rectangle((d['pos'][0]-2, d['pos'][1]-2), 4, 4, facecolor=C_STEEL, edgecolor=C_TEXT, lw=1, zorder=12))

    for w in r_mirv:
        px, py = w['pos'][0], w['pos'][1]
        vx, vy = w['vel'][0], w['vel'][1]
        ang = np.arctan2(vy, vx) - np.pi/2 
        poly = np.array([[0, 8], [-4, -5], [4, -5]])
        rot = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
        poly_rot = np.dot(poly, rot.T) + [px, py]
        ax.add_patch(patches.Polygon(poly_rot, facecolor=C_MIRV, edgecolor=C_TEXT, lw=1, zorder=13))
        
        dist_c = np.linalg.norm(w['pos'] - EARTH_C)
        if dist_c < R_ATMOS:
            ax.plot([px, px - vx*4], [py, py - vy*4], color=C_BURN, lw=3, solid_capstyle='round', zorder=12)

    for b in r_boost:
        px, py = b.pos[0], b.pos[1]
        ang = np.radians(b.pitch) - np.pi/2
        poly = np.array([[-5, 15], [5, 15], [5, -15], [-5, -15]])
        rot = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
        poly_rot = np.dot(poly, rot.T) + [px, py]
        ax.add_patch(patches.Polygon(poly_rot, facecolor=C_CRANE, edgecolor=C_TEXT, lw=1.5, zorder=14))
        
        vx, vy = b.vel[0], b.vel[1]
        p_x, p_y = px - np.sin(ang)*18, py - np.cos(ang)*18
        ax.scatter([p_x], [p_y], s=50, color=C_BURN, zorder=13)
        ax.plot([p_x, p_x - vx*3], [p_y, p_y - vy*3], color=C_BURN, lw=4, solid_capstyle='round', zorder=12)
        
    for db in r_dead:
        px, py = db['pos'][0], db['pos'][1]
        ang = np.arctan2(db['vel'][1], db['vel'][0]) - np.pi/2
        poly = np.array([[-5, 15], [5, 15], [5, -15], [-5, -15]])
        rot = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
        poly_rot = np.dot(poly, rot.T) + [px, py]
        ax.add_patch(patches.Polygon(poly_rot, facecolor=C_STEEL, alpha=0.4, zorder=14))

    # 5. SPALLATION DEBRIS & REENTRY HEATING
    if len(dx) > 0:
        c_deb = np.zeros((len(dx), 4))
        c_deb[:, :3] = np.array(mcol.to_rgb(C_TEXT))
        c_deb[dhot, :3] = np.array(mcol.to_rgb(C_BURN))
        c_deb[:, 3] = dl 
        ax.scatter(dx, dy, s=dl*15, c=c_deb, edgecolors='none', zorder=18)

    # 6. ABSOLUTE DAYLIGHT TELEMETRY 
    ax.add_patch(plt.Rectangle((0, 0.90), 1, 0.10, transform=ax.transAxes, facecolor=C_BG, zorder=80))
    ax.plot([0, 1], [0.90, 0.90], transform=ax.transAxes, color=C_TEXT, lw=6, zorder=81)
    
    ax.text(0.04, 0.965, "STRATEGIC DEFENCE INITIATIVE (SDI)", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=82)
    ax.text(0.04, 0.930, "LG-106f // FULL CONTINENTAL SUBORBITAL TENSOR", transform=ax.transAxes, color=C_SDI, fontsize=15, fontname='monospace', weight='bold', va='center', zorder=82)

    # Bottom Display
    ax.add_patch(plt.Rectangle((0, 0), 1, 0.12, transform=ax.transAxes, facecolor=C_BG, zorder=80))
    ax.plot([0, 1], [0.12, 0.12], transform=ax.transAxes, color=C_TEXT, lw=6, zorder=81)
    
    n_b = len(r_boost)
    n_w = len(r_mirv)
    n_d = len(r_decoy)
    n_deb = len(dx)
    
    if len(r_lasers) > 0: ui_msg = "[STATE: ENGAGEMENT IN PROGRESS]"
    elif n_b == 0 and n_w == 0 and t > 12.0: ui_msg = "[STATE: CONTINENTAL SKY CLEAR]"
    else: ui_msg = "[STATE: SCANNING SUBOBRITAL ARC]"
    
    ui_color = C_BURN if len(r_lasers) > 0 else (C_LOCK if "CLEAR" in ui_msg else C_TEXT)

    ax.text(0.04, 0.085, f"BIPARTITE KINEMATIC SUCCESS RATIO:", transform=ax.transAxes, color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(0.04, 0.055, f"[BOOST-MODE INTERCEPTS] : {stats['boost_kills']:02.0f}", transform=ax.transAxes, color=C_LASER, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(0.04, 0.025, f"[ORBIT-MODE INTERCEPTS] : {stats['orbit_kills']:02.0f}", transform=ax.transAxes, color=C_LOCK, fontsize=16, fontname='monospace', weight='bold', zorder=82)

    pulse = ui_color if (f % 30 < 20) else C_BG
    ax.text(0.96, 0.055, ui_msg, transform=ax.transAxes, color=pulse, fontsize=18, fontname='monospace', weight='bold', ha='right', va='center', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-106f: SDI MACRO GLOBAL MATRIX (DAYLIGHT) [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Global Bipartite Engagement Tensors Locked. Stand by for compilation.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
