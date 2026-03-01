"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v50.py
MODE:   Nursery (Tactical Display Palette)
TARGET: AEGIS Weapon System (Phased Array Defense)
STYLE:  "The Iron Shield" | 40s Deep Time | 4K Ready

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon, Wedge
import os

# --- 1. THE TACTICAL PALETTE ---
BG_COLOR = "#000510"        # Deep Ocean
RADAR_GRID = "#003010"      # Passive Grid
RADAR_SWEEP = "#00FF00"     # Active Elements
THREAT_RED = "#FF0000"      # Inbound Vampire
FRIENDLY_CYAN = "#00FFFF"   # Outbound Bird
LOCK_YELLOW = "#FFD700"     # FC Lock
EXPLOSION = "#FFFFFF"       # Kinetic Kill

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 40               # 40s Deep Time
TOTAL_FRAMES = FPS * DURATION

class Entity:
    def __init__(self, x, y, vx, vy, type_tag):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.type = type_tag # 'hostile', 'friendly'
        self.active = True
        self.id = np.random.randint(1000, 9999)
        self.target_id = None
        self.launch_phase = 0 # For VLS launch mechanics

class AegisSim:
    def __init__(self):
        self.ship_x = 0
        self.ship_y = 0
        self.threats = []
        self.interceptors = []
        self.explosions = []
        
        # Radar State
        self.tracks = {} # ID: {state}
        self.beams = [] # Visual beam lines
        
    def update(self, frame_idx):
        # 1. SPAWN THREATS (The Swarm)
        # 3 distinct waves
        wave_times = [30, 200, 400]
        if frame_idx in wave_times:
            count = 4 if frame_idx == 30 else 8
            for _ in range(count):
                angle = np.random.uniform(0, 2*np.pi)
                dist = 9.5
                speed = 0.015 # Vampire speed (Mach 2 scaled)
                
                ex = np.cos(angle) * dist
                ey = np.sin(angle) * dist
                vx = -np.cos(angle) * speed
                vy = -np.sin(angle) * speed
                
                self.threats.append(Entity(ex, ey, vx, vy, 'hostile'))

        # 2. UPDATE ENTITIES
        for e in self.threats:
            if not e.active: continue
            e.x += e.vx
            e.y += e.vy
            
            # Hit Ship?
            if np.sqrt(e.x**2 + e.y**2) < 0.2:
                e.active = False
                # Game Over logic (visualize ship damage)

        for i in self.interceptors:
            if not i.active: continue
            
            # VLS LAUNCH PHYSICS
            # Phase 0: Vertical Eject (0.5s)
            if i.launch_phase < 15:
                i.launch_phase += 1
                # Move "Up" visually relative to ship? 
                # On 2D map, it stays center but grows opacity, simulating vertical rise
                pass 
                
            # Phase 1: Turnover & Guidance
            else:
                target = self.get_threat_by_id(i.target_id)
                if target and target.active:
                    # Proportional Navigation (Intercept Course)
                    dx = target.x - i.x
                    dy = target.y - i.y
                    dist = np.sqrt(dx**2 + dy**2)
                    
                    # Normalize
                    dx /= dist
                    dy /= dist
                    
                    speed = 0.04 # SM-2 is fast (Mach 3.5+)
                    i.vx = dx * speed
                    i.vy = dy * speed
                    
                    i.x += i.vx
                    i.y += i.vy
                    
                    # Proximity Fuse
                    if dist < 0.2:
                        target.active = False
                        i.active = False
                        self.explosions.append({'x': target.x, 'y': target.y, 'life': 30})
                else:
                    # Target lost, self destruct
                    i.active = False

        # 3. AEGIS LOOP (The Brain)
        self.beams = []
        
        # Detection
        for t in self.threats:
            if not t.active: continue
            dist = np.sqrt(t.x**2 + t.y**2)
            
            # Track Init (Range 8.0)
            if dist < 8.0:
                if t.id not in self.tracks:
                    self.tracks[t.id] = {'status': 'detect', 'assigned': False}
                
                # Visual Tracking Beam (Phased Array Flash)
                # Random beam flicker to simulate electronic scan
                if frame_idx % 5 == 0:
                    self.beams.append({'x': t.x, 'y': t.y, 'type': 'track'})

            # Engagement (Range 6.0)
            if dist < 6.0 and self.tracks[t.id]['status'] == 'detect':
                if not self.tracks[t.id]['assigned']:
                    # FIRE VLS
                    interceptor = Entity(0, 0, 0, 0, 'friendly')
                    interceptor.target_id = t.id
                    self.interceptors.append(interceptor)
                    self.tracks[t.id]['assigned'] = True
                    self.tracks[t.id]['status'] = 'engage'

            # Terminal Illumination (Range 2.0)
            if dist < 2.0 and self.tracks[t.id]['status'] == 'engage':
                # Continuous Wave Illumination (Solid Beam)
                self.beams.append({'x': t.x, 'y': t.y, 'type': 'lock'})

        # Explosions
        for exp in self.explosions:
            exp['life'] -= 1
        self.explosions = [e for e in self.explosions if e['life'] > 0]

    def get_threat_by_id(self, tid):
        for t in self.threats:
            if t.id == tid: return t
        return None

    def render(self, frame_idx, ax):
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        
        # 1. SCOPE GRID
        for r in [2, 4, 6, 8]:
            ax.add_patch(Circle((0,0), r, color=RADAR_GRID, fill=False, linewidth=0.8))
        ax.plot([-10, 10], [0, 0], color=RADAR_GRID, linewidth=0.5)
        ax.plot([0, 0], [-10, 10], color=RADAR_GRID, linewidth=0.5)
        
        # 2. BEAMS (The Phased Array)
        for b in self.beams:
            col = RADAR_SWEEP if b['type'] == 'track' else LOCK_YELLOW
            width = 1.0 if b['type'] == 'track' else 2.0
            alpha = 0.3 if b['type'] == 'track' else 0.6
            ax.plot([0, b['x']], [0, b['y']], color=col, linewidth=width, alpha=alpha)

        # 3. THREATS (Vampires)
        for t in self.threats:
            if not t.active: continue
            # Diamond symbol
            ts = 0.15
            poly = [
                [t.x, t.y+ts], [t.x+ts, t.y], [t.x, t.y-ts], [t.x-ts, t.y]
            ]
            ax.add_patch(Polygon(poly, color=THREAT_RED))
            # Velocity vector
            ax.plot([t.x, t.x + t.vx*20], [t.y, t.y + t.vy*20], color=THREAT_RED, linewidth=1)
            # Designation
            if t.id in self.tracks:
                ax.text(t.x+0.2, t.y+0.2, f"TN-{t.id}", color=THREAT_RED, fontsize=6)

        # 4. INTERCEPTORS (Birds)
        for i in self.interceptors:
            if not i.active: continue
            if i.launch_phase < 15:
                # Launch bloom (VLS Cell)
                ax.add_patch(Circle((0,0), 0.3, color="white", alpha=0.8))
            else:
                # Missile
                ax.add_patch(Circle((i.x, i.y), 0.1, color=FRIENDLY_CYAN))
                # Trail
                ax.plot([i.x - i.vx*10, i.x], [i.y - i.vy*10, i.y], color=FRIENDLY_CYAN, alpha=0.5)

        # 5. EXPLOSIONS
        for exp in self.explosions:
            radius = (30 - exp['life']) * 0.05
            ax.add_patch(Circle((exp['x'], exp['y']), radius, color=EXPLOSION, alpha=0.8))
            ax.text(exp['x'], exp['y'], "KILL", color=EXPLOSION, fontsize=5, ha='center')

        # 6. SHIP (Center)
        ax.add_patch(Circle((0,0), 0.1, color="white"))
        
        # 7. HUD
        active_tracks = len(self.interceptors)
        status = "MODE: SEARCH"
        col = RADAR_SWEEP
        
        if self.beams:
            status = "MODE: TRACKING"
            col = LOCK_YELLOW
        if active_tracks > 0:
            status = "INTERCEPT IN PROGRESS"
            col = FRIENDLY_CYAN
            
        ax.text(0, -9.5, status, color=col, ha='center', fontfamily='monospace', fontsize=12,
               bbox=dict(facecolor='black', edgecolor=col))
               
        ax.text(-9, 9, "AN/SPY-1 RADAR", color=RADAR_SWEEP, fontsize=8)
        ax.text(-9, 8.5, "AUTO-SPECIAL", color=RADAR_SWEEP, fontsize=6)

        ax.set_aspect('equal')
        ax.set_axis_off()
        
        out_dir = "logic_garden_aegis_frames"
        os.makedirs(out_dir, exist_ok=True)
        filename = os.path.join(out_dir, f"aegis_{frame_idx:04d}.png")
        plt.savefig(filename, facecolor=BG_COLOR)
        plt.close()

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print(f"[NURSERY] Initializing AEGIS Combat System...")
    
    sim = AegisSim()
    
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
