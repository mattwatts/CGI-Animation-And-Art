import os
import math
from PIL import Image, ImageDraw, ImageFont

# -------------------------
# CONFIGURATION
# -------------------------
WIDTH = 1080
HEIGHT = 1920
FPS = 60
DURATION = 32  # Expanded to 32 seconds for a highly tranquil, slow progression
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

# -------------------------
# 3D CAMERA & GEOMETRY
# -------------------------
def project(x, y, z, cam_angle_rad, tilt_rad, scale, offset_x=WIDTH/2, offset_y=HEIGHT/2):
    # Rotate around Y axis (pan)
    x_rot = x * math.cos(cam_angle_rad) - z * math.sin(cam_angle_rad)
    z_rot = x * math.sin(cam_angle_rad) + z * math.cos(cam_angle_rad)
    
    # Rotate around X axis (tilt)
    y_rot = y * math.cos(tilt_rad) - z_rot * math.sin(tilt_rad)
    
    px = offset_x + (x_rot * scale)
    py = offset_y - (y_rot * scale)
    return px, py, z_rot

def draw_glowing_dot(draw, x, y, radius, colour, max_alpha=255):
    layers = 4
    for i in range(layers):
        r = radius * (1 - (i / layers))
        alpha = int(max_alpha * (i / layers))
        draw.ellipse([(x - r, y - r), (x + r, y + r)], fill=(colour[0], colour[1], colour[2], alpha))

# -------------------------
# RENDER LOOP
# -------------------------
print("Generating slow, tranquil continuous mechanics for LG-466...")

NODE_SPACING = 1.8
NUM_PARTICLES = 16
ORBIT_RADIUS = 2.8
PULSE_PERIOD = 4.0  # 4 seconds per cycle (0.25Hz). Very tranquil.

