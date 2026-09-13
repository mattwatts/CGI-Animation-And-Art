"""
PROJECT: Logic Garden 434 (Exact Physical Construct // Space Taxi Kinematics)
FORMAT: YouTube Shorts (1080x1920)
METADATA: SPACE TAXI, C64, MOMENTUM, KINEMATICS, DAYLIGHT
EXECUTION: 12.0s Sequence. True Seamless Cyclical Polynomial Matrix.
RULES ENFORCED:
- O(1) C2-continuous polynomials governing absolute zero-velocity docking.
- True Newtonian Thruster Kinematics mapping Gravity (T_y = A_y + g).
- Kinematic Camera Lock (Dynamic Y-Axis centering on chassis).
- Daylight Palette (White Substrate / High-Contrast Mathematical Geometry).
- Purged Jargon. Australian spelling conventions (maths, colour).
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
import math

# ======== SEQUENCE PARAMETERS ========
DURATION = 12.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_434_space_taxi"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- HIGH-CONTRAST DAYLIGHT PALETTE --------
C_BG        = '#FFFFFF'
C_TEXT      = '#111115'          # Indestructible Black UI
C_STEEL     = '#94A3B8'          # Elevator Shaft Superstructure
C_TAXI      = '#FFB300'          # Dense Amber (Iconic Cab Yellow)
C_GLASS     = '#005599'          # Deep Marine (Cab Window)
C_PAD1      = '#1E293B'          # Carbon Slate (Lower Pad)
C_PAD2      = '#1E293B'          # Carbon Slate (Upper Pad)
C_PASSENGER = '#00C853'          # Jade (Payload Entity)
C_THRUST    = '#FF3300'          # Intense Red (Hypergolic Reaction)
C_EXHAUST   = '#DE008A'          # Deep Magenta Spallation

# ------------------------------------------------------------------
# O(1) MACRO PHYSICS ENGINE (NEWTONIAN POLYNOMIALS)
# ------------------------------------------------------------------
G_CONST = 250.0  # Constant Downward Gravitational Force

def get_taxi_kinematics(t):
    """
    Evaluates exact 5th Degree continuous Splines.
    Guarantees structural touchdown velocity and acceleration equal strictly 0.0.
    """
    # Pad 1 (Bottom Left) -> Pad 2 (Top Right) constraints
    P1_X, P1_Y = -250.0, -400.0
    P2_X, P2_Y =  250.0,  400.0
    
    if t < 1.0:
        return P1_X, P1_Y, 0.0, 0.0, 0.0, 0.0
    elif t < 5.0:
        u = (t - 1.0) / 4.0
        fu = 6*u**5 - 15*u**4 + 10*u**3
        du = 30*u**4 - 60*u**3 + 30*u**2
        ddu = 120*u**3 - 180*u**2 + 60*u
        
        dx, dy = P2_X - P1_X, P2_Y - P1_Y
        x = P1_X + dx * fu
        y = P1_Y + dy * fu
        vx = (dx / 4.0) * du
        vy = (dy / 4.0) * du
        ax = (dx / 16.0) * ddu
        ay = (dy / 16.0) * ddu
        return x, y, vx, vy, ax, ay
    elif t < 7.0:
        return P2_X, P2_Y, 0.0, 0.0, 0.0, 0.0
    elif t < 11.0:
        u = (t - 7.0) / 4.0
        fu = 6*u**5 - 15*u**4 + 10*u**3
        du = 30*u**4 - 60*u**3 + 30*u**2
        ddu = 120*u**3 - 180*u**2 + 60*u
        
        dx, dy = P1_X - P2_X, P1_Y - P2_Y
        x = P2_X + dx * fu
        y = P2_Y + dy * fu
        vx = (dx / 4.0) * du
        vy = (dy / 4.0) * du
        ax = (dx / 16.0) * ddu
        ay = (dy / 16.0) * ddu
        return x, y, vx, vy, ax, ay
    else:
        return P1_X, P1_Y, 0.0, 0.0, 0.0, 0.0

def get_passenger(t, tax_x, tax_y):
    """ Rigid tracking equations for Passenger Payload matrix loop. """
    DOOR1_X, PAD1_Y = -450.0, -400.0
    DOOR2_X, PAD2_Y =  450.0,  400.0
    TAX1_X, TAX2_X = -250.0, 250.0
    
    if t < 1.0: 
        state = "BOARDING PAD 1"
        return DOOR1_X + 200.0 * t, PAD1_Y, True, state
    elif t < 5.0:
        state = "SECURED IN TRANSIT"
        return tax_x, tax_y, False, state  # Invisible while inside
    elif t < 6.0:
        state = "DISEMBARKING PAD 2"
        return TAX2_X + 200.0 * (t - 5.0), PAD2_Y, True, state
    elif t < 7.0:
        state = "BOARDING PAD 2"
        return DOOR2_X - 200.0 * (t - 6.0), PAD2_Y, True, state
    elif t < 11.0:
        state = "SECURED IN TRANSIT"
        return tax_x, tax_y, False, state
    else:
        state = "DISEMBARKING PAD 1"
        return TAX1_X - 200.0 * (t - 11.0), PAD1_Y, True, state

# ------------------------------------------------------------------
# PARALLEL GENERATOR (LOGIC TENSORS)
# ------------------------------------------------------------------
def generate_stream():
    np.random.seed(434)
    
    # Pre-allocate sheer exhaust spallation matrix
    MAX_D = 1500
    d_pos = np.zeros((MAX_D, 2))
    d_vel = np.zeros((MAX_D, 2))
    d_life = np.zeros(MAX_D)

    for f in range(TOTAL_FRAMES):
        t = f / float(FPS)
        x, y, vx, vy, ax, ay = get_taxi_kinematics(t)
        p_x, p_y, p_vis, p_state = get_passenger(t, x, y)
        
        # True Newtonian Thruster Force Evaluator
        # T_force = Mass * Accel. We assume Mass = 1.0. T_y must counter Gravity continuously.
        if (t >= 1.0 and t < 5.0) or (t >= 7.0 and t < 11.0):
            thrust_x = ax
            thrust_y = ay + G_CONST
        else:
            thrust_x = 0.0
            thrust_y = 0.0 # Pad geometry supplies identical normal force to gravity
            
        # Spawn Spallation Plume Density based on thruster yields
        actv_idx = np.where(d_life <= 0)[0]
        n_spawn = 0
        if thrust_y > 20.0: # Bottom thruster
            n_req = min(15, len(actv_idx))
            if n_req > 0:
                idx = actv_idx[:n_req]
                d_pos[idx, 0] = x + np.random.uniform(-10, 10, n_req)
                d_pos[idx, 1] = y - 25.0
                d_vel[idx, 0] = np.random.uniform(-15, 15, n_req) - vx*0.2
                d_vel[idx, 1] = -thrust_y * 0.5 * np.random.uniform(0.5, 1.5, n_req)
                d_life[idx] = np.random.uniform(0.2, 0.8, n_req)
                actv_idx = actv_idx[n_req:]

        # Left/Right Thrusters
        if abs(thrust_x) > 20.0:
            n_req = min(10, len(actv_idx))
            if n_req > 0:
                idx = actv_idx[:n_req]
                side = -1.0 if thrust_x > 0 else 1.0 # If pushing right (pos tx), fire LEFT thruster
                d_pos[idx, 0] = x + side * 40.0
                d_pos[idx, 1] = y
                d_vel[idx, 0] = side * abs(thrust_x) * 0.8 * np.random.uniform(0.5, 1.5, n_req) - vx*0.2
                d_vel[idx, 1] = np.random.uniform(-10, 10, n_req)
                d_life[idx] = np.random.uniform(0.2, 0.5, n_req)
        
        # Integrate Exhaust Particle Physics
        act = d_life > 0
        if np.any(act):
            d_vel[act, 1] -= G_CONST * (1.0/FPS) # Plume falls due to global gravity
            d_pos[act] += d_vel[act] * (1.0/FPS)
            # Hard collisions with Euclidean Pad constraints
            hit_pad1 = (d_pos[:, 0] < -100) & (d_pos[:, 1] < -415)
            hit_pad2 = (d_pos[:, 0] > 100) & (d_pos[:, 1] < 385) & (d_pos[:, 1] > 350)
            d_life[act & (hit_pad1 | hit_pad2)] = 0.0
            d_life[act] -= (1.0/FPS)

        active_indices = np.nonzero(d_life > 0)[0]
        
        yield (f, t, x, y, vx, vy, thrust_x, thrust_y, p_x, p_y, p_vis, p_state, 
               np.copy(d_pos[active_indices]), np.copy(d_life[active_indices]))

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t, tx, ty, vx, vy, T_x, T_y, px, py, p_vis, p_state, d_pos, d_life = packet

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # 1. KINEMATIC CAMERA LOCK
    # Dynamically tracking the Taxi explicitly along the Y-axis. Limits rigidly set to exactly 1920 vertical span.
    cam_y = ty
    ax.set_xlim(-540, 540)
    ax.set_ylim(cam_y - 960, cam_y + 960)

    # 2. EUCLIDEAN SHAFT ARCHITECTURE (Background Grids)
    # The absolute structure proves the camera velocity visually
    for i_x in [-450, 450]:
        ax.plot([i_x, i_x], [-2000, 2000], color=C_STEEL, lw=3, zorder=1)
    for i_y in range(-2000, 2000, 100):
        # Cross bracing
        ax.plot([-450, -350], [i_y, i_y+50], color=C_STEEL, lw=1, zorder=1)
        ax.plot([450, 350], [i_y, i_y+50], color=C_STEEL, lw=1, zorder=1)

    # 3. KINEMATIC PLATFORMS (THE PADS)
    # Pad 1 (Bottom Left)
    ax.add_patch(patches.Rectangle((-540, -440), 440, 20, facecolor=C_PAD1, edgecolor=C_TEXT, lw=3, zorder=5))
    ax.plot([-250, -150], [-420, -420], color=C_PASSENGER, lw=4, solid_capstyle='round', zorder=6) # Arrival Light
    ax.add_patch(patches.Rectangle((-540, -420), 90, 80, facecolor=C_TEXT, zorder=7)) # Door 1 Void
    ax.text(-400, -455, "ZONE [01]", color=C_BG, fontsize=12, fontname='monospace', weight='bold', zorder=8)

    # Pad 2 (Top Right)
    ax.add_patch(patches.Rectangle((100, 360), 440, 20, facecolor=C_PAD2, edgecolor=C_TEXT, lw=3, zorder=5))
    ax.plot([150, 250], [380, 380], color=C_PASSENGER, lw=4, solid_capstyle='round', zorder=6) # Arrival Light
    ax.add_patch(patches.Rectangle((450, 380), 90, 80, facecolor=C_TEXT, zorder=7)) # Door 2 Void
    ax.text(250, 345, "ZONE [02]", color=C_BG, fontsize=12, fontname='monospace', weight='bold', zorder=8)

    # 4. PASSENGER (BIOLOGICAL PAYLOAD KINEMATICS)
    if p_vis:
        ax.add_patch(patches.Rectangle((px-8, py+1), 16, 25, facecolor=C_PASSENGER, edgecolor=C_TEXT, lw=2, zorder=14))
        ax.add_patch(patches.Circle((px, py+32), 6, facecolor=C_BG, edgecolor=C_PASSENGER, lw=2, zorder=14))

    # 5. SPACE TAXI (THE MACHINED CONSTRUCT)
    # Intense Red Thruster Vectors computed dynamically from O(1) physics
    if abs(T_x) > 10.0:
        side = -1.0 if T_x > 0 else 1.0
        mag = abs(T_x) * 0.15
        poly_tx = [[tx + side*40, ty], [tx + side*40, ty+10], [tx + side*(40+mag), ty+5]]
        ax.add_patch(patches.Polygon(poly_tx, facecolor=C_THRUST, edgecolor='none', zorder=18))
    
    if T_y > 10.0:
        mag = T_y * 0.15
        poly_ty = [[tx-15, ty-20], [tx+15, ty-20], [tx, ty-20-mag]]
        ax.add_patch(patches.Polygon(poly_ty, facecolor=C_THRUST, edgecolor='none', zorder=18))
    elif T_y < -10.0: # Downward thrust (Firing Top engines)
        mag = abs(T_y) * 0.15
        poly_td = [[tx-10, ty+40], [tx+10, ty+40], [tx, ty+40+mag]]
        ax.add_patch(patches.Polygon(poly_td, facecolor=C_THRUST, edgecolor='none', zorder=18))

    # Main Structural Body (Dense Amber Carbon)
    ax.add_patch(patches.Rectangle((tx-40, ty-20), 80, 40, facecolor=C_TAXI, edgecolor=C_TEXT, lw=3, zorder=20))
    # Kinetic Checkers
    for bx in range(-40, 40, 10):
        c_chk = C_TEXT if (bx//10)%2==0 else C_BG
        ax.add_patch(patches.Rectangle((tx+bx, ty-5), 10, 10, facecolor=c_chk, zorder=21))
    
    # Windshield Canopy
    ax.add_patch(patches.Polygon([[tx-25, ty+20], [tx+25, ty+20], [tx+15, ty+40], [tx-15, ty+40]], facecolor=C_GLASS, edgecolor=C_TEXT, lw=3, zorder=22))
    
    # Rigid Landing Gear
    ax.plot([tx-30, tx-35], [ty-20, ty-30], color=C_TEXT, lw=4, solid_capstyle='round', zorder=19)
    ax.plot([tx+30, tx+35], [ty-20, ty-30], color=C_TEXT, lw=4, solid_capstyle='round', zorder=19)
    ax.plot([tx-45, tx-25], [ty-30, ty-30], color=C_TEXT, lw=4, solid_capstyle='round', zorder=19)
    ax.plot([tx+25, tx+45], [ty-30, ty-30], color=C_TEXT, lw=4, solid_capstyle='round', zorder=19)

    # 6. EXHAUST SPALLATION DEBRIS
    if len(d_pos) > 0:
        c_deb = np.zeros((len(d_pos), 4))
        c_deb[:, :3] = np.array(mcol.to_rgb(C_EXHAUST))
        c_deb[:, 3] = np.clip(d_life, 0, 1)
        ax.scatter(d_pos[:,0], d_pos[:,1], s=d_life*25, c=c_deb, edgecolors='none', zorder=17)

    # 7. ABSOLUTE DAYLIGHT TELEMETRY (TOP HUD)
    # Explicit use of transAxes to computationally lock UI to screen matrix, not geometry
    ax.add_patch(plt.Rectangle((0, 0.90), 1, 0.10, transform=ax.transAxes, facecolor=C_BG, zorder=80))
    ax.plot([0, 1], [0.90, 0.90], transform=ax.transAxes, color=C_TEXT, lw=6, zorder=81)

    ax.text(0.04, 0.965, 'LG-434 // "SPACE TAXI" KINEMATIC MATRIX', transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center', zorder=82)
    ax.text(0.04, 0.930, "EXACT COMMODORE 64 PHYSICS REPLICATION", transform=ax.transAxes, color=C_STEEL, fontsize=15, fontname='monospace', weight='bold', va='center', zorder=82)

    ax.text(0.96, 0.965, "TIPS: $92.50", transform=ax.transAxes, color=C_PASSENGER, fontsize=20, fontname='monospace', weight='bold', ha='right', va='center', zorder=82)

    # 8. ABSOLUTE DAYLIGHT TELEMETRY (BOTTOM HUD)
    ax.add_patch(plt.Rectangle((0, 0), 1, 0.14, transform=ax.transAxes, facecolor=C_BG, zorder=80))
    ax.plot([0, 1], [0.14, 0.14], transform=ax.transAxes, color=C_TEXT, lw=6, zorder=81)

    hud_col = C_PASSENGER if "SECURED" in p_state else C_TEXT
    ax.text(0.04, 0.10, f"PAYLOAD DOMAIN: {p_state}", transform=ax.transAxes, color=hud_col, fontsize=18, fontname='monospace', weight='bold', zorder=82)
    
    ax.text(0.04, 0.06, f"THRUST VECTOR X : {T_x:+07.1f} N", transform=ax.transAxes, color=C_THRUST, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(0.04, 0.03, f"THRUST VECTOR Y : {T_y:+07.1f} N", transform=ax.transAxes, color=C_THRUST, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    
    ax.text(0.60, 0.06, f"ALTITUDE (Y): {ty:+06.1f} M", transform=ax.transAxes, color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)
    ax.text(0.60, 0.03, f"GRAVITY CAP : {G_CONST:05.1f} G", transform=ax.transAxes, color=C_TEXT, fontsize=16, fontname='monospace', weight='bold', zorder=82)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=C_BG, edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect()
    return f

# ------------------------------------------------------------------
# MULTIPROCESSING LAUNCHER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-434: SPACE TAXI MOMENTUM MATRIX (DAYLIGHT) [CORES: {cpu_cores}]")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Total: {TOTAL_FRAMES} frames")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: Frame {finished_frame:>4d} / {TOTAL_FRAMES}")

    print("Spline Polynomials and Thruster Yields Locked. Stand by for compilation.")

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
