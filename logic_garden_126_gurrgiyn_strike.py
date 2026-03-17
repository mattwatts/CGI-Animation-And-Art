"""
SOVEREIGN CODE: logic_garden_126_gurrgiyn_strike.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python High-Fidelity Simulator
SCENE: Logic Garden 126 (Gurrgiyn: The Strike)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
import os
import math

# CONFIG
FPS = 30
DURATION = 15
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_126_gurrgiyn_strike"
os.makedirs(OUT_DIR, exist_ok=True)

# THE GURRGIYN PALETTE
C_VOID = '#000000'            # Absolute Black
C_MANTIS = '#39FF14'          # Neon Retro Green
C_MANTIS_DARK = '#006400'     # Deep Forest Green (Shadows)
C_NILA_BINDU = '#002FA7'      # International Klein Blue
C_METADATA = '#8A2BE2'        # Violet (Ancestral Data)
C_ENTROPY = '#FF003C'         # Red (The Target)
C_ASSIMILATED = '#FFD700'     # Gold (Neutralized)

def draw_environment(ax, frame):
    """Draws the Macleay River sine waves (Time/Events) flowing vertically."""
    y_vals = np.linspace(0, 1920, 100)
    for i in range(4):
        offset = (frame * 15) + (i * 400)
        # Vertical sine waves
        x_vals_left = 150 + np.sin((y_vals + offset) / 100) * 50
        x_vals_right = 930 + np.sin((y_vals - offset) / 120) * 50
        
        ax.plot(x_vals_left, y_vals, color=C_MANTIS_DARK, lw=2, alpha=0.5, zorder=1)
        ax.plot(x_vals_right, y_vals, color=C_MANTIS_DARK, lw=2, alpha=0.5, zorder=1)

def draw_gurrgiyn(ax, strike_ext, target_pos, frame):
    """
    Constructs the Mantis using rigid geometric vectors.
    strike_ext represents the extension of the arms (0.0 to 1.0).
    """
    cx, cy = 540, 600  # Base of thorax
    head_y = 1100
    shoulder_y = 950
    
    # 1. The Nila Bindu (Pearl of conscious stillness)
    bindu_y = head_y + 120 + math.sin(frame * 0.1) * 10
    ax.add_patch(Circle((cx, bindu_y), 30, color=C_NILA_BINDU, zorder=5))
    ax.add_patch(Circle((cx, bindu_y), 50, color=C_NILA_BINDU, alpha=0.3, zorder=4))
    
    # 2. Thorax (Center Line)
    ax.plot([cx, cx], [cy, head_y], color=C_MANTIS, lw=12, zorder=3)
    
    # 3. Head (Inverted Triangle)
    head = Polygon([[cx-60, head_y+50], [cx+60, head_y+50], [cx, head_y-40]], 
                   closed=True, color=C_MANTIS, zorder=4)
    ax.add_patch(head)
    
    # Eyes
    ax.add_patch(Circle((cx-50, head_y+40), 15, color=C_VOID, zorder=5))
    ax.add_patch(Circle((cx+50, head_y+40), 15, color=C_VOID, zorder=5))

    # 4. Raptorial Arms (Kinematic Extension)
    # Right Arm
    r_shoulder = np.array([cx + 20, shoulder_y])
    r_elbow_idle = np.array([cx + 150, shoulder_y - 150])
    r_claw_idle = np.array([cx + 40, shoulder_y + 50])
    
    if strike_ext > 0:
        # Interpolate elbow and claw towards the target
        # Target logic: Arm reaches out to target_pos
        tx, ty = target_pos
        r_claw = r_claw_idle + (np.array([tx, ty]) - r_claw_idle) * strike_ext
        # Elbow swings out to maintain segment length visually
        r_elbow = r_elbow_idle + (np.array([cx + 300, ty - 100]) - r_elbow_idle) * strike_ext
    else:
        r_elbow = r_elbow_idle
        r_claw = r_claw_idle

    # Draw Right Arm
    ax.plot([r_shoulder[0], r_elbow[0]], [r_shoulder[1], r_elbow[1]], color=C_MANTIS, lw=10, zorder=6)
    ax.plot([r_elbow[0], r_claw[0]], [r_elbow[1], r_claw[1]], color=C_MANTIS, lw=8, zorder=6)
    
    # Left Arm (Idle, passive observer)
    l_shoulder = np.array([cx - 20, shoulder_y])
    l_elbow = np.array([cx - 150, shoulder_y - 150])
    l_claw = np.array([cx - 40, shoulder_y + 50])
    ax.plot([l_shoulder[0], l_elbow[0]], [l_shoulder[1], l_elbow[1]], color=C_MANTIS, lw=10, zorder=2)
    ax.plot([l_elbow[0], l_claw[0]], [l_elbow[1], l_claw[1]], color=C_MANTIS, lw=8, zorder=2)

def run():
    print(f"LOGIC GARDEN 126: GURRGIYN STRIKE ({TOTAL_FRAMES} frames)")
    
    # Timing
    F_ENTER = 60      # Target enters
    F_WAIT = 150      # Target drifts into range
    F_STRIKE = F_WAIT + 2   # 2-frame snap (Blindingly fast)
    F_RETRACT = F_STRIKE + 10 # Retract back to center
    
    for f in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        ax.set_facecolor(C_VOID)
        ax.set_xlim(0, 1080)
        ax.set_ylim(0, 1920)
        
        draw_environment(ax, f)
        
        # Determine Target State
        target_x = 1200
        target_y = 1050
        strike_ext = 0.0
        target_color = C_ENTROPY
        
        if f >= F_ENTER:
            # Target is drifting in
            drift_p = min(1.0, (f - F_ENTER) / (F_WAIT - F_ENTER))
            target_x = 1200 - (drift_p * 400) # Drifts to X=800
            target_y = 1050 + math.sin(f * 0.2) * 20
            
            if f >= F_WAIT and f <= F_STRIKE:
                # STRIKE FRAME (Arm fully extended)
                strike_ext = 1.0
                
            elif f > F_STRIKE and f <= F_RETRACT:
                # RETRACT FRAME (Pulling target to center)
                ret_p = (f - F_STRIKE) / (F_RETRACT - F_STRIKE)
                strike_ext = 1.0 - ret_p
                target_x = 800 - (ret_p * 220) # Pulled to X=580
                target_y = 1050 - (ret_p * 50) # Pulled down to chest
                
            elif f > F_RETRACT:
                # ASSIMILATED
                strike_ext = 0.0
                target_x = 580
                target_y = 1000
                target_color = C_ASSIMILATED # Phase transition to Gold
        
        # Render Target (if exists)
        if f >= F_ENTER:
            ax.add_patch(Circle((target_x, target_y), 20, color=target_color, zorder=7))
            if target_color == C_ASSIMILATED:
                ax.add_patch(Circle((target_x, target_y), 40, color=target_color, alpha=0.3, zorder=6))

        draw_gurrgiyn(ax, strike_ext, (target_x, target_y), f)
        
        # Flight Recorder UI
        ax.text(540, 1800, "Gurrgiyn Strikes", color=C_MANTIS, ha='center',
                fontsize=40, fontname='monospace', weight='bold')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
