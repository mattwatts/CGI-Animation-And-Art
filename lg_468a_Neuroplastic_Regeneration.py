import os
import math
import random
from PIL import Image, ImageDraw, ImageFont

# -------------------------
# CONFIGURATION
# -------------------------
WIDTH = 1080
HEIGHT = 1920
FPS = 60
DURATION = 32  # 32-second seamless cycle
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

font_h1 = get_font(48)
font_h2 = get_font(36)

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
def project(x, y, z, cam_angle_rad, tilt_rad, scale, offset_x=WIDTH/2, offset_y=HEIGHT/2 + 30):
    x_rot = x * math.cos(cam_angle_rad) - z * math.sin(cam_angle_rad)
    z_rot = x * math.sin(cam_angle_rad) + z * math.cos(cam_angle_rad)
    y_rot = y * math.cos(tilt_rad) - z_rot * math.sin(tilt_rad)
    px = offset_x + (x_rot * scale)
    py = offset_y - (y_rot * scale)
    return px, py, z_rot

def draw_glowing_dot(draw, x, y, radius, colour, max_alpha=255):
    layers = 5
    for i in range(layers):
        r = radius * (1 - (i / layers))
        alpha = int(max_alpha * (i / layers))
        draw.ellipse([(x - r, y - r), (x + r, y + r)], fill=(colour[0], colour[1], colour[2], alpha))

def smoothstep(edge0, edge1, x):
    t = max(0.0, min(1.0, (x - edge0) / (edge1 - edge0)))
    return t * t * (3.0 - 2.0 * t)

# -------------------------
# STRUCTURAL VARIABLES
# -------------------------
print("Generating exact neuroplastic thermodynamic matrix for LG-468...")

NODE_TOP = (0, 6.0, 0)
NODE_BOT = (0, -6.0, 0)

# Peripheral "Silent Synapses"
NUM_PERIPHERAL = 8
RAD_PERIPHERAL = 4.5
silent_nodes = []
for i in range(NUM_PERIPHERAL):
    angle = (i / NUM_PERIPHERAL) * 2 * math.pi
    silent_nodes.append((math.cos(angle)*RAD_PERIPHERAL, 0, math.sin(angle)*RAD_PERIPHERAL))

