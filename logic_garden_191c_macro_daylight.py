"""
SOVEREIGN CODE: logic_garden_191b_macro_daylight.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Modular Phase Tensor
SCENE: LG-191b Macro (Daylight Protocol / Realistic Slider-Crank)
HOTFIX: White Background, Seamless Loop Math, High-Fidelity Mechanical Drafting
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon, Wedge
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 10.0
ROTATIONS = 10.0
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_191b_macro_daylight"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- DAYLIGHT MECHANICAL PALETTE --------
C_BG        = '#FFFFFF'        # Pure White Workspace
C_IRON_DK   = '#2C3E50'        # Heavy Dark Cast Iron
C_IRON_MD   = '#34495E'        # Base Cylinder / Boiler Block
C_WHEEL_RED = '#C0392B'        # Crimson Drive Wheel Spoke Base
C_STEEL     = '#BDC3C7'        # Machined Silver (Rods)
C_STEEL_LT  = '#ECF0F1'        # Specular Highlights
C_BRASS     = '#D4AC0D'        # Polished Brass Fittings
C_STEAM_DK  = '#7F8C8D'        # Dense Carbon Steam
C_STEAM_LT  = '#D5DBDB'        # Vaporizing Steam Transition

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE KINEMATIC BOUNDING BOX
# ------------------------------------------------------------------
WHEEL_X = 250.0
WHEEL_Y = 600.0
WHEEL_R = 280.0
CRANK_R = 140.0
ROD_L   = 580.0

CYL_X = WHEEL_X + CRANK_R + ROD_L + 60.0  # ≈ 1030.0
CYL_Y = WHEEL_Y
CYL_W = 180.0
CYL_H = 160.0
EXHAUST_X = CYL_X + 50.0
EXHAUST_Y = CYL_Y + CYL_H/2 + 20.0

# ------------------------------------------------------------------
# O(1) SEAMLESS STEAM TENSOR PRE-COMPUTATION
# ------------------------------------------------------------------
N_STEAM = 15000
np.random.seed(191)

# To sync visual steam 'chuffs' with the cylinder stroke, we cluster the offsets
# 2 exhausts per rotation, 10 rotations = 20 distinct chuffs in the loop.
CHUFFS = int(ROTATIONS * 2)
base_offsets = np.random.choice(np.arange(CHUFFS) / float(CHUFFS), N_STEAM)
# Jitter creates the expanding cloud nature
jitter = np.random.normal(0, 0.015, N_STEAM)
p_offsets = (base_offsets + jitter) % 1.0

# Fixed trajectory vectors mapped over the 10 sec lifespan
p_vx = np.random.normal(-180, 50, N_STEAM) # Wind blowing exhaust backwards (left)
p_vy = np.random.normal(700, 150, N_STEAM) # Upward stack velocity

p_sizes = np.random.uniform(10.0, 50.0, N_STEAM)
p_color_mix = np.random.uniform(0.0, 1.0, N_STEAM)

c_st_lt = np.array(hex_to_rgba(C_STEAM_LT)[:3])
c_st_dk = np.array(hex_to_rgba(C_STEAM_DK)[:3])

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    phase = f / float(TOTAL_FRAMES)  # 0.0 to 0.998...
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    fig.patch.set_facecolor(C_BG)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    # 1. KINEMATICS MATHEMATICS
    angle_deg = phase * 360.0 * ROTATIONS
    theta_rad = np.radians(angle_deg)

    pin_x = WHEEL_X + CRANK_R * np.cos(theta_rad)
    pin_y = WHEEL_Y + CRANK_R * np.sin(theta_rad)

    # Slider-Crank Formula
    ch_dist = CRANK_R * np.cos(theta_rad) + np.sqrt(max(0, ROD_L**2 - (CRANK_R * np.sin(theta_rad))**2))
    ch_x = WHEEL_X + ch_dist

    # 2. O(N) SEAMLESS STEAM TENSOR (Background Layer)
    # local_age scales exactly 0.0 -> 1.0 over the particle's 10sec life
    local_age = (phase - p_offsets) % 1.0
    t_age = local_age * DURATION
    
    # Kinematic projection
    px = EXHAUST_X + p_vx * t_age
    # Slight downward gravity drag on the cloud over time
    py = EXHAUST_Y + p_vy * t_age - (0.5 * 30.0 * t_age**2)
    
    mask = (py > EXHAUST_Y) & (px > -150) & (py < 2000)
    
    if np.any(mask):
        m_age = local_age[mask]
        sz = (1.0 + (m_age * 1.5)) * p_sizes[mask]
        
        # Color interpolation based on pre-computed mix
        cmix = p_color_mix[mask][:, None]
        base_colors = cmix * c_st_dk + (1 - cmix) * c_st_lt
        
        # Particles fade in instantly, fade out gracefully as they age
        alphas = np.clip((1.0 - m_age) * 1.5, 0.0, 0.4)
        
        rgba = np.zeros((len(base_colors), 4))
        rgba[:, :3] = base_colors
        rgba[:, 3] = alphas
        
        sort_idx = np.argsort(-sz)
        ax.scatter(px[mask][sort_idx], py[mask][sort_idx], s=sz[sort_idx], color=rgba[sort_idx], edgecolors='none', zorder=1)

    # 3. RENDER THE STATIC CHASSIS
    # Background alignment rail
    ax.axhline(WHEEL_Y, color=C_STEEL_LT, lw=10, zorder=2)
    
    # Cylinder Block & Housing
    ax.add_patch(Rectangle((CYL_X - 20, CYL_Y - CYL_H/2), CYL_W, CYL_H, facecolor=C_IRON_MD, edgecolor=C_IRON_DK, lw=6, zorder=3))
    # Rivet detailing
    for ry in [-50, -25, 0, 25, 50]:
        ax.add_patch(Circle((CYL_X + 10, CYL_Y + ry), 4, facecolor=C_IRON_DK, zorder=4))
        ax.add_patch(Circle((CYL_X + 130, CYL_Y + ry), 4, facecolor=C_IRON_DK, zorder=4))
    
    # Exhaust Stack base
    ax.add_patch(Rectangle((EXHAUST_X - 15, CYL_Y + CYL_H/2), 30, 40, facecolor=C_BRASS, edgecolor='#9C640C', lw=4, zorder=3))

    # 4. RENDER THE DRIVING WHEEL
    # Main outer rim
    ax.add_patch(Circle((WHEEL_X, WHEEL_Y), WHEEL_R, facecolor=C_BG, edgecolor=C_IRON_DK, lw=24, zorder=5))
    ax.add_patch(Circle((WHEEL_X, WHEEL_Y), WHEEL_R - 12, facecolor='none', edgecolor=C_STEEL_LT, lw=3, zorder=6))

    # Spokes
    for i in range(16):
        sa = np.radians(angle_deg + (i * 360/16))
        sx = WHEEL_X + (WHEEL_R - 20) * np.cos(sa)
        sy = WHEEL_Y + (WHEEL_R - 20) * np.sin(sa)
        ax.plot([WHEEL_X, sx], [WHEEL_Y, sy], color=C_WHEEL_RED, lw=18, solid_capstyle='round', zorder=5)
        ax.plot([WHEEL_X, sx], [WHEEL_Y, sy], color=C_IRON_DK, lw=6, zorder=6) # Central grove

    # Counterweight (Heavy Iron)
    ax.add_patch(Wedge((WHEEL_X, WHEEL_Y), WHEEL_R - 20, angle_deg+135, angle_deg+225, width=90, facecolor=C_IRON_MD, edgecolor=C_IRON_DK, lw=4, zorder=7))

    # Hub Center
    ax.add_patch(Circle((WHEEL_X, WHEEL_Y), 45, facecolor=C_IRON_DK, zorder=8))
    ax.add_patch(Circle((WHEEL_X, WHEEL_Y), 25, facecolor=C_BRASS, zorder=9))

    # 5. RENDER THE KINETIC LINKAGE
    # Main Rod
    ax.plot([pin_x, ch_x], [pin_y, CYL_Y], color=C_STEEL, lw=32, solid_capstyle='round', zorder=10)
    # Machined groove down the rod
    ax.plot([pin_x, ch_x], [pin_y, CYL_Y], color=C_STEEL_LT, lw=8, zorder=11)
    
    # Crosshead block sliding on rails
    ax.add_patch(Rectangle((ch_x - 35, CYL_Y - 45), 70, 90, facecolor=C_IRON_MD, edgecolor=C_IRON_DK, lw=5, zorder=12))
    
    # Internal Piston rod travelling into the cylinder
    ax.plot([ch_x, CYL_X + 150], [CYL_Y, CYL_Y], color=C_STEEL, lw=18, zorder=9)
    ax.plot([ch_x, CYL_X + 150], [CYL_Y, CYL_Y], color=C_STEEL_LT, lw=4, zorder=10) # Polish

    # Fasteners/Pins
    for p_x, p_y in [(pin_x, pin_y), (ch_x, CYL_Y)]:
        ax.add_patch(Circle((p_x, p_y), 22, facecolor=C_IRON_DK, zorder=13))
        ax.add_patch(Circle((p_x, p_y), 10, facecolor=C_BRASS, zorder=14))

    # 6. MINIMAL REALISTIC TELEMETRY
    ax.text(30, 20, f"MACRO-KINEMATICS // RATIO: π", color=C_IRON_DK, fontsize=12, fontname='monospace', alpha=0.5, zorder=20)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-191b MACRO v4: DAYLIGHT ENGINE [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Ouroboros Phase Math // Realism")

    with mp.Pool(processes=cpu_cores) as pool:
        frames = range(TOTAL_FRAMES)
        for finished_frame in pool.imap_unordered(render_frame, frames, chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")
    print("Compilation Complete. Absolute Serialisation achieved.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
