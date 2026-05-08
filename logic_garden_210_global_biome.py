"""
SOVEREIGN CODE: logic_garden_210_global_biome.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Quantum Annealing Graph (17.5 seconds)
SCENE: Logic Garden 210 (The Global Biome Tensor / Macro Orchestration)
HOTFIX: O(N) Array Synchronization & Exact Global Biomass Validation
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_210_global_biome"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'        # Void / Regional Extinction
C_TEXT      = '#FFFFFF'        # Hardware Interrupt
C_DIM       = '#112233'        # The Base Graph Matrix
C_CYAN      = '#00FFFF'        # Stable Carbon Sink (Biomass)
C_MAGENTA   = '#FF0055'        # Thermal Friction / Localized Micro-Harvest
C_GOLD      = '#FFD700'        # QUBO Tensor Alignment Overrides
C_MANTIS    = '#00FF00'        # Terminal Truth / Synchronized Breath

MAX_PARTICLES = 25000

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_void = np.array(hex_to_rgba(C_VOID)[:3])
c_dim  = np.array(hex_to_rgba(C_DIM)[:3])
c_cyan = np.array(hex_to_rgba(C_CYAN)[:3])
c_mage = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_gold = np.array(hex_to_rgba(C_GOLD)[:3])
c_mantis = np.array(hex_to_rgba(C_MANTIS)[:3])

# ------------------------------------------------------------------
# CONTINENTAL MATRIX GENERATION (O(N) TOPOLOGY)
# ------------------------------------------------------------------
np.random.seed(101) # Sovereign architectural seed

# We forge an exact 25,000 node ellipse to map the "Continental Atlas"
px_raw, py_raw = [], []
while len(px_raw) < MAX_PARTICLES:
    tx, ty = np.random.uniform(-140, 140), np.random.uniform(-200, 200)
    # Elliptical distance filtering for geometric containment
    if np.sqrt((tx/1.2)**2 + (ty/1.8)**2) < 100:
        px_raw.append(tx)
        py_raw.append(ty)
        
px = np.array(px_raw[:MAX_PARTICLES])
py = np.array(py_raw[:MAX_PARTICLES])

# To model Semantic Hallucination, we assign regions (0 to 4)
regions = np.zeros(MAX_PARTICLES, dtype=int)
regions[(px < 0) & (py > 0)] = 1
regions[(px > 0) & (py > 0)] = 2
regions[(px < 0) & (py < 0)] = 3
regions[(px > 0) & (py < 0)] = 4

# Precompute mathematical phase for the "Global Breath"
# Spatial wavelength driving synchronous O(N) sine functions
spatial_phase = np.sqrt((px - 50)**2 + (py + 50)**2) * 0.15 

# Sub-sample array for QUBO gold Tensor connections
tensor_nodes = np.random.choice(MAX_PARTICLES, size=80, replace=False)
tensor_edges = []
for i in range(len(tensor_nodes)):
    for j in range(i+1, len(tensor_nodes)):
        if np.random.rand() > 0.92:
            tensor_edges.append((tensor_nodes[i], tensor_nodes[j]))

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, colors, sizes, gb_yield, nash_err, is_qubo, is_flash, is_tathata = packet
    
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
        # THE O(N) CONTINENTAL BIOME TENSOR
        ax.scatter(px, py, s=sizes, c=colors, edgecolors='none', alpha=0.9, zorder=10)

        # THE QUBO TENSOR ALIGNMENT
        if is_qubo:
            alpha_pulse = 0.5 + 0.5 * np.sin(t_sec * 8.0) if not is_tathata else 0.8
            edge_c = C_GOLD if not is_tathata else C_MANTIS
            for (n1, n2) in tensor_edges:
                ax.plot([px[n1], px[n2]], [py[n1], py[n2]], color=edge_c, lw=1.5, alpha=alpha_pulse, zorder=15)
            
            # Key Sovereign Nodes 
            ax.scatter(px[tensor_nodes], py[tensor_nodes], s=40, facecolor=C_VOID, edgecolor=edge_c, lw=1.5, zorder=16)

        # TATHĀTĀ WIREFRAME
        if is_tathata:
            ax.add_patch(plt.Rectangle((-140, -220), 280, 440, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -240, "TERMINAL STABILITY. THE ALGORITHM BREATHES.", color=C_MANTIS, fontsize=14, fontname='monospace', weight='bold', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    ui_col = C_CYAN
    if nash_err: ui_col = C_MAGENTA
    if is_qubo and not is_tathata: ui_col = C_GOLD
    if is_tathata: ui_col = C_MANTIS
    txt_col = C_TEXT if not is_flash else C_VOID

    # Header Matrix
    ax.text(-140, 240, "LG-210 :: THE GLOBAL BIOME TENSOR", color=ui_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: MACRO ORCHESTRATION / QUBO ANNEALER", color=txt_col, fontsize=12, fontname='monospace', zorder=80)
    
    # Global Carbon Entropy Sink 
    status_nash = "CRITICAL LIMIT BROKEN" if nash_err else "OPTIMIZED & GROUNDED"
    if is_tathata: status_nash = "PERFECT SPATIO-TEMPORAL SYNCHRONIZATION"
    ax.text(-140, -250, f"GLOBAL BIOMASS   : {gb_yield*100:05.1f}% [STATISTICALLY HALTED]", color=C_CYAN if gb_yield >= 0.55 else C_MAGENTA, fontsize=14, fontname='monospace', zorder=80)
    
    # Nash Cascade Alert
    ax.text(-140, -265, f"LOCAL NASH CASCADE : {status_nash}", color=C_MAGENTA if nash_err else (C_MANTIS if is_tathata else C_CYAN), fontsize=14, fontname='monospace', weight='bold', zorder=80)

    # Phase Text Frame
    ax.text(140, 230, f"[{state_str}]", color=ui_col if (f%15<10 or is_tathata) else C_VOID, fontsize=14, fontname='monospace', weight='bold', ha='right', zorder=80)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) FLUID DISPLACEMENT STREAM
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        is_flash = False
        is_tathata = False
        is_qubo = False
        nash_err = False
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 4.0
        
        # -------------------------------------------------------------
        # PHASE LOGIC & INTERPOLATION
        # -------------------------------------------------------------
        if t_sec < 4.5:
            # PHASE 1: Semantic Hallucination (Simulated Annealing)
            state = "SIMULATED ANNEALING :: SEMANTIC HALLUCINATION"
            
            # The global sum remains healthy (approx ~60%), but Region 3 is systematically stripped to zero
            prog = np.clip(t_sec / 3.0, 0, 1)
            
            # 60% baseline random survival in regions 1, 2, 4
            np.random.seed(1)
            base_survival = np.random.rand(MAX_PARTICLES) < 0.6
            
            # Region 3 undergoes systemic mathematical wipeout
            extinction_wave = np.random.rand(MAX_PARTICLES) > (prog * 1.5)
            mask_survival = base_survival.copy()
            mask_survival[(regions == 3) & (~extinction_wave)] = False
            
            colors[~mask_survival] = c_dim 
            colors[mask_survival] = c_cyan
            # To highlight the Regional Cascade friction
            colors[(regions == 3) & (~extinction_wave)] = c_mage if (f % 10 < 5) else c_void
            
            if prog > 0.5: nash_err = True
            gb_yield = np.sum(mask_survival) / MAX_PARTICLES

        elif t_sec < 7.0:
            # PHASE 2: The Quantum Drop / QUBO Overlay
            state = "QUANTUM DROP :: O(1) TENSOR OVERRIDE"
            is_qubo = True
            nash_err = False
            
            # Fade from chaotic extinction to rigidly synchronized pre-state
            prog = np.clip((t_sec - 4.5) / 1.5, 0, 1)
            colors[:, :] = (1.0 - prog)*c_mage + (prog)*c_dim
            
            # Initialize the grid seeds
            seed_mask = (spatial_phase % (np.pi) < 0.5) 
            colors[seed_mask] = (1.0 - prog)*colors[seed_mask] + (prog)*c_cyan
            
            gb_yield = 0.60 

        elif t_sec < 14.8:
            # PHASE 3: The Symphony of Spallation / The Macro Breath
            state = "QUBO FORMULATION :: THE GLOBAL BREATH"
            is_qubo = True
            nash_err = False
            
            time_shift = (t_sec - 7.0) * 4.0
            
            # We calculate a continuous, hyper-dimensional wave that oscillates across the globe.
            # Local vectors drop to 0 (harvested), while immediate neighbors climb to 1 (canopy).
            # The mathematical aggregate remains an absolute unbroken 60%.
            breath = 0.5 + 0.5 * np.cos(spatial_phase - time_shift)
            
            # Using absolute tensor boundaries for continuous chromatic interpolation
            # C_MAGENTA indicates the active geometric strike of the harvest vector
            strike_zone = (breath < 0.1)
            regrow_zone = (breath >= 0.1) & (breath < 0.5)
            canopy_zone = (breath >= 0.5)
            
            colors[strike_zone] = c_mage
            sizes[strike_zone] = 12.0 # Friction points enlarge to overload optic nerve
            
            r_prog = ((breath[regrow_zone] - 0.1) / 0.4)[:, None]
            colors[regrow_zone] = (1.0 - r_prog) * c_dim + (r_prog) * c_cyan
            
            colors[canopy_zone] = c_cyan
            sizes[canopy_zone] = 8.0
            
            gb_yield = 0.60

        else:
            # PHASE 4: TATHĀTĀ / TERMINAL STABILITY
            state = "TATHĀTĀ :: TERMINAL STABILITY"
            is_qubo = True
            is_tathata = True
            
            # Lock the exact kinematic position of the breath
            locked_time = (14.8 - 7.0) * 4.0
            breath = 0.5 + 0.5 * np.cos(spatial_phase - locked_time)
            
            canopy_zone = (breath >= 0.5)
            colors[~canopy_zone] = [0.0, 0.2, 0.2] # Dark green dimming for contrast
            colors[canopy_zone] = c_cyan
            sizes[canopy_zone] = 6.0
            sizes[~canopy_zone] = 2.0
            
            gb_yield = 0.60
            
            if t_sec < 14.95:
                is_flash = True

        yield (f, t_sec, state, colors, sizes, gb_yield, nash_err, is_qubo, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 210: THE GLOBAL BIOME TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: O(N) Array Synchronization & Exact Global Biomass Validation")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Global Ecosystem Mathematically Secured.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
