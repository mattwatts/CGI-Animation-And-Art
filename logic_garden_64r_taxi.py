"""
SOVEREIGN CODE: logic_garden_64r_taxi.py
FORMAT: YouTube Shorts (9:16)
SYSTEM: C64 VIC-II Emulation
SCENE: Taxi Driver ("You talkin' to me?")
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import random

# C64 PALETTE
COLORS = {
    0:  [0, 0, 0],       # Black
    1:  [255, 255, 255], # White
    2:  [136, 0, 0],     # Red
    3:  [170, 255, 238], # Cyan
    4:  [204, 68, 204],  # Purple
    5:  [0, 204, 85],    # Green (Jacket)
    6:  [0, 0, 170],     # Blue
    7:  [238, 238, 119], # Yellow
    8:  [221, 136, 85],  # Orange (Skin)
    9:  [102, 68, 0],    # Brown (Wall)
    10: [255, 119, 119], # Light Red
    11: [51, 51, 51],    # Dark Grey (Shadows)
    12: [119, 119, 119], # Grey (Gun/Slider)
    13: [170, 255, 102], # Light Green
    14: [0, 136, 255],   # Light Blue
    15: [187, 187, 187]  # Light Grey (Mirror)
}

# CONFIG
FPS = 15
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_64r_taxi"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 110, 196 
GRID = np.zeros((H, W, 3), dtype=np.uint8)

def draw_rect(canvas, x, y, w, h, c_id):
    x, y, w, h = int(x), int(y), int(w), int(h)
    x1 = max(0, x)
    y1 = max(0, y)
    x2 = min(W, x+w)
    y2 = min(H, y+h)
    if x1 < x2 and y1 < y2:
        canvas[y1:y2, x1:x2] = COLORS[c_id]

def draw_travis(canvas, x, y, pose, talk_frame):
    # Travis Bickle Reflection
    # Center x, y is Approx Chest level
    
    # 1. HEAD
    # Neck
    draw_rect(canvas, x-4, y-20, 8, 6, 8) 
    # Face (Orange #8)
    draw_rect(canvas, x-7, y-36, 14, 18, 8)
    
    # Mohawk (Black #0)
    # Strip down center
    draw_rect(canvas, x-2, y-40, 4, 6, 0)
    # Shaved sides (Lighter orange/grey mix? Just skin)
    
    # Sunglasses? (Aviators) - No, eyes are scarier here.
    # Eyes (Black pixels)
    draw_rect(canvas, x-4, y-30, 2, 2, 0)
    draw_rect(canvas, x+2, y-30, 2, 2, 0)
    
    # Mouth
    if pose == "TALK":
        if talk_frame % 4 < 2:
            draw_rect(canvas, x-3, y-24, 6, 2, 0) # Open
        else:
            draw_rect(canvas, x-3, y-24, 6, 1, 0) # Closed
    elif pose == "SMILE":
        # Creepy grin
        draw_rect(canvas, x-4, y-24, 8, 1, 0) # Line
        draw_rect(canvas, x-5, y-25, 1, 1, 0) # Corner up
        draw_rect(canvas, x+4, y-25, 1, 1, 0)
    else:
        # Straight line
        draw_rect(canvas, x-3, y-24, 6, 1, 0)

    # 2. BODY (M-65 Jacket - Green #5)
    # Shoulders
    draw_rect(canvas, x-16, y-14, 32, 40, 5)
    # Collar (Darker Green/Grey #11)
    draw_rect(canvas, x-12, y-14, 24, 4, 11)
    # Zipper line
    draw_rect(canvas, x, y-10, 1, 36, 11)
    # Epaulets
    draw_rect(canvas, x-14, y-12, 4, 2, 11)
    draw_rect(canvas, x+10, y-12, 4, 2, 11)
    
    # King Kong Patch? (Too small)
    # "We Are The People" Button (Red/White pixel)
    draw_rect(canvas, x-10, y-4, 3, 3, 10) # Red
    draw_rect(canvas, x-9, y-3, 1, 1, 1) # White dot
    
    # 3. ARMS & GUN
    # Right Arm (Viewer's Left in mirror? Mirror logic is tricky)
    # Reflection: Right arm moves = Reflection's Left side moves.
    
    arm_y = y + 5
    
    if pose == "DRAW":
        # Arm raised, pointing at mirror
        # Sleeve extends forward (Perspective: circle/square)
        draw_rect(canvas, x+8, arm_y-10, 12, 8, 5) # Sleeve
        
        # The Mechanism (Grey slider)
        draw_rect(canvas, x+12, arm_y-12, 14, 4, 12) # Rail
        
        # The Gun (Small darker grey/black)
        draw_rect(canvas, x+20, arm_y-14, 4, 6, 0) # Muzzle
        
    elif pose == "HIDDEN":
         # Hands acting tough
         # Hands in pockets or just hanging
         draw_rect(canvas, x-20, arm_y, 4, 25, 5) # L Arm
         draw_rect(canvas, x+16, arm_y, 4, 25, 5) # R Arm

def run():
    print("LOGIC GARDEN 64r: TAXI DRIVER")
    
    # INIT WALL
    # Grime pattern
    WALL_TEX = np.zeros((H, W), dtype=int)
    for y in range(H):
        for x in range(W):
            r = random.random()
            if r > 0.9: WALL_TEX[y, x] = 11 # Dark stain
            elif r > 0.6: WALL_TEX[y, x] = 9 # Brown
            else: WALL_TEX[y, x] = 12 # Grey/Plaster
            
            
    for f in range(TOTAL_FRAMES):
        # 1. DRAW ROOM (WALL)
        for y in range(H):
            for x in range(W):
                GRID[y, x] = COLORS[WALL_TEX[y, x]]
                
        # 2. DRAW MIRROR
        # A lighter rectangle in center
        mx, my, mw, mh = 10, 20, 90, 120
        draw_rect(GRID, mx, my, mw, mh, 15) # Light Grey Glass
        # Reflection tint? (Slightly darker)
        # We just draw the reflection on top.
        
        # Mirror Frame (Wood)
        draw_rect(GRID, mx-2, my, 2, mh, 8) # Left
        draw_rect(GRID, mx+mw, my, 2, mh, 8) # Right
        draw_rect(GRID, mx-2, my-2, mw+4, 2, 8) # Top
        draw_rect(GRID, mx-2, my+mh, mw+4, 2, 8) # Bot
        
        # 3. TRAVIS LOGIC
        # 0-60: Look Left, Right ("You talkin' to me?")
        # 60-120: "I don't see anyone else." (Shrug/Gestures)
        # 120-130: THE DRAW (Snap)
        # 130-180: Pointing, Smiling
        
        tx = W // 2
        ty = 100
        pose = "HIDDEN"
        
        # Head movement
        head_offset_x = 0
        
        if f < 30:
            # Idle
            pass
        elif f < 45:
            # Look Left
            head_offset_x = -2
            pose = "TALK"
        elif f < 60:
            # Look Right
            head_offset_x = 2
            pose = "TALK"
        elif f < 90:
            # Center, Talking
            pose = "TALK"
            if (f % 10) < 5: head_offset_x = 0
            else: head_offset_x = 1 # Bob
        elif f < 120:
            # Silence. Look.
            pose = "IDLE"
        elif f < 130:
            # THE DRAW (Fast!)
            pose = "DRAW"
            # Shake screen?
            if f % 2 == 0: ty += 1
        else:
            pose = "DRAW"
            # Smile slowly appears
            if f > 150: 
               # We override mouth in draw_travis using SMILE param or specialized call
               # But draw_travis logic uses 'pose' for body and checks lips..
               # Let's add SMILE to DRAW logic?
               # Simpler: Modify the function to seperate face/body.
               # For now, let's just make his mouth pixel open.
               pass

        # Call Draw
        # We handle "SMILE" via a hack in the argument or just modify the function above.
        # Actually I added "SMILE" as a pose in draw_travis for mouth, but it conflicts with body "DRAW".
        # Let's fix draw_travis to separate Face/Body? 
        # Or just pass a combined state.
        
        render_pose = pose
        if f > 150: render_pose = "SMILE" # But this will reset body to default lines in my code!
        # My code: if pose == "DRAW"... else if pose == "SMILE"...
        # Correction needed.
        
        # Let's hack the pose string for the function:
        if f > 150: 
             # I need body DRAW and face SMILE.
             # I will modify the function call to handle this specifically? 
             # No, simply:
             pass 

        # Drawing Travis
        # Apply head offset
        draw_travis(GRID, tx + head_offset_x, ty, pose, f)
        
        # IF Smile needed (Body is DRAW, Face is SMILE)
        # Re-draw mouth
        if f > 150:
             # Overwrite mouth area
             draw_rect(GRID, tx+head_offset_x-4, ty-24, 8, 2, 8) # Erase (Skin)
             # Draw Smile
             draw_rect(GRID, tx+head_offset_x-4, ty-24, 8, 1, 0) # Line
             draw_rect(GRID, tx+head_offset_x-5, ty-25, 1, 1, 0) # Up
             draw_rect(GRID, tx+head_offset_x+4, ty-25, 1, 1, 0) # Up

        # 4. SUBTITLES (Typewriter style)
        text = ""
        if 30 < f < 90: text = "YOU TALKIN' TO ME?"
        elif 90 < f < 120: text = "I DON'T SEE ANYONE ELSE"
        
        if text:
            # Black Box
            draw_rect(GRID, 10, 150, 90, 20, 0)
            # Text dots (simulated)
            # Just some white pixels to represent text flow
            ln = len(text)
            chars_show = int((f % 60) / 2) # Typewriter speed
            if chars_show > ln: chars_show = ln
            
            caret_x = 15
            for i in range(chars_show):
                if text[i] != " ":
                     draw_rect(GRID, caret_x, 156, 3, 5, 1) # White char
                caret_x += 5

        # RENDER
        fig = plt.figure(figsize=(9, 16), dpi=80) 
        plt.figimage(GRID, resize=True, interpolation='nearest') 
        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor='black')
        plt.close(fig)

if __name__ == "__main__": run()
