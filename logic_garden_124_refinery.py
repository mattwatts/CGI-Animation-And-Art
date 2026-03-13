"""
SOVEREIGN CODE: logic_garden_123_refinery.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python High-Fidelity Simulator
SCENE: Logic Garden 123 (Scopus -> Pure Phase Transition)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.colors as mcolors
import os

# CONFIG
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_123_refinery"
os.makedirs(OUT_DIR, exist_ok=True)

# THE INDUSTRIAL PALETTE
C_VOID = '#050510'       # Deep Institutional Void
C_SCOPUS_NOISE = '#FF2244' # Red Entropy
C_PARSER = '#00FFCC'     # Cyan Logic Line
C_PURE_XML = '#FFDD33'   # Gold Structure
C_EDGE = '#FFFFFF'       # White Syntax connections

def run():
    print(f"LOGIC GARDEN 123: THE REFINERY ({TOTAL_FRAMES} frames)")
    
    # 1. DEFINE THE FINAL "PURE" STRUCTURE (The Gold Lattice)
    # A structured fractal tree/grid
    num_nodes = 60
    pure_positions = []
    edges = []
    
    # Simple hierarchy layout for visualization
    cols, rows = 5, 12
    margin_x, margin_y = 200, 300
    w, h = 1080 - 2*margin_x, 1920 - 2*margin_y
    
    for i in range(num_nodes):
        r = i // cols
        c = i % cols
        px = margin_x + (w / (cols-1)) * c
        py = margin_y + (h / (rows-1)) * r
        pure_positions.append([px, py])
        
        # Define strict structural edges (connecting rows/cols)
        if c > 0: edges.append((i, i-1))
        if r > 0: edges.append((i, i-cols))

    pure_positions = np.array(pure_positions)
    
    # 2. DEFINE THE INITIAL "SCOPUS" STATE (The Ragged Graph)
    # Chaotic, randomized positions rightwards
    np.random.seed(42)
    scopus_positions = pure_positions + np.random.normal(0, 150, (num_nodes, 2))
    
    # Pre-calculate random drift phases for the vibration effect
    drift_phases = np.random.uniform(0, 2*np.pi, (num_nodes, 2))
    drift_speeds = np.random.uniform(0.5, 2.0, num_nodes)

    for f in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(C_VOID)
        
        progress = f / TOTAL_FRAMES
        
        # 3. THE O(N) LINE SWEEP (Right to Left)
        # Starts off screen right, sweeps completely off screen left
        scan_x = 1200 - (progress * 1320)  
        
        # Draw the Parser Beam
        if -100 < scan_x < 1180:
            ax.axvline(scan_x, color=C_PARSER, linewidth=4, alpha=0.8)
            ax.axvspan(scan_x, scan_x+50, color=C_PARSER, alpha=0.1) # Glowing trail
        
        current_positions = []
        is_structured = []

        # 4. COMPUTE NODE STATES
        for i in range(num_nodes):
            # True if the scanner has passed over the final target X coordinate
            node_target_x = pure_positions[i][0]
            passed = scan_x < node_target_x 
            
            if not passed:
                # STATE: Scopus Entropy (Red, drifting, vibrating)
                dx = np.sin((f/FPS) * drift_speeds[i]*5 + drift_phases[i][0]) * 10
                dy = np.cos((f/FPS) * drift_speeds[i]*5 + drift_phases[i][1]) * 10
                pos = scopus_positions[i] + [dx, dy]
                current_positions.append(pos)
                is_structured.append(False)
            else:
                # STATE: Pure XML (Instantly snapped to Gold Lattice)
                current_positions.append(pure_positions[i])
                is_structured.append(True)

        current_positions = np.array(current_positions)

        # 5. DRAW EDGES (Only draw if BOTH nodes are structured)
        for e in edges:
            n1, n2 = e[0], e[1]
            if is_structured[n1] and is_structured[n2]:
                x_vals = [current_positions[n1][0], current_positions[n2][0]]
                y_vals = [current_positions[n1][1], current_positions[n2][1]]
                ax.plot(x_vals, y_vals, color=C_EDGE, linewidth=2, zorder=1, alpha=0.6)

        # 6. DRAW NODES
        for i in range(num_nodes):
            x, y = current_positions[i]
            if is_structured[i]:
                # The Golden Super-Node Standard
                ax.add_patch(Circle((x, y), 12, color=C_PURE_XML, zorder=2))
                ax.add_patch(Circle((x, y), 20, color=C_PURE_XML, zorder=1, alpha=0.2)) # Glow
            else:
                # The Red Scopus Noise
                ax.add_patch(Circle((x, y), 8, color=C_SCOPUS_NOISE, zorder=2))

        # UI OVERLAYS
        ax.text(540, 1800, "PROTOCOL: BRACE-MATCHING EXTRACTION", color=C_PARSER, ha='center',
                fontsize=30, fontname='monospace', alpha=0.7)
        
        status = "STATUS: ALIGNED (GOLD STANDARD)" if progress > 0.85 else "STATUS: PARSING METADATA..."
        ax.text(540, 1750, status, color=C_PURE_XML if progress > 0.85 else C_SCOPUS_NOISE, ha='center',
                fontsize=35, fontname='monospace', weight='bold')

        # Limit rendering area
        ax.set_xlim(0, 1080)
        ax.set_ylim(0, 1920)

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
