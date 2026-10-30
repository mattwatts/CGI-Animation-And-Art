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

def draw_solid_dot(draw, x, y, radius, colour):
    draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], fill=(colour[0], colour[1], colour[2], colour[3]))

def smoothstep(edge0, edge1, x):
    t = max(0.0, min(1.0, (x - edge0) / (edge1 - edge0)))
    return t * t * (3.0 - 2.0 * t)

# -------------------------
# STRUCTURAL MATRIX MATRICES
# -------------------------
print("Generating exact thermodynamic resonance matrix for LG-469...")

NUM_NODES = 300
R_CRYSTAL = 6.0
R_AMBIENT = 14.0

nodes_ambient = []
nodes_collapsed = []

# Generate Collapsed Matrix: A mathematically perfect Fibonacci Sphere (The 'Mind Crystal')
phi_golden = math.pi * (3.0 - math.sqrt(5.0))
for i in range(NUM_NODES):
    y = 1.0 - (i / float(NUM_NODES - 1)) * 2.0
    radius = math.sqrt(1.0 - y * y)
    theta = phi_golden * i
    
    cx = math.cos(theta) * radius * R_CRYSTAL
    cy = y * R_CRYSTAL
    cz = math.sin(theta) * radius * R_CRYSTAL
    nodes_collapsed.append((cx, cy, cz))

# Generate Ambient Field Matrix: A wide, high-entropy cylindrical wave
for i in range(NUM_NODES):
    ang = (i / float(NUM_NODES)) * math.pi * 18.0  
    rad = R_AMBIENT + math.sin(i * 0.1) * 2.0
    hgt = (i - (NUM_NODES/2.0)) * 0.15
    
    ax = math.cos(ang) * rad
    ay = hgt
    az = math.sin(ang) * rad
    nodes_ambient.append((ax, ay, az))

# Pre-calculate crystal edges (Only connect nodes that are physically adjacent)
# This provides the highly rigid structural detail during collapse.
crystal_edges = []
edge_distance_threshold = 2.4
for i in range(NUM_NODES):
    for j in range(i + 1, NUM_NODES):
        dx = nodes_collapsed[i][0] - nodes_collapsed[j][0]
        dy = nodes_collapsed[i][1] - nodes_collapsed[j][1]
        dz = nodes_collapsed[i][2] - nodes_collapsed[j][2]
        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        if dist < edge_distance_threshold:
            crystal_edges.append((i, j))

