"""
SOVEREIGN CODE: logic_garden_110_warhol.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: C64 VIC-II Mode (Multicolor Bitmap)
SCENE: Logic Garden 110 (Warhol Turn)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, Wedge, Ellipse
import matplotlib.patheffects as pe
import os
import math

# CONFIG
FPS = 12 # Low framerate for "Stop Motion" art feel
DURATION = 15
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_110_warhol"
os.makedirs(OUT_DIR, exist_ok=True)

# C64 PALETTE
C64 = {
    'BLACK': '#000000', 'WHITE': '#FFFFFF', 'RED': '#880000', 'CYAN': '#AAFFEE',
    'PURPLE': '#CC44CC', 'GREEN': '#00CC55', 'BLUE': '#0000AA', 'YELLOW': '#EEEE77',
    'ORANGE': '#DD8855', 'BROWN': '#664400', 'LIGHTRED': '#FF7777', 'DARKGREY': '#333333',
    'GREY': '#777777', 'LIGHTGREEN': '#AAFF66', 'LIGHTBLUE': '#0088FF', 'LIGHTGREY': '#BBBBBB',
    'PINK': '#FF7777' # Mapping Lightred to "Pink" for art
}

def get_face_geometry(angle_norm):
    """
    Returns lists of patches for the face based on rotation angle.
    angle_norm: 0.0 (Profile Left) -> 0.5 (3/4) -> 1.0 (Front)
    """
    patches = []
    
    # Base Scale
    s = 1.0
    
    # 1. HAIR (The iconic 'Wig')
    # Spiky, chaotic halo. Shifts slightly with angle.
    wig_w = 220
    wig_h = 240
    wig_x = 0
    
    # 2. FACE SHAPE
    # Profile: Narrower, offset left. Front: Wide, centered.
    face_w = 140 + (angle_norm * 40) # 140 -> 180
    face_x = 0
    
    # 3. EYES / GLASSES / BROWS
    # Profile: One eye visible on edge.
    # Front: Two eyes.
    
    # Eye positions
    left_eye_x = -40 + (angle_norm * 20)
    left_eye_w = 25 * angle_norm # Grows from sliver to full
    right_eye_x = 20 + (angle_norm * 20)
    right_eye_w = 25
    
    eye_y = 20
    
    # GEOMETRY DATA STRUCTURE
    geo = {
        'wig': {'xy': (wig_x, 50), 'w': wig_w, 'h': wig_h},
        'face': {'xy': (face_x, 0), 'w': face_w, 'h': 220},
        'l_eye': {'xy': (left_eye_x, eye_y), 'w': left_eye_w, 'h': 15},
        'r_eye': {'xy': (right_eye_x, eye_y), 'w': right_eye_w, 'h': 15},
        'nose': {'x': 0 + (angle_norm * 5), 'y': -20, 'w': 15, 'h': 35}, # Nose shifts right
        'mouth': {'x': 0 + (angle_norm * 5), 'y': -60, 'w': 30 + (angle_norm*30), 'h': 10}
    }
    return geo

def draw_andy(ax, x, y, palette, angle_norm):
    """
    Draws one Andy head at x,y with specific colors.
    Palette: [Background, Hair, Skin, Shadows/Details]
    """
    bg, hair_col, skin_col, detail_col = palette
    
    geo = get_face_geometry(angle_norm)
    
    # Clip grouping rect
    # Background Panel
    ax.add_patch(Rectangle((x - 200, y - 200), 400, 400, color=bg))
    
    # Hair (Back layer)
    # Using multiple wedges to simulate the messy wig style
    # Ideally a static polygon, but let's use Ellipse for simplicity
    ax.add_patch(Ellipse((x + geo['wig']['xy'][0], y + geo['wig']['xy'][1]), 
                         geo['wig']['w'], geo['wig']['h'], color=hair_col))
    
    # Add some "spikes" to hair
    ax.add_patch(Wedge((x - 60, y + 100), 50, 90, 180, color=hair_col))
    ax.add_patch(Wedge((x + 60, y + 100), 50, 0, 90, color=hair_col))

    # Face
    ax.add_patch(Ellipse((x + geo['face']['xy'][0], y + geo['face']['xy'][1]),
                         geo['face']['w'], geo['face']['h'], color=skin_col))
    
    # Neck (Turtleneck shadow)
    ax.add_patch(Rectangle((x - 40, y - 150), 80, 60, color=detail_col))
    
    # Eyes
    if geo['l_eye']['w'] > 2: # Visible?
        ax.add_patch(Ellipse((x + geo['l_eye']['xy'][0], y + geo['l_eye']['xy'][1]),
                             geo['l_eye']['w'], geo['l_eye']['h'], color=detail_col))
    
    ax.add_patch(Ellipse((x + geo['r_eye']['xy'][0], y + geo['r_eye']['xy'][1]),
                         geo['r_eye']['w'], geo['r_eye']['h'], color=detail_col))
                         
    # Nose (Shadow Polygon)
    # Triangle shape
    nx = x + geo['nose']['x']
    ny = y + geo['nose']['y']
    nose_poly = Polygon([(nx, ny+30), (nx-10, ny), (nx+5, ny)], color=detail_col, alpha=0.5)
    ax.add_patch(nose_poly)
    
    # Mouth
    mx = x + geo['mouth']['x']
    my = y + geo['mouth']['y']
    ax.add_patch(Rectangle((mx - geo['mouth']['w']/2, my), geo['mouth']['w'], geo['mouth']['h'], color=detail_col))


def run():
    print(f"LOGIC GARDEN 110: THE ARTIST ({TOTAL_FRAMES} frames)")
    
    # 4 distinct palettes (Warhol style)
    # Format: [BG, Hair, Skin, Details]
    p1 = [C64['YELLOW'], C64['BLACK'], C64['PINK'], C64['CYAN']] # Iconic Marilyn
    p2 = [C64['BLUE'], C64['YELLOW'], C64['GREY'], C64['BLACK']]
    p3 = [C64['RED'], C64['WHITE'], C64['ORANGE'], C64['BLACK']] # High contrast
    p4 = [C64['GREEN'], C64['PURPLE'], C64['LIGHTGREEN'], C64['BLUE']] # Toxic
    
    for f in range(TOTAL_FRAMES):
        
        # TIMING LOGIC
        # 0-3s: Still (Profile)
        # 3-6s: Turn to Front (Lerp)
        # 6-9s: Hold (Stare)
        # 9-12s: Color Cycle Flash
        # 12-15s: Hold
        
        turn_progress = 0.0
        if 45 <= f < 90: # Turn
            turn_progress = (f - 45) / 45.0
            # Ease in out
            turn_progress = turn_progress * turn_progress * (3 - 2 * turn_progress)
        elif f >= 90:
            turn_progress = 1.0
            
        # Color Cycle during flash phase
        if 135 <= f < 180:
            if f % 4 == 0:
                # Rotate palettes
                p1, p2, p3, p4 = p4, p1, p2, p3
        
        # --- RENDER ---
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        # Background: Dark Grey Border
        ax.set_facecolor(C64['DARKGREY'])
        
        # CRT Screen Area
        sx, sy, sw, sh = 50, 600, 980, 720
        ax.add_patch(Rectangle((sx, sy), sw, sh, color=C64['BLACK']))
        
        # Quadrant Centers
        cx_left = sx + sw*0.25
        cx_right = sx + sw*0.75
        cy_top = sy + sh*0.75
        cy_bot = sy + sh*0.25
        
        # Draw 4 Andys
        draw_andy(ax, cx_left, cy_top, p1, turn_progress)  # Top Left
        draw_andy(ax, cx_right, cy_top, p2, turn_progress) # Top Right
        draw_andy(ax, cx_left, cy_bot, p3, turn_progress)  # Bot Left
        draw_andy(ax, cx_right, cy_bot, p4, turn_progress) # Bot Right
        
        # Screen Divider Lines (Grid)
        ax.axvline(sx + sw/2, color=C64['BLACK'], linewidth=10)
        ax.axhline(sy + sh/2, color=C64['BLACK'], linewidth=10)

        # Scanlines
        for y in range(sy, sy + sh, 6):
            ax.axhline(y, color='black', alpha=0.15, linewidth=2)

        # UI Text
        ax.text(540, 1600, "LOGIC GARDEN 110", color=C64['WHITE'], ha='center',
                fontsize=40, fontname='monospace', weight='bold', 
                path_effects=[pe.withStroke(linewidth=4, foreground=C64['BLACK'])])
        
        caption = "15 MINUTES" if f < 90 else "OF FAME"
        ax.text(540, 1500, caption, color=C64['YELLOW'], ha='center',
                fontsize=30, fontname='monospace', weight='bold',
                path_effects=[pe.withStroke(linewidth=4, foreground=C64['BLACK'])])

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
