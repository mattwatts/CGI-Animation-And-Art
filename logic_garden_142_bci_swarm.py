"""
SOVEREIGN CODE: logic_garden_142_bci_swarm.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python High-Fidelity Simulator (Vectorized PSO/BCI Emulation)
SCENE: Logic Garden 142 (The Swarm Compiler)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 24                   # 24-Second Cognitive Cycle
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_142_swarm"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (HIGH-VOLTAGE) --------
C_VOID = '#020205'              # Absolute Black (The Void)
C_GRID = '#0A1520'              # Cortical Substrate Grid
C_CYAN = '#00FFCC'              # Swarm Search Phase (Entropy)
C_MAGENTA = '#FF00FF'           # Personal Best (pBest) Memory
C_GOLD = '#FFD700'              # BCI Global Attractor (gBest)
C_MANTIS = '#39FF14'            # Terminal Green (Coherence Lock)
C_TEXT = '#FFFFFF'              # UI Readout

def run():
    print(f"LOGIC GARDEN 142: BCI SWARM DECODER")
    print(f"Executing: {FPS} FPS | Total: {TOTAL_FRAMES} frames")
    
    # ------------------------------------------------------------------
    # PARTICLE SWARM OPTIMIZATION (PSO) KINEMATICS
    # ------------------------------------------------------------------
    np.random.seed(31415)
    
    N_PARTICLES = 150
    # PSO Parameters
    W = 0.75       # Inertia weight (Maintains current trajectory)
    C1 = 1.2       # Cognitive constant (Pull toward personal best)
    C2 = 2.0       # Social constant (Pull toward BCI Global Best)
    MAX_VEL = 25.0
    
    # Initialize Swarm
    pos = np.random.uniform(low=[100, 300], high=[980, 1600], size=(N_PARTICLES, 2))
    vel = np.random.uniform(low=-10, high=10, size=(N_PARTICLES, 2))
    pbest = np.copy(pos)
    pbest_fit = np.full(N_PARTICLES, np.inf)
    
    # History for visual trails (shape: N_PARTICLES x trail_length x 2)
    trail_len = 8
    history = np.zeros((N_PARTICLES, trail_len, 2))
    for i in range(trail_len):
        history[:, i, :] = pos

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
        # GRID ARCHITECTURE
        # ------------------------------------------------------------------
        # Render the Cortical Array Substrate (Target Matrix)
        for gy in range(200, 1800, 100):
            ax.axhline(gy, color=C_GRID, lw=1, alpha=0.5)
        for gx in range(0, 1080, 100):
            ax.axvline(gx, color=C_GRID, lw=1, alpha=0.5)

        # ------------------------------------------------------------------
        # BCI INTENT CONTROLLER (THE GLOBAL ATTRACTOR)
        # ------------------------------------------------------------------
        bci_active = False
        gbest = None
        target_bloom = 0.0
        
        # Timeline Logic
        if t_sec < 4.0:
            sys_state = "IDLE: STOCHASTIC WANDERING"
            c_state = C_CYAN
        elif t_sec < 13.0:
            sys_state = "BCI LOCK: TARGET ALPHA"
            c_state = C_GOLD
            bci_active = True
            gbest = np.array([540.0, 1400.0])
            target_bloom = min((t_sec - 4.0) * 2, 1.0)
        else:
            sys_state = "BCI SHIFT: TARGET BETA"
            c_state = C_MANTIS
            bci_active = True
            gbest = np.array([540.0, 500.0])
            target_bloom = min((t_sec - 13.0) * 2, 1.0)

        # ------------------------------------------------------------------
        # PSO MATHEMATICS ENGINE
        # ------------------------------------------------------------------
        if bci_active:
            # Calculate fitness (Distance to BCI target)
            dist = np.linalg.norm(pos - gbest, axis=1)
            
            # Update Personal Best
            improved = dist < pbest_fit
            pbest[improved] = pos[improved]
            pbest_fit[improved] = dist[improved]

            # Vectorized PSO Velocity Update
            r1 = np.random.rand(N_PARTICLES, 2)
            r2 = np.random.rand(N_PARTICLES, 2)
            
            cognitive_vel = C1 * r1 * (pbest - pos)
            social_vel = C2 * r2 * (gbest - pos)
            
            vel = (W * vel) + cognitive_vel + social_vel
        else:
            # No BCI. Swarm wanders (Brownian motion)
            vel += np.random.uniform(-2, 2, size=(N_PARTICLES, 2))
            
            # Repel from boundaries
            vel[pos[:, 0] < 50, 0] += 2
            vel[pos[:, 0] > 1030, 0] -= 2
            vel[pos[:, 1] < 250, 1] += 2
            vel[pos[:, 1] > 1650, 1] -= 2

        # Clamp Velocity for visual fluidity
        speeds = np.linalg.norm(vel, axis=1)
        over_limit = speeds > MAX_VEL
        vel[over_limit] = (vel[over_limit].T * (MAX_VEL / speeds[over_limit])).T

        # Update Position
        pos += vel
        
        # Update History memory layout
        history[:, 0:-1, :] = history[:, 1:, :]
        history[:, -1, :] = pos

        # Phase Coherence Metric (How tightly clumped is the swarm?)
        coherence = 0.0
        if bci_active:
            avg_dist = np.mean(np.linalg.norm(pos - gbest, axis=1))
            coherence = max(0.0, 1.0 - (avg_dist / 400.0))

        # ------------------------------------------------------------------
        # VISUAL RENDERING (THE POP)
        # ------------------------------------------------------------------
        # 1. Render BCI Target (The Observer's Intent)
        gamma_pulse = 1.0 if f % 2 == 0 else 0.4 # 30Hz Gamma Lock Visualizer
        
        if bci_active:
            ax.scatter(gbest[0], gbest[1], s=4000 * target_bloom, c=c_state, alpha=0.1 * gamma_pulse, edgecolors='none')
            ax.scatter(gbest[0], gbest[1], s=1000 * target_bloom, c=c_state, alpha=0.3, edgecolors='none')
            ax.add_patch(plt.Circle(gbest, 45, color=c_state, fill=False, lw=4*target_bloom, alpha=target_bloom))
            ax.scatter(gbest[0], gbest[1], s=50, c=C_TEXT, marker='+')
            ax.text(gbest[0] + 60, gbest[1], "gBest [NEURAL LOCK]", color=c_state, fontsize=14, fontname='monospace')

        # 2. Render Particle Swarm
        for i in range(N_PARTICLES):
            pts = history[i]
            
            # Color logic based on BCI engagement and coherence
            if not bci_active:
                c_trail = C_CYAN
                alpha_mult = 0.5
            else:
                p_dist = np.linalg.norm(pos[i] - gbest)
                if p_dist < 50:
                    c_trail = C_MANTIS # Terminal Green when locked
                    alpha_mult = 1.0
                elif p_dist < 150:
                    c_trail = C_GOLD # Pulling into the gravity well
                    alpha_mult = 0.8
                else:
                    c_trail = C_CYAN # Still seeking
                    alpha_mult = 0.6
            
            # Draw Trail
            alphas = np.linspace(0.0, alpha_mult, trail_len)
            for j in range(trail_len - 1):
                ax.plot([pts[j, 0], pts[j+1, 0]], [pts[j, 1], pts[j+1, 1]], color=c_trail, lw=2.5, alpha=alphas[j])
            
            # Draw Head
            head_c = C_TEXT if c_trail == C_MANTIS else c_trail
            ax.scatter(pos[i, 0], pos[i, 1], s=15, c=head_c, zorder=5)

            # Draw pBest faint tether (The cognitive memory)
            if bci_active and pbest_fit[i] < np.inf and (f % 4 == 0):
                if np.linalg.norm(pos[i] - pbest[i]) > 20: 
                    ax.plot([pos[i, 0], pbest[i, 0]], [pos[i, 1], pbest[i, 1]], color=C_MAGENTA, lw=0.5, alpha=0.2, linestyle=':')

        # ------------------------------------------------------------------
        # PROTOCOL: UI DECOUPLING & FLIGHT RECORDER
        # ------------------------------------------------------------------
        # Top Header Overlay
        ax.add_patch(plt.Rectangle((0, 1850), 1080, 70, color=C_VOID, alpha=0.9))
        ax.axhline(1850, color=C_CYAN, lw=2)
        ax.text(40, 1870, "LOGIC GARDEN 142 :: BCI SWARM DECODER", color=C_TEXT, fontsize=24, fontname='monospace', weight='bold')

        # Telemetry Block (Bottom HUD)
        ax.add_patch(plt.Rectangle((0, 0), 1080, 200, color=C_GRID, alpha=0.95))
        ax.axhline(200, color=C_CYAN, lw=2)
        
        ax.text(40, 150, f"STRUCTURAL SCHEMA  : PARTICLE SWARM OPTIMIZATION", color=C_TEXT, fontsize=20, fontname='monospace')
        ax.text(40, 110, f"SWARM INTELLIGENCE : {N_PARTICLES} CORTICAL NODES", color=C_TEXT, fontsize=20, fontname='monospace')
        
        # Coherence Bar Graph
        ax.text(40, 70, f"COHERENCE LOCK     : ", color=C_TEXT, fontsize=20, fontname='monospace')
        ax.add_patch(plt.Rectangle((330, 70), 400, 20, fill=False, edgecolor=C_TEXT, lw=2))
        ax.add_patch(plt.Rectangle((330, 70), 400 * coherence, 20, fill=True, color=c_state))
        
        # State Pulse
        pulse = c_state if (f % 20 < 10) else C_TEXT
        ax.text(40, 25, f"> {sys_state}", color=pulse, fontsize=24, fontname='monospace', weight='bold')

        # The Equations (Faint in background)
        if bci_active:
            ax.text(540, 1780, r"$V_{t+1} = wV_t + c_1 r_1 (pBest - X_t) + c_2 r_2 (gBest - X_t)$", 
                    color=C_CYAN, alpha=0.3, fontsize=18, ha='center', fontname='monospace')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close(fig)

if __name__ == "__main__": run()
