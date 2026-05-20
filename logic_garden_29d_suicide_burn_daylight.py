"""
SOVEREIGN CODE: logic_garden_29d_suicide_burn_daylight.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) True Perspective Projection
SCENE: LG-29d (The Suicide Burn / Apollo Guidance Daylight Protocol)
HOTFIX: Terrain Scaling, Vacuum Momentum Transfer (Vector Dependant Spallation)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 10.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_29d_suicide_burn_daylight"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST ENGINEERING PALETTE --------
C_BG        = '#FFFFFF'        
C_MOON      = '#E5E8E8'        
C_CRATER    = '#95A5A6'        
C_GOLD      = '#D4AC0D'        
C_FOIL_D    = '#B9770E'        
C_ALUM      = '#BDC3C7'        
C_WINDOW    = '#1C2833'        
C_ENGINE    = '#17202A'        
C_STRUT     = '#7F8C8D'        
C_TEXT      = '#111111'        

C_PLUME     = np.array([0.0, 1.0, 1.0])    
C_PLUME_C   = np.array([0.2, 0.6, 0.9])    
C_DUST      = np.array([0.4, 0.4, 0.4])    

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE KINEMATIC CAMERA & GROUND MATRIX
# ------------------------------------------------------------------
CX, CY_GND = 0.0, -300.0  

N_PLUME = 6000
N_DUST  = 12000

CRATER_N = 80
np.random.seed(290) 
cp_x = np.random.uniform(-1000, 3000, CRATER_N)
cp_w = np.random.uniform(50, 150, CRATER_N)
cp_d = np.random.uniform(10, 40, CRATER_N)

# ------------------------------------------------------------------
# MODULE GEOMETRY CONSTRUCT
# ------------------------------------------------------------------
def rotate_coord(x, y, pitch_deg):
    theta = np.radians(pitch_deg)
    c, s = np.cos(theta), np.sin(theta)
    return x * c - y * s, x * s + y * c

def draw_lander(ax, l_x, l_y, pitch, thrust_lvl, alpha_val):
    def xf(x, y):
        rx, ry = rotate_coord(x, y, pitch)
        return l_x + rx, l_y + ry

    ax.add_patch(Polygon([xf(-10, -35), xf(10, -35), xf(18, -65), xf(-18, -65)], facecolor=C_ENGINE, alpha=alpha_base, zorder=12))
    
    legs = [(-45, -60), (45, -60), (0, -70)] 
    for lx, ly in legs:
        p1 = xf(lx*0.5, -20); p2 = xf(lx, ly)
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=C_STRUT, lw=6, alpha=alpha_base, zorder=10)
        p3 = xf(lx*0.8, -10)
        ax.plot([p3[0], p2[0]], [p3[1], p2[1]], color=C_CRATER, lw=3, alpha=alpha_base, zorder=9)
        fx, fy = xf(lx, ly)
        pad = plt.Circle((fx, fy), 8, facecolor=C_GOLD, edgecolor=C_WINDOW, lw=2, zorder=11, alpha=alpha_base)
        pad.set_transform(matplotlib.transforms.Affine2D().scale(2.0, 0.5).translate(fx*(1-2.0), fy*(1-0.5)) + ax.transData)
        ax.add_patch(pad)
        pr1, pr2 = xf(lx, ly), xf(lx, ly-25)
        ax.plot([pr1[0], pr2[0]], [pr1[1], pr2[1]], color=C_WINDOW, lw=2, alpha=alpha_base, zorder=10)

    ax.add_patch(Polygon([xf(-40, -10), xf(40, -10), xf(45, -35), xf(-45, -35)], facecolor=C_GOLD, edgecolor=C_FOIL_D, lw=4, alpha=alpha_base, zorder=13))
    ax.add_patch(Polygon([xf(-30, -10), xf(30, -10), xf(35, -35), xf(-35, -35)], facecolor=C_FOIL_D, alpha=alpha_base, zorder=14)) 

    cx, cy = xf(0, 10)
    ax.add_patch(Circle((cx, cy), 28, facecolor=C_ALUM, edgecolor=C_WINDOW, lw=3, alpha=alpha_base, zorder=15))
    ax.add_patch(Polygon([xf(-20, 20), xf(20, 20), xf(15, -5), xf(-15, -5)], facecolor=C_ALUM, edgecolor=C_CRATER, lw=2, alpha=alpha_base, zorder=16))
    ax.add_patch(Polygon([xf(-18, 15), xf(-5, 12), xf(-8, 0), xf(-16, 2)], facecolor=C_WINDOW, alpha=alpha_base, zorder=17))
    ax.add_patch(Polygon([xf(18, 15), xf(5, 12), xf(8, 0), xf(16, 2)], facecolor=C_WINDOW, alpha=alpha_base, zorder=17))

    for rx, ry in [(-30, 5), (30, 5)]:
        ax.add_patch(Rectangle(xf(rx-4, ry-4), 8, 8, facecolor=C_STRUT, alpha=alpha_base, zorder=18))
        p_u = xf(rx, ry+6); p_d = xf(rx, ry-6); p_l = xf(rx-6, ry); p_r = xf(rx+6, ry)
        ax.add_patch(Circle(p_u, 3, facecolor=C_ENGINE, alpha=alpha_base, zorder=19))
        ax.add_patch(Circle(p_d, 3, facecolor=C_ENGINE, alpha=alpha_base, zorder=19))
        ax.add_patch(Circle(p_l, 3, facecolor=C_ENGINE, alpha=alpha_base, zorder=19))
        ax.add_patch(Circle(p_r, 3, facecolor=C_ENGINE, alpha=alpha_base, zorder=19))
        
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
        phase = f / float(TOTAL_FRAMES)
        
        # ---- THE KINEMATIC MATH ----
        l_prog = np.clip(phase / 0.75, 0.0, 1.0)
        
        # HOTFIX: Reduced horizontal scale so it brakes massively but smoothly
        v_x_ground = 35.0 * ((1.0 - l_prog)**1.5)
        total_dist_x += v_x_ground

        pitch = 65.0 * ((1.0 - l_prog)**2)
        raw_alt = 700.0 * ((1.0 - l_prog)**2.5) 
        
        l_y = CY_GND + raw_alt + 70.0
        l_x = CX

        throttle = 1.0 if phase < 0.75 else 0.0
        if 0.65 < phase < 0.75: throttle = 0.5 * (1.0 - (phase-0.65)/0.1)

        w_alpha = 0.0
        global alpha_base
        alpha_base = 1.0

        state = "P64: BRAKING PHASE"
        if l_prog > 0.8: state = "P66: TERMINAL DESCENT"
        if phase >= 0.75: state = "CONTACT LIGHT: GEOMETRY LOCKED"

        if phase > 0.85:
            r_prog = (phase - 0.85) / 0.15
            w_alpha = np.interp(r_prog, [0.0, 0.3, 0.8, 1.0], [0.0, 1.0, 1.0, 0.0])
            alpha_base = np.interp(r_prog, [0.3, 0.6], [1.0, 0.0])
            state = "EXECUTIVE OVERFLOW // 1202 ALARM RESET"
        
        # Determine Thrust Exit Vector mathematically
        tv_x, tv_y = rotate_coord(0, -80, pitch) 

        # ---- PLUME TENSOR UPDATE ----
        p_life -= 0.05
        spawns = int(200 * throttle)
        if spawns > 0:
            dead = np.where(p_life <= 0)[0]
            num = min(spawns, len(dead))
            if num > 0:
                idx = dead[:num]
                bx, by = rotate_coord(0, -65, pitch)
                p_x[idx] = l_x + bx + np.random.uniform(-10, 10, num)
                p_y[idx] = l_y + by + np.random.uniform(-5, 5, num)
                
                p_vx[idx] = tv_x + np.random.uniform(-15, 15, num)
                p_vy[idx] = tv_y + np.random.uniform(-15, 15, num) - 20 
                p_life[idx] = 1.0

        p_x += p_vx; p_y += p_vy
        p_vx *= 0.95; p_vy *= 0.95

        # ---- DUST TENSOR (VACUUM MOMENTUM TRANSFER) ----
        d_life -= 0.03 # Dust hangs slightly longer
        if raw_alt < 200 and throttle > 0:
            d_spawns = int((200 - raw_alt) * 3.0 * throttle)
            dead_d = np.where(d_life <= 0)[0]
            num_d = min(d_spawns, len(dead_d))
            if num_d > 0:
                idx_d = dead_d[:num_d]
                d_x[idx_d] = l_x + np.random.uniform(-40, 40, num_d)
                d_y[idx_d] = CY_GND
                
                # HOTFIX: The thrust vector horizontally shapes the dust spread.
                base_noise_x = np.random.normal(0, 25, num_d)
                # If tv_x is positive (pitch backward), blast shoots Right. Wait perfectly.
                d_vx[idx_d] = base_noise_x + (tv_x * 1.5) 
                
                d_vy[idx_d] = np.random.uniform(5, 50, num_d) + (abs(tv_x) * 0.2)
                d_life[idx_d] = 1.0
        
        d_x += d_vx - v_x_ground 
        d_y += d_vy
        
        # True Vacuum mechanics: Zero horizontal drag. Constant downward gravity.
        d_vy -= 1.2 

        hit_g = d_y < CY_GND
        d_y[hit_g] = CY_GND
        d_vx[hit_g] *= 0.7 # Ground friction absorbs sideways bounce
        d_vy[hit_g] = 0

        a_p = np.where(p_life > 0)[0]
        a_d = np.where(d_life > 0)[0]

        yield (f, phase, state, l_x, l_y, pitch, throttle, raw_alt, v_x_ground, total_dist_x, w_alpha, alpha_base, 
               np.copy(p_x[a_p]), np.copy(p_y[a_p]), np.copy(p_life[a_p]),
               np.copy(d_x[a_d]), np.copy(d_y[a_d]), np.copy(d_life[a_d]))

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, phase, state, l_x, l_y, pitch, throttle, alt, v_x, total_dist, w_alpha, g_alpha_base, px, py, pl, dx, dy, dl = packet

    global alpha_base
    alpha_base = g_alpha_base

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    fig.patch.set_facecolor(C_BG)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540)
    ax.set_ylim(-660, 1260) 

    ax.add_patch(Rectangle((-540, -660), 1080, (CY_GND - (-660)), facecolor=C_MOON, zorder=1))
    ax.plot([-540, 540], [CY_GND, CY_GND], color=C_CRATER, lw=3, zorder=2)

    wrap = 1500.0
    s_x = (cp_x - total_dist) % wrap - (wrap/2)
    
    vis = (s_x > -600) & (s_x < 600)
    vx_c = s_x[vis]
    vw_c = cp_w[vis]
    vd_c = cp_d[vis]

    for i in range(len(vx_c)):
        ax.add_patch(Polygon([(vx_c[i]-vw_c[i], CY_GND), (vx_c[i]-vw_c[i]*0.5, CY_GND-vd_c[i]), 
                              (vx_c[i] + vw_c[i]*0.5, CY_GND-vd_c[i]), (vx_c[i]+vw_c[i], CY_GND)], 
                             facecolor=C_CRATER, alpha=0.4, zorder=3))

    if alpha_base > 0:
        draw_lander(ax, l_x, l_y, pitch, throttle, alpha_base)

    x_list, y_list, c_list, s_list = [], [], [], []

    if len(px) > 0:
        c_p = np.zeros((len(px), 4))
        c_p[:, :3] = C_PLUME * pl[:, None] + C_PLUME_C * (1-pl[:, None])
        c_p[:, 3] = pl * 0.8 * alpha_base
        
        x_list.append(px); y_list.append(py)
        c_list.append(c_p); s_list.append(pl * 35.0)

    if len(dx) > 0:
        c_d = np.zeros((len(dx), 4))
        c_d[:, :3] = C_DUST
        c_d[:, 3] = dl * 0.6 * alpha_base
        
        x_list.append(dx); y_list.append(dy)
        c_list.append(c_d); s_list.append(dl * 20.0)

    if len(x_list) > 0:
        cat_x = np.concatenate(x_list)
        cat_y = np.concatenate(y_list)
        cat_c = np.concatenate(c_list)
        cat_s = np.concatenate(s_list)
        ax.scatter(cat_x, cat_y, c=cat_c, s=cat_s, edgecolors='none', zorder=20)

    if w_alpha > 0:
        ax.add_patch(Rectangle((-540, -660), 1080, 1920, facecolor=C_BG, alpha=w_alpha, zorder=50))

    # TELEMENTRY WIDGETS
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, facecolor=C_MOON, edgecolor=C_TEXT, lw=2, zorder=80))
    ax.text(0.5, 0.965, "LG-29d :: APOLLO EXACT GUIDANCE TENSOR", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace', weight='bold', ha='center', va='center', zorder=81)

    ax.add_patch(plt.Rectangle((0, 0), 1, 0.10, transform=ax.transAxes, facecolor=C_MOON, edgecolor=C_TEXT, lw=2, zorder=80))
    ax.text(0.04, 0.06, f"ALTITUDE: {int(alt):03d} M", transform=ax.transAxes, color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=81)
    
    ax.text(0.04, 0.03, f"VELOCITY: X {int(v_x*2.0):03d} // Y {int(-150.0 * ((1.0 - (phase/0.75))**1.5) if phase < 0.75 else 0):03d}", transform=ax.transAxes, color=C_TEXT, fontsize=16, fontname='monospace', alpha=0.8, zorder=81)
    
    col_state = '#111111' if phase < 0.85 else '#C0392B'
    ax.text(0.96, 0.045, f"[{state}]", transform=ax.transAxes, color=col_state, fontsize=18, fontname='monospace', weight='bold', ha='right', va='center', zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-29d THE SUICIDE BURN (DAYLIGHT) [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Kinematic Terrain Mapping // Spallation Vector Transfer")

    with mp.Pool(processes=cpu_cores) as pool:
        frames = range(TOTAL_FRAMES)
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Absolute Optical Alignment Secured. Contact is verified.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
