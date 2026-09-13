"""
PROJECT: Logic Garden 106i (Exact Physical Construct // Co-Orbital Interceptor)
FORMAT: YouTube Shorts (1080x1920)
METADATA: CO-ORBITAL, ASAT, KINETIC KILL, ORBITAL TRANSFER, DAYLIGHT
EXECUTION: 12.0s Sequence. True Seamless Modulo Constellation.
RULES ENFORCED: 
- O(1) Polar-to-Cartesian Kinematics for a perfect Phased Orbit Transfer.
- Frame-Zero Engagement (Radius collapsed to natively trap 135-degree arrays on-screen).
- Hardware Scale Magnification (Intricate detail mapping).
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
OUT_DIR = "frames_106i_co_orbital"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'          # Indestructible Black UI
C_STEEL     = '#94A3B8'          # Parking Orbits & Ghost Metrics
C_EARTH     = '#F1F5F9'          # Planetary Bedrock
C_SAT       = '#1E293B'          # Carbon Slate (Orbital Bus)
C_PANEL     = '#005599'          # Deep Marine (Solar Arrays)
C_ASAT      = '#E2E8F0'          # Bright Machined Steel (Space Mine)
C_BOOST     = '#FFB300'          # Dense Amber (Orbital Transfer Burn)
C_DIVERT    = '#FFB300'          # KKV Divert Thruster Flashes
C_KILL      = '#DE008A'          # Deep Magenta (Vaporisation Yield)
C_REENTRY   = '#FF3300'          # Intense Red (Atmospheric Spallation)

# ------------------------------------------------------------------
# O(1) MACRO PHYSICS ENGINE (RADIAL GRAVITY)
# ------------------------------------------------------------------
# MASSIVE SPATIAL COLLAPSE (Forces 135-degree kinematics immediately on screen)
EARTH_C = np.array([0.0, -350.0])
R_EARTH = 350.0
R_ATMOS = 450.0
R_PARKING = 500.0
R_TARGET  = 650.0        # Zenith perfectly frames at exact Y=300

GM_CONST = 5000000.0     # Planetary Gravitational Pull Tuned for rapid decay

# ------------------------------------------------------------------
# PARALLEL GENERATOR (LOGIC TENSORS)
# ------------------------------------------------------------------
def generate_stream():
    np.random.seed(1069)
    
    # Pre-allocate sheer spallation matrix
    MAX_D = 1800
    d_pos = np.zeros((MAX_D, 2))
    d_vel = np.zeros((MAX_D, 2))
    d_life = np.zeros(MAX_D)
    d_hot = np.zeros(MAX_D, dtype=bool)

    for f in range(TOTAL_FRAMES):
        t = f / float(FPS)

        # --- A. CONSTELLATION ORBIT KINEMATICS ---
        # 4 satellites spacing 90 deg. Orbit rate: 7.5 deg/s = 90 deg loop.
        sats = []
        for i in range(4):
            theta_deg = 135.0 - 7.5 * t + i * 90.0
            
            # The lead satellite hits exactly Zenith (90 degrees) at T=6.0
            # If t >= 6.0 and it is the lead sat, it no longer exists geometrically
            if i == 0 and t >= 6.0:
                continue
                
            sat_pos = EARTH_C + np.array([R_TARGET * np.cos(np.radians(theta_deg)), 
                                          R_TARGET * np.sin(np.radians(theta_deg))])
            sats.append({'pos': sat_pos, 'theta': theta_deg})

        # --- B. CO-ORBITAL INTERCEPTOR (SPACE MINE) TRAJECTORY ---
        asat_pos, asat_vel = np.zeros(2), np.zeros(2)
        asat_active = False
        
        # Inclusive Phase evaluation. Target Zenith execution at EXACTLY T=6.0!
        if t <= 6.0:
            tau = t / 6.0
            
            # Continuous Parametric Orbital Transfer
            # Starts behind at 150 degrees, climbs from R_PARKING to R_TARGET
            theta_I_deg = 150.0 - 10.0 * t
            theta_I = np.radians(theta_I_deg)
            r_I = R_PARKING + (R_TARGET - R_PARKING) * (tau**2)
            
            asat_pos = EARTH_C + np.array([r_I * np.cos(theta_I), r_I * np.sin(theta_I)])
            
            # Velocity Derivation (Chain Rule mapping Polar to Cartesian)
            dr_dt = (R_TARGET - R_PARKING) * 2 * tau * (1/6.0)
            dtheta_dt = np.radians(-10.0)
            
            asat_vel[0] = dr_dt * np.cos(theta_I) - r_I * dtheta_dt * np.sin(theta_I)
            asat_vel[1] = dr_dt * np.sin(theta_I) + r_I * dtheta_dt * np.cos(theta_I)
            
            if t < 6.0: 
                asat_active = True

        # --- C. SPALLATION IMPACT EVENT (T=6.0s) ---
        if f == int(6.0 * FPS):
            # Target's absolute Cartesian velocity at Zenith (moving purely right/positive X)
            v_targ_x = R_TARGET * np.radians(7.5) 
            target_vel = np.array([v_targ_x, 0.0])
            
            # The Kinetic collision transfers immense forward velocity to the debris
            drift_base = target_vel + asat_vel * 0.25
            
            d_pos[:] = asat_pos # Absolute impact at Zenith P3 [0.0, 300.0]
            
            # Blast cone predominantly drives forward along the orbital path
            angs_base = np.random.uniform(0, 2*np.pi, MAX_D)
            angs_forward = np.random.uniform(-math.pi/4, math.pi/4, MAX_D)
            angs = np.where(np.random.rand(MAX_D) > 0.4, angs_forward, angs_base)
            
            speeds = np.random.uniform(70, 500, MAX_D)
            
            d_vel[:, 0] = drift_base[0] + np.cos(angs) * speeds
            d_vel[:, 1] = drift_base[1] + np.sin(angs) * speeds
            
            # Explicit Modulo Drain: Time mathematically decays by loop-end T=12.0
            d_life[:] = 6.0 - np.random.uniform(0.0, 1.0, MAX_D)
            
        # --- D. DEBRIS KINEMATIC INTEGRATION ---
        act = d_life > 0
        if np.any(act):
            vecC = d_pos[act] - EARTH_C
            distC = np.linalg.norm(vecC, axis=1)
            
            gravX = -(GM_CONST / (distC**3)) * vecC[:, 0]
            gravY = -(GM_CONST / (distC**3)) * vecC[:, 1]
            
            d_vel[act, 0] += gravX * (1.0/FPS)
            d_vel[act, 1] += gravY * (1.0/FPS)
            
            d_pos[act] += d_vel[act] * (1.0/FPS)
            
            # Atmospheric Reentry (Drag and Heat)
            atmo_mask = distC < R_ATMOS
            idx_act = np.where(act)[0]
            
            d_hot[:] = False
            d_hot[idx_act[atmo_mask]] = True
            
            # Hyperthermal burn out (Highly accelerated to prevent crossing boundary loop)
            d_life[idx_act[atmo_mask]] -= 0.12
            d_vel[idx_act[atmo_mask]] *= 0.96
            
            # Time evaporation guarantees absolute clean state for loop wrap
            d_life[act] -= (1.0/FPS)

        active_indices = np.nonzero(d_life > 0)[0]
        
        yield (f, t, sats, asat_active, asat_pos, asat_vel,
               np.copy(d_pos[active_indices]), np.copy(d_life[active_indices]), np.copy(d_hot[active_indices]))

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t, sats, A_act, A_pos, A_vel, dx, dl, dhot = packet

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
    ax.add_patch(patches.Circle((EARTH_C[0], EARTH_C[1]), R_EARTH, fill=False, edgecolor=C_TEXT, lw=6, zorder=2))
    
    # Atmospheric Envelope
    ax.add_patch(patches.Circle((EARTH_C[0], EARTH_C[1]), R_ATMOS, fill=False, edgecolor=C_STEEL, lw=2.5, linestyle='dashed', zorder=2))
    ax.text(-500, R_ATMOS + EARTH_C[1] + 15, "ATMOSPHERIC SPALLATION BOUNDARY", color=C_STEEL, fontsize=12, fontname='monospace', weight='bold', rotation=15, zorder=3)

    # 3. KINEMATIC ORBITAL PATHS
    # Reveal the underlying mathematics. The Parking vs Target orbits.
    ax.add_patch(patches.Circle((EARTH_C[0], EARTH_C[1]), R_TARGET, fill=False, edgecolor=C_STEEL, lw=2, linestyle=':', alpha=0.6, zorder=2))
    ax.add_patch(patches.Circle((EARTH_C[0], EARTH_C[1]), R_PARKING, fill=False, edgecolor=C_STEEL, lw=2, linestyle=':', alpha=0.6, zorder=2))
    
    ax.text(-25, R_PARKING + EARTH_C[1] + 20, "KKV PARKING ORBIT", color=C_STEEL, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=3)
    ax.text(-25, R_TARGET + EARTH_C[1] + 20, "TARGET CONSTELLATION", color=C_STEEL, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=3)

    # 4. TARGET CONSTELLATION (SATELLITES UP-SCALED FOR INTRICATE DETAIL)
    for sat in sats:
        sx, sy = sat['pos'][0], sat['pos'][1]
        ang = np.radians(sat['theta'] - 90) # Tangent alignment
        
        trans = matplotlib.transforms.Affine2D().rotate_around(sx, sy, ang) + ax.transData
        
        ax.add_patch(patches.Rectangle((sx-10, sy-7.5), 20, 15, facecolor=C_SAT, edgecolor=C_TEXT, lw=2.0, zorder=15, transform=trans))
        ax.add_patch(patches.Rectangle((sx-45, sy-4), 35, 8, facecolor=C_PANEL, edgecolor=C_TEXT, lw=1.5, zorder=14, transform=trans))
        ax.add_patch(patches.Rectangle((sx+10, sy-4), 35, 8, facecolor=C_PANEL, edgecolor=C_TEXT, lw=1.5, zorder=14, transform=trans))

    # 5. CO-ORBITAL KINETIC KILL VEHICLE (THE SPACE MINE)
    if A_act:
        yaw = np.arctan2(A_vel[1], A_vel[0]) - np.pi/2
        ATrans = matplotlib.transforms.Affine2D().rotate_around(A_pos[0], A_pos[1], yaw) + ax.transData
        
        # Aerodynamic Cone/Cylinder architecture scaled dramatically up 
        poly = [[A_pos[0]-7, A_pos[1]-20], [A_pos[0]+7, A_pos[1]-20], [A_pos[0]+7, A_pos[1]+5], [A_pos[0], A_pos[1]+20], [A_pos[0]-7, A_pos[1]+5]]
        ax.add_patch(patches.Polygon(poly, facecolor=C_ASAT, edgecolor=C_TEXT, lw=2.0, zorder=11, transform=ATrans))
        
        # Hypergolic Orbital Transfer Burn
        flame_len = 50 + np.random.uniform(-6, 6)
        ax.add_patch(patches.Polygon([[A_pos[0]-6, A_pos[1]-20], [A_pos[0]+6, A_pos[1]-20], [A_pos[0], A_pos[1]-flame_len]], facecolor=C_PANEL, alpha=0.9, edgecolor='none', zorder=10, transform=ATrans))
        ax.add_patch(patches.Polygon([[A_pos[0]-8, A_pos[1]-20], [A_pos[0]+8, A_pos[1]-20], [A_pos[0], A_pos[1]-flame_len*1.3]], facecolor=C_BOOST, alpha=0.5, edgecolor='none', zorder=9, transform=ATrans))
        
        # Terminal Guidance Pulses
        if t > 4.5 and f % 6 < 3:
            for side in [-9, 9]:
                ax.plot([A_pos[0]+side, A_pos[0]+side*3.0], [A_pos[1]+10, A_pos[1]+10], color=C_DIVERT, lw=3.0, zorder=11, transform=ATrans)

    # 6. SPALLATION DEBRIS & REENTRY BURNOUT
    if len(dx) > 0:
        c_deb = np.zeros((len(dx), 4))
        c_deb[:, :3] = np.array(mcol.to_rgb(C_TEXT))
        c_deb[dhot, :3] = np.array(mcol.to_rgb(C_REENTRY))
        c_deb[:, 3] = np.clip(dl / 6.0 + 0.3, 0, 1) 
        ax.scatter(dx[:,0], dx[:,1], s=dl*20, c=c_deb, edgecolors='none', zorder=18)

    # 7. ABSOLUTE DAYLIGHT TELEMETRY (TOP HUD)
    ax.add_patch(plt.Rectangle((0, 0.90), 1, 0.10, transform=ax.transAxes, facecolor=C_BG, zorder=80))
    ax.plot([0, 1], [0.90, 0.90], transform=ax.transAxes, color=C_TEXT, lw=6, zorder=81)

    ax.text(0.04, 0.965, "LG-106i // CO-ORBITAL INTERCEPTOR", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=82)
    ax.text(0.04, 0.930, "PARKING ORBIT TRANSFER & TAIL-CHASE KINEMATICS", transform=ax.transAxes, color=C_PANEL, fontsize=15, fontname='monospace', weight='bold', va='center', zorder=82)

    # 8. ABSOLUTE DAYLIGHT TELEMETRY (BOTTOM HUD)
    ax.add_patch(plt.Rectangle((0, 0), 1, 0.14, transform=ax.transAxes, facecolor=C_BG, zorder=80))
    ax.plot([0, 1], [0.14, 0.14], transform=ax.transAxes, color=C_TEXT, lw=6, zorder=81)

    if t < 5.8: sys_state = "[PHASE ALIGNMENT // KINEMATIC BURN]"
    elif t < 6.2: sys_state = "[KINETIC IMPACT YIELD]"
    else: sys_state = "[SPALLATION SENSOR TRACKING]"

    hud_col = C_REENTRY if "IMPACT" in sys_state else (C_PANEL if "TRACKING" not in sys_state else C_TEXT)

    ax.text(0.04, 0.10, f"INTERCEPTOR DOMAIN : {sys_state}", transform=ax.transAxes, color=hud_col, fontsize=18, fontname='monospace', weight='bold', zorder=82)
    
    tti = max(0, 6.0 - t)
    target_vel = R_TARGET * math.radians(7.5)
    asat_mag = math.sqrt(A_vel[0]**2 + A_vel[1]**2) if A_act else 0
    delta_v = abs(target_vel - asat_mag) if t < 6.0 else 0
    
    ax.text(0.04, 0.06, f"TIME TO IMPACT (TTI) : {tti:05.2f} SECONDS", transform=ax.transAxes, color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(0.04, 0.03, f"CLOSURE VELOCITY (Δv): {delta_v:05.1f} KILOMETRES/SEC", transform=ax.transAxes, color=C_SAT, fontsize=16, fontname='monospace', weight='bold', zorder=82)

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
    print(f"LG-106i: CO-ORBITAL MATRIX (DAYLIGHT) [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Macro Spatial Constraints Re-Archived. Action visible T=0. Stand by for compilation.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
