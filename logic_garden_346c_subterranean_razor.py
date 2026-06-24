"""
SOVEREIGN CODE: logic_garden_346c_subterranean_razor.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 346c (The Thames Tunnel // The Subterranean Razor)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING, OPERATIONS RESEARCH
HOTFIX: Linear 24.0s Sequence. Dead-space eradicated. 3x 8.0s Execution Cycles.
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
OUT_DIR = "frames_346c_subterranean_razor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Brickwork Seal / Secured Topology
C_STEEL     = '#606065'   # The Bounding Box / Tunnel Shield
C_DARK      = '#202025'   # Clay Substrate
C_CYAN      = '#00FFFF'   # Hydraulic Advancement Rams
C_GOLD      = '#FFB300'   # Excavation Target Volume
C_MAGENTA   = '#DE008A'   # Thermodynamic Pressure Vectors (Threat)
C_MANTIS    = '#00FF00'   # Terminal Green / Secured Roof
C_WATER     = '#007FFF'   # Thames River Mass

# ------------------------------------------------------------------
# O(1) KINEMATIC FUNCTIONS
# ------------------------------------------------------------------
def ease_in_out(t):
    t = np.clip(t, 0.0, 1.0)
    return 4 * t**3 if t < 0.5 else 1 - (-2 * t + 2)**3 / 2

def draw_industrial_grid(ax):
    for i in range(-5, 6):
        ax.plot([i*100, i*100], [-960, 960], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)
    for j in range(-9, 10):
        ax.plot([-540, 540], [j*100, j*100], color=C_TITANIUM, lw=1, alpha=0.3, zorder=0)

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

    # 1. KINEMATICS LOGIC MATRIX: O(1) SERIALIZATION (Zero Dead Space)
    # ----------------------------------------------------------------
    cycle_duration = 8.0
    cycle_idx = int(t // cycle_duration)
    if cycle_idx > 2: cycle_idx = 2 # Clamp to final 3rd cycle for precision at f=1439
    
    c_time = t % cycle_duration
    if t >= DURATION:
        c_time = cycle_duration
        
    base_s_x = -400 + cycle_idx * 200
    base_b_x = -550 + cycle_idx * 200
    start_earth_x = -300 + cycle_idx * 200
    
    if c_time < 3.0:
        # PHASE A: Node Excavation (3.0s)
        op_phase = "EXCAVATE"
        excavate_prg = ease_in_out(c_time / 3.0)
        shield_x = base_s_x
        brick_x = base_b_x
        earth_x = start_earth_x + (200 * excavate_prg)
    elif c_time < 6.0:
        # PHASE B: Hydraulic Override (3.0s)
        op_phase = "RAM_PUSH"
        push_prg = ease_in_out((c_time - 3.0) / 3.0)
        shield_x = base_s_x + 200 * push_prg
        brick_x = base_b_x
        earth_x = start_earth_x + 200
    else:
        # PHASE C: Memory Annhilation (Brick Seal - 2.0s)
        op_phase = "BRICK_SEAL"
        seal_prg = ease_in_out((c_time - 6.0) / 2.0)
        shield_x = base_s_x + 200
        brick_x = base_b_x + 200 * seal_prg
        earth_x = start_earth_x + 200

    shield_front_x = shield_x + 100

    # 2. THE TOPOLOGICAL THREAT (THAMES RIVER & CLAY)
    # -----------------------------------------------
    # River Surface
    x_river = np.linspace(-600, 600, 100)
    y_river = 550 + 20 * np.sin(x_river * 0.02 + t * 4) + 15 * np.cos(x_river * 0.035 - t * 2)
    
    # Substrate Ceilings & Floors
    Y_ROOF_TOP = 350
    Y_ROOF_BOT = 150
    Y_FLOOR_TOP = -450
    
    # Water Mass
    ax.fill_between(x_river, Y_ROOF_TOP, y_river, facecolor=C_WATER, alpha=0.4, zorder=5)
    ax.plot(x_river, y_river, color=C_WATER, lw=6, zorder=6)
    
    # Hard bounds of the riverbed
    ax.plot([-600, 600], [Y_ROOF_TOP, Y_ROOF_TOP], color=C_DARK, lw=8, zorder=4)
    
    # Clay Matrix (Background Z-order locks to form the void)
    ax.add_patch(patches.Rectangle((-600, Y_ROOF_BOT), 1200, Y_ROOF_TOP - Y_ROOF_BOT, facecolor=C_DARK, zorder=2)) # Roof layer
    ax.add_patch(patches.Rectangle((-600, -960), 1200, Y_FLOOR_TOP - (-960), facecolor=C_DARK, zorder=2)) # Floor layer
    ax.add_patch(patches.Rectangle((earth_x, Y_FLOOR_TOP), 1200, Y_ROOF_BOT - Y_FLOOR_TOP, facecolor=C_DARK, zorder=2)) # Unmined face

    # Threat Vectors (Magnifying Roof Stress immediately mapping active terrain)
    arrow_xs = np.arange(-500, 550, 100)
    for ax_x in arrow_xs:
        if ax_x <= brick_x:
            c_arr = C_MANTIS # Terminal Green holding roof (Sealed)
        elif ax_x <= shield_front_x:
            c_arr = C_CYAN   # Shield isolating threat
        elif ax_x <= earth_x:
            c_arr = C_MAGENTA # Void threat boundary (Active tunneling face)
        else:
            c_arr = C_GOLD   # Solid intact matrix ahead
        
        alpha_arr = 0.8 + 0.2 * np.sin(t*15 + ax_x) if c_arr == C_MAGENTA else 0.8
        # Plunging arrow transmitting fluid pressure into the roof
        ax.arrow(ax_x, Y_ROOF_TOP - 20, 0, -110, head_width=25, head_length=20, fc=c_arr, ec=C_BG, lw=5, alpha=alpha_arr, zorder=15)

    # 3. KINEMATIC DIG OPERATIONS (Node Execution)
    # --------------------------------------------
    if op_phase == "EXCAVATE":
        ax.scatter(earth_x, np.random.uniform(Y_FLOOR_TOP, Y_ROOF_BOT), s=np.random.uniform(100,400), c=C_MAGENTA, marker='x', lw=3, zorder=12) 
        ax.scatter(earth_x + 5, np.random.uniform(Y_FLOOR_TOP, Y_ROOF_BOT), s=np.random.uniform(50,200), c=C_CYAN, zorder=12) 
        ax.plot([earth_x, earth_x], [Y_FLOOR_TOP, Y_ROOF_BOT], color=C_GOLD, lw=10, zorder=3)

    # 4. THE CAST-IRON BOUNDING BOX (Shield Architecture)
    # ---------------------------------------------------
    # Tail Extensions supporting the roof absolutely between brick and shield
    ax.add_patch(patches.Rectangle((brick_x, Y_ROOF_BOT - 10), shield_front_x - brick_x, 10, facecolor=C_STEEL, zorder=8))
    ax.add_patch(patches.Rectangle((brick_x, Y_FLOOR_TOP), shield_front_x - brick_x, 10, facecolor=C_STEEL, zorder=8))

    # The O(1) Matrix Core (The Shield itself)
    ax.add_patch(patches.Rectangle((shield_x, Y_FLOOR_TOP), 100, Y_ROOF_BOT - Y_FLOOR_TOP, facecolor=C_STEEL, edgecolor=C_BG, lw=4, zorder=10))
    # Horizontal compartment splitters (The 3 worker decks)
    ax.plot([shield_x, shield_front_x], [-250, -250], color=C_BG, lw=6, zorder=11)
    ax.plot([shield_x, shield_front_x], [-50, -50], color=C_BG, lw=6, zorder=11)
    
    # 5. O(1) MEMORY ANNIHILATION (C_TITANIUM Brickwork Seal)
    # -------------------------------------------------------
    # Top and Bottom Arches permanently locking out the matrix
    ax.add_patch(patches.Rectangle((-600, Y_ROOF_BOT - 30), brick_x - (-600), 30, facecolor=C_TITANIUM, edgecolor=C_STEEL, lw=2, zorder=7))
    ax.add_patch(patches.Rectangle((-600, Y_FLOOR_TOP), brick_x - (-600), 30, facecolor=C_TITANIUM, edgecolor=C_STEEL, lw=2, zorder=7))
    
    # Mortar lines ensuring structural seal reality
    for rx in np.arange(-600, brick_x, 40):
        ax.plot([rx, rx], [Y_ROOF_BOT - 30, Y_ROOF_BOT], color=C_STEEL, lw=3, zorder=8)
        ax.plot([rx, rx], [Y_FLOOR_TOP, Y_FLOOR_TOP + 30], color=C_STEEL, lw=3, zorder=8)

    # 6. HYDRAULIC ADVANCEMENT RAMS
    # -----------------------------
    ram_ys = [-350, -150, 50]
    for ry in ram_ys:
        # Anchor cylinders attached to brick wall
        ax.add_patch(patches.Rectangle((brick_x, ry-15), min(shield_x - brick_x, 90), 30, facecolor=C_DARK, edgecolor=C_STEEL, lw=3, zorder=9))
        # The Cyan Piston
        ax.plot([brick_x, shield_x], [ry, ry], color=C_CYAN, lw=12, zorder=8)
        
        # Kinetic visual for high fluid pressure during extension
        if op_phase == "RAM_PUSH":
            for _ in range(3):
                kx = np.random.uniform(brick_x + 90, shield_x)
                if kx < shield_x:
                    ax.plot([kx, kx], [ry-20, ry+20], color=C_BG, lw=4, zorder=12)

    # ====================================================
    # 7. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)

    ax.text(-500, 890, "LG-346c :: THE SUBTERRANEAN RAZOR", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-1.00] MAXTASKSPERCHILD=1 // O(1) TOPOLOGICAL ANNIHILATION", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    # State Telemetry Logic
    if op_phase == "EXCAVATE":
        s1, c1 = "SERIALIZATION ROUTINE // CELL EXTRACTION", C_CYAN
        s2, c2 = "EXTRACTING SUBSTRATE KINEMATICALLY", C_GOLD
        aud_str = "C_STEEL SHIELD MAINTAINING ROOF ISOLATION"
    elif op_phase == "RAM_PUSH":
        s1, c1 = "C_CYAN HYDRAULIC OVERRIDE ENGAGED", C_CYAN
        s2, c2 = "FORCING BASEPLATE THROUGH FLUID BOUNDARIES", C_CYAN
        aud_str = "TERMINAL THRUST SECURED // ADVANCING"
    elif op_phase == "BRICK_SEAL":
        s1, c1 = "C_TITANIUM MEMORY SEALING IN PROGRESS", C_MANTIS
        s2, c2 = "BRICKWORK TOPOLOGY LOCKED AGAINST MATRIX", C_MANTIS
        aud_str = "GEOMETRIC ANNIHILATION OF THE VOID DANGER"

    ax.text(-500, -760, "SYS_01 [O(1) SERIALIZATION]  :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, s1, color=c1, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [EXECUTION PHASE]     :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, s2, color=c2, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, f"CYCLE AUDIT [ITERATION {cycle_idx+1}/3] :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, aud_str, color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    # Master Chronology Slider [Strict Tuples]
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=c1, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close('all')
    gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-346c: THE SUBTERRANEAN RAZOR [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
