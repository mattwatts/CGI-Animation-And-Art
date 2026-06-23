"""
SOVEREIGN CODE: logic_garden_346d_latency_eradicated.py
SYSTEM: Python Multicore / O(1) Rigid Polygon Topology
SCENE: Logic Garden 346d (The Modern World // Latency Eradicated)
FORMAT: YouTube Shorts (1080x1920)
METADATA TARGETS: ALGORITHMIC PHYSICS, KINEMATIC ENGINEERING, OPERATIONS RESEARCH
HOTFIX: Linear 24.0s Sequence. Daylight Protocol. Camera Lock. Global Matrix Spliced.
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
OUT_DIR = "frames_346d_latency_eradicated"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE DAYLIGHT PROTOCOL + INDUSTRIAL ALLOY --------
C_BG        = '#FFFFFF'
C_TEXT      = '#020205'
C_TITANIUM  = '#E0E0E5'   # Background Grid / Brickwork
C_STEEL     = '#606065'   # The Bounding Box / Tracks / Engineering
C_DARK      = '#202025'   # Jagged Earth Substrate
C_CYAN      = '#00FFFF'   # Submarine Cable / High-Speed Data
C_GOLD      = '#FFB300'   # Biological Elements / Artisan Vectors
C_MAGENTA   = '#DE008A'   # Friction / Thermodynamic Waste / Latency
C_MANTIS    = '#00FF00'   # Terminal Green / O(1) Ping
C_WATER     = '#007FFF'   # Fluid Voids

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

def interp_path(dist, waypoints):
    # O(1) Vector Routing for ping packets across the rigid framework
    accum_d = 0.0
    for i in range(len(waypoints) - 1):
        p1, p2 = np.array(waypoints[i]), np.array(waypoints[i+1])
        seg_d = np.linalg.norm(p2 - p1)
        if dist <= accum_d + seg_d:
            prg = (dist - accum_d) / seg_d
            return p1 + (p2 - p1) * prg
        accum_d += seg_d
    return np.array(waypoints[-1])

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

    # 1. TIMELINE ARCHITECTURE
    # ------------------------
    T_BIOLOGICAL_END = 5.0
    T_DEPLOY_START = 5.0
    T_DEPLOY_END = 16.0
    T_MATRIX_LOCK = 17.0

    # 2. DEFINING THE JAGGED BIOLOGICAL TOPOLOGY
    # ------------------------------------------
    # Zone 1: GWR Land Matrix (-540 to -180) -> Jagged Mountains
    # Zone 2: Thames Subterranean (-180 to 180) -> River with deep clay bed
    # Zone 3: Pelagic Void (180 to 540) -> Deep Ocean
    
    # Earth Silhouette
    x_earth = np.linspace(-540, 540, 400)
    y_earth = []
    
    for x in x_earth:
        if x < -180:
            # Mountain Range
            y = 100 + 180 * np.sin(x * 0.02) + 50 * np.cos(x * 0.05)
        elif x < 180:
            # Thames Clay Bed
            y = -100 - 50 * np.cos((x + 180) * 0.015)
        else:
            # Ocean Trench Continental Drop
            y_base = -100 - 400 * np.clip((x - 180) / 100.0, 0.0, 1.0)
            y = y_base + 30 * np.sin(x * 0.03)
        y_earth.append(y)
    y_earth = np.array(y_earth)
    
    ax.fill_between(x_earth, -960, y_earth, facecolor=C_DARK, zorder=5)
    
    # Fluid Voids
    # Thames Fluid
    ax.fill_between([max(-180, x) for x in x_earth if x > -180 and x < 180], 
                    -100, 
                    [100 + 5*np.sin(t*3+x) for x in x_earth if x > -180 and x < 180], 
                    facecolor=C_WATER, alpha=0.6, zorder=6)
    # Pelagic Fluid
    ax.fill_between([max(180, x) for x in x_earth if x > 180], 
                    -500, 
                    [100 + 15*np.sin(t*2+x*0.02) for x in x_earth if x > 180], 
                    facecolor=C_WATER, alpha=0.6, zorder=6)
                    
    # Surface Line Plot
    ax.plot(x_earth, y_earth, color=C_TITANIUM, lw=4, zorder=7)

    # 3. HIGH-LATENCY BIOLOGICAL VECTORS (T=0 to T=8)
    # -----------------------------------------------
    if t < T_DEPLOY_END - 4.0:
        fade_bio = np.clip(1.0 - (t - T_DEPLOY_START)/2.0, 0.0, 1.0) if t > T_DEPLOY_START else 1.0
        
        # Horse Cart struggling over mountains
        cart_x = -540 + (t * 50) % 360
        cart_idx = np.abs(x_earth - cart_x).argmin()
        cart_y = y_earth[cart_idx] + 15
        
        ax.add_patch(patches.Rectangle((cart_x-15, cart_y), 30, 20, facecolor=C_GOLD, alpha=fade_bio, zorder=10))
        # Spallation / Friction Exhaust
        if t % 0.2 < 0.1:
            ax.scatter(cart_x - 10, cart_y - 10, c=C_MAGENTA, s=50, alpha=fade_bio, zorder=11)

        # Sailing ship bouncing on huge waves
        sail_x = 200 + (t * 25) % 340
        sail_y = 100 + 15*np.sin(t*2+sail_x*0.02)
        ax.plot([sail_x, sail_x], [sail_y, sail_y+50], color=C_GOLD, lw=4, alpha=fade_bio, zorder=10) # Mast
        ax.add_patch(patches.Polygon([(sail_x, sail_y+10), (sail_x+30, sail_y+10), (sail_x, sail_y+40)], facecolor=C_BG, edgecolor=C_GOLD, alpha=fade_bio, zorder=10))

    # 4. DOMAIN SEQUENCE OVERRIDES (T=5 to T=16)
    # ------------------------------------------
    deploy_prg = np.clip((t - T_DEPLOY_START) / (T_DEPLOY_END - T_DEPLOY_START), 0.0, 1.0)
    
    # SYSTEM 1: GWR LAND MATRIX (Flattening the Mountain)
    gwr_y = 100
    gwr_x_start, gwr_x_end = -540, -180
    current_gwr_x = gwr_x_start + (gwr_x_end - gwr_x_start) * ease_in_out(deploy_prg)
    
    if t >= T_DEPLOY_START:
        # The rigid line cutting the topology
        ax.plot([gwr_x_start, current_gwr_x], [gwr_y, gwr_y], color=C_STEEL, lw=12, zorder=20)
        # Viaduct columns dropping where terrain < 100
        dx_pillars = np.arange(-520, int(current_gwr_x), 40)
        for px in dx_pillars:
            p_idx = np.abs(x_earth - px).argmin()
            py = y_earth[p_idx]
            if py < gwr_y:
                ax.plot([px, px], [py, gwr_y], color=C_TITANIUM, lw=15, zorder=18)
                
        # The Excavating Train (The Razor)
        ax.add_patch(patches.Rectangle((current_gwr_x-40, gwr_y), 40, 25, facecolor=C_CYAN, zorder=21))
        # Spalling rock
        if deploy_prg < 1.0:
            ax.scatter(current_gwr_x, gwr_y, s=np.random.uniform(50, 150), c=C_MAGENTA, zorder=22)

    # SYSTEM 2: THE THAMES TUNNEL (Subterranean Drill)
    tunnel_y = -220
    tun_x_start, tun_x_end = -180, 180
    current_tun_x = tun_x_start + (tun_x_end - tun_x_start) * ease_in_out(deploy_prg)

    if t >= T_DEPLOY_START:
        # Rigid memory seal
        ax.plot([tun_x_start, current_tun_x], [tunnel_y, tunnel_y], color=C_TITANIUM, lw=20, solid_capstyle='round', zorder=20)
        ax.plot([tun_x_start, current_tun_x], [tunnel_y, tunnel_y], color=C_BG, lw=12, solid_capstyle='round', zorder=21)
        
        # The Shield (The Razor)
        ax.add_patch(patches.Rectangle((current_tun_x-15, tunnel_y-15), 20, 30, facecolor=C_STEEL, zorder=22))
        if deploy_prg < 1.0:
            ax.scatter(current_tun_x, tunnel_y, s=np.random.uniform(40, 100), c=C_MAGENTA, zorder=23)

    # SYSTEM 3: SS GREAT EASTERN (Telegraph Transatlantic Link)
    cable_y = -480
    ss_x_start, ss_x_end = 180, 540
    current_ss_x = ss_x_start + (ss_x_end - ss_x_start) * ease_in_out(deploy_prg)

    if t >= T_DEPLOY_START:
        # The Cable laying on the seabed
        ax.plot([ss_x_start, current_ss_x], [cable_y, cable_y], color=C_CYAN, lw=6, zorder=20)
        
        if deploy_prg < 1.0:
            # SS Great Eastern Silhouette
            ship_y = 100 + 10*np.sin(t+current_ss_x*0.02)
            hull_pts = [(current_ss_x-100, ship_y), (current_ss_x+80, ship_y), (current_ss_x+100, ship_y+30), (current_ss_x-100, ship_y+30)]
            ax.add_patch(patches.Polygon(hull_pts, facecolor=C_DARK, edgecolor=C_STEEL, lw=2, zorder=25))
            
            # The 5 iconic funnels
            for fx in range(-60, 61, 30):
                ax.plot([current_ss_x+fx, current_ss_x+fx], [ship_y+30, ship_y+70], color=C_DARK, lw=8, zorder=24)
                # Heavy Thermodynamics execution
                ax.scatter(current_ss_x+fx - t*10%20, ship_y+80 + t*15%30, s=np.random.uniform(50,150), c=C_MAGENTA, alpha=0.4, zorder=23)
            
            # Spooling cable down
            ax.plot([current_ss_x-80, current_ss_x-120], [ship_y, cable_y], color=C_CYAN, lw=2, zorder=19)

    # 5. THE MATRIX LOCK & TERMINAL GREEN FLOW (PING VECTORS)
    # -------------------------------------------------------
    # The Global Routing Matrix Waypoints
    net_pts = [
        (-540, 100), (-180, 100),            # GWR Subnet
        (-180, -220), (180, -220),           # Thames Drop + Tunnel
        (180, -480), (540, -480)             # Pelagic Drop + Telecom Cable
    ]

    # Render vertical hardware splices snapping into place
    if t >= T_DEPLOY_END:
        splice_alpha = np.clip((t - T_DEPLOY_END) / 1.0, 0.0, 1.0)
        c_splice = mcolors.to_rgba(C_GOLD, splice_alpha)
        # Drop shafts
        ax.plot([-180, -180], [100, -220], color=c_splice, lw=8, ls='dashed', zorder=15)
        ax.plot([180, 180], [-220, -480], color=c_splice, lw=8, ls='dashed', zorder=15)
        ax.scatter([-180, 180], [-220, -480], s=200, c=C_BG, edgecolor=c_splice, lw=4, zorder=26)

    # High-Frequency O(1) Ping Datastream
    if t >= T_MATRIX_LOCK:
        active_time = t - T_MATRIX_LOCK
        ping_speed = 1800 # Massive pixel velocity
        total_dist = 360 + 320 + 360 + 260 + 360 # Sum of line distances (approx)
        
        # Fire multiple packets at intervals
        for p_offset in [0.0, 0.3, 0.6, 0.9, 1.2]:
            p_time = active_time - p_offset
            if p_time > 0:
                p_dist = (p_time * ping_speed) % total_dist
                pos = interp_path(p_dist, net_pts)
                
                # Terminal Green logic pulse
                ax.scatter(pos[0], pos[1], s=300, facecolor=C_MANTIS, zorder=40)
                ax.add_patch(patches.Circle((pos[0], pos[1]), 40, fill=False, edgecolor=C_CYAN, lw=4, alpha=0.8, zorder=41))

    # ====================================================
    # 6. STATIC LOOP-SAFE ZERO-TEMPERATURE WIDGETS
    # ====================================================
    ax.add_patch(patches.Rectangle((-540, 800), 1080, 160, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [800, 800], color=C_TEXT, lw=4, zorder=81)

    ax.text(-500, 890, "LG-346d :: LATENCY ERADICATED", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', zorder=82)
    ax.text(-500, 845, "[SFI-0.50] DOMAIN SEQUENCE OVERRIDE // O(1) ROUTING LOCK", color=C_STEEL, fontsize=12, fontname='monospace', zorder=82)

    ax.add_patch(patches.Rectangle((-540, -960), 1080, 240, facecolor=C_TITANIUM, alpha=0.95, zorder=80))
    ax.plot([-540, 540], [-720, -720], color=C_TEXT, lw=4, zorder=81)

    # State Telemetry Logic
    if t < T_DEPLOY_START:
        s1, c1 = "BIOLOGICAL TOPOLOGY ACTIVE", C_MAGENTA
        s2, c2 = "HIGH C_MAGENTA LATENCY // O(N) TRAVEL", C_MAGENTA
        ping_str = "PING: > 2.5 MILLION MS // CONNECTION DROPPED"
    elif t < T_DEPLOY_END:
        s1, c1 = "THE SOVEREIGN FIX // DEPLOYING O(1) BOUNDARY", C_CYAN
        s2, c2 = "BRUNEL BASEPLATE FORCING VECTOR COMPLIANCE", C_GOLD
        ping_str = f"PING: HARDWARE ROUTING... {int((T_DEPLOY_END-t)*100)}%"
    elif t < T_MATRIX_LOCK:
        s1, c1 = "MATRIX TOPOLOGY LOCKED", C_STEEL
        s2, c2 = "GLOBAL SPLICES SECURED // BASEPLATE VERIFIED", C_GOLD
        ping_str = "PING: ESTABLISHING RIGID CONNECTION"
    else:
        s1, c1 = "THE MODERN WORLD CONCEPTION ONLINE", C_MANTIS
        s2, c2 = "LATENCY ERADICATED // TERMINAL GREEN FLOW", C_MANTIS
        ping_str = "PING: 001ms // ABSOLUTE SYNCHRONIZATION LOCKED"

    ax.text(-500, -760, "SYS_01 [INFRASTRUCTURE]      :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -760, s1, color=c1, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -800, "SYS_02 [THERMODYNAMIC STATE] :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -800, s2, color=c2, fontsize=15, fontname='monospace', weight='bold', zorder=82)

    ax.text(-500, -840, "STRUCTURAL LOAD AUDIT        :", color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)
    ax.text(20, -840, ping_str, color=C_TEXT, fontsize=14, fontname='monospace', weight='bold', zorder=82)

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
    print(f"LG-346d: LATENCY ERADICATED [CORES: {cpu_cores}] [CAMERA LOCK ACTIVE]")

    with mp.Pool(processes=cpu_cores, maxtasksperchild=1) as pool:
        for _ in pool.imap_unordered(render_frame, generate_stream(), chunksize=1):
            pass

if __name__ == "__main__":
    mp.freeze_support()
    run_batch()
