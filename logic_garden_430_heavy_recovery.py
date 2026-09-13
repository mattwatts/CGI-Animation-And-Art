"""
PROJECT: Logic Garden 430 (Exact Physical Construct // Heavy Recovery Matrix)
FORMAT: YouTube Shorts (1080x1920)
METADATA: KINEMATICS, DEADMAN ANCHOR, COUNTERWEIGHT, DAYLIGHT
EXECUTION: 24.0s Sequence. 3-Phase Failure & Resolution Demonstration.
RULES ENFORCED: 
- O(1) Kinematic Rotation vectors tracking Center of Gravity (CoG).
- Mathematical fluid/stress spallation for frictional translation.
- Daylight Palette (White Substrate / High-Contrast Edge Geometry).
- Purged Jargon. Australian spelling conventions.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcol
import multiprocessing as mp
import os
import gc

# ======== SEQUENCE PARAMETERS ========
DURATION = 24.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_430_recovery"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'          # Indestructible Black UI
C_BEDROCK   = '#F8FAFC'          # Clinical Light Grey Earth
C_TRENCH    = '#E2E8F0'          # Compacted Backfill Earth
C_CRANE     = '#FFB300'          # Dense Amber (Industrial Actuator)
C_CW        = '#1E293B'          # Carbon Slate (Counterweight Mass)
C_STATOR    = '#94A3B8'          # Steel Grey (Cable tension/Dust)
C_DEADMAN   = '#005599'          # Deep Marine (Shear Resistance Anchor)
C_PAYLOAD   = '#DE008A'          # Deep Magenta (Sunken Wreckage)
C_FAIL      = '#FF3300'          # Intense Red (Yield Exceeded)
C_OK        = '#00C853'          # Jade (Structural Dominance)

# ------------------------------------------------------------------
# O(1) VECTOR ROTATION ENGINE 
# ------------------------------------------------------------------
def rotate_poly(poly, pivot_x, pivot_y, angle_deg, offset_x):
    """
    Applies mathematically absolute rotation around a specific pivot,
    followed by a flat lateral Cartesian translation.
    """
    a = np.radians(angle_deg)
    c, s = np.cos(a), np.sin(a)
    new_poly = []
    for pt in poly:
        # Shift to origin around pivot
        dx = pt[0] - pivot_x
        dy = pt[1] - pivot_y
        # Rotate
        nx = dx * c + dy * s
        ny = -dx * s + dy * c
        # Return to position and strictly apply cinematic offset
        new_poly.append([nx + pivot_x + offset_x, ny + pivot_y])
    return np.array(new_poly)

# ------------------------------------------------------------------
# BASE GEOMETRIES (Relative to Crane Origin X=0)
# ------------------------------------------------------------------
# Pivot is exact front, bottom of the track (X=45, Y=-15)
PIVOT = (45, -15)

POLY_TRACK  = [[-55, -15], [45, -15], [55, 5], [-65, 5]]
POLY_BASE   = [[-45, 5], [35, 5], [35, 25], [-45, 25]]
POLY_CAB    = [[-35, 25], [15, 25], [5, 75], [-45, 75]]
POLY_BOOM   = [[0, 35], [20, 25], [140, 220], [120, 235]]
POLY_CW     = [[-75, 5], [-40, 5], [-40, 70], [-75, 70]]
HOOK_REAR   = [-45, 15]

# Environment Geometry
POLY_CHASM  = [[70, -15], [250, -15], [250, -800], [70, -800]]
POLY_DEADMAN = [[-240, -160], [-200, -160], [-200, -100], [-240, -100]]

# ------------------------------------------------------------------
# O(1) KINEMATIC STREAM 
# ------------------------------------------------------------------
def generate_stream():
    np.random.seed(430)
    # Friction Spallation Matrix (500 particles for extreme sliding)
    s_x, s_y = np.zeros(500), np.zeros(500)
    s_vx, s_vy = np.zeros(500), np.zeros(500)
    s_life = np.zeros(500)

    for f in range(TOTAL_FRAMES):
        t = f / FPS
        
        # State Matrix
        tilt = 0.0          # Degrees
        x_off = 0.0         # Metres
        load_y = -450.0     # Metres
        has_cw = False
        has_dm = False
        cw_drop_y = 0.0
        tension_lvl = 0.0
        winch_eng = False
        
        msg_top = ""
        msg_bot = ""
        col_ui = C_TEXT

        # ==========================================================
        # PHASE 1: TORQUE IMPALANCE / TIPPING (0 to 6.5s)
        # ==========================================================
        if t < 6.5:
            msg_top = "[PHASE 1: TORQUE IMBALANCE]"
            if t > 1.5: winch_eng = True
            
            if 1.5 < t < 3.5:
                tension_lvl = np.clip((t - 1.5) * 2.0, 0.0, 1.0)
                tilt = np.interp(t, [1.5, 3.5], [0.0, 18.0]) # Pitch forward
            elif t >= 3.5:
                tension_lvl = 1.0
                tilt = 18.0
                col_ui = C_FAIL
                msg_bot = "[FAILURE: CENTRE OF MASS YIELD EXCEEDED]"

        # ==========================================================
        # PHASE 2: STATIC FRICTION YIELD / SLIDING (6.5 to 14.5s)
        # ==========================================================
        elif t < 14.5:
            has_cw = True
            msg_top = "[PHASE 2: STATIC FRICTION YIELD]"
            
            # Counterweight dropped into existence gracefully
            if t < 7.5:
                cw_drop_y = np.interp(t, [6.5, 7.5], [200.0, 0.0])
                msg_bot = "[COUNTERWEIGHT MASS ADDED -> TORQUE SECURED]"
            else:
                if t > 8.5: winch_eng = True
                if 8.5 < t < 10.5:
                    tension_lvl = 1.0
                    x_off = np.interp(t, [8.5, 10.5], [0.0, 45.0])
                    
                    # Track Spallation Kinetic Dust Generator
                    spawns = 25
                    dead = np.where(s_life <= 0)[0]
                    if len(dead) > spawns:
                        idx = dead[:spawns]
                        s_x[idx] = np.random.uniform(-55, 45, spawns) + x_off
                        s_y[idx] = -15.0
                        s_vx[idx] = np.random.uniform(-8.0, -2.0, spawns) # Flies out back
                        s_vy[idx] = np.random.uniform( 1.0, 6.0, spawns)
                        s_life[idx] = 1.0

                elif t >= 10.5:
                    tension_lvl = 1.0
                    x_off = 45.0
                    col_ui = C_FAIL
                    msg_bot = "[FAILURE: LATERAL FRICTION OVERCOME]"

        # ==========================================================
        # PHASE 3: THE MACRO-ANCHOR DOMINANCE (14.5 to 24.0s)
        # ==========================================================
        else:
            has_cw = True
            has_dm = True
            msg_top = "[PHASE 3: BARE-METAL DOMINANCE]"
            
            if t < 15.5:
                msg_bot = "[DEADMAN BEAM BURIED -> SHEAR RESISTANCE LOCKED]"
            else:
                winch_eng = True
                if 15.5 < t < 16.5:
                    tension_lvl = np.clip((t - 15.5) * 2.0, 0.0, 1.0)
                    msg_bot = "[TENSIONING MACRO-ANCHOR VECTOR]"
                elif 16.5 < t < 21.5:
                    tension_lvl = 1.0
                    load_y = np.interp(t, [16.5, 21.5], [-450.0, 40.0])
                    col_ui = C_OK
                    msg_bot = "[NOMINAL: DEADMAN SECURES ARCHITECTURE]"
                elif t >= 21.5:
                    tension_lvl = 1.0
                    load_y = 40.0
                    col_ui = C_OK
                    msg_bot = "[LIFT COMPLETE]"

        # Modulo / Snap Rest transition wipe out parameters gracefully
        if 5.5 < t < 6.5 or 13.5 < t < 14.5:
            winch_eng = False
            tension_lvl = 0.0
            
        # Friction Tensor Processing
        s_life -= 0.05
        s_x += s_vx
        s_y += s_vy
        s_vy -= 0.5 # Gravity
        s_vx *= 0.9
        
        # Ground hit floor
        hit = s_y <= -15.0
        s_y[hit] = -15.0
        s_vy[hit] = 0.0
        
        act = np.where(s_life > 0)[0]

        yield (f, t, tilt, x_off, load_y, has_cw, has_dm, cw_drop_y, winch_eng, tension_lvl, msg_top, msg_bot, col_ui,
               np.copy(s_x[act]), np.copy(s_y[act]), np.copy(s_life[act]))

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    (f, t, tilt, x_off, load_y, has_cw, has_dm, cw_drop_y, winch_eng, 
     tension_lvl, msg_top, msg_bot, col_ui, sx, sy, sl) = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # Architectural framing (700w x 1244h geometrically maps 9:16)
    ax.set_xlim(-400, 300)
    ax.set_ylim(-800, 444)

    # 1. BEDROCK AND TOPOGRAPHY
    # Infinite Earth
    ax.add_patch(patches.Rectangle((-600, -900), 1200, 900-15, facecolor=C_BEDROCK, zorder=1))
    ax.plot([-600, 600], [-15, -15], color=C_TEXT, lw=4, zorder=2)
    
    # Excavated Deadman Trench
    if has_dm:
        ax.add_patch(patches.Rectangle((-260, -180), 80, 180-15, facecolor=C_TRENCH, zorder=3))
        ax.add_patch(patches.Polygon(POLY_DEADMAN, facecolor=C_DEADMAN, edgecolor=C_TEXT, lw=3, zorder=4))
        
        # Anchor Tension Cable (Deadman to Crane Hook)
        rear_hook = rotate_poly([HOOK_REAR], PIVOT[0], PIVOT[1], tilt, x_off)[0]
        dm_anchor = [-220, -130]
        
        cable_col = C_TEXT if winch_eng else C_STATOR
        cable_lw  = 6 if tension_lvl > 0.5 else 2
        ax.plot([dm_anchor[0], rear_hook[0]], [dm_anchor[1], rear_hook[1]], color=cable_col, lw=cable_lw, zorder=5)
        
        # Stress spallation triangles if tension is hitting absolute
        if tension_lvl > 0.5:
            for i in range(5):
                tx = -220 + (rear_hook[0] - -220) * (i/4.0)
                ty = -130 + (rear_hook[1] - -130) * (i/4.0)
                ax.add_patch(patches.Polygon([[tx, ty+10], [tx-15, ty-10], [tx+15, ty-10]], facecolor=C_OK, zorder=4, alpha=0.6))
        
    # The Payload Chasm
    ax.add_patch(patches.Polygon(POLY_CHASM, facecolor=C_BG, zorder=15))
    ax.plot([POLY_CHASM[0][0], POLY_CHASM[3][0]], [POLY_CHASM[0][1], POLY_CHASM[3][1]], color=C_TEXT, lw=4, zorder=16)

    # 2. THE ACTUATOR (CRANE KINEMATICS)
    # Track array
    t_track = rotate_poly(POLY_TRACK, PIVOT[0], PIVOT[1], tilt, x_off)
    ax.add_patch(patches.Polygon(t_track, facecolor=C_CW, edgecolor=C_TEXT, lw=3, zorder=20))
    
    t_base = rotate_poly(POLY_BASE, PIVOT[0], PIVOT[1], tilt, x_off)
    ax.add_patch(patches.Polygon(t_base, facecolor=C_CRANE, edgecolor=C_TEXT, lw=3, zorder=21))

    t_cab = rotate_poly(POLY_CAB, PIVOT[0], PIVOT[1], tilt, x_off)
    ax.add_patch(patches.Polygon(t_cab, facecolor=C_CRANE, edgecolor=C_TEXT, lw=3, zorder=22))
    
    # Counterweight (Drop logic handles Y offset before tilt)
    if has_cw:
        cw_local = [[p[0], p[1] + cw_drop_y] for p in POLY_CW]
        t_cw = rotate_poly(cw_local, PIVOT[0], PIVOT[1], tilt, x_off)
        ax.add_patch(patches.Polygon(t_cw, facecolor=C_CW, edgecolor=C_TEXT, lw=3, zorder=25))

    t_boom = rotate_poly(POLY_BOOM, PIVOT[0], PIVOT[1], tilt, x_off)
    ax.add_patch(patches.Polygon(t_boom, facecolor=C_CRANE, edgecolor=C_TEXT, lw=3, zorder=23))
    
    # 3. WINCH CABLE & PAYLOAD
    boom_tip = t_boom[2] # Top right coordinate of boom
    
    # Tension Visuals
    t_col = C_TEXT if winch_eng else C_STATOR
    t_lw  = 2 + (tension_lvl * 4) 
    
    # Payload center is locked directly below boom tip 
    # (Gravity always acts perfectly downward regardless of crane tilt)
    p_x = boom_tip[0]
    p_w = 25
    ax.plot([p_x, p_x], [boom_tip[1], load_y], color=t_col, lw=t_lw, zorder=30)
    
    ax.add_patch(patches.Rectangle((p_x - p_w, load_y - p_w*1.5), p_w*2, p_w*1.5, facecolor=C_PAYLOAD, edgecolor=C_TEXT, lw=3, zorder=31))
    
    # Overlaid structural cross to designate it as 'The Payload'
    ax.plot([p_x - p_w, p_x + p_w], [load_y - p_w*1.5, load_y], color=C_TEXT, lw=2, zorder=32)
    ax.plot([p_x - p_w, p_x + p_w], [load_y, load_y - p_w*1.5], color=C_TEXT, lw=2, zorder=32)

    # 4. FRICTION SPALLATION RENDER
    if len(sx) > 0:
        c_dust = np.zeros((len(sx), 4))
        c_dust[:, :3] = np.array(mcol.to_rgb(C_STATOR))  # Grey dust
        c_dust[:, 3] = sl * 0.8
        ax.scatter(sx, sy, s=sl*40, c=c_dust, edgecolors='none', zorder=28)

    # 5. ABSOLUTE DAYLIGHT TELEMETRY 
    ax.add_patch(plt.Rectangle((0, 0.92), 1, 0.08, transform=ax.transAxes, facecolor=C_BG, zorder=80))
    ax.plot([0, 1], [0.92, 0.92], transform=ax.transAxes, color=C_TEXT, lw=6, zorder=81)
    ax.text(0.04, 0.965, "LG-430 :: HEAVY LIFT RECOVERY", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=82)
    ax.text(0.04, 0.935, msg_top, transform=ax.transAxes, color=C_STATOR, fontsize=18, fontname='monospace', weight='bold', va='center', zorder=82)

    ax.add_patch(plt.Rectangle((0, 0), 1, 0.12, transform=ax.transAxes, facecolor=C_BG, zorder=80))
    ax.plot([0, 1], [0.12, 0.12], transform=ax.transAxes, color=C_TEXT, lw=6, zorder=81)
    
    # Live Kinematic Readouts
    d_torque = "IMBALANCED (-)" if tilt > 1 else ("BALANCED (+)" if has_cw else "YIELD (+/-)")
    d_frict  = "STATIC (+)" if x_off < 1 and not has_dm else ("YIELD (-)" if not has_dm else "ANCHORED (+)")
    
    ax.text(0.04, 0.085, f"TORQUE MOMENT: {d_torque}", transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace', weight='bold', zorder=82)
    ax.text(0.04, 0.055, f"LATERAL DRIFT: {d_frict}", transform=ax.transAxes, color=C_TEXT, fontsize=18, fontname='monospace', weight='bold', zorder=82)

    pulse = col_ui if (f % 30 < 15) or col_ui == C_OK else C_TEXT
    ax.text(0.96, 0.06, msg_bot, transform=ax.transAxes, color=pulse, fontsize=16, fontname='monospace', weight='bold', ha='right', va='center', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-430: HEAVY RECOVERY TENSORS (DAYLIGHT) [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Macro-Anchor Operational Physics Locked. Stand by for compilation.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
