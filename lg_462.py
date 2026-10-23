import os
import math
from PIL import Image, ImageDraw

WIDTH = 1080
HEIGHT = 1920
FPS = 60
DURATION = 15
TOTAL_FRAMES = FPS * DURATION

os.makedirs("frames", exist_ok=True)

VERTEX_X, VERTEX_Y = 540, 1600
TARGET_X, TARGET_Y = 540, 600

def ease_in_out(t):
    return t * t * (3 - 2 * t)

def draw_glowing_circle(draw, x, y, radius, colour, max_alpha=255):
    layers = 12
    for i in range(layers):
        r = radius * (1 - (i / layers))
        alpha = int(max_alpha * (i / layers))
        draw.ellipse(
            [(x - r, y - r), (x + r, y + r)],
            fill=(colour[0], colour[1], colour[2], alpha)
        )

print("Starting generation...")

for f in range(TOTAL_FRAMES):
    t = f / TOTAL_FRAMES
    
    # Timeline
    vertex_alpha = min(255, int((t / 0.05) * 255)) if t < 0.05 else 255
    cone_progress = ease_in_out(max(0, min(1, (t - 0.05) / 0.15)))
    beam_progress = ease_in_out(max(0, min(1, (t - 0.20) / 0.15)))
    mass_progress = ease_in_out(max(0, min(1, (t - 0.35) / 0.20)))
    decay_progress = ease_in_out(max(0, min(1, (t - 0.85) / 0.15)))
    
    current_mass = mass_progress * (1 - decay_progress)
    gravity_strength = current_mass * 350  
    
    img = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))
    overlay = Image.new('RGBA', (WIDTH, HEIGHT), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    
    max_distance = 1800
    current_max_dist = max_distance * cone_progress
    
    # 1. The Expanding Horizon (Cone)
    angles = 50
    for i in range(angles):
        angle_deg = -155 + (130 * i / (angles - 1))
        rad = math.radians(angle_deg)
        
        steps = 100
        path = []
        for j in range(steps + 1):
            dist = current_max_dist * (j / steps)
            px = VERTEX_X + math.cos(rad) * dist
            py = VERTEX_Y + math.sin(rad) * dist
            
            dx = px - TARGET_X
            dy = py - TARGET_Y
            d = math.hypot(dx, dy)
            if d > 0.1:
                pull = gravity_strength / (1 + d/50)
                pull = min(pull, d * 0.85)
                px -= (dx/d) * pull
                py -= (dy/d) * pull
                
            path.append((px, py))
            
        if len(path) > 1:
            line_alpha = int(120 * (1 - decay_progress * 0.9))
            draw.line(path, fill=(160, 180, 190, line_alpha), width=2)
            
    rings = 40
    for i in range(1, rings + 1):
        dist = current_max_dist * (i / rings)
        path = []
        for a in range(121):
            angle_deg = -155 + (130 * a / 120)
            rad = math.radians(angle_deg)
            px = VERTEX_X + math.cos(rad) * dist
            py = VERTEX_Y + math.sin(rad) * dist
            
            dx = px - TARGET_X
            dy = py - TARGET_Y
            d = math.hypot(dx, dy)
            if d > 0.1:
                pull = gravity_strength / (1 + d/50)
                pull = min(pull, d * 0.85)
                px -= (dx/d) * pull
                py -= (dy/d) * pull
                
            path.append((px, py))
            
        if len(path) > 1:
            ring_alpha = int(90 * (1 - decay_progress * 0.9))
            draw.line(path, fill=(190, 200, 210, ring_alpha), width=2)
            
    # 2. Directed Vector (Beam)
    if beam_progress > 0:
        bx = VERTEX_X + (TARGET_X - VERTEX_X) * beam_progress
        by = VERTEX_Y + (TARGET_Y - VERTEX_Y) * beam_progress
        beam_alpha = int(255 * (1 - decay_progress))
        draw.line([(VERTEX_X, VERTEX_Y), (bx, by)], fill=(15, 30, 70, beam_alpha), width=4)
        draw.line([(VERTEX_X, VERTEX_Y), (bx, by)], fill=(30, 60, 120, beam_alpha // 2), width=10)

    # 3. Observation Mass (Gravity Well)
    if current_mass > 0:
        pulse = 1.0 + (0.05 * math.sin(t * math.pi * 15))
        mass_radius = 50 * pulse * current_mass
        draw_glowing_circle(draw, TARGET_X, TARGET_Y, mass_radius, (10, 20, 60), int(220 * current_mass))
        
    # 4. The Vertex
    draw_glowing_circle(draw, VERTEX_X, VERTEX_Y, 20, (0, 0, 0), vertex_alpha)

    img.paste(overlay, (0, 0), overlay)
    
    img.save(f"frames/frame_{f:04d}.png")
    if f % 120 == 0:
        print(f"{f}/{TOTAL_FRAMES} frames processed")

print("Executing FFmpeg...")
os.system("ffmpeg -y -framerate 60 -i frames/frame_%04d.png -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p LG-462_Mental_Projection.mp4")
