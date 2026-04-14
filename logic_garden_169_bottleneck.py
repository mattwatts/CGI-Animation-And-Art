"""
SOVEREIGN CODE: logic_garden_169_bottleneck.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Topological Kinematics (35 seconds)
SCENE: Logic Garden 169 (Geometry of Annihilation / Crossing the T)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import LineCollection
import multiprocessing as mp
import os
import gc
import math

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 35                   
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_169_bottleneck"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_CYAN    = '#00FFFF'          # Enemy Array (Structurally Gagged)
C_GOLD    = '#FFD700'          # Friendly Array (Orthogonal Dominance)
C_MANTIS  = '#00FF00'          # Sovereign Vector Throughput (Perfect Fire)
C_RED     = '#FF0033'          # Error / Friction / Internal Entropy
C_DIM     = '#1A1A24'          # Hardware Grid
C_MAGENTA = '#FF00FF'          # Kinetic Erasure Blooms

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (ISOLATED MEMORY NODE)
# ------------------------------------------------------------------
def render_frame(data_packet):
    f, t_sec, state_str, ui_col, g_pos, c_pos, c_hp, g_wakes, c_wakes, debris, g_fire, c_fire, frictions = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # 1. HARDWARE GRID (THE BATTLESPACE MATRIX)
    for x in range(0, 1080, 108):
        ax.plot([x, x], [0, 1920], color=C_DIM, lw=1, alpha=0.5, zorder=0)
    for y in range(0, 1920, 108):
        ax.plot([0, 1080], [y, y], color=C_DIM, lw=1, alpha=0.5, zorder=0)

    # 2. RENDER WAKES (KINEMATIC HISTORY)
    for i in range(5):
        if len(g_wakes[i]) > 1:
            w_arr = np.array(g_wakes[i])
            ax.plot(w_arr[:,0], w_arr[:,1], color=C_GOLD, lw=3, alpha=0.3, zorder=1)
        if len(c_wakes[i]) > 1 and c_hp[i] > 0:
            w_arr = np.array(c_wakes[i])
            ax.plot(w_arr[:,0], w_arr[:,1], color=C_CYAN, lw=3, alpha=0.3, zorder=1)

    # 3. KINETIC VECTORS (THE MATHEMATICAL EXCHANGE)
    # C_GOLD projecting uninterrupted C_MANTIS beams
    for (gx, gy, cx, cy) in g_fire:
        # Glow
        ax.plot([gx, cx], [gy, cy], color=C_MANTIS, lw=4, alpha=0.3, zorder=2)
        # Core
        ax.plot([gx, cx], [gy, cy], color=C_TEXT, lw=1, alpha=0.9, zorder=3)
        # Impact Bloom
        ax.scatter([cx], [cy], s=400, c=C_MANTIS, alpha=0.2, zorder=4)

    # C_CYAN Lead node firing
    for (cx, cy, gx, gy) in c_fire:
        ax.plot([cx, gx], [cy, gy], color=C_CYAN, lw=2, alpha=0.6, zorder=2)

    # C_CYAN Structurally Gagged friction (Nodes 2-5 shooting themselves)
    for (cx, cy, ex, ey) in frictions:
        ax.plot([cx, ex], [cy, ey], color=C_RED, lw=2, linestyle=':', alpha=0.8, zorder=2)
        ax.scatter([ex], [ey], s=80, marker='x', color=C_RED, zorder=4)

    # 4. RENDER DEBRIS (ENTROPY BLOOMS)
    if debris:
        d_arr = np.array(debris)
        ax.scatter(d_arr[:,0], d_arr[:,1], s=d_arr[:,2], color=C_MAGENTA, alpha=d_arr[:,3], marker='h', zorder=2)

    # 5. RENDER THE NODES (THE HARDWARE)
    for i in range(5):
        # GOLD NODES
        gx, gy = g_pos[i]
        ax.scatter([gx], [gy], s=120, color=C_GOLD, marker='s', zorder=5)
        ax.scatter([gx], [gy], s=600, facecolors='none', edgecolors=C_GOLD, lw=2, alpha=0.4, zorder=4)

        # CYAN NODES
        if c_hp[i] > 0:
            cx, cy = c_pos[i]
            hp_ratio = c_hp[i] / 100.0
            col = hex_to_rgba(C_CYAN, hp_ratio)
            ax.scatter([cx], [cy], s=120 + ((1.0-hp_ratio)*100), color=col, marker='^', zorder=5)
            # Integrity Ring
            ax.scatter([cx], [cy], s=600, facecolors='none', edgecolors=C_CYAN, lw=2, alpha=hp_ratio, zorder=4)

    # 6. TELEMETRY WIDGETS & BOUNDING BOXES
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2)
    ax.text(0.04, 0.965, "LOGIC GARDEN 169 :: SELF-SHADOWING FRICTION", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

    # Kinematic Data Panel (Top Left)
    live_cyan = sum(1 for hp in c_hp if hp > 0)
    tput_gold = (5.0 / 5.0) * 100
    tput_cyan = (1.0 / live_cyan * 100) if live_cyan > 0 else 0

    ax.text(0.04, 0.88, f"[ORTHOGONAL ARRAY : GOLD]", transform=ax.transAxes, color=C_GOLD, fontsize=20, fontname='monospace', weight='bold')
    ax.text(0.04, 0.85, f"VECTOR THROUGHPUT : {tput_gold:.0f}%", transform=ax.transAxes, color=C_MANTIS, fontsize=18, fontname='monospace')
    
    ax.text(0.04, 0.80, f"[LONGITUDINAL QUEUE : CYAN]", transform=ax.transAxes, color=C_CYAN, fontsize=20, fontname='monospace', weight='bold')
    ax.text(0.04, 0.77, f"VECTOR THROUGHPUT   : {tput_cyan:.0f}%", transform=ax.transAxes, color=C_RED, fontsize=18, fontname='monospace')
    
    gag_nodes = max(0, live_cyan - 1)
    ax.text(0.04, 0.74, f"STRUCTURALLY GAGGED : {gag_nodes} NODES", transform=ax.transAxes, color=C_RED if gag_nodes > 0 else C_DIM, fontsize=18, fontname='monospace')

    # Bottom Terminal
    ax.add_patch(plt.Rectangle((0, 0), 0.95, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 0.95], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2)
    
    pulse = ui_col if (f % 60 < 30) or ui_col == C_MANTIS else C_TEXT
    ax.text(0.04, 0.08, "GEOMETRIC RESOLUTION:", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=24, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf(); plt.close(fig); plt.close('all'); gc.collect() 
    return f

# ------------------------------------------------------------------
# PHYSICS ENGINE (TOPOLOGICAL KINEMATICS)
# ------------------------------------------------------------------
def generate_physics_stream():
    # Initial Arrays
    g_start_x = np.linspace(-200, 200, 5) # Moves right
    g_start_y = np.full(5, 1400.0)
    
    c_start_x = np.full(5, 540.0)
    c_start_y = np.linspace(500, -100, 5) # Moves up (node 0 is lead)
    
    c_hp = np.full(5, 100.0)
    
    g_wakes = [[] for _ in range(5)]
    c_wakes = [[] for _ in range(5)]
    global_debris = []

    # Constants
    FIRE_RATE = 4 # Frames between shots
    DPS = 100.0 / (FPS * 3.5) # Time to kill 1 node under full focus (~3.5 sec)

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        # Kinematics Execution
        # Gold drifts gracefully to the right mapping the orthogonal cap
        g_pos = [(g_start_x[i] + 540 + (t_sec * 25.0), g_start_y[i] - min(t_sec*8, 80)) for i in range(5)]
        # Cyan drives hard upward into the bottleneck
        c_pos = [(c_start_x[i], c_start_y[i] + (t_sec * 45.0)) for i in range(5)]
        
        g_fire = []
        c_fire = []
        frictions = []
        
        # Phase Mechanics
        if t_sec < 5.0:
            state = "[01] TOPOLOGICAL INTERSECTION IMMINENT"
            ui_col = C_VOID
        elif t_sec < 30.0:
            state = "[02] BOTTLENECK ACTIVE: OPPRESSIVE BANDWIDTH CAP"
            ui_col = C_GOLD
        else:
            state = "[03] TATHĀTĀ: OPPONENT CONSUMED BY OWN GEOMETRY"
            ui_col = C_MANTIS

        # Combat Matrix Processing
        if t_sec >= 5.0 and t_sec < 30.0:
            # Elect target (the first Cyan node still alive)
            lead_idx = -1
            for i in range(5):
                if c_hp[i] > 0:
                    lead_idx = i
                    break
            
            if lead_idx != -1:
                # 1. Gold fires on Lead Cyan (O(N) orthogonal supremacy)
                c_hp[lead_idx] -= (5 * DPS)
                if c_hp[lead_idx] <= 0:
                    # Explosive bloom payload
                    c_hp[lead_idx] = 0
                    for _ in range(40):
                        dx = np.random.uniform(-1, 1) * 30
                        dy = np.random.uniform(-1, 1) * 30
                        global_debris.append([c_pos[lead_idx][0], c_pos[lead_idx][1], np.random.uniform(5, 40), 1.0, dx, dy])

                if f % FIRE_RATE == 0:
                    for i in range(5):
                        g_fire.append((g_pos[i][0], g_pos[i][1], c_pos[lead_idx][0], c_pos[lead_idx][1]))
                        
                # 2. Cyan attempts return fire
                # Lead node fires fine (if alive)
                if c_hp[lead_idx] > 0 and (f % FIRE_RATE == 0):
                    # Target middle gold node
                    c_fire.append((c_pos[lead_idx][0], c_pos[lead_idx][1], g_pos[2][0], g_pos[2][1]))
                
                # Gagged Nodes generate Self-Shadowing Friction
                for i in range(lead_idx + 1, 5):
                    if c_hp[i] > 0 and (f % (FIRE_RATE * 2) == 0):
                        # Blocked by the node strictly in front of them
                        cx, cy = c_pos[i]
                        ex, ey = c_pos[i-1][0] + np.random.uniform(-5,5), c_pos[i-1][1] - 20
                        frictions.append((cx, cy + 20, ex, ey))

        # Update Debris Vectors
        alive_debris = []
        for d in global_debris:
            d[0] += d[4] * (1.0/FPS) # x += dx
            d[1] += d[5] * (1.0/FPS) - 1.5 # y += dy - gravity drift
            d[3] -= 0.02 # alpha decay
            if d[3] > 0:
                alive_debris.append(d)
        global_debris = alive_debris

        # Store Wake History
        for i in range(5):
            if f % 3 == 0:
                g_wakes[i].append(g_pos[i])
                if len(g_wakes[i]) > 25: g_wakes[i].pop(0)
                
                if c_hp[i] > 0:
                    c_wakes[i].append(c_pos[i])
                    if len(c_wakes[i]) > 15: c_wakes[i].pop(0)

        # Snapshot cloning
        gw = [list(w) for w in g_wakes]
        cw = [list(w) for w in c_wakes]
        deb = [list(d) for d in global_debris]

        yield (f, t_sec, state, ui_col, g_pos.copy(), c_pos.copy(), c_hp.copy(), gw, cw, deb, g_fire, c_fire, frictions)

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 169: GEOMETRY OF ANNIHILATION [CORES: {cpu_cores}]")
    print(f"Tracking Topological Intersection over {TOTAL_FRAMES} kinematic states.")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
