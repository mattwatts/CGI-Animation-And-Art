"""
SOVEREIGN CODE: logic_garden_125_tide_turn.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: C64 VIC-II Emulation (Relaxed Rules + Shadows)
SCENE: Logic Garden 125 (LG-64AK Backdrop + LG-121 Foreground)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Ellipse, Wedge
import os
import math

# CONFIG
FPS = 20
DURATION = 15
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_125_tide_turn"
os.makedirs(OUT_DIR, exist_ok=True)

# C64 PALETTE
C64 = {
    'BLACK': '#000000', 'WHITE': '#FFFFFF', 'RED': '#880000', 'CYAN': '#AAFFEE',
    'PURPLE': '#CC44CC', 'GREEN': '#00CC55', 'BLUE': '#0000AA', 'YELLOW': '#EEEE77',
    'ORANGE': '#DD8855', 'BROWN': '#664400', 'LIGHTRED': '#FF7777', 
    'DARKGREY': '#333333', 'GREY': '#777777', 'LIGHTBLUE': '#0088FF'
}

def get_col(color, is_shadow):
    """Enforces absolute black for drop shadows to guarantee visual pop."""
    return C64['BLACK'] if is_shadow else color

def draw_dog(ax, base_x, base_y, scale, phase, facing='left', is_shadow=False):
    x = base_x + (15 if is_shadow else 0)
    y = base_y - (15 if is_shadow else 0)
    
    FUR = get_col(C64['YELLOW'], is_shadow)
    EAR = get_col(C64['BROWN'], is_shadow)
    SHADOW_LEG = get_col(C64['ORANGE'], is_shadow)
    
    d = -1.0 if facing == 'left' else 1.0
    
    is_moving = phase > 0
    wag = math.sin(phase * 4 * math.pi) * 15 if is_moving else math.sin(x*0.1)*5
    bob = abs(math.sin(phase * 4 * math.pi)) * 2 if is_moving else 0
    
    body_w = 50 * scale
    body_h = 25 * scale
    
    cx = x
    x_front = cx + (d * body_w/2)
    x_back = cx - (d * body_w/2)
    
    # Body
    ax.add_patch(Rectangle((cx - body_w/2, y), body_w, body_h, color=FUR))
    
    # Tail
    tail_tip = x_back - (d * 15 * scale)
    ax.plot([x_back, tail_tip], [y + 20*scale, y + 30*scale + wag], color=FUR, linewidth=4*scale)
    
    # Head & Features
    head_y = y + 25*scale
    ax.add_patch(Circle((x_front, head_y + bob), 15*scale, color=FUR))
    ax.add_patch(Ellipse((x_front - (d * 5 * scale), head_y + bob + 5*scale), 10*scale, 18*scale, color=EAR))
    
    snout_w = 12*scale
    snout_x = x_front if d==1 else (x_front - snout_w)
    ax.add_patch(Rectangle((snout_x, head_y + bob - 5*scale), snout_w, 10*scale, color=FUR))
    
    # Legs
    def leg(ox, oy, ph, col):
        ang = math.sin(ph * 2 * math.pi) if is_moving else 0
        kx = ox + (math.sin(ang)*10*scale*d)
        ky = oy - 20*scale
        ax.plot([ox, kx], [oy, ky], color=col, linewidth=5*scale)
        
    leg(x_back, y, phase, SHADOW_LEG)
    leg(x_front, y, phase + 0.5, SHADOW_LEG)
    leg(x_back, y, phase + 0.5, FUR)
    leg(x_front, y, phase, FUR)

def draw_boy(ax, base_x, base_y, scale, phase, facing='left', is_shadow=False):
    x = base_x + (15 if is_shadow else 0)
    y = base_y - (15 if is_shadow else 0)
    
    SHIRT = get_col(C64['CYAN'], is_shadow)
    SHORTS = get_col(C64['RED'], is_shadow)
    SKIN = get_col(C64['LIGHTRED'], is_shadow)
    HAIR = get_col(C64['BROWN'], is_shadow)
    
    d = -1.0 if facing == 'left' else 1.0
    
    is_moving = phase > 0
    bob = abs(math.sin(phase * 2 * math.pi)) * 5 * scale if is_moving else math.sin(x*0.1)*2
    
    w = 20 * scale
    cx = x
    
    # Torso
    ax.add_patch(Rectangle((cx - w/2, y + 25*scale + bob), w, 25*scale, color=SHIRT))
    ax.add_patch(Rectangle((cx - w/2, y + 15*scale + bob), w, 10*scale, color=SHORTS))
    
    # Head
    ax.add_patch(Circle((cx, y + 55*scale + bob), 12*scale, color=SKIN))
    ax.add_patch(Wedge((cx, y + 58*scale + bob), 14*scale, 0, 180, color=HAIR))
    
    # Legs
    swing = math.sin(phase * 2 * math.pi) if is_moving else 0
    fl_x = cx - (d * math.sin(-swing*0.5) * 15 * scale)
    nl_x = cx - (d * math.sin(swing*0.5) * 15 * scale)
    
    ax.plot([cx, fl_x], [y+20*scale+bob, y], color=SKIN, linewidth=6*scale)
    ax.plot([cx, nl_x], [y+20*scale+bob, y], color=SKIN, linewidth=6*scale)

def run():
    print(f"LOGIC GARDEN 125: THE COASTAL TURNAROUND ({TOTAL_FRAMES} frames)")
    scale = 3.5
    
    # Screen boundaries
    sx, sy, sw, sh = 0, 0, 1080, 1920
    
    # Timeline
    f_in = 100
    f_pause = 60
    f_out = 140
    
    start_x_b = sw + 200
    center_x = sw / 2
    
    # Pre-compute wave X coordinates for performance
    wave_x = np.linspace(0, 1080, 100)

    for f in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_xlim(0, 1080)
        ax.set_ylim(0, 1920)
        
        # --- BACKGROUND LOGIC (LG-64AK) ---
        # Sky
        ax.add_patch(Rectangle((0, 1200), 1080, 720, color=C64['CYAN']))
        # Sun
        ax.add_patch(Circle((540, 1200), 250, color=C64['YELLOW'], alpha=0.9))
        
        # Ocean
        ax.add_patch(Rectangle((0, 400), 1080, 800, color=C64['BLUE']))
        
        # Oceanic Tide Waves (Sine logic)
        for w_i in range(5):
            # Waves move progressively downwards
            base_y = 1200 - (((f * 2) + w_i * 160) % 800)
            wave_y = base_y + np.sin(wave_x/60 + f/10) * 15
            ax.plot(wave_x, wave_y, color=C64['WHITE'], linewidth=6, alpha=0.7)
            # Trailing shadow wave for depth
            ax.plot(wave_x, wave_y - 10, color=C64['CYAN'], linewidth=4, alpha=0.4)

        # Sand / Shoreline
        ax.add_patch(Rectangle((0, 0), 1080, 400, color=C64['ORANGE']))
        ax.axhline(400, color=C64['WHITE'], linewidth=8) # Shore foam line
        
        # --- FOREGROUND KINETICS (LG-121) ---
        boy_x = 0
        dog_x = 0
        facing = 'left'
        phase = 0
        
        if f < f_in:
            p = 1 - (1 - f/f_in)**2
            boy_x = start_x_b - (p * (start_x_b - center_x))
            dog_x = boy_x - (60 * scale) # Dog leads moving Left
            facing = 'left'
            phase = f / 18.0
        elif f < f_in + f_pause:
            boy_x = center_x
            dog_x = boy_x - (60 * scale)
            facing = 'left'
            phase = 0
        else:
            t = (f - (f_in + f_pause)) / f_out
            p = min(1.0, t * t)
            boy_x = center_x + (p * (start_x_b - center_x))
            dog_x = boy_x - (60 * scale) # Dog follows moving Right
            facing = 'right'
            phase = f / 18.0

        Y_POS = 300 # Grounded on the Orange Sand
        
        # Draw Drop Shadows First (Lowest Z)
        draw_boy(ax, boy_x, Y_POS + 35, scale, phase, facing, is_shadow=True)
        draw_dog(ax, dog_x, Y_POS + 20, scale, phase, facing, is_shadow=True)
        
        # Draw Sprites (Highest Z)
        draw_boy(ax, boy_x, Y_POS + 35, scale, phase, facing, is_shadow=False)
        draw_dog(ax, dog_x, Y_POS + 20, scale, phase, facing, is_shadow=False)
        
        # Flight Recorder UI
        ax.text(540, 1800, "LOGIC GARDEN 125", color=C64['BLACK'], ha='center',
                fontsize=40, fontname='monospace', weight='bold') # Drop shadow
        ax.text(535, 1805, "LOGIC GARDEN 125", color=C64['WHITE'], ha='center',
                fontsize=40, fontname='monospace', weight='bold')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
