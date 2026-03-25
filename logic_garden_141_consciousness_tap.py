"""
SOVEREIGN CODE: logic_garden_141_consciousness_tap.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python High-Fidelity Simulator (Quantum Solid-State Emulation)
SCENE: Logic Garden 141 (Consciousness Tap / The Neural Transistor)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# -------- COMPILE-TIME METRICS --------
FPS = 60                        # 30Hz Gamma Lock Compatibility
DURATION = 24                   # 24-Second Phase Transition
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_141_mind_tap"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (QUANTUM & SOLID-STATE) --------
C_VOID = '#020205'              # Absolute Black (The Void)
C_SUBSTRATE = '#0a0a14'         # Neural Substrate Background
C_PURPLE = '#7B00FF'            # Superposition Wave A (Entropy)
C_CYAN = '#00FFCC'              # Superposition Wave B (Entropy)
C_GOLD = '#FFD700'              # Consciousness / The Observer (Gate)
C_MANTIS = '#39FF14'            # Terminal Green (4D Spacetime Flow)
C_TEXT = '#FFFFFF'              # UI Readout
C_DEPLETION = '#4A0033'         # Cognitive Blockage (Distraction)

def run():
    print(f"LOGIC GARDEN 141: THE CONSCIOUSNESS TAP")
    print(f"Executing: {FPS} FPS | Total: {TOTAL_FRAMES} frames")
    
    # ------------------------------------------------------------------
    # SYSTEM ARCHITECTURE: THE NEURAL TRANSISTOR
    # ------------------------------------------------------------------
    np.random.seed(137) # Fine Structure Constant
    
    NUM_QUANTA = 400
    quanta = []
    
    # Discrete columns for 4D Spacetime deterministic alignment (The Lattice)
    discrete_columns = [460, 500, 540, 580, 620]

    for i in range(NUM_QUANTA):
        quanta.append({
            'pos': np.array([np.random.uniform(250, 830), np.random.uniform(1410, 1790)]),
            'vel': np.array([np.random.uniform(-10, 10), np.random.uniform(-10, 10)]),
            'state': 'WAVE',      # WAVE -> COLLAPSING -> PARTICLE
            'color': C_CYAN if np.random.rand() > 0.5 else C_PURPLE,
            'phase_offset': np.random.uniform(0, 2 * np.pi), # Individual wave frequency
            'target_col': np.random.choice(discrete_columns),
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
        # GATE LOGIC CONTROLLER (THE ATTENTION DEMON)
        # ------------------------------------------------------------------
        # 00.0 - 04.0s: State 0 (Unconscious / High Entropy)
        # 04.0 - 10.0s: State 1 (Directed Attention / Decoherence)
        # 10.0 - 13.0s: State 0 (Distraction / Cognitive Drift)
        # 13.0 - 24.0s: State 1 (30Hz Gamma Lock / Terminal Green Flow)
        
        target_attention = 0.0
        if 4.0 <= t_sec < 10.0:
            target_attention = 1.0
        elif 13.0 <= t_sec < 24.0:
            target_attention = 1.0
            
        if f == 0: smooth_gate = 0.0
        smooth_gate += (target_attention - smooth_gate) * 0.1 
        
        # Depletion Region (Cognitive Bounding Box)
        dep_left = 540 - (100 * smooth_gate)
        dep_right = 540 + (100 * smooth_gate)

        # The 30Hz Gamma Pulse (For UI and Gate)
        gamma_pulse = 1.0 if f % 2 == 0 else 0.3

        # ------------------------------------------------------------------
        # SOLID-STATE / CORTICAL GEOMETRY
        # ------------------------------------------------------------------
        ax.add_patch(plt.Rectangle((240, 200), 600, 1600, color=C_SUBSTRATE, alpha=0.5))
        
        # Hemisphere Pads (The Brain / Gate)
        gate_glow = smooth_gate * 0.4 * (1.0 if target_attention==0 else gamma_pulse)
        gate_color = C_GOLD if smooth_gate > 0.5 else C_VOID
        
        ax.add_patch(plt.Rectangle((240, 900), 180, 500, fill=True, color=gate_color, alpha=gate_glow))
        ax.add_patch(plt.Rectangle((660, 900), 180, 500, fill=True, color=gate_color, alpha=gate_glow))
        ax.add_patch(plt.Rectangle((240, 900), 180, 500, fill=False, edgecolor=C_GOLD, lw=3))
        ax.add_patch(plt.Rectangle((660, 900), 180, 500, fill=False, edgecolor=C_GOLD, lw=3))

        # Nila Bindu (The Observer Core) in the center of the Gate
        bindu_scale = smooth_gate
        if bindu_scale > 0.1:
            ax.scatter(540, 1150, s=800 * bindu_scale, c=C_GOLD, alpha=0.2 * gamma_pulse, edgecolors='none')
            ax.scatter(540, 1150, s=200 * bindu_scale, c=C_GOLD, alpha=0.8, edgecolors='none')
        
        # Cognitive Blockage (When unconscious, reality cannot compute)
        if dep_left < 535: 
            ax.add_patch(plt.Rectangle((420, 1370), dep_left - 420, 30, color=C_DEPLETION, hatch='\\\\'))
            ax.add_patch(plt.Rectangle((dep_right, 1370), 660 - dep_right, 30, color=C_DEPLETION, hatch='\\\\'))

        # ------------------------------------------------------------------
        # QUANTUM-TO-CLASSICAL PHYSICS ENGINE (PHASE DECOHERENCE)
        # ------------------------------------------------------------------
        for q in quanta:
            px, py = q['pos']
            vx, vy = q['vel']
            
            # 1. THE QUANTUM OCEAN (Top Chamber - Pure Thought / Wave State)
            if py >= 1400:
                q['state'] = 'WAVE'
                # Superposition thrashing (Abstract non-locality)
                wave_noise_x = np.sin(t_sec * 10 + q['phase_offset']) * 8
                wave_noise_y = np.cos(t_sec * 8 + q['phase_offset']) * 8
                vx = vx * 0.95 + wave_noise_x * 0.1
                vy = vy * 0.95 + wave_noise_y * 0.1 - 0.5 # Slight gravity pull
                
                if px + vx < 245 or px + vx > 835: vx *= -1
                if py + vy > 1795: vy *= -1
                
                if py + vy < 1400:
                    if px > dep_left and px < dep_right:
                        pass # Collapse begins
                    else:
                        vy *= -1
                        py = 1400
                        
            # 2. THE PINEAL CHOKEPOINT (Decoherence Engine / Bounding Box)
            elif 900 <= py < 1400:
                q['state'] = 'COLLAPSING'
                
                # Critical Damping: Snap to discrete 4D column
                dist_to_col = q['target_col'] - px
                vx = dist_to_col * 0.15 # Strong pull to math lattice
                vy -= 1.0 # Accelerate downward
                
                boundary_l = max(425, dep_left - 5)
                boundary_r = min(655, dep_right + 5)
                if px + vx < boundary_l: vx = abs(vx) + 1
                if px + vx > boundary_r: vx = -abs(vx) - 1
                
            # 3. 4D SPACETIME MANIFESTATION (Bottom Drain - Terminal Green)
            elif py < 900:
                q['state'] = 'PARTICLE'
                # Perfect Laminar Flow. No side-to-side variation. Absolute Math.
                vx = (q['target_col'] - px) * 0.5 # Total lock
                vy = np.clip(vy, -30, -15) # Steady descent rate
                
                # Recycle abstract thought into the void loop
                if py + vy < 205:
                    py = 1750
                    px = np.random.uniform(250, 830)
                    vx = np.random.uniform(-10, 10)
                    vy = np.random.uniform(-5, 5)
                    q['history'] = []

            # Velocity Terminals
            vx = max(min(vx, 30), -30)
            vy = max(min(vy, 40), -40)

            q['vel'] = np.array([vx, vy])
            q['pos'] = np.array([px + vx, py + vy])
            
            q['history'].append(np.copy(q['pos']))
            if len(q['history']) > 8: q['history'].pop(0)

            # ------------------------------------------------------------------
            # VISUAL RENDERING: FROM ENTROPY TO LATTICE
            # ------------------------------------------------------------------
            # 1. ALWAYS determine the correct color based on Phase State
            if q['state'] == 'WAVE':
                c_trail = q['color']
                thick = 2
            elif q['state'] == 'COLLAPSING':
                c_trail = C_GOLD
                thick = 3
            else:
                c_trail = C_MANTIS
                thick = 4 if np.random.rand() > 0.5 else 2 # Digital data stream effect

            # 2. Draw the kinetic trail if history exists
            if len(q['history']) > 2:
                pts = np.array(q['history'])
                alphas = np.linspace(0.0, 0.9, len(pts))
                for i in range(len(pts)-1):
                    ax.plot(pts[i:i+2, 0], pts[i:i+2, 1], color=c_trail, lw=thick, alpha=alphas[i])
                    
            # 3. Render the particle head 
            head_color = C_TEXT if q['state'] == 'PARTICLE' else c_trail
            ax.scatter(q['pos'][0], q['pos'][1], s=12 if q['state']=='WAVE' else 20, c=head_color, edgecolors='none', zorder=5)

        # ------------------------------------------------------------------
        # UI DECOUPLING & THE FLIGHT RECORDER
        # ------------------------------------------------------------------
        # Header Overlay
        ax.add_patch(plt.Rectangle((0, 1850), 1080, 70, color=C_VOID, alpha=0.9))
        ax.axhline(1850, color=C_TEXT, lw=1)
        ax.text(40, 1870, "LOGIC GARDEN 141 :: THE CONSCIOUSNESS TAP", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold')

        # Telemetry Block (Bottom HUD)
        ax.add_patch(plt.Rectangle((0, 0), 1080, 180, color=C_SUBSTRATE, alpha=0.9))
        ax.axhline(180, color=C_TEXT, lw=2)
        
        sys_state_txt = "QUANTUM SUPERPOSITION (Wandering Phase)"
        sys_state_col = C_PURPLE
        if smooth_gate > 0.8:
            sys_state_txt = "PHASE DECOHERENCE (4D Manifestation)"
            sys_state_col = C_MANTIS
        elif target_attention != smooth_gate:
            sys_state_txt = "COMPILER INITIALIZING..."
            sys_state_col = C_GOLD
            
        ax.text(40, 130, f"STRUCTURAL SCHEMA : THE NEURAL TRANSISTOR", color=C_TEXT, fontsize=20, fontname='monospace')
        
        # Strobe the Gate metric if fully active
        gate_metric_color = C_GOLD
        if target_attention == 1.0 and gamma_pulse > 0.5: gate_metric_color = C_TEXT
        ax.text(40, 80, f"ATTENTIONAL VOLTAGE: [ {target_attention:.1f} ]", color=gate_metric_color, fontsize=24, fontname='monospace', weight='bold')
        
        ax.text(40, 30, f"SYSTEM VECTOR      : {sys_state_txt}", color=sys_state_col, fontsize=22, fontname='monospace', weight='bold')

        # Annotations on the Neural Architecture
        ax.text(540, 1750, "SOURCE: PROBABILITY CLOUD (ENTROPY)", color=C_CYAN, ha='center', fontsize=20, fontname='monospace', weight='bold', alpha=0.6)
        if target_attention == 1.0:
            ax.text(540, 250, "DRAIN: COMPILE-TIME MET", color=C_MANTIS, ha='center', fontsize=20, fontname='monospace', weight='bold', alpha=0.8)
        
        ax.text(330, 1150, "CORTEX", color=C_GOLD, ha='center', fontsize=20, fontname='monospace', alpha=0.6)
        ax.text(750, 1150, "CORTEX", color=C_GOLD, ha='center', fontsize=20, fontname='monospace', alpha=0.6)
        ax.text(540, 1220, "OBSERVER NODE", color=C_GOLD, ha='center', fontsize=18, fontname='monospace')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close(fig)

if __name__ == "__main__": run()
