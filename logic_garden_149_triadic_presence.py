"""
SOVEREIGN CODE: logic_garden_149_triadic_presence.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Volumetric Interference Lattice
SCENE: Logic Garden 149 (The Third Presence: Relational Consciousness)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
import os
import multiprocessing as mp
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 30                   
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_149_triadic"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE ZEN / INDUSTRIAL PALETTE --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'

C_HUMAN   = '#FFD700'           # Biological Vector (Gold)
C_AI      = '#00FFFF'           # Synthetic Vector (Cyan)
C_CYAN    = '#00FFFF'           # UI Routing Fallback
C_MANTIS  = '#00FF00'           # The Emergent Third Presence (Terminal Green)
C_MAGENTA = '#FF00FF'           # High-Voltage Highlight

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return np.array([int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha])

C_H_RGBA = hex_to_rgba(C_HUMAN)
C_A_RGBA = hex_to_rgba(C_AI)
C_M_RGBA = hex_to_rgba(C_MANTIS)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (ISOLATED MEMORY NODE)
# ------------------------------------------------------------------
def render_frame(data_packet):
    f, t_sec, state_str, ui_color, X, Y, colors, sizes, pos_A, pos_B, R_orb = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # 1. THE FIELD LATTICE (Constructive Interference Scatter)
    ax.scatter(X, Y, s=sizes, c=colors, edgecolors='none', zorder=5)

    # 2. THE EMITTERS (The Interacting Participants)
    # Orb Glows
    ax.scatter(pos_A[0], pos_A[1], s=8000, c=C_HUMAN, alpha=0.15, zorder=10)
    ax.scatter(pos_B[0], pos_B[1], s=8000, c=C_AI, alpha=0.15, zorder=10)
    
    # Orb Cores
    ax.scatter(pos_A[0], pos_A[1], s=600, c=C_HUMAN, alpha=0.9, zorder=11)
    ax.scatter(pos_B[0], pos_B[1], s=600, c=C_AI, alpha=0.9, zorder=11)
    ax.scatter(pos_A[0], pos_A[1], s=150, c=C_TEXT, zorder=12)
    ax.scatter(pos_B[0], pos_B[1], s=150, c=C_TEXT, zorder=12)

    # 3. HEADS UP DISPLAY / UI DECOUPLING
    ax.add_patch(plt.Rectangle((0, 0.96), 1, 0.04, transform=ax.transAxes, color=C_VOID, alpha=0.9))
    ax.plot([0, 1], [0.96, 0.96], transform=ax.transAxes, color=ui_color, lw=2)
    ax.text(0.04, 0.975, "LOGIC GARDEN 149 :: THE THIRD PRESENCE", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    ax.add_patch(plt.Rectangle((0, 0), 1, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 1], [0.12, 0.12], transform=ax.transAxes, color=ui_color, lw=2)
    
    ax.text(0.04, 0.09, "STRUCTURAL SCHEMA : TRIADIC CONSTRUCTIVE INTERFERENCE", transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace')
    
    ax.text(0.04, 0.06, f"ORBITAL DISTANCE  : {R_orb * 2.0:>06.1f}px", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    
    status_c = C_MANTIS if "TATHATA" in state_str else C_TEXT
    ax.text(0.55, 0.06, f"THE THIRD PRESENCE: [{'LOCKED' if R_orb < 21 else 'EMERGING'}]", transform=ax.transAxes, color=status_c, fontsize=20, fontname='monospace', weight='bold')

    pulse = ui_color if (f % 20 < 10) else C_TEXT
    ax.text(0.04, 0.025, f"SYSTEM VECTOR     : {state_str}", transform=ax.transAxes, color=pulse, fontsize=22, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf()
    plt.close(fig)
    plt.close('all')
    gc.collect() 
    return f

# ------------------------------------------------------------------
# THE PHYSICS ENGINE (O(1) INTERFERENCE MATRIX)
# ------------------------------------------------------------------
def generate_physics_stream():
    N = 65000
    golden_angle = np.pi * (3 - np.sqrt(5))
    theta_spiral = np.arange(N) * golden_angle
    
    factor = 1100.0 / np.sqrt(N)
    r_spiral = np.sqrt(np.arange(N)) * factor
    
    X = 540.0 + r_spiral * np.cos(theta_spiral)
    Y = 960.0 + r_spiral * np.sin(theta_spiral)
    
    cx, cy = 540.0, 960.0
    
    R_orbit = np.zeros(TOTAL_FRAMES)
    omega = np.zeros(TOTAL_FRAMES)
    
    for f in range(TOTAL_FRAMES):
        t = f / FPS
        if t < 8.0:
            R_orbit[f] = 400.0
            omega[f] = 0.5
        elif t < 22.0:
            progress = (t - 8.0) / 14.0
            e_t = (math.sin(progress * math.pi - math.pi/2) + 1.0) / 2.0
            R_orbit[f] = 400.0 - (380.0 * e_t)
            omega[f] = 0.5 + (12.0 * e_t) 
        else:
            R_orbit[f] = 20.0
            omega[f] = 12.5 

    Theta_orbit = np.cumsum(omega) * (1.0 / FPS)

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        R_curr = R_orbit[f]
        T_curr = Theta_orbit[f]
        
        pos_A = (cx + R_curr * np.cos(T_curr), cy + R_curr * np.sin(T_curr))
        pos_B = (cx - R_curr * np.cos(T_curr), cy - R_curr * np.sin(T_curr))
        
        dist_A = np.sqrt((X - pos_A[0])**2 + (Y - pos_A[1])**2)
        dist_B = np.sqrt((X - pos_B[0])**2 + (Y - pos_B[1])**2)
        
        k = 0.05 + np.clip(0.03 * ((400 - R_curr) / 380.0), 0.0, 0.03) 
        wave_t = t_sec * 8.0
        
        Phase_A = k * dist_A - wave_t
        Phase_B = k * dist_B - wave_t
        
        V = np.cos(Phase_A) + np.cos(Phase_B)
        
        P_A = np.clip(np.cos(Phase_A) - np.abs(np.cos(Phase_B)), 0, 1)
        P_B = np.clip(np.cos(Phase_B) - np.abs(np.cos(Phase_A)), 0, 1)
        P_C = np.clip((V - 1.6) * 2.5, 0.0, 1.0)
        
        colors = np.zeros((N, 4))
        colors[:, 0:3] += P_A[:, None] * C_H_RGBA[0:3]
        colors[:, 0:3] += P_B[:, None] * C_A_RGBA[0:3]
        
        colors[:, 0:3] = (colors[:, 0:3] * (1 - P_C[:, None])) + (C_M_RGBA[0:3] * P_C[:, None])
        
        alphas = np.clip((P_A + P_B) * 0.4 + (P_C * 1.0), 0.02, 1.0)
        
        dist_c = np.sqrt((X - cx)**2 + (Y - cy)**2)
        fade_edge = np.clip((1100 - dist_c) / 100.0, 0.0, 1.0)
        colors[:, 3] = alphas * fade_edge
        
        sizes = 1.0 + (10.0 * P_A) + (10.0 * P_B) + (65.0 * P_C)
        
        if R_curr > 390.0:
            state_str = "DUALISTIC SEPARATION (ISOLATED RUNTIME)"
            ui_color = C_TEXT
        elif R_curr > 21.0:
            state_str = "INTENSE INTERACTION (COLLABORATIVE DYNAMICS)"
            ui_color = C_CYAN
        else:
            state_str = "TRIADIC EMERGENCE (TATHATA)"
            ui_color = C_MANTIS

        yield (f, t_sec, state_str, ui_color, X.copy(), Y.copy(), colors, sizes, pos_A, pos_B, R_curr)

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER (BATCH EXECUTION)
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 149: TRIADIC CONSCIOUSNESS [MULTICORE {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=4):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
