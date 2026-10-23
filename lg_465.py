import os
import math
from PIL import Image, ImageDraw, ImageFont

# -------------------------
# CONFIGURATION
# -------------------------
WIDTH = 1080
HEIGHT = 1920
FPS = 60
DURATION = 16
TOTAL_FRAMES = FPS * DURATION

os.makedirs("frames", exist_ok=True)

# -------------------------
# TYPOGRAPHY ENGINE
# -------------------------
def get_font(size):
    font_paths = [
        "arial.ttf", "Arial.ttf", "/Library/Fonts/Arial.ttf", 
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "C:\\Windows\\Fonts\\arial.ttf"
    ]
    for path in font_paths:
        try:
            return ImageFont.truetype(path, size)
        except IOError:
            continue
    return ImageFont.load_default()

font_h1 = get_font(52)
font_h2 = get_font(40)

def draw_text_with_outline(draw, position, text, font, text_colour, outline_colour=(255, 255, 255, 240), thickness=3):
    x, y = position
    for dx in range(-thickness, thickness + 1):
        for dy in range(-thickness, thickness + 1):
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_colour)
    draw.text((x, y), text, font=font, fill=text_colour)

def ease_in_out(t):
    if t <= 0: return 0
    if t >= 1: return 1
    return t * t * (3 - 2 * t)

# -------------------------
# GEOMETRY ENGINE (RADAR MAP)
# -------------------------
SCALE = 270
OFFSET_X = WIDTH / 2
OFFSET_Y = HEIGHT / 2 + 150  # Shift down slightly

def transform(u, v, warp_factor):
    """ Maps Radar Coordinates (u, v) to physical Canvas Coordinates (X, Y) """
    # The mathematical warp to reproduce the 'TwentyFiveZones' lobes
    X = v + warp_factor * math.sin(math.pi * u) * math.cos(math.pi * v)
    Y = u + warp_factor * math.cos(math.pi * u) * math.sin(math.pi * v)
    
    px = OFFSET_X + X * SCALE
    py = OFFSET_Y - Y * SCALE
    return px, py

def draw_glowing_ray(draw, pt1, pt2, colour, width, max_alpha=255):
    layers = 4
    for i in range(layers):
        w = width + (layers - i) * 2
        alpha = int(max_alpha * (i / layers))
        draw.line([pt1, pt2], fill=(colour[0], colour[1], colour[2], alpha), width=w)

# -------------------------
# RENDER LOOP
# -------------------------
print("Generating exact radar-time geometry for LG-465...")

# Define the coloured zones (u_min, u_max, RGB)
# Pink, Blue, Green, Yellow to match the provided model
zones = [
    (-4.0, -1.0, (244, 219, 244)), # Pink
    (-1.0,  1.0, (219, 244, 244)), # Blue
    ( 1.0,  2.0, (219, 244, 219)), # Green
    ( 2.0,  4.0, (244, 244, 219))  # Yellow
]

max_warp = 0.28  # Safe mathematical bound for grid integrity

