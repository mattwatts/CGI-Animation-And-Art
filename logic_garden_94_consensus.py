"""
SOVEREIGN CODE: logic_garden_94_consensus.py
FORMAT: YouTube Shorts (9:16)
CONTEXT: Wikipedia Edit Wars / Hegelian Dialectic
VISUAL: Red/Blue Conflict -> Lock -> Purple Synthesis
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import random

FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_94_consensus"
os.makedirs(OUT_DIR, exist_ok=True)

# Grid Params (Blocky Aesthetics)
GW, GH = 30, 50 

def run():
    print("LOGIC GARDEN 94: THE CONSENSUS ENGINE")
    
    # Init Grid (0 = Neutral, -1 = Blue, 1 = Red)
    grid = np.zeros((GH, GW))
    
    for f in range(TOTAL_FRAMES):
        # FIGURE SETUP
        fig = plt.figure(figsize=(9, 16), facecolor='#111111')
        ax = fig.add_axes([0, 0, 1, 1], facecolor='#111111')
        ax.set_ylim(GH, 0) # Flip Y
        ax.set_xlim(0, GW)
        ax.axis('off')
        
        # TIME PHASES
        # 0 - 240: WAR (Chaos)
        # 240 - 360: LOCK (Freeze)
        # 360 - 600: SYNTHESIS (Resolution)
        
        phase = "WAR"
        if f < 240:
            # EDIT WAR LOGIC
            # Random patches flip color
            num_edits = 10
            for _ in range(num_edits):
                # Pick a random patch
                x = random.randint(0, GW-5)
                y = random.randint(0, GH-5)
                w = random.randint(2, 8)
                h = random.randint(2, 8)
                
                # Team Red or Team Blue?
                # Oscillate dominance based on time
                bias = np.sin(f * 0.1) # -1 to 1
                team = 1 if random.random() > 0.5 - (bias*0.2) else -1
                
                grid[y:y+h, x:x+w] = team
                
        elif f < 360:
            phase = "LOCK"
            # Grid doesn't change. It is frozen.
            
        else:
            phase = "SYNTHESIS"
            # Smoothly blend everything to Purple (0)
            # We decay the values towards 0
            grid = grid * 0.95
            
            # Add "High Res" noise/texture to look like a solid document?
            # Or just let it fade to uniform stability.
            
        # RENDER GRID
        # We need a custom colormap: Blue -> Red via Purple?
        # No, Blue (-1) ... Purple (0) ... Red (1)
        # We construct a colored image buffer manually for control
        
        img = np.zeros((GH, GW, 3))
        
        for y in range(GH):
            for x in range(GW):
                val = grid[y, x]
                # Map val (-1 to 1) to RGB
                # -1 (Blue): [0, 0, 1]
                # 1 (Red):   [1, 0, 0]
                # 0 (Purple): [0.5, 0, 0.5] -- Wait, neutral is usually grey or black?
                # Let's make 0 = Purple [0.6, 0.0, 0.8] representing "Truth"
                
                # Simple interpolation is tricky with 3 targets.
                # Let's simple logic:
                if phase == "SYNTHESIS":
                   # Lerp towards purple based on how close to 0
                   # Abs(val) is distance from Truth
                   mix = abs(val) # 1.0 = Pure Red/Blue, 0.0 = Truth
                   # Base Purple
                   r, g, b = 0.6, 0.0, 0.8
                   # Add error color
                   if val > 0: # Red tint
                       r = 0.6 + 0.4*mix
                       b = 0.8 - 0.8*mix
                   else: # Blue tint
                       b = 0.8 + 0.2*mix
                       r = 0.6 - 0.6*mix
                else:
                    # Harsh Binary Conflicts
                    if val > 0.2: # RED
                        r, g, b = 1.0, 0.0, 0.2
                    elif val < -0.2: # BLUE
                        r, g, b = 0.0, 0.4, 1.0
                    else: # Grey/Void
                        r, g, b = 0.1, 0.1, 0.1
                        
                img[y, x] = [r, g, b]
                
        ax.imshow(img, interpolation='nearest', aspect='auto')
        
        # DRAW LOCK ICON (Phase 2 only)
        if phase == "LOCK" or (phase == "SYNTHESIS" and f < 400):
            # Draw a geometric padlock
            # Body
            rect = plt.Rectangle((GW/2 - 4, GH/2 - 2), 8, 6, color='white', alpha=0.9)
            ax.add_patch(rect)
            # Shackle
            arc = matplotlib.patches.Arc((GW/2, GH/2 - 2), 6, 6, theta1=0, theta2=180, 
                                        color='white', linewidth=4)
            ax.add_patch(arc)
            
            label = "PROTECTED"
            col = "white"
        
        elif phase == "WAR":
            label = "EDIT WAR"
            col = "#FF4444"
            if (f // 5) % 2 == 0: col = "#4444FF" # Flash
            
        else:
            label = "SYNTHESIS"
            col = "#D040E0" # Neon Purple
            
        # TEXT
        ax.text(GW/2, GH - 2, label, color=col, ha='center', fontsize=30, weight='bold', fontfamily='monospace',
               bbox=dict(facecolor='black', alpha=0.5, edgecolor='none'))

        fig.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), dpi=80, facecolor='#111111')
        plt.close(fig)

if __name__ == "__main__": run()
