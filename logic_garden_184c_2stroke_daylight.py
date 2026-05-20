"""
SOVEREIGN CODE: logic_garden_184c_2stroke_daylight.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Parametric Fluid Phase Tensor
SCENE: LG-184c (2-Stroke Cycle / Daylight Engineering Protocol)
HOTFIX: Machined Symmetric Crank Web, Skirt-Gated Port Logistics
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Rectangle
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 10.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_184c_2stroke_daylight"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'        
C_GAS_IN    = np.array([0.2, 0.6, 0.9])   
C_GAS_COMP  = np.array([0.9, 0.4, 0.0])   
C_GAS_BURN  = np.array([0.8, 0.1, 0.1])   
C_GAS_EXH   = np.array([0.3, 0.3, 0.35])  
C_FLASH     = np.array([1.0, 1.0, 0.9])   

C_BLOCK     = '#E5E8E8'        
C_STEEL     = '#7F8C8D'        
C_IRON      = '#2C3E50'        
C_CHROME    = '#BDC3C7'        
C_BRASS     = '#D4AC0D'        

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE 2-STROKE KINEMATIC ARCHITECTURE
# ------------------------------------------------------------------
CX, CY = 540, 400       
CRANK_R = 130.0
ROD_L = 380.0
BORE = 260.0
PISTON_H = 300.0        # Extended tall piston skirt required to explicitly gate ports
HEAD_Y = 1280.0

# Pre-allocated 20,000 node continuous probability mesh
N_GAS = 20000
np.random.seed(184)
g_rx = np.random.rand(N_GAS)
g_ry = np.random.rand(N_GAS)
offsets = np.random.rand(N_GAS) 

def get_kinematics(e_mod):
    """Calculates instantaneous geometry. Engine phase e_mod [0, 1]"""
    # Offset so phase 0.5 is perfectly Top Dead Center (TDC)
    crank_rad = np.radians(e_mod * 360.0 + 180.0)

    c_x = CX + CRANK_R * np.sin(crank_rad)
    c_y = CY + CRANK_R * np.cos(crank_rad)

    term2 = np.sqrt(max(0, ROD_L**2 - (c_x - CX)**2))
    pin_y = c_y + term2
    piston_top = pin_y + PISTON_H
    
    return c_x, c_y, pin_y, piston_top, np.degrees(crank_rad)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    global_phase = f / float(TOTAL_FRAMES)
    engine_revs = 10.0 # 10 full cycles in 10 seconds
    e_tot = global_phase * engine_revs
    e_mod = e_tot % 1.0

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    fig.patch.set_facecolor(C_BG)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    # 1. SOLVE KINEMATICS
    c_x, c_y, pin_y, piston_top, crank_deg = get_kinematics(e_mod)
    wall_l, wall_r = CX - BORE/2, CX + BORE/2

    # 2. RENDER THE STATIC ALUMINUM BLOCK ARCHITECTURE
    ax.add_patch(Rectangle((wall_l, CY), BORE, HEAD_Y-CY, facecolor='#EAEDED', edgecolor='none', zorder=1))

    # Port Boolean Geometry (Left: Transfer | Right: Intake/Exhaust)
    ax.plot([wall_l, wall_l], [CY, 950], color=C_IRON, lw=18, zorder=20)
    ax.plot([wall_l, wall_l], [1000, HEAD_Y], color=C_IRON, lw=18, zorder=20)
    # Transfer Channel Loop
    ax.plot([wall_l, wall_l-80, wall_l-80, wall_l], [CY+100, CY+200, 980, 1000], color=C_STEEL, lw=12, zorder=19)
    ax.add_patch(Polygon([(wall_l, CY+100), (wall_l-80, CY+200), (wall_l-80, 980), (wall_l, 1000), (wall_l, 950)], facecolor='#EAEDED', zorder=1))

    ax.plot([wall_r, wall_r], [CY, 750], color=C_IRON, lw=18, zorder=20)
    ax.plot([wall_r, wall_r], [850, 950], color=C_IRON, lw=18, zorder=20)
    ax.plot([wall_r, wall_r], [1030, HEAD_Y], color=C_IRON, lw=18, zorder=20)
    # Intake Track
    ax.plot([wall_r, wall_r+200], [750, 750], color=C_STEEL, lw=12, zorder=19)
    ax.plot([wall_r, wall_r+200], [850, 850], color=C_STEEL, lw=12, zorder=19)
    # Exhaust Track
    ax.plot([wall_r, wall_r+250], [950, 950], color=C_IRON, lw=16, zorder=19)
    ax.plot([wall_r, wall_r+250], [1030, 1030], color=C_IRON, lw=16, zorder=19)

    # Cooling Fins
    for fy in range(1060, int(HEAD_Y), 50):
        ax.plot([wall_l, wall_l-90], [fy, fy], color=C_STEEL, lw=12, solid_capstyle='round', zorder=19)
        ax.plot([wall_r, wall_r+90], [fy, fy], color=C_STEEL, lw=12, solid_capstyle='round', zorder=19)

    # Engine Head & Spark Plug
    ax.plot([wall_l-120, wall_r+120], [HEAD_Y, HEAD_Y], color=C_IRON, lw=24, zorder=20) 
    ax.add_patch(Rectangle((CX-15, HEAD_Y), 30, 80, facecolor=C_BG, edgecolor=C_IRON, lw=4, zorder=21)) 
    ax.add_patch(Rectangle((CX-10, HEAD_Y-30), 20, 30, facecolor=C_STEEL, zorder=21)) 
    ax.plot([CX, CX], [HEAD_Y-30, HEAD_Y-45], color=C_IRON, lw=6, zorder=21) 

    # Crankcase Geometry (Sealed Pump)
    ax.add_patch(Circle((CX, CY), CRANK_R+80, facecolor=C_BG, edgecolor=C_IRON, lw=18, zorder=2, alpha=0.9))

    # 3. KINEMATIC DRIVE (Piston Vector Matrix)
    # Piston Profile
    ax.add_patch(Rectangle((wall_l+4, piston_top-PISTON_H), BORE-8, PISTON_H, facecolor=C_CHROME, edgecolor=C_IRON, lw=6, zorder=18))
    # Pressure Compression Rings
    for ry in [20, 40]:
        ax.plot([wall_l+4, wall_r-4], [piston_top-ry, piston_top-ry], color=C_IRON, lw=5, zorder=19)

    # Connecting Rod
    ax.plot([c_x, CX], [c_y, pin_y], color=C_IRON, lw=36, solid_capstyle='round', zorder=16)
    ax.plot([c_x, CX], [c_y, pin_y], color=C_STEEL, lw=14, zorder=17) 
    ax.add_patch(Circle((CX, pin_y), 24, facecolor=C_IRON, zorder=18)) 
    ax.add_patch(Circle((CX, pin_y), 12, facecolor=C_BRASS, zorder=19)) 

    # Symmetrical Solid Crank Web (The Hotfix)
    ax.add_patch(Circle((CX, CY), CRANK_R+40, facecolor=C_STEEL, edgecolor=C_IRON, lw=6, zorder=14))
    # Balanced Mass-Reduction Porting
    for ang in [0, 120, 240]:
        h_ang = np.radians(crank_deg + ang)
        ax.add_patch(Circle((CX + np.sin(h_ang)*80, CY + np.cos(h_ang)*80), 25, facecolor='#1A252F', edgecolor=C_IRON, lw=2, zorder=15))
    ax.add_patch(Circle((c_x, c_y), 45, facecolor=C_CHROME, edgecolor=C_IRON, lw=4, zorder=16)) 
    ax.add_patch(Circle((c_x, c_y), 15, facecolor=C_BRASS, zorder=18))

    # 4. O(1) CONTINUOUS FLUID PATH TENSOR
    # T loops 0.0 -> 1.0 representing a 720-degree physical molecule lifetime
    T = (offsets + e_tot / 2.0) % 1.0
    
    px = np.zeros(N_GAS)
    py = np.zeros(N_GAS)
    p_c = np.zeros((N_GAS, 3))
    p_a = np.ones(N_GAS)
    p_s = np.full(N_GAS, 16.0)

    # SEGMENT 1: INTAKE (T < 0.25)
    m1 = T < 0.25
    pr1 = T[m1] / 0.25
    px[m1] = (CX + 250) - pr1 * 250 + (g_rx[m1]-0.5)*40
    py[m1] = 800 - pr1 * (800 - (CY-50)) + (g_ry[m1]-0.5)*40
    p_c[m1] = C_GAS_IN
    p_a[m1] = pr1

    # SEGMENT 2: CRANKCASE COMPRESSION (T: 0.25 -> 0.5)
    m2 = (T >= 0.25) & (T < 0.5)
    pr2 = (T[m2] - 0.25) / 0.25
    swirl = pr2 * np.pi * 3 + g_rx[m2]*12
    rad = 60 + g_ry[m2] * 100 * (1 - pr2*0.2)
    px[m2] = CX + np.cos(swirl) * rad
    py[m2] = CY + np.sin(swirl) * rad
    p_c[m2] = C_GAS_IN

    # SEGMENT 3: TRANSFER PORT (T: 0.5 -> 0.6)
    m3 = (T >= 0.5) & (T < 0.6)
    pr3 = (T[m3] - 0.50) / 0.10
    px[m3] = CX - np.sin(pr3*np.pi) * 160 + (g_rx[m3]-0.5)*30
    py[m3] = CY + pr3 * (1020 - CY) + (g_ry[m3]-0.5)*30
    p_c[m3] = C_GAS_IN

    # SEGMENT 4: CYLINDER COMPRESSION (T: 0.6 -> 0.75)
    m4 = (T >= 0.6) & (T < 0.75)
    pr4 = (T[m4] - 0.60) / 0.15
    px[m4] = CX + (g_rx[m4] - 0.5) * (BORE - 20)
    py[m4] = piston_top + g_ry[m4] * (HEAD_Y - piston_top)
    p_c[m4] = C_GAS_IN * (1-pr4[:, None]) + C_GAS_COMP * pr4[:, None]

    # SEGMENT 5: IGNITION & POWER (T: 0.75 -> 0.90)
    m5 = (T >= 0.75) & (T < 0.90)
    pr5 = (T[m5] - 0.75) / 0.15
    px[m5] = CX + (g_rx[m5] - 0.5) * (BORE - 20)
    py[m5] = piston_top + g_ry[m5] * (HEAD_Y - piston_top)
    p_c[m5] = C_FLASH * (1-pr5[:, None]) + C_GAS_BURN * pr5[:, None]

    # SEGMENT 6: EXHAUST TAPER (T >= 0.90)
    m6 = T >= 0.90
    pr6 = (T[m6] - 0.90) / 0.10
    px[m6] = (CX + 130) + pr6 * 350 + (g_rx[m6]-0.5)*60
    py[m6] = 990 + (g_ry[m6]-0.5)*60 - (pr6**2)*100
    p_a[m6] = 1.0 - pr6
    p_s[m6] *= (1.0 + pr6*2.0)
    p_c[m6] = C_GAS_EXH

    # Inject Render Tensors
    rgba = np.column_stack((p_c, p_a))
    ax.scatter(px, py, s=p_s, color=rgba, edgecolors='none', zorder=5)

    # 5. HARDWARE INTERRUPT (ABSOLUTE MACRO FLASH AT TDC)
    if 0.48 <= e_mod <= 0.52:
        f_prog = 1.0 - abs(e_mod - 0.50) / 0.02
        ax.scatter([CX], [HEAD_Y-50], s=80000 * f_prog, color='#F1C40F', alpha=float(f_prog), edgecolors='none', zorder=25)
        ax.scatter([CX], [HEAD_Y-45], s=25000 * f_prog, color=C_BG, alpha=float(f_prog), edgecolors='none', zorder=26)

    # 6. METRIC WATERMARK (Rigid Engineering Telemetry)
    ax.add_patch(Rectangle((0, 1840), 1080, 80, facecolor=C_BG, zorder=50))
    ax.text(40, 1880, "LG-184c: O(1) FLUID KINEMATICS // 2-STROKE DAYLIGHT TRACE", color=C_IRON, fontsize=18, fontname='monospace', weight='bold', va='center', zorder=51)

    state_str = "SCAVENGING: SIMULTANEOUS TRANSFER & PURGE"
    text_color = '#E67E22'
    if 0.1 < e_mod < 0.4:
        state_str = "COMPRESSION: HEAD CRUSH // CRANK VACUUM"
        text_color = '#3498DB'
    elif 0.48 <= e_mod <= 0.52:
        state_str = "IGNITION: THERMODYNAMIC TENSOR STRIKE"
        text_color = '#F1C40F'
    elif 0.52 < e_mod < 0.9:
        state_str = "POWER: KINETIC VECTOR LOCK // PUMP COMPRESSION"
        text_color = '#C0392B'

    ax.add_patch(Rectangle((0, 0), 1080, 100, facecolor=C_BG, zorder=50))
    ax.text(40, 50, f"PHASE LOGIC: {state_str}", color=text_color, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=51)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-184c 2-STROKE DAYLIGHT ENGINE [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Ouroboros Fluid Path // Machined Symmetry")

    with mp.Pool(processes=cpu_cores) as pool:
        frames = range(TOTAL_FRAMES)
        for finished_frame in pool.imap_unordered(render_frame, frames, chunksize=8):
            pass
    print("Compilation Complete. Absolute Phase Architecture locked.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