for f in range(TOTAL_FRAMES):
    t = f / TOTAL_FRAMES
    
    # Sequence Timers
    warp_prog = ease_in_out(max(0, min(1, (t - 0.10) / 0.20)))      # 10% to 30%
    radar_out_prog = ease_in_out(max(0, min(1, (t - 0.35) / 0.15))) # 35% to 50%
    radar_in_prog = ease_in_out(max(0, min(1, (t - 0.55) / 0.15)))  # 55% to 70%
    highlight_prog = ease_in_out(max(0, min(1, (t - 0.75) / 0.15))) # 75% to 90%
    
    k = max_warp * warp_prog
    
    img = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))
    overlay = Image.new('RGBA', (WIDTH, HEIGHT), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    
    # 1. DRAW BACKGROUND ZONES
    for u_min, u_max, color in zones:
        poly_pts = []
        # Walk along bottom edge
        for i in range(21):
            v_val = -2.0 + (4.0 * i / 20)
            poly_pts.append(transform(u_min, v_val, k))
        # Walk along top edge (reverse)
        for i in range(20, -1, -1):
            v_val = -2.0 + (4.0 * i / 20)
            poly_pts.append(transform(u_max, v_val, k))
            
        draw.polygon(poly_pts, fill=(color[0], color[1], color[2], 255))

    # 2. DRAW GRID LINES (Isocontours)
    major_alpha = 150
    minor_alpha = 40
    
    # Draw V (vertical-ish) lines
    for v_steps in range(-20, 21):
        v = v_steps * 0.1
        is_major = (v_steps % 5 == 0)
        alpha = major_alpha if is_major else minor_alpha
        w = 2 if is_major else 1
        
        path = []
        for u_steps in range(-40, 41):
            u = u_steps * 0.1
            path.append(transform(u, v, k))
        draw.line(path, fill=(80, 80, 110, alpha), width=w)
        
    # Draw U (horizontal-ish) lines (Radar Time Isocontours)
    for u_steps in range(-40, 41):
        u = u_steps * 0.1
        is_major = (u_steps % 10 == 0)
        alpha = major_alpha if is_major else minor_alpha
        w = 2 if is_major else 1
        
        # Highlight specific contours at the end
        if highlight_prog > 0 and (u_steps == -10 or u_steps == 10 or u_steps == 20):
            alpha = int(alpha + (255 - alpha) * highlight_prog)
            w = int(w + 3 * highlight_prog)
            color = (180, 50, 50, alpha)
        else:
            color = (80, 80, 110, alpha)
            
        path = []
        for v_steps in range(-20, 21):
            v = v_steps * 0.1
            path.append(transform(u, v, k))
        draw.line(path, fill=color, width=w)

    # 3. DRAW OBSERVER'S WORLDLINE (Central Red Spine)
    worldline_path = []
    for u_steps in range(-40, 41):
        u = u_steps * 0.1
        worldline_path.append(transform(u, 0, k))
    draw.line(worldline_path, fill=(180, 30, 30, 255), width=6)

    # 4. DRAW RADAR PULSES (Eyes & Ears) 
    # Light travels at exact 45 degrees relative to the raw canvas.
    emit_u = -1.5
    emit_x, emit_y = transform(emit_u, 0, k)
    
    pulse_length = 3.0 * radar_out_prog  # Distance in spacetime
    
    reflect_rx, reflect_ry = emit_x + (pulse_length * SCALE), emit_y - (pulse_length * SCALE)
    reflect_lx, reflect_ly = emit_x - (pulse_length * SCALE), emit_y - (pulse_length * SCALE)
    
    if radar_out_prog > 0:
        # Outgoing beams
        draw_glowing_ray(draw, (emit_x, emit_y), (reflect_rx, reflect_ry), (255, 180, 0), 4)
        draw_glowing_ray(draw, (emit_x, emit_y), (reflect_lx, reflect_ly), (255, 180, 0), 4)
        
    if radar_in_prog > 0:
        # Incoming beams returning to the observer
        return_len = 3.0 * radar_in_prog
        return_rx, return_ry = reflect_rx - (return_len * SCALE), reflect_ry - (return_len * SCALE)
        return_lx, return_ly = reflect_lx + (return_len * SCALE), reflect_ly - (return_len * SCALE)
        
        draw_glowing_ray(draw, (reflect_rx, reflect_ry), (return_rx, return_ry), (0, 200, 255), 4)
        draw_glowing_ray(draw, (reflect_lx, reflect_ly), (return_lx, return_ly), (0, 200, 255), 4)
        
        # Mark Reflection Events
        draw.ellipse([(reflect_rx-8, reflect_ry-8), (reflect_rx+8, reflect_ry+8)], fill=(255, 180, 0, 255))
        draw.ellipse([(reflect_lx-8, reflect_ly-8), (reflect_lx+8, reflect_ly+8)], fill=(255, 180, 0, 255))

    # 5. TYPOGRAPHY LAYER
    text_c = (20, 30, 40, 255)
    
    if t < 0.10:
        draw_text_with_outline(draw, (50, 150), "When you stand still...", font_h1, text_c)
        draw_text_with_outline(draw, (50, 220), "Space and time form a rigid grid.", font_h2, text_c)
    elif 0.10 <= t < 0.35:
        draw_text_with_outline(draw, (50, 150), "When you change speed...", font_h1, text_c)
        draw_text_with_outline(draw, (50, 220), "Your reality physically warps.", font_h2, text_c)
    elif 0.35 <= t < 0.55:
        draw_text_with_outline(draw, (50, 150), "Your eyes and ears...", font_h1, text_c)
        draw_text_with_outline(draw, (50, 220), "Send out signals at the speed of light.", font_h2, (200, 130, 0, 255))
    elif 0.55 <= t < 0.75:
        draw_text_with_outline(draw, (50, 150), "The signals bounce back...", font_h1, text_c)
        draw_text_with_outline(draw, (50, 220), "Telling you when events happened.", font_h2, (0, 150, 200, 255))
    elif t >= 0.75:
        draw_text_with_outline(draw, (50, 100), "These are lines of synchronisation.", font_h1, text_c)
        draw_text_with_outline(draw, (50, 170), "For you, events on the same curve", font_h2, (180, 50, 50, 255))
        draw_text_with_outline(draw, (50, 220), "happen at the exact same moment.", font_h2, (180, 50, 50, 255))

    img.paste(overlay, (0, 0), overlay)
    img.save(f"frames/frame_{f:04d}.png")
    
    if f % 150 == 0:
        print(f"Processed {f}/{TOTAL_FRAMES} frames...")

print("Rendering video via FFmpeg...")
os.system("ffmpeg -y -framerate 60 -i frames/frame_%04d.png -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p LG-465_Radar_Synchronisation.mp4")
print("Render complete: LG-465_Radar_Synchronisation.mp4")
