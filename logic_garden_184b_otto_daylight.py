"""
SOVEREIGN CODE: logic_garden_184b_otto_daylight.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Parametric Fluid Phase Tensor
SCENE: LG-184b (Otto Cycle / Daylight Engineering Protocol)
HOTFIX: IEEE-754 Floating-Point Precision Clamp on Optic Alpha
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Rectangle, Wedge
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 10.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_184b_otto_daylight"
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
# SYSTEM TOPOLOGY: THE KINEMATIC DOHC ARCHITECTURE
# ------------------------------------------------------------------
CX, CY = 540, 480      
CRANK_R = 150.0
ROD_L = 400.0
BORE = 280.0
PISTON_H = 140.0
HEAD_Y = 1200.0        

# ------------------------------------------------------------------
# O(1) SEAMLESS THERMODYNAMIC PHASE TENSOR
# ------------------------------------------------------------------
N_GAS = 20000
np.random.seed(184)
g_rx = np.random.uniform(-1, 1, N_GAS)
g_ry = np.random.uniform(0, 1, N_GAS)

stamp_in = np.random.uniform(0.01, 0.24, N_GAS)   
stamp_out = np.random.uniform(0.76, 0.99, N_GAS)  

def get_kinematics(phase):
    crank_deg = phase * 720.0
    crank_rad = np.radians(crank_deg)
    
    c_x = CX + CRANK_R * np.sin(crank_rad)
    c_y = CY + CRANK_R * np.cos(crank_rad)
    
    term2 = np.sqrt(max(0, ROD_L**2 - (c_x - CX)**2))
    pin_y = c_y + term2
    piston_top = pin_y + PISTON_H
    
    v_in = np.clip(np.sin((phase / 0.25) * np.pi), 0, 1) * 60.0 if 0.0 < phase < 0.25 else 0.0
    v_ex = np.clip(np.sin(((phase - 0.75) / 0.25) * np.pi), 0, 1) * 60.0 if 0.75 < phase < 1.0 else 0.0
    
    return c_x, c_y, pin_y, piston_top, v_in, v_ex

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    phase = f / float(TOTAL_FRAMES)  
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    fig.patch.set_facecolor(C_BG)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    # 1. SOLVE KINEMATICS
    c_x, c_y, pin_y, piston_top, v_in, v_ex = get_kinematics(phase)
    
    # 2. RENDER THE STATIC ALUMINUM BLOCK
    wall_l, wall_r = CX - BORE/2, CX + BORE/2
    ax.add_patch(Rectangle((wall_l, CY), BORE, HEAD_Y-CY, facecolor='#EAEDED', edgecolor='none', zorder=1))
    
    ax.plot([wall_l, wall_l], [CY, HEAD_Y], color=C_IRON, lw=18, zorder=20)
    ax.plot([wall_r, wall_r], [CY, HEAD_Y], color=C_IRON, lw=18, zorder=20)
    
    for fy in range(int(CY)+100, int(HEAD_Y), 60):
        ax.plot([wall_l, wall_l-80], [fy, fy], color=C_STEEL, lw=12, solid_capstyle='round', zorder=19)
        ax.plot([wall_r, wall_r+80], [fy, fy], color=C_STEEL, lw=12, solid_capstyle='round', zorder=19)

    ax.plot([wall_l-150, CX-90], [HEAD_Y, HEAD_Y], color=C_IRON, lw=24, zorder=20)   
    ax.plot([CX+90, wall_r+150], [HEAD_Y, HEAD_Y], color=C_IRON, lw=24, zorder=20)   
    ax.plot([CX-30, CX+30], [HEAD_Y, HEAD_Y], color=C_IRON, lw=24, zorder=20)        

    ax.plot([wall_l, CX-100], [HEAD_Y+250, HEAD_Y], color=C_STEEL, lw=12, zorder=19)
    ax.plot([wall_r, CX+100], [HEAD_Y+250, HEAD_Y], color=C_STEEL, lw=12, zorder=19)

    # 3. TITANIUM VALVETRAIN (DYNAMIC DOHC LIFT)
    in_v_y = HEAD_Y - v_in
    ex_v_y = HEAD_Y - v_ex
    ax.plot([CX-60, CX-60], [HEAD_Y+150, in_v_y], color=C_CHROME, lw=12, solid_capstyle='round', zorder=15)
    ax.add_patch(Polygon([(CX-110, in_v_y-5), (CX-10, in_v_y-5), (CX-60, in_v_y+25)], facecolor=C_CHROME, edgecolor=C_IRON, lw=3, zorder=15))
    ax.plot([CX+60, CX+60], [HEAD_Y+150, ex_v_y], color=C_CHROME, lw=12, solid_capstyle='round', zorder=15)
    ax.add_patch(Polygon([(CX+10, ex_v_y-5), (CX+110, ex_v_y-5), (CX+60, ex_v_y+25)], facecolor=C_CHROME, edgecolor=C_IRON, lw=3, zorder=15))

    ax.add_patch(Rectangle((CX-15, HEAD_Y), 30, 80, facecolor=C_BG, edgecolor=C_IRON, lw=4, zorder=21)) 
    ax.add_patch(Rectangle((CX-10, HEAD_Y-30), 20, 30, facecolor=C_STEEL, zorder=21)) 
    ax.plot([CX, CX], [HEAD_Y-30, HEAD_Y-45], color=C_IRON, lw=6, zorder=21) 

    # 4. KINEMATIC DRIVE
    ax.add_patch(Rectangle((wall_l+4, pin_y-40), BORE-8, PISTON_H+40, facecolor=C_CHROME, edgecolor=C_IRON, lw=6, zorder=18))
    for ry in [20, 40, 60]:
        ax.plot([wall_l+4, wall_r-4], [piston_top-ry, piston_top-ry], color=C_IRON, lw=5, zorder=19)

    ax.plot([c_x, CX], [c_y, pin_y], color=C_IRON, lw=36, solid_capstyle='round', zorder=16)
    ax.plot([c_x, CX], [c_y, pin_y], color=C_STEEL, lw=14, zorder=17) 
    ax.add_patch(Circle((CX, pin_y), 24, facecolor=C_IRON, zorder=18)) 
    ax.add_patch(Circle((CX, pin_y), 12, facecolor=C_BRASS, zorder=19)) 

    ax.add_patch(Circle((CX, CY), CRANK_R+40, facecolor='#1A252F', edgecolor=C_IRON, lw=4, zorder=14))
    ax.add_patch(Wedge((CX, CY), CRANK_R+80, (phase*720)+90, (phase*720)+270, facecolor=C_IRON, zorder=14))
    ax.add_patch(Circle((CX, CY), 30, facecolor=C_CHROME, zorder=15)) 
    ax.add_patch(Circle((c_x, c_y), 35, facecolor=C_CHROME, zorder=17)) 
    ax.add_patch(Circle((c_x, c_y), 15, facecolor=C_BRASS, zorder=18))

    # 5. O(1) FLUID TENSOR MATHEMATICS
    ch_x = CX + g_rx * (BORE/2 - 10)
    ch_y = piston_top + 10 + g_ry * (HEAD_Y - piston_top - 20)
    
    px = np.copy(ch_x)
    py = np.copy(ch_y)
    p_alpha = np.ones(N_GAS) * 0.9
    p_size = np.ones(N_GAS) * 16.0
    c_tensor = np.zeros((N_GAS, 3))

    if phase < 0.25:
        base_col = C_GAS_IN
    elif phase < 0.5:
        prog = (phase - 0.25) / 0.25
        base_col = C_GAS_IN * (1-prog) + C_GAS_COMP * prog
    elif phase < 0.75:
        prog = (phase - 0.5) / 0.25
        base_col = C_GAS_BURN * (1-prog) + C_GAS_EXH * prog
    else:
        base_col = C_GAS_EXH

    c_tensor[:] = base_col

    # Hardware Interrupt (Clamp added to prevent Floating Point Crash)
    if 0.49 <= phase <= 0.53:
        f_prog = np.clip(1.0 - abs(phase - 0.51) / 0.02, 0.0, 1.0)
        
        c_tensor = c_tensor * (1-f_prog) + C_FLASH * f_prog
        p_size *= (1.0 + f_prog * 1.5) 

        # Hardware visual spark with mathematically sound optics
        if f_prog > 0:
            ax.scatter([CX], [HEAD_Y-50], s=40000 * f_prog, color='#F1C40F', alpha=float(f_prog), edgecolors='none', zorder=25)
            ax.scatter([CX], [HEAD_Y-45], s=12000 * f_prog, color=C_BG, alpha=float(f_prog), edgecolors='none', zorder=26)

    # INTAKE TAPER
    in_mask = phase < stamp_in
    if np.any(in_mask):
        t_in = (stamp_in[in_mask] - phase) * 4.0
        px[in_mask] = (CX - 70) - t_in * 120 + (g_rx[in_mask] * 30)
        py[in_mask] = (HEAD_Y + 10) + t_in * 180 + (g_ry[in_mask] * 30)
        p_alpha[in_mask] = np.clip(1.0 - t_in, 0, 1)

    # EXHAUST TAPER
    ex_mask = phase > stamp_out
    if np.any(ex_mask):
        t_ex = (phase - stamp_out[ex_mask]) * 4.0
        px[ex_mask] = (CX + 70) + t_ex * 120 + (g_rx[ex_mask] * 30)
        py[ex_mask] = (HEAD_Y + 10) + t_ex * 180 + (g_ry[ex_mask] * 30)
        p_alpha[ex_mask] = np.clip(1.0 - t_ex, 0, 0.7)
        p_size[ex_mask] *= (1.0 + t_ex * 2.5) 

    rgba = np.column_stack((c_tensor, p_alpha))
    vis = py < 1800
    if np.any(vis):
        ax.scatter(px[vis], py[vis], s=p_size[vis], color=rgba[vis], edgecolors='none', zorder=5)

    # 6. METRIC WATERMARK (Rigid Engineering Telemetry)
    ax.add_patch(Rectangle((0, 1840), 1080, 80, facecolor=C_BG, zorder=50))
    ax.text(40, 1880, "LG-184b: O(1) FLUID KINEMATICS // 4-STROKE DAYLIGHT TRACE", color=C_IRON, fontsize=18, fontname='monospace', weight='bold', va='center', zorder=51)

    state_str = "INTAKE: MASS LOADING" if phase < 0.25 else ("COMPRESSION: VOLUME LIMITING" if phase < 0.5 else ("POWER: KINETIC VECTOR LOCK" if phase < 0.75 else "EXHAUST: ENTROPY PURGE"))
    text_color = '#3498DB' if phase < 0.25 else ('#E67E22' if phase < 0.5 else ('#C0392B' if phase < 0.75 else '#7F8C8D'))
    if 0.49 <= phase <= 0.53: text_color = '#F1C40F'
    
    ax.add_patch(Rectangle((0, 0), 1080, 100, facecolor=C_BG, zorder=50))
    ax.text(40, 50, f"PHASE TENSOR: {state_str}", color=text_color, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=51)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-184b OTTO DAYLIGHT ENGINE [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Ouroboros Fluid Expansion // IEEE-754 Safe Render")

    with mp.Pool(processes=cpu_cores) as pool:
        frames = range(TOTAL_FRAMES)
        for finished_frame in pool.imap_unordered(render_frame, frames, chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")
    print("Compilation Complete. Absolute Phase Architecture locked.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
