"""
SOVEREIGN CODE: logic_garden_340a_domain_boundary.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Vectorization
SCENE: Logic Garden 340a (Domain-Specific Boundaries // Semantic Leaks)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING, COGNITIVE LOGIC
HOTFIX: Linear 24.0s Sequence. Daylight Protocol. Absolute Camera Lock. Tuples Sealed.
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
DURATION = 24.0  
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_340a_domain"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Environment Matrix
C_STEEL     = '#606065'   # Domain Boundary / Physical Constraints
C_DARK      = '#202025'   # Unmapped Domain Obstacles
C_CYAN      = '#00FFFF'   # The Processing Node (Optimized State)
C_GOLD      = '#FFB300'   # High-Speed Vector Trail
C_MAGENTA   = '#FF0055'   # Semantic Exhaust / Friction / Error
C_MANTIS    = '#00FF00'   # Terminal Green 

def draw_domain_matrices(ax):
    """Draw the Structural Matrices (Cartesian vs Polar)"""
    # DOMAIN 1: Cartesian (Top Half)
    for i in range(-5, 6):
        ax.plot([i*100, i*100], [0, 800], color=C_TITANIUM, lw=2, zorder=0)
    for j in range(1, 9):
        ax.plot([-540, 540], [j*100, j*100], color=C_TITANIUM, lw=2, zorder=0)
        
    # DOMAIN 2: Polar / Concentric (Bottom Half)
    for r in range(100, 800, 100):
        ax.add_patch(patches.Circle((0, -400), r, fill=False, edgecolor=C_TITANIUM, lw=2, zorder=0))

    # THE BOUNDARY WALL
    ax.add_patch(patches.Rectangle((-540, -10), 1080, 20, facecolor=C_STEEL, zorder=5))
    ax.plot([-540, 540], [10, 10], color=C_TEXT, lw=4, zorder=6)
    ax.plot([-540, 540], [-10, -10], color=C_TEXT, lw=4, zorder=6)
    ax.text(-500, 30, "DOMAIN 1: [CARTESIAN TOPOLOGY]", color=C_STEEL, fontsize=14, weight='bold', fontname='monospace', zorder=6)
    ax.text(-500, -40, "DOMAIN 2: [NON-EUCLIDEAN TOPOLOGY]", color=C_STEEL, fontsize=14, weight='bold', fontname='monospace', zorder=6)

# Kinematic Pathing Engine (Domain 1)
# Path: (-300, 500) -> (200, 500) -> (200, 200) -> (0, 200) -> (0, -180) [CRASH]
PATH_NODES = [
    (-300, 500), # T=0
    (200, 500),  # T=2.5
    (200, 200),  # T=4.0
    (0, 200),    # T=5.5
    (0, -180)    # T=8.5 (Breach & Impact)
]

def get_kinematic_pos(t):
    if t < 2.5:
        prg = t / 2.5
        return PATH_NODES[0][0] + (PATH_NODES[1][0] - PATH_NODES[0][0]) * prg, PATH_NODES[0][1]
    elif t < 4.0:
        prg = (t - 2.5) / 1.5
        return PATH_NODES[1][0], PATH_NODES[1][1] + (PATH_NODES[2][1] - PATH_NODES[1][1]) * prg
    elif t < 5.5:
        prg = (t - 4.0) / 1.5
        return PATH_NODES[2][0] + (PATH_NODES[3][0] - PATH_NODES[2][0]) * prg, PATH_NODES[2][1]
    elif t < 8.5:
        prg = (t - 5.5) / 3.0
        return PATH_NODES[3][0], PATH_NODES[3][1] + (PATH_NODES[4][1] - PATH_NODES[3][1]) * prg
    else:
        # Grinding at the crash boundary
        return PATH_NODES[4][0], PATH_NODES[4][1]

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
    draw_domain_matrices(ax)

    # 1. RENDER DOMAIN 2 OBSTACLES (The Rotating Polar Gear)
    GEAR_CY = -400
    GEAR_R = 220
    gear_rot = t * 45  # Degrees
    
    # The massive Non-Euclidean Baffle that the node tries to Cartesian-route through
    trans_gear = matplotlib.transforms.Affine2D().rotate_deg_around(0, GEAR_CY, gear_rot) + ax.transData
    ax.add_patch(patches.RegularPolygon((0, GEAR_CY), numVertices=12, radius=GEAR_R, facecolor=C_TITANIUM, edgecolor=C_DARK, lw=6, transform=trans_gear, zorder=4))
    
    # Internal hazard details
    for i in range(0, 360, 30):
        rad = np.radians(i + gear_rot)
        bx, by = 0 + GEAR_R * np.cos(rad), GEAR_CY + GEAR_R * np.sin(rad)
        ax.plot([0, bx], [GEAR_CY, by], color=C_DARK, lw=4, zorder=5)

    ax.add_patch(patches.Circle((0, GEAR_CY), 60, facecolor=C_DARK, zorder=6))

    # 2. RENDER THE COGNITIVE NODE & KINEMATICS
    nx, ny = get_kinematic_pos(t)
    
    # Render Trajectory History (The smooth O(1) path in Domain 1)
    if t < 2.5:
        ax.plot([PATH_NODES[0][0], nx], [PATH_NODES[0][1], ny], color=C_CYAN, lw=6, zorder=10)
    elif t < 4.0:
        ax.plot([PATH_NODES[0][0], PATH_NODES[1][0]], [PATH_NODES[0][1], PATH_NODES[1][1]], color=C_CYAN, lw=6, zorder=10)
        ax.plot([PATH_NODES[1][0], nx], [PATH_NODES[1][1], ny], color=C_CYAN, lw=6, zorder=10)
    elif t < 5.5:
        ax.plot([PATH_NODES[0][0], PATH_NODES[1][0], PATH_NODES[2][0]], [PATH_NODES[0][1], PATH_NODES[1][1], PATH_NODES[2][1]], color=C_CYAN, lw=6, zorder=10)
        ax.plot([PATH_NODES[2][0], nx], [PATH_NODES[2][1], ny], color=C_CYAN, lw=6, zorder=10)
    else:
        ax.plot([PATH_NODES[0][0], PATH_NODES[1][0], PATH_NODES[2][0], PATH_NODES[3][0]], [PATH_NODES[0][1], PATH_NODES[1][1], PATH_NODES[2][1], PATH_NODES[3][1]], color=C_CYAN, lw=6, zorder=10)
        ax.plot([PATH_NODES[3][0], nx], [PATH_NODES[3][1], ny], color=C_MAGENTA if ny < -10 else C_CYAN, lw=6, zorder=10)

    # 3. IMPACT & SEMANTIC LEAK LOGIC
    is_crashing = t >= 8.5
    
    # Node Drawing
    # The node starts Cyan, but turns Magent when it violates the boundary rules
    node_c = C_MAGENTA if ny < 0 else C_CYAN
    j_x = np.random.uniform(-4, 4) if is_crashing else 0
    j_y = np.random.uniform(-4, 4) if is_crashing else 0
    
    ax.add_patch(patches.Rectangle((nx - 25 + j_x, ny - 25 + j_y), 50, 50, facecolor=C_BG, edgecolor=node_c, lw=5, zorder=20))
    ax.scatter(nx + j_x, ny + j_y, s=80, c=node_c, zorder=21)

    # The Spallation Cascade (Grinding against the Non-Euclidean Gear)
    if is_crashing:
        np.random.seed(int(t*100))
        # Throwing thermodynamic exhaust off the contact point
        n_sparks = 30
        spark_x = nx + np.random.normal(0, 10, n_sparks)
        # Sparks fly laterally because straight down is blocked by the gear
        spark_y = ny - 20 + np.random.normal(0, 5, n_sparks)
        
        sx_vel = np.random.uniform(-1, 1, n_sparks) * 200
        sy_vel = np.random.uniform(0, 1, n_sparks) * 100
        
        # Simple simulated decay
        ax.scatter(spark_x + sx_vel*0.1, spark_y + sy_vel*0.1, s=np.random.uniform(10, 60, n_sparks), c=C_MAGENTA, alpha=0.8, edgecolors='none', zorder=25)
        
        # Hazard Halo
        flash = 0.5 + 0.3 * np.sin(t*30)
        ax.add_patch(patches.Circle((nx, ny-20), 40, facecolor=C_MAGENTA, alpha=flash, lw=0, zorder=19))

    # 4. HUD LOGIC TEXT
    if t < 6.5:
        state_str = "OPTIMAL DOMAIN DYNAMICS OCCURRING"
        c_status = C_CYAN
        t_status = "O(1) NAVIGATIONAL MASTERY ALIGNED"
    elif t < 8.5:
        state_str = "WARNING // BOUNDARY BREACH INITIATED"
        c_status = C_GOLD
        t_status = "LEGACY LOGIC APPLIED TO NEW MATRIX"
    else:
        state_str = "CATASTROPHIC SEMANTIC LEAK"
        c_status = C_MAGENTA
        t_status = "TOPOLOGICAL PARITY ZERO // PINNED"

    # ====================================================
    # 5. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    # Top Header [Strict Tuples]
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)
    
    ax.text(-500, 890, "LG-340a :: DIMENSIONAL TRUNCATION TENSOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] O(1) FALSE AUTHORITY & SEMANTIC RUPTURE", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    # Bottom Telemetry HUD
    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    ax.text(-500, -760, "SYS_01 [COGNITIVE NODE]      :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, state_str, color=c_status, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [ROUTING ALGORITHM]   :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, t_status, color=C_CYAN if t < 6.5 else (C_GOLD if t < 8.5 else C_MAGENTA), fontsize=15, fontname='monospace', weight='bold', zorder=82)

    # Audit Metric
    audit_text = "VERIFIED // IN-DOMAIN INTEGRITY" if t < 6.5 else ("PENDING CONSTRAINT COLLISION" if t < 8.5 else "FAIL // FALSE AUTHORITY DETECTED")
    ax.text(-500, -840, "SOVEREIGN AUDIT [REALITY]    :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, audit_text, color=C_MANTIS if t < 6.5 else (C_GOLD if t < 8.5 else C_MAGENTA), fontsize=15, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider [Strict Tuples]
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=c_status, zorder=83))

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
    print(f"LG-340a: DIMENSIONAL TRUNCATION TENSOR [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")
    
    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
