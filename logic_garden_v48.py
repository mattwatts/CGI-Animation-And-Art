"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v48_final.py
MODE:   Nursery (Radar Palette)
TARGET: VT Proximity Fuse (Corrected Timing)
STYLE:  "The Smart Shell" | 40s Deep Time | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle
import os

# --- 1. THE RADAR PALETTE ---
BG_COLOR = "#080808"        # Deep Night
SHELL_BODY = "#C0C0C0"      # Polished Steel
SIGNAL_TX = "#00FFFF"       # Cyan (Outgoing)
SIGNAL_RX = "#39FF14"       # Green (Returning)
TARGET_RED = "#FF0000"      # Bandit
EXPLOSION = "#FF8C00"       # High Explosive
SHRAPNEL = "#FFFF00"        # Tungsten

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 40               # 40 Seconds
TOTAL_FRAMES = FPS * DURATION

class Wave:
    def __init__(self, x, y, type_tag):
        self.x = x
        self.y = y
        self.r = 0.0
        self.type = type_tag
        self.active = True
        self.opacity = 1.0

class ProximitySim:
    def __init__(self):
        self.shell_x = -9.0
        self.shell_y = -9.0
        self.target_x = 2.0
        self.target_y = 2.0
        
        # Calculate Vector
        target_pos = np.array([self.target_x, self.target_y])
        current_pos = np.array([self.shell_x, self.shell_y])
        direction = target_pos - current_pos
        dist = np.linalg.norm(direction)
        direction /= dist
        
        # SPEED CORRECTION: 
        # Needs to cover ~17 units in 900 frames. 17/900 = 0.018. 
        # Set to 0.022 to hit target around frame 800.
        self.speed = 0.022
        self.shell_vx = direction[0] * self.speed
        self.shell_vy = direction[1] * self.speed
        
        self.waves = []
        self.shrapnel = []
        self.signal_strength = 0.0
        self.threshold = 0.8
        
        self.detonated = False
        self.detonation_frame = -1
        self.sim_timer = 0
        
    def update(self, frame_idx):
        self.sim_timer = frame_idx
        
        # --- PAUSE PHASE (AFTERMATH) ---
        if self.detonated and (frame_idx - self.detonation_frame > 60):
            # Slow drift for cinematic effect
            for s in self.shrapnel:
                s['x'] += s['vx'] * 0.05
                s['y'] += s['vy'] * 0.05
            return # Freeze main logic

        if not self.detonated:
            self.shell_x += self.shell_vx
            self.shell_y += self.shell_vy
            
            # Emit TX (Slow Pulse)
            if frame_idx % 25 == 0:
                self.waves.append(Wave(self.shell_x, self.shell_y, 'tx'))
        
        # Wave Physics (c > v_shell)
        c = 0.15 
        
        for w in self.waves:
            if not w.active: continue
            w.r += c
            
            # Fade Distance
            if w.r > 25: w.active = False

            # REFLECTION from TARGET
            if w.type == 'tx':
                d_tgt = np.sqrt((w.x - self.target_x)**2 + (w.y - self.target_y)**2)
                if abs(d_tgt - w.r) < c:
                    if frame_idx % 5 == 0: # Limit echo noise
                        self.waves.append(Wave(self.target_x, self.target_y, 'rx'))
                    w.opacity = 0.3 # Energy absorbed

            # DETECTION at SHELL
            if w.type == 'rx' and not self.detonated:
                d_shell = np.sqrt((w.x - self.shell_x)**2 + (w.y - self.shell_y)**2)
                if abs(d_shell - w.r) < c:
                    # Signal Gain based on proximity
                    range_t = np.sqrt((self.shell_x - self.target_x)**2 + (self.shell_y - self.target_y)**2)
                    gain = 0.1 + (5.0 / (range_t**2 + 0.1)) * 0.05
                    self.signal_strength += gain
                    w.active = False
                    
        # Signal Decay
        self.signal_strength *= 0.98
        
        # Trigger
        if self.signal_strength > self.threshold and not self.detonated:
            self.detonated = True
            self.detonation_frame = frame_idx
            self.spawn_shrapnel()
            
        # Shrapnel Move
        if self.detonated:
            for s in self.shrapnel:
                s['x'] += s['vx']
                s['y'] += s['vy']
                s['vx'] *= 0.95
                s['vy'] *= 0.95
                
        self.waves = [w for w in self.waves if w.active]

    def spawn_shrapnel(self):
        angle_base = np.arctan2(self.shell_vy, self.shell_vx)
        for _ in range(80):
            # Spread 45 deg
            a = angle_base + np.random.uniform(-0.6, 0.6)
            s = np.random.uniform(0.3, 0.9)
            self.shrapnel.append({
                'x': self.shell_x,
                'y': self.shell_y,
                'vx': self.shell_vx + np.cos(a)*s,
                'vy': self.shell_vy + np.sin(a)*s
            })

    def render(self, frame_idx, ax):
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        
        # Background Elements
        for i in range(1, 6):
            ax.add_patch(Circle((0,0), i*4, color="#102010", fill=False))
            
        # Waves
        for w in self.waves:
            col = SIGNAL_TX if w.type == 'tx' else SIGNAL_RX
            alp = w.opacity
            if w.type == 'rx': alp = 0.9
            alp *= max(0, 1.0 - w.r/30)
            ax.add_patch(Circle((w.x, w.y), w.r, color=col, fill=False, linewidth=1.5, alpha=alp))
            
        # Target
        tx, ty = self.target_x, self.target_y
        ax.plot([tx-1, tx+1], [ty, ty], color=TARGET_RED, linewidth=4)
        ax.plot([tx, tx], [ty-1, ty+1], color=TARGET_RED, linewidth=4)
        
        # Shell
        if not self.detonated:
            sx, sy = self.shell_x, self.shell_y
            ax.add_patch(Circle((sx, sy), 0.3, color=SHELL_BODY))
            # Pulse
            if frame_idx % 25 < 10:
                ax.add_patch(Circle((sx, sy), 0.6, color=SIGNAL_TX, alpha=0.4))
        else:
            # Explosion
            dt = frame_idx - self.detonation_frame
            r = min(3.0, dt * 0.2)
            alpha = max(0.0, 1.0 - dt/80.0)
            ax.add_patch(Circle((self.shell_x, self.shell_y), r, color=EXPLOSION, alpha=alpha))
            
            # Shrapnel
            sx = [s['x'] for s in self.shrapnel]
            sy = [s['y'] for s in self.shrapnel]
            ax.scatter(sx, sy, c=SHRAPNEL, s=10, zorder=10)

        # OSCILLOSCOPE
        ax.add_patch(Rectangle((-9.5, -9.5), 1.5, 5, color="black", alpha=0.8, edgecolor="white"))
        h = min(4.8, self.signal_strength * 2.0)
        col = SIGNAL_RX if self.signal_strength <= self.threshold else EXPLOSION
        ax.add_patch(Rectangle((-9.25, -9.25), 1, h, color=col))
        
        # Threshold Line
        th_y = -9.25 + (self.threshold * 2.0)
        ax.plot([-9.5, -8.0], [th_y, th_y], color="red", linestyle="--")
        
        # PHASES
        if frame_idx < 200:
            p = "PHASE 1: TRANSMISSION"
            c = SIGNAL_TX
        elif frame_idx < 600:
            p = "PHASE 2: RETURN SIGNAL"
            c = SIGNAL_RX
        elif not self.detonated:
            p = "PHASE 3: SIGNAL GROWTH"
            c = "white"
        elif frame_idx - self.detonation_frame < 60:
            p = "PHASE 4: DETONATION"
            c = EXPLOSION
        else:
            p = "PHASE 5: TARGET DESTROYED"
            c = SHRAPNEL
            
        ax.text(0, 9, p, color=c, ha='center', fontfamily='monospace', fontsize=14,
                bbox=dict(facecolor='black', edgecolor=c))
                
        ax.set_aspect('equal')
        ax.set_axis_off()
        
        out_dir = "logic_garden_vt_final_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"vt_final_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print(f"[NURSERY] Simulating {TOTAL_FRAMES} frames (Corrected Timeline)...")
    
    sim = ProximitySim()
    
    for i in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10, 10), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.set_facecolor(BG_COLOR)
        
        sim.update(i)
        sim.render(i, ax)
        plt.close()
        
        if i % 60 == 0:
            print(f"Frame {i}/{TOTAL_FRAMES}")
