"""
SOVEREIGN CODE: logic_garden_204_kirov_deletion.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Kinematic Erasure Tensor (17.5 seconds)
SCENE: Logic Garden 204 (The Kirov Deletion / Thermodynamic Spine Fracture)
HOTFIX: Incompressible Fluid Shockwave Arrays, Boolean Masking, Radar Radius Matrix
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle, Circle, Wedge
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_204_kirov_deletion"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'        # Thermodynamic Vacuum / Ocean Depths
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'        # Dark Architecture
C_CYAN      = '#00FFFF'        # Stealth Intercept Vectors / Sub-surface Void
C_MAGENTA   = '#FF0055'        # Legacy Thermal Friction / Kirov Bloom
C_GOLD      = '#FFD700'        # Kinetic Spallation / Shockwave
C_RED       = '#FF3300'        # Dimensional Compiler Crash
C_MANTIS    = '#00FF00'        # Terminal Geometry (Tathata / The Broken Spine)

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_void = np.array(hex_to_rgba(C_VOID)[:3])
c_cyan = np.array(hex_to_rgba(C_CYAN)[:3])
c_mage = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_gold = np.array(hex_to_rgba(C_GOLD)[:3])
c_mant = np.array(hex_to_rgba(C_MANTIS)[:3])
c_txt  = np.array(hex_to_rgba(C_TEXT)[:3])

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE KINEMATIC ARCHITECTURE
# ------------------------------------------------------------------
MAX_PARTICLES = 25000
CENTER_X = 0.0  
CENTER_Y = 0.0

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, px, py, p_sizes, c_tensor, cam_w, radar_r, spine_angle, torpedo_y, is_flash, is_tathata, bg_strobe = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_TEXT if is_flash else C_VOID
    if bg_strobe and not is_tathata: bg_hex = '#0F0005' 
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    # Invert Y logic: Negative is underwater, positive is airspace
    cam_h = cam_w * (1920.0 / 1080.0)
    ax.set_xlim(CENTER_X - cam_w/2, CENTER_X + cam_w/2)
    ax.set_ylim(CENTER_Y - cam_h*0.3, CENTER_Y + cam_h*0.7) 

    # 1. THE TOPOLOGICAL GRIDS
    if not is_flash and not is_tathata:
        # Waterline
        ax.plot([CENTER_X - cam_w, CENTER_X + cam_w], [0, 0], color=C_DIM, lw=2, zorder=1)
        # Radar Bounding Box (Data Link)
        ax.add_patch(Circle((CENTER_X, 10.0), radar_r, facecolor='none', edgecolor=C_MAGENTA if radar_r > 50 else C_RED, linestyle='--', lw=1.5, alpha=0.5, zorder=2))

    # 2. THE MONOLITHIC HULL (KIROV)
    hull_w = 120.0
    hull_h = 24.0
    
    if not is_flash:
        h_color = C_MAGENTA if radar_r > 50 else C_RED
        if is_tathata: h_color = 'none'
        e_color = 'none' if not is_tathata else C_MANTIS
        t_lw = 0 if not is_tathata else 2.5
        
        # We model the hull splitting exactly at the center (X=0)
        # Left half
        left_pts = np.array([[-hull_w/2, 10], [0, 0], [0, hull_h], [-hull_w/2+10, hull_h]])
        # Rotate left half around (0, 0)
        sin_l, cos_l = np.sin(spine_angle), np.cos(spine_angle)
        R_l = np.array([[cos_l, -sin_l], [sin_l, cos_l]])
        left_rot = np.dot(left_pts, R_l.T)
        ax.add_patch(Polygon(left_rot, facecolor=h_color, edgecolor=e_color, lw=t_lw, alpha=0.9, zorder=20))
        
        # Right half
        right_pts = np.array([[0, 0], [hull_w/2, 10], [hull_w/2-10, hull_h], [0, hull_h]])
        # Rotate right half opposite
        sin_r, cos_r = np.sin(-spine_angle), np.cos(-spine_angle)
        R_r = np.array([[cos_r, -sin_r], [sin_r, cos_r]])
        right_rot = np.dot(right_pts, R_r.T)
        ax.add_patch(Polygon(right_rot, facecolor=h_color, edgecolor=e_color, lw=t_lw, alpha=0.9, zorder=20))

    # 3. THE STEALTH VECTOR (Mk-48)
    if torpedo_y < -5 and not is_flash and not is_tathata:
        ax.plot([0, 0], [-150, torpedo_y], color=C_CYAN, lw=2, zorder=10)
        ax.scatter([0], [torpedo_y], s=50, color=C_TEXT, edgecolor=C_CYAN, lw=1, zorder=11)

    # 4. O(N) INCOMPRESSIBLE KINETIC SWELL (Swarm)
    if len(px) > 0 and not is_tathata:
        ax.scatter(px, py, s=p_sizes*4.0, c=c_tensor, edgecolors='none', alpha=0.5, zorder=30)
        ax.scatter(px, py, s=p_sizes*1.5, c=C_TEXT if is_flash else c_tensor, edgecolors='none', alpha=0.9, zorder=31)

    # 5. TATHĀTĀ / GEOMETRIC EXTRACTION
    if is_tathata and not is_flash:
        ax.text(CENTER_X, 80, "HIERARCHICAL HUB DELETED", color=C_MANTIS, fontsize=18, fontname='monospace', ha='center', weight='bold', zorder=40)
        ax.plot([0, 0], [-cam_h*0.3, cam_h*0.7], color=C_DIM, lw=1, zorder=5) # The axis of execution

    if is_flash:
        # Shockwave interrupt
        ax.add_patch(Rectangle((CENTER_X - cam_w, CENTER_Y - cam_h), cam_w*2, cam_h*2, facecolor=C_TEXT, zorder=60))

    # 6. TELEMETRY WIDGETS (NEURAL ENTRAINMENT UI)
    ui_col = C_MAGENTA if radar_r > 50 else C_RED
    if spine_angle > 0.1: ui_col = C_GOLD
    if is_tathata: ui_col = C_MANTIS
    
    txt_col = C_TEXT if not is_flash else C_VOID
    ui_bg   = C_VOID if not is_flash else C_TEXT
    
    # Top Bar
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=ui_bg, alpha=0.9, zorder=80))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    ax.text(0.04, 0.965, "LG-204 :: HIERARCHICAL NODE DELETION TENSOR", transform=ax.transAxes, color=txt_col, fontsize=20, fontname='monospace', weight='bold', va='center', zorder=81)

    # Bottom Target Matrix
    ax.add_patch(plt.Rectangle((0, 0), 1.0, 0.16, transform=ax.transAxes, color=ui_bg, alpha=0.95, zorder=80))
    ax.plot([0, 1.0], [0.16, 0.16], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    
    # Sensor Bounding Box
    ax.text(0.04, 0.11, f"RADAR BOUNDING BOX : {radar_r:03.0f} NM", color=txt_col, fontsize=14, fontname='monospace', zorder=81)
    bar_r = C_MAGENTA if radar_r > 50 else C_CYAN
    if is_tathata: bar_r = C_MANTIS
    rad_ratio = np.clip(radar_r / 250.0, 0.0, 1.0)
    ax.add_patch(plt.Rectangle((0.45, 0.105), 0.50, 0.02, transform=ax.transAxes, color=C_DIM, zorder=80))
    ax.add_patch(plt.Rectangle((0.45, 0.105), 0.50 * rad_ratio, 0.02, transform=ax.transAxes, color=bar_r, zorder=81))
    
    # Hull Integrity
    integ_ratio = 1.0 - np.clip(spine_angle / 0.5, 0.0, 1.0)
    ax.text(0.04, 0.08, f"STRUCTURAL INTEGRITY: {integ_ratio*100:03.0f}%", color=txt_col, fontsize=14, fontname='monospace', zorder=81)
    bar_i = C_MAGENTA if integ_ratio > 0.5 else C_RED
    if is_tathata: bar_i = C_MANTIS
    ax.add_patch(plt.Rectangle((0.45, 0.075), 0.50, 0.02, transform=ax.transAxes, color=C_DIM, zorder=80))
    ax.add_patch(plt.Rectangle((0.45, 0.075), 0.50 * integ_ratio, 0.02, transform=ax.transAxes, color=bar_i, zorder=81))

    pulse = ui_col if (f % 10 < 5) and not is_flash else txt_col
    if is_flash: pulse = C_VOID

    ax.text(0.04, 0.03, f"[{state_str}]", transform=ax.transAxes, color=pulse, fontsize=20, fontname='monospace', weight='bold', zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)

# ------------------------------------------------------------------
# O(1) BALLISTIC KINEMATICS STREAM
# ------------------------------------------------------------------
def generate_stream():
    px = np.zeros(MAX_PARTICLES)
    py = np.zeros(MAX_PARTICLES)
    vx = np.zeros(MAX_PARTICLES)
    vy = np.zeros(MAX_PARTICLES)
    p_life = np.zeros(MAX_PARTICLES) 
    
    spawn_idx = 0
    cam_w = 200.0

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        dt = 0.016
        
        is_flash = False
        is_tathata = False
        bg_strobe = False
        
        spine_angle = 0.0
        torpedo_y = -150.0
        
        # ---- PHASE 1: THE MONOLITHIC HUB (0 - 4s) ----
        if t_sec < 4.0:
            state = "NOMINAL :: OTH SENSOR NETWORK ACTIVE"
            radar_r = 250.0 + np.sin(t_sec * 5.0) * 10.0 # Pulsing data link
            target_cam_w = 400.0

        # ---- PHASE 2: TOPOLOGICAL BLINDING (4 - 9s) ----
        elif t_sec < 9.0:
            state = "WARNING :: DATA LINKS DELETED. OTH BLIND."
            prog = (t_sec - 4.0) / 5.0
            # Radar violently collapses
            radar_r = max(40.0, 250.0 - (smoothstep(prog) * 300.0))
            if t_sec < 4.5 and f % 6 < 3: bg_strobe = True
            
            target_cam_w = 250.0

        # ---- PHASE 3: THE ACOUSTIC ERASURE (9 - 14.8s) ----
        elif t_sec < 14.8:
            state = "TENSOR INJECTION :: MK-48 FLUID CASCADE"
            prog = (t_sec - 9.0) / 5.8
            
            target_cam_w = 180.0
            radar_r = 40.0
            
            # Torpedo approaches the keel precisely
            if prog < 0.2:
                torpedo_y = -150.0 + (prog * 5.0 * 150.0)
            else:
                torpedo_y = 0.0 # Impact
                # Hull snaps
                spine_angle = smoothstep((prog - 0.2) * 1.25) * 0.6 
                
                # O(N) Incompressible water / plasma swarm generation
                if t_sec == 9.0 + (0.2 * 5.8): bg_strobe = True
                
                active_count = np.sum(p_life > 0)
                spawns_needed = 800 if prog < 0.5 else 100
                
                if spawns_needed > 0:
                    n_spawns = min(spawns_needed, MAX_PARTICLES - spawn_idx)
                    if n_spawns > 0:
                        px[spawn_idx:spawn_idx+n_spawns] = np.random.normal(0, 5, n_spawns)
                        py[spawn_idx:spawn_idx+n_spawns] = np.random.normal(0, 5, n_spawns)
                        
                        angles = np.random.uniform(np.pi*0.1, np.pi*0.9, n_spawns)
                        speeds = np.random.uniform(50.0, 350.0, n_spawns)
                        
                        vx[spawn_idx:spawn_idx+n_spawns] = np.cos(angles) * speeds
                        vy[spawn_idx:spawn_idx+n_spawns] = np.sin(angles) * speeds
                        # Add immense upward explosion vector
                        vy[spawn_idx:spawn_idx+n_spawns] += 150.0
                        
                        p_life[spawn_idx:spawn_idx+n_spawns] = 1.0
                        spawn_idx += n_spawns

        # ---- PHASE 4: TATHĀTĀ / HARDWARE INTERRUPT (14.8 - 17.5s) ----
        else:
            is_tathata = True
            radar_r = 0.0
            spine_angle = 0.6
            torpedo_y = 0.0
            target_cam_w = 160.0
            
            if t_sec < 14.95:
                is_flash = True
                p_life[:] = 0.0 # Mathematically delete ALL entropy
                
            state = "TATHĀTĀ: CENTRALIZATION IS OBSOLETE. GEOMETRY DELETED."

        cam_w += (target_cam_w - cam_w) * 0.1
        
        # -------------------------------------------------------------
        # TENSOR PARTICLE CALCULATION (Gravity & Friction)
        # -------------------------------------------------------------
        active = p_life > 0
        if np.any(active):
            px[active] += vx[active] * dt
            py[active] += vy[active] * dt
            
            # Gravity pulling the massive water displacement back down
            vy[active] -= 180.0 * dt
            
            # Water surface floor clamping (Particles vanish or splash at Y=0)
            hit_floor = (py < 0) & active
            p_life[hit_floor] -= 0.1
            vy[hit_floor] *= -0.3
            py[hit_floor] = 0
            
            p_life[active] -= np.random.uniform(0.005, 0.02, np.sum(active))
        
        # Memory Defrag
        if spawn_idx > MAX_PARTICLES - 2000:
            act_idx = np.where(p_life > 0)[0]
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
            
            v_mag = np.sqrt(vx[p_life > 0]**2 + vy[p_life > 0]**2)
            # Fast explosion is Gold, falling water is white/cyan
            heat_norm = np.clip((v_mag - 50.0) / 250.0, 0.0, 1.0)
            
            # Base color mix
            c_tensor = heat_norm[:, None] * c_gold + (1.0 - heat_norm[:, None]) * c_txt
            p_sizes = 1.0 + (heat_norm * 4.0) 
            c_tensor = c_tensor * lives
            c_tensor = np.clip(c_tensor, 0.0, 1.0)

        yield (f, t_sec, state, np.copy(px[p_life > 0]), np.copy(py[p_life > 0]), p_sizes, c_tensor, cam_w, radar_r, spine_angle, torpedo_y, is_flash, is_tathata, bg_strobe)

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 204: THE KIROV DELETION TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Radar Radius Collapse & Incompressible Spine Snapping")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Nodes: {MAX_PARTICLES}")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
