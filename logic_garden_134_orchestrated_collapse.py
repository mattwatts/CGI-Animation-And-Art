"""
SOVEREIGN CODE: logic_garden_134_orchestrated_collapse.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python High-Fidelity Simulator (Vectorized Numpy Array)
SCENE: Logic Garden 134 (The Orchestrated Collapse - 30Hz Gamma Lock)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import math
import os

# -------- COMPILE-TIME METRICS --------
FPS = 60                        # Required for the 30Hz Nyquist Lock
DURATION = 20                   # 20-Second Complete Cycle
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_134_collapse"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE --------
C_VOID = '#020205'              # Absolute Black
C_CYAN = '#00FFCC'              # Superposition Wave A
C_PURPLE = '#7B00FF'            # Superposition Wave B
C_GOLD = '#FFD700'              # The Observer (Nila Bindu)
C_MANTIS = '#39FF14'            # Terminal Green (4D Flow State)
C_TEXT = '#FFFFFF'

def run():
    print(f"LOGIC GARDEN 134: THE ORCHESTRATED COLLAPSE")
    print(f"Executing: {FPS} FPS | 30Hz Gamma Harmonic Limit | Total: {TOTAL_FRAMES} frames")

    # 1. INITIALIZE THE 3D QUANTUM LATTICE (6x6x6 Grid = 216 Nodes)
    grid_res = 6
    spacing = 40
    lin = np.linspace(-(grid_res-1)*spacing/2, (grid_res-1)*spacing/2, grid_res)
    X, Y, Z = np.meshgrid(lin, lin, lin)
    target_pos = np.column_stack([X.ravel(), Y.ravel(), Z.ravel()])
    V = len(target_pos)

    # 2. PRE-COMPUTE 4D CRYSTAL EDGES
    edges = []
    for i in range(grid_res):
        for j in range(grid_res):
            for k in range(grid_res):
                idx = i*(grid_res**2) + j*grid_res + k
                if i < grid_res - 1: edges.append((idx, idx + grid_res**2))
                if j < grid_res - 1: edges.append((idx, idx + grid_res))
                if k < grid_res - 1: edges.append((idx, idx + 1))
    edges = np.array(edges)

    for f in range(TOTAL_FRAMES):
        t = f / FPS
        
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        fig.patch.set_facecolor(C_VOID)
        ax.set_facecolor(C_VOID)
        ax.set_xlim(0, 1080)
        ax.set_ylim(0, 1920)

        # ------------------------------------------------------------------
        # STAGE COMMAND LOGIC (The Bounding Box of Reality)
        # ------------------------------------------------------------------
        if t < 2.0:
            sys_state = "STATE: QUANTUM SUPERPOSITION [HIGH ENTROPY]"
            R = 0  # Observer Offline
            gold_alpha = 0
        elif t < 4.0:
            sys_state = "STATE: DIMENSIONAL COMPILER ONLINE [COLLAPSING]"
            # Smooth step expansion of the Bubble of Reality
            progress = (t - 2.0) / 2.0
            R = progress * 300 
            gold_alpha = 1.0
        elif t < 16.0:
            sys_state = "STATE: 4D PHASE DECOHERENCE [TERMINAL GREEN]"
            R = 300 # Lock the crystal
            gold_alpha = 1.0
        elif t < 18.0:
            sys_state = "STATE: OBSERVER DECOUPLING [TATHĀTĀ]"
            progress = 1.0 - ((t - 16.0) / 2.0)
            R = max(0, progress * 300)
            gold_alpha = progress
        else:
            sys_state = "STATE: RETURN TO THE VOID"
            R = 0
            gold_alpha = 0

        # ------------------------------------------------------------------
        # SYSTEM PHYSICS & PROJECTION
        # ------------------------------------------------------------------
        # The 30Hz Gamma Pulse (ON every even frame, OFF every odd frame)
        gamma_pulse = 1.0 if f % 2 == 0 else 0.4
        
        # Calculate localized chaos (The Wave State)
        noise_x = np.sin(target_pos[:, 1]/30 + t*3) * 60
        noise_y = np.cos(target_pos[:, 0]/30 + t*2) * 50
        noise_z = np.sin(target_pos[:, 2]/30 + t*4) * 60
        noise_pos = target_pos + np.column_stack([noise_x, noise_y, noise_z])

        # Phase Decomposition Lerp (Calculate who is inside the Reality Bubble)
        dists = np.linalg.norm(target_pos, axis=1)
        # W = 1 (Reality Grid), W = 0 (Chaos Wave)
        W = np.clip((R - dists) / 40.0, 0, 1).reshape(-1, 1)
        
        current_pos = W * target_pos + (1 - W) * noise_pos

        # Faux-Isometric 3D Rotation Math
        rot_y = t * math.pi / 6  # Sweeping rotation
        rot_x = math.pi / 5      # Isometric downward tilt
        
        cy, sy = math.cos(rot_y), math.sin(rot_y)
        cx, sx = math.cos(rot_x), math.sin(rot_x)
        
        Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
        Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
        
        rotated = current_pos @ Ry.T @ Rx.T
        
        # Scale to 1080x1920
        scale = 3.8
        px = 540 + rotated[:, 0] * scale
        py = 960 + rotated[:, 1] * scale
        W_flat = W.ravel()

        # ------------------------------------------------------------------
        # PROTOCOL: NEON POP RENDERING
        # ------------------------------------------------------------------
        # 1. Render Floating Probability Particles (Outside Bounding Box)
        chaos_mask = W_flat < 0.9
        ax.scatter(px[chaos_mask], py[chaos_mask], s=15, c=C_CYAN, alpha=0.5, edgecolors='none')
        ax.scatter(px[chaos_mask], py[chaos_mask]-10, s=25, c=C_PURPLE, alpha=0.3, edgecolors='none')

        # 2. Render Emergent 4D Geometry (Inside Bounding Box)
        valid_edges = (W_flat[edges[:, 0]] > 0.8) & (W_flat[edges[:, 1]] > 0.8)
        if np.any(valid_edges):
            active_edges = edges[valid_edges]
            segs = [[(px[i], py[i]), (px[j], py[j])] for i, j in active_edges]
            
            # The Mantis Gamma Lock
            line_alpha = 0.5 + (0.5 * gamma_pulse)
            lc = LineCollection(segs, colors=C_MANTIS, linewidths=2.0 * gamma_pulse + 1.0, alpha=line_alpha)
            ax.add_collection(lc)

        # 3. Render The Observer (The Golden Node)
        if gold_alpha > 0:
            ax.scatter(540, 960, s=800 * gold_alpha, c=C_GOLD, alpha=0.2 * gamma_pulse * gold_alpha, edgecolors='none')
            ax.scatter(540, 960, s=300 * gold_alpha, c=C_GOLD, alpha=0.6 * gold_alpha, edgecolors='none')
            ax.scatter(540, 960, s=100 * gold_alpha, c=C_TEXT, alpha=gold_alpha, edgecolors='none')

        # ------------------------------------------------------------------
        # PROTOCOL: UI DECOUPLING & FLIGHT RECORDER
        # ------------------------------------------------------------------
        if f > 10:
            ax.text(80, 1820, sys_state, color=C_TEXT, fontsize=24, fontname='monospace', weight='bold')
            ax.text(80, 1770, f"OBSERVER RADIUS : {R:06.1f} Planck Lengths", color=C_TEXT, fontsize=20, fontname='monospace')
            ax.text(80, 1720, f"BIOMETRIC CLOCK : 30Hz Gamma Band", color=C_GOLD, fontsize=20, fontname='monospace')
            
            if "TERMINAL GREEN" in sys_state:
                ax.text(540, 200, "FLOW STATE ACHIEVED", color=C_MANTIS, ha='center', fontsize=35, fontname='monospace', weight='bold')

        # Rosetta Stone Header (Frames 0-10)
        if f <= 10:
            ax.text(540, 1100, "THE ORCHESTRATED COLLAPSE", color=C_GOLD, ha='center', fontsize=50, fontname='monospace', weight='bold')
            ax.text(540, 960, "Phase Decoherence Visualized", color=C_CYAN, ha='center', fontsize=35, fontname='monospace')
            ax.text(540, 800, "LOGIC GARDEN 134", color=C_TEXT, ha='center', fontsize=20, fontname='monospace')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close(fig)

if __name__ == "__main__": run()
