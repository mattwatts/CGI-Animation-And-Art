"""
SOVEREIGN CODE: logic_garden_122_team_refusal.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: C64 VIC-II Emulation
SCENE: Logic Garden 122 (Boy+Dog: Left->Center->Left)
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
OUT_DIR = "frames_122_team_refusal"
os.makedirs(OUT_DIR, exist_ok=True)

# C64 PALETTE
C64 = {
    'BLACK': '#000000', 'WHITE': '#FFFFFF', 'RED': '#880000', 'CYAN': '#AAFFEE',
    'PURPLE': '#CC44CC', 'GREEN': '#00CC55', 'BLUE': '#0000AA', 'YELLOW': '#EEEE77',
    'ORANGE': '#DD8855', 'BROWN': '#664400', 'LIGHTRED': '#FF7777', 
    'GREY': '#777777', 'LIGHTGREY': '#BBBBBB'
}

def draw_dog(ax, x, y, scale, phase, facing='right'):
    FUR = C64['YELLOW']
    EAR = C64['BROWN']
    SHADOW = C64['ORANGE']
    
    d = 1.0 if facing == 'right' else -1.0
    
    is_moving = phase > 0
    if is_moving:
        wag = math.sin(phase * 4 * math.pi) * 15
        bob = abs(math.sin(phase * 4 * math.pi)) * 2
    else:
        wag = math.sin(x*0.1) * 5
        bob = 0

    body_w = 50 * scale
    
    # Position Logic: x is Center Mass
    cx = x
    
    # Body
    ax.add_patch(Rectangle((cx - body_w/2, y), body_w, 25*scale, color=FUR))
    
    # Tail (Back)
    x_back = cx - (d * body_w/2)
    tail_tip = x_back - (d * 15 * scale)
    ax.plot([x_back, tail_tip], [y + 20*scale, y + 30*scale + wag], color=FUR, linewidth=4*scale)
    
    # Head (Front)
    x_front = cx + (d * body_w/2)
    head_y = y + 25*scale
    ax.add_patch(Circle((x_front, head_y + bob), 15*scale, color=FUR))
    
    # Ear
    ear_x = x_front - (d * 5 * scale)
    ax.add_patch(Ellipse((ear_x, head_y + bob + 5*scale), 10*scale, 18*scale, color=EAR))
    
    # Snout
    snout_draw_x = x_front if d==1 else (x_front - 12*scale)
    ax.add_patch(Rectangle((snout_draw_x, head_y + bob - 5*scale), 12*scale, 10*scale, color=FUR))
    
    # Legs
    def leg(ox, oy, ph, col):
        ang = math.sin(ph * 2 * math.pi) if is_moving else 0
        kx = ox + (math.sin(ang)*10*scale*d)
        ky = oy - 20*scale
        ax.plot([ox, kx], [oy, ky], color=col, linewidth=5*scale)
        
    leg(x_back, y, phase, SHADOW)
    leg(x_front, y, phase + 0.5, SHADOW)
    leg(x_back, y, phase + 0.5, FUR)
    leg(x_front, y, phase, FUR)

def draw_boy(ax, x, y, scale, phase, facing='right'):
    SHIRT = C64['CYAN']
    SHORTS = C64['RED']
    SKIN = C64['LIGHTRED']
    
    d = 1.0 if facing == 'right' else -1.0
    
    is_moving = phase > 0
    bob = abs(math.sin(phase * 2 * math.pi)) * 5 * scale if is_moving else math.sin(x*0.1)*2
    
    w = 20 * scale
    cx = x
    
    # Torso
    ax.add_patch(Rectangle((cx - w/2, y + 25*scale + bob), w, 25*scale, color=SHIRT))
    ax.add_patch(Rectangle((cx - w/2, y + 15*scale + bob), w, 10*scale, color=SHORTS))
    
    # Head
    ax.add_patch(Circle((cx, y + 55*scale + bob), 12*scale, color=SKIN))
    ax.add_patch(Wedge((cx, y + 58*scale + bob), 14*scale, 0, 180, color=C64['BROWN']))
    
    # Legs
    swing = math.sin(phase * 2 * math.pi) if is_moving else 0
    
    fl_x = cx - (d * math.sin(-swing*0.5) * 15 * scale)
    nl_x = cx - (d * math.sin(swing*0.5) * 15 * scale)
    
    ax.plot([cx, fl_x], [y+20*scale+bob, y], color=SKIN, linewidth=6*scale)
    ax.plot([cx, nl_x], [y+20*scale+bob, y], color=SKIN, linewidth=6*scale)

def run():
    print(f"LOGIC GARDEN 122: TEAM REFUSAL ({TOTAL_FRAMES} frames)")
    scale = 3.5
    
    sx, sy, sw, sh = 50, 600, 980, 720
    
    f_in = 100
    f_pause = 60
    f_out = 140
    
    # Formation: Dog is 60px "ahead" of Boy
    # If facing Right: Dog X = Boy X + 60
    
    start_x_boy = sx - 100
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
        facing = 'right'
        phase = 0
        caption = ""
        
        if f < f_in:
            # IN (Rightward)
            p = 1 - (1 - f/f_in)**2
            boy_x = start_x_boy + (p * (center_x - start_x_boy))
            dog_x = boy_x + (60 * scale) # Lead
            facing = 'right'
            phase = f / 18.0
            
        elif f < f_in + f_pause:
            # PAUSE
            boy_x = center_x
            dog_x = boy_x + (60 * scale)
            facing = 'right'
            phase = 0
            if f > f_in + 15: caption = "??"
        
        else:
            # OUT (Leftward)
            # Turn in place.
            # Boy at `center_x`. Facing Left.
            # Dog at `center_x + 60`. Facing Left.
            # Since walking Left (negative X), Dog is "Behind" Boy. 
            # (Boy is leftmost entity).
            
            t = (f - (f_in + f_pause)) / f_out
            p = t * t
            if p > 1: p = 1
            
            boy_x = center_x - (p * (center_x - start_x_boy))
            dog_x = boy_x + (60 * scale) # Maintained relative distance
            
            facing = 'left'
            phase = f / 18.0
            caption = "LOGIC GARDEN 122"

        draw_boy(ax, boy_x, floor_y + 35, scale, phase, facing)
        draw_dog(ax, dog_x, floor_y + 20, scale, phase, facing)
        
        if caption:
            ax.text(540, 1500, caption, color=C64['WHITE'], ha='center',
                    fontsize=40, fontname='monospace', weight='bold')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
