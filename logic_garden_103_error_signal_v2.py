"""
SOVEREIGN CODE: logic_garden_103_error_signal_v2.py
FORMAT: YouTube Shorts (1080x1920)
SCENE: The Error Signal (Syntax Patched)
SYSTEM: Pure Python
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import matplotlib.patheffects as pe
import os
import math
import random 

# CONFIG
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_103_error_v2"
os.makedirs(OUT_DIR, exist_ok=True)

# RESOLUTION
RES_W = 1080
RES_H = 1920

# PALETTE
C_BG     = '#050510'
C_NODE   = '#00FFFF'     # The Agent (Cyan)
C_TARGET = '#FFD700'     # The Truth (Gold)
C_MISS   = '#333344'     # Where it went wrong
C_ERROR  = '#FF0044'     # The Signal (Red)
C_BEAM   = '#00FFFF'
C_GRID   = '#111122'

class Agent:
    def __init__(self):
        self.pos = np.array([0.0, -600.0])
        self.angle = math.radians(75) # Initial bad angle
        
    def fire_vector(self, length=1200):
        dx = math.cos(self.angle) * length
        dy = math.sin(self.angle) * length
        return np.array([self.pos[0] + dx, self.pos[1] + dy])

def run():
    print(f"LOGIC GARDEN 103: THE ERROR SIGNAL V2 ({TOTAL_FRAMES} frames)")
    
    agent = Agent()
    target_pos = np.array([0.0, 600.0])
    
    for f in range(TOTAL_FRAMES):
        
        # --- STATE MACHINE ---
        PHASE = "PREDICTION"
        if f > 60: PHASE = "BACKPROP"
        if f > 180: PHASE = "OPTIMIZATION" 
        if f > 240: PHASE = "CONVERGENCE"
        
        # LOGIC
        # Interpolate Angle during Optimization
        if PHASE == "OPTIMIZATION":
            # Smooth ease-in-out
            t = (f - 180) / 60.0 
            if t > 1: t = 1
            t = t * t * (3 - 2 * t)
            
            start_a = math.radians(75)
            end_a = math.radians(90)
            agent.angle = start_a + (end_a - start_a) * t
            
        elif PHASE == "CONVERGENCE":
            agent.angle = math.radians(90)
            
        current_tip = agent.fire_vector(1400)

        # --- RENDER ---
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        ax.set_xlim(-540, 540)
        ax.set_ylim(-960, 960)
        ax.set_facecolor(C_BG)
        
        # 1. GRID
        for i in range(-500, 600, 200):
            ax.axvline(i, color=C_GRID, linewidth=2)
            ax.axhline(i, color=C_GRID, linewidth=2)
            
        # 2. TARGET
        tgt_sz = 80 + math.sin(f*0.1)*5
        c_tgt = Circle((target_pos[0], target_pos[1]), tgt_sz, color=C_TARGET, zorder=10)
        ax.add_patch(c_tgt)
        c_glow = Circle((target_pos[0], target_pos[1]), tgt_sz*2, color=C_TARGET, alpha=0.2, zorder=9)
        ax.add_patch(c_glow)
        
        # 3. BEAM / ERROR LOGIC
        miss_x_final = 0
        miss_y_final = 0
        
        if PHASE == "PREDICTION" or PHASE == "BACKPROP":
            # Draw Miss Beam
            ax.plot([agent.pos[0], current_tip[0]], [agent.pos[1], current_tip[1]], 
                    color=C_BEAM, linewidth=4, alpha=0.5, linestyle='--')
            
            # Simple Trig for Miss Point at Target Height
            # tan(theta) = dy / dx -> dx = dy / tan(theta)
            # relative angle
            dy = target_pos[1] - agent.pos[1] 
            dx = dy / math.tan(agent.angle)
            
            miss_pos = np.array([agent.pos[0] + dx, target_pos[1]])
            miss_x_final = miss_pos[0]
            miss_y_final = miss_pos[1]
            
            # Miss Marker
            ax.scatter(miss_pos[0], miss_pos[1], s=200, marker='x', color=C_ERROR, zorder=15, linewidth=4)
            ax.text(miss_pos[0]+50, miss_pos[1], "PREDICTION", color=C_BEAM, fontsize=20, fontname='monospace')
            
            if PHASE == "BACKPROP":
                # Draw Error Vector
                ax.plot([miss_pos[0], target_pos[0]], [miss_pos[1], target_pos[1]], 
                        color=C_ERROR, linewidth=6)
                
                # Signal Packet traveling BACK
                travel_t = (f - 60) / 60.0 
                if travel_t > 1: travel_t = 1
                
                # Lerp from Miss -> Agent
                sig_pos = miss_pos + (agent.pos - miss_pos) * travel_t
                
                c_sig = Circle((sig_pos[0], sig_pos[1]), 40, color=C_ERROR, zorder=20)
                ax.add_patch(c_sig)
                
                # Only show text if packet is visible
                if travel_t < 0.9:
                    ax.text(sig_pos[0]+60, sig_pos[1], "ERROR SIGNAL", color=C_ERROR, fontsize=25, fontname='monospace', weight='bold')

        elif PHASE == "OPTIMIZATION":
            # Rotating Beam
            ax.plot([agent.pos[0], current_tip[0]], [agent.pos[1], current_tip[1]], 
                    color=C_BEAM, linewidth=4, alpha=0.8)
            
            # Gear Visual around agent
            gear_sz = 160
            rect = Rectangle((agent.pos[0]-gear_sz/2, agent.pos[1]-gear_sz/2), gear_sz, gear_sz, 
                             fill=False, edgecolor=C_NODE, linewidth=3, linestyle='--')
            
            # Use matplotlib transform to rotate
            t = matplotlib.transforms.Affine2D().rotate_deg_around(agent.pos[0], agent.pos[1], f*5) + ax.transData
            rect.set_transform(t)
            ax.add_patch(rect)
            
            ax.text(0, -400, "RE-WEIGHTING...", color=C_NODE, ha='center', fontsize=30, fontname='monospace')

        elif PHASE == "CONVERGENCE":
            # Solid HIT Beam
            ax.plot([agent.pos[0], target_pos[0]], [agent.pos[1], target_pos[1]], 
                    color=C_TARGET, linewidth=8, alpha=0.9)
            
            # Particles
            for i in range(12):
                px = target_pos[0] + random.uniform(-100, 100)
                py = target_pos[1] + random.uniform(-100, 100)
                ax.scatter(px, py, c=C_TARGET, s=random.uniform(20, 60), zorder=20)
                
        # 4. DRAW AGENT
        c_ag = Circle((agent.pos[0], agent.pos[1]), 60, color=C_NODE, zorder=10)
        ax.add_patch(c_ag)
        
        # 5. UI
        stroke = [pe.withStroke(linewidth=4, foreground="black")]
        
        ax.text(0, 800, "OBJECTIVE FUNCTION", color=C_TARGET, ha='center', fontsize=20, fontname='monospace', path_effects=stroke)
        
        txt_col = C_MISS
        label_txt = "STATE: NAIVE"
        
        if PHASE == "BACKPROP": 
             label_txt = "READING LOGS"
             txt_col = C_ERROR
        if PHASE == "OPTIMIZATION":
             label_txt = "ADJUSTING WEIGHTS"
             txt_col = C_NODE
        if PHASE == "CONVERGENCE":
             label_txt = "COMPILE-TIME SAFETY"
             txt_col = C_TARGET

        ax.text(0, -850, label_txt, color=txt_col, ha='center', fontsize=35, fontname='monospace', weight='bold', path_effects=stroke)

        if f > 70 and f < 120:
             ax.text(0, 0, "PAIN IS DATA", color=C_ERROR, ha='center', fontsize=50, fontname='monospace', weight='bold', path_effects=stroke)

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
