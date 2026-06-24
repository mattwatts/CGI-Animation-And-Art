"""
SOVEREIGN CODE: logic_garden_317_orbital_shipyard.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 317 (The Orbital Shipyard)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, MEGASCAE ARCHITECTURE
HOTFIX: Implemented Static Gantry Lattice & Vertical Supply Kinematics.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import multiprocessing as mp
import os
import gc

# ======== ARCHITECT CONDITIONAL LOGIC ========
DURATION = 10.0  # 10.0 Second Seamless Loop
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_317_orbital_shipyard"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#A0A0A5'
C_STEEL     = '#303035'
C_GOLD      = '#FFB300'   # Internal Energy Spine / Exposed Engineering
C_AZURE     = '#007FFF'   # Supply Mag-Rails
C_CYAN      = '#00FFFF'   # Welding Spallation Sparks
C_WHITE     = '#FFFFFF'

# ------------------------------------------------------------------
# O(1) METALLIC SHADER
# ------------------------------------------------------------------
def draw_cylinder(ax, y_bottom, y_top, radius, zorder=5, color_base=C_STEEL, is_horizontal=False, x_center=0):
    steps = 40 
    r_val, g_val, b_val = [int(color_base.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)]
    
    for i in range(steps):
        ratio = (i / float(steps - 1))
        # Hard spec highlight simulating raw zero-atmosphere lighting
        light_curve = np.exp(-((ratio - 0.35) ** 2) / 0.04) 
        ambient = 0.2 + 0.8 * light_curve
        c = f'#{int(r_val*ambient):02x}{int(g_val*ambient):02x}{int(b_val*ambient):02x}'
        
        w = (radius * 2) / steps
        x_start = x_center - radius + (i * w)
        
        if not is_horizontal:
            rect = patches.Rectangle((x_start, y_bottom), w, y_top - y_bottom, facecolor=c, edgecolor='none', zorder=zorder)
        else:
            rect = patches.Rectangle((y_bottom, x_start), y_top - y_bottom, w, facecolor=c, edgecolor='none', zorder=zorder)
        ax.add_patch(rect)

def draw_gantry_arm(ax, y_anchor, side='left', zorder=8):
    # Brutalist angular scaffolding arms clamping onto the hull
    sign = -1 if side == 'left' else 1
    
    # Base anchor connecting to the outer rails
    poly_base = patches.Polygon([
        [sign * 480, y_anchor - 40], [sign * 400, y_anchor - 40],
        [sign * 400, y_anchor + 40], [sign * 480, y_anchor + 40]
    ], facecolor=C_TEXT, zorder=zorder)
    
    # Angled thrust arm extending to the ship hull
    poly_arm = patches.Polygon([
        [sign * 400, y_anchor - 30], [sign * 180, y_anchor - 80],
        [sign * 180, y_anchor - 40], [sign * 400, y_anchor + 30]
    ], facecolor=C_STEEL, zorder=zorder)
    
    # Locking clamp touching the hull
    poly_clamp = patches.Polygon([
        [sign * 180, y_anchor - 100], [sign * 160, y_anchor - 100],
        [sign * 160, y_anchor - 20], [sign * 180, y_anchor - 20]
    ], facecolor=C_TITANIUM, zorder=zorder+0.1)

    ax.add_patch(poly_base)
    ax.add_patch(poly_arm)
    ax.add_patch(poly_clamp)

# ------------------------------------------------------------------
# SUPPLY RAIL KINEMATICS (O(1) CACHED ARRAYS)
# ------------------------------------------------------------------
N_CARGO = 24
c_x = np.random.choice([-450, -420, 420, 450], N_CARGO)
c_y_offset = np.random.uniform(0, 1920, N_CARGO)
c_h = np.random.uniform(60, 140, N_CARGO)
c_w = 20

# Welding spark locations (Mapped strictly to exposed gold spine segments)
w_x = np.random.uniform(-100, 100, 30)
w_y = np.random.uniform(-400, 400, 30)

def render_frame(packet):
    f, phase_ratio = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)

    # 1. THE EXPOSED STARSHIP SPINE (Z=3)
    # This acts as the raw inner conduit of the ship being built
    draw_cylinder(ax, -800, 800, radius=90, color_base=C_GOLD, zorder=3)
    
    # Internal mechanical ribbing across the gold spine
    for spine_y in range(-780, 780, 60):
        draw_cylinder(ax, spine_y, spine_y+15, radius=95, color_base=C_TEXT, zorder=3.1)

    # 2. THE OUTER HULL PLATING (Z=4)
    # The Bounding Box of the ship, left partially constructed
    # Upper Hull Module
    draw_cylinder(ax, 200, 800, radius=180, color_base=C_TITANIUM, zorder=4)
    # Lower Hull Module
    draw_cylinder(ax, -800, -200, radius=180, color_base=C_TITANIUM, zorder=4)
    
    # Middle Hull Module (Being welded / assembled)
    # Left incomplete, exposing the gold spine inside
    rect_hull_patch = patches.Rectangle((-180, -200), 100, 400, facecolor=C_TITANIUM, zorder=4.1)
    ax.add_patch(rect_hull_patch)
    rect_hull_patch_2 = patches.Rectangle((80, -200), 100, 400, facecolor=C_TITANIUM, zorder=4.1)
    ax.add_patch(rect_hull_patch_2)

    # 3. GANTRY LATTICE / THE SHIPYARD FRAME (Z=2 && Z=8)
    # Massive outer vertical pylons
    draw_cylinder(ax, -960, 960, radius=30, color_base=C_STEEL, x_center=-450, zorder=8)
    draw_cylinder(ax, -960, 960, radius=30, color_base=C_STEEL, x_center=-420, zorder=2) # Background rail
    draw_cylinder(ax, -960, 960, radius=30, color_base=C_STEEL, x_center=450, zorder=8)
    draw_cylinder(ax, -960, 960, radius=30, color_base=C_STEEL, x_center=420, zorder=2)

    # Gantry Clamp Arms (Holding the hull at Z=8)
    for gantry_y in [-600, -300, 0, 300, 600]:
        draw_gantry_arm(ax, gantry_y, side='left', zorder=8)
        draw_gantry_arm(ax, gantry_y, side='right', zorder=8)

    # 4. KINEMATICS: MAG-RAIL CARGO UMBILICALS (Z=8.5)
    # Perfect Modulus 1920 wrap for the 10-second loop
    v_cargo = 1920.0
    cargo_y_current = ((c_y_offset + phase_ratio * v_cargo) % 1920) - 960
    
    for i in range(N_CARGO):
        # We enforce cargo blocks on the Z=8 and Z=2 rails appropriately
        cy = cargo_y_current[i]
        c_z = 8.5 if abs(c_x[i]) == 450 else 2.5
        rect = patches.Rectangle((c_x[i] - c_w/2, cy), c_w, c_h[i], facecolor=C_TEXT, edgecolor=C_AZURE, lw=2, zorder=c_z)
        ax.add_patch(rect)

    # 5. KINEMATICS: O(1) INDUSTRIAL WELDING SPARKS (Eulerian Spallation)
    # Sparks pulse mathematically using independent offset frequencies to simulate active construction
    np.random.seed(int(f/3)) # High frequency noise seed for harsh spark flicker
    for i in range(30):
        # Determine strict pulsing logic
        spark_phase = np.sin((phase_ratio * 2 * np.pi) * (10 + i%5) + i)
        if spark_phase > 0.5:
            # Active welding spike
            base_x = w_x[i]
            base_y = w_y[i]
            # Flash core
            ax.add_patch(patches.Circle((base_x, base_y), radius=np.random.uniform(3, 8), color=C_WHITE, zorder=4.5))
            # Spallation flare
            ax.add_patch(patches.Polygon([
                [base_x - 30, base_y], [base_x + 30, base_y], 
                [base_x, base_y - np.random.uniform(20, 80)]
            ], facecolor=C_CYAN, alpha=0.8, zorder=4.4))

    # 6. ZERO-TEMPERATURE WIDGETS
    ax.text(-500, 880, "LG-317 :: ORBITAL SHIPYARD", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=80)
    ax.text(-500, 840, "[SFI-1.00] VANGUARD ASSEMBLY CONDUIT // RIGID LATTICE", color=C_TEXT, fontsize=12, fontname='monospace', zorder=80)
    
    # Telemetry
    ax.text(-500, -840, "MAG-RAIL LOGISTICS // UMBILICAL THROUGHPUT", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=80)
    ax.add_patch(patches.Rectangle((-500, -860), 1000, 4, facecolor=C_TITANIUM, zorder=80))
    ax.add_patch(patches.Rectangle((-500, -860), 1000 * phase_ratio, 4, facecolor=C_AZURE, zorder=81))

    # Structural Callouts
    ax.text(-120, -180, "C_GOLD\nENERGY SPINE\nEXPOSED", color=C_TEXT, fontsize=10, fontname='monospace', zorder=80)
    ax.plot([-70, 0], [-130, -50], color=C_TEXT, lw=1.5, zorder=80) 

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0)
    fig.clf(); plt.close(fig); gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = mp.cpu_count()
    with mp.Pool(processes=cpu_cores) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
