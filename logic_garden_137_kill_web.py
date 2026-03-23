"""
SOVEREIGN CODE: logic_garden_137_kill_web_v2.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python High-Fidelity Simulator (Kinetic/AEGIS Phased Array Emulation)
SCENE: Logic Garden 137 (The Kill Web - Beam Steering & Staggered Ingress)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import RegularPolygon
import math
import os

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 25                   # 25-Second Phase Transition
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_137_killweb_v2"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (HIGH-VOLTAGE) --------
C_VOID = '#020205'              # Absolute Black
C_RADAR = '#003322'             # Deep Grid Green
C_RED = '#FF003C'               # Hypersonic Entropy
C_GOLD = '#FFD700'              # Kinetic Interceptor
C_CYAN = '#00FFCC'              # Target Lock & Phased Array Beam
C_MANTIS = '#39FF14'            # Terminal Green (System Nominal)
C_TEXT = '#FFFFFF'              # UI Readout

def run():
    print(f"LOGIC GARDEN 137 v2: AEGIS KILL WEB (PHASED ARRAY)")
    print(f"Executing: {FPS} FPS | Total: {TOTAL_FRAMES} frames")
    
    # ------------------------------------------------------------------
    # GENERATE DETERMINISTIC STAGGERED THREAT MATRIX 
    # ------------------------------------------------------------------
    np.random.seed(1024) 
    
    # We will build 3 distinct Waves to span 20 seconds of action.
    wave_configs = [
        {'count': 3, 'start_delay_sec': 1.0, 'speed': 10},
        {'count': 4, 'start_delay_sec': 7.0, 'speed': 12},
        {'count': 5, 'start_delay_sec': 13.0, 'speed': 14}
    ]
    
    threats = []
    threat_id_counter = 10
    interceptor_speed = 22.0 # Tuned down for visual comprehension
    base_pos = np.array([540.0, 100.0])
    
    for wave in wave_configs:
        for _ in range(wave['count']):
            # Spawn high off-screen
            start_x = np.random.uniform(100, 980)
            start_y = 2200 
            
            angle_to_base = math.atan2(100 - start_y, 540 - start_x)
            fuzz = np.random.uniform(-0.15, 0.15) 
            vx = math.cos(angle_to_base + fuzz) * wave['speed']
            vy = math.sin(angle_to_base + fuzz) * wave['speed']
            
            threats.append({
                'pos': np.array([start_x, start_y]),
                'vel': np.array([vx, vy]),
                'history': [],
                'locked': False,
                'destroyed': False,
                'id': f"TGT-{threat_id_counter:02d}",
                'interceptor': None,
                'bloom': 0.0,
                'beam_flash': 0.0,
                'spawn_frame': wave['start_delay_sec'] * FPS
            })
            threat_id_counter += 1

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        fig.patch.set_facecolor(C_VOID)
        ax.set_facecolor(C_VOID)
        ax.set_xlim(0, 1080)
        ax.set_ylim(0, 1920)

        # ------------------------------------------------------------------
        # GRID ARCHITECTURE
        # ------------------------------------------------------------------
        for r in [400, 800, 1200, 1600]:
            circle = plt.Circle(base_pos, r, color=C_RADAR, fill=False, linewidth=1, alpha=0.5, linestyle='--')
            ax.add_patch(circle)
            ax.text(545, base_pos[1] + r + 5, f"{r*10}KM", color=C_RADAR, fontsize=10, fontname='monospace')

        # Draw Base Bounding Box (Phased Array Faces)
        ax.add_patch(plt.Rectangle((440, 50), 200, 100, color=C_CYAN, fill=False, lw=3))
        # Draw the 4 static SPY radar faces (Diamond layout)
        spy_pts = [[540,150], [560,125], [540,100], [520,125]]
        ax.add_patch(plt.Polygon(spy_pts, color=C_CYAN, fill=True, alpha=0.5))
        ax.text(540, 30, "AEGIS CORE (SPY-6)", color=C_TEXT, ha='center', fontsize=20, fontname='monospace')

        # ------------------------------------------------------------------
        # KINETIC WARFARE LOGIC
        # ------------------------------------------------------------------
        active_threats = 0
        
        for tr in threats:
            # Hold threat outside space/time until its spawn frame
            if f < tr['spawn_frame']:
                continue
                
            if not tr['destroyed'] and tr['pos'][1] < 1920: active_threats += 1
            
            if not tr['destroyed']:
                tr['pos'] += tr['vel']
                tr['history'].append((tr['pos'][0], tr['pos'][1]))
                if len(tr['history']) > 20: tr['history'].pop(0)

                # Sensor Fusion Lock (Phased Array Beam Steering)
                # If target crosses the 1600km Bounding Box, instantly lock
                dist_to_base = np.linalg.norm(tr['pos'] - base_pos)
                if not tr['locked'] and dist_to_base < 1600:
                    tr['locked'] = True
                    tr['beam_flash'] = 1.0 # Trigger the instantaneous RF ping
                    
                    # Generate ProNet Firing Solution
                    tti = dist_to_base / interceptor_speed
                    ghost_x = tr['pos'][0] + (tr['vel'][0] * tti)
                    ghost_y = tr['pos'][1] + (tr['vel'][1] * tti)
                    
                    tr['interceptor'] = {
                        'pos': np.copy(base_pos),
                        'ghost': np.array([ghost_x, ghost_y]),
                        'history': []
                    }

            # ------------------------------------------------------------------
            # VISUAL RENDERING
            # ------------------------------------------------------------------
            if not tr['destroyed'] and tr['pos'][1] < 1920:
                
                # Render Phased Array Beam Steer (Instantanous Flash)
                if tr['beam_flash'] > 0:
                    ax.plot([base_pos[0], tr['pos'][0]], [base_pos[1], tr['pos'][1]], color=C_CYAN, lw=2, alpha=tr['beam_flash'])
                    tr['beam_flash'] -= 0.1 # Very fast decay (microsecond ping)

                # Render Threat Trail
                if len(tr['history']) > 2:
                    pts = np.array(tr['history'])
                    ax.plot(pts[:,0], pts[:,1], color=C_RED, alpha=0.6, lw=2)
                ax.scatter(tr['pos'][0], tr['pos'][1], c=C_RED, s=60, marker='v')

                if tr['locked'] and tr['interceptor']:
                    # UI: The Ghost Projection Vector
                    ax.plot([tr['pos'][0], tr['interceptor']['ghost'][0]], 
                            [tr['pos'][1], tr['interceptor']['ghost'][1]], 
                            color=C_RED, linestyle=':', lw=1, alpha=0.5)

                    # UI: Draw Target Bracket
                    size = 40
                    x, y = tr['pos']
                    ax.plot([x-size, x-size, x-size+10], [y+size-10, y+size, y+size], color=C_CYAN, lw=2)
                    ax.plot([x+size, x+size, x+size-10], [y+size-10, y+size, y+size], color=C_CYAN, lw=2)
                    ax.plot([x-size, x-size, x-size+10], [y-size+10, y-size, y-size], color=C_CYAN, lw=2)
                    ax.plot([x+size, x+size, x+size-10], [y-size+10, y-size, y-size], color=C_CYAN, lw=2)
                    ax.text(x + 50, y, tr['id'], color=C_CYAN, fontsize=12, fontname='monospace')

                    # Physics: Interceptor Proportional Navigation
                    intc_pos = tr['interceptor']['pos']
                    dist = np.linalg.norm(tr['pos'] - intc_pos)
                    tti = dist / interceptor_speed
                    dyn_ghost = tr['pos'] + (tr['vel'] * tti)
                    
                    dir_vec = dyn_ghost - intc_pos
                    # Guard against zero-division perfectly on intercept
                    if np.linalg.norm(dir_vec) > 0.1:
                        dir_norm = dir_vec / np.linalg.norm(dir_vec)
                        intc_pos += dir_norm * interceptor_speed
                    
                    tr['interceptor']['history'].append(np.copy(intc_pos))
                    
                    # Interceptor UI/Trails
                    if len(tr['interceptor']['history']) > 2:
                        ipts = np.array(tr['interceptor']['history'])
                        ax.plot(ipts[:,0], ipts[:,1], color=C_CYAN, lw=3, alpha=0.8)
                    ax.scatter(intc_pos[0], intc_pos[1], c=C_GOLD, s=70, marker='^', zorder=5)

                    # Collision Resolution
                    if np.linalg.norm(intc_pos - tr['pos']) < interceptor_speed * 1.5:
                        tr['destroyed'] = True
                        tr['bloom'] = 1.0

            # ------------------------------------------------------------------
            # THE EXPLOSION ENGINE (Critical Damping)
            # ------------------------------------------------------------------
            if tr['destroyed'] and tr['bloom'] > 0:
                hex_radius = (1.0 - tr['bloom']) * 200
                poly = RegularPolygon(tr['pos'], numVertices=6, radius=hex_radius, 
                                      orientation=math.pi/6, facecolor='none', 
                                      edgecolor=C_TEXT, linewidth=5 * tr['bloom'], alpha=tr['bloom'])
                ax.add_patch(poly)
                
                # Fragment scatter
                np.random.seed(int(tr['pos'][0])) 
                for _ in range(8):
                    ang = np.random.uniform(0, 2*math.pi)
                    rad = np.random.uniform(0, 150) * (1 - tr['bloom'])
                    fx = tr['pos'][0] + math.cos(ang) * rad
                    fy = tr['pos'][1] + math.sin(ang) * rad
                    ax.scatter(fx, fy, c=C_RED, s=20 * tr['bloom'], alpha=tr['bloom'])
                    
                tr['bloom'] -= 0.04 

        # ------------------------------------------------------------------
        # UI DECOUPLING & BATTLESPACE TELEMETRY
        # ------------------------------------------------------------------
        # Top Header Overlay
        ax.add_patch(plt.Rectangle((0, 1850), 1080, 70, color=C_CYAN, alpha=0.1))
        ax.axhline(1850, color=C_CYAN, lw=2)
        ax.text(40, 1870, "LOGIC GARDEN 137 [v2] :: AEGIS KILL WEB ARCHITECTURE", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold')

        # Side HUD Readout
        ax.text(40, 1780, f"FRAME METRIC : {f:04d}", color=C_CYAN, fontsize=18, fontname='monospace')
        ax.text(40, 1740, f"SYS TIME (T) : {t_sec:.2f}s", color=C_CYAN, fontsize=18, fontname='monospace')
        
        # Threat Detection Logic
        all_spawned = t_sec > 13.0
        all_destroyed = all(tr['destroyed'] for tr in threats)
        
        if active_threats > 0:
            ax.text(40, 1700, f"SYS STATUS   : RED ENTROPY INGRESS", color=C_RED, fontsize=18, fontname='monospace', weight='bold')
            ax.text(40, 1660, f"TGT TRACKED  : {active_threats}", color=C_TEXT, fontsize=18, fontname='monospace')
            ax.text(40, 1620, f"SENSOR FUSION: PHASED ARRAY LINKED", color=C_GOLD, fontsize=18, fontname='monospace')
        elif all_spawned and all_destroyed:
            ax.text(40, 1700, f"SYS STATUS   : TERMINAL GREEN", color=C_MANTIS, fontsize=22, fontname='monospace', weight='bold')
            ax.text(40, 1660, f"RESOLUTION   : COMPILE-TIME MET", color=C_GOLD, fontsize=18, fontname='monospace')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close(fig)

if __name__ == "__main__": run()
