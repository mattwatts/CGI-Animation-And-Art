"""
SOVEREIGN CODE: logic_garden_315_r36_hypergolic.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Kinematic Phase Tensor
SCENE: LG-315_v2 (R-36 Exact / Hypergolic Cold Launch)
HOTFIX: Seamless 10s Loop, Liquid Motor Override, True Parabolic Suspension
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 10.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_315_r36_hypergolic"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST ENGINEERING PALETTE --------
C_BG            = '#FFFFFF'       # Daylight Protocol Baseline
C_SOVIET_STEEL  = '#2C3E50'       # Deep Cold War Naval/Olive Alloy
C_TITANIUM      = '#D5DBDB'       # Baseplate / Accent Rings
C_IRON          = '#1C2833'       # Silo / Hatches / Engine Bells
C_STEEL         = '#7F8C8D'       # Mechanisms / Ground Track
C_SHADOW        = '#BDC3C7'       # Cold Launch Nitrogen Vapor
C_HYPERGOLIC    = '#E67E22'       # Pure Liquid Hypergolic Thrust
C_GOLD          = '#F1C40F'       # Secondary Ignition Core
C_WHITE         = '#FDFEFE'       # Mach Diamond Overpressure
C_TEXT          = '#111111'

def hex_to_rgba(h, a=1.0):
    h = h.lstrip('#')
    return [int(h[0:2],16)/255.0, int(h[2:4],16)/255.0, int(h[4:6],16)/255.0, a]

def ease_in_out(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)

# ------------------------------------------------------------------
# MISSILE KINEMATIC TIMELINE (Vectorized)
# ------------------------------------------------------------------
CY_GND = 300.0
CX = 540.0

def get_m_y_vectorized(t_arr):
    """Calculates the absolute Y coordinate of the bottom engine bell."""
    y = np.full_like(t_arr, -900.0)
    
    # Phase 1: Cold Launch Lift (Parabolic Deceleration to Apogee)
    m_cold = (t_arr >= 1.5) & (t_arr < 3.5)
    prog = (t_arr[m_cold] - 1.5) / 2.0
    y[m_cold] = -900.0 + 1350.0 * (1.0 - (1.0 - prog)**2)
    
    # Phase 2: Liquid Hypergolic Acceleration (Exponential)
    m_ign = (t_arr >= 3.5)
    dt = t_arr[m_ign] - 3.5
    y[m_ign] = 450.0 + 0.5 * 2800.0 * (dt**2)
    return y

def get_m_y(t):
    return get_m_y_vectorized(np.array([t]))[0]

# ------------------------------------------------------------------
# THERMODYNAMIC PARTICLE GENERATOR (O(1) Spatial Matrix)
# ------------------------------------------------------------------
np.random.seed(3152)

# Liquid Hypergolic Exhaust (High Velocity, Clean, Mach Diamonds)
N_EXHAUST = 15000
e_life = np.random.uniform(0.1, 0.9, N_EXHAUST) # Very short lifespan, fast burn
e_spawn = np.random.uniform(3.5, 6.0, N_EXHAUST) # Missile clears frame quickly
e_spawn_y = get_m_y_vectorized(e_spawn) 
# Much tighter X-dispersion for liquid engines, extreme downward Y velocity
e_vx = np.random.normal(0, 80, N_EXHAUST)
e_vy = np.random.uniform(-1000, -2500, N_EXHAUST) 
e_c_keys = np.random.choice([0, 1, 2], N_EXHAUST, p=[0.5, 0.3, 0.2])
cols = [C_WHITE, C_HYPERGOLIC, C_GOLD]
e_colors = np.array([hex_to_rgba(cols[k])[:3] for k in e_c_keys])

# Cold Launch Nitrogen Vapor (Compressible Gas, Mushrooming)
N_COLD = 8000
c_life = np.random.uniform(0.5, 2.5, N_COLD)
c_spawn = np.random.uniform(1.4, 2.5, N_COLD)
c_vx = np.random.normal(0, 400, N_COLD)
c_vy = np.random.uniform(300, 1500, N_COLD)

# ------------------------------------------------------------------
# MULTICORE RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    t = f / float(FPS)
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    fig.patch.set_facecolor(C_BG)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    # 1. THE SILO BASEPLATE & DOORS
    # -------------------------------------------------
    ax.add_patch(Rectangle((0, 0), 1080, CY_GND, facecolor='#F4F6F6', zorder=1))
    ax.plot([0, 1080], [CY_GND, CY_GND], color=C_STEEL, lw=16, zorder=2)
    
    # Underground Silo Shaft
    silo_w = 200
    ax.add_patch(Rectangle((CX - silo_w/2, 0), silo_w, CY_GND, facecolor=C_TEXT, zorder=3)) # Deep Void

    # Blast Door Kinematics (Slide aside)
    lid_x = CX
    lid_open_w = 220
    if 0.0 < t < 1.0:
        lid_x = CX + ease_in_out(t/1.0) * lid_open_w
    elif 1.0 <= t < 8.5:
        lid_x = CX + lid_open_w
    elif 8.5 <= t <= 10.0:
        lid_x = CX + lid_open_w - ease_in_out((t-8.5)/1.5) * lid_open_w

    # Left and Right interlocking doors
    l_lid = CX - (lid_x - CX)
    ax.add_patch(Rectangle((l_lid - 150, CY_GND), 150, 40, facecolor=C_IRON, edgecolor=C_BG, lw=4, zorder=20))
    ax.add_patch(Rectangle((lid_x, CY_GND), 150, 40, facecolor=C_IRON, edgecolor=C_BG, lw=4, zorder=20))

    # 2. ORDNANCE KINEMATICS (The Liquid Fuel R-36)
    # -------------------------------------------------
    M_y = get_m_y(t)
    M_h = 750
    M_w = 160

    if M_y + M_h > 0 and M_y < 2500: # Cull bounds
        # Primary Hull (Soviet Naval Steel)
        ax.add_patch(Rectangle((CX - M_w/2, M_y), M_w, M_h, facecolor=C_SOVIET_STEEL, edgecolor=C_IRON, lw=4, zorder=5))
        # Aerodynamic Shading (Cylindrical gradient)
        ax.add_patch(Rectangle((CX - M_w/4, M_y), M_w/2, M_h, facecolor=C_BG, alpha=0.25, zorder=6))
        
        # Staging Decouplers / Harness Lines
        ax.add_patch(Rectangle((CX - M_w/2, M_y + 200), M_w, 20, facecolor=C_TITANIUM, zorder=6))
        ax.add_patch(Rectangle((CX - M_w/2, M_y + 600), M_w, 15, facecolor=C_IRON, zorder=6))
        
        # Engine Skirt & Base
        ax.add_patch(Rectangle((CX - M_w/2, M_y), M_w, 60, facecolor=C_IRON, zorder=7))
        # 4 Main Engine Bells (R-36 layout)
        ax.add_patch(Polygon([(CX-60, M_y), (CX-20, M_y), (CX-10, M_y-50), (CX-70, M_y-50)], facecolor=C_TEXT, zorder=4))
        ax.add_patch(Polygon([(CX+20, M_y), (CX+60, M_y), (CX+70, M_y-50), (CX+10, M_y-50)], facecolor=C_TEXT, zorder=4))

        # R-36 Blunt Sabotless Nosecone
        nose_y = M_y + M_h
        ax.add_patch(Polygon([(CX - M_w/2, nose_y), (CX + M_w/2, nose_y), (CX + 40, nose_y + 160), (CX - 40, nose_y + 160)], facecolor=C_TITANIUM, edgecolor=C_IRON, lw=4, zorder=5))
        ax.add_patch(Polygon([(CX-20, nose_y), (CX+20, nose_y), (CX+15, nose_y + 160), (CX-15, nose_y + 160)], facecolor=C_BG, alpha=0.3, zorder=6))

    # 3. THERMODYNAMIC HYPERGOLIC IGNITION (Main Engine Thrust)
    # -------------------------------------------------
    if t >= 3.5 and M_y < 2200:
        ig_t = t - 3.5
        # Clean, intense white inner thrust column
        f_len = min(800, 400 + ig_t * 3000)
        ax.add_patch(Polygon([(CX-50, M_y-40), (CX+50, M_y-40), (CX, M_y-f_len)], facecolor=C_WHITE, zorder=8))
        ax.add_patch(Polygon([(CX-70, M_y-10), (CX+70, M_y-10), (CX, M_y-(f_len*0.8))], facecolor=C_HYPERGOLIC, alpha=0.6, zorder=7))

    # 4. COLD LAUNCH NITROGEN DISPLACEMENT VAPOR
    # -------------------------------------------------
    active_c = (t >= c_spawn) & (t < c_spawn + c_life)
    if np.any(active_c):
        age_c = t - c_spawn[active_c]
        cx_arr = CX + c_vx[active_c] * age_c
        cy_arr = CY_GND + c_vy[active_c] * age_c - 0.5 * 400.0 * (age_c**2)
        
        # Clamp to floor and spread radially
        hit_fl = cy_arr < CY_GND
        cy_arr[hit_fl] = CY_GND + np.random.uniform(0, 20, np.sum(hit_fl))
        cx_arr[hit_fl] += np.sign(c_vx[active_c][hit_fl]) * 250.0 * age_c[hit_fl]

        alpha_c = np.clip(1.0 - (age_c / c_life[active_c]), 0, 1)
        sz_c = 90.0 * alpha_c
        
        rgba_c = np.zeros((len(age_c), 4))
        rgba_c[:, :3] = hex_to_rgba(C_SHADOW)[:3]
        rgba_c[:, 3] = alpha_c * 0.45

        ax.scatter(cx_arr, cy_arr, s=sz_c, color=rgba_c, edgecolors='none', zorder=9)

    # 5. MASSIVE LIQUID FUEL EXHAUST & GROUND SHEAR
    # -------------------------------------------------
    active_e = (t >= e_spawn) & (t < e_spawn + e_life)
    if np.any(active_e):
        age_e = t - e_spawn[active_e]
        
        ex_arr = CX + e_vx[active_e] * age_e
        ey_arr = e_spawn_y[active_e] + e_vy[active_e] * age_e
        
        # Absolute Mushroom Shear (Violent 90-degree vector shift)
        hit_floor = ey_arr < CY_GND
        ey_arr[hit_floor] = CY_GND + np.random.uniform(0, 30, np.sum(hit_floor))
        
        # Spread velocity is immense for liquid fuel overpressure
        lat_spread = np.sqrt(age_e[hit_floor]) * 3500.0 
        ex_arr[hit_floor] += np.sign(e_vx[active_e][hit_floor]) * lat_spread

        alpha_e = np.clip(1.0 - (age_e / e_life[active_e]), 0, 1)
        # Liquid exhaust stays relatively tight, dense, bright
        sz_e = 60.0 * (1.0 - alpha_e) + 20.0 
        
        rgba_e = np.zeros((len(age_e), 4))
        rgba_e[:, :3] = e_colors[active_e]
        rgba_e[:, 3] = alpha_e * 0.75

        ax.scatter(ex_arr, ey_arr, s=sz_e, color=rgba_e, edgecolors='none', zorder=10)

    # 6. INDUSTRIAL HUD WIDGETS
    # -------------------------------------------------
    ax.add_patch(Rectangle((0, 1840), 1080, 80, facecolor=C_BG, zorder=60))
    txt_top = "LG-315(v2): KINEMATIC LAUNCH TENSOR // R-36 EXACT PARAMETERS"
    ax.text(40, 1880, txt_top, color=C_IRON, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=61)

    ax.add_patch(Rectangle((0, 0), 1080, 180, facecolor=C_BG, zorder=60))
    ax.add_patch(Rectangle((0, 180), 1080, 4, facecolor=C_IRON, zorder=61))

    sys_str = "STANDBY: ZERO KINETIC DEVIATION"
    sys_col = C_STEEL

    if 1.0 <= t < 3.5:
        sys_str = "COLD LAUNCH EXTRACTION: NITROGEN VENTING"
        sys_col = C_SHADOW
    elif t >= 3.5 and M_y < 1920:
        sys_str = "HYPERGOLIC IGNITION: EXTREME O(1) ACCELERATION"
        sys_col = C_HYPERGOLIC
    elif t >= 3.5 and M_y >= 1920:
        sys_str = "VANGUARD DEPARTURE: DOORS CYCLING SHUT"
        sys_col = C_STEEL

    ax.text(40, 135, f"SYSTEM STATE: {sys_str}", color=sys_col, fontsize=18, fontname='monospace', weight='bold', va='center', zorder=61)

    txt_tensor = f"TIMELINE [\u03C4]: {t:05.2f} // 10.0S SEAMLESS OUROBOROS"
    ax.text(40, 85, txt_tensor, color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=61)

    txt_legal = "LEGAL MATRIX: LIQUID PROPELLANT [UDMH/N2O4] PARAMETERS ACTIVE"
    ax.text(40, 45, txt_legal, color=C_SOVIET_STEEL, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=61)

    # Altitude Telemetry Dial
    dial_cx, dial_cy = 960, 90
    ax.add_patch(Circle((dial_cx, dial_cy), 50, facecolor='none', edgecolor=C_IRON, lw=4, zorder=61))
    
    # Needle traces elevation
    alt_ratio = np.clip((M_y - CY_GND) / 2000.0, 0, 1) if M_y > CY_GND else 0.0
    n_ang = np.radians(180) - alt_ratio * np.pi
    ax.plot([dial_cx, dial_cx + np.cos(n_ang)*45], [dial_cy, dial_cy + np.sin(n_ang)*45], color=sys_col, lw=6, zorder=62)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-315(v2): R-36 EXACT KINEMATIC TENSOR [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Continuous 10.0s Loop (600 Frames) // Hypergolic Engine")

    with mp.Pool(processes=cpu_cores) as pool:
        frames = range(TOTAL_FRAMES)
        for finished_frame in pool.imap_unordered(render_frame, frames, chunksize=16):
            pass
    print("Compilation Complete. Ordnance Detached.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