# -------------------------
# RENDER LOOP
# -------------------------
for f in range(TOTAL_FRAMES):
    t = f / FPS
    loop_progress = f / TOTAL_FRAMES
    
    # Mathematical Phase Curves
    phase_death = smoothstep(2.0, 4.0, t)        # 1.0 when broken
    phase_sprout = smoothstep(6.0, 10.0, t) - smoothstep(18.0, 24.0, t) # Bell curve of chaotic exploration
    phase_hebbian = smoothstep(16.0, 20.0, t)    # 1.0 when detour is locked
    phase_morph = smoothstep(26.0, 31.5, t)      # 1.0 when structure is physically normalized (Deep Sleep)
    
    # Camera gently orbits, proving exact 3D geometry
    cam_angle = loop_progress * 2 * math.pi * 1.5 
    cam_tilt = 0.20 + (math.sin(loop_progress * 2 * math.pi) * 0.1)
    
    img = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))
    overlay = Image.new('RGBA', (WIDTH, HEIGHT), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    scale = 135
    
    rendered_elements = []
    
    # Primary Nodes
    px_top, py_top, pz_top = project(*NODE_TOP, cam_angle, cam_tilt, scale)
    px_bot, py_bot, pz_bot = project(*NODE_BOT, cam_angle, cam_tilt, scale)
    rendered_elements.append((pz_top, 'node', (px_top, py_top), (20, 25, 30), 1.0, 10))
    rendered_elements.append((pz_bot, 'node', (px_bot, py_bot), (20, 25, 30), 1.0, 10))
    
    # The Decaying / Morphing Central Node Matrix
    # Morph pulls the elected detour node (index 0) firmly back into the center
    chosen_peripheral = silent_nodes[0]
    
    # Central Coordinate interpolates. When `phase_morph` engages, the chosen node slides to (0,0,0)
    current_mid_x = chosen_peripheral[0] * (1.0 - phase_morph)
    current_mid_y = chosen_peripheral[1] * (1.0 - phase_morph)
    current_mid_z = chosen_peripheral[2] * (1.0 - phase_morph)
    
    px_mid, py_mid, pz_mid = project(current_mid_x, current_mid_y, current_mid_z, cam_angle, cam_tilt, scale)
    
    # Prior to breakage, it sits in center. After morph, it returns to center.
    mid_alpha = max(1.0 - phase_death, phase_hebbian)
    if mid_alpha > 0.05:
        rgb = (190, 20, 40) if phase_hebbian > 0.5 else (20, 70, 140)
        rendered_elements.append((pz_mid, 'node', (px_mid, py_mid), rgb, mid_alpha, 12))
        
    # Particle scatter (Cell Death representation)
    if phase_death > 0 and phase_death < 1.0 or (phase_death == 1.0 and phase_hebbian < 1.0):
        scatter_t = max(0, t - 2.0)
        for i in range(20):
            sx = math.cos(i * 1.5) * (scatter_t * 2.0)
            sy = math.sin(i * 2.1) * (scatter_t * 2.0)
            sz = math.cos(i * 3.3) * (scatter_t * 2.0)
            rx, ry, rz = project(sx, sy, sz, cam_angle, cam_tilt, scale)
            a = max(0, 1.0 - (scatter_t * 0.2))
            if a > 0:
                rendered_elements.append((rz, 'particle', (rx, ry), (120, 130, 140), a))
    
    # Primary Connections
    # 0s to 4s: Straight line intact. 26s to 32s: Morphs back into straight line.
    if mid_alpha > 0.05:
        line_a = int(255 * mid_alpha)
        # Pulse flows down the connection
        pulse_c = int(math.sin(t * 8) * 100) + 155 if (t < 2.0 or t > 18.0) else 150
        thick = 4 if phase_hebbian > 0 else 2
        
        draw.line([(px_top, py_top), (px_mid, py_mid)], fill=(190, 20, 40, line_a) if phase_hebbian>0 else (40, 60, 120, line_a), width=thick)
        draw.line([(px_mid, py_mid), (px_bot, py_bot)], fill=(190, 20, 40, line_a) if phase_hebbian>0 else (40, 60, 120, line_a), width=thick)

    # Peripheral Silent Synapses & Collateral Sprouting web
    random.seed(468)
    for i in range(1, NUM_PERIPHERAL):
        ox, oy, oz = silent_nodes[i]
        
        # New base nodes fade in at end to replace the one that was consumed
        n_alpha = max(0.2, phase_morph * 0.2)
        rx, ry, rz = project(ox, oy, oz, cam_angle, cam_tilt, scale)
        rendered_elements.append((rz, 'node', (rx, ry), (150, 160, 170), n_alpha, 4))
        
        if phase_sprout > 0.05:
            # Massive over-growth of chaotic searching lines
            num_sprouts = 6
            for s in range(num_sprouts):
                noise_x = math.sin(t * (random.uniform(2, 6)) + s) * 0.5
                noise_y = math.cos(t * (random.uniform(2, 6)) + i) * 0.5
                noise_z = math.sin(t * (random.uniform(2, 6)) + s) * 0.5
                
                # Jiggling path calculation
                nx, ny, nz = project(ox+noise_x, oy+noise_y, oz+noise_z, cam_angle, cam_tilt, scale)
                sprout_a = int(120 * phase_sprout * (random.uniform(0.2, 1.0)))
                draw.line([(px_top, py_top), (nx, ny)], fill=(150, 160, 170, sprout_a), width=1)
                draw.line([(nx, ny), (px_bot, py_bot)], fill=(150, 160, 170, sprout_a), width=1)

    # 4. DRAW DEPTH SORTED NODES
    rendered_elements.sort(key=lambda x: x[0], reverse=True)
    
    for el in rendered_elements:
        if el[1] == 'node':
            cx, cy = el[2]
            rgb = el[3]
            a = el[4]
            r = el[5]
            draw_glowing_dot(draw, cx, cy, r, rgb, int(255 * a))
        elif el[1] == 'particle':
            cx, cy = el[2]
            rgb = el[3]
            a = el[4]
            draw.ellipse([(cx-2, cy-2), (cx+2, cy+2)], fill=(rgb[0], rgb[1], rgb[2], int(255 * a)))

    # 5. TYPOGRAPHY & UI LOGIC
    text_c = (20, 25, 30, 255)
    
    if t < 8.0:
        draw_text_with_outline(draw, (50, 150), "PHASE 1: CELL DEATH", font_h1, (30, 50, 140, 255))
        draw_text_with_outline(draw, (50, 220), "Primary circuit suffers catastrophic failure.", font_h2, text_c)
        draw_text_with_outline(draw, (50, 270), "Signal propagation collapses entirely.", font_h2, text_c)
    elif 8.0 <= t < 16.0:
        draw_text_with_outline(draw, (50, 150), "PHASE 2: COLLATERAL SPROUTING", font_h1, (130, 140, 150, 255))
        draw_text_with_outline(draw, (50, 220), "Intact neurons aggressively branch outward.", font_h2, text_c)
        draw_text_with_outline(draw, (50, 270), "A chaotic, energy-dense search for silent synapses.", font_h2, text_c)
    elif 16.0 <= t < 24.0:
        draw_text_with_outline(draw, (50, 150), "PHASE 3: HEBBIAN PLASTICITY", font_h1, (190, 20, 40, 255))
        draw_text_with_outline(draw, (50, 220), "A functional detour pathway is discovered.", font_h2, text_c)
        draw_text_with_outline(draw, (50, 270), "Dopaminergic gating structurally welds it in place.", font_h2, text_c)
    elif t >= 24.0:
        draw_text_with_outline(draw, (50, 150), "PHASE 4: SYNAPTIC PRUNING", font_h1, (80, 40, 140, 255))
        draw_text_with_outline(draw, (50, 220), "Microglia digest the chaotic, unused noise.", font_h2, text_c)
        draw_text_with_outline(draw, (50, 270), "Deep-sleep solidifies the new baseline matrix.", font_h2, text_c)

    draw.line([(50, HEIGHT-100), (WIDTH-50, HEIGHT-100)], fill=(200, 205, 210, 180), width=3)
    
    # Progress UI Bar
    line_w = (WIDTH - 100) * loop_progress
    bar_c = (190, 20, 40, 255) if phase_hebbian > 0.5 else (150, 160, 170, 255)
    draw.line([(50, HEIGHT-100), (50 + line_w, HEIGHT-100)], fill=bar_c, width=4)
    
    draw_text_with_outline(draw, (50, HEIGHT-80), "STRUCTURE: NEURAL MATRIX", font_h2, (120, 130, 140, 255))
    draw_text_with_outline(draw, (WIDTH-480, HEIGHT-80), "TARGET: PLASTIC REGENERATION", font_h2, (120, 130, 140, 255))

    img.paste(overlay, (0, 0), overlay)
    img.save(f"frames/frame_{f:04d}.png")
    
    if f % 150 == 0:
        print(f"Processed {f}/{TOTAL_FRAMES} frames...")

print("Rendering neuroplasticity video via FFmpeg...")
os.system("ffmpeg -y -framerate 60 -i frames/frame_%04d.png -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p LG-468_Neuroplastic_Regeneration.mp4")
print("Render complete: LG-468_Neuroplastic_Regeneration.mp4")
