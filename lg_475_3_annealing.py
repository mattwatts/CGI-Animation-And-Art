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
DURATION = 24  # Seconds (Extended for majestic, serene loop)
TOTAL_FRAMES = FPS * DURATION
OUTPUT_DIR = "frames_475"
OUTPUT_FILE = "lg_475_annealing_fixed.mp4"

# High Contrast Colour Palette
C_WHITE   = (255, 255, 255)
C_BLACK   = (10, 10, 10)
C_STEEL   = (60, 60, 65)
C_GREY    = (180, 180, 185)
C_THERMAL = (255, 60, 0)   # Vivid orange/red for heat
C_QUANTUM = (0, 180, 255)  # Cyan for quantum probability

def get_font(size):
    fonts_to_try = ["arial.ttf", "Ubuntu-R.ttf", "Helvetica.ttf", "DejaVuSans.ttf"]
    for f in fonts_to_try:
        try:
            return ImageFont.truetype(f, size)
        except IOError:
            continue
    return ImageFont.load_default()

def draw_text_box(draw, center_x, top_y, text, font, border_color):
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
    
    draw.rounded_rectangle([bx1, by1, bx2, by2], radius=10, fill=C_WHITE, outline=border_color, width=3)
    draw.multiline_text((bx1 + padding, by1 + padding), text, fill=C_BLACK, font=font, spacing=8, align="center")

def calculate_landscape(x, baseline_y):
    """Generates the exact mathematical physical valley geometry."""
    u = (x - 540) / 400.0
    # Inverted to create a visual valley (U-shape) in Pythons Y-down coordinate system.
    # The edges have smaller Y values (rendered higher), the center has larger Y values (rendered deeper).
    y_val = -180 * (u**2) - 50 * math.sin(u * 5 * math.pi) - 20 * math.sin(u * 11 * math.pi)
    return baseline_y + y_val

def generate_frames():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    font_main = get_font(28)
    font_title = get_font(36)
    
    x_coords = list(range(140, 941, 2))
    
    # Calculate the absolute lowest physical valley trap
    # In a Y-down renderer, the lowest physical trap is the MAXIMUM statistical Y-value.
    max_y = -999999
    global_min_x = 540
    for x in x_coords:
        y = calculate_landscape(x, 0)
        if y > max_y:
            max_y = y
            global_min_x = x

    for frame in range(TOTAL_FRAMES):
        t = frame / TOTAL_FRAMES 
        
        # Annealing Schedule: High energy decel to Zero, holding, fading back up.
        energy = abs(math.cos(t * math.pi))
        if 0.4 < t < 0.6:
            energy = 0.0
        elif 0.3 <= t <= 0.4:
            energy = (0.4 - t) * 10 * math.cos(t * math.pi)

        img = Image.new("RGB", (WIDTH, HEIGHT), C_WHITE)
        draw = ImageDraw.Draw(img)
        
        # ----------------------------------------------------
        # TOP FRAME: SIMULATED THERMAL ANNEALING
        # ----------------------------------------------------
        T_Y = 650  # This represents the deepest baseline of the first geometry
        
        draw.text((WIDTH//2, 180), "SIMULATED THERMAL ANNEALING", fill=C_THERMAL, font=font_title, anchor="mm")
        
        # Draw physical landscape
        poly_t = [(140, T_Y + 100)]
        for x in x_coords:
            poly_t.append((x, calculate_landscape(x, T_Y)))
        poly_t.append((940, T_Y + 100))
        draw.polygon(poly_t, fill=C_GREY, outline=C_BLACK)
        
        # Thermal Particle Kinematics
        sweep = math.sin((frame * 0.05)) * 300 * energy + math.sin((frame * 0.03)) * 100 * energy
        particle_x = global_min_x + sweep
        particle_x = max(140, min(940, particle_x))
        base_y = calculate_landscape(particle_x, T_Y)
        
        # Vertical bouncing reduces to exactly zero inside the trap
        bounce = abs(math.sin(frame * 0.1)) * 200 * energy
        particle_y = base_y - bounce - 18  
        
        # Draw flame/heat trail
        draw.line([(particle_x, particle_y+15), (particle_x, base_y)], fill=C_THERMAL, width=4)
        draw.ellipse([particle_x-20, particle_y-20, particle_x+20, particle_y+20], fill=C_THERMAL, outline=C_BLACK, width=2)

        text_t = "Thermal Annealing\nThe particle uses heat to violently jump\nOVER the physical barriers.\nAs temperature drops, it loses energy\nand falls permanently into the lowest trap."
        draw_text_box(draw, WIDTH//2, T_Y + 150, text_t, font_main, C_THERMAL)

        # ----------------------------------------------------
        # BOTTOM FRAME: SIMULATED QUANTUM ANNEALING
        # ----------------------------------------------------
        Q_Y = 1530  # Shifted down to provide perfect isolation
        
        draw.text((WIDTH//2, 1060), "SIMULATED QUANTUM ANNEALING", fill=C_QUANTUM, font=font_title, anchor="mm")
        
        # Draw physical landscape
        poly_q = [(140, Q_Y + 100)]
        for x in x_coords:
            poly_q.append((x, calculate_landscape(x, Q_Y)))
        poly_q.append((940, Q_Y + 100))
        draw.polygon(poly_q, fill=C_GREY, outline=C_BLACK)

        # Quantum Wave Function Kinematics
        wave_points = []
        for x in x_coords:
            surf_y = calculate_landscape(x, Q_Y)
            sharpness = 1.0 + (1.0 - energy) * 20.0
            dist = abs(x - global_min_x)
            prob = math.exp(-(dist**2) / (10000 / sharpness))
            
            # The quantum energy collapses completely to the surface at energy == 0.0
            ripple = math.cos((x - frame*2)*0.1) * 20 * energy
            wave_y = surf_y - (prob * 150 * energy) - ripple
            
            # Tunnel lines directly penetrating the physical structure
            # Triggered only when the wave calculation mathematically breaches the barrier
            if energy > 0.05 and frame % 4 == 0:
                if wave_y > surf_y: 
                    draw.line([(x, surf_y), (x, wave_y)], fill=C_QUANTUM, width=1)

            wave_points.append((x, min(surf_y, wave_y)))

        # Draw the wave envelope clipping exactly at the physical edge
        for i in range(len(wave_points)-1):
            draw.line([wave_points[i], wave_points[i+1]], fill=C_QUANTUM, width=6)
            
        # Particle forming directly in the trap as the wave flattens
        if energy < 0.2:
            alpha_radius = 20 * (1.0 - (energy * 5))
            qx = global_min_x
            qy = calculate_landscape(qx, Q_Y) - 18
            draw.ellipse([qx-alpha_radius, qy-alpha_radius, qx+alpha_radius, qy+alpha_radius], fill=C_WHITE, outline=C_QUANTUM, width=4)

        text_q = "Quantum Annealing\nThe system exists as a wave, tunnelling\nstraight THROUGH the solid barriers.\nAs the quantum field drops, it condenses\nstrictly into the lowest valley."
        draw_text_box(draw, WIDTH//2, Q_Y + 150, text_q, font_main, C_QUANTUM)

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
