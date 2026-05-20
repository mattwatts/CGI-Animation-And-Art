"""
SOVEREIGN CODE: logic_garden_184d_wankel_daylight.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Parametric Fluid Phase Tensor
SCENE: LG-184d (Wankel Rotary Engine / Daylight Engineering Protocol)
HOTFIX: Exact Epitrochoid Envelope, Local Coordinate Reuleaux Tensor
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
OUT_DIR = "frames_184d_wankel_daylight"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST ENGINEERING PALETTE --------
C_BG        = '#FFFFFF'        
C_BLOCK     = '#E5E8E8'        # Heavy Aluminum Casing
C_STEEL     = '#7F8C8D'        # Machined Components
C_IRON      = '#1C2833'        # Epitrochoid Boundary
C_ROTOR     = '#95A5A6'        # Gunmetal Reuleaux
C_CHROME    = '#D0D3D4'        # Eccentric Shaft Journal
C_BRASS     = '#B9770E'        # Stationary Gear Ring
C_WATER     = '#1ABC9C'        # Coolant Jacket Array

# Thermodynamic Plasma Vectors
C_IN_AERO   = np.array([0.0, 0.8, 0.8])    # Aerosol Mix
C_IN_COMP   = np.array([0.9, 0.5, 0.1])    # Heat Squeeze
C_IGNITION  = np.array([1.0, 1.0, 0.8])    # Spark Propagation
C_POWER     = np.array([1.0, 0.1, 0.1])    # Expanding Flash
C_EXHAUST   = np.array([0.2, 0.2, 0.25])   # Combusted Carbon

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: EPITROCHOID & REULEAUX CONSTANTS
# ------------------------------------------------------------------
CX, CY  = 540, 920       
R_GEN   = 240.0        # Generating Radius
E_ECC   = 35.0         # Eccentricity
BOW_MAX = 20.0         # Rotor face convexity

N_GAS_FACE = 8000
N_FACES = 3

# Pre-allocated arrays for fluid matrices
np.random.seed(184)
t_rands = np.random.rand(N_FACES, N_GAS_FACE)
n_rands = np.random.rand(N_FACES, N_GAS_FACE)

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    phase = f / float(TOTAL_FRAMES)
    
    # 2 full rotor rotations in 10 sec = 720 degrees
    rot_ang_deg = phase * 720.0
    rot_ang = np.radians(rot_ang_deg)
    
    # Eccentric shaft rotates 3x faster
    ecc_ang_deg = rot_ang_deg * 3.0
    ecc_ang = np.radians(ecc_ang_deg)

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    fig.patch.set_facecolor(C_BG)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    # 1. RENDER EPITROCHOID HOUSING ARCHITECTURE
    # Angle sweep for housing perimeter
    alpha = np.linspace(0, 2*np.pi, 400)
    # Parametric layout: Bulges Top/Bottom, Pinches Left/Right
    h_x = CX + E_ECC * np.sin(3 * alpha) + R_GEN * np.sin(alpha)
    h_y = CY + E_ECC * np.cos(3 * alpha) + R_GEN * np.cos(alpha)

    # Thick Cast Aluminum Base (Cooling block)
    block_h = 750
    ax.add_patch(Rectangle((CX-400, CY-block_h/2), 800, block_h, facecolor=C_BLOCK, edgecolor='none', zorder=1))
    
    # Peripheral Ports Castings
    ax.plot([CX-400, CX-200], [CY+200, CY+120], color=C_BG, lw=50, zorder=2) # Intake Pipe
    ax.plot([CX-400, CX-200], [CY-200, CY-120], color=C_BG, lw=50, zorder=2) # Exhaust Pipe
    
    # Epitrochoid Chamber Boundary
    ax.fill(h_x, h_y, facecolor=C_BG, zorder=4)  
    ax.plot(h_x, h_y, color=C_IRON, lw=12, zorder=20) # Machined iron face
    
    # Coolant Water Jacket Perimeter
    w_x = CX + (E_ECC+5) * np.sin(3 * alpha) + (R_GEN+25) * np.sin(alpha)
    w_y = CY + (E_ECC+5) * np.cos(3 * alpha) + (R_GEN+25) * np.cos(alpha)
    ax.plot(w_x, w_y, color=C_WATER, lw=8, zorder=3)

    # 2. INTERNAL KINEMATICS (Eccentric Shaft & Stationary Gear)
    crank_x = CX + E_ECC * np.sin(ecc_ang)
    crank_y = CY + E_ECC * np.cos(ecc_ang)

    ax.add_patch(Circle((CX, CY), 45, facecolor=C_BG, edgecolor=C_IRON, lw=6, zorder=21))
    ax.add_patch(Circle((CX, CY), 35, facecolor=C_BRASS, zorder=22)) # Stationary gear

    ax.add_patch(Circle((crank_x, crank_y), 75, facecolor=C_CHROME, edgecolor=C_IRON, lw=4, zorder=20))
    ax.add_patch(Circle((crank_x, crank_y), 25, facecolor=C_BG, edgecolor=C_IRON, lw=4, zorder=23))

    # 3. ROTOR DYNAMICS (The Reuleaux Tensor)
    v_x = np.zeros(3); v_y = np.zeros(3)
    rotor_pts = []
    
    for k in range(N_FACES):
        # Vertex angle
        vk_ang = rot_ang + np.radians(k * 120)
        v_x[k] = crank_x + R_GEN * np.sin(vk_ang)
        v_y[k] = crank_y + R_GEN * np.cos(vk_ang)
        
        # Apex Seals
        n_x = np.sin(vk_ang); n_y = np.cos(vk_ang)
        ax.plot([v_x[k], v_x[k] + n_x*12], [v_y[k], v_y[k] + n_y*12], color='#000000', lw=5, zorder=25)

    # Generating the bowed realistic rotor face
    for k in range(N_FACES):
        A = np.array([v_x[k], v_y[k]])
        B = np.array([v_x[(k+1)%3], v_y[(k+1)%3]])
        L = B - A
        norm = np.array([-L[1], L[0]]) / np.linalg.norm(L)
        
        # Ensure normal points outward
        if np.dot(norm, (A+B)/2 - np.array([crank_x, crank_y])) < 0: norm = -norm
        
        t = np.linspace(0, 1, 50).reshape(-1, 1)
        arc = A + t * L + norm * (BOW_MAX * np.sin(np.pi * t))
        rotor_pts.append(arc)
        
        # Combustion Pockets (Offset inward)
        pocket = A + t * L + norm * ((BOW_MAX - 15.0) * np.sin(np.pi * t))
        ax.plot(pocket[:,0], pocket[:,1], color=C_IRON, lw=4, alpha=0.4, zorder=22)

    rotor_poly = np.vstack(rotor_pts)
    ax.add_patch(Polygon(rotor_poly, facecolor=C_ROTOR, edgecolor=C_IRON, lw=5, zorder=21))

    # 4. O(1) THERMODYNAMIC FLUID TENSOR (Isolated Chamber Physics)
    for k in range(N_FACES):
        # Face Midpoint Phase Logic
        mid_ang = (rot_ang_deg + k * 120 + 60) % 360
        # Thickness of fluid chamber (Max at Y bulges, Min at X pinches)
        gap_w = 8.0 + 42.0 * ((1.0 - np.cos(np.radians(2 * mid_ang))) / 2.0)
        
        A = np.array([v_x[k], v_y[k]])
        B = np.array([v_x[(k+1)%3], v_y[(k+1)%3]])
        L = B - A
        norm = np.array([-L[1], L[0]]) / np.linalg.norm(L)
        if np.dot(norm, (A+B)/2 - np.array([crank_x, crank_y])) < 0: norm = -norm
        
        t_vec = t_rands[k]
        n_vec = n_rands[k]
        
        # Geometrically force particles into the exact crescent volume between rotor and epitrochoid
        base_x = A[0] + L[0] * t_vec
        base_y = A[1] + L[1] * t_vec
        
        rotor_bow = BOW_MAX * np.sin(np.pi * t_vec)
        fluid_depth = rotor_bow + (n_vec * gap_w * np.sin(np.pi * t_vec))
        
        px = base_x + norm[0] * fluid_depth
        py = base_y + norm[1] * fluid_depth

        # Color Schedule (Phase Dynamics)
        if mid_ang >= 270:
            prog = (mid_ang - 270) / 90.0
            base_col = C_IN_AERO
        elif mid_ang < 90:
            prog = mid_ang / 90.0
            base_col = C_IN_AERO * (1-prog) + C_IN_COMP * prog
        elif mid_ang < 180:
            prog = (mid_ang - 90) / 90.0
            base_col = C_POWER * (1-prog) + C_EXHAUST * prog
        else:
            base_col = C_EXHAUST
            
        c_tensor = np.zeros((N_GAS_FACE, 3))
        c_tensor[:] = base_col
        ps = np.full(N_GAS_FACE, 18.0)

        # Hardware Interrupt: Ignition Flash exactly at Minimum Volume Pinch (Right Side = 90 deg)
        if 85 < mid_ang < 98:
            f_prog = 1.0 - abs(mid_ang - 91.5) / 6.5
            c_tensor = c_tensor * (1-f_prog) + C_IGNITION * f_prog
            ps *= (1.0 + f_prog * 2.0)
            
            # Spark plug arcing visually
            ax.plot([CX+R_GEN-E_ECC, CX+R_GEN-E_ECC-15], [CY+15, CY+15], color='#FFFFFF', lw=4, zorder=30)
            ax.plot([CX+R_GEN-E_ECC, CX+R_GEN-E_ECC-15], [CY-15, CY-15], color='#FFFFFF', lw=4, zorder=30)

        # Draw Fluid Set
        ax.scatter(px, py, s=ps, color=c_tensor, alpha=0.9, edgecolors='none', zorder=10)

    # 5. STRUCTURAL PORTS & SPARK PLUGS 
    # Dual Spark Plugs (Trailing and Leading)
    bx_p = CX+R_GEN-E_ECC+5
    ax.add_patch(Rectangle((bx_p, CY+5), 60, 20, facecolor=C_STEEL, edgecolor=C_IRON, lw=2, zorder=20))
    ax.add_patch(Rectangle((bx_p, CY-25), 60, 20, facecolor=C_STEEL, edgecolor=C_IRON, lw=2, zorder=20))
    ax.text(bx_p+70, CY+15, "T", color=C_STEEL, fontsize=16, weight='bold', va='center', zorder=20)
    ax.text(bx_p+70, CY-15, "L", color=C_STEEL, fontsize=16, weight='bold', va='center', zorder=20)

    # 6. EXTERNAL MANIFOLD EMITTERS (Visual Flow Illusion)
    # Intake flow
    intake_active = (rot_ang_deg % 120) < 60
    if intake_active:
        sp_x = np.random.uniform(CX-400, CX-200, 200)
        sp_y = np.random.uniform(CY+140, CY+180, 200)
        ax.scatter(sp_x, sp_y, s=25, color=C_IN_AERO, alpha=0.7, zorder=3)
    
    # Exhaust flow
    exh_active = (rot_ang_deg % 120) > 60
    if exh_active:
        sp_x = np.random.uniform(CX-400, CX-200, 300)
        sp_y = np.random.uniform(CY-180, CY-140, 300)
        ax.scatter(sp_x, sp_y, s=35, color=C_EXHAUST, alpha=0.8, zorder=3)

    # 7. TELEMETRY WIDGETS
    ax.add_patch(Rectangle((0, 1840), 1080, 80, facecolor=C_BLOCK, zorder=50))
    ax.text(40, 1880, "LG-184d: EPITROCHOID TENSOR // ROTARY DAYLIGHT TRACE", color=C_IRON, fontsize=18, fontname='monospace', weight='bold', va='center', zorder=51)

    state_str = "REULEAUX ROTOR ACTIVE // O(1) FLUID ISOLATION"
    ax.add_patch(Rectangle((0, 0), 1080, 100, facecolor=C_BLOCK, zorder=50))
    ax.text(40, 50, f"KINEMATIC LOGIC: {state_str}", color=C_IRON, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=51)

    # Eccentric Telemetry Dial
    ax.add_patch(Circle((960, 50), 30, facecolor='none', edgecolor=C_IRON, lw=4, zorder=51))
    ind_ang = np.radians(-ecc_ang_deg + 90.0) 
    ax.plot([960, 960 - np.sin(ind_ang)*25], [50, 50 + np.cos(ind_ang)*25], color=C_STEEL, lw=4, zorder=52)
    ax.text(910, 50, f"ECC: {int(ecc_ang_deg%360):03d}°", color=C_IRON, fontsize=14, fontname='monospace', weight='bold', ha='right', va='center', zorder=51)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-184d ROTARY EPITROCHOID TENSOR [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Ouroboros Rotary Vector Arrays")

    with mp.Pool(processes=cpu_cores) as pool:
        frames = range(TOTAL_FRAMES)
        for finished_frame in pool.imap_unordered(render_frame, frames, chunksize=8):
            pass
    print("Compilation Complete. Absolute Phase Architecture locked.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
