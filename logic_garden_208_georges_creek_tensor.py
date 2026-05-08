"""
SOVEREIGN CODE: logic_garden_208_georges_creek_tensor.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(N) ILP Topological Mesh (17.5 seconds)
SCENE: Logic Garden 208 (The Georges Creek Tensor / Ancestral Lineage Routing)
HOTFIX: Exact 15,000 Node Manhattan Array & Continuous Lineage Validation
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_208_georges_creek"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'
C_TEXT      = '#FFFFFF'
C_DIM       = '#111116'
C_CYAN      = '#00FFFF'        # Late-Stage Canopy Node
C_MAGENTA   = '#FF0055'        # Artisan Error / Severed Circuit
C_GOLD      = '#FFD700'        # Grounded Truth Vector (Georges Creek)
C_MANTIS    = '#00FF00'        # Sovereign Constraint (The Biological Circuit)

# 15,000 Node Spatial Grid (100 cols x 150 rows)
GRID_W = 100
GRID_H = 150
MAX_PARTICLES = GRID_W * GRID_H

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_cyan = np.array(hex_to_rgba(C_CYAN)[:3])
c_mage = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_gold = np.array(hex_to_rgba(C_GOLD)[:3])
c_dim  = np.array(hex_to_rgba(C_DIM)[:3])

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, px, py, colors, path_x, path_y, is_severed, is_flash, is_tathata = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_TEXT if is_flash else C_VOID
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    ax.set_xlim(-150, 150)
    ax.set_ylim(-260, 260)

    if not is_flash:
        # THE 15,000 NODE DISCRETE SPATIAL GRID
        ax.scatter(px, py, s=4, c=colors, edgecolors='none', alpha=0.8, zorder=10)

        # GEORGES CREEK (THE GROUNDED TRUTH VECTOR)
        ax.plot([-140, 140], [-200, -200], color=C_GOLD, lw=6, zorder=12)
        ax.text(-135, -195, "GEORGES CREEK ALIGNMENT", color=C_GOLD, fontsize=10, fontname='monospace', weight='bold', zorder=13)

        # UPPER RIDGE (STYX RIVER ORIGIN)
        ax.plot([-140, 140], [200, 200], color=C_DIM, lw=4, zorder=12)
        
        # THE SOVEREIGN CONSTRAINT (ILP ROUTING WIREFRAME)
        if len(path_x) > 0:
            p_color = C_MAGENTA if is_severed else C_MANTIS
            lw_path = 8 if is_tathata else 4
            ax.plot(path_x, path_y, color=p_color, lw=lw_path, zorder=20)
            
            # The Ancestral Ping (Data traveling the logic circuit)
            if not is_severed:
                ping_idx = int((f * 2) % len(path_x))
                ax.scatter(path_x[ping_idx], path_y[ping_idx], s=120, c=C_TEXT, zorder=25)

        # TATHĀTĀ WIREFRAME & OVERRIDE
        if is_tathata:
            ax.add_patch(plt.Rectangle((-140, -200), 280, 400, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -220, "ILP OPTIMAL. THE LINEAGE HOLDS.", color=C_MANTIS, fontsize=16, fontname='monospace', weight='bold', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    ui_col = C_CYAN
    if is_severed: ui_col = C_MAGENTA
    if is_tathata: ui_col = C_MANTIS
    if t_sec >= 6.0 and not is_severed and not is_tathata: ui_col = C_TEXT
    txt_col = C_TEXT if not is_flash else C_VOID

    # Header Matrix
    ax.text(-140, 240, "LG-208 :: THE GEORGES CREEK TENSOR", color=ui_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: ILP PARETO FRONTIER / CONTINUITY MATRICES", color=txt_col, fontsize=12, fontname='monospace', zorder=80)
    
    # Mathematical Bounding Frame
    status_net = "SEVERED" if is_severed else "CONNECTED"
    ax.text(-140, -240, f"TOPOLOGICAL CONTINUITY : {status_net}", color=C_MAGENTA if is_severed else (C_MANTIS if is_tathata else C_TEXT), fontsize=14, fontname='monospace', weight='bold', zorder=80)
    
    # Phase Box
    ax.text(-140, -255, f"[{state_str}]", color=ui_col if (f%15<10 or is_tathata) else C_VOID, fontsize=18, fontname='monospace', weight='bold', zorder=80)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) ARRAY OPERATIONS & MATHEMATICAL ROUTING
# ------------------------------------------------------------------
def generate_stream():
    # Rigid 15,000 Node Grid Architecture
    gw = np.linspace(-130, 130, GRID_W)
    gh = np.linspace(200, -200, GRID_H) # Top to bottom
    X, Y = np.meshgrid(gw, gh)
    
    px = X.flatten()
    py = Y.flatten()

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        is_flash = False
        is_tathata = False
        is_severed = False
        state = "NOMINAL :: THE PRISTINE MATRIX"
        
        # Color Array base
        colors = np.zeros((MAX_PARTICLES, 3))
        colors[:, :] = c_cyan

        # Emptiness/Harvest logic parameters
        harvest_centers = []
        path_x, path_y = [], []
        
        # Phase 1: The Pristine Matrix (0 - 3s)
        if t_sec < 3.0:
            pass 

        # Phase 2: The Artisan's Gamble (3.0 - 6.0s)
        elif t_sec < 6.0:
            state = "ARTISAN GAMBLE :: UNBOUNDED HARVEST"
            # Random erratic static blocks
            harvest_centers = [
                (0, 50, 60), (-40, -50, 50), (40, 120, 50)
            ]
            is_severed = True # The Artisan accidentally cuts the continuous line
            
        # Phase 3: ILP Demon Deployment (6.0 - 14.8s)
        elif t_sec < 14.8:
            state = "ILP SOLVER :: GEOMETRIC RE-ROUTING"
            prog = (t_sec - 6.0) / 8.8
            
            # The emptiness (harvest) shifts deterministically like a puzzle
            # using mathematical Lissajous curves to map constraint pushing.
            h1_x = np.sin(prog * np.pi * 4) * 60
            h1_y = 50 + np.cos(prog * np.pi * 3) * 40
            
            h2_x = -40 + np.sin(prog * np.pi * 5) * 50
            h2_y = -50 + np.cos(prog * np.pi * 2) * 30
            
            h3_x = 40 + np.sin(prog * np.pi * 2) * 70
            h3_y = 120 + np.cos(prog * np.pi * 4) * 40
            
            harvest_centers = [
                (h1_x, h1_y, 45), (h2_x, h2_y, 45), (h3_x, h3_y, 45)
            ]
            
        # Phase 4: Tathātā (14.8 - 17.5s)
        else:
            state = "TATHĀTĀ :: THE UNBROKEN ANCESTRAL PING"
            is_tathata = True
            
            # Locked optimal state
            h1_x = np.sin(1.0 * np.pi * 4) * 60
            h1_y = 50 + np.cos(1.0 * np.pi * 3) * 40
            h2_x = -40 + np.sin(1.0 * np.pi * 5) * 50
            h2_y = -50 + np.cos(1.0 * np.pi * 2) * 30
            h3_x = 40 + np.sin(1.0 * np.pi * 2) * 70
            h3_y = 120 + np.cos(1.0 * np.pi * 4) * 40
            
            harvest_centers = [
                (h1_x, h1_y, 45), (h2_x, h2_y, 45), (h3_x, h3_y, 45)
            ]
            
            if t_sec < 14.95:
                is_flash = True

        # Apply Harvest Bounding Boxes to the Color Matrix
        # Using O(1) numpy array broadcast mathematics
        for (cx, cy, r) in harvest_centers:
            # Manhattan distance for rigid, industrial blocks rather than smooth circles
            dist = np.abs(px - cx) + np.abs(py - cy) 
            in_harvest = dist < r * 1.2
            
            if is_severed:
                colors[in_harvest] = c_mage # Artisan error registers as friction
            else:
                colors[in_harvest] = c_dim  # Industrial calculation registers as processed emptiness

        # --------------------------------------------------------------
        # MATHEMATICAL ROUTING OF THE SOVEREIGN CONSTRAINT
        # --------------------------------------------------------------
        if t_sec >= 1.0:
            if is_severed:
                # Plunges perfectly down but breaks at the harvest block
                path_x = [0, 0]
                path_y = [200, 110] # Hard break
            else:
                # Simulate the instantaneous ILP routing
                # The algorithm forces a geometric path (Manhattan zig-zags) dodging the harvest radii
                route_pts = []
                cur_y = 200
                cur_x = 0
                
                route_pts.append((cur_x, cur_y))
                
                # Rigid step logic simulating the solver
                for step in range(10):
                    next_y = cur_y - 40
                    # Evaluate if straight is blocked
                    collision = False
                    for (cx, cy, r) in harvest_centers:
                        if abs(cur_x - cx) < r and next_y < cy + r and cur_y > cy - r:
                            collision = True
                            # Push orthogonal vector
                            cur_x = cx + r + 10 if cur_x >= cx else cx - r - 10
                            route_pts.append((cur_x, cur_y)) # Horizontal correct
                            break
                    
                    cur_y = next_y
                    route_pts.append((cur_x, cur_y))
                
                # Clamp terminal edge to Georges Creek
                route_pts.append((cur_x, -200))
                
                path_x = [p[0] for p in route_pts]
                path_y = [p[1] for p in route_pts]

        # In Tathata, fade non-critical nodes to emphasize the topology
        if is_tathata:
            # Everything not deeply C_DIM turns slightly darker cyan
            mask = np.all(colors == c_cyan, axis=1)
            colors[mask] = [0.0, 0.4, 0.4] 

        yield (f, t_sec, state, np.copy(px), np.copy(py), colors, path_x, path_y, is_severed, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 208: THE GEORGES CREEK TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: Exact 15,000 Node ILP Array Validation")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Georges Creek Topology Restored.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
