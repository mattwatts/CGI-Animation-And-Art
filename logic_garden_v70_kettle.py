"""
UNE DEEP RESEARCH PROTOCOL v2.2 - SOVEREIGN CODE
SCRIPT: logic_garden_v70_kettle.py
MODE:   Retro (VIC-II Emulation)
TARGET: Nuclear Thermodynamics (PWR Simulation)
STYLE:  "The Kettle" | 20s | C64 Palette | Educational Mode

AUTHOR: Matt Watts / Assistant Protocol
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# --- 1. THE VIC-II PALETTE ---
C64 = np.array([
    [0.00, 0.00, 0.00], # 0: Black
    [1.00, 1.00, 1.00], # 1: White (Steam Peak)
    [0.53, 0.00, 0.00], # 2: Red (Hot Water)
    [0.45, 0.75, 0.79], # 3: Cyan
    [0.55, 0.17, 0.55], # 4: Purple
    [0.37, 0.65, 0.29], # 5: Green (Uranium)
    [0.21, 0.16, 0.47], # 6: Blue (Cold Water)
    [0.93, 0.94, 0.46], # 7: Yellow (Steam)
    [0.55, 0.31, 0.08], # 8: Orange (Warm Primary)
    [0.28, 0.20, 0.00], # 9: Brown
    [0.75, 0.42, 0.43], # 10: Light Red (Superhot Primary)
    [0.33, 0.33, 0.33], # 11: Dark Grey
    [0.47, 0.47, 0.47], # 12: Grey (Pipes)
    [0.63, 0.95, 0.61], # 13: Light Green
    [0.42, 0.37, 0.71], # 14: Light Blue (Feedwater)
    [0.70, 0.70, 0.70]  # 15: Light Grey
])

# --- 2. CONFIGURATION ---
FPS = 30
DURATION = 20
TOTAL_FRAMES = FPS * DURATION
W, H = 320, 200

# STRUCTURE ZONES
CORE_X, CORE_Y = 60, 120
SG_X, SG_Y = 160, 100 # Steam Generator
TURB_X, TURB_Y = 260, 80

class FluidPacket:
    def __init__(self, loop_type, path_nodes):
        self.loop = loop_type # "PRIMARY" or "SECONDARY"
        self.points = path_nodes
        self.progress = 0.0
        self.speed = 1.0 if loop_type == "PRIMARY" else 0.8
        self.temp = 0.0 # 0.0 (Cold) to 1.0 (Hot)

    def update(self):
        self.progress += self.speed
        if self.progress >= len(self.points) - 1:
            self.progress = 0

def get_path_point(packet):
    idx = int(packet.progress)
    next_idx = (idx + 1) % len(packet.points)
    t = packet.progress - idx
    
    p1 = packet.points[idx]
    p2 = packet.points[next_idx]
    
    x = p1[0] * (1-t) + p2[0] * t
    y = p1[1] * (1-t) + p2[1] * t
    return int(x), int(y)

def define_paths():
    # PRIMARY LOOP (Left loop: Core -> SG -> Core)
    # Rectangle with chamfered corners logic simplified to nodes
    p_primary = [
        (CORE_X, CORE_Y+40), (CORE_X, CORE_Y-20), # Up through Core
        (SG_X-10, SG_Y-20), (SG_X-10, SG_Y+20),   # Down through SG Tubes
        (CORE_X+20, CORE_Y+40), (CORE_X, CORE_Y+40) # Back to Pump/Core
    ]
    
    # SECONDARY LOOP (Right loop: SG -> Turbine -> Condenser -> SG)
    p_secondary = [
        (SG_X+10, SG_Y+40), (SG_X+10, SG_Y-40), # Up through SG Shell
        (TURB_X, TURB_Y),                       # Across to Turbine
        (TURB_X, TURB_Y+60),                    # Down to Condenser
        (SG_X+20, SG_Y+40)                      # Back to Feedwater
    ]
    
    # Interpolate for smoothness
    final_p = []
    final_s = []
    
    # Simple linear interpolation helper
    def interpolate(nodes, steps_per_seg=20):
        path = []
        for i in range(len(nodes)):
            p1 = nodes[i]
            p2 = nodes[(i+1)%len(nodes)]
            dist = np.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)
            steps = int(dist) # 1 pixel per step
            for s in range(steps):
                t = s / steps
                path.append((p1[0]*(1-t)+p2[0]*t, p1[1]*(1-t)+p2[1]*t))
        return path

    return interpolate(p_primary), interpolate(p_secondary)

def generate_kettle():
    out_dir = "logic_garden_kettle_frames"
    os.makedirs(out_dir, exist_ok=True)
    
    print(f"[C64] SCRAM Check complete. Reactor Startup...")
    
    path_prim, path_sec = define_paths()
    
    packets = []
    # Spawn Primary Packets
    for i in range(0, len(path_prim), 4): # Density
        p = FluidPacket("PRIMARY", path_prim)
        p.progress = i
        packets.append(p)
        
    # Spawn Secondary Packets
    for i in range(0, len(path_sec), 5):
        p = FluidPacket("SECONDARY", path_sec)
        p.progress = i
        packets.append(p)
        
    turbine_angle = 0.0
    
    for f in range(TOTAL_FRAMES):
        # 1. INIT BUFFER
        buffer = np.zeros((H, W, 3))
        buffer[:] = C64[0]
        
        # 2. DRAW INFRASTRUCTURE (Grey Lines)
        # Reactor Vessel
        col_pipe = C64[12]
        # Basic boxes for structure
        buffer[CORE_Y-30:CORE_Y+50, CORE_X-15:CORE_X+15] = col_pipe # Core
        buffer[SG_Y-50:SG_Y+50, SG_X-20:SG_X+20] = col_pipe # Steam Gen
        
        # Fuel Rods (Pulsing Green)
        pulse = (np.sin(f*0.2) + 1) * 0.5
        col_fuel = C64[5] * pulse + C64[13] * (1-pulse)
        buffer[CORE_Y:CORE_Y+30, CORE_X-5:CORE_X+5] = col_fuel
        
        # 3. UPDATE FLUIDS & THERMODYNAMICS
        for p in packets:
            p.update()
            x, y = get_path_point(p)
            
            # THERMO LOGIC
            if p.loop == "PRIMARY":
                # In Core? Heat up.
                if CORE_Y-20 < y < CORE_Y+40 and abs(x - CORE_X) < 20:
                    p.temp = min(1.0, p.temp + 0.05)
                # In SG? Cool down (Transfer to Secondary)
                if abs(x - (SG_X-10)) < 10 and abs(y - SG_Y) < 30:
                    p.temp = max(0.2, p.temp - 0.03)
                    
            if p.loop == "SECONDARY":
                # In SG? Heat up (Boil)
                if abs(x - (SG_X+10)) < 15 and abs(y - SG_Y) < 40:
                    p.temp = min(1.0, p.temp + 0.04)
                # At Turbine? Lose Energy (Work)
                if abs(x - TURB_X) < 20 and abs(y - TURB_Y) < 20:
                    p.temp = max(0.0, p.temp - 0.1) # Work extracted
                    turbine_angle += 0.2 # Spin turbine
                # Condenser (Bottom)
                if y > TURB_Y+20:
                    p.temp = max(0.0, p.temp - 0.05) # Cooling loop (implied)

            # 4. RENDER FLUIDS
            # Color Mapping
            c = C64[11] # Default
            
            if p.loop == "PRIMARY":
                # Cold: 2 (Red), Hot: 10 (Light Red/Pinkish) to indicate Radiation/Heat
                # Visual Distinction: Primary is RED based
                if p.temp > 0.8: c = C64[10] # Superhot
                elif p.temp > 0.5: c = C64[8] # Orange
                else: c = C64[2] # Red
                
            if p.loop == "SECONDARY":
                # Water: 6 (Blue), 14 (Lt Blue). Steam: 7 (Yellow), 1 (White)
                if p.temp > 0.9: c = C64[1] # White Steam
                elif p.temp > 0.6: c = C64[7] # Yellow Steam
                elif p.temp > 0.3: c = C64[14] # Hot Water
                else: c = C64[6] # Cold Water
            
            # Draw Packet (2x2 pixel)
            if 0 < x < W-1 and 0 < y < H-1:
                buffer[y, x] = c
                buffer[y+1, x] = c
                buffer[y, x+1] = c
                buffer[y+1, x+1] = c
                
        # 5. DRAW TURBINE (Procedural Sprite)
        tx, ty = TURB_X, TURB_Y
        # Draw Hub
        buffer[ty-2:ty+2, tx-2:tx+2] = C64[11]
        # Draw Blades
        for angle_offset in [0, np.pi/2, np.pi, 3*np.pi/2]:
            a = turbine_angle + angle_offset
            bx = int(tx + np.cos(a) * 12)
            by = int(ty + np.sin(a) * 12)
            # Line
            # Simple line draw (reusing Bresenham logic conceptually)
            num_pts = 10
            for k in range(num_pts):
                lx = int(tx + (bx-tx)*k/num_pts)
                ly = int(ty + (by-ty)*k/num_pts)
                if 0 <= lx < W and 0<= ly < H:
                    buffer[ly, lx] = C64[15]
                    
        # 6. HUD / DIAGRAM LABELS
        fig = plt.figure(figsize=(10, 10), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        fig.add_axes(ax)
        ax.set_axis_off()
        ax.imshow(buffer, interpolation='nearest', aspect='auto')
        
        # Labels
        f_size = 12
        ax.text(CORE_X, CORE_Y+60, "PRIMARY LOOP\n(RADIOACTIVE)", color="#ff5555", ha='center', fontfamily='monospace', fontweight='bold', fontsize=f_size)
        ax.text(SG_X, SG_Y+60, "HEAT\nEXCHANGER", color="#ffff55", ha='center', fontfamily='monospace', fontweight='bold', fontsize=f_size)
        ax.text(TURB_X, TURB_Y-20, "TURBINE", color="#55ffff", ha='center', fontfamily='monospace', fontweight='bold', fontsize=f_size)
        
        ax.text(W/2, 20, "LOGIC GARDEN 19: THE KETTLE", color="#aaaaaa", ha='center', fontfamily='monospace', fontweight='bold', fontsize=18)
        ax.text(W/2, 180, "THE FIRE AND THE STEAM NEVER TOUCH", color="#ffffff", ha='center', fontfamily='monospace', fontweight='bold', fontsize=14)

        filename = os.path.join(out_dir, f"kettle_{f:04d}.png")
        plt.savefig(filename, facecolor='black')
        plt.close()
        
        if f % 60 == 0:
            print(f"Frame {f}/{TOTAL_FRAMES}")

if __name__ == "__main__":
    generate_kettle()
