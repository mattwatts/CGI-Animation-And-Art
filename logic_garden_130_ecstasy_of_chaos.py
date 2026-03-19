"""
SOVEREIGN CODE: logic_garden_130_ecstasy_of_chaos_v2.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python High-Fidelity Simulator
SCENE: Logic Garden 130 (Ecstasy of Chaos - High Contrast/Slow Flow)
VERSION: 2.0
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import math

# CONFIG
FPS = 30
DURATION = 30 # Extended Cut
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_130_ecstasy_v2"
os.makedirs(OUT_DIR, exist_ok=True)

# THE INDUSTRIAL NEON PALETTE (Forced High-Viz)
C_VOID = '#020205'           # Absolute Vacuum (Darker for maximum contrast)
C_ROYAL = '#9900FF'          # High-Voltage Royal Indigo / Magenta
C_TRUE_BEING = '#FFD700'     # Blinding Gold
C_TEXT = '#FFFFFF'           # White UI
NEON_PALETTE = [
    '#FF003C', # Radiant Red
    '#00FFCC', # Cyan
    '#39FF14', # Mantis Green
    '#FF00FF', # Hot Magenta
    '#FFEA00', # Electric Yellow
    '#00BFFF'  # Deep Sky Blue
]

def draw_bloom_scatter(ax, x, y, sizes, colors, zorder=10):
    """Protocol: NEON POP. 3-Layer Artificial Luminescence."""
    s_arr = np.array(sizes)
    ax.scatter(x, y, s=s_arr, c=colors, alpha=1.0, edgecolors='none', zorder=zorder)
    ax.scatter(x, y, s=s_arr*3, c=colors, alpha=0.5, edgecolors='none', zorder=zorder-1)
    ax.scatter(x, y, s=s_arr*12, c=colors, alpha=0.15, edgecolors='none', zorder=zorder-2)

def draw_bloom_line(ax, x, y, color, lw, alpha=1.0, zorder=5):
    """Glow for the architectural lattice."""
    ax.plot(x, y, color=color, lw=lw, alpha=alpha, zorder=zorder)
    ax.plot(x, y, color=color, lw=lw*3, alpha=alpha*0.3, zorder=zorder-1)

def ease_in_out(t):
    return t * t * (3.0 - 2.0 * t)

def rotate_3d(x, y, z, angle):
    xr = x * math.cos(angle) - z * math.sin(angle)
    zr = x * math.sin(angle) + z * math.cos(angle)
    return xr, y, zr

def project_iso(x, y, z, scale=180): # Scaled up massively to fill screen
    ang = 0.523598
    px = (x - z) * math.cos(ang) * scale
    py = (y - (x + z) * math.sin(ang)) * scale
    return px, py

def run():
    print(f"LOGIC GARDEN 130: ECSTASY OF CHAOS v2 ({TOTAL_FRAMES} frames)")
    
    # 1. BUILD "TRUE BEING" (The Target Geometry - 6x6x6 Grid)
    dims = np.linspace(-2.5, 2.5, 6)
    base_nodes = []
    for x in dims:
        for y in dims:
            for z in dims:
                base_nodes.append((x, y, z))
    base_nodes = np.array(base_nodes)
    N = len(base_nodes) # 216 Nodes
    
    # 2. BUILD "FRAGMENTATION" (The Chaotic Genesis)
    np.random.seed(42)
    phi = np.random.uniform(0, math.pi * 2, N)
    costheta = np.random.uniform(-1, 1, N)
    u = np.random.uniform(0, 1, N)
    theta = np.arccos(costheta)
    
    # Start spread out so there's no "blank" void
    r_initial = 150 * np.cbrt(u) 
    start_x = r_initial * np.sin(theta) * np.cos(phi)
    start_y = r_initial * np.sin(theta) * np.sin(phi)
    start_z = r_initial * np.cos(theta)
    
    # Slower, majestic explosion velocities
    vx = np.sin(theta) * np.cos(phi) * 8
    vy = np.sin(theta) * np.sin(phi) * 8
    vz = np.cos(theta) * 8
    velocities = np.column_stack((vx, vy, vz))
    
    # Absolute Neon Colors
    chaos_colors = [np.random.choice(NEON_PALETTE) for _ in range(N)]
    
    CX, CY = 540, 1000 # Center lower slightly for text
    
    # Timeline
    F_EXPLODE = 15        # Instant shattering
    F_HOLD_FAST = 400     # "Hold fast..."
    F_RESTORE_START = 550 # Pulling back to structure
    F_RESTORE_END = 800   # "True being" assembled
    
    current_3d = np.column_stack((start_x, start_y, start_z))
    
    for f in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        fig.patch.set_facecolor(C_VOID)
        ax.set_facecolor(C_VOID)
        
        ax.set_xlim(0, 1080)
        ax.set_ylim(0, 1920)
        
        status_text = ""
        status_color = C_TEXT
        base_angle = f * 0.010 # Slower rotation
        
        # --- PHYSICS ENGINE ---
        if f >= F_EXPLODE and f < F_RESTORE_START:
            # Slow application of velocity + organic wobble
            wobble = np.random.normal(0, 0.4, (N, 3))
            current_3d += velocities + wobble
            
            # Massive friction/damping keeps them on screen, drifting like a nebula
            velocities *= 0.985 
            
            if f >= F_HOLD_FAST:
                velocities *= 0.85 # Critical Damping locks them in place
            
        # --- RENDER LOGIC ---
        if f < F_EXPLODE:
            status_text = "The Immense Drugged Universe"
            # Unstable, vibrating core
            scale_pulse = math.sin(f * 2.0) * 15
            current_3d += np.random.normal(0, 2, (N, 3)) # Violent shaking
            
            x_vals = CX + current_3d[:, 0]
            y_vals = CY + current_3d[:, 1]
            c_vals = chaos_colors
            sizes = [40 + scale_pulse] * N
            draw_bloom_scatter(ax, x_vals, y_vals, sizes, c_vals)

        elif f < F_RESTORE_START:
            # The "Ecstasy of Chaos"
            if f < F_HOLD_FAST: status_text = "Explodes In Colour"
            else: status_text = "Hold Fast"
            status_color = C_ROYAL if f >= F_HOLD_FAST else C_TEXT
            
            if f >= F_HOLD_FAST:
                # The Bounding Box ignites
                p = min(1.0, (f - F_HOLD_FAST) / 60.0)
                ax.add_patch(plt.Rectangle((40, 300), 1000, 1400, fill=False, color=C_ROYAL, lw=10*p, alpha=p, zorder=2))
                ax.add_patch(plt.Rectangle((40, 300), 1000, 1400, fill=False, color=C_ROYAL, lw=30*p, alpha=p*0.3, zorder=1))

            x_vals = CX + current_3d[:, 0]
            y_vals = CY + current_3d[:, 1]
            sizes = [30] * N
            draw_bloom_scatter(ax, x_vals, y_vals, sizes, chaos_colors)

        else:
            # "Restores Fragmentation into True Being"
            p = min(1.0, (f - F_RESTORE_START) / (F_RESTORE_END - F_RESTORE_START))
            eased_p = ease_in_out(p)
            
            if p < 1.0: status_text = "Fragmentation Restores"
            else: status_text = "To Existence"
            status_color = C_TRUE_BEING if p == 1.0 else C_ROYAL
            
            x_vals, y_vals, c_vals = [], [], []
            
            # Rotate Target & Lerp
            for i in range(N):
                rx, ry, rz = rotate_3d(base_nodes[i, 0], base_nodes[i, 1], base_nodes[i, 2], base_angle)
                tx, ty = project_iso(rx, ry, rz, scale=180) # Massive Screen-filling scale
                tx += CX
                ty += CY
                
                cx_start = CX + current_3d[i, 0]
                cy_start = CY + current_3d[i, 1]
                
                x_vals.append(cx_start + (tx - cx_start) * eased_p)
                y_vals.append(cy_start + (ty - cy_start) * eased_p)
                
                # Morph Color: Neon -> Pure Gold
                if p < 1.0:
                    c_vals.append(C_TRUE_BEING if np.random.rand() < p else chaos_colors[i])
                else:
                    c_vals.append(C_TRUE_BEING)

            sizes = [30 + (10 * eased_p)] * N
            draw_bloom_scatter(ax, x_vals, y_vals, sizes, c_vals, zorder=10)
            
            # Draw Structural Lattice Edges (Golden Threads pulling everything together)
            if p > 0.2:
                edge_alpha = min(1.0, (p - 0.2) * 1.5)
                for i in range(N):
                    for j in range(i+1, N):
                        dist = np.linalg.norm(base_nodes[i] - base_nodes[j])
                        # In a 6x6 grid from -2.5 to 2.5, spacing is 1.0 exactly.
                        if abs(dist - 1.0) < 0.01:
                            draw_bloom_line(ax, [x_vals[i], x_vals[j]], [y_vals[i], y_vals[j]], 
                                            C_TRUE_BEING, lw=2 + (2*p), alpha=edge_alpha * 0.7, zorder=5)

            if p == 1.0:
                # Core Geometry Glow (The Heart of the System)
                ax.add_patch(plt.Circle((CX, CY), 450, color=C_TRUE_BEING, alpha=0.1, zorder=1))

        # UI OVERLAYS
        ax.text(540, 1820, "Ecstasy Of Chaos", color=C_TEXT, ha='center', fontsize=35, fontname='monospace', weight='bold')
        ax.text(540, 1760, status_text, color=status_color, ha='center', fontsize=22, fontname='monospace')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close(fig)

if __name__ == "__main__": run()
