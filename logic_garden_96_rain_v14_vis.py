"""
SOVEREIGN CODE: logic_garden_101_rain_v14_vis.py
FORMAT: True HD 1080x1920
SCENE: Full Cycle (High Visibility UI + Impact Tracking)
SYSTEM: Pure Python
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import matplotlib.patheffects as pe
import os

# CONFIG
FPS = 30
DURATION = 32
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_101_rain_v14"
os.makedirs(OUT_DIR, exist_ok=True)

# PHYSICS
WORLD_H = 120000     
K_LINE = 40000       
G = 60.0             
THRUST = 180.0       

# RENDER
RES_W = 1080
RES_H = 1920
ASPECT = RES_H / RES_W 

# PALETTE
C_VOID   = '#050510'     
C_BUS    = '#DDDDDD'     # Light Grey for visibility
C_CYAN   = '#00FFFF'     
C_FIRE   = '#FF5500'     
C_CORE   = '#FFFFFF'     

class Entity:
    def __init__(self, x, y, vx, vy, kind="WARHEAD"):
        self.pos = np.array([float(x), float(y)])
        self.vel = np.array([float(vx), float(vy)])
        self.kind = kind
        self.active = True
        self.history = []
        self.temp = 0.0 

    def update(self, dt, thrust_on=False):
        if not self.active: return "DEAD"

        acc = np.array([0.0, -G]) 
        if thrust_on: acc[1] += THRUST 
            
        # Atmosphere
        if self.pos[1] < K_LINE:
            density = max(0.0, min(1.0, (K_LINE - self.pos[1]) / K_LINE))
            speed = np.linalg.norm(self.vel)
            if speed > 0:
                drag_k = 0.00001 if self.kind == "WARHEAD" else 0.00005
                acc += (-self.vel / speed * (drag_k * density * speed * speed))
            
            if self.kind == "WARHEAD":
                target_t = min(1.2, (speed * density) / 1200.0) 
                self.temp += (target_t - self.temp) * 0.1
        else:
            self.temp *= 0.95

        self.vel += acc * dt
        self.pos += self.vel * dt
        
        self.history.append(self.pos.copy())
        if len(self.history) > 30: self.history.pop(0)

        if self.pos[1] <= 0:
             self.pos[1] = 0
             self.active = False
             return "IMPACT"
        return "ALIVE"

def run():
    print(f"LOGIC GARDEN 101: HIGH VISIBILITY ({TOTAL_FRAMES} frames)")
    
    # 1. SETUP
    bus = Entity(0, 100, 0, 0, "BUS") 
    warheads = []
    explosions = []
    # Persistent lists for camera tracking
    all_impacts_x = [] 
    
    # Logic
    cam_y = 0
    cam_w = 8000
    
    MECO = 240         
    DEPLOY_START = 260 
    DEPLOY_END = 480   
    
    PHASE = "ASCENT"
    
    # Text Effect (Black Outline)
    stroke = [pe.withStroke(linewidth=3, foreground="black")]
    
    for f in range(TOTAL_FRAMES):
        
        # --- STATE MACHINE ---
        if f < MECO: PHASE = "ASCENT"
        elif f < DEPLOY_END: PHASE = "DEPLOY"
        else: PHASE = "DESCENT"
            
        # --- PHYSICS ---
        bus.update(0.1, thrust_on=(PHASE=="ASCENT"))
        
        # Deploy
        if PHASE == "DEPLOY" and f > DEPLOY_START and f % 22 == 0:
            count = len(warheads)
            side = -1 if count % 2 == 0 else 1
            spread = 600 + (count * 120)
            vx = spread * side
            vy = bus.vel[1] 
            warheads.append(Entity(bus.pos[0], bus.pos[1], vx, vy, "WARHEAD"))

        # Updates
        active_warheads = []
        new_impacts = []
        
        for w in warheads:
            res = w.update(0.1)
            if res == "IMPACT": 
                new_impacts.append(w.pos.copy())
                all_impacts_x.append(w.pos[0]) # REMEMBER THIS LOCATION
            if w.pos[1] > 0: active_warheads.append(w)

        active_ex = []
        for ex in explosions:
            ex['r'] += 100 
            ex['a'] -= 0.02
            if ex['a'] > 0: active_ex.append(ex)
        explosions = active_ex
        for p in new_impacts:
            explosions.append({'p': p, 'r': 60, 'a': 1.0})

        # --- CAMERA LOGIC (BOUNDING BOX SUPREMACY) ---
        
        # 1. Collect ALL Points of Interest
        xs = [0] # Center always relevant
        ys = []
        
        # Include Bus if alive
        if bus.active:
            xs.append(bus.pos[0])
            ys.append(bus.pos[1])
            
        # Include Active Warheads
        for w in active_warheads:
            xs.append(w.pos[0])
            ys.append(w.pos[1])
            
        # CRITICAL: Include Dead Warheads (Impact Sites)
        # This prevents the camera from "forgetting" the width
        for ix in all_impacts_x:
            xs.append(ix)
            ys.append(0) # Ground
            
        # 2. Calculate Bounds
        if not ys: ys = [0]
        
        min_y = min(ys)
        max_y = max(ys)
        max_abs_x = max([abs(x) for x in xs]) if xs else 5000
        
        # 3. Determine Target Box
        target_w = max_abs_x * 2.5 # Padding width
        target_w = max(12000, target_w) # Minimum width constant
        
        # Target Y Center
        if PHASE == "ASCENT":
            target_y = bus.pos[1] + 2000 # Look slightly ahead
        elif PHASE == "DEPLOY":
            target_y = bus.pos[1]
        else:
            # During descent, frame the vertical spread
            target_y = (min_y + max_y) / 2
            
            # If everything is low, pull camera up slightly to see ground
            if target_y < 10000: target_y = 10000

        # 4. Smooth Damping
        cam_w += (target_w - cam_w) * 0.1 # Faster response
        cam_h = cam_w * ASPECT
        
        # Vertical control
        # Force Bus roughly center/low-center
        offset = 0
        if PHASE == "ASCENT": offset = -cam_h * 0.1
        if PHASE == "DESCENT": offset = -cam_h * 0.1
        
        desired_y = target_y - offset
        cam_y += (desired_y - cam_y) * 0.1
        
        # Floor Clamp
        if cam_y - cam_h/2 < -2000:
             cam_y = (cam_h/2) - 2000

        # --- RENDER ---
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        xlim = [-cam_w/2, cam_w/2]
        ylim = [cam_y - cam_h/2, cam_y + cam_h/2]
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_facecolor(C_VOID)
        
        # 1. STARS
        if ylim[0] > 1000:
            np.random.seed(42)
            sx = np.random.randint(-100000, 100000, 800)
            sy = np.random.randint(0, 200000, 800)
            visible = (sx > xlim[0]) & (sx < xlim[1]) & (sy > ylim[0]) & (sy < ylim[1])
            ax.scatter(sx[visible], sy[visible], c='white', s=2, alpha=0.3)

        # 2. ATMOSPHERE
        if ylim[0] < K_LINE and ylim[1] > K_LINE:
            ax.axhline(K_LINE, color=C_FIRE, linestyle='--', alpha=0.3)
            ax.text(xlim[0]+(cam_w*0.05), K_LINE+500, "KARMAN LINE", 
                    color=C_FIRE, fontsize=12, fontname='monospace', path_effects=stroke)

        # 3. DRAW BUS 
        if bus.active:
            scale = cam_w / 6000.0 
            
            if PHASE == "ASCENT":
                # Flame behind
                ax.plot([bus.pos[0], bus.pos[0]], [bus.pos[1], bus.pos[1]-1500], color=C_FIRE, linewidth=8)
            
            # The Hull (Always drawn on top of flame)
            # Use Rectangle patch for solidity
            sz = 400
            rect = Rectangle((bus.pos[0]-sz/2, bus.pos[1]-sz/2), sz, sz, color=C_BUS, zorder=10)
            ax.add_patch(rect)

        # 4. WARHEADS
        for w in active_warheads:
            c = C_CYAN
            if w.temp > 0.4: c = C_CORE
            if w.temp > 0.8: c = C_FIRE 
            
            if len(w.history) > 1:
                hx = [h[0] for h in w.history]
                hy = [h[1] for h in w.history]
                ax.plot(hx, hy, color=c, linewidth=3, alpha=0.6)
            
            # Head (High zorder to pop)
            ax.plot(w.pos[0], w.pos[1], marker='v', color=c, markersize=8, zorder=11, markeredgecolor='black', markeredgewidth=0.5)
            
            if w.temp > 0.5:
                # Shockwave
                r = 1500 * w.temp 
                circ = Circle((w.pos[0], w.pos[1]), r, color=C_FIRE, alpha=0.2)
                ax.add_patch(circ)

        # 5. GROUND
        if ylim[0] < 5000:
             ax.axhline(0, color=C_FIRE, linewidth=3)
             for gx in range(-50000, 50001, 5000):
                 ax.plot([gx, gx], [0, 10000], color=C_FIRE, alpha=0.15)

        for ex in explosions:
             circ = Circle((ex['p'][0], ex['p'][1]), ex['r'], color=C_CORE, alpha=ex['a'])
             ax.add_patch(circ)
             circ2 = Circle((ex['p'][0], ex['p'][1]), ex['r']*1.4, color=C_FIRE, fill=False, linewidth=4, alpha=ex['a'])
             ax.add_patch(circ2)

        # 6. UI (High Contrast)
        ui_y = 0.95
        
        # Left: Phase
        txt_phase = PHASE
        if PHASE == "DESCENT": txt_phase = "TERMINAL"
        ax.text(0.05, ui_y, txt_phase, transform=ax.transAxes, color='white', ha='left', 
                fontsize=20, fontname='monospace', weight='bold', path_effects=stroke)
        
        # Right: Data
        txt_data = f"ALT: {int(bus.pos[1])}m"
        ax.text(0.95, ui_y, txt_data, transform=ax.transAxes, color=C_CYAN, ha='right', 
                fontsize=20, fontname='monospace', path_effects=stroke)

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"))
        plt.close(fig)

if __name__ == "__main__": run()
