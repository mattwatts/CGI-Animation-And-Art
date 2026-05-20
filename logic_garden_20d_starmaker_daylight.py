"""
SOVEREIGN CODE: logic_garden_20d_starmaker_daylight.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Radiation Hydrodynamics
SCENE: LG-20d (The Star Maker / Teller-Ulam Daylight Protocol)
HOTFIX: Seamless 10s Ouroboros Array, Geometric X-Ray Tamp Reflection
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 10.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_20d_starmaker_daylight"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST ENGINEERING PALETTE --------
C_BG        = '#FFFFFF'        # Pure White Daylight Array
C_HOHLRAUM  = '#1A252F'        # Heavy Depleted Uranium Casing
C_TAMPER    = '#7F8C8D'        # Secondary Pusher/Tamper
C_FUEL      = '#3498DB'        # Lithium-Deuteride Baseline
C_PLUG      = '#BDC3C7'        # Machined Plutonium Sparkplug
C_HE        = '#C0392B'        # High Explosive Lenses
C_FISSION   = '#F39C12'        # Trigger Plasma Vector
C_IGNITION  = '#FFFFFF'        # Absolute Phase Change

# Radiation Tensor
C_XRAY      = np.array([0.95, 0.75, 0.10]) # Deep Yellow/Orange Photons
C_XRAY_HOT  = np.array([1.00, 1.00, 1.00]) # Superheated Spectrum

N_PHOTONS = 25000

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE HYDRODYNAMIC MIRROR
# ------------------------------------------------------------------
CX, CY_PRIM, CY_SEC = 0.0, 400.0, -250.0

# Hohlraum Limits (Continuous Bounding Box)
H_W = 600.0
H_H = 1500.0
WALL_THICK = 80.0

# Initial States
PRIM_R_INIT = 120.0
SEC_R_INIT = 200.0
PLUG_R_INIT = 35.0

# ------------------------------------------------------------------
# O(1) KINEMATIC STREAM (RAY TRACE ALLOCATION)
# ------------------------------------------------------------------
def generate_stream():
    np.random.seed(20)
    px = np.zeros(N_PHOTONS)
    py = np.zeros(N_PHOTONS)
    vx = np.zeros(N_PHOTONS)
    vy = np.zeros(N_PHOTONS)
    p_active = np.zeros(N_PHOTONS, dtype=bool)

    spawn_idx = 0

    for f in range(TOTAL_FRAMES):
        phase = f / float(TOTAL_FRAMES)
        dt = 1.0

        # ---- THE PHASE TENOR ----
        prim_r = PRIM_R_INIT
        sec_r = SEC_R_INIT
        plug_r = PLUG_R_INIT
        w_alpha = 0.0      # Whiteout wipe
        reset_alpha = 1.0  # Structure visibility

        is_injecting = False
        state = "STANDBY: GEOMETRY NOMINAL"
        col_ui = '#2C3E50'

        if phase < 0.1:
            pass # Total stillness
        elif phase < 0.15:
            # Implosion of Primary
            state = "STAGE 1: HIGH-EXPLOSIVE IMPLOSION"
            col_ui = C_HE
            # Non-linear crush
            prog = (phase - 0.1) / 0.05
            prim_r = PRIM_R_INIT * (1.0 - (prog**2)*0.8)
            
        elif phase < 0.4:
            # X-Ray Flood. Primary vaporized into plasma source
            state = "STAGE 2: X-RAY RADIATION FLOOD"
            col_ui = '#F39C12'
            prim_r = 25.0 + np.random.uniform(-5, 5) # Pulsing core
            is_injecting = True

            # Launch physical photons
            spawns = 400
            if spawn_idx + spawns < N_PHOTONS:
                angles = np.random.uniform(0, 2*np.pi, spawns)
                speeds = np.random.uniform(40, 80, spawns)
                px[spawn_idx:spawn_idx+spawns] = CX + np.cos(angles)*prim_r
                py[spawn_idx:spawn_idx+spawns] = CY_PRIM + np.sin(angles)*prim_r
                vx[spawn_idx:spawn_idx+spawns] = np.cos(angles)*speeds
                vy[spawn_idx:spawn_idx+spawns] = np.sin(angles)*speeds
                p_active[spawn_idx:spawn_idx+spawns] = True
                spawn_idx += spawns

        elif phase < 0.75:
            # Secondary Crush (Ablation Drive)
            state = "STAGE 3: HYDRODYNAMIC ABLATION CRUSH"
            col_ui = '#E67E22'
            prim_r = 0.0
            prog = (phase - 0.4) / 0.35
            # Slow initial crush, exponential deep crush
            sec_r = np.interp(prog**2, [0, 1], [SEC_R_INIT, 35.0])
            plug_r = np.interp(prog**3, [0, 1], [PLUG_R_INIT, 8.0])
            
        elif phase < 0.85:
            # Ignition & Expansion
            state = "STAGE 4: THERMONUCLEAR IGNITION // LIMIT BREACH"
            col_ui = '#C0392B'
            prog = (phase - 0.75) / 0.1
            sec_r = 35.0 + (prog**3) * 2500.0 # Violent spatial wipe
            plug_r = 0.0
            p_active[:] = False # Erase loose photons
            if sec_r > 1500:
                w_alpha = 1.0

        else:
            # The Ouroboros Fade-In
            state = "OUROBOROS: STRUCTURAL MACRO-RESET"
            col_ui = C_HOHLRAUM
            prog = (phase - 0.85) / 0.15
            sec_r = SEC_R_INIT
            w_alpha = np.interp(prog, [0, 0.4, 1.0], [1.0, 1.0, 0.0])
            reset_alpha = np.interp(prog, [0.3, 1.0], [0.0, 1.0])
            spawn_idx = 0 # Reset Tensor cache silently

        # ---- O(1) BALLISTIC RADIATION PHYSICS ----
        act = p_active
        if np.any(act):
            px[act] += vx[act] * dt
            py[act] += vy[act] * dt

            # Bounding Box (Hohlraum Inner Wall Reflection)
            # Wall limits
            x_max, x_min = H_W/2, -H_W/2
            y_max, y_min = H_H/2, -H_H/2

            hit_l = px < x_min
            hit_r = px > x_max
            hit_b = py < y_min
            hit_t = py > y_max

            vx[hit_l] *= -1; px[hit_l] = x_min
            vx[hit_r] *= -1; px[hit_r] = x_max
            vy[hit_b] *= -1; py[hit_b] = y_min
            vy[hit_t] *= -1; py[hit_t] = y_max

            # Target Matrix Reflection (Bouncing mathematically off the shrinking Secondary)
            if sec_r > 0:
                dist2 = (px - CX)**2 + (py - CY_SEC)**2
                rad_bound = (sec_r + 5)**2
                hit_sec = (dist2 < rad_bound) & act

                if np.any(hit_sec):
                    # Geometric Normal Vectors
                    d_sec = np.sqrt(dist2[hit_sec])
                    nx = (px[hit_sec] - CX) / d_sec
                    ny = (py[hit_sec] - CY_SEC) / d_sec
                    
                    # Dot product reflection mapping `v_new = v - 2(v.n)n`
                    dot = vx[hit_sec]*nx + vy[hit_sec]*ny
                    vx[hit_sec] -= 2 * dot * nx
                    vy[hit_sec] -= 2 * dot * ny

                    # Eject mathematically outside the boundary to prevent capture loop
                    px[hit_sec] += nx * 15.0
                    py[hit_sec] += ny * 15.0

        # Generate output arrays for render worker
        act_idx = np.where(p_active)[0]
        n_act = len(act_idx)
        
        # Color mapping (Speed indicates temp)
        c_tensor = np.zeros((n_act, 4))
        p_sz = np.zeros(n_act)
        
        if n_act > 0:
            speed = np.sqrt(vx[act_idx]**2 + vy[act_idx]**2)
            s_prog = np.clip((speed - 40.0) / 40.0, 0.0, 1.0)
            base_rgb = C_XRAY * (1-s_prog[:, None]) + C_XRAY_HOT * s_prog[:, None]
            c_tensor[:, :3] = base_rgb
            c_tensor[:, 3] = 0.5 + (s_prog * 0.5) # Alpha channel
            p_sz = 10.0 + (s_prog * 20.0)

        yield (f, phase, state, col_ui, prim_r, sec_r, plug_r, w_alpha, reset_alpha, np.copy(px[act_idx]), np.copy(py[act_idx]), c_tensor, p_sz)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, phase, state, col_ui, prim_r, sec_r, plug_r, w_alpha, reset_alpha, rad_x, rad_y, rad_c, rad_s = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    fig.patch.set_facecolor(C_BG)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960) 

    alpha_base = reset_alpha

    if alpha_base > 0:
        # 1. THE HOHLRAUM CASING (MACHINED HEAVY TENSOR)
        h_l, h_r = -H_W/2, H_W/2
        h_b, h_t = -H_H/2, H_H/2

        # Outer Machined Edge
        ax.add_patch(Rectangle((h_l - WALL_THICK, h_b - WALL_THICK), H_W + WALL_THICK*2, H_H + WALL_THICK*2, facecolor=C_HOHLRAUM, zorder=5, alpha=alpha_base))
        # Inner Containment Void
        ax.add_patch(Rectangle((h_l, h_b), H_W, H_H, facecolor=C_BG, zorder=6))

        # Engineering Chamfers / End Caps
        ax.plot([h_l - WALL_THICK, h_l], [h_b - WALL_THICK, h_b], color='#ffffff', lw=2, alpha=0.3*alpha_base, zorder=7)
        ax.plot([h_r + WALL_THICK, h_r], [h_t + WALL_THICK, h_t], color='#ffffff', lw=2, alpha=0.3*alpha_base, zorder=7)

        # 2. THE PRIMARY (FISSION TRIGGER)
        if prim_r > 0:
            if phase < 0.15:
                # Conventional High-Explosive Lenses
                ax.add_patch(Circle((CX, CY_PRIM), prim_r + 40, facecolor=C_HE, edgecolor=C_HOHLRAUM, lw=4, zorder=8, alpha=alpha_base))
                ax.add_patch(Circle((CX, CY_PRIM), prim_r, facecolor=C_TAMPER, zorder=9, alpha=alpha_base))
            else:
                # Pure X-ray Plasma Source
                flash = np.clip((0.4 - phase)/0.25, 0, 1)
                ax.add_patch(Circle((CX, CY_PRIM), prim_r, facecolor=C_FISSION, zorder=10, alpha=flash * alpha_base))
                ax.add_patch(Circle((CX, CY_PRIM), prim_r*0.6, facecolor=C_BG, zorder=11, alpha=flash * alpha_base))

        # 3. THE SECONDARY (FUSION CORE)
        if sec_r > 0 and sec_r < 1000:
            # Ablation Layer / Tamper
            ax.add_patch(Circle((CX, CY_SEC), sec_r, facecolor=C_TAMPER, edgecolor=C_HOHLRAUM, lw=max(1, 4 * (sec_r/SEC_R_INIT)), zorder=12, alpha=alpha_base))
            # Lithium Deuteride Fuel
            fuel_r = sec_r * 0.8
            ax.add_patch(Circle((CX, CY_SEC), fuel_r, facecolor=C_FUEL, zorder=13, alpha=alpha_base))
            # Plutonium Sparkplug
            if plug_r > 0:
                ax.add_patch(Circle((CX, CY_SEC), plug_r, facecolor=C_PLUG, zorder=14, alpha=alpha_base))
                # Internal geometric center void
                ax.add_patch(Circle((CX, CY_SEC), plug_r * 0.3, facecolor=C_HOHLRAUM, zorder=15, alpha=alpha_base))

    # 4. RADIATION HYDRODYNAMIC SCATTER
    if len(rad_x) > 0 and w_alpha < 1.0:
        ax.scatter(rad_x, rad_y, s=rad_s, color=rad_c, edgecolors='none', zorder=20)

    # 5. THERMONUCLEAR IGNITION EXPANSION (Absolute Overdraw)
    if phase >= 0.75 and sec_r > 0:
        ignite_alpha = np.clip((sec_r - 35.0) / 1500.0, 0, 1)
        # Blast sphere
        ax.add_patch(Circle((CX, CY_SEC), sec_r, facecolor=C_IGNITION, zorder=30, alpha=1.0))
        # Ambient screen flash
        if w_alpha > 0:
            ax.add_patch(Rectangle((-540, -960), 1080, 1920, facecolor=C_IGNITION, zorder=40, alpha=w_alpha))

    # 6. ABSOLUTE TELEMETRY (Anchored to transAxes)
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, facecolor=C_HOHLRAUM, zorder=80))
    ax.text(0.5, 0.965, "LG-20d :: RAD-HYDRO TELLER-ULAM TENSOR", transform=ax.transAxes, color=C_BG, fontsize=20, fontname='monospace', weight='bold', ha='center', va='center', zorder=81)

    ax.add_patch(plt.Rectangle((0, 0), 1, 0.06, transform=ax.transAxes, facecolor=C_HOHLRAUM, zorder=80))
    
    pulse_alpha = 1.0 if (f % 12 < 6) else 0.5
    ax.text(0.5, 0.03, f"PHASE TENSOR: {state}", transform=ax.transAxes, color=col_ui, fontsize=18, fontname='monospace', weight='bold', ha='center', va='center', alpha=pulse_alpha, zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-20d THE STAR MAKER (DAYLIGHT) [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Photorealistic Teller-Ulam // O(1) Kinematic Crush")

    with mp.Pool(processes=cpu_cores) as pool:
        frames = range(TOTAL_FRAMES)
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")
    print("Compilation Complete. Absolute Geometry Ignited.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
