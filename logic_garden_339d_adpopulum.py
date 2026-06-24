"""
SOVEREIGN CODE: logic_garden_339d_adpopulum.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Vectorization
SCENE: Logic Garden 339d (Ad Populum // Consensus Smoothing)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING, COGNITIVE LOGIC
HOTFIX: Linear 22.0s Sequence. Daylight Protocol. Absolute Camera Lock. Tuples Sealed.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
DURATION = 22.0  
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_339d_adpopulum"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Environment Matrix
C_STEEL     = '#606065'   # The Objective Baseplate
C_DARK      = '#202025'   # Sovereign Node / Reality Base
C_CYAN      = '#00FFFF'   # Audit Scanner
C_MAGENTA   = '#FF0055'   # The Consensus Hallucination
C_GOLD      = '#FFB300'   # Physical Execution Parameter
C_MANTIS    = '#00FF00'   # Truth / Terminal Green

def draw_industrial_grid(ax):
    """Draw the Structural Matrix"""
    for i in range(-5, 6):
        ax.plot([i*100, i*100], [-960, 960], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)
    for j in range(-9, 10):
        ax.plot([-540, 540], [j*100, j*100], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)

# ------------------------------------------------------------------
# PRECOMPUTE SWARM (THE PEER CONSENSUS)
# ------------------------------------------------------------------
np.random.seed(339)
N_NODES = 600
# Initial floating states (Hallucinating a zero-gravity environment)
auth_y_init = 500.0
node_x = np.random.normal(0, 180, N_NODES)
node_y_init = np.random.normal(500, 120, N_NODES)

# Gravity Simulation Arrays
node_y = np.copy(node_y_init)
node_v = np.zeros(N_NODES)
auth_y = auth_y_init
auth_v = 0.0

# Precalculate Kinematics
GRAVITY_ON = 6.0
G_FORCE = -900.0 # Pixel acceleration per second squared
timeline_node_y = np.zeros((TOTAL_FRAMES, N_NODES))
timeline_auth_y = np.zeros(TOTAL_FRAMES)
sparks = [] # Will store (frame_idx, x, y, size)

for f in range(TOTAL_FRAMES):
    t = f / FPS
    dt = 1.0 / FPS
    
    if t > GRAVITY_ON:
        # Authority Falls
        auth_v += G_FORCE * dt
        auth_y += auth_v * dt
        if auth_y <= 20: 
            auth_y = 20
            # Bounce and settle
            if auth_v < 0: auth_v = -auth_v * 0.2
            if abs(auth_v) > 50: sparks.append((f, 0, 20, abs(auth_v)*10))
            
        # Swarm Falls
        node_v += G_FORCE * dt
        node_y += node_v * dt
        
        # Baseplate Collision
        hits = node_y <= 0
        node_y[hits] = 0
        
        for i in np.where(hits)[0]:
            if node_v[i] < -20: # Only spark on hard hit
                sparks.append((f, node_x[i], 0, abs(node_v[i])*2))
            node_v[i] = -node_v[i] * np.random.uniform(0.1, 0.4) # Spallation bounce
            
    timeline_node_y[f] = node_y
    timeline_auth_y[f] = auth_y

def render_frame(packet):
    f, phase_ratio = packet
    t = phase_ratio * DURATION 
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    
    # BARE-METAL CAMERA LOCK
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)
    ax.autoscale(False)
    draw_industrial_grid(ax)

    # 1. THE OBJECTIVE BASEPLATE (Y=0)
    ax.add_patch(patches.Rectangle((-540, -100), 1080, 100, facecolor=C_TITANIUM, edgecolor=C_STEEL, lw=4, zorder=2))
    ax.plot([-540, 540], [0, 0], color=C_TEXT, lw=4, zorder=3)
    ax.text(-500, -50, "PHYSICAL BASEPLATE // OBJECTIVE KINEMATICS", color=C_STEEL, fontsize=16, weight='bold', fontname='monospace', zorder=4)

    # 2. THE SOVEREIGN NODE (Architect running isolated processing)
    SOV_Y = -400
    ax.add_patch(patches.RegularPolygon((0, SOV_Y), numVertices=6, radius=60, facecolor=C_BG, edgecolor=C_DARK, lw=4, zorder=5))
    ax.add_patch(patches.Circle((0, SOV_Y), 20, facecolor=C_GOLD if t < GRAVITY_ON else C_MANTIS, zorder=6))
    
    aud_col = C_TITANIUM if t < GRAVITY_ON else C_MANTIS
    ax.plot([0, 0], [SOV_Y+60, 0], color=aud_col, lw=2, linestyle='--', zorder=4)

    # 3. THE AUTHORITY NODE
    curr_auth_y = timeline_auth_y[f]
    # Rotate gear based on velocity
    trans_auth = matplotlib.transforms.Affine2D().rotate_deg_around(0, curr_auth_y, t*30) + ax.transData
    
    auth_edge = C_MAGENTA if curr_auth_y > 25 else C_STEEL
    ax.add_patch(patches.RegularPolygon((0, curr_auth_y), numVertices=8, radius=40, facecolor=C_BG, edgecolor=auth_edge, lw=4, transform=trans_auth, zorder=15))
    ax.add_patch(patches.Circle((0, curr_auth_y), 15, facecolor=auth_edge, zorder=16))

    # Broadcast Wave from Authority
    if t < GRAVITY_ON:
        b_rad = (t * 200) % 600
        ax.add_patch(patches.Circle((0, curr_auth_y), b_rad, fill=False, edgecolor=C_MAGENTA, lw=2, alpha=1.0-(b_rad/600), zorder=10))

    # 4. THE SWARM (Ad Populum)
    curr_node_y = timeline_node_y[f]
    
    # Render intact nodes (floating or falling)
    floating_mask = curr_node_y > 2
    ground_mask = curr_node_y <= 2
    
    # Floating items sync to the Magenta Hallucination
    if np.any(floating_mask):
        ax.scatter(node_x[floating_mask], curr_node_y[floating_mask]-5, s=60, c=C_BG, edgecolors=C_MAGENTA, lw=1.5, zorder=12)
        ax.scatter(node_x[floating_mask], curr_node_y[floating_mask], s=20, c=C_MAGENTA, zorder=13)
        
    # Broken nodes on the baseplate (Consensus destroyed)
    if np.any(ground_mask):
        ax.scatter(node_x[ground_mask], curr_node_y[ground_mask], s=60, c=C_TITANIUM, marker='x', lw=2, zorder=11)

    # Render Spallation Sparks
    active_sparks = [s for s in sparks if f >= s[0] and f < s[0] + 30]
    for sp_f, sp_x, sp_y, sp_s in active_sparks:
        age = f - sp_f
        alpha = max(0, 1.0 - (age / 30.0))
        ry = sp_y + (age * 15.0) - (0.5 * 20.0 * age**2 * 0.001) # mini parabolic arc
        rx = sp_x + np.random.uniform(-age*2, age*2)
        ax.scatter(rx, ry, s=sp_s*alpha, c=C_MAGENTA, edgecolors='none', alpha=alpha, zorder=14)

    # ====================================================
    # 5. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    # Top Header [Strict Tuples]
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-339d :: AD POPULUM TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] OUTSOURCED DISCRIMINATORY KNOWLEDGE", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    # Bottom Telemetry HUD
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    # Logic Engine States
    if t < GRAVITY_ON:
        n_color = C_MAGENTA
        t_state = "CONSENSUS : 100% // NETWORK ALIGNED"
        g_state = "SUSPENDED [FALSE TOPOLOGY]"
    elif curr_auth_y > 25:
        n_color = C_MAGENTA
        t_state = "O(1) PHYSICAL RUPTURE DETECTED"
        g_state = "TENSOR IGNITED // 9.8m/s\u00b2 OBLIGATION"
    else:
        n_color = C_STEEL
        t_state = "CONSENSUS ANNIHILATED"
        g_state = "BASEPLATE VERIFIED // FRICTION SECURED"

    ax.text(-500, -760, "SYS_01 [NETWORK CLUSTER]     :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, t_state, color=n_color, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [THERMODYNAMIC TENSOR]:", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, g_state, color=C_GOLD if t < GRAVITY_ON else C_MANTIS, fontsize=15, fontname='monospace', weight='bold', zorder=82)
    
    ax.text(-500, -840, "SOVEREIGN AUDIT / BASELINE   :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, "ISOLATED // VERIFYING DATA LOCALLY" if t < GRAVITY_ON else "TATH\u0100T\u0100 // GROUNDED TRUTH ATTAINED", color=C_MANTIS if t >= GRAVITY_ON else C_TEXT, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider [Strict Tuples]
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=n_color if t < GRAVITY_ON else C_MANTIS, zorder=83))

    # Sovereign Execution Output
    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    
    # Absolute Memory Annihilation
    plt.close('all')
    gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-339d: AD POPULUM TENSOR [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE] [Tuples Sealed]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
