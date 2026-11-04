import os
import math
import subprocess
from PIL import Image, ImageDraw, ImageFont

# Variables
WIDTH = 1080
HEIGHT = 1920
FPS = 60
DURATION = 10  # Seconds
TOTAL_FRAMES = FPS * DURATION
OUTPUT_DIR = "erw_frames"
OUTPUT_FILE = "output_erw_scenarios.mp4"

# Australian / High Contrast Colour Palette
C_WHITE = (255, 255, 255)
C_BLACK = (10, 10, 10)
C_GREY = (150, 150, 150)
C_STEEL = (80, 80, 85)
C_NEUTRON = (0, 200, 255)  # Cyan for fast neutron flux
C_HEAT = (255, 50, 0)      # Melting core

def get_font():
    """Attempt to load a clear font, fallback to default PIL font scaled up."""
    fonts_to_try = ["arial.ttf", "Ubuntu-R.ttf", "Helvetica.ttf", "DejaVuSans.ttf"]
    for f in fonts_to_try:
        try:
            return ImageFont.truetype(f, 26), False
        except IOError:
            continue
    return ImageFont.load_default(), True

def draw_text_box(draw, center_x, top_y, text, font, is_default):
    """Draws a clean, jargon-free text box strictly anchored below the geometry."""
    padding = 15
    
    if is_default:
        lines = text.split('\n')
        w = max(len(line) for line in lines) * 6 * 2.5 
        h = len(lines) * 15 * 2.5
    else:
        # Measure text block dimensions
        bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center")
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # Calculate box boundaries based on center_x
    bx1 = center_x - (w / 2) - padding
    by1 = top_y
    bx2 = center_x + (w / 2) + padding
    by2 = top_y + h + padding * 2
    
    # Draw simple bounding box
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=8, fill=C_WHITE, outline=C_BLACK, width=3)
    
    if is_default:
        draw.multiline_text((bx1 + padding, by1 + padding), text, fill=C_BLACK, font=font, align="center")
    else:
        draw.multiline_text((bx1 + padding, by1 + padding), text, fill=C_BLACK, font=font, spacing=6, align="center")

def draw_tank(draw, x, y, scale=1.0):
    """Detailed geometric cross-section of an armoured vehicle."""
    draw.polygon([(x, y), (x+200*scale, y), (x+250*scale, y+50*scale), 
                  (x+250*scale, y+100*scale), (x-20*scale, y+100*scale), (x, y)], 
                 outline=C_STEEL, width=4)
    draw.polygon([(x+30*scale, y), (x+150*scale, y), (x+120*scale, y-40*scale), (x+50*scale, y-40*scale)], 
                 outline=C_STEEL, width=4)
    draw.line([(x+150*scale, y-20*scale), (x+350*scale, y-20*scale)], fill=C_STEEL, width=10)
    for i in range(5):
        cx = x + 30*scale + (i * 45*scale)
        cy = y + 100*scale
        draw.ellipse([cx-15*scale, cy-15*scale, cx+15*scale, cy+15*scale], outline=C_BLACK, width=3)

def draw_rv(draw, x, y, scale=1.0, heat=0):
    """Detailed geometric cross-section of an incoming reentry vehicle."""
    draw.polygon([(x, y), (x-40*scale, y-150*scale), (x+40*scale, y-150*scale)], outline=C_BLACK, width=4)
    core_rad = 15*scale
    r = int(C_BLACK[0] + (C_HEAT[0] - C_BLACK[0]) * heat)
    g = int(C_BLACK[1] + (C_HEAT[1] - C_BLACK[1]) * heat)
    b = int(C_BLACK[2] + (C_HEAT[2] - C_BLACK[2]) * heat)
    draw.ellipse([x-core_rad, y-100*scale-core_rad, x+core_rad, y-100*scale+core_rad], fill=(r,g,b), outline=C_BLACK, width=2)
    draw.rectangle([x-25*scale, y-140*scale, x+25*scale, y-120*scale], outline=C_GREY, width=2)

def draw_city(draw, x, y, scale=1.0):
    """Detailed city infrastructure scaled to fit."""
    draw.rectangle([x, y-150*scale, x+80*scale, y], outline=C_BLACK, width=4)
    draw.rectangle([x+100*scale, y-250*scale, x+180*scale, y], outline=C_BLACK, width=4)
    draw.rectangle([x+200*scale, y-100*scale, x+350*scale, y], outline=C_BLACK, width=4)
    
    for wy in range(int(y-230*scale), int(y-20*scale), int(30*scale)):
        draw.rectangle([x+110*scale, wy, x+130*scale, wy+15*scale], fill=C_GREY)
        draw.rectangle([x+150*scale, wy, x+170*scale, wy+15*scale], fill=C_GREY)
        
    draw.arc([x+350*scale, y-50*scale, x+550*scale, y+50*scale], start=180, end=270, fill=C_BLACK, width=4)
    draw.line([(x+350*scale, y), (x+550*scale, y)], fill=C_BLACK, width=4)

