"""
SOVEREIGN CODE: logic_garden_312b_crossroads_tensor.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Kinematic Phase Tensor
SCENE: LG-312b (Aeronaut Node / Sub-Atmospheric Guitar String Tensor)
HOTFIX: Seamless 10s Loop, Cartesian Crossroads, IK Tremolo Exhaust
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle, Ellipse
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 10.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_312b_crossroads_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST ENGINEERING PALETTE --------
C_BG        = '#FFFFFF'       # Daylight Protocol Baseline
C_VOID      = '#0B0F19'       # Deep Nano-Carbon (Cowboy Black Armor)
C_IRON      = '#1C2833'       # Raw Carbon / Boots / Grid Lines
C_STEEL     = '#7F8C8D'       # Rigid Hydraulics / Frets / Instrument Neck
C_BRONZE    = '#B87333'       # Acoustic Resonance Chamber (The "Gibson")
C_GOLD      = '#F39C12'       # Fret Spallation / Pick 
C_MAGENTA   = '#E74C3C'       # Sonic Shockwave Exhaust
C_MANTIS    = '#27AE60'       # Output Logic / Telemetry
C_TEXT      = '#111111'

def hex_to_rgba(h, a=1.0):
    h = h.lstrip('#')
    return [int(h[0:2],16)/255.0, int(h[2:4],16)/255.0, int(h[4:6],16)/255.0, a]

c_shock = np.array(hex_to_rgba(C_GOLD)[:3])
c_exhaust = np.array(hex_to_rgba(C_MAGENTA)[:3])

# ------------------------------------------------------------------
# O(1) INVERSE KINEMATICS ENGINE
# ------------------------------------------------------------------
def solve_ik(hx, hy, tx, ty, L1, L2, bend_dir=1):
    dx, dy = tx - hx, ty - hy
    d = np.hypot(dx, dy)
    d = np.clip(d, 0.01, (L1 + L2) - 0.01)
    a = (L1**2 + d**2 - L2**2) / (2 * L1 * d)
    a = np.clip(a, -1.0, 1.0)
    alpha = np.arccos(a)
    theta = np.arctan2(dy, dx)
    joint_theta = theta + (alpha * bend_dir)
    jx = hx + L1 * np.cos(joint_theta)
    jy = hy + L1 * np.sin(joint_theta)
    return jx, jy

# ------------------------------------------------------------------
# ACOUSTIC SPALLATION PARTICLE MATRIX
# ------------------------------------------------------------------
np.random.seed(312)
MAX_SPARKS = 1800
p_life = np.random.uniform(0.0, 1.0, MAX_SPARKS)
p_ang = np.random.uniform(0, 2*np.pi, MAX_SPARKS)
p_vel = np.random.uniform(300.0, 1200.0, MAX_SPARKS)
p_type = np.random.choice([0, 1], MAX_SPARKS)

# ------------------------------------------------------------------
# MULTICORE RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    tau = float(f) / float(TOTAL_FRAMES)
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    fig.patch.set_facecolor(C_BG)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.set_facecolor(C_BG)
    # Scaled to fill the screen (macro proximity)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    CY_GND = 250.0
    CX = 540.0

    # 1. THE CARTESIAN CROSSROADS (X/Z Absolute Intersection)
    # -------------------------------------------------
    ax.add_patch(Rectangle((0, 0), 1080, CY_GND, facecolor='#F4F6F6', zorder=1))
    ax.plot([0, 1080], [CY_GND, CY_GND], color=C_STEEL, lw=16, zorder=2)
    
    # Horizon Grid Lines converging at the True Center
    for gx in [-500, -200, 100, 400, 700, 1000, 1300, 1600]:
        ax.plot([gx, CX], [0, CY_GND], color=C_STEEL, lw=6, alpha=0.3, zorder=2)
    
    # The Physical Stamped "Crossroad" Marker Plate
    ax.plot([0, 1080], [CY_GND - 100, CY_GND - 100], color=C_IRON, lw=35, zorder=3)
    ax.plot([CX, CX], [0, CY_GND], color=C_IRON, lw=50, zorder=4)

    # 2. THE AERONAUT NODE (Stance Geometry)
    # -------------------------------------------------
    # Rhythmic bouncing based on the "Lick" timeline
    lick_freq = 4.0   # 4 main riff structures per loop
    beat_freq = 16.0  # High frequency 16th-note foot tapping & bouncing
    
    b_phase = (tau * beat_freq) % 1.0
    y_bounce = np.abs(np.sin(b_phase * np.pi)) * 12.0
    
    CY_hip = 650.0 - y_bounce
    
    # Foot positions (Wide Power Stance)
    ax_L, ay_L = CX - 180, CY_GND
    ax_R, ay_R = CX + 180, CY_GND
    
    # Foot-tap math on the Right Foot (keeping time)
    if b_phase < 0.5:
        ay_R = CY_GND + np.sin((b_phase / 0.5) * np.pi) * 30.0

    shadow_w = 450 - (y_bounce * 2.0)
    ax.add_patch(Ellipse((CX, CY_GND), shadow_w, 40, facecolor=C_IRON, alpha=0.15, zorder=4))

    # Leg IK (Bend outwards slightly)
    kx_L, ky_L = solve_ik(CX-60, CY_hip, ax_L, ay_L+20, 240, 250, 1)
    kx_R, ky_R = solve_ik(CX+60, CY_hip, ax_R, ay_R+20, 240, 250, -1)
    
    def draw_leg(hx, hy, kx, ky, fx, fy, zbase, is_fg):
        # Heavy Navy/Carbon void material pants
        ax.plot([hx, kx], [hy, ky], color=C_VOID, lw=70, zorder=zbase, solid_capstyle='round', solid_joinstyle='round')
        ax.plot([kx, fx], [ky, fy], color=C_VOID, lw=55, zorder=zbase, solid_capstyle='round', solid_joinstyle='round')
        # Joint structural plate
        ax.add_patch(Circle((kx, ky), 22, facecolor=C_IRON, edgecolor=C_TEXT, lw=4, zorder=zbase+1))
        # Boot (Heavy Iron base)
        boot_a = 15 if is_fg else -15
        ax.add_patch(Polygon([(fx-40, fy+10), (fx+50, fy+10), (fx+50, fy-20), (fx-30, fy-20)], facecolor=C_IRON, edgecolor=C_TEXT, lw=4, zorder=zbase+1, joinstyle='round'))

    # Render BG Leg (Right)
    draw_leg(CX+60, CY_hip, kx_R, ky_R, ax_R, ay_R, 10, False)
    
    # 3. CHASSIS & SUB-ATMOSPHERIC RADOME (The Hat)
    # -------------------------------------------------
    CY_neck = CY_hip + 380
    # Torso (Hunched forward over the instrument)
    t_poly = [(CX-90, CY_hip-20), (CX+90, CY_hip-20), (CX+110, CY_neck), (CX-110, CY_neck)]
    ax.add_patch(Polygon(t_poly, facecolor=C_VOID, edgecolor=C_TEXT, lw=8, zorder=15, joinstyle='round'))

    # Aeronaut Radome (Cowboy Hat)
    cx_H, cy_H = CX, CY_neck + 80 - y_bounce
    
    # Rigid Faceplate / Mask
    ax.add_patch(Circle((cx_H, cy_H), 60, facecolor=C_IRON, edgecolor=C_TEXT, lw=4, zorder=40))
    ax.add_patch(Rectangle((cx_H-25, cy_H-15), 50, 15, facecolor=C_BG, zorder=41))
    ax.add_patch(Circle((cx_H, cy_H-7), 5, facecolor=C_MANTIS, zorder=42))

    # The Massive Radome Brim
    ax.add_patch(Ellipse((cx_H, cy_H+50), 320, 45, facecolor=C_VOID, edgecolor=C_TEXT, lw=8, zorder=43))
    ax.add_patch(Polygon([(cx_H-70, cy_H+50), (cx_H+70, cy_H+50), (cx_H+40, cy_H+150), (cx_H-40, cy_H+150)], facecolor=C_VOID, edgecolor=C_TEXT, lw=6, zorder=44, joinstyle='round'))
    ax.plot([cx_H-70, cx_H+70], [cy_H+70, cy_H+70], color=C_GOLD, lw=10, zorder=45) # Resonance Band

    # Render FG Leg (Left)
    draw_leg(CX-60, CY_hip, kx_L, ky_L, ax_L, ay_L, 20, True)

    # 4. ACOUSTIC BALLISTIC TENSOR (The "Gibson")
    # -------------------------------------------------
    # Instrument hangs diagonally across the torso
    g_angle = 35.0 # Degrees
    g_cx, g_cy = CX + 40, CY_hip + 150
    
    # Acoustic Body (Heavy Bronze/Wood substitute)
    # Deep Elliptical curves of an dreadnought acoustic
    gw, gh = 280, 220
    ax.add_patch(Ellipse((g_cx-10, g_cy-20), gw, gh, angle=g_angle, facecolor=C_IRON, zorder=24)) # Shadow lip
    ax.add_patch(Ellipse((g_cx, g_cy), gw, gh, angle=g_angle, facecolor=C_BRONZE, edgecolor=C_TEXT, lw=8, zorder=25))
    ax.add_patch(Ellipse((g_cx + np.cos(np.radians(g_angle))*80, g_cy + np.sin(np.radians(g_angle))*80), 180, 160, angle=g_angle, facecolor=C_BRONZE, edgecolor=C_TEXT, lw=8, zorder=25))

    # Thermodynamic Exhaust Vent (Sound Hole)
    vent_x = g_cx + np.cos(np.radians(g_angle))*60
    vent_y = g_cy + np.sin(np.radians(g_angle))*60
    ax.add_patch(Circle((vent_x, vent_y), 45, facecolor=C_VOID, edgecolor=C_GOLD, lw=6, zorder=26))

    # The Structural Neck (Fretboard)
    neck_len = 500
    n_base_x = g_cx + np.cos(np.radians(g_angle))*100
    n_base_y = g_cy + np.sin(np.radians(g_angle))*100
    
    n_end_x = vent_x - np.cos(np.radians(g_angle))*neck_len
    n_end_y = vent_y - np.sin(np.radians(g_angle))*neck_len
    
    ax.plot([vent_x, n_end_x], [vent_y, n_end_y], color=C_STEEL, lw=28, zorder=24, solid_capstyle='round')
    ax.plot([vent_x, n_end_x], [vent_y, n_end_y], color=C_IRON, lw=20, zorder=25, solid_capstyle='round') # Fretboard surface
    
    # 5. MAXWELL'S KINEMATICS (The "Devil's Lick")
    # -------------------------------------------------
    # Right Hand (Strumming at the vent)
    # Violent vertical motion over the soundhole
    strum_phase = (tau * beat_freq * 0.5) % 1.0 # 8 strums per loop
    strum_y_off = np.sin(strum_phase * 2 * np.pi) * 80.0
    
    R_sh_x, R_sh_y = CX + 100, CY_neck - 40
    wr_R_x, wr_R_y = vent_x, vent_y + 40 + strum_y_off
    el_R_x, el_R_y = solve_ik(R_sh_x, R_sh_y, wr_R_x, wr_R_y, 160, 160, 1) # Elbow down
    
    ax.plot([R_sh_x, el_R_x, wr_R_x], [R_sh_y, el_R_y, wr_R_y], color=C_VOID, lw=35, zorder=28, solid_capstyle='round', solid_joinstyle='round')
    ax.add_patch(Circle((wr_R_x, wr_R_y), 22, facecolor=C_IRON, edgecolor=C_TEXT, lw=4, zorder=29)) # Fist
    ax.add_patch(Polygon([(wr_R_x, wr_R_y), (wr_R_x-10, wr_R_y-30), (wr_R_x+10, wr_R_y-30)], facecolor=C_GOLD, zorder=30)) # The Pick

    # Left Hand (Fretting on the neck)
    # Blindingly fast mathematical sweeps (Tremolo)
    sweep_phase = (tau * lick_freq * np.pi) 
    fret_drift = np.sin(sweep_phase * 2) * 120.0 + np.sin(sweep_phase * 16) * 15.0 # Macro slide + micro tremolo
    
    # Calculate pos along the neck
    slide_T = 0.5 + (fret_drift / neck_len)
    wr_L_x = vent_x - np.cos(np.radians(g_angle)) * (neck_len * slide_T)
    wr_L_y = vent_y - np.sin(np.radians(g_angle)) * (neck_len * slide_T)
    
    L_sh_x, L_sh_y = CX - 100, CY_neck - 40
    el_L_x, el_L_y = solve_ik(L_sh_x, L_sh_y, wr_L_x, wr_L_y+20, 180, 180, -1) # Elbow flared up/back
    
    ax.plot([L_sh_x, el_L_x, wr_L_x], [L_sh_y, el_L_y, wr_L_y+20], color=C_VOID, lw=35, zorder=22, solid_capstyle='round', solid_joinstyle='round')
    ax.add_patch(Circle((wr_L_x, wr_L_y+20), 22, facecolor=C_IRON, edgecolor=C_TEXT, lw=4, zorder=27))

    # 6. THERMODYNAMIC ACOUSTIC EXHAUST
    # -------------------------------------------------
    # Erupting from the sound vent exactly on the downward strum
    if strum_phase < 0.2:
        # Radial shockwave
        s_rad = (strum_phase / 0.2) * 250.0
        ax.add_patch(Circle((vent_x, vent_y), s_rad, facecolor='none', edgecolor=C_MAGENTA, lw=15 * (1.0 - strum_phase/0.2), zorder=45))
        
    for i in range(MAX_SPARKS):
        age_tau = (tau - p_life[i]) % 1.0
        spawn_time = tau - age_tau
        s_phase = (spawn_time * beat_freq * 0.5) % 1.0
        
        # Tie to the down-strum
        if s_phase < 0.15 and age_tau < 0.2:
            vx = np.cos(p_ang[i]) * p_vel[i]
            vy = np.sin(p_ang[i]) * p_vel[i]
            
            px = vent_x + vx * age_tau
            py = vent_y + vy * age_tau
            
            alpha = np.clip(1.0 - (age_tau / 0.2), 0, 1)
            if alpha > 0.05:
                sz = 20.0 * alpha if p_type[i] == 0 else 10.0 * alpha
                col = c_exhaust if p_type[i] == 0 else c_shock
                ax.scatter(px, py, s=sz, color=np.append(col, alpha*0.8), edgecolors='none', zorder=50)

    # 7. INDUSTRIAL HUD WIDGETS
    # -------------------------------------------------
    ax.add_patch(Rectangle((0, 1840), 1080, 80, facecolor=C_BG, zorder=60))
    txt_top = "LG-312b: AERONAUT NODE // DELTA RESONANCE TENSOR"
    ax.text(40, 1880, txt_top, color=C_IRON, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=61)

    ax.add_patch(Rectangle((0, 0), 1080, 180, facecolor=C_BG, zorder=60))
    ax.add_patch(Rectangle((0, 180), 1080, 4, facecolor=C_IRON, zorder=61))

    sys_str = "CROSSROADS MATRIX: CARTESIAN INTERSECTION CONSTRAINED"
    sys_col = C_MANTIS
    
    if strum_phase < 0.2:
        sys_str = "MAXWELL'S ALGORITHM: KINEMATIC EXHAUST DETECTED"
        sys_col = C_MAGENTA

    ax.text(40, 135, f"SYSTEM STATE: {sys_str}", color=sys_col, fontsize=18, fontname='monospace', weight='bold', va='center', zorder=61)

    txt_tensor = f"ACOUSTIC PACT: THERMODYNAMIC DEMON OVERRIDE"
    ax.text(40, 85, txt_tensor, color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=61)

    txt_legal = "LEGAL MATRIX: BIOLOGICAL SOUL MATHEMATICALLY EXCISIONSED"
    ax.text(40, 45, txt_legal, color=C_IRON, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=61)

    # Tremolo/Frequency HUD
    dial_cx, dial_cy = 960, 90
    ax.add_patch(Circle((dial_cx, dial_cy), 50, facecolor='none', edgecolor=C_IRON, lw=4, zorder=61))
    
    # Rapid needle tracking the fret sweep
    needle_ang = np.radians(180) - (fret_drift / 135.0) * np.pi
    ax.plot([dial_cx, dial_cx + np.cos(needle_ang)*40], [dial_cy, dial_cy + np.sin(needle_ang)*40], color=sys_col, lw=6, zorder=62)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-312b: DELTA RESONANCE TENSOR [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Continuous 10.0s Loop (600 Frames) // Maxwell's Acoustic Override")

    with mp.Pool(processes=cpu_cores) as pool:
        frames = range(TOTAL_FRAMES)
        for finished_frame in pool.imap_unordered(render_frame, frames, chunksize=16):
            pass
    print("Compilation Complete. Faustian Hardware Decoupled.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
