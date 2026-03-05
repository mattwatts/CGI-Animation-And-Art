"""
SOVEREIGN CODE: logic_garden_18c_quantum.py
VARIATION: 18c (Quantum Alchemist)
FORMAT: YouTube Shorts (9:16)
DURATION: 40 Seconds
VISUAL: Wave Packets, Superposition, Probability Clouds (No solid particles)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from matplotlib.patches import Ellipse

FPS = 30
DURATION = 40
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_18c_quantum"
os.makedirs(OUT_DIR, exist_ok=True)

# Canvas
W, H = 9, 16 
CENTER = np.array([4.5, 8.0])

def run():
    print("LOGIC GARDEN 18c: QUANTUM ALCHEMIST")
    fig = plt.figure(figsize=(9, 16), facecolor='#020205') # Deep Quantum Void
    ax = fig.add_axes([0, 0, 1, 1], facecolor='#020205')
    
    # PARAMETERS
    N_TOTAL = 150
    n_protons = int(150 * 0.38)
    
    # Init Quantum States (Particles)
    # Instead of x,y, we have orbital parameters
    states = []
    
    np.random.seed(42)
    for i in range(N_TOTAL):
        # Position in cloud (Mean position)
        r_mean = np.random.uniform(0.1, 2.5) 
        theta_mean = np.random.uniform(0, 2*np.pi)
        
        # Phase for breathing
        phase = np.random.uniform(0, 2*np.pi)
        freq = np.random.uniform(0.1, 0.3)
        
        p_type = 0 if i < n_protons else 1 
        
        states.append({
            'r_mean': r_mean,
            'theta_mean': theta_mean,
            'phase': phase,
            'freq': freq,
            'type': p_type,
            'id': i,
            'active': True
        })
        
    # THE GHOST WAVE PACKET
    # A soliton moving down
    ghost = {
        'y': 14.5, 'x': 4.5,
        'vy': -0.0131, # Syncs to 14s
        'active': True,
        'merged': False,
        'waiting': False,
        'phase': 0
    }
    
    sparks = [] # High freq electrons
    
    # GLOBAL VORTEX SPIN
    global_spin = 0.0
    
    for f in range(TOTAL_FRAMES):
        ax.clear()
        ax.set_xlim(0, 9)
        ax.set_ylim(0, 16)
        ax.axis('off')
        
        # TIME PHASES (Matches 18b)
        # 0-14s: Approach
        # 14-24s: Fever
        # 24-32s: Neptunium
        # 32-40s: Plutonium
        
        phase_title = "URANIUM-238"
        sub_title = "QUANTUM SUPERPOSITION"
        title_col = "#FF4444"
        
        # Cloud Agitation Level (Amplitude of breathing)
        agitation = 0.05 
        global_spin += 0.005 # Slow rotation
        
        if f < 420:
             sub_title = "WAVE FUNCTION COLLAPSE"
             title_col = "#4444FF" 
             if ghost['y'] <= 9.0 and not ghost['merged']:
                 ghost['y'] = 9.0
                 ghost['waiting'] = True
                 
        elif f < 720: # FEVER
            phase_title = "U-239 (Exited State)"
            sub_title = "PHASE DECOHERENCE"
            agitation = 0.3 # High turbulence
            title_col = "#FF00FF"
            
            if not ghost['merged']:
                # The wave packet merges into the cloud
                states.append({
                    'r_mean': 2.5, # Edge
                    'theta_mean': np.pi/2,
                    'phase': 0, 'freq': 0.5,
                    'type': 1, 'id': 999, 'active': True
                })
                ghost['merged'] = True
                
        elif f < 960: # NEPTUNIUM
            phase_title = "NEPTUNIUM-239"
            sub_title = "BETA DECAY (e- EMISSION)"
            title_col = "#00AAFF"
            agitation = 0.15
            
            if f == 720:
                ts = [s for s in states if s.get('id') == 999]
                if ts:
                    ts[0]['type'] = 0 
                    # Emit Spark (Vector)
                    sparks.append({'x': CENTER[0], 'y': CENTER[1], 'vx': 6.0, 'vy': 5.0, 'phase':0})
                    
        else:
            phase_title = "PLUTONIUM-239"
            sub_title = "STABLE STATE"
            title_col = "#FFD700"
            agitation = 0.05
            
            if f == 960:
                ts = [s for s in states if s['type'] == 1 and s.get('id') != 999]
                if ts:
                    ts[0]['type'] = 0
                    sparks.append({'x': CENTER[0], 'y': CENTER[1], 'vx': -6.0, 'vy': 3.0, 'phase':0})

        # RENDER QUANTUM CLOUD
        # We draw each "particle" as a translucent ellipse
        # This creates the "Cloud" effect via alpha blending
        
        for s in states:
            # Update Phase
            s['phase'] += s['freq'] + (agitation * 2.0)
            
            # Breathing Radius
            # The particle isn't a point, it's a probability orbital
            # r varies sinusoidally
            orbit_r = 0.3 + 0.1 * np.sin(s['phase']) 
            if agitation > 0.1: orbit_r += np.random.uniform(0, agitation) # Noise
            
            # Position (Orbiting the center)
            # Add Agitation to angular pos
            theta = s['theta_mean'] + global_spin
            if agitation > 0.1: theta += np.sin(f*0.1) * 0.1
            
            # Calculate Center of Orbital
            cx = CENTER[0] + s['r_mean'] * np.cos(theta)
            cy = CENTER[1] + s['r_mean'] * np.sin(theta)
            
            # Color Physics
            # Protons (Red) = High freq / Neutrons (Blue) = Low freq
            # Use Alpha to show superposition
            color = '#FF0000' if s['type'] == 0 else '#0066FF'
            alpha = 0.15 if s['type'] == 0 else 0.15 # Very transparent
            
            # Draw Orbital
            # Rotated ellipse for "Swirl" effect
            angle = np.degrees(theta) + 90
            ellipse = Ellipse((cx, cy), width=orbit_r*2, height=orbit_r*1.2, angle=angle, 
                             color=color, alpha=alpha, linewidth=0)
            ax.add_patch(ellipse)
            
            # Add a "Core" dot for coherence?
            # Tiny dot
            ax.scatter(cx, cy, s=2, c=color, alpha=0.4)

        # RENDER GHOST (Soliton)
        if not ghost['merged'] and not ghost['waiting']:
            ghost['y'] += ghost['vy']
            ghost['phase'] += 0.5
            
            # Draw Soliton (Concentric Rings moving)
            gx, gy = ghost['x'], ghost['y']
            for i in range(3):
                r = 0.3 + (i * 0.2) + 0.1 * np.sin(ghost['phase'])
                c = plt.Circle((gx, gy), r, color='#00FFFF', fill=False, alpha=0.5 - (i*0.1), linewidth=2)
                ax.add_patch(c)
                
            # Core
            ax.scatter(gx, gy, c='#FFFFFF', s=50, alpha=0.8, edgecolors='none', zorder=20)

        # RENDER SPARKS (High Freq Wave Packets)
        for s in sparks:
            s['x'] += s['vx'] * 0.3
            s['y'] += s['vy'] * 0.3
            s['phase'] += 1.0
            
            # Draw "Photon" / Electron Wave
            # A sine wave perp to direction?
            # Simplified: A glowing "Chevron" or dash
            
            # Tail
            tail_x = s['x'] - s['vx']*1.2
            tail_y = s['y'] - s['vy']*1.2
            
            ax.plot([s['x'], tail_x], [s['y'], tail_y], color='#FFFF00', linewidth=3, alpha=0.9)
            
            # Shockwave rings around head
            r = 0.5 * (f % 5) / 5.0
            c = plt.Circle((s['x'], s['y']), r, color='#FFFF00', fill=False, linewidth=1, alpha=1-r)
            ax.add_patch(c)

        # TEXT (HUD)
        ax.text(W/2, 15, phase_title, color=title_col, ha='center', fontsize=30, weight='bold', fontfamily='monospace',
                bbox=dict(facecolor='#000000', alpha=0.7, edgecolor='none'))
        ax.text(W/2, 14, sub_title, color='#888888', ha='center', fontsize=18, fontfamily='monospace')

        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=80, facecolor='#020205')
        plt.close(fig)

if __name__ == "__main__": run()
