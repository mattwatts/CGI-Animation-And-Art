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
def project(x, y, z, cam_angle_rad, tilt_rad, scale, offset_x=WIDTH/2, offset_y=HEIGHT/2 + 20):
    x_rot = x * math.cos(cam_angle_rad) - z * math.sin(cam_angle_rad)
    z_rot = x * math.sin(cam_angle_rad) + z * math.cos(cam_angle_rad)
    y_rot = y * math.cos(tilt_rad) - z_rot * math.sin(tilt_rad)
    px = offset_x + (x_rot * scale)
    py = offset_y - (y_rot * scale)
    return px, py, z_rot

def draw_glowing_dot(draw, x, y, radius, colour, max_alpha=255):
    # Glow aura
    layers = 4
    for i in range(layers):
        r = radius * (1 - (i / layers))
        alpha = int(max_alpha * (i / layers))
        draw.ellipse([(x - r, y - r), (x + r, y + r)], fill=(colour[0], colour[1], colour[2], alpha))
    # Solid inner core for maximum contrast
    r_core = radius * 0.4
    draw.ellipse([(x - r_core, y - r_core), (x + r_core, y + r_core)], fill=(colour[0], colour[1], colour[2], 255))

def smoothstep(edge0, edge1, x):
    t = max(0.0, min(1.0, (x - edge0) / (edge1 - edge0)))
    return t * t * (3.0 - 2.0 * t)

# -------------------------
# STRUCTURAL VARIABLES
# -------------------------
print("Generating high-contrast neuroplastic matrix for LG-468b...")

NODE_TOP = (0, 7.0, 0)
NODE_BOT = (0, -7.0, 0)

# The dying internal cluster (10 nodes - Critical Mass)
core_coords = []
for i in range(10):
    ang = (i / 10.0) * math.pi * 2
    core_coords.append((math.cos(ang) * 1.8, math.sin(ang * 4) * 1.2, math.sin(ang) * 1.8))

# Peripheral Silent Synapses (16 total: 10 detours, 6 unused)
periph_coords = []
for i in range(16):
    ang = (i / 16.0) * math.pi * 2
    periph_coords.append((math.cos(ang) * 5.5, math.sin(ang * 2) * 2.0, math.sin(ang) * 5.5))

# -------------------------
# RENDER LOOP
# -------------------------
random.seed(468)

