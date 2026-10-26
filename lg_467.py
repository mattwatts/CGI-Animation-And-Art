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
def project(x, y, z, cam_angle_rad, tilt_rad, scale, offset_x=WIDTH/2, offset_y=HEIGHT/2 + 50):
    # Pan (Y axis rotation)
    x_rot = x * math.cos(cam_angle_rad) - z * math.sin(cam_angle_rad)
    z_rot = x * math.sin(cam_angle_rad) + z * math.cos(cam_angle_rad)
    
    # Tilt (X axis rotation)
    y_rot = y * math.cos(tilt_rad) - z_rot * math.sin(tilt_rad)
    
    # Projection
    px = offset_x + (x_rot * scale)
    py = offset_y - (y_rot * scale)
    return px, py, z_rot

def draw_glowing_dot(draw, x, y, radius, colour, max_alpha=255):
    layers = 5
    for i in range(layers):
        r = radius * (1 - (i / layers))
        alpha = int(max_alpha * (i / layers))
        draw.ellipse([(x - r, y - r), (x + r, y + r)], fill=(colour[0], colour[1], colour[2], alpha))

# -------------------------
# DODECAHEDRON CRYSTAL MAP
# -------------------------
PHI = (1 + math.sqrt(5)) / 2
INV_PHI = 1 / PHI
RADIUS = 4.0

# Base coordinates normalized to unit sphere
base_vertices = [
    (1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1),
    (-1, 1, 1), (-1, 1, -1), (-1, -1, 1), (-1, -1, -1),
    (0, PHI, INV_PHI), (0, PHI, -INV_PHI),
    (0, -PHI, INV_PHI), (0, -PHI, -INV_PHI),
    (INV_PHI, 0, PHI), (-INV_PHI, 0, PHI),
    (INV_PHI, 0, -PHI), (-INV_PHI, 0, -PHI),
    (PHI, INV_PHI, 0), (PHI, -INV_PHI, 0),
    (-PHI, INV_PHI, 0), (-PHI, -INV_PHI, 0)
]

# Scale vertices radially
vertices = []
for v in base_vertices:
    norm = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    vertices.append((v[0]/norm * RADIUS, v[1]/norm * RADIUS, v[2]/norm * RADIUS))

# Determine edges (connected vertices) based on exact geometric distance
edges = []
edge_threshold = (2.0 / PHI / math.sqrt(3)) * RADIUS * 1.1 
for i in range(len(vertices)):
    for j in range(i + 1, len(vertices)):
        d = math.sqrt(sum((vertices[i][k] - vertices[j][k])**2 for k in range(3)))
        if d < edge_threshold:
            edges.append((i, j))

# Generate seamless deterministic noise for Phase Decomposition
# Integer frequencies ensure exact spatial matching at t=0s and t=32s
random.seed(467)
noise_params = []
for _ in range(len(vertices)):
    freq_x = random.randint(2, 6)
    freq_y = random.randint(2, 6)
    freq_z = random.randint(2, 6)
    phase_x = random.uniform(0, 2*math.pi)
    phase_y = random.uniform(0, 2*math.pi)
    phase_z = random.uniform(0, 2*math.pi)
    noise_params.append((freq_x, freq_y, freq_z, phase_x, phase_y, phase_z))

# -------------------------
# RENDER LOOP
# -------------------------
print("Generating thermodynamic crystal cycle for LG-467...")

MAX_SCATTER = 5.5

