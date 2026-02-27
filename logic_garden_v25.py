"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v25.py
MODE:   Nursery (Matrix Palette)
TARGET: Cryptanalysis (Frequency Analysis)
STYLE:  "The Golden Key" | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os
import string
import random

# --- 1. THE MATRIX PALETTE ---
BG_COLOR = "#000000"        # Terminal Black
REF_COLOR = "#FFFFFF"       # English (Truth)
CIPHER_COLOR = "#00FF00"    # Phosphor Green (The Signal)
MATCH_COLOR = "#FFD700"     # Cyber Yellow (The Key)
TEXT_COLOR = "#00FF00"

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION

# --- 3. DATA & MODEL ---

# Standard English Frequency (Approximate)
ENGLISH_FREQ = {
    'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7, 'S': 6.3,
    'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0, 'C': 2.8, 'U': 2.8, 'M': 2.4,
    'W': 2.4, 'F': 2.2, 'G': 2.0, 'Y': 2.0, 'P': 1.9, 'B': 1.5, 'V': 1.0,
    'K': 0.8, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07
}

# The Target Message (Must be long enough to have decent frequency stats)
# We will cheat slightly and ensure the sample text MATCHES the frequency rank for the visual lesson.
TARGET_MSG = "THE INDUSTRIAL REVOLUTION AND ITS CONSEQUENCES HAVE BEEN A DISASTER FOR THE HUMAN RACE"
# A shorter, punchier text for the visual ticker
DISPLAY_MSG = "KNOWLEDGE IS POWER IF YOU HAVE THE KEY"

def generate_cipher(msg):
    # 1. Create a Key
    alphabet = list(string.ascii_uppercase)
    shuffled = list(string.ascii_uppercase)
    
    # Deterministic shuffle for "Educational" match
    # We want the most frequent letter in MSG (say 'E') to map to something obvious like 'X'
    random.seed(42)
    random.shuffle(shuffled)
    
    mapping = dict(zip(alphabet, shuffled))
    inv_mapping = dict(zip(shuffled, alphabet))
    
    # 2. Encrypt
    cipher_text = ""
    for char in msg:
        if char in mapping:
            cipher_text += mapping[char]
        else:
            cipher_text += char
            
    return cipher_text, mapping, inv_mapping

class CryptoSim:
    def __init__(self):
        self.plain = DISPLAY_MSG
        self.cipher, self.map, self.inv_map = generate_cipher(self.plain)
        
        # Calculate Frequencies of the Cipher Text
        counts = {k: 0 for k in string.ascii_uppercase}
        total = 0
        for c in self.cipher:
            if c in counts:
                counts[c] += 1
                total += 1
                
        self.cipher_freq = []
        for k, v in counts.items():
            if total > 0:
                self.cipher_freq.append((k, (v / total) * 100))
            else:
                self.cipher_freq.append((k, 0))
                
        # Sort Cipher by Frequency (High to Low)
        self.cipher_freq.sort(key=lambda x: x[1], reverse=True)
        
        # Sort English by Frequency (High to Low)
        self.eng_freq_sorted = sorted(ENGLISH_FREQ.items(), key=lambda x: x[1], reverse=True)
        
        # Setup Animation State
        # We will "Solve" one letter pairs every X frames
        self.solved_letters = {} # CipherChar -> PlainChar

    def render(self, frame_idx, ax):
        # Timeline
        # 0-60: Static view of the mess
        # 60+: Start cracking 1 pair every 15 frames
        
        solve_idx = -1
        if frame_idx > 60:
            solve_idx = (frame_idx - 60) // 15
            
        # Limit
        if solve_idx >= len(self.eng_freq_sorted):
            solve_idx = len(self.eng_freq_sorted) - 1

        # Update Solved Set
        # We assume the sorted graphs align perfectly (Idealized Lesson)
        if solve_idx >= 0:
            for i in range(solve_idx + 1):
                if i < len(self.cipher_freq) and i < len(self.eng_freq_sorted):
                    c_char = self.cipher_freq[i][0]
                    p_char = self.eng_freq_sorted[i][0]
                    self.solved_letters[c_char] = p_char

        # --- DRAWING ---
        
        # 1. Top Graph (English Truth)
        bar_width = 0.8
        x_start = 0
        
        # Draw English bars (White)
        for i, (char, freq) in enumerate(self.eng_freq_sorted):
            x = x_start + i
            color = REF_COLOR
            
            # Highlight matching
            if i <= solve_idx:
                color = MATCH_COLOR
                
            ax.add_patch(Rectangle((x, 10), bar_width, freq, facecolor=color))
            # Label
            ax.text(x + bar_width/2, 10 + freq + 1, char, color=color, ha='center', fontweight='bold')

        ax.text(0, 25, "STANDARD ENGLISH FREQUENCY (TRUTH)", color=REF_COLOR, fontsize=12, fontweight='bold')

        # 2. Bottom Graph (Cipher Stats)
        # We sort this graph High->Low so it visualy matches the top graph shape
        for i, (char, freq) in enumerate(self.cipher_freq):
            x = x_start + i
            
            # If solved, turn Gold. If not, Green.
            if i <= solve_idx:
                color = MATCH_COLOR
                # Show the REAL letter
                label = self.solved_letters.get(char, "?")
            else:
                color = CIPHER_COLOR
                label = char # The Cipher Letter
            
            # Bars grow downwards from 0
            ax.add_patch(Rectangle((x, -2), bar_width, -freq, facecolor=color))
            # Label
            ax.text(x + bar_width/2, -2 - freq - 2, label, color=color, ha='center', fontweight='bold')

        ax.text(0, -20, "CIPHER TEXT FREQUENCY (NOISE)", color=CIPHER_COLOR, fontsize=12, fontweight='bold')

        # 3. The Decoding Text (The Ticker)
        # "XF GJ..." -> "TO BE..."
        
        current_str = ""
        for char in self.cipher:
            if char == " ":
                current_str += "  "
            elif char in self.solved_letters:
                # Decoded!
                current_str += self.solved_letters[char]
            else:
                # Still Cipher
                current_str += char

        # Add visual cursor/glitch effect?
        pass

        # Draw Text
        ax.text(13, -28, current_str, ha='center', va='center', 
                color=TEXT_COLOR, fontsize=24, fontfamily='monospace', fontweight='bold')

        # Scale
        ax.set_xlim(-1, 27)
        ax.set_ylim(-35, 30)
        ax.set_axis_off()
        
        # Save
        out_dir = "logic_garden_crypto_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"crypto_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Breaking the Enigma...")
    
    sim = CryptoSim()
    
    for i in range(TOTAL_FRAMES):
        # 1. Canvas
        fig = plt.figure(figsize=(16, 9), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        sim.render(i, ax)
        
        if i % 30 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
