"""
SOVEREIGN CODE: logic_garden_198_rupture_tensor.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Apollo 13 Thermodynamic Rupture Tensor (17.5 seconds)
SCENE: Logic Garden 198 (The Rupture Tensor / Bounding Box Migration)
HOTFIX: Boolean Array Geometry Alignment, Cartesian Origin Lock, Vacuum Gas Expansion
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
OUT_DIR = "frames_198_rupture_tensor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'        # Deep Space / Vacuum
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'        # Dark Architecture / Dead Node
C_CYAN      = '#00FFFF'        # Cryogenic Oxygen / Venting Gas
C_MAGENTA   = '#FF0055'        # Initial Plasma Shockwave / Friction
C_GOLD      = '#FFD700'        # Nominal Power / LM Lifeboat
C_RED       = '#FF3300'        # Critical Telemetry Alarm
C_IRON      = '#1A1A24'        # Solid Spacecraft Hull
C_MANTIS    = '#00FF00'        # Terminal Geometry (Tathata / Bounding Box Redrawn)

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
MAX_PARTICLES = 35000
CENTER_X = 0.0  # Absolute Cartesian Anchor

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, px, py, p_sizes, c_tensor, obj_pos, cam_w, sm_health, lm_load, is_flash, is_tathata, bg_strobe = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_TEXT if is_flash else C_VOID
    if bg_strobe and not is_tathata: bg_hex = '#0F0000' # Deep red alarm strobe
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    cx, cy = obj_pos
    cam_h = cam_w * (1920.0 / 1080.0)
    
    # Absolute Viewport Tracking Lock
    ax.set_xlim(cx - cam_w/2, cx + cam_w/2)
    ax.set_ylim(cy - cam_h/2, cy + cam_h/2)

    # 1. RENDER APOLLO STACK GEOMETRY
    if not is_flash:
        # State Colors
        c_sm = C_CYAN if sm_health > 0.05 else C_DIM
        c_cm = C_CYAN if not is_tathata else C_MANTIS
        c_lm = C_GOLD if sm_health < 0.5 and not is_tathata else C_CYAN
        if is_tathata: c_lm = C_MANTIS
        
        sm_lw = 2 if not is_tathata else 1
        ls_style = '-' if not is_tathata else '--'
        
        # Service Module (SM) - Cylinder based
        sm_pts = [[cx-12, cy-25], [cx+12, cy-25], [cx+12, cy+5], [cx-12, cy+5]]
        ax.add_patch(Polygon(sm_pts, closed=True, facecolor=C_VOID, edgecolor=c_sm, lw=sm_lw, linestyle=ls_style, zorder=20))
        # SM Engine Bell
        bell_pts = [[cx-4, cy-25], [cx+4, cy-25], [cx+7, cy-35], [cx-7, cy-35]]
        ax.add_patch(Polygon(bell_pts, closed=True, facecolor=C_VOID, edgecolor=c_sm, lw=sm_lw, linestyle=ls_style, zorder=20))
        
        # Tank Rupture Site Visual Marker
        if sm_health < 1.0 and not is_tathata:
            ax.scatter([cx+12], [cy-5], s=100 + (1-sm_health)*200, color=C_VOID, edgecolor=C_MAGENTA, lw=2, zorder=21)

        # Command Module (CM) - Cone
        cm_pts = [[cx-12, cy+5], [cx+12, cy+5], [cx+5, cy+18], [cx-5, cy+18]]
        ax.add_patch(Polygon(cm_pts, closed=True, facecolor=C_VOID, edgecolor=c_cm, lw=2, zorder=22))
        
        # Lunar Module (LM) - Docked
        lm_base = [[cx-8, cy+18], [cx+8, cy+18], [cx+10, cy+25], [cx-10, cy+25]]
        lm_ascent = [[cx-6, cy+25], [cx+6, cy+25], [cx+4, cy+33], [cx-4, cy+33]]
        ax.add_patch(Polygon(lm_base, closed=True, facecolor=C_VOID, edgecolor=c_lm, lw=2, zorder=23))
        ax.add_patch(Polygon(lm_ascent, closed=True, facecolor=C_VOID, edgecolor=c_lm, lw=2, zorder=23))

    # 2. O(N) KINEMATIC RUPTURE TENSOR (Gasses Venting)
    if len(px) > 0 and not is_tathata:
        ax.scatter(px, py, s=p_sizes*6.0, c=c_tensor, edgecolors='none', alpha=0.3, zorder=10)
        ax.scatter(px, py, s=p_sizes*2.0, c=C_TEXT if is_flash else c_tensor, edgecolors='none', alpha=0.9, zorder=11)

    # 3. TATHĀTĀ / GEOMETRIC EXTRACTION
    if is_tathata and not is_flash:
        # Bounding Box isolation - only CM and LM are inside the survival geometry
        ax.add_patch(Rectangle((cx-15, cy+2), 30, 35, facecolor='none', edgecolor=C_MANTIS, lw=2, linestyle='--', zorder=30))
        ax.text(cx, cy-40, "DEAD NODE MUTED", color=C_DIM, fontsize=16, fontname='monospace', ha='center', weight='bold', zorder=25)

    if is_flash:
        # Kinetic Overload Hardware Interrupt Screen Clear
        ax.add_patch(Rectangle((cx - cam_w, cy - cam_h), cam_w*2, cam_h*2, facecolor=C_TEXT, zorder=60))

    # 4. TELEMETRY WIDGETS (NEURAL ENTRAINMENT UI)
    ui_col = C_CYAN if not is_tathata else C_MANTIS
    if sm_health < 0.2: ui_col = C_RED # Overflow UI Red
    txt_col = C_TEXT if not is_flash else C_VOID
    ui_bg   = C_VOID if not is_flash else C_TEXT
    
    # Top Bar
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=ui_bg, alpha=0.9, zorder=80))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    ax.text(0.04, 0.965, "LG-198 :: THERMODYNAMIC RUPTURE MATRICES", transform=ax.transAxes, color=txt_col, fontsize=20, fontname='monospace', weight='bold', va='center', zorder=81)

    # Bottom Target Matrix
    ax.add_patch(plt.Rectangle((0, 0), 1.0, 0.16, transform=ax.transAxes, color=ui_bg, alpha=0.95, zorder=80))
    ax.plot([0, 1.0], [0.16, 0.16], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    
    # Dual Telemetry Feed
    ax.text(0.04, 0.11, "SM O2 TANK 2 PRESSURE :", color=txt_col, fontsize=14, fontname='monospace', zorder=81)
    bar_col_sm = C_CYAN if sm_health > 0.5 else C_RED
    if is_tathata: bar_col_sm = C_DIM
    ax.add_patch(plt.Rectangle((0.45, 0.105), 0.50, 0.02, transform=ax.transAxes, color=C_DIM, zorder=80))
    ax.add_patch(plt.Rectangle((0.45, 0.105), 0.50 * sm_health, 0.02, transform=ax.transAxes, color=bar_col_sm, zorder=81))
    
    ax.text(0.04, 0.08, "LM LIFEBOAT AMP LOAD  :", color=txt_col, fontsize=14, fontname='monospace', zorder=81)
    bar_col_lm = C_GOLD if lm_load > 0.5 else C_CYAN
    if is_tathata: bar_col_lm = C_MANTIS
    if is_flash: bar_col_lm = C_VOID
    ax.add_patch(plt.Rectangle((0.45, 0.075), 0.50, 0.02, transform=ax.transAxes, color=C_DIM, zorder=80))
    ax.add_patch(plt.Rectangle((0.45, 0.075), 0.50 * lm_load, 0.02, transform=ax.transAxes, color=bar_col_lm, zorder=81))

    pulse = ui_col if (f % 10 < 5) and not is_flash else txt_col
    if sm_health < 0.2 and not is_tathata and f % 4 < 2: pulse = C_RED
    if is_flash: pulse = C_VOID

    ax.text(0.04, 0.03, f"[{state_str}]", transform=ax.transAxes, color=pulse, fontsize=20, fontname='monospace', weight='bold', zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) BALLISTIC KINEMATICS STREAM
# ------------------------------------------------------------------
def generate_stream():
    px = np.zeros(MAX_PARTICLES)
    py = np.zeros(MAX_PARTICLES)
    vx = np.zeros(MAX_PARTICLES)
    vy = np.zeros(MAX_PARTICLES)
    p_life = np.zeros(MAX_PARTICLES)
    p_type = np.zeros(MAX_PARTICLES, dtype=int)
    
    spawn_idx = 0
    obj_y = 0.0
    cam_w = 120.0
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        dt = 0.016
        
        is_flash = False
        is_tathata = False
        bg_strobe = False
        
        sm_health = 1.0
        lm_load = 0.1
        generate_gas = 0
        target_cam_w = 120.0
        
        obj_y += 10.0 * dt 
        
        # ---- PHASE 1: NOMINAL FLIGHT (0 - 4s) ----
        if t_sec < 4.0:
            state = "NOMINAL :: O(2) CROSS-TIE ACTIVATED"
            sm_health = 1.0
            lm_load = 0.1

        # ---- PHASE 2: THE RUPTURE / TANK 2 EXPLOSION (4 - 8s) ----
        elif t_sec < 8.0:
            state = "ALARM :: MAIN B BUS UNDERVOLT"
            prog = (t_sec - 4.0) / 4.0
            sm_health = 1.0 - (prog**2 * 0.7)
            lm_load = 0.1 + (prog * 0.2)
            
            generate_gas = int(4000) if t_sec < 4.5 else int(1500)
            target_cam_w = 160.0
            if t_sec < 5.0 and f % 6 < 3: bg_strobe = True

        # ---- PHASE 3: THE VACCUM BLEED / REROUTE (8 - 14.8s) ----
        elif t_sec < 14.8:
            state = "HARDWARE REROUTE :: LIFEBOAT PROTOCOL INITIATED"
            prog = (t_sec - 8.0) / 6.8
            sm_health = max(0.0, 0.3 - (prog * 0.3))
            lm_load =  0.3 + (prog**3 * 0.7)
            
            generate_gas = int(1200 * (1.0 - prog))
            target_cam_w = 180.0
            if sm_health < 0.05: bg_strobe = True

        # ---- PHASE 4: TATHĀTĀ / HARDWARE INTERRUPT (14.8 - 17.5s) ----
        else:
            is_tathata = True
            sm_health = 0.0
            lm_load = 1.0
            target_cam_w = 140.0
            
            if t_sec < 14.95:
                is_flash = True
                p_life[:] = 0.0
                
            state = "TATHĀTĀ: TO SURVIVE, REDEFINE THE BOUNDING BOX."

        cam_w += (target_cam_w - cam_w) * 0.1
        
        # -------------------------------------------------------------
        # TENSOR PARTICLE GENERATION
        # -------------------------------------------------------------
        if generate_gas > 0:
            n_spawns = min(generate_gas, MAX_PARTICLES - spawn_idx)
            if n_spawns > 0:
                r_x = CENTER_X + 12.0
                r_y = obj_y - 5.0
                
                px[spawn_idx:spawn_idx+n_spawns] = r_x + np.random.normal(0, 1, n_spawns)
                py[spawn_idx:spawn_idx+n_spawns] = r_y + np.random.normal(0, 1, n_spawns)
                
                angles = np.random.uniform(-np.pi/2.5, np.pi/2.5, n_spawns)
                speeds = np.random.uniform(50, 400, n_spawns)
                
                vx[spawn_idx:spawn_idx+n_spawns] = np.cos(angles) * speeds
                vy[spawn_idx:spawn_idx+n_spawns] = np.sin(angles) * speeds + 10.0
                
                p_life[spawn_idx:spawn_idx+n_spawns] = np.random.uniform(0.6, 1.0, n_spawns)
                
                type_ratio = 0.7 if t_sec < 4.5 else 0.1
                r_types = np.random.choice([0, 1], size=n_spawns, p=[type_ratio, 1.0 - type_ratio])
                p_type[spawn_idx:spawn_idx+n_spawns] = r_types
                
                spawn_idx += n_spawns

        active = p_life > 0
        if np.any(active):
            px[active] += vx[active] * dt
            py[active] += vy[active] * dt
            p_life[active] -= 0.015
        
        if spawn_idx > MAX_PARTICLES - 5000:
            act_idx = np.where(active)[0]
            cnt = len(act_idx)
            px[:cnt] = px[act_idx]
            py[:cnt] = py[act_idx]
            vx[:cnt] = vx[act_idx]
            vy[:cnt] = vy[act_idx]
            p_life[:cnt] = p_life[act_idx]
            p_type[:cnt] = p_type[act_idx]
            p_life[cnt:] = 0
            spawn_idx = cnt

        active_cnt = np.sum(p_life > 0)
        c_tensor = np.zeros((active_cnt, 3))
        p_sizes = np.zeros(active_cnt)
        
        if active_cnt > 0:
            lives = np.clip(p_life[p_life > 0][:, None], 0.0, 1.0)
            types = p_type[p_life > 0]
            
            m_m = types == 0
            m_c = types == 1
            
            # Global color application
            c_tensor[m_m] = c_mage
            c_tensor[m_c] = c_cyan
            
            # SYNTAX REPAIR: Mask the localized size expansion logic accurately
            inv_life = 1.0 - lives.flatten()
            p_sizes[m_m] = 2.0 + (inv_life[m_m] * 6.0)
            p_sizes[m_c] = 1.0 + (inv_life[m_c] * 10.0)
            
            # Opacity Fade translation
            c_tensor = c_tensor * lives
            c_tensor = np.clip(c_tensor, 0.0, 1.0)

        yield (f, t_sec, state, np.copy(px[p_life > 0]), np.copy(py[p_life > 0]), p_sizes, c_tensor, (CENTER_X, obj_y), cam_w, sm_health, lm_load, is_flash, is_tathata, bg_strobe)

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 198: THE RUPTURE TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Boolean Tensor Logic & Cartesian Origins")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Nodes: {MAX_PARTICLES}")

    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
