"""
SOVEREIGN CODE: logic_garden_312c_green_velvet.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Kinematic Phase Tensor
SCENE: LG-312c (Harmonic Superposition Tensor / Green Velvet Array)
HOTFIX: Seamless 10s Loop, Emerald Oscillator, Radiant Pure Exhaust
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
OUT_DIR = "frames_312c_green_velvet"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST ENGINEERING PALETTE --------
C_BG        = '#FFFFFF'       # Daylight Protocol Baseline
C_VELVET    = '#0B5345'       # Deep Viridian (Green Velvet Carapace)
C_VOID      = '#0A0A0A'       # Obsidian Radiation Baffles (Sunglasses)
C_IRON      = '#1C2833'       # Raw Carbon / Boots / Grid Lines
C_STEEL     = '#7F8C8D'       # Rigid Hydraulics / Frets / Instrument Neck
C_BRONZE    = '#B87333'       # Acoustic Resonance Chamber
C_EMERALD   = '#2ECC71'       # Quantum Oscillator Core / Sonic Shockwave
C_WHITE     = '#FDFEFE'       # Pure Overload Spallation (Pure as Snow)
C_TEXT      = '#111111'

def hex_to_rgba(h, a=1.0):
    h = h.lstrip('#')
    return [int(h[0:2],16)/255.0, int(h[2:4],16)/255.0, int(h[4:6],16)/255.0, a]

c_exhaust1 = np.array(hex_to_rgba(C_EMERALD)[:3])
c_exhaust2 = np.array(hex_to_rgba(C_WHITE)[:3])

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
np.random.seed(3123)
MAX_SPARKS = 2200
p_life = np.random.uniform(0.0, 1.0, MAX_SPARKS)
p_ang = np.random.uniform(0, 2*np.pi, MAX_SPARKS)
p_vel = np.random.uniform(300.0, 1400.0, MAX_SPARKS)
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
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    CY_GND = 250.0
    CX = 540.0

    # 1. THE RESONANCE SUPERPOSITION GRID
    # -------------------------------------------------
    ax.add_patch(Rectangle((0, 0), 1080, CY_GND, facecolor='#F4F6F6', zorder=1))
    ax.plot([0, 1080], [CY_GND, CY_GND], color=C_STEEL, lw=16, zorder=2)
    
    # Horizon Grid Lines (Pure white track)
    for gx in [-500, -200, 100, 400, 700, 1000, 1300, 1600]:
        ax.plot([gx, CX], [0, CY_GND], color=C_EMERALD, lw=6, alpha=0.2, zorder=2)
    
    ax.plot([0, 1080], [CY_GND - 100, CY_GND - 100], color=C_IRON, lw=20, zorder=3)
    ax.plot([CX, CX], [0, CY_GND], color=C_IRON, lw=30, zorder=4)

    # 2. THE AERONAUT NODE (Green Velvet Power Stance)
    # -------------------------------------------------
    lick_freq = 4.0   
    beat_freq = 16.0  
    
    b_phase = (tau * beat_freq) % 1.0
    y_bounce = np.abs(np.sin(b_phase * np.pi)) * 12.0
    CY_hip = 650.0 - y_bounce
    
    ax_L, ay_L = CX - 180, CY_GND
    ax_R, ay_R = CX + 180, CY_GND
    
    if b_phase < 0.5:
        ay_R = CY_GND + np.sin((b_phase / 0.5) * np.pi) * 30.0

    # Dual-Stage Superposition Shadows (Phantom stages left and right)
    shadow_w = 450 - (y_bounce * 2.0)
    ax.add_patch(Ellipse((CX, CY_GND), shadow_w, 40, facecolor=C_IRON, alpha=0.15, zorder=4))
    # Ghost Instances proving the 2-stage simultaneous presence
    ax.add_patch(Ellipse((CX - 250, CY_GND), shadow_w*0.8, 30, facecolor=C_EMERALD, alpha=0.08, zorder=3))
    ax.add_patch(Ellipse((CX + 250, CY_GND), shadow_w*0.8, 30, facecolor=C_EMERALD, alpha=0.08, zorder=3))

    kx_L, ky_L = solve_ik(CX-60, CY_hip, ax_L, ay_L+20, 240, 250, 1)
    kx_R, ky_R = solve_ik(CX+60, CY_hip, ax_R, ay_R+20, 240, 250, -1)
    
    def draw_leg(hx, hy, kx, ky, fx, fy, zbase, is_fg):
        ax.plot([hx, kx], [hy, ky], color=C_VELVET, lw=70, zorder=zbase, solid_capstyle='round', solid_joinstyle='round')
        ax.plot([kx, fx], [ky, fy], color=C_VELVET, lw=55, zorder=zbase, solid_capstyle='round', solid_joinstyle='round')
        ax.add_patch(Circle((kx, ky), 22, facecolor=C_IRON, edgecolor=C_TEXT, lw=4, zorder=zbase+1))
        # Boot (Stainless white tipped for purity theme)
        ax.add_patch(Polygon([(fx-40, fy+10), (fx+50, fy+10), (fx+50, fy-20), (fx-30, fy-20)], facecolor=C_IRON, edgecolor=C_TEXT, lw=4, zorder=zbase+1, joinstyle='round'))
        if is_fg: ax.plot([fx-30, fx+40], [fy-15, fy-15], color=C_WHITE, lw=8, zorder=zbase+2)

    # Render BG Leg (Right)
    draw_leg(CX+60, CY_hip, kx_R, ky_R, ax_R, ay_R, 10, False)
    
    # 3. VELVET CHASSIS & THE EMERALD OSCILLATOR
    # -------------------------------------------------
    CY_neck = CY_hip + 380
    t_poly = [(CX-90, CY_hip-20), (CX+90, CY_hip-20), (CX+110, CY_neck), (CX-110, CY_neck)]
    ax.add_patch(Polygon(t_poly, facecolor=C_VELVET, edgecolor=C_TEXT, lw=8, zorder=15, joinstyle='round'))

    # The Emerald Chest Core (Quantum Oscillator)
    core_rad = 35.0 + np.sin(b_phase * 2 * np.pi) * 8.0 # Pulses with the beat
    ax.add_patch(Polygon([
        (CX, CY_hip+220+core_rad), (CX+core_rad*0.8, CY_hip+220),
        (CX, CY_hip+220-core_rad), (CX-core_rad*0.8, CY_hip+220)
    ], facecolor=C_EMERALD, edgecolor=C_WHITE, lw=4, zorder=20))
    ax.add_patch(Circle((CX, CY_hip+220), core_rad*2.5, facecolor=C_EMERALD, alpha=0.2, zorder=19))
    ax.add_patch(Circle((CX, CY_hip+220), core_rad*1.5, facecolor=C_WHITE, alpha=0.15, zorder=19))

    # Aeronaut Radome & Obsidian Visors (The Hat & Shades)
    cx_H, cy_H = CX, CY_neck + 80 - y_bounce
    
    # Cranium (Iron Plate)
    ax.add_patch(Circle((cx_H, cy_H), 60, facecolor=C_VELVET, edgecolor=C_TEXT, lw=4, zorder=40))
    
    # Obsidian Radiation Baffles (The "Cool Sunglasses")
    vis_w, vis_h = 90, 35
    ax.add_patch(Rectangle((cx_H-45, cy_H-10), vis_w, vis_h, facecolor=C_VOID, edgecolor=C_IRON, lw=6, zorder=41, joinstyle='round'))
    # Visor reflections (Emerald tint)
    ax.plot([cx_H-35, cx_H-10], [cy_H-5, cy_H+15], color=C_EMERALD, lw=4, zorder=42)
    ax.plot([cx_H+10, cx_H+35], [cy_H-5, cy_H+15], color=C_EMERALD, lw=4, zorder=42)

    # The Massive Radome Brim
    ax.add_patch(Ellipse((cx_H, cy_H+60), 340, 50, facecolor=C_VELVET, edgecolor=C_TEXT, lw=8, zorder=43))
    ax.add_patch(Polygon([(cx_H-80, cy_H+60), (cx_H+80, cy_H+60), (cx_H+50, cy_H+160), (cx_H-50, cy_H+160)], facecolor=C_VELVET, edgecolor=C_TEXT, lw=6, zorder=44, joinstyle='round'))
    ax.plot([cx_H-80, cx_H+80], [cy_H+80, cy_H+80], color=C_EMERALD, lw=12, zorder=45) # Resonance Band

    # Render FG Leg (Left)
    draw_leg(CX-60, CY_hip, kx_L, ky_L, ax_L, ay_L, 20, True)

    # 4. PURE HARMONIC TENSOR (The Synthesizer Deck/Guitar)
    # -------------------------------------------------
    g_angle = 35.0 
    g_cx, g_cy = CX + 40, CY_hip + 150
    
    gw, gh = 280, 220
    ax.add_patch(Ellipse((g_cx-10, g_cy-20), gw, gh, angle=g_angle, facecolor=C_IRON, zorder=24)) 
    # White-Albedo instrument to fulfill "Pure as snow"
    ax.add_patch(Ellipse((g_cx, g_cy), gw, gh, angle=g_angle, facecolor=C_WHITE, edgecolor=C_TEXT, lw=8, zorder=25))
    ax.add_patch(Ellipse((g_cx + np.cos(np.radians(g_angle))*80, g_cy + np.sin(np.radians(g_angle))*80), 180, 160, angle=g_angle, facecolor=C_WHITE, edgecolor=C_TEXT, lw=8, zorder=25))

    # Emerald Sound Hole (Thermodynamic Sync Vent)
    vent_x = g_cx + np.cos(np.radians(g_angle))*60
    vent_y = g_cy + np.sin(np.radians(g_angle))*60
    ax.add_patch(Circle((vent_x, vent_y), 45, facecolor=C_VOID, edgecolor=C_EMERALD, lw=8, zorder=26))

    neck_len = 500
    n_end_x = vent_x - np.cos(np.radians(g_angle))*neck_len
    n_end_y = vent_y - np.sin(np.radians(g_angle))*neck_len
    
    ax.plot([vent_x, n_end_x], [vent_y, n_end_y], color=C_STEEL, lw=28, zorder=24, solid_capstyle='round')
    ax.plot([vent_x, n_end_x], [vent_y, n_end_y], color=C_VELVET, lw=20, zorder=25, solid_capstyle='round') 
    
    # 5. KINEMATIC PURITY SWEEP
    # -------------------------------------------------
    # Right Hand
    strum_phase = (tau * beat_freq * 0.5) % 1.0
    strum_y_off = np.sin(strum_phase * 2 * np.pi) * 80.0
    
    R_sh_x, R_sh_y = CX + 100, CY_neck - 40
    wr_R_x, wr_R_y = vent_x, vent_y + 40 + strum_y_off
    el_R_x, el_R_y = solve_ik(R_sh_x, R_sh_y, wr_R_x, wr_R_y, 160, 160, 1)
    
    ax.plot([R_sh_x, el_R_x, wr_R_x], [R_sh_y, el_R_y, wr_R_y], color=C_VELVET, lw=35, zorder=28, solid_capstyle='round', solid_joinstyle='round')
    ax.add_patch(Circle((wr_R_x, wr_R_y), 22, facecolor=C_IRON, edgecolor=C_TEXT, lw=4, zorder=29)) 

    # Left Hand (High Frequency Electronic Sweep)
    sweep_phase = (tau * lick_freq * 2.0 * np.pi) 
    fret_drift = np.sin(sweep_phase * 2) * 120.0 + np.sin(sweep_phase * 16) * 15.0 
    
    slide_T = 0.5 + (fret_drift / neck_len)
    wr_L_x = vent_x - np.cos(np.radians(g_angle)) * (neck_len * slide_T)
    wr_L_y = vent_y - np.sin(np.radians(g_angle)) * (neck_len * slide_T)
    
    L_sh_x, L_sh_y = CX - 100, CY_neck - 40
    el_L_x, el_L_y = solve_ik(L_sh_x, L_sh_y, wr_L_x, wr_L_y+20, 180, 180, -1) 
    
    ax.plot([L_sh_x, el_L_x, wr_L_x], [L_sh_y, el_L_y, wr_L_y+20], color=C_VELVET, lw=35, zorder=22, solid_capstyle='round', solid_joinstyle='round')
    ax.add_patch(Circle((wr_L_x, wr_L_y+20), 22, facecolor=C_IRON, edgecolor=C_TEXT, lw=4, zorder=27))

    # 6. STERILE ACOUSTIC EXHAUST ("Pure as Snow")
    # -------------------------------------------------
    if strum_phase < 0.2:
        s_rad = (strum_phase / 0.2) * 280.0
        ax.add_patch(Circle((vent_x, vent_y), s_rad, facecolor='none', edgecolor=C_EMERALD, lw=18 * (1.0 - strum_phase/0.2), zorder=45))
        ax.add_patch(Circle((vent_x, vent_y), s_rad*0.8, facecolor='none', edgecolor=C_WHITE, lw=8 * (1.0 - strum_phase/0.2), zorder=45))
        
    for i in range(MAX_SPARKS):
        age_tau = (tau - p_life[i]) % 1.0
        spawn_time = tau - age_tau
        s_phase = (spawn_time * beat_freq * 0.5) % 1.0
        
        if s_phase < 0.15 and age_tau < 0.2:
            vx = np.cos(p_ang[i]) * p_vel[i]
            vy = np.sin(p_ang[i]) * p_vel[i]
            
            px = vent_x + vx * age_tau
            py = vent_y + vy * age_tau
            
            alpha = np.clip(1.0 - (age_tau / 0.2), 0, 1)
            if alpha > 0.05:
                # White and Emerald sparks (Sterilized purity)
                sz = 25.0 * alpha if p_type[i] == 0 else 12.0 * alpha
                col = c_exhaust1 if p_type[i] == 0 else c_exhaust2
                ax.scatter(px, py, s=sz, color=np.append(col, alpha*0.9), edgecolors='none', zorder=50)

    # 7. INDUSTRIAL HUD WIDGETS
    # -------------------------------------------------
    ax.add_patch(Rectangle((0, 1840), 1080, 80, facecolor=C_BG, zorder=60))
    txt_top = "LG-312c: HARMONIC SUPERPOSITION TENSOR // GREEN VELVET"
    ax.text(40, 1880, txt_top, color=C_IRON, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=61)

    ax.add_patch(Rectangle((0, 0), 1080, 180, facecolor=C_BG, zorder=60))
    ax.add_patch(Rectangle((0, 180), 1080, 4, facecolor=C_IRON, zorder=61))

    sys_str = "DUAL-STAGE SUPERPOSITION: 12-HOUR CONTINUOUS O(1) LOCK"
    sys_col = C_EMERALD
    
    if strum_phase < 0.2:
        sys_str = "QUANTUM OSCILLATOR: ACOUSTIC PURITY OVERRIDE"
        sys_col = C_EMERALD

    ax.text(40, 135, f"SYSTEM STATE: {sys_str}", color=sys_col, fontsize=18, fontname='monospace', weight='bold', va='center', zorder=61)

    txt_tensor = f"RADIATION BAFFLES: OBSIDIAN VISORS LATCHED"
    ax.text(40, 85, txt_tensor, color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=61)

    txt_legal = "LEGAL MATRIX: THERMODYNAMICALLY STERILE / MYTHOLOGICAL EXHAUST DELETED"
    ax.text(40, 45, txt_legal, color=C_VELVET, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=61)

    # 12-Hour Electronic Clock HUD
    dial_cx, dial_cy = 960, 90
    ax.add_patch(Circle((dial_cx, dial_cy), 50, facecolor='none', edgecolor=C_IRON, lw=4, zorder=61))
    
    # 12-scale ticks
    for tick in range(12):
        t_ang = np.radians(tick * 30)
        ax.plot([dial_cx + np.cos(t_ang)*40, dial_cx + np.cos(t_ang)*50], 
                [dial_cy + np.sin(t_ang)*40, dial_cy + np.sin(t_ang)*50], color=C_VELVET, lw=2, zorder=62)

    # Sweep Tracker
    needle_ang = np.radians(180) - (fret_drift / 135.0) * np.pi
    ax.plot([dial_cx, dial_cx + np.cos(needle_ang)*45], [dial_cy, dial_cy + np.sin(needle_ang)*45], color=sys_col, lw=6, zorder=62)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-312c: HARMONIC SUPERPOSITION TENSOR [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Continuous 10.0s Loop (600 Frames) // Thermodynamic Purity Lock")

    with mp.Pool(processes=cpu_cores) as pool:
        frames = range(TOTAL_FRAMES)
        for finished_frame in pool.imap_unordered(render_frame, frames, chunksize=16):
            pass
    print("Compilation Complete. Biological Deviance Decoupled.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
