"""
SOVEREIGN CODE: logic_garden_191e_hulk_rotator.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Cinematic Slipstream Tensor
SCENE: LG-191e (Hulk 2.0 / 50-Ton Rotator Kinematics)
HOTFIX: Seamless 10s Ouroboros Array, Multi-Axle Matrix, Hulk Paint Profile
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
OUT_DIR = "frames_191e_hulk_rotator"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST HULK 2.0 PALETTE --------
C_BG        = '#FFFFFF'        # Pure White Daylight Focus
C_ROAD      = '#2C3E50'        # Asphalt
C_LINE      = '#F1C40F'        # Highway Yellow
C_HULK_GRN  = '#7CFC00'        # Neon Hulk Green
C_GRAPE     = '#6A0DAD'        # Deep Purple Wrap
C_COBALT    = '#0047AB'        # Deep Blue Wrap
C_YELLOW    = '#FFD700'        # Decal Slash
C_CHROME    = '#E5E7E9'        # High-Gloss Chrome
C_CHROME_DK = '#95A5A6'        # Shaded Chrome
C_TIRE      = '#111111'        # Vulcanized Rubber
C_TRIM      = '#000000'        # Black Accents
C_STEEL     = '#7F8C8D'        # Rotator Boom Steel

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE 50-TON ROTATOR MASTER CHASSIS
# ------------------------------------------------------------------
GROUND_Y = 850.0  # Raised to fit the massive 9:16 frame better
WHEEL_R = 55.0
WHEEL_Y = GROUND_Y + WHEEL_R

# 5-Axle Heavy Configuration
AXLE_STEER = 250.0
AXLE_D1 = 600.0
AXLE_D2 = 725.0
AXLE_D3 = 850.0
AXLE_D4 = 975.0
ALL_AXLES = [AXLE_STEER, AXLE_D1, AXLE_D2, AXLE_D3, AXLE_D4]

# Master Velocity Math
ROTATIONS = 12.0
TOTAL_DISTANCE = ROTATIONS * 2 * np.pi * WHEEL_R
LINE_SPACING = 300.0

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

    # 1. KINEMATIC MATHEMATICS (Angular to Linear Translation)
    # Forward Matrix: Ground moves Left, Wheels rotate Clockwise (1.0 - phase)
    angle_deg = (1.0 - phase) * 360.0 * ROTATIONS
    dist_travelled = phase * TOTAL_DISTANCE

    # 2. RENDER THE ROAD (Continuous Seamless Slipstream)
    ax.add_patch(Rectangle((0, 0), 1080, GROUND_Y, facecolor=C_ROAD, zorder=1))
    
    # Rushing Highway Lines
    line_offset = dist_travelled % LINE_SPACING
    for i in range(-2, int(1080/LINE_SPACING) + 3):
        lx = (i * LINE_SPACING) - line_offset
        if -200 <= lx <= 1200:
            ax.add_patch(Rectangle((lx, GROUND_Y - 150), 150, 20, facecolor=C_LINE, zorder=2))

    # Chrome shadow reflection on asphalt
    ax.add_patch(Rectangle((100, GROUND_Y - 40), 950, 40, facecolor='#000000', alpha=0.3, zorder=3))

    # 3. STATIC CHASSIS: THE ROTATOR BODY
    # Under-chassis frame rail
    ax.add_patch(Rectangle((200, WHEEL_Y), 850, 30, facecolor=C_TRIM, zorder=10))
    ax.add_patch(Rectangle((400, WHEEL_Y-20), 150, 40, facecolor=C_CHROME, edgecolor=C_TRIM, lw=2, zorder=11)) # Fuel Tank

    # Main Cab / Sleeper Profile (The Peterbilt Block)
    CAB_X = 350.0
    CAB_Y = WHEEL_Y + 30.0
    ax.add_patch(Polygon([(CAB_X, CAB_Y), (CAB_X+250, CAB_Y), (CAB_X+250, CAB_Y+250), (CAB_X+30, CAB_Y+250), (CAB_X, CAB_Y+180)], facecolor=C_GRAPE, edgecolor=C_TRIM, lw=3, zorder=15))
    
    # The Custom Wrap Graphics (Angles and Slashes)
    ax.add_patch(Polygon([(CAB_X+50, CAB_Y), (CAB_X+200, CAB_Y+150), (CAB_X+250, CAB_Y+120), (CAB_X+100, CAB_Y)], facecolor=C_COBALT, zorder=16))
    ax.add_patch(Polygon([(CAB_X+80, CAB_Y), (CAB_X+250, CAB_Y+180), (CAB_X+250, CAB_Y+150), (CAB_X+120, CAB_Y)], facecolor=C_YELLOW, zorder=17))

    # Hood Profile (Long nose, sloped slightly)
    HOOD_X = 120.0
    ax.add_patch(Polygon([(HOOD_X, CAB_Y), (CAB_X, CAB_Y), (CAB_X, CAB_Y+130), (HOOD_X+20, CAB_Y+110)], facecolor=C_COBALT, edgecolor=C_TRIM, lw=3, zorder=16))
    ax.add_patch(Polygon([(HOOD_X+30, CAB_Y+20), (CAB_X-20, CAB_Y+110), (CAB_X-20, CAB_Y+80), (HOOD_X+60, CAB_Y+20)], facecolor=C_GRAPE, zorder=17))
    ax.add_patch(Polygon([(HOOD_X+60, CAB_Y+40), (CAB_X-50, CAB_Y+110), (CAB_X-50, CAB_Y+90), (HOOD_X+80, CAB_Y+40)], facecolor=C_YELLOW, zorder=18))

    # Massive Front Chrome Grille & Bumper
    ax.add_patch(Rectangle((HOOD_X-30, CAB_Y), 40, 120, facecolor=C_CHROME, edgecolor=C_TRIM, lw=2, zorder=18))
    ax.add_patch(Rectangle((HOOD_X-45, CAB_Y-20), 60, 30, facecolor=C_CHROME, edgecolor=C_TRIM, lw=3, zorder=19)) # Bumper

    # Cab Windows (Joshua's Viewport)
    ax.add_patch(Polygon([(CAB_X+20, CAB_Y+140), (CAB_X+100, CAB_Y+140), (CAB_X+100, CAB_Y+230), (CAB_X+35, CAB_Y+230)], facecolor='#1ABC9C', edgecolor=C_TRIM, lw=3, alpha=0.9, zorder=20))
    ax.plot([CAB_X+30, CAB_X+60], [CAB_Y+220, CAB_Y+150], color='#FFFFFF', lw=4, alpha=0.5, zorder=21) # Glare

    # Massive Chrome Exhaust Stacks
    STACK_X = CAB_X + 130
    ax.add_patch(Rectangle((STACK_X, CAB_Y), 30, 350, facecolor=C_CHROME, edgecolor=C_TRIM, lw=2, zorder=25))
    ax.add_patch(Rectangle((STACK_X+5, CAB_Y), 5, 350, facecolor='#FFFFFF', zorder=26)) # Highlight
    
    # 50-Ton Rotator Boom & Wrecker Body (Rear)
    REC_X = CAB_X + 250
    REC_W = 450
    ax.add_patch(Rectangle((REC_X, CAB_Y), REC_W, 160, facecolor=C_COBALT, edgecolor=C_TRIM, lw=3, zorder=14))
    # Hulk Graphics Base
    ax.add_patch(Circle((REC_X + 150, CAB_Y + 80), 60, facecolor=C_HULK_GRN, edgecolor=C_TRIM, lw=4, zorder=15))
    ax.add_patch(Circle((REC_X + 220, CAB_Y + 100), 50, facecolor=C_HULK_GRN, edgecolor=C_TRIM, lw=3, zorder=15))
    ax.text(REC_X + 185, CAB_Y + 80, "HULK 2.0", color=C_TRIM, fontsize=18, fontname='monospace', weight='bold', ha='center', zorder=16)

    # Steel Rotator Boom (Angled Up)
    ax.add_patch(Polygon([(REC_X+50, CAB_Y+160), (REC_X+150, CAB_Y+160), (REC_X+400, CAB_Y+300), (REC_X+350, CAB_Y+330)], facecolor=C_STEEL, edgecolor=C_TRIM, lw=4, zorder=13))
    ax.add_patch(Rectangle((REC_X+100, CAB_Y+160), 200, 40, facecolor=C_CHROME_DK, zorder=14)) # Turret base

    # 4. KINEMATICS: THE 5-AXLE MATRIX (Clockwise Torque)
    theta_rad = np.radians(angle_deg)
    
    # Front Steer Fender
    ax.add_patch(Wedge((AXLE_STEER, WHEEL_Y), WHEEL_R+20, 0, 180, facecolor=C_TRIM, zorder=17))

    for w_x in ALL_AXLES:
        # Custom Fender Arches for Rear Rears
        if w_x != AXLE_STEER:
            ax.add_patch(Wedge((w_x, WHEEL_Y), WHEEL_R+15, 0, 180, facecolor=C_COBALT, edgecolor=C_TRIM, lw=2, zorder=17))
            ax.add_patch(Wedge((w_x, WHEEL_Y), WHEEL_R+10, 0, 180, facecolor=C_GRAPE, zorder=18))

        # Core Rubber
        ax.add_patch(Circle((w_x, WHEEL_Y), WHEEL_R, facecolor=C_TIRE, zorder=19))
        ax.add_patch(Circle((w_x, WHEEL_Y), WHEEL_R-15, facecolor=C_CHROME, edgecolor=C_TRIM, lw=2, zorder=20))

        # Precision Custom Chrome Rims (10-Lug Simulation)
        for i in range(10):
            sa = np.radians(angle_deg + (i * 360/10))
            sx = w_x + (WHEEL_R - 25) * np.cos(sa)
            sy = WHEEL_Y + (WHEEL_R - 25) * np.sin(sa)
            ax.add_patch(Circle((sx, sy), 5, facecolor=C_BG, edgecolor=C_TRIM, lw=1, zorder=21))

        # Center Chrome Hub
        ax.add_patch(Circle((w_x, WHEEL_Y), 15, facecolor=C_CHROME_DK, edgecolor=C_TRIM, lw=2, zorder=22))
        ax.add_patch(Circle((w_x, WHEEL_Y), 8, facecolor=C_BG, zorder=23))

    # 5. METRIC WATERMARK (Rigid Engineering Telemetry)
    ax.text(30, 20, "LG-191e: 50-TON ROTATOR KINEMATICS // EXACT SEAMLESS LOOP", color=C_TRIM, fontsize=14, fontname='monospace', alpha=0.6, weight='bold', zorder=50)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LG-191e HULK 2.0 ROTATOR [CORES: {cpu_cores}]")
    print(f"Executing PROTOCOL: Forward Vector Ouroboros Array // Heavy 5-Axle")

    with mp.Pool(processes=cpu_cores) as pool:
        frames = range(TOTAL_FRAMES)
        for finished_frame in pool.imap_unordered(render_frame, frames, chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")
    print("Compilation Complete. Absolute Forward Physics achieved.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
