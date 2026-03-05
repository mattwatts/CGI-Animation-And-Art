"""
SOVEREIGN CODE: logic_garden_102_dampener_v2.py
FORMAT: YouTube Shorts (1080x1920)
SCENE: The Dampener (Syntax Patched)
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

# CONFIG
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_102_dampener_v2"
os.makedirs(OUT_DIR, exist_ok=True)

# RESOLUTION
RES_W = 1080
RES_H = 1920

# PALETTE
C_BG    = '#050510'
C_MASS  = '#FF3333' # High Energy Red
C_PISTON= '#00FFFF' # Logic Cyan
C_GOLD  = '#FFD700' # Zen Gold
C_SPRING= '#CCCCCC' 
C_TRACE = '#FF3333' # Graph Line

class Oscillator:
    def __init__(self):
        self.y = 600.0   # Start high (Displaced)
        self.vy = 0.0
        self.mass = 50.0
        self.k = 10.0    # Spring Constant
        self.c = 0.0     # Damping Coefficient (Starts at 0)
        self.target_c = 0.0
        
        self.history = [] # For graph
        
    def update(self, dt):
        # 1. Spring Force (Hooke's Law): F = -ky
        f_spring = -self.k * self.y
        
        # 2. Damping Force: F = -cv
        # Smoothly ramp c to target
        self.c += (self.target_c - self.c) * 0.1
        f_damp = -self.c * self.vy
        
        # 3. Integration
        acc = (f_spring + f_damp) / self.mass
        self.vy += acc * dt
        self.y += self.vy * dt
        
        # Store for graph
        self.history.append(self.y)
        if len(self.history) > 300: self.history.pop(0)

def draw_spring(ax, start_y, end_y, x=0, width=100, coils=10):
    """ Procedural ZigZag Spring """
    step = (start_y - end_y) / coils
    pts = []
    pts.append([x, start_y])
    for i in range(coils):
        y_top = start_y - (i * step)
        y_btm = start_y - ((i+1) * step)
        mid_y = (y_top + y_btm) / 2
        
        # Left/Right zig zag
        pts.append([x + width/2, mid_y])
        pts.append([x - width/2, y_btm])
        
    # Correct alignment
    pts[-1] = [x, end_y]
    
    px = [p[0] for p in pts]
    py = [p[1] for p in pts]
    # FIX: solid_capstyle instead of capstyle
    ax.plot(px, py, color=C_SPRING, linewidth=6, solid_capstyle='round')

def run():
    print(f"LOGIC GARDEN 102: THE DAMPENER V2 ({TOTAL_FRAMES} frames)")
    
    sys = Oscillator()
    
    # Calculate Critical Damping: c = 2 * sqrt(m * k)
    CRITICAL_DAMPING = 2.0 * math.sqrt(sys.mass * sys.k)
    
    for f in range(TOTAL_FRAMES):
        
        # --- LOGIC TIMELINE ---
        
        # 0-5s: CHAOS (No Damping)
        if f < 150:
            sys.target_c = 0.0
            # Inject energy to sustain chaos
            if abs(sys.y) < 100 and abs(sys.vy) < 10:
                sys.vy += 30.0 
        
        # 5s: INTERVENTION
        elif f == 150:
            pass # Event 
            
        # 5-20s: DAMPING (Transition to Zen)
        elif f > 150:
            sys.target_c = CRITICAL_DAMPING * 1.5 
            
        # --- PHYSICS ---
        for _ in range(5):
             sys.update(0.2)
             
        # --- RENDER ---
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        # Limits
        ax.set_xlim(-540, 540)
        ax.set_ylim(-960, 960)
        ax.set_facecolor(C_BG)
        
        # 1. REFERENCE LINE
        ax.axhline(0, color='#222233', linewidth=4, linestyle='--')
        
        # 2. DRAW SPRING
        ceil_y = 800
        mass_y = sys.y
        draw_spring(ax, ceil_y, mass_y + 80, x=0, width=120, coils=12)
        
        # 3. DRAW DASHPOT
        if f > 150:
            floor_y = -800
            house_h = 600
            
            # Draw Housing
            rect = Rectangle((-80, floor_y), 160, house_h, 
                             edgecolor=C_PISTON, facecolor='none', linewidth=5)
            ax.add_patch(rect)
            
            # Piston Rod
            rod_len = (mass_y - 80) - (floor_y + 100)
            ax.plot([0, 0], [mass_y - 80, mass_y - 80 - rod_len], 
                    color=C_PISTON, linewidth=15, alpha=0.8)
            
            # Piston Head
            head_y = mass_y - 80 - rod_len
            rect_head = Rectangle((-70, head_y-20), 140, 40, color=C_PISTON)
            ax.add_patch(rect_head)
            
            # Resistance Glow
            glow_a = min(1.0, abs(sys.vy) / 20.0)
            if glow_a > 0.1:
                circ = Circle((0, head_y), 100, color=C_PISTON, alpha=glow_a*0.3)
                ax.add_patch(circ)

        # 4. DRAW MASS
        c_ball = C_MASS
        if f > 150:
            err = abs(sys.y) + abs(sys.vy)
            if err < 10: c_ball = C_GOLD
            elif err < 100: c_ball = C_PISTON 
            
        c = Circle((0, mass_y), 80, color=c_ball, zorder=10)
        ax.add_patch(c)
        c2 = Circle((20, mass_y+20), 20, color='white', alpha=0.9, zorder=11)
        ax.add_patch(c2)

        # 5. TRACE GRAPH
        # Map history to X coords (Right to Left)
        if len(sys.history) > 1:
            hx = []
            hy = []
            for i, val in enumerate(reversed(sys.history)):
                hx.append(400 - (i * 3))
                hy.append(val)
                
            line_col = C_TRACE
            if f > 200: line_col = C_GOLD
            elif f > 150: line_col = C_PISTON
            
            ax.plot(hx, hy, color=line_col, linewidth=4, alpha=0.5)
            ax.fill_between(hx, hy, 0, color=line_col, alpha=0.1)

        # 6. UI
        stroke = [pe.withStroke(linewidth=4, foreground="black")]
        
        # Ceil Mount
        rect = Rectangle((-200, 800), 400, 40, color='#333344')
        ax.add_patch(rect)
        
        # Labels
        if f < 150:
            ax.text(0, 850, "UNDAMPED SYSTEM", color=C_MASS, ha='center', 
                    fontsize=30, fontname='monospace', weight='bold', path_effects=stroke)
            ax.text(0, -900, "HIGH ENTROPY", color=C_MASS, ha='center', 
                    fontsize=25, fontname='monospace', path_effects=stroke)
            
        elif f == 150:
            ax.text(0, 0, "ENGAGE LOGIC", color='white', ha='center', 
                    fontsize=50, fontname='monospace', weight='bold', path_effects=stroke)
            
        else:
            if abs(sys.y) < 5:
                ax.text(0, 850, "CRITICALLY DAMPED", color=C_GOLD, ha='center', 
                        fontsize=30, fontname='monospace', weight='bold', path_effects=stroke)
                ax.text(0, -900, "STATE: ZEN", color=C_GOLD, ha='center', 
                        fontsize=40, fontname='monospace', weight='bold', path_effects=stroke)
            else:
                 ax.text(0, 850, "CRITICALLY DAMPED", color=C_PISTON, ha='center', 
                        fontsize=30, fontname='monospace', weight='bold', path_effects=stroke)
                 ax.text(0, -900, "ABSORBING ENERGY...", color=C_PISTON, ha='center', 
                        fontsize=25, fontname='monospace', path_effects=stroke)

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
