import os
import math
import subprocess
from PIL import Image, ImageDraw, ImageFont

# ==========================================
# METRICS & VARIABLES
# ==========================================
WIDTH = 1080
HEIGHT = 1920
FPS = 60
DURATION = 12  # Seconds (Seamless loop)
TOTAL_FRAMES = FPS * DURATION
OUTPUT_DIR = "frames_474b"
OUTPUT_FILE = "lg_474b_neutron_weapons.mp4"

# High Contrast Colour Palette
C_WHITE   = (255, 255, 255)
C_BLACK   = (10, 10, 10)
C_STEEL   = (60, 60, 65)
C_GREY    = (140, 140, 145)
C_NEUTRON = (0, 200, 255)  # Cyan representing fast neutron radiation
C_CORE    = (255, 50, 0)   # Thermal core

def get_font(size):
    fonts_to_try = ["arial.ttf", "Ubuntu-R.ttf", "Helvetica.ttf", "DejaVuSans.ttf"]
    for f in fonts_to_try:
        try:
            return ImageFont.truetype(f, size)
        except IOError:
            continue
    return ImageFont.load_default()

def draw_text_box(draw, center_x, top_y, text, font):
    """Draws a clean, jargon-free text box strictly anchored below the geometry."""
    padding = 20
    is_default = (font.getname()[0] == 'Core') if hasattr(font, 'getname') else True
    
    if is_default:
        lines = text.split('\n')
        w = max(len(line) for line in lines) * 7.5
        h = len(lines) * 18
    else:
        bbox = draw.multiline_textbbox((0, 0), text, font=font, align="center")
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]

    bx1 = center_x - (w / 2) - padding
    by1 = top_y
    bx2 = center_x + (w / 2) + padding
    by2 = top_y + h + padding * 2
    
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=10, fill=C_WHITE, outline=C_BLACK, width=3)
    draw.multiline_text((bx1 + padding, by1 + padding), text, fill=C_BLACK, font=font, spacing=8, align="center")

def draw_neutron_beam(draw, x, y, scale, t):
    """PANEL 1: Theoretical Directed Neutron Beam Weapon."""
    # Accelerator body
    draw.rectangle([x-100*scale, y-40*scale, x+50*scale, y+40*scale], outline=C_STEEL, width=4)
    # Emitter dish/lens
    draw.arc([x+30*scale, y-80*scale, x+90*scale, y+80*scale], start=135, end=225, fill=C_BLACK, width=5)
    draw.polygon([(x+50*scale, y-40*scale), (x+80*scale, y-20*scale), (x+80*scale, y+20*scale), (x+50*scale, y+40*scale)], outline=C_BLACK, width=3)
    
    # Internal focusing rings
    for i in range(4):
        cx = x - 80*scale + (i * 30*scale)
        draw.line([(cx, y-40*scale), (cx, y+40*scale)], fill=C_GREY, width=2)
        
    # Directed Neutron Pulse (Action)
    pulse_offset = (t * 200) % 50
    for p in range(5):
        px = x + 100*scale + pulse_offset + (p * 50*scale)
        if px < x + 350*scale:
            # Concentrated parallel beam
            draw.line([(px, y-10*scale), (px+30*scale, y-10*scale)], fill=C_NEUTRON, width=3)
            draw.line([(px, y), (px+30*scale, y)], fill=C_NEUTRON, width=4)
            draw.line([(px, y+10*scale), (px+30*scale, y+10*scale)], fill=C_NEUTRON, width=3)

def draw_w66_sprint(draw, x, y, scale, t):
    """PANEL 2: W66 Thermonuclear Warhead (Sprint ABM)."""
    # Sprint Missile extreme conical geometry (Mach 10+ atmospheric profile)
    draw.polygon([(x, y-180*scale), (x-60*scale, y+100*scale), (x+60*scale, y+100*scale)], outline=C_STEEL, width=4)
    
    # Internal pit geometry
    core_rad = 20 * scale
    draw.ellipse([x-core_rad, y+20*scale-core_rad, x+core_rad, y+20*scale+core_rad], fill=C_CORE, outline=C_BLACK, width=2)
    
    # Radiation action: Fast neutrons expanding rapidly outward in 360 degrees
    wave_radius = (t * 300) % 150
    draw.ellipse([x-wave_radius, y+20*scale-wave_radius, x+wave_radius, y+20*scale+wave_radius], outline=C_NEUTRON, width=2)
    wave_radius_2 = ((t+0.5) * 300) % 150
    draw.ellipse([x-wave_radius_2, y+20*scale-wave_radius_2, x+wave_radius_2, y+20*scale+wave_radius_2], outline=C_NEUTRON, width=2)

