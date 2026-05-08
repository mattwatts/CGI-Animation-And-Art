"""
SOVEREIGN CODE: logic_garden_209_kinematic_spallation.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(N) QUBO Swarm Mesh (17.5 seconds)
SCENE: Logic Garden 209 (The Kinematic Spallation / Biomass Phase Transition)
HOTFIX: O(1) APV Kinetic Compression (Phase 1 Truncated to 1.5s)
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
OUT_DIR = "frames_209_spallation"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'        # Erasure / Bare Earth
C_TEXT      = '#FFFFFF'        # Hardware Interrupt
C_DIM       = '#003322'        # Low-Level Regrowth
C_CYAN      = '#00FFFF'        # Mature Phase Coherence (The Goal)
C_MAGENTA   = '#FF0055'        # The Strike / Localized Harvesting
C_MANTIS    = '#00FF00'        # Terminal Truth / Topological Continuity

# -------- MATRIX TOPOLOGY --------
GRID_W = 120
GRID_H = 160
MAX_PARTICLES = GRID_W * GRID_H
NUM_PATCHES = 150

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_void = np.array(hex_to_rgba(C_VOID)[:3])
c_cyan = np.array(hex_to_rgba(C_CYAN)[:3])
c_mage = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_dim  = np.array(hex_to_rgba(C_DIM)[:3])
c_mantis = np.array(hex_to_rgba(C_MANTIS)[:3])

# ------------------------------------------------------------------
# PRE-COMPUTED VORONOI SWARM MESH
# ------------------------------------------------------------------
np.random.seed(42) # Deterministic architecture
gx = np.linspace(-130, 130, GRID_W)
gy = np.linspace(-210, 210, GRID_H)
X, Y = np.meshgrid(gx, gy)
px = X.flatten()
py = Y.flatten()

# Generate mathematical centers for the harvest patches
patch_cx = np.random.uniform(-130, 130, NUM_PATCHES)
patch_cy = np.random.uniform(-210, 210, NUM_PATCHES)

# O(1) Broadcast: Map every single pixel to its nearest patch center
dist_matrix = (px[:, None] - patch_cx[None, :])**2 + (py[:, None] - patch_cy[None, :])**2
point_patch_idx = np.argmin(dist_matrix, axis=1)

# Generate algorithmic phase offsets for the QUBO solver.
patch_phi = ((patch_cx * 1.3) + (patch_cy * 0.7)) % 100 / 100.0

# Pre-calculate Voronoi adjacencies for the Tathata wireframe 
points_2d = np.column_stack((patch_cx, patch_cy))
delaunay = Delaunay(points_2d)
edges = set()
for simplex in delaunay.simplices:
    for i in range(3):
        edges.add((simplex[i], simplex[(i+1)%3]))
edges = list(edges)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, colors, sizes, active_patches, mature_patches, overall_biomass, coherence_val, is_flash, is_tathata = packet
    
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
        # THE O(N) FORESTRY CANOPY TENSOR
        ax.scatter(px, py, s=sizes, c=colors, edgecolors='none', alpha=0.9, zorder=10)

        # C_MAGENTA HARVEST FLASHES (Localized friction points)
        if len(active_patches) > 0 and not is_tathata:
            ax.scatter(patch_cx[active_patches], patch_cy[active_patches], s=120, facecolor=C_MAGENTA, edgecolor=C_TEXT, lw=1.5, zorder=15)

        # TATHĀTĀ: OVERLAY THE UNBROKEN MESH
        if is_tathata:
            valid_set = set(mature_patches)
            for (p1, p2) in edges:
                if p1 in valid_set and p2 in valid_set:
                    ax.plot([patch_cx[p1], patch_cx[p2]], [patch_cy[p1], patch_cy[p2]], color=C_MANTIS, lw=2.5, alpha=0.9, zorder=20)
            
            # Highlight network nodes
            ax.scatter(patch_cx[mature_patches], patch_cy[mature_patches], s=40, facecolor=C_MANTIS, edgecolor=C_VOID, lw=1, zorder=21)
            ax.add_patch(plt.Rectangle((-140, -220), 280, 440, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -240, "NETWORK PRESERVED. ENTROPY CONTROLLED.", color=C_MANTIS, fontsize=14, fontname='monospace', weight='bold', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    ui_col = C_CYAN
    if len(active_patches) > 10 and not is_tathata: ui_col = C_MAGENTA
    if is_tathata: ui_col = C_MANTIS
    txt_col = C_TEXT if not is_flash else C_VOID

    # Header Matrix
    ax.text(-140, 240, "LG-209 :: THE KINEMATIC SPALLATION", color=ui_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: DISTRIBUTED LETHALITY & SWARM REGROWTH", color=txt_col, fontsize=12, fontname='monospace', zorder=80)
    
    # Biomass Load
    ax.text(-140, -250, f"BIOMASS YIELD    : {overall_biomass*100:05.1f}%", color=C_CYAN if overall_biomass > 0.5 else C_TEXT, fontsize=14, fontname='monospace', zorder=80)
    
    # Phase Coherence Tracker
    col_coh = C_MANTIS if coherence_val > 0.8 else C_MAGENTA
    ax.text(-140, -265, f"PHASE COHERENCE  : {coherence_val*100:05.1f}% [QUBO LOCK]", color=col_coh, fontsize=14, fontname='monospace', zorder=80)

    # Phase Text Frame
    ax.text(140, 230, f"[{state_str}]", color=ui_col if (f%15<10 or is_tathata) else C_VOID, fontsize=14, fontname='monospace', weight='bold', ha='right', zorder=80)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) ARRAY OPERATIONS & MATHEMATICAL ROUTING
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        is_flash = False
        is_tathata = False
        state = "THE THERMODYNAMIC TRAP"
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 8.0
        
        active_patches = []
        mature_patches = []
        
        # APV TIMING HOTFIX: Swarm execution begins exactly 3.5s in
        time_speed = 0.4
        raw_patch_age = (patch_phi + (t_sec - 3.5) * time_speed) % 1.0
        
        # -------------------------------------------------------------
        # PHASE LOGIC & INTERPOLATION
        # -------------------------------------------------------------
        if t_sec < 1.5:
            # PHASE 1: The Monolithic Reserve (Truncated to 1.5s for APV preservation)
            dist_from_center = np.sqrt(px**2 + py**2)
            mask_monolith = dist_from_center < 90
            
            colors[mask_monolith] = c_cyan
            colors[~mask_monolith] = c_void
            
            overall_biomass = np.sum(mask_monolith) / MAX_PARTICLES
            coherence_val = 0.2 

        elif t_sec < 3.5:
            # PHASE 2: The Shattering / QUBO Initialization (1.5s to 3.5s)
            state = "QUBO DEPLOYED :: SHATTERING THE MATRIX"
            prog = (t_sec - 1.5) / 2.0
            
            dist_from_center = np.sqrt(px**2 + py**2)
            
            node_phi = patch_phi[point_patch_idx]
            monolith_val = (dist_from_center < 90).astype(float)
            
            interp_age = node_phi * prog + (1.0 - prog) * monolith_val
            
            colors[interp_age < 0.2] = c_void
            colors[(interp_age >= 0.2) & (interp_age < 0.6)] = c_dim
            colors[interp_age >= 0.6] = c_cyan
            
            overall_biomass = np.mean(interp_age)
            coherence_val = 0.2 + (prog * 0.75) 

        elif t_sec < 14.8:
            # PHASE 3: DISTRIBUTED LETHALITY & FLUID WAVE (Extended Entrainment)
            state = "SPATIO-TEMPORAL WAVE :: KINEMATIC CYCLE"
            
            patch_ages = raw_patch_age
            
            for p_idx in range(NUM_PATCHES):
                age = patch_ages[p_idx]
                if age < 0.05: 
                    active_patches.append(p_idx) 
                elif age > 0.6:
                    mature_patches.append(p_idx) 
            
            node_ages = patch_ages[point_patch_idx]
            
            mask_harvest = node_ages < 0.05
            mask_void    = (node_ages >= 0.05) & (node_ages < 0.2)
            mask_grow    = (node_ages >= 0.2) & (node_ages < 0.6)
            mask_mature  = node_ages >= 0.6
            
            colors[mask_harvest] = c_mage
            sizes[mask_harvest] = 12.0
            colors[mask_void]    = c_void
            
            prog_grow = ((node_ages[mask_grow] - 0.2) / 0.4)[:, None]
            colors[mask_grow] = (1.0 - prog_grow) * c_dim + prog_grow * c_cyan
            colors[mask_mature]  = c_cyan
            
            overall_biomass = np.mean(node_ages)
            coherence_val = len(mature_patches) / NUM_PATCHES

        else:
            # PHASE 4: TATHĀTĀ / THE INTERRUPT
            state = "TATHĀTĀ :: STRUCTURE REQUIRES FRICTION"
            is_tathata = True
            
            locked_patch_age = (patch_phi + (14.8 - 3.5) * time_speed) % 1.0
            
            for p_idx in range(NUM_PATCHES):
                age = locked_patch_age[p_idx]
                if age > 0.5: 
                    mature_patches.append(p_idx)
                    
            node_ages = locked_patch_age[point_patch_idx]
            mask_mature  = node_ages >= 0.5
            colors[~mask_mature] = [0, 0.1, 0.1] 
            colors[mask_mature] = c_cyan
            sizes[mask_mature] = 6.0
            sizes[~mask_mature] = 2.0
            
            overall_biomass = np.mean(locked_patch_age)
            coherence_val = len(mature_patches) / NUM_PATCHES

            if t_sec < 14.95:
                is_flash = True

        yield (f, t_sec, state, colors, sizes, active_patches, mature_patches, overall_biomass, coherence_val, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 209: THE KINEMATIC SPALLATION [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: O(1) APV Kinetic Compression")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Swarm Matrix Locked.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
