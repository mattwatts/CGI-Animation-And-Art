"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v55_fixed.py
MODE:   Nursery (Horology Palette)
TARGET: The Anchor Escapement (HUD Fix)
STYLE:  "The Iron Pulse" | 40s Deep Time | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Wedge, Rectangle
import os

# --- 1. THE HOROLOGY PALETTE ---
BG_DARK = "#0A0500"         # Workshop
GEAR_BRASS = "#B5A642"      # Escape Wheel
ANCHOR_STEEL = "#708090"    # Pallets
PENDULUM_IRON = "#C0C0C0"   # Rod
IMPULSE_RED = "#FF4500"     # Energy Transfer

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 40
TOTAL_FRAMES = FPS * DURATION

class ClockSim:
    def __init__(self):
        # Physics State
        self.time = 0.0
        self.dt = 0.05
        
        # Pendulum
        self.theta = 0.0
        self.omega = 0.0
        self.length = 8.0
        self.gravity = 9.8
        self.max_theta = 0.4 # Radians swing
        
        # Gear State
        self.gear_angle = 0.0
        self.num_teeth = 12
        self.tooth_step = (2 * np.pi) / self.num_teeth
        
        # Impulse State
        self.impulse_active = False
        self.impulse_dir = 0
        self.ticks = 0
        self.last_sign = 0
        
    def update(self, frame_idx):
        # 1. SIMPLE HARMONIC MOTION (Idealized)
        natural_freq = np.sqrt(self.gravity / self.length)
        visual_freq = natural_freq * 0.5 # Slow for nursery
        
        phase = frame_idx * self.dt * visual_freq
        self.theta = self.max_theta * np.sin(phase)
        
        # 2. ESCAPEMENT LOGIC (The Quantizer)
        # Detect zero crossing (Vertical)
        current_sign = 1 if self.theta >= 0 else -1
        
        # Init last_sign
        if frame_idx == 0: self.last_sign = current_sign

        # Tick Detection
        if current_sign != self.last_sign:
            self.ticks += 1
            self.impulse_active = True
            self.last_sign = current_sign
        else:
            # Short flash
            if abs(self.theta) > 0.1:
                self.impulse_active = False

        # Gear Animation logic (Visual stepping)
        # 1 Tick = Half a tooth step (Tick-Tock = 1 Full Tooth)
        # Total Ticks determines angle
        
        # Smooth the step transition
        # We want the gear to lurch forward ONLY when impulse_active is true
        
        target_angle = -(self.ticks * (self.tooth_step * 0.5))
        
        # Linear Interpolation (Lerp) towards target for "weight drop" feel
        self.gear_angle = self.gear_angle * 0.9 + target_angle * 0.1

    def render(self, frame_idx, ax):
        ax.set_xlim(-6, 6)
        ax.set_ylim(-10, 4)
        
        # 1. ESCAPE WHEEL (Gear)
        gear_r = 3.0
        # Main Disk
        ax.add_patch(Circle((0,0), gear_r*0.8, color=GEAR_BRASS, zorder=1))
        
        # Teeth
        for i in range(self.num_teeth):
            # Rotate whole gear
            base_angle = self.gear_angle + (i * self.tooth_step) + 1.57 # Rotate 90 deg start
            
            # Tooth shape (Sawtooth)
            tip_x = (gear_r + 0.5) * np.cos(base_angle)
            tip_y = (gear_r + 0.5) * np.sin(base_angle)
            
            br_x = gear_r * np.cos(base_angle + 0.15)
            br_y = gear_r * np.sin(base_angle + 0.15)
            
            bl_x = gear_r * np.cos(base_angle - 0.15)
            bl_y = gear_r * np.sin(base_angle - 0.15)
            
            poly = [[0,0], [br_x, br_y], [tip_x, tip_y], [bl_x, bl_y]]
            ax.add_patch(Polygon(poly, color=GEAR_BRASS, zorder=1))

        # 2. THE ANCHOR (Pallet Fork)
        # Pivot is fixed slightly above gear
        # Visualizing the rocking arm
        
        # Create a T-shape that rotates with theta
        # Pivot point
        px, py = 0, 3.5
        
        # Rotation Matrix
        c, s = np.cos(self.theta), np.sin(self.theta)
        R = np.array(((c, -s), (s, c)))
        
        # Define Anchor Shape (Centred at 0,0)
        anchor_pts = np.array([
            [-3.0, -1.0], [-3.0, -0.2], [-0.5, 0.5], # Left Arm
            [0.5, 0.5], [3.0, -0.2], [3.0, -1.0],    # Right Arm
            [0.5, -0.5], [-0.5, -0.5]                # Center Hub
        ])
        
        # Rotate and Translate
        rotated_pts = np.dot(anchor_pts, R.T)
        rotated_pts[:, 0] += px
        rotated_pts[:, 1] += py
        
        ax.add_patch(Polygon(rotated_pts, color=ANCHOR_STEEL, zorder=5))
        
        # 3. THE PENDULUM
        # Pivot at (0, 3.5)
        pend_len = 11.0
        bx = px + pend_len * np.sin(self.theta)
        by = py - pend_len * np.cos(self.theta)
        
        # Rod
        ax.plot([px, bx], [py, by], color=PENDULUM_IRON, linewidth=4, zorder=4)
        # Bob
        ax.add_patch(Circle((bx, by), 0.9, color=PENDULUM_IRON, zorder=6))
        ax.add_patch(Circle((bx, by), 0.7, color=ANCHOR_STEEL, zorder=7))

        # 4. IMPULSE VISUAL
        if self.impulse_active:
            # Flash the "Pallet" tip
            if self.theta > 0: # Right swing, Left pallet engages?
                fx, fy = rotated_pts[0] # Left tip approx
            else:
                fx, fy = rotated_pts[5] # Right tip approx
                
            ax.add_patch(Circle((fx, fy), 0.3, color=IMPULSE_RED, zorder=10))
            ax.text(fx, fy+0.5, "KICK!", color=IMPULSE_RED, fontsize=8, fontweight='bold', ha='center')

        # HUD
        p_lbl = "PHASE: SWING"
        col = PENDULUM_IRON
        if self.impulse_active:
            p_lbl = "PHASE: TICK (IMPULSE)"
            col = IMPULSE_RED
            
        # Center Label
        ax.text(0, -9, p_lbl, color=col, ha='center', fontfamily='monospace', fontsize=14, fontweight='bold',
                bbox=dict(facecolor='black', edgecolor=col))
                
        # FIXED: Counter Alignment
        # x=5.5 is safe right edge, ha='right' forces text to grow Leftward
        ax.text(5.5, -9, f"TICKS: {self.ticks}", color=GEAR_BRASS, 
                fontfamily='monospace', fontsize=12, ha='right', fontweight='bold',
                bbox=dict(facecolor='black', edgecolor=GEAR_BRASS, alpha=0.5))

        ax.set_aspect('equal')
        ax.set_axis_off()
        
        out_dir = "logic_garden_clock_fixed_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"clock_fixed_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_DARK)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print(f"[NURSERY] Simulating Precision Timekeeping...")
    
    sim = ClockSim()
    
    for i in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(8, 10), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_DARK)
        
        sim.update(i)
        sim.render(i, ax)
        plt.close()
        
        if i % 60 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
