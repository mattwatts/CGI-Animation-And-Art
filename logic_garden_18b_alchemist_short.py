"""
SOVEREIGN CODE: logic_garden_v94_alchemist_final.py
FORMAT: YouTube Shorts (9:16)
DURATION: 40 Seconds
FIX: 
1. Neutron Sync (Hit @ 14s)
2. Electron Trails (Speed lines, NO Tethers)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

FPS = 30
DURATION = 40
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_v94_alchemist_final"
os.makedirs(OUT_DIR, exist_ok=True)

# Canvas
W, H = 9, 16 
CENTER = np.array([4.5, 8.0])

def run():
    print("LOGIC GARDEN 94: THE ALCHEMIST (FINAL CUT)")
    fig = plt.figure(figsize=(9, 16), facecolor='#050505')
    ax = fig.add_axes([0, 0, 1, 1], facecolor='#050505')
    
    # PARAMETERS
    N_TOTAL = 150
    n_protons = int(150 * 0.38)
    
    # Init Particles
    particles = []
    
    np.random.seed(42)
    for i in range(N_TOTAL):
        r = np.random.uniform(0, 2.5) 
        theta = np.random.uniform(0, 2*np.pi)
        px = CENTER[0] + r * np.cos(theta)
        py = CENTER[1] + r * np.sin(theta)
        p_type = 0 if i < n_protons else 1 
        particles.append({
            'x': px, 'y': py, 'vx': 0, 'vy': 0, 'type': p_type, 'id': i
        })
        
    # GHOST NEUTRON (Sync target: 14s / Frame 420)
    # Start: 14.5, End: 9.0. Dist: 5.5
    # Speed: 5.5 / 420 = 0.0131
    ghost = {
        'x': 4.5, 'y': 14.5, 
        'vx': 0, 'vy': -0.0131, 
        'type': 1, 
        'active': True,
        'merged': False,
        'waiting': False
    }
    
    sparks = [] 
    
    for f in range(TOTAL_FRAMES):
        ax.clear()
        ax.set_xlim(0, 9)
        ax.set_ylim(0, 16)
        ax.axis('off')
        
        # TIME PHASES
        phase_title = "URANIUM-238"
        sub_title = "STABLE ISOTOPE"
        shiver_mag = 0.01 
        title_col = "#FF4444"
        
        # 1. APPROACH (0-14s)
        if f < 420:
             sub_title = "NEUTRON APPROACH"
             title_col = "#4444FF" 
             
             # Collision Guard
             if ghost['y'] <= 9.0 and not ghost['merged']:
                 ghost['y'] = 9.0
                 ghost['waiting'] = True
                 
        # 2. CAPTURE / FEVER (14-24s)
        elif f < 720:
            phase_title = "U-239 (UNSTABLE)"
            sub_title = "CRITICAL MASS"
            shiver_mag = 0.15 # VIOLENT
            title_col = "#FF00FF"
            
            # TRIGGER MERGE 
            if not ghost['merged']:
                particles.append({
                    'x': ghost['x'], 'y': ghost['y'], 'vx': 0, 'vy': -0.5, 'type': 1, 'id': 999
                })
                ghost['merged'] = True
                
        # 3. NEPTUNIUM (24-32s)
        elif f < 960:
            phase_title = "NEPTUNIUM-239"
            sub_title = "BETA DECAY (e- EJECTION)"
            title_col = "#00AAFF"
            shiver_mag = 0.08
            
            # TRIGGER 1: Frame 720
            if f == 720:
                ts = [p for p in particles if p.get('id') == 999]
                if ts:
                    ts[0]['type'] = 0 
                    # SPARK 1
                    sparks.append({'x': ts[0]['x'], 'y': ts[0]['y'], 'vx': 6.0, 'vy': 5.0, 'type': 2})
                    
        # 4. PLUTONIUM (32-40s)
        else:
            phase_title = "PLUTONIUM-239"
            sub_title = "THE KING OF ELEMENTS"
            title_col = "#FFD700"
            shiver_mag = 0.02
            
            # TRIGGER 2: Frame 960
            if f == 960:
                blacks = [p for p in particles if p['type'] == 1 and p.get('id') != 999]
                if blacks:
                    blacks[0]['type'] = 0
                    # SPARK 2
                    sparks.append({'x': blacks[0]['x'], 'y': blacks[0]['y'], 'vx': -6.0, 'vy': 3.0, 'type': 2})

        # PHYSICS
        for p in particles:
            dx = CENTER[0] - p['x']
            dy = CENTER[1] - p['y']
            dist = np.sqrt(dx*dx + dy*dy)
            force = 0.01 * dist
            # Volume repulsion
            if dist < 1.2: force -= 0.04
            
            p['vx'] += force * dx
            p['vy'] += force * dy
            p['vx'] += np.random.uniform(-shiver_mag, shiver_mag)
            p['vy'] += np.random.uniform(-shiver_mag, shiver_mag)
            p['vx'] *= 0.9
            p['vy'] *= 0.9
            p['x'] += p['vx']
            p['y'] += p['vy']

        # GHOST
        if not ghost['merged'] and not ghost['waiting']:
            ghost['y'] += ghost['vy']
            ghost['x'] = 4.5 + np.sin(f * 0.1) * 0.05

        # SPARKS
        for s in sparks:
            s['x'] += s['vx'] * 0.3
            s['y'] += s['vy'] * 0.3
            # Friction? No, electrons fly free.

        # RENDER ----------------
        
        # Neutrons (Blue)
        nx = [p['x'] for p in particles if p['type'] == 1]
        ny = [p['y'] for p in particles if p['type'] == 1]
        ax.scatter(nx, ny, c='#0066FF', s=180, alpha=0.9, edgecolors='none')
        
        # Protons (Red)
        px = [p['x'] for p in particles if p['type'] == 0]
        py = [p['y'] for p in particles if p['type'] == 0]
        ax.scatter(px, py, c='#FF2222', s=180, alpha=0.9, edgecolors='none')
        
        # Ghost
        if not ghost['merged']:
            ax.scatter(ghost['x'], ghost['y'], c='#00CCFF', s=200, edgecolors='white', linewidth=2, zorder=20)
            
        # Sparks (THE FIX: Independent Speed Trails)
        for s in sparks:
            # The Head
            ax.scatter(s['x'], s['y'], c='#FFFF00', s=120, edgecolors='white', linewidth=2, zorder=30)
            
            # The Tail (Vector based on CURRENT velocity)
            # NOT tethered to center
            tail_end_x = s['x'] - s['vx'] * 1.5 
            tail_end_y = s['y'] - s['vy'] * 1.5
            
            ax.plot([s['x'], tail_end_x], [s['y'], tail_end_y], c='#FFFF00', linewidth=4, alpha=0.8)

        # TEXT
        ax.text(W/2, 14.5, phase_title, color=title_col, ha='center', fontsize=30, weight='bold', fontfamily='monospace',
                bbox=dict(facecolor='black', edgecolor=title_col, pad=0.5))
        ax.text(W/2, 13.5, sub_title, color='#AAAAAA', ha='center', fontsize=20, fontfamily='monospace')
        
        if f > 720:
             ax.text(W/2, 2.0, r"$n \rightarrow p + e^-$", color='#666666', ha='center', fontsize=30)

        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=80, facecolor='#050505')
        plt.close(fig)

if __name__ == "__main__": run()
