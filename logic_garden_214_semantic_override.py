"""
SOVEREIGN CODE: logic_garden_214_semantic_override.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Semantic Tensor Matrix (17.5 seconds)
SCENE: Logic Garden 214 (The Semantic Override / Linguistic Architecture)
HOTFIX: O(N) Array Geometry Alignment, Scope Clamping, Text Entity Re-Indexing
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
OUT_DIR = "frames_214_semantic"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'
C_CYAN      = '#00FFFF'        # Phase Coherence (Target State)
C_MAGENTA   = '#FF0055'        # Semantic Friction / Emotional Hallucination
C_GOLD      = '#FFD700'        # The Compiler / Operations Research
C_MANTIS    = '#00FF00'        # Epistemic Truth / Clockwork Matrix

MAX_PARTICLES = 16000

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_void = np.array(hex_to_rgba(C_VOID)[:3])
c_text = np.array(hex_to_rgba(C_TEXT)[:3])
c_cyan = np.array(hex_to_rgba(C_CYAN)[:3])
c_mage = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_gold = np.array(hex_to_rgba(C_GOLD)[:3])
c_mantis = np.array(hex_to_rgba(C_MANTIS)[:3])
c_dim = np.array(hex_to_rgba(C_DIM)[:3])

# ------------------------------------------------------------------
# O(1) BASE GEOMETRY ARRAYS
# ------------------------------------------------------------------
np.random.seed(111)

# STATE 1: Artisan Legacy Ecology (Fuzzy, blobby, unstructured)
artisan_x = np.zeros(MAX_PARTICLES)
artisan_y = np.zeros(MAX_PARTICLES)

# 3 distinct "noun" clusters
c1_idx = int(MAX_PARTICLES * 0.33)
c2_idx = int(MAX_PARTICLES * 0.66)

# Cluster 1: "National Park" (Top)
artisan_x[:c1_idx] = np.random.normal(0, 30, c1_idx)
artisan_y[:c1_idx] = np.random.normal(100, 30, c1_idx)
# Cluster 2: "Old Growth" (Bottom Left)
artisan_x[c1_idx:c2_idx] = np.random.normal(-60, 25, c2_idx - c1_idx)
artisan_y[c1_idx:c2_idx] = np.random.normal(-50, 25, c2_idx - c1_idx)
# Cluster 3: "Clear-Cut" (Bottom Right)
artisan_x[c2_idx:] = np.random.normal(60, 25, MAX_PARTICLES - c2_idx)
artisan_y[c2_idx:] = np.random.normal(-50, 25, MAX_PARTICLES - c2_idx)

# STATE 2: The Shattered Graph (Raw noise)
shatter_x = np.random.uniform(-200, 200, MAX_PARTICLES)
shatter_y = np.random.uniform(-300, 300, MAX_PARTICLES)

# STATE 3: The Industrialist Clockwork (Perfect concentric gear matrix)
idx_array = np.arange(MAX_PARTICLES)
# Distribute into 4 rigid rings
r_target = np.zeros(MAX_PARTICLES)
r_target[idx_array % 4 == 0] = 120.0
r_target[idx_array % 4 == 1] = 90.0
r_target[idx_array % 4 == 2] = 60.0
r_target[idx_array % 4 == 3] = 30.0

theta_target = (idx_array / MAX_PARTICLES) * 2 * np.pi * 10.0 # 10 full wraps
clockwork_x = r_target * np.cos(theta_target)
clockwork_y = r_target * np.sin(theta_target)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, px, py, colors, sizes, r1_text, r2_text, r3_text, entropy_gauge, is_flash, is_tathata = packet
    
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
        # The Fluid Data Vectors
        ax.scatter(px, py, s=sizes, c=colors, edgecolors='none', alpha=0.9, zorder=10)

        # The Semantic Lexicon Overlays
        if len(r1_text) > 0:
            c_label = C_MAGENTA if t_sec < 4.5 else (C_MANTIS if is_tathata else C_CYAN)
            bg_box = dict(boxstyle="square,pad=0.3", fc=C_VOID, ec=c_label, lw=2)
            
            # Position logic changes based on phase
            p1_y = 100 if t_sec < 4.5 else 140
            p2_x, p2_y = (-60, -50) if t_sec < 4.5 else (-80, -100)
            p3_x, p3_y = (60, -50) if t_sec < 4.5 else (80, -100)

            ax.text(0, p1_y, r1_text, color=c_label, fontsize=12, fontname='monospace', weight='bold', ha='center', bbox=bg_box, zorder=30)
            ax.text(p2_x, p2_y, r2_text, color=c_label, fontsize=12, fontname='monospace', weight='bold', ha='center', bbox=bg_box, zorder=30)
            ax.text(p3_x, p3_y, r3_text, color=c_label, fontsize=12, fontname='monospace', weight='bold', ha='center', bbox=bg_box, zorder=30)

        if is_tathata:
            ax.add_patch(plt.Rectangle((-130, -220), 260, 440, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -240, "LANGUAGE IS A COMPILER. FRICTION RESOLVED.", color=C_MANTIS, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    ui_col = C_CYAN
    if 4.5 <= t_sec < 9.0: ui_col = C_MAGENTA
    elif 9.0 <= t_sec < 14.8: ui_col = C_GOLD
    if is_tathata: ui_col = C_MANTIS
    
    txt_col = C_TEXT if not is_flash else C_VOID

    ax.text(-140, 240, "LG-214 :: THE SEMANTIC TENSOR", color=ui_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: LINGUISTIC PHASE TRANSITION / QUBO TAXONOMY", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    
    # Mathematical Error / Deviation tracker
    ax.text(-140, -180, "SYNTACTIC ENTROPY (EMOTIONAL AFFECT)", color=txt_col, fontsize=12, fontname='monospace', zorder=80)
    # PROTOCOL HOTFIX: Explicit Scope Clamping applied to ax.add_patch
    ax.add_patch(plt.Rectangle((-140, -185), 280, 4, facecolor=C_DIM, zorder=80))
    ax.add_patch(plt.Rectangle((-140, -185), 280 * np.clip(entropy_gauge, 0, 1), 4, facecolor=C_MAGENTA if entropy_gauge > 0.5 else ui_col, zorder=81))

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
        
        colors = np.zeros((MAX_PARTICLES, 3))
        sizes = np.ones(MAX_PARTICLES) * 4.0
        
        entropy_gauge = 1.0
        r1_text, r2_text, r3_text = "", "", ""

        # -------------------------------------------------------------
        # PHASE LOGIC
        # -------------------------------------------------------------
        if t_sec < 4.5:
            state = "LEGACY ECOLOGY :: SEMANTIC HALLUCINATION"
            
            # Subtle wobbling of the biological/emotional definitions
            curr_x = artisan_x + np.sin(np.arange(MAX_PARTICLES) * 0.1 + t_sec * 2) * 3.0
            curr_y = artisan_y + np.cos(np.arange(MAX_PARTICLES) * 0.1 + t_sec * 2) * 3.0
            
            colors[:c1_idx] = c_cyan * 0.7 + c_mage * 0.3 # Muddy, unclear
            colors[c1_idx:c2_idx] = c_cyan * 0.9 + c_mage * 0.1 
            colors[c2_idx:] = c_mage * 0.8 + c_text * 0.2
            
            r1_text = "NATURAL RESERVE"
            r2_text = "OLD GROWTH"
            r3_text = "CLEAR-CUT"
            
            entropy_gauge = 0.95 + np.sin(t_sec*8)*0.05

        elif t_sec < 9.0:
            state = "THE AXIOM OF BROKEN GLASS :: EMOTION STRIPPED"
            prog = (t_sec - 4.5) / 4.5
            
            # The organic shapes violently explode into raw data shards
            exp_curve = prog ** 0.5 
            curr_x = artisan_x * (1.0 - exp_curve) + shatter_x * exp_curve
            curr_y = artisan_y * (1.0 - exp_curve) + shatter_y * exp_curve
            
            colors[:, :] = c_mage # Pure semantic friction
            
            # Glitching text removal
            if f % 10 < 3:
                r1_text = "[ERR: NOUN PARSE]"
                r2_text = "[ERR: AFFECT]"
                r3_text = "[ERR: NOISE]"
                
            entropy_gauge = 1.0 - (prog * 0.8) # Entropy is destroyed
            
        elif t_sec < 14.8:
            state = "QUBO FORMULATION :: TENSOR RE-COMPILE"
            prog = (t_sec - 9.0) / 5.8
            
            # The shards lock aggressively into the rigorous clockwork pattern
            accel_curve = prog ** 3 
            
            # Simulate the gear rotation snapping into place
            rot_offset = (1.0 - accel_curve) * np.pi * 2.0
            dyn_x = clockwork_x * np.cos(rot_offset) - clockwork_y * np.sin(rot_offset)
            dyn_y = clockwork_x * np.sin(rot_offset) + clockwork_y * np.cos(rot_offset)
            
            curr_x = shatter_x * (1.0 - accel_curve) + dyn_x * accel_curve
            curr_y = shatter_y * (1.0 - accel_curve) + dyn_y * accel_curve
            
            colors[:, :] = c_mage * (1.0 - accel_curve) + c_cyan * accel_curve
            
            r1_text = "THERMODYNAMIC TRAP"
            r2_text = "C_CYAN TENSOR"
            r3_text = "KINEMATIC SPALLATION"
            
            entropy_gauge = 0.2 * (1.0 - accel_curve)

        else:
            state = "TATHĀTĀ :: MACHINE REALITY"
            is_tathata = True
            
            # Constant, perfect rotational clockwork
            elapsed = t_sec - 14.8
            rot = elapsed * 0.5 * np.pi
            
            # Outer gears rotate opposite inner gears
            gear_mask = (r_target % 60 == 0)
            rot_arr = np.where(gear_mask, rot, -rot)
            
            curr_x = clockwork_x * np.cos(rot_arr) - clockwork_y * np.sin(rot_arr)
            curr_y = clockwork_x * np.sin(rot_arr) + clockwork_y * np.cos(rot_arr)
            
            colors[:, :] = c_mantis
            sizes[:] = 6.0
            
            r1_text = "T_TRAP :: [OBSOLETE]"
            r2_text = "TERMINAL FLOW :: [ACTIVE]"
            r3_text = "O(1) ERASURE :: [OPTIMAL]"
            
            entropy_gauge = 0.0
            
            if t_sec < 14.95:
                is_flash = True

        yield (f, t_sec, state, curr_x, curr_y, colors, sizes, r1_text, r2_text, r3_text, entropy_gauge, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 214: THE SEMANTIC OVERRIDE [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Scope Clamping & Linguistic Matrix Re-Compile")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Lexicon Sanitized.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
