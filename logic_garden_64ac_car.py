"""
SOVEREIGN CODE: logic_garden_64ac_car.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: C64 VIC-II Emulation
SCENE: Logic Garden 64AC (Car Driving)
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
OUT_DIR = "frames_64ac_car"
os.makedirs(OUT_DIR, exist_ok=True)

# C64 PALETTE (Pepto)
C64 = {
    'BLACK': '#000000', 'WHITE': '#FFFFFF', 'RED': '#880000', 'CYAN': '#AAFFEE',
    'PURPLE': '#CC44CC', 'GREEN': '#00CC55', 'BLUE': '#0000AA', 'YELLOW': '#EEEE77',
    'ORANGE': '#DD8855', 'BROWN': '#664400', 'LIGHTRED': '#FF7777', 'DARKGREY': '#333333',
    'GREY': '#777777', 'LIGHTGREEN': '#AAFF66', 'LIGHTBLUE': '#0088FF', 'LIGHTGREY': '#BBBBBB'
}

def draw_car_sprite(ax, x, y, scale, bounce, wheel_rot):
    # CAR BODY (RED)
    # Main chassis
    ax.add_patch(Rectangle((x, y + bounce), 40*scale, 12*scale, color=C64['RED']))
    # Cabin (Dark Grey/Black glass)
    p = Polygon([
        (x + 5*scale, y + 12*scale + bounce),
        (x + 10*scale, y + 20*scale + bounce),
        (x + 25*scale, y + 20*scale + bounce),
        (x + 35*scale, y + 12*scale + bounce)
    ], closed=True, color=C64['BLACK'])
    ax.add_patch(p)
    
    # Roof highlight
    ax.plot([x + 10*scale, x + 25*scale], [y + 20*scale + bounce, y + 20*scale + bounce], 
            color=C64['LIGHTRED'], linewidth=2*scale)

    # Spoiler
    ax.add_patch(Rectangle((x - 2*scale, y + 12*scale + bounce), 5*scale, 4*scale, color=C64['RED']))

    # WHEELS (Black Rubber, Grey Mag)
    # Rear
    rx, ry = x + 8*scale, y + bounce
    ax.add_patch(Circle((rx, ry), 7*scale, color=C64['BLACK'])) # Tire
    
    # Front
    fx, fy = x + 32*scale, y + bounce
    ax.add_patch(Circle((fx, fy), 7*scale, color=C64['BLACK'])) # Tire
    
    # Hubcaps (Rotating)
    # We simulate rotation by toggling the cross shape color or angle
    hub_col = C64['GREY']
    spoke_col = C64['LIGHTGREY']
    if wheel_rot % 2 == 0:
        hub_col, spoke_col = spoke_col, hub_col
    
    # Draw simple "Cross" spokes
    for wx, wy in [(rx, ry), (fx, fy)]:
        ax.add_patch(Circle((wx, wy), 4*scale, color=hub_col))
        ax.add_patch(Rectangle((wx - 1*scale, wy - 4*scale), 2*scale, 8*scale, color=spoke_col))
        ax.add_patch(Rectangle((wx - 4*scale, wy - 1*scale), 8*scale, 2*scale, color=spoke_col))


def run():
    print(f"LOGIC GARDEN 64AC: CAR ({TOTAL_FRAMES} frames)")
    
    # ASSET GENERATION
    # Hills
    hills = []
    for i in range(20):
        hills.append(random.randint(50, 150))
        
    # City Buildings
    buildings = []
    for i in range(30):
        buildings.append((random.randint(20, 60), random.randint(50, 120))) # width, height

    for f in range(TOTAL_FRAMES):
        
        # --- LOGIC ---
        # Scroll speeds
        speed_sky = 0.5
        speed_hills = 2.0
        speed_city = 5.0
        speed_road = 15.0
        
        off_hills = (f * speed_hills)
        off_city = (f * speed_city)
        off_road = (f * speed_road)
        
        # Car Bounce
        bounce = math.sin(f * 0.8) * 3.0
        
        # --- RENDER ---
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        # 1. BORDER / BACKGROUND
        ax.set_facecolor(C64['BLACK'])
        
        # 2. VIRTUAL CRT
        screen_x = 50
        screen_y = 600
        screen_w = 980
        screen_h = 720
        
        # Sky (Night)
        ax.add_patch(Rectangle((screen_x, screen_y + 200), screen_w, 520, color=C64['BLUE'], zorder=0))
        
        # Moon (Static)
        ax.add_patch(Circle((screen_x + 800, screen_y + 600), 40, color=C64['WHITE'], alpha=0.9, zorder=1))

        # 3. PARALLAX LAYERS
        
        # Layer 1: Hills (Purple)
        # Draw connected polygon? Or simple rect content
        # We loop hills
        hill_w = 100
        for i, h in enumerate(hills):
            hx = (i * hill_w) - (off_hills % (len(hills)*hill_w))
            pos_x = screen_x + hx
            # Wrap visual
            if pos_x < screen_x - 200: pos_x += (len(hills)*hill_w)
            
            if -200 < pos_x < screen_w + 100:
                # Draw Triangle Hill
                verts = [
                    (pos_x, screen_y + 150),
                    (pos_x + hill_w/2, screen_y + 150 + h),
                    (pos_x + hill_w, screen_y + 150)
                ]
                p = Polygon(verts, closed=True, color=C64['PURPLE'], zorder=2)
                ax.add_patch(p)

        # Layer 2: City (Dark Blue/Grey)
        total_city_w = 0
        for bw, bh in buildings: total_city_w += bw
        
        curr_x = 0
        for i, (bw, bh) in enumerate(buildings):
            bx = curr_x - (off_city % total_city_w)
            while bx < -100: bx += total_city_w # wrap
            
            pos_x = screen_x + bx
            if -100 < pos_x < screen_w + 100:
                ax.add_patch(Rectangle((pos_x, screen_y + 150), bw, bh, color=C64['DARKGREY'], zorder=3))
                # Windows
                if i % 3 == 0:
                    ax.add_patch(Rectangle((pos_x+5, screen_y + 150 + 10), 5, 5, color=C64['YELLOW'], zorder=4))
                    ax.add_patch(Rectangle((pos_x+5, screen_y + 150 + 30), 5, 5, color=C64['YELLOW'], zorder=4))

            curr_x += bw

        # Layer 3: Ground / Road
        ax.add_patch(Rectangle((screen_x, screen_y), screen_w, 150, color=C64['GREY'], zorder=5))
        
        # Road Lines (White dashes)
        dash_spacing = 100
        dash_off = off_road % dash_spacing
        for i in range(15):
            dx = screen_x + (i * dash_spacing) - dash_off
            ax.add_patch(Rectangle((dx, screen_y + 50), 40, 10, color=C64['WHITE'], zorder=6))

        # 4. STREETLIGHTS (Foreground Pop)
        light_spacing = 400
        light_off = (f * (speed_road * 1.2)) % light_spacing # Move faster than car? No, relative.
        
        # If car is moving right, lights move left
        # Let's say camera is tracking car, so road moves Left.
        
        highlight_car = False
        
        for i in range(5):
            lx = screen_x + (i * light_spacing) - light_off + 800
            if lx < screen_x - 100: lx += 2000 # Wrap
            
            if -100 < lx < screen_w + 100:
                # Pole
                ax.add_patch(Rectangle((lx, screen_y + 50), 10, 400, color=C64['LIGHTGREY'], zorder=7))
                # Lamp
                ax.add_patch(Wedge((lx-10, screen_y + 450), 30, 0, 180, color=C64['WHITE'], zorder=7))
                
                # Check for "Highlight" effect (Passes car)
                # Car is at center roughly
                if abs(lx - (screen_x + 300)) < 50:
                    highlight_car = True

        # 5. CAR SPRITE
        # Scale 4.0
        car_draw_x = screen_x + 200 # Fixed X
        car_draw_y = screen_y + 70 # Fixed Y base
        
        draw_car_sprite(ax, car_draw_x, car_draw_y, 4.0, bounce, f)
        
        # HEADLIGHTS
        # Cone of light
        light_poly = Polygon([
            (car_draw_x + 140, car_draw_y + 30 + bounce),
            (car_draw_x + 600, car_draw_y + 100 + bounce),
            (car_draw_x + 600, car_draw_y - 50 + bounce)
        ], closed=True, color=C64['YELLOW'], alpha=0.3, zorder=8)
        ax.add_patch(light_poly)

        # 6. SCANLINES
        for y in range(screen_y, screen_y + screen_h, 4):
            ax.axhline(y, color='black', alpha=0.1, linewidth=1)

        # 7. UI
        stroke = [pe.withStroke(linewidth=0, foreground="black")]
        
        ax.text(540, 1600, "LOGIC GARDEN 64AC", color=C64['LIGHTRED'], ha='center',
                fontsize=40, fontname='monospace', weight='bold')
        
        ax.text(540, 1500, "NIGHT DRIVE", color=C64['GREY'], ha='center',
                fontsize=30, fontname='monospace')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
