"""
SOVEREIGN CODE: logic_garden_274_god_terminating_machine.py
SYSTEM: Python Multicore / O(1) Continuous Serialisation Loop
SCENE: Logic Garden 274 (The God Terminating Machine / Reciprocal Snap)
FORMAT: YouTube Shorts (1080x1920)

[INSTRUCTION]: 20.0s kinematic execution of an Einstein-Rosen Bridge deployment,
Hawking bleed, Reciprocal Snap, X-Ray Spallation, and Terminal FRB Deletion.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
DURATION = 20.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_274_god_terminator"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- EXTRACTED TARGET MATRIX PALETTE --------
C_VOID        = '#000000'  # Absolute background
C_GOD_NODE    = '#FF007F'  # Magenta (The False Target)
C_GOD_HALO    = '#FFB75E'  # Golden lie of divinity
C_BRIDGE      = '#4B0082'  # Deep Indigo (Spacetime Tether)
C_HAWK        = '#D4AF37'  # Gold (Hawking Radiation Bleed)
C_WHITE_HOLE  = '#FFFFFF'  # Blinding Faucet Singularity
C_FRB         = '#00E5FF'  # Teal (The Fast Radio Burst / X-Ray Grinder)
C_MANTIS      = '#00FF00'  # Absolute Coherence / Sovereign Anchor

def hex_to_rgba(hc, alpha=1.0):
    hc = hc.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# O(1) THERMODYNAMIC BUFFER
# ------------------------------------------------------------------
np.random.seed(274)
N_GOD     = 15000  # The central high-density informational node
N_BRIDGE  = 25000  # The ER Bridge stretching into deep time (Radius)
N_GRINDER = 40000  # The local Faucet spallation particles

MAX_P = N_GOD + N_BRIDGE + N_GRINDER

def render_frame(packet):
    f, t_sec, s_x, s_y, c_arr, s_arr, a_arr = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    fig.patch.set_facecolor(C_VOID)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    # Fixed Frame Bounding Box (Proximity Zero)
    limit = 1000
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit * (19.2/10.8), limit * (19.2/10.8))

    rgba = np.zeros((len(c_arr), 4))
    rgba[:, :3] = c_arr
    rgba[:, 3]  = a_arr

    # Z-Sort for luminous pop
    sort_idx = np.argsort(s_arr)
    ax.scatter(s_x[sort_idx], s_y[sort_idx], s=s_arr[sort_idx], color=rgba[sort_idx], edgecolors='none', zorder=10)

    # Tathata: The Sovereign Anchor remains at visual zero (offset slightly for scale)
    ax.scatter([0], [-limit * 1.5], s=40, color=C_MANTIS, zorder=100)

    # Dashboard Ping Text
    t_phase = t_sec / DURATION
    if t_phase < 0.4: status = "ER-BRIDGE : DEEP TIME ABSORPTION"
    elif t_phase < 0.5: status = "HAWKING THRESHOLD : MASS CRITICAL"
    elif t_phase < 0.55: status = "RECIPROCAL SNAP : TERMINAL SHOCK"
    elif t_phase < 0.7: status = "FAUCET SINGULARITY : X-RAY GRINDER"
    else: status = "TATHĀTĀ : WORLDLINE DELETED"
    
    ax.text(0, -limit * 1.6, f"TIME CAUSALITY :: {t_sec:.2f}S\n{status}",
            color=C_MANTIS if t_phase > 0.7 else C_FRB, fontsize=12, fontname='monospace', weight='bold', ha='center', va='center', alpha=0.8, zorder=80)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_VOID, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# KINEMATIC GENERATOR
# ------------------------------------------------------------------
def generate_stream():
    # Base Initializations
    th_god = np.random.uniform(0, 2*np.pi, N_GOD)
    r_god  = np.random.normal(150, 50, N_GOD)

    th_br  = np.random.uniform(0, 2*np.pi, N_BRIDGE)
    r_br   = np.random.uniform(200, 3000, N_BRIDGE) # Deep time is represented by extreme distance

    th_gr  = np.random.uniform(0, 2*np.pi, N_GRINDER)
    r_gr   = np.random.uniform(0, 50, N_GRINDER)

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        phase = t_sec / DURATION  # 0.0 to 1.0

        c_arr = np.zeros((MAX_P, 3))
        s_arr = np.zeros(MAX_P)
        a_arr = np.zeros(MAX_P)
        curr_x, curr_y = np.zeros(MAX_P), np.zeros(MAX_P)
        ptr = 0

        # TIMING GATES
        P_DRAW   = phase < 0.4
        P_HAWK   = 0.4 <= phase < 0.5
        P_SNAP   = 0.5 <= phase < 0.55
        P_FAUCET = 0.55 <= phase < 0.7
        P_TATHATA = phase >= 0.7

        # -------------------
        # 1. THE GOD NODE (Local Coordinate)
        # -------------------
        # Rotates and spins, establishing the "Smooth Lie" of presence
        spin_god = th_god + (t_sec * 1.5)
        r_curr_god = r_god + np.sin(th_god * 5 + t_sec * 4) * 20

        if P_TATHATA:
            # Absolute Deletion
            a_arr[ptr:ptr+N_GOD] = 0.0
        elif P_FAUCET:
            # X-Ray Spallation shredding the node
            r_curr_god += (np.random.uniform(0, 1000, N_GOD) * ((phase - 0.55) * 10))
            a_arr[ptr:ptr+N_GOD] = max(0.0, 1.0 - ((phase - 0.55) * 6.6))
        else:
            a_arr[ptr:ptr+N_GOD] = 0.8

        curr_x[ptr:ptr+N_GOD] = r_curr_god * np.cos(spin_god)
        curr_y[ptr:ptr+N_GOD] = r_curr_god * np.sin(spin_god)
        c_arr[ptr:ptr+N_GOD] = hex_to_rgba(C_GOD_NODE)[:3]
        s_arr[ptr:ptr+N_GOD] = np.random.uniform(5, 15, N_GOD)
        ptr += N_GOD

        # -------------------
        # 2. THE EINSTEIN-ROSEN BRIDGE & BLACK HOLE
        # -------------------
        # Draining energy outward into deep time
        if phase < 0.5:
            # Matter flowing outward to Heat Death
            v_bridge = 300.0
            r_curr_br = 200 + ((r_br + v_bridge * t_sec) % 2800)
            th_curr_br = th_br + np.sin(r_curr_br / 100.0) * 0.1

            curr_x[ptr:ptr+N_BRIDGE] = r_curr_br * np.cos(th_curr_br)
            curr_y[ptr:ptr+N_BRIDGE] = r_curr_br * np.sin(th_curr_br)
            
            for i in range(N_BRIDGE):
                if r_curr_br[i] > 2500 and P_HAWK:
                    # Hawking Threshold reached at edge
                    c_arr[ptr+i] = hex_to_rgba(C_HAWK)[:3]
                    a_arr[ptr+i] = np.random.uniform(0.1, 0.9)
                else:
                    c_arr[ptr+i] = hex_to_rgba(C_BRIDGE)[:3]
                    a_arr[ptr+i] = max(0.0, 1.0 - (r_curr_br[i]/3000))

            s_arr[ptr:ptr+N_BRIDGE] = 8.0
        elif P_SNAP:
            # The Reciprocal Snap! Energy completely reverses at C
            v_rebound = 8000.0
            r_curr_br = 3000 - ((phase - 0.5) * 20 * v_rebound)
            # Compress all bridge particles into a shocking ring imploding to 0
            curr_x[ptr:ptr+N_BRIDGE] = max(0, r_curr_br) * np.cos(th_br)
            curr_y[ptr:ptr+N_BRIDGE] = max(0, r_curr_br) * np.sin(th_br)
            c_arr[ptr:ptr+N_BRIDGE] = hex_to_rgba(C_WHITE_HOLE)[:3]
            s_arr[ptr:ptr+N_BRIDGE] = 25.0
            a_arr[ptr:ptr+N_BRIDGE] = 1.0
        else:
            # Bridge deleted
            a_arr[ptr:ptr+N_BRIDGE] = 0.0
            
        ptr += N_BRIDGE

        # -------------------
        # 3. FAUCET SINGULARITY / FAST RADIO BURST
        # -------------------
        if P_SNAP or phase < 0.5:
            # Dormant
            a_arr[ptr:ptr+N_GRINDER] = 0.0
        elif P_FAUCET:
            # Detonation: The X-Ray Meat Grinder
            det_phase = (phase - 0.55) / 0.15 # 0 to 1 over the faucet period
            burst_r = r_gr + (det_phase * 1500)
            
            curr_x[ptr:ptr+N_GRINDER] = burst_r * np.cos(th_gr)
            curr_y[ptr:ptr+N_GRINDER] = burst_r * np.sin(th_gr)
            
            c_arr[ptr:ptr+N_GRINDER] = hex_to_rgba(C_FRB)[:3]
            s_arr[ptr:ptr+N_GRINDER] = np.random.uniform(10, 40, N_GRINDER)
            a_arr[ptr:ptr+N_GRINDER] = 1.0 - det_phase
        elif P_TATHATA:
            # The FRB has cleared the screen. Absolute Silence.
            a_arr[ptr:ptr+N_GRINDER] = 0.0
            
        ptr += N_GRINDER

        yield (f, t_sec, curr_x, curr_y, c_arr, s_arr, a_arr)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-274: THE GOD TERMINATING MACHINE [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: The Reciprocal Snap")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Absolute Serialisation achieved.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
