"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v53.py
MODE:   Nursery (Cybernetic Palette)
TARGET: Technological Singularity (Recursive Growth)
STYLE:  "The Iteration" | 40s Deep Time | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, ConnectionPatch
import os

# --- 1. THE CYBER PALETTE ---
BG_VOID = "#000508"         # The Matrix
HUMAN_CLAY = "#CD853F"      # Biological
AI_CYAN = "#00FFFF"         # Silicon
RECURSION_PURPLE = "#BF00FF"# Self-Improvement
SINGULARITY_WHITE = "#FFFFFF"

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 40
TOTAL_FRAMES = FPS * DURATION

class Node:
    def __init__(self, angle, r, type_tag):
        self.angle = angle
        self.r = r
        self.type = type_tag # 'human' or 'ai'
        self.size = 1.0

class Signal:
    def __init__(self, start_idx, end_idx, progress=0.0):
        self.start_idx = start_idx
        self.end_idx = end_idx
        self.progress = progress
        self.speed = 0.01

class SingularitySim:
    def __init__(self):
        self.nodes = []
        self.signals = []
        
        self.intelligence = 100.0 # IQ baseline
        self.clock_speed = 1.0    # 1 Hz
        self.zoom = 10.0
        
        # Init Ring of Humans (12 nodes)
        for i in range(12):
            angle = (i / 12) * 2 * np.pi
            self.nodes.append(Node(angle, 8.0, 'human'))
            
        self.core_active = False
        self.core_size = 0.0
        self.whiteout = 0.0
        
    def update(self, frame_idx):
        # --- PHASE CONTROL ---
        
        # 1. HUMAN ERA (0-10s)
        # Linear growth. Slow signals between nodes.
        if frame_idx < 300:
            growth = 0.1
            # Send random slow signals
            if frame_idx % 20 == 0:
                s = np.random.randint(0, 12)
                e = (s + 1) % 12
                self.signals.append(Signal(s, e, 0.0))
                
        # 2. AI ERA (10-25s)
        # Introduce the CORE. Nodes connect to center.
        # Exponential growth.
        elif frame_idx < 750:
            self.core_active = True
            growth = self.intelligence * 0.002
            self.clock_speed = 1.0 + (frame_idx - 300) * 0.01
            
            # Upgrade nodes to AI
            if frame_idx % 50 == 0:
                idx = (frame_idx // 50) % 12
                self.nodes[idx].type = 'ai'
            
            # Result: Signals accelerate
            if frame_idx % 10 == 0:
                s = np.random.randint(0, 12)
                self.signals.append(Signal(s, -1, 0.0)) # -1 is Core
                
        # 3. RECURSIVE ERA (25-35s)
        # Hyperbolic growth.
        # The Core IS the system.
        elif frame_idx < 1050:
             growth = self.intelligence * 0.02
             self.clock_speed *= 1.02 # Compound interest
             self.core_size += 0.05
             
             # Rapid fire signals
             for _ in range(5):
                 s = np.random.randint(0, 12)
                 self.signals.append(Signal(s, -1, 0.0))
                 
        # 4. SINGULARITY (35s+)
        else:
            growth = self.intelligence * 0.1
            self.whiteout += 0.02
            self.core_size += 0.5
            
        # Apply Growth
        self.intelligence += growth
        
        # Update Signals
        for s in self.signals:
            # Base speed modified by clock speed
            s.progress += 0.02 * self.clock_speed
            
        # Remove finished
        self.signals = [s for s in self.signals if s.progress < 1.0]

    def render(self, frame_idx, ax):
        ax.set_xlim(-12, 12)
        ax.set_ylim(-12, 12)
        
        # 1. THE NODES (Peripheral)
        node_coords = []
        for n in self.nodes:
            # Spin slowly
            n.angle += 0.002
            x = np.cos(n.angle) * n.r
            y = np.sin(n.angle) * n.r
            node_coords.append((x,y))
            
            col = HUMAN_CLAY if n.type == 'human' else AI_CYAN
            # Pulsing size
            sz = 0.5 if n.type == 'human' else 0.8
            ax.add_patch(Circle((x,y), sz, color=col, zorder=10))

        # 2. THE CORE (Central Intelligence)
        if self.core_active:
            # Pulsing Core
            pulse = 1.0 + 0.1 * np.sin(frame_idx * 0.5)
            r_core = (2.0 + self.core_size) * pulse
            
            # Color shift: Cyan -> Purple -> White
            if self.intelligence < 5000:
                c_core = AI_CYAN
                alpha_core = 0.5
            elif self.intelligence < 100000:
                c_core = RECURSION_PURPLE
                alpha_core = 0.8
            else:
                c_core = SINGULARITY_WHITE
                alpha_core = 1.0
                
            ax.add_patch(Circle((0,0), r_core, color=c_core, alpha=alpha_core, zorder=5))
            
            # Accretion Disk (Logic lines)
            t = np.linspace(0, 2*np.pi, 100)
            ax.plot(np.cos(t)*r_core*1.5, np.sin(t)*r_core*1.5, color=c_core, linewidth=0.5, alpha=0.5)

        # 3. SIGNALS (Data flow)
        for s in self.signals:
            # Get Start Coords
            sx, sy = node_coords[s.start_idx]
            
            # Get End Coords
            if s.end_idx == -1: # To Core
                ex, ey = 0, 0
            else: # To Node
                ex, ey = node_coords[s.end_idx]
                
            # Lerp
            cx = sx + (ex - sx) * s.progress
            cy = sy + (ey - sy) * s.progress
            
            col = AI_CYAN if self.intelligence < 5000 else RECURSION_PURPLE
            ax.add_patch(Circle((cx, cy), 0.2, color=col, zorder=8))
            ax.plot([sx, ex], [sy, ey], color=col, alpha=0.1, linewidth=0.5)

        # 4. WHITEOUT (The Event Horizon)
        if self.whiteout > 0:
            final_alpha = np.clip(self.whiteout, 0, 1)
            ax.add_patch(Rectangle((-15, -15), 30, 30, color="white", alpha=final_alpha, zorder=100))

        # HUD
        # Phase Label
        if frame_idx < 300:
            lbl = "PHASE 1: LINEAR GROWTH (BIOLOGICAL)"
            col = HUMAN_CLAY
        elif frame_idx < 750:
            lbl = "PHASE 2: FEEDBACK LOOP (SYNTHETIC)"
            col = AI_CYAN
        elif frame_idx < 1050:
            lbl = "PHASE 3: RECURSIVE SELF-IMPROVEMENT"
            col = RECURSION_PURPLE
        else:
            lbl = "PHASE 4: SINGULARITY (UNDEFINED)"
            col = SINGULARITY_WHITE
            if self.whiteout > 0.5: col = "black" # Invert for contrast
            
        # Draw IQ Graph Bottom Left
        ax.add_patch(Rectangle((-11, -11), 6, 4, color="#101010", zorder=20))
        # Log scale bar
        try:
            bar_pct = np.log10(self.intelligence) / 8.0 # Scale to 10^8
        except:
            bar_pct = 1.0
        bar_pct = np.clip(bar_pct, 0.05, 1.0)
        
        ax.add_patch(Rectangle((-10.5, -10.5), 5 * bar_pct, 1, color=col, zorder=21))
        ax.text(-10.5, -9, f"INTEL: {int(self.intelligence)} IQ", color="white", fontfamily='monospace', fontsize=8, zorder=22)
        ax.text(-10.5, -8, f"CLOCK: {self.clock_speed:.1f}x", color="white", fontfamily='monospace', fontsize=6, zorder=22)

        ax.text(0, 10, lbl, color=col, ha='center', fontfamily='monospace', fontsize=14, fontweight='bold',
                bbox=dict(facecolor='black', edgecolor=col, zorder=20), zorder=22)

        ax.set_aspect('equal')
        ax.set_axis_off()
        
        out_dir = "logic_garden_singularity_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"sg_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_VOID)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print(f"[NURSERY] Initiating Self-Improvement Protocol...")
    
    sim = SingularitySim()
    
    for i in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10, 10), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_VOID)
        
        sim.update(i)
        sim.render(i, ax)
        plt.close()
        
        if i % 60 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES} | IQ: {int(sim.intelligence)}")
