"""
SOVEREIGN CODE: logic_garden_135_fmj_mickey.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python High-Fidelity Simulator (C-64 Demake Protocol)
SCENE: Logic Garden 135 (Full Metal Jacket / Mickey Mouse March)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# -------- COMPILE-TIME METRICS --------
FPS = 30
DURATION = 30                   # 30-Second Extended Cut
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_135_fmj"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (HIGH-VOLTAGE) --------
C_VOID = '#020205'              # Absolute Black (The Night)
C_RUIN_BG = '#1A1A1A'           # Parallax Background Ruins
C_RUIN_FG = '#2B2B2B'           # Foreground Ruins
C_FIRE_1 = '#FF003C'            # Red Entropy
C_FIRE_2 = '#FF7700'            # Orange Entropy
C_FIRE_3 = '#FFD700'            # Gold Entropy
C_GOLD = '#FFD700'              # UI Gold
C_CYAN = '#00FFCC'              # UI Cyan (The Fix)
C_MARINE = '#00FFCC'            # Cyan Terminal Precision
C_TEXT = '#FFFFFF'              # UI Readout
C_MANTIS = '#39FF14'            # Terminal Green

# -------- VIC-II SPRITE ARCHITECTURE (MICKEY MARINE) --------
# Frame 0: Legs separated | Frame 1: Legs together
SPRITE_MATRIX = [
    [
        "1000001",
        "1111111",
        "0111110",
        "0011100",
        "0111110",
        "1111111",
        "0111110",
        "0010100",
        "0100010"
    ],
    [
        "1000001",
        "1111111",
        "0111110",
        "0011100",
        "0111110",
        "1111111",
        "0111110",
        "0010100",
        "0010100"
    ]
]
PIXEL_SIZE = 18  # Scaling factor for the C-64 block look

def generate_skyline(width, max_height, block_w):
    h = 200
    points = []
    for x in range(0, width, block_w):
        # Stepped random walk for geometric ruins
        step = np.random.choice([-80, -40, 0, 40, 80])
        h = np.clip(h + step, 100, max_height)
        points.append((x, h))
    return points

def run():
    print(f"LOGIC GARDEN 135: FULL METAL JACKET 64")
    print(f"Executing: {FPS} FPS | Total: {TOTAL_FRAMES} frames")
    
    # Pre-compute Parallax Ruins
    np.random.seed(1987) # Compile-Time Safety (Year of Film Release)
    ruin_bg = generate_skyline(3000, 800, 60)
    ruin_fg = generate_skyline(3000, 500, 80)
    
    # Pre-compute Marine Squad (x offsets)
    squad_spacing = 250
    squad_x_offsets = [i * squad_spacing for i in range(5)]
    
    for f in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        fig.patch.set_facecolor(C_VOID)
        ax.set_facecolor(C_VOID)
        ax.set_xlim(0, 1080)
        ax.set_ylim(0, 1920)
        
        t_sec = f / FPS
        
        # ------------------------------------------------------------------
        # STAGE 1: PARALLAX RUINS & FIRE GENERATION
        # ------------------------------------------------------------------
        # BG Ruins (moves slow)
        bg_offset = (f * 0.5) % 1920
        for x, h in ruin_bg:
            rx = x - bg_offset
            if -100 < rx < 1180:
                ax.add_patch(plt.Rectangle((rx, 0), 60, h, color=C_RUIN_BG))
                
        # FG Ruins (moves faster)
        fg_offset = (f * 1.5) % 1920
        fire_x, fire_y, fire_c, fire_s = [], [], [], []
        
        for x, h in ruin_fg:
            rx = x - fg_offset
            if -100 < rx < 1180:
                ax.add_patch(plt.Rectangle((rx, 0), 80, h, color=C_RUIN_FG))
                # Generate Fire Entropy at base of foreground
                for _ in range(3):
                    fire_x.append(rx + np.random.randint(0, 80))
                    fire_y.append(h + np.random.randint(-20, 150))
                    fire_c.append(np.random.choice([C_FIRE_1, C_FIRE_2, C_FIRE_3]))
                    fire_s.append(np.random.randint(50, 250))
                    
        # Render the fire as scaled scatter blocks for pixel aesthetic
        if fire_x:
            ax.scatter(fire_x, fire_y, s=fire_s, c=fire_c, marker='s', alpha=0.8, edgecolors='none')

        # ------------------------------------------------------------------
        # STAGE 2: THE SQUAD MARCHO-ROUTINE
        # ------------------------------------------------------------------
        # Marching speed and animation state
        march_speed = 3.0
        global_x_offset = 1200 - (f * march_speed) 
        anim_frame = (f // 8) % 2  # Swap legs every 8 frames
        
        marine_px, marine_py = [], []
        
        for offset in squad_x_offsets:
            mx_base = global_x_offset + offset
            # Only draw if on screen
            if -200 < mx_base < 1280:
                my_base = 250 # Floor level
                # Parse the Sprite Array
                sprite = SPRITE_MATRIX[anim_frame]
                for row_idx, row in enumerate(sprite):
                    for col_idx, pixel in enumerate(row):
                        if pixel == "1":
                            # Flip horizontally so they march left
                            px = mx_base - (col_idx * PIXEL_SIZE) 
                            py = my_base + ((8 - row_idx) * PIXEL_SIZE * 1.5)
                            marine_px.append(px)
                            marine_py.append(py)
                            
        if marine_px:
            # Render Marines as Neon Cyan Terminals
            ax.scatter(marine_px, marine_py, s=PIXEL_SIZE*15, c=C_MARINE, marker='s', edgecolors='none')

        # ------------------------------------------------------------------
        # STAGE 3: UI DECOUPLING & THE MICKEY MOUSE LOGIC OVERLAY
        # ------------------------------------------------------------------
        # Rosetta Stone Header
        if t_sec < 1.0:
            ax.text(540, 1400, "PROTOCOL: CRITICAL DAMPING", color=C_GOLD, ha='center', fontsize=35, fontname='monospace', weight='bold')
            ax.text(540, 1300, "C-64 VIC-II EMULATION", color=C_CYAN, ha='center', fontsize=25, fontname='monospace')
            
        # The Song Matrix (Typography acting as system readout)
        lyric = ""
        c_lyric = C_TEXT
        if 2.0 <= t_sec < 5.0:
            lyric = "WHO'S THE LEADER OF THE CLUB"
        elif 5.5 <= t_sec < 8.5:
            lyric = "THAT'S MADE FOR YOU AND ME?"
        elif 9.0 <= t_sec < 12.0:
            lyric = "M - I - C"
            c_lyric = C_GOLD
        elif 12.5 <= t_sec < 15.5:
            lyric = "K - E - Y"
            c_lyric = C_GOLD
        elif 16.0 <= t_sec < 21.0:
            lyric = "M - O - U - S - E"
            c_lyric = C_MANTIS
            
        if lyric:
            # Glitch/Blink effect on text based on frame modulo
            if f % 4 != 0:
                ax.text(540, 1600, lyric, color=c_lyric, ha='center', fontsize=45, fontname='monospace', weight='bold')

        # Permanent HUD
        ax.text(80, 1820, f"FRAME: {f:04d} | HUE CITY", color=C_TEXT, fontsize=20, fontname='monospace')
        ax.text(80, 1780, f"ENTROPY OVERRIDE ACTIVE", color=C_MANTIS, fontsize=20, fontname='monospace')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close(fig)

if __name__ == "__main__": run()
