"""
SOVEREIGN CODE: logic_garden_104_scarcity.py
FORMAT: YouTube Shorts (1080x1920)
SCENE: Scarcity (Infinite Desire vs Finite Supply)
SYSTEM: Pure Python
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
import matplotlib.patheffects as pe
import os
import random
import math

# CONFIG
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_104_scarcity"
os.makedirs(OUT_DIR, exist_ok=True)

# RESOLUTION
RES_W = 1080
RES_H = 1920

# PALETTE
C_BG       = '#050510'     # Void
C_CORE     = '#FFFFFF'     # The Source
C_RESOURCE = '#00FFFF'     # Finite Atoms (Cyan)
C_NEED     = '#FF3300'     # Desires (Red)
C_SATISFIED= '#FFD700'     # Met Need (Gold)
C_STARVED  = '#333344'     # Unmet Need (Ash)

class Resource:
    def __init__(self):
        self.active = True
        self.pos = np.array([0.0, 0.0]) # Start at core
        angle = random.uniform(0, 6.28)
        speed = random.uniform(2, 4)
        self.vel = np.array([math.cos(angle), math.sin(angle)]) * speed
        self.radius = 15

    def update(self):
        self.pos += self.vel

class Agent:
    def __init__(self, uid):
        self.id = uid
        self.active = True
        self.state = "HUNGRY" # HUNGRY, FED, STARVED
        
        # Spawn at random edge
        side = random.choice(['TOP', 'BOTTOM', 'LEFT', 'RIGHT'])
        if side == 'TOP':
            self.pos = np.array([random.uniform(-600, 600), 1000.0])
        elif side == 'BOTTOM':
            self.pos = np.array([random.uniform(-600, 600), -1000.0])
        elif side == 'LEFT':
            self.pos = np.array([-600.0, random.uniform(-1000, 1000)])
        else:
            self.pos = np.array([600.0, random.uniform(-1000, 1000)])
            
        # Velocity aimed at Core (0,0)
        vec_to_center = np.array([0.0, 0.0]) - self.pos
        dist = np.linalg.norm(vec_to_center)
        self.dir = vec_to_center / dist
        self.vel = self.dir * random.uniform(8, 12) # Fast and aggressive
        self.angle = math.atan2(self.dir[1], self.dir[0])

    def update(self, resources):
        if not self.active: return
        
        self.pos += self.vel
        
        if self.state == "HUNGRY":
            # 1. Check Collision with Resources
            for r in resources:
                if r.active:
                    d = np.linalg.norm(self.pos - r.pos)
                    if d < 40: # Grab radius
                        # SUCCESS
                        self.state = "FED"
                        r.active = False # Consumption
                        # Change direction to leave
                        self.vel = -self.vel * 0.5 
                        return "FLASH"

            # 2. Check Collision with Core (Starvation Line)
            d_core = np.linalg.norm(self.pos)
            if d_core < 50:
                # FAILURE
                self.state = "STARVED"
                # Drift aimlessly
                self.vel = np.array([random.uniform(-1, 1), random.uniform(-1, 1)]) * 2
                return "FAIL"
                
        elif self.state == "FED" or self.state == "STARVED":
            # Just drift away
            pass

def run():
    print(f"LOGIC GARDEN 104: SCARCITY ({TOTAL_FRAMES} frames)")
    
    resources = []
    agents = []
    flashes = [] # Visual FX
    
    # METRICS
    total_desire = 0
    total_fed = 0
    
    for f in range(TOTAL_FRAMES):
        
        # --- 1. SPAWN LOGIC ---
        
        # RESOURCE SPAWN (Fixed supply)
        # Every 5 frames, emit 1 resource
        if f % 5 == 0:
            resources.append(Resource())
            
        # DESIRE SPAWN (Exponential Demand)
        # Ramp up intensity
        spawn_rate = 1 + int((f / TOTAL_FRAMES) * 8) # 1 -> 9 agents per frame
        
        for _ in range(spawn_rate):
            agents.append(Agent(len(agents)))
            total_desire += 1

        # --- 2. UPDATE PHYSICS ---
        
        # Resources
        active_res = []
        for r in resources:
            r.update()
            # Despawn if too far to save memory
            if np.linalg.norm(r.pos) < 1500:
                active_res.append(r)
        resources = active_res
        
        # Agents
        active_agents = []
        for a in agents:
            res = a.update(resources)
            
            if res == "FLASH":
                flashes.append({'p': a.pos.copy(), 'r': 10, 'max': 100, 'c': C_SATISFIED})
                total_fed += 1
            if res == "FAIL":
                flashes.append({'p': a.pos.copy(), 'r': 10, 'max': 50, 'c': C_STARVED})
            
            # Keep them until they drift off screen
            if np.linalg.norm(a.pos) < 1200:
                active_agents.append(a)
        agents = active_agents
        
        # FX
        active_flashes = []
        for fl in flashes:
            fl['r'] += 10
            if fl['r'] < fl['max']:
                active_flashes.append(fl)
        flashes = active_flashes

        # --- 3. RENDER ---
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        ax.set_xlim(-540, 540)
        ax.set_ylim(-960, 960)
        ax.set_facecolor(C_BG)
        
        # Background Grid (The Matrix)
        for i in range(-500, 600, 200):
            ax.axvline(i, color='#111122', linewidth=2)
            ax.axhline(i, color='#111122', linewidth=2)

        # DRAW FLASHES (Bottom)
        for fl in flashes:
            # Ring
            alpha = 1.0 - (fl['r'] / fl['max'])
            circ = Circle((fl['p'][0], fl['p'][1]), fl['r'], color=fl['c'], fill=False, linewidth=3, alpha=alpha)
            ax.add_patch(circ)

        # DRAW STARVED AGENTS (Ash Layer - Accumulating clutter)
        for a in agents:
            if a.state == "STARVED":
                ax.scatter(a.pos[0], a.pos[1], c=C_STARVED, s=30, marker='x', alpha=0.6)

        # DRAW RESOURCES (Precious Atoms)
        for r in resources:
            # Glow
            circ = Circle((r.pos[0], r.pos[1]), r.radius*2, color=C_RESOURCE, alpha=0.3)
            ax.add_patch(circ)
            ax.scatter(r.pos[0], r.pos[1], c=C_RESOURCE, s=50, zorder=5)

        # DRAW HUNGRY AGENTS (The Swarm)
        for a in agents:
            if a.state == "HUNGRY":
                # Draw oriented triangle
                # Matplotlib marker rotation is tricky, easier to construct polygon or just user marker with rotation arg?
                # Marker rotation in scatter uses degrees.
                deg = math.degrees(a.angle) - 90 
                # Note: large scatter calls are faster than patches
                # We will batch render just to be industrial
                pass
        
        # Batch rendering for speed and visual consistency
        hungry_x = [a.pos[0] for a in agents if a.state == "HUNGRY"]
        hungry_y = [a.pos[1] for a in agents if a.state == "HUNGRY"]
        
        if hungry_x:
            # Needles
            ax.scatter(hungry_x, hungry_y, c=C_NEED, marker='v', s=60, zorder=10) # Simplified orientation for batch
            
        fed_x = [a.pos[0] for a in agents if a.state == "FED"]
        fed_y = [a.pos[1] for a in agents if a.state == "FED"]
        if fed_x:
            ax.scatter(fed_x, fed_y, c=C_SATISFIED, marker='o', s=80, zorder=15, edgecolors='white')

        # CENTRAL CORE (The Bottleneck)
        # Pulsating
        core_sz = 60 + math.sin(f*0.2)*10
        center_c = Circle((0,0), core_sz, color=C_CORE, zorder=20)
        ax.add_patch(center_c)
        center_glow = Circle((0,0), core_sz*2, color=C_RESOURCE, alpha=0.2, zorder=19)
        ax.add_patch(center_glow)

        # UI OVERLAY
        stroke = [pe.withStroke(linewidth=4, foreground="black")]
        
        # Counters
        ax.text(0.05, 0.95, f"DESIRES: {total_desire}", transform=ax.transAxes, 
                color=C_NEED, fontsize=25, fontname='monospace', weight='bold', path_effects=stroke)
        ax.text(0.05, 0.92, f"SUPPLY : {total_fed}", transform=ax.transAxes, 
                color=C_RESOURCE, fontsize=25, fontname='monospace', weight='bold', path_effects=stroke)
                
        # Main Title Scaling
        if f > 100:
            scale_fac = min(1.0, (f-100)/20.0)
            ax.text(0.5, 0.2, "FINITE ATOMS", transform=ax.transAxes, 
                    color=C_RESOURCE, ha='center', fontsize=30*scale_fac, fontname='monospace', weight='bold', path_effects=stroke)
            
        if f > 150:
            ax.text(0.5, 0.5, "SCARCITY", transform=ax.transAxes, 
                    color='white', ha='center', fontsize=60, fontname='monospace', weight='bold', path_effects=stroke)
            
        if f > 180:
             ax.text(0.5, 0.8, "INFINITE DESIRE", transform=ax.transAxes, 
                    color=C_NEED, ha='center', fontsize=30, fontname='monospace', weight='bold', path_effects=stroke)

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