for f in range(TOTAL_FRAMES):
    t = f / FPS
    loop_progress = f / TOTAL_FRAMES
    
    # Scale time so the geometry moves 1 unit every 4 seconds.
    scaled_t = t / PULSE_PERIOD
    
    # PULSE MECHANICS (0.25 Hz)
    # Cosine wave from 0.0 to 1.0, peaking smoothly every 4 seconds.
    raw_pulse = (math.cos(scaled_t * 2 * math.pi) + 1.0) / 2.0
    
    # Base intensity NEVER drops below 0.40 to guarantee continuous visibility.
    pulse_intensity = 0.40 + 0.60 * (raw_pulse ** 4)
    
    # CAMERA (Seamless 360 degree pan across the 32 second loop)
    cam_angle = loop_progress * 2 * math.pi
    cam_tilt = 0.35 + (math.sin(loop_progress * 2 * math.pi * 2) * 0.05)
    
    img = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))
    overlay = Image.new('RGBA', (WIDTH, HEIGHT), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    
    scale = 130
    
    # 1. THE CENTRAL MEDIUM (Always solid and unbroken)
    draw.line([(WIDTH/2, 0), (WIDTH/2, HEIGHT)], fill=(120, 130, 140, 120), width=8)

    rendered_elements = []
    
    # 2. INFINITE TREADMILL NODES
    start_i = int(scaled_t) - 10
    end_i = int(scaled_t) + 10
    
    for i in range(start_i, end_i):
        # Position relative to Present (y=0). Moves remarkably smoothly now.
        y_pos = (i - scaled_t) * NODE_SPACING 
        
        is_present = abs(y_pos) < (NODE_SPACING / 2.5)
        is_past = y_pos < 0 and not is_present
        is_future = y_pos > 0 and not is_present
        
        # High-contrast baseline parameters
        if is_present:
            node_colour = (190, 20, 40) # Sharp Red
            alpha_mult = pulse_intensity
            scatter_amp = (1.0 - pulse_intensity) * 2.5 # Structural static blossoms slowly
        elif is_past:
            node_colour = (20, 70, 140) # Deep Blue
            alpha_mult = max(0.4, 1.0 - (abs(y_pos) * 0.1))
            scatter_amp = 0.0 # Memories remain perfectly solidified
        else:
            node_colour = (70, 80, 90) # Slate Grey
            alpha_mult = max(0.4, 1.0 - (abs(y_pos) * 0.1))
            scatter_amp = 1.0 
            
        cx, cy, cz = project(0, y_pos, 0, cam_angle, cam_tilt, scale)
        rendered_elements.append((cz, 'node', (cx, cy), node_colour, alpha_mult, is_present))
        
        pts = []
        # Draw orbiting particles
        for p in range(NUM_PARTICLES):
            angle = (p / NUM_PARTICLES) * 2 * math.pi
            
            # Slow, mathematically phase-locked drift
            drift_clock = (scaled_t * 2 * math.pi) * 2
            px = math.cos(angle) * ORBIT_RADIUS + (math.sin(drift_clock + i + p) * scatter_amp)
            pz = math.sin(angle) * ORBIT_RADIUS + (math.cos(drift_clock + i + p) * scatter_amp)
            
            rx, ry, rz = project(px, y_pos, pz, cam_angle, cam_tilt, scale)
            pts.append((rx, ry))
            rendered_elements.append((rz, 'particle', (rx, ry), node_colour, max(0.5, alpha_mult)))
            
        # Bond connections
        for p in range(NUM_PARTICLES):
            p1 = pts[p]
            p2 = pts[(p + 1) % NUM_PARTICLES]
            p3 = (cx, cy)
            
            if is_present:
                line_col = (node_colour[0], node_colour[1], node_colour[2], int(255 * pulse_intensity))
                draw.line([p1, p2], fill=line_col, width=max(2, int(4 * pulse_intensity)))
                draw.line([p1, p3], fill=line_col, width=max(1, int(3 * pulse_intensity)))
            elif is_past:
                line_col = (node_colour[0], node_colour[1], node_colour[2], int(200 * alpha_mult))
                draw.line([p1, p2], fill=line_col, width=3)

    # Depth sorting for 3D visual integrity
    rendered_elements.sort(key=lambda x: x[0], reverse=True)
    
    for el in rendered_elements:
        if el[1] == 'node':
            cx, cy = el[2]
            rgb = el[3]
            a = el[4]
            is_p = el[5]
            radius = 20 * a if is_p else 10
            draw_glowing_dot(draw, cx, cy, radius, rgb, int(255 * a))
            
        elif el[1] == 'particle':
            cx, cy = el[2]
            rgb = el[3]
            a = el[4]
            draw.ellipse([(cx-4, cy-4), (cx+4, cy+4)], fill=(rgb[0], rgb[1], rgb[2], int(255 * a)))

    # 3. TYPOGRAPHY LAYER (Now spread over 32 seconds)
    text_c = (20, 25, 30, 255)
    
    if t < 8.0:
        draw_text_with_outline(draw, (50, 150), "Consciousness is a clock pulse.", font_h1, text_c)
        draw_text_with_outline(draw, (50, 220), "A continuous chain linking the past", font_h2, text_c)
        draw_text_with_outline(draw, (50, 270), "^ flowing vertically into the future v", font_h2, text_c)
    elif 8.0 <= t < 16.0:
        draw_text_with_outline(draw, (50, 150), "When the pulse strikes...", font_h1, (180, 20, 40, 255))
        draw_text_with_outline(draw, (50, 220), "Biological static steadily locks into", font_h2, text_c)
        draw_text_with_outline(draw, (50, 270), "rigid, high-contrast geometry.", font_h2, text_c)
    elif 16.0 <= t < 24.0:
        draw_text_with_outline(draw, (50, 150), "Generating a frame of perception.", font_h1, text_c)
        draw_text_with_outline(draw, (50, 220), "This highly ordered state allows you to", font_h2, text_c)
        draw_text_with_outline(draw, (50, 270), "temporarily form ideas and memories.", font_h2, text_c)
    elif t >= 24.0:
        draw_text_with_outline(draw, (50, 150), "Between the pulses:", font_h1, text_c)
        draw_text_with_outline(draw, (50, 220), "The mind crystal slowly decomposes.", font_h2, (180, 20, 40, 255))
        draw_text_with_outline(draw, (50, 270), "Your brain simply hallucinates the gaps.", font_h2, text_c)

    # UI Context
    draw.line([(50, HEIGHT-100), (WIDTH-50, HEIGHT-100)], fill=(200, 205, 210, 180), width=3)
    draw_text_with_outline(draw, (50, HEIGHT-80), "PULSE FREQUENCY: 0.25Hz", font_h2, (120, 130, 140, 255))
    draw_text_with_outline(draw, (WIDTH-420, HEIGHT-80), "MECHANISM: SEAMLESS LOOP", font_h2, (120, 130, 140, 255))

    img.paste(overlay, (0, 0), overlay)
    img.save(f"frames/frame_{f:04d}.png")
    
    if f % 150 == 0:
        print(f"Processed {f}/{TOTAL_FRAMES} frames...")

print("Rendering tranquil seamless video via FFmpeg...")
os.system("ffmpeg -y -framerate 60 -i frames/frame_%04d.png -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p LG-466_The_Consciousness_Machine.mp4")
print("Render complete: LG-466_The_Consciousness_Machine.mp4")
