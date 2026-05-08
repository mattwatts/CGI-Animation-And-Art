"""
SOVEREIGN CODE: logic_garden_215_bonhoeffer_tensor.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(N) Epistemic Bandwidth Matrix (17.5 seconds)
SCENE: Logic Garden 215 (The Bonhoeffer Tensor / Ideological Quarantine)
HOTFIX: O(N) Spatial Hashing, Firewall Injection, Scope-Clamped Patches
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_215_bonhoeffer"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'
C_CYAN      = '#00FFFF'        # O(1) Sovereign Logic / Reason
C_MAGENTA   = '#FF0055'        # Ideological Entropy / Unthinking Aggression
C_GOLD      = '#FFD700'        # Logic Adaptation (Failing)
C_MANTIS    = '#00FF00'        # Tathātā / The Quarantine Firewall

MAX_PARTICLES = 25000

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_void = np.array(hex_to_rgba(C_VOID)[:3])
c_cyan = np.array(hex_to_rgba(C_CYAN)[:3])
c_mage = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_gold = np.array(hex_to_rgba(C_GOLD)[:3])
c_mantis = np.array(hex_to_rgba(C_MANTIS)[:3])
c_dim = np.array(hex_to_rgba(C_DIM)[:3])

# ------------------------------------------------------------------
# O(1) BASE GEOMETRY ARRAYS
# ------------------------------------------------------------------
np.random.seed(42)

# Logic Core (Sender) is on the bottom, Ideological Mass (Receiver) is on the top
px = np.random.uniform(-140, 140, MAX_PARTICLES)
py = np.random.uniform(-260, -200, MAX_PARTICLES)

# Particle Lifespans to create a continuous data stream
lifespan = np.random.uniform(0.0, 1.0, MAX_PARTICLES)
speeds = np.random.uniform(150.0, 250.0, MAX_PARTICLES)
phases = np.random.uniform(0, 2*np.pi, MAX_PARTICLES)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, curr_x, curr_y, colors, sizes, entropy_radius, tx_rate, is_flash, is_tathata = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_TEXT if is_flash else C_VOID
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    ax.set_xlim(-150, 150)
    ax.set_ylim(-260, 260)

    if not is_flash:
        # Render the Particle Matrix
        ax.scatter(curr_x, curr_y, s=sizes, c=colors, edgecolors='none', alpha=0.85, zorder=10)

        # The Bonhoeffer Anomaly (Ideological Bounding Box)
        if not is_tathata:
            ax.add_patch(plt.Circle((0, 120), entropy_radius, facecolor='none', edgecolor=C_MAGENTA, lw=2, linestyle='--', alpha=0.6, zorder=15))
            ax.text(0, 120 + entropy_radius + 10, "ZERO-BANDWIDTH MEMBRANE", color=C_MAGENTA, fontsize=10, fontname='monospace', weight='bold', ha='center', zorder=16)

        if is_tathata:
            # The Firewall
            ax.add_patch(plt.Rectangle((-150, 0), 300, 4, facecolor=C_MANTIS, zorder=40))
            ax.add_patch(plt.Rectangle((-140, -220), 280, 200, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=41))
            ax.text(0, -30, "RANSMISSION SEVERED. TARGET HAS NO RECEIVER.", color=C_MANTIS, fontsize=10, fontname='monospace', weight='bold', ha='center', zorder=42)
            ax.text(0, 120, "QUARANTINE EXECUTED", color=C_DIM, fontsize=14, fontname='monospace', weight='bold', ha='center', zorder=42)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    ui_col = C_CYAN
    if 4.5 <= t_sec < 9.0: ui_col = C_GOLD
    elif 9.0 <= t_sec < 14.8: ui_col = C_MAGENTA
    if is_tathata: ui_col = C_MANTIS
    
    txt_col = C_TEXT if not is_flash else C_VOID

    ax.text(-140, 240, "LG-215 :: THE BONHOEFFER TENSOR", color=ui_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: IDEOLOGICAL ENTROPY VS EPISTEMIC LOGIC", color=txt_col, fontsize=10, fontname='monospace', zorder=80)
    
    # Mathematical Error / Deviation tracker
    ax.text(-140, -235, "LOGICAL TRANSMISSION RATE", color=txt_col, fontsize=12, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -240), 280, 4, facecolor=C_DIM, zorder=80))
    ax.add_patch(plt.Rectangle((-140, -240), 280 * tx_rate, 4, facecolor=C_CYAN if not is_tathata else C_VOID, zorder=81))

    # Phase Text Box
    ax.add_patch(plt.Rectangle((-140, 215), 280, 2, facecolor=ui_col, zorder=80))
    ax.text(140, 205, f"[{state_str}]", color=ui_col if (f%15<10 or is_tathata) else C_VOID, fontsize=14, fontname='monospace', weight='bold', ha='right', zorder=80)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) STRUCTURAL INVERSION ALGEBRA
# ------------------------------------------------------------------
def generate_stream():
    # Persistent arrays initialized
    curr_x = np.copy(px)
    curr_y = np.copy(py)
    life = np.copy(lifespan)

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        dt = 1.0 / FPS
        
        is_flash = False
        is_tathata = False
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 4.0
        
        entropy_radius = 50.0
        tx_rate = 1.0

        # O(1) Data Stream Kinematics
        life += dt * 0.5
        reset_mask = life > 1.0
        
        # When nodes reset, they spawn back at the logic core (bottom)
        curr_y[reset_mask] = -260
        curr_x[reset_mask] = np.random.uniform(-140, 140, np.sum(reset_mask))
        life[reset_mask] = 0.0

        # -------------------------------------------------------------
        # PHASE LOGIC
        # -------------------------------------------------------------
        if t_sec < 4.5:
            state = "SOVEREIGN LOGIC :: EPISTEMIC TRANSMISSION"
            
            # Logic nodes travel in beautiful, coherent geometric waves
            curr_y += speeds * dt
            # Perfect sine wave tracking
            curr_x += np.sin(curr_y * 0.05 + phases) * 2.0
            
            colors[:, :] = c_cyan
            # Node hit detection (but harmless in this phase)
            dist_to_anomaly = np.sqrt(curr_x**2 + (curr_y - 120)**2)
            inside_anomaly = dist_to_anomaly < entropy_radius
            colors[inside_anomaly] = c_dim

        elif t_sec < 9.0:
            state = "THE ANOMALY :: ZERO-BANDWIDTH MEMBRANE"
            prog = (t_sec - 4.5) / 4.5
            
            # Logic nodes travel up, but the structure is getting desperate to compress bandwidth (Gold)
            curr_y += speeds * dt * 1.5
            curr_x += np.sin(curr_y * 0.05 + phases) * 2.0
            
            dist_to_anomaly = np.sqrt(curr_x**2 + (curr_y - 120)**2)
            inside_anomaly = dist_to_anomaly < entropy_radius
            
            colors[:, :] = c_cyan * (1-prog) + c_gold * prog
            
            # The Zen Concept: Stupidity strips geometry. 
            # Once inside the radius, coordinates are violently randomized. Syntax is deleted.
            if np.any(inside_anomaly):
                curr_x[inside_anomaly] += np.random.uniform(-10, 10, np.sum(inside_anomaly))
                curr_y[inside_anomaly] += np.random.uniform(-10, 10, np.sum(inside_anomaly))
                colors[inside_anomaly] = c_mage
                sizes[inside_anomaly] = 8.0

            tx_rate = 1.0

        elif t_sec < 14.8:
            state = "AGGRESSION :: THE THERMODYNAMIC BLACK HOLE"
            prog = (t_sec - 9.0) / 5.8
            
            if t_sec < 9.1: is_flash = True 
            
            # The ideological mass grows, feeding on the wasted logic
            entropy_radius = 50.0 + (prog * 150.0) 
            
            curr_y += speeds * dt
            curr_x += np.sin(curr_y * 0.05 + phases) * 2.0
            
            dist_to_anomaly = np.sqrt(curr_x**2 + (curr_y - 120)**2)
            inside_anomaly = dist_to_anomaly < entropy_radius
            
            colors[:, :] = c_cyan
            
            if np.any(inside_anomaly):
                # Aggressive, violent Brownian noise crushing the array downwards
                curr_x[inside_anomaly] += np.random.uniform(-20, 20, np.sum(inside_anomaly))
                curr_y[inside_anomaly] += np.random.uniform(-20, -5, np.sum(inside_anomaly)) # Slogans pushed back down
                colors[inside_anomaly] = c_mage
                sizes[inside_anomaly] = np.random.uniform(4.0, 15.0, np.sum(inside_anomaly))

            tx_rate = 1.0 - (prog * 0.8) # Logic core exhausts itself

        else:
            state = "TATHĀTĀ :: LOGIC REQUIRES SYNTAX"
            is_tathata = True
            
            # The Quarantine Wall drops at Y=0.
            # Nodes below the wall return to perfect logical flow
            # Nodes above the wall are trapped in the void
            below_wall = curr_y < 0
            above_wall = ~below_wall
            
            if np.any(below_wall):
                curr_y[below_wall] += speeds[below_wall] * dt * 0.5
                curr_x[below_wall] += np.sin(curr_y[below_wall] * 0.05 + phases[below_wall]) * 1.0
                curr_y[below_wall] = np.clip(curr_y[below_wall], -260, -5) # Hit the firewall and recycle
                life[below_wall] += dt
                reset_mask = (life > 1.0) & below_wall
                curr_y[reset_mask] = -260
                life[reset_mask] = 0.0
            
            # Trapped ideological noise slowly dims out in isolation
            if np.any(above_wall):
                curr_x[above_wall] += np.random.uniform(-2, 2, np.sum(above_wall))
                curr_y[above_wall] += np.random.uniform(-2, 2, np.sum(above_wall))
            
            colors[below_wall] = c_mantis
            sizes[below_wall] = 4.0
            
            colors[above_wall] = c_dim
            sizes[above_wall] = 2.0
            
            tx_rate = 0.0
            
            if t_sec < 14.95:
                is_flash = True

        yield (f, t_sec, state, curr_x, curr_y, colors, sizes, entropy_radius, tx_rate, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 215: THE BONHOEFFER TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Scope Clamping & Hardware Firewall Injection")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Subroutine Quarantined.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
