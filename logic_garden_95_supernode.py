"""
SOVEREIGN CODE: logic_garden_95_supernode.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: Network Topology / Six Degrees of Separation
VISUAL: Disconnected -> Super-Node -> Gravity Well
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_95_supernode"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 9, 16 
CENTER = (4.5, 8.0)

def run():
    print("LOGIC GARDEN 95: THE SUPER NODE")
    
    # Init Particles (Drifting thoughts)
    N = 300
    particles = []
    np.random.seed(99)
    for i in range(N):
        particles.append({
            'x': np.random.uniform(0, W),
            'y': np.random.uniform(0, H),
            'vx': np.random.uniform(-0.02, 0.02),
            'vy': np.random.uniform(-0.02, 0.02),
            'connected': False
        })
        
    for f in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(9, 16), facecolor='#000510')
        ax = fig.add_axes([0, 0, 1, 1], facecolor='#000510')
        ax.set_xlim(0, W)
        ax.set_ylim(0, H)
        ax.axis('off')
        
        # TIME PHASES
        # 0-180: ENTROPY
        # 180-300: THE EVENT (Node Appears)
        # 300-600: GRAVITY (The Snap)
        
        show_node = False
        gravity_on = False
        node_scale = 0
        
        if f > 180:
            show_node = True
            # Grow animation
            node_scale = min(1.0, (f - 180) / 30.0) 
            
        if f > 300:
            gravity_on = True
            
        # PHYSICS UPDATE
        for p in particles:
            if gravity_on:
                # VELOCITY OVERRIDE
                # Pull straight to center
                dx = CENTER[0] - p['x']
                dy = CENTER[1] - p['y']
                dist = np.sqrt(dx*dx + dy*dy)
                
                # Spring forces
                # Accelerate towards center
                p['vx'] += dx * 0.005
                p['vy'] += dy * 0.005
                
                # Dampen
                p['vx'] *= 0.90
                p['vy'] *= 0.90
                
                # Draw Line (The Edge)
                # Alpha depends on distance?
                alpha = max(0.1, 1.0 - (dist/8.0))
                ax.plot([p['x'], CENTER[0]], [p['y'], CENTER[1]], color='#FFD700', alpha=alpha*0.3, linewidth=0.5)
                
            else:
                # Drift
                p['x'] += p['vx']
                p['y'] += p['vy']
                
                # Bounce
                if p['x'] < 0 or p['x'] > W: p['vx'] *= -1
                if p['y'] < 0 or p['y'] > H: p['vy'] *= -1
            
            # Apply pos
            if gravity_on:
                p['x'] += p['vx']
                p['y'] += p['vy']
                
            # Draw Node
            if gravity_on:
                col = '#FFD700' # Gold
                s = 10
            else:
                col = '#555555' # Grey
                s = 20
            ax.scatter(p['x'], p['y'], c=col, s=s, alpha=0.8)

        # DRAW SUPER NODE
        if show_node:
            s_size = 500 * node_scale
            ax.scatter(CENTER[0], CENTER[1], c='#FFD700', s=s_size, zorder=100, edgecolors='white')
            
            # Label
            if node_scale > 0.8:
                ax.text(CENTER[0], CENTER[1], "SUPER NODE", color='black', ha='center', va='center', 
                       fontsize=12, weight='bold', fontfamily='monospace')
                       
        # HUD
        if f < 180: 
            stats = "TOPOLOGY: DISCONNECTED"
            c = "#888888"
        elif f < 300:
            stats = "NEW VERTEX DETECTED"
            c = "white"
        else:
            stats = f"CONNECTIONS: {N}"
            c = "#FFD700"
            
        ax.text(W/2, 1.0, stats, color=c, ha='center', fontsize=25, fontfamily='monospace')

        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=80, facecolor='#000510')
        plt.close(fig)

if __name__ == "__main__": run()
