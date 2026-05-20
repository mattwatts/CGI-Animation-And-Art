"""
SOVEREIGN CODE: logic_garden_191d_behemoth_daylight.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Cinematic Slipstream Tensor
SCENE: Logic Garden 191d (The Kinetic Behemoth - Daylight Loop)
HOTFIX: Kinematic Inversion (Clockwise Drive Sync), Seamless 10s Array
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
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_191d_behemoth_daylight"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- DAYLIGHT REALISM PALETTE --------
C_SKY       = '#FFFFFF'        # Pure White Workspace
C_GRASS     = '#27AE60'        # Ground Cover
C_DIRT      = '#5D4037'        # Sub-ballast
C_BALLAST   = '#7F8C8D'        # Track Ballast Crushed Stone
C_IRON      = '#2C3E50'        # Boiler & Chassis
C_CABIN     = '#1A252F'        # Darker Iron for contrast
C_WHEELS    = '#C0392B'        # Crimson Drive Wheels
C_BRASS     = '#D4AC0D'        # Polished Brass
C_STEEL     = '#BDC3C7'        # Machined Rods
C_STEAM_W   = '#ECF0F1'        # Vapor Stream
C_STEAM_D   = '#7F8C8D'        # Dense Carbon Particulates

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_st_w = np.array(hex_to_rgba(C_STEAM_W)[:3])
c_st_d = np.array(hex_to_rgba(C_STEAM_D)[:3])

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE FULL CHASSIS ARCHITECTURE
# ------------------------------------------------------------------
GROUND_Y = 500.0
DRIVE_R = 140.0
WHEEL_Y = GROUND_Y + DRIVE_R + 10.0

# Driving Wheels (The heavy traction)
W1_X = 350.0
W2_X = 650.0
CRANK_R = 75.0

# Main Boiler Math
BOILER_X = 150.0
BOILER_Y = WHEEL_Y + 30.0
BOILER_W = 750.0
BOILER_H = 220.0

CAB_X = BOILER_X - 120.0
CAB_Y = BOILER_Y - 40.0
CAB_W = 200.0
CAB_H = 380.0

STACK_W = 70.0
STACK_H = 140.0
STACK_X = BOILER_X + BOILER_W - 90.0
STACK_Y = BOILER_Y + BOILER_H

PILOT_X = BOILER_X + BOILER_W

# Kinematic Ratios
ROTATIONS = 12.0
TOTAL_DISTANCE = ROTATIONS * 2 * np.pi * DRIVE_R
TOTAL_SLEEPERS = 80.0
SLEEPER_SPACING = TOTAL_DISTANCE / TOTAL_SLEEPERS

# ------------------------------------------------------------------
# O(1) SEAMLESS STEAM TENSOR & SLIPSTREAM PRE-COMPUTATION
# ------------------------------------------------------------------
N_STEAM = 25000
N_SLIP = 800
np.random.seed(1914)

# Chuff Synchronization (2 Exhausts per rotation)
CHUFFS = int(ROTATIONS * 2)
chuff_centers = np.linspace(0, 1, CHUFFS, endpoint=False)
base_offsets = np.random.choice(chuff_centers, N_STEAM)
jitter = np.random.normal(0, 0.015, N_STEAM)
p_offsets = (base_offsets + jitter) % 1.0

# Kinematic Trajectories for Steam
p_vx = np.random.normal(-350, 80, N_STEAM) # Violent horizontal aerodynamic drag backwards
p_vy = np.random.normal(600, 200, N_STEAM) # High-pressure vertical ejection
p_sizes = np.random.uniform(5.0, 45.0, N_STEAM)
p_color_mix = np.random.uniform(0.0, 1.0, N_STEAM)

# Slipstream parallax tracking leftwards seamlessly (Engine pulling forward)
sx_base = np.random.uniform(0, 1200, N_SLIP)
sy_base = np.random.uniform(0, 1920, N_SLIP)
s_len = np.random.uniform(50, 300, N_SLIP)
s_mult = np.random.choice([0.6, 0.8, 1.0, 1.2], N_SLIP) # Parallax depth layers

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(f):
    phase = f / float(TOTAL_FRAMES)  # 0.0 to 0.998...
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    fig.patch.set_facecolor(C_SKY)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    ax.set_facecolor(C_SKY)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    # 1. KINEMATIC MATHEMATICS (Angular to Linear Translation)
    # HOTFIX: Inverted Phase to force Native Clockwise Rotation.
    # Driving the train Right (+x) means rolling the wheel Clockwise (-theta).
    angle_deg = (1.0 - phase) * 360.0 * ROTATIONS
    theta_rad = np.radians(angle_deg)
    dist_travelled = phase * TOTAL_DISTANCE

    # 2. RENDER THE SLIPSTREAM (Atmospheric Aerodynamics)
    # Applying seamless modulo math to the background parallax vectors (rolling left)
    curr_sx = (sx_base - dist_travelled * s_mult) % 1400 - 200
    
    for i in range(min(500, N_SLIP)):
        ax.plot([curr_sx[i], curr_sx[i] + s_len[i]], [sy_base[i], sy_base[i]], color='#ECF0F1', lw=1.5, alpha=0.4, zorder=1)

    # 3. RENDER THE EARTH & BALLAST (Seamless Modulo Loop)
    ax.add_patch(Rectangle((0, 0), 1080, GROUND_Y - 50, facecolor=C_GRASS, zorder=1))
    ax.add_patch(Rectangle((0, GROUND_Y - 50), 1080, 50, facecolor=C_DIRT, zorder=2))
    ax.add_patch(Rectangle((0, GROUND_Y - 15), 1080, 25, facecolor=C_BALLAST, zorder=3))

    # Heavy Steel Rail
    ax.axhline(GROUND_Y + 10, color='#95A5A6', lw=12, zorder=5)
    ax.axhline(GROUND_Y + 14, color='#FFFFFF', lw=2, alpha=0.5, zorder=5) # Glare

    # Rushing Sleepers tied to Master Velocity (Rolling Left)
    track_offset = dist_travelled % SLEEPER_SPACING
    for i in range(-5, int(1080/SLEEPER_SPACING) + 5):
        sleep_x = (i * SLEEPER_SPACING) - track_offset
        if -150 <= sleep_x <= 1180:
            ax.add_patch(Rectangle((sleep_x, GROUND_Y - 20), 45, 20, facecolor='#3E2723', edgecolor='#212121', lw=2, zorder=4))
            ax.add_patch(Rectangle((sleep_x + 10, GROUND_Y), 25, 4, facecolor=C_IRON, zorder=4))

    # 4. RENDER THE STATIC CHASSIS (The Heavy Iron)
    ax.add_patch(Rectangle((CAB_X, CAB_Y), CAB_W, CAB_H, facecolor=C_CABIN, edgecolor='#111820', lw=4, zorder=10))
    ax.add_patch(Polygon([(CAB_X-20, CAB_Y+CAB_H), (CAB_X+CAB_W+20, CAB_Y+CAB_H), (CAB_X+CAB_W+10, CAB_Y+CAB_H+40), (CAB_X-10, CAB_Y+CAB_H+40)], facecolor='#111820', zorder=11))
    
    ax.add_patch(Rectangle((CAB_X + 60, CAB_Y + 150), 80, 110, facecolor='#AED6F1', edgecolor=C_STEEL, lw=4, zorder=12))
    ax.plot([CAB_X + 60, CAB_X + 130], [CAB_Y + 250, CAB_Y + 150], color='#FFFFFF', lw=4, alpha=0.4, zorder=13)

    ax.add_patch(Rectangle((BOILER_X, BOILER_Y), BOILER_W, BOILER_H, facecolor=C_IRON, edgecolor='#1C2833', lw=5, zorder=10))
    ax.add_patch(Rectangle((BOILER_X, BOILER_Y + BOILER_H*0.7), BOILER_W, BOILER_H*0.15, facecolor='#FFFFFF', alpha=0.1, zorder=11))
    
    for bx in [BOILER_X + 150, BOILER_X + 350, BOILER_X + 550]:
        ax.add_patch(Rectangle((bx, BOILER_Y), 15, BOILER_H, facecolor=C_CABIN, zorder=12))
        ax.add_patch(Circle((bx+7, BOILER_Y-10), 12, facecolor=C_BRASS, zorder=12))

    ax.add_patch(Polygon([(BOILER_X+300, BOILER_Y+BOILER_H), (BOILER_X+400, BOILER_Y+BOILER_H), (BOILER_X+380, BOILER_Y+BOILER_H+80), (BOILER_X+320, BOILER_Y+BOILER_H+80)], facecolor=C_BRASS, edgecolor='#947808', lw=4, zorder=9))
    
    ax.add_patch(Polygon([(STACK_X, STACK_Y), (STACK_X+STACK_W, STACK_Y), (STACK_X+STACK_W+15, STACK_Y+STACK_H), (STACK_X-15, STACK_Y+STACK_H)], facecolor=C_CABIN, edgecolor='#1C2833', lw=4, zorder=10))
    ax.add_patch(Rectangle((STACK_X-25, STACK_Y+STACK_H-20), STACK_W+50, 20, facecolor=C_BRASS, zorder=11))

    ax.add_patch(Polygon([(PILOT_X, BOILER_Y+30), (PILOT_X+120, GROUND_Y+15), (PILOT_X, GROUND_Y+15)], facecolor=C_IRON, edgecolor=C_STEEL, lw=4, zorder=15))

    # 5. THE KINETIC LINKAGE & DRIVE WHEELS (Clockwise Torque)
    pin1_x = W1_X + CRANK_R * np.cos(theta_rad)
    pin1_y = WHEEL_Y + CRANK_R * np.sin(theta_rad)
    pin2_x = W2_X + CRANK_R * np.cos(theta_rad)
    pin2_y = WHEEL_Y + CRANK_R * np.sin(theta_rad)

    for w_x in [W1_X, W2_X]:
        ax.add_patch(Circle((w_x, WHEEL_Y), DRIVE_R, facecolor='#212F3D', edgecolor=C_STEEL, lw=6, zorder=16))
        ax.add_patch(Circle((w_x, WHEEL_Y), DRIVE_R - 18, facecolor='none', edgecolor=C_WHEELS, lw=24, zorder=17))

        for i in range(16):
            sa = np.radians(angle_deg + (i * 360/16))
            sx = w_x + (DRIVE_R - 25) * np.cos(sa)
            sy = WHEEL_Y + (DRIVE_R - 25) * np.sin(sa)
            ax.plot([w_x, sx], [WHEEL_Y, sy], color=C_WHEELS, lw=14, zorder=17)
            ax.plot([w_x, sx], [WHEEL_Y, sy], color='#78281F', lw=4, zorder=18)

        # Counterweight rotates clockwise
        ax.add_patch(Wedge((w_x, WHEEL_Y), DRIVE_R - 25, angle_deg+130, angle_deg+230, width=80, facecolor=C_CABIN, edgecolor='#1C2833', lw=3, zorder=19))
        ax.add_patch(Circle((w_x, WHEEL_Y), 40, facecolor=C_CABIN, zorder=20))
        ax.add_patch(Circle((w_x, WHEEL_Y), 20, facecolor=C_BRASS, zorder=21))

    # Coupling Rod Array
    ax.plot([pin1_x, pin2_x], [pin1_y, pin2_y], color=C_STEEL, lw=28, solid_capstyle='round', zorder=22)
    ax.plot([pin1_x, pin2_x], [pin1_y, pin2_y], color='#FFFFFF', lw=6, alpha=0.5, zorder=23)

    # Main Linkage (Piston offset correctly scales horizontally regardless of clockwise/counter-clock)
    cyl_pin_x = BOILER_X + BOILER_W
    piston_x = cyl_pin_x + CRANK_R * np.cos(theta_rad)
    
    ax.plot([pin2_x, piston_x], [pin2_y, WHEEL_Y], color=C_STEEL, lw=22, solid_capstyle='round', zorder=21)
    ax.plot([pin2_x, piston_x], [pin2_y, WHEEL_Y], color='#FFFFFF', lw=4, alpha=0.5, zorder=22)
    
    ax.add_patch(Rectangle((cyl_pin_x - 30, WHEEL_Y - 40), 120, 80, facecolor=C_CABIN, edgecolor=C_STEEL, lw=4, zorder=10))
    ax.plot([piston_x, cyl_pin_x + 80], [WHEEL_Y, WHEEL_Y], color=C_STEEL, lw=14, zorder=20)

    for p_x, p_y in [(pin1_x, pin1_y), (pin2_x, pin2_y), (piston_x, WHEEL_Y)]:
        ax.add_patch(Circle((p_x, p_y), 22, facecolor=C_CABIN, zorder=24))
        ax.add_patch(Circle((p_x, p_y), 10, facecolor=C_BRASS, zorder=25))

    # 6. O(N) THERMODYNAMIC FLUID TENSOR
    local_age = (phase - p_offsets) % 1.0
    t_age = local_age * DURATION
    
    px = (STACK_X + STACK_W/2) + p_vx * t_age
    py = (STACK_Y + STACK_H) + p_vy * t_age - (0.5 * 25.0 * t_age**2) 
    
    mask = (py > STACK_Y) & (px > -200) & (px < 1200) & (py < 2000)
    
    if np.any(mask):
        m_age = local_age[mask]
        sz = (1.0 + (m_age * 2.0)) * p_sizes[mask]
        
        cmix = p_color_mix[mask][:, None]
        base_colors = cmix * c_st_d + (1 - cmix) * c_st_w
        alphas = np.clip((1.0 - m_age) * 1.5, 0.0, 0.6)
        
        rgba = np.zeros((len(base_colors), 4))
        rgba[:, :3] = base_colors
        rgba[:, 3] = alphas
        
        sort_idx = np.argsort(-sz)
        ax.scatter(px[mask][sort_idx], py[mask][sort_idx], s=sz[sort_idx], color=rgba[sort_idx], edgecolors='none', zorder=26)

    # 7. METRIC WATERMARK 
    ax.text(20, 20, "O(1) MATHEMATICAL LOCOMOTION TENSOR // CLOCKWISE FORWARD VECTOR", color=C_IRON, fontsize=14, fontname='monospace', alpha=0.4, weight='bold', zorder=50)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_SKY, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-191d BEHEMOTH v5: DAYLIGHT PROTOCOL [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Forward Vector Physics Fix // Clockwise Lock")

    with mp.Pool(processes=cpu_cores) as pool:
        frames = range(TOTAL_FRAMES)
        for finished_frame in pool.imap_unordered(render_frame, frames, chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")
    print("Compilation Complete. Absolute Forward Physics achieved.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
