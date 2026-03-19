"""
SOVEREIGN CODE: logic_garden_132_amor_fati.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python High-Fidelity Simulator
SCENE: Logic Garden 132 (Amor Fati / The Modular Envelope)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle
import math
import os

# CONFIG
FPS = 30
DURATION = 30
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_132_emergence"
os.makedirs(OUT_DIR, exist_ok=True)

# THE INDUSTRIAL / ANCESTRAL PALETTE
C_VOID = '#020205'           # Absolute Vacuum
C_NILA = '#002FA7'           # International Klein Blue (The Deep Core)
C_MANTIS = '#39FF14'         # Resonance / Gurrgiyn
C_CYAN = '#00FFCC'           # Mid-Band Friction
C_RED = '#FF003C'            # High-Band Friction / Frontier Blood
C_GOLD = '#FFD700'           # The Perimeter Bounding Box
C_TEXT = '#FFFFFF'           # Telemetry

def get_color_by_length(dist, max_dist):
    """
    Maps the length of the historical vector to a specific energy level.
    Short chords = Red (Violence, fast local friction)
    Mid chords = Cyan/Mantis (Nature, fluid flow)
    Long chords (passing through center) = Nila Bindu (Deep stillness)
    """
    ratio = dist / max_dist
    if ratio > 0.85: return C_NILA
    elif ratio > 0.5: return C_CYAN
    elif ratio > 0.2: return C_MANTIS
    else: return C_RED

def ease_in_out(t):
    # Smooth S-curve for the phase multiplier
    t /= 1.0
    return -0.5 * (math.cos(math.pi * t) - 1)

def run():
    print(f"LOGIC GARDEN 132: AMOR FATI [THE ENVELOPE] ({TOTAL_FRAMES} frames)")
    
    # 1. COMPILE-TIME GEOMETRY
    N = 400  # Number of nodes on the Bounding Box
    CX, CY = 540, 960
    R = 480  # Full width of the 1080p frame minus padding
    max_dist = 2 * R
    
    # The Nodes (Tethered to the perimeter)
    base_angles = np.linspace(0, 2*np.pi, N, endpoint=False)
    
    # Timeline
    F_SWEEP = 750 # Frames spent sweeping through chaos (0 to 25s)
    F_LOCK = 900  # Frames locked in pure Zen structure (25s to 30s)
    
    # The Multiplier dictates the topology. 
    # M=2 is a Cardioid. 
    # M=51 is a 50-petal lotus. 
    M_START = 2.0
    M_END = 51.0 
    
    for f in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        fig.patch.set_facecolor(C_VOID)
        ax.set_facecolor(C_VOID)
        
        ax.set_xlim(0, 1080)
        ax.set_ylim(0, 1920)
        
        # --- PHASE KINETICS ---
        if f <= F_SWEEP:
            # Sweeping through the decimal multipliers creates continuous topological evolution
            p = f / F_SWEEP
            eased_p = ease_in_out(p)
            M = M_START + (M_END - M_START) * eased_p
            rot_offset = f * 0.005 # Slow macro spin
            status_color = C_CYAN
        else:
            # Protocol: COMPILE-TIME SAFETY. Lock exactly on M=51.0 for the Perfect Lotus.
            M = M_END
            # Accelerate rotation once the structure is achieved
            rot_offset = (F_SWEEP * 0.005) + ((f - F_SWEEP) * 0.015)
            status_color = C_GOLD

        # --- THE ALGORITHM ---
        # Instead of arrays, calculate endpoints natively via the Angles
        # Point A = theta. Point B = theta * Multiplier.
        t_start = base_angles + rot_offset
        t_end = (base_angles * M) + rot_offset
        
        start_x = CX + R * np.cos(t_start)
        start_y = CY + R * np.sin(t_start)
        end_x = CX + R * np.cos(t_end)
        end_y = CY + R * np.sin(t_end)
        
        # Build the Line Vectors
        segments = []
        colors = []
        
        # Vector lengths for color grading
        dists = np.hypot(end_x - start_x, end_y - start_y)
        
        for i in range(N):
            segments.append([(start_x[i], start_y[i]), (end_x[i], end_y[i])])
            colors.append(get_color_by_length(dists[i], max_dist))

        # --- RENDERING (PROTOCOL: NEON POP) ---
        # The Bounding Box
        ax.add_patch(Circle((CX, CY), R, fill=False, color=C_GOLD, lw=2, alpha=0.9, zorder=5))
        ax.add_patch(Circle((CX, CY), R, fill=False, color=C_GOLD, lw=8, alpha=0.3, zorder=4))
        
        # The Nila Bindu (The Observer at Ground Zero)
        ax.add_patch(Circle((CX, CY), 8, color=C_NILA, zorder=10))
        
        # Pass 1: Core Lines (Bright, thin)
        lc1 = LineCollection(segments, colors=colors, linewidths=0.6, alpha=0.7, zorder=2)
        # Pass 2: Bloom (Soft, thick) - The cumulative overlapping of these creates the "curves"
        lc2 = LineCollection(segments, colors=colors, linewidths=2.5, alpha=0.12, zorder=1)
        
        ax.add_collection(lc1)
        ax.add_collection(lc2)

        # --- UI OVERLAYS (TELEMETRY) ---
        ax.text(540, 1850, "Emergence", color=C_TEXT, ha='center', fontsize=35, fontname='monospace', weight='bold')
        ax.text(540, 1800, "Amor Fati - Emergent Envolope", color=status_color, ha='center', fontsize=20, fontname='monospace', weight='bold')
        
        # Mathematical Proof HUD
        hud_y = 120
        status_text = "Sweeping" if f <= F_SWEEP else "Optimal"
        ax.text(80, hud_y + 40, "Rules:", color=C_TEXT, fontsize=18, fontname='monospace')
        ax.text(80, hud_y + 10, "No Curves", color=C_RED, fontsize=20, fontname='monospace', weight='bold')
        ax.text(80, hud_y - 20, "Fluidity born of friction", color=C_CYAN, fontsize=20, fontname='monospace', weight='bold')
        
        ax.text(1000, hud_y + 10, f"M : {M:06.3f}", color=status_color, ha='right', fontsize=24, fontname='monospace', weight='bold')
        ax.text(1000, hud_y - 20, f"{status_text}", color=status_color, ha='right', fontsize=18, fontname='monospace')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close(fig)

if __name__ == "__main__": run()
