"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v16.py
MODE:   Nursery (Bauhaus Palette)
TARGET: Number Theory (Sieve of Eratosthenes)
STYLE:  "The Unbreakable Numbers" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

# --- 1. THE NURSERY PALETTE ---
BG_COLOR = "#FFFFFF"        # Void
TEXT_COLOR = "#000000"      # Ink
ELIMINATED_COLOR = "#EEEEEE"# The Mud
ELIMINATED_TEXT = "#CCCCCC" # Faded Ink

# Prime Colors (Cyclical)
PRIME_PALETTE = ["#FF4500", "#0080FF", "#FFD700", "#000000"] 
# Red, Blue, Yellow, then Black for higher primes

# --- 2. CONFIGURATION ---
GRID_SIZE = 10 # 10x10 = 100
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION

class PrimeSieve:
    def __init__(self):
        self.limit = GRID_SIZE * GRID_SIZE
        self.numbers = np.arange(1, self.limit + 1)
        self.status = np.zeros(self.limit + 1, dtype=int) 
        # 0 = Unknown, 1 = Prime, 2 = Eliminated
        
        self.prime_colors = {} # Store assigned color for primes
        
        # 1 is not prime, not composite. Just Grey it out first.
        self.status[1] = 2 
        
    def get_coords(self, n):
        # Map number n (1-100) to (row, col)
        # 0-indexed for drawing
        # Grid layout: 
        # 1  2  3 ... 10
        # 11 12 13... 20
        idx = n - 1
        row = idx // GRID_SIZE
        col = idx % GRID_SIZE
        # Invert row for plotting (0 at bottom is default, we want 0 at top)
        # Actually easier to just draw and set Y axis inverted
        return col, row

    def run_algorithm(self):
        # Generator for animation steps
        
        # Pre-yield logic: 1 is grey
        yield {'current': 1, 'action': 'eliminate'}
        
        # Sieve
        for i in range(2, int(np.sqrt(self.limit)) + 1):
            if self.status[i] == 0:
                # Found a Prime!
                self.status[i] = 1
                yield {'current': i, 'action': 'found_prime'}
                
                # Eliminate multiples
                for j in range(i*i, self.limit + 1, i):
                    if self.status[j] == 0: # Only mark if not already marked
                        self.status[j] = 2 # Eliminated
                        yield {'current': j, 'action': 'eliminate', 'source': i}
                        
        # Mark remaining as prime
        for i in range(2, self.limit + 1):
            if self.status[i] == 0:
                self.status[i] = 1
                yield {'current': i, 'action': 'found_prime_late'}
                
        # Victory Lap
        yield {'current': None, 'action': 'finished'}

    def render(self, frame_idx, ax, current_focus=None, action=None):
        # 1. Draw Grid
        for n in range(1, self.limit + 1):
            col, row = self.get_coords(n)
            
            # Draw Box
            face = BG_COLOR
            text_c = TEXT_COLOR
            
            st = self.status[n]
            
            if st == 2: # Eliminated
                face = ELIMINATED_COLOR
                text_c = ELIMINATED_TEXT
            elif st == 1: # Prime
                # Deterministic color based on the number? or order?
                # Simple logic: If it's small, give specific color.
                if n == 2: face = PRIME_PALETTE[0]
                elif n == 3: face = PRIME_PALETTE[1]
                elif n == 5: face = PRIME_PALETTE[2]
                elif n == 7: face = "#000000" # Black key
                else: face = "#333333" # Dark Grey for higher primes
                
                text_c = "#FFFFFF" # White text on color
            
            # Highlight current focus (animation)
            if current_focus == n:
                if action == 'eliminate':
                    face = "#FFCCCC" # Flash fail
                elif action == 'found_prime':
                    # Scale effect?
                    pass

            # Rect
            # Note: In matplotlib, (x, y) is bottom-left. 
            # We want row 0 at top.
            # let's map row 0 -> y=9, row 9 -> y=0
            draw_y = (GRID_SIZE - 1) - row
            
            rect = Rectangle((col, draw_y), 1, 1, facecolor=face, edgecolor="#FFFFFF", linewidth=2)
            ax.add_patch(rect)
            
            # Text
            ax.text(col + 0.5, draw_y + 0.5, str(n), 
                    ha='center', va='center', 
                    color=text_c, fontsize=18, fontweight='bold', fontfamily='sans-serif')

        # Scale
        ax.set_xlim(0, GRID_SIZE)
        ax.set_ylim(0, GRID_SIZE)
        ax.set_aspect('equal')

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Filtering the Integers...")
    
    sieve = PrimeSieve()
    gen = sieve.run_algorithm()
    
    frame_idx = 0
    
    # We need to manually drive the generator and hold frames
    
    stop = False
    while not stop:
        try:
            step = next(gen)
            
            # How many frames per step?
            # Finding a prime: Long pause (Statement)
            # Eliminating: Fast (Machine gun)
            
            hold = 1
            if step['action'] == 'found_prime':
                hold = 20 # Pause for glory
            elif step['action'] == 'eliminate':
                hold = 2  # Pew pew
            elif step['action'] == 'found_prime_late':
                hold = 2 # Sweep up the rest fast
            elif step['action'] == 'finished':
                hold = 60 # End freeze
                stop = True
            
            for _ in range(hold):
                # 1. Canvas
                fig = plt.figure(figsize=(10, 10), dpi=100) # Square canvas for 16:9 box?
                # Actually let's keep 16:9 but center the grid
                fig = plt.figure(figsize=(16, 9), dpi=100)
                
                # Math to center 10x10 grid in 16x9 aspect
                # We render 10x10 into ax, then limits handle it?
                # Let's clean up limits.
                
                ax = plt.Axes(fig, [0., 0., 1., 1.])
                ax.set_axis_off()
                fig.add_axes(ax)
                ax.set_facecolor(BG_COLOR)
                
                # Render Grid
                # To center 0-10 on X axis of length 16...
                # Shift X limits? 
                
                sieve.render(frame_idx, ax, step['current'], step['action'])
                
                # Center calculation
                # Grid is width 10. Screen is ratio 16/9 * 10 (height) approx 17.7?
                # If we set ylim(0, 10), xlim needs to be 17.77 to match aspect.
                # Grid is 0-10. Center is 5.
                # X range should be 5 - (17.77/2) to 5 + (17.77/2)
                
                aspect_w = (16/9) * 10
                pad = (aspect_w - 10) / 2
                ax.set_xlim(-pad, 10 + pad)
                ax.set_ylim(0, 10)
                
                # Save
                out_dir = "logic_garden_sieve_frames"
                os.makedirs(out_dir, exist_ok=True)
                filename = os.path.join(out_dir, f"sieve_{frame_idx:04d}.png")
                plt.savefig(filename, facecolor=BG_COLOR)
                plt.close()
                frame_idx += 1
                
        except StopIteration:
            stop = True
            
    print(f"Total Frames: {frame_idx}")
