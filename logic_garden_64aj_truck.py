"""
SOVEREIGN CODE: logic_garden_64aj_truck.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: C64 VIC-II Emulation
SCENE: Logic Garden 64AJ (Truck Cab)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, Wedge
import matplotlib.patheffects as pe
import os
import math
import random

# CONFIG
FPS = 15
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_64aj_truck"
os.makedirs(OUT_DIR, exist_ok=True)

# C64 PALETTE (Pepto)
C64 = {
    'BLACK': '#000000', 'WHITE': '#FFFFFF', 'RED': '#880000', 'CYAN': '#AAFFEE',
    'PURPLE': '#CC44CC', 'GREEN': '#00CC55', 'BLUE': '#0000AA', 'YELLOW': '#EEEE77',
    'ORANGE': '#DD8855', 'BROWN': '#664400', 'LIGHTRED': '#FF7777', 'DARKGREY': '#333333',
    'GREY': '#777777', 'LIGHTGREEN': '#AAFF66', 'LIGHTBLUE': '#0088FF', 'LIGHTGREY': '#BBBBBB'
}

def draw_scenery(ax, window_rect, scroll_x, frame_idx):
    # Clip drawing to window area
    wx, wy, ww, wh = window_rect
    
    # 1. Sky Gradient (Stripes)
    # Sunset: Blue -> Purple -> Orange
    ax.add_patch(Rectangle((wx, wy + wh*0.6), ww, wh*0.4, color=C64['BLUE'], zorder=1))
    ax.add_patch(Rectangle((wx, wy + wh*0.3), ww, wh*0.3, color=C64['PURPLE'], zorder=1))
    ax.add_patch(Rectangle((wx, wy), ww, wh*0.3, color=C64['ORANGE'], zorder=1))
    
    # 2. Distant Hills (Slow Scroll)
    hill_speed = 2.0
    hx = -(scroll_x * 0.2) % 200
    hill_poly = Polygon([
        (wx + hx - 100, wy + 50),
        (wx + hx + 100, wy + 150),
        (wx + hx + 300, wy + 50),
        (wx + hx + 500, wy + 120),
        (wx + hx + 800, wy + 50)
    ], closed=True, color=C64['BLACK'], alpha=0.5, zorder=2)
    # Clip logic is hard with naive poly, so we rely on Z-order and overlaying the Cab on top later
    # Actually, simpler to just draw Cab Frame *after* this heavily.
    ax.add_patch(hill_poly)
    
    # 3. Telephone Poles (Fast Scroll)
    pole_speed = 15.0
    pole_gap = 400
    pole_offset = (frame_idx * pole_speed) % pole_gap
    
    for i in range(3):
        px = wx + ww - pole_offset + (i * pole_gap)
        if px > wx - 50 and px < wx + ww + 50:
            # Pole
            ax.add_patch(Rectangle((px, wy), 10, wh, color=C64['BLACK'], zorder=3))
            # Crossbar
            ax.add_patch(Rectangle((px-20, wy + wh - 50), 40, 5, color=C64['BLACK'], zorder=3))
            # Wires
            ax.plot([wx, ww+wx], [wy+wh-50, wy+wh-60], color=C64['BLACK'], linewidth=1, zorder=3)

def draw_dad_driver(ax, x, y, scale, bounce):
    # RHD -> Dad on Right
    
    # Seat (High back)
    ax.add_patch(Rectangle((x - 10*scale, y), 25*scale, 40*scale, color=C64['GREY']))
    
    # Body (Flannel/Blue Shirt)
    ax.add_patch(Rectangle((x, y + 10*scale + bounce), 18*scale, 25*scale, color=C64['BLUE']))
    
    # Head
    head_y = y + 35*scale + bounce
    ax.add_patch(Circle((x + 8*scale, head_y), 8*scale, color=C64['LIGHTRED']))
    
    # Trucker Cap
    ax.add_patch(Wedge((x + 8*scale, head_y + 4*scale), 9*scale, 0, 180, color=C64['RED']))
    ax.add_patch(Rectangle((x - 2*scale, head_y + 4*scale), 10*scale, 2*scale, color=C64['RED'])) # Brim facing left (talking to kid) or right (road)? Road.
    
    # Arms / Steering Wheel
    # Steering Wheel (Side view - Ellipse)
    wheel_x = x + 25*scale
    wheel_y = y + 20*scale + bounce
    ax.add_patch(Circle((wheel_x, wheel_y), 12*scale, fill=False, edgecolor=C64['BLACK'], linewidth=3*scale))
    
    # Arms reaching to wheel
    shoulder_x = x + 5*scale
    shoulder_y = y + 30*scale + bounce
    ax.plot([shoulder_x, wheel_x], [shoulder_y, wheel_y], color=C64['BLUE'], linewidth=4*scale)
    
    # Hands on wheel
    ax.add_patch(Circle((wheel_x - 2*scale, wheel_y + 5*scale), 3*scale, color=C64['LIGHTRED']))

def draw_kid_passenger(ax, x, y, scale, bounce, wave_cycle):
    # Passenger Seat (Left)
    ax.add_patch(Rectangle((x - 5*scale, y), 25*scale, 35*scale, color=C64['GREY']))
    
    # Body (Small)
    ax.add_patch(Rectangle((x + 2*scale, y + 10*scale + bounce), 12*scale, 15*scale, color=C64['GREEN']))
    
    # Head
    head_y = y + 26*scale + bounce
    ax.add_patch(Circle((x + 8*scale, head_y), 6*scale, color=C64['LIGHTRED']))
    
    # Arm (Pointing at window)
    shoulder_x = x + 10*scale
    shoulder_y = y + 20*scale + bounce
    
    # Pointing animation
    arm_angle = math.sin(wave_cycle * 0.2) * 20
    arm_len = 15*scale
    hand_x = shoulder_x - (math.cos(math.radians(arm_angle)) * arm_len) # Pointing Left (out window?) 
    # Wait, RHD usually keeps Driver Right, Passenger Left. Window is on the Left or Front?
    # If side view, we look in from passenger side? Or cutaway?
    # Let's assume Cutaway looking from PASSENGER side (Left).
    # So Kid is close, Dad is far?
    # Or purely 2D profile. 
    # Let's point Left (towards window if window is backdrop).
    pass_hand_y = shoulder_y + (math.sin(math.radians(arm_angle)) * arm_len)
    
    ax.plot([shoulder_x, hand_x], [shoulder_y, pass_hand_y], color=C64['GREEN'], linewidth=3*scale)

def run():
    print(f"LOGIC GARDEN 64AJ: TRUCK ({TOTAL_FRAMES} frames)")
    
    scale = 6.0
    
    # Positions (Screen coords)
    cab_x = 100
    cab_y = 600
    cab_w = 880
    cab_h = 500
    
    # RHD: Kid Left (Passenger), Dad Right (Driver)
    kid_x = cab_x + 150
    dad_x = cab_x + 550
    
    for f in range(TOTAL_FRAMES):
        
        # --- LOGIC ---
        # Truck Vibration
        vibe_y = math.sin(f * 2.5) * 5 # High freq rumble
        bounce_y = math.sin(f * 0.2) * 15 # Low freq suspension
        total_bounce = vibe_y + bounce_y
        
        # --- RENDER ---
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        # 1. BORDER (C64 Grey)
        ax.set_facecolor(C64['DARKGREY'])
        
        # 2. VIRTUAL CRT
        screen_x = 50
        screen_y = 600
        screen_w = 980
        screen_h = 720
        
        # Clear Screen
        ax.add_patch(Rectangle((screen_x, screen_y), screen_w, screen_h, color=C64['BLACK'], zorder=0))
        
        # 3. WINDOW (The View)
        # Defines the viewable area
        win_x = screen_x + 50
        win_y = screen_y + 250
        win_w = 880
        win_h = 350
        
        draw_scenery(ax, (win_x, win_y, win_w, win_h), f * 10, f)
        
        # 4. CAB INTERIOR (MASK)
        # Draw the Cab Structure overlaying the scenery
        # Structure Color
        cab_col = C64['BROWN'] # Retro wood texture? or Grey plastic
        
        # Dashboard (Bottom)
        ax.add_patch(Rectangle((screen_x, screen_y), screen_w, 250, color=cab_col, zorder=5))
        # Roof / Frame (Top)
        ax.add_patch(Rectangle((screen_x, win_y + win_h), screen_w, 120, color=cab_col, zorder=5))
        # A-Pillar / B-Pillar
        ax.add_patch(Rectangle((screen_x, screen_y), 50, screen_h, color=cab_col, zorder=5))
        ax.add_patch(Rectangle((screen_x + screen_w - 50, screen_y), 50, screen_h, color=cab_col, zorder=5))
        
        # 5. CHARACTERS (Inside the Cab)
        # They bounce WITH the truck usually? Or truck bounces around them?
        # Usually seats suspension absorbs.
        # Let's bounce the CHARACTERS and the WINDOW stays (chassis), while SCENERY shakes?
        # Simpler: Cab shakes relative to camera.
        
        # Apply Bounce offset to everything "Attached" to truck
        # Actually easier to shake the scenery (Camera shake).
        # Let's bounce characters on seats.
        
        draw_kid_passenger(ax, kid_x, cab_y + 50, scale, total_bounce * 0.8, f)
        draw_dad_driver(ax, dad_x, cab_y + 50, scale, total_bounce * 0.5) # Dad bounces less (heavier)
        
        # 6. DASHBOARD DETAILS
        # Steering Column
        ax.add_patch(Rectangle((dad_x + 130, cab_y + 100 + total_bounce), 20, 100, color=C64['BLACK'], zorder=6))
        # Radio
        ax.add_patch(Rectangle((cab_x + 400, cab_y + 100 + total_bounce), 80, 40, color=C64['BLACK'], zorder=6))
        # CB Radio Mic wire
        ax.plot([cab_x + 420, cab_x + 440], [cab_y + 100 + total_bounce, cab_y + 80 + total_bounce], color=C64['BLACK'], linewidth=2, zorder=6)

        # 7. SCANLINES
        for y in range(screen_y, screen_y + screen_h, 4):
            ax.axhline(y, color='black', alpha=0.1, linewidth=1, zorder=10)

        # 8. UI
        stroke = [pe.withStroke(linewidth=0, foreground="black")]
        
        ax.text(540, 1600, "LOGIC GARDEN 64AJ", color=C64['ORANGE'], ha='center',
                fontsize=40, fontname='monospace', weight='bold', path_effects=[pe.withStroke(linewidth=4, foreground=C64['BLACK'])])
        
        ax.text(540, 1500, "TRUCK'N", color=C64['YELLOW'], ha='center',
                fontsize=30, fontname='monospace', weight='bold')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
