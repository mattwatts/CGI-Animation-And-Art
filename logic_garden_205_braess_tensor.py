"""
SOVEREIGN CODE: logic_garden_205_braess_tensor.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(N) Fluid Network Topology (17.5 seconds)
SCENE: Logic Garden 205 (The Braess Tensor / Nash Equilibrium Deadlock)
HOTFIX: Path Density Penalties & Gaussian Vein Rendering
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
OUT_DIR = "frames_205_braess"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'
C_CYAN      = '#00FFFF'        # Balanced Flow
C_MAGENTA   = '#FF0055'        # Thermodynamic Deadlock / Nash Cascade
C_GOLD      = '#FFD700'        # The O(1) Zero-Friction Highway
C_MANTIS    = '#00FF00'        # Terminal Truth / Structure 
C_NODE      = '#222233'

MAX_PARTICLES = 15000

# Graph Coordinates (The Bounding Box)
NODE_A = np.array([0.0, -80.0])   # Ingestion
NODE_B = np.array([-40.0, 0.0])   # Left Peripheral
NODE_C = np.array([40.0, 0.0])    # Right Peripheral
NODE_D = np.array([0.0, 80.0])    # Sink / Extraction

# Path logic arrays
# Path 0: A -> B, Path 1: A -> C
# Path 2: B -> D, Path 3: C -> D
# Path 4: B -> C (The Super Highway)

def get_perpendicular(v):
    mag = np.linalg.norm(v)
    if mag == 0: return np.array([0,0])
    v_norm = v / mag
    return np.array([-v_norm[1], v_norm[0]])

def render_frame(packet):
    f, t_sec, px, py, colors, throughput, latency, phase, is_flash, is_tathata = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_TEXT if is_flash else C_VOID
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    ax.set_xlim(-70, 70)
    ax.set_ylim(-120, 120)

    if not is_flash:
        # Draw base edges
        edges = [
            (NODE_A, NODE_B), (NODE_A, NODE_C),
            (NODE_B, NODE_D), (NODE_C, NODE_D)
        ]
        active_edge_color = C_CYAN if latency < 0.5 else C_MAGENTA
        if is_tathata: active_edge_color = C_MANTIS

        for n1, n2 in edges:
            ax.plot([n1[0], n2[0]], [n1[1], n2[1]], color=C_DIM, lw=10, solid_capstyle='round', zorder=1)
            ax.plot([n1[0], n2[0]], [n1[1], n2[1]], color=active_edge_color, lw=2, alpha=0.3, zorder=2)

        # Draw The Super-Highway (B to C)
        if 5.0 <= t_sec < 14.8:
            ax.plot([NODE_B[0], NODE_C[0]], [NODE_B[1], NODE_C[1]], color=C_DIM, lw=10, zorder=1)
            ax.plot([NODE_B[0], NODE_C[0]], [NODE_B[1], NODE_C[1]], color=C_GOLD, lw=4, alpha=0.8, zorder=2)
            # Pulsing vector arrows
            if f % 10 < 5: ax.plot([NODE_B[0], NODE_C[0]], [NODE_B[1], NODE_C[1]], color=C_TEXT, lw=1, zorder=3)

        # Draw Nodes
        for pt in [NODE_A, NODE_B, NODE_C, NODE_D]:
            nc = C_MANTIS if is_tathata else C_NODE
            ax.scatter([pt[0]], [pt[1]], s=800, c=nc, edgecolors=active_edge_color, lw=3, zorder=10)

        # O(N) Fluid Swarm
        if len(px) > 0:
            ax.scatter(px, py, s=8, c=colors, edgecolors='none', alpha=0.7, zorder=20)
            ax.scatter(px, py, s=1.5, c=C_TEXT, edgecolors='none', alpha=0.9, zorder=21)

    # UI WIDGETS
    ui_col = C_CYAN
    if phase == 2: ui_col = C_GOLD
    if phase == 3: ui_col = C_MAGENTA
    if is_tathata: ui_col = C_MANTIS

    txt_col = C_TEXT if not is_flash else C_VOID
    
    # Header
    ax.text(-65, 110, "LG-205 :: THE BRAESS TENSOR", color=ui_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-65, 105, "OPERATIONS RESEARCH / TOPOLOGICAL DEADLOCK", color=txt_col, fontsize=12, fontname='monospace', zorder=80)
    
    # Live Telemetry
    ax.text(-65, -95, f"THROUGHPUT YIELD : {int(throughput):05d} NODES", color=txt_col, fontsize=16, fontname='monospace', zorder=80)
    
    # Latency Matrix Gauge
    ax.text(-65, -100, f"SYSTEMIC LATENCY : {latency*100:03.0f}%", color=txt_col, fontsize=16, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-65, -103), 130, 2, facecolor=C_DIM, zorder=80))
    lat_w = min(130, 130 * latency)
    bar_c = C_MAGENTA if latency > 0.6 else C_CYAN
    if is_tathata: bar_c = C_MANTIS
    ax.add_patch(plt.Rectangle((-65, -103), lat_w, 2, facecolor=bar_c, zorder=81))

    # Phase Text
    status_txt = "NOMINAL :: BIFURCATED ROUTING"
    if phase == 2: status_txt = "OVERRIDE :: O(1) HIGHWAY DEPLOYED"
    if phase == 3: status_txt = "DEADLOCK :: NASH EQUILIBRIUM CASCADE"
    if is_tathata: status_txt = "TATHĀTĀ :: STRUCTURE REQUIRES FRICTION."

    ax.text(-65, -110, f"[{status_txt}]", color=ui_col if (f%15<10 or is_tathata) else C_VOID, fontsize=16, fontname='monospace', weight='bold', zorder=80)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

def generate_stream():
    # Particle States: 
    # 0 = Void, 1 = Node A, 2 = EdgeAB, 3 = EdgeAC, 4 = EdgeBD, 5 = EdgeCD, 6 = EdgeBC
    
    px = np.zeros(MAX_PARTICLES)
    py = np.zeros(MAX_PARTICLES)
    state = np.zeros(MAX_PARTICLES, dtype=np.int32)
    progress = np.zeros(MAX_PARTICLES)  # 0.0 to 1.0 along the current edge
    offsets = np.random.normal(0, 1.5, MAX_PARTICLES) # Gaussian spread for visual fluid vein

    throughput = 0
    spawns_per_frame = 30
    spawn_idx = 0

    base_speed = 0.02
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        dt = 1.0

        is_flash = False
        is_tathata = False
        phase = 1
        
        if t_sec >= 5.0 and t_sec < 9.0: phase = 2
        if t_sec >= 9.0 and t_sec < 14.8: phase = 3
        if t_sec >= 14.8: phase = 4

        if phase == 4:
            is_tathata = True
            if t_sec < 14.95:
                is_flash = True

        # SPAWN LOGIC AT NODE A
        if phase != 4 or (phase == 4 and not is_flash):
            to_spawn = min(spawns_per_frame, MAX_PARTICLES - np.count_nonzero(state))
            available = np.where(state == 0)[0]
            for i in range(min(to_spawn, len(available))):
                idx = available[i]
                state[idx] = 1
                progress[idx] = 0.0
                px[idx] = NODE_A[0]
                py[idx] = NODE_A[1]

        # CALCULATE DENSITY (The Thermodynamic Trap)
        edge_counts = {2: np.count_nonzero(state == 2), 3: np.count_nonzero(state == 3),
                       4: np.count_nonzero(state == 4), 5: np.count_nonzero(state == 5),
                       6: np.count_nonzero(state == 6)}
        
        # Max capacity before extreme slowdown
        capacity = 500.0   

        # KINEMATIC UPDATE LOGIC
        active = np.where(state > 0)[0]
        
        # Determine global latency for UI
        total_active = len(active)
        latency = 0.0
        if total_active > 0:
            latency = np.clip((edge_counts[2] + edge_counts[6]) / 4000.0, 0.1, 1.0)
            if phase == 3: latency = min(0.99, latency * 1.5)

        for idx in active:
            s = state[idx]
            
            # Physics Engine Routing
            if s == 1: # At Node A
                if phase in [1, 4]:
                    # Bifurcated flow
                    state[idx] = 2 if np.random.rand() > 0.5 else 3
                else:
                    # Nash Cascade: Everyone calculates B is strictly better because of the highway
                    state[idx] = 2 
                continue

            # Determine start, end, and flow speed based on current edge
            if s == 2:  start, end = NODE_A, NODE_B
            elif s == 3: start, end = NODE_A, NODE_C
            elif s == 4: start, end = NODE_B, NODE_D
            elif s == 5: start, end = NODE_C, NODE_D
            elif s == 6: start, end = NODE_B, NODE_C

            edge_density = edge_counts[s]
            speed_mult = max(0.05, 1.0 - (min(edge_density, capacity*2) / (capacity*2.5)))
            
            if phase == 3 and s in [2,6]: speed_mult *= 0.1 # Absolute Deadlock Simulation

            # Hardware Interrupt: Instantly shatter highway flow
            if phase == 4 and s == 6:
                state[idx] = 4 # Force them onto the high-friction path B->D
                continue

            delta = base_speed * speed_mult * dt
            progress[idx] += delta
            
            # Reached Node
            if progress[idx] >= 1.0:
                progress[idx] = 0.0
                if s == 2: # At Node B
                    if phase in [2, 3]: state[idx] = 6 # Exploit the Highway!
                    else: state[idx] = 4
                elif s == 3: state[idx] = 5 # At Node C, go to D
                elif s == 6: state[idx] = 5 # At Node C (via highway), go to D
                elif s in [4, 5]: # At Node D (Sink)
                    state[idx] = 0
                    throughput += 1
                continue

            # Map mathematical progress back into Cartesian space
            vec = end - start
            perp = get_perpendicular(vec)
            
            base_pos = start + (vec * progress[idx])
            px[idx] = base_pos[0] + (perp[0] * offsets[idx] * (1.0 + (1.0 - speed_mult)*2))
            py[idx] = base_pos[1] + (perp[1] * offsets[idx] * (1.0 + (1.0 - speed_mult)*2))

        # Chromatic Mapping
        active_cnt = len(active)
        c_tensor = np.zeros((active_cnt, 3))
        
        # Color dynamically shifts based on latency and phase
        base_color = np.array([0, 1, 1]) # Cyan
        if phase in [2,3]:
            mix = min(1.0, latency * 1.2)
            base_color = (1.0 - mix) * np.array([0, 1, 1]) + (mix) * np.array([1, 0, 0.3]) # Shifts to Magenta
        if is_tathata:
            base_color = np.array([0, 1, 0]) # Mantis Green

        c_tensor[:, :] = base_color
        
        # Sparkles for fastest objects
        fast_idx = np.where((progress[active] % 0.1) < 0.02)[0]
        c_tensor[fast_idx] = np.array([1, 1, 1])

        yield (f, t_sec, np.copy(px[active]), np.copy(py[active]), c_tensor, throughput, latency, phase, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 205: THE BRAESS TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Nash Equilibrium Pathing & Fluid Congestion")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