def draw_w70_lance(draw, x, y, scale, t):
    """PANEL 3: W70 Mod 3 (Lance Missile)."""
    # Cylindrical body turning into an ogive nose
    draw.line([(x-40*scale, y+150*scale), (x-40*scale, y-20*scale)], fill=C_STEEL, width=4)
    draw.line([(x+40*scale, y+150*scale), (x+40*scale, y-20*scale)], fill=C_STEEL, width=4)
    draw.arc([x-40*scale, y-120*scale, x+40*scale, y+80*scale], start=180, end=360, fill=C_STEEL, width=4) # Nose
    draw.line([(x-40*scale, y+150*scale), (x+40*scale, y+150*scale)], fill=C_STEEL, width=4) # Base
    
    # Physics package detail
    draw.rectangle([x-25*scale, y+30*scale, x+25*scale, y+110*scale], outline=C_GREY, width=2)
    draw.ellipse([x-15*scale, y+90*scale, x+15*scale, y+110*scale], fill=C_CORE, outline=C_BLACK, width=2) # Primary
    
    # Radiation action: Targeted lateral emission
    pulse_y = y - 50*scale
    pulse_r = (t * 200) % 100
    for ang in [0, 45, 135, 180, 225, 315]:
        rad_ang = math.radians(ang)
        lx = x + math.cos(rad_ang) * pulse_r
        ly = (y+70*scale) + math.sin(rad_ang) * pulse_r
        draw.line([(x, y+70*scale), (lx, ly)], fill=C_NEUTRON, width=2)

def draw_w79_artillery(draw, x, y, scale, t):
    """PANEL 4: W79 Artillery Shell 203mm."""
    # Heavy artillery shell geometry
    draw.line([(x-50*scale, y+120*scale), (x-50*scale, y-10*scale)], fill=C_STEEL, width=5)
    draw.line([(x+50*scale, y+120*scale), (x+50*scale, y-10*scale)], fill=C_STEEL, width=5)
    
    # Driving band
    draw.rectangle([x-52*scale, y+90*scale, x+52*scale, y+105*scale], fill=C_BLACK)
    
    # Pointed artillery nose
    draw.polygon([(x-50*scale, y-10*scale), (x, y-130*scale), (x+50*scale, y-10*scale)], outline=C_STEEL, width=5)
    
    # Internal dense core
    draw.rectangle([x-20*scale, y, x+20*scale, y+70*scale], outline=C_BLACK, width=3)
    
    # Radiation action: Pulsing solid field representing area saturation
    pulse = int(math.sin(t * math.pi * 2) * 80 + 100)
    pulse_w = int(math.sin((t+0.5) * math.pi * 2) * 80 + 100)
    draw.ellipse([x-100, y-100, x+100, y+150], outline=C_NEUTRON, width=3)
    draw.line([(x-120, y+20), (x+120, y+20)], fill=C_NEUTRON, width=2)
    draw.line([(x, y-120), (x, y+160)], fill=C_NEUTRON, width=2)

def generate_frames():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    font_main = get_font(28)
    
    # Spread coordinates to fill the 1920 height
    C_1_X = 270    
    C_2_X = 810    
    ROW_1_Y = 500  
    ROW_2_Y = 1250 

    for frame in range(TOTAL_FRAMES):
        t = frame / FPS
        cycle_t = (frame % FPS) / FPS  # Local cycle for tight continuous loops
        anim_t = frame / TOTAL_FRAMES  # Global 0-1 cycle
        
        img = Image.new("RGB", (WIDTH, HEIGHT), C_WHITE)
        draw = ImageDraw.Draw(img)
        
        # Faint structural cross to anchor the grid visually but not interfere with UI
        draw.line([(WIDTH//2, 300), (WIDTH//2, 1600)], fill=(230,230,230), width=2)
        draw.line([(50, HEIGHT//2), (WIDTH-50, HEIGHT//2)], fill=(230,230,230), width=2)

        # ----------------------------------------------------
        # Panel 1: Theoretical Beam
        # ----------------------------------------------------
        draw_neutron_beam(draw, 180, ROW_1_Y - 100, 1.2, cycle_t)
        text1 = "1: Neutron Beam\nA theoretical directed energy\nweapon. Uses accelerators\nto shoot a focused straight line\nof neutrons directly at a target."
        draw_text_box(draw, C_1_X, ROW_1_Y + 70, text1, font_main)

        # ----------------------------------------------------
        # Panel 2: W66 Sprint ABM
        # ----------------------------------------------------
        draw_w66_sprint(draw, C_2_X, ROW_1_Y - 50, 1.1, anim_t)
        text2 = "2: W66 Sprint Missile\nA highly pointed warhead\nmade to intercept incoming\nrockets. It creates a sphere\nof energy to melt the\nenemy electronics."
        draw_text_box(draw, C_2_X, ROW_1_Y + 70, text2, font_main)

        # ----------------------------------------------------
        # Panel 3: W70 Mod 3 Lance
        # ----------------------------------------------------
        draw_w70_lance(draw, C_1_X, ROW_2_Y - 140, 1.1, cycle_t)
        text3 = "3: W70 Mod 3 (Lance)\nA battlefield missile payload.\nIt reduces the blast and\ncreates intense radiation\nto halt tank columns.\nThe terrain is unharmed."
        draw_text_box(draw, C_1_X, ROW_2_Y + 50, text3, font_main)

        # ----------------------------------------------------
        # Panel 4: W79 Artillery
        # ----------------------------------------------------
        draw_w79_artillery(draw, C_2_X, ROW_2_Y - 140, 1.1, anim_t)
        text4 = "4: W79 Heavy Artillery\nA massive 203mm shell.\nFired from a standard\nmilitary cannon, turning\nheavy artillery into a\nprecision radiation tool."
        draw_text_box(draw, C_2_X, ROW_2_Y + 50, text4, font_main)

        # Secure UI areas at the extreme top and bottom
        draw.rectangle([0, 0, WIDTH, 100], fill=C_WHITE)
        draw.rectangle([0, HEIGHT-150, WIDTH, HEIGHT], fill=C_WHITE)

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
