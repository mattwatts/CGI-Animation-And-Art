"""
PROJECT: Logic Garden 106h (Exact Physical Construct // ASAT Kinematic Kill)
FORMAT: YouTube Shorts (1080x1920)
METADATA: ASAT, ANTI-SATELLITE, KINETIC KILL, ORBITAL MECHANICS, DAYLIGHT
EXECUTION: 12.0s Sequence. True Seamless Modulo Constellation.
RULES ENFORCED: 
- O(1) Parametric Bezier Targeting ensures KKV hits moving Zenith exactly at T=6.0.
- Seamless Macro-Global Array (4 Constellation Targets wrapping 90 degrees/12s).
- Central Impact Framing (Intercept Altitude perfectly framed at Y=300).
- Daylight Palette (White Substrate / High-Contrast Solid Geometry).
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
DURATION = 12.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_106h_asat"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'          # Indestructible Black UI
C_STEEL     = '#94A3B8'          # Atmospheric Metrics
C_EARTH     = '#F1F5F9'          # Planetary Bedrock
C_SAT       = '#1E293B'          # Carbon Slate (Orbital Bus)
C_PANEL     = '#005599'          # Deep Marine (Solar Arrays)
C_ASAT      = '#E2E8F0'          # Bright Machined Steel (Interceptor)
C_BOOST     = '#FFB300'          # Dense Amber (Solid Rocket Plume)
C_DIVERT    = '#FFB300'          # KKV Divert Thruster Flashes
C_KILL      = '#DE008A'          # Deep Magenta (Vaporisation Yield)
C_REENTRY   = '#FF3300'          # Intense Red (Atmospheric Burn)

# ------------------------------------------------------------------
# O(1) MACRO PHYSICS ENGINE (RADIAL GRAVITY)
# ------------------------------------------------------------------
EARTH_C = np.array([0.0, -1800.0])
R_EARTH = 1300.0
R_ATMOS = 1450.0
R_ORBIT = 2100.0        # FIXED: Pulled down from 2550 to visually center the Array
GM_CONST = 5000000.0    # Tuned Orbital Pull 

# Launch Base (Western Hemisphere Arc)
BASE_DEG = 105.0 
BASE_POS = EARTH_C + np.array([R_EARTH * np.cos(np.radians(BASE_DEG)), 
                               R_EARTH * np.sin(np.radians(BASE_DEG))])

# ASAT Bezier Constraints (Hits exactly at X=0, Y=300 Zenith)
P0 = BASE_POS
P1 = np.array([BASE_POS[0], -200.0])
P2 = np.array([-150.0, 50.0])
P3 = np.array([0.0, 300.0])

def bezier(t, p0, p1, p2, p3):
    u = 1 - t
    pos = u**3 * p0 + 3*u**2*t * p1 + 3*u*t**2 * p2 + t**3 * p3
    vel = 3*u**2 * (p1 - p0) + 6*u*t * (p2 - p1) + 3*t**2 * (p3 - p2)
    return pos, vel

# ------------------------------------------------------------------
# PARALLEL GENERATOR (LOGIC TENSORS)
# ------------------------------------------------------------------
def generate_stream():
    np.random.seed(106)
    
    # Pre-allocate sheer spallation matrix
    MAX_D = 1200
    d_pos = np.zeros((MAX_D, 2))
    d_vel = np.zeros((MAX_D, 2))
    d_life = np.zeros(MAX_D)
    d_hot = np.zeros(MAX_D, dtype=bool)

    # Reusable Booster Drop Matrix
    booster_pos = np.zeros(2)
    booster_vel = np.zeros(2)
    booster_active = False

    for f in range(TOTAL_FRAMES):
        t = f / FPS

        # --- A. CONSTELLATION ORBIT KINEMATICS ---
        # 4 satellites spacing 90 deg. Orbit rate: 7.5 deg/s = 90 deg loop.
        sats = []
        for i in range(4):
            theta_deg = 135.0 + i * 90.0 - 7.5 * t
            
            # Absolute Logical Intercept Condition
            if i == 0 and t >= 6.0:
                continue
                
            sat_pos = EARTH_C + np.array([R_ORBIT * np.cos(np.radians(theta_deg)), 
                                          R_ORBIT * np.sin(np.radians(theta_deg))])
            sats.append({'pos': sat_pos, 'theta': theta_deg})

        # --- B. KKV ASAT TRAJECTORY ---
        asat_pos, asat_vel = np.zeros(2), np.zeros(2)
        asat_active = False
        
        # Inclusive Evaluation limits. Extracts true Zenith velocity at T=6.0 exact frame.
        if t <= 6.0:
            tau = t / 6.0
            asat_pos, asat_vel = bezier(tau, P0, P1, P2, P3)
            # Velocity must be scaled because tau spans 0-1 over 6 seconds
            asat_vel = asat_vel / 6.0
            
            if t < 6.0: 
                asat_active = True

            # First Stage Booster Separation Physics (occurring at T=2.5s)
            if tau > (2.5/6.0) and not booster_active:
                _, b_v = bezier(2.5/6.0, P0, P1, P2, P3)
                booster_vel = (b_v / 6.0) * 0.9 # Slight mechanical braking on shedding
                booster_pos = asat_pos.copy()
                booster_active = True

        # --- C. FIRST STAGE BOOSTER DECAY ---
        if booster_active:
            vec_earth = booster_pos - EARTH_C
            dist = np.linalg.norm(vec_earth)
            if dist > R_EARTH:
                grav = -(GM_CONST / (dist**2)) * (vec_earth / dist)
                booster_vel += grav * (1.0/FPS)
                booster_pos += booster_vel * (1.0/FPS)
                if dist < R_ATMOS:
                    booster_vel *= 0.98 # Atmospheric drag

        # --- D. SPALLATION IMPACT EVENT (T=6.0s) ---
        if f == int(6.0 * FPS):
            # Base satellite orbital velocity vector at Zenith
            v_orb_mag = (7.5 * math.pi / 180.0) * R_ORBIT
            drift_base = np.array([v_orb_mag + (asat_vel[0] * 0.2), asat_vel[1] * 0.2]) 
            
            d_pos[:] = asat_pos # Now strictly evaluates to P3 [0.0, 300.0]
            angs = np.random.uniform(0, 2*np.pi, MAX_D)
            angs_biased = np.where(np.random.rand(MAX_D) > 0.3, np.random.uniform(-0.5, 0.5, MAX_D), angs)
            speeds = np.random.uniform(50, 400, MAX_D)
            
            d_vel[:, 0] = drift_base[0] + np.cos(angs_biased) * speeds
            d_vel[:, 1] = drift_base[1] + np.sin(angs_biased) * speeds
            
            # Explicit Modulo Drain: Vaporises by T=12.0
            d_life[:] = 6.0 - np.random.uniform(0.0, 1.0, MAX_D)
            
        # --- E. DEBRIS KINEMATIC INTEGRATION ---
        act = d_life > 0
        if np.any(act):
            vecC = d_pos[act] - EARTH_C
            distC = np.linalg.norm(vecC, axis=1)
            
            gravX = -(GM_CONST / (distC**3)) * vecC[:, 0]
            gravY = -(GM_CONST / (distC**3)) * vecC[:, 1]
            
            d_vel[act, 0] += gravX * (1.0/FPS)
            d_vel[act, 1] += gravY * (1.0/FPS)
            
            d_pos[act] += d_vel[act] * (1.0/FPS)
            
            atmo_mask = distC < R_ATMOS
            idx_act = np.where(act)[0]
            
            d_hot[:] = False
            d_hot[idx_act[atmo_mask]] = True
            
            d_life[idx_act[atmo_mask]] -= 0.05
            d_vel[idx_act[atmo_mask]] *= 0.98
            
            d_life[act] -= (1.0/FPS)

        active_indices = np.nonzero(d_life > 0)[0]
        
        yield (f, t, sats, asat_active, asat_pos, asat_vel, booster_active, booster_pos, booster_vel, 
               np.copy(d_pos[active_indices]), np.copy(d_life[active_indices]), np.copy(d_hot[active_indices]))

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t, sats, A_act, A_pos, A_vel, B_act, B_pos, B_vel, dx, dl, dhot = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # 1. ARCHITECTURAL FRAME (9:16)
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)

    # 2. PLANETARY BEDROCK & EXOATMOSPHERE
    ax.add_patch(patches.Circle((EARTH_C[0], EARTH_C[1]), R_EARTH, facecolor=C_EARTH, zorder=1))
    ax.add_patch(patches.Circle((EARTH_C[0], EARTH_C[1]), R_EARTH, fill=False, edgecolor=C_TEXT, lw=5, zorder=2))
    
    # Atmospheric Envelope
    ax.add_patch(patches.Circle((EARTH_C[0], EARTH_C[1]), R_ATMOS, fill=False, edgecolor=C_STEEL, lw=2, linestyle='dashed', zorder=2))
    
    # Mathematical Suborbital Launch Complex Extrusion
    b_x, b_y = BASE_POS[0], BASE_POS[1]
    ax.plot([b_x-25, b_x+25], [b_y, b_y], color=C_TEXT, lw=4, zorder=3)
    ax.plot([b_x-15, b_x-15], [b_y, b_y-40], color=C_TEXT, lw=4, zorder=3)
    ax.plot([b_x+15, b_x+15], [b_y, b_y-40], color=C_TEXT, lw=4, zorder=3)

    # 3. KINEMATIC CONSTELLATION (SATELLITES)
    for sat in sats:
        sx, sy = sat['pos'][0], sat['pos'][1]
        ang = np.radians(sat['theta'] - 90) # Tangent alignment
        
        trans = matplotlib.transforms.Affine2D().rotate_around(sx, sy, ang) + ax.transData
        
        ax.add_patch(patches.Rectangle((sx-8, sy-6), 16, 12, facecolor=C_SAT, edgecolor=C_TEXT, lw=1.5, zorder=15, transform=trans))
        ax.add_patch(patches.Rectangle((sx-35, sy-3), 27, 6, facecolor=C_PANEL, edgecolor=C_TEXT, lw=1.0, zorder=14, transform=trans))
        ax.add_patch(patches.Rectangle((sx+8, sy-3), 27, 6, facecolor=C_PANEL, edgecolor=C_TEXT, lw=1.0, zorder=14, transform=trans))

    # 4. KINETIC KILL VEHICLE (ASAT INTERCEPTOR)
    if A_act:
        yaw = np.arctan2(A_vel[1], A_vel[0]) - np.pi/2
        ATrans = matplotlib.transforms.Affine2D().rotate_around(A_pos[0], A_pos[1], yaw) + ax.transData
        
        if t <= 2.5:
            ax.add_patch(patches.Rectangle((A_pos[0]-6, A_pos[1]-20), 12, 35, facecolor=C_ASAT, edgecolor=C_TEXT, lw=1.5, zorder=11, transform=ATrans))
            flame_len = 45 + np.random.uniform(-5, 5)
            ax.add_patch(patches.Polygon([[A_pos[0]-4, A_pos[1]-20], [A_pos[0]+4, A_pos[1]-20], [A_pos[0], A_pos[1]-flame_len]], facecolor=C_PANEL, alpha=0.8, edgecolor='none', zorder=10, transform=ATrans))
            ax.add_patch(patches.Polygon([[A_pos[0]-6, A_pos[1]-20], [A_pos[0]+6, A_pos[1]-20], [A_pos[0], A_pos[1]-flame_len*1.2]], facecolor=C_BOOST, alpha=0.4, edgecolor='none', zorder=9, transform=ATrans))
        else:
            ax.add_patch(patches.Polygon([[A_pos[0]-4, A_pos[1]-8], [A_pos[0]+4, A_pos[1]-8], [A_pos[0], A_pos[1]+10]], facecolor=C_ASAT, edgecolor=C_TEXT, lw=1.5, zorder=11, transform=ATrans))
            if f % 4 < 2:
                for side in [-5, 5]:
                    ax.plot([A_pos[0]+side, A_pos[0]+side*3], [A_pos[1], A_pos[1]], color=C_DIVERT, lw=3, zorder=11, transform=ATrans)

    if B_act:
        yaw_b = np.arctan2(B_vel[1], B_vel[0]) - np.pi/2
        BTrans = matplotlib.transforms.Affine2D().rotate_around(B_pos[0], B_pos[1], yaw_b) + ax.transData
        ax.add_patch(patches.Rectangle((B_pos[0]-6, B_pos[1]-15), 12, 30, facecolor=C_STEEL, edgecolor=C_BG, lw=1, alpha=0.6, zorder=8, transform=BTrans))

    # 5. SPALLATION DEBRIS & REENTRY BURNOUT
    if len(dx) > 0:
        c_deb = np.zeros((len(dx), 4))
        c_deb[:, :3] = np.array(mcol.to_rgb(C_TEXT))
        c_deb[dhot, :3] = np.array(mcol.to_rgb(C_REENTRY))
        c_deb[:, 3] = np.clip(dl / 6.0 + 0.3, 0, 1) 
        ax.scatter(dx[:,0], dx[:,1], s=dl*15, c=c_deb, edgecolors='none', zorder=18)

    # 6. ABSOLUTE DAYLIGHT TELEMETRY (TOP HUD)
    ax.add_patch(plt.Rectangle((0, 0.90), 1, 0.10, transform=ax.transAxes, facecolor=C_BG, zorder=80))
    ax.plot([0, 1], [0.90, 0.90], transform=ax.transAxes, color=C_TEXT, lw=6, zorder=81)

    ax.text(0.04, 0.965, "LG-106h // ANTI-SATELLITE (ASAT) KKV", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=82)
    ax.text(0.04, 0.930, "DIRECT ASCENT INTERCEPT MATRIX // MODULO WRAP", transform=ax.transAxes, color=C_PANEL, fontsize=15, fontname='monospace', weight='bold', va='center', zorder=82)

    # 7. ABSOLUTE DAYLIGHT TELEMETRY (BOTTOM HUD)
    ax.add_patch(plt.Rectangle((0, 0), 1, 0.14, transform=ax.transAxes, facecolor=C_BG, zorder=80))
    ax.plot([0, 1], [0.14, 0.14], transform=ax.transAxes, color=C_TEXT, lw=6, zorder=81)

    if t < 2.5: sys_state = "[BOOSTER ACTIVE // ASCENT]"
    elif t < 6.0: sys_state = "[KKV FREEFLIGHT // TERMINAL ALIGN]"
    elif t < 6.2: sys_state = "[KINETIC IMPACT YIELD]"
    else: sys_state = "[SPALLATION SENSOR TRACKING]"

    hud_col = C_REENTRY if "IMPACT" in sys_state else (C_PANEL if "TRACKING" not in sys_state else C_TEXT)

    ax.text(0.04, 0.10, f"INTERCEPTOR DOMAIN : {sys_state}", transform=ax.transAxes, color=hud_col, fontsize=18, fontname='monospace', weight='bold', zorder=82)
    
    tti = max(0, 6.0 - t)
    ax.text(0.04, 0.06, f"TIME TO IMPACT (TTI) : {tti:05.2f} SECONDS", transform=ax.transAxes, color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(0.04, 0.03, f"TARGET ORBITAL VEL   : 07.50 KILOMETRES/SEC", transform=ax.transAxes, color=C_SAT, fontsize=16, fontname='monospace', weight='bold', zorder=82)

    if t > 5.9 and t < 6.3:
        ax.add_patch(patches.Rectangle((0,0), 1080, 1920, facecolor=C_BG, alpha=(1.0 - abs(t-6.0)*3), zorder=90))

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-106i: ASAT INTERCEPT MATRIX (DAYLIGHT) [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Geometric Payload Centred. Tensors Balanced. Stand by for compilation.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
