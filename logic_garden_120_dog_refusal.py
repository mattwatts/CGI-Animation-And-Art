"""
SOVEREIGN CODE: logic_garden_120_dog_refusal.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: C64 VIC-II Emulation
SCENE: Logic Garden 120 (Dog: Left->Center->Left)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Ellipse
import matplotlib.patheffects as pe
import os
import math

# CONFIG
FPS = 20
DURATION = 15
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_120_dog_refusal"
os.makedirs(OUT_DIR, exist_ok=True)

# C64 PALETTE
C64 = {
    'BLACK': '#000000', 'WHITE': '#FFFFFF', 'RED': '#880000', 'CYAN': '#AAFFEE',
    'PURPLE': '#CC44CC', 'GREEN': '#00CC55', 'BLUE': '#0000AA', 'YELLOW': '#EEEE77',
    'ORANGE': '#DD8855', 'BROWN': '#664400', 'LIGHTRED': '#FF7777', 'DARKGREY': '#333333',
    'GREY': '#777777', 'LIGHTGREEN': '#AAFF66', 'LIGHTBLUE': '#0088FF', 'LIGHTGREY': '#BBBBBB'
}

def draw_dog(ax, x, y, scale, phase, facing='right'):
    """
    Draws dog facing 'left' or 'right'.
    Reuse of Sovereign Dog Asset from LG-119.
    """
    FUR = C64['YELLOW']
    EAR = C64['BROWN']
    NOSE = C64['BLACK']
    COLLAR = C64['RED']
    SHADOW = C64['ORANGE']
    
    d = 1.0 if facing == 'right' else -1.0
    
    is_moving = phase > 0
    if is_moving:
        wag = math.sin(phase * 4 * math.pi) * 15
        bob = abs(math.sin(phase * 4 * math.pi)) * 2
        leg_cycle = phase
    else:
        # Suspicious stillness
        wag = 0 
        bob = 0
        leg_cycle = 0

    body_w = 60 * scale
    body_h = 30 * scale
    
    # Body
    cx = x
    x_front = cx + (d * body_w/2)
    x_back = cx - (d * body_w/2)
    
    ax.add_patch(Rectangle((cx - body_w/2, y), body_w, body_h, color=FUR))
    
    # Tail
    tail_tip_x = x_back - (d * 20 * scale)
    ax.plot([x_back, tail_tip_x], [y + 25*scale, y + 35*scale + wag], 
            color=FUR, linewidth=5*scale)
            
    # Head
    head_x = x_front
    head_y = y + 20*scale
    ax.add_patch(Circle((head_x, head_y + bob), 18*scale, color=FUR))
    
    # Ear (Perked up if stationary?)
    ear_h = 25*scale if not is_moving else 20*scale
    ear_x = head_x - (d * 5 * scale)
    ax.add_patch(Ellipse((ear_x, head_y + bob + 5*scale), 12*scale, ear_h, color=EAR))
    
    # Snout
    snout_w = 15*scale
    snout_draw_x = head_x if facing=='right' else (head_x - snout_w)
    ax.add_patch(Rectangle((snout_draw_x, head_y + bob - 5*scale), snout_w, 12*scale, color=FUR))
    
    # Nose
    nose_x = head_x + (d * 15 * scale)
    ax.add_patch(Circle((nose_x, head_y + bob + 5*scale), 3*scale, color=NOSE))
    
    # Collar
    collar_draw_x = (x_front - 10*scale) if facing=='right' else (x_front + 5*scale)
    # Adjust for facing flipping
    col_x = x_front - (d*10*scale)
    col_rect_x = col_x if facing=='right' else (col_x - 5*scale)
    ax.add_patch(Rectangle((col_rect_x, y + 15*scale), 5*scale, 15*scale, color=COLLAR))
    
    # LEGS
    leg_h_len = 25 * scale
    leg_w_th = 8 * scale
    
    def draw_leg(anchor_x, anchor_y, l_phase, color):
        if not is_moving:
            ax.plot([anchor_x, anchor_x], [anchor_y, anchor_y - leg_h_len], color=color, linewidth=leg_w_th)
            paw_tip = anchor_x + (d * 5 * scale)
            ax.plot([anchor_x, paw_tip], [anchor_y - leg_h_len, anchor_y - leg_h_len], color=color, linewidth=leg_w_th)
            return

        angle = math.sin((l_phase) * 2 * math.pi)
        kx = anchor_x + (math.sin(angle) * 10 * scale * d)
        ky = anchor_y - leg_h_len
        lift = max(0, -math.sin(angle + math.pi/2)) * 10 * scale
        
        ax.plot([anchor_x, kx], [anchor_y, ky+lift], color=color, linewidth=leg_w_th)
        ax.plot([kx, kx + (d*5*scale)], [ky+lift, ky+lift], color=color, linewidth=leg_w_th)

    front_anchor = x_front - (d * 10 * scale)
    back_anchor = x_back + (d * 10 * scale)
    
    draw_leg(back_anchor, y, leg_cycle + 0.5, SHADOW)
    draw_leg(front_anchor, y, leg_cycle + 0.0, SHADOW)
    draw_leg(back_anchor, y, leg_cycle + 0.0, FUR)
    draw_leg(front_anchor, y, leg_cycle + 0.5, FUR)


def run():
    print(f"LOGIC GARDEN 120: DOG REFUSAL ({TOTAL_FRAMES} frames)")
    scale = 3.5
    
    sx, sy, sw, sh = 50, 600, 980, 720
    
    # Timeline
    f_in = 100
    f_pause = 60
    f_out = 140
    
    start_x_left = sx - 150
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
        
        dog_x = 0
        facing = 'right'
        phase = 0
        caption = ""
        
        if f < f_in:
            # Entering from Left (Moving Right)
            progress = f / f_in
            p = 1 - (1-progress)**2
            dog_x = start_x_left + (p * (center_x - start_x_left))
            facing = 'right'
            phase = f / 18.0
            
        elif f < f_in + f_pause:
            # Pause
            dog_x = center_x
            facing = 'right'
            phase = 0
            if f > f_in + 20: caption = "..."
            
        else:
            # Turn and Return (Moving Left)
            t = (f - (f_in + f_pause)) / f_out
            p = t * t
            if p > 1.0: p = 1.0
            
            dog_x = center_x - (p * (center_x - start_x_left))
            facing = 'left'
            phase = f / 18.0
            caption = "LOGIC GARDEN 120"

        draw_dog(ax, dog_x, floor_y + 30, scale, phase, facing)
        
        if caption:
            ax.text(540, 1500, caption, color=C64['WHITE'], ha='center',
                    fontsize=40, fontname='monospace', weight='bold')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
