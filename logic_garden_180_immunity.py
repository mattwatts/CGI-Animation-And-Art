"""
SOVEREIGN CODE: logic_garden_180_immunity.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / Naval Ballistics Geometry (17.8 seconds)
SCENE: Logic Garden 180 (Zone of Immunity / Armour vs Range)
HOTFIX: Bezier Kinematics & Incidence Angles
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Arc
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.8                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_180_immunity"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID    = '#020205'
C_TEXT    = '#FFFFFF'
C_DIM     = '#1A1A24'          # Background Grid
C_CYAN    = '#00FFFF'          # Sovereign Hull Architecture
C_ORANGE  = '#FF5500'          # Kinetic Vector (Incoming Shell)
C_RED     = '#FF0033'          # Structural Defeat (Penetration)
C_MANTIS  = '#00FF00'          # Ricochet / Deflection (Survival)

def hex_to_rgba(hex_code, alpha=1.0):
    hex_code = hex_code.lstrip('#')
    return [int(hex_code[0:2], 16)/255.0, int(hex_code[2:4], 16)/255.0, int(hex_code[4:6], 16)/255.0, alpha]

# ------------------------------------------------------------------
# SYSTEM TOPOLOGY: THE ARMOUR MATRIX
# ------------------------------------------------------------------
# Belt is at X=600. Deck is at Y=960.
hull_pts = np.array([[600, 200], [600, 960], [1080, 960], [1080, 200]])
belt_armor = np.array([[600, 200], [600, 960], [630, 960], [630, 200]])
deck_armor = np.array([[600, 960], [1080, 960], [1080, 930], [600, 930]])

def bezier(t, p0, p1, p2):
    return (1-t)**2 * p0 + 2*(1-t)*t * p1 + t**2 * p2

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, ui_col, shell_x, shell_y, shell_hist, zoom_factor, cx, cy, impact_pt, angle_text = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    fig.patch.set_facecolor(C_VOID)
    ax.set_facecolor(C_VOID)

    w_width = 1080 / zoom_factor
    w_height = 1920 / zoom_factor
    ax.set_xlim(cx - w_width/2, cx + w_width/2)
    ax.set_ylim(cy - w_height/2, cy + w_height/2)

    # 1. RENDER VOID GRID
    for y_line in range(0, 1920, 100):
        ax.axhline(y_line, color=C_DIM, lw=1, zorder=1)
    for x_line in range(0, 1080, 100):
        ax.axvline(x_line, color=C_DIM, lw=1, zorder=1)

    # 2. RENDER THE BATTLESHIP ARCHITECTURE
    ax.add_patch(Polygon(hull_pts, closed=True, facecolor=C_VOID, edgecolor=C_CYAN, lw=2, zorder=2))
    ax.add_patch(Polygon(belt_armor, closed=True, facecolor=hex_to_rgba(C_CYAN, 0.4), edgecolor='none', zorder=3))
    ax.add_patch(Polygon(deck_armor, closed=True, facecolor=hex_to_rgba(C_CYAN, 0.4), edgecolor='none', zorder=3))
    
    # Internal Citadel
    ax.add_patch(Rectangle((680, 400), 300, 400, fill=False, edgecolor=C_CYAN, lw=2, linestyle='--', zorder=3))
    ax.text(830, 600, "VULNERABLE\nCITADEL", color=C_CYAN, fontname='monospace', fontsize=20, ha='center', va='center', zorder=4)

    # 3. KINETIC VECTOR (THE SHELL)
    if len(shell_hist) > 0:
        hx = [p[0] for p in shell_hist]
        hy = [p[1] for p in shell_hist]
        ax.plot(hx, hy, color=ui_col if zoom_factor > 1.5 else C_ORANGE, lw=6, zorder=6)
        ax.scatter([shell_x], [shell_y], s=400, c=C_TEXT, edgecolors=ui_col, lw=3, zorder=7)

    # 4. PENETRATION / DEFLECTION GRAPHICS & INCIDENCE ANGLES
    if impact_pt is not None:
        ix, iy = impact_pt
        
        # Draw Incidence Normal Line
        if iy == 960: # Deck Hit
            ax.plot([ix, ix], [960, 1160], color=C_TEXT, lw=2, linestyle=':', zorder=5)
            # Angle arc
            ax.add_patch(Arc((ix, iy), 200, 200, theta1=0, theta2=180, color=ui_col, lw=2, zorder=5))
        elif ix == 600: # Belt Hit
            ax.plot([400, 600], [iy, iy], color=C_TEXT, lw=2, linestyle=':', zorder=5)
            ax.add_patch(Arc((ix, iy), 200, 200, angle=90, theta1=0, theta2=180, color=ui_col, lw=2, zorder=5))

        ax.text(ix - 50, iy + 100, angle_text, color=ui_col, fontname='monospace', fontsize=22, weight='bold', zorder=10)

        # Explosions
        if ui_col == C_RED: # Penetration Bloom inside ship
            ax.scatter([ix+80], [iy-80], s=8000, facecolors='none', edgecolors=C_RED, lw=8, zorder=8)
            ax.scatter([ix+80], [iy-80], s=3000, c=C_RED, edgecolors='none', alpha=0.6, zorder=9)
        elif ui_col == C_MANTIS: # Deflection Spark outside ship
            ax.scatter([ix], [iy], s=4000, facecolors='none', edgecolors=C_MANTIS, lw=5, zorder=8)

    # 5. ATOMIC LATTICE (ZOOM REQUIREMENT)
    if zoom_factor > 1.5:
        alpha_lat = min(1.0, (zoom_factor - 1.5) / 5.0)
        grid_x, grid_y = np.meshgrid(np.linspace(ix-20, ix+20, 15), np.linspace(iy-20, iy+20, 15))
        ax.scatter(grid_x.flatten(), grid_y.flatten(), s=1500*zoom_factor, facecolors='none', edgecolors=hex_to_rgba(C_MANTIS, alpha_lat), lw=2*zoom_factor, zorder=4)

    # 6. TELEMETRY WIDGETS
    if zoom_factor < 2.0:
        ax.add_patch(plt.Rectangle((0, 0.94), 1, 0.06, transform=ax.transAxes, color=C_VOID, alpha=0.9))
        ax.plot([0, 1], [0.94, 0.94], transform=ax.transAxes, color=C_ORANGE, lw=2)
        ax.text(0.04, 0.965, "LG-180 :: THE GEOMETRY OF SURVIVAL", transform=ax.transAxes, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold', va='center')

        ax.add_patch(plt.Rectangle((0, 0), 1, 0.12, transform=ax.transAxes, color=C_VOID, alpha=0.95))
        ax.plot([0, 1], [0.12, 0.12], transform=ax.transAxes, color=ui_col, lw=2)
        ax.text(0.04, 0.08, "BALLISTIC TRAJECTORY STATUS:", transform=ax.transAxes, color=C_TEXT, fontsize=20, fontname='monospace')
        
        pulse = ui_col if (f % 10 < 5) or ui_col == C_MANTIS else C_TEXT
        ax.text(0.04, 0.04, f"{state_str}", transform=ax.transAxes, color=pulse, fontsize=24, fontname='monospace', weight='bold')

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# STRICT BEZIER KINEMATICS STREAM
# ------------------------------------------------------------------
def generate_stream():
    hist = []
    zoom = 1.0
    cam_x, cam_y = 540, 960
    sx, sy = -200, 960 
    
    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        impact_pt = None
        angle_text = ""
        
        # ---------------------------------------------------
        # TARGET 1: SHORT RANGE (FLAT / BELT DEFEAT)
        # ---------------------------------------------------
        if t_sec < 5.0:
            local_t = min(1.0, t_sec / 4.0) # Hits at 4.0s, explosion lingers 1s
            
            p0 = np.array([-200, 750])
            p1 = np.array([200, 800])
            p2 = np.array([600, 700]) # Exact Belt Impact
            
            p = bezier(local_t, p0, p1, p2)
            sx, sy = p[0], p[1]
            
            if local_t < 1.0:
                ui_col = C_ORANGE
                state = "[01] SHORT RANGE: FLAT VECTOR DETECTED"
                hist.append((sx, sy))
            else:
                ui_col = C_RED
                state = "INCIDENCE 85°: VERTICAL BELT PENETRATED"
                impact_pt = (600, 700)
                angle_text = "ΔΘ: 85° (CRITICAL)"

        # ---------------------------------------------------
        # TARGET 2: LONG RANGE (PLUNGING / DECK DEFEAT)
        # ---------------------------------------------------
        elif t_sec < 10.0:
            if t_sec >= 5.0 and t_sec < 5.1: hist.clear()
            local_t = min(1.0, (t_sec - 5.0) / 4.0)
            
            p0 = np.array([-200, 1920])
            p1 = np.array([550, 1920])
            p2 = np.array([750, 960]) # Exact Deck Impact
            
            p = bezier(local_t, p0, p1, p2)
            sx, sy = p[0], p[1]
            
            if local_t < 1.0:
                ui_col = C_ORANGE
                state = "[02] LONG RANGE: PLUNGING VECTOR DETECTED"
                hist.append((sx, sy))
            else:
                ui_col = C_RED
                state = "INCIDENCE 82°: HORIZONTAL DECK PENETRATED"
                impact_pt = (750, 960)
                angle_text = "ΔΘ: 82° (CRITICAL)"

        # ---------------------------------------------------
        # TARGET 3: ZONE OF IMMUNITY (SHALLOW ANGLE DECK RICOCHET)
        # ---------------------------------------------------
        else:
            if t_sec >= 10.0 and t_sec < 10.1: hist.clear()
            
            if t_sec < 14.0:
                # Incoming trajectory
                local_t = (t_sec - 10.0) / 4.0
                p0 = np.array([-200, 1200])
                p1 = np.array([200, 1400])
                p2 = np.array([650, 960]) # Hits Deck at oblique angle
                p = bezier(local_t, p0, p1, p2)
                sx, sy = p[0], p[1]
                
                ui_col = C_ORANGE
                state = "[03] ZONE OF IMMUNITY GEOMETRY ENGAGED"
                hist.append((sx, sy))
                
            else:
                # Ricochet trajectory & Zen Hook Zoom
                local_t = (t_sec - 14.0) / 3.8
                # Bounce up and right into the sky
                p0 = np.array([650, 960])
                p1 = np.array([800, 1300])
                p2 = np.array([1200, 1920])
                p = bezier(local_t, p0, p1, p2)
                sx, sy = p[0], p[1]
                
                ui_col = C_MANTIS
                state = "TATHĀTĀ: SHALLOW ANGLE RICOCHET ACHIEVED"
                hist.append((sx, sy))
                impact_pt = (650, 960)
                angle_text = "ΔΘ: 18° (DEFLECT)"
                
                # Camera zooms aggressively into the impact point
                zoom = 1.0 + (local_t ** 3) * 45.0 
                cam_x = 540 + (local_t ** 2) * (650 - 540)
                cam_y = 960

        yield (f, t_sec, state, ui_col, sx, sy, list(hist), zoom, cam_x, cam_y, impact_pt, angle_text)

# ------------------------------------------------------------------
# MULTIPROCESSING COMPILER
# ------------------------------------------------------------------
def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 180: ZONE OF IMMUNITY [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX Bezier Kinematics...")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            if finished_frame % 60 == 0:
                print(f"Compiled: {finished_frame:>4d} / {TOTAL_FRAMES}")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
