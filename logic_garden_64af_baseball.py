"""
SOVEREIGN CODE: logic_garden_64af_baseball.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: C64 VIC-II Emulation
SCENE: Logic Garden 64AF (Baseball)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, Wedge
import matplotlib.patheffects as pe
import os
import math

# CONFIG
FPS = 15
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_64af_baseball"
os.makedirs(OUT_DIR, exist_ok=True)

# C64 PALETTE (Pepto)
C64 = {
    'BLACK': '#000000', 'WHITE': '#FFFFFF', 'RED': '#880000', 'CYAN': '#AAFFEE',
    'PURPLE': '#CC44CC', 'GREEN': '#00CC55', 'BLUE': '#0000AA', 'YELLOW': '#EEEE77',
    'ORANGE': '#DD8855', 'BROWN': '#664400', 'LIGHTRED': '#FF7777', 'DARKGREY': '#333333',
    'GREY': '#777777', 'LIGHTGREEN': '#AAFF66', 'LIGHTBLUE': '#0088FF', 'LIGHTGREY': '#BBBBBB'
}

def draw_pitcher(ax, x, y, scale, phase):
    # Blue Uniform
    # Phase 0: Stand, 1: Leg Kick, 2: Throw
    
    # Body
    ax.add_patch(Rectangle((x, y+15*scale), 14*scale, 18*scale, color=C64['BLUE']))
    
    # Head (Cap)
    ax.add_patch(Circle((x+7*scale, y+38*scale), 6*scale, color=C64['LIGHTRED'])) # Face
    ax.add_patch(Wedge((x+7*scale, y+40*scale), 7*scale, 0, 180, color=C64['BLUE'])) # Cap
    
    # Arm
    if phase == "THROW":
        # Arm forward
        ax.plot([x+14*scale, x+25*scale], [y+28*scale, y+25*scale], color=C64['BLUE'], linewidth=4*scale)
    else:
        # Holding ball
        ax.plot([x+7*scale, x+7*scale], [y+28*scale, y+20*scale], color=C64['BLUE'], linewidth=4*scale)

    # Legs
    if phase == "KICK":
        # Leg up
        ax.plot([x+2*scale, x+2*scale], [y+15*scale, y], color=C64['WHITE'], linewidth=4*scale) # Plant leg
        ax.plot([x+12*scale, x+20*scale], [y+15*scale, y+10*scale], color=C64['WHITE'], linewidth=4*scale) # Kick
    else:
        # Normal stand
        ax.plot([x+2*scale, x+2*scale], [y+15*scale, y], color=C64['WHITE'], linewidth=4*scale)
        ax.plot([x+12*scale, x+12*scale], [y+15*scale, y], color=C64['WHITE'], linewidth=4*scale)

def draw_batter(ax, x, y, scale, phase):
    # Red Uniform
    # Phase 0: Stance, 1: Swing
    
    # Body
    ax.add_patch(Rectangle((x, y+15*scale), 14*scale, 18*scale, color=C64['RED']))
    
    # Legs (Grey pants)
    ax.plot([x+2*scale, x+2*scale], [y+15*scale, y], color=C64['GREY'], linewidth=4*scale)
    ax.plot([x+12*scale, x+12*scale], [y+15*scale, y], color=C64['GREY'], linewidth=4*scale)

    # Head (Helmet)
    ax.add_patch(Circle((x+7*scale, y+38*scale), 7*scale, color=C64['RED']))
    
    # Bat
    hand_x = x - 5*scale
    hand_y = y + 25*scale
    
    if phase == "SWING":
        # Bat extended forward (Horizontal-ish)
        bat_tip_x = x - 35*scale
        bat_tip_y = y + 25*scale
        ax.plot([hand_x, bat_tip_x], [hand_y, bat_tip_y], color=C64['YELLOW'], linewidth=3*scale)
        # Arms
        ax.plot([x+7*scale, hand_x], [y+28*scale, hand_y], color=C64['RED'], linewidth=3*scale)
    else:
        # Bat held high (Vertical)
        bat_tip_x = x - 5*scale
        bat_tip_y = y + 50*scale
        ax.plot([hand_x, bat_tip_x], [hand_y, bat_tip_y], color=C64['YELLOW'], linewidth=3*scale)
        # Arms
        ax.plot([x+7*scale, hand_x], [y+28*scale, hand_y], color=C64['RED'], linewidth=3*scale)


def run():
    print(f"LOGIC GARDEN 64AF: BASEBALL ({TOTAL_FRAMES} frames)")
    
    # ANIMATION STATE MACHINE
    # 0-30: Wait
    # 30-50: Windup (Kick)
    # 50: Throw
    # 50-70: Ball Flight
    # 70: HIT
    # 70-100: Home Run
    
    state = "WAIT"
    ball_x = 0
    ball_y = 0
    scale = 5.0
    
    pitcher_x = 200
    pitcher_y = 650
    batter_x = 800
    batter_y = 650
    
    for f in range(TOTAL_FRAMES):
        
        # --- LOGIC ---
        pitcher_phase = "STAND"
        batter_phase = "STAND"
        show_ball = False
        flash = False
        
        cycle = f % 150 # Loop
        
        if cycle < 30:
            state = "WAIT"
        elif cycle < 50:
            state = "WINDUP"
            pitcher_phase = "KICK"
        elif cycle == 50:
            state = "PITCH"
            pitcher_phase = "THROW"
            # Spawn ball at hand
            ball_x = pitcher_x + 25*scale
            ball_y = pitcher_y + 25*scale
            show_ball = True
        elif cycle < 70:
            state = "FLIGHT"
            pitcher_phase = "THROW"
            show_ball = True
            # Move ball
            t = (cycle - 50) / 20.0
            # Lerp to batter zone
            start_x = pitcher_x + 25*scale
            end_x = batter_x - 10*scale
            ball_x = start_x + (end_x - start_x) * t
            ball_y = pitcher_y + 25*scale # Flat pitch for now
            
        elif cycle == 70:
            state = "HIT"
            batter_phase = "SWING"
            flash = True
            show_ball = True
            ball_x = batter_x - 10*scale
        elif cycle < 100:
            state = "HOMERUN"
            batter_phase = "SWING" # Follow through
            show_ball = True
            # Fly out up and left
            t = (cycle - 70)
            ball_x = (batter_x - 10*scale) - (t * 30) # Fast!
            ball_y = (pitcher_y + 25*scale) + (t * 20)
        else:
            state = "DONE"
            
        # --- RENDER ---
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        # 1. BORDER
        bg_color = C64['LIGHTGREEN']
        if flash: bg_color = C64['WHITE'] # Impact flash
        ax.set_facecolor(bg_color)
        
        # 2. VIRTUAL CRT
        screen_x = 50
        screen_y = 600
        screen_w = 980
        screen_h = 720
        
        ax.add_patch(Rectangle((screen_x, screen_y), screen_w, screen_h, color=C64['GREEN'], zorder=0))
        
        # Dirt / Bases
        # Pitchers Mound
        ax.add_patch(Circle((pitcher_x+10*scale, pitcher_y+10*scale), 30*scale, color=C64['BROWN'], zorder=1))
        # Home Plate circle
        ax.add_patch(Circle((batter_x, batter_y+10*scale), 30*scale, color=C64['BROWN'], zorder=1))
        
        # 3. SPRITES
        draw_pitcher(ax, pitcher_x, pitcher_y, scale, pitcher_phase)
        draw_batter(ax, batter_x, batter_y, scale, batter_phase)
        
        if show_ball:
            ax.add_patch(Circle((ball_x, ball_y), 3*scale, color=C64['WHITE'], zorder=10))

        # 4. SCANLINES
        for y in range(screen_y, screen_y + screen_h, 4):
            ax.axhline(y, color='black', alpha=0.1, linewidth=1)

        # 5. UI
        stroke = [pe.withStroke(linewidth=0, foreground="black")]
        
        ax.text(540, 1600, "LOGIC GARDEN 64AF", color=C64['RED'], ha='center',
                fontsize=40, fontname='monospace', weight='bold')
        
        if state == "HOMERUN":
             ax.text(540, 1400, "IT'S GONE!", color=C64['YELLOW'], ha='center',
                fontsize=50, fontname='monospace', weight='bold', path_effects=[pe.withStroke(linewidth=4, foreground=C64['BLACK'])])

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
