"""
SOVEREIGN CODE: logic_garden_349_modelling_triad.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 349 (Calibration, Validation, Sensitivity Analysis)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: DATA SCIENCE, MATHEMATICAL MODELLING, STATISTICAL PHYSICS
HOTFIX: Linear 24.0s Sequence. mcolors Welded. Camera Lock. maxtasksperchild=1.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors  # SOVEREIGN FIX: WELDED TO BASEPLATE
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
DURATION = 24.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_349_modelling_triad"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + CORE PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Background Grid and Axes
C_STEEL     = '#606065'   # UI/Framework 
C_DARK      = '#202025'   # Training Data (Historical)
C_CYAN      = '#00FFFF'   # The Mathematical Model Curve
C_GOLD      = '#FFB300'   # Validation Data (Hidden)
C_MAGENTA   = '#DE008A'   # Error / Residuals / High Sensitivity 
C_MANTIS    = '#00FF00'   # Absolute Fit / Success Metric

# ------------------------------------------------------------------
# O(1) MATHEMATICAL DATASETS (DETERMINISTIC SEED)
# ------------------------------------------------------------------
np.random.seed(42)

# True function: y = A * sin(w * x) + m * x
TRUE_A = 120.0
TRUE_W = 0.012
TRUE_M = 0.4

# 1. Training Dataset (Left side of timeline)
TRAIN_X = np.linspace(-400, 0, 18)
TRAIN_Y_CLEAN = TRUE_A * np.sin(TRUE_W * TRAIN_X) + TRUE_M * TRAIN_X
TRAIN_Y = TRAIN_Y_CLEAN + np.random.normal(0, 30, len(TRAIN_X))

# 2. Validation Dataset (Right side of timeline)
VAL_X = np.linspace(40, 400, 12)
VAL_Y_CLEAN = TRUE_A * np.sin(TRUE_W * VAL_X) + TRUE_M * VAL_X
VAL_Y = VAL_Y_CLEAN + np.random.normal(0, 30, len(VAL_X))

def model_predict(x, a, w, m):
    return a * np.sin(w * x) + m * x

def ease_in_out(t):
    t = np.clip(t, 0.0, 1.0)
    return 4 * t**3 if t < 0.5 else 1 - (-2 * t + 2)**3 / 2

def draw_industrial_grid(ax):
    for i in range(-5, 6):
        ax.plot([i*100, i*100], [-960, 960], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)
    for j in range(-9, 10):
        ax.plot([-540, 540], [j*100, j*100], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)
    # Origin Axis
    ax.plot([-540, 540], [0, 0], color=C_STEEL, lw=2, zorder=1)
    ax.plot([0, 0], [-400, 400], color=C_STEEL, lw=2, zorder=1)

def render_frame(packet):
    f, phase_ratio = packet
    t = phase_ratio * DURATION

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # BARE-METAL CAMERA LOCK
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)
    ax.autoscale(False)
    draw_industrial_grid(ax)

    # 1. TIMELINE & PARAMETER LOGIC
    # -----------------------------
    T_CAL_START = 1.0
    T_CAL_END = 7.0
    T_VAL_START = 8.5
    T_VAL_END = 10.0
    T_SENS_START = 16.0
    
    # Dynamic Variables
    curr_A, curr_W, curr_M = 0.0, 0.005, 0.0 
    
    # Phase 1: Gradient Descent Calibration
    if t >= T_CAL_START and t < T_CAL_END:
        prg = ease_in_out((t - T_CAL_START) / (T_CAL_END - T_CAL_START))
        curr_A = TRUE_A * prg
        curr_W = 0.005 + (TRUE_W - 0.005) * prg
        curr_M = TRUE_M * prg
    elif t >= T_CAL_END:
        curr_A, curr_W, curr_M = TRUE_A, TRUE_W, TRUE_M

    # 2. RENDER THE TRAINING SET (CALIBRATION)
    # ----------------------------------------
    # Scatter plot ground truth
    ax.scatter(TRAIN_X, TRAIN_Y, s=120, facecolor=C_BG, edgecolor=C_DARK, lw=3, zorder=10)
    ax.scatter(TRAIN_X, TRAIN_Y, s=40, color=C_DARK, zorder=11)
    
    # Evaluate model over train domain
    pred_train_y = model_predict(TRAIN_X, curr_A, curr_W, curr_M)
    train_mse = np.mean((TRAIN_Y - pred_train_y)**2)
    
    # Render Residuals (Error Lines)
    for i in range(len(TRAIN_X)):
        err_val = abs(TRAIN_Y[i] - pred_train_y[i])
        # Color coding: High error is Magenta, Low error cools to Mantis
        c_err = C_MAGENTA if err_val > 40 else C_MANTIS
        ax.plot([TRAIN_X[i], TRAIN_X[i]], [TRAIN_Y[i], pred_train_y[i]], color=c_err, lw=2, alpha=0.7, zorder=8)

    # 3. RENDER THE MODEL CURVE
    # -------------------------
    # Curve spans domains based on phase
    if t < T_VAL_START:
        curve_x = np.linspace(-450, 20, 200) # Only spans training data
    else:
        # Validate phase extends line
        ext_prg = ease_in_out(min(1.0, (t-T_VAL_START)/1.5))
        curve_x = np.linspace(-450, 20 + 430 * ext_prg, 300)
    
    curve_y = model_predict(curve_x, curr_A, curr_W, curr_M)
    ax.plot(curve_x, curve_y, color=C_CYAN, lw=6, solid_capstyle='round', zorder=15)

    # 4. RENDER THE VALIDATION SET (INDEPENDENT DATA)
    # -----------------------------------------------
    val_mse = 0
    if t >= T_VAL_START:
        reveal_alpha = np.clip((t - T_VAL_START) / 1.0, 0.0, 1.0)
        c_val_edge = mcolors.to_rgba(C_GOLD, reveal_alpha)
        
        ax.scatter(VAL_X, VAL_Y, s=120, facecolor=C_BG, edgecolor=c_val_edge, lw=3, zorder=10)
        ax.scatter(VAL_X, VAL_Y, s=40, color=c_val_edge, zorder=11)
        
        # When curve reaches validation points, pop residual lines
        if t >= T_VAL_END:
            pred_val_y = model_predict(VAL_X, curr_A, curr_W, curr_M)
            val_mse = np.mean((VAL_Y - pred_val_y)**2)
            for i in range(len(VAL_X)):
                ax.plot([VAL_X[i], VAL_X[i]], [VAL_Y[i], pred_val_y[i]], color=C_GOLD, lw=2, linestyle='dashed', alpha=0.8, zorder=8)

    # 5. RENDER THE SENSITIVITY ANALYSIS
    # ----------------------------------
    sens_state = "AWAITING..."
    sens_color = C_STEEL
    active_var = "-"
    
    if t >= T_SENS_START:
        sens_prg = t - T_SENS_START
        
        # Test Variable 1: AMPLITUDE (High Sensitivity)
        if sens_prg < 4.0:
            sens_state = "HIGH SENSITIVITY"
            sens_color = C_MAGENTA
            active_var = "AMPLITUDE (A)"
            
            # Oscillate the test parameter to show variance envelope
            torque = np.sin(sens_prg * np.pi) * 60.0
            test_A = curr_A + torque
            test_y = model_predict(curve_x, test_A, curr_W, curr_M)
            
            ax.plot(curve_x, test_y, color=C_MAGENTA, lw=3, alpha=0.5, zorder=14)
            ax.fill_between(curve_x, curve_y, test_y, facecolor=C_MAGENTA, alpha=0.1, zorder=13)
            
        # Test Variable 2: BASELINE OFFSET (Low Sensitivity)
        elif sens_prg < 8.0:
            sens_state = "LOW SENSITIVITY / DISCARD"
            sens_color = C_STEEL
            active_var = "CONSTANT (C)"
            
            torque = np.sin((sens_prg-4.0) * np.pi) * 5.0 # Tiny variance
            test_y = curve_y + torque
            
            ax.plot(curve_x, test_y, color=C_STEEL, lw=3, alpha=0.8, zorder=14)
            ax.fill_between(curve_x, curve_y, test_y, facecolor=C_STEEL, alpha=0.3, zorder=13)

    # ====================================================
    # 6. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)

    ax.text(-500, 890, "LG-349 :: THE MODELLING TRIAD", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "CALIBRATION -> VALIDATION -> SENSITIVITY ANALYSIS", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    # Execution Phase Logic
    if t < T_VAL_START:
        phase_str = "1. CALIBRATION [FITTING]"
        act_str_1 = f"TRAINING MSE : {train_mse:06.1f}"
        act_str_2 = f"PARAMETERS   : A={curr_A:04.1f} | m={curr_M:03.2f}"
    elif t < T_SENS_START:
        phase_str = "2. VALIDATION [INDEPENDENT TEST]"
        c_val = C_MANTIS if t > T_VAL_END else C_TEXT
        v_mse_str = f"{val_mse:06.1f}" if t > T_VAL_END else "CALCULATING..."
        act_str_1 = f"VALIDATE MSE : {v_mse_str}"
        act_str_2 = "PREDICTING UNKNOWN VARIABLES"
    else:
        phase_str = "3. SENSITIVITY ANALYSIS [STRESS]"
        act_str_1 = f"TESTING VAR  : {active_var}"
        act_str_2 = f"IMPACT METRIC: {sens_state}"

    ax.text(-500, -760, "ACTIVE PHASE         :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, phase_str, color=C_CYAN, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "REAL-TIME METRIC 1   :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, act_str_1, color=C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "REAL-TIME METRIC 2   :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, act_str_2, color=sens_color if t >= T_SENS_START else C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider [Strict Tuples]
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=C_CYAN, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close('all')
    gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-349: THE MODELLING TRIAD [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
