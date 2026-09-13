"""
SOVEREIGN CODE: logic_garden_50e_aegis_omni.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Parametric Modulo Matrix
SCENE: LG-50e (AEGIS Omnidirectional Intercept / Daylight Protocol)
HOTFIX: 360-Degree Threat Saturation, Core Deckhouse Anchor, Seamless 10s Loop
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Rectangle
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 10.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_50e_aegis"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST ENGINEERING PALETTE --------
C_BG        = '#FFFFFF'
C_GRID      = '#E5E8E8'        # Passive Euclidean Ground
C_IRON      = '#1C2833'        # Aegis Deckhouse / Structural Shards
C_STEEL     = '#7F8C8D'        # UI Tags & Ordnance Hull
C_VAMPIRE   = '#E74C3C'        # Threat Red
C_BIRD      = '#3498DB'        # SM-2 Interceptor Blue
C_LOCK      = '#D4AC0D'        # Terminal Illumination Gold
C_TEXT      = '#111111'

# ------------------------------------------------------------------
# O(1) TOPOLOGICAL TRAJECTORY GENERATION
# ------------------------------------------------------------------
np.random.seed(505) # Specific seed for beautiful 360 distribution
N_ENGAGEMENTS = 32

# Flawless staggering of 32 threats across T=1.0 loop cycle
phases = np.linspace(0, 1, N_ENGAGEMENTS, endpoint=False)

# Threat Origins (360 Degree Saturation)
threat_angles = np.random.uniform(0, 2 * np.pi, N_ENGAGEMENTS)
spawn_radius = 1200.0
vx_start = 540.0 + spawn_radius * np.cos(threat_angles)
vy_start = 960.0 + spawn_radius * np.sin(threat_angles)

# Ship Baseplate Array (Central Anchor)
SHIP_X = 540.0
SHIP_Y = 960.0

def get_bezier_pos(p0, p1, p2, m):
    """Calculates instantaneous position along quadratic Hermite spline"""
    bx = (1-m)**2 * p0[0] + 2*(1-m)*m * p1[0] + m**2 * p2[0]
    by = (1-m)**2 * p0[1] + 2*(1-m)*m * p1[1] + m**2 * p2[1]
    return bx, by

def get_bezier_tangent(p0, p1, p2, m):
    """Calculates first derivative of trajectory for aerodynamic yaw alignment"""
    tx = 2*(1-m)*(p1[0] - p0[0]) + 2*m*(p2[0] - p1[0])
    ty = 2*(1-m)*(p1[1] - p0[1]) + 2*m*(p2[1] - p1[1])
    return np.arctan2(ty, tx)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (Parametric Timeline)
# ------------------------------------------------------------------
def render_frame(f):
    tau = f / float(TOTAL_FRAMES) # Global loop progress (0.0 -> 1.0)

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    fig.patch.set_facecolor(C_BG)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    # 1. THE RADAR GRID
    # Passive Operations Topography
    for r in [300, 600, 900]:
        ax.add_patch(Circle((SHIP_X, SHIP_Y), r, color=C_GRID, fill=False, lw=2, zorder=1))
        ax.text(SHIP_X + 10, SHIP_Y - r + 15, f"{r//10} km", color=C_STEEL, fontsize=10, fontname='monospace', zorder=1)

    ax.plot([SHIP_X, SHIP_X], [0, 1920], color=C_GRID, lw=2, zorder=1)
    ax.plot([0, 1080], [SHIP_Y, SHIP_Y], color=C_GRID, lw=2, zorder=1)

    active_threats = []

    # 2. ENGAGEMENT KINEMATICS MATRIX
    for i in range(N_ENGAGEMENTS):
        t_loc = (tau - phases[i]) % 1.0

        P_start = (vx_start[i], vy_start[i])
        # The target aims directly for the ship geometry
        P_end = (SHIP_X, SHIP_Y)

        # Intercept constraints
        pct_hit = 0.45
        # Linear interpolation to exact spatial intersection
        P_intercept = (
            P_start[0] + (P_end[0] - P_start[0]) * (pct_hit / 0.5),
            P_start[1] + (P_end[1] - P_start[1]) * (pct_hit / 0.5)
        )

        # ------------------------------------------------------
        # A. HOSTILE VECTOR (Inbound Threat) -> t=0.0 to t=0.45
        # ------------------------------------------------------
        if 0.0 <= t_loc < pct_hit:
            m_v = t_loc / pct_hit
            vx, vy = get_bezier_pos(P_start, P_intercept, P_intercept, m_v) 
            angle_v = np.arctan2(P_intercept[1] - P_start[1], P_intercept[0] - P_start[0])

            if m_v > 0.05:
                trail_x, trail_y = get_bezier_pos(P_start, P_intercept, P_intercept, max(0, m_v - 0.06))
                ax.plot([trail_x, vx], [trail_y, vy], color=C_VAMPIRE, lw=2, alpha=0.3, zorder=10)

            # Delta Wing Machined Geometry
            l_x = vx - 22 * np.cos(angle_v) + 8 * np.sin(angle_v)
            l_y = vy - 22 * np.sin(angle_v) - 8 * np.cos(angle_v)
            r_x = vx - 22 * np.cos(angle_v) - 8 * np.sin(angle_v)
            r_y = vy - 22 * np.sin(angle_v) + 8 * np.cos(angle_v)
            ax.add_patch(Polygon([(vx, vy), (l_x, l_y), (r_x, r_y)], facecolor=C_VAMPIRE, zorder=15))
            ax.text(vx+15, vy+10, f"H-{(i+1):02d}", color=C_VAMPIRE, fontsize=9, fontname='monospace', weight='bold', zorder=16)

            active_threats.append({'id': i, 'x': vx, 'y': vy, 't': t_loc})

        # ------------------------------------------------------
        # B. INTERCEPTOR VECTOR (SM-2 Burst) -> t=0.15 to t=0.45
        # ------------------------------------------------------
        if 0.15 <= t_loc < pct_hit:
            m_i = (t_loc - 0.15) / (pct_hit - 0.15)
            
            # Select VLS Cell (Forward or Aft depending on approach angle)
            vls_y = SHIP_Y + 40 if vy_start[i] > SHIP_Y else SHIP_Y - 40
            P_vls = (SHIP_X, vls_y)

            # Turnover Control Node logic
            # Simulates vertical launch and aggressive lateral pitch-over
            pitch_dist = 180.0
            P_control = (
                P_vls[0] + np.cos(threat_angles[i]) * pitch_dist,
                P_vls[1] + np.sin(threat_angles[i]) * pitch_dist
            )

            ix, iy = get_bezier_pos(P_vls, P_control, P_intercept, m_i)
            angle_i = get_bezier_tangent(P_vls, P_control, P_intercept, m_i)

            # Solid Rocket Booster Trail (Continuous Hermite mapping of history)
            hist_steps = np.linspace(max(0, m_i - 0.10), m_i, 10)
            for hs in range(len(hist_steps)-1):
                hx1, hy1 = get_bezier_pos(P_vls, P_control, P_intercept, hist_steps[hs])
                hx2, hy2 = get_bezier_pos(P_vls, P_control, P_intercept, hist_steps[hs+1])
                fade = hs / 10.0
                ax.plot([hx1, hx2], [hy1, hy2], color=C_BIRD, lw=4*fade, alpha=fade*0.6, zorder=11)

            # SM-2 Interceptor Dart
            l_xi = ix - 18 * np.cos(angle_i) + 5 * np.sin(angle_i)
            l_yi = iy - 18 * np.sin(angle_i) - 5 * np.cos(angle_i)
            r_xi = ix - 18 * np.cos(angle_i) - 5 * np.sin(angle_i)
            r_yi = iy - 18 * np.sin(angle_i) + 5 * np.cos(angle_i)
            ax.add_patch(Polygon([(ix, iy), (l_xi, l_yi), (r_xi, r_yi)], facecolor=C_BIRD, zorder=16))

        # ------------------------------------------------------
        # C. KINETIC INTERSECTION (Detonation) -> t=0.45 to t=0.75
        # ------------------------------------------------------
        if pct_hit <= t_loc < 0.75:
            m_e = (t_loc - pct_hit) / (0.75 - pct_hit)

            # Thermal Flash
            flash_alpha = max(0, 1.0 - m_e*4.0) 
            if flash_alpha > 0:
                ax.add_patch(Circle(P_intercept, 40 + m_e*100, facecolor='#E67E22', alpha=flash_alpha, zorder=8))

            # Expanding Shockwave Overpressure Ring
            ring_r = 10 + m_e*150
            ax.add_patch(Circle(P_intercept, ring_r, edgecolor=C_IRON, facecolor='none', lw=2 * (1-m_e), alpha=1-m_e, zorder=7))

            # Spallation Fragments / Debris Matrix
            np.random.seed(505 + i) 
            shrapnel_x = P_intercept[0] + np.random.normal(0, ring_r*0.5, 25)
            shrapnel_y = P_intercept[1] + np.random.normal(0, ring_r*0.5, 25)
            ax.scatter(shrapnel_x, shrapnel_y, s=12*(1-m_e), color=C_STEEL, alpha=1-m_e, edgecolors='none', zorder=6)

            # Execution Readout
            ax.text(P_intercept[0]+20, P_intercept[1]+20, "INTERCEPT", color=C_IRON, fontsize=10, fontname='monospace', weight='bold', alpha=max(0, 1-m_e*1.5), zorder=9)

    # 3. ELECTRONIC SCANNING MATRIX (AN/SPY-1 Duty Cycles)
    if len(active_threats) > 0:
        # PESA / AESA Beam allocation logic
        # Micro-second scanning flashes to distinct targets in sequence
        focused_target = active_threats[f % len(active_threats)]

        # Broad Track Phase Illumination
        ax.plot([SHIP_X, focused_target['x']], [SHIP_Y, focused_target['y']], color=C_BIRD, lw=1.5, alpha=0.9, zorder=5)

        # Terminal Phase Continuous Wave Illumination
        for v in active_threats:
            if v['t'] > 0.38:
                ax.plot([SHIP_X, v['x']], [SHIP_Y, v['y']], color=C_LOCK, lw=3, alpha=0.8, zorder=6)
                ax.add_patch(Circle((v['x'], v['y']), 30, edgecolor=C_LOCK, facecolor='none', lw=2, zorder=6))

    # 4. AEGIS DESTROYER (The Central Sovereign Anchor)
    # Forward Hull
    ax.add_patch(Polygon([
        (SHIP_X, SHIP_Y+120), (SHIP_X-20, SHIP_Y+70), 
        (SHIP_X-20, SHIP_Y-100), (SHIP_X+20, SHIP_Y-100), 
        (SHIP_X+20, SHIP_Y+70)], facecolor='#BDC3C7', edgecolor=C_IRON, lw=2, zorder=25))
    
    # Octagonal SPY-1 Deckhouse
    dh_rad = 18
    dh_pts = []
    for deg in range(22, 382, 45):
        dh_pts.append((SHIP_X + dh_rad * np.cos(np.radians(deg)), SHIP_Y + dh_rad * np.sin(np.radians(deg))))
    ax.add_patch(Polygon(dh_pts, facecolor=C_IRON, zorder=26))

    # VLS Grids (Forward and Aft)
    def draw_vls(cx, cy):
        ax.add_patch(Rectangle((cx-8, cy-12), 16, 24, facecolor=C_TEXT, zorder=26))
        for x_off in [-4, 4]:
            for y_off in [-8, 0, 8]:
                ax.add_patch(Rectangle((cx+x_off-2, cy+y_off-2), 4, 4, facecolor=C_GRID, zorder=27))

    draw_vls(SHIP_X, SHIP_Y+50)  # Forward VLS
    draw_vls(SHIP_X, SHIP_Y-40)  # Aft VLS

    # 5. DIAGNOSTIC HUD LAYER
    ax.add_patch(Rectangle((0, 1840), 1080, 80, facecolor=C_BG, zorder=50))
    ax.text(40, 1880, f"LG-50e: OMNIDIRECTIONAL O(1) TENSOR // AEGIS", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=51)

    sys_mode = "360-DEGREE SWARM SATURATION"
    sys_col = "#E74C3C"
    terminal_engagements = sum(1 for v in active_threats if v['t'] > 0.38)

    if terminal_engagements > 0:
        sys_mode = "TERMINAL ILLUMINATION HANDSHAKE"
        sys_col = C_LOCK
    elif len(active_threats) == 0:
        sys_mode = "SEARCH AND TRACK"
        sys_col = "#27AE60"

    ax.add_patch(Rectangle((0, 0), 1080, 120, facecolor=C_BG, zorder=50))
    ax.add_patch(Rectangle((0, 120), 1080, 3, facecolor=C_IRON, zorder=51))

    ax.text(40, 75, f"SYSTEM VECTOR : {sys_mode}", color=sys_col, fontsize=18, fontname='monospace', weight='bold', va='center', zorder=51)
    ax.text(40, 35, f"VLS VECTORS ACTIVE: {sum(1 for _ in active_threats):02d}    RADAR BEAMS: OMNI", color=C_IRON, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=51)

    # Dial Spinner (Radar Heartbeat)
    dial_cx, dial_cy = 960, 60
    ax.add_patch(Circle((dial_cx, dial_cy), 35, facecolor='none', edgecolor=C_IRON, lw=4, zorder=51))
    ind_ang = np.radians(tau * 360 * 4) # Sweeps 4 times per 10s cycle
    ax.plot([dial_cx, dial_cx + np.cos(ind_ang)*25], [dial_cy, dial_cy + np.sin(ind_ang)*25], color=C_IRON, lw=4, zorder=52)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-50e: AEGIS OMNIDIRECTIONAL KINEMATICS [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: 360-Degree Spherical Integration")

    with mp.Pool(processes=cpu_cores) as pool:
        frames = range(TOTAL_FRAMES)
        for finished_frame in pool.imap_unordered(render_frame, frames, chunksize=8):
            pass
    print("Compilation Complete. 360-Degree Anchor Locked.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
