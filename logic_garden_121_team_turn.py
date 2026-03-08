"""
SOVEREIGN CODE: logic_garden_121_team_turn.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: C64 VIC-II Emulation
SCENE: Logic Garden 121 (Boy+Dog: Right->Center->Right)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Ellipse, Wedge
import matplotlib.patheffects as pe
import os
import math

# CONFIG
FPS = 20
DURATION = 15
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_121_team_turn"
os.makedirs(OUT_DIR, exist_ok=True)

# C64 PALETTE
C64 = {
    'BLACK': '#000000', 'WHITE': '#FFFFFF', 'RED': '#880000', 'CYAN': '#AAFFEE',
    'PURPLE': '#CC44CC', 'GREEN': '#00CC55', 'BLUE': '#0000AA', 'YELLOW': '#EEEE77',
    'ORANGE': '#DD8855', 'BROWN': '#664400', 'LIGHTRED': '#FF7777', 
    'GREY': '#777777', 'LIGHTGREY': '#BBBBBB'
}

def draw_dog(ax, x, y, scale, phase, facing='left'):
    # Dog (Yellow)
    FUR = C64['YELLOW']
    EAR = C64['BROWN']
    
    d = -1.0 if facing == 'left' else 1.0 # Default Right
    
    is_moving = phase > 0
    wag = math.sin(phase * 4 * math.pi) * 15 if is_moving else math.sin(x*0.1)*5
    bob = abs(math.sin(phase * 4 * math.pi)) * 2 if is_moving else 0
    
    body_w = 50 * scale
    body_h = 25 * scale
    
    # Center X is Pivot
    # If facing Left (d=-1): Head at X + (d*w/2) -> X - w/2. Tail at X - (d*w/2) -> X + w/2
    # Correct logic:
    # Front = X + (d * body_w/2)
    # Back = X - (d * body_w/2)
    
    cx = x
    x_front = cx + (d * body_w/2)
    x_back = cx - (d * body_w/2)
    
    ax.add_patch(Rectangle((cx - body_w/2, y), body_w, body_h, color=FUR))
    
    # Tail (At Back)
    tail_tip = x_back - (d * 15 * scale)
    ax.plot([x_back, tail_tip], [y + 20*scale, y + 30*scale + wag], color=FUR, linewidth=4*scale)
    
    # Head (At Front)
    head_x = x_front
    head_y = y + 25*scale
    ax.add_patch(Circle((head_x, head_y + bob), 15*scale, color=FUR))
    
    # Ear
    ear_x = head_x - (d * 5 * scale)
    ax.add_patch(Ellipse((ear_x, head_y + bob + 5*scale), 10*scale, 18*scale, color=EAR))
    
    # Snout
    snout_w = 12*scale
    snout_draw_x = head_x if d==1 else (head_x - snout_w)
    ax.add_patch(Rectangle((snout_draw_x, head_y + bob - 5*scale), snout_w, 10*scale, color=FUR))
    
    # Legs (simplified)
    leg_len = 20*scale
    def leg(ax, ox, oy, ph, col):
        ang = math.sin(ph * 2 * math.pi) if is_moving else 0
        kx = ox + (math.sin(ang)*10*scale*d)
        ky = oy - leg_len
        ax.plot([ox, kx], [oy, ky], color=col, linewidth=5*scale)
        
    leg(ax, x_back, y, phase, C64['ORANGE'])
    leg(ax, x_front, y, phase + 0.5, C64['ORANGE'])
    leg(ax, x_back, y, phase + 0.5, FUR)
    leg(ax, x_front, y, phase, FUR)

def draw_boy(ax, x, y, scale, phase, facing='left'):
    # Boy (Cyan/Red)
    SHIRT = C64['CYAN']
    SHORTS = C64['RED']
    SKIN = C64['LIGHTRED']
    
    d = -1.0 if facing == 'left' else 1.0
    
    is_moving = phase > 0
    bob = abs(math.sin(phase * 2 * math.pi)) * 5 * scale if is_moving else math.sin(x*0.1)*2
    
    w = 20 * scale
    cx = x
    
    # Body
    ax.add_patch(Rectangle((cx - w/2, y + 25*scale + bob), w, 25*scale, color=SHIRT))
    ax.add_patch(Rectangle((cx - w/2, y + 15*scale + bob), w, 10*scale, color=SHORTS))
    
    # Head
    ax.add_patch(Circle((cx, y + 55*scale + bob), 12*scale, color=SKIN))
    # Hair Cap
    ax.add_patch(Wedge((cx, y + 58*scale + bob), 14*scale, 0, 180, color=C64['BROWN']))
    
    # Legs
    swing = math.sin(phase * 2 * math.pi) if is_moving else 0
    
    # Far Leg
    fl_x = cx - (d * math.sin(-swing*0.5) * 15 * scale)
    ax.plot([cx, fl_x], [y+20*scale+bob, y], color=SKIN, linewidth=6*scale)
    
    # Near Leg
    nl_x = cx - (d * math.sin(swing*0.5) * 15 * scale)
    ax.plot([cx, nl_x], [y+20*scale+bob, y], color=SKIN, linewidth=6*scale)

def run():
    print(f"LOGIC GARDEN 121: TEAM TURN ({TOTAL_FRAMES} frames)")
    scale = 3.5
    
    sx, sy, sw, sh = 50, 600, 980, 720
    
    f_in = 100
    f_pause = 60
    f_out = 140
    
    # Spacing: Dog is 60px "Ahead" relative to facing.
    # Moving Left: Dog X < Boy X
    # Moving Right: Dog X > Boy X
    
    start_x_b = sx + sw + 150
    center_x = sx + sw/2
    
    for f in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        ax.set_facecolor(C64['BLACK'])
        ax.add_patch(Rectangle((sx, sy), sw, sh, color=C64['BLACK']))
        floor_y = sy + 250
        ax.axhline(floor_y, color=C64['WHITE'], linewidth=4)
        
        boy_x = 0
        dog_x = 0
        facing = 'left'
        phase = 0
        caption = ""
        
        if f < f_in:
            # IN (Left)
            p = 1 - (1 - f/f_in)**2
            boy_x = start_x_b - (p * (start_x_b - center_x))
            dog_x = boy_x - (60 * scale)
            facing = 'left'
            phase = f / 18.0
            
        elif f < f_in + f_pause:
            # PAUSE
            boy_x = center_x
            dog_x = boy_x - (60 * scale) # Keep formation
            facing = 'left'
            phase = 0
            if f > f_in + 15: caption = "??"
            
        else:
            # OUT (Right)
            # When turning right, Dog should be AHEAD (Right of Boy).
            # So Dog transitions from (Boy - 60) to (Boy + 60)?
            # Or they just turn in place? 
            # If they turn in place, Dog is BEHIND Boy walking back.
            # Let's do a "Formation Shift" or just Turn in Place (Dog follows).
            # Turn in place is funnier. Dog led the way in, now follows Boy out.
            
            t = (f - (f_in + f_pause)) / f_out
            p = t * t
            if p > 1: p = 1
            
            boy_x = center_x + (p * (start_x_b - center_x))
            # Dog follows Boy now (Behind)
            # Position = BoyX - (60 * scale) still? 
            # If facing Right, Behind is X - 60. 
            # So relative pos stays same!
            
            dog_x = boy_x - (60 * scale)
            
            facing = 'right'
            phase = f / 18.0
            caption = "LOGIC GARDEN 121"

        draw_boy(ax, boy_x, floor_y + 35, scale, phase, facing)
        draw_dog(ax, dog_x, floor_y + 20, scale, phase, facing)
        
        if caption:
            ax.text(540, 1500, caption, color=C64['WHITE'], ha='center',
                    fontsize=40, fontname='monospace', weight='bold')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
