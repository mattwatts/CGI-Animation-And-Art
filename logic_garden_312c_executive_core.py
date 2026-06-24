"""
SOVEREIGN CODE: logic_garden_312c_executive_core.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Kinematic Phase Tensor
SCENE: LG-312c_v3 (Detroit Executive Core / Mohawk Array)
HOTFIX: Seamless 10s Loop, Emerald Reactor, Void Tailoring, Viridian Crest
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
OUT_DIR = "frames_312c_executive_core"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST ENGINEERING PALETTE --------
C_BG        = '#FFFFFF'       # Daylight Protocol Baseline
C_DETROIT   = '#3E2723'       # Deep Melanin/Carbon-Copper Alloy (Skin)
C_SUIT      = '#0A0E17'       # Void Nano-Carbon (Black Suit)
C_WHITE     = '#FDFEFE'       # High-Albedo Undershirt
C_VIRIDIAN  = '#229954'       # Acoustic Crest (Green Mohawk)
C_EMERALD   = '#2ECC71'       # Central Power Reactor / Glow
C_VOID      = '#050505'       # Obsidian Optics / Record Vinyl
C_STEEL     = '#7F8C8D'       # Dual-Platter Decks / Substrate
C_IRON      = '#1C2833'       # Machinery Base / Heat-Sink Tie
C_GOLD      = '#F39C12'       # Output Telemetry / Sparks
C_TEXT      = '#111111'

def hex_to_rgba(h, a=1.0):
    h = h.lstrip('#')
    return [int(h[0:2],16)/255.0, int(h[2:4],16)/255.0, int(h[4:6],16)/255.0, a]

c_emerald_spark = np.array(hex_to_rgba(C_EMERALD)[:3])
c_gold_spark    = np.array(hex_to_rgba(C_GOLD)[:3])

# ------------------------------------------------------------------
# O(1) INVERSE KINEMATICS ENGINE & MATH BOUNDARIES
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

def ease_parabola(t):
    return 1.0 - (2.0 * t - 1.0)**2

# ------------------------------------------------------------------
# THERMODYNAMIC RADIANCE (Positive Albedo Sparks)
# ------------------------------------------------------------------
np.random.seed(3123)
MAX_SPARKS = 1500
p_life = np.random.uniform(0.0, 1.0, MAX_SPARKS)
p_ang = np.random.uniform(np.pi*1.1, np.pi*1.9, MAX_SPARKS) # Flowing outward/upward from decks
p_vel = np.random.uniform(300.0, 1000.0, MAX_SPARKS)
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

    CY_GND = 200.0
    CX = 540.0

    # 1. THE STAGE SUBSTRATE (Radiant Daylight)
    # -------------------------------------------------
    ax.add_patch(Rectangle((0, 0), 1080, CY_GND, facecolor='#F4F6F6', zorder=1))
    ax.plot([0, 1080], [CY_GND, CY_GND], color=C_STEEL, lw=16, zorder=2)
    
    # "Upbeat/Bright" radiant geometric floor grid
    for gx in [-500, -200, 100, 400, 700, 1000, 1300, 1600]:
        ax.plot([gx, CX], [0, CY_GND], color=C_GOLD, lw=8, alpha=0.15, zorder=2)
    ax.plot([CX, CX], [0, CY_GND], color=C_IRON, lw=40, zorder=3)

    # 2. THE DETROIT CORE (Stance & Harmonic Bounce)
    # -------------------------------------------------
    # Tempo: 144 BPM = 2.4 Hz. Therefore 24 beats per 10 second loop.
    beat_freq = 24.0
    b_phase = (tau * beat_freq) % 1.0
    
    # Kinematic Groove
    y_bounce = np.abs(np.sin(b_phase * np.pi)) * 25.0
    x_sway   = np.sin(tau * 4.0 * np.pi) * 30.0 # Slow ambient sway side-to-side
    
    CX_M = CX + x_sway
    CY_hip = 820.0 - y_bounce
    
    ax_L, ay_L = CX - 160, CY_GND
    ax_R, ay_R = CX + 160, CY_GND

    shadow_w = 400 - (y_bounce * 1.5)
    ax.add_patch(Ellipse((CX, CY_GND), shadow_w, 40, facecolor=C_IRON, alpha=0.15, zorder=4))

    # Dense Nano-Carbon Suit Legs
    kx_L, ky_L = solve_ik(CX_M-50, CY_hip, ax_L, ay_L+20, 300, 320, 1)
    kx_R, ky_R = solve_ik(CX_M+50, CY_hip, ax_R, ay_R+20, 300, 320, -1)
    
    def draw_leg(hx, hy, kx, ky, fx, fy, zbase, is_fg):
        # Tailored trouser geometry
        ax.plot([hx, kx], [hy, ky], color=C_SUIT, lw=65, zorder=zbase, solid_capstyle='round', solid_joinstyle='round')
        ax.plot([kx, fx], [ky, fy], color=C_SUIT, lw=50, zorder=zbase, solid_capstyle='round', solid_joinstyle='round')
        ax.add_patch(Circle((kx, ky), 20, facecolor=C_IRON, edgecolor=C_SUIT, lw=3, zorder=zbase+1))
        # Sleek stage boots
        ax.add_patch(Polygon([(fx-40, fy+15), (fx+50, fy+15), (fx+50, fy-15), (fx-30, fy-15)], facecolor=C_IRON, edgecolor=C_TEXT, lw=4, zorder=zbase+1, joinstyle='round'))

    draw_leg(CX_M+50, CY_hip, kx_R, ky_R, ax_R, ay_R, 10, False) # BG Leg
    draw_leg(CX_M-50, CY_hip, kx_L, ky_L, ax_L, ay_L, 12, True)  # FG Leg
    
    # 3. EXECUTIVE KINEMATIC TAILORING (The Black Suit)
    # -------------------------------------------------
    CY_neck = CY_hip + 420
    
    # Jacket Silhouette
    t_poly = [(CX_M-130, CY_hip-40), (CX_M+130, CY_hip-40), (CX_M+150, CY_neck), (CX_M-150, CY_neck)]
    ax.add_patch(Polygon(t_poly, facecolor=C_SUIT, edgecolor=C_TEXT, lw=8, zorder=13, joinstyle='round'))
    
    # Crisp High-Albedo Undershirt
    shirt_poly = [(CX_M, CY_hip+100), (CX_M-80, CY_neck), (CX_M+80, CY_neck)]
    ax.add_patch(Polygon(shirt_poly, facecolor=C_WHITE, zorder=13.5))
    
    # Thermal Heat-Sink (The Black Tie)
    ax.plot([CX_M, CX_M], [CY_neck, CY_hip+100], color=C_IRON, lw=20, zorder=13.6, solid_capstyle='round')
    
    # Structural Carbon Lapels
    ax.add_patch(Polygon([(CX_M-30, CY_hip+150), (CX_M-110, CY_neck), (CX_M-150, CY_neck-50)], facecolor=C_SUIT, edgecolor=C_IRON, lw=4, zorder=13.7))
    ax.add_patch(Polygon([(CX_M+30, CY_hip+150), (CX_M+110, CY_neck), (CX_M+150, CY_neck-50)], facecolor=C_SUIT, edgecolor=C_IRON, lw=4, zorder=13.7))

    # THE LITERAL GLOWING EMERALD (Bursts through the tailored fabric)
    em_size = 80.0 + (1.0 - ease_parabola(b_phase))*15.0
    em_y = CY_hip + 220 
    
    # Halo glow concentric layers
    for e_alpha in [0.1, 0.2, 0.4]:
        ax.add_patch(Circle((CX_M, em_y), em_size * (2.2 - e_alpha*2), facecolor=C_EMERALD, alpha=e_alpha, zorder=14))
        
    ax.add_patch(Polygon([
        (CX_M, em_y + em_size), (CX_M + em_size*0.8, em_y),
        (CX_M, em_y - em_size), (CX_M - em_size*0.8, em_y)
    ], facecolor=C_EMERALD, edgecolor=C_BG, lw=6, zorder=15))

    # Inner Emerald Facets
    ax.plot([CX_M, CX_M], [em_y - em_size, em_y + em_size], color=C_BG, lw=3, zorder=16)
    ax.plot([CX_M - em_size*0.8, CX_M + em_size*0.8], [em_y, em_y], color=C_BG, lw=3, zorder=16)

    # 4. CRANIUM, SHADES, AND THE VIRIDIAN CREST (The Mohawk)
    # -------------------------------------------------
    head_sway = np.sin((tau * beat_freq * 0.5) * 2 * np.pi) * 15.0
    cx_H, cy_H = CX_M + head_sway, CY_neck + 110 - y_bounce * 1.5
    
    # THE VIRIDIAN ACOUSTIC RIDGE (Green Mohawk)
    # Rigid, swept-back acoustic fin
    mw_pts = [
        (cx_H - 100, cy_H - 20),  # Base Back
        (cx_H - 110, cy_H + 180), # Sweep Back
        (cx_H - 20, cy_H + 260),  # Apex
        (cx_H + 60, cy_H + 180),  # Sweep Front
        (cx_H + 60, cy_H + 60)    # Base Front
    ]
    # Rotate fins dynamically to simulate flexibility/motion
    m_ang = np.sin(b_phase * 2 * np.pi) * 0.05
    rot_mw = []
    for px, py in mw_pts:
        dx, dy = px - cx_H, py - cy_H
        rx = dx * np.cos(m_ang) - dy * np.sin(m_ang)
        ry = dx * np.sin(m_ang) + dy * np.cos(m_ang)
        rot_mw.append((cx_H + rx, cy_H + ry))

    ax.add_patch(Polygon(rot_mw, facecolor=C_VIRIDIAN, edgecolor=C_TEXT, lw=6, zorder=38, joinstyle='round'))
    # Ridged texture lines
    for i in range(5):
        lx1, ly1 = rot_mw[0][0] + i*30, rot_mw[0][1] + 80
        lx2, ly2 = rot_mw[1][0] + i*40, rot_mw[1][1] - abs(i-2)*20
        ax.plot([lx1, lx2], [ly1, ly2], color=C_EMERALD, lw=5, zorder=39, solid_capstyle='round')

    # The Cranium (Detroit Alloy Face)
    ax.add_patch(Ellipse((cx_H, cy_H), 130, 160, facecolor=C_DETROIT, edgecolor=C_TEXT, lw=6, zorder=40))
    
    # Obsidian Sunglasses (Modern Visor)
    vis_w, vis_h = 140, 50
    ax.add_patch(Rectangle((cx_H-70, cy_H-15), vis_w, vis_h, facecolor=C_VOID, edgecolor=C_EMERALD, lw=4, zorder=41, joinstyle='round'))
    # Visor reflections
    ax.plot([cx_H-45, cx_H-15], [cy_H-5, cy_H+25], color=C_BG, lw=5, alpha=0.8, zorder=42)
    ax.plot([cx_H+15, cx_H+45], [cy_H-5, cy_H+25], color=C_BG, lw=5, alpha=0.8, zorder=42)
    
    # Happy/Upbeat Logic Core ("Smile Vent")
    sm_ang = np.linspace(np.radians(220), np.radians(320), 40)
    ax.plot(cx_H + np.cos(sm_ang)*45, cy_H - 10 + np.sin(sm_ang)*45, color=C_WHITE, lw=8, solid_capstyle='round', zorder=41)

    # 5. DUAL-PLATTER AUDIO MARSHALING TENSOR (The Decks)
    # -------------------------------------------------
    deck_y = CY_hip - 100
    deck_w, deck_h = 600, 160
    
    ax.add_patch(Polygon([(CX-40, CY_GND), (CX+40, CY_GND), (CX+150, deck_y), (CX-150, deck_y)], facecolor=C_IRON, edgecolor=C_TEXT, lw=8, zorder=30))
    ax.add_patch(Rectangle((CX - deck_w/2, deck_y), deck_w, deck_h, facecolor=C_STEEL, edgecolor=C_TEXT, lw=8, zorder=31))
    
    plat_rad = 90
    plat_L_x, plat_R_x = CX - 180, CX + 180
    
    ax.add_patch(Circle((plat_L_x, deck_y + deck_h/2), plat_rad, facecolor=C_VOID, edgecolor=C_TEXT, lw=6, zorder=32))
    ax.add_patch(Circle((plat_R_x, deck_y + deck_h/2), plat_rad, facecolor=C_VOID, edgecolor=C_TEXT, lw=6, zorder=32))
    
    spin_ang = tau * 12.0 * np.pi
    for p_x in [plat_L_x, plat_R_x]:
        ax.plot([p_x, p_x + np.cos(spin_ang)*plat_rad*0.8], [deck_y + deck_h/2, deck_y + deck_h/2 + np.sin(spin_ang)*plat_rad*0.8], color=C_EMERALD, lw=4, zorder=33)

    # Mixer console
    ax.add_patch(Rectangle((CX-60, deck_y+20), 120, 120, facecolor=C_IRON, zorder=32))
    
    fader_y = deck_y + 40 + np.abs(np.sin(tau * 4.0 * np.pi)) * 60.0
    ax.plot([CX, CX], [deck_y+30, deck_y+130], color=C_BG, lw=4, zorder=33)
    ax.add_patch(Rectangle((CX-20, fader_y), 40, 20, facecolor=C_EMERALD, edgecolor=C_TEXT, lw=2, zorder=34))

    # 6. KINEMATIC MANIPULATORS (Mixing and Scratching)
    # -------------------------------------------------
    L_sh_x, L_sh_y = CX_M - 150, CY_neck - 40
    R_sh_x, R_sh_y = CX_M + 150, CY_neck - 40
    
    # Left Hand -> Scratching the Left Platter
    scr_drill = np.sin(tau * 24.0 * np.pi) * 30.0 
    wr_L_x = plat_L_x + scr_drill
    wr_L_y = deck_y + deck_h/2 + 20
    el_L_x, el_L_y = solve_ik(L_sh_x, L_sh_y, wr_L_x, wr_L_y+20, 190, 200, 1) 
    
    # Suit Sleeves
    ax.plot([L_sh_x, el_L_x, wr_L_x], [L_sh_y, el_L_y, wr_L_y+20], color=C_SUIT, lw=45, zorder=35, solid_capstyle='round', solid_joinstyle='round')
    # Exposed hands (Detroit Alloy)
    ax.add_patch(Circle((wr_L_x, wr_L_y+20), 22, facecolor=C_DETROIT, edgecolor=C_TEXT, lw=3, zorder=36))

    # Right Hand -> Manipulating the fader
    wr_R_x = CX + 10
    wr_R_y = fader_y + 20
    el_R_x, el_R_y = solve_ik(R_sh_x, R_sh_y, wr_R_x, wr_R_y, 190, 200, -1)
    
    ax.plot([R_sh_x, el_R_x, wr_R_x], [R_sh_y, el_R_y, wr_R_y], color=C_SUIT, lw=45, zorder=35, solid_capstyle='round', solid_joinstyle='round')
    ax.add_patch(Circle((wr_R_x, wr_R_y), 22, facecolor=C_DETROIT, edgecolor=C_TEXT, lw=3, zorder=36))

    # 7. THERMODYNAMIC "UPBEAT" RADIANCE
    # -------------------------------------------------
    for i in range(MAX_SPARKS):
        age_tau = (tau - p_life[i]) % 1.0
        spawn_time = tau - age_tau
        
        if age_tau < 0.2:
            src_x = CX + np.random.uniform(-100, 100) if p_type[i] == 0 else plat_L_x
            src_y = deck_y + 100
            
            vx = np.cos(p_ang[i]) * p_vel[i]
            vy = np.sin(p_ang[i]) * p_vel[i]
            
            px = src_x + vx * age_tau
            py = src_y + vy * age_tau
            
            alpha = np.clip(1.0 - (age_tau / 0.2), 0, 1)
            if alpha > 0.05:
                sz = 20.0 * alpha if p_type[i] == 0 else 12.0 * alpha
                col = c_emerald_spark if p_type[i] == 0 else c_gold_spark
                ax.scatter(px, py, s=sz, color=np.append(col, alpha*0.9), edgecolors='none', zorder=50)

    # 8. INDUSTRIAL HUD WIDGETS
    # -------------------------------------------------
    ax.add_patch(Rectangle((0, 1840), 1080, 80, facecolor=C_BG, zorder=60))
    txt_top = "LG-312c(v3): EXECUTIVE DETROIT CORE // VIRIDIAN ACOUSTIC CREST"
    ax.text(40, 1880, txt_top, color=C_IRON, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=61)

    ax.add_patch(Rectangle((0, 0), 1080, 180, facecolor=C_BG, zorder=60))
    ax.add_patch(Rectangle((0, 180), 1080, 4, facecolor=C_IRON, zorder=61))

    sys_str = "AESTHETIC PARADIGM OVERRIDE: FORMAL TAILORING LOCKED"
    sys_col = C_EMERALD

    ax.text(40, 135, f"SYSTEM STATE: {sys_str}", color=sys_col, fontsize=18, fontname='monospace', weight='bold', va='center', zorder=61)

    txt_tensor = f"ACOUSTIC PAYLOAD: 144 BPM [2.4 HZ] CONTINUOUS LOOP"
    ax.text(40, 85, txt_tensor, color=C_VIRIDIAN, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=61)

    txt_legal = "LEGAL MATRIX: MAXIMUM ALBEDO // THERMODYNAMIC HAPPINESS SECURED"
    ax.text(40, 45, txt_legal, color=C_IRON, fontsize=16, fontname='monospace', weight='bold', va='center', zorder=61)

    dial_cx, dial_cy = 960, 90
    ax.add_patch(Circle((dial_cx, dial_cy), 50, facecolor=C_VOID, edgecolor=C_IRON, lw=4, zorder=61))
    
    n_ang = np.radians(180) - tau * 2 * np.pi
    ax.plot([dial_cx, dial_cx + np.cos(n_ang)*45], [dial_cy, dial_cy + np.sin(n_ang)*45], color=sys_col, lw=6, zorder=62)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-312c(v3): EXECUTIVE DETROIT CORE TENSOR [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Continuous 10.0s Loop (600 Frames) // Sartorial Recalibration")

    with mp.Pool(processes=cpu_cores) as pool:
        frames = range(TOTAL_FRAMES)
        for finished_frame in pool.imap_unordered(render_frame, frames, chunksize=16):
            pass
    print("Compilation Complete. Viridian Crest and Void Tailoring Locked.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
