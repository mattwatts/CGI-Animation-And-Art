"""
SOVEREIGN CODE: logic_garden_131_the_imaginary_axis.py
FORMAT: YouTube Shorts (1080x1920)
SYSTEM: Python High-Fidelity Simulator
SCENE: Logic Garden 131 (Euler's Shadow / Phase Coherence)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
import os

# CONFIG
FPS = 30
DURATION = 24
TOTAL_FRAMES = FPS * DURATION
OUT_DIR = "frames_131_the_imaginary_axis"
os.makedirs(OUT_DIR, exist_ok=True)

# THE INDUSTRIAL PALETTE
C_VOID = '#050510'           # Absolute Vacuum
C_GRID_BACK = '#112233'      # Muted Structural Wall Grid (Real Matrix)
C_GRID_FLOOR = '#331122'     # Muted Structural Floor Grid (Imaginary Matrix)
C_REAL = '#00FFCC'           # Cyan (The Observable / Amplitude)
C_IMAG = '#FF003C'           # Radiant Red (The Hidden Conjugate / Phase)
C_COMPLEX = '#FFD700'        # Gold (The True Unified State / Helix)
C_TETHER = '#FFFFFF'         # White Projection Binding
C_TEXT = '#FFFFFF'           # UI Protocol
C_DIM = '#555577'            # Subdued UI text

def project_iso(t, im, re, CX=200, CY=1200, scale=0.85):
    """
    Protocol: MATHEMATICAL RIGIDNESS (Isometric Mapping).
    t: Space/Time (Angle 330: Right-Down)
    im: The Hidden Phase (Angle 150: Left-Up, receding)
    re: The Observable Amplitude (Angle 90: Straight Up)
    """
    ang_t = math.radians(-30)
    ang_im = math.radians(150)
    
    # Scale applied at root to guarantee 1080x1920 fit
    t *= scale
    im *= scale
    re *= scale
    
    px = CX + (t * math.cos(ang_t)) + (im * math.cos(ang_im))
    py = CY + (t * math.sin(ang_t)) + (im * math.sin(ang_im)) + re
    return px, py

def draw_bloom_line(ax, x, y, color, lw, alpha=1.0, zorder=5):
    """Protocol: NEON POP. Triple-layer Gaussian distribution decay."""
    if alpha <= 0: return
    ax.plot(x, y, color=color, lw=lw, alpha=alpha, zorder=zorder)
    ax.plot(x, y, color=color, lw=lw*3, alpha=alpha*0.4, zorder=zorder-1)
    ax.plot(x, y, color=color, lw=lw*10, alpha=alpha*0.1, zorder=zorder-2)

def draw_grid_wall(ax, t_max, R, alpha):
    """Constructs the rigid 'Real' observable geometry."""
    if alpha <= 0: return
    # Horizontal lines
    for re_val in np.linspace(-R, R, 9):
        x_pts, y_pts = [], []
        for t_val in [0, t_max]:
            px, py = project_iso(t_val, R, re_val)
            x_pts.append(px)
            y_pts.append(py)
        ax.plot(x_pts, y_pts, color=C_GRID_BACK, lw=2, alpha=alpha, zorder=1)
    # Vertical lines
    for t_val in np.linspace(0, t_max, 15):
        x_pts, y_pts = [], []
        for re_val in [-R, R]:
            px, py = project_iso(t_val, R, re_val)
            x_pts.append(px)
            y_pts.append(py)
        ax.plot(x_pts, y_pts, color=C_GRID_BACK, lw=2, alpha=alpha, zorder=1)

def draw_grid_floor(ax, t_max, R, alpha):
    """Constructs the hidden 'Imaginary' depth geometry."""
    if alpha <= 0: return
    # Horizontal lines
    for im_val in np.linspace(-R, R, 9):
        x_pts, y_pts = [], []
        for t_val in [0, t_max]:
            px, py = project_iso(t_val, im_val, -R)
            x_pts.append(px)
            y_pts.append(py)
        ax.plot(x_pts, y_pts, color=C_GRID_FLOOR, lw=2, alpha=alpha, zorder=1)
    # Vertical lines
    for t_val in np.linspace(0, t_max, 15):
        x_pts, y_pts = [], []
        for im_val in [-R, R]:
            px, py = project_iso(t_val, im_val, -R)
            x_pts.append(px)
            y_pts.append(py)
        ax.plot(x_pts, y_pts, color=C_GRID_FLOOR, lw=2, alpha=alpha, zorder=1)

def ease(t):
    return t * t * (3.0 - 2.0 * t)

def run():
    print(f"LOGIC GARDEN 131: THE IMAGINARY AXIS ({TOTAL_FRAMES} frames)")
    
    # Mathematical Bounds
    T_MAX = 1200 # Length of the spatial progression
    R = 250      # Radius of the complex helix (Amplitude)
    
    # Timing Phases
    F_PHASE2 = 120   # Begin floor fade (Imaginary)
    F_PHASE3 = 300   # Begin helix fade (Truth)
    F_PHASE4 = 480   # Full operation / Binding tethers activate
    
    t_array = np.linspace(0, T_MAX, 600)
    
    for f in range(TOTAL_FRAMES):
        fig = plt.figure(figsize=(10.8, 19.2), dpi=100)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        fig.patch.set_facecolor(C_VOID)
        ax.set_facecolor(C_VOID)
        
        ax.set_xlim(0, 1080)
        ax.set_ylim(0, 1920)
        
        # --- PHASE LOGIC (Friction to Flow) ---
        alpha_real = 1.0 # Always visible
        
        p2_prog = min(1.0, max(0.0, (f - F_PHASE2) / 60.0))
        alpha_imag = ease(p2_prog)
        
        p3_prog = min(1.0, max(0.0, (f - F_PHASE3) / 90.0))
        alpha_helix = ease(p3_prog)
        
        p4_prog = min(1.0, max(0.0, (f - F_PHASE4) / 45.0))
        alpha_tethers = ease(p4_prog) * 0.4
        
        # UI Text Logic
        status_text = "OBSERVABLE REALITY: 1D OSCILLATION"
        status_color = C_REAL
        if f >= F_PHASE4:
            status_text = "TRUTH: ROTATION CASTS AN OSCILLATING SHADOW"
            status_color = C_COMPLEX
        elif f >= F_PHASE3:
            status_text = "EULER'S IDENTITY: 3D ROTATIONAL PHASE"
            status_color = C_COMPLEX
        elif f >= F_PHASE2:
            status_text = "INTRODUCTION OF ORTHOGONAL OPERATOR (i)"
            status_color = C_IMAG
            
        # --- THE PHYSICS ENGINE ---
        # The wave propagates forward while continuously spinning
        # e^(i * (kx - wt)) = cos(kx - wt) + i sin(kx - wt)
        k = 0.02 # Spatial frequency
        w = 0.08 # Temporal spin frequency
        time_offset = f * w
        
        re_vals = R * np.cos(k * t_array - time_offset)
        im_vals = R * np.sin(k * t_array - time_offset)
        
        # --- RENDERING THE ENVIRONMENT ---
        # Draw the structural matrix bounds
        draw_grid_floor(ax, T_MAX, R, alpha=alpha_imag)
        draw_grid_wall(ax, T_MAX, R, alpha=alpha_real)
        
        # --- 1. THE IMAGINARY SHADOW (The Floor) ---
        if alpha_imag > 0:
            x_im, y_im = [], []
            for i in range(len(t_array)):
                px, py = project_iso(t_array[i], im_vals[i], -R)
                x_im.append(px)
                y_im.append(py)
            draw_bloom_line(ax, x_im, y_im, C_IMAG, lw=4, alpha=alpha_imag, zorder=2)
            
        # --- 2. THE REAL SHADOW (The Wall) ---
        x_re, y_re = [], []
        for i in range(len(t_array)):
            px, py = project_iso(t_array[i], R, re_vals[i])
            x_re.append(px)
            y_re.append(py)
        draw_bloom_line(ax, x_re, y_re, C_REAL, lw=4, alpha=alpha_real, zorder=3)
        
        # --- 3. THE QUANTUM HELIX (The True Object) ---
        if alpha_helix > 0:
            x_cx, y_cx = [], []
            for i in range(len(t_array)):
                px, py = project_iso(t_array[i], im_vals[i], re_vals[i])
                x_cx.append(px)
                y_cx.append(py)
            draw_bloom_line(ax, x_cx, y_cx, C_COMPLEX, lw=6, alpha=alpha_helix, zorder=5)

            # Draw the leading node (The Particle)
            ax.add_patch(plt.Circle((x_cx[-1], y_cx[-1]), 15 * alpha_helix, color=C_TEXT, zorder=10))
            ax.add_patch(plt.Circle((x_cx[-1], y_cx[-1]), 30 * alpha_helix, color=C_COMPLEX, alpha=0.5, zorder=9))

        # --- 4. THE PROJECTION TETHERS (The Mathematical Proof) ---
        if alpha_tethers > 0:
            for i in range(0, len(t_array), 25): # Draw binding lines every Nth index
                # Origin point on the Helix
                h_px, h_py = project_iso(t_array[i], im_vals[i], re_vals[i])
                
                # Drop to Real Wall
                r_px, r_py = project_iso(t_array[i], R, re_vals[i])
                ax.plot([h_px, r_px], [h_py, r_py], color=C_REAL, lw=1.5, alpha=alpha_tethers, linestyle='--', zorder=4)
                
                # Drop to Imag Floor
                i_px, i_py = project_iso(t_array[i], im_vals[i], -R)
                ax.plot([h_px, i_px], [h_py, i_py], color=C_IMAG, lw=1.5, alpha=alpha_tethers, linestyle='--', zorder=4)

        # --- UI OVERLAYS (HUD) ---
        ax.text(540, 1820, "Complex Numbers", color=C_TEXT, ha='center', fontsize=35, fontname='monospace', weight='bold')
        ax.text(540, 1760, status_text, color=status_color, ha='center', fontsize=22, fontname='monospace', weight='bold')

        # Telemetry Block
        hud_y = 150
        ax.text(80, hud_y, "SYSTEM EQUATION:", color=C_DIM, fontsize=20, fontname='monospace')
        ax.text(370, hud_y, "f(x,t) = e^(i(kx - ωt))", color=C_COMPLEX if alpha_helix > 0 else C_VOID, fontsize=24, fontname='monospace', weight='bold')
        
        ax.text(80, hud_y - 40, "REAL MATRIX:", color=C_DIM, fontsize=18, fontname='monospace')
        ax.text(280, hud_y - 40, "Re = cos(kx - ωt)", color=C_REAL, fontsize=20, fontname='monospace', weight='bold')
        
        ax.text(80, hud_y - 75, "IMAG MATRIX:", color=C_DIM, fontsize=18, fontname='monospace')
        ax.text(280, hud_y - 75, "Im = sin(kx - ωt)", color=C_IMAG if alpha_imag > 0 else C_VOID, fontsize=20, fontname='monospace', weight='bold')

        plt.savefig(os.path.join(OUT_DIR, f"frame_{f:04d}.png"), facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close(fig)

if __name__ == "__main__": run()
