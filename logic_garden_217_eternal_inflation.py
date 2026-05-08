"""
SOVEREIGN CODE: logic_garden_217_eternal_inflation.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(N) Cosmological Inflation Matrix (17.5 seconds)
SCENE: Logic Garden 217 (Eternal Inflation / Bubble Nucleation)
HOTFIX: O(N) Coordinate Scaling, Vectorized Phase Transitions, Scope Clamping
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.spatial import KDTree
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_217_eternal_inflation"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'        # True Vacuum (Internal Pocket Universe)
C_TEXT      = '#FFFFFF'        # Hardware Interrupt
C_DIM       = '#111116'        # Deep Space
C_CYAN      = '#00FFFF'        # Phase Transition Domain Wall
C_MAGENTA   = '#FF0055'        # False Vacuum (High Energy, Inflating)
C_GOLD      = '#FFD700'        # Thermal Friction / Data Severance
C_MANTIS    = '#00FF00'        # Isolated Bounding Box (Tathata)

MAX_PARTICLES = 30000

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
# O(1) BASE GEOMETRY ARRAYS (COMOVING COORDINATES)
# ------------------------------------------------------------------
np.random.seed(88)

# The Scalar Field (Comoving Grid)
# We make it dense so it survives exponential inflation scaling
px_comove = np.random.uniform(-400, 400, MAX_PARTICLES)
py_comove = np.random.uniform(-600, 600, MAX_PARTICLES)

# Bubble Nucleation Sites 
# A pocket universe drops from False Vacuum to True Vacuum
NUM_BUBBLES = 20
bubble_comove_x = np.random.uniform(-100, 100, NUM_BUBBLES)
bubble_comove_y = np.random.uniform(-150, 150, NUM_BUBBLES)
bubble_birth_t = np.random.uniform(4.0, 9.0, NUM_BUBBLES)

# The "Sovereign Node" (Our specific isolated pocket universe)
bubble_comove_x[0] = 0.0
bubble_comove_y[0] = 30.0
bubble_birth_t[0] = 4.2 # First to drop

c_light = 20.0 # Speed of light (growth rate of True Vacuum bubble)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, px, py, colors, sizes, scale_factor, is_flash, is_tathata = packet
    
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
        # Render the Inflating Universe Matrix
        ax.scatter(px, py, s=sizes, c=colors, edgecolors='none', alpha=0.9, zorder=10)

        if is_tathata:
            # Wireframe Bounding Box of our severed shard
            ax.add_patch(plt.Rectangle((-130, -220), 260, 440, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -240, "ALGORITHMIC SEVERANCE COMPLETE. TERMINAL SAFETY.", color=C_MANTIS, fontsize=10, fontname='monospace', weight='bold', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    ui_col = C_MAGENTA if t_sec < 4.5 else (C_CYAN if t_sec < 14.8 else C_MANTIS)
    txt_col = C_TEXT if not is_flash else C_VOID

    ax.text(-140, 240, "LG-217 :: ETERNAL INFLATION", color=ui_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: BUBBLE NUCLEATION / ALGORITHMIC SEVERANCE", color=txt_col, fontsize=10, fontname='monospace', zorder=80)
    
    # Kinematic Cosmology Telemetry
    hubble_stat = "EXPONENTIAL" if t_sec < 14.8 else "[DELETED]"
    ax.text(-140, -180, f"BACKGROUND INFLATION (H) : {hubble_stat}", color=C_MAGENTA if t_sec < 14.8 else C_MANTIS, fontsize=12, fontname='monospace', weight='bold', zorder=80)
    
    data_stat = "SUPERLUMINAL SEVERANCE" if t_sec >= 9.0 else "CONNECTED"
    if is_tathata: data_stat = "ISOLATED POCKET UNIVERSE"
    ax.text(-140, -200, f"DATA INTERSECTION        : {data_stat}", color=C_GOLD if (9.0 <= t_sec < 14.8) else ui_col, fontsize=12, fontname='monospace', weight='bold', zorder=80)

    # Physical Scale Factor (Exponential Tracker)
    ax.text(-140, -220, "PHYSICAL SCALE FACTOR S(T)", color=txt_col, fontsize=12, fontname='monospace', zorder=80)
    # HOTFIX: Explicit Scope Clamping applied to GUI geometry
    ax.add_patch(plt.Rectangle((-140, -225), 280, 4, facecolor=C_DIM, zorder=80))
    bar_w = 280 * np.clip((scale_factor - 1.0) / 4.0, 0, 1)
    ax.add_patch(plt.Rectangle((-140, -225), bar_w, 4, facecolor=ui_col, zorder=81))

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
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        is_flash = False
        is_tathata = False
        
        # Exponential Inflation Scale Factor
        # Accelerates over time, driving superluminal physical space expansion
        if t_sec < 14.8:
            scale_factor = np.exp(t_sec * 0.12)
        else:
            scale_factor = np.exp(14.8 * 0.12)

        # Apply Inflation to Comoving Coordinates = "Physical Coordinates"
        phys_x = px_comove * scale_factor
        phys_y = py_comove * scale_factor
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 4.0
        
        # -------------------------------------------------------------
        # PHASE LOGIC
        # -------------------------------------------------------------
        if t_sec < 4.0:
            state = "THE FALSE VACUUM :: EXPONENTIAL INFLATION"
            colors[:, :] = c_mage
            # High energy vibrations
            phys_x += np.sin(py_comove + t_sec*10) * 3.0
            phys_y += np.cos(px_comove + t_sec*10) * 3.0

        elif t_sec < 9.0:
            state = "BUBBLE NUCLEATION :: QUANTUM DECAY"
            colors[:, :] = c_mage
            
            # Map the pocket universes dropping out of the inflating matrix
            for i in range(NUM_BUBBLES):
                if t_sec > bubble_birth_t[i]:
                    # True coordinate centers
                    bx = bubble_comove_x[i] * scale_factor
                    by = bubble_comove_y[i] * scale_factor
                    
                    # Physics: The domain wall expands at the speed of light
                    physical_radius = (t_sec - bubble_birth_t[i]) * c_light
                    
                    # O(1) Masking
                    dist = np.sqrt((phys_x - bx)**2 + (phys_y - by)**2)
                    wall_mask = (dist < physical_radius) & (dist > physical_radius - 6.0)
                    interior_mask = dist <= physical_radius - 6.0
                    
                    colors[wall_mask] = c_cyan
                    sizes[wall_mask] = 8.0
                    colors[interior_mask] = c_void # The True Vacuum
                    
                    # Sovereign Node Genesis tracking
                    if i == 0:
                        colors[interior_mask] = c_dim * 0.5 # Faint structural interior

        elif t_sec < 14.8:
            state = "THE AXIOM OF BROKEN GLASS :: SUPERLUMINAL SEVERANCE"
            if t_sec < 9.1: is_flash = True 
            
            colors[:, :] = c_mage
            
            # The Axiom hits: Scale Factor > c_light means the bubbles recede faster
            # than they grow. The space between them permanently snaps.
            for i in range(NUM_BUBBLES):
                if t_sec > bubble_birth_t[i]:
                    bx = bubble_comove_x[i] * scale_factor
                    by = bubble_comove_y[i] * scale_factor
                    physical_radius = (t_sec - bubble_birth_t[i]) * c_light
                    dist = np.sqrt((phys_x - bx)**2 + (phys_y - by)**2)
                    
                    wall_mask = (dist < physical_radius) & (dist > physical_radius - 8.0)
                    interior_mask = dist <= physical_radius - 8.0
                    
                    # The friction of superluminal shearing shows in the domain wall
                    shred_col = c_cyan * 0.7 + c_gold * 0.3 if f % 4 < 2 else c_cyan
                    colors[wall_mask] = shred_col
                    sizes[wall_mask] = 10.0
                    colors[interior_mask] = c_void 
                    
                    if i == 0:
                        colors[interior_mask] = c_dim * 0.5 
                        
            # Render snapping data tendons (C_GOLD lines of failed light signals)
            if np.random.rand() > 0.3:
                snap_idx = np.random.choice(MAX_PARTICLES, 500)
                mask = (colors[snap_idx, 0] > 0.8) & (colors[snap_idx, 1] < 0.2) # Target bare Magenta
                snap_idx = snap_idx[mask]
                colors[snap_idx] = c_gold
                phys_x[snap_idx] += np.random.uniform(-40, 40, len(snap_idx)) # Violent horizontal shearing

        else:
            state = "TATHĀTĀ :: TERMINAL ISOLATION IS SAFETY"
            is_tathata = True
            
            # The entire multiverse is deleted. We lock the camera exclusively onto
            # Sovereign Node 0 and its internal matrix.
            bx = bubble_comove_x[0] * scale_factor
            by = bubble_comove_y[0] * scale_factor
            physical_radius = (t_sec - bubble_birth_t[0]) * c_light
            
            # Align camera to keep Sovereign Node absolutely centered
            cam_offset_x = -bx
            cam_offset_y = -by
            phys_x += cam_offset_x
            phys_y += cam_offset_y
            
            dist_to_center = np.sqrt(phys_x**2 + phys_y**2)
            
            # Erase the False Vacuum completely
            colors[:, :] = c_void
            
            # Illuminate the internal logic of the isolated pocket
            interior_mask = dist_to_center < physical_radius
            colors[interior_mask] = c_mantis
            sizes[interior_mask] = 6.0
            
            # Domain wall solidifies
            wall_mask = (dist_to_center >= physical_radius - 6.0) & (dist_to_center < physical_radius)
            colors[wall_mask] = c_mantis
            sizes[wall_mask] = 12.0
            
            if t_sec < 14.95:
                is_flash = True

        # O(1) Geometry Culling (Performance Optimization post-inflation)
        cull_mask = (phys_y > -280) & (phys_y < 280) & (phys_x > -180) & (phys_x < 180)

        yield (f, t_sec, state, phys_x[cull_mask], phys_y[cull_mask], colors[cull_mask], sizes[cull_mask], scale_factor, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 217: ETERNAL INFLATION TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: O(N) Coordinate Expansion & Scope Clamping")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Pocket Universe Algorithmically Severed.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