def draw_satellite(draw, x, y, scale=1.0, glitch_phase=0):
    """Orbital satellite lattice and solar array."""
    draw.rectangle([x-20*scale, y-40*scale, x+20*scale, y+40*scale], outline=C_BLACK, width=4)
    glitch_offset = math.sin(glitch_phase * math.pi * 2) * 5
    draw.rectangle([x-150*scale, y-20*scale + glitch_offset, x-20*scale, y+20*scale - glitch_offset], outline=C_STEEL, width=3)
    draw.rectangle([x+20*scale, y-20*scale - glitch_offset, x+150*scale, y+20*scale + glitch_offset], outline=C_STEEL, width=3)
    draw.arc([x-30*scale, y-80*scale, x+30*scale, y-20*scale], start=180, end=360, fill=C_BLACK, width=3)
    draw.line([(x, y-40*scale), (x, y-70*scale)], fill=C_BLACK, width=2)

def draw_neutrons(draw, bx, by, bw, bh, t, direction="right"):
    """Draws invisible radiation strictly bounded to the local panel architecture."""
    wave_count = 6
    spacing = bh // wave_count
    
    if direction == "right":
        for i in range(wave_count):
            y = by + 20 + (i * spacing)
            offset = (t * 1500) % 80
            for x in range(bx - 100, bx + bw, 80):
                px = x + offset
                # Clip drawing to panel dimensions
                if px > bx and px + 30 < bx + bw:
                    draw.line([(px, y), (px+30, y)], fill=C_NEUTRON, width=2)
                    
    elif direction == "down":
        for i in range(wave_count):
            x = bx + 40 + (i * (bw // wave_count))
            offset = (t * 1500) % 80
            for py_grid in range(by - 100, by + bh, 80):
                py = py_grid + offset
                if py > by and py + 30 < by + bh:
                    draw.line([(x, py), (x, py+30)], fill=C_NEUTRON, width=2)

def generate_frames():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    font, is_default = get_font()
    
    # 2x2 Grid Centers (Leave top 250px and bottom 600px blank for YT UI)
    C_1_X = 270    # Left column center
    C_2_X = 810    # Right column center
    ROW_1_Y = 400  # Top row assets
    ROW_2_Y = 950  # Bottom row assets
    
    for frame in range(TOTAL_FRAMES):
        t = frame / TOTAL_FRAMES
        img = Image.new("RGB", (WIDTH, HEIGHT), C_WHITE)
        draw = ImageDraw.Draw(img)
        
        # Draw a faint structural divider to anchor the layout (stops short of UI safe zones)
        draw.line([(WIDTH//2, 250), (WIDTH//2, 1400)], fill=C_GREY, width=2)
        draw.line([(50, 725), (WIDTH-50, 725)], fill=C_GREY, width=2)

        # ----------------------------------------------------
        # Panel 1: Armour Interdiction (Top Left)
        # ----------------------------------------------------
        draw_tank(draw, C_1_X - 120, ROW_1_Y - 50, scale=0.9)
        draw_neutrons(draw, 20, 250, 500, 280, t, direction="right")
        text1 = "1: Armour Intercept\nInvisible energy phases\nthrough solid metal.\nThe armour stops.\nThe terrain remains\nfree of craters."
        draw_text_box(draw, C_1_X, ROW_1_Y + 120, text1, font, is_default)

        # ----------------------------------------------------
        # Panel 2: Ballistic Intercept (Top Right)
        # ----------------------------------------------------
        heat_val = math.sin(t * math.pi) 
        draw_rv(draw, C_2_X, ROW_1_Y + 70, scale=1.3, heat=heat_val)
        draw_neutrons(draw, 560, 250, 500, 280, t, direction="down")
        text2 = "2: Sky Defence\nEnergy hits the incoming\nwarhead high in the sky.\nIt melts the electronics\ninside instantly.\nThe weapon is ruined\nbefore impact."
        draw_text_box(draw, C_2_X, ROW_1_Y + 120, text2, font, is_default)

        # ----------------------------------------------------
        # Panel 3: Urban Offensive (Bottom Left)
        # ----------------------------------------------------
        draw_city(draw, C_1_X - 180, ROW_2_Y + 50, scale=0.7)
        draw_neutrons(draw, 20, 780, 500, 300, t, direction="right")
        text3 = "3: Intact Cities\nThe wave clears out\nbiological defenses.\nThe buildings are not\nshattered. The infrastructure\nremains fully intact."
        draw_text_box(draw, C_1_X, ROW_2_Y + 120, text3, font, is_default)

        # ----------------------------------------------------
        # Panel 4: Space Electronics (Bottom Right)
        # ----------------------------------------------------
        glitch = t * 10 if (t * 100) % 20 > 15 else 0
        draw_satellite(draw, C_2_X, ROW_2_Y, scale=1.3, glitch_phase=glitch)
        draw_neutrons(draw, 560, 780, 500, 300, t, direction="right")
        text4 = "4: Orbit Control\nIn space, there is no\nblast wave.\nRadiation disrupts the\nmaths in the chips,\nleaving orbit safe."
        draw_text_box(draw, C_2_X, ROW_2_Y + 120, text4, font, is_default)

        # Save frame
        filename = f"{OUTPUT_DIR}/frame_{frame:04d}.png"
        img.save(filename)
        if frame % 60 == 0:
            print(f"Generated {frame}/{TOTAL_FRAMES} frames...")

def compile_video():
    print("Compiling video using ffmpeg...")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", f"{OUTPUT_DIR}/frame_%04d.png",
        "-c:v", "libx264",
        "-r", str(FPS),
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "fast",
        OUTPUT_FILE
    ]
    subprocess.run(cmd, check=True)
    print(f"Video generated successfully: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_frames()
    compile_video()
