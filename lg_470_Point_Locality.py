import os
import math
from PIL import Image, ImageDraw, ImageFont

# -------------------------
# CONFIGURATION 
# -------------------------
WIDTH = 1080
HEIGHT = 1920
FPS = 60
DURATION = 32  # 32-second seamless continuous loop
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
# 3D CAMERA & PROJECTION
# -------------------------
def project(x, y, z, cam_angle_rad, tilt_rad, scale, offset_x=WIDTH/2, offset_y=HEIGHT/2 + 20):
    # Standard Y-axis rotation (Pan)
    x_rot = x * math.cos(cam_angle_rad) - z * math.sin(cam_angle_rad)
    z_rot = x * math.sin(cam_angle_rad) + z * math.cos(cam_angle_rad)
    
    # Standard X-axis rotation (Tilt)
    y_rot = y * math.cos(tilt_rad) - z_rot * math.sin(tilt_rad)
    
    px = offset_x + (x_rot * scale)
    py = offset_y - (y_rot * scale)
    return px, py, z_rot

def smoothstep(edge0, edge1, x):
    t = max(0.0, min(1.0, (x - edge0) / (edge1 - edge0)))
    return t * t * (3.0 - 2.0 * t)

# -------------------------
# POLAR GRID MATRIX (THE FIELD)
# -------------------------
print("Generating exact Point Locality geometric matrix for LG-470...")

RINGS = 24
SPOKES = 48
MAX_RADIUS = 18.0