for f in range(TOTAL_FRAMES):
    t = f / FPS
    loop_progress = f / TOTAL_FRAMES
    
    # CRYSTAL INTEGRITY CURVE
    # mathematical sine curve mapped over 32s.
    # Power of 6 creates a slow chaotic build, a sharp snap, and a violent drop.
    crystal_integrity = math.sin(loop_progress * math.pi) ** 6
    chaos = 1.0 - crystal_integrity
    
    # Camera gently orbits the single locality over the full 32 seconds
    cam_angle = loop_progress * 2 * math.pi * 2  # 2 full rotations
    cam_tilt = 0.25 + (math.sin(loop_progress * 2 * math.pi) * 0.1)
    
    img = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))
    overlay = Image.new('RGBA', (WIDTH, HEIGHT), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    
    scale = 135
    
    # 1. THE LOCALITY BOUNDARY (Sphere denoting the frontal lobe boundary)
    # Always completely visible to provide high-contrast baseline structure
    border_pts = 60
    for p in range(border_pts):
        ang_1 = (p / border_pts) * 2 * math.pi
        ang_2 = ((p + 1) / border_pts) * 2 * math.pi
        
        c1x, c1y, c1z = project(math.cos(ang_1)*RADIUS*1.5, 0, math.sin(ang_1)*RADIUS*1.5, cam_angle, cam_tilt, scale)
        c2x, c2y, c2z = project(math.cos(ang_2)*RADIUS*1.5, 0, math.sin(ang_2)*RADIUS*1.5, cam_angle, cam_tilt, scale)
        # Faint meridian ring
        draw.line([(c1x, c1y), (c2x, c2y)], fill=(120, 130, 140, 40), width=1)
    
    rendered_nodes = []
    current_positions = []
    
    # 2. CALCULATE PARTICLE PHYSICS
    for i, v in enumerate(vertices):
        nx, ny, nz, px, py, pz = noise_params[i]
        
        # Calculate seamless harmonic scattered positions
        time_angle = loop_progress * 2 * math.pi
        ox = math.sin(time_angle * nx + px) * MAX_SCATTER * chaos
        oy = math.cos(time_angle * ny + py) * MAX_SCATTER * chaos
        oz = math.sin(time_angle * nz + pz) * MAX_SCATTER * chaos
        
        # Current physical location interpolates from chaos to ideal vertex
        vx = v[0] + ox
        vy = v[1] + oy
        vz = v[2] + oz
        
        rx, ry, rz = project(vx, vy, vz, cam_angle, cam_tilt, scale)
        current_positions.append((rx, ry))
        
        # Colours shift identically with phase state
        r_col = int(30 + (crystal_integrity * 160)) # Shifts to sharp Red
        b_col = int(140 - (crystal_integrity * 100)) # Shifts away from Blue
        node_colour = (r_col, 40, b_col)
        
        # Opacity and node size scale with crystal density
        a_mult = 0.5 + (crystal_integrity * 0.5)
        rendered_nodes.append((rz, 'node', (rx, ry), node_colour, a_mult, crystal_integrity))
        
    # 3. DRAW CRYSTAL BONDS (Edges only form when composition begins)
    # The edges dynamically fade in/out and snap into perfect geometry
    edge_alpha_raw = (crystal_integrity - 0.1) / 0.9 if crystal_integrity > 0.1 else 0.0
    if edge_alpha_raw > 0:
        for (i, j) in edges:
            p1 = current_positions[i]
            p2 = current_positions[j]
            edge_intensity = min(1.0, edge_alpha_raw)
            # Bonds hold intense crimson colour
            line_c = (190, 20, 40, int(255 * edge_intensity))
            bond_thickness = max(1, int(4 * edge_intensity))
            draw.line([p1, p2], fill=line_c, width=bond_thickness)
            
    # 4. DRAW NODES (Depth sorted)
    rendered_nodes.sort(key=lambda x: x[0], reverse=True)
    
    for el in rendered_nodes:
        if el[1] == 'node':
            cx, cy = el[2]
            rgb = el[3]
            a = el[4]
            c_int = el[5]
            rad = 8 + (c_int * 8) # Nodes physically expand when locked
            draw_glowing_dot(draw, cx, cy, rad, rgb, int(255 * a))

    # 5. TYPOGRAPHY & UI LOGIC (Syncs directly to the 4 identical quarters)
    text_c = (20, 25, 30, 255)
    
    if t < 8.0:
        draw_text_with_outline(draw, (50, 150), "PHASE 1: ACCUMULATION", font_h1, (30, 50, 140, 255))
        draw_text_with_outline(draw, (50, 220), "Raw material gathers in the locality.", font_h2, text_c)
        draw_text_with_outline(draw, (50, 270), "Impulses orbit chaotically as pressure builds.", font_h2, text_c)
    elif 8.0 <= t < 16.0:
        draw_text_with_outline(draw, (50, 150), "PHASE 2: PHASE COMPOSITION", font_h1, (130, 40, 60, 255))
        draw_text_with_outline(draw, (50, 220), "A critical threshold is reached.", font_h2, text_c)
        draw_text_with_outline(draw, (50, 270), "The swarm snaps into ordered geometry.", font_h2, text_c)
    elif 16.0 <= t < 24.0:
        # Peak Crystal State
        draw_text_with_outline(draw, (50, 150), "PHASE 3: PARETO ADJACENT CRYSTAL", font_h1, (190, 20, 40, 255))
        draw_text_with_outline(draw, (50, 220), "Maximum structural integrity achieved.", font_h2, text_c)
        draw_text_with_outline(draw, (50, 270), "The exact fractional window of peak self-usefulness.", font_h2, text_c)
    elif t >= 24.0:
        draw_text_with_outline(draw, (50, 150), "PHASE 4: PHASE DECOMPOSITION", font_h1, (80, 40, 80, 255))
        draw_text_with_outline(draw, (50, 220), "The state requires too much glucose to sustain.", font_h2, text_c)
        draw_text_with_outline(draw, (50, 270), "Consciousness dissolves back into unstructured static.", font_h2, text_c)

    draw.line([(50, HEIGHT-100), (WIDTH-50, HEIGHT-100)], fill=(200, 205, 210, 180), width=3)
    
    # Progress UI Bar
    line_w = (WIDTH - 100) * loop_progress
    draw.line([(50, HEIGHT-100), (50 + line_w, HEIGHT-100)], fill=(190, 20, 40, 255), width=4)
    
    draw_text_with_outline(draw, (50, HEIGHT-80), "STRUCTURE: SINGLE NODE", font_h2, (120, 130, 140, 255))
    draw_text_with_outline(draw, (WIDTH-420, HEIGHT-80), "TARGET: THERMODYNAMIC CYCLE", font_h2, (120, 130, 140, 255))

    img.paste(overlay, (0, 0), overlay)
    img.save(f"frames/frame_{f:04d}.png")
    
    if f % 150 == 0:
        print(f"Processed {f}/{TOTAL_FRAMES} frames...")

print("Rendering single-node thermodynamic cycle via FFmpeg...")
os.system("ffmpeg -y -framerate 60 -i frames/frame_%04d.png -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p LG-467_The_Cycle_Of_Thought.mp4")
print("Render complete: LG-467_The_Cycle_Of_Thought.mp4")
