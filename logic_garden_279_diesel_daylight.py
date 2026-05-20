"""
SOVEREIGN CODE: logic_garden_279_diesel_daylight_12rpm.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Unified Batch Phase Tensor
SCENE: LG-279 (Diesel 4-Stroke Compression Ignition / Daylight Protocol)
HOTFIX: Single-Cycle Precision (10s = 1 Loop), Complete Logic Audit
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
OUT_DIR = "frames_279_diesel_daylight_12rpm"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST ENGINEERING PALETTE --------
C_BG        = '#FFFFFF'        
C_DIM       = '#D0D0D5'        # Heavy Cast Casing
C_IRON      = '#1C2833'        # Hard Engine Limits
C_STEEL     = '#7F8C8D'        # Machined Rods & Valves
C_CHROME    = '#D0D3D4'        # Specular Highlights
C_INJECTOR  = '#222222'        # Nozzle

# Thermodynamics
C_AIR_COLD  = np.array([0.20, 0.80, 0.95]) # Pure Atmospheric Draw
C_AIR_COMP  = np.array([0.95, 0.35, 0.00]) # 18:1 Adiabatic Squeeze
C_MAGENTA   = np.array([0.90, 0.10, 0.30]) # Diffusion Detonation
C_EXHAUST   = np.array([0.45, 0.45, 0.45]) # Base Dark Gas
C_SOOT      = np.array([0.05, 0.05, 0.05]) # Particulate Matter matrix

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY & RIGID CONSTANTS
# ------------------------------------------------------------------
CX, CY  = 540, 480       
CRANK_R = 170.0
ROD_L   = 560.0
BORE    = 280.0
PISTON_H = 180.0
HEAD_Y  = 1400.0  # 10px absolute clearance at TDC

N_CYL = 20000
N_PORT = 6000

np.random.seed(279)
cyl_rx = np.random.uniform(-0.5, 0.5, N_CYL)
cyl_ry = np.random.uniform(0.0, 1.0, N_CYL)
cyl_swirl = np.random.normal(0, 1, N_CYL) # Thermal mixing dynamics

in_rx = np.random.uniform(-0.5, 0.5, N_PORT)
in_ry = np.random.uniform(0.0, 1.0, N_PORT)

ex_rx = np.random.uniform(-0.5, 0.5, N_PORT)
ex_ry = np.random.uniform(0.0, 1.0, N_PORT)
is_soot_port = np.random.rand(N_PORT) > 0.75 

# ------------------------------------------------------------------
# PRE-CALCULATED MACRO-INTEGRATION (Perfect Manifold Wrapping)
# ------------------------------------------------------------------
# We execute precisely 1 engine cycle across 10 seconds.
v_in_raw = np.zeros(TOTAL_FRAMES)
v_ex_raw = np.zeros(TOTAL_FRAMES)

for f in range(TOTAL_FRAMES):
    # e_mod exactly maps f / 600
    e_mod = f / float(TOTAL_FRAMES)
    if e_mod < 0.25: v_in_raw[f] = 1.0 # Intake Valve Open (0 - 180 deg)
    if e_mod > 0.75: v_ex_raw[f] = 1.0 # Exhaust Valve Open (540 - 720 deg)

cum_in = np.cumsum(v_in_raw)
cum_ex = np.cumsum(v_ex_raw)

# Enforce integer modulo wrapping. Velocity scales perfectly to visual WRAP boundary.
WRAP = 1000.0
cum_in = (cum_in / cum_in[-1]) * (WRAP * 1.0) 
cum_ex = (cum_ex / cum_ex[-1]) * (WRAP * 1.0)

# ------------------------------------------------------------------
# THE 4-STROKE KINEMATICS
# ------------------------------------------------------------------
def get_kinematics(e_mod):
    crank_deg = e_mod * 720.0 
    crank_rad = np.radians(crank_deg)

    c_x = CX + CRANK_R * np.sin(crank_rad)
    c_y = CY + CRANK_R * np.cos(crank_rad)

    term2 = np.sqrt(max(0, ROD_L**2 - (c_x - CX)**2))
    pin_y = c_y + term2
    piston_top = pin_y + PISTON_H
    
    # Valve timing strictly gated to exact quarters of the cycle.
    v_in = np.clip(np.sin((e_mod / 0.25) * np.pi), 0, 1) * 60.0 if e_mod < 0.25 else 0.0
    v_ex = np.clip(np.sin(((e_mod - 0.75) / 0.25) * np.pi), 0, 1) * 60.0 if e_mod > 0.75 else 0.0

    return c_x, c_y, pin_y, piston_top, crank_deg, v_in, v_ex

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    e_mod = f / float(TOTAL_FRAMES) # Guaranteed 0.0 to 1.0

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    fig.patch.set_facecolor(C_BG)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    # 1. KINEMATICS
    c_x, c_y, pin_y, piston_top, crank_deg, v_in, v_ex = get_kinematics(e_mod)
    wall_l, wall_r = CX - BORE/2, CX + BORE/2

    # 2. RENDER THE BATCH FLUID TENSOR
    
    # --- CYLINDER BATCH (Unified Strict Column) ---
    px_c = CX + cyl_rx * (BORE - 10)
    # Volumetric fill constraint: Fluid perfectly fills the instantaneous gap.
    py_c = piston_top + 5 + cyl_ry * (HEAD_Y - piston_top - 10)
    
    pc_c = np.zeros((N_CYL, 3))
    ps_c = np.full(N_CYL, 20.0)
    
    if e_mod < 0.25: # Intake Phase
        if e_mod < 0.10: # Valve Overlap / Scavenging blend (Seamless Loop Hotfix)
            prog = e_mod / 0.10
            c_base = C_EXHAUST * (1.0-prog) + C_AIR_COLD * prog
            pc_c[:] = c_base
            pc_c[cyl_swirl > 0.5] = C_SOOT * (1.0-prog) + C_AIR_COLD * prog
        else:
            pc_c[:] = C_AIR_COLD
    elif e_mod < 0.5: # Adiabatic Compression (Valves Closed)
        prog = (e_mod - 0.25) / 0.25
        pc_c[:] = C_AIR_COLD * (1.0-prog) + C_AIR_COMP * prog
        px_c += cyl_swirl * (5.0 * prog) 
    elif e_mod < 0.75: # Diffusion Power Stroke (Valves Closed)
        prog = (e_mod - 0.5) / 0.25
        burn_line = 1.0 - (prog * 1.5) 
        is_burnt = cyl_ry > burn_line
        
        fade = np.clip(prog * 1.5, 0.0, 1.0)
        c_fire = C_MAGENTA * (1.0 - fade) + C_EXHAUST * fade
        pc_c[:] = c_fire
        pc_c[is_burnt] = C_EXHAUST
        pc_c[(cyl_swirl > 0.5) & is_burnt] = C_SOOT # Soot formation in diffusion edge
        px_c += cyl_swirl * (10.0 * prog) 
    else: # Exhaust Phase
        pc_c[:] = C_EXHAUST
        pc_c[cyl_swirl > 0.5] = C_SOOT 

    ax.scatter(px_c, py_c, s=ps_c, color=pc_c, edgecolors='none', zorder=5)

    # --- INTAKE MANIFOLD ---
    y_shift_in = cum_in[f] % WRAP
    px_in = CX - 100 + in_rx * 100
    py_in = HEAD_Y + 400 - (in_ry * WRAP) - y_shift_in
    py_in = np.where(py_in < HEAD_Y, py_in + WRAP, py_in)
    
    valid_in = (py_in > HEAD_Y) & (py_in < HEAD_Y + 300)
    ax.scatter(px_in[valid_in], py_in[valid_in], s=20, color=C_AIR_COLD, edgecolors='none', zorder=4)

    # --- EXHAUST MANIFOLD ---
    y_shift_ex = cum_ex[f] % WRAP
    px_ex = CX + 100 + ex_rx * 100
    py_ex = HEAD_Y + (ex_ry * WRAP) + y_shift_ex
    py_ex = np.where(py_ex > HEAD_Y + WRAP, py_ex - WRAP, py_ex)
    
    valid_ex = (py_ex > HEAD_Y) & (py_ex < HEAD_Y + 300)
    pc_ex = np.zeros((len(py_ex), 3))
    pc_ex[:] = C_EXHAUST
    pc_ex[is_soot_port] = C_SOOT
    ax.scatter(px_ex[valid_ex], py_ex[valid_ex], s=20, color=pc_ex[valid_ex], edgecolors='none', zorder=4)

    # 3. HIGH-PRESSURE DIRECT INJECTOR (Diesel Core Physics)
    ax.add_patch(Rectangle((CX-25, HEAD_Y), 50, 60, facecolor=C_STEEL, edgecolor=C_IRON, lw=4, zorder=21))
    ax.add_patch(Rectangle((CX-15, HEAD_Y-20), 30, 20, facecolor=C_INJECTOR, edgecolor=C_IRON, lw=2, zorder=21))

    # Injection Window: 0.490 to 0.520 (approx 18 frames in slow-motion)
    if 0.49 <= e_mod <= 0.52:
        inj_prog = float(np.clip(1.0 - abs(e_mod - 0.505) / 0.015, 0.0, 1.0))
        if inj_prog > 0:
            for angle_deg in [-25, -10, 10, 25]:
                a_rad = np.radians(angle_deg - 90) 
                spray_len = 160 * inj_prog
                jx = CX + np.cos(a_rad) * spray_len
                jy = HEAD_Y - 20 + np.sin(a_rad) * spray_len
                
                # Raw Fuel Shards injecting into adiabatic core
                ax.plot([CX, jx], [HEAD_Y-20, jy], color=C_INJECTOR, lw=8, zorder=25)
                # Outer Detonation Plasma
                ax.plot([CX, jx], [HEAD_Y-20, jy], color=C_MAGENTA, lw=4, zorder=26)
                
                ax.scatter([jx], [jy], s=12000 * inj_prog, color='#FF4500', alpha=inj_prog * 0.8, edgecolors='none', zorder=27)
                ax.scatter([jx], [jy], s=4000 * inj_prog, color='#FFFFFF', alpha=inj_prog, edgecolors='none', zorder=28)

    # 4. ENGINE ARCHITECTURE OVERLAY
    ax.add_patch(Rectangle((wall_l, CY), BORE, HEAD_Y-CY, facecolor='none', edgecolor=C_IRON, lw=20, zorder=20))
    ax.add_patch(Rectangle((wall_l-120, CY), BORE+240, 20, facecolor=C_IRON, zorder=20)) 

    # Head Deck (Zero Piston Intersection Allowed)
    ax.plot([wall_l-150, CX-40], [HEAD_Y, HEAD_Y], color=C_IRON, lw=36, zorder=20)   
    ax.plot([CX+40, wall_r+150], [HEAD_Y, HEAD_Y], color=C_IRON, lw=36, zorder=20)   
    
    # Cast Manifold Trunks
    ax.plot([wall_l, CX-50], [HEAD_Y+240, HEAD_Y], color=C_DIM, lw=20, zorder=19) 
    ax.plot([wall_r, CX+50], [HEAD_Y+240, HEAD_Y], color=C_DIM, lw=20, zorder=19) 

    in_v_y = HEAD_Y - v_in
    ex_v_y = HEAD_Y - v_ex
    
    # Intake Valve
    ax.plot([CX-95, CX-95], [HEAD_Y+140, in_v_y], color=C_STEEL, lw=12, zorder=15)
    ax.add_patch(Polygon([(CX-145, in_v_y), (CX-45, in_v_y), (CX-95, in_v_y+30)], facecolor=C_CHROME, edgecolor=C_IRON, lw=4, zorder=16))
    
    # Exhaust Valve
    ax.plot([CX+95, CX+95], [HEAD_Y+140, ex_v_y], color=C_STEEL, lw=12, zorder=15)
    ax.add_patch(Polygon([(CX+45, ex_v_y), (CX+145, ex_v_y), (CX+95, ex_v_y+30)], facecolor=C_CHROME, edgecolor=C_IRON, lw=4, zorder=16))

    # 5. KINEMATIC ACTUATOR
    ax.add_patch(Rectangle((wall_l+6, piston_top-PISTON_H), BORE-12, PISTON_H, facecolor='#AAB7B8', edgecolor=C_IRON, lw=8, zorder=18))
    for ry in [20, 50, 80]: 
        ax.plot([wall_l+4, wall_r-4], [piston_top-ry, piston_top-ry], color=C_IRON, lw=8, zorder=19)
    
    # Diesel specific Combustion Bowl
    bp_x = np.linspace(CX-70, CX+70, 50)
    bp_y = piston_top - 25 * np.sin(np.pi * (bp_x - (CX-70)) / 140)
    ax.plot(bp_x, bp_y, color=C_IRON, lw=6, zorder=19)
    ax.fill_between(bp_x, piston_top, bp_y, facecolor=C_BG, zorder=19)

    ax.plot([c_x, CX], [c_y, pin_y], color=C_IRON, lw=46, solid_capstyle='round', zorder=16)
    ax.plot([c_x, CX], [c_y, pin_y], color=C_STEEL, lw=20, zorder=17) 
    ax.add_patch(Circle((CX, pin_y), 35, facecolor=C_IRON, zorder=18)) 
    ax.add_patch(Circle((CX, pin_y), 18, facecolor='#A04000', zorder=19)) 

    # Symmetrical Solid Steel Crank Web
    ax.add_patch(Circle((CX, CY), CRANK_R+60, facecolor=C_STEEL, edgecolor=C_IRON, lw=8, zorder=14))
    opp_ang = np.radians(crank_deg + 180.0)
    for spread in [-30.0, 0.0, 30.0]:
        h_ang = opp_ang + np.radians(spread)
        h_x = CX + np.sin(h_ang) * (CRANK_R - 15)
        h_y = CY + np.cos(h_ang) * (CRANK_R - 15)
        ax.add_patch(Circle((h_x, h_y), 40, facecolor=C_BG, edgecolor=C_IRON, lw=4, zorder=15))

    ax.add_patch(Circle((CX, CY), 45, facecolor=C_CHROME, edgecolor=C_IRON, lw=5, zorder=16)) 
    ax.add_patch(Circle((c_x, c_y), 50, facecolor=C_CHROME, edgecolor=C_IRON, lw=5, zorder=16)) 

    # 6. METRIC WATERMARK & UI
    ax.add_patch(Rectangle((0, 1840), 1080, 80, facecolor=C_BG, zorder=50))
    ax.text(40, 1880, "LG-279: COMPRESSION IGNITION (DIESEL) // O(1) BATCH TENSOR", color=C_IRON, fontsize=18, fontname='monospace', weight='bold', va='center', zorder=51)

    state_str = "INTAKE: PURE ATMOSPHERIC DRAW"
    text_color = '#3498DB'
    if 0.25 <= e_mod < 0.50:
        state_str = "COMPRESSION: ADIABATIC THERMAL SQUEEZE"
        text_color = '#E67E22'
    elif 0.50 <= e_mod < 0.75:
        state_str = "POWER: DIFFUSION FLAME EXPANSION"
        text_color = '#C0392B'
    elif 0.75 <= e_mod:
        state_str = "EXHAUST: EXACT SOOT/CARBON MATRIX"
        text_color = '#515A5A'

    ax.add_patch(Rectangle((0, 0), 1080, 100, facecolor=C_BG, zorder=50))
    ax.text(40, 50, f"PHASE LOGIC: {state_str}", color=text_color, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=51)
    
    # Exact Crank Angle Graphic Dial Widget
    ax.add_patch(Circle((1000, 50), 30, facecolor='none', edgecolor=C_IRON, lw=4, zorder=51))
    ind_ang = np.radians(crank_deg + 180.0) 
    ax.plot([1000, 1000 - np.sin(ind_ang)*25], [50, 50 + np.cos(ind_ang)*25], color=C_STEEL, lw=4, zorder=52)
    ax.text(950, 50, f"{int(crank_deg%360):03d}°", color=C_IRON, fontsize=18, fontname='monospace', weight='bold', ha='right', va='center', zorder=51)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-279: TRUE DIESEL KINEMATICS [12 RPM INTENSIVE TRACE] [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: 1 Cycle / 10 Seconds // O(1) Slow-Motion Geometry")

    with mp.Pool(processes=cpu_cores) as pool:
        frames = range(TOTAL_FRAMES)
        for finished_frame in pool.imap_unordered(render_frame, frames, chunksize=8):
            pass
    print("Compilation Complete. Raw Compression Thermodynamics Locked.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
