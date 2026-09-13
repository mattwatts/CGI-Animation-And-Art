"""
PROJECT: Logic Garden 106c (Exact Physical Construct // Strategic Defence Initiative)
FORMAT: YouTube Shorts (1080x1920)
METADATA: SDI, BALLISTICS, KINEMATIC INTERCEPT, DAYLIGHT
EXECUTION: 24.0s Sequence. True 2D High-Density Construct.
RULES ENFORCED:
- O(N) Particle Spallation for Kinematic Intercept Debris.
- Directed Energy 'Burn-Through' timing limits.
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
OUT_DIR = "frames_106c_star_wars"
os.makedirs(OUT_DIR, exist_ok=True)

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
C_LOCK      = '#00C853'          # Tracking Telemetry (Jade)

# ------------------------------------------------------------------
# O(1) FLIGHT KINEMATICS ENGINE
# ------------------------------------------------------------------
class Missile:
    def __init__(self, uid, x_pos, t_launch):
        self.id = uid
        self.pos = np.array([x_pos, -800.0])
        self.vel = np.array([np.random.uniform(-4.0, 4.0), 18.0])
        self.state = "BOOST"
        self.t_launch = t_launch
        self.warheads = []
        self.decoys = []
        self.health = 1.0

    def deploy_bus(self):
        self.state = "BUS_DEPLOY"
        # Deploy 3 MIRVs
        for i in range(3):
            drift = np.array([np.random.uniform(-3, 3), np.random.uniform(-1, 2)])
            self.warheads.append({'pos': self.pos.copy(), 'vel': self.vel + drift, 'health': 1.0})
        # Deploy 6 Decoys
        for i in range(6):
            drift = np.array([np.random.uniform(-5, 5), np.random.uniform(-2, 3)])
            self.decoys.append({'pos': self.pos.copy(), 'vel': self.vel + drift, 'health': 0.1}) # Decoys vaporise instantly

class SDISatellite:
    def __init__(self, uid, x_pos, y_pos):
        self.id = uid
        self.pos = np.array([x_pos, y_pos])
        self.base_x = x_pos
        self.target = None      # dict pointer to specific threat
        self.fire_timer = 0     # Burn-through timer
        self.cooldown = 0

def generate_stream():
    np.random.seed(106)

    missiles = []
    # Schedule launches over the first 5 seconds
    launch_schedule = [
        (0.5, -300), (1.2, 200), (2.0, -100),
        (2.8, 350),  (3.5, 0),   (4.8, -400)
    ]

    satellites = [
        SDISatellite(0, -350, 750), SDISatellite(1, -120, 800),
        SDISatellite(2,  120, 800), SDISatellite(3,  350, 750)
    ]

    # Spallation Engine
    N_DEBRIS = 5000
    d_x, d_y = np.zeros(N_DEBRIS), np.zeros(N_DEBRIS)
    d_vx, d_vy = np.zeros(N_DEBRIS), np.zeros(N_DEBRIS)
    d_life = np.zeros(N_DEBRIS)

    def spawn_debris(pos, base_vel, count, speed_fac=2.0):
        dead = np.where(d_life <= 0)[0]
        n_spawn = min(count, len(dead))
        if n_spawn > 0:
            idx = dead[:n_spawn]
            d_x[idx] = pos[0] + np.random.uniform(-10, 10, n_spawn)
            d_y[idx] = pos[1] + np.random.uniform(-10, 10, n_spawn)
            angs = np.random.uniform(0, 2*np.pi, n_spawn)
            spds = np.random.uniform(1.0, 5.0, n_spawn) * speed_fac
            d_vx[idx] = base_vel[0] + np.cos(angs) * spds
            d_vy[idx] = base_vel[1] + np.sin(angs) * spds
            d_life[idx] = 1.0

    for f in range(TOTAL_FRAMES):
        t = f / FPS

        # 1. Spawn Logic
        for tt, tx in launch_schedule:
            if abs(t - tt) < 0.01:
                missiles.append(Missile(len(missiles), tx, t))

        # 2. Update Threats
        threats_list = [] # For targeting

        for m in missiles:
            if m.state == "BOOST":
                m.pos += m.vel
                m.vel[1] -= 0.015 # Gravity
                threats_list.append({'obj': m, 'pos': m.pos, 'type': 'BOOST', 'uid': f"M_{m.id}"})

                # Deploy trigger
                if m.pos[1] > 100: m.deploy_bus()

            elif m.state == "BUS_DEPLOY":
                # Update payload physics
                for w in m.warheads:
                    if w['health'] > 0:
                        w['pos'] += w['vel']
                        w['vel'][1] -= 0.015
                        threats_list.append({'obj': w, 'pos': w['pos'], 'type': 'MIRV', 'uid': f"W_{m.id}_{id(w)}"})
                for d in m.decoys:
                    if d['health'] > 0:
                        d['pos'] += d['vel']
                        d['vel'][1] -= 0.015
                        threats_list.append({'obj': d, 'pos': d['pos'], 'type': 'DECOY', 'uid': f"D_{m.id}_{id(d)}"})

        # 3. SDI Engagement Matrix
        active_lasers = []

        for s in satellites:
            s.pos[0] = s.base_x + np.sin(t * 0.5 + s.id) * 30.0 # Slight patrol orbit
            s.pos[1] += np.cos(t * 0.3) * 0.1

            if s.cooldown > 0:
                s.cooldown -= 1
                s.target = None
                continue

            if s.target is None and len(threats_list) > 0:
                # Target lock priority: MIRV > BOOST > DECOY
                prio_map = {'MIRV': 1, 'BOOST': 2, 'DECOY': 3}
                # Filter targets inside engagement envelope (Y < s.pos[1])
                valid = [th for th in threats_list if th['pos'][1] < s.pos[1]]
                if valid:
                    # Sort by Priority, then Distance
                    valid.sort(key=lambda th: (prio_map[th['type']], np.linalg.norm(th['pos'] - s.pos)))
                    s.target = valid[0]
                    s.fire_timer = 20 if s.target['type'] != 'DECOY' else 5 # Decoys pop fast

            if s.target is not None:
                th_obj = s.target['obj']
                th_pos = s.target['pos']
                
                # RECTIFICATION: Object vs Dictionary Property Bridging
                is_dict = isinstance(th_obj, dict)
                hp = th_obj['health'] if is_dict else th_obj.health

                if hp > 0:
                    s.fire_timer -= 1
                    
                    # Compute structural damage
                    if is_dict:
                        th_obj['health'] -= 0.05
                        hp = th_obj['health']
                        vel = th_obj['vel']
                    else:
                        th_obj.health -= 0.05
                        hp = th_obj.health
                        vel = th_obj.vel
                        
                    active_lasers.append((s.pos.copy(), th_pos.copy()))

                    # Terminal Yield Check
                    if s.fire_timer <= 0 or hp <= 0:
                        if is_dict: th_obj['health'] = 0
                        else: th_obj.health = 0
                        
                        target_type = s.target['type']
                        s.target = None
                        s.cooldown = 15 # Rest optics
                        
                        # Violent Spallation
                        spawn_debris(th_pos, vel, 120 if target_type != 'DECOY' else 30)
                else:
                    s.target = None
                    s.cooldown = 5

        # 4. Spallation Tensor Update
        d_life -= 0.015
        d_x += d_vx
        d_y += d_vy
        d_vy -= 0.01 # Gravity fall

        act_d = np.where(d_life > 0)[0]

        # Freeze extraction arrays for rendering
        r_boost   = [m for m in missiles if m.state == "BOOST"]
        r_mirv    = [w for m in missiles for w in m.warheads if w['health'] > 0]
        r_decoy   = [d for m in missiles for d in m.decoys if d['health'] > 0]
        r_lasers  = active_lasers
        r_sats    = [s.pos.copy() for s in satellites]

        yield (f, t, r_boost, r_mirv, r_decoy, r_lasers, r_sats,
               np.copy(d_x[act_d]), np.copy(d_y[act_d]), np.copy(d_life[act_d]))

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t, r_boost, r_mirv, r_decoy, r_lasers, r_sats, dx, dy, dl = packet

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

    # Karman Line / Exo-atmosphere
    ax.plot([-540, 540], [0, 0], color=C_STEEL, lw=2, linestyle='dashed', zorder=2)
    ax.text(-520, 20, "EXOATMOSPHERIC INTERFACE (Y=0)", color=C_STEEL, fontsize=12, fontname='monospace', weight='bold', zorder=50)

    # 2. SDI PLATFORMS (Deep Marine Block Geometry)
    for p in r_sats:
        px, py = p[0], p[1]
        # Main chassis
        ax.add_patch(patches.Rectangle((px-15, py-10), 30, 20, facecolor=C_SDI, edgecolor=C_TEXT, lw=2, zorder=10))
        # Solar Arrays
        ax.add_patch(patches.Rectangle((px-55, py-5), 40, 10, facecolor=C_STEEL, edgecolor=C_TEXT, lw=1, zorder=9))
        ax.add_patch(patches.Rectangle((px+15, py-5), 40, 10, facecolor=C_STEEL, edgecolor=C_TEXT, lw=1, zorder=9))
        # Targeting Optic
        ax.add_patch(patches.Circle((px, py-10), 6, facecolor=C_LOCK, zorder=11))

    # 3. DIRECTED ENERGY TENSORS
    for L_start, L_end in r_lasers:
        # Core Beam
        ax.plot([L_start[0], L_end[0]], [L_start[1], L_end[1]], color=C_LASER, lw=8, zorder=4, solid_capstyle='round')
        # Core Heat
        ax.plot([L_start[0], L_end[0]], [L_start[1], L_end[1]], color=C_BG, lw=3, zorder=5, solid_capstyle='round')
        # Strike Bloom
        ax.add_patch(patches.Circle((L_end[0], L_end[1]), 25, facecolor=C_LASER, alpha=0.6, zorder=15))
        ax.add_patch(patches.Circle((L_end[0], L_end[1]), 10, facecolor=C_BG, zorder=16))

    # 4. THREAT MATRICES
    # A. Decoys (Lightweight Steel Blocks)
    for d in r_decoy:
        ax.add_patch(patches.Rectangle((d['pos'][0]-5, d['pos'][1]-5), 10, 10, facecolor=C_STEEL, edgecolor=C_TEXT, lw=1, zorder=12))

    # B. True Warheads (Deep Magenta Cones)
    for w in r_mirv:
        px, py = w['pos'][0], w['pos'][1]
        vx, vy = w['vel'][0], w['vel'][1]
        ang = np.arctan2(vy, vx) - np.pi/2 # Point along velocity
        poly = np.array([[0, 15], [-8, -10], [8, -10]])
        rot = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
        poly_rot = np.dot(poly, rot.T) + [px, py]
        ax.add_patch(patches.Polygon(poly_rot, facecolor=C_MIRV, edgecolor=C_TEXT, lw=2, zorder=13))

    # C. Boost Vehicles (Massive Carbon Cylinders)
    for b in r_boost:
        px, py = b.pos[0], b.pos[1]
        vx, vy = b.vel[0], b.vel[1]
        ang = np.arctan2(vy, vx) - np.pi/2
        poly = np.array([[-12, 40], [12, 40], [12, -40], [-12, -40]])
        rot = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
        poly_rot = np.dot(poly, rot.T) + [px, py]
        ax.add_patch(patches.Polygon(poly_rot, facecolor=C_CRANE, edgecolor=C_TEXT, lw=3, zorder=14))

        # Intense Red Kinematic Plume
        p_x, p_y = px - np.sin(ang)*45, py - np.cos(ang)*45
        ax.scatter([p_x], [p_y], s=250, color=C_BURN, zorder=13)
        ax.plot([p_x, p_x - vx*3], [p_y, p_y - vy*3], color=C_BURN, lw=8, solid_capstyle='round', zorder=12)

    # 5. SPALLATION DEBRIS
    if len(dx) > 0:
        c_deb = np.zeros((len(dx), 4))
        c_deb[:, :3] = np.array(mcol.to_rgb(C_TEXT))
        # Mix Red heat into new fragments
        hot_mask = dl > 0.7
        c_deb[hot_mask, :3] = np.array(mcol.to_rgb(C_BURN))
        c_deb[:, 3] = dl # Opacity tracks life
        ax.scatter(dx, dy, s=dl*30, c=c_deb, edgecolors='none', zorder=18)

    # 6. ABSOLUTE DAYLIGHT TELEMETRY
    ax.add_patch(plt.Rectangle((0, 0.90), 1, 0.10, transform=ax.transAxes, facecolor=C_BG, zorder=80))
    ax.plot([0, 1], [0.90, 0.90], transform=ax.transAxes, color=C_TEXT, lw=6, zorder=81)

    ax.text(0.04, 0.965, "STRATEGIC DEFENCE INITIATIVE (SDI)", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=82)
    ax.text(0.04, 0.930, "LG-106c // KINEMATIC INTERCEPT MATRIX", transform=ax.transAxes, color=C_SDI, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=82)

    ax.add_patch(plt.Rectangle((0, 0), 1, 0.12, transform=ax.transAxes, facecolor=C_BG, zorder=80))
    ax.plot([0, 1], [0.12, 0.12], transform=ax.transAxes, color=C_TEXT, lw=6, zorder=81)

    # Active Combat Status
    n_b = len(r_boost)
    n_w = len(r_mirv)
    n_d = len(r_decoy)

    # UI Tensors
    if n_b > 0 and n_w == 0: ui_msg = "[WARNING: MULTIPLE ASCENT VECTORS TRACKED]"
    elif n_w > 0 and len(r_lasers) == 0: ui_msg = "[BUS DEPLOYMENT DETECTED // TARGETING ACTIVE]"
    elif len(r_lasers) > 0: ui_msg = "[ENGAGEMENT: DIRECTED ENERGY TRANSFER]"
    elif n_b == 0 and n_w == 0 and t > 8.0: ui_msg = "[THREAT NEUTRALIZED // SKY CLEAR]"
    else: ui_msg = "[AWAITING TELEMETRY]"

    ax.text(0.04, 0.085, f"HEAVY BOOSTERS : {n_b:02.0f}", transform=ax.transAxes, color=C_CRANE, fontsize=18, fontname='monospace', weight='bold', zorder=82)
    ax.text(0.04, 0.055, f"EXO-WARHEADS   : {n_w:02.0f}", transform=ax.transAxes, color=C_MIRV, fontsize=18, fontname='monospace', weight='bold', zorder=82)
    ax.text(0.04, 0.025, f"DECOY CHAFF    : {n_d:02.0f}", transform=ax.transAxes, color=C_STEEL, fontsize=18, fontname='monospace', weight='bold', zorder=82)

    ui_color = C_LOCK if "NEUTRALIZED" in ui_msg else (C_BURN if "ENGAGEMENT" in ui_msg else C_TEXT)
    pulse = ui_color if (f % 30 < 20) else C_BG
    ax.text(0.96, 0.055, ui_msg, transform=ax.transAxes, color=pulse, fontsize=16, fontname='monospace', weight='bold', ha='right', va='center', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-106c: STRATEGIC DEFENCE INITIATIVE (DAYLIGHT) [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Orbital Intercept Mechanics Locked. Stand by for compilation.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
