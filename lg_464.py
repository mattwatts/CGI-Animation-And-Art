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

CENTER_X = 540
CENTER_Y = 1050

# -------------------------
# TYPOGRAPHY ENGINE
# -------------------------
def get_font(size):
    font_paths = [
        "arial.ttf", 
        "Arial.ttf",
        "/Library/Fonts/Arial.ttf", 
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:\\Windows\\Fonts\\arial.ttf"
    ]
    for path in font_paths:
        try:
            return ImageFont.truetype(path, size)
        except IOError:
            continue
    return ImageFont.load_default()

font_h1 = get_font(52)
font_h2 = get_font(42)

def draw_text_with_outline(draw, position, text, font, text_colour, outline_colour=(255, 255, 255, 240), thickness=3):
    x, y = position
    # Draw outline for maximum contrast on intersecting geometry
    for dx in range(-thickness, thickness + 1):
        for dy in range(-thickness, thickness + 1):
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_colour)
    # Draw core text
    draw.text((x, y), text, font=font, fill=text_colour)

# -------------------------
# GEOMETRY ENGINE
# -------------------------
def ease_in_out(t):
    if t <= 0: return 0
    if t >= 1: return 1
    return t * t * (3 - 2 * t)

# Pre-calculate the exact mathematical nodes
NUM_NODES = 800
GOLDEN_ANGLE = 137.5077640500378546463487 * (math.pi / 180.0)
C_SCALE = 18.0 # Spread of the logic lattice

nodes = []
for i in range(NUM_NODES):
    r = C_SCALE * math.sqrt(i)
    theta = i * GOLDEN_ANGLE
    x = CENTER_X + r * math.cos(theta)
    y = CENTER_Y + r * math.sin(theta)
    nodes.append((x, y))

# -------------------------
# RENDER LOOP
# -------------------------
print("Generating exact geometric frames for LG-464...")

for f in range(TOTAL_FRAMES):
    t = f / TOTAL_FRAMES
    
    # Mathematical Timing Sequences
    seq_progress = min(1.0, t / 0.40)                     # Step-by-step logic build (0 to 40%)
    phase_shift_progress = ease_in_out(max(0, min(1, (t - 0.50) / 0.15)))  # The Phase Transition (50% to 65%)
    rotation = t * math.pi * 0.5                          # Gentle global perspective rotation
    
    # Calculate how many nodes are active in the causal chain right now
    active_nodes = int(seq_progress * NUM_NODES)
    if active_nodes < 1: active_nodes = 1
    
    img = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))
    overlay = Image.new('RGBA', (WIDTH, HEIGHT), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    
    # -------------------------
    # TYPOGRAPHY LAYER
    # -------------------------
    title_colour = (12, 18, 30, 255)
    accent_colour = (20, 100, 160, 255)
    shift_colour = (180, 40, 40, int(255 * phase_shift_progress))
    
    if t < 0.20:
        draw_text_with_outline(draw, (70, 150), "Intelligence is an output.\nNot magic.", font_h1, title_colour)
    elif 0.20 <= t < 0.45:
        draw_text_with_outline(draw, (70, 150), "It begins with step-by-step logic.", font_h1, title_colour)
        draw_text_with_outline(draw, (70, 280), "A rigid, unbroken causal chain.", font_h2, (60, 70, 80, 255))
    elif 0.45 <= t < 0.65:
        draw_text_with_outline(draw, (70, 150), "When steps scale into the thousands...", font_h1, title_colour)
        draw_text_with_outline(draw, (70, 230), "A Phase Transition triggers.", font_h1, shift_colour)
    elif t >= 0.65:
        draw_text_with_outline(draw, (70, 150), "EMERGENT PROPERTY", font_h1, title_colour)
        draw_text_with_outline(draw, (70, 230), "The macro-structure possesses order\nthat the individual parts lack.", font_h2, accent_colour)
        # The Friction Warning:
        draw_text_with_outline(draw, (70, HEIGHT - 180), "If one early step fails,\nthe entire lattice collapses.", font_h2, (180, 40, 40, 255))

    # -------------------------
    # RENDER CAUSAL CHAIN
    # -------------------------
    # Draw the baseline sequential steps (1 -> 2 -> 3...)
    # This represents standard linear maths/logic
    chain_path = []
    for i in range(active_nodes):
        rx, ry = nodes[i]
        
        # Apply slow rotation from center to give it life
        dx = rx - CENTER_X
        dy = ry - CENTER_Y
        rot_x = CENTER_X + dx * math.cos(rotation) - dy * math.sin(rotation)
        rot_y = CENTER_Y + dx * math.sin(rotation) + dy * math.cos(rotation)
        
        chain_path.append((rot_x, rot_y))
        
        # Individual logic node
        r_node = 4
        # Nodes get slightly brighter/thicker during the phase shift
        alpha_node = 150 + int(105 * phase_shift_progress)
        draw.ellipse([(rot_x - r_node, rot_y - r_node), (rot_x + r_node, rot_y + r_node)], fill=(30, 40, 50, alpha_node))

    # Draw the rigid causal chain (the O(N) linear sequence)
    if len(chain_path) > 1:
        draw.line(chain_path, fill=(40, 50, 70, 160), width=2)
        
    # -------------------------
    # RENDER THE PHASE TRANSITION
    # -------------------------
    # The magical emergence: Cross-connecting nodes separated by Fibonacci distances (21, 34).
    # When N reaches a threshold, these distant points naturally align, creating a breathtaking lattice.
    if phase_shift_progress > 0:
        emergent_alpha = int(140 * phase_shift_progress)
        emergent_width = 1 + int(2 * phase_shift_progress)
        
        for i in range(active_nodes):
            current_pt = chain_path[i]
            
            # Fibonacci link 34
            if i >= 34:
                link_pt = chain_path[i - 34]
                draw.line([current_pt, link_pt], fill=(20, 110, 180, emergent_alpha), width=emergent_width)
            
            # Fibonacci link 55
            if i >= 55:
                link_pt = chain_path[i - 55]
                draw.line([current_pt, link_pt], fill=(40, 140, 160, int(emergent_alpha * 0.7)), width=emergent_width)

    # Composite and save frame
    img.paste(overlay, (0, 0), overlay)
    img.save(f"frames/frame_{f:04d}.png")
    
    if f % 150 == 0:
        print(f"Processed {f}/{TOTAL_FRAMES} frames...")

print("Rendering video via FFmpeg...")
os.system("ffmpeg -y -framerate 60 -i frames/frame_%04d.png -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p LG-464_Emergent_Properties.mp4")
print("Render complete: LG-464_Emergent_Properties.mp4")
