"""
PROJECT: Logic Garden 435 (Exact Physical Construct // The Fogbank Interstage)
FORMAT: YouTube Shorts (1080x1920)
METADATA: TELLER-ULAM, FOGBANK, AEROGEL, FUSION, KINEMATICS, DAYLIGHT
EXECUTION: 24.0s Sequence. Irreversible Thermodynamic Discontinuity.
RULES ENFORCED:
- Explicit Causality: No dead time. Force vectors and text overlays prove the physics.
- Dynamic Structural Compression (Radiation Implosion tracking).
- Absolute Macro Destructive Yield overriding casing geometry.
- Daylight Palette (White Substrate / High-Contrast Solid Geometry).
- Purged Jargon. Australian spelling conventions (maths, colour, vaporise).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import multiprocessing as mp
import os
import gc
import math

# ======== SEQUENCE PARAMETERS ========
DURATION = 24.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_435_fogbank"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'          # Indestructible Black UI / Casing
C_PRIMARY   = '#005599'          # Deep Marine (Fission Core)
C_FOGBANK   = '#94A3B8'          # Machined Steel (Static Aerogel)
C_PLASMA    = '#FF3300'          # Intense Red (Radiation Plasma)
C_SECONDARY = '#1E293B'          # Carbon Slate (Fusion Core)
C_YIELD     = '#DE008A'          # Deep Magenta (Thermonuclear Criticality)
C_SPARKPLUG = '#FFB300'          # Dense Amber
C_XRAY      = '#00C853'          # Jade (Radiation Wavefront)
C_STEEL     = '#64748B'          # UI Ghost Metrics

# ------------------------------------------------------------------
# PARALLEL GENERATOR (LOGIC TENSORS)
# ------------------------------------------------------------------
def generate_stream():
    np.random.seed(435)

    X_LEFT_CASE, X_RIGHT_CASE = 200.0, 880.0
    
    # FOGBANK Aerogel Substrate Matrix
    N_NODES = 12000
    f_x = np.zeros(N_NODES)
    f_y = np.zeros(N_NODES)

    # Pack nodes into left and right interstage channels
    half = N_NODES // 2
    f_x[:half] = np.random.uniform(220, 390, half)
    f_y[:half] = np.random.uniform(400, 1400, half)
    f_x[half:] = np.random.uniform(690, 860, half)
    f_y[half:] = np.random.uniform(400, 1400, half)

    f_vx = np.zeros(N_NODES)
    f_vy = np.zeros(N_NODES)
    f_state = np.zeros(N_NODES, dtype=int) 

    # Macro Casing Debris
    N_DEBRIS = 2000
    c_x = np.zeros(N_DEBRIS)
    c_y = np.zeros(N_DEBRIS)
    c_vx = np.zeros(N_DEBRIS)
    c_vy = np.zeros(N_DEBRIS)

    for f in range(TOTAL_FRAMES):
        t = f / float(FPS)

        # A) KINEMATIC EVENT TRIGGERS (EXPLICIT CAUSALITY)
        # Primary Implosion (Radius visually crushes inwards from 140 to 70 over 4 seconds)
        prim_r = 140.0 - 70.0 * min(1.0, t / 4.0)

        # X-Ray Flux triggers exactly at T=6.0 and wipes the channel cleanly
        if t > 6.0 and t < 8.0:
            y_flux = 1500.0 - 600.0 * (t - 6.0)
        elif t >= 8.0:
            y_flux = 300.0
        else:
            y_flux = 2000.0

        # Secondary Radiation Implosion (Violent crushing from T=8.0 to 14.0)
        if t < 8.0:
            c_factor = 0.0
        elif t < 14.0:
            raw_c = (t - 8.0) / 6.0
            c_factor = raw_c * raw_c * (3 - 2 * raw_c) # S-Curve
        else:
            c_factor = 1.0

        sec_w = 340.0 - (240.0 * c_factor) # Shrinks massively from 340 to 100 units
        x_sec_l = 540.0 - (sec_w / 2)
        x_sec_r = 540.0 + (sec_w / 2)

        # B) FOGBANK PHASE TRANSITION (VAPORISATION)
        hit_mask = (f_y > y_flux) & (f_state == 0)
        f_state[hit_mask] = 1

        hit_idx = np.where(hit_mask)[0]
        # Inward kinetic rush
        f_vx[hit_idx] = np.random.uniform(50, 150, len(hit_idx)) * np.sign(540 - f_x[hit_idx])
        f_vy[hit_idx] = np.random.uniform(-30, -5, len(hit_idx)) 

        # C) PLASMA KINETICS (BOILING STATE)
        plasma_mask = f_state == 1
        
        # Inject "Boiling" jitter to plasma nodes so they aggressively vibrate
        p_act = np.where(plasma_mask)[0]
        f_x[p_act] += np.random.normal(0, 2.0, len(p_act))
        f_y[p_act] += np.random.normal(0, 2.0, len(p_act))

        # Add heavy pressure inward
        f_vx[p_act] += np.sign(540 - f_x[p_act]) * 20.0 * (1.0/FPS)
        f_x[p_act] += f_vx[p_act]
        f_y[p_act] += f_vy[p_act]

        # Clamp to Casing (Left/Right bounds)
        out_L = f_x[p_act] < X_LEFT_CASE + 20
        f_x[p_act[out_L]] = X_LEFT_CASE + 20
        f_vx[p_act[out_L]] *= -0.5

        out_R = f_x[p_act] > X_RIGHT_CASE - 20
        f_x[p_act[out_R]] = X_RIGHT_CASE - 20
        f_vx[p_act[out_R]] *= -0.5

        # Crush against the shifting Secondary
        hit_sec_L = (f_x[p_act] > x_sec_l) & (f_x[p_act] < 540) & (f_y[p_act] > 400) & (f_y[p_act] < 1200)
        f_x[p_act[hit_sec_L]] = x_sec_l
        f_vx[p_act[hit_sec_L]] *= -0.8 # Heavy dampening

        hit_sec_R = (f_x[p_act] < x_sec_r) & (f_x[p_act] > 540) & (f_y[p_act] > 400) & (f_y[p_act] < 1200)
        f_x[p_act[hit_sec_R]] = x_sec_r
        f_vx[p_act[hit_sec_R]] *= -0.8

        # D) THERMONUCLEAR YIELD (CATASTROPHIC BLOWOUT T=18.0)
        if f == int(18.0 * FPS):
            f_state[:] = 2
            angs = np.random.uniform(0, 2*np.pi, N_NODES)
            speeds = np.random.uniform(500, 2000, N_NODES) 
            vecX = f_x - 540
            vecY = f_y - 750
            mags = np.sqrt(vecX**2 + vecY**2) + 0.1
            f_vx = (vecX / mags) * speeds
            f_vy = (vecY / mags) * speeds

            c_x[:] = np.concatenate([np.random.uniform(180, 220, N_DEBRIS//2), np.random.uniform(860, 900, N_DEBRIS//2)])
            c_y[:] = np.random.uniform(300, 1700, N_DEBRIS)
            d_vecX = c_x - 540
            d_vecY = c_y - 750
            d_mags = np.sqrt(d_vecX**2 + d_vecY**2) + 0.1
            c_vx = (d_vecX / d_mags) * np.random.uniform(800, 2500, N_DEBRIS)
            c_vy = (d_vecY / d_mags) * np.random.uniform(800, 2500, N_DEBRIS)

        if t > 18.0:
            f_x += f_vx * (1.0/FPS)
            f_y += f_vy * (1.0/FPS)
            c_x += c_vx * (1.0/FPS)
            c_y += c_vy * (1.0/FPS)

        yield (f, t, x_sec_l, x_sec_r, sec_w, y_flux, prim_r,
               np.copy(f_x), np.copy(f_y), np.copy(f_state),
               np.copy(c_x), np.copy(c_y))

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t, sl, sr, sw, y_flux, prim_r, fx, fy, fstate, cx, cy = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # 1. ARCHITECTURAL FRAME (9:16)
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # 2. O(N) FOGBANK SUBSTRATE KINEMATICS
    mask_0 = fstate == 0
    if np.any(mask_0):
        ax.scatter(fx[mask_0], fy[mask_0], s=3, color=C_FOGBANK, edgecolors='none', zorder=5)

    # BOILING PLASMA
    mask_1 = fstate == 1
    if np.any(mask_1):
        ax.scatter(fx[mask_1], fy[mask_1], s=8, color=C_PLASMA, edgecolors='none', alpha=0.9, zorder=6)

    mask_2 = fstate == 2
    if np.any(mask_2):
        ax.scatter(fx[mask_2], fy[mask_2], s=12, color=C_YIELD, edgecolors='none', alpha=0.8, zorder=20)

    if t < 18.0:
        # 3. OUTER TUNGSTEN CASING (Intact)
        ax.add_patch(patches.Rectangle((180, 280), 20, 1440, facecolor=C_TEXT, zorder=10))
        ax.add_patch(patches.Rectangle((880, 280), 20, 1440, facecolor=C_TEXT, zorder=10))
        ax.add_patch(patches.Polygon([[180, 1720], [880, 1720], [700, 1850], [380, 1850]], facecolor=C_TEXT, zorder=10))
        ax.add_patch(patches.Polygon([[180, 280], [880, 280], [700, 150], [380, 150]], facecolor=C_TEXT, zorder=10))

        # 4. FISSION PRIMARY (The Trigger)
        # Visual critical pulsing before detonation flash
        if t >= 4.0 and t < 6.0:
            prim_col = C_BG if (f % 6) < 3 else C_PRIMARY
        elif t < 4.0:
            prim_col = C_PRIMARY
        else:
            prim_col = C_BG

        prim_s = 1.0 if t < 6.0 else (1.0 + (t-6.0)*8) # Aggressive blowout out of existence
        if prim_s < 10.0: # Stop drawing after it blows out
            trans_p = matplotlib.transforms.Affine2D().scale(prim_s).translate(540*(1-prim_s), 1450*(1-prim_s)) + ax.transData
            ax.add_patch(patches.Circle((540, 1450), prim_r, facecolor=prim_col, edgecolor=C_TEXT, lw=4, transform=trans_p, zorder=12))

        # Explicit Trigger Labelling
        if t < 4.0:
            ax.text(540, 1450, "HIGH EXPLOSIVE\nIMPLOSION", color=C_BG, fontsize=18, fontname='monospace', weight='bold', ha='center', va='center', zorder=13)
        elif t < 6.0:
            ax.text(540, 1450, "CRITICALITY", color=C_TEXT if prim_col == C_BG else C_BG, fontsize=22, fontname='monospace', weight='bold', ha='center', va='center', zorder=13)

        # The X-Ray Flux wavefront line visually
        if t > 6.0 and t < 8.0:
            ax.plot([200, 880], [y_flux, y_flux], color=C_XRAY, lw=8, zorder=15)
            ax.fill_between([200, 880], y_flux, y_flux+150, color=C_XRAY, alpha=0.5, zorder=14)
            # Explicit Tracking Text sliding with the wave
            ax.text(540, y_flux + 50, "[X-RAY FLUX FLASH]", color=C_BG, fontsize=20, fontname='monospace', weight='bold', ha='center', va='center', zorder=16)

        # 5. FUSION SECONDARY (The Payload)
        sec_col = C_SECONDARY if t < 16.0 else (C_YIELD if t < 18.0 else C_BG)
        ax.add_patch(patches.Rectangle((sl, 400), sw, 800, facecolor=sec_col, edgecolor=C_TEXT, lw=4, zorder=11))

        # Explicit Force Arrows mapping the Plasma Yield crushing the core
        if t > 8.0 and t < 15.0:
            arr_len = max(20, 80 - (t-8.0)*10) # Arrows push inward
            for arr_y in [600, 800, 1000]:
                ax.arrow(sl - arr_len - 30, arr_y, arr_len, 0, head_width=20, head_length=20, fc=C_PLASMA, ec=C_PLASMA, lw=4, zorder=17)
                ax.arrow(sr + arr_len + 30, arr_y, -arr_len, 0, head_width=20, head_length=20, fc=C_PLASMA, ec=C_PLASMA, lw=4, zorder=17)
            # Explicit Dynamic Label
            ax.text(540, 800, "RADIATION\nIMPLOSION", color=C_BG, fontsize=22, fontname='monospace', weight='bold', ha='center', va='center', zorder=13)

        # Central Sparkplug (Plutonium trigger rod)
        # Visual pulsing and expansion right before yield
        if t > 14.0 and t < 16.0:
            plug_col = C_BG if (f % 4) < 2 else C_SPARKPLUG
            pw = max(4, sw * 0.15) * (1.0 + (t-14.0)*0.5) # Expands
        else:
            plug_col = C_SPARKPLUG if t < 16.0 else C_BG
            pw = max(4, sw * 0.15) 
            
        ax.add_patch(patches.Rectangle((540 - pw/2, 450), pw, 700, facecolor=plug_col, edgecolor=C_TEXT, lw=2, zorder=12))

    else:
        # T > 18.0 : CATASTROPHIC BLOWOUT DEBRIS
        ax.scatter(cx, cy, s=35, color=C_TEXT, edgecolors='none', zorder=25)
        ax.scatter(cx[::2], cy[::2], s=70, color=C_BG, edgecolors='none', zorder=26)
        ax.add_patch(plt.Rectangle((0, 0), 1080, 1920, facecolor=C_BG, alpha=min(1.0, (t-18.0)*0.8), zorder=85))

    # 6. ABSOLUTE DAYLIGHT TELEMETRY (TOP HUD)
    ax.add_patch(plt.Rectangle((0, 0.90), 1, 0.10, transform=ax.transAxes, facecolor=C_BG, zorder=90))
    ax.plot([0, 1], [0.90, 0.90], transform=ax.transAxes, color=C_TEXT, lw=6, zorder=91)

    ax.text(0.04, 0.965, "LG-435 // THE FOGBANK PARADOX", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=92)
    ax.text(0.04, 0.930, "TELLER-ULAM THERMONUCLEAR INTERSTAGE", transform=ax.transAxes, color=C_STEEL, fontsize=15, fontname='monospace', weight='bold', va='center', zorder=92)

    ax.text(0.96, 0.965, "AEROGEL SOLVENT : [ACETONITRILE]", transform=ax.transAxes, color=C_FOGBANK, fontsize=16, fontname='monospace', weight='bold', ha='right', va='center', zorder=92)
    warning_col = C_YIELD if t > 18.0 else C_TEXT
    warning_msg = "[SYNTHETIC LOST]" if t > 18.0 else "[SYNTHETIC VERIFIED]"
    ax.text(0.96, 0.930, warning_msg, transform=ax.transAxes, color=warning_col, fontsize=14, fontname='monospace', weight='bold', ha='right', va='center', zorder=92)

    # 7. ABSOLUTE DAYLIGHT TELEMETRY (BOTTOM HUD)
    ax.add_patch(plt.Rectangle((0, 0), 1, 0.14, transform=ax.transAxes, facecolor=C_BG, zorder=90))
    ax.plot([0, 1], [0.14, 0.14], transform=ax.transAxes, color=C_TEXT, lw=6, zorder=91)

    if t < 4.0: sys_state = "[PHASE 1 : HIGH EXPLOSIVE IMPLOSION]"
    elif t < 6.0: sys_state = "[PHASE 2 : PRIMARY FISSION CRITICALITY]"
    elif t < 8.0: sys_state = "[PHASE 3 : X-RAY FLUX FLASH // FOGBANK VAPORISES]"
    elif t < 16.0: sys_state = "[PHASE 4 : THERMODYNAMIC PLASMA CRUSH CORE]"
    elif t < 18.0: sys_state = "[PHASE 5 : SECONDARY CRITICALITY // FUSION YIELD]"
    else: sys_state = "[PHASE 6 : CASING ANNIHILATION // O(1) BLOWOUT]"

    hud_col = C_PLASMA if "CRUSH" in sys_state else (C_YIELD if "ANNIHILATION" in sys_state else C_TEXT)

    ax.text(0.04, 0.10, f"KINEMATIC TIMELINE : {sys_state}", transform=ax.transAxes, color=hud_col, fontsize=16, fontname='monospace', weight='bold', zorder=92)

    ax.text(0.04, 0.05, f"SECONDARY IMPLOSION WIDTH : {sw:06.1f} U", transform=ax.transAxes, color=C_TEXT if t < 18.0 else C_BG, fontsize=16, fontname='monospace', weight='bold', zorder=92)

    p_density = np.sum(fstate == 1) / float(len(fstate)) * 100
    ax.text(0.60, 0.05, f"TARGET TRANSITION TO PLASMA: {p_density:05.1f} %", transform=ax.transAxes, color=C_PLASMA if t < 18.0 else C_BG, fontsize=16, fontname='monospace', weight='bold', zorder=92)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-435: FOGBANK INTERSTAGE MATRIX (DAYLIGHT) [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Phase Transition Logic and Yield Blowout Tensors Secured. Stand by for compilation.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
