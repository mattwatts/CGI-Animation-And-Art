"""
SOVEREIGN CODE: logic_garden_191_kinetic_behemoth.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Cinematic Slipstream Tensor (17.5 seconds)
SCENE: Logic Garden 191 v2 (The Kinetic Behemoth)
HOTFIX: Kinematic Phase Inversion (Clockwise Forward Vector)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_191_behemoth"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'        # Deep Night Sky
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'        # Heavy Iron Frame / Telemetry Base
C_IRON      = '#1A1A24'        # Heavy Boiler Cast Iron
C_BRASS     = '#B5A642'        # Polished Brass Fittings
C_CYAN      = '#00FFFF'        # Atmospheric Slipstream
C_MAGENTA   = '#FF0055'        # High-Pressure Live Steam / Embers
C_GOLD      = '#FFD700'        # Drive Linkage
C_RED       = '#FF0033'        # Friction Overload Overdraw
C_MANTIS    = '#00FF00'        # Terminal Geometry (Tathata)

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_mag   = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_cy    = np.array(hex_to_rgba(C_CYAN)[:3])
c_smoke = np.array(hex_to_rgba('#444455')[:3])

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE KINEMATIC ARCHITECTURE
# ------------------------------------------------------------------
MAX_PARTICLES = 25000
MAX_SLIP_LINES = 500

# Base Track Geometry
GROUND_Y = 500.0

# Locomotive Geometry
DRIVE_R = 150.0
WHEEL_Y = GROUND_Y + DRIVE_R
W1_X = 350.0
W2_X = 650.0
CRANK_R = 75.0

BOILER_X = 150.0
BOILER_Y = WHEEL_Y + 50.0
BOILER_W = 700.0
BOILER_H = 220.0

CAB_X = BOILER_X - 100.0
CAB_Y = BOILER_Y
CAB_W = 180.0
CAB_H = 350.0

STACK_X = BOILER_X + BOILER_W - 80.0
STACK_Y = BOILER_Y + BOILER_H
STACK_W = 60.0
STACK_H = 120.0

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, px, py, p_sizes, c_tensor, sx, sy, s_len, angle_deg, track_offset, vel_mult, is_flash, is_tathata, bg_strobe = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    bg = C_TEXT if is_flash else C_VOID
    if bg_strobe and not is_tathata: bg = '#0A0A10'
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)
    ax.set_xlim(0, 1080); ax.set_ylim(0, 1920)

    theta_rad = np.radians(angle_deg)
    pin1_x = W1_X + CRANK_R * np.cos(theta_rad)
    pin1_y = WHEEL_Y + CRANK_R * np.sin(theta_rad)
    pin2_x = W2_X + CRANK_R * np.cos(theta_rad)
    pin2_y = WHEEL_Y + CRANK_R * np.sin(theta_rad)

    # 1. RENDER BACKGROUND SLIPSTREAM & TRACK
    if not is_flash and not is_tathata:
        # Slipstream Vectors
        ax.plot([sx, sx + s_len], [sy, sy], color=C_CYAN, alpha=0.15, lw=1)
        
        # Earth & Track
        ax.add_patch(Rectangle((0, 0), 1080, GROUND_Y, facecolor='#05050A', zorder=1))
        ax.axhline(GROUND_Y, color=C_DIM, lw=8, zorder=2)
        ax.axhline(GROUND_Y + 5, color=C_TEXT, lw=2, alpha=0.3, zorder=2)

        # Rushing Sleepers (Translating chaos to velocity)
        for i in range(-5, 20):
            sleep_x = (i * 80) - track_offset
            if -100 <= sleep_x <= 1180:
                ax.add_patch(Rectangle((sleep_x, GROUND_Y - 20), 30, 20, facecolor=C_TEXT, alpha=0.4, zorder=3))

    # 2. RENDER THE LOCOMOTIVE
    if not is_flash and not is_tathata:
        # Boiler
        ax.add_patch(Rectangle((BOILER_X, BOILER_Y), BOILER_W, BOILER_H, facecolor=C_IRON, edgecolor=C_TEXT, lw=2, zorder=10))
        # Gradient highlight on boiler
        ax.add_patch(Rectangle((BOILER_X, BOILER_Y + BOILER_H*0.7), BOILER_W, BOILER_H*0.1, facecolor=C_TEXT, alpha=0.1, zorder=11))
        
        # Cab
        ax.add_patch(Rectangle((CAB_X, CAB_Y), CAB_W, CAB_H, facecolor=C_IRON, edgecolor=C_TEXT, lw=2, zorder=9))
        # Cab Window
        ax.add_patch(Rectangle((CAB_X + 80, CAB_Y + 150), 60, 100, facecolor=C_MAGENTA, alpha=0.3, edgecolor=C_GOLD, lw=2, zorder=11))
        
        # Smoke Stack
        ax.add_patch(Polygon([[STACK_X, STACK_Y], [STACK_X + STACK_W, STACK_Y], 
                              [STACK_X + STACK_W + 20, STACK_Y + STACK_H], [STACK_X - 20, STACK_Y + STACK_H]], 
                             facecolor=C_IRON, edgecolor=C_TEXT, lw=2, zorder=10))

    # 3. KINEMATIC DRIVE (The Bounding Boxes of Pi)
    link_c = C_GOLD if not is_tathata else C_MANTIS
    if is_flash: link_c = C_VOID

    for w_x in [W1_X, W2_X]:
        if not is_tathata and not is_flash:
            # Drive Wheels
            ax.add_patch(Circle((w_x, WHEEL_Y), DRIVE_R, facecolor=C_VOID, edgecolor=C_IRON, lw=15, zorder=12))
            ax.add_patch(Circle((w_x, WHEEL_Y), DRIVE_R-15, facecolor=C_VOID, edgecolor=C_TEXT, lw=2, alpha=0.5, zorder=13))
            ax.add_patch(Circle((w_x, WHEEL_Y), 20, facecolor=C_BRASS, zorder=14))
            
            # Spokes
            for i in range(12):
                sa = np.radians(angle_deg + (i * 360/12))
                sx_pos = w_x + (DRIVE_R-20) * np.cos(sa)
                sy_pos = WHEEL_Y + (DRIVE_R-20) * np.sin(sa)
                ax.plot([w_x, sx_pos], [WHEEL_Y, sy_pos], color=C_IRON, lw=8, zorder=13)
        
    # Coupling Rods
    if not is_flash:
        ax.plot([pin1_x, pin2_x], [pin1_y, pin2_y], color=link_c, lw=20, zorder=15)
        ax.plot([pin1_x, pin2_x], [pin1_y, pin2_y], color=C_TEXT if not is_tathata else C_VOID, lw=4, alpha=0.5, zorder=16)
        
        # Main Drag Rod (To imaginary cylinder off-screen right)
        cyl_pin_x = W2_X + 250 + CRANK_R * np.cos(theta_rad)
        ax.plot([pin2_x, cyl_pin_x], [pin2_y, WHEEL_Y], color=link_c, lw=16, zorder=14)

        # Pins
        for p_x, p_y in [(pin1_x, pin1_y), (pin2_x, pin2_y)]:
            ax.add_patch(Circle((p_x, p_y), 25, facecolor=C_IRON, edgecolor=link_c, lw=4, zorder=17))
            ax.add_patch(Circle((p_x, p_y), 8, facecolor=C_TEXT, zorder=18))

    # 4. O(N) THERMODYNAMIC FLUID TENSOR (Steam/Smoke)
    if len(px) > 0 and not is_tathata:
        ax.scatter(px, py, s=p_sizes*4.0, c=c_tensor, edgecolors='none', alpha=0.3, zorder=6)
        ax.scatter(px, py, s=p_sizes*1.2, c=C_MAGENTA if vel_mult > 3.0 and not is_flash else c_tensor, edgecolors='none', alpha=0.7, zorder=7)

    # Tathata Geometry Rewrite
    if is_tathata and not is_flash:
        ax.axhline(GROUND_Y, color=C_MANTIS, lw=2, linestyle=':', zorder=5)
        ax.add_patch(Circle((W1_X, WHEEL_Y), DRIVE_R, fill=False, edgecolor=C_MANTIS, lw=4, zorder=20))
        ax.add_patch(Circle((W2_X, WHEEL_Y), DRIVE_R, fill=False, edgecolor=C_MANTIS, lw=4, zorder=20))
        ax.add_patch(Circle((W1_X, WHEEL_Y), CRANK_R, fill=False, edgecolor=C_MANTIS, lw=2, linestyle='--', alpha=0.5, zorder=20))
        ax.add_patch(Circle((W2_X, WHEEL_Y), CRANK_R, fill=False, edgecolor=C_MANTIS, lw=2, linestyle='--', alpha=0.5, zorder=20))
        ax.plot([0, 1080], [STACK_Y + STACK_H, STACK_Y + STACK_H], color=C_MANTIS, linestyle=':', alpha=0.3)

    # 5. TELEMETRY WIDGETS
    ui_col = C_CYAN if not is_tathata else C_MANTIS
    txt_col = C_TEXT if not is_flash else C_VOID
    bg_col  = C_VOID if not is_flash else C_TEXT

    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=bg_col, alpha=0.9, zorder=80))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    ax.text(0.04, 0.965, "LG-191 v2 :: KINETIC BEHEMOTH TENSOR", transform=ax.transAxes, color=txt_col, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=81)

    ax.add_patch(plt.Rectangle((0, 0), 1.0, 0.12, transform=ax.transAxes, color=bg_col, alpha=0.95, zorder=80))
    ax.plot([0, 1.0], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)

    velocity = vel_mult * 45.0
    ax.text(0.04, 0.08, f"LINE VELOCITY EXHAUST | MPH: {velocity:05.1f}", transform=ax.transAxes, color=txt_col, fontsize=20, fontname='monospace', zorder=81)

    # Heat Load Bar
    ax.add_patch(plt.Rectangle((0.72, 0.03), 0.25, 0.02, transform=ax.transAxes, color=C_DIM, zorder=80))
    bar_fill = min(1.0, vel_mult / 5.0)
    bar_color = C_MAGENTA if vel_mult > 3.0 else ui_col
    if vel_mult > 4.5: bar_color = C_RED
    if is_flash: bar_color = C_VOID
    if is_tathata: bar_color = C_MANTIS

    ax.add_patch(plt.Rectangle((0.72, 0.03), 0.25 * bar_fill, 0.02, transform=ax.transAxes, color=bar_color, zorder=81))

    pulse = ui_col if (f % 10 < 5) and not is_flash else txt_col
    if vel_mult > 4.0 and not is_tathata and f % 4 < 2: pulse = C_RED
    if is_flash: pulse = C_VOID
    if is_tathata and not is_flash: pulse = C_MANTIS

    ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=24, fontname='monospace', weight='bold', zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# O(1) TENSOR KINEMATICS STREAM
# ------------------------------------------------------------------
def generate_stream():
    px = np.zeros(MAX_PARTICLES)
    py = np.zeros(MAX_PARTICLES)
    vx = np.zeros(MAX_PARTICLES)
    vy = np.zeros(MAX_PARTICLES)
    p_life = np.zeros(MAX_PARTICLES)

    sx = np.random.uniform(0, 1080, MAX_SLIP_LINES)
    sy = np.random.uniform(0, 1920, MAX_SLIP_LINES)
    s_len = np.zeros(MAX_SLIP_LINES)

    spawn_idx = 0
    angle_deg = 0.0
    global_dist = 0.0

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS

        is_flash = False
        is_tathata = False
        bg_strobe = False
        vel_mult = 0.0
        
        # ---- PHASE 1: IDLE / BUILD PRESSURE (0 - 3s) ----
        if t_sec < 3.0:
            state = "[01] BOILER SATURATION :: PRESSURE BUILDING"
            vel_mult = 0.1 # Very slow roll

        # ---- PHASE 2: ACCELERATION & SLIPSTREAM (3 - 10s) ----
        elif t_sec < 10.0:
            state = "[02] THERMODYNAMIC TRANSLATION :: THE FORWARD VECTOR"
            prog = (t_sec - 3.0) / 7.0
            vel_mult = 0.1 + (prog**1.5 * 3.4)

        # ---- PHASE 3: TERMINAL KINETICS (10 - 14.8s) ----
        elif t_sec < 14.8:
            state = "WARNING: MAXIMUM AERODYNAMIC DRAG. STRUCTURAL STRESS."
            prog = (t_sec - 10.0) / 4.8
            vel_mult = 3.5 + (prog * 1.5)
            if t_sec > 13.5: bg_strobe = True

        # ---- PHASE 4: TATHĀTĀ / GEOMETRIC EXTRACTION (14.8 - 17.5s) ----
        else:
            is_tathata = True
            vel_mult = 2.0 
            if t_sec < 14.95:
                is_flash = True
            state = "TATHĀTĀ: TO MOVE FORWARD, YOU PULL THE EARTH BACKWARDS."

        # Kinematic Updates (The Engine drives the World)
        # linear distance = theta_radians * R
        delta_angle = 3.5 * vel_mult
        
        # HOTFIX: KINEMATIC PHASE INVERSION (CLOCKWISE FORWARD VECTOR)
        # Subtracting the angle forces a right-hand clockwise rotation, matching correct forward kinematics.
        angle_deg = (angle_deg - delta_angle) % 360.0 
        
        linear_v = np.radians(delta_angle) * DRIVE_R
        global_dist += linear_v
        
        track_offset = global_dist % 80.0

        # Slipstream Vectors
        sx -= linear_v * 0.8
        s_len[:] = linear_v * 1.5
        wrap_mask = sx < -200
        sx[wrap_mask] = 1080 + np.random.uniform(0, 500, np.sum(wrap_mask))

        # Thermodynamics / Steam
        theta_rad = np.radians(angle_deg)
        # Chuff logic: occurs roughly when crank is parallel 
        is_chuff = abs(np.sin(theta_rad)) < 0.2 and not is_tathata

        spawns = int(250 * vel_mult) if is_chuff else int(20 * vel_mult)
        spawns = min(spawns, MAX_PARTICLES - spawn_idx)

        if spawns > 0 and spawn_idx < MAX_PARTICLES:
            ex_x = STACK_X + (STACK_W/2)
            ex_y = STACK_Y + STACK_H

            px[spawn_idx:spawn_idx+spawns] = ex_x + np.random.uniform(-10, 10, spawns)
            py[spawn_idx:spawn_idx+spawns] = ex_y + np.random.uniform(0, 10, spawns)

            # Ejection speed is high upward
            v_blow = 25.0 * vel_mult if is_chuff else 8.0
            vx[spawn_idx:spawn_idx+spawns] = np.random.uniform(-2, 2, spawns) - (linear_v * 0.4) # Wind drag pulls it back
            vy[spawn_idx:spawn_idx+spawns] = np.random.uniform(v_blow*0.8, v_blow*1.2, spawns)

            p_life[spawn_idx:spawn_idx+spawns] = 1.0
            spawn_idx += spawns

        # Global Physical Matrix
        active = p_life > 0
        if np.any(active):
            px[active] += vx[active]
            py[active] += vy[active]

            # Heavy slipstream drag
            vx[active] -= (linear_v * 0.05) # Persistent backward force
            vy[active] -= 0.1 # Gravity pulls the heavier carbon particles down
            vx[active] *= 0.98
            vy[active] *= 0.98

            p_life[active] -= 0.015

        # Memory Cleanup Matrix
        if spawn_idx > MAX_PARTICLES - 1500:
            act_idx = np.where(active)[0]
            cnt = len(act_idx)
            px[:cnt] = px[act_idx]
            py[:cnt] = py[act_idx]
            vx[:cnt] = vx[act_idx]
            vy[:cnt] = vy[act_idx]
            p_life[:cnt] = p_life[act_idx]
            p_life[cnt:] = 0
            spawn_idx = cnt

        # Chromatic Mapping
        active_cnt = np.sum(p_life > 0)
        c_tensor = np.zeros((active_cnt, 3))
        p_sizes = np.zeros(active_cnt)

        if active_cnt > 0:
            lives = np.clip(p_life[p_life > 0][:, None], 0.0, 1.0)
            
            # Start bright Magenta (Heat), rapidly cool to dense Carbon smoke
            c_tensor = lives * c_mag + (1 - lives) * c_smoke
            if vel_mult > 3.0: 
                # Add intense Cyan burn at terminal velocities
                c_tensor = np.where(lives > 0.8, c_cy, c_tensor)
                
            c_tensor = np.clip(c_tensor, 0.0, 1.0)
            p_sizes = 2.0 + (1.0 - lives.flatten()) * 30.0 # Smoke expands as it cools

        yield (f, t_sec, state, np.copy(px[p_life > 0]), np.copy(py[p_life > 0]), p_sizes, c_tensor, np.copy(sx), np.copy(sy), np.copy(s_len), angle_deg, track_offset, vel_mult, is_flash, is_tathata, bg_strobe)

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 191 v2: THE KINETIC BEHEMOTH [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Kinematic Phase Inversion (Clockwise Rotation)")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Nodes: {MAX_PARTICLES}")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
