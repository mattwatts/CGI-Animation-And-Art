"""
SOVEREIGN CODE: logic_garden_138_sage_fsq7_v2.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python High-Fidelity Simulator (SAGE Vector CRT / Multithreaded)
SCENE: Logic Garden 138 (AN/FSQ-7 Continuous Telemetry)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
import os

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 30                   # 30-Second Extended Intercept
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_138_sage_v2"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE SAGE PHOSPHOR PALETTE --------
C_VOID = '#050B14'              # Deep CRT Blue/Black
C_PHOSPHOR_BLUE = '#55aaff'     # SAGE Vector Standard
C_PHOSPHOR_DIM = '#225577'      # Fading Phosphor / Background flights
C_AMBER = '#ffb000'             # Light Gun / Selection
C_RED = '#ff3333'               # Hostile Track
C_MANTIS = '#39FF14'            # Terminal Green
C_TEXT = '#FFFFFF'              # High-Contrast UI Strobe (The Fix)

def generate_vector_map():
    coastline = [
        (200, 1800), (350, 1600), (300, 1400), (450, 1200), (400, 1000),
        (550, 850), (450, 600), (500, 400), (600, 200), (550, 0)
    ]
    borders = [
        [(200, 1800), (100, 1800)], [(300, 1400), (100, 1400)],
        [(400, 1000), (150, 950)], [(500, 400), (300, 400)]
    ]
    return coastline, borders

def run():
    print(f"LOGIC GARDEN 138 v2: SAGE (MULTITHREADED BATTLESPACE)")
    print(f"Executing: {FPS} FPS | Total: {TOTAL_FRAMES} frames")

    coastline, borders = generate_vector_map()
    coast_x, coast_y = zip(*coastline)
    base_pos = np.array([600.0, 400.0]) # BOMARC Airbase
    
    np.random.seed(1958) # SAGE Implementation Year
    
    # 1. Background Commercial/Friendly Traffic
    friendlies = []
    for i in range(12):
        pos = np.array([np.random.uniform(50, 1000), np.random.uniform(200, 1800)])
        ang = np.random.uniform(0, 2*math.pi)
        vel = np.array([math.cos(ang), math.sin(ang)]) * np.random.uniform(0.5, 1.5)
        friendlies.append({
            'pos': pos, 'vel': vel, 'history': [], 'id': f"FLT-{np.random.randint(100,999)}"
        })

    # 2. Hostile Kinetic Tracks (Staggered to cover 30 seconds)
    hostiles = [
        {'id': "TRK-01", 'start': np.array([200.0, 1950.0]), 'aim': np.array([550.0, 400.0]), 'spawn': 1.0, 'select': 3.0, 'launch': 4.5, 'vel_mag': 4.0},
        {'id': "TRK-02", 'start': np.array([1000.0, 1900.0]), 'aim': np.array([650.0, 300.0]), 'spawn': 10.0, 'select': 12.0, 'launch': 13.5, 'vel_mag': 4.5},
        {'id': "TRK-03", 'start': np.array([50.0, 1600.0]), 'aim': np.array([500.0, 450.0]), 'spawn': 19.0, 'select': 21.0, 'launch': 22.5, 'vel_mag': 5.0}
    ]
    
    for h in hostiles:
        direction = h['aim'] - h['start']
        h['vel'] = (direction / np.linalg.norm(direction)) * h['vel_mag']
        h['pos'] = np.copy(h['start'])
        h['history'] = []
        h['state'] = 'PENDING' # PENDING -> TRACKING -> SELECTED -> ENGAGED -> DESTROYED
        h['int_pos'] = np.copy(base_pos)
        h['int_history'] = []
        h['bloom'] = 0.0

    interceptor_speed = 9.0

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
        # STAGE 1: SAGE CRT & VECTOR GEOGRAPHY
        # ------------------------------------------------------------------
        ax.plot(coast_x, coast_y, color=C_PHOSPHOR_DIM, lw=2, alpha=0.5)
        for bx, by in borders:
            ax.plot([bx[0], by[0]], [bx[1], by[1]], color=C_PHOSPHOR_DIM, lw=1, alpha=0.3)
            
        ax.add_patch(plt.Rectangle((base_pos[0]-15, base_pos[1]-15), 30, 30, fill=False, color=C_PHOSPHOR_BLUE, lw=2))
        ax.text(base_pos[0]+25, base_pos[1]-5, "BASE 07", color=C_PHOSPHOR_BLUE, fontsize=12, fontname='monospace')

        # Radar Sweep Angle
        radar_angle = -(t_sec * 2.5) % (2 * math.pi)

        # ------------------------------------------------------------------
        # STAGE 2: BACKGROUND SYSTEM TRAFFIC (The Hive Mind always works)
        # ------------------------------------------------------------------
        for flt in friendlies:
            flt['pos'] += flt['vel']
            # Wrap around canvas
            if flt['pos'][0] < -50: flt['pos'][0] = 1130
            if flt['pos'][0] > 1130: flt['pos'][0] = -50
            if flt['pos'][1] < -50: flt['pos'][1] = 1970
            if flt['pos'][1] > 1970: flt['pos'][1] = -50
            
            flt['history'].append(np.copy(flt['pos']))
            if len(flt['history']) > 15: flt['history'].pop(0)
            
            # Phosphor trails
            if len(flt['history']) > 2:
                pts = np.array(flt['history'])
                ax.plot(pts[:, 0], pts[:, 1], color=C_PHOSPHOR_DIM, lw=2, alpha=0.4)
            
            ax.scatter(flt['pos'][0], flt['pos'][1], marker='o', c=C_PHOSPHOR_DIM, s=20, alpha=0.6)
            
            # Simulated CRT Sweep illumination
            ang_to_flt = math.atan2(flt['pos'][1] - base_pos[1], flt['pos'][0] - base_pos[0]) % (2 * math.pi)
            if abs(radar_angle - ang_to_flt) < 0.2:
                ax.text(flt['pos'][0]+15, flt['pos'][1]-5, flt['id'], color=C_PHOSPHOR_BLUE, fontsize=10, fontname='monospace')
                ax.scatter(flt['pos'][0], flt['pos'][1], marker='o', c=C_PHOSPHOR_BLUE, s=50, alpha=1.0)

        # ------------------------------------------------------------------
        # STAGE 3: MULTITHREADED KINETIC LOGIC
        # ------------------------------------------------------------------
        active_hostile_tag = "NOMINAL"
        active_hostile_color = C_PHOSPHOR_BLUE
        
        for h in hostiles:
            if t_sec >= h['spawn'] and h['state'] == 'PENDING':
                h['state'] = 'TRACKING'
            if t_sec >= h['select'] and h['state'] == 'TRACKING':
                h['state'] = 'SELECTED'
            if t_sec >= h['launch'] and h['state'] == 'SELECTED':
                h['state'] = 'ENGAGED'

            if h['state'] in ['TRACKING', 'SELECTED', 'ENGAGED']:
                h['pos'] += h['vel']
                h['history'].append((h['pos'][0], h['pos'][1]))
                if len(h['history']) > 30: h['history'].pop(0)

                # Render Hostile Trail & Icon
                if len(h['history']) > 2:
                    pts = np.array(h['history'])
                    alphas = np.linspace(0.0, 0.8, len(pts))
                    for i in range(len(pts)-1):
                        ax.plot(pts[i:i+2, 0], pts[i:i+2, 1], color=C_RED, lw=3, alpha=alphas[i])

                ax.add_patch(plt.Rectangle((h['pos'][0]-10, h['pos'][1]-10), 20, 20, fill=False, color=C_RED, lw=2))
                ax.plot([h['pos'][0], h['pos'][0] + h['vel'][0]*4], 
                        [h['pos'][1], h['pos'][1] + h['vel'][1]*4], color=C_RED, lw=2)

                # Light Gun Selection Ring & UI Update
                if h['state'] in ['SELECTED', 'ENGAGED']:
                    active_hostile_tag = h['id']
                    active_hostile_color = C_AMBER
                    
                    cx, cy = h['pos']
                    s = 30
                    ax.plot([cx-s, cx-s, cx-s+10], [cy+s, cy+s-10, cy+s-10], color=C_AMBER, lw=3)
                    ax.plot([cx-s, cx-s, cx-s+10], [cy-s, cy-s+10, cy-s+10], color=C_AMBER, lw=3)
                    ax.plot([cx+s, cx+s, cx+s-10], [cy+s, cy+s-10, cy+s-10], color=C_AMBER, lw=3)
                    ax.plot([cx+s, cx+s, cx+s-10], [cy-s, cy-s+10, cy-s+10], color=C_AMBER, lw=3)
                    ax.text(cx + 40, cy, h['id'], color=C_AMBER, fontsize=14, fontname='monospace', weight='bold')

                    # Calculate Ghost Intercept Point
                    dist = np.linalg.norm(h['pos'] - base_pos)
                    tti = dist / interceptor_speed
                    ghost_x = h['pos'][0] + (h['vel'][0] * tti)
                    ghost_y = h['pos'][1] + (h['vel'][1] * tti)
                    
                    ax.plot([base_pos[0], ghost_x], [base_pos[1], ghost_y], color=C_PHOSPHOR_BLUE, linestyle=':', lw=2, alpha=0.5)
                    ax.scatter(ghost_x, ghost_y, marker='x', color=C_PHOSPHOR_BLUE, s=100)

                # Interceptor Logic
                if h['state'] == 'ENGAGED':
                    active_hostile_tag = f"{h['id']} - DATALINK"
                    
                    dist = np.linalg.norm(h['pos'] - h['int_pos'])
                    tti = dist / interceptor_speed
                    dyn_ghost = h['pos'] + (h['vel'] * tti)
                    
                    dir_vec = dyn_ghost - h['int_pos']
                    if np.linalg.norm(dir_vec) > 0.1:
                        dir_norm = dir_vec / np.linalg.norm(dir_vec)
                        h['int_pos'] += dir_norm * interceptor_speed
                        
                    h['int_history'].append((h['int_pos'][0], h['int_pos'][1]))
                    if len(h['int_history']) > 30: h['int_history'].pop(0)

                    if len(h['int_history']) > 2:
                        ipts = np.array(h['int_history'])
                        alphas = np.linspace(0.0, 0.9, len(ipts))
                        for i in range(len(ipts)-1):
                            ax.plot(ipts[i:i+2, 0], ipts[i:i+2, 1], color=C_PHOSPHOR_BLUE, lw=3, alpha=alphas[i])

                    ax.scatter(h['int_pos'][0], h['int_pos'][1], marker='^', c=C_PHOSPHOR_BLUE, s=150, zorder=10)
                    
                    if f % 10 < 5:
                        ax.plot([base_pos[0], h['int_pos'][0]], [base_pos[1], h['int_pos'][1]], color=C_AMBER, lw=1, alpha=0.3)

                    # Collision Resolution
                    if np.linalg.norm(h['int_pos'] - h['pos']) < interceptor_speed * 1.5:
                        h['state'] = 'DESTROYED'
                        h['bloom'] = 1.0

            # SAGE Vector Explosion Bloom
            if h['state'] == 'DESTROYED' and h['bloom'] > 0:
                active_hostile_tag = "SPLASH"
                active_hostile_color = C_MANTIS
                for radius_mult in [0.5, 1.0, 1.5]:
                    circle = plt.Circle(h['pos'], 150 * (1 - h['bloom']) * radius_mult, 
                                        color=C_PHOSPHOR_BLUE, fill=False, lw=4 * h['bloom'], alpha=h['bloom'])
                    ax.add_patch(circle)
                    
                ax.scatter(h['pos'][0], h['pos'][1], s=5000 * (1-h['bloom']), c=C_AMBER, marker='x', alpha=h['bloom'], lw=3)
                h['bloom'] -= 0.02

        # ------------------------------------------------------------------
        # UI OVERLAYS (The Command Terminal)
        # ------------------------------------------------------------------
        # Top Header Overlay
        ax.add_patch(plt.Rectangle((0, 1850), 1080, 70, color=C_VOID, alpha=0.8))
        ax.axhline(1850, color=C_PHOSPHOR_BLUE, lw=2)
        ax.text(40, 1870, "USAF AN/FSQ-7 [SEMI-AUTOMATIC GROUND ENVIRONMENT]", color=C_PHOSPHOR_BLUE, fontsize=20, fontname='monospace', weight='bold')
        
        # Biometric Block
        ax.text(850, 1870, f"CYC:{f:05d}", color=C_PHOSPHOR_BLUE, fontsize=20, fontname='monospace')
        
        # SAGE Status Block
        ax.add_patch(plt.Rectangle((0, 0), 1080, 160, color=C_PHOSPHOR_DIM, alpha=0.1))
        ax.axhline(160, color=C_PHOSPHOR_BLUE, lw=2)
        
        ax.text(40, 110, f"SYSTEM TRAFFIC : 12 CONTACTS TRACKED", color=C_PHOSPHOR_BLUE, fontsize=22, fontname='monospace')
        ax.text(40, 60, f"KINETIC FOCUS  : ", color=C_PHOSPHOR_BLUE, fontsize=22, fontname='monospace')
        ax.text(320, 60, active_hostile_tag, color=active_hostile_color, fontsize=24, fontname='monospace', weight='bold')
        
        if active_hostile_tag == "NOMINAL":
            ax.text(40, 15, "> SCANNING SECTOR...", color=C_PHOSPHOR_DIM, fontsize=18, fontname='monospace')
        else:
            pulse = C_TEXT if (f % 10) < 5 else C_PHOSPHOR_BLUE
            ax.text(40, 15, "> SENSOR FUSION ACTIVE OVERRIDE", color=pulse, fontsize=18, fontname='monospace')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close(fig)

if __name__ == "__main__": run()
