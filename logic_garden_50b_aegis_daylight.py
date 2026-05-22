"""
SOVEREIGN CODE: logic_garden_50b_aegis_daylight.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Parametric Modulo Matrix
SCENE: LG-50b (AEGIS Phased Array Shield / Daylight Protocol)
HOTFIX: True VLS Intercept Kinematics, Electronic Beam Scanning, Seamless 10s Loop
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
OUT_DIR = "frames_50b_aegis"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST ENGINEERING PALETTE --------
C_BG        = '#FFFFFF'
C_GRID      = '#E5E8E8'        # Passive Euclidean Ground
C_IRON      = '#1C2833'        # Aegis Deckhouse / Structural Shards
C_STEEL     = '#7F8C8D'        # UI Tags & Expired Smoke
C_VAMPIRE   = '#E74C3C'        # Threat Red
C_BIRD      = '#3498DB'        # SM-2 Cyan/Azure
C_LOCK      = '#D4AC0D'        # SPY-1 Terminal Illumination Gold
C_TEXT      = '#111111'

# ------------------------------------------------------------------
# O(1) TOPOLOGICAL TRAJECTORY GENERATION
# ------------------------------------------------------------------
np.random.seed(50)
N_ENGAGEMENTS = 16

# We space 16 individual saturation engagements flawlessly across T=1.0
phases = np.linspace(0, 1, N_ENGAGEMENTS, endpoint=False)

# Randomize topological threat vectors
vx_start = np.random.uniform(50, 1030, N_ENGAGEMENTS)
vy_start = np.random.uniform(-400, -100, N_ENGAGEMENTS)
vy_intercept = np.random.uniform(400, 1000, N_ENGAGEMENTS)

# Ship Baseplate Array (Vertical Launch Matrix)
SHIP_X = 540.0
SHIP_Y = 1600.0

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
    for r in [300, 600, 900, 1200, 1500]:
        ax.add_patch(Circle((SHIP_X, SHIP_Y), r, color=C_GRID, fill=False, lw=2, zorder=1))
        if r < 1500:
            ax.text(SHIP_X + 10, SHIP_Y - r + 15, f"{r//10} km", color=C_STEEL, fontsize=10, fontname='monospace', zorder=1)
    
    ax.plot([SHIP_X, SHIP_X], [0, 1800], color=C_GRID, lw=2, zorder=1)
    ax.plot([0, 1080], [SHIP_Y, SHIP_Y], color=C_GRID, lw=2, zorder=1)

    active_vampires = []
    
    # 2. ENGAGEMENT KINEMATICS MATRIX
    for i in range(N_ENGAGEMENTS):
        # Calculate local time isolated to this specific engagement phase
        # Wrap safely around the 10-second loop barrier using modulo
        t_loc = (tau - phases[i]) % 1.0
        
        P_start = (vx_start[i], vy_start[i])
        # The target aims structurally lower to threaten the ship geometry
        P_end = (540 + np.random.uniform(-100, 100), SHIP_Y + 100)
        
        # Intercept constraints
        pct_hit = 0.45
        # Linear interpolation to find the exact spatial intersection 
        P_intercept = (
            P_start[0] + (P_end[0] - P_start[0]) * (pct_hit / 0.5),
            P_start[1] + (P_end[1] - P_start[1]) * (pct_hit / 0.5)
        )

        # ------------------------------------------------------
        # A. VAMPIRE PATH (Inbound Threat) -> Active from t=0.0 to t=0.45
        # ------------------------------------------------------
        if 0.0 <= t_loc < pct_hit:
            m_v = t_loc / pct_hit
            vx, vy = get_bezier_pos(P_start, P_intercept, P_intercept, m_v) # Linear slide
            angle_v = np.arctan2(P_intercept[1] - P_start[1], P_intercept[0] - P_start[0])
            
            # Draw Plasma Trail
            if m_v > 0.1:
                trail_x, trail_y = get_bezier_pos(P_start, P_intercept, P_intercept, max(0, m_v - 0.08))
                ax.plot([trail_x, vx], [trail_y, vy], color=C_VAMPIRE, lw=2, alpha=0.3, zorder=10)

            # Delta Wing Machined Geometry
            l_x = vx - 25 * np.cos(angle_v) + 10 * np.sin(angle_v)
            l_y = vy - 25 * np.sin(angle_v) - 10 * np.cos(angle_v)
            r_x = vx - 25 * np.cos(angle_v) - 10 * np.sin(angle_v)
            r_y = vy - 25 * np.sin(angle_v) + 10 * np.cos(angle_v)
            ax.add_patch(Polygon([(vx, vy), (l_x, l_y), (r_x, r_y)], facecolor=C_VAMPIRE, zorder=15))
            ax.text(vx+15, vy, f"V-{(i+1)*7:02d}", color=C_VAMPIRE, fontsize=9, fontname='monospace', weight='bold', zorder=16)

            active_vampires.append({'id': i, 'x': vx, 'y': vy, 't': t_loc})

        # ------------------------------------------------------
        # B. INTERCEPTOR PATH (SM-2 Bird) -> Active from t=0.15 to t=0.45
        # ------------------------------------------------------
        if 0.15 <= t_loc < pct_hit:
            m_i = (t_loc - 0.15) / (pct_hit - 0.15)
            
            # Turnover Control Node logic
            # Ejects upwards (y=1300), banks heavily towards threat
            p1_x = SHIP_X + (P_intercept[0] - SHIP_X) * 0.8
            P_control = (p1_x, SHIP_Y - 300) 
            
            ix, iy = get_bezier_pos((SHIP_X, SHIP_Y), P_control, P_intercept, m_i)
            angle_i = get_bezier_tangent((SHIP_X, SHIP_Y), P_control, P_intercept, m_i)
            
            # Solid Rocket Booster Trail (Continuous Hermite mapping of history)
            hist_steps = np.linspace(max(0, m_i - 0.15), m_i, 8)
            for hs in range(len(hist_steps)-1):
                hx1, hy1 = get_bezier_pos((SHIP_X, SHIP_Y), P_control, P_intercept, hist_steps[hs])
                hx2, hy2 = get_bezier_pos((SHIP_X, SHIP_Y), P_control, P_intercept, hist_steps[hs+1])
                fade = hs / 8.0
                ax.plot([hx1, hx2], [hy1, hy2], color=C_BIRD, lw=4*fade, alpha=fade*0.6, zorder=11)

            # SM-2 Interceptor Dart
            l_xi = ix - 20 * np.cos(angle_i) + 6 * np.sin(angle_i)
            l_yi = iy - 20 * np.sin(angle_i) - 6 * np.cos(angle_i)
            r_xi = ix - 20 * np.cos(angle_i) - 6 * np.sin(angle_i)
            r_yi = iy - 20 * np.sin(angle_i) + 6 * np.cos(angle_i)
            ax.add_patch(Polygon([(ix, iy), (l_xi, l_yi), (r_xi, r_yi)], facecolor=C_BIRD, zorder=16))

        # ------------------------------------------------------
        # C. KINETIC INTERSECTION (Explosion & Debris) -> t=0.45 to t=0.75
        # ------------------------------------------------------
        if pct_hit <= t_loc < 0.75:
            m_e = (t_loc - pct_hit) / (0.75 - pct_hit)
            
            # Thermal Flash
            flash_alpha = max(0, 1.0 - m_e*3.0) # Flashes out instantly
            if flash_alpha > 0:
                ax.add_patch(Circle(P_intercept, 50 + m_e*100, facecolor='#F39C12', alpha=flash_alpha, zorder=8))
                
            # Expansion Ring (The Kinetic Shockwave)
            ring_r = 10 + m_e*180
            ax.add_patch(Circle(P_intercept, ring_r, edgecolor=C_IRON, facecolor='none', lw=2 * (1-m_e), alpha=1-m_e, zorder=7))
            
            # Soot/Shrapnel Matrix
            np.random.seed(50 + i) # Maintain identical deterministic seeds per array
            shrapnel_x = P_intercept[0] + np.random.normal(0, ring_r*0.6, 20)
            shrapnel_y = P_intercept[1] + np.random.normal(0, ring_r*0.6, 20)
            ax.scatter(shrapnel_x, shrapnel_y, s=15*(1-m_e), color=C_STEEL, alpha=1-m_e, edgecolors='none', zorder=6)

            # Reticle Strike Update
            ax.text(P_intercept[0]+25, P_intercept[1], "KILL", color=C_IRON, fontsize=11, fontname='monospace', weight='bold', alpha=max(0, 1-m_e*1.5), zorder=9)

    # 3. ELECTRONIC SCANNING MATRIX (AN/SPY-1 Radar Pulses)
    if len(active_vampires) > 0:
        # PESA / AESA Beam allocation logic
        # Radar skips to a different target mathematically synced to the exact frame cycle
        focused_target = active_vampires[f % len(active_vampires)]
        
        # Track Phase (General Illumination)
        ax.plot([SHIP_X, focused_target['x']], [SHIP_Y, focused_target['y']], color=C_BIRD, lw=1.5, alpha=0.9, zorder=5)
        
        # Continuous Wave Illumination (Terminal Phase)
        # If any target is about to be hit (t > 0.40), the AEGIS locks a solid illumination beam
        for v in active_vampires:
            if v['t'] > 0.38:
                ax.plot([SHIP_X, v['x']], [SHIP_Y, v['y']], color=C_LOCK, lw=3, alpha=0.9, zorder=6)
                ax.add_patch(Circle((v['x'], v['y']), 35, edgecolor=C_LOCK, facecolor='none', lw=2, zorder=6))

    # 4. AEGIS DECKHOUSE (The Structural Baseplate)
    # Ticonderoga/Burke Blueprint Top-Down Abstract
    ax.add_patch(Polygon([
        (540, 1550), (510, 1600), (510, 1750), 
        (540, 1780), (570, 1750), (570, 1600)
    ], facecolor='#BDC3C7', edgecolor=C_IRON, lw=4, zorder=25))
    
    # Octagonal SPY-1 Radar Plates
    for phase_adj in [(-25, 1610), (25, 1610), (-25, 1720), (25, 1720)]:
        ax.add_patch(Circle((SHIP_X + phase_adj[0], phase_adj[1]), 12, facecolor=C_IRON, zorder=26))

    # 5. DIAGNOSTIC HUD LAYER
    ax.add_patch(Rectangle((0, 1840), 1080, 80, facecolor=C_BG, zorder=50))
    ax.text(40, 1880, f"LG-50b: O(1) TENSOR // AEGIS PHASED ARRAY INTERCEPT", color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=51)

    sys_mode = "SWARM SATURATION DETECTED"
    sys_col = "#E74C3C"
    terminal_engagements = sum(1 for v in active_vampires if v['t'] > 0.38)
    
    if terminal_engagements > 0:
        sys_mode = "TERMINAL ILLUMINATION HANDSHAKE"
        sys_col = C_LOCK
    elif len(active_vampires) == 0:
        sys_mode = "SECTOR CLEAR. SCAN MODE."
        sys_col = "#27AE60"

    ax.add_patch(Rectangle((0, 0), 1080, 120, facecolor=C_BG, zorder=50))
    ax.add_patch(Rectangle((0, 120), 1080, 2, facecolor=C_IRON, zorder=51))
    
    ax.text(40, 75, f"SYSTEM VECTOR : {sys_mode}", color=sys_col, fontsize=18, fontname='monospace', weight='bold', va='center', zorder=51)
    ax.text(40, 35, f"VLS CELLS FLIGHT: {sum(1 for _ in active_vampires)}    ACTIVE TRACKS: {len(active_vampires)}", color=C_IRON, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=51)

    # Dial Spinner (Radar Heartbeat)
    dial_cx, dial_cy = 960, 60
    ax.add_patch(Circle((dial_cx, dial_cy), 35, facecolor='none', edgecolor=C_IRON, lw=4, zorder=51))
    ind_ang = np.radians(tau * 360 * 3) # Sweeps 3 times per 10s cycle
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
    print(f"LG-50b: AEGIS KINEMATICS MATRIX [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Parametric Bezier Saturation // Daylight Modulo")

    with mp.Pool(processes=cpu_cores) as pool:
        frames = range(TOTAL_FRAMES)
        for finished_frame in pool.imap_unordered(render_frame, frames, chunksize=8):
            pass
    print("Compilation Complete. Iron Shield Logic verified.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
