"""
SOVEREIGN CODE: logic_garden_096_steel_rain_entrainment.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Ballistic Tensor (17.5 seconds)
SCENE: Logic Garden 096 (Steel Rain / MIRV Re-Entry)
HOTFIX: Optical Tensor Scaling (Screen-Space Invariance)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_096_steel_rain"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#000000'        # Absolute Vacuum
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'        # Telemetry Base
C_CYAN      = '#00FFFF'        # Boost Phase / Cold Exo-Atmosphere
C_GOLD      = '#FFD700'        # MIRV Bus / Separation
C_MAGENTA   = '#FF0055'        # Atmospheric Re-Entry / Plasma Sheer
C_MANTIS    = '#00FF00'        # Terminal Impact Grid (Tathata)
C_RED       = '#FF0033'        # Friction Overload Warning

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_mag = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_cy  = np.array(hex_to_rgba(C_CYAN)[:3])
c_txt = np.array(hex_to_rgba(C_TEXT)[:3])

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE KINEMATIC BOUNDING BOX
# ------------------------------------------------------------------
N_MIRVS = 12
KARMAN_LINE = 100000.0  
G_FORCE = 80.0

# O(1) Plasma Particle System (Re-entry Bloom)
MAX_PLASMA = 15000

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, bus_pos, mirv_pos, mirv_active, px, py, p_sizes, c_tensor, cam_bounds, is_flash, is_tathata, friction_load, bg_strobe = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_TEXT if is_flash else C_VOID
    if bg_strobe and not is_tathata: bg_hex = '#0A0A10'
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    cam_x, cam_y, cam_w, cam_h = cam_bounds
    ax.set_xlim(cam_x - cam_w/2, cam_x + cam_w/2)
    ax.set_ylim(cam_y - cam_h/2, cam_y + cam_h/2)

    # 1. RENDER STATIC INFRASTRUCTURE
    if not is_flash:
        # Ground Node
        ax.axhline(0, color=C_DIM if not is_tathata else C_MANTIS, lw=10, zorder=1)
        ax.axhline(0, color=C_RED if not is_tathata and friction_load > 0 else C_MANTIS, lw=2, alpha=0.5, zorder=2)
        
        # Karman Line
        if (cam_y + cam_h/2) > KARMAN_LINE and (cam_y - cam_h/2) < KARMAN_LINE:
            ax.axhline(KARMAN_LINE, color=C_CYAN, linestyle='--', lw=2, alpha=0.3, zorder=1)

    # 2. RENDER THE BUS & MULTIPLE INDEPENDENT VECTORS
    if not is_flash and not is_tathata:
        bx, by = bus_pos
        
        # HOTFIX: OPTICAL TENSOR SCALING
        # Force the geometries to render at a minimum percentage of the optical window
        # while respecting their true minimum physical dimensions.
        bus_w = max(300.0, cam_w * 0.015)
        bus_h = max(800.0, cam_w * 0.040)
        
        # Bus
        ax.add_patch(Rectangle((bx - bus_w/2, by - bus_h/2), bus_w, bus_h, facecolor=C_VOID, edgecolor=C_GOLD, lw=4, zorder=20))
        
        # Active MIRVs (Cones)
        mx = mirv_pos[:, 0]
        my = mirv_pos[:, 1]
        
        mirv_w = max(80.0, cam_w * 0.005)
        mirv_h = max(150.0, cam_w * 0.012)
        
        for i in range(N_MIRVS):
            if mirv_active[i] or (t_sec > 14.8 and i < 12): # Explicitly draw impacts
                cone = np.array([
                    [mx[i] - mirv_w, my[i] + mirv_h], 
                    [mx[i] + mirv_w, my[i] + mirv_h], 
                    [mx[i], my[i] - mirv_h]
                ])
                mirv_c = C_TEXT if friction_load < 0.1 else C_VOID
                edge_c = C_CYAN if friction_load < 0.1 else C_TEXT
                ax.add_patch(plt.Polygon(cone, facecolor=mirv_c, edgecolor=edge_c, lw=2, zorder=25))

    # 3. O(N) PLASMA FRICTION TENSOR
    if len(px) > 0 and not is_tathata:
        # Note: 's' parameter in scatter is inherently Screen-Space (Points^2), so it auto-scales robustly against the bounding box.
        ax.scatter(px, py, s=p_sizes*4.0, c=c_tensor, edgecolors='none', alpha=0.2, zorder=10)
        ax.scatter(px, py, s=p_sizes*1.0, c=C_TEXT if is_flash else c_tensor, edgecolors='none', alpha=0.8, zorder=11)

    # 4. TATHĀTĀ / IMPACT GEOMETRY (THE HARDWARE INTERRUPT)
    if is_tathata and not is_flash:
        mx = mirv_pos[:, 0]
        for i in range(N_MIRVS):
            # Perfect glowing geometric craters (Already scaling dynamically via cam_w)
            ax.add_patch(Circle((mx[i], 0), max(cam_w*0.02, 1500), facecolor=C_VOID, edgecolor=C_MANTIS, lw=8, zorder=30))
            ax.add_patch(Circle((mx[i], 0), max(cam_w*0.005, 400), facecolor=C_TEXT, zorder=31))
            # Vertical connection lines
            ax.plot([mx[i], mx[i]], [0, cam_y + cam_h/2], color=C_MANTIS, lw=2, linestyle=':', alpha=0.4, zorder=5)

    if is_flash:
        # Immediate Overload
        ax.axhline(0, color=C_MANTIS, lw=80, zorder=60)

    # 5. TELEMETRY WIDGETS (NEURAL ENTRAINMENT UI)
    ui_col = C_CYAN if not is_tathata else C_MANTIS
    if friction_load > 0.5: ui_col = C_MAGENTA
    if is_flash: ui_col = C_VOID
    
    txt_col = C_TEXT if not is_flash else C_VOID
    ui_bg   = C_VOID if not is_flash else C_TEXT
    
    # Top Bar (Static overlay)
    ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=ui_bg, alpha=0.9, zorder=80))
    ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    ax.text(0.04, 0.965, "LG-096 :: POST-BOOST VEHICLE / MIRV TENSOR", transform=ax.transAxes, color=txt_col, fontsize=22, fontname='monospace', weight='bold', va='center', zorder=81)

    # Bottom Target Matrix
    ax.add_patch(plt.Rectangle((0, 0), 1.0, 0.12, transform=ax.transAxes, color=ui_bg, alpha=0.95, zorder=80))
    ax.plot([0, 1.0], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2, zorder=80)
    
    ax.text(0.04, 0.08, f"THERMODYNAMIC FRICTION: {friction_load*100:05.1f}%", transform=ax.transAxes, color=txt_col, fontsize=18, fontname='monospace', zorder=81)
    
    # Atmospheric Load Bar
    ax.add_patch(plt.Rectangle((0.72, 0.03), 0.25, 0.02, transform=ax.transAxes, color=C_DIM, zorder=80))
    bar_fill = min(1.0, friction_load)
    bar_color = C_MAGENTA if friction_load > 0.6 else C_CYAN
    if friction_load > 0.9: bar_color = C_RED
    if is_flash: bar_color = C_VOID
    if is_tathata: bar_color = C_MANTIS
    
    ax.add_patch(plt.Rectangle((0.72, 0.03), 0.25 * bar_fill, 0.02, transform=ax.transAxes, color=bar_color, zorder=81))

    pulse = ui_col if (f % 10 < 5) and not is_flash else txt_col
    if friction_load > 0.9 and not is_tathata and f % 4 < 2: pulse = C_RED
    if is_flash: pulse = C_VOID
    if is_tathata and not is_flash: pulse = C_MANTIS

    ax.text(0.04, 0.03, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=22, fontname='monospace', weight='bold', zorder=81)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) BALLISTIC KINEMATICS STREAM
# ------------------------------------------------------------------
def generate_stream():
    bus_pos = np.array([0.0, 0.0])
    bus_vel = np.array([0.0, 25000.0]) # Massive initial vertical velocity
    
    mirv_pos = np.zeros((N_MIRVS, 2))
    mirv_vel = np.zeros((N_MIRVS, 2))
    mirv_active = np.zeros(N_MIRVS, dtype=bool)
    
    # Plasma array
    px = np.zeros(MAX_PLASMA)
    py = np.zeros(MAX_PLASMA)
    vx = np.zeros(MAX_PLASMA)
    vy = np.zeros(MAX_PLASMA)
    plife = np.zeros(MAX_PLASMA)
    plasma_idx = 0
    
    # Camera Smoothing
    cam_x, cam_y = 0.0, 0.0
    cam_w = 4000.0  
    
    deploy_idx = 0
    t_impact = 14.8
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        is_flash = False
        is_tathata = False
        bg_strobe = False
        friction_load = 0.0
        
        dt = 0.06 # Time scaling param
        
        # ---- PHASE 1: THE ASCENT (0 - 3s) ----
        if t_sec < 3.0:
            state = "[01] MAIN ENGINE BURN :: TENSOR INJECTED"
            bus_vel[1] -= G_FORCE * dt
            bus_pos += bus_vel * dt
            
            # Boost Plume (Cyan)
            spawns = 400
            if plasma_idx + spawns < MAX_PLASMA:
                px[plasma_idx:plasma_idx+spawns] = bus_pos[0] + np.random.uniform(-100, 100, spawns)
                py[plasma_idx:plasma_idx+spawns] = bus_pos[1] - 400 - np.random.uniform(0, 2000, spawns)
                vx[plasma_idx:plasma_idx+spawns] = np.random.uniform(-50, 50, spawns)
                vy[plasma_idx:plasma_idx+spawns] = -np.random.uniform(1000, 3000, spawns)
                plife[plasma_idx:plasma_idx+spawns] = 1.0
                plasma_idx += spawns

        # ---- PHASE 2: THE DEPLOYMENT (3 - 7s) ----
        elif t_sec < 7.0:
            state = "[02] POST-BOOST DEPLOYMENT :: MULTIPLYING THREAT VECTOR"
            bus_vel[1] -= G_FORCE * dt
            bus_pos += bus_vel * dt
            
            # Eject MIRVs symmetrically
            if f % int(0.3 * FPS) == 0 and deploy_idx < N_MIRVS:
                side = 1 if deploy_idx % 2 == 0 else -1
                spread_vel = 1200 + (deploy_idx * 500)
                mirv_pos[deploy_idx] = bus_pos.copy()
                mirv_vel[deploy_idx] = [spread_vel * side, bus_vel[1]]
                mirv_active[deploy_idx] = True
                deploy_idx += 1

        # ---- PHASE 3: RE-ENTRY / PLASMA SHEARING (7 - 14.8s) ----
        elif t_sec < t_impact:
            state = "WARNING: ATMOSPHERIC FRICTION MAXIMUM. TERMINAL DESCENT."
            bus_vel[1] -= G_FORCE * dt
            bus_pos += bus_vel * dt
            
            # Calculate friction dynamically based on height
            avg_y = np.mean(mirv_pos[mirv_active, 1]) if np.any(mirv_active) else 0.0
            if avg_y < KARMAN_LINE:
                friction_load = min(1.0, 1.0 - (avg_y / KARMAN_LINE))
                if t_sec > 13.5: bg_strobe = True
            
            # Generate massive plasma friction trails
            for i in range(N_MIRVS):
                if mirv_active[i] and mirv_pos[i, 1] < KARMAN_LINE:
                    spawns = int(80 * friction_load)
                    if plasma_idx + spawns < MAX_PLASMA:
                        px[plasma_idx:plasma_idx+spawns] = mirv_pos[i,0] + np.random.uniform(-100, 100, spawns)
                        py[plasma_idx:plasma_idx+spawns] = mirv_pos[i,1] + np.random.uniform(0, 800, spawns)
                        vx[plasma_idx:plasma_idx+spawns] = np.random.uniform(-150, 150, spawns)
                        vy[plasma_idx:plasma_idx+spawns] = np.random.uniform(500, 2500, spawns)
                        plife[plasma_idx:plasma_idx+spawns] = 1.0
                        plasma_idx += spawns

        # ---- PHASE 4: TATHĀTĀ / GRID LOCK (14.8 - 17.5s) ----
        else:
            is_tathata = True
            friction_load = 0.0
            if t_sec < 14.95:
                is_flash = True
            state = "TATHĀTĀ: TARGET MATRIX SATURATED. GEOMETRY PURIFIED."
            
            # Lock the active MIRVs to the exact ground plane
            mirv_pos[:deploy_idx, 1] = 0.0

        # O(1) Update for MIRVs
        if not is_tathata and np.any(mirv_active):
            idx = np.where(mirv_active)[0]
            mirv_vel[idx, 1] -= G_FORCE * dt
            mirv_pos[idx] += mirv_vel[idx] * dt
            
            # Impact Trigger
            hit_mask = mirv_pos[idx, 1] <= 0
            if np.any(hit_mask):
                hit_idx = idx[hit_mask]
                mirv_pos[hit_idx, 1] = 0
                mirv_vel[hit_idx] = 0

        # Update Plasma Particles
        p_act = plife > 0
        if np.any(p_act):
            px[p_act] += vx[p_act] * 0.016
            py[p_act] += vy[p_act] * 0.016
            plife[p_act] -= 0.04
            
        # Buffer Roll
        if plasma_idx > MAX_PLASMA - 1000:
            act_idx = np.where(p_act)[0]
            cnt = len(act_idx)
            px[:cnt] = px[act_idx]
            py[:cnt] = py[act_idx]
            vx[:cnt] = vx[act_idx]
            vy[:cnt] = vy[act_idx]
            plife[:cnt] = plife[act_idx]
            plife[cnt:] = 0
            plasma_idx = cnt

        # -----------------------------------------------
        # HOTFIX: UNIFIED BOUNDING BOX SUPREMACY
        # -----------------------------------------------
        xs = [0.0]  
        ys = [0.0]  
        
        # Include the Bus vector
        if t_sec < 10.0:
            xs.append(bus_pos[0])
            ys.append(bus_pos[1])
            
        # Include all active Swarm Geometry
        if deploy_idx > 0:
            xs.extend(mirv_pos[:deploy_idx, 0])
            ys.extend(mirv_pos[:deploy_idx, 1])

        max_abs_x = max([abs(x) for x in xs])
        max_y = max(ys)

        req_w_from_x = max_abs_x * 2.8 
        req_w_from_y = (max_y * 1.25) * (1080.0 / 1920.0)
        
        target_w = max(14000.0, req_w_from_x, req_w_from_y)
        
        # The true y-center of the entire vertical structure
        target_y = max_y / 2.0 
        
        # Smooth interpolation
        damp = 0.15 
        cam_w += (target_w - cam_w) * damp
        cam_h = cam_w * (1920.0 / 1080.0)
        
        # Offset (Rule of Thirds execution)
        offset_y = 0.0
        if t_sec < 7.0:
            offset_y = cam_h * 0.1 
            
        cam_y += ((target_y + offset_y) - cam_y) * damp
        
        # Hard Floor Clamp
        if cam_y - cam_h/2.0 < -1000.0:
            cam_y = (cam_h/2.0) - 1000.0

        cam_bounds = (cam_x, cam_y, cam_w, cam_h)

        # O(N) Chromatics for export
        curr_act = np.sum(p_act)
        c_tensor = np.zeros((curr_act, 3))
        p_sizes = np.zeros(curr_act)
        
        if curr_act > 0:
            lives = np.clip(plife[p_act][:, None], 0.0, 1.0)
            c_tensor = lives * c_txt + (1 - lives) * c_mag
            if t_sec < 3.0: 
                c_tensor = lives * c_txt + (1 - lives) * c_cy
            
            c_tensor = np.clip(c_tensor, 0.0, 1.0)
            p_sizes = 2.0 + (lives.flatten()) * 10.0

        yield (f, t_sec, state, bus_pos.copy(), mirv_pos.copy(), mirv_active.copy(), np.copy(px[p_act]), np.copy(py[p_act]), p_sizes, c_tensor, cam_bounds, is_flash, is_tathata, friction_load, bg_strobe)

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 096: THE MIRV TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Optical Tensor Scaling (Screen-Space Invariance)")
    print(f"Executing: {FPS} FPS | Duration: {DURATION}s | Format: YouTube Shorts")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
