"""
SOVEREIGN CODE: logic_garden_155_gold_mill.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Vector Physics Emulation
SCENE: Logic Garden 155 (MBMM Gravity Separation - Rock to Button)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing as mp
import os
import gc
import math

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 35                   
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_155_mill"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_RED     = '#FF0033'          # Entropy / Raw Rock / Tailings
C_GOLD    = '#FFD700'          # The Truth / Target Payload
C_CYAN    = '#00FFFF'          # MBMM Machinery / The Bounding Box
C_MANTIS  = '#00FF00'          # Terminal Flow / System Success
C_WATER   = '#0044FF'          # Slurry Flow
C_FIRE    = '#FF5500'          # Thermal Phase Transition

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# Compile-time lock for particle generation (Absolute Determinism)
np.random.seed(MBMM_155 := 155)
NUM_PARTICLES = 2000
p_id = np.arange(NUM_PARTICLES)
is_gold = (p_id % 12 == 0)  # ~8.3% yield (High Grade)

# Initial random offsets for organic flow
r_offset_x = np.random.uniform(-1, 1, NUM_PARTICLES)
r_offset_y = np.random.uniform(-1, 1, NUM_PARTICLES)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER (ISOLATED MEMORY NODE)
# ------------------------------------------------------------------
def render_frame(data_packet):
    f, t_sec, state_str, ui_color, p_x, p_y, p_sizes, p_alphas, mach_data = data_packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)
    
    ax.set_xlim(0, 1080)
    ax.set_ylim(0, 1920)

    # -------- MACHINERY RENDER LAYER --------
    if mach_data['type'] == 'CRUSHER':
        # Jaw Crusher Lines
        jaw_gap = mach_data['jaw_gap']
        y_top, y_bot = 1600, 600
        # Left Jaw
        ax.plot([540 - jaw_gap - 200, 540 - jaw_gap/2], [y_top, y_bot], color=C_CYAN, lw=15, solid_capstyle='round')
        # Right Jaw (Moving)
        ax.plot([540 + jaw_gap + 200, 540 + jaw_gap/2], [y_top, y_bot], color=C_CYAN, lw=20, solid_capstyle='round')
        ax.plot([540 + jaw_gap + 200, 540 + jaw_gap/2], [y_top, y_bot], color=C_TEXT, lw=4, alpha=0.5)

    elif mach_data['type'] == 'TABLE':
        # Shaker Table Riffles (Diagonal from Bottom-Left to Top-Right)
        shake = mach_data['shake']
        table_y = np.linspace(300, 1500, 15)
        for ty in table_y:
            ax.plot([100 + shake, 980 + shake], [ty, ty + 200], color=C_CYAN, lw=6, alpha=0.3)
        # Water Wash overlay
        ax.add_patch(plt.Rectangle((100, 300), 880, 1400, color=C_WATER, alpha=0.1, zorder=0))

    elif mach_data['type'] == 'FURNACE':
        # Crucible
        heat = mach_data['heat']
        ax.scatter([540], [800], s=80000, color=C_VOID, edgecolors=C_CYAN, lw=10)
        ax.scatter([540], [800], s=60000, color=C_FIRE, alpha=heat*0.4)
        ax.scatter([540], [800], s=30000, color=C_GOLD, alpha=heat*0.2)

    # -------- PARTICLES (THE PAYLOAD) --------
    color_array = np.where(is_gold[:, None], hex_to_rgba(C_GOLD), hex_to_rgba(C_RED))
    color_array[:, 3] = p_alphas  # Apply dynamic alpha
    
    # Render Rock/Tailings (Underneath)
    mask_rock = ~is_gold
    ax.scatter(p_x[mask_rock], p_y[mask_rock], s=p_sizes[mask_rock], c=color_array[mask_rock], marker='H', zorder=5)
    
    # Render Gold (On Top - Neop Pop Bloom)
    mask_gold = is_gold
    ax.scatter(p_x[mask_gold], p_y[mask_gold], s=p_sizes[mask_gold]*1.5, c=color_array[mask_gold], zorder=10)
    ax.scatter(p_x[mask_gold], p_y[mask_gold], s=p_sizes[mask_gold]*4, c=C_GOLD, alpha=0.3, zorder=9) # Glow

    # -------- TELEMETRY WIDGETS --------
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.9))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_color, lw=2)
    ax.text(0.04, 0.965, "LOGIC GARDEN 155 :: MBMM GRAVITY SEPARATION", transform=ax.transAxes, color=C_TEXT, fontsize=22, fontname='monospace', weight='bold', va='center')

    # Data Panel
    sg_rock = 2.7
    sg_gold = 19.3
    ax.text(0.04, 0.88, f"GANGUE (ROCK) S.G. : {sg_rock:>05.2f} g/cm3", transform=ax.transAxes, color=C_RED, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.85, f"AURUM  (GOLD) S.G. : {sg_gold:>05.2f} g/cm3", transform=ax.transAxes, color=C_GOLD, fontsize=20, fontname='monospace')
    
    phase_data = mach_data.get('telemetry', '')
    ax.text(0.04, 0.81, phase_data, transform=ax.transAxes, color=ui_color, fontsize=20, fontname='monospace')

    # Bottom Terminal
    ax.add_patch(plt.Rectangle((0, 0), 0.95, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
    ax.plot([0, 0.95], [0.12, 0.12], transform=ax.transAxes, color=ui_color, lw=2)
    
    pulse = ui_color if (f % 30 < 15) or ui_color == C_MANTIS else C_TEXT
    ax.text(0.04, 0.08, "SYSTEM STATUS:", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=28, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    fig.clf(); plt.close(fig); plt.close('all'); gc.collect() 
    return f

# ------------------------------------------------------------------
# PHYSICS ENGINE (DETERMINISTIC PHASE ROUTING)
# ------------------------------------------------------------------
def generate_physics_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        p_x = np.zeros(NUM_PARTICLES)
        p_y = np.zeros(NUM_PARTICLES)
        p_sizes = np.ones(NUM_PARTICLES)
        p_alphas = np.ones(NUM_PARTICLES)
        mach_data = {}

        # -----------------------------------------------------------
        # PHASE 1: JAW CRUSHER (0 - 10s)
        # -----------------------------------------------------------
        if t_sec < 10.0:
            state = "[01] JAW CRUSHER (MECHANICAL ENTROPY)"
            ui_col = C_RED
            
            # Machine Math: Jaw oscillating
            osc = abs(math.sin(t_sec * 8.0))
            mach_data = {'type': 'CRUSHER', 'jaw_gap': 200 - (osc * 100), 'telemetry': f"CRUSHING FORCE: {120 + osc*40:.1f} MPa"}
            
            # Particle Math: Flowing down the V-chamber
            drop_y = 1920 - ((t_sec * 300 + p_id * 5) % 1500)
            
            # Squeeze x based on y position (The V funnel)
            funnel_width = np.clip((drop_y - 600) / 1000.0, 0.1, 1.0) * 350
            
            # Jitter increases as they get squeezed
            jitter = (1.0 - funnel_width/350) * 40 * r_offset_x
            
            p_x = 540 + (r_offset_x * funnel_width) + jitter
            p_y = drop_y
            
            # Particles shatter (get smaller) as they hit the bottom
            p_sizes = np.where(drop_y > 1000, 150, np.where(drop_y > 700, 50, 15))

        # -----------------------------------------------------------
        # PHASE 2: THE SHAKER TABLE (10 - 24s)
        # -----------------------------------------------------------
        elif t_sec < 24.0:
            state = "[02] SHAKER TABLE (SPECIFIC GRAVITY BINDING)"
            ui_col = C_CYAN
            phase_t = t_sec - 10.0
            
            # Machine Math: High-frequency shaking
            shake = math.sin(phase_t * 50.0) * 15
            mach_data = {'type': 'TABLE', 'shake': shake, 'telemetry': f"DECK FREQUENCY: 300 RPM"}
            
            # Slurry flow from Top Left (200, 1600) to Bottom Right
            # Timeline loops every 4 seconds for continuous visual flow
            flow_t = (phase_t + (p_id / float(NUM_PARTICLES)) * 4.0) % 4.0
            progress = flow_t / 4.0  # 0.0 to 1.0
            
            # The Routing Logic (Density Sorting)
            # Gold (Heavy) catches the diagonal riffles and walks RIGHT and UP.
            gold_x = 200 + (progress * 700) + shake
            gold_y = 1400 + (progress * 200) # Walks UP the table
            
            # Rock (Light) washes directly DOWN and RIGHT with the water
            rock_x = 200 + (progress * 600) + shake + (r_offset_x * 100)
            rock_y = 1400 - (progress * 1100) + (r_offset_y * 100)
            
            p_x = np.where(is_gold, gold_x, rock_x)
            p_y = np.where(is_gold, gold_y, rock_y)
            p_sizes = np.full(NUM_PARTICLES, 20)
            
            # Tailings fade out at the bottom
            p_alphas = np.where(~is_gold & (p_y < 500), np.clip((p_y - 200)/300, 0, 1), 1.0)

        # -----------------------------------------------------------
        # PHASE 3: THE FURNACE (24 - 35s)
        # -----------------------------------------------------------
        else:
            state = "[03] THERMAL PHASE TRANSITION (TATHĀTĀ)"
            ui_col = C_MANTIS if t_sec > 32 else C_FIRE
            phase_t = t_sec - 24.0
            
            # Machine Math: Rising heat bloom
            heat_val = np.clip(phase_t / 5.0, 0, 1)
            mach_data = {'type': 'FURNACE', 'heat': heat_val, 'telemetry': f"CRUCIBLE TEMP: {int(20 + heat_val*1044)} °C"}
            
            # Hide the rock completely
            p_alphas = np.where(~is_gold, 0.0, 1.0)
            
            # Gold particles fall into the crucible, then coalesce
            target_x = 540
            target_y = 800
            
            if phase_t < 3.0:
                # Falling in (Gravity)
                fall_p = phase_t / 3.0
                p_x = np.where(is_gold, target_x + (r_offset_x * 400 * (1-fall_p)), 0)
                p_y = np.where(is_gold, 1800 - (fall_p * 1000) + (r_offset_y * 200 * (1-fall_p)), 0)
                p_sizes = np.full(NUM_PARTICLES, 25)
            else:
                # Melting into the singular button (Tathātā)
                melt_p = np.clip((phase_t - 3.0) / 4.0, 0, 1)
                
                # Orbit and shrink radius towards absolute center
                orbit_angle = p_id + (phase_t * 2.0)
                radius = (1.0 - melt_p) * 150
                
                p_x = np.where(is_gold, target_x + np.cos(orbit_angle) * radius, 0)
                p_y = np.where(is_gold, target_y + np.sin(orbit_angle) * radius, 0)
                
                # As they converge, they become a single giant mass
                p_sizes = np.where(is_gold, 25 + (melt_p * 150), 0)
                # At Terminal Green Flow (32s+), state reaches absolute stillness.
                if t_sec > 32:
                    state = "[04] TERMINAL GREEN FLOW (ABSOLUTE YIELD)"

        yield (f, t_sec, state, ui_col, p_x, p_y, p_sizes, p_alphas, mach_data)

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 155: GRAVITY SEPARATION (MBMM) [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_physics_stream(), chunksize=4):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Batch Execution Complete. Stand by for ffmpeg assembly.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
