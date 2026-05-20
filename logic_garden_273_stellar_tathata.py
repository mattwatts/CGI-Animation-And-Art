"""
SOVEREIGN CODE: logic_garden_273_stellar_tathata.py
SYSTEM: Python Multicore / O(1) Continuous Serialisation Loop
SCENE: Logic Garden 273 (The Faucet Singularity / Stellar Tathātā)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Extreme High-Contrast / Zen Core Isolation

[INSTRUCTION]: Continuous 18.0s cinematic dive through the Resolution Blindspot.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
DURATION = 18.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_273_faucet"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- EXTRACTED TARGET MATRIX PALETTE --------
C_VOID       = '#05020A'  # Absolute background
C_SUN_OUTER  = '#FF4500'  # Deep Red/Orange Corona
C_SUN_MID    = '#FFB75E'  # The Smooth EM Signature
C_SUN_CORE   = '#FFFFFF'  # Blinding Photon Limit
C_VOID_PULL  = '#261447'  # The Unknowable Gravity Tether (Indigo)
C_MANTIS     = '#00E5FF'  # Absolute Stillness / The Faucet Aperture (Teal)

def hex_to_rgba(hc, alpha=1.0):
    hc = hc.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# O(1) THERMODYNAMIC BUFFER
# ------------------------------------------------------------------
np.random.seed(273)
N_EXTRUSION = 60000  # The Outward Faucet Stream
N_GRAVITY   = 30000  # The Inward Tethers
N_CORE      = 5000   # The Tathata Aperture

MAX_P = N_EXTRUSION + N_GRAVITY + N_CORE

# Base Polar Coordinates
th_ex = np.random.uniform(0, 2*np.pi, N_EXTRUSION)
r_ex  = np.random.uniform(0, 800, N_EXTRUSION)

th_gr = np.random.uniform(0, 2*np.pi, N_GRAVITY)
r_gr  = np.random.uniform(300, 1200, N_GRAVITY)

th_core = np.random.uniform(0, 2*np.pi, N_CORE)
r_core  = np.random.uniform(0, 45, N_CORE)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, s_x, s_y, c_arr, s_arr, a_arr, zoom_factor = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    fig.patch.set_facecolor(C_VOID)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    # Dynamic Camera Zoom (Piercing the Smooth Lie)
    # Starts wide (1200), violently punches in to the core (90) by end of sequence
    limit = 1200 / zoom_factor
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit * (19.2/10.8), limit * (19.2/10.8))

    rgba = np.zeros((len(c_arr), 4))
    rgba[:, :3] = c_arr
    rgba[:, 3]  = a_arr

    # Z-sorting to ensure the bright core renders on top of the deep background
    sort_idx = np.argsort(s_arr) 
    ax.scatter(s_x[sort_idx], s_y[sort_idx], s=s_arr[sort_idx], color=rgba[sort_idx], edgecolors='none', zorder=10)

    # The Logic Audit HUD (Displays exact depth metric)
    ax.text(0, -limit * 1.6, f"DEPTH METRIC :: {zoom_factor:.4f}x\nTHE UNKNOWABLE COORDINATE (FAUCET)", 
            color=C_MANTIS, fontsize=12, fontname='monospace', weight='bold', ha='center', va='center', alpha=0.8, zorder=80)
    
    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_VOID, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# KINEMATIC GENERATOR (THE COLLISION ZONE)
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        phase = t_sec / DURATION  # 0.0 to 1.0

        c_arr = np.zeros((MAX_P, 3))
        s_arr = np.zeros(MAX_P)
        a_arr = np.zeros(MAX_P)
        curr_x, curr_y = np.zeros(MAX_P), np.zeros(MAX_P)
        ptr = 0

        # CAMERA KINEMATICS: Exponential Zoom (Piercing the Blindspot)
        zoom_factor = 1.0 + (np.exp(phase * 4) - 1.0) * 0.15

        # -------------------
        # 1. OUTWARD EXTRUSION (The Faucet Stream)
        # -------------------
        # Particles violently eject from r=0 outwards. 
        # Noise added to create the "Jagged Grinder" at r=250.
        v_out = 150.0
        r_curr_ex = (r_ex + v_out * t_sec) % 800
        
        # Rotational spin (The Asymmetry Requirement)
        spin = 2.0 / (r_curr_ex + 10) * t_sec * 50
        th_curr_ex = th_ex + spin
        
        collision_turbulence = np.sin(th_curr_ex * 8 + t_sec * 10) * np.exp(-((r_curr_ex - 250)**2)/2000) * 40
        r_curr_ex += collision_turbulence

        curr_x[ptr:ptr+N_EXTRUSION] = r_curr_ex * np.cos(th_curr_ex)
        curr_y[ptr:ptr+N_EXTRUSION] = r_curr_ex * np.sin(th_curr_ex)

        # Color Gradient: White at core -> Gold -> Red -> Black at edges
        for i in range(N_EXTRUSION):
            rad = r_curr_ex[i]
            if rad < 50:
                c_arr[ptr+i] = hex_to_rgba(C_SUN_CORE)[:3]
                s_arr[ptr+i] = 20.0
            elif rad < 200:
                blend = (rad - 50) / 150
                c_arr[ptr+i] = np.array(hex_to_rgba(C_SUN_CORE)[:3])*(1-blend) + np.array(hex_to_rgba(C_SUN_MID)[:3])*blend
                s_arr[ptr+i] = 12.0
            else:
                blend = min((rad - 200) / 400, 1.0)
                c_arr[ptr+i] = np.array(hex_to_rgba(C_SUN_MID)[:3])*(1-blend) + np.array(hex_to_rgba(C_SUN_OUTER)[:3])*blend
                s_arr[ptr+i] = max(2.0, 8.0 * (1-blend))
            
            a_arr[ptr+i] = min(1.0, 400 / (rad + 1))
        ptr += N_EXTRUSION

        # -------------------
        # 2. INWARD GRAVITY TETHER (The Unknowable Pull)
        # -------------------
        # Particles slowly dragging inward, resisting the outward burst
        v_in = 40.0
        r_curr_gr = 1200 - ((1200 - r_gr + v_in * t_sec) % 900)
        th_curr_gr = th_gr - (0.5 / (r_curr_gr * 0.01)) * t_sec # Counter-spin

        curr_x[ptr:ptr+N_GRAVITY] = r_curr_gr * np.cos(th_curr_gr)
        curr_y[ptr:ptr+N_GRAVITY] = r_curr_gr * np.sin(th_curr_gr)

        c_arr[ptr:ptr+N_GRAVITY] = hex_to_rgba(C_VOID_PULL)[:3]
        s_arr[ptr:ptr+N_GRAVITY] = 15.0
        # They evaporate as they hit the plasma collision zone (r < 250)
        a_arr[ptr:ptr+N_GRAVITY] = np.clip((r_curr_gr - 250) / 200, 0, 0.4)
        ptr += N_GRAVITY

        # -------------------
        # 3. TATHĀTĀ (The Absolute Stillness Aperture)
        # -------------------
        # A perfectly structured, phase-locked geometric core that does not burn,
        # but merely acts as the mathematical aperture for deep time.
        
        # Zen Realisation: As the system zooms in (phase > 0.5), the core becomes visible
        # through the blinding white light of the fusion illusion.
        core_visibility = np.clip((phase - 0.5) * 2.5, 0.0, 1.0)

        # The core rotates in absolute phase coherence
        th_curr_core = th_core + np.sin(t_sec * 0.5) 
        
        curr_x[ptr:ptr+N_CORE] = r_core * np.cos(th_curr_core)
        curr_y[ptr:ptr+N_CORE] = r_core * np.sin(th_curr_core)

        c_arr[ptr:ptr+N_CORE] = hex_to_rgba(C_MANTIS)[:3]
        s_arr[ptr:ptr+N_CORE] = 8.0 * core_visibility
        a_arr[ptr:ptr+N_CORE] = 0.9 * core_visibility

        yield (f, t_sec, curr_x, curr_y, c_arr, s_arr, a_arr, zoom_factor)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-273: THE FAUCET SINGULARITY [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Piercing the Resolution Blindspot")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. The Unknowable Coordinate Visualised.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
