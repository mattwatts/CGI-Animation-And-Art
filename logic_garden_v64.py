"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v64.py
MODE:   Nursery (Probability Palette)
TARGET: Galton Board (Normal Distribution)
STYLE:  "The Rain of Truth" | 40s Deep Time | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# --- 1. THE PROBABILITY PALETTE ---
BG_VOID = "#121215"
PEG_GREY = "#404050"
RAIN_CYAN = "#00FFFF"
CURVE_MAGENTA = "#FF00FF"
BAR_FILL = "#008888"

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 40
TOTAL_FRAMES = FPS * DURATION
RES_X, RES_Y = 1920, 1080

class GaltonSim:
    def __init__(self):
        # Simulation Params
        self.rows = 12
        self.pegs_x = []
        self.pegs_y = []
        
        # Setup Pegs (Triangle)
        for r in range(self.rows):
            y = self.rows - r # Top is row 12, bottom row 1
            # Row 0 has 1 peg at 0
            # Row 1 has 2 pegs at -0.5, 0.5
            # Staggered grid
            count = r + 1
            start_x = -(count - 1) * 0.5
            for c in range(count):
                self.pegs_x.append(start_x + c)
                self.pegs_y.append(y)

        # Particles: List of [x, y, vx, vState]
        # vState = 0 (falling), 1 (landed)
        self.particles = np.zeros((0, 4)) 
        
        # Bins for histogram
        # Center of bins are integers from -rows/2 to rows/2
        self.bin_edges = np.arange(-(self.rows+1)/2, (self.rows+1)/2 + 1, 1)
        self.bins = np.zeros(len(self.bin_edges)-1)
        
        self.spawn_rate = 5 # Particles per frame
        self.speed = 0.15
        
    def pdf(self, x, total_count):
        # Theoretical Normal Distribution for Binomial(n, 0.5)
        # Mean = n * p = 0 (centered)
        # Variance = n * p * (1-p)
        # Actually, for range -n/2 to n/2 steps of +/- 0.5:
        # Variance is summed: Var = sum(0.5^2) * rows = 0.25 * rows
        # Sigma = sqrt(0.25 * rows) = 0.5 * sqrt(rows)
        
        sigma = 0.5 * np.sqrt(self.rows)
        mu = 0
        
        c = 1 / (sigma * np.sqrt(2 * np.pi))
        prob = c * np.exp(-0.5 * ((x - mu) / sigma)**2)
        
        # Scale by total count/area to match histogram
        # Histogram area = total_count * bin_width (1)
        return prob * total_count

    def update(self, frame_idx):
        # 1. SPAWN PARTICLES
        if frame_idx < TOTAL_FRAMES - 150: # Stop spawning near end
            new_p = np.zeros((self.spawn_rate, 4))
            new_p[:, 1] = self.rows + 1 # Start above top
            # Add small random jitter to X start to look natural
            new_p[:, 0] = np.random.normal(0, 0.05, self.spawn_rate)
            self.particles = np.vstack([self.particles, new_p])
            
        # 2. PHYSICS UPDATE
        # Filter active particles
        active = self.particles[:, 3] == 0
        landed = self.particles[:, 3] == 1
        
        if np.any(active):
            # Move Down
            self.particles[active, 1] -= self.speed
            
            # PEG LOGIC
            # If passing an integer Y level (roughly), jitter X
            # We check if they crossed a threshold (row - 0.5?)
            # Simplified: Since rows are integers 1..12
            # If (previous_y > row) and (current_y <= row)
            # Find the row integer
            
            prev_y = self.particles[active, 1] + self.speed
            curr_y = self.particles[active, 1]
            
            # Check integer crossing
            for r in range(1, self.rows + 1):
                # Trigger slightly above precision issues
                mask = (prev_y > r + 0.1) & (curr_y <= r + 0.1)
                
                # Apply Kick (Left or Right 0.5)
                # + Jitter for visuals
                if np.any(mask):
                    idx_mask = np.where(active)[0][mask]
                    
                    # Random choice -0.5 or 0.5
                    kicks = np.random.choice([-0.5, 0.5], size=len(idx_mask))
                    self.particles[idx_mask, 0] += kicks + np.random.normal(0, 0.02, size=len(idx_mask))

            # LANDING LOGIC
            # Ground is y = 0
            ground_mask = (curr_y <= 0) & active
            if np.any(ground_mask):
                idx_landed = np.where(active)[0][ground_mask] # Local mask indices
                # Actually, where provides indices into self.particles
                true_indices = np.where(ground_mask)[0] # Indices in active set? No.
                
                # Correct logic for partial update:
                # ground_mask is subset of active. 
                # We need indices in full array.
                full_indices = np.where(active)[0][np.where(curr_y[active[active]] <= 0 if False else (curr_y <= 0)[active[active]])] 
                # That's messy. Let's iterate all active.
                
                # Re-do specific mask logic safely
                hitting_ground = (self.particles[:, 1] <= 0) & (self.particles[:, 3] == 0)
                
                if np.count_nonzero(hitting_ground) > 0:
                    # Freeze
                    self.particles[hitting_ground, 3] = 1 
                    self.particles[hitting_ground, 1] = 0 # Snap to proper Y? 
                    # Actually we remove them from drawing array and add to Bin Counts for performance
                    # Calculate bin
                    x_vals = self.particles[hitting_ground, 0]
                    # Digitize
                    bin_indices = np.digitize(x_vals, self.bin_edges) - 1
                    
                    # Valid bins only
                    valid = (bin_indices >= 0) & (bin_indices < len(self.bins))
                    
                    # Update bins
                    for b in bin_indices[valid]:
                        self.bins[b] += 1
                        
                    # Visual Hack: Keep particles for a moment then delete? 
                    # To show accumulation, we keep "Landed" particles in the array 
                    # but maybe just let them pile up visually?
                    # The histogram bars will do the heavy lifting.
                    # Let's delete landed particles to save memory/render tim vs using rects
                    self.particles = self.particles[~hitting_ground]

    def render(self, frame_idx, ax):
        ax.set_xlim(-7, 7)
        ax.set_ylim(-2, 14) # -2 for bars
        
        # 1. DRAW PEGS
        ax.scatter(self.pegs_x, self.pegs_y, color=PEG_GREY, s=20, zorder=5)
        
        # 2. DRAW HISTOGRAM (The Accumulation)
        # Bar centers
        centers = (self.bin_edges[:-1] + self.bin_edges[1:]) / 2
        
        # Scale histogram height to not overlap pegs immediately
        # Max height say 12 units
        max_count = np.max(self.bins) if np.max(self.bins) > 0 else 1
        scale_factor = 3.0 / max_count if max_count > 0 else 1 # Normalize strictly visual
        
        # Use simple fixed scale? No, dynamic growth.
        # Let's fix scale so 500 balls = height 3
        vis_heights = self.bins * 0.015 
        
        ax.bar(centers, vis_heights, width=0.9, color=BAR_FILL, alpha=0.6, zorder=2, align='center')
        
        # 3. DRAW FALLING RAIN (The Chaos)
        if len(self.particles) > 0:
            ax.scatter(self.particles[:, 0], self.particles[:, 1], color=RAIN_CYAN, s=10, alpha=0.8, zorder=10)
            
        # 4. DRAW IDEAL CURVE (The Truth)
        # Fade in curve as data accumulates
        total_landed = np.sum(self.bins)
        if total_landed > 50:
            x_curve = np.linspace(-6, 6, 200)
            y_curve = self.pdf(x_curve, total_landed) * 0.015 # Match the bar scaling factor
            
            alpha = min(1.0, total_landed / 500.0)
            ax.plot(x_curve, y_curve, color=CURVE_MAGENTA, linewidth=3, alpha=alpha, zorder=20)
            
            # Equation
            if alpha > 0.8:
                ax.text(3, 10, r"$y = e^{-x^2}$", color=CURVE_MAGENTA, fontsize=14)

        # 5. HUD
        ax.text(0, 13.5, "LOGIC GARDEN 64: THE RAIN OF TRUTH", color="white", ha='center', fontsize=14, fontweight='bold', fontfamily='monospace')
        
        status = f"SAMPLES: {int(total_landed)}"
        ax.text(0, 12.8, status, color=RAIN_CYAN, ha='center', fontfamily='monospace', fontsize=10)

        ax.set_axis_off()
        ax.set_facecolor(BG_VOID)
        
        # Save
        out_dir = "logic_garden_galton_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"galton_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_VOID)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print(f"[NURSERY] Dropping Chaos...")
    
    sim = GaltonSim()
    
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
            print(f"Frame {i}/{TOTAL_FRAMES}")
