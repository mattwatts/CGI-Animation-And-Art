"""
PROJECT: Logic Garden 29b (Exact Physical Construct // The Suicide Burn)
FORMAT: YouTube Shorts (1080x1920)
METADATA: APOLLO 11, LUNAR DESCENT, SUICIDE BURN, DAYLIGHT
EXECUTION: 24.0s Sequence. True 3D Beveled Geometry. 
RULES ENFORCED: 
- 24.0 Second Continuous Approach (Braking -> Pitchover -> Touchdown).
- Realisational Aspect: High-velocity Cartesian background tracking.
- Daylight Palette (White Substrate / High-Contrast Solid Geometry).
- Purged Jargon. Australian spelling conventions.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle
import multiprocessing as mp
import os
import gc

# ======== SEQUENCE PARAMETERS ========
DURATION = 24.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_29b_suicide_burn"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'        # Pure White Daylight Array
C_MOON      = '#E5E8E8'        # Clinical Grey Regolith Matrix
C_CRATER    = '#95A5A6'        # Topographic Depressions
C_GOLD      = '#D4AC0D'        # Kapton Mylar Foil
C_FOIL_D    = '#B9770E'        # Shadowed Foil
C_ALUM      = '#BDC3C7'        # Machined Ascent Stage
C_WINDOW    = '#1C2833'        # Pressure Viewport
C_ENGINE    = '#17202A'        # Carbon-scored Nozzle
C_STRUT     = '#7F8C8D'        # Titanium Landing Gear
C_TEXT      = '#111115'        # Telemetry Text
C_GUI_OK    = '#00C853'        # Jade Green (Systems Nominal)
C_GUI_WARN  = '#FFB300'        # Dense Amber (Braking)

# Plume Tensors
C_PLUME_1   = np.array([0.0, 1.0, 1.0])    # High-Velocity Thrust Base
C_PLUME_2   = np.array([0.2, 0.6, 0.9])    # Core Blue Heat
C_DUST      = np.array([0.4, 0.4, 0.4])    # Abrasive Silicate Regolith

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE KINEMATIC CAMERA & GROUND MATRIX
# ------------------------------------------------------------------
CX, CY_GND = 0.0, -500.0  # Ground locked in lower frame

N_PLUME = 4000
N_DUST  = 8000

# Base Topography for infinitely scrolling surface
CRATER_N = 100
cp_x = np.random.uniform(-2000, 4000, CRATER_N)
cp_w = np.random.uniform(50, 200, CRATER_N)
cp_d = np.random.uniform(10, 50, CRATER_N)

# ------------------------------------------------------------------
# MODULE GEOMETRY CONSTRUCT (Exact Physical Construct)
# ------------------------------------------------------------------
def rotate_coord(x, y, pitch_deg):
    theta = np.radians(pitch_deg)
    c, s = np.cos(theta), np.sin(theta)
    return x * c - y * s, x * s + y * c

def draw_lander(ax, l_x, l_y, pitch, thrust_lvl, alpha_val):
    def xf(x, y):
        rx, ry = rotate_coord(x, y, pitch)
        return l_x + rx, l_y + ry

    # 1. Main Engine Bell
    ax.add_patch(Polygon([xf(-12, -35), xf(12, -35), xf(20, -65), xf(-20, -65)], facecolor=C_ENGINE, alpha=alpha_val, zorder=12))

    # 2. Landing Gear (Struts and Footpads)
    legs = [(-50, -65), (50, -65), (0, -75)] 
    for lx, ly in legs:
        p1 = xf(lx*0.5, -20); p2 = xf(lx, ly)
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=C_STRUT, lw=6, alpha=alpha_val, zorder=10)
        p3 = xf(lx*0.8, -10)
        ax.plot([p3[0], p2[0]], [p3[1], p2[1]], color=C_CRATER, lw=3, alpha=alpha_val, zorder=9)
        
        fx, fy = xf(lx, ly)
        pad = plt.Circle((0, 0), 10, facecolor=C_GOLD, edgecolor=C_WINDOW, lw=2, zorder=11, alpha=alpha_val)
        pad.set_transform(matplotlib.transforms.Affine2D().scale(2.0, 0.5).rotate(np.radians(pitch)).translate(fx, fy) + ax.transData)
        ax.add_patch(pad)
        
        pr1, pr2 = xf(lx, ly), xf(lx, ly-30)
        ax.plot([pr1[0], pr2[0]], [pr1[1], pr2[1]], color=C_WINDOW, lw=2, alpha=alpha_val, zorder=10)

    # 3. Descent Stage (Octagonal Mylar Block)
    ax.add_patch(Polygon([xf(-45, -10), xf(45, -10), xf(50, -35), xf(-50, -35)], facecolor=C_GOLD, edgecolor=C_FOIL_D, lw=4, alpha=alpha_val, zorder=13))
    ax.add_patch(Polygon([xf(-35, -10), xf(35, -10), xf(40, -35), xf(-40, -35)], facecolor=C_FOIL_D, alpha=alpha_val, zorder=14))

    # 4. Ascent Stage (Cabin & Pressure Vessel)
    cx, cy = xf(0, 10)
    ax.add_patch(Circle((cx, cy), 32, facecolor=C_ALUM, edgecolor=C_WINDOW, lw=3, alpha=alpha_val, zorder=15))
    ax.add_patch(Polygon([xf(-22, 22), xf(22, 22), xf(18, -5), xf(-18, -5)], facecolor=C_ALUM, edgecolor=C_STRUT, lw=2, alpha=alpha_val, zorder=16))
    
    # Windows
    ax.add_patch(Polygon([xf(-20, 15), xf(-5, 12), xf(-8, 0), xf(-18, 2)], facecolor=C_WINDOW, alpha=alpha_val, zorder=17))
    ax.add_patch(Polygon([xf(20, 15), xf(5, 12), xf(8, 0), xf(18, 2)], facecolor=C_WINDOW, alpha=alpha_val, zorder=17))

    # 5. RCS Quads
    for rx, ry in [(-35, 5), (35, 5)]:
        ax.add_patch(Rectangle(xf(rx-5, ry-5), 10, 10, facecolor=C_STRUT, alpha=alpha_val, zorder=18))
        p_u = xf(rx, ry+7); p_d = xf(rx, ry-7); p_l = xf(rx-7, ry); p_r = xf(rx+7, ry)
        ax.add_patch(Circle(p_u, 4, facecolor=C_ENGINE, alpha=alpha_val, zorder=19))
        ax.add_patch(Circle(p_d, 4, facecolor=C_ENGINE, alpha=alpha_val, zorder=19))
        ax.add_patch(Circle(p_l, 4, facecolor=C_ENGINE, alpha=alpha_val, zorder=19))
        ax.add_patch(Circle(p_r, 4, facecolor=C_ENGINE, alpha=alpha_val, zorder=19))

# ------------------------------------------------------------------
# O(1) KINEMATIC STREAM 
# ------------------------------------------------------------------
def generate_stream():
    np.random.seed(290)

    p_x = np.zeros(N_PLUME); p_y = np.zeros(N_PLUME)
    p_vx = np.zeros(N_PLUME); p_vy = np.zeros(N_PLUME)
    p_life = np.zeros(N_PLUME)

    d_x = np.zeros(N_DUST); d_y = np.zeros(N_DUST)
    d_vx = np.zeros(N_DUST); d_vy = np.zeros(N_DUST)
    d_life = np.zeros(N_DUST)

    total_dist_x = 0.0

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        # Normalise 24 seconds to 1.0 logic phase
        phase = np.clip(t_sec / 20.0, 0.0, 1.0) # Lands precisely at 20 seconds, holds 4s.

        # ---- THE KINEMATIC MATH (20s TERMINAL BRAKE) ----
        # Smooth ease-out deceleration
        v_x_ground = 140.0 * ((1.0 - phase)**1.5)
        total_dist_x += v_x_ground

        # Pitchover timeline
        if t_sec < 12.0:
            pitch = 65.0 
        elif t_sec < 18.0:
            pitch = 65.0 * (1.0 - (t_sec - 12) / 6.0)
        else:
            pitch = 0.0
            
        # Alt Drop
        alt = 1800.0 * ((1.0 - phase)**2.5) + 30.0 # Land legs rest
        l_y = CY_GND + alt
        l_x = CX

        throttle = 1.0 if t_sec < 19.5 else 0.0
        if 18.0 < t_sec < 19.5: throttle = 0.4 # Hover ease

        # State Strings
        if t_sec < 12.0:
            state = "P64: BRAKING PHASE (GRAVITY TURN)"
            ui_col = C_GUI_WARN
        elif t_sec < 18.0:
            state = "P64: PITCH-OVER MANOEUVRE"
            ui_col = C_GUI_WARN
        elif t_sec < 19.8:
            state = "P66: TERMINAL DESCENT (HOVER)"
            ui_col = C_TEXT
        else:
            state = "CONTACT LIGHT: ENGINE STOP"
            ui_col = C_GUI_OK

        # ---- PLUME TENSOR UPDATE ----
        p_life -= 0.04
        spawns = int(250 * throttle)
        if spawns > 0:
            dead = np.where(p_life <= 0)[0]
            num = min(spawns, len(dead))
            if num > 0:
                idx = dead[:num]
                bx, by = rotate_coord(0, -65, pitch)
                p_x[idx] = l_x + bx + np.random.uniform(-10, 10, num)
                p_y[idx] = l_y + by + np.random.uniform(-5, 5, num)

                tv_x, tv_y = rotate_coord(0, -80, pitch)
                p_vx[idx] = tv_x + np.random.uniform(-10, 10, num)
                p_vy[idx] = tv_y + np.random.uniform(-10, 10, num) - 15 
                p_life[idx] = 1.0

        p_x += p_vx; p_y += p_vy
        p_vx *= 0.94; p_vy *= 0.94

        # ---- DUST TENSOR (SURFACE SPALLATION) ----
        d_life -= 0.02
        if alt < 350 and throttle > 0:
            d_spawns = int((350 - alt) * 1.5 * throttle)
            dead_d = np.where(d_life <= 0)[0]
            num_d = min(d_spawns, len(dead_d))
            if num_d > 0:
                idx_d = dead_d[:num_d]
                d_x[idx_d] = l_x + np.random.uniform(-60, 60, num_d)
                d_y[idx_d] = CY_GND
                
                # RECTIFICATION: O(1) Concatenation instead of internal np.random.choice dimensional failure
                angs = np.concatenate([
                    np.random.uniform(0.05, 0.4, num_d//2 + 1),
                    np.random.uniform(2.7, 3.1, num_d//2 + 1)
                ])[:num_d]
                
                speeds = np.random.uniform(40, 120, num_d)
                d_vx[idx_d] = np.cos(angs) * speeds
                d_vy[idx_d] = np.sin(angs) * speeds
                d_life[idx_d] = 1.0

        d_x += d_vx - v_x_ground 
        d_y += d_vy
        d_vy -= 1.5 
        d_vx *= 0.97

        hit_g = d_y < CY_GND
        d_y[hit_g] = CY_GND
        d_vx[hit_g] *= 0.8
        d_vy[hit_g] = 0

        a_p = np.where(p_life > 0)[0]
        a_d = np.where(d_life > 0)[0]

        yield (f, t_sec, state, ui_col, l_x, l_y, pitch, throttle, alt, v_x_ground, total_dist_x,
               np.copy(p_x[a_p]), np.copy(p_y[a_p]), np.copy(p_life[a_p]),
               np.copy(d_x[a_d]), np.copy(d_y[a_d]), np.copy(d_life[a_d]))

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state, ui_col, l_x, l_y, pitch, throttle, alt, v_x, total_dist, px, py, pl, dx, dy, dl = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    fig.patch.set_facecolor(C_BG)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    ax.set_facecolor(C_BG)
    
    # Cinematic Tracking Camera (Frames the lander heavily in the upper sector)
    ax.set_xlim(-540, 540)
    ax.set_ylim(-760, 1160)

    # 1. INFINITE SCROLLING MOON TERRAIN
    ax.add_patch(Rectangle((-540, -760), 1080, (CY_GND - (-760)), facecolor=C_MOON, zorder=1))
    ax.plot([-540, 540], [CY_GND, CY_GND], color=C_CRATER, lw=3, zorder=2)

    # Cartesian Background Speed Grids
    grid_spacing = 300.0
    s_grid = (np.arange(0, 3000, grid_spacing) - total_dist) % 1500.0 - 750.0
    for gx in s_grid:
        if -540 < gx < 540:
            ax.plot([gx, gx], [CY_GND, 1160], color=C_MOON, lw=1.0, alpha=0.5, zorder=1)

    wrap = 1500.0
    s_x = (cp_x - total_dist) % wrap - (wrap/2)
    vis = (s_x > -600) & (s_x < 600)
    vx_c = s_x[vis]
    vw_c = cp_w[vis]
    vd_c = cp_d[vis]

    for i in range(len(vx_c)):
        ax.add_patch(Polygon([(vx_c[i]-vw_c[i], CY_GND), (vx_c[i]-vw_c[i]*0.5, CY_GND-vd_c[i]),
                              (vx_c[i] + vw_c[i]*0.5, CY_GND-vd_c[i]), (vx_c[i]+vw_c[i], CY_GND)],
                             facecolor=C_CRATER, alpha=0.5, zorder=3))

    # 2. RENDER LUNAR MODULE
    draw_lander(ax, l_x, l_y, pitch, throttle, 1.0)

    # 3. THRUST PLUME & ABRASIVE REGOLITH 
    x_list, y_list, c_list, s_list = [], [], [], []

    if len(px) > 0:
        c_p = np.zeros((len(px), 4))
        c_p[:, :3] = C_PLUME_1 * pl[:, None] + C_PLUME_2 * (1-pl[:, None])
        c_p[:, 3] = pl * 0.85 

        x_list.append(px); y_list.append(py)
        c_list.append(c_p); s_list.append(pl * 40.0)

    if len(dx) > 0:
        c_d = np.zeros((len(dx), 4))
        c_d[:, :3] = C_DUST
        c_d[:, 3] = dl * 0.7 

        x_list.append(dx); y_list.append(dy)
        c_list.append(c_d); s_list.append(dl * 25.0)

    if len(x_list) > 0:
        cat_x = np.concatenate(x_list)
        cat_y = np.concatenate(y_list)
        cat_c = np.concatenate(c_list)
        cat_s = np.concatenate(s_list)
        ax.scatter(cat_x, cat_y, c=cat_c, s=cat_s, edgecolors='none', zorder=20)

    # 4. ABSOLUTE TELEMETRY 
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, facecolor=C_BG, zorder=80))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=C_TEXT, lw=4, zorder=81)
    ax.text(0.04, 0.965, "LG-29b :: APOLLO TERMINAL DESCENT (P64/P66)", transform=ax.transAxes, color=C_TEXT, fontsize=22, fontname='monospace', weight='bold', va='center', zorder=81)

    ax.add_patch(plt.Rectangle((0, 0), 1, 0.12, transform=ax.transAxes, facecolor=C_BG, zorder=80))
    ax.plot([0, 1], [0.12, 0.12], transform=ax.transAxes, color=C_TEXT, lw=4, zorder=81)
    
    ax.text(0.04, 0.08, f"ALTITUDE  : {max(0, int(alt - 30)):04d} METRES", transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace', weight='bold', zorder=81)
    ax.text(0.04, 0.04, f"VELOCITY  : X {int(v_x):03d} // Y {int(abs(l_y - CY_GND - 30)):03d}", transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace', zorder=81)

    pulse = ui_col if (f % 30 < 15) or ui_col == C_GUI_OK else C_TEXT
    ax.text(0.96, 0.06, f"[{state}]", transform=ax.transAxes, color=pulse, fontsize=20, fontname='monospace', weight='bold', ha='right', va='center', zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-29b THE SUICIDE BURN (DAYLIGHT) [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Extended 24.0s Kinematics // O(1) Matrix Rectified")

    with mp.Pool(processes=cpu_cores) as pool:
        frames = range(TOTAL_FRAMES)
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")
    print("Compilation Complete. Absolute Touchdown Matrix Achieved.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