# -------------------------
# MAIN RENDER LOOP
# -------------------------
for f in range(TOTAL_FRAMES):
    t = f / FPS
    loop_progress = f / TOTAL_FRAMES
    
    # 32 Second Master Phases:
    # 0s - 8s   : Flat baseline field
    # 8s - 16s  : Topological Drag (The point asserts tension)
    # 16s - 24s : Absolute Zero-Point Collapse (Data is trapped at coordinate 0,0,0)
    # 24s - 32s : Ripple and Dissolution to baseline
    
    phase_drag = smoothstep(6.0, 14.0, t)
    phase_release = smoothstep(22.0, 28.0, t)
    
    # Collapse State: 0.0 is flat field, 1.0 is absolute singularity compression
    collapse_factor = phase_drag - phase_release
    
    # The camera performs a slow, highly controlled orbital pan
    cam_angle = loop_progress * 2 * math.pi * 1.5 
    cam_tilt = 0.35 + (math.sin(loop_progress * 2 * math.pi) * 0.10)
    
    img = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))
    overlay = Image.new('RGBA', (WIDTH, HEIGHT), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    scale = 140
    
    current_nodes = {}
    
    # Calculate physical distortion for every coordinate in the polar grid
    for r_idx in range(1, RINGS + 1):
        base_r = (r_idx / float(RINGS)) * MAX_RADIUS
        
        # Exponential curve: The center is sucked in violently, the edges remain anchored
        influence = math.exp(-base_r * 0.25)
        
        # At collapse_factor 1.0, the inner rings are completely crushed to r=0
        r_current = base_r * (1.0 - (influence * collapse_factor * 0.95))
        
        # The timespace field dips physically downward into the center (a gravity well)
        y_current = - (influence * collapse_factor * 8.0)
        
        # Add subtle ambient wave motion to the baseline field
        wave_y = math.sin((r_idx * 0.5) - (t * 2.0)) * 0.2 * (1.0 - collapse_factor)
        
        for s_idx in range(SPOKES):
            theta = (s_idx / float(SPOKES)) * 2 * math.pi
            
            x = math.cos(theta) * r_current
            z = math.sin(theta) * r_current
            y = y_current + wave_y
            
            px, py, pz = project(x, y, z, cam_angle, cam_tilt, scale)
            current_nodes[(r_idx, s_idx)] = (px, py, pz)

    # -------------------------
    # RENDER GRID EDGES (HIGH CONTRAST)
    # -------------------------
    # Field baseline is Deep Navy. As it compresses, it shifts to stark Crimson.
    c_r = int(20 + (170 * collapse_factor))
    c_g = int(40 - (20 * collapse_factor))
    c_b = int(140 - (110 * collapse_factor))
    
    # Render Rings
    for r_idx in range(1, RINGS + 1):
        for s_idx in range(SPOKES):
            p1 = current_nodes[(r_idx, s_idx)]
            p2 = current_nodes[(r_idx, (s_idx + 1) % SPOKES)]
            
            # Line thickness increases slightly towards the compressed center
            line_a = max(20, int(255 * (1.0 - (r_idx / (RINGS + 2.0)))))
            thick = max(1, min(4, int(4 - (r_idx * 0.15) + (collapse_factor * 2))))
            draw.line([p1[:2], p2[:2]], fill=(c_r, c_g, c_b, line_a), width=thick)

    # Render Spokes
    for s_idx in range(SPOKES):
        for r_idx in range(1, RINGS):
            p1 = current_nodes[(r_idx, s_idx)]
            p2 = current_nodes[(r_idx + 1, s_idx)]
            
            line_a = max(20, int(255 * (1.0 - (r_idx / (RINGS + 2.0)))))
            thick = max(1, min(3, int(3 - (r_idx * 0.1))))
            draw.line([p1[:2], p2[:2]], fill=(c_r, c_g, c_b, line_a), width=thick)

    # -------------------------
    # THE POINT LOCALITY (THE SINGULARITY)
    # -------------------------
    # At the absolute center (0,0,0), a single ultra-dense geometrical point flares up
    point_y = - (collapse_factor * 8.0)
    c_x, c_y, c_z = project(0, point_y, 0, cam_angle, cam_tilt, scale)
    
    point_alpha = int(255 * collapse_factor)
    if point_alpha > 0:
        radius = 5 + (collapse_factor * 12)
        # Inner Core (Stark White)
        draw.ellipse([(c_x - radius, c_y - radius), (c_x + radius, c_y + radius)], fill=(190, 20, 30, point_alpha))
        draw.ellipse([(c_x - radius*0.3, c_y - radius*0.3), (c_x + radius*0.3, c_y + radius*0.3)], fill=(255, 255, 255, point_alpha))
        
        # A rigid vertical transmission line representing the exact locality axis
        ax_top_px, ax_top_py, _ = project(0, point_y + 12.0, 0, cam_angle, cam_tilt, scale)
        ax_bot_px, ax_bot_py, _ = project(0, point_y - 12.0, 0, cam_angle, cam_tilt, scale)
        draw.line([(ax_top_px, ax_top_py), (ax_bot_px, ax_bot_py)], fill=(190, 20, 30, int(point_alpha*0.6)), width=2)

    # -------------------------
    # TYPOGRAPHY & UI LOGIC
    # -------------------------
    text_c = (20, 25, 30, 255)
    
    if t < 8.0:
        draw_text_with_outline(draw, (50, 150), "PHASE 1: THE FIELD", font_h1, (20, 40, 140, 255))
        draw_text_with_outline(draw, (50, 220), "Spacetime potential is evenly distributed.", font_h2, text_c)
        draw_text_with_outline(draw, (50, 270), "No specific coordinate holds structural data.", font_h2, text_c)
    elif 8.0 <= t < 16.0:
        draw_text_with_outline(draw, (50, 150), "PHASE 2: TOPOLOGICAL DRAG", font_h1, (100, 30, 80, 255))
        draw_text_with_outline(draw, (50, 220), "A single locality asserts intense physical tension.", font_h2, text_c)
        draw_text_with_outline(draw, (50, 270), "The ambient grid is drawn heavily inward.", font_h2, text_c)
    elif 16.0 <= t < 24.0:
        draw_text_with_outline(draw, (50, 150), "PHASE 3: POINT LOCALITY COLLAPSE", font_h1, (190, 20, 30, 255))
        draw_text_with_outline(draw, (50, 220), "Total geometric compression into a zero-dimensional coordinate.", font_h2, text_c)
        draw_text_with_outline(draw, (50, 270), "Consciousness forms tightly at coordinate exactness.", font_h2, text_c)
    elif t >= 24.0:
        draw_text_with_outline(draw, (50, 150), "PHASE 4: DISSOLUTION RIPPLE", font_h1, (80, 30, 80, 255))
        draw_text_with_outline(draw, (50, 220), "The tension is physically released.", font_h2, text_c)
        draw_text_with_outline(draw, (50, 270), "The exact coordinate releases potential back to the baseline.", font_h2, text_c)

    draw.line([(50, HEIGHT-100), (WIDTH-50, HEIGHT-100)], fill=(120, 130, 140, 255), width=4)
    
    line_w = (WIDTH - 100) * loop_progress
    bar_c = (190, 20, 30, 255) if collapse_factor > 0.5 else (20, 40, 140, 255)
    draw.line([(50, HEIGHT-100), (50 + line_w, HEIGHT-100)], fill=bar_c, width=8)
    
    draw_text_with_outline(draw, (50, HEIGHT-80), "STRUCTURE: POLAR TENSION MESH", font_h2, (60, 70, 80, 255))
    draw_text_with_outline(draw, (WIDTH-480, HEIGHT-80), "TARGET: POINT LOCALITY", font_h2, (60, 70, 80, 255))

    img.paste(overlay, (0, 0), overlay)
    img.save(f"frames/frame_{f:04d}.png")
    
    if f % 150 == 0:
        print(f"Processed {f}/{TOTAL_FRAMES} frames...")

print("Rendering high-contrast Point Locality sequence via FFmpeg...")
os.system("ffmpeg -y -framerate 60 -i frames/frame_%04d.png -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p LG-470_Point_Locality.mp4")
print("Render complete: LG-470_Point_Locality.mp4")
