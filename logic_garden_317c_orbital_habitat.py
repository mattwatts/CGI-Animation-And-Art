"""
CODE: logic_garden_317c_orbital_habitat.py
SYSTEM: Python Multicore / Rigid Polygon Topology
SCENE: Logic Garden 317c (Orbital Shipyard // The Rotating Megascale Habitat)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ASTROPHYSICS, SPACE SETTLEMENT, PROCEDURAL ARCHITECTURE
HOTFIX: Data structure tuple fix in get_shipyard_geometry().
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
DURATION = 24.0
FPS = 60
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_317c_orbital_habitat"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- VISUAL PALETTE (HIGH VISIBILITY) --------
C_BG        = '#FFFFFF'   # Base void
C_TEXT      = '#020205'
C_TITANIUM  = '#A0A0A5'
C_STEEL     = '#2C2F33'   # Heavy structure
C_HULL      = '#E3E5E8'   # Starship Armor
C_GOLD      = '#FFB300'   # Energy / Hub Core
C_AZURE     = '#007FFF'   # Spoke Transit
C_CYAN      = '#00F0FF'   # Megacity Nodes
C_HABITAT   = '#10B981'   # 1G Biosphere / Forest Zones
C_GLASS     = '#D0F0FF'   # Translucent Atmosphere Retainer

# ------------------------------------------------------------------
# PROCEDURAL GEOMETRY CACHING
# ------------------------------------------------------------------
# We pre-calculate all static structural polygons in unrotated world space
# to allow instantaneous rendering across extreme scaling factors.
WORLD_POLYS = []

def push_poly(pts, color, z, alpha=1.0):
    WORLD_POLYS.append((np.array(pts), color, z, alpha))

def get_shipyard_geometry():
    """Generates the local shipyard module matching LG-317 proportions"""
    polys = []
    # Core Spine (Gold) wrapped accurately as (geometry_list, color, z_index)
    polys.append(( [[-100, -800], [100, -800], [100, 800], [-100, 800]], C_GOLD, 3 ))
    # Hull Modules (Titanium)
    polys.append(( [[-200, 300], [200, 300], [200, 800], [-200, 800]], C_HULL, 4 ))
    polys.append(( [[-200, -800], [200, -800], [200, -200], [-200, -200]], C_HULL, 4 ))
    # Gantry Clamp Arms (Dark Steel)
    for gy in [-500, -200, 100, 400]:
        polys.append(( [[-500, gy-30], [-200, gy-60], [-200, gy-20], [-500, gy+30]], C_STEEL, 8 ))
        polys.append(( [[500, gy-30], [200, gy-60], [200, gy-20], [500, gy+30]], C_STEEL, 8 ))
    # Base structural rails
    polys.append(( [[-400, -960], [-350, -960], [-350, 960], [-400, 960]], '#222225', 2 ))
    polys.append(( [[350, -960], [400, -960], [400, 960], [350, 960]], '#222225', 2 ))
    return polys

# Build Central Hub Core
for a1, a2 in zip(np.linspace(0, 2*np.pi, 60)[:-1], np.linspace(0, 2*np.pi, 60)[1:]):
    p_core = [[4000*np.cos(a1), 4000*np.sin(a1)], [4000*np.cos(a2), 4000*np.sin(a2)], [0,0], [0,0]]
    push_poly(p_core, '#FFDD44', 1.0)
    p_inner = [[2500*np.cos(a1), 2500*np.sin(a1)], [2500*np.cos(a2), 2500*np.sin(a2)], [0,0], [0,0]]
    push_poly(p_inner, '#FFAA00', 1.1)

# Build the 48km Diameter Rotating Biosphere Ring
steps = 240
for i in range(steps):
    a1 = i * 2 * np.pi / steps
    a2 = (i+1) * 2 * np.pi / steps
    
    # Outer Reinforced Hull
    p_out = [
        [22000*np.cos(a1), 22000*np.sin(a1)], [24000*np.cos(a1), 24000*np.sin(a1)],
        [24000*np.cos(a2), 24000*np.sin(a2)], [22000*np.cos(a2), 22000*np.sin(a2)]
    ]
    push_poly(p_out, '#33363D', 2.0)
    
    # Inner Habitation Topology (Forests & High-Density Zones)
    p_in = [
        [21000*np.cos(a1), 21000*np.sin(a1)], [22000*np.cos(a1), 22000*np.sin(a1)],
        [22000*np.cos(a2), 22000*np.sin(a2)], [21000*np.cos(a2), 21000*np.sin(a2)]
    ]
    hab_color = C_HABITAT if (i % 7) < 5 else C_CYAN 
    push_poly(p_in, hab_color, 2.1)
    
    # Atmospheric Retainer Shell (Translucent Glass)
    p_glass = [
        [20000*np.cos(a1), 20000*np.sin(a1)], [21000*np.cos(a1), 21000*np.sin(a1)],
        [21000*np.cos(a2), 21000*np.sin(a2)], [20000*np.cos(a2), 20000*np.sin(a2)]
    ]
    push_poly(p_glass, C_GLASS, 2.2, alpha=0.35)

# Assemble Sparks, Spokes, and the Shipyard Matrices
ship_template = get_shipyard_geometry()

for s in range(6):
    angle = s * np.pi / 3
    ca, sa = np.cos(angle), np.sin(angle)
    
    def rot_pt(x, y): return [x * ca - y * sa, x * sa + y * ca]
    
    # Primary Transit Spoke Truss
    spk = [rot_pt(-800, 3000), rot_pt(800, 3000), rot_pt(800, 20000), rot_pt(-800, 20000)]
    push_poly(spk, '#D3D5D8', 4.0)
    
    # High-Strength Cross Braces
    for yb in np.linspace(4000, 19000, 18):
        b1 = [rot_pt(-800, yb), rot_pt(-600, yb), rot_pt(800, yb+1000), rot_pt(600, yb+1000)]
        b2 = [rot_pt(800, yb), rot_pt(600, yb), rot_pt(-800, yb+1000), rot_pt(-600, yb+1000)]
        push_poly(b1, C_STEEL, 4.1)
        push_poly(b2, C_STEEL, 4.1)
        
    # Standardized Orbital Shipyards along the Spar
    # Rad = 10000 exactly aligns with Spoke 0 for our tracking start position
    for rad in np.arange(4000, 20000, 2000):
        for data in ship_template:
            poly_pts, color, z_order = data[0], data[1], data[2]
            offset_poly = [[p[0], p[1] + rad] for p in poly_pts]
            rot_poly = [rot_pt(p[0], p[1]) for p in offset_poly]
            push_poly(rot_poly, color, 4.2 + z_order/10.0)

def render_frame(packet):
    f, phase_ratio = packet
    t = phase_ratio * DURATION

    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)

    # CAMERA LOCK
    ax.set_xlim(-540, 540)
    ax.set_ylim(-960, 960)
    ax.autoscale(False)

    # 1. ROTATION PARAMETERS
    # Omega = 0.0211 rad/s generates ~9.79 m/s^2 acceleration at R=22,000m
    w_speed = 0.0211
    theta_W = w_speed * t

    # 2. EXPONENTIAL CAMERA TRANSITION ROUTINE
    # ----------------------------------------
    T_ZOOM_START = 4.0
    T_ZOOM_END = 18.0
    
    zoom_prg = np.clip((t - T_ZOOM_START) / (T_ZOOM_END - T_ZOOM_START), 0.0, 1.0)
    ease = zoom_prg ** 3.0  # Deep exponential transition for vastly expanding scale
    
    # Ground Truth target: Spoke 0, R=10000 (Matches LG-317 framing)
    ship_cam_x = -10000 * np.sin(theta_W)
    ship_cam_y =  10000 * np.cos(theta_W)
    ship_cam_rot = theta_W
    
    # Final Camera Anchor Point: True Space Center (0,0)
    final_cam_x, final_cam_y, final_cam_rot = 0, 0, 0
    
    # Blending the Camera Coordinates
    cam_x = ship_cam_x * (1 - ease) + final_cam_x * ease
    cam_y = ship_cam_y * (1 - ease) + final_cam_y * ease
    cam_rot = ship_cam_rot * (1 - ease) + final_cam_rot * ease
    
    # Zoom Expansion (1.0 captures tight 1080x1920 slot; 28.0 perfectly captures a 44k diameter grid)
    cam_zoom = 1.0 * (1 - ease) + 28.0 * ease

    # 3. WORLD TRANSFORMATION MATRIX ROUTING
    # --------------------------------------
    cw, sw = np.cos(theta_W), np.sin(theta_W)
    cc, sc = np.cos(-cam_rot), np.sin(-cam_rot)

    # Cache valid patches
    patch_list = []
    
    for poly, fc, z_order, a_val in WORLD_POLYS:
        x = poly[:, 0]
        y = poly[:, 1]
        
        # World Physics Rotation
        x_w = x * cw - y * sw
        y_w = x * sw + y * cw
        
        # Camera Translation
        x_t = x_w - cam_x
        y_t = y_w - cam_y
        
        # Camera Orientation
        x_c = x_t * cc - y_t * sc
        y_c = x_t * sc + y_t * cc
        
        # Camera Zoom Scale
        x_s = x_c / cam_zoom
        y_s = y_c / cam_zoom
        
        # Strict Frustum Cull (Major performance boost during Phase 1 tight view)
        if np.max(x_s) < -640 or np.min(x_s) > 640 or np.max(y_s) < -1060 or np.min(y_s) > 1060:
            continue
            
        screen_poly = np.column_stack((x_s, y_s))
        patch_list.append((screen_poly, fc, z_order, a_val))
        
    # Standard Z-Sort
    patch_list.sort(key=lambda item: item[2])
    
    for item in patch_list:
        ax.add_patch(patches.Polygon(item[0], facecolor=item[1], edgecolor='none', alpha=item[3], zorder=item[2]))

    # 4. LIVING DETAILS (Only rendered when zoom permits visibility)
    # --------------------------------------------------------------
    if cam_zoom < 3.0:
        np.random.seed(int(t * 10) + 317)
        # Lock active welding sparks exclusively to our local focal shipyard
        for _ in range(12):
            wx = np.random.uniform(-150, 150)
            wy = np.random.uniform(-300, 300)
            x_w = wx * cw - wy * sw + ship_cam_x
            y_w = wx * sw + wy * cw + ship_cam_y
            
            x_t, y_t = x_w - cam_x, y_w - cam_y
            x_s = (x_t * cc - y_t * sc) / cam_zoom
            y_s = (x_t * sc + y_t * cc) / cam_zoom
            
            ax.add_patch(patches.Circle((x_s, y_s), radius=np.random.uniform(4, 12)/cam_zoom, color='#FFFFFF', zorder=10.0))

    # ====================================================
    # 5. VISUAL TELEMETRY WIDGETS
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)

    ax.text(-500, 890, "LG-317c :: MACRO HABITAT SCALE", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "THE VANGUARD RING // 1G ROTATIONAL METRIC", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    if t < T_ZOOM_START:
        s1, c1 = "ORBITAL SHIPYARD // LOCAL VIEW", C_TEXT
        s2, c2 = "ASSEMBLY SPAR 001 ACTIVE", C_AZURE
        t_state = f"LOCAL TRACKING SET // ZOOM: {cam_zoom:.1f}X"
    elif t < T_ZOOM_END:
        s1, c1 = "EXPONENTIAL FOCAL EXPANSION", C_TEXT
        s2, c2 = "SCALE DISCLOSURE IN PROGRESS", C_STEEL
        t_state = f"UNTETHERING FROM ROTATIONAL FRAME // ZOOM: {cam_zoom:.1f}X"
    else:
        s1, c1 = "O'NEILL CYLINDER // HABITAT RING", C_HABITAT
        s2, c2 = "DIAMETER: 48 KILOMETERS // RADIUS: 24,000 M", C_CYAN
        t_state = f"MACRO-STRUCTURE IDENTIFIED // METRICS SECURED"

    ax.text(-500, -760, "SYS_01 [FRAMING BOUNDS]      :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, s1, color=c1, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [DATA METRICS]        :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, s2, color=c2, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "STATUS TRACKING              :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, t_state, color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)

    # Sequence Timeline
    ax.add_patch(patches.Rectangle((-500, -890), 1000, 6, facecolor=C_STEEL, zorder=82))
    ax.add_patch(patches.Rectangle((-500, -890), 1000 * phase_ratio, 6, facecolor=C_AZURE, zorder=83))

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0)
    plt.close('all')
    gc.collect()

    return f

def generate_stream():
    for f in range(TOTAL_FRAMES):
        yield (f, f / float(TOTAL_FRAMES))

def run_batch():
    cpu_cores = max(1, mp.cpu_count() - 1)
    print(f"LG-317c: ORBITAL HABITAT TRAVERSAL [CORES: {cpu_cores}] [CAMERA UNTETHERING ACTIVE]")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
