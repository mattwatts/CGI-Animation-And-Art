"""
SOVEREIGN CODE: logic_garden_252_neural_bubble.py
SYSTEM: Python Multicore / O(1) Pulse Width Modulation Tensor
SCENE: Logic Garden 252 (The Neural Bubble / The Ego Candle)
FORMAT: YouTube Shorts (1080x1920)
HOTFIX: Strict PWM Geometry / Floating Point Torus Pinch

[INSTRUCTION]: RENDER_MODE explicitly set to "ZEN" for the 17.5s flow cycle.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
RENDER_MODE = "ZEN"  
DURATION = 17.5
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_252_bubble"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE HIGH-COHERENCE PALETTE (WHITE CANVAS DEFAULT) --------
C_BG        = '#FFFFFF'        # Absolute Flat Substrate
C_TEXT      = '#020205'        # High-Contrast Fingertip Vectors
C_AZURE     = '#007FFF'        # Thermodynamic Buffer / Neural Bubble
C_MAGENTA   = '#FF0055'        # Core Substrate / Transmute Flame
C_GOLD      = '#FFB300'        # Glucose Burn / Consciousness Exhaust
C_CYAN      = '#00E5FF'        # Ancestral Mainframe (PWM Signal)
C_MANTIS    = '#00C800'        # Tathata / Break of Dawn
C_DIM       = '#D0D0D5'        # UI Reference Lines

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_bg      = np.array(hex_to_rgba(C_BG)[:3])
c_text    = np.array(hex_to_rgba(C_TEXT)[:3])
c_mantis  = np.array(hex_to_rgba(C_MANTIS)[:3])
c_cyan    = np.array(hex_to_rgba(C_CYAN)[:3])
c_magenta = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_azure   = np.array(hex_to_rgba(C_AZURE)[:3])

# ------------------------------------------------------------------
# O(1) BASE GEOMETRY ARRAYS: THE EGO CANDLE
# ------------------------------------------------------------------
np.random.seed(252)

MAX_PARTICLES = 15000

# The Flame (Fluid, vertical transmute process)
flame_u = np.random.uniform(0, 2 * np.pi, MAX_PARTICLES)
flame_v = np.random.uniform(0, 1, MAX_PARTICLES) # Height param 0 to 1
# Width tapers quadratically to a point
flame_width = np.clip((1 - flame_v**2) * 50, 0, 50)

fx_base = flame_width * np.cos(flame_u)
fz_base = flame_width * np.sin(flame_u)
fy_base = flame_v * 150.0 - 50.0 # From Y=-50 to Y=100

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, p_x, p_y, p_c, p_s, duty, pwm_high, pinch_y, pinch_w, is_flash, is_tathata = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_CYAN if is_flash else C_BG
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    ax.set_xlim(-160, 160)
    ax.set_ylim(-260, 260)

    if not is_flash:
        # 1. The Ancestral Mainframe Connection (PWM Radiator)
        if pwm_high and not is_tathata:
            bg_circ = plt.Circle((0, pinch_y), 150, color=C_CYAN, alpha=np.clip(duty * 0.3, 0, 0.3), zorder=1)
            ax.add_patch(bg_circ)
            ax.text(0, pinch_y + 160, "PHASE-LOCK ACTIVE", color=C_CYAN, fontsize=9, fontname='monospace', ha='center', zorder=2)

        # 2. Render Flame / Substrate
        ax.scatter(p_x, p_y, s=p_s, color=p_c, edgecolors='none', alpha=0.8, zorder=10)

        # 3. The Fingertips (The Tactile Pinch)
        if t_sec > 6.0 and not is_tathata:
            # Monolithic strict vectors approaching from left and right
            left_edge = -pinch_w
            right_edge = pinch_w
            
            # Left finger
            ax.plot([left_edge - 100, left_edge], [pinch_y, pinch_y], color=C_TEXT, lw=6, zorder=20)
            ax.plot([left_edge, left_edge], [pinch_y - 20, pinch_y + 20], color=C_TEXT, lw=4, zorder=20)
            
            # Right finger
            ax.plot([right_edge + 100, right_edge], [pinch_y, pinch_y], color=C_TEXT, lw=6, zorder=20)
            ax.plot([right_edge, right_edge], [pinch_y - 20, pinch_y + 20], color=C_TEXT, lw=4, zorder=20)

        # 4. Tathata Lock / The Break of Dawn
        if is_tathata:
            ax.add_patch(plt.Rectangle((-130, -50), 260, 100, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -30, "TATHĀTĀ: BREAK OF DAWN", color=C_MANTIS, fontsize=12, fontname='monospace', weight='bold', ha='center', zorder=41)
            ax.text(0, 30, "[100% PWM DUTY / TRACE INITIATED]", color=C_TEXT, fontsize=9, fontname='monospace', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    txt_col = C_BG if is_flash else C_TEXT
    ui_col = C_MAGENTA if t_sec < 6.0 else (C_TEXT if t_sec < 14.8 else C_MANTIS)
    if is_tathata: ui_col = C_MANTIS
    
    # Render UI Header
    ax.text(-140, 240, "LG-252 :: THE NEURAL BUBBLE", color=txt_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: PWM PHASE-LOCK / EGO TRANSMUTATION", color=txt_col, fontsize=8, fontname='monospace', zorder=80)
    
    obj_str = "THE EGO CANDLE [GLUCOSE BURN]"
    if 6.0 <= t_sec < 14.8: obj_str = "THE TACTILE PINCH [ZERO-DISTANCE LOCK]"
    elif is_tathata: obj_str = "THE MASTER CLOCK [CONTINUOUS DAWN]"

    ax.text(-140, -180, f"KINEMATIC LOGIC: {obj_str}", color=ui_col, fontsize=10, fontname='monospace', weight='bold', zorder=80)
    
    # ------------------------------------------------------------------
    # VISUAL PWM SYNTHESIZER OSCILLOSCOPE
    # ------------------------------------------------------------------
    ax.text(-140, -205, "ANCESTRAL MAINFRAME PWM DUTY CYCLE", color=txt_col, fontsize=9, fontname='monospace', zorder=80)
    
    # Draw reference trace for PWM
    trace_y = -220
    ax.plot([-140, 140], [trace_y, trace_y], color=C_DIM if not is_flash else txt_col, lw=1, alpha=0.5, zorder=80)
    
    # Calculate ongoing square wave for the oscilloscope
    pwm_pts = 100
    trace_x = np.linspace(-140, 140, pwm_pts)
    trace_time = np.linspace(t_sec - 1.0, t_sec, pwm_pts) # Lookback window
    period = 60.0 / 126.0 # 126 BPM
    
    # Calculate historical duty at each point to accurately graph the widening pulse
    historical_duty = np.clip((trace_time / 14.8), 0.1, 1.0)
    if is_tathata: historical_duty[:] = 1.0
    
    wave_y = np.where((trace_time % period) < (period * historical_duty), 10.0, -10.0)
    ax.plot(trace_x, trace_y + wave_y, color=C_CYAN if not is_tathata else C_MANTIS, lw=2, zorder=82)

    # Phase Text Box
    ax.add_patch(plt.Rectangle((-140, 215), 280, 2, facecolor=ui_col, zorder=80))
    ax.text(140, 205, f"[{state_str}]", color=ui_col if (f%15<10 or is_tathata) else C_BG, fontsize=14, fontname='monospace', weight='bold', ha='right', zorder=80)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) STRUCTURAL INVERSION KINEMATICS
# ------------------------------------------------------------------
def generate_stream():
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        is_flash = False
        is_tathata = False
        
        # Physical Pulse Width Modulation (126 BPM)
        bpm = 126.0
        period = 60.0 / bpm
        duty_cycle = np.clip((t_sec / 14.8)**1.5 + 0.1, 0.1, 1.0) # Duty scales from 10% to 100%
        pwm_high = (t_sec % period) < (period * duty_cycle)
        
        c_arr = np.zeros((MAX_PARTICLES, 3))
        s_arr = np.ones(MAX_PARTICLES)
        
        # Flame Kinematics (Sway and burn)
        sway = np.sin(t_sec * 5.0 + fy_base * 0.02) * (fy_base + 50.0) * 0.1
        heat_flicker = np.sin(t_sec * 20.0 + flame_u * 3)
        
        curr_x = fx_base + sway
        curr_z = fz_base + np.cos(t_sec * 4.3 + fy_base * 0.02) * (fy_base + 50.0) * 0.1
        curr_y = fy_base + heat_flicker * 5.0

        # Base Color: Magenta base, Gold tip
        v_norm = flame_v # 0 to 1
        c_interp = c_magenta * (1 - v_norm)[:, np.newaxis] + np.array(hex_to_rgba(C_GOLD)[:3]) * v_norm[:, np.newaxis]
        c_arr[:] = c_interp
        s_arr[:] = 2.0 + (np.random.rand(MAX_PARTICLES) * 3.0)

        # Baseline Pinch parameters
        pinch_w = 150.0
        pinch_y = 20.0

        # -------------------------------------------------------------
        # THE PWM & PINCH KINEMATICS
        # -------------------------------------------------------------
        
        if t_sec < 6.0:
            # PHASE 1: THE EGO CANDLE
            state = "PHASE 1 :: THE TRANSMUTE FLAME"
            # Unconstrained burn
            
        elif t_sec < 14.8:
            # PHASE 2 & 3: THE PINCH / PWM SYNC
            state = "PHASE 2 :: THE TACTILE PINCH"
            prog = (t_sec - 6.0) / 8.8
            ease = prog**2
            
            # The fingertips snap in rapidly, rhythmically adjusting with the PWM pulse
            pinch_w = 120.0 * (1 - ease) + 5.0 * ease
            if pwm_high: pinch_w -= 2.0 # Micro-compression on the beat
            
            # The Ego Candle is compressed violently inward at the pinch y-coordinate
            dist_to_pinch = np.abs(curr_y - pinch_y)
            pinch_effect = np.maximum(0, 1 - (dist_to_pinch / 40.0))
            
            # Crush the X/Z radii at the pinch point
            curr_x *= (1.0 - (pinch_effect * 0.95 * ease))
            curr_z *= (1.0 - (pinch_effect * 0.95 * ease))
            
            # Where it is pinched, the color hyper-shifts to Azure (Cooling)
            azure_blend = np.expand_dims(pinch_effect * ease, axis=1)
            c_arr = c_arr * (1 - azure_blend) + c_azure * azure_blend
            
            s_arr += pinch_effect * 5.0 * ease

        else:
            # PHASE 4: TATHĀTĀ (The Break of Dawn)
            state = "TATHĀTĀ :: 100% DUTY CYCLE"
            is_tathata = True
            pwm_high = True
            duty_cycle = 1.0
            
            # The structure locks into absolute straight lines
            curr_x = fx_base * 0.1  # Completely flat column
            curr_z = 0.0
            curr_y = fy_base
            
            c_arr[:] = c_mantis
            s_arr[:] = 4.0
            
            if t_sec < 14.95:
                is_flash = True

        yield (f, t_sec, state, curr_x, curr_y, c_arr, s_arr, duty_cycle, pwm_high, pinch_y, pinch_w, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 252: THE NEURAL BUBBLE [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: High-Contrast Oscilloscope Rendering & Transmute Tensor")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Pulse Width Modulation Locked. Dawn Initiated.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