# -------------------------
# MAIN RENDER LOOP
# -------------------------
for f in range(TOTAL_FRAMES):
    t = f / FPS
    loop_progress = f / TOTAL_FRAMES
    
    # 32 Second Master Phases:
    # 0s - 8s   : Ambient Timespace Field
    # 8s - 16s  : Topological Resonance (Drawing inward)
    # 16s - 24s : Locality Collapse (Rigid Crystal forms)
    # 24s - 32s : Dissolution to Baseline
    
    phase_resonate = smoothstep(6.0, 14.0, t)
    phase_release  = smoothstep(22.0, 30.0, t)
    
    # Structural state (0.0 = Pure Ambient Field, 1.0 = Pure Rigid Collapse)
    collapse_factor = phase_resonate - phase_release
    
    # Camera maintains an intricate, slow sweeping observation
    cam_angle = loop_progress * 2 * math.pi * 2.0 
    cam_tilt = 0.30 + (math.sin(loop_progress * 2 * math.pi) * 0.15)
    
    img = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))
    overlay = Image.new('RGBA', (WIDTH, HEIGHT), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    scale = 135
    
    # Current positions array for this exact frame
    rendered_elements = []
    current_coords = []
    
    # Interpolate physics for all 300 nodes
    for i in range(NUM_NODES):
        ax, ay, az = nodes_ambient[i]
        cx, cy, cz = nodes_collapsed[i]
        
        # The ambient field is not static; it flows like a fluid using timespace wave maths
        wave_offset_y = math.sin(t * 3.0 + i * 0.1) * 1.5
        wave_offset_x = math.cos(t * 2.0 + i * 0.05) * 1.0
        
        current_ax = ax + wave_offset_x
        current_ay = ay + wave_offset_y
        current_az = az
        
        # Calculate current real-world coordinate based on the collapse factor
        mx = current_ax * (1.0 - collapse_factor) + cx * collapse_factor
        my = current_ay * (1.0 - collapse_factor) + cy * collapse_factor
        mz = current_az * (1.0 - collapse_factor) + cz * collapse_factor
        
        px, py, pz = project(mx, my, mz, cam_angle, cam_tilt, scale)
        current_coords.append((px, py))
        
        # Dynamic high-contrast colours
        # Ambient: Deep Navy (20, 40, 140). Collapsed: Stark Crimson (190, 20, 30).
        r_col = int(20 + (190 - 20) * collapse_factor)
        g_col = int(40 + (20 - 40) * collapse_factor)
        b_col = int(140 + (30 - 140) * collapse_factor)
        
        # Nodes scale up in physical size and contrast as they collapse
        node_radius = 4 + (collapse_factor * 6)
        alpha = 150 + int(105 * collapse_factor) # Never invisible. High contrast baseline.
        
        rendered_elements.append((pz, 'node', (px, py), (r_col, g_col, b_col, alpha), node_radius))
        
    # Draw Field Geometry and Interlocking Crystal Cages
    bond_alpha = int(255 * collapse_factor)
    if bond_alpha > 5:
        # Drawing the exact rigid structure established upon locality collapse
        bond_colour = (190, 20, 30, bond_alpha)
        bond_thick = max(1, int(4 * collapse_factor))
        
        for (i, j) in crystal_edges:
            # Depth sort line segments roughly based on the first node to maintain realism
            dz = rendered_elements[i][0]
            rendered_elements.append((dz, 'bond', (current_coords[i], current_coords[j]), bond_colour, bond_thick))

    # Render Depth-Sorted 3D Elements
    rendered_elements.sort(key=lambda x: x[0], reverse=True)
    
    for el in rendered_elements:
        if el[1] == 'node':
            cx, cy = el[2]
            rgb = el[3]
            rad = el[4]
            draw_solid_dot(draw, cx, cy, rad, rgb)
        elif el[1] == 'bond':
            pts = el[2]
            rgb = el[3]
            thick = el[4]
            draw.line([pts[0], pts[1]], fill=rgb, width=thick)

    # -------------------------
    # HIGH-CONTRAST TYPOGRAPHY & UI LOGIC
    # -------------------------
    text_c = (20, 25, 30, 255)
    
    if t < 8.0:
        draw_text_with_outline(draw, (50, 150), "PHASE 1: THE AMBIENT FIELD", font_h1, (20, 40, 140, 255))
        draw_text_with_outline(draw, (50, 220), "Timespace exists as an unstructured, fluid medium.", font_h2, text_c)
        draw_text_with_outline(draw, (50, 270), "Raw potential flows without boundaries.", font_h2, text_c)
    elif 8.0 <= t < 16.0:
        draw_text_with_outline(draw, (50, 150), "PHASE 2: TOPOLOGICAL RESONANCE", font_h1, (100, 30, 80, 255))
        draw_text_with_outline(draw, (50, 220), "The physical locality begins to exert drag.", font_h2, text_c)
        draw_text_with_outline(draw, (50, 270), "The ambient grid is drawn into a standing wave.", font_h2, text_c)
    elif 16.0 <= t < 24.0:
        draw_text_with_outline(draw, (50, 150), "PHASE 3: LOCALITY COLLAPSE", font_h1, (190, 20, 30, 255))
        draw_text_with_outline(draw, (50, 220), "The surrounding field snaps onto the central coordinate.", font_h2, text_c)
        draw_text_with_outline(draw, (50, 270), "Consciousness forms exactly here. A locked, rigid state.", font_h2, text_c)
    elif t >= 24.0:
        draw_text_with_outline(draw, (50, 150), "PHASE 4: DISSOLUTION", font_h1, (80, 30, 80, 255))
        draw_text_with_outline(draw, (50, 220), "The locality releases its structural hold.", font_h2, text_c)
        draw_text_with_outline(draw, (50, 270), "The locked energy simply melts back into the baseline.", font_h2, text_c)

    draw.line([(50, HEIGHT-100), (WIDTH-50, HEIGHT-100)], fill=(120, 130, 140, 255), width=4)
    
    # Progress UI Bar
    line_w = (WIDTH - 100) * loop_progress
    bar_c = (190, 20, 30, 255) if collapse_factor > 0.5 else (20, 40, 140, 255)
    draw.line([(50, HEIGHT-100), (50 + line_w, HEIGHT-100)], fill=bar_c, width=8)
    
    draw_text_with_outline(draw, (50, HEIGHT-80), "STRUCTURE: TIMESPACE MATRIX", font_h2, (60, 70, 80, 255))
    draw_text_with_outline(draw, (WIDTH-480, HEIGHT-80), "TARGET: FIELD RESONANCE", font_h2, (60, 70, 80, 255))

    img.paste(overlay, (0, 0), overlay)
    img.save(f"frames/frame_{f:04d}.png")
    
    if f % 150 == 0:
        print(f"Processed {f}/{TOTAL_FRAMES} frames...")

print("Rendering high-contrast field collapse video via FFmpeg...")
os.system("ffmpeg -y -framerate 60 -i frames/frame_%04d.png -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p LG-469_Field_Collapse.mp4")
print("Render complete: LG-469_Field_Collapse.mp4")
