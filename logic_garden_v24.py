"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v24_loop.py
MODE:   Nursery (Ochre Bauhaus Palette)
TARGET: Indigenous Knowledge Systems (Songlines / Graph Theory)
STYLE:  "The Living Map" (Seamless Loop) | High Contrast | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, ConnectionPatch
import os

# --- 1. THE OCHRE PALETTE ---
BG_COLOR = "#000000"        # The Dreamtime (Void)
NODE_COLOR = "#FFFFFF"      # Waterhole (Knowledge)
PATH_COLOR = "#A52A2A"      # Red Ochre (The Path)
WALKER_COLOR = "#FFD700"    # Yellow Ochre (The Singer)
RIPPLE_COLOR = "#888888"    # The Echo

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20 # 20 Seconds
TOTAL_FRAMES = FPS * DURATION
NUM_NODES = 8 # Extended song

class SonglineSim:
    def __init__(self):
        # 1. Generate The Landscape (Immutable Map)
        np.random.seed(101) # A good seed for spacing
        
        # Random positions constrained to screen safe area
        self.nodes_x = np.random.rand(NUM_NODES) * 12 - 6
        self.nodes_y = np.random.rand(NUM_NODES) * 6 - 3
        
        # 2. Define The Song (The Order of Visitation)
        # A simple closed loop connecting nearest random neighbours visually
        # This order creates a nice winding path without too many cross-overs
        self.path_order = [0, 4, 1, 5, 2, 7, 3, 6, 0] # Ends at 0 for loop
        
        # 3. Calculate The Geometry
        self.segments = []
        self.cumulative_dist = [0.0]
        self.total_dist = 0.0
        
        for i in range(len(self.path_order) - 1):
            u = self.path_order[i]
            v = self.path_order[i+1]
            
            p1 = np.array([self.nodes_x[u], self.nodes_y[u]])
            p2 = np.array([self.nodes_x[v], self.nodes_y[v]])
            
            d = np.linalg.norm(p2 - p1)
            self.segments.append({
                'start': p1, 'end': p2, 
                'len': d, 
                'u': u, 'v': v
            })
            self.total_dist += d
            self.cumulative_dist.append(self.total_dist)

    def get_state(self, frame_idx):
        # Time 0.0 to 1.0
        # We want strict seamless loop. 
        # T=0 is Start Node 0. T=1 is End Node 0.
        
        t = (frame_idx % TOTAL_FRAMES) / TOTAL_FRAMES
        current_d = t * self.total_dist
        
        # Find segment
        pos = np.array([0.0, 0.0])
        active_segment_idx = 0
        
        for i, seg in enumerate(self.segments):
            seg_start_d = self.cumulative_dist[i]
            seg_end_d = self.cumulative_dist[i+1]
            
            if seg_start_d <= current_d <= seg_end_d:
                # Interpolate
                local_t = (current_d - seg_start_d) / seg['len']
                pos = seg['start'] + (seg['end'] - seg['start']) * local_t
                active_segment_idx = i
                break
                
        # Calculate Pulse States (Deterministic for Looping)
        # A node pulses if the walker passed it recently
        # We need to handle the "Wrap Around" pulse for Node 0
        node_pulses = np.zeros(NUM_NODES)
        
        for i, node_idx in enumerate(self.path_order[:-1]): # Ignore the duplicate end 0
            # When did we hit this node?
            hit_dist = self.cumulative_dist[i]
            
            # Distance from walker to this hit event
            delta = current_d - hit_dist
            
            # Handle Wrap-around logic for Node 0 logic?
            # Actually, standard logic:
            # If delta is small positive, we just hit it.
            # Decay over distance 2.0 units
            
            if 0 < delta < 2.0:
                strength = 1.0 - (delta / 2.0)
                node_pulses[node_idx] = max(node_pulses[node_idx], strength)
                
            # Special case for the Loop Point (Node 0) at the very end
            # If current_d is near total_dist, it effectively hits Node 0 again
            delta_end = (current_d - self.total_dist) 
            # This will be negative, bringing us to T=1.
            # But visually, Node 0 should pulse at T=0.
            # Let's check "Time since T=0"
            
            if i == 0:
                 # We are at start.
                 # Hit happened at distance 0.
                 delta_start = current_d
                 if 0 <= delta_start < 2.0:
                      node_pulses[node_idx] = max(node_pulses[node_idx], 1.0 - (delta_start/2.0))
        
        return pos, node_pulses

    def render(self, frame_idx, ax):
        pos, pulses = self.get_state(frame_idx)
        
        # 1. Draw The Dream (Lines)
        for seg in self.segments:
            # Dashed or Solid? Solid Earth.
            ax.plot([seg['start'][0], seg['end'][0]], 
                    [seg['start'][1], seg['end'][1]], 
                    color=PATH_COLOR, linewidth=3, zorder=1, alpha=0.5)

        # 2. Draw The Waterholes (Nodes)
        for i in range(NUM_NODES):
            x, y = self.nodes_x[i], self.nodes_y[i]
            # Concentric motif
            
            # Outer Ring
            ax.add_patch(Circle((x, y), 0.35, facecolor="black", edgecolor=NODE_COLOR, linewidth=2, zorder=5))
            # Inner Dot
            ax.add_patch(Circle((x, y), 0.12, facecolor=NODE_COLOR, zorder=6))
            
            # 3. Draw The Echo (Pulses)
            p = pulses[i]
            if p > 0.01:
                # Radius expands as strength drops (Time moves forward)
                # strength = 1 - (delta/2). So delta/2 = 1 - strength.
                # expansion = (1-strength) * scale
                expansion = (1.0 - p) * 1.5
                r = 0.35 + expansion
                alpha = p # Fade out
                
                ax.add_patch(Circle((x, y), r, color=RIPPLE_COLOR, fill=False, linewidth=2, alpha=alpha, zorder=4))
                # Second Echo
                if p < 0.8:
                     ax.add_patch(Circle((x, y), r*0.7, color=RIPPLE_COLOR, fill=False, linewidth=1, alpha=alpha*0.5, zorder=4))

        # 4. Draw The Singer (Walker)
        ax.add_patch(Circle((pos[0], pos[1]), 0.2, color=WALKER_COLOR, zorder=10))
        # Glow
        ax.add_patch(Circle((pos[0], pos[1]), 0.5, color=WALKER_COLOR, alpha=0.2, zorder=9))

        # Scale
        ax.set_xlim(-7, 7)
        ax.set_ylim(-4, 4)
        ax.set_aspect('equal')
        
        # Save
        out_dir = "logic_garden_songline_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"song_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("[NURSERY] Walking the Infinite Songline...")
    
    sim = SonglineSim()
    
    for i in range(TOTAL_FRAMES):
        # 1. Canvas
        fig = plt.figure(figsize=(16, 9), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        sim.render(i, ax)
        
        if i % 30 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
