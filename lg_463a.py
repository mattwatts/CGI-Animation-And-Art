import os
import math
from PIL import Image, ImageDraw

# Configuration
WIDTH = 1080
HEIGHT = 1920
FPS = 60
DURATION = 16
TOTAL_FRAMES = FPS * DURATION

os.makedirs("frames", exist_ok=True)

# Core Coordinates
ORIGIN_X, ORIGIN_Y = 250, 1500           # Sydney (Observer location)
ANDROMEDA_X = 900                        # Andromeda Galaxy location
DISTANCE = ANDROMEDA_X - ORIGIN_X

def ease_in_out(t):
    if t <= 0: return 0
    if t >= 1: return 1
    return t * t * (3 - 2 * t)

def draw_dashed_line(draw, pt1, pt2, fill, width, dash_len=10):
    x1, y1 = pt1
    x2, y2 = pt2
    dist = math.hypot(x2 - x1, y2 - y1)
    if dist == 0: return
    dx = (x2 - x1) / dist
    dy = (y2 - y1) / dist
    steps = int(dist / dash_len)
    for i in range(0, steps, 2):
        start = (x1 + i * dash_len * dx, y1 + i * dash_len * dy)
        end = (x1 + (i + 1) * dash_len * dx, y1 + (i + 1) * dash_len * dy)
        draw.line([start, end], fill=fill, width=width)

def draw_glowing_dot(draw, x, y, radius, colour):
    layers = 8
    for i in range(layers):
        r = radius * (1 - (i / layers))
        alpha = int(255 * (i / layers))
        draw.ellipse([(x - r, y - r), (x + r, y + r)], fill=(colour[0], colour[1], colour[2], alpha))

print("Generating exact geometric frames...")

for f in range(TOTAL_FRAMES):
    t = f / TOTAL_FRAMES
    
    # Timeline sequencing
    grid_fade = ease_in_out(min(1, t / 0.05))
    light_cone_prog = ease_in_out(max(0, min(1, (t - 0.05) / 0.10)))
    stationary_now_prog = ease_in_out(max(0, min(1, (t - 15) / 0.10))) # Sydney Now
    walker_prog = ease_in_out(max(0, min(1, (t - 0.35) / 0.20)))       # The Tilt
    light_firewall_prog = ease_in_out(max(0, min(1, (t - 0.70) / 0.20))) # Info travel
    
    # Create canvas
    img = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))
    overlay = Image.new('RGBA', (WIDTH, HEIGHT), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    
    # 1. Draw Background Grid (Space/Time Metric)
    if grid_fade > 0:
        grid_alpha = int(30 * grid_fade)
        for x in range(50, WIDTH, 50):
            draw.line([(x, 0), (x, HEIGHT)], fill=(0, 0, 0, grid_alpha), width=1)
        for y in range(0, HEIGHT, 50):
            draw.line([(0, y), (WIDTH, y)], fill=(0, 0, 0, grid_alpha), width=1)
            
        # Andromeda Timeline (Vertical)
        draw.line([(ANDROMEDA_X, HEIGHT), (ANDROMEDA_X, 0)], fill=(100, 100, 120, int(150 * grid_fade)), width=3)
        
        # Sydney Timeline (Vertical)
        draw.line([(ORIGIN_X, HEIGHT), (ORIGIN_X, 0)], fill=(10, 20, 40, int(200 * grid_fade)), width=4)

    # 2. Add The Light Cone (Speed Limit Firewall - 45 Degrees)
    if light_cone_prog > 0:
        cone_len = 1600 * light_cone_prog
        # Right traveling light
        lx = ORIGIN_X + cone_len
        ly = ORIGIN_Y - cone_len
        draw_dashed_line(draw, (ORIGIN_X, ORIGIN_Y), (lx, ly), (220, 160, 50, 180), 3, 15)
        # Left traveling light
        lx2 = ORIGIN_X - cone_len
        ly2 = ORIGIN_Y - cone_len
        draw_dashed_line(draw, (ORIGIN_X, ORIGIN_Y), (lx2, ly2), (220, 160, 50, 180), 3, 15)

    # 3. Stationary Observer's "Current Moment" (Horizontal)
    if t > 0.15:
        alpha_stat = 255
        line_end_x = ORIGIN_X + (1200 * ease_in_out(max(0, min(1, (t - 0.15)/0.1))))
        draw.line([(ORIGIN_X, ORIGIN_Y), (line_end_x, ORIGIN_Y)], fill=(30, 80, 150, alpha_stat), width=5)
        
        if line_end_x >= ANDROMEDA_X:
            # Event A: Council Debating
            draw_glowing_dot(draw, ANDROMEDA_X, ORIGIN_Y, 15, (30, 80, 150))

    # 4. Moving Observer's "Current Moment" (The Tilt)
    # Velocity fraction determines angle. tan(theta) = v/c
    # We visually use max tan(theta) = 0.5 to keep it on screen
    max_tan_theta = 0.5
    current_tan_theta = max_tan_theta * walker_prog
    
    if walker_prog > 0:
        # Walker's Space Axis (Tilted Up)
        w_end_x = ORIGIN_X + 1200
        w_end_y = ORIGIN_Y - (1200 * current_tan_theta)
        draw.line([(ORIGIN_X, ORIGIN_Y), (w_end_x, w_end_y)], fill=(180, 40, 40, 200), width=5)
        
        # Walker's Time Axis (Tilted Right)
        w_time_x = ORIGIN_X + (1200 * current_tan_theta)
        w_time_y = ORIGIN_Y - 1200
        draw.line([(ORIGIN_X, ORIGIN_Y), (w_time_x, w_time_y)], fill=(180, 40, 40, 120), width=3)
        
        # The Huge Vertical Sweep on Andromeda
        sweep_y = ORIGIN_Y - (DISTANCE * current_tan_theta)
        
        # Highlight the gap (The Future realized today for the walker)
        draw.line([(ANDROMEDA_X, ORIGIN_Y), (ANDROMEDA_X, sweep_y)], fill=(180, 40, 40, 100), width=8)
        
        # Event B: Fleet Launched
        draw_glowing_dot(draw, ANDROMEDA_X, sweep_y, 18, (180, 40, 40))

    # 5. The Light Firewall (Information travelling back to Sydney at 45 degrees)
    if light_firewall_prog > 0:
        final_sweep_y = ORIGIN_Y - (DISTANCE * max_tan_theta)
        # Light travels diagonally at 45 degrees (X decreases by 1, Y decreases by 1)
        firewall_len = DISTANCE * light_firewall_prog
        fx = ANDROMEDA_X - firewall_len
        fy = final_sweep_y - firewall_len
        draw.line([(ANDROMEDA_X, final_sweep_y), (fx, fy)], fill=(220, 150, 0, 255), width=6)
        draw_glowing_dot(draw, fx, fy, 12, (220, 150, 0))

    # Always draw the observers origin point last so it sits on top
    draw_glowing_dot(draw, ORIGIN_X, ORIGIN_Y, 20, (0, 0, 0))
    
    img.paste(overlay, (0, 0), overlay)
    img.save(f"frames/frame_{f:04d}.png")
    
    if f % 120 == 0:
        print(f"Processed {f}/{TOTAL_FRAMES} frames...")

print("Rendering video via FFmpeg...")
os.system("ffmpeg -y -framerate 60 -i frames/frame_%04d.png -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p LG-463_Relativity_Simultaneity.mp4")
print("Render complete: LG-463_Relativity_Simultaneity.mp4")
