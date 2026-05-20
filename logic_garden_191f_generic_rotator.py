"""
SOVEREIGN CODE: logic_garden_191f_generic_rotator.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Cinematic Slipstream Tensor
SCENE: LG-191f (Generic Heavy Rotator / Forward Vector)
HOTFIX: Right-Facing Kinematics, Generic Industrial Crimson Palette, Seamless Loop
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
OUT_DIR = "frames_191f_generic_rotator"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST HEAVY RESCUE PALETTE --------
C_BG        = '#FFFFFF'        # Pure White Daylight Focus
C_ROAD      = '#2C3E50'        # Asphalt Base
C_LINE      = '#F1C40F'        # Highway Marker Striping
C_PRIMARY   = '#900C3F'        # Industrial Heavy Crimson (Main Body)
C_SEC       = '#BDC3C7'        # Silver Metallic (Trim / Second Stage)
C_STRIPE    = '#C0392B'        # Bright Red Accent Line
C_CHASSIS   = '#1C2833'        # Dark Cast Iron / Lower Frame rails
C_CHROME    = '#E5E7E9'        # High-Gloss Chrome Stacks/Bumpers
C_CHROME_DK = '#95A5A6'        # Shaded Chrome / Hydraulics
C_TIRE      = '#111111'        # Vulcanized Rubber
C_AMBER     = '#F39C12'        # Warning Amber Strobes

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: RIGHT-FACING 50-TON MASTER CHASSIS
# ------------------------------------------------------------------
GROUND_Y = 850.0  
WHEEL_R = 55.0
WHEEL_Y = GROUND_Y + WHEEL_R

# 5-Axle Heavy Configuration (Steer is Front/Right)
AXLE_D4    = 250.0 # Rear-most Tail axle
AXLE_D3    = 375.0
AXLE_D2    = 500.0
AXLE_D1    = 625.0
AXLE_STEER = 925.0 # Front Steer Axle
ALL_AXLES = [AXLE_STEER, AXLE_D1, AXLE_D2, AXLE_D3, AXLE_D4]

# Master Velocity Math
ROTATIONS = 12.0
TOTAL_DISTANCE = ROTATIONS * 2 * np.pi * WHEEL_R
# Math clamp to ensure the highway line spacing perfectly divides the total distance
LINE_SPACING = TOTAL_DISTANCE / 14.0 

# ------------------------------------------------------------------
# O(1) FLAWLESS SLIPSTREAM MATRIX
# ------------------------------------------------------------------
N_SLIP = 600
np.random.seed(1916)
# Ensure slipstream velocities are exact integers of the global distance to modulo cleanly
s_mult = np.random.choice([1.0, 2.0], N_SLIP) 
WRAP_DIST = TOTAL_DISTANCE * 2.0 # Master Wrap scale
sx_base = np.random.uniform(0, WRAP_DIST + 1200, N_SLIP) - 400
sy_base = np.random.uniform(100, 1920, N_SLIP)
s_len = np.random.uniform(50, 250, N_SLIP)

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

    # 1. KINEMATIC MATHEMATICS (Right-Facing Forward Vector)
    # Target goes Right = Earth goes Left. Wheels rotate Clockwise.
    angle_deg = (1.0 - phase) * 360.0 * ROTATIONS
    dist_travelled = phase * TOTAL_DISTANCE

    # 2. RENDER THE ROAD (Seamless leftward translation)
    ax.add_patch(Rectangle((0, 0), 1080, GROUND_Y, facecolor=C_ROAD, zorder=1))
    
    line_offset = dist_travelled % LINE_SPACING
    for i in range(-5, int(1080/LINE_SPACING) + 5):
        lx = (i * LINE_SPACING) - line_offset
        if -200 <= lx <= 1200:
            ax.add_patch(Rectangle((lx, GROUND_Y - 150), LINE_SPACING*0.4, 20, facecolor=C_LINE, zorder=2))

    # Fast Slipstream lines (Atmospheric speed)
    curr_sx = ((sx_base - dist_travelled * s_mult) % WRAP_DIST) - 400
    for i in range(N_SLIP):
        ax.plot([curr_sx[i], curr_sx[i] + s_len[i]], [sy_base[i], sy_base[i]], color=C_CHROME, lw=1.5, alpha=0.3, zorder=3)

    # Ambient chassis shadow
    ax.add_patch(Rectangle((120, GROUND_Y - 40), 900, 40, facecolor='#000000', alpha=0.35, zorder=4))

    # 3. STATIC CHASSIS: THE ROTATOR BODY
    CAB_X = 670.0
    CAB_Y = WHEEL_Y + 30.0

    # Under-chassis frame rails
    ax.add_patch(Rectangle((100, WHEEL_Y - 10), 850, 30, facecolor=C_CHASSIS, zorder=10))
    # Underside fuel payload & Toolboxes
    ax.add_patch(Rectangle((700, WHEEL_Y-20), 100, 40, facecolor=C_CHROME, edgecolor=C_CHASSIS, lw=2, zorder=11))
    ax.add_patch(Rectangle((450, WHEEL_Y-20), 150, 35, facecolor=C_PRIMARY, edgecolor=C_CHASSIS, lw=2, zorder=11))

    # Rear Underlift (Stinger) Folded up
    ax.add_patch(Rectangle((100, WHEEL_Y - 15), 100, 25, facecolor=C_CHROME_DK, edgecolor=C_CHASSIS, lw=2, zorder=12))
    ax.add_patch(Polygon([(80, WHEEL_Y), (110, WHEEL_Y), (110, WHEEL_Y+30)], facecolor=C_CHASSIS, zorder=13))

    # Main Wrecker Body (Houses the rear 4 axles)
    BODY_X, BODY_W, BODY_H = 150.0, 500.0, 140.0
    ax.add_patch(Rectangle((BODY_X, CAB_Y), BODY_W, BODY_H, facecolor=C_PRIMARY, edgecolor=C_CHASSIS, lw=3, zorder=14))
    # Body Accents (Silver Slash)
    ax.add_patch(Polygon([(BODY_X+50, CAB_Y), (BODY_X+250, CAB_Y+BODY_H), (BODY_X+450, CAB_Y+BODY_H), (BODY_X+250, CAB_Y)], facecolor=C_SEC, zorder=15))
    ax.add_patch(Polygon([(BODY_X+100, CAB_Y), (BODY_X+300, CAB_Y+BODY_H), (BODY_X+320, CAB_Y+BODY_H), (BODY_X+120, CAB_Y)], facecolor=C_STRIPE, zorder=16))

    # Cab / Sleeper Profile (Conventional Rig)
    ax.add_patch(Polygon([(CAB_X, CAB_Y), (CAB_X+200, CAB_Y), (CAB_X+200, CAB_Y+240), (CAB_X+30, CAB_Y+240)], facecolor=C_PRIMARY, edgecolor=C_CHASSIS, lw=3, zorder=15))
    
    # Hood Profile (Long Nose, faces Right)
    HOOD_Y_TOP = CAB_Y + 110
    ax.add_patch(Polygon([(CAB_X+200, CAB_Y), (CAB_X+200, HOOD_Y_TOP+10), (CAB_X+350, HOOD_Y_TOP-10), (CAB_X+350, CAB_Y)], facecolor=C_PRIMARY, edgecolor=C_CHASSIS, lw=3, zorder=16))
    # Silver Hood stripe connecting from body
    ax.add_patch(Polygon([(CAB_X+200, CAB_Y+40), (CAB_X+200, CAB_Y+80), (CAB_X+300, CAB_Y+20)], facecolor=C_SEC, zorder=17))

    # Front Grille & Heavy Bumper
    ax.add_patch(Rectangle((CAB_X+340, CAB_Y), 30, 110, facecolor=C_CHROME, edgecolor=C_CHASSIS, lw=2, zorder=18))
    ax.add_patch(Rectangle((CAB_X+330, CAB_Y-25), 60, 35, facecolor=C_CHROME, edgecolor=C_CHASSIS, lw=3, zorder=19)) # Bumper

    # Side Window Area
    WIN_BOT, WIN_TOP, WIN_BACK, WIN_FRONT = CAB_Y + 130, CAB_Y + 220, CAB_X + 40, CAB_X + 170
    ax.add_patch(Polygon([(WIN_BACK, WIN_BOT), (WIN_FRONT, WIN_BOT), (WIN_FRONT, WIN_TOP), (WIN_BACK+30, WIN_TOP)], facecolor='#7FB3D5', edgecolor=C_SEC, lw=3, alpha=0.9, zorder=20))
    ax.plot([WIN_BACK+40, WIN_FRONT-20], [WIN_BOT+10, WIN_TOP-10], color='#FFFFFF', lw=4, alpha=0.6, zorder=21) # Window Reflection

    # Warning Light Bar (Amber strobes mapping to Phase logic)
    bar_glow = C_AMBER if (int(f / 8) % 2 == 0) else '#B9770E'
    ax.add_patch(Rectangle((CAB_X + 80, CAB_Y + 240), 80, 15, facecolor=bar_glow, edgecolor=C_CHASSIS, lw=2, zorder=25))

    # Exhaust Stacks (Behind the Cab)
    ax.add_patch(Rectangle((CAB_X - 40, CAB_Y + 100), 30, 240, facecolor=C_CHROME, edgecolor=C_CHASSIS, lw=2, zorder=25))
    ax.add_patch(Rectangle((CAB_X - 35, CAB_Y + 100), 5, 240, facecolor='#FFFFFF', alpha=0.7, zorder=26)) # Highlight

    # 4. HEAVY ROTATOR BOOM (Angled UP/LEFT)
    TURRET_X = BODY_X + 250
    # Turret Base ring
    ax.add_patch(Rectangle((TURRET_X, CAB_Y + BODY_H), 120, 30, facecolor=C_CHROME_DK, edgecolor=C_CHASSIS, lw=3, zorder=10))
    # Main Base Boom Stage
    boom_end_x, boom_end_y = TURRET_X - 150, CAB_Y + BODY_H + 180
    ax.add_patch(Polygon([(TURRET_X+20, CAB_Y + BODY_H + 30), (TURRET_X+100, CAB_Y + BODY_H + 30), (boom_end_x+50, boom_end_y), (boom_end_x, boom_end_y-20)], facecolor=C_PRIMARY, edgecolor=C_CHASSIS, lw=3, zorder=12))
    # Second Stage Boom (Telescoped outward)
    ax.add_patch(Polygon([(boom_end_x+10, boom_end_y-15), (boom_end_x+40, boom_end_y-5), (boom_end_x-100, boom_end_y+70), (boom_end_x-130, boom_end_y+50)], facecolor=C_SEC, edgecolor=C_CHASSIS, lw=3, zorder=11))
    
    # Massive Chrome Hydraulic Lift Rams
    ax.add_patch(Polygon([(TURRET_X-20, CAB_Y + BODY_H + 10), (TURRET_X, CAB_Y + BODY_H + 10), (boom_end_x+20, boom_end_y-40), (boom_end_x, boom_end_y-50)], facecolor=C_CHROME_DK, edgecolor=C_CHASSIS, zorder=13))

    # 5. KINEMATICS: THE 5-AXLE MATRIX (Clockwise Torque)
    for index, w_x in enumerate(ALL_AXLES):
        # Fenders (Except Front Steer)
        if w_x != AXLE_STEER:
            ax.add_patch(Wedge((w_x, WHEEL_Y), WHEEL_R+20, 0, 180, facecolor=C_CHASSIS, zorder=17))
            ax.add_patch(Wedge((w_x, WHEEL_Y), WHEEL_R+15, 0, 180, facecolor=C_SEC, zorder=18))
        else:
            # Drop steer fender
            ax.add_patch(Wedge((w_x, WHEEL_Y), WHEEL_R+20, 45, 180, facecolor=C_PRIMARY, edgecolor=C_CHASSIS, lw=2, zorder=17))

        # Core Rubber Base
        ax.add_patch(Circle((w_x, WHEEL_Y), WHEEL_R, facecolor=C_TIRE, zorder=19))
        ax.add_patch(Circle((w_x, WHEEL_Y), WHEEL_R-15, facecolor=C_CHROME_DK, edgecolor=C_CHASSIS, lw=2, zorder=20))

        # Precision 10-Lug Simulation
        for lug in range(10):
            sa = np.radians(angle_deg + (lug * 360/10))
            sx = w_x + (WHEEL_R - 25) * np.cos(sa)
            sy = WHEEL_Y + (WHEEL_R - 25) * np.sin(sa)
            # Add motion blur elongation based on speed radius
            ax.add_patch(Circle((sx, sy), 5, facecolor=C_BG, edgecolor=C_CHASSIS, lw=1, zorder=21))

        # Center Chrome Hub
        hub_scale = 18 if w_x == AXLE_STEER else 22
        ax.add_patch(Circle((w_x, WHEEL_Y), hub_scale, facecolor=C_CHROME, edgecolor=C_CHASSIS, lw=2, zorder=22))
        ax.add_patch(Circle((w_x, WHEEL_Y), 6, facecolor=C_CHASSIS, zorder=23))

    # 6. METRIC WATERMARK (Rigid Engineering Telemetry)
    ax.text(30, 20, "LG-191f: FORWARD KINEMATICS // 50-TON ROTATOR ARRAY", color=C_CHASSIS, fontsize=14, fontname='monospace', alpha=0.6, weight='bold', zorder=50)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-191f GENERIC HEAVY ROTATOR [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Forward Vector Kinematics // Clockwise Modulo Lock")

    with mp.Pool(processes=cpu_cores) as pool:
        frames = range(TOTAL_FRAMES)
        for finished_frame in pool.imap_unordered(render_frame, frames, chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")
    print("Compilation Complete. Absolute Forward physics deployed.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
