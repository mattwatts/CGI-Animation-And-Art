"""
SOVEREIGN CODE: logic_garden_143_zen_emergence.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python High-Fidelity Simulator (Vectorized Numpy Array)
SCENE: Logic Garden 143 (The Zen Intersection / Emergent BCI Exocortex)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import math
import os

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 26                   # 26-Second Zen Cycle
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_143_zen"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (HIGH-VOLTAGE) --------
C_VOID = '#020205'              # Absolute Black (The Static Void)
C_CYAN = '#00FFCC'              # Synthetic Hive Mind (Unbound)
C_PURPLE = '#7B00FF'            # High-Dimensional AI Depth
C_GOLD = '#FFD700'              # The Observer Core / Nila Bindu
C_MANTIS = '#39FF14'            # Terminal Green (Emergence)
C_TEXT = '#FFFFFF'              # UI Readout

def run():
    print(f"LOGIC GARDEN 143: THE ZEN INTERSECTION (BCI & AI EMERGENCE)")
    print(f"Executing: {FPS} FPS | Total: {TOTAL_FRAMES} frames")

    np.random.seed(108) # Zen Mala Bead Constant
    
    # ------------------------------------------------------------------
    # SYSTEM ARCHITECTURE: BIOLOGICAL & SYNTHETIC NODES
    # ------------------------------------------------------------------
    N_NODES = 120
    center_pos = np.array([540.0, 1000.0])
    
    # Initial Chaotic AI Swarm (Unbound)
    ai_theta = np.random.uniform(0, 2*math.pi, N_NODES)
    ai_radius = np.random.uniform(200, 700, N_NODES)
    ai_vel_th = np.random.uniform(-0.02, 0.02, N_NODES)
    ai_vel_r = np.random.uniform(-2, 2, N_NODES)
    
    # Final Uniform State (The BCM Exocortex Envelope)
    target_theta = np.linspace(0, 2*math.pi, N_NODES, endpoint=False)
    target_radius = 450.0

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
        # TIMELINE LOGIC CONTROLLER (THE KOAN)
        # ------------------------------------------------------------------
        """
        0.0 -  5.0 : DUALITY (Chaotic Synthetic Cloud + Breathing Core)
        5.0 -  9.0 : THE HANDSHAKE (BCI Tethers fire, Lock initiated)
        9.0 - 15.0 : CRITICAL DAMPING (AI aligns to perfect orbital ring)
        15.0 - 26.0: EMERGENCE (Modular Envelope constructs the Lotus Exocortex)
        """
        sys_state = "DUALITY: BIOLOGICAL AND SYNTHETIC"
        ui_color = C_CYAN
        tether_alpha = 0.0
        lerp_progress = 0.0
        emerge_factor = 0.0
        
        if 5.0 <= t_sec < 9.0:
            sys_state = "BCI HANDSHAKE: NEURAL TETHERS ACTIVE"
            ui_color = C_GOLD
            tether_alpha = min((t_sec - 5.0) / 2.0, 0.4)
            
        elif 9.0 <= t_sec < 15.0:
            sys_state = "PHASE COHERENCE: CRITICAL DAMPING"
            ui_color = C_MANTIS
            tether_alpha = max(0.4 - ((t_sec - 9.0) / 4.0), 0.0)
            # Smooth Hermite Interpolation for absolute visual butter
            raw_p = min((t_sec - 9.0) / 5.0, 1.0)
            lerp_progress = raw_p * raw_p * (3 - 2 * raw_p) 
            
        elif t_sec >= 15.0:
            sys_state = "EMERGENCE: THE LOTUS EXOCORTEX [TATHĀTĀ]"
            ui_color = C_MANTIS
            lerp_progress = 1.0
            emerge_factor = min((t_sec - 15.0) / 10.0, 1.0) # Slowly reveals the math

        # ------------------------------------------------------------------
        # BIOLOGICAL KINEMATICS (THE CORE)
        # ------------------------------------------------------------------
        # 4Hz Theta breathing (Deep Intuition)
        theta_pulse = math.sin(t_sec * 4 * math.pi)
        core_scale = 1.0 + 0.1 * theta_pulse
        core_alpha = 0.8 + 0.2 * theta_pulse
        
        # When emergence happens, the core transitions from flesh to synthetic
        c_core = C_GOLD if t_sec < 17.0 else C_MANTIS
        c_core_glow = C_GOLD if t_sec < 17.0 else C_CYAN
        
        ax.scatter(center_pos[0], center_pos[1], s=4000 * core_scale, c=c_core_glow, alpha=0.1 * core_alpha, edgecolors='none')
        ax.scatter(center_pos[0], center_pos[1], s=800 * core_scale, c=c_core, alpha=0.5 * core_alpha, edgecolors='none')
        ax.scatter(center_pos[0], center_pos[1], s=200, c=C_TEXT, alpha=1.0, edgecolors='none')

        # ------------------------------------------------------------------
        # SYNTHETIC KINEMATICS (THE HIVE MIND)
        # ------------------------------------------------------------------
        # Unbound physics execution
        ai_theta += ai_vel_th
        ai_radius += ai_vel_r
        # Bounding box for chaos
        ai_radius = np.clip(ai_radius, 150, 750) 
        
        # Apply BCI Critical Damping (Lerp to the target math)
        current_theta = (1.0 - lerp_progress) * ai_theta + (lerp_progress * target_theta)
        current_radius = (1.0 - lerp_progress) * ai_radius + (lerp_progress * target_radius)
        
        x = center_pos[0] + current_radius * np.cos(current_theta)
        y = center_pos[1] + current_radius * np.sin(current_theta)
        pos = np.column_stack((x, y))

        # 1. Render Neural Tethers (Phase 2)
        if tether_alpha > 0:
            tether_segs = [[(center_pos[0], center_pos[1]), (pos[i,0], pos[i,1])] for i in range(N_NODES)]
            # Only connect closer nodes visually for bandwidth optimization look
            mask = ai_radius < 500
            active_segs = [tether_segs[i] for i in range(N_NODES) if mask[i]]
            ax.add_collection(LineCollection(active_segs, colors=C_GOLD, lw=1.5, alpha=tether_alpha))

        # 2. Render Unbound AI Connections (Delaunay/Distance style)
        if lerp_progress < 1.0:
            chaos_alpha = 1.0 - lerp_progress
            dist_matrix = np.linalg.norm(pos[:, np.newaxis] - pos, axis=2)
            # Find close pairs
            pairs = np.argwhere((dist_matrix > 0) & (dist_matrix < 80))
            chaos_segs = [[(pos[i,0], pos[i,1]), (pos[j,0], pos[j,1])] for i, j in pairs]
            ax.add_collection(LineCollection(chaos_segs, colors=C_PURPLE, lw=1, alpha=0.2 * chaos_alpha))

        # 3. Render Emergent Geometric Envelope (Phase 4 - The Lotus)
        if emerge_factor > 0:
            # The Modular Math of Amor Fati
            # M sweeps from 2.0 to 51.0 over 10 seconds. We lock at M=51 for the 50-petal lotus.
            M = 2.0 + (emerge_factor * 49.0)
            
            pA = pos
            # Calculate target point B using continuous modular offset
            # Index continuous logic: i_target = (i * M) % N
            idx_target = (np.arange(N_NODES) * M) % N_NODES
            # We must lerp between the two closest integer nodes to keep the lines silky smooth
            idx_low = np.floor(idx_target).astype(int)
            idx_high = (idx_low + 1) % N_NODES
            idx_frac = idx_target - idx_low
            
            pB = (1 - idx_frac[:, np.newaxis]) * pos[idx_low] + (idx_frac[:, np.newaxis]) * pos[idx_high]
            
            lotus_segs = [[(pA[i,0], pA[i,1]), (pB[i,0], pB[i,1])] for i in range(N_NODES)]
            
            # Neon Pop styling: Brilliant Cyan to Terminal Green transition
            lotus_c = C_CYAN if t_sec < 22 else C_MANTIS
            line_alpha = 0.5 * emerge_factor
            if t_sec > 25: line_alpha = 0.8 # Final flash lock
            
            lc = LineCollection(lotus_segs, colors=lotus_c, lw=1.5, alpha=line_alpha)
            ax.add_collection(lc)

        # Render Nodes
        node_c = C_CYAN
        if lerp_progress > 0: node_c = C_GOLD # Acquiring data
        if emerge_factor == 1.0: node_c = C_TEXT # Absolute clarity limit
        
        ax.scatter(pos[:, 0], pos[:, 1], s=25 - (15*lerp_progress), c=node_c, edgecolors='none', zorder=5)

        # ------------------------------------------------------------------
        # UI DECOUPLING & THE FLIGHT RECORDER
        # ------------------------------------------------------------------
        # Header Overlay
        ax.add_patch(plt.Rectangle((0, 1850), 1080, 70, color=C_VOID, alpha=0.9))
        ax.axhline(1850, color=ui_color, lw=2)
        ax.text(40, 1870, "LOGIC GARDEN 143 :: EMERGENT EXOCORTEX", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold')

        # Telemetry Block (Bottom HUD)
        ax.add_patch(plt.Rectangle((0, 0), 1080, 180, color=C_VOID, alpha=0.95))
        ax.axhline(180, color=ui_color, lw=2)
        
        ax.text(40, 130, f"STRUCTURAL SCHEMA : BCI NEURAL ENTRAINMENT", color=C_TEXT, fontsize=20, fontname='monospace')
        
        # State Pulse Matrix
        pulse = ui_color if (f % 20 < 10) else C_TEXT
        ax.text(40, 80, f"SYSTEM VECTOR     : {sys_state}", color=pulse, fontsize=20, fontname='monospace', weight='bold')
        
        # Mathematical HUD parameters
        fric = max(1.0 - lerp_progress, 0.0)
        flow = lerp_progress
        mult = 2.0 + (emerge_factor * 49.0) if emerge_factor > 0 else 0.0
        
        ax.text(40, 30, f"FRICTION: {fric:.2f} | FLOW: {flow:.2f} | M-VAL: {mult:>05.2f}", color=C_TEXT, fontsize=18, fontname='monospace')

        # Zen Annotations
        if emerge_factor > 0.9:
            ax.text(540, 1550, "C_VOID == STRUCTURE", color=C_MANTIS, ha='center', fontsize=20, fontname='monospace', alpha=0.6)
            ax.text(540, 450, "[ TATHĀTĀ ]", color=C_GOLD, ha='center', fontsize=26, fontname='monospace', alpha=0.9)

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close(fig)

if __name__ == "__main__": run()
