"""
SOVEREIGN CODE: logic_garden_139_transistor.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python High-Fidelity Simulator (Kinetic/Solid-State Emulation)
SCENE: Logic Garden 139 (The Transistor: Friction vs Flow)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 24                   # 24-Second Logic Cycle
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_139_transistor"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (HIGH-VOLTAGE) --------
C_VOID = '#020205'              # Absolute Black
C_SILICON = '#081015'           # Substrate Background
C_RED = '#FF003C'               # Thermal Entropy (Friction)
C_GOLD = '#FFD700'              # Gate Voltage (The Signal)
C_CYAN = '#00FFCC'              # Laminar Flow (Directed Kinetic)
C_MANTIS = '#39FF14'            # Terminal Green (Logic 1)
C_TEXT = '#FFFFFF'              # UI Readout
C_DEPLETION = '#4A0010'         # Closed Bounding Box Barrier

def run():
    print(f"LOGIC GARDEN 139: THE TRANSISTOR (FRICTION VS FLOW)")
    print(f"Executing: {FPS} FPS | Total: {TOTAL_FRAMES} frames")
    
    # ------------------------------------------------------------------
    # SYSTEM ARCHITECTURE & PARTICLE INSTANTIATION
    # ------------------------------------------------------------------
    np.random.seed(42) # Compile-Time Safety
    
    NUM_ELECTRONS = 450
    electrons = []
    
    # We conceptualize a vertical FET (Field-Effect Transistor)
    # The "Data Waterfall"
    # Source (Top):     y = [1400, 1800], x = [240, 840]
    # Gate Chokepoint:  y = [900, 1400],  x = [440, 640]  (Left Pad: 240-420, Right Pad: 660-840)
    # Drain (Bottom):   y = [200, 900],   x = [240, 840]
    
    for i in range(NUM_ELECTRONS):
        electrons.append({
            'pos': np.array([np.random.uniform(250, 830), np.random.uniform(1410, 1790)]),
            'vel': np.array([np.random.uniform(-15, 15), np.random.uniform(-15, 15)]),
            'state': 'FRICTION', # FRICTION (Red) -> FLOW (Cyan)
            'history': []
        })

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        fig.patch.set_facecolor(C_VOID)
        ax.set_facecolor(C_VOID)
        ax.set_xlim(0, 1080)
        ax.set_ylim(0, 1920)

        # ------------------------------------------------------------------
        # GATE LOGIC CONTROLLER (THE MAXWELL DEMON)
        # ------------------------------------------------------------------
        # The transistor switches states based on this timeline:
        # 0.0 - 04.0s: State 0 (Cut-Off / High Friction)
        # 04.0 - 10.0s: State 1 (Saturation / Laminar Flow)
        # 10.0 - 12.0s: State 0 (Cut-Off)
        # 12.0 - 18.0s: High-Frequency Pulse Modulation (01010101)
        # 18.0 - 24.0s: State 1 (Terminal Green Flow)
        
        target_gate = 0.0
        if 4.0 <= t_sec < 10.0:
            target_gate = 1.0
        elif 12.0 <= t_sec < 18.0:
            # PWM Clock Cycle visualization (~3Hz)
            if (f % 20) < 10: target_gate = 1.0
        elif t_sec >= 18.0:
            target_gate = 1.0
            
        # Smooth phase transition (RC time constant emulation)
        # To avoid NameError in the loop, initialize smooth_gate in frame 0
        if f == 0: smooth_gate = 0.0
        smooth_gate += (target_gate - smooth_gate) * 0.15 
        
        # Calculate Depletion Region (The visual Bounding Box)
        # When 0, depletion meets in middle (x=540). When 1, retracts to gate walls (440 & 640)
        dep_left = 540 - (100 * smooth_gate)
        dep_right = 540 + (100 * smooth_gate)

        # ------------------------------------------------------------------
        # DRAWING THE SOLID-STATE GEOMETRY
        # ------------------------------------------------------------------
        # Substrate background
        ax.add_patch(plt.Rectangle((240, 200), 600, 1600, color=C_SILICON, alpha=0.5))
        
        # Gate Contact Pads (The Command Inputs)
        gate_color = C_GOLD if smooth_gate > 0.5 else C_VOID
        gate_glow = smooth_gate * 0.5
        ax.add_patch(plt.Rectangle((240, 900), 180, 500, fill=True, color=gate_color, alpha=gate_glow))
        ax.add_patch(plt.Rectangle((660, 900), 180, 500, fill=True, color=gate_color, alpha=gate_glow))
        ax.add_patch(plt.Rectangle((240, 900), 180, 500, fill=False, edgecolor=C_GOLD, lw=4))
        ax.add_patch(plt.Rectangle((660, 900), 180, 500, fill=False, edgecolor=C_GOLD, lw=4))
        
        # The Depletion Region (The Resistance Barricade)
        if dep_left < 538: # Draw physical blockage if not fully open
            ax.add_patch(plt.Rectangle((420, 1370), dep_left - 420, 30, color=C_DEPLETION, hatch='////'))
            ax.add_patch(plt.Rectangle((dep_right, 1370), 660 - dep_right, 30, color=C_DEPLETION, hatch='////'))

        # ------------------------------------------------------------------
        # KINETIC ENGINE (PARTICLE PHYSICS & VOLUME MANAGEMENT)
        # ------------------------------------------------------------------
        for e in electrons:
            px, py = e['pos']
            vx, vy = e['vel']
            
            # 1. Source Chamber (High Entropy / Chaos)
            if py >= 1400:
                e['state'] = 'FRICTION'
                # Outer boundaries
                if px + vx < 245 or px + vx > 835: vx *= -1
                if py + vy > 1795: vy *= -1
                
                # Floor interaction (The Chokepoint)
                if py + vy < 1400:
                    # Check if particle hits the open channel or the depletion wall
                    if px > dep_left and px < dep_right:
                        # Success - Fall into channel
                        pass 
                    else:
                        # Blocked - Bounce back up (Friction remains)
                        vy *= -1
                        py = 1400
                        
            # 2. The Channel (Phase Transition / Laminar Flow)
            elif 900 <= py < 1400:
                e['state'] = 'FLOW'
                # Vector Alignment (Critical Damping applied to X velocity)
                vx *= 0.85 
                # Gravity / E-Field accelerates downward
                vy -= 1.5 
                
                # Channel Walls constraint
                # Note: To prevent escaping through sides if channel closes WHILE inside
                boundary_l = max(425, dep_left - 5)
                boundary_r = min(655, dep_right + 5)
                if px + vx < boundary_l: vx = abs(vx) + 2
                if px + vx > boundary_r: vx = -abs(vx) - 2
                
            # 3. Drain Chamber (The Output)
            elif py < 900:
                e['state'] = 'FLOW'
                # Maintain downward velocity, slight random scatter like hitting a pool
                if vy < 0: vy *= 0.98
                vx += np.random.uniform(-1.0, 1.0)
                
                if px + vx < 245 or px + vx > 835: vx *= -1
                
                # Teleport back to Source when it hits bottom to loop the current
                if py + vy < 205:
                    py = 1750
                    px = np.random.uniform(250, 830)
                    vx = np.random.uniform(-15, 15)
                    vy = np.random.uniform(-15, 15)
                    e['history'] = []

            # Velocity Terminal Limits
            vx = max(min(vx, 30), -30)
            vy = max(min(vy, 40), -40)

            # Apply Physics
            e['vel'] = np.array([vx, vy])
            e['pos'] = np.array([px + vx, py + vy])
            
            # Track History for visual persistence
            e['history'].append(np.copy(e['pos']))
            if len(e['history']) > 6: e['history'].pop(0)

            # ------------------------------------------------------------------
            # PHOSPHOR / GLOW RENDERING
            # ------------------------------------------------------------------
            if len(e['history']) > 2:
                pts = np.array(e['history'])
                c_trail = C_RED if e['state'] == 'FRICTION' else C_CYAN
                alphas = np.linspace(0.0, 0.8, len(pts))
                for i in range(len(pts)-1):
                    ax.plot(pts[i:i+2, 0], pts[i:i+2, 1], color=c_trail, lw=3, alpha=alphas[i])
                    
            head_color = C_GOLD if e['state'] == 'FRICTION' else C_TEXT
            ax.scatter(e['pos'][0], e['pos'][1], s=15, c=head_color)

        # ------------------------------------------------------------------
        # UI DECOUPLING & STRUCTURAL TELEMETRY
        # ------------------------------------------------------------------
        # Header Protocol
        ax.add_patch(plt.Rectangle((0, 1850), 1080, 70, color=C_VOID, alpha=0.9))
        ax.axhline(1850, color=C_TEXT, lw=1)
        ax.text(40, 1870, "LOGIC GARDEN 139 :: THE MAXWELL DEMON", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold')
        
        # Telemetry Block (Bottom HUD)
        ax.add_patch(plt.Rectangle((0, 0), 1080, 180, color=C_SILICON, alpha=0.8))
        ax.axhline(180, color=C_TEXT, lw=2)
        
        ax.text(40, 130, f"STRUCTURAL SCHEMA : FIELD-EFFECT TRANSISTOR", color=C_TEXT, fontsize=20, fontname='monospace')
        
        status_text = "CUT-OFF (High Friction)"
        status_color = C_RED
        if smooth_gate > 0.8:
            status_text = "SATURATION (Laminar Flow)"
            status_color = C_CYAN
        elif target_gate != smooth_gate:
            status_text = "PHASE TRANSITION"
            status_color = C_GOLD
            
        ax.text(40, 80, f"GATE VOLTAGE LOGIC: [ {target_gate:.1f} ]", color=C_GOLD, fontsize=24, fontname='monospace', weight='bold')
        ax.text(40, 30, f"VOLUME FLOW STATE : {status_text}", color=status_color, fontsize=24, fontname='monospace', weight='bold')

        # Annotations on the silicon
        ax.text(540, 1750, "SOURCE: THERMAL ENTROPY", color=C_RED, ha='center', fontsize=20, fontname='monospace', weight='bold', alpha=0.6)
        if target_gate == 1.0:
            ax.text(540, 500, "DRAIN: COMPILE-TIME MET", color=C_MANTIS, ha='center', fontsize=20, fontname='monospace', weight='bold')
        ax.text(330, 1250, "GATE", color=C_GOLD, ha='center', fontsize=20, fontname='monospace')
        ax.text(750, 1250, "GATE", color=C_GOLD, ha='center', fontsize=20, fontname='monospace')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close(fig)

if __name__ == "__main__": run()
