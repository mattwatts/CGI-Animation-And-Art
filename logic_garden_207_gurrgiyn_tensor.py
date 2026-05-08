"""
SOVEREIGN CODE: logic_garden_207_gurrgiyn_tensor.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python Multicore / O(1) Fluid Cavitation Matrix (17.5 seconds)
SCENE: Logic Garden 207 (The Gurrgiyn Tensor / Kinematic Cavitation)
HOTFIX: Incompressible Fluid Repulsion, Sonoluminescence Thermal Bloom, O(N) Array Geometry Alignment
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
import multiprocessing as mp
import os
import gc

# -------- COMPILE-TIME METRICS --------
FPS = 60
DURATION = 17.5                   
TOTAL_FRAMES = int(FPS * DURATION)
OUT_DIR = "frames_207_gurrgiyn"
os.makedirs(OUT_DIR, exist_ok=True)

# -------- THE INDUSTRIAL PALETTE (NEON POP) --------
C_VOID      = '#020205'        # Deep Ocean Vacuum
C_TEXT      = '#FFFFFF'        # Sonoluminescence Flash (Absolute Heat)
C_DIM       = '#111116'        # The Obsolete Target Node
C_CYAN      = '#00FFFF'        # Biological Hardware / Calm Fluid matrix
C_MAGENTA   = '#FF0055'        # Fluid Shear / Division by Zero Tension
C_GOLD      = '#FFD700'        # Micro-Star Thermal Spallation
C_MANTIS    = '#00FF00'        # Terminal Truth / The Strike
C_BLUE      = '#0044FF'        # Dense Ocean Matrix

MAX_PARTICLES = 25000
CENTER_X = 0.0
CENTER_Y = 0.0

def hex_to_rgba(hex_code, alpha=1.0):
    hc = hex_code.lstrip('#')
    return [int(hc[0:2], 16)/255.0, int(hc[2:4], 16)/255.0, int(hc[4:6], 16)/255.0, alpha]

c_cyan = np.array(hex_to_rgba(C_CYAN)[:3])
c_mage = np.array(hex_to_rgba(C_MAGENTA)[:3])
c_gold = np.array(hex_to_rgba(C_GOLD)[:3])
c_blue = np.array(hex_to_rgba(C_BLUE)[:3])

# ------------------------------------------------------------------
# PARALLEL RENDER WORKER
# ------------------------------------------------------------------
def render_frame(packet):
    f, t_sec, state_str, px, py, colors, p_sizes, hammer_ang, void_r, bloom_r, temp_k, is_flash, is_tathata = packet
    
    fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    
    bg_hex = C_TEXT if is_flash else C_VOID
    fig.patch.set_facecolor(bg_hex)
    ax.set_facecolor(bg_hex)
    
    ax.set_xlim(-150, 150)
    ax.set_ylim(-260, 260)

    if not is_flash:
        # THE OBSOLETE TARGET 
        if t_sec < 9.0: # Before total erasure
            ax.scatter([0], [-60], s=8000, facecolor=C_DIM, edgecolor=C_MAGENTA if void_r > 5 else C_CYAN, lw=2, zorder=2)
            ax.text(0, -60, "ERR: COMPROMISED NODE", color=C_TEXT, fontsize=10, fontname='monospace', ha='center', va='center', zorder=3)
        elif is_tathata:
            ax.add_patch(Circle((0, -60), 40, facecolor='none', edgecolor=C_MANTIS, linestyle='--', lw=2, zorder=40))

        # THE O(N) INCOMPRESSIBLE FLUID MATRIX
        if len(px) > 0 and not is_tathata:
            ax.scatter(px, py, s=p_sizes, c=colors, edgecolors='none', alpha=0.8, zorder=10)

        # THE GURRGIYN HAMMER (BIOLOGICAL HARDWARE)
        pivot_x, pivot_y = -100.0, 150.0
        hammer_len = 160.0
        hx = pivot_x + np.cos(hammer_ang) * hammer_len
        hy = pivot_y + np.sin(hammer_ang) * hammer_len
        
        h_color = C_CYAN if void_r < 10 else C_MAGENTA
        if is_tathata: h_color = C_MANTIS
        
        ax.plot([pivot_x, hx], [pivot_y, hy], color=h_color, lw=18, solid_capstyle='round', zorder=20)
        ax.plot([pivot_x, hx], [pivot_y, hy], color=C_TEXT, lw=4, solid_capstyle='round', zorder=21)
        
        # PIVOT NODE
        ax.scatter([pivot_x], [pivot_y], s=800, c=C_VOID, edgecolor=h_color, lw=3, zorder=22)
        ax.scatter([pivot_x], [pivot_y], s=100, c=C_MANTIS if is_tathata else C_TEXT, zorder=23)

        # THE CAVITATION VOID (THE TEAR IN REALITY)
        if void_r > 0.5 and void_r < 200.0:
            ax.add_patch(Circle((hx, hy), void_r, facecolor=C_VOID, edgecolor=C_MAGENTA, lw=3, zorder=30))
        
        # SONOLUMINESCENCE BLOOM
        if bloom_r > 0:
            ax.add_patch(Circle((0, -60), bloom_r, facecolor=C_GOLD, alpha=0.4, zorder=5))
            ax.add_patch(Circle((0, -60), bloom_r*0.6, facecolor=C_TEXT, alpha=0.8, zorder=6))

        # TATHĀTĀ WIREFRAME
        if is_tathata:
            ax.add_patch(Circle((0, -60), 120, facecolor='none', edgecolor=C_MANTIS, lw=3, zorder=40))
            ax.text(0, -210, "STRIKE TRUE. DELETE THE COMPROMISE.", color=C_MANTIS, fontsize=16, fontname='monospace', weight='bold', ha='center', zorder=41)

    # ------------------------------------------------------------------
    # ZERO-TEMPERATURE TELEMETRY WIDGETS
    # ------------------------------------------------------------------
    ui_col = C_CYAN
    if void_r > 5.0: ui_col = C_MAGENTA
    if temp_k > 300: ui_col = C_GOLD
    if is_tathata: ui_col = C_MANTIS
    txt_col = C_TEXT if not is_flash else C_VOID

    # Header Matrix
    ax.text(-140, 240, "LG-207 :: THE GURRGIYN TENSOR", color=ui_col, fontsize=21, fontname='monospace', weight='bold', zorder=80)
    ax.text(-140, 230, "SYSTEM: KINEMATIC CAVITATION / SONOLUMINESCENCE", color=txt_col, fontsize=12, fontname='monospace', zorder=80)
    
    # Kinematic Limits
    strike_v = 0.0 if is_tathata else min(23.0, (temp_k/5000)*23 + (15 if void_r > 1 else 0))
    if t_sec > 7.9 and t_sec < 9.0: strike_v = 23.0
    
    ax.text(-140, -180, f"STRIKE VECTOR ACCEL : {strike_v:05.1f} M/s", color=C_CYAN if (strike_v<20 and not is_tathata) else txt_col, fontsize=14, fontname='monospace', zorder=80)
    ax.text(-140, -195, f"LOCALIZED THERMAL   : {temp_k:05.0f} °C", color=C_GOLD if (temp_k>400 and not is_tathata) else txt_col, fontsize=14, fontname='monospace', zorder=80)

    # Division By Zero Gauge
    ax.text(-140, -220, "FLUID SHEAR / VAPOR PRESSURE THRESHOLD", color=txt_col, fontsize=12, fontname='monospace', zorder=80)
    ax.add_patch(plt.Rectangle((-140, -225), 280, 4, facecolor=C_DIM, zorder=80))
    bar_w = 280 * np.clip(void_r/80.0, 0, 1) if temp_k < 1000 else 280 * (1.0 - np.clip(bloom_r/200, 0, 1))
    if is_tathata: bar_w = 280
    ax.add_patch(plt.Rectangle((-140, -225), bar_w, 4, facecolor=ui_col, zorder=81))

    # Phase Status
    ax.text(-140, -245, f"[{state_str}]", color=ui_col if (f%15<10 or is_tathata) else C_VOID, fontsize=18, fontname='monospace', weight='bold', zorder=80)

    out_path = os.path.join(OUT_DIR, f"frame_{f:04d}.png")
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none')
    fig.clf(); plt.close(fig); gc.collect() 
    return f

# ------------------------------------------------------------------
# O(1) FLUID DISPLACEMENT STREAM
# ------------------------------------------------------------------
def generate_stream():
    # Ambient grid of fluid vectors [PROTOCOL :: GEOMETRIC TRUNCATION HOTFIX]
    # We force the ceiling computation to ensure we never drop below 25,000 spatial nodes.
    gw = int(np.ceil(np.sqrt(MAX_PARTICLES)))
    gx = np.linspace(-160, 160, gw)
    gy = np.linspace(-270, 270, gw)
    X, Y = np.meshgrid(gx, gy)
    
    # Absolute extraction block. This enforces exactly 25,000 nodes.
    px = X.flatten()[:MAX_PARTICLES]
    py = Y.flatten()[:MAX_PARTICLES]
    
    # Store initial grid mathematically to calculate shear distortion
    orig_px = np.copy(px)
    orig_py = np.copy(py)

    for f in range(TOTAL_FRAMES):
        t_sec = f / FPS
        
        is_flash = False
        is_tathata = False
        state = "NOMINAL :: HARDWARE LOCK"
        
        hammer_ang = -np.pi/4 # Start raised
        void_r = 0.0
        bloom_r = 0.0
        temp_k = 20.0
        
        # Phase 1: The Build (0 - 7s)
        if t_sec < 7.0:
            hammer_ang = -np.pi/4 + np.sin(t_sec)*0.05
            void_r = 0.0

        # Phase 2: The Strike & Division by Zero (7.0 - 8.9s)
        elif t_sec < 8.9:
            state = "DIVISION BY ZERO :: VAPOR CAVITY EXPANSION"
            prog = np.clip((t_sec - 7.0) / 1.9, 0, 1)
            # Power curve: slow start, violent finish
            curve = prog**4
            
            hammer_ang = -np.pi/4 - (curve * (np.pi/1.8))
            
            # As hammer moves, void opens behind the pressure wave
            if prog > 0.5:
                void_r = ((prog - 0.5) / 0.5) * 80.0
                
        # Phase 3: The Erasure / Collapse / Sonoluminescence (8.9 - 14.8s)
        elif t_sec < 14.8:
            state = "ERASURE :: O(1) SONOLUMINESCENCE CASCADE"
            prog = (t_sec - 8.9) / 5.9
            
            hammer_ang = -np.pi/4 - (np.pi/1.8) # Hammer is fully down
            
            # The Collapse is brutal and instantaneous
            if prog < 0.02:
                void_r = 80.0 * (1.0 - (prog / 0.02))
            else:
                void_r = 0.0
                if prog < 0.05: # Pure C_TEXT Flash
                    is_flash = True
                    temp_k = 4700.0
                else:
                    # Dissipating Thermal bloom
                    bloom_r = ((prog - 0.05)/0.2) * 200.0 if prog < 0.25 else 200.0 - ((prog - 0.25)/0.75)*200.0
                    temp_k = 4700.0 * (1.0 - prog)
                    
        # Phase 4: Tathātā (14.8 - 17.5s)
        else:
            state = "TATHĀTĀ :: WEAPONIZED VOID. THE STRIKE TRUE."
            is_tathata = True
            hammer_ang = -np.pi/4 - (np.pi/1.8)
            void_r = 0.0
            bloom_r = 0.0
            
            if t_sec < 14.95:
                is_flash = True

        # Fluid Displacement Logic (Applying the Tension Tensor)
        pivot_x, pivot_y = -100.0, 150.0
        hammer_len = 160.0
        hx = pivot_x + np.cos(hammer_ang) * hammer_len
        hy = pivot_y + np.sin(hammer_ang) * hammer_len

        # Vectors representing the physical push of the hammer and the void
        dx = orig_px - hx
        dy = orig_py - hy
        dist = np.sqrt(dx**2 + dy**2)
        dist = np.maximum(dist, 1.0)
        
        # Rigid O(N) mapping ensures no scalar indexes
        push_factor = np.zeros_like(orig_px)
        
        if 7.0 <= t_sec < 8.9:
            # Water violently shearing away from the hammer
            push_factor = (80.0 / dist) * (void_r/80.0) * 40.0
            
        elif 8.9 <= t_sec < 9.5:
            # Ocean violently rushing back IN to crush the void
            push_factor = -(100.0 / dist) * (1.0 - ((t_sec-8.9)/0.6)) * 60.0
            
        px_current = orig_px + (dx / dist) * push_factor
        py_current = orig_py + (dy / dist) * push_factor

        # Fluid Chromatic Distortion
        colors = np.zeros((MAX_PARTICLES, 3))
        
        # Base Ocean deep blue
        colors[:, :] = c_blue
        
        # Shear tension becomes Magenta
        shear = np.abs(push_factor) / 40.0
        shear = np.clip(shear, 0, 1)[:, None]
        colors = (1.0 - shear) * colors + shear * c_mage
        
        # Thermal bloom makes fluid Gold
        if temp_k > 100:
            dx_c = px_current - 0
            dy_c = py_current - (-60)
            dist_c = np.sqrt(dx_c**2 + dy_c**2)
            heat_inf = np.clip((bloom_r - dist_c) / 50.0, 0, 1)[:, None]
            colors = (1.0 - heat_inf) * colors + heat_inf * c_gold

        p_sizes = 6.0 + (shear.flatten() * 10.0)

        yield (f, t_sec, state, np.copy(px_current), np.copy(py_current), colors, p_sizes, hammer_ang, void_r, bloom_r, temp_k, is_flash, is_tathata)

def run_batch():
    cpu_cores = mp.cpu_count()
    print(f"LOGIC GARDEN 207: THE GURRGIYN TENSOR [CORES: {cpu_cores}]")
    print(f"Executing HOTFIX: O(N) Array Geometry Alignment")
    
    with mp.Pool(processes=cpu_cores) as pool:
        for finished_frame in pool.imap_unordered(render_frame, generate_stream(), chunksize=8):
            pass
    print("Compilation Complete. Zero-Friction parameters held.")

if __name__ == "__main__": 
    mp.freeze_support() 
    run_batch()
