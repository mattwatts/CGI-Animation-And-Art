"""
SOVEREIGN CODE: logic_garden_202_commutative_tensor.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Da Vinci Bipartite Graph Tensor (17.5 seconds)
SCENE: Logic Garden 202 (The Commutative Graph / The Complete Mind)
HOTFIX: O(N) Matrix Fusion, Bipartite LineCollection, Vitruvian Bounding Box
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
from matplotlib.collections import LineCollection
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_202_commutative_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'        # Vacuum
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'        # Void Infrastructure
C_CYAN      = '#00FFFF'        # Phase A: Science (Rigid Cartesian Grid)
C_MAGENTA   = '#FF0055'        # Phase B: Art (Fluid Chaos Matrix)
C_GOLD      = '#FFD700'        # The Commutative Bridge (Golden Ratio)
C_RED       = '#FF3300'        # Entropy Overload
C_MANTIS    = '#00FF00'        # Terminal Geometry (Tathata / Vitruvian Unity)

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_void = np.array(hex_to_rgba(C_VOID)[:3])
c_cyan = np.array(hex_to_rgba(C_CYAN)[:3])
c_mage = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_gold = np.array(hex_to_rgba(C_GOLD)[:3])
c_mant = np.array(hex_to_rgba(C_MANTIS)[:3])
c_txt  = np.array(hex_to_rgba(C_TEXT)[:3])

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE KINEMATIC ARCHITECTURE
# ------------------------------------------------------------------
NUM_SCIENCE = 400
NUM_ART = 400
MAX_PARTICLES = NUM_SCIENCE + NUM_ART
CENTER_X = 0.0  
CENTER_Y = 0.0

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, px, py, p_sizes, c_tensor, edges, e_colors, e_lws, bridge_r, is_flash, is_tathata, bg_strobe = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_TEXT if is_flash else C_VOID
    if bg_strobe and not is_tathata: bg_hex = '#0F0010' 
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    cam_w = 200.0
    cam_h = cam_w * (1920.0 / 1080.0)
    
    # Absolute Viewport Tracking Lock
    ax.set_xlim(CENTER_X - cam_w/2, CENTER_X + cam_w/2)
    ax.set_ylim(CENTER_Y - cam_h/2, CENTER_Y + cam_h/2)

    # 1. THE BIPARTITE COMMUTATIVE GRAPH (Z-Buffer Wireframe)
    if not is_flash and not is_tathata and len(edges) > 0:
        lc = LineCollection(edges, colors=e_colors, linewidths=e_lws, zorder=5, alpha=0.6)
        ax.add_collection(lc)

    # 2. THE COMMUTATIVE BRIDGE (Fibonacci Expansion)
    if not is_flash and not is_tathata and bridge_r > 0.1:
        # Drawing the geometric pulse forcing the connection
        ax.add_patch(Circle((CENTER_X, CENTER_Y), bridge_r, facecolor='none', edgecolor=C_GOLD, lw=3, linestyle='-', zorder=8, alpha=0.8))
        ax.add_patch(Circle((CENTER_X, CENTER_Y), bridge_r * 0.618, facecolor='none', edgecolor=C_GOLD, lw=1.5, linestyle='--', zorder=8, alpha=0.5))

    # 3. O(N) KINEMATIC TENSOR (Science vs Art Nodes)
    if len(px) > 0 and not is_tathata:
        ax.scatter(px, py, s=p_sizes*5.0, c=c_tensor, edgecolors='none', alpha=0.3, zorder=10)
        ax.scatter(px, py, s=p_sizes*1.5, c=C_TEXT if is_flash else c_tensor, edgecolors='none', alpha=0.9, zorder=11)

    # 4. TATHĀTĀ / THE VITRUVIAN UNIFICATION
    if is_tathata and not is_flash:
        # Vitruvian Math (Squaring the Circle)
        v_r = 80.0
        # The Circle
        ax.add_patch(Circle((CENTER_X, CENTER_Y), v_r, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=20))
        # The Square (Bottom aligned to circle base per Da Vinci proportion)
        sq_off = v_r * 0.15 
        sq_size = v_r * 1.7
        ax.add_patch(Rectangle((CENTER_X - sq_size/2, CENTER_Y - v_r + sq_off), sq_size, sq_size, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=20))
        
        # Center Singularity (The Complete Mind)
        ax.scatter([CENTER_X], [CENTER_Y], s=150, color=C_VOID, edgecolor=C_MANTIS, lw=2, zorder=25)
        
        # Inner harmonic lines
        ax.plot([CENTER_X - v_r, CENTER_X + v_r], [CENTER_Y, CENTER_Y], color=C_MANTIS, alpha=0.4, lw=1, zorder=15)
        ax.plot([CENTER_X, CENTER_X], [CENTER_Y - v_r, CENTER_Y + v_r], color=C_MANTIS, alpha=0.4, lw=1, zorder=15)

    if is_flash:
        ax.add_patch(Rectangle((CENTER_X - cam_w, CENTER_Y - cam_h), cam_w*2, cam_h*2, facecolor=C_TEXT, zorder=60))

    # 5. TELEMETRY WIDGETS (NEURAL ENTRAINMENT UI)
    ui_col = C_CYAN if not is_tathata else C_MANTIS
    if bridge_r > 50.0: ui_col = C_GOLD 
    if bridge_r > 150.0: ui_col = C_MAGENTA
    txt_col = C_TEXT if not is_flash else C_VOID
    ui_bg   = C_VOID if not is_flash else C_TEXT
    
    # Top Bar
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=ui_bg, alpha=0.9, zorder=80))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    ax.text(0.04, 0.965, "LG-202 :: THE COMMUTATIVE GRAPH TENSOR", transform=ax.transAxes, color=txt_col, fontsize=20, fontname='monospace', weight='bold', va='center', zorder=81)

    # Bottom Target Matrix
    ax.add_patch(plt.Rectangle((0, 0), 1.0, 0.16, transform=ax.transAxes, color=ui_bg, alpha=0.95, zorder=80))
    ax.plot([0, 1.0], [0.16, 0.16], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    
    # Integration Metric
    ax.text(0.04, 0.11, "SYSTEM INTEGRATION PHASE :", color=txt_col, fontsize=14, fontname='monospace', zorder=81)
    int_ratio = np.clip(bridge_r / 200.0, 0.0, 1.0)
    bar_i = C_GOLD if int_ratio > 0.01 else C_CYAN
    if is_tathata: bar_i = C_MANTIS; int_ratio = 1.0
    ax.add_patch(plt.Rectangle((0.45, 0.105), 0.50, 0.02, transform=ax.transAxes, color=C_DIM, zorder=80))
    ax.add_patch(plt.Rectangle((0.45, 0.105), 0.50 * int_ratio, 0.02, transform=ax.transAxes, color=bar_i, zorder=81))
    
    # Boolean Mute State
    msg = "FALSE" if int_ratio < 0.9 else "TRUE [GRAPH UNIFIED]"
    if is_tathata: msg = "ABSOLUTE RESOLUTION ACHIEVED"
    ax.text(0.04, 0.08, f"EVERYTHING CONNECTS      : {msg}", color=txt_col, fontsize=14, fontname='monospace', zorder=81)

    pulse = ui_col if (f % 10 < 5) and not is_flash else txt_col
    if is_flash: pulse = C_VOID

    ax.text(0.04, 0.03, f"[{state_str}]", transform=ax.transAxes, color=pulse, fontsize=20, fontname='monospace', weight='bold', zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)

# ------------------------------------------------------------------
# O(1) BALLISTIC KINEMATICS STREAM
# ------------------------------------------------------------------
def generate_stream():
    # 1. Initialize Matrices
    px = np.zeros(MAX_PARTICLES)
    py = np.zeros(MAX_PARTICLES)
    
    # SCIENCE (Lower half, Cartesian Grid)
    grid_dim = int(np.sqrt(NUM_SCIENCE))
    lin_x = np.linspace(-80, 80, grid_dim)
    lin_y = np.linspace(-140, -20, grid_dim)
    gx, gy = np.meshgrid(lin_x, lin_y)
    px[:NUM_SCIENCE] = gx.flatten()[:NUM_SCIENCE]
    py[:NUM_SCIENCE] = gy.flatten()[:NUM_SCIENCE]
    
    # ART (Upper half, Fluid Noise)
    np.random.seed(42)
    angles = np.random.uniform(0, 2*np.pi, NUM_ART)
    radii = np.random.uniform(0, 80, NUM_ART)
    px[NUM_SCIENCE:] = np.cos(angles) * radii
    py[NUM_SCIENCE:] = np.sin(angles) * radii + 80
    
    vx = np.zeros(MAX_PARTICLES)
    vy = np.zeros(MAX_PARTICLES)
    
    c_tensor = np.zeros((MAX_PARTICLES, 3))
    c_tensor[:NUM_SCIENCE] = c_cyan
    c_tensor[NUM_SCIENCE:] = c_mage
    p_sizes = np.ones(MAX_PARTICLES) * 4.0

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        dt = 0.016
        
        is_flash = False
        is_tathata = False
        bg_strobe = False
        
        bridge_r = 0.0
        edge_density = 0
        
        # ---- PHASE 1: ORTHOGONAL SOVEREIGNTY (0 - 4s) ----
        if t_sec < 4.0:
            state = "AXIOM 1&2 :: ISOLATED MATRICES (SCIENCE // ART)"
            # Science is completely rigid
            # Art slowly oscillates in Brownian loops
            vx[NUM_SCIENCE:] = np.sin(py[NUM_SCIENCE:] * 0.1 + t_sec) * 10.0
            vy[NUM_SCIENCE:] = np.cos(px[NUM_SCIENCE:] * 0.1 + t_sec) * 10.0

        # ---- PHASE 2: THE COMMUTATIVE BRIDGE (4 - 10s) ----
        elif t_sec < 10.0:
            state = "AXIOM 3 :: GEOMETRIC COMPILER INJECTED"
            prog = (t_sec - 4.0) / 6.0
            bridge_r = smoothstep(prog) * 150.0
            
            # The bridge pulls the grid and the fluid into orbital resonance
            dx = CENTER_X - px
            dy = CENTER_Y - py
            dist = np.sqrt(dx**2 + dy**2) + 0.001
            
            # Gravity pull toward center
            pull = np.where(dist < bridge_r, 1.0, 0.0)
            vx += (dx/dist) * pull * 5.0
            vy += (dy/dist) * pull * 5.0
            
            # Introduce rotation
            vx += (-dy/dist) * pull * 10.0
            vy += (dx/dist) * pull * 10.0
            
            edge_density = int(prog * 100) # Start forming lines

        # ---- PHASE 3: O(N^2) GRAPH INTEGRATION (10 - 14.8s) ----
        elif t_sec < 14.8:
            state = "WARNING :: TOPOLOGICAL UNIFICATION. O(N^2) OVERLOAD."
            prog = (t_sec - 10.0) / 4.8
            bridge_r = 150.0 + (prog * 200.0)
            
            # Violent mixing and extreme gravity
            dx = CENTER_X - px
            dy = CENTER_Y - py
            dist = np.sqrt(dx**2 + dy**2) + 0.001
            
            vx = (-dy/dist) * 150.0 * (1.0 + prog) - (dx/dist) * 50.0
            vy = (dx/dist) * 150.0 * (1.0 + prog) - (dy/dist) * 50.0
            
            edge_density = int(100 + prog * 400) # Massive spike in connections
            
            if t_sec > 13.5: bg_strobe = True
            
            # Colors dynamically shift to Gold as they unify
            gold_blend = smoothstep(prog)
            mix_c = (1-gold_blend) * c_tensor + gold_blend * c_gold
            c_tensor = np.clip(mix_c, 0, 1)

        # ---- PHASE 4: TATHĀTĀ / VITRUVIAN UNIFICATION (14.8 - 17.5s) ----
        else:
            is_tathata = True
            bridge_r = 0.0
            edge_density = 0
            
            if t_sec < 14.95:
                is_flash = True
                
            state = "TATHĀTĀ: EVERYTHING CONNECTS. THE MIND IS COMPLETE."

        # Kinematic Execution
        if not is_tathata:
            px += vx * dt
            py += vy * dt
            
            # Dampening
            vx *= 0.95
            vy *= 0.95

        # -------------------------------------------------------------
        # BIPARTITE EDGE ASSEMBLY (The Connection Graph)
        # -------------------------------------------------------------
        edges = []
        e_colors = []
        e_lws = []
        
        if edge_density > 0 and not is_tathata:
            # Randomly select N indices from Science and M from Art
            sci_idx = np.random.choice(NUM_SCIENCE, edge_density, replace=True)
            art_idx = np.random.choice(NUM_ART, edge_density, replace=True)
            art_idx += NUM_SCIENCE # Offset for art array bounds
            
            for i in range(edge_density):
                idx1 = sci_idx[i]
                idx2 = art_idx[i]
                
                pt1 = [px[idx1], py[idx1]]
                pt2 = [px[idx2], py[idx2]]
                edges.append([pt1, pt2])
                
                # Line color scales from Cyan to Magenta via Gold
                e_colors.append(hex_to_rgba(C_GOLD, 0.4))
                e_lws.append(0.5 + np.random.uniform(0, 1.5))

        yield (f, t_sec, state, np.copy(px), np.copy(py), p_sizes, np.copy(c_tensor), edges, e_colors, e_lws, bridge_r, is_flash, is_tathata, bg_strobe)

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 202: THE COMMUTATIVE TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Bipartite Graph Matrices & Vitruvian Unification")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Nodes: {MAX_PARTICLES}")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