for f in range(TOTAL_FRAMES):
    t = f / FPS
    loop_progress = f / TOTAL_FRAMES
    
    # Mathematical Phase Curves
    phase_death   = smoothstep(1.5, 3.5, t)
    phase_sprout  = smoothstep(4.5, 8.0, t) - smoothstep(17.0, 23.0, t)
    phase_hebbian = smoothstep(14.0, 18.0, t)
    phase_morph   = smoothstep(25.0, 31.0, t)
    
    # Camera gently orbits, providing steady, exact 3D geometry observation
    cam_angle = loop_progress * 2 * math.pi * 1.5 
    cam_tilt = 0.20 + (math.sin(loop_progress * 2 * math.pi) * 0.1)
    
    img = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))
    overlay = Image.new('RGBA', (WIDTH, HEIGHT), (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    scale = 130
    
    rendered_elements = []
    
    # PRIMARY STRUCTURE NODES (Dark Slate - Highest Contrast)
    px_top, py_top, pz_top = project(*NODE_TOP, cam_angle, cam_tilt, scale)
    px_bot, py_bot, pz_bot = project(*NODE_BOT, cam_angle, cam_tilt, scale)
    rendered_elements.append((pz_top, 'node', (px_top, py_top), (40, 50, 60), 1.0, 12))
    rendered_elements.append((pz_bot, 'node', (px_bot, py_bot), (40, 50, 60), 1.0, 12))
    
    # PHASE 1: DYING CORE (10 Nodes)
    alpha_dead = int(255 * (1.0 - phase_death))
    if alpha_dead > 0:
        for i in range(10):
            scatter_vel = max(0, (t - 1.5) * 8.0)
            dx = math.sin(i * 7.1) * scatter_vel
            dy = math.cos(i * 3.3) * scatter_vel
            dz = math.sin(i * 1.8) * scatter_vel
            
            ex, ey, ez = core_coords[i]
            dead_pos = (ex + dx, ey + dy, ez + dz)
            pr_dx, pr_dy, pr_dz = project(*dead_pos, cam_angle, cam_tilt, scale)
            
            rendered_elements.append((pr_dz, 'node', (pr_dx, pr_dy), (40, 50, 60), alpha_dead/255.0, 10))
            
            if phase_death < 0.1: # Bonds shatter immediately
                draw.line([(px_top, py_top), (pr_dx, pr_dy)], fill=(40, 50, 60, alpha_dead), width=5)
                draw.line([(pr_dx, pr_dy), (px_bot, py_bot)], fill=(40, 50, 60, alpha_dead), width=5)

    # PHASE 2: SPROUTING (Massive, High-Contrast Chaotic Reach)
    if phase_sprout > 0.01:
        sprout_alpha = int(220 * phase_sprout)
        for p_idx, p_target in enumerate(periph_coords):
            for s in range(2): 
                for src in [NODE_TOP, NODE_BOT]:
                    nx = math.sin(t*5.0 + p_idx*3 + s*5) * 4.0
                    ny = math.cos(t*4.0 - p_idx*2 + s*7) * 4.0
                    nz = math.sin(t*6.0 + p_idx*4 + s*3) * 4.0
                    
                    mid1 = (src[0]*0.6 + p_target[0]*0.4 + nx*0.4,
                            src[1]*0.6 + p_target[1]*0.4 + ny*0.4,
                            src[2]*0.6 + p_target[2]*0.4 + nz*0.4)
                    mid2 = (src[0]*0.2 + p_target[0]*0.8 + nx*0.8,
                            src[1]*0.2 + p_target[1]*0.8 + ny*0.8,
                            src[2]*0.2 + p_target[2]*0.8 + nz*0.8)
                    end = (p_target[0] + nx*0.3, p_target[1] + ny*0.3, p_target[2] + nz*0.3)
                    
                    p0 = project(*src, cam_angle, cam_tilt, scale)
                    p1 = project(*mid1, cam_angle, cam_tilt, scale)
                    p2 = project(*mid2, cam_angle, cam_tilt, scale)
                    p3 = project(*end, cam_angle, cam_tilt, scale)
                    
                    # Vivid Deep Blue searching lines
                    draw.line([p0[:2], p1[:2], p2[:2], p3[:2]], fill=(20, 70, 160, sprout_alpha), width=3)

    # PHASE 3 & 4: THE DETOUR MULTI-ARRAY & MORPH
    # Array maps 10 successful detours from Peripheral to Core
    c_r, c_g, c_b = 40, 50, 60 # Default Slate Slate
    
    if phase_hebbian > 0.0 and phase_morph == 0.0:
        c_r = int(40 + (180 - 40) * phase_hebbian)
        c_g = int(50 + (10 - 50) * phase_hebbian)
        c_b = int(60 + (30 - 60) * phase_hebbian)
    elif phase_morph > 0.0:
        # Fades identically back into standard dark grey core
        c_r = int(180 + (40 - 180) * phase_morph)
        c_g = int(10 + (50 - 10) * phase_morph)
        c_b = int(30 + (60 - 30) * phase_morph)

    # 10 Chosen Detours
    for i in range(10): 
        sx, sy, sz = periph_coords[i]
        ex, ey, ez = core_coords[i]
        
        # Morph translation
        mx = sx + (ex - sx) * phase_morph
        my = sy + (ey - sy) * phase_morph
        mz = sz + (ez - sz) * phase_morph
        
        pr_mx, pr_my, pr_mz = project(mx, my, mz, cam_angle, cam_tilt, scale)
        rendered_elements.append((pr_mz, 'node', (pr_mx, pr_my), (c_r, c_g, c_b), 1.0, 10))
        
        # Solidified Pathway Bonds
        alpha_hebbian = int(255 * phase_hebbian)
        if alpha_hebbian > 0:
            draw.line([(px_top, py_top), (pr_mx, pr_my)], fill=(c_r, c_g, c_b, alpha_hebbian), width=6)
            draw.line([(pr_mx, pr_my), (px_bot, py_bot)], fill=(c_r, c_g, c_b, alpha_hebbian), width=6)

    # 6 Unused Peripheral "Silent Synapses"
    for i in range(10, 16):
        ux, uy, uz = periph_coords[i]
        pr_ux, pr_uy, pr_uz = project(ux, uy, uz, cam_angle, cam_tilt, scale)
        rendered_elements.append((pr_uz, 'node', (pr_ux, pr_uy), (40, 50, 60), 1.0, 8))

    # 10 Replacement Peripheral Nodes (Fading in exactly to replace migrated core)
    alpha_repl = int(255 * phase_morph)
    if alpha_repl > 0:
        for i in range(10):
            rx, ry, rz = periph_coords[i]
            pr_rx, pr_ry, pr_rz = project(rx, ry, rz, cam_angle, cam_tilt, scale)
            rendered_elements.append((pr_rz, 'node', (pr_rx, pr_ry), (40, 50, 60), alpha_repl/255.0, 8))

    # 4. DRAW DEPTH SORTED NODES
    rendered_elements.sort(key=lambda x: x[0], reverse=True)
    for el in rendered_elements:
        if el[1] == 'node':
            cx, cy = el[2]
            rgb = el[3]
            a = el[4]
            r = el[5]
            draw_glowing_dot(draw, cx, cy, r, rgb, int(255 * a))

    # 5. HIGH-CONTRAST TYPOGRAPHY & UI LOGIC
    text_c = (20, 25, 30, 255)
    
    if t < 8.0:
        draw_text_with_outline(draw, (50, 150), "PHASE 1: CELL DEATH", font_h1, (30, 40, 50, 255))
        draw_text_with_outline(draw, (50, 220), "Critical cluster failure in the primary core.", font_h2, text_c)
        draw_text_with_outline(draw, (50, 270), "Signal coherence collapses completely.", font_h2, text_c)
    elif 8.0 <= t < 16.0:
        draw_text_with_outline(draw, (50, 150), "PHASE 2: COLLATERAL SPROUTING", font_h1, (20, 70, 160, 255))
        draw_text_with_outline(draw, (50, 220), "Intact neurons aggressively branch outward.", font_h2, text_c)
        draw_text_with_outline(draw, (50, 270), "A chaotic, energy-dense search for silent synapses.", font_h2, text_c)
    elif 16.0 <= t < 24.0:
        draw_text_with_outline(draw, (50, 150), "PHASE 3: HEBBIAN PLASTICITY", font_h1, (180, 10, 30, 255))
        draw_text_with_outline(draw, (50, 220), "Multiple functional detour pathways lock in.", font_h2, text_c)
        draw_text_with_outline(draw, (50, 270), "Dopaminergic gating structurally welds the network.", font_h2, text_c)
    elif t >= 24.0:
        draw_text_with_outline(draw, (50, 150), "PHASE 4: SYNAPTIC PRUNING", font_h1, (80, 20, 100, 255))
        draw_text_with_outline(draw, (50, 220), "Microglia digest the chaotic, unused noise.", font_h2, text_c)
        draw_text_with_outline(draw, (50, 270), "Deep-sleep solidifies the new matrix into the core.", font_h2, text_c)

    draw.line([(50, HEIGHT-100), (WIDTH-50, HEIGHT-100)], fill=(120, 130, 140, 255), width=4)
    
    # Progress UI Bar
    line_w = (WIDTH - 100) * loop_progress
    bar_c = (180, 10, 30, 255) if phase_hebbian > 0.5 else (40, 50, 60, 255)
    draw.line([(50, HEIGHT-100), (50 + line_w, HEIGHT-100)], fill=bar_c, width=8)
    
    draw_text_with_outline(draw, (50, HEIGHT-80), "STRUCTURE: NEURAL MATRIX", font_h2, (60, 70, 80, 255))
    draw_text_with_outline(draw, (WIDTH-480, HEIGHT-80), "TARGET: PLASTIC REGENERATION", font_h2, (60, 70, 80, 255))

    img.paste(overlay, (0, 0), overlay)
    img.save(f"frames/frame_{f:04d}.png")
    
    if f % 150 == 0:
        print(f"Processed {f}/{TOTAL_FRAMES} frames...")

print("Rendering high-contrast neuroplasticity video via FFmpeg...")
os.system("ffmpeg -y -framerate 60 -i frames/frame_%04d.png -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p LG-468b_Neuroplastic_Regeneration.mp4")
print("Render complete: LG-468b_Neuroplastic_Regeneration.mp4")
