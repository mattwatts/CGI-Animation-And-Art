"""
SOVEREIGN CODE: logic_garden_97_attractor.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: Wikipedia 'Getting to Philosophy' Phenomenon
VISUAL: 100 Paths collapsing into a central Singularity.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_97_attractor"
os.makedirs(OUT_DIR, exist_ok=True)

# Canvas
W, H = 9, 16 
CENTER = (4.5, 8.0)

def run():
    print("LOGIC GARDEN 97: THE STRANGE ATTRACTOR")
    fig = plt.figure(figsize=(9, 16), facecolor='#050010') # Deep Void Purple
    ax = fig.add_axes([0, 0, 1, 1], facecolor='#050010')
    
    # PARAMETERS
    num_particles = 100
    
    # Initialize particles at the "Edge of Knowledge" (Outer Ring)
    # They have a 'Level' (Distance from Philosophy)
    # Level 0 = Philosophy. Level 6 = Toaster.
    
    particles = []
    np.random.seed(42)
    
    for i in range(num_particles):
        angle = np.random.uniform(0, 2*np.pi)
        dist = np.random.uniform(3.5, 4.5) # Outer rim
        
        particles.append({
            'x': CENTER[0] + dist * np.cos(angle),
            'y': CENTER[1] + dist * np.sin(angle),
            'target_x': CENTER[0], # Ultimate target
            'target_y': CENTER[1],
            'angle': angle,
            'dist': dist,
            'speed': np.random.uniform(0.02, 0.05),
            'wobble_phase': np.random.uniform(0, 10),
            'history': [], # For trails
            'captured': False
        })
        
    for f in range(TOTAL_FRAMES):
        ax.clear()
        ax.set_xlim(0, 9)
        ax.set_ylim(0, 16)
        ax.axis('off')
        
        # DRAW CENTER (PHILOSOPHY)
        # It pulses
        pulse = 0.2 + 0.05 * np.sin(f * 0.1)
        phil_circle = plt.Circle(CENTER, pulse, color='#FFD700', zorder=100) # Gold
        ax.add_patch(phil_circle)
        
        # Halo
        halo = plt.Circle(CENTER, pulse * 4, color='#FFD700', alpha=0.1, zorder=50)
        ax.add_patch(halo)
        
        # TEXT
        ax.text(CENTER[0], CENTER[1] + 6.5, "ALL ROADS LEAD TO", color='white', ha='center', fontsize=20, fontfamily='monospace')
        ax.text(CENTER[0], CENTER[1] + 6.0, "PHILOSOPHY", color='#FFD700', ha='center', fontsize=40, weight='bold', fontfamily='monospace')

        # UPDATE PARTICLES
        for p in particles:
            if p['captured']:
                continue
                
            # Move towards center (The Attractor)
            # Logic: Spiral movement
            
            # Decrease distance
            p['dist'] -= p['speed']
            
            # Rotate (Spiral effect)
            p['angle'] += 0.05
            
            if p['dist'] < 0.2:
                p['dist'] = 0.2
                p['captured'] = True
                
            # Calculate new X/Y
            # Add "Concept Wobble" (Concepts aren't straight lines)
            wobble = 0.1 * np.sin(f * 0.1 + p['wobble_phase'])
            
            nx = CENTER[0] + p['dist'] * np.cos(p['angle'] + wobble)
            ny = CENTER[1] + p['dist'] * np.sin(p['angle'] + wobble)
            
            p['x'] = nx
            p['y'] = ny
            
            # History for trails
            p['history'].append((nx, ny))
            if len(p['history']) > 20: p['history'].pop(0)
            
            # Draw Trail
            if len(p['history']) > 1:
                hx = [h[0] for h in p['history']]
                hy = [h[1] for h in p['history']]
                # Alpha fades
                ax.plot(hx, hy, color='#00CCFF', linewidth=1, alpha=0.4)
                
            # Draw Head
            ax.scatter(nx, ny, color='white', s=15, alpha=0.8)

        # HUD STATS
        # "Hop Count" simulation
        avg_dist = np.mean([p['dist'] for p in particles])
        hops = int(avg_dist * 5)
        
        ax.text(4.5, 2.0, f"AVG SEPARATION: {hops}", color='#00CCFF', ha='center', fontsize=25, fontfamily='monospace')
        
        if f > 500:
             ax.text(4.5, 1.5, "CONVERGENCE ACHIEVED", color='#FFD700', ha='center', fontsize=20)

        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=80, facecolor='#050010')
        plt.close(fig)

if __name__ == "__main__": run()
