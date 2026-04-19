"""
SOVEREIGN CODE: logic_garden_189_gravitational_entrainment.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Spacetime Metric Tensor (17.5 seconds)
SCENE: Logic Garden 189 (The Cosmic Chirp / LIGO Binary Merger)
HOTFIX: Retarded Time (t - r/c) Vectorization, Quadrupole Photic Strobe
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Rectangle
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_189_ligo"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#000000'        # The Vacuum Vector
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'
C_CYAN      = '#00FFFF'        # Negative Spacetime Strain
C_MAGENTA   = '#FF00FF'        # Positive Spacetime Strain
C_RED       = '#FF0033'        # The Plunge / Frequency Overload
C_MANTIS    = '#00FF00'        # Ringdown Coherence / Tathata
EVENT_H     = '#04040A'        # Event Horizon Absolute Black

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE SPACETIME METRIC (O(N) LATTICE)
# ------------------------------------------------------------------
N_POINTS = 30000
CX, CY = 540, 960

# We distribute the 30,000 points logarithmically out from the center
np.random.seed(189)
grid_r = np.random.uniform(0, 1.0, N_POINTS) ** 0.5 * 1200.0  # Dense center, spreading out
grid_theta = np.random.uniform(0, 2*np.pi, N_POINTS)

base_x = CX + grid_r * np.cos(grid_theta)
base_y = CY + grid_r * np.sin(grid_theta)

# Relativity Constants
C_SPEED = 400.0        # Sim speed of gravitational waves
T_MERGE = 14.8         # The Hardware Interrupt

# Pre-calculate Universal Chirp Data to ensure perfect UI alignment
t_arr = np.linspace(0, DURATION, TOTAL_FRAMES)
strain_arr = np.zeros(TOTAL_FRAMES)
for i, t in enumerate(t_arr):
    if t < T_MERGE:
        tau = max(0.001, T_MERGE - t)
        amp = 1.0 / (tau**0.25)
        freq = 30.0 / (tau**0.375)
        strain_arr[i] = amp * np.cos(freq * t)
    else:
        t_ring = t - T_MERGE
        amp = (1.0 / (0.001**0.25)) * np.exp(-t_ring * 6.0)
        strain_arr[i] = amp * np.cos(150.0 * t_ring)
        
strain_norm = strain_arr / np.max(np.abs(strain_arr))

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, px, py, p_sizes, p_cols, bh1, bh2, is_flash, is_tathata, current_strain = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg = C_TEXT if is_flash else C_VOID
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    # 1. RENDER O(N) SPACETIME FABRIC (LENSING GRID)
    # Background Grid Lines (Euclidean Reference)
    if not is_flash:
        for offset in range(-1200, 1200, 200):
            ax.axvline(CX + offset, color=C_DIM, lw=1, zorder=1)
            ax.axhline(CY + offset, color=C_DIM, lw=1, zorder=1)
            
    # Scatter Spacetime Metric Points
    if len(px) > 0 and not is_flash:
        ax.scatter(px, py, s=p_sizes, c=p_cols, edgecolors='none', alpha=0.8, zorder=5)

    # 2. RENDER THE SINGULARITIES (EVENT HORIZONS)
    if not is_flash:
        if not is_tathata:
            # Binary Inspiral
            x1, y1, r1 = bh1
            x2, y2, r2 = bh2
            # Singularity 1
            ax.add_patch(Circle((x1, y1), r1*1.5, color=C_CYAN, alpha=0.3, zorder=9))
            ax.add_patch(Circle((x1, y1), r1, color=C_TEXT, lw=4, fill=False, zorder=10))
            ax.add_patch(Circle((x1, y1), r1*0.9, color=EVENT_H, zorder=11))
            # Singularity 2
            ax.add_patch(Circle((x2, y2), r2*1.5, color=C_MAGENTA, alpha=0.3, zorder=9))
            ax.add_patch(Circle((x2, y2), r2, color=C_TEXT, lw=4, fill=False, zorder=10))
            ax.add_patch(Circle((x2, y2), r2*0.9, color=EVENT_H, zorder=11))
            
            # Orbital Link (The Tension)
            ax.plot([x1, x2], [y1, y2], color=C_TEXT, lw=2, alpha=0.2, linestyle='--', zorder=8)
        else:
            # Merged Singularity (Quasinormal Mode Ringdown)
            x_m, y_m, r_m, r_wobble = bh1 # Encoded wobble
            ax.add_patch(Circle((x_m, y_m), r_m * 2.0, color=C_MANTIS, alpha=0.2, zorder=9))
            ax.add_patch(Ellipse((x_m, y_m), r_m*2 + r_wobble, r_m*2 - r_wobble, angle=45, color=C_TEXT, lw=4, fill=False, zorder=10))
            ax.add_patch(Circle((x_m, y_m), r_m*0.95, color=EVENT_H, zorder=11))

    # Hardware Flash Geometry
    if is_flash:
        ax.scatter([CX], [CY], s=200000, facecolors='none', edgecolors=C_MANTIS, lw=80, zorder=30)
        ax.scatter([CX], [CY], s=50000, c=C_TEXT, zorder=31)

    # 3. TELEMETRY WIDGETS (THE CHIRP SIGNAL)
    ui_col = C_CYAN if not is_tathata else C_MANTIS
    if t_sec > 13.0 and not is_tathata: ui_col = C_RED # Plunge warning
    if is_flash: ui_col = C_VOID
    txt_col = C_TEXT if not is_flash else C_VOID
    bg_col  = C_VOID if not is_flash else C_TEXT
    
    # Top Bar
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=bg_col, alpha=0.9, zorder=80))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    ax.text(0.04, 0.965, "LG-189 :: GRAVITATIONAL WAVE INTERFEROMETRY", transform=ax.transAxes, color=txt_col, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=81)

    # Bottom UI Matrix (The Strain Graph)
    ax.add_patch(plt.Rectangle((0, 0), 1.0, 0.18, transform=ax.transAxes, color=bg_col, alpha=0.95, zorder=80))
    ax.plot([0, 1.0], [0.18, 0.18], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    ax.text(0.04, 0.14, "QUADRUPOLE STRAIN AMPLITUDE $h(t)$:", transform=ax.transAxes, color=txt_col, fontsize=18, fontname='monospace', zorder=81)
    
    # Graphing the Chirp
    # Plot the last 4 seconds of data (to make it move like an oscilloscope)
    lookback_frames = int(4.0 * FPS)
    start_f = max(0, f - lookback_frames)
    end_f = f
    
    if end_f > start_f:
        hist_x = np.linspace(0.04, 0.96, end_f - start_f)
        hist_y = 0.08 + (strain_norm[start_f:end_f] * 0.04) # Map -1 to 1 into 0.04 to 0.12
        
        # O(1) Plot array
        ax.plot(hist_x, hist_y, transform=ax.transAxes, color=ui_col, lw=3, zorder=82)
        # Lead point dot
        ax.scatter([hist_x[-1]], [hist_y[-1]], transform=ax.transAxes, s=150, c=C_TEXT if not is_flash else C_VOID, zorder=83)

    pulse = ui_col if (f % 10 < 5) and not is_flash else txt_col
    if is_flash: pulse = C_VOID

    ax.text(0.04, 0.03, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=22, fontname='monospace', weight='bold', zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) RELATIVISTIC KINEMATICS STREAM
# ------------------------------------------------------------------
def generate_stream():
    
    c_cy_rgb = np.array(hex_to_rgba(C_CYAN)[:3])
    c_mg_rgb = np.array(hex_to_rgba(C_MAGENTA)[:3])
    c_mn_rgb = np.array(hex_to_rgba(C_MANTIS)[:3])
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        is_flash = False
        is_tathata = False
        current_strain = strain_norm[f]
        
        # Black Hole Kinematics
        bh1 = (0, 0, 0)
        bh2 = (0, 0, 0)

        # ---- PHASE 1: INSPIRAL (0 - 12s) ----
        if t_sec < 12.0:
            state = "[01] BINARY INSPIRAL :: GRAVITATIONAL RADIATION DETECTED"
            tau = T_MERGE - t_sec
            sep = 40.0 * (tau**0.4)
            omega = 3.0 / (tau**0.375)
            orbit_angle = omega * t_sec
            
            bh1 = (CX + sep*np.cos(orbit_angle), CY + sep*np.sin(orbit_angle), 35.0)
            bh2 = (CX - sep*np.cos(orbit_angle), CY - sep*np.sin(orbit_angle), 35.0)

        # ---- PHASE 2: THE PLUNGE (12 - 14.8s) ----
        elif t_sec < T_MERGE:
            state = "WARNING: THE PLUNGE. EVENT HORIZON VELOCITY AT OPTICAL LIMIT."
            tau = max(0.001, T_MERGE - t_sec)
            sep = 40.0 * (tau**0.4)
            omega = 3.0 / (tau**0.375)
            orbit_angle = omega * t_sec
            
            bh1 = (CX + sep*np.cos(orbit_angle), CY + sep*np.sin(orbit_angle), 35.0 + (14.8-t_sec)*2.0)
            bh2 = (CX - sep*np.cos(orbit_angle), CY - sep*np.sin(orbit_angle), 35.0 + (14.8-t_sec)*2.0)

        # ---- PHASE 3: TATHĀTĀ / HARDWARE INTERRUPT (14.8 - 17.5s) ----
        else:
            is_tathata = True
            t_ring = t_sec - T_MERGE
            if t_sec < 14.95:
                is_flash = True
            state = "TATHĀTĀ: SINGULARITY MERGE. TOPOLOGICAL RINGDOWN ACHIEVED."
            
            # Quasinormal mode wobble decays exponentially
            r_wobble = 50.0 * np.exp(-t_ring * 6.0) * np.cos(150.0 * t_ring)
            bh1 = (CX, CY, 55.0, r_wobble)

        # -----------------------------------------------
        # O(N) RETARDED TIME SPACETIME SOLVER 
        # -----------------------------------------------
        # Spacetime distortion is emitted from the center and travels at C_SPEED
        # The strain h at distance r at time t is determined by the source state at t_ret
        t_ret = t_sec - (grid_r / C_SPEED)
        
        # Mask valid retarded times
        valid_mask = t_ret > 0
        h_grid = np.zeros(N_POINTS)
        
        # We compute the exact analytical chirp function for the entire field instantly
        tau_grid = np.maximum(0.001, T_MERGE - t_ret[valid_mask])
        
        # Piecewise tensor calculation for Inspiral vs Ringdown propagating outward
        inspi_mask = t_ret[valid_mask] < T_MERGE
        ringd_mask = ~inspi_mask
        
        # Inspiral spatial calculation
        h_grid[valid_mask & (t_ret < T_MERGE)] = (1.0 / tau_grid[inspi_mask]**0.25) * np.cos((30.0 / tau_grid[inspi_mask]**0.375) * t_ret[valid_mask][inspi_mask] - 2*grid_theta[valid_mask & (t_ret < T_MERGE)])
        
        # Ringdown spatial calculation
        t_r = t_ret[valid_mask][ringd_mask] - T_MERGE
        h_grid[valid_mask & (t_ret >= T_MERGE)] = (1.0 / 0.001**0.25) * np.exp(-t_r * 6.0) * np.cos(150.0 * t_r)
        
        # Attenuate by 1/r
        h_grid = h_grid * (500.0 / (grid_r + 100.0))
        
        # Map h_grid into positional quadrupole distortion
        # Distort the base Euclidean coordinates
        px = base_x + h_grid * np.cos(grid_theta) * 20.0
        py = base_y + h_grid * np.sin(grid_theta) * 20.0
        
        # Dynamic particle sizing for visual pop
        p_sizes = 3.0 + np.abs(h_grid) * 15.0

        # -----------------------------------------------
        # O(N) COLOR CHROMATICS MATRIX 
        # -----------------------------------------------
        c_tensor = np.zeros((N_POINTS, 3)) 
        
        # Default to dim space
        c_base = np.array(hex_to_rgba(C_DIM)[:3])
        c_tensor[:] = c_base
        
        # Positive strain -> Cyan, Negative strain -> Magenta
        pos_mask = h_grid > 0.1
        neg_mask = h_grid < -0.1
        
        # Blend based on amplitude
        blend_pos = np.clip(h_grid[pos_mask] / 3.0, 0, 1)[:, None]
        c_tensor[pos_mask] = (1 - blend_pos) * c_base + blend_pos * c_cy_rgb
        
        blend_neg = np.clip(np.abs(h_grid[neg_mask]) / 3.0, 0, 1)[:, None]
        c_tensor[neg_mask] = (1 - blend_neg) * c_base + blend_neg * c_mg_rgb
        
        # Post-merger tracking (Tathata cleanup wave)
        # A massive ring of Mantis energy radiating outward
        if is_tathata:
            pulse_r = (t_sec - T_MERGE) * C_SPEED * 1.5
            ring_mask = np.abs(grid_r - pulse_r) < 80.0
            blend_ring = np.clip(1.0 - np.abs(grid_r[ring_mask] - pulse_r)/80.0, 0, 1)[:, None]
            c_tensor[ring_mask] = (1 - blend_ring) * c_tensor[ring_mask] + blend_ring * c_mn_rgb

        yield (f, t_sec, state, px, py, p_sizes, c_tensor, bh1, bh2, is_flash, is_tathata, current_strain)

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 189: THE GRAVITATIONAL TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: O(N) Retarded-Time Spacetime Metric Vectorization")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Nodes: {N_POINTS}")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
